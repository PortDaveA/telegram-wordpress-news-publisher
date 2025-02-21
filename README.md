# Telegram WordPress News Publisher

This script fetches news articles from multiple RSS feeds, summarizes them using AI, and posts them to a **WordPress** site while also sending updates to a **Telegram** channel.

---

## 🔹 **Setup Instructions**

### **1️⃣ Adding Credentials**
Before running the script, you need to set up environment variables for authentication.

#### **📌 Method 1: Create a `.env` File (Recommended)**
Create a new file named `.env` in the same directory as the script and add the following:

```
OPENAI_API_KEY=your-openai-api-key
WORDPRESS_USERNAME=your-wordpress-username
WORDPRESS_APPLICATION_PASSWORD=your-wordpress-app-password
TELEGRAM_BOT_TOKEN=your-telegram-bot-token
TELEGRAM_CHAT_ID=your-telegram-chat-id
```

#### **📌 Method 2: Set Credentials in PowerShell (Temporary)**
Alternatively, set these credentials in PowerShell:

```powershell
$env:OPENAI_API_KEY="your-openai-api-key"
$env:WORDPRESS_USERNAME="your-wordpress-username"
$env:WORDPRESS_APPLICATION_PASSWORD="your-wordpress-app-password"
$env:TELEGRAM_BOT_TOKEN="your-telegram-bot-token"
$env:TELEGRAM_CHAT_ID="your-telegram-chat-id"
```

**Note:** These settings will reset once you close PowerShell. To make them permanent, use a `.env` file.

---

## 🔹 **Running the Script**
After setting up credentials, run the script using **PowerShell**:

```powershell
python telegram-wordpress-news-publisher.py
```

Or if you're using a virtual environment:

```powershell
venv\Scripts\activate  # (Activate the virtual environment)
python telegram-wordpress-news-publisher.py
```

To run the script continuously, use:

```powershell
python telegram-wordpress-news-publisher.py &
```

---

## 🔹 **Changing the News Sources**
The script pulls articles from multiple RSS feeds. To modify them:

1. Open **`telegram-wordpress-news-publisher.py`** in a text editor.
2. Find the `rss_feeds` list:
   ```python
   rss_feeds = [
       "https://www.sciencedaily.com/rss/top/science.xml",
       "https://rss.nytimes.com/services/xml/rss/nyt/Technology.xml",
       "https://feeds.bbci.co.uk/news/technology/rss.xml",
       "https://www.theverge.com/rss/index.xml",
       "https://feeds.arstechnica.com/arstechnica/index",
       "https://phys.org/rss-feed/breaking/"
   ]
   ```
3. **Add or remove RSS feed URLs** as needed.
4. Save the file and restart the script.

---

## 🔹 **Automating the Script**
To run the script automatically every 10 minutes, use:

#### **📌 Windows Task Scheduler**
1. Open **Task Scheduler** and create a new task.
2. Set it to run `python telegram-wordpress-news-publisher.py` every **10 minutes**.

#### **📌 Linux Cron Job**
Run `crontab -e` and add:

```cron
*/10 * * * * /usr/bin/python3 /path/to/telegram-wordpress-news-publisher.py
```

---

## 🔹 **Contributing**
Feel free to fork the repository and submit pull requests. If you have suggestions, open an issue.

---

## 🔹 **License**
This project is licensed under the **GNU General Public License v3.0 (GPL-3.0)**.  
See the [`LICENSE`](LICENSE) file for more details.
