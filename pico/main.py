import machine
import time

import epd
import struct
import deflate
import io

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
    with open("video.bin", "rb") as f:
        index = 0
        while True:
            size_bytes = f.read(4)
            if not size_bytes:
                break
        
            (size,) = struct.unpack("<I", size_bytes)

            comp = f.read(size)

            with deflate.DeflateIO(io.BytesIO(comp), deflate.ZLIB) as d:
                frame = bytearray(d.read())

                display.buffer_balck[:] = frame

                display.display()
                print("FRAME " + str(index))
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