import requests

# --- 你的配置 ---
SEND_KEY = "SCT305753TX74cfUZm4vJtw50hWCyCdpnl"
# 监控日期：2025年12月28日
TARGET_DATE = "28/12/2025" 

def send_wechat(title, content):
    """通过Server酱发送微信通知"""
    url = f"https://sctapi.ftqq.com/{SEND_KEY}.send"
    data = {"title": title, "desp": content}
    try:
        requests.post(url, data=data, timeout=10)
    except:
        pass

def check():
    # 监控三个档位的票：GENERAL(普通), PPLUS(优选), UNDER(地下)
    categories = {
        "GENERAL": "普通看台",
        "PPLUS": "优选看台",
        "UNDER": "地下看台"
    }
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Accept': 'application/json'
    }

    print(f"开始检查 {TARGET_DATE} 的票务情况...")
    
    for cat_code, cat_name in categories.items():
        api_url = f"https://bookings.penguins.org.au/BookingCat/Availability/?Category={cat_code}"
        
        try:
            response = requests.get(api_url, headers=headers, timeout=15)
            sessions = response.json() 
            
            for s in sessions:
                display_date = s.get('DisplayDate', '')
                remaining = s.get('TotalRemaining', 0)
                
                # 匹配目标日期
                if TARGET_DATE in display_date:
                    if remaining > 0:
                        msg = (f"妈！企鹅岛【{cat_name}】有票了！\n\n"
                               f"日期：{display_date}\n"
                               f"目前剩余：{remaining}张\n"
                               f"官网快抢：https://www.penguins.org.au/")
                        send_wechat(f"企鹅岛{cat_name}放票提醒", msg)
                        print(f"！！！发现 {cat_name} 余票: {remaining}")
                    else:
                        print(f"{cat_name} ({display_date}): 仍然售罄")
        except Exception as e:
            print(f"检查 {cat_name} 时出错: {e}")

if __name__ == "__main__":
    check()
