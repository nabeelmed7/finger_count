import cv2
import time
import hand_tracking_module as hndm
import os

path = 'fingers'
path_list = os.listdir(path)
images_list = []
for image_path in path_list:
    image = cv2.imread(f'{path}/{image_path}')
    images_list.append(image)

cap = cv2.VideoCapture(0)
time_previous = 0
detector = hndm.hand_tracking(confidence_detection = 0.80, confidence_tracking = 0.80)
tipIds = [4, 8, 12, 16, 20]
while True:
    ret, frame = cap.read()
    frame = detector.hands_tracking(frame)
    llist = detector.position_find(frame, draw = False)
    h, w, c = frame.shape
    c_x = int(w / 2)
    c_y = int(h / 2)
    
    fingers = []
    if len(llist) != 0:
        
        # for thumb
        if llist[tipIds[0]][1] < llist[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # llist[8][2] < llist[6][2] means if the y co-ordinate of 8th element(top portion ofindex finger) is higher than the y co=ordinate of 6th element(middle portion of index finger) it means it's open. In open cv0 is highest hence higher is <
        for id in range(1, 5):
            if llist[tipIds[id]][2] < llist[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        f_count = str(fingers.count(1))
        cv2.putText(frame, f_count, (c_x, c_y), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    time_current = time.time()
    fps = 1 / (time_current - time_previous)
    time_previous = time_current
    fps_text = "FPS: {:.1f}".format(fps)
    cv2.putText(frame, fps_text, (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    tracking_text = "Finger counter"
    cv2.putText(frame, tracking_text, (10, 80), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
    
    cv2.imshow('Webcam', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()