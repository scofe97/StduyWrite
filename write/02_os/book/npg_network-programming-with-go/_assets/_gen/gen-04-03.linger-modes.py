# 타입 스펙: type-flowchart
# 사실 출처: NPG 04-03 §3 · SetLinger modes & RST teardown, p.34-35
import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 880, 560
d = D(W, H, "NPG CH.4 — SETLINGER MODES",
      "SetLinger 인자별 종료 동작과 데이터 처리",
      "SetLinger(sec) 값(음수·0·양수)에 따른 잔여 데이터 처리 방식과 RST·FIN 분기 흐름",
      "음수(기본 백그라운드 FIN) vs 0(즉시 폐기 및 RST) vs 양수(지정 초 대기)")

# 시작 노드: Close 호출
d.box(310, 96, 260, 36, fill=PAPER2, stroke=RULE, r=18)
d.t(440, 114, "tcpConn.Close() 호출", 12, INK, MONO, "middle", 600)
d.t(440, 126, "송신 버퍼 잔여 데이터 존재", 11, MUTED, KR, "middle")

d.arrow([(440, 132), (440, 156)], MUTED, "ar", 1.2)

# 메인 분기 다이아몬드 (cy = 180)
cy_d = 180
pts_d = f"440,{cy_d - 24} 530,{cy_d} 440,{cy_d + 24} 350,{cy_d}"
d.o.append(f'<polygon points="{pts_d}" fill="{PAPER2}" stroke="{WARN}" stroke-width="1.2"/>')
d.t(440, cy_d + 4, "SetLinger(sec) 설정값", 11, WARN, KR, "middle", 600)

cx1, cx2, cx3 = 175, 440, 705

# --- 분기 1: sec < 0 (음수 / 기본값) ---
d.line(350, cy_d, cx1, cy_d, OK, 1.2)
d.arrow([(cx1, cy_d), (cx1, 230)], OK, "ok", 1.4)
d.t(255, cy_d - 8, "sec < 0 (기본값)", 11, OK, MONO, "middle", 600)

d.box(70, 230, 210, 42, fill=PAPER2, stroke=RULE, r=6)
d.t(cx1, 247, "Close() 즉시 반환", 11, INK, KR, "middle", 600)
d.t(cx1, 263, "비차단 즉시 복귀", 11, MUTED, KR, "middle")

d.arrow([(cx1, 272), (cx1, 298)], MUTED, "ar", 1.2)

d.box(70, 298, 210, 42, fill=PAPER2, stroke=RULE, r=6)
d.t(cx1, 315, "백그라운드 전송", 11, INK, KR, "middle", 600)
d.t(cx1, 331, "잔여 데이터 전송 및 FIN", 11, MUTED, KR, "middle")

d.arrow([(cx1, 340), (cx1, 368)], OK, "ok", 1.4)

d.box(70, 368, 210, 42, fill=PAPER2, stroke=OK, r=21)
d.t(cx1, 386, "우아한 종료 (FIN)", 12, OK, KR, "middle", 600)
d.t(cx1, 401, "정상 4-way 완결", 11, MUTED, KR, "middle")

d.box(70, 426, 210, 34, fill=PAPER2, stroke=RULE, r=6)
d.t(cx1, 447, "서버 수신 미확인 (크래시 시 유실)", 11, MUTED, KR, "middle")

# --- 분기 2: sec == 0 (강제 즉시 종료) ---
d.arrow([(cx2, cy_d + 24), (cx2, 230)], BAD, "bad", 1.4)
d.t(cx2 + 16, cy_d + 36, "sec == 0", 11, BAD, MONO, "start", 600)

d.box(335, 230, 210, 42, fill=PAPER2, stroke=BAD, r=6)
d.t(cx2, 247, "미전송 잔여 데이터 폐기", 11, BAD, KR, "middle", 600)
d.t(cx2, 263, "송신 버퍼 즉시 파기", 11, BAD, KR, "middle")

d.arrow([(cx2, 272), (cx2, 298)], BAD, "bad", 1.4)

d.box(335, 298, 210, 42, fill=PAPER2, stroke=BAD, r=6)
d.t(cx2, 315, "정상 FIN 생략 · RST 송신", 11, BAD, KR, "middle", 600)
d.t(cx2, 331, "강제 종료 (Abortive Close)", 11, BAD, KR, "middle")

d.arrow([(cx2, 340), (cx2, 368)], BAD, "bad", 1.4)

d.box(335, 368, 210, 42, fill=PAPER2, stroke=BAD, r=21)
d.t(cx2, 386, "소켓 즉시 파괴", 12, BAD, KR, "middle", 600)
d.t(cx2, 401, "상대: reset by peer 오류", 11, BAD, KR, "middle")

d.box(335, 426, 210, 34, fill=PAPER2, stroke=BAD, r=6)
d.t(cx2, 447, "데이터 유실 필수 통보 (규격 강제)", 11, BAD, KR, "middle")

# --- 분기 3: sec > 0 (시한부 대기) ---
d.line(530, cy_d, cx3, cy_d, WARN, 1.2)
d.arrow([(cx3, cy_d), (cx3, 230)], WARN, "warn", 1.4)
d.t(620, cy_d - 8, "sec > 0 (양수)", 11, WARN, MONO, "middle", 600)

d.box(600, 230, 210, 42, fill=PAPER2, stroke=RULE, r=6)
d.t(cx3, 247, "Close() sec초 블로킹 대기", 11, INK, KR, "middle", 600)
d.t(cx3, 263, "잔여 데이터 전송 및 ACK 대기", 11, MUTED, KR, "middle")

d.arrow([(cx3, 272), (cx3, 298)], MUTED, "ar", 1.2)

# 하위 판별 다이아몬드 (cx3 = 705, cy = 318)
cy_sub = 318
pts_sub = f"{cx3},{cy_sub - 20} {cx3 + 55},{cy_sub} {cx3},{cy_sub + 20} {cx3 - 55},{cy_sub}"
d.o.append(f'<polygon points="{pts_sub}" fill="{PAPER2}" stroke="{WARN}" stroke-width="1.2"/>')
d.t(cx3, cy_sub + 4, "ACK 완료?", 11, WARN, KR, "middle", 600)

# 성공 하위 분기 (왼쪽 -> 645)
d.line(cx3 - 55, cy_sub, 645, cy_sub, OK, 1.2)
d.arrow([(645, cy_sub), (645, 368)], OK, "ok", 1.4)
d.t(630, cy_sub + 18, "완료", 11, OK, KR, "middle", 600)

d.box(595, 368, 100, 42, fill=PAPER2, stroke=OK, r=6)
d.t(645, 386, "정상 FIN", 11, OK, KR, "middle", 600)
d.t(645, 400, "전송 완료", 11, MUTED, KR, "middle")

# 실패 하위 분기 (오른쪽 -> 765)
d.line(cx3 + 55, cy_sub, 765, cy_sub, WARN, 1.2)
d.arrow([(765, cy_sub), (765, 368)], WARN, "warn", 1.4)
d.t(780, cy_sub + 18, "초과", 11, WARN, KR, "middle", 600)

d.box(715, 368, 100, 42, fill=PAPER2, stroke=WARN, r=6)
d.t(765, 386, "잔여 폐기", 11, WARN, KR, "middle", 600)
d.t(765, 400, "데이터 버림", 11, WARN, KR, "middle")

d.box(600, 426, 210, 34, fill=PAPER2, stroke=RULE, r=6)
d.t(cx3, 447, "OS 커널 지원 여부 의존", 11, MUTED, KR, "middle")

# 범례
d.legend(H - 44, [("우아한 정상 종료 (FIN)", OK), ("강제 즉시 파괴 (RST)", BAD), ("시한부 대기 / 전송 검증", WARN)])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "04-03.linger-modes.svg"))
d.save(out_path)
print(f"Generated: {out_path}")
