# 18-03 §3 — 네이티브 사이드카가 있는 Job 의 완료 순서
#
# 재생성: cd <이 파일이 있는 디렉토리> && vhs 18-03-sidecar-completion.tape
#
# 전제 1. KUBECONFIG 는 kind 전용 사본을 물린다. 전역 kubeconfig 에는
# 회사 운영 클러스터가 함께 등록돼 있어 그대로 쓰면 오발사 위험이 있다.
# 아래 경로가 없으면 다음으로 다시 만든다:
#   kubectl config view --minify --flatten --context=kind-k8s-lab > /tmp/18-03-sidecar.kubeconfig
#
# 전제 2. /tmp/sidecar-timing.yaml 은 §3.2 매니페스트에서 대기 시간만 줄인 것이다
# (메인 sleep 20 → 10, terminationGracePeriodSeconds 5 추가). 녹화 길이를 줄이기
# 위한 것이고 완료 순서 자체는 같다.

Output "18-03-sidecar-completion.gif"

Require kubectl

Set Shell "bash"
Set Width 1200
Set Height 480
Set FontSize 19
Set FontFamily "JetBrains Mono"
Set Theme "GitHub Dark"
Set Padding 26
Set Framerate 24
Set TypingSpeed 18ms
Set CursorBlink false

Hide
Type "export KUBECONFIG=/tmp/18-03-sidecar.kubeconfig"
Enter
Type "kubectl config set-context --current --namespace=ch18-lab"
Enter
Type "kubectl delete job sidecar-timing --ignore-not-found"
Enter
Type "cd /tmp"
Enter
Type "export PS1='$ '"
Enter
Type "clear"
Enter
Show

Sleep 1s

Type "kubectl apply -f sidecar-timing.yaml"
Sleep 400ms
Enter
Wait+Screen /created/
Sleep 1s

Type "kubectl get pod -w"
Sleep 400ms
Enter
Sleep 27s
Ctrl+C
Sleep 500ms
Enter
Sleep 500ms

Type "kubectl get job"
Sleep 400ms
Enter
Wait+Screen /COMPLETIONS/
Sleep 6s
