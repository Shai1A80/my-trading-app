import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import yfinance as yf

st.set_page_config(page_title="ניהול תיק וסורק", layout="wide")
st.title("💼 ניהול תיק וסורק הזדמנויות")

# יצירת החיבור לגיליון
conn = st.connection("gsheets", type=GSheetsConnection)

tab1, tab2, tab3 = st.tabs(["📝 עדכון תיק", "📊 סל הקניות (רווחים)", "🏹 סורק שוק"])

with tab1:
    st.header("הוספת מניה לזיכרון הענן")
    with st.form("add_stock"):
        ticker = st.text_input("סימול (למשל AAPL):").upper()
        price = st.number_input("($) מחיר קנייה:", min_value=0.01)
        quantity = st.number_input("כמות:", min_value=1)
        submitted = st.form_submit_button("שמור וסנכרן")
        
        if submitted:
            try:
                # קריאת הנתונים הקיימים (מוודא שהגיליון לא ריק)
                existing_data = conn.read(worksheet="Sheet1", ttl=0)
                new_row = pd.DataFrame([{"Ticker": ticker, "Price": price, "Quantity": quantity}])
                updated_df = pd.concat([existing_data, new_row], ignore_index=True)
                
                # שמירת הנתונים המעודכנים חזרה לגיליון
                conn.update(worksheet="Sheet1", data=updated_df)
                st.success(f"המניה {ticker} נשמרה בגיליון!")
                st.balloons()
            except Exception as e:
                st.error(f"שגיאה בשמירה: {e}")

with tab2:
    st.header("מצב התיק")
    try:
        df = conn.read(worksheet="Sheet1", ttl=0)
        if not df.empty:
            st.dataframe(df, use_container_width=True)
        else:
            st.info("התיק ריק כרגע.")
    except:
        st.warning("לא ניתן לקרוא נתונים. וודא שהגיליון מוגדר נכון.")

with tab3:
    st.header("סורק פריצות (בזמן אמת)")
    if st.button("הפעל סריקה"):
        stocks = ["NVDA", "TSLA", "AAPL", "AMZN", "MSFT", "GOOGL", "META"]
        for s in stocks:
            try:
                data = yf.Ticker(s).history(period="1d")
                if not data.empty:
                    current_price = data['Close'].iloc[-1]
                    st.write(f"🔥 **{s}**: ${current_price:.2f}")
            except:
                continue
