const express = require('express');
const cors = require('cors');
const path = require('path');

const app = express();
const PORT = 3002;

// 미들웨어
app.use(cors());
app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

// ============================================================
// 데이터 및 상태
// ============================================================

// 사용자 데이터
const users = {
  admin: { password: 'admin123', userId: 'admin', userNm: '관리자', isAdmin: true },
  user01: { password: 'password', userId: 'user01', userNm: '사용자01', isAdmin: false }
};

// 토큰 저장소
const sessions = new Map();

// 티켓 데이터 로드
const ticketsFile = require('./data/tickets.json');
let ticketsData = [...ticketsFile.data.data]; // 런타임 수정 가능한 복사본

let ticketCounter = 1;

// ============================================================
// 유틸리티 함수
// ============================================================

// 토큰 생성
function generateToken() {
  return 'token_' + Date.now() + '_' + Math.random().toString(36).substring(7);
}

// 티켓번호 생성
function generateTicketNo() {
  const date = new Date().toISOString().split('T')[0].replace(/-/g, '');
  const num = String(ticketCounter++).padStart(4, '0');
  return `TCKT-${date}-${num}`;
}

// 지연 헬퍼
const delay = (ms) => new Promise(resolve => setTimeout(resolve, ms));

// ============================================================
// 인증 미들웨어
// ============================================================

function authMiddleware(req, res, next) {
  const skipPaths = ['/api/auth/login', '/login', '/health', '/'];
  const isStaticFile = req.path.match(/\.(html|css|js|png|jpg|jpeg|gif|ico)$/);

  if (skipPaths.some(path => req.path === path || req.path.startsWith(path)) || isStaticFile) {
    return next();
  }

  const token = req.headers.authorization?.replace('Bearer ', '');
  if (!token || !sessions.has(token)) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  req.user = sessions.get(token);
  next();
}

// ============================================================
// 헬스체크
// ============================================================

app.get('/health', (req, res) => {
  res.json({ status: 'ok' });
});

// ============================================================
// 인증 API
// ============================================================

// 로그인
app.post('/api/auth/login', (req, res) => {
  const { username, password } = req.body;
  const user = users[username];

  if (!user || user.password !== password) {
    return res.status(401).json({ error: 'Invalid credentials' });
  }

  const token = generateToken();
  const userInfo = { userId: user.userId, userNm: user.userNm, isAdmin: user.isAdmin };
  sessions.set(token, userInfo);

  res.json({ token, user: userInfo });
});

// 현재 사용자 정보
app.get('/api/auth/me', (req, res) => {
  const token = req.headers.authorization?.replace('Bearer ', '');

  if (!token || !sessions.has(token)) {
    return res.status(401).json({ error: 'Unauthorized' });
  }

  res.json(sessions.get(token));
});

// 인증 미들웨어 적용 (위의 라우트 이후에 적용)
app.use(authMiddleware);

// ============================================================
// 티켓 API
// ============================================================

// 티켓 목록 (페이징, 검색, 필터)
app.get('/api/v1/tickets', async (req, res) => {
  await delay(200); // 네트워크 시뮬레이션

  const { page = 1, pageSize = 10, searchColumn, searchKeyword, tcktStts } = req.query;

  let filtered = [...ticketsData];

  // 검색 필터
  if (searchColumn && searchKeyword) {
    filtered = filtered.filter(ticket => {
      const value = ticket[searchColumn];
      return value && value.toString().includes(searchKeyword);
    });
  }

  // 상태 필터
  if (tcktStts) {
    filtered = filtered.filter(ticket => ticket.tcktStts === tcktStts);
  }

  // 정렬 (regDt DESC)
  filtered.sort((a, b) => new Date(b.regDt) - new Date(a.regDt));

  // 페이징
  const totalItemSize = filtered.length;
  const startIdx = (page - 1) * pageSize;
  const endIdx = startIdx + parseInt(pageSize);
  const paginatedData = filtered.slice(startIdx, endIdx);

  res.json({
    data: {
      data: paginatedData,
      pageSize: parseInt(pageSize),
      totalItemSize,
      currentPage: parseInt(page)
    }
  });
});

// 티켓 상세
app.get('/api/v1/tickets/:tcktNo', (req, res) => {
  const { tcktNo } = req.params;
  const ticket = ticketsData.find(t => t.tcktNo === tcktNo);

  if (!ticket) {
    return res.status(404).json({ error: 'Ticket not found' });
  }

  const ticketWithRepo = {
    ...ticket,
    ticketRepoInfoList: [
      {
        repoUrl: `https://git.okestro.com/tps/tps-api`,
        repoNm: 'tps-api',
        branchNm: `feature/${tcktNo}`,
        tagNm: '',
        commitHash: ''
      }
    ]
  };

  res.json({ data: ticketWithRepo });
});

// CICD 티켓 생성
app.post('/api/v1/tickets/cicd', async (req, res) => {
  await delay(500);

  const { tcktNm, taskCd, wrkflwCd, devlopPicId } = req.body;

  if (!tcktNm || !taskCd || !wrkflwCd || !devlopPicId) {
    return res.status(400).json({ error: 'Missing required fields: tcktNm, taskCd, wrkflwCd, devlopPicId' });
  }

  const newTicket = {
    tcktNo: generateTicketNo(),
    tcktNm,
    taskCd,
    wrkflwCd,
    devlopPicId,
    tcktStts: 'REGISTERED',
    rgtrId: req.user.userId,
    regDt: new Date().toISOString(),
    ...req.body
  };

  ticketsData.push(newTicket);
  res.status(201).json({ data: newTicket });
});

// PMS 티켓 생성
app.post('/api/v1/tickets/pms', async (req, res) => {
  await delay(500);

  const { tcktNm, taskCd, wrkflwCd, devlopPicId } = req.body;

  if (!tcktNm || !taskCd || !wrkflwCd || !devlopPicId) {
    return res.status(400).json({ error: 'Missing required fields: tcktNm, taskCd, wrkflwCd, devlopPicId' });
  }

  const newTicket = {
    tcktNo: generateTicketNo(),
    tcktNm,
    taskCd,
    wrkflwCd,
    devlopPicId,
    tcktStts: 'REGISTERED',
    rgtrId: req.user.userId,
    regDt: new Date().toISOString(),
    ...req.body
  };

  ticketsData.push(newTicket);
  res.status(201).json({ data: newTicket });
});

// 티켓 상태 업데이트
app.put('/api/v1/tickets/:tcktNo/status', (req, res) => {
  const { tcktNo } = req.params;
  const { tcktStts } = req.body;

  const ticket = ticketsData.find(t => t.tcktNo === tcktNo);
  if (!ticket) {
    return res.status(404).json({ error: 'Ticket not found' });
  }

  ticket.tcktStts = tcktStts;
  res.json({ data: ticket });
});

// ============================================================
// 워크플로우 API
// ============================================================

// 워크플로우 진행 상태
app.get('/api/v1/tickets/:tcktNo/progress', (req, res) => {
  const { tcktNo } = req.params;
  const ticket = ticketsData.find(t => t.tcktNo === tcktNo);

  if (!ticket) {
    return res.status(404).json({ error: 'Ticket not found' });
  }

  const steps = [
    { stepSn: 1, stepNm: 'Planning', stepStts: 'COMPLETED', startDt: '2026-02-01T09:00:00Z', endDt: '2026-02-02T17:00:00Z' },
    { stepSn: 2, stepNm: 'Development', stepStts: 'IN_PROGRESS', startDt: '2026-02-03T09:00:00Z', endDt: null },
    { stepSn: 3, stepNm: 'Testing', stepStts: 'PENDING', startDt: null, endDt: null },
    { stepSn: 4, stepNm: 'Deployment', stepStts: 'PENDING', startDt: null, endDt: null }
  ];

  res.json({
    data: {
      steps,
      currentStep: 2
    }
  });
});

// ============================================================
// HTML 페이지 라우트
// ============================================================

// 루트 리디렉션
app.get('/', (req, res) => {
  res.redirect('/login');
});

// HTML 페이지들
app.get('/login', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'login.html'));
});

app.get('/tickets', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'ticket-list.html'));
});

app.get('/tickets/create/cicd', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'ticket-create-cicd.html'));
});

app.get('/tickets/create/pms', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'ticket-create-pms.html'));
});

app.get('/components', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'components.html'));
});

// 티켓 진행 상태 페이지 (동적 라우트는 마지막에)
app.get('/tickets/:tcktNo/progress', (req, res) => {
  res.sendFile(path.join(__dirname, 'views', 'ticket-progress.html'));
});

// ============================================================
// 서버 시작
// ============================================================

app.listen(PORT, () => {
  console.log(`Mock server running on http://localhost:${PORT}`);
  console.log(`Health check: http://localhost:${PORT}/health`);
});
