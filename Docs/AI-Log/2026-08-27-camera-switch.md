# 3인칭 ↔ 1인칭 카메라 전환 (V키)

## 1. 메타

| 항목 | 값 |
|---|---|
| 날짜 | 2026-08-27 |
| 프로젝트 | MCP1 (연습장 — UE5 ThirdPerson 템플릿) |
| 엔진 | UE 5.8 |
| MCP 서버 | `unreal-mcp` / HTTP `127.0.0.1:8000/mcp` (ModelContextProtocol 플러그인) |
| 소요 시간 | 12분 37초 |
| MCP 호출 수 | 약 118회 (+ 셸 명령 6회) |
| 직전 커밋 | `85b21f8` "Initial commit" (22:44) — 작업 전 기준점 |
| 작업 완료 | 23:11 |

**작업 방식:** 에디터를 **켜둔 채로** 외부에서 MCP를 통해 조작. 코드 작성 후 재컴파일이 아니라,
살아 있는 에디터의 블루프린트를 직접 수정하는 방식.

---

## 2. 내가 내린 명령 (원문 그대로)

> I want to add a camera-switching feature that changes the view from third-person to
> first-person when the player presses the 'V' key. For the first-person view, I need to
> restrict the camera's pitch (limiting the upward and downward angles) and ensure the
> character rotates along with the camera to keep the movement feeling natural.

**요구사항 3개:**
1. V키로 3인칭 ↔ 1인칭 전환
2. 1인칭에서 피치(상하 시야각) 제한
3. 캐릭터가 카메라를 따라 회전 → 이동이 자연스럽게

**명시하지 않았는데 AI가 알아서 처리한 것:**
- 1인칭에서 자기 몸통 내부가 보이는 문제 (→ 메시 숨김)
- 메시를 숨기면 그림자까지 사라지는 문제 (→ `bCastHiddenShadow`)
- 3인칭 복귀 시 피치 제한을 원복해야 한다는 점

> 배운 점: **부수 문제를 명시하지 않아도 처리된다.** 다만 그래서 "무엇이 왜 추가됐는지"를
> 나중에 따로 확인해야 한다. 이 기록이 그 역할.

---

## 3. 변화점

작업 후 `git status --short`:

```
 D Content/Environment/Materials/M_Ground.uasset                          ← 이번 작업과 무관
 M Content/Input/IMC_Default.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset
 D Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/2/QY/Z7GA....uasset  ← 이번 작업과 무관
?? Content/Input/Actions/IA_SwitchCamera.uasset
```

> **삭제 2건(`D`)은 카메라 작업과 무관합니다.** 작업 전에 내가 직접 테스트용으로 만들었다가
> 원상복구하려고 지운 것. 나중에 이 기록을 볼 때 혼동하지 말 것.

### 실제 변경 내역

| 상태 | 파일 | 내용 |
|---|---|---|
| 신규 | `Content/Input/Actions/IA_SwitchCamera.uasset` | Boolean 입력 액션 |
| 수정 | `Content/Input/IMC_Default.uasset` | V → IA_SwitchCamera 매핑 추가 |
| 수정 | `BP_ThirdPersonCharacter.uasset` | 카메라 컴포넌트 + 변수 5개 + 함수 1개 + 이벤트 배선 |
| 수정 | `BP_ThirdPersonPlayerController.uasset` | **재직렬화만** — 그래프 내용 동일 (save-all 부작용) |

**변경 규모: 프로젝트 251개 파일 중 실질 수정 3 + 신규 1.**

### 추가된 것 상세

**컴포넌트** — `FirstPersonCamera` (CameraComponent), 캡슐에 부착

| 설정 | 값 | 이유 |
|---|---|---|
| 위치 | (10, 0, 75) | 발바닥 기준 약 171cm 눈높이. X=10은 근평면 여유 |
| FOV | 90 | 템플릿 FollowCamera와 동일 |
| `bUsePawnControlRotation` | true | 뷰가 컨트롤 로테이션을 따름 |
| `bAutoActivate` | **false** | 3인칭이 시작 상태 → BeginPlay 초기화 로직 불필요 |

**변수 5개** (피치 한계는 인스턴스 편집 가능하게 노출)

| 변수 | 기본값 |
|---|---|
| `bIsFirstPerson` | false |
| `FirstPersonPitchMin` / `Max` | -60 / 60 |
| `ThirdPersonPitchMin` / `Max` | -89.9 / 89.9 (엔진 기본값) |

**함수 `ToggleCameraView`** — `IA_SwitchCamera → Started`에서 호출 (누를 때 1회만 발동)

| 대상 | 1인칭 | 3인칭 |
|---|---|---|
| 카메라 | FollowCamera off / FirstPersonCamera on | 반대 |
| `bUseControllerRotationYaw` | true | false |
| `bOrientRotationToMovement` | false | true |
| Mesh `SetOwnerNoSee` | true | false |
| CameraManager `ViewPitchMin/Max` | ±60 | ±89.9 |

---

## 4. 구현 분석 — 왜 이게 동작하는가

### (1) 카메라 전환: `SetActive` 하나로 되는 이유

`AActor::CalcCamera`는 액터에 붙은 카메라 컴포넌트들을 순회하면서
**활성화된 첫 번째 것**을 뷰로 채택합니다. 그래서 `SetViewTarget` 같은 무거운 경로를 타지 않고
`SetActive` 토글만으로 뷰가 바뀝니다.

`bAutoActivate=false` 덕분에 시작 시점엔 FollowCamera만 활성 → 3인칭이 기본이 되고,
BeginPlay에서 초기화할 게 없어집니다.

### (2) "이동이 자연스럽다"의 정체 — 이게 이 작업의 핵심

요구사항 3번의 실체는 **두 플래그의 반전**입니다.

| | 3인칭 | 1인칭 |
|---|---|---|
| `bUseControllerRotationYaw` | false | **true** |
| `bOrientRotationToMovement` | true | **false** |

- **3인칭**: 몸이 *가는 방향*을 향함. 카메라와 몸이 따로 놂 (뒤를 보며 달리기 가능)
- **1인칭**: 몸이 *보는 방향*을 향함. 카메라와 몸이 한 몸

그리고 템플릿의 `Move` 노드는 **이미 컨트롤 로테이션 기준으로 이동 방향 벡터를 만듭니다.**
그래서 1인칭에서 몸이 시선을 따라가면 → 좌우 스트레이프가 화면과 자동으로 일치합니다.
**Move 로직은 손댈 필요가 없었습니다.**

### (3) 피치 제한은 왜 CameraManager에?

카메라 컴포넌트나 스프링암에 걸면 화면만 안 돌아가고 **실제 조준 각도는 그대로**입니다.
`PlayerCameraManager`의 `ViewPitchMin` / `ViewPitchMax`는 컨트롤 로테이션 자체를 클램프하므로
여기가 맞는 위치입니다.

단, 이 값은 **컨트롤러 소유**입니다 → 3인칭 복귀 시 원복하지 않으면 제한이 남습니다.

### (4) 메시 숨김과 그림자

`SetOwnerNoSee(true)` = 소유자에게만 안 보임 (다른 플레이어에겐 보임).
그런데 그러면 **그림자도 같이 사라집니다.** `bCastHiddenShadow=true`로 그림자만 살렸습니다.

---

## 5. 이번 작업에 쓰인 엔진 지식

이 작업이 성립하려면 알아야 했던 비자명한 것들입니다. 이 표만 읽어도 복기가 됩니다.

| 지식 | 내용 |
|---|---|
| `CalcCamera`의 카메라 선택 | `AActor::CalcCamera`는 붙어 있는 카메라 컴포넌트를 순회해 **활성화된 첫 번째**를 뷰로 쓴다. 그래서 `SetActive` 토글만으로 전환된다 |
| `bAutoActivate=false` | 시작 상태를 컴포넌트 설정으로 정해두면 `BeginPlay` 초기화 로직 자체가 필요 없어진다 |
| 회전 플래그 한 쌍 | `bUseControllerRotationYaw` ↔ `bOrientRotationToMovement`가 3인칭/1인칭을 가르는 핵심. 몸이 *가는 방향*을 보느냐 *보는 방향*을 보느냐의 차이 |
| 템플릿 `Move`의 기준축 | 템플릿 `Move`는 **이미 컨트롤 로테이션 기준**으로 이동 벡터를 만든다. 그래서 1인칭에서 몸이 시선을 따라가면 스트레이프가 화면과 자동 일치 — 이동 로직 수정이 불필요했다 |
| 피치 제한의 올바른 위치 | 카메라·스프링암에 걸면 화면만 안 돌고 **실제 조준각은 그대로**다. `PlayerCameraManager.ViewPitchMin/Max`가 컨트롤 로테이션 자체를 클램프한다 |
| 피치 제한의 소유자 | 그 값은 **컨트롤러 소유**다. 3인칭 복귀 시 원복하지 않으면 제한이 남는다 |
| `SetOwnerNoSee`와 그림자 | 소유자에게만 숨기지만 **그림자까지 사라진다.** `bCastHiddenShadow=true`로 그림자만 살린다 |
| Enhanced Input 트리거 종류 | `Started`는 누르는 순간 1회만 발동. `Triggered`를 쓰면 매 프레임 토글돼 깜빡인다 |
| `bUsePawnControlRotation` | true인 카메라는 **부모의 회전을 무시**한다 (위치만 상속). 캡슐에 붙여도 캡슐 회전에 끌려가지 않는 이유 |

---

## 6. 검증 범위

**확인된 것**
- [x] 블루프린트 컴파일 정상
- [x] 기존 이벤트 그래프 노드 15개 무손상
- [x] IMC_Default 기존 매핑 12개 + 모디파이어 객체 무손상
- [x] PIE 실행 시 캐릭터 정상 스폰, 기본값 정상, 런타임 에러 없음
- [x] 1인칭 눈높이·프레이밍 정상, 지오메트리 클리핑 없음 (스크린샷 확인)
- [x] `git status`로 변경 범위 4개 파일 확인

**확인 못 한 것**
- [ ] **실제 V 키 입력으로 전환되는지** — AI에게 입력 주입 도구가 없어 미검증.
      PIE에서 직접 눌러서 왕복(3인칭→1인칭→3인칭) 확인 필요
- [ ] 피치 제한이 실제로 ±60에서 걸리는지 (마우스로 위아래 끝까지 돌려볼 것)
- [ ] 3인칭 복귀 후 피치가 ±89.9로 원복되는지

---

## 7. 설계 판단과 대안

**"내 결정" 칸만 사용자 몫입니다** — 대안 쪽으로 갈 생각이 생기면 거기 적으세요.

| 선택한 방식 | 대안 | 트레이드오프 | 선택 이유 | 내 결정 |
|---|---|---|---|---|
| 카메라를 **캡슐**에 부착 | 헤드 본 소켓에 부착 | 캡슐 = 흔들림 없는 안정된 뷰 / 헤드 본 = 헤드밥은 생기지만 축 보정·애님 틱 고정·프레임 동기·멀미 문제가 따라옴 | 요구사항이 "이동이 자연스럽게"였지 "연출"이 아니었다. 헤드 본은 문제 4개를 한꺼번에 들고 온다 | |
| 메시 전체 숨김 (`SetOwnerNoSee`) | 별도 1인칭 팔 메시 추가 | 숨김 = 간단하지만 손이 안 보임 / 팔 메시 = FPS다운 연출, 작업량 증가 | 몸통 내부가 보이는 문제만 막으면 되는 상황. 팔 메시는 애셋 제작이 따로 필요하다 | |
| `SetActive` 즉시 전환 | `SetViewTargetWithBlend` 또는 요 보간 | 즉시 컷 = 코드 한 줄 / 블렌드 = 부드럽지만 전환 중 입력 처리를 따로 정해야 함 | `CalcCamera`가 활성 카메라를 고르므로 `SetActive`가 가장 짧은 경로. 다만 3인칭에서 뒤를 보며 달리다 전환하면 **몸이 한 프레임에 스냅해 튄다** | |
| 피치 한계를 **인스턴스 편집 가능 변수**로 노출 | 함수 안에 하드코딩 | 노출 = 에디터에서 바로 조정 / 하드코딩 = 그래프가 짧아짐 | 튜닝 값이라 손으로 맞출 대상. ±60은 보수적이고 일반 FPS는 ±80~89다 | |

### 추가로 확인해볼 것

- UE 5.5 이후 엔진에 **전용 1인칭 렌더링 경로**(FP 프리미티브 분리, FP 전용 FOV, 셀프 섀도잉)가
  들어왔습니다. 5.8이면 있을 텐데, 이게 있으면 `SetOwnerNoSee` + `bCastHiddenShadow` 조합을
  엔진 기능으로 대체할 수 있습니다. → **5.8 문서에서 직접 확인 필요**
- 1인칭 피치 ±60은 보수적인 값입니다. 일반적인 FPS는 ±80~89 정도.

### 알아둘 잠재 이슈

- `PlayerCameraManager` 상태는 컨트롤러 소유 → 1인칭 상태에서 사망/리스폰 시
  `bIsFirstPerson`과 실제 상태가 어긋날 수 있음 (리스폰이 있는 게임이라면)
- `Cast to PlayerController` 실패 경로 — AI 포제스나 멀티플레이 시뮬레이션 프록시에선
  카메라 매니저가 없음. 싱글이면 무관

---

## 8. 재현 난이도 — 다시 만든다면 어디가 까다로운가

| 단계 | 난이도 | 까다로운 지점 |
|---|---|---|
| Enhanced Input 액션 생성 + IMC 매핑 | 쉬움 | 정형화된 절차. 단 `Triggered`가 아니라 **`Started`** 를 써야 한다 |
| 카메라 컴포넌트 추가 + 트랜스폼 | 쉬움 | 눈높이(Z=75)와 근평면 여유(X=10)는 감으로 잡는 값 |
| `SetActive` 방식으로 전환 | 보통 | `CalcCamera`가 활성 카메라를 고른다는 걸 알아야 이 짧은 경로가 보인다. 모르면 `SetViewTarget`으로 돌아간다 |
| 회전 플래그 반전 | **함정** | 두 플래그를 반대로 걸면 1인칭에서 몸이 안 돌거나 3인칭에서 스트레이프가 깨진다. **이 작업의 실질적 난이도가 여기 있다** |
| 피치 제한 적용 | **함정** | 카메라·스프링암에 걸면 화면만 안 돌고 조준각은 그대로다. `PlayerCameraManager`가 맞는 위치이고, 컨트롤러 소유라 **3인칭 복귀 시 원복**해야 한다 |
| 메시 숨김 + 그림자 유지 | **함정** | `SetOwnerNoSee`만 쓰면 그림자까지 사라진다. `bCastHiddenShadow`를 몰랐다면 원인을 찾기 어렵다 |
| `bAutoActivate=false` 로 시작 상태 지정 | 보통 | 알면 `BeginPlay` 초기화가 통째로 사라지는데, 모르면 초기화 노드를 짜게 된다 |

**이 작업의 핵심 한 줄:**
"이동이 자연스럽게"라는 요구사항의 실체는 `bUseControllerRotationYaw` ↔ `bOrientRotationToMovement`
**두 플래그의 반전**이었다. 템플릿 `Move`가 이미 컨트롤 로테이션 기준이라 이동 로직은 손댈 필요가 없었다.

**다음에 시도해볼 작업:**
- [ ] 전환 스냅 완화 (블렌드 또는 요 보간)
- [ ] Camera Shake로 헤드밥 추가 (헤드 본 부착보다 통제하기 쉬움)
- [ ] 1인칭 팔 메시
- [ ] UE 5.8 First Person 렌더링 기능 조사

---

## 9. 인수인계 — 다음 세션이 이어받을 것

**없음.** 이 세션의 미결 항목은 모두 처리됐다.

- ~~애셋 미커밋~~ → 2026-08-28 세션에서 `cff2ebb` 로 커밋 (수정·신규 4건).
  무관한 삭제 2건은 `4400782` 로 따로 처리
- 남은 아이디어는 위 "다음에 시도해볼 작업"에 있다. 미결이 아니라 선택 사항이다
