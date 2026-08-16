Output "01-04.udp-dns.gif"

Require dig

Set Shell "bash"
Set Width 1440
Set Height 400
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

Type "dig @8.8.8.8 example.com +noall +answer +stats"
Sleep 400ms
Enter
Wait+Screen /MSG SIZE/
Sleep 6s
