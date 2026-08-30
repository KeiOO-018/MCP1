# 2026-08-30 · Command 41 — TryConsumeSelected pure-node re-evaluation fix

Target: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`, graph `TryConsumeSelected`.

Fix a confirmed runtime bug: `ANDBoolean` is a **pure** node whose output fed both
`Branch.Condition` and `Return.Success`. Pure nodes re-evaluate at every read, so the Branch
read `true`, `SetArrayElem` blanked the selected slot, and the Return then re-read the same
pure chain — now `false`, because `Equal(Name)` no longer matched the blanked slot. The
function returned `false` after having consumed the item.

The fix latches the AND's value into a **local** bool with an impure Set node, and feeds both
the Branch and the Return from that latch. One new node, one new local variable, nothing
deleted.

`AssetTools.is_dirty` was **not** called, per the instruction.
`TryAddItem`, `EventGraph` and `BP_Door` were not touched.

---

## Pre-flight

### P1 — `find_nodes` on TryConsumeSelected, empty title

Returned **exactly 13 nodes**. Every refPath, with the position read from
`get_node_infos` (the `…BP_ThirdPersonCharacter:TryConsumeSelected.` prefix is trimmed in
the table; the full form is
`/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:TryConsumeSelected.<node>`):

| # | node | type_id | position |
|---|---|---|---|
| 1 | `K2Node_FunctionEntry_0` | `\|TryConsumeSelected` | (0, 0) |
| 2 | `K2Node_FunctionResult_0` | `\|ReturnNode` | (120, 0) |
| 3 | `K2Node_VariableGet_0` | `\|GetSelectedSlot` | (-700, 400) |
| 4 | `K2Node_PromotableOperator_0` | `Math\|Integer\|int-int` | (-500, 400) |
| 5 | `K2Node_VariableGet_1` | `\|GetInventorySlots` | (-700, 250) |
| 6 | `K2Node_GetArrayItem_0` | `Utilities\|Array\|Get(acopy)` | (-300, 300) |
| 7 | `K2Node_PromotableOperator_1` | `Utilities\|Name\|Equal(Name)` | (-60, 300) |
| 8 | `K2Node_PromotableOperator_2` | `Utilities\|Name\|NotEqual(Name)` | (-60, 480) |
| 9 | `K2Node_CommutativeAssociativeBinaryOperator_0` | `Math\|Boolean\|ANDBoolean` | (180, 380) |
| 10 | `K2Node_IfThenElse_0` | `Utilities\|FlowControl\|Branch` | (420, 0) |
| 11 | `K2Node_VariableGet_2` | `\|GetInventorySlots` | (560, 250) |
| 12 | `K2Node_CallArrayFunction_0` | `Utilities\|Array\|SetArrayElem` | (820, 0) |
| 13 | `K2Node_CallFunction_0` | `\|RefreshHeldItem` | (1080, 0) |

**PASS.** Exactly 13.

### P2 — `get_node_infos` on K2Node_CommutativeAssociativeBinaryOperator_0

`type_id` is `Math|Boolean|ANDBoolean`. Output pin [0] `"ReturnValue"`, `connected_pins`
verbatim:

```json
[{"direction":"EGPD_Input","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_IfThenElse_0"}},{"direction":"EGPD_Input","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_FunctionResult_0"}}]
```

Exactly two destinations:

| destination | index | pin name (read from that node) |
|---|---|---|
| `K2Node_IfThenElse_0` | in 1 | `Condition` |
| `K2Node_FunctionResult_0` | in 1 | `Success` |

**PASS.** This is the bug, visible in the data: one pure output, two independent reads.

### P3 — `get_node_infos` on K2Node_IfThenElse_0

| | expected | measured | |
|---|---|---|---|
| input [0] `execute` source | `K2Node_FunctionEntry_0` [out 0] `then` | `K2Node_FunctionEntry_0` [out 0], name confirmed `then` | **PASS** |
| output [0] `then` dest | `K2Node_CallArrayFunction_0` | `K2Node_CallArrayFunction_0` [in 0] | **PASS** |
| output [1] `else` dest | `K2Node_FunctionResult_0` [in 0] | `K2Node_FunctionResult_0` [in 0] | **PASS** |

**PASS.**

### P4 — `list_variables` on BP_ThirdPersonCharacter

```json
["bIsFirstPerson","FirstPersonPitchMin","FirstPersonPitchMax","ThirdPersonPitchMin","ThirdPersonPitchMax","InventorySlots","SelectedSlot","CurrentHP","MaxHP","InteractDistance","FoundSlotIndex"]
```

**Count: 11.** Does **not** contain `bMatched`. **PASS.**

### P5 — baselines for the two graphs that must not change

| graph | expected | measured | |
|---|---|---|---|
| `TryAddItem` | 12 | **12** | **PASS** |
| `EventGraph` | 87 | **87** | **PASS** |

All five pre-flight checks passed.

---

## Stage 1 — the local variable

`add_variable` with `blueprint` BP_ThirdPersonCharacter, `name` `bMatched`,
`type_name` `bool`, and `graph` set to the TryConsumeSelected graph (the `graph` argument is
what makes it local):

```json
{"returnValue":null}
```

`add_variable` declares no output schema, so `null` is what a completed call returns — not a
status value.

### It is LOCAL, not a member — read-back proof

`list_variables` on BP_ThirdPersonCharacter (no `graph` argument), verbatim:

```json
["bIsFirstPerson","FirstPersonPitchMin","FirstPersonPitchMax","ThirdPersonPitchMin","ThirdPersonPitchMax","InventorySlots","SelectedSlot","CurrentHP","MaxHP","InteractDistance","FoundSlotIndex"]
```

Still 11 entries, still no `bMatched` — identical to P4. The STOP condition did not trigger;
nothing had to be removed.

That read alone only proves `bMatched` is *not a member*. To prove it positively exists as a
local, `list_variables` was called again **with** the graph argument:

```json
{"returnValue":["bMatched"]}
```

Member scope: unchanged, 11, no `bMatched`. Graph scope: exactly `["bMatched"]`.
**The variable is local to TryConsumeSelected.**

---

## Stage 2 — the Set node, as an island

### Position

The requested point was (300, 560). Checking every P1 node against it, one is inside 250
units:

- `K2Node_CommutativeAssociativeBinaryOperator_0` (ANDBoolean) at **(180, 380)** —
  distance `sqrt(120² + 180²)` = **216.3**, which is < 250.

Next-nearest are NotEqual(Name) at (-60, 480) at 368.8 and Equal(Name) at (-60, 300) at
444.1; everything else is past 570.

**So the fallback position (300, 760) was used instead**, as the command directed. At (300,
760) the nearest node is ANDBoolean at 398.5 units — clear.

### Discovering the type_id

`find_node_types` on the TryConsumeSelected graph with empty `context_pins` and
`type_id_filter` `"bMatched"`:

```json
{"returnValue":[]}
```

**No entry contains the literal string `bMatched`.** Rather than go straight to the blind
fallback, the filter was widened to `"Matched"`:

```json
["Class|MovieSceneSkeletalAnimationSection|GetMatchedLocationOffset","Class|MovieSceneSkeletalAnimationSection|GetMatchedRotationOffset","Class|PCGMatchandSetAttributesSettings|GetKeepUnmatched","Class|PCGMatchandSetAttributesSettings|SetKeepUnmatched","Variables|Default|GetMatched","Variables|Default|SetMatched"]
```

The last two are the getter and setter for the new local. The name has no `b` because Unreal
strips the `b` prefix from a bool variable's **display** name — the variable itself is still
`bMatched`. The other four entries are unrelated engine classes.

`Variables|Default|SetMatched` was used. This is a **discovered** type_id, not an improvised
one: it came back from `find_node_types` on this graph, and `Variables|Default|` is the
local/member variable namespace. It cannot be a pre-existing member called `Matched`, because
P4 and the Stage 1 read-back both show no such member exists.

`create_node` with `type_id` `Variables|Default|SetMatched` at `pos` (300, 760):

```json
{"returnValue":{"refPath":"/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:TryConsumeSelected.K2Node_VariableSet_0"}}
```

**The fallback was never needed, and the read-back settles that the two names are the same
node type anyway:** the created node's own `type_id` reads back as **`|SetbMatched`** — the
exact string the command named as the fallback. `Variables|Default|SetMatched` is the
*creation* spelling, `|SetbMatched` is the *stored* spelling, and they are one node type. No
ambiguity remains about which node was made.

### Full pin list of the Set node

`get_node_infos` on `K2Node_VariableSet_0`, position confirmed **(300, 760)**,
`type_id` **`|SetbMatched`**:

| direction | index | name | type_id | value | connected (at creation) |
|---|---|---|---|---|---|
| output | 0 | `then` | `Exec` | `""` | none |
| output | 1 | **`Output_Get`** | `Boolean` | `"false"` | none |
| input | 0 | `execute` | `Exec` | `""` | none |
| input | 1 | **`bMatched`** | `Boolean` | `"false"` | none |

Two things this settles. The input pin is named **`bMatched`**, with the `b` — so the node
targets the local variable that was just created, not some other symbol. And:

> **The node HAS an output pin named `Output_Get`, at output index 1.**

So the first case applies: **no getter node was needed and none was created.** "The latch
output" throughout Stage 3 and Stage 4 means `K2Node_VariableSet_0` **[out 1 `Output_Get`]`**.
The graph therefore gains exactly one node, and the expected final count is 14, not 15.

---

## Stage 3 — rewire

Every pin was resolved by name to its index from a `get_node_infos` read, never by assuming
an index. The indices used:

- ANDBoolean out [0] = `ReturnValue`
- FunctionEntry out [0] = `then`
- Set in [0] = `execute`, in [1] = `bMatched`, out [0] = `then`, out [1] = `Output_Get`
- Branch in [0] = `execute`, in [1] = `Condition`
- Return in [1] = `Success`

| # | operation | call | returned |
|---|---|---|---|
| 1 | connect ANDBoolean [out 0 `ReturnValue`] → Set [in 1 `bMatched`] | `connect_pins` | `{"returnValue":null}` |
| 2 | break FunctionEntry [out 0 `then`] → Branch [in 0 `execute`] | `break_pins` | `{"returnValue":null}` |
| 3 | connect FunctionEntry [out 0 `then`] → Set [in 0 `execute`] | `connect_pins` | `{"returnValue":null}` |
| 4 | connect Set [out 0 `then`] → Branch [in 0 `execute`] | `connect_pins` | `{"returnValue":null}` |
| 5 | break ANDBoolean [out 0] → Branch [in 1 `Condition`] | `break_pins` | `{"returnValue":null}` |
| 6 | connect Set [out 1 `Output_Get`] → Branch [in 1 `Condition`] | `connect_pins` | `{"returnValue":null}` |
| 7 | break ANDBoolean [out 0] → Return [in 1 `Success`] | `break_pins` | `{"returnValue":null}` |
| 8 | connect Set [out 1 `Output_Get`] → Return [in 1 `Success`] | `connect_pins` | `{"returnValue":null}` |

All eight in the specified order. `connect_pins` and `break_pins` both declare no output
schema, so `null` is what a completed call returns from each — none of these eight values is
evidence of anything. Stage 4 is the evidence.

---

## Stage 4 — verify

### V1 — ANDBoolean output [0] destinations

Expected: exactly one entry, the Set node's `bMatched` input. Not the Branch, not the Return.

Measured, verbatim:

```json
{"value":"false","connected_pins":[{"direction":"EGPD_Input","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_VariableSet_0"}}],"pin_id":{"direction":"EGPD_Output","index_id":0,"node":{"refPath":"…:TryConsumeSelected.K2Node_CommutativeAssociativeBinaryOperator_0"}},"type_id":"Boolean","name":"ReturnValue"}
```

Exactly one destination: `K2Node_VariableSet_0` [in 1], which is the pin named `bMatched`.
The Branch and the Return are both gone from this list. **V1 PASS.**

### V2 — Branch [in 1 `Condition`] sources

Expected: exactly one entry, the latch output.

Measured, verbatim:

```json
{"value":"true","connected_pins":[{"direction":"EGPD_Output","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_VariableSet_0"}}],"pin_id":{"direction":"EGPD_Input","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_IfThenElse_0"}},"type_id":"Boolean","name":"Condition"}
```

Exactly one source: `K2Node_VariableSet_0` [out **1**] = `Output_Get`. **V2 PASS.**

### V3 — Return [in 1 `Success`] sources

Expected: exactly one entry, the latch output.

Measured, verbatim:

```json
{"value":"false","connected_pins":[{"direction":"EGPD_Output","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_VariableSet_0"}}],"pin_id":{"direction":"EGPD_Input","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_FunctionResult_0"}},"type_id":"Boolean","name":"Success"}
```

Exactly one source: `K2Node_VariableSet_0` [out 1] = `Output_Get`. **V3 PASS.**

**V2 and V3 together are the fix.** Branch and Return now read the same latched storage, set
once before `SetArrayElem` runs. They can no longer disagree.

### V4 — the exec chain through the Set node

| | expected | measured | |
|---|---|---|---|
| Branch [in 0 `execute`] source | Set node's `then` | `K2Node_VariableSet_0` [out 0] = `then` | **PASS** |
| Set [in 0 `execute`] source | FunctionEntry `then` | `K2Node_FunctionEntry_0` [out 0] = `then` | **PASS** |

**V4 PASS.** The Set is spliced in front of the Branch, so the latch is written before the
Branch reads it.

### V5 — Branch outputs unchanged

| | expected | measured | |
|---|---|---|---|
| out [0] `then` | → `K2Node_CallArrayFunction_0` | `K2Node_CallArrayFunction_0` [in 0] | **PASS** |
| out [1] `else` | → `K2Node_FunctionResult_0` [in 0] | `K2Node_FunctionResult_0` [in 0] | **PASS** |

**V5 PASS.** Identical to P3.

### V6 — SetArrayElem pins unchanged

| pin | expected | measured | |
|---|---|---|---|
| `execute` [in 0] | from Branch `then` | `K2Node_IfThenElse_0` [out 0] | **PASS** |
| `TargetArray` [in 1] | from `K2Node_VariableGet_2` | `K2Node_VariableGet_2` [out 0] | **PASS** |
| `Index` [in 2] | from `K2Node_PromotableOperator_0` | `K2Node_PromotableOperator_0` [out 0] | **PASS** |
| `Item` [in 3] | unconnected, empty value | `connected_pins: []`, `value: ""` | **PASS** |
| `bSizeToFit` [in 4] | false | `connected_pins: []`, `value: "false"` | **PASS** |
| `then` [out 0] | → `K2Node_CallFunction_0` | `K2Node_CallFunction_0` [in 0] | **PASS** |

**V6 PASS.** Position still (820, 0), type_id still `Utilities|Array|SetArrayElem`. The
consume path itself was not altered — only when its result is read.

### V7 — int-int output still feeds both consumers

Expected: `K2Node_PromotableOperator_0` output feeds BOTH `K2Node_GetArrayItem_0` [in 1] and
`K2Node_CallArrayFunction_0` [in 2].

Measured, verbatim:

```json
{"value":"","connected_pins":[{"direction":"EGPD_Input","index_id":1,"node":{"refPath":"…:TryConsumeSelected.K2Node_GetArrayItem_0"}},{"direction":"EGPD_Input","index_id":2,"node":{"refPath":"…:TryConsumeSelected.K2Node_CallArrayFunction_0"}}],"pin_id":{"direction":"EGPD_Output","index_id":0,"node":{"refPath":"…:TryConsumeSelected.K2Node_PromotableOperator_0"}},"type_id":"Integer","name":"ReturnValue"}
```

Both destinations present, in that order. **V7 PASS.**

This one is worth naming: `int-int` is *also* a pure node read twice, and it was deliberately
left alone. It is not a bug, because it reads `SelectedSlot`, which nothing in this function
writes — both reads return the same value. Only the AND chain was hazardous, because
`SetArrayElem` mutates what it reads.

### V8 — node counts

| graph | expected | measured | |
|---|---|---|---|
| `TryConsumeSelected` | 14 (15 only if a getter had been needed — it was not) | **14** | **PASS** |
| `TryAddItem` | still 12 | **12** | **PASS** |
| `EventGraph` | still 87 | **87** | **PASS** |

**V8 PASS.** The TryConsumeSelected list is the 13 original nodes plus
`K2Node_VariableSet_0`; no original node was removed. The `TryAddItem` and `EventGraph`
listings came back element-for-element identical to P5.

### Verify summary

| check | result |
|---|---|
| V1 ANDBoolean → Set only | PASS |
| V2 Branch Condition ← latch only | PASS |
| V3 Return Success ← latch only | PASS |
| V4 exec chain Entry → Set → Branch | PASS |
| V5 Branch outputs unchanged | PASS |
| V6 SetArrayElem unchanged | PASS |
| V7 int-int still feeds both | PASS |
| V8 counts 14 / 12 / 87 | PASS |

Eight of eight.

---

## Stage 5 — compile and save

`compile_blueprint` on `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter`
(`warnings_as_errors` left at its default, `false`):

```json
{"returnValue":null}
```

The tool declares no output schema, so `null` is what a completed call returns — it carries
no pass/fail information and is not evidence of a clean compile.

`AssetTools.save_assets` on `["/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"]`:

```json
{"returnValue":true}
```

**This `true` was checked against the disk, because command 40 produced a `true` from this
same tool while writing nothing.** Here it is truthful:

```
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
-rw-r--r-- 1 a0108 197609 592040 2026-08-30_21:09:54 Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

The asset is modified in `git status` and its mtime is the moment of the save. The Blueprint
reached disk.

---

## Errors and warnings

**No error or warning was produced by any call in this command.** Every pre-flight check,
`add_variable`, both `list_variables` read-backs, both `find_node_types` calls, `create_node`,
all eight rewire calls, every `get_node_infos`, every `find_nodes`, `compile_blueprint` and
`save_assets` returned without a message.

There is therefore no error text to reproduce. Two results were *empty* rather than
erroneous, and neither is a warning:

```json
{"returnValue":[]}
```

— returned by `find_node_types` with `type_id_filter` `"bMatched"` (the `b`-prefix spelling
does not appear in any type_id), and by `find_nodes` on EventGraph with
`title` `"K2Node_Message_1"` (that argument matches a node's *title*, not its object name; it
was a probe and was replaced by a full re-listing).

`compile_blueprint` emitted nothing through the MCP surface. The editor's own Message Log and
Output Log were **not** read as part of this command, so a compile warning that appeared only
there would not have been captured here.

---

## Not confirmed

- **The fix was not tested in PIE.** The bug was confirmed in PIE on 2026-08-30, but the
  repaired function has not been run. Nobody has yet observed `TryConsumeSelected` return
  `true` after consuming, and nobody has yet seen BP_Door unlock. The graph is correct by
  read-back; the behaviour is unverified.
- **The compile is not confirmed clean.** `null` proves only that the call completed. No
  Message Log was read.
- The `Output_Get` pin was wired and read back as connected, but its *runtime* value has not
  been observed. That it returns the latched value rather than re-reading is the documented
  behaviour of an impure Set node, not something measured here.
- `bMatched` is never explicitly reset between calls. As a local it is re-initialised per
  invocation by the Blueprint VM, and it is written before every read on the one path that
  reads it — but this was reasoned from the graph, not measured.
