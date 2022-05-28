from cProfile import run
from email.policy import default
from flask import Flask, render_template
from datetime import datetime
import cv2
from matplotlib import image
import numpy as np
import face_recognition
import os
import sys
from datetime import datetime
camvar=True

#code for getting list
path='./images/images'
imagesAtt = []
classNames = []
myList = os.listdir(path)
print(myList)

#for getting classes
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    imagesAtt.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

#encoding of images
def findEncodings(imagesAtt):
    encodeList = []
    for img in imagesAtt:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encode = face_recognition.face_encodings(img)[0]
        encodeList.append(encode)
    return encodeList
#for marking attendance in excel sheet
def markAttendance(name):
    with open('./images/Attendance.csv','r+') as f:
        myDataList = f.readlines()
        nameList = []
        for line in myDataList:
            entry = line.split(',')
            nameList.append(entry[0])
        if name not in nameList:
            now = datetime.now()
            dtString = now.strftime('%H:%M:%S')
            f.writelines(f'\n{name} , {dtString}')
          
encodeListKnown = findEncodings(imagesAtt)
print('encoding complete')
#for webcam
cap = cv2.VideoCapture(0)


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']= "sqlite:///todo.db"
app.config['SQLALCHEMY_DATABASE_URI']= False

@app.route("/cam")
def hello_world():
    global camvar
    print("working")

    
    while True:
        success,img = cap.read()
        imgS = cv2.resize(img,(0,0),None,0.25,0.25)
        imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

        facesCurFrame = face_recognition.face_locations(imgS)
        encodesCurFrame = face_recognition.face_encodings(imgS,facesCurFrame)

        for encodeFace,faceLoc in zip(encodesCurFrame,facesCurFrame):
            matches = face_recognition.compare_faces(encodeListKnown,encodeFace)
            faceDis = face_recognition.face_distance(encodeListKnown,encodeFace)
            #print(faceDis)
            matchIndex=np.argmin(faceDis)

            if matches[matchIndex]:
                name = classNames[matchIndex].upper()
                print(name)
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255),2)
                markAttendance(name)
            else :
                name="unknown"
                y1,x2,y2,x1 = faceLoc
                y1,x2,y2,x1 = y1*4,x2*4,y2*4,x1*4
                cv2.rectangle(img,(x1,y1),(x2,y2),(0,255,0),2)
                cv2.rectangle(img,(x1,y2-35),(x2,y2),(0,255,0),cv2.FILLED)
                cv2.putText(img,name,(x1+6,y2-6),cv2.FONT_HERSHEY_COMPLEX,1,(255,255,255))
                
        cv2.imshow('Webcam',img)
        cv2.waitKey(10)
            

#button funntionalities
@app.route("/")
def products():
    print("woking")
    return render_template('index.html')


@app.route("/closecam")
def closecam():
    global camvar
    #global cv2
    camvar=False
    cap.release();
    cv2.destroyAllWindows()
    print("woking")

    return render_template('index.html') 




@app.route("/statistic")
def product():
    print("sheet")

    return render_template('attendance.html')  


@app.route("/nextpage")
def productss():
    

    return render_template('second.html')  
from analyze import   *
@app.route("/mofie")
def mofie():
    print("updating")
    profile()
    

    return render_template('second.html') 

if __name__ == "__main__":
 app.run(debug=True)