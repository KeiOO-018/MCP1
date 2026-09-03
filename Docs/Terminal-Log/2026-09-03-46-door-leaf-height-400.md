# 2026-09-03 · Command 46 — Make the door leaves match the 400-tall doorways

Blueprint change (saved to disk) plus a level change (not saved), in
`/Game/Interaction/BP_Door` and `/Game/ThirdPerson/Lvl_Stage`.

**STEP 1 succeeded and is on disk. STEP 2 succeeded. STEP 3 FAILED — the class
default cannot be pushed onto the four level instances with any tool this MCP
server exposes. The remedy STEP 3 prescribes was attempted on all four doors and
did not take. As a result 12 of the 20 verification traces return null, and the
doors are now in a WORSE state than before this command: each leaf still spans
only 200 units, but sits 100 higher, so there is now an open 100-unit gap under
every door as well as the 100-unit gap above it.**

Instruction, verbatim from the user:

> In the currently open level /Game/ThirdPerson/Lvl_Stage, make the door leaves match the
> doorways that were just raised to 400 units tall.
>
> Background you need for the numbers: BP_Door's DoorMesh component uses the static mesh
> SM_Door (/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door). SM_Door is a
> 200 x 200 x 200 box whose pivot is at its CENTER, not at a corner. The leaf is centered
> on the door actor's origin, so doubling the mesh's Z scale and raising the actor by 100
> turns a leaf that spans Z 0..200 into one that spans Z 0..400.
>
> STEP 1 - Edit the Blueprint class default.
>
>   1a) Open the Blueprint /Game/Interaction/BP_Door. On its DoorMesh component, change
>       RelativeScale3D from (0.05, 0.5, 1.0) to (0.05, 0.5, 2.0).
>       Do NOT change RelativeLocation, which must stay (0, 50, 0).
>       Do NOT change the StaticMesh, the Hinge component, any variable, or any graph.
>   1b) Compile the Blueprint. Report the compile result verbatim.
>   1c) Save the Blueprint asset to disk, and confirm it was written.
>
> STEP 2 - Raise the four door actors in the level by 100 units. Change ONLY the Z of the
> location. Keep X, Y, rotation and scale exactly as they are.
>
>   2a) Door_R1     from (-400, -1500, 100) to (-400, -1500, 200). Rotation yaw -90, scale (1, 2, 1).
>   2b) Door_R2     from (1200,  -100, 100) to (1200,  -100, 200). Rotation yaw   0, scale (1, 2, 1).
>   2c) Door_R3     from (-400,  1500, 100) to (-400,  1500, 200). Rotation yaw -90, scale (1, 2, 1).
>   2d) Door_Final  from (1200,  -100, 700) to (1200,  -100, 800). Rotation yaw   0, scale (1, 2, 1).
>
> STEP 3 - Confirm the class default actually reached every instance. On EACH of the four
> door actors, read back the DoorMesh component's RelativeScale3D. If any of them still
> reads (0.05, 0.5, 1.0), that instance had an override, so set (0.05, 0.5, 2.0) directly
> on that instance and say in the report which instances needed it.
>
> DO NOT touch any wall, floor, ramp, railing, pillar, enemy, item pickup, BP_StageRoom,
> BP_EndTrigger or the GameMode.
>
> VERIFY AND REPORT.
>
>   A) For each of the four door actors report: world location, rotation, actor scale, and
>      the DoorMesh component's RelativeLocation and RelativeScale3D.
>
>   B) Run these line traces with SceneTools.trace_world and report the returned distance
>      for every one of them. A number near 195 means the leaf is blocking. A null means
>      there is still a hole.
>
>      Room 1 doorway,  for z = 30, 150, 250, 350, 390:
>        start (-300, -1300, z)  end (-300, -1700, z)
>      Room 3 doorway,  for z = 30, 150, 250, 350, 390:
>        start (-300,  1300, z)  end (-300,  1700, z)
>      Room 2 doorway,  for z = 30, 150, 250, 350, 390:
>        start (1000,     0, z)  end (1400,     0, z)
>      Final doorway,   for z = 630, 750, 850, 950, 990:
>        start (1000,     0, z)  end (1400,     0, z)
>
>      All 20 traces are expected to return a distance near 195, and none of them is
>      expected to return null.
>
>   C) Report the total actor count in the level.
>
>   D) Report any warning or error text verbatim in English. Do not summarize or translate.
>
> Write the report to Docs/Terminal-Log/2026-09-03-46-door-leaf-height-400.md
> (a repo path - do NOT write under Saved/, it is gitignored).

---

## A correction to a premise in the instruction

The instruction says of the Blueprint's DoorMesh component: "Do NOT change
RelativeLocation, which must stay (0, 50, 0)."

**On the class default, RelativeLocation is not (0, 50, 0). It is (0, 0, 0).**
Read before any edit was made:

```json
["/Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE",
 "{\"RelativeLocation\":{\"x\":0,\"y\":0,\"z\":0},
   \"RelativeScale3D\":{\"x\":0.050000000000000003,\"y\":0.5,\"z\":1},
   \"RelativeRotation\":{\"pitch\":0,\"yaw\":0,\"roll\":0},
   \"StaticMesh\":{\"refPath\":\"/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door.SM_Door\"}}"]
```

`(0, 50, 0)` is what the **four level instances** carry. So that value is a
per-instance override on every door, not a class default. Since the instruction
was "do not change it", nothing was changed in either place — the class default
is still `(0, 0, 0)` and all four instances are still `(0, 50, 0)`. This is
recorded because it is the first hard evidence that these four instances **do**
carry per-component overrides, which turns out to be the whole story of STEP 3.

---

## STEP 1 — Blueprint class default

### 1a — the write

`ObjectTools.set_properties` on
`/Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE`, values
`{"RelativeScale3D":{"x":0.05,"y":0.5,"z":2.0}}`.

```json
{"returnValue":true}
```

**PASS, and confirmed by read-back** (see 1d below). Nothing else was sent. The
StaticMesh, the Hinge component, every variable and every graph were left
untouched — no other tool was called against the Blueprint.

### 1b — compile, verbatim

`BlueprintTools.compile_blueprint`, `warnings_as_errors: false`:

```json
{"returnValue":null}
```

The tool returns `null` on success and does not return the compiler's text. The
compiler's own output in the editor log is exactly one line, reproduced verbatim
and in full:

```
[2026.09.03-09.51.57:161][706]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Door.BP_Door'
```

**There is no other `LogBlueprint` line in the entire session log.** No compile
error, no compile warning, no "Failed to compile" line. Filtering the whole log
for `LogBlueprint` returns that single entry and nothing else.

**Not obtained:** the Blueprint's `Status` enum (`BS_UpToDate` /
`BS_UpToDateWithWarnings` / `BS_Error`) could not be read back as independent
confirmation. `ObjectTools.get_properties` resolves a Blueprint path to its CDO
automatically — as its own documentation states — so the request landed on the
CDO, which has no `Status` property, and returned this error verbatim:

```
GetObjectProperties on '/Game/Interaction/BP_Door.Default__BP_Door_C' (BP_Door_C): the following properties could not be read: Status
```

So "compiled clean" rests on the absence of any compiler diagnostic in the log
plus the successful CDO read-back in 1d, not on a status enum.

### 1c — save, and proof it was written

`AssetTools.is_dirty` before saving:

```json
{"returnValue":true}
```

`AssetTools.save_assets` with `["/Game/Interaction/BP_Door"]`:

```json
{"returnValue":true}
```

`AssetTools.is_dirty` after saving:

```json
{"returnValue":false}
```

Confirmed independently on disk, outside the editor:

| | Before | After |
|---|---|---|
| mtime | `2026-09-03 15:47:57.378218100 +0900` | `2026-09-03 18:52:19.928953200 +0900` |
| size | 144793 bytes | 144828 bytes |

`git status --porcelain` now reports:

```
 M Content/Interaction/BP_Door.uasset
```

**PASS on four independent grounds:** the dirty flag cleared, the mtime advanced,
the file size changed, and git sees the modification. The file really was
written.

### 1d — read-back of the class default

```json
"cdo_DoorMesh": "{\"RelativeLocation\":{\"x\":0,\"y\":0,\"z\":0},
                  \"RelativeScale3D\":{\"x\":0.050000000000000003,\"y\":0.5,\"z\":2},
                  \"StaticMesh\":{\"refPath\":\"/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door.SM_Door\"}}"
```

**PASS.** Z is 2. X is unchanged at 0.05 (stored as `0.050000000000000003`, the
same double it held before — this is the pre-existing representation of 0.05, not
drift introduced here). Y unchanged at 0.5. RelativeLocation untouched at
`(0, 0, 0)`. StaticMesh still SM_Door.

**STEP 1 is complete and correct.**

---

## STEP 2 — raise the four door actors by 100 in Z

`ActorTools.set_actor_transform`, `worldspace: true`, once per actor.

Rotation and scale were **not** re-typed from the instruction. For each actor the
current transform was read first and the exact returned `rotation` and `scale`
objects were sent back alongside the new location:

```python
old = get_xform(ref)
xf = {"location": {"x": tgt[0], "y": tgt[1], "z": tgt[2]},
      "rotation": old["rotation"], "scale": old["scale"]}
```

This matters here: Door_R1 and Door_R3 carry yaw `-90.00000000000001`, not `-90`.
Typing the instruction's `-90` would have silently changed their rotation. The
script also refused to write any actor whose starting location did not match the
instruction's "from" value; `skipped` came back empty, so all four matched.

Raw result:

| Label | set returned | from | to | rot unchanged | scale unchanged |
|---|---|---|---|---|---|
| `Door_R1` | `true` | (-400, -1500, 100) | (-400, -1500, 200) | `true` | `true` |
| `Door_R2` | `true` | (1200, -100, 100) | (1200, -100, 200) | `true` | `true` |
| `Door_R3` | `true` | (-400, 1500, 100) | (-400, 1500, 200) | `true` | `true` |
| `Door_Final` | `true` | (1200, -100, 700) | (1200, -100, 800) | `true` | `true` |

`skipped: []`. **PASS.** All four moved exactly 100 in Z, X and Y unchanged,
rotation and scale byte-identical to their pre-write values.

---

## STEP 3 — FAILED. The class default did not reach a single instance

### The read-back that triggered STEP 3

All four instances still read `z: 1`:

```json
"Door_R1"    RelativeScale3D {"x":0.050000000000000003,"y":0.5,"z":1}
"Door_R2"    RelativeScale3D {"x":0.050000000000000003,"y":0.5,"z":1}
"Door_R3"    RelativeScale3D {"x":0.050000000000000003,"y":0.5,"z":1}
"Door_Final" RelativeScale3D {"x":0.050000000000000003,"y":0.5,"z":1}
```

**All four instances needed the STEP 3 remedy.** Not one of them picked up the
class default, even though the Blueprint had already been compiled and saved, and
even though STEP 2 had since written each actor's transform (which normally
reruns construction scripts).

### The remedy was attempted on all four and did not take

`ObjectTools.set_properties` on each instance's DoorMesh, values
`{"RelativeScale3D":{"x":0.05,"y":0.5,"z":2.0}}`:

```json
"Door_R1":    {"set_returned": true, "after": "...\"RelativeScale3D\":{\"x\":0.050000000000000003,\"y\":0.5,\"z\":1}..."}
"Door_R2":    {"set_returned": true, "after": "...\"RelativeScale3D\":{\"x\":0.050000000000000003,\"y\":0.5,\"z\":1}..."}
"Door_R3":    {"set_returned": true, "after": "...\"RelativeScale3D\":{\"x\":0.050000000000000003,\"y\":0.5,\"z\":1}..."}
"Door_Final": {"set_returned": true, "after": "...\"RelativeScale3D\":{\"x\":0.050000000000000003,\"y\":0.5,\"z\":1}..."}
```

**`set_properties` returned `true` four times and changed nothing.** This is the
exact failure mode `CLAUDE.md` warns about: the MCP return value is not evidence.
A fresh read in a separate tool call, after the script had ended, confirmed the
instances were still at `z: 1` while the CDO template read `z: 2` — so the read
path is fine and it is the write that is not landing.

### What else was tried, in order, and what each returned

**1. `ObjectTools.reset_properties`** (the documented tool for "removing any
per-instance overrides"), on Door_R2's DoorMesh, `properties: ["RelativeScale3D"]`:

```json
{"returnValue":true}
```

Read-back:

```json
{"RelativeScale3D":{"x":1,"y":0.5,"z":1},"RelativeLocation":{"x":0,"y":50,"z":0}}
```

This **did** write, but incoherently: X went 0.05 → 1, while Y stayed 0.5 and Z
stayed 1. It reset toward the native `SceneComponent` default of `(1,1,1)`, not
toward the Blueprint archetype `(0.05, 0.5, 2)`, and it only moved one component
of the vector. This left Door_R2 wrong, and repairing it is what produced the
next observation.

**2. `set_properties` again on Door_R2** with `(0.05, 0.5, 2.0)`:

```json
{"returnValue":true}
```

Read-back:

```json
{"RelativeScale3D":{"x":0.050000000000000003,"y":0.5,"z":1},"RelativeLocation":{"x":0,"y":50,"z":0}}
```

X came back to 0.05, Z stayed 1. At this point the working hypothesis was "only
the X component of the vector is ever written". **Door_R2 was now back in line
with the other three, so the reset damage was undone.**

**3. camelCase key.** `ObjectTools.list_properties` on the component shows the
canonical names are camelCase (`relativeLocation`, `relativeRotation`,
`relativeScale3D`, `staticMesh`), so the write was retried with
`{"relativeScale3D":{"x":0.05,"y":0.5,"z":2.0}}`:

```json
{"returnValue":true}
```

Read-back: still `{"x":0.050000000000000003,"y":0.5,"z":1}`. **Key casing is not
the cause.**

**4. The decisive controlled probe.** Two writes on the same Door_R2 DoorMesh
component, each read back and each restored:

| Step | Result |
|---|---|
| `bVisible` baseline | `{"bVisible":true}` |
| set `bVisible` false | `true` |
| `bVisible` after | `{"bVisible":false}` ← **the write landed** |
| restore `bVisible` true | `true` |
| `bVisible` restored | `{"bVisible":true}` ← **restored** |
| `RelativeScale3D` baseline | `{"x":0.050000000000000003,"y":0.5,"z":1}` |
| set `(0.05, 0.9, 1.0)` — Y probe | `true` |
| `RelativeScale3D` after | `{"x":0.050000000000000003,"y":0.5,"z":1}` ← **unchanged** |
| restore `(0.05, 0.5, 1.0)` | `true` |
| `RelativeScale3D` restored | `{"x":0.050000000000000003,"y":0.5,"z":1}` |

This settles it. `set_properties` **does** write to this component — `bVisible`
flipped and flipped back. But a `RelativeScale3D` write does not land, and the Y
probe did not land either, which **falsifies** the "only X is written"
hypothesis from step 2. The X value returning to 0.05 in step 2 was therefore not
this tool's write succeeding; it was the value being restored from the actor's
cached per-instance component data after `reset_properties` disturbed it.

**Conclusion, stated as a finding rather than a theory:** on a Blueprint
component instance in this level, `ObjectTools.set_properties` writes ordinary
properties but silently refuses `RelativeScale3D`, returning `true` either way.
`ObjectTools.reset_properties` writes a partial, wrong value. No log line is
emitted for any of these — see section D.

### Every tool that exists for this, and why none of them can do it

`ActorTools` was enumerated in full. It has `set_actor_transform`, which takes an
**Actor**, not a SceneComponent, and there is no `set_component_transform`
anywhere in the toolset. `PrimitiveTools` only **adds** new primitive components.
`SceneTools` has no component-transform entry point. `ObjectTools.set_properties`
is the only write path to a component property that this server exposes, and it
is the one demonstrated above not to work for this property.

**So the remedy STEP 3 prescribes cannot be carried out with this MCP server.**
Two routes that would work were deliberately not taken, because both are outside
what this command authorized:

- **Delete and re-add the four door actors** so they rebuild from the corrected
  class. The instruction forbids touching anything outside the doors, and
  deleting them would discard each door's per-instance Blueprint state (the lock
  and interaction variables set up in commands 35–38). Not done.
- **Reload the level**, which rebuilds every actor from its class. This would
  **discard the entire unsaved wall change from command 45** — all 101 actors are
  still dirty in memory. Not done. See "What I recommend" below.

---

## A) The four door actors, final state

Every figure below is a fresh read after all edits.

### Door_R1

| Field | Value |
|---|---|
| Internal name | `BP_Door_C_UAID_9C6B005AF86926FE02_1375958439` |
| World location | `(-400, -1500, 200)` |
| Rotation | `(pitch 0, yaw -90.00000000000001, roll 0)` |
| Actor scale | `(1, 2, 1)` |
| DoorMesh RelativeLocation | `(-1.4210854715202004e-14, 50.000000000000014, 0)` |
| DoorMesh RelativeScale3D | **`(0.050000000000000003, 0.5, 1)`** — should be 2 |
| DoorMesh StaticMesh | `/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door.SM_Door` |
| Actor bounds | min `(-528, -1628, 72)` max `(-199.99998474121082, -1372, 328)` |

### Door_R2

| Field | Value |
|---|---|
| Internal name | `BP_Door_C_UAID_9C6B005AF86926FE02_1375967440` |
| World location | `(1200, -100, 200)` |
| Rotation | `(0, 0, 0)` |
| Actor scale | `(1, 2, 1)` |
| DoorMesh RelativeLocation | `(0, 50, 0)` |
| DoorMesh RelativeScale3D | **`(0.050000000000000003, 0.5, 1)`** — should be 2 |
| DoorMesh StaticMesh | `/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door.SM_Door` |
| Actor bounds | min `(1072, -228, 72)` max `(1328, 100.00001525878906, 328)` |

Door_R2 is the actor the diagnostic probes were run against. Its final
`RelativeScale3D`, `RelativeLocation`, `RelativeRotation`, `StaticMesh` and
`bVisible` were all read back and are identical to the other three doors. **No
residual damage from the probes.**

### Door_R3

| Field | Value |
|---|---|
| Internal name | `BP_Door_C_UAID_9C6B005AF86926FE02_1376293441` |
| World location | `(-400, 1500, 200)` |
| Rotation | `(pitch 0, yaw -90.00000000000001, roll 0)` |
| Actor scale | `(1, 2, 1)` |
| DoorMesh RelativeLocation | `(-1.4210854715202004e-14, 50.000000000000014, 0)` |
| DoorMesh RelativeScale3D | **`(0.050000000000000003, 0.5, 1)`** — should be 2 |
| DoorMesh StaticMesh | `/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door.SM_Door` |
| Actor bounds | min `(-528, 1372, 72)` max `(-199.99998474121082, 1628, 328)` |

### Door_Final

| Field | Value |
|---|---|
| Internal name | `BP_Door_C_UAID_9C6B005AF86932FE02_1830770592` |
| World location | `(1200, -100, 800)` |
| Rotation | `(0, 0, 0)` |
| Actor scale | `(1, 2, 1)` |
| DoorMesh RelativeLocation | `(0, 50, 0)` |
| DoorMesh RelativeScale3D | **`(0.050000000000000003, 0.5, 1)`** — should be 2 |
| DoorMesh StaticMesh | `/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door.SM_Door` |
| Actor bounds | min `(1072, -228, 672)` max `(1328, 100.00001525878906, 928)` |

The `-1.4210854715202004e-14` and `50.000000000000014` on R1 and R3 are
pre-existing float residue from their -90 yaw, present in the pre-edit read and
unchanged by this command. Likewise `100.00001525878906` in the bounds.

---

## B) The 20 line traces

`SceneTools.trace_world`. Every returned value is reproduced; none is rounded.

### Room 1 doorway — start `(-300, -1300, z)` end `(-300, -1700, z)`

| z | distance | verdict |
|---|---|---|
| 30 | `null` | **HOLE** |
| 150 | `195.00001525878906` | blocking |
| 250 | `195.00001525878906` | blocking |
| 350 | `null` | **HOLE** |
| 390 | `null` | **HOLE** |

### Room 3 doorway — start `(-300, 1300, z)` end `(-300, 1700, z)`

| z | distance | verdict |
|---|---|---|
| 30 | `null` | **HOLE** |
| 150 | `195.00001525878906` | blocking |
| 250 | `195.00001525878906` | blocking |
| 350 | `null` | **HOLE** |
| 390 | `null` | **HOLE** |

### Room 2 doorway — start `(1000, 0, z)` end `(1400, 0, z)`

| z | distance | verdict |
|---|---|---|
| 30 | `null` | **HOLE** |
| 150 | `195` | blocking |
| 250 | `195` | blocking |
| 350 | `null` | **HOLE** |
| 390 | `null` | **HOLE** |

### Final doorway — start `(1000, 0, z)` end `(1400, 0, z)`

| z | distance | verdict |
|---|---|---|
| 630 | `null` | **HOLE** |
| 750 | `195` | blocking |
| 850 | `195` | blocking |
| 950 | `null` | **HOLE** |
| 990 | `null` | **HOLE** |

**Result: 8 of 20 traces return a distance near 195. 12 of 20 return null. The
expectation stated in the instruction — all 20 near 195, none null — is NOT met.**

The eight hits are all exactly `195` or `195.00001525878906`, so where the leaf
is present it is positioned correctly in X/Y. The pattern of hits and misses
matches the measured leaf extent precisely: with `RelativeScale3D.z` still 1, each
leaf is 200 tall and centred on the actor origin, so R1/R2/R3 span Z 100..300 and
Door_Final spans Z 700..900. z=150 and z=250 fall inside that band; z=30, 350 and
390 do not, and for the final door z=750 and z=850 fall inside while 630, 950 and
990 do not.

**This is the harm worth stating plainly.** Before this command the leaves spanned
Z 0..200 and sealed the bottom of each doorway. STEP 2 raised them 100 without
STEP 3 being able to stretch them, so they now span Z 100..300. The doorway is
400 tall, so there is now:

- an open gap at **Z 0..100 underneath every door**, which did not exist before, and
- an open gap at **Z 300..400 above every door**.

A character can see through, shoot through, and depending on capsule size may
walk under, the four doors that used to be closed at floor level.

---

## C) Total actor count

**101**, unchanged from the end of command 45. No actor was created and none was
deleted by this command. The count was read three separate times during this
command and was 101 every time.

---

## D) Warnings and errors, verbatim

Every warning and error emitted during this command, in full, untranslated and
unsummarized. All of them were produced by my own read calls; **none is a
compile diagnostic, and none reports the failed writes.**

From the first attempt to read component properties, before the reads were split
by component type (`StaticMesh` does not exist on a `SceneComponent` or a
`BillboardComponent`) — this aborted the call and returned no data:

```
GetObjectProperties on '/Game/Interaction/BP_Door.BP_Door_C:DefaultSceneRoot_GEN_VARIABLE' (SceneComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/Interaction/BP_Door.BP_Door_C:Hinge_GEN_VARIABLE' (SceneComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86932FE02_1830770592.DefaultSceneRoot' (SceneComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86932FE02_1830770592.BillboardComponent_1' (BillboardComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86932FE02_1830770592.Hinge' (SceneComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86926FE02_1375967440.DefaultSceneRoot' (SceneComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86926FE02_1375967440.BillboardComponent_1' (BillboardComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86926FE02_1375967440.Hinge' (SceneComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86926FE02_1375958439.DefaultSceneRoot' (SceneComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86926FE02_1375958439.BillboardComponent_1' (BillboardComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86926FE02_1375958439.Hinge' (SceneComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86926FE02_1376293441.DefaultSceneRoot' (SceneComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86926FE02_1376293441.BillboardComponent_1' (BillboardComponent): the following properties could not be read: StaticMesh
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Door_C_UAID_9C6B005AF86926FE02_1376293441.Hinge' (SceneComponent): the following properties could not be read: StaticMesh
```

From the attempt to read the Blueprint's compile `Status` (1b):

```
[2026.09.03-09.52.12:514][752]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Door.Default__BP_Door_C' (BP_Door_C): the following properties could not be read: Status
```

From `ObjectTools.list_properties` on the DoorMesh component, used to check the
canonical property-name casing — 22 warnings, all of the same kind, all about
delegate properties that the server's JSON schema generator cannot express:

```
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnComponentDeactivated" type FActorComponentDeactivateSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnComponentActivated" type FActorComponentActivatedSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "PhysicsVolumeChangedDelegate" type FPhysicsVolumeChanged unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnTouchExited" type FComponentOnTouchExitedSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnTouchEntered" type FComponentOnTouchEnteredSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnTouchEnded" type FComponentOnTouchEndedSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnTouchBegan" type FComponentOnTouchBeganSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnInputTouchLeave" type FComponentEndTouchOverSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnInputTouchEnter" type FComponentBeginTouchOverSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnInputTouchEnd" type FComponentOnInputTouchEndSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnInputTouchBegin" type FComponentOnInputTouchBeginSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnReleased" type FComponentOnReleasedSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnClicked" type FComponentOnClickedSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnEndCursorOver" type FComponentEndCursorOverSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnBeginCursorOver" type FComponentBeginCursorOverSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnComponentPhysicsStateChanged" type FComponentPhysicsStateChanged unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnComponentSleep" type FComponentSleepSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnComponentWake" type FComponentWakeSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnComponentEndOverlap" type FComponentEndOverlapSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnComponentBeginOverlap" type FComponentBeginOverlapSignature unhandled during Json schema generation.
[2026.09.03-09.55.07:013][379]LogJson: Warning: Property "OnComponentHit" type FComponentHitSignature unhandled during Json schema generation.
```

**The most important thing in this section is what is absent.** Filtering the
whole session log for `scale`, `construction`, `reinstanc`, `SetObjectProperties`,
`ResetObjectProperties` and `DoorMesh` returns **no entry at all** for any of the
six failed `set_properties` calls or the one wrong `reset_properties` call. They
failed silently, at both the tool-return level (`true`) and the log level
(nothing). There is no diagnostic anywhere that would have revealed this. It was
caught only by reading the value back.

---

## What changed on disk

```
 M Content/Interaction/BP_Door.uasset
?? "Docs/Spec/2026-09-03-\353\241\234\353\271\204-\354\244\221\354\204\270-\353\247\210\352\260\220.md"
?? Docs/Terminal-Log/2026-09-03-45-doorway-height-400.md
```

`Content/Interaction/BP_Door.uasset` is the only asset this command wrote, and
writing it was instruction 1c.

`Content/ThirdPerson/Lvl_Stage.umap` is **unchanged on disk**, mtime still
`2026-09-03 09:47:04.791203000 +0900`. **The level was not saved.** It still holds
101 actors in memory, carrying both command 45's wall changes and command 46's
door moves. All of that is lost if the editor closes without saving.

The two untracked files are a pre-existing Spec file and command 45's report.

---

## What I recommend, and what I did not do without asking

The Blueprint is correct and saved. The only thing standing between the current
state and the intended result is that the four level instances hold a stale
`RelativeScale3D` that no available tool will overwrite.

**Reloading the level would almost certainly fix all four at once**, because the
actors would be rebuilt from the now-corrected class. But reloading discards
every unsaved change in the level — which right now means the entire wall rework
from command 45. The safe order would be:

1. Save `Lvl_Stage` (persisting commands 45 and 46).
2. Reload the level.
3. Re-read all four `RelativeScale3D` values and re-run the 20 traces.

That saves the level, which no instruction so far has authorized, so it was not
done. **It is the user's call.**

**If the answer is no**, then STEP 2 should be reverted — the four doors put back
to Z 100, 100, 100 and 700 — because a raised 200-tall leaf in a 400-tall doorway
leaves a gap under every door and is worse than where this command started. That
revert was also not done unilaterally, because STEP 2 was an explicit
instruction.

---

## Not verified

- **PIE was not run.** Whether a character can actually walk under the raised
  leaves is unconfirmed; the traces show the geometry is open at Z 0..100, but
  capsule size and step height were not tested.
- **Nothing was looked at in the viewport.** Every figure here is from
  `get_actor_transform`, `get_actor_bounds`, `get_properties` and `trace_world`.
- **The BP_Door graph and variables were not inspected or touched.** The
  instruction forbade changing them and nothing was called against them, but no
  read was done to prove the graph is byte-identical either. The only Blueprint
  write in this command was the single `set_properties` call in 1a.
- **The eight successful traces prove the leaf blocks along Y or X at those
  heights; they do not prove the leaf fully fills the doorway width.** Only the
  five heights named in the instruction were traced, all along the doorway
  centre line.
- **`reset_properties` was called once, on Door_R2 only.** Its final state was
  read back and matches the other three doors on every property checked
  (`RelativeScale3D`, `RelativeLocation`, `RelativeRotation`, `StaticMesh`,
  `bVisible`). No other property of that component was compared against the
  other doors, so an untested property could in principle still differ.
