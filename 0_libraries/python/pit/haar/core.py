import cv2
import os

# Based on the Open CV Haar example from Geeks for Geeks
# https://www.geeksforgeeks.org/face-detection-using-cascade-classifier-using-opencv-python/

class HaarDetect():
    haar_location   = os.getenv('QAL_DIR') +'\\0_libraries\\python\\pit\\haar\\'
    face_cascade    = cv2.CascadeClassifier(haar_location+'haarcascade_frontalface_default.xml')
    eye_cascade     = cv2.CascadeClassifier(haar_location+'haarcascade_eye.xml')

    def __init__(self):
        pass

    def adjusted_detect_face(self, img, color=(255, 255, 255), thickness=5):
        face_img = img.copy()
        face_rect = self.face_cascade.detectMultiScale(face_img, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in face_rect:
            cv2.rectangle(face_img, (x, y), (x + w, y + h), color, thickness)

        return face_img

    def detect_eyes(self, img, color=(255, 255, 255), thickness=5):
        eye_img = img.copy()
        eye_rect = self.eye_cascade.detectMultiScale(eye_img, scaleFactor=1.2, minNeighbors=5)

        for (x, y, w, h) in eye_rect:
            cv2.rectangle(eye_img, (x, y), (x + w, y + h), color, thickness)

        return eye_img