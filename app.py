# app.py

import streamlit as st
import pandas as pd
import json
import time
from datetime import datetime
from indicator import is_breakout

CONFIG_FILE = "config.json"

st.set_page_config(page_title="📈 Live Stock Monitor", layout="wide")
st.title("📊 Real-Time Multi-Stock Monitor")


def load_config():
    try:
        with open(CONFIG_FILE, "r") as f:
            return json.load(f)
    except:
        return {"stocks": []}


def save_config(config):
    with open(CONFIG_FILE, "w") as f:
        json.dump(config, f, indent=2)


if "breakout_shown" not in st.session_state:
    st.session_state.breakout_shown = {}
if "toast_shown_time" not in st.session_state:
    st.session_state.toast_shown_time = {}


def load_latest_df(stock_code):
    try:
        df = pd.read_csv(f"latest_data_{stock_code}.csv")
        if len(df) > 0:
            df = df.sort_values("Timestamp")
            return df
        else:
            return None
    except:
        return None


def toast(message, type="info"):
    if type == "success":
        st.success(message)
    elif type == "error":
        st.error(message)
    elif type == "warning":
        st.warning(message)
    else:
        st.info(message)


def render_cards():
    config = load_config()
    stocks = config.get("stocks", [])

    cols = st.columns(3)

    for i, stock in enumerate(stocks):
        code = stock["stock_code"]
        with cols[i % 3].container(border=True):
            df = load_latest_df(code)
            if df is None:
                st.warning(f"⏳ Waiting for {code} data...")
                continue

            st.subheader(code)
            st.metric("Latest Price", f"₹{df['Close'].iloc[-1]:.2f}")
            st.caption(f"Updated: {df['Timestamp'].iloc[-1]}")

            # === Threshold Inputs ===
            new_support = st.number_input(
                f"{code} Support",
                value=stock.get("support", 0),
                step=1,
                key=f"{code}_support",
            )
            new_resistance = st.number_input(
                f"{code} Resistance",
                value=stock.get("resistance", 0),
                step=1,
                key=f"{code}_resistance",
            )
            new_volume = st.number_input(
                f"{code} Volume Threshold",
                value=stock.get("volume_threshold", 0),
                step=1000,
                key=f"{code}_volume",
            )

            # === Bollinger Bands ===
            bb = stock.get("bollinger", {})
            bb_period = st.number_input(
                f"{code} Bollinger Period",
                value=bb.get("period", 20),
                step=1,
                key=f"{code}_bb_period",
            )
            bb_std = st.number_input(
                f"{code} Bollinger Std Dev",
                value=float(bb.get("std_dev", 2)),
                step=0.1,
                key=f"{code}_bb_std",
            )

            # === MACD ===
            macd = stock.get("macd", {})
            macd_fast = st.number_input(
                f"{code} MACD Fast",
                value=macd.get("fast_period", 12),
                step=1,
                key=f"{code}_macd_fast",
            )
            macd_slow = st.number_input(
                f"{code} MACD Slow",
                value=macd.get("slow_period", 26),
                step=1,
                key=f"{code}_macd_slow",
            )
            macd_signal = st.number_input(
                f"{code} MACD Signal",
                value=macd.get("signal_period", 9),
                step=1,
                key=f"{code}_macd_signal",
            )

            # === ADX ===
            adx = stock.get("adx", {})
            adx_period = st.number_input(
                f"{code} ADX Period",
                value=float(adx.get("period", 14)),
                step=1.0,
                key=f"{code}_adx_period",
            )
            adx_thresh = st.number_input(
                f"{code} ADX Threshold",
                value=adx.get("threshold", 25),
                step=1,
                key=f"{code}_adx_thresh",
            )

            # === MA ===
            ma = stock.get("moving_averages", {})
            ma_fast = st.number_input(
                f"{code} MA Fast",
                value=ma.get("ma_fast", 9),
                step=1,
                key=f"{code}_ma_fast",
            )
            ma_slow = st.number_input(
                f"{code} MA Slow",
                value=ma.get("ma_slow", 21),
                step=1,
                key=f"{code}_ma_slow",
            )

            # === Inside Bar ===
            ib = stock.get("inside_bar", {})
            ib_lookback = st.number_input(
                f"{code} Inside Bar Lookback",
                value=ib.get("lookback", 1),
                step=1,
                key=f"{code}_ib_lookback",
            )

            # === Candle ===
            candle = stock.get("candle", {})
            candle_body = st.number_input(
                f"{code} Min Candle Body %",
                value=float(candle.get("min_body_percent", 0.7)),
                step=0.1,
                key=f"{code}_candle",
            )

            # === Save if any change ===
            if (
                new_support != stock.get("support")
                or new_resistance != stock.get("resistance")
                or new_volume != stock.get("volume_threshold")
                or bb_period != bb.get("period")
                or bb_std != bb.get("std_dev")
                or macd_fast != macd.get("fast_period")
                or macd_slow != macd.get("slow_period")
                or macd_signal != macd.get("signal_period")
                or adx_period != adx.get("period")
                or adx_thresh != adx.get("threshold")
                or ma_fast != ma.get("ma_fast")
                or ma_slow != ma.get("ma_slow")
                or ib_lookback != ib.get("lookback")
                or candle_body != candle.get("min_body_percent")
            ):
                stock["support"] = new_support
                stock["resistance"] = new_resistance
                stock["volume_threshold"] = new_volume
                stock["bollinger"] = {"period": bb_period, "std_dev": bb_std}
                stock["macd"] = {
                    "fast_period": macd_fast,
                    "slow_period": macd_slow,
                    "signal_period": macd_signal,
                }
                stock["adx"] = {"period": adx_period, "threshold": adx_thresh}
                stock["moving_averages"] = {"ma_fast": ma_fast, "ma_slow": ma_slow}
                stock["inside_bar"] = {"lookback": ib_lookback}
                stock["candle"] = {"min_body_percent": candle_body}
                save_config(config)

            # === Breakout logic ===
            signal, current_price, levels, reason = is_breakout(
                df, new_resistance, new_support, stock
            )

            if code not in st.session_state.breakout_shown:
                st.session_state.breakout_shown[code] = False

            now = time.time()
            if signal == "breakout" and not st.session_state.breakout_shown[code]:
                st.session_state.breakout_shown[code] = True
                st.session_state.toast_shown_time[code] = now
                toast(
                    f"🚀 Breakout Alert: {code} at ₹{current_price:.2f} ↑ {new_resistance}",
                    "warning",
                )

            elif signal == "breakdown" and not st.session_state.breakout_shown[code]:
                st.session_state.breakout_shown[code] = True
                st.session_state.toast_shown_time[code] = now
                toast(
                    f"⚠️ Breakdown Alert: {code} at ₹{current_price:.2f} ↓ {new_support}",
                    "error",
                )

            elif st.session_state.breakout_shown.get(code, False):
                elapsed = now - st.session_state.toast_shown_time.get(code, 0)
                if elapsed > 10:
                    st.session_state.breakout_shown[code] = False


placeholder = st.empty()
while True:
    with placeholder.container():
        render_cards()
    time.sleep(5)
    st.rerun()
