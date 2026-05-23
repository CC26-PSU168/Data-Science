import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
 
# ─────────────────────────── PAGE CONFIG ───────────────────────────
st.set_page_config(
    page_title="Budgetly — Student Finance Dashboard",
    page_icon="💸",
    layout="wide",
    initial_sidebar_state="expanded",
)
 
# ─────────────────────────── THEME CSS ─────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
 
html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', sans-serif !important;
}
 
/* Background */
.stApp { background-color: #0B0F1A; }
section[data-testid="stSidebar"] {
    background: #111827 !important;
    border-right: 1px solid #1f2937;
}
 
/* Hide default header */
header[data-testid="stHeader"] { background: transparent; }
 
/* Metric cards override */
div[data-testid="metric-container"] {
    background: #131929;
    border: 1px solid #1f2937;
    border-radius: 16px;
    padding: 16px 20px;
}
div[data-testid="metric-container"] label {
    color: #94a3b8 !important;
    font-size: 12px !important;
    font-weight: 500 !important;
    letter-spacing: 0.05em;
    text-transform: uppercase;
}
div[data-testid="metric-container"] div[data-testid="stMetricValue"] {
    color: #f1f5f9 !important;
    font-size: 22px !important;
    font-weight: 700 !important;
}
div[data-testid="metric-container"] div[data-testid="stMetricDelta"] {
    font-size: 12px !important;
}
 
/* Tabs */
div[data-testid="stTabs"] button {
    color: #94a3b8 !important;
    font-weight: 500;
    border-radius: 8px 8px 0 0;
}
div[data-testid="stTabs"] button[aria-selected="true"] {
    color: #1D9E75 !important;
    border-bottom: 2px solid #1D9E75 !important;
}
 
/* Selectbox, multiselect */
div[data-testid="stSelectbox"] > div,
div[data-testid="stMultiSelect"] > div {
    background: #1a2035 !important;
    border: 1px solid #2a3550 !important;
    border-radius: 10px;
}
 
/* Dataframe */
div[data-testid="stDataFrame"] {
    border: 1px solid #1f2937;
    border-radius: 12px;
    overflow: hidden;
}
 
/* Divider */
hr { border-color: #1f2937 !important; }
 
/* Scrollbar */
::-webkit-scrollbar { width: 6px; }
::-webkit-scrollbar-track { background: #0B0F1A; }
::-webkit-scrollbar-thumb { background: #1f2937; border-radius: 3px; }
</style>
""", unsafe_allow_html=True)
 
# ─────────────────────────── PLOTLY THEME ──────────────────────────
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="Plus Jakarta Sans", color="#94a3b8", size=12),
    margin=dict(t=30, b=20, l=10, r=10),
)
 
LEGEND_DEFAULT  = dict(bgcolor="rgba(19,25,41,0.8)", bordercolor="#1f2937",
                       borderwidth=1, font=dict(color="#cbd5e1"))
LEGEND_BOTTOM_H = dict(bgcolor="rgba(19,25,41,0.8)", bordercolor="#1f2937",
                       borderwidth=1, font=dict(color="#cbd5e1"),
                       orientation="h", y=-0.15)
LEGEND_TOP_H    = dict(bgcolor="rgba(19,25,41,0.8)", bordercolor="#1f2937",
                       borderwidth=1, font=dict(color="#cbd5e1"),
                       orientation="h", y=1.1, x=0)
 
CAT_COLORS = {
    "Makan & Minum": "#1D9E75",
    "Tagihan":       "#3b82f6",
    "Hiburan":       "#a78bfa",
    "Belanja":       "#f59e0b",
    "Lain-lain":     "#64748b",
    "Gaji":          "#22d3ee",
    "Goals":         "#f472b6",
}
 
ACC_COLORS = {
    "BCA":          "#2563eb",
    "Gopay":        "#1D9E75",
    "OVO":          "#7c3aed",
    "Dana":         "#dc2626",
    "Dompet Tunai": "#d97706",
}
 
MONTH_ORDER = ["January","February","March","April","May","June",
               "July","August","September","October","November","December"]
DAY_ORDER   = ["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"]
 
# ─────────────────────────── LOAD DATA ─────────────────────────────
@st.cache_data
def load_data():
    # Sesuaikan path jika deploy di Streamlit Cloud
    paths = [
        "Dataset/Processed/Data_Final_Combine.csv",
        "data/processed/Data_Final_Combine.csv",
        "Data_Final_Combine.csv",
    ]
    for p in paths:
        try:
            df = pd.read_csv(p)
            df["Date"] = pd.to_datetime(df["Date"])
            df["Year"]  = df["Date"].dt.year
            df["Month_Name"] = pd.Categorical(df["Month_Name"], categories=MONTH_ORDER, ordered=True)
            df["Day_of_Week"] = pd.Categorical(df["Day_of_Week"], categories=DAY_ORDER, ordered=True)
            return df
        except FileNotFoundError:
            continue
    st.error("❌ File Data_Final_Combine.csv tidak ditemukan. Pastikan path sudah benar.")
    st.stop()
 
df_all = load_data()
 
# ─────────────────────────── SIDEBAR ───────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style='text-align:center; padding: 16px 0 24px;'>
        <div style='font-size:28px;'>💸</div>
        <div style='font-size:20px; font-weight:800; color:#f1f5f9; letter-spacing:-0.5px;'>Budgetly</div>
        <div style='font-size:12px; color:#4ade80; margin-top:2px;'>Student Finance Dashboard</div>
    </div>
    """, unsafe_allow_html=True)
 
    st.markdown("**🗓️ Filter Periode**")
    years = sorted(df_all["Year"].unique())
    selected_years = st.multiselect("Tahun", years, default=years, label_visibility="collapsed")
 
    months_avail = sorted(df_all["Month"].unique())
    selected_months = st.multiselect(
        "Bulan", MONTH_ORDER,
        default=MONTH_ORDER,
        label_visibility="collapsed"
    )
 
    st.markdown("---")
    st.markdown("**💳 Filter Akun**")
    akun_options = sorted(df_all["Account_Name"].unique())
    selected_akun = st.multiselect("Akun", akun_options, default=akun_options, label_visibility="collapsed")
 
    st.markdown("---")
    st.markdown("**🏷️ Filter Kategori**")
    kat_expense = ["Makan & Minum", "Tagihan", "Hiburan", "Belanja", "Lain-lain"]
    kat_income  = ["Gaji", "Goals"]
    selected_kat = st.multiselect(
        "Kategori", kat_expense + kat_income,
        default=kat_expense + kat_income,
        label_visibility="collapsed"
    )
 
    st.markdown("---")
    st.caption(f"📊 Dataset: **{len(df_all):,}** transaksi  \n📅 2024 – 2025")
 
# ─────────────────────────── FILTER DATA ───────────────────────────
df = df_all[
    df_all["Year"].isin(selected_years) &
    df_all["Month_Name"].isin(selected_months) &
    df_all["Account_Name"].isin(selected_akun) &
    df_all["Category"].isin(selected_kat)
].copy()
 
df_exp = df[df["Transaction_Type"] == "EXPENSE"]
df_inc = df[df["Transaction_Type"] == "INCOME"]
 
total_exp   = df_exp["Amount"].sum()
total_inc   = df_inc["Amount"].sum()
net_balance = total_inc - total_exp
avg_daily   = df_exp.groupby("Date")["Amount"].sum().mean()
 
# ─────────────────────────── HEADER ────────────────────────────────
st.markdown("""
<div style='padding: 8px 0 24px;'>
    <h1 style='color:#f1f5f9; font-size:26px; font-weight:800; margin:0; letter-spacing:-0.5px;'>
        Finance Overview
    </h1>
    <p style='color:#64748b; font-size:14px; margin: 4px 0 0;'>
        Analisis keuangan mahasiswa · Data periode 2024–2025
    </p>
</div>
""", unsafe_allow_html=True)
 
# ─────────────────────────── KPI CARDS ─────────────────────────────
k1, k2, k3, k4 = st.columns(4)
 
with k1:
    st.metric("💚 Total Pemasukan",
              f"Rp {total_inc:,.0f}".replace(",", "."),
              f"{len(df_inc):,} transaksi")
with k2:
    st.metric("🔴 Total Pengeluaran",
              f"Rp {total_exp:,.0f}".replace(",", "."),
              f"{len(df_exp):,} transaksi")
with k3:
    balance_icon = "✅" if net_balance >= 0 else "⚠️"
    st.metric(f"{balance_icon} Saldo Bersih",
              f"Rp {abs(net_balance):,.0f}".replace(",", "."),
              "Surplus" if net_balance >= 0 else "Defisit",
              delta_color="normal" if net_balance >= 0 else "inverse")
with k4:
    st.metric("📅 Rata-rata Harian",
              f"Rp {avg_daily:,.0f}".replace(",", "."),
              "per hari (pengeluaran)")
 
st.markdown("<br>", unsafe_allow_html=True)
 
# ─────────────────────────── TABS ──────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs([
    "📊  Overview",
    "💸  Pengeluaran",
    "💰  Pemasukan",
    "⚖️  Perbandingan"
])
 
# ══════════════════════════════════════════
# TAB 1 — OVERVIEW
# ══════════════════════════════════════════
with tab1:
    col_l, col_r = st.columns([1.3, 1])
 
    # Tren bulanan (income vs expense)
    with col_l:
        st.markdown("#### 📈 Tren Bulanan")
 
        monthly = df.groupby(["Month_Name", "Transaction_Type"])["Amount"].sum().reset_index()
        monthly["Month_Name"] = pd.Categorical(monthly["Month_Name"], categories=MONTH_ORDER, ordered=True)
        monthly = monthly.sort_values("Month_Name")
 
        fig_trend = go.Figure()
        for ttype, color in [("INCOME","#1D9E75"), ("EXPENSE","#ef4444")]:
            m = monthly[monthly["Transaction_Type"] == ttype]
            fig_trend.add_trace(go.Bar(
                name=ttype,
                x=m["Month_Name"].astype(str),
                y=m["Amount"],
                marker_color=color,
                opacity=0.85,
            ))
 
        fig_trend.update_layout(**PLOTLY_LAYOUT, barmode="group", height=300,
                               legend=LEGEND_TOP_H)
        fig_trend.update_xaxes(gridcolor="#1f2937", tickfont=dict(color="#64748b", size=10))
        fig_trend.update_yaxes(tickformat=".2s", gridcolor="#1f2937", zerolinecolor="#1f2937",
                               tickprefix="Rp ", tickfont=dict(color="#64748b"))
        st.plotly_chart(fig_trend, use_container_width=True)
 
    # Pie chart kategori pengeluaran
    with col_r:
        st.markdown("#### 🏷️ Komposisi Pengeluaran")
 
        cat_sum = df_exp.groupby("Category")["Amount"].sum().reset_index()
        fig_pie = go.Figure(go.Pie(
            labels=cat_sum["Category"],
            values=cat_sum["Amount"],
            hole=0.55,
            marker=dict(colors=[CAT_COLORS.get(c, "#94a3b8") for c in cat_sum["Category"]]),
            textinfo="percent",
            textfont=dict(color="#f1f5f9", size=11),
            hovertemplate="<b>%{label}</b><br>Rp %{value:,.0f}<extra></extra>",
        ))
        fig_pie.update_layout(**PLOTLY_LAYOUT, height=300, legend=LEGEND_DEFAULT,
            annotations=[dict(text="EXPENSE", x=0.5, y=0.5,
                              font=dict(size=13, color="#94a3b8"), showarrow=False)]
        )
        st.plotly_chart(fig_pie, use_container_width=True)
 
    st.markdown("---")
 
    # Heatmap hari vs bulan
    st.markdown("#### 🗓️ Pola Pengeluaran: Hari × Bulan")
    pivot = df_exp.groupby(["Day_of_Week", "Month_Name"])["Amount"].sum().reset_index()
    pivot["Month_Name"] = pd.Categorical(pivot["Month_Name"], categories=MONTH_ORDER, ordered=True)
    pivot["Day_of_Week"] = pd.Categorical(pivot["Day_of_Week"], categories=DAY_ORDER, ordered=True)
    pivot = pivot.sort_values(["Day_of_Week", "Month_Name"])
    heatmap_data = pivot.pivot_table(index="Day_of_Week", columns="Month_Name", values="Amount", aggfunc="sum")
 
    fig_heat = go.Figure(go.Heatmap(
        z=heatmap_data.values,
        x=[str(c) for c in heatmap_data.columns],
        y=[str(i) for i in heatmap_data.index],
        colorscale=[[0, "#0B0F1A"], [0.5, "#134e35"], [1, "#1D9E75"]],
        hovertemplate="<b>%{y} · %{x}</b><br>Rp %{z:,.0f}<extra></extra>",
        showscale=True,
    ))
    fig_heat.update_layout(**PLOTLY_LAYOUT, height=260)
    fig_heat.update_xaxes(tickfont=dict(size=10, color="#64748b"))
    fig_heat.update_yaxes(tickfont=dict(size=10, color="#64748b"))
    st.plotly_chart(fig_heat, use_container_width=True)
 
# ══════════════════════════════════════════
# TAB 2 — PENGELUARAN
# ══════════════════════════════════════════
with tab2:
    c1, c2 = st.columns(2)
 
    # Bar per kategori
    with c1:
        st.markdown("#### 💸 Total per Kategori")
        cat_exp = df_exp.groupby("Category")["Amount"].sum().reset_index().sort_values("Amount", ascending=True)
        fig_bar = go.Figure(go.Bar(
            y=cat_exp["Category"],
            x=cat_exp["Amount"],
            orientation="h",
            marker=dict(
                color=[CAT_COLORS.get(c, "#94a3b8") for c in cat_exp["Category"]],
                line=dict(width=0),
            ),
            text=[f"Rp {v/1e6:.1f}jt" for v in cat_exp["Amount"]],
            textfont=dict(color="#f1f5f9", size=11),
            textposition="outside",
            hovertemplate="<b>%{y}</b><br>Rp %{x:,.0f}<extra></extra>",
        ))
        fig_bar.update_layout(**PLOTLY_LAYOUT, height=320)
        fig_bar.update_xaxes(tickformat=".2s", tickprefix="Rp ", gridcolor="#1f2937",
                             tickfont=dict(color="#64748b"))
        fig_bar.update_yaxes(tickfont=dict(color="#cbd5e1", size=12))
        st.plotly_chart(fig_bar, use_container_width=True)
 
    # Pengeluaran per hari dalam seminggu
    with c2:
        st.markdown("#### 📅 Pengeluaran per Hari")
        day_exp = df_exp.groupby("Day_of_Week")["Amount"].sum().reset_index()
        day_exp["Day_of_Week"] = pd.Categorical(day_exp["Day_of_Week"], categories=DAY_ORDER, ordered=True)
        day_exp = day_exp.sort_values("Day_of_Week")
        day_exp["short"] = day_exp["Day_of_Week"].astype(str).str[:3]
 
        max_day = day_exp["Amount"].idxmax()
        colors  = ["#1D9E75" if i == max_day else "#1f2937" for i in day_exp.index]
 
        fig_day = go.Figure(go.Bar(
            x=day_exp["short"],
            y=day_exp["Amount"],
            marker=dict(color=colors, line=dict(width=0)),
            text=[f"Rp {v/1e6:.1f}jt" for v in day_exp["Amount"]],
            textposition="outside",
            textfont=dict(color="#94a3b8", size=10),
            hovertemplate="<b>%{x}</b><br>Rp %{y:,.0f}<extra></extra>",
        ))
        fig_day.update_layout(**PLOTLY_LAYOUT, height=320)
        fig_day.update_yaxes(tickformat=".2s", tickprefix="Rp ", gridcolor="#1f2937",
                             tickfont=dict(color="#64748b"))
        st.plotly_chart(fig_day, use_container_width=True)
 
    st.markdown("---")
 
    # Tren pengeluaran bulanan per kategori (stacked area)
    st.markdown("#### 📈 Tren Bulanan per Kategori")
    monthly_cat = df_exp.groupby(["Month_Name", "Category"])["Amount"].sum().reset_index()
    monthly_cat["Month_Name"] = pd.Categorical(monthly_cat["Month_Name"], categories=MONTH_ORDER, ordered=True)
    monthly_cat = monthly_cat.sort_values("Month_Name")
 
    fig_area = go.Figure()
    for cat in kat_expense:
        m = monthly_cat[monthly_cat["Category"] == cat]
        fig_area.add_trace(go.Scatter(
            x=m["Month_Name"].astype(str),
            y=m["Amount"],
            name=cat,
            mode="lines",
            stackgroup="one",
            line=dict(width=0.5),
            fillcolor=CAT_COLORS.get(cat, "#94a3b8"),
            hovertemplate=f"<b>{cat}</b><br>%{{x}}: Rp %{{y:,.0f}}<extra></extra>",
        ))
    fig_area.update_layout(**PLOTLY_LAYOUT, height=320, legend=LEGEND_BOTTOM_H)
    fig_area.update_yaxes(tickformat=".2s", tickprefix="Rp ", gridcolor="#1f2937",
                          tickfont=dict(color="#64748b"))
    st.plotly_chart(fig_area, use_container_width=True)
 
    st.markdown("---")
 
    # Penggunaan per metode pembayaran
    st.markdown("#### 💳 Pengeluaran per Akun / Metode Bayar")
    acc_exp = df_exp.groupby("Account_Name")["Amount"].sum().reset_index().sort_values("Amount", ascending=False)
    total_acc = acc_exp["Amount"].sum()
    acc_exp["pct"] = acc_exp["Amount"] / total_acc * 100
 
    fig_acc = go.Figure()
    for _, row in acc_exp.iterrows():
        fig_acc.add_trace(go.Bar(
            name=row["Account_Name"],
            x=[row["Account_Name"]],
            y=[row["Amount"]],
            marker_color=ACC_COLORS.get(row["Account_Name"], "#64748b"),
            text=f"{row['pct']:.1f}%",
            textposition="outside",
            textfont=dict(color="#94a3b8"),
            hovertemplate=f"<b>{row['Account_Name']}</b><br>Rp {row['Amount']:,.0f}<extra></extra>",
        ))
    fig_acc.update_layout(**PLOTLY_LAYOUT, height=300, showlegend=False)
    fig_acc.update_yaxes(tickformat=".2s", tickprefix="Rp ", gridcolor="#1f2937",
                         tickfont=dict(color="#64748b"))
    st.plotly_chart(fig_acc, use_container_width=True)
 
# ══════════════════════════════════════════
# TAB 3 — PEMASUKAN
# ══════════════════════════════════════════
with tab3:
    c1, c2 = st.columns(2)
 
    with c1:
        st.markdown("#### 💰 Komposisi Pemasukan")
        inc_cat = df_inc.groupby("Category")["Amount"].sum().reset_index()
        fig_inc_pie = go.Figure(go.Pie(
            labels=inc_cat["Category"],
            values=inc_cat["Amount"],
            hole=0.55,
            marker=dict(colors=[CAT_COLORS.get(c, "#64748b") for c in inc_cat["Category"]]),
            textinfo="label+percent",
            textfont=dict(color="#f1f5f9", size=12),
            hovertemplate="<b>%{label}</b><br>Rp %{value:,.0f}<extra></extra>",
        ))
        fig_inc_pie.update_layout(**PLOTLY_LAYOUT, height=320, legend=LEGEND_DEFAULT,
            annotations=[dict(text="INCOME", x=0.5, y=0.5,
                              font=dict(size=13, color="#94a3b8"), showarrow=False)]
        )
        st.plotly_chart(fig_inc_pie, use_container_width=True)
 
    with c2:
        st.markdown("#### 📅 Pemasukan per Bulan")
        monthly_inc = df_inc.groupby("Month_Name")["Amount"].sum().reset_index()
        monthly_inc["Month_Name"] = pd.Categorical(monthly_inc["Month_Name"], categories=MONTH_ORDER, ordered=True)
        monthly_inc = monthly_inc.sort_values("Month_Name")
 
        fig_inc_bar = go.Figure(go.Bar(
            x=monthly_inc["Month_Name"].astype(str),
            y=monthly_inc["Amount"],
            marker_color="#1D9E75",
            opacity=0.85,
            text=[f"Rp {v/1e6:.1f}jt" for v in monthly_inc["Amount"]],
            textposition="outside",
            textfont=dict(color="#94a3b8", size=10),
            hovertemplate="<b>%{x}</b><br>Rp %{y:,.0f}<extra></extra>",
        ))
        fig_inc_bar.update_layout(**PLOTLY_LAYOUT, height=320)
        fig_inc_bar.update_yaxes(tickformat=".2s", tickprefix="Rp ", gridcolor="#1f2937",
                                 tickfont=dict(color="#64748b"))
        fig_inc_bar.update_xaxes(tickfont=dict(size=10, color="#64748b"))
        st.plotly_chart(fig_inc_bar, use_container_width=True)
 
    st.markdown("---")
 
    # Tabel ringkasan pemasukan
    st.markdown("#### 📋 Ringkasan Pemasukan per Kategori")
    inc_summary = df_inc.groupby("Category").agg(
        Jumlah_Transaksi=("Amount", "count"),
        Total=("Amount", "sum"),
        Rata_rata=("Amount", "mean"),
        Maksimum=("Amount", "max"),
    ).reset_index()
    inc_summary["Total"]     = inc_summary["Total"].apply(lambda x: f"Rp {x:,.0f}".replace(",","."))
    inc_summary["Rata_rata"] = inc_summary["Rata_rata"].apply(lambda x: f"Rp {x:,.0f}".replace(",","."))
    inc_summary["Maksimum"]  = inc_summary["Maksimum"].apply(lambda x: f"Rp {x:,.0f}".replace(",","."))
    st.dataframe(inc_summary, use_container_width=True, hide_index=True)
 
# ══════════════════════════════════════════
# TAB 4 — PERBANDINGAN
# ══════════════════════════════════════════
with tab4:
    st.markdown("#### ⚖️ Income vs Expense per Bulan")
 
    monthly_comp = df.groupby(["Month_Name","Transaction_Type"])["Amount"].sum().unstack(fill_value=0).reset_index()
    monthly_comp["Month_Name"] = pd.Categorical(monthly_comp["Month_Name"], categories=MONTH_ORDER, ordered=True)
    monthly_comp = monthly_comp.sort_values("Month_Name")
    monthly_comp.columns.name = None
 
    if "INCOME" not in monthly_comp.columns:  monthly_comp["INCOME"]  = 0
    if "EXPENSE" not in monthly_comp.columns: monthly_comp["EXPENSE"] = 0
    monthly_comp["Net"] = monthly_comp["INCOME"] - monthly_comp["EXPENSE"]
 
    fig_comp = go.Figure()
    fig_comp.add_trace(go.Bar(
        name="Pemasukan", x=monthly_comp["Month_Name"].astype(str),
        y=monthly_comp["INCOME"], marker_color="#1D9E75", opacity=0.85,
        hovertemplate="Pemasukan<br>%{x}: Rp %{y:,.0f}<extra></extra>",
    ))
    fig_comp.add_trace(go.Bar(
        name="Pengeluaran", x=monthly_comp["Month_Name"].astype(str),
        y=monthly_comp["EXPENSE"], marker_color="#ef4444", opacity=0.85,
        hovertemplate="Pengeluaran<br>%{x}: Rp %{y:,.0f}<extra></extra>",
    ))
    fig_comp.add_trace(go.Scatter(
        name="Net Balance", x=monthly_comp["Month_Name"].astype(str),
        y=monthly_comp["Net"], mode="lines+markers",
        line=dict(color="#facc15", width=2, dash="dot"),
        marker=dict(size=7, color="#facc15"),
        hovertemplate="Net<br>%{x}: Rp %{y:,.0f}<extra></extra>",
    ))
    fig_comp.update_layout(**PLOTLY_LAYOUT, height=360,
        barmode="group", legend=LEGEND_TOP_H)
    fig_comp.update_yaxes(tickformat=".2s", tickprefix="Rp ", gridcolor="#1f2937",
                          tickfont=dict(color="#64748b"))
    fig_comp.update_xaxes(tickfont=dict(size=10, color="#64748b"))
    st.plotly_chart(fig_comp, use_container_width=True)
 
    st.markdown("---")
 
    # Insight cards
    st.markdown("#### 💡 Key Insights")
    ia, ib, ic = st.columns(3)
 
    top_cat = df_exp.groupby("Category")["Amount"].sum().idxmax()
    top_month = df_exp.groupby("Month_Name")["Amount"].sum().idxmax()
    top_day   = df_exp.groupby("Day_of_Week")["Amount"].sum().idxmax()
 
    with ia:
        st.info(f"🏆 **Kategori terboros**\n\n**{top_cat}** adalah kategori pengeluaran terbesar")
    with ib:
        st.warning(f"📅 **Bulan paling boros**\n\n**{str(top_month)}** mencatat pengeluaran tertinggi")
    with ic:
        st.error(f"📆 **Hari paling boros**\n\n**{str(top_day)}** adalah hari dengan pengeluaran terbesar")
 
    st.markdown("---")
 
    # Tabel ringkasan
    st.markdown("#### 📋 Tabel Perbandingan Bulanan")
    display_comp = monthly_comp[["Month_Name", "INCOME", "EXPENSE", "Net"]].copy()
    display_comp.columns = ["Bulan", "Pemasukan", "Pengeluaran", "Net Balance"]
    for col in ["Pemasukan", "Pengeluaran", "Net Balance"]:
        display_comp[col] = display_comp[col].apply(lambda x: f"Rp {x:,.0f}".replace(",","."))
    st.dataframe(display_comp, use_container_width=True, hide_index=True)
 
# ─────────────────────────── FOOTER ────────────────────────────────
st.markdown("---")
st.markdown("""
<div style='text-align:center; color:#374151; font-size:12px; padding: 12px 0;'>
    💸 <b style='color:#1D9E75;'>Budgetly</b> · Student Personal Finance Dashboard ·
    Capstone Project Data Science 2025
</div>
""", unsafe_allow_html=True)
