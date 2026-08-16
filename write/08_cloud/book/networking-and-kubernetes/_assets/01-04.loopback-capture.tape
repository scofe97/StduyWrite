Output "01-04.loopback-capture.gif"

Require tcpdump
Require curl

# 사용자가 직접 굽는 테이프다. 라이브 캡처는 /dev/bpf 가 root 전용이라 sudo 가 필요하다.
#
# 굽기 전에 두 가지를 먼저 한다.
#   1. sudo -v            # 자격 증명을 캐시해 녹화 중 암호 프롬프트가 뜨지 않게 한다
#   2. go run web-server.go &   # 01-01 의 Go 웹 서버를 8080 으로 띄운다
#
# 캡처 대상은 lo0 뿐이라 남의 트래픽이 섞이지 않는다.

Set Shell "bash"
Set Width 1440
Set Height 420
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export PS1='$ '"
Enter
Type "rm -f /tmp/loop.pcap"
Enter
Type "clear"
Enter
Show

Type "sudo tcpdump -i lo0 -n port 8080 -w /tmp/loop.pcap &"
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

Type "tcpdump -r /tmp/loop.pcap -n | wc -l"
Sleep 400ms
Enter
Wait+Screen /12/
Sleep 6s
