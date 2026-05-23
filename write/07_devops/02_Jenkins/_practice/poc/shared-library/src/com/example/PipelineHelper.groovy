package com.example

// =============================================================================
// PipelineHelper: 파이프라인 유틸리티 클래스
//
// Shared Library의 src/ 디렉토리에 위치하는 헬퍼 클래스이다.
// vars/와 달리 이곳의 클래스는 명시적으로 import하여 사용한다.
//
// 사용 예시 (Jenkinsfile 또는 vars/*.groovy에서):
//   @Library('my-shared-lib') _
//   import com.example.PipelineHelper
//
//   def helper = new PipelineHelper(this)
//   helper.validateConfig(config)
// =============================================================================

class PipelineHelper implements Serializable {

    // Jenkins Pipeline 컨텍스트 (steps 객체)
    // Serializable이 필요한 이유: Jenkins는 파이프라인 상태를 디스크에 저장(직렬화)할 수 있어야 한다
    private def steps

    PipelineHelper(steps) {
        this.steps = steps
    }

    // -------------------------------------------------------------------------
    // validateConfig: 파이프라인 설정을 검증한다
    //
    // 파이프라인 시작 전에 필수 설정이 모두 존재하는지 확인한다.
    // 설정 누락으로 중간에 실패하는 것보다, 시작 전에 빠르게 실패하는 것이 낫다 (Fail Fast).
    // -------------------------------------------------------------------------
    def validateConfig(Map config) {
        steps.echo "=== 설정 검증 시작 ==="

        // TODO: 필수 파라미터가 존재하는지 검증하라
        // 힌트: 필수 키 목록을 정의하고, config에 해당 키가 있는지 확인한다
        // 질문: 검증 실패 시 어떤 정보를 에러 메시지에 포함해야 디버깅이 쉬운가?
        //
        // def requiredKeys = ['appName', 'imageName', 'registry']
        // def missingKeys = requiredKeys.findAll { !config.containsKey(it) || !config[it] }
        //
        // if (missingKeys) {
        //     steps.error "필수 설정 누락: ${missingKeys.join(', ')}"
        // }
        steps.echo "TODO: 필수 파라미터 검증 로직 구현"

        // TODO: 설정 값의 형식을 검증하라
        // 예시: imageName에 허용되지 않는 문자가 포함되어 있는지 확인
        // 힌트: 정규식을 사용하여 패턴 매칭
        //
        // if (config.imageName && !(config.imageName ==~ /^[a-z0-9\-\/\.:]+$/)) {
        //     steps.error "imageName 형식이 잘못됨: ${config.imageName}"
        // }
        steps.echo "TODO: 설정 값 형식 검증 구현"

        steps.echo "=== 설정 검증 완료 ==="
        return true
    }

    // -------------------------------------------------------------------------
    // getDeploymentTarget: 브랜치 이름으로 배포 대상 환경을 결정한다
    //
    // Git 브랜치 전략과 배포 환경을 매핑한다.
    // 이 매핑 규칙은 조직의 Git 워크플로우에 따라 달라질 수 있다.
    // -------------------------------------------------------------------------
    def getDeploymentTarget(String branchName) {
        steps.echo "=== 배포 대상 결정: 브랜치=${branchName} ==="

        // TODO: 브랜치 이름에 따라 배포 환경을 반환하라
        // 힌트: main/master → prod, develop → staging, feature/* → dev
        // 질문: release/* 브랜치는 어디에 배포해야 하는가?
        //
        // switch (branchName) {
        //     case 'main':
        //     case 'master':
        //         return 'prod'
        //     case 'develop':
        //         return 'staging'
        //     case ~/^feature\/.*/:
        //         return 'dev'
        //     case ~/^release\/.*/:
        //         return 'staging'
        //     case ~/^hotfix\/.*/:
        //         return 'staging'
        //     default:
        //         steps.echo "경고: 알 수 없는 브랜치 패턴 '${branchName}', dev 환경으로 배포"
        //         return 'dev'
        // }
        steps.echo "TODO: 브랜치 → 환경 매핑 로직 구현"
        return 'dev'  // 기본값: 구현 전까지 dev로 반환
    }

    // -------------------------------------------------------------------------
    // notifyBuildResult: 빌드 결과를 알림으로 보낸다
    //
    // Slack, 이메일 등 다양한 채널로 빌드 결과를 전송한다.
    // -------------------------------------------------------------------------
    def notifyBuildResult(Map params) {
        def status  = params.status  ?: 'UNKNOWN'
        def channel = params.channel ?: '#ci-cd'

        steps.echo "=== 빌드 알림: ${status} ==="

        // TODO: 빌드 결과를 Slack으로 전송하라
        // 힌트: slackSend 플러그인 사용
        // 질문: 알림에 어떤 정보를 포함해야 개발자가 빠르게 대응할 수 있는가?
        //
        // def color = status == 'SUCCESS' ? 'good' : 'danger'
        // def message = """
        //     *${status}*: ${steps.env.JOB_NAME} #${steps.env.BUILD_NUMBER}
        //     Branch: ${steps.env.BRANCH_NAME}
        //     Duration: ${steps.currentBuild.durationString}
        //     <${steps.env.BUILD_URL}|빌드 로그 보기>
        // """.stripIndent()
        //
        // steps.slackSend(channel: channel, color: color, message: message)
        steps.echo "TODO: Slack 알림 전송 구현"
    }
}
