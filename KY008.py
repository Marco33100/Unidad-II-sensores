import network
from umqtt.simple import MQTTClient
from machine import Pin
import time

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/actuadorLaser"  # Aún puedes usar este tema, aunque ya no sea un sensor de temperatura
MQTT_PORT = 1883

# Configurar el LED láser en el pin 2 (GPIO 2)
pin_led = Pin(2, Pin.OUT)

# Función para conectar a WiFi
def conectar_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    
    for _ in range(30):  # Esperar 9 segundos máximo
        if sta_if.isconnected():
            print("✅ WiFi conectada!")
            return
        time.sleep(0.3)
    
    print("⚠ Error: No se pudo conectar a WiFi")

# Función para conectar al broker MQTT
def conectar_broker():
    global client
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.connect()
        print(f"✅ Conectado a MQTT Broker: {MQTT_BROKER}, Topic: {MQTT_TOPIC}")
    except Exception as e:
        print(f"⚠ Error al conectar con MQTT: {e}")
        client = None

# Conectar a WiFi y MQTT
conectar_wifi()
conectar_broker()

# Bucle principal: Encender y apagar el LED láser
while True:
    try:
        # Encender el LED láser
        pin_led.value(1)
        print("🔴 LED láser encendido")

        if client:  # Si hay conexión MQTT
            try:
                client.publish(MQTT_TOPIC, "LED Encendido")
            except Exception as e:
                print(f"⚠ Error al enviar MQTT: {e}")
                conectar_broker()  # Reconectar
        
        time.sleep(2)  # Esperar 2 segundos con el LED encendido
        
        # Apagar el LED láser
        pin_led.value(0)
        print("⚫ LED láser apagado")
        
        if client:  # Si hay conexión MQTT
            try:
                client.publish(MQTT_TOPIC, "LED Apagado")
            except Exception as e:
                print(f"⚠ Error al enviar MQTT: {e}")
                conectar_broker()  # Reconectar
        
        time.sleep(2)  # Esperar 2 segundos con el LED apagado
        
    except Exception as e:
        print(f"⚠ Error en bucle principal: {e}")
        time.sleep(3)