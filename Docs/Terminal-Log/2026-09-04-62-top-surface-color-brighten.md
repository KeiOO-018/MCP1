# 2026-09-04-62 · MI_Castle_Stone vector TopSurfaceColor brightened

One vector parameter changed, saved, verified. The StaticSwitch of the same name was not touched
and is still `true`. Every other parameter was read after the save and matches the before-values
supplied with the task.

---

## 0 · PIE state

```
call: EditorToolset.EditorAppToolset.IsPIERunning
args: {}
```

```
{"returnValue":false}
```

**No PIE session is running.** Every call below therefore hit the editor world, and no `refPath`
in this log carries a `UEDPIE_0_` prefix. (Worth remembering from log 2026-09-04-61: a PIE session
had been torn down only 8 seconds before that task's check, so this is not a formality.)

---

## 1 · The write

`MaterialInstanceTools` has a separate setter per parameter type, so the Vector/StaticSwitch name
collision on `TopSurfaceColor` is resolved by which tool is called, not by anything in the
arguments. `set_vector_parameter` can only reach the vector.

```
call: editor_toolset.toolsets.material_instance.MaterialInstanceTools.set_vector_parameter
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}, "name": "TopSurfaceColor", "value": {"r": 0.18, "g": 0.172174, "b": 0.159652, "a": 1}}
```

```
{"returnValue":null}
```

That is the only write call in this task. No `set_static_switch_parameter`, no
`set_scalar_parameter`, no `set_parameter_override`, no `set_parent`, and nothing addressed to
`M_PrototypeGrid`.

---

## 2 · Save

```
call: editor_toolset.toolsets.asset.AssetTools.save_assets
args: {"asset_paths": ["/Game/LevelPrototyping/Materials/MI_Castle_Stone"]}
```

```
{"returnValue":true}
```

The save in the log, showing the destination is `Content/` and not `Saved/`:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "02\\.3[3-6]\\.", "maxEntries": 40}
```

```
[2026.09.04-02.35.19:379][325]OBJ SavePackage: Generating thumbnails for [1] asset(s) in package [/Game/LevelPrototyping/Materials/MI_Castle_Stone] ([1] browsable assets)...
[2026.09.04-02.35.19:459][325]OBJ SavePackage:     Rendered thumbnail for [MaterialInstanceConstant /Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone]
[2026.09.04-02.35.19:459][325]OBJ SavePackage: Finished generating thumbnails for package [/Game/LevelPrototyping/Materials/MI_Castle_Stone]
[2026.09.04-02.35.19:459][325]Cmd: OBJ SAVEPACKAGE PACKAGE="/Game/LevelPrototyping/Materials/MI_Castle_Stone" FILE="D:/20260827/MCP1/Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset" SILENT=true
[2026.09.04-02.35.19:468][325]LogSavePackage: Moving output files for package: /Game/LevelPrototyping/Materials/MI_Castle_Stone
[2026.09.04-02.35.19:468][325]LogSavePackage: Moving 'D:/20260827/MCP1/Saved/MI_Castle_StoneF6A4DEDD49BF69AF3C7A749E2A1BC4D2.tmp' to 'D:/20260827/MCP1/Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset'
[2026.09.04-02.35.19:472][325]LogFileHelpers: InternalPromptForCheckoutAndSave took 121.892 ms (total: 624.572 ms)
```

The same response also contains the post-save content validation, which passed:

```
[2026.09.04-02.35.19:710][326]LogContentValidation: Display: Starting to validate 1 assets (0 associated objects such as actors)
[2026.09.04-02.35.19:711][326]AssetCheck: /Game/LevelPrototyping/Materials/MI_Castle_Stone Validating asset
[2026.09.04-02.35.19:711][326]LogContentValidation: Validated asset counts for 9 validators:
[2026.09.04-02.35.19:711][326]LogContentValidation:   /Script/DataValidation.DirtyFilesChangelistValidator : 0
[2026.09.04-02.35.19:711][326]LogContentValidation:   /Script/DataValidation.EditorValidator_ActionUtility : 0
[2026.09.04-02.35.19:711][326]LogContentValidation:   /Script/DataValidation.EditorValidator_Localization : 1
[2026.09.04-02.35.19:711][326]LogContentValidation:   /Script/DataValidation.EditorValidator_Material : 0
[2026.09.04-02.35.19:711][326]LogContentValidation:   /Script/DataValidation.PackageFileValidator : 0
[2026.09.04-02.35.19:711][326]LogContentValidation:   /Script/DataValidation.WorldPartitionChangelistValidator : 0
[2026.09.04-02.35.19:711][326]LogContentValidation:   /Script/InputBlueprintNodes.EnhancedInputUserWidgetValidator : 0
[2026.09.04-02.35.19:711][326]LogContentValidation:   /Script/MutableValidation.AssetValidator_CustomizableObjects : 0
[2026.09.04-02.35.19:711][326]LogContentValidation:   /Script/MutableValidation.AssetValidator_ReferencedCustomizableObjects : 0
```

Those trailing numbers are counts of assets each validator handled, not error counts — no
validation error or warning was emitted. No shader compiler line appeared either, which is
expected: a vector parameter is a uniform, not a shader permutation.

---

## 3 · Read-back 1 — the TopSurfaceColor VECTOR

```
call: editor_toolset.toolsets.material_instance.MaterialInstanceTools.get_vector_parameter
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}, "name": "TopSurfaceColor"}
```

```
{"returnValue":{"r":0.18000000715255737,"g":0.17217400670051575,"b":0.1596519947052002,"a":1}}
```

| Channel | Requested | Read back |
| --- | --- | --- |
| r | 0.18 | 0.18000000715255737 |
| g | 0.172174 | 0.17217400670051575 |
| b | 0.159652 | 0.1596519947052002 |
| a | 1.0 | 1 |

**The write landed.** The extra digits are the float32 representations of the requested values —
the tool takes a double from JSON and stores a float, so 0.18 comes back as the nearest float,
0.18000000715255737. This is not a different value; it is the same value printed at full
precision. Previous value was r 0.115, g 0.11, b 0.102, a 1.

---

## 4 · Read-back 2 — the TopSurfaceColor STATIC SWITCH

```
call: editor_toolset.toolsets.material_instance.MaterialInstanceTools.get_static_switch_parameter
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}, "name": "TopSurfaceColor"}
```

```
{"returnValue":true}
```

**Still `true`.** The vector write did not disturb the switch that shares its name.

---

## 5 · Read-back 3 — all fourteen parameters

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: get_static_switch_parameter / get_scalar_parameter / get_vector_parameter for every parameter
```

```
{"static_switches_effective": {"TopSurfaceColor": true, "ObjectAligned": false, "Grid": true}, "scalars_effective": {"Roughness": 1, "Grid Size": 200, "Sub Grid Number": 5, "CircleSize": 100}, "vectors_effective": {"SurfaceColor": {"r": 0.13500000536441803, "g": 0.125, "b": 0.1120000034570694, "a": 1}, "TopGridColor": {"r": 0.03999999910593033, "g": 0.03799999877810478, "b": 0.03500000014901161, "a": 1}, "GridColor": {"r": 0.04500000178813934, "g": 0.041999999433755875, "b": 0.03799999877810478, "a": 1}, "TopSurfaceColor": {"r": 0.18000000715255737, "g": 0.17217400670051575, "b": 0.1596519947052002, "a": 1}, "TopSubGridGridColor": {"r": 0.07999999821186066, "g": 0.07599999755620956, "b": 0.07000000029802322, "a": 1}, "SubGridColor": {"r": 0.09000000357627869, "g": 0.08500000089406967, "b": 0.07800000160932541, "a": 1}, "Line Dimensions": {"r": 0.021838000044226646, "g": 0.0013470000121742487, "b": 0.5, "a": 0}}}
```

The raw override arrays, as a second independent look:

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}, "properties": ["Parent", "ScalarParameterValues", "VectorParameterValues", "TextureParameterValues"]}
```

```
{"returnValue":"{\"Parent\":{\"refPath\":\"/Game/LevelPrototyping/Materials/M_PrototypeGrid.M_PrototypeGrid\"},\"ScalarParameterValues\":[{\"atlasData\":{\"bIsUsedAsAtlasPosition\":false,\"curve\":\"None\",\"atlas\":\"None\"},\"parameterInfo\":{\"name\":\"Grid Size\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":200,\"expressionGUId\":\"24F0A099-4A5F-B333-0BF3-8D8355E1A214\"},{\"atlasData\":{\"bIsUsedAsAtlasPosition\":false,\"curve\":\"None\",\"atlas\":\"None\"},\"parameterInfo\":{\"name\":\"Roughness\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":1,\"expressionGUId\":\"5258442B-443D-60A7-B6C2-A48F588D02BB\"}],\"VectorParameterValues\":[{\"parameterInfo\":{\"name\":\"SurfaceColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.13500000536441803,\"g\":0.125,\"b\":0.1120000034570694,\"a\":1},\"expressionGUId\":\"00ABBD3F-48B1-4CCB-49E1-2995BAFE00FB\"},{\"parameterInfo\":{\"name\":\"GridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.045000001788139343,\"g\":0.041999999433755875,\"b\":0.037999998778104782,\"a\":1},\"expressionGUId\":\"D5FCC737-4FCC-A3EE-9646-B1A8BD94555C\"},{\"parameterInfo\":{\"name\":\"SubGridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.090000003576278687,\"g\":0.085000000894069672,\"b\":0.078000001609325409,\"a\":1},\"expressionGUId\":\"F04EB7DA-459B-AE57-E5D6-2080C7B9FCEC\"},{\"parameterInfo\":{\"name\":\"TopSurfaceColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.18000000715255737,\"g\":0.17217400670051575,\"b\":0.1596519947052002,\"a\":1},\"expressionGUId\":\"E7116BE2-4576-3AC8-F6F7-3BA5CA8D3091\"},{\"parameterInfo\":{\"name\":\"TopGridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.039999999105930328,\"g\":0.037999998778104782,\"b\":0.035000000149011612,\"a\":1},\"expressionGUId\":\"0DD4B258-4314-E25F-674D-65A5EF75B58C\"},{\"parameterInfo\":{\"name\":\"TopSubGridGridColor\",\"association\":\"GlobalParameter\",\"index\":-1},\"parameterValue\":{\"r\":0.079999998211860657,\"g\":0.075999997556209564,\"b\":0.070000000298023224,\"a\":1},\"expressionGUId\":\"AF4DD804-46F6-AA38-1400-A3A3F0F202E1\"}],\"TextureParameterValues\":[]}"}
```

### Static switches

| Static switch | Before (given with task) | After | Moved? |
| --- | --- | --- | --- |
| TopSurfaceColor | true | true | no |
| ObjectAligned | false | false | no |
| Grid | true | true | no |

### Scalars

| Scalar | Before (given with task) | After | Moved? |
| --- | --- | --- | --- |
| Roughness | 1 | 1 | no |
| Grid Size | 200 | 200 | no |
| Sub Grid Number | 5 | 5 | no |
| CircleSize | 100 | 100 | no |

### Vectors

| Vector | Before (given with task) | After | Moved? |
| --- | --- | --- | --- |
| SurfaceColor | 0.135, 0.125, 0.112, 1 | 0.13500000536441803, 0.125, 0.1120000034570694, 1 | no |
| TopGridColor | 0.04, 0.038, 0.035, 1 | 0.03999999910593033, 0.03799999877810478, 0.03500000014901161, 1 | no |
| GridColor | 0.045, 0.042, 0.038, 1 | 0.04500000178813934, 0.041999999433755875, 0.03799999877810478, 1 | no |
| **TopSurfaceColor** | 0.115, 0.11, 0.102, 1 | **0.18000000715255737, 0.17217400670051575, 0.1596519947052002, 1** | **yes — this task** |
| TopSubGridGridColor | 0.08, 0.076, 0.07, 1 | 0.07999999821186066, 0.07599999755620956, 0.07000000029802322, 1 | no |
| SubGridColor | 0.09, 0.085, 0.078, 1 | 0.09000000357627869, 0.08500000089406967, 0.07800000160932541, 1 | no |
| Line Dimensions | 0.021838, 0.001347, 0.5, 0 | 0.021838000044226646, 0.0013470000121742487, 0.5, 0 | no |

The "before" column is the rounded form supplied with the task; the "after" column is what the
tool actually prints. Every unchanged row is the float32 expansion of its own before-value —
0.135 -> 0.13500000536441803, 0.04 -> 0.03999999910593033, and so on. **TopSurfaceColor is the
only parameter whose value differs, exactly as required.**

Two further confirmations from the raw array: every `expressionGUId` is unchanged from the values
recorded in log 2026-09-04-61, including TopSurfaceColor's own
`E7116BE2-4576-3AC8-F6F7-3BA5CA8D3091` — so the write updated the existing override rather than
creating a new one. `TextureParameterValues` is still `[]`, and `Parent` is still
`/Game/LevelPrototyping/Materials/M_PrototypeGrid.M_PrototypeGrid`, so the parent material was
neither written nor reassigned.

---

## 6 · Read-back 4 — dirty flag and disk

```
call: editor_toolset.toolsets.asset.AssetTools.is_dirty
args: {"asset_path": "/Game/LevelPrototyping/Materials/MI_Castle_Stone"}
```

```
{"returnValue":false}
```

```
$ ls -l --time-style=full-iso Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset
-rw-r--r-- 1 a0108 197609 12462 2026-09-04 11:35:19.468185400 +0900 Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset

$ date '+now: %Y-%m-%d %H:%M:%S.%N %z'
now: 2026-09-04 11:35:54.513951100 +0900
```

| | Value |
| --- | --- |
| mtime | 2026-09-04 11:35:19.468185400 +0900 |
| now | 2026-09-04 11:35:54.513951100 +0900 |
| difference | **35.05 s** |

The mtime matches the `LogSavePackage: Moving ...` line at `02:35:19.468` to the millisecond. The
save reached disk; it did not merely clear a flag.

The file also grew from 11992 bytes (after log 61's save) to 12462 bytes, a further sign the
package was genuinely rewritten.

---

## 7 · Read-back 5 — git status

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
?? Docs/Terminal-Log/2026-09-04-61-castle-stone-top-surface-color.md
```

The same three modified assets as after log 61 — `MI_Castle_Stone.uasset` was already modified
there, so this task adds no new path to the list, only new content inside that file.
`BP_Torch.uasset` is from task 56 and `M_Flame.uasset` from task 60. No `M_PrototypeGrid.uasset`,
no level package, nothing under `Content/__ExternalActors__`.

---

## 8 · What is still unverified

The screen. Nothing here rendered or measured a pixel, so how the brighter top surface actually
looks on the castle stone is not confirmed. The change raises the top-face colour from roughly
0.115/0.11/0.102 to 0.18/0.172/0.16 — about 57% brighter in linear space, and slightly less warm
in the ratio between channels. Whether that reads correctly next to the unchanged side colour
(SurfaceColor, 0.135/0.125/0.112) needs eyes on the viewport.
