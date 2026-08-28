# 2026-08-28

## 작업물

`BP_ThirdPersonCharacter`에 UE 5.8 FirstPerson 템플릿의 전신 1인칭 구조를 이식해, 1인칭 전환 시 자기 팔이 보이도록 했다.

**소요 시간**: 약 2시간 15분 (직전 커밋 `98630f1` 10:19:01 이후 첫 작업 ~ 넘김 항목 정리 커밋 `d206fce` 12:34:10). 세션 시작 시각이 따로 기록돼 있지 않아 커밋 타임스탬프로 잡은 값이다.

## 명령

### 한글

> 지난 작업 보자

> 1인칭 팔 메시 쓸거긴해 그럼 제안은?

이 지점에서 선택지 세 개를 제시하고 답을 받았다. 타이핑이 아니라 선택이라 원문이 없으므로 고른 항목을 적는다.

- 팔 메시 출처: `FirstPerson 템플릿 콘텐츠 추가`
- 팔의 용도: `무기를 들 예정`
- 카메라 부착: `캡슐 유지 — 헤드 소켓 안 씀`

> A로하자

> V아주잘됨

> 이거 Content Drawer에서 우클릭 후 Add Feature or Content Pack 해야되는데 Tools에 없어 이거 확인좀

> 이거 틀린 이유랑 다음에 이런일이 일어나지 않게 하기 위한 대처

> 1번먼저

> 커밋하고 내가 OnePerson 저거 추가했어

> 이거 이렇게뜨는데 글자가 깨지는 저거 어떻게 해결할까

> A

> 우선 저 명령어로 해서 영어로 잘나오네 그다음

> 두번째명령해서 작업끝났어확인좀

> head지정했어

> 일단 저건 손에 무기를 들거나 상호작용같은 애니메이션을 해봐야알겠는데

> 눈높이는 문제없어

> 커밋먼저하자

> 1. v를 누르고 나서 바로 보이는 화면
> 2. 3인칭 정면

> 1인칭 플레이 화면, 캐릭터가 앞으로 갈때 나오는 손이 왔다갔다하는 애니메이션때 손이 아래에서 잠깐 올라와서보이는데 화면의 가장 아래쪽에 조금씩보였다가사라짐

> 3. 4는 문제없어

> BP_ThirdPersonCharacter 의 FirstPersonCamera의 부모 소켓값은 head야 커밋하고 기록에 지금 했던 명령있잔아 그걸 통합요약해서 기록본 하나 작성하고 그 다음 작업은 다음 세션에서 하는게 나아 아니면 여기서하는게 나은지 확인 후 진행하자

### English — MCP에 실제로 보낸 명령

Terminal에 붙여 넣도록 뽑아준 영어 원문 그대로다. 조회·검증 목적의 MCP 호출은 내가 직접 했고 자연어 명령이 아니라서 여기 적지 않는다.

명령 1 — `FirstPersonMesh` 추가

> In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, add a new SkeletalMeshComponent named FirstPersonMesh as a child of the existing Mesh component. Set its SkeletalMeshAsset to /Game/Characters/Mannequins/Meshes/SKM_Quinn_Simple.SKM_Quinn_Simple and its AnimClass to /Game/FirstPerson/Anims/ABP_FP_Copy.ABP_FP_Copy_C. Set bOnlyOwnerSee to true, CastShadow to false, bCastHiddenShadow to false, and bVisible to false. Leave its relative location and rotation at zero. Then compile the Blueprint.

명령 2 — 카메라를 `head` 본으로 재부착

> In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, re-attach the existing FirstPersonCamera component so that its parent is the FirstPersonMesh component and its parent socket is the bone named head. Set its RelativeLocation to X=2.793880, Y=5.880724, Z=0.0 and its RelativeRotation to Pitch=0.0, Yaw=90.0, Roll=-90.0. Leave bAutoActivate at false, bUsePawnControlRotation at true, and FieldOfView at 90 exactly as they already are. Do not modify any other component, and do not change the SpringArm or the third-person CameraComponent. Then compile the Blueprint and report back the resulting parent component, parent socket, relative location, relative rotation, bAutoActivate, bUsePawnControlRotation, and FieldOfView of FirstPersonCamera.

명령 3 — 토글에 가시성 연결

> In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, edit the existing function ToggleCameraView. In the branch that runs when the new bIsFirstPerson value is true, add a SetVisibility node targeting the FirstPersonMesh component with NewVisibility set to true, inserted into the execution chain immediately after the existing SetOwnerNoSee node in that branch. In the branch that runs when the new bIsFirstPerson value is false, add a SetVisibility node targeting the FirstPersonMesh component with NewVisibility set to false, inserted into the execution chain immediately after the existing SetOwnerNoSee node in that branch. Leave bPropagateToChildren at its default value of false on both nodes. Do not add, remove, reorder, retarget, or disconnect any other node in this function or anywhere else in the Blueprint. Then compile the Blueprint and report back the complete node list and execution order of ToggleCameraView for both branches.

명령 4 — 조준 포즈 테스트 (버리는 작업)

> In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, temporarily change the Mesh component (CharacterMesh0) so that AnimationMode is AnimationSingleNode and AnimationData animToPlay is /Game/Characters/Mannequins/Anims/Rifle/MF_Rifle_Idle_ADS.MF_Rifle_Idle_ADS with looping enabled and playing enabled. Leave AnimClass pointing at ABP_Unarmed_C so it can be restored later — do not clear it. Do not modify FirstPersonMesh, FirstPersonCamera, the SpringArm, the third-person CameraComponent, or the ToggleCameraView function. Do not save the Blueprint to disk. Then compile and report back AnimationMode, AnimClass, and AnimationData for the Mesh component.

명령 5 — 테스트 되돌리기

> In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, restore the Mesh component (CharacterMesh0) to its original animation setup: set AnimationMode back to AnimationBlueprint and clear AnimationData animToPlay back to None. AnimClass should already be /Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C — leave it as is. Do not modify FirstPersonMesh, FirstPersonCamera, the SpringArm, the third-person CameraComponent, or the ToggleCameraView function. Then compile and report back AnimationMode, AnimClass, and AnimationData for the Mesh component.

명령 외 — 터미널 에이전트 출력 언어 지시. MCP 명령이 아니라 터미널 안에서 도는 에이전트에게 준 지시다. 한글이 두부로 깨져서 넣었다.

> From now on, write all of your output in English only. Do not use Korean, Japanese, or Chinese characters anywhere — not in prose, tables, bullet lists, headings, or status lines. The UE Terminal renders with CascadiaMono, which has no Hangul glyphs and no CJK fallback font, so any Korean text you print shows up as unreadable boxes. This applies to everything you write, including summaries and verification reports. Box-drawing and table characters are fine.

**옮기며 들어간 해석** — 한글 지시에 없던 값을 영어 명령에 넣은 것들이다. 전부 내가 정했다.

- 명령 1의 `bVisible = false`. Epic 참조 구현에는 없다. 그쪽은 항상 1인칭이라 켜둔 채지만 이 프로젝트는 3인칭으로 시작하므로, 끄지 않으면 3인칭일 때 소유자 화면에 팔이 몸 앞에 떠 보인다.
- 명령 1의 컴포넌트 이름 `FirstPersonMesh`. Epic과 같게 맞춰 나중에 대조하기 쉽게 했다.
- 명령 2의 좌표는 `BP_FirstPersonCharacter`에서 읽은 참조값이지만, 원본 회전 `Yaw=89.999999301698679 / Roll=-89.999999300843086`을 `90 / -90`으로 반올림한 것은 내 손이다.
- 명령 3의 삽입 위치 "`SetOwnerNoSee` 바로 뒤"와 `bPropagateToChildren=false` 유지.
- 명령 4의 애님 선택 `MF_Rifle_Idle_ADS`. "무기를 들거나 상호작용같은 애니메이션"이라는 말에는 특정 애셋이 없었다. 두 팔이 시야 중앙에 모이는 포즈라 판정에 유리해서 골랐다.
- 출력 언어 지시의 "일본어·중국어도 금지"와 "박스 문자는 괜찮다". 요청은 한글 깨짐에 대한 것이었다.

## Terminal 결과

### 원문 — English

성공 보고는 판단 근거가 된 줄만 발췌했고, 실패·경고는 전문을 붙였다.

명령 2 — 소켓 설정 실패. 전문.

> Parent socket │ NOT SET — and not readable
>
> The socket could not be set
>
> set_properties rejected it outright:
>
> SetObjectProperties on '...BP_ThirdPersonCharacter_C:FirstPersonCamera_GEN_VARIABLE'
> (CameraComponent): the following properties could not be set: AttachSocketName
>
> This is a real limitation of the toolset, not a transient failure. I checked the engine source at C:\Program Files\Epic Games\UE_5.8\Engine\Source:
>
> - Runtime/Engine/Classes/Components/SceneComponent.h:112 — AttachSocketName is declared UPROPERTY(ReplicatedUsing = OnRep_AttachSocketName, ...) with no Edit flag.
> - Runtime/Engine/Classes/Engine/SCS_Node.h:44 — AttachToName, which is the field that actually stores the socket for Blueprint SCS components, is a bare UPROPERTY(), also with no Edit flag.
>
> The property tool only exposes editable properties, so both are out of reach. I reached the SCS node object itself (...BP_ThirdPersonCharacter_C:SimpleConstructionScript_0.SCS_Node_0 resolves and reports its class as SCS_Node), but reading or writing AttachToName on it fails the same way. set_parent_component takes only a component and a parent — no socket argument — and no tool in any of the 19 toolsets accepts a socket for component attachment.
>
> I also cannot read the socket back, so I cannot report its current value:
>
> GetObjectProperties on '...FirstPersonCamera_GEN_VARIABLE' (CameraComponent):
> the following properties could not be read: AttachParent, AttachSocketName

내가 직접 같은 호출을 때려 재현했다. 전문.

> SetObjectProperties on '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C:FirstPersonCamera_GEN_VARIABLE' (CameraComponent): the following properties could not be set: AttachSocketName

명령 1 — 컴파일 응답이 실제와 어긋난 사례. 전문.

> Compile returned null. Verifying actual state rather than trusting the responses.

명령 4·5 — 애니메이션 경고. 전문.

> LogAnimation: Warning: Invalid animation skeleton
> LogAnimation: Warning: Invalid animation skeleton
> LogAnimation: Warning: Currently in Animation Blueprint mode. Please change AnimationMode to Use Animation Asset

명령 5 — 세터 부작용이 비대칭이라는 관찰. 발췌.

> Writing AnimationData had flipped AnimationMode to AnimationSingleNode automatically on the way in; clearing animToPlay back to None did not flip it back — the mode stayed AnimationSingleNode.

명령 3 — 성공 보고. 발췌.

> Node count went 30 → 34. All 30 original nodes are still present under their original names.

에디터 폰트 경고. 한글 깨짐의 직접 증거다. 발췌.

> LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+d6c4, getting last resort font data

내가 직접 확인한 MCP 경로 불일치. 전문.

> Unknown tool editor_toolset.toolsets.asset.AssetTools.find_assets

> Asset does not exist: /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter

### 요약 — 한글

FirstPerson 콘텐츠 팩을 넣고, `BP_ThirdPersonCharacter`에 컴포넌트 하나를 더해 카메라를 옮기고, `ToggleCameraView`에 두 줄을 끼웠다.

| 대상 | 변화 |
|---|---|
| `Content/FirstPerson/` | 신규 8개 — `ABP_FP_Copy`, `CtrlRig_FPWarp`, BP 4개, `Lvl_FirstPerson`, `MI_FirstPersonColorway` |
| `Content/Weapons/` | 신규 27개 — `SKM_Pistol` / `SKM_Rifle` / `SKM_GrenadeLauncher` 및 머티리얼·텍스처 |
| `Content/__ExternalActors__/FirstPerson/`, `__ExternalObjects__/FirstPerson/` | `Lvl_FirstPerson`용 신규 |
| `BP_ThirdPersonCharacter.uasset` | 243,750 → 254,333 B. 컴포넌트 1개 추가, 카메라 1개 재부모화, 노드 30 → 34 |
| `Content/Input/IMC_Default.uasset` | **변화 없음.** 8,324 B 유지 |
| `CLAUDE.md` | 규칙 2개 추가 |
| `Docs/AI-Log/2026-08-27-camera-switch.md` | 처리된 넘김 항목 2개 삭제 |

애셋 총계 240 → 339개. 팩 추가로 **덮어쓴 기존 애셋은 0개**다.

커밋 4개: `d27a6da`(CLAUDE.md 규칙), `5bf3bab`(팩), `436968c`(구현), `d206fce`(넘김 항목 정리).

## 분석

### 무엇을 만들었나

**컴포넌트 — `FirstPersonMesh` (신규)**

- 부모: `Mesh`(= `CharacterMesh0`)
- `SkeletalMeshAsset`: `SKM_Quinn_Simple` — 3인칭과 같은 애셋
- `AnimClass`: `ABP_FP_Copy_C`, `AnimationMode`: `AnimationBlueprint`
- `bOnlyOwnerSee = true`, `bOwnerNoSee = false`
- `CastShadow = false`, `bCastHiddenShadow = false`
- `bVisible = false` (3인칭으로 시작하므로)
- 상대 위치 `(0, 0, 0)` / 회전 `(0, 0, 0)`

**컴포넌트 — `FirstPersonCamera` (기존, 재부모화)**

- 부모: `CollisionCylinder` → `FirstPersonMesh`, 부모 소켓 `head`
- 상대 위치: `(10, 0, 75)` → `(2.793880, 5.880724, 0)`
- 상대 회전: `(0, 0, 0)` → `(Pitch 0, Yaw 90, Roll -90)`
- `bAutoActivate = false`, `bUsePawnControlRotation = true`, `FieldOfView = 90` — 셋 다 기존 값 유지

**함수 — `ToggleCameraView` (기존, 2줄 추가)**

- 1인칭 분기: `SetOwnerNoSee(Mesh, true)` 다음에 `SetVisibility(FirstPersonMesh, true)`
- 3인칭 분기: `SetOwnerNoSee(Mesh, false)` 다음에 `SetVisibility(FirstPersonMesh, false)`
- 두 노드 모두 `bPropagateToChildren = false`
- 기존 14줄은 순서·연결 그대로

**최종 계층**

```
CollisionCylinder
├─ SpringArmComponent_0
│  └─ CameraComponent_0          (3인칭)
└─ CharacterMesh0                 SKM_Quinn_Simple / ABP_Unarmed
   └─ FirstPersonMesh             SKM_Quinn_Simple / ABP_FP_Copy
      └─ FirstPersonCamera        socket = head
```

**규칙 — `CLAUDE.md` `# 출력 방식`에 2개 추가**

- 코드 블록은 검증한 것만 넣는다. 미검증 UI 경로·메뉴 위치·버전별 동작은 산문으로 쓰고 "확인 안 함"을 붙인다. 엔진 소스가 `C:\Program Files\Epic Games\UE_5.8\Engine\Source`에 있으니 추측 대신 확인한다.
- 정정할 때 새로운 추측을 덧붙이지 않는다.

### 기술적으로 맞게 짚은 부분

**참조 구현을 먼저 읽고 사양을 뒤집은 것.** 처음 세운 안은 "카메라는 캡슐에 두고 팔 메시를 카메라의 자식으로 단다"였고 사용자 승인까지 받았다. 그런데 `BP_FirstPersonCharacter`를 실제로 읽어보니 부착 순서가 정반대였다 — 카메라가 1인칭 메시의 자식이고, 1인칭 메시는 3인칭 메시의 자식이다. **승인받은 결정이라도 증거가 어긋나면 되돌리는 게 맞다.** 그대로 갔으면 워프 리그가 전제하는 배치를 벗어났을 것이다.

**`bUsePawnControlRotation`이 헤드밥 문제를 반만 만든다는 것.** 이 값이 `true`면 카메라의 월드 회전은 매 프레임 컨트롤 로테이션으로 덮인다. 부모 본이 흔들려도 **위치만 따라가고 회전은 안 따라간다.** 그래서 머리에 붙여도 멀미 요인인 회전 흔들림은 안 생기고 이동감인 위치 흔들림만 남는다. 처음에 "헤드 소켓은 애니메이션을 카메라에 그대로 싣는다"고 한 건 절반만 맞았다.

**팩을 넣기 전에 무엇이 덮일지 파일 단위로 대조한 것.** `TemplateDefs.ini`가 공유 팩 `Input`을 끌고 오고, 그 팩의 `IMC_Default.uasset`(7,787 B)이 이 프로젝트의 것(8,324 B)과 같은 경로였다. 지난 세션이 V키를 넣으며 7,787 → 8,324로 키운 바로 그 파일이다. 실제로는 덮이지 않았지만, **베이스라인을 먼저 확보하고 들어간 덕에 안 덮였다는 사실을 증명할 수 있었다.**

**`CopyPoseFromMesh`가 포즈 수준 복사라는 걸 확인하고 나서 테스트를 설계한 것.** `ABP_FP_Copy`의 AnimGraph는 `CopyPoseFromMesh → ControlRig → Root` 세 노드뿐이고 `SourceMeshComponent` 핀은 연결이 없다. 복사가 포즈 수준이므로 소스 메시를 무엇으로 애니메이션하든 흘러간다. **그래서 `Mesh`의 애님만 잠깐 갈아끼우는 테스트가 사슬을 안 깨뜨린다고 판단할 수 있었다.** 확인 안 하고 했으면 근거 없는 시도였다.

**무기 시스템을 만들지 않고 애님 한 줄로 답을 낸 것.** "무기를 들어봐야 알겠다"는 말에 무기 장착을 만들 수도 있었지만, 진짜 질문은 "팔이 시야에 들어왔을 때 어떻게 보이는가"였다. 조준 포즈 애님 하나로 답이 나왔고, 무기 메시 부착에 또 필요했을 소켓 수작업을 아꼈다. 답이 "전용 애님이 필요하다"로 나왔으니 **무기를 붙였어도 어차피 다시 했을 작업이다.**

**Epic 원본과 대조해 결함이 아님을 가른 것.** 팔이 화면 하단에만 보이는 걸 두고 우리 포팅 문제인지 리그의 원래 동작인지 갈렸다. 우리 BP를 건드려 실험하는 대신 팩과 함께 들어온 `Lvl_FirstPerson`을 그냥 플레이해봤다. **편집 0회로 판별됐고**, Epic 원본도 같은 그림이라 우리 포팅이 정확하다는 게 확정됐다.

### 확인한 것 / 확인 못 한 것

**확인한 것** — PIE에서 합격 기준 4개 전부. ① V로 1인칭 전환 시 팔이 보인다 ② 이동 시 팔이 애니메이션한다 ③ V로 3인칭 복귀 시 팔이 사라지고 몸이 보인다 ④ 3인칭 이동·점프가 기존과 같다. 눈높이가 선 사람 높이로 나오는 것도 화면으로 확인했다. `Lvl_FirstPerson`에서 Epic 원본 캐릭터가 같은 동작을 하는 것도 화면으로 확인했다. `FirstPersonCamera`의 부모 소켓이 `head`라는 것은 사용자가 디테일 패널에서 읽어 알려줬다. 컴포넌트 속성과 그래프 구조는 MCP로 읽어 대조했다.

**확인 못 한 것** — 부모 소켓 값을 **내가** 읽은 적은 없다. MCP가 `AttachSocketName`을 읽지도 쓰지도 못한다. 사용자 보고와 눈높이 정상이라는 간접 증거로 확정했다. `CtrlRig_FPWarp`가 Quinn 프로포션에서 Manny와 동등하게 도는지는 확인 못 했다 — 두 메시가 `SK_Mannequin` 스켈레톤을 공유한다는 것까지만 확인했고 리그 내부 동작을 비교하지 않았다. `bPropagateToChildren = true`였을 때 카메라가 실제로 꺼지는지도 확인 안 했다. 확인할 이유가 없어서 기본값을 유지했을 뿐이다. `MF_Rifle_Idle_ADS` 테스트 중 나온 `Invalid animation skeleton` 경고가 정말 무해한지는 **증명하지 못했다** — 두 스켈레톤이 같다는 것과 경고가 모드 전환 전에 찍혔다는 정황뿐이다.

### 남는 리스크

- **팔이 화면 하단에만 보인다.** 결함이 아니라 이 구성의 정상 결과다. Epic 원본도 같다. 손을 시야로 올리려면 `Variant_Shooter`의 `ABP_FP_Weapon`·`Ctrl_HandAdjusment`가 필요한데 그 팩은 이 프로젝트에 없다. **현재 상태로는 1인칭이 "팔이 거의 안 보이는 1인칭"이다.**
- **MCP로 부착 소켓을 다룰 수 없다.** 이번엔 카메라 하나라 손으로 처리했지만, 무기를 `HandGrip_R`에 붙이는 순간 같은 벽에 다시 부딪힌다. BP 컴포넌트를 소켓에 붙이는 작업은 앞으로도 수작업이 섞인다.
- **`Compile returned null`이 성공을 실패처럼 보고한다.** 이번엔 실제 상태를 다시 읽어 거짓 음성임을 확인했지만, 응답만 믿으면 되돌리지 않아도 될 것을 되돌리게 된다.
- **`AnimationData` 세터의 부작용이 비대칭이다.** 애님을 꽂으면 `AnimationMode`가 `AnimationSingleNode`로 자동 전환되지만, `None`으로 지워도 `AnimationBlueprint`로 안 돌아온다. 되돌릴 때 모드를 따로 써야 한다. 모르고 지나가면 AnimBP가 죽은 채 남는다.
- **`save_assets`가 경로 형식을 일관되게 안 받는다.** 패키지 경로 `/Game/.../BP_ThirdPersonCharacter`가 한 번은 성공했고 나중엔 `Asset does not exist`가 났다. 오브젝트 경로 `....BP_ThirdPersonCharacter`로는 됐다.
- **UE Terminal이 한글을 못 그린다.** 폰트 후보(`CascadiaMono` → `CascadiaCode` → `consola` → `cour`, 기호 `seguisym`, 이모지 `seguiemj`)에 CJK가 하나도 없다. 이번엔 터미널 에이전트에게 영어로만 쓰라고 지시해 넘겼지만 **세션마다 다시 넣어야 한다.**
- **`Content/Weapons/` 27개가 안 쓰인 채 들어와 있다.** 무기 작업을 안 하면 그냥 짐이다.
- **`Lvl_FirstPerson`과 BP 4개도 안 쓴다.** `ABP_FP_Copy`와 `CtrlRig_FPWarp`만 실제로 참조된다. 참조 구현으로 남겨두는 값은 있지만 정리 대상이기는 하다.
- **`bIsFirstPerson`과 실제 상태가 어긋날 여지는 그대로다.** 지난 세션에서 지적된 것이고 이번에 손대지 않았다. 리스폰·언포제스 시 `FirstPersonMesh`의 `bVisible`도 같이 어긋난다.

### 총평

요청은 "1인칭 팔 메시를 쓸 계획인데 그럼 제안은?"이었고, 결과적으로 **팔이 보이는 1인칭까지 갔지만 쓸 만한 1인칭까지는 못 갔다.** 합격 기준 4개는 전부 통과했으므로 사양은 충족했다. 다만 사양을 세울 때 "팔이 보인다"를 기준으로 잡은 것 자체가 느슨했다 — `ABP_Unarmed` 기본 포즈에서는 팔이 몸 옆에 있어 판정이 거의 불가능하다는 걸 기준을 쓸 때 몰랐다.

이 작업의 실질적 난이도는 노드 조작이 아니라 **추측을 사실로 바꾸는 데 있었다.** 팔 메시가 템플릿에 있다는 내 첫 설명이 틀렸고(없었다), 메뉴 경로가 틀렸고(Tools에 없었다), 사용자 승인까지 받은 부착 구조가 틀렸다(반대였다). 세 번 다 엔진 소스나 참조 애셋을 읽어서 바로잡았다. 반대로 덮어쓰기 경고는 실제로는 일어나지 않아 **내 예측이 과했던 쪽**이었다.

## AI의 제안

> 1. Editor Preferences → General → Terminal → `StartupCommands`에 `set CLAUDE_UE_TERMINAL=1` 한 줄 추가 (기존 3줄 앞에)
> 2. CLAUDE.md에 "`CLAUDE_UE_TERMINAL`이 설정돼 있으면 모든 출력을 영어로 쓴다 — 그 터미널 폰트에 한글 글리프가 없다" 규칙 추가

터미널 한글 깨짐을 세션마다 수동 지시로 막는 대신 영구화하는 안이다. 얻는 것은 매번 문구를 붙여 넣는 수고가 사라지는 것이고, 잃는 것은 환경변수라는 우회 장치가 하나 늘어 CLAUDE.md 규칙이 조건부로 복잡해지는 것이다. 이 세션은 한글로 대화 중이라 조건 없이 "영어로 써라"를 넣으면 이쪽까지 걸리기 때문에 표시가 필요했다.

## 다음으로 넘김

없음. 이 항목들은 같은 날 후속 작업으로 이어져 2026-08-28-inventory-hud.md의 `다음으로 넘김`에 모았다.
