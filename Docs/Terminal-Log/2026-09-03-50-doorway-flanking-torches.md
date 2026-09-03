# 2026-09-03 · Command 50 — 6 flanking torches, one pair per remaining doorway

Level change only, in `/Game/ThirdPerson/Lvl_Stage`.
**6 PointLight actors created, all 6 configured identically to the existing 12
torches, all 6 in the "Lighting" folder, all 6 saved to disk. All 13 pre-existing
lights verified byte-identical to a baseline captured before any write. No
Blueprint edited, no mesh touched.**

Instruction, verbatim from the user:

> In the currently open level /Game/ThirdPerson/Lvl_Stage, add 6 more PointLight actors so
> that all four doorways have a torch on each side, matching the pair that already flanks
> the Room 2 doorway (Torch_1F_N_2 and Torch_1F_N_3, which sit 400 units to either side of
> that doorway's centre line).
>
> Every one of the 6 uses EXACTLY the same settings as the 12 existing torches:
>   Mobility        = Movable
>   Intensity       = 5000
>   IntensityUnits  = Unitless
>   AttenuationRadius = 1200
>   LightColor      = R 255, G 170, B 90
>   SourceRadius    = 10
>   CastShadows     = true
>   Rotation        = (0, 0, 0)
>   Outliner folder = "Lighting"
>
> GROUP 1 - ground floor, Room 1 doorway (the left / west one). That doorway is the gap
> X -400..-200 in the wall at Y -1600..-1400, so its centre is X -300 and the wall's inner
> face is Y -1400. Lights go 50 units off that face at Y -1350, and 400 units to either
> side of X -300.
>
>   Torch_1F_W_1   (-700, -1350, 250)
>   Torch_1F_W_2   ( 100, -1350, 250)
>
> GROUP 2 - ground floor, Room 3 doorway (the right / east one). Same doorway shape,
> mirrored to the wall at Y 1400..1600.
>
>   Torch_1F_E_1   (-700, 1350, 250)
>   Torch_1F_E_2   ( 100, 1350, 250)
>
> GROUP 3 - second floor, the final door in the middle of the north wall. That doorway is
> the gap Y -100..100 in the wall at X 1100..1300, at Z 600..1000. Its centre is Y 0 and
> the wall's inner face is X 1100. Lights go 50 units off that face at X 1050, 400 units
> to either side of Y 0, at Z 850 - which is 250 above the second floor walking surface at
> Z 600, the same height above the floor as the ground floor torches.
>
>   Torch_2F_N_1   (1050, -400, 850)
>   Torch_2F_N_2   (1050,  400, 850)
>
> DO NOT move, delete or change any of the 13 lights that already exist, including
> KeyLight_FinalDoor. DO NOT change the DirectionalLight, SkyLight, SkyAtmosphere,
> VolumetricCloud, ExponentialHeightFog or PostProcessVolume. DO NOT edit any Blueprint or
> touch any mesh, wall, floor, door, ramp, railing or pillar.
>
> STEP 2 - Save with AssetTools.save_assets and an empty list. Do not use save_actor - it
> fails on external actor packages that have not been written yet. Verify on disk that 6
> new packages appeared under Content/__ExternalActors__/ThirdPerson/Lvl_Stage/, and do
> not report success from the return value alone.
>
> VERIFY AND REPORT.
>
>   A) For each of the 6 new lights report the world location, Mobility, Intensity,
>      IntensityUnits, AttenuationRadius, LightColor, SourceRadius, CastShadows and
>      outliner folder, read back after creation.
>
>   B) Read back all 12 pre-existing torches and KeyLight_FinalDoor and confirm none of
>      them changed. Report their Intensity and location.
>
>   C) Report the total actor count before and after. Exactly 6 are expected to be added.
>
>   D) Report which packages were written to disk.
>
>   E) Report any warning or error text verbatim in English. Do not summarize or translate.
>
> Write the report to Docs/Terminal-Log/2026-09-03-50-doorway-flanking-torches.md
> (a repo path - do NOT write under Saved/, it is gitignored).

**Headline: all 6 created and correct on every one of the 10 checked fields, and
all 13 pre-existing lights are unchanged — this time proven by a real
before/after comparison, not by inference. Actor count 115 → 121, exactly +6.
The save wrote exactly 6 packages, all new, and modified zero tracked files. No
warning and no error was emitted by this command.**

---

## What is different about the verification this time

In command 49 I reported the untouched lights' values but had to admit I never
captured a baseline beforehand, so "unchanged" rested on inference. **That gap is
closed here.** Before any actor was created, a full baseline was read of all 13
existing lights — refPath, location, rotation, and all seven light-component
properties each. Section B compares against that recorded baseline field by
field. The baseline also confirmed there were no label collisions with the 6 new
names (`label_collisions_with_new: []`), so no existing light could be
accidentally targeted by a label lookup.

The colour conversion decision from command 49 carries over unchanged and is
restated here because it is still my decision, not the user's wording: the tool
types `lightColor` as a LinearColor clamped 0..1, so `R 255, G 170, B 90` was sent
as `r = 1.0`, `g = 170/255`, `b = 90/255`. Sending 255 would clamp to 1 and
silently produce white. All 6 read back as `(255, 170, 90)` after converting the
stored floats back to bytes.

---

## Pre-flight baseline

Actor count **115**. Existing light count **13**. Label collisions with the 6 new
names: **none**.

| Label | Location | Intensity | AttenRadius | refPath tail |
|---|---|---|---|---|
| `Torch_1F_S_1` | `(-1050, -1200, 250)` | `5000` | `1200` | `..._1955570339` |
| `Torch_1F_S_2` | `(-1050, -400, 250)` | `5000` | `1200` | `..._2016904340` |
| `Torch_1F_S_3` | `(-1050, 400, 250)` | `5000` | `1200` | `..._2017578341` |
| `Torch_1F_S_4` | `(-1050, 1200, 250)` | `5000` | `1200` | `..._2018570342` |
| `Torch_1F_N_1` | `(1050, -1200, 250)` | `5000` | `1200` | `..._2019903343` |
| `Torch_1F_N_2` | `(1050, -400, 250)` | `5000` | `1200` | `..._2020906344` |
| `Torch_1F_N_3` | `(1050, 400, 250)` | `5000` | `1200` | `..._2022237345` |
| `Torch_1F_N_4` | `(1050, 1200, 250)` | `5000` | `1200` | `..._2023238346` |
| `Torch_2F_W_1` | `(-700, -1350, 850)` | `5000` | `1200` | `..._2024240347` |
| `Torch_2F_W_2` | `(300, -1350, 850)` | `5000` | `1200` | `..._2025904348` |
| `Torch_2F_E_1` | `(-700, 1350, 850)` | `5000` | `1200` | `..._2027239349` |
| `Torch_2F_E_2` | `(300, 1350, 850)` | `5000` | `1200` | `..._2028241350` |
| `KeyLight_FinalDoor` | `(1000, 0, 900)` | `20000` | `2500` | `..._2029570351` |

All 13 baselined at `Movable / Unitless / sourceRadius 10 / castShadows true /
rotation (0,0,0) / colour (255,170,90) / folder Lighting`.

**The instruction's premise checks out.** `Torch_1F_N_2` at `(1050, -400, 250)`
and `Torch_1F_N_3` at `(1050, 400, 250)` do sit 400 units either side of Y 0, the
Room 2 doorway centre line, at X 1050 which is 50 off the inner wall face at
X 1100. The 6 new lights reproduce that geometry at the other three doorways.

---

## The write

`SceneTools.add_to_scene_from_class` with `actor_type` `/Script/Engine.PointLight`
and `snap_to_ground: false`, then `set_label`, then `set_properties` on the
actor's own `LightComponent0`, then `set_actor_folder` to `"Lighting"`. Identical
sequence and identical property payload for all 6 — the payload was built once as
a single constant and reused, so the 6 cannot drift from each other.

All `set_label` and `set_properties` calls returned `true`. **Per `CLAUDE.md`
that is not evidence**, so everything below is a fresh read-back.

No write tool was called against any pre-existing actor. The 6 refPaths written
to all share the `_UAID_9C6B005AF86943FE02_` prefix, which is distinct from the
`_UAID_9C6B005AF86942FE02_` prefix of every light created in command 49.

---

## A) The 6 new lights, read back

Shared by all 6 and verified individually on each: `Mobility = Movable`,
`IntensityUnits = Unitless`, `SourceRadius = 10`, `CastShadows = true`,
`Rotation = (0, 0, 0)`, `LightColor = (255, 170, 90)`, folder `Lighting`.

### Group 1 — Room 1 doorway (west), centre X -300, wall face Y -1400

| Label | Location | Intensity | AttenRadius | Folder | Match |
|---|---|---|---|---|---|
| `Torch_1F_W_1` | `(-700, -1350, 250)` | `5000` | `1200` | `Lighting` | **all 10 ✓** |
| `Torch_1F_W_2` | `(100, -1350, 250)` | `5000` | `1200` | `Lighting` | **all 10 ✓** |

### Group 2 — Room 3 doorway (east), mirrored to wall face Y 1400

| Label | Location | Intensity | AttenRadius | Folder | Match |
|---|---|---|---|---|---|
| `Torch_1F_E_1` | `(-700, 1350, 250)` | `5000` | `1200` | `Lighting` | **all 10 ✓** |
| `Torch_1F_E_2` | `(100, 1350, 250)` | `5000` | `1200` | `Lighting` | **all 10 ✓** |

### Group 3 — second floor final door, centre Y 0, wall face X 1100

| Label | Location | Intensity | AttenRadius | Folder | Match |
|---|---|---|---|---|---|
| `Torch_2F_N_1` | `(1050, -400, 850)` | `5000` | `1200` | `Lighting` | **all 10 ✓** |
| `Torch_2F_N_2` | `(1050, 400, 850)` | `5000` | `1200` | `Lighting` | **all 10 ✓** |

Full property read, identical on all 6 (this is `Torch_2F_N_1`'s, verbatim):

```json
{"mobility":"Movable","intensity":5000,"intensityUnits":"Unitless",
 "sourceRadius":10,"attenuationRadius":1200,
 "lightColor":{"r":1,"g":0.6666666865348816,"b":0.3529411852359772,"a":1},
 "castShadows":true}
```

Internal names:

| Label | Internal name |
|---|---|
| `Torch_1F_W_1` | `PointLight_UAID_9C6B005AF86943FE02_1815541528` |
| `Torch_1F_W_2` | `PointLight_UAID_9C6B005AF86943FE02_1815609529` |
| `Torch_1F_E_1` | `PointLight_UAID_9C6B005AF86943FE02_1815703530` |
| `Torch_1F_E_2` | `PointLight_UAID_9C6B005AF86943FE02_1815836531` |
| `Torch_2F_N_1` | `PointLight_UAID_9C6B005AF86943FE02_1816014532` |
| `Torch_2F_N_2` | `PointLight_UAID_9C6B005AF86943FE02_1816153533` |

Folder membership was verified by calling `get_actors_in_folder("Lighting",
recursive: true)` and testing each refPath for set membership, not by trusting
the `set_actor_folder` return value.

---

## B) The 13 pre-existing lights are unchanged

Read back after all 6 creations and compared against the pre-write baseline.

| Label | Intensity | Location | vs baseline |
|---|---|---|---|
| `Torch_1F_S_1` | `5000` | `(-1050, -1200, 250)` | **identical** |
| `Torch_1F_S_2` | `5000` | `(-1050, -400, 250)` | **identical** |
| `Torch_1F_S_3` | `5000` | `(-1050, 400, 250)` | **identical** |
| `Torch_1F_S_4` | `5000` | `(-1050, 1200, 250)` | **identical** |
| `Torch_1F_N_1` | `5000` | `(1050, -1200, 250)` | **identical** |
| `Torch_1F_N_2` | `5000` | `(1050, -400, 250)` | **identical** |
| `Torch_1F_N_3` | `5000` | `(1050, 400, 250)` | **identical** |
| `Torch_1F_N_4` | `5000` | `(1050, 1200, 250)` | **identical** |
| `Torch_2F_W_1` | `5000` | `(-700, -1350, 850)` | **identical** |
| `Torch_2F_W_2` | `5000` | `(300, -1350, 850)` | **identical** |
| `Torch_2F_E_1` | `5000` | `(-700, 1350, 850)` | **identical** |
| `Torch_2F_E_2` | `5000` | `(300, 1350, 850)` | **identical** |
| `KeyLight_FinalDoor` | `20000` | `(1000, 0, 900)` | **identical** |

"Identical" is not limited to the two columns shown. For each of the 13 the
comparison covers location, rotation, `mobility`, `intensity`, `intensityUnits`,
`sourceRadius`, `attenuationRadius`, `lightColor` and `castShadows`, plus the
refPath and the outliner folder. Every field matches the baseline exactly,
including the float32 colour values `0.6666666865348816` and `0.3529411852359772`
reproduced bit-for-bit.

**`KeyLight_FinalDoor` in particular is untouched** at Intensity `20000`,
AttenuationRadius `2500`, location `(1000, 0, 900)` — still the only light in the
level with different values from the torches. The two new `Torch_2F_N_*` lights
sit near it at `(1050, ±400, 850)` but are separate actors with separate
refPaths; nothing was written to the key light.

Aggregate over all 19 lights now in the level:

```json
{"all_ok": true, "missing": [], "dupes": [], "light_count": 19}
```

`dupes: []` confirms no label resolves to two actors — the 6 new labels did not
collide with anything. `missing: []` confirms all 19 expected labels were found.

Corroborating this independently: **the save modified zero tracked files.** Every
actor in this World Partition level has its own package, so if any of the 13
lights — or the DirectionalLight, SkyLight, SkyAtmosphere, VolumetricCloud,
ExponentialHeightFog, PostProcessVolume, or any wall, floor, door, ramp, railing,
pillar or mesh — had been altered in any way, its package would have been dirty
and written. `git status` shows **not one ` M` entry.**

---

## C) Actor count

| | Count |
|---|---|
| Before | **115** |
| After | **121** |
| Delta | **+6** |

**Exactly 6 added, as expected.** Nothing deleted. Corroborated by the save
writing exactly 6 packages and by the editor's validator reporting 6 associated
objects.

The `Lighting` outliner folder now holds **26** actors: 7 pre-existing
environment/lighting actors + 13 from command 49 + these 6.

---

## D) Packages written to disk

`AssetTools.save_assets` with `[]` returned `{"returnValue":true}`. `save_actor`
was **not** used, per the instruction and per command 47's finding that it fails
on external actor packages that do not exist yet.

**Exactly 6 packages, all new**, all written at `2026-09-03 20:06:50`:

```
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/PZ/68A4RY02IXX8CBJQS7ERCZ.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/8/C0/WLY15WGVH1FUO5DR4S2EWW.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/C/66/J2GZ3QU79B85EDE19M9QQH.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/D/LE/0U4ALFPFVU9N12U74AC51M.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/5/O2/MO2UNWUFENDGG3OJYPQJ7T.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/EO/74A1FMG5JLTS2WNL2U7TYE.uasset
```

The package names are content-hash style IDs and no tool exposes a label→package
mapping, so **I cannot say which file is which light and am not going to guess.**
What is certain is that there are exactly 6, all new, written in the same save as
the 6 new lights.

Verified four ways, none of them the tool's return value:

1. **A `find` for every file under `Content` modified in the last 5 minutes
   returned those 6 paths and nothing else.**
2. External actor file count went **151 → 157**, exactly `+6`.
3. `git status --porcelain` filtered for modified tracked files returns
   **nothing** — zero ` M` entries. Only 6 new untracked package directories
   appeared, on top of the 14 already untracked from commands 48 and 49 which are
   not yet committed.
4. The editor log — exactly 6 `Saving Package` lines, and the validator count
   matching:
   ```
   [2026.09.03-11.06.50:738][137]LogFileHelpers: Saving Package: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/PZ/68A4RY02IXX8CBJQS7ERCZ
   [2026.09.03-11.06.50:747][137]LogFileHelpers: Saving Package: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/8/C0/WLY15WGVH1FUO5DR4S2EWW
   [2026.09.03-11.06.50:763][137]LogFileHelpers: Saving Package: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/C/66/J2GZ3QU79B85EDE19M9QQH
   [2026.09.03-11.06.50:770][137]LogFileHelpers: Saving Package: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/D/LE/0U4ALFPFVU9N12U74AC51M
   [2026.09.03-11.06.50:776][137]LogFileHelpers: Saving Package: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/5/O2/MO2UNWUFENDGG3OJYPQJ7T
   [2026.09.03-11.06.50:781][137]LogFileHelpers: Saving Package: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/EO/74A1FMG5JLTS2WNL2U7TYE
   [2026.09.03-11.06.51:041][138]LogContentValidation: Display: Starting to validate 1 assets (6 associated objects such as actors)
   ```

**`Lvl_Stage.umap` was not written** — still mtime
`2026-09-03 09:47:04.791203000 +0900`, still 12,824 bytes, absent from
`git status`. Correct for a World Partition level.

### Still uncommitted

`git status` currently carries **20 untracked package directories**: 1 from
command 48 (the ceiling slab), 13 from command 49 (the first light set), and 6
from this command. Plus three untracked report files
(`2026-09-03-48-…`, `-49-…`, and this one). Commands 48, 49 and 50 are all on
disk but none is committed yet.

---

## E) Warnings and errors

**No warning and no error was emitted by this command.**

This command's work runs from `11:05:59` (the first `execute_tool_script`
dispatch that created the lights) through `11:06:51` (end of save validation):

```
[2026.09.03-11.05.59:215][429]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script'
[2026.09.03-11.06.22:992][ 54]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script'
[2026.09.03-11.06.50:660][137]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.asset.AssetTools.save_assets'
```

Filtering the entire session log for `Warning`, `Error` and `Failed`, the most
recent matching entry is at **`10:52:22`**, roughly thirteen minutes before this
command began, and it belongs to command 49:

```
[2026.09.03-10.52.22:712][812]LogScript: Warning: GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.DirectionalLight_UAID_F4A475FF15A3736A02_1961932697.LightComponent0' (DirectionalLightComponent): the following properties could not be read: intensityUnits
```

Nothing was added to that list by this command. In particular there were **no
`LogJson` schema warnings** this time, because no `list_properties` call was
needed — the point light schema was already known from command 49.

For completeness, every other warning still in the recent log predates this
command and was not caused by it:

```
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+b9cc, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+b9cc, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c2e4, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:497][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c2e4, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:497][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c81c, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.22.28:497][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c81c, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-10.31.28:203][324]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
[2026.09.03-10.45.26:720][932]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
[2026.09.03-10.50.34:516][976]LogJson: Warning: Property "OnComponentDeactivated" type FActorComponentDeactivateSignature unhandled during Json schema generation.
[2026.09.03-10.50.34:516][976]LogJson: Warning: Property "OnComponentActivated" type FActorComponentActivatedSignature unhandled during Json schema generation.
[2026.09.03-10.50.34:516][976]LogJson: Warning: Property "PhysicsVolumeChangedDelegate" type FPhysicsVolumeChanged unhandled during Json schema generation.
```

The `LogSlate` entries are the terminal font lacking Hangul glyphs. The
`LogJson` entries are from command 49's `list_properties` call.

---

## The lobby light count is now 19

| Group | Count | Intensity |
|---|---|---|
| 1F wall torches (`Torch_1F_S_*`, `Torch_1F_N_*`) | 8 | 5000 |
| 1F doorway flanking torches (`Torch_1F_W_*`, `Torch_1F_E_*`) — **new** | 4 | 5000 |
| 2F gallery torches (`Torch_2F_W_*`, `Torch_2F_E_*`) | 4 | 5000 |
| 2F final-door flanking torches (`Torch_2F_N_*`) — **new** | 2 | 5000 |
| Key light (`KeyLight_FinalDoor`) | 1 | 20000 |
| **Total** | **19** | |

All four doorways now have a torch on each side, which was the goal.

---

## Not verified

- **No lighting was observed. This report still contains zero evidence about how
  the lobby looks.** Every value is a property read. Command 49's report raised
  this and it is still open — the lighting has never been looked at.
- **PIE was not run.**
- **No light was checked for being embedded inside geometry.** The placements are
  consistent with the wall bounds recorded in command 45 — the 1F doorway lights
  at Y ±1350 are 50 units clear of the wall inner faces at Y ∓1400, and the 2F
  ones at X 1050 are 50 clear of the face at X 1100 — but that is arithmetic from
  recorded numbers, not a trace or overlap query.
- **`Torch_1F_W_2` and `Torch_1F_E_2` sit at X 100, near the lobby's centre, and
  their 1200 attenuation radius reaches well past the doorways.** Whether they
  spill into rooms 1 and 3 was not measured.
- **`Torch_2F_N_1` and `Torch_2F_N_2` at `(1050, ±400, 850)` are close to
  `KeyLight_FinalDoor` at `(1000, 0, 900)`** — within about 400 units. Three
  overlapping shadow-casting lights in that corner may wash out the key light the
  instruction described as "the one dominant warm light the room reads from". Not
  measured, but worth looking at.
- **Shadow cost was not considered.** There are now 19 Movable shadow-casting
  point lights in one enclosed room, with heavily overlapping attenuation
  spheres. No profiling was done.
- **`bUseInverseSquaredFalloff` is still `true`** on all of them, as flagged in
  command 49. It was not part of this instruction so it was not changed.
- **Nothing was rebuilt** — no lighting build (not needed for Movable lights) and
  no navmesh rebuild.
