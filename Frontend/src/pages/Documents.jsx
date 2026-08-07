import React, { useEffect, useState } from "react";

import {
  FileText,
  Database,
  Upload,
  Loader2,
  CheckCircle,
  AlertCircle,
} from "lucide-react";

function Documents() {
  const [documents, setDocuments] = useState([]);

  const [selectedFile, setSelectedFile] = useState(null);

  const [uploading, setUploading] = useState(false);

  const [message, setMessage] = useState("");

  const [error, setError] = useState("");

  // =========================
  // Fetch Documents
  // =========================

  async function fetchDocuments() {
    try {
      const response = await fetch("http://127.0.0.1:5000/documents");

      if (!response.ok) {
        throw new Error("Failed to fetch documents");
      }

      const data = await response.json();

      setDocuments(data.documents || []);
    } catch (error) {
      console.log(error);

      setError("Unable to load documents.");
    }
  }

  useEffect(() => {
    fetchDocuments();
  }, []);

  // =========================
  // File Selection
  // =========================

  function handleFileChange(event) {
    const file = event.target.files[0];

    setMessage("");

    setError("");

    if (!file) {
      setSelectedFile(null);

      return;
    }

    if (file.type !== "application/pdf") {
      setError("Please select a PDF file.");

      setSelectedFile(null);

      return;
    }

    setSelectedFile(file);
  }

  // =========================
  // Upload
  // =========================

  async function handleUpload() {
    if (!selectedFile) {
      setError("Please select a PDF first.");

      return;
    }

    setUploading(true);

    setMessage("");

    setError("");

    try {
      const formData = new FormData();

      formData.append("file", selectedFile);

      const response = await fetch("http://127.0.0.1:5000/upload", {
        method: "POST",
        body: formData,
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Upload failed.");
      }

      setMessage(
        `${data.document} indexed successfully. ${data.chunks} chunks added.`,
      );

      setSelectedFile(null);

      // Refresh document list

      await fetchDocuments();
    } catch (error) {
      console.log(error);

      setError(error.message || "Something went wrong while uploading.");
    } finally {
      setUploading(false);
    }
  }

  return (
    <div
      className="
        max-w-6xl
        mx-auto
        space-y-8
      "
    >
      {/* =========================
          Header
      ========================= */}

      <div>
        <h1
          className="
            text-3xl
            font-bold
            text-stone-800
          "
        >
          Documents
        </h1>

        <p
          className="
            mt-2
            text-stone-500
          "
        >
          Upload and manage documents indexed by Persona RAG.
        </p>
      </div>

      {/* =========================
          Upload Section
      ========================= */}

      <div
        className="
          bg-white
          border
          border-stone-200
          rounded-3xl
          p-6
          shadow-sm
        "
      >
        <div
          className="
            flex
            items-center
            gap-3
            mb-6
          "
        >
          <div
            className="
              p-3
              rounded-xl
              bg-amber-100
            "
          >
            <Upload
              size={22}
              className="
                text-amber-700
              "
            />
          </div>

          <div>
            <h2
              className="
                text-xl
                font-semibold
                text-stone-800
              "
            >
              Upload Document
            </h2>

            <p
              className="
                text-sm
                text-stone-500
              "
            >
              Add a PDF to the RAG knowledge base.
            </p>
          </div>
        </div>

        {/* File Picker */}

        <label
          className="
            block
            border-2
            border-dashed
            border-stone-300
            rounded-2xl
            p-8
            text-center
            cursor-pointer
            hover:border-amber-500
            hover:bg-amber-50/40
            transition
          "
        >
          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={handleFileChange}
            className="hidden"
          />

          <FileText
            size={42}
            className="
              mx-auto
              text-stone-400
              mb-3
            "
          />

          {selectedFile ? (
            <>
              <p
                className="
                  font-medium
                  text-stone-800
                "
              >
                {selectedFile.name}
              </p>

              <p
                className="
                  text-sm
                  text-stone-500
                  mt-1
                "
              >
                Ready to upload
              </p>
            </>
          ) : (
            <>
              <p
                className="
                  font-medium
                  text-stone-700
                "
              >
                Choose a PDF file
              </p>

              <p
                className="
                  text-sm
                  text-stone-400
                  mt-1
                "
              >
                PDF documents only
              </p>
            </>
          )}
        </label>

        {/* Upload Button */}

        <button
          onClick={handleUpload}
          disabled={!selectedFile || uploading}
          className="
            mt-5
            px-6
            py-3
            rounded-xl
            bg-amber-600
            hover:bg-amber-700
            disabled:bg-stone-300
            disabled:cursor-not-allowed
            text-white
            font-medium
            flex
            items-center
            gap-3
            transition
          "
        >
          {uploading ? (
            <>
              <Loader2
                size={18}
                className="
                  animate-spin
                "
              />
              Indexing Document...
            </>
          ) : (
            <>
              <Upload size={18} />
              Upload & Index
            </>
          )}
        </button>

        {/* Success */}

        {message && (
          <div
            className="
              mt-5
              flex
              items-start
              gap-3
              rounded-xl
              bg-green-50
              border
              border-green-200
              p-4
              text-green-700
              text-sm
            "
          >
            <CheckCircle
              size={20}
              className="
                shrink-0
              "
            />

            <span>{message}</span>
          </div>
        )}

        {/* Error */}

        {error && (
          <div
            className="
              mt-5
              flex
              items-start
              gap-3
              rounded-xl
              bg-red-50
              border
              border-red-200
              p-4
              text-red-700
              text-sm
            "
          >
            <AlertCircle
              size={20}
              className="
                shrink-0
              "
            />

            <span>{error}</span>
          </div>
        )}
      </div>

      {/* =========================
          Documents
      ========================= */}

      <div>
        <div
          className="
            flex
            items-center
            justify-between
            mb-5
          "
        >
          <div>
            <h2
              className="
                text-xl
                font-bold
                text-stone-800
              "
            >
              Indexed Documents
            </h2>

            <p
              className="
                text-sm
                text-stone-500
                mt-1
              "
            >
              Documents currently available to the RAG system.
            </p>
          </div>

          <span
            className="
              px-3
              py-1
              rounded-full
              bg-stone-100
              text-stone-600
              text-sm
            "
          >
            {documents.length} documents
          </span>
        </div>

        {documents.length === 0 ? (
          <div
            className="
              bg-white
              border
              border-stone-200
              rounded-3xl
              p-10
              text-center
            "
          >
            <FileText
              size={42}
              className="
                mx-auto
                text-stone-300
                mb-3
              "
            />

            <p
              className="
                text-stone-600
                font-medium
              "
            >
              No documents indexed yet.
            </p>

            <p
              className="
                text-stone-400
                text-sm
                mt-1
              "
            >
              Upload a PDF to get started.
            </p>
          </div>
        ) : (
          <div
            className="
              grid
              sm:grid-cols-2
              lg:grid-cols-3
              gap-5
            "
          >
            {documents.map((doc, index) => (
              <div
                key={index}
                className="
                      bg-white
                      border
                      border-stone-200
                      rounded-3xl
                      p-6
                      shadow-sm
                    "
              >
                <div
                  className="
                        flex
                        items-start
                        justify-between
                      "
                >
                  <div
                    className="
                          p-3
                          rounded-xl
                          bg-amber-100
                        "
                  >
                    <FileText
                      className="
                            text-amber-700
                          "
                    />
                  </div>

                  <span
                    className="
                          px-2.5
                          py-1
                          rounded-full
                          bg-green-50
                          text-green-700
                          text-xs
                          font-medium
                        "
                  >
                    {doc.status}
                  </span>
                </div>

                <h3
                  className="
                        mt-5
                        font-semibold
                        text-stone-800
                        break-words
                      "
                >
                  {doc.name}
                </h3>

                <div
                  className="
                        mt-4
                        flex
                        items-center
                        gap-2
                        text-sm
                        text-stone-500
                      "
                >
                  <Database size={17} />
                  {doc.chunks} chunks
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default Documents;
