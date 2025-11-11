import { useState } from "react";

export default function FloatingInfoButton() {
  const [open, setOpen] = useState(false);

  return (
    <>
      <button
        className="fixed left-4 bottom-4 z-50 bg-blue-600 hover:bg-blue-700 text-white rounded-full w-14 h-14 flex items-center justify-center shadow-lg transition"
        onClick={() => setOpen((o) => !o)}
        aria-label="도움말 열기"
      >
        {/* Heroicons의 QuestionMarkCircleIcon SVG */}
        <svg xmlns="http://www.w3.org/2000/svg" className="h-8 w-8" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8.227 9a3 3 0 115.546 0c0 1.657-1.5 2.5-2.5 2.5m.25 4h.01M12 21c4.97 0 9-4.03 9-9s-4.03-9-9-9-9 4.03-9 9 4.03 9 9 9z" />
        </svg>
      </button>
      {open && (
        <div
          className="
            fixed z-50
            left-4 bottom-24
            w-64 max-w-[90vw]
            bg-white dark:bg-gray-900
            border border-gray-200 dark:border-gray-700
            rounded-2xl shadow-xl p-6
          "
          style={{ minWidth: 220 }}
        >
          <h2 className="text-lg font-semibold mb-2">도움말 & 안내</h2>
          <ul className="mb-3 text-sm text-gray-700 dark:text-gray-200 space-y-2">
            <li>
              <span className="font-bold">FAQ:</span>{" "}
              <a href="https://bible.gpt/faq" target="_blank" className="underline">자주 묻는 질문 보기</a>
            </li>
            <li>
              <span className="font-bold">문의:</span>{" "}
              <a href="mailto:your@email.com" className="underline">이메일로 문의하기</a>
            </li>
            <li>
              <span className="font-bold">피드백:</span>{" "}
              <a href="https://bible.gpt/feedback" target="_blank" className="underline">피드백 남기기</a>
            </li>
            <li>
              <span className="font-bold">개인정보 안내:</span> 질문은 저장되지 않습니다.
            </li>
          </ul>
          <button
            className="mt-2 text-xs text-gray-400 hover:text-gray-600"
            onClick={() => setOpen(false)}
          >
            닫기
          </button>
        </div>
      )}
    </>
  );
} 