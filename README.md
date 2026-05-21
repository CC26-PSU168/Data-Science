# 💸 Budgetly — Student Personal Finance Dashboard

> Capstone Project · Data Science 2025

Dashboard interaktif berbasis **Streamlit** untuk menganalisis pola keuangan mahasiswa — mencakup pengeluaran, pemasukan, dan perbandingan bulanan.

---

## 📁 Struktur Repositori

```
budgetly-capstone/
├── Dataset/
│   ├── Processed/
│   │   ├── Data_Final_Combine.csv       ← dataset utama (cleaned)
│   │   ├── df_expense_clean_final.csv
│   │   ├── df_income_clean_final.csv
│   │   ├── data_dictionary.csv
│   │   └── eda_insights.json
│   └── Raw/
│       ├── Data_Finance_6_Bulan.csv
│       ├── dummy_dataset_persona_1.csv
│       └── dummy_data_persona_234.csv
├── Notebook/
│   ├── 01_Capstone_Preprocessing.ipynb
│   ├── 02_Capstone_EDA.ipynb
│   ├── 03_Feature_Engineering.ipynb     ← (coming soon)
│   └── 04_AB_Testing.ipynb              ← (coming soon)
├── dashboard/
│   ├── app.py                           ← Streamlit app
│   └── requirements.txt
├── .gitignore
└── README.md
```

---

## 🚀 Cara Menjalankan Dashboard

### 1. Clone repositori
```bash
git clone https://github.com/username/budgetly-capstone.git
cd budgetly-capstone
```

### 2. Install dependencies
```bash
pip install -r dashboard/requirements.txt
```

### 3. Jalankan Streamlit
```bash
streamlit run dashboard/app.py
```

---

## 📊 Fitur Dashboard

| Tab | Konten |
|-----|--------|
| **Overview** | KPI cards, tren bulanan, komposisi pengeluaran, heatmap hari × bulan |
| **Pengeluaran** | Breakdown per kategori, per hari, tren stacked area, per akun |
| **Pemasukan** | Komposisi Gaji vs Goals, pemasukan bulanan, tabel ringkasan |
| **Perbandingan** | Income vs Expense per bulan, net balance, key insights |

---

## 🗂️ Dataset

- **Sumber**: Data transaksi nyata platform Budgetly + dummy data persona mahasiswa
- **Periode**: Januari 2024 – Desember 2025
- **Total baris**: ~4.981 transaksi
- **Kolom**: `Date`, `Description`, `Amount`, `Transaction_Type`, `Category`, `Account_Name`, `Month`, `Month_Name`, `Day_of_Week`

---

## 👥 Tim

Capstone Project — Data Science Track 2025  
Berkolaborasi dengan tim AI & Fullstack → [budgetly-dbs.vercel.app](https://budgetly-dbs.vercel.app)
