import re
import argparse
from pathlib import Path

def entropy_bits(password: str) -> float:
    # Simple entropy estimation based on character variety and length
    charset = 0
    if re.search(r'[a-z]', password):
        charset += 26
    if re.search(r'[A-Z]', password):
        charset += 26
    if re.search(r'[0-9]', password):
        charset += 10
    if re.search(r'[^a-zA-Z0-9]', password):
        charset += 32  # Approximate number of symbols
    if charset == 0:
        return 0.0
    return len(password) * (charset.bit_length())

def repeated_sequence_score(password: str) -> int:
    # Penalize repeated sequences (e.g., "aaa", "abcabc")
    for i in range(1, len(password)//2 + 1):
        seq = password[:i]
        if seq * (len(password)//i) == password:
            return 1
    if re.search(r'(.)\1{2,}', password):
        return 1
    return 0

def keyboard_pattern_score(password: str) -> int:
    # Penalize common keyboard patterns
    patterns = ['qwerty', 'asdf', 'zxcv', '12345', 'password']
    for pat in patterns:
        if pat in password.lower():
            return 1
    return 0

def is_common_password(password: str, common_set: set) -> bool:
    return password in common_set or password.lower() in common_set

def load_common_passwords(path: Path) -> set:
    s = set()
    try:
        with path.open(encoding='utf-8', errors='ignore') as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                s.add(line)
                s.add(line.lower())
    except Exception as e:
        print(f"Could not read common passwords file: {e}")
    return s

def grade_password(pw: str, common_set: set = None) -> dict:
    ent = entropy_bits(pw)
    length = len(pw)
    has_lower = bool(re.search(r'[a-z]', pw))
    has_upper = bool(re.search(r'[A-Z]', pw))
    has_digit = bool(re.search(r'[0-9]', pw))
    has_symbol = bool(re.search(r'[^a-zA-Z0-9]', pw))

    issues = []
    score = 0

    if length < 8:
        issues.append("Password length is short (< 8).")
    else:
        score += 1
    if has_lower: score += 1
    else: issues.append("Add lowercase letters (a-z).")
    if has_upper: score += 1
    else: issues.append("Add uppercase letters (A-Z).")
    if has_digit: score += 1
    else: issues.append("Add digits (0-9).")
    if has_symbol: score += 1
    else: issues.append("Add symbols or punctuation (e.g. !@#).")

    rep = repeated_sequence_score(pw)
    keypat = keyboard_pattern_score(pw)
    score -= (rep + keypat)
    if rep:
        issues.append("Repeated characters or patterns in password.")
    if keypat:
        issues.append("Contains a known keyboard pattern (e.g. qwerty or 12345).")

    if common_set and is_common_password(pw, common_set):
        issues.append("Password is found in the common passwords list — change it immediately!")
        score -= 5

    if ent >= 60 and score >= 3:
        strength = "Very strong"
    elif ent >= 45 and score >= 1:
        strength = "Strong"
    elif ent >= 28:
        strength = "Medium"
    else:
        strength = "Weak"

    suggestions = []
    if length < 12:
        suggestions.append("Make the password 12 characters or longer for better security.")
    suggestions.append("Use a long passphrase instead of a short password.")
    suggestions.append("Combine uppercase, lowercase, digits, and symbols.")
    suggestions.append("Avoid known words or keyboard patterns.")
    suggestions.append("Use a password manager to generate and store strong, unique passwords for each site.")

    return {
        "password": pw,
        "length": length,
        "entropy_bits": round(ent, 2),
        "score_metric": score,
        "strength": strength,
        "issues": issues,
        "suggestions": suggestions
    }

def pretty_print_report(r: dict):
    print("=== Password Check Report ===")
    print(f"Entered password: {r['password']}")
    print(f"Length: {r['length']}  |  Entropy estimate: {r['entropy_bits']} bits")
    print(f"Overall assessment: {r['strength']}  |  Internal metric: {r['score_metric']}")
    if r['issues']:
        print("\nDetected issues:")
        for i in r['issues']:
            print(" -", i)
    else:
        print("\nNo major issues detected.")
    print("\nSuggestions to improve your password:")
    for s in r['suggestions']:
        print(" -", s)
    print("=============================")

def parse_args():
    p = argparse.ArgumentParser(description="Password Strength Checker with optional common-password file")
    p.add_argument("password", nargs='?', help="Password to check (or leave empty for interactive input)")
    p.add_argument("--common", "-c", help="Path to common passwords file (txt) for dictionary check", default=None)
    return p.parse_args()

def main():
    args = parse_args()
    common_set = set()
    if args.common:
        path = Path(args.common)
        if path.exists():
            common_set = load_common_passwords(path)
            print(f"Loaded {len(common_set)} entries (including lowercase copies) from file: {path}")
        else:
            print(f"Common passwords file not found: {path} — dictionary check will be skipped.")

    if args.password:
        pw = args.password
    else:
        try:
            pw = input("Enter password to check: ")
        except KeyboardInterrupt:
            print("\nCancelled.")
            return

    report = grade_password(pw, common_set)
    pretty_print_report(report)
