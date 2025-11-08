import requests
import feedparser
import time
from bs4 import BeautifulSoup

# ---------- تنظیمات ----------
BOT_TOKEN = "8419410295:AAEoZYyk1iI7PTXbTnKOVRfTQbx7UtD5Whs #  "توکن_بات_اینجا
CHAT_ID = "7182754907 #   "آی‌دی_چت_اینجا

NEWS_FEEDS = [
    "https://www.coindesk.com/arc/outboundfeeds/rss/",
    "https://cointelegraph.com/rss"
]

CHECK_INTERVAL = 60 * 60  # هر چند وقت یک بار خبر بفرسته (اینجا هر ۱ ساعت)
MAX_ARTICLES = 5          # حداکثر چند خبر در هر بار بررسی

sent_titles = set()       # برای جلوگیری از تکرار

# ---------- تابع ارسال پیام به تلگرام ----------
def send_to_telegram(message):
    url = f"https://api.telegram.org/bot{BOT_TOKEN}/sendMessage"
    data = {"chat_id": CHAT_ID, "text": message}
    try:
        requests.post(url, data=data)
    except Exception as e:
        print("❌ خطا در ارسال:", e)

# ---------- تابع گرفتن خلاصه متن خبر ----------
def summarize_article(link):
    try:
        res = requests.get(link, timeout=10)
        soup = BeautifulSoup(res.text, "html.parser")
        paragraphs = soup.find_all("p")
        text = " ".join(p.get_text() for p in paragraphs[:3])
        if len(text) > 400:
            text = text[:400] + "..."
        return text.strip()
    except:
        return ""

# ---------- تابع گرفتن خبرها ----------
def fetch_news():
    all_news = []
    for feed in NEWS_FEEDS:
        parsed = feedparser.parse(feed)
        for entry in parsed.entries[:MAX_ARTICLES]:
            title = entry.title
            link = entry.link
            if title not in sent_titles:
                summary = summarize_article(link)
                msg = f"📰 {title}\n\n{summary}\n\n🔗 {link}"
                all_news.append(msg)
                sent_titles.add(title)
    return all_news

# ---------- اجرای بات ----------
print("✅ بات خبری کریپتو شروع به کار کرد...")
while True:
    news_items = fetch_news()
    for n in news_items:
        send_to_telegram(n)
        time.sleep(2)  # تا تلگرام اسپم حساب نکنه
    print("🔁 منتظر بررسی بعدی...")
    time.sleep(CHECK_INTERVAL)
  
