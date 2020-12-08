import cv2
import os
import numpy as np
from PIL import Image
import random2 as rdm   
import subprocess

def ambilgambar():
    cam = cv2.VideoCapture(0)
    cam.set(3, 640) 
    cam.set(4, 480)

    face_detector = cv2.CascadeClassifier('Cascades/haarcascade_frontalface_default.xml')
    face_id = input('\n Masukan User ID <return> ==>  ')
    

    print("\n Memulai Kamera")
    count = 0

    while(True):
        ret, img = cam.read()
        img = cv2.flip(img, 1)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1

            cv2.imwrite("dataset/User." + str(face_id) + '.' + str(count) + ".jpg", gray[y:y+h,x:x+w])

            cv2.imshow('image', img)


        k = cv2.waitKey(100) & 0xff 
        if k == 27:
            break
        elif count >= 40: 
            break

    print("\n Bersih Bersih ")
    cam.release()
    cv2.destroyAllWindows()
ambilgambar()


def trainGambar():
    path = 'dataset'
    noTelp1 = input('\n Masukan nomer telponmu <return> ==>  ')
    word = ['dede', 'didi', 'dodo']
    sendWord = rdm.choice(word)
    subprocess.call(['curl', '-X', 'POST', "https://api.thebigbox.id/sms-notification/1.0.0/messages", '-H', "accept: application/x-www-form-urlencoded", '-H', "x-api-key: 2y2XT6ELcv16nD92H4mTpktqdF2sEChk", '-H', "Content-Type: application/x-www-form-urlencoded", '-d', "msisdn="+ noTelp1 + '&content=' + sendWord])
    # subprocess.call(['curl', '-X', 'POST', 'https://api.thebigbox.id/sms-notification/1.0.0/messages','-H','accept: application/x-www-form-urlencoded','-H', 'x-api-key: 2y2XT6ELcv16nD92H4mTpktqdF2sEChk','-H', 'Content-Type: application/x-www-form-urlencoded', '-d' ,"msisdn='%s' content='%s'"] %) 
    

    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier("Cascades/haarcascade_frontalface_default.xml");


    def getImagesAndLabels(path):
        imagePaths = [os.path.join(path,f) for f in os.listdir(path)]     
        faceSamples=[]
        ids = []
        for imagePath in imagePaths:
            PIL_img = Image.open(imagePath).convert('L') 
            img_numpy = np.array(PIL_img,'uint8')
            id = int(os.path.split(imagePath)[-1].split(".")[1])
            faces = detector.detectMultiScale(img_numpy)
            for (x,y,w,h) in faces:
                faceSamples.append(img_numpy[y:y+h,x:x+w])
                ids.append(id)
        return faceSamples,ids

    print ("\n [INFO] Sedang Train Dataset ...")
    faces,ids = getImagesAndLabels(path)
    recognizer.train(faces, np.array(ids))


    recognizer.write('trainer.yml')

    print("\n [INFO] {0} Dataset Telah Disimpan".format(len(np.unique(ids))))
trainGambar()
