import { AdaptivePollingDemo } from '../components/ch08/AdaptivePollingDemo';

export function Ch08Page() {
  return (
    <div style={{ padding: '32px', maxWidth: '900px' }}>
      <h2 style={{ fontSize: '24px', marginBottom: '8px', color: '#1a1a2e' }}>
        Ch08: 대규모 트래픽 아키텍처
      </h2>
      <p style={{ color: '#666', lineHeight: 1.6, marginBottom: '24px' }}>
        어댑티브 폴링 + Full Jitter를 구현합니다.
        서버가 TTL로 폴링 주기를 제어하고, 클라이언트가 Jitter로 요청을 분산합니다.
      </p>
      <AdaptivePollingDemo />
    </div>
  );
}
