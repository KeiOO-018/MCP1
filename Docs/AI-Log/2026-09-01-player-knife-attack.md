# 2026-09-01

## 작업물

플레이어가 칼을 주워 오른손에 들고, `LMB`로 휘두르면 몽타주의 타격 프레임에 전방 구체 트레이스가 나가 적을 잡아내는 것까지.

**소요 시간**: UE 출력 로그 타임스탬프 기준 약 6시간 15분 (`00:26` → `06:39`). 벽시계 시간이며 집중 작업 시간이 아니다. 중간에 수작업 구간과 PIE 확인이 여러 번 끼어 있다.

## 명령

### 한글

```
작업준비
```
```
(질문 답) 칼부터
```
```
(질문 답) 엔진 Cube 늘려서 임시 칼
(질문 답) DT_Items에 Knife 행 추가 (Holdable)
(질문 답) AnimNotify로 타격 창 열기
(질문 답) 공격 모션 + 타격 판정까지 (적은 안 죽음)
```
```
(질문 답) S_ItemDef에 HeldScale(Vector) 칸 추가
(질문 답) AnimNotify — 한 순간, 트레이스 1회
(질문 답) 1번 방 스폰 근처
```
```
가자
```
```
결과 확인
```
```
결과 확인
```
```
이거보임 1인칭일때 손에 아이템에 있는게 아니라 손 아래쪽에 아이템이있어 이거 놓친거같에 확인좀
```
```
이거 확인해줘 저거뜨면서 변경이 안됨
```
```
여기서 우클릭을 어디에 해야 보이는거야 저거 3번
```
```
이렇게?
```
```
그거 다했는데 이렇게 보임 확인좀
```
```
했어
```
```
이거 원래 큐브 위치가 저기가 맞는거야?
```
```
오케이 그럼 그렇게하자
```
```
칸만들고 저장했어
```
```
결과 확인
```
```
결과 확인
```
```
이것들 바바
```
```
근데 막대가 이게 방향이 맞아?
```
```
이거 명령넣을태니까 아마 잘될거야 어택준비하자
```
```
막대방향 처음 그거대로 바
```
```
막대방향 처음 한대로 바꿔놔줘
```
```
PIE 결과 막대 잘 돌아감
```
```
8번해보자 결과 확인해주고
```
```
결과 확인
```
```
결과 확이
```
```
근데이게 왼손을 뻗는 애니메이션같은데 이걸 오른손이 멀리 나간걸로 해도되는거야?
```
```
저건 발차기임
```
```
결과 확인과 오른손으로 때리네 저건 보니까
```
```
가자
```
```
결과 확인
```
```
결과 확인
```
```
결과 확인
```
```
저 4가지 잘 되는데 나중에 나중에는 애니메이션을 실제로 구해봐야겠다 이거 검으로 휘둘러서 때려야 하는디 무료 제공중에 머 없나도 찾아봐야 할듯? 지금은 잘 되니까 나중에 바꿔끼면 되는거 아닌가 아니면 나중을 대비해서 상하체 따로 분리를 미리 해야하나 고민좀 해볼까
```
```
분리를 해야하긴 하겠다 이거좀 오래걸릴라나
```
```
15 가자
```
```
결과 확인
```
```
1 2 3 4 다 잘되는데 이거 적어놀게 공격 애니메이션 지금 있는게 앞으로 이동한다 애니메이션 동작할 때 이거 때문이라도 상체 하체 나눠야겠다
```
```
그리고 나중에 검 오브젝트 구하면 검 경로에 따라 히트 트레이스 이거 바꿀 수 있는거지? 적 공격에도 똑같이 적용시킬거라 지금 적이 공격하면 무조건 맞는거잔아 나중에 이렇게 똑같이 바꿀 수 있게 되어있나 확인도
```
```
그럼 지금 정리하는게 나은 시점인가?
```
```
세이브 했어 다 정리하자 좀 많이 한거같아서 정리가 필요할 거 같아
```

### English — MCP에 실제로 보낸 명령

이 세션에서 영어 명령은 **사용자가 UE의 Terminal에 붙여넣는 형태**로 나갔다. AI가 직접 MCP를 호출한 것은 전부 읽기(`get_properties`, `find_nodes`, `read_graph_dsl`, `get_rows`, `GetLogEntries` 등)였고, 쓰기는 아래 명령문으로만 이루어졌다.

**명령 1 — `DT_Items`에 `Knife` 행**

```
In the DataTable at /Game/Inventory/DT_Items, add a new row named "Knife".
Then set that row's values to:
  displayName = "Knife"
  iconColor   = R 0.7, G 0.7, B 0.75, A 1.0
  mesh        = /Engine/BasicShapes/Cube.Cube
  nature      = Holdable
  healAmount  = 0

Do not modify any other row.
After setting the values, read the "Knife" row back and report its full contents.
```

**명령 2 — 칼 픽업 배치**

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, spawn a new actor
from the asset /Game/Inventory/BP_ItemPickup at world location X=300, Y=0, Z=20
with zero rotation and scale 1,1,1. Name the actor "Knife_Pickup".

Then set that new actor's ItemRow property to point at the DataTable
/Game/Inventory/DT_Items with row name "Knife".

Then read back and report: the actor's world transform, its ItemRow value,
and the StaticMesh currently assigned to its Mesh component.
```

**명령 3 — `HeldItemMesh` 트랜스폼 영으로**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter,
set these properties on the HeldItemMesh component template:
  RelativeLocation = X 0, Y 0, Z 0
  RelativeRotation = Pitch 0, Yaw 0, Roll 0
Leave RelativeScale3D at 0.15, 0.15, 0.15 — do not change it.

Then compile the Blueprint.
Then read back and report HeldItemMesh's parent component, its RelativeLocation,
RelativeRotation, and RelativeScale3D.
```

**콘솔 명령 (Terminal 아님, PIE 콘솔)**

```
GetAll StaticMeshComponent AttachSocketName Name=HeldItemMesh
```

**명령 4 — `heldTransform` 네 행 채우기**

```
In the DataTable /Game/Inventory/DT_Items, set the heldTransform property on all four rows.
The heldTransform value is a ToolsetTransform with the shape
{"location": {"x":..,"y":..,"z":..}, "rotation": {"pitch":..,"yaw":..,"roll":..}, "scale": {"x":..,"y":..,"z":..}}

Key_Stage1   -> location (0,0,0), rotation (0,0,0), scale (0.15, 0.15, 0.15)
Potion_Small -> location (0,0,0), rotation (0,0,0), scale (0.15, 0.15, 0.15)
Ball_Test    -> location (0,0,0), rotation (0,0,0), scale (0.15, 0.15, 0.15)
Knife        -> location (0,0,0), rotation (0,0,0), scale (0.04, 0.04, 0.5)

Change only the heldTransform property. Do not touch displayName, iconColor, mesh,
nature, or healAmount on any row.

Then read all four rows back and report their full contents.
```

**명령 5 — `RefreshHeldItem`에 `SetRelativeTransform` 추가**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, edit the
function graph named "RefreshHeldItem".

That graph currently has a Get Data Table Row node on /Game/Inventory/DT_Items.
On its "Row Found" execution branch it breaks the returned S_ItemDef struct and
calls SetStaticMesh on the HeldItemMesh component using the struct's Mesh member.

Add exactly one new step, immediately AFTER that SetStaticMesh node and on the same
execution line: call SetRelativeTransform on the HeldItemMesh component, and wire the
broken struct's HeldTransform member into its New Transform pin. Leave Sweep
unchecked and Teleport at its default value.

Do not add, remove, or rewire anything in the other branches - the empty-name branch,
the Row Not Found branch, and the out-of-range branch must stay exactly as they are.

Then compile the Blueprint and report the compiler output.
```

**막대 축 실험 (X축)**

```
In the DataTable /Game/Inventory/DT_Items, set the heldTransform property on the
"Knife" row only:
  location (0, 0, 0)
  rotation (0, 0, 0)
  scale (0.5, 0.04, 0.04)

Do not touch any other row, and do not touch any other property on the Knife row.
Then read the Knife row back and report its full contents.
```

**명령 6 — 막대 축 원복 (Z축)**

```
In the DataTable /Game/Inventory/DT_Items, set the heldTransform property on the
"Knife" row only:
  location (0, 0, 0)
  rotation (0, 0, 0)
  scale (0.04, 0.04, 0.5)

Do not touch any other row, and do not touch any other property on the Knife row.
Then read the Knife row back and report its full contents.
```

**명령 7 — 몽타주 복제**

```
Duplicate the asset /Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Enemy_Attack
to /Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.

Do not modify the original AM_Enemy_Attack in any way.

Then read the new AM_Player_Attack and report its SlotAnimTracks, SequenceLength,
BlendIn, and BlendOut.
```

**명령 8 — 시퀀스를 `MM_Attack_02`로 교체**

```
On the asset /Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack,
set the SlotAnimTracks property to exactly this value:

[ { "slotName": "DefaultSlot",
    "animTrack": {
      "animSegments": [ {
        "cachedPlayLength": 1,
        "animReference": { "refPath": "/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_02.MM_Attack_02" },
        "startPos": 0,
        "animStartTime": 0,
        "animEndTime": 1,
        "animPlayRate": 1,
        "loopingCount": 1
      } ] } } ]

The only difference from the current value is animReference, which currently points at
MM_Attack_01. Every other field must stay as written above.

Do not touch AM_Enemy_Attack.

Then read AM_Player_Attack back and report its SlotAnimTracks and SequenceLength.
```

**명령 10 — `MM_Attack_01`로 원복**

```
On the asset /Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack,
set the SlotAnimTracks property to exactly this value:

[ { "slotName": "DefaultSlot",
    "animTrack": {
      "animSegments": [ {
        "cachedPlayLength": 1,
        "animReference": { "refPath": "/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01.MM_Attack_01" },
        "startPos": 0,
        "animStartTime": 0,
        "animEndTime": 1,
        "animPlayRate": 1,
        "loopingCount": 1
      } ] } } ]

Do not touch AM_Enemy_Attack.
Then read AM_Player_Attack back and report its SlotAnimTracks and SequenceLength.
```

**콘솔 명령 (노티파이 확인용 — 실행되지 않음)**

```
GetAll AnimMontage Notifies Name=AM_Player_Attack
```

**명령 11 — `IA_Attack` 생성**

```
Create a new Enhanced Input InputAction asset:
  folder path : /Game/Input/Actions
  asset name  : IA_Attack
  asset class : /Script/EnhancedInput.InputAction

Then set these properties on the new IA_Attack asset, matching the existing
/Game/Input/Actions/IA_Interact asset:
  ValueType          = Boolean
  bConsumeInput      = true
  bTriggerWhenPaused = false
  Triggers           = empty array
  Modifiers          = empty array

Then read IA_Attack back and report ValueType, Triggers, Modifiers, bConsumeInput,
and bTriggerWhenPaused.
```

**명령 12 — `IMC_Default`에 `LeftMouseButton` 매핑 추가**

```
In the Input Mapping Context /Game/Input/IMC_Default, add ONE new entry to the
defaultKeyMappings.mappings array:

  { "triggers": [],
    "modifiers": [],
    "action": { "refPath": "/Game/Input/Actions/IA_Attack.IA_Attack" },
    "key": { "keyName": "LeftMouseButton" },
    "settingBehavior": "InheritSettingsFromAction",
    "playerMappableKeySettings": "None" }

CRITICAL: the array currently holds 13 entries - IA_Jump on SpaceBar and
Gamepad_FaceButton_Bottom, IA_Move on W/S/A/D/Up/Down/Right/Left/Gamepad_Left2D,
IA_Look on Gamepad_Right2D, and IA_SwitchCamera on V. Several of those carry
modifier object references such as InputModifierSwizzleAxis_3 and
InputModifierNegate_0. Read the array first, then write it back with all 13
existing entries preserved byte for byte and the new entry appended at the end.
Do not drop or rebuild any modifier reference.

Then read defaultKeyMappings back and report every entry - action, key, and modifiers.
```

**명령 13 — 캐릭터에 변수 3개**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, add three
new member variables:

1. Name: AttackMontage
   Type: object reference to /Script/Engine.AnimMontage
   Instance editable: true

2. Name: AttackRange
   Type: float (double-precision)
   Instance editable: true

3. Name: AttackTraceRadius
   Type: float (double-precision)
   Instance editable: true

Then compile the Blueprint.

Then set these default values on the Blueprint's class default object:
   AttackMontage     = /Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack
   AttackRange       = 200.0
   AttackTraceRadius = 40.0

Then compile again, and read back all three values from the class default object
and report them.
```

**명령 14 — `IA_Attack` 이벤트 → 조건 검사 → 몽타주 재생**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, in the
EventGraph, build this chain. Place it in an empty area below the existing
IA_SwitchCamera chain.

1. Add an Enhanced Input Action event for /Game/Input/Actions/IA_Attack.IA_Attack
   and use its "Triggered" execution pin to drive everything below.

2. First gate - are we already attacking? Call GetCurrentMontage on self (it is a
   Character function), feed its return into an IsValid check, and Branch on it.
   If it IS valid, a montage is already playing: do nothing, leave that path empty.
   Continue only on the NOT-valid path.

3. Second gate - is the Knife the selected item? Reproduce the same index logic the
   RefreshHeldItem function already uses:
     - Get SelectedSlot, subtract 1 -> Index
     - Get InventorySlots
     - Branch on ( Index >= 0 AND Index < Length(InventorySlots) )
     - On true: Get InventorySlots[Index] -> compare that Name to the literal "Knife"
       with a Name Equal node -> Branch
     - On false or on not-equal: do nothing, leave those paths empty.

4. On the path where the name equals "Knife": add a Play Montage node
   (the one with OnCompleted / OnBlendOut / OnInterrupted / OnNotifyBegin /
   OnNotifyEnd output pins - NOT Play Anim Montage).
   Wire:
     In Skeletal Mesh Component = the Mesh component (CharacterMesh0)
     Montage to Play           = the AttackMontage variable
     Play Rate                 = 1.0
     Starting Position         = 0.0
     Starting Section          = None
     Should Stop All Montages  = true
   Leave all five output execution pins unconnected for now.

Do not modify any existing node or connection anywhere else in the EventGraph.

Then compile the Blueprint and report the compiler output.
```

**명령 15 — 타격 판정**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, in the
EventGraph, extend the Play Montage node that was added for IA_Attack
(node K2Node_PlayMontage_0). Place the new nodes below it.

1. From that Play Montage node's OnNotifyBegin execution pin, run into a Branch.
   The Branch condition is a Name Equal node comparing the Play Montage node's
   NotifyName output pin against the literal Name "AttackHit".
   Leave the Branch's false path empty.

2. On the Branch's true path, add a "Sphere Trace For Objects" node
   (SphereTraceSingleForObjects - the single-hit version, NOT the multi version).
   Wire it as follows:
     Start          = Get Actor Location (self)
     End            = Get Actor Location (self) + ( Get Actor Forward Vector (self)
                        * the AttackRange variable )
     Radius         = the AttackTraceRadius variable
     Object Types   = an array with one entry: Pawn
     Trace Complex  = false
     Actors to Ignore = empty array
     Ignore Self    = true
     Draw Debug Type = For Duration
     Draw Time      = 2.0
   Leave the trace colour pins at their defaults.

3. From the trace node's execution output, run into a second Branch whose condition
   is the trace node's Return Value boolean.
   Leave that Branch's false path empty.

4. On that Branch's true path, add a Print String node.
   Its In String is an Append of the literal "Hit: " and the Get Display Name of
   the Hit Actor taken from breaking the trace node's Out Hit result.
   Leave Print String's other pins at their defaults.

Do not modify any existing node or connection anywhere else in the EventGraph.

Then compile the Blueprint and report the compiler output.
```

**옮기며 넣은 해석**

- 한글 지시에 "공격 키"가 없었다. **`LeftMouseButton`은 AI가 정했다.** 비어 있는 키였고 관례를 따랐다.
- 한글 지시에 매핑을 어느 IMC에 넣을지 없었다. **`IMC_Default`(인벤토리용 `IMC_Inventory`가 아니라)는 AI가 정했다.** 인벤토리와 무관한 상시 동작이라는 판단이다.
- `AttackRange 200` / `AttackTraceRadius 40` / `Knife`의 `heldTransform` 값 / `iconColor (0.7, 0.7, 0.75)` / 픽업 위치 `(300, 0, 20)` / 액터 이름 `Knife_Pickup` / 몽타주 이름 `AM_Player_Attack` / 노티파이 이름 `AttackHit` — **전부 AI가 정한 값이다.** 한글 지시에 없었다.
- 사용자가 고른 것은 "AnimNotify로 타격 창 열기"였는데, **AI가 "한 순간, 트레이스 1회"와 "구간, 매 프레임"으로 갈라 다시 물었고 사용자가 전자를 골랐다.** "창"이라는 단어와 실제 구현이 다르므로 여기 밝힌다.

## Terminal 결과

터미널 자체의 출력은 사용자가 옮겨 붙이지 않았다. **아래 원문은 전부 AI가 MCP 읽기 도구와 UE 출력 로그로 직접 받아온 것이다.** 즉 "명령이 뭐라고 답했는가"가 아니라 "실행 후 실제 상태가 어땠는가"다. 이 프로젝트의 규칙(응답을 성공 근거로 삼지 않는다)에 따른 것이지만, 그 결과 **터미널이 무슨 말을 했는지는 이 기록에 남아 있지 않다.**

### 원문 — English

**`DT_Items` — 네 행 최종 상태 (`get_rows`)**

```json
{"Key_Stage1": {"displayName": "NSLOCTEXT(\"[31D95D90E0F90A083145F5565E5C1688]\", \"8F5F203F44A1BCD3E6978C81511DDF35\", \"Rusty Key\")", "iconColor": {"R": 1, "G": 0.8, "B": 0.1, "A": 1}, "mesh": "/Script/Engine.StaticMesh'/Engine/BasicShapes/Cube.Cube'", "nature": "Key", "healAmount": 0, "heldTransform": {"Rotation": {"X": 0, "Y": 0, "Z": 0, "W": 1}, "Translation": {"X": 0, "Y": 0, "Z": 0}, "Scale3D": {"X": 0.15, "Y": 0.15, "Z": 0.15}}}, "Potion_Small": {"displayName": "NSLOCTEXT(\"[31D95D90E0F90A083145F5565E5C1688]\", \"CFAE3ED64F9FDF2DE10AD58645397397\", \"Small Potion\")", "iconColor": {"R": 0.9, "G": 0.1, "B": 0.1, "A": 1}, "mesh": "/Script/Engine.StaticMesh'/Engine/BasicShapes/Cylinder.Cylinder'", "nature": "Consumable", "healAmount": 25, "heldTransform": {"Rotation": {"X": 0, "Y": 0, "Z": 0, "W": 1}, "Translation": {"X": 0, "Y": 0, "Z": 0}, "Scale3D": {"X": 0.15, "Y": 0.15, "Z": 0.15}}}, "Ball_Test": {"displayName": "NSLOCTEXT(\"[31D95D90E0F90A083145F5565E5C1688]\", \"EADADC87491C210F62D3A291F87C296F\", \"Test Ball\")", "iconColor": {"R": 0.2, "G": 0.4, "B": 1, "A": 1}, "mesh": "/Script/Engine.StaticMesh'/Engine/BasicShapes/Sphere.Sphere'", "nature": "Holdable", "healAmount": 0, "heldTransform": {"Rotation": {"X": 0, "Y": 0, "Z": 0, "W": 1}, "Translation": {"X": 0, "Y": 0, "Z": 0}, "Scale3D": {"X": 0.15, "Y": 0.15, "Z": 0.15}}}, "Knife": {"displayName": "NSLOCTEXT(\"DT_Items [31D95D90E0F90A083145F5565E5C1688]\", \"Knife_DisplayName\", \"Knife\")", "iconColor": {"R": 0.7, "G": 0.7, "B": 0.75, "A": 1}, "mesh": "/Script/Engine.StaticMesh'/Engine/BasicShapes/Cube.Cube'", "nature": "Holdable", "healAmount": 0, "heldTransform": {"Rotation": {"X": 0, "Y": 0, "Z": 0, "W": 1}, "Translation": {"X": 0, "Y": 0, "Z": 0}, "Scale3D": {"X": 0.04, "Y": 0.04, "Z": 0.5}}}}
```

**MCP 읽기 실패 — 전문**

```
GetObjectProperties on '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C:HeldItemMesh_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be read: AttachSocketName
```

```
GetObjectProperties on '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C:HeldItemMesh_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be read: CollisionEnabled
```

```
GetObjectProperties on '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C:HeldItemMesh_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be read: attachParent
```

```
GetObjectProperties on '/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Enemy_Attack.AM_Enemy_Attack' (AnimMontage): the following properties could not be read: Notifies
```

```
GetObjectProperties on '/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack' (AnimMontage): the following properties could not be read: bEnableRootMotionTranslation, bEnableRootMotionRotation
```

```
GetObjectProperties on '/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01.MM_Attack_01' (AnimSequence): the following properties could not be read: bRootMotionSettingsCopiedFromMontage
```

```
Parameter error: /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C:Default__BP_ThirdPersonCharacter_C is not valid Actor for property 'actor'.
```

```
Unknown tool editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools.get_socket_names
```

```
Function "CaptureViewport", input param "captureTransform" needs a default value.Function input params Json -
{}
```

```
Function "CaptureViewport", input param "annotations" needs a default value.Function input params Json -
{"captureTransform":{"location":{"x":590.20000000000005,"y":1541.9000000000001,"z":122},"rotation":{"pitch":0,"yaw":171,"roll":0},"scale":{"x":1,"y":1,"z":1}},"bShowUI":false}
```

```
Material slot "Material0" not found on Cube.
```

**소켓 확인 — PIE 콘솔 `GetAll` 출력**

```
[2026.09.01-03.53.02:395][560]Cmd: GetAll StaticMeshComponent AttachSocketName Name=HeldItemMesh
[2026.09.01-03.53.02:402][560]0) StaticMeshComponent /Engine/Transient.World_1:PersistentLevel.BP_ThirdPersonCharacter_C_7.HeldItemMesh.AttachSocketName = HandGrip_R
[2026.09.01-03.53.02:402][560]1) StaticMeshComponent /Engine/Transient.World_0:PersistentLevel.BP_ThirdPersonCharacter_C_0.HeldItemMesh.AttachSocketName = HandGrip_R
[2026.09.01-03.53.02:402][560]2) StaticMeshComponent /Game/ThirdPerson/UEDPIE_0_Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_ThirdPersonCharacter_C_0.HeldItemMesh.AttachSocketName = HandGrip_R
```

**노티파이 이동 취소 흔적**

```
[2026.09.01-05.13.21:503][ 61]LogEditorTransaction: Undo Move Anim Notifies
[2026.09.01-05.13.23:519][156]LogEditorTransaction: Undo Move Anim Notifies
```

**`RefreshHeldItem` 최종 그래프 (`read_graph_dsl`)**

```
(fn RefreshHeldItem ()
  (bind _selectedslot (Variables|Default|GetSelectedSlot))
  (bind _returnvalue (- _selectedslot 1))
  (bind _inventoryslots (Variables|Default|GetInventorySlots))
  (bind _output (Utilities|Array|Get(acopy) _inventoryslots _returnvalue))
  (bind _helditemmesh (Variables|Default|GetHeldItemMesh))
  (if (and (>= _returnvalue 0) (< _returnvalue (Utilities|Array|Length _inventoryslots)))
    (if (Utilities|Name|Equal(Name) _output "")
      (Components|StaticMesh|SetStaticMesh _helditemmesh)
      (else
        (bind _returnvalue_1 (Utilities|GetDataTableRowDT_Items "/Game/Inventory/DT_Items.DT_Items" _output)
          (:then
            (Components|StaticMesh|SetStaticMesh _helditemmesh (Utilities|Struct|BreakSItemDef _returnvalue_1))
            (Transformation|SetRelativeTransform _helditemmesh (Utilities|Struct|BreakSItemDef _returnvalue_1)))
          (:RowNotFound
            (Components|StaticMesh|SetStaticMesh _helditemmesh)))))
    (else
      (Components|StaticMesh|SetStaticMesh _helditemmesh))))
```

**`AM_Player_Attack` 최종 상태**

```json
{"SlotAnimTracks":[{"slotName":"DefaultSlot","animTrack":{"animSegments":[{"cachedPlayLength":1,"animReference":{"refPath":"/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01.MM_Attack_01"},"startPos":0,"animStartTime":0,"animEndTime":1,"animPlayRate":1,"loopingCount":1}]}}],"SequenceLength":1,"BlendIn":{"customCurve":"None","blendTime":0.25,"blendOption":"HermiteCubic"},"BlendOut":{"customCurve":"None","blendTime":0.25,"blendOption":"HermiteCubic"}}
```

**`MM_Attack_01` 루트 모션**

```json
{"bEnableRootMotion":true,"RootMotionRootLock":"RefPose","bForceRootLock":false}
```

**`BP_ThirdPersonCharacter` CDO 기본값**

```json
{"AttackMontage":{"refPath":"/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack"},"AttackRange":200,"AttackTraceRadius":40,"RespawnDelay":2,"MaxHP":100,"InteractDistance":800}
```

**`IA_Attack` 최종 상태**

```json
{"ValueType":"Boolean","Triggers":[],"Modifiers":[],"bConsumeInput":true,"bTriggerWhenPaused":false,"ActionDescription":""}
```

**`IMC_Default` 새 매핑 (14번째 항목만 발췌 — 앞 13개는 명령 전 값과 동일함을 대조 확인)**

```json
{"triggers":[],"modifiers":[],"action":{"refPath":"/Game/Input/Actions/IA_Attack.IA_Attack"},"key":"LeftMouseButton","settingBehavior":"InheritSettingsFromAction","playerMappableKeySettings":"None"}
```

**컴파일 로그 — `LogBlueprint`의 경고 (발췌, 같은 형태가 수십 줄)**

```
[2026.09.01-06.39.29:050][129]LogBlueprint: Warning: No then pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_CallFunction_10
[2026.09.01-06.39.29:050][129]LogBlueprint: Warning: No then pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_PromotableOperator_15
[2026.09.01-06.39.29:051][129]LogBlueprint: Warning: No execute pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_Event_3
```

**에디터 설정 저장 실패 — 전문 (블루프린트와 무관)**

```
[2026.09.01-06.17.47:627][ 51]LogFileManager: Warning: MoveFile was unable to move 'D:/20260827/MCP1/Saved/EditorPerProjectUserSettingsF435939641B00D6294379B8803004E71.tmp' to 'D:/20260827/MCP1/Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini' (Error Code 183), retrying in .5s...
[2026.09.01-06.17.52:636][ 51]LogFileManager: Error: Error moving file 'D:/20260827/MCP1/Saved/EditorPerProjectUserSettingsF435939641B00D6294379B8803004E71.tmp' to 'D:/20260827/MCP1/Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini'.
```

**MCP 서버 에러 — 전문**

```
[2026.09.01-00.15.48:926][596]LogModelContextProtocol: Error: Call to unknown method "server/discover"
```

### 요약 — 한글

- `DT_Items`에 `Knife` 행이 생겼다. `nature = Holdable`, `mesh = /Engine/BasicShapes/Cube.Cube`.
- `S_ItemDef`에 `HeldTransform`(Transform) 칸이 생겼다. 네 행 모두 값이 채워졌다. 기존 3행은 `Scale3D (0.15, 0.15, 0.15)`, `Knife`는 `(0.04, 0.04, 0.5)`.
- `RefreshHeldItem`에 `Transformation|SetRelativeTransform` 노드 하나가 `SetStaticMesh` 뒤에 붙었다. `BreakSItemDef`의 출력 5번(`HeldTransform_17_...`)이 `NewTransform`에 물렸다.
- `HeldItemMesh`의 부모가 `CollisionCylinder` → `CharacterMesh0`으로 바뀌고 소켓이 `HandGrip_R`로 지정됐다. 상대 트랜스폼은 전부 영, 스케일은 `0.15`.
- `AM_Player_Attack`이 `AM_Enemy_Attack`의 복제로 생겼다. 최종적으로 `MM_Attack_01`을 쓴다.
- `IA_Attack`(`InputAction`)이 생기고 `IMC_Default`에 `LeftMouseButton`으로 매핑됐다. 기존 13개 매핑은 그대로다.
- `BP_ThirdPersonCharacter`에 `AttackMontage` / `AttackRange` / `AttackTraceRadius` 세 변수가 생겼다. CDO 기본값 `AM_Player_Attack` / `200` / `40`.
- EventGraph에 `IA_Attack [Triggered]` → `GetCurrentMontage` + `IsValid` → 슬롯 경계 `Branch` → `Name Equal "Knife"` `Branch` → `Play Montage` 체인이 생겼다.
- 그 뒤로 `OnNotifyBegin` → `Name Equal "AttackHit"` `Branch` → `Collision|SphereTraceForObjects` → `Branch` → `Print String` 체인이 붙었다.
- 레벨에 `Knife_Pickup`(`BP_ItemPickup`) 액터가 `(300, 0, 20)`에 배치됐다.

## 분석

### 무엇을 만들었나

**데이터**

- `DT_Items` 신규 행 `Knife` — `displayName "Knife"`, `iconColor (0.7, 0.7, 0.75, 1)`, `mesh /Engine/BasicShapes/Cube.Cube`, `nature Holdable`, `healAmount 0`, `heldTransform` 위치·회전 영 / `Scale3D (0.04, 0.04, 0.5)`
- `S_ItemDef` 신규 칸 `HeldTransform` (Transform) — 사용자가 구조체 에디터에서 손으로 추가
- 기존 3행(`Key_Stage1`, `Potion_Small`, `Ball_Test`)의 `heldTransform` — 전부 위치·회전 영 / `Scale3D (0.15, 0.15, 0.15)`

**입력**

- `IA_Attack` — `/Game/Input/Actions/`, `ValueType Boolean`, `Triggers []`, `Modifiers []`, `bConsumeInput true`, `bTriggerWhenPaused false`
- `IMC_Default`의 14번째 매핑 — `IA_Attack` / `LeftMouseButton` / `InheritSettingsFromAction` / 모디파이어 없음

**애니메이션**

- `AM_Player_Attack` — `AM_Enemy_Attack`의 복제. `DefaultSlot`, `MM_Attack_01`, `0~1`, `animPlayRate 1`, `SequenceLength 1.0`, `BlendIn`/`BlendOut` 각 `0.25` `HermiteCubic`
- 그 안의 `Montage Notify` 하나 — `Notify Name = AttackHit`. 사용자가 몽타주 에디터에서 손으로 찍음

**컴포넌트**

- `HeldItemMesh` — 부모 `CharacterMesh0`, 소켓 `HandGrip_R`, `RelativeLocation (0,0,0)`, `RelativeRotation (0,0,0)`, `RelativeScale3D (0.15, 0.15, 0.15)`. 부모와 소켓은 사용자가 컴포넌트 패널에서 손으로 바꿈, 트랜스폼은 명령 3으로 영으로 되돌림

**변수** (전부 `BP_ThirdPersonCharacter`, 인스턴스 편집 켜짐, 카테고리 `Default`)

- `AttackMontage` (AnimMontage 참조) = `AM_Player_Attack`
- `AttackRange` (Float) = `200`
- `AttackTraceRadius` (Float) = `40`

**함수 그래프**

- `RefreshHeldItem` — `Row Found` 분기에 `SetRelativeTransform(HeldItemMesh, BreakSItemDef.HeldTransform)` 한 단계 추가. 나머지 세 분기는 손대지 않음

**이벤트 그래프**

```
IA_Attack [Triggered]
  → GetCurrentMontage(self) → IsValid
       Is Valid     : 미연결
       Is Not Valid → Branch  ( (SelectedSlot-1) >= 0  AND  (SelectedSlot-1) < Length(InventorySlots) )
       then → Branch  ( Name Equal( InventorySlots[SelectedSlot-1], "Knife" ) )
       then → Play Montage ( Mesh, AttackMontage, rate 1.0, pos 0.0, section None, stopAll true )
                OnNotifyBegin → Branch ( Name Equal( NotifyName, "AttackHit" ) )
                  then → Sphere Trace For Objects
                           Start  = GetActorLocation(self)
                           End    = GetActorLocation(self) + GetActorForwardVector(self) * AttackRange
                           Radius = AttackTraceRadius
                           ObjectTypes = [ObjectTypeQuery3 = Pawn]
                           bTraceComplex false / ActorsToIgnore [] / bIgnoreSelf true
                           DrawDebugType ForDuration / DrawTime 2.0
                  → Branch ( trace.ReturnValue )
                    then → Print String ( Append("Hit: ", GetDisplayName(BreakHitResult(OutHit).HitActor)) )
                             screen true / log true / duration 2.0
```

**레벨**

- `Knife_Pickup` — `BP_ItemPickup`, `(300, 0, 20)`, 회전 영, 스케일 1, `ItemRow = DT_Items:Knife`. 외부 액터 패키지 `Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/2/ZZ/MKTX9I9EXQ7VT5OCJ0B901.uasset`로 떨어짐

### 기술적으로 맞게 짚은 부분

**`HeldScale`(Vector) 대신 `HeldTransform`(Transform)으로 바꾼 것.**
처음 사양은 크기만 담는 칸이었다. `HandGrip_R` 소켓이 `hand_r` 기준 `(-7.012, 2.049, 0.00003)` / `yaw 90`에 있고 **무기의 피벗을 얹으라고 만들어진 자리**라, 피벗이 정중앙인 큐브는 크기만으로 자세를 못 맞춘다. 위치·회전이 같이 필요하다. 칸을 셋으로 늘리는 대신 Transform 하나로 간 것은 **나중에 진짜 칼 메시가 왔을 때 피벗이 어디에 있든 그 한 칸으로 흡수된다**는 뜻이다. 칸 수도 노드 수도 안 늘었다.

**`GetCurrentMontage` + `IsValid`로 연타를 막은 것.**
`Character.h:897`에 `UFUNCTION(BlueprintCallable, Category=Animation) UAnimMontage* GetCurrentMontage() const`가 있다. 캐릭터가 직접 주므로 `Mesh → GetAnimInstance → IsAnyMontagePlaying` 세 단계가 두 단계로 준다. **새 `bIsAttacking` 불리언을 만들지 않은 것이 핵심이다** — 상태를 따로 들면 그걸 켜고 끄는 자리가 늘고, 몽타주가 중단됐을 때 꺼주는 걸 잊으면 영원히 공격 못 하는 버그가 된다. 엔진이 이미 들고 있는 상태를 읽으면 그 부류가 통째로 사라진다.

**사망 중 공격 차단이 공짜로 딸려온 것.** 사망 몽타주가 도는 동안 `GetCurrentMontage`가 유효하므로 공격이 안 나간다. 따로 만든 게 아니라 위 선택의 부산물이다.

**이름 노티파이가 아니라 `Montage Notify`를 쓴 것.**
`AnimInstance.cpp:2070`의 주석이 `// Custom Event based notifies. These will call a AnimNotify_* function on the AnimInstance.`다. **이름만 붙인 노티파이는 `ABP_Unarmed`에서 `AnimNotify_AttackHit`을 찾는다.** 캐릭터 블루프린트가 아니다. 처음 사양은 이 방식이었고 그대로 갔으면 이벤트가 안 불렸다.
`AnimNotify_PlayMontageNotify.cpp:30`이 `AnimInstance->OnPlayMontageNotifyBegin.Broadcast(NotifyName, ...)`를 부르고, `PlayMontageCallbackProxy.cpp:68`이 그걸 받는다. 그래서 `Play Montage` 노드의 `OnNotifyBegin` 핀이 **캐릭터 블루프린트에서 직접** 뜬다. **`ABP_Unarmed`를 안 건드렸다는 게 진짜 이득이다** — 그건 `BP_Enemy`와 공유되는 애셋이다.

**채널 트레이스가 아니라 `SphereTraceForObjects` + `Pawn`을 쓴 것.**
시작점이 액터 위치(캡슐 중심, 발에서 92cm)이고 앞으로 200cm를 쏜다. `Visibility` 채널로 쐈으면 벽·바닥·칼 픽업을 먼저 물고 끝났을 것이다. 오브젝트 타입을 `Pawn`으로 한정하면 그 부류가 통째로 안 생긴다. `bIgnoreSelf = true`가 없으면 자기 캡슐을 첫 히트로 잡는다.

**`IMC_Default`의 기존 13개 매핑을 명령문에 전부 나열한 것.**
배열을 통째로 다시 쓰는 명령이었고, 그 안에 `InputModifierSwizzleAxis_3`, `InputModifierNegate_0` 같은 오브젝트 참조가 열 개 넘게 들어 있었다. **하나라도 날아가면 이동이 조용히 망가진다 — 컴파일 에러가 안 난다.** 명령에 개수와 이름을 박아두고 실행 후 14개를 하나씩 대조했다.

**`BP_ThirdPersonCharacter`에 인스턴스 리셋 단계를 안 넣은 것.**
직전 기록의 규칙은 "`BP_Enemy`에 변수를 추가하는 명령에는 배치 인스턴스를 `reset_properties`로 리셋하는 단계를 같이 넣는다"였다. **이번엔 안 넣은 것이 맞다.** `find_actors`로 확인한 결과 `BP_ThirdPersonCharacter`는 레벨에 배치된 인스턴스가 없다. 플레이어는 `PlayerStart`에서 런타임 스폰된다. 규칙을 기계적으로 적용하지 않고 전제를 확인했다.

**`AttackMontage`를 CDO에 박은 것.**
`BP_Enemy`는 지금 CDO의 `AttackMontage`가 `None`이고 배치된 `Enemy_Test` 인스턴스에만 값이 있다. 같은 모양을 반복하지 않으려고 명령에 CDO 설정을 명시했다.

**`MM_Attack_02`로 갈랐다가 되돌린 것.**
적과 플레이어 동작을 구분하려는 시도였고, 왼손 지르기라 칼 든 오른손과 안 맞았다. `MM_Attack_03`은 발차기였다. **원래 사양에 적혀 있던 `MM_Attack_01`로 돌아온 것이 옳다.** 사양의 「만들지 않는 것」에 "칼 전용 애니메이션 — 맨손 시퀀스 `MM_Attack_01`을 그대로 쓴다"가 이미 있었다.

**막대 방향을 회전이 아니라 스케일 축으로 실험한 것.**
`HandGrip_R`이 이미 `yaw 90`으로 돌아가 있어서, 추측한 회전값을 넣으면 결과를 봐도 왜 그런지 알 수 없다. 스케일 축만 바꾸면 결과가 "그 축이 칼날 방향이다/아니다" 하나만 말해준다.

### 확인한 것 / 확인 못 한 것

**확인한 것** (PIE 또는 에디터 실제 상태를 다시 읽은 것)

- 합격 기준 1 — 칼 픽업에 다가가 `F`로 줍고 슬롯을 고르면 오른손에 길쭉한 막대가 붙는다. PIE 3인칭·1인칭 양쪽에서 봄
- 합격 기준 2 — 칼을 든 채 `LMB`를 누르면 공격 몽타주가 재생되고, `V`로 1인칭으로 바꿔도 같은 동작이 보인다
- 합격 기준 3 — 적을 정면 200cm 안에 두고 `LMB`를 누르면 `Hit: <적 이름>`이 한 번 출력된다. 초록 트레이스가 그려지고, 안 맞으면 빨간 트레이스만 그려진다
- 합격 기준 4 — 빈 슬롯이나 `Knife`가 아닌 아이템을 든 채 `LMB`를 누르면 아무 일도 일어나지 않는다
- 공격 중 `LMB` 연타 시 동작이 처음부터 다시 시작되지 않는다
- 기존 아이템(`Potion_Small`, `Ball_Test`)의 손에 든 크기가 `HeldTransform` 도입 후에도 안 변했다
- `HeldItemMesh.AttachSocketName = HandGrip_R` — PIE 콘솔 `GetAll` 출력으로 확인
- `HeldItemMesh`의 부모가 `CharacterMesh0` — PIE 인스턴스와 에디터 템플릿 양쪽에서 `get_parent_component`
- `IMC_Default`의 기존 13개 매핑이 명령 후에도 순서·키·모디파이어 참조까지 동일
- `AM_Enemy_Attack`이 명령 7·8·10을 거치는 동안 한 번도 안 바뀜
- `IA_Attack`의 모든 프로퍼티가 `IA_Interact`와 동일
- CDO의 `RespawnDelay 2` / `MaxHP 100` / `InteractDistance 800`이 안 바뀜
- `MM_Attack_01.bEnableRootMotion = true` — 공격 중 전진의 원인
- `BP_Enemy`의 공격이 `PlayAnimMontage → ApplyDamage → Delay` 순서이고 히트 판정이 없음
- `BP_Enemy`도 `ABP_Unarmed`를 쓴다
- 모든 노드의 핀 연결 — `get_node_infos`로 명령 5·14·15의 결과를 핀 단위로 대조

**확인 못 한 것** (이유 포함)

- **`AttackHit` 노티파이가 몽타주의 몇 초 지점에 있는가.** MCP가 `Notifies` 프로퍼티를 못 읽는다 — `AnimSequenceBase.h:42`의 선언이 `EditAnywhere`도 `VisibleAnywhere`도 없는 맨 `UPROPERTY()`다. 콘솔 `GetAll AnimMontage Notifies Name=AM_Player_Attack`을 안내했으나 실행되지 않았다. 로그에 `Undo Move Anim Notifies`가 두 번 찍혀 있어 **처음 위치(약 0.03초)로 돌아가 있을 가능성이 있다**
- **노티파이의 클래스가 정말 `Montage Notify`인지.** Details에 `Notify Name` 칸이 있었고 표식이 점 하나였다는 화면 근거뿐이다. 다만 PIE에서 `OnNotifyBegin`이 실제로 떴으므로 **동작으로는 확인된 셈**이다
- **`HeldItemMesh`의 `CollisionEnabled` 설정.** `get_properties`가 못 읽는다
- **막대의 긴 축(`Z`)이 손 기준 어느 방향인지.** `Z`와 `X` 둘 다 봤고 둘 다 팔 방향이 아니었다. `Y`는 안 해봤다
- **뛰면서 공격했을 때의 모양.** 상하체 분리 필요성의 근거가 될 관찰인데 안 봤다
- **`MM_ChargedAttack`이 어떤 동작인지.** 유일하게 안 열어본 공격 시퀀스다
- **상하체 분리가 실제로 루트 모션을 죽이는지.** 엔진 소스(`AnimNode_LayeredBoneBlend.cpp:155, 181-192, 205`)를 읽고 그렇게 된다고 판단했으나 **PIE에서 본 것이 아니다**
- **터미널이 각 명령에 뭐라고 답했는지.** 출력을 옮겨 받지 않았다. 검증은 전부 MCP 재읽기로 했다

### 남는 리스크

- **`AttackHit` 노티파이가 0.03초에 있으면 휘두르기 전에 판정이 나간다.** 심문에서 `AnimNotify`를 고른 이유가 "데미지가 애니메이션의 타격 순간보다 먼저 들어가는 것"을 피하려는 것이었는데, 위치가 이르면 안 고른 쪽과 결과가 같아진다. 동작 자체는 정상이다
- **공격 중 캐릭터가 앞으로 이동한다.** `MM_Attack_01`의 `bEnableRootMotion = true` 때문이다. 오늘 만든 것이 아니라 애니메이션에 원래 켜져 있던 성질이다
- **전신 몽타주라 휘두르는 동안 하체 동작이 덮인다.** 뛰면서 공격하면 다리가 멈춘 것처럼 보일 것으로 예상되나 안 봤다
- **칼이 맨손 주먹질 애니메이션으로 나간다.** 사양의 「만들지 않는 것」에 이미 있던 항목이다
- **막대가 손 한가운데를 가로질러 뻗는다.** 큐브의 피벗이 정중앙이고 오프셋을 안 넣었다. `heldTransform`의 `location`에 `(0, 0, ±25)`를 넣으면 손잡이 끝을 쥔 모양이 되지만 부호를 안 정했다
- **적과 플레이어가 같은 동작(`MM_Attack_01`)을 한다.** 갈랐다가 되돌렸다. 화면에서는 플레이어가 칼을 들고 있어 구분은 된다
- **`Knife`와 `Key_Stage1`이 같은 `Cube` 메시를 쓴다.** `HeldTransform`이 달라 크기로는 구분되지만 색이 같다
- **디버그 표시가 하나 늘었다.** `SphereTraceForObjects`의 `DrawDebugType = ForDuration`, `DrawTime 2.0`. 기존 `PrintString` 10개 + `ToString(Float)` 3개에 더해진다
- **플레이어는 `PrintString`만 하고 적은 `ApplyDamage`를 한다.** 데미지 파이프라인이 한쪽만 제대로 돼 있다
- **`S_ItemDef` 변경으로 `BP_ItemPickup`과 `BP_ThirdPersonHUD`가 dirty가 됐다.** 직접 건드리지 않았고 재직렬화된 것이다. 내용이 실제로 안 바뀌었는지는 바이너리라 못 읽는다
- **칼 픽업이 100cm 큐브라 바닥에 30cm 파묻힌다.** 기존 픽업 6개도 같은 상태다
- **`MM_Attack_02`와 `MM_Attack_03`을 열어보느라 왕복이 두 번 늘었다.** 어느 손으로 치는지 안 보고 고른 결과다

### 총평

요청은 "칼을 넣고 공격을 만든다"였고 합격 기준 4개를 다 채웠다. 범위대로 적은 안 죽고, 맞았다는 사실만 화면에 뜬다.

**실질적인 난이도는 공격 로직이 아니라 두 가지였다.**

첫째는 **기존 인벤토리가 실제로 어디까지 되어 있었는가**였다. `HeldItemMesh`가 있고 `RefreshHeldItem`이 메시를 꽂고 있어서 "붙이는 구조는 다 있다"고 사양에 적었는데, **붙는 자리가 캡슐이었다.** 아이템이 손이 아니라 골반에 떠 있었고 3인칭에서는 카메라가 뒤에 있어 지금까지 안 보였다. 이번 세션 시간의 상당 부분이 여기 갔다. 사양 단계에서 `AttachSocketName`을 못 읽는다고 단서를 달아둔 게 그대로 터진 셈이다.

둘째는 **MCP가 못 하는 일이 예상보다 많았다**는 것이다. 구조체 칸 추가, 컴포넌트 부모/소켓 지정, 노티파이 찍기 — 셋 다 수작업이었다. 그리고 그때마다 UI 경로를 짐작하지 않고 엔진 소스에서 확인해야 했다. `Parent Socket` 버튼이 아무 반응 없던 것(`OnBrowseSocket`이 부모의 `HasAnySockets()`가 거짓이면 조용히 리턴)과, 노티파이 메뉴의 `New Notify...`와 `Montage Notify`가 다른 것 — 둘 다 소스를 안 봤으면 못 잡았다.

**사양을 두 번 고쳤고 둘 다 구현 전에 잡혔다.** `HeldScale` → `HeldTransform`, 이름 노티파이 → `Montage Notify`. 후자는 그대로 갔으면 이벤트가 아예 안 불리는 종류였다.

**헛짚은 것이 셋 있다.** 성공 확인 문구를 "`FirstPersonMesh`와 같은 깊이"라고 애매하게 써서 사용자가 자식으로 넣은 것, 어느 손인지 안 보고 `MM_Attack_02`로 갈랐다가 되돌린 것, `CaptureViewport`로 PIE 화면을 찍으려다 에디터 월드가 나온 것.

## AI의 제안

1. **`HeldScale`(Vector) 대신 `HeldTransform`(Transform)으로 칸을 만들자**
   > `S_ItemDef`에 `HeldTransform` (Transform) 한 칸. `RefreshHeldItem`에 `SetRelativeTransform` 한 단계.

   얻는 것 — 진짜 칼 메시가 왔을 때 피벗이 어디에 있든 `DT_Items` 한 행 수정으로 흡수된다. 잃는 것 — 없다. 칸 수와 노드 수가 같다.

2. **플레이어 몽타주를 `MM_Attack_02`로 갈라 적과 구분하자**
   > `AM_Player_Attack`의 `animReference`를 `MM_Attack_02`로. 비용이 같고 합격 기준 3 확인 때 누가 휘둘렀는지 눈으로 구분된다.

   얻는 것 — 화면에서 적·플레이어 동작 구분. 잃는 것 — **어느 손으로 치는지 확인하지 않고 꺼낸 제안이었다.** 왼손 지르기였고 되돌리는 데 왕복 두 번이 들었다.

3. **채널 트레이스 대신 `SphereTraceForObjects` + `Pawn`을 쓰자**
   > 사양에는 "SphereTrace"라고만 적혀 있었다. `Visibility` 채널로 쏘면 벽·바닥·픽업이 먼저 걸린다.

   얻는 것 — 시작점이 캡슐 중심이라 앞에 벽이 있으면 매번 벽을 무는 문제가 통째로 사라진다. 잃는 것 — 폰이 아닌 대상은 영원히 못 때린다. 파괴 가능한 오브젝트가 생기면 타입을 추가해야 한다.

4. **`AttackHit` 노티파이를 오른손이 가장 뻗은 프레임으로 옮기자**
   > 지금 프레임 1(약 0.03초)에 있다. 그러면 `LMB`를 누르는 순간 곧바로 판정이 나가 안 고른 선택지와 결과가 같아진다.

   얻는 것 — `AnimNotify`를 고른 이유가 살아난다. 잃는 것 — 없다. 표식을 끌어다 놓는 것뿐이다.

5. **지금은 상하체 분리를 만들지 말자**
   > 미리 해도 나중에 하는 것보다 안 싸진다. `ABP_Unarmed`의 AnimGraph에 블렌드 노드 하나 끼우고 몽타주의 `slotName`을 바꾸는 독립적인 변경이라, 오늘 무엇을 만들어두든 그때 드는 비용이 같다.

   얻는 것 — 공유 애셋(`BP_Enemy`가 같이 쓴다)을 필요해지기 전에 안 건드린다. 잃는 것 — 없다. 다만 **사용자가 이후 루트 모션 전진을 관찰해 만들 근거가 생겼다.**

6. **뛰면서 `LMB`를 눌러보자**
   > 만드는 것과 알아보는 것은 다르다. 전신 몽타주라 다리가 멈춘 것처럼 보일 텐데, 그게 얼마나 거슬리는지가 상하체 분리의 필요성을 정한다.

   얻는 것 — 공짜로 얻는 판단 근거. 잃는 것 — 없다.

## 다음으로 넘김

**바로 이어서 할 것**

- **`AttackHit` 노티파이 위치 확인과 이동.** 콘솔에 `GetAll AnimMontage Notifies Name=AM_Player_Attack`을 넣으면 실제 시각이 로그에 찍힌다. 프레임 1에 있으면 오른손이 가장 뻗은 프레임으로 옮긴다. **MCP는 `Notifies`를 못 읽으므로 콘솔이 유일한 확인 수단이다**
- **뛰면서 `LMB` 눌러보기.** 상하체 분리 사양을 쓰기 전에 있어야 할 관찰이다
- **`AttackMontage`·`AttackRange`·`AttackTraceRadius`의 인스턴스 편집 표시 확인.** My Blueprint 패널의 눈 아이콘. **`list_variables`가 이름만 돌려주고 `set_variable_instance_editable`은 있는데 get이 없다 — AI가 읽을 수단이 없음이 이번에 확정됐다.** `BP_Enemy`의 앞선 변수 넷 + `RespawnDelay` + `SightHalfAngle`도 같은 상태로 이월 — 합쳐서 아홉 개다

**정해진 것**

- **상하체 분리는 플레이어만 한다. 적은 지금처럼 전신 몽타주로 둔다.** (기록 직후 사용자가 정함)
  - `AM_Player_Attack`의 `slotName`만 `DefaultSlot` → `UpperBody`로 바꾼다. `AM_Enemy_Attack`은 손대지 않는다
  - `ABP_Unarmed`의 AnimGraph에서 `Slot 'DefaultSlot'`의 출력이 `LayeredBoneBlend`의 base pose로 들어가므로 **적은 지금과 완전히 같은 결과를 받는다**
  - **따라오는 결과 — 적은 공격 중 루트 모션 전진을 그대로 유지한다.** 플레이어만 안 밀린다. 적이 달려들며 치는 모양이 되므로 문제로 보이지 않지만, 의도한 것이 아니라 이 결정에 딸려온 것이다
  - 적은 공격 중 다리도 계속 멈춘다. 적은 공격할 때 제자리에 서므로 티가 안 날 것으로 보이나 **확인 안 함**

**결정 필요**

- **`UpperBody` 슬롯 이름을 스켈레톤에 등록하는 것.** `SK_Mannequin`은 프로젝트 전체가 공유하는 애셋이다
- **칼 손잡이 오프셋.** `heldTransform.location`에 `(0, 0, 25)` 또는 `(0, 0, -25)`. 부호는 PIE에서 봐야 안다
- **디버그 표시 제거 시점.** `PrintString` 10개 + `ToString(Float)` 3개 + 이번에 늘어난 `DrawDebugType ForDuration` 하나
- **`RETURN` 분기도 비래턴트로 바꿀 것인가.** 복귀 중 감지 주기가 홉 하나(약 6.4초)다
- **복귀 속도를 되돌릴 것인가.** 초당 45. 앞서 `그대로두자`로 정했으므로 거슬릴 때만 다시 꺼낸다
- **칸막이 `SM_Cube2`를 `Divider_L`로 리네임할 것인가.** 짝이 `SM_Cube2` / `Divider_R`로 어긋나 있다

**확인 필요**

- **상하체 분리가 실제로 루트 모션을 죽이는지.** 소스로는 `AnimNode_LayeredBoneBlend.cpp`의 `RootMotionClearWeight` 경로가 그렇게 되지만 PIE에서 안 봤다
- **`MM_ChargedAttack`이 어떤 동작인지.** 유일하게 안 열어본 공격 시퀀스다
- **막대의 긴 축 `Y`는 어느 방향인지.** `Z`·`X`는 봤고 둘 다 팔 방향이 아니었다
- **`BP_Enemy`가 왜 `BP_ThirdPersonCharacter` 컴파일에 딸려 dirty가 되는지.** 참조 사슬이 안 보인다
- **재직렬화된 `.uasset`들의 내용이 실제로 안 바뀌었는지.** 바이너리라 못 읽는다
- **`LogCrowdFollowing: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance`.** PIE 종료 무렵마다 나온다
- **`LogModelContextProtocol: Error: Call to unknown method "server/discover"`.** 세션 시작 무렵 한 번 찍힌다
- **`EditorPerProjectUserSettings.ini` 저장 실패 (`Error Code 183`).** 열 번 재시도 후 최종 실패했다. 에디터 설정이 저장 안 되고 있을 수 있다
- **`read_graph_dsl`과 `write_graph_dsl`의 id 체계가 다른 이유.** 누적 세 종류
- **`find_node_types`와 `get_node_type_pins`의 type_id 표기가 다른 이유.** `SimpleMovetoActor` / `SimpleMoveToActor`
- **MCP 읽기/쓰기 모양 비대칭.** `heldTransform`은 쓸 때 `location/rotation/scale`, 읽을 때 `Translation/Rotation(쿼터니언)/Scale3D`. `key`는 쓸 때 `{keyName: "..."}`, 읽을 때 평문자열. **`read/write_graph_dsl` id 불일치와 같은 부류로 보인다**
- **`CaptureViewport`가 PIE 화면이 아니라 에디터 월드를 렌더하는 것.** PIE 중에 찍었는데 빈 방이 나왔다
- **MCP가 못 읽는 프로퍼티 목록.** `AttachSocketName`, `attachParent`, `CollisionEnabled`, `Notifies`, `bEnableRootMotionTranslation`, `bEnableRootMotionRotation`, `bRootMotionSettingsCopiedFromMontage`. **공통점은 `EditAnywhere`/`VisibleAnywhere`가 없는 `UPROPERTY()`로 보이나 전부 확인한 것은 아니다**
- **`Knife`의 `displayName` NSLOCTEXT 네임스페이스가 기존 행과 다른 이유.** 기존은 `"[GUID]"` + GUID 키, `Knife`는 `"DT_Items [GUID]"` + `"Knife_DisplayName"` 키. **MCP로 만든 텍스트와 손으로 만든 텍스트의 형식이 다르다**
- **복귀가 초당 45로 느려진 진짜 원인.** `AcceptanceRadius 0` 가설만 있다
- **`DisableInput`이 Enhanced Input 매핑까지 막는지**
- **HUD의 `CachedCharacter` 재획득이 실제로 일어나는지**
- **2번 방의 조명.** `DirectionalLight`·`SkyLight` 외에 아무것도 없다
- **`bCanEverTick`이 명령 56 직후 `false`로 읽혔던 이유**
- **`trace_world`가 방향에 따라 같은 솔리드를 놓치는 이유**
- **`show navigation`이 PIE에서 안 먹는 이유.** 에디터 뷰포트의 `P`로 우회했다
- **외부 액터 패키지와 `__ExternalObjects__` 파일의 정체.** 이번에 `Knife_Pickup`이 `.../2/ZZ/MKTX9I9EXQ7VT5OCJ0B901.uasset`로 하나 더 늘었다
- **`Lvl_ArenaShooter`의 WorldSettings가 `BP_ShooterGameMode`를 가리키는지.** `.umap`이 바이너리라 못 읽었다

**접어둔 것**

- **적 HP·피격·사망.** 다음 사양의 본체다. 만들 때 **플레이어의 `PrintString`을 `ApplyDamage`로 올려야 적과 짝이 맞는다**
- **적 공격에도 히트 판정 붙이기.** 지금은 `PlayAnimMontage → ApplyDamage → Delay`로 무조건 맞는다. 바꾸는 데 필요한 것 셋 — (1) `PlayAnimMontage`를 `Play Montage`로 교체, (2) `AM_Enemy_Attack`에 `Montage Notify` 찍기(수작업), (3) `ApplyDamage`를 노티파이 분기 뒤 트레이스 성공 쪽으로 옮기기. **오늘 전부 해본 모양이다**
- **칼 메시 구하기.** 리타깃 비용이 애셋 고르는 기준에 들어가야 한다. 루트 모션이 켜져 있는지도 봐야 한다. 웹 검색은 아직 안 했다
- **칼 궤적 트레이스.** 밑동·칼끝 소켓 사이를 매 프레임 훑는 방식. `Play Montage`의 `OnNotifyEnd` 핀이 비어 있어 `Montage Notify Window`로 바꾸면 그대로 올라간다. **지금 구조가 막지 않는다**
- **카메라 작업.** 셋으로 갈렸다
  - **A — 원본 ICI 구조(`캡슐 → Camera → SkeletalMesh`)로 교체.** 팔만 있는 스켈레탈 메시가 프로젝트에 없어 지금 그대로는 못 한다. **이 안은 `HeldItemMesh`의 부모인 `CharacterMesh0`도 갈아엎는다**
  - **B — 지금 구조를 두고 팔을 시야로 올린다.** `Variant_Shooter/Anims/ABP_FP_Weapon` + `Ctrl_HandAdjusment`
  - **C — 전환 스냅 완화만.** 요 보간 또는 `SetViewTargetWithBlend`. 2026-08-27부터 이월
- **1인칭으로 죽으면 3인칭으로 부활하는 것.** 사용자가 `내비두자`로 정했다
- **30초 갇힘 사망**
- **사망 시 아이템 드롭**
- **게임오버 화면 · 사망 카운트 · 체크포인트**
- **적 체력바 위젯 / 순찰 / EQS / 여러 적의 회피 / 적 종류별 DataTable**
- **소리 감지 · 여러 적의 정보 공유 · "뭔가 봤다" 중간 경계 상태**
- **여러 적을 한 번에 때리기.** `SphereTraceForObjects`의 `Multi` 버전으로 노드 하나 교체
- **`BP_ShooterNPC` · `ST_Shooter` · EQS 3개 · StateTree 태스크 6개.** 안 쓰기로 했지만 지우지 않는다
- **`--append-system-prompt`가 저장소에 없다.** `Editor Preferences → General → Terminal → Startup Commands`의 사용자 설정이다. 원문은 `Docs/AI-Log/2026-08-28-inventory-item-data.md`의 `명령` 칸에 있다
- **`BP_Door.uasset`의 재직렬화.** 참조하는 블루프린트를 컴파일하면 딸려 dirty가 된다
- **문간 위 `X 1800..1900, Z 200..400`의 열린 홈.** 관통은 아니다
- **열린 문짝 20cm가 문간 위로 삐져나온다.** 문짝 220, 문간 200
- **`ForLoop.FirstIndex`가 빈 값인 이유.** 동작에 지장이 없다
- **`SP` 스태미나.** 원본에 있고 MCP1에 없다. `06-플레이어-UI.md:54` 참조
- **슬롯 2칸 vs 3칸.** 원본은 2칸, MCP1은 3칸이다
- **미사용 애셋 정리.** 2026-08-30에 **남기기로** 정했다
- **`MoveComponentTo`의 `Stop`·`Return` 핀.** 연타로는 문제가 안 났다
- **칼 픽업이 바닥에 파묻히는 것.** 기존 픽업 6개도 같다
- **`Knife`와 `Key_Stage1`이 같은 메시라 색이 같은 것.** 머티리얼로 가를 수 있다
