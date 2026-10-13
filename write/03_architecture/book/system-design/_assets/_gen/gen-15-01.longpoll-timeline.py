# 타입 스펙: type-timeline — 0~80 초 가로 축 위에 롱 폴링 요청 셋의 막힘 구간(0~41 s·41~58 s·60 s~)과 58 초의 변경 발생·changes true·list_folder/continue 를 정직한 눈금으로 놓는다.
# 사실 출처: Dropbox API 스펙 files.stone 의 ListFolderLongpollArg·Result·route list_folder/longpoll(dropbox-api-spec 3c363a5, L1869-L1892·L2892):
#   timeout 기본 30 s(30~480 s), "요청은 최대 이 시간에 최대 90 초의 무작위 지터를 더해 막힌다(thundering herd 방지)", 결과 changes(true 면 list_folder/continue 를 부른다)·backoff.
#   41 s = 30 s + 지터 11 s, 58 s 와 60 s(변경 2 초 뒤의 다음 요청)는 설명용 값이다. 추출본 v2.txt 4665~4669행(변경이 감지되면 연결을 닫고 메타데이터에서 받으며 응답이나 타임아웃 직후 즉시 새 요청).
# Layout conventions: 축 y=348, 0 초 x=80·10 px/초(80 초 x=880), 눈금 10 초 간격, 막대 높이 44·줄 stride 64(y=116·180·244). 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, SOFT, RULE, KR, MONO

W, H = 1000, 452
d = D(W, H, "SYSTEM DESIGN INTERVIEW · 15-01 §8",
      "요청은 변경이 있거나 시간이 차면 돌아오고 곧바로 다음 요청이 나간다",
      "변경이 없으면 timeout 에 지터를 더한 시간 뒤 changes false 로 돌아오고, 변경이 있으면 그 즉시 true 로 돌아와 목록을 받는다.",
      "timeout 30 s + 지터 ≤ 90 s")

X0, PX, AY = 80, 10, 348


def xt(t):
    return X0 + PX * t


d.line(X0 - 20, AY, 920, AY, MUTED, 1.2)
for t in range(0, 90, 10):
    d.line(xt(t), AY - 6, xt(t), AY + 6, MUTED, 1.0)
    d.t(xt(t), AY + 28, f"{t} s", 13, SOFT, MONO, "middle")

BARS = (
    (116, 0, 41, INFO, "longpoll #1 · changes false"),
    (180, 41, 58, INFO, "#2 · changes true"),
    (244, 60, 80, INFO, "#3 · 대기 중"),
)
for y, a, b, c, lab in BARS:
    d.tone(xt(a), y, xt(b) - xt(a), 44, c, 6, "14", 1.2)
    d.t(xt(a) + 12, y + 27, lab, 13, INK, MONO, "start", 600)

d.chip(xt(41), 104, "30 + 11 = 41", WARN, 13)
d.arrow([(xt(41), 160), (xt(41), 176)], WARN, "warn", 1.4)
d.line(xt(58), 224, xt(58), AY - 8, ACC, 1.4, "4 4")
d.o.append(f'<circle cx="{xt(58)}" cy="{AY}" r="7" fill="{ACC}"/>')
d.t(xt(58) - 12, 300, "58 s 변경 · list_folder/continue", 13, ACC, KR, "end", 600)

d.legend(H - 56, [("막혀 있는 요청", INFO), ("지터가 붙은 timeout", WARN), ("변경 발생", ACC)])
d.save("15-01.longpoll-timeline.svg")
