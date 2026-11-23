# 타입 스펙: type-flowchart
# 4절 연결 단절과 진행 중 빌드의 운명 — 채널 단절 뒤 동기 호출과 durable-task sh step 의 생존·실패 갈림
import pathlib
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import (D, PAPER2, INK, MUTED, RULE, ACC,  # noqa: E402
                BAD, INFO, KR, MONO)

W, H = 960, 776

d = D(
    W, H,
    "JENKINS · CHANNEL DISCONNECT FATES",
    "채널 단절 뒤 진행 중 step 의 갈림",
    "Remoting 채널이 닫힌 뒤 동기 원격 호출의 즉시 실패와 durable-task sh step 의 5분 대기·재개·중단·취소 분기",
    lead="Remoting 채널이 닫힌 뒤 동기 원격 호출과 durable-task sh step 의 생존 및 종료 분기"
)


def _fam(txt):
    return KR if any("가" <= ch <= "힣" for ch in str(txt)) else MONO


def oval_node(x, y, w, h, title, sub, c, focal=False):
    r = h // 2
    if focal:
        d.tone(x, y, w, h, c, r=r, op="12", sw=1.4)
        tc = c
    else:
        d.box(x, y, w, h, PAPER2, c, 1.2, r)
        tc = INK
    tfam, sfam = _fam(title), _fam(sub)
    ssz = 11 if sfam == MONO and len(sub) > 20 else (12 if sfam == MONO and len(sub) > 16 else 13)
    d.t(x + w / 2, y + 24, title, 14, tc, tfam, "middle", 600)
    d.t(x + w / 2, y + 44, sub, ssz, MUTED, sfam, "middle")


def step_box(x, y, w, h, title, sub, c=INFO):
    d.box(x, y, w, h, PAPER2, c, 1.1, 6)
    tfam, sfam = _fam(title), _fam(sub)
    d.t(x + w / 2, y + 24, title, 14, INK, tfam, "middle", 600)
    d.t(x + w / 2, y + 44, sub, 13, MUTED, sfam, "middle")


def diamond(cx, cy, hw, hh, line1, line2, c=RULE):
    pts = f"{cx},{cy - hh} {cx + hw},{cy} {cx},{cy + hh} {cx - hw},{cy}"
    d.o.append(f'<polygon points="{pts}" fill="{PAPER2}" stroke="{c}" stroke-width="1.2"/>')
    d.t(cx, cy - 4, line1, 13, INK, _fam(line1), "middle", 600)
    d.t(cx, cy + 14, line2, 13, MUTED, _fam(line2), "middle")


CX = 356

# ── Arrows (z-order: behind nodes) ─────────────────────────────────────
# Start -> Diamond 1
d.arrow([(CX, 160), (CX, 196)], INFO, "info", 1.3)

# Diamond 1 -> 동기 호출 (우측)
d.arrow([(CX + 96, 232), (596, 232)], BAD, "bad", 1.3)
d.t(524, 220, "동기 · checkout", 13, BAD, KR, "middle", 600)
d.arrow([(744, 232), (780, 232)], BAD, "bad", 1.3)

# Diamond 1 -> sh (아래)
d.arrow([(CX, 268), (CX, 316)], INFO, "info", 1.3)
d.t(CX + 12, 296, "durable-task · sh", 13, INFO, KR, "start", 600)

# ws 비움 -> Diamond 2
d.arrow([(CX, 372), (CX, 408)], INFO, "info", 1.3)

# Diamond 2 -> 5분 초과 (좌측 아래 L-경로)
d.path(f"M {CX - 104} 444 H 128 Q 120 444 120 452 V 528", BAD, sw=1.3, m="bad")
d.t(186, 432, "5분 초과", 13, BAD, KR, "middle", 600)

# Diamond 2 -> 일회용 노드 삭제 (우측)
d.arrow([(CX + 104, 444), (596, 444)], BAD, "bad", 1.3)
d.t(528, 432, "일회용 노드 삭제", 13, BAD, KR, "middle", 600)

# Diamond 2 -> 5분 내 재연결 (아래)
d.arrow([(CX, 480), (CX, 528)], ACC, "acc", 1.4)
d.t(CX + 12, 508, "5분 내 재연결", 13, ACC, KR, "start", 600)

# Diamond 3 -> 생존 예 (우측 · focal 경로)
d.arrow([(CX + 96, 564), (596, 564)], ACC, "acc", 1.5)
d.t(524, 552, "예 · 셸 생존", 13, ACC, KR, "middle", 600)

# Diamond 3 -> 이미 종료 (아래)
d.arrow([(CX, 600), (CX, 640)], BAD, "bad", 1.3)
d.t(CX + 12, 624, "아니오 · 이미 종료", 13, BAD, KR, "start", 600)

# ── Nodes ──────────────────────────────────────────────────────────────
oval_node(CX - 112, 108, 224, 52, "Channel 단절", "Channel.close · terminate", INFO)

diamond(CX, 232, 96, 36, "실행 중인", "step 종류", INFO)
step_box(596, 204, 148, 56, "Channel.call 대기", "pendingCalls", INFO)
oval_node(780, 204, 156, 56, "즉시 실패", "RequestAborted", BAD)

step_box(CX - 120, 316, 240, 56, "ws 핸들 비움 · 재연결 대기", "백그라운드 래퍼 · 기본 5분", INFO)

diamond(CX, 444, 104, 36, "5분 내 재연결", "및 노드 상태", INFO)
oval_node(16, 528, 208, 56, "타임아웃 중단", "RemovedNodeTimeoutCause", BAD)
oval_node(596, 416, 184, 56, "즉시 취소", "RemovedNodeListener", BAD)

diamond(CX, 564, 96, 36, "셸 프로세스", "생존 여부", ACC)
oval_node(596, 536, 184, 56, "감시 재개", "watch · 폴링 이어감", ACC, focal=True)
oval_node(CX - 92, 640, 184, 56, "실패 종료", "래퍼 종료 확인", BAD)

# ── Legend ─────────────────────────────────────────────────────────────
d.legend(720, [
    ("대기 · 상태 확인", INFO),
    ("실패 · 중단 · 취소", BAD),
    ("생존 · 감시 재개", ACC),
])

out_path = sys.argv[1] if len(sys.argv) > 1 else str(pathlib.Path(__file__).resolve().parent.parent / "01-03.disconnect-fates.svg")
d.save(out_path)
print(f"saved: {out_path}")
