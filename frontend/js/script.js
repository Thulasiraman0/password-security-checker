// ===== CONFIGURATION =====
const API_BASE_URL = 'http://localhost:5000/api';

// ===== STATE =====
let currentPassword = '';

// ===== DOM ELEMENTS =====
const elements = {
    // Tabs
    tabButtons: document.querySelectorAll('.tab-button'),
    tabContents: document.querySelectorAll('.tab-content'),
    
    // Password Checker
    passwordInput: document.getElementById('passwordInput'),
    togglePassword: document.getElementById('togglePassword'),
    checkButton: document.getElementById('checkButton'),
    strengthSection: document.getElementById('strengthSection'),
    strengthBar: document.getElementById('strengthBar'),
    strengthLabel: document.getElementById('strengthLabel'),
    strengthScore: document.getElementById('strengthScore'),
    statLength: document.getElementById('statLength'),
    statEntropy: document.getElementById('statEntropy'),
    statCrackTime: document.getElementById('statCrackTime'),
    feedbackSection: document.getElementById('feedbackSection'),
    feedbackList: document.getElementById('feedbackList'),
    
    // Breach Checker
    breachSection: document.getElementById('breachSection'),
    checkBreachButton: document.getElementById('checkBreachButton'),
    breachResult: document.getElementById('breachResult'),
    
    // Password Generator
    genTypeButtons: document.querySelectorAll('.gen-type-btn'),
    randomGenerator: document.getElementById('randomGenerator'),
    passphraseGenerator: document.getElementById('passphraseGenerator'),
    lengthSlider: document.getElementById('lengthSlider'),
    lengthValue: document.getElementById('lengthValue'),
    useLowercase: document.getElementById('useLowercase'),
    useUppercase: document.getElementById('useUppercase'),
    useDigits: document.getElementById('useDigits'),
    useSpecial: document.getElementById('useSpecial'),
    excludeAmbiguous: document.getElementById('excludeAmbiguous'),
    generateButton: document.getElementById('generateButton'),
    wordCount: document.getElementById('wordCount'),
    wordCountValue: document.getElementById('wordCountValue'),
    capitalizeWords: document.getElementById('capitalizeWords'),
    addNumber: document.getElementById('addNumber'),
    generatePassphraseButton: document.getElementById('generatePassphraseButton'),
    generatedPasswordSection: document.getElementById('generatedPasswordSection'),
    generatedPassword: document.getElementById('generatedPassword'),
    copyButton: document.getElementById('copyButton'),
    copyFeedback: document.getElementById('copyFeedback')
};

// ===== EVENT LISTENERS =====

// Tab Navigation
elements.tabButtons.forEach(button => {
    button.addEventListener('click', () => {
        const tabName = button.getAttribute('data-tab');
        switchTab(tabName);
    });
});

// Toggle Password Visibility
elements.togglePassword.addEventListener('click', () => {
    const type = elements.passwordInput.type === 'password' ? 'text' : 'password';
    elements.passwordInput.type = type;
    elements.togglePassword.textContent = type === 'password' ? '👁️' : '🙈';
});

// Real-time password checking
elements.passwordInput.addEventListener('input', debounce(() => {
    const password = elements.passwordInput.value;
    if (password) {
        checkPasswordStrength(password);
    } else {
        elements.strengthSection.style.display = 'none';
        elements.breachSection.style.display = 'none';
    }
}, 500));

// Check Password Button
elements.checkButton.addEventListener('click', () => {
    const password = elements.passwordInput.value;
    if (password) {
        checkPasswordStrength(password);
    } else {
        alert('Please enter a password to check');
    }
});

// Check Breach Button
elements.checkBreachButton.addEventListener('click', () => {
    const password = elements.passwordInput.value;
    if (password) {
        checkPasswordBreach(password);
    }
});

// Generator Type Toggle
elements.genTypeButtons.forEach(button => {
    button.addEventListener('click', () => {
        const type = button.getAttribute('data-type');
        
        elements.genTypeButtons.forEach(btn => btn.classList.remove('active'));
        button.classList.add('active');
        
        if (type === 'random') {
            elements.randomGenerator.style.display = 'block';
            elements.passphraseGenerator.style.display = 'none';
        } else {
            elements.randomGenerator.style.display = 'none';
            elements.passphraseGenerator.style.display = 'block';
        }
    });
});

// Length Slider
elements.lengthSlider.addEventListener('input', (e) => {
    elements.lengthValue.textContent = e.target.value;
});

// Word Count Slider
elements.wordCount.addEventListener('input', (e) => {
    elements.wordCountValue.textContent = e.target.value;
});

// Generate Password Button
elements.generateButton.addEventListener('click', () => {
    generatePassword();
});

// Generate Passphrase Button
elements.generatePassphraseButton.addEventListener('click', () => {
    generatePassphrase();
});

// Copy Button
elements.copyButton.addEventListener('click', () => {
    copyToClipboard(elements.generatedPassword.value);
});

// ===== FUNCTIONS =====

/**
 * Switch between tabs
 */
function switchTab(tabName) {
    elements.tabButtons.forEach(button => {
        button.classList.remove('active');
        if (button.getAttribute('data-tab') === tabName) {
            button.classList.add('active');
        }
    });
    
    elements.tabContents.forEach(content => {
        content.classList.remove('active');
        if (content.id === tabName) {
            content.classList.add('active');
        }
    });
}

/**
 * Check password strength
 */
async function checkPasswordStrength(password) {
    try {
        const response = await fetch(`${API_BASE_URL}/check-strength`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password })
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayStrengthResults(result.data);
            currentPassword = password;
        } else {
            console.error('Error:', result.error);
        }
    } catch (error) {
        console.error('Network error:', error);
        alert('Error connecting to server. Make sure the backend is running.');
    }
}

/**
 * Display strength results
 */
function displayStrengthResults(data) {
    // Show sections
    elements.strengthSection.style.display = 'block';
    elements.breachSection.style.display = 'block';
    
    // Update strength bar
    const percentage = data.percentage;
    elements.strengthBar.style.width = `${percentage}%`;
    
    // Remove all strength classes
    elements.strengthBar.className = 'strength-bar';
    
    // Add appropriate class based on strength
    const strengthClass = data.strength.toLowerCase().replace(' ', '-');
    elements.strengthBar.classList.add(`strength-${strengthClass}`);
    
    // Update strength label
    elements.strengthLabel.textContent = data.strength;
    elements.strengthLabel.style.color = getStrengthColor(data.strength);
    
    // Update score
    elements.strengthScore.textContent = `${data.score}/${data.max_score} points`;
    
    // Update stats
    elements.statLength.textContent = `${data.length} chars`;
    elements.statEntropy.textContent = `${data.entropy} bits`;
    elements.statCrackTime.textContent = data.crack_time;
    
    // Update feedback
    elements.feedbackList.innerHTML = '';
    data.feedback.forEach(item => {
        const li = document.createElement('li');
        li.textContent = item;
        elements.feedbackList.appendChild(li);
    });
    
    // Clear previous breach results
    elements.breachResult.innerHTML = '';
    elements.breachResult.className = 'breach-result';
}

/**
 * Get color based on strength
 */
function getStrengthColor(strength) {
    const colors = {
        'Very Weak': '#ef4444',
        'Weak': '#f97316',
        'Medium': '#f59e0b',
        'Strong': '#84cc16',
        'Very Strong': '#10b981'
    };
    return colors[strength] || '#64748b';
}

/**
 * Check if password has been breached
 */
async function checkPasswordBreach(password) {
    elements.checkBreachButton.disabled = true;
    elements.checkBreachButton.innerHTML = '<span class="loading"></span> Checking...';
    
    try {
        const response = await fetch(`${API_BASE_URL}/check-breach`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ password })
        });
        
        const result = await response.json();
        
        if (result.success && result.data.checked) {
            displayBreachResults(result.data);
        } else {
            elements.breachResult.textContent = result.data.error || 'Error checking breach status';
            elements.breachResult.className = 'breach-result';
        }
    } catch (error) {
        console.error('Network error:', error);
        elements.breachResult.textContent = 'Error connecting to breach database';
        elements.breachResult.className = 'breach-result';
    } finally {
        elements.checkBreachButton.disabled = false;
        elements.checkBreachButton.textContent = 'Check for Data Breaches';
    }
}

/**
 * Display breach results
 */
function displayBreachResults(data) {
    elements.breachResult.textContent = data.message;
    
    if (data.breached) {
        elements.breachResult.className = 'breach-result danger';
    } else {
        elements.breachResult.className = 'breach-result safe';
    }
}

/**
 * Generate random password
 */
async function generatePassword() {
    const options = {
        length: parseInt(elements.lengthSlider.value),
        lowercase: elements.useLowercase.checked,
        uppercase: elements.useUppercase.checked,
        digits: elements.useDigits.checked,
        special: elements.useSpecial.checked,
        exclude_ambiguous: elements.excludeAmbiguous.checked
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/generate-password`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(options)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayGeneratedPassword(result.password);
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Network error:', error);
        alert('Error connecting to server');
    }
}

/**
 * Generate passphrase
 */
async function generatePassphrase() {
    const options = {
        word_count: parseInt(elements.wordCount.value),
        separator: '-',
        capitalize: elements.capitalizeWords.checked,
        add_number: elements.addNumber.checked
    };
    
    try {
        const response = await fetch(`${API_BASE_URL}/generate-passphrase`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(options)
        });
        
        const result = await response.json();
        
        if (result.success) {
            displayGeneratedPassword(result.passphrase);
        } else {
            alert(result.error);
        }
    } catch (error) {
        console.error('Network error:', error);
        alert('Error connecting to server');
    }
}

/**
 * Display generated password
 */
function displayGeneratedPassword(password) {
    elements.generatedPasswordSection.style.display = 'block';
    elements.generatedPassword.value = password;
    elements.copyFeedback.textContent = '';
}

/**
 * Copy to clipboard
 */
function copyToClipboard(text) {
    navigator.clipboard.writeText(text).then(() => {
        elements.copyFeedback.textContent = '✓ Copied to clipboard!';
        setTimeout(() => {
            elements.copyFeedback.textContent = '';
        }, 2000);
    }).catch(err => {
        console.error('Failed to copy:', err);
        elements.copyFeedback.textContent = '✗ Failed to copy';
    });
}

/**
 * Debounce function for performance
 */
function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== INITIALIZATION =====
console.log('🔐 Password Security Checker initialized');
console.log('📡 API URL:', API_BASE_URL);