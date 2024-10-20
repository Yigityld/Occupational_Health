import cv2
import time
from ultralytics import YOLO
from gtts import gTTS
import pygame
from playsound import playsound
import os

model = YOLO("helmet.pt")
font = cv2.FONT_HERSHEY_COMPLEX
kamera = cv2.VideoCapture(0)

m = 0
i = 0

start = 0
end = time.time()

yelek_yok_time = None
baret_yok_time = None

while True:
    ret, frame = kamera.read()
    if not ret:
        break

    results = model(frame)
    labels = results[0].names

    yelek_yok_goruldu = False
    baret_yok_goruldu = False

    current_time = time.time()

    for i in range(len(results[0].boxes)):
        x1, y1, x2, y2 = results[0].boxes.xyxy[i]
        cls = results[0].boxes.cls[i]
        score = results[0].boxes.conf[i]
        try:
            ids = results[0].boxes.id[i]
        except TypeError:
            ids = 0
        x1, y1, x2, y2, cls, ids, score = int(x1), int(y1), int(x2), int(y2), int(cls), int(ids), float(score)
        name = labels[cls]

        if cls == 4 and score >= 0.4:
            yelek_yok_goruldu = True
        if cls == 2 and score >= 0.4:
            baret_yok_goruldu = True
        if score < 0.4:
            continue

        labels[4] = "Yelek Yok"
        labels[7] = "Yelek"
        labels[2] = "Baret Yok"
        labels[0] = "Baret"

        if cls == 0 or cls == 7:
            color = (255, 255, 255) if cls == 0 else (255, 0, 0)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            label = f"{name} {score:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

        elif cls == 2 or cls == 4:
            color = (0, 0, 0) if cls == 2 else (0, 0, 255)
            cv2.rectangle(frame, (x1, y1), (x2, y2), color, 2)
            label = f"{name} {score:.2f}"
            cv2.putText(frame, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)

    if baret_yok_goruldu:
        if baret_yok_time is None:
            baret_yok_time = current_time

        elif current_time - baret_yok_time >= 4:
            tts = gTTS(text="Bu alanda baret takılmadan çalışma yapılmaktadır.", lang="tr", slow=False)

            temp_file = str(f"temp{i}.mp3")
            i += 1
            tts.save(temp_file)
            pygame.mixer.init()
            pygame.mixer.music.load("alarm.mp3")
            pygame.mixer.music.play()
            time.sleep(2)
            pygame.mixer.music.stop()
            playsound(temp_file)

            baret_yok_time = None
            baret_yok_goruldu = False
            os.remove(temp_file)

    else:
        baret_yok_time = None

    if yelek_yok_goruldu:
        print("yelek", yelek_yok_goruldu)
        if yelek_yok_time is None:
            yelek_yok_time = current_time
        elif current_time - yelek_yok_time >= 4:
            tts = gTTS(text="Bu alanda yelek giyilmeden çalışma yapılmaktadır.", lang="tr")

            temp_file = str(f"temps{m}.mp3")
            m += 1
            tts.save(temp_file)
            pygame.mixer.init()
            pygame.mixer.music.load("alarm.mp3")
            pygame.mixer.music.play()
            time.sleep(2)
            pygame.mixer.music.stop()
            playsound(temp_file)

            yelek_yok_time = None
            yelek_yok_goruldu = False
            os.remove(temp_file)

    else:
        yelek_yok_time = None

    end = time.time()
    fps = 1 / (end - start)
    start = end
    cv2.putText(frame, f"FPS sayisi: {fps:.2f}", (10, 60), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow("Kask ve Yelek Tespiti", frame)

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

kamera.release()
cv2.destroyAllWindows()
