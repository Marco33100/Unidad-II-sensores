from machine import Pin
import time

# Definimos los pines para los 10 LEDs
led_pins = [2, 4, 5, 13, 14, 15, 16, 17, 18, 19]

# Configuramos cada pin como salida
leds = [Pin(pin, Pin.OUT) for pin in led_pins]

# Función para encender los LEDs de forma secuencial
def encender_secuencial():
    for led in leds:
        led.on()
        time.sleep(0.5)
        led.off()
        time.sleep(0.1)

# Función para encender y apagar todos los LEDs al mismo tiempo
def encender_todos():
    for led in leds:
        led.on()
    time.sleep(2)
    for led in leds:
        led.off()
    time.sleep(2)

# Función para hacer un efecto de "carrera" de LEDs
def efecto_carrera():
    for i in range(10):
        leds[i].on()
        time.sleep(0.2)
        leds[i].off()
    for i in range(8, -1, -1):
        leds[i].on()
        time.sleep(0.2)
        leds[i].off()

# Bucle principal
while True:
    encender_secuencial()
    encender_todos()
    efecto_carrera()