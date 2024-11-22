import requests

# Define the cookies and headers as before
cookies = {
    'wcs_bt': 's_3c13a5d027ae:1732223997',
    '_fwb': '198cmLVBcwGcCyJNueiqDl8.1731760840424',
    'NAC': 'Q0nIBYgcrOHM',
    'NNB': 'IJG5CGGNSI4GO',
    'CBI_SNS': 'naver|trLWd_3SWmr_Rrz8',
    'NACT': '1',
    'BUC': '1zf-yI8R4YON3UM6s2PdRPPFG9zr5C69qwHQ2LODPJ8=',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-PK,en-US;q=0.9,en;q=0.8',
    'cache-control': 'max-age=0',
    # 'cookie': 'wcs_bt=s_3c13a5d027ae:1732223997; _fwb=198cmLVBcwGcCyJNueiqDl8.1731760840424; NAC=Q0nIBYgcrOHM; NNB=IJG5CGGNSI4GO; CBI_SNS=naver|trLWd_3SWmr_Rrz8; NACT=1; BUC=1zf-yI8R4YON3UM6s2PdRPPFG9zr5C69qwHQ2LODPJ8=',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="128", "Not;A=Brand";v="24", "Google Chrome";v="128"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Linux"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36',
}

# Create a session
session = requests.Session()

# Set the headers and cookies for the session
session.cookies.update(cookies)
session.headers.update(headers)

# Perform a GET request using the session
response = session.get('https://smartstore.naver.com/hamonni')

print(response.status_code)

# You can now make further requests in the session
# Example:
response2 = session.get('https://smartstore.naver.com/hamonni/products/3665125285')
print(response2.status_code)
