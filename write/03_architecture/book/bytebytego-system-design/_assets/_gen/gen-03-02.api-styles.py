# 타입 스펙: type-dp-security-matrix — 사용자 7 한 명을 조회하는 같은 일을 SOAP·REST·GraphQL·gRPC 네 행 × 요청 줄·요청 본문·응답 본문 세 열로 비교하는 격자(격자 문법을 비교 행렬로 사용). 초점 칸은 GraphQL 이 요청한 필드만 돌려주는 응답.
# 사실 출처: SOAP — W3C SOAP 1.2 Part 1 (https://www.w3.org/TR/soap12-part1/) 의 Envelope 네임스페이스 http://www.w3.org/2003/05/soap-envelope, 미디어 타입 application/soap+xml 은 같은 문서 §A 의 SHOULD.
#   REST — GET /users/7 은 HTTP 의 자원 URL + 메서드(Fielding 2000, §5.1.5 Uniform Interface). GraphQL — GraphQL over HTTP 초안(https://graphql.github.io/graphql-over-http/draft/) §4.4 POST 요청 본문 `{"query": ...}` 과 Content-Type application/json.
#   gRPC — grpc/grpc doc/PROTOCOL-HTTP2.md: 메서드는 `:method POST`, 경로는 `/서비스명/메서드명`, 본문은 길이 접두 메시지(압축 플래그 1바이트 + 길이 4바이트 + 메시지). 필드 번호 1 정수 7 → 바이트 08 07, 필드 2 문자열 Kim → 12 03 4b 69 6d (protobuf 인코딩 문서의 태그 = (필드 번호 << 3) | 와이어 타입).
#   사용자 7·이름 Kim·서비스명 users.UserService·GetUser 는 이 노트가 만든 예시 값. 추출본 v1.txt 1560~1580행(스타일 네 가지).
# Layout conventions: §2 공식 — left_pad 12, 행 라벨 열 폭 140, 데이터 열 폭 252·196·264 (간격 8), header_h 44(header_y 96), row_h 56 · stride 64. 모든 좌표 4의 배수.
import sys; sys.path.insert(0, ".")
from dd import D, ACC, OK, WARN, INFO, MUTED, INK, PAPER, PAPER2, RULE, SOFT, KR, MONO

LEFT, LAB_W, GAP = 12, 140, 8
COLS = [252, 196, 264]
HDR_Y, HDR_H, ROW0, ROW_H, STRIDE = 96, 44, 156, 56, 64
heads = ["요청 줄", "요청 본문", "응답 본문"]
rows = [
    ("SOAP", "연산 이름", ["POST /UserService", "<m:GetUser> id=7", "<m:GetUserResponse>"]),
    ("REST", "URL + 메서드", ["GET /users/7", "(본문 없음)", '{"id":7,"name":"Kim"}']),
    ("GraphQL", "필드 선택", ["POST /graphql", "{ user(id:7){ name } }", '{"data":{"user":{"name":"Kim"}}}']),
    ("gRPC", "메서드 호출", ["POST /users.UserService/GetUser", "00 00000002 0807", "00 00000007 0807 12034b696d"]),
]
FOCAL = (2, 2)

W = LEFT + LAB_W + GAP + sum(COLS) + GAP * 2 + 12
H = ROW0 + 3 * STRIDE + ROW_H + 20 + 44
d = D(W, H, "BYTEBYTEGO · 03-02 §1",
      "같은 사용자 조회가 네 스타일에서 갖는 모양",
      "사용자 7 한 명을 가져오는 일은 같지만 요청이 가리키는 대상과 본문이 달라집니다",
      "SOAP 1.2 · REST · GraphQL over HTTP · gRPC")


def cx(j):
    return LEFT + LAB_W + GAP + sum(COLS[:j]) + GAP * j


d.box(LEFT, HDR_Y, LAB_W, HDR_H, PAPER2, RULE, 0.9, 6)
d.t(LEFT + LAB_W / 2, HDR_Y + 27, "스타일", 12, INK, KR, "middle", 600)
for j, nm in enumerate(heads):
    d.box(cx(j), HDR_Y, COLS[j], HDR_H, PAPER2, "rgba(191,192,192,0.45)", 0.9, 6)
    d.t(cx(j) + COLS[j] / 2, HDR_Y + 27, nm, 12, INK, KR, "middle", 600)

for i, (name, hint, cells) in enumerate(rows):
    y = ROW0 + i * STRIDE
    d.box(LEFT, y, LAB_W, ROW_H, PAPER2, RULE, 0.8, 4)
    d.t(LEFT + 12, y + 24, name, 12, INK, MONO, "start", 600)
    d.t(LEFT + 12, y + 44, hint, 12, MUTED, KR, "start")
    for j, txt in enumerate(cells):
        x = cx(j)
        if (i, j) == FOCAL:
            d.tone(x, y, COLS[j], ROW_H, ACC, 4, "14", 1.4)
            d.t(x + COLS[j] / 2, y + 34, txt, 12, ACC, MONO, "middle", 600)
        else:
            d.tone(x, y, COLS[j], ROW_H, INFO, 4, "0c", 0.8)
            d.t(x + COLS[j] / 2, y + 34, txt, 12, INK, MONO, "middle")

d.legend(H - 44, [("스타일별 모양", INFO), ("요청한 필드만 응답", ACC)])
d.save("03-02.api-styles.svg")
