from flask import Flask, render_template, request, jsonify
import re

app = Flask(__name__)


def safe_eval(expression: str) -> float:
    cleaned = re.sub(r"\s+", "", expression)
    if not re.match(r"^[\d+\-*/().]+$", cleaned):
        raise ValueError("Invalid characters in expression")
    allowed = {"+", "-", "*", "/", "(", ")", "."}
    for c in cleaned:
        if c.isdigit() or c in allowed:
            continue
        raise ValueError(f"Unexpected character: {c}")
    try:
        return float(eval(cleaned, {"__builtins__": {}}, {}))
    except Exception as e:
        raise ValueError(f"Evaluation error: {e}")


def fmt_currency(val: float) -> str:
    if val >= 0:
        return f"Rp{val:,.2f}"
    return f"-Rp{abs(val):,.2f}"


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


@app.route("/api/calculate/alloc-income", methods=["POST"])
def api_alloc_income():
    data = request.get_json()
    income = float(data.get("income", 0))
    alloc_type = data.get("allocation_type", "saving")
    percentage = float(data.get("percentage", 0))
    amount = income * percentage / 100
    labels = {"saving": "Menabung/Investasi", "charity": "Beramal"}
    return jsonify({
        "amount": round(amount, 2),
        "formatted": fmt_currency(amount),
        "allocation_label": labels.get(alloc_type, alloc_type),
        "percentage": percentage,
    })


@app.route("/api/calculate/bep", methods=["POST"])
def api_bep():
    data = request.get_json()
    fixed = float(data.get("fixed_costs", 0))
    variable = float(data.get("variable_costs", 0))
    if variable == 0:
        return jsonify({"error": "Biaya variabel tidak boleh 0"}), 400
    bep = fixed / variable
    return jsonify({"bep": round(bep, 2), "unit": "unit"})


@app.route("/api/calculate/financial", methods=["POST"])
def api_financial():
    data = request.get_json()
    income = float(data.get("income", 0))
    expenses = float(data.get("expenses", 0))
    profit = income - expenses
    return jsonify({
        "profit": round(profit, 2),
        "formatted": fmt_currency(profit),
    })


@app.route("/api/calculate/investment", methods=["POST"])
def api_investment():
    data = request.get_json()
    initial = float(data.get("initial", 0))
    rate = float(data.get("rate", 0))
    years = float(data.get("years", 0))
    future = initial * (1 + rate / 100) ** years
    return jsonify({
        "future_value": round(future, 2),
        "formatted": fmt_currency(future),
        "years": int(years),
    })


@app.route("/api/calculate/profit-loss", methods=["POST"])
def api_profit_loss():
    data = request.get_json()
    revenue = float(data.get("revenue", 0))
    expenses = float(data.get("expenses", 0))
    result = revenue - expenses
    if result > 0:
        status = "Laba"
    elif result < 0:
        status = "Rugi"
    else:
        status = "Impas"
    return jsonify({
        "result": round(result, 2),
        "formatted": fmt_currency(result),
        "status": status,
        "is_profit": result >= 0,
    })


@app.route("/api/calculate/tax", methods=["POST"])
def api_tax():
    data = request.get_json()
    revenue = float(data.get("revenue", 0))
    expenses = float(data.get("expenses", 0))
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
        "tax": round(tax, 2),
        "formatted": fmt_currency(tax),
        "taxable_income": round(taxable, 2),
    })


@app.route("/api/calculate/evaluate", methods=["POST"])
def api_evaluate():
    data = request.get_json()
    expression = data.get("expression", "")
    try:
        result = safe_eval(expression)
        return jsonify({"result": result})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
