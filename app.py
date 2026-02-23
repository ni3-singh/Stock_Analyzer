from flask import Flask, render_template, request
from services.stock_service import fetch_stock_data
from services.scoring_service import calculate_score

app = Flask(__name__)

@app.route("/", methods=["GET", "POST"])
def home():

    data = None
    score = None
    rating = None
    error = None

    if request.method == "POST":
        ticker = request.form.get("ticker")
        data = fetch_stock_data(ticker)

        if not data:
            error = "Invalid stock code. Please try something like RELIANCE.NS"
        else:
            score = calculate_score(data)

            if score <= 2:
                rating = "Weak"
            elif score == 3:
                rating = "Average"
            else:
                rating = "Strong"

    return render_template(
        "index.html",
        data=data,
        score=score,
        rating=rating,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)