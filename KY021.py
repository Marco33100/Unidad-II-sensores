from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_CLIENT_ID = "reed_switch_client"
MQTT_TOPIC = "utng/miniInterruptor"
MQTT_PORT = 1883

# Configuración del Reed Switch
pin_reed = Pin(4, Pin.IN, Pin.PULL_UP)  # Conectar el Reed Switch al GPIO4

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

# Función para leer el estado del Reed Switch
def leer_estado():
    return pin_reed.value()  # Leer el valor del pin (0 o 1)

# Conectar a WiFi
conectar_wifi()

# Conectar al broker MQTT
client = conectar_broker()

# Bucle principal
while True:
    try:
        estado_actual = leer_estado()  # Obtener el estado actual
        
        # Solo enviar un mensaje si el estado ha cambiado
        if estado_actual != ultimo_estado:
            estado_texto = "Activado" if estado_actual == 0 else "Desactivado"
            print(f"Reed Switch: {estado_texto}")
            
            if client:  # Si hay conexión MQTT
                try:
                    client.publish(MQTT_TOPIC, estado_texto)  # Enviar estado al broker MQTT
                    print(f"✅ Mensaje enviado a MQTT: {estado_texto}")
                except Exception as e:
                    print(f"⚠ Error al enviar MQTT: {e}")
                    client = conectar_broker()  # Intentar reconectar
            
            ultimo_estado = estado_actual  # Actualizar el último estado
        
        time.sleep(0.1)  # Esperar 0.1 segundos entre lecturas
        
    except Exception as e:
        print(f"⚠ Error en bucle principal: {e}")
        time.sleep(3)