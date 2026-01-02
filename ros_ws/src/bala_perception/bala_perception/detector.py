import cv2 as cv
import numpy as np



def detect_green(frame : np.ndarray) -> tuple[int, int] | None:

    blank = np.zeros(frame.shape[:2], dtype='uint8')

    framehsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)

    kernel = np.ones((5,5), dtype='uint8')


    greenlow1 = np.array([25, 100, 40])
    greenhigh1 = np.array([50, 255, 255])

    maska = cv.inRange(framehsv, greenlow1, greenhigh1)
    maska = cv.morphologyEx(maska, cv.MORPH_OPEN, kernel)

    maskaiframe = cv.bitwise_and(frame, frame, mask=maska)

    krawedzie,_ = cv.findContours(maska, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)




    maks = 0
    x, y, w, h = (0,0,0,0)
    for konturki in krawedzie:
        pole = cv.contourArea(konturki)

        if pole > maks:
            maks = pole

            if pole > 200:
                x, y, w, h = cv.boundingRect(konturki)    
    

    if (x,y,w,h) != (0,0,0,0):
        return (x + w//2, y + h//2)



    else:
        return None