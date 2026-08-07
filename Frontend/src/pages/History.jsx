import React, { useEffect, useState } from "react";

import { FileText, Database, Clock } from "lucide-react";

import { getDocuments } from "../services/api";

function History() {
  const [docs, setDocs] = useState([]);

  useEffect(() => {
    async function load() {
      const data = await getDocuments();

      setDocs(Array.isArray(data) ? data : []);
    }

    load();
  }, []);

  return (
    <div className="space-y-8">
      <h1
        className="
text-3xl
font-bold
text-stone-900
"
      >
        Document History
      </h1>

      {docs.length === 0 ? (
        <div
          className="
bg-white
border
rounded-2xl
p-8
text-stone-500
"
        >
          No uploaded documents available.
        </div>
      ) : (
        <div
          className="
space-y-5
"
        >
          {docs.map((doc, index) => (
            <div
              key={index}
              className="
bg-white
border
rounded-2xl
p-6
shadow-sm
"
            >
              <div
                className="
flex
justify-between
flex-wrap
gap-3
"
              >
                <h2
                  className="
text-xl
font-semibold
flex
gap-2
items-center
"
                >
                  <FileText size={22} className="text-amber-600" />

                  {doc.name}
                </h2>

                <span
                  className="
text-sm
px-3
py-1
rounded-full
bg-green-100
text-green-700
"
                >
                  {doc.status || "indexed"}
                </span>
              </div>

              <div
                className="
mt-5
grid
md:grid-cols-3
gap-4
text-stone-600
"
              >
                <p>
                  <Database size={16} className="inline mr-2" />
                  Chunks:
                  {doc.chunks}
                </p>

                <p>
                  <Clock size={16} className="inline mr-2" />
                  {doc.uploaded}
                </p>

                <p>
                  Persona:
                  {doc.persona?.persona || "Dynamic"}
                </p>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default History;
