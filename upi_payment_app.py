
import streamlit as st
import qrcode
from PIL import Image
import io
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="💸 UPI Payment - Ayush Bhardwaj", layout="centered")

st.title("💰 UPI Payment Portal")
st.markdown("**Pay securely using the UPI ID below or scan the QR code.**")

# UPI ID
upi_id = "ayushbhradwaj009-1@okicici"
st.subheader("📌 UPI ID:")
st.code(upi_id, language='text')

# Generate QR Code
upi_url = f"upi://pay?pa={upi_id}&pn=AyushBhardwaj&cu=INR"
qr = qrcode.make(upi_url)
buf = io.BytesIO()
qr.save(buf)
buf.seek(0)
img = Image.open(buf)
st.image(img, caption="Scan this QR to Pay", width=300)

st.markdown("---")
st.subheader("📝 Confirm Your Payment")
name = st.text_input("Enter your name")
amount = st.text_input("Enter amount paid (INR)")

if st.button("✅ I’ve completed the payment"):
    if name and amount:
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_entry = pd.DataFrame([[name, amount, timestamp]], columns=["Name", "Amount (INR)", "Timestamp"])
        file_path = "transactions.csv"
        if os.path.exists(file_path):
            old_data = pd.read_csv(file_path)
            all_data = pd.concat([old_data, new_entry], ignore_index=True)
        else:
            all_data = new_entry
        all_data.to_csv(file_path, index=False)
        st.success("Thank you! Your payment has been recorded.")
    else:
        st.error("Please enter both name and amount.")

st.markdown("---")
st.subheader("📜 Payment History")
file_path = "transactions.csv"
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
    st.dataframe(df)
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("⬇️ Download History as CSV", data=csv, file_name="payment_history.csv", mime="text/csv")
else:
    st.info("No transactions recorded yet.")
