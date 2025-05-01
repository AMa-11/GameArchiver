from paddleocr import PaddleOCR,draw_ocr
import os

# Paddleocr supports Chinese, English, French, German, Korean and Japanese.
# You can set the parameter `lang` as `ch`, `en`, `fr`, `german`, `korean`, `japan`
# to switch the language model in order.
ocr = PaddleOCR(use_angle_cls=True, lang='en', debug = False, show_log = False) # need to run only once to download and load model into memory

def test():
    directory = 'test'
    for filename in os.listdir(directory):
        image = os.path.join(directory, filename)
        # checking if it is a file
        if os.path.isfile(image):
            infer(image)
            
def infer(img_path):
    # need to run only once to download and load model into memory
    result = ocr.ocr(img_path, cls=True)
    print(result)
    for idx in range(len(result)):
        res = result[idx]
        text = ''
        for line in res:
            text = text + " " + line[1][0]
        print(text)

if __name__ == "__main__":
    #test()
    infer("test/test6.png")


# draw result
# from PIL import Image
# result = result[0]
# image = Image.open(img_path).convert('RGB')
# boxes = [line[0] for line in result]
# txts = [line[1][0] for line in result]
# scores = [line[1][1] for line in result]
# im_show = draw_ocr(image, boxes, txts, scores, font_path='./fonts/simfang.ttf')
# im_show = Image.fromarray(im_show)
# im_show.save('result.jpg')