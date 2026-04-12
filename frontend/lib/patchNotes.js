import fs from 'fs';
import path from 'path';
import matter from 'gray-matter';

// patch-notes 디렉토리의 절대 경로
const postsDirectory = path.join(process.cwd(), 'patch-notes');

export function getAllPatchNotes() {
  // 디렉토리의 모든 파일 이름을 읽어옴
  const fileNames = fs.readdirSync(postsDirectory);

  const allPostsData = fileNames.map((fileName) => {
    // '.md' 확장자 제거하여 id(버전)으로 사용
    const id = fileName.replace(/\.md$/, '');

    // 파일 전체 경로
    const fullPath = path.join(postsDirectory, fileName);
    // 파일 내용 읽기
    const fileContents = fs.readFileSync(fullPath, 'utf8');

    // gray-matter로 frontmatter 파싱
    const matterResult = matter(fileContents);

    // 데이터와 id 합치기
    return {
      id,
      ...matterResult.data,
    };
  });

  // 날짜(date) 기준으로 최신순 정렬
  return allPostsData.sort((a, b) => {
    if (a.date < b.date) {
      return 1;
    } else {
      return -1;
    }
  });
}

export function getPatchNoteData(id) {
    const fullPath = path.join(postsDirectory, `${id}.md`);
    const fileContents = fs.readFileSync(fullPath, 'utf8');

    // frontmatter와 content 분리
    const matterResult = matter(fileContents);

    return {
        id,
        content: matterResult.content, // 마크다운 본문
        ...matterResult.data, // 메타데이터 (title, date 등)
    };
}