import { getPatchNoteData } from '@/lib/patchNotes';
import MarkdownRenderer from '../../components/patchnotes/MarkdownRenderer';
import styles from '../page.module.css';

export async function generateMetadata({ params }) {
  const noteData = getPatchNoteData(params.version);
  return {
    title: noteData.title,
  };
}

export default function PatchNoteDetailPage({ params }) {
  const noteData = getPatchNoteData(params.version);

  return (
    <article style={{ padding: '2rem', width: '70vw', margin: 'auto' }}>
      <header style={{ borderBottom: '1px solid #ddd', marginBottom: '2rem' }}>
        <h1>{noteData.title}</h1>
        <p style={{ color: '#666' }}>{noteData.date}</p>
      </header>
      
      <div className={styles.patchArea}>
        <MarkdownRenderer content={noteData.content} />
      </div>
    </article>
  );
}
