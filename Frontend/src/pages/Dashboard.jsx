import React, { useEffect, useState } from "react";

import {
  Brain,
  FileText,
  Database,
  Search,
  ShieldCheck,
  UploadCloud,
} from "lucide-react";

import { getDocuments } from "../services/api.js";

function Dashboard() {
  const [documents, setDocuments] = useState([]);

  const [stats, setStats] = useState({
    documents: 0,
    chunks: 0,
  });

  useEffect(() => {
    async function load() {
      try {
        const response = await getDocuments();

        const docs = Array.isArray(response) ? response : [];

        setDocuments(docs);

        setStats({
          documents: docs.length,

          chunks: docs.reduce((sum, doc) => sum + Number(doc.chunks || 0), 0),
        });
      } catch (error) {
        console.error("Dashboard error", error);
      }
    }

    load();
  }, []);

  return (
    <div className="space-y-8">
      {/* HERO */}

      <section
        className="
rounded-3xl
bg-gradient-to-r
from-amber-100
via-orange-50
to-stone-100
border
border-amber-200
p-10
"
      >
        <div className="flex justify-between items-center flex-wrap gap-8">
          <div>
            <h1
              className="
text-4xl
font-bold
text-stone-900
"
            >
              Persona RAG
            </h1>

            <p
              className="
mt-3
max-w-2xl
text-stone-700
"
            >
              Document intelligence system combining PDF understanding, hybrid
              retrieval, dynamic persona detection and grounded AI generation.
            </p>

            <div
              className="
mt-5
flex
gap-3
flex-wrap
"
            >
              <Badge text="Hybrid Retrieval" />

              <Badge text="FAISS Vector Search" />

              <Badge text="Grounded LLM" />
            </div>
          </div>

          <div
            className="
w-28
h-28
rounded-3xl
bg-white
flex
items-center
justify-center
shadow-lg
"
          >
            <Brain size={55} className="text-amber-600" />
          </div>
        </div>
      </section>

      {/* STATS */}

      <div
        className="
grid
md:grid-cols-2
xl:grid-cols-4
gap-6
"
      >
        <StatCard title="Documents" value={stats.documents} icon={FileText} />

        <StatCard title="Indexed Chunks" value={stats.chunks} icon={Database} />

        <StatCard title="Retriever" value="Hybrid" icon={Search} />

        <StatCard title="Generation" value="Grounded" icon={ShieldCheck} />
      </div>

      <div
        className="
grid
lg:grid-cols-2
gap-6
"
      >
        {/* DOCUMENTS */}

        <div
          className="
bg-white
border
rounded-2xl
p-6
shadow-sm
"
        >
          <h2 className="text-xl font-semibold">Latest Documents</h2>

          <div className="mt-5 space-y-3">
            {documents.length === 0 ? (
              <div
                className="
text-stone-500
flex
gap-2
"
              >
                <UploadCloud size={20} />
                No documents uploaded
              </div>
            ) : (
              documents.slice(0, 5).map((doc, index) => (
                <div
                  key={index}
                  className="
border
rounded-xl
p-4
"
                >
                  <h3
                    className="
font-medium
text-stone-900
"
                  >
                    {doc.name}
                  </h3>

                  <p className="text-sm text-stone-600 mt-1">
                    Chunks:
                    {doc.chunks}
                  </p>

                  <p className="text-sm text-amber-600 mt-1">
                    Persona:
                    {doc.persona?.persona || "Generated dynamically"}
                  </p>
                </div>
              ))
            )}
          </div>
        </div>

        {/* RETRIEVAL */}

        <div
          className="
bg-white
border
rounded-2xl
p-6
shadow-sm
"
        >
          <h2 className="text-xl font-semibold">System Capabilities</h2>

          <div
            className="
mt-5
space-y-3
text-stone-600
"
          >
            <p>✓ Semantic Embedding Retrieval</p>

            <p>✓ BM25 Keyword Retrieval</p>

            <p>✓ Hybrid Score Fusion</p>

            <p>✓ Document Metadata Tracking</p>

            <p>✓ Persona Based Response Style</p>

            <p>✓ Source Grounded Answers</p>
          </div>
        </div>
      </div>

      <div
        className="
grid
lg:grid-cols-2
gap-6
"
      >
        <Feature
          title="Document Intelligence"
          text="PDF extraction, cleaning, semantic chunking and metadata enrichment create searchable document knowledge."
        />

        <Feature
          title="Persona Engine"
          text="The system dynamically adapts response style according to query intent and document context."
        />

        <Feature
          title="Retrieval Pipeline"
          text="Dense embeddings and BM25 retrieval work together to improve relevant context selection."
        />

        <Feature
          title="Safety Layer"
          text="Responses are generated only from retrieved evidence to reduce hallucination."
        />
      </div>
    </div>
  );
}

function StatCard({ title, value, icon: Icon }) {
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
      <Icon size={30} className="text-amber-600" />

      <p className="mt-5 text-sm text-stone-500">{title}</p>

      <h2 className="text-3xl font-bold mt-2">{value}</h2>
    </div>
  );
}

function Feature({ title, text }) {
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
      <h2 className="text-xl font-semibold">{title}</h2>

      <p
        className="
mt-3
text-stone-600
leading-7
"
      >
        {text}
      </p>
    </div>
  );
}

function Badge({ text }) {
  return (
    <span
      className="
px-3
py-1
rounded-full
bg-white
border
text-sm
text-stone-700
"
    >
      {text}
    </span>
  );
}

export default Dashboard;
