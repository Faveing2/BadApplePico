import serial
import cv2
import time

connected = False
while not connected:
    try:
        ser = serial.Serial("/dev/cu.usbmodem1401", 115200)
        connected = True
    except serial.serialutil.SerialException:
        print("could not fine Pico, trying again")
        time.sleep(0.5)

cap = cv2.VideoCapture(0)

DISPLAY = True

def loop():
    while True:
        line = ser.readline().decode("utf-8", errors="replce")
        
        if "FRAME" in line:
            ret, frame = cap.read()
            frame_idx = line.split(" ")[1].rstrip()
            print("Recording frame "+frame_idx)

            cv2.imwrite("Frame "+ frame_idx+".png", frame)

            if DISPLAY:
                cv2.imshow("WEBCAM", frame)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break

if __name__ == "__main__":
    try:
        loop()
    except cv2.error as e:
        print(e)
        cap.release()
        exit()