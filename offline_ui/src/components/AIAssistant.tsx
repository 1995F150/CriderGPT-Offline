import React from "react";

export default function AIAssistant({ message }: { message?: string }) {
  return (
    <div className="card">
      <h3 style={{ color: "var(--accent)" }}>CriderGPT Offline</h3>
      <p className="muted">An offline assistant built by Jessie Crider.</p>
      {message && <div style={{ marginTop: 8 }}>{message}</div>}
    </div>
  );
}

