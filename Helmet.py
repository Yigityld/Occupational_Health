import cv2
from ultralytics import YOLO


model = YOLO("helmet.pt")
font = cv2.FONT_HERSHEY_COMPLEX
cam = cv2.VideoCapture(0)


while True:
    ret, frame = cam.read()
    if not ret:
        break

    results = model(frame)
    labels = results[0].names

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

        if score < 0.45:
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

    cv2.imshow("Kask ve Yelek Tespiti", frame)

    if cv2.waitKey(50) & 0xFF == ord("q"):
        break

kamera.release()
cv2.destroyAllWindows()
