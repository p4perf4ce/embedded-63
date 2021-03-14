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