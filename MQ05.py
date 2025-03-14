from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_CLIENT_ID = "mq05_client"
MQTT_TOPIC = "utng/mq5"
MQTT_PORT = 1883

# Configuración del MQ-05 (Sensor de Gas)
pin_mq05 = ADC(Pin(34))  # Conectar el MQ-05 al GPIO34 (entrada analógica)
pin_mq05.atten(ADC.ATTN_11DB)  # Configurar el rango de lectura (0-3.3V)

# Variables para almacenar el último valor y umbral de cambio
ultimo_valor = None
umbral_cambio = 100  # Umbral para considerar un cambio significativo

# Función para conectar a WiFi
def conectar_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    
    for _ in range(30):  # Esperar 9 segundos máximo
        if sta_if.isconnected():
            print("✅ WiFi conectada!")
            return
        time.sleep(0.3)
    
    print("⚠ Error: No se pudo conectar a WiFi")
    raise Exception("No se pudo conectar a WiFi")

# Función para conectar al broker MQTT
def conectar_broker():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.connect()
        print(f"✅ Conectado a MQTT Broker: {MQTT_BROKER}, Topic: {MQTT_TOPIC}")
        return client
    except Exception as e:
        print(f"⚠ Error al conectar con MQTT: {e}")
        return None

# Función para leer el valor del MQ-05
def leer_valor():
    return pin_mq05.read()  # Leer el valor analógico (0-4095)

# Conectar a WiFi
conectar_wifi()

# Conectar al broker MQTT
client = conectar_broker()

# Bucle principal
while True:
    try:
        valor_actual = leer_valor()  # Obtener el valor actual
        
        # Solo enviar un mensaje si hay un cambio significativo
        if ultimo_valor is None or abs(valor_actual - ultimo_valor) >= umbral_cambio:
            print(f"Valor MQ-05: {valor_actual}")
            
            if client:  # Si hay conexión MQTT
                try:
                    client.publish(MQTT_TOPIC, str(valor_actual))  # Enviar valor al broker MQTT
                    print(f"✅ Mensaje enviado a MQTT: {valor_actual}")
                except Exception as e:
                    print(f"⚠ Error al enviar MQTT: {e}")
                    client = conectar_broker()  # Intentar reconectar
            
            ultimo_valor = valor_actual  # Actualizar el último valor
        
        time.sleep(0.1)  # Esperar 0.1 segundos entre lecturas
        
    except Exception as e:
        print(f"⚠ Error en bucle principal: {e}")
        time.sleep(3)