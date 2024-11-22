import requests
import pandas as pd
from time import time



starttime = time()
filtered_data=[]
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


# Note: json_data will not be serialized by requests
# exactly as it was in the original request.
# data = '{"checkoutMerchantNo":510244741,"originProductNo":3659054112,"page":1,"pageSize":30,"reviewSearchSortType":"REVIEW_RANKING"}'
# response = requests.post(
#    'https://smartstore.naver.com/i/v1/contents/reviews/query-pages',
#    cookies=cookies,
#    headers=headers,
#    data=data,
# ) 

for i in range(1,2900):
    data = '{"checkoutMerchantNo":510244741,"originProductNo":3659054112,"page":' + str(i) + ',"pageSize":30,"reviewSearchSortType":"REVIEW_RANKING"}'
    response = requests.post(
   'https://smartstore.naver.com/i/v1/contents/reviews/query-pages',
    cookies=cookies,
    headers=headers,
    data=data,  
        )
    print(response.status_code)
    if response.status_code==200:
        data = response.json()
        contents = data.get('contents', [])
        
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
        
    else:
        print("No more reviews left or an error occured")
        break
    print(str(i) + " pages scraped")


# Create a pandas DataFrame from the filtered data
df = pd.DataFrame(filtered_data)

# Specify the output Excel file path
output_excel_path = './filtered_data_new.xlsx'

# Write the DataFrame to an Excel file
df.to_excel(output_excel_path, index=False)

print(f"Excel file saved to {output_excel_path}")


endtime=time()

print("Total time taken:  " + str(endtime-starttime) + " sec")