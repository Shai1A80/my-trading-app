import streamlit as st
import yfinance as yf
import requests

st.set_page_config(page_title="Pro Stock Manager", layout="wide")
st.title("💼 ניהול תיק וצייד מניות")

# הגדרת מפתח ה-API שלך באופן קבוע בקוד
AV_API_KEY = "BJYKXIY0BWBSYDDE"

if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}

tab1, tab2, tab3 = st.tabs(["➕ ניהול תיק", "📊 סל הקניות (רווחים)", "🏹 סורק פריצות"])

# --- טאב 1: הוספה ועדכון מניות ---
with tab1:
    st.subheader("הכנס מניה חדשה לסל")
    c1, c2, c3 = st.columns(3)
    with c1: t_in = st.text_input("סימול (למשל AMZN):").upper()
    with c2: p_in = st.number_input("מחיר קנייה ($):", min_value=0.01)
    with c3: q_in = st.number_input("כמות מניות:", min_value=1, step=1)
    
    if st.button("שמור בתיק"):
        if t_in:
            st.session_state.portfolio[t_in] = {"price": p_in, "qty": q_in}
            st.success(f"עודכן: {q_in} מניות של {t_in}")

# --- טאב 2: סל הקניות עם חישובי נטו/ברוטו ---
with tab2:
    if not st.session_state.portfolio:
        st.info("התיק ריק")
    else:
        total_invested = 0
        total_current_value = 0
        
        for ticker, data in st.session_state.portfolio.items():
            stock = yf.Ticker(ticker)
            curr_price = stock.fast_info['last_price']
            
            invested = data['price'] * data['qty']
            current_val = curr_price * data['qty']
            profit_bruto = current_val - invested
            profit_neto = profit_bruto * 0.75 if profit_bruto > 0 else profit_bruto
            
            total_invested += invested
            total_current_value += current_val
            
            with st.expander(f"📦 {ticker} | רווח ברוטו: ${profit_bruto:.2f}"):
                col_a, col_b = st.columns(2)
                col_a.write(f"**הושקע:** ${invested:,.2f} (${data['price']} למניה)")
                col_b.write(f"**רווח נטו (אחרי מס):** ${profit_neto:.2f}")

        st.divider()
        st.header("💰 סיכום תיק כללי")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("סך הכל הושקע", f"${total_invested:,.2f}")
        m2.metric("שווי נוכחי", f"${total_current_value:,.2f}")
        
        total_bruto = total_current_value - total_invested
        total_neto = total_bruto * 0.75 if total_bruto >
