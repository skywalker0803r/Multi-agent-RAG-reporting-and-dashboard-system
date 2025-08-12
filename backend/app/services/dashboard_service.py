from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.core.rag import get_embedding, get_pinecone_index, get_llm_response
from app.db.models import ReturnWarrantyData # Import your model
from sqlalchemy import select

class DashboardService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db
        self.pinecone_index_name = "retail-data-index" # Placeholder index name
        self.pinecone_index = get_pinecone_index(self.pinecone_index_name)

    async def _get_data_from_db(self, limit: int = 100):
        """Helper to fetch some data from the database."""
        # This is a placeholder. In a real app, you'd filter/query based on needs.
        result = await self.db.execute(select(ReturnWarrantyData).limit(limit))
        return result.scalars().all()

    

    def _parse_metadata_for_charts(self, matches: list) -> list:
        """
        Parses Pinecone match metadata to extract data for charts.
        This version is tailored to the retail_sales_dataset.csv and warranty-claims.csv metadata.
        """
        charts_data = []

        # Data structures for aggregation
        monthly_sales = {} # { 'YYYY-MM': total_price }
        sales_by_category = {} # { 'Category': total_price }
        warranty_status_counts = {} # { 'Status': count }

        for match in matches:
            metadata = match.metadata

            # Process retail_sales_dataset.csv data
            if 'Date' in metadata and 'Total Price' in metadata and 'Product Category' in metadata:
                try:
                    # For monthly sales
                    date_str = metadata['Date'] # Assuming 'YYYY-MM-DD'
                    month_year = date_str[:7] # Extract 'YYYY-MM'
                    total_price = float(metadata['Total Price'])
                    monthly_sales[month_year] = monthly_sales.get(month_year, 0.0) + total_price

                    # For sales by category
                    category = metadata['Product Category']
                    sales_by_category[category] = sales_by_category.get(category, 0.0) + total_price
                except (ValueError, TypeError) as e:
                    print(f"Error parsing retail sales metadata: {metadata}. Error: {e}")
                    continue

            # Process warranty-claims.csv data
            if 'Status' in metadata:
                status = metadata['Status']
                warranty_status_counts[status] = warranty_status_counts.get(status, 0) + 1

        # Generate charts from aggregated data

        # Monthly Sales Chart (Line or Bar)
        if monthly_sales:
            sorted_months = sorted(monthly_sales.keys())
            sales_values = [monthly_sales[month] for month in sorted_months]
            charts_data.append({
                "type": "line", # Line chart for time series
                "labels": sorted_months,
                "data": sales_values,
                "title": "Monthly Sales Trends"
            })

        # Sales by Product Category Chart (Bar or Pie)
        if sales_by_category:
            categories = list(sales_by_category.keys())
            sales_values = [sales_by_category[cat] for cat in categories]
            charts_data.append({
                "type": "bar", # Bar chart for categorical comparison
                "labels": categories,
                "data": sales_values,
                "title": "Sales by Product Category"
            })

        # Warranty Status Counts Chart (Bar or Pie)
        if warranty_status_counts:
            statuses = list(warranty_status_counts.keys())
            counts = [warranty_status_counts[status] for status in statuses]
            charts_data.append({
                "type": "pie", # Pie chart for proportions
                "labels": statuses,
                "data": counts,
                "title": "Warranty Claim Status Distribution"
            })

        return charts_data

    async def get_dashboard_data(self, query: str):

        # Example: Fetch some data from the database (for context or initial analysis)
        # raw_data_from_db = await self._get_data_from_db(limit=10)
        # print(f"Fetched {len(raw_data_from_db)} items from DB.")

        # 1. Process query (embed it)
        query_embedding = get_embedding(query)

        # 2. Search vector DB for relevant data
        search_results = self.pinecone_index.query(
            vector=query_embedding,
                        top_k=50, # Retrieve top 50 most relevant chunks
            include_metadata=True
        )

        context = ""
        if search_results.matches:
            context = "\n".join([match.metadata['original_text'] for match in search_results.matches if 'original_text' in match.metadata])

        if not context:
            context = "No relevant context found in the database."

        # 3. Integrate with LLM to generate insights/summaries for dashboard
        llm_prompt = f"Generate a concise summary and key insights for a dashboard based on the following query and context. Provide data points if available in context. Focus on actionable insights. Respond in Chinese.\nQuery: {query}"
        narrative_insights = get_llm_response(llm_prompt, context)

        # Extract data for charts from Pinecone search results metadata
        charts_data = self._parse_metadata_for_charts(search_results.matches)

        data = {
            "title": f"Dashboard for {query}",
            "charts": charts_data,
            "narrative_insights": narrative_insights
        }
        return data
