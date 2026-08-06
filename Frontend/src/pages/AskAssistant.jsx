import React, { useState } from "react";

import { Send, Brain, Loader2, User } from "lucide-react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

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

    try {
      const response = await fetch(
        "http://127.0.0.1:5000/ask",

        {
          method: "POST",

          headers: {
            "Content-Type": "application/json",
          },

          body: JSON.stringify({
            query: userMessage,
          }),
        },
      );

      const data = await response.json();

      setMessages((prev) => [
        ...prev,

        {
          role: "assistant",

          text: data.answer,
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
      {/* Header */}

      <div
        className="
        bg-white

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
          gap-3
          "
        >
          <div
            className="
            p-3
            rounded-2xl

            bg-amber-100
            "
          >
            <Brain size={28} className="text-amber-700" />
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
              Ask questions from your indexed documents
            </p>
          </div>
        </div>
      </div>

      {/* Chat Area */}

      <div
        className="
        flex-1

        overflow-y-auto

        space-y-5

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
            <div
              className={`
              
              max-w-[80%]

              rounded-3xl

              px-6

              py-5


              ${
                msg.role === "user"
                  ? "bg-amber-600 text-white"
                  : "bg-white border border-stone-200 text-stone-700 shadow-sm"
              }

              `}
            >
              <div
                className="
              flex
              items-center
              gap-2
              mb-3
              "
              >
                {msg.role === "user" ? <User size={18} /> : <Brain size={18} />}

                <span
                  className="
              text-sm
              font-semibold
              "
                >
                  {msg.role === "user" ? "You" : "Persona RAG"}
                </span>
              </div>

              <div
                className="
prose
prose-stone
max-w-none

text-sm

leading-8
"
              >
                <ReactMarkdown
                  remarkPlugins={[remarkGfm]}
                  components={{
                    h1: ({ children }) => (
                      <h1
                        className="
text-2xl
font-bold
text-stone-800
mt-4
mb-3
"
                      >
                        {children}
                      </h1>
                    ),

                    h2: ({ children }) => (
                      <h2
                        className="
text-xl
font-bold
text-stone-800
mt-5
mb-3
"
                      >
                        {children}
                      </h2>
                    ),

                    h3: ({ children }) => (
                      <h3
                        className="
text-lg
font-semibold
text-amber-700
mt-4
"
                      >
                        {children}
                      </h3>
                    ),

                    strong: ({ children }) => (
                      <strong
                        className="
font-bold
text-stone-900
"
                      >
                        {children}
                      </strong>
                    ),

                    li: ({ children }) => (
                      <li
                        className="
ml-5
mb-3
"
                      >
                        {children}
                      </li>
                    ),
                  }}
                >
                  {msg.text}
                </ReactMarkdown>
              </div>
            </div>
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

            border-stone-200

            rounded-3xl

            px-6

            py-4

            flex

            items-center

            gap-3
            "
            >
              <Loader2 size={18} className="animate-spin text-amber-600" />

              <span
                className="
              text-stone-500
              "
              >
                Thinking...
              </span>
            </div>
          </div>
        )}
      </div>

      {/* Input */}

      <div
        className="
        mt-5

        bg-white

        rounded-3xl

        border

        border-stone-200

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
          placeholder="Ask something about your documents..."
          className="
        flex-1

        resize-none

        h-20

        rounded-2xl

        p-4

        outline-none

        bg-stone-50

        border

        border-stone-200

        focus:ring-2

        focus:ring-amber-400

        "
        />

        <button
          onClick={askQuestion}
          className="
        self-end

        p-4

        rounded-2xl

        bg-amber-600

        hover:bg-amber-700

        text-white

        transition

        "
        >
          {loading ? (
            <Loader2 size={20} className="animate-spin" />
          ) : (
            <Send size={20} />
          )}
        </button>
      </div>
    </div>
  );
}

export default AskAssistant;
