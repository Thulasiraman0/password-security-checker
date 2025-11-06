import hashlib
import requests
import time

class BreachChecker:
    """
    Check if password has been compromised in data breaches
    Uses Have I Been Pwned API with k-anonymity
    """
    
    def __init__(self):
        self.api_url = "https://api.pwnedpasswords.com/range/"
        self.timeout = 5  # seconds
    
    def check_breach(self, password):
        """
        Check if password appears in known data breaches
        Uses k-anonymity model - only sends first 5 chars of hash
        """
        if not password:
            return {
                'checked': False,
                'error': 'No password provided'
            }
        
        try:
            # Generate SHA-1 hash of password
            sha1_hash = hashlib.sha1(password.encode('utf-8')).hexdigest().upper()
            
            # Split hash: first 5 chars (prefix) and rest (suffix)
            hash_prefix = sha1_hash[:5]
            hash_suffix = sha1_hash[5:]
            
            # Query API with prefix only (k-anonymity)
            response = requests.get(
                f"{self.api_url}{hash_prefix}",
                timeout=self.timeout,
                headers={'User-Agent': 'Password-Checker-Educational-Project'}
            )
            
            if response.status_code != 200:
                return {
                    'checked': False,
                    'error': f'API Error: {response.status_code}'
                }
            
            # Parse response
            hashes = response.text.splitlines()
            
            for hash_line in hashes:
                parts = hash_line.split(':')
                if len(parts) != 2:
                    continue
                
                returned_suffix, count = parts
                
                if returned_suffix == hash_suffix:
                    return {
                        'checked': True,
                        'breached': True,
                        'count': int(count),
                        'message': f'⚠️ WARNING: This password has been exposed {int(count):,} times in data breaches!',
                        'severity': self._get_severity(int(count))
                    }
            
            # Password not found in breaches
            return {
                'checked': True,
                'breached': False,
                'count': 0,
                'message': '✓ Good news! This password was not found in known data breaches.',
                'severity': 'safe'
            }
        
        except requests.exceptions.Timeout:
            return {
                'checked': False,
                'error': 'Request timeout. Please try again.'
            }
        except requests.exceptions.ConnectionError:
            return {
                'checked': False,
                'error': 'Connection error. Check your internet connection.'
            }
        except Exception as e:
            return {
                'checked': False,
                'error': f'Unexpected error: {str(e)}'
            }
    
    def _get_severity(self, count):
        """Determine severity based on breach count"""
        if count > 100000:
            return 'critical'
        elif count > 10000:
            return 'high'
        elif count > 1000:
            return 'medium'
        else:
            return 'low'
