**URL Scan Tool**

## Description
**URL Scan Tool** is a Python-based application designed to scan URLs and assess website risks through an API. It supports user authentication, registration, customizable scanning options, and outputs scan results in multiple formats.

## Prerequisites
Before using this tool, you need to **register an account** at [URLScore.ai](https://urlscore.ai). After registration, ensure you verify your account via the confirmation email that may arrive in your inbox or spam folder.

## Features
- **Authentication and Registration**: Manage user login and registration directly from the script.
- **Flexible Scanning Options**: Customize scanning based on DNS, IP, page, and technology checks.
- **Multiple Output Formats**: Outputs scan results in JSON, plain text, and HTML for easy review.
- **Screenshot Integration**: Includes webpage screenshots in the HTML output for visual reference.

## Usage
Setting Up Credentials
- **Login Credentials: Either login via prompt or create a login.txt file in the root directory with your email and password formatted as email:password.
- **URL List: Either submit URL via prompt or create a url.txt file in the root directory with the list of URLs you want to scan, each on a new line.

Configuring Scan Options
- **Either define options via Prompt or create a ScanOptions.txt file in the root directory to specify the scanning options. Use the following format: true for enabled, false for disabled.

Example:
dns_checks:true
ip_checks:false
page_checks:true
webtech_checks:true

## Running the Script
Execute the script using Python:
python urlscore.py

## Output
The script saves the scan results in the ScanResults directory in three formats: JSON, plain text, and HTML. Each file will be named using the domain and the scan date/time.

## Contributing
Contributions are what make the open-source community such an amazing place to learn, inspire, and create. Any contributions you make are greatly appreciated.

## Fork the Project
Create your Feature Branch (git checkout -b feature/AmazingFeature)
Commit your Changes (git commit -m 'Add some AmazingFeature')
Push to the Branch (git push origin feature/AmazingFeature)
Open a Pull Request

## License
Distributed under the MIT License. See LICENSE for more information.

## Output
Contact info@urlscore.ai

## Requirements
- **Python 3.x**
- **Requests Library**: This project relies on the Requests library to handle HTTP requests.

## Installation
Clone the repository and install the necessary Python packages.

```bash
git clone https://github.com/your-github-username/url-scan-tool.git
cd url-scan-tool
pip install requests
