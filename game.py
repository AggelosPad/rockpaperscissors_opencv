import cv2
import time
import random
import handtrack as htm


def game(move):
    possible_actions = ["rock", "paper", "scissors"]
    computer_action = random.choice(possible_actions)

    if move == 'rock' and computer_action == 'paper':
        result = 'Lost'
    if move =='scissors' and computer_action == 'rock':
       result = 'Lost'
    if move =='paper' and computer_action == 'scissors':
        result = 'Lost'
    if move == computer_action:
        result = 'Drawed'
    else:
        result = 'Won'        
    return result,computer_action




pTime = 0
cTime = 0


cap = cv2.VideoCapture(0)



detector = htm.handDetector(detectionCon=0.75)

while True:
    success, img = cap.read()
    img = detector.findHands(img)
    lmList = detector.findPosition(img,draw = False)
    
    tipIds = [4, 8, 12, 16, 20] #mediapipe graph
    
    if len(lmList) != 0:
        
        fingers = []
        move = 'None'

        # Thumb
        if lmList[tipIds[0]][1] > lmList[tipIds[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)
        # 4 Fingers
        for id in range(1, 5):
            if lmList[tipIds[id]][2] < lmList[tipIds[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)
        
        totalFingers = fingers.count(1)

        if totalFingers == 5:
            move = 'paper'
        if totalFingers == 2 and fingers[1] == 1 and fingers[2] == 1:
            move = 'scissors'
        if totalFingers == 0:
            move = 'rock'    


        if move != 'None' :
            result,computer_move = game(move)
            cv2.putText(img,"Your move: " + str(move), (50, 200), cv2.FONT_HERSHEY_PLAIN, 1.5,(0,0, 255), 2)
            cv2.putText(img,"Computer's move: " + str(computer_move), (50, 250), cv2.FONT_HERSHEY_PLAIN, 1.5,(0,0, 255), 2)
            cv2.putText(img,result, (50, 350), cv2.FONT_HERSHEY_PLAIN, 4,(0,0, 255), 2)

    elif len(lmList) == 0 :

        cv2.putText(img,"Place your right hand on the screen", (50, 200), cv2.FONT_HERSHEY_PLAIN, 1,(255,0, 0), 2)
        
            
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime
    
    cv2.putText(img,"FPS: " + str(int(fps)), (10, 50), cv2.FONT_HERSHEY_PLAIN, 2,(255, 0, 255), 2)
    cv2.imshow("Image", img)
    cv2.waitKey(100)

