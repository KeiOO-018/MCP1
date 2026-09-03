# 2026-09-03 · Command 47 — Finish raising the door leaves, via actor scale

Blueprint change (saved) plus a level change (saved), in `/Game/Interaction/BP_Door`
and `/Game/ThirdPerson/Lvl_Stage`.

**All three steps succeeded. All 20 verification traces return a distance near 195
and none returns null — the result command 46 could not reach. The four door
leaves now span the full 400-tall doorway. No component property was touched. No
actor was created, deleted or re-created. Everything is on disk: 12 packages
written in total.**

Instruction, verbatim from the user:

> In the currently open level /Game/ThirdPerson/Lvl_Stage, finish raising the door leaves.
> Command 46 could not do it through the component; this command does it through the
> actor scale instead.
>
> Why: the leaf size is SM_Door (200 x 200 x 200, pivot centered) multiplied by the
> DoorMesh component scale (0.05, 0.5, 1.0) and then by the door actor's scale (1, 2, 1).
> Command 46 proved that ObjectTools.set_properties silently refuses to write
> RelativeScale3D on these component instances, but ActorTools.set_actor_transform does
> work on the actors. Setting the actor Z scale from 1 to 2 produces the same 400-tall
> leaf without touching any component.
>
> STEP 1 - Undo the class default change made by command 46, so it cannot take effect
> later if the per-instance overrides are ever cleared.
>
>   1a) Open /Game/Interaction/BP_Door. On its DoorMesh component, set RelativeScale3D
>       back to (0.05, 0.5, 1.0).
>   1b) Compile the Blueprint and report the result verbatim.
>   1c) Save the Blueprint asset and confirm it was written to disk.
>   1d) Read back the class default and confirm it now reads (0.05, 0.5, 1.0).
>
> STEP 2 - Set the actor scale on the four doors. Use ActorTools.set_actor_transform.
> Change ONLY the Z component of the scale, from 1 to 2. Keep location and rotation
> exactly as they are.
>
>   2a) Door_R1     location (-400, -1500, 200), rotation yaw -90, scale (1, 2, 1) -> (1, 2, 2)
>   2b) Door_R2     location (1200,  -100, 200), rotation yaw   0, scale (1, 2, 1) -> (1, 2, 2)
>   2c) Door_R3     location (-400,  1500, 200), rotation yaw -90, scale (1, 2, 1) -> (1, 2, 2)
>   2d) Door_Final  location (1200,  -100, 800), rotation yaw   0, scale (1, 2, 1) -> (1, 2, 2)
>
> DO NOT change any component property on any door. DO NOT delete or re-create any door
> actor - each one carries per-instance Blueprint state (bLocked, RequiredKey, tags) and
> three BP_StageRoom actors hold references to them. DO NOT reload the level: the wall
> changes from command 45 are still unsaved in memory.
>
> STEP 3 - Save. After the verification below passes, save the level so command 45's wall
> edits and this command's door edits both reach disk. Report which packages were written.
>
> VERIFY AND REPORT.
>
>   A) For each of the four doors report world location, rotation, actor scale, and the
>      DoorMesh component's RelativeLocation and RelativeScale3D. The component values are
>      expected to be UNCHANGED at RelativeLocation (0, 50, 0) and RelativeScale3D
>      (0.05, 0.5, 1.0) - this command deliberately does not touch them.
>
>   B) Run these line traces with SceneTools.trace_world and report the distance for each.
>      A number near 195 means the leaf is blocking. A null means a hole is still there.
>
>      Room 1 doorway, for z = 30, 150, 250, 350, 390:
>        start (-300, -1300, z)  end (-300, -1700, z)
>      Room 3 doorway, for z = 30, 150, 250, 350, 390:
>        start (-300,  1300, z)  end (-300,  1700, z)
>      Room 2 doorway, for z = 30, 150, 250, 350, 390:
>        start (1000,     0, z)  end (1400,     0, z)
>      Final doorway,  for z = 630, 750, 850, 950, 990:
>        start (1000,     0, z)  end (1400,     0, z)
>
>      All 20 are expected to return a distance near 195. None is expected to return null.
>
>   C) Report the actor bounding box of each of the four doors.
>
>   D) Report the total actor count in the level, and confirm no actor was created or
>      deleted by this command.
>
>   E) Report any warning or error text verbatim in English. Do not summarize or translate.
>
> Write the report to Docs/Terminal-Log/2026-09-03-47-door-leaf-via-actor-scale.md
> (a repo path - do NOT write under Saved/, it is gitignored).

---

## STEP 1 — revert the class default

### 1a — the write

`ObjectTools.set_properties` on
`/Game/Interaction/BP_Door.BP_Door_C:DoorMesh_GEN_VARIABLE`, values
`{"RelativeScale3D":{"x":0.05,"y":0.5,"z":1.0}}`:

```json
{"returnValue":true}
```

This is the SCS template, not a level instance, and command 46 already
established that writes to the template do land. Confirmed in 1d.

### 1b — compile, verbatim

`BlueprintTools.compile_blueprint`, `warnings_as_errors: false`:

```json
{"returnValue":null}
```

The tool returns `null` on success and does not return compiler text. The
compiler's own log output is one line, verbatim:

```
[2026.09.03-10.16.10:497][876]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Door.BP_Door'
```

Filtering the whole session log for `LogBlueprint` returns exactly two entries —
command 46's compile and this one — and nothing else:

```
[2026.09.03-09.51.57:161][706]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Door.BP_Door'
[2026.09.03-10.16.10:497][876]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Door.BP_Door'
```

**No compile error and no compile warning was emitted.**

### 1c — save, and proof it was written

`AssetTools.save_assets` with `["/Game/Interaction/BP_Door"]`:

```json
{"returnValue":true}
```

`AssetTools.is_dirty` afterwards:

```json
{"returnValue":false}
```

On disk:

| | Before this command | After |
|---|---|---|
| mtime | `2026-09-03 18:52:19.928953200 +0900` | `2026-09-03 19:16:19.547985700 +0900` |
| size | 144828 bytes | 144828 bytes |

**PASS.** The mtime advanced by ~24 minutes, matching the save, and the dirty
flag cleared.

**One thing worth naming:** the file size is identical before and after, and
`git status` still reports `M Content/Interaction/BP_Door.uasset` even though the
value is now semantically back to where it was at HEAD. That is expected — a
resaved `.uasset` does not reproduce the original bytes — but it means **git
cannot be used to confirm the revert.** The revert is confirmed by the read-back
in 1d instead, not by the working tree being clean.

### 1d — read-back of the class default

```json
{"RelativeLocation":{"x":0,"y":0,"z":0},
 "RelativeScale3D":{"x":0.050000000000000003,"y":0.5,"z":1},
 "RelativeRotation":{"pitch":0,"yaw":0,"roll":0},
 "StaticMesh":{"refPath":"/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door.SM_Door"}}
```

**PASS. `z` is back to 1.** X is `0.050000000000000003`, the same double the
class default has always carried. Y is 0.5. `RelativeLocation` is still
`(0, 0, 0)` — as recorded in command 47's predecessor, the class default is
`(0, 0, 0)` and only the instances carry `(0, 50, 0)`; that asymmetry is
untouched. StaticMesh still SM_Door. The stale `z: 2` can no longer reach an
instance if the per-instance overrides are ever cleared, which was the point of
STEP 1.

---

## STEP 2 — set actor scale Z from 1 to 2 on the four doors

`ActorTools.set_actor_transform`, `worldspace: true`.

Location and rotation were **not** retyped from the instruction. For each actor
the current transform was read first and the exact returned `location` and
`rotation` objects were sent straight back, with only `scale.z` replaced:

```python
old = get_xform(ref)
xf = {"location": old["location"], "rotation": old["rotation"],
      "scale": {"x": old["scale"]["x"], "y": old["scale"]["y"], "z": 2.0}}
```

This matters: Door_R1 and Door_R3 carry yaw `-90.00000000000001`, not the `-90`
the instruction writes. Retyping `-90` would have silently altered their
rotation. The script also refused to write any actor whose starting location was
not the expected value **and** whose starting scale was not exactly `(1, 2, 1)`.
`skipped` came back empty, so all four passed both guards.

| Label | set returned | scale before | scale after | loc unchanged | rot unchanged |
|---|---|---|---|---|---|
| `Door_R1` | `true` | `(1, 2, 1)` | `(1, 2, 2)` | `true` | `true` |
| `Door_R2` | `true` | `(1, 2, 1)` | `(1, 2, 2)` | `true` | `true` |
| `Door_R3` | `true` | `(1, 2, 1)` | `(1, 2, 2)` | `true` | `true` |
| `Door_Final` | `true` | `(1, 2, 1)` | `(1, 2, 2)` | `true` | `true` |

`skipped: []`. **PASS.** `loc_unchanged` and `rot_unchanged` are whole-object
comparisons against the pre-write values, not approximate checks.

**No component write was issued by this command.** The only tools called against
a door were `get_actor_transform`, `set_actor_transform`, `get_actor_bounds`,
`get_components` and `get_properties`. No actor was deleted or re-created, so
every door's per-instance Blueprint state (`bLocked`, `RequiredKey`, tags) and
the three `BP_StageRoom` references to them are untouched — the internal names
are unchanged from command 46 and are listed in section A.

---

## A) The four doors, final state

Every value is a fresh read taken **after** the level was saved.

### Door_R1

| Field | Value |
|---|---|
| Internal name | `BP_Door_C_UAID_9C6B005AF86926FE02_1375958439` |
| World location | `(-400, -1500, 200)` |
| Rotation | `(pitch 0, yaw -90.00000000000001, roll 0)` |
| Actor scale | **`(1, 2, 2)`** |
| DoorMesh RelativeLocation | `(-1.4210854715202004e-14, 50.000000000000014, 0)` |
| DoorMesh RelativeScale3D | `(0.050000000000000003, 0.5, 1)` — **unchanged, as intended** |

### Door_R2

| Field | Value |
|---|---|
| Internal name | `BP_Door_C_UAID_9C6B005AF86926FE02_1375967440` |
| World location | `(1200, -100, 200)` |
| Rotation | `(0, 0, 0)` |
| Actor scale | **`(1, 2, 2)`** |
| DoorMesh RelativeLocation | `(0, 50, 0)` |
| DoorMesh RelativeScale3D | `(0.050000000000000003, 0.5, 1)` — **unchanged, as intended** |

### Door_R3

| Field | Value |
|---|---|
| Internal name | `BP_Door_C_UAID_9C6B005AF86926FE02_1376293441` |
| World location | `(-400, 1500, 200)` |
| Rotation | `(pitch 0, yaw -90.00000000000001, roll 0)` |
| Actor scale | **`(1, 2, 2)`** |
| DoorMesh RelativeLocation | `(-1.4210854715202004e-14, 50.000000000000014, 0)` |
| DoorMesh RelativeScale3D | `(0.050000000000000003, 0.5, 1)` — **unchanged, as intended** |

### Door_Final

| Field | Value |
|---|---|
| Internal name | `BP_Door_C_UAID_9C6B005AF86932FE02_1830770592` |
| World location | `(1200, -100, 800)` |
| Rotation | `(0, 0, 0)` |
| Actor scale | **`(1, 2, 2)`** |
| DoorMesh RelativeLocation | `(0, 50, 0)` |
| DoorMesh RelativeScale3D | `(0.050000000000000003, 0.5, 1)` — **unchanged, as intended** |

**All four component values are exactly what the instruction predicted they would
be: `RelativeLocation (0, 50, 0)` and `RelativeScale3D (0.05, 0.5, 1.0)`.** The
`-1.4210854715202004e-14` and `50.000000000000014` on R1 and R3 are pre-existing
float residue from their -90 yaw, present in command 46's pre-edit read and
unchanged here.

---

## B) The 20 line traces

`SceneTools.trace_world`. Every returned value reproduced exactly, nothing
rounded. This set was run twice — once before the save and once after — and both
runs returned identical values.

### Room 1 doorway — start `(-300, -1300, z)` end `(-300, -1700, z)`

| z | distance | verdict |
|---|---|---|
| 30 | `195.00001525878906` | blocking |
| 150 | `195.00001525878906` | blocking |
| 250 | `195.00001525878906` | blocking |
| 350 | `195.00001525878906` | blocking |
| 390 | `195.00001525878906` | blocking |

### Room 3 doorway — start `(-300, 1300, z)` end `(-300, 1700, z)`

| z | distance | verdict |
|---|---|---|
| 30 | `195.00001525878906` | blocking |
| 150 | `195.00001525878906` | blocking |
| 250 | `195.00001525878906` | blocking |
| 350 | `195.00001525878906` | blocking |
| 390 | `195.00001525878906` | blocking |

### Room 2 doorway — start `(1000, 0, z)` end `(1400, 0, z)`

| z | distance | verdict |
|---|---|---|
| 30 | `195` | blocking |
| 150 | `195` | blocking |
| 250 | `195` | blocking |
| 350 | `195` | blocking |
| 390 | `195` | blocking |

### Final doorway — start `(1000, 0, z)` end `(1400, 0, z)`

| z | distance | verdict |
|---|---|---|
| 630 | `195` | blocking |
| 750 | `195` | blocking |
| 850 | `195` | blocking |
| 950 | `195` | blocking |
| 990 | `195` | blocking |

**Result: 20 of 20 return a distance near 195. `null_count` is 0.** The
expectation stated in the instruction is met in full.

For contrast, command 46 got 8 hits and 12 nulls on this same set. The 12 that
were null are exactly the low and high samples — z=30, 350, 390 and z=630, 950,
990 — and all 12 now hit. **The gap that command 46 opened underneath every door
is closed, and so is the gap above.**

The two distinct values are not noise: the -90-yaw doors (R1, R3) return
`195.00001525878906` and the zero-yaw doors (R2, Final) return exactly `195`.
That split matches the float residue in those two actors' rotations and was
present in command 46's eight hits as well.

---

## C) Actor bounding boxes of the four doors

| Door | Bounds min | Bounds max | Z span |
|---|---|---|---|
| `Door_R1` | `(-528, -1628, 0)` | `(-199.99998474121082, -1372, 400)` | **0 .. 400** |
| `Door_R2` | `(1072, -228, 0)` | `(1328, 100.00001525878906, 400)` | **0 .. 400** |
| `Door_R3` | `(-528, 1372, 0)` | `(-199.99998474121082, 1628, 400)` | **0 .. 400** |
| `Door_Final` | `(1072, -228, 600)` | `(1328, 100.00001525878906, 1000)` | **600 .. 1000** |

The three ground-floor doors span exactly `Z 0..400`, matching the doorways
raised in command 45. `Door_Final` spans exactly `Z 600..1000`, matching the
opening between `Wall_2F_N_Sill` (top at Z 600) and `Wall_2F_N_Lintel` (bottom at
Z 1000).

For comparison, the same four bounds at the end of command 46 were `Z 72..328`,
`72..328`, `72..328` and `672..928`. The X and Y extents are unchanged — only Z
grew, which is what changing only `scale.z` should do.

---

## D) Actor count

**101 before, 101 after.** The count was read four separate times across this
command and was 101 every time.

**No actor was created and none was deleted by this command.** Confirmed three
ways: the count never moved; all four doors kept the internal names they had in
command 46 (`..._1375958439`, `..._1375967440`, `..._1376293441`,
`..._1830770592`), so they were edited in place rather than replaced; and no
`add_to_scene_*` or `remove_from_scene` tool was called at any point.

---

## STEP 3 — save, and what actually happened

This step did not work the first way, and the failure is worth recording because
the tool reported success.

### First attempt — `save_assets` on the level package, which silently did nothing

`AssetTools.save_assets` with `["/Game/ThirdPerson/Lvl_Stage"]`:

```json
{"returnValue":true}
```

`AssetTools.is_dirty` on the level afterwards:

```json
{"returnValue":false}
```

**Both of those are misleading. Nothing was written.** `Lvl_Stage.umap` still had
mtime `2026-09-03 09:47:04.791203000 +0900` and `git status` showed no change to
it or to anything else under `Content/`. A `find` for any file under `Content`
modified after 19:00 returned only `BP_Door.uasset` from STEP 1.

**Why:** this is a **World Partition** level. `Lvl_Stage.umap` is only 12,824
bytes and there are 134 actor packages under
`Content/__ExternalActors__/ThirdPerson/Lvl_Stage/`. The actors are not stored in
the `.umap` at all — each lives in its own package. The level package genuinely
was not dirty, so `is_dirty: false` was truthful about the level package and
completely uninformative about the actors.

### Second attempt — `SceneTools.save_actor`, which failed on all 11

Called on each of the 11 actors changed by commands 45–47. All 11 failed, with
this text verbatim (full block reproduced in section E):

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/3/NT/AE23ABHD86QNB96RH83E51
Failed to save 'Wall_Lobby_W_UpperA'.
```

`save_actor` resolves the actor's external package path and then refuses because
that package is not in the asset registry. **It cannot save an actor whose
external package has not been written yet, which is exactly the case that needs
saving.** Notably the paths it printed are the correct ones — they are the same
11 files that the next attempt went on to write successfully.

### Third attempt — `save_assets` with an empty list, which worked

`AssetTools.save_assets` with `[]` ("Pass an empty list to save all dirty
assets"):

```json
{"returnValue":true}
```

This one really wrote. Verified on disk, not from the return value.

### Packages written

**12 packages in total.** One Blueprint asset from STEP 1, and 11 external actor
packages from STEP 3.

`Content/Interaction/BP_Door.uasset` — modified, mtime `19:16:19`.

Eight **modified** external actor packages, all mtime `19:19:03`:

| Package | Actor | Changed by |
|---|---|---|
| `__ExternalActors__/ThirdPerson/Lvl_Stage/3/NT/AE23ABHD86QNB96RH83E51.uasset` | `Wall_Lobby_W_UpperA` | cmd 45 |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/7/QT/EKA4ZIANI4Z804H5FBSABQ.uasset` | `Wall_Lobby_E_UpperA` | cmd 45 |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/9/W7/3LFPR5UMU0W4IN33CGF4FE.uasset` | `Wall_Lobby_N_UpperA` | cmd 45 |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/B/4L/MOG24GZF46KIDMFEAHJ8UC.uasset` | `Wall_2F_N_Lintel` | cmd 45 |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/4/I1/YSQWZLPORCO257IL2GF2M5.uasset` | `Door_R1` | cmd 46 + 47 |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/D/HJ/2G51YLGE8ZGV4AATK5FAQQ.uasset` | `Door_R2` | cmd 46 + 47 |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/7/OQ/18J6R3STOL5A06WBA36F9C.uasset` | `Door_R3` | cmd 46 + 47 |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/0/R0/10SQ2O49OAHPAFPKK3Y6CG.uasset` | `Door_Final` | cmd 46 + 47 |

Three **newly created** external actor packages, all mtime `19:19:03`, showing as
untracked directories in git:

| Package | Actor | Created by |
|---|---|---|
| `__ExternalActors__/ThirdPerson/Lvl_Stage/6/EK/2PDGC2V7JFPRMX9RBI2WDT.uasset` | `Wall_Lobby_W_UpperB` | cmd 45 |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/B/4Q/EOSI6243HDJYT8T09IFNXO.uasset` | `Wall_Lobby_E_UpperB` | cmd 45 |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/6/BZ/IHIBB6U08DS2M6SREO5CBT.uasset` | `Wall_Lobby_N_UpperB` | cmd 45 |

The external actor file count went **134 → 137**, `+3`, which is exactly the three
walls command 45 created and no more.

**`Lvl_Stage.umap` itself was not written** — still mtime
`2026-09-03 09:47:04.791203000 +0900`, still 12,824 bytes, still absent from
`git status`. For a World Partition level this is correct, not a failure: the
actor data lives entirely in the external packages listed above.

`git status --porcelain` at the end:

```
 M Content/Interaction/BP_Door.uasset
 M Content/__ExternalActors__/ThirdPerson/Lvl_Stage/0/R0/10SQ2O49OAHPAFPKK3Y6CG.uasset
 M Content/__ExternalActors__/ThirdPerson/Lvl_Stage/3/NT/AE23ABHD86QNB96RH83E51.uasset
 M Content/__ExternalActors__/ThirdPerson/Lvl_Stage/4/I1/YSQWZLPORCO257IL2GF2M5.uasset
 M Content/__ExternalActors__/ThirdPerson/Lvl_Stage/7/OQ/18J6R3STOL5A06WBA36F9C.uasset
 M Content/__ExternalActors__/ThirdPerson/Lvl_Stage/7/QT/EKA4ZIANI4Z804H5FBSABQ.uasset
 M Content/__ExternalActors__/ThirdPerson/Lvl_Stage/9/W7/3LFPR5UMU0W4IN33CGF4FE.uasset
 M Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/4L/MOG24GZF46KIDMFEAHJ8UC.uasset
 M Content/__ExternalActors__/ThirdPerson/Lvl_Stage/D/HJ/2G51YLGE8ZGV4AATK5FAQQ.uasset
?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/6/BZ/
?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/6/EK/
?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/4Q/
?? "Docs/Spec/2026-09-03-\353\241\234\353\271\204-\354\244\221\354\204\270-\353\247\210\352\260\220.md"
?? Docs/Terminal-Log/2026-09-03-45-doorway-height-400.md
?? Docs/Terminal-Log/2026-09-03-46-door-leaf-height-400.md
```

The `Docs/Spec/` entry is a pre-existing untracked file unrelated to this work.

### Command 45's walls were re-checked before saving

Because the save persists whatever is in memory, all eight walls that commands 45
touched or created were re-read immediately before STEP 3 and compared against
command 45's expected bounds. `all_match: true`, `missing: []`:

| Wall | Bounds | Matches cmd 45 |
|---|---|---|
| `Wall_Lobby_W_UpperA` | `(-1300,-1600,200)`..`(-400,-1400,400)` | yes |
| `Wall_Lobby_W_UpperB` | `(-200,-1600,200)`..`(1300,-1400,400)` | yes |
| `Wall_Lobby_E_UpperA` | `(-1300,1400,200)`..`(-400,1600,400)` | yes |
| `Wall_Lobby_E_UpperB` | `(-200,1400,200)`..`(1300,1600,400)` | yes |
| `Wall_Lobby_N_UpperA` | `(1100,-1600,200)`..`(1300,-100,400)` | yes |
| `Wall_Lobby_N_UpperB` | `(1100,100,200)`..`(1300,1600,400)` | yes |
| `Wall_2F_N_Lintel` | `(1100,-100,1000)`..`(1300,100,1200)` | yes |
| `Wall_2F_N_Sill` | `(1100,-100,400)`..`(1300,100,600)` | yes |

**Command 45's work reached disk intact.**

---

## E) Warnings and errors, verbatim

Every warning and error emitted during this command, in full, untranslated and
unsummarized.

**Two from a read**, caused by asking for `StaticMesh` on components that do not
have it while walking the Blueprint's component list:

```
[2026.09.03-10.06.39:457][703]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Door.BP_Door_C:DefaultSceneRoot_GEN_VARIABLE' (SceneComponent): the following properties could not be read: StaticMesh
[2026.09.03-10.06.39:795][704]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Door.BP_Door_C:Hinge_GEN_VARIABLE' (SceneComponent): the following properties could not be read: StaticMesh
```

**Twenty-two from the failed `save_actor` attempt**, one pair per actor plus a
trailing stack line on each. Reproduced complete and in order:

```
[2026.09.03-10.18.44:497][338]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/3/NT/AE23ABHD86QNB96RH83E51
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.44:497][338]LogScript: Warning: Failed to save 'Wall_Lobby_W_UpperA'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.44:830][339]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/7/QT/EKA4ZIANI4Z804H5FBSABQ
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.44:830][339]LogScript: Warning: Failed to save 'Wall_Lobby_E_UpperA'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.45:496][341]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/9/W7/3LFPR5UMU0W4IN33CGF4FE
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.45:496][341]LogScript: Warning: Failed to save 'Wall_Lobby_N_UpperA'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.45:830][342]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/6/EK/2PDGC2V7JFPRMX9RBI2WDT
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.45:830][342]LogScript: Warning: Failed to save 'Wall_Lobby_W_UpperB'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.45:831][342]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/4Q/EOSI6243HDJYT8T09IFNXO
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.45:831][342]LogScript: Warning: Failed to save 'Wall_Lobby_E_UpperB'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.46:496][344]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/6/BZ/IHIBB6U08DS2M6SREO5CBT
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.46:496][344]LogScript: Warning: Failed to save 'Wall_Lobby_N_UpperB'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.46:831][345]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/4L/MOG24GZF46KIDMFEAHJ8UC
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.46:831][345]LogScript: Warning: Failed to save 'Wall_2F_N_Lintel'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.47:496][347]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/4/I1/YSQWZLPORCO257IL2GF2M5
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.47:496][347]LogScript: Warning: Failed to save 'Door_R1'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.47:830][348]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/D/HJ/2G51YLGE8ZGV4AATK5FAQQ
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.47:830][348]LogScript: Warning: Failed to save 'Door_R2'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.48:496][350]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/7/OQ/18J6R3STOL5A06WBA36F9C
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.48:496][350]LogScript: Warning: Failed to save 'Door_R3'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.48:831][351]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/0/R0/10SQ2O49OAHPAFPKK3Y6CG
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
[2026.09.03-10.18.48:831][351]LogScript: Warning: Failed to save 'Door_Final'.
	Function /Script/Engine.KismetSystemLibrary:RaiseScriptError:64X
```

**No compile error, no compile warning, and no error of any kind was emitted by
the Blueprint edit, the four actor-scale writes, or the successful save.** The
24 entries above are the complete set for this command.

---

## Two tool behaviours worth carrying forward

Both are cases where the MCP return value disagreed with reality, which is the
thing `CLAUDE.md` says to record as an observation rather than treat as a bug.

1. **`save_assets(["/Game/ThirdPerson/Lvl_Stage"])` returns `true` and
   `is_dirty` then returns `false`, while writing nothing.** In a World Partition
   level the actors are in external packages and the level package is not dirty,
   so both answers are technically true and jointly useless. `save_assets([])`
   is what actually saves the actors.
2. **`SceneTools.save_actor` cannot save an actor whose external package does not
   exist on disk yet** — it fails with `Asset does not exist` for the very path
   it would need to create. It failed on all 11 actors here, including 8 whose
   packages did already exist, so the limitation is broader than just newly
   created actors.

---

## Not verified

- **PIE was not run.** No gameplay observation is in this report. Whether a
  character is now correctly blocked by these doors, and whether the doors still
  open and close properly at their new scale, is unconfirmed.
- **The door open/close animation was not exercised.** The leaf is scaled on the
  actor, so the Hinge rotation should be unaffected, but nothing here tests that.
  This is the one thing most worth checking in PIE, because the change went in
  through the actor transform rather than the component.
- **Nothing was looked at in the viewport.** Every figure is from
  `get_actor_transform`, `get_actor_bounds`, `get_properties` and `trace_world`.
- **The traces sample five heights along the doorway centre line only.** They
  show the leaf blocks at those heights; they do not prove it fully fills the
  doorway width, and no trace was run off-centre.
- **The BP_Door graph and variables were not read.** No tool was called against
  them and the only Blueprint write was the single `set_properties` in 1a, but
  no positive check was done to prove the graph is byte-identical.
- **`bLocked`, `RequiredKey` and the door tags were not read back.** No actor was
  deleted or re-created and no component or variable was written, so they should
  be untouched — but that is an argument from what was not called, not a
  measurement.
- **The three `BP_StageRoom` references to the doors were not re-read.** Same
  reasoning: the door actors kept their internal names, so the references cannot
  have broken, but this was not directly confirmed.
