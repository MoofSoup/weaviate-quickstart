import weaviate
from weaviate.classes.init import Auth
import os, json, requests
from dotenv import load_dotenv
from pathlib import Path
from weaviate.classes.config import Configure

# Try loading with explicit path
env_path = Path(__file__).parent / ".env"
load_dotenv(env_path)

# Check if file exists
print(".env file exists:", env_path.exists())
print("after loading .env", os.environ.get("WCD_URL"))

openai_key = os.getenv("OPENAI_API_KEY")
headers = {
    "X-OpenAI-Api-Key": openai_key,
}

wcd_url = os.environ["WCD_URL"]
wcd_api_key = os.environ["WCD_API_KEY"]
client = weaviate.connect_to_weaviate_cloud(
    cluster_url=wcd_url,
    auth_credentials=Auth.api_key(wcd_api_key),
    headers= headers,

)
print(client.is_ready())

questions= client.collections.create(
    "Question",
    vectorizer_config=Configure.Vectorizer.text2vec_openai(),
    generative_config=Configure.Generative.openai(),
)
questions= client.collections.get("Question")
resp =requests.get(
    "https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json"
)
data = json.loads(resp.text)

with questions.batch.dynamic() as batch:
    for d in data:
        batch.add_object({
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        })
client.close()