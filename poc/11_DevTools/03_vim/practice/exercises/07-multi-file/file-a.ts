// file-a.ts - 사용자 서비스 (Ch08: 다중 파일 연습)
// 이 파일은 사용자 관련 타입과 함수를 정의합니다.

export interface User {
  id: number;
  name: string;
  email: string;
  createdAt: Date;
}

export function createUser(name: string, email: string): User {
  return {
    id: Date.now(),
    name,
    email,
    createdAt: new Date(),
  };
}

export function formatUser(user: User): string {
  return `${user.name} <${user.email}>`;
}

export function validateEmail(email: string): boolean {
  const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
  return emailRegex.test(email);
}

export function isUserActive(user: User): boolean {
  const now = new Date();
  const daysSinceCreation = Math.floor(
    (now.getTime() - user.createdAt.getTime()) / (1000 * 60 * 60 * 24)
  );
  return daysSinceCreation < 30;
}

// 다중 파일 연습 미션:
// 1. :e file-b.ts 로 file-b.ts 열기
// 2. :bn (버퍼 next)로 file-a.ts와 file-b.ts 전환
// 3. :b file-a.ts 로 이름으로 버퍼 전환
// 4. :ls 로 버퍼 목록 확인
// 5. :sp file-b.ts 로 수평 분할하여 두 파일 동시에 보기
// 6. Ctrl+W hjkl 로 윈도우 간 이동
