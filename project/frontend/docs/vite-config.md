# Vite 설정 가이드

이 문서는 `vite.config.ts`에 추가된 설정과 그 필요성을 설명합니다.

## 현재 설정

```typescript
import path from "path"
import react from "@vitejs/plugin-react-swc"
import { defineConfig } from "vite"

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      "@": path.resolve(__dirname, "./src"),
    },
  },
  server: {
    port: 3000,
    allowedHosts: ["app.scofe97.net", "localhost"],
  },
})
```

## 설정 항목 설명

### 1. plugins: [react()]

**플러그인**: `@vitejs/plugin-react-swc`

React + SWC 조합을 사용합니다. SWC(Speedy Web Compiler)는 Rust로 작성된 빠른 컴파일러로, Babel보다 빌드 속도가 빠릅니다.

**장점**:
- 개발 서버 HMR(Hot Module Replacement) 속도 향상
- 프로덕션 빌드 시간 단축
- JSX/TSX 변환 처리

### 2. resolve.alias

```typescript
alias: {
  "@": path.resolve(__dirname, "./src"),
}
```

**목적**: 경로 별칭(Path Alias) 설정

**필요성**:
- 상대 경로 대신 절대 경로 사용 가능
- 깊은 폴더 구조에서 `../../../../` 같은 복잡한 경로 회피
- 코드 가독성 및 유지보수성 향상

**사용 예시**:
```typescript
// 상대 경로 (비권장)
import { Button } from "../../../components/ui/button"

// 별칭 사용 (권장)
import { Button } from "@/components/ui/button"
```

**참고**: TypeScript에서도 인식하려면 `tsconfig.json`에 동일한 설정 필요:
```json
{
  "compilerOptions": {
    "paths": {
      "@/*": ["./src/*"]
    }
  }
}
```

### 3. server.port

```typescript
port: 3000
```

**목적**: 개발 서버 포트 지정

**필요성**:
- 기본 포트(5173) 대신 친숙한 3000 포트 사용
- 다른 서비스(백엔드 API 등)와의 포트 충돌 방지
- 프록시 설정 시 일관된 포트 사용

### 4. server.allowedHosts

```typescript
allowedHosts: ["app.scofe97.net", "localhost"]
```

**목적**: 허용된 호스트 명시적 지정

**필요성**:
- **보안**: Vite 5.x부터 Host Header Attack 방지를 위해 기본적으로 허용되지 않은 호스트 차단
- **외부 접근**: 커스텀 도메인(예: ngrok, cloudflare tunnel, 개인 도메인)으로 접속 시 필수
- **개발 환경**: 모바일 테스트, 원격 협업 시 외부 접근 허용

**오류 상황**:
```
This host is not allowed.
To allow this host, add app.scofe97.net to server.allowedHosts in vite.config.js.
```

위 오류는 `allowedHosts`에 해당 도메인이 없을 때 발생합니다.

**주의사항**:
- `true` 값을 사용하면 모든 호스트 허용 (보안 위험)
- 프로덕션에서는 이 설정이 적용되지 않음 (개발 서버 전용)

## 추가 가능한 설정

### HTTPS 설정 (로컬 개발 시)
```typescript
server: {
  https: true,
}
```

### 프록시 설정 (백엔드 API 연동)
```typescript
server: {
  proxy: {
    "/api": {
      target: "http://localhost:8080",
      changeOrigin: true,
    },
  },
}
```

### 빌드 최적화
```typescript
build: {
  rollupOptions: {
    output: {
      manualChunks: {
        vendor: ["react", "react-dom"],
      },
    },
  },
}
```

## 참고 문서

- [Vite 공식 문서 - 서버 옵션](https://vitejs.dev/config/server-options.html)
- [Vite 공식 문서 - 공유 옵션](https://vitejs.dev/config/shared-options.html)
- [@vitejs/plugin-react-swc](https://github.com/vitejs/vite-plugin-react-swc)
