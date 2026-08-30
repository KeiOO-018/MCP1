# 2026-08-30 — BP_ThirdPersonHUD EventGraph: the message drawing block

Nine nodes created and one rewire, in `BP_ThirdPersonHUD:EventGraph`. Compiled clean and saved.

`write_graph_dsl` was **not** used on this graph. Everything was done with `create_node`,
`connect_pins`, `break_pins` and `get_node_infos`. `AssetTools.is_dirty` was not called.

---

## 1. Pre-flight — all four checks passed

### Check 1 — node count

`find_nodes` on `BP_ThirdPersonHUD:EventGraph` with an empty title returned **107** nodes. Pass.

### Check 2 — K2Node_MacroInstance_2

```
type_id : Utilities|IsValid
position: (480, -700)
outputs :
  [0] "Is Valid"     -> K2Node_MacroInstance_0 [in 0]
  [1] "Is Not Valid" -> K2Node_DynamicCast_0 [in 0]
inputs  :
  [0] "exec"        <- K2Node_Event_3 [out 1]
  [1] "InputObject" <- K2Node_VariableGet_16 [out 0]
```

type_id is `Utilities|IsValid`, output pin index 0 is named `Is Valid`, and it is connected to
`K2Node_MacroInstance_0` input pin index 0. Pass.

### Check 3 — K2Node_MacroInstance_0

```
type_id : Utilities|FlowControl|ForLoop
position: (6720, 0)
inputs  :
  [0] "execute"    <- K2Node_MacroInstance_2 [out 0], K2Node_VariableSet_0 [out 0]
  [1] "FirstIndex" <- (none)
  [2] "LastIndex"  <- K2Node_PromotableOperator_10 [out 0]
```

type_id is `Utilities|FlowControl|ForLoop`, and input pin 0 `execute` carried exactly the two
incoming connections named in the command. Pass.

### Check 4 — variables

`list_variables` returned all 18, including all six the command required:

```
MessageText, MessageExpireTime, ColorMessage, MessageMargin, MessageDuration, TextScale
```

Pass.

---

## 2. Position scan of the target band — nothing in the way

Every one of the 107 existing nodes was read with `get_node_infos` and filtered for
y within 400 of −1600, i.e. −2000 ≤ y ≤ −1200:

```
[]
```

**No existing node falls in that band.** In fact the whole EventGraph has only six nodes with
any negative y at all, and the most negative is −700 — 900 units clear of the target row:

| node | type_id | x | y |
|---|---|---|---|
| `K2Node_VariableGet_16` | `\|GetCachedCharacter` | 200 | -700 |
| `K2Node_MacroInstance_2` | `Utilities\|IsValid` | 480 | -700 |
| `K2Node_CallFunction_10` | `HUD\|GetOwningPlayerController` | 200 | -400 |
| `K2Node_CallFunction_11` | `Pawn\|GetControlledPawn` | 520 | -400 |
| `K2Node_DynamicCast_0` | `Utilities\|Casting\|CastToBP_ThirdPersonCharacter` | 840 | -480 |
| `K2Node_VariableSet_0` | `\|SetCachedCharacter` | 1200 | -480 |

So the nine new nodes went at **y = −1600 as originally specified**. The fallback to y = −2200
was not needed and was not used.

---

## 3. The nine new nodes — refPath, type_id, position

All at y = −1600, x spread evenly from 1200 to 2600 in left-to-right dataflow order.
(`...` = `/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD:EventGraph`)

| step | refPath | type_id (read back) | x | y |
|---|---|---|---|---|
| a | `....K2Node_CallFunction_21` | `Utilities\|Time\|GetTimeSeconds` | 1200 | -1600 |
| b | `....K2Node_VariableGet_27` | `\|GetMessageExpireTime` | 1375 | -1600 |
| c | `....K2Node_PromotableOperator_42` | `Math\|Float\|float<float` | 1550 | -1600 |
| d | `....K2Node_IfThenElse_0` | `Utilities\|FlowControl\|Branch` | 1725 | -1600 |
| f | `....K2Node_VariableGet_29` | `\|GetMessageText` | 1900 | -1600 |
| g | `....K2Node_VariableGet_30` | `\|GetColorMessage` | 2075 | -1600 |
| h | `....K2Node_VariableGet_31` | `\|GetMessageMargin` | 2250 | -1600 |
| i | `....K2Node_VariableGet_32` | `\|GetTextScale` | 2425 | -1600 |
| e | `....K2Node_CallFunction_25` | `HUD\|DrawText` | 2600 | -1600 |

**Exactly one getter per variable.** `K2Node_VariableGet_31` (MessageMargin) feeds two DrawText
pins from its single output; no second margin getter was created.

### One type_id read-back difference

Node **c** was created as `Utilities|Operators|Less(<)`, the type_id the command specified, and
**reads back as `Math|Float|float<float`**. It was created as a wildcard (showing
`Math|Timespan|Timespan<Timespan` immediately after creation, both pins Wildcard) and resolved
to the float overload when the two double-precision sources were connected. Same promotable
behaviour recorded in commands 24, 25, 27 and 31.

---

## 4. The new Branch — full pin list, read back after wiring

`K2Node_IfThenElse_0`, `Utilities|FlowControl|Branch`, at (1725, −1600):

**Inputs**

| # | pin | type | value | source |
|---|---|---|---|---|
| 0 | `execute` | Exec | — | `K2Node_MacroInstance_2` [out 0] (`Is Valid`) |
| 1 | `Condition` | Boolean | `true` | `K2Node_PromotableOperator_42` [out 0] |

**Outputs**

| # | pin | type | goes to |
|---|---|---|---|
| 0 | `then` | Exec | `K2Node_CallFunction_25` [in 0] (DrawText `execute`) |
| 1 | `else` | Exec | `K2Node_MacroInstance_0` [in 0] (ForLoop `execute`) |

**Naming note:** the command calls these outputs `True` and `False`. The pins read back as
`then` (index 0) and `else` (index 1) — `then` is the true branch and `else` is the false
branch. Step 2c ("Branch True -> DrawText execute") was wired from index 0, and step 2e
("Branch False -> ForLoop execute") from index 1.

The condition chain feeding it, read back:

```
K2Node_PromotableOperator_42  Math|Float|float<float
  A (Float, double-precision) <- K2Node_CallFunction_21 [out 0]   (GetTimeSeconds)
  B (Float, double-precision) <- K2Node_VariableGet_27  [out 0]   (MessageExpireTime)
  ReturnValue (Boolean)       -> K2Node_IfThenElse_0 [in 1]
```

So the branch is true while `GetTimeSeconds < MessageExpireTime` — the message is still live.

---

## 5. The new DrawText — full pin list, read back after wiring

`K2Node_CallFunction_25`, `HUD|DrawText`, at (2600, −1600):

**Inputs**

| # | pin | type | value | source |
|---|---|---|---|---|
| 0 | `execute` | Exec | — | `K2Node_IfThenElse_0` [out 0] (`then`) |
| 1 | `self` | HUD Object Reference | `""` | **unconnected** — left alone |
| 2 | `Text` | String | `""` | `K2Node_VariableGet_29` [out 0] (MessageText) |
| 3 | `TextColor` | Linear Color Structure | `(R=0,G=0,B=0,A=1)` | `K2Node_VariableGet_30` [out 0] (ColorMessage) |
| 4 | `ScreenX` | Float (single-precision) | `0.0` | `K2Node_VariableGet_31` [out 0] (MessageMargin) |
| 5 | `ScreenY` | Float (single-precision) | `0.0` | `K2Node_VariableGet_31` [out 0] (MessageMargin — **the same node**) |
| 6 | `Font` | Font Object Reference | `""` | **unconnected** — value untouched |
| 7 | `Scale` | Float (single-precision) | `1.000000` | `K2Node_VariableGet_32` [out 0] (TextScale) |
| 8 | `bScalePosition` | Boolean | `false` | **unconnected** — left at `false`, untouched |

**Outputs**

| # | pin | type | goes to |
|---|---|---|---|
| 0 | `then` | Exec | `K2Node_MacroInstance_0` [in 0] (ForLoop `execute`) |

Every connection was made by pin name resolved to its index from a `get_node_infos` read of the
node taken before wiring, not by assuming an index order.

`ScreenX` and `ScreenY` both list `K2Node_VariableGet_31 [out 0]` as their source, confirming
one getter feeds both pins.

The residual `value` entries on connected pins (`(R=0,G=0,B=0,A=1)`, `0.0`, `1.000000`) are the
dead literal defaults sitting under live connections — the same thing seen on the trace Start/End
pins in command 25.

### No conversion nodes were inserted

`MessageMargin` and `TextScale` are `Float (double-precision)`; `ScreenX`, `ScreenY` and `Scale`
are `Float (single-precision)`. The node count was sampled three times during data wiring —
after node creation, after the first double→single connection, and after all of them — and read
**116, 116, 116**. UE 5.8 narrows on the pin without adding a `Conv_DoubleToFloat` node, so the
final count is unaffected.

---

## 6. K2Node_MacroInstance_0 [in 0] — three incoming connections

Read back after the rewire:

```
K2Node_MacroInstance_0  input pin [0] "execute"  (Exec)
  <- K2Node_VariableSet_0   [out 0]
  <- K2Node_CallFunction_25 [out 0]
  <- K2Node_IfThenElse_0    [out 1]
```

**Exactly three**, as required:

| source | what it is | status |
|---|---|---|
| `K2Node_VariableSet_0` [out 0] | the pre-existing `SetCachedCharacter` -> ForLoop link | **untouched** — never broken, never reconnected |
| `K2Node_CallFunction_25` [out 0] | new — DrawText `then` (step 2d) | added |
| `K2Node_IfThenElse_0` [out 1] | new — Branch `else` / False (step 2e) | added |

The rewire was traced step by step, reading the incoming list after each stage:

```
before      : ["K2Node_MacroInstance_2[out 0]", "K2Node_VariableSet_0[out 0]"]
after 2a    : ["K2Node_VariableSet_0[out 0]"]                                       <- break removed only the IsValid link
after 2d    : ["K2Node_VariableSet_0[out 0]", "K2Node_CallFunction_25[out 0]"]
after 2e    : ["K2Node_VariableSet_0[out 0]", "K2Node_CallFunction_25[out 0]", "K2Node_IfThenElse_0[out 1]"]
```

`K2Node_VariableSet_0 [out 0]` is present in every one of those four reads. It survived the
command untouched.

The ForLoop's other pins are also unchanged: `FirstIndex` still unconnected, `LastIndex` still
from `K2Node_PromotableOperator_10 [out 0]`, and its three outputs (`LoopBody`, `Index`,
`Completed`) still go exactly where they did in the pre-flight read.

---

## 7. K2Node_MacroInstance_2 [out 0] goes to the Branch and nothing else

Read back after the rewire:

```
K2Node_MacroInstance_2  outputs
  [0] "Is Valid"     -> ["K2Node_IfThenElse_0[in 0]"]
  [1] "Is Not Valid" -> ["K2Node_DynamicCast_0[in 0]"]
```

Output pin 0 (`Is Valid`) has **exactly one** destination, the new Branch. Its old link to
`K2Node_MacroInstance_0` is gone, broken by step 2a.

Its `Is Not Valid` pin still goes to `K2Node_DynamicCast_0`, and both of its input pins are
unchanged (`exec` <- `K2Node_Event_3 [out 1]`, `InputObject` <- `K2Node_VariableGet_16 [out 0]`).
Nothing on this node was touched other than the one break and the one new connection.

### Resulting exec path

```
IsValid . Is Valid
  -> Branch (GetTimeSeconds < MessageExpireTime)
       then  -> DrawText -> ForLoop . execute
       else  ----------------------> ForLoop . execute

SetCachedCharacter . then --------> ForLoop . execute   (pre-existing, untouched)
```

---

## 8. EventGraph node count

From the length of a `find_nodes` result with an empty title:

- **Before:** 107
- **After:** 116

107 + 9 = **116**, matching the required figure exactly. No node was created beyond the nine,
none was removed, and no implicit conversion node appeared.

---

## 9. Compile result

`BlueprintTools.compile_blueprint` on BP_ThirdPersonHUD, `warnings_as_errors` = `false`,
returned:

```
{"returnValue":null}
```

The tool raises on error; it did not raise.

```
[2026.08.30-04.22.36:399][553]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD'
```

No error and no warning followed it. **Compiled clean.**

`AssetTools.save_assets` -> `true`. The save wrote the package and ran the editor's content
validation pass:

```
[2026.08.30-04.22.45:831][581]LogSavePackage: Moving 'D:/20260827/MCP1/Saved/BP_ThirdPersonHUDD5ACDCEF4655794A8DD832A15F6D6677.tmp' to 'D:/20260827/MCP1/Content/ThirdPerson/Blueprints/BP_ThirdPersonHUD.uasset'
[2026.08.30-04.22.46:097][582]AssetCheck: /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD Validating asset
```

Nine validators ran and reported no failure.

**Not verified:** no tool reports a Blueprint's compiled status flag directly. "Compiled clean"
rests on the call not raising plus an empty log window, as in every previous command.

---

## 10. Errors and warnings — exact English text

### 10.1 From this work

**None.** Every call in this command — `find_nodes`, `get_node_infos`, `list_variables`,
`find_node_types`, `create_node` (x9), `connect_pins` (x11), `break_pins` (x1),
`compile_blueprint` and `save_assets` — completed without raising, and nothing was written to
the log beyond routine dispatch, save and validation lines.

There is no error or warning text to quote for this command.

### 10.2 Present in the log but NOT from this work

Nothing new. The `LogBlueprint` warning block from `00.36.49` — which names only pre-existing
nodes in BP_ThirdPersonCharacter, not this HUD — is still the newest set of Blueprint warnings,
now roughly four hours old. Already recorded in commands 24, 25, 27, 28, 29 and 31.

---

## 11. git status after the work

```
 M Content/Interaction/BP_Door.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonHUD.uasset
?? Docs/Terminal-Log/2026-08-30-31-hud-message-vars.md
```

`BP_ThirdPersonHUD.uasset` is the file this command changed.

`Content/Interaction/BP_Door.uasset` is **not** from this command and was already showing as
modified before it started — the same observation recorded in command 31, section 8. BP_Door was
not touched here.

---

## 12. What is not verified

- **Nothing was run in PIE.** The block compiles and its wiring reads correctly, but no message
  has been drawn on screen. Unconfirmed in particular:
  - that `MessageMargin` = 24 puts the text somewhere sensible on screen — it drives both
    ScreenX and ScreenY, so the message sits 24 px from the top-left corner
  - that leaving `Font` unconnected gives a readable default font at `TextScale` = 2
  - that the message actually disappears when `GetTimeSeconds` passes `MessageExpireTime`
  - that `ShowMessage` (built in command 31) is ever called — **nothing calls it yet.** Until
    something does, `MessageExpireTime` stays at its default 0, the Branch condition is false
    from the first frame, and this block draws nothing. That is expected at this stage.
- **That the two new exec links into the ForLoop behave as intended at runtime.** Three
  execution paths now converge on one `execute` pin; that was already true of two of them before
  this command, and the command stated the third is intentional. Whether the ForLoop being
  entered from the DrawText path as well as the Branch-false path is correct for the HUD's draw
  order was not evaluated — it was specified, not derived.
