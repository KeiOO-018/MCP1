# 2026-08-30 — BP_ThirdPersonHUD: five message variables and ShowMessage

Five variables and one function graph added to
`/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD`. The EventGraph was not touched — the drawing
block is the next command. Compiled clean and saved.

`AssetTools.is_dirty` was not called, as instructed.

---

## 1. Pre-flight — both checks passed

### `BlueprintTools.list_variables` on BP_ThirdPersonHUD, verbatim

```
["SlotCount", "SlotSize", "SlotGap", "BottomMargin", "BorderThickness", "ColorIdle",
 "ColorSelected", "CachedCharacter", "HPBarHeight", "ColorHPBack", "ColorHPFill",
 "TextLineHeight", "TextScale"]
```

13 names, exactly the 13 the command listed, in the same order. **No variable whose name starts
with `Message` or `ColorMessage` existed** — nothing was at risk of being overwritten.

### `BlueprintTools.list_functions` on BP_ThirdPersonHUD, verbatim

```
[{"name": "UserConstructionScript", "description": "", "bIsImplemented": true}]
```

Function names: `["UserConstructionScript"]`. **`ShowMessage` was not present.**

Both checks passed, so the build went ahead.

### Also captured before any change

`list_graphs` returned two graphs — `UserConstructionScript` and `EventGraph`.
`find_nodes` on `EventGraph` with an empty title returned **107** nodes.

---

## 2. list_variables AFTER the change — 18 names

Read back from the saved asset:

```
["SlotCount", "SlotSize", "SlotGap", "BottomMargin", "BorderThickness", "ColorIdle",
 "ColorSelected", "CachedCharacter", "HPBarHeight", "ColorHPBack", "ColorHPFill",
 "TextLineHeight", "TextScale", "MessageText", "MessageExpireTime", "ColorMessage",
 "MessageMargin", "MessageDuration"]
```

**18 names.** The original 13 are unchanged and in their original order; the five new ones are
appended in the order the command listed them.

`list_functions` after: `["UserConstructionScript", "ShowMessage"]`.

---

## 3. The five new variables — type and default, read back

Read with `ObjectTools.get_properties` on the Blueprint (which redirects to the CDO,
`Default__BP_ThirdPersonHUD_C`), after the compile:

```
{"MessageText":"",
 "MessageExpireTime":0,
 "ColorMessage":{"r":0,"g":0.6600000262260437,"b":1,"a":1},
 "MessageMargin":24,
 "MessageDuration":3}
```

| variable | type read back | default requested | default read back | matches |
|---|---|---|---|---|
| `MessageText` | `string` | empty string | `""` | yes |
| `MessageExpireTime` | `number` (Float, double-precision) | `0.0` | `0` | yes |
| `ColorMessage` | `LinearColor` struct, fields `r` `g` `b` `a` | R=0.0 G=0.66 B=1.0 A=1.0 | `r`=0, `g`=0.6600000262260437, `b`=1, `a`=1 | yes |
| `MessageMargin` | `number` (Float, double-precision) | `24.0` | `24` | yes |
| `MessageDuration` | `number` (Float, double-precision) | `3.0` | `3` | yes |

Types come from `ObjectTools.list_properties`, which returns the CDO's property schema.

`0`, `24` and `3` print without a decimal point because JSON drops a trailing zero on a whole
number, not because they are integers — the ShowMessage graph read-back in section 4 shows
`MessageExpireTime` and `MessageDuration` on `Float (double-precision)` pins.

`g` reads `0.6600000262260437` rather than `0.66` — that is float32 storage of 0.66 widened for
JSON, the same round-tripping the existing `ColorHPFill` shows (`0.89999997615814209` for 0.9).

### ColorMessage mirrors ColorIdle

`ColorIdle` was read first, as instructed. Its declared schema and `ColorMessage`'s, from
`ObjectTools.list_properties`, are byte-identical:

```
colorIdle    : {"type": "object", "title": "LinearColor", "properties": {"r": {"type": "number", "minimum": 0}, "g": {"type": "number", "minimum": 0}, "b": {"type": "number", "minimum": 0}, "a": {"type": "number", "minimum": 0}}, "required": ["r", "g", "b", "a"]}
colorMessage : {"type": "object", "title": "LinearColor", "properties": {"r": {"type": "number", "minimum": 0}, "g": {"type": "number", "minimum": 0}, "b": {"type": "number", "minimum": 0}, "a": {"type": "number", "minimum": 0}}, "required": ["r", "g", "b", "a"]}
```

`ColorMessage` was created with `add_struct_variable` and `struct_type`
`/Script/CoreUObject.LinearColor`, as the command suggested. `ColorIdle`'s own default reads
`{"r":1,"g":1,"b":1,"a":1}` and was not touched.

**Not verified:** which tool originally created `ColorIdle` cannot be read back — only the
resulting type can. The claim above is that the two variables have identical resulting types,
not that they were declared by the same call.

### Instance Editable — calls made, not read back

There is no `get_variable_instance_editable` on this build, so **no claim is made here that any
flag was verified.** What follows is only which calls were made and whether each raised.

| variable | `instance_editable` passed | raised? | returned |
|---|---|---|---|
| `MessageText` | `false` | no | `{'returnValue': None}` |
| `MessageExpireTime` | `false` | no | `{'returnValue': None}` |
| `ColorMessage` | `true` | no | `{'returnValue': None}` |
| `MessageMargin` | `true` | no | `{'returnValue': None}` |
| `MessageDuration` | `true` | no | `{'returnValue': None}` |

All five `set_variable_instance_editable` calls completed without raising. Whether the flags
actually took cannot be confirmed by any tool on this build. `MessageText` and
`MessageExpireTime` were explicitly set to `false` rather than left at whatever
`add_variable`'s default is, so an explicit write was attempted in the OFF direction for both
runtime-state variables.

---

## 4. ShowMessage — complete node inventory

Graph: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD:ShowMessage`

Created with `add_function_graph`; the `Message` input added with `add_function_param`
(`param_type` `string`, `input_param` true). Immediately after that the graph read
`(fn ShowMessage (Message))` — entry only, no outputs. The body was then written with
`write_graph_dsl`.

Read back with `read_graph_dsl`:

```
(fn ShowMessage (Message)
  (Variables|Default|SetMessageText Message)
  (Variables|Default|SetMessageExpireTime (+ (Utilities|Time|GetTimeSeconds) (Variables|Default|GetMessageDuration))))
```

### Every node — refPath and type_id

`find_nodes` on the graph returned **6** nodes.

| # | refPath | type_id |
|---|---|---|
| 1 | `...:ShowMessage.K2Node_FunctionEntry_0` | `\|ShowMessage` |
| 2 | `...:ShowMessage.K2Node_VariableSet_0` | `\|SetMessageText` |
| 3 | `...:ShowMessage.K2Node_CallFunction_0` | `Utilities\|Time\|GetTimeSeconds` |
| 4 | `...:ShowMessage.K2Node_VariableGet_0` | `\|GetMessageDuration` |
| 5 | `...:ShowMessage.K2Node_PromotableOperator_0` | `Math\|Float\|float+float` |
| 6 | `...:ShowMessage.K2Node_VariableSet_1` | `\|SetMessageExpireTime` |

(`...` = `/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD`)

### Connections, read back

```
K2Node_FunctionEntry_0
  then    -> K2Node_VariableSet_0 [in 0]
  Message -> K2Node_VariableSet_0 [in 1]   (String)

K2Node_VariableSet_0  (Set MessageText)
  execute     <- K2Node_FunctionEntry_0 [out 0]
  MessageText <- K2Node_FunctionEntry_0 [out 1]
  then        -> K2Node_VariableSet_1 [in 0]
  Output_Get  -> (nothing)

K2Node_CallFunction_0  (GetTimeSeconds)
  input pins  : (none)
  ReturnValue -> K2Node_PromotableOperator_0 [in 0]   (Float, double-precision)

K2Node_VariableGet_0  (Get MessageDuration)
  MessageDuration -> K2Node_PromotableOperator_0 [in 1]

K2Node_PromotableOperator_0  (Add)
  A           <- K2Node_CallFunction_0 [out 0]
  B           <- K2Node_VariableGet_0 [out 0]
  ReturnValue -> K2Node_VariableSet_1 [in 1]

K2Node_VariableSet_1  (Set MessageExpireTime)
  execute           <- K2Node_VariableSet_0 [out 0]
  MessageExpireTime <- K2Node_PromotableOperator_0 [out 0]
  then       -> (nothing)
  Output_Get -> (nothing)
```

Exec chain: entry -> Set MessageText -> Set MessageExpireTime -> end. **No Branch, Timer, Delay,
Print String or Timeline** — the six nodes above are the whole graph.

`GetTimeSeconds` reads back with **no input pins at all**, so its `WorldContextObject` pin is
hidden as the command said. It was not touched.

### Nodes beyond the ones step 2 named

Step 2 named five things: the entry, `Set MessageText`, `Set MessageExpireTime`, the Add, and
`GetTimeSeconds`. The graph has six.

| extra node | which tool created it | why |
|---|---|---|
| `K2Node_VariableGet_0` — `\|GetMessageDuration` | `write_graph_dsl`, from the `(Variables|Default|GetMessageDuration)` term in the script I passed | `MessageDuration` appears as a term of the Add in step 2's body, and reading a Blueprint member variable requires a getter node. Nothing else can supply that pin. |

No other node was emitted. This is notably cleaner than the DSL's behaviour in the previous
command, where `write_graph_dsl` expanded a similar expression into nine helper nodes
(`MakeLiteralFloat`, `BreakVector`, `Select`); here the expression had no literals or struct
accessors to expand.

### One read-back difference from the requested type_id

The Add node was written as `Utilities|Operators|Add`, the type_id the command specified, and
**reads back as `Math|Float|float+float`**. That is the wildcard promotable resolving to its
float overload once both inputs are connected to double pins — the same pattern seen in
commands 24, 25 and 27, where `Utilities|Operators|Subtract` read back as `Math|Integer|int-int`
and `Utilities|Operators|Add` as `Math|Vector|vector+vector`. Nothing went wrong.

---

## 5. EventGraph was not modified

`find_nodes` on `BP_ThirdPersonHUD:EventGraph` with an empty title:

- **Before:** 107
- **After:** 107

**Unchanged.** No tool call in this command targeted the EventGraph — the variables were added
at Blueprint level and the DSL write targeted the `ShowMessage` graph only.

**Not verified:** the count matching does not by itself prove no node inside the EventGraph
changed a pin value; it proves nothing was added or removed. No call in this command addressed
that graph or any node in it.

---

## 6. Compile result

`BlueprintTools.compile_blueprint` on BP_ThirdPersonHUD, `warnings_as_errors` = `false`,
returned:

```
{"returnValue":null}
```

The tool raises on error; it did not raise. Three compiles of this Blueprint happened during the
command — one after the variables were added (so the CDO would carry them before defaults were
written), one performed internally by `write_graph_dsl`, and the explicit final one:

```
[2026.08.30-04.12.15:439][758]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD'
[2026.08.30-04.13.00:723][891]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD'
[2026.08.30-04.13.23:425][958]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD'
```

No error and no warning followed any of the three. **Compiled clean.**

`AssetTools.save_assets` -> `true`. The save triggered the editor's content validation pass,
which logged `AssetCheck: /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD Validating asset` and
nine validator counts, reporting no failure.

**Not verified:** no tool reports a Blueprint's compiled status flag directly. "Compiled clean"
rests on the calls not raising plus an empty log window, as in every previous command.

---

## 7. Errors and warnings — exact English text

### 7.1 From this work

**None.** Every call in this command — `list_variables`, `list_functions`, `list_graphs`,
`find_nodes`, `get_properties`, `list_properties`, `add_variable` (x4),
`add_struct_variable`, `set_properties`, `set_variable_instance_editable` (x5),
`add_function_graph`, `add_function_param`, `find_node_types`, `read_graph_dsl`,
`write_graph_dsl`, `get_node_infos`, `compile_blueprint` and `save_assets` — completed without
raising and wrote nothing to the log beyond routine dispatch lines.

There is no error or warning text to quote for this command.

### 7.2 Present in the log but NOT from this work

Nothing new. The `LogBlueprint` warning block from `00.36.49` — which names only pre-existing
nodes in BP_ThirdPersonCharacter, not this HUD — remains the newest set of Blueprint warnings,
now over three hours old. It was already recorded in the reports for commands 24, 25, 27, 28
and 29.

---

## 8. git status after the work

```
 M Content/Interaction/BP_Door.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonHUD.uasset
```

`BP_ThirdPersonHUD.uasset` is the file this command changed.

`Content/Interaction/BP_Door.uasset` is **not** from this command. It was untracked at the end
of the previous command and is now tracked-and-modified, so the door assets were committed in
between and BP_Door has since been changed. The log shows a compile of it that this session did
not perform:

```
[2026.08.30-04.00.29:368][634]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Door.BP_Door'
```

Recorded as an observation only; not investigated, and BP_Door was not touched by this command.

---

## 9. What is not verified

- **The Instance Editable flag on all five new variables.** No getter exists on this build.
  Section 3. The two runtime-state variables in particular — `MessageText` and
  `MessageExpireTime` — were asked to stay OFF, and that cannot be confirmed here.
- **That `ColorIdle` and `ColorMessage` were declared by the same tool.** Only that their
  resulting types are identical. Section 3.
- **That ShowMessage behaves correctly at runtime.** Nothing was run. The graph compiles and its
  wiring reads correctly, but no message has been shown — the drawing block that would make it
  visible is the next command.
- **Whether `GetTimeSeconds` resolves its hidden WorldContextObject correctly from a HUD.** The
  pin is hidden and was left alone as instructed; it compiles, but this was not exercised.
