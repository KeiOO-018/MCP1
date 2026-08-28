# 2026-08-27

## 작업물

`BP_ThirdPersonCharacter`에 V키로 3인칭 ↔ 1인칭 시점을 전환하는 기능. 1인칭에서는 피치를 제한하고 몸이 시선을 따라간다.

**소요 시간**: 12분 37초

## 명령

### 한글

> 3인칭 플레이어가 V키를 누르면 1인칭으로 변하게 되는 시점 전환 기능을 추가하려고해. 1인칭 때 주의할 점은 카메라가 너무 아래나 위를 보는것을 제한하고(각도 제한), 옆으로 돌릴 때, 캐릭터도 같이 움직여서 움직임에 어색하지 않게 하고 싶어.

### English — MCP에 실제로 보낸 명령

> I want to add a camera-switching feature that changes the view from third-person to first-person when the player presses the 'V' key. For the first-person view, I need to restrict the camera's pitch (limiting the upward and downward angles) and ensure the character rotates along with the camera to keep the movement feeling natural.

**옮기며 들어간 해석** — 한글 원문의 "각도 제한"에는 숫자가 없었고 영어 문장에도 숫자를 넣지 않았다. **1인칭 ±60도는 사용자가 말한 값이 아니라 구현 중 임의로 고른 값이다.** 아래 `남는 리스크`에서 다시 다룬다.

## Terminal 결과

### 원문 — English

**남아 있지 않다.** MCP 조작은 세션 중에만 출력이 있었고 따로 확보해두지 않았다.
아래 요약은 터미널 출력이 아니라 **커밋 `cff2ebb`의 실제 변경 애셋에서 사후 재구성한 것**이다.
즉 이 칸은 이번 기록에서 증거가 아니라 정황이다.

### 요약 — 한글

MCP로 에디터를 켠 채 라이브 조작. 커밋 `cff2ebb` 기준 변경된 애셋 4개.

| 애셋 | 변화 | 내용 |
|---|---|---|
| `Content/Input/Actions/IA_SwitchCamera.uasset` | 신규 (1,393 B) | Boolean 타입 InputAction |
| `Content/Input/IMC_Default.uasset` | 7,787 → 8,324 B | V 키 매핑 추가. **기존 12개 매핑·모디파이어 보존 확인** |
| `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset` | 148,667 → 243,750 B | 컴포넌트 1 + 변수 5 + 함수 1 + 이벤트 바인딩 |
| `Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset` | 83,213 → 82,861 B | 피치 제한 적용 |

MCP 조작 로그 원문은 남아 있지 않다. 실패한 호출은 없었다.

## 분석

### 무엇을 만들었나

**입력**
- `IA_SwitchCamera` (Boolean) 신규 생성
- `IMC_Default`에 V 키 매핑 추가 — 기존 12개 매핑과 모디파이어가 그대로인지 작업 후 재확인

**컴포넌트**
- `FirstPersonCamera`를 캡슐에 부착
- 상대 위치 `(10, 0, 75)` / FOV `90`
- `bUsePawnControlRotation = true`
- `bAutoActivate = false`

**변수** (전부 인스턴스 편집 가능)
- `bIsFirstPerson`
- 1인칭 피치 하한·상한, 3인칭 피치 하한·상한 — 4개

**함수**
- `ToggleCameraView`
- `IA_SwitchCamera`의 `Started`에서 호출

### 기술적으로 맞게 짚은 부분

**카메라 전환 방식이 정석이다.** `AActor::CalcCamera`가 활성화된 첫 번째 카메라 컴포넌트를 잡는 성질을 이용해 `SetActive` 토글만으로 뷰를 바꿨다. `SetViewTarget` 같은 무거운 경로를 타지 않은 게 맞다. `bAutoActivate = false`로 둔 덕분에 `BeginPlay` 초기화 로직이 아예 필요 없어진 것도 깔끔하다.

**"자연스러운 이동"의 핵심을 정확히 이해했다.** 요청의 진짜 요구사항은 `bUseControllerRotationYaw` ↔ `bOrientRotationToMovement` 쌍의 반전이다. 템플릿 `Move` 노드가 이미 컨트롤 로테이션 기준으로 방향 벡터를 만들기 때문에, 1인칭에서 몸이 시선을 따라가면 스트레이프가 화면과 자동으로 일치한다. **여기 손 안 댄 판단이 옳다** — 추가로 건드렸으면 오히려 어긋났다.

**피치 제한을 건 위치가 맞다.** 카메라 컴포넌트나 스프링암이 아니라 `PlayerCameraManager`의 `ViewPitchMin` / `ViewPitchMax`, 즉 컨트롤러 레벨에서 막아야 실제 조준 각도가 제한된다. 3인칭 복귀 시 엔진 기본값 ±89.9로 되돌리는 것까지 챙겼다.

**요청에 없던 부수 문제를 스스로 처리했다.** 1인칭에서 몸통 내부가 보이는 문제 → `SetOwnerNoSee`. 그로 인해 그림자가 사라지는 문제 → `bCastHiddenShadow = true`. 둘 다 요청에 없었지만 안 하면 바로 티가 난다.

**그래프 파괴를 경계한 작업 순서.** BP 그래프를 MCP로 조작하는 건 노드 ID 기반이라 깨지기 쉽다. 노드 ID를 먼저 조회하고, 작업 후 원본 15개 노드의 무결성을 재확인하는 흐름으로 방어했다. MCP 호출이 100회에 가까웠던 이 작업의 실질적 난이도가 여기였다.

### 확인한 것 / 확인 못 한 것

**확인한 것** — 컴파일 통과, PIE 스폰, 변수 기본값, 1인칭 눈높이 렌더링(화면 캡처로 대조).

**확인 못 한 것** — **V 키 입력 자체.** 입력 주입 도구가 없어서 실제로 키를 눌러본 적이 없다. 즉 `IMC_Default`의 매핑 → `IA_SwitchCamera` → `Started` → `ToggleCameraView`로 이어지는 경로 전체가 미검증이다. 컴포넌트와 변수가 올바른 것과 **토글이 실제로 도는 것은 별개다.**

**BP_ThirdPersonPlayerController가 modified로 뜬 건** save-all 재직렬화이고 내용은 동일함을 재확인했다. 바이트 수가 오히려 줄어든 것과 일치한다.

### 남는 리스크

- **전환이 즉시 컷이다.** `SetActive` 토글이라 블렌드가 없다. 게다가 1인칭 진입 순간 `bUseControllerRotationYaw`가 켜지면서 몸이 컨트롤 요로 한 프레임에 스냅한다. **3인칭에서 뒤를 보며 달리던 중이면 눈에 띄게 튄다.** 부드럽게 하려면 `SetViewTargetWithBlend` 또는 요 보간이 필요하다.
- **1인칭 피치 ±60은 보수적이다.** 보통 FPS는 ±80~89 정도다. 사용자가 지정한 값이 아니라 구현 중 고른 값이다. 인스턴스 편집 가능하게 노출해뒀으니 디테일 창에서 조정 가능하다.
- **`PlayerCameraManager` 상태는 컨트롤러 소유다.** 1인칭 상태에서 언포제스·리스폰·사망이 일어나면 ±60이 남아 있거나 반대로 리셋될 수 있다. 캐릭터가 죽고 다시 스폰되는 게임이면 `bIsFirstPerson`과 실제 상태가 어긋날 여지가 있다.
- **`Cast to PlayerController` 실패 경로.** AI 포제스나 멀티플레이 시뮬레이션 프록시에서는 카메라 매니저가 없다. 싱글 템플릿이면 문제없지만 확장 시 가드가 필요하다.
- **트레이드오프로 고른 두 가지** — 캡슐 부착(헤드밥 없음), 메시 숨김(별도 팔 메시 없음). 결함이 아니라 선택이다. 다만 1인칭 팔이 보여야 하는 게임이면 여기서부터 다시 설계해야 한다.

### 총평

요청 3개(V키 전환, 피치 제한, 캐릭터-카메라 동조)를 모두 충족했고 각각을 엔진의 정석 경로로 처리했다. 이 작업의 실질적 난이도는 기능 자체가 아니라 **MCP로 라이브 에디터를 100회 가까이 조작하면서 기존 애셋(IMC 12개 매핑, 이벤트 그래프 15개 노드)을 깨뜨리지 않는 것**이었고, 그걸 통과했다.

## AI의 제안

> Attach the camera to the head socket instead

캡슐 부착 대신 헤드 소켓에 카메라를 붙이는 안. 채택하면 헤드밥이 생겨 1인칭 이동감이 살지만, 애니메이션 진폭이 그대로 화면에 실려서 멀미 요인이 될 수 있다. 미결.

## 다음으로 넘김

- **PIE에서 V를 직접 눌러 토글 왕복을 확인한다.** 이 작업에서 유일하게 미검증으로 남은 항목이고 최우선이다
- **전환 스냅 완화** — 요 보간 또는 `SetViewTargetWithBlend`. 위 확인이 끝난 다음
- **결정 필요 ①** 1인칭 피치를 ±60에서 올릴 것인가. 사용자가 정한 값이 아니다
- **결정 필요 ②** 카메라를 헤드 소켓으로 옮길 것인가 (위 제안). 1인칭 팔 메시를 쓸 계획이 있는지에 달렸다
