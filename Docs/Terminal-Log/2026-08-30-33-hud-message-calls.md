# 2026-08-30 — ShowHUDMessage, and the two Print Strings replaced

Function `ShowHUDMessage` added to BP_ThirdPersonCharacter, and both `Development|PrintString`
nodes in its EventGraph replaced with calls to it. Compiled clean and saved.

`write_graph_dsl` was **not** used on `BP_ThirdPersonCharacter:EventGraph`. The two swaps were
done with `create_node`, `set_pin_value`, `connect_pins` and `delete_node`. DSL was used only on
the new, empty `ShowHUDMessage` graph, which the command exempted.

`AssetTools.is_dirty` was not called.

**The step 2 stop check did not trigger** — `Class|BPThirdPersonHUD|ShowMessage` was already
present on the first attempt, so no refresh was needed and the build continued. Detail in
section 2, including how the observed output differs from the command's stated expectation.

---

## 1. Pre-flight — all five checks passed

### P1 — the two Print String nodes

`find_nodes` on `BP_ThirdPersonCharacter:EventGraph`, title `"Print"`:

```
["K2Node_CallFunction_36", "K2Node_CallFunction_8"]
```

Exactly two, exactly the two named. Pass.

The note about the title filter is confirmed — `find_nodes` with title `"Print String"` on the
same graph returned:

```
[]
```

So `"Print"` really is the working filter on this build.

### P2 — K2Node_CallFunction_36

```
type_id : Development|PrintString
position: (320, 980)
inputs  :
  execute        <- K2Node_IfThenElse_2 [out 1]
  InString        = "INVENTORY FULL"
  bPrintToScreen  = "true"
  bPrintToLog     = "true"
  TextColor       = "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)"
  Duration        = "3.0"
  Key             = "None"
outputs :
  then -> []
```

All four stated facts match. Pass.

### P3 — K2Node_CallFunction_8

```
type_id : Development|PrintString
position: (400, 3600)
inputs  :
  execute        <- K2Node_IfThenElse_6 [out 1]
  InString        = "CANNOT DROP HERE"
  bPrintToScreen  = "true"
  bPrintToLog     = "true"
  TextColor       = "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)"
  Duration        = "3.0"
  Key             = "None"
outputs :
  then -> []
```

All four stated facts match. Pass.

### P4 — node count

`find_nodes` with an empty title on `BP_ThirdPersonCharacter:EventGraph`: **98** nodes.

### P5 — no ShowHUDMessage yet

`list_functions` on BP_ThirdPersonCharacter:

```
["UserConstructionScript", "Move", "Aim", "ToggleCameraView", "RefreshHeldItem", "CanJumpInternal"]
```

`ShowHUDMessage` is not present. Pass.

---

## 2. Step 2 stop check — the node was already there

To avoid leaving a half-built graph if the check failed, step 1 was split: the function graph
and its `Message` parameter were created first, the filter was run, and only then was the body
written.

After `add_function_graph` + `add_function_param`, the graph read:

```
(fn ShowHUDMessage (Message))
```

`find_node_types` on `BP_ThirdPersonCharacter:ShowHUDMessage`, `type_id_filter`
`"BPThirdPersonHUD"`, `context_pins` `[]`, returned **40 entries**, full output verbatim:

```
["Class|BPThirdPersonHUD|ShowMessage", "Class|BPThirdPersonHUD|GetDefaultSceneRoot",
 "Class|BPThirdPersonHUD|SetDefaultSceneRoot", "Class|BPThirdPersonHUD|GetSlotCount",
 "Class|BPThirdPersonHUD|SetSlotCount", "Class|BPThirdPersonHUD|GetSlotSize",
 "Class|BPThirdPersonHUD|SetSlotSize", "Class|BPThirdPersonHUD|GetSlotGap",
 "Class|BPThirdPersonHUD|SetSlotGap", "Class|BPThirdPersonHUD|GetBottomMargin",
 "Class|BPThirdPersonHUD|SetBottomMargin", "Class|BPThirdPersonHUD|GetBorderThickness",
 "Class|BPThirdPersonHUD|SetBorderThickness", "Class|BPThirdPersonHUD|GetColorIdle",
 "Class|BPThirdPersonHUD|SetColorIdle", "Class|BPThirdPersonHUD|GetColorSelected",
 "Class|BPThirdPersonHUD|SetColorSelected", "Class|BPThirdPersonHUD|GetCachedCharacter",
 "Class|BPThirdPersonHUD|SetCachedCharacter", "Class|BPThirdPersonHUD|GetHPBarHeight",
 "Class|BPThirdPersonHUD|SetHPBarHeight", "Class|BPThirdPersonHUD|GetColorHPBack",
 "Class|BPThirdPersonHUD|SetColorHPBack", "Class|BPThirdPersonHUD|GetColorHPFill",
 "Class|BPThirdPersonHUD|SetColorHPFill", "Class|BPThirdPersonHUD|GetTextLineHeight",
 "Class|BPThirdPersonHUD|SetTextLineHeight", "Class|BPThirdPersonHUD|GetTextScale",
 "Class|BPThirdPersonHUD|SetTextScale", "Class|BPThirdPersonHUD|GetMessageText",
 "Class|BPThirdPersonHUD|SetMessageText", "Class|BPThirdPersonHUD|GetMessageExpireTime",
 "Class|BPThirdPersonHUD|SetMessageExpireTime", "Class|BPThirdPersonHUD|GetColorMessage",
 "Class|BPThirdPersonHUD|SetColorMessage", "Class|BPThirdPersonHUD|GetMessageMargin",
 "Class|BPThirdPersonHUD|SetMessageMargin", "Class|BPThirdPersonHUD|GetMessageDuration",
 "Class|BPThirdPersonHUD|SetMessageDuration"]
```

**`Class|BPThirdPersonHUD|ShowMessage` appeared — it is the first entry in the list.**

### This differs from the command's stated expectation

The command said the filter "returns 28 entries which are ONLY the accessors of the 13 OLD
BP_ThirdPersonHUD variables plus two component accessors", with `ShowMessage` absent and the
five `Message*` accessors absent.

What was actually observed is 40 entries, containing `ShowMessage` **and** all ten `Message*`
accessors (`Get`/`Set` for `MessageText`, `MessageExpireTime`, `ColorMessage`, `MessageMargin`,
`MessageDuration`). The registry was already current.

The likely reason is ordering: BP_ThirdPersonHUD was compiled and saved at the end of the
previous two commands (`04.13.23` and `04.22.36` in the log), which is exactly the refresh the
command prescribed as the remedy. By the time this command ran, it had already happened.

**No refresh attempt was made**, because none was needed — there is therefore no "after
refresh" output to report. Compiling BP_ThirdPersonHUD again would have been a no-op write to
an asset this command was not asked to touch.

The build continued to step 1's body and step 3.

---

## 3. ShowHUDMessage — complete node inventory

Graph: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:ShowHUDMessage`

Body written with `write_graph_dsl`. The cast node's exec pin names were read first with
`get_node_type_pins` rather than assumed — they are `then` (out 0) and `CastFailed` (out 1),
with the data output named `AsBP Third Person HUD` (out 2).

`find_nodes` returned **6** nodes. (`...` = the graph path above.)

| # | refPath | type_id |
|---|---|---|
| 1 | `....K2Node_FunctionEntry_0` | `\|ShowHUDMessage` |
| 2 | `....K2Node_CallFunction_3` | `Game\|GetPlayerController` |
| 3 | `....K2Node_CallFunction_4` | `HUD\|GetHUD` |
| 4 | `....K2Node_DynamicCast_1` | `Utilities\|Casting\|CastToBP_ThirdPersonHUD` |
| 5 | `....K2Node_CallFunction_5` | `\|ShowMessage` |
| 6 | `....K2Node_CallFunction_6` | `Development\|PrintString` |

No node beyond the six the body calls for. `write_graph_dsl` emitted no helper nodes this time —
the script had no literals or struct accessors to expand.

### Full pin connection list

```
K2Node_FunctionEntry_0   |ShowHUDMessage
  out [0] "then"    -> K2Node_DynamicCast_1 [in 0]
  out [1] "Message" (String) -> K2Node_CallFunction_5 [in 2]

K2Node_CallFunction_3   Game|GetPlayerController
  in  [0] "PlayerIndex" (Integer) = "0"   (no connection)
  out [0] "ReturnValue" (Player Controller Object Reference) -> K2Node_CallFunction_4 [in 0]

K2Node_CallFunction_4   HUD|GetHUD
  in  [0] "self" (Player Controller Object Reference) <- K2Node_CallFunction_3 [out 0]
  out [0] "ReturnValue" (HUD Object Reference) -> K2Node_DynamicCast_1 [in 1]

K2Node_DynamicCast_1   Utilities|Casting|CastToBP_ThirdPersonHUD
  in  [0] "execute" (Exec)             <- K2Node_FunctionEntry_0 [out 0]
  in  [1] "Object"  (Object Reference) <- K2Node_CallFunction_4 [out 0]
  out [0] "then"       (Exec) -> K2Node_CallFunction_5 [in 0]
  out [1] "CastFailed" (Exec) -> K2Node_CallFunction_6 [in 0]
  out [2] "AsBP Third Person HUD" (BP Third Person HUD Object Reference) -> K2Node_CallFunction_5 [in 1]

K2Node_CallFunction_5   |ShowMessage
  in  [0] "execute" (Exec)                                  <- K2Node_DynamicCast_1 [out 0]
  in  [1] "self"    (BP Third Person HUD Object Reference)  <- K2Node_DynamicCast_1 [out 2]
  in  [2] "Message" (String)                                <- K2Node_FunctionEntry_0 [out 1]
  out [0] "then" (Exec) -> (nothing)

K2Node_CallFunction_6   Development|PrintString
  in  [0] "execute"        (Exec)    <- K2Node_DynamicCast_1 [out 1]
  in  [1] "InString"       (String)   = "HUD MESSAGE DROPPED"
  in  [2] "bPrintToScreen" (Boolean)  = "true"        (default, untouched)
  in  [3] "bPrintToLog"    (Boolean)  = "true"        (default, untouched)
  in  [4] "TextColor"      (LinearColor) = "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)"  (default, untouched)
  in  [5] "Duration"       (Float single) = "2.000000"  (default, untouched)
  in  [6] "Key"            (Name)     = "None"        (default, untouched)
  out [0] "then" (Exec) -> (nothing)
```

The success branch calls `ShowMessage` on the cast result with the entry's `Message`; the
failure branch prints `HUD MESSAGE DROPPED` with every other pin left at its creation default,
as instructed.

`ShowMessage` reads back as type_id `|ShowMessage` rather than the
`Class|BPThirdPersonHUD|ShowMessage` that was passed — the registry name carries the owning
class, the node's own type_id does not. Same shape as `|RefreshHeldItem` in command 31.

After the body was written, BP_ThirdPersonCharacter was compiled so the self-call node would
register. `find_node_types` on the EventGraph with filter `"ShowHUDMessage"` then returned:

```
["CallFunction|ShowHUDMessage"]
```

and `list_functions` returned:

```
["UserConstructionScript", "Move", "Aim", "ToggleCameraView", "RefreshHeldItem", "ShowHUDMessage", "CanJumpInternal"]
```

---

## 4. Step 3a — INVENTORY FULL

New node `K2Node_CallFunction_34`, type_id `|ShowHUDMessage`, at **(320, 1120)**.

Its pins at creation were read before wiring: `execute` [0], `self` [1] (Self Object Reference),
`Message` [2] (String). `Message` is index 2, not 1 — the `self` pin sits between them.

Read back after the swap:

```
K2Node_CallFunction_34   |ShowHUDMessage   at (320, 1120)
  in  [0] "execute" <- K2Node_IfThenElse_2 [out 1]
  in  [1] "self"     = ""   (unconnected — self call)
  in  [2] "Message"  = "INVENTORY FULL"
  out [0] "then" -> (nothing)
```

### K2Node_IfThenElse_2 [out 1] after the swap

```
out [0] "then" -> ["K2Node_CallArrayFunction_3[in 0]"]
out [1] "else" -> ["K2Node_CallFunction_34[in 0]"]
```

**Pin [out 1] goes to the new node and to nothing else.** Its `then` pin is untouched.

### The Print String is gone

`delete_node` on `K2Node_CallFunction_36` completed without raising. `find_nodes` with title
`"Print"` immediately afterwards returned:

```
["K2Node_CallFunction_8"]
```

`K2Node_CallFunction_36` is absent. Node count at this point: **98** (98 + 1 created − 1
deleted).

One observation worth recording: the branch's `else` pin was read **before** the delete as
already pointing only at `K2Node_CallFunction_34`. Connecting a new destination to an exec
output replaces the existing one rather than adding to it, so the old Print String was already
orphaned at connect time; the delete then removed a disconnected node. No `break_pins` call was
needed and none was made.

---

## 5. Step 3b — CANNOT DROP HERE

New node `K2Node_CallFunction_37`, type_id `|ShowHUDMessage`, at **(400, 3740)**.

Read back after the swap:

```
K2Node_CallFunction_37   |ShowHUDMessage   at (400, 3740)
  in  [0] "execute" <- K2Node_IfThenElse_6 [out 1]
  in  [1] "self"     = ""   (unconnected — self call)
  in  [2] "Message"  = "CANNOT DROP HERE"
  out [0] "then" -> (nothing)
```

### K2Node_IfThenElse_6 [out 1] after the swap

```
out [0] "then" -> ["K2Node_SpawnActorFromClass_0[in 0]"]
out [1] "else" -> ["K2Node_CallFunction_37[in 0]"]
```

**Pin [out 1] goes to the new node and to nothing else.** Its `then` pin still drives the
SpawnActor from command 27, untouched.

### The Print String is gone

`delete_node` on `K2Node_CallFunction_8` completed without raising.

Both message strings were copied exactly as written in the command — capitals, single space —
and read back byte-identical to the strings the deleted nodes carried (P2 and P3 above).

---

## 6. find_nodes title "Print" after the work

```
[]
```

**Empty array.** No `Development|PrintString` node remains anywhere in
`BP_ThirdPersonCharacter:EventGraph`.

The one PrintString that still exists in this Blueprint is
`K2Node_CallFunction_6` inside the `ShowHUDMessage` function graph — the deliberate
`HUD MESSAGE DROPPED` diagnostic. It is in a different graph and is not matched by this query.

---

## 7. EventGraph node count

From the length of a `find_nodes` result with an empty title:

- **Before (P4):** 98
- **After 3a:** 98
- **After 3b:** 98
- **Final:** 98

**Unchanged from P4**, as required. Two nodes created, two deleted.

The `ShowHUDMessage` function graph's 6 nodes are in their own graph and do not count toward the
EventGraph total.

---

## 8. Compile result

`BlueprintTools.compile_blueprint` on BP_ThirdPersonCharacter, `warnings_as_errors` = `false`,
returned:

```
{"returnValue":null}
```

The tool raises on error; it did not raise. Three compiles of this Blueprint happened during the
command — one internal to `write_graph_dsl`, one explicit after the body was written so the
self-call node would register, and the final one after both swaps:

```
[2026.08.30-04.46.53:956][357]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.08.30-04.47.16:747][426]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.08.30-04.48.13:738][597]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
```

No error and no warning followed any of the three. **Compiled clean.**

`AssetTools.save_assets` -> `true`. The save wrote the package and ran content validation:

```
[2026.08.30-04.48.23:980][627]LogSavePackage: Moving 'D:/20260827/MCP1/Saved/BP_ThirdPersonCharacterC31472DE43B9945A435729B73908E888.tmp' to 'D:/20260827/MCP1/Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset'
[2026.08.30-04.48.24:096][628]AssetCheck: /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter Validating asset
```

Nine validators ran, no failure reported.

**Not verified:** no tool reports a Blueprint's compiled status flag directly. "Compiled clean"
rests on the calls not raising plus an empty log window.

---

## 9. Errors and warnings — exact English text

### 9.1 From this work

**None.** Every call — `find_nodes`, `get_node_infos`, `get_node_type_pins`, `find_node_types`,
`list_functions`, `list_graphs`, `add_function_graph`, `add_function_param`, `read_graph_dsl`,
`write_graph_dsl`, `create_node` (x2), `set_pin_value` (x2), `connect_pins` (x2), `delete_node`
(x2), `compile_blueprint` (x2 explicit) and `save_assets` — completed without raising, and
nothing was written to the log beyond routine dispatch, compile, save and validation lines.

There is no error or warning text to quote for this command.

### 9.2 Present in the log but NOT from this work

Nothing new. A filter for `Warning|Error` across the command's time window returned only the
save and content-validation lines quoted in section 8. The `LogBlueprint` warning block from
`00.36.49` is no longer within the last-5 window of `LogBlueprint` entries, having been pushed
out by this session's compiles; it was recorded verbatim in the reports for commands 24, 25, 27,
28, 29, 31 and 32.

---

## 10. git status after the work

```
 M Content/Interaction/BP_Door.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonHUD.uasset
?? Docs/Terminal-Log/2026-08-30-31-hud-message-vars.md
?? Docs/Terminal-Log/2026-08-30-32-hud-message-draw.md
```

`BP_ThirdPersonCharacter.uasset` is the file this command changed.

`BP_ThirdPersonHUD.uasset` is from commands 31 and 32, and `BP_Door.uasset` was already showing
as modified before command 31 started — the same observation recorded there. Neither was touched
by this command.

---

## 11. What is not verified

- **Nothing was run in PIE.** The whole message pipeline now exists end to end — Character
  calls `ShowHUDMessage`, which casts to the HUD and calls `ShowMessage`, which sets
  `MessageText` and `MessageExpireTime`, which the HUD's draw block reads — but no message has
  been shown on screen. Unconfirmed in particular:
  - that the level's GameMode actually uses `BP_ThirdPersonHUD`. If it does not, the cast fails
    and every message becomes the `HUD MESSAGE DROPPED` diagnostic instead. **This is the single
    most likely thing to be wrong**, and it is exactly what the failure branch was built to make
    visible. The GameMode's HUD class was not read in this command.
  - that `GetPlayerController` with `PlayerIndex` 0 resolves correctly from a Character
  - that the drawn message is legible at `MessageMargin` 24 and `TextScale` 2
- **That the two swapped call sites still fire under the same conditions as the Print Strings
  they replaced.** The driving branches (`K2Node_IfThenElse_2 [out 1]` and
  `K2Node_IfThenElse_6 [out 1]`) were read back as pointing at the new nodes, and neither
  branch's `then` pin was touched, but the surrounding logic was not re-traced.
