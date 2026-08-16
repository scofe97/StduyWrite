Output "02-01.veth-pair-lab.gif"

Require docker

# macOS 에서는 netns·veth 가 네이티브로 없다. Docker Desktop 이 띄운 리눅스 커널을
# 빌려 쓰는 것이며 --privileged 로 네트워크 장치를 만들 권한을 준다.
# 임시 컨테이너라 --rm 으로 빠져나오면 만든 장치도 함께 사라진다.

Set Shell "bash"
Set Width 1440
Set Height 520
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
Type "clear"
Enter
Show

Type "docker run --rm -it --privileged nicolaka/netshoot"
Sleep 400ms
Enter
Sleep 4s

Hide
Type "clear"
Enter
Show

Type "ip link add br0 type bridge"
Sleep 300ms
Enter
Sleep 500ms

Type "ip link add veth1 type veth peer name veth2"
Sleep 300ms
Enter
Sleep 500ms

Type "ip link set veth2 master br0"
Sleep 300ms
Enter
Sleep 800ms

Type "ip -br link show type veth"
Sleep 300ms
Enter
Sleep 2s

Type "bridge link"
Sleep 300ms
Enter
Wait+Screen /master br0/
Sleep 6s
