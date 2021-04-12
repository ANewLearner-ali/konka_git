import cv2
import logging

from utils import image_utils


def capture_shot(path):
    cap = None
    try:
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            image_utils.write_img(path, frame)
            return True
        else:
            return False
    except BaseException as e:
        logging.exception(e)
    finally:
        if cap is not None:
            cap.release()
    return False