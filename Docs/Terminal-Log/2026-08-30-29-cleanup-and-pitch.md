# 2026-08-30 — remove dead HeldItemSlot, raise first-person pitch limits

Two unrelated edits to `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`, bundled only
because they touch the same Blueprint. Both done, compiled clean, saved.

- **EDIT 1** — member variable `HeldItemSlot` removed. 12 variables -> 11.
- **EDIT 2** — `FirstPersonPitchMin` -60 -> -80, `FirstPersonPitchMax` 60 -> 80.

`FoundSlotIndex` and its three nodes were left untouched and verified intact.

`AssetTools.is_dirty` was not called, as instructed.

---

## 1. EDIT 1 — the HeldItemSlot reference check, before removal

`find_nodes(title: "HeldItemSlot")` was re-run in all nine graphs named in the command. Graph
names were confirmed first with `list_graphs` on each Blueprint, so no graph was searched under
a guessed name.

| graph | result |
|---|---|
| `BP_ThirdPersonCharacter : EventGraph` | `[]` |
| `BP_ThirdPersonCharacter : RefreshHeldItem` | `[]` |
| `BP_ThirdPersonCharacter : ToggleCameraView` | `[]` |
| `BP_ThirdPersonCharacter : Move` | `[]` |
| `BP_ThirdPersonCharacter : Aim` | `[]` |
| `BP_ThirdPersonCharacter : UserConstructionScript` | `[]` |
| `BP_ThirdPersonHUD : EventGraph` | `[]` |
| `BP_ThirdPersonPlayerController : EventGraph` | `[]` |
| `BP_ThirdPersonGameMode : EventGraph` | `[]` |

**All nine returned an empty array.** Zero references, matching what the command stated. The
removal went ahead.

### The same sweep for FoundSlotIndex, run at the same time

Run as a control, to make certain the search was actually finding things and not silently
returning empty for a bad graph reference:

| graph | result |
|---|---|
| `BP_ThirdPersonCharacter : EventGraph` | `["K2Node_VariableSet_1", "K2Node_VariableGet_8", "K2Node_VariableGet_9"]` |
| all eight other graphs | `[]` |

`FoundSlotIndex` returns exactly the three nodes the command named, from the same query shape
that returned empty for `HeldItemSlot`. So the empty results above are real, not a broken
query.

### Graphs found by list_graphs

- `BP_ThirdPersonCharacter`: UserConstructionScript, Move, Aim, ToggleCameraView,
  RefreshHeldItem, EventGraph — all six searched
- `BP_ThirdPersonHUD`: UserConstructionScript, EventGraph
- `BP_ThirdPersonPlayerController`: UserConstructionScript, **Should Use Touch Controls**,
  EventGraph
- `BP_ThirdPersonGameMode`: UserConstructionScript, EventGraph

**Not verified:** the command listed nine graphs and nine were searched, but the four
Blueprints actually contain twelve graphs between them. Three were not on the list and were
not searched: `BP_ThirdPersonHUD : UserConstructionScript`,
`BP_ThirdPersonPlayerController : UserConstructionScript`,
`BP_ThirdPersonPlayerController : Should Use Touch Controls`, and
`BP_ThirdPersonGameMode : UserConstructionScript` (four, in fact). A construction script or
touch-controls graph in another Blueprint referencing this Character's `HeldItemSlot` is very
unlikely — it would need a cast to BP_ThirdPersonCharacter first — but it was not checked, and
the compile afterwards was clean, which is the practical evidence that nothing broke.

---

## 2. list_variables — before and after

Tool: `BlueprintTools.list_variables` on
`/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter`.

### BEFORE — 12 names

```
bIsFirstPerson
FirstPersonPitchMin
FirstPersonPitchMax
ThirdPersonPitchMin
ThirdPersonPitchMax
InventorySlots
SelectedSlot
HeldItemSlot
CurrentHP
MaxHP
InteractDistance
FoundSlotIndex
```

### AFTER — 11 names

```
bIsFirstPerson
FirstPersonPitchMin
FirstPersonPitchMax
ThirdPersonPitchMin
ThirdPersonPitchMax
InventorySlots
SelectedSlot
CurrentHP
MaxHP
InteractDistance
FoundSlotIndex
```

12 -> 11. **`HeldItemSlot` is gone. `FoundSlotIndex` is still present.** Every other name is
unchanged and in the same relative order — only the one entry was removed.

`find_nodes(title: "HeldItemSlot")` on the EventGraph after removal also returns `[]`, so no
orphaned node was left behind by the removal.

Removed with `BlueprintTools.remove_variable` (blueprint, name `HeldItemSlot`, no `graph`
argument, so it removed a member variable rather than a local). It returned
`{"returnValue":null}` — the read-backs above are what confirm it worked, not the return value.

---

## 3. FoundSlotIndex — the three live nodes, before and after

All three still exist, at the same positions, with identical connections. Read back after the
removal and after the compile.

**`K2Node_VariableSet_1` — `|SetFoundSlotIndex` at (-450, 220)**

| | before | after |
|---|---|---|
| `execute` <- | `K2Node_DynamicCast_1[out 0]` | `K2Node_DynamicCast_1[out 0]` |
| `FoundSlotIndex` <- | `K2Node_CallArrayFunction_2[out 0]`, value `"0"` | `K2Node_CallArrayFunction_2[out 0]`, value `"0"` |
| `then` -> | `K2Node_IfThenElse_2[in 0]` | `K2Node_IfThenElse_2[in 0]` |
| `Output_Get` -> | `[]` | `[]` |

**`K2Node_VariableGet_8` — `|GetFoundSlotIndex` at (-420, 900)**

| | before | after |
|---|---|---|
| `FoundSlotIndex` -> | `K2Node_PromotableOperator_5[in 0]` | `K2Node_PromotableOperator_5[in 0]` |

**`K2Node_VariableGet_9` — `|GetFoundSlotIndex` at (60, 430)**

| | before | after |
|---|---|---|
| `FoundSlotIndex` -> | `K2Node_CallArrayFunction_3[in 2]` | `K2Node_CallArrayFunction_3[in 2]` |

Identical in every field. The F pickup chain is intact. The variable's own default also still
reads `-1` on the CDO after the compile.

---

## 4. EDIT 2 — variable defaults after the change

Written with `ObjectTools.set_properties` on the Blueprint reference, which redirects to
`Default__BP_ThirdPersonCharacter_C` where a Blueprint's variable defaults live. Returned
`{"returnValue":true}`.

Read back from the CDO after the compile:

| variable | before | after | intended |
|---|---|---|---|
| `FirstPersonPitchMin` | `-60` | **`-80`** | changed |
| `FirstPersonPitchMax` | `60` | **`80`** | changed |
| `ThirdPersonPitchMin` | `-89.900000000000006` | `-89.900000000000006` | untouched |
| `ThirdPersonPitchMax` | `89.900000000000006` | `89.900000000000006` | untouched |
| `InteractDistance` | `800` | `800` | untouched |
| `CurrentHP` | `75` | `75` | untouched |
| `MaxHP` | `100` | `100` | untouched |
| `FoundSlotIndex` | `-1` | `-1` | untouched |

Only the first-person pair moved. The third-person pair keeps its full `-89.9 / 89.9` range.

The third-person values print as `89.900000000000006` in both reads — that is float-to-JSON
round-tripping of 89.9, not a change; the before and after strings are byte-identical.

`CurrentHP` reads `75`, not `100`. That is its pre-existing default and was left exactly as
found.

---

## 5. Placed instances in Lvl_ThirdPerson

`SceneTools.get_current_level` -> `/Game/ThirdPerson/Lvl_ThirdPerson` (the level asked about is
the one currently loaded, so the query ran against the right level).

`SceneTools.find_actors` with `actor_type` =
`/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter_C`:

```
{"returnValue":[]}
```

**Count: 0.** There is no placed BP_ThirdPersonCharacter instance in Lvl_ThirdPerson, so there
is no instance carrying an override that would shadow the new pitch defaults. The character is
spawned at runtime from the GameMode, which takes the class defaults, so the new
`-80 / 80` will apply. No instance was modified — none exists to modify.

---

## 6. EventGraph node count

From the length of a `find_nodes` result (graph = EventGraph, `title` = `""`):

- **Before:** 98
- **After:** 98

**Unchanged at 98**, as required. Expected, since no node referenced `HeldItemSlot` — removing
the variable removed only the entry in the Blueprint's variable list, not any graph node. EDIT 2
touched only CDO property values, which are not nodes either.

---

## 7. Compile result

`BlueprintTools.compile_blueprint`, `warnings_as_errors` = `false`. Returned:

```
{"returnValue":null}
```

The tool raises on error; it did not raise. The full log window around the compile:

```
[2026.08.30-02.24.41:776][371]LogModelContextProtocol: Running tool: 'call_tool'
[2026.08.30-02.24.41:776][371]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint'
[2026.08.30-02.24.41:776][371]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.08.30-02.24.41:879][371]LogUObjectHash: Compacting FUObjectHashTables data took   1.65ms
```

Nothing between the compile line and the next tool call. **No compile errors, no compile
warnings.** This matters more than usual here: removing a variable is the kind of edit that
produces "variable not found" errors if anything still referenced it, and none appeared.

Saved with `AssetTools.save_assets` -> `true`.

---

## 8. Errors and warnings — exact English text

### 8.1 From this work

**None.** `remove_variable`, `set_properties`, `compile_blueprint`, `save_assets`,
`find_actors`, `get_current_level`, and every `find_nodes` / `list_variables` /
`list_graphs` / `get_node_infos` call completed without raising. Nothing was written to the log
by any of them beyond the routine dispatch lines.

There is no error text to quote for this command.

One log entry from the middle of the command that is not an error, recorded so it is not
mistaken for one later — the editor's autosave timer fired between the two edits and wrote an
autosave copy under `Saved/`, which is gitignored:

```
[2026.08.30-02.24.24:845][320]OBJ SavePackage: Generating thumbnails for [1] asset(s) in package [/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter] ([2] browsable assets)...
[2026.08.30-02.24.24:950][320]LogSavePackage: Moving 'D:/20260827/MCP1/Saved/BP_ThirdPersonCharacter_Auto88D477BB34D54CFC985BDC8AB94F16827.tmp' to 'D:/20260827/MCP1/Saved/Autosaves/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter_Auto8.uasset'
```

That autosave captured the Blueprint mid-command — after the variable removal and the property
set, before the compile. It is not the saved asset; the real save happened at the end.

### 8.2 Present in the log but NOT from this work

The `LogBlueprint` warning block from `00.36.49` is still the newest set of Blueprint warnings,
now roughly two hours old. Every node it names is pre-existing. Already recorded in the reports
for commands 24, 25, 27 and 28. First and last lines, verbatim:

```
[2026.08.30-00.36.49:926][550]LogBlueprint: Warning: No execute pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_Event_5
```

```
[2026.08.30-00.36.49:926][550]LogBlueprint: Warning: No then pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_CallFunction_27
```

---

## 9. git status after the work

```
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

One file, the one this command changed. Both edits are in it.

---

## 10. What is not verified

- **Nothing was tested in PIE.** That the -80 / 80 first-person pitch range actually feels
  right, and that looking that far up or down in first person does not clip into the character
  mesh or reveal geometry gaps, is unconfirmed. The numbers were set; the view was not looked
  through.
- **The four unlisted graphs** noted in section 1 were not searched for `HeldItemSlot`. The
  clean compile is the evidence that nothing referenced it.
- **The drop feature from commands 23–28 still has not been run in PIE.** Q behaviour, the
  dropped item's mesh, the +50 z lift and the CANNOT DROP HERE path all remain untested.
