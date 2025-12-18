import requests
import time

# --- 配置 ---
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
    
    # 模拟真实海外浏览器的请求头
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'application/json, text/plain, */*',
        'Accept-Language': 'en-US,en;q=0.9',
        'Referer': 'https://bookings.penguins.org.au/',
        'Origin': 'https://bookings.penguins.org.au',
        'Cache-Control': 'no-cache',
        'Pragma': 'no-cache'
    }

    print(f"Starting check for {TARGET_DATE}...")
    
    # 创建一个 Session 自动处理 Cookie，这能大幅降低被拦截的概率
    session = requests.Session()
    session.headers.update(headers)

    for cat_code, cat_name in categories.items():
        api_url = f"https://bookings.penguins.org.au/BookingCat/Availability/?Category={cat_code}"
        
        try:
            # 稍微停顿一下，不要请求太猛
            time.sleep(2)
            response = session.get(api_url, timeout=20)
            
            # 检查是否被拦截（非200状态码）
            if response.status_code != 200:
                print(f"Server blocked us (Status {response.status_code}) for {cat_name}")
                continue

            # 尝试解析
            try:
                data = response.json()
            except:
                print(f"Received non-JSON response for {cat_name}. Website might be showing a CAPTCHA.")
                continue
            
            for s in data:
                display_date = s.get('DisplayDate', '')
                remaining = s.get('TotalRemaining', 0)
                
                if TARGET_DATE in display_date:
                    if remaining > 0:
                        msg = f"妈！企鹅岛【{cat_name}】有票了！\n日期：{display_date}\n余票：{remaining}\n快抢：https://www.penguins.org.au/"
                        send_wechat(f"企鹅岛放票提醒", msg)
                        print(f"!!! Found {remaining} tickets for {cat_name}")
                    else:
                        print(f"{cat_name}: Still Sold Out")
                        
        except Exception as e:
            print(f"Error checking {cat_name}: {e}")

if __name__ == "__main__":
    check()
