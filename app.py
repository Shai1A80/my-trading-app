import streamlit as st
import yfinance as yf

st.set_page_config(page_title="AI Stock Hunter", layout="wide")
st.title("🏹 צייד המניות: מה כדאי לקנות עכשיו?")

# רשימת המניות לסריקה (מניות פריצה וצמיחה חזקות)
watchlist = ["NVDA", "PLTR", "TSLA", "META", "AMZN", "AMD", "MSFT", "GOOGL"]

st.subheader("🔎 סורק הזדמנויות בשידור חי")
if st.button("הפעל סריקת שוק"):
    found_opportunity = False
    
    for ticker in watchlist:
        try:
            stock = yf.Ticker(ticker)
            # בדיקת ביצועים ב-24 שעות האחרונות
            hist = stock.history(period="2d")
            if len(hist) < 2: continue
            
            change = ((hist['Close'].iloc[-1] / hist['Close'].iloc[-2]) - 1) * 100
            
            # תנאי ל"הזדמנות": עליה של מעל 2% ביום אחד (סימן לפריצה)
            if change > 2:
                found_opportunity = True
                st.success(f"🔥 **הזדמנות ב-{ticker}**: המניה עולה ב-{change:.2f}%!")
                st.write(f"מחיר נוכחי: ${hist['Close'].iloc[-1]:.2f}")
                st.write(f"[קרא חדשות על {ticker}](https://finance.yahoo.com/quote/{ticker})")
                st.divider()
        except:
            continue
            
    if not found_opportunity:
        st.info("כרגע אין פריצות חריגות ברשימת המעקב. השוק רגוע.")

st.sidebar.header("חיפוש ידני")
manual_ticker = st.sidebar.text_input("או בדוק מניה ספציפית:")
if manual_ticker:
    st.sidebar.write(f"בדוק בנפרד את: {manual_ticker}")
