import React from 'react';
import ReactMarkdown from 'react-markdown';

export default function ChatMessage({ message }: { message: string }) {
  return <ReactMarkdown>{message}</ReactMarkdown>;
} 