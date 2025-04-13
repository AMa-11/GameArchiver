import cv2

#may not be needed
def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)
    
    height, width, channels = image.shape
    print(image.shape)

    cropped = image[int(height*0.86):height, int(width*0.16):int(width*0.90)]

    cv2.imwrite('test/image1.png', cropped)


if __name__ == "__main__":
    image_path = 'test/test.png'
    preprocess_image('test/test.png')