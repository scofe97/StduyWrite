import { ReactIntegrationDemo } from '../components/ch06/ReactIntegrationDemo';

export function Ch06Page() {
  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1 style={{ color: '#333', marginBottom: '8px' }}>Ch06: React Integration</h1>
      <p style={{ color: '#666', marginBottom: '24px' }}>
        React에서 SSE를 올바르게 통합하는 방법: cleanup, Strict Mode, AbortController, 메모이제이션을 구현합니다.
      </p>
      <ReactIntegrationDemo />
    </div>
  );
}
