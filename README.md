# Chess Automation Bot

Welcome to the Chess Automation Bot project! This tool helps you analyze chess positions on online platforms like Lichess and Chess.com using the powerful Stockfish engine.

**Important Disclaimer:**

- This bot is for learning and personal analysis only.
- Cheating in online games is wrong and against the rules. Please don't do it.
- Always follow the rules of the websites you use.

## Features

- **HTML Parsing:** Extracts the chessboard, turn, and other game details directly from the website's HTML.
- **Stockfish Analysis:** Uses Stockfish to find the best moves.
- **Move Suggestions:** Shows you the best moves based on Stockfish's analysis.
- **(TODO) Move Automation:** Automatically make the moves on the online chess platform (Currently in development).
- **Lichess Compatibility:** Currently optimized for use on Lichess against the Stockfish bot.
- **Chess.com Compatibility:** Fully functional with chess.com bots.

## Technology Used

- **Python:** The main programming language.
- **Stockfish:** The chess engine that analyzes the positions.
- **Selenium:** Automates web browser actions to get game data.
- **stockfish.py:** A Python library for talking to the Stockfish engine.

## Setup

1.  **Create a Virtual Environment (Recommended):**
    - This keeps your project's tools separate from other Python projects.
    - **Windows:**
      ```bash
      python -m venv venv
      venv\Scripts\activate
      ```
    - **macOS/Linux:**
      ```bash
      python3 -m venv venv
      source venv/bin/activate
      ```
2.  **Install Dependencies:**
    - After activating the virtual environment, install the required packages:
      ```bash
      pip install -r requirements.txt
      ```
    - Download and install Stockfish separately. Make sure it's added to your computer's PATH.
3.  **Configure the Bot:**
    - **Chess.com:**
      - Use your browser's web driver to open a chess.com game page against bots.
      - Start a new game against any bot.
      - Run the python script `python3 src/chess_com.py`
      - Then the bot should start working and even making moves on board automatically.
    - **Lichess (Development):**
      - Use your browser's web driver to open a Lichess game page.
      - Start a new game against Stockfish.
      - Run the python script `python3 src/lichess.py`
      - Then the bot should start working.

## Important Notes

**On lichess**

- For best results, keep the chessboard at its normal size. Resizing might cause errors.
- Always follow the rules of the website you are playing on.
- This project is not responsible for any account gettign banned if used illegally or any other poiiitential lawsuits.

## Chess.com Demo

<p>
<video width="640" height="480" controls>
  <source src="./demo.webm">
  Your browser does not support the video tag.
</video>
</p>

## TODO

- Implement the move automation feature for lichess.

## Contributing

Coming soon!

## License

Chess Automation Bot - Public Source License

1.  **Grant of Access:**

    - The source code for the Chess Automation Bot ("the Software") is made publicly available for learning.
    - You can look at and change the Software for your own personal use.

2.  **Restrictions:**

    - You can't give, sell, or use the Software to make money without asking the person who made it.
    - Don't use this software to break the rules of any website.
    - Don't use this software to cheat.
    - The person who made this software isn't responsible if anything bad happens because you use it.

3.  **Copyright:**

    - The person who made the Software still owns it.
    - This license doesn't mean you own it.

4.  **Future Open Source:**

    - The person who made the Software can change this license later, and maybe make it open source.
    - It's up to them if they want to do that.

5.  **Disclaimer:**

    - The Software is given to you "as is," meaning there are no promises it will work perfectly.
    - The person who made it isn't responsible if you have any problems using it.

6.  **Acceptance:**
    - If you use the Software, it means you agree to these rules.

This license is effective as of the date of publication.
