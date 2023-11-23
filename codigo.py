import dht
from machine import Pin
from time import sleep
import network
import time
from math import sin
from umqtt.simple import MQTTClient

wifi_ssid = "Inteli-welcome"
wifi_password = ""

dt11_sensor = dht.DHT11(Pin(10))

def read_dht11sensor():
    try:
        sleep(2)
        dt11_sensor.measure()
        temp = dt11_sensor.temperature()
        hum = dt11_sensor.humidity()
        temp_f = temp * (9/5) + 32.0
        return [temp, hum]
    
    except OSError as e:
        print('Failed to read sensor')
        return "Error"


wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(wifi_ssid, wifi_password)
while wlan.isconnected() == False:
    print('Waiting for connection...')
    time.sleep(1)
print("Connected to WiFi")


mqtt_host = "industrial.api.ubidots.com"
mqtt_username = "BBUS-qOL1fqXidPJoIMJBj0f3KbjLqDug0Q" 
mqtt_password = "" 
mqtt_publish_topic = "/v1.6/devices/demo/temp" 

mqtt_client_id = "somethingreallyrandomandunique123"

mqtt_client = MQTTClient(
        client_id=mqtt_client_id,
        server=mqtt_host,
        user=mqtt_username,
        password=mqtt_password)

mqtt_client.connect()

try:
    while True:
        dht11 = read_dht11sensor()
        humidity = dht11[1]
        
        print(f'Publish {humidity:.2f}')
        mqtt_client.publish(mqtt_publish_topic, str(humidity))
        
        time.sleep(3)
except Exception as e:
    print(f'Failed to publish message: {e}')
finally:
    mqtt_client.disconnect()



