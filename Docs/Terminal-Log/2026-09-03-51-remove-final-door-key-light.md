# 2026-09-03 · Command 51 — Delete KeyLight_FinalDoor

Level change only, in `/Game/ThirdPerson/Lvl_Stage`.
**One actor deleted. Nothing else touched. Saved to disk, verified by a
before/after diff of the external actor package list: exactly one package
removed, zero added, zero modified.**

Instruction, verbatim from the user:

> In the currently open level /Game/ThirdPerson/Lvl_Stage, delete the PointLight actor
> labeled "KeyLight_FinalDoor". It sits at (1000, 0, 900) with Intensity 20000 and
> AttenuationRadius 2500, and it is the only light in the level that does not use the
> shared torch settings.
>
> Reason: command 50 added Torch_2F_N_1 and Torch_2F_N_2 flanking that same doorway, so
> the area is now lit three times over and is blown out. Removing this one leaves all four
> doorways with the same treatment - exactly two flanking torches - and leaves every light
> in the level at Intensity 5000 / AttenuationRadius 1200.
>
> Delete ONLY that actor. Do not touch the 18 torches, the DirectionalLight, the SkyLight,
> the SkyAtmosphere, the VolumetricCloud, the ExponentialHeightFog or the
> PostProcessVolume. Do not edit any Blueprint, mesh, wall, floor, door, ramp, railing or
> pillar.
>
> STEP 2 - Save with AssetTools.save_assets and an empty list. Verify on disk that the
> actor's external package was removed, and do not report success from the return value
> alone.
>
> VERIFY AND REPORT.
>
>   A) Confirm no actor labeled "KeyLight_FinalDoor" remains in the level.
>   B) List all remaining PointLight actors with their label, world location, Intensity and
>      AttenuationRadius. Exactly 18 are expected, all at Intensity 5000 and
>      AttenuationRadius 1200.
>   C) Report the total actor count before and after. Exactly one actor should be removed.
>   D) Report which packages were written or deleted on disk.
>   E) Report any warning or error text verbatim in English. Do not summarize or translate.
>
> Write the report to Docs/Terminal-Log/2026-09-03-51-remove-final-door-key-light.md
> (a repo path - do NOT write under Saved/, it is gitignored).

Follow-up message from the user, after this command was halted on the first
attempt:

> PIE is stopped now. IsPIERunning returns false, the actor count is back to 121, and no
> refPath contains UEDPIE. Go ahead with the deletion of KeyLight_FinalDoor as originally
> instructed, re-checking IsPIERunning yourself first.

**Headline: deleted. 121 → 120 actors, 19 → 18 PointLights, no actor labeled
`KeyLight_FinalDoor` remains, and all 18 survivors are at Intensity 5000 /
AttenuationRadius 1200 with identical shared settings. Exactly one external
actor package disappeared from disk and nothing else changed. No warning or
error was emitted by this command.**

---

## The first attempt was halted: PIE was running

This command was issued once, stopped without making any change, and then
re-issued. That is worth recording because the failure mode is silent and would
have produced a false success report.

On the first attempt, the actor came back as:

```
/Game/ThirdPerson/UEDPIE_0_Lvl_Stage.Lvl_Stage:PersistentLevel.PointLight_UAID_9C6B005AF86942FE02_2029570351
```

The `UEDPIE_0_` prefix means a Play-In-Editor session was running and every scene
tool was resolving against the **PIE world**, which is a duplicate of the editor
world. The engine log shows the duplication explicitly:

```
[2026.09.03-11.16.30:850][342]LogPlayLevel: PIE: Created PIE world by copying editor world from /Game/ThirdPerson/Lvl_Stage.Lvl_Stage to /Game/ThirdPerson/UEDPIE_0_Lvl_Stage.Lvl_Stage (0.011916s)
```

`EditorToolset.EditorAppToolset.IsPIERunning` confirmed it:

```json
{"returnValue":true}
```

The actor count also disagreed — **138** in the PIE world versus the level's
actual 121, the difference being gameplay actors spawned at BeginPlay.

**Had the deletion gone ahead, it would have removed the PIE copy.** That copy is
discarded when PIE stops, the real editor actor would have survived untouched,
and `save_assets` would have had nothing to write — while every tool return value
said success. There is no world-selection parameter on `find_actors` or
`remove_from_scene`, so the editor world was simply unreachable.

Nothing was written on that attempt. The only actions were reads, plus one
snapshot of the on-disk package list to the scratchpad, which is what made
section D's exact diff possible. The user was asked how to proceed and chose to
stop PIE themselves.

### Re-check before proceeding

As instructed, `IsPIERunning` was called again first:

```json
{"returnValue":false}
```

The log confirms PIE had been torn down at `11:18:53`, between the two checks:

```
[2026.09.03-11.17.40:049][544]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.EditorAppToolset.IsPIERunning'
[2026.09.03-11.18.53:347][  2]LogWorld: BeginTearingDown for /Game/ThirdPerson/UEDPIE_0_Lvl_Stage
[2026.09.03-11.18.53:350][  2]LogWorldPartition: UWorldPartition::Uninitialize : World = /Game/ThirdPerson/UEDPIE_0_Lvl_Stage.Lvl_Stage
[2026.09.03-11.22.12:195][687]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.EditorAppToolset.IsPIERunning'
```

---

## Pre-flight, in the editor world

| Check | Result |
|---|---|
| `IsPIERunning` | `false` |
| `get_current_level` | `/Game/ThirdPerson/Lvl_Stage` |
| Total actors | **121** |
| refPaths containing `UEDPIE` | **`[]`** — none |
| PointLight actors | 19 |
| Actors labeled `KeyLight_FinalDoor` | **exactly 1** |
| `can_edit` on that actor | `true` |

The target resolved to exactly one actor, and its identity and values matched the
record captured on the first attempt:

```json
{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.PointLight_UAID_9C6B005AF86942FE02_2029570351",
 "loc":[1000,0,900], "intensity":20000, "atten":2500}
```

The instruction's three identifying facts all check out: location `(1000, 0, 900)`,
Intensity `20000`, AttenuationRadius `2500`. It was also the only one of the 19
lights not at 5000/1200, exactly as the instruction said.

### The deleted actor's full configuration, for the record

A deletion is not trivially reversible, so the complete settings are preserved
here so the light can be rebuilt by hand if this turns out to be wrong:

```
KeyLight_FinalDoor   class /Script/Engine.PointLight
  internal name  PointLight_UAID_9C6B005AF86942FE02_2029570351
  Location (1000, 0, 900)   Rotation (0, 0, 0)   Scale (1, 1, 1)
  Mobility                   Movable
  Intensity                  20000
  IntensityUnits             Unitless
  AttenuationRadius          2500
  SourceRadius               10
  CastShadows                true
  LightColor                 (255, 170, 90)
                             = (1, 0.6666666865348816, 0.3529411852359772, 1)
  bUseInverseSquaredFalloff  true
  lightFalloffExponent       8
  bAffectsWorld              true
  bVisible                   true
  castDynamicShadows         true
  castStaticShadows          true
  indirectLightingIntensity  1
  volumetricScatteringIntensity 1
  temperature                6500   (bUseTemperature false)
  specularScale              1
  Tags                       none
  Outliner folder            Lighting
  Components                 LightComponent0
```

---

## The write

`SceneTools.remove_from_scene`, one call, targeting the refPath above:

```json
{"returnValue":true}
```

That was the only write this command made. No other tool that modifies state was
called against anything.

```
[2026.09.03-11.22.53:082][333]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.scene.SceneTools.remove_from_scene'
```

Per `CLAUDE.md` the `true` is not evidence. Everything below is a fresh read-back
and an on-disk diff.

---

## A) No `KeyLight_FinalDoor` remains

A fresh search was run across three name patterns — `Torch_`, `KeyLight_` and the
broader `Light` — with results filtered to `/Script/Engine.PointLight`:

```json
{"keylight_remaining": [], "pointlight_count": 18, "missing_expected": []}
```

**`keylight_remaining` is empty.** No actor with that label exists in the level.
`missing_expected` is also empty, confirming all 18 torches that *should* still
be there were found.

---

## B) The 18 remaining PointLights

```json
{"all_uniform_5000_1200": true}
```

That aggregate flag is `true` only if **every** one of the 18 has Intensity 5000,
AttenuationRadius 1200, the expected location, `Movable`, `Unitless`,
SourceRadius 10, CastShadows `true`, colour `(255, 170, 90)` and folder
`Lighting`. It passed.

### Ground floor wall torches — Z 250

| Label | Location | Intensity | AttenRadius |
|---|---|---|---|
| `Torch_1F_S_1` | `(-1050, -1200, 250)` | `5000` | `1200` |
| `Torch_1F_S_2` | `(-1050, -400, 250)` | `5000` | `1200` |
| `Torch_1F_S_3` | `(-1050, 400, 250)` | `5000` | `1200` |
| `Torch_1F_S_4` | `(-1050, 1200, 250)` | `5000` | `1200` |
| `Torch_1F_N_1` | `(1050, -1200, 250)` | `5000` | `1200` |
| `Torch_1F_N_2` | `(1050, -400, 250)` | `5000` | `1200` |
| `Torch_1F_N_3` | `(1050, 400, 250)` | `5000` | `1200` |
| `Torch_1F_N_4` | `(1050, 1200, 250)` | `5000` | `1200` |

### Ground floor doorway flanking torches — Z 250

| Label | Location | Intensity | AttenRadius |
|---|---|---|---|
| `Torch_1F_W_1` | `(-700, -1350, 250)` | `5000` | `1200` |
| `Torch_1F_W_2` | `(100, -1350, 250)` | `5000` | `1200` |
| `Torch_1F_E_1` | `(-700, 1350, 250)` | `5000` | `1200` |
| `Torch_1F_E_2` | `(100, 1350, 250)` | `5000` | `1200` |

### Second floor gallery torches — Z 850

| Label | Location | Intensity | AttenRadius |
|---|---|---|---|
| `Torch_2F_W_1` | `(-700, -1350, 850)` | `5000` | `1200` |
| `Torch_2F_W_2` | `(300, -1350, 850)` | `5000` | `1200` |
| `Torch_2F_E_1` | `(-700, 1350, 850)` | `5000` | `1200` |
| `Torch_2F_E_2` | `(300, 1350, 850)` | `5000` | `1200` |

### Second floor final-door flanking torches — Z 850

| Label | Location | Intensity | AttenRadius |
|---|---|---|---|
| `Torch_2F_N_1` | `(1050, -400, 850)` | `5000` | `1200` |
| `Torch_2F_N_2` | `(1050, 400, 850)` | `5000` | `1200` |

**Exactly 18, all at Intensity 5000 and AttenuationRadius 1200, as expected.**
Every location is unchanged from command 50's verified values, and every refPath
is unchanged, so none of the 18 was moved, replaced or re-created. The lobby now
has a single uniform light treatment: four doorways, two flanking torches each,
plus eight wall torches and four gallery torches, all identical.

The `Lighting` outliner folder went from 26 actors to **25**, consistent with one
light removed and nothing else disturbed.

---

## C) Actor count

| | Count |
|---|---|
| Before | **121** |
| After | **120** |
| Delta | **−1** |

**Exactly one actor removed.** Nothing was created. Corroborated by the package
diff in section D, which shows one removal and zero additions.

---

## D) Packages written or deleted on disk

`AssetTools.save_assets` with `[]` returned `{"returnValue":true}`. That is not
what this section rests on.

Because a full listing of `Content/__ExternalActors__` was captured **before** the
deletion, the on-disk effect could be diffed exactly rather than inferred.

| | Count |
|---|---|
| Packages before | **157** |
| Packages after | **156** |

**Deleted — exactly one:**

```
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/0/80/S2JMCSPDP0J3S2PIKKXV5E.uasset
```

**Written or added: none.** `comm -13` on the two sorted listings returned
nothing.

**Modified: none.** `git status --porcelain` filtered for ` M` returns nothing,
and a `find` for any file under `Content` modified in the last 5 minutes returned
**nothing at all** — no package was rewritten, only the one removed.

### Cross-check: that package really was the key light

`0/80/S2JMCSPDP0J3S2PIKKXV5E.uasset` appears in the list of 13 packages written
by command 49, which is the command that created `KeyLight_FinalDoor` along with
the first 12 torches. It is one of that set and is now the only one of them gone.
This independently confirms the right package was removed — command 49 could not
have known which of its 13 files was the key light, and this deletion identifies
it retroactively.

### One leftover worth naming

The directory `Content/__ExternalActors__/ThirdPerson/Lvl_Stage/0/80/` **still
exists and is now empty**:

```
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/0/80
total 4
drwxr-xr-x 1 a0108 197609 0 Sep  3 20:23 .
drwxr-xr-x 1 a0108 197609 0 Sep  3 19:52 ..
```

The `.uasset` inside it is gone; the empty folder is not cleaned up by the editor.
Git does not track empty directories, so `0/80/` has simply dropped out of
`git status` and this leaves no trace in the repository. It is harmless. It was
not deleted because removing directories was not part of the instruction.

**`Lvl_Stage.umap` was not written** — unchanged at 12,824 bytes, mtime
`2026-09-03 09:47:04`. Correct for a World Partition level.

### Still uncommitted

`git status` now shows **19 untracked package directories** (down from 20 — the
`0/80/` entry disappeared with its file) plus three untracked report files from
commands 48, 49 and 50. Commands 48 through 51 are all on disk; none is committed.

---

## E) Warnings and errors

**No warning and no error was emitted by this command.**

This command's work runs from `11:22:12` (the `IsPIERunning` re-check) through
the save at `11:23:33`:

```
[2026.09.03-11.22.12:195][687]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.EditorAppToolset.IsPIERunning'
[2026.09.03-11.22.53:082][333]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.scene.SceneTools.remove_from_scene'
[2026.09.03-11.23.33:306][856]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.asset.AssetTools.save_assets'
```

Filtering the whole session log for `Warning`, `Error` and `Failed` while
excluding `LogSlate`, the most recent matching entry is at **`11:18:53`** — the
PIE teardown, before this command's work began:

```
[2026.09.03-11.18.53:347][  2]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
```

That is a recurring pre-existing warning; identical lines appear at `10:31:28`,
`10:45:26` and `11:14:35`, all tied to PIE sessions starting and stopping, none
caused by this command.

The only log entries at all inside this command's window that match a warning
filter are `LogSlate` font warnings from `11:19:09`, which are the terminal font
lacking Hangul glyphs while rendering the user's message and have nothing to do
with the level. A representative sample, verbatim:

```
[2026.09.03-11.19.09:215][802]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c5b4, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-11.19.09:215][802]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c5b4, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-11.19.09:215][802]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c774, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-11.19.09:215][802]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c774, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-11.19.09:215][802]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c9c0, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-11.19.09:215][802]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c9c0, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-11.19.09:215][802]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c6cc, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-11.19.09:215][802]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c6cc, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-11.19.09:215][802]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c918, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.09.03-11.19.09:215][802]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c918, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
```

**Notably, the delete itself logged nothing** — no `LogEditor` deletion line, no
content validation pass. The save had no dirty package to write, only a package
to remove, and the validator did not run. This is the same class of silence
recorded in command 46: the tools do not narrate what they do, so the on-disk
diff in section D is the only real evidence that the deletion took effect.

---

## Not verified

- **No lighting was observed. This report contains no evidence about how the
  lobby looks now.** Every value is a property read and a file listing. Whether
  removing the key light actually fixes the blown-out area at the final door is
  exactly the question this command was meant to address, and it is still
  unanswered here. This has been open since command 49.
- **PIE was not run afterward.** It was running before this command and was
  stopped by the user; it was not restarted to check the result.
- **The final doorway is now lit only by `Torch_2F_N_1` and `Torch_2F_N_2`** at
  Intensity 5000 / radius 1200, down from those two plus a 20000 / 2500 key
  light. Whether that area is now correctly lit, or has swung from too bright to
  too dim, was not measured. The instruction's stated intent was uniformity, and
  uniformity is what was verified — not that the result looks good.
- **Nothing was rebuilt.** No lighting build (not needed for Movable lights) and
  no navmesh rebuild.
- **The empty `0/80/` directory was left in place**, as described in section D.
- **Only the 18 PointLights were re-read.** The DirectionalLight, SkyLight,
  SkyAtmosphere, VolumetricCloud, ExponentialHeightFog and PostProcessVolume were
  not individually read back this time. They are covered by the stronger
  package-level check — zero packages modified means none of them changed — but
  no direct property comparison was made for them in this command.
