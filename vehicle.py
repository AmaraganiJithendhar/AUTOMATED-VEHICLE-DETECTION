import cv2
import numpy as np

# Path to the video file
video_path = 'video.mp4'

# Create VideoCapture object
cap = cv2.VideoCapture(video_path)

# Check if the video file can be opened
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

# Parameters
min_width_react = 80
min_height_react = 80
count_line_position = 550

# Background subtractor
algo = cv2.createBackgroundSubtractorMOG2()

def center_handle(x, y, w, h):
    x1 = int(w / 2)
    y1 = int(h / 2)
    cx = x + x1
    cy = y + y1
    return cx, cy

detect = []
offset = 6
counter = 0

while True:
    ret, frame1 = cap.read()

    # Check if the frame was read correctly
    if not ret:
        print("Error: Could not read frame or end of video reached.")
        break

    grey = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(grey, (3, 3), 5)
    img_sub = algo.apply(blur)
    dilat = cv2.dilate(img_sub, np.ones((5, 5), np.uint8))

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
    dilatada = cv2.morphologyEx(dilat, cv2.MORPH_CLOSE, kernel)
    dilatada = cv2.morphologyEx(dilatada, cv2.MORPH_CLOSE, kernel)

    # Correctly unpack the contours and hierarchy
    contours, _ = cv2.findContours(dilatada, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Draw the line on the frame
    cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (255, 127, 0), 3)

    for contour in contours:
        (x, y, w, h) = cv2.boundingRect(contour)
        validate_counter = (w >= min_width_react) and (h >= min_height_react)
        if not validate_counter:
            continue
        cv2.rectangle(frame1, (x, y), (x + w, y + h), (0, 255, 0), 2)
        center = center_handle(x, y, w, h)
        detect.append(center)
        cv2.circle(frame1, center, 4, (0, 0, 255), -1)
        for (cx, cy) in detect:
            if cy < (count_line_position + offset) and cy > (count_line_position - offset):
                counter += 1
                cv2.line(frame1, (25, count_line_position), (1200, count_line_position), (0, 127, 255), 3)
                detect.remove((cx, cy))
                print("Vehicle Counter:" + str(counter))
        
    # Display the vehicle counter on the frame
    cv2.putText(frame1, "VEHICLE COUNTER: " + str(counter), (450, 70), cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 0, 255), 5)

    cv2.imshow('Video Original', frame1)

    if cv2.waitKey(1) == 13:  # 13 is the Enter key
        break

cap.release()
cv2.destroyAllWindows()


