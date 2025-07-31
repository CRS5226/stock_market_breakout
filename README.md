# Real-Time Multi-Stock Monitor

A Streamlit-based dashboard for monitoring multiple stocks in real time, with configurable technical indicators, breakout logic, and Telegram notifications.

## Project Overview

- **collector.py** collects live stock data from an API and stores it in CSV files.
- **server.py** must be started first; it manages the data collection and breakout logic.
- **Breakout logic** is applied to the CSV data, using thresholds from `config.json`.
- **Telegram notifications** are sent when a breakout is detected.
- **app.py** provides a Streamlit frontend for monitoring stocks and updating thresholds.
- Any threshold changes made in the frontend update `config.json`, which is used by `server.py` for real-time logic.

## How to Run

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Start the server (data collector and breakout logic):**
   ```
   python server.py
   ```

3. **Start the Streamlit dashboard in a new terminal:**
   ```
   streamlit run app.py
   ```

4. **Configure stocks:**
   - Edit `config.json` to add your stock codes and thresholds, or use the Streamlit frontend to update thresholds.

5. **Ensure data files exist:**
   - The collector will create `latest_data_<STOCKCODE>.csv` files for each stock.

## Features

- Live price monitoring for multiple stocks
- Configurable support, resistance, and volume thresholds (via frontend or `config.json`)
- Technical indicators: Bollinger Bands, MACD, ADX, Moving Averages, Inside Bar, Candle patterns
- Real-time breakout and breakdown alerts
- Telegram notifications for breakouts

## File Structure

- `app.py` - Streamlit dashboard (frontend)
- `server.py` - Runs the collector and breakout logic
- `collector.py` - Collects data from the API and writes to CSV
- `indicator.py` - Technical indicator logic
- `telegram_alert.py` - Telegram notification logic
- `config.json` - Stock configuration and thresholds
- `latest_data_*.csv` - Latest stock data files

## Notes

- The app reloads every 5 seconds to update data and alerts.
- Threshold changes in the frontend are saved to `config.json` and reflected in the backend logic.
- Make sure your Telegram bot credentials and stock market api are set up in `.env` or as required.

