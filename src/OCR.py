from paddleocr import PaddleOCR,draw_ocr
import os
import cv2 as cv
import sys

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.

class OCR:
    # TODO: add option of using other OCRs later
    def __init__(self):
        # need to run only once to download and load model into memory
        self.myOcr = PaddleOCR(use_angle_cls=True, lang='en', use_gpu=False, enable_mkldnn=True, debug = False, show_log = False)

    def __init__(self, ocrName="Paddle"):
        self.myOcr = PaddleOCR(use_angle_cls=True, lang='en', debug = False, show_log = False) 

    def infer(self, img_path):

        result = self.myOcr.ocr(img_path, cls=True)
        #print("Result::", result)
        
        if result[0] != None:
            for idx in range(len(result)):
                res = result[idx]
                text = ''
                for line in res:
                    text = text + " " + line[1][0]
                #print(text)

if __name__ == "__main__":
    testOCR = OCR()
    img = cv.imread(cv.samples.findFile("test/test.png"))
     
    if img is None:
        sys.exit("Could not read the image.")

    height, width, channels = img.shape
    img = img[int(height*0.85):height, int(width*0.18):int(width*0.9)]
    #cv.imshow("Display window", img)
    #k = cv.waitKey(0)

    testOCR.infer(img)