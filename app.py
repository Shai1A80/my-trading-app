import streamlit as st
import yfinance as yf

st.set_page_config(page_title="AI Stock Analyzer", layout="wide")
st.title("🚀 מנתח מניות: דוחות ופוטנציאל")

ticker = st.text_input("הכנס סימול מניה (למשל: NVDA, TSLA):", "NVDA").upper()

if ticker:
    try:
        stock = yf.Ticker(ticker)
        
        # משיכת נתונים בסיסיים בצורה בטוחה
        hist = stock.history(period="1d")
        if not hist.empty:
            current_price = hist['Close'].iloc[-1]
            
            st.header(f"📊 נתונים עבור {ticker}")
            st.metric("מחיר נוכחי", f"${current_price:.2f}")

            # ניסיון משיכת נתונים פונדמנטליים
            info = stock.info
            st.subheader("💡 ניתוח פוטנציאל ודוחות")
            
            col1, col2 = st.columns(2)
            with col1:
                income = info.get('netIncomeToCommon', 'N/A')
                st.write(f"**רווח נקי:** {income}")
            with col2:
                growth = info.get('revenueGrowth', 0) * 100
                st.write(f"**צמיחה:** {growth:.1f}%")

            if growth > 15:
                st.success("🔥 פוטנציאל צמיחה גבוה לפי דוחות אחרונים!")
            
            st.subheader("📰 חדשות")
            news = stock.news
            if news:
                for n in news[:2]:
                    st.write(f"🔹 {n['title']}")
        else:
            st.error("לא נמצאו נתונים עבור הסימול הזה.")
            
    except Exception as e:
        st.warning("המערכת מנסה להתחבר לנתונים עמוקים... נסה לרענן בעוד רגע.")
