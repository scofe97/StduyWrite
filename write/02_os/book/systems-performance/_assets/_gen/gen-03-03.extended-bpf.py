# 03-03 §6 — 원서 그림 3.16 BPF components 재구성: 유저 쪽 BPF 도구 · 커널 쪽 검증기와 BPF · 이벤트 세 묶음 · 출력 두 길.
# 타입 스펙: type-architecture — 유저 / 커널 두 구역 안의 구성요소와 연결이다.
#           옛 손 SVG(이벤트 → 검증기 → 실행 → 출력 한 줄 흐름, 유저·커널 경계 없음)를 대체한다.
#           축약: 이벤트 연결은 세로 버스 하나로 모은다(대각선 금지). 열 x = 48 · 232 · 432 · 704, 행 stride 72.
#           focal 은 검증기.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 960, 636
d = DK(W, H, "SYSTEMS PERFORMANCE · 03-03 §6",
       "Extended BPF 구성 — 유저 쪽 도구에서 커널의 이벤트와 출력까지",
       "원서 그림 3.16. 유저 쪽 BPF 도구가 프로그램을 바이트코드로 만들어 넘기면, 커널은 검증기로 안전을 확인한 뒤 BPF 로 적재하고 이벤트에 붙인다. 결과는 per-event 데이터(perf buffer)와 통계 · 스택(map) 두 길로 돌아온다.",
       "커널을 깨지 않는다는 보장은 검증기에서 나옵니다")

UZ, KZ, ZY, ZH = 24, 392, 104, 452
d.box(UZ, ZY, 344, ZH, PAPER, RULE, 1.0, 10)
d.box(KZ, ZY, 544, ZH, PAPER, RULE, 1.0, 10)
d.t(UZ + 16, ZY + 24, "USER", 12, SOFT, MONO, "start", 600)
d.t(KZ + 16, ZY + 24, "KERNEL", 12, SOFT, MONO, "start", 600)

def blk(x, y, w, h, t1, t2=None, c=None):
    if c: d.tone(x, y, w, h, c, 6)
    else: d.box(x, y, w, h, PAPER2, RULE, 1.0, 6)
    d.t(x + w / 2, y + (20 if t2 else h / 2 + 5), t1, 13, c if c else INK, KR if any("가" <= ch <= "힣" for ch in t1) else MONO, "middle", 600)
    if t2: d.t(x + w / 2, y + 38, t2, 12, MUTED, KR)

# 유저 쪽
blk(48, 144, 136, 48, "BPF 프로그램", "BCC · bpftrace")
blk(212, 144, 136, 48, "BPF 바이트코드")
blk(48, 248, 136, 48, "이벤트 설정")
blk(48, 384, 136, 48, "per-event 데이터")
blk(48, 456, 136, 48, "통계 · 스택")
d.arrow([(184, 168), (208, 168)], MUTED, "ar", 1.3)

# 커널 쪽
blk(432, 136, 64, 32, "BTF")
blk(432, 184, 160, 48, "검증기", "verifier", ACC)
blk(432, 248, 160, 48, "BPF", "명령 집합 · helper")
blk(432, 384, 104, 48, "perf buffer")
blk(432, 456, 160, 48, "maps", "stacks")
# 바이트코드 → 검증기
d.arrow([(280, 192), (280, 208), (428, 208)], MUTED, "ar", 1.4)
# BTF ↔ 검증기 (짧은 세로)
d.line(464, 168, 464, 184, MUTED, 1.0)
# 검증기 → BPF
d.arrow([(512, 232), (512, 244)], MUTED, "ar", 1.4)
# 이벤트 설정 → BPF
d.arrow([(184, 272), (428, 272)], MUTED, "ar", 1.4, "4 4")
# BPF → perf buffer, BPF → maps
d.arrow([(472, 296), (472, 380)], INFO, "info", 1.4)
d.arrow([(568, 296), (568, 452)], OK, "ok", 1.4)
# perf buffer → per-event 데이터, maps → 통계
d.arrow([(432, 408), (188, 408)], INFO, "info", 1.4)
d.arrow([(432, 480), (188, 480)], OK, "ok", 1.4)

# 이벤트 세 묶음
EX, EW = 720, 176
GROUPS = [("정적 트레이싱", ["Sockets", "Tracepoints", "USDT"], 136),
          ("동적 트레이싱", ["kprobes", "uprobes"], 308),
          ("샘플링 · PMC", ["perf_events"], 440)]
ys = []
for g, items, gy in GROUPS:
    d.t(EX, gy - 8, g, 12, SOFT, KR, "start", 600)
    for k, it in enumerate(items):
        y = gy + k * 40
        d.box(EX, y, EW, 32, PAPER2, RULE, 1.0, 4)
        d.t(EX + EW / 2, y + 21, it, 12, INK, MONO)
        ys.append(y + 16)
BUS = 664
d.line(BUS, min(ys), BUS, max(ys), WARN, 1.2)
for y in ys: d.line(BUS, y, EX, y, WARN, 1.2)
d.arrow([(BUS, 272), (596, 272)], WARN, "warn", 1.5)
d.t(BUS - 8, 264, "이벤트", 12, WARN, KR, "end", 600)

d.legend(ZY + ZH + 24, [("안전 확인", ACC), ("이벤트", WARN), ("per-event 출력", INFO), ("통계 출력", OK)])
d.save("03-03.extended-bpf.svg")
