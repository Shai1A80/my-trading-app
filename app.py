import streamlit as st
import yfinance as yf
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import requests

st.set_page_config(page_title="Investment Dashboard", layout="wide")
st.title("💼 ניהול תיק וסורק הזדמנויות")

# חיבור לגיליון גוגל
conn = st.connection("gsheets", type=GSheetsConnection)

def load_portfolio():
    try:
        return conn.read(worksheet="Sheet1", ttl="0")
    except:
        return pd.DataFrame(columns=['Ticker', 'Price', 'Quantity'])

df = load_portfolio()

tab1, tab2, tab3 = st.tabs(["📝 עדכון תיק", "📊 סל הקניות (רווחים)", "🏹 סורק שוק"])

with tab1:
    st.subheader("הוספת מניה לזיכרון הענן")
    with st.form("add_form"):
        t = st.text_input("סימול:").upper()
        p = st.number_input("מחיר קנייה ($):", min_value=0.01)
        q = st.number_input("כמות:", min_value=1)
        if st.form_submit_button("שמור וסנכרן"):
            new_row = pd.DataFrame([{"Ticker": t, "Price": p, "Quantity": q}])
            # עדכון או הוספה
            if not df.empty and t in df['Ticker'].values:
                df.loc[df['Ticker'] == t, ['Price', 'Quantity']] = [p, q]
                updated_df = df
            else:
                updated_df = pd.concat([df, new_row], ignore_index=True)
            
            conn.update(worksheet="Sheet1", data=updated_df)
            st.success("הנתונים נשמרו בהצלחה!")
            st.rerun()

with tab2:
    if df.empty:
        st.info("התיק ריק.")
    else:
        total_inv = 0
        total_val = 0
        for _, row in df.iterrows():
            stock = yf.Ticker(row['Ticker'])
            curr = stock.fast_info['last_price']
            inv = row['Price'] * row['Quantity']
            val = curr * row['Quantity']
            total_inv += inv
            total_val += val
            
            with st.expander(f"{row['Ticker']} - פירוט"):
                st.write(f"הושקע: ${inv:,.2f} | שווי: ${val:,.2f}")
                profit = val - inv
                st.write(f"רווח נטו (אחרי מס): ${profit * 0.75 if profit > 0 else profit:.2f}")

        st.divider()
        st.metric("סה''כ הושקע בתיק", f"${total_inv:,.2f}")
        total_profit = total_val - total_inv
        st.metric("רווח נטו כללי", f"${total_profit * 0.75 if total_profit > 0 else total_profit:,.2f}")

with tab3:
    st.subheader("סורק פריצות (בזמן אמת)")
    if st.button("הפעל סריקה"):
        for sym in ["NVDA", "AMZN", "TSLA", "PLTR", "META"]:
            url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={sym}&apikey=BJYKXIY0BWBSYDDE'
            data = requests.get(url).json()
            if "Global Quote" in data:
                p = data["Global Quote"]["05. price"]
                c = data["Global Quote"]["10. change percent"]
                st.write(f"🔥 **{sym}**: ${p} ({c})")
