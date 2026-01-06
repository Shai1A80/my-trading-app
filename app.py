import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Pro Portfolio Manager", layout="wide")
st.title("💼 ניהול תיק השקעות חכם")

# שימוש ב-Session State כדי לשמור את הנתונים גם כשעוברים טאבים
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}

tab1, tab2, tab3 = st.tabs(["➕ הוספה/עדכון מניות", "📊 סל הקניות שלי", "🏹 צייד הזדמנויות"])

# --- טאב 1: הוספה ועדכון ---
with tab1:
    st.subheader("ניהול רשימת המניות")
    col1, col2, col3 = st.columns(3)
    with col1:
        ticker = st.text_input("סימול מניה (למשל AMZN):").upper()
    with col2:
        buy_price = st.number_input("מחיר קנייה ($):", min_value=0.01)
    with col3:
        quantity = st.number_input("כמות מניות:", min_value=1, step=1)
    
    if st.button("עדכן בתיק"):
        st.session_state.portfolio[ticker] = {"price": buy_price, "qty": quantity}
        st.success(f"המניה {ticker} עודכנה בהצלחה!")

# --- טאב 2: סל הקניות (המצב כרגע) ---
with tab2:
    if not st.session_state.portfolio:
        st.info("התיק ריק. הוסף מניות בטאב הראשון.")
    else:
        total_invested = 0
        total_value = 0
        
        st.subheader("פירוט אחזקות")
        for t, data in st.session_state.portfolio.items():
            stock = yf.Ticker(t)
            curr_price = stock.fast_info['last_price']
            
            invested = data['price'] * data['qty']
            current_val = curr_price * data['qty']
            profit_bruto = current_val - invested
            # חישוב נטו (לפי מס רווחי הון של 25%)
            profit_neto = profit_bruto * 0.75 if profit_bruto > 0 else profit_bruto
            
            total_invested += invested
            total_value += current_val
            
            with st.expander(f"📈 {t} - רווח ברוטו: ${profit_bruto:.2f}"):
                c1, c2, c3 = st.columns(3)
                c1.metric("מושקע", f"${invested:,.2f}")
                c2.metric("שווי נוכחי", f"${current_val:,.2f}")
                c3.metric("רווח נטו (אחרי מס)", f"${profit_neto:.2f}")

        st.divider()
        st.header("💰 סיכום תיק כללי")
        m1, m2, m3, m4 = st.columns(4)
        m1.metric("סה''כ הושקע", f"${total_invested:,.2f}")
        m2.metric("שווי תיק", f"${total_value:,.2f}")
        
        total_profit_bruto = total_value - total_invested
        total_profit_neto = total_profit_bruto * 0.75 if total_profit_bruto > 0 else total_profit_bruto
        
        m3.metric("רווח ברוטו כללי", f"${total_profit_bruto:,.2f}")
        m4.metric("רווח נטו כללי", f"${total_profit_neto:,.2f}")

# --- טאב 3: צייד הזדמנויות ---
with tab3:
    st.subheader("מניות מעניינות לרכישה")
    if st.button("סרוק שוק"):
        for t in ["NVDA", "TSLA", "AAPL", "MSFT", "GOOGL"]:
            s = yf.Ticker(t)
            h = s.history(period="2d")
            ch = ((h['Close'].iloc[-1] / h['Close'].iloc[-2]) - 1) * 100
            if ch > 2:
                st.write(f"🔥 {t} בזינוק של {ch:.2f}%")
