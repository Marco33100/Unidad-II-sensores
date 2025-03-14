#import para acceso a red
import network
#Para usar protocolo MQTT
from umqtt.simple import MQTTClient

#Importamos modulos necesarios
from machine import Pin
from time import sleep

#Propiedades para conectar a un cliente MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/actuadorActivoBuzzer"

MQTT_PORT = 1883

# Configuración del sensor de led
buzzer = Pin(14, Pin.OUT)


#Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect('ANTONIOBM', '12345678')
    while not sta_if.isconnected():
        print(".", end="")
        sleep(0.3)
    print("\nWiFi Conectada!")

#Funcion para subscribir al broker, topic
def conecta_broker():
    client = MQTTClient(MQTT_CLIENT_ID,
    MQTT_BROKER, port=MQTT_PORT,
    user=MQTT_USER,
    password=MQTT_PASSWORD,
    keepalive=0)
    client.connect()
    print("Conectado a %s, en el topico %s"%(MQTT_BROKER, MQTT_TOPIC))
    return client

#Conectar a wifi
conectar_wifi()
#Conectando a un broker mqtt
client = conecta_broker()

while True:
    buzzer.value(1)
    print("Buzzer activado")
    client.publish(MQTT_TOPIC, "Buzzer activado")
    sleep(1)
    
    buzzer.value(0)
    print("Buzzer desactivado")
    client.publish(MQTT_TOPIC, "Buzzer desactivado")
    sleep(1)