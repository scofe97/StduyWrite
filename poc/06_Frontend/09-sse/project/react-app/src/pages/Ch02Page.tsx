import { EventSourceDemo } from '../components/ch02/EventSourceDemo';

export function Ch02Page() {
  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1 style={{ color: '#333', marginBottom: '8px' }}>Ch02: EventSource API</h1>
      <p style={{ color: '#666', marginBottom: '24px' }}>
        EventSource API의 기본 사용법, readyState 관리, event-source-polyfill을 활용한 커스텀 헤더 지원을 실습합니다.
      </p>
      <EventSourceDemo />
    </div>
  );
}
