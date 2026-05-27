import { BasicCustomEventsDemo, AuthCustomEventsDemo } from '../components/ch03/CustomEventsDemo';

export function Ch03Page() {
  return (
    <div style={{ padding: '20px', maxWidth: '1000px', margin: '0 auto' }}>
      <h1 style={{ color: '#333', marginBottom: '8px' }}>Ch03: Custom Events</h1>
      <p style={{ color: '#666', marginBottom: '24px' }}>
        SSE의 event: 필드를 사용한 커스텀 이벤트 타입 분리와 addEventListener 패턴을 실습합니다.
      </p>
      <BasicCustomEventsDemo />
      <AuthCustomEventsDemo />
    </div>
  );
}
