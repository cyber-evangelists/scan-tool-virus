from dotenv import load_dotenv
import os
load_dotenv()
mongo_url = os.getenv('MONGO_URL')