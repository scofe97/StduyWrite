Output "03-03.ping-rtt-samples.gif"

Require ping

Set Shell "bash"
Set Width 1440
Set Height 880
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false
Set WaitTimeout 45s

Hide
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "ping -c 30 -i 0.5 gaia.cs.umass.edu | grep --line-buffered -oE 'time=[0-9.]+' | cut -d= -f 2"
Sleep 600ms
Enter
Wait+Line /^\$ ?$/
Sleep 6s
