import React from "react";

import {
  Brain,
  FileText,
  Database,
  MessageSquare,
  ArrowRight,
} from "lucide-react";

function Dashboard() {
  return (
    <div className="space-y-8">

      {/* Hero */}

      <section
        className="
          rounded-3xl
          bg-gradient-to-r
          from-amber-100
          via-orange-50
          to-stone-100

          p-10

          border
          border-amber-200
        "
      >

        <div className="flex justify-between items-center flex-wrap gap-8">

          <div>

            <h1 className="text-4xl font-bold text-stone-900">
              Persona RAG
            </h1>

            <p className="mt-3 text-stone-700 max-w-2xl">

              AI-powered document intelligence with
              Persona Detection, Hybrid Retrieval,
              Context Building and LLM generation.

            </p>

          </div>

          <div
            className="
              w-24
              h-24

              rounded-3xl

              bg-white

              flex
              items-center
              justify-center

              shadow-lg
            "
          >

            <Brain
              size={48}
              className="text-amber-600"
            />

          </div>

        </div>

      </section>

      {/* Stats */}

      <div
        className="
          grid
          gap-6

          md:grid-cols-2
          xl:grid-cols-4
        "
      >

        <StatCard
          title="Indexed Documents"
          value="9"
          icon={FileText}
        />

        <StatCard
          title="Document Chunks"
          value="107"
          icon={Database}
        />

        <StatCard
          title="Retriever"
          value="Hybrid"
          icon={Brain}
        />

        <StatCard
          title="API"
          value="Running"
          icon={MessageSquare}
        />

      </div>

      {/* Features */}

      <div
        className="
          grid
          lg:grid-cols-2
          gap-6
        "
      >

        <Feature
          title="Hybrid Retrieval"

          text="
Dense embeddings and BM25
work together to retrieve
highly relevant document chunks."

        />

        <Feature
          title="Persona Detection"

          text="
Automatically detects the user's
intent and generates answers in
an appropriate style."

        />

        <Feature
          title="Grounded Responses"

          text="
Answers are generated only from
retrieved document evidence,
reducing hallucinations."

        />

        <Feature
          title="Source Attribution"

          text="
Every answer contains the
document, section and pages
used for generation."

        />

      </div>

    </div>
  );
}

function StatCard({
  title,
  value,
  icon: Icon,
}) {
  return (

    <div
      className="
        bg-white

        rounded-2xl

        border
        border-stone-200

        p-6

        shadow-sm
      "
    >

      <div className="flex justify-between items-center">

        <Icon
          className="text-amber-600"
          size={28}
        />

        <ArrowRight
          size={18}
          className="text-stone-400"
        />

      </div>

      <h3 className="mt-6 text-sm text-stone-500">
        {title}
      </h3>

      <p className="text-3xl font-bold mt-2 text-stone-900">
        {value}
      </p>

    </div>

  );
}

function Feature({
  title,
  text,
}) {
  return (

    <div
      className="
        bg-white

        rounded-2xl

        border
        border-stone-200

        p-6

        shadow-sm
      "
    >

      <h2 className="font-semibold text-xl text-stone-900">
        {title}
      </h2>

      <p className="mt-3 text-stone-600 leading-7">
        {text}
      </p>

    </div>

  );
}

export default Dashboard;