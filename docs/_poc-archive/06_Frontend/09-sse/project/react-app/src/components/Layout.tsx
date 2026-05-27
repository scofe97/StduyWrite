import { NavLink, Outlet } from 'react-router-dom';

interface ChapterLink {
  path: string;
  label: string;
  badge: 'done' | 'todo' | 'theory';
}

interface LayoutProps {
  chapters: ChapterLink[];
}

export function Layout({ chapters }: LayoutProps) {
  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Sidebar */}
      <nav style={{
        width: '240px',
        background: '#1a1a2e',
        color: '#eee',
        padding: '20px 0',
        flexShrink: 0,
      }}>
        <NavLink
          to="/"
          style={{ display: 'block', padding: '12px 20px', color: '#fff', textDecoration: 'none', fontWeight: 'bold', fontSize: '16px' }}
        >
          SSE 실습
        </NavLink>
        <hr style={{ border: 'none', borderTop: '1px solid #333', margin: '8px 0' }} />

        {chapters.map(({ path, label, badge }) => {
          const badgeConfig = {
            done: null,
            todo: { bg: '#ff9800', text: 'TODO' },
            theory: { bg: '#2196F3', text: 'THEORY' },
          }[badge];
          return (
            <NavLink
              key={path}
              to={path}
              style={({ isActive }) => ({
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                padding: '10px 20px',
                color: isActive ? '#fff' : '#aaa',
                background: isActive ? '#16213e' : 'transparent',
                textDecoration: 'none',
                fontSize: '14px',
                borderLeft: isActive ? '3px solid #4fc3f7' : '3px solid transparent',
              })}
            >
              <span>{label}</span>
              {badgeConfig && (
                <span style={{
                  padding: '1px 6px',
                  borderRadius: '3px',
                  background: badgeConfig.bg,
                  color: '#fff',
                  fontSize: '10px',
                }}>
                  {badgeConfig.text}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* Main content */}
      <main style={{ flex: 1, background: '#f5f5f5', overflow: 'auto' }}>
        <Outlet />
      </main>
    </div>
  );
}
