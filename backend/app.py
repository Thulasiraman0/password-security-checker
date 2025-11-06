from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from pathlib import Path
from password_checker import PasswordChecker
from breach_checker import BreachChecker
from password_generator import PasswordGenerator

# Serve frontend `index.html` (project layout: backend/ and frontend/ at repo root)
# static_folder set to ../frontend so Flask can serve files from the frontend folder
app = Flask(__name__, static_folder=str(Path(__file__).resolve().parents[1] / 'frontend'), static_url_path='')
CORS(app)  # Enable CORS for frontend requests

# Initialize modules
password_checker = PasswordChecker()
breach_checker = BreachChecker()
password_generator = PasswordGenerator()

@app.route('/')
def home():
    """Serve the frontend index.html if present, otherwise return the API home JSON."""
    # frontend index location (project root/frontend/index.html)
    index_path = Path(app.static_folder) / 'index.html'
    if index_path.exists():
        # send index.html from the configured static folder
        return app.send_static_file('index.html')

    # fallback: API home JSON
    return jsonify({
        'message': 'Password Security Checker API',
        'version': '1.0.0',
        'endpoints': {
            'check_strength': '/api/check-strength',
            'check_breach': '/api/check-breach',
            'generate_password': '/api/generate-password',
            'generate_passphrase': '/api/generate-passphrase'
        }
    })

@app.route('/api/check-strength', methods=['POST'])
def check_strength():
    """Check password strength"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        result = password_checker.check_strength(password)
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/check-breach', methods=['POST'])
def check_breach():
    """Check if password has been breached"""
    try:
        data = request.get_json()
        password = data.get('password', '')
        
        result = breach_checker.check_breach(password)
        
        return jsonify({
            'success': True,
            'data': result
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/generate-password', methods=['POST'])
def generate_password():
    """Generate a random password"""
    try:
        data = request.get_json()
        
        length = data.get('length', 16)
        use_lowercase = data.get('lowercase', True)
        use_uppercase = data.get('uppercase', True)
        use_digits = data.get('digits', True)
        use_special = data.get('special', True)
        exclude_ambiguous = data.get('exclude_ambiguous', False)
        
        result = password_generator.generate(
            length=length,
            use_lowercase=use_lowercase,
            use_uppercase=use_uppercase,
            use_digits=use_digits,
            use_special=use_special,
            exclude_ambiguous=exclude_ambiguous
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

@app.route('/api/generate-passphrase', methods=['POST'])
def generate_passphrase():
    """Generate a passphrase"""
    try:
        data = request.get_json()
        
        word_count = data.get('word_count', 4)
        separator = data.get('separator', '-')
        capitalize = data.get('capitalize', True)
        add_number = data.get('add_number', True)
        
        result = password_generator.generate_passphrase(
            word_count=word_count,
            separator=separator,
            capitalize=capitalize,
            add_number=add_number
        )
        
        return jsonify(result)
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 400

if __name__ == '__main__':
    print("🔐 Password Security Checker API")
    print("📍 Server running on http://localhost:5000")
    print("📚 API Documentation: http://localhost:5000/")
    app.run(debug=True, port=5000)