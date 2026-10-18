# 타입 스펙: type-state
# 사실 출처: portal/lease.go:26-35, 136, 152, 184, 337, 593, 722, 872, portal/server.go:1054, docs/maintainer/architecture.md
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, OK, WARN, BAD, INFO, ACC, KR, MONO

W, H = 960, 500
d = D(W, H, "PORTAL-TUNNEL · LEASE LIFECYCLE & IDENTITY STATE",
      "임대 상태 머신과 접근 제어 수명주기",
      "SIWE 챌린지 발급부터 fail-closed 격리, 라우팅 승인, 갱신, 만료 및 포트 유예 정리까지의 전이",
      lead="등록 직후 격리 상태를 거쳐 오케스트레이터 접근 판정 후 라우팅이 활성화됩니다")

# 0. 시작 기호 (Start dot)
sx, sy = 28, 178
d.o.append(f'<circle cx="{sx}" cy="{sy}" r="6" fill="{INK}"/>')
d.t(sx, sy - 14, "Start", 9, SOFT, MONO, "middle")

# 1. State: Challenge Pending
s1_x, s1_y, s1_w, s1_h = 104, 144, 200, 68
d.box(s1_x, s1_y, s1_w, s1_h, fill=PAPER2, stroke=INFO, sw=1.2, r=8)
d.t(s1_x + 14, s1_y + 22, "CHALLENGE PENDING", 9, INFO, MONO, "start", 600)
d.t(s1_x + 14, s1_y + 40, "1. 챌린지 대기", 12, INK, KR, "start", 600)
d.t(s1_x + 14, s1_y + 57, "TTL 2분 · IP당 32개 한도", 11, MUTED, KR, "start")

# 2. State: Registered (Suspended)
s2_x, s2_y, s2_w, s2_h = 384, 144, 208, 68
d.box(s2_x, s2_y, s2_w, s2_h, fill=PAPER2, stroke=WARN, sw=1.2, r=8)
d.t(s2_x + 14, s2_y + 22, "REGISTERED (SUSPENDED)", 9, WARN, MONO, "start", 600)
d.t(s2_x + 14, s2_y + 40, "2. 등록 격리 (fail-closed)", 12, INK, KR, "start", 600)
d.t(s2_x + 14, s2_y + 57, "isRoutable=false · 캐시 분리", 11, MUTED, KR, "start")

# 3. State: Routable (Focal)
s3_x, s3_y, s3_w, s3_h = 672, 144, 208, 68
d.box(s3_x, s3_y, s3_w, s3_h, fill=PAPER2, stroke=OK, sw=1.4, r=8)
d.t(s3_x + 14, s3_y + 22, "ROUTABLE (ACTIVE)", 9, OK, MONO, "start", 600)
d.t(s3_x + 14, s3_y + 40, "3. 라우팅 활성", 12, INK, KR, "start", 600)
d.t(s3_x + 14, s3_y + 57, "isRoutable=true · 트래픽 중계", 11, MUTED, KR, "start")

# 4. State: Revoked / Expired / Denied
s4_x, s4_y, s4_w, s4_h = 672, 292, 208, 68
d.box(s4_x, s4_y, s4_w, s4_h, fill=PAPER2, stroke=BAD, sw=1.2, r=8)
d.t(s4_x + 14, s4_y + 22, "REVOKED / EXPIRED", 9, BAD, MONO, "start", 600)
d.t(s4_x + 14, s4_y + 40, "4. 종료 및 차단", 12, INK, KR, "start", 600)
d.t(s4_x + 14, s4_y + 57, "진행 bridge 즉시 취소", 11, MUTED, KR, "start")

# 5. State: Cleanup & Grace
s5_x, s5_y, s5_w, s5_h = 384, 292, 208, 68
d.box(s5_x, s5_y, s5_w, s5_h, fill=PAPER2, stroke=RULE, sw=1.2, r=8)
d.t(s5_x + 14, s5_y + 22, "CLEANUP & GRACE", 9, SOFT, MONO, "start", 600)
d.t(s5_x + 14, s5_y + 40, "5. 정리 및 유예", 12, INK, KR, "start", 600)
d.t(s5_x + 14, s5_y + 57, "DNS 삭제 · 포트 유예 5분", 11, MUTED, KR, "start")

# 6. 종료 기호 (End ringed dot)
ex, ey = 244, 326
d.o.append(f'<circle cx="{ex}" cy="{ey}" r="8" fill="none" stroke="{MUTED}" stroke-width="1.2"/>')
d.o.append(f'<circle cx="{ex}" cy="{ey}" r="5" fill="{MUTED}"/>')
d.t(ex, ey + 22, "End", 9, SOFT, MONO, "middle")

# ── 전이 화살표 (Transitions) ──

# Start -> State 1
d.arrow([(sx + 8, sy), (s1_x, sy)], c=INFO, m="info", sw=1.4)
d.t((sx + 8 + s1_x) // 2, sy - 8, "발급 요청", 11, INFO, KR, "middle")

# State 1 -> State 2
d.arrow([(s1_x + s1_w, sy), (s2_x, sy)], c=INFO, m="info", sw=1.4)
d.t((s1_x + s1_w + s2_x) // 2, sy - 8, "서명 등록", 11, INFO, KR, "middle")

# State 2 -> State 3
d.arrow([(s2_x + s2_w, sy), (s3_x, sy)], c=OK, m="ok", sw=1.6)
d.t((s2_x + s2_w + s3_x) // 2, sy - 8, "접근 승인", 11, OK, KR, "middle")

# State 3 Self-loop (Renew)
d.arrow([(s3_x + 48, s3_y), (s3_x + 48, s3_y - 28), (s3_x + 160, s3_y - 28), (s3_x + 160, s3_y)], c=ACC, m="acc", sw=1.4)
d.t(s3_x + 104, s3_y - 34, "POST /sdk/renew (스트림 유지)", 11, ACC, KR, "middle")

# State 3 -> State 4 (Revocation/Expiry/Unregister)
d.arrow([(s3_x + 104, s3_y + s3_h), (s3_x + 104, s4_y)], c=BAD, m="bad", sw=1.4)
d.t(s3_x + 104 + 10, (s3_y + s3_h + s4_y) // 2 + 4, "만료 · unregister · 차단", 11, BAD, KR, "start")

# State 2 -> State 5 (Direct Expiry/Deny before approval)
d.arrow([(s2_x + 104, s2_y + s2_h), (s2_x + 104, s5_y)], c=WARN, m="warn", sw=1.4)
d.t(s2_x + 104 + 10, (s2_y + s2_h + s5_y) // 2 + 4, "미승인 만료 · 거부", 11, WARN, KR, "start")

# State 4 -> State 5 (Janitor Cleanup)
d.arrow([(s4_x, ey), (s5_x + s5_w, ey)], c=MUTED, m="ar", sw=1.4)
d.t((s4_x + s5_x + s5_w) // 2, ey - 8, "만료 수거", 11, MUTED, KR, "middle")

# State 5 -> End (Grace Expired)
d.arrow([(s5_x, ey), (ex + 10, ey)], c=MUTED, m="ar", sw=1.4)
d.t((s5_x + ex + 10) // 2, ey - 8, "유예 5분 경과", 11, MUTED, KR, "middle")

# 범례 (Legend)
d.legend(436, [
    ("등록·대기", INFO),
    ("격리 (fail-closed)", WARN),
    ("라우팅 활성", OK),
    ("종료·차단", BAD),
    ("갱신 루프", ACC),
])

out_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "01-06-lease-state.svg"))
d.save(out_path)
print(f"saved: {out_path}")
