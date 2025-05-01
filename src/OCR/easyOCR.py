import easyocr, cv2

#run once
# reader = easyocr.Reader(['en'], gpu=False) # this needs to run only once to load the model into memory
# result = reader.readtext('test2.png')
# print(result)


def preprocess_image(image_path):
    # Load the image
    image = cv2.imread(image_path)

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Apply a threshold to get a binary image
    _, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)

    # Crop the bottom part of the image where subtitles usually appear
    height, width = binary.shape
    cropped = binary[int(height*0.1):height, 0:width]

    return cropped

def extract_text_from_image(image_path):
    # Preprocess the image
    processed_image = preprocess_image(image_path)

    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en'])  # Specify the language(s) you need

    # Perform OCR on the processed image
    result = reader.readtext(processed_image)

    # Extract and concatenate detected text
    detected_text = " ".join([text[1] for text in result])

    return detected_text

if __name__ == "__main__":
    image_path = 'test/test.png'
    detected_text = extract_text_from_image(image_path)
    print("Detected Text:", detected_text)