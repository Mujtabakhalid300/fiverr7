#pip install playwright
#python -m playwright install



import json
import os
from datetime import datetime
from time import sleep
import pandas as pd
from playwright.sync_api import sync_playwright

pageCount = 1
filtered_data = []  # List to store filtered data from each response

# Function to save the filtered data to Excel
def save_data_to_excel(filtered_data):
    # Convert the filtered data to a DataFrame
    df = pd.DataFrame(filtered_data)

    # Specify the output Excel file path
    output_excel_path = './filtered_data.xlsx'

    # If the file already exists, append the data; otherwise, create a new file
    if os.path.exists(output_excel_path):
        with pd.ExcelWriter(output_excel_path, engine='openpyxl', mode='a', if_sheet_exists='overlay') as writer:
            df.to_excel(writer, index=False, header=False, startrow=writer.sheets['Sheet1'].max_row)
    else:
        df.to_excel(output_excel_path, index=False)

    print(f"Excel file saved to {output_excel_path}")

# Function to handle request interception
def handle_request(route, request):
    if 'fetch' in request.url or 'xhr' in request.url:  # Filter for fetch/xhr requests
        print(f"Request URL: {request.url}")
        print(f"Request Method: {request.method}")
        route.continue_()  # Allow the request to continue

# Function to handle responses
def handle_response(response):
    # Check if the response URL contains 'reviews' or another indicator for reviews
    if 'query-pages' in response.url and "exceptional" not in response.url:  # Modify this condition to match the relevant API URL
        print(f"Response URL: {response.url}")
        print(f"Response Status: {response.status}")
        if response.status == 200:
            try:
                json_data = response.json()  # Parse the JSON response
                # Extract the 'contents' field and filter it
                contents = json_data.get('contents', [])
                
                # Iterate over each item in the 'contents' list
                for item in contents:
                    # Extract specific fields (modify these as needed)
                    filtered_item = {
                        'id': item.get('id'),
                        'reviewScore': item.get('reviewScore'),
                        'reviewContent': item.get('reviewContent'),
                        'createDate': item.get('createDate'),
                        'productOption': item.get("productOptionContent")
                    }
                    
                    # Append the filtered data to the list
                    filtered_data.append(filtered_item)
            except Exception as e:
                print(f"Error parsing JSON from {response.url}: {e}")

# Function to scroll the page down
def scroll_page(page):
    # Scroll down the page by a certain amount
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")  # Scroll to the bottom
    sleep(2)  # Wait for some time after scrolling

# Main script to use Playwright for scraping
def run_browser_script():
    with sync_playwright() as p:
        # Connect to the running browser using CDP
        browser = p.chromium.launch(headless=False)
        context = browser.new_context(ignore_https_errors=True)  # Ignore SSL errors
        page = context.new_page()

        # Attach event listeners to intercept requests and responses
        page.on('route', handle_request)
        page.on('response', handle_response)

        # Navigate to the page
        page.goto("https://smartstore.naver.com/hamonni")

        # Wait for the page to load completely
        page.wait_for_load_state("networkidle")

        # Scroll down the page after loading
        scroll_page(page)

        # Wait for a few more seconds to capture additional XHR requests
        sleep(3)

        page.click("#BestReviewProducts > div > ul._3sedve9sdj > li:nth-child(1) > div > a > div.EmQ79FXbY0 > div > div")
        # Wait for the requests to be intercepted and processed
        page.wait_for_timeout(10000)  # Adjust timeout if needed to ensure data is captured
        page.wait_for_load_state("networkidle")

        scroll_page(page)
        
        # Send the fetch request and log the response status code
        page.evaluate("""
    (async function fetchData() {
        for (let pageNum = 1; pageNum <= 1001; pageNum++) {
            try {
                // Send fetch request
                const response = await fetch("https://smartstore.naver.com/i/v1/contents/reviews/query-pages", {
                    method: "POST",
                    headers: {
                        "accept": "application/json, text/plain, */*",
                        "accept-language": "en-PK,en-US;q=0.9,en;q=0.8",
                        "content-type": "application/json",
                        "priority": "u=1, i",
                        "sec-ch-ua": "\\"Chromium\\";v=\\"128\\", \\"Not;A=Brand\\";v=\\"24\\", \\"Google Chrome\\";v=\\"128\\"",
                        "sec-ch-ua-mobile": "?0",
                        "sec-ch-ua-platform": "\\"Linux\\"",
                        "sec-fetch-dest": "empty",
                        "sec-fetch-mode": "cors",
                        "sec-fetch-site": "same-origin",
                        "x-client-version": "20241119000241"
                    },
                    referrer: "https://smartstore.naver.com/hamonni/products/3665125285",
                    referrerPolicy: "no-referrer-when-downgrade",
                    body: JSON.stringify({
                        "checkoutMerchantNo": 510244741,
                        "originProductNo": 3659054112,
                        "page": pageNum,
                        "pageSize": 20,
                        "reviewSearchSortType": "REVIEW_RANKING"
                    }),
                    mode: "cors",
                    credentials: "include"
                });

                console.log('Page', pageNum, 'Response Status:', response.status);
                const data = await response.json();
                console.log('Fetched data for page', pageNum, ':', data);

            } catch (error) {
                console.error('Error for page', pageNum, ':', error);
            }

            // Wait for 2 seconds before sending the next request
            await new Promise(resolve => setTimeout(resolve, 2000));
        }
    })(); // Self-invoking the async function
""")

        # Wait for a while to let the fetch request complete
        page.wait_for_timeout(5000)

        # Save the data to Excel
        save_data_to_excel(filtered_data)

        # Close the browser
        input("Press Enter to close the browser...")  # This will keep the browser open until the user presses Enter


def main():
    sleep(3)  # Ensure that the Chrome session is ready
    run_browser_script()

# Run the main function
main()
