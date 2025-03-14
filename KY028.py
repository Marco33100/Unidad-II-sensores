import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
import time

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/sensor028"
MQTT_PORT = 1883

# Configurar pines del módulo KY-028 (Sensor de temperatura)
sensor_analogico = ADC(Pin(34))  # Pin analógico para temperatura
sensor_analogico.atten(ADC.ATTN_11DB)  # Rango de 0 a 3.3V
sensor_digital = Pin(15, Pin.IN)  # Pin digital para umbral

# Conectar a WiFi
def conectar_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    for _ in range(30):  # Esperar 9 segundos máximo
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
        print(f"Conectado a MQTT Broker: {MQTT_BROKER}, Topic: {MQTT_TOPIC}")
        return client
    except Exception as e:
        print(f"Error al conectar con MQTT: {e}")
        return None

# Iniciar conexiones
conectar_wifi()
client = conectar_broker()

# Bucle infinito para leer el sensor
while True:
    valor_analogico = sensor_analogico.read()  # Leer temperatura en escala 0-4095
    estado_digital = sensor_digital.value()  # Leer umbral digital
    mensaje = f"Temperatura: {valor_analogico}, Umbral: {'Alto' if estado_digital else 'Bajo'}"
    print(mensaje)
    if client:
        client.publish(MQTT_TOPIC, mensaje)
    time.sleep(2)