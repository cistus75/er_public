import { getPatchNoteData } from '@/lib/patchNotes';
// 1. ReactMarkdown과 remarkGfm 임포트 제거
// import ReactMarkdown from 'react-markdown';
// import remarkGfm from 'remark-gfm';

// 2. 새로 만든 클라이언트 컴포넌트를 임포트합니다.
import MarkdownRenderer from '../../components/MarkdownRenderer';

// ... generateMetadata 함수 (변경 없음) ...
export async function generateMetadata({ params }) {
  const noteData = getPatchNoteData(params.version);
  return {
    title: noteData.title,
  };
}

export default function PatchNoteDetailPage({ params }) {
  const noteData = getPatchNoteData(params.version);

  return (
    <article style={{ padding: '2rem', maxWidth: '800px', margin: 'auto' }}>
      <header style={{ borderBottom: '1px solid #ddd', marginBottom: '2rem' }}>
        <h1>{noteData.title}</h1>
        <p style={{ color: '#666' }}>{noteData.date}</p>
      </header>
      
      <div>
        {/* 3. ReactMarkdown 대신 MarkdownRenderer를 사용합니다. */}
        <MarkdownRenderer content={noteData.content} />
      </div>
    </article>
  );
}