import React, { useState } from "react";

import { Send, Brain, Loader2, User, FileText } from "lucide-react";

import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import logo from "../assets/logo.png";

function AskAssistant() {
  const [query, setQuery] = useState("");

  const [loading, setLoading] = useState(false);

  const [messages, setMessages] = useState([]);

  async function askQuestion() {
    if (!query.trim()) return;

    const userMessage = query;

    setMessages((prev) => [
      ...prev,
      {
        role: "user",
        text: userMessage,
      },
    ]);

    setQuery("");

    setLoading(true);
    const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:5000";

    try {
      const response = await fetch(`${API_URL}/ask`, {
        method: "POST",

        headers: {
          "Content-Type": "application/json",
        },

        body: JSON.stringify({
          query: userMessage,
        }),
      });

      const data = await response.json();

      setMessages((prev) => [
        ...prev,

        {
          role: "assistant",

          text: data.answer,

          persona: data.persona,

          sources: data.sources || [],
        },
      ]);
    } catch (error) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          text: "Unable to connect with Persona RAG API.",
        },
      ]);
    }

    setLoading(false);
  }

  return (
    <div
      className="
max-w-5xl
mx-auto

h-[calc(100vh-120px)]

flex
flex-col
"
    >
      {/* HEADER */}

      <div
        className="
bg-gradient-to-r
from-stone-50
to-amber-50

rounded-3xl

border
border-stone-200

shadow-sm

p-6

mb-5
"
      >
        <div
          className="
flex
items-center
gap-4
"
        >
          <div
            className="
p-3

rounded-2xl

bg-amber-100
"
          >
            <img
              src={logo}
              className="
 w-16
 h-16
 object-contain
 "
            />
          </div>

          <div>
            <h1
              className="
text-2xl
font-bold
text-stone-800
"
            >
              Persona RAG Assistant
            </h1>

            <p
              className="
text-sm
text-stone-500
"
            >
              AI powered document historian
            </p>
          </div>
        </div>
      </div>

      {/* CHAT AREA */}

      <div
        className="
flex-1

overflow-y-auto

space-y-6

pr-2
"
      >
        {messages.map((msg, index) => (
          <div
            key={index}
            className={`
flex

${msg.role === "user" ? "justify-end" : "justify-start"}

`}
          >
            {/* USER MESSAGE */}

            {msg.role === "user" ? (
              <div
                className="
max-w-[75%]

bg-amber-600

text-white

rounded-3xl

px-6

py-4

shadow-sm
"
              >
                <div
                  className="
flex
gap-2
items-center

mb-2
"
                >
                  <User size={18} />

                  <span
                    className="
font-semibold
text-sm
"
                  >
                    You
                  </span>
                </div>

                <p>{msg.text}</p>
              </div>
            ) : (
              /* ASSISTANT */

              <div
                className="
max-w-[85%]

bg-white

border

border-stone-200

rounded-3xl

shadow-sm

p-6
"
              >
                {/* Persona */}

                <div
                  className="
flex
items-center
justify-between

mb-5
"
                >
                  <div
                    className="
flex
items-center
gap-3
"
                  >
                    <div
                      className="
p-2
rounded-xl

bg-amber-100
"
                    >
                      <Brain size={20} className="text-amber-700" />
                    </div>

                    <div>
                      <h3
                        className="
font-bold
text-stone-800
"
                      >
                        {msg.persona?.name || "Persona RAG"}
                      </h3>
                    </div>
                  </div>
                </div>

                {/* ANSWER */}

                <div
                  className="
prose

prose-stone

max-w-none

leading-8

text-sm
"
                >
                  <ReactMarkdown remarkPlugins={[remarkGfm]}>
                    {msg.text}
                  </ReactMarkdown>
                </div>

                {/* SOURCES */}

                {msg.sources && msg.sources.length > 0 && (
                  <div
                    className="
mt-6

border-t

border-stone-200

pt-5
"
                  >
                    <h4
                      className="
font-bold

text-stone-800

mb-4

flex

items-center

gap-2
"
                    >
                      <FileText size={18} />
                      Sources
                    </h4>

                    <div
                      className="
space-y-3
"
                    >
                      {msg.sources.map((source, i) => (
                        <div
                          key={i}
                          className="
bg-stone-50

border

border-stone-200

rounded-2xl

p-4
"
                        >
                          <p
                            className="
font-semibold
text-stone-800
"
                          >
                            📄 {source.document}
                          </p>

                          <p
                            className="
text-sm
text-stone-600
mt-1
"
                          >
                            Section:
                            {source.section || "N/A"}
                          </p>

                          <p
                            className="
text-xs
text-stone-500
mt-2
"
                          >
                            Pages:
                            {source.pages?.join("-")}
                            &nbsp; | &nbsp; Score:
                            {(source.score * 100).toFixed(1)}%
                          </p>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
              </div>
            )}
          </div>
        ))}

        {loading && (
          <div
            className="
flex
justify-start
"
          >
            <div
              className="
bg-white

border

rounded-3xl

px-6

py-4

flex

gap-3

items-center
"
            >
              <Loader2
                className="
animate-spin
text-amber-600
"
              />

              <span
                className="
text-stone-500
"
              >
                Searching documents...
              </span>
            </div>
          </div>
        )}
      </div>

      {/* INPUT */}

      <div
        className="
mt-5

bg-white

border

border-stone-200

rounded-3xl

shadow-sm

p-4

flex

gap-3
"
      >
        <textarea
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          onKeyDown={(e) => {
            if (e.key === "Enter" && !e.shiftKey) {
              e.preventDefault();

              askQuestion();
            }
          }}
          placeholder="
Ask from your documents...
"
          className="
flex-1

h-20

resize-none

rounded-2xl

bg-stone-50

border

border-stone-200

p-4

outline-none

focus:ring-2

focus:ring-amber-400
"
        />

        <button
          onClick={askQuestion}
          className="
bg-amber-600

hover:bg-amber-700

text-white

rounded-2xl

px-5

transition
"
        >
          {loading ? <Loader2 className="animate-spin" /> : <Send />}
        </button>
      </div>
    </div>
  );
}

export default AskAssistant;
