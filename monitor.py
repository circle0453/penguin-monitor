import requests
import json

# --- Config ---
SEND_KEY = "SCT305753TX74cfUZm4vJtw50hWCyCdpnl"
TARGET_DATE = "28/12/2025" 

def send_wechat(title, content):
    url = f"https://sctapi.ftqq.com/{SEND_KEY}.send"
    data = {"title": title, "desp": content}
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def check():
    categories = {
        "GENERAL": "普通看台",
        "PPLUS": "优选看台",
        "UNDER": "地下看台"
    }
    
    # 增强伪装：让官网觉得我们是真实的浏览器
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Referer': 'https://bookings.penguins.org.au/',
        'Origin': 'https://bookings.penguins.org.au'
    }

    print(f"Starting check for {TARGET_DATE}...")
    
    for cat_code, cat_name in categories.items():
        api_url = f"https://bookings.penguins.org.au/BookingCat/Availability/?Category={cat_code}"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=15)
            
            # 先检查状态码，如果是 403 或 500 说明被拦截了
            if response.status_code != 200:
                print(f"Error checking {cat_name}: Server returned status {response.status_code}")
                continue

            # 尝试解析数据
            sessions = response.json() 
            
            for s in sessions:
                display_date = s.get('DisplayDate', '')
                remaining = s.get('TotalRemaining', 0)
                
                if TARGET_DATE in display_date:
                    if remaining > 0:
                        msg = f"妈！企鹅岛【{cat_name}】有票了！\n日期：{display_date}\n余票：{remaining}\n快抢：https://www.penguins.org.au/"
                        send_wechat(f"企鹅岛{cat_name}放票提醒", msg)
                        print(f"!!! Found {remaining} tickets for {cat_name}")
                    else:
                        print(f"{cat_name}: Still Sold Out")
        except Exception as e:
            # 如果还是报错，打印出前 100 个字符看看官网返回了什么
            print(f"Error checking {cat_name}: {str(e)[:100]}")

if __name__ == "__main__":
    check()
