# **Web Crawler**  

## **How It Works**  
1. Give it a URL.  
2. It **hunts down all the links, images, and text**.  
3. It shoves everything directly into **your Google Drive folder**.  
4. Done.  

## **Setup (You Have to Do Some Work)**  
1. Clone this thing:  
   ```bash
   git clone https://github.com/ThutaCodes/webspider
   cd webcrawler
   ```  
2. Make a Python virtual environment:  
   ```bash
   python3 -m venv venv  
   source venv/bin/activate  
   ```  
3. Install the necessary libraries:  
   ```bash
   pip install -r requirements.txt  
   ```  
4. Set up Google Drive access (ugh, this part is annoying but worth it):  
   - Create a **Service Account** in Google Cloud.  
   - Download the **JSON key file**.  
   - Share your Google Drive folder with the Service Account email.  
   - Put the JSON file in this project and rename it **`service_account.json`**.  
   - Create a `.env` file with:  
     ```plaintext
     SERVICE_ACCOUNT_FILE=service_account.json  
     DRIVE_FOLDER_ID=your_google_drive_folder_id  
     ```  

## **Run It**  
```bash
python3 web_spider.py  
```  

Now, wait while it **crawls the web and throws everything into your Drive**.  
