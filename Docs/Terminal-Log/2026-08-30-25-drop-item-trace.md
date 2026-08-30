# 2026-08-30 — Q (drop item) ground trace and hit/miss branch

Continues the Q island in `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`, `EventGraph`.
Attached to `K2Node_IfThenElse_5 . then`, which the previous command left open.

All 8 requested nodes were created and wired. **One extra node beyond the requested list was
required** — see section 4. Blueprint compiled clean and saved.

Everything in the read-back sections comes from `get_node_infos` run AFTER the work, not from
what was requested.

---

## 1. Dirty check before any work

`AssetTools.is_dirty` on `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`, called before
a single node was created:

```
{"returnValue":false}
```

**Not dirty this time.** The previous command found it already dirty before any work and had to
save an unknown pre-existing change to disk along with its own. That did not recur here: the
Blueprint was clean at the start, so everything now in the saved `.uasset` beyond the previous
command's state was made by this command.

---

## 2. Nodes created — name, type_id, x, y (read back)

| # | role | node name | type_id (read back) | x | y |
|---|---|---|---|---|---|
| 13 | Get Actor Location | `K2Node_CallFunction_5` | `Transformation\|GetActorLocation` | -1300 | 3650 |
| 14 | Get Actor Forward Vector | `K2Node_CallFunction_6` | `Transformation\|GetActorForwardVector` | -1300 | 3820 |
| — | **extra** float literal 150.0 | `K2Node_CallFunction_10` | `Math\|Float\|MakeLiteralFloat` | -1300 | 3980 |
| 15 | vector * float | `K2Node_PromotableOperator_12` | `Math\|Vector\|vector*vector` | -1060 | 3820 |
| 16 | vector + vector (TraceStart) | `K2Node_PromotableOperator_13` | `Math\|Vector\|vector+vector` | -820 | 3700 |
| 17 | vector + vector (TraceEnd) | `K2Node_PromotableOperator_14` | `Math\|Vector\|vector+vector` | -580 | 3820 |
| 18 | LineTraceByChannel | `K2Node_CallFunction_7` | `Collision\|LineTraceByChannel` | -300 | 3400 |
| 19 | Branch (hit / miss) | `K2Node_IfThenElse_6` | `Utilities\|FlowControl\|Branch` | 100 | 3400 |
| 20 | PrintString | `K2Node_CallFunction_8` | `Development\|PrintString` | 400 | 3600 |

All within the requested band: y 3400–3980, x -1300 to 400. The one y value outside the stated
3400–3900 range is the extra literal node at y=3980, placed below node 14 so it does not
overlap anything.

### type_ids passed vs read back

As anticipated, several requested strings do not exist in the creatable-node registry.
`find_node_types` was used to find the real ones.

| requested | passed to `create_node` | reads back as |
|---|---|---|
| Get Actor Location (self) | `Transformation\|GetActorLocation` | `Transformation\|GetActorLocation` |
| Get Actor Forward Vector (self) | `Transformation\|GetActorForwardVector` | `Transformation\|GetActorForwardVector` |
| `Math\|Vector\|vector*float` | `Utilities\|Operators\|Multiply` | `Math\|Vector\|vector*vector` |
| `Math\|Vector\|vector+vector` (x2) | `Utilities\|Operators\|Add` | `Math\|Vector\|vector+vector` |
| `Collision\|LineTraceByChannel` | `Collision\|LineTraceByChannel` | `Collision\|LineTraceByChannel` |
| `Utilities\|FlowControl\|Branch` | `Utilities\|FlowControl\|Branch` | `Utilities\|FlowControl\|Branch` |
| `Development\|PrintString` | `Development\|PrintString` | `Development\|PrintString` |

`Math|Vector|vector*float` **does not exist as a readable type_id anywhere in this project.**
The existing F-chain multiply node `K2Node_PromotableOperator_2` — which has a Vector A and a
`Float (double-precision)` B, i.e. it *is* a vector-times-float node — also reads back as
`Math|Vector|vector*vector`. So `vector*vector` is the correct and expected read-back here;
the float-ness lives in the B pin's type, not in the type_id.

The two `Add` nodes and the `Multiply` were created as wildcard promotables and showed
placeholder types immediately after creation (`Utilities|TimeManagement|Seconds*FrameRate`,
`Utilities|TimeManagement|FrameNumber+Int` twice). They resolved to the vector forms once the
Vector sources were connected.

---

## 3. Input pins of nodes 13–20 — read back

**13. `K2Node_CallFunction_5` — Get Actor Location**
- `self` (Actor Object Reference) = `""` — no connection. Unconnected `self` is the "(self)"
  target, i.e. this Character.

Output `ReturnValue` (Vector) -> `K2Node_PromotableOperator_13` [in 0].

**14. `K2Node_CallFunction_6` — Get Actor Forward Vector**
- `self` (Actor Object Reference) = `""` — no connection. Same "(self)" target.

Output `ReturnValue` (Vector) -> `K2Node_PromotableOperator_12` [in 0].

**extra. `K2Node_CallFunction_10` — MakeLiteralFloat**
- `Value` (Float (double-precision)) = `"150.0"` — no connection.

Output `ReturnValue` (Float (double-precision)) -> `K2Node_PromotableOperator_12` [in 1].

**15. `K2Node_PromotableOperator_12` — vector * float**
- `A` (Vector) = `""` <- `K2Node_CallFunction_6` [out 0] (Get Actor Forward Vector)
- `B` (**Float (double-precision)**) = `""` <- `K2Node_CallFunction_10` [out 0] (literal 150.0)

Output `ReturnValue` (Vector) -> `K2Node_PromotableOperator_13` [in 1].

B is a float pin, matching the F-chain reference node's pin types exactly. The 150.0 arrives
through the literal node rather than as a pin default — see section 4 for why.

**16. `K2Node_PromotableOperator_13` — vector + vector (TraceStart)**
- `A` (Vector) = `""` <- `K2Node_CallFunction_5` [out 0] (Get Actor Location)
- `B` (Vector) = `""` <- `K2Node_PromotableOperator_12` [out 0] (forward * 150)

Output `ReturnValue` (Vector) fans out to **two** consumers:
`K2Node_PromotableOperator_14` [in 0] and `K2Node_CallFunction_7` [in 1] (the trace's Start).
**Created once, not duplicated**, as required.

**17. `K2Node_PromotableOperator_14` — vector + vector (TraceEnd)**
- `A` (Vector) = `""` <- `K2Node_PromotableOperator_13` [out 0] (TraceStart)
- `B` (Vector) = `"0, 0, -300"` — **no connection, a literal pin value** as required

Output `ReturnValue` (Vector) -> `K2Node_CallFunction_7` [in 2] (the trace's End).

**18. `K2Node_CallFunction_7` — LineTraceByChannel**

| pin | type | value | source |
|---|---|---|---|
| `execute` | Exec | — | `K2Node_IfThenElse_5` [out 0] (`then`) |
| `Start` | Vector | `0, 0, 0` | `K2Node_PromotableOperator_13` [out 0] |
| `End` | Vector | `0, 0, 0` | `K2Node_PromotableOperator_14` [out 0] |
| `TraceChannel` | ETraceTypeQuery Enum | `TraceTypeQuery1` | — |
| `bTraceComplex` | Boolean | `false` | — |
| `ActorsToIgnore` | Array of Actor Object References | `""` | — (left at default) |
| `DrawDebugType` | EDrawDebugTrace Enum | `ForDuration` | — |
| `bIgnoreSelf` | Boolean | `true` | — |
| `TraceColor` | Linear Color Structure | `(R=1.000000,G=0.000000,B=0.000000,A=1.000000)` | — (left at default) |
| `TraceHitColor` | Linear Color Structure | `(R=0.000000,G=1.000000,B=0.000000,A=1.000000)` | — (left at default) |
| `DrawTime` | Float (single-precision) | `5.000000` | — |

The `Start` / `End` pins still show their literal `0, 0, 0` defaults; that value is dead
because both pins are connected. This is the same as the F-chain trace, whose Start/End also
read `0, 0, 0` under live connections.

Of these, only `DrawDebugType` had to be written — it is created as `None`. `TraceTypeQuery1`,
`bTraceComplex false`, `bIgnoreSelf true` and `DrawTime 5.000000` were already the node's
creation defaults and match the F-chain reference `K2Node_CallFunction_25` exactly.
**`DrawDebugType` is the one trace setting that differs from the F-chain reference**, which
reads `None`; `ForDuration` was requested here.

Start comes from the actor location chain, not from a camera node — `K2Node_CallFunction_20`
(`GetCameraLocation`, used by the F trace) was not touched or referenced.

Outputs: `then` [0] -> `K2Node_IfThenElse_6` [in 0]; `OutHit` [1] -> nothing;
`ReturnValue` [2] -> `K2Node_IfThenElse_6` [in 1].

**19. `K2Node_IfThenElse_6` — Branch (hit / miss)**
- `execute` (Exec) <- `K2Node_CallFunction_7` [out 0] (`then`)
- `Condition` (Boolean) = `"true"` <- `K2Node_CallFunction_7` [out 2] (`ReturnValue`)

**20. `K2Node_CallFunction_8` — PrintString**

| pin | type | value | source |
|---|---|---|---|
| `execute` | Exec | — | `K2Node_IfThenElse_6` [out 1] (`else`) |
| `InString` | String | `CANNOT DROP HERE` | — |
| `bPrintToScreen` | Boolean | `true` | — |
| `bPrintToLog` | Boolean | `true` | — |
| `TextColor` | Linear Color Structure | `(R=0.000000,G=0.660000,B=1.000000,A=1.000000)` | — |
| `Duration` | Float (single-precision) | `3.0` | — |
| `Key` | Name | `None` | — |

Every value matches the INVENTORY FULL reference node `K2Node_CallFunction_36` read back at the
start of this command, except `InString`. Only `InString` and `Duration` had to be written —
the node is created with `InString` = `Hello` and `Duration` = `2.000000`; `bPrintToScreen`,
`bPrintToLog`, `TextColor` and `Key` were already correct at creation.

`Duration` reads back as `3.0` here and as `3.0` on the reference node — same string.

Output `then` [0] -> nothing.

---

## 4. The extra node — why node 15's B could not be a pin default

**This command created 9 nodes, not the 8 in the list.** The extra one is
`K2Node_CallFunction_10` (`Math|Float|MakeLiteralFloat`, `Value` = `150.0`) at (-1300, 3980),
feeding node 15's `B` pin.

It was not possible to build node 15 as written — `B = 150.0` as a pin value — with the tools
available. The evidence, in order:

1. `Utilities|Operators|Multiply` is created as a wildcard. Connecting the forward vector to
   `A` resolved the node to `Math|Vector|vector*vector` and **made `B` a Vector pin**:

   ```
   {"type_id": "Math|Vector|vector*vector", "in": [[0, "A", "Vector", ""], [1, "B", "Vector", ""]]}
   ```

2. `set_pin_value` on that Vector `B` with `"150.0"` returned `{"returnValue":null}` — it did
   not raise — but the read-back showed the value had **not** been written:

   ```
   [1, "B", "Vector", ""]
   ```

   This is the return-value-is-not-evidence pattern: the call reported nothing wrong and
   changed nothing.

3. `set_pin_value` does work on Vector pins when the string is a valid vector literal. Node
   17's `B` was set to `"0, 0, -300"` on an identical Vector pin and read back correctly:

   ```
   [1, "B", "Vector", "0, 0, -300"]
   ```

   So the failure in step 2 is specifically that `"150.0"` is not a valid Vector literal, not
   that Vector pins reject values.

4. No `vector * float` node exists in the creatable registry. The full `Math|Vector|` listing
   (94 entries) contains no multiply, and a search for `Scale` turned up no vector-scale-by-float
   function. `retarget_node_class` only swaps Blueprint class references on cast / call / event
   nodes; it cannot change an operator's overload.

5. Connecting a float output to `B` **does** select the vector*float overload:

   ```
   after float connected:  [[0, "A", "Vector", ""], [1, "B", "Float (double-precision)", ""]]
   ```

   but breaking that connection reverts it, and a subsequent `set_pin_value` of `"150.0"` still
   does nothing:

   ```
   after break:            [[0, "A", "Vector", ""], [1, "B", "Vector", ""]]
   after set B = "150.0":  [[0, "A", "Vector", ""], [1, "B", "Vector", ""]]
   ```

So keeping a float source wired to `B` is the only way through this tool surface to get the
requested `vector * float` with 150.0. The alternative — writing `B` as the Vector literal
`150, 150, 150` — is numerically identical for any A, but it would change the pin's data type
away from what was asked and would put a value in the graph that was never written down. The
extra node was judged the smaller deviation because it preserves the exact requested semantics
and matches the pin types of the existing F-chain multiply node.

**This is a decision made here, not something that was asked for.** If the extra node is
unwanted, deleting `K2Node_CallFunction_10` and setting node 15's `B` to `150, 150, 150`
produces the same trace start; say so and it will be changed.

---

## 5. Node 19's `then` is open — read back

From the `get_node_infos` read of `K2Node_IfThenElse_6` taken after all work was done:

```
{"i": 0, "n": "then", "t": "Exec", "to": []}
{"i": 1, "n": "else", "t": "Exec", "to": ["K2Node_CallFunction_8[in 0]"]}
```

`to` is the list of pins the output is connected to. **`K2Node_IfThenElse_6.then` has no
connection** — that is where the next command attaches the spawn. Its `else` goes to the
PrintString, as specified.

`K2Node_IfThenElse_5.else` (the previous command's second gate) also still reads `to: []`.

---

## 6. EventGraph node count

From the length of a `find_nodes` result (graph = EventGraph, `title` = `""`), not counted by
hand:

- **Before:** 82
- **After:** 91

91 - 82 = 9, which is the 8 requested nodes plus the one extra literal node from section 4, and
confirms nothing else was added or removed anywhere in the graph.

**Not verified:** no node outside the Q island was re-read one by one this time. The count
going from exactly 82 to exactly 91 is the evidence that nothing was deleted. Every
`connect_pins` call in this command named only Q-island nodes, and `K2Node_IfThenElse_5` — the
one pre-existing node touched — was the intended attachment point; its read-back shows its
`execute` and `Condition` inputs unchanged and only its previously-empty `then` now filled.

---

## 7. Compile result

`BlueprintTools.compile_blueprint`, `warnings_as_errors` = `false`. Returned:

```
{"returnValue":null}
```

The tool raises on error; it did not raise. The log around the compile:

```
[2026.08.30-01.22.01:427][725]LogModelContextProtocol: Running tool: 'call_tool'
[2026.08.30-01.22.01:429][725]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint'
[2026.08.30-01.22.01:429][725]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.08.30-01.22.01:533][725]LogUObjectHash: Compacting FUObjectHashTables data took   1.55ms
[2026.08.30-01.22.06:095][739]LogModelContextProtocol: Running tool: 'call_tool'
```

Nothing between the compile line and the next tool call. **No compile errors, no compile
warnings.**

**Not verified:** as in the previous command, no tool reports a Blueprint's compiled status
flag directly. "Compiled clean" rests on the tool not raising plus an empty log window.

Saved with `AssetTools.save_assets` -> `true`; `AssetTools.is_dirty` afterwards -> `false`.

---

## 8. Errors and warnings — exact English text

### 8.1 From this work

**No tool call in this command returned an error.** Every `create_node`, `connect_pins`,
`break_pins` and `set_pin_value` call completed without raising.

The one silent failure is recorded in section 4: `set_pin_value` on
`K2Node_PromotableOperator_12` input pin 1 with value `"150.0"` returned

```
{"returnValue":null}
```

with no error text, no warning, and no change to the pin. There is no English message to quote
because the plugin emitted none — the failure is visible only by reading the pin back.

### 8.2 Present in the log but NOT from this work

The `LogBlueprint` warning block from `00.36.49` is still the newest set of Blueprint warnings
in the log. It predates this command by roughly 45 minutes and every node it names is a
pre-existing one; none of the nine new node names appears in it. It was already recorded in the
previous command's report. First and last lines of that block, verbatim:

```
[2026.08.30-00.36.49:926][550]LogBlueprint: Warning: No execute pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_Event_5
```

```
[2026.08.30-00.36.49:926][550]LogBlueprint: Warning: No then pin found on node /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_CallFunction_27
```

A scan of the whole log window covering this command (`01.20` – `01.22`) returned only
`LogEOSSDK` config-update lines and `LogModelContextProtocol` tool-dispatch lines. No error and
no warning from any category.

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
?? Docs/Terminal-Log/2026-08-30-24-drop-item-gate.md
```

`BP_ThirdPersonCharacter.uasset` is the file this command changed. Everything else is from the
two previous commands or predates this session.

---

## 10. Handoff to the next command

The Q chain now runs: `IA_DropItem.Started` -> slot-range gate -> slot-not-empty gate ->
ground trace -> hit/miss branch, with the miss branch printing CANNOT DROP HERE.

The next command builds the spawn and attaches it to:

```
K2Node_IfThenElse_6 . then     (output pin index 0, currently unconnected)
```

Useful names for that work:

- `K2Node_CallFunction_7` output 1 — `OutHit` (Hit Result Structure), **currently unconnected**;
  break it for the impact point to spawn at
- `K2Node_CallFunction_7` output 2 — `ReturnValue` (Boolean), already feeding the branch
- `K2Node_GetArrayItem_1` output 0 — the row name of the item being dropped (Name)
- `K2Node_PromotableOperator_8` output 0 — the `SelectedSlot - 1` index (Integer), for the slot
  clearing that is still to come
- `BP_ItemPickup`'s `ItemRow` variable still has **Expose on Spawn unknown / not set** — see
  `2026-08-30-23-drop-item-prep.md` section 3. If the spawn needs an `ItemRow` pin on
  SpawnActor, that has to be turned on by hand in the editor first.
