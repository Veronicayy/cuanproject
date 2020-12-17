import cv2
import numpy as np
import os 
import requests
import json
import urllib
from GetAndTrainnew import sendWord
import speech_recognition as sr

# MASUKIN FILE RECOGNIZER HASIL TRAINING
filePengenal = cv2.face.LBPHFaceRecognizer_create()
filePengenal.read('trainer.yml')
fileHaarcascade = "Cascades/haarcascade_frontalface_default.xml"
haarcasCadeWajah = cv2.CascadeClassifier(fileHaarcascade)
font = cv2.FONT_HERSHEY_SIMPLEX
#COUNTER DIMULAI DARI 0 YA MAS
id = 0
# NAMA SESUAI DENGAN INDEX DI FILE 01url = 'http://webdee.xyz/api/get.php'
url = 'http://webdee.xyz/api/get.php'
r=requests.get(url)
data = r.json()
for i in data:
    nama = data[i]['nama']
    print(nama)

# nama = ['dimas', 'Mamang Kanbaw']

# MULAI KAMERA (BISA DIATUR UKURANNYA SESUAI KEBUTUHAN DAN SPESIFIKASI)
cam = cv2.VideoCapture(0)
cam.set(3, 640) # LEBAR
cam.set(4, 480) # TINGGI
# UKURAN WINDOW
lebarMinimal = 0.1*cam.get(3)
tinggiMinimal = 0.1*cam.get(4)
while True:
    ret, img =cam.read()
    img = cv2.flip(img, 1) 
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    
    wajah = haarcasCadeWajah.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        minSize = (int(lebarMinimal), int(tinggiMinimal)),
       )
    for(x,y,w,h) in wajah:
        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)
        id, confidence = filePengenal.predict(gray[y:y+h,x:x+w])
        # CEK CONFIDENCE
        url = 'http://webdee.xyz/api/get.php'
        r=requests.get(url)
        data = r.json()
        # dataStr = json.dumps(data)
        for i in data:
            nama = data[i]['nama']
            # print(nama)
        if (confidence < 100 and confidence>35):
            id = nama[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
       
        cv2.putText(img, str(id), (20,20), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (255,255,0), 1) 
    
    cv2.imshow('camera',img) 
    k = cv2.waitKey(10) & 0xff 
    if k == 27:
        break

print("\n BERSIH BERSIH MASE")
cam.release()
cv2.destroyAllWindows()

