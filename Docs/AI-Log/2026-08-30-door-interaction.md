# 2026-08-30

## 작업물

`Print String` 안내 둘을 HUD 좌상단으로 옮기고, 문(`BP_Door`)을 열쇠로 여닫히게 만들고, `F` 습득을 `BPI_Interact` 인터페이스로 이전했다 — 명령 31~38, 커밋 9개.

**소요 시간**: 약 4시간 40분. 근거는 Terminal-Log 파일의 mtime이다 — 명령 31의 보고가 `13:15`, 명령 38의 보고가 `17:35`. 그 앞의 인계 확인·사양 작성과 그 뒤의 PIE 검증·커밋·문서 갱신은 이 구간 밖이다.

## 명령

### 한글

```
작업 준비 드가자
```

```
한글화는 안하고 둘다 영어로 쓰자 미사용에셋은 나중에 쓸 수도 있으니까 남겨놓고 HUD에 뜨게 하자 왼쪽 위정도에 뜨게하면 될거같은데 어떤데
```

```
오케이 그대로 가자
```

```
확인해줘
```

```
결과확인
```

```
다됬어 봐봐
```

(선택지 질문에 대한 답)

```
합격 기준 4개 중 실제로 해본 것은?  →  전부 다 해서 이상없었음
디테일 패널에서 Instance Editable 11개를 눈으로 봤나?  →  이걸 어떻게 확인하는지 좀더 구체적으로 제시
```

```
커밋할까
```

```
갱신하자
```

```
가자
```

```
결과확인
```

```
커밋 할까
```

```
확인해보자
```

(선택지 질문에 대한 답)

```
문 회전을 무엇으로 만들까?  →  MoveComponentTo (권장)
SwingSpeed를 어떻게 처리할까?  →  OverTime = 1 / SwingSpeed (권장)
```

```
결과확인
```

```
36하고하자
```

```
결과 확인좀
```

```
저 Interface 항목이 Outliner에서 어떤걸 선택했을때 나와야 하는거야?
```

```
(스크린샷 2장) 첫번째가 클래스세팅 버튼 눌렀을때고 두번째가 그 클래스세팅에서 Interface관련 add되어있는거 확인한거
```

```
결과확인
```

```
커밋하고 가자
```

```
결과 확인
```

```
BP_ItemPickup에 붙였어 명령다시붙일게
```

```
결과확인
```

```
커밋하고 하자 그리고 지금 작업 좀 오래했는데 작업상태 괜찬나 자체확인 하고
```

```
PIE 결과 이상없음
```

```
결과 확인 후 정리하고 다음 세션 슬슬 준비할까
```

```
PIE 결과 이상 없음 정리하자
```

### English — MCP에 실제로 보낸 명령

사용자가 UE의 Terminal에 붙여 넣은 영어 원문이다. 다듬지 않았다.

**옮기며 넣은 해석 — 사용자가 말하지 않은 것들**

- `"왼쪽 위정도"` → `MessageMargin = 24.0`. 픽셀 값은 AI가 골랐다
- `"HUD에 뜨게 하자"` → 색 `(0, 0.66, 1, 1)`과 지속 `3.0`. 둘 다 기존 `Print String` 노드 `K2Node_CallFunction_36`에서 읽어 옮긴 값이고, 사용자는 색도 시간도 말하지 않았다
- `"HUD에 뜨게 하자"` → **한 번에 하나만 뜨고 새 메시지가 덮어쓴다**는 규칙. 큐도 스택도 안 만든 것은 AI 결정이다
- `"MoveComponentTo (권장)"` → `bEaseIn`/`bEaseOut`을 둘 다 `true`로. 사용자는 이징을 말하지 않았다
- 잠긴 문의 안내 문구 `"DOOR IS LOCKED"` → AI가 지었다
- Cast 실패 가지의 처리(진단 `Print String`을 붙일지, 비워둘지) → 전부 AI가 정했다. `ShowHUDMessage`에는 `"HUD MESSAGE DROPPED"`를 붙였고 `BP_Door`·`BP_ItemPickup`의 `Interact`에서는 비워뒀다
- `TryConsumeSelected`의 `RowName != ""` 검사 → AI가 넣었다
- 모든 노드 좌표와 보고 파일 이름 → AI가 정했다

#### 명령 31

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD, add five variables and one
function. Do NOT touch the EventGraph in this command - the drawing block is the
next command. Do NOT call AssetTools.is_dirty.

PRE-FLIGHT. Report the results. Stop if either check fails:
- BlueprintTools.list_variables on BP_ThirdPersonHUD must return exactly these 13
  names: SlotCount, SlotSize, SlotGap, BottomMargin, BorderThickness, ColorIdle,
  ColorSelected, CachedCharacter, HPBarHeight, ColorHPBack, ColorHPFill,
  TextLineHeight, TextScale.
  If any variable whose name starts with "Message" or "ColorMessage" already
  exists, STOP and report. Do not overwrite it.
- BlueprintTools.list_functions on BP_ThirdPersonHUD must not contain
  "ShowMessage".

1. Add these five variables:

   name               type          default value                instance editable
   MessageText        String        (empty string)               OFF
   MessageExpireTime  Float         0.0                          OFF
   ColorMessage       LinearColor   (R=0.0,G=0.66,B=1.0,A=1.0)   ON
   MessageMargin      Float         24.0                         ON
   MessageDuration    Float         3.0                          ON

   For ColorMessage, read how the existing ColorIdle variable is declared first
   and mirror it exactly. LinearColor is a struct, so add_struct_variable is
   likely the right tool, not add_variable.

   MessageText and MessageExpireTime are runtime state, not tuning knobs. Leave
   their instance editable flag OFF. Do not turn it on.

   Note: there is no get_variable_instance_editable tool on this build, only the
   setter. Do NOT claim in the report that you verified the instance editable
   flags by reading them back. Report only which set_variable_instance_editable
   calls you made and whether each returned without raising.

2. Add a function graph named ShowMessage with one input parameter:
   Message, type String. No output parameters.

   Body - exactly this and nothing more:

     ShowMessage (entry, Message)
       -> Set MessageText        , value = Message
       -> Set MessageExpireTime  , value = Add( GetTimeSeconds , MessageDuration )

   The Add node is type_id  Utilities|Operators|Add
   The time node is type_id Utilities|Time|GetTimeSeconds
   Its WorldContextObject pin is hidden in Blueprints; leave it alone.

   Do NOT add a Branch, a Timer, a Delay, a Print String, or a Timeline.

3. Compile BP_ThirdPersonHUD and save it.

Write the report to Docs/Terminal-Log/2026-08-30-31-hud-message-vars.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- the pre-flight list_variables and list_functions results, verbatim
- BlueprintTools.list_variables on BP_ThirdPersonHUD AFTER the change, the
  complete list read back from the saved asset. It must be 18 names.
- for each of the five new variables, its type and its default value as READ BACK
  from get_default_object, not as requested
- the complete node inventory of the ShowMessage graph after building it: every
  node's refPath and type_id. If there are more nodes than the ones listed in
  step 2, list the extras and say which tool created them
- the node count of BP_ThirdPersonHUD:EventGraph before and after this command,
  to confirm it was not modified
- the compile result of BP_ThirdPersonHUD
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

#### 명령 32

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD, EventGraph, add the block that
draws the message. Nine new nodes and one rewire. Do NOT call AssetTools.is_dirty.

DO NOT USE write_graph_dsl ON THIS GRAPH. Use create_node / connect_pins /
break_pins / set_pin_value only. This project has recorded twice that
read_graph_dsl silently drops exec continuations on this EventGraph, so a
read -> write round trip would destroy existing wiring.

PRE-FLIGHT. Report the results. Stop if any check fails:
- find_nodes on BP_ThirdPersonHUD:EventGraph with an empty title returns 107 nodes.
- K2Node_MacroInstance_2 has type_id  Utilities|IsValid
  Its output pin index 0 is named "Is Valid" and is connected to
  K2Node_MacroInstance_0 input pin index 0.
- K2Node_MacroInstance_0 has type_id  Utilities|FlowControl|ForLoop
  Its input pin index 0 ("execute") currently has TWO incoming connections:
  K2Node_MacroInstance_2 [out 0] and K2Node_VariableSet_0 [out 0].
  The K2Node_VariableSet_0 one must survive this command untouched.
- BP_ThirdPersonHUD has the variables MessageText, MessageExpireTime,
  ColorMessage, MessageMargin, MessageDuration, TextScale.

1. Create these nine nodes. Place them at y = -1600, x from 1200 to 2600.
   Before creating them, report the position of every existing EventGraph node
   whose position is within 400 units of that band; if any exists, move the new
   nodes to y = -2200 instead and say so.

   a. Utilities|Time|GetTimeSeconds
   b. Get MessageExpireTime
   c. Utilities|Operators|Less(<)          A <- (a), B <- (b)
   d. Utilities|FlowControl|Branch         Condition <- (c)
   e. HUD|DrawText
   f. Get MessageText
   g. Get ColorMessage
   h. Get MessageMargin
   i. Get TextScale

   Wire HUD|DrawText (e) by pin name, not by index alone:
     Text          <- (f) Get MessageText
     TextColor     <- (g) Get ColorMessage
     ScreenX       <- (h) Get MessageMargin
     ScreenY       <- (h) Get MessageMargin      <- the SAME getter node, both pins
     Font          -> leave unconnected, leave its value alone
     Scale         <- (i) Get TextScale
     bScalePosition-> leave at false, do not touch
     self          -> leave unconnected

   Create exactly one Get node per variable. MessageMargin feeds two input pins
   from one output pin - do not create a second getter for it.

2. Rewire, in this order:

   a. break_pins  K2Node_MacroInstance_2 [out 0, "Is Valid"]
               -> K2Node_MacroInstance_0 [in 0, "execute"]
   b. connect    K2Node_MacroInstance_2 [out 0, "Is Valid"]  -> Branch (d) execute
   c. connect    Branch (d) "True"   -> DrawText (e) execute
   d. connect    DrawText (e) "then" -> K2Node_MacroInstance_0 [in 0, "execute"]
   e. connect    Branch (d) "False"  -> K2Node_MacroInstance_0 [in 0, "execute"]

   Steps d and e both land on the same exec input. That is intentional and legal -
   that pin already carries two incoming connections today.

   Do not touch any other pin in this graph. In particular do not touch the
   K2Node_VariableSet_0 -> K2Node_MacroInstance_0 connection.

3. Compile BP_ThirdPersonHUD and save it.

Write the report to Docs/Terminal-Log/2026-08-30-32-hud-message-draw.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight check and its result
- the refPath, type_id and position of each of the nine new nodes
- the complete input and output pin connection list of the new Branch and the
  new DrawText, read back with get_node_infos after the wiring
- the complete incoming connection list of K2Node_MacroInstance_0 [in 0] after
  the rewire. It must be THREE connections: Branch False, DrawText then, and the
  untouched K2Node_VariableSet_0.
- confirmation that K2Node_MacroInstance_2 [out 0] now goes to the Branch and to
  nothing else
- the EventGraph node count after the change. It must be 116.
- the compile result of BP_ThirdPersonHUD
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

#### 명령 33

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, add the function
ShowHUDMessage and replace the two Print String nodes with calls to it.
Do NOT call AssetTools.is_dirty.

DO NOT USE write_graph_dsl ON BP_ThirdPersonCharacter:EventGraph. This project has
recorded that read_graph_dsl returns a lossy script for that graph - the
IA_Interact, IA_UseItem and IA_DropItem events read back with no exec bodies at
all even though they drive real chains. A read -> write round trip would destroy
them. Use create_node / connect_pins / break_pins / delete_node / set_pin_value.
The NEW ShowHUDMessage function graph is exempt - DSL is fine there, it starts
empty.

PRE-FLIGHT. Report every result. Stop where told:

 P1. find_nodes on BP_ThirdPersonCharacter:EventGraph with title "Print" returns
     exactly two nodes: K2Node_CallFunction_36 and K2Node_CallFunction_8.
     Note: title "Print String" returns an empty array on this build - use "Print".
 P2. K2Node_CallFunction_36 is Development|PrintString at (320, 980),
     InString "INVENTORY FULL", execute <- K2Node_IfThenElse_2 [out 1],
     then -> nothing.
 P3. K2Node_CallFunction_8 is Development|PrintString at (400, 3600),
     InString "CANNOT DROP HERE", execute <- K2Node_IfThenElse_6 [out 1],
     then -> nothing.
 P4. Record the total node count of BP_ThirdPersonCharacter:EventGraph.
 P5. list_functions on BP_ThirdPersonCharacter must not contain "ShowHUDMessage".

1. Add a function graph on BP_ThirdPersonCharacter named ShowHUDMessage, with one
   input parameter: Message, type String. No output parameters.

   Body:
     Entry(Message)
       -> Cast to BP_ThirdPersonHUD
            Object <- HUD|GetHUD  <- Game|GetPlayerController (PlayerIndex 0)
            success exec -> Class|BPThirdPersonHUD|ShowMessage
                              target  <- the cast's As BP_ThirdPersonHUD pin
                              Message <- the entry's Message pin
            failure exec -> Development|PrintString , InString "HUD MESSAGE DROPPED"
                              leave its other pins at their defaults

   Node type_ids, all confirmed to resolve in this Blueprint:
     Game|GetPlayerController
     HUD|GetHUD
     Utilities|Casting|CastToBP_ThirdPersonHUD
     Development|PrintString

   Read the cast node's exec pin names with get_node_infos before wiring rather
   than assuming them.

   The failure Print String is deliberate. It is a developer diagnostic, not
   player feedback: if the level's GameMode uses a HUD class that is not
   BP_ThirdPersonHUD, every message would otherwise vanish with no trace.

2. STOP CHECK - do this after step 1's graph exists and BP_ThirdPersonHUD's
   function must be reachable:

   Run find_node_types on the ShowHUDMessage graph with type_id_filter
   "BPThirdPersonHUD" and empty context_pins.

   As of right now, from BP_ThirdPersonCharacter, that filter returns 28 entries
   which are ONLY the accessors of the 13 OLD BP_ThirdPersonHUD variables plus
   two component accessors. Class|BPThirdPersonHUD|ShowMessage is NOT among them,
   and neither are the five Message* variable accessors. The same filter run
   inside BP_ThirdPersonHUD's own EventGraph does return CallFunction|ShowMessage,
   so the function exists.

   If Class|BPThirdPersonHUD|ShowMessage is still absent, try refreshing: compile
   BP_ThirdPersonHUD, then compile BP_ThirdPersonCharacter, then re-run the
   filter.

   If it is STILL absent after that, STOP. Create nothing further, delete nothing,
   and write the report saying so, quoting the full filter output both times.
   Do not substitute a different call, do not use a raw function-name string, and
   do not leave a half-built graph - if you already created nodes in step 1,
   leave them but say exactly what exists.

3. Only if step 2 found the node. Replace the two Print Strings, one at a time,
   verifying between them:

   3a. Create Class|BPThirdPersonHUD|ShowHUDMessage - no. Create
       CallFunction|ShowHUDMessage (a self call, the function you just made) at
       (320, 1120). Set its Message pin to the literal string  INVENTORY FULL
       Connect K2Node_IfThenElse_2 [out 1] -> the new node's execute pin.
       Then delete_node K2Node_CallFunction_36.
       Read back: K2Node_IfThenElse_2 [out 1] must now go to the new node and to
       nothing else.

   3b. Create CallFunction|ShowHUDMessage at (400, 3740). Set its Message pin to
       the literal string  CANNOT DROP HERE
       Connect K2Node_IfThenElse_6 [out 1] -> the new node's execute pin.
       Then delete_node K2Node_CallFunction_8.
       Read back: K2Node_IfThenElse_6 [out 1] must now go to the new node and to
       nothing else.

   Copy the two strings exactly as written above, in capitals, one space between
   the words. They are the strings the old nodes carried.

   Touch nothing else in this EventGraph.

4. Compile BP_ThirdPersonCharacter and save it.

Write the report to Docs/Terminal-Log/2026-08-30-33-hud-message-calls.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight check and its result
- the full output of the step 2 filter, before and after any refresh attempt,
  and whether Class|BPThirdPersonHUD|ShowMessage appeared
- the complete node inventory of the ShowHUDMessage graph - refPath and type_id
  for every node - plus its full pin connection list
- for each of 3a and 3b: the read-back of the driving Branch's [out 1] pin after
  the swap, and confirmation the Print String node is gone
- find_nodes with title "Print" on BP_ThirdPersonCharacter:EventGraph after the
  work. It must return an EMPTY array.
- the EventGraph node count before and after. Two nodes added and two removed, so
  it must be unchanged from P4.
- the compile result of BP_ThirdPersonCharacter
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

**명령 33의 3a 첫 줄에 자기정정이 섞여 나갔다.** `Create Class|BPThirdPersonHUD|ShowHUDMessage - no. Create CallFunction|ShowHUDMessage ...` — 초안을 고치다 지우지 않은 흔적이다. 사용자에게 고쳐도 되고 그대로 둬도 뜻은 통한다고 말했고, 실제로 그대로 나갔다. 터미널은 뜻을 정확히 읽었다.

#### 명령 34

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, add two function graphs:
TryAddItem and TryConsumeSelected. Nothing calls them yet - that is commands 36
and 37. Do NOT touch BP_ThirdPersonCharacter:EventGraph in this command.
Do NOT call AssetTools.is_dirty.

DSL is allowed on these two NEW graphs. Do NOT use write_graph_dsl on the
EventGraph or on RefreshHeldItem.

PRE-FLIGHT. Report every result. Stop if any fails:
 P1. list_functions on BP_ThirdPersonCharacter returns exactly:
     UserConstructionScript, Move, Aim, ToggleCameraView, RefreshHeldItem,
     ShowHUDMessage, CanJumpInternal
     Neither TryAddItem nor TryConsumeSelected may already exist.
 P2. list_variables returns 11 names including InventorySlots (Array of Names),
     SelectedSlot (Integer) and FoundSlotIndex (Integer).
 P3. Record the node count of BP_ThirdPersonCharacter:EventGraph. It must be
     unchanged at the end.

1. Function TryAddItem
   input  : RowName , type Name
   output : Success , type Boolean

   Body:
     Entry(RowName)
       -> Set FoundSlotIndex = Utilities|Array|FindItem( InventorySlots , "" )
            leave FindItem's ItemToFind pin UNCONNECTED at its default empty Name.
            That empty Name is what "an empty slot" means here.
       -> Branch , Condition = ( FoundSlotIndex >= 0 )
            true  -> Utilities|Array|SetArrayElem
                       TargetArray = InventorySlots (a Get of the member array)
                       Index       = FoundSlotIndex
                       Item        = the entry's RowName
                       bSizeToFit  = false
                  -> CallFunction|RefreshHeldItem
                  -> the Return node
            false -> CallFunction|ShowHUDMessage , Message = "INVENTORY FULL"
                  -> the Return node
       Return node: Success <- the SAME >= node that feeds the Branch condition.
       Do not create a second comparison and do not add a bool variable.

   This is the existing F chain's middle section, moved into a function. Read
   K2Node_CallArrayFunction_2 (FindItem), K2Node_VariableSet_1 (Set
   FoundSlotIndex), K2Node_PromotableOperator_5 (>=) and K2Node_CallArrayFunction_3
   (SetArrayElem) in the EventGraph FIRST and mirror their pin values exactly.
   Do not modify those nodes - read only.

2. Function TryConsumeSelected
   input  : RowName , type Name
   output : Success , type Boolean

   Body:
     Entry(RowName)
       -> Branch , Condition = Success (below)
            true -> Utilities|Array|SetArrayElem
                      TargetArray = InventorySlots
                      Index       = SelectedSlot - 1
                      Item        = an empty Name (leave the pin at its default)
                      bSizeToFit  = false
                 -> CallFunction|RefreshHeldItem
                 -> the Return node
            false -> the Return node
       Return node: Success <- the same AND node that feeds the Branch condition.

     Success = Math|Boolean|ANDBoolean of
        A : Utilities|Name|Equal(Name)
              A <- Utilities|Array|Get(acopy)( InventorySlots , SelectedSlot - 1 )
              B <- the entry's RowName
        B : Utilities|Name|NotEqual(Name)
              A <- the entry's RowName
              B <- leave UNCONNECTED at its default empty Name

     The NotEqual term is deliberate: without it a door whose RequiredKey was left
     blank would be opened by an empty slot.

     Deliberately NO array bounds check. Array Get out of range does not crash -
     GenericArray_Get in KismetArrayLibrary.cpp logs a warning and returns the
     default, and an empty Name never equals a real row name, so Success is
     already false. A bounds check would add nodes and change nothing.

     "SelectedSlot - 1" appears twice (the Get index and the SetArrayElem index).
     Use ONE subtract node feeding both pins. Do not create two.

   Node type_ids, all confirmed present in this Blueprint:
     Utilities|Array|FindItem        Utilities|Array|SetArrayElem
     Utilities|Array|Get(acopy)      Utilities|FlowControl|Branch
     Utilities|Name|Equal(Name)      Utilities|Name|NotEqual(Name)
     Math|Boolean|ANDBoolean         Math|Integer|integer>=integer
   Promotable operators may read back under a different resolved type_id
   (Utilities|Operators|GreaterEqual(>=) resolves to Math|Integer|integer>=integer).
   Report what they read back as; that is expected, not an error.

3. STOP CHECK. Both functions need a Return node carrying the Success output.
   If add_function_param with an output parameter does not produce a Return node
   in the graph, STOP. Report what the graph contains, do not improvise a
   substitute (no bool member variable, no second function), and leave what you
   built in place.

4. Compile BP_ThirdPersonCharacter and save it.

Write the report to Docs/Terminal-Log/2026-08-30-34-character-item-functions.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight check and its result
- the four EventGraph nodes you read in step 1, with their pin values, and a
  statement that they were not modified
- for EACH function: the complete node inventory (refPath and type_id) and the
  complete pin connection list, read back after building
- confirmation that TryAddItem's Return.Success and its Branch.Condition come
  from the SAME node, and likewise for TryConsumeSelected
- confirmation that TryConsumeSelected uses ONE subtract node feeding two pins
- confirmation that FindItem's ItemToFind and NotEqual's B pin are unconnected
  and hold an empty Name
- the EventGraph node count after the command. It must equal P3.
- list_functions after the change
- the compile result
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

**명령 34의 "all confirmed present in this Blueprint" 목록이 틀렸다.** `Utilities|Name|Equal(Name)` · `Utilities|Name|NotEqual(Name)` · `Math|Integer|integer>=integer` 셋은 기존 노드에서 **되읽은** 이름이지 팔레트에서 **만들 수 있는** 이름이 아니다. 터미널이 `find_node_types`로 확인해 promotable(`Utilities|Operators|Equal(==)` 등)로 만들었고 그것이 요구한 type_id로 굳는 것까지 확인해 요구를 충족시켰다.

#### 명령 35

```
In /Game/Interaction/BP_Door, EventGraph, build the open/close motion as a custom
event named ToggleDoor. NO lock check, NO interface implementation - those are
command 36. Do NOT call AssetTools.is_dirty.

There is NO Timeline in this design. Do not create one. Reason, established by
reading the toolset: a blank Timeline node has only Update / Finished / Direction
outputs, and nothing in this build can author the float track that would carry the
angle - add_node_pin is documented for Switch / Sequence / commutative operators /
Make Array only and takes neither a name nor a type, Components|Timeline|AddInterpFloat
is a runtime UTimelineComponent function rather than editor-time track authoring,
and there is no curve asset and no tool that makes one. Components|MoveComponentTo
does the whole job in one node.

PRE-FLIGHT. Report every result. Stop if any fails:
 P1. BP_Door:EventGraph contains exactly 3 nodes: K2Node_Event_0, K2Node_Event_1,
     K2Node_Event_2. Report each one's type_id.
 P2. list_variables on BP_Door returns exactly:
     bLocked, RequiredKey, bHingeOnRight, OpenAngle, SwingSpeed, bOpen
 P3. The Hinge component's relative transform on the CDO
     (/Game/Interaction/BP_Door.BP_Door_C:Hinge_GEN_VARIABLE) reads
     location (0,0,0), rotation (0,0,0), scale (1,1,1).
     If it does not, STOP - TargetRelativeLocation (0,0,0) would move the hinge.
 P4. list_functions on BP_Door must not already contain ToggleDoor, and
     list_events must not already contain it.

1. Create a custom event named exactly  ToggleDoor  with NO parameters.
   Node type_id: AddEvent|AddCustomEvent...
   Place the block at y = 400, x from -600 to 1400.

2. Create these ten nodes and wire them:

   a. Variables|Default|GetbOpen
   b. Math|Boolean|NOTBoolean          A <- (a)
   c. Set bOpen                        value <- (b)
   d. Variables|Default|GetHinge
   e. Variables|Default|GetOpenAngle
   f. Math|Float|SelectFloat
        A      <- (e) OpenAngle
        B      =  0.0   (leave the pin at its default)
        bPickA <- the "Output_Get" OUTPUT pin of (c), the Set bOpen node.
                  Do NOT create a second GetbOpen node for this.
   g. Math|Rotator|MakeRotator
        Roll  = 0.0   (default)
        Pitch = 0.0   (default)
        Yaw   <- (f)
   h. Variables|Default|GetSwingSpeed
   i. Utilities|Operators|Divide
        A = 1.0   (a literal on the pin)
        B <- (h) SwingSpeed
   j. Components|MoveComponentTo
        Move                       <- exec from (c) Set bOpen "then"
        Stop                       leave unconnected
        Return                     leave unconnected
        Component                  <- (d) Hinge
        TargetRelativeLocation     leave at its default 0,0,0 - do not connect
        TargetRelativeRotation     <- (g)
        bEaseOut                   set to true
        bEaseIn                    set to true
        OverTime                   <- (i)
        bForceShortestRotationPath leave at its default false
        then                       leave unconnected

   Exec chain:  ToggleDoor -> Set bOpen -> MoveComponentTo(Move)

   SelectFloat returns A when bPickA is true, so bOpen true gives OpenAngle and
   bOpen false gives 0. bOpen is set BEFORE the move, so the move uses the new
   value. That ordering is required - do not move the Set after the MoveComponentTo.

   Promotable operators may read back under a resolved type_id
   (Utilities|Operators|Divide is expected to read back as Math|Float|float/float).
   Report what it reads back as; that is expected, not an error.

3. Compile BP_Door and save it.

Write the report to Docs/Terminal-Log/2026-08-30-35-door-toggle.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight check and its result, including the three existing events'
  type_ids and the Hinge transform as read
- the complete node inventory of BP_Door:EventGraph after the work - refPath and
  type_id for every node - and the complete pin connection list of the new nodes
- explicit confirmation that SelectFloat's bPickA comes from the Set bOpen node's
  Output_Get pin and that the graph contains exactly ONE GetbOpen node
- explicit confirmation that MoveComponentTo's TargetRelativeLocation is
  unconnected and still reads 0,0,0, and that bEaseIn and bEaseOut read true
- the EventGraph node count before and after. 3 before, 14 after.
- confirmation that the three pre-existing event nodes were not modified
- the compile result of BP_Door
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up. In particular, if the compiler rejects
  MoveComponentTo for any reason, quote the message verbatim and STOP rather than
  substituting another approach.
```

#### 명령 36

두 번 보냈다. 첫 번째는 P1에서 멈췄고, 사용자가 `BP_Door`에 인터페이스를 손으로 붙인 뒤 **같은 원문을 그대로** 다시 보냈다.

```
In /Game/Interaction/BP_Door, EventGraph, implement the BPI_Interact event and the
lock check. Do NOT call AssetTools.is_dirty. Do NOT use write_graph_dsl on this
graph - it already has wiring from command 35.

PRE-FLIGHT. Report every result. STOP if P1 fails:
 P1. list_events on BP_Door must contain an entry named "Interact".
     If it does not, the BPI_Interact interface has not been added to BP_Door's
     Implemented Interfaces yet. STOP. Create nothing. Report the full list_events
     output so it is clear what is there instead.
     Also report Interact's bIsImplemented value before you touch anything.
 P2. BP_Door:EventGraph has 14 nodes. Report each one's refPath and type_id.
 P3. list_variables on BP_Door returns bLocked, RequiredKey, bHingeOnRight,
     OpenAngle, SwingSpeed, bOpen.
 P4. RequiredKey's default value, read from the CDO. Report the DataTable and
     RowName it holds.
 P5. find_node_types on this graph, empty context_pins, must offer all of:
       Class|BPThirdPersonCharacter|TryConsumeSelected
       Class|BPThirdPersonCharacter|ShowHUDMessage
       CallFunction|ToggleDoor
       Utilities|Struct|BreakDataTableRowHandle
       Utilities|Casting|CastToBP_ThirdPersonCharacter
     If any is missing, STOP and report which.

1. Add the interface event with add_event, event_name "Interact".
   It must come back with an "Interactor" output pin of type Actor. Report its
   pins. If it has no Interactor pin, STOP.
   Place the new block at y = 1200, x from -600 to 1600.

2. Create these nodes and wire them:

   a. Utilities|FlowControl|Branch            <- Branch A, the lock test
        Condition <- a Get of bLocked
        execute   <- the Interact event's exec output
   b. Variables|Default|GetbLocked            (feeds a)
   c. Utilities|Casting|CastToBP_ThirdPersonCharacter
        execute <- Branch A "then"   (bLocked TRUE goes here)
        Object  <- the Interact event's Interactor pin
        CastFailed -> leave UNCONNECTED. This is deliberate, not an oversight.
   d. Variables|Default|GetRequiredKey
   e. Utilities|Struct|BreakDataTableRowHandle
        DataTableRowHandle <- (d)
   f. Class|BPThirdPersonCharacter|TryConsumeSelected
        execute <- (c) cast success exec
        target/self <- (c) the "As BP Third Person Character" data pin
        RowName <- (e) the "RowName" output
   g. Utilities|FlowControl|Branch            <- Branch B, the key test
        execute   <- (f) then
        Condition <- (f) Success
   h. Set bLocked
        execute <- Branch B "then"
        value   = false   (a literal on the pin, not a connection)
   i. CallFunction|ToggleDoor                 <- create ONE of these only
        execute <- BOTH of:  Branch A "else"   (bLocked FALSE, already unlocked)
                        and  (h) Set bLocked "then"
        Two exec outputs into one exec input is intentional and legal.
   j. Class|BPThirdPersonCharacter|ShowHUDMessage
        execute <- Branch B "else"
        target/self <- (c) the "As BP Third Person Character" data pin
        Message = "DOOR IS LOCKED"

   Read each node's pins with get_node_infos before wiring and connect by pin NAME
   resolved to its index, not by assuming an index order. The cast node's exec
   outputs are named "then" and "CastFailed"; its data output name contains
   "BP Third Person Character".

   Create exactly ONE GetbLocked node and ONE ToggleDoor call node.

3. Compile BP_Door and save it.

Write the report to Docs/Terminal-Log/2026-08-30-36-door-interact-lock.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight check and its result, including Interact's bIsImplemented
  before and after, and RequiredKey's DataTable and RowName
- the Interact event node's complete pin list as created
- the complete node inventory of BP_Door:EventGraph after the work and the full
  pin connection list of every node added by this command
- explicit confirmation that the ToggleDoor call node has TWO incoming exec
  connections - Branch A "else" and Set bLocked "then" - and that there is only
  one such node in the graph
- explicit confirmation that the cast node's CastFailed pin is unconnected
- explicit confirmation that Set bLocked's value pin holds the literal false and
  is not connected to anything
- the EventGraph node count before and after. 14 before; report the after count
  and list any node you created beyond the ones named in step 2.
- confirmation that the ToggleDoor block built in command 35 (K2Node_CustomEvent_0
  through K2Node_CallFunction_6) was not modified
- the compile result of BP_Door
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

#### 명령 37

이것도 두 번 보냈다. 첫 번째는 P1에서 멈췄고, 사용자가 `BP_ItemPickup`에 인터페이스를 손으로 붙인 뒤 **같은 원문을 그대로** 다시 보냈다.

```
In /Game/Inventory/BP_ItemPickup, EventGraph, implement the BPI_Interact event.
This command is purely additive - nothing calls Interact yet, so the existing F
pickup chain in BP_ThirdPersonCharacter keeps working exactly as it does now.
Moving that chain over is the NEXT command. Do not touch
BP_ThirdPersonCharacter in this command.

Do NOT call AssetTools.is_dirty. Do NOT use write_graph_dsl.

PRE-FLIGHT. Report every result. STOP if P1 fails:
 P1. list_events on BP_ItemPickup must contain an entry named "Interact".
     If it does not, BPI_Interact has not been added to BP_ItemPickup's
     Implemented Interfaces yet. STOP. Create nothing. Report the full
     list_events output. Note: BlueprintTools has no tool that can add an
     interface - do not try to work around it, it is a hand edit.
     Report Interact's bIsImplemented value before you touch anything.
 P2. BP_ItemPickup:EventGraph has 3 nodes. Report each refPath and type_id.
 P3. list_variables on BP_ItemPickup returns exactly ["ItemRow"].
     Report ItemRow's type and its default value from the CDO.
 P4. find_node_types on this graph, empty context_pins, must offer all of:
       Class|BPThirdPersonCharacter|TryAddItem
       Utilities|Casting|CastToBP_ThirdPersonCharacter
       Utilities|Struct|BreakDataTableRowHandle
       Actor|DestroyActor
     If any is missing, STOP and report which.

1. Add the interface event with add_event, event_name "Interact".
   It must come back with an "Interactor" output pin of type Actor. Report its
   pins. If it has no Interactor pin, STOP.
   Place the new block at y = 600, x from -600 to 1200.

2. Create these six nodes and wire them:

   a. Utilities|Casting|CastToBP_ThirdPersonCharacter
        execute <- the Interact event's exec output
        Object  <- the Interact event's Interactor pin
        CastFailed -> leave UNCONNECTED. Deliberate.
   b. Variables|Default|GetItemRow
   c. Utilities|Struct|BreakDataTableRowHandle
        DataTableRowHandle <- (b)
   d. Class|BPThirdPersonCharacter|TryAddItem
        execute     <- (a) cast success exec
        target/self <- (a) the "As BP Third Person Character" data pin
        RowName     <- (c) the "RowName" output
   e. Utilities|FlowControl|Branch
        execute   <- (d) then
        Condition <- (d) Success
   f. Actor|DestroyActor
        execute <- Branch (e) "then"
        its self / Target pin: leave UNCONNECTED so it destroys THIS actor.
        Read the pin back and confirm it is unconnected. This is the one place
        this command differs from the old F chain, where DestroyActor's target
        was wired to the cast result because the caller was the Character.
        Here the caller is the pickup itself.

   Branch (e) "else" -> leave UNCONNECTED. TryAddItem already shows
   "INVENTORY FULL" from inside itself, so there is nothing to do on failure.

   Read each node's pins with get_node_infos before wiring and connect by pin
   NAME resolved to its index. The cast node's data output name contains
   "BP Third Person Character".

3. Compile BP_ItemPickup and save it.

Write the report to Docs/Terminal-Log/2026-08-30-37-pickup-interact.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight check and its result, including Interact's bIsImplemented
  before and after, and ItemRow's type and CDO default value
- the Interact event node's complete pin list as created
- the complete node inventory of BP_ItemPickup:EventGraph after the work and the
  full pin connection list of every node added
- explicit confirmation that DestroyActor's target pin is UNCONNECTED
- explicit confirmation that the cast's CastFailed pin and Branch's "else" pin
  are both unconnected
- the EventGraph node count before and after. 3 before, 10 after. List any node
  you created beyond the ones named in step 2.
- confirmation that the three pre-existing event stubs were not modified
- confirmation that no call in this command targeted BP_ThirdPersonCharacter
- the compile result of BP_ItemPickup
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

#### 명령 38

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, EventGraph, move the F
interact chain onto the BPI_Interact interface. This DELETES 15 nodes from a chain
that has been working in PIE since 2026-08-28. Build the replacement FIRST, rewire,
verify, and only then delete. Do NOT call AssetTools.is_dirty.

DO NOT USE write_graph_dsl ON THIS GRAPH. read_graph_dsl returns a lossy script for
it - the IA_Interact / IA_UseItem / IA_DropItem events read back with no exec bodies
even though they drive real chains. A round trip would destroy them.
Use create_node / connect_pins / break_pins / delete_node / set_pin_value only.

PRE-FLIGHT. Report every result. STOP if any fails:
 P1. EventGraph node count is 98.
 P2. These 15 nodes exist with these exact type_ids. Report each one's full pin
     connection list BEFORE anything is changed - this is the record that makes
     the deletion reversible by hand if it goes wrong:
       K2Node_DynamicCast_1      Utilities|Casting|CastToBP_ItemPickup
       K2Node_VariableGet_3      |GetItemRow
       K2Node_BreakStruct_1      Utilities|Struct|BreakDataTableRowHandle
       K2Node_VariableGet_5      |GetInventorySlots
       K2Node_CallArrayFunction_2 Utilities|Array|FindItem
       K2Node_VariableSet_1      |SetFoundSlotIndex
       K2Node_VariableGet_8      |GetFoundSlotIndex
       K2Node_PromotableOperator_5 Math|Integer|integer>=integer
       K2Node_IfThenElse_2       Utilities|FlowControl|Branch
       K2Node_CallArrayFunction_3 Utilities|Array|SetArrayElem
       K2Node_VariableGet_6      |GetInventorySlots
       K2Node_VariableGet_9      |GetFoundSlotIndex
       K2Node_CallFunction_18    |RefreshHeldItem
       K2Node_CallFunction_35    Actor|DestroyActor
       K2Node_CallFunction_34    |ShowHUDMessage   (its Message pin reads "INVENTORY FULL")
 P3. K2Node_IfThenElse_1 is Utilities|FlowControl|Branch, its "then" output goes to
     K2Node_DynamicCast_1, and its "else" output goes to nothing.
 P4. K2Node_CallFunction_26 is Collision|BreakHitResult and its output pin named
     "HitActor" goes to K2Node_DynamicCast_1 [in 1].
 P5. find_node_types on this graph, empty context_pins, offers all of:
       Utilities|DoesObjectImplementInterface
       Class|BPIInteract|Interact(Message)
       Variables|Getareferencetoself
       Utilities|FlowControl|Branch
 P6. /Game/Interaction/BPI_Interact exists and its BlueprintType asset tag is
     BPTYPE_Interface.

STAGE 1 - build the replacement. Place at y = -400, x from -900 to 200.
Report the position of any existing node within 400 units of that band first; if
any exists, use y = -900 instead and say so.

   a. Utilities|DoesObjectImplementInterface
        TestObject <- K2Node_CallFunction_26 output pin named "HitActor"
        Interface  = the BPI_Interact interface class.
          Try set_pin_value with "/Game/Interaction/BPI_Interact.BPI_Interact_C".
          Read the pin back. If it does not hold the interface afterwards, try
          "/Game/Interaction/BPI_Interact.BPI_Interact". If neither takes, STOP -
          report both attempts and their read-backs, delete the nodes you created
          in this stage, and change nothing else. Do NOT substitute a Cast node.
   b. Utilities|FlowControl|Branch
        Condition <- (a) ReturnValue
   c. Variables|Getareferencetoself
   d. Class|BPIInteract|Interact(Message)
        execute   <- Branch (b) "then"
        self      <- K2Node_CallFunction_26 "HitActor"   (this pin is the TARGET
                     the message is sent to, not this Blueprint's self)
        Interactor <- (c) the self reference
        then      -> leave unconnected
      Branch (b) "else" -> leave unconnected.

   Do NOT connect stage 1 to K2Node_IfThenElse_1 yet. Compile here and report the
   result. The new block is an island at this point; the old chain still runs.

STAGE 2 - rewire, one call:
   break_pins  K2Node_IfThenElse_1 [out 0 "then"] -> K2Node_DynamicCast_1 [in 0]
   connect     K2Node_IfThenElse_1 [out 0 "then"] -> the Branch (b) execute pin

   Read back and report:
   - K2Node_IfThenElse_1 [out 0] now goes ONLY to (b)
   - K2Node_DynamicCast_1 [in 0] now has NO incoming connection
   Compile and report the result. At this point the 15 old nodes are orphaned but
   still present, and the node count is 102.

STAGE 3 - delete the 15 nodes listed in P2, one delete_node call each, in the
   order listed. After each delete, report the running node count.
   Delete NOTHING else. In particular:
   - do NOT delete the variable FoundSlotIndex. It is still used by the
     TryAddItem function built in command 34.
   - do NOT touch K2Node_CallFunction_26 (BreakHitResult), K2Node_CallFunction_25
     (the line trace), K2Node_IfThenElse_1, or K2Node_EnhancedInputAction_3.
   - do NOT touch the IA_UseItem (E) or IA_DropItem (Q) chains.

STAGE 4 - compile BP_ThirdPersonCharacter and save it.

Write the report to Docs/Terminal-Log/2026-08-30-38-f-chain-to-interface.md
(a repo path - do NOT write under Saved/, it is gitignored).
The report must contain:
- every pre-flight check, and the FULL pin connection list of all 15 doomed nodes
  as read before any change
- the four new nodes' refPaths, type_ids, positions and full pin connection lists
- the Interface pin's read-back value on (a), and which string took
- the stage 2 read-backs named above
- the running node count after each of the 15 deletes, and the final count. It
  must be 87 (98 + 4 - 15).
- find_nodes with title "Print" on this EventGraph after the work. Must be [].
- confirmation that list_variables still contains FoundSlotIndex
- confirmation that K2Node_EnhancedInputAction_1 (IA_UseItem) and
  K2Node_EnhancedInputAction_4 or whichever node drives the Q chain still have
  their exec chains intact - report the first three nodes of each chain
- the compile result at the end of stage 1, stage 2 and stage 4
- the exact English text of every error or warning encountered. Do not translate
  it and do not clean it up.
```

**명령 38의 `K2Node_EnhancedInputAction_1 (IA_UseItem)`이 틀렸다.** 그 노드는 `IA_Move`다. 터미널이 잡아서 진짜 주인(`_2` = IA_UseItem, `_5` = IA_DropItem)을 찾아 확인했다.

## Terminal 결과

### 원문 — English

터미널 보고 전문은 `Docs/Terminal-Log/2026-08-30-31-*.md` 부터 `-38-*.md` 까지 여덟 개 파일에 있다. 여기에는 **판단 근거가 된 줄과, 멈춤·어긋남의 원문만 발췌한다.** 발췌했다는 사실을 밝힌다.

**명령 31 — `is_dirty` 대신 남긴 것**

```
There is no `get_variable_instance_editable` on this build, so **no claim is made here that any
flag was verified.** What follows is only which calls were made and whether each raised.
```

**명령 31 — DSL이 함수 출력 파라미터를 안 낸다 (명령 34의 보고에서)**

```
Worth recording: `read_graph_dsl` on both graphs at this point returned
`(fn TryAddItem (RowName))` and `(fn TryConsumeSelected (RowName))` — **the DSL representation
shows only the input, not the `Success` output.** That is a second instance of the DSL being
lossy on this project's graphs, alongside the EventGraph exec-body loss the command cited.
```

**명령 33 — 팔레트가 낡았다던 내 관찰과 어긋난 결과**

```
The command said the filter "returns 28 entries which are ONLY the accessors of the 13 OLD
BP_ThirdPersonHUD variables plus two component accessors", with `ShowMessage` absent and the
five `Message*` accessors absent.

What was actually observed is 40 entries, containing `ShowMessage` **and** all ten `Message*`
accessors (`Get`/`Set` for `MessageText`, `MessageExpireTime`, `ColorMessage`, `MessageMargin`,
`MessageDuration`). The registry was already current.
```

**명령 34 — 내 명령문의 type_id 목록이 틀렸다는 지적**

```
The four type_ids the command listed as "confirmed present" that are in fact **not creatable**
are `Utilities|Name|Equal(Name)`, `Utilities|Name|NotEqual(Name)` and
`Math|Integer|integer>=integer` — `find_node_types` for `Math|Integer|integer>=integer` returned
`[]`, and the `Utilities|Name|` filter returned only `EnumtoName` and `MakeLiteralName`. They
are read-back names, not palette names.
```

**명령 34 — DSL을 허용했는데 안 쓴 이유**

```
Command 30 established that this DSL's `bind` is textual substitution, not a node reference — a
bound value used twice produced two copies of the whole sub-expression. Using DSL here would
therefore have produced exactly the duplicate comparison and duplicate subtract the command
forbids.
```

**명령 36 — 첫 시도의 멈춤. 전문**

```
# 2026-08-30 — BP_Door Interact + lock check: STOPPED at P1, nothing built

**P1 failed. No node was created, no pin was changed, nothing was compiled or saved.**
`BP_Door:EventGraph` is exactly as command 35 left it — 14 nodes.

`list_events` on BP_Door contains no entry named `Interact`. Per the command's instruction that
means BPI_Interact has not been added to BP_Door's Implemented Interfaces, so the build stopped
before step 1.
```

```
`ObjectTools.get_properties` on the Blueprint:

[2026.08.30-07.37.39:024][915]LogScript: Warning: GetObjectProperties on
'/Game/Interaction/BP_Door.Default__BP_Door_C' (BP_Door_C): the following properties could not
be read: ImplementedInterfaces
```

```
**No tool on this build can add it.** The full 54-tool `BlueprintTools` inventory was searched
for any name containing `interface` or `implement`; there are none. There is `get_parent` /
`set_parent` for the parent class, but the implemented-interface array is separate from the
parent class and is not exposed. `retarget_node_class` only swaps class references on existing
cast/call/event nodes. So this is a hand edit, like the Expose on Spawn flag in command 23 and
the Blueprint Interface asset creation in command 30.
```

```
**The hand edit:** open BP_Door, Class Settings, Interfaces → Implemented Interfaces → Add →
BPI_Interact, then compile and save. `Interact` should then appear in `list_events` with
`bIsImplemented: false`, and re-running this command will find it. *(Not verified — this UI path
was not walked in this session, and per project rules I am flagging it as unconfirmed rather
than presenting it as a checked procedure.)*
```

**명령 36 — 부른 쪽과 구현한 쪽을 구분한 것**

```
`find_node_types` with filter `"BPIInteract"`:

["Class|BPIInteract|Interact", "Class|BPIInteract|Interact(Message)"]

These two **do** exist — but they are the *caller* side. ... Their presence proves the
BPI_Interact asset is loaded and its function is registered; it does **not** mean BP_Door
implements the interface. Only the implementation side is missing.
```

**명령 36 — 노드가 저절로 움직였다는 관찰**

```
**One discrepancy, in position only.** `K2Node_VariableSet_0` (`|SetbOpen`) reads **(0, 272)**;
command 35's report recorded it at **(-40, 400)**.

This command issued no `set_node_position` and no `arrange_nodes`, and made no call naming that
node. The change is cosmetic — no connection, pin value or type differs — but it is a real
difference from the last recorded state and is not explained by anything this command did.
```

**명령 37 — 첫 시도의 멈춤. 발췌**

```
# 2026-08-30 — BP_ItemPickup Interact: STOPPED at P1, nothing built

**P1 failed. No node was created, no pin was changed, nothing was compiled or saved.**
`BP_ItemPickup:EventGraph` is unchanged at 3 nodes.
```

**명령 38 — 인터페이스 클래스 핀이 먹혔다**

```
`set_pin_value` on `K2Node_CallFunction_44` input [1] `Interface` with
`"/Game/Interaction/BPI_Interact.BPI_Interact_C"` did not raise, and the read-back immediately
after was:

[1, "Interface", "Interface Interface", "/Game/Interaction/BPI_Interact.BPI_Interact_C"]

**The `_C` class path took on the first attempt.**
```

**명령 38 — 3단계 삭제가 안전했다는 근거**

```
No error and no warning followed it. **Compiled clean** — which matters here, because deleting a
`SetFoundSlotIndex` node and its readers is exactly the edit that would raise "variable not
found" if something still referenced them.
```

**명령 38 — 내 명령문의 노드 지목이 틀렸다는 지적**

```
The command asked about `K2Node_EnhancedInputAction_1`; that node is **IA_Move**, not IA_UseItem.
The actual owners are `K2Node_EnhancedInputAction_2` (IA_UseItem / E) and
`K2Node_EnhancedInputAction_5` (IA_DropItem / Q).
```

**세션 전체 로그 스캔 (자체 확인 중 `LogsToolset.GetLogEntries`로 직접 읽음)**

`LogBlueprint` 카테고리의 이번 세션 컴파일 30건 중 **경고·에러 0건.** 남은 경고는 둘뿐이고 만든 것과 무관하다:

```
[2026.08.30-08.18.53:546][958]LogJson: Warning: Property "OnActorBeginOverlap" type
FActorBeginOverlapSignature unhandled during Json schema generation.
```

```
[2026.08.30-07.59.48:279][189]LogEditorClassViewer: Warning: Class
/Script/ModelViewViewModelBlueprint.MVVMK2Node_LoadSoftInputAction has parent
/Script/ModelViewViewModelBlueprint.MVVMK2Node_LoadSoftResource, but this parent is not found.
The Class will not be shown in ClassViewer.
```

**세션이 하지 않은 컴파일 두 건**

```
[2026.08.30-04.52.27:199][949]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.08.30-04.52.27:253][949]LogBlueprint: Compiling Blueprint '/Game/LevelPrototyping/Interactable/Door/BP_DoorFrame.BP_DoorFrame'
```

```
[2026.08.30-07.49.47:795][181]LogBlueprint: Compiling Blueprint '/Game/LevelPrototyping/Interactable/Door/BP_DoorFrame.BP_DoorFrame'
```

### 요약 — 한글

**`BP_ThirdPersonHUD`** — 변수 5개(`MessageText` · `MessageExpireTime` · `ColorMessage` · `MessageMargin` · `MessageDuration`), 함수 `ShowMessage(Message: String)` 6노드, `Receive Draw HUD`에 그리기 블록 9노드. EventGraph 107 → 116.

**`BP_ThirdPersonCharacter`** — 함수 `ShowHUDMessage(Message: String)` 6노드, `TryAddItem(RowName: Name) → Success` 12노드, `TryConsumeSelected(RowName: Name) → Success` 13노드. EventGraph에서 `Development|PrintString` 두 개를 `ShowHUDMessage` 호출로 교체(개수 98 유지), 이어서 `F` 습득 로직 15노드를 지우고 인터페이스 블록 4노드로 교체(98 → 87).

**`BP_Door`** — 커스텀 이벤트 `ToggleDoor` + `MoveComponentTo` 블록 11노드, 인터페이스 이벤트 `Interact` + 잠금 판정 11노드. EventGraph 3 → 14 → 25. `BPI_Interact`를 사용자가 손으로 부착.

**`BP_ItemPickup`** — 인터페이스 이벤트 `Interact` + `TryAddItem` 호출 블록 7노드. EventGraph 3 → 10. `BPI_Interact`를 사용자가 손으로 부착.

**타임라인을 안 만들었다.** 명령 35가 사양의 타임라인 대신 `Components|MoveComponentTo` 한 노드로 갔다.

## 분석

### 무엇을 만들었나

**HUD 안내 메시지 — `BP_ThirdPersonHUD`**

| 변수 | 타입 | 기본값 | Instance Editable |
|---|---|---|---|
| `MessageText` | String | `""` | OFF (런타임 상태) |
| `MessageExpireTime` | Float | `0.0` | OFF (런타임 상태) |
| `ColorMessage` | LinearColor | `(0, 0.66, 1, 1)` | ON |
| `MessageMargin` | Float | `24.0` | ON |
| `MessageDuration` | Float | `3.0` | ON |

색과 지속시간은 기존 `Print String` 노드 `K2Node_CallFunction_36`에서 읽어 그대로 옮긴 값이다 — `(R=0.000000,G=0.660000,B=1.000000,A=1.000000)` / `3.0`.

함수 `ShowMessage(Message: String)`: `Set MessageText = Message` → `Set MessageExpireTime = GetTimeSeconds + MessageDuration`. 타이머를 안 쓴다.

`Receive Draw HUD`의 그리기 블록: `IsValid`의 `Is Valid` 핀과 `ForLoop` 사이에 끼웠다. `Branch(GetTimeSeconds < MessageExpireTime)` → 참이면 `DrawText(MessageText, ColorMessage, MessageMargin, MessageMargin, Font=None, Scale=TextScale)`. 두 갈래가 `ForLoop`의 같은 exec 입력에 모인다 — 그 핀은 원래도 둘을 받고 있었다.

**캐릭터 — `BP_ThirdPersonCharacter`**

`ShowHUDMessage(Message: String)`: `GetPlayerController(0)` → `GetHUD` → `Cast to BP_ThirdPersonHUD` → `ShowMessage`. Cast 실패 가지에 `Print String "HUD MESSAGE DROPPED"`.

`TryAddItem(RowName: Name) → Success: bool`:
```
FoundSlotIndex = FindItem(InventorySlots, "")
Branch(FoundSlotIndex >= 0)
  true  → SetArrayElem(InventorySlots, FoundSlotIndex, RowName) → RefreshHeldItem
  false → ShowHUDMessage("INVENTORY FULL")
Return Success = 같은 >= 노드
```

`TryConsumeSelected(RowName: Name) → Success: bool`:
```
Success = (InventorySlots[SelectedSlot-1] == RowName) AND (RowName != "")
Branch(Success)
  true → SetArrayElem(InventorySlots, SelectedSlot-1, "") → RefreshHeldItem
Return Success = 같은 AND 노드
```

`F` 체인의 새 꼬리:
```
LineTraceByChannel → Branch(명중)
  true → DoesObjectImplementInterface(HitActor, "/Game/Interaction/BPI_Interact.BPI_Interact_C")
       → Branch
           true → Interact(Message)  self ← HitActor, Interactor ← Self
```

**문 — `BP_Door`**

`ToggleDoor` (커스텀 이벤트, 함수가 아님):
```
Set bOpen = NOT(bOpen)
MoveComponentTo(
  Component = Hinge,
  TargetRelativeLocation = (0,0,0),
  TargetRelativeRotation = MakeRotator(0, 0, SelectFloat(OpenAngle, 0.0, bOpen)),
  bEaseIn = true, bEaseOut = true,
  OverTime = 1.0 / SwingSpeed,
  bForceShortestRotationPath = false)
```

`Interact(Interactor)`:
```
Branch A (bLocked?)
  false → ToggleDoor
  true  → Cast to BP_ThirdPersonCharacter
            CastFailed → 아무것도 안 함
            then → TryConsumeSelected(Break(RequiredKey).RowName)
                     → Branch B (Success?)
                         true  → Set bLocked = false → ToggleDoor
                         false → ShowHUDMessage("DOOR IS LOCKED")
```

`RequiredKey` 기본값은 `DT_Items` / `Key_Stage1`, `bLocked` `true`, `bOpen` `false`.

**픽업 — `BP_ItemPickup`**

`Interact(Interactor)`:
```
Cast to BP_ThirdPersonCharacter
  CastFailed → 아무것도 안 함
  then → TryAddItem(Break(ItemRow).RowName)
           → Branch(Success)
               true  → DestroyActor (self, 핀 미연결)
               false → 아무것도 안 함
```

`ItemRow`의 CDO 기본값은 `DT_Items` / `rowName: "None"`.

### 기술적으로 맞게 짚은 부분

**HUD 메시지에 타이머를 안 쓴 것.** `AHUD::ReceiveDrawHUD`는 매 프레임 돈다. 만료 시각을 저장하고 `GetTimeSeconds < MessageExpireTime`을 비교하면 타이머 노드도, 델리게이트도, 정리 코드도 필요 없다. 타이머를 쓰면 `EndPlay`에서 지워야 할 것이 생긴다.

**`Set` 노드의 `Output_Get` 핀을 쓴 것.** `K2Node_VariableSet`은 방금 쓴 값을 그대로 내주는 출력 핀을 가진다. `BP_Door`의 `ToggleDoor`가 `bOpen`을 뒤집고 그 새 값으로 목표 각도를 고를 때 이 핀을 썼다. 게터를 하나 더 만들면 값이 같으리라는 보장은 있지만 노드가 늘고, 나중에 사이에 뭔가 끼면 조용히 틀려진다.

**`TryConsumeSelected`에 범위 검사를 안 넣은 것.** 엔진 소스를 읽고 결정했다 — `KismetArrayLibrary.cpp`의 `GenericArray_Get`은 범위를 벗어나면 크래시하지 않고 경고를 남긴 뒤 기본값(빈 `Name`)을 준다. 빈 `Name`은 어떤 열쇠 행 이름과도 같지 않으므로 `Success`가 이미 `false`다. 범위 검사는 노드만 늘리고 결과를 안 바꾼다.

**`SwingSpeed`를 나눈 것.** 사양은 `SwingSpeed`를 "타임라인 Play Rate"로 정의했다. `MoveComponentTo`의 `OverTime`은 초 단위라 의미가 뒤집힌다 — 그대로 꽂았으면 "속도"라는 이름의 변수가 클수록 문이 느려진다. `1.0 / SwingSpeed`로 나누면 이름이 계속 참이고 기본값 `1.0`은 여전히 1초다. 나누기 노드 하나로 이름이 거짓말하는 것을 막았다.

**손대지 않은 것이 정답이었던 것 — `FoundSlotIndex`.** 명령 38이 `SetFoundSlotIndex`와 그 독자 셋을 지웠지만 변수 자체는 안 지웠다. `TryAddItem`이 여전히 쓴다. 이전 세션 기록에도 이 변수가 "죽은 변수인 줄 알았으나 아니었다"로 한 번 올라온 적이 있다.

**명령 38을 4단계로 나눈 것.** 1단계에서 새 노드를 섬으로 만들어 컴파일, 2단계에서 배선만 옮겨 컴파일, 3단계에서 하나씩 지우며 매번 개수 확인, 4단계에서 최종 컴파일. `SetFoundSlotIndex`와 그 독자들을 지우는 편집은 "변수를 못 찾는다"가 터질 수 있는 자리다. 세 번의 컴파일 중 어디서 터졌어도 원인이 한 단계로 좁혀졌다.

**멈춤 조건을 명령에 넣은 것.** 명령 36과 37이 각각 첫 시도에서 P1에 걸려 **아무것도 안 만들고** 멈췄다. 인터페이스가 안 붙은 채로 진행했으면 `add_event`가 커스텀 이벤트를 만들었을 것이고, 이름은 `Interact`인데 인터페이스 구현이 아닌 노드가 생겨 컴파일은 되고 런타임에만 안 불렸을 것이다.

**Cast 실패 가지를 두 방식으로 나눠 처리한 것.** `ShowHUDMessage`에는 진단 `Print String`을 붙였고 `BP_Door`·`BP_ItemPickup`의 `Interact`에는 안 붙였다. 근거가 다르다 — 전자는 GameMode가 다른 HUD 클래스를 쓰면 실제로 실패할 수 있고(그것이 네 세션째 미확인 항목이었다), 후자는 `Interact`를 부르는 것이 `F` 트레이스 하나뿐이고 거기서 `self`를 넘기므로 실패 경로가 사실상 없다. 게다가 후자는 잠김 안내(메시지 뜸)와 캐스트 실패(아무 일 없음)가 서로 구분되어 침묵 자체가 단서가 된다.

**`Interact(Message)` 노드의 `self` 핀이 대상이라는 것.** 인터페이스 메시지 노드의 `self`는 이 블루프린트의 `self`가 아니라 **메시지를 받을 객체**다. 명령문에 그렇게 명시했고 터미널이 `HitActor`를 거기 꽂았다. 헷갈리면 캐릭터가 자기 자신에게 `Interact`를 보내게 된다.

### 확인한 것 / 확인 못 한 것

**확인한 것**

- **PIE, 2026-08-30 오후 (명령 33 직후).** 사용자가 합격 기준 4개를 전부 해봤고 이상 없었다 — (1) 슬롯 3칸을 채우고 네 번째에 `F`를 누르면 좌상단에 `INVENTORY FULL`이 뜨고 3초 뒤 사라진다, (2) 아이템을 든 채 바닥 없는 쪽에 `Q`를 누르면 `CANNOT DROP HERE`, (3) 겹칠 때 두 줄로 안 쌓이고 덮어쓴다, (4) 메시지가 없을 때 좌상단이 비고 하단 UI가 그대로다
- **PIE, 명령 38 직전.** 명령 34~37이 검증 없이 넷 쌓인 것을 발견해 회귀 확인을 넣었다. `F` 습득 · `INVENTORY FULL` · `CANNOT DROP HERE` 셋 다 이상 없었다
- **PIE, 명령 38 직후.** `F`로 아이템을 줍고 바닥의 것이 사라지는 것, 슬롯이 찼을 때 `INVENTORY FULL`이 뜨는 것. **문 사양의 합격 기준 4번이다** — "인터페이스로 옮긴 뒤에도 아이템 습득이 그대로 된다". 사양이 가장 중요하다고 적은 기준이고, 통과했다
- **에디터 로그를 직접 읽었다.** `LogsToolset.GetLogEntries`로 `LogBlueprint` 카테고리를 훑어 이번 세션 컴파일 30건에 경고·에러가 0건임을 확인했다. 그 전까지 매 명령의 "compiled clean"은 "예외가 안 났다"에만 기대고 있었다
- **모든 명령의 결과를 MCP로 다시 읽었다.** 터미널 보고를 근거로 삼지 않고 `get_node_infos` · `find_nodes` · `list_variables` · `list_events` · `get_properties`로 매번 재확인했다. 여덟 번 다 보고와 일치했다
- **`BP_ThirdPersonGameMode.HUDClass = BP_ThirdPersonHUD_C`.** 네 세션째 이월되던 항목의 절반이 풀렸다. `ShowHUDMessage`의 Cast가 `Lvl_ThirdPerson`에서 성공하는 근거이고, PIE에서 실제로 성공했다
- **`BP_ShooterGameMode.HUDClass = /Script/Engine.HUD`** (스톡). 그 변종에는 인벤토리 HUD가 없다

**확인 못 한 것**

- **문이 실제로 도는 것을 아무도 못 봤다.** `BP_Door`가 레벨에 배치된 적이 없다. `ToggleDoor`도 `Interact`도 한 번도 실행되지 않았다. 이유: 레벨 배치가 명령 39이고 아직 안 했다
- **`Yaw`가 이 경첩의 맞는 축인지, `OpenAngle 90`이 원하는 쪽으로 젖혀지는지.** 계산은 맞게 읽히지만 눈으로 본 적이 없다
- **`1 / SwingSpeed = 1초`가 적당한 속도인지.** 숫자만 정했다
- **여는 도중 다시 `Interact`가 오면 어떻게 되는지.** `MoveComponentTo`의 `Stop`·`Return` 핀을 비워뒀다. 재진입 동작을 시험하지 않았다
- **`OverTime = 0`(`SwingSpeed = 0`)의 실제 동작.** `Divide_DoubleDouble`이 `0.0`을 준다는 것은 엔진 소스에서 확인했지만(`KismetMathLibrary.inl:490`), `MoveComponentTo`가 `OverTime 0`을 어떻게 다루는지는 안 봤다
- **`Instance Editable` 플래그 전부.** `get_variable_instance_editable`이 이 빌드에 없다. 다만 이번에 **볼 필요가 없다는 것**이 밝혀졌다 — 아래 참조
- **`Font` 핀을 비워둔 기본 폰트가 읽히는 크기인지.** PIE에서 메시지가 보였으므로 읽히긴 하는데, 크기가 적당한지는 판단하지 않았다
- **`BP_DoorFrame` 재직렬화의 원인.** 로그에 세션이 하지 않은 컴파일 두 건이 있다. 하나(`04.52.27`)는 `BP_ThirdPersonCharacter` 컴파일과 **같은 프레임**이라 연쇄 재컴파일로 보이지만, git에 뜬 것은 그보다 뒤인 `07.49.47` 단독 컴파일 다음이다. 확정 못 했다
- **`SetbOpen` 노드가 저절로 움직인 이유.** `(-40, 400)` → `(0, 272)`. 배선과 핀 값은 동일하다. 손 작업 중 드래그로 보이지만 확인 안 했다
- **`Lvl_ArenaShooter`의 WorldSettings가 `BP_ShooterGameMode`를 가리키는지.** `.umap`이 바이너리라 못 읽었고, 그 레벨을 로드하는 것은 쓰기라 안 했다

### 남는 리스크

**`Instance Editable`이 이 HUD에서 아무 효과가 없다.** 두 세션째 "눈으로 확인해야 함"으로 이월되던 항목인데, 확인하는 대신 **볼 필요가 없다는 것**이 밝혀졌다. `AHUD`는 `PlayerController`가 `RF_Transient`로 스폰하고 맵에 저장하지 않는다:

```cpp
// PlayerController.cpp:1373  ClientSetHUD_Implementation
SpawnInfo.ObjectFlags |= RF_Transient;	// We never want to save HUDs into a map
```

디테일 패널을 열 인스턴스 자체가 없다. 그리고 이 플래그는 Class Defaults 편집과 무관하다 — `FBlueprintEditorUtils::SetBlueprintOnlyEditableFlag`가 건드리는 것은 `CPF_DisableEditOnInstance` 하나뿐이고 `CPF_Edit`은 안 만진다. 원래 기록에 적혀 있던 **"안 켜져 있으면 레벨에서 인스턴스별 조정이 안 된다"는 걱정은 전제가 틀렸다.**

**인터페이스 부착이 MCP로 안 되는 것이 앞으로도 계속 걸린다.** 상호작용 대상이 늘 때마다 손 작업이 한 번씩 필요하다. 이번에 두 번(`BP_Door` · `BP_ItemPickup`) 걸렸고 둘 다 명령이 P1에서 멈췄다. 멈춤 조건을 넣지 않았으면 조용히 잘못된 노드가 생겼을 것이다.

**타임라인이 이 프로젝트에서 여전히 못 만드는 것으로 남아 있다.** `MoveComponentTo`로 우회했지만 커브 모양을 못 정한다. 문이 튕겼다 멈추는 식의 곡선이 필요해지면 그때 손으로 타임라인을 만들어야 한다.

**`DoesObjectImplementInterface` 검사가 동작상 불필요하다.** `Interact(Message)` 노드는 대상이 인터페이스를 구현 안 했으면 혼자서도 조용히 아무 일도 안 한다. 노드 2개를 쓰고 있다. 사양이 그렇게 적었고 가장 위험한 명령에서 설계까지 같이 바꾸지 않으려고 그대로 뒀다. 나중에 "[F] 열기" 같은 안내를 붙일 자리가 그 분기다.

**문이 한 번 열리면 다시 안 잠긴다.** 사양대로다(`bLocked`는 `false`로만 간다). PIE에서 반복 시험하려면 껐다 켜야 한다.

**빈 `EventTick` 스텁이 세 블루프린트에 있다.** `BP_Door` · `BP_ItemPickup` · `BP_ThirdPersonCharacter` 전부 템플릿이 만든 빈 이벤트 스텁 셋(`BeginPlay` · `ActorBeginOverlap` · `Tick`)을 가지고 있다. 지금은 아무것도 안 하지만 CLAUDE.md가 "기본은 Tick을 꺼둔다"라고 적어둔 것이다.

**내가 명령문에 두 번 틀린 정보를 넣었다.** 명령 34에서 되읽기 이름을 생성 가능 이름으로 착각했고, 명령 38에서 `K2Node_EnhancedInputAction_1`을 `IA_UseItem`이라고 단정했다(실제로는 `IA_Move`). 둘 다 터미널이 잡았다. 노드 ref와 type_id를 기억으로 쓰지 말고 매번 `find_node_types`·`get_node_infos`로 확인해야 한다.

**아이템 습득 경로가 한동안 둘이었다.** 명령 37이 `BP_ItemPickup`의 `Interact`를 만들었고 명령 38이 옛 체인을 지울 때까지 둘이 공존했다. 그 사이에 누가 `Interact`를 불렀으면 아이템이 두 번 들어갔을 것이다. 아무도 안 불러서 문제가 없었지만, 순수 추가라도 이런 창이 생긴다.

### 총평

요청은 셋이었다 — HUD 안내, 문 만들기, 인터페이스 이전. 셋 다 됐고 PIE로 볼 수 있는 것은 전부 봤다.

**이 작업의 실질적 난이도는 블루프린트 로직이 아니라 도구의 벽을 찾는 데 있었다.** 문 여닫기는 사양대로면 타임라인 하나이고, 인터페이스 이전은 노드 넷이다. 실제로 시간을 먹은 것은 (1) 타임라인 트랙을 만들 수단이 없다는 것을 읽기만으로 확정하는 일, (2) 인터페이스 부착이 숨은 프로퍼티라 MCP로 못 닿는다는 것을 엔진 소스까지 가서 확인하는 일, (3) 그 손 작업의 UI 경로를 추측이 아니라 소스로 확인해 내는 일이었다. 세 번째는 한 번 틀렸다 — 사용자가 Outliner에서 찾으려 했는데, 그것이 레벨 에디터가 아니라 블루프린트 에디터 툴바라는 것을 내가 처음에 말하지 않았다.

**명령을 낼 때마다 멈춤 조건을 넣은 것이 값을 했다.** 여덟 개 중 둘이 실제로 멈췄고, 둘 다 아무것도 안 만들고 멈췄다. 명령 26이 `Expose on Spawn` 때문에 통째로 버려졌던 전례가 이 습관을 만들었는데, 이번에 두 번 회수했다.

**가장 위험하다던 작업이 가장 매끄러웠다.** 명령 38이 PIE로 검증된 체인에서 노드 15개를 지웠는데 경고 하나 없이 지나갔다. 4단계로 나누고 매 단계 컴파일한 것, 그리고 지울 15개의 배선을 전부 기록에 남기게 한 것이 그 이유다. 반대로 사양이 "손 작업이 없다"고 적었던 부분에서 손 작업이 두 번 나왔다.

## AI의 제안

**1. 안내 메시지를 좌상단에 두자**

> 좌상단 찬성이다. 세 메시지 다 "방금 누른 키가 실패했다"는 드문 알림이라 상시 UI 자리를 뺏을 이유가 없다. 하단 중앙에 얹으면 아이템 이름·`[E] Use`와 세로로 세 줄이 겹쳐 쌓인다 — 아이템 든 채 인벤토리가 차면 실제로 동시에 뜬다.

사용자가 먼저 좌상단을 제안했고 AI가 근거를 붙여 동의한 것이다. 얻는 것은 하단 UI와 안 겹치는 것. 잃는 것은 시선에서 먼 자리라는 것 — 이 프로젝트에 크로스헤어가 없어 화면 중앙에 기준점이 없다는 것도 근거로 댔다.

**2. HUD 작업을 문 작업 앞에 끼우자**

> HUD 메시지를 문 작업보다 앞에 넣는다. 문 작업의 다음 명령이 `TryAddItem`을 만드는데 그 안에 `INVENTORY FULL` 안내가 들어간다 — HUD 경로가 먼저 있어야 `Print String`을 만들었다가 도로 뜯어내는 일이 없다.

얻는 것은 만들었다 지우는 노드가 없어지는 것. 잃는 것은 명령 번호가 세 칸 밀려 사양 문서와 인계를 고쳐야 하는 것이다.

**3. 타임라인 대신 `MoveComponentTo`**

> 대신 노드 하나로 된다 — `Components|MoveComponentTo`. 핀을 직접 읽어 확인했다. 회전 보간에 필요한 게 전부 한 노드에 있다. Tick도 안 쓰고, 커브 애셋도 안 만들고, 사양의 `범위`에서 "만들지 않는 것"에 뭘 추가하지도 않는다. 잃는 것은 **커브 모양을 못 정하는 것**이다.

사용자가 선택지에서 골랐다. 얻는 것은 지금 바로 되는 것. 잃는 것은 이징 두 불린 말고는 곡선을 못 만드는 것.

**4. `SwingSpeed`를 나눠 쓰자**

> `OverTime = 1 / SwingSpeed` — 나누기 노드 하나 추가. 이름이 계속 참이다 — 큰 값이 빠른 문. 기본값 1.0은 1초 그대로.

사용자가 선택지에서 골랐다. 얻는 것은 변수 이름이 거짓말하지 않는 것. 잃는 것은 노드 하나와, `SwingSpeed = 0`일 때 0으로 나누는 경로가 생기는 것.

**5. 명령 37을 둘로 쪼개자**

> 38이 PIE로 검증된 체인에서 노드 15개를 지운다. 37과 묶으면 뭐가 깨졌을 때 원인이 갈리지 않는다. 그리고 38이 끝나면 바로 PIE로 합격 기준 4번을 볼 수 있다.

얻는 것은 실패 원인이 좁혀지는 것과 검증 시점이 앞당겨지는 것. 잃는 것은 레벨 배치가 39로 또 밀리는 것.

**6. 명령 38 전에 회귀 PIE를 한 번 돌리자**

> 마지막 PIE 검증이 HUD 메시지(명령 33 뒤)다. 그 뒤로 검증 없이 넷이 쌓였다. 34·37은 순수 추가라 안 깨졌어야 하지만 **"안 깨졌어야 한다"는 검증이 아니다.**

사용자가 "작업 상태 괜찮나 자체 확인"을 요청했을 때 나온 것이다. 얻는 것은 명령 38 뒤에 뭔가 깨졌을 때 원인이 38인지 그 앞 넷인지 갈리는 것. 잃는 것은 몇 분.

## 다음으로 넘김

**바로 이어서 할 것**

- **문 작업의 명령 39 — 레벨에 테스트 배치.** 사양은 [`Docs/Spec/2026-08-30-문과-상호작용.md`](../Spec/2026-08-30-문과-상호작용.md)에 있고 표를 39까지 갱신해뒀다.
  - **명령 38까지 끝났다.** 문 로직은 끝에서 끝까지 붙어 있고 컴파일된다. **다만 한 번도 실행된 적이 없다** — `BP_Door`가 레벨에 없어서다
  - **배치할 것**: 벽 대용 박스 둘과 문 하나. 사양의 `범위` 참조 — 문틀 메시(`SM_DoorFrame_Edge`)는 안 붙인다
  - **배치 직후가 문 사양의 합격 기준 1·2·3을 처음 보는 시점이다.** 열쇠 없이 잠긴 문에 `F` → 안내만 뜸 / 열쇠를 들고 `F` → 열리고 열쇠 칸이 빔 / 다시 `F` → 닫힘, 열쇠를 다시 요구 안 함, `bHingeOnRight`를 뒤집으면 반대쪽 경첩
  - **`Lvl_ThirdPerson`에 배치한다.** `GameDefaultMap`이 그것이고 `BP_ThirdPersonGameMode`가 `BP_ThirdPersonHUD`를 쓴다
  - **열쇠를 손에 넣을 방법이 필요하다.** `DT_Items`에 `Key_Stage1` 행이 있고 `BP_ItemPickup`을 배치해 `ItemRow`를 그 행으로 지정하면 된다. 이것도 배치에 포함해야 문을 열어볼 수 있다

**결정 필요**

- **빈 `EventTick` 스텁을 지울 것인가.** `BP_Door` · `BP_ItemPickup` · `BP_ThirdPersonCharacter` 셋 다 템플릿이 만든 빈 이벤트 스텁(`BeginPlay` · `ActorBeginOverlap` · `Tick`)을 갖고 있다. 지금은 아무것도 안 한다
- **`DoesObjectImplementInterface` 검사를 뺄 것인가.** `Interact(Message)`가 혼자서도 안전하게 no-op이라 동작상 불필요하다. 노드 2개. 나중에 상호작용 안내를 붙일 자리이기도 하다
- **드롭 시 벽 앞 판정을 넣을 것인가.** 전방 트레이스 하나가 더 든다

**확인 필요**

- **벽에 붙어 서서 `Q`.** 벽에 반쯤 묻힌 아이템이 나올 것으로 예상만 했다
- **같은 자리에 두 번 `Q`.** 쌓일 것으로 예상만 했다
- **경사면에 `Q`.** 스폰 회전이 `0,0,0`이라 안 눕는다. 얼마나 어색한지 안 봤다
- **`Lvl_ArenaShooter`의 WorldSettings가 `BP_ShooterGameMode`를 가리키는지.** 절반은 풀렸다 — 그 GameMode의 `HUDClass`가 스톡 `/Script/Engine.HUD`인 것은 읽었다. 남은 것은 레벨이 실제로 그 GameMode를 지정하느냐다. `.umap`이 바이너리라 못 읽었다
- **`HandGrip_R` 소켓의 위치·각도.** 지금 아이템 셋이 전부 대칭 도형이라 각도 문제가 안 드러났을 수 있다. 방향이 있는 메시(칼)가 오면 그때 드러난다
- **`MoveComponentTo`를 여는 도중 다시 부르면 어떻게 되는지.** `Stop`·`Return` 핀을 비워뒀다. 명령 39 뒤에 문을 연타해보면 바로 나온다

**접어둔 것**

- **칼로 가기 전에 카메라 작업을 먼저 한다.** `BP_ShooterCharacter`가 `BP_FirstPersonCharacter`를 상속해 카메라가 `head` 본에 붙기 때문에 손이 안 보인다. 원본 Project ICI는 `캡슐 → Camera → SkeletalMesh` 구조라 이 문제가 없었다
- **전환 스냅 완화** — 요 보간 또는 `SetViewTargetWithBlend`. 2026-08-27 기록에서 이월
- **`ForLoop.FirstIndex`가 빈 값인 이유.** 동작에 지장이 없다. 그 그래프를 다시 편집할 일이 생기면 그때 본다
- **`--append-system-prompt`가 저장소에 없다.** `Editor Preferences → General → Terminal → Startup Commands`의 사용자 설정이라 다른 환경에서는 다시 넣어야 한다. 원문은 `Docs/AI-Log/2026-08-28-inventory-item-data.md`의 `명령` 칸에 있다
- **원인 미상의 재직렬화 두 건.** `BP_Door`(커밋 `b4ab97a`)와 `BP_DoorFrame`(커밋 `8e8e30a`). 내용은 안 깨졌다. 다시 나오면 그때 본다
- **`SetbOpen` 노드가 저절로 움직인 것.** 배선과 핀 값이 동일해서 동작에 영향이 없다
- **`Key`의 나머지 용도.** 이 사양이 문 하나를 여는 것까지만 한다. 스테이지별 열쇠, 여러 문, 진행 조건은 진행 구조 단계다
- **`SP` 스태미나.** 원본에 있고 MCP1에 없다. `06-플레이어-UI.md:54` 참조
- **슬롯 2칸 vs 3칸.** 원본은 2칸, MCP1은 3칸이다. 의도한 차이인지 안 정했다
- **미사용 애셋 정리.** 2026-08-30에 **남기기로** 정했다. 지우지 않는다
