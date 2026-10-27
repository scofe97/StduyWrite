# 타입 스펙: type-sequence
# 사실 출처: RFC 8446 §2 (Handshake Protocol Overview), §4.4, NPG Ch.11
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, INFO, KR, MONO

W, H = 880, 848
s = Seq(W, H, "SEQUENCE · TLS 1.3 1-RTT HANDSHAKE",
        "TLS 1.3 핸드셰이크와 키 교환 및 세션 키 생성 순서",
        "클라이언트와 서버가 임시 ECDHE 키 공유를 교환해 세션 대칭 키를 유도하고 암호화 통신을 엽니다.",
        lead="TLS 1.3 은 단 1-RTT 만에 키 교환과 서버 인증 및 핸드셰이크 완료를 마칩니다.")

xc, xs = 220, 660
lane_w = 260
y0 = 104

# 1. 참여자 레인 머리
s.LX = {"클라이언트": xc, "서버": xs}
s.lane_top = y0 + 44

s.box(xc - lane_w / 2, y0, lane_w, 44, fill=PAPER2, stroke=RULE, sw=1.0)
s.t(xc, y0 + 19, "클라이언트", 13, INK, KR, "middle", 600)
s.t(xc, y0 + 35, "TLS Client", 11, MUTED, MONO, "middle")

s.box(xs - lane_w / 2, y0, lane_w, 44, fill=PAPER2, stroke=RULE, sw=1.0)
s.t(xs, y0 + 19, "서버", 13, INK, KR, "middle", 600)
s.t(xs, y0 + 35, "cert.pem(공개 키) · key.pem(개인 키)", 11, MUTED, KR, "middle")

# 2. 생명선 (레일)
y_rail_end = 724
s.line(xc, s.lane_top + 6, xc, y_rail_end, RULE, 1.0, "3 6")
s.line(xs, s.lane_top + 6, xs, y_rail_end, RULE, 1.0, "3 6")

# 3. 활성화 막대
# 상단 세그먼트 (Hello 구간)
s.box(xc - 4, 168, 8, 108, fill=MUTED, stroke=RULE, sw=0.8, r=2)
s.box(xs - 4, 168, 8, 108, fill=MUTED, stroke=RULE, sw=0.8, r=2)

# 하단 세그먼트 (암호화 핸드셰이크 및 데이터 구간)
s.box(xc - 4, 356, 8, 356, fill=MUTED, stroke=RULE, sw=0.8, r=2)
s.box(xs - 4, 356, 8, 356, fill=MUTED, stroke=RULE, sw=0.8, r=2)

mx = (xc + xs) / 2  # 440

# ── 메시지 1: ClientHello ───────────────────────────────────────────
y_m1 = 184
s.path(f"M {xc + 8} {y_m1} L {xs - 10} {y_m1}", INFO, 1.5, m="info")
s.t(mx, y_m1 - 9, "ClientHello", 12, INFO, MONO, "middle", 600)
s.t(mx, y_m1 + 16, "key_share (임시 공개값) · TLS 1.3 · AES-128-GCM", 11, MUTED, KR, "middle")

# ── 메시지 2: ServerHello ───────────────────────────────────────────
y_m2 = 244
s.path(f"M {xs - 8} {y_m2} L {xc + 10} {y_m2}", INFO, 1.5, m="info")
s.t(mx, y_m2 - 9, "ServerHello", 12, INFO, MONO, "middle", 600)
s.t(mx, y_m2 + 16, "key_share (임시 공개값) · 고른 스위트 · ServerRandom", 11, MUTED, KR, "middle")

# ── 양쪽 메모: ECDHE 공유 비밀 및 핸드셰이크 키 유도 ───────────────
y_memo = 284
memo_w, memo_h = 300, 60
s.box(xc - memo_w / 2, y_memo, memo_w, memo_h, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
s.t(xc, y_memo + 19, "자기 임시 키 + 상대 key_share", 11, INK, KR, "middle")
s.t(xc, y_memo + 36, "→ ECDHE 공유 비밀 (비전송)", 11, MUTED, KR, "middle")
s.t(xc, y_memo + 51, "→ HKDF → 핸드셰이크 키", 11, OK, MONO, "middle", 600)

s.box(xs - memo_w / 2, y_memo, memo_w, memo_h, fill=PAPER2, stroke=INFO, sw=1.0, r=6)
s.t(xs, y_memo + 19, "자기 임시 키 + 상대 key_share", 11, INK, KR, "middle")
s.t(xs, y_memo + 36, "→ ECDHE 공유 비밀 (비전송)", 11, MUTED, KR, "middle")
s.t(xs, y_memo + 51, "→ HKDF → 핸드셰이크 키", 11, OK, MONO, "middle", 600)

# ── 메시지 3: {EncryptedExtensions, Certificate} ───────────────────
y_m3 = 380
s.path(f"M {xs - 8} {y_m3} L {xc + 10} {y_m3}", OK, 1.5, m="ok")
s.t(mx, y_m3 - 9, "{EncryptedExtensions} · {Certificate}", 12, OK, MONO, "middle", 600)
s.t(mx, y_m3 + 16, "cert.pem 제시 · CA 서명 검증 (§2·§3)", 11, MUTED, KR, "middle")

# ── 메시지 4: {CertificateVerify} — FOCAL (ACCENT) ─────────────────
y_m4 = 448
s.path(f"M {xs - 8} {y_m4} L {xc + 10} {y_m4}", ACC, 2.0, m="acc")
s.t(mx, y_m4 - 9, "{CertificateVerify}", 13, ACC, MONO, "middle", 600)
s.t(mx, y_m4 + 16, "key.pem 으로 기록 서명 (유일한 개인 키 사용처)", 11, ACC, KR, "middle")
s.t(mx, y_m4 + 32, "cert.pem 검증 → [서버의 key.pem 보유 확인]", 11, INK, KR, "middle", 600)

# ── 메시지 5: {Finished} (서버 완료) ───────────────────────────────
y_m5 = 532
s.path(f"M {xs - 8} {y_m5} L {xc + 10} {y_m5}", OK, 1.5, m="ok")
s.t(mx, y_m5 - 9, "{Finished}", 12, OK, MONO, "middle", 600)
s.t(mx, y_m5 + 16, "finished 키로 HMAC 생성 (기록 해시)", 11, MUTED, KR, "middle")
s.t(mx, y_m5 + 32, "HMAC 대조 → [동일 기록 · 동일 키 일치 확인]", 11, OK, KR, "middle", 600)

# ── 메시지 6: {Finished} (클라이언트 완료) ─────────────────────────
y_m6 = 616
s.path(f"M {xc + 8} {y_m6} L {xs - 10} {y_m6}", OK, 1.5, m="ok")
s.t(mx, y_m6 - 9, "{Finished}", 12, OK, MONO, "middle", 600)
s.t(mx, y_m6 + 16, "클라이언트 HMAC 전송 → [동일 기록 · 동일 키 확인]", 11, MUTED, KR, "middle")

# ── 메시지 7: Application Data (양방향) ─────────────────────────────
y_m7 = 676
s.path(f"M {xc + 8} {y_m7} L {xs - 10} {y_m7}", OK, 1.5, m="ok")
s.path(f"M {xs - 8} {y_m7 + 12} L {xc + 10} {y_m7 + 12}", OK, 1.5, m="ok")
s.t(mx, y_m7 - 9, "Application Data (양방향)", 12, OK, MONO, "middle", 600)
s.t(mx, y_m7 + 28, "AES-128-GCM 세션 키 암호화 통신", 11, MUTED, KR, "middle")

# ── 끝 메모: 전방 비밀성 ───────────────────────────────────────────
y_end = 736
s.box(160, y_end, 560, 36, fill=PAPER2, stroke=RULE, sw=0.9, r=6)
s.t(mx, y_end + 22, "임시 키 · 세션 키 폐기 → 전방 비밀성", 11, INK, KR, "middle")

# ── 범례 (LEGEND) ───────────────────────────────────────────────────
s.line(12, 796, W - 12, 796, RULE, 0.8)
s.t(12, 818, "LEGEND", 8, SOFT, MONO, "start")

leg_items = [
    ("ClientHello · ServerHello (평문)", INFO),
    ("CertificateVerify (key.pem 서명)", ACC),
    ("{Finished} · 데이터 (암호화)", OK),
]
lx = 96
for lab, c in leg_items:
    s.o.append(f'<rect x="{lx}" y="808" width="14" height="12" rx="2" fill="{c}22" stroke="{c}" stroke-width="1.1"/>')
    s.t(lx + 22, 818, lab, 11, MUTED, KR, "start")
    w = sum(11.5 if '가' <= ch <= '힣' else 7.0 for ch in lab)
    lx += int(w + 36)

svg_path = pathlib.Path(__file__).resolve().parent.parent / "11-01.tls-handshake.svg"
s.save(str(svg_path))
print("ok 11-01 tls-handshake")
