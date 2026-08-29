# 2026-08-28

## 작업물

이전 프로젝트 **Project ICI**의 발표 자료를 전수 판독해 재설계 문서로 정리하고, 그 결론에 따라 UE 5.8에서 DataTable 기반 아이템 데이터 계층과 라인트레이스 습득을 만들었다.

**소요 시간**: 약 5시간 30분 (19:30 ~ 23:00 무렵. 앞의 2시간은 PDF 판독과 문서화, 뒤의 3시간 30분이 구현)

## 명령

### 한글

```
작업 준비
```

```
이제 그걸 할려면 우선 이 프로젝트의 근원이 되는 이전 프로젝트 관련 파일들을 지금부터 줄거야 일단 이 파일들을 보고 요약 분석을 해놓고 그 다음에 쓸 것들을 내가 하나씩 말하거나 작업하면 참고용으로 쓰자 어때
```

```
1. 파일은 여기에 줄거고 포트폴리오랑 발표 자료로 썻던 것들을 줄거야 ppt파일이나 시연 영상 링크같은것
2. mcp는 지금 열어야됨? 지금은 저 프로젝트 정리 및 재구성할건데
3. 요약은 문서 저장하는 폴더 내 폴더를 ProjectICI5.8 이런걸로 해서 만들고 거기에 넣자
4. 요약 목적은 이전 프로젝트에서의 기능과 구현 방식등을 재해석하고 실용적이게 다듬는 목적임 버전 5.8로 최신 업데이트 하고싶어서, 그리고 이전 프로젝트가 많이 많이 빈약해 이점을 좀 계속 마음에 두고 있었어서 이것들도 좀 바꿔볼려고
```

```
음 파일이 안올라가서 내가 pptx파일을 저 프로젝트요약용 폴더 안으로 옮겨줄까?
```

```
D:\20260827\MCP1\Docs\ProjectICI5.8 여기에 놨어
```

```
1. 인벤토리가 있잔아 그럼 그에 맞는 아이템을 구조화하고 설계해야지 아이템의 종류나 실제 아이템 배치 및 상호작용 등을 하고 나면 적 AI가 있어야지 적 AI가 생기면 전투시스템을 추가하는거야

2. 전수 판독고고

3. 우리가 요약한 요약프로젝트본을 커밋하자 어떤데
```

```
1. 열쇠, 회복포션, (손에 들 수있는 구체) 테스트용 공 같은걸로 실험할거야 나중에 더 추가하거나 확장에 용이할 수 있도록
2. 너가 권장하는 것으로 하고나서 나에게 요약 설명
```

```
1. A
```

```
2. A
3. A
```

```
프로젝트 켰어 일단 확인할것이 있나 검토 한번만
```

```
터미널에서 /mcp 를 치는거야?아님 여기서 치는거야
```

```
그대로가자 프로젝트 터미널에 쓸 첫번째 명령어
```

```
이거 글자 깨지는거 설정 하자 이거 계속이러네
```

```
A로하자
```

```
다음 명령을 할려면 일단 뭘 해야됨?
```

```
아이템 줍는 키를 F로 할까 F로하자
```

```
A
```

```
지금 현재 작업공간 효율이나 앞으로 얼마나 더 여기서 작업해도 되는지 자체 점검 해볼까
```

```
지금 하자
```

```
A하자
```

```
2. 이걸 뷰포트에 3개 끌어다 놓는게 아니라 복제를 먼저 해야되는거아니야? 확인해봐 나도 헷갈리는데 이게 안되는데
```

```
2. 이걸 뷰포트로 3개 끌어다 놓는게 뭔뜻이야 저게 안되는데 하나 끌어놓고 한번 더할려고 하면 없어지는데
```

```
디테일 패널이 어디에있어
```

```
이거 뷰포트에 지금 뭐뭐있는지 확인하는 패널은 어떻게 생성해
```

```
이게 평소 화면이거든 근데 너가 알려준 Outliner저거 Outliner 1에 체크가 되어있는데 Outliner 2 눌러보면 창이 뜨거든? 그거확인좀
```

```
고쳤어 이제 잘보인다 땡큐 이제 아이템 저거 디테일에서 해볼게 기다려봐
```

```
아이템 3개 추가했어 확인해봐
```

```
이거 아이템 두개 먹은 상태에서 세번째꺼 먹으면 슬롯1이라고 뜨는데 이거확인좀
```

```
이거 결과 보고있어봐 PIE하러갈게
```

```
응 잘나와
```

```
이 세션을 정리하려고해 일단 지금까지 기록할 것들 기록하고 진행상황과 다음 작업을 위한 인수인계 등을 총정리 하고 마무리 하는 작업을 가지자 이세션에서 고생했다
```

### English — MCP에 실제로 보낸 명령

사용자의 한글 지시는 "아이템을 구조화하고 설계해야지" 수준의 방향 제시였고, 아래 영어 명령은 그것을 사양으로 굳힌 뒤 옮긴 것이다. **애셋 이름·경로·필드 타입·기본값·노드 배선은 전부 옮기는 과정에서 AI가 정한 것이고 사용자가 말한 것이 아니다.** 무엇을 정했는지는 `분석` 칸과 `Docs/Spec/2026-08-28-인벤토리-1단계.md`에 적었다.

**명령 1 — enum (실패. 아래 `Terminal 결과` 참조)**

```
Create a new Blueprint Enumeration asset named E_ItemNature at /Game/Inventory/E_ItemNature.

It must have exactly three enumerators, in this order:
  1. Key
  2. Consumable
  3. Holdable

Set each enumerator's display name to the same text as its name (Key, Consumable, Holdable). Do not add a description to any of them.

Save the asset to disk. Then read the asset back and report, verbatim, the full list of enumerators it actually contains including their index numbers and display names, and report the asset's on-disk path and file size.
```

**명령 — 능력 확인 (명령 1이 튕긴 뒤)**

```
Do not create anything yet. This is a capability check only.

Report which unreal-mcp tool, if any, can create each of these three asset types, and what the tool's parameters would be:
  1. a Blueprint Enumeration (UserDefinedEnum)
  2. a Blueprint Structure (UserDefinedStruct)
  3. a Data Table (UDataTable) whose row struct is a UserDefinedStruct

For each one, if no tool can create it, say so plainly and quote the exact error or type restriction you hit. Also list the full set of asset_type values that the asset-creation tool accepts, verbatim.

Do not write commands for me to paste. Just answer.
```

**명령 — 손으로 만든 애셋 3개 읽어오기**

```
Read back three assets and report what they actually contain. Do not create or modify anything.

1. /Game/Inventory/E_ItemNature — list every enumerator with its index and display name, in order.
2. /Game/Inventory/S_ItemDef — list every member variable with its name and its exact type.
3. /Game/Inventory/DT_Items — report the row struct it points at, then list every row: the Row Name and the value of all five columns. For the Mesh column report the full object path, not just the asset name.

Report each value verbatim as the tool returns it. If a tool cannot read one of these, say which tool you tried and what it returned, and move on to the next one.
```

**명령 2 — 입력 액션 2개**

```
Create two Input Action assets in the folder /Game/Input/Actions, next to the existing IA_SelectSlot.

1. IA_Interact  — value type Digital (bool)
2. IA_UseItem   — value type Digital (bool)

Both are plain button actions: leave Triggers and Modifiers empty, and leave every other property at its default. Do not touch IA_SelectSlot, IMC_Default, IMC_Inventory, or any other asset.

Save both to disk. Then read each one back and report, verbatim, its value type and its full asset path, plus the on-disk file size of each. If the creation tool refuses either one, report the tool you called, the exact arguments, and the exact error, and stop without creating the other.
```

**명령 3 — `IMC_Inventory` 매핑 추가 (Step 3에서 멈춤. 손으로 처리)**

```
Modify the existing asset /Game/Input/IMC_Inventory. This asset already has three key mappings and they must all survive.

Step 1 — before changing anything, read and report the current Mappings array verbatim: every entry's key, its action, and its modifiers. There should be three entries mapping One, Two and Three to /Game/Input/Actions/IA_SelectSlot, each with a Scalar modifier.

Step 2 — check for key collisions before you add anything. Read /Game/Input/IMC_Default and report which keys it maps. Say explicitly whether the keys E or F are already bound to anything in IMC_Default. Do not modify IMC_Default either way.

Step 3 — append exactly two new mappings to IMC_Inventory, without removing or altering the existing three:
  - key F  ->  /Game/Input/Actions/IA_Interact
  - key E  ->  /Game/Input/Actions/IA_UseItem
Both new mappings get no triggers and no modifiers.

Step 4 — save IMC_Inventory to disk, then read the Mappings array back and report all five entries verbatim, in order, with each entry's key, action and modifiers.

If appending would require rewriting the whole array and you cannot guarantee the existing three survive, stop before Step 3 and tell me what the tool would do instead. Do not touch any asset other than IMC_Inventory.
```

**명령 — 손으로 넣은 매핑 검증**

```
Read /Game/Input/IMC_Inventory and report its defaultKeyMappings.mappings array verbatim: every entry's key, action, triggers and modifiers, in order.

Then read the three Scalar modifier subobjects it references and report each one's scalar value.

I am checking two things: that five mappings now exist (One, Two, Three, F, E), and that the three Scalar modifiers still read 1, 2 and 3 rather than all reading 1. Report both plainly. Do not modify anything.
```

**명령 4 — `BP_ItemPickup` 골격**

```
Create a new Blueprint class asset named BP_ItemPickup at /Game/Inventory/BP_ItemPickup, with /Script/Engine.Actor as its parent class.

Then set it up as follows:

1. Components. Add one StaticMeshComponent named Mesh and make it the root component. Do not add any other component. Leave its collision settings at their defaults.

2. Variable. Add one variable named ItemRow of type /Script/Engine.DataTableRowHandle. Make it instance editable (editable on placed instances in the level). Set its default value so that the handle's DataTable points at /Game/Inventory/DT_Items and its RowName is left empty.

Do not add any graph logic yet — no ConstructionScript nodes, no EventGraph nodes. That comes next.

Compile and save the Blueprint. Then read it back and report:
  - the parent class
  - every component, with its name, class, and which one is the root
  - every variable, with its name, exact type, whether it is instance editable, and its default value including the DataTable it points at
  - the on-disk file size

If any of these three things cannot be done with the available tools — creating the Blueprint, adding the component, or adding the variable — report which tool you called, the exact arguments, and the exact error, and stop there rather than working around it.
```

**명령 5 — ConstructionScript**

```
In the Blueprint /Game/Inventory/BP_ItemPickup, build the Construction Script so that a placed instance shows the mesh defined by its ItemRow.

The graph must be exactly this:

  Construction Script (entry)
    -> Get Data Table Row
         Data Table pin : the literal asset /Game/Inventory/DT_Items.DT_Items, set as the pin's default value. This pin must NOT be connected to anything.
         Row Name pin   : connected to the RowName output of a Break DataTableRowHandle node fed by the ItemRow variable.
         Row Found exec -> Set Static Mesh
                             Target   : the Mesh component
                             New Mesh : the "mesh" member of the Out Row, taken through a Break node for the S_ItemDef struct
         Row Not Found exec : leave unconnected

The Data Table pin being a literal is required, not a style choice: UK2Node_GetDataTableRow::GetDataTableRowStructType only resolves the Out Row struct type when that pin has a default object and no link. If you connect it, Out Row stays a wildcard and the node will not compile.

Compile and save the Blueprint. Then report:
  - every node in the Construction Script graph with its type and its pin connections
  - confirmation that the Out Row pin's struct type resolved to S_ItemDef and not a wildcard
  - the compile result, including any warnings
  - the on-disk file size

Use get_node_infos pin data to report the connections. Do not rely on read_graph_dsl for the exec chain — it has previously reported multi-exec node bodies as empty in this project even when they were fully wired.
```

**명령 6 — 캐릭터 변수 5개**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, add five new variables. Do not modify any existing variable, graph, component, or default value. Do not add any nodes.

1. InventorySlots — array of Name. Default value: exactly three elements, each one the empty name (None).
2. SelectedSlot   — Integer. Default 1.
3. HeldItemSlot   — Integer. Default 0.
4. CurrentHP      — Float. Default 75.0.
5. MaxHP          — Float. Default 100.0.

Leave all five at their default flags: not instance editable, not exposed on spawn, no replication, no category.

Compile and save the Blueprint. Then read it back and report:
  - the complete list of variables on this Blueprint, with each one's name, exact type, and default value
  - specifically, the element count and the value of every element of InventorySlots
  - the compile result including any warnings
  - the on-disk file size before and after

If setting a three-element default on the array is not possible with the available tools, report exactly which tool you called, the arguments, and what it returned, and leave the array at whatever default it has rather than adding graph nodes to fill it.
```

**명령 7 — 라인트레이스 (진단용)**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, add one variable and one new event chain in the EventGraph. Do not modify any existing node, variable, component, or default value.

Variable
  InteractDistance — Float, default 800.0, not instance editable.

New event chain in the EventGraph:

  EnhancedInputAction event for /Game/Input/Actions/IA_Interact, from its Triggered pin
    -> Line Trace By Channel
         Start            : Get Player Camera Manager (Player Index 0) -> Get Camera Location
         End              : Start + ( Get Player Camera Manager (0) -> Get Camera Rotation -> Get Forward Vector ) * InteractDistance
         Trace Channel    : Visibility
         Trace Complex    : false
         Ignore Self      : true
         Draw Debug Type  : For Duration
    -> Branch on the trace's Return Value
         True  -> Break Hit Result -> Hit Actor -> Cast To BP_ItemPickup
                    successful cast -> Break DataTableRowHandle on that actor's ItemRow variable
                                    -> Print String
                                         In String     : the RowName converted to a string
                                         Print to Screen: true
                                         Print to Log   : true
                                         Duration       : 3.0
                    Cast Failed     -> leave unconnected
         False -> leave unconnected

This is a diagnostic step. Nothing is picked up and nothing is destroyed. Draw Debug Type is deliberately visible so the trace line can be seen in PIE; it will be turned off in a later step.

Compile and save. Then report:
  - every node in this new chain with its pin connections, from get_node_infos
  - confirmation that no pre-existing node in the EventGraph was rewired
  - the compile result including warnings
  - the on-disk file size before and after
```

**명령 8 — 실제 습득**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, modify the IA_Interact chain that was built in the previous step. Do not touch any other event chain.

Change 1 — the event pin.
The chain is currently driven by the Triggered pin of the IA_Interact event node, which fires every frame while F is held. Disconnect it and drive the same Line Trace By Channel node from the Started pin instead, so one key press fires exactly one trace. Leave Triggered unconnected.

Change 2 — replace the diagnostic Print String with the real pickup logic.
After the successful Cast To BP_ItemPickup, build this:

  Cast succeeded
    -> Find (array Find on InventorySlots, Item to Find = the empty Name / None)
       This returns the index of the first empty slot, or -1 if there is none.
    -> Branch, condition = (Find result >= 0)
         True  -> Set Array Elem
                    Target Array : InventorySlots
                    Index        : the Find result
                    Item         : the RowName from Break DataTableRowHandle on the cast actor's ItemRow
                    Size to Fit  : false
                -> Print String
                     In String      : a string built as "PICKED <RowName> -> slot <Find result>"
                     Print to Screen: true, Print to Log: true, Duration: 3.0
                -> Destroy Actor, Target = the cast actor
         False -> Print String
                     In String      : "INVENTORY FULL"
                     Print to Screen: true, Print to Log: true, Duration: 3.0

Keep the existing Break DataTableRowHandle and the Get ItemRow variable node if they can be reused for the Item pin; delete the old ToString(Name) node and the old Print String node that only printed the row name.

Leave Draw Debug Type on the trace as ForDuration for now.

Compile and save. Then report every node in this chain with its pin connections from get_node_infos, confirm that the Triggered pin is now unconnected and Started drives the trace, confirm no other event chain was rewired, the compile result including warnings, and the on-disk file size before and after.
```

**명령 9 — `Find` 결과 고정 (버그 수정)**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, fix the IA_Interact pickup chain. Do not touch any other event chain.

The problem: the Array Find node is pure, so it is re-evaluated separately at each of its three consumers. The Branch and Set Array Elem read it before the write, but the Print's BuildString reads it after the write, so the printed index is wrong. Verified in the log: three consecutive pickups print slot 1, slot 2, slot -1 while actually writing to slots 0, 1, 2.

Add one variable:
  FoundSlotIndex — Integer, default -1, not instance editable.

Then rewire so the Find runs exactly once per press:

  Cast To BP_ItemPickup succeeded
    -> SET FoundSlotIndex = the return value of the existing Array Find node
       (Find keeps its current inputs: TargetArray = InventorySlots, ItemToFind = None)
    -> Branch, condition = ( Get FoundSlotIndex >= 0 )
         True  -> Set Array Elem   Index = Get FoundSlotIndex   (all other pins unchanged)
               -> Print String     the index now comes from Get FoundSlotIndex
               -> Destroy Actor    (unchanged)
         False -> Print String "INVENTORY FULL" (unchanged)

After the change, the Array Find node must have exactly one outgoing connection: into the SET FoundSlotIndex node. The >= node, the Set Array Elem Index pin, and the BuildString(Integer) InInt pin must all read from Get FoundSlotIndex nodes instead.

Compile and save. Then report every node in this chain with its pin connections from get_node_infos, confirm the Array Find node has exactly one outgoing edge, confirm no other event chain was rewired, the compile result including warnings, and the on-disk file size before and after.
```

**명령 10 — PlayerController 재배선 (작성했으나 이 세션에서 실행 안 함)**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController, extend the existing IA_SelectSlot chain so it also writes the selected slot onto the possessed pawn. Do not remove or rewire anything that already exists.

The chain today is:
  EnhancedInputAction IA_SelectSlot . Triggered
    -> Get HUD -> Cast To BP_ThirdPersonHUD -> SetSlot( NewSlot = Truncate(ActionValue) )

Change it to:
  EnhancedInputAction IA_SelectSlot . Triggered
    -> Sequence
         Then 0 -> the existing Get HUD / Cast To BP_ThirdPersonHUD / SetSlot chain, completely unchanged
         Then 1 -> Get Controlled Pawn
                -> Cast To BP_ThirdPersonCharacter
                     on success -> SET SelectedSlot on that character = the same Truncate(ActionValue) integer
                     Cast Failed -> leave unconnected

Reuse the existing Truncate node for both consumers rather than adding a second one.

The Sequence is there so the two branches are independent: if the HUD cast ever fails, the pawn must still receive the slot number.

Compile and save. Then report every node in this chain with its pin connections from get_node_infos, confirm the existing Get HUD / Cast / SetSlot nodes still carry exactly the connections they had before, the compile result including warnings, and the on-disk file size before and after.
```

또한 UE Terminal 세션의 시작 명령을 아래로 바꿨다. 이건 MCP 명령이 아니라 `Editor Preferences → General → Terminal → Startup Commands`의 세 번째 항목이다.

```
"C:\Users\a0108\.local\bin\claude.exe" --append-system-prompt "This session runs inside the Unreal Editor Terminal. Its font has no Hangul glyphs, so Korean text renders as empty boxes. Write every response in English only, even if the user writes to you in Korean. Do not output Korean characters. You are the executor, not a command writer: the project CLAUDE.md describes writing English commands for the user to paste into the UE Terminal, but you ARE that terminal. Carry out the instructions you are given directly, using the unreal-mcp tools. Never reply with a command for the user to paste. If a tool cannot do what was asked, say exactly which tool you tried and what it returned, and stop."
```

## Terminal 결과

### 원문 — English

터미널 출력 전체는 매우 길어 **판단 근거가 된 부분만 발췌했다.** 다만 실패·경고·어긋난 응답은 발췌하지 않고 전문을 넣었다. 원문 일부는 UE Terminal 폰트에 한글 글리프가 없어 화면이 깨진 채로 붙여진 것이라 문장 중간이 잘려 있다 — 그것도 다듬지 않고 그대로 뒀다.

**명령 1 실패 — enum 생성 불가**

```
- /Game/Inventory에 폴더 없음(MCP AssetTools.exists → false).
- unreal-mcp의 Enum 생성 툴 없음. BlueprintTools.create는 Blueprint 애셋만(asset_type은 UClass),
  AssetTools에도 해당 툴 없음
```

**능력 확인 — 전문**

```
Summary

| Asset type                                  | Tool that creates it                                     | Verdict                                              |
| 1. Blueprint Enumeration (UserDefinedEnum)  | none                                                     | Cannot be created                                    |
| 2. Blueprint Structure (UserDefinedStruct)  | none                                                     | Cannot be created                                    |
| 3. DataTable with a UserDefinedStruct row   | editor_toolset.toolsets.data_table.DataTableTools.create | Exists, but the row struct must already exist and    |
|    struct                                   |                                                          | must be passed by hand                               |

I did not call any create tool — you said not to create anything — so the restrictions below are quoted from the toolset
source on disk, not from a runtime error. Source root: C:\Program Files\Epic Games\UE_5.8\Engine\Plugins\Experimental\Toolsets\.

I enumerated every tool in all 18 registered toolsets. The only asset-creating tools are:

asset.AssetTools.create_folder
blueprint.BlueprintTools.create
curve_table.CurveTableTools.create
data_asset.DataAssetTools.create
data_table.DataTableTools.create  /  .import_file
material.MaterialTools.create_material / .create_function / .create_parameter_collection
material_instance.MaterialInstanceTools.create
string_table.StringTableTools.create
scene.SceneTools.create_level_instance

None of them produces a UUserDefinedEnum. Grepping the whole toolset Python package for
UserDefinedEnum, EnumFactory, StructureFactory returns zero hits.

The nearest candidate, BlueprintTools.create — blueprint.py:188-193:

assert unreal.MathLibrary.class_is_child_of(asset_type, unreal.Object.static_class()), (
    f'{asset_type} cannot be stored in a Blueprint.')
factory = unreal.BlueprintFactory()
factory.set_editor_property('parent_class', asset_type)
blueprint = create_asset(
    folder_path, asset_name, unreal.Blueprint.static_class(), factory)

The asset class is hardcoded as unreal.Blueprint; asset_type only sets the parent class of a Blueprint.
UUserDefinedEnum is not a UBlueprint, so this tool cannot make one regardless of what you pass.

No workaround via ProgrammaticToolset either — its sandbox whitelist (programmatic.py, _SUPPORTED_MODULES)
is json, math, datetime, copy, re, time. The unreal module is not importable there.

2. Blueprint Structure (UserDefinedStruct) — no tool

Same finding, same evidence. No tool creates a UUserDefinedStruct, and no tool edits one either
(there is no add-member / remove-member / set-member-type tool anywhere in the registry).

Note for later: AssetTools.duplicate could copy the existing
/Game/Variant_Shooter/Blueprints/Pickups/ST_WeaponTableRow, but since nothing can then edit the copy's
members, that gets you a struct with the wrong fields and no way to fix them over MCP.

3. DataTable with a UserDefinedStruct row struct — tool exists

The catch — the discovery tool won't find your struct. search_row_structs filters on TableRowBase
descendants only (data_table.py:29: unreal.ToolsetLibrary.get_derived_structs(unreal.TableRowBase.static_struct())).
A UserDefinedStruct has no super struct, so it never appears. Verified live in this project:

- AssetTools.find_assets for /Script/Engine.UserDefinedStruct → ["/Game/Variant_Shooter/Blueprints/Pickups/ST_WeaponTableRow"]
- DataTableTools.search_row_structs with "*WeaponTableRow*" → []

Also note find_assets for /Script/Engine.UserDefinedEnum over /Game → [].
The project currently has no Blueprint Enumerations at all.
```

**애셋 읽어오기 — enum 읽기 실패 전문**

```
No MCP tool in this server exposes an enum's enumerator list. What I tried:

- ObjectTools.list_properties on /Game/Inventory/E_ItemNature.E_ItemNature returned only:
{"enumDescription":{"type":"string","description":"Shows up in the content browser when the enum asset is hovered"}}
- ObjectTools.get_properties with ["Names","DisplayNameMap","enumDescription"] returned an error:
GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: Names, DisplayNameMap
- AssetTools.get_asset_tags on /Game/Inventory/E_ItemNature returned {}.
```

**구조체·DataTable 읽기 — 발췌**

```
{"displayName":{"type":"string"},"iconColor":{"type":"object","title":"LinearColor",...},
"mesh":{"type":"object","Mesh",...},"nature":{"type":"string","title":"E_ItemNature",
"enum":["Key","Consumable","Holdable"]},"healAmount":{"type":"number"}}

{"RowStruct":{"refPath":"/Game/Inventory/S_ItemDef.S_ItemDef"}}
DataTableTools.list_rows: ["Key_Stage1","Potion_Small","Ball_Test"]

"Key_Stage1": {"displayName": "NSLOCTEXT(...\"Rusty Key\")", "iconColor": {"R": 1, "G": 0.8, ...},
"mesh": "/Script/Engine.StaticMesh'/Engine/BasicShapes/Cube.Cube'", "nature": "Key", "healAmount": 0}
"Potion_Small": {... "mesh": "/Script/Engine.StaticMesh'/Engine/BasicShapes/Cylinder.Cylinder'",
"nature": "Consumable", "healAmount": 25}
"Ball_Test": {... "mesh": "/Script/Engine.StaticMesh'/Engine/BasicShapes/Sphere.Sphere'",
"nature": "Holdable", "healAmount": 0}
```

**명령 3 — Step 3에서 멈춤. 전문**

```
Step 3 — stopped, per your condition

Appending requires rewriting the whole array, and I cannot guarantee the existing three survive. Details:

The only write path to this property anywhere in the MCP server is ObjectTools.set_properties, whose contract is
"Sets the values of properties on an object… values: A JSON formatted string of the properties to set and their values."
It replaces a property's value wholesale. There is no array-element-set tool. I checked every toolset list_toolsets
reports (ObjectTools, AssetTools, BlueprintTools, DataAssetTools, DataTableTools, ActorTools, SceneTools, and the rest);
none has one, and grepping the full BlueprintTools tool dump found no array-element operation either.

So the call would be set_properties on IMC_Inventory with defaultKeyMappings set to a five-element array I construct —
the three existing entries retyped by me, plus two new ones. The existing three would not be preserved by the tool;
they would be re-sent by me, and whether they come back identical depends on how the tool deserializes them.
Two concrete reasons I can't promise that:

1. The instanced Scalar modifiers. Each mapping points at a subobject (IMC_Inventory:InputModifierScalar_0/1/2)
   carrying scalar 1 / 2 / 3. set_properties' own documentation says "For instanced sub-object properties, pass a
   class path as the instance member" — i.e. the documented way to set an instanced subobject is by class, which
   creates a fresh instance at defaults. Whether passing an existing subobject's refPath instead re-binds to that
   object or silently makes a new default-valued Scalar is not documented and I have not tested it. If it
   re-instantiates, all three become scalar (1,1,1) and slots 2 and 3 stop working — with no error, since the
   mapping array itself would still look correct.
2. The read format is not the write format. The read returns "key":"One" and "playerMappableKeySettings":"None"
   as bare strings, but list_properties declares key as an object and playerMappableKeySettings as an object
   {"refPath": string}. I do not know which shape set_properties accepts, so I cannot round-trip the existing
   entries verbatim.
```

**`IMC_Inventory`의 `Mappings`가 빈 배열인 것 — 전문**

```
First, a finding worth recording: mappings on this asset returns an empty array.
ObjectTools.get_properties with ["mappings"] returned verbatim:
{"mappings":[]}
The three real mappings live under defaultKeyMappings.mappings. ObjectTools.list_properties shows UE 5.8 exposes
both mappings and defaultKeyMappings (type InputMappingContextMappingData) on InputMappingContext.
Reading mappings alone would have made this asset look empty.
```

**명령 4 — `BlueprintTools.create`의 오해를 부르는 오류. 전문**

```
BlueprintTools.create — the asset_type argument is the parent class, not the Blueprint asset class, despite its
description reading "The specific kind of Blueprint to make". My first call:

create(folder_path="/Game/Inventory", asset_name="BP_ItemPickup",
       asset_type={"refPath": "/Script/Engine.Blueprint"})
→ error: Unable to create asset BP_ItemPickup at /Game/Inventory

Passing /Script/Engine.Actor instead succeeded. The error text gives no hint that the argument was the problem —
it reads like a filesystem or permissions failure.
```

**명령 5 — Out Row 타입 해소 확인. 발췌**

```
Resolved to S_ItemDef, not a wildcard. The node's own type_id reads Utilities|GetDataTableRowDT_Items
(it read Utilities|GetDataTableRowNONE with a Wildcard ReturnValue before the DataTable literal was set).
The DataTable input pin carries the asset path as its value with connected_pins: [], which is the condition
GetDataTableRowStructType needs.
```

**명령 6 — `add_variable`에 기본값 파라미터가 없다. 발췌**

```
add_variable has no default-value parameter — the only path to a default is writing the CDO through
ObjectTools.set_properties.

ObjectTools.set_properties(instance=/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.Default__BP_ThirdPersonCharacter_C,
values={"InventorySlots":["None","None","None"],"SelectedSlot":1,"HeldItemSlot":0,"CurrentHP":75.0,"MaxHP":100.0}) → returned true.

Type verification. list_properties reports inventorySlots as {"type":"array","items":{"type":"string"}} — the JSON
schema cannot distinguish Name from String. I confirmed it is Name by diffing the saved .uasset name table against
git show HEAD: of the same file: the pin-category FName name appears only in the new file, and string appears in neither.
```

**명령 7 — `TraceTypeQuery1` 검증. 발췌**

```
Trace channel confirmed: TraceTypeMapping is filled in ascending channel order with ECC_Visibility (3) before
ECC_Camera (4), so TraceTypeQuery1 = Visibility.

CollisionProfile.cpp:373-378 adds ECC_Visibility (3) to TraceTypeMapping before ECC_Camera (4) while iterating
channels in ascending order, and this project declares no custom collision channels in Config/DefaultEngine.ini,
so nothing shifts the index.
```

**명령 7 — `read_graph_dsl`을 안 쓴 이유. 전문**

```
I deliberately did not use write_graph_dsl. read_graph_dsl on this EventGraph returns a lossy script — it renders
EnhancedInputActionIA_Move with an empty body even though that event drives CallFunction_38. Writing that DSL back
would have destroyed existing wiring. Everything was built with create_node / connect_pins / set_pin_value instead.
```

**PIE 로그 — `Find` 재평가 버그의 증거. `Saved/Logs/MCP1.log` 발췌 (5회 실행분 중 3회)**

```
[2026.08.28-13.47.02:370][893]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Potion_Small -> slot 1
[2026.08.28-13.47.04:308][ 68]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Ball_Test -> slot 2
[2026.08.28-13.47.05:939][212]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Key_Stage1 -> slot -1
[2026.08.28-13.48.36:591][233]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Key_Stage1 -> slot 1
[2026.08.28-13.48.38:979][447]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Ball_Test -> slot 2
[2026.08.28-13.48.41:116][641]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Potion_Small -> slot -1
[2026.08.28-13.49.28:705][323]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Ball_Test -> slot 1
[2026.08.28-13.49.30:938][524]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Potion_Small -> slot 2
[2026.08.28-13.49.32:897][700]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Key_Stage1 -> slot -1
```

**명령 9 — 승격 연산자의 리터럴이 조용히 지워진 것. 전문**

```
One thing worth recording

Breaking the connection into GreaterEqual.A silently cleared the literal on the other input, B — it went from '0'
to ''. The compile with warnings_as_errors=true passed it. I caught it only because I re-read every input pin
after the rewire, and set it back to '0' explicitly. If you rewire a promotable operator elsewhere, its
unconnected literals are worth re-reading rather than assuming they survived.
```

**명령 9 — `Find`의 나가는 간선 3개 → 1개. 전문**

```
find_edges_before: ["ReturnValue -> K2Node_PromotableOperator_5",
                    "ReturnValue -> K2Node_CallArrayFunction_3",
                    "ReturnValue -> K2Node_CallFunction_33"]
find_edges_after:  ["ReturnValue -> K2Node_VariableSet_1"]
```

**수정 후 PIE 로그. 전문**

```
[2026.08.28-13.54.49:324][598]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Ball_Test -> slot 0
[2026.08.28-13.54.50:639][715]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Potion_Small -> slot 1
[2026.08.28-13.54.51:886][827]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PICKED Key_Stage1 -> slot 2
```

**남은 불일치 — 곱하기 노드의 라벨과 핀 타입이 어긋난다. 전문**

```
The multiply node reports type_id as Math|Vector|vector*vector, not a vector×float operator. Its actual pins are
A: Vector, B: Float (double-precision), ReturnValue: Vector, with InteractDistance connected straight to B and no
conversion node inserted. So the resolved signature is vector × scalar, which is the intended math — but the
reported type_id label and the resolved pin types disagree, and I could not determine from the tools which of the
two the compiler actually bound. I am reporting the pin types as the evidence, not the label.
```

### 요약 — 한글

**애셋 — 손으로 만든 것 3개**

`unreal-mcp`가 만들 수 없어 콘텐츠 브라우저에서 직접 만들었다.

- `/Game/Inventory/E_ItemNature` — `UserDefinedEnum`. 열거자 `Key` / `Consumable` / `Holdable`
- `/Game/Inventory/S_ItemDef` — `UserDefinedStruct`. 필드 `displayName`(Text) · `iconColor`(LinearColor) · `mesh`(StaticMesh) · `nature`(`E_ItemNature`) · `healAmount`(float)
- `/Game/Inventory/DT_Items` — `UDataTable`, 행 구조체 `S_ItemDef`. 행 `Key_Stage1` · `Potion_Small` · `Ball_Test`

세 애셋 모두 처음엔 기본 이름(`NewUserDefinedEnumeration` 등)으로 저장돼 있었고, 디스크를 읽어 확인한 뒤 `F2`로 고쳤다.

**애셋 — MCP가 만든 것 3개**

- `/Game/Input/Actions/IA_Interact` — `InputAction`, `valueType: Boolean` (1,174 B)
- `/Game/Input/Actions/IA_UseItem` — `InputAction`, `valueType: Boolean` (1,169 B)
- `/Game/Inventory/BP_ItemPickup` — `Actor` 상속. `StaticMeshComponent` `Mesh`가 루트. 변수 `ItemRow`(`DataTableRowHandle`, 기본 DataTable `DT_Items`)

**애셋 — 손으로 고친 것 1개**

- `/Game/Input/IMC_Inventory` — 매핑 2개 추가 (`F` → `IA_Interact`, `E` → `IA_UseItem`). 3,604 → 4,516 B

**그래프**

- `BP_ItemPickup.UserConstructionScript` — 7노드. `Get Data Table Row`(DataTable 핀은 리터럴 `DT_Items`, RowName은 `Break DataTableRowHandle`에서) → `Row Found` → `Set Static Mesh`
- `BP_ThirdPersonCharacter.EventGraph` — `IA_Interact` 체인 30노드. `Started` → `Line Trace By Channel` → `Cast To BP_ItemPickup` → `SET FoundSlotIndex` → `Branch` → `Set Array Elem` / `Print String` / `Destroy Actor`

**변수 — `BP_ThirdPersonCharacter`에 7개 추가**

`InventorySlots`(Name 배열 `["None","None","None"]`) · `SelectedSlot`(1) · `HeldItemSlot`(0) · `CurrentHP`(75) · `MaxHP`(100) · `InteractDistance`(800) · `FoundSlotIndex`(-1)

**레벨 — `Lvl_ThirdPerson`**

`BP_ItemPickup` 인스턴스 3개. 각 인스턴스의 `ItemRow.RowName`이 `Key_Stage1` / `Potion_Small` / `Ball_Test`로 서로 다르다.

**문서**

- `Docs/ProjectICI5.8/` — README + 6개 분석 문서 + 재설계 우선순위. 원본 PDF는 `.gitignore`로 제외
- `Docs/Spec/2026-08-28-인벤토리-1단계.md` — 1단계 사양

**설정**

- `Editor Preferences → General → Terminal → Startup Commands`의 Claude 실행 줄에 `--append-system-prompt` 추가

## 분석

### 무엇을 만들었나

**1. 이전 프로젝트 분석 — `Docs/ProjectICI5.8/`**

`Project ICI 게임 소개 PDF.pdf` 85페이지를 전수 판독했다. `Read` 도구의 PDF 렌더링이 `pdftoppm`(poppler) 부재로 실패해서 두 가지로 우회했다.

- 텍스트: Git for Windows 동봉 `pdftotext -layout -enc UTF-8`
- 이미지: poppler의 `pdfimages`도 없어서 **의존성 없는 추출 스크립트를 직접 작성**. UE 5.8 동봉 Python 3.11(`Engine/Binaries/ThirdParty/Python3/Win64/python.exe`)로 실행. PDF의 간접 객체와 객체 스트림(`ObjStm`)을 풀어 페이지 트리를 걷고, 각 페이지의 `/Resources → /XObject`에서 이미지 스트림을 꺼내 `DCTDecode`는 `.jpg` 그대로, `FlateDecode`는 PNG로 다시 감쌌다

238장 추출 → 중복(템플릿 배경·로고) 제거 후 100장 → 실질 스크린샷 70장을 전부 판독했다. 블루프린트 노드 이름과 핀 값까지 읽혔다.

문서 8개. 각 문서는 `자료에 있는 것`(확인된 사실)과 `다시 만들면`(AI 의견)을 분리했다.

**2. 사양 — `Docs/Spec/2026-08-28-인벤토리-1단계.md`**

범위 · 상태 · 규칙 · 권한 · 수명 · 튜닝 값의 주인 · 합격 기준 4개 · AI가 정한 것 13개 · 진행 상황 표 · `unreal-mcp` 경계선.

합격 기준 4개는 이렇다.

> 1. PIE에서 바닥에 놓인 공을 조준하고 `F`를 누르면, 선택된 슬롯이 파란색으로 채워지고 바닥의 공이 사라진다.
> 2. PIE에서 세 칸을 열쇠·포션·공으로 채운 뒤 `1`/`2`/`3`을 누르면, 세 칸이 각각 노랑·빨강·파랑으로 남은 채 선택된 칸의 테두리만 초록으로 바뀐다.
> 3. PIE에서 포션이 든 칸을 선택하고 `E`를 누르면, HP 바가 75%에서 100%로 늘고 그 칸이 빈칸(테두리만)으로 돌아간다.
> 4. PIE에서 빈 칸을 선택하고 `E`를 누르면 아무 일도 일어나지 않고 에러 로그도 없다.

**3. 데이터 계층**

`E_ItemNature`(enum 3값) → `S_ItemDef`(구조체 5필드) → `DT_Items`(DataTable 3행). 행 값은 다음과 같다.

| Row Name | displayName | iconColor (R,G,B,A) | mesh | nature | healAmount |
|---|---|---|---|---|---|
| `Key_Stage1` | `Rusty Key` | 1 / 0.8 / 0.1 / 1 | `/Engine/BasicShapes/Cube.Cube` | `Key` | 0 |
| `Potion_Small` | `Small Potion` | 0.9 / 0.1 / 0.1 / 1 | `/Engine/BasicShapes/Cylinder.Cylinder` | `Consumable` | 25 |
| `Ball_Test` | `Test Ball` | 0.2 / 0.4 / 1 / 1 | `/Engine/BasicShapes/Sphere.Sphere` | `Holdable` | 0 |

**4. 입력**

| 애셋 | 값 타입 | 키 | 컨텍스트 |
|---|---|---|---|
| `IA_SelectSlot`(기존) | Axis1D | `1` `2` `3` | `IMC_Inventory`, 스칼라 모디파이어 1/2/3 |
| `IA_Interact`(신규) | Digital(bool) | `F` | `IMC_Inventory`, 트리거·모디파이어 없음 |
| `IA_UseItem`(신규) | Digital(bool) | `E` | `IMC_Inventory`, 트리거·모디파이어 없음 |

`IMC_Default`는 건드리지 않았다. 그쪽 매핑 13개는 `SpaceBar`·`Gamepad_FaceButton_Bottom`(`IA_Jump`), `W`/`S`/`A`/`D`/`Up`/`Down`/`Right`/`Left`/`Gamepad_Left2D`(`IA_Move`), `Gamepad_Right2D`(`IA_Look`), `V`(`IA_SwitchCamera`)다. `E`·`F`와 겹치지 않는다.

**5. `BP_ItemPickup`**

- 컴포넌트 `Mesh`(StaticMeshComponent) 하나뿐. 루트다. `create`가 만든 `DefaultSceneRoot`는 `Mesh`가 루트로 승격되면서 자동 제거됐다
- 변수 `ItemRow` — `DataTableRowHandle`, 기본값 `{"dataTable":{"refPath":"/Game/Inventory/DT_Items.DT_Items"},"rowName":"None"}`
- ConstructionScript 7노드

**6. `BP_ThirdPersonCharacter`**

변수 7개, `IA_Interact` 체인 30노드. 사거리 `InteractDistance = 800`.

**7. 레벨 배치**

`BP_ItemPickup` 3개. 액터 파일 세 개가 `Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/` 아래 `7/6I/`, `B/UL/`, `D/DP/`에 생겼다.

### 기술적으로 맞게 짚은 부분

**`Get Data Table Row`의 DataTable 핀을 리터럴로 둔 것.** 이건 스타일이 아니라 필수다. `UK2Node_GetDataTableRow::GetDataTableRowStructType`(`K2Node_GetDataTableRow.cpp:145`)이 `DataTablePin->DefaultObject != nullptr && DataTablePin->LinkedTo.Num() == 0`일 때만 행 구조체를 알아낸다. 선을 연결하면 `Out Row`가 와일드카드로 남아 컴파일이 안 된다. 명령을 쓰기 전에 엔진 소스에서 확인했고, 터미널이 노드 `type_id`가 `GetDataTableRowNONE` → `GetDataTableRowDT_Items`로 바뀐 것을 근거로 보고했다.

**`TraceTypeQuery1`이 `Visibility`인지 배선 전에 확인한 것.** 터미널이 먼저 짚었고 별도로 재확인했다. 프로젝트에 커스텀 콜리전 채널이 선언돼 있으면 인덱스가 밀려 `TraceTypeQuery1`이 다른 채널이 된다. `Config/DefaultEngine.ini`에 `DefaultChannelResponses` 선언이 없고, `CollisionProfile.cpp:373-377`이 채널을 오름차순으로 돌며 `ECC_Visibility`(3)를 `ECC_Camera`(4)보다 먼저 `TraceTypeMapping`에 넣는다. 그래서 `TraceTypeQuery1` = `Visibility`다.

**`IMC_Inventory` 매핑을 MCP로 안 쓰고 손으로 넣은 것.** 터미널이 Step 3에서 멈춘 판단이 맞다. `ObjectTools.set_properties`는 배열을 통째로 교체하고, 각 매핑이 가리키는 `InputModifierScalar_0/1/2`는 인스턴스 서브오브젝트다. 문서상 인스턴스 서브오브젝트는 클래스 경로로 넘기게 돼 있어 **기본값짜리 새 인스턴스가 만들어질 수 있다.** 그러면 스칼라가 셋 다 `(1,1,1)`이 되어 슬롯 2·3번이 죽는데, **매핑 배열 자체는 멀쩡해 보이고 에러도 안 난다.** 실패가 조용한 쪽을 피한 것이다.

**`write_graph_dsl`을 안 쓴 것.** 2026-08-28 오전 기록에 `read_graph_dsl`이 이 EventGraph의 멀티 exec 노드 본문을 빈 것으로 내놓는다는 관찰이 이미 있었다. 터미널이 그걸 독립적으로 재확인하고(`EnhancedInputActionIA_Move`가 본문 없이 나오는데 실제로는 `CallFunction_38`을 구동한다) `create_node` / `connect_pins` / `set_pin_value`로만 작업했다. **DSL을 되써넣었으면 기존 배선이 날아갔다.**

**`Get Player Camera Manager`를 쓴 것.** 이 캐릭터는 1인칭/3인칭을 전환한다(`bIsFirstPerson`). 카메라 컴포넌트를 직접 참조하면 어느 쪽이 켜져 있는지에 따라 갈리고 컴포넌트 이름에도 묶인다. 카메라 매니저는 **지금 보고 있는 시점**을 준다.

**사거리를 300에서 800으로 바꾼 것.** 원본 Project ICI의 라인트레이스 사거리가 300이고 사양에도 그렇게 적었지만, **원본은 1인칭이고 여기는 3인칭이다.** 카메라가 스프링암 끝 캐릭터 뒤 약 400 지점에 있어서 300이면 캐릭터에도 못 닿는다. PIE에서 디버그 선이 캐릭터를 지나 앞으로 뻗는 것으로 확인됐다.

**빈 칸 찾기를 `Find` 노드 하나로 한 것.** `Find(InventorySlots, 'None')`이 첫 번째 빈 칸의 인덱스를 주고 없으면 `-1`이다. 사양의 "빈 칸 중 가장 앞"과 "가득 차면 안 줍는다"가 노드 하나로 동시에 처리된다. `ForEachLoop`으로 도는 것보다 싸다.

**상호작용 인터페이스를 안 만든 것.** 처음 계획에는 `BPI_Interactable`이 있었는데 뺐다. 지금 상호작용 대상이 아이템 하나뿐이다. CLAUDE.md의 결정 사다리 — *"지금 하나뿐인데 인터페이스를 파거나 컴포넌트로 분리하지 않는다. 두 번째가 실제로 생겼을 때 그때 뽑는다."* 덤으로 위험도 줄었다. `BlueprintTools.create`가 `BlueprintFactory`를 하드코딩해 쓰므로 `BlueprintInterfaceFactory`가 필요한 인터페이스는 **아마 못 만들었을 것이다.**

**Pickup에 콜리전 컴포넌트를 따로 안 단 것.** 라인트레이스가 `Visibility` 채널로 쏘니 스태틱 메시가 그대로 판정 대상이 된다. 원본이 아이템에 별도 `Collision` 구를 단 것은 오버랩 방식이었기 때문이다.

**`ItemRow`를 `DataTableRowHandle`로 한 것.** 디테일 패널에서 드롭다운으로 행을 고른다. 원본 Project ICI는 아이템 식별을 `Item_Name`(Name) 문자열 비교로 했고, 문의 `KeyID`와 오타 하나만 달라도 컴파일 에러 없이 조용히 안 열렸다. 핸들은 그 실패 경로 자체를 없앤다.

**`Started` 핀으로 바꾼 것.** 처음에 `Triggered`로 지정한 것은 AI의 실수다. `Triggered`는 키를 누르고 있는 동안 매 프레임 발동한다. 진단 단계에서 한 번 눌렀는데 `Key_Stage1`이 11줄 찍힌 것으로 드러났다. 습득 로직을 붙였으면 매 프레임 줍기를 시도했을 것이다. 원본 Project ICI도 `ICI_Interaction`에 `Started`를 썼다.

**라인트레이스와 습득을 두 명령으로 쪼갠 것.** 조준이 실제로 맞는지부터 확인하고 인벤토리 로직을 붙였다. 한 번에 만들었으면 안 될 때 원인이 두 군데가 된다.

**`Find`의 재평가 버그를 로그로 잡은 것.** 사용자가 "세번째꺼 먹으면 슬롯1이라고 뜬다"고 했을 때 고쳐보고 돌려보는 대신 `Saved/Logs/MCP1.log`를 직접 읽었다. 5회 실행에서 `slot 1 → 2 → -1` 패턴이 완전히 동일했고, **세 번째가 `-1`인데도 `INVENTORY FULL`이 아니라 `PICKED`로 찍혔다**는 것이 결정적이었다. `Branch`가 본 값과 `Print`가 본 값이 다르다는 뜻이고, 그건 pure 노드가 소비처마다 따로 평가된다는 것이다.

**손대지 않은 것 — `IA_SelectSlot`의 `Triggered`.** 이것도 매 프레임 발동하지만 하는 일이 정수 대입이라 몇 번을 해도 결과가 같다. `Started`로 바꾸면 깔끔하지만 지금 잘 되는 슬롯 선택을 건드리는 위험이 그 이득보다 크다고 판단해 그대로 뒀다.

**손대지 않은 것 — 원본의 튜닝 값.** `FirstPersonPitchMin/Max = -60/60`, `ThirdPersonPitchMin/Max = ∓89.9`가 읽혀 나왔지만 건드리지 않았다.

### 확인한 것 / 확인 못 한 것

**확인한 것** — PIE 또는 디스크에서 실제로 본 것만이다.

- 레벨의 `BP_ItemPickup` 인스턴스 3개가 서로 다른 `ItemRow.RowName`을 든다. 액터 `.uasset` 세 개를 열어 `Key_Stage1` / `Potion_Small` / `Ball_Test` 문자열을 각각 확인했다. **이것으로 `ItemRow`의 Instance Editable이 실제로 걸려 있음이 확인됐다** — 안 걸렸으면 셋 다 `None`이었다
- ConstructionScript가 작동한다. 사용자가 디테일 패널에서 `Row Name`을 고르는 순간 뷰포트에 메시가 나타났고, PIE 화면에 큐브와 실린더가 보인다
- 라인트레이스가 조준한 곳으로 간다. `InteractDistance = 800`으로 디버그 선이 캐릭터를 지나 앞으로 뻗는다
- 히트 → 캐스팅 → 행 이름 읽기가 된다. 화면과 로그에 `Key_Stage1` 등이 찍혔다
- `Started` 배선이 맞다. 한 번 누를 때 한 줄씩만 찍힌다
- **습득이 사양대로 작동한다.** `MCP1.log` 13:54:49~51에 `PICKED Ball_Test -> slot 0`, `PICKED Potion_Small -> slot 1`, `PICKED Key_Stage1 -> slot 2`. 빈 칸 중 가장 앞부터 찬다
- `Set Array Elem`이 변수 게터를 통해 멤버 배열에 실제로 쓴다. 인덱스가 0 → 1 → 2로 올라간 것이 증거다
- 습득한 아이템이 월드에서 사라진다
- `IMC_Inventory`에 매핑 5개가 있고 `Scalar` 모디파이어 셋이 1 / 2 / 3 그대로다
- 애셋 파일 크기와 `git status`가 매 단계 보고와 일치한다. `BP_ThirdPersonCharacter`는 254,218 → 259,104 → 324,210 → 350,440 → 360,677 B로 단계마다 늘었다
- 터미널 세션이 영어로 답하고, 명령문을 작성하는 대신 실행한다

**확인 못 한 것** — 이유까지 적는다.

- **`E_ItemNature`의 열거자 인덱스가 0/1/2인지.** `unreal-mcp`에 enum을 읽는 툴이 없다. 이름 순서는 `S_ItemDef`의 JSON 스키마에 `["Key","Consumable","Holdable"]`로 딸려 나온 것이 유일한 근거이고, 인덱스는 어떤 툴도 반환하지 않았다. `Switch on E_ItemNature` 노드를 만들 때 핀 순서로 드러난다
- **`INVENTORY FULL` 경로.** 레벨에 아이템이 3개뿐이고 칸도 3개라 딱 맞게 찬다. 넷째를 조준할 대상이 없어 `else` 가지가 한 번도 실행되지 않았다
- **합격 기준 4개 중 어느 것도 통과하지 못했다.** 1번은 "슬롯이 파란색으로 채워진다"를 요구하는데 HUD가 아직 색을 안 칠한다. 2·3·4번은 사용(`E`) 로직과 HP 바가 없어 시작도 못 한다. **지금 확인된 것은 "아이템이 배열에 들어가고 월드에서 사라진다"까지다**
- **캐릭터 변수 7개의 플래그**(replication / instance editable / category). `add_variable`이 만든 기본값일 것으로 추정하지만 읽는 툴을 부르지 않았다. 추론이지 읽어온 값이 아니다
- **`BP_ItemPickup.ItemRow`의 Instance Editable 플래그 자체를 읽은 것은 아니다.** 레벨 인스턴스가 서로 다른 행을 든다는 사실에서 역으로 확인했다
- **곱하기 노드가 어느 오버로드로 바인딩됐는지.** `type_id`는 `Math|Vector|vector*vector`인데 핀은 Vector × double이다. 변환 노드가 없고 컴파일이 깨끗하므로 `vector × float`로 풀린 것으로 보이지만, 툴로는 확정할 수 없었다
- **명령 10(PlayerController 재배선)은 작성만 하고 실행하지 않았다.** 세션이 여기서 끝났다

### 남는 리스크

- **임시 코드가 그래프에 남아 있다.** `Print String` 3개(`PICKED …`, `INVENTORY FULL`, 그리고 습득 성공 로그), 라인트레이스의 `Draw Debug Type: ForDuration`. 셋 다 의도적으로 켜둔 것이고 HUD가 슬롯 색을 칠하기 시작하면 지운다. **지금 이대로 두면 배포본에 디버그 선과 로그가 남는다** — 원본 Project ICI에서 지적했던 바로 그 문제다
- **off-by-one이 잠복해 있다.** `InventorySlots`는 0부터, `SelectedSlot`은 1부터다. `IA_SelectSlot`의 스칼라 모디파이어가 1/2/3을 실어 나르기 때문에 입력 쪽이 1-based로 고정돼 있다. 사용(`E`) 로직에서 `InventorySlots[SelectedSlot - 1]`을 써야 하고, **변환 지점을 그 한 곳으로 못 박지 않으면 반드시 어긋난다**
- **`SelectedSlot`이 두 군데에 있다.** `BP_ThirdPersonHUD.SelectedSlot`(그리기용, 현재 유일하게 갱신되는 것)과 `BP_ThirdPersonCharacter.SelectedSlot`(아직 아무도 안 건드림). 이 상태로 오래 두면 원본 Project ICI의 Skeleton이 `Current HP`와 `Current Health`를 따로 굴리던 것과 같은 문제가 된다. HUD 단계에서 하나로 합쳐야 한다
- **승격 연산자를 재배선하면 안 건드린 리터럴이 조용히 지워진다.** `GreaterEqual.A`의 연결을 끊었더니 `B`가 `'0'`에서 빈 값이 됐고 `warnings_as_errors=true` 컴파일이 통과시켰다. 이번엔 빈 int가 0으로 해석돼 결과가 같았지만, 0이 아닌 값이나 float였으면 조용히 바뀌었을 것이다
- **`FoundSlotIndex`가 멤버 변수다.** 한 번 쓰고 버리는 값인데 클래스에 남는다. EventGraph에는 로컬 변수가 없어서 값을 붙들 자리가 멤버뿐이었다. 습득을 함수로 빼면 로컬 변수를 쓸 수 있지만, 지금 요구사항이 그걸 정당화하지 않는다
- **`Find` 노드가 pure라는 사실이 다른 곳에서도 물린다.** 이번엔 `Find`였지만, 배열을 변경하는 exec 흐름 안에서 그 배열을 읽는 pure 노드를 여러 곳에 물리면 같은 일이 다시 일어난다
- **`unreal-mcp`가 만들지도 읽지도 못하는 애셋 종류가 있다.** enum과 구조체는 손으로만 만들 수 있고 편집도 안 된다. **앞으로 enum 값이나 구조체 필드를 늘릴 때마다 손으로 해야 한다**
- **`--append-system-prompt`가 터미널 창의 시작 명령에만 있다.** `Editor Preferences`의 사용자별 설정이라 저장소에 안 들어간다. 다른 PC나 에디터 설정 초기화 후에는 터미널 에이전트가 다시 명령문을 작성하고 한글로 답한다
- **터미널 출력 원문이 화면 폭에 잘려 붙여진다.** 이 기록의 `Terminal 결과` 칸에도 문장 중간이 끊긴 부분이 있다. 표가 든 출력일수록 심하다
- **`displayName`이 영어다.** MCP가 읽어 터미널에 뱉을 때 한글이 네모가 되는 것을 피하려고 정한 것인데, 게임 화면에 뜨는 이름이라 나중에 한글로 바꿔야 한다

### 총평

요청은 두 겹이었다. 하나는 "이전 프로젝트를 판독해 재해석"이고, 다른 하나는 그 결론에 따라 "인벤토리부터 다시 만들기"다. 첫째는 끝났고, 둘째는 데이터 계층과 습득까지 왔다. **합격 기준 4개 중 통과한 것은 없다** — HUD 표시와 사용 로직이 남았기 때문이다.

이 작업의 실질적 난이도는 블루프린트가 아니라 **`unreal-mcp`의 경계선을 찾는 것**이었다. 시간의 절반이 "이 툴로 이게 되나"를 확인하는 데 들어갔다. enum·구조체는 만들 수도 읽을 수도 없고, 배열에 원소를 덧붙이는 툴이 없고, `BlueprintTools.create`의 인자는 이름과 다른 것을 받고, `InputMappingContext`의 데이터는 이름이 비슷한 다른 프로퍼티에 들어 있다. 이것들은 전부 **응답만 보고는 알 수 없고 소스를 읽어야 나온다.**

판독 쪽의 난이도는 도구가 없다는 것이었다. `Read`가 PDF를 못 열어서 PDF 객체 스트림을 직접 파싱하는 스크립트를 썼다. 결과적으로 이게 이번 세션에서 가장 값이 컸다 — 70장의 블루프린트 스크린샷을 읽지 못했으면 "아이템이 열쇠 하나뿐이라 인벤토리가 존재할 이유가 없었다"는 결론에 못 갔고, 그러면 지금 만든 DataTable 구조도 나오지 않았다.

버그 하나를 만났고 로그로 잡았다. 고쳐보고 돌려보는 것을 반복하지 않았다는 점에서 CLAUDE.md의 절차가 실제로 작동했다.

AI의 실수가 셋 있었다. `Triggered`를 `Started` 대신 지정한 것, 사거리 300을 3인칭에 그대로 적용하려 한 것, 그리고 커밋 메시지에 "그래프 없음"이라 적었는데 그 커밋에 그래프가 들어 있던 것이다. 셋 다 잡혔지만 첫째와 셋째는 사용자가 아니라 검증 과정에서 걸린 것이고, 둘째는 명령을 쓰기 직전에 스스로 알아챈 것이다.

## AI의 제안

**1. `Docs/Spec/` 폴더를 새로 만들 것**

> `Docs/Spec/2026-08-28-인벤토리-1단계.md` — `Docs/ProjectICI5.8/`는 과거 분석, `Docs/AI-Log/`는 세션 기록 양식이 따로 있다. 사양은 둘 다 아니다.

사양이 채팅에만 있으면 세션이 끊길 때 사라진다. 폴더가 하나 늘어나는 대신 사양의 자리가 생긴다.

**2. 상호작용 인터페이스를 만들지 말 것**

> **상호작용 인터페이스(`BPI_...`)를 만들지 않는다.** 지금 상호작용 대상이 아이템 하나뿐이다. 라인트레이스가 `BP_ItemPickup`으로 직접 캐스팅한다. **문이 생기는 순간 그때 인터페이스를 뽑는다**

원래 계획(명령 4에 `BPI_Interactable`을 포함)을 스스로 철회한 것이다. 지금은 캐스팅 하나로 끝나 단순하지만, 두 번째 상호작용 대상이 생기면 그때 리팩터링이 필요하다.

**3. 아이콘을 텍스처가 아니라 색으로 할 것**

> **아이콘을 텍스처가 아니라 색으로 한다.** 프로젝트에 쓸 수 있는 텍스처가 없고(`StarterContent` 미설치), HUD가 `DrawRect` 캔버스라 색이 그대로 맞는다. 진짜 아이콘이 생기면 `DrawTexture`로 바꾸고 행에 `icon` 필드를 더한다

애셋을 하나도 안 만들고 시작할 수 있고 현재 HUD 구현과도 맞는다. 대신 아이템이 늘어나면 색으로 구분하는 데 한계가 온다.

**4. 라인트레이스와 습득을 두 명령으로 쪼갤 것**

> **습득 로직을 바로 만들지 않는다.** 조준이 실제로 아이템에 맞는지부터 확인한다. 여기서 안 맞으면 인벤토리 로직을 아무리 잘 짜도 안 되고, 그때 원인이 두 군데가 된다.

왕복이 한 번 늘어나는 대신 실패 원인이 하나로 좁혀진다. 실제로 이 덕분에 사거리 문제와 `Triggered` 문제가 습득 로직과 섞이지 않고 드러났다.

**5. 터미널 폰트 대신 출력 언어를 고정할 것**

> `"C:\Users\a0108\.local\bin\claude.exe" --append-system-prompt "This session runs inside the Unreal Editor Terminal. Its font has no Hangul glyphs, so Korean text renders as empty boxes. Write every response in English only, even if the user writes to you in Korean. Do not output Korean characters. You are the executor, not a command writer: ..."`

환경변수(`CLAUDE_UE_TERMINAL`) 안보다 낫다 — 그 안은 변수를 읽어줄 규칙을 `CLAUDE.md`에 또 써야 해서 두 군데를 건드린다. 이건 한 군데다. 대신 `Editor Preferences`는 저장소에 안 들어가서 다른 환경에서는 다시 해야 한다.

**6. 커밋 메시지가 틀린 것을 히스토리 재작성으로 고칠 것**

> **A. 두 커밋을 다시 쓴다 (권장)** — `git reset --soft HEAD~2` 후 메시지를 바로잡아 다시 커밋한다. 히스토리가 깨끗해진다

`origin/main`보다 앞서 있고 push 안 된 상태였다. 이 프로젝트에서 커밋은 "무엇을 건드렸는가"의 증거로 쓰이므로 증거가 틀린 채 남으면 나중에 그걸 믿고 판단하게 된다. 대신 히스토리를 다시 쓰는 것 자체가 되돌리기 어려운 조작이다.

**7. `Find` 결과를 멤버 변수로 고정할 것**

> 지금 `Branch`와 `SetArrayElem`이 우연히 같은 값을 보는 건 **그 사이에 배열이 안 바뀌기 때문일 뿐이다.** 같은 계산을 세 번 하고 그중 하나가 변경 후에 일어나는 구조 자체가 문제다.

출력 숫자만 틀린 상태라 "동작에는 지장 없다"로 넘어갈 수도 있었다. 멤버 변수가 하나 늘어나는 대신 pure 노드 재평가라는 구조적 문제가 사라진다.

## 다음으로 넘김

이 목록의 항목은 **전부 2026-08-29 세션이 이어받았다.**
처리된 것과 아직 남은 것을 함께 정리해 옮겼으므로 여기서는 지운다.

**→ `Docs/AI-Log/2026-08-29-inventory-hold-use-hud.md`의 `다음으로 넘김`을 볼 것.**

이 세션에서 처리된 것만 적어 둔다.

- 명령 10 실행 — 완료 (커밋 `dc0b7ef`)
- 사용(`E`) 로직 — 완료 (커밋 `dc0b7ef`)
- HUD 슬롯 색·HP 바·`SelectedSlot` 일원화 — 완료 (커밋 `dc0b7ef`, `8b27acf`)
- 임시 코드 제거 — 완료 (커밋 `8b27acf`). 단 `INVENTORY FULL`은 의도적으로 남겼다
- off-by-one 변환 지점 못 박기 — `SelectedSlot - 1` 한 곳으로 고정
- `E_ItemNature`의 열거자 인덱스 확인 — `DataTableTools.get_schema`로 읽히고 PIE로도 확정
- `BP_ThirdPersonCharacter` 자동 재저장 — 2026-08-29에는 한 번도 안 일어났다. 재발하면 다시 올린다
