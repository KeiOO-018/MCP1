# 2026-08-30 · Command 40 — Door test placement in Lvl_ThirdPerson

Level change only. Two `SM_Cube` wall boxes and one `BP_Door` instance placed in
`/Game/ThirdPerson/Lvl_ThirdPerson`. **No Blueprint was edited.**

`AssetTools.is_dirty` was **not** called, per the instruction.

**Headline: the placement and every geometric check succeeded, but the save did not.
All three `SceneTools.save_actor` calls returned errors, and nothing reached disk.
See "Save" and "Not confirmed".**

---

## Pre-flight

### P1 — `SceneTools.get_current_level`

```json
{"returnValue":"/Game/ThirdPerson/Lvl_ThirdPerson"}
```

**PASS.**

### P2 — `find_actors`, `actor_type = /Game/Interaction/BP_Door.BP_Door_C`

```json
{"returnValue":[]}
```

**PASS.** No BP_Door instance existed before this command.

### P3 — `find_actors` in bounds min (1150,-550,-20) max (1350,550,400)

Called with empty `name`, empty `tag`, empty `collision_channels`.
Every refPath returned, in full:

```
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.StaticMeshActor_UAID_F4A475FF15A3736A02_1961928692
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.Floor_UAID_F4A475FF15A3736A02_1961940706
```

Raw return value:

```json
{"returnValue":[{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.StaticMeshActor_UAID_F4A475FF15A3736A02_1961928692"},{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.Floor_UAID_F4A475FF15A3736A02_1961940706"}]}
```

Two actors only. The first has no descriptive name in its path, so its label was read with
`ActorTools.get_label` to confirm which actor it is:

```json
{"returnValue":"SM_SkySphere"}
```

**PASS.** The box contains only the SkySphere StaticMeshActor and the Floor. The site is clear.

### P4 — `StaticMeshTools.get_bounds` on `/Game/LevelPrototyping/Meshes/SM_Cube`

```json
{"returnValue":{"min":{"x":0,"y":0,"z":0},"max":{"x":100,"y":100,"z":100},"isValid":true}}
```

Exact numbers:

| | x | y | z |
|---|---|---|---|
| min | 0 | 0 | 0 |
| max | 100 | 100 | 100 |

`isValid: true`. **PASS.** The min is exactly the origin — no float tail at all, unlike SM_Door.
The corner-pivot assumption behind the placement arithmetic holds, so `location` is the min
corner and `scale * 100` is the size.

### P5 — `ObjectTools.get_properties` on `/Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE`

```json
{"RelativeScale3D":{"x":0.050000000000000003,"y":0.5,"z":1.1000000000000001}}
```

**PASS.** Reads about `(0.05, 0.5, 1.1)`, not `(1,1,1)`. Command 39 stuck.

### P6 — `SceneTools.get_folders`

```json
{"returnValue":["Lighting","Playground"]}
```

**PASS.** Two folders, `Lighting` and `Playground`. No `DoorTest` folder existed.

All six pre-flight checks passed. Proceeded to placement.

---

## Place

Three `SceneTools.add_to_scene_from_asset` calls, one actor at a time, each with
`parent` unset and `snap_to_ground` **false**. The refPath returned by each:

**1. Wall_L** — asset `/Game/LevelPrototyping/Meshes/SM_Cube`,
location (1200, -450, 0), rotation (0,0,0), scale (0.5, 4.0, 2.2)

```
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.StaticMeshActor_UAID_9C6B005AF86904FD02_1183964367
```

**2. Wall_R** — asset `/Game/LevelPrototyping/Meshes/SM_Cube`,
location (1200, 50, 0), rotation (0,0,0), scale (0.5, 4.0, 2.2)

```
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.StaticMeshActor_UAID_9C6B005AF86904FD02_1188960368
```

**3. Door_Test** — asset `/Game/Interaction/BP_Door`,
location (1225, -50, 110), rotation (0,0,0), scale (1,1,1)

```
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_Door_C_UAID_9C6B005AF86904FD02_1193627369
```

All three returned a refPath. None returned null or nothing.

### Labels

`ActorTools.set_label`, one call each:

| actor | label | return |
|---|---|---|
| StaticMeshActor_..._1183964367 | `Wall_L` | `{"returnValue":true}` |
| StaticMeshActor_..._1188960368 | `Wall_R` | `{"returnValue":true}` |
| BP_Door_C_..._1193627369 | `Door_Test` | `{"returnValue":true}` |

### Folders

`SceneTools.set_actor_folder` with `folder_path "DoorTest"`, one call each. All three
returned:

```json
{"returnValue":null}
```

`set_actor_folder` declares no output schema, so `null` is what a completed call returns —
it is not a status value. The assignment was therefore confirmed independently with
`SceneTools.get_actors_in_folder("DoorTest", recursive=false)`:

```json
{"returnValue":[{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.StaticMeshActor_UAID_9C6B005AF86904FD02_1183964367"},{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.StaticMeshActor_UAID_9C6B005AF86904FD02_1188960368"},{"refPath":"/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_Door_C_UAID_9C6B005AF86904FD02_1193627369"}]}
```

All three are in `DoorTest`, and no other actor is.

---

## Verify

### V1 — `get_actor_transform` on all three, verbatim

**Wall_L**

```json
{"returnValue":{"location":{"x":1200,"y":-450,"z":0},"rotation":{"pitch":0,"yaw":0,"roll":-0},"scale":{"x":0.5,"y":4,"z":2.2000000000000002}}}
```

| | expected | measured | |
|---|---|---|---|
| location | (1200, -450, 0) | (1200, -450, 0) | **PASS** |
| rotation | (0, 0, 0) | pitch 0, yaw 0, roll -0 | **PASS** |
| scale | (0.5, 4.0, 2.2) | (0.5, 4, 2.2000000000000002) | **PASS** |

**Wall_R**

```json
{"returnValue":{"location":{"x":1200,"y":50,"z":0},"rotation":{"pitch":0,"yaw":0,"roll":-0},"scale":{"x":0.5,"y":4,"z":2.2000000000000002}}}
```

| | expected | measured | |
|---|---|---|---|
| location | (1200, 50, 0) | (1200, 50, 0) | **PASS** |
| rotation | (0, 0, 0) | pitch 0, yaw 0, roll -0 | **PASS** |
| scale | (0.5, 4.0, 2.2) | (0.5, 4, 2.2000000000000002) | **PASS** |

**Door_Test**

```json
{"returnValue":{"location":{"x":1225,"y":-50,"z":110},"rotation":{"pitch":0,"yaw":0,"roll":-0},"scale":{"x":1,"y":1,"z":1}}}
```

| | expected | measured | |
|---|---|---|---|
| location | (1225, -50, 110) | (1225, -50, 110) | **PASS** |
| rotation | (0, 0, 0) | pitch 0, yaw 0, roll -0 | **PASS** |
| scale | (1, 1, 1) | (1, 1, 1) | **PASS** |

Two things in these numbers are worth naming rather than glossing over.
`roll: -0` is negative zero, which compares equal to `0` — it is a float sign bit, not a
rotation. `2.2000000000000002` is the double representation of `2.2`, which is not exactly
representable in binary floating point; it is the round-trip of the value sent, not drift.

### V2 — `get_actor_bounds` Wall_L

```json
{"returnValue":{"min":{"x":1200,"y":-450,"z":0},"max":{"x":1250,"y":-50,"z":220.00000000000003},"isValid":true}}
```

| | expected | measured | |
|---|---|---|---|
| min | about (1200, -450, 0) | (1200, -450, 0) | **PASS** |
| max | about (1250, -50, 220) | (1250, -50, 220.00000000000003) | **PASS** |

The `220.00000000000003` is `2.2000000000000002 * 100`. **V2 PASS.**

### V3 — `get_actor_bounds` Wall_R

```json
{"returnValue":{"min":{"x":1200,"y":50,"z":0},"max":{"x":1250,"y":450,"z":220.00000000000003},"isValid":true}}
```

| | expected | measured | |
|---|---|---|---|
| min | about (1200, 50, 0) | (1200, 50, 0) | **PASS** |
| max | about (1250, 450, 220) | (1250, 450, 220.00000000000003) | **PASS** |

**V3 PASS.** Wall_L ends at Y = -50 and Wall_R starts at Y = +50, so the doorway gap is
exactly the intended 100 cm, Y -50..+50.

### V4 — `get_components` on Door_Test, then its DoorMesh properties

Every refPath returned:

```
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_Door_C_UAID_9C6B005AF86904FD02_1193627369.DefaultSceneRoot
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_Door_C_UAID_9C6B005AF86904FD02_1193627369.BillboardComponent_6
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_Door_C_UAID_9C6B005AF86904FD02_1193627369.Hinge
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_Door_C_UAID_9C6B005AF86904FD02_1193627369.DoorMesh
```

**Four components, not the three on the class default object.** Command 39 recorded exactly
three on `Default__BP_Door_C` (`DefaultSceneRoot_GEN_VARIABLE`, `Hinge_GEN_VARIABLE`,
`DoorMesh_GEN_VARIABLE`). The placed instance additionally has `BillboardComponent_6`.
This is not a change to the Blueprint — the Blueprint was not edited — it is a component
present on the level instance that is absent from the CDO. It matters for V5 below.

`ObjectTools.get_properties` on the instance's DoorMesh for
`["RelativeLocation","RelativeScale3D"]`:

```json
{"RelativeLocation":{"x":0,"y":50,"z":0},"RelativeScale3D":{"x":0.050000000000000003,"y":0.5,"z":1.1000000000000001}}
```

| | expected | measured | |
|---|---|---|---|
| RelativeLocation | about (0, 50, 0) | (0, 50, 0) | **PASS** |
| RelativeScale3D | (0.05, 0.5, 1.1) | (0.05..., 0.5, 1.1...) | **PASS** |

**V4 PASS.**

### The ConstructionScript offset — first observation

> **`DoorMesh.RelativeLocation` on the placed instance reads exactly `(0, 50, 0)`.**

This is the first time the BP_Door ConstructionScript has ever been observed running. Until
now the `100 * ScaleY` offset was only ever *derived* from the DSL — command 39 recorded it
explicitly as not confirmed, because the script had never been seen to execute.

The chain now closes end to end:

- the DSL computes `MakeVector(0.0, 100.0 * DoorMesh.RelativeScale3D.y * sign)`
- `bHingeOnRight` is `false`, so the `select` yields `1.0`
- `ScaleY` is exactly `0.5` (exactly representable, no float tail)
- therefore Y = `100.0 * 0.5 * 1.0` = exactly `50`

and the measured value is exactly `50`, with X and Z exactly `0`. Not "about 50" — exactly.
The hinge axis sits on the Y = -50 jamb and the leaf fills the doorway toward Y = +50, which
is the intended geometry.

### V5 — `get_actor_bounds` Door_Test

```json
{"returnValue":{"min":{"x":1097,"y":-178,"z":-18},"max":{"x":1353,"y":78,"z":238},"isValid":true}}
```

| | expected | measured | |
|---|---|---|---|
| min | about (1220, -50, 0) | (1097, -178, -18) | **FAIL** |
| max | about (1230, 50, 220) | (1353, 78, 238) | **FAIL** |

**V5 FAIL as stated.** The measured box is far larger than the door leaf in every axis.

What the numbers are: the box is 256 x 256 x 256 (1353-1097 = 256, 78-(-178) = 256,
238-(-18) = 256) and it is centred exactly on the actor location (1225, -50, 110), with a
128 cm half-extent on each axis. A perfect cube centred on the actor pivot is not any
door-leaf shape; a 10 x 100 x 220 leaf could not produce it.

The likely cause is the extra `BillboardComponent_6` found in V4: `get_actor_bounds` returns
the union of all component bounds, and an editor billboard sprite contributes a fixed-size
box around the actor origin regardless of what the mesh does. That is a **hypothesis** — it
was not tested, because testing it would mean touching the actor, and no component-level
bounds tool exists in this toolset. What is certain from the measurement alone is that the
returned box is dominated by something other than the door leaf, so **V5 does not measure the
leaf and cannot confirm or deny its position either way.**

V7 below does measure the leaf, and it lands where V5 was supposed to show it.

### V6 — `ObjectTools.get_properties` on the Door_Test ACTOR

```json
{"bLocked":true,"bOpen":false,"bHingeOnRight":false,"OpenAngle":90,"SwingSpeed":1,"RequiredKey":{"dataTable":{"refPath":"/Game/Inventory/DT_Items.DT_Items"},"rowName":"Key_Stage1"}}
```

| property | expected | measured | |
|---|---|---|---|
| bLocked | true | `true` | **PASS** |
| bOpen | false | `false` | **PASS** |
| bHingeOnRight | false | `false` | **PASS** |
| OpenAngle | 90 | `90` | **PASS** |
| SwingSpeed | 1 | `1` | **PASS** |
| RequiredKey | DT_Items / Key_Stage1 | dataTable `/Game/Inventory/DT_Items.DT_Items`, rowName `Key_Stage1` | **PASS** |

**V6 PASS.** None of these were changed; they were read only.

### V7 — `SceneTools.trace_world` (1225, 0, 1000) to (1225, 0, -100)

```json
{"returnValue":780}
```

| expected | measured | |
|---|---|---|
| about 780 (hit leaf top at Z=220) | `780` | **PASS** |

**V7 PASS, and it is the "hit the leaf" outcome, not the "through to the floor" outcome.**
The trace starts at Z = 1000 and travels down, so a distance of 780 puts the hit at
Z = 1000 - 780 = **220**, exactly the top of the leaf. It is not about 1000, so the trace did
not pass through to the plaza floor — the leaf has collision there.

This is the measurement V5 failed to provide. The trace runs down the line X = 1225, Y = 0.
Y = 0 is inside the doorway gap (Y -50..+50) and outside both walls, so no wall could have
been hit; X = 1225 is inside the leaf's X span 1220..1230. Something solid is at
(1225, 0, 220) and only the door leaf can be there. The leaf is therefore positioned and
collidable as intended, independently of what `get_actor_bounds` reported.

### Verify summary

| check | result |
|---|---|
| V1 transforms, all three | PASS |
| V2 Wall_L bounds | PASS |
| V3 Wall_R bounds | PASS |
| V4 components + DoorMesh RelativeLocation `(0,50,0)` | PASS |
| V5 Door_Test actor bounds | **FAIL** (box dominated by a non-leaf component; does not measure the leaf) |
| V6 door variables | PASS |
| V7 trace, 780 | PASS |

---

## Save

**All three `SceneTools.save_actor` calls failed.** Each returned an error, not a value.
Exact English text, untranslated and uncleaned:

Wall_L:

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/EB/M2R2969V25QR9HAZAO0DTH
Failed to save 'Wall_L'.
```

Wall_R:

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/8Q/388B6MQM912EX2BXH5U4GD
Failed to save 'Wall_R'.
```

Door_Test:

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/5/D1/KK3E4BC1U33OGW1QTQUUOL
Failed to save 'Door_Test'.
```

The second and third calls were not retries of the first — they are the three separate calls
the command specified, made once each. Nothing was retried.

`AssetTools.save_assets` on `["/Game/ThirdPerson/Lvl_ThirdPerson"]`:

```json
{"returnValue":true}
```

### That `true` is not evidence, and here it is demonstrably wrong

The three external actor packages named in the errors were checked on disk. None exists:

```
ls: cannot access 'Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/EB/': No such file or directory
ls: cannot access 'Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/8Q/': No such file or directory
ls: cannot access 'Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/5/D1/': No such file or directory
```

`Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson` holds 71 `.uasset` files, and
**none of them has a modification time on or after 2026-08-30** — the directory is untouched
by this command.

`git status --porcelain` after the whole sequence:

```
 M Content/Interaction/BP_Door.uasset
?? Docs/Terminal-Log/2026-08-30-39-door-mesh-scale.md
```

The only modified asset is `BP_Door.uasset` from command 39. No new external actor package,
and `Content/ThirdPerson/Lvl_ThirdPerson.umap` is not modified either.

So `save_assets` returned `true` while writing nothing for these actors. This is a fresh
instance of the standing project observation that a `unreal-mcp` return value is not
evidence, and a sharper one than usual: the failure is not a null-where-true-was-expected,
it is a **`true` where the work did not happen**.

The three actors exist and verify correctly in the loaded level **in memory only**. They are
unsaved. Closing the editor without saving them by hand would discard the entire placement.
Nothing was retried and no workaround was attempted, per the instruction not to retry blind.

---

## Untouched

No existing actor was modified. In particular `BP_ItemPickup2` (the Key_Stage1 pickup at
(840, 1130, 0)), the other `BP_ItemPickup` actors, `SM_Ramp11` and the `PlayerStart` were
never passed to any call in this command. No Blueprint was edited — every call in the
placement and verify phases targeted level actors or read-only queries, except the two reads
of the Blueprint CDO in P5, which were `get_properties` and wrote nothing.

---

## Errors and warnings

Every error encountered, exact English text, untranslated and uncleaned:

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/EB/M2R2969V25QR9HAZAO0DTH
Failed to save 'Wall_L'.
```

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/C/8Q/388B6MQM912EX2BXH5U4GD
Failed to save 'Wall_R'.
```

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/5/D1/KK3E4BC1U33OGW1QTQUUOL
Failed to save 'Door_Test'.
```

No other error or warning was produced. Every pre-flight check, every
`add_to_scene_from_asset`, every `set_label`, every `set_actor_folder`, and every verify call
completed without a message. The editor's own Message Log and Output Log were not read as
part of this command, so a warning that appeared only there would not have been captured.

---

## Not confirmed

- **The placement is not on disk.** The three actors live only in the loaded level in memory.
  All three `save_actor` calls errored and the external actor packages do not exist. This is
  the one thing in this command that failed outright.
- **V5 did not measure the door leaf.** `get_actor_bounds` on Door_Test returned a 256 cm
  cube centred on the actor pivot. The billboard-component explanation is a hypothesis, not a
  tested finding.
- **Nothing was run in PIE.** The door was never opened, `bLocked` was never exercised, and
  the `RequiredKey` check against `DT_Items / Key_Stage1` was never executed. `bOpen` was read
  as `false` and left there.
- **The scene was not viewed.** No screenshot or viewport observation was taken; the geometry
  is confirmed by transforms, bounds and one downward trace, not visually.
- The `OpenAngle` of 90 and `SwingSpeed` of 1 were read but never applied to anything.
