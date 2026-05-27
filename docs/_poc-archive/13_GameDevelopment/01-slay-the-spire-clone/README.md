# Slay the Spire 클론코딩 학습

Java는 학습했으나 게임 개발은 처음인 상태에서, STS(Slay the Spire) 클론코딩을 통해 게임 아키텍처와 libGDX를 학습합니다. 원작 에셋을 추출하여 로컬 학습용으로만 사용하며, libGDX를 STS에 필요한 범위만 집중 학습합니다.

---

## 학습 목표

1. libGDX의 핵심 기능(렌더링, Scene2D, 입력, 에셋)을 이해하고 사용할 수 있다
2. STS의 핵심 아키텍처(Action Queue, 카드 시스템, 전투 루프)를 구현할 수 있다
3. 데이터 드리븐 설계로 카드/몬스터를 JSON으로 관리할 수 있다
4. DAG 기반 맵 생성과 런 구조를 구현할 수 있다

---

## 기술 스택

| 기술 | 버전 | 용도 |
|------|------|------|
| Java | 17 | 메인 언어 |
| libGDX | 1.12+ | 게임 프레임워크 |
| gdx-liftoff | latest | 프로젝트 생성 도구 |
| Gradle (Kotlin DSL) | 8.x | 빌드 도구 |
| IntelliJ IDEA | latest | IDE |

---

## 학습 리소스

| 리소스 | 용도 | 비용 |
|--------|------|------|
| [libGDX Wiki](https://libgdx.com/wiki/) | 메인 참조 | 무료 |
| [gdx-liftoff](https://github.com/libgdx/gdx-liftoff) | 프로젝트 생성 | 무료 |
| [Scene2D Wiki](https://libgdx.com/wiki/graphics/2d/scene2d/scene2d) | UI 시스템 | 무료 |
| [STS Modding Wiki](https://github.com/Gremious/StS-DefaultModBase/wiki) | 원작 아키텍처 참고 | 무료 |
| Slay the Spire (Steam) | 에셋 추출 원본 | 유료 (소유) |

---

## 커리큘럼

### Part 1: libGDX 기초 (Ch01~08)

libGDX를 STS 클론에 필요한 범위만 학습. 물리엔진, 3D, 타일맵 등은 제외.

| 순서 | 파일 | 주제 | 핵심 개념 |
|------|------|------|----------|
| 01 | [01-libgdx-lifecycle](./learning/01-libgdx-lifecycle/LEARN.md) | libGDX 생명주기 & 프로젝트 구조 | Game, Screen, ApplicationListener |
| 02 | [02-rendering-basics](./learning/02-rendering-basics/LEARN.md) | 렌더링 기초 | SpriteBatch, Texture, Camera, Viewport |
| 03 | [03-scene2d-core](./learning/03-scene2d-core/LEARN.md) | Scene2D 핵심 | Stage, Actor, Group, Table, Actions |
| 04 | [04-input-drag-drop](./learning/04-input-drag-drop/LEARN.md) | 입력 & DragAndDrop | InputProcessor, DragAndDrop |
| 05 | [05-asset-management](./learning/05-asset-management/LEARN.md) | 에셋 관리 & 한글 폰트 | AssetManager, TextureAtlas, FreeType |
| 06 | [06-screen-gamestate](./learning/06-screen-gamestate/LEARN.md) | Screen 전환 & 상태 관리 | Game.setScreen(), 전역 상태 |
| 07 | [07-ui-widgets-skin](./learning/07-ui-widgets-skin/LEARN.md) | UI 위젯 & 스킨 | Skin, TextButton, ProgressBar |
| 08 | [08-json-data-loading](./learning/08-json-data-loading/LEARN.md) | JSON 데이터 로딩 | Json, JsonReader, 데이터 직렬화 |

### Part 2: STS 클론 구현 (Ch09~13)

| 순서 | 파일 | 주제 | 구현 목표 |
|------|------|------|----------|
| 09 | [09-phase1-combat](./learning/09-phase1-combat/LEARN.md) | 최소 전투 프로토타입 | Strike/Defend/Bash vs Jaw Worm |
| 10 | [10-phase2-action-queue](./learning/10-phase2-action-queue/LEARN.md) | Action Queue & 버프 시스템 | AbstractAction, 버프/디버프, Intent |
| 11 | [11-phase3-map-run](./learning/11-phase3-map-run/LEARN.md) | 맵 & 런 구조 | DAG 맵 생성, 카드 보상, 상점 |
| 12 | [12-phase4-content](./learning/12-phase4-content/LEARN.md) | 콘텐츠 확장 | 렐릭, 포션, 업그레이드, 보스 |
| 13 | [13-audio-polish](./learning/13-audio-polish/LEARN.md) | 오디오 & 폴리싱 | SFX, BGM, 애니메이션, 시드 랜덤 |

---

## 핵심 아키텍처

```
com.simbohyeon.sts/
├── SlayTheSpire.java           # Game 클래스 (Screen 전환)
├── screen/                     # 각 화면 (MainMenu, Map, Combat, Reward, Shop)
├── model/                      # 순수 Java (libGDX 의존 없음)
│   ├── card/                   # AbstractCard, Strike, Defend...
│   ├── creature/               # Player, AbstractMonster
│   ├── combat/                 # CombatState, ActionQueue, TurnPhase
│   ├── dungeon/                # DungeonMap, MapNode
│   ├── relic/                  # AbstractRelic
│   └── buff/                   # AbstractBuff
├── data/                       # JSON 데이터 로딩
├── ui/                         # Scene2D Actor들 (CardActor, HandDisplay, EnemyActor)
└── util/                       # GameRandom, Assets
```

**핵심 원칙**: `model/`은 libGDX import 없이 순수 Java → 단위 테스트 용이, UI 교체 가능

---

## 에셋 추출 가이드

```bash
# macOS Steam 설치 경로
cd ~/Library/Application\ Support/Steam/steamapps/common/SlayTheSpire/

# JAR 추출
mkdir -p ~/sts-assets && cd ~/sts-assets
unzip ~/Library/Application\ Support/Steam/steamapps/common/SlayTheSpire/desktop-1.0.jar -d unpacked/

# 핵심 디렉토리
ls unpacked/images/cards/      # 카드 이미지
ls unpacked/images/monsters/   # 몬스터 이미지
ls unpacked/images/ui/         # UI 요소
ls unpacked/audio/             # 사운드/BGM
```

추출한 에셋을 `practice/slay-the-spire-clone/assets/`에 복사하여 사용.

> ⚠️ **주의**: 추출한 에셋은 학습 목적으로만 로컬에서 사용. 배포/공유 금지.

---

## 프로젝트 구조

```
01-slay-the-spire-clone/
├── README.md                    # 이 파일
├── learning/                    # 학습 문서 (13챕터)
│   ├── 01-libgdx-lifecycle/     # Ch01~Ch13
│   │   └── LEARN.md
│   └── ...
└── practice/                    # gdx-liftoff으로 생성할 실습 프로젝트
    └── slay-the-spire-clone/    # 단일 통합 Gradle 프로젝트
        ├── core/                # 게임 로직 전부
        ├── lwjgl3/              # Desktop 런처
        ├── assets/              # 이미지, 사운드, JSON
        └── build.gradle.kts
```
