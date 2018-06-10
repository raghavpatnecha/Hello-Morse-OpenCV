from scipy.spatial import distance
from imutils import face_utils
import imutils
import dlib
import cv2
from morse_converter import convertMorseToText
from collections import deque

def eye_aspect_ratio(eye):
    A = distance.euclidean(eye[1], eye[5])
    B = distance.euclidean(eye[2], eye[4])
    C = distance.euclidean(eye[0], eye[3])
    ear = (A + B) / (2.0 * C)
    return ear


thresh = 0.25
dot = 10
dash=40
detect = dlib.get_frontal_face_detector()
predict = dlib.shape_predictor(
    "F:\projects\morse\shape_predictor_68_face_landmarks.dat")  # Dat file is the crux of the code

(lStart, lEnd) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
(rStart, rEnd) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]
def main():
    cap = cv2.VideoCapture(0)
    flag = 0
    openEye=0
    final = ''
    str = ''
    finalString=[]
    L = []
    closed = False
    timer = 0
    pts = deque(maxlen=512)

    while True:
        ret, frame = cap.read()
        #cam1 = Camera()
        #frame = cam1.get_frame()
        frame = imutils.resize(frame, width=640)
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        subjects = detect(gray, 0)
        for subject in subjects:
            shape = predict(gray, subject)
            shape = face_utils.shape_to_np(shape)  # converting to NumPy Array
            leftEye = shape[lStart:lEnd]
            rightEye = shape[rStart:rEnd]
            leftEAR = eye_aspect_ratio(leftEye)
            rightEAR = eye_aspect_ratio(rightEye)
            ear = (leftEAR + rightEAR) / 2.0
            leftEyeHull = cv2.convexHull(leftEye)
            rightEyeHull = cv2.convexHull(rightEye)
            cv2.drawContours(frame, [leftEyeHull], -1, (0, 255, 0), 1)
            cv2.drawContours(frame, [rightEyeHull], -1, (0, 255, 0), 1)
            if ear < thresh: #closed eyes
                flag+=1
                pts.appendleft(flag)
                openEye=0
            else:
                openEye+=1
                flag=0
                pts.appendleft(flag)
            for i in range(1, len(pts)):
                if pts[i] > pts[i - 1]:
                    #print(pts[i - 1], pts[i])
                    if pts[i] > 30 and pts[i]<60:
                        print("Eyes have been closed for 50 frames!")
                        L.append("-")
                        pts = deque(maxlen=512)
                        break
                    elif pts[i] > 15 and pts[i]<30:
                        print("Eyes have been closed for 20 frames!")
                        L.append(".")
                        pts = deque(maxlen=512)
                        break

                    elif pts[i] > 60:
                        print("Eyes have been closed for 60 frames!")
                        L.pop()
                        pts = deque(maxlen=512)
                        break

        if (L != []):
            print(L)
        if openEye>60:
            if (L!=[]):
                print(L)
            str=convertMorseToText(''.join(L))

            if str != None:
                print(str)
                finalString.append(str)
                final=(''.join(finalString))
            if str==None:
                L=[]
            L=[]
        cv2.putText(frame, "Predicted :  " + final, (10, 470),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
        cv2.imshow("Frame", frame)
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            break
    cv2.destroyAllWindows()
    cap.stop()

if __name__ == '__main__':
    main()

