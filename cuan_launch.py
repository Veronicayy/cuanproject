import cv2
import numpy as np
import os 
import requests
import json
import urllib
from GetAndTrainCuan import sendWord
import time
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

def recognize_speech_from_mic(recognizer, microphone):
    with microphone as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

if __name__ == "__main__":
    # set the list of words, maxnumber of guesses, and prompt limit
    WORDS = sendWord
    NUM_GUESSES = 3
    PROMPT_LIMIT = 5

    # create recognizer and mic instances
    recognizer = sr.Recognizer()
    microphone = sr.Microphone()

        # format the instructions string
    instructions = (
        "Please Say The CodeWord\n"
        
        "You have {n} tries to Guess CodeWord.\n"
    ).format(words=', '.join(WORDS), n=NUM_GUESSES)

    # show instructions and wait 3 seconds before starting the game
    print(instructions)
    time.sleep(3)

    for i in range(NUM_GUESSES):
        # get the guess from the user
        # if    a transcription is returned, break out of the loop and
        #     continue
        # if no transcription returned and API request failed, break
        #     loop and continue
        # if API request succeeded but no transcription was returned,
        #     re-prompt the user to say their guess again. Do this up
        #     to PROMPT_LIMIT times
        for j in range(PROMPT_LIMIT):
            print('Guess {}. Please Say The CodeWord !'.format(i+1))
            guess = recognize_speech_from_mic(recognizer, microphone)
            if guess["transcription"]:
                break
            if not guess["success"]:
                break
            print("I didn't catch that. What did you say?\n")

        # if there was an error, stop the game
        if guess["error"]:
            print("ERROR: {}".format(guess["error"]))
            break

        # show the user the transcription
        print("You said: {}".format(guess["transcription"]))

        # determine if guess is correct and if any attempts remain
        guess_is_correct = guess["transcription"].lower() == word.lower()
        user_has_more_attempts = i < NUM_GUESSES - 1

        # determine if the user has won the game
        # if not, repeat the loop if user has more attempts
        # if no attempts left, the user loses the game
        if guess_is_correct:
            print("Correct!".format(word))
            break
        elif user_has_more_attempts:
            print("Incorrect. Try again.\n")
        else:
            print("Sorry, Time Is Up '{}'.".format(word))
            break