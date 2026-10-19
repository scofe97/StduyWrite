# 타입 스펙: type-sequence
# 사실 출처: encoding/gob, Rob Pike "Gobs of Data", NPG Ch.12 Listing 12-13~12-15
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from dd import Seq, MUTED, SOFT, ACC, OK, WARN, INFO, MONO, KR

W, H = 960, 580
s = Seq(W, H, "SEQUENCE · GOB SELF-DESCRIBING STREAM",
        "Gob 파일이 형식 명세 두 메시지 뒤에 값 메시지를 싣는 순서",
        "gob.Encoder 는 []*Chore 와 Chore 의 형식 명세를 먼저 보내고 값 메시지를 보내며, 메시지마다 앞의 1바이트가 길이입니다.",
        lead="1 + 13 + 1 + 40 + 1 + 49 = 105 B. 한 Encoder 는 이미 보낸 형식을 다시 보내지 않습니다.")

s.lanes([("gob.Encoder", "Encode(chores)"),
         ("Gob 바이트", "housework.db"),
         ("gob.Decoder", "Decode(&chores)")], y0=104, lane_w=176)

def selfmsg_left(s, a, label, y, c=MUTED, sub=None):
    x = s.LX[a]
    s.path(f"M {x-10} {y-10} L {x-58} {y-10} L {x-58} {y+10} L {x-13} {y+10}", c, 1.4, m="ar")
    s.t(x - 68, y - 4, label, 11, c, MONO, "end")
    if sub:
        s.t(x - 68, y + 13, sub, 11, MUTED, KR, "end")

# 1. 인코더가 형식 명세를 만든다
s.selfmsg("gob.Encoder", "형식 명세 만들기", 176, INFO,
          sub="[]*Chore · Chore 의 공개 필드")

# 2~4. 스트림에 실리는 세 메시지
s.msg("gob.Encoder", "Gob 바이트", "메시지 1 · 0d (13 B)", 232, OK, "ok",
      sub="[]*Chore 슬라이스 형식")
s.msg("gob.Encoder", "Gob 바이트", "메시지 2 · 28 (40 B)", 288, OK, "ok",
      sub="Chore 형식 · Complete · Description 이름")
s.msg("gob.Encoder", "Gob 바이트", "메시지 3 · 31 (49 B)", 344, OK, "ok",
      sub="값 · Mop floors · Clean dishes · Mow the lawn")

# 5~6. 디코더가 명세 먼저, 값 나중에 읽는다
s.msg("Gob 바이트", "gob.Decoder", "명세 2개 읽기", 400, ACC, "acc",
      sub="필드 이름으로 받을 변수와 맞춤")
s.msg("Gob 바이트", "gob.Decoder", "값 읽기", 456, ACC, "acc",
      sub="명세대로 필드 값 해석")

# 7. 복원
selfmsg_left(s, "gob.Decoder", "[]*Chore 3건", 508, ACC,
             sub="이름 없이 값만 읽어 복원")

s.rails(520)
s.legend(538, [("인코더", INFO), ("스트림에 실린 메시지", OK), ("디코더", ACC)])

svg_path = pathlib.Path(__file__).resolve().parent.parent / "12-01.gob-stream-layout.svg"
s.save(str(svg_path))
print("ok 12-01 gob-stream-layout")
