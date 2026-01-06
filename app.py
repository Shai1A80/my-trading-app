import streamlit as st
import yfinance as yf
from streamlit_gsheets import GSheetsConnection
import pandas as pd

st.set_page_config(page_title="Cloud Portfolio", layout="wide")
st.title("☁️ תיק השקעות מסונכרן לענן")

# חיבור לגיליון גוגל
try:
    conn = st.connection("gsheets", type=GSheetsConnection)
    df = conn.read(worksheet="Sheet1", ttl="0")
except:
    df = pd.DataFrame(columns=['Ticker', 'Price', 'Quantity'])

tab1, tab2 = st.tabs(["📝 עדכון תיק", "📊 מצב נוכחי"])

with tab1:
    st.subheader("הוספה או עדכון מניה")
    with st.form("stock_form"):
        t = st.text_input("סימול (Ticker):").upper()
        p = st.number_input("מחיר קנייה ($):", min_value=0.01)
        q = st.number_input("כמות מניות:", min_value=1)
        
        if st.form_submit_button("שמור וסנכרן לענן"):
            new_entry = pd.DataFrame([{"Ticker": t, "Price": p, "Quantity": q}])
            if t in df['Ticker'].values:
                df.loc[df['Ticker'] == t, ['Price', 'Quantity']] = [p, q]
                final_df = df
            else:
                final_df = pd.concat([df, new_entry], ignore_index=True)
            
            conn.update(worksheet="Sheet1", data=final_df)
            st.success(f"נשמר בהצלחה!")
            st.rerun()

with tab2:
    if df.empty:
        st.info("התיק ריק.")
    else:
        total_inv = 0
        total_val = 0
        for _, row in df.iterrows():
            s = yf.Ticker(row['Ticker'])
            curr = s.fast_info['last_price']
            inv = row['Price'] * row['Quantity']
            val = curr * row['Quantity']
            total_inv += inv
            total_val += val
            
            with st.expander(f"{row['Ticker']} - פרטים"):
                st.write(f"הושקע: ${inv:,.2f} | שווי: ${val:,.2f}")

        st.divider()
        st.metric("סה''כ מושקע", f"${total_inv:,.2f}")
        profit = total_val - total_inv
        # התיקון לשגיאה:
        neto = profit * 0.75 if profit > 0 else profit
        st.metric("רווח נטו (אחרי מס)", f"${neto:,.2f}")
