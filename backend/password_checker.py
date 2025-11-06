import re
import math
from collections import Counter

class PasswordChecker:
    """
    A comprehensive password strength checker
    """
    
    def __init__(self):
        # Common weak passwords
        self.common_passwords = [
            'password', '123456', '12345678', 'qwerty', 'abc123',
            'monkey', '1234567', 'letmein', 'trustno1', 'dragon',
            'baseball', 'iloveyou', 'master', 'sunshine', 'ashley',
            'bailey', 'passw0rd', 'shadow', '123123', '654321',
            'superman', 'qazwsx', 'michael', 'football'
        ]
        
        # Common patterns
        self.common_patterns = [
            r'123', r'abc', r'qwerty', r'asdf', r'zxcv',
            r'password', r'pass', r'admin', r'user', r'login'
        ]
        
        # Keyboard patterns
        self.keyboard_patterns = [
            'qwertyuiop', 'asdfghjkl', 'zxcvbnm',
            '1qaz2wsx', 'qweasd', 'zaqwsx'
        ]
    
    def check_strength(self, password):
        """
        Main method to check password strength
        Returns a dictionary with score, strength level, and feedback
        """
        if not password:
            return {
                'score': 0,
                'strength': 'Empty',
                'percentage': 0,
                'feedback': ['Please enter a password'],
                'entropy': 0,
                'crack_time': 'Instant'
            }
        
        score = 0
        max_score = 7  # Changed from 10 to actual maximum (3+4)
        feedback = []
        
        # 1. Length Check (0-3 points)
        length_score, length_feedback = self._check_length(password)
        score += length_score
        feedback.extend(length_feedback)
        
        # 2. Character Diversity (0-4 points)
        diversity_score, diversity_feedback = self._check_diversity(password)
        score += diversity_score
        feedback.extend(diversity_feedback)
        
        # 3. Common Password Check (-2 points if found)
        if self._is_common_password(password):
            score -= 2
            feedback.append('❌ This is a commonly used password')
        
        # 4. Pattern Check (-1 point if found)
        if self._has_common_patterns(password):
            score -= 1
            feedback.append('⚠️ Contains common patterns (123, abc, etc.)')
        
        # 5. Keyboard Pattern Check (-1 point if found)
        if self._has_keyboard_patterns(password):
            score -= 1
            feedback.append('⚠️ Contains keyboard patterns (qwerty, asdf, etc.)')
        
        # 6. Repetition Check (-1 point if found)
        if self._has_repetitions(password):
            score -= 1
            feedback.append('⚠️ Contains repetitive characters')
        
        # 7. Sequential Characters (-1 point if found)
        if self._has_sequential_chars(password):
            score -= 1
            feedback.append('⚠️ Contains sequential characters')
        
        # Ensure score is within bounds
        score = max(0, min(score, max_score))
        
        # Calculate entropy
        entropy = self._calculate_entropy(password)
        
        # Estimate crack time
        crack_time = self._estimate_crack_time(entropy)
        
        # Determine strength level
        strength, percentage = self._get_strength_level(score, max_score)
        
        # Add positive feedback if strong
        if score >= 6:
            feedback.insert(0, '✓ Excellent password strength!')
        elif score >= 4:
            feedback.insert(0, '✓ Good password strength')
        
        return {
            'score': score,
            'max_score': max_score,
            'strength': strength,
            'percentage': percentage,
            'feedback': feedback,
            'entropy': round(entropy, 2),
            'crack_time': crack_time,
            'length': len(password)
        }
    
    def _check_length(self, password):
        """Check password length"""
        length = len(password)
        feedback = []
        
        if length < 8:
            feedback.append('❌ Too short (minimum 8 characters)')
            return 0, feedback
        elif length < 12:
            feedback.append('⚠️ Consider using 12+ characters')
            return 1, feedback
        elif length < 16:
            feedback.append('✓ Good length')
            return 2, feedback
        else:
            feedback.append('✓ Excellent length')
            return 3, feedback
    
    def _check_diversity(self, password):
        """Check character type diversity"""
        score = 0
        feedback = []
        
        has_lower = bool(re.search(r'[a-z]', password))
        has_upper = bool(re.search(r'[A-Z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*()_+\-=\[\]{};:\'",.<>?/\\|`~]', password))
        
        if has_lower:
            score += 1
        else:
            feedback.append('➕ Add lowercase letters (a-z)')
        
        if has_upper:
            score += 1
        else:
            feedback.append('➕ Add uppercase letters (A-Z)')
        
        if has_digit:
            score += 1
        else:
            feedback.append('➕ Add numbers (0-9)')
        
        if has_special:
            score += 1
        else:
            feedback.append('➕ Add special characters (!@#$%...)')
        
        return score, feedback
    
    def _is_common_password(self, password):
        """Check if password is in common passwords list"""
        return password.lower() in self.common_passwords
    
    def _has_common_patterns(self, password):
        """Check for common patterns"""
        password_lower = password.lower()
        return any(re.search(pattern, password_lower) for pattern in self.common_patterns)
    
    def _has_keyboard_patterns(self, password):
        """Check for keyboard patterns"""
        password_lower = password.lower()
        return any(pattern in password_lower for pattern in self.keyboard_patterns)
    
    def _has_repetitions(self, password):
        """Check for repetitive characters (e.g., 'aaa', '111')"""
        return bool(re.search(r'(.)\1{2,}', password))
    
    def _has_sequential_chars(self, password):
        """Check for sequential characters (e.g., 'abc', '123')"""
        sequences = ['0123456789', 'abcdefghijklmnopqrstuvwxyz']
        password_lower = password.lower()
        
        for sequence in sequences:
            for i in range(len(sequence) - 2):
                if sequence[i:i+3] in password_lower or sequence[i:i+3][::-1] in password_lower:
                    return True
        return False
    
    def _calculate_entropy(self, password):
        """Calculate password entropy in bits"""
        pool_size = 0
        
        if re.search(r'[a-z]', password):
            pool_size += 26
        if re.search(r'[A-Z]', password):
            pool_size += 26
        if re.search(r'\d', password):
            pool_size += 10
        if re.search(r'[^a-zA-Z0-9]', password):
            pool_size += 32
        
        if pool_size == 0:
            return 0
        
        entropy = len(password) * math.log2(pool_size)
        return entropy
    
    def _estimate_crack_time(self, entropy):
        """Estimate time to crack password"""
        # Assuming 10 billion guesses per second
        guesses_per_second = 10_000_000_000
        
        total_combinations = 2 ** entropy
        seconds = total_combinations / (2 * guesses_per_second)  # Average case
        
        if seconds < 1:
            return "Instant"
        elif seconds < 60:
            return f"{int(seconds)} seconds"
        elif seconds < 3600:
            return f"{int(seconds/60)} minutes"
        elif seconds < 86400:
            return f"{int(seconds/3600)} hours"
        elif seconds < 2592000:
            return f"{int(seconds/86400)} days"
        elif seconds < 31536000:
            return f"{int(seconds/2592000)} months"
        else:
            years = int(seconds/31536000)
            if years > 1000000:
                return "Millions of years"
            return f"{years} years"
    
    def _get_strength_level(self, score, max_score):
        """Determine strength level based on score (4-tier system)"""
        percentage = int((score / max_score) * 100)
        
        if percentage < 30:
            return 'Very Weak', percentage
        elif percentage < 55:
            return 'Weak', percentage
        elif percentage < 80:
            return 'Medium', percentage
        else:
            return 'Strong', percentage  # 80-100% = Strong