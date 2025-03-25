import google.generativeai as genai
from flask import Flask, render_template, request

# Configure Gemini API
genai.configure(api_key="AIzaSyDB_-LMXmyRaYS6yaFX5agSNwR8QwupsXk")

app = Flask(__name__)

@app.route("/")
def index():
    return render_template('chat.html')

@app.route("/get", methods=["POST"])
def chat():
    msg = request.form.get("msg", "")
    response = get_Chat_response(msg)
    return response

def get_Chat_response(text):
    try:
        model = genai.GenerativeModel("gemini-1.5-pro")
        response = model.generate_content([text])
        return response.text.strip()
    except Exception as e:
        return f"Error:{str(e)}"

if __name__ == '__main__':
   app.run(debug=True)