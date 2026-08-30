# 2026-08-30

## 작업물

문(`BP_Door`)을 `Lvl_ThirdPerson`에 처음으로 배치해 실행하고, 그 과정에서 드러난 `TryConsumeSelected`의 pure 노드 재계산 버그를 고쳤다 — 명령 39~41, 커밋 3개. 문 사양의 합격 기준 넷이 전부 통과했다.

**소요 시간**: 약 35분(명령 구간). 근거는 Terminal-Log 파일의 mtime이다 — 명령 39의 보고가 `20:36`, 명령 41의 보고가 `21:11`. 그 앞의 인계 확인·조사·심문과 그 뒤의 PIE 검증·손 저장·커밋(`21:24`~`21:25`)은 이 구간 밖이다.

## 명령

### 한글

```
작업준비
```

```
명령 39가자
```

**심문의 답 셋.** 아래는 타이핑한 문장이 아니라 AI가 제시한 항목별 안에서 사용자가 고른 것이다. 셋 다 AI가 권장으로 표시한 안을 골랐다.

- 문짝 크기 → **`BP_Door` 기본값에** (레벨 인스턴스에만 넣는 안, 그 외 중 택1)
- 경첩 반전 테스트 → **두 단계 편집을 받아들인다** (문을 두 개 놓고 비교 / 체크박스만 뒤집고 본다 중 택1)
- 열쇠 픽업 → **그대로 둔다** (문 앞으로 옮긴다 / 하나 더 놓는다 중 택1)

```
결과확인
```

```
결과 확인
```

```
세이브했어확인좀
```

```
열쇠를 들고 문을 F 했을때 열쇠는 사라지는걸 확인했는데 DOOR IS LOCKED 가 뜨고 문이 안열림 계속 눌러도 DOOR IS LOCKED 가 뜸 이거 확인좀
```

```
물약들고 F눌러도 물약안사라져 DOOR IS LOCKED는 뜨고
```

```
결과 확인좀
```

```
PIE 결과 이상 없음 다 잘됨
```

```
빈칸 이상없고 경첩 반전시에 문이 옆 벽에 박힘 아마 문 전체가 돌아가는듯? 그래서 내가 수동으로 원래 자리로 옮기면 잘됨 인벤토리도 FULL잘뜸
```

```
갱신하고 커밋하고 할거 다하고 다음작업하자
```

### English — MCP에 실제로 보낸 명령

**옮기며 AI가 넣은 해석.** 한글 지시는 "명령 39가자" 한 줄이었다. 그 한 줄이 아래 세 개의 영어 명령이 됐고, 그 사이의 모든 숫자·이름·판정 조건은 AI가 정했다.

- **명령 39를 새로 만들었다.** 사양의 계획 표에는 39가 "레벨에 테스트 배치" 하나뿐이었다. `SM_Door`가 2m 정육면체라는 것을 조사에서 발견해 "BP 기본 스케일"을 39로 앞에 끼우고 배치를 40으로 밀었다. 41은 계획에 없던 버그 수정이다
- **좌표 전부** — 벽 위치 `X=1200`, 벽 두께 50 · 높이 220 · 길이 각 400, 문틀 폭 100, 문 액터 `(1225, -50, 110)`. 사용자는 "레벨에 배치하자"만 말했다
- **문짝 크기 `(0.05, 0.5, 1.1)`** = 10 × 100 × 220 cm. 근거는 관례적 문짝 두께, 캐릭터 캡슐 지름 68보다 넉넉한 폭, 벽 높이와 맞춘 높이
- **벽 메시로 `SM_Cube`**, 아웃라이너 폴더 이름 `DoorTest`, 액터 이름 `Wall_L` · `Wall_R` · `Door_Test`
- **로컬 변수 이름 `bMatched`**, 노드 위치 `(300, 560)`과 대체 위치 `(300, 760)`
- **모든 STOP 조건과 보고 항목**

#### 명령 39

```
In /Game/Interaction/BP_Door, set the DoorMesh component's default RelativeScale3D
so the door leaf is 10 x 100 x 220 cm instead of the 200 cm cube it is now.
This is a Blueprint default change, not a level change. Do NOT call AssetTools.is_dirty.

WHY these numbers: SM_Door is a plain cube with local bounds
(-100,-100,-100)..(100,100,100). At scale (1,1,1) BP_Door renders a 2 m cube.
The target leaf is thickness 10 cm on X, width 100 cm on Y, height 220 cm on Z,
so the scale is (0.05, 0.5, 1.1). The Y component matters twice: the
ConstructionScript computes the hinge offset as 100 * DoorMesh.RelativeScale3D.Y,
so ScaleY 0.5 must produce an offset of exactly 50.

PRE-FLIGHT. Report every result. STOP if any fails:
 P1. ActorTools.get_components on /Game/Interaction/BP_Door.Default__BP_Door_C
     returns exactly three components, in this order:
       DefaultSceneRoot_GEN_VARIABLE
       Hinge_GEN_VARIABLE
       DoorMesh_GEN_VARIABLE
 P2. ObjectTools.get_properties on
     /Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE for
     ["RelativeLocation","RelativeRotation","RelativeScale3D","StaticMesh"]
     returns location (0,0,0), rotation (0,0,0), scale (1,1,1), and StaticMesh
     /Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door.SM_Door
 P3. StaticMeshTools.get_bounds on SM_Door returns min about (-100,-100,-100)
     and max about (100,100,100). Report the exact numbers.
 P4. BlueprintTools.list_functions on BP_Door returns ["UserConstructionScript"]
     and read_graph_dsl of that graph still reads:
       (fn ConstructionScript ()
         (Transformation|SetRelativeLocation (Variables|Default|GetDoorMesh)
           (Math|Vector|MakeVector 0.0
             (* (* 100.0 (.y (Class|SceneComponent|GetRelativeScale3D
                              (Variables|Default|GetDoorMesh))))
                (select (|GetbHingeOnRight) -1.0 1.0)))))
     Report the DSL you actually get. STOP if the 100.0 literal or the
     GetRelativeScale3D .y read is not there - the offset would then not follow
     the scale and this change would break the hinge.
 P5. SceneTools.find_actors in the currently loaded level, filtered to the
     BP_Door_C class, returns an EMPTY list. Report the current level path too.
     STOP if any BP_Door instance already exists - a placed instance would keep
     its own overridden component scale and would not follow this default.

ACTION - one call:
   ObjectTools.set_properties on
   /Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE
   with {"RelativeScale3D":{"x":0.05,"y":0.5,"z":1.1}}
   Report the boolean it returns.

   Do NOT touch RelativeLocation, RelativeRotation or StaticMesh on DoorMesh.
   Do NOT touch the Hinge or DefaultSceneRoot components.
   Do NOT touch any variable (bLocked, RequiredKey, bHingeOnRight, OpenAngle,
   SwingSpeed, bOpen) - their defaults stay as they are.

VERIFY, in this order:
   1. Read RelativeScale3D back BEFORE compiling. Report it.
   2. Compile BP_Door. Report the result.
   3. Read RelativeScale3D back AFTER compiling. Report it.
   4. Save BP_Door.
   5. Read RelativeScale3D back AFTER saving. Report it.
   If any of the three read-backs is not (0.05, 0.5, 1.1), say so plainly and
   report what it actually holds. Do not retry silently - report every attempt.

Write the report to Docs/Terminal-Log/2026-08-30-39-door-mesh-scale.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight result, including the exact SM_Door bounds numbers and the
  exact ConstructionScript DSL as read
- the current level path and the BP_Door instance count found in it
- the boolean returned by set_properties
- all three read-backs of RelativeScale3D (before compile, after compile,
  after save), verbatim
- the compile result
- a re-read of ActorTools.get_components confirming there are still exactly
  three components with the same names
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

#### 명령 40

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, place the door
test: two wall boxes and one BP_Door. This is a LEVEL change only - do NOT edit
any Blueprint. Do NOT call AssetTools.is_dirty.

GEOMETRY (world space, every rotation zero, Z=0 is the plaza floor):
  Wall_L    SM_Cube   location (1200, -450, 0)   scale (0.5, 4.0, 2.2)
            -> X 1200..1250,  Y -450..-50,  Z 0..220
  Wall_R    SM_Cube   location (1200,   50, 0)   scale (0.5, 4.0, 2.2)
            -> X 1200..1250,  Y   50..450,  Z 0..220
  doorway   the 100 cm gap between them, Y -50..+50
  Door_Test BP_Door   location (1225, -50, 110)  scale (1, 1, 1)
            -> hinge axis on the Y=-50 jamb, leaf fills Y -50..+50,
               X 1220..1230, Z 0..220

  SM_Cube's pivot is at its MIN corner (local bounds (0,0,0)..(100,100,100)),
  so the location IS the min corner and scale*100 is the size. Do not offset it.
  BP_Door's DoorMesh pivot is at the mesh CENTRE, which is why the door actor
  sits at Z=110 rather than Z=0.

PRE-FLIGHT. Report every result. STOP if any fails:
 P1. SceneTools.get_current_level returns /Game/ThirdPerson/Lvl_ThirdPerson.
 P2. find_actors with actor_type /Game/Interaction/BP_Door.BP_Door_C returns [].
 P3. find_actors with bounds min (1150,-550,-20) max (1350,550,400), empty name,
     empty tag, empty collision_channels. Report EVERY refPath returned. It must
     contain only the SkySphere StaticMeshActor and Floor. If anything else is in
     that box, STOP - the site is not clear.
 P4. StaticMeshTools.get_bounds on /Game/LevelPrototyping/Meshes/SM_Cube.
     Report the exact numbers. Expect min (0,0,0) max (100,100,100). STOP if the
     min is not the origin - the entire placement arithmetic assumes a corner pivot.
 P5. ObjectTools.get_properties on
     /Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE for
     ["RelativeScale3D"]. Expect about (0.05, 0.5, 1.1). STOP if it reads
     (1,1,1) - command 39 would not have stuck.
 P6. SceneTools.get_folders. Report the list. STOP if a folder DoorTest exists.

PLACE, one actor at a time, reporting the returned refPath after each:
 1. SceneTools.add_to_scene_from_asset
      asset_path "/Game/LevelPrototyping/Meshes/SM_Cube"
      name "Wall_L"
      xform: location (1200,-450,0), rotation (0,0,0), scale (0.5,4.0,2.2)
      parent unset, snap_to_ground FALSE
 2. the same, name "Wall_R", location (1200,50,0), same rotation and scale
 3. SceneTools.add_to_scene_from_asset
      asset_path "/Game/Interaction/BP_Door"
      name "Door_Test"
      xform: location (1225,-50,110), rotation (0,0,0), scale (1,1,1)
      parent unset, snap_to_ground FALSE

 If any call returns null or nothing, STOP and say which actor failed. Do not
 retry blind.

 Then ActorTools.set_label on each to exactly Wall_L / Wall_R / Door_Test, and
 SceneTools.set_actor_folder on each with folder_path "DoorTest".

VERIFY. This is the part that matters - the ConstructionScript has never been
observed running. Report expected beside measured, with PASS/FAIL on each:
 V1. get_actor_transform on all three. Verbatim.
 V2. get_actor_bounds Wall_L    -> about min (1200,-450,0) max (1250,-50,220)
 V3. get_actor_bounds Wall_R    -> about min (1200,50,0)   max (1250,450,220)
 V4. get_components on Door_Test. Report every refPath. Then
     ObjectTools.get_properties on its DoorMesh component for
     ["RelativeLocation","RelativeScale3D"].
     RelativeLocation MUST read about (0, 50, 0). That is the ConstructionScript's
     100 * ScaleY offset and this is the FIRST time it has ever been observed.
     If it reads (0,0,0) the ConstructionScript did not run - report that plainly
     and do NOT try to fix it.
 V5. get_actor_bounds Door_Test -> about min (1220,-50,0) max (1230,50,220)
 V6. ObjectTools.get_properties on the Door_Test ACTOR for
     ["bLocked","bOpen","bHingeOnRight","OpenAngle","SwingSpeed","RequiredKey"].
     Expect bLocked true, bOpen false, bHingeOnRight false, OpenAngle 90,
     SwingSpeed 1, RequiredKey DT_Items / Key_Stage1. Report what it actually
     holds. Do NOT change any of them.
 V7. SceneTools.trace_world from (1225, 0, 1000) to (1225, 0, -100). Report the
     distance. About 780 means it hit the top of the leaf at Z=220. About 1000
     means it went through and hit the floor, i.e. the leaf has no collision
     there - report which one happened.

SAVE. This level is World Partition - it has WorldDataLayers and
WorldPartitionMiniMap actors and Content/__ExternalActors__/Lvl_ThirdPerson
exists - so new actors live in their own external actor packages:
  SceneTools.save_actor on Wall_L, Wall_R and Door_Test, one call each.
  Then AssetTools.save_assets on ["/Game/ThirdPerson/Lvl_ThirdPerson"].
  Report every return value.

Do NOT touch any existing actor. In particular do NOT move BP_ItemPickup2 (the
Key_Stage1 pickup at (840,1130,0)), any other BP_ItemPickup, SM_Ramp11, or the
PlayerStart.

Write the report to Docs/Terminal-Log/2026-08-30-40-door-test-placement.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight result, including the full refPath list from P3 and the exact
  SM_Cube bounds numbers from P4
- the refPath returned for each of the three placed actors
- V1 through V7 verbatim, expected beside measured, PASS/FAIL each
- the placed instance's DoorMesh RelativeLocation called out on its own - it is
  the first observation of the ConstructionScript running
- the return value of every save call
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

#### 명령 41

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, graph TryConsumeSelected,
fix a confirmed runtime bug. Do NOT call AssetTools.is_dirty.
Do NOT touch TryAddItem, do NOT touch EventGraph, do NOT touch BP_Door.

THE BUG, confirmed in PIE on 2026-08-30:
  ANDBoolean is a PURE node and its output feeds BOTH Branch.Condition AND
  Return.Success. Pure nodes are re-evaluated at every read. The Branch reads it
  (true, the selected slot holds the key), SetArrayElem then blanks that slot, and
  the Return reads the SAME pure chain again - now the slot is empty, Equal(Name)
  is false, and the function returns FALSE after having consumed the item.
  Observed: the key vanished, BP_Door still showed DOOR IS LOCKED, bLocked stayed
  true. Control test: with a non-matching item selected, nothing was consumed and
  the message still showed - so the consume path only runs when the Branch is true,
  which is what proves the two reads disagree.

THE FIX: latch the AND's value into a LOCAL bool with an impure Set node, and feed
both the Branch and the Return from that latch instead of from the pure chain.
One new node, one new local variable, nothing deleted.

PRE-FLIGHT. Report every result. STOP if any fails:
 P1. find_nodes on
     /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:TryConsumeSelected
     with empty title returns exactly 13 nodes. Report every refPath AND every
     node's position - the positions decide where the new node goes.
 P2. get_node_infos on K2Node_CommutativeAssociativeBinaryOperator_0. Its
     type_id must be Math|Boolean|ANDBoolean and its output pin [0] "ReturnValue"
     must list EXACTLY two destinations:
       K2Node_IfThenElse_0     [in 1]  "Condition"
       K2Node_FunctionResult_0 [in 1]  "Success"
 P3. get_node_infos on K2Node_IfThenElse_0. Its input [0] "execute" must come
     from K2Node_FunctionEntry_0 [out 0] "then", its output [0] "then" must go to
     K2Node_CallArrayFunction_0, its output [1] "else" must go to
     K2Node_FunctionResult_0 [in 0].
 P4. list_variables on BP_ThirdPersonCharacter. Report it. It must NOT contain
     bMatched. Report the count.
 P5. find_nodes on BP_ThirdPersonCharacter:TryAddItem returns 12 nodes, and on
     BP_ThirdPersonCharacter:EventGraph returns 87. Report both numbers. These are
     the untouched baselines to re-check at the end.

STAGE 1 - the local variable.
   add_variable
     blueprint  BP_ThirdPersonCharacter
     name       bMatched
     type_name  bool
     graph      the TryConsumeSelected graph      <- THIS MAKES IT LOCAL
   Then verify it is LOCAL, not a member:
     list_variables on BP_ThirdPersonCharacter must STILL not contain bMatched and
     must still have the same count as P4. Report it.
   If bMatched shows up in list_variables it was created as a member variable -
   STOP, report that, remove it with remove_variable, and change nothing else.

STAGE 2 - the Set node, as an island. Nothing is rewired yet.
   Place it at (300, 560). First report any node from P1 whose position is within
   250 units of that point; if any is, use (300, 760) instead and say so.
   Discover the type_id: call find_node_types on the TryConsumeSelected graph with
   empty context_pins and report every entry whose name contains "bMatched".
   Create the node with the exact type_id that returned. If none returned, try
   create_node with type_id "|SetbMatched" and report that you fell back to it.
   If neither produces a node, STOP - do not improvise a member variable.

   Read the new node back with get_node_infos and report its FULL pin list.
   State explicitly whether it has an output pin named "Output_Get".
     - If it HAS Output_Get, that pin is "the latch output" below.
     - If it does NOT, create one more node - a getter for bMatched, discovered the
       same way (find_node_types, else type_id "|GetbMatched") - at (300, 900), and
       ITS output pin is "the latch output" below. Say clearly which case happened.

STAGE 3 - rewire, in exactly this order, reporting after each call:
   1. connect  ANDBoolean [out 0 "ReturnValue"] -> Set bMatched [in "bMatched"]
   2. break    FunctionEntry [out 0 "then"] -> Branch [in 0 "execute"]
   3. connect  FunctionEntry [out 0 "then"] -> Set bMatched [in "execute"]
   4. connect  Set bMatched [out "then"] -> Branch [in 0 "execute"]
   5. break    ANDBoolean [out 0] -> Branch [in 1 "Condition"]
   6. connect  the latch output -> Branch [in 1 "Condition"]
   7. break    ANDBoolean [out 0] -> Return [in 1 "Success"]
   8. connect  the latch output -> Return [in 1 "Success"]

   Resolve every pin by NAME to its index from a get_node_infos read, not by
   assuming an index.

STAGE 4 - verify. Report expected beside measured with PASS/FAIL on each:
 V1. ANDBoolean output [0] destination list is EXACTLY one entry: the Set node's
     "bMatched" input. Not the Branch, not the Return.
 V2. Branch [in 1 "Condition"] source list is EXACTLY one entry: the latch output.
 V3. Return [in 1 "Success"] source list is EXACTLY one entry: the latch output.
 V4. Branch [in 0 "execute"] source is the Set node's "then", and the Set node's
     "execute" source is FunctionEntry "then".
 V5. Branch [out 0 "then"] still goes to K2Node_CallArrayFunction_0 and
     [out 1 "else"] still goes to K2Node_FunctionResult_0 [in 0]. Unchanged.
 V6. K2Node_CallArrayFunction_0 (SetArrayElem) pins are unchanged: TargetArray from
     K2Node_VariableGet_2, Index from K2Node_PromotableOperator_0, Item unconnected
     with an empty value, bSizeToFit false, then -> K2Node_CallFunction_0.
 V7. K2Node_PromotableOperator_0 (int-int) output still feeds BOTH
     K2Node_GetArrayItem_0 [in 1] and K2Node_CallArrayFunction_0 [in 2].
 V8. find_nodes on TryConsumeSelected: 14 nodes (15 if the extra getter was needed).
     find_nodes on TryAddItem: still 12. find_nodes on EventGraph: still 87.

STAGE 5 - compile BP_ThirdPersonCharacter and report the result, then save it.
   Report the save return value.

Write the report to Docs/Terminal-Log/2026-08-30-41-consume-latch-fix.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight result, including all 13 node positions from P1 and both
  baseline counts from P5
- whether add_variable produced a LOCAL variable, and the list_variables read-back
  that proves it
- which type_id created the Set node, and whether the Output_Get pin existed or a
  getter node had to be added
- the full pin list of the Set node (and the getter, if created)
- V1 through V8 verbatim, expected beside measured, PASS/FAIL each
- the compile result and the save return value
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

## Terminal 결과

### 원문 — English

**발췌했다.** 세 보고서는 합쳐 약 46,000자다. 아래는 판단 근거가 된 줄만 뽑았다. 다만 **실패와 어긋난 응답은 발췌하지 않고 전문을 붙였다.**

#### 명령 39 — 세 번의 read-back

```json
{"RelativeScale3D":{"x":0.050000000000000003,"y":0.5,"z":1.1000000000000001}}
```

세 번(컴파일 전 · 컴파일 후 · 저장 후) 모두 같은 값이었다. 보고서의 해설:

```
The printed decimals 0.050000000000000003 and 1.1000000000000001 are the
double-precision representations of 0.05 and 1.1 - neither 0.05 nor 1.1 is exactly
representable in binary floating point, so this is the expected round-trip of the
values that were sent, not a drift or a rounding introduced by the editor. y came
back as exactly 0.5, which is exactly representable.
```

`SM_Door`의 바운드:

```json
{"returnValue":{"min":{"x":-100.00001525878906,"y":-100.00001525878906,"z":-100},"max":{"x":100.00001525878906,"y":100.00001525878906,"z":100},"isValid":true}}
```

`compile_blueprint`에 대해 보고서가 스스로 적은 것:

```
The tool declares no output schema, so null is what a completed call returns here - it
is not a status value and carries no pass/fail information. This matches the standing
project observation that a unreal-mcp return value is not evidence.
```

#### 명령 40 — 저장 실패, 전문

세 번 다 실패했다. 보고서에 실린 원문 그대로:

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/EB/M2R2969V25QR9HAZAO0DTH
Failed to save 'Wall_L'.
```

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/8Q/388B6MQM912EX2BXH5U4GD
Failed to save 'Wall_R'.
```

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/5/D1/KK3E4BC1U33OGW1QTQUUOL
Failed to save 'Door_Test'.
```

이어서 `AssetTools.save_assets`가:

```json
{"returnValue":true}
```

보고서가 그 `true`를 디스크와 대조한 결과, 역시 전문:

```
ls: cannot access 'Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/EB/': No such file or directory
ls: cannot access 'Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/8Q/': No such file or directory
ls: cannot access 'Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/5/D1/': No such file or directory
```

```
So save_assets returned true while writing nothing for these actors. This is a fresh
instance of the standing project observation that a unreal-mcp return value is not
evidence, and a sharper one than usual: the failure is not a null-where-true-was-expected,
it is a true where the work did not happen.
```

#### 명령 40 — ConstructionScript의 첫 관측

```json
{"RelativeLocation":{"x":0,"y":50,"z":0},"RelativeScale3D":{"x":0.050000000000000003,"y":0.5,"z":1.1000000000000001}}
```

#### 명령 40 — `V5`의 어긋난 값, 전문

```json
{"returnValue":{"min":{"x":1097,"y":-178,"z":-18},"max":{"x":1353,"y":78,"z":238},"isValid":true}}
```

```
V5 FAIL as stated. The measured box is far larger than the door leaf in every axis.
What the numbers are: the box is 256 x 256 x 256 and it is centred exactly on the actor
location (1225, -50, 110), with a 128 cm half-extent on each axis. A perfect cube centred
on the actor pivot is not any door-leaf shape; a 10 x 100 x 220 leaf could not produce it.
The likely cause is the extra BillboardComponent_6 found in V4 [...] That is a hypothesis -
it was not tested, because testing it would mean touching the actor, and no component-level
bounds tool exists in this toolset.
```

`Door_Test`의 컴포넌트가 CDO보다 하나 많다:

```
....DefaultSceneRoot
....BillboardComponent_6
....Hinge
....DoorMesh
```

`V7`의 트레이스:

```json
{"returnValue":780}
```

#### 명령 41 — `bMatched`가 팔레트에 안 뜬 것

```json
{"returnValue":[]}
```

필터를 `"Matched"`로 넓히자:

```json
["Class|MovieSceneSkeletalAnimationSection|GetMatchedLocationOffset","Class|MovieSceneSkeletalAnimationSection|GetMatchedRotationOffset","Class|PCGMatchandSetAttributesSettings|GetKeepUnmatched","Class|PCGMatchandSetAttributesSettings|SetKeepUnmatched","Variables|Default|GetMatched","Variables|Default|SetMatched"]
```

```
The name has no b because Unreal strips the b prefix from a bool variable's display name -
the variable itself is still bMatched.
```

만든 노드가 되읽히는 이름:

```
Variables|Default|SetMatched is the creation spelling, |SetbMatched is the stored
spelling, and they are one node type.
```

#### 명령 41 — 로컬임을 증명한 두 읽기

```json
{"returnValue":["bIsFirstPerson","FirstPersonPitchMin","FirstPersonPitchMax","ThirdPersonPitchMin","ThirdPersonPitchMax","InventorySlots","SelectedSlot","CurrentHP","MaxHP","InteractDistance","FoundSlotIndex"]}
```

```json
{"returnValue":["bMatched"]}
```

#### 명령 41 — 수정의 핵심 세 읽기

```json
{"value":"false","connected_pins":[{"direction":"EGPD_Input","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_VariableSet_0"}}],"pin_id":{"direction":"EGPD_Output","index_id":0,"node":{"refPath":"…:TryConsumeSelected.K2Node_CommutativeAssociativeBinaryOperator_0"}},"type_id":"Boolean","name":"ReturnValue"}
```

```json
{"value":"true","connected_pins":[{"direction":"EGPD_Output","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_VariableSet_0"}}],"pin_id":{"direction":"EGPD_Input","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_IfThenElse_0"}},"type_id":"Boolean","name":"Condition"}
```

```json
{"value":"false","connected_pins":[{"direction":"EGPD_Output","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_VariableSet_0"}}],"pin_id":{"direction":"EGPD_Input","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_FunctionResult_0"}},"type_id":"Boolean","name":"Success"}
```

#### 명령 41 — 저장이 이번엔 진짜였다

```
This true was checked against the disk, because command 40 produced a true from this
same tool while writing nothing. Here it is truthful:

 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
-rw-r--r-- 1 a0108 197609 592040 2026-08-30_21:09:54 Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

#### 명령 39·40·41 공통 — 잡지 못한 것

세 보고서가 모두 같은 문장을 적었다.

```
The editor's own Message Log and Output Log were not read as part of this command, so a
compile warning that appeared only there would not have been captured here.
```

### 요약 — 한글

**명령 39** — `BP_Door`의 `DoorMesh` 컴포넌트 기본 `RelativeScale3D`가 `(1,1,1)` → `(0.05, 0.5, 1.1)`. 애셋 하나(`BP_Door.uasset`)만 바뀌었다. `Hinge` · `DefaultSceneRoot` · 변수 6개(`bLocked` · `RequiredKey` · `bHingeOnRight` · `OpenAngle` · `SwingSpeed` · `bOpen`)는 안 건드렸다. 사전 검사 다섯 통과 — 그중 `P4`가 `UserConstructionScript`의 DSL에서 `100.0` 리터럴과 `GetRelativeScale3D`의 `.y` 읽기가 살아 있는지 확인하는 것이었고, `P5`가 레벨에 `BP_Door` 인스턴스가 하나도 없음을 확인하는 것이었다.

**명령 40** — 레벨 액터 3개 신규. `Wall_L`(`SM_Cube`, `(1200,-450,0)`, 스케일 `(0.5,4.0,2.2)`), `Wall_R`(`SM_Cube`, `(1200,50,0)`, 같은 스케일), `Door_Test`(`BP_Door`, `(1225,-50,110)`). 셋 다 아웃라이너 폴더 `DoorTest`. `ConstructionScript`가 처음으로 실행돼 인스턴스의 `DoorMesh.RelativeLocation`이 `(0, 50, 0)`이 됐다. **저장은 MCP로 안 됐다** — `save_actor` 세 번 모두 `Asset does not exist`, `save_assets`는 `true`를 주고 아무것도 안 씀. 사용자가 에디터에서 `Ctrl+S`로 저장해 외부 액터 패키지 3개와 `__ExternalObjects__` 1개가 디스크에 생겼다.

**명령 41** — `BP_ThirdPersonCharacter`의 `TryConsumeSelected`에 로컬 변수 `bMatched`(bool) 하나와 `K2Node_VariableSet_0`(`|SetbMatched`) 노드 하나 추가. 노드 13 → 14, 삭제 0. `ANDBoolean`의 출력이 `Branch.Condition`·`Return.Success` 두 곳을 먹이던 것을 끊고, 그 자리에 `Set.Output_Get`을 넣었다. `TryAddItem`(12) · `EventGraph`(87)는 개수까지 그대로.

## 분석

### 무엇을 만들었나

**애셋 변경 — `Content/Interaction/BP_Door.uasset`** (명령 39, 커밋 `bb3b783`)

| 대상 | 이전 | 이후 |
|---|---|---|
| `DoorMesh.RelativeScale3D` | `(1, 1, 1)` | `(0.05, 0.5, 1.1)` |

실제 문짝 치수는 `SM_Door`의 200 큐브에 곱한 값이라 **10 × 100 × 220 cm**. 파일 크기가 135818 → 135014바이트로 **804바이트 줄었다.**

**레벨 액터 — `Lvl_ThirdPerson`** (명령 40, 커밋 `47fc60f`)

| 액터 | 클래스/메시 | 위치 | 회전 | 스케일 | 결과 월드 바운드 |
|---|---|---|---|---|---|
| `Wall_L` | `SM_Cube` | `(1200, -450, 0)` | `(0,0,0)` | `(0.5, 4.0, 2.2)` | `min (1200,-450,0)` `max (1250,-50,220.00000000000003)` |
| `Wall_R` | `SM_Cube` | `(1200, 50, 0)` | `(0,0,0)` | `(0.5, 4.0, 2.2)` | `min (1200,50,0)` `max (1250,450,220.00000000000003)` |
| `Door_Test` | `BP_Door` | `(1225, -50, 110)` | `(0,0,0)` | `(1,1,1)` | 문짝 X 1220~1230 · Y -50~+50 · Z 0~220 |

문틀은 두 벽 사이의 **Y −50 ~ +50, 폭 100cm**. 셋 다 아웃라이너 폴더 `DoorTest`.

`Door_Test`의 인스턴스 변수는 전부 CDO 기본값 그대로다 — `bLocked true` · `bOpen false` · `bHingeOnRight false` · `OpenAngle 90` · `SwingSpeed 1` · `RequiredKey = DT_Items / Key_Stage1`. **인스턴스 오버라이드가 하나도 없다.**

디스크에 생긴 파일 4개:

```
Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/EB/M2R2969V25QR9HAZAO0DTH.uasset   Wall_L
Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/8Q/388B6MQM912EX2BXH5U4GD.uasset   Wall_R
Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/5/D1/KK3E4BC1U33OGW1QTQUUOL.uasset   Door_Test
Content/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/E/2R/I7YTTKZX32ZUPSIFKIB1NS.uasset  정체 미확인
```

`Lvl_ThirdPerson.umap` 자체는 수정되지 않았다. World Partition이라 액터가 전부 외부 패키지에 있기 때문이다.

**함수 수정 — `BP_ThirdPersonCharacter:TryConsumeSelected`** (명령 41, 커밋 `c090dde`)

추가된 것은 로컬 변수 `bMatched`(bool)와 노드 `K2Node_VariableSet_0`(`|SetbMatched`, 위치 `(300, 760)`) 하나뿐이다. `bMatched`는 **로컬**이라 `list_variables(blueprint)`에는 안 나오고 `list_variables(blueprint, graph)`에만 나온다.

배선 변경 — 끊은 것 3, 이은 것 5.

```
끊음  FunctionEntry.then      -> Branch.execute
끊음  ANDBoolean.ReturnValue  -> Branch.Condition
끊음  ANDBoolean.ReturnValue  -> Return.Success

이음  ANDBoolean.ReturnValue  -> Set.bMatched
이음  FunctionEntry.then      -> Set.execute
이음  Set.then                -> Branch.execute
이음  Set.Output_Get          -> Branch.Condition
이음  Set.Output_Get          -> Return.Success
```

결과 구조:

```
TryConsumeSelected(RowName) -> Success

  entry -> Set bMatched  (값 <- (Slot[SelectedSlot-1] == RowName) AND (RowName != None))
        -> Branch (Set.Output_Get)
             true  -> SetArrayElem(Slot[SelectedSlot-1] = 빈 Name) -> RefreshHeldItem -> Return
             false ->                                                                   Return
  Return.Success <- Set.Output_Get
```

### 기술적으로 맞게 짚은 부분

**`SM_Door`가 문짝이 아니라는 것을 명령을 쓰기 전에 잡았다.** 사양이 "`SM_Door`의 피벗이 정중앙이다. 바운드가 `min (-100,-100,-100)` `max (100,100,100)`"이라고 적어놓고도 **그게 세 축 모두 200이라는 뜻**임을 읽지 않았다. 문짝이면 한 축이 얇아야 한다. `CaptureAssetImage`로 썸네일을 뽑아 정육면체인 것을 눈으로 확인한 뒤에야 명령 39가 생겼다. 이걸 안 잡았으면 2m 큐브를 배치하고 "왜 문처럼 안 보이지"부터 시작했을 것이다.

**`SM_Cube`의 피벗을 추측하지 않고 역검증했다.** `get_bounds`가 `min (0,0,0)`을 주는 것만으로는 코너 피벗이라고 단정하기 이르다. 레벨의 `SM_Cube14`(위치 `(200,210,0)`, yaw 90, 스케일 `(3,4,2)`)를 골라 코너 피벗을 가정하고 월드 바운드를 손으로 계산했고, 측정값 `min (-200,210,0) max (200,510,200)`과 정확히 일치했다. 배치 산술 전체가 이 가정 위에 서 있었으므로 이 검증이 없었으면 벽이 절반씩 어긋났을 것이다.

**지형을 `trace_world`로 찍었다.** 스크린샷으로는 램프가 어디서 어디까지인지 안 보였다. 세 점(`X=400` → Z 200, `X=700` → Z 100, `X=1000` → Z 0)을 찍어 램프 구간을 특정하고, 그 밖의 평지에 벽을 놓았다. 그림을 오래 들여다보는 대신 세 번 찍은 것이 빨랐고 정확했다.

**`P5`가 배치 전에 인스턴스 유무를 확인하게 한 것.** CLAUDE.md가 "부모 BP 기본값을 바꾸면 그 값을 이미 덮어쓴 자식·레벨 인스턴스는 따라오지 않는다"고 못 박았다. 명령 39는 BP 기본값을 바꾸는 명령이었으므로 인스턴스가 0개임을 먼저 확인해야 했다. 실제로 0개였고, 그래서 명령 40에서 배치한 인스턴스가 새 스케일을 그대로 받았다.

**저장 실패 앞에서 재시도하지 않았다.** `save_actor`가 세 번 실패했을 때 터미널이 다른 도구를 시도하거나 같은 호출을 반복하지 않고 멈춰서 원문을 남겼다. 그 원문(`Asset does not exist: /Game/__ExternalActors__/.../C/EB/M2R...`)이 원인을 그대로 말해줬다 — 없는 패키지를 저장하려 한 것. 그 문장이 없었으면 "MCP 저장이 안 된다"까지만 알고 왜인지는 몰랐을 것이다.

**엔진 소스에서 저장 경로를 확인하고 손 작업으로 넘겼다.** 추측으로 `Ctrl+S`를 시키지 않았다. `LevelEditorActions.cpp:4367`이 `Save Current Level`을 `Ctrl+S`에 매고, `:568`이 `FEditorFileUtils::SaveCurrentLevel()`을 부르고, `FileHelpers.cpp:4444-4453`이 `Level->GetLoadedExternalObjectPackages()`를 돌면서 `IsDirty()` **또는 `PKG_NewlyCreated`**인 패키지를 저장 목록에 넣는다. 새 액터의 패키지가 정확히 `PKG_NewlyCreated`고, 이것이 `save_actor`가 못 하는 일이다. **`save_actor`와 `SaveCurrentLevel`의 차이가 소스 한 줄에 있었다.**

**`get_actor_bounds`가 문짝을 못 잰다는 것을 우회했다.** `V5`가 256cm 정육면체를 뱉었을 때 터미널이 "PASS로 봐줄 수 없다"고 적고, 대신 `V7`의 `trace_world`가 문짝을 실제로 짚었다는 것을 논증했다 — `(1225, 0)`은 문틀 틈 안이라 벽일 수 없고 `X=1225`는 문짝 X 범위 안이므로 거기 있을 수 있는 것은 문짝뿐이다. **실패한 검사를 성공으로 뭉개지 않고 다른 검사로 대체하면서 그 사실을 밝혔다.**

**버그를 고치기 전에 반증 테스트를 했다.** 가설(pure 노드 재계산)을 세운 뒤 "이 가설이 틀렸다면 무엇이 보일지"를 먼저 말했다 — 물약(안 맞는 아이템)을 들고 `F`를 눌렀을 때 물약도 사라지면 가설이 틀린 것이다. 사용자가 PIE에서 확인했고 물약은 남았다. **편집을 하나도 안 하고 PIE 한 번으로 가설이 갈렸다.**

**"열쇠는 사라졌는데 실패했다"가 증거 자체였다.** 사라졌다는 것은 함수 안의 `Branch`가 `true`였다는 뜻이고, 실패했다는 것은 `Return`이 `false`였다는 뜻이다. 배선상 둘은 같은 `ANDBoolean` 출력을 읽는다. 같은 노드에서 두 값이 갈리는 경로는 재계산 하나뿐이다. 로그를 더 뽑을 필요가 없었다.

**`TryAddItem`을 안 고친 것.** 같은 모양(`>=` 하나가 `Branch`와 `Return`을 동시에 먹임)이지만 그 조건이 `FoundSlotIndex`라는 **변수**를 읽고 `SetArrayElem`은 `InventorySlots`를 쓴다. 재계산해도 값이 같다. 손대지 않는 것이 정답이었다. 같은 논리로 `TryConsumeSelected` 안의 `int-int`(`SelectedSlot - 1`)도 두 번 읽히지만 `SelectedSlot`을 이 함수가 안 쓰므로 그대로 뒀다.

**로컬 변수를 골랐다.** 멤버 변수로 만들었으면 캐릭터에 상태가 하나 늘고 2단계 사양의 "`SelectedSlot` 하나가 유일한 상태다"가 깨진다. `add_variable`의 `graph` 인자가 로컬을 만든다는 것을 도구 설명에서 확인하고, 만든 뒤에 **두 번 읽어서** 로컬임을 증명했다 — `list_variables(blueprint)`는 11개 그대로, `list_variables(blueprint, graph)`는 `["bMatched"]`.

### 확인한 것 / 확인 못 한 것

**확인한 것** — PIE 또는 에디터에서 실제로 본 것.

- **합격 기준 1** — 잠긴 문에 열쇠 없이 `F` → 문이 안 열리고 좌상단에 `DOOR IS LOCKED`. **빈 칸 형태와 안 맞는 아이템(물약) 형태 둘 다** 확인했다
- **합격 기준 2** — 열쇠를 든 칸을 선택하고 `F` → 문이 경첩을 축으로 열리고, 그 칸이 비고, 오른손이 빈다
- **합격 기준 3 앞부분** — 열린 문에 `F` → 닫힘, 또 `F` → 열림. 열쇠를 다시 요구하지 않는다
- **합격 기준 4** — 아이템 습득이 그대로 되고, 3칸이 차면 `INVENTORY FULL`이 뜬다
- **경첩 반전 시 문짝이 반대쪽으로 간다** — `bHingeOnRight`를 뒤집으면 문짝이 `Wall_L`(Y −450~−50) 속으로 들어간다. 계산과 일치한다: 오프셋 부호가 `+50` → `−50`이 되어 문짝이 Y −50~−150을 차지한다
- **`MoveComponentTo`를 여는 도중에 다시 부르는 것** — 문이 열리는 중에 `F`를 연타해도 이상 없음. `Stop`·`Return` 핀을 비워둔 것이 문제를 안 냈다. 인계 목록의 "확인 필요" 하나가 해결됐다
- **`TryConsumeSelected`가 소비 후 `true`를 반환한다** — 명령 41 전에는 `false`였다
- **명령 39의 스케일이 실제로 붙었다** — 세 번의 read-back + 명령 40의 `P5` + 배치한 인스턴스의 `DoorMesh.RelativeScale3D`
- **`ConstructionScript`가 실행된다** — 배치한 인스턴스의 `DoorMesh.RelativeLocation`이 정확히 `(0, 50, 0)`
- **레벨이 디스크에 저장됐다** — 외부 액터 파일 71개 → 74개, 에러 메시지가 예고한 세 경로가 그대로 생김
- **`git status`가 건드린 것만 보여준다** — `BP_Door.uasset` · `BP_ThirdPersonCharacter.uasset` · 새 외부 패키지 4개 · Terminal-Log 3개

**확인 못 한 것** — 이유까지.

- **합격 기준 3 뒷부분이 절반만 확인됐다.** `bHingeOnRight`를 뒤집으면 문짝이 반대쪽으로 간다는 것은 확인됐지만(벽에 박힌 것이 그 증거다), **그 상태에서 액터 `Y`를 `+50`으로 옮겨 문틀을 채우고 정상 개폐까지 봤는지는 갈린다.** 사용자의 보고가 "수동으로 원래 자리로 옮기면 잘됨"이었는데, "원래 자리"가 반대쪽 문설주(`Y=+50`)인지 원상복귀(`bHingeOnRight` 되돌림)인지 문장에서 결정되지 않는다. 최종 상태를 읽어보니 `bHingeOnRight = false`, 위치 `(1225,-50,110)`으로 원래대로 돌아와 있다
- **컴파일 경고를 세 명령 모두 못 잡았다.** `compile_blueprint`가 `null`만 주고 에디터의 Message Log와 Output Log를 안 읽었다. 경고가 거기에만 떴다면 지금 아무도 모른다
- **`get_actor_bounds`가 문짝을 못 재는 이유가 가설이다.** `BillboardComponent_6`이 바운드를 지배한다는 설명은 CDO(컴포넌트 3개)와 인스턴스(4개)의 차이에서 나온 추론이고, 시험하지 않았다. 컴포넌트 단위 바운드를 읽는 도구가 이 툴셋에 없다
- **`__ExternalObjects__`에 생긴 파일의 정체.** `DoorTest` 폴더의 `UActorFolder`일 가능성이 높지만(같은 저장에서 생겼고 폴더가 2 → 3, 파일이 3 → 4) `get_asset_class`가 외부 패키지에 `Asset does not exist`를 낸다. 세 액터 패키지도 같은 이유로 못 읽었다. **정황이지 확인이 아니다**
- **문짝을 애셋 단독으로 못 봤다.** `CaptureAssetImage`를 `/Game/Interaction/BP_Door`에 걸었더니 `Asset type does not support image capture` — 블루프린트는 썸네일 캡처 대상이 아니다. 배치한 뒤 PIE에서 본 것이 전부다
- **`Output_Get`의 런타임 값을 직접 안 봤다.** 배선은 읽어서 확인했고 PIE에서 문이 열렸으니 `true`가 흘렀다는 것은 결과로 안다. 그 핀 자체를 찍어본 것은 아니다

### 남는 리스크

- **`Output_Get`은 스냅샷이 아니라 변수를 다시 읽는 핀이다.** 이번에 안전한 이유는 이 함수 안에서 `bMatched`에 쓰는 곳이 그 `Set` 하나뿐이기 때문이다. 나중에 이 함수가 길어져서 `bMatched`를 두 번 쓰게 되면 같은 종류의 문제가 다시 난다. **수정이 근본적인 게 아니라 이 함수의 현재 모양에 맞는 것이다**
- **`TryAddItem`이 우연히 안전하다.** 조건이 `FoundSlotIndex >= 0`이라 배열 쓰기의 영향을 안 받는다. 그 조건이 언젠가 배열을 보게 되면 `TryConsumeSelected`와 똑같이 터진다. 지금은 버그가 아니라서 안 고쳤다
- **`OpenAngle` 기본값 90이면 문이 플레이어 쪽(−X)으로 열린다.** 경첩 yaw +90이 문짝 방향 `(0,1,0)`을 `(-1,0,0)`으로 돌린다. 문 바로 앞에 붙어 서서 누르면 문짝이 몸을 통과한다. 인스턴스에서 `-90`으로 바꾸면 바깥으로 열린다. 이번에는 안 바꿨다
- **경첩 반전이 두 단계 편집을 요구한다.** 체크박스만 뒤집으면 문짝이 문틀 밖으로 나간다. 액터 `Y`도 문설주 폭만큼 옮겨야 한다. 심문에서 승인받은 절충이지만, 문이 여러 개가 되면 매번 두 곳을 고쳐야 한다
- **`Wall_L`·`Wall_R`이 문틀 메시가 아니라 회색 박스다.** 사양이 그렇게 정했고 성 문틀은 맵을 만들 때 온다. 문 위가 뚫려 있다(벽 높이 220 = 문짝 높이 220, 인방이 없다)
- **`__ExternalObjects__` 파일을 정체도 모른 채 커밋했다.** 내용이 깨지지 않았고 `DoorTest` 폴더와 시점이 맞지만, 무엇인지 모르는 바이너리가 저장소에 들어갔다
- **World Partition 레벨에 액터를 놓을 때마다 손 저장이 필요하다.** 인터페이스 구현에 이어 두 번째로 확인된 손 작업 지점이다. 앞으로 배치 명령을 쓸 때마다 이 단계가 붙는다
- **`MoveComponentTo`의 `Stop`·`Return`이 여전히 비어 있다.** 연타로는 문제가 안 났지만, 그건 "이 상황에서 안 났다"이지 핀을 채운 것과 같지 않다

### 총평

**요청은 "명령 39가자" 한 줄이었고, 그 한 줄이 명령 셋과 커밋 셋이 됐다.** 사양의 계획 표는 39 하나로 끝날 예정이었다.

이 작업의 실질적 난이도는 배치 산술이 아니었다. 좌표는 조사 30분이면 나온다. **어려웠던 것은 두 번, 겉으로 성공처럼 보이는 것을 성공으로 안 받아들인 자리다.**

첫 번째는 `save_assets`의 `true`다. 터미널이 그 `true`를 디스크와 대조하지 않았으면 배치가 끝난 줄 알고 다음으로 넘어갔을 것이고, 에디터를 끄는 순간 액터 셋이 사라졌을 것이다. 이 프로젝트가 지금까지 본 어긋남은 "성공했는데 `null`"이었는데 이번은 반대 방향이었다 — **`true`인데 일이 안 일어났다.** CLAUDE.md의 "MCP 응답을 성공 근거로 삼지 않는다"가 두 방향 다 필요하다는 것이 이번에 드러났다.

두 번째는 명령 34가 만든 버그다. 그 명령은 "하나의 노드가 `Branch.Condition`과 `Return.Success`를 동시에 먹여라, 두 번째 비교 노드를 만들지 마라"를 요구사항으로 못 박았고, 터미널이 그걸 정확히 지켰다. **요구사항을 어긴 게 아니라 지켜서 버그가 났다.** pure 노드를 공유하는 것은 캐시가 아니라 재계산이고, 그 사이에 배열이 바뀌면 두 읽기가 갈린다. 세 세션 동안 아무도 못 봤고 PIE에서만 드러났다.

버그를 잡은 것은 로그가 아니라 **증상의 조합**이었다. "열쇠는 사라졌는데 실패했다"는 배선상 재계산 말고는 설명이 없다. 그리고 고치기 전에 물약으로 반증 테스트를 한 번 돌린 것이, 편집을 하나도 안 하고 가설을 확정시켰다.

문 사양은 이걸로 끝났다. 합격 기준 넷 중 셋이 완전히 통과했고 하나(경첩 반전)가 절반 남았다.

## AI의 제안

> **사용자가 시키지 않았는데 AI가 먼저 꺼낸 것.**

1. **명령 39를 새로 만들어 배치 앞에 끼운 것**

   > `In /Game/Interaction/BP_Door, set the DoorMesh component's default RelativeScale3D so the door leaf is 10 x 100 x 220 cm instead of the 200 cm cube it is now.`

   사양의 계획 표에 39는 "레벨에 테스트 배치" 하나뿐이었다. 얻는 것 — 2m 큐브를 배치하고 나서 고치는 왕복을 없앤다. 잃는 것 — 명령 39가 "레벨 배치"라고 적힌 사양 표와 인계 문서가 그 순간부터 실제와 어긋난다.

2. **문짝 크기를 레벨 인스턴스가 아니라 BP 기본값에 넣자는 것**

   > 2m 큐브는 이 인스턴스 하나의 문제가 아니라 모든 문에 대해 틀린 값이다.

   얻는 것 — 문을 하나 더 놓을 때마다 같은 값을 다시 넣지 않아도 된다. 잃는 것 — 명령 39가 "레벨 배치"만 하는 게 아니라 BP를 건드리게 된다. 사용자가 심문에서 이 안을 골랐다.

3. **명령 39를 39·40으로 쪼개자는 것**

   > 문짝 스케일이 `BP_Door` 기본값 변경이라 레벨과 다른 애셋이고, 이게 안 먹으면 2m 큐브를 배치하는 셈이 되기 때문이다.

   얻는 것 — 스케일이 실제로 붙었는지 확인한 뒤에 배치한다. 잃는 것 — 명령이 하나 늘고 사양 표의 번호가 또 밀린다.

4. **고치기 전에 물약으로 반증 테스트를 하자는 것**

   > 이 가설이 **틀렸다면 무엇이 보일지**: 물약을 선택한 칸에 두고 문을 보고 `F`를 눌러라. 가설이 맞으면 `DOOR IS LOCKED`가 뜨고 **물약은 그대로 남는다.** 가설이 틀렸으면 물약도 같이 사라진다.

   얻는 것 — 편집을 하나도 안 하고 PIE 한 번으로 가설이 갈린다. 잃는 것 — 사용자에게 PIE를 한 번 더 돌리게 한다.

5. **`TryAddItem`을 지금 안 고치자는 것**

   > 같은 모양이지만 그 조건이 `FoundSlotIndex`라는 변수를 읽고, `SetArrayElem`은 `InventorySlots`를 쓴다. 재계산해도 값이 같다. **우연히 안전한 것이지 설계가 다른 게 아니다.**

   얻는 것 — 지금 버그가 아닌 것을 안 건드린다. 잃는 것 — 같은 함정이 하나 남는다.

6. **로컬 변수를 쓰자는 것 (멤버가 아니라)**

   > 멤버 변수로 만들면 캐릭터에 상태가 하나 늘고, 2단계 사양의 "`SelectedSlot` 하나가 유일한 상태다"가 깨진다.

   얻는 것 — 캐릭터의 공개 상태가 그대로다. 잃는 것 — `add_variable`의 `graph` 인자가 실제로 로컬을 만드는지 검증 단계가 하나 더 필요했다.

7. **`Ctrl+S`로 손 저장하자는 것 (MCP 재시도 대신)**

   > 엔진 소스에서 확인했다. `FileHelpers.cpp:4444-4453`이 `Level->GetLoadedExternalObjectPackages()`를 돌면서 `IsDirty()` 이거나 `PKG_NewlyCreated`인 패키지를 저장 목록에 넣는다.

   얻는 것 — 추측으로 다른 MCP 도구를 시험하는 왕복을 없앤다. 잃는 것 — 손 작업 지점이 하나 늘고, 앞으로 배치 명령마다 붙는다.

## 다음으로 넘김

**이 칸은 넘겼다.** 여기 있던 목록은 전부
[`2026-08-30-enemy-ai-navmesh.md`](2026-08-30-enemy-ai-navmesh.md)의 `다음으로 넘김`으로
옮겼다. **다음 세션은 그 기록을 읽는다.**

옮기면서 해결된 것은 그쪽 목록에서 뺐다 — "바로 이어서 할 것: 없음"(이제 명령 43이 있다),
카메라 작업의 크기(조사해서 A·B·C 셋으로 갈렸고 B가 유력하다는 것까지 나왔다).
그리고 항목이 늘었다 — `AI MoveTo`의 핀 확인, 적을 놓을 자리, NavMesh가 실제로
바닥을 덮었는지, 외부 패키지의 정체가 하나 더.
