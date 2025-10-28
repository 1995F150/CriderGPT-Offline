import React from "react";

export function NavigationMenu() {
  return (
    <div className="card sidebar">
      <div className="brand">
        <img src="/public/logo.svg" alt="logo" width={36} height={36} />
        <h1>CriderGPT</h1>
      </div>
      <nav style={{ marginTop: 12 }}>
        <ul style={{ display: "flex", flexDirection: "column", gap: 8 }}>
          <li>Chat</li>
          <li>Files</li>
          <li>Tools</li>
        </ul>
      </nav>
    </div>
  );
}
