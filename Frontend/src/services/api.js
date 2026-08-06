const API_URL = "http://127.0.0.1:5000";

export async function askAssistant(query) {
  const response = await fetch(`${API_URL}/ask`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({
      query,
    }),
  });

  return response.json();
}
