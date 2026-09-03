# 2026-09-03 · Command 52 — MI_Castle_Stone on the three prototype meshes

Asset change, in `/Game/LevelPrototyping/`. No level actor was touched.
**One MaterialInstanceConstant created with all 8 requested parameter overrides,
assigned to the `lambert1` slot on SM_Cube, SM_Cylinder and SM_Ramp, saved to
disk. 4 packages written: 1 new, 3 modified. Nothing else changed.**

**One thing needs your attention before this looks right: the `TopSurfaceColor`
static switch is `false` on the new instance, so the three "upward faces"
colours are stored but will not render.** Detail in its own section below.

Instruction, verbatim from the user:

> In the currently open project, create a stone MaterialInstance and put it on the three
> prototype meshes the level is built from.
>
> Do NOT author a new Material from scratch. /Game/LevelPrototyping/Materials/
> M_PrototypeGrid already exposes every parameter needed, including separate colours for
> upward-facing surfaces, so a MaterialInstance of it is enough.
>
> STEP 1 - Create a MaterialInstanceConstant.
>
>   Folder  /Game/LevelPrototyping/Materials
>   Name    MI_Castle_Stone
>   Parent  /Game/LevelPrototyping/Materials/M_PrototypeGrid
>
> STEP 2 - Set these parameters on it. Every one is an override on the instance.
>
>   Scalar parameters
>     Grid Size   200        (was 100 on MI_PrototypeGrid_Gray; 200 makes one block equal
>                             one 2 m floor tile, the module this level is built on)
>     Roughness   1.0
>
>   Vector parameters - side faces, i.e. walls
>     SurfaceColor          R 0.135  G 0.125  B 0.112
>     GridColor             R 0.045  G 0.042  B 0.038
>     SubGridColor          R 0.090  G 0.085  B 0.078
>
>   Vector parameters - upward faces, i.e. floors and the ceiling underside
>     TopSurfaceColor       R 0.115  G 0.110  B 0.102
>     TopGridColor          R 0.040  G 0.038  B 0.035
>     TopSubGridGridColor   R 0.080  G 0.076  B 0.070
>
>   If any of these parameter names does not exist on M_PrototypeGrid, do NOT guess a
>   different name. Report the exact list of parameter names the material actually exposes
>   and stop.
>
> STEP 3 - Assign it to the material slot of the three meshes the level geometry uses.
> All three currently point at MI_PrototypeGrid_Gray on a slot named "lambert1".
>
>   /Game/LevelPrototyping/Meshes/SM_Cube        slot lambert1
>   /Game/LevelPrototyping/Meshes/SM_Cylinder    slot lambert1
>   /Game/LevelPrototyping/Meshes/SM_Ramp        slot lambert1
>
> DO NOT touch SM_Door, M_FlatCol, MI_DefaultColorway, or any of the existing
> MI_PrototypeGrid_* instances - leave all of them exactly as they are. DO NOT set a
> material override on any actor. DO NOT edit any Blueprint, move any actor, or change any
> light.
>
> STEP 4 - Save with AssetTools.save_assets and an empty list. Report which packages were
> written, verified on disk and not from the return value.
>
> VERIFY AND REPORT.
>
>   A) Read back MI_Castle_Stone and report its Parent plus every scalar and vector
>      parameter override it now carries, with values. Say for each whether it matches
>      what was asked.
>
>   B) Read back the material assigned to slot lambert1 on SM_Cube, SM_Cylinder and
>      SM_Ramp and confirm all three are MI_Castle_Stone.
>
>   C) Read back SM_Door's slot Material_0 and confirm it is still M_FlatCol, and read
>      back MI_PrototypeGrid_Gray's parameters and confirm they are unchanged.
>
>   D) Report EditorToolset.EditorAppToolset.IsPIERunning. If it returns true, stop before
>      making any change and say so - with PIE running the tools resolve against the
>      UEDPIE_0_ copy of the world, not the editor world.
>
>   E) Report which packages were written to disk.
>
>   F) Report any warning or error text verbatim in English. Do not summarize or translate.
>
> Write the report to Docs/Terminal-Log/2026-09-03-52-castle-stone-material.md
> (a repo path - do NOT write under Saved/, it is gitignored).

---

## D) PIE state — checked first, before any change

`EditorToolset.EditorAppToolset.IsPIERunning`:

```json
{"returnValue":false}
```

**PIE is not running**, so the tools resolve against the editor world and it was
safe to proceed. This was the very first call this command made, before the
parameter list was even queried.

(For context: command 51 was halted on its first attempt because this returned
`true`. That check is now the first thing done in any command that writes.)

---

## STEP 1 gate — the parameter names all exist

The instruction said to report the exposed names and stop if any requested name
does not exist. `MaterialInstanceTools.list_parameters` on
`M_PrototypeGrid` returns **14 parameters**, verbatim:

| Type | Name |
|---|---|
| Scalar | `Roughness` |
| Scalar | `Grid Size` |
| Scalar | `Sub Grid Number` |
| Scalar | `CircleSize` |
| Vector | `SurfaceColor` |
| Vector | `TopGridColor` |
| Vector | `GridColor` |
| Vector | `TopSurfaceColor` |
| Vector | `TopSubGridGridColor` |
| Vector | `SubGridColor` |
| Vector | `Line Dimensions` |
| StaticSwitch | `TopSurfaceColor` |
| StaticSwitch | `ObjectAligned` |
| StaticSwitch | `Grid` |

**All 8 requested names exist, spelled exactly as the instruction wrote them** —
including `Grid Size` with its space and the oddly doubled `TopSubGridGridColor`.
Nothing was guessed and there was no need to stop.

Note for later: `TopSurfaceColor` appears **twice** — once as a Vector and once as
a StaticSwitch. That collision is the subject of the warning section below.

`MI_Castle_Stone` did not already exist (`AssetTools.exists` → `false`), so
nothing was overwritten.

---

## Pre-flight baseline

Read before any write, so sections B and C rest on a real comparison.

| Mesh | Slots | Material |
|---|---|---|
| `SM_Cube` | `["lambert1"]` | `MI_PrototypeGrid_Gray` |
| `SM_Cylinder` | `["lambert1"]` | `MI_PrototypeGrid_Gray` |
| `SM_Ramp` | `["lambert1"]` | `MI_PrototypeGrid_Gray` |
| `SM_Door` | `["Material_0"]` | `M_FlatCol` |

Every premise in the instruction checks out: the three meshes each have exactly
one slot named `lambert1` pointing at `MI_PrototypeGrid_Gray`, and SM_Door's slot
is `Material_0` on `M_FlatCol`.

`MI_PrototypeGrid_Gray` baseline (parent `M_PrototypeGrid`):

```json
{"scalars":{"Roughness":1,"Grid Size":100,"Sub Grid Number":5,"CircleSize":100},
 "vectors":{"SurfaceColor":[0.18000000715255737,0.18000000715255737,0.18000000715255737,1],
            "GridColor":[0.026041999459266663,...,1],
            "SubGridColor":[0.08854199945926666,...,1],
            "TopSurfaceColor":[0.04800000041723251,...,1],
            "TopGridColor":[0,0,0,1],
            "TopSubGridGridColor":[0.16770799458026886,...,1],
            "Line Dimensions":[0.021838000044226646,0.0013470000121742487,0.5,0]},
 "switches":{"TopSurfaceColor":false,"ObjectAligned":false,"Grid":true}}
```

This confirms the instruction's parenthetical — `Grid Size` **was** 100 on
`MI_PrototypeGrid_Gray`.

---

## The write

- `MaterialInstanceTools.create`, folder `/Game/LevelPrototyping/Materials`,
  name `MI_Castle_Stone`, parent `M_PrototypeGrid`. Returned
  `{"refPath":"/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone"}`.
- `set_scalar_parameter` ×2, `set_vector_parameter` ×6. All returned
  `{"returnValue": null}` — this toolset returns null on success rather than
  `true`, so the return values carry no information either way and everything
  below is a read-back.
- `set_material` ×3 on the three meshes, each guarded by a check that the mesh's
  slot list was exactly `["lambert1"]` before writing. All three returned `true`.

**A decision I made that the instruction did not specify:** the vector setter
requires a LinearColor with an alpha channel, but the instruction gave only RGB.
**I used `a = 1.0` for all six colours**, matching the convention of every
existing colour on `MI_PrototypeGrid_Gray` (all `a = 1`). Alpha is unused by these
grid-colour inputs, but the value is mine, not yours.

No `set_static_switch_parameter` call was made, no override was set on any actor,
no Blueprint was opened, no actor was moved, no light was touched.

---

## A) MI_Castle_Stone, read back

**Parent:** `/Game/LevelPrototyping/Materials/M_PrototypeGrid.M_PrototypeGrid` ✓
as asked.

### Scalar overrides

| Parameter | Value | Asked | Match |
|---|---|---|---|
| `Grid Size` | `200` | 200 | **✓** |
| `Roughness` | `1` | 1.0 | **✓** |

### Vector overrides — side faces (walls)

| Parameter | Value (R, G, B, A) | Asked (R, G, B) | Match |
|---|---|---|---|
| `SurfaceColor` | `0.13500000536441803, 0.125, 0.1120000034570694, 1` | 0.135, 0.125, 0.112 | **✓** |
| `GridColor` | `0.04500000178813934, 0.041999999433755875, 0.03799999877810478, 1` | 0.045, 0.042, 0.038 | **✓** |
| `SubGridColor` | `0.09000000357627869, 0.08500000089406967, 0.07800000160932541, 1` | 0.090, 0.085, 0.078 | **✓** |

### Vector overrides — upward faces (floors, ceiling underside)

| Parameter | Value (R, G, B, A) | Asked (R, G, B) | Match |
|---|---|---|---|
| `TopSurfaceColor` | `0.11500000208616257, 0.10999999940395355, 0.10199999809265137, 1` | 0.115, 0.110, 0.102 | **✓** |
| `TopGridColor` | `0.03999999910593033, 0.03799999877810478, 0.03500000014901161, 1` | 0.040, 0.038, 0.035 | **✓** |
| `TopSubGridGridColor` | `0.07999999821186066, 0.07599999755620956, 0.07000000029802322, 1` | 0.080, 0.076, 0.070 | **✓** |

```json
{"all_params_ok": true}
```

**All 8 match.** The comparison was done with a tolerance of `1e-6` per channel,
not by eye. The trailing digits are float32 representation of the decimal values
requested — e.g. `0.13500000536441803` is the nearest float to `0.135`. No value
drifted.

### Parameters left inherited from the parent, not overridden

These were not in the instruction and were not touched:

| Parameter | Effective value |
|---|---|
| `Sub Grid Number` | `5` |
| `CircleSize` | `100` |
| `Line Dimensions` | `0.021838000044226646, 0.0013470000121742487, 0.5, 0` |

### Static switches — inherited, and one of them matters

| Switch | Value |
|---|---|
| `TopSurfaceColor` | **`false`** |
| `ObjectAligned` | `false` |
| `Grid` | `true` |

---

## The problem: the "upward faces" colours will not render

The instruction's stated reason for using this parent was that it exposes
"separate colours for upward-facing surfaces". **It does — but that feature is
gated behind a static switch that is currently off on the new instance.**

`M_PrototypeGrid` exposes `TopSurfaceColor` twice: once as a **Vector** (the
colour) and once as a **StaticSwitch** (the on/off for the whole top-surface
branch). The three Top\* colours were written correctly, but the switch reads
`false`, inherited from the parent material's default.

Evidence that the switch is what gates the feature — a read-only comparison
across every `MI_PrototypeGrid_*` instance in the project:

| Instance | `TopSurfaceColor` switch | Vector `TopSurfaceColor` | Vector `SurfaceColor` |
|---|---|---|---|
| `MI_PrototypeGrid_Gray` | `false` | 0.048, 0.048, 0.048 | 0.18, 0.18, 0.18 |
| `MI_PrototypeGrid_Gray_02` | `false` | 0.048, 0.048, 0.048 | 0.18, 0.18, 0.18 |
| **`MI_PrototypeGrid_TopDark`** | **`true`** | 0.06, 0.06, 0.06 | 0.18, 0.18, 0.18 |
| `MI_Castle_Stone` (new) | `false` | 0.115, 0.11, 0.102 | 0.135, 0.125, 0.112 |

`MI_PrototypeGrid_TopDark` — the one stock instance whose *name* says it has a
dark top — is the **only** one with that switch enabled, and it is otherwise
identical to Gray apart from the top colour. That is as direct a demonstration as
the project offers: the switch turns the top-colour branch on.

**Consequence:** as saved, floors, stair treads and the lobby ceiling underside
will render with the **side-face** colours (`SurfaceColor` 0.135/0.125/0.112 and
its grid colours), not the slightly darker top set. The material will still look
like stone and the Grid Size 200 change still applies everywhere — but the
floor/wall distinction the instruction was after is not there.

**I did not fix this.** Two reasons: the instruction listed exactly 8 parameters
and said every one is an override on the instance, and changing a static switch is
a different kind of edit that triggers a shader recompile — the toolset
documentation says so explicitly. Flipping it was not authorised.

**The fix, if you want it, is one call:**
`MaterialInstanceTools.set_static_switch_parameter` on `MI_Castle_Stone`, name
`TopSurfaceColor`, value `true`. Say the word and I'll run it and re-verify.

---

## B) The three meshes

| Mesh | Slot | Material after | Confirmed |
|---|---|---|---|
| `SM_Cube` | `lambert1` | `/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone` | **✓** |
| `SM_Cylinder` | `lambert1` | `/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone` | **✓** |
| `SM_Ramp` | `lambert1` | `/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone` | **✓** |

```json
{"three_meshes_ok": true}
```

**All three are MI_Castle_Stone.** Each still has exactly one slot, still named
`lambert1` — the slot was reassigned, not renamed or added to.

This is an **asset-level** change, so it reaches every actor that does not
override the slot. That is deliberate and is what the instruction asked for; no
per-actor override was set on anything.

---

## C) What had to stay unchanged

### SM_Door

| Slot | Material | Confirmed |
|---|---|---|
| `Material_0` | `/Game/LevelPrototyping/Materials/M_FlatCol.M_FlatCol` | **✓ unchanged** |

```json
{"door_unchanged": true}
```

### MI_PrototypeGrid_Gray

Re-read after all writes and compared field by field against the pre-write
baseline:

```json
{"gray_unchanged": true}
```

| | Value | vs baseline |
|---|---|---|
| `Roughness` | `1` | identical |
| `Grid Size` | `100` | identical |
| `Sub Grid Number` | `5` | identical |
| `CircleSize` | `100` | identical |
| `SurfaceColor` | `0.18000000715255737` ×3 | identical |
| `GridColor` | `0.026041999459266663` ×3 | identical |
| `SubGridColor` | `0.08854199945926666` ×3 | identical |
| `TopSurfaceColor` | `0.04800000041723251` ×3 | identical |
| `TopGridColor` | `0, 0, 0` | identical |
| `TopSubGridGridColor` | `0.16770799458026886` ×3 | identical |
| switch `TopSurfaceColor` | `false` | identical |
| switch `ObjectAligned` | `false` | identical |
| switch `Grid` | `true` | identical |

**`MI_PrototypeGrid_Gray` is untouched. Its Grid Size is still 100** — the 200 is
only on the new instance, as intended.

`M_FlatCol`, `MI_DefaultColorway`, `MI_PrototypeGrid_TopDark`,
`MI_PrototypeGrid_Gray_02` and `MI_PrototypeGrid_Gray_Round` were read but never
written. Section E proves this at the file level: none of their packages was
saved.

---

## E) Packages written to disk

`AssetTools.save_assets` with `[]` returned `{"returnValue":true}`. That is not
what this rests on. A full listing of every `.uasset` under `Content` was captured
before the save and diffed against one taken after.

| | Count |
|---|---|
| `.uasset` files before | **357** |
| `.uasset` files after | **358** |

**Added — exactly one:**

```
Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset
```

**Removed: none.**

**Modified — exactly three**, by mtime and by git:

```
2026-09-03 20:38:44.4433726000  Content/LevelPrototyping/Meshes/SM_Cube.uasset
2026-09-03 20:38:44.4872934000  Content/LevelPrototyping/Meshes/SM_Cylinder.uasset
2026-09-03 20:38:44.5170202000  Content/LevelPrototyping/Meshes/SM_Ramp.uasset
2026-09-03 20:38:44.5333789000  Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset
```

A `find` for anything under `Content` modified in the last 5 minutes returned
exactly those four paths and nothing else.

`git status --porcelain`:

```
 M Content/LevelPrototyping/Meshes/SM_Cube.uasset
 M Content/LevelPrototyping/Meshes/SM_Cylinder.uasset
 M Content/LevelPrototyping/Meshes/SM_Ramp.uasset
?? Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset
```

**Four packages total: three modified, one new.** Crucially, the following do
**not** appear anywhere in that list, which is the file-level proof they were left
alone: `MI_PrototypeGrid_Gray.uasset`, `MI_PrototypeGrid_Gray_02.uasset`,
`MI_PrototypeGrid_Gray_Round.uasset`, `MI_PrototypeGrid_TopDark.uasset`,
`M_FlatCol.uasset`, `MI_DefaultColorway.uasset`, `M_PrototypeGrid.uasset`,
`SM_Door.uasset`, and every `__ExternalActors__` package (no level actor changed).

Confirmed in the editor log — exactly four `Saving Package` lines:

```
[2026.09.03-11.38.44:401][939]LogFileHelpers: Saving Package: /Game/LevelPrototyping/Meshes/SM_Cube
[2026.09.03-11.38.44:444][939]LogFileHelpers: Saving Package: /Game/LevelPrototyping/Meshes/SM_Cylinder
[2026.09.03-11.38.44:487][939]LogFileHelpers: Saving Package: /Game/LevelPrototyping/Meshes/SM_Ramp
[2026.09.03-11.38.44:518][939]LogFileHelpers: Saving Package: /Game/LevelPrototyping/Materials/MI_Castle_Stone
```

Content validation ran clean on exactly those four, with zero failures across
nine validators:

```
[2026.09.03-11.38.44:581][940]LogContentValidation: Display: Starting to validate 4 assets (0 associated objects such as actors)
[2026.09.03-11.38.44:581][940]AssetCheck: /Game/LevelPrototyping/Meshes/SM_Cube Validating asset
[2026.09.03-11.38.44:582][940]AssetCheck: /Game/LevelPrototyping/Meshes/SM_Cylinder Validating asset
[2026.09.03-11.38.44:582][940]AssetCheck: /Game/LevelPrototyping/Meshes/SM_Ramp Validating asset
[2026.09.03-11.38.44:582][940]AssetCheck: /Game/LevelPrototyping/Materials/MI_Castle_Stone Validating asset
[2026.09.03-11.38.44:582][940]LogContentValidation:   /Script/DataValidation.EditorValidator_Material : 0
[2026.09.03-11.38.44:582][940]LogContentValidation:   /Script/DataValidation.PackageFileValidator : 0
```

`0 associated objects such as actors` independently confirms no level actor was
involved.

---

## F) Warnings and errors, verbatim

This command's work runs from `11:36:02` (the `list_parameters` call) to
`11:38:44` (end of save validation). **Exactly one warning falls in that window,
caused by one of my own read calls.**

The tool returned this error, which aborted a baseline read and forced a retry:

```
Parameter error: /Game/LevelPrototyping/Materials/M_PrototypeGrid.M_PrototypeGrid is not valid MaterialInstanceConstant for property 'instance'.
```

The same thing in the editor log, with its stack, verbatim:

```
[2026.09.03-11.36.38:175][525]LogScript: Warning: /Game/LevelPrototyping/Materials/M_PrototypeGrid.M_PrototypeGrid is not valid MaterialInstanceConstant for property 'instance'
	PythonGeneratedClass /EditorToolset/Python/editor_toolset/toolsets/material_instance_PY.MaterialInstanceTools
	Function /EditorToolset/Python/editor_toolset/toolsets/material_instance_PY.MaterialInstanceTools:get_scalar_parameter:64X
```

**Cause, and it is a tool limitation worth knowing:** `get_scalar_parameter`,
`get_vector_parameter` and `get_static_switch_parameter` accept only a
`MaterialInstanceConstant`. They **cannot read a base Material**, so
`M_PrototypeGrid`'s own default parameter values cannot be read through this
toolset at all. `list_parameters` accepts a `MaterialInterface` and does work on
the base material, which is why the STEP 1 gate could be checked. This is a
read-only failure — it read nothing and wrote nothing, and the baseline was
re-taken without the parent.

**No error and no other warning was emitted.** In particular the create, the 8
parameter writes, the 3 material assignments and the save produced nothing.

### Predating this command

The most recent non-`LogSlate` warning before this command is at `11:18:53`,
about seventeen minutes earlier, from command 51's PIE teardown:

```
[2026.09.03-11.18.53:347][  2]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
```

`LogSlate` "Could not find Glyph Index" warnings continue to appear whenever
Korean text is rendered in the terminal; they are a font issue and have nothing to
do with the project.

---

## Not verified

- **Nothing was looked at. No viewport capture, no PIE, no render.** Every value
  in this report is a property read or a file listing. **Whether the level now
  looks like stone is completely unverified** — and given the static switch
  finding above, at least one aspect of the intended look is definitely not
  there.
- **The colours were not evaluated as colours.** `0.135, 0.125, 0.112` is a dark
  warm grey in linear space; whether it reads as "castle stone" under the 18
  torches from commands 49–50 is a judgement no number here supports. Note these
  are *linear* values, so they will look considerably lighter on screen than the
  decimals suggest.
- **`Grid Size 200` was not checked against the actual geometry.** The
  instruction's reasoning — that 200 makes one grid block equal one 2 m floor
  tile — is consistent with the level's 200-unit doorway module recorded in
  commands 45–47, but no measurement was made of how the grid actually lands on a
  wall face.
- **The knock-on scope of the mesh assignment was not enumerated.** SM_Cube,
  SM_Cylinder and SM_Ramp are used by far more than the lobby — every wall,
  floor, ramp and railing in rooms 1, 2 and 3 uses them too. **This change
  restyles the entire level, not just the lobby.** That follows from the
  instruction as written, but no count was made of how many actors are affected.
- **No shader recompile was triggered or observed.** Only scalar and vector
  parameters were set, which do not require one. Had the static switch been
  flipped, it would have.
- **`M_PrototypeGrid`'s own default parameter values were never read**, for the
  tool reason in section F. So "inherited" values reported in section A are the
  instance's effective values, which is the same thing, but the parent's defaults
  were not independently confirmed.
