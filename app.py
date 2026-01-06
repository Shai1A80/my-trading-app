import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="AI Stock Analyzer", layout="wide")

st.title("🚀 מנתח מניות חכם: טכני, פונדמנטלי וחדשות")

# תיבת קלט לחיפוש מניה
ticker_input = st.text_input("הכנס סימול מניה (למשל: NVDA, PLTR, TSLA):", "PLTR").upper()

if ticker_input:
    with st.spinner(f'מנתח את חברת {ticker_input}...'):
        stock = yf.Ticker(ticker_input)
        info = stock.info
        
        # --- חלק 1: נתונים כספיים (דוחות) ---
        st.header("📋 נתונים כספיים ודוחות")
        col1, col2, col3 = st.columns(3)
        
        price = info.get('currentPrice', 0)
        net_income = info.get('netIncomeToCommon', 0)
        profit_margin = info.get('profitMargins', 0) * 100
        
        col1.metric("מחיר נוכחי", f"${price}")
        col2.metric("רווח נקי", f"${net_income:,.0f}" if net_income else "N/A")
        col3.metric("שולי רווח", f"{profit_margin:.2f}%")
        
        if net_income > 0:
            st.success(f"✅ זוהי חברה רווחית. (רווח נקי: ${net_income:,.0f})")
        else:
            st.error("❌ החברה עדיין לא רווחית (שורפת מזומנים).")

        # --- חלק 2: ניתוח אתרים וחדשות (Sentiment) ---
        st.header("📰 חדשות אחרונות וסנטימנט")
        news = stock.news
        if news:
            for n in news[:3]: # מציג את 3 הידיעות האחרונות
                st.info(f"🔹 **{n['title']}**\n\n[לכתבה המלאה]({n['link']})")
        else:
            st.write("לא נמצאו חדשות עדכניות כרגע.")

        # --- חלק 3: על החברה (ביזנס) ---
        st.header("🏢 על העסק")
        st.write(info.get('longBusinessSummary', 'אין פירוט זמין.'))
