# 2026-09-02

## 작업물

**스테이지 진행 구조를 만들었다** — `BP_StageRoom` 액터가 자기 방의 적을 세고, 전멸하면 열쇠를 떨구거나 클리어 문구를 띄운다. 곁들여 `AM_Player_Attack`의 노티파이 창 끝을 적과 맞췄고, 적 공격에 조준이 없다는 것을 그래프에서 확인하고 접었고, 적이 플레이어가 든 칼에 끼는 것을 `HeldItemMesh`의 콜리전을 꺼서 없앴다.

**소요 시간**: 증거가 남은 범위로 `AM_Player_Attack.uasset` 저장(로컬 `17:25:24`)부터 커밋 `34e8d81`(`20:14:34`)까지 약 **2시간 49분**. 그 앞의 인계·심문·조사 구간은 파일도 로그도 안 남아서 **실제 벽시계 시간은 이보다 길다.** 세션 시작 시각을 기록하지 않아 정확한 값을 모른다.

## 명령

### 한글

```
작업준비
```

```
1. 적당함
2. 할까 
3. 적상태는 안해도될듯이제
4. 이름에 문제있는거 아니면 그대로 쓸까
5. 기본값을 100으로 하는게 나은거야? 이건 확인좀 
에디터 켜져있어 슬슬 작업 정리되면 다음 작업 목록들 보고 할까 처음에 정했던 순서
```

```
(스크린샷 두 장 첨부 — AM_Player_Attack 몽타주 에디터, 변경 전 / 변경 후)
변경했어
```

```
확인해줘
```

```
이거 때리고나서 다시 어택할 때 나를 안바라보고 때리는 경우가 있던데 이거에 대해 의견있어?
```

```
아닌가 지금했을땐 또 문제 없어보이거든? 일단 확인좀
```

```
음 이건 그냥 냅두자 그럼 나중에 공격모션 바뀔거니까 그럼 됬다이건
```

```
5단계하자 이거 확인용으로만 내비두고 나중에 구현할 때 확인을 해바
```

```
A 두마리
B 삭제하자 이제 이거 테스트 다했으니까
C 게임모드에서하는것이랑 액터로 하는거중에 자원 덜 쓰고 게임이니까 좀더 낫다고 생각하는 걸 생각해보고 해봐 
D 방마다 고정 지점을 두개 하자 그게 낫겠다 
E 는 기존꺼그대로 하자
```

```
r가자
```

```
결과 확인
```

위 `결과 확인`은 명령 2·3·4·5·6·8 뒤에 각각 한 번씩 들어왔다. 그중 **터미널 출력이 붙어 온 것은 명령 1 뒤의 한 번뿐**이고 나머지는 출력 없이 들어왔다.

```
1번했어기다려봐
```

```
결과 확인해봐 1부터 4까진 다잘된거같다고 생각
```

```
다하자 커밋 기록부터하고
```

```
PIE 결과 확인
```

```
갱신 하고 다음꺼준비
```

```
그렇게하자
```

```
결과 확인
```

```
아까 아이템 줍고 버리기 잘 됬어
```

```
그렇게하자
```

### English — MCP에 실제로 보낸 명령

**이번 세션의 영어 명령은 MCP에 직접 보낸 것이 아니라, 사용자가 UE Terminal에 붙여넣도록 낸 명령문이다.** 아래는 낸 그대로다. 심문 5번의 확인과 이후의 조사·검증은 명령문이 아니라 AI가 MCP로 직접 읽은 것이고, 그 호출 결과는 이 칸이 아니라 `Terminal 결과`에 있다.

한글 지시를 영어로 옮기며 넣은 해석:

- `3. 적상태는 안해도될듯이제` → 적 상태 표시(`ATTACK`/`CHASE`/…)를 **다시 심지 않는다**로 읽었다. "지금은 안 해도 될 듯"이라는 뜻이지 "영원히 안 한다"가 아닐 수 있다.
- `C ... 자원 덜 쓰고 게임이니까 좀더 낫다고 생각하는 걸 생각해보고 해봐` → **AI가 판단해서 하나를 고르고 근거를 대라**로 읽었다. 액터 방식(`BP_StageRoom`)을 골랐다.
- `D 방마다 고정 지점을 두개 하자` → **방마다 고정 지점을 하나씩 두자**로 읽었다. "두개"를 "두자"의 오타로 본 것이다. 방마다 지점을 두 개씩 두라는 뜻이었다면 이 해석은 틀렸다.
- `E 는 기존꺼그대로 하자` → 기존 `ShowHUDMessage` 함수를 그대로 쓴다로 읽었다.

**명령 1**

```
Create a new Blueprint class in the Unreal project.

1. Create a Blueprint asset named BP_StageRoom, parent class Actor,
   in the content folder /Game/Progression (create the folder if it does not exist).

2. Add an ArrowComponent named DropPoint, attached as a child of the
   existing DefaultSceneRoot. Set its relative location to (0, 0, 20)
   and leave its relative rotation and scale at defaults.

3. Add three member variables to BP_StageRoom:
   - EnemiesAlive : Integer, default value 0, instance editable OFF
   - KeyToDrop    : DataTableRowHandle, instance editable ON,
                    leave the default row handle empty
   - bIsFinalRoom : Boolean, default value false, instance editable ON

4. Compile the blueprint, then save it.

Do not add any other components, variables, functions, or event nodes.
Do not modify any other asset.

Then report, read back from the editor after compiling and saving:
  - the full component hierarchy of BP_StageRoom with each component's
    class name and relative location
  - the list of member variables with, for each one, its type,
    its default value, and whether Instance Editable is ON or OFF
  - the on-disk file path of the created .uasset and its file size
```

**명령 2**

```
Edit the Blueprint /Game/Progression/BP_StageRoom. Add two function graphs.

FUNCTION 1 — name it RegisterEnemy. No inputs, no outputs.
  Body: Set EnemiesAlive = EnemiesAlive + 1

FUNCTION 2 — name it NotifyEnemyDied. No inputs, no outputs.
  Body, in this order:

  1. Set EnemiesAlive = EnemiesAlive - 1
  2. -> Branch, Condition = (EnemiesAlive == 0)
       Use an Integer Equal (==) node reading EnemiesAlive AFTER the Set,
       compared against the literal 0. Leave the False pin unconnected.
  3. Branch True -> a second Branch, Condition = bIsFinalRoom

  4. Second Branch TRUE pin (this is the final room):
       Get Player Character (Player Index 0)
       -> Cast To BP_ThirdPersonCharacter
       -> Cast succeeded pin -> call ShowHUDMessage on the cast result
          with the message text: STAGE CLEAR
       Leave the Cast Failed pin unconnected.

  5. Second Branch FALSE pin (a key drops here):
       Spawn Actor from Class
         Class                      = /Game/Inventory/BP_ItemPickup
         Collision Handling Override = Always Spawn, Ignore Collisions
         ItemRow pin                = KeyToDrop      (this pin exists because
                                      BP_ItemPickup's ItemRow has Expose on Spawn)
         Spawn Transform            = a Make Transform node with
                                        Location = DropPoint -> GetWorldLocation
                                        Rotation = (0, 0, 0)
                                        Scale    = (1, 1, 1)
       Do not connect the spawned actor return value to anything.

Do not add variables. Do not touch the Event Graph. Do not modify any
other asset, including BP_ItemPickup and BP_Enemy.

Compile, then save.

Then report, read back from the editor after compiling and saving:
  - read_graph_dsl output for BOTH function graphs, verbatim
  - the full input-pin list of the Spawn Actor from Class node, verbatim,
    so I can confirm the ItemRow pin actually exists
  - any compile warnings or errors, verbatim in English
  - BP_StageRoom.uasset file size and mtime
```

**명령 3**

```
Edit the Blueprint /Game/Enemy/BP_Enemy. Add exactly one member variable.

  Name            : OwningRoom
  Type            : Object Reference to the Blueprint class BP_StageRoom
                    (/Game/Progression/BP_StageRoom.BP_StageRoom_C)
  Default value   : None
  Instance Editable : ON

Do not add any other variable. Do not add, delete, move or reconnect any
node in any graph. Do not modify any other asset.

Compile, then save.

Then report, read back from the editor after compiling and saving:
  - the full output of list_variables for BP_Enemy
  - the resolved type of OwningRoom, stated as the exact class path it
    points to, not just "object reference"
  - whether the two placed BP_Enemy instances in Lvl_ThirdPerson now show
    an OwningRoom field in their Details panel, and what value each shows
  - any compile warnings or errors, verbatim in English
  - BP_Enemy.uasset file size and mtime
```

**명령 4**

```
Edit the Event Graph of /Game/Enemy/BP_Enemy. This is a targeted insertion,
NOT a graph rewrite. Do not delete, move, or re-create any existing node.
Do not read the whole graph out and write it back.

INSERTION 1 — in the Event BeginPlay chain.

  The chain today is:
    Event BeginPlay -> Set PlayerRef -> Set HomeLocation -> Set HomeRotation
      -> Set LastSeenTime -> Set CurrentHP -> Think

  "Set CurrentHP" here means the one in the BeginPlay chain, whose Value
  input comes from Get MaxHP. Not the one in Event AnyDamage.

  a. Break only the exec link from that Set CurrentHP to Think.
  b. Add an Is Valid macro node (the one with "Is Valid" and "Is Not Valid"
     exec output pins), Input Object = Get OwningRoom.
  c. Set CurrentHP  ->  Is Valid macro exec input.
  d. Is Valid pin      -> call RegisterEnemy on Get OwningRoom  -> Think
  e. Is Not Valid pin  -> Think
     Both paths end at the same existing Think node.

INSERTION 2 — in the Event AnyDamage chain.

  The chain today is:
    Event AnyDamage -> Set CurrentHP -> Print String
      -> Branch (Condition = CurrentHP <= 0) -> True -> DestroyActor

  a. Break only the exec link from that Branch's True pin to DestroyActor.
  b. Add a second Is Valid macro node, Input Object = Get OwningRoom.
  c. Branch True  ->  Is Valid macro exec input.
  d. Is Valid pin      -> call NotifyEnemyDied on Get OwningRoom -> DestroyActor
  e. Is Not Valid pin  -> DestroyActor
     Both paths end at the same existing DestroyActor node.

Change nothing else. Do not touch the Think custom event body, Event Tick,
any variable default, or any other asset.

Compile, then save.

Then report, read back from the editor after compiling and saving:
  - read_graph_dsl for BP_Enemy's Event Graph, verbatim
  - a confirmation that Event Tick and the Think event body are byte-identical
    to before the edit
  - any compile warnings or errors, verbatim in English
  - BP_Enemy.uasset file size and mtime
```

**명령 5 — 불필요했던 명령이다.** AI의 오진에서 나왔다. 아래 `총평` 참조.

```
Edit the Event Graph of /Game/Enemy/BP_Enemy. Connect two exec pins that
were left unconnected. This is the only change. Do not add, delete, move,
or re-create any node. Do not read the whole graph out and write it back.

CONNECTION 1 — in Event BeginPlay.
  There is an Is Valid macro node whose Input Object is Get OwningRoom.
  Its "Is Valid" pin already goes to RegisterEnemy -> Think.
  Its "Is Not Valid" pin is unconnected.
  Connect that "Is Not Valid" pin to the SAME existing Think node that the
  Is Valid path already reaches. Do not create a second Think node.

CONNECTION 2 — in Event AnyDamage.
  There is a second Is Valid macro node whose Input Object is Get OwningRoom,
  reached from the Branch (CurrentHP <= 0) True pin.
  Its "Is Valid" pin already goes to NotifyEnemyDied -> DestroyActor.
  Its "Is Not Valid" pin is unconnected.
  Connect that "Is Not Valid" pin to the SAME existing DestroyActor node that
  the Is Valid path already reaches. Do not create a second DestroyActor node.

Change nothing else.

Compile, then save.

Then report, read back from the editor after compiling and saving:
  - read_graph_dsl for BP_Enemy's Event Graph, verbatim
  - confirm that both "Is Not Valid" branches are no longer empty
  - confirm the graph still contains exactly one Think call node reached from
    BeginPlay and exactly one DestroyActor node
  - any compile warnings or errors, verbatim in English
  - BP_Enemy.uasset file size and mtime
```

**명령 6**

```
Work in the level /Game/ThirdPerson/Lvl_ThirdPerson.
Place two actors of the Blueprint class /Game/Progression/BP_StageRoom.

ACTOR 1
  Actor label   : Room1
  World location: (840, 1130, 0)
  Rotation      : (0, 0, 0)      Scale: (1, 1, 1)
  Property values on this instance:
    KeyToDrop    = DataTable /Game/Inventory/DT_Items, Row Name Key_Stage1
    bIsFinalRoom = false
  Leave the DropPoint component at its default relative location (0, 0, 20),
  so its world location is (840, 1130, 20).

ACTOR 2
  Actor label   : Room2
  World location: (4000, 0, 0)
  Rotation      : (0, 0, 0)      Scale: (1, 1, 1)
  Property values on this instance:
    KeyToDrop    = leave empty (no DataTable, no Row Name)
    bIsFinalRoom = true
  Leave the DropPoint component at its default relative location.

Do not move, delete or modify any other actor. Do not modify any Blueprint asset.

Save the level.

Then report, read back from the editor after saving:
  - the result of find_actors for class BP_StageRoom_C in this level:
    how many were found and the label plus world location of each
  - for each of the two actors, the values of KeyToDrop and bIsFinalRoom
    and EnemiesAlive, read from the placed instance and not from the CDO
  - for each of the two actors, the world location of its DropPoint component
  - the on-disk mtime and file size of the level's .umap file
```

**명령 7**

```
Work in the level /Game/ThirdPerson/Lvl_ThirdPerson.

PART 1 — place two new enemies in Room 1.

Place two actors of the Blueprint class /Game/Enemy/BP_Enemy.

  Actor label Enemy_R1_A : world location (-1400,   0, 90), rotation (0, 0, 0)
  Actor label Enemy_R1_B : world location (-1400, 150, 90), rotation (0, 0, 0)

  Scale (1,1,1) for both. Do not change any other property on them.

PART 2 — assign OwningRoom on all four enemies.

Set the OwningRoom instance property on each of these four actors:

  Enemy_R1_A                                          -> Room1
  Enemy_R1_B                                          -> Room1
  BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143       -> Room2
  BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879       -> Room2

  Room1 is the placed actor
    PersistentLevel.BP_StageRoom_C_UAID_9C6B005AF869F1FD02_1985138080
  Room2 is the placed actor
    PersistentLevel.BP_StageRoom_C_UAID_9C6B005AF869F1FD02_1990423081

Do not move, delete or modify any other actor. Do not modify any Blueprint asset.
Do not touch the BP_ItemPickup actors.

Save the level.

Then report, read back from the editor after saving:
  - find_actors for class BP_Enemy_C: how many were found, and for each one
    its label, its world location, and the label of the actor its OwningRoom
    points to (or None)
  - confirm that no enemy has OwningRoom = None
  - the list of new or changed paths under Content/__ExternalActors__/
```

**명령 8**

```
Work in the level /Game/ThirdPerson/Lvl_ThirdPerson.

Delete exactly one actor: the BP_ItemPickup instance at world location
(840, 1130, 0), whose ItemRow is DataTable /Game/Inventory/DT_Items,
Row Name Key_Stage1. Its path is

  PersistentLevel.BP_ItemPickup_C_UAID_9C6B005AF86967FC02_1094395736

Before deleting, confirm that this actor's ItemRow really is Key_Stage1 and
that its world location really is (840, 1130, 0). If either does not match,
stop and report instead of deleting.

Delete nothing else. There are six other BP_ItemPickup actors in this level
and all six must remain. Do not modify any Blueprint asset.

Save the level.

Then report, read back from the editor after saving:
  - find_actors for class BP_ItemPickup_C: how many remain, and for each one
    its world location and its ItemRow row name
  - confirm that no remaining pickup has row name Key_Stage1
  - the list of new, changed or deleted paths under Content/__ExternalActors__/
```

**명령 9**

```
Edit the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.
Change exactly one component setting.

Component: HeldItemMesh (the StaticMeshComponent)

  Set its Collision Presets to: NoCollision

  That is the only change. Specifically:
  - do NOT change RelativeLocation, RelativeScale3D, or the static mesh
  - do NOT change Generate Overlap Events or Can Character Step Up On;
    leave both at whatever they are now
  - do NOT touch any other component, variable, function or node
  - do NOT modify any other asset

Compile, then save.

Then report, read back from the editor after compiling and saving:
  - the BodyInstance of HeldItemMesh, specifically collisionProfileName
    and collisionEnabled
  - RelativeScale3D and RelativeLocation of HeldItemMesh, to confirm they
    did not move
  - BP_ThirdPersonCharacter.uasset file size and mtime
```

**명령 9는 경고 보고를 요구하지 않았다.** `LogsToolset.GetLogEntries`로 직접 읽을 수 있다는 것을 그 직전에 알았기 때문이다. 앞의 여덟 개와 다른 점이다.

## Terminal 결과

**이 세션은 터미널 출력을 거의 못 받았다.** 명령 여덟 개 중 출력이 붙어 온 것은 **명령 1 하나뿐**이고, 명령 7에서 터미널이 저장 방법을 되물어온 프롬프트가 하나 더 있다. 나머지는 사용자가 `결과 확인`만 입력했고 **AI가 MCP로 에디터를 직접 읽어서 검증했다.** 그래서 아래 원문 칸에는 터미널 출력과 MCP 읽기 결과가 섞여 있고 어느 쪽인지 표시했다. 길이 때문에 발췌한 것은 발췌라고 적었고, **실패·경고·어긋난 응답은 전문을 붙였다.**

### 원문 — English

**터미널 출력 — 명령 1의 보고. 사용자가 붙여넣은 그대로다. 표 테두리가 깨진 것과 문장이 잘린 것(`anefaults`, `ng tree`, `Nofolder`, `BP_Sm_C`)도 그대로 둔다.**

```
Created and saved. Everything below is read back from the editor after compile + save.

Component hierarchy

┌──────────────────┬───────────────────────────────┬──────────────────┬───────────────────┐
│    Component     │             Class             │      Parent      │ Relative Location │
├──────────────────┼───────────────────────────────┼──────────────────┼───────────────────┤
│ DefaultSceneRoot │ /Script/Engine.SceneComponent │ (root)           │ (0, 0, 0)         │
├──────────────────┼───────────────────────────────┼──────────────────┼───────────────────┤
│ └ DropPoint      │ /Script/Engine.ArrowComponent │ DefaultSceneRoot │ (0, 0, 20)        │
└──────────────────┴─────────────────────────────────────────┘

DropPoint rotation (pitch 0, yaw 0, roll 0) anefaults, confirmed by read-back. Parent linkconfirmed via get_parent_component. Only these two components exist (get_components returned exactly these two).

Member variables

Values read from the CDO /Game/Progression/BP_StageRoom.Default__BP_StageRoom_C:

┌──────────────┬────────────────────┬─────────────────────────────────────────────────┬─────────────────────────┐
│   Variable   │        Type        │                  Default value                  │    Instance Editable    │
├──────────────┼────────────────────┼────────────────────┼─────────────────────────┤
│ EnemiesAlive │ Integer            │ 0                                               │ OFF — set, not verified │
├──────────────┼────────────────────┼─────────────────────────────────────────────────┼─────────────────────────┤
│ KeyToDrop    │ DataTableRowHandle │ {dataTable: None, rowName: None} (empty handle) │ ON — set, not verified  │
├──────────────┼────────────────────┼────────────────────┼─────────────────────────┤
│ bIsFinalRoom │ Boolean            │ false                                           │ ON — set, not verified  │
└──────────────┴────────────────────┴─────────────────────────────────────────────────┴─────────────────────────┘

list_variables returned exactly ["EnemiesAlive","KeyToDrop","bIsFinalRoom"] — no extra variables.

Instance Editable could not be read back. I called BlueprintTools.set_variable_instance_editable once per variable (false / true / true); each returned {"returnValue":null}, which in this plugin means nothing. The blueprint toolset has get_variable_category and get_variable_replication but no get_variable_instance_editable. I then tried ObjectTools.get_properties on the Blueprint for NewVariables to read the flags directly; it redirected to the CDO and      failed:

GetObjectProperties on '/Game/Progression/BP_Sm_C' (BP_StageRoom_C): the following propertiescould not be read: NewVariables

So the three Instance Editable states are what I asked for, not what I confirmed. Please check the checkboxes in the My Blueprint panel.

On disk

D:\20260827\MCP1\Content\Progression\BP_StageRoom.uasset                                                                   28,991 bytes
mtime 2026-09-02 18:48:43 +0900 — after the compile, so the save reached disk (is_dirty also returned false).

Scope check

git status shows Content/Progression/ as the only new path. The three M entries (AM_Player_Attack.uasset, BP_Enemy.uasset, BP_Door.uasset) predate this task — they were ng tree; I did not touch them in this step. Nofolder existed at /Game/Progression beforehand (exists returned false), so I created it.
```

**터미널 출력 — 명령 7에서 터미널이 되물어온 프롬프트. 사용자가 붙여넣은 그대로다. 선택지 2번의 문장이 `for` 뒤에서 잘린 것도 그대로 둔다.**

```
Same request as last turn. Checking current state first so I don't create duplicates.

No console-command or save-level tool exists in the editor toolset either. Trying one more save route — the external-actor package path directly, now that I know it.

Save route

Every path-based save tool is broken for this OFPA level, so the only way I can persist the four enemies is save_assets([]) — save ALL dirty assets. Right now that set is: the new/changed actor packages (wanted), BP_Enemy and BP_StageRoom (my edits, wanted), and BP_Door (dirty from before my session, and you said not to modify any Blueprint asset). How should I proceed?

1. You press Ctrl+S
     I leave everything as-is. You save in the editor, which persists all four enemies plus BP_Door on your own authority. This is what appears to have happened at 19:44:53 for Room1/Room2.
2. Run save_assets([]) anyway
     I save all dirty assets now. The four enemies persist, but BP_Door gets written to disk too, overriding the "do not modify any Blueprint asset" constraint for
3. Leave it unsaved
     Editor-only state is fine for now; you'll decide later. The two new enemies and all four OwningRoom assignments are lost if the editor closes.
4. Type something.
```

**MCP 읽기 실패 — 몽타주의 노티파이는 여전히 못 읽는다. `ObjectTools.get_properties` 에러 전문 셋.**

```
GetObjectProperties on '/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack' (AnimMontage): the following properties could not be read: Notifies
```

```
GetObjectProperties on '/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Enemy_Attack.AM_Enemy_Attack' (AnimMontage): the following properties could not be read: bEnableRootMotion, bEnableRootMotionTranslation, bEnableRootMotionRotation
```

```
GetObjectProperties on '/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01.MM_Attack_01' (AnimSequence): the following properties could not be read: bRootMotionSettingsCopiedFromMontage
```

```
GetObjectProperties on '/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_ItemPickup_C_UAID_9C6B005AF86998FC02_1359517359' (BP_ItemPickup_C): the following properties could not be read: RowName, ItemHandle
```

**MCP 호출 실패 — 툴 인자 이름이 예상과 다른 것. 이번 세션에 여섯 번 걸렸다. 에러 전문 넷.**

```
Function "list_variables", input param "blueprint" is required by the function input schema Json, but is missing from the incoming function input params Json.
Function schema Json -
{"type":"object","properties":{"blueprint":{"type":"object","title":"/Script/Engine.Blueprint","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]},"graph":{"default":null,"type":"object","title":"/Script/Engine.EdGraph","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]}},"required":["blueprint"]}
Function input params Json -
{"blueprint_path":"/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"}
```

```
Function "get_properties", input param "instance" is required by the function input schema Json, but is missing from the incoming function input params Json.
Function schema Json -
{"type":"object","properties":{"instance":{"type":"object","title":"/Script/CoreUObject.Object","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]},"properties":{"type":"array","items":{"type":"string"}}},"required":["instance","properties"]}
Function input params Json -
{"object":{"refPath":"/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.Default__BP_ThirdPersonCharacter_C"},"property_names":["CurrentHP","MaxHP","RespawnDelay"]}
```

```
Function "find_nodes", input param "title" is required by the function input schema Json, but is missing from the incoming function input params Json.
Function schema Json -
{"type":"object","properties":{"graph":{"type":"object","title":"/Script/Engine.EdGraph","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]},"title":{"type":"string"},"node_class":{"default":null,"type":"object","title":"/Script/CoreUObject.Class","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]},"entry_points_only":{"type":"boolean","default":false}},"required":["graph","title"]}
Function input params Json -
{"blueprint":{"refPath":"/Game/Progression/BP_StageRoom.BP_StageRoom"},"graph":{"refPath":"/Game/Progression/BP_StageRoom.BP_StageRoom:NotifyEnemyDied"}}
```

```
Function "get_pin_value", input param "pin" is required by the function input schema Json, but is missing from the incoming function input params Json.
Function schema Json -
{"type":"object","properties":{"pin":{"title":"PinID","type":"object","properties":{"direction":{"type":"string","title":"EEdGraphPinDirection","enum":["EGPD_Input","EGPD_Output"]},"index_id":{"type":"integer"},"node":{"type":"object","title":"/Script/Engine.EdGraphNode","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]}},"required":["direction","index_id","node"]}},"required":["pin"]}
Function input params Json -
{"node":{"refPath":"/Game/Progression/BP_StageRoom.BP_StageRoom:NotifyEnemyDied.K2Node_CallFunction_13"},"pin_name":"Scale"}
```

**MCP 호출 실패 — `describe_toolset`을 `call_tool`로 부른 것. 최상위 툴이라 안 된다.**

```
Unknown tool describe_toolset
```

**MCP 호출 실패 — 존재하지 않는 툴 이름.**

```
Unknown tool get_row_names
```

```
Unknown tool get_transform
```

**MCP 응답 초과 — `BlueprintTools`의 `describe_toolset`이 응답 한도를 넘는다.**

```
Error: result (72,168 characters across 1 line) exceeds maximum allowed tokens. Output has been saved to C:\Users\a0108\.claude\projects\d--20260827-MCP1\eebbf1fd-cec0-46f8-b218-0ede2c3b3b0c\tool-results\mcp-unreal-mcp-describe_toolset-1788337910043.txt.
```

**MCP 읽기 — `AM_Player_Attack`의 노티파이 시각. 저장된 `.uasset`을 커밋본과 바이트 비교해 디코딩한 값이다. PowerShell `[BitConverter]::ToSingle` 출력 발췌.**

```
=== anchor 10329
10329  old=0.496946 new=0.534953   oldFrame=14.91 newFrame=16.05  <-- CHANGED
=== anchor 10797
10797  old=0.209040 new=0.247048   oldFrame=6.27 newFrame=7.41  <-- CHANGED
=== anchor 11134
11134  old=0.496946 new=0.534953   oldFrame=14.91 newFrame=16.05  <-- CHANGED
```

```
10206  0.287906   frame=8.64
11878  0.287906   frame=8.64
```

**MCP 읽기 — `AM_Enemy_Attack`의 같은 오프셋. 비교용 발췌.**

```
10208  0.304194   frame=9.13
10331  0.532238   frame=15.97
10799  0.228044   frame=6.84
11136  0.532238   frame=15.97
11880  0.304194   frame=9.13
```

**엔진 소스 — `MakeTransform`의 `Scale` 기본값 근거. `KismetMathLibrary.h:3932`.**

```
	static UE_INL_API FTransform MakeTransform(FVector Location, FRotator Rotation, FVector Scale = FVector(1,1,1));
```

**MCP 읽기 — 적 회전 경로를 뒤진 결과. `get_properties` 출력.**

```
{"bUseControllerRotationYaw":false,"bUseControllerRotationPitch":false,"bUseControllerRotationRoll":false,"AttackRange":150,"AttackCooldown":1.5,"ThinkInterval":0.29999999999999999,"SightRange":1200,"AttackDamage":10}
```

```
{"bOrientRotationToMovement":true,"RotationRate":{"pitch":0,"yaw":500,"roll":0},"bUseControllerDesiredRotation":false,"MaxWalkSpeed":300}
```

```
{"bUseControllerRotationYaw":false,"AttackRange":150,"AttackCooldown":1.5,"ReturnSightRange":300,"SightHalfAngle":60,"FistRadius":15,"AIControllerClass":{"refPath":"/Script/AIModule.AIController"},"AutoPossessAI":"PlacedInWorld"}
```

```
{"AnimClass":{"refPath":"/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed_C"},"SkeletalMesh":{"refPath":"/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"},"RelativeRotation":{"pitch":0,"yaw":270,"roll":0},"RelativeLocation":{"x":0,"y":0,"z":-89}}
```

```
{"RootMotionMode":"RootMotionFromMontagesOnly"}
```

```
{"bEnableRootMotion":true,"RootMotionRootLock":"RefPose","bForceRootLock":false}
```

**MCP 읽기 — `BP_StageRoom`의 두 함수. `read_graph_dsl` 출력 전문.**

```
(fn RegisterEnemy ()
  (Variables|Default|SetEnemiesAlive (+ (Variables|Default|GetEnemiesAlive) 1)))
```

```
(fn NotifyEnemyDied ()
  (Variables|Default|SetEnemiesAlive (- (Variables|Default|GetEnemiesAlive) 1))
  (if (== (Variables|Default|GetEnemiesAlive) 0)
    (if (|GetbIsFinalRoom)
      (bind _asbp_third_person_character (Utilities|Casting|CastToBP_ThirdPersonCharacter (Game|GetPlayerCharacter 0)))
      (Class|BPThirdPersonCharacter|ShowHUDMessage _asbp_third_person_character "STAGE CLEAR")
      (else
        (Game|SpawnActorBPItemPickup "/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C" (Math|Transform|MakeTransform (Transformation|GetWorldLocation (Variables|Default|GetDropPoint))) "AlwaysSpawn" "MultiplyWithRoot" 0 (Variables|Default|GetKeytoDrop) 0)))))
```

**MCP 읽기 — `MakeTransform` 노드 `K2Node_CallFunction_13`의 실제 핀값. `get_pin_value` 출력 둘.**

```
"1.000000,1.000000,1.000000"
```

```
"0, 0, 0"
```

**MCP 읽기 — `get_node_type_pins`가 응답에 담아 보낸, 그래프에 존재하지 않는 노드. 위치가 `(0,0)`이고 id가 `_26`인데, 같은 그래프를 `find_nodes`로 세면 `_13` 하나뿐이다.**

```
{"returnValue":{"output_pins":[{"value":"","connected_pins":[],"pin_id":{"direction":"EGPD_Output","index_id":0,"node":{"refPath":"/Game/Progression/BP_StageRoom.BP_StageRoom:NotifyEnemyDied.K2Node_CallFunction_26"}},"type_id":"Transform","name":"ReturnValue"}],"input_pins":[{"value":"0, 0, 0","connected_pins":[],"pin_id":{"direction":"EGPD_Input","index_id":0,"node":{"refPath":"/Game/Progression/BP_StageRoom.BP_StageRoom:NotifyEnemyDied.K2Node_CallFunction_26"}},"type_id":"Vector","name":"Location"},{"value":"0, 0, 0","connected_pins":[],"pin_id":{"direction":"EGPD_Input","index_id":1,"node":{"refPath":"/Game/Progression/BP_StageRoom.BP_StageRoom:NotifyEnemyDied.K2Node_CallFunction_26"}},"type_id":"Rotator","name":"Rotation"},{"value":"1.000000,1.000000,1.000000","connected_pins":[],"pin_id":{"direction":"EGPD_Input","index_id":2,"node":{"refPath":"/Game/Progression/BP_StageRoom.BP_StageRoom:NotifyEnemyDied.K2Node_CallFunction_26"}},"type_id":"Vector","name":"Scale"}],"position":{"x":0,"y":0},"node":{"refPath":"/Game/Progression/BP_StageRoom.BP_StageRoom:NotifyEnemyDied.K2Node_CallFunction_26"},"type_id":"Math|Transform|MakeTransform"}}
```

**MCP 읽기 — 오진의 원인이 된 출력. `BP_Enemy` EventGraph의 `read_graph_dsl` 중 두 이벤트 발췌. `Is Not Valid` 가지가 비어 보인다.**

```
(event EventBeginPlay
  (bind _owningroom (Variables|Default|GetOwningRoom))
  (Variables|Default|SetPlayerRef (Game|GetPlayerCharacter 0))
  (Variables|Default|SetHomeLocation (Transformation|GetActorLocation))
  (Variables|Default|SetHomeRotation (Transformation|GetActorRotation))
  (Variables|Default|SetLastSeenTime (Utilities|Time|GetGameTimeInSeconds))
  (Variables|Default|SetCurrentHP (Variables|Default|GetMaxHP))
  (Utilities|IsValid _owningroom
    (:"Is Valid"
      (Class|BPStageRoom|RegisterEnemy _owningroom)
      (CallFunction|Think))
    (:"Is Not Valid")))

(event Game|Damage|EventAnyDamage (Damage DamageType InstigatedBy DamageCauser)
  (bind _owningroom (Variables|Default|GetOwningRoom))
  (bind _output_get (Variables|Default|SetCurrentHP (Math|Float|Clamp(Float) (- (Variables|Default|GetCurrentHP) Damage) 0.0 (Variables|Default|GetMaxHP))))
  (Development|PrintString (Utilities|String|Append "EnemyHP: " (Utilities|String|ToString(Float) _output_get)))
  (if (<= _output_get 0)
    (Utilities|IsValid _owningroom
      (:"Is Valid"
        (Class|BPStageRoom|NotifyEnemyDied _owningroom)
        (Actor|DestroyActor))
      (:"Is Not Valid"))))
```

**MCP 읽기 — 같은 그래프를 `get_node_infos`로 읽은 것. 연결이 실제로는 있다. `Think(_82)`의 exec 입력에 연결이 둘이고, `_34`의 `Is Not Valid`가 `DestroyActor(_3)`로 간다.**

```
{"value":"","connected_pins":[{"direction":"EGPD_Output","index_id":0,"node":{"refPath":"/Game/Enemy/BP_Enemy.BP_Enemy:EventGraph.K2Node_CallFunction_117"}},{"direction":"EGPD_Output","index_id":1,"node":{"refPath":"/Game/Enemy/BP_Enemy.BP_Enemy:EventGraph.K2Node_MacroInstance_33"}}],"pin_id":{"direction":"EGPD_Input","index_id":0,"node":{"refPath":"/Game/Enemy/BP_Enemy.BP_Enemy:EventGraph.K2Node_CallFunction_82"}},"type_id":"Exec","name":"execute"}
```

```
{"value":"","connected_pins":[{"direction":"EGPD_Input","index_id":0,"node":{"refPath":"/Game/Enemy/BP_Enemy.BP_Enemy:EventGraph.K2Node_CallFunction_3"}}],"pin_id":{"direction":"EGPD_Output","index_id":1,"node":{"refPath":"/Game/Enemy/BP_Enemy.BP_Enemy:EventGraph.K2Node_MacroInstance_34"}},"type_id":"Exec","name":"Is Not Valid"}
```

**MCP 읽기 — `OwningRoom`의 해석된 타입.**

```
"type_id":"BP Stage Room Object Reference","name":"OwningRoom"
```

**MCP 읽기 — 방 액터 둘의 인스턴스 값.**

```
{"KeyToDrop":{"dataTable":{"refPath":"/Game/Inventory/DT_Items.DT_Items"},"rowName":"Key_Stage1"},"bIsFinalRoom":false,"EnemiesAlive":0}
```

```
{"KeyToDrop":{"dataTable":"None","rowName":"None"},"bIsFinalRoom":true,"EnemiesAlive":0}
```

**셸 — 건드리지 않은 애셋이 세션 중 dirty가 된 것. 세션 시작 시 `git status`는 비어 있었다. 커밋본과의 바이트 비교.**

```
Content/Enemy/BP_Enemy.uasset  size 395090 -> 395090  diffbytes=1911  range=25..15847
Content/Interaction/BP_Door.uasset  size 135077 -> 135077  diffbytes=49  range=25..97226
Content/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.uasset  size 12303 -> 12303  diffbytes=31  range=25..11138
```

**셸 — `BP_Door`의 헤더(바이트 25~44)를 뺀 나머지 차이. 한 덩어리 32바이트 구간에 몰려 있다.**

```
97195 97196 97197 97198 97199 97200 97201 97202 97204 97205 97206 97208 97209 97210 97211 97212 97213 97214 97215 97216 97217 97218 97219 97220 97221 97222 97223 97224 97225 97226
```

**셸 — 저장이 `.umap`이 아니라 외부 액터 파일로 간다는 것. 최종 `git status` 발췌.**

```
 M Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/0/KM/MV2KKKYMIZ9A43Y7GVWSU9.uasset
 M Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/A/IN/5FI6JSM02A316FCLSZ10WA.uasset
 D Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/B/UL/398OVSFQQJ4SYP7ZQL6IFH.uasset
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/3/FH/
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/8/GO/
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/D/4G/AEZ8G3JRFXKZO668LCTF6P.uasset
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/D/J4/
```

**UE 출력 로그 — 이번 세션이 끝난 뒤 `LogsToolset.GetLogEntries`로 읽은 것이다. 열 번째로 "못 받았다"고 적었던 경고가 `LogScript` 카테고리에 그대로 있었다.** 타임스탬프는 UTC이고 로컬은 `+9`시간이다.

```
[2026.09.02-09.56.24:515][367]LogScript: Warning: Unknown input pin "ItemRow" on Game|SpawnActorfromClass. Input pins: ['Class', 'SpawnTransform', 'CollisionHandlingOverride', 'TransformScaleMethod', 'Owner']. Output pins: ['ReturnValue'] (use positional bind to capture outputs)
```

```
[2026.09.02-09.49.35:446][726]LogScript: Warning: GetObjectProperties on '/Game/Progression/BP_StageRoom.Default__BP_StageRoom_C' (BP_StageRoom_C): the following properties could not be read: NewVariables
[2026.09.02-10.43.16:439][810]LogScript: Warning: GetObjectProperties on '/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_StageRoom_C_UAID_9C6B005AF869F1FD02_1985138080.DropPoint' (ArrowComponent): the following properties could not be read: ComponentToWorld
```

```
[2026.09.02-10.41.52:260][479]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/D/J4/YRCTSX0Q6C6HOI4XYRJT1I
[2026.09.02-10.41.52:260][479]LogScript: Warning: Failed to save 'Room1'.
[2026.09.02-10.42.26:472][602]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/3/FH/1US2PN6P1S72Z6OC6K0FNA
[2026.09.02-10.42.26:472][602]LogScript: Warning: Failed to save 'Room2'.
[2026.09.02-10.48.03:297][108]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/8/GO/Q4KQB556FPML8LI4ML69JM
[2026.09.02-10.48.03:297][108]LogScript: Warning: Failed to save 'Enemy_R1_A'.
```

**UE 출력 로그 — 노티파이 창 회귀 검사에 쓴 PIE. `11.11` UTC = 로컬 `20:11`. 적 넷이 전부 죽은 판이다. 발췌가 아니라 이 판의 `EnemyHP` 전부다.**

```
[2026.09.02-11.11.22:237][191]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1233633259] EnemyHP: 66.0
[2026.09.02-11.11.24:237][326]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1233633259] EnemyHP: 32.0
[2026.09.02-11.11.25:849][433]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1228603258] EnemyHP: 66.0
[2026.09.02-11.11.25:891][436]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1233633259] EnemyHP: 0.0
[2026.09.02-11.11.39:010][380]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1228603258] EnemyHP: 32.0
[2026.09.02-11.11.40:658][492]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1228603258] EnemyHP: 0.0
[2026.09.02-11.11.54:153][441]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 66.0
[2026.09.02-11.11.56:437][593]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 32.0
[2026.09.02-11.12.00:672][874]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143] EnemyHP: 66.0
[2026.09.02-11.12.03:690][ 76]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 0.0
[2026.09.02-11.12.05:137][175]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143] EnemyHP: 32.0
[2026.09.02-11.12.06:768][287]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143] EnemyHP: 0.0
```

**UE 출력 로그 — 한 스윙이 적 둘을 같은 프레임에 때린 사례. `08.01` UTC = 로컬 `17:01`. 프레임 번호와 밀리초가 둘 다 같다.**

```
[2026.09.02-08.01.58:520][434]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 66.0
[2026.09.02-08.01.58:520][434]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143] EnemyHP: 66.0
```

**UE 출력 로그 — 방1의 적이 플레이어가 든 칼에 끼인 것. 전문.**

```
[2026.09.02-11.35.16:505][275]LogCharacterMovement: BP_Enemy_C_UAID_9C6B005AF869F2FD02_1228603258 is stuck and failed to move! Velocity: X=-168.80 Y=20.88 Z=0.00 Location: X=-1291.88 Y=-45.52 Z=90.07 Normal: X=0.85 Y=0.30 Z=-0.44 PenetrationDepth:18.127 Actor:BP_ThirdPersonCharacter_C_0 Component:HeldItemMesh BoneName:None (0 other events since notify)
```

**UE 출력 로그 — PIE 종료 시 경고.**

```
[2026.09.02-11.35.40:935][437]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
```

**UE 출력 로그 — `LogBlueprint` 카테고리 전문. 세션 전체에서 `Compiling Blueprint` 줄만 있고 경고도 에러도 하나 없다. 열 세션째 이월돼온 "컴파일 경고 원문"의 답은 "경고가 없었다"였다. 발췌가 아니라 이 카테고리의 전부다.**

```
[2026.09.02-07.04.56:128][811]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.02-07.05.00:796][825]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.09.02-07.20.51:537][910]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.02-07.26.03:851][804]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.09.02-07.49.56:071][121]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.02-07.50.00:405][134]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.09.02-08.06.50:757][294]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.02-08.07.09:797][669]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.09.02-08.35.26:804][557]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.02-09.47.50:094][228]LogBlueprint: Compiling Blueprint '/Game/Progression/BP_StageRoom.BP_StageRoom'
[2026.09.02-09.48.39:264][467]LogBlueprint: Compiling Blueprint '/Game/Progression/BP_StageRoom.BP_StageRoom'
[2026.09.02-09.54.57:245][113]LogBlueprint: Compiling Blueprint '/Game/Progression/BP_StageRoom.BP_StageRoom'
[2026.09.02-09.56.36:523][397]LogBlueprint: Compiling Blueprint '/Game/Progression/BP_StageRoom.BP_StageRoom'
[2026.09.02-09.57.16:468][513]LogBlueprint: Compiling Blueprint '/Game/Progression/BP_StageRoom.BP_StageRoom'
[2026.09.02-10.10.06:716][ 42]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.02-10.27.08:818][400]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.02-11.11.12:238][512]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Door.BP_Door'
[2026.09.02-11.11.12:264][512]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.02-11.46.19:001][646]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
```

`11.11.12`의 두 줄은 **내가 시키지 않은 컴파일이다.** `BP_Door`와 `BP_Enemy`가 PIE 시작 직전에 컴파일됐다. 두 애셋이 dirty가 된 경로의 단서다.

**UE 출력 로그 — `HeldItemMesh` 콜리전을 끈 뒤의 PIE. `11.57` UTC = 로컬 `20:57`. 저장이 `11.46`이므로 변경 후 판이다. 이 판의 `EnemyHP` 전부다.**

```
[2026.09.02-11.57.25:279][903]PIE: Play in editor total start time 0.155 seconds.
[2026.09.02-11.57.33:609][612]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1228603258] EnemyHP: 66.0
[2026.09.02-11.57.33:609][612]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1233633259] EnemyHP: 66.0
[2026.09.02-11.57.34:070][652]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 90.0
[2026.09.02-11.57.34:081][653]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 80.0
[2026.09.02-11.57.36:073][822]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1228603258] EnemyHP: 32.0
[2026.09.02-11.57.36:153][829]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 70.0
[2026.09.02-11.57.36:426][852]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 60.0
[2026.09.02-11.57.38:463][ 26]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1228603258] EnemyHP: 0.0
[2026.09.02-11.57.38:556][ 34]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1233633259] EnemyHP: 32.0
[2026.09.02-11.57.38:938][ 67]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 50.0
[2026.09.02-11.57.41:961][324]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869F2FD02_1233633259] EnemyHP: 0.0
[2026.09.02-11.57.51:149][ 95]LogWorld: BeginTearingDown for /Game/ThirdPerson/UEDPIE_0_Lvl_ThirdPerson
```

**이 판에 `LogCharacterMovement` 줄이 하나도 없다.** 그 카테고리 전체가 여전히 8줄이고 마지막이 `11.35.16`이다.

**MCP 읽기 — `HeldItemMesh`의 `BodyInstance` 변경 전후. 발췌다.**

```
전: "objectType":"ECC_WorldDynamic","collisionEnabled":"QueryAndPhysics","collisionProfileName":"BlockAllDynamic"
후: "objectType":"ECC_WorldStatic","collisionEnabled":"NoCollision","collisionProfileName":"NoCollision"
```

### 요약 — 한글

**새로 만든 것**

- `/Game/Progression/BP_StageRoom` — `Actor` 파생. 이 세션의 유일한 새 애셋이다. `/Game/Progression` 폴더도 새로 생겼다
- 컴포넌트 둘 — `DefaultSceneRoot`(`SceneComponent`)와 그 자식 `DropPoint`(`ArrowComponent`, 상대 위치 `(0,0,20)`)
- 변수 셋 — `EnemiesAlive`(`Integer`, `0`), `KeyToDrop`(`DataTableRowHandle`, 빈 핸들), `bIsFinalRoom`(`Boolean`, `false`)
- 함수 둘 — `RegisterEnemy`, `NotifyEnemyDied`

**`BP_Enemy`에 더한 것**

- `OwningRoom` — `BP_StageRoom` 오브젝트 참조. 21번째 변수다. 타입이 `BP Stage Room Object Reference`로 잡혔다
- `EventBeginPlay` — `Set CurrentHP`와 `Think` 사이에 `Utilities|IsValid` 매크로를 끼웠다. `Is Valid` → `RegisterEnemy` → `Think`, `Is Not Valid` → **같은** `Think`
- `EventAnyDamage` — `Branch(CurrentHP <= 0)`의 `True`와 `DestroyActor` 사이에 두 번째 `IsValid` 매크로. `Is Valid` → `NotifyEnemyDied` → `DestroyActor`, `Is Not Valid` → **같은** `DestroyActor`
- `Think` 본체와 `EventTick`은 안 건드렸다. 편집 전후 `read_graph_dsl` 출력이 글자까지 같다

**레벨에 한 것 (`Lvl_ThirdPerson`)**

- `Room1` — `BP_StageRoom` 인스턴스, `(840, 1130, 0)`. `KeyToDrop = DT_Items:Key_Stage1`, `bIsFinalRoom = false`. `DropPoint` 월드 `(840, 1130, 20)`
- `Room2` — `(4000, 0, 0)`. `KeyToDrop` 비어 있음, `bIsFinalRoom = true`
- `Enemy_R1_A` `(-1400, 0, 90)` / `Enemy_R1_B` `(-1400, 150, 90)` 신규 배치. 둘 다 `OwningRoom = Room1`
- 기존 적 둘(`(4000, 0, 90)`, `(4000, 150, 90)`)에 `OwningRoom = Room2`
- `BP_ItemPickup` 하나 삭제 — `(840, 1130, 0)`의 `Key_Stage1`. 픽업이 7개에서 6개가 됐고 남은 여섯에 `Key_Stage1`은 없다

**애니메이션에 한 것**

- `AM_Player_Attack`의 `AttackHit` 윈도우 끝을 `0.496946` → `0.534953`초로 넓혔다. 창 길이 `0.209040` → `0.247048`초. 시작 `0.287906`초는 안 건드렸다. **사용자 수작업이다** — MCP로는 노티파이를 쓸 수 없다

**플레이어에 한 것**

- `BP_ThirdPersonCharacter`의 `HeldItemMesh` 컴포넌트 `Collision Presets`를 `BlockAllDynamic` → `NoCollision`. `collisionEnabled`가 `QueryAndPhysics` → `NoCollision`, `objectType`이 `ECC_WorldDynamic` → `ECC_WorldStatic`으로 따라 바뀌었다(프리셋에 딸린 값이다). `RelativeLocation`·`RelativeScale3D`·`bGenerateOverlapEvents`·`CanCharacterStepUpOn`은 그대로다

**안 바꾼 것**

`BP_Enemy`의 기존 변수 20개 값 전부, `BP_Door`의 그래프·변수·CDO 전부, `BP_ItemPickup` 애셋, `BP_ThirdPersonCharacter`의 변수·그래프·다른 컴포넌트 전부, `BP_ThirdPersonGameMode`, `DT_Items`, 남은 픽업 여섯, 적 회전 관련 값 전부, `AM_Enemy_Attack`.

## 분석

### 무엇을 만들었나

**애셋 (`/Game/Progression/BP_StageRoom`)**

| 덩어리 | 실제 값 |
|---|---|
| 부모 클래스 | `Actor` |
| 컴포넌트 | `DefaultSceneRoot`(`SceneComponent`, `(0,0,0)`) / `DropPoint`(`ArrowComponent`, 상대 `(0,0,20)`) |
| `EnemiesAlive` | `Integer`, `0`, `Instance Editable` OFF |
| `KeyToDrop` | `DataTableRowHandle`, 빈 핸들, `Instance Editable` ON |
| `bIsFinalRoom` | `Boolean`, `false`, `Instance Editable` ON |
| 디스크 | `93,029`바이트, `18:57:21` |

**함수 `RegisterEnemy`** — 입력·출력 없음. `EnemiesAlive = EnemiesAlive + 1` 하나.

**함수 `NotifyEnemyDied`** — 입력·출력 없음.

```
Set EnemiesAlive = EnemiesAlive - 1
  -> Branch (EnemiesAlive == 0)
       True -> Branch (bIsFinalRoom)
                 True  -> GetPlayerCharacter(0) -> Cast To BP_ThirdPersonCharacter
                          -> ShowHUDMessage("STAGE CLEAR")
                 False -> SpawnActor BP_ItemPickup
                            Transform = MakeTransform(DropPoint.GetWorldLocation, (0,0,0), (1,1,1))
                            CollisionHandlingOverride = AlwaysSpawn
                            ItemRow = KeyToDrop
       False -> (미연결)
```

`Cast Failed` 핀은 미연결이다. 캐스트가 실패하면 아무 일도 안 일어난다.

**`BP_Enemy` — `OwningRoom` 하나와 노드 여섯**

| 노드 | 역할 | 위치 |
|---|---|---|
| `K2Node_MacroInstance_33` | `BeginPlay`의 `IsValid` | `(2740, 3260)` |
| `K2Node_CallFunction_117` | `RegisterEnemy` | `(3020, 3260)` |
| `K2Node_MacroInstance_34` | `AnyDamage`의 `IsValid` | `(2620, 4830)` |
| `K2Node_CallFunction_118` | `NotifyEnemyDied` | `(2900, 4830)` |
| `K2Node_VariableGet_92` / `_93` | `Get OwningRoom` 둘 | — |

`Think(_82)`는 원래 있던 노드 그대로고 exec 입력에 연결이 둘 붙었다. `DestroyActor(_3)`도 하나 그대로다.

**레벨 (`Lvl_ThirdPerson`, One File Per Actor)**

| 액터 | 위치 | 값 |
|---|---|---|
| `Room1` | `(840, 1130, 0)` | `KeyToDrop = DT_Items:Key_Stage1`, `bIsFinalRoom = false`, `EnemiesAlive = 0` |
| `Room2` | `(4000, 0, 0)` | `KeyToDrop` 비어 있음, `bIsFinalRoom = true`, `EnemiesAlive = 0` |
| `Enemy_R1_A` | `(-1400, 0, 90)` | `OwningRoom = Room1` |
| `Enemy_R1_B` | `(-1400, 150, 90)` | `OwningRoom = Room1` |
| 기존 적 A | `(4000, 150, 90)` | `OwningRoom = Room2` |
| 기존 적 B | `(4000, 0, 90)` | `OwningRoom = Room2` |

남은 픽업 여섯 — `(1130, 870, 20)` `Potion_Small`, `(1150, 1250, 20)` `Potion_Small`, `(300, 0, 20)` `Knife`, `(440, 700, 0)` `Ball_Test`, `(1140, 1090, 20)` `Potion_Small`, `(690, 670, 20)` `Potion_Small`.

**플레이어 (`BP_ThirdPersonCharacter`의 `HeldItemMesh`)**

| 값 | 전 | 후 |
|---|---|---|
| `collisionProfileName` | `BlockAllDynamic` | `NoCollision` |
| `collisionEnabled` | `QueryAndPhysics` | `NoCollision` |
| `objectType` | `ECC_WorldDynamic` | `ECC_WorldStatic` |
| `RelativeLocation` | `(0,0,0)` | `(0,0,0)` |
| `RelativeScale3D` | `0.15` | `0.15` |
| `bGenerateOverlapEvents` | `true` | `true` |
| `CanCharacterStepUpOn` | `ECB_Yes` | `ECB_Yes` |
| 디스크 | — | `834,549`바이트, `20:46:23` |

**애니메이션 (`AM_Player_Attack`)**

| | 시작 | 끝 | 창 길이 |
|---|---|---|---|
| 변경 전 | `0.287906` (f8.64) | `0.496946` (f14.91) | `0.209040` |
| 변경 후 | `0.287906` (f8.64) | `0.534953` (f16.05) | `0.247048` |
| 적 `AM_Enemy_Attack` | `0.304194` (f9.13) | `0.532238` (f15.97) | `0.228044` |

프레임 값은 `SequenceLength 1.0`, 30fps 기준으로 초에서 환산한 것이다. **초 값이 원본이다.**

### 기술적으로 맞게 짚은 부분

**`GameMode`를 한 줄도 안 건드린 것.** `07-재설계-우선순위.md`가 원본의 병으로 지목한 것이 `Stage 1/2/3 Spawn` 함수 세 개, `Switch on Int` 세 갈래, `Is Stage 1/2/3 Clear?` bool 세 개였다. 진행 상태를 방 액터가 들고 있게 하면 **`GameMode`에 스테이지 번호가 아예 안 생긴다.** 방을 하나 더 만들 때 고칠 코드가 0줄이고 액터 하나만 놓으면 된다. 원본이 "스테이지 하나 늘리면 최소 6군데"였던 것과 대비된다.

**액터 방식을 고른 근거를 자원이 아니라 좌표의 주인으로 잡은 것.** 사용자가 `자원 덜 쓰고`를 기준으로 제시했는데, 액터 두 개는 `Tick`도 안 쓰고 메모리도 무시할 수준이라 **자원으로는 갈리지 않는다.** 실제로 갈린 것은 `D`의 답(방마다 고정 지점)이었다. `GameMode`는 레벨에 인스턴스가 없어서 디테일 패널에서 레벨 액터를 꽂을 수 없다. 그러면 좌표를 BP 기본값에 숫자로 박거나 태그 문자열로 찾아야 하는데, 앞은 `07` 문서가 지목한 "데이터가 코드에 박힌다"이고 뒤는 같은 문서가 `Item_Name` 문자열 비교를 버리라고 한 이유(오타가 컴파일 에러 없이 통과)와 같다. **레벨 좌표는 레벨에 있는 액터가 주인이어야 한다**로 정리했다.

**`Expose on Spawn`을 다시 만들지 않은 것.** 열쇠를 스폰할 때 메시가 뜨려면 `ConstructionScript`가 `ItemRow`를 읽은 뒤에 돌아야 한다. `BP_ItemPickup`을 고치거나 `RerunConstructionScripts` 우회를 만들 뻔했는데, `2026-08-30-drop-item.md`를 먼저 뒤져서 **`ItemRow`의 `Expose on Spawn`이 이미 켜져 있다**는 것을 찾았다. 결정 사다리 2번에서 끝났고 `BP_ItemPickup`을 한 글자도 안 건드렸다. `SpawnActor` 노드에 `ItemRow` 핀이 실제로 나온 것으로 전제가 맞았음이 확인됐다.

**`MakeTransform`의 `Scale` 기본값을 추측하지 않고 확인한 것.** DSL이 인자 하나만 보여줘서 나머지가 기본값이라는 것만 알 수 있었다. `Scale`이 `(0,0,0)`이면 열쇠가 스케일 0으로 스폰돼 **안 보이는데 존재하는** 상태가 된다 — PIE에서 "안 나왔다"로 보이고 원인을 못 찾을 종류다. `KismetMathLibrary.h:3932`에서 `FVector Scale = FVector(1,1,1)`를 확인하고, 다시 실제 노드 `K2Node_CallFunction_13`의 핀값이 `1.000000,1.000000,1.000000`인 것까지 읽었다. **헤더 기본값과 실제 핀값을 둘 다 본 것**이 맞다 — `2026-08-29-중간점검.md`에 "헤더의 지정자만 보고 노드 모양을 단정한 것"이 실수로 적혀 있다.

**`Is Valid`를 매크로로 지시한 것.** 같은 중간점검에 "`IsValid`를 순수 함수 + `Branch`로 지시 → 매크로 자체가 분기. 터미널이 잡음"이 적혀 있다. 이번에는 명령문에 `the one with "Is Valid" and "Is Not Valid" exec output pins`라고 못 박아서 왕복이 없었다.

**널 체크를 깎지 않은 것.** `OwningRoom`이 `None`일 수 있다. 두 곳 다 `IsValid`로 감쌌고 `Is Not Valid` 경로도 원래 흐름으로 이었다. 이걸 안 했으면 `OwningRoom`이 비어 있는 적은 `Think`가 안 불려 **AI가 통째로 안 돌고**, 죽어도 `DestroyActor`가 안 불려 **HP 0인 채로 서 있게** 된다.

**적 조준 문제를 고치지 않고 접은 것.** 원인은 그래프에 명백히 있었다. 그런데 사용자가 "공격 모션이 바뀔 것"이라고 했다. 모션이 바뀌면 루트모션·노티파이 구간·조준이 한꺼번에 다시 걸리므로 **지금 조준만 붙이면 그때 버린다.** 결정 사다리 1번이다.

**적 회전 경로를 하나씩 배제한 것.** "회전 노드가 없다"만으로 단정하지 않고, 적을 돌릴 수 있는 경로를 전부 확인했다 — 컨트롤러(`bUseControllerRotationYaw = false`), AI 컨트롤러의 focus(`AIControllerClass`가 기본 `/Script/AIModule.AIController`라 커스텀 focus 없음), 이동 방향(`bOrientRotationToMovement = true`지만 움직일 때만), 배치 인스턴스 오버라이드(둘 다 CDO와 동일), 루트모션(`bEnableRootMotion = true` + `RootMotionFromMontagesOnly`라 **적용된다**). 마지막 것은 처음 가설("회전 입력이 아예 없다")을 반증했고, 그 자리에서 정정했다. 맞는 문장은 "적을 돌리는 경로 둘 다 플레이어를 향해 돌지 않는다"였다.

**루트모션이 왜 증상을 간헐적으로 만드는지까지 설명한 것.** 사용자가 "지금 했을 땐 문제 없어 보인다"고 했을 때, 그것을 반증으로 받지 않고 구조로 설명했다. `MM_Attack_01`의 루트모션이 공격마다 적을 앞으로 밀어서 거리가 바뀌고, `AttackRange 150`을 벗어나면 다음 `Think`가 추격으로 가면서 `bOrientRotationToMovement`이 자동으로 재조준한다. **버그가 구조적으로 간헐적이다.**

**`AM_Player_Attack`의 실제 값을 눈대중이 아니라 바이너리에서 읽은 것.** 기록에 "플레이어 9~14, 적 9~16"으로 남아 있던 값이 **양쪽 다 틀렸다.** 실제는 플레이어 `8.64~14.91`, 적 `9.13~15.97`이었다. 저장된 `.uasset`을 커밋본과 바이트 비교하니 실제 데이터 변경이 세 자리(끝 시각 두 곳, 창 길이 한 곳)뿐이고 나머지는 헤더 해시였다. 시작 시각이 소수점 여섯 자리까지 같아서 **끝만 밀었다는 것이 증명됐다.** 09-02 knife 기록의 "창 길이 약 0.21초"가 실측 `0.209040`과 맞아 교차 검증이 됐다.

**`HeldItemMesh`의 콜리전을 끄기 전에 그 콜리전을 쓰는 곳이 없다는 것을 먼저 확인한 것.** 끄는 것이 정답인 근거가 "안 쓰니까"여야 하는데, 그걸 세 갈래로 확인했다 — 칼 히트 판정은 `HeldItemMesh`의 **위치만** 읽어 `MultiSphereTraceForObjects`를 쏘므로 콜리전을 안 쓴다, EventGraph의 `HeldItemMesh` 노드 넷이 전부 `Get`이고 `K2Node_ComponentBoundEvent`가 하나도 없다(오버랩·히트 델리게이트에 물린 게 없다), `RefreshHeldItem`이 `SetStaticMesh`와 `SetRelativeTransform`만 부르므로 런타임에 콜리전을 바꾸는 곳도 없다. **세 번째를 안 봤으면 CDO를 고쳐도 런타임에 덮어써질 가능성이 남았다.**

**끼임의 근거를 화면 인상이 아니라 로그 8줄로 잡은 것.** `LogCharacterMovement`가 매번 `Component:HeldItemMesh`와 `PenetrationDepth`를 찍고 있었다. 그리고 고친 뒤의 판정도 없음의 증거로 두지 않고 **전후 비교**로 만들었다 — 같은 방1 근접전에서 `11:11` 3줄, `11:35` 1줄, 변경 후 `11:57` 0줄이고, `11:57` 판에서 플레이어 체력이 `90 → 50`까지 깎였으니 접촉은 확실히 있었다.

**손대지 않은 것이 정답이었던 것 — 플레이어 `BeginPlay`의 HP 초기화.** 심문 5번의 답으로 "넣지 말자"를 골랐고, 근거를 레벨에서 읽었다. `find_actors`로 배치된 `BP_ThirdPersonCharacter` 인스턴스가 **0개**임을 확인했고, 폰은 항상 `PlayerStart`에서 스폰되므로 CDO 기본값 `100`이 곧 시작 체력이다. 08-31 기록에 리스폰된 폰 `_2`의 `CurrentHP`가 당시 기본값 `75`였다는 실측이 남아 있어 교차 검증됐다.

**`git status`가 세션 시작에 깨끗했다는 것을 근거로 터미널 보고를 정정한 것.** 명령 1의 보고가 `The three M entries ... predate this task`라고 했는데, 세션 시작 시 트리는 비어 있었다. 세 파일 다 이 세션 중에 dirty가 된 것이다. **작업 전 커밋해두는 것이 실제로 증거 역할을 했다.**

### 확인한 것 / 확인 못 한 것

**확인한 것 — 전부 에디터에서 다시 읽었거나 디스크에서 확인한 것이다.**

- `BP_StageRoom`의 컴포넌트 둘, 변수 셋의 타입과 기본값 — `list_variables`와 CDO `get_properties`
- 두 함수의 그래프 구조 — `read_graph_dsl` 전문
- `SpawnActor` 노드에 `ItemRow` 핀이 실제로 존재하고 `KeyToDrop`이 물려 있는 것
- `MakeTransform` 노드 `_13`의 `Scale = (1,1,1)`, `Rotation = (0,0,0)` — `get_pin_value`
- `OwningRoom`의 타입이 `BP Stage Room Object Reference`로 잡힌 것 — `get_node_type_pins`
- **`BP_Enemy`의 `Is Not Valid` 두 경로가 실제로 연결된 것** — `get_node_infos`. `Think(_82)`의 exec 입력에 연결이 둘, `_34`의 `Is Not Valid`가 `DestroyActor(_3)`로 간다
- `Think` 노드와 `DestroyActor` 노드가 각각 하나뿐인 것 — `find_nodes`
- `Think` 본체와 `EventTick`이 편집 전후 동일한 것 — DSL 대조
- 방 액터 둘의 라벨·위치·`KeyToDrop`·`bIsFinalRoom`·`EnemiesAlive`, `DropPoint` 상대 위치 — 배치 인스턴스에서 읽음
- 적 넷의 위치와 `OwningRoom`이 각각 올바른 방을 가리키는 것 — 배치 인스턴스에서 읽음. **`None`인 적 없음**
- 남은 픽업 여섯의 위치와 `ItemRow`, 그중에 `Key_Stage1`이 없는 것
- 저장이 디스크에 도달한 것 — 외부 액터 파일 42 → 44 → 43개, `git status`의 `D` 항목
- `BP_Door`와 `BP_Enemy`가 세션 중 dirty가 됐지만 **로직은 안 바뀐 것** — DSL 대조, 변수 목록 대조, CDO 값 대조, 파일 크기 동일, `BP_Door`의 비헤더 차이가 `97195~97226` 한 덩어리 32바이트뿐
- `AM_Player_Attack`의 노티파이 시각 변경분 — 바이너리 디코딩
- `MM_Attack_01.bEnableRootMotion = true`, `ABP_Unarmed.RootMotionMode = RootMotionFromMontagesOnly`
- 적 회전 경로 전부가 플레이어를 향하지 않는다는 것 — CDO와 배치 인스턴스 양쪽
- 레벨에 배치된 `BP_ThirdPersonCharacter` 인스턴스가 0개라는 것
- `DT_Items`의 행 넷 — `Key_Stage1`, `Potion_Small`, `Ball_Test`, `Knife`
- `get_node_type_pins`가 응답에 담은 `_26` 노드가 그래프에 실제로 추가되지는 않았다는 것 — `find_nodes`로 재확인
- **노티파이 창 회귀 검사 1(이중 타격) — 통과.** `11:11` UTC 판에서 적 넷이 전부 죽었고 칼 히트 12번이 **전부 한 번씩만** 찍혔다. 플레이어 칼 데미지는 34이고 모든 적이 `100 → 66 → 32 → 0`으로 정확히 세 번에 죽었다. 같은 스윙에서 두 번 깎인 적이 없다
- **노티파이 창 회귀 검사 3(적 둘 각각 한 번씩) — 통과.** `08:01:58.520`의 **같은 밀리초, 같은 프레임 `[434]`** 에 적 둘이 각각 `66.0`을 찍었다. 한 스윙이 둘을 때렸고 각자 한 번씩만 들어갔다
- **`MultiTrace`가 한 프레임에 히트 둘을 반환하는 경로.** 위와 같은 로그다. `2026-09-02-two-enemies-friendly-fire.md`가 "두 번 시도해 두 번 다 연속 프레임이었다"고 미확인으로 남긴 것인데, **같은 프레임 사례가 로그에 있다**
- **UE Terminal의 경고가 어디로 가는지.** Output Log의 `LogScript` 카테고리다. `LogsToolset.GetLogEntries`로 읽힌다. **열 번을 "못 받았다"고 적어온 항목인데 읽을 방법이 처음부터 있었다**
- **명령 2가 한 번 미끄러졌던 것.** 터미널이 일반 `Game|SpawnActorfromClass`를 먼저 시도해 `Unknown input pin "ItemRow"`로 실패했고, 그 뒤 클래스 특화 노드 `Game|SpawnActorBPItemPickup`으로 바꿔 성공했다. 최종 결과는 맞지만 **당시에는 이 실패를 몰랐다**
- **명령 6·7의 저장 실패 원문.** `Asset does not exist: /Game/__ExternalActors__/...` 뒤에 `Failed to save 'Room1'` / `'Room2'` / `'Enemy_R1_A'`가 붙는다. 아직 디스크에 없는 OFPA 신규 액터 패키지를 경로로 저장하려다 실패한 것이다
- **블루프린트 컴파일 경고가 세션 전체에 하나도 없었다는 것.** `LogBlueprint` 카테고리에 `Compiling Blueprint '...'` 줄 19개뿐이고 `Warning`도 `Error`도 없다. **"경고 원문을 못 받았다"의 답은 "경고가 없었다"였다**
- **`HeldItemMesh`의 콜리전을 쓰는 곳이 없다는 것.** 히트 판정은 위치만 읽어 스피어 트레이스를 쏜다, EventGraph에 `K2Node_ComponentBoundEvent`가 없다, `RefreshHeldItem`이 콜리전을 안 건드린다 — 셋 다 확인했다
- **콜리전을 끈 뒤 끼임이 사라진 것.** `LogCharacterMovement` 카테고리가 여전히 8줄이고 마지막이 `11.35.16`이다. 변경 후 판(`11:57`)에서 한 줄도 안 나왔다. 같은 방1 근접전 기준 `11:11` 3줄 → `11:35` 1줄 → `11:57` 0줄
- **콜리전을 껐는데도 칼 히트 판정이 안 깨진 것.** 변경 후 판에서 적 둘이 각각 `100 → 66 → 32 → 0`으로 34씩 정확히 세 번에 죽었다. 첫 두 줄이 **같은 밀리초, 같은 프레임 `[612]`** 라 한 스윙이 둘을 각각 한 번씩 때린 사례가 변경 후에도 재현됐다

**확인 못 한 것**

- **합격 기준 네 개의 PIE 결과.** 사용자가 `1부터 4까진 다잘된거같다고 생각`이라고 했다. **AI는 PIE를 안 봤다.** 근거는 사용자 관찰 하나뿐이고 로그 숫자를 못 받았다. 이유 — 사용자가 PIE를 직접 돌렸고 출력을 붙이지 않았다
- **아이템을 줍고 버리는 것이 콜리전을 끈 뒤에도 되는지.** 사용자가 `아까 아이템 줍고 버리기 잘 됬어`라고 확인했는데, **그 "아까"가 변경 후 판(`11:57`)인지 그 전 판인지 확정하지 않았다.** 로그로 확인되는 것은 변경 후 판에서 칼을 들고 휘둘러 데미지가 나갔다는 것까지다 — `RefreshHeldItem`이 메시를 붙였다는 뜻이지 줍고 버리기가 됐다는 증거는 아니다
- **`BP_StageRoom` 변수 셋의 `Instance Editable` 플래그.** MCP에 읽는 도구가 없다(`get_variable_category`와 `get_variable_replication`은 있는데 이것만 없다). 터미널도 `NewVariables` 읽기에 실패했다
- **`BP_Enemy.OwningRoom`의 `Instance Editable`.** 같은 이유로 직접은 못 읽었다. 다만 배치 인스턴스 넷에 값이 실제로 꽂혔고 PIE가 돌았으므로 **켜져 있다는 것이 간접 증명됐다**
- **`BP_Enemy`와 `BP_Door`가 dirty가 된 원인.** 세션 시작 시 트리는 깨끗했다. AI의 `read_graph_dsl` 읽기가 원인인지 터미널의 저장이 원인인지 **구분 못 했다.** `BP_Enemy`는 1911바이트, `BP_Door`는 49바이트가 갈렸는데 둘 다 파일 크기는 같다
- **`AM_Player_Attack` 노티파이 창 회귀 검사 2 — 창 밖에서 판정이 열려 있는지.** 1과 3은 로그로 통과했지만 2는 **판정할 수 없다.** 로그에 "플레이어가 가만히 서 있었다"는 표시가 없다. 정황은 있다 — `11:11:25.891`에 한 마리가 죽은 뒤 `11:11:39.010`까지 **13초 동안 살아 있는 적의 `EnemyHP` 줄이 하나도 없다.** 하지만 그 사이 플레이어가 무엇을 했는지 모르므로 없음의 증거일 뿐이다
- **적이 옆으로 도는 플레이어를 못 따라가는 것의 PIE 재현.** 그래프 근거는 확보했지만 재현하지 않았다. 이유 — 사용자가 접기로 했다
- **`D 방마다 고정 지점을 두개 하자`의 해석.** "두자"의 오타로 읽고 방마다 하나씩 뒀다. 사용자에게 확인하지 않았다
- **`ShowHUDMessage`의 표시 지속 시간.** 기존 함수를 그대로 쓰기로 했고 그래프를 안 읽었다
- **명령 5가 실제로 실행됐는지.** `BP_Enemy.uasset`의 mtime이 `19:27:13`에서 안 움직였으니 **아무것도 안 바뀐 것은 확실하다.** 실행 자체가 안 된 것인지, 실행됐는데 이미 연결이 있어서 no-op이었는지는 모른다

### 남는 리스크

- **`EnemiesAlive`가 `== 0`으로만 발동한다.** 어떤 이유로든 `NotifyEnemyDied`가 한 번 더 불리면 값이 `-1`이 되고 그 뒤로는 영원히 `0`을 못 만난다. 지금은 `DestroyActor` 직전에 한 번만 불리므로 문제가 안 되지만, 스포너나 리셋이 붙으면 이 가정이 깨진다
- **방을 안 꽂은 적은 조용히 카운트에서 빠진다.** `IsValid`가 널을 막아주지만 "이 적은 어느 방에도 안 속한다"는 상태가 **경고 없이 성립한다.** 방1에 적을 하나 더 놓고 `OwningRoom`을 안 꽂으면 나머지 둘만 죽여도 열쇠가 나온다
- **`EnemiesAlive`가 `BeginPlay` 등록에만 의존한다.** 적이 레벨에 배치된 것을 전제로 한다. 스포너를 붙이면 스폰 시점에 `RegisterEnemy`를 불러야 하는데 잊으면 카운트가 어긋난다
- **플레이어가 죽어도 진행이 안 되돌아간다.** 5번 답대로 의도한 것이다. 열쇠를 줍고 쓰기 전에 죽는 경우는 **닫힌 문이 방2 적을 막기 때문에** 성립하지 않는데, 이건 **지금 레벨 구조에 의존하는 안전**이다. 로비를 실제로 만들거나 문 여는 순서가 바뀌면 깨진다
- **`Room1`의 `DropPoint`가 원래 열쇠 픽업이 있던 자리다.** 좋은 자리라는 근거는 "거기 있었다"뿐이다. 방1의 적은 `(-1400, *)`에 있으므로 **전멸시킨 자리에서 열쇠까지 2200 이상 걸어와야 한다**
- **적 공격에 조준이 없다.** 접기로 했지만 사라진 문제는 아니다. 붙어서 원을 그리며 도는 플레이에서 적은 처음 멈춘 방향으로 계속 지른다
- **`ReturnSightRange 300` 안에서는 시야각을 안 본다.** `SightHalfAngle 60`은 `SightRange` 쪽에만 걸린다. 등 뒤에 서 있어도 공격에 들어가고, 조준이 없으니 등을 보인 채 허공을 친다
- **`AM_Player_Attack`의 창이 적보다 `0.019`초 길고 시작이 `0.49`프레임 이르다.** 끝만 맞췄다
- **방1 적이 `SightRange 1200` 경계 근처에 있다.** `(-1400, *)`이라 시작 지점에서 200 여유뿐이다. 플레이어가 조금만 다가가면 둘이 동시에 붙는다
- **`FoundSlotIndex`가 아직 `BP_ThirdPersonCharacter`에 남아 있다.** `2026-08-29-중간점검.md`가 죽은 변수로 지목한 것이고 닷새째다
- **`get_node_type_pins`가 그래프에 없는 노드를 응답에 담는다.** 이 응답으로 노드 수를 세면 틀린다
- **`read_graph_dsl`로 수렴 간선이 있는 그래프를 감사할 수 없다.** 이번에 실제로 오진을 만들었다
- **One File Per Actor 레벨에서 터미널이 저장을 못 한다.** 세 번 다 사용자가 `Ctrl+S`를 눌러야 했다. 실패 원문은 `Asset does not exist: /Game/__ExternalActors__/...` → `Failed to save 'Room1'`이다
- **`HeldItemMesh`의 `bGenerateOverlapEvents`와 `CanCharacterStepUpOn`이 켜진 채 남아 있다.** `NoCollision`이라 둘 다 아무 일도 안 하지만, 나중에 이 컴포넌트를 보는 사람에게 "오버랩을 쓰나?"라는 오해를 준다. 지시할 때 일부러 안 건드리게 했다
- **`objectType`이 `ECC_WorldStatic`으로 바뀐 것.** `NoCollision` 프리셋에 딸린 값이고 콜리전이 꺼져 있어 의미가 없지만, **내가 지시한 변경이 아니라 프리셋이 끌고 온 변경이다**
- **끼임을 없앤 것이지 근접전에서 적과 플레이어가 겹치는 것 자체를 다룬 것은 아니다.** 칼이 안 막을 뿐 캡슐끼리는 여전히 부딪친다
- **터미널이 실패한 뒤 스스로 다른 노드로 갈아타도 나는 모른다.** 명령 2에서 `Game|SpawnActorfromClass` → `Game|SpawnActorBPItemPickup` 전환이 그랬다. 결과가 맞으면 미끄러진 흔적이 보고에 안 남는다
- **PIE 종료 시 `LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance`.** 매 판 뜨는지, 이번만인지 확인 안 했다

### 총평

**요청은 충족됐다.** 5단계 사양의 범위가 전부 들어갔고 합격 기준 넷을 사용자가 PIE에서 통과 확인했다. 커밋 둘로 끊었고 작업 트리는 깨끗하다.

**실질적 난이도는 블루프린트가 아니었다.** `BP_StageRoom`은 컴포넌트 둘, 변수 셋, 함수 둘이고 `BP_Enemy` 편집은 노드 여섯이다. 시간이 든 곳은 셋이다.

첫째, **심문 답과 레벨의 실제 상태가 어긋난 것을 조사에서 잡은 것.** 사용자가 "적 전멸 시 열쇠 드롭"을 골랐는데 **적 둘이 전부 방2에 있었고 방1에는 0마리였다.** 그리고 5번 답의 근거였던 "로비"가 현재 레벨에 없었다 — 방1과 방2가 문 하나로 직결이다. 로비 허브는 `07-재설계-우선순위.md`가 원본에서 가져오자고 적은 기획이지 만들어진 것이 아니다. 결론(리셋 없이도 안전)은 살았지만 이유가 달랐다. 조사를 안 했으면 **스테이지 1이 성립하지 않는 사양을 쓸 뻔했다.**

둘째, **저장이 세 번 미끄러진 것.** 명령 6·7·8 모두 에디터에는 반영됐는데 디스크에 안 갔다. 이 레벨이 One File Per Actor라서 `.umap` mtime이 안 움직이고, 터미널의 경로 기반 저장 도구가 전부 실패했다. 매번 `git status`와 `__ExternalActors__` 파일 수로 잡아서 사용자에게 `Ctrl+S`를 요청했다. **`.umap` mtime을 저장 증거로 쓰던 습관이 이 레벨에서는 안 통한다.**

셋째, **내가 만든 오진.** 가장 큰 실수다. `read_graph_dsl`이 수렴 간선을 생략한다는 것은 `2026-08-29-중간점검.md`에 **내가 적어둔 사실**이고, 명령 4는 두 경로를 **같은 노드로 수렴시키라**고 내가 쓴 것이다. 그런데 DSL에서 `Is Not Valid`가 비어 보이자 **"적 AI가 통째로 안 돈다"고 단정하고 사용자에게 불필요한 명령을 하나 더 냈다.** 도구의 한계를 알면서 그 도구의 출력만으로 판정한 것이다. `get_node_infos`로 봤으면 처음부터 연결이 보였다. 명령 5는 아무것도 안 바꿨고 사용자 시간만 썼다. **이 그래프를 앞으로 볼 때는 DSL이 아니라 `get_node_infos`로 본다.**

**터미널 출력을 거의 못 받은 채 진행한 것도 이번 세션의 특징이다.** 명령 여덟 개 중 하나만 출력이 왔고, 나머지는 AI가 MCP로 직접 읽어 검증했다. 결과적으로 검증 자체는 오히려 촘촘해졌다 — 노드 단위, 핀 단위, 바이트 단위까지 갔다. 그리고 명령 1의 보고에 사실과 다른 문장(`predate this task`)이 하나 있었는데, 그것도 `git status`를 세션 시작에 찍어둔 덕에 잡혔다.

**세션이 끝난 뒤에야 경고를 읽는 방법을 찾은 것이 이번의 두 번째 실수다.** 열 번을 "컴파일 경고 원문을 못 받았다"고 적어왔는데, `LogsToolset.GetLogEntries`로 `LogScript`와 `LogBlueprint` 카테고리를 읽으면 그대로 나온다. **읽을 방법이 처음부터 있었고 툴 목록에도 있었다.** 실제로 읽어보니 명령 2가 한 번 미끄러졌던 것(`Unknown input pin "ItemRow" on Game|SpawnActorfromClass`)과 명령 6·7의 저장 실패 원문(`Failed to save 'Room1'`)이 다 있었다. 그리고 **블루프린트 컴파일 경고는 세션 전체에 하나도 없었다** — 열 세션 동안 "못 받았다"고 적어온 것의 답이 "없었다"였다. 명령마다 "경고를 보고하라"고 쓰는 대신 **끝나고 로그를 직접 읽으면 된다.** 명령 9부터 그렇게 했다.

**마지막에 붙인 `HeldItemMesh` 작업은 이 세션에서 가장 값이 싼 것이었다.** 설정 하나를 바꿨고, 근거는 이미 로그에 8줄 쌓여 있었다. 그런데 **여덟 번 다 아무도 안 봤다.** 화면으로는 "적이 잠깐 멈칫한다" 정도로만 보였을 것이고, 로그를 안 읽었으면 지금도 몰랐다. 이 프로젝트에서 반복될 종류의 것이다 — `LogCharacterMovement`·`LogScript`·`LogBlueprint`는 요구하지 않아도 쌓이고 있으니 **세션 끝에 한 번 훑는 것이 싸다.**

**MCP 툴 인자 이름을 여섯 번 틀렸다.** `blueprint_path` 대신 `blueprint`, `object` 대신 `instance`, `property_names` 대신 `properties`, `find_nodes`의 필수 `title`, `get_pin_value`의 `pin` 객체, `get_node_type_pins`의 `graph`+`type_id`. 전부 첫 호출에서 에러를 받고 스키마를 보고 고쳤다. 비용은 크지 않았지만 여섯 번은 많다.

## AI의 제안

> **안: (c2).** "배치 유지 + 디스패처"라는 선택의 핵심은 그대로 지킨다. 나중에 스포너를 붙여도 스폰할 때 카운트를 올리면 되니 확장을 막지 않는다. **지금 방이 둘뿐인데 방 클래스를 파는 건 사다리 위쪽에서 걸린다**

심문 단계에서 `GameMode`가 세는 안을 권했다. 얻는 것은 새 BP 0개. 잃는 것은 레벨 좌표의 주인이 없어지는 것. **사용자가 `D`에서 고정 지점을 고르자 AI가 스스로 뒤집어 액터 방식을 권했다.**

> **결정적인 건 D 답이 바뀐 것이다.** "방마다 고정 지점"은 **레벨 좌표**다. 그런데 **GameMode는 레벨에 인스턴스가 없다.**

뒤집은 근거다. 얻는 것은 좌표를 뷰포트에서 끌어 옮길 수 있게 되는 것과 `GameMode`에 스테이지 번호가 안 생기는 것. 잃는 것은 새 BP 클래스 하나와 배치 액터 둘.

> **안: 마지막으로 죽은 적의 위치** (Z만 바닥 높이로 내림). 대안은 방마다 고정 지점을 두는 것

열쇠 드롭 위치로 먼저 낸 안이다. 얻는 것은 "죽인 자리에서 바로 줍는다"는 직관. 잃는 것은 마지막 적의 위치를 붙들어야 하고, 적이 벽에 끼거나 밖으로 밀려난 자리에 열쇠가 떨어질 수 있다는 것.

> **안: 삭제.** 다만 **삭제는 되돌리기 어려우니 승인이 필요합니다.** 지우지 말고 방2로 옮겨두는 것도 가능한데, 그러면 방2에서 쓸 데 없는 열쇠가 굴러다닙니다

방1 바닥의 `Key_Stage1` 픽업 처리안. 얻는 것은 "적을 안 죽여도 문이 열리는" 구멍을 막는 것. 잃는 것은 배치를 되돌리려면 커밋에서 꺼내야 한다는 것.

> **안: `ShowHUDMessage("STAGE CLEAR")`.** 문이 잠겼을 때 쓰는 그 함수를 그대로 쓴다. **표시 지속 시간은 확인 안 했습니다**

클리어 표시안. 얻는 것은 새로 만들 게 없다는 것(결정 사다리 2번). 잃는 것은 문구가 얼마나 떠 있는지 정하지 못한다는 것.

> **`Room1`의 위치를 `(840, 1130, 0)`으로 한 것. 지금 `Key_Stage1` 픽업이 있는 바로 그 자리다. 방 중앙 `(0,0)`은 `PlayerStart`를 받치는 원반 밑이라 열쇠가 가려질 수 있습니다.**

드롭 지점 좌표안. 얻는 것은 값에 출처가 생기는 것(내가 지어낸 숫자가 아니다). 잃는 것은 적을 죽인 자리에서 멀다는 것.

> **적 배치는 명령으로 넣지 말고 에디터에서 직접 끌어 놓으시는 게 나을 수도 있습니다.**

방1 적 좌표를 AI가 정한 것에 대한 단서다. 얻는 것은 손으로 맞춘 위치의 자연스러움. 잃는 것은 좌표가 기록에 안 남는 것.

> **`Ctrl+S`로 레벨을 저장한 다음, `Save All`까지** 눌러주세요.

터미널이 저장 방법을 물었을 때의 답. 얻는 것은 `save_assets([])`로 전부 저장하는 것보다 범위가 좁다는 것. 잃는 것은 사용자 손이 한 번 더 든다는 것.

> **`BP_Door` 제약은 제가 풀겠습니다.** "다른 블루프린트를 건드리지 말라"는 제가 쓴 문장인데 ... 디스크 변경분이 해시 churn 32바이트뿐인 것을 바이트 단위로 확인했습니다

AI가 자기 명령문의 제약을 스스로 푼 것이다. 얻는 것은 터미널이 제약에 막혀 멈추지 않는 것. 잃는 것은 명령문의 제약이 절대적이지 않다는 선례가 생기는 것.

> **커밋** — 지금 작업 트리가 5단계 하나로 깔끔합니다. 다음 작업 전에 끊어두면 `git status`가 다시 증거가 됩니다

세션 마무리 제안. 얻는 것은 다음 세션의 `git status`가 다시 "무엇을 건드렸는가"의 증거가 되는 것. 잃는 것은 없다.

## 다음으로 넘김

**바로 이어서 할 것**

- 없음. 커밋까지 반영됐고 `git status`가 비었다

**결정 필요**

- **`D 방마다 고정 지점을 두개 하자`를 "하나씩"으로 읽은 것이 맞는가.** "두자"의 오타로 봤다. 방마다 두 개를 두라는 뜻이었다면 `BP_StageRoom`에 `DropPoint`를 하나 더 붙여야 한다
- **`Room1`의 `DropPoint` 위치.** 지금 `(840, 1130, 20)`이고 근거는 "원래 열쇠 픽업이 거기 있었다"뿐이다. 방1의 적은 `(-1400, *)`이라 전멸시킨 자리에서 2200 이상 걸어와야 한다
- **`AM_Player_Attack`의 창 시작을 적과 맞출 것인가.** 끝은 `0.08`프레임 차이로 맞췄다. 시작은 플레이어 `0.287906`, 적 `0.304194`로 `0.49`프레임 차이가 남아 있다. 맞추려면 창을 앞에서 깎아야 한다
- **방1 적 좌표 `(-1400, *)`이 적당한가.** AI가 정한 값이다. `PlayerStart(0,0)`에서 1400 떨어져 `SightRange 1200` 밖이라 시작하자마자 안 달려오게 한 것인데, 여유가 200뿐이다
- **`EnemiesAlive`의 `== 0` 판정을 유지할 것인가.** 지금은 맞지만 스포너나 리셋이 붙으면 가정이 깨진다
- **`FoundSlotIndex`를 지울 것인가.** `BP_ThirdPersonCharacter`에 있고 닷새째다. 지우기 전에 `find_nodes`로 참조 0을 확인해야 한다

**확인 필요**

- **`BP_StageRoom`의 `Instance Editable` 셋.** MCP에도 터미널에도 읽는 방법이 없다. My Blueprint 패널의 눈 아이콘을 눈으로 봐야 한다. `KeyToDrop`과 `bIsFinalRoom`은 배치 인스턴스에서 값이 읽히므로 켜져 있을 가능성이 높지만, `EnemiesAlive`가 OFF인지는 모른다
- **`AM_Player_Attack` 노티파이 창 회귀 검사 2.** 1과 3은 로그로 통과했다. 2(창 밖에서 판정이 열려 있는지)만 남았고, 판정하려면 **적 옆에 붙어 아무것도 안 하는 구간을 의도적으로 만들어야 한다**
- **아이템 줍고 버리기가 콜리전을 끈 뒤에도 되는지.** 사용자가 된다고 했으나 그 판이 변경 전인지 후인지 확정하지 않았다. **다음 PIE에서 한 번 주워보고 버려보면 닫힌다**
- **`BP_Enemy`·`BP_Door`가 읽기만 했는데 dirty가 되는 경로.** 세션 시작 시 트리는 깨끗했다. `read_graph_dsl`이 원인인지 저장 쪽인지 구분 못 했다. **단서 하나 — `LogBlueprint`에 `11.11.12`에 두 애셋이 내가 시키지 않았는데 컴파일된 기록이 있다. PIE 시작 직전이다**
- **One File Per Actor 레벨에서 터미널의 경로 기반 저장 도구가 전부 실패하는 것.** 세 번 다 사용자가 `Ctrl+S`를 눌러야 했다. 터미널이 `save_assets([])`(전체 저장)밖에 없다고 보고했다
- **MCP로 그래프를 고친 뒤 Compile을 눌러야 저장이 걸리는 것.** `2026-09-02-two-enemies-friendly-fire.md`에서 넘어온 항목이다. 이번 세션의 애셋 편집(`BP_StageRoom` `18:57:21`, `BP_Enemy` `19:27:13`)은 컴파일+저장 뒤 디스크에 도달했으므로 어긋나지 않았지만, 원인은 여전히 확인 못 했다
- **`get_node_type_pins`가 응답에 그래프에 없는 임시 노드를 담는 것.** 실제로 추가되지는 않는다는 것을 `find_nodes`로 확인했지만 왜 그런지는 모른다
- **적 넷이 서로 밀치는 동작.** 방1에 둘이 늘어 총 넷이 됐다. 관찰하지 않았다
- **닫힌 문이 방2 적을 실제로 막는지.** 열쇠 소실 안전의 근거가 이것인데 적이 늘어난 뒤로 확인하지 않았다
- **`2026-09-02-two-enemies-friendly-fire.md`에서 옮겨온 것.** 적끼리 방지가 실제로 막은 것인지(방지 `Branch`의 `False` 핀에 임시 `PrintString` 한 줄이면 된다), `Sequence` 제거 후 공격 주기(화면 인상만 있다), 배치 인스턴스 `FistRadius`의 덮어쓰기 유무(`FistRadius`를 실제로 튜닝할 때 자연히 드러난다). **`MultiTrace`의 같은 프레임 히트 둘은 이번에 로그로 확인돼 목록에서 뺐다**
- **`2026-09-01-enemy-hp-death.md`의 `확인 필요` 목록.** `arrange_nodes`, `EditorPerProjectUserSettings.ini` 저장 실패, `CaptureViewport`가 에디터 월드를 그리는 것 등이 그 파일에 그대로 있다

**접어둔 것**

- **적 공격의 조준.** 원인 확정됐다 — 공격 경로에 회전 노드가 없고, `bUseControllerRotationYaw = false`, `bOrientRotationToMovement`는 움직일 때만 돈다. 고치려면 `PlayMontage` 직전에 플레이어 쪽으로 `SetActorRotation`(Yaw만, 피치를 지워야 함) 한 번이면 된다. **공격 모션을 교체할 때 다시 연다**
- **적 사망 연출과 액터 제거 분리.** 지금 즉시 `DestroyActor`다. 연출을 넣을 때 같이 한다
- **플레이어 사망 시 방 단위 리셋.** 5번 답에서 나중으로 미뤘다
- **적 스포너.** 3번 답에서 "나중에 가능한지 판단"으로 미뤘다. 지금 구조는 스포너가 스폰 시 `RegisterEnemy`를 부르면 된다
- **적 상태 표시(`ATTACK`/`CHASE`/`RETURN`/`IDLE_HOME`/`IDLE_WAIT`/`NO_PLAYER`) 다시 심기.** 이번 세션에서 "이제 안 해도 될 듯"으로 접었다
- **`HitActorsThisSwing` 이름 바꾸기.** 실제 의미는 "훑힌 액터"인데 이름은 "때린 액터"다. 리네임이 참조를 조용히 끊을 위험이 이름값보다 크다고 판단했다
- **플레이어 `BeginPlay`에 `CurrentHP = MaxHP` 초기화.** 안 넣기로 했다. 레벨에 배치된 플레이어 인스턴스가 0개고 폰은 항상 `PlayerStart`에서 새로 스폰되므로 CDO 기본값 `100`이 곧 시작 체력이다. **다만 리스폰을 "폰을 파괴하지 않고 상태만 되돌리는" 방식으로 바꾸면 그때는 리셋 지점에서 명시적으로 초기화해야 한다**
- **Mixamo 등 외부 베기 애니메이션.** IK Rig도 IK Retargeter도 없고 MCP 툴셋에 리타깃 도구가 없다. 한 세션짜리 수작업
- **진짜 칼 메시 구하기.** 구하면 `BladeHalfLength`와 중심 오프셋을 손잡이 위로 옮겨 "칼날만" 판정이 된다
- **`Knife`와 `Key_Stage1`이 같은 `Cube` 메시라 색이 같은 것.** 머티리얼로 가를 수 있다
- **`heldTransform`의 회전·오프셋이 짝이라는 사실을 `DT_Items` 어디에도 안 적어뒀다.** 주석 칸이 없다
- **적 공격 이펙트·사운드.** 판정만 있다
- **`MM_Attack_02` / `MM_Attack_03` / `MM_ChargedAttack`.** 사용자가 "셋 다 칼이랑 관련없음"으로 확인했다
