from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct,Filter, FieldCondition, MatchValue
from app.config.config import config
from dotenv import load_dotenv
import uuid
import os
COLLECTION_NAME = "documents"

# client = QdrantClient(host="localhost", port=6333) #CHANGING THIS TO TURN TO AIRFLOW INSTEAD OF LOCAL SETUP
client = QdrantClient(
    # host="qdrant",
    host="host.docker.internal",
    port=6333
)

def init_collection(dim: int):
    if COLLECTION_NAME in [c.name for c in client.get_collections().collections]:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=dim, distance=Distance.COSINE), #cosine similarity used for vectors
        
    )


def upsert_vectors(ids, vectors, payloads):
    points = [
        PointStruct(id=i, vector=v.tolist(), payload=p)
        for i, v, p in zip(ids, vectors, payloads)
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

#initially ts was my search
def search_simple_with_duplicates(query_vector, top_k=5):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector.tolist(),
        limit=top_k
    )
    return results.points
#CHANGING BECAUSE DUPLICATE RESULTS IN THE QUERY

def search(query_vector, top_k=5):
    limit = min(top_k * 5, 100)  # hard cap, gets the top 25 chunks for this paarticular embeddings
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector.tolist(),
        limit=limit
    )
    seen = {}
    #removing duplicate chunks for the same file_id
    for p in results.points:
        fid = p.payload["file_id"]
        if fid not in seen or p.score > seen[fid].score:
            seen[fid] = p
    unique = sorted(seen.values(), key=lambda x: x.score, reverse=True)
    return unique[:top_k]

#to delete old chunks before upserting new ones

def delete_vectors_by_file_id(file_id: int):
    client.delete(
        collection_name=COLLECTION_NAME,
        points_selector=Filter(
            must=[
                FieldCondition(
                    key="file_id",
                    match=MatchValue(value=file_id)
                )
            ]
        )
    )

#100th commit in laast 365 days ITMO rhinks
