# 2026-08-29

## 작업물

선택한 인벤토리 칸의 아이템이 오른손에 들리게 하고, `E`로 쓰게 하고, HUD가 폰을 직접 읽어 칸 색·HP 바·아이템 이름·`[E] Use`를 그리게 했다. 인벤토리 1단계의 합격 기준 4개가 전부 통과됐다.

**소요 시간**: 약 5시간 (10:00 무렵 세션 시작 ~ 마무리 커밋 `8b27acf` 14:04:43). 중간 커밋 `dc0b7ef` 12:18:23, 사양 문서 `b62b669` 12:22:01.

## 명령

### 한글

사용자가 입력한 순서대로 전부 옮긴다. 오타·말투 그대로다.

```
작업준비
```

```
일단 에디터 켜져있는거 확인해봐
```

```
PIE는 꺼져있어 명령 10 하자
```

```
터미널 결과 보고있어봐
```

```
PIE결과 문제없음
```

```
터미널결과
```

```
PIE에서 1 2 3 눌럿을때 밑에 인벤토리에 초록색 테두리로 표시 잘 되면 된거지? A로 하자 이 두개 확인좀
```

```
1.  Key, Consumable, Holdable 순서
2. 그대로 해
3. 소유하고 있는 아이템을 버리는 기능도 넣을까 아이템 버리기 Q로 해서 만약 아이템 있다면 버릴 수 있는거지 플레이어 위치에다가 버릴 수 있는지도 판단하고 버리는거야 그 기능을 추가해볼까 어떻게 생각하는지
```

```
E에 대한게 좀 다르게 인식된거 같은데 우선 아이템을 먹으면 인벤토리 칸에 아이템이 떠야하는데 지금 아이콘이 없으니까 그건 냅두고, 비어있는것처럼 보이지만 실제로 습득을 한거잔아? 그러면 인벤토리 칸에 만약 아이템이 있다면, 아이템을 오른손에 들고 있는 것으로 보이게끔 하고싶은거임 마인크래프트와 비슷한 아이템 칸 메커니즘 1부터 9까지 선택되잔아 그런걸 하고싶은거임 그리고 아이템이 있는 인벤토리에 만약 사용할 수 있는 기능이 있다면, E를 활성화해서 E를 눌러 사용할 수 있음을 UI로 표현하고 싶어, 지금 아이템이 있을 때 인벤토리 선택시 확인하는 방법이 없잔아, 그러니까 인벤토리 UI 바로 위쪽에 아이템 이름을 텍스트로 나타나게 하는 UI를 추가하자 어떤데
```

```
1. 가
2. 가
3. IconColor 하자
4. 커밋은 이거 작업 하고 하자
```

```
터미널 결과
```

```
터미널 겨로가 보고있어봐
```

```
아저거오타임 결과보고있어봐
```

```
PIE결과 잘나옴
```

```
터미널 결과 확인해봐봐
```

```
PIE 결과 이상없음
```

```
터미널결과봐봐
```

```
PIE 결과 이상 없어 보임
```

```
자자 이거 하기전에 기록해야하는지 지금 작업 효율 괜찮은지 세션에서 작업 더 해도되는지 중간세이브해야하는지 등을 확인해볼까
```

```
커밋과 사양문서쓰고 오늘작업다하고 총정리 개념으로 기록하자
```

```
D:\20260827\MCP1\Docs\Terminal-Log 여기에 터미널 로그 쓰게하는거 어때?
```

```
다된듯?
```

```
PIE 문제없음
```

```
글자를 인벤토리 중앙 위쪽에 뜨게할까 [E] Use도 중앙쪽으로 그리고 글자 크기 좀만 더 키우자 한 2.0할까
```

```
터미널결과봐봐
```

```
PIE결과 문제 없음
```

```
확인해줘
```

```
21 하고 하자
```

```
이대로 올릴게 기다려봐
```

```
확인해줘
```

```
PIE 이상없어보임
```

```
확인해줘
```

```
PIE 결과 이상없음
```

```
일단내비둬 저 파일이 없어질 일은 없을것같아서
```

### English — MCP에 실제로 보낸 명령

이 세션에서 AI가 직접 MCP에 쓴 것은 **하나도 없다.** 읽기(`get_node_infos`, `find_nodes`, `read_graph_dsl`, `get_properties`, `list_variables`, `list_graphs`, `get_schema`, `get_rows`, `get_socket_names`, `get_components`, `get_actor_bounds`, `search_subclasses`, `get_current_level`, `find_actors`)만 AI가 했고, **쓰기는 전부 아래 영어 명령문을 사용자가 UE Terminal에 붙여넣어 실행했다.**

옮기면서 넣은 해석은 각 명령 아래에 따로 밝힌다.

**명령 10 — PlayerController 재배선** (지난 세션에서 작성만 하고 실행 안 한 것을 그대로 사용)

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

**명령 11 — HUD 기본값**

한글 지시에 없던 값: `1`. 사용자가 `1`번 칸을 시작 선택으로 원한 것은 맞으나, "`0`을 `1`로 바꾼다"는 표현은 AI가 정한 것이다.

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD, change the default value of the existing member variable SelectedSlot from 0 to 1. Do not add, rename, or remove any variable, and do not touch the EventGraph or the SetSlot function.

Reason: at PIE start nothing has pressed 1/2/3 yet, so SelectedSlot is 0, which matches no slot and leaves every slot border ColorIdle. The pawn BP_ThirdPersonCharacter already defaults its own SelectedSlot to 1, so this makes the two agree at startup and makes slot 1 highlighted from the first frame.

Compile and save. Then read the value back from the class default object (not from the write call's return value) and report SelectedSlot along with ColorSelected, ColorIdle, SlotCount, confirm that BP_ThirdPersonHUD still has exactly the same variable list it had before, report the compile result including warnings, and the on-disk file size before and after.
```

**명령 12 — 손에 든 아이템 컴포넌트와 갱신 함수**

한글 지시에 없던 값 다섯: 컴포넌트 이름 `HeldItemMesh`, 함수 이름 `RefreshHeldItem`, 스케일 `0.15`, `NoCollision`, 부착 규칙 `Snap to Target` / `Keep Relative`. 스케일 `0.15`는 `/Engine/BasicShapes/Cube`가 100×100×100cm임을 레벨의 `BP_ItemPickup` 바운드(`min -50 → max 50`)로 확인한 뒤 정한 값이다.

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, add a held-item mesh component and a function that refreshes it. Do not modify any existing event chain in this command - no call sites yet.

1. Add a StaticMeshComponent named HeldItemMesh.
   - Static Mesh: none
   - Relative Scale 3D: (0.15, 0.15, 0.15)
   - Collision Enabled: NoCollision

2. Add an Event BeginPlay to the EventGraph. This graph currently has no BeginPlay - confirm that before adding one, and if one already exists, append to it instead of creating a second.
   BeginPlay -> AttachComponentToComponent
     Component      = HeldItemMesh
     Parent         = Mesh (the inherited CharacterMesh0 skeletal mesh component)
     Socket Name    = HandGrip_R
     Location Rule  = Snap to Target
     Rotation Rule  = Snap to Target
     Scale Rule     = Keep Relative
     Weld Simulated Bodies = false
   Scale must be Keep Relative so the 0.15 relative scale survives the attach.

3. Add a new function graph named RefreshHeldItem with no inputs and no outputs. Note that InventorySlots is an Array of Name, not an array of DataTableRowHandle - the slot stores the DataTable row name only.

   Index  = SelectedSlot - 1
   Branch: Index >= 0 AND Index < Length(InventorySlots)
     False -> SetStaticMesh(HeldItemMesh, None) and end
     True  -> RowName = InventorySlots[Index]
              Branch: RowName == None (Name literal None)
                True  -> SetStaticMesh(HeldItemMesh, None) and end
                False -> Get Data Table Row
                           Table   = /Game/Inventory/DT_Items
                           Row Name = RowName
                         Row Found     -> Break S_ItemDef -> SetStaticMesh(HeldItemMesh, mesh)
                         Row Not Found -> SetStaticMesh(HeldItemMesh, None)

   Keep every failure branch wired to SetStaticMesh(None). Do not leave any exec pin dangling.

Compile with warnings_as_errors and save. Then report, read back from get_node_infos and not from the write calls' return values: every node in RefreshHeldItem with its pin connections, every node in the new BeginPlay chain with its pin connections, the component list of the Blueprint, the HeldItemMesh relative scale and collision setting read back from the component template, the full variable list of the Blueprint to confirm nothing was added or renamed, the compile result including warnings, and the on-disk file size before and after. Also confirm that the IA_Interact chain and every other existing event chain still has exactly the connections it had before.
```

**명령 13 — 호출 지점 두 곳 연결**

```
Connect the existing RefreshHeldItem function to the two places that change what the selected slot holds. Add no new variables and no new functions.

1. In /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, EventGraph, IA_Interact chain:
   The pickup success path currently runs ... -> K2Node_IfThenElse_2 (True) -> K2Node_CallArrayFunction_3 (Set Array Elem) -> K2Node_CallFunction_34.
   Insert a call to RefreshHeldItem between Set Array Elem and K2Node_CallFunction_34, so the order becomes:
     Set Array Elem -> RefreshHeldItem -> K2Node_CallFunction_34
   Do not remove the Set Array Elem -> K2Node_CallFunction_34 relationship; re-route it through the new node. Report what K2Node_CallFunction_34 actually is.

2. In /Game/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController, EventGraph, the IA_SelectSlot chain:
   K2Node_VariableSet_0 (SET SelectedSlot on the cast BP_ThirdPersonCharacter) currently has its "then" output unconnected.
   Connect that "then" to a call to RefreshHeldItem on the same character.
   Use the existing K2Node_DynamicCast_0 "AsBP Third Person Character" output as the target - do not add a second Get Controlled Pawn or a second cast.

Compile both Blueprints with warnings_as_errors and save. Then report, read back from get_node_infos and not from the write calls' return values: every node in the IA_Interact success path and in the IA_SelectSlot chain with its pin connections, confirmation that no pre-existing connection was dropped, the compile result including warnings for both Blueprints, and the on-disk file size before and after for both.
```

**명령 14 — HUD가 폰을 읽는 배선**

한글 지시에 없던 값 둘: 변수 이름 `CachedCharacter`, 그리고 "캐스트 실패 시 아무것도 안 그린다"는 동작. 후자는 사용자가 고른 게 아니라 AI가 대안(빈 테두리만 그리기)보다 단순해서 고른 것이다.

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD, make the HUD read the selected slot from the possessed pawn instead of from its own variable. Do not delete BP_ThirdPersonHUD.SelectedSlot or the SetSlot function in this command - they are removed in a later step. Do not change any drawing geometry, any color, or any of SlotCount / SlotSize / SlotGap / BottomMargin / BorderThickness / ColorIdle / ColorSelected.

1. Add a new member variable:
   Name: CachedCharacter
   Type: BP_ThirdPersonCharacter Object Reference
   Default: none
   Instance Editable: false

2. In the Event Receive Draw HUD graph, insert an acquire-and-cache step in front of the existing drawing chain. The existing chain currently starts directly from the event. Change it to:

   Event Receive Draw HUD
     -> Branch: IsValid(CachedCharacter)
          True  -> [the existing drawing chain, completely unchanged]
          False -> Get Owning Player Controller
                -> Get Controlled Pawn
                -> Cast To BP_ThirdPersonCharacter
                     on success -> SET CachedCharacter -> [the same existing drawing chain]
                     Cast Failed -> leave unconnected, so nothing is drawn this frame

   Both the True path and the cast-success path must converge on the same first node of the existing chain. Do not duplicate any drawing node.

3. In the same graph there is a comparison that decides the border color:
       (ForLoop index + 1) == SelectedSlot     ->  Select(ColorSelected, ColorIdle)
   The SelectedSlot side of that Equal node is currently fed by a Get of the HUD's own SelectedSlot variable.
   Re-point that pin so it reads SelectedSlot from CachedCharacter instead.
   Leave the HUD's own SelectedSlot variable in place, now unused.

Compile with warnings_as_errors and save. Then report, read back from get_node_infos and not from the write calls' return values: every node in the new acquire chain with its pin connections, the Equal node with both of its input pins and where each comes from, confirmation that every DrawRect node and every value feeding them still has exactly the connections it had before, the full variable list of the Blueprint before and after, the compile result including warnings, and the on-disk file size before and after.
```

**명령 15 — 칸 색 채우기**

한글 지시("IconColor 하자")에 없던 값 둘: 채움을 `BorderThickness`만큼만 안쪽으로 넣는다는 것, 그리고 테두리 넷 다음에 그린다는 순서.

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD, Event Receive Draw HUD graph, fill each inventory slot that holds an item with that item's iconColor. Do not change any existing node, any existing connection, or any existing pin value. This command is purely additive.

The ForLoop body currently runs four DrawRect nodes in order: K2Node_CallFunction_6 -> 7 -> 8 -> 9. K2Node_CallFunction_9's "then" output is currently unconnected. Append the new logic there.

Reuse these existing pure nodes rather than creating duplicates - identify them by what they compute:
  SLOT_X      the value already feeding K2Node_CallFunction_6's ScreenX  (= left edge of the current slot)
  SLOT_Y      the value already feeding K2Node_CallFunction_6's ScreenY  (= top edge of the current slot)
  INNER       the value already feeding K2Node_CallFunction_8's ScreenH  (= SlotSize - BorderThickness * 2)
  Y_INSET     the value already feeding K2Node_CallFunction_8's ScreenY  (= SLOT_Y + BorderThickness)
  BORDER      the existing Get of BorderThickness
  INDEX       the ForLoop's Index output
  CHARACTER   the existing Get of CachedCharacter

Create exactly one new arithmetic node: X_INSET = SLOT_X + BORDER.

Then:

  K2Node_CallFunction_9.then
    -> Branch A: INDEX < Length(CHARACTER.InventorySlots)
         False -> leave unconnected
         True  -> Branch B: NotEqual_Name( CHARACTER.InventorySlots[INDEX], None )
                    False -> leave unconnected
                    True  -> Get Data Table Row
                               Table    = /Game/Inventory/DT_Items
                               Row Name = CHARACTER.InventorySlots[INDEX]
                             Row Not Found -> leave unconnected
                             Row Found     -> Break S_ItemDef -> DrawRect
                                                RectColor = iconColor
                                                ScreenX   = X_INSET
                                                ScreenY   = Y_INSET
                                                ScreenW   = INNER
                                                ScreenH   = INNER

Use nested Branches as written above. Do NOT combine the two conditions with an AND Boolean node - AND evaluates both inputs, which would read the array out of range whenever Length is smaller than SlotCount.

Use a single Array Get node feeding both Branch B and the Get Data Table Row RowName pin, not two.

Compile with warnings_as_errors and save. Then report, read back from get_node_infos and not from the write calls' return values: every new node with its pin connections, which existing node was reused for each of SLOT_X / SLOT_Y / INNER / Y_INSET / BORDER / INDEX / CHARACTER and its refPath, confirmation that all four original DrawRect nodes still have exactly the pin values and connections they had before apart from K2Node_CallFunction_9's then output, the full variable list before and after, the compile result including warnings, and the on-disk file size before and after.
```

**명령 16 — `E` 사용 로직**

한글 지시에 없던 값 둘: `Started` 핀을 쓴다는 것(사용자는 "E를 눌러 사용"이라고만 했다), 그리고 `Consumable`만 동작한다는 것(사용자가 "사용할 수 있는 기능이 있다면"이라고 한 것을 AI가 `nature == Consumable`로 굳혔다).

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, add the item-use logic for the E key. Do not create any Input Action asset and do not modify any Input Mapping Context - IA_UseItem already exists and IMC_Inventory already maps it to E. Do not modify any existing event chain; this is a new, separate chain in the EventGraph.

Before wiring, report the pin type of the existing variables CurrentHP and MaxHP, and the pin type of the healAmount output on Break S_ItemDef. If CurrentHP is an Integer while healAmount is a Double, insert the conversion the compiler needs and say exactly where you put it. If they are the same type, add no conversion.

Add an EnhancedInputAction IA_UseItem event. Drive the chain from its Started pin, NOT Triggered - IA_UseItem has an empty Triggers array, so Triggered fires every frame the key is held and would consume the item repeatedly. IA_Interact in this same graph already uses Started; follow that.

  IA_UseItem . Started
    -> Index = SelectedSlot - 1
    -> Branch A: (Index >= 0) AND (Index < Length(InventorySlots))
         False -> leave unconnected
         True  -> Branch B: NotEqual_Name( InventorySlots[Index], None )
                    False -> leave unconnected
                    True  -> Get Data Table Row
                               Table    = /Game/Inventory/DT_Items
                               Row Name = InventorySlots[Index]
                             Row Not Found -> leave unconnected
                             Row Found     -> Break S_ItemDef -> Switch on E_ItemNature (nature)
                                                Key       -> leave unconnected
                                                Holdable  -> leave unconnected
                                                Consumable ->
                                                     SET CurrentHP = Clamp( CurrentHP + healAmount, 0, MaxHP )
                                                  -> Set Array Elem( InventorySlots, Index, None )
                                                  -> RefreshHeldItem

Notes on shape:
- Branch A may use an AND node because neither of its two conditions reads the array. Branch B must be nested inside Branch A, not ANDed with it, because it does read the array.
- Use a single Subtract node for Index feeding every consumer, and a single Array Get feeding both Branch B and the Get Data Table Row RowName pin.
- Set Array Elem writes the Name literal None into the slot, clearing it.
- RefreshHeldItem is the existing function; call it, do not duplicate its logic. This is its third call site.
- The Switch on E_ItemNature enumerator order is Key, Consumable, Holdable. Confirm the pin order you actually see on the node and report it - if it differs, report that and stop rather than guessing which pin is which.

Compile with warnings_as_errors and save. Then report, read back from get_node_infos and not from the write calls' return values: every node in the new chain with its pin connections, the Switch node's exec output pin names in the order they appear, the types you found for CurrentHP / MaxHP / healAmount and any conversion you added, the full variable list before and after to confirm nothing was added, confirmation that every pre-existing chain in this graph still has exactly the connections it had before, the compile result including warnings, and the on-disk file size before and after.
```

**명령 17 — HP 바**

여기부터 보고를 화면이 아니라 파일로 받게 했다. 한글 지시에 없던 값 셋: `HPBarHeight 12`, `ColorHPBack (0.1,0.1,0.1,0.8)`, `ColorHPFill (0.9,0.2,0.2,1.0)`. 위치는 슬롯 아래 `SlotGap`만큼으로 정했고, 이는 새 숫자를 만들지 않으려고 기존 값을 재사용한 것이다.

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD, draw an HP bar under the inventory slots. Do not change any existing node, connection, or pin value. Append only.

1. Add three member variables, all Instance Editable:
   HPBarHeight   Float                  default 12
   ColorHPBack   Linear Color           default (R=0.1, G=0.1, B=0.1, A=0.8)
   ColorHPFill   Linear Color           default (R=0.9, G=0.2, B=0.2, A=1.0)

2. In Event Receive Draw HUD, the ForLoop node K2Node_MacroInstance_0 has its "Completed" output unconnected. Append there - the bar is drawn once, after the slot loop, not inside it.

Reuse these existing pure nodes rather than creating duplicates. Identify each by what it computes and report the refPath you settled on:
  BAR_X     the left edge of the whole inventory bar = (SizeX / 2) - (BAR_W / 2).
            It is the value wired into input A of the Add node that produces K2Node_CallFunction_6's ScreenX.
  BAR_W     the total width of the bar = SlotCount * (SlotSize + SlotGap) - SlotGap.
            It is the value wired into the Divide node whose result is subtracted from SizeX / 2.
  SLOT_TOP  the top edge of the slot row. It is the value already feeding K2Node_CallFunction_6's ScreenY.
  SLOT_SIZE the existing Get of SlotSize
  SLOT_GAP  the existing Get of SlotGap
  CHARACTER the existing Get of CachedCharacter that sits in the drawing region (the one feeding GetSelectedSlot), not the one feeding the IsValid gate

3. Wire:

  ForLoop.Completed
    -> Branch: CHARACTER.MaxHP > 0
         False -> leave unconnected
         True  -> DrawRect  RectColor = ColorHPBack
                            ScreenX   = BAR_X
                            ScreenY   = HP_Y
                            ScreenW   = BAR_W
                            ScreenH   = HPBarHeight
               -> DrawRect  RectColor = ColorHPFill
                            ScreenX   = BAR_X
                            ScreenY   = HP_Y
                            ScreenW   = BAR_W * ( CHARACTER.CurrentHP / CHARACTER.MaxHP )
                            ScreenH   = HPBarHeight

  where HP_Y = SLOT_TOP + SLOT_SIZE + SLOT_GAP

Create only the arithmetic nodes this needs: HP_Y (two Adds), the CurrentHP / MaxHP Divide, and the BAR_W * ratio Multiply. Use a single Get of CHARACTER.MaxHP feeding both the Branch condition and the Divide, and a single Get of CHARACTER.CurrentHP.

The background rect must be drawn before the fill rect so the fill sits on top.

Compile with warnings_as_errors and save.

Then write the full report to Docs/Terminal-Log/2026-08-29-17-hp-bar.md as UTF-8. Do NOT print the report - print only that file path and a one-line PASS or FAIL. Do not truncate, summarise, or reflow anything in the file; it is the archived original and will be committed. Wrap raw tool output and log lines in fenced code blocks so nothing is reformatted.

The report must contain, read back from get_node_infos and not from the write calls' return values: every new node with its pin connections, the refPath you used for each of BAR_X / BAR_W / SLOT_TOP / SLOT_SIZE / SLOT_GAP / CHARACTER and how you confirmed it is the right node, the default value of each of the three new variables read back from the class default object, confirmation that all five pre-existing DrawRect nodes and the ForLoop still have exactly the connections and pin values they had before apart from ForLoop.Completed, the full variable list before and after, the compile result including warnings, and the on-disk file size before and after. Also record verbatim any warning or error line you saw, and anything where a tool's response disagreed with what you read back afterwards.
```

**명령 18 — 아이템 이름과 `[E] Use`**

한글 지시에 없던 값 넷: `TextLineHeight 24`, 이름 색을 기존 `ColorIdle`로, `[E] Use` 색을 기존 `ColorSelected`로, 문구를 `[E] Use`로. 사용자는 "아이템 이름을 텍스트로", "E를 눌러 사용할 수 있음을 UI로 표현"이라고만 했다.

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD, draw the selected item's name and an "[E] Use" prompt above the inventory bar. Do not change any existing node, connection, or pin value. Append only.

1. Add one member variable, Instance Editable:
   TextLineHeight   Float   default 24

2. K2Node_CallFunction_20 (the HP fill DrawRect added in the previous command) has its "then" output unconnected. Append there. This runs once per frame, after the slot loop and the HP bar - not inside the loop.

Reuse these existing nodes rather than creating duplicates, and report the refPath you settled on for each:
  BAR_X       K2Node_PromotableOperator_5   (left edge of the bar, = SizeX/2 - BAR_W/2)
  SLOT_TOP    K2Node_PromotableOperator_7   (top edge of the slot row)
  CHARACTER   K2Node_VariableGet_17         (the Get of CachedCharacter in the drawing region)
  COLOR_IDLE     the existing Get of ColorIdle that feeds the Select node
  COLOR_SELECTED the existing Get of ColorSelected that feeds the Select node
Confirm each by its pin connections before using it.

3. Wire:

  K2Node_CallFunction_20.then
    -> SEL = CHARACTER.SelectedSlot - 1
    -> Branch A: (SEL >= 0) AND (SEL < Length(CHARACTER.InventorySlots))
         False -> leave unconnected
         True  -> Branch B: NotEqual_Name( CHARACTER.InventorySlots[SEL], None )
                    False -> leave unconnected
                    True  -> Get Data Table Row
                               Table    = /Game/Inventory/DT_Items
                               Row Name = CHARACTER.InventorySlots[SEL]
                             Row Not Found -> leave unconnected
                             Row Found     -> Break S_ItemDef
                                           -> DrawText
                                                Text      = ToString( displayName )
                                                TextColor = COLOR_IDLE
                                                ScreenX   = BAR_X
                                                ScreenY   = NAME_Y
                                                Font      = None, Scale = 1.0, bScalePosition = false
                                           -> Branch C: nature == Consumable
                                                False -> leave unconnected
                                                True  -> DrawText
                                                           Text      = the literal string  [E] Use
                                                           TextColor = COLOR_SELECTED
                                                           ScreenX   = BAR_X
                                                           ScreenY   = USE_Y
                                                           Font      = None, Scale = 1.0, bScalePosition = false

  where  USE_Y  = SLOT_TOP - TextLineHeight
         NAME_Y = SLOT_TOP - ( TextLineHeight * 2 )

Notes on shape:
- Branch A may use an AND node because neither condition reads the array. Branch B must be nested inside Branch A, not ANDed with it, because it does read the array.
- Use a single Subtract for SEL feeding every consumer, and a single Array Get feeding both Branch B and the Get Data Table Row RowName pin.
- displayName is a Text pin and AHUD::DrawText takes an FString, so a ToString (Text) conversion node is required. Report where you placed it.
- For Branch C use an Equal (Enum) node comparing the Break's nature output against a literal. Enum literal pins store the internal enumerator name, not the display name: E_ItemNature's declaration order is Key, Consumable, Holdable, so Consumable is index 1. Report the exact string that ended up stored in that literal pin, and report the index you used and why.
- Create only the arithmetic these need: SEL, TextLineHeight * 2, and the two Subtracts for USE_Y and NAME_Y.

Compile with warnings_as_errors and save.

Then write the full report to Docs/Terminal-Log/2026-08-29-18-item-name-use-prompt.md as UTF-8. Do NOT print the report - print only that file path and a one-line PASS or FAIL. Do not truncate, summarise, or reflow anything in the file; it is the archived original and will be committed. Wrap raw tool output and log lines in fenced code blocks.

The report must contain, read back from get_node_infos and not from the write calls' return values: every new node with its pin connections, the refPath used for each reused node and how it was confirmed, the literal string stored in the Equal (Enum) pin, where the ToString conversion sits, the TextLineHeight default read back from the class default object, a whole-graph before/after set difference showing exactly which lines were removed or altered, the full variable list before and after, the compile result including warnings, and the on-disk file size before and after. Also record verbatim any warning or error line seen, and anything where a tool's response disagreed with what you read back afterwards.
```

**명령 19 — 중앙 정렬과 글자 확대**

사용자가 `2.0`을 지정했다. AI가 정한 것 둘: `TextScale`을 변수로 뺀 것(`GetTextSize`와 `DrawText`의 `Scale`이 어긋나면 정렬이 틀어지므로), `TextLineHeight`를 `24`에서 `40`으로 올린 것.

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD, centre the two text lines horizontally over the inventory bar and enlarge them. Change only what is listed here.

1. Add one member variable, Instance Editable:
   TextScale   Float   default 2.0

2. Change the default value of the existing variable TextLineHeight from 24 to 40.
   Reason: at Scale 2.0 the default HUD font renders roughly 32px tall, so a 24px line
   spacing would make the two lines overlap. Do not change any other variable's default.

3. The current text chain is:
     K2Node_GetDataTableRow_1.then -> K2Node_CallFunction_23 (DrawText, item name)
                                   -> K2Node_IfThenElse_6 (Branch C, nature == Consumable)
                                   -> K2Node_CallFunction_24 (DrawText, "[E] Use")
   Confirm that exec order by reading it back before changing anything, and report what you
   found. If it differs, report the difference and stop rather than guessing.

4. Insert a GetTextSize call in front of each DrawText and recompute its ScreenX so the text
   is centred on the inventory bar:

     GetDataTableRow_1.then
       -> GetTextSize  (call it SIZE_NAME)
            Text  = the SAME ToString(displayName) output already feeding
                    K2Node_CallFunction_23's Text pin - reuse that node, do not add a second
                    ToString
            Font  = None
            Scale = TextScale
       -> K2Node_CallFunction_23 (DrawText, item name)   [unchanged except ScreenX and Scale]
       -> K2Node_IfThenElse_6 (Branch C)
            False -> leave unconnected
            True  -> GetTextSize  (call it SIZE_USE)
                       Text  = LITERAL_USE (see below)
                       Font  = None
                       Scale = TextScale
                  -> K2Node_CallFunction_24 (DrawText, "[E] Use")  [unchanged except ScreenX and Scale]

   LITERAL_USE: create one Make Literal String node holding exactly  [E] Use  and wire its
   output to BOTH SIZE_USE's Text pin and K2Node_CallFunction_24's Text pin, replacing the
   inline literal currently on that DrawText pin. One source, two consumers - a second
   inline literal would let the measured width and the drawn text drift apart.

5. Re-point these pins:

   K2Node_CallFunction_23 (name)
     ScreenX  = BAR_X + ( ( BAR_W - SIZE_NAME.OutWidth ) / 2 )
     Scale    = TextScale        (currently the literal 1.0)
     ScreenY  unchanged - leave it on K2Node_PromotableOperator_34
     TextColor unchanged - leave it on the ColorIdle Get

   K2Node_CallFunction_24 ("[E] Use")
     ScreenX  = BAR_X + ( ( BAR_W - SIZE_USE.OutWidth ) / 2 )
     Scale    = TextScale        (currently the literal 1.0)
     ScreenY  unchanged - leave it on K2Node_PromotableOperator_35
     TextColor unchanged - leave it on the ColorSelected Get

   where BAR_X = K2Node_PromotableOperator_5 and BAR_W = K2Node_PromotableOperator_2,
   the same nodes reused in the previous two commands. Reuse them; create no duplicates.

   Each line needs its own Subtract, Divide and Add - the two widths differ, so these cannot
   be shared between the two lines. Use a single Get of TextScale feeding all four Scale pins.

Do not touch the slot loop, the four slot-border DrawRects, the icon fill DrawRect, the two
HP bar DrawRects, or the IsValid acquire chain.

Compile with warnings_as_errors and save.

Then write the full report to Docs/Terminal-Log/2026-08-29-19-center-text.md as UTF-8. Do NOT print the report - print only that file path and a one-line PASS or FAIL. Do not truncate, summarise, or reflow anything in the file; it is the archived original and will be committed. Wrap raw tool output and log lines in fenced code blocks.

The report must contain, read back from get_node_infos and not from the write calls' return values: the exec order you found in step 3 before changing anything, every new node with its pin connections, the full pin list of both DrawText nodes after the change, the string stored in the Make Literal String node, the defaults of TextScale and TextLineHeight read back from the class default object, a whole-graph before/after set difference showing exactly which lines were removed or altered, the full variable list before and after, the compile result including warnings, and the on-disk file size before and after. Also record verbatim any warning or error line seen, and anything where a tool's response disagreed with what you read back afterwards.
```

**명령 20 — PlayerController 정리**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController, remove the now-dead HUD branch from the IA_SelectSlot chain and collapse the Sequence. This is a deletion command - read the graph back first and stop if what you find differs from what is described.

Expected current shape of the IA_SelectSlot chain:

  K2Node_EnhancedInputAction_0 (IA_SelectSlot) . Triggered
    -> K2Node_ExecutionSequence_0 (Sequence)
         then_0 -> K2Node_DynamicCast_2 (Cast To BP_ThirdPersonHUD)
                     Object   <- K2Node_CallFunction_46 (Get HUD)
                     then     -> K2Node_CallFunction_48 (SetSlot)
                     AsBP...  -> K2Node_CallFunction_48.self
         then_1 -> K2Node_DynamicCast_0 (Cast To BP_ThirdPersonCharacter)
                     Object   <- K2Node_CallFunction_10 (Get Controlled Pawn)
                     then     -> K2Node_VariableSet_0 (SET SelectedSlot)
                              -> K2Node_CallFunction_11 (RefreshHeldItem)

  K2Node_CallFunction_47 (Truncate) takes the event's ActionValue and currently feeds
  BOTH K2Node_CallFunction_48.NewSlot AND K2Node_VariableSet_0.SelectedSlot.

Report that shape back before deleting anything. If it differs, report the difference and stop.

Then:

1. Delete these four nodes and nothing else:
     K2Node_CallFunction_48   (SetSlot call)
     K2Node_DynamicCast_2     (Cast To BP_ThirdPersonHUD)
     K2Node_CallFunction_46   (Get HUD)
     K2Node_ExecutionSequence_0 (Sequence)

2. Connect K2Node_EnhancedInputAction_0's Triggered pin directly to
   K2Node_DynamicCast_0's execute pin. The Sequence existed only to feed two consumers;
   with the HUD branch gone there is one consumer left.

3. Do NOT delete K2Node_CallFunction_47 (Truncate). After step 1 it feeds only
   K2Node_VariableSet_0.SelectedSlot, which is still needed. Confirm after the deletion
   that its ReturnValue has exactly one outgoing connection and that its A input is still
   the event's ActionValue.

4. Do NOT touch the Event BeginPlay chain, the three AddMappingContext calls, the touch
   controls branch, K2Node_CallFunction_10, K2Node_DynamicCast_0, K2Node_VariableSet_0 or
   K2Node_CallFunction_11.

Do not delete or modify anything in BP_ThirdPersonHUD in this command - its SelectedSlot
variable and SetSlot function are removed in a later step. After this command SetSlot simply
has no callers.

Compile with warnings_as_errors and save.

Then write the full report to Docs/Terminal-Log/2026-08-29-20-cleanup-playercontroller.md as UTF-8. Do NOT print the report - print only that file path and a one-line PASS or FAIL. Do not truncate, summarise, or reflow anything in the file; it is the archived original and will be committed. Wrap raw tool output and log lines in fenced code blocks.

The report must contain, read back from get_node_infos and not from the write calls' return values: the chain shape you found before deleting, every node remaining in the IA_SelectSlot chain after the change with its pin connections, the node count before and after, a whole-graph before/after set difference showing exactly which lines were removed or altered, confirmation that the BeginPlay chain is untouched, the full variable list before and after, the compile result including warnings, and the on-disk file size before and after. Also record verbatim any warning or error line seen, and anything where a tool's response disagreed with what you read back afterwards.
```

**명령 21 — HUD 정리**

이 명령문에는 AI의 실수가 하나 들어 있다. "13 member variables"라고 써놓고 14개를 나열했다. 사용자에게 알리고 **일부러 고치지 않은 채로 보냈다** — 검증 장치가 잡아내는지 보려는 것이었다.

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD, remove the now-dead SelectedSlot variable, the SetSlot function, and the orphaned getter node. This is a deletion command - read the state back first and stop if what you find differs from what is described.

Expected current state:
  - The Blueprint has 13 member variables:
      SelectedSlot, SlotCount, SlotSize, SlotGap, BottomMargin, BorderThickness,
      ColorIdle, ColorSelected, CachedCharacter, HPBarHeight, ColorHPBack, ColorHPFill,
      TextScale, TextLineHeight
    (that list is 14 - report the exact list you actually find rather than trusting this)
  - It has a function graph named SetSlot
  - In EventGraph, K2Node_VariableGet_5 is a Get of the HUD's own SelectedSlot whose output
    has NO outgoing connections. The border colour now reads SelectedSlot from
    CachedCharacter via K2Node_VariableGet_17 -> K2Node_VariableGet_18 instead.
  - BP_ThirdPersonPlayerController no longer calls SetSlot - that caller was removed in the
    previous command.

Before deleting anything, report:
  a. the full variable list
  b. the full graph list
  c. K2Node_VariableGet_5's outgoing connections
  d. every node in EventGraph, in ANY graph of this Blueprint, that reads or writes the
     HUD's own SelectedSlot variable - search the whole Blueprint, not just EventGraph
If (c) is not empty, or if (d) finds anything other than K2Node_VariableGet_5 and whatever
lives inside the SetSlot function graph, report it and STOP without deleting.

Then, in this order:

1. Delete the function graph SetSlot. It is deleted first because its body reads and writes
   SelectedSlot; removing the variable first would leave a broken reference inside it.
2. Delete the node K2Node_VariableGet_5 from EventGraph.
3. Delete the member variable SelectedSlot.

Do not delete or modify anything else. In particular do not touch:
  - the other 13 variables or any of their default values
  - CachedCharacter, K2Node_VariableGet_16, K2Node_VariableGet_17, K2Node_VariableGet_18
  - the IsValid acquire chain, the ForLoop, any DrawRect, any DrawText, any GetTextSize
  - the UserConstructionScript graph

Compile with warnings_as_errors and save. If the compile fails, report the exact error text
and stop - do not attempt a fix.

Then write the full report to Docs/Terminal-Log/2026-08-29-21-cleanup-hud.md as UTF-8. Do NOT print the report - print only that file path and a one-line PASS or FAIL. Do not truncate, summarise, or reflow anything in the file; it is the archived original and will be committed. Wrap raw tool output and log lines in fenced code blocks.

The report must contain, read back from get_node_infos / list_variables / list_graphs and not from the write calls' return values: the four items (a) to (d) as found before deleting, the variable list after, the graph list after, the node count in EventGraph before and after, a whole-graph before/after set difference showing exactly which lines were removed or altered, confirmation that the defaults of all remaining variables are unchanged as read from the class default object, the compile result including warnings, and the on-disk file size before and after. Also record verbatim any warning or error line seen, and anything where a tool's response disagreed with what you read back afterwards.
```

**명령 22 — Character 임시 코드 제거**

`INVENTORY FULL`을 남긴 것은 AI의 판단이다. 사용자는 "임시 코드 제거"를 승인했을 뿐 어느 것을 남길지 말하지 않았다. AI가 먼저 이유를 대고 제안했고 사용자가 이의를 달지 않았다.

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, remove the pickup debug print and turn off the line trace debug drawing. Read the state back first and stop if what you find differs from what is described.

Expected current state in EventGraph:

  Pickup success path:
    K2Node_CallArrayFunction_3 (Set Array Elem)
      -> K2Node_CallFunction_18 (RefreshHeldItem)
      -> K2Node_CallFunction_34 (Print String)
      -> K2Node_CallFunction_35 (Destroy Actor)

  The Print String's InString comes from a two-node string chain:
    K2Node_CallFunction_32 (BuildString(Name))     Prefix "PICKED "  Suffix " -> slot "
                                                   InName <- K2Node_BreakStruct_1.out1
      -> K2Node_CallFunction_33 (BuildString(Integer))  InInt <- K2Node_VariableGet_10
      -> K2Node_CallFunction_34.InString

  K2Node_CallFunction_25 (Line Trace By Channel) has its DrawDebugType pin set to ForDuration.

Report that shape back before changing anything. If it differs, report the difference and stop.

Then:

1. Delete these three nodes:
     K2Node_CallFunction_34   (Print String)
     K2Node_CallFunction_33   (BuildString(Integer))
     K2Node_CallFunction_32   (BuildString(Name))

2. Connect K2Node_CallFunction_18's then output directly to K2Node_CallFunction_35's execute
   input, so the success path becomes
     Set Array Elem -> RefreshHeldItem -> Destroy Actor

3. Check K2Node_VariableGet_10 (the Get feeding the deleted BuildString(Integer)'s InInt).
   After step 1, if its output has NO remaining outgoing connections, delete it too. If it
   still has any consumer, leave it and report which node still uses it. Report which variable
   it gets, and which way you went.

4. Set K2Node_CallFunction_25's DrawDebugType pin to None. Change no other pin on that node -
   leave Start, End, TraceChannel, bTraceComplex, ActorsToIgnore, DrawTime and the colours
   exactly as they are.

Do NOT delete K2Node_BreakStruct_1 - it also feeds K2Node_CallArrayFunction_3's Item pin and
must survive.

Do NOT delete or modify K2Node_CallFunction_36, the "INVENTORY FULL" Print String on
K2Node_IfThenElse_2's else branch. It is deliberately kept: it is the only feedback the
player gets when the inventory is full, and nothing has replaced it yet.

Do not touch the IA_UseItem chain, the BeginPlay attach chain, RefreshHeldItem, Move, Aim,
ToggleCameraView, or any variable or its default.

Compile with warnings_as_errors and save.

Then write the full report to Docs/Terminal-Log/2026-08-29-22-cleanup-character.md as UTF-8. Do NOT print the report - print only that file path and a one-line PASS or FAIL. Do not truncate, summarise, or reflow anything in the file; it is the archived original and will be committed. Wrap raw tool output and log lines in fenced code blocks.

The report must contain, read back from get_node_infos and not from the write calls' return values: the shape you found before changing anything, every node remaining in the IA_Interact chain after the change with its pin connections, the full pin list of K2Node_CallFunction_25 after the change, what you did about K2Node_VariableGet_10 and why, confirmation that K2Node_BreakStruct_1 and K2Node_CallFunction_36 still have exactly the connections they had before, the node count before and after, a whole-graph before/after set difference showing exactly which lines were removed or altered, the full variable list before and after, the compile result including warnings, and the on-disk file size before and after. Also record verbatim any warning or error line seen, and anything where a tool's response disagreed with what you read back afterwards.
```

## Terminal 결과

### 원문 — English

**명령 17~22의 터미널 출력은 전문이 `Docs/Terminal-Log/`에 파일로 보존돼 있다.** 커밋 `8b27acf`에 들어 있다.

```
Docs/Terminal-Log/2026-08-29-17-hp-bar.md                    469 lines
Docs/Terminal-Log/2026-08-29-18-item-name-use-prompt.md      562 lines
Docs/Terminal-Log/2026-08-29-19-center-text.md               533 lines
Docs/Terminal-Log/2026-08-29-20-cleanup-playercontroller.md  469 lines
Docs/Terminal-Log/2026-08-29-21-cleanup-hud.md               410 lines
Docs/Terminal-Log/2026-08-29-22-cleanup-character.md         609 lines
```

**명령 10~16의 출력은 파일이 없다.** 화면에 찍힌 것을 사용자가 복사해 붙였고, **전부 UE Terminal 창의 폭에서 잘렸다.** 아래는 그중 판단 근거가 된 부분과, 잘림·어긋남의 증거가 되는 부분을 발췌한 것이다. 잘린 자리는 원문 그대로 두었다 — 다듬으면 잘렸다는 사실 자체가 지워진다.

**명령 13 — MCP가 노드 생성을 거부한 원문 (전문)**

```
[2026.08.29-02.13.47:595][757]LogScript: Warning: The node could not be created /
CallFunction|RefreshHeldItem does not exist
```

터미널의 설명:

```
find_node_types in that graph reported CallFunction|RefreshHeldItem as valid — but only when given the cast's output pin as context_pins. Without context it returned nothing, and its Class|BPThirdPersonCharacter| listing omitted RefreshHeldItem while including Move, Aim, and ToggleCameraVie"CallFunction|RefreshHeldItem" plusdeclaring_class: BP_ThirdPersonCharacter_C was rejected anyway; type_id: "Class|BPThirdPersonCharacter|RefreshHeldItem" —
the form the listing claimed did not exist — she character confirms RefreshHeldItem withbIsImplemented: true throughout. I don't know why the listing omits it, so I'm not guessing; the working recipe is the Class|<BP>|<Func> type_id.
```

**명령 14 — `IsValid` 순수 노드를 만들 수 없다는 보고 (전문)**

```
You specified Branch: IsValid(CachedCharacter) — a pure IsValid feeding a Branch node. I could not create the pure IsValid (Object) function node. find_node_types reports three separate entries all sharing the type_id Utilities|IsValid, and create_node resolves that id to the IsValid macro every time. I tried declaring_class: /Script/Engine.KismetSystemLibrary and /Script/Engine.BlueprintFunctionLibrary; both produced K2Node_MacroInstance with exec pins Is Valid / Is Not Valid, not a boolean output.

So I used the IsValid macro directly and deleted the Branch. The macro is a branch: its two exec outputs are the True and False paths. Behavior matches your spec exactly; the node count is one lower than you described. Everything else follows your spec literally. I deleted the three nodes I had created and did not need (the Branch and two probe macros) — all created in this command, none pre-existing.
```

**명령 11 — 설명되지 않은 파일 크기 감소 (잘린 채로 그대로)**

```
File size

- Before: 145,593 bytes (Aug 28 15:51)
- After: 145,156 bytes (Aug 29 10:39) — −437 bytes

It got smaller. I did not expect that from fliverified explanation, so I'm not offering one.save_assets returned true, is_dirty now returns false, and git status shows M
Content/ThirdPerson/Blueprints/BP_ThirdPersonHroller from the previous task — nothing else.
```

**명령 11 — 터미널이 출처를 못 밝힌 경고 (전문)**

```
[2026.08.29-01.34.52:515][919]LogScript: Warning: GetObjectProperties on
'/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD_C'
(BlueprintGeneratedClass): the following prope
SelectedSlot, ColorSelected, ColorIdle, SlotCount, SlotSize, SlotGap,
BorderThickness, BottomMargin
      Function /Script/ToolsetRegistry.ToolsetLibrary:GetObjectProperties:64X
```

이것은 AI가 낸 것이다. 명령 11을 쓰기 전 색을 확인하려고 CDO가 아니라 생성 클래스(`..._C`)에 `get_properties`를 걸었다가 실패했다.

**명령 16 — enum 프로퍼티를 읽지 못한 경고 (전문, 명령 18 보고에서 발췌)**

```
[2026.08.29-03.00.10:250][294]LogScript: Warning: GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: DisplayNameMap
[2026.08.29-03.00.10:584][295]LogScript: Warning: GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: Names
[2026.08.29-03.00.10:919][296]LogScript: Warning: GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: NamesAndValues
[2026.08.29-03.00.11:251][297]LogScript: Warning: GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: EnumDisplayNameFn
[2026.08.29-03.00.11:252][297]LogScript: Warning: GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: CppForm
```

**터미널 폰트에 한글 글리프가 없다는 로그 증거 (명령 18 보고에서 발췌, 대표 4줄)**

```
[2026.08.29-03.32.24:958][396]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+b85c, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.29-03.32.24:959][396]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+bc14, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.29-03.32.24:959][396]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+d655, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.29-03.32.24:959][396]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c778, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
```

`U+b85c`=로, `U+bc14`=바, `U+d655`=확, `U+c778`=인. 터미널 보고는 약 30줄이 코드포인트만 다른 같은 모양이라고 밝히고 4줄만 발췌했다.

**명령 19 — `GetTextSize`가 순수 노드라는 보고 (전문)**

```
The command's step 4 diagram places `GetTextSize` inside the execution chain:

  GetDataTableRow_1.then
    -> GetTextSize  (SIZE_NAME)
    -> K2Node_CallFunction_23 (DrawText, item name)

`HUD|GetTextSize` has **no exec pins**. Read back from `get_node_type_pins` before any node
was created:

  input_pins:  0 self (HUD Object Reference)
               1 Text (String)
               2 Font (Font Object Reference)
               3 Scale (Float (single-precision))  value 1.000000
  output_pins: 0 OutWidth  (Float (single-precision))
               1 OutHeight (Float (single-precision))

There is no `execute` input and no `then` output, so the node cannot be inserted into an exec
chain - there is nothing to connect an exec wire to. It is a pure function node: it is
evaluated on demand when something downstream needs its output.
```

**명령 19 — `get_node_type_pins`가 존재하지 않는 노드를 가리킨다는 보고 (전문)**

```
Probing `HUD|GetTextSize` returned a full NodeInfo whose `node.refPath` was
`...:EventGraph.K2Node_CallFunction_25`, with a `position` of 0,0. That node is not in the
graph. Checked immediately afterwards: `find_nodes` still returned 98 nodes and the list
of `K2Node_CallFunction_*` names contained no `K2Node_CallFunction_25`:

{"count": 98, "has_CallFunction_25": false, "callfunctions": ["K2Node_CallFunction_1", "K2Node_CallFunction_10", "K2Node_CallFunction_11", "K2Node_CallFunction_15", "K2Node_CallFunction_19", "K2Node_CallFunction_2", "K2Node_CallFunction_20", "K2Node_CallFunction_22", "K2Node_CallFunction_23", "K2Node_CallFunction_24", "K2Node_CallFunction_3", "K2Node_CallFunction_4", "K2Node_CallFunction_5", "K2Node_CallFunction_6", "K2Node_CallFunction_7", "K2Node_CallFunction_8", "K2Node_CallFunction_9"]}

So the probe leaves nothing behind, but the refPath and position it reports are not real
and must not be used to address a node. The pin names, indices, types and default values
it reports were all confirmed correct against the nodes actually created afterwards.
```

**명령 21 — AI의 틀린 숫자를 잡아낸 부분 (전문)**

```
That is **14** member variables, not 13. The command's prose said "13 member variables" and
then listed 14 names, and instructed me to report the exact list I actually find rather than
trusting the prose. The list I find has 14 entries and matches the command's enumerated names
```

**명령 21 — `SelectedSlot`이라는 이름이 넷이었다는 부분 (전문)**

```
[SetSlot] K2Node_VariableSet_0 [|SetSelectedSlot] selfpins=NONE(self=HUD) | out0(then) -> <none> ; out1(Output_Get) -> <none>
[EventGraph] K2Node_VariableGet_5 [|GetSelectedSlot] selfpins=NONE(self=HUD) | out0(SelectedSlot) -> <none>
[EventGraph] K2Node_VariableGet_18 [|GetSelectedSlot] selfpins=['self:BP Third Person Character Object Reference'] | out0(SelectedSlot) -> ['K2Node_PromotableOperator_14.in1']
[EventGraph] K2Node_VariableGet_44 [|GetSelectedSlot] selfpins=['self:BP Third Person Character Object Reference'] | out0(SelectedSlot) -> ['K2Node_PromotableOperator_29.in0']
```

**모든 보고에 공통으로 나온 반환값 관찰 (명령 17 보고에서, 전문)**

```
Write calls return `null` on success, not `true`.
   `add_variable`, `set_variable_instance_editable` and `compile_blueprint` all returned
   `null`. Read-back confirmed all three variables exist with the requested types and that
   the Blueprint compiled. So `null` here means success, and the return value carries no
   information either way. By contrast `ObjectTools.set_properties` and
   `AssetTools.save_assets` both returned `true`. The return values of these tools are not a
   reliable success signal and were not used as one anywhere in this report.
```

**명령 19 — 연결된 핀이 옛 리터럴을 계속 보고한다는 관찰 (전문)**

```
Connected pins still report their stale literal in `value`.
   After connecting TextScale to the four Scale pins, all four still read
   `val=1.000000` alongside the connection. Same for `TextColor` reading
   `val=(R=0,G=0,B=0,A=1)` under a live wire. The `value` field is the pin's stored default
   and is not cleared when a connection is made; the connection is what matters. Anyone
   auditing this graph from the `value` field alone would wrongly conclude Scale is still
   1.0.
```

### 요약 — 한글

**`BP_ThirdPersonCharacter`**

- `HeldItemMesh`(`StaticMeshComponent`) 추가. `BeginPlay`에서 `CharacterMesh0`의 `HandGrip_R` 소켓에 `AttachComponentToComponent`로 부착. `RelativeScale3D (0.15, 0.15, 0.15)`, `CollisionEnabled NoCollision`, `LocationRule/RotationRule SnapToTarget`, `ScaleRule KeepRelative`, `bWeldSimulatedBodies false`
- `RefreshHeldItem` 함수 그래프 추가. `SelectedSlot - 1`로 인덱스를 만들고 범위·`None`·행 없음 셋 다 `SetStaticMesh(None)`으로 닫는다
- `RefreshHeldItem` 호출 지점 셋: 습득 성공(`SetArrayElem` 직후), 슬롯 선택(PlayerController에서), `Consumable` 사용 직후
- `EnhancedInputActionIA_UseItem` 이벤트를 `Started` 핀에서 시작. `Switch on E_ItemNature`의 `NewEnumerator1`(=`Consumable`)만 연결. `Clamp(Float)`로 HP를 올리고 `SetArrayElem`으로 칸을 `None`으로
- `Print String`(`PICKED …`)과 `BuildString` 둘, `FoundSlotIndex` getter 삭제. `LineTraceByChannel`의 `DrawDebugType`을 `ForDuration` → `None`
- `Print String`(`INVENTORY FULL`)은 남겼다
- 변수 12개 그대로. 추가·삭제·리네임 없음

**`BP_ThirdPersonPlayerController`**

- `IA_SelectSlot` 체인에 `Sequence`를 넣어 폰의 `SelectedSlot`도 설정하게 했다가(명령 10), HUD 가지가 죽자 `Sequence`·`GetHUD`·`CastToBP_ThirdPersonHUD`·`SetSlot` 넷을 삭제하고 `Triggered`를 캐스트에 직결했다(명령 20)
- `Truncate` 노드는 하나 그대로. 소비자가 둘에서 하나(`SetSelectedSlot`)로 줄었다
- `RefreshHeldItem` 호출 노드 추가
- 노드 21 → 26 → 22

**`BP_ThirdPersonHUD`**

- `SelectedSlot` 기본값 `0` → `1`, 이후 변수 자체를 삭제
- `CachedCharacter` 추가. `IsValid` 매크로로 게이트하고, 무효면 `GetOwningPlayerController` → `GetControlledPawn` → `CastToBP_ThirdPersonCharacter` → `SET`. 두 경로가 `ForLoop`의 같은 `execute` 핀으로 수렴한다
- 칸 색 채우기 `DrawRect` 추가. 분기 중첩으로 범위 밖에서 배열을 안 읽는다
- HP 바 `DrawRect` 둘 추가(`ColorHPBack` 배경 → `ColorHPFill` 채움). `MaxHP > 0` 분기로 0 나눗셈 방지
- 아이템 이름 `DrawText`와 `[E] Use` `DrawText` 추가. `ToString(Text)` 변환 하나, `Equal(Enum)`의 리터럴은 `NewEnumerator1`
- `GetTextSize` 둘로 폭을 재서 `BAR_X + (BAR_W - width) / 2`로 중앙 정렬. `MakeLiteralString`(`[E] Use`) 하나가 측정과 그리기 양쪽에 물린다
- `SetSlot` 함수 그래프와 죽은 getter `K2Node_VariableGet_5` 삭제
- 변수 8 → 9 → 12 → 13 → 14 → 13. 최종: `SlotCount 3`, `SlotSize 64`, `SlotGap 8`, `BottomMargin 48`, `BorderThickness 2`, `ColorIdle (1,1,1,1)`, `ColorSelected (0,1,0,1)`, `CachedCharacter`, `HPBarHeight 12`, `ColorHPBack (0.1,0.1,0.1,0.8)`, `ColorHPFill (0.9,0.2,0.2,1)`, `TextLineHeight 40`, `TextScale 2`
- 노드 44 → 52 → 63 → 76 → 98 → 96

**새 애셋 없음.** `IA_UseItem`과 `IMC_Inventory`의 `E` 매핑은 이미 있었다. `HandGrip_R` 소켓도 이미 있었다. `S_ItemDef.mesh` 필드와 세 행의 값도 이미 있었다.

## 분석

### 무엇을 만들었나

**컴포넌트 — `BP_ThirdPersonCharacter`**

- `HeldItemMesh` : `StaticMeshComponent`
  - `StaticMesh` = `None` (런타임에 교체)
  - `RelativeScale3D` = `(0.14999999999999999, ...)` — double로 찍힌 `0.15`
  - `Mobility` = `Movable`
  - `BodyInstance.collisionEnabled` = `NoCollision`
  - `collisionProfileName`은 `BlockAllDynamic`으로 남아 있다. 충돌이 꺼져 있어 무효지만 값 자체는 안 건드렸다
  - 부착: `BeginPlay` → `AttachComponentToComponent(HeldItemMesh, Mesh, "HandGrip_R", SnapToTarget, SnapToTarget, KeepRelative, false)`

**함수 — `BP_ThirdPersonCharacter.RefreshHeldItem`** (입력 없음, 출력 없음)

```
(if (and (>= (- SelectedSlot 1) 0) (< (- SelectedSlot 1) (Length InventorySlots)))
  (if (Equal(Name) InventorySlots[i] "None")
    (SetStaticMesh HeldItemMesh)
    (else (GetDataTableRow "/Game/Inventory/DT_Items" InventorySlots[i]
      (:then (SetStaticMesh HeldItemMesh (BreakSItemDef row).mesh))
      (:RowNotFound (SetStaticMesh HeldItemMesh)))))
  (else (SetStaticMesh HeldItemMesh)))
```

**입력 — 새로 만든 것 없음**

- `IA_UseItem` : `/Game/Input/Actions/IA_UseItem`, `ValueType Boolean`, `Triggers []`, `Modifiers []`, `bConsumeInput true`
- `IMC_Inventory`의 5번째 매핑 : `action = IA_UseItem`, `key = E`, `triggers []`, `modifiers []`
- 이벤트는 `Started` 핀에서 시작. `IA_Interact`(F)도 `Started`를 쓴다

**변수 — `BP_ThirdPersonHUD` 최종 13개**

| 이름 | 타입 | 기본값 |
|---|---|---|
| `SlotCount` | int | `3` |
| `SlotSize` | float | `64` |
| `SlotGap` | float | `8` |
| `BottomMargin` | float | `48` |
| `BorderThickness` | float | `2` |
| `ColorIdle` | LinearColor | `(1, 1, 1, 1)` |
| `ColorSelected` | LinearColor | `(0, 1, 0, 1)` |
| `CachedCharacter` | `BP_ThirdPersonCharacter` 참조 | 없음 |
| `HPBarHeight` | float | `12` |
| `ColorHPBack` | LinearColor | `(0.1, 0.1, 0.1, 0.8)` |
| `ColorHPFill` | LinearColor | `(0.9, 0.2, 0.2, 1.0)` |
| `TextLineHeight` | float | `40` |
| `TextScale` | float | `2.0` |

**HUD 그리기 순서 (한 프레임)**

1. `IsValid(CachedCharacter)` — 무효면 폰을 잡아 캐시. 캐스트 실패면 이 프레임에 아무것도 안 그린다
2. `ForLoop 0..SlotCount-1` 안에서 칸마다: 테두리 `DrawRect` 4개(위·아래·왼쪽·오른쪽), 그 다음 아이템이 있으면 `iconColor` 채움 `DrawRect` 1개
3. 루프 종료 후: HP 바 `DrawRect` 2개(배경 → 채움)
4. 그 다음: 선택된 칸에 아이템이 있으면 이름 `DrawText`, `nature == Consumable`이면 `[E] Use` `DrawText`

**기하 값**

- 바 왼쪽 = `SizeX / 2 - BAR_W / 2`, `BAR_W = SlotCount * (SlotSize + SlotGap) - SlotGap` = `3 * 72 - 8` = `208`
- 슬롯 위 = `SizeY - BottomMargin - SlotSize`
- 채움 = 테두리 안쪽 `BorderThickness`만큼, 폭·높이 모두 `SlotSize - BorderThickness * 2` = `60`
- HP 바 Y = 슬롯 위 + `SlotSize` + `SlotGap`
- 이름 Y = 슬롯 위 − `TextLineHeight * 2`, `[E] Use` Y = 슬롯 위 − `TextLineHeight`
- 두 텍스트 X = `BAR_X + (BAR_W - GetTextSize.OutWidth) / 2`

### 기술적으로 맞게 짚은 부분

**`E`를 `Triggered`가 아니라 `Started`에서 받은 것.** `IA_UseItem`의 `Triggers` 배열이 비어 있다(MCP로 읽어 확인). Enhanced Input에서 트리거가 하나도 없는 bool 액션은 키를 누르고 있는 동안 `Triggered`가 매 프레임 발동한다. 포션을 한 번 눌러 여러 번 먹게 된다. `Started`는 눌린 순간 한 번만 발동한다. 같은 그래프의 `IA_Interact`가 이미 `Started`를 쓰고 있었고(`out 1`에 연결됨을 `get_node_infos`로 확인), 그 관례를 따랐다.

**`AND` 대신 분기를 중첩한 것.** 블루프린트의 `AND Boolean`은 단락 평가를 하지 않고 두 입력을 모두 평가한다. `Index < Length(InventorySlots)`와 `InventorySlots[Index] != None`을 `AND`로 묶으면, 인덱스가 범위 밖일 때도 `Get (a copy)`가 실행되어 경고가 나고 기본값이 흘러간다. 분기를 중첩하면 안쪽 분기의 조건은 바깥 분기가 통과한 뒤에만 평가되므로 배열을 안 읽는다. 순수 노드는 소비 지점에서 평가되기 때문에 이 구분이 실제로 작동한다.

**부착 규칙에서 스케일만 `Keep Relative`로 둔 것.** `Snap to Target`은 대상의 트랜스폼을 그대로 받는다는 뜻이라, 스케일까지 Snap하면 컴포넌트에 설정한 `0.15`가 부모 스켈레탈 메시의 스케일로 덮인다. 위치·회전은 소켓에 딱 붙어야 하므로 Snap이 맞고, 스케일만 상대값을 지켜야 한다.

**아이템 액터를 스폰하지 않고 메시만 갈아끼운 것.** `S_ItemDef`에 이미 `mesh` 필드가 있었으므로 `SetStaticMesh` 한 번으로 끝난다. `BP_ItemPickup`을 스폰해 붙이는 방식이면 스폰·파괴·`EndPlay` 정리가 전부 따라온다. 지금 요구사항은 "보이게만 하면 된다"이므로 그것을 정당화하지 않는다.

**손 갱신을 함수로 뽑은 것.** 호출 지점이 **실제로 셋**이다 — 슬롯 선택, 습득 성공, 사용으로 칸이 빔. 가상의 미래를 위한 구조가 아니라 이미 존재하는 중복이었다. 셋 중 둘은 다른 블루프린트(`PlayerController`)에서 부른다.

**HUD가 폰을 `BeginPlay`가 아니라 첫 그리기에서 잡은 것.** `AHUD`는 `APlayerController::ClientRestart`에서 스폰되므로 보통 빙의 뒤지만, 보장은 없다. 첫 `ReceiveDrawHUD`에서 잡으면 순서에 의존하지 않는다. 그리고 `IsValid`로 게이트하므로 이후 프레임에는 `Cast`를 타지 않는다 — `Event Tick`에서 `Cast`를 돌리지 말라는 규칙이 그리기 이벤트에도 그대로 적용된다.

**`TextScale`을 하드코딩하지 않고 변수로 뺀 것.** `GetTextSize`의 `Scale`과 `DrawText`의 `Scale`이 다르면 잰 폭과 그린 폭이 달라져 중앙 정렬이 조용히 틀어진다. 변수 하나가 네 핀에 물리면 구조적으로 어긋날 수 없다. 값이 `2.0`이라서가 아니라 **두 곳이 반드시 같아야 해서** 변수인 것이다.

**`MakeLiteralString`을 하나 두고 두 곳에 물린 것.** 같은 이유다. `[E] Use`를 두 핀에 각각 리터럴로 넣으면 나중에 한쪽만 고쳐서 폭 계산이 어긋난다.

**삭제 순서를 `SetSlot` 함수 → getter 노드 → 변수로 잡은 것.** `SetSlot`의 본체가 `SelectedSlot`을 쓴다. 변수를 먼저 지우면 함수 그래프 안에 깨진 참조가 남는다. 마찬가지로 `BP_ThirdPersonHUD.SetSlot`을 지우기 전에 `BP_ThirdPersonPlayerController`의 호출 노드를 먼저 끊었다. 순서를 뒤집었으면 컴파일이 깨졌다.

**`BreakStruct_1`을 안 지운 것.** `Print String` 체인을 지울 때 딸려 죽을 뻔했는데, 그 노드의 `RowName` 출력이 `SetArrayElem.Item`에도 물려 있었다. 지웠으면 **습득이 칸에 아무것도 안 넣게 됐을 것이고, 컴파일 에러도 안 났을 것이다** — 핀이 비면 `None`이 흘러간다.

**`INVENTORY FULL`을 안 지운 것.** 1단계 사양이 "가득 찼을 때 안내만 띄운다"고 못 박아 뒀는데, 대체할 HUD 표시가 아직 없다. 임시 코드라는 이유로 지웠으면 사양이 요구하는 동작이 조용히 사라졌을 것이다.

**`Truncate`를 안 지운 것.** `SetSlot` 노드를 지우면 소비자가 둘에서 하나로 줄지만 노드 자체는 여전히 필요하다. "죽은 가지를 지운다"는 흐름에 휩쓸려 같이 지웠으면 `SelectedSlot`에 정수가 안 들어갔을 것이다.

**MCP의 반환값을 근거로 삼지 않은 것.** 모든 명령이 "쓰기 호출의 반환값이 아니라 다시 읽어서 보고하라"고 요구했고, 그 결과 `add_variable`·`set_variable_instance_editable`·`compile_blueprint`가 **성공에 `null`을 돌려준다**는 사실이 드러났다. 반환값을 성공 신호로 썼다면 매번 실패로 판단했을 것이다.

### 확인한 것 / 확인 못 한 것

**확인한 것 — PIE에서 눈으로 본 것**

- 시작하자마자 1번 칸이 초록 테두리 (명령 11)
- `1`/`2`/`3`으로 초록 테두리가 옮겨 다닌다 (명령 10·11)
- 공을 조준하고 `F` → 공이 사라지고 **오른손에 공이 들린다** (명령 12·13)
- `1`/`2`/`3`으로 **손의 물건이 바뀐다.** 빈 칸이면 손이 빈다 (명령 13)
- HUD가 폰을 읽게 바꾼 뒤에도 초록 테두리가 전과 똑같이 움직인다 (명령 14)
- 칸이 `iconColor`로 채워진다 — 열쇠 노랑, 포션 빨강, 공 파랑 (명령 15)
- 포션 칸에서 `E` → 칸이 비고 손이 빈다. 열쇠·공에서 `E` → 아무 일도 없다. 빈 칸에서 `E` → 아무 일도 없고 에러 없음 (명령 16)
- HP 바가 슬롯 아래에 뜨고 포션을 먹으면 가득 찬다 (명령 17)
- 아이템 이름과 `[E] Use`가 뜨고, `[E] Use`는 포션에만 뜬다 (명령 18)
- 두 줄이 바 중앙에 정렬되고 글자가 커졌다 (명령 19)
- `Sequence`를 지우고 HUD 변수를 지운 뒤에도 화면이 그대로다 (명령 20·21)
- 디버그 선과 `PICKED` 글자가 사라졌다 (명령 22)

**확인한 것 — MCP로 실제 상태를 다시 읽은 것**

명령 10~22 전부에 대해 `get_node_infos` / `find_nodes` / `list_variables` / `list_graphs` / `get_properties`로 재확인했다. 터미널 보고와 어긋난 곳은 **한 건도 없었다.**

**합격 기준 4개 전부 통과.** `Docs/Spec/2026-08-28-인벤토리-1단계.md`의 기준을 `Docs/Spec/2026-08-29-인벤토리-2단계.md`에서 갱신한 문장 기준이다.

**확인 못 한 것**

- **`Instance Editable` 플래그 — 다섯 변수 전부.** `BlueprintTools`에 `get_variable_instance_editable`이 없다. `get_variable_category`와 `get_variable_replication`은 있는데 이것만 없다. 유일한 근거가 쓰기 호출의 응답인데, **그 응답이 `null`이었다.** 이 툴에서 `null`은 성공도 실패도 될 수 있다. 디테일 패널에서 눈으로 봐야 확실하다
- **`INVENTORY FULL` 경로.** 이번에도 한 번도 못 봤다. 인벤토리를 가득 채운 상태로 또 주워야 하는데 레벨에 `BP_ItemPickup`이 3개뿐이라 칸이 딱 맞게 찬다. 명령 22가 그 노드를 안 건드렸다는 것은 `get_node_infos`로 확인했지만, 실제로 발동하는지는 안 봤다
- **`MaxHP`가 0일 때 HP 바를 안 그리는 분기.** 분기는 그래프에 있으나 `MaxHP`를 0으로 만들어 본 적이 없다
- **캐스트 실패 시 HUD가 아무것도 안 그리는 경로.** `Lvl_ThirdPerson`에서는 항상 성공한다
- **`Lvl_ArenaShooter`에서의 동작.** 그 레벨이 어떤 GameMode를 쓰는지 이번에도 안 봤다
- **`0.15` 스케일과 `HandGrip_R` 소켓의 위치·각도가 아이템마다 적절한지.** 큐브·원기둥·구 셋 다 대칭이라 각도 문제가 드러나지 않았을 수 있다. 칼처럼 방향이 있는 메시가 오면 그때 드러난다

### 남는 리스크

**`unreal-mcp`의 경계선 — 이번에 새로 확인된 것**

- **`read_graph_dsl`은 함수 그래프에서 정확하고, EventGraph의 `EnhancedInputAction` 이벤트 체인에서 본체가 잘린다.** 이벤트 노드만 뱉고 뒤를 통째로 생략한다. **한 핀에 들어오는 두 번째 연결(수렴 간선)도 생략한다** — `ForLoop.execute`에 두 경로가 물린 것을 DSL은 하나만 보여줬다. 노드 단위 확인은 `find_nodes` + `get_node_infos`로 해야 한다
- **`ObjectTools.get_properties`는 `..._C`(BlueprintGeneratedClass)로 안 읽힌다.** `Default__..._C`(CDO)를 넘겨야 한다
- **`UserDefinedEnum`은 프로퍼티를 하나도 못 읽는다.** `DisplayNameMap`, `Names`, `NamesAndValues`, `EnumDisplayNameFn`, `CppForm` 전부 거부된다
- **`DataTableTools.get_schema`는 enum 선언 순서를 준다.** 1단계 기록의 "`E_ItemNature`는 MCP로 못 읽는다"가 이 경로에서는 틀렸다
- **`find_nodes`의 `title`은 짧은 부분 문자열로 걸어야 한다.** `"Refresh Held Item"`은 빈 배열, `"Refresh"`는 잡힌다
- **다른 BP의 함수를 부르는 노드의 `type_id`는 `Class|<BP>|<Func>`다.** `find_node_types`가 그 형식을 목록에서 빠뜨리는데도 그게 작동하는 형식이다
- **`Utilities|IsValid`는 `declaring_class`를 무엇으로 주든 항상 매크로로 해석된다**
- **`Utilities|Enum|Equal(Enum)`은 Wildcard 핀으로 생성된다.** 한쪽을 연결해야 타입이 해소되므로 **리터럴은 연결 뒤에 넣어야 한다**
- **`find_node_types`를 `E_ItemNature`로 거르면 `Equal(Enum)`이 안 나온다.** `Equal`로 걸러야 나온다
- **이 툴셋에 블루프린트 변수의 타입을 읽는 도구가 없다.** `get_node_type_pins`로 노드 핀을 통해 우회해야 한다
- **`get_variable_instance_editable`이 없다**
- **`get_node_type_pins`가 존재하지 않는 노드의 `refPath`와 `position`을 돌려준다.** 핀 정보는 정확하지만 그 refPath로 노드를 지목하면 안 된다
- **쓰기 툴의 반환값이 일관되지 않다.** `add_variable`·`set_variable_instance_editable`·`compile_blueprint`는 성공에 `null`, `set_properties`·`save_assets`는 `true`
- **연결된 핀도 `value` 필드에 옛 리터럴을 그대로 들고 있다.** `Scale`이 `TextScale`에 연결됐는데도 `val=1.000000`으로 읽힌다. **`value`만 보고 감사하면 틀린 결론에 간다 — `connected_pins`를 봐야 한다**

**설계상 남는 것**

- **`HeldItemSlot` 변수가 죽어 있다.** 이 설계에서 안 쓴다. 남겨두면 나중에 누가 "손에 든 것"의 출처로 착각할 수 있다
- **`FoundSlotIndex` 변수도 이제 읽는 곳이 없다.** getter 노드는 명령 22에서 지웠지만 변수는 남았다
- **`HeldItemMesh`의 스케일이 컴포넌트에 있다.** 아이템마다 크기가 달라야 하면 `S_ItemDef`로 옮겨야 한다. 지금은 셋 다 100cm 기본 도형이라 하나로 맞는다
- **`displayName`이 영어다.** 이제 화면에 뜬다. `Text`(NSLOCTEXT) 타입이라 경로는 열려 있다
- **`[E] Use`도 영어다.** `MakeLiteralString`의 값 하나만 바꾸면 되지만, 폰트에 한글 글리프가 없으면 게임 화면에서도 깨질 수 있다. HUD 폰트는 터미널 폰트와 다르므로 확인해봐야 안다
- **캐스트 실패 프레임에 인벤토리 바가 통째로 사라진다.** 빈 테두리라도 그리는 대안을 안 골랐다
- **`double` → `float` 축소 변환이 `Scale` 핀 넷에 새로 생겼다.** 경고 없이 컴파일됐고 이 그래프의 모든 `ScreenX/Y/W/H`가 이미 같은 상태다
- **`BP_ThirdPersonHUD`가 값 하나(`SelectedSlot` `0`→`1`)를 바꿨는데 파일이 437바이트 줄었다.** `145,593` → `145,156`. 터미널도 설명을 안 붙였고 여기서도 붙이지 않는다
- **명령 15 때 출처 불명의 HUD 컴파일이 하나 있었다.** `02.29.16`과 `02.47.58` 사이. 경고·에러는 없었다

**절차상 관찰**

- **명령 15가 실행되지 않았는데 명령 14의 결과가 다시 붙여졌다.** 디스크 크기·mtime·`DrawRect_9.then`이 여전히 미연결이라는 것으로 잡았다. **MCP 응답이 아니라 실제 상태를 다시 읽는 습관이 값을 한 사례다.** 붙여넣기만 믿었으면 없는 작업을 있다고 판단하고 다음 단계로 갔을 것이다
- **명령 10~16의 터미널 출력이 전부 화면 폭에서 잘렸다.** 매번 AI가 MCP로 5~10회 더 읽어 메웠다. 명령 17부터 파일로 받자 그 비용이 3회로 줄었고 잘림이 사라졌다
- **`Saved/`는 `.gitignore`의 67행 `Saved/*`에 걸린다.** 처음에 거기 쓰라고 낸 명령이 틀렸다. 사용자가 `Docs/Terminal-Log/`를 제안해 바로잡았다

### 총평

요청은 세 겹이었다. 하나는 지난 세션이 남긴 명령 10을 실행하는 것, 둘은 "선택하면 손에 들리고 `E`로 쓴다"는 새 요구, 셋은 그것을 눈에 보이게 만드는 HUD다. 셋 다 끝났고 **합격 기준 4개가 전부 통과했다.** 지난 세션 마감 시점의 통과 개수는 0이었다.

이 작업의 실질적 난이도는 블루프린트가 아니었다. 두 가지였다.

**첫째, 사용자의 의도를 잘못 굳혔던 것을 되돌리는 일.** 1단계 사양에는 "`E`로 `Holdable`을 손에 붙이는 토글"이라고 적혀 있었고, AI는 그 문장을 근거로 심문 질문을 만들었다. 사용자가 "E에 대한게 좀 다르게 인식된거 같은데"라고 정정하고서야 **선택 자체가 장착이라는 마인크래프트 모델**이 드러났다. 사양 문서에 적혀 있다는 것이 그것이 옳다는 뜻은 아니다. 그리고 이 정정이 늦었으면 `HeldItemSlot`을 중심으로 토글 상태를 관리하는 구조를 먼저 만들고 나서 버렸을 것이다.

**둘째, `unreal-mcp`의 경계선을 계속 찾는 일.** 이번에도 시간의 상당 부분이 "이 툴로 이게 되나"에 들어갔다. 위 `남는 리스크`에 나열한 13개 항목이 전부 이번 세션에 새로 확인된 것이다. 그중 넷은 **AI가 명령문에 틀리게 쓴 것을 터미널이 실제 핀을 읽어 바로잡은 것**이다 — `IsValid`가 매크로라는 것, `GetTextSize`가 순수 노드라는 것, `Equal(Enum)`이 Wildcard로 생성된다는 것, `SelectedSlot`이라는 이름이 넷인데 둘만 HUD의 것이라는 것.

**AI의 실수가 넷 있었다.**

1. **`GetTextSize`가 exec 핀을 가진다고 단정했다.** 헤더에 `UFUNCTION(BlueprintCallable)`만 있고 `BlueprintPure`가 없는 것을 보고 판단했다. 실제로는 UHT가 `const` + `BlueprintCallable` + 출력 있음 조건에서 자동으로 `BlueprintPure`를 붙인다(`Engine/Source/Programs/Shared/EpicGames.UHT/Types/UhtFunction.cs:707`). **헤더의 지정자만 보고 노드 모양을 단정하면 안 된다.**
2. **보고 파일을 `Saved/`에 쓰라고 했다.** `.gitignore`에 걸려 커밋이 안 되는 자리다.
3. **명령 21에 "13 member variables"라고 써놓고 14개를 나열했다.** 이건 사용자에게 알린 뒤 일부러 고치지 않고 보냈고, 터미널이 잡았다.
4. **`IsValid`를 순수 함수 + `Branch`로 지시했다.** 매크로 자체가 분기다.

넷 중 셋은 터미널이 잡았고, 첫째는 터미널이 잡은 뒤 AI가 엔진 소스로 확인했다. **명령을 쓰는 쪽과 실행하는 쪽이 나뉘어 있는 것이 실제로 검증 장치로 작동했다.** 한 쪽이 다 했으면 넷 다 그대로 들어갔을 것이다.

**터미널의 판단 중 시키지 않았는데 옳았던 것 둘.** `Switch on E_ItemNature`의 핀 이름이 `NewEnumerator0/1/2`로 나오자 추측하지 않고 `K2Node_SwitchEnum.cpp`를 열어 핀 순서가 선언 순서와 같다는 것을 확인했다. 그리고 `SelectedSlot`이라는 이름의 노드 넷 중 둘만 HUD의 것임을 `self` 핀 타입으로 갈라냈다 — 이름으로 지웠으면 초록 테두리와 아이템 이름이 컴파일 에러 없이 조용히 끊겼다.

**작업 방식 하나가 바뀌었다.** 터미널 보고를 화면 붙여넣기에서 `Docs/Terminal-Log/` 파일로 옮겼다. CLAUDE.md가 "터미널 출력은 영어가 원본이다, 실패·경고·어긋난 응답은 그 자리에서 원문을 확보한다"고 요구하는데, 지금까지는 **잘린 조각이 원문 행세를 해왔다.** 이제 3,052줄이 커밋돼 있다.

## AI의 제안

**1. 버리기(`Q`)를 `E` 다음으로 미루자**

> 그래서 제안은 **`E` → PIE로 기준 3·4 확인 → 그 다음 Q**입니다.

사용자가 먼저 꺼낸 기능이지만 순서는 AI가 제안했다. 얻는 것은 `E`가 만드는 것(슬롯 읽기, 변환 지점, 칸 비우기)을 Q가 그대로 재사용한다는 것, 그리고 손에 드는 방식이 정해져야 버릴 때 손을 비우는 처리가 정해진다는 것. 잃는 것은 기능이 하루 늦어지는 것이다.

**2. 터미널 보고를 화면이 아니라 파일로 받자**

> Write the entire report to Saved/report.md as UTF-8 instead of printing it. Print only the file path and a one-line pass/fail.

(경로는 사용자가 `Docs/Terminal-Log/`로 바로잡았다.) 얻는 것은 잘림이 사라지고, 원문이 커밋되고, 붙여넣기 착오가 없어지는 것. 잃는 것은 사용자가 결과를 바로 못 본다는 것 — 파일을 열거나 AI의 요약을 기다려야 한다.

**3. `INVENTORY FULL` Print String을 남기자**

> Do NOT delete or modify K2Node_CallFunction_36, the "INVENTORY FULL" Print String on K2Node_IfThenElse_2's else branch. It is deliberately kept: it is the only feedback the player gets when the inventory is full, and nothing has replaced it yet.

사용자는 "임시 코드 제거"를 승인했을 뿐 어느 것을 남길지 말하지 않았다. 얻는 것은 1단계 사양이 요구한 "가득 찼을 때 안내"가 유지되는 것. 잃는 것은 배포본에 디버그 로그가 하나 남는다는 것이다.

**4. `TextScale`을 하드코딩하지 말고 변수로 빼자**

> **`TextScale` 변수를 새로 만듭니다 (`2.0`).** 하드코딩하지 않는 이유가 있습니다 — **`GetTextSize`의 `Scale`과 `DrawText`의 `Scale`이 어긋나면 중앙 정렬이 틀어집니다.**

사용자는 `2.0`이라는 값만 말했다. 얻는 것은 두 곳이 구조적으로 어긋날 수 없게 되는 것. 잃는 것은 변수가 하나 느는 것이다.

**5. 커밋과 사양 문서를 지금 쓰자**

> **지금**: 커밋 + 사양 문서 (둘 다 5분 안)

사용자가 "확인해볼까"라고 물었을 때 AI가 낸 권고다. 얻는 것은 `.uasset`이 바이너리라 되돌리기가 파일 단위뿐인 상황에서 복구 지점이 생기는 것, 그리고 채팅에만 있던 2단계 사양이 파일로 남는 것. 잃는 것은 작업 흐름이 한 번 끊기는 것이다.

## 다음으로 넘김

**바로 이어서 할 것**

- **버리기(`Q`).** 사용자가 넣기로 한 기능이고 `E`가 끝났으니 순서가 왔다. 설계 근거는 `Docs/Spec/2026-08-29-인벤토리-2단계.md`의 `접어둔 것` 절에 정리돼 있다. 핵심: `BP_ItemPickup`은 `bSimulatePhysics: false`라 **버린 자리에 그대로 뜬다.** 그래서 "버릴 수 있는지 판단"이 실제로 필요하고, 캐릭터 앞에서 아래로 라인트레이스하는 쪽을 권한다. `IA_DropItem` 액션 하나와 `IMC_Inventory`의 `Q` 매핑이 새로 든다. 액터 원점이 메시 중심이라(`z -50 → +50`) 바닥 높이에 그대로 스폰하면 절반이 묻힌다

**결정 필요**

- **`HeldItemSlot`과 `FoundSlotIndex` 변수를 지울 것인가.** 둘 다 이제 읽는 곳이 없다. `FoundSlotIndex`는 습득 때 `Find` 결과를 담는 용도였는데 getter 노드를 명령 22에서 지웠다
- **`displayName`을 한글로 바꿀 것인가.** 이제 게임 화면에 뜬다. `Text`(NSLOCTEXT)라 경로는 열려 있다. 바꾸기 전에 **HUD 폰트에 한글 글리프가 있는지 먼저 봐야 한다** — 터미널 폰트에는 없다는 것이 이번에 로그로 확인됐다
- **`[E] Use` 문구를 한글로 바꿀 것인가.** `MakeLiteralString` 하나만 고치면 된다. 위와 같은 폰트 문제가 걸린다
- **1인칭 피치를 ±60에서 올릴 것인가.** 사용자가 정한 값이 아니다. 2026-08-27 기록에서 이월
- **`Content/Variant_Shooter/`(50개), `Content/Weapons/`(27개), `Content/FirstPerson/`의 미사용 애셋을 남길 것인가 지울 것인가.** `Variant_Shooter/Blueprints/Pickups/ST_WeaponTableRow`와 `DT_WeaponList`가 지금 만든 것과 같은 구조체+DataTable 패턴이라 지우기 전에 볼 이유가 있다

**확인 필요**

- **`Instance Editable` 플래그 다섯 개.** `CachedCharacter`, `HPBarHeight`, `ColorHPBack`, `ColorHPFill`, `TextLineHeight`, `TextScale`. **MCP로 읽는 방법이 없다.** 디테일 패널에서 눈으로 봐야 한다. 안 켜져 있으면 레벨에서 인스턴스별로 조정이 안 된다
- **`INVENTORY FULL` 경로.** 레벨의 `BP_ItemPickup`을 `Alt`+드래그로 하나 더 놓으면 확인된다. 행은 아무거나 상관없다
- **`Lvl_ArenaShooter`가 어떤 GameMode를 쓰는지.** 인벤토리 HUD가 그 레벨에서 안 보일 것으로 예상만 했다. 세 세션째 이월
- **`HandGrip_R` 소켓의 위치·각도.** 지금 아이템 셋이 전부 대칭 도형이라 각도 문제가 안 드러났을 수 있다. 방향이 있는 메시(칼)가 오면 그때 드러난다

**접어둔 것**

- **칼로 가기 전에 카메라 작업을 먼저 한다.** `BP_ShooterCharacter`가 `BP_FirstPersonCharacter`를 상속해 카메라가 `head` 본에 붙기 때문에 손이 안 보인다. 원본 Project ICI는 `캡슐 → Camera → SkeletalMesh` 구조라 이 문제가 없었다
- **전환 스냅 완화** — 요 보간 또는 `SetViewTargetWithBlend`. 2026-08-27 기록에서 이월
- **`ForLoop.FirstIndex`가 빈 값인 이유.** 동작에 지장이 없다. 그 그래프를 다시 편집할 일이 생기면 그때 본다
- **`--append-system-prompt`가 저장소에 없다.** `Editor Preferences → General → Terminal → Startup Commands`의 사용자 설정이라 다른 환경에서는 다시 넣어야 한다. 원문은 `Docs/AI-Log/2026-08-28-inventory-item-data.md`의 `명령` 칸에 있다

**해결되어 목록에서 뺀 것**

- `BP_ThirdPersonCharacter` 자동 재저장 — 2026-08-28에 세 번 반복됐으나 **2026-08-29에는 한 번도 안 일어났다.** 원인은 여전히 모르지만 재발하지 않아 목록에서 뺀다. 다시 나오면 그때 다시 올린다
- `E_ItemNature`의 열거자 인덱스 확인 — `get_schema`로 읽히고 PIE로도 확정됐다
- off-by-one 변환 지점 못 박기 — `SelectedSlot - 1` 한 곳으로 고정했고 사양 문서에 적었다
