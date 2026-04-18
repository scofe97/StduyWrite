/**
 * @redpanda-data/transform-sdk Mock
 *
 * WASM SDK는 Redpanda 브로커 런타임에서만 동작하므로,
 * 단위 테스트 시에는 이 mock을 사용한다.
 * 테스트에서는 마스킹 함수만 직접 테스트하고,
 * onRecordWritten 콜백은 통합 테스트(rpk)로 검증한다.
 */
export function onRecordWritten(_callback: Function): void {
  // no-op in test environment
}
