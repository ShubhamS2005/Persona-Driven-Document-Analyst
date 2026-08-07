export function saveHistory(item) {
  let history = JSON.parse(localStorage.getItem("history")) || [];

  history.unshift({
    ...item,

    time: new Date().toISOString(),
  });

  localStorage.setItem("history", JSON.stringify(history));
}

export function getHistory() {
  return JSON.parse(localStorage.getItem("history")) || [];
}
