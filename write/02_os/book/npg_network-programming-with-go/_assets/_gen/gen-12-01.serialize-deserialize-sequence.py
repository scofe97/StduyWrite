# 타입 스펙: type-sequence
# 사실 출처: NPG Ch.12 도입 ~ Serializing Objects, net.Conn.Write, RFC 8259
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, MUTED, SOFT, ACC, OK, WARN, INFO, MONO, KR

W, H = 940, 560
s = Seq(W, H, "SEQUENCE · SERIALIZATION LIFECYCLE",
        "구조체를 바이트로 바꿔 보내고 받는 쪽이 복제본을 만드는 순서",
        "구조체는 연결에 그대로 실을 수 없어 []byte 로 인코딩해 쓰고, 받는 쪽은 같은 형식으로 디코딩해 복제본을 만듭니다.",
        lead="net.Conn.Write 는 []byte 만 받으므로 양쪽이 같은 직렬화 형식을 알아야 합니다.")

s.lanes([("송신 프로세스", "Chore{…}"),
         ("전송·저장 매체", "net.Conn · housework.db"),
         ("수신 프로세스", "Chore{…}")], y0=104, lane_w=170)

def selfmsg_left(s, a, label, y, c=MUTED, sub=None):
    x = s.LX[a]
    s.path(f"M {x-10} {y-10} L {x-58} {y-10} L {x-58} {y+10} L {x-13} {y+10}", c, 1.4, m="ar")
    s.t(x - 68, y - 4, label, 11, c, MONO, "end")
    if sub:
        s.t(x - 68, y + 13, sub, 11, MUTED, KR, "end")

# 1. 원본 메모리 상태
s.selfmsg("송신 프로세스", "원본 구조체", 176, INFO,
          sub='Chore{Complete:false, Description:"Mop floors"}')

# 2. 직렬화 인코딩
s.selfmsg("송신 프로세스", "Encode · Marshal", 232, OK,
          sub="형식 규칙대로 []byte 로")

# 3. 매체로 전송 / 기록
s.msg("송신 프로세스", "전송·저장 매체", "Write([]byte)", 288, OK, "ok",
      sub="net.Conn 또는 housework.db 에 쓰기")

# 4. 매체에서 수신 / 읽기
s.msg("전송·저장 매체", "수신 프로세스", "Read([]byte)", 348, OK, "ok",
      sub="net.Conn 또는 housework.db 에서 읽기")

# 5. 역직렬화 디코딩 (수신 프로세스 내부 동작 - 안쪽으로 표시)
selfmsg_left(s, "수신 프로세스", "Decode · Unmarshal", 408, ACC,
             sub="같은 형식으로 필드 값 읽기")

# 6. 복원된 메모리 상태
selfmsg_left(s, "수신 프로세스", "복제본", 464, ACC,
             sub='Chore{Complete:false, Description:"Mop floors"}')

s.rails(490)
s.legend(510, [("보내는 쪽 메모리", INFO), ("바이트 쓰기·읽기", OK), ("받는 쪽 복원", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-01.serialize-deserialize-sequence.svg"
s.save(str(svg_path))
print("ok 12-01 serialize-deserialize-sequence")
