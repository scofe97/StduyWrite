// 간단한 Express 서버 - Docker 실습용
const express = require('express');
const app = express();
const PORT = process.env.PORT || 3000;

// 미들웨어
app.use(express.json());

// 루트 엔드포인트
app.get('/', (req, res) => {
  res.json({
    message: 'Docker PoC - Basic Node.js App',
    version: '1.0.0',
    timestamp: new Date().toISOString()
  });
});

// 헬스체크 엔드포인트
app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// 서버 시작
app.listen(PORT, () => {
  console.log(`Server running on port ${PORT}`);
});
