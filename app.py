import cohere
from flask import Flask, render_template, request

# Configure Cohere API
COHERE_API_KEY = "jaoP7aCdulo0z8SEWYbtHkDdpgvsy241jss3HzBB"  # Replace with your actual API key
co = cohere.Client(COHERE_API_KEY)

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
        # Using a valid Cohere model (change if needed)
        response = co.generate(
            model="command",  # Change if list_models() shows a different valid model
            prompt=text,
            max_tokens=100
        )
        return response.generations[0].text.strip()
    except Exception as e:
        print("Error:", e)  # Print actual error in the terminal
        return f"Sorry, an error occurred: {str(e)}"

if __name__ == '__main__':
    app.run(debug=True)