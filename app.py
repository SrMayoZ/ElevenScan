from flask import Flask, request, jsonify, render_template
import requests
import os

app = Flask(__name__)

# Coloca tu clave API aquí, aunque lo recomendable es usar variables de entorno
HIBP_API_KEY = "778d847eb3ac4ceca5e30106cabbf8c9"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/check_email', methods=['POST'])
def check_email():
    email = request.form['email']
    headers = {'hibp-api-key': HIBP_API_KEY}

    try:
        response = requests.get(f'https://haveibeenpwned.com/api/v3/breachedaccount/{email}', headers=headers)
        if response.status_code == 200:
            breaches = response.json()
            formatted_breaches = [breach["Name"] for breach in breaches]
            return jsonify({"status": "Breaches found", "data": formatted_breaches})
        elif response.status_code == 404:
            return jsonify({"status": "No breaches found"}), 200
        else:
            return jsonify({"status": "An error occurred"}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
