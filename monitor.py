import requests
import time

SEND_KEY = "SCT305753TX74cfUZm4vJtw50hWCyCdpnl"
TARGET_DATE = "28/12/2025"

def check():
    # 建立一个会话，模拟点击 Buy Now 之前的访问
    session = requests.Session()
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Referer': 'https://www.penguins.org.au/',
    }

    try:
        # 第一步：模拟访问官网首页，获取合法的 Cookie
        print("Step 1: Visiting homepage to get cookies...")
        session.get("https://bookings.penguins.org.au/", headers=headers, timeout=15)
        
        # 稍微等一下，模拟人的操作延迟
        time.sleep(3)

        # 第二步：访问数据接口
        api_url = f"https://bookings.penguins.org.au/BookingCat/Availability/?Category=GENERAL&_={int(time.time())}"
        print("Step 2: Checking ticket data...")
        
        response = session.get(api_url, headers=headers, timeout=15)
        
        # 如果返回的是 HTML 而不是数据，说明还是被拦截了
        if "<html" in response.text.lower():
            print("Failed: The website redirected us to a web page instead of data.")
            return

        data = response.json()
        for s in data:
            if TARGET_DATE in s.get('DisplayDate', ''):
                remaining = s.get('TotalRemaining', 0)
                print(f"Result: {s.get('DisplayDate')} remains {remaining}")
                if remaining > 0:
                    # 发送通知逻辑...
                    pass
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    check()
