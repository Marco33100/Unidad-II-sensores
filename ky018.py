import network
from umqtt.simple import MQTTClient
from machine import Pin, ADC
import time
import math

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_CLIENT_ID = "ESP32_SENSOR"
MQTT_TOPIC_TEMP = "utng/sensorTemperatura"
MQTT_PORT = 1883

# Configurar el sensor KY-013 en un pin analógico (por ejemplo, GPIO 34)
sensor_temp = ADC(Pin(34))
sensor_temp.atten(ADC.ATTN_11DB)  # Configurar el rango de lectura de 0 a 3.3V

# Parámetros del termistor NTC (ajusta según las especificaciones de tu sensor)
BETA = 3950  # Coeficiente Beta del termistor
R_NOMINAL = 10e3  # Resistencia nominal a 25°C (10kΩ)
T_NOMINAL = 25 + 273.15  # Temperatura nominal en Kelvin (25°C)

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
        print(f"Conectado a MQTT Broker: {MQTT_BROKER}, Topic: {MQTT_TOPIC_TEMP}")
        return client
    except Exception as e:
        print(f"Error al conectar con MQTT: {e}")
        return None

# Convertir el valor analógico a temperatura
def leer_temperatura():
    # Leer el valor analógico del KY-013
    valor_analogico = sensor_temp.read()

    # Convertir el valor analógico a voltaje (0-3.3V)
    voltaje = (valor_analogico / 4095) * 3.3

    # Calcular la resistencia del termistor
    resistencia = (3.3 * 10e3) / voltaje - 10e3

    # Calcular la temperatura usando la ecuación del termistor NTC
    temperatura_kelvin = 1 / (1/T_NOMINAL + (1/BETA) * math.log(resistencia / R_NOMINAL))
    temperatura_celsius = temperatura_kelvin - 273.15

    return temperatura_celsius

# Iniciar conexiones
conectar_wifi()
client = conectar_broker()

if client:
    while True:
        try:
            # Leer la temperatura del KY-013
            temperatura = leer_temperatura()

            # Mostrar la temperatura en el monitor serial
            print(f"Temperatura: {temperatura:.2f}°C")

            # Publicar la temperatura en el tópico MQTT
            client.publish(MQTT_TOPIC_TEMP, str(temperatura))

            time.sleep(2)  # Esperar 2 segundos antes de tomar otra lectura

        except Exception as e:
            print(f"Error en el loop MQTT: {e}")
            time.sleep(5)