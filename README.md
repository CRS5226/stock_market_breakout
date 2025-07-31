# Real-Time Multi-Stock Monitor

A Streamlit-based dashboard for monitoring multiple stocks in real time, with configurable technical indicators and breakout alerts.

## Features

- Live price monitoring for multiple stocks
- Configurable support, resistance, and volume thresholds
- Technical indicators: Bollinger Bands, MACD, ADX, Moving Averages, Inside Bar, Candle patterns
- Real-time breakout and breakdown alerts

## Getting Started

1. **Install dependencies:**
   ```
   pip install -r requirements.txt
   ```

2. **Configure stocks:**
   - Edit `config.json` to add your stock codes and thresholds.

3. **Run the app:**
   ```
   streamlit run app.py
   ```

4. **Data files:**
   - Ensure `latest_data_<STOCKCODE>.csv` files are present for each stock.

## File Structure

- `app.py` - Main Streamlit dashboard
- `indicator.py` - Technical indicator logic
- `config.json` - Stock configuration
- `latest_data_*.csv` - Latest stock data files

## Notes

- The app reloads every 5 seconds to update data and alerts.
- You may need to run a separate data collector to keep the CSV files updated.

---

**Author:** Your Name  
**License:** MIT
