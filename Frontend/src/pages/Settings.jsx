import React from "react";

function Settings() {
  return (
    <div className="space-y-8">
      <h1
        className="
text-3xl
font-bold
text-stone-900
"
      >
        System Configuration
      </h1>

      <div
        className="
grid
md:grid-cols-2
gap-6
"
      >
        <Card
          title="Architecture"
          items={[
            "PDF Upload Pipeline",
            "Document Cleaning",
            "Semantic Chunking",
            "Metadata Enrichment",
            "Persona Embedding Generation",
            "Hybrid Retrieval",
            "Grounded Generation",
          ]}
        />

        <Card
          title="Retrieval Engine"
          items={[
            "Dense Vector Search",
            "BM25 Keyword Search",
            "Hybrid Score Fusion",
            "FAISS Vector Index",
            "Cosine Similarity Ranking",
          ]}
        />

        <Card
          title="AI Models"
          items={[
            "Embedding: all-MiniLM-L6-v2",
            "Embedding Dimension: 384",
            "Sentence Transformer Based Matching",
            "LLM Grounded Generation",
          ]}
        />

        <Card
          title="Pipeline Configuration"
          items={[
            "Top-K Retrieval Enabled",
            "Metadata Source Tracking",
            "Incremental Vector Updates",
            "Document Level Understanding",
          ]}
        />

        <Card
          title="Evaluation / System Metrics"
          items={[
            "Retriever: Hybrid",
            "Vector Store: FAISS",
            "Similarity: Cosine Similarity",
            "Generation: Evidence Grounded",
            "Hallucination Control: Context Only",
          ]}
        />

        <Card
          title="Supported Features"
          items={[
            "Multiple PDF Upload",
            "Dynamic Personas",
            "Conversation History",
            "Source Attribution",
            "Document Intelligence",
          ]}
        />
      </div>
    </div>
  );
}

function Card({ title, items }) {
  return (
    <div
      className="
bg-white
border
rounded-2xl
p-6
shadow-sm
"
    >
      <h2
        className="
text-xl
font-semibold
text-stone-900
"
      >
        {title}
      </h2>

      <ul
        className="
mt-4
space-y-2
text-stone-600
"
      >
        {items.map((item, index) => (
          <li key={index}>• {item}</li>
        ))}
      </ul>
    </div>
  );
}

export default Settings;
