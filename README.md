# Multi-agent RAG Reporting and Dashboard System

## 專案概述
本專案旨在設計並實現一個輕量級的 AI 系統，該系統能夠自動化地從零售數據庫中提取數據，並生成基於事實、帶有引用的 Excel 報告和互動式網頁儀表板。此系統特別適用於需要快速獲取業務洞察的零售連鎖企業。

## 專案目標
*   從零售數據庫讀取最新的退貨與保固數據。
*   透過多代理協同和 RAG (Retrieval-Augmented Generation) 技術，生成帶有明確引用的敘述性洞察。
*   自動化生成結構化的 Excel 報告（包含表格和圖表）。
*   自動化生成互動式網頁儀表板（包含條形圖、折線圖及敘述性摘要）。

## 架構設計
本系統採用高層次的多代理架構，確保模組化、靈活性和可擴展性。核心組件包括：
*   **數據獲取代理 (Data Fetcher Agent)**：負責從零售數據庫提取原始數據。
*   **報告代理 (Report Agent)**：協調整個報告生成流程，接收用戶查詢，並對原始數據進行正規化處理。
*   **RAG 核心 (RAG Core)**：系統的智能核心，負責將原始數據轉化為可檢索的向量，並根據查詢檢索相關信息，結合大型語言模型生成洞察。
*   **Excel 代理 (Excel Agent)**：專注於將洞察和數據轉化為 Excel 報告。
*   **儀表板代理 (Dashboard Agent)**：專注於生成互動式網頁儀表板。
*   **用戶界面 (User Interface)**：提供用戶與系統交互的入口。

詳細的架構圖請參考 `RAG零售.mmd` 檔案。

## 技術深度與實踐細節
本系統的 RAG 核心設計融入了多項先進技術與實踐：

### 1. 數據攝取與嵌入 (Data Ingestion & Embedding)
*   **數據處理**：原始數據經過清洗、標準化，並採用語義分塊策略切分為可管理的「塊」(chunks)，同時提取關鍵元數據。
*   **嵌入模型**：選用如 Google Universal Sentence Encoder 或 OpenAI text-embedding-ada-002 等預訓練的 Transformer-based 嵌入模型，確保生成高質量、語義豐富的向量嵌入，為精準檢索奠定基礎。

### 2. 向量資料庫 (Vector Database)
*   **高效儲存與檢索**：採用專用向量資料庫（如 Pinecone, ChromaDB, Weaviate），利用 HNSW 等索引技術實現對海量高維向量的毫秒級近似最近鄰 (ANN) 搜索。
*   **元數據過濾**：結合元數據儲存，支持基於時間、產品類別等條件的精確過濾檢索。

### 3. 查詢處理與檢索 (Query Processing & Retrieval)
*   **向量空間一致性**：用戶查詢使用與數據攝取階段相同的嵌入模型轉換為查詢向量。
*   **相似性搜索**：在向量資料庫中執行餘弦相似度搜索，檢索 Top-K 個語義最相關的數據塊。
*   **重排序 (Optional)**：可選地引入 Cross-Encoder 等重排序模型，對初步檢索結果進行二次評分，進一步提升相關性。

### 4. LLM 整合與響應生成 (LLM Integration & Response Generation)
*   **上下文學習**：檢索到的數據塊、用戶查詢和精心設計的系統提示一同送入大型語言模型（如 Gemini 系列模型）。
*   **提示工程**：運用思維鏈 (Chain-of-Thought) 等提示工程技術，引導 LLM 進行推理，並從提供的數據中生成帶有明確引用的敘述性洞察，有效降低「幻覺」現象。

## 技術棧
*   **圖表繪製**：Mermaid
*   **嵌入模型**：Google Universal Sentence Encoder / OpenAI text-embedding-ada-002 (示例)
*   **向量資料庫**：Pinecone / ChromaDB / Weaviate (示例)
*   **大型語言模型**：Gemini 系列模型 (示例)

## 檔案結構
*   `作業要求.txt`: 原始專案任務要求。
*   `設計說明.txt`: 詳細的系統設計選擇與技術實踐說明。
*   `RAG零售.mmd`: 系統的高層次多代理架構圖（Mermaid 格式）。
*   `RAG零售.png`: `RAG零售.mmd` 渲染後的圖像。
*   `README.md`: 本專案的概覽與說明 (即本文件)。

## 如何查看圖表
請使用支持 Mermaid 語法的 Markdown 渲染器（例如 GitHub、VS Code 的 Markdown 預覽）打開 `RAG零售.mmd` 檔案以查看系統架構圖。