import streamlit as st
import yfinance as yf

st.set_page_config(page_title="Pro Portfolio", layout="wide")
st.title("💼 ניהול תיק וצייד מניות")

# שמירת הנתונים
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = {}

tab1, tab2, tab3 = st.tabs(["➕ ניהול תיק", "📊 סל הקניות", "🏹 סורק הזדמנויות"])

with tab1:
    st.subheader("הוספת מניה לתיק")
    c1, c2, c3 = st.columns(3)
    with c1: t_input = st.text_input("סימול:").upper()
    with c2: p_input = st.number_input("מחיר קנייה ($):", min_value=0.0)
    with c3: q_input = st.number_input("כמות מניות:", min_value=1)
    
    if st.button("שמור בתיק"):
        st.session_state.portfolio[t_input] = {"price": p_input, "qty": q_input}
        st.success(f"עודכן: {q_input} מניות של {t_input}")

with tab2:
    if not st.session_state.portfolio:
        st.write("התיק ריק")
    else:
        total_inv = 0
        total_curr = 0
        for t, d in st.session_state.portfolio.items():
            s = yf.Ticker(t)
            curr = s.fast_info['last_price']
            inv = d['price'] * d['qty']
            val = curr * d['qty']
            bruto = val - inv
            neto = bruto * 0.75 if bruto > 0 else bruto
            
            total_inv += inv
            total_curr += val
            
            with st.expander(f"Mניה: {t} | רווח ברוטו: ${bruto:.2f}"):
                st.write(f"הושקע: ${inv:,.2f} | שווי נוכחי: ${val:,.2f}")
                st.write(f"**רווח נטו (אחרי מס 25%): ${neto:.2f}**")

        st.divider()
        st.subheader("סיכום כללי")
        st.metric("סה''כ הושקע בתיק", f"${total_inv:,.2f}")
        st.metric("רווח נטו כללי (אחרי מס)", f"${(total_curr - total_inv) * 0.75 if (total_curr - total_inv) > 0 else (total_curr - total_inv):,.2f}")

with tab3:
    st.subheader("סריקה מהירה (Top Growth)")
    if st.button("הפעל סריקה חכמה"):
        # רשימה מצומצמת כדי לא להיחסם
        for ticker in ["NVDA", "AMZN", "PLTR", "TSLA"]:
            with st.spinner(f"בודק את {ticker}..."):
                s = yf.Ticker(ticker)
                # שימוש ב-fast_info שלא חוסם
                change = s.fast_info['year_to_date_return'] * 100 
                price = s.fast_info['last_price']
                st.write(f"🔹 **{ticker}**: מחיר ${price:.2f} (תשואה מתחילת שנה: {change:.1f}%)")
