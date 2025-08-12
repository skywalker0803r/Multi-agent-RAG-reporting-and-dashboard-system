from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.core.rag import get_embedding, get_pinecone_index, get_llm_response
from app.db.models import ReturnWarrantyData # Import your model
from sqlalchemy import select

class ReportService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.pinecone_index_name = "retail-data-index" # Placeholder index name
        self.pinecone_index = get_pinecone_index(self.pinecone_index_name)

    async def _get_data_from_db(self, limit: int = 100):
        """Helper to fetch some data from the database."""
        # This is a placeholder. In a real app, you'd filter/query based on needs.
        result = await self.db.execute(select(ReturnWarrantyData).limit(limit))
        return result.scalars().all()

    async def generate_excel_report(self, query: str) -> str:
        print(f"Generating Excel report for query: {query}")

        # Example: Fetch some data from the database (for context or initial analysis)
        # raw_data_from_db = await self._get_data_from_db(limit=10)
        # print(f"Fetched {len(raw_data_from_db)} items from DB.")

        # 1. Process query (embed it)
        query_embedding = get_embedding(query)

        # 2. Search vector DB for relevant data
        # In a real scenario, you might add filters here based on query intent or metadata
        search_results = self.pinecone_index.query(
            vector=query_embedding,
            top_k=5, # Retrieve top 5 most relevant chunks
            include_metadata=True
        )

        context = ""
        if search_results.matches:
            context = "\n".join([match.metadata['original_text'] for match in search_results.matches if 'original_text' in match.metadata])
        
        if not context:
            context = "No relevant context found in the database."

        # 3. Integrate with LLM to generate insights
        llm_prompt = f"Generate a detailed report based on the following query and context. Focus on key findings and provide actionable insights. Ensure to cite sources from the context if possible. Respond in Chinese.\nQuery: {query}"
        report_content = get_llm_response(llm_prompt, context)

        # 4. Format insights into Excel (Placeholder - actual Excel generation would be complex)
        report_path = f"./reports/report_{query.replace(' ', '_')}.txt" # Changed to .txt for simplicity
        # Ensure the 'reports' directory exists
        import os
        os.makedirs(os.path.dirname(report_path), exist_ok=True)
        with open(report_path, "w", encoding="utf-8") as f:
            f.write(report_content)
        
        print(f"Report saved to {report_path}")
        return report_path, report_content
