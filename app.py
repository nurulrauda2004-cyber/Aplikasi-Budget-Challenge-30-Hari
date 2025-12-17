import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date

st.set_page_config(page_title="Budget Challenge 30 Hari", layout="wide")

st.title("🔥 Budget Challenge 30 Hari")
st.caption("Dashboard pengeluaran harian dengan berbagai grafik")

# ===== DATA SESSION =====
if "data" not in st.session_state:
    st.session_state.data = pd.DataFrame(
        columns=["Tanggal", "Keterangan", "Pengeluaran"]
    )

# ===== SIDEBAR INPUT =====
st.sidebar.header("➕ Input Pengeluaran")

tanggal = st.sidebar.date_input("Tanggal", date.today())
keterangan = st.sidebar.text_input("Keterangan")
jumlah = st.sidebar.number_input("Jumlah (Rp)", min_value=0)

if st.sidebar.button("Simpan"):
    new_row = {
        "Tanggal": tanggal,
        "Keterangan": keterangan,
        "Pengeluaran": jumlah
    }
    st.session_state.data = pd.concat(
        [st.session_state.data, pd.DataFrame([new_row])],
        ignore_index=True
    )
    st.sidebar.success("Data tersimpan")

# ===== BUDGET =====
st.sidebar.header("🎯 Budget")
budget_harian = st.sidebar.number_input(
    "Budget per hari (Rp)",
    min_value=0,
    value=50000
)

df = st.session_state.data

# ===== RINGKASAN =====
total_pengeluaran = df["Pengeluaran"].sum() if not df.empty else 0
total_budget = budget_harian * 30
sisa_budget = total_budget - total_pengeluaran

c1, c2, c3 = st.columns(3)
c1.metric("Total Budget", f"Rp {total_budget:,.0f}")
c2.metric("Total Pengeluaran", f"Rp {total_pengeluaran:,.0f}")
c3.metric("Sisa Budget", f"Rp {sisa_budget:,.0f}")

# ===== TABEL =====
st.subheader("📋 Data Pengeluaran")
st.dataframe(df)

# ===== GRAFIK =====
if not df.empty:
    st.subheader("📊 Visualisasi Pengeluaran")

    g1, g2 = st.columns(2)

    # 1. Line Chart
    with g1:
        st.caption("Pengeluaran Harian")
        fig1, ax1 = plt.subplots()
        ax1.plot(df["Tanggal"], df["Pengeluaran"], marker="o")
        ax1.set_xlabel("Tanggal")
        ax1.set_ylabel("Rp")
        st.pyplot(fig1)

    # 2. Bar Chart
    with g2:
        st.caption("Perbandingan Pengeluaran")
        fig2, ax2 = plt.subplots()
        ax2.bar(df["Tanggal"], df["Pengeluaran"])
        ax2.set_xlabel("Tanggal")
        ax2.set_ylabel("Rp")
        st.pyplot(fig2)

    # 3. Pie Chart
    st.caption("Proporsi Pengeluaran")
    fig3, ax3 = plt.subplots()
    ax3.pie(
        df["Pengeluaran"],
        labels=df["Keterangan"],
        autopct="%1.1f%%",
        startangle=90
    )
    ax3.axis("equal")
    st.pyplot(fig3)

    # 4. Grafik Sisa Budget
    st.caption("Sisa Budget Selama Challenge")
    df_sorted = df.sort_values("Tanggal")
    df_sorted["Sisa Budget"] = total_budget - df_sorted["Pengeluaran"].cumsum()

    fig4, ax4 = plt.subplots()
    ax4.plot(df_sorted["Tanggal"], df_sorted["Sisa Budget"], marker="o")
    ax4.set_xlabel("Tanggal")
    ax4.set_ylabel("Rp")
    st.pyplot(fig4)
