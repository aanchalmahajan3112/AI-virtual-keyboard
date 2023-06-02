import cv2
from cvzone.HandTrackingModule import HandDetector           # used for hand detection and tracking
from time import sleep
from pynput.keyboard import Controller                       # used for emulating keyboard input


cap=cv2.VideoCapture(0)             # initializes a video capture object for the default camera
cap.set(3,1280)                      # sets the width of the capture window to 1280 pixels
cap.set(4,720)                       # sets the height to 720 pixels

detector=HandDetector(detectionCon=0.8)      #An instance of the HandDetector class is created with a detection confidence threshold of 0.8

keys = [["Q", "W", "E", "R", "T", "Y", "U", "I", "O", "P"],
        ["A", "S", "D", "F", "G", "H", "J", "K", "L", ";"],
        ["Z", "X", "C", "V", "B", "N", "M", ",", ".", "/"]]

ClickedText=""
keyboard=Controller()
def drawAll(img,buttonList):

    for button in buttonList:
        x, y = button.pos
        w, h = button.size
        cv2.rectangle(img, button.pos, (x + w, y + h), (0, 0, 0), cv2.FILLED)     # setting rectangle in order to make a key
        cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),5)  # text to b inserted in rectangle
    return img


class Button():
    def __init__(self,pos,text,size=[80,80]):
        self.pos=pos
        self.text=text
        self.size=size


buttonList=[]
for i in range(len(keys)):                           # iterates over each row of keys in the virtual keyboard
    for j, key in enumerate(keys[i]):                # iterates over the elements of the current row  j-index, key- value of element
        buttonList.append(Button([100 * j + 50, 100 * i + 50], key))          #appending keys in buttonList

while True:
    success,img=cap.read()                       #method reads a frame from the video capture object
    img = detector.findHands(img)                # processes the frame to detect hands and draw landmarks and bounding boxes around them
    lmlist,bboxInfo =detector.findPosition(img)    #extracts landmarks positions & returns them in lmlist along with additional information in bboxInfo.

    drawAll(img,buttonList)                        #draw all the buttons from the buttonList on the img frame

    if lmlist:
        for button in buttonList:
            x,y= button.pos
            w,h=button.size
            if x< lmlist[8][0]<x+w and y<lmlist[8][1] < y+h:     #pos of tip of index finger(lmlist[8]) is within boundaries of button's position & size
                cv2.rectangle(img, button.pos, (x + w, y + h), (255, 0, 0),cv2.FILLED)  # converts key to blue where finger is hovered
                cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),5)
                l,_,_ =detector.findDistance(8,12,img)         #detects the distance between index & middle finger

                if l<50:
                    keyboard.press(button.text)                 #checks for which button is pressed
                    cv2.rectangle(img, button.pos, (x + w, y + h), (0, 255, 0),cv2.FILLED)  # converts d pressed key to green where distance is small
                    cv2.putText(img, button.text, (x + 20, y + 65), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),5)
                    ClickedText+=button.text
                    sleep(0.2)                                    #to avoid multiple clicks


    cv2.rectangle(img, (55,345),(700,450), (255, 0, 0), cv2.FILLED)  # blank space where pressed keys are typed
    cv2.putText(img, ClickedText, (60,425), cv2.FONT_HERSHEY_SIMPLEX, 2, (255, 255, 255),5)  # provides keys which are clicked

    cv2.imshow('camera',img)                                                    #resulting image is displayed in a window named 'camera'
    cv2.waitKey(1)