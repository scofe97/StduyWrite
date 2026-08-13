Output "18-01-job-suspend.gif"

Require kubectl

Set Shell "bash"
Set Width 1200
Set Height 420
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export KUBECONFIG=/tmp/18-job.kubeconfig"
Enter
Type "kubectl config set-context --current --namespace=job-lab"
Enter
Type "kubectl delete job demo-suspend --ignore-not-found"
Enter
Type "cd /tmp && cp job-suspend.yaml job.demo-suspend.yaml"
Enter
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Type "kubectl apply -f job.demo-suspend.yaml"
Sleep 400ms
Enter
Wait+Screen /created/
Sleep 1s

Type "kubectl get po -l job-name=demo-suspend"
Sleep 400ms
Enter
Wait+Screen /No resources found/
Sleep 3s

Type "kubectl patch job demo-suspend --patch-file /tmp/resume.json"
Sleep 400ms
Enter
Sleep 3s

Type "kubectl get po -l job-name=demo-suspend"
Sleep 400ms
Enter
Wait+Screen /demo-suspend-/
Sleep 6s
