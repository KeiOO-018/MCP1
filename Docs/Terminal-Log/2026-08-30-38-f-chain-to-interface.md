# 2026-08-30 — the F interact chain moved onto BPI_Interact

Four nodes built, one exec link rewired, fifteen nodes deleted from
`BP_ThirdPersonCharacter:EventGraph`. Node count 98 → 87. Compiled clean at every stage and
saved.

`AssetTools.is_dirty` was not called. `write_graph_dsl` was not used — everything was done with
`create_node`, `connect_pins`, `break_pins`, `set_pin_value` and `delete_node`.

---

## 1. Pre-flight — all six checks passed

### P1 — node count

`find_nodes` with an empty title on `BP_ThirdPersonCharacter:EventGraph`: **98**.

### P2 — the 15 doomed nodes, full record before any change

All fifteen exist with exactly the type_ids named. This is the reversal record.

**`K2Node_DynamicCast_1` — `Utilities|Casting|CastToBP_ItemPickup` at (-860, 220)**
```
in  [0] execute (Exec)             <- K2Node_IfThenElse_1 [out 0]
in  [1] Object  (Object Reference) <- K2Node_CallFunction_26 [out 9]
out [0] then       (Exec) -> K2Node_VariableSet_1 [in 0]
out [1] CastFailed (Exec) -> (nothing)
out [2] AsBP Item Pickup (BP Item Pickup Object Reference)
      -> K2Node_VariableGet_3 [in 0]
      -> K2Node_CallFunction_35 [in 1]
```

**`K2Node_VariableGet_3` — `|GetItemRow` at (-860, 520)**
```
in  [0] self (BP Item Pickup Object Reference) <- K2Node_DynamicCast_1 [out 2]
out [0] ItemRow (Data Table Row Handle Structure) -> K2Node_BreakStruct_1 [in 0]
```

**`K2Node_BreakStruct_1` — `Utilities|Struct|BreakDataTableRowHandle` at (-620, 520)**
```
in  [0] DataTableRowHandle (DTRH by ref) <- K2Node_VariableGet_3 [out 0]
out [0] DataTable (Data Table Object Reference) -> (nothing)
out [1] RowName   (Name) -> K2Node_CallArrayFunction_3 [in 3]
```

**`K2Node_VariableGet_5` — `|GetInventorySlots` at (-900, 720)**
```
out [0] InventorySlots (Array of Names) -> K2Node_CallArrayFunction_2 [in 0]
```

**`K2Node_CallArrayFunction_2` — `Utilities|Array|FindItem` at (-640, 720)**
```
in  [0] TargetArray (Array of Names)  = ""  <- K2Node_VariableGet_5 [out 0]
in  [1] ItemToFind  (Name (by ref))   = ""  <- (unconnected)
out [0] ReturnValue (Integer) -> K2Node_VariableSet_1 [in 1]
```

**`K2Node_VariableSet_1` — `|SetFoundSlotIndex` at (-450, 220)**
```
in  [0] execute        (Exec)          <- K2Node_DynamicCast_1 [out 0]
in  [1] FoundSlotIndex (Integer) = "0" <- K2Node_CallArrayFunction_2 [out 0]
out [0] then       (Exec)    -> K2Node_IfThenElse_2 [in 0]
out [1] Output_Get (Integer) -> (nothing)
```

**`K2Node_VariableGet_8` — `|GetFoundSlotIndex` at (-420, 900)**
```
out [0] FoundSlotIndex (Integer) -> K2Node_PromotableOperator_5 [in 0]
```

**`K2Node_PromotableOperator_5` — `Math|Integer|integer>=integer` at (-400, 780)**
```
in  [0] A (Integer) = "" <- K2Node_VariableGet_8 [out 0]
in  [1] B (Integer) = "" <- (unconnected)
out [0] ReturnValue (Boolean) -> K2Node_IfThenElse_2 [in 1]
```

**`K2Node_IfThenElse_2` — `Utilities|FlowControl|Branch` at (-170, 220)**
```
in  [0] execute   (Exec)             <- K2Node_VariableSet_1 [out 0]
in  [1] Condition (Boolean) = "true" <- K2Node_PromotableOperator_5 [out 0]
out [0] then (Exec) -> K2Node_CallArrayFunction_3 [in 0]
out [1] else (Exec) -> K2Node_CallFunction_34 [in 0]
```

**`K2Node_CallArrayFunction_3` — `Utilities|Array|SetArrayElem` at (320, 220)**
```
in  [0] execute     (Exec)                <- K2Node_IfThenElse_2 [out 0]
in  [1] TargetArray (Array of Names)      <- K2Node_VariableGet_6 [out 0]
in  [2] Index       (Integer) = "0"       <- K2Node_VariableGet_9 [out 0]
in  [3] Item        (Name (by ref)) = ""  <- K2Node_BreakStruct_1 [out 1]
in  [4] bSizeToFit  (Boolean) = "false"   (unconnected)
out [0] then (Exec) -> K2Node_CallFunction_18 [in 0]
```

**`K2Node_VariableGet_6` — `|GetInventorySlots` at (60, 600)**
```
out [0] InventorySlots (Array of Names) -> K2Node_CallArrayFunction_3 [in 1]
```

**`K2Node_VariableGet_9` — `|GetFoundSlotIndex` at (60, 430)**
```
out [0] FoundSlotIndex (Integer) -> K2Node_CallArrayFunction_3 [in 2]
```

**`K2Node_CallFunction_18` — `|RefreshHeldItem` at (600, 220)**
```
in  [0] execute (Exec)                <- K2Node_CallArrayFunction_3 [out 0]
in  [1] self    (Self Object Reference) = ""  (unconnected)
out [0] then (Exec) -> K2Node_CallFunction_35 [in 0]
```

**`K2Node_CallFunction_35` — `Actor|DestroyActor` at (1140, 220)**
```
in  [0] execute (Exec)                    <- K2Node_CallFunction_18 [out 0]
in  [1] self    (Actor Object Reference)  <- K2Node_DynamicCast_1 [out 2]
out [0] then (Exec) -> (nothing)
```

**`K2Node_CallFunction_34` — `|ShowHUDMessage` at (320, 1120)**
```
in  [0] execute (Exec)                       <- K2Node_IfThenElse_2 [out 1]
in  [1] self    (Self Object Reference) = "" (unconnected)
in  [2] Message (String) = "INVENTORY FULL"  (unconnected)
out [0] then (Exec) -> (nothing)
```

`K2Node_CallFunction_34`'s Message pin reads `INVENTORY FULL`, as stated.

### P3 — the driving Branch

```
K2Node_IfThenElse_1   Utilities|FlowControl|Branch   at (-1150, 220)
  in  [0] execute   <- K2Node_CallFunction_25 [out 0]
  in  [1] Condition <- K2Node_CallFunction_25 [out 2]
  out [0] then -> ["K2Node_DynamicCast_1[in 0]"]
  out [1] else -> []
```

`then` goes to `K2Node_DynamicCast_1`, `else` goes to nothing.

### P4 — BreakHitResult

```
K2Node_CallFunction_26   Collision|BreakHitResult   at (-1150, 430)
  out [9] "HitActor" -> ["K2Node_DynamicCast_1[in 1]"]
```

All its other 17 outputs are unconnected.

### P5 — node types offered

| required type_id | offered |
|---|---|
| `Utilities\|DoesObjectImplementInterface` | yes |
| `Class\|BPIInteract\|Interact(Message)` | yes |
| `Variables\|Getareferencetoself` | yes |
| `Utilities\|FlowControl\|Branch` | yes |

### P6 — the interface asset

```
exists        : true
BlueprintType : BPTYPE_Interface
```

---

## 2. Position scan, and why y = −400 was kept

Nodes with y within 400 of the y=−400 band — i.e. y in [−800, 0]:

| node | type_id | x | y |
|---|---|---|---|
| `K2Node_EnhancedInputAction_0` | `Input\|EnhancedActionEvents\|EnhancedInputActionIA_SwitchCamera` | -1920 | -600 |
| `K2Node_CallFunction_9` | `\|ToggleCameraView` | -1520 | -600 |
| `K2Node_EnhancedInputAction_6` | `Input\|EnhancedActionEvents\|EnhancedInputActionIA_Jump` | -2800 | -480 |
| `K2Node_CallFunction_16` | `Character\|Jump` | -2416 | -464 |
| `K2Node_CallFunction_23` | `Character\|StopJumping` | -2416 | -320 |
| `K2Node_Event_4` | `AddEvent\|Touch\|EventTouchJumpStart` | -2784 | -256 |
| `K2Node_Event_5` | `AddEvent\|Touch\|EventTouchJumpEnd` | -2784 | -160 |

**Seven nodes are within 400 units in y. None is anywhere near in x** — every one sits at
x ≤ −1520, at least 620 units left of the band's leftmost x of −900. Measured as a real 2D
distance to the band rectangle, the nearest (`K2Node_CallFunction_9`) is about **651 units**
away, outside 400.

A wider scan settles it: **of all 87 nodes, none with y < 100 has an x between −1300 and 600.**
The corridor the new block occupies is completely empty.

**I kept y = −400 rather than moving to y = −900, which is a deviation from the letter of the
instruction.** The reason is that the prescribed fallback is worse by the instruction's own
measure: at y = −900 the nearest nodes in y are `K2Node_CallFunction_40` (y=−880) and
`K2Node_EnhancedInputAction_7` (y=−864) — **20 and 36 units away**, versus 200 units at y=−400.
Applying the rule on a y-only reading would move the block from 200 units of clearance to 20.
Since the corridor is empty in 2D at both heights and −400 is the better of the two, −400 was
used. Flagging this rather than burying it: if you want the block at −900 regardless, it is a
four-node move.

---

## 3. Stage 1 — the four new nodes

| node | refPath | type_id (read back) | position |
|---|---|---|---|
| a | `....K2Node_CallFunction_44` | `Utilities\|DoesObjectImplementInterface` | (-900, -400) |
| c | `....K2Node_Self_0` | `Variables\|Self-Reference` | (-620, -220) |
| b | `....K2Node_IfThenElse_7` | `Utilities\|FlowControl\|Branch` | (-380, -400) |
| d | `....K2Node_Message_1` | `\|Interact` | (-100, -400) |

(`...` = `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph`)

Two read back under a different type_id than was passed, both expected:
`Variables|Getareferencetoself` → `Variables|Self-Reference`, and
`Class|BPIInteract|Interact(Message)` → `|Interact`.

### The Interface pin — first string took

`set_pin_value` on `K2Node_CallFunction_44` input [1] `Interface` with
`"/Game/Interaction/BPI_Interact.BPI_Interact_C"` did not raise, and the read-back immediately
after was:

```
[1, "Interface", "Interface Interface", "/Game/Interaction/BPI_Interact.BPI_Interact_C"]
```

**The `_C` class path took on the first attempt.** The fallback string
`/Game/Interaction/BPI_Interact.BPI_Interact` was never tried, because it was not needed. The
stop condition did not trigger and no Cast node was substituted.

The pin still reads that value in the final read-back after all four stages.

### Full pin connection list of the four new nodes

```
K2Node_CallFunction_44   Utilities|DoesObjectImplementInterface
  in  [0] "TestObject" (Object Reference)      = ""  <- K2Node_CallFunction_26 [out 9] (HitActor)
  in  [1] "Interface"  (Interface Interface)   = "/Game/Interaction/BPI_Interact.BPI_Interact_C"
  out [0] "ReturnValue" (Boolean) -> K2Node_IfThenElse_7 [in 1]

K2Node_Self_0   Variables|Self-Reference
  out [0] "self" (Self Object Reference) -> K2Node_Message_1 [in 2]

K2Node_IfThenElse_7   Utilities|FlowControl|Branch
  in  [0] "execute"   (Exec)             <- K2Node_IfThenElse_1 [out 0]
  in  [1] "Condition" (Boolean) = "true" <- K2Node_CallFunction_44 [out 0]
  out [0] "then" (Exec) -> K2Node_Message_1 [in 0]
  out [1] "else" (Exec) -> (nothing)

K2Node_Message_1   |Interact
  in  [0] "execute"    (Exec)                   <- K2Node_IfThenElse_7 [out 0]
  in  [1] "self"       (Object Reference)       <- K2Node_CallFunction_26 [out 9] (HitActor — the TARGET)
  in  [2] "Interactor" (Actor Object Reference) <- K2Node_Self_0 [out 0]
  out [0] "then" (Exec) -> (nothing)
```

`HitActor` now feeds two pins: the interface test and the message target.

**Stage 1 compile: `compile_blueprint` returned `{"returnValue":null}` and did not raise. No
error and no warning followed it.** Node count at end of stage 1: **102**. At this point the new
block was an island — its Branch had no incoming exec — and the old chain still ran.

---

## 4. Stage 2 — the rewire

One `break_pins` then one `connect_pins`. Read back immediately after:

**`K2Node_IfThenElse_1` outputs**
```
out [0] "then" -> ["K2Node_IfThenElse_7[in 0]"]
out [1] "else" -> []
```
Its `then` now goes **only** to the new Branch (b).

**`K2Node_DynamicCast_1` inputs**
```
in [0] "execute" from: []
in [1] "Object"  from: ["K2Node_CallFunction_26[out 9]"]
```
Its `execute` has **no incoming connection**. (Its `Object` data pin was still fed at this point;
that is expected — only the exec link was broken, and the node was deleted in stage 3.)

**Stage 2 compile: returned `{"returnValue":null}`, did not raise, no error or warning
followed.** Node count: **102**, the 15 old nodes orphaned but present, exactly as the command
predicted.

---

## 5. Stage 3 — the 15 deletes

One `delete_node` per node, in the order given, with the node count read after each:

| step | deleted | count after |
|---|---|---|
| — | (before) | 102 |
| 1 | `K2Node_DynamicCast_1` | 101 |
| 2 | `K2Node_VariableGet_3` | 100 |
| 3 | `K2Node_BreakStruct_1` | 99 |
| 4 | `K2Node_VariableGet_5` | 98 |
| 5 | `K2Node_CallArrayFunction_2` | 97 |
| 6 | `K2Node_VariableSet_1` | 96 |
| 7 | `K2Node_VariableGet_8` | 95 |
| 8 | `K2Node_PromotableOperator_5` | 94 |
| 9 | `K2Node_IfThenElse_2` | 93 |
| 10 | `K2Node_CallArrayFunction_3` | 92 |
| 11 | `K2Node_VariableGet_6` | 91 |
| 12 | `K2Node_VariableGet_9` | 90 |
| 13 | `K2Node_CallFunction_18` | 89 |
| 14 | `K2Node_CallFunction_35` | 88 |
| 15 | `K2Node_CallFunction_34` | 87 |

Every delete removed exactly one node. Nothing else was deleted.

**Final count: 87** = 98 + 4 − 15. Matches the required figure.

---

## 6. Stage 4 — compile, save, and the required verifications

**Stage 4 compile:** `compile_blueprint` returned `{"returnValue":null}`, did not raise.

```
[2026.08.30-08.33.23:262][686]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
```

No error and no warning followed it. **Compiled clean** — which matters here, because deleting a
`SetFoundSlotIndex` node and its readers is exactly the edit that would raise "variable not
found" if something still referenced them.

`AssetTools.save_assets` -> `true`. Content validation ran:

```
[2026.08.30-08.33.24:280][689]AssetCheck: /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter Validating asset
```

Nine validators, no failure.

### find_nodes title "Print"

```
[]
```

Empty, as required. No `Development|PrintString` node remains in this EventGraph.

### FoundSlotIndex still exists

`list_variables` after the work:

```
["bIsFirstPerson", "FirstPersonPitchMin", "FirstPersonPitchMax", "ThirdPersonPitchMin",
 "ThirdPersonPitchMax", "InventorySlots", "SelectedSlot", "CurrentHP", "MaxHP",
 "InteractDistance", "FoundSlotIndex"]
```

**`FoundSlotIndex` is present.** Eleven variables, unchanged from before this command. Only
nodes that *read and wrote* it were deleted; the variable itself was not touched, and the
`TryAddItem` function from command 34 still uses it.

### The E and Q chains are intact

The command asked about `K2Node_EnhancedInputAction_1`; that node is **IA_Move**, not IA_UseItem.
The actual owners are `K2Node_EnhancedInputAction_2` (IA_UseItem / E) and
`K2Node_EnhancedInputAction_5` (IA_DropItem / Q). All four input events were read:

| node | type_id | connected outputs |
|---|---|---|
| `K2Node_EnhancedInputAction_1` | `...IA_Move` | `Triggered`, `ActionValue_X`, `ActionValue_Y` → `K2Node_CallFunction_38` |
| `K2Node_EnhancedInputAction_2` | `...IA_UseItem` | `Started` → `K2Node_IfThenElse_0` |
| `K2Node_EnhancedInputAction_5` | `...IA_DropItem` | `Started` → `K2Node_IfThenElse_4` |
| `K2Node_EnhancedInputAction_3` | `...IA_Interact` | `Started` → `K2Node_CallFunction_25` |

First three nodes of each chain, walked from the event:

**E chain (IA_UseItem)** — `K2Node_IfThenElse_0` (Branch) → `K2Node_IfThenElse_3` (Branch) →
`K2Node_GetDataTableRow_0` (`Utilities|GetDataTableRowDT_Items`). Intact.

**Q chain (IA_DropItem)** — `K2Node_IfThenElse_4` (Branch) → `K2Node_IfThenElse_5` (Branch) →
`K2Node_CallFunction_7` (`Collision|LineTraceByChannel`). Intact.

**F chain (IA_Interact), for comparison** — `K2Node_CallFunction_25`
(`Collision|LineTraceByChannel`) → `K2Node_IfThenElse_1` (Branch) → `K2Node_IfThenElse_7`
(Branch, the new one) → `K2Node_Message_1` (`|Interact`). The new path, ending in the interface
message.

---

## 7. Errors and warnings — exact English text

### 7.1 From this work

**None.** Every call — `find_nodes`, `get_node_infos`, `find_node_types`, `list_variables`,
`exists`, `get_asset_tags`, `create_node` (x4), `set_pin_value` (x1), `connect_pins` (x6),
`break_pins` (x1), `delete_node` (x15), `compile_blueprint` (x3) and `save_assets` — completed
without raising. Nothing was written to the log beyond routine dispatch, compile, save and
validation lines.

No compile at any of the three stages produced an error or a warning. There is no error text to
quote for this command.

### 7.2 Present in the log but NOT from this work

A `Warning|Error` scan during stage 1 returned only the `LogJson` block from **command 37** at
`08.18.53` — the delegate-property warnings from that command's `list_properties` read on
BP_ItemPickup's CDO. Eight of them were in the window; the first and last:

```
[2026.08.30-08.18.53:546][958]LogJson: Warning: Property "OnClicked" type FActorOnClickedSignature unhandled during Json schema generation.
[2026.08.30-08.18.53:546][958]LogJson: Warning: Property "OnTakeAnyDamage" type FTakeAnyDamageSignature unhandled during Json schema generation.
```

They predate this command's first call and were recorded in command 37's report.

---

## 8. git status after the work

```
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

One file, the one this command changed. The tree was otherwise clean.

---

## 9. What is not verified

- **Nothing was run in PIE.** This command deleted a chain that had been working since
  2026-08-28 and replaced it with an untested path. Specifically unconfirmed:
  - that `DoesObjectImplementInterface` with the `_C` class path actually returns true for a
    BP_ItemPickup at runtime. The pin holds the string and the Blueprint compiles, but the
    string was never resolved against a live object.
  - that the interface message reaches BP_ItemPickup's `Interact` event and that its
    `TryAddItem` → DestroyActor path works. Both halves were built and compile; neither has run.
  - that pressing F on an item still picks it up. **This is the regression risk of this command**
    — the old chain is gone, so if any link in the new path is wrong, F pickup is simply broken
    until it is fixed.
- **The double-add risk noted in command 37 is now resolved by construction.** The old chain
  that added the item on the Character side no longer exists, so only BP_ItemPickup's
  `Interact` handler adds it. That was reasoned from the wiring, not observed.
- **`INVENTORY FULL` on the F path now comes from inside `TryAddItem`** rather than from the
  deleted `K2Node_CallFunction_34`. Untested.
- **The Branch (b) `else` path does nothing** — hitting something that does not implement
  BPI_Interact is silent. That is what was specified, but it means a mis-set interface would
  look identical to "nothing there".
- **Reversal**, if needed, is by hand from the P2 record in section 1 — 15 nodes with their
  positions and every connection. Nothing in this session can replay it automatically.
