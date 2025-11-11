"use client";
import { useState, useRef, useEffect } from "react";
import Image from "next/image";
import FAQAccordion, { FAQItem } from "./components/FAQAccordion";
import FloatingInfoButton from "./components/FloatingInfoButton";
import ChatMessage from "./components/ChatMessage";

export default function Home() {
  const [messages, setMessages] = useState([
    { role: "assistant", content: "안녕하세요! 성경에 대해 궁금한 점을 자유롭게 질문해 주세요." },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const inputRef = useRef<HTMLInputElement>(null);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const faqList: FAQItem[] = [
    {
      question: "직장에서 신앙인으로 산다는 건 구체적으로 뭘 의미해?",
      answer:
        "신앙인은 직장에서 단순히 착하게 사는 걸 넘어서, 일 자체를 하나님께 드리는 예배로 봅니다 (골 3:23). 진실함, 공의, 사랑을 실천하고, 경쟁과 성공의 논리 속에서도 복음의 겸손과 섬김을 선택하는 삶입니다.\n예를 들어, 동료들이 보고하지 않는 실수를 솔직히 보고하거나, 부당한 요구를 거절하면서도 상대를 존중하는 태도가 그런 모습일 수 있어요.",
    },
    {
      question: "하나님을 믿는데도 불안하고 우울할 땐 어떻게 해야 해?",
      answer:
        "믿음은 항상 평안한 감정을 보장하지 않아요. 시편 기자처럼 하나님께 정직하게 감정을 토로하고, 공동체와 전문가의 도움을 구하며, 말씀과 기도로 마음을 훈련하는 과정이 필요합니다 (시 42:11). 하나님은 우리의 연약함 속에서도 일하십니다.\n예를 들어, 아침마다 시편 한 편을 소리 내어 읽으며 하나님께 마음을 열고, 믿음의 친구와 정기적으로 감정을 나누는 시간을 가질 수 있어요.",
    },
    {
      question: "성경을 어떻게 읽어야 내 삶에 적용할 수 있을까?",
      answer:
        "성경은 단순한 규칙서가 아니라 하나님이 나를 위해 하신 일의 이야기예요 (눅 24:27). 먼저 예수 그리스도를 중심으로 읽고, 매일 작은 순종과 실천으로 연결해보세요. 성경을 통해 자신을 보려 하기보다 하나님을 보려는 시각이 필요합니다.\n예를 들어, '원수를 사랑하라'는 말씀을 읽고, 실제로 나를 힘들게 한 사람을 위해 짧게라도 기도해보는 실천을 할 수 있어요.",
    },
    {
      question: "왜 성경은 성(sexuality)에 대해 보수적인 기준을 요구할까?",
      answer:
        "성경은 성을 억압하려는 게 아니라, 언약적 사랑과 헌신 속에서 성의 깊이와 의미를 보호하려 합니다 (창 2:24). 성은 단순한 욕망이 아니라 관계를 맺고 주는 전인격적 선물로 설계되었기에, 하나님은 그 선을 지키길 원하십니다.\n예를 들어, 혼전 성관계를 기다리는 선택은 단순한 규칙 따르기가 아니라, '나를 전적으로 맡기기 전에 먼저 언약으로 나를 지키겠다'는 신뢰의 표현이에요.",
    },
  ];

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;
    setMessages((prev) => [...prev, { role: "user", content: input }]);
    setInput("");
    setLoading(true);
    try {
      const res = await fetch("/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ message: input }),
      });
      if (!res.ok) {
        throw new Error("API Error");
      }
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.message || "답변을 불러오지 못했습니다." },
      ]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "오류가 발생했습니다. 잠시 후 다시 시도해 주세요." },
      ]);
    } finally {
      setLoading(false);
    }
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === "Enter" && !loading) handleSend();
  };

  return (
    <div className="flex flex-col min-h-screen bg-background text-foreground">
      <header className="flex flex-col items-center pt-4 pb-2 gap-2">
        <div className="text-4xl font-extrabold tracking-tight text-blue-700 dark:text-blue-200 mb-1">말씀 길잡이</div>
      </header>
      <div className="max-w-5xl w-full mx-auto mb-2 px-2">
        <div className="text-sm text-gray-500 dark:text-gray-400 text-center leading-relaxed">
          <div>질문이 신앙의 시작입니다.</div>
          <div>자유롭게, 솔직하게 물어보세요.</div>
          <div className="mt-1">(여러분의 질문은 저장되지 않습니다.)</div>
        </div>
      </div>
      <main className="flex-1 flex flex-col items-center px-2 sm:px-8 md:px-8 lg:px-0 w-full bg-gradient-to-br from-gray-50 via-white to-blue-50 dark:from-gray-900 dark:via-black dark:to-blue-950 transition-colors duration-500">
        <div className="w-full flex flex-col sm:flex-row items-stretch gap-6 mb-6 max-w-5xl mx-auto">
          <div className="sm:w-2/3 w-full flex flex-col order-1 sm:order-2">
            <div className="max-w-md w-full mx-auto sm:max-w-none flex-1 chat-scroll bg-white/90 dark:bg-black/40 rounded-2xl shadow-lg p-6 flex flex-col gap-3 mb-3 border border-gray-100 dark:border-gray-800">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
                >
                  <div
                    className={`rounded-2xl px-5 py-3 max-w-[80%] text-base whitespace-pre-line shadow-sm transition-colors duration-200 ${
                      msg.role === "user"
                        ? "bg-blue-600 text-white dark:bg-blue-500 dark:text-white"
                        : "bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100"
                    }`}
                    aria-label={msg.role === "user" ? "내 메시지" : "AI 답변"}
                  >
                    {msg.role === "assistant" ? (
                      <ChatMessage message={msg.content} />
                    ) : (
                      msg.content
                    )}
                  </div>
                </div>
              ))}
              {loading && (
                <div className="flex justify-start">
                  <div className="rounded-2xl px-5 py-3 bg-gray-100 dark:bg-gray-800 text-gray-900 dark:text-gray-100 text-base animate-pulse shadow-sm">
                    답변을 불러오는 중...
                  </div>
                </div>
              )}
              <div ref={chatEndRef} />
            </div>
            <div className="max-w-md w-full mx-auto sm:max-w-none flex gap-2 mt-auto min-w-0">
              <input
                ref={inputRef}
                type="text"
                className="flex-1 min-w-0 rounded-xl border border-gray-300 dark:border-gray-700 px-5 py-3 text-base focus:outline-none focus:ring-2 focus:ring-blue-400 bg-white/80 dark:bg-black/50 shadow-sm transition-colors duration-200"
                placeholder="질문을 입력하세요.. ex)눅3:21, 시편1편"
                value={input}
                onChange={(e) => setInput(e.target.value)}
                onKeyDown={handleKeyDown}
                disabled={loading}
                aria-label="질문 입력"
              />
              <button
                onClick={handleSend}
                disabled={loading || !input.trim()}
                className="rounded-xl bg-blue-600 text-white px-4 py-3 font-semibold hover:bg-blue-700 disabled:opacity-50 transition-colors shadow-sm w-auto"
                aria-label="질문 보내기"
              >
                전송
              </button>
            </div>
          </div>
          <div className="sm:w-1/3 w-full flex-shrink-0 order-2 sm:order-1">
            <div className="max-w-md w-full mx-auto sm:max-w-none">
              <FAQAccordion faqs={faqList} />
            </div>
          </div>
        </div>
      </main>
      <footer className="py-4 text-center text-xs text-gray-400">© 2025 말씀 길잡이 | BIBLE-GPT</footer>
      <FloatingInfoButton />
    </div>
  );
}
