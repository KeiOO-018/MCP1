# 2026-08-30 — Q (drop item) gate, front half

Built in `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`, `EventGraph`, live through
`unreal-mcp`. All 12 nodes created, all 16 links made, Blueprint compiled and saved.

Everything in the "read back" sections below comes from `get_node_infos` run AFTER the work
was finished, not from what was requested.

---

## 1. Nodes created — name, type_id, position

The `type_id` column is the value `get_node_infos` reports after the fact. For the four
promotable operators this is NOT the string that was passed to `create_node` — see section 5.

| # | role | node name | type_id (read back) | x | y |
|---|---|---|---|---|---|
| 1 | IA_DropItem event | `K2Node_EnhancedInputAction_5` | `Input\|EnhancedActionEvents\|EnhancedInputActionIA_DropItem` | -2800 | 3400 |
| 2 | Get SelectedSlot | `K2Node_VariableGet_0` | `\|GetSelectedSlot` | -2800 | 3650 |
| 3 | int - int | `K2Node_PromotableOperator_8` | `Math\|Integer\|int-int` | -2560 | 3650 |
| 4 | Get InventorySlots | `K2Node_VariableGet_1` | `\|GetInventorySlots` | -2800 | 3820 |
| 5 | Length | `K2Node_CallArrayFunction_4` | `Utilities\|Array\|Length` | -2560 | 3820 |
| 6 | integer >= integer | `K2Node_PromotableOperator_9` | `Math\|Integer\|integer>=integer` | -2300 | 3580 |
| 7 | integer < integer | `K2Node_PromotableOperator_10` | `Math\|Integer\|integer<integer` | -2300 | 3730 |
| 8 | AND Boolean | `K2Node_CommutativeAssociativeBinaryOperator_1` | `Math\|Boolean\|ANDBoolean` | -2060 | 3650 |
| 9 | Branch (gate 1) | `K2Node_IfThenElse_4` | `Utilities\|FlowControl\|Branch` | -1820 | 3400 |
| 10 | Get (a copy) | `K2Node_GetArrayItem_1` | `Utilities\|Array\|Get(acopy)` | -2300 | 3920 |
| 11 | NotEqual (Name) | `K2Node_PromotableOperator_11` | `Utilities\|Name\|NotEqual(Name)` | -2060 | 3920 |
| 12 | Branch (gate 2) | `K2Node_IfThenElse_5` | `Utilities\|FlowControl\|Branch` | -1560 | 3400 |

Positions are exactly the E-chain layout shifted +1200 in y (E starts at y=2200, Q at y=3400).
x spans -2800 to -1560, inside the requested -2800..-1500 band. No node overlaps the E chain.

The event node's `InputAction` output pin reads back
`/Game/Input/Actions/IA_DropItem.IA_DropItem`, so it is bound to the asset created in the
previous command.

---

## 2. Input pin connections of all 12 nodes — read back after the work

Format: `pin name (type) = <value>` and, where connected, `<- source node [output pin index]`.

**1. `K2Node_EnhancedInputAction_5` — EnhancedInputAction IA_DropItem**
No input pins (it is an event node).
Output `Started` [1] -> `K2Node_IfThenElse_4` input 0 (`execute`).
Outputs `Triggered` [0], `Ongoing` [2], `Canceled` [3], `Completed` [4], `ActionValue` [5],
`ElapsedSeconds` [6], `TriggeredSeconds` [7], `InputAction` [8] are all unconnected.
**Started was used, not Triggered** — confirmed by read-back: `Triggered.to = []`.

**2. `K2Node_VariableGet_0` — Get SelectedSlot**
No input pins.
Output `SelectedSlot` (Integer) [0] -> `K2Node_PromotableOperator_8` input 0 (`A`).

**3. `K2Node_PromotableOperator_8` — int - int**
- `A` (Integer) = `""` <- `K2Node_VariableGet_0` [out 0]
- `B` (Integer) = `"1"` — no connection

Output `ReturnValue` (Integer) [0] fans out to three consumers:
`K2Node_PromotableOperator_9` [in 0], `K2Node_PromotableOperator_10` [in 0],
`K2Node_GetArrayItem_1` [in 1].
**This is the only int-int node in the island** and it is the single off-by-one conversion
point — the >=, the <, and the Get(acopy) index all read this one output.

**4. `K2Node_VariableGet_1` — Get InventorySlots**
No input pins.
Output `InventorySlots` (Array of Names) [0] -> `K2Node_CallArrayFunction_4` [in 0] and
`K2Node_GetArrayItem_1` [in 0].
**One getter serves both Length and Get(acopy)**, as required.

**5. `K2Node_CallArrayFunction_4` — Length**
- `TargetArray` (Array of Names) = `""` <- `K2Node_VariableGet_1` [out 0]

Output `ReturnValue` (Integer) [0] -> `K2Node_PromotableOperator_10` [in 1].

**6. `K2Node_PromotableOperator_9` — integer >= integer**
- `A` (Integer) = `""` <- `K2Node_PromotableOperator_8` [out 0]
- `B` (Integer) = `"0"` — no connection

Output `ReturnValue` (Boolean) [0] -> `K2Node_CommutativeAssociativeBinaryOperator_1` [in 0].

**7. `K2Node_PromotableOperator_10` — integer < integer**
- `A` (Integer) = `""` <- `K2Node_PromotableOperator_8` [out 0]
- `B` (Integer) = `""` <- `K2Node_CallArrayFunction_4` [out 0]

Output `ReturnValue` (Boolean) [0] -> `K2Node_CommutativeAssociativeBinaryOperator_1` [in 1].

**8. `K2Node_CommutativeAssociativeBinaryOperator_1` — AND Boolean**
- `A` (Boolean) = `"false"` <- `K2Node_PromotableOperator_9` [out 0]
- `B` (Boolean) = `"false"` <- `K2Node_PromotableOperator_10` [out 0]

Output `ReturnValue` (Boolean) [0] -> `K2Node_IfThenElse_4` [in 1].

**9. `K2Node_IfThenElse_4` — Branch (gate 1)**
- `execute` (Exec) <- `K2Node_EnhancedInputAction_5` [out 1] (`Started`)
- `Condition` (Boolean) = `"true"` <- `K2Node_CommutativeAssociativeBinaryOperator_1` [out 0]

Output `then` [0] -> `K2Node_IfThenElse_5` [in 0]. Output `else` [1] -> **nothing**.

**10. `K2Node_GetArrayItem_1` — Get (a copy)**
- `Array` (Array of Names) = `""` <- `K2Node_VariableGet_1` [out 0]
- `Dimension 1` (Integer) = `"0"` <- `K2Node_PromotableOperator_8` [out 0]

Output `Output` (Name) [0] -> `K2Node_PromotableOperator_11` [in 0].

**11. `K2Node_PromotableOperator_11` — NotEqual (Name)**
- `A` (Name) = `""` <- `K2Node_GetArrayItem_1` [out 0]
- `B` (Name) = `""` — **no connection, left at its default empty value** as instructed

Output `ReturnValue` (Boolean) [0] -> `K2Node_IfThenElse_5` [in 1].

**12. `K2Node_IfThenElse_5` — Branch (gate 2)**
- `execute` (Exec) <- `K2Node_IfThenElse_4` [out 0] (`then`)
- `Condition` (Boolean) = `"true"` <- `K2Node_PromotableOperator_11` [out 0]

Outputs: see next section.

---

## 3. Branch (12) `then` is open — read back

From the `get_node_infos` read of `K2Node_IfThenElse_5` taken after all work was done, its
output pins were reported as:

```
{"i": 0, "name": "then",  "type": "Exec", "to": []}
{"i": 1, "name": "else",  "type": "Exec", "to": []}
```

`to` is the list of pins each output is connected to. Both lists are empty.
**`K2Node_IfThenElse_5.then` has no connection**, and neither does its `else`.
The last exec pin of the chain is left open for the next command, as required.

`K2Node_IfThenElse_4.else` is likewise `[]` — no `else` pin anywhere in the island is
connected.

---

## 4. Node count in the EventGraph

Taken from the length of a `find_nodes` result (graph = EventGraph, `title` = `""`, which
matches every node), not counted by hand:

- Before any node was created: **70**
- After all work: **82**

82 - 70 = 12, which matches the 12 nodes created and confirms nothing else was added or
removed.

### The E chain was not touched

All 12 E-chain nodes were re-read after the work and compared against the read taken before
it. Positions, type_ids and input connections are identical:

```
K2Node_EnhancedInputAction_2  Input|EnhancedActionEvents|EnhancedInputActionIA_UseItem  (-2800,2200)  in: []
K2Node_VariableGet_13         |GetSelectedSlot                (-2800,2450)  in: []
K2Node_PromotableOperator_0   Math|Integer|int-int            (-2560,2450)  in: [K2Node_VariableGet_13->A]
K2Node_VariableGet_14         |GetInventorySlots              (-2800,2620)  in: []
K2Node_CallArrayFunction_0    Utilities|Array|Length          (-2560,2620)  in: [K2Node_VariableGet_14->TargetArray]
K2Node_PromotableOperator_1   Math|Integer|integer>=integer   (-2300,2380)  in: [K2Node_PromotableOperator_0->A]
K2Node_PromotableOperator_4   Math|Integer|integer<integer    (-2300,2530)  in: [K2Node_PromotableOperator_0->A, K2Node_CallArrayFunction_0->B]
K2Node_CommutativeAssociativeBinaryOperator_0  Math|Boolean|ANDBoolean  (-2060,2450)  in: [K2Node_PromotableOperator_1->A, K2Node_PromotableOperator_4->B]
K2Node_IfThenElse_0           Utilities|FlowControl|Branch    (-1820,2200)  in: [K2Node_EnhancedInputAction_2->execute, K2Node_CommutativeAssociativeBinaryOperator_0->Condition]
K2Node_GetArrayItem_0         Utilities|Array|Get(acopy)      (-2300,2720)  in: [K2Node_VariableGet_14->Array, K2Node_PromotableOperator_0->Dimension 1]
K2Node_PromotableOperator_6   Utilities|Name|NotEqual(Name)   (-2060,2720)  in: [K2Node_GetArrayItem_0->A]
K2Node_IfThenElse_3           Utilities|FlowControl|Branch    (-1560,2200)  in: [K2Node_IfThenElse_0->execute, K2Node_PromotableOperator_6->Condition]
```

No node is shared between the two islands: every input of the Q island is fed by a Q-island
node, and every Q-island output goes only to Q-island nodes.

**Not verified:** only the 12 E-gate nodes were diffed. The rest of the E chain past
`K2Node_IfThenElse_3` (GetDataTableRow, BreakStruct, SwitchEnum, and the F chain) was not
re-read node by node. The node count going from 70 to exactly 82 is the evidence that nothing
was deleted anywhere in the graph.

---

## 5. Deviations — type_ids that had to be looked up, not used as given

Four of the requested `type_id` strings do not exist in this graph's creatable-node registry.
`find_node_types` was used to find the real ones. In every case the node **reads back after
wiring with exactly the type_id that was requested**, because these are promotable (wildcard)
operators that resolve their type when a typed pin is connected.

| requested type_id | passed to `create_node` | reads back as |
|---|---|---|
| `Input\|EnhancedActionEvents\|EnhancedInputActionIA_DropItem` | `Input\|EnhancedActionEvents\|IA_DropItem` | `Input\|EnhancedActionEvents\|EnhancedInputActionIA_DropItem` |
| `\|GetSelectedSlot` | `Variables\|Default\|GetSelectedSlot` | `\|GetSelectedSlot` |
| `\|GetInventorySlots` | `Variables\|Default\|GetInventorySlots` | `\|GetInventorySlots` |
| `Math\|Integer\|int-int` | `Utilities\|Operators\|Subtract` | `Math\|Integer\|int-int` |
| `Math\|Integer\|integer>=integer` | `Utilities\|Operators\|GreaterEqual(>=)` | `Math\|Integer\|integer>=integer` |
| `Math\|Integer\|integer<integer` | `Utilities\|Operators\|Less(<)` | `Math\|Integer\|integer<integer` |
| `Utilities\|Name\|NotEqual(Name)` | `Utilities\|Operators\|NotEqual(!=)` | `Utilities\|Name\|NotEqual(Name)` |

`Math|Boolean|ANDBoolean`, `Utilities|Array|Length`, `Utilities|Array|Get(acopy)` and
`Utilities|FlowControl|Branch` existed in the registry under exactly the requested names and
were used verbatim.

Immediately after creation the four promotable nodes read back with placeholder types —
`Utilities|TimeManagement|FrameNumber-Int`, `Math|Timespan|Timespan>=Timespan`,
`Math|Timespan|Timespan<Timespan`, `GameplayTags|NotEqual(GameplayTagContainer)`, all with
Wildcard pins. They resolved to the correct integer / Name forms once the typed sources were
connected. The connections were deliberately ordered so the typed pin lands first
(`SelectedSlot` -> `sub.A` before `sub.B` is set, `Get(acopy).Output` -> `neq.A` before
anything else on that node).

### One value chosen that differs from the E chain

The `>=` node's `B` pin was explicitly set to `"0"`, as the instruction said
("B = 0"). On the E chain the same pin reads back as `""` (never explicitly set). Both mean
integer zero; the read-back strings differ. Nothing else was set that the E chain leaves at
default.

---

## 6. Compile result

`BlueprintTools.compile_blueprint` on
`/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter`,
`warnings_as_errors` = `false`. Returned:

```
{"returnValue":null}
```

The tool returns null and raises on error; it did not raise. The log for the compile is:

```
[2026.08.30-00.59.36:709][622]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint'
[2026.08.30-00.59.36:709][622]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.08.30-00.59.36:803][622]LogUObjectHash: Compacting FUObjectHashTables data took   1.64ms
```

Nothing else was logged between the compile call and the next tool call. **No compile errors
and no compile warnings.**

**Not verified:** no tool in this MCP server reports a Blueprint's compiled status flag
(Up To Date / Dirty / Error) directly. "Compiled clean" here rests on two things: the tool did
not raise, and the log holds no error or warning between the compile line and the next
timestamp.

Saved with `AssetTools.save_assets` -> `true`; `AssetTools.is_dirty` afterwards -> `false`.

---

## 7. Errors and warnings — exact English text

### 7.1 From the editor, caused by this work

Two `create_node` calls failed on a type_id that does not exist. Both were recoverable: the
script had already created the nodes before the failing one, and no partial node was left
behind (verified — `find_nodes` for "DropItem" returned exactly one node, and the final count
of 82 is exactly 70 + 12).

```
line 6: RuntimeError: Script error in editor_toolset.toolsets.blueprint.BlueprintTools.create_node:
The node could not be created / |GetSelectedSlot does not exist
Traceback (script frames only):
  File "<script>", line 27, in run
    out[key] = create(tid, x, y)
               ^^^^^^^^^^^^^^^^^
  File "<script>", line 6, in create
    return execute_tool(
           ^^^^^^^^^^^^^
```

```
line 6: RuntimeError: Script error in editor_toolset.toolsets.blueprint.BlueprintTools.create_node:
The node could not be created / Math|Integer|int-int does not exist
Traceback (script frames only):
  File "<script>", line 26, in run
    out[key] = create(tid, x, y)
               ^^^^^^^^^^^^^^^^^
  File "<script>", line 6, in create
    return execute_tool(
           ^^^^^^^^^^^^^
```

No warnings were produced by any `connect_pins` or `set_pin_value` call. All 16 succeeded.

### 7.2 Present in the log but NOT from this work

`LogBlueprint` holds a block of warnings timestamped `00.36.49`, twenty-three minutes before
this session's compile at `00.59.36`. They are from an earlier compile and every node they
name is a pre-existing one — none of the twelve new node names appears in them. Recording the
first and last of the block verbatim; the block is 39 lines of the same two shapes:

```
[2026.08.30-00.36.49:926][550]LogBlueprint: Warning: No execute pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_Event_5
```

```
[2026.08.30-00.36.49:926][550]LogBlueprint: Warning: No then pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_CallFunction_27
```

A search of the whole session log for `Error` returned only editor startup noise from
`00.07.21` (missing profiler DLLs, `LogTemp` self-test lines) and three
`LogModelContextProtocol: Error: Call to unknown method "server/discover"` entries from
before this work. None relate to the Blueprint.

---

## 8. Side effect worth flagging

**BP_ThirdPersonCharacter was already dirty in the editor before this work started.**
`AssetTools.is_dirty` returned `true` on it before the first node was created, while
`git status` showed the `.uasset` as unmodified — so the editor held unsaved changes from
before this session. Saving at the end of this command wrote those to disk along with the new
Q island. What that pre-existing change was is unknown; it was not inspected and cannot be
separated from this command's diff.

---

## 9. git status after the work

```
 M Content/Input/IMC_Inventory.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
?? Content/Input/Actions/IA_DropItem.uasset
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/2/9H/
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/2/LI/
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/8/WQ/
?? "Docs/2026-08-29-중간점검.md"
?? Docs/Terminal-Log/2026-08-30-23-drop-item-prep.md
```

`BP_ThirdPersonCharacter.uasset` is the file this command changed. `IMC_Inventory.uasset` and
`IA_DropItem.uasset` are from the previous command. The `__ExternalActors__` folders and the
`Docs/2026-08-29` file predate this session.

---

## 10. Handoff to the next command

The Q island is wired up to and including the second Branch. The next command builds the trace
and attaches it to:

```
K2Node_IfThenElse_5 . then     (output pin index 0, currently unconnected)
```

Useful names from this island for that work:

- `K2Node_PromotableOperator_8` output 0 — the `SelectedSlot - 1` index (Integer)
- `K2Node_GetArrayItem_1` output 0 — the row name at that index (Name)
- `K2Node_VariableGet_1` output 0 — `InventorySlots` (Array of Names)
