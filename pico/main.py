import machine
import time

import epd

import deflate

TOTAL=3999

display = epd.EPD_2in13_B_V4_Landscape()

def display_frame(display, frame_idx):
    frame = None
    with open("data/"+str(frame_idx)+".bin", "rb") as f:
        with deflate.DeflateIO(f, deflate.ZLIB) as d:
            #frame = bytearray(deflate.gzip_decompress(f.read()))
            frame = bytearray(d.read())

    display.buffer_balck[:] = frame

    display.display()

def loop():
    index = 0
    while index <= TOTAL:
        display_frame(display, index)
        index += 1

while True:
    loop()

# # Standard Pico vs. Pico W pin assignments
# # Standard Pico pin is 'LED'
# # Pico W uses 'WL_GPIO' or 'LED' depending on the firmware version
# led = machine.Pin('LED', machine.Pin.OUT)

# while True:
#     led.toggle()
#     time.sleep(1) # Blinks every 1 second