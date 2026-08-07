import React, { useEffect, useState } from "react";

import {
  FileText,
  Database,
  Upload,
  Loader2,
  CheckCircle,
  AlertCircle,
  Trash2,
} from "lucide-react";

function Documents() {
  const [documents, setDocuments] = useState([]);

  const [selectedFile, setSelectedFile] = useState(null);

  const [uploading, setUploading] = useState(false);

  const [deleting, setDeleting] = useState("");

  const [message, setMessage] = useState("");

  const [error, setError] = useState("");

  // =========================
  // Fetch Documents
  // =========================

  async function fetchDocuments() {
    try {
      const response = await fetch("http://127.0.0.1:5000/documents");

      if (!response.ok) throw new Error("Failed to fetch documents");

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
        throw new Error(data.error || "Upload failed");
      }

      setMessage(
        `${data.document} indexed successfully. ${data.chunks} chunks added.`,
      );

      setSelectedFile(null);

      await fetchDocuments();
    } catch (error) {
      setError(error.message);
    } finally {
      setUploading(false);
    }
  }

  // =========================
  // Delete Document
  // =========================

  async function handleDelete(name) {
    const confirmDelete = window.confirm(`Delete ${name}?`);

    if (!confirmDelete) return;

    setDeleting(name);

    setMessage("");

    setError("");

    try {
      const response = await fetch(`http://127.0.0.1:5000/documents/${name}`, {
        method: "DELETE",
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Delete failed");
      }

      setMessage(`${name} deleted successfully`);

      await fetchDocuments();
    } catch (error) {
      setError(error.message);
    } finally {
      setDeleting("");
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
      {/* HEADER */}

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

      {/* UPLOAD CARD */}

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
            <Upload size={22} className="text-amber-700" />
          </div>

          <div>
            <h2
              className="
              text-xl
              font-semibold
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
              Add a PDF to knowledge base.
            </p>
          </div>
        </div>

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
          transition
          "
        >
          <input
            type="file"
            accept=".pdf"
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
            <p className="font-medium">{selectedFile.name}</p>
          ) : (
            <p>Choose PDF file</p>
          )}
        </label>

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
          text-white
          flex
          gap-3
          items-center
          "
        >
          {uploading ? (
            <>
              <Loader2 size={18} className="animate-spin" />
              Indexing...
            </>
          ) : (
            <>
              <Upload size={18} />
              Upload & Index
            </>
          )}
        </button>

        {message && (
          <div
            className="
          mt-5
          bg-green-50
          text-green-700
          p-4
          rounded-xl
          flex
          gap-2
          "
          >
            <CheckCircle size={20} />

            {message}
          </div>
        )}

        {error && (
          <div
            className="
          mt-5
          bg-red-50
          text-red-700
          p-4
          rounded-xl
          flex
          gap-2
          "
          >
            <AlertCircle size={20} />

            {error}
          </div>
        )}
      </div>

      {/* DOCUMENT CARDS */}

      <div>
        <div
          className="
        flex
        justify-between
        mb-5
        "
        >
          <h2
            className="
          text-xl
          font-bold
          "
          >
            Indexed Documents
          </h2>

          <span
            className="
          bg-stone-100
          px-3
          py-1
          rounded-full
          text-sm
          "
          >
            {documents.length}
          </span>
        </div>

        <div
          className="
        grid
        sm:grid-cols-2
        lg:grid-cols-3
        gap-5
        "
        >
          {documents.map((doc) => (
            <div
              key={doc.name}
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
                  <FileText className="text-amber-700" />
                </div>

                <button
                  onClick={() => handleDelete(doc.name)}
                  disabled={deleting === doc.name}
                  className="
              p-2
              rounded-xl
              bg-red-50
              text-red-600
              hover:bg-red-100
              "
                >
                  {deleting === doc.name ? (
                    <Loader2 size={18} className="animate-spin" />
                  ) : (
                    <Trash2 size={18} />
                  )}
                </button>
              </div>

              <h3
                className="
            mt-5
            font-semibold
            break-words
            "
              >
                {doc.name}
              </h3>

              <div
                className="
            mt-4
            flex
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
      </div>
    </div>
  );
}

export default Documents;
