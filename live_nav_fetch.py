import requests
import pandas as pd

SCHEMES = {
    119598: "SBI_Large_Cap_Direct",
    120586: "ICICI_Large_Cap_Direct",
    120465: "Axis_Large_Cap_Direct",
    118632: "Nippon_Large_Cap_Direct",
    125497: "SBI_Small_Cap_Direct",   
}
all_navs = []
for code, name in SCHEMES.items():
    url = f"https://api.mfapi.in/mf/{code}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        meta = data['meta']

        df = pd.DataFrame(data['data'])
        df['scheme_code'] = meta['scheme_code']
        df['scheme_name'] = meta['scheme_name']
        df['fund_house'] = meta['fund_house']
        df['scheme_category'] = meta['scheme_category']
        df['scheme_type'] = meta['scheme_type']
        df['isin_growth'] = meta['isin_growth']
        df['isin_div_reinvestment'] = meta['isin_div_reinvestment']
        all_navs.append(df)
    else:
        print(f"{name}: HTTP {response.status_code}")

# print(all_navs[0].head())  
final_df = pd.concat(all_navs, ignore_index=True)
final_df.to_csv('data/raw/live_nav_history.csv', index=False)
print("Live NAV history saved to: data/raw/live_nav_history.csv") 
print(len(final_df), "rows fetched across", len(SCHEMES), "schemes.")

print(final_df.head())