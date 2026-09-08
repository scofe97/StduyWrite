# 11-04 전체 지도 — 경량 가상화에서 기타 유형, 그리고 셋의 비교.
# 타입 스펙: type-layers — 네 절이 구체 기술에서 비교·판단으로 올라가는 지도다.
#           축약: OSI 층이 아니므로 인덱스 태그를 절 번호로 채운다.
import sys; sys.path.insert(0, ".")
from ddk import DK
from dd import D, ACC, MUTED, SOFT, INK, INFO, OK, WARN, PAPER, PAPER2, RULE, KR, MONO

W, H = 928, 520
BX, BW, BH, Y0, STRIDE = 96, 736, 68, 116, 78

d = DK(W, H, "SYSTEMS PERFORMANCE · 11-04",
       "경량 가상화와 세 기술의 비교",
       "11-04 가 다루는 네 절. 경량 가상화가 양쪽 장점을 어떻게 얻는지 보고, 기타 유형을 거쳐, 세 기술을 관측성 기준으로 비교한다.",
       "마지막 절이 11장 전체의 결론입니다 — 관측성이 선택을 가릅니다")

BANDS = [
    ("§1", "경량 가상화", "Firecracker · Kata · gVisor", "양쪽의 장점을 노린다", None),
    ("§2", "관측", "VM 처럼 게스트가 자체 커널을 본다", "컨테이너와 다르다", None),
    ("§3", "기타 유형", "FaaS · SaaS · Unikernel", "로그인할 OS 가 없다", None),
    ("§4", "세 기술 비교", "관측성이 선택을 가른다", "누가 분석하는가로 갈린다", ACC),
]

for i, (tag, name, sub, role, c) in enumerate(BANDS):
    y = Y0 + i * STRIDE
    if c: d.tone(BX, y, BW, BH, c, 8)
    else: d.box(BX, y, BW, BH, PAPER2, RULE, 1.0, 8)
    d.t(BX - 24, y + 40, tag, 13, c if c else SOFT, MONO, "end", 600)
    d.t(BX + 20, y + 30, name, 14, c if c else INK, KR, "start", 600)
    d.t(BX + 20, y + 52, sub, 13, MUTED, KR, "start")
    d.t(BX + BW - 20, y + 40, role, 13, c if c else SOFT, KR, "end")

d.t(BX - 60, Y0 + 4, "기술", 13, SOFT, KR, "middle")
d.arrow([(BX - 60, Y0 + 16), (BX - 60, Y0 + 3 * STRIDE + BH - 8)], SOFT, "soft", 1.2, "4 6")
d.t(BX - 60, Y0 + 3 * STRIDE + BH + 16, "판단", 13, SOFT, KR, "middle")

d.t(BX, Y0 + 4 * STRIDE + 12, "경량 VM 은 컨테이너의 단점을 풀되 통합 캐시 같은 일부 장점을 대가로 냅니다", 13, MUTED, KR, "start")

d.legend(Y0 + 4 * STRIDE + 36, [("11장 전체의 결론", ACC), ("나머지 절", MUTED)])
d.save("11-04.chapter-overview.svg")
