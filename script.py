import os
from dotenv import load_dotenv

# 1. Load the variables from the .env file into the environment
load_dotenv()

# 2. Grab the specific keys using os.getenv
app_id = os.getenv("EDAMAM_APP_ID")
app_key = os.getenv("EDAMAM_APP_KEY")

# 3. Use them! (This is a simple test to see if it works)
if app_id and app_key:
    print("✅ Keys loaded successfully!")
    print(f"Your App ID is: {app_id}")
else:
    print("❌ Failed to load keys. Check your .env file name and location.")