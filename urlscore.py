import json
import os
from datetime import datetime
import requests
from urllib.parse import urlparse


def format_scan_results(scan_results):
    results = scan_results  # Assuming scan_results is already a dictionary
    output = []
    output.append(f"Scan Summary for: {results['url']}\n")
    for category in results['checks']:
        output.append(f"Category: {category['category']} (Risk Score: {category['risk_score']})")
        for detail in category['details']:
            output.append(f"  Check: {detail['title']} - {detail['message']} (Risk Score: {detail['risk_score']})")
        output.append("")
    output.append("Overall Analysis:")
    output.append(f"  Risk Score: {results['overall_risk']}")
    output.append(f"  Classification: {results.get('risk_score_text', {}).get('name', 'N/A')}")
    output.append(f"  Description: {results.get('risk_score_text', {}).get('description', 'N/A')}")
    output.append(f"  AI Analysis: {results['ai_analysis']}")
    geo_info = results.get('geo_location', {})
    if geo_info:
        output.append("Geolocation Details:")
        output.append(f"  IP: {geo_info.get('ip', 'N/A')} - ISP: {geo_info.get('isp', 'N/A')}")
        output.append(f"  Location: {geo_info.get('city', 'N/A')}, {geo_info.get('state_prov', 'N/A')}, {geo_info.get('country_name', 'N/A')}")
        output.append(f"  Continent: {geo_info.get('continent_name', 'N/A')}")
    screenshot = results.get('screenshot_link', None)
    if screenshot:
        output.append(f"Screenshot of the scan: {screenshot}")
    return "\n".join(output)
    
    
def read_login():
    try:
        with open('login.txt', 'r') as file:
            credentials = file.readline().strip().split(':')
            return credentials[0], credentials[1]
    except FileNotFoundError:
        return None, None

def login(email, password):
    url = 'https://scan.urlscore.ai/api/login/'
    headers = {'Content-Type': 'application/json'}
    data = {'email': email, 'password': password}
    response = requests.post(url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Authenticated with {email}")
        return response.json()['token']  # Ensure this matches the key provided by your API
    else:
        print("Login failed. Check credentials or network.")
        return None

def scan_url(api_token, url, scan_options):
    api_url = "https://scan.urlscore.ai/api/check-url/"
    headers = {"Authorization": f"Token {api_token}"}  # Correctly formatted header
    params = scan_options
    params['url'] = url
    response = requests.get(api_url, headers=headers, params=params)
    if response.status_code == 200:
        return response.json()
    else:
        # Handle failure scenarios
        print(f"Error scanning {url}, HTTP Status Code: {response.status_code}")
        return None

def get_scan_options():
    try:
        with open('ScanOptions.txt', 'r') as file:
            options = {line.split(':')[0].strip(): line.split(':')[1].strip() == 'true' for line in file}
            return options
    except FileNotFoundError:
        options = {}
        options['dns_checks'] = input("Enable DNS Checks? (yes/no): ").strip().lower() == 'yes'
        options['ip_checks'] = input("Enable IP Checks? (yes/no): ").strip().lower() == 'yes'
        options['page_checks'] = input("Enable Page Checks? (yes/no): ").strip().lower() == 'yes'
        options['webtech_checks'] = input("Enable Webtech Checks? (yes/no): ").strip().lower() == 'yes'
        return options



def scan_url(api_token, url, scan_options):
    api_url = "https://scan.urlscore.ai/api/check-url/"
    headers = {"Authorization": f"token {api_token}"}

    # Check if URL starts with http:// or https://, otherwise prepend https://
    if not url.startswith(('http://', 'https://')):
        url = f'https://{url}'
        
    params = scan_options
    params['url'] = url
    response = requests.get(api_url, headers=headers, params=params)

    print(f"Submitting URL {url} with options {json.dumps(scan_options)}")  # Debug: request details

    def handle_response(response):
        if response.status_code == 200:
            print(f"Scan successful for {url}")
            results = response.json()
            formatted_results = format_scan_results(results)  # Assuming format_scan_results is defined
            print(formatted_results)  # Print formatted results for immediate user feedback
            return results
        else:
            print(f"Error scanning {url}")
            print(f"Status Code: {response.status_code}")  # Debug: status code
            try:
                print(f"Response: {response.json()}")  # Debug: response body
            except json.JSONDecodeError:
                print(f"Non-JSON response: {response.text}")  # Debug: non-JSON response
            return None

    # First try HTTPS (or HTTP if already in the URL)
    result = handle_response(response)
    if result is not None:
        return result

    # If HTTPS fails, try with HTTP only if HTTPS was originally added
    if url.startswith('https://'):
        url = url.replace('https://', 'http://')
        params['url'] = url
        response = requests.get(api_url, headers=headers, params=params)
        print(f"Submitting URL {url} with options {json.dumps(scan_options)}")  # Debug: request details
        return handle_response(response)
    else:
        return None  # If the first try was already HTTP, no need to retry

def format_results_to_html(results):
    html_content = ['<html><head><title>Scan Results</title><style>body { font-family: Arial, sans-serif; } h1, h2, p { margin: 0.5em 0; }</style></head><body>']
    
    # Add the screenshot if available at the top under the title
    html_content.append(f"<h1>Scan Summary for: {results['url']}</h1>")
    screenshot = results.get('screenshot_link')
    if screenshot:
        html_content.append(f'<img src="{screenshot}" alt="Screenshot of {results["url"]}" style="max-width:100%;height:auto;">')

    for category in results['checks']:
        html_content.append(f"<h2>Category: {category['category']} (Risk Score: {category['risk_score']})</h2>")
        for detail in category['details']:
            html_content.append(f"<p><b>{detail['title']}</b>: {detail['message']} (Risk Score: {detail['risk_score']})</p>")
    
    html_content.append("<h2>Overall Analysis:</h2>")
    html_content.append(f"<p>Risk Score: {results['overall_risk']}</p>")
    html_content.append(f"<p>Classification: {results.get('risk_score_text', {}).get('name', 'N/A')}</p>")
    html_content.append(f"<p>Description: {results.get('risk_score_text', {}).get('description', 'N/A')}</p>")
    html_content.append(f"<p>AI Analysis: {results['ai_analysis']}</p>")
    
    if 'geo_location' in results:
        geo_info = results['geo_location']
        html_content.append("<h2>Geolocation Details:</h2>")
        html_content.append(f"<p>IP: {geo_info.get('ip', 'N/A')} - ISP: {geo_info.get('isp', 'N/A')}</p>")
        html_content.append(f"<p>Location: {geo_info.get('city', 'N/A')}, {geo_info.get('state_prov', 'N/A')}, {geo_info.get('country_name', 'N/A')}</p>")
        html_content.append(f"<p>Continent: {geo_info.get('continent_name', 'N/A')}</p>")
    
    html_content.append("</body></html>")
    return ''.join(html_content)




def save_scan_results(domain, results):
    directory = 'ScanResults'
    if not os.path.exists(directory):
        os.makedirs(directory)
    date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    base_filename = f"Scan_{domain[:7]}_{date_str}"
    json_path = os.path.join(directory, f"{base_filename}.json")
    txt_path = os.path.join(directory, f"{base_filename}.txt")
    html_path = os.path.join(directory, f"{base_filename}.html")

    with open(json_path, 'w') as file:
        json.dump(results, file, indent=4)
    with open(txt_path, 'w') as file:
        file.write(str(results))
    with open(html_path, 'w') as file:
        html_results = format_results_to_html(results)
        file.write(html_results)

    print(f"Results saved in JSON, text, and HTML formats under {directory}/")



def main():
    email, password = read_login()
    if not email or not password:
        email = input("Enter your email: ")
        password = input("Enter your password: ")

    # Initialize token as None to ensure it has a defined state
    token = None

    # Attempt to login and fallback to registration if unsuccessful
    if email and password:
        token = login(email, password)
        if not token:
            token = register(email, password)

    # Check if token was successfully obtained before proceeding
    if not token:
        print("Authentication failed. Cannot proceed without a valid token. Exiting...")
        return

    try:
        with open('url.txt', 'r') as file:
            urls = [line.strip() for line in file if line.strip()]
    except FileNotFoundError:
        urls = [input("Enter URL to scan: ").strip()]

    scan_options = get_scan_options()
    
    for url in urls:
        results = scan_url(token, url, scan_options)
        if results:
            parsed_url = urlparse(url)
            domain = parsed_url.netloc or urlparse('http://' + url).netloc  # Handles cases without schemes
            save_scan_results(domain.split(':')[0], results)  # Strip port if included
            
    print("Scanning complete. Check the 'ScanResults' directory for output files.")


if __name__ == "__main__":
    main()
