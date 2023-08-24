import cv2, time, os, sys
import numpy as np
import mediapipe as mp
from datetime import datetime

mp_drawing = mp.solutions.drawing_utils
mp_selfie_segmentation = mp.solutions.selfie_segmentation
selfie_segmentation = mp_selfie_segmentation.SelfieSegmentation(model_selection=1)


BG_COLOR = (192, 192, 192) # gray
cap = cv2.VideoCapture(0)
ret, image = cap.read()
(h,w,c)=image.shape
background = cv2.imread("transparent_picture.png")
bg_image = cv2.resize(background, (w,h))

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("영상 끝")
        cap = cv2.VideoCapture("test.mp4")
        success, image = cap.read()

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    results = selfie_segmentation.process(image)
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
    condition = np.stack((results.segmentation_mask,) * 3, axis=-1) > 0.1

    if bg_image is None:
        bg_image = np.zeros(image.shape, dtype=np.uint8)
        bg_image[:] = BG_COLOR

    # 이미지 픽셀 단위로 저장
    output_image = np.where(condition, image, bg_image)
    #
    output_filename = f"output_{datetime.now().strftime('%Y%m%d%H%M%S%f')}.png"
    cv2.imwrite(output_filename, output_image)

    cv2.imshow('MediaPipe Selfie Segmentation', output_image)
    time.sleep(0.025)
    if cv2.waitKey(1) == 27: # esc 키를 누르면 창이 닫힘
        cv2.destroyAllWindows()
        break