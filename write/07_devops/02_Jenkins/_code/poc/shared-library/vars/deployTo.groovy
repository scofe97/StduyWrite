// =============================================================================
// Shared Library: deployTo
//
// 지정된 환경(dev/staging/prod)에 Docker 이미지를 배포하는 공통 함수이다.
// 환경에 따라 배포 전략이 달라진다는 점이 핵심 학습 포인트이다.
//
// 사용 예시:
//   deployTo(
//       environment: 'staging',
//       imageName:   'localhost:5000/my-app',
//       tag:         env.BUILD_NUMBER,
//       port:        '8081'
//   )
// =============================================================================

def call(Map config) {
    // 파라미터 기본값 설정
    def environment = config.environment ?: error('environment는 필수 파라미터이다')
    def imageName   = config.imageName   ?: error('imageName은 필수 파라미터이다')
    def tag         = config.tag         ?: 'latest'
    def port        = config.port        ?: '8081'

    echo "=== 배포 시작: ${environment} ==="
    echo "이미지: ${imageName}:${tag}"

    // 환경별 배포 전략 분기
    switch (environment) {
        case 'dev':
            deployWithDocker(imageName, tag, port)
            break
        case 'staging':
            deployWithDocker(imageName, tag, port)
            break
        case 'prod':
            deployWithKubernetes(imageName, tag)
            break
        default:
            error "알 수 없는 환경: ${environment}"
    }

    echo "=== 배포 완료: ${environment} ==="
}

// -----------------------------------------------------------------------------
// Docker 기반 배포 (dev, staging)
// -----------------------------------------------------------------------------
private def deployWithDocker(String imageName, String tag, String port) {
    def containerName = imageName.split('/').last()

    // TODO: 기존 컨테이너를 정리하고 새 컨테이너를 실행하라
    // 힌트:
    //   1. 기존 컨테이너 중지 및 삭제 (없어도 에러가 나지 않게)
    //   2. 새 컨테이너를 detached 모드로 실행
    //
    // sh """
    //     docker stop ${containerName} || true
    //     docker rm ${containerName} || true
    //     docker run -d \
    //         --name ${containerName} \
    //         -p ${port}:${port} \
    //         ${imageName}:${tag}
    // """
    echo "TODO: Docker 기반 배포 구현 (docker run)"

    // TODO: 배포 후 헬스체크를 수행하라
    // 힌트: 일정 시간 대기 후 /health 엔드포인트 호출
    // 질문: 헬스체크 실패 시 롤백은 어떻게 구현해야 하는가?
    //
    // sh """
    //     sleep 5
    //     curl -f http://localhost:${port}/health || exit 1
    // """
    echo "TODO: 배포 후 헬스체크 구현"
}

// -----------------------------------------------------------------------------
// Kubernetes 기반 배포 (prod)
// -----------------------------------------------------------------------------
private def deployWithKubernetes(String imageName, String tag) {
    // TODO: kubectl을 사용하여 Kubernetes에 배포하라
    // 힌트:
    //   1. kubectl set image로 이미지 업데이트
    //   2. kubectl rollout status로 배포 완료 대기
    //
    // sh """
    //     kubectl set image deployment/${containerName} \
    //         ${containerName}=${imageName}:${tag} \
    //         --namespace=production
    //     kubectl rollout status deployment/${containerName} \
    //         --namespace=production \
    //         --timeout=300s
    // """
    echo "TODO: Kubernetes 기반 배포 구현 (kubectl)"

    // TODO: 배포 실패 시 롤백 로직을 구현하라
    // 질문: kubectl rollout undo와 수동 롤백의 차이는?
    echo "TODO: 배포 실패 시 롤백 로직 구현"
}
