import network
from umqtt.simple import MQTTClient
from machine import Pin
import time
import onewire
import ds18x20

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_CLIENT_ID = ""
MQTT_TOPIC = "utng/sensorTemperatura"
MQTT_PORT = 1883

# Configurar el sensor KY-001 (Temperatura DS18B20)
pin_temp = Pin(4)  # GPIO4 para datos del sensor
ow = onewire.OneWire(pin_temp)
ds = ds18x20.DS18X20(ow)
roms = ds.scan()

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

# Verificar sensor
if not roms:
    print("⚠ Error: Sensor DS18B20 no detectado")
else:
    print(f"✅ Sensor DS18B20 detectado: {roms[0]}")

# Bucle principal: Leer temperatura y enviar MQTT
while True:
    try:
        ds.convert_temp()  # Iniciar conversión de temperatura
        time.sleep_ms(750)  # Esperar conversión (750ms mínimo)
        temperatura = ds.read_temp(roms[0])  # Leer temperatura
        
        print(f"🌡 Temperatura: {temperatura:.2f}°C")
        
        if client:  # Si hay conexión MQTT
            try:
                client.publish(MQTT_TOPIC, str(temperatura))
            except Exception as e:
                print(f"⚠ Error al enviar MQTT: {e}")
                conectar_broker()  # Reconectar
        
        time.sleep(5)  # Esperar 5 segundos entre lecturas
        
    except Exception as e:
        print(f"⚠ Error en bucle principal: {e}")
        time.sleep(3)