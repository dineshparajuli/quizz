from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)
df = pd.read_excel("quiz_questions_numbered.xlsx")

@app.route("/")
def home():
    row = df.sample().iloc[0]
    options = [
        row["Option 1"],
        row["Option 2"],
        row["Option 3"],
        row["Option 4"]
    ]
    correct_index = int(row["CorrectAnswer"]) - 1
    question = {
        "text": row["Question"],
        "options": options,
        "answer": options[correct_index]
    }
    return render_template("question.html", question=question)

@app.route("/check", methods=["POST"])
def check():
    selected = request.form["option"]
    correct = request.form["correct"]
    result = "✅ Correct!" if selected == correct else f"❌ Incorrect! Correct answer: {correct}"
    return render_template("result.html", result=result)

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
