from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import re
import time
from bs4 import BeautifulSoup
import chess
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from stockfish import Stockfish
from selenium.webdriver.common.by import By

STOCKFISH_PATH = "/usr/games/stockfish"

def initialize_stockfish():
    try:
        stockfish = Stockfish(STOCKFISH_PATH)
        return stockfish
    except Exception as e:
        print(f"Error initializing Stockfish: {e}")
        return None

stockfish = initialize_stockfish()  # Initialize Stockfish globally

def get_best_move(fen: str):
    global stockfish
    if stockfish is None:
        stockfish = initialize_stockfish()
    if stockfish is None:
        return None  # Stockfish still not available

    try:
        stockfish.set_fen_position(fen)
        return stockfish.get_best_move()
    except Exception as e:
        print(f"Stockfish error: {e}. Reloading Stockfish.")
        stockfish = initialize_stockfish()
        return None



def extract_game_info(driver):
    """Extracts FEN, side, and side to move from Chess.com HTML."""
    try:
        html_content = driver.page_source
        soup = BeautifulSoup(html_content, 'html.parser')

        # Determine board orientation
        board_element = soup.find('wc-chess-board')
        if board_element and 'flipped' in board_element.get('class', []):
            my_side = 'b'  # Black
        else:
            my_side = 'w'  # White

        # Extract FEN
        fen = extract_fen_from_chesscom(driver)


        # Determine side to move
        move_list_element = soup.find('wc-simple-move-list')
        if move_list_element:
            moves = move_list_element.find_all(class_='main-line-ply')
            if len(moves) % 2 == 0:
                side_to_move = 'w'  # White's turn
            else:
                side_to_move = 'b'  # Black's turn
        else:
            side_to_move = None  # Could not determine

        fen += f" {side_to_move} - - 0 1"

        return fen, my_side, side_to_move

    except Exception as e:
        print(f"Error extracting game info: {e}")
        return None, None, None



def extract_fen_from_chesscom(driver):
    try:
        board_element = driver.find_element("css selector", "wc-chess-board")
        html_content = board_element.get_attribute("innerHTML")

        piece_map = {
            'br': 'r', 'bn': 'n', 'bb': 'b', 'bq': 'q', 'bk': 'k', 'bp': 'p',
            'wr': 'R', 'wn': 'N', 'wb': 'B', 'wq': 'Q', 'wk': 'K', 'wp': 'P'
        }

        board = [['.'] * 8 for _ in range(8)]

        piece_elements = re.findall(r'piece(?: (\w+))? square-(\d+)(?: (\w+))?', html_content)

        for match in piece_elements:
            piece_class = None
            square = None
            for item in match:
                if item and item.isdigit():
                    square = item
                elif item and item in piece_map:
                    piece_class = item
            if square:
                piece = piece_map.get(piece_class, '.')
                file = int(square[0]) - 1
                rank = 8 - int(square[1])
                rank = 8 - int(square[1])
                board[rank][file] = piece

        fen = ""
        for row in board:
            empty_count = 0
            for piece in row:
                if piece == '.':
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen += str(empty_count)
                        empty_count = 0
                    fen += piece
            if empty_count > 0:
                fen += str(empty_count)
            fen += '/'
        fen = fen[:-1]
        return fen
    except Exception as e:
        print(f"Error extracting FEN: {e}")
        return ""

def print_board(fen: str):
    board = chess.Board(fen)
    print(board)

def algebraic_to_pixels(square: str, square_size: int):
    file = ord(square[0]) - ord('a') + 1
    rank = int(square[1]) - 1 + 1
    square_class = "square-" + str(file) + str(rank)
    return square_class

def make_move(driver, move: str, square_size: int, my_side: str):
    try:
        from_square = move[:2]
        to_square = move[2:4]
        promotion_piece = None

        if len(move) == 5:  # Check for promotion
            promotion_piece = move[4]

        from_square_class = algebraic_to_pixels(from_square, square_size)
        to_square_class = algebraic_to_pixels(to_square, square_size)

        try:
            actions = ActionChains(driver)

            element = driver.find_element(By.CSS_SELECTOR, f"div[class*='{from_square_class}']")
            actions.move_to_element(element)
            actions.click()
            actions.perform()

            element = driver.find_element(By.CSS_SELECTOR, f"div[class*='{to_square_class}']")
            actions.move_to_element(element)
            actions.click()
            actions.perform()

            if promotion_piece:
                if my_side == 'w':
                    if promotion_piece == 'q':
                        promo_element = driver.find_element(By.CSS_SELECTOR, "div.promotion-piece.wq")
                    elif promotion_piece == 'r':
                        promo_element = driver.find_element(By.CSS_SELECTOR, "div.promotion-piece.wr")
                    elif promotion_piece == 'b':
                        promo_element = driver.find_element(By.CSS_SELECTOR, "div.promotion-piece.wb")
                    elif promotion_piece == 'n':
                        promo_element = driver.find_element(By.CSS_SELECTOR, "div.promotion-piece.wn")
                else:  # my_side == 'b'
                    if promotion_piece == 'q':
                        promo_element = driver.find_element(By.CSS_SELECTOR, "div.promotion-piece.bq")
                    elif promotion_piece == 'r':
                        promo_element = driver.find_element(By.CSS_SELECTOR, "div.promotion-piece.br")
                    elif promotion_piece == 'b':
                        promo_element = driver.find_element(By.CSS_SELECTOR, "div.promotion-piece.bb")
                    elif promotion_piece == 'n':
                        promo_element = driver.find_element(By.CSS_SELECTOR, "div.promotion-piece.bn")

                actions.move_to_element(promo_element)
                actions.click()
                actions.perform()

            print(f"Made move: {move}")

        except Exception as E:
            print(E)
            return

    except Exception as e:
        print(f"Error making move: {e}")

def main():
    try:
        chrome_options = Options()
        chrome_options.add_experimental_option("debuggerAddress", "127.0.0.1:9222")

        driver = webdriver.Chrome(options=chrome_options)
        target_tab_title = "Chess.com"
        found = False

        for handle in driver.window_handles:
            driver.switch_to.window(handle)
            if target_tab_title in driver.title:
                found = True
                print("Connected to Chess.com!")
                break

        if not found:
            print("Chess.com tab not found!")
            return

        last_fen = None
        square_size = 100 / 8

        while True:
            fen, my_side, side_to_move = extract_game_info(driver)
            if fen and fen != last_fen or side_to_move == my_side:
                print(f"FEN: {fen}, My Side: {my_side}, Side to Move: {side_to_move}")
                last_fen = fen

                # If it is our turn
                if side_to_move == my_side:
                    try:
                        board = chess.Board(fen)
                        if board.is_game_over():
                            print("Game Over!")
                            break

                        best_move = get_best_move(board.fen())
                        if best_move:
                            print(best_move)
                            make_move(driver, best_move, square_size, my_side)
                        else:
                            print("Stockfish returned None")
                    except Exception as e:
                        print(f"Error making move: {e}")

            # time.sleep(1)

    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if 'driver' in locals():
            driver.quit()

if __name__ == "__main__":
    main()