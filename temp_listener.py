import time
import requests
import RPi.GPIO as GPIO

dweetIO = "https://dweet.io/get/latest/dweet/for/"
myThing = "bujoldzack_raspi"
TEMP_THRESHOLD = 25
LED_PIN_TEMP = 20

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_PIN_TEMP, GPIO.OUT)

def temperature_listener():
    while True:
        try:
            response = requests.get(dweetIO + myThing)
            response_data = response.json()
            temp = response_data['with'][0]['content']['temperature']
            
            if temp > TEMP_THRESHOLD:
                GPIO.output(LED_PIN_TEMP, GPIO.HIGH)
                print("Temperature > 25°C - LED ON")
            else:
                GPIO.output(LED_PIN_TEMP, GPIO.LOW)
                print("Temperature <= 25°C - LED OFF")
            
            time.sleep(5)

        except Exception as e:
            print("Error in temperature listener:", e)
            time.sleep(5)

if __name__ == '__main__':
    try:
        temperature_listener()
    except KeyboardInterrupt:
        GPIO.cleanup()
        print("Temperature listener stopped")
