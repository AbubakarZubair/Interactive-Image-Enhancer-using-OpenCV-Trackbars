import cv2
import numpy as np

# Callback function for the trackbars (it does nothing but is required by OpenCV)
def nothing(x):
    pass

# Load an image
image_path = 'Coins.png'
image = cv2.imread(image_path)

# Check if the image was loaded correctly
if image is None:
    print(f"Error: Could not load image from {image_path}.")
    exit()

# Desired output window size
output_width = 600
output_height = 300

# Convert the image to HSV color space for saturation adjustment
image_hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

# Create a window named 'Image'
cv2.namedWindow('Image')

# Create trackbars for brightness, contrast, saturation, and gamma correction
cv2.createTrackbar('Brightness', 'Image', 50, 100, nothing)
cv2.createTrackbar('Contrast', 'Image', 50, 100, nothing)
cv2.createTrackbar('Saturation', 'Image', 50, 100, nothing)
cv2.createTrackbar('Gamma', 'Image', 100, 200, nothing)

while True:
    # Get the current positions of the trackbars
    brightness = cv2.getTrackbarPos('Brightness', 'Image')
    contrast = cv2.getTrackbarPos('Contrast', 'Image')
    saturation = cv2.getTrackbarPos('Saturation', 'Image')
    gamma = cv2.getTrackbarPos('Gamma', 'Image')

    # Adjust brightness and contrast
    alpha = contrast / 50.0  # Scale factor to adjust contrast
    beta = brightness - 50   # Offset to adjust brightness
    adjusted_image = cv2.convertScaleAbs(image, alpha=alpha, beta=beta)

    # Adjust saturation
    hsv_image = cv2.cvtColor(adjusted_image, cv2.COLOR_BGR2HSV)
    hsv_image[:, :, 1] = np.clip(hsv_image[:, :, 1] * (saturation / 50.0), 0, 255)
    adjusted_image = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

    # Adjust gamma
    gamma_value = gamma / 100.0
    inv_gamma = 1.0 / gamma_value
    table = np.array([(i / 255.0) ** inv_gamma * 255 for i in np.arange(0, 256)]).astype("uint8")
    adjusted_image = cv2.LUT(adjusted_image, table)

    # Resize the image to the desired output size
    resized_image = cv2.resize(adjusted_image, (output_width, output_height))

    # Display the adjusted image
    cv2.imshow('Image', resized_image)

    # Break the loop when the user presses 'Esc' key
    if cv2.waitKey(1) & 0xFF == 27:
        break

# Release all resources
cv2.destroyAllWindows()
