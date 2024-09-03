import cv2

def main():
    cap = cv2.VideoCapture(0) 

    ret, frame1 = cap.read()
    ret, frame2 = cap.read()

    while cap.isOpened():
        if frame1 is None or frame2 is None:
            break

        # Konversi frame menjadi grayscale
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)


        diff = cv2.absdiff(gray1, gray2)
        _, thresh = cv2.threshold(diff, 20, 255, cv2.THRESH_BINARY)
        dilated = cv2.dilate(thresh, None, iterations=3)
        contours, _ = cv2.findContours(dilated, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        object_moving = False

        for contour in contours:
            if cv2.contourArea(contour) < 700:
                continue
            object_moving = True
            break

        if object_moving:
            cv2.putText(frame1, "Keterangan : {}".format('Bergerak'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 3)
        else:
            cv2.putText(frame1, "Keterangan : {}".format('Diam'), (10, 20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 3) 

        cv2.imshow("feed", frame1)
        frame1 = frame2
        ret, frame2 = cap.read()

        if cv2.waitKey(1) & 0xFF == ord('q'): 
            break

    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
