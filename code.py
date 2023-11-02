import cv2
import dlib

tracker = dlib.correlation_tracker()
selection = None
tracking = False

start_x, start_y = -1, -1
end_x, end_y = -1, -1

def select_object(event, x, y, flags, param):
    global tracking, selection, start_x, start_y, end_x, end_y

    if event == cv2.EVENT_LBUTTONDOWN:
        start_x, start_y = x, y
        end_x, end_y = x, y
    elif event == cv2.EVENT_MOUSEMOVE:
        end_x, end_y = x, y
    elif event == cv2.EVENT_LBUTTONUP:
        x1 = min(start_x, end_x)
        y1 = min(start_y, end_y)
        x2 = max(start_x, end_x)
        y2 = max(start_y, end_y)
        selection = (x1, y1, x2 - x1, y2 - y1)
        if selection[2] > 0 and selection[3] > 0:
            tracking = True

# Open your webcam for video capture
cap = cv2.VideoCapture(f'test2.mp4')

cv2.namedWindow("Select Object")
cv2.setMouseCallback("Select Object", select_object)

while True:
    ret, frame = cap.read()

    if tracking and selection:
        x, y, w, h = selection
        if w > 0 and h > 0:
            if tracker.get_position().is_empty():
                img = frame[y:y+h, x:x+w]
                tracker.start_track(frame, dlib.rectangle(x, y, x + w, y + h))
            else:
                tracker.update(frame)
                new_position = tracker.get_position()
                selection = (int(new_position.left()), int(new_position.top()), int(new_position.width()), int(new_position.height()))
        print(x,y,w,h)

    win_img = frame.copy()
    if selection:
        x, y, w, h = selection
        cv2.rectangle(win_img, (x, y), (x + w, y + h), (0, 255, 0), 2)

    cv2.imshow("Select Object", win_img)

    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# Release the video capture and close windows
cap.release()
cv2.destroyAllWindows()
