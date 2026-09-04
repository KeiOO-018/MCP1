# 2026-09-04-60 · M_Flame FlameBrightness 30 -> 5

One value changed, recompiled, saved, verified. FlameColor, the Multiply node, every material
setting, and the graph wiring were left alone, and the read-back confirms all of them are
unchanged. No material instance was created.

**The one thing that did not happen as the task expected: no shader compilation appeared in the
log at all.** Details in section 2 — that is a real observation, not a missed check.

---

## 0 · Before the write

```
call: EditorToolset.EditorAppToolset.IsPIERunning
args: {}
```

```
{"returnValue":false}
```

Log marker taken so the recompile window could be isolated afterwards:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "LogModelContextProtocol", "pattern": "", "maxEntries": 2}
```

```
{"returnValue":["[2026.09.04-02.11.04:192][754]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-02.11.04:192][754]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.EditorAppToolset.IsPIERunning'"]}
```

The log stamps UTC; KST is +9, so 02:11 in the log is 11:11 on the shell clock.

---

## 1 · The write

```
call: editor_toolset.toolsets.object.ObjectTools.set_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionScalarParameter_0"}, "values": "{\"DefaultValue\": 5}"}
```

```
{"returnValue":true}
```

That is the only `set_properties` call in this task. `MaterialExpressionVectorParameter_0`
(FlameColor) and `MaterialExpressionMultiply_0` received no write, and no material setting on
`M_Flame` itself was written.

---

## 2 · Recompile, and how long it took

Shell clock either side of the call:

```
$ date '+%Y-%m-%d %H:%M:%S.%N %z'
2026-09-04 11:11:15.058765000 +0900
```

```
call: editor_toolset.toolsets.material.MaterialTools.recompile
args: {"material_or_function": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame"}}
```

```
{"returnValue":null}
```

```
$ date '+%Y-%m-%d %H:%M:%S.%N %z'
2026-09-04 11:11:20.995411300 +0900
```

Wall clock across the call: **5.94 s**. That figure is almost entirely MCP round-trip overhead —
every tool call in this session takes 4–5 s of transport — so it is not the compile time.

The editor-side timing, from the log:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "02\\.1[1-9]\\.", "maxEntries": 60}
```

```
{"returnValue":["[2026.09.04-02.11.04:192][754]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-02.11.04:192][754]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.EditorAppToolset.IsPIERunning'","[2026.09.04-02.11.08:192][766]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-02.11.08:193][766]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.LogsToolset.GetLogEntries'","[2026.09.04-02.11.13:195][781]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-02.11.13:196][781]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.object.ObjectTools.set_properties'","[2026.09.04-02.11.18:858][798]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-02.11.18:858][798]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.material.MaterialTools.recompile'","[2026.09.04-02.11.18:916][798]LogUObjectHash: Compacting FUObjectHashTables data took   0.68ms","[2026.09.04-02.11.19:085][798]LogUObjectHash: Compacting FUObjectHashTables data took   0.24ms","[2026.09.04-02.11.23:238][811]LogUObjectHash: Compacting FUObjectHashTables data took   0.23ms","[2026.09.04-02.11.23:239][811]LogFileHelpers: Editor autosave (incl. external actors) for '/Game/ThirdPerson/Lvl_Stage' took 0.025","[2026.09.04-02.11.23:239][811]OBJ SavePackage: Generating thumbnails for [1] asset(s) in package [/Game/LevelPrototyping/Materials/M_Flame] ([1] browsable assets)...","[2026.09.04-02.11.23:339][811]OBJ SavePackage:     Rendered thumbnail for [Material /Game/LevelPrototyping/Materials/M_Flame.M_Flame]","[2026.09.04-02.11.23:339][811]OBJ SavePackage: Finished generating thumbnails for package [/Game/LevelPrototyping/Materials/M_Flame]","[2026.09.04-02.11.23:339][811]Cmd: OBJ SAVEPACKAGE PACKAGE=\"/Game/LevelPrototyping/Materials/M_Flame\" FILE=\"D:/20260827/MCP1/Saved/Autosaves/Game/LevelPrototyping/Materials/M_Flame_Auto2.uasset\" SILENT=false AUTOSAVING=true","[2026.09.04-02.11.23:347][811]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/LevelPrototyping/Materials/M_Flame_Auto2","[2026.09.04-02.11.23:347][811]LogSavePackage: Moving 'D:/20260827/MCP1/Saved/M_Flame_Auto221A3ACAD4B134322C0B76292D8267EA5.tmp' to 'D:/20260827/MCP1/Saved/Autosaves/Game/LevelPrototyping/Materials/M_Flame_Auto2.uasset'","[2026.09.04-02.11.23:347][811]LogFileHelpers: Auto-saving content packages took 0.108","[2026.09.04-02.11.26:192][820]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-02.11.26:192][820]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.LogsToolset.GetLogEntries'"]}
```

The recompile dispatched at `02:11:18.858` and the editor logged nothing after
`02:11:19.085` until an unrelated autosave woke up 4 s later. **Editor-side the recompile took
about 0.23 s**, and the only work it logged was two `FUObjectHashTables` compactions of 0.68 ms
and 0.24 ms.

### No shader compilation, no errors, no warnings

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "(?i)shader|LogMaterial|compil.*error|error.*compil|warning.*material", "maxEntries": 25}
```

The response contains **no `LogShaderCompilers` entry from the 02:11 window at all**. Every
`LogShaderCompilers` line it returns is from engine startup at `01:10:13`–`01:10:16`
("Using 12 local workers for shader compilation", "Autogen file is unchanged, skipping write",
and similar). The newest line in that response is unrelated:

```
[2026.09.04-02.02.33:879][961]LogScript: Warning: GetObjectProperties on '/Game/LevelPrototyping/Materials/M_Flame.M_Flame' (Material): the following properties could not be read: bUsedAsSpecialEngineMaterial
```

— that is the failed property read from task 59, not from this task.

**So: zero shader compile errors and zero shader compile warnings, because no shader compile job
ran.** The task's premise was that "the shader has to be rebuilt for the change to reach the
screen". On the evidence here it did not need to be. A ScalarParameter's `DefaultValue` is a
uniform fed to an already-compiled shader, not something baked into the shader code, so changing
it leaves the shader map valid and nothing recompiles. The `recompile` call was still made as
instructed and it returned without error; it simply had no shader work to do.

That is a reading of why the log is empty, not a separate measurement. What is measured is only
this: no shader compiler activity was logged, and no error or warning appeared.

### One incidental finding

```
[2026.09.04-02.11.23:239][811]LogFileHelpers: Editor autosave (incl. external actors) for '/Game/ThirdPerson/Lvl_Stage' took 0.025
```

An autosave fired at 02:11:23 and named **no** `__ExternalActors__` packages for Lvl_Stage — it
only wrote `M_Flame_Auto2`, which was dirty from the write above. This closes the open question
left in log 2026-09-04-58 section STEP 4: the level's external actor packages really are clean
after the reload. The autosave witness has now reported, and it found nothing there.

---

## 3 · Save

```
call: editor_toolset.toolsets.asset.AssetTools.save_assets
args: {"asset_paths": ["/Game/LevelPrototyping/Materials/M_Flame"]}
```

```
{"returnValue":true}
```

The matching log lines, showing the write went to `Content/` and not to `Saved/`:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "M_Flame", "maxEntries": 14}
```

```
[2026.09.04-02.11.41:573][866]LogFileHelpers: Saving Package: /Game/LevelPrototyping/Materials/M_Flame
[2026.09.04-02.11.41:573][866]OBJ SavePackage: Generating thumbnails for [0] asset(s) in package [/Game/LevelPrototyping/Materials/M_Flame] ([1] browsable assets)...
[2026.09.04-02.11.41:573][866]OBJ SavePackage: Finished generating thumbnails for package [/Game/LevelPrototyping/Materials/M_Flame]
[2026.09.04-02.11.41:573][866]Cmd: OBJ SAVEPACKAGE PACKAGE="/Game/LevelPrototyping/Materials/M_Flame" FILE="D:/20260827/MCP1/Content/LevelPrototyping/Materials/M_Flame.uasset" SILENT=true
[2026.09.04-02.11.41:581][866]LogSavePackage: Moving output files for package: /Game/LevelPrototyping/Materials/M_Flame
[2026.09.04-02.11.41:581][866]LogSavePackage: Moving 'D:/20260827/MCP1/Saved/M_Flame3F7F534F4B79D4407ABD9DA54D2A7D27.tmp' to 'D:/20260827/MCP1/Content/LevelPrototyping/Materials/M_Flame.uasset'
[2026.09.04-02.11.41:884][867]AssetCheck: /Game/LevelPrototyping/Materials/M_Flame Validating asset
```

---

## 4 · Read-back 1 — FlameBrightness

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionScalarParameter_0"}, "properties": ["ParameterName", "DefaultValue"]}
```

```
{"returnValue":"{\"ParameterName\":\"FlameBrightness\",\"DefaultValue\":5}"}
```

**`DefaultValue` is 5.** The write landed. It was 30 before (log 2026-09-04-59 section 2).

---

## 5 · Read-back 2 — FlameColor undisturbed

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionVectorParameter_0"}, "properties": ["ParameterName", "DefaultValue"]}
```

```
{"returnValue":"{\"ParameterName\":\"FlameColor\",\"DefaultValue\":{\"r\":1,\"g\":0.44999998807907104,\"b\":0.11999999731779099,\"a\":1}}"}
```

| Channel | Expected | Read back |
| --- | --- | --- |
| r | 1 | 1 |
| g | 0.44999998807907104 | 0.44999998807907104 |
| b | 0.11999999731779099 | 0.11999999731779099 |
| a | 1 | 1 |

Exact match, to the last digit. **FlameColor was not disturbed.**

---

## 6 · Read-back 3 — graph not rewired

```
call: editor_toolset.toolsets.material.MaterialTools.get_property_input
args: {"material": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame"}, "material_property": "MP_EmissiveColor"}
```

```
{"returnValue":{"output_name":"","expression":{"refPath":"/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionMultiply_0"},"input_name":""}}
```

**MP_EmissiveColor is still driven by `MaterialExpressionMultiply_0`.**

The Multiply's own inputs were re-read as well, since "not rewired" should mean the whole path,
not just the last hop:

```
call: editor_toolset.toolsets.material.MaterialTools.get_expression_inputs
args: {"material_or_function": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame"}, "expression": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionMultiply_0"}}
```

```
{"returnValue":[{"output_name":"RGB","expression":{"refPath":"/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionVectorParameter_0"},"input_name":"A"},{"output_name":"","expression":{"refPath":"/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionScalarParameter_0"},"input_name":"B"}]}
```

Byte-for-byte the same response as in log 2026-09-04-59: `FlameColor.RGB -> A`,
`FlameBrightness -> B`. The graph is untouched.

---

## 7 · Read-back 4 — dirty flag and disk

```
call: editor_toolset.toolsets.asset.AssetTools.is_dirty
args: {"asset_path": "/Game/LevelPrototyping/Materials/M_Flame"}
```

```
{"returnValue":false}
```

```
$ ls -l --time-style=full-iso Content/LevelPrototyping/Materials/M_Flame.uasset
-rw-r--r-- 1 a0108 197609 10860 2026-09-04 11:11:41.581058100 +0900 Content/LevelPrototyping/Materials/M_Flame.uasset

$ date '+now: %Y-%m-%d %H:%M:%S.%N %z'
now: 2026-09-04 11:12:06.147661800 +0900
```

| | Value |
| --- | --- |
| mtime | 2026-09-04 11:11:41.581058100 +0900 |
| now | 2026-09-04 11:12:06.147661800 +0900 |
| difference | **24.57 s** |

The file was rewritten 24.57 seconds before the clock was read, and the mtime matches the
`LogSavePackage: Moving ...` line at `02:11:41.581` to the millisecond. **The save reached disk;
it did not merely clear a flag.**

---

## 8 · Read-back 5 — git status

```
$ git status --short
 M Content/Interaction/BP_Torch.uasset
 M Content/LevelPrototyping/Materials/M_Flame.uasset
?? "Docs/Spec/2026-09-04-<Korean filename, shown as octal escapes by git>.md"
?? Docs/Terminal-Log/2026-09-04-56-torch-cast-shadow-off.md
?? Docs/Terminal-Log/2026-09-04-57-torch-shadow-after-reload.md
?? Docs/Terminal-Log/2026-09-04-58-torch-shadow-reload-readback.md
?? Docs/Terminal-Log/2026-09-04-59-flame-material-readout.md
```

`M_Flame.uasset` is newly modified — this task. `BP_Torch.uasset` was already modified from task
56. Nothing under `Content/__ExternalActors__` and no level package changed, which is right for a
task that touched only a material.

---

## 9 · What is still unverified

The screen. Nothing in this task rendered or measured a pixel, so whether the flame now shows its
orange instead of a white blob is **not confirmed here**. The emissive the material outputs is now
`(1, 0.45, 0.12) * 5 = (5, 2.25, 0.6)` instead of `(30, 13.5, 3.6)` — still above 1.0 and still
bloom-worthy, which is what an emissive flame wants, but far enough down that the channels should
no longer converge to white under the tonemapper. Confirming that needs a viewport capture or a
look with human eyes.
