import { ReconnectionDemo } from '../components/ch04/ReconnectionDemo';

export function Ch04Page() {
  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1 style={{ color: '#333', marginBottom: '8px' }}>Ch04: Reconnection</h1>
      <p style={{ color: '#666', marginBottom: '24px' }}>
        SSE의 자동 재연결, Last-Event-ID, retry 필드, 수동 재연결 로직(exponential backoff)을 구현합니다.
      </p>
      <ReconnectionDemo />
    </div>
  );
}
