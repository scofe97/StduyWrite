# 타입 스펙: type-dp-security-matrix — 격자 문법을 비교 행렬로 쓴다. 같은 질문 다섯(정의·암호화 포트·메시지 위치·새 메일 알림·보내기)을 IMAP·POP3·웹메일 세 열에 나란히 놓는다.
# 사실 출처: RFC 9051(IMAP4rev2, 2021-08, 초록·§6.3.13 IDLE), RFC 1939(POP3, 1996-05, §1 Introduction 의 내려받은 뒤 지움·QUIT 의 UPDATE 상태),
#   RFC 8314 §3.1·§3.2(pop3s 995, imaps 993), RFC 6409(IMAP 은 메일 게시를 정하지 않고 제출은 RFC 6409), RFC 1939 §2(POP3 클라이언트는 메일을 SMTP 연결로 보냄), 추출본 v1.txt 2685~2696행(온라인은 WebSocket 실시간 서버, 오프라인은 웹 서버가 REST 로 당김).
# Layout conventions: 머리 행 높이 40, 데이터 행 stride 72, 열 폭 [136, 264, 264, 264], 열 사이 간격 없음. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, BAD, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 576
d = D(W, H, "BYTEBYTEGO · 08-02 §2",
      "받는 길은 메시지를 어디에 두느냐로 IMAP 과 POP3 가 갈린다",
      "같은 질문 다섯을 IMAP4rev2·POP3·웹메일에 나란히 놓고 서버에 상태가 남는 자리를 짚습니다.",
      "웹메일 열은 서비스가 정한 HTTP·WebSocket 경로이고 표준 문서가 따로 없습니다")

cols = [("질문", 136), ("IMAP4rev2", 264), ("POP3", 264), ("웹메일", 264)]
X0, Y0, HH, RH = 12, 100, 40, 72
x = X0
xs = []
for nm, w in cols:
    xs.append((x, w))
    d.box(x, Y0, w, HH, PAPER2, RULE, 0.9, 0)
    d.t(x + w / 2, Y0 + 25, nm, 13, MUTED, KR if any("가" <= c <= "힣" for c in nm) else MONO, "middle", 600)
    x += w

# (질문, (IMAP 위, IMAP 아래, 색), (POP3 …), (웹메일 …))
rows = [
    ("정의 문서", ("RFC 9051", "IMAP4rev2 · 2021-08", INFO), ("RFC 1939", "POP3 · 1996-05", INFO), ("서비스 자체 API", "HTTP · WebSocket", INFO)),
    ("암호화 접속", ("포트 993", "imaps · RFC 8314", INFO), ("포트 995", "pop3s · RFC 8314", INFO), ("HTTPS", "웹 서버 · 실시간 서버", INFO)),
    ("메시지 위치", ("서버에 둠", "폴더 · 플래그도 서버", OK), ("내려받은 뒤 지움", "QUIT 의 UPDATE 상태", WARN), ("서버에 둠", "저장 계층", OK)),
    ("새 메일 알림", ("IDLE 명령", "서버가 먼저 알려 줌", OK), ("알림 명령 없음", "다시 조회해야 함", WARN), ("WebSocket", "오프라인은 REST 로 당김", OK)),
    ("메일 보내기", ("정하지 않음", "RFC 6409 제출 사용", WARN), ("정하지 않음", "제출은 SMTP 에 맡김", WARN), ("웹 서버가 받음", "발신 큐로 넘김", OK)),
]
FOCAL = (2, 1)
fam = lambda s: KR if any("가" <= ch <= "힣" for ch in s) else MONO
for r, row in enumerate(rows):
    y = Y0 + HH + r * RH
    for k in range(4):
        cx0, w = xs[k]
        if k == 0:
            d.box(cx0, y, w, RH, PAPER2, RULE, 0.9, 0)
            d.t(cx0 + w / 2, y + 42, row[0], 13, INK, KR, "middle", 600)
            continue
        a, b, c = row[k]
        if (r, k) == FOCAL:
            d.tone(cx0, y, w, RH, ACC, 0, "14", 1.4)
            col = ACC
        else:
            d.box(cx0, y, w, RH, PAPER, RULE, 0.9, 0)
            col = c if c != INFO else INK
        d.t(cx0 + w / 2, y + 32, a, 13, col, fam(a), "middle", 600)
        d.t(cx0 + w / 2, y + 56, b, 13, MUTED, fam(b), "middle")

d.legend(H - 56, [("가능·서버가 함", OK), ("한계·정하지 않음", WARN), ("이 절의 초점", ACC)])
d.save("08-02.access-matrix.svg")
