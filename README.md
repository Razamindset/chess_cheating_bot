# Chess Automation Bot

Welcome to the Chess Automation Bot project! This tool helps you analyze chess positions on online platforms like Lichess using the powerful Stockfish engine.

**Important Disclaimer:**

- This bot is for learning and personal analysis only.
- Cheating in online games is wrong and against the rules. Please don't do it.
- Always follow the rules of the websites you use.

## Features

- **HTML Parsing:** Extracts the chessboard, turn, and other game details directly from the website's html.
- **Stockfish Analysis:** Uses Stockfish to find the best moves.
- **Move Suggestions:** Shows you the best moves based on Stockfish's analysis.
- **(TODO) Move Automation:** Automatically make the moves on the online chess platform (Currently in development).
- **Lichess Compatibility:** Currently optimized for use on Lichess against the Stockfish bot.

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

    - Use your browsers web driver to open a lichess game page.
    - Start a new game against stockfish.
    - Run the python script `python3 src/lichess.py`
    - Then the bot should start working.

## Important Notes

- For best results, keep the chessboard at its normal size. Resizing might cause errors.
- Be careful when using the bot to control your mouse and keyboard. Test it safely!
- Always follow the rules of the website.

## TODO

- Implement the move automation feature.

## Contributing

- Coming soon!

## License

- Coming soon!
