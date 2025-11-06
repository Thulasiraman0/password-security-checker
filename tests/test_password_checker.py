import sys
sys.path.append('../backend')

from password_checker import PasswordChecker

def test_password_strength():
    checker = PasswordChecker()
    
    # Test 1: Empty password
    result = checker.check_strength("")
    assert result['strength'] == 'Empty'
    print("✓ Test 1 passed: Empty password")
    
    # Test 2: Weak password
    result = checker.check_strength("password")
    assert result['strength'] in ['Very Weak', 'Weak']
    print("✓ Test 2 passed: Weak password")
    
    # Test 3: Strong password
    result = checker.check_strength("Tr0pic@l-Storm!2024")
    assert result['strength'] in ['Strong', 'Very Strong']
    print("✓ Test 3 passed: Strong password")
    
    # Test 4: Length check
    result = checker.check_strength("abc")
    assert result['length'] == 3
    print("✓ Test 4 passed: Length check")
    
    # Test 5: Entropy calculation
    result = checker.check_strength("P@ssw0rd!")
    assert result['entropy'] > 0
    print("✓ Test 5 passed: Entropy calculation")
    
    print("\n✅ All tests passed!")

if __name__ == '__main__':
    test_password_strength()