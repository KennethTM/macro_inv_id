import numpy as np
import cv2
import time
from fastai.vision.all import *

if __name__ == "__main__":
  
  weights_dir = Path("models")/"resnet34-fin-ept-dk.export"
  learn_inf = load_learner(weights_dir)

  cap = cv2.VideoCapture('/dev/video0')

  while(True):
    time.sleep(1)

    # Capture frame-by-frame
    ret, frame = cap.read()

    img = PILImage.create(frame)

    pred, pred_idx, probs = learn_inf.predict(img)
    label = f'Navn: {pred} ({int(probs[pred_idx]*100)} %)'

    position = (10,50)
    cv2.putText(frame, label, (10,50), cv2.FONT_HERSHEY_SIMPLEX, 1, (209, 80, 0, 255), 3)

    # Display the resulting frame
    cv2.imshow('frame',frame)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        break

  # When everything done, release the capture
  cap.release()
  cv2.destroyAllWindows()