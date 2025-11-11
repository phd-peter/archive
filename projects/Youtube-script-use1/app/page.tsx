"use client";
import React, { useState, useEffect } from "react";
import { supabase } from "@/lib/supabaseClient";
import dynamic from "next/dynamic";
import Modal from "@/app/components/Modal";
const UserMenu = dynamic(() => import("@/app/components/UserMenu"), { ssr: false });
const AuthForm = dynamic(() => import("@/app/components/AuthForm"), { ssr: false });

export default function Home() {
  const [youtubeUrl, setYoutubeUrl] = useState("");
  const [transcript, setTranscript] = useState<string | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [thread, setThread] = useState<string | null>(null);
  const [post, setPost] = useState<string | null>(null);
  const [postLoading, setPostLoading] = useState(false);
  const [postError, setPostError] = useState<string | null>(null);
  const [copied, setCopied] = useState<string | null>(null);
  const [user, setUser] = useState<any>(null);
  const [authOpen, setAuthOpen] = useState(false);

  useEffect(() => {
    const getUser = async () => {
      const { data } = await supabase.auth.getUser();
      setUser(data.user);
    };
    getUser();
    const { data: listener } = supabase.auth.onAuthStateChange((_event, session) => {
      setUser(session?.user ?? null);
    });
    return () => {
      listener.subscription.unsubscribe();
    };
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setTranscript(null);
    setError(null);
    setThread(null);
    setPost(null);
    setPostError(null);
    setLoading(true);
    try {
      const res = await fetch("/api/youtube-script", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: youtubeUrl }),
      });
      const data = await res.json();
      if (res.ok && data.transcript && data.transcript.length > 0) {
        // docs는 배열이므로, 텍스트만 추출
        setTranscript(data.transcript.map((doc: any) => doc.pageContent).join("\n\n"));
      } else {
        setError(data.error || "자막을 불러올 수 없습니다.");
      }
    } catch (err: any) {
      setError(err.message || "알 수 없는 오류가 발생했습니다.");
    } finally {
      setLoading(false);
    }
  };

  const handleGeneratePost = async () => {
    setThread(null);
    setPost(null);
    setPostError(null);
    setPostLoading(true);
    try {
      const res = await fetch("/api/youtube-script", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: youtubeUrl, generatePost: true }),
      });
      const data = await res.json();
      if (res.ok && (data.thread || data.post)) {
        setThread(data.thread || null);
        setPost(data.post || null);
      } else {
        setPostError(data.error || "게시글/스레드를 생성할 수 없습니다.");
      }
    } catch (err: any) {
      setPostError(err.message || "알 수 없는 오류가 발생했습니다.");
    } finally {
      setPostLoading(false);
    }
  };

  const handleCopy = async (text: string, type: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setCopied(type);
      setTimeout(() => setCopied(null), 1500);
    } catch {
      setCopied(null);
    }
  };

  // SPLIT 구분자 기준 스레드 분리
  const splitThread = (thread: string) => thread.split(/---SPLIT---/g).map(s => s.trim()).filter(Boolean);

  return (
    <div>
      <UserMenu onLoginOpen={() => setAuthOpen(true)} />
      <Modal open={authOpen} onClose={() => setAuthOpen(false)}>
        <AuthForm onAuth={() => setAuthOpen(false)} />
      </Modal>
      <div className="flex flex-col items-center justify-center min-h-screen p-8 w-full">
        <form onSubmit={handleSubmit} className="flex gap-2 w-full max-w-md mb-8">
          <input
            type="url"
            placeholder="유튜브 링크를 입력하세요"
            value={youtubeUrl}
            onChange={e => setYoutubeUrl(e.target.value)}
            className="flex-1 px-3 py-2 border rounded focus:outline-none focus:ring"
            required
          />
          <button
            type="submit"
            className="px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition-colors"
            disabled={loading}
          >
            {loading ? "로딩중..." : "제출"}
          </button>
        </form>
        {error && <div className="text-red-500 mb-4">{error}</div>}
        {transcript && (
          <div className="w-full max-w-2xl p-4 border rounded bg-gray-50 whitespace-pre-wrap overflow-x-auto mb-4" style={{ maxHeight: 400 }}>
            {transcript}
          </div>
        )}
        {transcript && (
          user ? (
            <button
              onClick={handleGeneratePost}
              className="px-4 py-2 bg-green-600 text-white rounded hover:bg-green-700 transition-colors mb-4"
              disabled={postLoading}
            >
              {postLoading ? "게시글/스레드 생성중..." : "스레드/링크드인 게시글 생성"}
            </button>
          ) : (
            <div className="mb-4 text-gray-500 flex items-center gap-2">
              로그인 후 AI 게시글 생성이 가능합니다.
              <button
                onClick={() => setAuthOpen(true)}
                className="ml-2 px-3 py-1 bg-blue-600 text-white rounded hover:bg-blue-700 text-sm"
              >
                로그인 / 회원가입
              </button>
            </div>
          )
        )}
        {postError && <div className="text-red-500 mb-4">{postError}</div>}
        {thread && (
          <div className="w-full max-w-2xl p-4 border rounded bg-yellow-50 whitespace-pre-wrap overflow-x-auto mb-4" style={{ maxHeight: 400 }}>
            <b>생성된 스레드:</b>
            <div className="flex flex-col gap-2 mt-2">
              {splitThread(thread).map((t, i) => (
                <div key={i} className="flex items-center gap-2">
                  <span className="flex-1">{t}</span>
                  <button
                    onClick={() => handleCopy(t, `thread-${i}`)}
                    className="px-2 py-1 text-xs bg-gray-200 rounded hover:bg-gray-300"
                  >
                    복사
                  </button>
                  {copied === `thread-${i}` && <span className="text-green-600 text-xs ml-1">복사됨</span>}
                </div>
              ))}
            </div>
            <div className="mt-4 flex justify-end">
              <button
                onClick={() => handleCopy(thread, "thread-all")}
                className="px-3 py-1 text-xs bg-blue-200 rounded hover:bg-blue-300"
              >
                전체 복사
              </button>
              {copied === "thread-all" && <span className="text-green-600 text-xs ml-2">전체 복사됨</span>}
            </div>
          </div>
        )}
        {post && (
          <div className="w-full max-w-2xl p-4 border rounded bg-blue-50 whitespace-pre-wrap overflow-x-auto" style={{ maxHeight: 400 }}>
            <b>생성된 게시글:</b>
            <div className="flex items-center gap-2 mt-2">
              <span className="flex-1">{post}</span>
              <button
                onClick={() => handleCopy(post, "post")}
                className="px-2 py-1 text-xs bg-gray-200 rounded hover:bg-gray-300"
              >
                복사
              </button>
              {copied === "post" && <span className="text-green-600 text-xs ml-1">복사됨</span>}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
