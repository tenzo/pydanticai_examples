from dataclasses import dataclass, field
from openai import AsyncOpenAI

from qdrant_client import AsyncQdrantClient, models


@dataclass
class VectorStore:
    """Vector store dependency for PydanticAI
    Bases on Qdrant and requires a server running Qdrant

    Attributes:
        url (str): URL of the Qdrant server
        port: (int): Port of the Qdrant server
        collection_name (str): Name of the collection to use
    """
    url: str
    port: int
    collection_name: str
    openai_api_key: str
    qdrant_client: AsyncQdrantClient = field(default=None, init=False)
    openai: AsyncOpenAI = field(default=None, init=False)

    def __post_init__(self):
        """Post init method to check if the URL and port are set"""
        if not self.url or not self.port:
            raise ValueError("URL and port must be set")
        self.client = AsyncQdrantClient(
            url=self.url,
            port=self.port,
        )
        self.openai = AsyncOpenAI(
            api_key=self.openai_api_key,
        )

    async def search(self, query: str, top_k: int = 5) -> list[dict]:
        """Search the vector store for the given query

        Args:
            query (str): Query to search for
            top_k (int): Number of results to return

        Returns:
            list[dict]: List of results
        """
        # Embed the query
        query_vector = await self._embed_query(query)
        response = await self.client.query_points(
            collection_name=self.collection_name,
            query=query_vector,
            limit=top_k,
        )
        documents = [hit.payload["document"] for hit in response.points]
        return documents

    async def _embed_query(self, query: str) -> list[float]:
        """Embed the query using OpenAI

        Returns:
            list[float]: List of embeddings
        """
        response = await self.openai.embeddings.create(
            input=query,
            model="text-embedding-3-small",
        )
        return response.data[0].embedding
