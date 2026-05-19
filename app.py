import os
import re
import logging
from flask import Flask, render_template, request, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_app():
    app = Flask(__name__)

    env = os.environ.get("FLASK_ENV", "production")
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["MAX_CONTENT_LENGTH"] = 1024 * 1024

    def safe_eval(expression: str) -> float:
        cleaned = re.sub(r"\s+", "", expression)
        if not re.match(r"^[\d+\-*/().]+$", cleaned):
            raise ValueError("Ekspresi mengandung karakter ilegal")
        try:
            return float(eval(cleaned, {"__builtins__": {}}, {}))
        except Exception as e:
            raise ValueError(f"Gagal mengevaluasi ekspresi: {e}")

    def fmt_currency(val: float) -> str:
        if val >= 0:
            return f"Rp{val:,.2f}"
        return f"(Rp{abs(val):,.2f})"

    def safe_float(val, default=0.0):
        try:
            return float(val)
        except (TypeError, ValueError):
            return None

    def json_error(msg, status=400):
        return jsonify({"status": "error", "message": msg}), status

    # --- Template context ---
    @app.context_processor
    def inject_globals():
        return {
            "current_year": 2024,
            "app_name": "PolarPurse",
        }

    # --- Error handlers ---
    @app.errorhandler(404)
    def not_found(e):
        return render_template("error.html", code=404, message="Halaman tidak ditemukan"), 404

    @app.errorhandler(500)
    def server_error(e):
        logger.error(f"Internal error: {e}")
        return render_template("error.html", code=500, message="Terjadi kesalahan server"), 500

    @app.errorhandler(413)
    def too_large(e):
        return json_error("Request terlalu besar", 413)

    # --- Routes ---
    @app.route("/")
    def index():
        return render_template("index.html")

    @app.route("/alloc-income")
    def alloc_income():
        return render_template("alloc-income.html")

    @app.route("/business/bep")
    def business_bep():
        return render_template("business/bep.html")

    @app.route("/business/financial")
    def business_financial():
        return render_template("business/financial.html")

    @app.route("/business/investment")
    def business_investment():
        return render_template("business/investment.html")

    @app.route("/business/profit-loss")
    def business_profit_loss():
        return render_template("business/profit-loss.html")

    @app.route("/business/tax")
    def business_tax():
        return render_template("business/tax.html")

    # --- API ---
    @app.route("/api/v1/health")
    def api_health():
        return jsonify({"status": "ok", "app": "PolarPurse"})

    @app.route("/api/v1/calculate/alloc-income", methods=["POST"])
    def api_alloc_income():
        data = request.get_json(silent=True)
        if not data:
            return json_error("Request body harus JSON")
        income = safe_float(data.get("income"))
        pct = safe_float(data.get("percentage"))
        alloc_type = data.get("allocation_type", "saving")
        if income is None or income < 0:
            return json_error("Pendapatan harus angka positif")
        if pct is None or pct < 0 or pct > 100:
            return json_error("Persentase harus 0-100")
        amount = income * pct / 100
        labels = {"saving": "Menabung/Investasi", "charity": "Beramal"}
        return jsonify({
            "status": "ok",
            "amount": round(amount, 2),
            "formatted": fmt_currency(amount),
            "allocation_label": labels.get(alloc_type, alloc_type),
            "percentage": pct,
        })

    @app.route("/api/v1/calculate/bep", methods=["POST"])
    def api_bep():
        data = request.get_json(silent=True)
        if not data:
            return json_error("Request body harus JSON")
        fixed = safe_float(data.get("fixed_costs"))
        variable = safe_float(data.get("variable_costs"))
        price = safe_float(data.get("selling_price"))
        if fixed is None or fixed <= 0:
            return json_error("Biaya tetap harus angka positif")
        if variable is None or variable < 0:
            return json_error("Biaya variabel harus angka positif")
        if price is None or price <= 0:
            return json_error("Harga jual harus angka positif")
        contribution = price - variable
        if contribution <= 0:
            return json_error("Harga jual harus lebih besar dari biaya variabel")
        bep_units = fixed / contribution
        bep_revenue = bep_units * price
        return jsonify({
            "status": "ok",
            "bep_units": round(bep_units, 2),
            "bep_revenue": round(bep_revenue, 2),
            "revenue_formatted": fmt_currency(bep_revenue),
            "contribution_margin": round(contribution, 2),
        })

    @app.route("/api/v1/calculate/financial", methods=["POST"])
    def api_financial():
        data = request.get_json(silent=True)
        if not data:
            return json_error("Request body harus JSON")
        income = safe_float(data.get("income"))
        expenses = safe_float(data.get("expenses"))
        if income is None or expenses is None:
            return json_error("Pendapatan dan pengeluaran harus angka")
        profit = income - expenses
        return jsonify({
            "status": "ok",
            "profit": round(profit, 2),
            "formatted": fmt_currency(profit),
            "is_profit": profit >= 0,
        })

    @app.route("/api/v1/calculate/investment", methods=["POST"])
    def api_investment():
        data = request.get_json(silent=True)
        if not data:
            return json_error("Request body harus JSON")
        initial = safe_float(data.get("initial"))
        rate = safe_float(data.get("rate"))
        years = safe_float(data.get("years"))
        if initial is None or initial <= 0:
            return json_error("Investasi awal harus angka positif")
        if rate is None or rate < 0:
            return json_error("Tingkat pengembalian harus angka positif")
        if years is None or years <= 0:
            return json_error("Jangka waktu harus angka positif")
        future = initial * (1 + rate / 100) ** years
        series = [round(initial * (1 + rate / 100) ** y, 2) for y in range(int(years) + 1)]
        return jsonify({
            "status": "ok",
            "future_value": round(future, 2),
            "formatted": fmt_currency(future),
            "years": int(years),
            "growth_series": series,
        })

    @app.route("/api/v1/calculate/profit-loss", methods=["POST"])
    def api_profit_loss():
        data = request.get_json(silent=True)
        if not data:
            return json_error("Request body harus JSON")
        revenue = safe_float(data.get("revenue"))
        expenses = safe_float(data.get("expenses"))
        if revenue is None or expenses is None:
            return json_error("Pendapatan dan beban harus angka")
        result = revenue - expenses
        if result > 0:
            status = "Laba"
        elif result < 0:
            status = "Rugi"
        else:
            status = "Impas"
        return jsonify({
            "status": "ok",
            "result": round(result, 2),
            "formatted": fmt_currency(result),
            "status_label": status,
            "is_profit": result >= 0,
        })

    @app.route("/api/v1/calculate/tax", methods=["POST"])
    def api_tax():
        data = request.get_json(silent=True)
        if not data:
            return json_error("Request body harus JSON")
        revenue = safe_float(data.get("revenue"))
        expenses = safe_float(data.get("expenses"))
        if revenue is None or expenses is None:
            return json_error("Pendapatan dan beban harus angka")
        taxable = max(0, revenue - expenses)
        if taxable <= 0:
            tax = 0
        elif taxable <= 50000:
            tax = taxable * 0.05
        elif taxable <= 100000:
            tax = 2500 + (taxable - 50000) * 0.1
        else:
            tax = 7500 + (taxable - 100000) * 0.15
        return jsonify({
            "status": "ok",
            "tax": round(tax, 2),
            "formatted": fmt_currency(tax),
            "taxable_income": round(taxable, 2),
            "taxable_formatted": fmt_currency(taxable),
        })

    @app.route("/api/v1/calculate/evaluate", methods=["POST"])
    def api_evaluate():
        data = request.get_json(silent=True)
        if not data:
            return json_error("Request body harus JSON")
        expression = data.get("expression", "")
        if not expression.strip():
            return json_error("Ekspresi tidak boleh kosong")
        try:
            result = safe_eval(expression)
            return jsonify({"status": "ok", "result": result})
        except ValueError as e:
            return json_error(str(e))

    return app


app = create_app()

if __name__ == "__main__":
    env = os.environ.get("FLASK_ENV", "production")
    debug = os.environ.get("FLASK_DEBUG", "0") == "1"
    host = os.environ.get("FLASK_HOST", "127.0.0.1")
    port = int(os.environ.get("FLASK_PORT", 5000))
    app.run(debug=debug, host=host, port=port)
