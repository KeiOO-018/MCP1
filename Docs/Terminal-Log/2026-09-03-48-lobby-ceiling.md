# 2026-09-03 · Command 48 — Ceiling slab over the lobby

Level change only, in `/Game/ThirdPerson/Lvl_Stage`.
**One actor created. Nothing else touched. No Blueprint edited, no light or
atmosphere actor touched, no material set. Saved to disk.**

Instruction, verbatim from the user:

> In the currently open level /Game/ThirdPerson/Lvl_Stage, add a ceiling slab over the
> lobby. This is one new actor and nothing else.
>
> Purpose: this level has no ceiling anywhere, so the lobby is lit by the outdoor sky.
> Capping the lobby cuts that sky light for the lobby ONLY, which is what makes it
> possible to relight the lobby with torches without darkening rooms 1, 2 and 3.
>
> The slab covers the whole lobby footprint including the walls, so there is no seam at
> the wall faces and the wall tops are capped. The lobby's second-floor walls all end at
> Z 1200, so the slab sits directly on top of them.
>
>   Create a new StaticMeshActor using SM_Cube
>   (/Game/LevelPrototyping/Meshes/SM_Cube), labeled "Ceiling_Lobby",
>   at location (-1300, -1600, 1200), rotation (0, 0, 0), scale (26, 32, 0.5).
>
>   SM_Cube's pivot is at its minimum corner and its unscaled size is 100 x 100 x 100,
>   so this gives world bounds X -1300..1300, Y -1600..1600, Z 1200..1250.
>
>   Do not set a material. It must inherit SM_Cube's own material, the same way every
>   wall in this level does.
>
> DO NOT touch any other actor. DO NOT edit any Blueprint. DO NOT change any light,
> the SkyLight, the SkyAtmosphere, the DirectionalLight, the ExponentialHeightFog or the
> PostProcessVolume - this command only adds geometry.
>
> STEP 2 - Save, using AssetTools.save_assets with an empty list. Report which packages
> were written, verified on disk and not from the return value.
>
> VERIFY AND REPORT.
>
>   A) Report Ceiling_Lobby's location, rotation, scale, world bounding box, static mesh
>      and OverrideMaterials, and say whether the bounds match X -1300..1300,
>      Y -1600..1600, Z 1200..1250.
>
>   B) Confirm the slab actually seals. Run these downward line traces with
>      SceneTools.trace_world and report the distance for each. Each starts at Z 2000 and
>      ends at Z 0 at the same X and Y. A distance of 750 means it hit the top of the slab
>      at Z 1250. A larger number or a null means there is a hole.
>
>        ( 0,     0)   ( 700,     0)   (-1000,     0)
>        (-1000, -1300) ( 1000, -1300) (-1000,  1300) ( 1000,  1300)
>        ( 1200,     0) (-1200,     0) ( 0,    -1500) ( 0,     1500)
>
>   C) Report the total actor count before and after. Exactly one actor is expected to be
>      added.
>
>   D) Report any warning or error text verbatim in English. Do not summarize or translate.
>
> Write the report to Docs/Terminal-Log/2026-09-03-48-lobby-ceiling.md
> (a repo path - do NOT write under Saved/, it is gitignored).

**Headline: the slab was created with the exact requested transform, its world
bounds match the expected box exactly with no float residue, and all 11 downward
traces return exactly 750 — the lobby is sealed at every sampled point. Actor
count 98→102 across the session; 101 before this command, 102 after, +1. The save
wrote exactly one package and nothing else, which is itself the proof that no
other actor was disturbed. No warning or error was emitted by this command.**

---

## Pre-flight

### P1 — Level guard

`SceneTools.get_current_level`:

```json
{"returnValue":"/Game/ThirdPerson/Lvl_Stage"}
```

**PASS.**

### P2 — Nothing named "Ceiling" already exists

`find_actors` with `name: "Ceiling"` returned an empty list. There was no
pre-existing ceiling actor to collide with or duplicate.

### P3 — The claim "the lobby's second-floor walls all end at Z 1200" was checked, not assumed

`find_actors` with `name: "Wall_2F"`, then `get_actor_bounds` on each:

| Wall | Bounds min | Bounds max | Top Z |
|---|---|---|---|
| `Wall_2F_W` | `(-1300, -1600, 400)` | `(1300, -1400, 1200)` | **1200** |
| `Wall_2F_E` | `(-1300, 1400, 400)` | `(1300, 1600, 1200)` | **1200** |
| `Wall_2F_S` | `(-1300, -1400, 400)` | `(-1100, 1400, 1200)` | **1200** |
| `Wall_2F_N_A` | `(1100, -1400, 400)` | `(1300, -100, 1200)` | **1200** |
| `Wall_2F_N_B` | `(1100, 100, 400)` | `(1300, 1400, 1200)` | **1200** |
| `Wall_2F_N_Lintel` | `(1100, -100, 1000)` | `(1300, 100, 1200)` | **1200** |
| `Wall_2F_N_Sill` | `(1100, -100, 400)` | `(1300, 100, 600)` | 600 (below the doorway, not a top wall) |

**PASS.** Every wall that forms the top of the lobby ends at exactly Z 1200, so
the slab's underside at Z 1200 sits flush on them with no gap and no overlap.

The footprint also checks out. The lobby's outer wall faces span X -1300..1300
(`Wall_2F_W`/`Wall_2F_E` max X 1300, `Wall_2F_S` min X -1300) and Y -1600..1600
(`Wall_2F_W` min Y -1600, `Wall_2F_E` max Y 1600). The requested slab covers
exactly X -1300..1300, Y -1600..1600 — the whole footprint **including** the wall
thickness, which is what the instruction asked for, so the wall tops are capped
and there is no seam at any wall face.

### P4 — Actor count before

`find_actors` with an empty name: **101**.

---

## The write

`SceneTools.add_to_scene_from_asset`:

```json
{"asset_path": "/Game/LevelPrototyping/Meshes/SM_Cube",
 "name": "Ceiling_Lobby",
 "xform": {"location": {"x": -1300, "y": -1600, "z": 1200},
           "rotation": {"pitch": 0, "yaw": 0, "roll": 0},
           "scale": {"x": 26, "y": 32, "z": 0.5}},
 "snap_to_ground": false}
```

Returned:

```json
{"returnValue":{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.StaticMeshActor_UAID_9C6B005AF86942FE02_1348737338"}}
```

Followed by an explicit `ActorTools.set_label` to `"Ceiling_Lobby"`:

```json
{"returnValue":true}
```

`snap_to_ground` was explicitly `false`. Had it been left on, the slab would have
been dropped onto whatever is below it and the Z 1200 placement would have been
silently lost.

**No material tool was called.** `OverrideMaterials` was never written — confirmed
empty in section A.

These are the only two write calls this command made. Every other call was a read
(`get_current_level`, `find_actors`, `get_label`, `get_actor_transform`,
`get_actor_bounds`, `get_class`, `get_components`, `get_properties`,
`trace_world`, `GetLogEntries`) plus the one save.

---

## A) Ceiling_Lobby

| Field | Value |
|---|---|
| Editor label | `Ceiling_Lobby` |
| Internal name | `StaticMeshActor_UAID_9C6B005AF86942FE02_1348737338` |
| Class | `/Script/Engine.StaticMeshActor` |
| Location | `(-1300, -1600, 1200)` |
| Rotation | `(pitch 0, yaw 0, roll 0)` |
| Scale | `(26, 32, 0.5)` |
| **Bounds min** | `(-1300, -1600, 1200)` |
| **Bounds max** | `(1300, 1600, 1250)` |
| Static mesh | `/Game/LevelPrototyping/Meshes/SM_Cube.SM_Cube` |
| **OverrideMaterials** | `[]` — empty |

Component read, verbatim:

```json
["/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.StaticMeshActor_UAID_9C6B005AF86942FE02_1348737338.StaticMeshComponent0",
 "{\"StaticMesh\":{\"refPath\":\"/Game/LevelPrototyping/Meshes/SM_Cube.SM_Cube\"},\"OverrideMaterials\":[]}"]
```

**The bounds match X -1300..1300, Y -1600..1600, Z 1200..1250 exactly.** The
comparison was done as a whole-object equality test against the expected box, not
by eye:

```json
"bounds_match": true
```

Every component is an exact integer — no float residue anywhere, including on the
`0.5` Z scale, which produces a clean 50-unit thickness (1200..1250).

**Material:** `OverrideMaterials` is an empty array, so the slab renders with
SM_Cube's own default material. This is identical to how every wall in the level
is set up — the same check was run on `Wall_Lobby_W_UpperA` in command 45 and it
too reported `"OverrideMaterials":[]`. The instruction's requirement is met.

The actor has exactly one component, `StaticMeshComponent0`, which is the normal
shape for a `StaticMeshActor`.

---

## B) The 11 downward seal traces

`SceneTools.trace_world`, each from `(x, y, 2000)` to `(x, y, 0)`. A distance of
750 means the trace stopped at Z 1250, the top of the slab.

| # | X | Y | distance | verdict |
|---|---|---|---|---|
| 1 | 0 | 0 | `750` | sealed |
| 2 | 700 | 0 | `750` | sealed |
| 3 | -1000 | 0 | `750` | sealed |
| 4 | -1000 | -1300 | `750` | sealed |
| 5 | 1000 | -1300 | `750` | sealed |
| 6 | -1000 | 1300 | `750` | sealed |
| 7 | 1000 | 1300 | `750` | sealed |
| 8 | 1200 | 0 | `750` | sealed |
| 9 | -1200 | 0 | `750` | sealed |
| 10 | 0 | -1500 | `750` | sealed |
| 11 | 0 | 1500 | `750` | sealed |

**All 11 return exactly `750`. Not one is null, and not one is larger.** These are
integer 750 values, not approximations — the script tested `abs(d - 750) < 0.01`
and the count of traces failing that test was `0`.

```json
"not_750_count": 0
```

Points 8 and 9 (X ±1200) and points 10 and 11 (Y ±1500) sit close to the wall
lines, and they seal too, which is the evidence that the slab really does cover
the full footprint out to the walls rather than stopping short of them.

**Interpretation, stated carefully:** these 11 traces prove the slab blocks a
vertical line at 11 sampled points. They do not prove there is no hole anywhere —
only the sampled columns were tested. But the bounds in section A are a single
unbroken box covering the entire footprint, and a single box has no interior
holes, so the geometry argument and the trace evidence agree.

---

## C) Actor count

| | Count |
|---|---|
| Before | **101** |
| After | **102** |
| Delta | **+1** |

**Exactly one actor was added, as expected.** Nothing was deleted.

Corroborated three ways beyond the count itself:

1. `find_actors` with `name: "Ceiling"` after the write returns exactly one label,
   `["Ceiling_Lobby"]` — the create did not produce a duplicate, and the
   `set_label` did not collide with anything.
2. **The save wrote exactly one package.** If any other actor had been modified,
   its external package would have been written too. See the next section.
3. The editor's own content validation on save reported
   `Starting to validate 1 assets (1 associated objects such as actors)`.

---

## STEP 2 — Save, verified on disk

`AssetTools.save_assets` with `[]`:

```json
{"returnValue":true}
```

Per the finding recorded in command 47, this empty-list form is the one that
actually writes a World Partition level's actors; passing the level's own package
path returns `true` and writes nothing. That is why the empty list was used, and
why the result below is checked on disk rather than taken from the return value.

### Packages written — exactly one

```
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/UI/6Y42US2MONK6DNTSL013DP.uasset
```

mtime `2026-09-03 19:40:52.782908300 +0900`. This is `Ceiling_Lobby`'s external
actor package, newly created.

Verified four ways, none of them the tool's return value:

1. **A `find` for every file under `Content` modified in the last 10 minutes
   returned that one path and nothing else.**
2. External actor file count went **137 → 138**, exactly `+1`.
3. `git status --porcelain` was **completely clean** before this command (commands
   45–47 having been committed) and afterwards shows only:
   ```
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/UI/
   ```
   One new untracked directory, nothing modified.
4. The editor log, verbatim:
   ```
   [2026.09.03-10.40.52:772][496]LogFileHelpers: Saving Package: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/UI/6Y42US2MONK6DNTSL013DP
   [2026.09.03-10.40.52:782][496]LogSavePackage: Moving output files for package: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/UI/6Y42US2MONK6DNTSL013DP
   [2026.09.03-10.40.52:782][496]LogSavePackage: Moving 'D:/20260827/MCP1/Saved/6Y42US2MONK6DNTSL013DP556706ED4299E0DD5017FBA024265F86.tmp' to 'D:/20260827/MCP1/Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/UI/6Y42US2MONK6DNTSL013DP.uasset'
   ```
   `Saving Package` appears once in the whole save.

**That the clean working tree gained exactly one untracked file is the strongest
evidence in this report that "DO NOT touch any other actor" was honoured.** Every
actor in this level has its own package. Had a light, the SkyLight, the
SkyAtmosphere, the DirectionalLight, the ExponentialHeightFog, the
PostProcessVolume, a wall or a door been modified in any way, its package would
have been dirty and would have been written by the same save. None was.

**`Lvl_Stage.umap` was not written** — still mtime
`2026-09-03 09:47:04.791203000 +0900`, still 12,824 bytes, absent from
`git status`. For a World Partition level this is correct: actor data lives
entirely in the external packages.

The editor also wrote an autosave copy at 10:40:28 under
`Saved/Autosaves/...`, which is gitignored and not part of the deliverable:

```
[2026.09.03-10.40.28:763][424]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/UI/6Y42US2MONK6DNTSL013DP_Auto5
```

### Content validation on save

Ran clean on the one asset, with nine validators enabled and zero failures:

```
[2026.09.03-10.40.53:049][497]LogContentValidation: Display: Starting to validate 1 assets (1 associated objects such as actors)
[2026.09.03-10.40.53:050][497]LogContentValidation: Validated asset counts for 9 validators:
[2026.09.03-10.40.53:050][497]LogContentValidation:   /Script/DataValidation.DirtyFilesChangelistValidator : 0
[2026.09.03-10.40.53:050][497]LogContentValidation:   /Script/DataValidation.EditorValidator_ActionUtility : 0
[2026.09.03-10.40.53:050][497]LogContentValidation:   /Script/DataValidation.EditorValidator_Localization : 1
[2026.09.03-10.40.53:050][497]LogContentValidation:   /Script/DataValidation.EditorValidator_Material : 0
[2026.09.03-10.40.53:050][497]LogContentValidation:   /Script/DataValidation.PackageFileValidator : 0
[2026.09.03-10.40.53:050][497]LogContentValidation:   /Script/DataValidation.WorldPartitionChangelistValidator : 0
[2026.09.03-10.40.53:050][497]LogContentValidation:   /Script/InputBlueprintNodes.EnhancedInputUserWidgetValidator : 0
[2026.09.03-10.40.53:050][497]LogContentValidation:   /Script/MutableValidation.AssetValidator_CustomizableObjects : 0
[2026.09.03-10.40.53:050][497]LogContentValidation:   /Script/MutableValidation.AssetValidator_ReferencedCustomizableObjects : 0
```

No validator reported an error.

---

## D) Warnings and errors

**No warning and no error was emitted by this command.**

This command's work runs from `10:40:18` (the `add_to_scene_from_asset` dispatch)
to `10:40:53` (the end of save validation):

```
[2026.09.03-10.40.18:674][394]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.scene.SceneTools.add_to_scene_from_asset'
```

Filtering the entire session log for `Warning`, `Error` and `Failed`, the most
recent matching entry is at **`10:31:28`**, roughly nine minutes before this
command began:

```
[2026.09.03-10.31.28:203][324]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
```

That entry predates this command and was not caused by it.

For completeness, the other warnings visible in the recent log are all from
`10:22:28`, also before this command, and are a display artefact of the terminal
font rather than anything to do with the level. They are the Slate font system
failing to find Hangul glyphs in Cascadia Mono. Reproduced verbatim:

```
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+d130, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+d130, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+ac00, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+ac00, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+b530, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+b530, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c788, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c788, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+b9cc, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+b9cc, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c2e4, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:497][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c2e4, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:497][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c81c, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:497][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c81c, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
```

Unlike commands 46 and 47, **this command produced no `GetObjectProperties`
warnings**, because the component read was restricted to the one
`StaticMeshComponent0` and asked only for properties that a StaticMeshComponent
actually has.

---

## What this does and does not do for the lighting goal

The instruction's stated purpose is to cut sky light from the lobby only, so it
can be relit with torches without darkening rooms 1, 2 and 3.

**What is established:** the lobby footprint is now capped by opaque geometry from
X -1300..1300, Y -1600..1600 at Z 1200..1250, and 11 downward traces confirm a
vertical line is blocked at every sampled point. No other room's ceiling was
added or changed, so rooms 1, 2 and 3 are still open to the sky.

**What is NOT established — this is a geometry result, not a lighting result.**
Nothing in this report measures light. Specifically:

- **No lighting was rebuilt and no light was re-evaluated.** Whether the lobby is
  actually darker now is unverified.
- **The lobby is not sealed against light from the sides.** The three ground-floor
  doorways and the second-floor final doorway are still openings, and the doors in
  them are 200 wide × 400 tall leaves, not light-tight seals. Sky light and
  bounced light can still enter through them and through any gap between the
  lobby and the corridors.
- **This project's lighting is likely Lumen** (the log shows Lumen CVars at
  startup), so sky occlusion is computed dynamically at runtime. What the editor
  viewport shows and what PIE shows may differ, and neither was checked.

---

## Not verified

- **PIE was not run.** No gameplay or runtime lighting observation is in this
  report.
- **Nothing was looked at in the viewport.** Every figure comes from
  `get_actor_transform`, `get_actor_bounds`, `get_properties`, `get_class` and
  `trace_world`.
- **Only 11 columns were traced.** The seal is proven at those points and argued
  from the single unbroken bounding box everywhere else.
- **The slab's underside contact with the wall tops was not traced.** Both are at
  exactly Z 1200 by measurement, so they are flush, but no trace tested the
  junction itself for a light leak or for Z-fighting between the slab's bottom
  face and the wall top faces. **Z-fighting at that shared plane is the most
  likely visual problem with this slab and it was not checked.**
- **Whether the slab is visible from outside the building** — it will be, since it
  is an opaque box on top of the lobby with SM_Cube's default material — was not
  evaluated against the level's exterior appearance.
- **The navmesh was not rebuilt.** A ceiling at Z 1200 should not affect the
  walkable floor, but that is reasoning, not a measurement.
