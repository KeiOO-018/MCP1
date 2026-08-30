# 2026-08-30 — BP_Door: the Interact event and the lock check

The interface event plus ten nodes in `BP_Door:EventGraph`. Compiled clean and saved.

This is the second run of this command. The first attempt stopped at P1 because BPI_Interact was
not in BP_Door's Implemented Interfaces; that has since been added by hand, so P1 now passes and
the build went through. This report replaces the stop report at the same path.

`AssetTools.is_dirty` was not called. `write_graph_dsl` was not used.

---

## 1. Pre-flight — all five checks passed

### P1 — Interact is now present

`BlueprintTools.list_events` on BP_Door returned **24** entries. Full list of names, verbatim:

```
["ToggleDoor", "ReceiveTick", "ReceiveRadialDamage", "ReceivePointDamage", "ReceiveHit",
 "ReceiveEndPlay", "ReceiveDestroyed", "ReceiveBeginPlay", "ReceiveAsyncPhysicsTick",
 "ReceiveAnyDamage", "ReceiveActorOnReleased", "ReceiveActorOnInputTouchLeave",
 "ReceiveActorOnInputTouchEnter", "ReceiveActorOnInputTouchEnd",
 "ReceiveActorOnInputTouchBegin", "ReceiveActorOnClicked", "ReceiveActorEndOverlap",
 "ReceiveActorEndCursorOver", "ReceiveActorBeginOverlap", "ReceiveActorBeginCursorOver",
 "K2_OnReset", "K2_OnEndViewTarget", "K2_OnBecomeViewTarget", "Interact"]
```

The `Interact` entry, in full:

```
{"name": "Interact", "description": "Interact", "bIsImplemented": false}
```

**`bIsImplemented` BEFORE: `false`** — the interface is on the class, but no event node existed
in the graph yet.

**`bIsImplemented` AFTER (re-read at the end of the command): `true`.**

For contrast, the previous run of this command read the same list at 23 entries with no
`Interact` at all — that is the change the hand edit made.

### P2 — 14 nodes before

| # | refPath | type_id |
|---|---|---|
| 1 | `...:EventGraph.K2Node_Event_0` | `AddEvent\|EventBeginPlay` |
| 2 | `...:EventGraph.K2Node_Event_1` | `AddEvent\|Collision\|EventActorBeginOverlap` |
| 3 | `...:EventGraph.K2Node_Event_2` | `AddEvent\|EventTick` |
| 4 | `...:EventGraph.K2Node_CustomEvent_0` | `AddEvent\|Custom\|ToggleDoor` |
| 5 | `...:EventGraph.K2Node_VariableGet_0` | `\|GetbOpen` |
| 6 | `...:EventGraph.K2Node_CallFunction_3` | `Math\|Boolean\|NOTBoolean` |
| 7 | `...:EventGraph.K2Node_VariableSet_0` | `\|SetbOpen` |
| 8 | `...:EventGraph.K2Node_VariableGet_1` | `\|GetHinge` |
| 9 | `...:EventGraph.K2Node_VariableGet_2` | `\|GetOpenAngle` |
| 10 | `...:EventGraph.K2Node_CallFunction_4` | `Math\|Float\|SelectFloat` |
| 11 | `...:EventGraph.K2Node_CallFunction_5` | `Math\|Rotator\|MakeRotator` |
| 12 | `...:EventGraph.K2Node_VariableGet_3` | `\|GetSwingSpeed` |
| 13 | `...:EventGraph.K2Node_PromotableOperator_0` | `Math\|Float\|float/float` |
| 14 | `...:EventGraph.K2Node_CallFunction_6` | `Components\|MoveComponentTo` |

(`...` = `/Game/Interaction/BP_Door.BP_Door`)

### P3 — variables

```
["bLocked", "RequiredKey", "bHingeOnRight", "OpenAngle", "SwingSpeed", "bOpen"]
```

Exactly the six required.

### P4 — RequiredKey's default, from the CDO

```
{"RequiredKey":{"dataTable":{"refPath":"/Game/Inventory/DT_Items.DT_Items"},"rowName":"Key_Stage1"},
 "bLocked":true,
 "bOpen":false}
```

- **DataTable:** `/Game/Inventory/DT_Items.DT_Items`
- **RowName:** `Key_Stage1`

`bLocked` is `true` and `bOpen` is `false`, unchanged from command 30.

### P5 — all five node types offered

| required type_id | offered |
|---|---|
| `Class\|BPThirdPersonCharacter\|TryConsumeSelected` | yes |
| `Class\|BPThirdPersonCharacter\|ShowHUDMessage` | yes |
| `CallFunction\|ToggleDoor` | yes |
| `Utilities\|Struct\|BreakDataTableRowHandle` | yes |
| `Utilities\|Casting\|CastToBP_ThirdPersonCharacter` | yes |

None missing.

---

## 2. The Interact event node as created

`BlueprintTools.add_event`, `event_name` `"Interact"`, `position` (-600, 1200). Because
`Interact` matches an inherited overridable event — the one the interface contributes — it
created an implementation node rather than a custom event.

```
refPath  : /Game/Interaction/BP_Door.BP_Door:EventGraph.K2Node_Event_3
type_id  : AddEvent|EventInteract
position : (-608, 1200)

input pins : (none)
output pins:
  [0] "OutputDelegate"  Delegate
  [1] "then"            Exec
  [2] "Interactor"      Actor Object Reference
```

**The `Interactor` pin is present, at output index 2, typed `Actor Object Reference`.** The stop
condition in step 1 did not trigger.

Its x reads **-608**, not the -600 that was passed — the editor snapped the node to its grid.
A change of 8 units, noted rather than corrected.

---

## 3. Node inventory of BP_Door:EventGraph after the work

**25 nodes.** The 14 from P2, unchanged, plus these 11:

| # | refPath | type_id | position |
|---|---|---|---|
| 15 | `...:EventGraph.K2Node_Event_3` | `AddEvent\|EventInteract` | (-608, 1200) |
| 16 | `...:EventGraph.K2Node_VariableGet_4` | `\|GetbLocked` | (-400, 1400) |
| 17 | `...:EventGraph.K2Node_IfThenElse_0` | `Utilities\|FlowControl\|Branch` | (-200, 1200) |
| 18 | `...:EventGraph.K2Node_DynamicCast_0` | `Utilities\|Casting\|CastToBP_ThirdPersonCharacter` | (100, 1200) |
| 19 | `...:EventGraph.K2Node_VariableGet_5` | `\|GetRequiredKey` | (100, 1560) |
| 20 | `...:EventGraph.K2Node_BreakStruct_0` | `Utilities\|Struct\|BreakDataTableRowHandle` | (330, 1560) |
| 21 | `...:EventGraph.K2Node_CallFunction_7` | `\|TryConsumeSelected` | (560, 1200) |
| 22 | `...:EventGraph.K2Node_IfThenElse_1` | `Utilities\|FlowControl\|Branch` | (860, 1200) |
| 23 | `...:EventGraph.K2Node_VariableSet_1` | `\|SetbLocked` | (1080, 1200) |
| 24 | `...:EventGraph.K2Node_CallFunction_8` | `\|ToggleDoor` | (1380, 1200) |
| 25 | `...:EventGraph.K2Node_CallFunction_9` | `\|ShowHUDMessage` | (1080, 1480) |

Node 15 is step 1's event; nodes 16–25 are step 2's a–j. All sit in the y 1200–1560 band with
x from -608 to 1380, inside the requested -600…1600 range.

### Full pin connection list of every node added by this command

```
K2Node_Event_3   AddEvent|EventInteract
  out [0] "OutputDelegate" (Delegate) -> (nothing)
  out [1] "then"           (Exec)     -> K2Node_IfThenElse_0 [in 0]
  out [2] "Interactor"     (Actor Object Reference) -> K2Node_DynamicCast_0 [in 1]

K2Node_VariableGet_4   |GetbLocked                                    (b)
  out [0] "bLocked" (Boolean) -> K2Node_IfThenElse_0 [in 1]

K2Node_IfThenElse_0   Utilities|FlowControl|Branch                    (a) Branch A
  in  [0] "execute"   (Exec)              <- K2Node_Event_3 [out 1]
  in  [1] "Condition" (Boolean) = "true"  <- K2Node_VariableGet_4 [out 0]
  out [0] "then" (Exec) -> K2Node_DynamicCast_0 [in 0]
  out [1] "else" (Exec) -> K2Node_CallFunction_8 [in 0]

K2Node_DynamicCast_0   Utilities|Casting|CastToBP_ThirdPersonCharacter   (c)
  in  [0] "execute" (Exec)             <- K2Node_IfThenElse_0 [out 0]
  in  [1] "Object"  (Object Reference) <- K2Node_Event_3 [out 2]
  out [0] "then"       (Exec) -> K2Node_CallFunction_7 [in 0]
  out [1] "CastFailed" (Exec) -> (nothing)
  out [2] "AsBP Third Person Character" (BP Third Person Character Object Reference)
        -> K2Node_CallFunction_7 [in 1]
        -> K2Node_CallFunction_9 [in 1]

K2Node_VariableGet_5   |GetRequiredKey                                (d)
  out [0] "RequiredKey" (Data Table Row Handle Structure) -> K2Node_BreakStruct_0 [in 0]

K2Node_BreakStruct_0   Utilities|Struct|BreakDataTableRowHandle       (e)
  in  [0] "DataTableRowHandle" (DTRH by ref) <- K2Node_VariableGet_5 [out 0]
  out [0] "DataTable" (Data Table Object Reference) -> (nothing)
  out [1] "RowName"   (Name) -> K2Node_CallFunction_7 [in 2]

K2Node_CallFunction_7   |TryConsumeSelected                           (f)
  in  [0] "execute" (Exec)                     <- K2Node_DynamicCast_0 [out 0]
  in  [1] "self"    (BP Third Person Character Object Reference) <- K2Node_DynamicCast_0 [out 2]
  in  [2] "RowName" (Name) = "None"            <- K2Node_BreakStruct_0 [out 1]
  out [0] "then"    (Exec)    -> K2Node_IfThenElse_1 [in 0]
  out [1] "Success" (Boolean) -> K2Node_IfThenElse_1 [in 1]

K2Node_IfThenElse_1   Utilities|FlowControl|Branch                    (g) Branch B
  in  [0] "execute"   (Exec)              <- K2Node_CallFunction_7 [out 0]
  in  [1] "Condition" (Boolean) = "true"  <- K2Node_CallFunction_7 [out 1]
  out [0] "then" (Exec) -> K2Node_VariableSet_1 [in 0]
  out [1] "else" (Exec) -> K2Node_CallFunction_9 [in 0]

K2Node_VariableSet_1   |SetbLocked                                    (h)
  in  [0] "execute" (Exec)               <- K2Node_IfThenElse_1 [out 0]
  in  [1] "bLocked" (Boolean) = "false"  <- (unconnected)
  out [0] "then"       (Exec)    -> K2Node_CallFunction_8 [in 0]
  out [1] "Output_Get" (Boolean) -> (nothing)

K2Node_CallFunction_8   |ToggleDoor                                   (i)
  in  [0] "execute" (Exec) <- K2Node_VariableSet_1 [out 0], K2Node_IfThenElse_0 [out 1]
  in  [1] "self"    (Self Object Reference) = ""  (unconnected — self call)
  out [0] "then" (Exec) -> (nothing)

K2Node_CallFunction_9   |ShowHUDMessage                               (j)
  in  [0] "execute" (Exec)                     <- K2Node_IfThenElse_1 [out 1]
  in  [1] "self"    (BP Third Person Character Object Reference) <- K2Node_DynamicCast_0 [out 2]
  in  [2] "Message" (String) = "DOOR IS LOCKED"  (unconnected)
  out [0] "then" (Exec) -> (nothing)
```

Every connection was made by resolving the pin **name** to its index from a `get_node_infos`
read of each node taken before wiring. The cast's data pin is named `AsBP Third Person Character`
(no space after "As") and its exec outputs are `then` and `CastFailed`, as the command said.

### Resulting logic

```
Interact(Interactor)
  -> Branch A (bLocked?)
       false -> ToggleDoor                                    (already unlocked, just open/close)
       true  -> Cast Interactor to BP_ThirdPersonCharacter
                  CastFailed -> (nothing, deliberately)
                  then -> TryConsumeSelected(RowName = RequiredKey.RowName)
                            -> Branch B (Success?)
                                 true  -> Set bLocked = false -> ToggleDoor
                                 false -> ShowHUDMessage "DOOR IS LOCKED"
```

---

## 4. The three specific confirmations

### ToggleDoor has TWO incoming exec connections, and there is only one such node

`K2Node_CallFunction_8`, input pin [0] `execute`, read back:

```
from: ["K2Node_VariableSet_1[out 0]", "K2Node_IfThenElse_0[out 1]"]
```

Two sources: **`Set bLocked`'s `then`** and **Branch A's `else`** — exactly the pair the command
specified. Confirmed from the other side too: `K2Node_IfThenElse_0 out[1] "else"` lists
`["K2Node_CallFunction_8[in 0]"]`, and `K2Node_VariableSet_1 out[0] "then"` lists
`["K2Node_CallFunction_8[in 0]"]`.

Scanning the full 25-node inventory for type_id `|ToggleDoor` finds **exactly one** match,
`K2Node_CallFunction_8`. (`K2Node_CustomEvent_0` is `AddEvent|Custom|ToggleDoor` — the event
being called, not a second call node.) Likewise, scanning for `|GetbLocked` finds exactly one,
`K2Node_VariableGet_4`.

### The cast's CastFailed pin is unconnected

`K2Node_DynamicCast_0`, output pin [1]:

```
{"i": 1, "n": "CastFailed", "t": "Exec", "to": []}
```

Empty `to` list. Left open deliberately, as instructed.

### Set bLocked's value pin holds the literal false and is not connected

`K2Node_VariableSet_1`, input pin [1]:

```
{"i": 1, "n": "bLocked", "t": "Boolean", "v": "false", "from": []}
```

Value `"false"`, `from` empty. `set_pin_value` was called explicitly with `"false"` rather than
relying on the creation default, and the read-back confirms both the value and that nothing
drives the pin.

---

## 5. EventGraph node count

- **Before:** 14
- **After:** 25

14 + 11 = 25. The eleven are the Interact event from step 1 plus the ten nodes a–j from step 2.

**No node was created beyond the ones named in the command.** There is nothing extra to list —
no helper node, no conversion node, no duplicate getter.

---

## 6. The command-35 ToggleDoor block

All eleven nodes `K2Node_CustomEvent_0` through `K2Node_CallFunction_6` were re-read in full
after the work. **Every pin connection and every pin value is identical to command 35's
report** — the exec chain `ToggleDoor → SetbOpen → MoveComponentTo`, `bPickA` still fed from
`SetbOpen.Output_Get`, `TargetRelativeLocation` still unconnected at `0, 0, 0`, `bEaseIn` and
`bEaseOut` still `true`, the divide still `A = 1.0` with `B` from `SwingSpeed`.

**One discrepancy, in position only.** `K2Node_VariableSet_0` (`|SetbOpen`) reads **(0, 272)**;
command 35's report recorded it at **(-40, 400)**.

This command issued no `set_node_position` and no `arrange_nodes`, and made no call naming that
node. The change is cosmetic — no connection, pin value or type differs — but it is a real
difference from the last recorded state and is not explained by anything this command did. The
likeliest cause is the same hand session that added the interface: the log shows a compile of
BP_Door at `08.00.11` that this session did not perform, and `git status` shows
`BP_DoorFrame.uasset` modified, which this session has never touched. Recorded as an
observation; not investigated further.

The other ten nodes of that block read at their command-35 positions unchanged.

---

## 7. Compile result

`BlueprintTools.compile_blueprint` on BP_Door, `warnings_as_errors` = `false`, returned:

```
{"returnValue":null}
```

The tool raises on error; it did not raise.

```
[2026.08.30-08.03.00:736][654]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Door.BP_Door'
```

No error and no warning followed it. **Compiled clean.** In particular the interface event, the
cast with an unconnected `CastFailed`, and the two exec lines converging on one `ToggleDoor`
input all compiled without complaint.

`AssetTools.save_assets` -> `true`. Content validation ran on save:

```
[2026.08.30-08.03.11:761][687]AssetCheck: /Game/Interaction/BP_Door Validating asset
```

Nine validators, no failure reported.

**Not verified:** no tool reports a Blueprint's compiled status flag directly. "Compiled clean"
rests on the call not raising plus an empty log window.

---

## 8. Errors and warnings — exact English text

### 8.1 From this work

**None.** Every call in this command — `list_events`, `find_nodes`, `get_node_infos`,
`list_variables`, `get_properties`, `find_node_types`, `add_event`, `create_node` (x10),
`connect_pins` (x15), `set_pin_value` (x2), `compile_blueprint` and `save_assets` — completed
without raising, and nothing was written to the log beyond routine dispatch, compile, save and
validation lines.

### 8.2 Present in the log but NOT from this work

A `Warning|Error` scan turned up these, none of them from this command's calls:

```
[2026.08.30-05.21.35:688][517]LogJson: Warning: Property "OnReachedJumpApex" type FCharacterReachedApexSignature unhandled during Json schema generation.
```

Tail of the `LogJson` block from command 34's `list_properties` read; recorded there in full.

```
[2026.08.30-07.23.11:266][585]LogScript: Warning: /Game/Interaction/BP_Door.BP_Door is not valid Actor for property 'actor'
[2026.08.30-07.37.39:024][915]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Door.Default__BP_Door_C' (BP_Door_C): the following properties could not be read: ImplementedInterfaces
```

Both from the **previous** run of this command, at `07.23` and `07.37` — the diagnostic reads
made while establishing that P1 had failed. They predate this run and reflect calls that
returned nothing rather than calls that broke anything.

```
[2026.08.30-07.59.48:279][189]LogEditorClassViewer: Warning: Class /Script/ModelViewViewModelBlueprint.MVVMK2Node_LoadSoftTexture has parent /Script/ModelViewViewModelBlueprint.MVVMK2Node_LoadSoftResource, but this parent is not found. The Class will not be shown in ClassViewer.
```

Five lines of this shape at `07.59.48`, naming `MVVMK2Node_LoadSoftTexture`,
`MVVMK2Node_LoadSoftMaterial`, `MVVMK2Node_LoadSoftInputAction`,
`MVVMK2Node_MakeBrushFromSoftTexture` and `MVVMK2Node_MakeBrushFromSoftMaterial`. These come
from the editor's Class Viewer refreshing — `07.59.48` is inside the hand session that added the
interface, before this command's first call. They concern a Model-View-ViewModel plugin and
have nothing to do with BP_Door.

A foreign Blueprint compile also appears, which this session did not perform:

```
[2026.08.30-07.49.47:795][181]LogBlueprint: Compiling Blueprint '/Game/LevelPrototyping/Interactable/Door/BP_DoorFrame.BP_DoorFrame'
```

---

## 9. git status after the work

```
 M Content/Interaction/BP_Door.uasset
 M Content/LevelPrototyping/Interactable/Door/BP_DoorFrame.uasset
?? Docs/Terminal-Log/2026-08-30-35-door-toggle.md
?? Docs/Terminal-Log/2026-08-30-36-door-interact-lock.md
```

`BP_Door.uasset` is the file this command changed.

**`BP_DoorFrame.uasset` is newly modified and was not touched by this session** — it appears
alongside the `07.49.47` compile above. Recorded as an observation.

---

## 10. What is not verified

- **Nothing was run in PIE.** The whole door chain now exists — Interact → lock test → key
  consume → unlock → swing — but has never executed. Unconfirmed in particular:
  - that anything calls `Interact` on the door. The Character's F chain would have to send the
    BPI_Interact message to whatever it traces; that wiring was not inspected in this command
    and may not exist yet.
  - that `TryConsumeSelected` returns true when the player holds `Key_Stage1` in the selected
    slot. The function was built in command 34 and has never run.
  - that the door swings the right way, and that the 1-second `MoveComponentTo` looks right.
- **The `CastFailed` path silently does nothing.** That is what was specified, and it is correct
  for a non-Character interactor, but it also means a *Character* that somehow failed the cast
  would produce no diagnostic at all — unlike the `HUD MESSAGE DROPPED` path in
  `ShowHUDMessage`.
- **`bLocked` is set to false but never back to true.** Once unlocked the door stays unlocked
  for the rest of play. That follows from the design as specified; no re-lock was asked for.
- **The `K2Node_VariableSet_0` position change** in section 6 was not explained, only observed.
