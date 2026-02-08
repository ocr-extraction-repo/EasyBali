import os
import pinecone
from pinecone import ServerlessSpec
from app.settings.config import settings

def get_index(index_name: str, dimension: int = 1536, metric: str = "cosine") -> pinecone.Index:
    pinecone_api_key = settings.pinecone_api_key
    pinecone_region = settings.pinecone_region
    pinecone_cloud = settings.pinecone_cloud

    pc = pinecone.Pinecone(api_key=pinecone_api_key)

    existing_indexes = pc.list_indexes().names()
    if index_name not in existing_indexes:
        pc.create_index(
            name=index_name,
            dimension=dimension,
            metric=metric,
            spec=ServerlessSpec(cloud=pinecone_cloud, region=pinecone_region)
        )
    
    # Return the index object.
    return pc.Index(index_name)
