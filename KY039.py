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
MQTT_TOPIC = "utng/039"  # Tópico para los datos del sensor de pulso
MQTT_PORT = 1883

# Configurar el sensor KY-039 en el GPIO34 (entrada analógica)
sensor_pulso = ADC(Pin(34))
sensor_pulso.atten(ADC.ATTN_11DB)  # Configurar el rango de voltaje de 0 a 3.3V

# Umbral de cambio para detectar variaciones significativas
UMBRAL_CAMBIO = 100  # Ajusta este valor según la sensibilidad que necesites

# Variable para almacenar el último valor enviado
ultimo_valor_enviado = None

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
        print(f"Conectado a MQTT Broker: {MQTT_BROKER}, Topic: {MQTT_TOPIC}")
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
            # Leer el valor analógico del sensor KY-039
            valor_actual = sensor_pulso.read()
            
            # Verificar si hay un cambio significativo respecto al último valor enviado
            if ultimo_valor_enviado is None or abs(valor_actual - ultimo_valor_enviado) >= UMBRAL_CAMBIO:
                # Mostrar el valor en el monitor serial
                print(f"Valor analógico del pulso: {valor_actual}")
                
                # Publicar el valor en el tópico MQTT
                client.publish(MQTT_TOPIC, str(valor_actual))
                
                # Actualizar el último valor enviado
                ultimo_valor_enviado = valor_actual
            
            time.sleep(0.1)  # Esperar 100 ms antes de tomar otra lectura
        except Exception as e:
            print(f"Error en el loop MQTT: {e}")
            time.sleep(5)