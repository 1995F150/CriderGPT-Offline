import React, { useState } from "react";
import { NavigationMenu } from "../components/navigation-menu";
import ChatInterface, { Message } from "../components/ChatInterface";
import AIAssistant from "../components/AIAssistant";
import { getOfflineResponse } from "../utils/localAI";

export default function Index() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [value, setValue] = useState("");
  const [loading, setLoading] = useState(false);

  async function send() {
    if (!value.trim()) return;
    const txt = value.trim();
    const userMsg: Message = { who: "user", text: txt };
    setMessages((s) => [...s, userMsg]);
    setValue("");
    setLoading(true);
    try {
      const r = await getOfflineResponse(txt);
      const aiMsg: Message = { who: "ai", text: r };
      setMessages((s) => [...s, aiMsg]);
    } catch (e) {
      const aiMsg: Message = { who: "ai", text: "(error contacting local backend)" };
      setMessages((s) => [...s, aiMsg]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="app-shell">
      <NavigationMenu />
      <div className="main-panel">
        <div className="card">
          <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center" }}>
            <div>
              <h2 style={{ margin: 0 }}>CriderGPT Offline</h2>
              <div style={{ fontSize: 12, color: "var(--muted)" }}>Built by Jessie Crider — Local-only AI assistant</div>
            </div>
            <AIAssistant />
          </div>
        </div>

        <ChatInterface messages={messages} />

        <div className="card">
          <div className="compose">
            <input
              placeholder={loading ? "Thinking..." : "Type a prompt..."}
              value={value}
              onChange={(e) => setValue(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") send();
              }}
            />
            <button onClick={send} disabled={loading}>
              Send
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
