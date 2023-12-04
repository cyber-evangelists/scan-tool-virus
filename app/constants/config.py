from dotenv import load_dotenv
import os
load_dotenv()
mongo_url = os.getenv('MONGO_URL')
secret = os.getenv('JWT_SECRET')
algorithm = os.getenv('JWT_ALGORITHM')
vt_api_key = os.getenv('VT_API')