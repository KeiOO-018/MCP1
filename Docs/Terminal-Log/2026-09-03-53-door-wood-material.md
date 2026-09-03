# 2026-09-03 · Command 53 — MI_Castle_Wood on SM_Door

Asset change, in `/Game/LevelPrototyping/`. No level actor was touched.
**One MaterialInstanceConstant created with both requested parameter overrides,
assigned to SM_Door's only slot, saved to disk. 2 packages written: 1 new, 1
modified. Nothing else changed. No warning or error was emitted by this command.**

Instruction, verbatim from the user:

> In the currently open project, give the door leaves a wood material.
>
> SM_Door (/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door) currently points its
> only slot, "Material_0", directly at the material /Game/LevelPrototyping/Materials/
> M_FlatCol with no instance in between, so all four doors render as a flat grey slab. In
> the now-dark lobby that reads as a hole rather than a door.
>
> STEP 1 - Create a MaterialInstanceConstant.
>
>   Folder  /Game/LevelPrototyping/Materials
>   Name    MI_Castle_Wood
>   Parent  /Game/LevelPrototyping/Materials/M_FlatCol
>
> STEP 2 - Set these parameters on it.
>
>   Vector parameter
>     Base Color   R 0.055  G 0.032  B 0.018
>
>   Scalar parameter
>     Roughness    0.75
>
>   The parameter is named "Base Color" with a space - that is the name
>   MI_DefaultColorway uses on this same parent. If either name does not exist, do NOT
>   guess a different one: report the exact list of parameters M_FlatCol exposes and stop.
>
> STEP 3 - Assign MI_Castle_Wood to SM_Door, slot "Material_0".
>
> DO NOT modify M_FlatCol itself, MI_DefaultColorway, MI_Castle_Stone,
> MI_PrototypeGrid_Gray or any other existing material. DO NOT touch SM_Cube, SM_Cylinder
> or SM_Ramp. DO NOT edit any Blueprint, move any actor, or change any light.
>
> STEP 4 - Save with AssetTools.save_assets and an empty list. Report which packages were
> written, verified on disk and not from the return value.
>
> VERIFY AND REPORT.
>
>   A) Report EditorToolset.EditorAppToolset.IsPIERunning first. If it returns true, make
>      no change and stop - with PIE running the tools resolve against the UEDPIE_0_ copy
>      of the world rather than the editor world.
>
>   B) Read back MI_Castle_Wood and report its Parent and every parameter override with
>      values, saying whether each matches what was asked.
>
>   C) Read back SM_Door slot Material_0 and confirm it is MI_Castle_Wood.
>
>   D) Read back M_FlatCol and MI_DefaultColorway and confirm neither changed. Report
>      MI_DefaultColorway's Base Color and Roughness.
>
>   E) Report which packages were written to disk.
>
>   F) Report any warning or error text verbatim in English. Do not summarize or translate.
>
> Write the report to Docs/Terminal-Log/2026-09-03-53-door-wood-material.md
> (a repo path - do NOT write under Saved/, it is gitignored).

---

## A) PIE state — checked first, before any change

`EditorToolset.EditorAppToolset.IsPIERunning`:

```json
{"returnValue":false}
```

**PIE is not running**, so the tools resolve against the editor world and it was
safe to proceed. This was the first call of the command, dispatched at
`12:04:04`, before the parameter list was even queried.

---

## STEP 2 gate — both parameter names exist

The instruction said to report the exposed parameters and stop if either name is
absent. `MaterialInstanceTools.list_parameters` on `M_FlatCol` returns **exactly
three** parameters, verbatim:

| Type | Name |
|---|---|
| Scalar | `Metallic` |
| Scalar | `Roughness` |
| Vector | `Base Color` |

**Both requested names exist, spelled exactly as asked** — `Base Color` with its
space, and `Roughness`. Nothing was guessed and there was no need to stop.

The instruction's supporting claim also checks out: `MI_DefaultColorway`'s parent
is `M_FlatCol`, and it carries values on both of those names.

`MI_Castle_Wood` did not already exist (`AssetTools.exists` → `false`), so
nothing was overwritten.

Note the third parameter, `Metallic`, was not in the instruction and was
deliberately left inherited.

---

## Pre-flight baseline

Read before any write, so section D rests on a real comparison rather than
inference.

| Asset | Value |
|---|---|
| `SM_Door` slots | `["Material_0"]` |
| `SM_Door` `Material_0` | `/Game/LevelPrototyping/Materials/M_FlatCol.M_FlatCol` |
| `MI_DefaultColorway` parent | `M_FlatCol` |
| `MI_DefaultColorway` `Base Color` | `0.528689980506897, 0.528689980506897, 0.528689980506897, 1` |
| `MI_DefaultColorway` `Roughness` | `0.2680000066757202` |
| `MI_DefaultColorway` `Metallic` | `0` |
| `MI_Castle_Stone` `Grid Size` | `200` |
| `MI_PrototypeGrid_Gray` `Grid Size` | `100` |
| `SM_Cube` / `SM_Cylinder` / `SM_Ramp` `lambert1` | `MI_Castle_Stone` (all three) |

**The instruction's premise is confirmed exactly:** SM_Door has one slot,
`Material_0`, pointing **directly at the base material** `M_FlatCol` with no
instance in between. That is unusual — every other mesh in the project goes
through an instance — and it is why the doors had no independent colour control
before this command.

---

## The write

- `MaterialInstanceTools.create`, folder `/Game/LevelPrototyping/Materials`, name
  `MI_Castle_Wood`, parent `M_FlatCol`. Returned
  `{"refPath":"/Game/LevelPrototyping/Materials/MI_Castle_Wood.MI_Castle_Wood"}`.
- `set_vector_parameter` `Base Color` → `(0.055, 0.032, 0.018, 1.0)`.
- `set_scalar_parameter` `Roughness` → `0.75`.
  Both returned `{"returnValue": null}` — this toolset returns null on success,
  so the return values carry no information and everything below is a read-back.
- `set_material` on SM_Door slot `Material_0`, guarded by a check that the slot
  list was exactly `["Material_0"]` first. Returned `true`.

**A decision I made that the instruction did not specify:** the vector setter
requires an alpha channel but the instruction gave only RGB. **I used `a = 1.0`**,
matching `MI_DefaultColorway` on this same parent, which also has `a = 1`. The
value is mine, not yours. This is the same call I made in command 52.

No other tool that modifies state was called. No Blueprint was opened, no actor
moved, no light touched, no per-actor material override set.

---

## B) MI_Castle_Wood, read back

**Parent:** `/Game/LevelPrototyping/Materials/M_FlatCol.M_FlatCol` ✓ as asked.

| Parameter | Type | Value | Asked | Match |
|---|---|---|---|---|
| `Base Color` | Vector | `0.054999999701976776, 0.03200000151991844, 0.017999999225139618, 1` | R 0.055, G 0.032, B 0.018 | **✓** |
| `Roughness` | Scalar | `0.75` | 0.75 | **✓** |

Both compared with a tolerance of `1e-6` per channel, not by eye; both passed.
The trailing digits are the float32 representation of the requested decimals —
`0.054999999701976776` is the nearest float to `0.055`. Nothing drifted.

**Inherited, not overridden:**

| Parameter | Effective value |
|---|---|
| `Metallic` | `0` |

`Metallic` was not in the instruction, so it was left to inherit from the parent.
It reads `0`, which is correct for wood — a metallic value above 0 would have made
the doors look like painted metal.

---

## C) SM_Door

| Slot | Material after | Confirmed |
|---|---|---|
| `Material_0` | `/Game/LevelPrototyping/Materials/MI_Castle_Wood.MI_Castle_Wood` | **✓** |

```json
{"door_ok": true}
```

SM_Door still has exactly one slot, still named `Material_0` — the slot was
reassigned, not renamed or added to. It now goes through an instance instead of
pointing at the base material directly, which is the structural change that makes
the door colour independently controllable.

This is an **asset-level** change, so it reaches all four door actors
(`Door_R1`, `Door_R2`, `Door_R3`, `Door_Final`) plus any other user of SM_Door.
No per-actor override was set on anything.

---

## D) What had to stay unchanged

### M_FlatCol

**Unchanged.** No write tool was ever called against it — the only calls touching
it were `list_parameters` (read) and its use as the `parent` argument when
creating the instance, which reads it but does not modify it.

Confirmed at the file level in section E: `M_FlatCol.uasset` was **not** among the
packages written. If it had been modified it would have been dirty and saved.

**A tool limitation worth restating:** `M_FlatCol`'s own parameter *values* could
not be read back, because `get_scalar_parameter` / `get_vector_parameter` accept
only a `MaterialInstanceConstant`, not a base Material. This was established in
command 52 and the same call was not retried here. So "M_FlatCol is unchanged"
rests on the file-level evidence and on no write having been issued, not on a
value comparison.

### MI_DefaultColorway

Re-read after all writes and compared field by field against the pre-write
baseline:

```json
{"dcw_unchanged": true}
```

| Property | Value | vs baseline |
|---|---|---|
| Parent | `M_FlatCol` | identical |
| **`Base Color`** | **`0.528689980506897, 0.528689980506897, 0.528689980506897`** | identical |
| **`Roughness`** | **`0.2680000066757202`** | identical |
| `Metallic` | `0` | identical |

**Unchanged.** Its `Base Color` is a mid grey and its `Roughness` is `0.268` —
notably different from the new instance's `0.75`, so the two instances of the same
parent are clearly distinct and neither leaked into the other.

### The command 52 assets, re-checked

Not required by the instruction, but checked because command 52's work was still
uncommitted and worth protecting:

| Asset | Value | Status |
|---|---|---|
| `MI_Castle_Stone` `Grid Size` | `200` | unchanged |
| `MI_Castle_Stone` `SurfaceColor` | `0.13500000536441803, 0.125, 0.1120000034570694` | unchanged |
| `MI_PrototypeGrid_Gray` `Grid Size` | `100` | unchanged |
| `MI_PrototypeGrid_Gray` `SurfaceColor` | `0.18000000715255737` ×3 | unchanged |
| `SM_Cube` `lambert1` | `MI_Castle_Stone` | unchanged |
| `SM_Cylinder` `lambert1` | `MI_Castle_Stone` | unchanged |
| `SM_Ramp` `lambert1` | `MI_Castle_Stone` | unchanged |

---

## E) Packages written to disk

`AssetTools.save_assets` with `[]` returned `{"returnValue":true}`. That is not
what this rests on. A full listing of every `.uasset` under `Content` was captured
before the save and diffed against one taken after.

| | Count |
|---|---|
| `.uasset` files before | **358** |
| `.uasset` files after | **359** |

**Added — exactly one:**

```
Content/LevelPrototyping/Materials/MI_Castle_Wood.uasset
```

**Removed: none.**

**Written by this command — exactly two**, and a `find` for anything under
`Content` modified in the last 4 minutes returned these and nothing else:

```
2026-09-03 21:05:21.7418246000  Content/LevelPrototyping/Interactable/Door/Meshes/SM_Door.uasset
2026-09-03 21:05:21.7759534000  Content/LevelPrototyping/Materials/MI_Castle_Wood.uasset
```

Confirmed in the editor log — exactly two `Saving Package` lines in this
command's window:

```
[2026.09.03-12.05.21:581][886]LogFileHelpers: Saving Package: /Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door
[2026.09.03-12.05.21:743][886]LogFileHelpers: Saving Package: /Game/LevelPrototyping/Materials/MI_Castle_Wood
```

Content validation ran clean on exactly those two, zero failures across nine
validators:

```
[2026.09.03-12.05.21:862][887]LogContentValidation: Display: Starting to validate 2 assets (0 associated objects such as actors)
[2026.09.03-12.05.21:862][887]AssetCheck: /Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door Validating asset
[2026.09.03-12.05.21:862][887]AssetCheck: /Game/LevelPrototyping/Materials/MI_Castle_Wood Validating asset
[2026.09.03-12.05.21:862][887]LogContentValidation:   /Script/DataValidation.EditorValidator_Material : 0
[2026.09.03-12.05.21:862][887]LogContentValidation:   /Script/DataValidation.PackageFileValidator : 0
```

`0 associated objects such as actors` independently confirms no level actor was
involved.

Crucially, none of these appear among the written packages, which is the
file-level proof they were left alone: `M_FlatCol.uasset`,
`MI_DefaultColorway.uasset`, `MI_Castle_Stone.uasset`,
`MI_PrototypeGrid_Gray.uasset`, `MI_PrototypeGrid_Gray_02.uasset`,
`MI_PrototypeGrid_Gray_Round.uasset`, `MI_PrototypeGrid_TopDark.uasset`,
`M_PrototypeGrid.uasset`, `SM_Cube.uasset`, `SM_Cylinder.uasset`,
`SM_Ramp.uasset`, and every `__ExternalActors__` package.

### Reading the working tree correctly

`git status --porcelain` after the save:

```
 M Content/LevelPrototyping/Interactable/Door/Meshes/SM_Door.uasset
 M Content/LevelPrototyping/Meshes/SM_Cube.uasset
 M Content/LevelPrototyping/Meshes/SM_Cylinder.uasset
 M Content/LevelPrototyping/Meshes/SM_Ramp.uasset
?? Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset
?? Content/LevelPrototyping/Materials/MI_Castle_Wood.uasset
?? Docs/Terminal-Log/2026-09-03-52-castle-stone-material.md
```

**Only two of those seven lines belong to this command** — `SM_Door.uasset` and
`MI_Castle_Wood.uasset`. The three mesh entries and `MI_Castle_Stone.uasset` are
carried over from **command 52**, which is still uncommitted; their mtimes are
`20:38:44`, not `21:05:21`, and they do not appear in the 4-minute `find`. This
is worth stating explicitly because a reader glancing at `git status` alone would
wrongly conclude this command touched the three meshes.

Commands 52 and 53 are both on disk and neither is committed.

---

## F) Warnings and errors

**No warning and no error was emitted by this command.**

This command's work runs from `12:04:04` (the `IsPIERunning` check) through
`12:05:22` (end of save validation):

```
[2026.09.03-12.04.04:500][655]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.EditorAppToolset.IsPIERunning'
[2026.09.03-12.04.35:500][748]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.material_instance.MaterialInstanceTools.create'
[2026.09.03-12.05.21:501][886]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.asset.AssetTools.save_assets'
```

Filtering the entire session log for `Warning`, `Error` and `Failed` while
excluding `LogSlate`, the most recent matching entry is at **`11:53:37`**, about
eleven minutes before this command began:

```
[2026.09.03-11.53.37:930][530]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
```

That is the recurring navmesh warning that accompanies PIE sessions starting and
stopping; identical lines appear at `10:31:28`, `10:45:26`, `11:14:35` and
`11:18:53`. It predates this command and was not caused by it. Its presence
indicates a PIE session ran at some point before this command — consistent with
`IsPIERunning` returning `false` by the time this command started.

Unlike command 52, **this command produced no `GetObjectProperties` or
`MaterialInstanceConstant` warnings**, because the known tool limitation was
already understood and no attempt was made to read parameter values off the base
material `M_FlatCol`.

`LogSlate` "Could not find Glyph Index" warnings continue to appear whenever
Korean text is rendered in the terminal. They are a font issue in the terminal,
unrelated to the project, and none falls inside this command's window.

---

## Not verified

- **Nothing was looked at. No viewport capture, no PIE, no render.** Every value
  in this report is a property read or a file listing. **Whether the doors now
  read as wood — or read as doors at all rather than holes, which was the stated
  problem — is completely unverified.**
- **The colour was not evaluated as a colour.** `0.055, 0.032, 0.018` is a very
  dark warm brown in linear space. Note these are *linear* values: they will
  appear noticeably lighter on screen than the decimals suggest, but this is still
  a dark material, and the lobby is lit only by 18 torches at Intensity 5000.
  **Whether the doors are now distinguishable from the surrounding stone
  (`0.135, 0.125, 0.112`) or simply darker than it is exactly the thing that needs
  eyes on it.** The wood is darker than the stone in every channel.
- **`Roughness 0.75` versus the stone's `1.0` was not evaluated.** The doors will
  be slightly shinier than the walls, which is plausible for timber against
  stone, but nothing here confirms how that reads under torchlight.
- **`M_FlatCol` is a flat-colour material with no grid or texture**, so the doors
  will be a uniform slab of colour with no surface detail — flat brown rather than
  flat grey. The instruction's complaint was that the doors read as a hole; a
  uniform dark brown slab may still read as a hole. Not measured.
- **Scope of the assignment was not enumerated.** SM_Door is used by all four
  door actors; whether anything else in the project uses it was not checked with
  `get_referencers`.
- **No shader recompile was triggered or observed.** Only a scalar and a vector
  parameter were set, which do not require one.
- **The `MI_Castle_Stone` static-switch issue from command 52 is still open.**
  `TopSurfaceColor` remains `false`, so floors and the ceiling underside still
  render with the side-face colours. That is unrelated to this command but
  unresolved.
