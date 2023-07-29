from flask import Flask, render_template, request
import requests

app = Flask(__name__)

def get_exchange_rate(base_currency, target_currency):
    url = f"https://api.exchangerate.host/convert?from={base_currency}&to={target_currency}"
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        return data["result"]
    else:
        return None

@app.route("/", methods=["GET", "POST"])
def currency_converter():
    if request.method == "POST":
        base_currency = request.form.get("base_currency")
        target_currency = request.form.get("target_currency")
        amount = float(request.form.get("amount"))

        exchange_rate = get_exchange_rate(base_currency, target_currency)

        if exchange_rate is not None:
            converted_amount = amount * exchange_rate
            return render_template("result.html", base_currency=base_currency, target_currency=target_currency,
                                   amount=amount, converted_amount=converted_amount)
        else:
            error_message = "Currency conversion failed. Please check the currency codes and try again."
            return render_template("index.html", error_message=error_message)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)