import network
from umqtt.simple import MQTTClient
import time
import machine

# 🔹 Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# 🔹 Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_CLIENT_ID = "ESP32_Buzzer"
MQTT_TOPIC = "utng/actuadorPasivoBuzzer"
MQTT_PORT = 1883

# 🔹 Configuración del buzzer KY-006
BUZZER_PIN = 14  # ⚠ Cambia este número según tu conexión
buzzer = machine.PWM(machine.Pin(BUZZER_PIN))

# Lista de frecuencias para generar tonos
TONOS = [262, 294, 330, 349, 392, 440, 494]  # Notas C, D, E, F, G, A, B (Do-Re-Mi)

# 🔹 Función para conectar a WiFi
def conectar_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
    while not sta_if.isconnected():
        time.sleep(0.1)
    print("WiFi Conectada!")
    print("IP:", sta_if.ifconfig()[0])

# 🔹 Función para conectar a MQTT
def conectar_mqtt():
    try:
        client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT)
        client.connect()
        print("Conectado a MQTT")
        return client
    except Exception as e:
        print("Error MQTT:", e)
        return None

# 🔹 Función para reproducir un tono
def reproducir_tono(frecuencia, duracion=0.5):
    buzzer.freq(frecuencia)  # Configura la frecuencia
    buzzer.duty(512)  # Activa el sonido (duty cycle 50%)
    time.sleep(duracion)
    buzzer.duty(0)  # Apaga el buzzer
    time.sleep(0.1)

# 🔹 Reproducir sonidos y enviar datos por MQTT
def reproducir_melodía(client):
    for tono in TONOS:
        mensaje = f"Tocando frecuencia: {tono} Hz"
        print(mensaje)
        client.publish(MQTT_TOPIC, mensaje)  # Enviar a MQTT
        reproducir_tono(tono, 0.3)  # Reproducir tono

# 🔹 Ejecutar
conectar_wifi()
client = conectar_mqtt()

if client:  # Solo continuar si la conexión MQTT fue exitosa
    while True:
        reproducir_melodía(client)  # Reproducir tonos secuenciales
        time.sleep(2)  # Esperar 2 segundos antes de repetir
