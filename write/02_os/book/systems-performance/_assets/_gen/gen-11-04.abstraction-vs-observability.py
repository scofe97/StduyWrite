# 11-04 §3 — 추상이 올라갈수록 로그인할 자리가 사라진다.
# 타입 스펙: type-layers — 추상 수준이 올라갈수록 분석 주체가 옮겨 가는 층 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 추상 단계 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 952, 528
BX, BW, BH, Y0, STRIDE = 156, 676, 64, 116, 76

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-04 §3",
       "추상이 올라가면 분석 자리가 옮겨 간다",
       "서버에서 함수로, 다시 단일 바이너리로 올라갈수록 로그인해 도구를 돌릴 OS 가 사라진다. 분석은 앱 계측이나 운영자·하이퍼바이저 쪽으로 옮겨 간다.",
       "엔드유저가 전통 성능 도구를 쓸 수 있는 범위가 위로 갈수록 줄어듭니다")

BANDS = [
    ("01", "서버 · VM · 컨테이너", "로그인해 도구를 돌립니다", "엔드유저가 분석", OK),
    ("02", "FaaS", "서버가 없어 CLI 도구를 못 씁니다", "앱 타임스탬프에 의존", None),
    ("03", "SaaS", "설정할 서버도 앱도 없습니다", "운영자만 분석", None),
    ("04", "Unikernel", "OS 가 없어 /proc 도 없습니다", "커스텀 도구 · 하이퍼바이저", ACC),
]

for i, (n, name, sub, who, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c is ACC: d.tone(BX, y, BW, BH, c, 8)
    elif c is OK: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 20, y + 38, n, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 28, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 48, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 38, who, 13, c if c else SOFT, KR, "end")

d.t(BX - 132, Y0 + 4, "직접 분석", 13, SOFT, KR, "start")
d.arrow([(BX - 76, Y0 + 16), (BX - 76, Y0 + 3 * STRIDE + BH - 28)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 132, Y0 + 3 * STRIDE + BH - 4, "남에게 의존", 13, SOFT, KR, "start")

YB = Y0 + 4 * STRIDE + 24
d.t(BX - 132, YB, "Unikernel 은 명령 text 를 줄여 CPU 캐시 오염을 낮추지만, 그 대가로 관측 도구를 둘 자리를 없앱니다",
    13, MUTED, KR, "start")

d.legend(YB + 28, [("관측이 가장 어려운 자리", ACC), ("도구를 다 쓸 수 있는 자리", OK), ("중간 단계", MUTED)])
d.save("11-04.abstraction-vs-observability.svg")
