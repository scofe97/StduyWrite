Output "01-02.tcpdump-12packets.gif"

Require tcpdump
Require curl

# 사용자가 직접 굽는 테이프다. 라이브 캡처는 /dev/bpf 가 root 전용이라 sudo 가 필요하고,
# macOS sudo 는 tty 단위로 자격을 캐시하므로 굽는 터미널에서 직접 `sudo -v` 를 해야 한다.
#
# 굽기 전에 두 가지를 먼저 한다.
#   1. sudo -v                  # 녹화 중 암호 프롬프트가 뜨지 않게 자격을 캐시한다
#   2. go run main.go &         # 01-01 §5 의 Go 웹 서버를 8080 으로 띄운다
#
# 그다음: vhs 01-02.tcpdump-12packets.tape
#
# 캡처는 파일로 받고 화면 표시는 `-r` 로 다시 읽는다. 터미널 하나로 끝내려는 것도 있지만,
# 파일 읽기는 root 가 필요 없어 출력 부분이 권한과 무관해지는 이점이 크다.
# 표시에 `-vvv` 를 붙이는 것이 이 장면의 핵심이다 — 플래그 순서와 함께
# 괄호로 묶인 IP 헤더 필드(tos·ttl·id·offset·flags·proto·length)가 어디에 찍히는지 보인다.

Set Shell "bash"
Set Width 1600
Set Height 720
Set FontSize 18
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export PS1='$ '"
Enter
Type "rm -f /tmp/p12.pcap"
Enter
Type "clear"
Enter
Show

Type "sudo tcpdump -i lo0 -n tcp port 8080 -w /tmp/p12.pcap &"
Sleep 400ms
Enter
Sleep 3s

Type "curl -s localhost:8080"
Sleep 400ms
Enter
Sleep 2s

Type "sudo pkill tcpdump"
Sleep 400ms
Enter
Sleep 2s

# 1차 결과 — 몇 개가 잡혔나
Type "tcpdump -r /tmp/p12.pcap -n | wc -l"
Sleep 400ms
Enter
Wait+Screen /12/
Sleep 3s

# 2차 — 플래그 순서와 IP 헤더 필드를 함께 본다
Type "clear"
Enter
Type "tcpdump -r /tmp/p12.pcap -n -vvv | head -20"
Sleep 400ms
Enter
Sleep 8s
