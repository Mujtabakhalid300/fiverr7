import requests

cookies = {
    '_fwb': '153xPUKhGK7Y0p0tJiz9FHG.1731960655552',
    'NAC': '66NeCwAfRZYRB',
    'NNB': 'LJETARSTT45WO',
    'BUC': 'DxZ80uWMXLx4qcH_T9UiQVshvsRgFDOKu4xaaUzLYgw=',
}

headers = {
    'Cache-Control': 'no-cache',  # Prevents caching
    'Pragma': 'no-cache', 
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-US,en;q=0.9',
    'content-type': 'application/json',
    # 'cookie': '_fwb=153xPUKhGK7Y0p0tJiz9FHG.1731960655552; NAC=66NeCwAfRZYRB; NNB=LJETARSTT45WO; BUC=DxZ80uWMXLx4qcH_T9UiQVshvsRgFDOKu4xaaUzLYgw=',
    'origin': 'https://smartstore.naver.com',
    'priority': 'u=1, i',
    'referer': 'https://smartstore.naver.com/hamonni/products/3665125285',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
    'x-client-version': '20241119000241',
}

json_data = {
    'checkoutMerchantNo': 510244741,
    'originProductNo': 3659054112,
    'page': 3,
    'pageSize':20,
    'reviewSearchSortType': 'REVIEW_RANKING',
}

response = requests.post(
    'https://smartstore.naver.com/i/v1/contents/reviews/query-pages',
    cookies=cookies,
    headers=headers,
    json=json_data,
)

# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
data = '{"checkoutMerchantNo":510244741,"originProductNo":3659054112,"page":1,"pageSize":30,"reviewSearchSortType":"REVIEW_RANKING"}'
response = requests.post(
   'https://smartstore.naver.com/i/v1/contents/reviews/query-pages',
   cookies=cookies,
   headers=headers,
   data=data,
) 

import json

# Assuming you have the 'response' object, for example from an HTTP request:
# response = requests.get("your_api_url")

# 1. Parse response content to JSON
try:
    # If response.content is a byte object, we can decode it to a string and load it as JSON
    json_data = response.json()
    # .json() method automatically converts content to JSON
    print(len(json_data["contents"]))
    # 2. Define the path for the output JSON file
    output_file = "response_data.json"

    # 3. Write JSON data to a file
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(json_data, f, ensure_ascii=False, indent=4)

    print(f"JSON data saved to {output_file}")

except Exception as e:
    print(f"Error parsing response content: {e}")
