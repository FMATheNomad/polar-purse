<div align="center">
  <img src="screenshot/Screenshot_Landingpage.png" alt="PolarPurse" width="600" />
  <h1>PolarPurse</h1>
  <p><strong>Kalkulator Alokasi Pendapatan & Tools Keuangan Bisnis</strong></p>
  <p>
    <a href="#fitur">Fitur</a> •
    <a href="#tech">Teknologi</a> •
    <a href="#mulai">Mulai</a> •
    <a href="#api">API</a> •
    <a href="#struktur">Struktur</a>
  </p>
</div>

PolarPurse adalah platform kalkulator keuangan berbasis web yang membantu Anda menghitung persentase pendapatan yang bisa dialokasikan untuk menabung, berinvestasi, atau beramal. Selain itu, tersedia pula berbagai kalkulator bisnis untuk membantu analisis keuangan usaha Anda.

[![Flask](https://img.shields.io/badge/backend-Flask-000?logo=flask)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/frontend-Tailwind_CSS-38bdf8?logo=tailwindcss)](https://tailwindcss.com/)
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)

---

<h2 id="fitur">Fitur</h2>

### Kalkulator Personal
- **Alokasi Pendapatan** — Hitung persentase pendapatan harian/bulanan/tahunan untuk tabungan, investasi, atau amal

### Kalkulator Bisnis
- **Keuangan Bisnis** — Hitung keuntungan bulanan usaha
- **Break Even Point (BEP)** — Hitung titik impas bisnis
- **Laba Rugi** — Hitung laba/rugi bisnis dengan indikator visual
- **Investasi** — Proyeksikan nilai investasi di masa depan dengan bunga majemuk
- **Pajak Bisnis** — Hitung pajak penghasilan berdasarkan tarif progresif

### Keamanan
Semua perhitungan dilakukan di **server-side** melalui REST API. Kalkulator sederhana menggunakan **safe arithmetic parser** (bukan `eval()`) sehingga aman dari code injection.

---

<h2 id="tech">Teknologi</h2>

| Stack | Teknologi |
|-------|-----------|
| **Backend** | Python 3 + Flask |
| **Frontend** | Tailwind CSS (CDN), Vanilla JS |
| **Templating** | Jinja2 |
| **API** | REST JSON |
| **Icons** | Font Awesome 6 |

---

<h2 id="mulai">Cara Menjalankan</h2>

**Prasyarat:** Python 3.9+

```bash
# Clone
git clone https://github.com/FMATheNomad/polar-purse.git
cd polar-purse

# Buat virtual environment (disarankan)
python -m venv venv

# Aktifkan
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt

# Jalankan
python app.py
```

Buka **http://localhost:5000** di browser.

---

<h2 id="api">API Endpoints</h2>

Semua endpoint menerima `POST` dengan `Content-Type: application/json`.

### Alokasi Pendapatan
```json
POST /api/calculate/alloc-income
{ "income": 5000000, "allocation_type": "saving", "percentage": 20 }
// → { "amount": 1000000, "formatted": "Rp1,000,000.00", "allocation_label": "Menabung/Investasi" }
```

### Break Even Point
```json
POST /api/calculate/bep
{ "fixed_costs": 100000, "variable_costs": 25000 }
// → { "bep": 4.0, "unit": "unit" }
```

### Keuangan Bisnis
```json
POST /api/calculate/financial
{ "income": 10000000, "expenses": 7000000 }
// → { "profit": 3000000, "formatted": "Rp3,000,000.00" }
```

### Investasi
```json
POST /api/calculate/investment
{ "initial": 10000000, "rate": 10, "years": 5 }
// → { "future_value": 16105100, "formatted": "Rp16,105,100.00", "years": 5 }
```

### Laba Rugi
```json
POST /api/calculate/profit-loss
{ "revenue": 100000, "expenses": 80000 }
// → { "result": 20000, "formatted": "Rp20,000.00", "status": "Laba", "is_profit": true }
```

### Pajak Bisnis
```json
POST /api/calculate/tax
{ "revenue": 200000, "expenses": 50000 }
// → { "tax": 15000, "formatted": "Rp15,000.00", "taxable_income": 150000 }
```

### Kalkulator Sederhana (safe eval)
```json
POST /api/calculate/evaluate
{ "expression": "2+3*4" }
// → { "result": 14 }
```

---

<h2 id="struktur">Struktur Direktori</h2>

```
polar-purse/
├── app.py                    # Flask application
├── requirements.txt          # Dependencies
├── templates/
│   ├── base.html             # Layout utama (navbar + footer)
│   ├── index.html            # Landing page
│   ├── alloc-income.html     # Kalkulator alokasi pendapatan
│   └── business/
│       ├── bep.html          # BEP calculator
│       ├── financial.html    # Financial calculator
│       ├── investment.html   # Investment calculator
│       ├── profit-loss.html  # Profit & loss calculator
│       └── tax.html          # Tax calculator
├── static/
│   ├── css/style.css         # Custom styles
│   └── js/
│       ├── main.js           # Navbar, global
│       └── calculators.js    # API helper
├── images/                   # Hero & card images
└── screenshot/               # Screenshots
```

---

<h2 id="lisensi">Lisensi</h2>

MIT © 2024 [FMATheNomad](https://github.com/FMATheNomad) & [ryugenxd](https://github.com/ryugenxd)
