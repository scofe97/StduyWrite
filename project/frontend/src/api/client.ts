import axios, { AxiosError, AxiosInstance, InternalAxiosRequestConfig } from "axios"

// API 기본 설정
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8080"

// Axios 인스턴스 생성
export const apiClient: AxiosInstance = axios.create({
  baseURL: API_BASE_URL,
  timeout: 30000,
  headers: {
    "Content-Type": "application/json",
  },
})

// Request Interceptor
apiClient.interceptors.request.use(
  (config: InternalAxiosRequestConfig) => {
    // 토큰이 있으면 Authorization 헤더 추가
    const token = localStorage.getItem("accessToken")
    if (token && config.headers) {
      config.headers.Authorization = `Bearer ${token}`
    }
    return config
  },
  (error: AxiosError) => {
    return Promise.reject(error)
  }
)

// Response Interceptor
apiClient.interceptors.response.use(
  (response) => response,
  (error: AxiosError) => {
    // 401 Unauthorized 처리
    if (error.response?.status === 401) {
      localStorage.removeItem("accessToken")
      // TODO: 로그인 페이지로 리다이렉트 또는 인증 상태 초기화
    }

    // 에러 메시지 추출
    const errorMessage =
      (error.response?.data as { message?: string })?.message ||
      error.message ||
      "알 수 없는 오류가 발생했습니다."

    return Promise.reject(new Error(errorMessage))
  }
)

export default apiClient
