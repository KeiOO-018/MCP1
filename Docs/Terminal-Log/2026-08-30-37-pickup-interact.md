# 2026-08-30 — BP_ItemPickup: the Interact event

The interface event plus six nodes in `BP_ItemPickup:EventGraph`. Compiled clean and saved.

This is the second run of this command. The first attempt stopped at P1 because BPI_Interact was
not in BP_ItemPickup's Implemented Interfaces; that has since been added by hand, so P1 now
passes and the build went through. This report replaces the stop report at the same path.

Purely additive. Nothing calls `Interact` on a pickup yet, so the existing F chain in
BP_ThirdPersonCharacter still does the picking up and still behaves exactly as before.

`AssetTools.is_dirty` was not called. `write_graph_dsl` was not used.

---

## 1. Pre-flight — all four checks passed

### P1 — Interact is now present

`BlueprintTools.list_events` on `/Game/Inventory/BP_ItemPickup.BP_ItemPickup` returned **23**
entries. Full list of names, verbatim:

```
["ReceiveTick", "ReceiveRadialDamage", "ReceivePointDamage", "ReceiveHit", "ReceiveEndPlay",
 "ReceiveDestroyed", "ReceiveBeginPlay", "ReceiveAsyncPhysicsTick", "ReceiveAnyDamage",
 "ReceiveActorOnReleased", "ReceiveActorOnInputTouchLeave", "ReceiveActorOnInputTouchEnter",
 "ReceiveActorOnInputTouchEnd", "ReceiveActorOnInputTouchBegin", "ReceiveActorOnClicked",
 "ReceiveActorEndOverlap", "ReceiveActorEndCursorOver", "ReceiveActorBeginOverlap",
 "ReceiveActorBeginCursorOver", "K2_OnReset", "K2_OnEndViewTarget", "K2_OnBecomeViewTarget",
 "Interact"]
```

The `Interact` entry, in full:

```
{"name": "Interact", "description": "Interact", "bIsImplemented": false}
```

**`bIsImplemented` BEFORE: `false`** — the interface is on the class, but no event node existed
in the graph yet.

**`bIsImplemented` AFTER (re-read at the end of the command): `true`.**

The previous run read the same list at 22 entries with no `Interact` at all. That is the change
the hand edit made, and it matches exactly what happened to BP_Door between the two runs of
command 36.

### P2 — 3 nodes before

| # | refPath | type_id | position | connections |
|---|---|---|---|---|
| 1 | `...:EventGraph.K2Node_Event_0` | `AddEvent\|EventBeginPlay` | (0, 0) | all pins unconnected |
| 2 | `...:EventGraph.K2Node_Event_1` | `AddEvent\|Collision\|EventActorBeginOverlap` | (0, 208) | all pins unconnected |
| 3 | `...:EventGraph.K2Node_Event_2` | `AddEvent\|EventTick` | (0, 416) | all pins unconnected |

(`...` = `/Game/Inventory/BP_ItemPickup.BP_ItemPickup`)

### P3 — ItemRow

`list_variables`:

```
["ItemRow"]
```

Exactly one variable.

**Type:** `DataTableRowHandle` — the CDO property schema reports
`{"title": "DataTableRowHandle", "type": "object", "properties": {"dataTable": ..., "rowName": ...}}`.

**CDO default value:**

```
{"ItemRow":{"dataTable":{"refPath":"/Game/Inventory/DT_Items.DT_Items"},"rowName":"None"}}
```

- **DataTable:** `/Game/Inventory/DT_Items.DT_Items`
- **RowName:** `None`

A `rowName` of `None` is the expected class default; each placed or spawned pickup sets its own
row. The spawn path from command 27 feeds a `MakeDataTableRowHandle` into the SpawnActor's
`ItemRow` pin, so spawned pickups override this rather than inheriting it.

### P4 — all four node types offered

| required type_id | offered |
|---|---|
| `Class\|BPThirdPersonCharacter\|TryAddItem` | yes |
| `Utilities\|Casting\|CastToBP_ThirdPersonCharacter` | yes |
| `Utilities\|Struct\|BreakDataTableRowHandle` | yes |
| `Actor\|DestroyActor` | yes |

None missing.

---

## 2. The Interact event node as created

`BlueprintTools.add_event`, `event_name` `"Interact"`, `position` (-600, 600). Because `Interact`
matches an inherited overridable event — the one the interface contributes — it created an
implementation node.

```
refPath  : /Game/Inventory/BP_ItemPickup.BP_ItemPickup:EventGraph.K2Node_Event_3
type_id  : AddEvent|EventInteract
position : (-608, 592)

input pins : (none)
output pins:
  [0] "OutputDelegate"  Delegate
  [1] "then"            Exec
  [2] "Interactor"      Actor Object Reference
```

**The `Interactor` pin is present, at output index 2, typed `Actor Object Reference`.** The stop
condition in step 1 did not trigger.

The position reads **(-608, 592)** rather than the (-600, 600) that was passed — the editor
snapped the node to its grid, the same 8-unit snap seen on BP_Door's Interact event in command
36.

---

## 3. Node inventory of BP_ItemPickup:EventGraph after the work

**10 nodes.** The 3 from P2, unchanged, plus these 7:

| # | refPath | type_id | position |
|---|---|---|---|
| 4 | `...:EventGraph.K2Node_Event_3` | `AddEvent\|EventInteract` | (-608, 592) |
| 5 | `...:EventGraph.K2Node_DynamicCast_0` | `Utilities\|Casting\|CastToBP_ThirdPersonCharacter` | (-300, 600) |
| 6 | `...:EventGraph.K2Node_VariableGet_0` | `\|GetItemRow` | (-300, 900) |
| 7 | `...:EventGraph.K2Node_BreakStruct_0` | `Utilities\|Struct\|BreakDataTableRowHandle` | (-60, 900) |
| 8 | `...:EventGraph.K2Node_CallFunction_0` | `\|TryAddItem` | (200, 600) |
| 9 | `...:EventGraph.K2Node_IfThenElse_0` | `Utilities\|FlowControl\|Branch` | (560, 600) |
| 10 | `...:EventGraph.K2Node_CallFunction_1` | `Actor\|DestroyActor` | (840, 600) |

Node 4 is step 1's event; nodes 5–10 are step 2's a–f. All sit in the y 592–900 band with x from
-608 to 840, inside the requested -600…1200 range.

### Full pin connection list of every node added

```
K2Node_Event_3   AddEvent|EventInteract
  out [0] "OutputDelegate" (Delegate) -> (nothing)
  out [1] "then"           (Exec)     -> K2Node_DynamicCast_0 [in 0]
  out [2] "Interactor"     (Actor Object Reference) -> K2Node_DynamicCast_0 [in 1]

K2Node_DynamicCast_0   Utilities|Casting|CastToBP_ThirdPersonCharacter        (a)
  in  [0] "execute" (Exec)             <- K2Node_Event_3 [out 1]
  in  [1] "Object"  (Object Reference) <- K2Node_Event_3 [out 2]
  out [0] "then"       (Exec) -> K2Node_CallFunction_0 [in 0]
  out [1] "CastFailed" (Exec) -> (nothing)
  out [2] "AsBP Third Person Character" (BP Third Person Character Object Reference)
        -> K2Node_CallFunction_0 [in 1]

K2Node_VariableGet_0   |GetItemRow                                            (b)
  out [0] "ItemRow" (Data Table Row Handle Structure) -> K2Node_BreakStruct_0 [in 0]

K2Node_BreakStruct_0   Utilities|Struct|BreakDataTableRowHandle               (c)
  in  [0] "DataTableRowHandle" (DTRH by ref) <- K2Node_VariableGet_0 [out 0]
  out [0] "DataTable" (Data Table Object Reference) -> (nothing)
  out [1] "RowName"   (Name) -> K2Node_CallFunction_0 [in 2]

K2Node_CallFunction_0   |TryAddItem                                           (d)
  in  [0] "execute" (Exec)                     <- K2Node_DynamicCast_0 [out 0]
  in  [1] "self"    (BP Third Person Character Object Reference) <- K2Node_DynamicCast_0 [out 2]
  in  [2] "RowName" (Name) = "None"            <- K2Node_BreakStruct_0 [out 1]
  out [0] "then"    (Exec)    -> K2Node_IfThenElse_0 [in 0]
  out [1] "Success" (Boolean) -> K2Node_IfThenElse_0 [in 1]

K2Node_IfThenElse_0   Utilities|FlowControl|Branch                            (e)
  in  [0] "execute"   (Exec)             <- K2Node_CallFunction_0 [out 0]
  in  [1] "Condition" (Boolean) = "true" <- K2Node_CallFunction_0 [out 1]
  out [0] "then" (Exec) -> K2Node_CallFunction_1 [in 0]
  out [1] "else" (Exec) -> (nothing)

K2Node_CallFunction_1   Actor|DestroyActor                                    (f)
  in  [0] "execute" (Exec)                   <- K2Node_IfThenElse_0 [out 0]
  in  [1] "self"    (Actor Object Reference) = ""  (unconnected)
  out [0] "then" (Exec) -> (nothing)
```

Every connection was made by resolving the pin **name** to its index from a `get_node_infos`
read of each node taken before wiring. The cast's data output is named
`AsBP Third Person Character` (no space after "As").

### Resulting logic

```
Interact(Interactor)
  -> Cast Interactor to BP_ThirdPersonCharacter
       CastFailed -> (nothing, deliberately)
       then -> TryAddItem(RowName = ItemRow.RowName) on the caster
                 -> Branch (Success?)
                      true  -> DestroyActor (self)
                      false -> (nothing; TryAddItem already showed INVENTORY FULL)
```

---

## 4. The three specific confirmations

### DestroyActor's target pin is UNCONNECTED

`K2Node_CallFunction_1`, input pin [1]:

```
{"i": 1, "n": "self", "t": "Actor Object Reference", "v": "", "from": []}
```

Empty `from` list and empty value. The pin is named `self` on this node, and leaving it
unconnected means the call targets **this actor** — the pickup destroys itself.

This is the one deliberate difference from the old F chain, where `DestroyActor`'s target was
wired to the cast result because the Character was the caller. Here the pickup is the caller, so
the target must stay open. No `set_pin_value` was issued on it either.

### The cast's CastFailed pin is unconnected

`K2Node_DynamicCast_0`, output pin [1]:

```
{"i": 1, "n": "CastFailed", "t": "Exec", "to": []}
```

Empty `to` list.

### Branch's "else" pin is unconnected

`K2Node_IfThenElse_0`, output pin [1]:

```
{"i": 1, "n": "else", "t": "Exec", "to": []}
```

Empty `to` list. Nothing happens on a failed add, because `TryAddItem` shows INVENTORY FULL from
inside itself.

---

## 5. EventGraph node count

- **Before:** 3
- **After:** 10

3 + 7 = 10, matching the required figure. The seven are the Interact event from step 1 plus the
six nodes a–f from step 2.

**No node was created beyond the ones named in the command.** Nothing extra to list — no helper
node, no conversion node, no duplicate getter.

---

## 6. The three pre-existing event stubs were not modified

Read in pre-flight and again in the full read-back after all work. Identical both times:

```
K2Node_Event_0  AddEvent|EventBeginPlay                    (0, 0)
  OutputDelegate -> []   then -> []
K2Node_Event_1  AddEvent|Collision|EventActorBeginOverlap  (0, 208)
  OutputDelegate -> []   then -> []   OtherActor -> []
K2Node_Event_2  AddEvent|EventTick                         (0, 416)
  OutputDelegate -> []   then -> []   DeltaSeconds -> []
```

Same type_ids, same positions, every pin still unconnected. No `connect_pins`, `break_pins`,
`set_pin_value` or `delete_node` call named any of them.

---

## 7. No call targeted BP_ThirdPersonCharacter

Every MCP call in this command named one of:

- `/Game/Inventory/BP_ItemPickup.BP_ItemPickup` and its `EventGraph` — reads and writes
- nothing else

**`BP_ThirdPersonCharacter` was never named in any call**, for read or write. Its EventGraph and
its F pickup chain are untouched and behave exactly as they did before this command.

The one place the Character appears at all is inside the type_ids of two nodes created here —
`Utilities|Casting|CastToBP_ThirdPersonCharacter` and `Class|BPThirdPersonCharacter|TryAddItem`.
Those are references to its class from within BP_ItemPickup's graph; they read the Character's
compiled class but modify nothing in that Blueprint.

---

## 8. Compile result

`BlueprintTools.compile_blueprint` on BP_ItemPickup, `warnings_as_errors` = `false`, returned:

```
{"returnValue":null}
```

The tool raises on error; it did not raise. Two compiles of this Blueprint appear in the log —
one when the event was added, and the explicit one after wiring:

```
[2026.08.30-08.17.56:474][255]LogBlueprint: Compiling Blueprint '/Game/Inventory/BP_ItemPickup.BP_ItemPickup'
[2026.08.30-08.20.04:775][265]LogBlueprint: Compiling Blueprint '/Game/Inventory/BP_ItemPickup.BP_ItemPickup'
```

No error and no warning followed either. **Compiled clean.**

`AssetTools.save_assets` -> `true`. Content validation ran on save:

```
[2026.08.30-08.20.15:803][298]AssetCheck: /Game/Inventory/BP_ItemPickup Validating asset
```

Nine validators, no failure reported.

**Not verified:** no tool reports a Blueprint's compiled status flag directly. "Compiled clean"
rests on the call not raising plus an empty log window.

---

## 9. Errors and warnings — exact English text

### 9.1 From this work

No tool call raised. One set of warnings **was** produced by a call this command made — the
`ObjectTools.list_properties` read in pre-flight P3, which generates a JSON schema for the CDO
and cannot represent delegate properties:

```
[2026.08.30-08.18.53:546][958]LogJson: Warning: Property "OnBeginCursorOver" type FActorBeginCursorOverSignature unhandled during Json schema generation.
[2026.08.30-08.18.53:546][958]LogJson: Warning: Property "OnActorEndOverlap" type FActorEndOverlapSignature unhandled during Json schema generation.
[2026.08.30-08.18.53:546][958]LogJson: Warning: Property "OnActorBeginOverlap" type FActorBeginOverlapSignature unhandled during Json schema generation.
[2026.08.30-08.18.53:546][958]LogJson: Warning: Property "OnTakeRadialDamage" type FTakeRadialDamageSignature unhandled during Json schema generation.
[2026.08.30-08.18.53:546][958]LogJson: Warning: Property "OnTakePointDamage" type FTakePointDamageSignature unhandled during Json schema generation.
[2026.08.30-08.18.53:546][958]LogJson: Warning: Property "OnTakeAnyDamage" type FTakeAnyDamageSignature unhandled during Json schema generation.
```

These are read-side warnings from the schema generator, not Blueprint compile warnings, and
nothing was modified by that call. The one thing the check needed — `itemRow`'s schema title,
`DataTableRowHandle` — was returned correctly.

The same class of warning appeared in command 34 from the same tool on BP_ThirdPersonCharacter's
CDO; there the unhandled properties were the Character's movement delegates, here they are the
Actor damage and overlap delegates.

### 9.2 Present in the log but NOT from this work

Nothing new. The two BP_Door compiles at `08.00.11` and `08.03.00` are from command 36 — the
first of those was the hand session's, as recorded there.

---

## 10. git status after the work

```
 M Content/Inventory/BP_ItemPickup.uasset
?? Docs/Terminal-Log/2026-08-30-37-pickup-interact.md
```

`BP_ItemPickup.uasset` is the file this command changed. The tree was clean before this command
started, so this is the only asset change since the last commit.

---

## 11. What is not verified

- **Nothing was run in PIE, and nothing calls `Interact` on a pickup.** This event has never
  fired. The next command moves the F chain over to send the interface message; until then the
  old chain in BP_ThirdPersonCharacter is what actually picks items up, and this new block is
  dead code that compiles.
- **That `TryAddItem` returns true and the pickup destroys itself.** The function was built in
  command 34 and has still never executed.
- **The `CastFailed` path silently does nothing.** Correct for a non-Character interactor, but it
  also means a Character that somehow failed the cast produces no diagnostic — the same tradeoff
  noted for BP_Door in command 36.
- **Both the old F chain and this new block will exist simultaneously until the next command.**
  If something did start calling `Interact` on pickups before that chain is removed, an item
  could be added twice. Nothing calls it yet, so this is not live — but it is the thing to watch
  when the next command lands.
- **`BP_ItemPickup` carries an `EventTick` stub** (`K2Node_Event_2`), empty and driving nothing.
  Left exactly as found.
