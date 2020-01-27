import cv2
import numpy

def nothing(x):
    pass

def createWindow():
    cv2.namedWindow('image')
    cv2.createTrackbar('Upper Hue','image',0,180,nothing)
    cv2.setTrackbarPos('Upper Hue','image',79)
    cv2.createTrackbar('Upper Sat','image',0,255,nothing)
    cv2.setTrackbarPos('Upper Sat','image',255)
    cv2.createTrackbar('Upper Val','image',0,255,nothing)
    cv2.setTrackbarPos('Upper Val','image',255)

    cv2.createTrackbar('Lower Hue','image',0,180,nothing)
    cv2.setTrackbarPos('Lower Hue','image',64)
    cv2.createTrackbar('Lower Sat','image',0,255,nothing)
    cv2.setTrackbarPos('Lower Sat','image',90)
    cv2.createTrackbar('Lower Val','image',0,255,nothing)
    cv2.setTrackbarPos('Lower Val','image',69)

def customThresh(hsv_frame):
    kernel = numpy.ones((1,1),numpy.uint8)
    upper_hsv = numpy.array([cv2.getTrackbarPos('Upper Hue','image'),cv2.getTrackbarPos('Upper Sat','image'),cv2.getTrackbarPos('Upper Val',
        'image')])
    lower_hsv = numpy.array([cv2.getTrackbarPos('Lower Hue','image'),cv2.getTrackbarPos('Lower Sat','image'),cv2.getTrackbarPos('Lower Val', 'image')])
    hsv_thresh =  cv2.inRange(hsv_frame,lower_hsv,upper_hsv)
    blur = cv2.GaussianBlur(hsv_thresh,(5,5),0)
    return cv2.dilate(blur,kernel,iterations=1)


def findContours(frame):
    _,thresh = cv2.threshold(frame,127,255,cv2.THRESH_BINARY)
    contours,hierarchy = cv2.findContours(thresh,1,2)
    cnt = contours[0]
    M = cv2.moments(cnt)
    return thresh, cnt, M 

def main():
    frame = cv2.imread('assets/BlueGoal-Far-ProtectedZone.jpg')
    #show orginal frame
    cv2.imshow('frame',frame)
    hsv = cv2.cvtColor(frame,cv2.COLOR_BGR2HSV)
    createWindow()
    while(True):
        hsv_thresh = customThresh(hsv)
        thresh,cnt, M = findContours(hsv_thresh)
        #create bounding rect
        x,y,w,h = cv2.boundingRect(cnt)
        rect = cv2.minAreaRect(cnt)
        box = cv2.boxPoints(rect)
        box = numpy.int0(box)
        frame = cv2.drawContours(frame,[box],0,(0,255,255),2)
        frame = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)
        frame = cv2.circle(frame,(int(x+w/2),int(y+h/2)),2,(0,255,0),1)


        #show images
        cv2.imshow('image',hsv_thresh)
        cv2.imshow('threshold',frame)
        print(x)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    cv2.destroyAllWindows()



if __name__ == '__main__':
    main()