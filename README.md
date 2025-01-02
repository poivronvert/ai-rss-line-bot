This project is an AI-powered RSS feed bot for Line. It fetches RSS feeds and sends updates to users via Line messages.

## Project Structure

This project is divided into two parts: backend and frontend.

## Features

- Fetches RSS feeds from multiple sources
- Sends updates to Line users
- Customizable feed sources
- AI-powered content filtering

## Installation

### Backend

1. Clone the repository:
    ```bash
    git clone https://github.com/yourusername/ai-rss-line-bot.git
    ```
2. Navigate to the backend directory:
    ```bash
    cd ai-rss-line-bot/backend
    ```
3. Install dependencies using Poetry:
    ```bash
    poetry install
    ```

### Frontend

1. Navigate to the frontend directory:
    ```bash
    cd ai-rss-line-bot/frontend
    ```
2. Install dependencies:
    ```bash
    npm install
    ```

## Usage

### Backend

1. Set up environment variables:
    - Create a `.env` file and add variables following .env.example file.

2. Start the backend server using FastAPI:
    ```bash
    python -m my_journalist
    ```

### Frontend

1. Start the frontend server:
    ```bash
    PORT=3000 npm start
    ```