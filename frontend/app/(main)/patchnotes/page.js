import Link from 'next/link';
import styles from './page.module.css';

import { getAllPatchNotes } from '@/lib/patchNotes';
export default function PatchNotesPage() {
  const allNotes = getAllPatchNotes();

  return (
    <div className={styles.patchnoteContainer}>
      <div className={styles.title}>
        <h1 style={{all:'revert'}}>패치노트</h1>
        <p>최신 업데이트 내역을 확인하는 거다요.</p>
        <hr />
      </div>
      <section>
        <ul>
          {allNotes.map(({ id, title, date }) => (
            <li key={id} className={styles.patchnoteItem}>
              <Link href={`/patchnotes/${id}`}>
                <div>
                  <h2>{title}</h2>
                  <small>{date}</small>
                </div>
              </Link>
            </li>
          ))}
        </ul>
      </section>
    </div>
  );
}
