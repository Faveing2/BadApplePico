import argparse
import cv2
from PIL import Image
import numpy as np

import matplotlib.pyplot as plt
#import heatshrink2
import zlib
import deflate

import struct

WIDTH = 122
HEIGHT = 250

DATA_DIR = "data/"

def encode_video(filepath):

    cap = cv2.VideoCapture(filepath)

    frames = []

    if not cap.isOpened():

        print("Error: Could not open video")
        exit()

    frame_idx = 0

    while cap.isOpened():
        print(frame_idx)
        # if frame_idx == 4000:
        #     break

        ### Read in the video frame
        ret, frame = cap.read()

        if (frame_idx%2)==1:
            ret, frame =cap.read()

        if not ret:
            break

        height = None
        width = None

        if WIDTH % 8 == 0:
            width = WIDTH
        else :
            width = (WIDTH // 8) * 8 + 8
        height = HEIGHT

        ### Create a bytearray for that frame
        buffer = bytearray(height*width // 8)

        #bw = frame.mean(axis=2) > 127
        try:
            rgb_img = Image.fromarray(frame)
        except AttributeError:
            frame_idx += 1
            break  
        rgb_img = rgb_img.resize((height, width), Image.Resampling.LANCZOS)

        rgb_data = np.array(rgb_img)
        bw_data = rgb_data.mean(axis=2)>127
        #bw_data = np.rot90(bw_data, -1)

        #bw_data[100, :] = 1

        #print(str(bw_data.shape))
        # if frame_idx == 240:
        #     plt.imshow(bw_data)
        #     plt.show()

        ### Pack data into buffer
        #print(bw_data.shape)
        for x in range(HEIGHT):
            for y in range(WIDTH):
                if bw_data[y, x]:
                    index = x + (y // 8) * HEIGHT
                    #index = y * (width // 8) + (x // 8)
                    try:
                        buffer[index] |= 1 << (y & 7)
                        #buffer[index] |= 0x80 >> (x & 7)
                    except IndexError:
                        print("Error: IndexError")
                        print("Frame:" + str(frame_idx))
                        print("Array Index:", index)
                        pass

        ### Save buffer to a file

        # with open(DATA_DIR+str(frame_idx)+".bin", "wb") as file:
        #     file.write(deflate.zlib_compress(buffer))

        frames.append(buffer)

        frame_idx += 1

        # if frame_idx==100:
        #     break

    with open("pico/video.bin", "wb") as f:
        for frame in frames:
            comp = deflate.zlib_compress(frame)
            f.write(struct.pack("<I", len(comp)))
            f.write(comp)

    cap.release

def main():
    parser = argparse.ArgumentParser(description="Script to encode a video to be played on the Pico")
    
    parser.add_argument("file", help="Filepath to video")

    args = parser.parse_args()
    filepath = args.file

    encode_video(filepath)

if __name__ == "__main__":
    main()