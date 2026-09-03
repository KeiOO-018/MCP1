# 2026-09-03 · Command 49 — 13 point lights in the lobby

Level change only, in `/Game/ThirdPerson/Lvl_Stage`.
**13 PointLight actors created, all 13 configured, all 13 in the "Lighting"
folder, all 13 saved to disk. No existing actor was modified — proven by the save
writing 13 new packages and zero modified ones. No Blueprint edited, no mesh
added, no existing light or atmosphere actor touched.**

Instruction, verbatim from the user:

> In the currently open level /Game/ThirdPerson/Lvl_Stage, add point lights to the lobby.
> It is completely dark since command 48 capped it, so nothing can be judged until there
> is light in it.
>
> Create 13 PointLight actors. Put every one of them in the outliner folder "Lighting",
> which already exists in this level.
>
> Settings shared by ALL 13 lights:
>   Mobility        = Movable
>   LightColor      = R 255, G 170, B 90   (warm torch colour)
>   IntensityUnits  = Unitless
>   SourceRadius    = 10
>   CastShadows     = true
>   Rotation        = (0, 0, 0)
>
> GROUP 1 - ground floor wall torches. Z 250, 50 units off the wall face.
> Intensity 5000, AttenuationRadius 1200 for all eight.
>
>   Torch_1F_S_1   (-1050, -1200, 250)
>   Torch_1F_S_2   (-1050,  -400, 250)
>   Torch_1F_S_3   (-1050,   400, 250)
>   Torch_1F_S_4   (-1050,  1200, 250)
>   Torch_1F_N_1   ( 1050, -1200, 250)
>   Torch_1F_N_2   ( 1050,  -400, 250)
>   Torch_1F_N_3   ( 1050,   400, 250)
>   Torch_1F_N_4   ( 1050,  1200, 250)
>
> GROUP 2 - second floor gallery torches. Z 850, which is 250 above the 2F walking
> surface at Z 600. Intensity 5000, AttenuationRadius 1200 for all four.
>
>   Torch_2F_W_1   (-700, -1350, 850)
>   Torch_2F_W_2   ( 300, -1350, 850)
>   Torch_2F_E_1   (-700,  1350, 850)
>   Torch_2F_E_2   ( 300,  1350, 850)
>
> GROUP 3 - the key light, in front of the final door on the second floor. This is the
> one dominant warm light the room reads from.
>
>   KeyLight_FinalDoor   (1000, 0, 900)
>   Intensity 20000, AttenuationRadius 2500
>
> DO NOT change the existing DirectionalLight, SkyLight, SkyAtmosphere, VolumetricCloud,
> ExponentialHeightFog or PostProcessVolume. Rooms 1, 2 and 3 still have no ceiling and
> are lit by those; touching them would darken the rooms too. DO NOT edit any Blueprint,
> move any wall, floor, door, ramp, railing or pillar, and do not add any mesh.
>
> STEP 2 - Save with AssetTools.save_assets and an empty list. Report which packages were
> written, verified on disk and not from the return value.
>
> VERIFY AND REPORT.
>
>   A) For all 13 lights report the actual world location, Mobility, Intensity,
>      IntensityUnits, AttenuationRadius, LightColor and CastShadows, read back after
>      creation. Say for each whether it matches what was asked. If any property could not
>      be set, say so plainly and give the error verbatim rather than reporting success.
>
>   B) Report the outliner folder each light ended up in.
>
>   C) Report the total actor count before and after. Exactly 13 are expected to be added.
>
>   D) Confirm by reading them back that the DirectionalLight, SkyLight and
>      PostProcessVolume are unchanged, and report their Intensity values.
>
>   E) Report any warning or error text verbatim in English. Do not summarize or translate.
>
> Write the report to Docs/Terminal-Log/2026-09-03-49-lobby-lights.md
> (a repo path - do NOT write under Saved/, it is gitignored).

**Headline: every one of the 13 lights matches every requested value exactly, on
all ten checks each (location, rotation, Mobility, Intensity, IntensityUnits,
SourceRadius, AttenuationRadius, LightColor, CastShadows, folder). The aggregate
`all_pass` flag is `true` and `missing` is empty. No property failed to set.
Actor count 102 → 115, exactly +13. The save wrote exactly 13 packages, all
new, none modified.**

---

## The one thing that needed interpretation: LightColor

The instruction says `LightColor = R 255, G 170, B 90`. **The MCP tool does not
accept 0–255 values for this property.** `ObjectTools.list_properties` on the
light component types it as a LinearColor with each channel clamped to 0..1:

```json
"lightColor":{"type":"object","title":"LinearColor",
  "properties":{"r":{"type":"number","minimum":0,"maximum":1},
                "g":{"type":"number","minimum":0,"maximum":1},
                "b":{"type":"number","minimum":0,"maximum":1},
                "a":{"type":"number","minimum":0,"maximum":1}},
  "required":["r","g","b","a"]}
```

Sending `255` would have been clamped to `1` and produced **white**, silently.

**So I converted, and this is my decision, not something the user wrote:** each
channel was sent as `value / 255`, i.e. `r = 1.0`, `g = 170/255 = 0.666666…`,
`b = 90/255 = 0.352941…`, `a = 1.0`.

This was verified to round-trip correctly rather than assumed. Read back, the
stored float32 values are:

```json
"lightColor":{"r":1,"g":0.6666666865348816,"b":0.3529411852359772,"a":1}
```

Multiplying back by 255: `1 × 255 = 255`, `0.6666666865348816 × 255 = 170.0000…`,
`0.3529411852359772 × 255 = 90.0000…`. Rounded, that is **exactly (255, 170, 90)**.
The verification script computed this conversion for every light and compared the
result to `[255, 170, 90]`; all 13 matched.

---

## Pre-flight

### P1 — Level, count, folders

`get_current_level` → `/Game/ThirdPerson/Lvl_Stage`. Actor count **102**.
`get_folders` → `["Lighting","Navigation"]`, so the "Lighting" folder the
instruction refers to does exist and did not need creating.

### P2 — No name collisions

`find_actors` for `"Torch"` and `"KeyLight"` returned nothing. All 13 labels were
free.

### P3 — Learning the property names before writing anything

One light was created first and `ObjectTools.list_properties` was run on its
`LightComponent0` to get the exact schema, rather than guessing property names.
This is what surfaced the LightColor problem above. The canonical names are
camelCase: `mobility`, `intensity`, `intensityUnits`, `sourceRadius`,
`attenuationRadius`, `lightColor`, `castShadows`.

The default state of a fresh PointLight, read before configuring it, was:

```json
{"mobility":"Stationary","intensity":8,"intensityUnits":"Candelas",
 "sourceRadius":0,"attenuationRadius":1000,
 "lightColor":{"r":1,"g":1,"b":1,"a":1},"castShadows":true}
```

Every single one of those defaults differs from what was asked except
`castShadows`, so this is a useful control: the values reported in section A
cannot be defaults that happened to match.

---

## The write

`SceneTools.add_to_scene_from_class` with `actor_type`
`/Script/Engine.PointLight`, `snap_to_ground: false`, and an explicit rotation of
`(0, 0, 0)` and scale `(1, 1, 1)`. Then `ActorTools.set_label`, then
`ObjectTools.set_properties` on the actor's `LightComponent0`, then
`SceneTools.set_actor_folder` to `"Lighting"`.

`snap_to_ground` was explicitly `false`. Left on, every light would have been
dropped onto the floor and the Z values would have been silently lost.

`set_properties` returned `true` for all 13. **Per `CLAUDE.md` that is not
evidence**, so everything in section A is a fresh read-back taken afterwards.

---

## A) All 13 lights, read back

Shared by all 13 and verified individually on each: `Mobility = Movable`,
`IntensityUnits = Unitless`, `SourceRadius = 10`, `CastShadows = true`,
`Rotation = (0, 0, 0)`, `LightColor = (255, 170, 90)`.

### Group 1 — ground floor wall torches

| Label | Location | Intensity | AttenRadius | Mobility | Units | SrcRadius | Color | CastShadows | Match |
|---|---|---|---|---|---|---|---|---|---|
| `Torch_1F_S_1` | `(-1050, -1200, 250)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |
| `Torch_1F_S_2` | `(-1050, -400, 250)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |
| `Torch_1F_S_3` | `(-1050, 400, 250)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |
| `Torch_1F_S_4` | `(-1050, 1200, 250)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |
| `Torch_1F_N_1` | `(1050, -1200, 250)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |
| `Torch_1F_N_2` | `(1050, -400, 250)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |
| `Torch_1F_N_3` | `(1050, 400, 250)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |
| `Torch_1F_N_4` | `(1050, 1200, 250)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |

### Group 2 — second floor gallery torches

| Label | Location | Intensity | AttenRadius | Mobility | Units | SrcRadius | Color | CastShadows | Match |
|---|---|---|---|---|---|---|---|---|---|
| `Torch_2F_W_1` | `(-700, -1350, 850)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |
| `Torch_2F_W_2` | `(300, -1350, 850)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |
| `Torch_2F_E_1` | `(-700, 1350, 850)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |
| `Torch_2F_E_2` | `(300, 1350, 850)` | `5000` | `1200` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |

### Group 3 — key light

| Label | Location | Intensity | AttenRadius | Mobility | Units | SrcRadius | Color | CastShadows | Match |
|---|---|---|---|---|---|---|---|---|---|
| `KeyLight_FinalDoor` | `(1000, 0, 900)` | `20000` | `2500` | Movable | Unitless | `10` | 255,170,90 | `true` | **all 10 ✓** |

### Aggregate

```json
{"all_pass": true, "missing": [], "total_actors": 115}
```

**No property failed to set. There is nothing to report under "if any property
could not be set".** Every location is exact-integer equal to the requested
triple; every intensity, attenuation radius and source radius is an exact
integer; every rotation is exactly `(0, 0, 0)`.

Internal names, for traceability:

| Label | Internal name |
|---|---|
| `Torch_1F_S_1` | `PointLight_UAID_9C6B005AF86942FE02_1955570339` |
| `Torch_1F_S_2` | `PointLight_UAID_9C6B005AF86942FE02_2016904340` |
| `Torch_1F_S_3` | `PointLight_UAID_9C6B005AF86942FE02_2017578341` |
| `Torch_1F_S_4` | `PointLight_UAID_9C6B005AF86942FE02_2018570342` |
| `Torch_1F_N_1` | `PointLight_UAID_9C6B005AF86942FE02_2019903343` |
| `Torch_1F_N_2` | `PointLight_UAID_9C6B005AF86942FE02_2020906344` |
| `Torch_1F_N_3` | `PointLight_UAID_9C6B005AF86942FE02_2022237345` |
| `Torch_1F_N_4` | `PointLight_UAID_9C6B005AF86942FE02_2023238346` |
| `Torch_2F_W_1` | `PointLight_UAID_9C6B005AF86942FE02_2024240347` |
| `Torch_2F_W_2` | `PointLight_UAID_9C6B005AF86942FE02_2025904348` |
| `Torch_2F_E_1` | `PointLight_UAID_9C6B005AF86942FE02_2027239349` |
| `Torch_2F_E_2` | `PointLight_UAID_9C6B005AF86942FE02_2028241350` |
| `KeyLight_FinalDoor` | `PointLight_UAID_9C6B005AF86942FE02_2029570351` |

### One setting I did not touch, which affects how Intensity behaves

`bUseInverseSquaredFalloff` is **`true`** on these lights — the engine default. It
was not in the instruction so it was left alone, but it changes what
"Intensity 5000, Unitless" means. The engine's own description of that property:

> Whether to use physically based inverse squared distance falloff, where AttenuationRadius is only clamping the light's contribution.
> Disabling inverse squared falloff can be useful when placing fill lights (don't want a super bright spot near the light).
> When enabled, the light's Intensity is in units of lumens, where 1700 lumens is a 100W lightbulb.
> When disabled, the light's Intensity is a brightness scale.

Read back from `Torch_1F_S_1`, alongside other defaults left untouched:

```json
{"bUseInverseSquaredFalloff":true,"lightFalloffExponent":8,"bAffectsWorld":true,
 "castDynamicShadows":true,"bVisible":true,"indirectLightingIntensity":1,
 "volumetricScatteringIntensity":1}
```

**Flagging it because it is the most likely reason the result looks wrong if it
does.** With inverse-squared falloff on, brightness drops off sharply with
distance and the lights may read as hot near the wall and dim in the middle of
the lobby. If that is what you see, the fix is either
`bUseInverseSquaredFalloff = false` (making Intensity a plain brightness scale,
with `lightFalloffExponent` 8 controlling the curve) or a different Intensity
value. Both are tuning values and neither was changed without being asked.

---

## B) Outliner folder

**All 13 are in `Lighting`.** This was not read from the `set_actor_folder`
return value; it was verified by calling `SceneTools.get_actors_in_folder` with
`folder_path: "Lighting"`, `recursive: true`, collecting the returned refPaths
into a set, and testing each light's refPath for membership. The `folder` check
is `true` for all 13.

| Label | Folder |
|---|---|
| `Torch_1F_S_1` … `Torch_1F_S_4` | `Lighting` |
| `Torch_1F_N_1` … `Torch_1F_N_4` | `Lighting` |
| `Torch_2F_W_1`, `Torch_2F_W_2` | `Lighting` |
| `Torch_2F_E_1`, `Torch_2F_E_2` | `Lighting` |
| `KeyLight_FinalDoor` | `Lighting` |

The `Lighting` folder now holds **20** actors: the 7 that were already there
(SkyLight, DirectionalLight, ExponentialHeightFog, SkyAtmosphere,
VolumetricCloud, PostProcessVolume and one other) plus these 13. `get_folders`
still returns `["Lighting","Navigation"]` — no new folder was created.

---

## C) Actor count

| | Count |
|---|---|
| Before | **102** |
| After | **115** |
| Delta | **+13** |

**Exactly 13 added, as expected.** Nothing was deleted. Corroborated by the save
writing exactly 13 packages (next section) and by the editor's own validation
reporting 13 associated objects.

---

## D) The existing lighting actors are unchanged

Read back after all 13 lights were created:

| Actor | Property | Value |
|---|---|---|
| **DirectionalLight** | **Intensity** | **`3`** |
| | LightColor | `(1, 1, 1, 1)` — white |
| | Mobility | `Movable` |
| | CastShadows | `true` |
| | bAffectsWorld | `true` |
| | Actor location | `(0, 0, 1190)` |
| | Actor rotation | `(pitch -60.77915199999994, yaw -14.98816099999997, roll 25.555013999999957)` |
| | Actor scale | `(2.5, 2.5, 2.5)` |
| **SkyLight** | **Intensity** | **`1`** |
| | LightColor | `(1, 1, 1, 1)` — white |
| | Mobility | `Movable` |
| | CastShadows | `true` |
| | bAffectsWorld | `true` |
| **PostProcessVolume** | bEnabled | `true` |
| | **BlendWeight** | **`1`** |
| | bUnbound | `true` |
| | Priority | `0` |
| **ExponentialHeightFog** | FogDensity | `0.043600000441074371` |
| | FogHeightFalloff | `0.20000000298023224` |

**PostProcessVolume has no "Intensity" property** — it is a volume, not a light.
The closest equivalent is `BlendWeight`, which is `1`, and it is enabled and
unbounded. That is reported above in place of an intensity.

### How "unchanged" is established, stated precisely

**I did not capture a pre-change baseline of these values before creating the
lights, so I cannot show a before/after diff.** Saying otherwise would be
inventing evidence. What actually establishes it is stronger than a value
comparison would have been:

1. **No write tool was ever called against any of them.** The only writes this
   command issued were `add_to_scene_from_class`, `set_label`, `set_properties`
   and `set_actor_folder`, each targeting one of the 13 new PointLights or their
   own `LightComponent0`. Their refPaths are listed in section A and none is a
   DirectionalLight, SkyLight, SkyAtmosphere, VolumetricCloud,
   ExponentialHeightFog or PostProcessVolume path.
2. **The save wrote 13 new packages and modified zero existing ones.** In this
   World Partition level every actor has its own package. Had any of these six
   actors been altered in any way, its package would have been dirty and written
   by the same save, and would appear as ` M` in `git status`. **There is not a
   single ` M` entry.** This is a complete, not a sampled, check — it covers every
   actor in the level, including every wall, floor, door, ramp, railing, pillar
   and mesh the instruction said not to touch.

---

## STEP 2 — Save, verified on disk

`AssetTools.save_assets` with `[]`:

```json
{"returnValue":true}
```

Per command 47's finding, the empty-list form is the one that actually writes a
World Partition level's actors. The result below is checked on disk.

### Packages written — exactly 13, all new

All written at `2026-09-03 19:52:41`:

| Package | Actor |
|---|---|
| `__ExternalActors__/ThirdPerson/Lvl_Stage/8/PX/1I144KLCEXOGEMRJIJVP08.uasset` | one of the 13 lights |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/0/YX/8NB34T0MH9HTLAY3XPEY0V.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/B/QU/BUXIC4W4YV0HCXXHGU28HJ.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/D/LB/81LCXWHJHFO0B6OZX92FL5.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/D/Z3/S2SOVEWWMV4H62NJQPRIWS.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/E/WH/YRFJIUQW0OAUPJQ1SP5KE4.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/A/PQ/O3HHOUW1GHRVTZ08BA0484.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/7/QA/20YTIA1J4VHGBGJ4F5EUBY.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/5/Z1/LZ4IP07CLG11GM4RN1YF6L.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/4/PQ/8HVI0Q1QL5MT82UHP43TP4.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/1/MS/K6HGPN9IDPNJG8QPVQPFI1.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/4/XP/4RHYBR78DKZYQMEUXEHW9B.uasset` | " |
| `__ExternalActors__/ThirdPerson/Lvl_Stage/0/80/S2JMCSPDP0J3S2PIKKXV5E.uasset` | " |

The package filenames are content-hash style IDs and the tools do not expose a
label→package mapping, so I cannot say which file is which light without
guessing. **I am not going to guess.** What is certain is that there are exactly
13 of them, they are all new, and they appeared in the same save as the 13 new
lights.

Verified four ways, none of them the tool's return value:

1. **A `find` for every file under `Content` modified in the last 6 minutes
   returned those 13 paths and nothing else.**
2. External actor file count went **138 → 151**, exactly `+13`.
3. `git status --porcelain` shows **13 new untracked directories and zero
   modified files**:
   ```
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/0/80/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/0/YX/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/1/MS/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/4/PQ/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/4/XP/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/5/Z1/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/7/QA/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/8/PX/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/A/PQ/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/QU/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/UI/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/D/LB/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/D/Z3/
   ?? Content/__ExternalActors__/ThirdPerson/Lvl_Stage/E/WH/
   ?? Docs/Terminal-Log/2026-09-03-48-lobby-ceiling.md
   ```
   That is 14 untracked package directories, because `B/UI/` is command 48's
   ceiling slab, which is still uncommitted from the previous command. The 13
   new ones are the lights.
4. The editor log shows exactly 13 `Saving Package` lines at `10.52.41`, and the
   content validator reports the matching count:
   ```
   [2026.09.03-10.52.41:956][357]LogContentValidation: Display: Starting to validate 1 assets (13 associated objects such as actors)
   ```

**`Lvl_Stage.umap` was not written** — still mtime
`2026-09-03 09:47:04.791203000 +0900`, still 12,824 bytes, absent from
`git status`. Correct for a World Partition level.

---

## E) Warnings and errors, verbatim

This command's work runs from `10:50:25` (the first `add_to_scene_from_class`
dispatch) to `10:52:42` (end of save validation). Four warnings fall in that
window, all caused by my own read calls. **No error was emitted, and nothing was
emitted by the 13 creations, the property writes or the save.**

**One from a read that failed** — `DirectionalLightComponent` has no
`intensityUnits` property, which aborted that read call and forced a retry
without it. Verbatim, both as the tool returned it and as it appears in the log:

```
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.DirectionalLight_UAID_F4A475FF15A3736A02_1961932697.LightComponent0' (DirectionalLightComponent): the following properties could not be read: intensityUnits
```

```
[2026.09.03-10.52.22:712][812]LogScript: Warning: GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.DirectionalLight_UAID_F4A475FF15A3736A02_1961932697.LightComponent0' (DirectionalLightComponent): the following properties could not be read: intensityUnits
```

This is a read-only failure — it read nothing and wrote nothing. `IntensityUnits`
exists on point and spot lights but not on directional lights, which is why the
DirectionalLight row in section D has no units column.

**Three from `list_properties`** on the point light component, the call used to
learn the schema. All are the JSON schema generator declining to express delegate
properties:

```
[2026.09.03-10.50.34:516][976]LogJson: Warning: Property "OnComponentDeactivated" type FActorComponentDeactivateSignature unhandled during Json schema generation.
[2026.09.03-10.50.34:516][976]LogJson: Warning: Property "OnComponentActivated" type FActorComponentActivatedSignature unhandled during Json schema generation.
[2026.09.03-10.50.34:516][976]LogJson: Warning: Property "PhysicsVolumeChangedDelegate" type FPhysicsVolumeChanged unhandled during Json schema generation.
```

### Warnings that predate this command

Included for completeness and explicitly **not** caused by this command. The most
recent pre-existing entry is at `10:45:26`, about five minutes before this
command began:

```
[2026.09.03-10.31.28:203][324]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
[2026.09.03-10.45.26:720][932]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
```

And a block of Slate font warnings from `10:22:28`, which are the terminal font
lacking Hangul glyphs and have nothing to do with the level:

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

---

## Not verified

- **No lighting was observed. This report contains zero evidence about how the
  lobby actually looks.** Every value here is a property read. Whether 5000
  Unitless with inverse-squared falloff is too bright, too dim, or right is
  unknown, and it is the whole point of the exercise. **This needs eyes on it —
  either a screenshot from you or a PIE run.**
- **PIE was not run.**
- **No light was checked for being embedded inside geometry.** The Group 1
  torches sit at X ±1050, and the lobby's 1F walls occupy X -1300..-1100 and
  X 1100..1300, so ±1050 is 50 units clear of the inner faces as the instruction
  intended — but that is arithmetic from command 45's recorded bounds, not a
  trace. No trace or overlap query was run to confirm any light is in open air.
  The same applies to the Group 2 torches at Y ±1350 and to
  `KeyLight_FinalDoor` at `(1000, 0, 900)`, which sits close to the 2F north wall
  line at X 1100.
- **`bUseInverseSquaredFalloff` was left at its default `true`** and is discussed
  in section A. Not a failure, but not what a torch look usually wants.
- **Shadow cost was not considered.** 13 Movable point lights with
  `CastShadows = true` and radii of 1200–2500 in one enclosed room is a real
  runtime cost, and several of these attenuation spheres overlap heavily. No
  profiling was done.
- **The lights are inside the sealed lobby, but nothing confirms they do not
  spill into rooms 1, 2 and 3** through the four doorways. With radius 1200 from
  X ±1050, the attenuation spheres certainly reach the doorway openings. Whether
  that visibly brightens the corridors was not measured.
- **Nothing was rebuilt.** These are Movable lights so no lighting build is
  required, but no build was run and no navmesh was rebuilt.
