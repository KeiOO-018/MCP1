# 2026-09-03 · Command 54 — M_Flame and BP_Torch

Asset change only, in `/Game/LevelPrototyping/Materials/` and `/Game/Interaction/`.
**No actor was created, moved or deleted. Actor count 120 before and after.**

**Two assets created: `M_Flame` (unlit emissive material, 2 exposed parameters) and
`BP_Torch` (Actor Blueprint, 5 components + DefaultSceneRoot, no variables, no
graph logic). Both compiled clean and saved. 2 packages written, both new.**

Instruction, verbatim from the user:

> In the currently open project, create a torch. This command creates assets ONLY - it
> must not add, move or delete any actor in the level, and must not touch the 18 existing
> PointLight actors. Replacing them comes in a separate command.
>
> Background for the geometry: the torch will be placed against a wall, at the exact
> positions the 18 existing PointLight actors occupy. Those sit 50 units out from the wall
> face. So build the torch in local space with the wall behind it at local X = -50, and
> the torch pointing along local +X into the room. Each placement will then just need a
> yaw to face the right wall.
>
> STEP 1 - Create an emissive flame material.
>
>   Folder  /Game/LevelPrototyping/Materials
>   Name    M_Flame
>   Shading model unlit if the material supports it, otherwise leave the default.
>
>   Graph: a constant colour of R 1.0, G 0.45, B 0.12 multiplied by a scalar of 30,
>   connected to Emissive Color. Expose the colour as a vector parameter named
>   "FlameColor" and the scalar as a scalar parameter named "FlameBrightness" so both can
>   be tuned from an instance later. Compile it and report the compile result verbatim.
>
> STEP 2 - Create an Actor Blueprint.
>
>   Folder  /Game/Interaction
>   Name    BP_Torch
>   Parent class  Actor
>
>   Set bCanEverTick to false.
>   Add NO variables and NO event graph logic. This actor is geometry and a light, nothing
>   more.
>
> STEP 3 - Add five components to BP_Torch. All local transforms are relative to the
> actor origin. The actor origin is where the light goes, so that placing BP_Torch at an
> existing PointLight's coordinates reproduces that light exactly.
>
>   1. "Backplate"  cube,     dimensions X 12, Y 16, Z 34,  local location (-46, 0, -24)
>   2. "Bracket"    cylinder, radius 5,  height 55,          local location (-24, 0, -22),
>                                                            local rotation pitch 55
>   3. "Cup"        cone,     radius 13, height 20,          local location (0, 0, -24)
>   4. "Flame"      cone,     radius 9,  height 30,          local location (0, 0, -14)
>   5. "Light"      PointLight component,                    local location (0, 0, 0)
>
>   Cup must open upward like a bowl. If the cone primitive is created with its apex up
>   and its base down, rotate Cup by 180 degrees so the apex points down. Flame keeps the
>   default orientation, apex up.
>
>   Assign M_Flame to the Flame component only. Backplate, Bracket and Cup take
>   /Game/LevelPrototyping/Materials/MI_Castle_Stone.
>
>   Set the Light component to exactly the values the 18 existing PointLight actors use:
>     Mobility          Movable
>     Intensity         5000
>     IntensityUnits    Unitless
>     AttenuationRadius 1200
>     SourceRadius      10
>     CastShadows       true
>     LightColor        R 255, G 170, B 90
>
>   Give the Flame component CastShadow false and collision disabled, so the flame mesh
>   does not block its own light.
>
> STEP 4 - Compile and save BP_Torch and M_Flame. Save with AssetTools.save_assets and an
> empty list. Report which packages were written, verified on disk.
>
> DO NOT create, move or delete any actor in the level. DO NOT touch the 18 PointLight
> actors, any wall, floor, door, ramp, railing or pillar. DO NOT modify MI_Castle_Stone,
> MI_Castle_Wood, M_FlatCol, M_PrototypeGrid or any MI_PrototypeGrid_* instance.
>
> VERIFY AND REPORT.
>
>   A) Report EditorToolset.EditorAppToolset.IsPIERunning first. If true, stop and say so.
>
>   B) List every component on BP_Torch with its name, type, local location, local
>      rotation, local scale, assigned material, and - for the mesh components - the
>      LOCAL-SPACE bounding box the component actually occupies. I need the real bounds
>      because I do not know this toolset's pivot and axis convention for cube, cylinder
>      and cone primitives, and the numbers above were written assuming Z-up shapes.
>      Report what they really are rather than what was asked for.
>
>   C) Report the combined local bounding box of the whole actor, so I can tell how far
>      the torch sticks out from the wall and how tall it is.
>
>   D) Report every property of the Light component, and say whether each matches the
>      values listed in STEP 3.
>
>   E) Confirm the level was not modified: report the total actor count and confirm it is
>      120, the same as before this command.
>
>   F) Report which packages were written to disk.
>
>   G) Report any warning or error text verbatim in English. Do not summarize or translate.
>
> Write the report to Docs/Terminal-Log/2026-09-03-54-torch-blueprint.md
> (a repo path - do NOT write under Saved/, it is gitignored).

---

## A) PIE state — checked first

`EditorToolset.EditorAppToolset.IsPIERunning`:

```json
{"returnValue":false}
```

**PIE is not running.** Checked before any change, and re-checked at the end —
still `false`.

---

## STEP 1 — M_Flame

Created with `MaterialTools.create_material`. Graph built from three expressions:

| Expression | Class | Settings |
|---|---|---|
| `MaterialExpressionVectorParameter_0` | VectorParameter | `parameterName` **FlameColor**, `defaultValue` `(1, 0.44999998807907104, 0.11999999731779099, 1)` |
| `MaterialExpressionScalarParameter_0` | ScalarParameter | `parameterName` **FlameBrightness**, `defaultValue` **30** |
| `MaterialExpressionMultiply_0` | Multiply | A ← FlameColor `RGB`, B ← FlameBrightness |

Wiring, read back rather than assumed:

```json
"emissive_source": {"output_name":"","expression":{"refPath":"...M_Flame:MaterialExpressionMultiply_0"},"input_name":""}
"multiply_inputs": [
  {"output_name":"RGB","expression":{"refPath":"...MaterialExpressionVectorParameter_0"},"input_name":"A"},
  {"output_name":"","expression":{"refPath":"...MaterialExpressionScalarParameter_0"},"input_name":"B"}]
```

So the graph is exactly `FlameColor.RGB × FlameBrightness → Emissive Color`.
`expression_count` is **3** — no stray nodes.

**Shading model: unlit.** The material supports it and it was set:

```json
{"shadingModel":"MSM_Unlit","blendMode":"BLEND_Opaque","twoSided":false}
```

**Parameters exposed to future instances**, confirmed via `list_parameters`:

```json
[{"type":"Scalar","name":"FlameBrightness"},{"type":"Vector","name":"FlameColor"}]
```

Exactly the two asked for, and nothing else.

### Compile result, verbatim

`MaterialTools.recompile`:

```json
{"returnValue":null}
```

The tool returns `null` on success; its documentation states it "raises if the
shader fails to compile", and it did not raise. **No `LogShaderCompilers` error
or warning was emitted for M_Flame** — the only shader-compiler lines in the
whole session log are from editor startup at `08:46:02`, before this command
existed:

```
[2026.09.03-08.46.02:056][  0]LogShaderCompilers: Display: No distributed shader compiler controller found
[2026.09.03-08.46.02:056][  0]LogShaderCompilers: Display: Using 12 local workers for shader compilation
[2026.09.03-08.46.02:066][  0]LogShaderCompilers: Display: Compiling shader autogen file: D:/20260827/MCP1/Intermediate/ShaderAutogen/PCD3D_SM6/AutogenShaderHeaders.ush
[2026.09.03-08.46.02:083][  0]LogShaderCompilers: Display: Autogen file is unchanged, skipping write.
```

There is no per-material compile line to quote. The compile is evidenced by the
absence of any raise and the absence of any diagnostic.

---

## The pivot and axis convention, measured

The instruction asked for the real bounds because the toolset's primitive
convention was unknown. **It was measured, not assumed.** All three primitive
types resolve to 100×100×100 engine meshes whose pivot is at their **centre**,
and `dimensions` / `radius` / `height` are converted into a scale:

| Primitive | Mesh | Mesh local bounds | Conversion observed |
|---|---|---|---|
| cube | `/Engine/BasicShapes/Cube` | `(-50,-50,-50)` .. `(50,50,50)` | scale = dimensions / 100 |
| cylinder | `/Engine/BasicShapes/Cylinder` | `(-50,-50,-50)` .. `(50,50,50)` | scale XY = radius / 50, Z = height / 100 |
| cone | `/Engine/BasicShapes/Cone` | `(-50,-50,-50)` .. `(50,50,49.99998474121094)` | scale XY = radius / 50, Z = height / 100 |

**The pivot is the centre, not a corner and not the base.** So a component placed
at local Z = -24 with height 20 spans Z -34..-14, straddling its location — not
sitting on top of it.

### Cone apex direction — verified by rendering, not assumed

The instruction made the Cup flip conditional on the cone's default orientation.
The cone's bounding box is symmetric in Z, so it cannot answer the question.
`EditorAppToolset.CaptureAssetImage` on `/Engine/BasicShapes/Cone` was rendered
and inspected: **the apex points up (+Z) and the circular base is down (−Z).**

Therefore the condition in the instruction applies, and **Cup was rotated 180°**
so its apex points down and it opens upward like a bowl. **The axis was my
choice** — the instruction said "rotate Cup by 180 degrees" without naming one. I
used **roll 180**. The cone is radially symmetric about Z, so roll and pitch give
the same result here.

Flame was left at rotation `(0,0,0)`, apex up, as instructed.

---

## B) Every component on BP_Torch

All five requested components exist, plus the `DefaultSceneRoot` that UE creates
with a new Actor Blueprint. **All five are parented directly to
`DefaultSceneRoot`**, which is the root component — no accidental nesting.

Local bounds below are computed from each component's actual mesh bounds, put
through its actual relative location, rotation and scale. They are the real
occupied boxes, not the requested figures.

### 1. Backplate

| Field | Value |
|---|---|
| Type | `/Script/Engine.StaticMeshComponent` (cube) |
| Mesh | `/Engine/BasicShapes/Cube.Cube` |
| Local location | `(-46, 0, -24)` |
| Local rotation | `(0, 0, 0)` |
| Local scale | `(0.12, 0.16, 0.34)` |
| **Local bounds** | **min `(-52, -8, -41)` max `(-40, 8, -7)`** |
| **Occupied size** | **12 × 16 × 34** — exactly the requested dimensions |
| Material | `MI_Castle_Stone` |
| CastShadow | `true` |

### 2. Bracket

| Field | Value |
|---|---|
| Type | `/Script/Engine.StaticMeshComponent` (cylinder) |
| Mesh | `/Engine/BasicShapes/Cylinder.Cylinder` |
| Local location | `(-24, 0, -22)` |
| Local rotation | `(pitch 55.00000000000003, 0, 0)` |
| Local scale | `(0.1, 0.1, 0.55)` |
| **Local bounds** | **min `(-49.395, -5, -41.869)` max `(1.395, 5, -2.131)`** |
| **Occupied size** | **50.79 × 10 × 39.738** |
| Material | `MI_Castle_Stone` |
| CastShadow | `true` |

The cylinder is 10 across and 55 long as asked; the 50.79 × 39.738 box is the
axis-aligned envelope of that 55-long rod tilted 55°, which is expected, not an
error.

### 3. Cup

| Field | Value |
|---|---|
| Type | `/Script/Engine.StaticMeshComponent` (cone) |
| Mesh | `/Engine/BasicShapes/Cone.Cone` |
| Local location | `(0, 0, -24)` |
| Local rotation | **`(0, 0, 180)`** — the flip, apex now down |
| Local scale | `(0.26, 0.26, 0.20000003051758278)` |
| **Local bounds** | **min `(-13, -13, -34)` max `(13, 13, -14)`** |
| **Occupied size** | **26 × 26 × 20** — diameter 26, i.e. radius 13, as asked |
| Material | `MI_Castle_Stone` |
| CastShadow | `true` |

### 4. Flame

| Field | Value |
|---|---|
| Type | `/Script/Engine.StaticMeshComponent` (cone) |
| Mesh | `/Engine/BasicShapes/Cone.Cone` |
| Local location | `(0, 0, -14)` |
| Local rotation | `(0, 0, 0)` — apex up, as instructed |
| Local scale | `(0.18, 0.18, 0.3000000457763742)` |
| **Local bounds** | **min `(-9, -9, -29)` max `(9, 9, 1)`** |
| **Occupied size** | **18 × 18 × 30** — diameter 18, i.e. radius 9, as asked |
| Material | **`M_Flame`** — the only component with it |
| **CastShadow** | **`false`** ✓ |
| **Collision** | **`bodyInstance.collisionEnabled` = `NoCollision`** ✓ |

### 5. Light

| Field | Value |
|---|---|
| Type | `/Script/Engine.PointLightComponent` |
| Local location | `(0, 0, 0)` — the actor origin, as required |
| Local rotation | `(0, 0, 0)` |
| Local scale | `(1, 1, 1)` |
| Material | n/a |

### 6. DefaultSceneRoot (engine-created)

| Field | Value |
|---|---|
| Type | `/Script/Engine.SceneComponent` |
| Local transform | location `(0,0,0)`, rotation `(0,0,0)`, scale `(1,1,1)` |

It is the root and adds no offset, so every component's local transform above is
also its transform relative to the actor origin.

---

## C) Combined local bounding box

Over the four mesh components (the light and the empty root have no geometry):

| | X | Y | Z |
|---|---|---|---|
| **min** | **-52** | **-13** | **-41.869** |
| **max** | **13** | **13** | **1** |
| **size** | **65** | **26** | **42.869** |

### What that means against the wall at local X = -50

- **The torch reaches 63 units into the room** — from the wall face at X = -50 out
  to X = +13, the front lip of the Cup.
- **The Backplate is embedded 2 units into the wall** (its min X is -52, the wall
  face is -50). That is a deliberate consequence of the numbers given and is
  useful: it avoids a coplanar seam with the wall surface. It does mean the
  backplate is not flush-mounted but sunk slightly.
- **The light sits exactly 50 units from the wall face**, at local X = 0. That
  reproduces the existing PointLight standoff exactly, which is the whole point
  of the origin placement.
- **Total height is 42.87 units**, from Z -41.869 to Z +1.
- **The actor origin is near the top of the torch, not its centre.** The body hangs
  below the origin: 41.87 units below, and only 1 unit above. So placing BP_Torch
  at an existing light's Z will hang the torch **below** that point — at the
  ground-floor lights (Z 250) the torch would occupy roughly Z 208–251, and at
  the second-floor lights (Z 850) roughly Z 808–851.
- **Width is 26 units**, set by the Cup, centred on Y = 0.

### How the parts relate to each other

- Cup occupies Z -34..-14; Flame occupies Z -29..+1. **The flame's base is inside
  the cup**, overlapping it over Z -29..-14, which is the intended "flame sitting
  in a bowl" arrangement.
- Bracket spans Z -41.869..-2.131 and X -49.395..1.395, so it runs from just in
  front of the backplate up to under the cup, which is what a wall bracket should
  do.
- **The Light at (0,0,0) sits inside the Flame cone**, 1 unit below its tip. Because
  Flame has `castShadow false` and `NoCollision`, it does not occlude or block the
  light — which is exactly why the instruction asked for those two settings.

---

## D) The Light component

Read back after compiling.

| Property | Value | Asked | Match |
|---|---|---|---|
| `mobility` | `Movable` | Movable | **✓** |
| `intensity` | `5000` | 5000 | **✓** |
| `intensityUnits` | `Unitless` | Unitless | **✓** |
| `attenuationRadius` | `1200` | 1200 | **✓** |
| `sourceRadius` | `10` | 10 | **✓** |
| `castShadows` | `true` | true | **✓** |
| `lightColor` | `(1, 0.6666666865348816, 0.3529411852359772, 1)` = **(255, 170, 90)** | R255 G170 B90 | **✓** |
| `relativeLocation` | `(0, 0, 0)` | (0,0,0) | **✓** |

```json
{"all_light_ok": true}
```

The colour floats are bit-identical to those on the 18 existing PointLight actors
(`0.6666666865348816`, `0.3529411852359772`), so this light is an exact match for
them, not merely a close one. As in commands 49–50, the RGB→0..1 conversion is
mine: the setter clamps at 1, so 255/170/90 was sent as 1.0 / 170÷255 / 90÷255.

Additional properties read but not specified, left at engine defaults:

| Property | Value |
|---|---|
| `relativeRotation` | `(0, 0, 0)` |
| `bUseInverseSquaredFalloff` | `true` |
| `bAffectsWorld` | `true` |

`bUseInverseSquaredFalloff = true` matches the 18 existing lights, so the torch
light will behave identically to them. This is the same setting flagged in
command 49 as the likely cause if the lighting reads wrong; it is consistent
here by design, not overlooked.

---

## STEP 2 checks — tick, variables, graph

| Requirement | Result |
|---|---|
| Parent class | `/Script/Engine.Actor` ✓ |
| `bCanEverTick` | **`false`** ✓ (verified **after** the final compile) |
| `bStartWithTickEnabled` | `false` |
| Variables | **`[]`** — none added ✓ |
| Functions | only `UserConstructionScript` (engine default) |

**`primaryActorTick`, read back in full:**

```json
{"tickGroup":"TG_PrePhysics","endTickGroup":"TG_PrePhysics","bTickEvenWhenPaused":false,
 "bCanEverTick":false,"bStartWithTickEnabled":false,"bAllowTickOnDedicatedServer":true,
 "tickInterval":0}
```

**On the event graph — stating this precisely rather than just claiming "empty".**
`find_nodes` reports 3 nodes in `EventGraph` and 1 in `UserConstructionScript`.
These are the stub nodes UE places on every new Actor Blueprint. Reading the graph
confirms **nothing is wired to any of them**:

```
(event EventBeginPlay)

(event Collision|EventActorBeginOverlap (OtherActor))

(event EventTick (DeltaSeconds))
```

Three bare event nodes, no execution chains, no logic. **I added no nodes.** I
also did not delete these engine defaults, since removing them was not requested.

Note that `list_events` reports `ReceiveTick` with `bIsImplemented: true` because
the stub node exists. It has no connected logic, and `bCanEverTick` reads `false`
after the final compile, so the tick will not run. Flagging it because the two
facts look contradictory in isolation.

### Blueprint compile

`BlueprintTools.compile_blueprint` returned `{"returnValue": null}` (null on
success). Six `LogBlueprint` compile lines appear for BP_Torch — each
`add_component` / primitive add triggers one, plus the explicit final compile:

```
[2026.09.03-12.15.02:157][ 49]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Torch.BP_Torch'
[2026.09.03-12.15.33:162][142]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Torch.BP_Torch'
[2026.09.03-12.15.33:492][143]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Torch.BP_Torch'
[2026.09.03-12.15.33:826][144]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Torch.BP_Torch'
[2026.09.03-12.16.22:969][795]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Torch.BP_Torch'
[2026.09.03-12.18.04:632][100]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Torch.BP_Torch'
```

**No compile error or compile warning appears in any of them.**

---

## E) The level was not modified

| | Count |
|---|---|
| Total actors before | **120** |
| Total actors after | **120** |

**Unchanged, as required.** Additionally:

- Actors matching `Torch_`: **18** — the existing PointLight actors, all still
  present and untouched.
- `BP_Torch` instances in the level: **0** — the Blueprint was created as an asset
  only and never placed, which the instruction required.
- `IsPIERunning`: `false` at the end as well as the start.

The strongest evidence is at file level: **no `__ExternalActors__` package was
written by the save** (section F). Every actor in this World Partition level lives
in its own package, so if any actor had been created, moved, deleted or edited,
its package would have been written. None was.

---

## F) Packages written to disk

`AssetTools.save_assets` with `[]` returned `{"returnValue":true}`. Verified by
diffing a full `.uasset` listing taken before the save against one taken after.

| | Count |
|---|---|
| `.uasset` files before | **359** |
| `.uasset` files after | **361** |

**Added — exactly two, both new:**

```
Content/LevelPrototyping/Materials/M_Flame.uasset
Content/Interaction/BP_Torch.uasset
```

**Removed: none. Modified: none.**

A `find` for anything under `Content` modified in the last 4 minutes returned
exactly these two and nothing else:

```
2026-09-03 21:19:57.7229703000  Content/LevelPrototyping/Materials/M_Flame.uasset
2026-09-03 21:19:57.8154169000  Content/Interaction/BP_Torch.uasset
```

Confirmed in the log — exactly two `Saving Package` lines, and validation on
exactly two assets:

```
[2026.09.03-12.19.57:714][439]LogFileHelpers: Saving Package: /Game/LevelPrototyping/Materials/M_Flame
[2026.09.03-12.19.57:727][439]LogFileHelpers: Saving Package: /Game/Interaction/BP_Torch
[2026.09.03-12.19.57:987][440]LogContentValidation: Display: Starting to validate 2 assets (0 associated objects such as actors)
[2026.09.03-12.19.57:987][440]AssetCheck: /Game/LevelPrototyping/Materials/M_Flame Validating asset
[2026.09.03-12.19.57:988][440]AssetCheck: /Game/Interaction/BP_Torch Validating asset
```

`0 associated objects such as actors` independently confirms no actor was
involved.

**Not written, which is the proof they were left alone:**
`MI_Castle_Stone.uasset`, `MI_Castle_Wood.uasset`, `M_FlatCol.uasset`,
`M_PrototypeGrid.uasset`, every `MI_PrototypeGrid_*.uasset`, `SM_Cube.uasset`,
`SM_Cylinder.uasset`, `SM_Ramp.uasset`, `SM_Door.uasset`, `BP_Door.uasset`, and
every `__ExternalActors__` package.

### Reading the working tree correctly

```
 M Content/LevelPrototyping/Interactable/Door/Meshes/SM_Door.uasset
 M Content/LevelPrototyping/Meshes/SM_Cube.uasset
 M Content/LevelPrototyping/Meshes/SM_Cylinder.uasset
 M Content/LevelPrototyping/Meshes/SM_Ramp.uasset
?? Content/Interaction/BP_Torch.uasset
?? Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset
?? Content/LevelPrototyping/Materials/MI_Castle_Wood.uasset
?? Content/LevelPrototyping/Materials/M_Flame.uasset
?? Docs/Terminal-Log/2026-09-03-52-castle-stone-material.md
?? Docs/Terminal-Log/2026-09-03-53-door-wood-material.md
```

**Only two of those ten lines belong to this command** — `BP_Torch.uasset` and
`M_Flame.uasset`. The four ` M` entries and the two `MI_Castle_*` entries are
carried over from commands 52 and 53, which are still uncommitted; their mtimes
are `20:38:44` and `21:05:21`, not `21:19:57`. Commands 52, 53 and 54 are all on
disk and none is committed.

---

## G) Warnings and errors, verbatim

This command's work runs from `12:12` (create_material) to `12:19:58` (end of save
validation). **No error was emitted. Three `LogScript` warnings and a block of
`LogJson` schema warnings occurred, all from my own calls.** Details below.

### The three that mattered — disabling collision took three attempts

`collisionEnabled` and `collisionProfileName` are listed by `list_properties` on a
StaticMeshComponent, but **neither can be written, and neither can even be read**.
Verbatim, in order:

```
[2026.09.03-12.16.40:966][849]LogScript: Warning: SetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Flame_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be set: collisionEnabled
[2026.09.03-12.16.58:968][903]LogScript: Warning: SetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Flame_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be set: collisionProfileName
[2026.09.03-12.17.34:299][  9]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Flame_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be read: collisionEnabled, collisionProfileName
```

The tool returned the first two to me as errors, verbatim:

```
SetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Flame_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be set: collisionEnabled
```

```
SetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Flame_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be set: collisionProfileName
```

**The working route is the `bodyInstance` struct**, which is both writable and
readable:

```
set_properties → {"bodyInstance":{"collisionEnabled":"NoCollision"}}  →  true
get_properties → "bodyInstance":{..., "collisionEnabled":"NoCollision", ...}
```

Collision on Flame is genuinely disabled, confirmed by read-back after the final
compile.

**A tool behaviour worth recording:** these failures propagate out of
`execute_tool_script` and abort the entire script, and a Python `try`/`except`
inside the script does **not** catch them — the promotion to error happens at the
MCP layer, below the script. So a batch script must not contain a call that might
fail this way; each risky property has to be attempted in its own call. Two of my
batch scripts were killed this way before I split the calls out.

### The rest — schema-generation noise from `list_properties`

`ObjectTools.list_properties` on components emits one warning per delegate
property it cannot express in JSON Schema. These are harmless and read-only. The
block at `12:17:44`, verbatim:

```
[2026.09.03-12.17.44:638][ 40]LogJson: Warning: Property "OnInputTouchLeave" type FComponentEndTouchOverSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:638][ 40]LogJson: Warning: Property "OnInputTouchEnter" type FComponentBeginTouchOverSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:638][ 40]LogJson: Warning: Property "OnInputTouchEnd" type FComponentOnInputTouchEndSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:638][ 40]LogJson: Warning: Property "OnInputTouchBegin" type FComponentOnInputTouchBeginSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:638][ 40]LogJson: Warning: Property "OnReleased" type FComponentOnReleasedSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:638][ 40]LogJson: Warning: Property "OnClicked" type FComponentOnClickedSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:640][ 40]LogJson: Warning: Property "OnEndCursorOver" type FComponentEndCursorOverSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:640][ 40]LogJson: Warning: Property "OnBeginCursorOver" type FComponentBeginCursorOverSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:640][ 40]LogJson: Warning: Property "OnComponentPhysicsStateChanged" type FComponentPhysicsStateChanged unhandled during Json schema generation.
[2026.09.03-12.17.44:640][ 40]LogJson: Warning: Property "OnComponentSleep" type FComponentSleepSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:640][ 40]LogJson: Warning: Property "OnComponentWake" type FComponentWakeSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:640][ 40]LogJson: Warning: Property "OnComponentEndOverlap" type FComponentEndOverlapSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:640][ 40]LogJson: Warning: Property "OnComponentBeginOverlap" type FComponentBeginOverlapSignature unhandled during Json schema generation.
[2026.09.03-12.17.44:640][ 40]LogJson: Warning: Property "OnComponentHit" type FComponentHitSignature unhandled during Json schema generation.
```

One more tool error, from a call whose parameter names I got wrong, returned
verbatim and then corrected:

```
Function "find_nodes", input param "title" is required by the function input schema Json, but is missing from the incoming function input params Json.
```

**No compile error, no shader error, no validation failure, and nothing at all
from the saves.**

---

## Not verified

- **Nothing was looked at except the engine's cone thumbnail.** The torch itself
  has never been rendered. **Whether it looks like a torch is entirely unverified**
  — the geometry is four untextured primitives and the report only proves their
  boxes are where the arithmetic says.
- **BP_Torch has never been placed in a level or run in PIE.** Whether the light
  actually reproduces an existing PointLight in situ, and whether the flame reads
  as a flame, is unknown until it is placed. That is the next command.
- **`FlameBrightness 30` on an unlit emissive was not evaluated.** An emissive of
  `(1, 0.45, 0.12) × 30` is well above 1 and will bloom heavily depending on the
  PostProcessVolume's bloom settings, which were not inspected. It may read as a
  white blob rather than an orange flame. **This is the most likely thing to need
  tuning**, and it is exactly why the value was exposed as a parameter.
- **The Backplate sinks 2 units into the wall** at local X -52 vs the wall face at
  -50. Whether that matters depends on the wall, and no wall was tested against.
- **The torch hangs entirely below the actor origin**, so replacing each existing
  PointLight with a BP_Torch at the same coordinates will put the visible torch
  40 units *below* where the light currently is. The light itself stays exactly
  where it was. This is a consequence of the geometry as specified, not a
  deviation from it, but it is worth knowing before the placement command.
- **No check was made that the torch fits its surroundings.** It reaches 63 units
  into the room from the wall face; whether that clears railings, doors or the
  2F walkway at any of the 18 positions was not tested.
- **Backplate, Bracket and Cup keep `castShadow true`.** Only Flame was changed, as
  instructed. Eighteen shadow-casting torch bodies each wrapped around a
  shadow-casting light is a real cost that was not profiled.
- **The three engine-default event stubs were left in the graph.** They have no
  logic, and `bCanEverTick` is `false`, but they were not removed.
