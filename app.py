import streamlit as st
import yfinance as yf

st.set_page_config(page_title="AI Trading Manager", layout="wide")
st.title("💰 ניהול תיק: מתי למכור?")

tab1, tab2 = st.tabs(["🏹 צייד הזדמנויות", "📋 התיק שלי (ניהול מכירה)"])

with tab1:
    st.subheader("סורק שוק למציאת רכישה")
    watchlist = ["NVDA", "PLTR", "TSLA", "META", "AMZN", "AMD"]
    if st.button("הפעל סריקה"):
        for t in watchlist:
            stock = yf.Ticker(t)
            hist = stock.history(period="2d")
            change = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-2]) - 1) * 100
            if change > 2:
                st.success(f"🔥 הזדמנות ב-{t}: עליה של {change:.2f}%")

with tab2:
    st.subheader("הזן את המניות שקנית")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        my_ticker = st.text_input("סימול המניה שקנית:", "AMZN").upper()
    with col2:
        buy_price = st.number_input("מחיר קנייה ($):", value=238.0)
    with col3:
        target_profit = st.number_input("יעד רווח (%) - מתי תרצה לצאת?", value=10.0)

    if my_ticker:
        stock = yf.Ticker(my_ticker)
        current_price = stock.fast_info['last_price']
        profit_loss = ((current_price / buy_price) - 1) * 100
        
        st.divider()
        st.write(f"### מצב נוכחי עבור {my_ticker}")
        st.metric("רווח/הפסד נוכחי", f"{profit_loss:.2f}%", delta=f"{current_price - buy_price:.2f}$")
        
        # --- מנגנון ההתראות (ה"פוש") ---
        if profit_loss >= target_profit:
            st.balloons()
            st.success(f"🎊 יעד הרווח הושג! מומלץ למכור עכשיו ברווח של {profit_loss:.2f}%")
        elif profit_loss <= -5:
            st.error(f"⚠️ אזהרה: המניה ירדה ב-5%. שקול מכירה (Stop Loss) כדי להגן על הכסף.")
        else:
            st.info("💎 החזק חזק: המניה עדיין לא הגיעה ליעד המכירה.")
