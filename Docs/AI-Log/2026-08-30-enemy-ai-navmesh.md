# 2026-08-30

## 작업물

카메라 작업의 크기를 조사해 미루기로 정하고, **적 AI 1단계 사양을 확정한 뒤 첫 관문인 `NavMeshBoundsVolume`을 놓았다** — 명령 42, 커밋 2개.

**소요 시간**: 약 1시간 10분. 근거는 파일 mtime이다 — 직전 커밋 `3bbfae3`이 `21:34:22`, 명령 42의 Terminal-Log가 `22:18:27`, 사용자의 `Ctrl+S`가 `22:28:51`. 그중 실제 명령은 하나뿐이고 나머지는 조사·심문·사양 작성이다.

## 명령

### 한글

```
카메라 많은 작업을 요구해?
```

```
적 AI먼저 하는데 이 세션에서 작업해도 되는지 여부만 확인하고 할까그럼
```

```
나 하자
```

**심문의 답 넷.** 아래는 타이핑한 문장이 아니라 AI가 제시한 항목별 안에서 사용자가 고른 것이다. 넷 다 AI가 권장으로 표시한 안을 골랐다.

- AI 구동 → **블루프린트 로직만으로** (StateTree / BehaviorTree 중 택1)
- 적 폰 → **`Character` 상속으로 새로** (`BP_ShooterNPC`를 복제해 고친다 중 택1)
- 범위 → **인지 + 추격 + 공격까지** (추격까지만 / 적 사망까지 전부 중 택1)
- 공격 연출 → **몽타주를 손으로 하나 만든다** (연출 없이 데미지만 중 택1)

네 번째는 심문을 한 번에 몰아서 내는 규칙을 어긴 것이다. 사양을 쓰는 도중에 `MM_Attack_01`이 `AnimSequence`라는 것이 드러나 뒤늦게 물었다.

```
결과확인
```

```
저장한거 확인좀
```

```
커밋하자 하고 정리하고 다음 세션 준비까지 해놓고 내일하자
```

### English — MCP에 실제로 보낸 명령

**옮기며 AI가 넣은 해석.** 한글 지시는 "나 하자"(= 사양 + 명령 1개까지) 한 줄이었다. 그 한 줄이 사양 문서 하나와 아래 영어 명령 하나가 됐다.

- **목표 상자의 여섯 숫자 전부** — `min (-2100,-2100,-200)` `max (2100,2100,600)`. `Floor`의 `±2000`에 100을 더하고, Z는 바닥 아래 −200부터 벽 위 600까지 덮게 잡은 것이다
- **볼륨 이름 `NavBounds_Main`**, 아웃라이너 폴더 `Navigation`
- **"측정한 뒤 스케일을 계산하라"는 절차 자체.** 기본 브러시 크기를 몰라서 넣은 것이고, 사용자가 요구한 것이 아니다
- **`sizeX`가 0이면 STOP** — 브러시 없는 볼륨은 우회할 것이 아니라 관찰이라는 판단
- **저장을 아예 시도하지 말라는 지시** — 명령 40에서 확인된 것을 반복하지 않기 위해서다
- **모든 사전 검사와 보고 항목**

#### 명령 42

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, place one
NavMeshBoundsVolume covering the whole playable area. This is a LEVEL change only -
do NOT edit any Blueprint. Do NOT call AssetTools.is_dirty.

TARGET: after scaling, the volume's world bounds must be about
    min (-2100, -2100, -200)   max (2100, 2100, 600)
i.e. a 4200 x 4200 x 800 box centred at (0, 0, 200).

WHY those numbers: the Floor spans X/Y -2000..2000 with its top at Z=0, the
PlayerStart platform sits at Z=200, and the door test walls reach Z=220. The box
is padded 100 past the floor edge on X/Y and runs from Z -200 to Z 600 so it
covers under the floor and over the walls.

PRE-FLIGHT. Report every result. STOP if any fails:
 P1. SceneTools.get_current_level returns /Game/ThirdPerson/Lvl_ThirdPerson.
 P2. SceneTools.find_actors with name "Nav", empty tag, empty collision_channels.
     Report EVERY refPath. Expect exactly one: AbstractNavData-Default.
     This is the BEFORE picture - you will run it again at the end.
 P3. ObjectTools.search_subclasses with base_class /Script/Engine.Actor and
     class_name "NavMeshBoundsVolume". Report every refPath returned. Use the
     exact class refPath that comes back for the placement below. STOP if the
     list is empty - do not guess a class path.
 P4. ActorTools.get_actor_bounds on
     /Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.Floor_UAID_F4A475FF15A3736A02_1961940706
     Report the exact numbers. Expect about min (-2000,-2000,-50) max (2000,2000,0).

PLACE, then measure, then scale. Do NOT guess the default brush size.
 1. SceneTools.add_to_scene_from_class
      actor_type   the class refPath from P3
      name         "NavBounds_Main"
      xform        location (0, 0, 200), rotation (0,0,0), scale (1,1,1)
      parent unset, snap_to_ground FALSE
    Report the returned refPath. STOP if it is null or nothing.

 2. ActorTools.get_actor_bounds on the new actor. Report it verbatim.
    This is the volume's size at scale 1. Compute from it:
        sizeX = max.x - min.x     sizeY = max.y - min.y     sizeZ = max.z - min.z
    Report those three numbers. STOP if any is 0 - a volume with no brush cannot
    be scaled into one, and that is a finding, not something to work around.

 3. Compute the scale that turns that box into the target:
        scaleX = 4200 / sizeX     scaleY = 4200 / sizeY     scaleZ = 800 / sizeZ
    Report the arithmetic - the three measured sizes and the three results.

 4. ActorTools.set_actor_transform on the new actor with
        location (0, 0, 200), rotation (0,0,0), scale (scaleX, scaleY, scaleZ)
        worldspace true
    Report the boolean it returns.

 5. ActorTools.set_label to exactly "NavBounds_Main".
    SceneTools.set_actor_folder with folder_path "Navigation".
    Confirm the folder with SceneTools.get_actors_in_folder("Navigation", false)
    and report it - set_actor_folder returns null and that is not evidence.

VERIFY. Report expected beside measured with PASS/FAIL on each:
 V1. get_actor_transform on NavBounds_Main. Verbatim.
 V2. get_actor_bounds on NavBounds_Main. Expect about
     min (-2100,-2100,-200) max (2100,2100,600). Anything within 5 units passes.
 V3. SceneTools.find_actors with name "Nav" again. Report EVERY refPath.
     Compare against P2. A RecastNavMesh actor appearing here means the editor
     built navigation data on its own. Say plainly whether one appeared or not -
     both outcomes are informative and NEITHER is a failure of this command.
 V4. SceneTools.get_folders. Report the list. Expect DoorTest, Lighting,
     Navigation, Playground.
 V5. Confirm nothing else moved: get_actor_transform on
     PlayerStart_UAID_F4A475FF15A3736A02_1961960731 must still read
     location (0, 0, 302.012643), and get_actors_in_folder("DoorTest", false)
     must still return exactly three actors.

DO NOT SAVE. Command 40 established that SceneTools.save_actor cannot save a
newly placed actor - it errors with "Asset does not exist" because the external
actor package does not exist yet - and that AssetTools.save_assets returns true
while writing nothing. Do not call either one. Do not look for a third way.
Say in the report that the volume is unsaved and that the user must press Ctrl+S
(Save Current Level) in the level editor.

Do NOT touch any existing actor. In particular do NOT move Wall_L, Wall_R,
Door_Test, any BP_ItemPickup, SM_Ramp11, or the PlayerStart.

Write the report to Docs/Terminal-Log/2026-08-30-42-navmesh-bounds.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight result, including the full refPath list from P2 and P3 and the
  exact Floor bounds from P4
- the refPath of the placed actor
- the measured scale-1 bounds, the three computed scale factors with their
  arithmetic shown, and the boolean from set_actor_transform
- V1 through V5 verbatim, expected beside measured, PASS/FAIL each
- an explicit statement of whether a RecastNavMesh actor appeared in V3
- an explicit statement that nothing was saved and why
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

## Terminal 결과

### 원문 — English

**발췌했다.** 보고서는 약 15,000자다. 아래는 판단 근거가 된 줄만 뽑았다. 다만 **AI가 잘못 정정한 대목은 발췌하지 않고 전문을 붙였다** — 그것이 이번 보고서에서 가장 중요한 어긋남이다.

#### 클래스 경로 탐색

```json
{"returnValue":[{"refPath":"/Script/NavigationSystem.NavMeshBoundsVolume"}]}
```

#### 스케일 1에서 잰 기본 브러시

```json
{"returnValue":{"min":{"x":-100,"y":-100,"z":100},"max":{"x":100,"y":100,"z":300},"isValid":true}}
```

```
The default brush is a clean 200 x 200 x 200 cube with no float tail at all, already centred
on the actor location (0, 0, 200) - the Z span 100..300 is that cube centred on Z = 200.

The measurement was taken rather than assumed, as instructed. Had the default been guessed at
the common 200-cube value it would have happened to be right, but that would not have been
evidence.
```

#### 스케일 적용 후 바운드

```json
{"returnValue":{"min":{"x":-2100,"y":-2100,"z":-200},"max":{"x":2100,"y":2100,"z":600},"isValid":true}}
```

```
V2 PASS. Not merely within the 5-unit tolerance - exact on all six faces, with isValid: true.
```

#### `RecastNavMesh`가 저절로 생긴 것

```
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.AbstractNavData-Default
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.NavMeshBoundsVolume_UAID_9C6B005AF86909FD02_1188892250
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default
```

```
Yes. A RecastNavMesh actor appeared. [...] it was not created by any call in this command.

P2 established that no RecastNavMesh existed before. The only actor this command created is
the NavMeshBoundsVolume. So the editor spawned the RecastNavMesh itself in response to a
nav bounds volume existing in the level - that is the navigation system building its data.
```

#### 잘못된 정정 — 전문

```
One correction to the premise, recorded because it affects how much the user should trust the
"returns true while writing nothing" half of it. Command 40's report concluded that
save_assets wrote nothing. That conclusion was wrong. The three external actor packages
named in command 40's error messages
(.../C/EB/M2R2969V25QR9HAZAO0DTH.uasset, .../C/8Q/388B6MQM912EX2BXH5U4GD.uasset,
.../5/D1/KK3E4BC1U33OGW1QTQUUOL.uasset) are present on disk, timestamped 20:53:17, which is
when that save_assets call ran. The disk check performed immediately after that call
reported them absent; the timestamp says otherwise. Why the check and the timestamp disagree
is not known and is not guessed at here.

The save_actor half of the premise stands unchallenged - those three errors are quoted
verbatim in command 40's report and were real. And not saving here is harmless either way, so
the instruction was followed without argument.
```

#### `RecastNavMesh`의 프로퍼티 — 명령 42의 지시에 없던 것을 AI가 따로 읽은 것

```json
{"RuntimeGeneration":"Static","AgentRadius":35,"AgentHeight":144,"AgentMaxSlope":44,"TileSizeUU":1000}
```

#### 잡지 못한 것

```
The editor's own Message Log and Output Log were not read as part of this command, so a
navigation-build warning that appeared only there - for instance about the RecastNavMesh
generation - would not have been captured here.
```

### 요약 — 한글

**명령 42** — 레벨 액터 하나 신규. `NavBounds_Main`(`/Script/NavigationSystem.NavMeshBoundsVolume`), 위치 `(0, 0, 200)`, 회전 `(0,0,0)`, 스케일 `(21, 21, 4)`, 아웃라이너 폴더 `Navigation`. 월드 바운드가 `min (-2100,-2100,-200)` `max (2100,2100,600)`로 여섯 면 모두 목표값과 정확히 일치했다.

**그리고 액터가 하나 더 늘었다** — `RecastNavMesh_UAID_9C6B005AF86909FD02-Default`. 명령이 만든 것이 아니라 에디터의 네비게이션 시스템이 볼륨을 보고 스스로 만든 것이다. 사전 검사 `P2`가 "지금은 `AbstractNavData-Default` 하나뿐"을 기록해뒀기 때문에 이 비교가 읽힌다.

**저장은 명령이 시도하지 않았다.** 사용자가 `Ctrl+S`를 눌러 `22:28:51`에 저장했고, `__ExternalActors__/ThirdPerson/Lvl_ThirdPerson`이 74개 → 76개가 됐다. 볼륨과 `RecastNavMesh` 둘 다 액터라 같이 저장됐다. `__ExternalObjects__`에 하나 더 생겼는데 새 폴더 `Navigation`의 것으로 보이나 확인 못 했다.

## 분석

### 무엇을 만들었나

**사양 문서 — `Docs/Spec/2026-08-30-적-AI-1단계.md`**

이번 세션의 산출물 중 가장 큰 것이다. 정한 것들:

| 항목 | 내용 |
|---|---|
| 범위 | 인지 + 추격 + 공격까지. 적 HP·피격·사망과 플레이어 사망은 안 만든다 |
| 상태 | **`BP_Enemy`는 상태 변수를 갖지 않는다.** 저장하는 것은 `PlayerRef` 캐시 하나뿐 |
| AI 구동 | 블루프린트 로직만. StateTree·BehaviorTree·Blackboard 안 씀 |
| AI 컨트롤러 | **BP를 안 만든다.** 엔진 기본 `AIController`를 쓰고 `AI MoveTo`는 폰이 부른다 |
| 루프 | `Tick`도 `Timer`도 안 씀. `Think`가 자기를 다시 부르고, 돌아가는 네 경로 전부 앞에 지연이 있다 |
| 인지 | 거리 하나로만. 시야각·라인 오브 사이트 없음 |
| 공격 | 몽타주 + `Apply Damage`. 무기 콜리전·AnimNotify 없음 |
| 체력 | **한 벌.** `CurrentHP`만 깎고 HUD가 그것을 읽는다 |

튜닝 값 일곱 개 전부 인스턴스 편집 변수다 — `SightRange 1200` · `AttackRange 150` · `AttackDamage 10.0` · `AttackCooldown 1.5` · `ThinkInterval 0.3` · `AttackMontage` · `PlayerRef`(런타임).

합격 기준 넷과 명령 계획 42~48을 적었다.

**레벨 액터 — `Lvl_ThirdPerson`** (명령 42, 커밋 `2cd1ced`)

| 액터 | 클래스 | 위치 | 회전 | 스케일 | 결과 월드 바운드 |
|---|---|---|---|---|---|
| `NavBounds_Main` | `/Script/NavigationSystem.NavMeshBoundsVolume` | `(0, 0, 200)` | `(0,0,0)` | `(21, 21, 4)` | `min (-2100,-2100,-200)` `max (2100,2100,600)` |

아웃라이너 폴더 `Navigation`(신규). 디스크에 생긴 파일 4개:

```
Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/D/4G/L3E6D4QT6PYA5U1VLMF7ZD.uasset   신규
Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/4/OC/R1TLJFGAENLS2HJLJILODF.uasset   신규
Content/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/4/N4/1UVYQEVSONIYWETDLYKSAD.uasset  신규
Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/5/D1/KK3E4BC1U33OGW1QTQUUOL.uasset   Door_Test가 다시 쓰임
```

두 신규 액터 패키지 중 어느 것이 볼륨이고 어느 것이 `RecastNavMesh`인지는 **구분 못 했다** — `get_asset_class`가 외부 패키지에 `Asset does not exist`를 낸다. 개수(74 → 76)와 늘어난 액터 수(2)가 맞는 것까지만 확인했다.

`Door_Test`의 패키지가 같은 저장에서 다시 쓰였는데 `git status`에 안 뜬다. 바이트가 동일하다는 뜻이다.

**조사 산출물 — 카메라 작업의 크기**

애셋을 만들지 않았지만 이번 세션의 결과물이다. `06-플레이어-UI.md`와 `07-재설계-우선순위.md`가 권한 "원본 ICI 구조(`캡슐 → Camera → SkeletalMesh`)로 바꾼다"가 **지금 그대로는 불가능하다**는 것을 확인했다. 팔만 있는 스켈레탈 메시가 프로젝트에 하나도 없다(`SKM_Manny_Simple`·`SKM_Quinn_Simple`은 전신이고 나머지는 무기다). 전신 메시를 카메라 자식으로 달면 시선을 내릴 때 몸 전체가 기운다.

그리고 2026-08-28 기록이 "`ABP_FP_Weapon`·`Ctrl_HandAdjusment`가 필요한데 그 팩은 이 프로젝트에 없다"고 적어둔 것이 **지금은 틀렸다는 것**을 찾았다. 같은 날 오후 `Variant_Shooter`를 임포트하면서 들어왔다.

### 기술적으로 맞게 짚은 부분

**명령을 쓰기 전에 "이미 있는가"를 먼저 봤다.** `Variant_Shooter`에 `BP_ShooterNPC` · `BP_ShooterAIController` · `BP_ShooterNPCSpawner` · `ST_Shooter` · StateTree 태스크 6개 · EQS 3개가 통째로 있다. 결정 사다리 2번이다. 그런데 `get_parent`로 읽어보니 **`BP_ShooterNPC`의 부모가 `BP_FirstPersonCharacter`**라 근접 적에게 필요 없는 `FirstPersonMesh`와 `CameraComponent`를 상속으로 달고 오고, `list_variables`가 준 12개가 전부 총 전용이었다(`Weapon` · `Aim Range` · `Aim Variance Half Angle` · `Is Shooting` · `Team Byte` …). **문 작업에서 `BP_DoorFrame`을 읽고 "있지만 안 맞는다"로 판단한 것과 같은 자리를 지났다.**

**AI 컨트롤러 블루프린트를 안 만들기로 한 것.** `AI MoveTo` 노드의 첫 핀이 `Pawn`이라 폰이 자기를 넘겨 부를 수 있다. 컨트롤러 BP를 하나 만들고 거기에 그래프를 넣는 것이 "정석"처럼 보이지만, 지금 컨트롤러가 할 일이 없다. 사다리 1번 — 안 만들어도 된다.

**`Tick`도 `Timer`도 안 쓰기로 한 것.** CLAUDE.md가 `Event Tick`에서 무거운 일을 금지하고 "기본은 Tick을 꺼둔다"고 못 박았다. 타이머는 `EndPlay`에서 지워야 하는 것이 하나 늘어난다. 행동 루프가 자기를 다시 부르는 구조는 그 둘을 다 피하면서, **모든 가지 앞에 지연이 있는지만 확인하면 폭주하지 않는다.** `AI MoveTo`의 `On Fail`이 즉시 나올 때를 위해 그쪽에도 `Delay`를 넣은 것이 그 확인의 결과다.

**상태 변수를 안 두기로 한 것.** "지금 쫓는 중인가", "지금 공격 중인가" 플래그를 두면 그 플래그와 실제 행동이 어긋날 경로가 생긴다. 이 프로젝트에 이미 `bIsFirstPerson`이 그 문제로 남아 있고, 원본 ICI는 `Is Attack` / `Is Attacking` 두 키가 같은 것을 가리키는 척하다 애님이 공격 상태를 영영 못 읽었을 가능성까지 갔다. **거리는 매번 다시 잴 수 있다.**

**기본 브러시 크기를 추측하지 않게 한 것.** 스케일 1로 놓고 재서 계산하게 했다. 결과가 200이라 추측했어도 맞았겠지만, 터미널이 스스로 적었듯 *"that would not have been evidence"*다. 그리고 `sizeX`가 0이면 우회하지 말고 STOP하게 한 것 — 브러시 없는 볼륨은 회피할 문제가 아니라 관찰이다.

**클래스 경로도 `search_subclasses`로 찾게 한 것.** `/Script/NavigationSystem.NavMeshBoundsVolume`을 기억에서 적어 넣을 수도 있었지만, 이 프로젝트에서 기억으로 단정했다가 틀린 적이 여러 번이다(명령 34의 type_id, 명령 38의 노드 ref).

**`P2`를 "BEFORE 사진"으로 명시한 것.** 이게 없었으면 `RecastNavMesh`가 원래 있었는지 새로 생겼는지 구분이 안 됐다. 사전 검사가 검증의 절반이었다.

**저장을 아예 시도하지 말라고 한 것.** 명령 40에서 확인된 실패를 반복할 이유가 없다. CLAUDE.md의 "고쳐보고 돌려보는 것을 반복하지 않는다"와 같은 자리다.

**터미널의 정정을 액면 그대로 받지 않은 것.** 보고서가 명령 40의 결론이 틀렸다고 적었는데, 파일 mtime(`20:53:17`)과 명령 40 보고서의 작성 시각(`20:50:26`)을 대조하니 시각이 안 맞았다. 그 사이에 `git status`로 파일이 없는 것을 확인했고 그 뒤 사용자가 `Ctrl+S`를 눌렀다. **명령 42의 터미널은 `Ctrl+S`가 있었다는 것을 몰랐다** — 부분 정보로는 합리적인 추론이었지만 결론이 틀렸다.

**지시에 없던 것을 하나 더 읽은 것.** `RecastNavMesh`의 프로퍼티를 읽어 `RuntimeGeneration: Static`을 확인했고, 그것이 사양에 "확인 못 함"으로 열어둔 리스크의 답이었다. 볼륨을 놓은 그 순간에만 읽을 수 있는 값이었다.

### 확인한 것 / 확인 못 한 것

**확인한 것** — 에디터에서 실제로 읽은 것.

- **`NavBounds_Main`의 월드 바운드가 `min (-2100,-2100,-200)` `max (2100,2100,600)`이다.** 오차 허용 5를 줬는데 여섯 면 편차가 전부 0이다. 직접 다시 읽어 확인했다
- **`RecastNavMesh` 액터가 존재한다.** `find_actors("Nav")`가 셋을 준다. 명령 전에는 하나였다
- **`RuntimeGeneration`이 `Static`이다.** `AgentRadius 35` · `AgentHeight 144` · `AgentMaxSlope 44` · `TileSizeUU 1000`도 같이 읽었다
- **디스크에 저장됐다.** `22:28:51`에 파일 4개, 외부 액터 74개 → 76개
- **아웃라이너 폴더가 넷이다** — `DoorTest` · `Lighting` · `Navigation` · `Playground`
- **기존 액터가 안 움직였다.** `PlayerStart`가 `(0,0,302.012643)` 그대로고 `DoorTest` 폴더에 셋 그대로다
- **명령 42 보고서의 정정이 틀렸다.** 파일 mtime과 보고서 작성 시각의 대조로 확정했다
- **카메라 작업 — `BP_ThirdPersonCharacter`의 실제 컴포넌트 트리.** `CharacterMesh0` → `FirstPersonMesh`(`SKM_Quinn_Simple`, `bOnlyOwnerSee`, AnimBP `ABP_FP_Copy`) → `FirstPersonCamera`(회전 `(0, 90, -90)` = 본 좌표 보정)
- **`ABP_Unarmed`의 AnimGraph에 `AnimGraphNode_Slot_0`이 있고 `slotName`이 `DefaultSlot`이다**
- **`MM_Attack_01`~`03`과 `MM_ChargedAttack`은 `AnimSequence`다.** `get_referencers`가 `[]` — 아무도 안 쓴다
- **플레이어에게 데미지 경로가 없다.** `ReceiveAnyDamage` · `ReceivePointDamage` · `ReceiveRadialDamage`가 전부 `bIsImplemented: false`

**확인 못 한 것** — 이유까지.

- **NavMesh가 실제로 생성됐는지 안 봤다.** `RecastNavMesh` 액터가 있다는 것과 네비 메시가 바닥을 덮었다는 것은 다르다. **PIE를 한 번도 안 돌렸고, 뷰포트의 네비 오버레이(`P` 키)도 안 봤다.** 명령 45에서 처음 보게 된다
- **두 신규 외부 액터 패키지 중 어느 것이 볼륨이고 어느 것이 `RecastNavMesh`인지 모른다.** `get_asset_class`가 외부 패키지를 못 읽는다. 개수만 맞췄다
- **`__ExternalObjects__`에 생긴 파일의 정체.** `Navigation` 폴더의 `UActorFolder`로 **추정**한 채 커밋했다. 명령 40의 `DoorTest` 때와 같고 같은 이유로 못 읽는다
- **네비게이션 빌드 경고.** 에디터의 Message Log와 Output Log를 안 읽었다
- **문틀 100cm를 NavMesh가 통과하는지.** `AgentRadius 35`를 침식하면 걸을 폭이 30cm쯤 남는다. 계산이지 관측이 아니다
- **`AI MoveTo`가 폰을 받는다는 전제.** 사양 전체가 이 위에 서 있는데 엔진 소스나 문서로 확인하지 않았다. 노드의 첫 핀 이름이 `Pawn`이라는 것에서 판단했다. **명령 44가 이것을 먼저 봐야 한다**
- **`Variant_Shooter`의 StateTree AI가 실제로 어떻게 도는지.** 애셋 목록과 `BP_ShooterNPC`의 부모·변수만 읽었고 `ST_Shooter`의 내용은 안 봤다. 안 쓰기로 정했으므로 더 안 팠다
- **카메라의 B안(`ABP_FP_Weapon` + `Ctrl_HandAdjusment`)이 맨손·칼에 맞는지.** 이름이 무기용이라 열어봐야 안다

### 남는 리스크

- **`AI MoveTo`가 폰을 받는다는 전제가 미확인이다.** 틀리면 사양의 "AI 컨트롤러 BP를 안 만든다"가 무너지고 명령 계획이 바뀐다. 사양이 이것을 "가장 위험한 것" 둘째로 적어뒀다
- **NavMesh가 생성됐다는 증거가 액터의 존재뿐이다.** 볼륨이 있고 `RecastNavMesh`가 있다고 해서 타일이 실제로 구워졌다는 뜻은 아니다
- **`RuntimeGeneration`이 `Static`이라 닫힌 문이 적을 못 막는다.** 이번 범위에서는 문제가 아니지만 진행 구조 단계에서 문이 길을 막아야 할 때 다시 온다
- **`AgentHeight 144`가 캐릭터 키 180보다 낮다.** 지금 천장이 없어 안 드러난다
- **심문을 두 번 나눠 했다.** 사양을 쓰는 도중 `MM_Attack_01`이 `AnimSequence`라는 것이 드러나 네 번째 질문이 뒤늦게 나갔다. CLAUDE.md는 한 번에 몰아서 묻게 한다. **조사가 덜 된 채 심문에 들어간 것**이 원인이다
- **몽타주 생성이 네 번째 손 작업 지점이 된다.** 인터페이스 부착, 레벨 저장에 이어 셋째 종류다. 명령 47이 여기 걸린다
- **`Content/Enemy/` 폴더가 아직 없다.** 명령 43이 만든다
- **적을 놓을 자리를 아직 안 정했다.** 사양이 "손으로 배치한다"까지만 적었다. 명령 45에서 정해야 하고, 문 반대편이면 안 된다

### 총평

**요청은 "카메라 많은 작업을 요구해?"로 시작해 "나 하자"로 끝났고, 명령은 하나만 나갔다.** 산출물의 대부분이 사양 문서다.

이 작업의 실질적 난이도는 `NavMeshBoundsVolume`을 놓는 것이 아니었다 — 그건 명령 하나로 끝났고 편차 0으로 통과했다. **어려웠던 것은 두 번, "이미 있는 것"을 안 쓰기로 정한 자리다.**

첫 번째는 카메라다. 문서 셋(`06` · `07` · `screenshots/README`)이 모두 "원본 ICI 구조로 바꿔라"라고 적어뒀고 그게 이월 목록의 첫 줄이었는데, 조사해보니 **팔만 있는 메시가 없어서 그 구조를 만들 수 없었다.** UE 5.5부터 FirstPerson 템플릿이 전신 메시 + `head` 본 카메라로 바뀌었고 지금 구조가 그것이다. **머리에 붙은 것이 실수가 아니라 그 설계의 전제였다.** 문서가 권한 것을 그대로 했으면 몸이 시선을 따라 기우는 것을 만들고 있었을 것이다.

두 번째는 `Variant_Shooter`의 AI다. 완성된 StateTree 스택이 통째로 있는데 `BP_ShooterNPC`의 부모가 `BP_FirstPersonCharacter`였다. 문 작업의 `BP_DoorFrame`과 정확히 같은 모양이다 — **있지만 안 맞는다.** 사다리 2번은 "있으면 그걸 쓴다"인데, 읽어보고 안 쓰기로 정하는 것까지가 그 칸의 일이다.

그리고 세 번째로, 터미널이 명령 40을 정정하려 한 것을 받지 않았다. 시각 대조 하나로 갈렸다. **다른 에이전트의 보고를 액면 그대로 받으면 맞는 결론이 틀린 것으로 뒤집힌다.**

## AI의 제안

> **사용자가 시키지 않았는데 AI가 먼저 꺼낸 것.**

1. **적 AI를 먼저 하고 카메라는 칼 직전에 하자는 것**

   > `ABP_FP_Copy`가 3인칭 포즈를 복사하고 `HeldItemMesh`가 캡슐 직속이라, **적 AI 작업은 카메라 구조와 안 겹친다.** 지금 안 해도 막히지 않는다.

   얻는 것 — 애셋 제작이 필요한 작업(팔 메시)을 뒤로 민다. 잃는 것 — 이월 목록의 첫 줄이 또 하루 밀린다.

2. **오늘의 목표를 세 안으로 쪼개 제시한 것**

   > **나를 권한다.** NavMesh는 되돌리기 쉽고, 그게 있어야 적 폰을 만들자마자 PIE에서 볼 수 있다. 사양을 쓰는 동안 NavMesh가 빌드될 시간도 번다.

   얻는 것 — "적 AI 하자"가 오늘 안에 안 끝난다는 것을 시작 전에 못 박는다. 잃는 것 — 질문이 하나 더 든다.

3. **AI 컨트롤러 블루프린트를 안 만들자는 것**

   > `AI MoveTo` 노드는 **컨트롤러가 아니라 폰을 받는다.** 그래서 적 폰이 자기 그래프에서 자기를 넘겨 부르면 된다. **결정 사다리 1번 — 안 만들어도 된다**

   얻는 것 — 블루프린트 하나와 그 사이의 캐스팅이 사라진다. 잃는 것 — 전제가 틀리면 사양의 명령 계획이 바뀐다. 미확인이다.

4. **`Tick`도 `Timer`도 안 쓰고 루프가 자기를 부르게 하자는 것**

   > 모든 가지가 끝에서 `Think`로 돌아온다. **모든 가지에 지연이 있다** — `AI MoveTo`는 라텐트고 나머지는 `Delay`다. 지연 없이 `Think`로 돌아오는 경로가 하나도 없어야 한다

   얻는 것 — Tick 금지 규칙을 지키면서 `EndPlay`에서 정리할 타이머도 없앤다. 잃는 것 — 지연 없는 경로가 하나라도 생기면 프레임 안에서 무한 루프가 된다. 사양이 그것을 규칙으로 적었지만 강제하는 장치는 없다.

5. **상태 변수를 아예 두지 말자는 것**

   > 상태 플래그를 두면 **그 플래그와 실제 행동이 어긋날 수 있는 경로**가 생긴다. … **거리는 매번 다시 잴 수 있다. 재면 되는 것을 저장하지 않는다.**

   얻는 것 — `bIsFirstPerson`과 원본의 `Is Attack`/`Is Attacking`이 겪은 종류의 버그가 원천적으로 없다. 잃는 것 — 행동이 복잡해지면 매번 전부 다시 판단하는 것이 비싸진다.

6. **기본 브러시 크기를 추측하지 말고 재게 하자는 것**

   > 스케일 1로 먼저 놓고 바운드를 재서 거기서 스케일을 계산하라. `sizeX`가 0으로 나오면 그건 "브러시 없는 볼륨"이라는 관찰이지 우회할 것이 아니라서 STOP을 걸었다.

   얻는 것 — 결과가 여섯 면 편차 0으로 나왔고 그게 왜 그런지(4200/200 = 21이 나머지 없이 나눠떨어져서)까지 근거가 남았다. 잃는 것 — 왕복이 한 번 는다.

7. **저장을 아예 시도하지 말라고 한 것**

   > 명령 40에서 확인된 것을 반복할 이유가 없다.

   얻는 것 — 실패가 예정된 호출 셋을 안 한다. 잃는 것 — `NavMeshBoundsVolume`에도 같은 실패가 나는지는 확인 안 된 채로 남는다.

## 다음으로 넘김

**2026-08-31 세션이 이 목록을 소진했다. 처리한 항목은 아래에서 지웠고, 남은 것은
[2026-08-31 기록](2026-08-31-two-rooms-and-enemy-bp.md)의 `다음으로 넘김`으로 옮겼다.
이 칸은 이제 읽지 않아도 된다 — 가장 최근 기록을 보면 된다.**

### 이 세션에서 처리된 것

- **명령 43 `BP_Enemy` 생성** → 완료. 번호가 밀려 **명령 53·54**가 됐다(커밋 `2342d76`).
  `SkeletalMesh` 프로퍼티가 UE5에서 폐기되어 명령이 둘로 갈라졌다
- **`AI MoveTo`의 핀 확인** → 완료. 입력 1번 핀이 **`Pawn` (Pawn Object Reference)**다.
  사양의 전제가 맞았고 AI 컨트롤러를 안 만든다는 결정이 근거를 얻었다
- **`AIControllerClass`·`AutoPossessAI`를 반드시 설정한다** → **틀린 메모였다.**
  엔진 기본값이 이미 `AIController` / `PlacedInWorld`라 건드리지 않았다
- **`get_variable_instance_editable`이 없다** → 정확히는 **읽기만 없다.**
  `set_variable_instance_editable`은 있고 정상 동작한다
- **적을 어디에 놓을 것인가** → **2번 방.** 닫힌 문이 NavMesh를 실제로 끊는 것이 확인되어,
  문을 열기 전에는 적이 못 넘어온다
- **`OpenAngle`을 `-90`으로 바꿀 것인가** → **바꾸지 않는다.** 지금 배치(`X 1795`)에서
  `-90`이면 문이 벽 속으로 열린다. 사용자가 현행 유지를 선택했다
- **NavMesh가 실제로 바닥을 덮었는지** → 확인. `[-1976,-1976,10]..[5928,1976,410]`으로
  두 방을 덮는다. 단 `RebuildNavigation`을 돌려야 했다
- **문틀 100cm를 NavMesh가 통과하는지** → **통과 못 한다.** `AgentRadius 35`가
  `cellSize 19`에서 2셀(38)로 올림되어 24만 남고 셀 하나보다 좁다.
  문간을 200으로 넓혀 124를 확보했다
- **합격 기준 3의 경첩 반전 뒷부분** / **벽에 붙어 서서 `Q` · 경사면에 `Q`** →
  **검증 대상이 사라졌다.** `Wall_L`·`Wall_R`은 명령 45에서, `SM_Ramp11`은 명령 43에서 삭제됐다
