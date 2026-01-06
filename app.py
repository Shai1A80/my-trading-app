import streamlit as st
import yfinance as yf

st.set_page_config(page_title="AI Stock Analyzer", layout="wide")
st.title("🚀 מנתח מניות: דוחות, פוטנציאל וחדשות")

ticker = st.text_input("הכנס סימול מניה (למשל: NVDA, PLTR):", "NVDA").upper()

if ticker:
    with st.spinner('מושך נתונים עמוקים...'):
        stock = yf.Ticker(ticker)
        info = stock.info
        
        # --- 1. נתונים פיננסיים ודוחות ---
        st.header(f"📊 נתונים עבור {ticker}")
        col1, col2, col3 = st.columns(3)
        
        price = info.get('currentPrice', 0)
        net_income = info.get('netIncomeToCommon', 0)
        rev_growth = info.get('revenueGrowth', 0) * 100
        
        col1.metric("מחיר נוכחי", f"${price}")
        col2.metric("צמיחה שנתית", f"{rev_growth:.1f}%")
        col3.metric("מצב", "✅ רווחית" if net_income > 0 else "❌ מפסידה")

        # --- 2. ניתוח פוטנציאל ---
        st.subheader("💡 הערכת פוטנציאל")
        if rev_growth > 15:
            st.success("🔥 פוטנציאל צמיחה גבוה לפי הדוחות האחרונים.")
        else:
            st.info("🐢 צמיחה יציבה/מתונה.")

        # --- 3. חדשות (עם מנגנון הגנה) ---
        st.subheader("📰 חדשות אחרונות")
        try:
            news = stock.news
            if news:
                for n in news[:3]:
                    st.write(f"🔹 **{n['title']}** ([קרא עוד]({n['link']}))")
            else:
                st.write("אין חדשות עדכניות כרגע.")
        except:
            st.write("זמנית לא ניתן למשוך חדשות, נסה לרענן בעוד דקה.")
