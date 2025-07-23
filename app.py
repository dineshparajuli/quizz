from flask import Flask, render_template, request
import pandas as pd

app = Flask(__name__)

try:
    df = pd.read_excel("quiz_questions_numbered.xlsx")
    df.columns = df.columns.str.strip()
    print("Excel columns:", df.columns.tolist())
except Exception as e:
    print("🔥 Failed to load Excel file:", e)

@app.route("/")
def home():
    try:
        row = df.sample().iloc[0]
        print("Sampled row:", row.to_dict())
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
    except Exception as e:
        print("🔥 ERROR loading question:", e)
        return f"Error loading question: {e}"

@app.route("/check", methods=["POST"])
def check():
    try:
        selected = request.form["option"]
        correct = request.form["correct"]
        result = "✅ Correct!" if selected == correct else f"❌ Incorrect! Correct answer: {correct}"
        return render_template("result.html", result=result)
    except Exception as e:
        print("🔥 ERROR in /check:", e)
        return f"Error: {e}"

if __name__ == "__main__":
    app.run(debug=True)
