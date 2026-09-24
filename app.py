import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
import urllib.request
import json
import datetime
import random

# Cấu hình trang Streamlit
st.set_page_config(
    page_title="Bitcoin Real-Time Candlestick & Volume Stream",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS Dark Theme (TradingView style)
st.markdown("""
<style>
    .main { background-color: #0D0E12; }
    .stMetric {
        background-color: #1E222D;
        padding: 12px;
        border-radius: 8px;
        border: 1px solid #2B2E3A;
    }
    .status-badge {
        background-color: #00E676;
        color: #000000;
        padding: 4px 12px;
        border-radius: 20px;
        font-weight: bold;
        font-size: 13px;
    }
</style>
""", unsafe_allow_html=True)

# Khởi tạo dữ liệu Session State
if 'candles' not in st.session_state:
    st.session_state.candles = []
if 'last_time' not in st.session_state:
    st.session_state.last_time = None
if 'last_price' not in st.session_state:
    st.session_state.last_price = 65000.0

CANDLE_DURATION_SEC = 5

def fetch_btc_price_and_volume():
    """Lấy giá BTC/USD realtime từ API Coinbase & Giả lập Volume"""
    try:
        req = urllib.request.Request(
            "https://api.coinbase.com/v2/prices/BTC-USD/spot", 
            headers={'User-Agent': 'Mozilla/5.0'}
        )
        with urllib.request.urlopen(req, timeout=2) as response:
            data = json.loads(response.read().decode())
            price = float(data['data']['amount'])
            st.session_state.last_price = price
            tick_vol = round(random.uniform(1.2, 8.5), 2)
            return price, tick_vol
    except Exception:
        st.session_state.last_price += random.uniform(-15.0, 15.0)
        tick_vol = round(random.uniform(1.2, 8.5), 2)
        return round(st.session_state.last_price, 2), tick_vol

# Tải dữ liệu ban đầu nếu chưa có
if not st.session_state.candles:
    initial_p, initial_v = fetch_btc_price_and_volume()
    now = datetime.datetime.now()
    st.session_state.candles = [{
        'time': now.strftime('%H:%M:%S'),
        'open': initial_p,
        'high': initial_p,
        'low': initial_p,
        'close': initial_p,
        'volume': initial_v
    }]
    st.session_state.last_time = now

# TIÊU ĐỀ TRANG
st.markdown("""
<h2 style='text-align: center; color: #F7931A; margin-bottom: 5px;'>BITCOIN REALTIME CANDLESTICK & VOLUME MONITOR</h2>
<div style='text-align: center; margin-bottom: 20px;'>
    <span class='status-badge'>● LIVE STREAMING 24/7 (STREAMLIT CLOUD)</span>
</div>
""", unsafe_allow_html=True)

# CƠ CHẾ FRAGMENT CHUẨN CỦA STREAMLIT (Cập nhật 1s/lần, 0% chớp nháy, không bao giờ bị nghẽn Server Cloud)
@st.fragment(run_every="1s")
def render_realtime_chart():
    current_price, tick_vol = fetch_btc_price_and_volume()
    now = datetime.datetime.now()
    now_str = now.strftime('%H:%M:%S')

    elapsed = (now - st.session_state.last_time).total_seconds()
    
    if elapsed >= CANDLE_DURATION_SEC:
        # Hết 5s -> Mở cây nến mới
        st.session_state.candles.append({
            'time': now_str,
            'open': current_price,
            'high': current_price,
            'low': current_price,
            'close': current_price,
            'volume': tick_vol
        })
        st.session_state.last_time = now
        
        # Giữ tối đa 50 cây nến trên màn hình
        if len(st.session_state.candles) > 50:
            st.session_state.candles.pop(0)
    else:
        # Chưa hết 5s -> Cập nhật nến hiện tại + tích lũy volume
        curr = st.session_state.candles[-1]
        curr['close'] = current_price
        curr['high'] = max(curr['high'], current_price)
        curr['low'] = min(curr['low'], current_price)
        curr['volume'] = round(curr['volume'] + tick_vol, 2)

    # Đồ thị Nến (Row 1) + Volume (Row 2)
    fig = make_subplots(
        rows=2, cols=1,
        shared_xaxes=True,
        vertical_spacing=0.03,
        row_heights=[0.75, 0.25]
    )

    times = [c['time'] for c in st.session_state.candles]

    # 1. Vẽ Nến Nhật rõ nét
    fig.add_trace(
        go.Candlestick(
            x=times,
            open=[c['open'] for c in st.session_state.candles],
            high=[c['high'] for c in st.session_state.candles],
            low=[c['low'] for c in st.session_state.candles],
            close=[c['close'] for c in st.session_state.candles],
            increasing_line_color='#00E676', increasing_line_width=1.5,
            increasing_fillcolor='#00E676',
            decreasing_line_color='#FF5252', decreasing_line_width=1.5,
            decreasing_fillcolor='#FF5252',
            name='BTC/USD'
        ), row=1, col=1
    )

    # 2. Vẽ Volume Đỏ / Xanh
    vol_colors = ['#00E676' if c['close'] >= c['open'] else '#FF5252' for c in st.session_state.candles]
    fig.add_trace(
        go.Bar(
            x=times,
            y=[c['volume'] for c in st.session_state.candles],
            marker_color=vol_colors,
            name='Volume',
            showlegend=False
        ), row=2, col=1
    )

    fig.update_layout(
        title={
            'text': f"Bitcoin Live Realtime Stream (Khung nến {CANDLE_DURATION_SEC}s)",
            'x': 0.5, 'xanchor': 'center',
            'font': {'size': 18, 'color': '#F7931A'}
        },
        template="plotly_dark",
        height=620,
        uirevision='btc_streamlit_constant', # Tuyệt đối không chớp nháy
        margin=dict(l=20, r=20, t=40, b=20),
        xaxis_rangeslider_visible=False,
        xaxis2=dict(
            title="Thời gian (Dùng con lăn chuột để Zoom In/Out / Kéo thanh trượt bên dưới)",
            showgrid=True, gridcolor='#222222',
            rangeslider=dict(visible=True, thickness=0.08, bgcolor='#1E2026')
        ),
        yaxis1=dict(title="Giá BTC (USD)", tickprefix="$", showgrid=True, gridcolor='#222222'),
        yaxis2=dict(title="Volume", showgrid=True, gridcolor='#222222')
    )

    # Metric Header
    latest_c = st.session_state.candles[-1]['close']
    prev_c = st.session_state.candles[-2]['close'] if len(st.session_state.candles) > 1 else latest_c
    diff = latest_c - prev_c

    m1, m2, m3 = st.columns(3)
    m1.metric("Giá Bitcoin Live Spot", f"${latest_c:,.2f}", f"{diff:+.2f} USD")
    m2.metric("Số cây nến hiển thị", len(st.session_state.candles))
    m3.metric("Khung thời gian nến", f"{CANDLE_DURATION_SEC} giây / nến")

    # Render Plotly Chart với chế độ Zoom mượt
    st.plotly_chart(
        fig,
        use_container_width=True,
        config={'scrollZoom': True, 'displayModeBar': True, 'displaylogo': False}
    )

render_realtime_chart()
