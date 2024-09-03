import cv2

cap = cv2.VideoCapture(0)  
ret, frame1 = cap.read()
ret, frame2 = cap.read()

status_sebelumnya = "Bergerak"  # Menginisialisasi status_sebelumnya ke "Bergerak"

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    diff = cv2.absdiff(frame1, frame)
    gray = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    _, thresh = cv2.threshold(blur, 20, 255, cv2.THRESH_BINARY)
    dilated = cv2.dilate(thresh, None, iterations=3)
    contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    object_moving = False

    for contour in contours:
        if cv2.contourArea(contour) < 700:
            continue
        object_moving = True
        (x, y, w, h) = cv2.boundingRect(contour)
        cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
        break

    status = "Bergerak" if object_moving else "Diam"

    if status != status_sebelumnya:  # Memeriksa apakah status berubah
        cv2.putText(frame, "Keterangan : {}".format(status), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3) 

    cv2.imshow("feed", frame)

    status_sebelumnya = status  # Menyimpan status saat ini sebagai status_sebelumnya untuk iterasi selanjutnya

    frame1 = frame2
    ret, frame2 = cap.read()

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
