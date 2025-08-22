import cv2
import numpy as np
import os
import csv


# Configuration parameters
HEAD_COLOR = (255, 0, 0)  # Red for head detection
PHONE_COLOR = (0, 0, 255)  # Blue for phone detection

# Set paths to prediction folders
PREDICT_FOLDERS = ["predict1", "predict2"]  # Update with actual paths to folders containing images to process


def detect_objects(image_path):
    """
    Detect heads and phones in an image
    Args:
        image_path: Path to the image file
    Returns:
        heads: List of head bounding boxes [(x1, y1, x2, y2), ...]
        phones: List of phone bounding boxes [(x1, y1, x2, y2), ...]
    """
    # Read image
    img = cv2.imread(image_path)
    if img is None:
        return [], []

    # Convert to HSV color space for color detection
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    # Detect pure red (heads) - (255,0,0)
    # In HSV, pure red has H value 0 or 180, S and V values 255
    # Using a very narrow range to detect only pure red
    lower_red = np.array([0, 254, 254])
    upper_red = np.array([0, 255, 255])
    mask_red = cv2.inRange(hsv, lower_red, upper_red)

    # Detect pure blue (phones) - (0,0,255)
    # In HSV, pure blue has H value around 120, S and V values 255
    # Using a very narrow range to detect only pure blue
    lower_blue = np.array([120, 254, 254])
    upper_blue = np.array([120, 255, 255])
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)

    # Apply morphological operations to remove noise
    kernel = np.ones((5, 5), np.uint8)
    mask_red = cv2.morphologyEx(mask_red, cv2.MORPH_CLOSE, kernel)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_CLOSE, kernel)

    # Find contours
    contours_red, _ = cv2.findContours(mask_red, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours_blue, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # Get bounding boxes for heads and phones
    heads = []
    for contour in contours_red:
        x, y, w, h = cv2.boundingRect(contour)
        heads.append((x, y, x + w, y + h))

    phones = []
    for contour in contours_blue:
        x, y, w, h = cv2.boundingRect(contour)
        phones.append((x, y, x + w, y + h))

    return heads, phones


def classify_image(image_path):
    """
    Classify if person in image is using phone
    Simplified logic: If both head and phone are detected, classify as using phone
    Args:
        image_path: Path to the image file
    Returns:
        class_id: 0(using phone), 1(not using phone)
    """
    heads, phones = detect_objects(image_path)

    # If both head and phone are detected, classify as using phone
    if len(heads) > 0 and len(phones) > 0:
        return 0
    else:
        return 1


def process_all_images():
    """
    Process all images in specified folders and generate results CSV
    """
    if not PREDICT_FOLDERS or len(PREDICT_FOLDERS) == 0:
        print("Error: Please set valid prediction folder paths.")
        return

    # Check if folders exist
    for folder in PREDICT_FOLDERS:
        if not os.path.exists(folder):
            print(f"Warning: Folder {folder} does not exist, skipping.")

    # Prepare results list
    results = []


    for folder in PREDICT_FOLDERS:
        if not os.path.exists(folder):
            continue


        image_files = [f for f in os.listdir(folder) if f.lower().endswith(('.jpg', '.jpeg'))]


        for image_file in image_files:
            image_path = os.path.join(folder, image_file)
            class_id = classify_image(image_path)
 
            results.append((image_file, class_id))


    output_file = "result_detr.csv"
    with open(output_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(['image_name', 'class_id'])
        writer.writerows(results)

    print(f"done at {output_file}")


if __name__ == "__main__":
    # PREDICT_FOLDERS = ["path/to/predict1/folder", "path/to/predict2/folder"]
    if not PREDICT_FOLDERS or len(PREDICT_FOLDERS) == 0:
        print("error")
    else:
        process_all_images()