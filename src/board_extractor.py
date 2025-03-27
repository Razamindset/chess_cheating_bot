import cv2
import numpy as np
import os

reference_pieces_dir = "src/assets"

# Load reference piece images
piece_types = {
    "P": "wp.png", "N": "wn.png", "B": "wb.png", "R": "wr.png", "Q": "wq.png", "K": "wk.png",
    "p": "bp.png", "n": "bn.png", "b": "bb.png", "r": "br.png", "q": "bq.png", "k": "bk.png",
    "dark": "empty-dark.png",
    "light": "empty-light.png"
}


# Load images
reference_pieces = {}
for piece, filename in piece_types.items():
    path = os.path.join(reference_pieces_dir, filename)
    ref_img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    
    # if ref_img is None:
    #     print(f"Error: Failed to load {filename} at {path}")
    # else:
    #     print(f"Loaded {filename} successfully.")
    
    reference_pieces[piece] = ref_img


# 2. Load the Chessboard Screenshot
board_image_path = "screenshot.png"  # Change this to your board image
board_image = cv2.imread(board_image_path)
if board_image is None:
    raise ValueError("Board image not found!")


# Convert to grayscale
gray_board = cv2.cvtColor(board_image, cv2.COLOR_BGR2GRAY)

# Get board dimensions
H, W = gray_board.shape
SQUARE_SIZE = H // 8  # Assuming a square board

print(f"Board image loaded with size: {H}x{W}")



# 3. Function to Compare Images (Mean Squared Error)
def match_piece(image):
    best_match = None
    best_score = float("inf")  # Lower is better

    for piece, ref_img in reference_pieces.items():
        ref_resized = cv2.resize(ref_img, (SQUARE_SIZE, SQUARE_SIZE))

        # Compute Mean Squared Error (MSE)
        diff = np.abs(image.astype("float") - ref_resized.astype("float"))
        score = np.mean(diff)

        if score < best_score:
            best_score = score
            best_match = piece

    return best_match if best_score < 50 else None  # Adjust threshold if needed

# 4. Loop Through Each Square and Identify Pieces
board_state = [["" for _ in range(8)] for _ in range(8)]



for row in range(8):
    for col in range(8):
        # Extract square region
        y1, y2 = row * SQUARE_SIZE, (row + 1) * SQUARE_SIZE
        x1, x2 = col * SQUARE_SIZE, (col + 1) * SQUARE_SIZE
        square_img = gray_board[y1:y2, x1:x2]

        # Match piece
        matched_piece = match_piece(square_img)
        board_state[row][col] = matched_piece if matched_piece else " "

print("Board extraction and matching completed!")

# 5. Print Board State (for Debugging)
for row in board_state:
    print(" ".join(row))

