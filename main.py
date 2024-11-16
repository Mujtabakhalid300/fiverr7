import json
import os
from datetime import datetime
from playwright.sync_api import sync_playwright

# Function to save the JSON data to a file
def save_json_to_file(url, json_data):
    # Generate a unique filename based on the URL or a timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    url_segment = url.split("/")[-1]  # Get a relevant part of the URL as the identifier
    filename = f"{url_segment}_{timestamp}.json"
    print(filename)

    # Ensure the directory exists
    os.makedirs('json_responses', exist_ok=True)

    # Save JSON data to a file
    file_path = os.path.join('json_responses', filename)
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)
    print(f"JSON saved to {file_path}")

# Function to handle request interception
def handle_request(route, request):
    if 'fetch' in request.url or 'xhr' in request.url:  # Filter for fetch/xhr requests
        print(f"Request URL: {request.url}")
        print(f"Request Method: {request.method}")
        route.continue_()  # Allow the request to continue

# Function to handle responses
def handle_response(response):
    # Check if the response URL contains 'reviews' or another indicator for reviews
    if 'reviews' in response.url:  # Modify this condition to match the relevant API URL
        print(f"Response URL: {response.url}")
        print(f"Response Status: {response.status}")
        if response.status == 200:
            try:
                json_data = response.json()  # Parse the JSON response
                #print(f"Reviews JSON: {json_data}")
                save_json_to_file(response.url, json_data)  # Save the JSON data to a file
            except Exception as e:
                print(f"Error parsing JSON from {response.url}: {e}")

# Main script to use Playwright for scraping
with sync_playwright() as p:
    # Connect to the running browser using CDP
    browser = p.chromium.connect_over_cdp("http://127.0.0.1:9222")
    context = browser.new_context(ignore_https_errors=True)  # Ignore SSL errors
    page = context.new_page()

    # Attach event listeners to intercept requests and responses
    page.on('route', handle_request)
    page.on('response', handle_response)

    # Navigate to the page
    page.goto("https://smartstore.naver.com/hamonni/products/3665125285")

    # Wait for the page to load completely
    page.wait_for_load_state("networkidle")

    # Wait for the requests to be intercepted and processed
    page.wait_for_timeout(5000)  # Adjust timeout if needed to ensure data is captured

    # Close the browser
    browser.close()
