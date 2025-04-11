import streamlit as st
import qrcode
from PIL import Image
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="CashPocket 💼", page_icon="💰")

# Title and Logo
st.image("cashpocket_logo.png", width=150)
st.title("💼 CashPocket - UPI Payment Tracker")

# UPI details
upi_id = "ayushbhradwaj009-1@okicici"
upi_name = "Ayush Bhardwaj"

# Generate and show QR code
qr_data = f"upi://pay?pa={upi_id}&pn={upi_name}"
qr_img = qrcode.make(qr_data)
qr_img_path = "upi_qr.png"
qr_img.save(qr_img_path)
st.image(qr_img_path, caption="Scan to Pay", width=250)

# Payment verification checkbox
st.subheader("🔐 Step 1: Verify Payment")
payment_verified = st.checkbox("✅ I have received the payment")

# Proceed if payment is verified
if payment_verified:
    st.subheader("💳 Step 2: Enter Payment Details")

    name = st.text_input("Enter payer's name")
    amount = st.number_input("Enter amount (₹)", min_value=1.0, format="%.2f")

    if st.button("✅ Add to Transaction History"):
        # Record transaction
        time_now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        new_data = pd.DataFrame([[name, amount, time_now]],
                                columns=["Name", "Amount (₹)", "Timestamp"])

        # Append to file or create it
        if os.path.exists("transactions.csv"):
            df = pd.read_csv("transactions.csv")
            df = pd.concat([df, new_data], ignore_index=True)
        else:
            df = new_data

        df.to_csv("transactions.csv", index=False)
        st.success("💾 Transaction saved successfully!")

# Show transaction history
if os.path.exists("transactions.csv"):
    st.subheader("📜 Transaction History")
    df = pd.read_csv("transactions.csv")
    st.dataframe(df)

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download History", data=csv,
                       file_name='cashpocket_transactions.csv',
                       mime='text/csv')
