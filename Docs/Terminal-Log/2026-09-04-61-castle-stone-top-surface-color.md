# 2026-09-04-61 · MI_Castle_Stone static switch TopSurfaceColor false -> true

One static switch changed, saved, verified. Every other parameter on the instance was read before
and after and is unchanged. The parent material `M_PrototypeGrid` was not touched.

**The one place the task's expectation did not hold: no shader compilation appeared in the log, so
"how many shaders were compiled" cannot be answered from the log — it records none.** That is
covered in section 3 and is a real observation, not a check I skipped.

---

## 0 · PIE state — read this one carefully

```
call: EditorToolset.EditorAppToolset.IsPIERunning
args: {}
```

```
{"returnValue":false}
```

**No PIE session is running now.** But the log shows one was torn down eight seconds before that
check, so this is worth stating rather than just answering "no":

```
[2026.09.04-02.17.34:591][735]LogWorld: BeginTearingDown for /Game/ThirdPerson/UEDPIE_0_Lvl_Stage
[2026.09.04-02.17.34:591][735]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
[2026.09.04-02.17.34:592][735]LogWorld: UWorld::CleanupWorld for Lvl_Stage, bSessionEnded=true, bCleanupResources=true
[2026.09.04-02.17.34:594][735]LogWorldPartition: UWorldPartition::Uninitialize : World = /Game/ThirdPerson/UEDPIE_0_Lvl_Stage.Lvl_Stage
[2026.09.04-02.17.34:596][735]LogPlayLevel: Display: Shutting down PIE online subsystems
[2026.09.04-02.17.34:737][736]LogPlayLevel: Display: Destroying online subsystem :Context_5
```

`IsPIERunning` was called at `02:17:42.599` — **8.0 seconds after PIE shut down.** Every call in
this task therefore hit the editor world, and no `refPath` below carries a `UEDPIE_0_` prefix. Had
this task started a few seconds earlier the writes would have gone somewhere else.

---

## 1 · Finding the parameter, and a name collision worth knowing about

```
call: editor_toolset.toolsets.material_instance.MaterialInstanceTools.list_parameters
args: {"material": {"refPath": "/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}}
```

```
{"returnValue":[{"type":"Scalar","name":"Roughness"},{"type":"Scalar","name":"Grid Size"},{"type":"Scalar","name":"Sub Grid Number"},{"type":"Scalar","name":"CircleSize"},{"type":"Vector","name":"SurfaceColor"},{"type":"Vector","name":"TopGridColor"},{"type":"Vector","name":"GridColor"},{"type":"Vector","name":"TopSurfaceColor"},{"type":"Vector","name":"TopSubGridGridColor"},{"type":"Vector","name":"SubGridColor"},{"type":"Vector","name":"Line Dimensions"},{"type":"StaticSwitch","name":"TopSurfaceColor"},{"type":"StaticSwitch","name":"ObjectAligned"},{"type":"StaticSwitch","name":"Grid"}]}
```

**`TopSurfaceColor` exists twice: once as a `Vector` and once as a `StaticSwitch`.** They are
different parameters that happen to share a name — the switch turns the feature on, the vector
holds the colour it uses. A tool call that addressed the parameter by name alone without a type
would be ambiguous here. `set_static_switch_parameter` is type-specific, so it targets the switch;
the read-back in section 5 confirms the vector of the same name did not move.

---

## 2 · State before the write

Raw override arrays on the instance:

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}, "properties": ["Parent", "ScalarParameterValues", "VectorParameterValues", "TextureParameterValues", "StaticParameters", "StaticParametersRuntime"]}
```

```
GetObjectProperties on '/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone' (MaterialInstanceConstant): the following properties could not be read: StaticParameters, StaticParametersRuntime
```

Neither static-parameter container is reachable through `ObjectTools`, so the static switch values
in this report all come from `MaterialInstanceTools.get_static_switch_parameter`. Re-sent without
them:

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}, "properties": ["Parent", "ScalarParameterValues", "VectorParameterValues", "TextureParameterValues"]}
```

```
{"returnValue":"{\"Parent\":{\"refPath\":\"/Game/LevelPrototyping/Materials/M_PrototypeGrid.M_PrototypeGrid\"},\"ScalarParameterValues\":[{\"atlasData\":{\"bIsUsedAsAtlasPosition\":false,\"curve\":\"None\",\"atlas\":\"None\"},\"parameterInfo\":{\"name\":\"Grid Size\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":200,\"expressionGUId\":\"24F0A099-4A5F-B333-0BF3-8D8355E1A214\"},{\"atlasData\":{\"bIsUsedAsAtlasPosition\":false,\"curve\":\"None\",\"atlas\":\"None\"},\"parameterInfo\":{\"name\":\"Roughness\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":1,\"expressionGUId\":\"5258442B-443D-60A7-B6C2-A48F588D02BB\"}],\"VectorParameterValues\":[{\"parameterInfo\":{\"name\":\"SurfaceColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.13500000536441803,\"g\":0.125,\"b\":0.1120000034570694,\"a\":1},\"expressionGUId\":\"00ABBD3F-48B1-4CCB-49E1-2995BAFE00FB\"},{\"parameterInfo\":{\"name\":\"GridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.045000001788139343,\"g\":0.041999999433755875,\"b\":0.037999998778104782,\"a\":1},\"expressionGUId\":\"D5FCC737-4FCC-A3EE-9646-B1A8BD94555C\"},{\"parameterInfo\":{\"name\":\"SubGridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.090000003576278687,\"g\":0.085000000894069672,\"b\":0.078000001609325409,\"a\":1},\"expressionGUId\":\"F04EB7DA-459B-AE57-E5D6-2080C7B9FCEC\"},{\"parameterInfo\":{\"name\":\"TopSurfaceColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.11500000208616257,\"g\":0.10999999940395355,\"b\":0.10199999809265137,\"a\":1},\"expressionGUId\":\"E7116BE2-4576-3AC8-F6F7-3BA5CA8D3091\"},{\"parameterInfo\":{\"name\":\"TopGridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.039999999105930328,\"g\":0.037999998778104782,\"b\":0.035000000149011612,\"a\":1},\"expressionGUId\":\"0DD4B258-4314-E25F-674D-65A5EF75B58C\"},{\"parameterInfo\":{\"name\":\"TopSubGridGridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.079999998211860657,\"g\":0.075999997556209564,\"b\":0.070000000298023224,\"a\":1},\"expressionGUId\":\"AF4DD804-46F6-AA38-1400-A3A3F0F202E1\"}],\"TextureParameterValues\":[]}"}
```

Effective values of all fourteen parameters:

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: get_static_switch_parameter / get_scalar_parameter / get_vector_parameter for every parameter
```

```
{"static_switches_effective": {"TopSurfaceColor": false, "ObjectAligned": false, "Grid": true}, "scalars_effective": {"Roughness": 1, "Grid Size": 200, "Sub Grid Number": 5, "CircleSize": 100}, "vectors_effective": {"SurfaceColor": {"r": 0.13500000536441803, "g": 0.125, "b": 0.1120000034570694, "a": 1}, "TopGridColor": {"r": 0.03999999910593033, "g": 0.03799999877810478, "b": 0.03500000014901161, "a": 1}, "GridColor": {"r": 0.04500000178813934, "g": 0.041999999433755875, "b": 0.03799999877810478, "a": 1}, "TopSurfaceColor": {"r": 0.11500000208616257, "g": 0.10999999940395355, "b": 0.10199999809265137, "a": 1}, "TopSubGridGridColor": {"r": 0.07999999821186066, "g": 0.07599999755620956, "b": 0.07000000029802322, "a": 1}, "SubGridColor": {"r": 0.09000000357627869, "g": 0.08500000089406967, "b": 0.07800000160932541, "a": 1}, "Line Dimensions": {"r": 0.021838000044226646, "g": 0.0013470000121742487, "b": 0.5, "a": 0}}, "static_props_on_object": []}
```

(The script also filtered `list_properties` for any property name containing "tatic" and got
`[]` — confirming there is no static-parameter container exposed on the object at all.)

`TopSurfaceColor` static switch was **false** before the write.

---

## 3 · The write, and the shader rebuild that did not appear

Shader compiler log immediately before the write, for a baseline:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "LogShaderCompilers", "pattern": "", "maxEntries": 4}
```

```
{"returnValue":["[2026.09.04-01.10.13:480][  0]LogShaderCompilers: Display: Compiling shader autogen file: D:/20260827/MCP1/Intermediate/ShaderAutogen/PCD3D_SM6/AutogenShaderHeaders.ush","[2026.09.04-01.10.13:496][  0]LogShaderCompilers: Display: Autogen file is unchanged, skipping write.","[2026.09.04-01.10.16:022][  0]LogShaderCompilers: Display: Compiling shader autogen file: D:/20260827/MCP1/Intermediate/ShaderAutogen/PCD3D_SM5/AutogenShaderHeaders.ush","[2026.09.04-01.10.16:039][  0]LogShaderCompilers: Display: Autogen file is unchanged, skipping write."]}
```

Shell clock either side of the write:

```
$ date '+%Y-%m-%d %H:%M:%S.%N %z'
2026-09-04 11:18:30.699093200 +0900
```

```
call: editor_toolset.toolsets.material_instance.MaterialInstanceTools.set_static_switch_parameter
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}, "name": "TopSurfaceColor", "value": true}
```

```
{"returnValue":null}
```

```
$ date '+%Y-%m-%d %H:%M:%S.%N %z'
2026-09-04 11:18:39.211555500 +0900
```

Wall clock across the call: **8.51 s**, most of which is MCP transport (every call this session
costs 4–5 s of it).

The editor-side window:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "02\\.1[6-9]\\.|02\\.2[0-9]\\.", "maxEntries": 60}
```

The relevant lines from that response:

```
[2026.09.04-02.18.35:264][ 98]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.material_instance.MaterialInstanceTools.set_static_switch_parameter'
[2026.09.04-02.18.35:380][ 98]LogUObjectHash: Compacting FUObjectHashTables data took   0.52ms
[2026.09.04-02.18.37:346][ 98]LogUObjectHash: Compacting FUObjectHashTables data took   0.26ms
[2026.09.04-02.18.43:366][117]LogModelContextProtocol: Running tool: 'call_tool'
```

**Editor-side the write took about 2.08 s** (`02:18:35.264` to the last work at `02:18:37.346`).
For comparison, the scalar-parameter change in log 2026-09-04-60 took about 0.23 s editor-side, so
this did roughly nine times the work — the static switch really is a heavier operation.

### How many shaders were compiled: the log says none

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "LogShaderCompilers", "pattern": "", "maxEntries": 30}
```

```
{"returnValue":["[2026.09.04-01.10.13:472][  0]LogShaderCompilers: Guid format shader working directory is 29 characters bigger than the processId version (D:/20260827/MCP1/Intermediate/Shaders/WorkingDirectory/22840/).","[2026.09.04-01.10.13:472][  0]LogShaderCompilers: Cleaned the shader compiler working directory 'C:/Users/a0108/AppData/Local/Temp/UnrealShaderWorkingDir/8AE5881A40DC07AC91F98289DBBB8AF2/'.","[2026.09.04-01.10.13:473][  0]LogShaderCompilers: Display: No distributed shader compiler controller found","[2026.09.04-01.10.13:473][  0]LogShaderCompilers: Display: Using 12 local workers for shader compilation","[2026.09.04-01.10.13:480][  0]LogShaderCompilers: Display: Compiling shader autogen file: D:/20260827/MCP1/Intermediate/ShaderAutogen/PCD3D_SM6/AutogenShaderHeaders.ush","[2026.09.04-01.10.13:496][  0]LogShaderCompilers: Display: Autogen file is unchanged, skipping write.","[2026.09.04-01.10.16:022][  0]LogShaderCompilers: Display: Compiling shader autogen file: D:/20260827/MCP1/Intermediate/ShaderAutogen/PCD3D_SM5/AutogenShaderHeaders.ush","[2026.09.04-01.10.16:039][  0]LogShaderCompilers: Display: Autogen file is unchanged, skipping write."]}
```

**Identical to the baseline taken before the write — eight entries, all from engine startup at
`01:10:13`–`01:10:16`. Not one new line.** The category is not muted:

```
call: EditorToolset.LogsToolset.GetVerbosity
args: {"category": "LogShaderCompilers"}
```

```
{"returnValue":"Log"}
```

`Log` verbosity would show `Display` messages, so submitted-jobs and compile-finished lines would
have appeared if there were any. A broader sweep found nothing either:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "(?i)shader|material|derived ?data|DDC", "maxEntries": 12}
```

```
{"returnValue":["[2026.09.04-02.11.41:581][866]LogSavePackage: Moving output files for package: /Game/LevelPrototyping/Materials/M_Flame","[2026.09.04-02.11.41:581][866]LogSavePackage: Moving 'D:/20260827/MCP1/Saved/M_Flame3F7F534F4B79D4407ABD9DA54D2A7D27.tmp' to 'D:/20260827/MCP1/Content/LevelPrototyping/Materials/M_Flame.uasset'","[2026.09.04-02.11.41:884][867]LogContentValidation: \t/Script/DataValidation.EditorValidator_Material","[2026.09.04-02.11.41:884][867]AssetCheck: /Game/LevelPrototyping/Materials/M_Flame Validating asset","[2026.09.04-02.11.41:884][867]LogContentValidation:   /Script/DataValidation.EditorValidator_Material : 0","[2026.09.04-02.11.54:526][905]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.material.MaterialTools.get_property_input'","[2026.09.04-02.11.59:193][919]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.material.MaterialTools.get_expression_inputs'","[2026.09.04-02.12.44:567][ 56]LogDerivedDataCache: C:/Users/a0108/AppData/Local/UnrealEngine/Common/DerivedDataCache: Maintenance finished in +00:00:31.093 and deleted 0 files with total size 0 MiB and 0 empty folders. Scanned 16343 files in 16457 folders with total size 331 MiB.","\t\tNumShaderSlotsPerGeometrySegment changed: current: 1 - new: 2","[2026.09.04-02.17.51:932][968]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.material_instance.MaterialInstanceTools.list_parameters'","[2026.09.04-02.18.00:601][994]LogScript: Warning: GetObjectProperties on '/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone' (MaterialInstanceConstant): the following properties could not be read: StaticParameters, StaticParametersRuntime","[2026.09.04-02.18.35:264][ 98]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.material_instance.MaterialInstanceTools.set_static_switch_parameter'"]}
```

Nothing shader-related in the 02:18 window.

### Answers to the three questions asked about the rebuild

| Question | Answer |
| --- | --- |
| How long did the rebuild take? | 8.51 s wall clock; **~2.08 s editor-side**, vs ~0.23 s for the scalar change in log 60 |
| How many shaders were compiled? | **Cannot be answered — the log records no shader compile jobs at all.** Not zero-because-I-did-not-look; zero lines exist |
| Every shader compile error or warning | **There are none to quote.** No `LogShaderCompilers` line was emitted during this task, so there is nothing to reproduce verbatim |

The task's premise — "a static switch is baked into the shader ... so this one really does force a
shader rebuild" — is right about the mechanism. What it does not account for is the Derived Data
Cache. A new static-switch permutation needs a different shader map, but if that permutation has
been compiled before on this machine it comes back from the DDC instead of being compiled again,
and a DDC hit produces no `LogShaderCompilers` output. The DDC here holds 16343 files
(`LogDerivedDataCache` line above), and `TopSurfaceColor = true` is the stock configuration of the
engine's own `M_PrototypeGrid`, so a cached shader map for it is very likely to exist.

**That explanation is inference, not measurement.** What is measured is only this: 2.08 s of
editor-side work, zero shader compile log lines, zero errors, zero warnings. Proving the DDC
theory would mean clearing the DDC and repeating, which is slow and destructive to other work, and
was not done.

---

## 4 · Save

```
call: editor_toolset.toolsets.asset.AssetTools.save_assets
args: {"asset_paths": ["/Game/LevelPrototyping/Materials/MI_Castle_Stone"]}
```

```
{"returnValue":true}
```

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "MI_Castle_Stone", "maxEntries": 12}
```

```
[2026.09.04-02.19.11:754][202]LogFileHelpers: Saving Package: /Game/LevelPrototyping/Materials/MI_Castle_Stone
[2026.09.04-02.19.11:754][202]OBJ SavePackage: Generating thumbnails for [1] asset(s) in package [/Game/LevelPrototyping/Materials/MI_Castle_Stone] ([1] browsable assets)...
[2026.09.04-02.19.11:972][202]OBJ SavePackage:     Rendered thumbnail for [MaterialInstanceConstant /Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone]
[2026.09.04-02.19.11:972][202]OBJ SavePackage: Finished generating thumbnails for package [/Game/LevelPrototyping/Materials/MI_Castle_Stone]
[2026.09.04-02.19.11:972][202]Cmd: OBJ SAVEPACKAGE PACKAGE="/Game/LevelPrototyping/Materials/MI_Castle_Stone" FILE="D:/20260827/MCP1/Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset" SILENT=true
[2026.09.04-02.19.11:982][202]LogSavePackage: Moving output files for package: /Game/LevelPrototyping/Materials/MI_Castle_Stone
[2026.09.04-02.19.11:982][202]LogSavePackage: Moving 'D:/20260827/MCP1/Saved/MI_Castle_StoneD15764DF4047E185CB82339E3657F261.tmp' to 'D:/20260827/MCP1/Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset'
[2026.09.04-02.19.12:063][203]AssetCheck: /Game/LevelPrototyping/Materials/MI_Castle_Stone Validating asset
```

Destination is `Content/`, not `Saved/`.

---

## 5 · Read-back 1 — TopSurfaceColor static switch

```
call: editor_toolset.toolsets.material_instance.MaterialInstanceTools.get_static_switch_parameter
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}, "name": "TopSurfaceColor"}
```

```
{"returnValue":true}
```

**The write landed: `false` -> `true`.**

---

## 6 · Read-back 2 — everything else

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: same reads as section 2, re-run after the save
```

```
{"static_switches_effective": {"TopSurfaceColor": true, "ObjectAligned": false, "Grid": true}, "scalars_effective": {"Roughness": 1, "Grid Size": 200, "Sub Grid Number": 5, "CircleSize": 100}, "vectors_effective": {"SurfaceColor": {"r": 0.13500000536441803, "g": 0.125, "b": 0.1120000034570694, "a": 1}, "TopGridColor": {"r": 0.03999999910593033, "g": 0.03799999877810478, "b": 0.03500000014901161, "a": 1}, "GridColor": {"r": 0.04500000178813934, "g": 0.041999999433755875, "b": 0.03799999877810478, "a": 1}, "TopSurfaceColor": {"r": 0.11500000208616257, "g": 0.10999999940395355, "b": 0.10199999809265137, "a": 1}, "TopSubGridGridColor": {"r": 0.07999999821186066, "g": 0.07599999755620956, "b": 0.07000000029802322, "a": 1}, "SubGridColor": {"r": 0.09000000357627869, "g": 0.08500000089406967, "b": 0.07800000160932541, "a": 1}, "Line Dimensions": {"r": 0.021838000044226646, "g": 0.0013470000121742487, "b": 0.5, "a": 0}}}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}, "properties": ["Parent", "ScalarParameterValues", "VectorParameterValues", "TextureParameterValues"]}
```

```
{"returnValue":"{\"Parent\":{\"refPath\":\"/Game/LevelPrototyping/Materials/M_PrototypeGrid.M_PrototypeGrid\"},\"ScalarParameterValues\":[{\"atlasData\":{\"bIsUsedAsAtlasPosition\":false,\"curve\":\"None\",\"atlas\":\"None\"},\"parameterInfo\":{\"name\":\"Grid Size\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":200,\"expressionGUId\":\"24F0A099-4A5F-B333-0BF3-8D8355E1A214\"},{\"atlasData\":{\"bIsUsedAsAtlasPosition\":false,\"curve\":\"None\",\"atlas\":\"None\"},\"parameterInfo\":{\"name\":\"Roughness\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":1,\"expressionGUId\":\"5258442B-443D-60A7-B6C2-A48F588D02BB\"}],\"VectorParameterValues\":[{\"parameterInfo\":{\"name\":\"SurfaceColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.13500000536441803,\"g\":0.125,\"b\":0.1120000034570694,\"a\":1},\"expressionGUId\":\"00ABBD3F-48B1-4CCB-49E1-2995BAFE00FB\"},{\"parameterInfo\":{\"name\":\"GridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.045000001788139343,\"g\":0.041999999433755875,\"b\":0.037999998778104782,\"a\":1},\"expressionGUId\":\"D5FCC737-4FCC-A3EE-9646-B1A8BD94555C\"},{\"parameterInfo\":{\"name\":\"SubGridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.090000003576278687,\"g\":0.085000000894069672,\"b\":0.078000001609325409,\"a\":1},\"expressionGUId\":\"F04EB7DA-459B-AE57-E5D6-2080C7B9FCEC\"},{\"parameterInfo\":{\"name\":\"TopSurfaceColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.11500000208616257,\"g\":0.10999999940395355,\"b\":0.10199999809265137,\"a\":1},\"expressionGUId\":\"E7116BE2-4576-3AC8-F6F7-3BA5CA8D3091\"},{\"parameterInfo\":{\"name\":\"TopGridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.039999999105930328,\"g\":0.037999998778104782,\"b\":0.035000000149011612,\"a\":1},\"expressionGUId\":\"0DD4B258-4314-E25F-674D-65A5EF75B58C\"},{\"parameterInfo\":{\"name\":\"TopSubGridGridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.079999998211860657,\"g\":0.075999997556209564,\"b\":0.070000000298023224,\"a\":1},\"expressionGUId\":\"AF4DD804-46F6-AA38-1400-A3A3F0F202E1\"}],\"TextureParameterValues\":[]}"}
```

### Every static switch parameter

| Static switch | Before | After |
| --- | --- | --- |
| **TopSurfaceColor** | false | **true** (this task) |
| ObjectAligned | false | false |
| Grid | true | true |

### Every scalar parameter

| Scalar | Effective value before | Effective value after | Overridden on this instance? |
| --- | --- | --- | --- |
| Roughness | 1 | 1 | yes — `parameterValue: 1`, GUID `5258442B-443D-60A7-B6C2-A48F588D02BB` |
| Grid Size | 200 | 200 | yes — `parameterValue: 200`, GUID `24F0A099-4A5F-B333-0BF3-8D8355E1A214` |
| Sub Grid Number | 5 | 5 | no — inherited from parent |
| CircleSize | 100 | 100 | no — inherited from parent |

### Every vector parameter

| Vector | Effective value before | Effective value after | Overridden on this instance? |
| --- | --- | --- | --- |
| SurfaceColor | r 0.13500000536441803, g 0.125, b 0.1120000034570694, a 1 | identical | yes — GUID `00ABBD3F-48B1-4CCB-49E1-2995BAFE00FB` |
| GridColor | r 0.04500000178813934, g 0.041999999433755875, b 0.03799999877810478, a 1 | identical | yes — GUID `D5FCC737-4FCC-A3EE-9646-B1A8BD94555C` |
| SubGridColor | r 0.09000000357627869, g 0.08500000089406967, b 0.07800000160932541, a 1 | identical | yes — GUID `F04EB7DA-459B-AE57-E5D6-2080C7B9FCEC` |
| TopSurfaceColor (the vector, not the switch) | r 0.11500000208616257, g 0.10999999940395355, b 0.10199999809265137, a 1 | identical | yes — GUID `E7116BE2-4576-3AC8-F6F7-3BA5CA8D3091` |
| TopGridColor | r 0.03999999910593033, g 0.03799999877810478, b 0.03500000014901161, a 1 | identical | yes — GUID `0DD4B258-4314-E25F-674D-65A5EF75B58C` |
| TopSubGridGridColor | r 0.07999999821186066, g 0.07599999755620956, b 0.07000000029802322, a 1 | identical | yes — GUID `AF4DD804-46F6-AA38-1400-A3A3F0F202E1` |
| Line Dimensions | r 0.021838000044226646, g 0.0013470000121742487, b 0.5, a 0 | identical | no — inherited from parent |

`TextureParameterValues` is `[]` before and after — no texture override exists or was created.
`Parent` is `/Game/LevelPrototyping/Materials/M_PrototypeGrid.M_PrototypeGrid` before and after —
the parent was not touched or reassigned.

**Two scalar overrides and six vector overrides, unchanged in value and GUID. Only the one static
switch moved.**

Note the small display differences between the two reads of the same vectors — e.g. SurfaceColor
prints `0.13500000536441803` in both, but GridColor prints `0.045000001788139343` in the raw array
and `0.04500000178813934` from `get_vector_parameter`. That is float-to-string formatting in two
different code paths, not a value change; the underlying float is the same.

---

## 7 · Read-back 3 — dirty flag and disk

```
call: editor_toolset.toolsets.asset.AssetTools.is_dirty
args: {"asset_path": "/Game/LevelPrototyping/Materials/MI_Castle_Stone"}
```

```
{"returnValue":false}
```

```
$ ls -l --time-style=full-iso Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset
-rw-r--r-- 1 a0108 197609 11992 2026-09-04 11:19:11.982912600 +0900 Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset

$ date '+now: %Y-%m-%d %H:%M:%S.%N %z'
now: 2026-09-04 11:19:41.111632400 +0900
```

| | Value |
| --- | --- |
| mtime | 2026-09-04 11:19:11.982912600 +0900 |
| now | 2026-09-04 11:19:41.111632400 +0900 |
| difference | **29.13 s** |

The mtime matches the `LogSavePackage: Moving ...` line at `02:19:11.982` to the millisecond. The
save reached disk; it did not merely clear a flag.

---

## 8 · Read-back 4 — git status

```
$ git status --short
 M Content/Interaction/BP_Torch.uasset
 M Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset
 M Content/LevelPrototyping/Materials/M_Flame.uasset
?? "Docs/Spec/2026-09-04-<Korean filename, shown as octal escapes by git>.md"
?? Docs/Terminal-Log/2026-09-04-56-torch-cast-shadow-off.md
?? Docs/Terminal-Log/2026-09-04-57-torch-shadow-after-reload.md
?? Docs/Terminal-Log/2026-09-04-58-torch-shadow-reload-readback.md
?? Docs/Terminal-Log/2026-09-04-59-flame-material-readout.md
?? Docs/Terminal-Log/2026-09-04-60-flame-brightness-30-to-5.md
```

`MI_Castle_Stone.uasset` is newly modified — this task. `M_Flame.uasset` is from task 60 and
`BP_Torch.uasset` from task 56. No level package, no `__ExternalActors__`, and no
`M_PrototypeGrid.uasset` — the parent material was not written.

---

## 9 · What is still unverified

The screen. Nothing here rendered or measured a pixel, so what `TopSurfaceColor = true` actually
does to the look of the castle stone is not confirmed. From the parameter names the switch should
make top-facing surfaces use `TopSurfaceColor` / `TopGridColor` / `TopSubGridGridColor` instead of
the side colours, all six of which are already overridden on this instance — but that is read off
the naming, not observed.

Also unverified: whether any shader was actually compiled. The log says nothing was, and the DDC
explanation in section 3 is inference. If the intent was specifically to watch a shader compile
happen, this instance did not produce one.
