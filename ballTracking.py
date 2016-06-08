import cv2
import numpy as np
import time

def onMouse(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        value = 'H('+str(hsv[y,x][0])+') S('+str(hsv[y,x][1])+') V('+str(hsv[y,x][2])+')'
        print(value)

cap = cv2.VideoCapture(1)
width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
videoFrame = cv2.VideoWriter('frame.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 25, (int(width),int(height)), True)
videoRes = cv2.VideoWriter('res.avi', cv2.VideoWriter_fourcc('M','J','P','G'), 25, (int(width),int(height)), True)

lowerYellow = np.array([14,110,150])
upperYellow = np.array([35,255,255])

points = []
pointsSub = []
mode = False
cv2.namedWindow('frame')
cv2.setMouseCallback('frame', onMouse)
while True:
    res, frame = cap.read()
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, lowerYellow, upperYellow)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    im, contours, hierarchy = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for p in points:
        for i in range(1, len(p)):
            cv2.line(frame, p[i-1], p[i], (127,0,255), 2)
    for c in contours:
        (x, y), radius = cv2.minEnclosingCircle(c)
        if radius > 30:
            cv2.circle(frame, (int(x), int(y)), int(radius), (153,153,0),2)
            cv2.circle(frame, (int(x), int(y)), 2, (127,0,255),2)
            if mode:
                pointsSub.append((int(x),int(y)))
                for i in range(1, len(pointsSub)):
                    cv2.line(frame, pointsSub[i-1], pointsSub[i], (127,0,255), 2)
    cv2.imshow('frame', frame)
    cv2.imshow('res', res)
    key = cv2.waitKey(5) & 0xff
    videoFrame.write(frame)
    videoRes.write(res)
    if key == ord(' '):
        break
    elif key == ord('s'):
        cv2.imwrite('screenshot.jpg', frame)
    elif key == ord('x'):
        if mode:
            points.append(pointsSub)
            pointsSub = []
        mode = not mode
    elif key == ord('c'):
        points.clear()

cap.release()
cv2.destroyAllWindows()
