import network
from umqtt.simple import MQTTClient
from machine import Pin
import dht
import time

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_CLIENT_ID = "ESP32_SENSOR"
MQTT_TOPIC_TEMP = "utng/sensorTH"
MQTT_TOPIC_HUM = "utng/sensorTH"
MQTT_PORT = 1883

# Configurar el sensor KY-015 (DHT11) en GPIO 4
sensor = dht.DHT11(Pin(4))

# Conectar a WiFi
def conectar_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    for _ in range(30):  # Esperar hasta 9 segundos
        if sta_if.isconnected():
            print("WiFi conectada!")
            return
        time.sleep(0.3)
    print("Error: No se pudo conectar a WiFi")
    return

# Conectar a MQTT
def conectar_broker():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.connect()
        print(f"Conectado a MQTT Broker: {MQTT_BROKER}")
        return client
    except Exception as e:
        print(f"Error al conectar con MQTT: {e}")
        return None

# Iniciar conexiones
conectar_wifi()
client = conectar_broker()

if client:
    while True:
        try:
            sensor.measure()  # Leer datos del KY-015 (DHT11)
            temperatura = sensor.temperature()
            humedad = sensor.humidity()

            print(f"Temperatura: {temperatura}°C, Humedad: {humedad}%")

            # Enviar datos por MQTT
            client.publish(MQTT_TOPIC_TEMP, str(temperatura))
            client.publish(MQTT_TOPIC_HUM, str(humedad))

            time.sleep(5)  # Esperar 5 segundos antes de la siguiente lectura
        except Exception as e:
            print(f"Error en el loop MQTT: {e}")
            time.sleep(5)
