# 2026-08-30 — Q (drop item) spawn and slot clear — BUILT

Replaces the blocked command recorded in `2026-08-30-26-drop-item-spawn.md`. With
`ItemRow` now Expose on Spawn, the plain `Game|SpawnActorfromClass` node grew an `ItemRow`
input pin and the deferred Begin/Finish pair was not needed.

All 7 nodes created and wired, Blueprint compiled clean and saved. The Q island is complete.

---

## 1. Dirty check before any work

`AssetTools.is_dirty` on `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`, called before
anything else:

```
{"returnValue":false}
```

**Not dirty.** Third command in a row that started clean.

---

## 2. STEP 0 — does the ItemRow pin appear?

**Yes.** `Game|SpawnActorfromClass` was created at (1650, 3400), producing
`K2Node_SpawnActorFromClass_0`, then its `Class` pin (index 1) was set to
`/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C`.

### Input pins at creation, before Class was set — verbatim

```
[0, "execute", "Exec", ""]
[1, "Class", "Actor Class Reference", ""]
[2, "SpawnTransform", "Transform", ""]
[3, "CollisionHandlingOverride", "ESpawnActorCollisionHandlingMethod Enum", "Undefined"]
[4, "TransformScaleMethod", "ESpawnActorScaleMethod Enum", "MultiplyWithRoot"]
[5, "Owner", "Actor Object Reference", ""]
```

type_id at this point: `Game|SpawnActorNONE`. Outputs: `then` (Exec),
`ReturnValue` (Actor Object Reference).

### Input pins after Class was set — verbatim

```
[0, "execute", "Exec", ""]
[1, "Class", "Actor Class Reference", "/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C"]
[2, "SpawnTransform", "Transform", ""]
[3, "CollisionHandlingOverride", "ESpawnActorCollisionHandlingMethod Enum", "Undefined"]
[4, "TransformScaleMethod", "ESpawnActorScaleMethod Enum", "MultiplyWithRoot"]
[5, "Owner", "Actor Object Reference", ""]
[6, "ItemRow", "Data Table Row Handle Structure", ""]
[7, "Instigator", "Pawn Object Reference", ""]
```

**`ItemRow` is present at index 6, reading as type `Data Table Row Handle Structure`.**

Setting the Class pin reconstructed the node and added three things: the `ItemRow` pin
(index 6), an `Instigator` pin (index 7), and a narrowed return type — `ReturnValue` went from
`Actor Object Reference` to `BP Item Pickup Object Reference`. The node's type_id changed from
`Game|SpawnActorNONE` to `Game|SpawnActorBPItemPickup`.

This is direct confirmation that the hand-edit worked: `ItemRow` on BP_ItemPickup is now both
Instance Editable and Expose on Spawn. The condition that blocked the previous command is gone,
so the build continued.

The node was created at its final position (1650, 3400) in the first place, so no move was
needed and no second SpawnActor node was created.

---

## 3. Nodes created — name, type_id, x, y (read back)

| # | role | node name | type_id (read back) | x | y |
|---|---|---|---|---|---|
| 21 | Break Hit Result | `K2Node_CallFunction_11` | `Collision\|BreakHitResult` | 700 | 3800 |
| 22 | vector + vector (lift 50) | `K2Node_PromotableOperator_15` | `Math\|Vector\|vector+vector` | 1000 | 3900 |
| 23 | Make Transform | `K2Node_CallFunction_12` | `Math\|Transform\|MakeTransform` | 1300 | 3900 |
| 25 | Make DataTableRowHandle | `K2Node_MakeStruct_0` | `Utilities\|Struct\|MakeDataTableRowHandle` | 1300 | 4100 |
| 24 | Spawn Actor | `K2Node_SpawnActorFromClass_0` | `Game\|SpawnActorBPItemPickup` | 1650 | 3400 |
| 26 | Set Array Elem | `K2Node_CallArrayFunction_5` | `Utilities\|Array\|SetArrayElem` | 2000 | 3400 |
| 27 | Refresh Held Item | `K2Node_CallFunction_13` | `\|RefreshHeldItem` | 2350 | 3400 |

All within the requested band: x 700–2350, y 3400–4100.

### type_ids passed vs read back

Every registry entry from the previous report worked as given. Nothing had to be looked up
again, and no `create_node` call failed in this command.

| passed to `create_node` | reads back as |
|---|---|
| `Collision\|BreakHitResult` | `Collision\|BreakHitResult` |
| `Utilities\|Operators\|Add` | `Math\|Vector\|vector+vector` |
| `Math\|Transform\|MakeTransform` | `Math\|Transform\|MakeTransform` |
| `Utilities\|Struct\|MakeDataTableRowHandle` | `Utilities\|Struct\|MakeDataTableRowHandle` |
| `Game\|SpawnActorfromClass` | `Game\|SpawnActorBPItemPickup` |
| `Utilities\|Array\|SetArrayElem` | `Utilities\|Array\|SetArrayElem` |
| `CallFunction\|RefreshHeldItem` | `\|RefreshHeldItem` |

Two read back differently from what was passed, both expected:

- **`Utilities|Operators|Add` -> `Math|Vector|vector+vector`.** A wildcard promotable that
  resolved when the Vector was connected, same as in the previous two commands. It showed
  `Utilities|TimeManagement|FrameNumber+Int` immediately after creation.
- **`Game|SpawnActorfromClass` -> `Game|SpawnActorBPItemPickup`.** The type_id carries the
  chosen class, so it changes when the Class pin is set. Same shape as `|RefreshHeldItem`
  reading back without its `CallFunction` prefix — that one matches the E chain's
  `K2Node_CallFunction_28`, whose type_id is also `|RefreshHeldItem`.

---

## 4. Input pins of nodes 21–27 — read back

**21. `K2Node_CallFunction_11` — Break Hit Result**
- `Hit` (Hit Result Structure (by ref)) = `""` <- `K2Node_CallFunction_7` [out 1] (`OutHit`)

Outputs: only `Location` [4] (Vector) is connected, to `K2Node_PromotableOperator_15` [in 0].
The other 17 outputs — `bBlockingHit`, `bInitialOverlap`, `Time`, `Distance`, `ImpactPoint`,
`Normal`, `ImpactNormal`, `PhysMat`, `HitActor`, `HitComponent`, `HitBoneName`, `BoneName`,
`HitItem`, `ElementIndex`, `FaceIndex`, `TraceStart`, `TraceEnd` — all read `to: []`, left open
as instructed.

**22. `K2Node_PromotableOperator_15` — vector + vector**
- `A` (Vector) = `""` <- `K2Node_CallFunction_11` [out 4] (`Location`)
- `B` (Vector) = **`"0, 0, 50"`** — no connection, a literal pin value

Output `ReturnValue` (Vector) -> `K2Node_CallFunction_12` [in 0].

**The B value was read back and confirmed.** The node was read three times: as a Wildcard at
creation, as `[1, "B", "Vector", ""]` after `A` was connected, and as
`[1, "B", "Vector", "0, 0, 50"]` after the set. The value took. This was checked explicitly
because in command 25 a `set_pin_value` with a type-mismatched string returned `null` and
silently changed nothing.

**23. `K2Node_CallFunction_12` — Make Transform**
- `Location` (Vector) = `"0, 0, 0"` <- `K2Node_PromotableOperator_15` [out 0]
- `Rotation` (Rotator) = `"0, 0, 0"` — no connection, left at default
- `Scale` (Vector) = `"1.000000,1.000000,1.000000"` — no connection, left at default

Output `ReturnValue` (Transform) -> `K2Node_SpawnActorFromClass_0` [in 2].

The `Location` pin still shows its `0, 0, 0` literal; that value is dead because the pin is
connected.

**25. `K2Node_MakeStruct_0` — Make DataTableRowHandle**
- `DataTable` (Data Table Object Reference) = `"/Game/Inventory/DT_Items.DT_Items"` — no
  connection
- `RowName` (Name) = `"None"` <- `K2Node_GetArrayItem_1` [out 0]

Output `DataTableRowHandle` -> `K2Node_SpawnActorFromClass_0` [in 6] (`ItemRow`).

**24. `K2Node_SpawnActorFromClass_0` — Spawn Actor**

| pin | type | value | source |
|---|---|---|---|
| `execute` | Exec | — | `K2Node_IfThenElse_6` [out 0] (`then`) |
| `Class` | Actor Class Reference | `/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C` | — |
| `SpawnTransform` | Transform | `""` | `K2Node_CallFunction_12` [out 0] |
| `CollisionHandlingOverride` | ESpawnActorCollisionHandlingMethod Enum | `Undefined` | — (left at default) |
| `TransformScaleMethod` | ESpawnActorScaleMethod Enum | `MultiplyWithRoot` | — (left at default) |
| `Owner` | Actor Object Reference | `""` | — (unconnected) |
| `ItemRow` | Data Table Row Handle Structure | `""` | `K2Node_MakeStruct_0` [out 0] |
| `Instigator` | Pawn Object Reference | `""` | — (unconnected) |

`CollisionHandlingOverride` is `Undefined`, i.e. its default — Do Not Spawn If Colliding was
not set, as instructed. Outputs: `then` [0] -> `K2Node_CallArrayFunction_5` [in 0];
`ReturnValue` [1] (BP Item Pickup Object Reference) -> nothing, which was not asked for.

**26. `K2Node_CallArrayFunction_5` — Set Array Elem**

| pin | type | value | source |
|---|---|---|---|
| `execute` | Exec | — | `K2Node_SpawnActorFromClass_0` [out 0] |
| `TargetArray` | Array of Names | `""` | `K2Node_VariableGet_1` [out 0] |
| `Index` | Integer | `0` | `K2Node_PromotableOperator_8` [out 0] |
| `Item` | Name (by ref) | `""` | — (left at default empty Name) |
| `bSizeToFit` | Boolean | `false` | — |

`TargetArray` was `Array of Wildcards` at creation and resolved to `Array of Names` when
`InventorySlots` was connected; `Item` resolved with it from `Wildcard (by ref)` to
`Name (by ref)`. Both were read back and confirmed.

This matches the E chain's `K2Node_CallArrayFunction_1` pin for pin: same `Item` type
`Name (by ref)` with empty value, same `bSizeToFit false`, same `Index` fed by the chain's
single subtract node, same `TargetArray` fed by its `GetInventorySlots`.

Output `then` [0] -> `K2Node_CallFunction_13` [in 0].

**27. `K2Node_CallFunction_13` — Refresh Held Item**
- `execute` (Exec) <- `K2Node_CallArrayFunction_5` [out 0]
- `self` (Self Object Reference) = `""` — no connection, i.e. called on self

Same shape as the E chain's `K2Node_CallFunction_28`, which also has an unconnected `self`.

---

## 5. The three reuse nodes — old consumers kept, exactly one new one each

Read before the work and again after. No new getter and no second subtract node was created.

**`K2Node_GetArrayItem_1` output 0 (`Output`, Name)**

| | consumers |
|---|---|
| before | `K2Node_PromotableOperator_11[in 0]` |
| after | `K2Node_PromotableOperator_11[in 0]`, **`K2Node_MakeStruct_0[in 1]`** |

1 -> 2. Old consumer kept, exactly one gained.

**`K2Node_VariableGet_1` output 0 (`InventorySlots`, Array of Names)**

| | consumers |
|---|---|
| before | `K2Node_CallArrayFunction_4[in 0]`, `K2Node_GetArrayItem_1[in 0]` |
| after | `K2Node_CallArrayFunction_4[in 0]`, `K2Node_GetArrayItem_1[in 0]`, **`K2Node_CallArrayFunction_5[in 1]`** |

2 -> 3. Both old consumers kept, exactly one gained.

**`K2Node_PromotableOperator_8` output 0 (`ReturnValue`, Integer — the single `SelectedSlot - 1`)**

| | consumers |
|---|---|
| before | `K2Node_PromotableOperator_9[in 0]`, `K2Node_PromotableOperator_10[in 0]`, `K2Node_GetArrayItem_1[in 1]` |
| after | `K2Node_PromotableOperator_9[in 0]`, `K2Node_PromotableOperator_10[in 0]`, `K2Node_GetArrayItem_1[in 1]`, **`K2Node_CallArrayFunction_5[in 2]`** |

3 -> 4. All three old consumers kept, exactly one gained. Its own inputs are unchanged
(`A` <- `K2Node_VariableGet_0`, `B` = `"1"`), so it is still the one off-by-one conversion
point for the whole island.

---

## 6. Node 27's `then` ends the chain

Read back after all work:

```
K2Node_CallFunction_13: outputs [{"i": 0, "n": "then", "t": "Exec", "to": []}]
```

`to` is empty. **`K2Node_CallFunction_13 . then` is the end of the Q chain.** There is nothing
after Refresh Held Item, which is correct — the E chain terminates the same way, its
`K2Node_CallFunction_28 . then` also reading `to: []`.

### The completed exec path

```
IA_DropItem . Started
  -> Branch (slot index in range)          K2Node_IfThenElse_4
  -> Branch (slot not empty)               K2Node_IfThenElse_5
  -> LineTraceByChannel (ground, 300 down) K2Node_CallFunction_7
  -> Branch (did it hit)                   K2Node_IfThenElse_6
       else -> PrintString CANNOT DROP HERE   K2Node_CallFunction_8   (ends)
       then -> SpawnActor BP_ItemPickup       K2Node_SpawnActorFromClass_0
            -> SetArrayElem (clear slot)      K2Node_CallArrayFunction_5
            -> RefreshHeldItem                K2Node_CallFunction_13  (ends)
```

The spawn runs before the slot is cleared, so a failed spawn cannot empty the slot — the
ordering requirement holds, confirmed by the read-back exec links above.

---

## 7. EventGraph node count

From the length of a `find_nodes` result (graph = EventGraph, `title` = `""`):

- **Before:** 91
- **After:** 98

98 - 91 = 7, which is exactly the 7 nodes in the table in section 3 (the 6 created in one batch
plus the STEP 0 SpawnActor node). Nothing else was added and nothing was removed.

---

## 8. Compile result

`BlueprintTools.compile_blueprint`, `warnings_as_errors` = `false`. Returned:

```
{"returnValue":null}
```

The tool raises on error; it did not raise. The log around the compile:

```
[2026.08.30-01.39.06:650][821]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint'
[2026.08.30-01.39.06:650][821]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.08.30-01.39.06:757][821]LogUObjectHash: Compacting FUObjectHashTables data took   1.60ms
```

Nothing between the compile line and the next tool call. **No compile errors, no compile
warnings.**

A `LogBlueprint` query filtered on `Warning|Error` still returns the same `00.36.49` block as
its newest entries — this compile added nothing to it.

**Not verified:** as in the previous commands, no tool reports a Blueprint's compiled status
flag directly. "Compiled clean" rests on the tool not raising plus an empty log window.

Saved with `AssetTools.save_assets` -> `true`; `AssetTools.is_dirty` afterwards -> `false`.

---

## 9. Errors and warnings — exact English text

### 9.1 From this work

**None.** Every `create_node`, `connect_pins` and `set_pin_value` call in this command
succeeded. No tool returned an error, no tool raised, and no silent no-op was found — the two
pins set by value (`K2Node_PromotableOperator_15 . B` and `K2Node_MakeStruct_0 . DataTable`)
were both read back and both held their values.

There is no error text to quote for this command.

### 9.2 Present in the log but NOT from this work

The `LogBlueprint` warning block from `00.36.49` remains the newest set of Blueprint warnings,
now roughly an hour old. Every node it names is pre-existing; none of the seven new node names
appears in it. Already recorded in the reports for commands 24 and 25. First and last lines:

```
[2026.08.30-00.36.49:926][550]LogBlueprint: Warning: No execute pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_Event_5
```

```
[2026.08.30-00.36.49:926][550]LogBlueprint: Warning: No then pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_CallFunction_27
```

The log also shows the user's hand-edit to BP_ItemPickup, which this command did not perform
and did not touch — recorded here only because it explains the changed situation:

```
[2026.08.30-01.35.52:907][764]LogBlueprint: Compiling Blueprint '/Game/Inventory/BP_ItemPickup.BP_ItemPickup'
```

---

## 10. Nodes created that were not on this list

**None.** All 7 nodes created appear on the command's list. No helper, literal or adapter node
was needed this time.

This is unlike command 25, which had to add a `MakeLiteralFloat` because a float pin default
could not be written; see `2026-08-30-25-drop-item-trace.md` section 4. Nothing comparable
arose here.

---

## 11. git status after the work

```
 M Content/Input/IMC_Inventory.uasset
 M Content/Inventory/BP_ItemPickup.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
?? Content/Input/Actions/IA_DropItem.uasset
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/2/9H/
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/2/LI/
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/8/WQ/
?? "Docs/2026-08-29-중간점검.md"
?? Docs/Terminal-Log/2026-08-30-23-drop-item-prep.md
?? Docs/Terminal-Log/2026-08-30-24-drop-item-gate.md
?? Docs/Terminal-Log/2026-08-30-25-drop-item-trace.md
?? Docs/Terminal-Log/2026-08-30-26-drop-item-spawn.md
```

`BP_ThirdPersonCharacter.uasset` is the file this command changed.
**`BP_ItemPickup.uasset` is newly modified since the last command's git status** — that is the
Expose on Spawn hand-edit, not this command's work. This command did not open, modify, compile
or save BP_ItemPickup.

---

## 12. What is not verified

The drop feature is built and compiles, but **nothing here was tested in PIE.** No part of this
session ran the game. Specifically unconfirmed:

- that pressing Q actually drops the selected item
- that the dropped item shows the right mesh — the whole point of the Expose on Spawn work is
  that ConstructionScript runs with `ItemRow` already set, and only PIE proves it
- that the +50 z lift is the right amount, i.e. that the item rests on the floor rather than
  hovering or sinking. The 50 came from the stated bounds of z -50 to +50, not from measurement
- that the slot clears and the HUD refreshes
- that the CANNOT DROP HERE path fires when aiming at a spot with no ground within 300 units

The pass/fail criteria for those belong in a PIE check, which has not been run.
