# 타입 스펙: type-dp-security-matrix — 저장소 세 종류(행) × 접근 성질 네 개(열)의 가능·불가 격자(격자 문법을 비교 행렬로 사용). 초점 칸 하나는 객체 저장소의 제자리 수정 불가.
# 사실 출처: 추출본 v1.txt 2311~2384행(블록=원시 블록 볼륨·서버 하나가 소유, 파일=계층 디렉터리·NFS/SMB 공유, 객체=평평한 구조·RESTful API)
#   · AWS S3 사용자 가이드 "Amazon S3 data consistency model"·"Retaining multiple versions of objects with S3 Versioning"(덮어쓰기는 새 버전)·"Appending data to objects in directory buckets"(Express One Zone 만 append)
#   · AWS EBS 사용자 가이드 "Multi-Attach"(같은 AZ 의 io1·io2, 표준 파일 시스템은 동시 접근용이 아님) · S3 사용자 가이드 "Directory buckets overview"(디렉터리 버킷은 계층 디렉터리, 범용 버킷은 평평) · RFC 7143(iSCSI) · RFC 8881(NFS 4.1).
# Layout conventions: §2 공식 — left_pad 12, comp_col_w 208, role_col_w 148, role_col_gap 16, header_h 52, header_y 96, row_h 44 · stride 48. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LEFT, COMP_W, GAP0, ROLE_W, ROLE_GAP, HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 12, 208, 12, 148, 16, 96, 52, 164, 44, 48
roles = [("제자리 부분 수정", "일부만 덮어쓰기"), ("여러 서버가 함께", "동시에 접근"), ("디렉터리 계층", "경로 트리"), ("접근 경로", "프로토콜")]
rows = [
    ("블록 저장소", "LBA 단위"),
    ("파일 저장소", "경로 + 오프셋"),
    ("객체 저장소", "키 하나 = 객체 하나"),
]
# kind: ok 가능 · warn 불가·제한 · info 사실 나열
cells = [
    [("ok", "가능", "블록 덮어쓰기"), ("warn", "제한", "대개 서버 하나"), ("warn", "없음", "원시 블록"), ("info", "iSCSI · FC", "")],
    [("ok", "가능", "파일 일부 쓰기"), ("ok", "가능", "NFS · SMB"), ("ok", "있음", "경로 트리"), ("info", "NFS · SMB", "")],
    [("warn", "불가", "통째 교체 · 버전"), ("ok", "가능", "HTTP 요청"), ("warn", "없음", "범용 버킷 기준"), ("info", "REST API", "")],
]
FOCAL = (2, 0)
COLOR = {"ok": OK, "warn": WARN, "info": INFO}

W = LEFT + COMP_W + GAP0 + 4 * ROLE_W + 3 * ROLE_GAP + 48
H = ROW0 + 2 * STRIDE + ROW_H + 20 + 44
d = D(W, H, "BYTEBYTEGO · 04-01 §2",
      "블록 · 파일 · 객체 저장소의 접근 성질",
      "객체 저장소는 제자리 수정이 없고 범용 버킷은 디렉터리 대신 평평한 키 공간을 씁니다",
      "접근 단위가 다르면 되는 일이 갈립니다")

d.box(LEFT, HDR_Y, COMP_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LEFT + COMP_W / 2, HDR_Y + 22, "저장소", 12, INK, KR, "middle", 600)
d.t(LEFT + COMP_W / 2, HDR_Y + 40, "× 접근 성질", 12, MUTED, KR)


def rx(j):
    return LEFT + COMP_W + GAP0 + j * (ROLE_W + ROLE_GAP)


for j, (nm, sub) in enumerate(roles):
    d.box(rx(j), HDR_Y, ROLE_W, HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 22, nm, 12, INK, KR, "middle", 600)
    d.t(rx(j) + ROLE_W / 2, HDR_Y + 40, sub, 12, MUTED, KR)

for i, (name, hint) in enumerate(rows):
    y = ROW0 + i * STRIDE
    d.box(LEFT, y, COMP_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT + 12, y + 18, name, 12, INK, KR, "start", 600)
    d.t(LEFT + 12, y + 35, hint, 12, MUTED, KR, "start")
    for j in range(4):
        kind, label, sub = cells[i][j]
        x = rx(j)
        c = COLOR[kind]
        if (i, j) == FOCAL:
            d.tone(x, y, ROLE_W, ROW_H, ACC, 4, "14", 1.4)
            d.t(x + ROLE_W / 2, y + 19, label, 12, ACC, KR, "middle", 600)
            d.t(x + ROLE_W / 2, y + 36, sub, 12, ACC, KR)
        else:
            d.tone(x, y, ROLE_W, ROW_H, c, 4, "10", 0.9)
            fam = KR if any("가" <= ch <= "힣" for ch in label) else MONO
            if sub:
                d.t(x + ROLE_W / 2, y + 19, label, 12, c, fam, "middle", 600)
                d.t(x + ROLE_W / 2, y + 36, sub, 12, MUTED, KR)
            else:
                d.t(x + ROLE_W / 2, y + 27, label, 12, c, fam, "middle", 600)

d.legend(H - 44, [("가능", OK), ("불가 · 제한 · 없음", WARN), ("접근 경로", INFO), ("이 편의 초점", ACC)])
d.save("04-01.storage-access-matrix.svg")
