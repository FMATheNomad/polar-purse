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

PolarPurse adalah platform kalkulator keuangan berbasis web yang membantu Anda menghitung persentase pendapatan yang bisa dialokasikan untuk menabung, berinvestasi, atau beramal. Dilengkapi berbagai kalkulator bisnis untuk membantu analisis keuangan usaha Anda.

[![Flask](https://img.shields.io/badge/backend-Flask-000?logo=flask)](https://flask.palletsprojects.com/)
[![Tailwind CSS](https://img.shields.io/badge/frontend-Tailwind_CSS-38bdf8?logo=tailwindcss)](https://tailwindcss.com/)
[![Python](https://img.shields.io/badge/python-3.12-blue?logo=python)](https://python.org)
[![Test](https://img.shields.io/badge/tests-12%20passed-green)]()

---

<h2 id="fitur">Fitur</h2>

### Kalkulator Personal
- **Alokasi Pendapatan** — Hitung persentase pendapatan harian/bulanan/tahunan untuk tabungan, investasi, atau amal

### Kalkulator Bisnis
- **Keuangan Bisnis** — Hitung keuntungan bulanan usaha
- **Break Even Point (BEP)** — Hitung titik impas berdasarkan biaya tetap, biaya variabel, dan harga jual
- **Laba Rugi** — Hitung laba/rugi bisnis dengan indikator visual warna
- **Investasi** — Proyeksikan nilai investasi dengan bunga majemuk + **grafik interaktif**
- **Pajak Bisnis** — Hitung pajak penghasilan berdasarkan tarif progresif

### Kenyamanan
- **Dark Mode** — Toggle theme dengan ikon bulan/matahari (tersimpan di localStorage)
- **Responsive** — Mobile-first, hamburger menu, grid adaptif
- **Keyboard Support** — Tekan Enter untuk submit di semua kalkulator
- **Loading State** — Tombol menampilkan spinner + disabled saat memproses
- **Error Handling** — Pesan error jelas di UI + timeout 15 detik

### Keamanan
- Semua perhitungan **server-side** via REST API
- Safe arithmetic parser (bukan `eval()`) — regex whitelist + builtins kosong
- Input validation server & client side
- Custom error pages (404/500)
- Rate limit via `MAX_CONTENT_LENGTH`

---

<h2 id="tech">Teknologi</h2>

| Stack | Teknologi |
|-------|-----------|
| **Backend** | Python 3.12+ / Flask |
| **Frontend** | Tailwind CSS (class-based dark mode), Vanilla JS |
| **Chart** | Chart.js (grafik investasi interaktif) |
| **Templating** | Jinja2 |
| **API** | REST JSON (`/api/v1/`) |
| **Icons** | Font Awesome 6 |
| **Infrastructure** | Docker, Gunicorn, dotenv |
| **Testing** | pytest (12 test cases) |

---

<h2 id="mulai">Cara Menjalankan</h2>

**Prasyarat:** Python 3.9+

```bash
# Clone
git clone https://github.com/FMATheNomad/polar-purse.git
cd polar-purse

# Buat virtual environment
python -m venv venv
source venv/bin/activate  # Linux/macOS

# Install dependencies
pip install -r requirements.txt

# Jalankan (development)
FLASK_DEBUG=1 FLASK_HOST=127.0.0.1 python app.py

# Atau via gunicorn (production)
gunicorn --bind 0.0.0.0:5000 wsgi:app
```

Buka **http://localhost:5000** di browser.

### Docker

```bash
docker build -t polar-purse .
docker run -p 5000:5000 polar-purse
```

### Testing

```bash
pytest tests/ -v
```

---

<h2 id="api">API Endpoints</h2>

Semua endpoint menerima `POST` dengan `Content-Type: application/json` di bawah prefix `/api/v1/`.

### Alokasi Pendapatan
```json
POST /api/v1/calculate/alloc-income
{ "income": 5000000, "allocation_type": "saving", "percentage": 20 }
// → { "amount": 1000000, "formatted": "Rp1,000,000.00", ... }
```

### Break Even Point
```json
POST /api/v1/calculate/bep
{ "fixed_costs": 100000, "variable_costs": 25000, "selling_price": 50000 }
// → { "bep_units": 4.0, "bep_revenue": 200000, "revenue_formatted": "Rp200,000.00", ... }
```

### Keuangan Bisnis
```json
POST /api/v1/calculate/financial
{ "income": 10000000, "expenses": 7000000 }
// → { "profit": 3000000, "formatted": "Rp3,000,000.00" }
```

### Investasi
```json
POST /api/v1/calculate/investment
{ "initial": 10000000, "rate": 10, "years": 5 }
// → { "future_value": 16105100, "formatted": "Rp16,105,100.00", "growth_series": [...], ... }
```

### Laba Rugi
```json
POST /api/v1/calculate/profit-loss
{ "revenue": 100000, "expenses": 80000 }
// → { "result": 20000, "formatted": "Rp20,000.00", "status_label": "Laba", "is_profit": true }
```

### Pajak Bisnis
```json
POST /api/v1/calculate/tax
{ "revenue": 200000, "expenses": 50000 }
// → { "tax": 15000, "formatted": "Rp15,000.00", "taxable_income": 150000, ... }
```

### Kalkulator Sederhana
```json
POST /api/v1/calculate/evaluate
{ "expression": "2+3*4" }
// → { "result": 14 }
```

### Health Check
```
GET /api/v1/health
// → { "status": "ok", "app": "PolarPurse" }
```

---

<h2 id="struktur">Struktur Direktori</h2>

```
polar-purse/
├── app.py                    # Flask application (factory pattern)
├── wsgi.py                   # Gunicorn entry point
├── requirements.txt          # Dependencies
├── Dockerfile                # Container build
├── .env.example              # Environment variables template
├── tests/
│   └── test_api.py           # 12 test cases
├── templates/
│   ├── base.html             # Layout utama (navbar + footer + dark mode)
│   ├── error.html            # Custom 404/500 page
│   ├── index.html            # Landing page (6 fitur icon-based)
│   ├── alloc-income.html     # Kalkulator alokasi pendapatan
│   └── business/
│       ├── bep.html          # BEP calculator (fixed formula)
│       ├── financial.html    # Financial calculator
│       ├── investment.html   # Investment calculator + Chart.js
│       ├── profit-loss.html  # Profit & loss calculator
│       └── tax.html          # Tax calculator
├── static/
│   ├── css/style.css         # Custom styles + dark mode
│   └── js/
│       ├── main.js           # Navbar, dark mode toggle
│       └── calculators.js    # API helper, error handling, loading
├── images/                   # Hero images
└── screenshot/               # Screenshots
```

---

<h2 id="lisensi">Lisensi</h2>

MIT © 2024 [FMATheNomad](https://github.com/FMATheNomad) & [ryugenxd](https://github.com/ryugenxd)
