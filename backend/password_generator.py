import random
import string

class PasswordGenerator:
    """
    Generate secure random passwords
    """
    
    def __init__(self):
        self.lowercase = string.ascii_lowercase
        self.uppercase = string.ascii_uppercase
        self.digits = string.digits
        self.special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
    
    def generate(self, length=16, use_lowercase=True, use_uppercase=True, 
                 use_digits=True, use_special=True, exclude_ambiguous=False):
        """
        Generate a random password based on specified criteria
        """
        if length < 4:
            return {
                'success': False,
                'error': 'Password length must be at least 4 characters'
            }
        
        # Build character pool
        char_pool = ""
        required_chars = []
        
        if use_lowercase:
            chars = self.lowercase
            if exclude_ambiguous:
                chars = chars.replace('l', '').replace('o', '')
            char_pool += chars
            required_chars.append(random.choice(chars))
        
        if use_uppercase:
            chars = self.uppercase
            if exclude_ambiguous:
                chars = chars.replace('I', '').replace('O', '')
            char_pool += chars
            required_chars.append(random.choice(chars))
        
        if use_digits:
            chars = self.digits
            if exclude_ambiguous:
                chars = chars.replace('0', '').replace('1', '')
            char_pool += chars
            required_chars.append(random.choice(chars))
        
        if use_special:
            char_pool += self.special
            required_chars.append(random.choice(self.special))
        
        if not char_pool:
            return {
                'success': False,
                'error': 'At least one character type must be selected'
            }
        
        # Generate password
        remaining_length = length - len(required_chars)
        password_chars = required_chars + [random.choice(char_pool) for _ in range(remaining_length)]
        
        # Shuffle to avoid predictable patterns
        random.shuffle(password_chars)
        password = ''.join(password_chars)
        
        return {
            'success': True,
            'password': password
        }
    
    def generate_passphrase(self, word_count=4, separator='-', capitalize=True, add_number=True):
        """
        Generate a memorable passphrase using random words
        """
        # Common word list (in practice, use a larger dictionary)
        words = [
            'rainbow', 'mountain', 'sunset', 'ocean', 'forest', 'thunder',
            'crystal', 'shadow', 'phoenix', 'dragon', 'wizard', 'castle',
            'knight', 'legend', 'mystic', 'storm', 'silver', 'golden',
            'tiger', 'eagle', 'wolf', 'bear', 'lion', 'hawk',
            'river', 'valley', 'meadow', 'glacier', 'volcano', 'canyon',
            'anchor', 'compass', 'journey', 'voyage', 'atlas', 'cosmos',
            'nebula', 'quantum', 'prism', 'eclipse', 'zenith', 'aurora'
        ]
        
        selected_words = random.sample(words, word_count)
        
        if capitalize:
            selected_words = [word.capitalize() for word in selected_words]
        
        passphrase = separator.join(selected_words)
        
        if add_number:
            passphrase += separator + str(random.randint(100, 999))
        
        return {
            'success': True,
            'passphrase': passphrase
        }