import argparse
import cv2
from PIL import Image
import numpy as np

import zlib
import deflate

import struct

WIDTH = 128
HEIGHT = 64

DATA_DIR = "data/"

DITHER = False
BAYER_8X8 = np.array([
    [ 0,48,12,60, 3,51,15,63],
    [32,16,44,28,35,19,47,31],
    [ 8,56, 4,52,11,59, 7,55],
    [40,24,36,20,43,27,39,23],
    [ 2,50,14,62, 1,49,13,61],
    [34,18,46,30,33,17,45,29],
    [10,58, 6,54, 9,57, 5,53],
    [42,26,38,22,41,25,37,21]
], dtype=np.uint8)

def encode_video(filepath, dither):

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
        #bw_img = rgb_img.convert(,, dither=Image.Dither.ORDERED)

        if dither:
            rgb_img = rgb_img.convert("L")
            gray = np.array(rgb_img, dtype=np.uint8)

            h, w = gray.shape

            thresholds = np.tile(
                BAYER_8X8,
                (h // 4 + 1, w // 4 + 1)
            )[:h, :w]

            thresholds = thresholds * 4

            bw_data = (gray > thresholds).astype(np.uint8) * 255
        else:
            rgb_data = np.array(rgb_img)
            bw_data = rgb_data.mean(axis=2)>127

        #rgb_data = np.array(rgb_img)
        #bw_data = rgb_data.mean(axis=2)>127
        #bw_data = np.array(bw_img, dtype=np.uint8)
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
        deflate.zlib_decompress
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
    parser.add_argument("-W", "--width", type=int, default=120, help="Width of the video")
    parser.add_argument("-H", "--height", type=int, default=250, help="Height of the video")
    parser.add_argument("-d", "--dither", action="store_true", help="Enable dithering in video output (Will increase filesize)")

    args = parser.parse_args()
    filepath = args.file

    if args.dither:
        print("Applying Dither")

    encode_video(filepath, args.dither)

if __name__ == "__main__":
    main()