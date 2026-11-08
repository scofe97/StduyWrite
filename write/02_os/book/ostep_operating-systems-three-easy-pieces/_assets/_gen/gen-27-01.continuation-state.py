# 27-01 §4 — FILE 요청 하나의 job_t 는 읽는 중 상태에 머물며, aio_read 가 끝날 때마다 off 를 읽은 만큼 늘려 다시 읽고, 0 바이트가 오면 소켓을 닫는다.
# 본문 근거: 이 노트 「4. 비동기 뒤 상태 넘기기」 의 「수동 스택 관리와 continuation」 소절.
# 검증 근거: macOS(Darwin 25.6, 2026-11-08)에서 evsrv.c 에 stderr 출력을 넣은 복사본으로 400,001 바이트 FILE 을 읽음.
#            aio_read 완료 25회(16,384 바이트 24회, 6,785 바이트 1회)로 off 가 0 → 16,384 → … → 393,216 → 400,001, 26번째 완료는 0 바이트였고 이어 close.
# 공식 근거: aio_return(3) — 완료 뒤 요청마다 한 번만 호출해 읽은 바이트 수를 받는다.
# 타입 스펙: type-state — 시작점, 읽는 중, 닫힘 세 상태. 자기 전이는 위로 올라갔다 내려오는 직각 경로로 그리고 라벨에 사건 [조건] / 동작 형식을 쓴다.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, MUTED, SOFT, INK, PAPER2, RULE, OK, WARN, BAD, INFO, KR, MONO

W, H = 880, 444
d = D(W, H, "OSTEP · 27-01 §4",
      "job_t 는 읽는 중 상태에서 off 를 늘리며 파일 끝까지 돈다",
      "FILE 요청이 들어오면 job_t 에 소켓 sd 와 읽은 위치 off=0 을 적고 읽는 중 상태가 된다. "
      "aio_read 가 끝나 읽은 바이트 수 n 이 0 보다 크면 소켓에 쓰고 off 를 n 만큼 늘려 다시 읽는 일을 25회 반복한다. "
      "n 이 0 이면 닫힘 상태가 되어 소켓과 파일을 닫는다. 아래 줄은 400,001 바이트 파일에서 off 가 바뀐 값이다.",
      "읽다 만 자리와 응답할 소켓이 job_t 에 남아 다음 완료 핸들러가 이어받습니다")

# 상태 박스
S1 = (200, 164, 300, 96)
S2 = (644, 180, 208, 64)
d.tone(*S1, ACC, 8, "14", 1.4)
d.t(S1[0] + S1[2] / 2, S1[1] + 32, "읽는 중", 15, ACC, KR, "middle", 600)
d.t(S1[0] + S1[2] / 2, S1[1] + 58, "job_t { sd, off }", 14, INK, MONO, "middle", 600)
d.t(S1[0] + S1[2] / 2, S1[1] + 80, "used = 1", 12, MUTED, MONO)
d.tone(*S2, OK, 8, "14", 1.2)
d.t(S2[0] + S2[2] / 2, S2[1] + 28, "닫힘", 15, OK, KR, "middle", 600)
d.t(S2[0] + S2[2] / 2, S2[1] + 50, "used = 0", 12, MUTED, MONO)

# 시작점과 진입 전이
sy = S1[1] + S1[3] / 2
d.o.append(f'<circle cx="44" cy="{sy}" r="6" fill="{INK}"/>')
d.arrow([(52, sy), (S1[0] - 4, sy)], MUTED, "ar", 1.4)
d.t(122, sy - 14, "FILE 요청", 12, MUTED, KR, "middle", 600)
d.t(122, sy + 22, "off = 0", 12, MUTED, MONO, "middle")

# 종료 전이
ey = S2[1] + S2[3] / 2
d.arrow([(S1[0] + S1[2] + 2, ey), (S2[0] - 4, ey)], MUTED, "ar", 1.4)
d.t((S1[0] + S1[2] + S2[0]) / 2, ey - 22, "n = 0", 12, MUTED, MONO, "middle", 600)
d.t((S1[0] + S1[2] + S2[0]) / 2, ey - 6, "/ close", 12, MUTED, MONO, "middle")

# 자기 전이: 직각 경로로 위를 돌아 같은 상태로 돌아온다
lx1, lx2, ly = S1[0] + 80, S1[0] + S1[2] - 80, S1[1] - 44
d.arrow([(lx1, S1[1] - 2), (lx1, ly), (lx2, ly), (lx2, S1[1] - 4)], MUTED, "ar", 1.4)
d.t((lx1 + lx2) / 2, ly - 22, "n > 0 / write(sd), off += n", 12, MUTED, MONO, "middle", 600)
d.t((lx1 + lx2) / 2, ly - 6, "aio_read 재호출 · 25회", 12, MUTED, MONO, "middle")

# off 값의 변화
d.t(20, 300, "off 값(400,001 바이트 파일)", 12, MUTED, KR, "start", 600)
vals = [("0", SOFT), ("16,384", SOFT), ("32,768", SOFT), ("…", SOFT), ("393,216", SOFT), ("400,001", OK)]
BW, PITCH, X0, BY, BH = 112, 140, 20, 316, 40
for i, (v, c) in enumerate(vals):
    x = X0 + i * PITCH
    d.tone(x, BY, BW, BH, c, 6, "14", 1.2)
    d.t(x + BW / 2, BY + 25, v, 13, INK, MONO, "middle", 600)
    if i < len(vals) - 1:
        d.arrow([(x + BW + 2, BY + BH / 2), (x + PITCH - 4, BY + BH / 2)], MUTED, "ar", 1.4)

d.legend(388, [("읽는 중 · 이어 읽기", ACC), ("닫힘", OK), ("off 가 지나는 값", SOFT)])
d.save("27-01.continuation-state.svg")
print("ok 27-01 continuation-state")
