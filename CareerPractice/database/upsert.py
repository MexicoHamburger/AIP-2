import json
import os
from dotenv import load_dotenv
from pinecone import Pinecone
import openai


load_dotenv()
openai_api_key = os.getenv("OPENAI_API_KEY")
pinecone_api_key = os.getenv("PINECONE_API_KEY")


client = openai.OpenAI(api_key=openai_api_key)
pc = Pinecone(api_key=pinecone_api_key)
index = pc.Index("careerpractice-index")


with open("result1.json", encoding="utf-8") as f:
    data = json.load(f)


for vec_id, item in data.items():

    emb = (
        client.embeddings.create(
            model="text-embedding-3-small", input=item["text"], dimensions=512
        )
        .data[0]
        .embedding
    )

    meta = {
        "category": item["category"],
        "name": item["name"],
        "link": item["link"],
        "field": ", ".join(item["field"]),
        "skills": ", ".join(item["skills"]),
        "description": item["description"],
    }

    index.upsert([{"id": vec_id, "values": emb, "metadata": meta}])
