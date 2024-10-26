import weaviate
from weaviate.classes.init import Auth
import os
from dotenv import load_dotenv
from pathlib import Path

# Try loading with explicit path
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Check if file exists
print(".env file exists:", env_path.exists())
print("after loading .env", os.environ.get("WCD_URL"))
wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,
    auth_credentials=Auth.api_key(wcd_api_key),

)
print(client.is_ready())
client.close()