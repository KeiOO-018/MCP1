# 2026-09-01

## 작업물

이월된 항목 여섯 개를 처리했다 — 인스턴스 편집 플래그 아홉 개 확인, 복귀 속도 측정, `BP_Enemy`의 `self` 연결 정리, 칼 손잡이 오프셋, 칸막이 라벨 통일, 디버그 노드 개수 정정.

**소요 시간**: 약 1시간 26분 (20:49 ~ 22:16)

## 명령

### 한글

```
작업 준비
```

```
이어서하자 확인필요는 너가 MCP 따로 써서 못하는 것들이야?
```

```
이거바바
```
(첨부: `BP_ThirdPersonCharacter` 에디터 스크린샷 1919px)

```
아 이거 스크롤 내리는게 안되는거야?
```
(첨부: `BP_Enemy` 에디터 스크린샷 1919px)

```
화면 캡처는 나한테물어봐 그게낫지않나
```

```
다했어 해바
```

```
네 개 할까
```

```
머부터 확인하냐 그럼 그리고 BP_Enemy이거 노드랑 이게 너무 보기 안좋게 연결되어 있는데 이 부분에 대해서는 뭐 제안이나 방법 같은건 없어? 없음말고
```

선택지 네 개에 대한 답 (AskUserQuestion, 전부 권장안 선택):

```
BP_Enemy의 self 핀을 어느 쪽으로 통일할까요?  → Self 연결 14개 끊기 (권장)
그래프 정리를 어디까지 할까요?                → self 연결 끊기까지만 (권장)
칼 손잡이 오프셋은?                           → +25 넣고 PIE 확인 (권장)
칸막이 라벨 리네임은?                         → 세 조각 다 통일 (권장)
```

```
결과 확인
```

```
PIE 결과 이상없음 2번가자
```

```
결과 확인 및 이미지 확인
```
(첨부: PIE 중 칼을 든 캐릭터 스크린샷 1919px)

```
결과 확인
```

```
정리 기록 한번 하고 다음꺼하자
```

### English — MCP에 실제로 보낸 명령

**명령 1 — `BP_Enemy`의 `self` 연결 끊기**

```
In /Game/Enemy/BP_Enemy:EventGraph, break 13 self-pin connections that come
from the two Self-Reference nodes, then delete the one Self node that becomes
orphaned. This is a readability change only. An unconnected self pin compiles
to the same self context (KismetCompiler.cpp:2185 - a self pin with
LinkedTo.Num()==0 and DefaultObject==nullptr is only checked for self
compatibility), so behaviour must not change.

There are exactly two Self-Reference nodes:
  K2Node_Self_1  at (0, 420)   - 12 outgoing connections
  K2Node_Self_2  at (0, 3474)  -  2 outgoing connections

STEP 0. Read both Self nodes with get_node_infos and report every outgoing
  connection: destination node refPath, destination node type_id, and the
  NAME of the destination pin. Confirm the list matches the 14 below exactly.
  If it does not match, STOP and report the difference. Do not guess.

STEP 1. Break these 13 connections, and only these 13. Each destination pin
  below is named "self". Before breaking each one, confirm the destination pin
  name really is "self". If any destination pin is NOT named "self", do NOT
  break it and report it.

  From K2Node_Self_1 (11):
    K2Node_CallFunction_37   Transformation|GetActorLocation           . self
    K2Node_CallFunction_39   Transformation|GetDistanceTo              . self
    K2Node_CallFunction_45   Pawn|GetController                        . self
    K2Node_CallFunction_47   Animation|PlayAnimMontage                 . self
    K2Node_CallFunction_48   Pawn|GetController                        . self
    K2Node_CallFunction_53   Pawn|GetController                        . self
    K2Node_CallFunction_64   Pawn|GetController                        . self
    K2Node_CallFunction_66   Transformation|SetActorRotation           . self
    K2Node_CallFunction_70   Pawn|GetController                        . self
    K2Node_CallFunction_171  Pawn|GetController                        . self
    K2Node_CallFunction_173  Transformation|GetHorizontalDotProductTo  . self

  From K2Node_Self_2 (2):
    K2Node_CallFunction_79   Transformation|GetActorLocation           . self
    K2Node_CallFunction_80   Transformation|GetActorRotation           . self

STEP 2. Do NOT break this connection. It is the 14th and it is NOT a self pin:
    K2Node_Self_1 -> K2Node_CallFunction_49
                     Game|Damage|ApplyDamage . DamageCauser
  DamageCauser is a real parameter. Breaking it would pass null.

STEP 3. Delete K2Node_Self_2. It has no remaining connections after STEP 1.
  Do NOT delete K2Node_Self_1 - it still feeds ApplyDamage.DamageCauser.
  Before deleting K2Node_Self_2, re-read it and confirm its output pin has
  zero connections. If it has any, STOP.

STEP 4. Compile BP_Enemy.

Do NOT move any node. Do NOT call arrange_nodes or set_node_position.
Do NOT create any node.
Do NOT delete or rename any Blueprint variable.
Do NOT change any default value: ThinkInterval 0.3, ReturnDelay 7,
HomeArriveRadius 100, ReturnStepDistance 300, ReturnSightRange 300,
SightRange 1200, SightHalfAngle 60, AttackRange 150, AttackDamage,
AttackCooldown all stay as they are.
Do NOT remove or modify any PrintString.
Do NOT touch BP_ThirdPersonCharacter or any animation asset.

REPORT:
 R1. the STEP 0 reading, verbatim - all 14 connections with pin names
 R2. every connection actually broken, one line each
 R3. the K2Node_Self_2 re-read before deletion, and the deletion result
 R4. re-read the whole graph and report the self-pin tally:
     how many self pins are wired, how many are empty.
     Expected after this change: 4 wired, 21 empty (before: 17 and 8).
 R5. confirm K2Node_Self_1 still exists and still connects to
     K2Node_CallFunction_49 . DamageCauser
 R6. the compile result with any warning text verbatim
```

**명령 2 — 칼 손잡이 오프셋**

```
In the DataTable /Game/Inventory/DT_Items, set the heldTransform property on
the row named "Knife" only.

Write the transform in FULL, all three fields, do not rely on partial-update
semantics:
  location  (0, 0, 25)
  rotation  (0, 0, 0)
  scale     (0.04, 0.04, 0.5)

The rotation and scale values above are the CURRENT values, restated on
purpose so they cannot be reset to identity by a partial write. Only the
location changes, from (0, 0, 0) to (0, 0, 25).

Note the read/write shape asymmetry on this property: set_rows takes
location / rotation / scale, while get_rows returns
Translation / Rotation (as a quaternion) / Scale3D. Expect the read-back to
come in the second shape.

Do NOT touch the rows Key_Stage1, Potion_Small or Ball_Test.
Do NOT touch displayName, iconColor, mesh, nature or healAmount on any row,
including Knife.
Do NOT touch BP_ThirdPersonCharacter, BP_Enemy, or any Blueprint.
Do NOT touch the Knife_Pickup actor in the level.

STEP 0. Read the Knife row with get_rows and report it verbatim.
STEP 1. Write heldTransform as specified above.
STEP 2. Read all four rows back with get_rows and report them verbatim.
STEP 3. Save the DT_Items asset.

REPORT:
 R1. the STEP 0 reading, verbatim
 R2. the exact JSON passed to set_rows, verbatim
 R3. the STEP 2 reading of all four rows, verbatim
 R4. confirm Knife's Scale3D is still (0.04, 0.04, 0.5) and its Rotation is
     still identity - a partial write wiping these is the main risk here
 R5. confirm the other three rows are unchanged: all still
     Translation (0,0,0), Rotation identity, Scale3D (0.15, 0.15, 0.15)
 R6. the save result
```

이 명령의 `Note the read/write shape asymmetry` 문단은 **틀렸다.** `set_rows`도 `Translation` / `Rotation` / `Scale3D`를 받는다. 이월 기록의 "쓸 때 `location/rotation/scale`"은 `SceneTools`·`ActorTools`의 `ToolsetTransform`에 해당하는 이야기였는데 그것을 DataTable에 그대로 옮겨 적었다. 첫 호출이 실패했고 두 번째가 통과했다.

**명령 3 — 칸막이 라벨 통일**

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, rename the
labels of the three actors that form the shared divider between room 1 and
room 2. This is a label change only. Do not move, scale, rotate, delete or
duplicate anything.

Current labels and target labels:
  "SM_Cube2"   ->  "Divider_L"
  "Divider_R"  ->  "Divider_M"
  "SM_Cube17"  ->  "Divider_R"

Note the middle step: the actor currently labelled "Divider_R" must be renamed
to "Divider_M" BEFORE "SM_Cube17" is renamed to "Divider_R", or two actors
will briefly share the label. Do them in the order listed above.

CAUTION on "SM_Cube2": the label "SM_Cube2" is a prefix of "SM_Cube20", and
find_actors matches labels by substring. There are exactly two actors whose
label contains "SM_Cube2". Only ONE of them is the divider: the one whose
location X is 1800. Before renaming, report both actors with their locations
and state which one you picked and why. If you cannot tell them apart by an
exact label match, STOP.

Do NOT rename any other actor. Do NOT touch SM_Cube3, SM_Cube4, SM_Cube5,
SM_Cube18, SM_Cube19, SM_Cube20, Floor, Floor_Room2, SM_SkySphere, Wall_L,
Wall_R, Door_Test, any Room2_Wall_*, any BP_ItemPickup, Knife_Pickup,
Enemy_Test, the NavMeshBoundsVolume or the RecastNavMesh.
Do NOT change any transform.
Do NOT touch any Blueprint or DataTable.

STEP 0. Find and report all actors whose label contains "SM_Cube2",
  "Divider" or "SM_Cube17". For each, report its object path, its exact
  label, and its world location, rotation and scale.
STEP 1. Rename the three labels in the order given.
STEP 2. Re-read all three actors and report their exact labels and their
  world location, rotation and scale.
STEP 3. Save the level.

REPORT:
 R1. the STEP 0 listing, verbatim
 R2. which actor you picked as "SM_Cube2" and how you told it from "SM_Cube20"
 R3. each rename performed, one line each
 R4. the STEP 2 re-read - confirm the three labels are now
     Divider_L, Divider_M, Divider_R
 R5. confirm all three transforms are UNCHANGED from the STEP 0 reading
 R6. confirm no other actor's label changed - re-list actors matching
     "SM_Cube" and report the full list
 R7. the save result
```

**옮기며 AI가 해석을 넣은 곳 셋.**

1. **`DamageCauser` 연결을 살린 것** (명령 1 STEP 2). 사용자는 "Self 연결 14개 끊기"를 골랐고 예외를 말하지 않았다. 14개 중 하나가 `self` 핀이 아니라 `ApplyDamage.DamageCauser`라는 것은 명령을 쓰기 직전 MCP로 조사하다 나왔고, 그것을 빼기로 한 것은 AI의 판단이다. 그 결과 `K2Node_Self_1`도 남았다.
2. **`Divider_L` / `Divider_M` / `Divider_R`이라는 이름** (명령 3). 사용자는 "세 조각 다 통일"만 정했고 이름은 안 정했다. 왼쪽부터 L/M/R로 둔 것은 AI가 정했다.
3. **`rotation`과 `scale`을 현재값 그대로 다시 적게 한 것** (명령 2). 지시에 없었다. `set_rows` 설명이 구조체 안쪽 필드까지 병합되는지 밝히지 않아, `location`만 보내면 `Scale3D (0.04, 0.04, 0.5)`가 단위값으로 날아갈 위험을 없애려고 넣었다.

**AI가 직접 MCP로 한 조사 호출.** 쓰기는 전부 사용자의 Terminal로 넘겼고, 아래는 AI가 읽기·검증에 쓴 것이다.

```
list_toolsets, describe_toolset x9
EditorToolset.EditorAppToolset.OpenEditorForAsset      x2
EditorToolset.EditorAppToolset.CaptureEditorImage      x2
EditorToolset.EditorAppToolset.GetOpenAssets           x1
EditorToolset.LogsToolset.GetLogCategories             x1
EditorToolset.LogsToolset.GetLogEntries                x9
editor_toolset.toolsets.blueprint.BlueprintTools.list_graphs      x3
editor_toolset.toolsets.blueprint.BlueprintTools.find_nodes       x5
editor_toolset.toolsets.blueprint.BlueprintTools.get_node_infos   x7
editor_toolset.toolsets.blueprint.BlueprintTools.read_graph_dsl   x1
editor_toolset.toolsets.object.ObjectTools.get_properties         x1
editor_toolset.toolsets.data_table.DataTableTools.get_rows        x5
editor_toolset.toolsets.programmatic.ProgrammaticToolset.get_execution_environment x3
editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script       x18
editor_toolset.toolsets.programmatic.ProgrammaticToolset.run_script                x1  (존재하지 않는 툴)
```

## Terminal 결과

### 원문 — English

**`UBlueprint`에 닿으려다 CDO로 리다이렉트된 것**

```
GetObjectProperties on '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.Default__BP_ThirdPersonCharacter_C' (BP_ThirdPersonCharacter_C): the following properties could not be read: NewVariables
```

**`ActorLabel`을 읽으려다 실패한 것 — 17개 액터 전부 같은 실패, 앞 3줄만 발췌**

```
GetObjectProperties on '/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.StaticMeshActor_UAID_F4A475FF15A3736A02_1961928692' (StaticMeshActor): the following properties could not be read: ActorLabel
GetObjectProperties on '/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.StaticMeshActor_UAID_9C6B005AF86931FD02_2140508290' (StaticMeshActor): the following properties could not be read: ActorLabel
GetObjectProperties on '/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default' (RecastNavMesh): the following properties could not be read: ActorLabel
```

**`list_graphs`에 애셋 경로를 그대로 넣었을 때**

```
Parameter error: /Game/Enemy/BP_Enemy is not a valid object path for property 'blueprint'
```

같은 것이 UE 로그에도 남았다.

```
[2026.09.01-12.15.45:068][880]LogScript: Warning: /Game/Enemy/BP_Enemy is not a valid object path for property 'blueprint'
```

**`ProgrammaticToolset`의 `_StrictDict` 제약**

```
line 22: TypeError: _StrictDict.get() does not support a default value. Use direct key access [] instead.
Traceback (script frames only):
  File "<script>", line 22, in run
    tid = i.get("type_id", "?")
          ^^^^^^^^^^^^^^^^^^^^^
```

**존재하지 않는 툴 이름을 부른 것**

```
Unknown tool run_script
```

**`CaptureEditorImage`가 컨텍스트 한도를 넘긴 것 — 두 번 다 같은 형태, 첫 번째만 발췌**

```
Error: result (369,726 characters across 1 line) exceeds maximum allowed tokens. Output has been saved to C:\Users\a0108\.claude\projects\d--20260827-MCP1\d603dd88-3cff-43c0-ad5b-9cdb5a8984d2\tool-results\mcp-unreal-mcp-call_tool-1788263519751.txt.
```

**명령 2의 첫 번째 `set_rows`가 실패한 것 — 전문**

```
[2026.09.01-12.54.04:875][677]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.data_table.DataTableTools.set_rows'
[2026.09.01-12.54.04:877][677]LogCSVImportFactory: Imported DataTable 'DT_Items' - 3 Problems
[2026.09.01-12.54.04:877][677]LogCSVImportFactory: 0:Row 'Knife' is missing an entry for 'W'.
[2026.09.01-12.54.04:877][677]LogCSVImportFactory: 1:Row 'Knife' is missing an entry for 'Translation'.
[2026.09.01-12.54.04:877][677]LogCSVImportFactory: 2:Row 'Knife' is missing an entry for 'Scale3D'.
```

26초 뒤의 두 번째 호출.

```
[2026.09.01-12.54.30:208][753]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.data_table.DataTableTools.set_rows'
[2026.09.01-12.54.30:209][753]LogCSVImportFactory: Imported DataTable 'DT_Items' - 0 Problems
```

**명령 1의 컴파일 — 진단이 한 줄도 안 붙었다**

```
[2026.09.01-12.41.20:183][264]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.01-12.41.20:275][264]LogUObjectHash: Compacting FUObjectHashTables data took   1.88ms
```

**복귀 속도 측정 — 변경 전 (12:18), `3_home` 발췌**

```
12.18.01:017  CHASE
12.18.05:894  IDLE_WAIT
12.18.12:626  RETURN
12.18.12:934  home=1370.237907
12.18.13:243  home=1278.261209
12.18.13:846  home=1096.648235
12.18.14:770  home=819.486048
12.18.15:683  home=545.474380
12.18.16:603  home=269.668002
12.18.17:213  home=86.660239
12.18.17:213  IDLE_HOME
```

**복귀 속도 측정 — 변경 후 (12:47), 전체**

```
12.46.57:323 STATE=IDLE_HOME
12.47.09:333 STATE=CHASE
12.47.13:010 STATE=IDLE_WAIT
12.47.19:726 STATE=RETURN
12.47.20:034  home=1008.531826
12.47.20:340  home=916.76939
12.47.20:647  home=824.709145
12.47.20:953  home=732.799111
12.47.21:259  home=640.896038
12.47.21:574  home=546.503928
12.47.21:875  home=456.29724
12.47.22:182  home=364.167647
12.47.22:489  home=272.000418
12.47.22:800  home=178.98881
12.47.23:107  home=86.920735
12.47.23:107 STATE=IDLE_HOME
12.47.26:199 STATE=CHASE
```

**`EditorPerProjectUserSettings.ini` 저장 실패 — 재시도 9회 중 첫 줄과 최종 실패 줄만 발췌**

```
[2026.09.01-12.37.52:453][423]LogFileManager: Warning: MoveFile was unable to move 'D:/20260827/MCP1/Saved/EditorPerProjectUserSettings13C82E534D1817793B2D71AA28CFFC4A.tmp' to 'D:/20260827/MCP1/Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini' (Error Code 183), retrying in .5s...
[2026.09.01-12.37.56:960][423]LogFileManager: Error: Error moving file 'D:/20260827/MCP1/Saved/EditorPerProjectUserSettings13C82E534D1817793B2D71AA28CFFC4A.tmp' to 'D:/20260827/MCP1/Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini'.
```

**`server/discover` 오류 — 이번에도 한 번**

```
[2026.09.01-12.38.03:125][926]LogModelContextProtocol: Error: Call to unknown method "server/discover"
```

**한글 글리프 경고 — 4줄 중 2줄 발췌**

```
[2026.09.01-12.42.32:011][607]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c624, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.01-12.42.32:022][607]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+d6c4, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
```

**인스턴스 편집 아이콘의 근거 — 엔진 소스**

```
Engine/Source/Editor/Kismet/Private/SBlueprintPalette.cpp:1077-1081
	const FSlateBrush* GetVisibilityIcon() const
	{
		return GetVisibilityToggleState() == ECheckBoxState::Checked ?
			FAppStyle::GetBrush( "Kismet.VariableList.ExposeForInstance" ) :
			FAppStyle::GetBrush( "Kismet.VariableList.HideForInstance" );
	}
```

```
Engine/Source/Editor/EditorStyle/Private/StarshipStyle.cpp:5999-6000
		Set("Kismet.VariableList.ExposeForInstance", new CORE_IMAGE_BRUSH_SVG("Starship/Common/visible", Icon16x16));
		Set("Kismet.VariableList.HideForInstance", new CORE_IMAGE_BRUSH_SVG("Starship/Common/hidden", Icon16x16));
```

**빈 `self` 핀의 컴파일 처리 — 엔진 소스**

```
Engine/Source/Editor/KismetCompiler/Private/KismetCompiler.cpp:2185-2188
					if (Schema->IsSelfPin(*Pin) && (Pin->LinkedTo.Num() == 0) && Pin->DefaultObject == nullptr)
					{
						FKismetCompilerUtilities::ValidateSelfCompatibility(Pin, Context);
					}
```

**액터 라벨 변경이 오브젝트를 리네임하지 않는 근거 — 엔진 소스**

```
Engine/Source/Runtime/Engine/Private/ActorEditor.cpp:1305-1313
	else if (FCString::Strcmp(*NewActorLabel, *GetActorLabel(false)) != 0)
	{
		// Store new label
		Modify(bMarkDirty);
		ActorLabel = MoveTemp(NewActorLabel);

		FPropertyChangedEvent PropertyEvent(FindFProperty<FProperty>(AActor::StaticClass(), "ActorLabel"));
		PostEditChangeProperty(PropertyEvent);
```

**`NewVariables`의 선언 — 엔진 소스**

```
Engine/Source/Runtime/Engine/Classes/Engine/Blueprint.h:590-592
	/** Array of new variables to be added to generated class */
	UPROPERTY()
	TArray<FBPVariableDescription> NewVariables;
```

### 요약 — 한글

- `BP_Enemy`의 `EventGraph`에서 `self` 핀으로 가는 연결 13개가 끊겼다. `K2Node_Self_2`가 지워졌다. `K2Node_Self_1`은 남았고 `K2Node_CallFunction_49`(`Game|Damage|ApplyDamage`)의 `DamageCauser` 핀 하나만 먹인다. 노드 수 99 → 98. `self` 핀 집계 `wired 17 / empty 8` → `wired 4 / empty 21`. 컴파일에 에러도 경고도 없었다
- `DT_Items`의 `Knife` 행에서 `heldTransform.Translation`이 `(0, 0, 0)` → `(0, 0, 25)`가 됐다. `Rotation`은 단위값, `Scale3D`는 `(0.04, 0.04, 0.5)` 그대로. 나머지 세 행(`Key_Stage1`, `Potion_Small`, `Ball_Test`)은 `Translation (0,0,0)` / `Rotation` 단위값 / `Scale3D (0.15, 0.15, 0.15)`로 무변경
- 레벨의 액터 라벨 셋이 바뀌었다. `SM_Cube2` → `Divider_L`, `Divider_R` → `Divider_M`, `SM_Cube17` → `Divider_R`. 오브젝트 경로는 각각 `..._1961959730`, `..._1392108111`, `..._1961956726`으로 리네임 전과 같다. `SM_Cube20`(`..._1961929693`)은 안 건드려졌다
- `git status` 기준 바뀐 파일 여섯 개 — `Content/Enemy/BP_Enemy.uasset`, `Content/Inventory/DT_Items.uasset`, `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset`, `Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/` 아래 `.uasset` 셋
- `Lvl_ThirdPerson.umap` 자체는 안 바뀌었다

## 분석

### 무엇을 만들었나

**만든 것은 없다. 이번 세션은 전부 확인·정정·정리다.**

**확인 — 인스턴스 편집 플래그 아홉 개, 전부 켜짐**

`BP_ThirdPersonCharacter` 넷.

| 변수 | 타입 | 인스턴스 편집 |
|---|---|---|
| `RespawnDelay` | Float | 켜짐 |
| `AttackMontage` | Anim Montage | 켜짐 |
| `AttackRange` | Float | 켜짐 |
| `AttackTraceRadius` | Float | 켜짐 |

`BP_Enemy` 다섯.

| 변수 | 타입 | 인스턴스 편집 |
|---|---|---|
| `ReturnDelay` | Float | 켜짐 |
| `ReturnSightRange` | Float | 켜짐 |
| `ReturnStepDistance` | Float | 켜짐 |
| `HomeArriveRadius` | Float | 켜짐 |
| `SightHalfAngle` | Float | 켜짐 |

같은 화면에서 읽힌 대조군.

- `BP_ThirdPersonCharacter` 켜짐 — `FirstPersonPitchMin`, `FirstPersonPitchMax`, `ThirdPersonPitchMin`, `ThirdPersonPitchMax`, `MaxHP`, `InteractDistance`
- `BP_ThirdPersonCharacter` 꺼짐 — `bIsFirstPerson`, `InventorySlots`, `SelectedSlot`, `CurrentHP`, `FoundSlotIndex`
- `BP_Enemy` 켜짐 — `SightRange`, `AttackRange`, `AttackDamage`, `AttackCooldown`, `ThinkInterval`, `AttackMontage`
- `BP_Enemy` 꺼짐 — `PlayerRef`, `LastSeenTime`, `HomeLocation`, `HomeRotation`

**확인 — 복귀 속도**

변경 전(12:18) `1370.237907 → 86.660239`을 4.279초에, 초당 **299.97**.
변경 후(12:47) `1008.531826 → 86.920735`을 3.073초에, 초당 **299.9**.
`MaxWalkSpeed`는 300이다.

`IDLE_WAIT` → `RETURN` 사이 간격은 각각 6.732초, 6.716초. `ReturnDelay 7`, `ThinkInterval 0.3`이다.
둘 다 `86.x`에서 멈추고 `IDLE_HOME`으로 넘어갔다. `HomeArriveRadius 100`이다.

이월 기록에 남아 있던 관측치는 명령 70 이전 초당 180, 이후 초당 45였다. 지금은 300이다.

**정정 — 디버그 노드 개수**

`type_id`로 모든 그래프의 노드를 전수 조사한 결과.

| | 이월 기록 | 실제 |
|---|---|---|
| `BP_Enemy` `Development\|PrintString` | 8 | 9 |
| `BP_Enemy` `Utilities\|String\|ToString(Float)` | 3 | 3 |
| `BP_ThirdPersonCharacter` `Development\|PrintString` | 10 | 2 |
| `BP_ThirdPersonCharacter` `Utilities\|String\|ToString(Float)` | 3 | 0 |
| `DrawDebugType ForDuration` | 1 | 1 |

`BP_ThirdPersonCharacter`의 둘 중 하나는 `ShowHUDMessage` 함수 안에 있고 그 기능의 구현체다. 디버그로 지울 대상이 아니다. 남는 디버그는 `EventGraph`의 `K2Node_CallFunction_86` 하나. `DrawDebugType ForDuration`은 노드가 아니라 `Collision|SphereTraceForObjects`(`K2Node_CallFunction_83`)의 핀 값이다.

그래프별 노드 총수도 같이 나왔다.

```
BP_ThirdPersonCharacter
  UserConstructionScript  1     Move 11     Aim 5     ToggleCameraView 34
  RefreshHeldItem 20      ShowHUDMessage 6           TryAddItem 12
  TryConsumeSelected 14   CanJumpInternal 6          EventGraph 143
BP_Enemy
  UserConstructionScript  1     EventGraph 99 (작업 후 98)
```

**정리 — `BP_Enemy`의 `self` 연결**

작업 전 그래프 범위는 `x 0..10920`, `y 300..3554`. `Self` 노드가 둘이었고 (`K2Node_Self_1` at `(0, 420)` 팬아웃 12, `K2Node_Self_2` at `(0, 3474)` 팬아웃 2), 그 14개가 폭 11000짜리 그래프를 가로질렀다. 13개를 끊고 `K2Node_Self_2`를 지웠다. `DamageCauser`로 가는 한 개만 남았다.

**정정 — 칸막이는 짝이 아니라 세 조각**

`SM_Cube2` / `Divider_R` / `SM_Cube17`. 이월 기록은 앞의 둘만 짝으로 보고 `SM_Cube17`을 빠뜨렸다. 셋을 `Divider_L` / `Divider_M` / `Divider_R`로 통일했다.

**변경 — 칼 손잡이**

`Knife.heldTransform.Translation`이 `(0, 0, 25)`가 됐다. 메시는 `/Engine/BasicShapes/Cube.Cube`에 `Scale3D (0.04, 0.04, 0.5)`이라 로컬 Z로 ±25 뻗는다. 오프셋 25는 그 절반 길이다.

### 기술적으로 맞게 짚은 부분

**빈 `self` 핀을 "미완성"이 아니라 "정상"으로 읽은 것.** 이월 기록은 `K2Node_CallFunction_21`의 빈 `self`를 나머지 여섯처럼 명시로 바꿀지 묻고 있었다. 방향이 반대였다. `KismetCompiler.cpp:2185`는 `self` 핀이 `LinkedTo.Num() == 0`이고 `DefaultObject == nullptr`일 때 `ValidateSelfCompatibility`만 부르고 넘어간다 — 즉 연결이 없으면 self 컨텍스트로 컴파일된다. 명시 연결은 정보를 하나도 더 주지 않으면서 그래프를 가로지르는 선을 하나 더 그린다. 어긋난 하나가 옳았고 나머지 여섯이 틀렸던 셈이다.

**끊기 전에 목적지 핀 이름을 확인한 것.** `Self` 노드에서 나가는 14개 중 13개만 `self` 핀이었다. 14번째는 `Game|Damage|ApplyDamage`의 `DamageCauser`로, 이름이 다르고 의미도 다르다. 끊었으면 `ApplyDamage`가 null causer로 호출됐을 것이다. 지금은 플레이어의 `EventAnyDamage`가 `DamageCauser`를 안 읽어서 티가 안 났겠지만, 다음 사양인 적 HP·피격·사망에서 "누가 때렸는가"가 필요해지는 값이다. **"자기 자신을 가리키는 선"과 "자기 자신을 인자로 넘기는 선"은 그리는 모양이 같고 뜻이 다르다.**

**라벨 변경이 참조를 안 끊는다는 것을 소스로 확인한 것.** CLAUDE.md는 리네임이 "컴파일 에러 없이 조용히 끊는다"고 경고한다. 그 경고는 BP 변수·함수·이벤트 디스패처 이름에 대한 것이고 액터 라벨은 다르다. `AActor::SetActorLabel`(`ActorEditor.cpp:1291`)은 `ActorLabel` FString만 갈아끼우고 `Rename()`을 부르지 않는다. 오브젝트 이름은 그대로다. 실제로도 리네임 뒤에 오브젝트 경로가 그대로였고, 그래서 어느 액터가 어느 라벨을 받았는지 경로로 추적할 수 있었다.

**`SM_Cube2` / `SM_Cube20` 부분 일치를 명령에 못박은 것.** `find_actors`의 `name`은 부분 문자열로 라벨을 거른다. `SM_Cube2`로 찾으면 `SM_Cube20`도 잡힌다. 같은 함정이 2026-08-31 기록에 이미 한 번 적혀 있었다 — `SM_Cube`가 `SM_Cube2`~`SM_Cube20`을 잡아먹으면 벽이 통째로 날아간다. 명령에 "둘 중 X가 1800인 쪽", "구분 못 하면 STOP"을 넣었고, 사후에 `SM_Cube2` 검색 결과가 2개 → 1개로 줄고 남은 것이 칸막이 영역 밖이라는 것으로 확인했다.

**리네임 순서를 지정한 것.** `SM_Cube17`을 먼저 `Divider_R`로 바꾸면 기존 `Divider_R`과 잠깐 라벨이 겹친다. `Divider_R` → `Divider_M`을 먼저 하도록 순서를 못박았다.

**구조체 필드를 전부 다시 적게 한 것.** `set_rows` 설명은 "Only specified properties are updated"라고만 하고 구조체 **안쪽** 필드의 병합 규칙을 밝히지 않는다. `location`만 보냈다가 `Scale3D`가 단위값으로 돌아가면 칼이 한 변 100짜리 큐브가 된다. 세 필드를 다 적게 한 덕에 그 경우가 안 생겼다.

**동작이 안 바뀌는 변경에 "안 바뀜"을 합격 기준으로 세운 것.** 명령 1은 가독성 변경이라 "무엇이 좋아졌나"로는 검증이 안 된다. 대신 `self` 핀 집계를 사전에 `4 / 21`로 예측해서 숫자로 걸었고, 그 다음 PIE 로그로 상태 전이와 복귀 속도가 그대로인지 봤다. 초당 299.97 → 299.9로 나왔다.

**로그 파일을 직접 읽은 것.** `PrintString`은 `bPrintToLog`이 `true`라 `LogBlueprintUserMessages`에 남는다. `GetLogEntries`는 524줄을 통째로 컨텍스트에 올리지만 `Saved/Logs/MCP1.log`를 `grep`/`awk`로 걸면 필요한 줄만 본다. 복귀 속도 측정을 사용자 눈이 아니라 숫자로 할 수 있었던 이유다.

**세 숫자 중 어느 것이 홈까지 거리인지 대조군으로 가른 것.** `PrintString`의 `Key`는 화면 중복 제거용이라 로그에 안 찍힌다. 로그에는 라벨 없는 숫자만 나온다. `IDLE_WAIT` 22틱 동안 두 번째 값만 `1441.991848`로 완전히 고정돼 있었고 — 서서 기다리는 상태와 정확히 맞는다 — 첫 번째 값은 같은 구간에 1431~1934로 출렁였다. 추론이 아니라 대조로 갈랐다.

**손대지 않은 것이 옳았던 것 셋.** `ReturnStepDistance`는 이제 아무도 안 읽지만 여전히 남겨뒀다. `arrange_nodes`를 99개 전체에 걸지 않았다 — 손으로 맞춘 배치가 통째로 날아가고 되돌리기 어렵다. 디버그 노드를 지금 지우지 않았다 — 이번 세션의 복귀 속도 측정이 바로 그 `PrintString`으로 이뤄졌고, 다음 사양인 적 HP·피격·사망에서 또 쓴다.

### 확인한 것 / 확인 못 한 것

**확인한 것**

- **인스턴스 편집 플래그 아홉 개가 전부 켜짐.** 사용자가 붙여준 1919px 스크린샷 2장에서 눈 아이콘을 읽었고, 아이콘의 뜻은 `SBlueprintPalette.cpp:1079-1080` → `StarshipStyle.cpp:5999-6000`으로 확정했다. 대조군(꺼진 변수 아홉)이 전부 런타임 상태 변수였다는 점이 읽기를 뒷받침한다
- **`self` 핀 집계가 `wired 4 / empty 21`.** 명령 전에 예측한 숫자와 일치. MCP로 다시 읽었다
- **`K2Node_Self_2`가 지워지고 노드 수가 99 → 98.** MCP로 다시 읽었다
- **`K2Node_Self_1`이 남았고 `K2Node_CallFunction_49`의 `DamageCauser`만 먹인다.** MCP로 다시 읽었다
- **컴파일에 에러도 경고도 없음.** UE 로그에서 컴파일 줄과 그 다음 줄 사이에 진단이 하나도 없다
- **동작이 안 바뀜.** 변경 후 PIE 로그에서 `CHASE → IDLE_WAIT → RETURN → IDLE_HOME`이 그대로 났고, 복귀 속도 299.9, 대기 6.716초, 정지 거리 86.92
- **`Knife.heldTransform`이 `Translation (0,0,25)` / `Rotation` 단위값 / `Scale3D (0.04, 0.04, 0.5)`.** MCP로 다시 읽었다. 우려했던 스케일 소실이 안 일어났다
- **나머지 세 행 무변경.** MCP로 다시 읽었다
- **라벨 셋이 `Divider_L` / `Divider_M` / `Divider_R`.** 각 이름으로 `find_actors`를 돌려 정확히 하나씩 잡혔고, 오브젝트 경로가 리네임 전 조사와 같다
- **`SM_Cube17` 0개, `SM_Cube2` 1개(= `SM_Cube20`), `Divider` 3개.** 오염 없음
- **`__ExternalActors__` 아래 `.uasset` 세 개만 바뀜.** 리네임한 액터 수와 일치
- **`CaptureEditorImage`가 존재하고 동작한다.** 두 번 찍었다. 반환 크기는 두 번 다 1280x688 고정
- **`bPrintToLog`이 `true`.** `K2Node_CallFunction_41`(`2_dist`)과 `K2Node_CallFunction_176`(`4_angle`) 두 노드에서 핀 값을 읽었다
- **`EditorPerProjectUserSettings.ini` 저장 실패가 재현된다.** 이번에도 아홉 번 재시도 후 최종 실패

**확인 못 한 것**

- **`Divider_L` / `M` / `R`이 실제 좌우 순서와 맞는지.** 라벨이 붙은 것만 확인했다. 리네임 **전에 세 액터의 트랜스폼을 기록해두지 않았다.** `find_actors`의 바운즈 검사로 셋 다 `X 1750..2050` 안에 있다는 것만 확인했고, 그 안에서 Y가 어떤 순서인지는 안 봤다
- **세 액터의 트랜스폼이 안 바뀐 것.** 위와 같은 이유. 300유닛 폭 바운즈 안의 이동은 이 검사로 안 걸린다
- **칼이 정확히 끝을 쥔 모양인지.** 스크린샷에서 막대가 손 앞으로 뻗는 것은 보였다 — 부호가 맞았다는 뜻이다. 하지만 캐릭터를 옆·뒤에서 본 각도라 손과 막대 시작점이 겹쳐서, 손 뒤로 조금 남았는지는 판단이 안 된다
- **`BP_ThirdPersonCharacter.uasset`이 왜 dirty가 됐는지.** 명령 1은 `BP_Enemy`만 건드렸는데 둘 다 dirty가 됐다. 다만 세션 초반에 AI가 `OpenEditorForAsset`으로 그 BP를 열어둔 것도 있어서 **둘 중 무엇이 원인인지 구분이 안 된다**
- **`PrintString` 개수가 8에서 9로 늘어난 시점.** 이월 기록은 8이라고 적었고 지금 9다. 언제 하나가 늘었는지 기록에 없다
- **`BP_ThirdPersonCharacter`의 `PrintString`이 왜 10으로 적혔었는지.** 실제는 2다. 세어본 근거가 이월 기록에 안 남아 있다
- **`arrange_nodes`가 실제로 어떤 결과를 내는지.** 이 프로젝트에서 한 번도 안 써봤다
- **`ProgrammaticToolset`으로 코멘트 노드를 만들 수 있는지.** 제안만 하고 안 봤다

### 남는 리스크

- **`K2Node_Self_1`이 혼자 남아 `x=0`에 서 있다.** 팬아웃 1짜리 노드가 그래프 맨 왼쪽에 있고 거기서 나온 선 하나가 여전히 그래프를 가로지른다. 없앨 수는 있다 — `ApplyDamage` 근처로 옮기면 선이 짧아진다. 이번 결정 범위 밖이었다
- **칼이 수평으로 몸 앞을 향해 뻗는다.** 칼처럼 세워 쥔 모양이 아니다. `heldTransform.Rotation`이 단위값이라 그렇고, 이번에 정한 것은 위치뿐이다
- **`Divider_L` / `M` / `R`의 좌우가 틀렸을 수 있다.** 이름을 AI가 정했고 실제 배치와 대조하지 않았다. 틀렸다면 이름이 뜻을 반대로 말하게 된다 — 라벨이 없는 것보다 나쁘다
- **`ReturnStepDistance 300`이 읽히지 않는 값으로 남아 있다.** 지난 세션부터 그대로다. 나중에 이 값을 바꾸고 "왜 안 변하지" 하는 일이 생길 수 있다
- **디버그 표시가 그대로 있다.** `BP_Enemy`에 `PrintString` 아홉과 `ToString(Float)` 셋, `BP_ThirdPersonCharacter`에 `PrintString` 하나(+ `ShowHUDMessage`의 하나는 기능)와 `SphereTraceForObjects`의 `DrawDebugType ForDuration`. 남기기로 정했다
- **로그의 `PrintString` 값에 라벨이 없다.** 화면에는 `2_dist` / `3_home` / `4_angle`로 구분되지만 로그에는 숫자만 나온다. 이번엔 대조군으로 갈랐지만, 프린트 순서가 바뀌면 과거 로그의 해석이 틀어진다
- **`EditorPerProjectUserSettings.ini` 저장이 매번 실패한다.** 일회성이 아님이 확인됐다. 무엇을 잃고 있는지는 모른다

### 총평

요청은 이월 목록을 소화하는 것이었고, `바로 이어서 할 것` 둘과 `결정 필요` 넷 중 셋을 처리했다. 나머지 하나(디버그 제거)는 의도적으로 미뤘다.

**이 작업의 실질적 난이도는 만드는 것이 아니라 이월 기록을 믿지 않는 데 있었다.** 손댄 네 항목 중 **셋이 전제부터 틀려 있었다.**

- 디버그 노드 개수 — 플레이어 쪽이 10+3+1이 아니라 1+1
- 칸막이 — 짝이 아니라 세 조각
- `self` 핀 — 하나를 여섯에 맞추는 게 아니라 여섯을 하나에 맞추는 문제

셋 다 "기록대로 명령을 썼으면 틀린 것을 정성껏 실행했을" 경우다. 특히 `self` 핀은 기록대로 했으면 그래프가 더 나빠졌다. 사용자가 "노드 연결이 보기 안 좋다"고 따로 짚어주지 않았으면 방향이 안 뒤집혔을 것이다.

**AI가 쓴 명령에도 틀린 것이 하나 있었다.** 명령 2의 `set_rows` 쓰기 모양을 이월 기록의 "읽기/쓰기 비대칭"에서 그대로 가져다 썼는데, 그 비대칭은 `ToolsetTransform`을 쓰는 툴셋 이야기지 `DataTableTools`가 아니었다. 첫 호출이 `3 Problems`로 실패하고 두 번째가 통과했다. 기록의 관찰을 다른 툴셋에 그대로 옮긴 것이 원인이다.

## AI의 제안

1)
```
Break the 13 self-pin connections coming from the two Self-Reference nodes in
BP_Enemy:EventGraph, and delete K2Node_Self_2. An unconnected self pin
compiles to the same self context (KismetCompiler.cpp:2185), so behaviour
does not change. This removes 14 long wires crossing an 11,000-unit-wide
graph, leaving only the one that feeds ApplyDamage.DamageCauser.
```
얻는 것 — 그래프를 가로지르는 장거리 선이 14개에서 1개로 준다. 노드도 하나 준다. 잃는 것 — `self` 대상이 명시로 보이지 않는다. 노드를 클릭해서 빈 핀에 `self`라고 쓰여 있는 것을 봐야 안다.

2)
```
Rename all three divider pieces, not just SM_Cube2:
  "SM_Cube2"   ->  "Divider_L"
  "Divider_R"  ->  "Divider_M"
  "SM_Cube17"  ->  "Divider_R"
```
얻는 것 — 세 조각이 한 무리로 보인다. `Divider`로 검색하면 셋이 다 나온다. 잃는 것 — 이월 기록·과거 명령문에 적힌 `SM_Cube2` / `SM_Cube17`이 더 이상 지금 라벨과 안 맞는다. 옛 기록을 읽을 때 대조가 한 단계 더 필요해진다.

3)
```
Restate rotation and scale explicitly when writing heldTransform, instead of
sending location alone. set_rows does not document whether inner struct
fields are merged, and a partial write could reset Scale3D (0.04, 0.04, 0.5)
to identity.
```
얻는 것 — 병합 규칙에 의존하지 않는다. 잃는 것 — 현재값을 명령문에 손으로 옮겨 적어야 하고, 옮겨 적다 틀리면 그 값이 그대로 덮어써진다.

4)
```
Read Saved/Logs/MCP1.log directly with grep/awk instead of GetLogEntries,
for anything more than a spot check.
```
얻는 것 — 524줄을 컨텍스트에 올리지 않고 필요한 줄만 본다. `awk`로 집계·계산까지 한 번에 된다. 잃는 것 — 에디터가 아직 flush 하지 않은 최신 몇 줄이 파일에 없을 수 있다. `GetLogEntries`는 그 점에서 더 즉각적이다.

5)
```
Do not call CaptureEditorImage. Ask the user for a screenshot instead.
```
얻는 것 — 1919px 대 1280x688. 16px 아이콘을 읽을 수 있다. 스크롤이 필요한 경우에도 사용자 손이 어차피 든다. 잃는 것 — 왕복이 한 번 더 생긴다. 사용자가 자리에 없으면 진행이 멈춘다.

## 다음으로 넘김

**바로 이어서 할 것**

없음. (좌우 확인은 2026-09-01 `enemy-hp-death` 세션에서 처리됨 — 세 조각이 좌·중·우가 아니라 문설주 둘과 상인방 하나였고, 이름을 `Divider_L` / `Divider_R` / `Divider_Top`으로 다시 고쳤다)

**결정 필요**

적 HP·피격·사망은 착수해서 끝났다. 남은 셋(디버그 표시 제거 시점, 칼의 회전, `K2Node_Self_1` 이동)은 갱신된 개수와 함께 `2026-09-01-enemy-hp-death.md`로 넘어갔다.

**확인 필요**

- **`arrange_nodes`가 실제로 어떤 배치를 내는지.** 걸어보려면 `RETURN` 분기 하나로 좁혀서 걸고 결과를 본다
- **`ProgrammaticToolset`으로 코멘트 노드를 만들 수 있는지**
- **`BP_Enemy`의 `PrintString`이 8에서 9로 언제 늘었는지**
- **`BP_ThirdPersonCharacter`의 `PrintString`이 왜 10으로 기록됐었는지.** 실제는 2다
- **`BP_Enemy`가 왜 `BP_ThirdPersonCharacter` 컴파일에 딸려 dirty가 되는지.** 이번엔 방향이 반대로 났고, AI가 에디터를 열어둔 것과 구분이 안 됐다
- **`read_graph_dsl`이 그래프를 통째로 안 뱉는다.** `BP_ThirdPersonCharacter:EventGraph`를 읽었더니 `IA_Interact`·`IA_Attack`·`IA_UseItem`의 본문이 `bind` 몇 줄에서 끊겼고 `PrintString`이 하나도 안 나왔다. `find_nodes`는 같은 그래프에서 143개 노드를 반환한다. **DSL로 그래프 전체를 판단하면 안 된다**
- **MCP가 못 읽는 프로퍼티 목록.** `AttachSocketName`, `attachParent`, `CollisionEnabled`, `Notifies`, `bEnableRootMotionTranslation`, `bEnableRootMotionRotation`, `bRootMotionSettingsCopiedFromMontage`, `SlotGroups`, `SlotToGroupNameMap`에 이번에 **`NewVariables`와 `ActorLabel`이 추가됐다.** `NewVariables`는 edit 지정자 없는 `UPROPERTY()`다 (`Blueprint.h:591`)
- **MCP는 블루프린트 애셋 경로를 항상 CDO로 리다이렉트한다.** `/Game/.../BP_X.BP_X`를 주면 `Default__BP_X_C`를 잡는다. `UBlueprint` 객체 자체에 닿을 길이 없다. 인스턴스 편집 플래그를 읽을 수단이 없는 **이유**가 이것이다
- **`ProgrammaticToolset`의 dict가 `_StrictDict`다.** `.get(key, default)`가 막혀 있고 직접 키 접근만 된다
- **`DataTableTools.set_rows`는 `Translation` / `Rotation`(`W` 포함) / `Scale3D`를 받는다.** `location` / `rotation` / `scale`이 아니다. 쓰기 경로가 `LogCSVImportFactory`를 탄다 — 실패가 `Imported DataTable 'DT_Items' - N Problems`로 나온다
- **`CaptureEditorImage`가 PIE 중에도 되는지.** 되면 "PIE 화면을 못 본다"는 제약이 사라진다. `CaptureViewport`가 에디터 월드를 렌더하는 이월 항목도 여기서 답이 날 수 있다
- **`LogCrowdFollowing: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance`**
- **`LogModelContextProtocol: Error: Call to unknown method "server/discover"`.** 이번에도 세션당 한 번 찍혔다
- **`EditorPerProjectUserSettings.ini` 저장 실패 (`Error Code 183`).** 이번에도 아홉 번 재시도 후 최종 실패. **매번 나는 것이 확인됐다**
- **`read_graph_dsl`과 `write_graph_dsl`의 id 체계가 다른 이유**
- **`find_node_types`와 `get_node_type_pins`의 type_id 표기가 다른 이유.** `SimpleMovetoActor` / `SimpleMoveToActor`
- **`CaptureViewport`가 PIE 화면이 아니라 에디터 월드를 렌더하는 것**
- **MCP로는 만들 수 없는 노드 목록.** `K2Node_CallParentFunction`, 순수 `IsValid`, `Use Cached Pose`
- **`UpperBody` 슬롯이 원래 있었는지 이번에 추가됐는지**
- **`Use cached pose 'BodyBase'`가 왜 `find_node_types`에 안 떴는지**
- **적이 제자리에서 공격할 때 다리가 멈추는 것이 티가 나는지**
- **`SaveCachedPose 'BodyBase'`의 `NOTE` 배지가 사라졌는지**
- **`ABP_Unarmed`의 `Is Falling` → `NOT` → `ShouldDoIKTrace` 배선이 무엇을 하는지**
- **`MM_ChargedAttack`이 어떤 동작인지**
- **막대의 긴 축 `Y`는 어느 방향인지**
- **재직렬화된 `.uasset`들의 내용이 실제로 안 바뀌었는지**
- **`Knife`의 `displayName` NSLOCTEXT 네임스페이스가 기존 행과 다른 이유**
- **`DisableInput`이 Enhanced Input 매핑까지 막는지**
- **HUD의 `CachedCharacter` 재획득이 실제로 일어나는지**
- **2번 방의 조명**
- **`bCanEverTick`이 명령 56 직후 `false`로 읽혔던 이유**
- **`trace_world`가 방향에 따라 같은 솔리드를 놓치는 이유**
- **`show navigation`이 PIE에서 안 먹는 이유**
- **`__ExternalObjects__` 파일의 정체.** `__ExternalActors__` 쪽은 이번에 답이 났다 — **액터 하나가 `.uasset` 하나이고, 레벨을 저장하면 맵 파일이 아니라 건드린 액터의 개별 파일만 바뀐다.** `__ExternalObjects__`는 아직 모른다
- **`Lvl_ArenaShooter`의 WorldSettings가 `BP_ShooterGameMode`를 가리키는지**

**접어둔 것**

- **적 HP·피격·사망.** 다음 사양의 본체다. 만들 때 **플레이어의 `PrintString`을 `ApplyDamage`로 올려야 적과 짝이 맞는다.** 그리고 **`ApplyDamage.DamageCauser`가 이미 `self`로 연결돼 있다** — 이번에 일부러 살렸다
- **적 공격에도 히트 판정 붙이기.** 지금은 `PlayAnimMontage → ApplyDamage → Delay`로 무조건 맞는다. 필요한 것 셋 — (1) `PlayAnimMontage`를 `Play Montage`로 교체, (2) `AM_Enemy_Attack`에 `Montage Notify` 찍기(수작업), (3) `ApplyDamage`를 노티파이 분기 뒤 트레이스 성공 쪽으로 옮기기
- **칼 메시 구하기.** 리타깃 비용이 애셋 고르는 기준에 들어가야 한다. 루트 모션이 켜져 있는지도 봐야 한다
- **칼 궤적 트레이스.** 밑동·칼끝 소켓 사이를 매 프레임 훑는 방식. `Play Montage`의 `OnNotifyEnd` 핀이 비어 있어 `Montage Notify Window`로 바꾸면 그대로 올라간다. 바꾸면 `EndLink.LinkValue`가 살아나므로 그 값도 같이 봐야 한다
- **카메라 작업.** 셋으로 갈렸다
  - **A — 원본 ICI 구조(`캡슐 → Camera → SkeletalMesh`)로 교체.** 팔만 있는 스켈레탈 메시가 프로젝트에 없어 지금 그대로는 못 한다
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
