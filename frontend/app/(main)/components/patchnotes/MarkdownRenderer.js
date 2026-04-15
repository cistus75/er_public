"use client"; // 👈 이것이 가장 중요합니다.

import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

// ReactMarkdown에 필요한 로직을 이 클라이언트 컴포넌트로 옮깁니다.
export default function MarkdownRenderer({ content }) {
  return (
    <ReactMarkdown remarkPlugins={[remarkGfm]}>
      {content}
    </ReactMarkdown>
  );
}