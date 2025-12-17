import requests
import os

# 配置信息
SEND_KEY = "SCT305753TX74cfUZm4vJtw50hWCyCdpnl"
# 你想监控的日期，格式 YYYY-MM-DD，如果监控多个日期用逗号隔开
TARGET_DATES = ["2025-01-20", "2025-01-21"] 

def check():
    # 企鹅岛官方查询接口 (这里以 Penguins Plus 为例)
    url = "https://bookings.penguins.org.au/BookingCat/Availability/?Category=PPLUS"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # 获取网页数据
        response = requests.get(url, headers=headers, timeout=10)
        # 简单判断页面是否包含有票的标志 (这只是一个逻辑演示，具体需匹配官网JSON)
        # 为了稳定，我们直接查找目标日期
        content = response.text
        
        for date in TARGET_DATES:
            if date in content and "Sold Out" not in content:
                msg = f"企鹅岛有票啦！日期：{date}。快去官网抢票！"
                requests.post(f"https://sctapi.ftqq.com/{SEND_KEY}.send?title=企鹅岛票务提醒&desp={msg}")
                print(f"{date} 可能有票，已发送通知")
            else:
                print(f"{date} 目前无票")
    except Exception as e:
        print(f"检查失败: {e}")

if __name__ == "__main__":
    check()
