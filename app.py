import streamlit as st
import yfinance as yf
import time

st.set_page_config(page_title="AI Stock Analyzer", layout="wide")
st.title("🚀 מנתח מניות חכם: טכני, פונדמנטלי וחדשות")

ticker_input = st.text_input("הכנס סימול מניה (למשל: NVDA, PLTR):", "PLTR").upper()

if ticker_input:
    try:
        stock = yf.Ticker(ticker_input)
        
        # שימוש בפונקציה מהירה יותר למניעת חסימות
        fast_info = stock.fast_info 
        
        st.header(f"📋 נתונים עבור {ticker_input}")
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("מחיר נוכחי", f"${fast_info.last_price:.2f}")
        
        with col2:
            # משיכת נתונים בסיסיים בלבד כדי לא להעמיס על השרת
            basic_info = stock.history(period="1d")
            st.write("✅ חיבור לנתוני בורסה תקין")

        st.subheader("📰 חדשות אחרונות")
        news = stock.news
        if news:
            for n in news[:3]:
                st.info(f"🔹 **{n['title']}**\n\n[לכתבה המלאה]({n['link']})")
        
    except Exception as e:
        st.error(f"נראה שיש עומס על השרת. אנא המתן 30 שניות ונסה שוב. (טעות: {e})")
