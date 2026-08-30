# 2026-08-30 · Command 39 — BP_Door DoorMesh default RelativeScale3D

Target: `/Game/Interaction/BP_Door`, component `DoorMesh`.
Change the Blueprint **default** `RelativeScale3D` from `(1,1,1)` to `(0.05, 0.5, 1.1)`
so the door leaf reads 10 x 100 x 220 cm instead of the 200 cm cube.
This is a Blueprint default change, not a level change.

`AssetTools.is_dirty` was **not** called, per the instruction.

---

## Pre-flight

### P1 — `ActorTools.get_components` on `/Game/Interaction/BP_Door.Default__BP_Door_C`

```json
{"returnValue":[{"refPath":"/Game/Interaction/BP_Door.BP_Door_C:DefaultSceneRoot_GEN_VARIABLE"},{"refPath":"/Game/Interaction/BP_Door.BP_Door_C:Hinge_GEN_VARIABLE"},{"refPath":"/Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE"}]}
```

**PASS.** Exactly three components, in the expected order:
`DefaultSceneRoot_GEN_VARIABLE`, `Hinge_GEN_VARIABLE`, `DoorMesh_GEN_VARIABLE`.

### P2 — `ObjectTools.get_properties` on `/Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE`

Properties requested: `["RelativeLocation","RelativeRotation","RelativeScale3D","StaticMesh"]`

```json
{"RelativeLocation":{"x":0,"y":0,"z":0},"RelativeRotation":{"pitch":0,"yaw":0,"roll":0},"RelativeScale3D":{"x":1,"y":1,"z":1},"StaticMesh":{"refPath":"/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door.SM_Door"}}
```

**PASS.** Location `(0,0,0)`, rotation `(0,0,0)`, scale `(1,1,1)`,
StaticMesh `/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door.SM_Door`.

### P3 — `StaticMeshTools.get_bounds` on SM_Door

```json
{"returnValue":{"min":{"x":-100.00001525878906,"y":-100.00001525878906,"z":-100},"max":{"x":100.00001525878906,"y":100.00001525878906,"z":100},"isValid":true}}
```

**PASS.** Exact numbers as returned:

| | x | y | z |
|---|---|---|---|
| min | -100.00001525878906 | -100.00001525878906 | -100 |
| max | 100.00001525878906 | 100.00001525878906 | 100 |

`isValid: true`. X and Y carry a float-precision tail of about 1.5e-5 cm; Z is exactly ±100.
This is about (-100,-100,-100)..(100,100,100) as expected, so the 200 cm cube reading holds
and the derived scale `(0.05, 0.5, 1.1)` for a 10 x 100 x 220 cm leaf is correct.

### P4 — `BlueprintTools.list_functions` and the ConstructionScript DSL

`list_functions` on `/Game/Interaction/BP_Door.BP_Door`:

```json
{"returnValue":[{"name":"UserConstructionScript","description":"","bIsImplemented":true}]}
```

**PASS.** One function only: `UserConstructionScript`.

The graph was resolved with `BlueprintTools.get_graph(blueprint, "UserConstructionScript")`,
which returned `/Game/Interaction/BP_Door.BP_Door:UserConstructionScript`.

`read_graph_dsl` on that graph returned, verbatim — the tool returns the whole
`SetRelativeLocation` expression on a single line; the raw string with its `\n` escapes was:

```
(fn ConstructionScript ()\n  (Transformation|SetRelativeLocation (Variables|Default|GetDoorMesh) (Math|Vector|MakeVector 0.0 (* (* 100.0 (.y (Class|SceneComponent|GetRelativeScale3D (Variables|Default|GetDoorMesh)))) (select (|GetbHingeOnRight) -1.0 1.0)))))\n
```

The same text with the newlines rendered:

```
(fn ConstructionScript ()
  (Transformation|SetRelativeLocation (Variables|Default|GetDoorMesh) (Math|Vector|MakeVector 0.0 (* (* 100.0 (.y (Class|SceneComponent|GetRelativeScale3D (Variables|Default|GetDoorMesh)))) (select (|GetbHingeOnRight) -1.0 1.0)))))
```

**PASS.** The `100.0` literal is present and the `.y` read of
`Class|SceneComponent|GetRelativeScale3D (Variables|Default|GetDoorMesh)` is present.
The offset therefore follows the scale: with ScaleY `0.5` the hinge offset computes to
`100.0 * 0.5 = 50`, times the `select` sign taken from `bHingeOnRight`.

Note on formatting only: the expected DSL in the command was written across several lines,
while the tool returns it on one. The node structure, the literals and the operand order are
identical — the difference is whitespace in the returned string, not a difference in the graph.

### P5 — `SceneTools.find_actors` for BP_Door_C in the loaded level

Current level, from `SceneTools.get_current_level`:

```
/Game/ThirdPerson/Lvl_ThirdPerson
```

`find_actors` with `actor_type = /Game/Interaction/BP_Door.BP_Door_C`
(and empty `name`, empty `tag`, empty `collision_channels`):

```json
{"returnValue":[]}
```

**PASS.** BP_Door instance count in the loaded level: **0**. No placed instance can shadow
this default with its own overridden component scale.

All five pre-flight checks passed. Proceeded to the action.

---

## Action

One call, `ObjectTools.set_properties`:

- instance: `/Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE`
- values: `{"RelativeScale3D":{"x":0.05,"y":0.5,"z":1.1}}`

Returned boolean:

```json
{"returnValue":true}
```

`RelativeLocation`, `RelativeRotation` and `StaticMesh` on DoorMesh were not touched.
`Hinge` and `DefaultSceneRoot` were not touched. No variable (`bLocked`, `RequiredKey`,
`bHingeOnRight`, `OpenAngle`, `SwingSpeed`, `bOpen`) was touched.

---

## Verify

### 1. Read-back BEFORE compiling

```json
{"RelativeScale3D":{"x":0.050000000000000003,"y":0.5,"z":1.1000000000000001}}
```

### 2. Compile

`BlueprintTools.compile_blueprint` on `/Game/Interaction/BP_Door.BP_Door`
(`warnings_as_errors` left at its default, `false`):

```json
{"returnValue":null}
```

The tool declares no output schema, so `null` is what a completed call returns here — it is
not a status value and carries no pass/fail information. This matches the standing project
observation that a `unreal-mcp` return value is not evidence. The evidence that the compile
did not disturb the change is read-back #3 below, plus the component re-read.

### 3. Read-back AFTER compiling

```json
{"RelativeScale3D":{"x":0.050000000000000003,"y":0.5,"z":1.1000000000000001}}
```

### 4. Save

`AssetTools.save_assets` with `asset_paths = ["/Game/Interaction/BP_Door"]`:

```json
{"returnValue":true}
```

### 5. Read-back AFTER saving

```json
{"RelativeScale3D":{"x":0.050000000000000003,"y":0.5,"z":1.1000000000000001}}
```

### Read-back verdict

All three read-backs hold the target value. The printed decimals
`0.050000000000000003` and `1.1000000000000001` are the double-precision
representations of `0.05` and `1.1` — neither `0.05` nor `1.1` is exactly representable in
binary floating point, so this is the expected round-trip of the values that were sent, not a
drift or a rounding introduced by the editor. `y` came back as exactly `0.5`, which is
exactly representable.

`ScaleY` is therefore exactly `0.5`, so the ConstructionScript hinge offset
`100.0 * ScaleY` evaluates to exactly `50`, as required.

No retry of any kind was needed; every call above was made once.

### Component re-read after the whole sequence

`ActorTools.get_components` on `/Game/Interaction/BP_Door.Default__BP_Door_C`:

```json
{"returnValue":[{"refPath":"/Game/Interaction/BP_Door.BP_Door_C:DefaultSceneRoot_GEN_VARIABLE"},{"refPath":"/Game/Interaction/BP_Door.BP_Door_C:Hinge_GEN_VARIABLE"},{"refPath":"/Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE"}]}
```

Still exactly three components, same names, same order as in P1. Nothing was added,
removed or renamed.

---

## Errors and warnings

Two errors were encountered. Both belong to tool discovery, not to the door change.
Both texts below are reproduced exactly as returned, untranslated and uncleaned.

`describe_toolset` on `BlueprintTools` returned a payload too large to read directly:

```
Error: result (72,168 characters across 1 line) exceeds maximum allowed tokens. Output has been saved to C:\Users\a0108\.claude\projects\D--20260827-MCP1\87ded4f6-4592-46f2-bb0a-5f0d5a4781ec\tool-results\mcp-unreal-mcp-describe_toolset-1788089584129.txt.
```

An earlier call named the toolset with its short name and produced:

```
Toolset 'ActorTools' not found. Available toolsets: ToolsetRegistry.AgentSkillToolset, EditorToolset.EditorAppToolset, EditorToolset.LogsToolset, editor_toolset.toolsets.actor.ActorTools, editor_toolset.toolsets.asset.AssetTools, editor_toolset.toolsets.blueprint.BlueprintTools, editor_toolset.toolsets.curve_table.CurveTableTools, editor_toolset.toolsets.data_asset.DataAssetTools, editor_toolset.toolsets.data_table.DataTableTools, editor_toolset.toolsets.material.MaterialTools, editor_toolset.toolsets.material_instance.MaterialInstanceTools, editor_toolset.toolsets.object.ObjectTools, editor_toolset.toolsets.primitive.PrimitiveTools, editor_toolset.toolsets.scene.SceneTools, editor_toolset.toolsets.skeletal_mesh.SkeletalMeshTools, editor_toolset.toolsets.static_mesh.StaticMeshTools, editor_toolset.toolsets.string_table.StringTableTools, editor_toolset.toolsets.programmatic.ProgrammaticToolset, editor_toolset.toolsets.texture.TextureTools
```

The fully-qualified toolset names are required; the short names are not accepted.

**No error or warning was produced by any pre-flight check, by `set_properties`, by
`compile_blueprint`, by `save_assets`, or by any read-back.** The compile in particular
emitted no message through the MCP surface — a `null` return is all that came back, and the
editor's own Message Log was not read as part of this command, so a compile warning that
appeared only there would not have been captured here.

---

## Not confirmed

- The door leaf was **not** viewed in the editor viewport or in PIE. The change is confirmed
  by property read-back only, not visually.
- The hinge offset of `50` is **derived** from the DSL and `ScaleY = 0.5`. The
  ConstructionScript was not observed running, so the resulting `DoorMesh`
  `RelativeLocation` at construction time was not measured.
- Compile warnings, if any, were not captured — see the note above.
