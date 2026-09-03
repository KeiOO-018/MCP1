# 2026-09-03 · Command 55 — Replace the 18 PointLights with 18 BP_Torch actors

Level change only, in `/Game/ThirdPerson/Lvl_Stage`. No asset was edited.
**18 BP_Torch actors created and verified, then the 18 PointLight actors deleted.
Actor count 120 → 138 → 120. Zero PointLight-class actors remain. 18 packages
written and 18 removed on disk, a clean one-for-one swap.**

**The engine emitted a new rendering warning during this command — a virtual
shadow map light overflow. It is the first of its kind in the session and it is a
direct consequence of 18 shadow-casting torches. Section F.**

Instruction, verbatim from the user:

> In the currently open level /Game/ThirdPerson/Lvl_Stage, replace the 18 bare PointLight
> actors with 18 BP_Torch actors, so each torch is one actor carrying both its mesh and
> its light.
>
> Order matters: create all 18 first, verify them, and only then delete the 18 PointLight
> actors. Do not delete anything before the 18 new actors are confirmed present. The 18
> labels are reused, so during the middle of this command two actors will briefly share
> each label - that is expected and harmless, because the delete step targets actors whose
> class is PointLight, never BP_Torch.
>
> BP_Torch is built pointing along its local +X with the wall behind it at local X = -50,
> and its origin is where the light sits. So each actor goes at the exact coordinates the
> PointLight it replaces occupies, and only the yaw differs, chosen so local +X points
> into the room.
>
> STEP 1 - Create 18 actors from /Game/Interaction/BP_Torch. Rotation is (pitch 0, yaw as
> listed, roll 0) and scale (1, 1, 1) for every one. Put all 18 in the outliner folder
> "Lighting".
>
>   Label            Location              Yaw    Wall it hangs on
>   Torch_1F_S_1     (-1050, -1200, 250)     0    south, X -1100
>   Torch_1F_S_2     (-1050,  -400, 250)     0    south
>   Torch_1F_S_3     (-1050,   400, 250)     0    south
>   Torch_1F_S_4     (-1050,  1200, 250)     0    south
>   Torch_1F_N_1     ( 1050, -1200, 250)   180    north, X 1100
>   Torch_1F_N_2     ( 1050,  -400, 250)   180    north
>   Torch_1F_N_3     ( 1050,   400, 250)   180    north
>   Torch_1F_N_4     ( 1050,  1200, 250)   180    north
>   Torch_1F_W_1     ( -700, -1350, 250)    90    west,  Y -1400
>   Torch_1F_W_2     (  100, -1350, 250)    90    west
>   Torch_1F_E_1     ( -700,  1350, 250)   -90    east,  Y 1400
>   Torch_1F_E_2     (  100,  1350, 250)   -90    east
>   Torch_2F_W_1     ( -700, -1350, 850)    90    west
>   Torch_2F_W_2     (  300, -1350, 850)    90    west
>   Torch_2F_E_1     ( -700,  1350, 850)   -90    east
>   Torch_2F_E_2     (  300,  1350, 850)   -90    east
>   Torch_2F_N_1     ( 1050,  -400, 850)   180    north
>   Torch_2F_N_2     ( 1050,   400, 850)   180    north
>
> STEP 2 - Verify all 18 BP_Torch actors exist at the right transforms. If any is missing
> or wrong, STOP HERE, delete nothing, and report what happened.
>
> STEP 3 - Only after STEP 2 passes, delete the 18 actors whose class is PointLight. There
> are exactly 18 of them and they carry the same 18 labels. Delete ONLY actors of class
> PointLight. Do NOT delete the DirectionalLight, the SkyLight, or anything else.
>
> STEP 4 - Save with AssetTools.save_assets and an empty list. Verify on disk which
> packages were written and which were removed.
>
> DO NOT touch the DirectionalLight, SkyLight, SkyAtmosphere, VolumetricCloud,
> ExponentialHeightFog or PostProcessVolume. DO NOT edit any Blueprint, material or mesh
> asset. DO NOT move any wall, floor, door, ramp, railing, pillar or the ceiling.
>
> VERIFY AND REPORT.
>
>   A) Report EditorToolset.EditorAppToolset.IsPIERunning first. If true, stop before
>      making any change and say so.
>
>   B) For each of the 18 BP_Torch actors report label, world location, rotation, scale,
>      outliner folder, and the actor's world bounding box.
>
>   C) Confirm zero actors of class PointLight remain in the level.
>
>   D) Report the total actor count before and after. It should start at 120, rise to 138,
>      and end at 120.
>
>   E) Report which packages were written and which were removed on disk.
>
>   F) Report any warning or error text verbatim in English. Do not summarize or translate.
>
> Write the report to Docs/Terminal-Log/2026-09-03-55-place-torches.md
> (a repo path - do NOT write under Saved/, it is gitignored).

---

## A) PIE state — checked first

`EditorToolset.EditorAppToolset.IsPIERunning`:

```json
{"returnValue":false}
```

**PIE is not running.** Checked before any change.

---

## STEP 1 — 18 actors created

`SceneTools.add_to_scene_from_asset` with `asset_path` `/Game/Interaction/BP_Torch`,
`snap_to_ground: false`, then `set_label`, then `set_actor_folder` to `"Lighting"`.

`snap_to_ground` was explicitly false. Left on, all 18 would have been dropped to
the floor and every Z lost.

`created_count`: **18**. Total actors after creation: **138**.

---

## STEP 2 — the gate

This is the step that had to pass before anything was deleted, and it did.

**Verification was done by refPath, not by label.** At this moment each of the 18
labels existed twice — once on a BP_Torch and once on a PointLight — so a
label-based lookup would have been ambiguous. Every check below targets the exact
refPath returned by the creation call.

Each actor was checked on eight things: label, class, location, pitch, roll, yaw,
scale, and folder membership.

```json
{"all_ok": true, "count": 18, "failed": []}
```

**All 18 passed. Nothing was deleted until this returned true.**

Class on all 18 read `/Game/Interaction/BP_Torch.BP_Torch_C` — confirming they are
BP_Torch instances and not something else.

---

## B) The 18 BP_Torch actors

All 18: scale `(1, 1, 1)`, pitch `0`, roll `0`, folder **`Lighting`**.

| Label | World location | Yaw | World bounds min | World bounds max |
|---|---|---|---|---|
| `Torch_1F_S_1` | `(-1050, -1200, 250)` | `0` | `(-1178, -1328, 122)` | `(-922, -1072, 378)` |
| `Torch_1F_S_2` | `(-1050, -400, 250)` | `0` | `(-1178, -528, 122)` | `(-922, -272, 378)` |
| `Torch_1F_S_3` | `(-1050, 400, 250)` | `0` | `(-1178, 272, 122)` | `(-922, 528, 378)` |
| `Torch_1F_S_4` | `(-1050, 1200, 250)` | `0` | `(-1178, 1072, 122)` | `(-922, 1328, 378)` |
| `Torch_1F_N_1` | `(1050, -1200, 250)` | `180` | `(922, -1328, 122)` | `(1178, -1072, 378)` |
| `Torch_1F_N_2` | `(1050, -400, 250)` | `180` | `(922, -528, 122)` | `(1178, -272, 378)` |
| `Torch_1F_N_3` | `(1050, 400, 250)` | `180` | `(922, 272, 122)` | `(1178, 528, 378)` |
| `Torch_1F_N_4` | `(1050, 1200, 250)` | `180` | `(922, 1072, 122)` | `(1178, 1328, 378)` |
| `Torch_1F_W_1` | `(-700, -1350, 250)` | `89.99999999999999` | `(-828, -1478, 122)` | `(-572, -1222, 378)` |
| `Torch_1F_W_2` | `(100, -1350, 250)` | `89.99999999999999` | `(-28, -1478, 122)` | `(228, -1222, 378)` |
| `Torch_1F_E_1` | `(-700, 1350, 250)` | `-90.00000000000001` | `(-828, 1222, 122)` | `(-572, 1478, 378)` |
| `Torch_1F_E_2` | `(100, 1350, 250)` | `-90.00000000000001` | `(-28, 1222, 122)` | `(228, 1478, 378)` |
| `Torch_2F_W_1` | `(-700, -1350, 850)` | `89.99999999999999` | `(-828, -1478, 722)` | `(-572, -1222, 978)` |
| `Torch_2F_W_2` | `(300, -1350, 850)` | `89.99999999999999` | `(172, -1478, 722)` | `(428, -1222, 978)` |
| `Torch_2F_E_1` | `(-700, 1350, 850)` | `-90.00000000000001` | `(-828, 1222, 722)` | `(-572, 1478, 978)` |
| `Torch_2F_E_2` | `(300, 1350, 850)` | `-90.00000000000001` | `(172, 1222, 722)` | `(428, 1478, 978)` |
| `Torch_2F_N_1` | `(1050, -400, 850)` | `180` | `(922, -528, 722)` | `(1178, -272, 978)` |
| `Torch_2F_N_2` | `(1050, 400, 850)` | `180` | `(922, 272, 722)` | `(1178, 528, 978)` |

Every location is exact-integer equal to the requested triple. The `±90` yaws
carry float residue (`89.99999999999999`, `-90.00000000000001`) — that is how UE
stores a 90° rotator and matches the existing `BP_Door` actors, which show the
same values. The yaw comparison used a wrapped-angle tolerance rather than exact
equality, which is why those still pass.

### The bounding boxes are not the torch — read this before using them

**Every one of the 18 boxes is a uniform 256 × 256 × 256 cube centred exactly on
the actor location.** That is not the torch geometry. Command 54 measured the
torch's actual local extent as **65 × 26 × 42.87** (X −52..13, Y ±13, Z −41.87..1).

The cause was checked rather than guessed. Reading the components of a placed
torch:

```json
["DefaultSceneRoot", "BillboardComponent_12", "Backplate", "Bracket", "Cup",
 "Flame", "Light", "BillboardComponent_13"]
```

The placed actor carries **two `/Script/Engine.BillboardComponent`** instances —
editor sprite icons, one for the Actor and one added for the PointLightComponent —
which are not present in the Blueprint's own component list and which dominate the
bounds. They are editor-only and do not render in game.

**So `get_actor_bounds` on these actors reports the sprite envelope, not the
mesh.** The real geometry, from command 54 and unchanged here, extends 63 units
from the wall face into the room and hangs from Z −41.87 to Z +1 relative to each
actor origin. At the ground-floor torches that means roughly Z 208–251; at the
second-floor torches roughly Z 808–851.

---

## STEP 3 — the delete

**The delete set was re-derived from scratch rather than reusing the earlier
list.** Every actor in the level was enumerated, its class read with
`ObjectTools.get_class`, and only those whose class string was exactly
`/Script/Engine.PointLight` were selected. The script also refused to proceed
unless that set contained exactly 18 entries:

```python
if len(targets) != 18:
    return {"aborted": "expected exactly 18 PointLight actors", "found": len(targets)}
```

It did not abort. 18 targets, 18 deletes, all returned `true`:

| Label | Internal name deleted |
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
| `Torch_1F_W_1` | `PointLight_UAID_9C6B005AF86943FE02_1815541528` |
| `Torch_1F_W_2` | `PointLight_UAID_9C6B005AF86943FE02_1815609529` |
| `Torch_1F_E_1` | `PointLight_UAID_9C6B005AF86943FE02_1815703530` |
| `Torch_1F_E_2` | `PointLight_UAID_9C6B005AF86943FE02_1815836531` |
| `Torch_2F_N_1` | `PointLight_UAID_9C6B005AF86943FE02_1816014532` |
| `Torch_2F_N_2` | `PointLight_UAID_9C6B005AF86943FE02_1816153533` |

These are exactly the 18 internal names created in commands 49 and 50, so the
right objects were removed. No BP_Torch actor was in the target set, because none
of them has class `PointLight` — the class check is what made reusing the labels
safe.

---

## C) Zero PointLight-class actors remain

A full class histogram of all 120 actors was taken after the delete:

```json
{"pointlight_class_count": 0, "bp_torch_count": 18, "duplicate_labels": {}}
```

**`/Script/Engine.PointLight` does not appear in the histogram at all.** The 18
BP_Torch actors are present, and `duplicate_labels` is empty — the transient
double-labelling is resolved, each of the 18 labels now belongs to exactly one
actor.

The 18 labels found on BP_Torch actors are precisely the 18 requested:

```
Torch_1F_E_1, Torch_1F_E_2, Torch_1F_N_1, Torch_1F_N_2, Torch_1F_N_3, Torch_1F_N_4,
Torch_1F_S_1, Torch_1F_S_2, Torch_1F_S_3, Torch_1F_S_4, Torch_1F_W_1, Torch_1F_W_2,
Torch_2F_E_1, Torch_2F_E_2, Torch_2F_N_1, Torch_2F_N_2, Torch_2F_W_1, Torch_2F_W_2
```

### The do-not-touch actors all survived

| Actor | Count after |
|---|---|
| `DirectionalLight` | **1** |
| `SkyLight` | **1** |
| `SkyAtmosphere` | **1** |
| `VolumetricCloud` | **1** |
| `ExponentialHeightFog` | **1** |
| `PostProcessVolume` | **1** |

Confirmed independently in the class histogram: `/Script/Engine.DirectionalLight`
1, `/Script/Engine.SkyLight` 1, `/Script/Engine.SkyAtmosphere` 1,
`/Script/Engine.VolumetricCloud` 1, `/Script/Engine.ExponentialHeightFog` 1,
`/Script/Engine.PostProcessVolume` 1.

Also unchanged: `/Script/Engine.StaticMeshActor` **65** (every wall, floor, ramp,
railing, pillar and the ceiling slab), `BP_Door_C` **4**, `BP_Enemy_C` **6**,
`BP_StageRoom_C` **3**, `BP_ItemPickup_C` **3**, `BP_EndTrigger_C` **1**.

The `Lighting` outliner folder holds **25** actors: the 18 torches plus the 7
environment/lighting actors that were already there. Same as before the command.

---

## D) Actor count

| Stage | Count |
|---|---|
| Before | **120** |
| After creating 18 BP_Torch | **138** |
| After deleting 18 PointLight | **120** |

**Exactly the 120 → 138 → 120 the instruction predicted.**

---

## E) Packages written and removed

`AssetTools.save_assets` with `[]` returned `{"returnValue":true}`. Verified by
diffing a full `.uasset` listing captured before the command against one taken
after the save.

| | Before | After |
|---|---|---|
| Total `.uasset` files | **361** | **361** |
| `__ExternalActors__` packages | **156** | **156** |

The totals are unchanged because this was a one-for-one swap. The diff shows the
churn underneath:

### Written — 18 new packages, the BP_Torch actors

```
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/0/3M/P6JIGHZ879GWQXGT391UUE.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/4/3X/2GXVP3ZH3K0QJUXBX0Z91M.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/4/Q1/60U60G6J3GO4J6R3VQJWKU.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/5/JW/CM2PD8NYBNR2ZTBDGX6FU8.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/7/57/UU7NDMHA9OJ8L9W8D5AZYL.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/7/G9/9KYQPMJ1USTU6JIQGBGHSL.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/7/ZY/DK86JMBJG7GY1J09QO20TN.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/8/MX/8W0U3QCKVHMJVYRFF53VVM.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/8/YJ/PUBCXX0PV3IM7O2RMMDMRQ.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/KW/AM1SBVWN51GLKRVO179A4L.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/NG/W5B9FPBDBAFOWFY5W0EG1D.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/NG/XDT24DOHOISKSPTK5Y44BC.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/C/1Q/HMKIOS8ZGDUT8UQQLZNY89.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/C/DU/ZF7WMSHK1V7T3MF3SOO52C.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/C/VT/5G811NTTYAZ5DJH52GD3XM.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/D/KC/GT8X6H5TBDS1HXMGH1IMLU.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/E/TK/8818ACEC7Z8SCS0SAVQLAZ.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/E/X0/TJILOUY6XF4UI6CNQAAIVM.uasset
```

### Removed — 18 packages, the PointLight actors

```
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/0/YX/8NB34T0MH9HTLAY3XPEY0V.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/1/MS/K6HGPN9IDPNJG8QPVQPFI1.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/4/PQ/8HVI0Q1QL5MT82UHP43TP4.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/4/XP/4RHYBR78DKZYQMEUXEHW9B.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/5/O2/MO2UNWUFENDGG3OJYPQJ7T.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/5/Z1/LZ4IP07CLG11GM4RN1YF6L.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/7/QA/20YTIA1J4VHGBGJ4F5EUBY.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/8/C0/WLY15WGVH1FUO5DR4S2EWW.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/8/PX/1I144KLCEXOGEMRJIJVP08.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/A/PQ/O3HHOUW1GHRVTZ08BA0484.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/EO/74A1FMG5JLTS2WNL2U7TYE.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/PZ/68A4RY02IXX8CBJQS7ERCZ.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/B/QU/BUXIC4W4YV0HCXXHGU28HJ.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/C/66/J2GZ3QU79B85EDE19M9QQH.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/D/LB/81LCXWHJHFO0B6OZX92FL5.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/D/LE/0U4ALFPFVU9N12U74AC51M.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/D/Z3/S2SOVEWWMV4H62NJQPRIWS.uasset
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/E/WH/YRFJIUQW0OAUPJQ1SP5KE4.uasset
```

**These 18 removed files are exactly the 18 light packages still standing from
commands 49 and 50.** Command 49 wrote 13, command 51 removed one of them
(`0/80/S2JMC…`, the key light), leaving 12; command 50 wrote 6. 12 + 6 = 18, and
every one is in the removed list. Nothing else was removed.

**Nothing else was modified.** A `find` for files touched in the last 4 minutes
returned only the 18 new packages. No asset outside `__ExternalActors__` was
written — `BP_Torch.uasset`, `M_Flame.uasset`, `MI_Castle_Stone.uasset`,
`MI_Castle_Wood.uasset`, `M_FlatCol.uasset`, `SM_Cube/Cylinder/Ramp/Door.uasset`
and every `MI_PrototypeGrid_*` were untouched, which is the file-level proof that
no Blueprint, material or mesh asset was edited.

`git status` shows the swap directly: **18 ` D` deletions** of tracked packages and
**18 `??` new untracked directories**. Note the 4 ` M` mesh entries and the 4 `??`
asset entries are carried over from commands 52–54 and are unrelated to this
command.

**`Lvl_Stage.umap` was not written** — unchanged at 12,824 bytes, mtime
`2026-09-03 09:47:04`. Correct for a World Partition level.

Commands 52 through 55 are all on disk; none is committed.

---

## F) Warnings and errors, verbatim

This command's work runs from `12:30:00` (the creation script) to `12:34:24` (the
save). **No error was emitted.** One warning falls inside the window, and it is a
real one.

### The one that matters — virtual shadow map light overflow

```
[2026.09.03-12.33.48:332][286]LogRenderer: Warning: [VSM] One Pass Projection max lights overflow. If you see shadow artifacts, decrease the amount of local lights per pixel, or increase r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel.
```

**This is the first `LogRenderer` warning of any kind in the entire session.** The
full `LogRenderer` history is otherwise nine benign `Display` lines about ray
tracing PSOs and SBT recreation, dating back to editor startup. Nothing like this
appeared during commands 49, 50 or 51, when the same 18 lights existed as bare
PointLights.

It fired at `12:33:48`, four seconds after the delete step was dispatched at
`12:33:44` — i.e. on the first viewport redraw after the swap completed.

**What it means:** too many shadow-casting local lights overlap on some pixels for
the virtual shadow map's one-pass projection path to handle. Each torch now
contributes both a shadow-casting point light **and** three shadow-casting meshes
(Backplate, Bracket, Cup — only Flame has `castShadow false`), where before there
was a light and nothing else. That is the shadow cost flagged as unverified at the
end of commands 50 and 54, now confirmed by the engine itself rather than by
speculation.

The warning is conditional — "**If** you see shadow artifacts" — so it is not proof
of a visible defect. But it is a genuine signal that the lighting setup is at or
past a renderer limit, and it appeared only once, so it has not been characterised
under camera movement.

The two remedies the engine names are raising
`r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel` or reducing overlapping
local lights. **Neither was applied** — no console variable was changed and no
light was altered, because neither was part of this instruction.

### Warnings from just before this command

For completeness, these `LogScript` warnings sit immediately before the window and
belong to **command 54's** verification reads, not to this command. They are the
familiar "property does not exist on this component type" pattern:

```
[2026.09.03-12.23.59:350][361]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Backplate_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be read: Intensity, AttenuationRadius, LightColor, SourceRadius, CastShadows, IntensityUnits
[2026.09.03-12.24.00:006][363]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Bracket_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be read: Intensity, AttenuationRadius, LightColor, SourceRadius, CastShadows, IntensityUnits
[2026.09.03-12.24.00:340][364]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Cup_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be read: Intensity, AttenuationRadius, LightColor, SourceRadius, CastShadows, IntensityUnits
[2026.09.03-12.24.00:676][365]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Flame_GEN_VARIABLE' (StaticMeshComponent): the following properties could not be read: Intensity, AttenuationRadius, LightColor, SourceRadius, CastShadows, IntensityUnits
[2026.09.03-12.24.01:009][366]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Light_GEN_VARIABLE' (PointLightComponent): the following properties could not be read: StaticMesh, OverrideMaterials
[2026.09.03-12.24.01:340][367]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:Light_GEN_VARIABLE' (PointLightComponent): the following properties could not be read: CastShadow
[2026.09.03-12.24.01:343][367]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:DefaultSceneRoot_GEN_VARIABLE' (SceneComponent): the following properties could not be read: StaticMesh, OverrideMaterials
[2026.09.03-12.24.01:343][367]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Torch.BP_Torch_C:DefaultSceneRoot_GEN_VARIABLE' (SceneComponent): the following properties could not be read: Intensity, AttenuationRadius, LightColor, SourceRadius, CastShadows, IntensityUnits
```

**The 18 creations, the 18 deletes and the save produced no log output of their
own** — no per-actor spawn or destroy line, and no content validation pass for the
removals. As in command 51, the on-disk package diff in section E is the only
real evidence the deletions took effect.

---

## Not verified

- **Nothing was rendered or looked at. The lobby has still never been seen.** This
  is now seven commands of geometry, materials and lighting with zero visual
  evidence, and this command is the one that most needs it: the torches have gone
  in for the first time and the VSM warning says the renderer is unhappy.
- **PIE was not run.**
- **Whether the torches are visually correct is entirely unknown.** In particular:
  whether each torch's local +X actually faces into the room at every yaw, whether
  any torch intersects a wall, railing or the 2F walkway, and whether the flame
  emissive at `(1, 0.45, 0.12) × 30` reads as fire or as a white bloom. The yaw
  values came from the instruction and were applied as given; no trace or capture
  confirms the facing.
- **The VSM overflow was not characterised.** It fired once, on one frame, from one
  editor camera position. How bad it is under gameplay camera movement, and whether
  it produces visible shadow artifacts, is unmeasured.
- **The light contribution is assumed identical, not measured.** Each BP_Torch's
  Light component was verified in command 54 to carry bit-identical values to the
  old PointLights, and every torch sits at the exact coordinates of the light it
  replaced, so the lighting should be unchanged — but no trace, capture or
  luminance measurement confirms that. The three shadow-casting torch meshes now
  wrapped around each light are new occluders that did not exist before and will
  change the shadowing.
- **The navmesh was not rebuilt.** The torch meshes are new geometry at Z 208–251
  and Z 808–851. `Flame` has collision disabled, but Backplate, Bracket and Cup do
  not, so 54 new colliders now exist near the walls. Whether any intrudes on the
  walkable surface was not checked.
