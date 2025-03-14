import network
from umqtt.simple import MQTTClient
import time
import machine

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = "ESP32_SensorMercurio"
MQTT_TOPIC = "utng/sensorBoton"
MQTT_PORT = 1883

# Configuración del botón
BUTTON_PIN = 4  # Pin GPIO donde está conectado el botón
button = machine.Pin(BUTTON_PIN, machine.Pin.IN, machine.Pin.PULL_UP)  # Configura el pin como entrada con pull-up

# Función para conectar a WiFi
def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    while not sta_if.isconnected():
        print(".", end="")
        time.sleep(0.3)
    print("\nWiFi Conectada!")

# Función para conectar al broker MQTT
def conectar_broker():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect()
    print(f"Conectado a MQTT Broker: {MQTT_BROKER}, Topic: {MQTT_TOPIC}")
    return client

# Función para publicar un mensaje MQTT cuando se presiona el botón
def publicar_mensaje(client):
    mensaje = "Click"
    client.publish(MQTT_TOPIC, mensaje)
    print(f"Mensaje publicado: {mensaje}")

# Conectar a WiFi y MQTT
conectar_wifi()
client = conectar_broker()

# Bucle principal para detectar la presión del botón
while True:
    if button.value() == 0:  # El botón se presiona cuando el valor es bajo (0)
        print("Botón presionado...")
        publicar_mensaje(client)
        time.sleep(1)  # Para evitar múltiples publicaciones por un solo click
    time.sleep(0.1)  # Pequeña pausa para evitar sobrecargar el microcontrolador
