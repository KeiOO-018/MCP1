# 2026-08-31

## 작업물

**ThirdPerson 기본 레벨의 실내를 비우고 같은 크기의 두 번째 방을 붙여 잠긴 문 하나로만 통하게 만든 뒤, 적 AI의 첫 애셋 `BP_Enemy`를 만들었다** — 명령 43~54, 커밋 3개.

**소요 시간**: 약 2시간 20분. 근거는 로그와 파일 mtime이다 — UE 로그의 첫 MCP 호출 흔적이 `00:43:18`, `BP_Enemy` 컴파일이 `02:56:28`이고, `BP_Enemy.uasset`의 mtime이 `12:01:07 +0900`이다. **UE 로그는 UTC이고 파일시스템은 KST(+9)다** — 컴파일 `02:56` UTC와 저장 `12:01` KST가 5분 차이로 맞물리는 것이 그 근거다. 그래서 실제 구간은 `09:43 ~ 12:03 KST`. 커밋 셋은 `10:25:05` · `11:23:17` · `12:02:53`이다.

## 명령

### 한글

```
작업 준비
```

```
에디터 켜져있는데 방을 새롭게 하나 더 만들까 이거 원래 있던 ThirdPerson 기본 제공 프로젝트에 기본 레벨 맵 배치 크기 있잔아 안에 내용물만 싹 빼고 옆에 똑같은 크기의 바닥과 벽을 하나 더 만드는거야 그 사이를 문으로 통과하게 설계하고 이건 어때
```

**심문의 답 넷.** 아래는 타이핑한 문장이 아니라 AI가 제시한 항목별 안에서 사용자가 고른 것이다. 넷 다 AI가 권장으로 표시한 안을 골랐다.

- 칸막이 → **기존 `+X` 벽에 문을 뚫는다** (지금 문 벽을 늘려 칸막이로 쓴다 중 택1)
- NavMesh → **닫힌 문이 적을 막게 한다 · `Dynamic` + NavModifier** (`Static`으로 둔다 / 나중에 정한다 중 택1)
- 레벨 → **`Lvl_ThirdPerson`을 그대로 고친다** (복사본을 만든다 중 택1)
- 2번 방 → **비워둔다** (적 배치 지점을 지금 정한다 / 아이템을 옮긴다 중 택1)

```
커밋먼저 고
```

```
결과 확인
```

```
저거 내가 옮긴거임 괜찬아
```

```
결과 확인
```

```
터미널에 이렇게 떴어 이거 확인좀
```

```
2번 한 결과 다시 봐줘
```

```
결과 확인
```

```
커밋하자
```

```
결과 확인
```

```
이거랑 결과랑 같이봐봐
```

```
터미널말하는거지?
```

```
확인좀
```

```
방과 방 사이를 보여달라는거 아니야? 여기 왼쪽이 원래 있던거고 오른쪽이 새로운 방이고 cmd에 RebuildNavigation 했는데 이거야
```

```
첫번째봐봐 그리고 두번째 문 왜 저기로 옮겨져있어 원래 그런거야 아님 오류야 저거확인좀 일단 내가 안옮김
```

```
cmd 명령 넣었어 결과 확인해봐
```

```
다했어
```

```
PIE 결과 이상없음
```

```
커밋 먼저 고고
```

```
터미널 수행 다했고 결과가 이런건 잘 된거 같은데
```

```
A로
```

```
시작하자
```

```
결과 확인좀
```

```
결과랑 눈아이콘은 봤는데 다 잘 되어있더라 확인해봐
```

```
지금 세션 괜찬은지 확인하고 기록하거나 다음 세션 넘어가야되면 알려줘
```

```
1했고 2 3 하자
```

**스크린샷 6장이 같이 왔다.** 넷은 뷰포트(두 방 전경 · 문간 근접 · 위에서 본 칸막이 · 파킹된 문), 하나는 터미널 출력, 하나는 명령 51 결과다. 그중 문간 판정은 **AI가 `CaptureViewport`로 직접 카메라를 잡아 다시 찍어** 했다 — 사용자 스크린샷의 각도로는 그늘과 네비메시가 구분되지 않았기 때문이다.

### English — MCP에 실제로 보낸 명령

**옮기며 AI가 넣은 해석.** 한글 지시는 "방 하나 더 만들자" 한 줄이었다. 아래 좌표·라벨·플래그는 **전부 AI가 조사와 계산으로 정한 것**이고 사용자가 말한 것이 아니다.

- **방 하나의 크기 `4000×4000`, 방 2를 `+X`로 붙임** — `Floor`를 읽어 나온 값이고 방향은 AI가 정했다
- **삭제 대상 45개의 라벨 전부**와 **남길 13개의 명시적 금지 목록** — `SM_Cube`가 부분 일치로 `SM_Cube2`~`SM_Cube20`을 잡아먹으면 벽이 통째로 날아가기 때문이다
- **문간 폭 100 → 200**, `Y -100..100` — 처음 100은 지금 문짝 폭에 맞춘 값이고, NavMesh가 안 통과해 200으로 늘렸다
- **문 액터 `X 1795`** — 열릴 때 회전 반경이 벽을 안 물게 계산한 값
- **문 액터 스케일 `(1, 2, 1)`** — `BP_Door` 애셋을 안 고치고 문짝만 넓히는 우회
- **`Divider_R` · `Floor_Room2` · `Room2_Wall_*` 여섯 — 라벨 전부**
- **`NavBounds_Main` 스케일 `(41, 21, 4)`와 위치 `(2000, 0, 200)`**
- **`BP_Enemy`의 변수 일곱과 그 기본값** — 사양에서 가져왔다
- **`bUseControllerRotationYaw false`** — 사양에 없던 값. AI가 넣었다
- **`AIControllerClass`·`AutoPossessAI`를 "읽되 바꾸지 말라"는 지시** — 기본값이 이미 맞다는 판단
- **"메시지 로그를 직접 읽고 보고하라"는 지시 전부** — `compile_blueprint`의 반환값을 근거로 삼지 않기 위해서다
- **"저장하지 말라"는 지시 전부**

#### 명령 43

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, delete exactly these 45 actors, matching by EXACT actor label only (never by substring or prefix):

SM_Ramp, SM_Ramp2, SM_Ramp3, SM_Ramp4, SM_Ramp5, SM_Ramp6, SM_Ramp7, SM_Ramp8, SM_Ramp9, SM_Ramp10, SM_Ramp11, SM_Ramp12,
SM_QuarterCylinder, SM_QuarterCylinder2, SM_QuarterCylinder3, SM_QuarterCylinder4, SM_QuarterCylinder5, SM_QuarterCylinder6, SM_QuarterCylinder7, SM_QuarterCylinder8, SM_QuarterCylinder9, SM_QuarterCylinder10, SM_QuarterCylinder11, SM_QuarterCylinder12,
SM_Cylinder, SM_Cylinder2, SM_Cylinder3, SM_Cylinder4, SM_Cylinder5, SM_Cylinder6, SM_Cylinder7, SM_Cylinder8, SM_Cylinder9,
SM_Cube, SM_Cube6, SM_Cube7, SM_Cube8, SM_Cube9, SM_Cube10, SM_Cube11, SM_Cube12, SM_Cube13, SM_Cube14, SM_Cube15, SM_Cube16

CRITICAL - these actors must NOT be deleted, they are the room's floor and perimeter walls:
SM_Cube2, SM_Cube3, SM_Cube4, SM_Cube5, SM_Cube17, SM_Cube18, SM_Cube19, SM_Cube20, Floor, SM_SkySphere, Wall_L, Wall_R, Door_Test

Do not save the level yet. After deleting, report back the exact count of actors you deleted and list any label from the 45 that you could not find.
```

#### 명령 44

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, do these two things:

1. Modify the existing actor labeled exactly "SM_Cube2". Change ONLY its scale, from (2, 40, 2) to (2, 19.5, 2). Leave its location at (1800, -2000, 0) and its rotation at (0, 0, 0) unchanged. After this its bounds should be [1800, -2000, 0] to [2000, -50, 200].

2. Spawn a new StaticMeshActor from the asset /Game/LevelPrototyping/Meshes/SM_Cube with:
   - label: Divider_R
   - world location: (1800, 50, 0)
   - rotation: (0, 0, 0)
   - scale: (2, 19.5, 2)
   - mobility: Static
   - no material overrides
   Do not snap it to the ground. Its bounds should end up as [1800, 50, 0] to [2000, 2000, 200].

This leaves a 100-unit-wide gap in the wall between Y=-50 and Y=+50, spanning Z=0 to Z=200.

Do NOT modify SM_Cube17 - it stays as the lintel above the gap.
Do not save the level yet.

Report back the final location, rotation and scale of both SM_Cube2 and Divider_R.
```

#### 명령 45

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, do these three things:

1. Move the actor labeled exactly "Door_Test" to world location (1795, -50, 100). Keep its rotation at (0, 0, 0) and its scale at (1, 1, 1).

2. On that same actor, set the RelativeScale3D of its "DoorMesh" component to (0.05, 0.5, 1.0). This is currently (0.05, 0.5, 1.1). Change ONLY the Z value. Do not touch the DoorMesh RelativeLocation, which must stay (0, 50, 0).

   Do NOT change any of these variables on Door_Test - leave them exactly as they are:
   bLocked, RequiredKey, OpenAngle, bHingeOnRight, SwingSpeed.

   After this, the door mesh should occupy X 1790..1800, Y -50..50, Z 0..200.

3. Delete the two actors labeled exactly "Wall_L" and "Wall_R". Match by exact label only.
   Do NOT delete SM_Cube2, Divider_R, or SM_Cube17.

Do not save the level yet.

Report back Door_Test's world transform, its DoorMesh RelativeLocation and RelativeScale3D, and confirm Wall_L and Wall_R are gone.
```

#### 명령 46

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, spawn 7 new actors. Do not snap any of them to the ground - use the exact world transforms given.

FLOOR (1 actor), from asset /Engine/MapTemplates/SM_Template_Map_Floor
  label: Floor_Room2
  location (4000, 0, 0)   rotation (0, 0, 0)   scale (4, 4, 1)
  mobility: Movable
  override material on slot 0: /Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray
  expected bounds: [2000, -2000, -50] .. [6000, 2000, 0]

WALLS (6 actors), all from asset /Game/LevelPrototyping/Meshes/SM_Cube
  All mobility: Static. All with NO override materials.
  Rotation below is (pitch, yaw, roll).

  label: Room2_Wall_XPos_Lower
    location (5800, -2000, 0)  rotation (0, 0, 0)    scale (2, 40, 2)
    expected bounds: [5800, -2000, 0] .. [6000, 2000, 200]

  label: Room2_Wall_YNeg_Lower
    location (2000, -1800, 0)  rotation (0, -90, 0)  scale (2, 38, 2)
    expected bounds: [2000, -2000, 0] .. [5800, -1800, 200]

  label: Room2_Wall_YPos_Lower
    location (2000, 2000, 0)   rotation (0, -90, 0)  scale (2, 38, 2)
    expected bounds: [2000, 1800, 0] .. [5800, 2000, 200]

  label: Room2_Wall_XPos_Upper
    location (5900, -2000, 200) rotation (0, 0, 0)   scale (1, 40, 2)
    expected bounds: [5900, -2000, 200] .. [6000, 2000, 400]

  label: Room2_Wall_YNeg_Upper
    location (2000, -1900, 200) rotation (0, -90, 0) scale (1, 39, 2)
    expected bounds: [2000, -2000, 200] .. [5900, -1900, 400]

  label: Room2_Wall_YPos_Upper
    location (2000, 2000, 200)  rotation (0, -90, 0) scale (1, 39, 2)
    expected bounds: [2000, 1900, 200] .. [5900, 2000, 400]

Do NOT create a wall on room 2's -X side. The existing actors SM_Cube2, Divider_R and SM_Cube17 are the shared divider and must not be modified or duplicated.

Do not save the level yet.

Report back the actual world bounds of all 7 new actors and flag any that differ from the expected bounds above.
```

#### 명령 47

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, change two things:

1. Modify the actor labeled exactly "NavBounds_Main" (a NavMeshBoundsVolume).
   Set its world location to (2000, 0, 200) and its scale to (41, 21, 4).
   Leave its rotation at (0, 0, 0).
   Its current values are location (0, 0, 200), scale (21, 21, 4).
   Expected resulting bounds: [-2100, -2100, -200] .. [6100, 2100, 600]

2. On the actor labeled exactly "RecastNavMesh-Default", set the property
   RuntimeGeneration to Dynamic. It is currently Static.
   Do not change AgentRadius, AgentHeight, TileSizeUU, TilePoolSize,
   bFixedTilePoolSize or NavMeshResolutionParams.

Do not save the level yet.

Then report back:
- NavBounds_Main's actual world bounds
- RecastNavMesh-Default's RuntimeGeneration value, read back after the write
- RecastNavMesh-Default's actual world bounds (this shows how far the generated navmesh reaches)
```

#### 명령 48 — MCP가 아니라 에디터 Cmd 콘솔

```
RebuildNavigation
```

#### 명령 49 — 프로브. 커밋하지 않음

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, move the actor labeled exactly "Door_Test" to world location (0, 5000, 100). Keep its rotation at (0, 0, 0) and its scale at (1, 1, 1).

This is a TEMPORARY probe. The door is being parked outside the navigation bounds (which end at Y=2100) so it cannot affect the navmesh at all. It will be moved back to (1795, -50, 100) immediately afterwards.

Do NOT change any variables on Door_Test - leave bLocked, RequiredKey, OpenAngle, bHingeOnRight and SwingSpeed exactly as they are.

DO NOT SAVE THE LEVEL.

Report back Door_Test's world location after the move.
```

#### 명령 50

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, change three actors. Match by exact label only.

1. "SM_Cube2"  - change ONLY the scale, from (2, 19.5, 2) to (2, 19, 2).
   Location stays (1800, -2000, 0), rotation stays (0, 0, 0).
   Expected bounds after: [1800, -2000, 0] .. [2000, -100, 200]

2. "Divider_R" - change location from (1800, 50, 0) to (1800, 100, 0)
   AND scale from (2, 19.5, 2) to (2, 19, 2).
   Rotation stays (0, 0, 0).
   Expected bounds after: [1800, 100, 0] .. [2000, 2000, 200]

3. "Door_Test" - move it back from its parked position to
   location (1795, -100, 100), rotation (0, 0, 0),
   and set its ACTOR scale to (1, 2, 1).
   This is the actor's own scale, NOT the DoorMesh component's RelativeScale3D.
   Do NOT touch DoorMesh's RelativeScale3D - it must stay (0.05, 0.5, 1.1).
   Do NOT change bLocked, RequiredKey, OpenAngle, bHingeOnRight or SwingSpeed.
   Expected: the door mesh should end up spanning X 1790..1800, Y -100..100, Z -10..210.

This widens the doorway from 100 to 200 units (now Y -100..100) and widens the door to match.
Do NOT modify SM_Cube17 - it stays as the lintel.

Do not save the level yet.

Report back the world bounds of all three actors, plus Door_Test's actor scale and its DoorMesh RelativeScale3D and RelativeLocation.
```

#### 명령 51 — 프로브. 커밋하지 않음

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, rotate the actor labeled exactly "Door_Test" to rotation (pitch 0, yaw 90, roll 0).

Keep its location at (1795, -100, 100) and its scale at (1, 2, 1) unchanged.

This simulates the door in its open state so we can see whether the navmesh reconnects through the doorway. It will be rotated back to (0, 0, 0) afterwards.

Do NOT change bLocked, RequiredKey, OpenAngle, bHingeOnRight or SwingSpeed.
Do NOT touch the DoorMesh component.
DO NOT SAVE THE LEVEL.

Report back Door_Test's world transform after the rotation.
```

#### 명령 52

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, rotate the actor labeled exactly "Door_Test" back to rotation (pitch 0, yaw 0, roll 0).

Keep its location at (1795, -100, 100) and its scale at (1, 2, 1) unchanged.
Do NOT change bLocked, RequiredKey, OpenAngle, bHingeOnRight or SwingSpeed.
Do NOT touch the DoorMesh component.

Report back Door_Test's world transform.
```

#### 명령 53

```
Create a new Blueprint asset at /Game/Enemy/BP_Enemy with parent class Character.
(The folder /Game/Enemy does not exist yet - create it.)

Then configure it:

MESH (the inherited skeletal mesh component, usually named "Mesh" / "CharacterMesh0"):
  SkeletalMesh:      /Game/Characters/Mannequins/Meshes/SKM_Manny_Simple
  AnimClass:         /Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C
  RelativeLocation:  (0, 0, -89)
  RelativeRotation:  (pitch 0, yaw 270, roll 0)
  RelativeScale3D:   (1, 1, 1)

CAPSULE (the inherited capsule component, usually "CapsuleComponent" / "CollisionCylinder"):
  CapsuleHalfHeight: 90
  CapsuleRadius:     35

CHARACTER MOVEMENT component:
  bOrientRotationToMovement: true
  RotationRate:              (pitch 0, yaw 500, roll 0)
  MaxWalkSpeed:              600

CLASS DEFAULTS on the Blueprint itself:
  bUseControllerRotationYaw: false

VARIABLES - create these seven. The first six must be marked instance editable
(exposed on the Details panel of placed instances). PlayerRef must NOT be.

  SightRange      float                    default 1200.0   instance editable
  AttackRange     float                    default 150.0    instance editable
  AttackDamage    float                    default 10.0     instance editable
  AttackCooldown  float                    default 1.5      instance editable
  ThinkInterval   float                    default 0.3      instance editable
  AttackMontage   AnimMontage object ref   default None     instance editable
  PlayerRef       Character object ref     default None     NOT instance editable

  AttackMontage is intentionally left empty - the montage asset does not exist yet.

DO NOT add any event nodes or graph logic. This command only creates the asset,
its components and its variables.

Then compile the Blueprint and report back:
  - whether compilation produced any errors or warnings (read the message log, do not
    just report the return value of the compile call)
  - the Mesh component's SkeletalMesh, AnimClass, RelativeLocation, RelativeRotation
  - the capsule's CapsuleHalfHeight and CapsuleRadius
  - CharacterMovement's bOrientRotationToMovement, RotationRate, MaxWalkSpeed
  - the class defaults bUseControllerRotationYaw, AIControllerClass and AutoPossessAI
    (read them - do NOT change them; AIControllerClass should already be
     /Script/AIModule.AIController and AutoPossessAI should already be PlacedInWorld)
  - the list of variables with their types and default values
```

#### 명령 54

```
In the Blueprint /Game/Enemy/BP_Enemy, set the skeletal mesh on the component named "CharacterMesh0" (it appears as "Mesh" in the editor).

The property name is SkeletalMeshAsset - NOT SkeletalMesh. In UE 5.8 the old
SkeletalMesh property is deprecated; writing to it silently does nothing.

  SkeletalMeshAsset: /Game/Characters/Mannequins/Meshes/SKM_Manny_Simple

It currently reads None. Everything else on that component is already correct and
must NOT be changed: AnimClass, RelativeLocation (0,0,-89),
RelativeRotation (pitch 0, yaw 270, roll 0), RelativeScale3D (1,1,1).

Do not touch any variables or class defaults.

Then compile the Blueprint and report:
  - what SkeletalMeshAsset reads back as after the write
  - any compile errors or warnings, read from the message log
```

## Terminal 결과

### 원문 — English

**발췌다.** 성공한 명령의 정상 응답은 아래 `요약`에 값으로 옮겼다. **실패·경고·어긋난 응답은 전문을 붙인다.**

명령 45의 터미널 에이전트 보고 전문. 사용자가 붙여넣은 것이라 터미널 렌더링이 줄을 중복·절단한 상태 그대로다.

```
set_properties returned true but the DoorMesh scale is still 1.1. Hypothesis: the actor was reconstructed after the transform change in the same batch, reverting the component override. If that's wrong, a standalone set with no transform change will also fail to stick. Testing that now.

Hypothesis was wrong — it fails standalone too. set_properties reports true but silently drops the write. Investigating why and looking for another route.

Key finding: my cached DoorMesh path now resolves to TRASH_StaticMeshComponent_3 — the BP actor reran its construction script when I moved it, destroying and recreating its components. Re-fetching a live reference and retrying.

set_properties can write RelativeScale3D — I proved it on Divider_R's native root component (2 → 2.5, then restored to 2). It fails only on the BP-instance SCS component. Doing a read-only probe of the Blueprint default to pin down the cause.

Items 1 and 3 are done and verified. Item 2 is blocked — here is exactly what I tried and what came back.

1. Door_Test moved — done
- Location (1795, -50, 100), Rotation (0, 0, 0), Scale (1, 1, 1) — re-read from the editor.
- bLocked true, RequiredKey DT_Items/Key_Stage1, OpenAngle 90, bHingeOnRight false, SwingSpeed 1 — all unchanged.

3. Wall_L and Wall_R deleted — done
- Both gone from the outliner (matched by exact label). Actor count 39 → 37.
- SM_Cube2, Divider_R, SM_Cube17 all re-read and unchanged.

2. DoorMesh scale — NOT changed. Still (0.05, 0.5, 1.1).

ObjectTools.set_properties returns true and the value does not change. Current live state: RelativeLocation (0, 50, 0) ✔ untouched, RelativeScale3D (0.05, 0.5, 1.1) ✘.

What I established, with evidence rather than guesswork:

- The tool can write this property. On Divider_R's native root component I wrote RelativeScale3D Z 2 → 2.5, read it back as 2.5, and restored it to 2. So it is not a general "set_properties can't write transforms" failure.
- BP_Door's construction script is the cause. Read from the graph: (fn ConstructionScript () (Transformation|SetRelativeLocation (GetDoorMesh) (MakeVector 0.0 (* (* 100.0 (.y (GetRelativeScale3D (GetDoorMesh)))) (select (GetbHingeOnRight) -1.0 1.0))))). Moving the actor reruns construction, which rebuilds the SCS components from the Blueprint template and discards the write. The components actually get recreated: my cached DoorMesh reference resolved to TRASH_StaticMeshComponent_3, and the billboard component's suffix walked _1 → _2 → _4 across calls.
- The 1.1 comes from the asset, not from an instance override. The CDO template BP_Door_C:DoorMesh_GEN_VARIABLE reads RelativeScale3D (0.05, 0.5, 1.1), RelativeLocation (0,50,0) is computed by that construction script (100 × 0.5 × 1), not stored — which is also why leaving Y scale at 0.5 keeps RelativeLocation at (0,50,0).

So an instance-only override isn't durable here: even if it stuck momentarily, the next construction — including a level reload after save — resets it to the template value.

Current mesh extent with Z scale 1.1: X 1790..1800 ✔, Y -50..50 ✔, Z -10..210 instead of 0..200 — 10 units of overshoot at the floor and at the lintel.

The only route to Z scale 1.0 is editing the DoorMesh component default on the asset /Game/Interaction/BP_Door, which affects every BP_Door instance, not just Door_Test. That is broader than "on that same actor," so I stopped rather than widen the scope on my own. (I grepped the three other placements and found no hits, but .umap is compressed binary so that search proves nothing — treat the instance count as unknown.)

Level is not saved.
```

명령 51 직전, 같은 에이전트가 낸 보고 중 어긋남 부분.

```
Door_Test was at (1905, -50, 100) when I picked it up, not (1795, -50, 100). I read its transform immediately before writing the new one. I did not move it there — the last position I set was (1795, -50, 100) two steps ago, and I verified it as 1795 at the time; you also confirmed 1795 in your own state dump. Something shifted it +110 in X between then and now, outside anything I did.
```

레벨 로드 시점의 네비게이션 경고.

```
[2026.08.31-00.35.52:416][  0]LogNavigation: Warning: Recreating dtNavMesh instance (RecastNavMesh_UAID_9C6B005AF86909FD02-Default) due mismatch in number of bytes required to store serialized maxTiles (serialized: 3, 2 bits) vs calculated required (75, 7 bits)
```

PIE 종료 시점의 경고.

```
[2026.08.31-00.55.04:005][857]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
```

MCP 도구 자체가 실패한 것들.

```
GetObjectProperties on '/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default' (RecastNavMesh): the following properties could not be read: AgentMaxStepHeight, CellSize
```

```
/Game/Interaction/BP_Door.Default__BP_Door_C.DoorMesh_GEN_VARIABLE is not valid Object for property 'instance'
```

```
Function "find_nodes", input param "title" is required by the function input schema Json, but is missing from the incoming
```

```
Function "CaptureViewport", input param "annotations" needs a default value.
```

```
line 30: TypeError: _StrictDict.get() does not support a default value. Use direct key access [] instead.
```

`BP_Enemy` 컴파일 로그 — 에러도 경고도 없다.

```
[2026.08.31-02.41.55:868][282]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.08.31-02.42.27:174][379]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.08.31-02.56.28:692][879]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
```

`AI MoveTo`의 핀 — 사양의 전제를 검증한 원문 발췌.

```
"AI|AIMoveTo": {
  "input_pins": [
    {"name": "execute",          "type_id": "Exec"},
    {"name": "Pawn",             "type_id": "Pawn Object Reference"},
    {"name": "Destination",      "type_id": "Vector",                 "value": "0, 0, 0"},
    {"name": "TargetActor",      "type_id": "Actor Object Reference"},
    {"name": "AcceptanceRadius", "type_id": "Float (single-precision)","value": "5.000000"},
    {"name": "bStopOnOverlap",   "type_id": "Boolean",                "value": "false"}
  ],
  "output_pins": [
    {"name": "then",           "type_id": "Exec"},
    {"name": "OnSuccess",      "type_id": "Exec"},
    {"name": "OnFail",         "type_id": "Exec"},
    {"name": "MovementResult", "type_id": "EPathFollowingResult Enum"}
  ]
}
```

### 요약 — 한글

- **명령 43** — 액터 `83 → 38`. 정확히 45개가 사라졌다. 지울 45개 중 남은 것 없음, 남길 21개 중 사라진 것 없음
- **명령 44** — `SM_Cube2` 스케일 `(2,40,2) → (2,19.5,2)`, `Divider_R` 신규. 문간 `X 1800..2000, Y -50..50, Z 0..200`. `SM_Cube17` 무변경
- **명령 45** — 1·3 완료, 2 실패. `Door_Test`가 `(1795,-50,100)`으로 이동하고 `Wall_L`·`Wall_R`이 사라져 액터 `39 → 37`. `DoorMesh.RelativeScale3D`는 `(0.05, 0.5, 1.1)` 그대로. `ObjectTools.set_properties`가 `true`를 반환하고 값은 안 바뀌었다
- **명령 46** — 7개 전부 예상 bounds와 일치. 액터 `37 → 44`. `Floor_Room2`는 `Movable` + `MI_PrototypeGrid_Gray`, 벽 6개는 `Static` + 오버라이드 없음
- **명령 47** — `NavBounds_Main` `[-2100,-2100,-200]..[6100,2100,600]`, `RuntimeGeneration`이 `Dynamic`으로 읽힘. **그런데 생성된 네비메시는 `X 2964`에서 멈췄다**
- **명령 48** — `RebuildNavigation` 후 네비메시가 `[-1976,-1976,10]..[5928,1976,410]`로 확장
- **명령 49~50** — 문간 폭 `100 → 200`. `SM_Cube2`·`Divider_R` 스케일 `19.5 → 19`, `Divider_R` `Y 50 → 100`, `Door_Test` `(1795,-100,100)` 액터 스케일 `(1,2,1)`
- **명령 51~52** — 문 회전 `yaw 90` → `0`. 프로브라 커밋 안 함
- **명령 53** — `BP_Enemy` 생성. 부모 `Character`, 변수 7개, 캡슐·무브먼트·클래스 기본값 전부 지시대로. **`SkeletalMeshAsset`만 `None`**
- **명령 54** — `SkeletalMeshAsset`이 `SKM_Manny_Simple`로 들어감. 컴파일 깨끗

## 분석

### 무엇을 만들었나

**레벨 — `Lvl_ThirdPerson`**

- **삭제 47개** — 실내 장애물 45(램프 12 · 4분원기둥 12 · 원기둥 9 · 큐브 12)와 토막 벽 `Wall_L`·`Wall_R`
- **신규 8개** — `Divider_R`(칸막이 `+Y` 조각)과 2번 방 7개
  - `Floor_Room2` `(4000,0,0)` 스케일 `(4,4,1)` · `SM_Template_Map_Floor` · `Movable` · `MI_PrototypeGrid_Gray`
  - `Room2_Wall_XPos_Lower` `(5800,-2000,0)` yaw `0` 스케일 `(2,40,2)`
  - `Room2_Wall_YNeg_Lower` `(2000,-1800,0)` yaw `-90` 스케일 `(2,38,2)`
  - `Room2_Wall_YPos_Lower` `(2000,2000,0)` yaw `-90` 스케일 `(2,38,2)`
  - `Room2_Wall_XPos_Upper` `(5900,-2000,200)` yaw `0` 스케일 `(1,40,2)`
  - `Room2_Wall_YNeg_Upper` `(2000,-1900,200)` yaw `-90` 스케일 `(1,39,2)`
  - `Room2_Wall_YPos_Upper` `(2000,2000,200)` yaw `-90` 스케일 `(1,39,2)`
  - 벽 6개 전부 `SM_Cube` · `Static` · 머티리얼 오버라이드 없음
- **수정 4개**
  - `SM_Cube2` 스케일 `(2,40,2) → (2,19,2)` — 칸막이 `-Y` 조각
  - `Door_Test` `(1225,-50,110) → (1795,-100,100)`, 액터 스케일 `(1,1,1) → (1,2,1)`
  - `NavBounds_Main` `(0,0,200)/(21,21,4) → (2000,0,200)/(41,21,4)`
  - `RecastNavMesh-Default.RuntimeGeneration` `Static → Dynamic`
- **문간** — `X 1800..2000, Y -100..100, Z 0..200`. 폭 200. 위 띠 `SM_Cube17`이 인방

**애셋 — `Content/Enemy/BP_Enemy` 신규**

- 부모 `Character`. 그래프 로직 없음. 컴포넌트는 `CollisionCylinder` · `Arrow` · `CharacterMesh0` · `CharMoveComp`
- `CharacterMesh0` — `SKM_Manny_Simple` / `ABP_Unarmed_C` / `RelativeLocation (0,0,-89)` / `RelativeRotation (0,270,0)` / `Scale (1,1,1)`
- `CollisionCylinder` — `CapsuleHalfHeight 90` / `CapsuleRadius 35`
- `CharMoveComp` — `bOrientRotationToMovement true` / `RotationRate (0,500,0)` / `MaxWalkSpeed 600`
- 클래스 기본값 — `bUseControllerRotationYaw false` / `AIControllerClass /Script/AIModule.AIController`(기본값) / `AutoPossessAI PlacedInWorld`(기본값)
- 변수 7개 — `SightRange 1200` · `AttackRange 150` · `AttackDamage 10` · `AttackCooldown 1.5` · `ThinkInterval 0.3` · `AttackMontage None` · `PlayerRef None`

**문서** — [두 방 사양](../Spec/2026-08-31-두-방-구조.md) 신규, [적 AI 1단계 사양](../Spec/2026-08-30-적-AI-1단계.md) 네 곳 수정.

### 기술적으로 맞게 짚은 부분

- **삭제 명령에 "남길 목록"을 명시적으로 넣은 것.** `SM_Cube`를 부분 일치로 지우면 `SM_Cube2`~`SM_Cube20`이 딸려가 바닥과 외벽이 통째로 날아간다. 정확 라벨 일치를 강제하고 금지 목록을 따로 준 덕에 47개가 정확히 지워졌다
- **2번 방에 `-X` 벽을 만들지 않은 것.** `SM_Cube2`/`Divider_R`/`SM_Cube17`이 이미 두 방의 경계다. 액터 두 개와, 두 벽이 등을 맞대 400 두께가 되는 흉한 결과를 같이 피했다
- **위 띠 `SM_Cube17`을 자르지 않은 것.** 문간을 아래 띠에만 내면 위 띠가 그대로 인방이 된다. 넘겨받은 "문틀 메시와 인방" 항목이 액터를 하나도 안 만들고 해결됐다
- **`NavModifierComponent`를 안 만든 것.** `DoorMesh`가 이미 `Movable` + `bCanEverAffectNavigation true`라 `RuntimeGeneration = Dynamic` 속성 하나로 끝났다. 결정 사다리 3번에서 멈춘 것이다
- **`RuntimeGeneration`을 소스로 검증한 것.** `ARecastNavMesh::SupportsRuntimeGeneration()`이 `RuntimeGeneration != Static` 하나로 결정되고(`RecastNavMesh.cpp:4379`) `bRebuildAtRuntime`은 폐기됐다(`NavigationData.cpp:185`). 프로젝트 설정을 따로 찾아 헤매지 않았다
- **`bIsWorldPartitioned`를 먼저 읽은 것.** `false`라서 World Partition 동적 네비 경로도 액티브 타일 생성도 안 탄다는 것을 미리 확인했다. `IsUsingActiveTilesGeneration()`이 참이었다면 인보커 없이는 네비가 비었을 것이다
- **`show navigation` 대신 에디터에서 확인한 것.** PIE 콘솔이 안 먹자 PIE를 파고들지 않고, 문 액터를 `yaw 90`으로 돌려 열린 상태를 만들고 **닫힘·열림을 완전히 같은 카메라로 찍어 비교**했다. 바뀐 변수가 문 회전 하나뿐이라 비교가 성립한다
- **문짝 폭을 액터 스케일로 넓힌 것.** `DoorMesh.RelativeScale3D`는 애셋 템플릿 값이라 고치면 모든 `BP_Door` 인스턴스가 따라온다. 액터 스케일 `(1,2,1)`은 이 인스턴스에만 걸리고, 컨스트럭션 스크립트가 **상대** 스케일만 읽기 때문에 힌지 오프셋도 같이 두 배가 되어 정확히 맞는다
- **문 높이 220 → 200을 취소한 것.** 합격 기준 어디도 요구하지 않는 미관 항목이었고 공유 애셋을 고쳐야만 가능했다. 손대지 않은 것이 정답이었다
- **`AIControllerClass`·`AutoPossessAI`를 안 건드린 것.** 엔진 기본값이 이미 `AIController` / `PlacedInWorld`다. 넘겨받은 "반드시 설정한다"는 메모가 틀렸다
- **`PlayerStart`를 안 건드린 것.** 사양은 `Z 92`로 내리기로 했는데, 조사 중 사용자가 손으로 `192`에 맞춘 것이 드러나 계획에서 뺐다

### 확인한 것 / 확인 못 한 것

**확인한 것** — 전부 에디터에서 실제 상태를 다시 읽었다. MCP 응답을 근거로 삼은 것은 하나도 없다.

- 액터 수 `83 → 38 → 39 → 37 → 44`. 각 단계에서 라벨을 전수 대조
- 신규·수정 액터 전부의 월드 bounds가 예상값과 일치. `mismatched: []`
- 문간 지오메트리를 트레이스로 검증. `Z=100`에서 `X 1700→2100` 스캔 — `Y -110..-100` 벽, `Y -100..+100` 문짝, `Y +110..+130` 벽. 빈틈 없음
- 인방 위치 — `Y 0, Z 300` 트레이스가 `X 1900`(`SM_Cube17`) 히트
- 문짝 실측 — 정면 `(1400,0,110)` 캡처에서 `Y -98..+100`, `Z 208`
- 네비메시 범위 `[-1976,-1976,10]..[5928,1976,410]`
- **문 닫힘 → 문간 네비 단절.** 1번 방 네비가 `X 1743`에서 끝나고 문간 네비가 `X 1842`에서 시작. 99 폭의 빈 구간
- **문 열림 → 연속.** 같은 카메라에서 `X 1629..1946` 끊김 없음
- `BP_Enemy`의 메시·캡슐·무브먼트·클래스 기본값·변수 7개를 `BP_ThirdPersonCharacter`와 나란히 읽어 대조
- `BP_Enemy` 컴파일 — `LogK2Compiler` 비었고 `LogBlueprint`에 `Compiling Blueprint` 세 줄뿐. **메시지 로그를 직접 읽었다**
- `AI|AIMoveTo`의 입력 1번 핀이 `Pawn (Pawn Object Reference)`
- 커밋 3개의 파일을 단위로 대조. 삭제 47 = 45 + `Wall_L` + `Wall_R`, 신규 8, 수정 파일은 해시 파일명에서 라벨을 뽑아 신원 확인
- `BP_ThirdPersonCharacter`의 EventGraph 노드 87개 전수 조회 — `K2Node_AIMoveTo`·`K2Node_LatentGameplayTaskCall` 없음

**확인 못 한 것**

- **`BP_Enemy`의 인스턴스 편집 플래그.** `set_variable_instance_editable`은 있는데 `get_...`이 없다. **사용자가 눈 아이콘을 보고 "다 잘 되어있더라"고 알려준 것이 유일한 근거다**
- **PIE 합격 기준 1·2·3.** 사용자가 "PIE 결과 이상없음"이라고 보고했다. **AI가 화면으로 본 것이 아니다.** 어느 기준을 어떤 순서로 봤는지도 안 물었다
- **`show navigation`이 PIE에서 안 먹는 이유.** 플래그(`ShowFlagsValues.inl:179`)와 명령 파싱은 확인했고 `UNavMeshRenderingComponent`에 `bIsEditorOnly = true`가 있는 것도 봤지만, 그것이 원인인지 확인하지 않았다
- **`trace_world`가 방향에 따라 결과가 갈리는 이유.** 열린 문짝을 X축으로 쏘면 `X 1595`에서 잡히는데 Y축으로 쏘면 `X 1600~1780` 전부 놓쳤다. 4개 높이에서 일관된 X축 결과를 근거로 삼고 원인은 안 봤다
- **`Door_Test`가 `1795 → 1905`로 +110 옮겨진 경위.** 디스크 파일이 커밋과 동일했으므로 저장 이후 메모리에서만 생긴 값인 것까지는 확인했으나, 누가 옮겼는지는 모른다. 사용자에게 물었고 답을 못 받았다
- **`BP_Door.uasset` +32바이트의 정체.** `DoorMesh` 템플릿의 `RelativeScale3D`가 `(0.05,0.5,1.1)` 그대로임은 확인했다. 나머지 차이는 바이너리라 못 읽었다
- **네비 경고 `maxTiles (serialized: 3, 2 bits) vs calculated required (75, 7 bits)`의 의미.** 프레임 0에 찍혔고 이후 동작에 지장이 없어 보이지만 해석하지 않았다
- **2번 방의 조명.** 방을 새로 만들었는데 `DirectionalLight`·`SkyLight` 외에 아무것도 안 놓았다. 눈으로 이상한지 안 봤다

### 남는 리스크

- **비균등 액터 스케일이 물리 바디를 스테일로 남긴다.** `Door_Test`에 `(1,2,1)`을 넣었을 때 화면에서는 문짝이 200인데 `trace_world`는 100으로 읽었다. **레벨을 저장하고 다시 연 뒤에야 일치했다.** 콜리전을 읽는 모든 것(트레이스·NavMesh 생성)이 영향을 받는다. 앞으로 비균등 스케일을 쓰면 재로드 전에는 검증이 무의미하다
- **`ObjectTools.set_properties`가 BP 인스턴스의 SCS 컴포넌트에서 `true`를 반환하고 조용히 쓰지 않는다.** 같은 도구가 네이티브 루트 컴포넌트(`Divider_R`)에는 정상적으로 쓴다. 터미널 에이전트가 `2 → 2.5 → 2`로 대조 실험까지 해서 확인했다
- **`SkeletalMesh` 프로퍼티는 UE5에서 폐기됐다.** 쓰기가 무시되고 **로그도 안 남는다.** `SkeletalMeshAsset`을 써야 한다. 명령 하나가 통째로 헛돌았다
- **`BlueprintTools.get_node_type_pins`가 읽기인데 대상 블루프린트를 더티로 만든다.** `BP_ThirdPersonCharacter`의 EventGraph에서 `AI MoveTo` 핀을 읽었더니 파일이 재직렬화됐다. 노드는 안 남았고 바이트 수도 `592040`으로 같지만, **읽기라고 믿고 남의 애셋에 돌리면 안 된다**
- **`NavMeshBoundsVolume`을 옮기면 증분 갱신만 돈다.** 볼륨을 `X 6100`까지 늘렸는데 네비메시는 타일 한 장만 늘어 `X 2964`에서 멈췄다. `RebuildNavigation`으로 전체를 다시 구워야 했다
- **`trace_world`가 방향에 따라 같은 솔리드를 놓친다.** 원인 미상
- **`get_label`이 간헐적으로 예외를 던진다.** 검증 스크립트가 그걸 `continue`로 삼켜서 아이템 픽업 3개가 없어진 것처럼 보였다. **스크립트가 예외를 삼킨 것은 AI의 잘못이다**
- **`BP_Door.uasset` 재직렬화가 세 번째다** (`b4ab97a` · 명령 39 · 이번). 원인 미상
- **문간 위 `X 1800..1900, Z 200..400`이 열린 홈으로 남는다.** 위 띠가 100 안쪽으로 물러나 있어 1번 방 쪽에서 보면 문 위가 우묵하다. 관통은 아니다
- **열린 문짝 20cm가 문간 위로 삐져나온다.** 문짝 220, 문간 200
- **칸막이 짝의 이름이 어긋난다.** `SM_Cube2` / `Divider_R`. 리네임은 먼저 묻기로 되어 있어 안 했다
- **적 AI 사양의 합격 기준 4·5 문구가 미승인 상태다.** `Wall_L`이 지워져 원래 문구를 못 쓰게 됐고, AI가 대체안을 냈으나 사용자가 채택 여부를 답하지 않았다
- **2번 방이 비어 있다.** 바닥과 벽뿐이다

### 총평

요청은 "방 하나 더 만들고 그 사이를 문으로 통과하게" 한 줄이었고, 결과는 그것을 넘어섰다 — **잠긴 문 하나가 두 방을 가르고, 열쇠가 1번 방에 있으며, 닫힌 문이 AI의 경로까지 실제로 끊는다.** 열쇠 루프는 이미 있던 것을 발견해 쓴 것이고 새로 만들지 않았다.

**실질적 난이도는 지오메트리가 아니라 "MCP가 안 했는데 했다고 말하는 것"을 잡아내는 데 있었다.** 세 번 걸렸다. `set_properties`가 `true`를 주고 안 쓴 것, `SkeletalMesh` 쓰기가 로그도 없이 무시된 것, 비균등 스케일이 렌더만 갱신하고 콜리전을 남긴 것. 셋 다 **응답이 아니라 실제 상태를 다시 읽어서** 잡혔고, 세 번째는 화면과 트레이스를 대조해야만 보였다.

가장 비쌌던 판단은 **문간 폭 100**이다. 문짝을 안 건드리려고 100으로 잡았는데 `AgentRadius 35`가 `cellSize 19`에서 2셀로 올림되어 양쪽 76이 깎이고 24만 남았다 — 셀 하나보다 좁아 네비가 0개가 됐다. 200으로 늘려 124를 확보했다. **넘겨받은 "확인 필요" 항목이 정확히 이것을 가리키고 있었고, 계산까지 맞았는데도 실제로 부딪히기 전까지는 어느 쪽인지 몰랐다.**

`BP_Enemy`는 값을 플레이어와 나란히 읽어 대조했으므로 안전하다. 다만 **인스턴스 편집 플래그만은 AI가 읽을 수 없어 사용자 눈에 의존한다.**

## AI의 제안

1. > **저장 시점을 앞당기자.** "원래 계획은 48에서 저장이었는데, 세 명령이 다 검증을 통과했으니 지금 잠그는 게 낫다."

   명령 43~45가 전부 미저장이라 에디터가 죽으면 45개 삭제가 통째로 날아가는 상태였다. 얻는 것은 작업 보존과 `git status`라는 증거, 잃는 것은 "저장 안 했으니 그냥 안 하면 되돌아간다"는 값싼 취소 경로다.

2. > **합격 기준 4를 바꾸자.** "PIE에서 문을 닫아둔 채 2번 방의 적이 나를 보면 적이 칸막이를 통과하지 못하고 넘어오지 않는다 / 문을 열면 적이 문간을 지나 1번 방까지 따라온다."

   원래 기준 4가 이번에 지운 `Wall_L`을 가리켜 검증이 불가능해졌다. 얻는 것은 같은 목적을 지키면서 동적 네비 차단까지 보는 것, 잃는 것은 기준이 넷에서 다섯으로 늘어 검증 시간이 길어지는 것.

3. > **문을 벽 가운데로 못 옮긴다.** "힌지가 `X ≤ 1800`이어야 회전 반경이 벽을 안 문다. 지금 1795니까 가운데로 옮길 여유가 5밖에 없다."

   사용자가 문을 두 벽 사이 가운데로 옮겨도 되는지 물었을 때 낸 답이다. 얻는 것은 문이 실제로 열린다는 것, 잃는 것은 두꺼운 벽에서 문이 한쪽 면에 치우쳐 보이는 것. 대안으로 `X 2005` + `OpenAngle -90`(2번 방으로 열림)을 같이 냈고 사용자가 현행 유지를 골랐다.

4. > **`bUseControllerRotationYaw`를 `false`로.** "`APawn` 기본값이 `true`라 그냥 두면 `bOrientRotationToMovement true`와 컨트롤러 요가 서로 싸운다."

   사양의 "베낄 값" 표에 없던 항목이다. 얻는 것은 적이 이동 방향으로 정상 회전하는 것, 잃는 것은 없다 — 플레이어 BP도 같은 값이다.

5. > **`AIControllerClass`와 `AutoPossessAI`를 건드리지 말자.** "엔진 기본값이 이미 `AIController` / `PlacedInWorld`이고 손으로 배치하는 적에게는 그게 맞는 설정이다."

   넘겨받은 메모가 "반드시 설정한다"고 적어둔 것을 뒤집은 것이다. 얻는 것은 명령이 짧아지고 기본값과 다른 값이 안 생기는 것, 잃는 것은 의도가 문서에만 남고 BP에는 안 보이는 것.

## 다음으로 넘김

**바로 이어서 할 것**

- **명령 55 — `BP_Enemy`의 `Think` 루프.** [사양](../Spec/2026-08-30-적-AI-1단계.md)의 `완성 후의 호출 구조` 그대로, **공격 없이 추격까지만**. `BeginPlay`에서 `PlayerRef` 캐시 → `Think` 커스텀 이벤트 → 거리 재기 → `AI MoveTo(Pawn=self, TargetActor=PlayerRef, AcceptanceRadius=AttackRange-20)` → `OnSuccess`/`OnFail` 각각 `Delay(ThinkInterval)` → `Think`
  - **핀 이름과 타입은 확인됐다.** 위 `Terminal 결과` 원문 참조
  - **`AI MoveTo`는 라텐트다.** `Think`는 반드시 **커스텀 이벤트**여야 한다. 함수 그래프에는 못 넣는다
- **명령 56 — 레벨에 `BP_Enemy` 배치 + 손 저장 → PIE.** 적은 **2번 방**에 둔다. 닫힌 문이 네비를 끊는 것이 확인됐으므로 문을 열기 전에는 안 넘어온다

**결정 필요**

- **합격 기준 4·5의 문구.** AI가 낸 대체안을 사양에 써두었으나 **사용자 승인을 못 받았다.** 명령 56 전에 확정해야 한다
- **적을 2번 방 어디에 둘 것인가.** 문에서 너무 멀면 `SightRange 1200` 밖이라 아무 일도 안 일어난다. 문간이 `X 1900`이므로 `(2500, 0, 90)` 근처를 권한다 — 미확정
- **칸막이 `SM_Cube2`를 `Divider_L`로 리네임할 것인가.** 짝이 `SM_Cube2` / `Divider_R`로 어긋나 있다
- **`BP_Door.uasset`의 세 번째 재직렬화를 어떻게 다룰 것인가.** 매번 커밋에 섞여 들어온다

**확인 필요**

- **`BP_Enemy`의 인스턴스 편집 플래그.** 사용자가 눈으로 확인해줬으나 AI가 읽을 수단이 없다. 명령 56에서 레벨에 놓았을 때 디테일 패널에 여섯 개가 실제로 나오는지가 두 번째 근거가 된다
- **PIE 합격 기준 1·2·3의 실제 관찰 내용.** "이상없음"만 받았고 어느 기준을 어떻게 봤는지 안 물었다
- **2번 방의 조명.** 새 방에 조명을 하나도 안 놓았다
- **`Door_Test`가 `1795 → 1905`로 옮겨진 경위.** 사용자에게 물었고 답을 못 받았다
- **두 신규 외부 액터 패키지의 정체와 `__ExternalObjects__` 파일의 정체.** 명령 40·42 때부터 쌓인 항목이다
- **`Lvl_ArenaShooter`의 WorldSettings가 `BP_ShooterGameMode`를 가리키는지.** `.umap`이 바이너리라 못 읽었다
- **`HandGrip_R` 소켓의 위치·각도.** 방향이 있는 메시(칼)가 오면 드러난다

**접어둔 것**

- **카메라 작업.** 조사해서 셋으로 갈렸다.
  - **A — 원본 ICI 구조(`캡슐 → Camera → SkeletalMesh`)로 교체.** 문서 셋이 권했지만 **지금 그대로는 못 한다.** 팔만 있는 스켈레탈 메시가 프로젝트에 없다
  - **B — 지금 구조를 두고 팔을 시야로 올린다.** `Variant_Shooter/Anims/ABP_FP_Weapon` + `Ctrl_HandAdjusment`. 무기용이라 맨손·칼에 맞는지는 열어봐야 안다
  - **C — 전환 스냅 완화만.** 요 보간 또는 `SetViewTargetWithBlend`. 2026-08-27부터 이월. 작다
  - **칼 직전에 B로 가는 것을 권했고 사용자가 적 AI를 먼저 하기로 정했다**
- **적의 HP · 피격 · 사망 · 시체 정리.** 플레이어에게 공격 수단이 생긴 뒤에
- **플레이어 사망과 리스폰.** 진행 구조 단계
- **적 체력바 위젯 / 시야각 / 순찰 / EQS / 여러 적의 회피 / 적 종류별 DataTable.** 사양의 `접어둔 것` 참조
- **AnimNotify로 타격 창 열기.** 무기가 생길 때. 지금은 데미지가 애니메이션의 타격 순간보다 먼저 들어간다
- **`BP_ShooterNPC` · `ST_Shooter` · EQS 3개 · StateTree 태스크 6개.** 안 쓰기로 했지만 지우지 않는다
- **`--append-system-prompt`가 저장소에 없다.** `Editor Preferences → General → Terminal → Startup Commands`의 사용자 설정이라 다른 환경에서는 다시 넣어야 한다. 원문은 `Docs/AI-Log/2026-08-28-inventory-item-data.md`의 `명령` 칸에 있다
- **`show navigation`이 PIE에서 안 먹는 이유.** 에디터 뷰포트의 `P`로 우회했다
- **`trace_world`의 방향 의존 누락.** X축 결과를 근거로 삼고 넘어갔다
- **`ForLoop.FirstIndex`가 빈 값인 이유.** 동작에 지장이 없다
- **`SP` 스태미나.** 원본에 있고 MCP1에 없다. `06-플레이어-UI.md:54` 참조
- **슬롯 2칸 vs 3칸.** 원본은 2칸, MCP1은 3칸이다. 의도한 차이인지 안 정했다
- **미사용 애셋 정리.** 2026-08-30에 **남기기로** 정했다. 지우지 않는다
- **`MoveComponentTo`의 `Stop`·`Return` 핀.** 연타로는 문제가 안 났다
