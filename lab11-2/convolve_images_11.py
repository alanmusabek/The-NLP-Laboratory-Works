import os
import cv2
import numpy as np

IMAGES_PATH = "images_conv"

def load_image(image_path):
    if not os.path.exists(IMAGES_PATH):
        os.makedirs(IMAGES_PATH)

    colored = cv2.imread(image_path)
    grey = cv2.cvtColor(colored, cv2.COLOR_BGR2GRAY)

    print("Image shape:", grey.shape)
    print("Top-left 5×5 pixels:\n", grey[:5, :5])

    return grey


def convolve2d(image, kernel):
    kernel = np.flipud(np.fliplr(kernel))  # flip kernel
    output = np.zeros_like(image)

    # zero-padding
    padded = np.zeros((image.shape[0] + 2, image.shape[1] + 2))
    padded[1:-1, 1:-1] = image

    for x in range(image.shape[1]):        # width
        for y in range(image.shape[0]):    # height
            output[y, x] = (kernel * padded[y:y+3, x:x+3]).sum()

    return output

blur_kernel = np.array([
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9],
    [1/9, 1/9, 1/9]
])

sharpen_kernel = np.array([
    [0, -1,  0],
    [-1, 5, -1],
    [0, -1,  0]
])

sobel_x = np.array([
    [-1, 0, 1],
    [-2, 0, 2],
    [-1, 0, 1]
])

def apply_all(image_path):

    img = load_image(image_path)

    # manual convolutions
    blur_manual = convolve2d(img, blur_kernel)
    sharpen_manual = convolve2d(img, sharpen_kernel)
    sobel_manual = convolve2d(img, sobel_x)

    # opencv convolutions
    blur_cv = cv2.filter2D(img, -1, blur_kernel)
    sharpen_cv = cv2.filter2D(img, -1, sharpen_kernel)
    sobel_cv = cv2.filter2D(img, -1, sobel_x)

    # save results
    cv2.imwrite(os.path.join(IMAGES_PATH, "blur_manual.jpg"), blur_manual)
    cv2.imwrite(os.path.join(IMAGES_PATH, "sharpen_manual.jpg"), sharpen_manual)
    cv2.imwrite(os.path.join(IMAGES_PATH, "sobel_manual.jpg"), sobel_manual)

    cv2.imwrite(os.path.join(IMAGES_PATH, "blur_cv.jpg"), blur_cv)
    cv2.imwrite(os.path.join(IMAGES_PATH, "sharpen_cv.jpg"), sharpen_cv)
    cv2.imwrite(os.path.join(IMAGES_PATH, "sobel_cv.jpg"), sobel_cv)

    print("\nSaved results to:", IMAGES_PATH)
    print("Files:")
    print(" - blur_manual.jpg / blur_cv.jpg")
    print(" - sharpen_manual.jpg / sharpen_cv.jpg")
    print(" - sobel_manual.jpg / sobel_cv.jpg")


if __name__ == "__main__":
    # Put your image name here
    apply_all("your_image.jpg")
