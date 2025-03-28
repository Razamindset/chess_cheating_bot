from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from bs4 import BeautifulSoup
import re
from typing import List, Dict
import time
from stockfish import Stockfish


# * Fishy Buisness
STOCKFISH_PATH = "/usr/games/stockfish"  
stockfish = Stockfish(STOCKFISH_PATH)
stockfish.set_depth(15)

def get_best_move(fen: str):
    """Returns the best move from Stockfish for the given FEN."""
    stockfish.set_fen_position(fen)
    best_move = stockfish.get_best_move()
    return best_move

# Scrapping and UI related fucntions

perspective = ""

def print_board(board):
    for row in board:
        for piece in row:
            print(piece, end=" ")
        
        print()


# Calculate the square size using the board measure
def get_square_size(driver):
    """Dynamically calculate the size of each square."""
    board_element = driver.find_element("css selector", "cg-board")
    board_size = board_element.size  # Get board dimensions
    print(board_size)
    square_size = board_size['width'] / 8  # Assuming a square board
    return square_size


def html_to_fen(board_html: str, square_size: int, side_to_move:str) -> str:
    # Mapping of piece classes to FEN notation
    piece_map: Dict[str, str] = {
        'black rook': 'r',
        'black knight': 'n',
        'black bishop': 'b',
        'black queen': 'q',
        'black king': 'k',
        'black pawn': 'p',
        'white rook': 'R',
        'white knight': 'N',
        'white bishop': 'B',
        'white queen': 'Q',
        'white king': 'K',
        'white pawn': 'P'
    }


    # Create an 8x8 board filled with empty squares
    board: List[List[str]] = [['.'] * 8 for _ in range(8)]

    # Debug: print the entire board_html to see its structure
    # print("Full board HTML:", str(board_html))

    str_html = str(board_html)

    #! If any peice is sected or being dragged the fen calcutaion will be abandoned
    if 'selected' in str_html or "dragging" in str_html:
        # print("Found a pwn dragging or selected returning")
        return "error"
    
    # Extract all piece elements 
    piece_elements = re.findall(
        r'<piece[^>]*>',
        str_html
    )

    # These are square highlighting check last move and dests etc 
    square_elements = re.findall(r'<square[^>]*>', str_html)
    
    for piece in piece_elements:
        class_match = re.search(r'class="([^"]+)"', piece)
        if not class_match:
            continue
        piece_class = class_match.group(1)


        # Extract transform
        transform_match = re.search(r'transform: translate\((\d+)px, (\d+)px\)', piece)
        if not transform_match:
            continue
        
        x = int(transform_match.group(1))
        y = int(transform_match.group(2))

        # Calculate board coordinates
        board_x = round(x / square_size)
        board_y = round(y / square_size)

        fen_symbol = piece_map.get(piece_class, '.')

        board[board_y][board_x] = fen_symbol

    # Filter squares that have the "last-move" class
    square_elements = [sq for sq in square_elements if 'last-move' in sq]

    # We get two square elements one is the move.from and other is move.to
    if len(square_elements) < 2:
        print("Invalid input: Need both 'from' and 'to' squares.")
        return "error"
    
    # The perspective will be calculted only once
    global perspective
    if(perspective == ""):
        perspective = "b" if board[7][7].islower() else "w"

    fen = ""
    # Print the board and build the FEN string
    for i in range(0, 8):
        empty_count = 0  # Reset empty_count at the start of each row
        for j in range(0, 8):
            if perspective == "b":
                piece = board[7 - i][7 - j]
            else:
                piece = board[i][j]

            if piece == '.':
                empty_count += 1
            else:
                if empty_count > 0:
                    fen += str(empty_count)
                    empty_count = 0  # Reset after adding the count
                fen += piece


        if empty_count > 0:
            fen += str(empty_count)
        if i < 7:
            fen += "/"

   
    fen += f" {side_to_move} - - 0 1" 
            
    return fen


from bs4 import BeautifulSoup

def determine_side_to_move_from_moves(html_content: str) -> str:
    """
    Determines the side to move (white or black) from the move list in HTML.

    Args:
        html_content (str): The HTML content of the chess game.

    Returns:
        str: "w" for white, "b" for black, or "" if it cannot be determined.
    """
    try:
        soup = BeautifulSoup(html_content, 'html.parser')
        moves_list = soup.find('l4x')  # Find the <l4x> tag

        if moves_list:
            move_tags = moves_list.find_all('kwdb')  # Find all <kwdb> tags
            move_count = len(move_tags)

            if move_count % 2 == 0:
                return "w"  # Even number of moves, black's turn
            else:
                return "b"  # Odd number of moves, white's turn
        else:
            return ""  # Could not find the move list
    except Exception as e:
        print(f"Error determining side to move: {e}")
        return ""  # An error occurred

def extract_fen_from_html(html_content, square_size):
    """Extracts FEN string from HTML content using BeautifulSoup."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html_content, 'html.parser')
    board_div = soup.find('cg-board')
    if not board_div:
        print("Could not find main-board div.")
        return ""

    side_to_move = determine_side_to_move_from_moves(html_content)

    try:
        res = html_to_fen(board_div, square_size, side_to_move)
        if res == "error":
            return ""
        return res
    except KeyError:
        print("Could not find 'data-fen' attribute.")
        return ""

# Folowing functions will be related to move automation 

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By

def draw_click_marker(driver, x, y):
    """Draws a marker on the screen at the given coordinates."""
    js_code = f"""
        var marker = document.createElement('div');
        marker.style.position = 'absolute';
        marker.style.left = '{x}px';
        marker.style.top = '{y}px';
        marker.style.width = '20px';
        marker.style.height = '20px';
        marker.style.background = 'red';
        marker.style.zIndex = '9999'; // Make it appear on top
        document.body.appendChild(marker);
    """
    driver.execute_script(js_code)

def make_move(driver, move: str, square_size: int):
    """
    Makes a move on the Lichess board using Selenium.

    Args:
        driver: The Selenium WebDriver instance.
        move: The move in algebraic notation (e.g., "e2e4").
        square_size: The size of each square on the board in pixels.
    """
    try:
        from_square = move[:2]  # Extract the "from" square (e.g., "e2")
        to_square = move[2:4]  # Extract the "to" square (e.g., "e4")
        print("In move making")

        # Convert algebraic notation to pixel coordinates
        from_x, from_y = algebraic_to_pixels(from_square, square_size)
        to_x, to_y = algebraic_to_pixels(to_square, square_size)

        print(f"From square: {from_square}, To square: {to_square}")  # Debugging
        print(f"From: {from_x}, {from_y}, To: {to_x}, {to_y}")  # Debugging


       
        # Click on the "from" square
        draw_click_marker(driver, from_x, 2*from_y)
        # actions = ActionChains(driver)
        # actions.move_to_element_with_offset(driver.find_element(By.CSS_SELECTOR, "cg-board"), from_x, from_y)
        # actions.click()
        # actions.perform()

        # Click on the "to" square
        # actions = ActionChains(driver)
        # actions.move_to_element_with_offset(driver.find_element(By.CSS_SELECTOR, "cg-board"), to_x, to_y)
        # actions.click()
        # actions.perform()


        print(f"Made move: {move}")

    except Exception as e:
        print(f"Error making move: {e}")

def algebraic_to_pixels(square: str, square_size: int):
    """Converts algebraic notation (e.g., "e4") to pixel coordinates."""
    file = ord(square[0]) - ord('a')  # 'a' = 0, 'b' = 1, etc.
    rank = int(square[1]) - 1  # '1' = 0, '2' = 1, etc.

    x = file * square_size + square_size / 2  # Center of the square
    y = (7 - rank) * square_size + square_size / 2  # Center of the square (inverted y-axis)

    return x, y

# * Connecting all the masala here
def main():
    """Continuously monitors the FEN string and prints when it changes."""
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        driver = webdriver.Chrome(options=chrome_options)
        target_tab_title = "lichess.org"
        found = False

        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if target_tab_title in driver.title:
                found = True
                print("Connected to Lichess!")
                break

        if not found:
            print("Lichess tab not found!")
            return

        square_size = get_square_size(driver)
        last_fen = None
        best_move = None
        stockfish_processing = False  # Flag to track if Stockfish is running

        while True:
            html_content = driver.page_source
            if not html_content:
                print("No HTML data found!")
                return

            if "Checkmate" in html_content:
                print("The game is over")
                return

            if "You play the white pieces" in html_content:
                if best_move is None:
                    best_move = get_best_move("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
                    print(best_move)
                continue

            current_fen = extract_fen_from_html(html_content, square_size)
            if current_fen and current_fen != last_fen:
                print(f"Position Change: {current_fen}")
                last_fen = current_fen

                global perspective
                side_to_move = last_fen.split()[1]

                if side_to_move == perspective and not stockfish_processing:
                    stockfish_processing = True  # Set the flag
                    print("Calling stockfish with new fen")
                    best_move = get_best_move(last_fen)
                    print(best_move)
                    stockfish_processing = False  # Reset the flag
                    make_move(driver, best_move, square_size)

            # time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if driver:
            driver.quit()


if __name__ == "__main__":
    main()
    # print(get_best_move("r1b2b1r/ppp1k2p/3p1np1/4p1N1/2NnP3/3P4/PPP2PPP/R1B1K2R b - - 0 1"))