
# import network
# from urequests import request
# import ujson
# import time
# from machine import Pin
# interrupt_pin = 9999
# ssid = "a"
# password = "1234567890"
# change = False

# def connect():
#     station = network.WLAN(network.STA_IF)
 
#     if station.isconnected() == True:
#         print("Already connected")
#         return
    
#     station.active(True)
#     station.connect(ssid, password)
    
#     while not station.isconnected():
#         time.sleep(0.5)
#         print("connecting...")
        
#     print("Connection successful")
#     print(station.ifconfig())

# def post_book():
#     post_data = ujson.dumps({'kuy':'hee'})
#     url = ''
#     headers = {'content-type': 'application/json'}
#     res = request("post",headers,url,post_data).json()
#     #return r.text
#     return ujson.dumps({'name':'hee'})

# def interrupt_handle(pin):
#     global change
#     global interrupt_pin
#     change = True
#     interrupt_pin = pin
    
# def i2c_write():
#     i2c.writeto(0x90,b'Hello World' )
#     print("write to i2c")
    
# i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100000)    
# #main
# i2c_write()
# '''
# #connect()
# hee1 = Pin(39,Pin.IN)
# hee2 = Pin(35,Pin.IN)
# hee3 = Pin(34,Pin.IN)
# hee1.irq(trigger=3, handler=interrupt_handle)
# hee2.irq(trigger=3, handler=interrupt_handle)
# hee3.irq(trigger=3, handler=interrupt_handle)
# i = 0
# while True:
#     print(i," ",hee1.value() , " " , hee2.value() , " " , hee3.value())
#     time.sleep(1)
#     i = i + 1
#     if change:
#         print("change on pin ",interrupt_pin)
#         i2c_write()
#         time.sleep(2)
#         change = False
#         print("Done...")
        
# '''
# '''
# #i2c = I2C(scl=Pin(22),sda=Pin(21),freq=100000)

# #print("Scanning I2C bus... found",i2c.scan())
# #time.sleep(0.5)

# #while True:
#  #   print("Send data to STM32...")
#   #  i2c.writeto(0x90, )
# '''
# '''
import time
from machine import Pin,I2C
import random
i2c = I2C(scl=Pin(22),sda = Pin(21),freq=100000)

while True:
    count = str(random.randint(1,10))
    #count = '1'
    print("Request ",count ," blinks to STM32...")
    i2c.writeto(0x50,"hee")
    time.sleep(2)