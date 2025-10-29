export async function getOfflineResponse(prompt: string, brain?: any): Promise<string> {
  const payload: any = { prompt };
  if (brain) payload.brain = brain;
  const res = await fetch("http://127.0.0.1:5000/api/respond", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(payload),
  });
  const data = await res.json();
  return data.response;
}
