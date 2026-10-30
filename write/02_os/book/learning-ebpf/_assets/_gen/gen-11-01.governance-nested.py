# 타입 스펙: type-nested — Linux Foundation ⊃ {eBPF Foundation ⊃ BSC, CNCF ⊃ Cilium·Falco·Pixie}, IETF ⊃ BPF WG → RFC 9669, Linux 커널 ⊃ BPF 서브시스템. BSC — IETF 사이 점선 협력선(화살촉 없음).
# 사실 출처: LF 보도자료 2021-08-12(재단은 Linux Foundation 이 호스팅), 헌장 L46~48(BSC 구성·한 회사 최대 2명), IETF BPF WG 헌장(재단 운영위원회와 협력 명시) · RFC 9669,
#   cncf/landscape landscape.yml(커밋 5ebec81) L3834~3849(Cilium graduated 2023-10-11) · L1432~1444(Falco 2024-02-29) · L12326~12336(Pixie sandbox),
#   v7.2 MAINTAINERS L4899~4912(BPF [GENERAL], bpf@vger.kernel.org, M: 다섯 줄).
# Layout conventions: 바깥 상자 rx=8, 안쪽 상자 인셋 24px, 상자 이름은 왼쪽 위 mono eyebrow. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, BAD, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

W, H = 960, 520
d = D(W, H, "LEARNING EBPF · 11-01 §1",
      "재단은 자금과 방향을, IETF 는 명령어 집합을, 커널은 코드를 맡는다",
      "Linux Foundation 아래 eBPF Foundation 과 CNCF 가 있고, IETF 와 리눅스 커널은 별도 기관이다. 운영위원회가 워킹그룹과 협력한다.",
      "바깥 상자가 안쪽 상자를 품는다")


def fam(s):
    return KR if any("가" <= c <= "힣" for c in s) else MONO


def ring(x, y, w, h, label, c, op="0A"):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="{c}{op}" stroke="{c}" stroke-width="1.2"/>')
    kr = any("가" <= ch <= "힣" for ch in label)
    d.t(x + 16, y + 20, label, 11 if kr else 9, SOFT, KR if kr else MONO, "start")


def item(x, y, w, h, c, l1, l2=None, focal=False):
    d.tone(x, y, w, h, c, 6, "1F" if focal else "12", 1.6 if focal else 1.2)
    if l2:
        d.t(x + w / 2, y + 22, l1, 13, INK, fam(l1), "middle", 600)
        d.t(x + w / 2, y + 42, l2, 12, MUTED, fam(l2))
    else:
        d.t(x + w / 2, y + h / 2 + 5, l1, 13, INK, fam(l1), "middle", 600)


# 협력선(점선)은 상자보다 먼저. 헌장은 두 쪽의 협력을 적을 뿐 방향을 정하지 않으므로 화살촉을 달지 않는다.
d.path("M172 212 V124 H616", INFO, 1.4, None, "5 4")
d.chip(400, 124, "협력", INFO, 12)

# 색은 기관 종류 하나로 가른다: 재단(파랑) · 재단 밖 기관(회색) · CNCF 성숙도(초록 졸업 · 노랑 샌드박스). focal 은 RFC 9669 하나.
ring(24, 96, 560, 316, "LINUX FOUNDATION", INFO)
ring(48, 148, 248, 236, "eBPF FOUNDATION", INFO)
item(72, 212, 200, 84, INFO, "BSC", "회사당 최대 2명")
ring(320, 148, 240, 236, "CNCF", INFO)
item(340, 180, 200, 52, OK, "Cilium", "졸업 2023-10-11")
item(340, 244, 200, 52, OK, "Falco", "졸업 2024-02-29")
item(340, 308, 200, 52, WARN, "Pixie", "샌드박스")

ring(616, 96, 320, 140, "IETF", MUTED)
item(636, 136, 128, 72, MUTED, "BPF WG")
item(792, 136, 128, 72, ACC, "RFC 9669", None, True)
d.arrow([(764, 172), (788, 172)], ACC, "acc", 1.5)

ring(616, 268, 320, 144, "리눅스 커널", MUTED)
item(636, 308, 280, 76, MUTED, "BPF 서브시스템", "bpf@vger.kernel.org · 메인테이너 5명")

d.legend(H - 56, [("재단 · 위원회", INFO), ("CNCF 졸업", OK), ("CNCF 샌드박스", WARN), ("별도 기관", MUTED), ("표준", ACC)])
d.save("11-01.governance-nested.svg")
