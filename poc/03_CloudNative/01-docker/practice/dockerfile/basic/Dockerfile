# 기본 Node.js 애플리케이션 빌드
FROM node:20-alpine

# 작업 디렉토리 설정
WORKDIR /app

# 의존성 파일 먼저 복사 (캐시 최적화)
COPY package*.json ./

# 의존성 설치
RUN npm ci --only=production

# 소스 코드 복사
COPY . .

# 포트 노출
EXPOSE 3000

# 애플리케이션 실행
CMD ["node", "app.js"]
