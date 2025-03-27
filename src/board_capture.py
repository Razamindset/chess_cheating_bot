import pyscreenshot as ImageGrab
import os
import time

os.environ["SCROT_PARAMS"] = "--silent"  # Suppress the sound

# Tweak this to apture tht board area only
def capture_board():
    start_value_x=105
    start_value_y=185

    board_width = 510

    end_value_x = start_value_x + board_width
    end_value_y = start_value_y + board_width

    region = [start_value_x, start_value_y, end_value_x, end_value_y]

    im = ImageGrab.grab(bbox=region, childprocess=False)
    im.save("chessboard_capture.png")


time.sleep(2)    
capture_board()
