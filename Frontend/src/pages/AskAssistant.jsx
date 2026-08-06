import React, { useState } from "react";

import {
  Send,
  Brain,
  Loader2,
} from "lucide-react";

function AskAssistant() {

  const [query, setQuery] = useState("");

  const [loading, setLoading] = useState(false);

  const [answer, setAnswer] = useState("");

  async function askQuestion() {

    if (!query.trim())
      return;

    setLoading(true);

    try {

      const response = await fetch(
        "http://127.0.0.1:5000/ask",
        {
          method: "POST",

          headers: {
            "Content-Type":
              "application/json",
          },

          body: JSON.stringify({
            query,
          }),
        }
      );

      const data =
        await response.json();

      setAnswer(data.answer);

    } catch (err) {

      console.log(err);

    }

    setLoading(false);

  }

  return (

    <div
      className="
        max-w-5xl
        mx-auto

        space-y-6
      "
    >

      <div
        className="
          bg-white

          rounded-3xl

          border
          border-stone-200

          shadow-sm

          p-8
        "
      >

        <div className="flex items-center gap-3">

          <Brain
            className="text-amber-600"
            size={28}
          />

          <h1 className="text-2xl font-bold">
            Ask Persona RAG
          </h1>

        </div>

        <p className="mt-2 text-stone-600">

          Ask questions from your indexed
          documents.

        </p>

        <textarea

          value={query}

          onChange={(e)=>
            setQuery(e.target.value)
          }

          placeholder="
Example:
Explain medieval architecture
of Carcassonne."

          className="
            mt-6

            w-full

            h-44

            rounded-2xl

            border
            border-stone-300

            p-5

            resize-none

            outline-none

            focus:ring-2

            focus:ring-amber-500
          "
        />

        <button

          onClick={askQuestion}

          className="
            mt-5

            px-6
            py-3

            rounded-xl

            bg-amber-600

            hover:bg-amber-700

            text-white

            flex

            items-center

            gap-3

            transition
          "
        >

          {

            loading

            ?

            <Loader2
              className="animate-spin"
              size={18}
            />

            :

            <Send size={18}/>

          }

          Ask Assistant

        </button>

      </div>

      {

        answer &&

        <div
          className="
            bg-white

            rounded-3xl

            border
            border-stone-200

            p-8

            shadow-sm
          "
        >

          <h2
            className="
              font-bold

              text-xl

              mb-5
            "
          >
            Response
          </h2>

          <p
            className="
              whitespace-pre-wrap

              leading-8

              text-stone-700
            "
          >
            {answer}
          </p>

        </div>

      }

    </div>

  );
}

export default AskAssistant;