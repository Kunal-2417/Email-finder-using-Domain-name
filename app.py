from flask import Flask, request, jsonify
from flask_cors import CORS 
import requests

app = Flask(__name__)
CORS(app)

# Replace this with your Hunter.io API key
HUNTER_API_KEY = 'YOUR_HUNTER_API_KEY'

# Function to get emails using Hunter.io API
def get_emails_from_hunter(domain):
    print(domain)
    
    url = f"https://api.hunter.io/v2/domain-search?domain={domain}&api_key={HUNTER_API_KEY}"
    
    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get('data') and data['data'].get('emails'):
            emails = [email['value'] for email in data['data']['emails']]
            return emails, None
        else:
            return None, "No emails found for this domain."
    except Exception as e:
        return None, f"Error fetching data from Hunter.io: {str(e)}"

# Route for email enrichment (using Hunter.io)
@app.route("/find-emails", methods=["POST"])
def find_emails():
    domain = request.form.get("domain")

    if not domain:
        return jsonify({"error": "Please provide a valid domain"}), 400

    # Get emails from Hunter.io API
    emails, error = get_emails_from_hunter(domain)
    
    if error:
        return jsonify({"error": error}), 400

    return jsonify(emails)

# Route for the home page
@app.route("/")
def home():
    return "Email Finder Service using Hunter.io API"

if __name__ == "__main__":
    app.run(debug=True)