import streamlit as st

# Helper functions
def get_pip_size(pair):
    return 0.0001 if pair not in ["USD/JPY", "XAU/USD"] else 0.01

def get_pip_value(pair):
    if pair == "EUR/USD":
        return 10.0
    elif pair == "USD/JPY":
        return 9.1
    elif pair == "XAU/USD":
        return 1.0
    return 10.0

st.set_page_config(page_title="Forex Multi-Tool", layout="centered")
st.title("📊 Forex Multi-Scenario Calculator")

pair = st.selectbox("Currency Pair", ["EUR/USD", "USD/JPY", "XAU/USD"])
pip_size = get_pip_size(pair)
pip_value_per_lot = get_pip_value(pair)

tab1, tab2, tab3, tab4 = st.tabs(["📐 Scenario 1: Lot Size", "💰 Scenario 2: P&L", "📏 Scenario 3: Pip Value", "🎯 Scenario 4: TP/SL from %"])

# --- SCENARIO 1: Calculate Lot Size ---
with tab1:
    st.header("📐 Scenario 1: Lot Size from Account Risk")
    account = st.number_input("Account Balance ($)", value=10000.0)
    risk_percent = st.slider("Risk %", 0.1, 10.0, value=2.0, step=0.1)
    open_price = st.number_input("Open Price", value=1.1000, format="%.5f")
    stop_price = st.number_input("Stop Loss Price", value=1.0950, format="%.5f")

    sl_pips = abs(open_price - stop_price) / pip_size
    risk_amount = account * (risk_percent / 100)
    lot_size = risk_amount / (sl_pips * pip_value_per_lot)

    st.success(f"✅ Recommended Lot Size: `{lot_size:.2f}` standard lots")
    st.write(f"• Stop Loss: `{sl_pips:.1f} pips`")
    st.write(f"• Risk Amount: `${risk_amount:.2f}`")

# --- SCENARIO 2: Calculate P&L from Lot Size ---
with tab2:
    st.header("💰 Scenario 2: Profit & Loss")
    lot_size = st.number_input("Lot Size", value=1.0)
    open_price = st.number_input("Open Price", value=1.1000, format="%.5f", key="pl_open")
    target_price = st.number_input("Target Price", value=1.1100, format="%.5f", key="pl_target")
    stop_price = st.number_input("Stop Loss Price", value=1.0950, format="%.5f", key="pl_stop")

    tp_pips = abs(target_price - open_price) / pip_size
    sl_pips = abs(open_price - stop_price) / pip_size

    profit = tp_pips * pip_value_per_lot * lot_size
    loss = sl_pips * pip_value_per_lot * lot_size

    st.info(f"📈 Potential Profit: `${profit:.2f}`")
    st.error(f"📉 Potential Loss: `${loss:.2f}`")
    st.write(f"• TP: `{tp_pips:.1f} pips`")
    st.write(f"• SL: `{sl_pips:.1f} pips`")

# --- SCENARIO 3: Calculate Pip Value from Lot Size ---
with tab3:
    st.header("📏 Scenario 3: Pip Value")
    lot_size = st.number_input("Lot Size", value=1.0, key="pip_lot")
    open_price = st.number_input("Open Price", value=1.1000, format="%.5f", key="pip_open")
    target_price = st.number_input("Target Price", value=1.1100, format="%.5f", key="pip_target")
    stop_price = st.number_input("Stop Loss Price", value=1.0950, format="%.5f", key="pip_stop")

    tp_pips = abs(target_price - open_price) / pip_size
    sl_pips = abs(open_price - stop_price) / pip_size

    pip_value = pip_value_per_lot * lot_size

    st.success(f"💡 Pip Value per pip: `${pip_value:.2f}`")
    st.write(f"• TP Pips: `{tp_pips:.1f}` → Profit = `${tp_pips * pip_value:.2f}`")
    st.write(f"• SL Pips: `{sl_pips:.1f}` → Loss = `${sl_pips * pip_value:.2f}`")

# --- SCENARIO 4: TP/SL from % ---
with tab4:
    st.header("🎯 Scenario 4: TP & SL Price from %")
    open_price = st.number_input("Open Price", value=1.1000, format="%.5f", key="rr_open")
    tp_percent = st.slider("Target %", 0.1, 10.0, value=1.0, step=0.1)
    sl_percent = st.slider("Stop Loss %", 0.1, 10.0, value=1.0, step=0.1)
    direction = st.radio("Direction", ["Buy", "Sell"], horizontal=True)

    if direction == "Buy":
        target_price = open_price * (1 + tp_percent / 100)
        stop_price = open_price * (1 - sl_percent / 100)
    else:  # Sell
        target_price = open_price * (1 - tp_percent / 100)
        stop_price = open_price * (1 + sl_percent / 100)

    st.success(f"🎯 Target Price: `{target_price:.5f}`")
    st.error(f"🛑 Stop Loss Price: `{stop_price:.5f}`")
    st.caption("Based on % movement from the open price")

