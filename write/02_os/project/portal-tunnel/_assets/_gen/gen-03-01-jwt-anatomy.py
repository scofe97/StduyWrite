# 사실 출처: RFC 7515 §7.1 · RFC 7519 §3 · RFC 6750 · RFC 8812 §3.2 · portal/identity/lease_token.go:16-125
# 타입 스펙: type-layers
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 540
d = D(
    W, H,
    "LAYERS · JWT TOKEN ANATOMY",
    "JWT 세 부분의 해부와 컴팩트 직렬화 (ES256K / RFC 8812)",
    "Header·Payload·Signature 세 계층이 Base64URL과 점(.)으로 결합되는 토큰 구조",
    lead="공개키 기반 무상태 인증을 위해 세 부분의 역할과 서명 알고리즘을 계층별로 분리합니다"
)

# 좌측 방향 표시 (논리 요소 ↑ / 와이어 직렬화 ↓)
d.t(48, 116, "논리 요소 ↑", 10, SOFT, fam=KR, anchor="middle", weight=600)
d.arrow([(48, 412), (48, 130)], SOFT, "soft", 1.2)
d.t(48, 428, "직렬화 ↓", 10, SOFT, fam=KR, anchor="middle")

LX, LW = 92, 856
layers = [
    ("01", "JOSE Header", "RFC 7515 · alg ES256K / typ JWT",
     "alg: ES256K", "base64url(Header) · 서명 규격 지정",
     PAPER2, RULE, INK, INFO),
    ("02", "JWT Claims Set", "RFC 7519 · iss / sub / aud / exp",
     "aud: portal-sdk", "base64url(Payload) · 용도 분리 클레임",
     PAPER2, RULE, INK, INFO),
    ("03", "JWS Signature", "secp256k1.Sign(SHA256(H.P))",
     "64B (r || s)", "base64url(Sig) · 위조 방지 타원곡선 서명",
     f"{ACC}14", ACC, ACC, ACC),
    ("04", "Compact Wire", "RFC 7515 §7.1 (Compact) · Bearer 는 RFC 6750",
     "헤더 . 페이로드 . 서명", "점(.) 2개로 결합된 단일 와이어 문자열",
     PAPER2, RULE, INK, OK),
]

y0 = 104
h_layer = 68
gap = 16

for i, (tag, name, path_txt, chip_txt, note, fill, stroke, text_col, chip_col) in enumerate(layers):
    y = y0 + i * (h_layer + gap)
    is_focal = (stroke == ACC)
    d.box(LX, y, LW, h_layer, fill=fill, stroke=stroke, sw=1.4 if is_focal else 1.0, r=6)

    # 인덱스 태그
    d.box(LX + 14, y + 14, 30, 24, fill=PAPER, stroke=stroke, sw=0.8, r=4)
    d.t(LX + 29, y + 30, tag, 10.5, stroke if is_focal else SOFT, fam=MONO, anchor="middle", weight=600)

    # 계층 이름 및 사양
    d.t(LX + 56, y + 26, name, 13, text_col, fam=KR, anchor="start", weight=600)
    d.t(LX + 56, y + 48, path_txt, 10, MUTED if not is_focal else INK, fam=MONO, anchor="start")

    # 칩 (중앙)
    d.chip(LX + 470, y + 34, chip_txt, chip_col, size=10.5)

    # 설명 노트 (우측)
    d.t(LX + LW - 18, y + 38, note, 11, MUTED if not is_focal else INK, fam=KR, anchor="end")

# 범례
legend_y = 464
d.legend(legend_y, [
    ("토큰 메타데이터 및 클레임 계층", INFO),
    ("위조 방지 암호학적 서명 계층 (Focal)", ACC),
    ("네트워크 전송 직렬화 와이어 형식", OK),
])

out_path = Path(__file__).parent.parent / "03-01-jwt-anatomy.svg"
d.save(str(out_path))
print(f"saved: {out_path}")
