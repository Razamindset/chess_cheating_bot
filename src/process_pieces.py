import cv2
import numpy as np
import os

# Load the image
image_path = "chessboard.png"  # Change this to your image file
image = cv2.imread(image_path)

# Define board size
BOARD_SIZE = 8
H, W, _ = image.shape
SQUARE_SIZE = H // BOARD_SIZE

# Convert to grayscale and apply thresholding
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
_, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY_INV)

# Find contours of pieces
contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Create a directory for extracted pieces
output_dir = "extracted_pieces"
os.makedirs(output_dir, exist_ok=True)

# Process each detected piece
piece_count = 0
for contour in contours:
    x, y, w, h = cv2.boundingRect(contour)
    
    # Determine board row and column
    col = x // SQUARE_SIZE
    row = y // SQUARE_SIZE

    # Extract piece region
    piece_image = image[row * SQUARE_SIZE:(row + 1) * SQUARE_SIZE, 
                        col * SQUARE_SIZE:(col + 1) * SQUARE_SIZE]

    # Save the extracted piece image
    piece_filename = f"{output_dir}/piece_{row}_{col}.png"
    cv2.imwrite(piece_filename, piece_image)
    piece_count += 1

print(f"Extracted {piece_count} pieces and saved them in '{output_dir}'")
