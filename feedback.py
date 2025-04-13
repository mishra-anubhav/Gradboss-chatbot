import openai
import os

# ✅ Moderation: Check if user input violates OpenAI safety policies
def is_allowed_by_moderation(user_input):
    """
    Uses OpenAI's Moderation API to check for content violations.
    Returns True if input is safe, False if flagged.
    """
    try:
        response = openai.Moderation.create(input=user_input)
        results = response["results"][0]
        return not results["flagged"]
    except Exception as e:
        print(f"⚠️ Moderation check failed: {e}")
        return True  # Default to allowing if moderation API fails

# ✅ Feedback: Store up/downvote with optional logging
def record_feedback(question, answer, feedback_type, log_file="feedback_log.txt"):
    """
    Logs user feedback (thumbs up/down) to a local file.
    feedback_type: "up" or "down"
    """
    entry = f"QUESTION: {question}\nANSWER: {answer}\nFEEDBACK: {feedback_type}\n{'-'*40}\n"
    try:
        with open(log_file, "a") as f:
            f.write(entry)
    except Exception as e:
        print(f"⚠️ Failed to record feedback: {e}")


#Explanation

"""
Absolutely — here’s a full breakdown of what’s happening in your feedback.py file and why it's essential for a real-world AI chatbot, especially one like GradBoss that supports students 👇

🛡️ Moderation Check — Why and How?
📘 What It Does:
The function is_allowed_by_moderation(user_input):

Sends the user’s message to OpenAI’s Moderation API

The API checks if the message contains anything that violates safety policies (like hate speech, violence, explicit content, etc.)

If the message is flagged 🚩 → your app refuses to answer

If it's safe ✅ → your chatbot continues processing the question

🔍 Why It Matters:
Risk	What Can Go Wrong
❌ Offensive input	A user might type something inappropriate
⚠️ Model misuse	Someone could trick the bot into talking about unethical or unsafe topics
🔒 Policy compliance	OpenAI requires moderation if you’re building public apps using GPT-3.5
This feature acts as a first line of defense — before even talking to the LLM.

🛠️ How It Works in Code:
python
Copy
Edit
response = openai.Moderation.create(input=user_input)
results = response["results"][0]
return not results["flagged"]
flagged = True → input was unsafe

The function then returns False so your UI can say:

"⚠️ Sorry, I cannot respond to that."

⚠️ If the API fails (maybe no internet), the function returns True by default — so the app won’t break.

👍👎 Feedback Logging — What, Why, and How
📘 What It Does:
The function record_feedback():

Takes the user’s question, the bot’s answer, and a vote ("up" or "down")

Writes that feedback to a file: feedback_log.txt

📈 Why This Is Important:
Benefit	Description
✅ Improve responses	You’ll know which answers are helpful and which need better prompts or retriever tuning
🔄 Continuous improvement	Feedback lets you fine-tune your system over time — even without full RLHF
📊 Future analysis	You can analyze what types of questions get low votes (e.g., vague queries? missing context?)
In short: it closes the loop. You’re not just giving answers — you’re learning from how users respond to them.

🛠️ How It Works in Code:
python
Copy
Edit
entry = f\"QUESTION: {question}\\nANSWER: {answer}\\nFEEDBACK: {feedback_type}\\n{'-'*40}\\n\"
with open(\"feedback_log.txt\", \"a\") as f:
    f.write(entry)
This appends a new block to the file every time a user clicks 👍 or 👎 in the UI.

✅ You can later parse this file for analytics, export to a database, or even retrain/fine-tune the model based on it.

🔐 Real-World Best Practices:
For production, you can replace this with:

✅ A database (e.g., Firebase, MongoDB)

✅ Or send to a webhook that logs to Slack, Notion, or Airtable

This modular record_feedback() function gives you the flexibility to plug in any future system

"""