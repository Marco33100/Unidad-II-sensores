from umqtt.simple import MQTTClient
from machine import Pin
import network
import time

# Configuración WiFi
WIFI_SSID = "ANTONIOBM"
WIFI_PASSWORD = "12345678"

# Configuración MQTT
MQTT_BROKER = "192.168.137.167"
MQTT_USER = ""
MQTT_PASSWORD = ""
MQTT_CLIENT_ID = ""
MQTT_PORT = 1883
MQTT_TOPIC_PUB = "utng/040"

# Configuración del sensor KY-040
CLK = Pin(4, Pin.IN, Pin.PULL_UP)  # CLK (Clock)
DT = Pin(5, Pin.IN, Pin.PULL_UP)   # DT (Data)
SW = Pin(18, Pin.IN, Pin.PULL_UP)  # SW (Botón)

estado_anterior = CLK.value()

def conectar_wifi():
    print("Conectando a WiFi...", end="")
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(WIFI_SSID, WIFI_PASSWORD)

    start_time = time.time()
    while not sta_if.isconnected():
        if time.time() - start_time > 10:
            print("\nError al conectar a WiFi")
            return False
        print(".", end="")
        time.sleep(0.3)

    print("\nWiFi Conectada!")
    print("IP:", sta_if.ifconfig()[0])
    return True

def conectar_broker():
    client = MQTTClient(MQTT_CLIENT_ID, MQTT_BROKER, port=MQTT_PORT, user=MQTT_USER, password=MQTT_PASSWORD)
    client.connect()
    print(f"Conectado a MQTT Broker: {MQTT_BROKER}")
    return client

# Inicialización
if conectar_wifi():
    client = conectar_broker()

# Bucle principal de lectura del encoder
try:
    while True:
        clk_actual = CLK.value()
        dt_actual = DT.value()
        sw_actual = SW.value()

        if clk_actual != estado_anterior:
            if dt_actual != clk_actual:
                mensaje = "Giro horario"
            else:
                mensaje = "Giro antihorario"

            client.publish(MQTT_TOPIC_PUB, mensaje)
            print(f"Encoder: {mensaje}")

        if sw_actual == 0:  # Botón presionado
            client.publish(MQTT_TOPIC_PUB, "Botón presionado")
            print("Botón presionado")
            time.sleep(0.3)  # Pequeño retraso para evitar rebotes

        estado_anterior = clk_actual
        time.sleep(0.01)  # Pequeño delay para estabilidad

except Exception as e:
    print("Error:", e)
    client.disconnect()