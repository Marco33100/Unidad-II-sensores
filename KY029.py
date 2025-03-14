from machine import Pin
import time
import network
from umqtt.simple import MQTTClient

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_CLIENT_ID = "led_2colores_client"
MQTT_TOPIC = "utng/2colores"
MQTT_PORT = 1883

# Configuración del LED de 2 colores
pin_rojo = Pin(4, Pin.OUT)  # Conectar el ánodo del color rojo al GPIO4
pin_verde = Pin(5, Pin.OUT)  # Conectar el ánodo del color verde al GPIO5

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

# Función para cambiar el color del LED
def cambiar_color(color):
    if color == "rojo":
        pin_rojo.value(1)  # Encender el color rojo
        pin_verde.value(0)  # Apagar el color verde
    elif color == "verde":
        pin_rojo.value(0)  # Apagar el color rojo
        pin_verde.value(1)  # Encender el color verde
    else:
        pin_rojo.value(0)  # Apagar ambos colores
        pin_verde.value(0)

# Conectar a WiFi
conectar_wifi()

# Conectar al broker MQTT
client = conectar_broker()

# Bucle principal
while True:
    try:
        # Simular un cambio de estado (alternar entre rojo y verde)
        if ultimo_estado == "rojo":
            nuevo_estado = "verde"
        else:
            nuevo_estado = "rojo"
        
        # Cambiar el color del LED
        cambiar_color(nuevo_estado)
        print(f"Color LED: {nuevo_estado}")
        
        if client:  # Si hay conexión MQTT
            try:
                client.publish(MQTT_TOPIC, nuevo_estado)  # Enviar estado al broker MQTT
                print(f"✅ Mensaje enviado a MQTT: {nuevo_estado}")
            except Exception as e:
                print(f"⚠ Error al enviar MQTT: {e}")
                client = conectar_broker()  # Intentar reconectar
        
        ultimo_estado = nuevo_estado  # Actualizar el último estado
        
        time.sleep(5)  # Esperar 5 segundos antes de cambiar de color
        
    except Exception as e:
        print(f"⚠ Error en bucle principal: {e}")
        time.sleep(3)