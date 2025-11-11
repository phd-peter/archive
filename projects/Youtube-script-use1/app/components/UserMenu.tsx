"use client";
import { useEffect, useState } from "react";
import { supabase } from "@/lib/supabaseClient";

export default function UserMenu({ onLoginOpen }: { onLoginOpen: () => void }) {
  const [user, setUser] = useState<any>(null);

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

  const handleLogout = async () => {
    await supabase.auth.signOut();
  };

  return (
    <div className="flex justify-end items-center w-full max-w-2xl mx-auto mt-4 mb-2 pr-2">
      {user ? (
        <>
          <span className="mr-4 text-gray-700 font-medium">{user.email}</span>
          <button
            onClick={handleLogout}
            className="bg-gray-200 hover:bg-gray-300 text-gray-800 font-semibold py-1 px-4 rounded shadow-sm transition-colors border border-gray-300"
          >
            로그아웃
          </button>
        </>
      ) : (
        <button
          onClick={onLoginOpen}
          className="bg-blue-600 hover:bg-blue-700 text-white font-semibold py-1 px-4 rounded shadow-sm transition-colors"
        >
          로그인 / 회원가입
        </button>
      )}
    </div>
  );
} 