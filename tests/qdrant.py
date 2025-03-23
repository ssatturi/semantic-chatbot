from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct
import json
# Connect to Qdrant (update host/port if needed)
client = QdrantClient(host="localhost", port=6333)

# Replace with your actual collection name
collection_name = "chat_vectors"

# Fetch a few sample points (e.g., top 5)
response = client.scroll(
    collection_name=collection_name,
    limit=5,
    with_payload=True,
    with_vectors=True  # Set True if you also want to inspect vector values
)

print("\n=== Sample Points in Collection ===")
for point in response[0]:
    print(f"ID: {point.id}")
    print(f"Payload: {point.payload}")
    print("-" * 30)
    # myres = point
    # print(myres)
    print("-" * 30)
    # results = client.scroll(
    #     collection_name=collection_name,
    #     limit=10,
    #     with_payload=True,
    #     scroll_filter={
    #         "must": [
    #             {"key": "metadata_id", "match": {"value": ['metadata_id']}}
    #         ]
    #     }
    # )
    #
    # for point in results[0]:
    #     print(point.payload)