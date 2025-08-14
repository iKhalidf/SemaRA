# SemaRA – Semantic Retrieval for Arabic PDFs

SemaRA is a **Retrieval-Augmented Generation (RAG)** system designed to **chat and search within Arabic PDF documents** efficiently and securely.  
It enables organizations, professionals, and researchers to interact with their documents through **contextual AI-powered search**, without compromising privacy.

---

## ● Features

- **Arabic-First Processing** – Optimized for Arabic language tokenization, normalization, and semantic embeddings.
- **Full Privacy** – 100% local processing; no external API calls unless configured.
- **Fast Semantic Search** – Vector-based retrieval with ChromaDB for high-performance document queries.
- **Contextual Q&A** – LLM integration for answering queries based on extracted document context.
- **Scalable Architecture** – Supports large documents and multiple file uploads.

---

## ● Use Cases

- **Legal Teams** – Quickly retrieve clauses and legal terms from lengthy contracts.
- **Research & Academia** – Search through books, reports, or academic papers.
- **Business Intelligence** – Extract relevant insights from operational documents.

---

## ● Technical Overview

| Layer                | Implementation Details |
|----------------------|------------------------|
| **Data Sources**     | PDF, E-Books |
| **Preprocessing**    | Tokenization, normalization |
| **Vector Store**     | [ChromaDB](https://www.trychroma.com/) – lightweight, optimized for Arabic text |
| **Embedding Model**  | OpenAI `text-embedding-3-large` |
| **Indexing Strategy**| Chunking by 1000 characters or custom term-based indexing |
| **Search Method**    | Approximate Nearest Neighbors (ANN) |
| **LLM**              | OpenAI gpt-3.5-turbo-instruct |
| **Prompt Engineering**| Context injection, instructions, guardrails |
| **Privacy**          | Local deployment option ensures 100% control of data |

---

## ● Project Structure

```
SemaRA/
│
├── pages/               # the Q and A page
├── scripts/             # Data loading, preprocessing, indexing
├── rag_logic.py         # Retrieval and LLM query logic
├── requirements.txt     # Python dependencies
└── README.md            # Project documentation
```

---

## ● Setup & Installation

1. **Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/SemaRA.git
   cd SemaRA
   ```

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Add Your PDFs**
   Place your `.pdf` files inside the `data/` folder.

4. **Run the RAG Pipeline**
   ```bash
   python main.py
   ```

---

## ● Future Enhancements

-  Chain-of-thought reasoning over PDFs
-  Summarization & automated report generation
-  Multi-modal search (semantic + keyword + filters)

---

## 📜 License

This project is open-source under the **MIT License**.