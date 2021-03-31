# Import
import micropython
import gc
from urequests import request, put
import ujson
import network
import uasyncio as asyncio
import esp32
import sys
from machine import I2C, Pin

# End Import

# Global Vars
NETWORK_CONNECTIVITY = False
I2C_DEVICES_ADDR = [0x50, 0x68, 0x7f]
I2C_DATA_BROADCAST = {row: {col: "n/a" for col in range(1, 4)} for row in I2C_DEVICES_ADDR}
BOOK_STATUS = {row: {col: 0 for col in range(1, 4)} for row in range(1, 4)}
GET = "GET"

AUTH_HEADER = {"Authorization": "Token c0d3ad98c5f072042023198171c76bb56f565bd2", "Content-Type": "application/json"}

# End Global Flag

class NetworkManager:
    MODE = network.STA_IF
    class WiFiMeta:
        SSID = "HPCNC801"
        PASSWORD = "1q2w3e4r"
    def __init__(self, event_loop):
        print("SET UP CONFIGURATION ...")
        self.dla = network.WLAN(self.MODE)
        self.dla.active(True)
        self.event_loop = event_loop

    async def _connect(self):
        global NETWORK_CONNECTIVITY
        print("Connecting to network ...")
        self.dla.connect(self.WiFiMeta.SSID, self.WiFiMeta.PASSWORD)
        while not self.dla.isconnected():
            print("Retrying ...")
            await asyncio.sleep(1)
        NETWORK_CONNECTIVITY = True
        print("Success ...")

    def start(self):
        if self.MODE == network.STA_IF:
            self.event_loop.create_task(self.STA_LOOP())
        else:
            pass
    
    async def STA_LOOP(self, silent=True):
        global NETWORK_CONNECTIVITY
        while True:
            if self.dla.isconnected():
                if not silent: print("Heartbeat from NetworkManager")
                await asyncio.sleep(3)
            else:
                # Regain Connection
                await self._connect()
                await asyncio.sleep(0)
        pass


class Broadcaster:
    I2C_SCL_PIN = 32
    I2C_SDA_PIN = 33
    I2C_FREQ = 400000

    def __init__(self, event_loop):
        print("Initializing I2C Master")
        self.COMM = I2C(scl=Pin(self.I2C_SCL_PIN), sda=Pin(self.I2C_SDA_PIN))
        print("Master Initialized ...")
        self.event_loop = event_loop
        print("Performing Scan ...")
        scan_result = self.COMM.scan()
        print("Available channel:", scan_result)

    def formatter(self, addr, col, data):
        formaddr = addr << 1
        data = "{}|{}|{}".format(formaddr, col, data)
        return data

    async def send_data(self, addr: int, row_data, retries: int = 3):
        acks = None
        for col, data in row_data.items():
            try:
                if not isinstance(data, dict): continue
                to_send = self.formatter(addr, col, data)
                acks = self.COMM.writeto(addr, to_send)
                await asyncio.sleep_ms(500)  # I2C Delay
            except OSError as e:
                if retries > 0:
                    print("I2C Error while sending data ...")
                    retries -= 1
                else:
                    raise e
            return acks
    
    async def broadcast(self, addresses: list, datum: dict, tolerate=True):
        """
        Addresses `addresses` of devices should be static and all data in `datum` are dynamically changed by other task.
        """
        for device_index, device_address in enumerate(addresses):
            try: acks = await self.send_data(device_address, datum[device_address]) # NOTE: datum[device_address] need transformation first
            except OSError as e:
                if not tolerate: raise e
            await asyncio.sleep_ms(1000)  # I2C Delay
        await asyncio.sleep(5)

    def start(self):
        global I2C_DEVICES_ADDR
        global I2C_DATA_BROADCAST
        print("Start broadcasting to I2C...")
        self.event_loop.create_task(self.broadcast(I2C_DEVICES_ADDR, I2C_DATA_BROADCAST))


class ServerCommunicator:
    class Meta:
        FETCH_URL = r"http://158.108.38.149:8000/shelf-info/"
        UPDATE_URL = r"http://158.108.38.149:8000/shelf-update/"
        HEARTBEAT_URL = r"http://158.108.38.149:8000/heart-beat/"
    
    def __init__(self, event_loop):
        print("Initiating Server Communication ...")
        self.event_loop = event_loop

    def fetch_serializer(self, data):
        global I2C_DATA_BROADCAST
        if data.status_code == 200:
            datum = data.json()
            for data in datum:
                # Update book name for broadcasting
                I2C_DATA_BROADCAST[I2C_DEVICES_ADDR[data['row'] - 1]][data['col']] = data['current_book']['title']
        else:
            print("Unable to fetch data", data.status_code, data.reason)

    def send_serializer(self, data):
        to_send = []
        for row, row_data in data.items():
            for col, status in row_data.items():
                temp = {"row": row, "col": col, "shelf_status": status}
                to_send.append(temp)
        return to_send

    async def fetch_data(self):
        global GET
        global I2C_DATA_BROADCAST
        while True:
            r = None
            try:
                r = request(GET, self.Meta.FETCH_URL)
                self.fetch_serializer(r)
            except OSError as e:
                print("Error while requesting data", e)
            except Exception as e:
                print("Other exception caughted while requesting ", e)
            finally:
                if not r is None: r.close()
            print("Current Table:")
            print(I2C_DATA_BROADCAST)
            await asyncio.sleep(15)
    
    async def send_data(self):
        global BOOK_STATUS
        while True:
            to_send = BOOK_STATUS.copy()
            to_send = self.send_serializer(to_send)
            r = None
            try:
                gc.collect()
                r = put(url=self.Meta.UPDATE_URL, json=to_send, headers=AUTH_HEADER)
                if r.status_code != 200:
                    raise Exception("Failed", r.status_code, r.reason, r.text)
            except OSError as e:
                print("Error while sending data ", e)
            except Exception as e:
                print("Other exception caughted while sending", e)
            finally:
                if not r is None: r.close()
            await asyncio.sleep(15)

    def start(self):
        print("Starting Communication Coroutines")
        self.event_loop.create_task(self.fetch_data())
        self.event_loop.create_task(self.send_data())


# END TASK CLASS

def diag_function(func, funcname):
    val = None
    try:
        val = func()
    except Exception as e:
        print(funcname, val,  "Failed")
        return 0
    else:
        print(funcname, val, "Ok")
        return True

async def main():
    print("System Awake")
    print("Memory")
    print(micropython.mem_info())
    print("Running Self-Check")
    passed = 0
    passed += diag_function(esp32.hall_sensor, 'Hall sensor')
    passed += diag_function(esp32.raw_temperature, 'Temperature sensor')
    passed += diag_function(esp32.ULP, 'Ultra Low-Power Co-processor (ULC)')
    print("Basic function passed", passed, "/", 3)
    print("Global Variables")
    print("NETWORK_CONNECTIVITY", NETWORK_CONNECTIVITY)
    print("Devices List:")
    print(I2C_DATA_BROADCAST)
    event_loop = asyncio.get_event_loop()
    print("Starting Network Manager ...")
    networkManager = NetworkManager(event_loop=event_loop)
    networkManager.start()
    print("Starting I2C Manager")
    broadcastManager = Broadcaster(event_loop=event_loop)
    broadcastManager.start()
    print("Starting Server fetcher")
    serverComm = ServerCommunicator(event_loop=event_loop)
    serverComm.start()


    # Nothing shall go below this line
    event_loop.run_forever()
    
if __name__ == '__main__':
    asyncio.run(main())
