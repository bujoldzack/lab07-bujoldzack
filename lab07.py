import time
import requests
from w1thermsensor import W1ThermSensor
import ADC0832
import RPi.GPIO as GPIO

dweetIO = "https://dweet.io/dweet/for/"
myThing = "bujoldzack_raspi"
MAX_VOLTAGE = 3.3
MAX_ADC_VALUE = 255
LED_PIN_LIGHT = 26

sensor = W1ThermSensor()
ADC0832.setup()
GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_LIGHT, GPIO.OUT)

def get_lux(adc_value):
    voltage = MAX_VOLTAGE / MAX_ADC_VALUE * adc_value
    lux = voltage * 100
    return lux

n = 15

while n > 0:
    temp = sensor.get_temperature()

    adc_value = ADC0832.getADC(0)
    lux = get_lux(adc_value)
   
    if lux < 10:
        GPIO.output(LED_PIN_LIGHT, GPIO.LOW)
    else:
        GPIO.output(LED_PIN_LIGHT, GPIO.HIGH)
    
    rqsString = f"{dweetIO}{myThing}?temperature={temp}&lux={lux}"
    print(rqsString)
    rqs = requests.post(rqsString)
    print(rqs.status_code)
    print(rqs.headers)
    print(rqs.content)
    
    time.sleep(5)
    n -= 1

ADC0832.destroy()
GPIO.cleanup()
