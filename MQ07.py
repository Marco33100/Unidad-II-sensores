from machine import Pin, ADC
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_CLIENT_ID = "mq7_client"
MQTT_TOPIC = "utng/mq7"
MQTT_PORT = 1883

# Configuración del MQ-7 (Sensor de Monóxido de Carbono)
pin_mq7 = ADC(Pin(34))  # Conectar el MQ-7 al GPIO34 (entrada analógica)
pin_mq7.atten(ADC.ATTN_11DB)  # Configurar el rango de lectura (0-3.3V)

# Umbral para detectar humo (ajusta según sea necesario)
UMBRAL_HUMO = 1500  # Si el valor es menor que este umbral, se detecta humo

# Variable para almacenar el último estado
ultimo_estado = None

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

# Función para leer el valor del MQ-7
def leer_valor():
    return pin_mq7.read()  # Leer el valor analógico (0-4095)

# Conectar a WiFi
conectar_wifi()

# Conectar al broker MQTT
client = conectar_broker()

# Bucle principal
while True:
    try:
        valor_actual = leer_valor()  # Obtener el valor actual
        
        # Determinar si se detectó humo (valor menor que el umbral)
        if valor_actual < UMBRAL_HUMO:
            estado_actual = "Humo detectado"
        else:
            estado_actual = "No se detectó humo"
        
        # Solo enviar un mensaje si el estado ha cambiado
        if estado_actual != ultimo_estado:
            print(f"Estado: {estado_actual}, Valor: {valor_actual}")
            
            if client:  # Si hay conexión MQTT
                try:
                    client.publish(MQTT_TOPIC, estado_actual)  # Enviar estado al broker MQTT
                    print(f"✅ Mensaje enviado a MQTT: {estado_actual}")
                except Exception as e:
                    print(f"⚠ Error al enviar MQTT: {e}")
                    client = conectar_broker()  # Intentar reconectar
            
            ultimo_estado = estado_actual  # Actualizar el último estado
        
        time.sleep(0.1)  # Esperar 0.1 segundos entre lecturas
        
    except Exception as e:
        print(f"⚠ Error en bucle principal: {e}")
        time.sleep(3)