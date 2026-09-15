# 타입 스펙: type-data-flow — 같은 OSPF 패킷 띠를 세 번 옮겨 그린다. 캡슐화에서 인증 칸이 놓인 자리 →
#       인증 칸에 싣는 값 셋 → 받는 라우터가 버리는 두 패킷.
#       축약: 역할 레인 없이 패킷 띠 자체가 단계를 건너간다. gen-04-03.crc-check.py 와 같은 문법이다.
# 출처: 《Computer Networking A Top-Down Approach》 9판 §5.3 "Security" (인쇄 347쪽)
#       "By default, OSPF packets between routers are not authenticated and could be forged"
#       "With simple authentication ... it includes the password in plaintext"
#       "the router computes the MD5 hash of the content of the OSPF packet appended with the secret key"
#       "The receiving router, using the preconfigured secret key, will compute an MD5 hash of the packet and compare it"
#       "Sequence numbers are also used with MD5 authentication to protect against replay attacks"
#       같은 절 — OSPF 메시지는 IP 위에 직접 · 상위 프로토콜 89. BGP 의 TCP 포트 179 는 원문 §5.4.2.
# 원문 밖(RFC 2328 부록 D, https://www.rfc-editor.org/rfc/rfc2328.txt):
#       AuType 0 Null · 1 Simple password · 2 Cryptographic (Table 20). 64비트 Authentication 필드.
#       암호 인증에서 이 필드 = Key ID · Auth Data Len · 32비트 순서 번호 (Figure 18), 다이제스트는 패킷 끝에 붙음 (D.3).
#       수신 — 순서 번호가 기록보다 작으면 폐기, 재계산한 다이제스트가 다르면 폐기 (D.5.3).
# 노트의 읽기: 포트가 없다는 사실과 인증 칸을 잇는 ACC 연결선. 원문은 둘을 잇지 않는다.
# focal: 첫 단의 OSPF 헤더 칸 — 포트가 없는 패킷에서 상대를 확인할 자리.
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import D, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 776
d = D(W, H, "SECTION 5.3 · OSPF SECURITY",
      "포트가 없는 OSPF 는 인증 값을 자기 패킷에 싣습니다",
      "BGP 는 TCP 포트 179 위에서 돌지만 OSPF 는 IP 위에 직접 실려 전송 계층 헤더와 포트가 없다. "
      "그래서 상대를 확인할 값은 OSPF 헤더의 인증 칸에 들어간다(노트의 읽기). 인증 칸은 기본값이면 검사하지 않고, "
      "단순 인증이면 평문 암호를 싣고, MD5 인증이면 키 번호와 순서 번호를 싣고 패킷 끝에 다이제스트를 붙인다. "
      "받는 라우터는 같은 키로 다시 계산한 값이 다르면 위조로, 순서 번호가 기록보다 작으면 재전송으로 보고 버린다.",
      "포트와 인증 칸을 잇는 선은 노트의 읽기, AuType·Key ID·순서 번호 비교는 RFC 2328 부록 D 입니다.")

SH = 44                                   # 패킷 띠 높이


def cell(x, y, w, label, stroke=MUTED, color=INK, h=SH, size=13, fam=KR):
    d.box(x, y, w, h, PAPER2, stroke, 1.1, 5)
    d.t(x + w / 2, y + h / 2 + 5, label, size, color, fam)


def hole(x, y, w, label, h=SH):
    d.path(f"M {x} {y} L {x + w} {y} L {x + w} {y + h} L {x} {y + h} Z", MUTED, 1.1, dash="5 4")
    d.t(x + w / 2, y + h / 2 + 5, label, 13, MUTED, KR)


# ── 1. 캡슐화 — 포트가 들어갈 자리 ──
d.t(24, 112, "1. 캡슐화 · 포트가 들어갈 자리", 13, INK, KR, "start", 600)
d.t(24, 154, "BGP", 13, MUTED, MONO, "start", 600)
cell(96, 128, 196, "IP 헤더")
cell(296, 128, 228, "TCP 헤더 · 포트 179")
cell(528, 128, 448, "BGP 메시지")

d.t(24, 210, "OSPF", 13, INK, MONO, "start", 600)
cell(96, 184, 196, "IP 헤더 · 프로토콜 89")
hole(296, 184, 228, "TCP·UDP 헤더 없음 · 포트 없음")
d.tone(528, 184, 228, SH, ACC, 5, "14", 1.4)
d.t(642, 211, "OSPF 헤더 · 인증 칸", 13, ACC, KR, "middle", 600)
cell(760, 184, 216, "링크 상태 광고")

# 노트의 읽기 — 포트로 못 가리는 상대를 인증 칸에서 확인
d.arrow([(642, 228), (642, 256), (304, 256), (304, 292)], ACC, "acc", 1.6)
d.t(660, 252, "상대 확인은 인증 칸에서 · 노트의 읽기", 13, ACC, KR, "start", 600)

# ── 2. 인증 칸에 싣는 값 셋 ──
d.t(24, 280, "2. 인증 칸 설정 셋", 13, INK, KR, "start", 600)
d.t(304, 316, "OSPF 헤더의 인증 칸", 12, ACC, KR, "middle", 600)
d.t(524, 316, "OSPF 본문", 12, MUTED, KR)
d.t(684, 316, "패킷 끝", 12, MUTED, KR)
d.t(772, 316, "받는 쪽", 12, MUTED, KR, "start")

ROWS = [
    (BAD,  "기본값",   "AuType 0", "검사 안 함",          None,             "위조 링크 상태도 수락"),
    (WARN, "단순 인증", "AuType 1", "평문 암호",           None,             "엿듣기로 암호 노출"),
    (OK,   "MD5 인증", "AuType 2", "Key ID · 순서 번호",  "MD5 다이제스트", "같은 키로 재계산 · 비교"),
]
Y2, STRIDE = 328, 56
for i, (c, name, autype, auth, digest, verdict) in enumerate(ROWS):
    y = Y2 + i * STRIDE
    d.t(24, y + 20, name, 13, c, KR, "start", 600)
    d.t(24, y + 38, autype, 11, SOFT, MONO, "start")
    cell(176, y, 256, auth, c, INK, h=40)
    cell(436, y, 176, "링크 상태 광고", h=40)
    if digest:
        cell(616, y, 136, digest, c, INK, h=40)
    d.t(772, y + 25, verdict, 13, c, KR, "start", 600)

# ── 3. MD5 인증에서 버려지는 두 패킷 ──
d.t(24, 520, "3. MD5 인증에서 버려지는 두 패킷", 13, INK, KR, "start", 600)

CASES = [
    (24, "위조 · 링크 상태를 바꿈",
     [("순서 번호", MUTED), ("틀린 링크 상태", BAD), ("다이제스트", MUTED)],
     [("같은 키로 재계산 · 실린 값과 다름", BAD)]),
    (508, "재전송 · 앞서 받은 패킷 그대로",
     [("옛 순서 번호", BAD), ("링크 상태 광고", MUTED), ("다이제스트", MUTED)],
     [("같은 키로 재계산 · 실린 값과 같음", OK), ("순서 번호 · 기록보다 작음", BAD)]),
]
for x0, head, parts, checks in CASES:
    d.box(x0, 536, 468, 168, f"{INK}05", RULE, 1.0, 8)
    d.t(x0 + 20, 560, head, 13, INK, KR, "start", 600)
    px = x0 + 20
    for (lab, c), w in zip(parts, (128, 160, 128)):
        cell(px, 576, w - 4, lab, c, INK, h=36)
        px += w
    for k, (lab, c) in enumerate(checks):
        d.t(x0 + 20, 636 + k * 24, lab, 13, c, KR, "start")
    d.t(x0 + 448, 688, "폐기", 13, BAD, KR, "end", 600)

d.legend(728, [("노트의 읽기 · 인증 칸", ACC), ("받아들여지는 값", OK), ("엿듣기에 드러나는 값", WARN), ("위조·재전송", BAD)])
d.t(960, 768, "KUROSE-ROSS 9E 5.3 P.347 · RFC 2328 APP. D", 8, SOFT, MONO, "end")

out = pathlib.Path(__file__).resolve().parent.parent / "05-02.ospf-security.svg"
d.save(out)
print("→", out)
