import { Routes, Route, Navigate } from 'react-router-dom';
import { Layout } from './components/Layout';
import { Ch02Page } from './pages/Ch02Page';
import { Ch03Page } from './pages/Ch03Page';
import { Ch04Page } from './pages/Ch04Page';
import { Ch05Page } from './pages/Ch05Page';
import { Ch06Page } from './pages/Ch06Page';
import { Ch07Page } from './pages/Ch07Page';
import { Ch08Page } from './pages/Ch08Page';

const chapters = [
  { path: '/ch02', label: 'Ch02: EventSource API', component: Ch02Page, badge: 'done' as const },
  { path: '/ch03', label: 'Ch03: Custom Events', component: Ch03Page, badge: 'done' as const },
  { path: '/ch04', label: 'Ch04: Reconnection', component: Ch04Page, badge: 'done' as const },
  { path: '/ch05', label: 'Ch05: Error Handling', component: Ch05Page, badge: 'done' as const },
  { path: '/ch06', label: 'Ch06: React Integration', component: Ch06Page, badge: 'done' as const },
  { path: '/ch07', label: 'Ch07: WebSocket vs SSE', component: Ch07Page, badge: 'theory' as const },
  { path: '/ch08', label: 'Ch08: 대규모 아키텍처', component: Ch08Page, badge: 'done' as const },
];

export function App() {
  return (
    <Routes>
      <Route element={<Layout chapters={chapters.map(c => ({ path: c.path, label: c.label, badge: c.badge }))} />}>
        <Route index element={<HomePage />} />
        {chapters.map(({ path, component: Component }) => (
          <Route key={path} path={path} element={<Component />} />
        ))}
        <Route path="*" element={<Navigate to="/" replace />} />
      </Route>
    </Routes>
  );
}

function HomePage() {
  return (
    <div style={{ padding: '40px', maxWidth: '800px' }}>
      <h1 style={{ fontSize: '28px', marginBottom: '16px', color: '#1a1a2e' }}>
        SSE (Server-Sent Events) 실습
      </h1>
      <p style={{ color: '#666', lineHeight: 1.6, marginBottom: '32px' }}>
        각 챕터별 실습을 좌측 네비게이션에서 선택하세요.<br />
        Ch02~Ch06, Ch08은 완성된 코드, Ch07은 이론입니다.
      </p>

      <div style={{ display: 'grid', gap: '16px' }}>
        {chapters.map(({ path, label, badge }) => {
          const badgeConfig = {
            done: { border: '#4CAF50', bg: '#e8f5e9', badgeBg: '#4CAF50', text: 'DONE' },
            todo: { border: '#ff9800', bg: '#fff8e1', badgeBg: '#ff9800', text: 'TODO' },
            theory: { border: '#2196F3', bg: '#e3f2fd', badgeBg: '#2196F3', text: 'THEORY' },
          }[badge];
          return (
            <a
              key={path}
              href={path}
              style={{
                display: 'block',
                padding: '20px',
                borderRadius: '8px',
                border: `2px solid ${badgeConfig.border}`,
                background: badgeConfig.bg,
                textDecoration: 'none',
                color: '#333',
              }}
            >
              <strong>{label}</strong>
              <span style={{
                marginLeft: '12px',
                padding: '2px 8px',
                borderRadius: '4px',
                background: badgeConfig.badgeBg,
                color: 'white',
                fontSize: '12px',
              }}>
                {badgeConfig.text}
              </span>
            </a>
          );
        })}
      </div>
    </div>
  );
}
