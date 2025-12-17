import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Budget Challenge 30 Hari", layout="wide")

st.title("🔥 Budget Challenge 30 Hari")
st.caption("Tantangan mengatur pengeluaran harian")

# ===== SESSION DATA =====
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Tanggal", "Keterangan", "Pengeluaran"]
    )

# ===== SIDEBAR INPUT =====
st.sidebar.header("➕ Input Pengeluaran")

tanggal = st.sidebar.date_input("Tanggal", date.today())
keterangan = st.sidebar.text_input("Keterangan")
jumlah = st.sidebar.number_input("Jumlah Pengeluaran", min_value=0)

if st.sidebar.button("Simpan"):
    new_data = {
        "Tanggal": tanggal,
        "Keterangan": keterangan,
        "Pengeluaran": jumlah,
    }
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_data])],
        ignore_index=True
    )
    st.sidebar.success("Data tersimpan!")

# ===== INPUT BUDGET =====
st.sidebar.header("🎯 Budget Harian")
budget_harian = st.sidebar.number_input(
    "Masukkan budget per hari",
    min_value=0,
    value=50000
)

# ===== DASHBOARD =====
df = st.session_state.data

col1, col2 = st.columns(2)

with col1:
    st.subheader("📋 Catatan Pengeluaran")
    st.dataframe(df)

with col2:
    st.subheader("📊 Ringkasan")

    total_pengeluaran = df["Pengeluaran"].sum()
    sisa_budget = (budget_harian * 30) - total_pengeluaran

    st.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
    st.metric("Sisa Budget 30 Hari", f"Rp {sisa_budget:,.0f}")

    if sisa_budget >= 0:
        st.success("✅ Kamu masih dalam jalur challenge!")
    else:
        st.error("❌ Budget terlampaui!")

# ===== GRAFIK =====
if not df.empty:
    st.subheader("📈 Grafik Pengeluaran")
    fig, ax = plt.subplots()
    ax.plot(df["Tanggal"], df["Pengeluaran"], marker="o")
    ax.set_xlabel("Tanggal")
    ax.set_ylabel("Pengeluaran")
    st.pyplot(fig)
