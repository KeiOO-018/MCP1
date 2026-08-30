# 2026-08-30 — BP_ThirdPersonCharacter: TryAddItem and TryConsumeSelected

Two function graphs added. Nothing calls them yet. `BP_ThirdPersonCharacter:EventGraph` was not
touched — its node count is unchanged. `AssetTools.is_dirty` was not called.

**`write_graph_dsl` was not used at all in this command**, on any graph. Although DSL was
permitted on the two new graphs, both were built with `create_node` / `connect_pins` /
`set_pin_value` — see section 4 for why.

---

## 1. Pre-flight — all three checks passed

### P1 — existing functions

`list_functions` on BP_ThirdPersonCharacter:

```
["UserConstructionScript", "Move", "Aim", "ToggleCameraView", "RefreshHeldItem",
 "ShowHUDMessage", "CanJumpInternal"]
```

Exactly the seven named, in that order. **Neither `TryAddItem` nor `TryConsumeSelected`
existed.** Pass.

### P2 — variables

`list_variables` returned 11 names:

```
["bIsFirstPerson", "FirstPersonPitchMin", "FirstPersonPitchMax", "ThirdPersonPitchMin",
 "ThirdPersonPitchMax", "InventorySlots", "SelectedSlot", "CurrentHP", "MaxHP",
 "InteractDistance", "FoundSlotIndex"]
```

Types from the CDO property schema:

| variable | schema | reads as |
|---|---|---|
| `InventorySlots` | `{"type": "array", "items": {"type": "string"}}` | Array of Names |
| `SelectedSlot` | `{"type": "integer"}` | Integer |
| `FoundSlotIndex` | `{"type": "integer"}` | Integer |

All three present with the required types. Pass.

### P3 — EventGraph node count

`find_nodes` with an empty title on `BP_ThirdPersonCharacter:EventGraph`: **98** nodes.

---

## 2. The four EventGraph reference nodes — read only, not modified

Read with `get_node_infos` before anything was created. **None of these four nodes was modified
by this command.** No `connect_pins`, `break_pins`, `set_pin_value` or `delete_node` call in
this command named any node in `BP_ThirdPersonCharacter:EventGraph`, and the graph's node count
is unchanged at 98 (section 8).

**`K2Node_CallArrayFunction_2` — `Utilities|Array|FindItem` at (-640, 720)**

| pin | type | value | connection |
|---|---|---|---|
| in [0] `TargetArray` | Array of Names | `""` | <- `K2Node_VariableGet_5` [out 0] |
| in [1] `ItemToFind` | Name (by ref) | `""` | **unconnected** |
| out [0] `ReturnValue` | Integer | — | -> `K2Node_VariableSet_1` [in 1] |

**`K2Node_VariableSet_1` — `|SetFoundSlotIndex` at (-450, 220)**

| pin | type | value | connection |
|---|---|---|---|
| in [0] `execute` | Exec | `""` | <- `K2Node_DynamicCast_1` [out 0] |
| in [1] `FoundSlotIndex` | Integer | `"0"` | <- `K2Node_CallArrayFunction_2` [out 0] |
| out [0] `then` | Exec | — | -> `K2Node_IfThenElse_2` [in 0] |
| out [1] `Output_Get` | Integer | — | (nothing) |

**`K2Node_PromotableOperator_5` — `Math|Integer|integer>=integer` at (-400, 780)**

| pin | type | value | connection |
|---|---|---|---|
| in [0] `A` | Integer | `""` | <- `K2Node_VariableGet_8` [out 0] |
| in [1] `B` | Integer | `""` | **unconnected** |
| out [0] `ReturnValue` | Boolean | — | -> `K2Node_IfThenElse_2` [in 1] |

**`K2Node_CallArrayFunction_3` — `Utilities|Array|SetArrayElem` at (320, 220)**

| pin | type | value | connection |
|---|---|---|---|
| in [0] `execute` | Exec | `""` | <- `K2Node_IfThenElse_2` [out 0] |
| in [1] `TargetArray` | Array of Names | `""` | <- `K2Node_VariableGet_6` [out 0] |
| in [2] `Index` | Integer | `"0"` | <- `K2Node_VariableGet_9` [out 0] |
| in [3] `Item` | Name (by ref) | `""` | <- `K2Node_BreakStruct_1` [out 1] |
| in [4] `bSizeToFit` | Boolean | `"false"` | unconnected |
| out [0] `then` | Exec | — | -> `K2Node_CallFunction_18` [in 0] |

### What was mirrored from them

- `FindItem.ItemToFind` left unconnected at its default empty Name — the reference does the same.
- The `>=` node's `B` pin left unconnected. **Note:** the reference's `B` reads value `""`, not
  `"0"`. An empty int pin means zero, so `FoundSlotIndex >= 0` holds, but the literal string was
  mirrored rather than "improved" to `"0"`.
- `SetArrayElem.bSizeToFit` = `false`, `Item` typed `Name (by ref)`.
- The F chain uses **two separate** `GetInventorySlots` nodes (`VariableGet_5` for FindItem,
  `VariableGet_6` for SetArrayElem). TryAddItem mirrors that with two getters.

---

## 3. Step 3 STOP CHECK — Return nodes were produced

`add_function_param` with `input_param` false **did** produce a Return node in both graphs. Read
back immediately after the two params were added, before any body was built:

```
TryAddItem
  K2Node_FunctionEntry_0   |TryAddItem   out: [0 "then" Exec] [1 "RowName" Name]
  K2Node_FunctionResult_0  |ReturnNode   in:  [0 "execute" Exec] [1 "Success" Boolean]

TryConsumeSelected
  K2Node_FunctionEntry_0   |TryConsumeSelected  out: [0 "then" Exec] [1 "RowName" Name]
  K2Node_FunctionResult_0  |ReturnNode          in:  [0 "execute" Exec] [1 "Success" Boolean]
```

The check passed, so the build continued. No substitute was needed and none was improvised.

Worth recording: `read_graph_dsl` on both graphs at this point returned
`(fn TryAddItem (RowName))` and `(fn TryConsumeSelected (RowName))` — **the DSL representation
shows only the input, not the `Success` output.** That is a second instance of the DSL being
lossy on this project's graphs, alongside the EventGraph exec-body loss the command cited.

---

## 4. Why DSL was not used, even though it was allowed

Both functions require **one node to feed two pins**:

- TryAddItem: the `>=` node feeds both `Branch.Condition` and `Return.Success`, and the command
  says "Do not create a second comparison".
- TryConsumeSelected: the AND node feeds both `Branch.Condition` and `Return.Success`, and the
  single subtract feeds both the `Get(acopy)` index and the `SetArrayElem` index, with "Use ONE
  subtract node feeding both pins. Do not create two."

Command 30 established that this DSL's `bind` is textual substitution, not a node reference — a
bound value used twice produced two copies of the whole sub-expression. Using DSL here would
therefore have produced exactly the duplicate comparison and duplicate subtract the command
forbids. Building with `create_node` / `connect_pins` guarantees the shared-node requirement,
so that is what was done for both graphs.

---

## 5. TryAddItem — node inventory and pin connections

Graph: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:TryAddItem`
**12 nodes.** (`...` = the graph path above.)

| # | refPath | type_id |
|---|---|---|
| 1 | `....K2Node_FunctionEntry_0` | `\|TryAddItem` |
| 2 | `....K2Node_FunctionResult_0` | `\|ReturnNode` |
| 3 | `....K2Node_VariableGet_0` | `\|GetInventorySlots` |
| 4 | `....K2Node_CallArrayFunction_0` | `Utilities\|Array\|FindItem` |
| 5 | `....K2Node_VariableSet_0` | `\|SetFoundSlotIndex` |
| 6 | `....K2Node_VariableGet_1` | `\|GetFoundSlotIndex` |
| 7 | `....K2Node_PromotableOperator_0` | `Math\|Integer\|integer>=integer` |
| 8 | `....K2Node_IfThenElse_0` | `Utilities\|FlowControl\|Branch` |
| 9 | `....K2Node_VariableGet_2` | `\|GetInventorySlots` |
| 10 | `....K2Node_CallArrayFunction_1` | `Utilities\|Array\|SetArrayElem` |
| 11 | `....K2Node_CallFunction_0` | `\|RefreshHeldItem` |
| 12 | `....K2Node_CallFunction_1` | `\|ShowHUDMessage` |

### Full pin connection list

```
K2Node_FunctionEntry_0   |TryAddItem
  out [0] "then"    -> K2Node_VariableSet_0 [in 0]
  out [1] "RowName" (Name) -> K2Node_CallArrayFunction_1 [in 3]

K2Node_VariableGet_0   |GetInventorySlots
  out [0] "InventorySlots" (Array of Names) -> K2Node_CallArrayFunction_0 [in 0]

K2Node_CallArrayFunction_0   Utilities|Array|FindItem
  in  [0] "TargetArray" (Array of Names) = ""   <- K2Node_VariableGet_0 [out 0]
  in  [1] "ItemToFind"  (Name (by ref))  = ""   <- (unconnected)
  out [0] "ReturnValue" (Integer) -> K2Node_VariableSet_0 [in 1]

K2Node_VariableSet_0   |SetFoundSlotIndex
  in  [0] "execute"        (Exec)    <- K2Node_FunctionEntry_0 [out 0]
  in  [1] "FoundSlotIndex" (Integer) = "0"  <- K2Node_CallArrayFunction_0 [out 0]
  out [0] "then"       -> K2Node_IfThenElse_0 [in 0]
  out [1] "Output_Get" -> (nothing)

K2Node_VariableGet_1   |GetFoundSlotIndex
  out [0] "FoundSlotIndex" (Integer)
        -> K2Node_PromotableOperator_0 [in 0]
        -> K2Node_CallArrayFunction_1 [in 2]

K2Node_PromotableOperator_0   Math|Integer|integer>=integer
  in  [0] "A" (Integer) = ""  <- K2Node_VariableGet_1 [out 0]
  in  [1] "B" (Integer) = ""  <- (unconnected)
  out [0] "ReturnValue" (Boolean)
        -> K2Node_IfThenElse_0     [in 1]   (Branch.Condition)
        -> K2Node_FunctionResult_0 [in 1]   (Return.Success)

K2Node_IfThenElse_0   Utilities|FlowControl|Branch
  in  [0] "execute"   (Exec)    <- K2Node_VariableSet_0 [out 0]
  in  [1] "Condition" (Boolean) = "true" <- K2Node_PromotableOperator_0 [out 0]
  out [0] "then" -> K2Node_CallArrayFunction_1 [in 0]
  out [1] "else" -> K2Node_CallFunction_1 [in 0]

K2Node_VariableGet_2   |GetInventorySlots
  out [0] "InventorySlots" (Array of Names) -> K2Node_CallArrayFunction_1 [in 1]

K2Node_CallArrayFunction_1   Utilities|Array|SetArrayElem
  in  [0] "execute"     (Exec)            <- K2Node_IfThenElse_0 [out 0]
  in  [1] "TargetArray" (Array of Names)  <- K2Node_VariableGet_2 [out 0]
  in  [2] "Index"       (Integer) = "0"   <- K2Node_VariableGet_1 [out 0]
  in  [3] "Item"        (Name (by ref))   <- K2Node_FunctionEntry_0 [out 1]
  in  [4] "bSizeToFit"  (Boolean) = "false"  (unconnected)
  out [0] "then" -> K2Node_CallFunction_0 [in 0]

K2Node_CallFunction_0   |RefreshHeldItem
  in  [0] "execute" <- K2Node_CallArrayFunction_1 [out 0]
  in  [1] "self"    = ""  (unconnected — self call)
  out [0] "then" -> K2Node_FunctionResult_0 [in 0]

K2Node_CallFunction_1   |ShowHUDMessage
  in  [0] "execute" <- K2Node_IfThenElse_0 [out 1]
  in  [1] "self"    = ""  (unconnected — self call)
  in  [2] "Message" (String) = "INVENTORY FULL"
  out [0] "then" -> K2Node_FunctionResult_0 [in 0]

K2Node_FunctionResult_0   |ReturnNode
  in  [0] "execute" (Exec)    <- K2Node_CallFunction_0 [out 0], K2Node_CallFunction_1 [out 0]
  in  [1] "Success" (Boolean) <- K2Node_PromotableOperator_0 [out 0]
```

Both exec paths converge on the Return node's `execute`, which is legal — an exec input accepts
multiple incoming links.

**One getter note:** `K2Node_VariableGet_1` (`GetFoundSlotIndex`) feeds both the `>=` and the
`SetArrayElem.Index`. The F chain uses two separate getters there (`VariableGet_8` and
`VariableGet_9`); one was used here since it is a pure getter and nothing required a second.
This is a deviation from a strict mirror of the F chain and is called out rather than hidden.

---

## 6. TryConsumeSelected — node inventory and pin connections

Graph: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:TryConsumeSelected`
**13 nodes.**

| # | refPath | type_id |
|---|---|---|
| 1 | `....K2Node_FunctionEntry_0` | `\|TryConsumeSelected` |
| 2 | `....K2Node_FunctionResult_0` | `\|ReturnNode` |
| 3 | `....K2Node_VariableGet_0` | `\|GetSelectedSlot` |
| 4 | `....K2Node_PromotableOperator_0` | `Math\|Integer\|int-int` |
| 5 | `....K2Node_VariableGet_1` | `\|GetInventorySlots` |
| 6 | `....K2Node_GetArrayItem_0` | `Utilities\|Array\|Get(acopy)` |
| 7 | `....K2Node_PromotableOperator_1` | `Utilities\|Name\|Equal(Name)` |
| 8 | `....K2Node_PromotableOperator_2` | `Utilities\|Name\|NotEqual(Name)` |
| 9 | `....K2Node_CommutativeAssociativeBinaryOperator_0` | `Math\|Boolean\|ANDBoolean` |
| 10 | `....K2Node_IfThenElse_0` | `Utilities\|FlowControl\|Branch` |
| 11 | `....K2Node_VariableGet_2` | `\|GetInventorySlots` |
| 12 | `....K2Node_CallArrayFunction_0` | `Utilities\|Array\|SetArrayElem` |
| 13 | `....K2Node_CallFunction_0` | `\|RefreshHeldItem` |

### Full pin connection list

```
K2Node_FunctionEntry_0   |TryConsumeSelected
  out [0] "then"    -> K2Node_IfThenElse_0 [in 0]
  out [1] "RowName" (Name)
        -> K2Node_PromotableOperator_1 [in 1]   (Equal.B)
        -> K2Node_PromotableOperator_2 [in 0]   (NotEqual.A)

K2Node_VariableGet_0   |GetSelectedSlot
  out [0] "SelectedSlot" (Integer) -> K2Node_PromotableOperator_0 [in 0]

K2Node_PromotableOperator_0   Math|Integer|int-int          <- THE ONE SUBTRACT
  in  [0] "A" (Integer) = ""   <- K2Node_VariableGet_0 [out 0]
  in  [1] "B" (Integer) = "1"  (unconnected)
  out [0] "ReturnValue" (Integer)
        -> K2Node_GetArrayItem_0    [in 1]   (Get(acopy).Dimension 1)
        -> K2Node_CallArrayFunction_0 [in 2] (SetArrayElem.Index)

K2Node_VariableGet_1   |GetInventorySlots
  out [0] "InventorySlots" (Array of Names) -> K2Node_GetArrayItem_0 [in 0]

K2Node_GetArrayItem_0   Utilities|Array|Get(acopy)
  in  [0] "Array"       (Array of Names)  <- K2Node_VariableGet_1 [out 0]
  in  [1] "Dimension 1" (Integer) = "0"   <- K2Node_PromotableOperator_0 [out 0]
  out [0] "Output" (Name) -> K2Node_PromotableOperator_1 [in 0]

K2Node_PromotableOperator_1   Utilities|Name|Equal(Name)
  in  [0] "A" (Name) = ""  <- K2Node_GetArrayItem_0 [out 0]
  in  [1] "B" (Name) = ""  <- K2Node_FunctionEntry_0 [out 1]
  out [0] "ReturnValue" (Boolean) -> K2Node_CommutativeAssociativeBinaryOperator_0 [in 0]

K2Node_PromotableOperator_2   Utilities|Name|NotEqual(Name)
  in  [0] "A" (Name) = ""  <- K2Node_FunctionEntry_0 [out 1]
  in  [1] "B" (Name) = ""  <- (unconnected)
  out [0] "ReturnValue" (Boolean) -> K2Node_CommutativeAssociativeBinaryOperator_0 [in 1]

K2Node_CommutativeAssociativeBinaryOperator_0   Math|Boolean|ANDBoolean
  in  [0] "A" (Boolean) = "false" <- K2Node_PromotableOperator_1 [out 0]
  in  [1] "B" (Boolean) = "false" <- K2Node_PromotableOperator_2 [out 0]
  out [0] "ReturnValue" (Boolean)
        -> K2Node_IfThenElse_0     [in 1]   (Branch.Condition)
        -> K2Node_FunctionResult_0 [in 1]   (Return.Success)

K2Node_IfThenElse_0   Utilities|FlowControl|Branch
  in  [0] "execute"   (Exec)    <- K2Node_FunctionEntry_0 [out 0]
  in  [1] "Condition" (Boolean) = "true" <- K2Node_CommutativeAssociativeBinaryOperator_0 [out 0]
  out [0] "then" -> K2Node_CallArrayFunction_0 [in 0]
  out [1] "else" -> K2Node_FunctionResult_0 [in 0]

K2Node_VariableGet_2   |GetInventorySlots
  out [0] "InventorySlots" (Array of Names) -> K2Node_CallArrayFunction_0 [in 1]

K2Node_CallArrayFunction_0   Utilities|Array|SetArrayElem
  in  [0] "execute"     (Exec)            <- K2Node_IfThenElse_0 [out 0]
  in  [1] "TargetArray" (Array of Names)  <- K2Node_VariableGet_2 [out 0]
  in  [2] "Index"       (Integer) = "0"   <- K2Node_PromotableOperator_0 [out 0]
  in  [3] "Item"        (Name (by ref)) = ""  <- (unconnected — empty Name)
  in  [4] "bSizeToFit"  (Boolean) = "false"   (unconnected)
  out [0] "then" -> K2Node_CallFunction_0 [in 0]

K2Node_CallFunction_0   |RefreshHeldItem
  in  [0] "execute" <- K2Node_CallArrayFunction_0 [out 0]
  in  [1] "self"    = ""  (unconnected — self call)
  out [0] "then" -> K2Node_FunctionResult_0 [in 0]

K2Node_FunctionResult_0   |ReturnNode
  in  [0] "execute" (Exec)    <- K2Node_CallFunction_0 [out 0], K2Node_IfThenElse_0 [out 1]
  in  [1] "Success" (Boolean) <- K2Node_CommutativeAssociativeBinaryOperator_0 [out 0]
```

No bounds check was added, as specified.

---

## 7. The specific confirmations requested

### Return.Success and Branch.Condition come from the SAME node

**TryAddItem** — `K2Node_PromotableOperator_0` (the `>=`) has one output pin whose `to` list is:

```
["K2Node_IfThenElse_0[in 1]", "K2Node_FunctionResult_0[in 1]"]
```

Both destinations are on that single output. Reading it from the other side, `Branch [in 1]`
and `Return [in 1]` each list `K2Node_PromotableOperator_0 [out 0]` as their only source. **One
comparison node, no second one** — the graph contains exactly one node with a `>=` type_id.

**TryConsumeSelected** — `K2Node_CommutativeAssociativeBinaryOperator_0` (the AND) output `to`
list:

```
["K2Node_IfThenElse_0[in 1]", "K2Node_FunctionResult_0[in 1]"]
```

Same shape. The graph contains exactly one ANDBoolean node.

### ONE subtract node feeding two pins

`K2Node_PromotableOperator_0` in TryConsumeSelected is the only `int-int` node in that graph.
Its single output pin's `to` list:

```
["K2Node_GetArrayItem_0[in 1]", "K2Node_CallArrayFunction_0[in 2]"]
```

That is `Get(acopy).Dimension 1` and `SetArrayElem.Index` — the two places "SelectedSlot − 1" is
needed, both fed from one node. Its `B` pin reads `"1"`.

### FindItem.ItemToFind and NotEqual.B are unconnected and empty

```
TryAddItem  K2Node_CallArrayFunction_0  in [1] "ItemToFind" (Name (by ref))  value ""  from []
TryConsumeSelected  K2Node_PromotableOperator_2  in [1] "B" (Name)           value ""  from []
```

Both have an empty `from` list and an empty string value — unconnected, holding an empty Name.

### Promotable type_ids as created vs read back

Expected and not an error, per the command:

| passed to `create_node` | reads back as |
|---|---|
| `Utilities\|Operators\|GreaterEqual(>=)` | `Math\|Integer\|integer>=integer` |
| `Utilities\|Operators\|Subtract` | `Math\|Integer\|int-int` |
| `Utilities\|Operators\|Equal(==)` | `Utilities\|Name\|Equal(Name)` |
| `Utilities\|Operators\|NotEqual(!=)` | `Utilities\|Name\|NotEqual(Name)` |

The four type_ids the command listed as "confirmed present" that are in fact **not creatable**
are `Utilities|Name|Equal(Name)`, `Utilities|Name|NotEqual(Name)` and
`Math|Integer|integer>=integer` — `find_node_types` for `Math|Integer|integer>=integer` returned
`[]`, and the `Utilities|Name|` filter returned only `EnumtoName` and `MakeLiteralName`. They
are read-back names, not palette names. The promotables above were used instead and resolve to
exactly those type_ids once wired, which is why the requirement is still met.
`Utilities|Array|FindItem`, `Utilities|Array|SetArrayElem`, `Utilities|Array|Get(acopy)`,
`Utilities|FlowControl|Branch` and `Math|Boolean|ANDBoolean` were creatable under the names
given.

---

## 8. EventGraph node count after the command

`find_nodes` with an empty title on `BP_ThirdPersonCharacter:EventGraph`: **98**.

Equal to P3. The EventGraph was not touched — every `create_node` and `connect_pins` call in
this command targeted `:TryAddItem` or `:TryConsumeSelected`.

---

## 9. list_functions after the change

```
["UserConstructionScript", "Move", "Aim", "ToggleCameraView", "RefreshHeldItem",
 "ShowHUDMessage", "TryAddItem", "TryConsumeSelected", "CanJumpInternal"]
```

Nine names — the original seven plus the two new ones.

---

## 10. Compile result

`BlueprintTools.compile_blueprint` on BP_ThirdPersonCharacter, `warnings_as_errors` = `false`,
returned:

```
{"returnValue":null}
```

The tool raises on error; it did not raise.

```
[2026.08.30-05.24.57:310][228]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
```

No error and no warning followed it. **Compiled clean.**

`AssetTools.save_assets` -> `true`. Content validation ran on save:

```
[2026.08.30-05.25.08:441][261]AssetCheck: /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter Validating asset
```

Nine validators, no failure reported.

**Not verified:** no tool reports a Blueprint's compiled status flag directly. "Compiled clean"
rests on the call not raising plus an empty log window.

---

## 11. Errors and warnings — exact English text

### 11.1 From this work

No tool call raised. One set of warnings **was** produced by a call this command made — the
`ObjectTools.list_properties` read in pre-flight P2, which generates a JSON schema for the CDO
and cannot represent delegate properties:

```
[2026.08.30-05.21.35:688][517]LogJson: Warning: Property "ReceiveRestartedDelegate" type FPawnRestartedSignature unhandled during Json schema generation.
[2026.08.30-05.21.35:688][517]LogJson: Warning: Property "ReceiveControllerChangedDelegate" type FPawnControllerChangedSignature unhandled during Json schema generation.
[2026.08.30-05.21.35:688][517]LogJson: Warning: Property "OnCharacterMovementUpdated" type FCharacterMovementUpdatedSignature unhandled during Json schema generation.
[2026.08.30-05.21.35:688][517]LogJson: Warning: Property "MovementModeChangedDelegate" type FMovementModeChangedSignature unhandled during Json schema generation.
[2026.08.30-05.21.35:688][517]LogJson: Warning: Property "LandedDelegate" type FLandedSignature unhandled during Json schema generation.
[2026.08.30-05.21.35:688][517]LogJson: Warning: Property "OnReachedJumpApex" type FCharacterReachedApexSignature unhandled during Json schema generation.
```

These are read-side warnings from the schema generator, not Blueprint compile warnings, and
nothing was modified by that call. The three property types the check needed
(`inventorySlots`, `selectedSlot`, `foundSlotIndex`) were returned correctly.

### 11.2 Present in the log but NOT from this work

A compile of a Blueprint this session did not touch, between the previous command's save
(`04.48`) and this command's first action:

```
[2026.08.30-04.52.27:253][949]LogBlueprint: Compiling Blueprint '/Game/LevelPrototyping/Interactable/Door/BP_DoorFrame.BP_DoorFrame'
```

Recorded as an observation only; `BP_DoorFrame` was not read or modified here.

---

## 12. git status after the work

```
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

One file, the one this command changed. The `BP_Door.uasset` and `BP_ThirdPersonHUD.uasset`
entries that appeared in the previous three reports have gone — those were committed between
commands.

---

## 13. What is not verified

- **Neither function is called by anything.** That is by design — commands 36 and 37. Until
  then neither has ever executed, and nothing here was run in PIE.
- **That `FindItem` with an empty `ItemToFind` really returns the first empty slot.** It
  mirrors the F chain, which presumably works, but the semantics were not tested — only the
  wiring was copied.
- **That `TryAddItem` returns the right thing when the array is full.** `Success` is wired to
  the `>=` result, so a full inventory returns false and shows INVENTORY FULL; that follows from
  the wiring but was not exercised.
- **That out-of-range `Get(acopy)` behaves as the command states** (logs a warning, returns the
  default). The command asserts this from `GenericArray_Get` in `KismetArrayLibrary.cpp`; that
  source was not opened and the claim was not independently checked. The bounds check was
  omitted on the strength of it.
- **`SelectedSlot` is 1-based here** — the subtract assumes it. That matches the E and Q chains
  in the EventGraph, but no runtime check was made.
