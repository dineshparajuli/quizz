from flask import Flask, render_template, request
import pandas as pd
import os

app = Flask(__name__)

# Load Excel safely
try:
    df = pd.read_excel("quiz_questions_numbered.xlsx")
    df.columns = df.columns.str.strip()

    df = df.rename(columns={
        "correct option number": "CorrectAnswer"
    })
except Exception as e:
    print("❌ Excel load failed:", e)
    df = pd.DataFrame()

@app.route("/")
def home():
    try:
        row = df.sample().iloc[0]
        options = [row["Option 1"], row["Option 2"], row["Option 3"], row["Option 4"]]
        correct_index = int(row["CorrectAnswer"]) - 1
        question = {
            "text": row["Question"],
            "options": options,
            "answer": options[correct_index]
        }
        return render_template("question.html", question=question)
    except Exception as e:
        return f"Error loading question: {e}"

@app.route("/check", methods=["POST"])
def check():
    selected = request.form["option"]
    correct = request.form["correct"]
    result = "✅ Correct!" if selected == correct else f"❌ Incorrect! Correct answer: {correct}"
    return render_template("result.html", result=result)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host="0.0.0.0", port=port)
