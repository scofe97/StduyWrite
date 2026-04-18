// Mock 모드 설정
// .env 파일에서 VITE_USE_MOCK=true 로 설정하면 Mock 데이터 사용
// VITE_USE_MOCK=false 또는 미설정 시 실제 API 호출

export const USE_MOCK = import.meta.env.VITE_USE_MOCK === "true"

// Mock API 지연 시간 (ms) - 실제 API 호출처럼 보이게 함
export const MOCK_DELAY = 300
