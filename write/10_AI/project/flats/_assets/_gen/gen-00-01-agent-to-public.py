# 사실 출처: README.md:93-108,156-173,228-253 · docs/design.md Approvals
# 타입 스펙: type-data-flow
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))
from dd import D, PAPER, PAPER2, INK, MUTED, SOFT, RULE, ACC, OK, WARN, BAD, INFO, KR, MONO

W, H = 1000, 560
d = D(
    W, H,
    "DATA FLOW · AGENT TO PUBLIC PIPELINE",
    "에이전트 초안 저장부터 콘솔 승인을 거친 공개까지의 데이터 흐름",
    "에이전트의 초안은 비공개로 격리되며 운영자의 버전 동결·배포·공개 승인을 거쳐야만 단계별로 활성화됩니다",
    "에이전트(save_draft) → 루프백 MCP → Private Draft → create_version 대기 → 콘솔 승인 → vN → deploy 승인 → 라이브 → 공개"
)

# 4개 영역 (Zone) 정의
# 1. 에이전트 & 루프백 통로 (x: 18 ~ 190)
# 2. 로컬 초안 & 버전 동결 (x: 230 ~ 480)
# 3. 로컬 라이브 서빙 (x: 530 ~ 736)
# 4. 외부 네트워크 공개 (x: 826 ~ 988)

def zone(x, y, w, h, label, sub=""):
    d.o.append(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="8" fill="rgba(255,255,255,0.015)" stroke="{RULE}" stroke-width="0.8" stroke-dasharray="3 3"/>')
    d.t(x + 14, y + 20, label, 11, SOFT, KR, "start", 600)
    if sub:
        d.t(x + 14, y + 36, sub, 9, SOFT, MONO, "start")

zone(18, 104, 172, 396, "에이전트 영역", "CLI · MCP 클라이언트")
zone(230, 104, 250, 396, "격리 작업본 및 버전 동결", "루프백 127.0.0.1:7878")
zone(530, 104, 206, 396, "로컬 라이브 서빙", "루프백 127.0.0.1:7879")
zone(826, 104, 162, 396, "외부 네트워크 공개", "제공자 릴레이 연동")

# 1. 에이전트 박스
d.box(30, 170, 150, 80, PAPER2, RULE, 1.0)
d.t(105, 196, "AI 에이전트", 12, INK, KR, "middle", 600)
d.t(105, 216, "Claude Code · Codex", 10, MUTED, KR, "middle")
d.t(105, 234, "save_draft 호출", 10, INFO, MONO, "middle")

# MCP 통로 화살표 (1 -> 2, 간격 60px 확보, 라벨 마진 양옆 10px)
d.arrow([(180, 210), (240, 210)], INFO, "info", 1.4)
d.t(210, 200, "POST", 9, INFO, MONO, "middle")
d.t(210, 226, "/mcp", 9, SOFT, MONO, "middle")

# 2. Private Draft 노드
d.tone(240, 170, 230, 80, INFO, 6, "12", 1.2)
d.t(355, 196, "Private Draft", 12, INFO, KR, "middle", 600)
d.t(355, 216, "호스트 draft-revs 보관", 10, INK, KR, "middle")
d.t(355, 234, "외부 접근 불가 · live 영향 없음", 9, MUTED, KR, "middle")

# 아래로: create_version 요청 (화살표 좌측 오프셋으로 라벨 관통 방지)
d.arrow([(264, 250), (264, 282)], WARN, "warn", 1.4)
d.t(276, 268, "create_version (hash 고정)", 9, WARN, MONO, "start")

# 3. 승인 대기 (pending) & 콘솔 승인 노드
d.tone(240, 284, 230, 100, WARN, 6, "14", 1.2)
d.t(355, 308, "승인 대기 (pending)", 12, WARN, KR, "middle", 600)
d.t(355, 328, "CLI exit 3 · revision/hash 동결", 10, INK, MONO, "middle")
d.t(355, 348, "콘솔 검토: /approvals/apr-*", 10, MUTED, MONO, "middle")
d.t(355, 368, "사람의 명시적 승인 결정", 10, ACC, KR, "middle", 600)

# 아래로: 버전 생성 (화살표 좌측 오프셋으로 라벨 관통 방지)
d.arrow([(264, 384), (264, 416)], OK, "ok", 1.4)
d.t(276, 402, "승인 적용 (1회 실행)", 9, OK, KR, "start")

# 4. 불변 버전 (vN) 노드
d.box(240, 418, 230, 64, PAPER2, OK, 1.1)
d.t(355, 442, "불변 버전 (v1, v2, ...)", 12, OK, KR, "middle", 600)
d.t(355, 462, "스냅샷 보관 · 미배포 상태", 10, MUTED, KR, "middle")

# 오른쪽으로: 배포 요청 및 승인 (2 -> 3, 간격 50px 통로, 중앙선 x=505 로 꺾임선 및 라벨 여백 확보)
d.arrow([(470, 450), (505, 450), (505, 210), (540, 210)], ACC, "acc", 1.4)
d.t(505, 440, "deploy", 8.5, ACC, MONO, "middle")

# 5. 배포 승인 노드 (x: 540, w: 186)
d.tone(540, 170, 186, 80, ACC, 6, "14", 1.2)
d.t(633, 196, "배포 승인 (deploy)", 12, ACC, KR, "middle", 600)
d.t(633, 216, "콘솔 deploy 승인 확인", 10, INK, KR, "middle")
d.t(633, 234, "데이터 스냅샷 생성 (server)", 9, MUTED, KR, "middle")

# 아래로: 라이브 활성화 (화살표 좌측 오프셋으로 라벨 관통 방지)
d.arrow([(562, 250), (562, 292)], OK, "ok", 1.4)
d.t(574, 273, "활성화 전환", 9, OK, KR, "start")

# 6. 로컬 라이브 서비스 노드 (x: 540, w: 186)
d.tone(540, 294, 186, 90, OK, 6, "12", 1.2)
d.t(633, 320, "로컬 Live 서비스", 12, OK, KR, "middle", 600)
d.t(633, 342, "127.0.0.1:7879", 11, INK, MONO, "middle")
d.t(633, 362, "<slug>.localhost:7879", 10, MUTED, MONO, "middle")

# 오른쪽으로: 공개 승인 및 네트워크 제공자 연결 (3 -> 4, 간격 90px 확보, set_visibility 라벨 양옆 10px 마진)
d.arrow([(726, 339), (836, 339)], ACC, "acc", 1.4)
d.t(781, 327, "set_visibility", 8.5, ACC, MONO, "middle")

# 7. 외부 공개 엔드포인트 노드 (x: 836, w: 146)
d.tone(836, 294, 146, 100, ACC, 6, "16", 1.4)
d.t(909, 320, "외부 공개 서비스", 12, ACC, KR, "middle", 600)
d.t(909, 342, "공개 URL 접속", 10, INK, KR, "middle")
d.t(909, 360, "<slug>.<relay 도메인>", 9, ACC, MONO, "middle")
d.t(909, 378, "/mcp·/api 접근 차단", 9, WARN, MONO, "middle")

# 범례
d.legend(515, [
    ("초안 및 비공개 작업본", INFO),
    ("승인 대기 및 통제 지점", WARN),
    ("승인 완료 및 불변 버전", OK),
    ("라이브 및 외부 공개", ACC)
])

out_path = Path(__file__).parent.parent / "00-01-agent-to-public.svg"
d.save(str(out_path))
print(f"Saved: {out_path}")
