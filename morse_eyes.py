from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
from morse_converter import convertMorseToText
from collections import deque
import numpy as np
from morse_log import log

class Detectmorse():

    # Constructor...
    def __init__(self):
        self.flag = 0
        self.openEye = 0
        self.str = ''
        self.finalString = []
        global L
        self.L = []
        self.closed = False
        self.timer = 0
        self.final = ''
        self.pts = deque(maxlen=512)
        self.thresh = 0.25
        self.dot = 10
        self.dash = 40
        self.detect = dlib.get_frontal_face_detector()
        self.predict = dlib.shape_predictor(
            "shape_predictor_68_face_landmarks.dat")  # Dat file is the crux of the code

        (self.lStart, self.lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (self.rStart, self.rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

    def eye_aspect_ratio(self,eye):
        A = distance.euclidean(eye[1], eye[5])
        B = distance.euclidean(eye[2], eye[4])
        C = distance.euclidean(eye[0], eye[3])
        self.ear = (A + B) / (2.0 * C)
        return self.ear


    def calculate(self,frame):

        decoded = cv2.imdecode(np.frombuffer(frame, np.uint8), -1)
        frame = imutils.resize(decoded, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        subjects = self.detect(gray, 0)
        for subject in subjects:
            shape = self.predict(gray, subject)
            shape = face_utils.shape_to_np(shape)  # converting to NumPy Array
            leftEye = shape[self.lStart:self.lEnd]
            rightEye = shape[self.rStart:self.rEnd]
            leftEAR = self.eye_aspect_ratio(leftEye)
            rightEAR = self.eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            if ear < self.thresh:  # closed eyes
                self.flag += 1
                self.pts.appendleft(self.flag)
                self.openEye = 0
            else:
                self.openEye += 1
                self.flag = 0
                self.pts.appendleft(self.flag)
            for i in range(1, len(self.pts)):
                if self.pts[i] > self.pts[i - 1]:
                    # print(pts[i - 1], pts[i])
                    if self.pts[i] > 30 and self.pts[i] < 60:
                        print("Eyes have been closed for 50 frames! - Print '-'")
                        log("Eyes have been closed for 50 frames!")
                        self.L.append("-")
                        self.pts = deque(maxlen=512)
                        break
                    elif self.pts[i] > 15 and self.pts[i] < 30:
                        print("Eyes have been closed for 20 frames!")
                        log("Eyes have been closed for 20 frames! - Print '.'")
                        self.L.append(".")
                        self.pts = deque(maxlen=512)
                        break

                    elif self.pts[i] > 60:
                        print("Eyes have been closed for 60 frames!")
                        log("Eyes have been closed for 60 frames! - Remove morse character")
                        self.L.pop()
                        self.pts = deque(maxlen=512)
                        break

        if (self.L != []):

            print(self.L)
        if self.openEye > 60:
            if (self.L != []):
                print(self.L)
            self.str = convertMorseToText(''.join(self.L))

            if self.str != None:
                print(self.str)
                self.finalString.append(self.str)
                self.final = ''.join(self.finalString)
            if self.str == None:
                self.L = []
            self.L = []
        cv2.putText(frame, "Predicted :  " + self.final, (10, 470),
                    cv2.FONT_HERSHEY_DUPLEX, 0.7, (52, 152, 219), 2)
        ret, png = cv2.imencode('.png', frame)
        return png, self.L


