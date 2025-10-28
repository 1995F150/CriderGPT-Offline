import React, { useEffect, useRef } from "react";

export type Message = { who: "user" | "ai"; text: string };

export default function ChatInterface({
  messages,
}: {
  messages: Message[];
}) {
  const scrollRef = useRef<HTMLDivElement | null>(null);

  useEffect(() => {
    if (scrollRef.current) scrollRef.current.scrollTop = scrollRef.current.scrollHeight;
  }, [messages]);

  return (
    <div className="card chat-window">
      <div ref={scrollRef} className="messages">
        {messages.map((m, i) => (
          <div key={i} className={`message ${m.who}`}>
            {m.text}
          </div>
        ))}
      </div>
    </div>
  );
}
