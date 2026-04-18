import { ErrorHandlingDemo } from '../components/ch05/ErrorHandlingDemo';

export function Ch05Page() {
  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1 style={{ color: '#333', marginBottom: '8px' }}>Ch05: Error Handling</h1>
      <p style={{ color: '#666', marginBottom: '24px' }}>
        SSE 에러 처리, readyState 기반 판단, heartbeat 타임아웃, fallback polling 전략을 구현합니다.
      </p>
      <ErrorHandlingDemo />
    </div>
  );
}
