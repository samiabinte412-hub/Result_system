import requests

barcode = "3017620422003"

url = f"https://world.openfoodfacts.org/api/v3/product/{barcode}"

headers = {
    "User-Agent": "ExpenseTracker/1.0 (your_email@example.com)",
    "Accept": "application/json",
}

response = requests.get(url, headers=headers)

data = response.json()

print(data["product"]["product_name"])
print(data["product"]["brands"])
print(data["product"]["image_front_url"])