# Weather Bot Documentation

## Description

This Telegram bot provides current weather information and a 3-day weather forecast for a specified city. It uses an external weather API to fetch weather data and stores user interactions in a PostgreSQL database.

## Project Structure

### Dependencies

To run the project, the following libraries are required:
- `python-dotenv` — for loading environment variables.
- `requests` — for making HTTP requests.
- `psycopg2` — for interacting with PostgreSQL database.
- `python-telegram-bot` — for creating the Telegram bot.

### Environment Variables

The project uses environment variables for sensitive data. Create a `.env` file with the following variables:
- `TELEGRAM_TOKEN` — your Telegram bot token.
- `API_URL` — the base URL for the weather API.
- `API_KEY` — the API key for accessing weather data.
- `DB_HOST` — the database host.
- `DB_NAME` — the database name.
- `DB_USER` — the database user.
- `DB_PASSWORD` — the database password.

### Key Functions

1. **Database Connection**  
   The `get_db_connection` function establishes a connection to the PostgreSQL database using the parameters from the environment variables.

2. **Saving Data to Database**  
   The `save_to_db` function saves information about user interactions in the `interactions` table in the database. The following data is stored:
   - `user_id` — the Telegram user ID.
   - `user_message` — the message sent by the user.
   - `api_reply` — the reply from the weather API.

3. **Command Handlers**  
   - `/start` — sends a welcome message to the user.
   - `/help` — sends a list of available commands.
   - `/weather <city>` — sends the current weather for the specified city.
   - `/forecast <city>` — sends a 3-day weather forecast for the specified city.

4. **API Requests**  
   The bot makes requests to the weather API to retrieve current weather and forecast data. Responses are processed and sent to the user as text messages.

5. **Error Handling**  
   If there are any issues with the API or database, errors are logged, and the user is notified of the problem.

## Installation

1. Clone the repository:
   ```bash
   git clone <repository_link>
   cd <project_folder>

2. Install dependencies:
   ```bash
   pip install -r requirements.txt

3. Create a .env file in the project root and add the required environment variables.

4. Run the bot:
   ```bash
   python bot.py

## Database Structure
The PostgreSQL database should have the following table interactions:
   ```sql
   CREATE TABLE interactions (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    user_message TEXT NOT NULL,
    api_reply TEXT NOT NULL,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

### Notes

- The bot uses asynchronous request handling with the python-telegram-bot library and async functions.
- The database interaction is handled using the psycopg2 library.
- The weather data is fetched via HTTP requests to the weather API, returning the data in JSON format.

### Example .env File
   ```bash
   TELEGRAM_TOKEN=<your_telegram_token>
   API_URL=<weather_api_url>
   API_KEY=<your_weather_api_key>
   DB_HOST=<database_host>
   DB_NAME=<database_name>
   DB_USER=<database_user>
   DB_PASSWORD=<database_password>

This documentation provides a complete overview of the Weather Bot, including:
- Key dependencies and how to set them up.
- Environment variables configuration.
- Functions of the bot and their roles.
- Database schema for logging interactions.
- Installation and setup instructions.

