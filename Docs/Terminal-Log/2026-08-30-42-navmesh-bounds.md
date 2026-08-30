# 2026-08-30 · Command 42 — NavMeshBoundsVolume over the playable area

Level change only, in `/Game/ThirdPerson/Lvl_ThirdPerson`. One
`NavMeshBoundsVolume` placed and scaled to cover the whole playable area.
**No Blueprint was edited.**

Target world bounds after scaling: min (-2100, -2100, -200), max (2100, 2100, 600) —
a 4200 x 4200 x 800 box centred at (0, 0, 200).

`AssetTools.is_dirty` was **not** called, per the instruction.

**Headline: every check passed, the bounds landed exactly on target with no error
anywhere, and the editor spawned a `RecastNavMesh` actor on its own. Nothing was
saved — see "Not saved".**

---

## Pre-flight

### P1 — `SceneTools.get_current_level`

```json
{"returnValue":"/Game/ThirdPerson/Lvl_ThirdPerson"}
```

**PASS.**

### P2 — `SceneTools.find_actors`, name `"Nav"` — the BEFORE picture

Called with `name` `"Nav"`, empty `tag`, empty `collision_channels`.
Every refPath returned:

```
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.AbstractNavData-Default
```

Raw return value:

```json
{"returnValue":[{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.AbstractNavData-Default"}]}
```

**PASS.** Exactly one actor, `AbstractNavData-Default`. No `RecastNavMesh` existed
before this command — that fact is what makes V3 readable.

### P3 — `ObjectTools.search_subclasses`, base `/Script/Engine.Actor`, filter `"NavMeshBoundsVolume"`

Every refPath returned:

```
/Script/NavigationSystem.NavMeshBoundsVolume
```

Raw return value:

```json
{"returnValue":[{"refPath":"/Script/NavigationSystem.NavMeshBoundsVolume"}]}
```

**PASS.** The list is not empty. Exactly one class, and `/Script/NavigationSystem.NavMeshBoundsVolume`
is the exact refPath used for the placement below — nothing was guessed.

### P4 — `ActorTools.get_actor_bounds` on the Floor

Actor: `/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.Floor_UAID_F4A475FF15A3736A02_1961940706`

```json
{"returnValue":{"min":{"x":-2000.001220703125,"y":-1999.999755859375,"z":-50.000030517578125},"max":{"x":2000.000244140625,"y":2000.000244140625,"z":0},"isValid":true}}
```

Exact numbers:

| | x | y | z |
|---|---|---|---|
| min | -2000.001220703125 | -1999.999755859375 | -50.000030517578125 |
| max | 2000.000244140625 | 2000.000244140625 | 0 |

`isValid: true`. **PASS.** About min (-2000, -2000, -50) max (2000, 2000, 0) as expected.
The X/Y values carry float tails of roughly 1e-3 to 2e-4 cm and Z max is exactly 0.

This confirms the premise behind the target numbers: the floor spans X/Y -2000..2000 with its
top at Z = 0, so padding the volume 100 past the floor edge gives the -2100..2100 span.

All four pre-flight checks passed.

---

## Place, measure, scale

### 1. `SceneTools.add_to_scene_from_class`

- `actor_type`: `/Script/NavigationSystem.NavMeshBoundsVolume` (the exact refPath from P3)
- `name`: `NavBounds_Main`
- `xform`: location (0, 0, 200), rotation (0, 0, 0), scale (1, 1, 1)
- `parent` unset, `snap_to_ground` **false**

Returned refPath:

```
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.NavMeshBoundsVolume_UAID_9C6B005AF86909FD02_1188892250
```

Not null, not nothing. The placement succeeded.

### 2. Measured bounds at scale 1

`ActorTools.get_actor_bounds` on the new actor, verbatim:

```json
{"returnValue":{"min":{"x":-100,"y":-100,"z":100},"max":{"x":100,"y":100,"z":300},"isValid":true}}
```

Computed sizes:

| | arithmetic | result |
|---|---|---|
| sizeX | `max.x - min.x` = `100 - (-100)` | **200** |
| sizeY | `max.y - min.y` = `100 - (-100)` | **200** |
| sizeZ | `max.z - min.z` = `300 - 100` | **200** |

**None of the three is 0**, so the STOP condition did not trigger. The default brush is a
clean 200 x 200 x 200 cube with no float tail at all, already centred on the actor location
(0, 0, 200) — the Z span 100..300 is that cube centred on Z = 200.

The measurement was taken rather than assumed, as instructed. Had the default been guessed at
the common 200-cube value it would have happened to be right, but that would not have been
evidence.

### 3. Computed scale factors

| | arithmetic | result |
|---|---|---|
| scaleX | `4200 / sizeX` = `4200 / 200` | **21** |
| scaleY | `4200 / sizeY` = `4200 / 200` | **21** |
| scaleZ | `800 / sizeZ` = `800 / 200` | **4** |

All three divide exactly, with no remainder and no floating-point residue. That is why V2
below lands on the target to the unit rather than merely within tolerance.

### 4. `ActorTools.set_actor_transform`

Applied with location (0, 0, 200), rotation (0, 0, 0), scale (21, 21, 4), `worldspace` **true**.

Returned boolean:

```json
{"returnValue":true}
```

### 5. Label and folder

`ActorTools.set_label` to exactly `NavBounds_Main`:

```json
{"returnValue":true}
```

`SceneTools.set_actor_folder` with `folder_path` `"Navigation"`:

```json
{"returnValue":null}
```

`set_actor_folder` declares no output schema, so `null` is what a completed call returns — it
is not a status value and is not evidence. The assignment was confirmed independently with
`SceneTools.get_actors_in_folder("Navigation", recursive=false)`:

```json
{"returnValue":[{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.NavMeshBoundsVolume_UAID_9C6B005AF86909FD02_1188892250"}]}
```

Exactly one actor in `Navigation`, and it is the volume just placed.

---

## Verify

### V1 — `get_actor_transform` on NavBounds_Main

Verbatim:

```json
{"returnValue":{"location":{"x":0,"y":0,"z":200},"rotation":{"pitch":0,"yaw":0,"roll":-0},"scale":{"x":21,"y":21,"z":4}}}
```

| | expected | measured | |
|---|---|---|---|
| location | (0, 0, 200) | (0, 0, 200) | **PASS** |
| rotation | (0, 0, 0) | pitch 0, yaw 0, roll -0 | **PASS** |
| scale | (21, 21, 4) | (21, 21, 4) | **PASS** |

**V1 PASS.** `roll: -0` is negative zero, which compares equal to `0` — a float sign bit, not
a rotation. The scale values are exact integers with no float tail, because 4200/200 and
800/200 divide cleanly.

### V2 — `get_actor_bounds` on NavBounds_Main

Verbatim:

```json
{"returnValue":{"min":{"x":-2100,"y":-2100,"z":-200},"max":{"x":2100,"y":2100,"z":600},"isValid":true}}
```

| | expected (±5) | measured | deviation | |
|---|---|---|---|---|
| min.x | -2100 | **-2100** | 0 | **PASS** |
| min.y | -2100 | **-2100** | 0 | **PASS** |
| min.z | -200 | **-200** | 0 | **PASS** |
| max.x | 2100 | **2100** | 0 | **PASS** |
| max.y | 2100 | **2100** | 0 | **PASS** |
| max.z | 600 | **600** | 0 | **PASS** |

**V2 PASS.** Not merely within the 5-unit tolerance — **exact on all six faces**, with
`isValid: true`. The box measures 4200 x 4200 x 800 centred at (0, 0, 200), which is the
target.

Against the P4 floor measurement, the volume overhangs the floor by about 99.999 cm on each
X/Y edge (the sub-centimetre shortfall is the floor's own float tail, not the volume's) and
spans Z -200..600, so it reaches 150 below the floor's underside at Z = -50 and 380 above the
door-test walls at Z = 220.

### V3 — `SceneTools.find_actors` name `"Nav"` again — the AFTER picture

Every refPath returned:

```
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.AbstractNavData-Default
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.NavMeshBoundsVolume_UAID_9C6B005AF86909FD02_1188892250
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default
```

Raw return value:

```json
{"returnValue":[{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.AbstractNavData-Default"},{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.NavMeshBoundsVolume_UAID_9C6B005AF86909FD02_1188892250"},{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default"}]}
```

Compared against P2:

| actor | in P2 (before) | in V3 (after) |
|---|---|---|
| `AbstractNavData-Default` | yes | yes — unchanged |
| `NavMeshBoundsVolume_..._1188892250` | no | yes — this command placed it |
| `RecastNavMesh_..._-Default` | **no** | **yes — appeared on its own** |

**V3 PASS**, in the sense that the comparison was made and reported. One went from one actor
to three.

### A RecastNavMesh actor DID appear

> **Yes. A `RecastNavMesh` actor appeared.** It is
> `/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default`,
> and it was **not** created by any call in this command.

P2 established that no `RecastNavMesh` existed before. The only actor this command created is
the `NavMeshBoundsVolume`. So the editor spawned the RecastNavMesh itself in response to a
nav bounds volume existing in the level — that is the navigation system building its data.

**This is not a failure and it is not an error.** The command stated in advance that either
outcome is informative and neither is a failure, and this is the outcome that indicates the
navigation system noticed the volume. Its `UAID` prefix `9C6B005AF86909FD02` is the same
session prefix as the volume's, which is consistent with it having been created in this
editor session rather than loaded from disk.

Nothing was done to it. It was not moved, renamed, foldered, or configured.

### V4 — `SceneTools.get_folders`

```json
{"returnValue":["DoorTest","Lighting","Navigation","Playground"]}
```

| expected | measured | |
|---|---|---|
| DoorTest, Lighting, Navigation, Playground | `["DoorTest","Lighting","Navigation","Playground"]` | **PASS** |

**V4 PASS.** Four folders, exactly the expected set. `Navigation` is new in this command;
`DoorTest` came from command 40; `Lighting` and `Playground` are the originals from the P6
reading in command 40.

### V5 — nothing else moved

`get_actor_transform` on `PlayerStart_UAID_F4A475FF15A3736A02_1961960731`, verbatim:

```json
{"returnValue":{"location":{"x":0,"y":0,"z":302.01264300000003},"rotation":{"pitch":0,"yaw":0,"roll":-0},"scale":{"x":1,"y":1,"z":1}}}
```

| | expected | measured | |
|---|---|---|---|
| PlayerStart location | (0, 0, 302.012643) | (0, 0, 302.01264300000003) | **PASS** |

The trailing `00000003` is the double representation of `302.012643`, which is not exactly
representable in binary floating point. It is the same stored value, not a movement.

`get_actors_in_folder("DoorTest", recursive=false)`:

```json
{"returnValue":[{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.StaticMeshActor_UAID_9C6B005AF86904FD02_1183964367"},{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.StaticMeshActor_UAID_9C6B005AF86904FD02_1188960368"},{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_Door_C_UAID_9C6B005AF86904FD02_1193627369"}]}
```

| | expected | measured | |
|---|---|---|---|
| DoorTest contents | exactly three actors | exactly three — Wall_L, Wall_R, Door_Test, same refPaths as command 40 | **PASS** |

**V5 PASS.** Nothing else moved.

### Verify summary

| check | result |
|---|---|
| V1 transform (0,0,200) / (21,21,4) | PASS |
| V2 bounds -2100..2100, -200..600 | PASS — exact, not just within 5 |
| V3 Nav actor scan, before vs after | PASS — RecastNavMesh appeared |
| V4 four folders | PASS |
| V5 PlayerStart and DoorTest untouched | PASS |

Five of five.

---

## Not saved

**Nothing was saved. No save call of any kind was made in this command.**
`SceneTools.save_actor` was not called. `AssetTools.save_assets` was not called. No third
route was attempted.

This was the instruction, and it was followed exactly. The reasoning given for it was
command 40's experience: `save_actor` on a newly placed actor errored with
`Asset does not exist:` because the external actor package did not yet exist.

> **The user must press Ctrl+S (Save Current Level) in the level editor to persist this
> volume.** Until then `NavBounds_Main` — and the `RecastNavMesh` actor the editor spawned
> alongside it — exist only in the loaded level in memory. Closing the editor without saving
> discards both.

One correction to the premise, recorded because it affects how much the user should trust the
"returns true while writing nothing" half of it. Command 40's report concluded that
`save_assets` wrote nothing. That conclusion was **wrong**. The three external actor packages
named in command 40's error messages
(`…/C/EB/M2R2969V25QR9HAZAO0DTH.uasset`, `…/C/8Q/388B6MQM912EX2BXH5U4GD.uasset`,
`…/5/D1/KK3E4BC1U33OGW1QTQUUOL.uasset`) are present on disk, timestamped 20:53:17, which is
when that `save_assets` call ran. The disk check performed immediately after that call
reported them absent; the timestamp says otherwise. Why the check and the timestamp disagree
is not known and is not guessed at here.

The `save_actor` half of the premise stands unchallenged — those three errors are quoted
verbatim in command 40's report and were real. And not saving here is harmless either way, so
the instruction was followed without argument.

---

## Untouched

No existing actor was modified. `Wall_L`, `Wall_R`, `Door_Test`, every `BP_ItemPickup`,
`SM_Ramp11` and the `PlayerStart` were never passed to any mutating call — the PlayerStart and
the DoorTest folder appear only in V5, which is a read. No Blueprint was edited; no Blueprint
tool was called at all in this command.

The `RecastNavMesh` actor that appeared was not touched either. It was observed in V3 and
otherwise left alone.

---

## Errors and warnings

**No error or warning was produced by any call in this command.** Every pre-flight check,
`add_to_scene_from_class`, both `get_actor_bounds` calls, `set_actor_transform`, `set_label`,
`set_actor_folder`, both `get_actors_in_folder` calls, both `find_actors` calls,
`get_folders`, and both `get_actor_transform` calls returned without a message.

There is therefore no error text to reproduce, translated or otherwise.

The editor's own Message Log and Output Log were **not** read as part of this command, so a
navigation-build warning that appeared only there — for instance about the RecastNavMesh
generation — would not have been captured here.

---

## Not confirmed

- **The volume is not on disk.** It exists only in the loaded level in memory, deliberately,
  per the instruction. So does the RecastNavMesh actor the editor spawned.
- **Navigation was never tested.** Nothing was run in PIE. No AI or navigation query was
  issued, no path was requested, and no agent walked the floor. That a RecastNavMesh actor
  exists is not the same as confirming the navmesh actually generated over the floor, covers
  the door gap, or is usable.
- **The navmesh was not viewed.** No viewport observation or screenshot was taken; the green
  navmesh overlay (the `P` key in the level viewport) was not checked. The geometry is
  confirmed by bounds arithmetic only.
- **Why the RecastNavMesh appeared is inferred, not measured.** P2 and V3 together prove it
  was not there before and is there now, and that this command created only the volume. That
  the navigation system spawned it in response to the volume is the reading of that evidence,
  not a separately observed event.
- The volume's own properties beyond its transform — for example whether it has a
  `NavigationSystem` agent filter set — were not read.
