export async function getOfflineResponse(prompt: string): Promise<string> {
  const res = await fetch("http://127.0.0.1:5000/api/respond", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ prompt }),
  });
  const data = await res.json();
  return data.response;
}
