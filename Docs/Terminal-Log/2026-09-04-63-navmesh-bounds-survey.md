# 2026-09-04-63 · Lvl_Stage geometry survey for NavMesh bounds Z

Read-only. No `set_properties`, no `save_assets`, no writes of any kind — every call below is a
read, and `git status` was not touched by this task.

**Read section 6 before choosing a number. The survey turns up a conflict that the Z-range
framing does not have an answer for: the wall tops that are collecting navmesh sit at Z 200 and
400, and the 2F floor the player must walk on tops at Z 550–600. No single ceiling separates
them.**

---

## 0 · PIE state and level

```
call: EditorToolset.EditorAppToolset.IsPIERunning
args: {}
```

```
{"returnValue":false}
```

```
call: editor_toolset.toolsets.scene.SceneTools.get_current_level
args: {}
```

```
{"returnValue":"/Game/ThirdPerson/Lvl_Stage"}
```

**No PIE session is running.** All reads hit the editor world; no `refPath` below carries a
`UEDPIE_0_` prefix.

Method note: all bounding boxes come from `ActorTools.get_actor_bounds`, which returns the
actor's world-space AABB. Nothing in this report is computed from location × scale by hand. Three
scripts ran; **all three completed with `"errors": []`** — no script failed part way, and no gap
in the data is being filled by anything other than a tool response.

---

## 1 · Every actor and its Z extent (the base dataset)

First, labels for all actors, so the later filters can be checked:

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: find_actors(all) then get_label for each
```

That returned `{"count": 120, ... "errors": [], "elapsed_sec": 28.0}` — 120 actors in the level.
(The full label list is long; every label referenced in this report comes from it.)

Then bounds for all 120, sorted by top Z:

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: for every actor -> [get_label, get_actor_bounds.min.z, get_actor_bounds.max.z, isValid], sorted by max.z
```

```
{"schema": "[label, boundsMinZ, boundsMaxZ, isValid] sorted by boundsMaxZ", "count": 120, "rows": [["ExponentialHeightFog", -6978, -6722, true], ["WorldSettings", 0, 0, true], ["WorldDataLayers", 0, 0, true], ["BuoyancyManager0", 0, 0, true], ["DefaultPhysicsVolume0", 0, 0, true], ["GameplayDebuggerPlayerManager0", 0, 0, true], ["Actor", 0, 0, true], ["Floor_Main", -50, 0, true], ["Floor_Room2", -50, 0, true], ["WorldPartitionMiniMap", 0, 0, true], ["Floor_LobbyNorth", -50, 0, true], ["Actor2", 0, 0, true], ["AbstractNavData-Default", 0, 0, true], ["Knife_Pickup", -30, 70, true], ["BP_ItemPickup2", -30, 70, true], ["BP_ItemPickup", -30, 70, true], ["Brush0", -128, 128, true], ["KnifeSpawnPoint", -108, 148, true], ["Enemy_R1_A", 0, 180, true], ["Enemy_Test2", 0, 180, true], ["Enemy_R3_A", -0.9664882859891577, 180, true], ["Enemy_R3_B", -0.9664882859891577, 180, true], ["Enemy_Test", -0.9664882859891577, 180, true], ["Enemy_R1_B", -0.9664882859891577, 180, true], ["Wall_Lobby_E_LowerB", 0, 200, true], ["Wall_S_Lower", 0, 200, true], ["Wall_R3_N_Lower", 0, 200, true], ["Wall_W_Lower", 0, 200, true], ["Wall_E_Lower", 0, 200, true], ["Wall_Lobby_W_LowerA", 0, 200, true], ["Wall_Lobby_N_LowerA", 0, 200, true], ["Wall_R2_N_Lower", 0, 200, true], ["Wall_R2_W_Lower", 0, 200, true], ["Wall_Lobby_E_LowerA", 0, 200, true], ["Wall_R2_E_Lower", 0, 200, true], ["Wall_Lobby_W_LowerB", 0, 200, true], ["Wall_Lobby_N_LowerB", 0, 200, true], ["Wall_R1_N_Lower", 0, 200, true], ["PlayerStart", 64.01264300000003, 320.012643, true], ["Torch_1F_N_1", 122, 378, true], ["Torch_1F_S_4", 122, 378, true], ["Torch_1F_S_2", 122, 378, true], ["Torch_1F_W_1", 122, 378, true], ["Torch_1F_N_3", 122, 378, true], ["Torch_1F_E_1", 122, 378, true], ["Torch_1F_E_2", 122, 378, true], ["Torch_1F_S_3", 122, 378, true], ["Torch_1F_N_4", 122, 378, true], ["Torch_1F_N_2", 122, 378, true], ["Torch_1F_S_1", 122, 378, true], ["Torch_1F_W_2", 122, 378, true], ["Room2", -128, 400, true], ["Door_R2", 0, 400, true], ["Room1", -128, 400, true], ["Door_R1", 0, 400, true], ["Wall_S_Upper", 200, 400, true], ["Wall_R2_N_Upper", 200, 400, true], ["Wall_E_Upper", 200, 400, true], ["Wall_Lobby_W_UpperA", 200, 400, true], ["Wall_W_Upper", 200, 400, true], ["Wall_R2_E_Upper", 200, 400, true], ["Room3", -128, 400, true], ["Door_R3", 0, 400, true], ["Wall_R2_W_Upper", 200, 400, true], ["Wall_Lobby_N_UpperB", 200, 400, true], ["Wall_Lobby_W_UpperB", 200, 400, true], ["Wall_Lobby_E_UpperA", 200, 400, true], ["Wall_Lobby_N_UpperA", 200, 400, true], ["Wall_Lobby_E_UpperB", 200, 400, true], ["Wall_R1_N_Upper", 200, 400, true], ["Wall_R3_N_Upper", 200, 400, true], ["Pillar_W1", 0, 550, true], ["Pillar_W2", 0, 550, true], ["Pillar_E1", 0, 550, true], ["Pillar_E2", 0, 550, true], ["Pillar_W3", 0, 550, true], ["Pillar_E3", 0, 550, true], ["RecastNavMesh-Default", 10, 570, true], ["Floor_2F_East", 550, 600, true], ["NavBounds_Main", -200, 600, true], ["PostProcessVolume", 400, 600, true], ["Ramp_E", 0, 600, true], ["Floor_2F_West", 550, 600, true], ["Ramp_W", 0, 600, true], ["Floor_2F_North", 550, 600, true], ["Floor_End_B", 550, 600, true], ["Wall_2F_N_Sill", 400, 600, true], ["Floor_End_A", 550, 600, true], ["Rail_2F_E", 600, 700, true], ["Rail_2F_W", 600, 700, true], ["Rail_2F_N_A", 600, 700, true], ["Rail_2F_N_B", 600, 700, true], ["Rail_2F_N_C", 600, 700, true], ["VolumetricCloud", 692, 948, true], ["Torch_2F_N_1", 722, 978, true], ["Torch_2F_W_1", 722, 978, true], ["Torch_2F_E_1", 722, 978, true], ["Torch_2F_E_2", 722, 978, true], ["Torch_2F_N_2", 722, 978, true], ["Torch_2F_W_2", 722, 978, true], ["Door_Final", 600, 1000, true], ["EndTrigger", 472, 1000, true], ["SkyLight", -1, 1136, true], ["Wall_2F_N_A", 400, 1200, true], ["Wall_End_S_B", 600, 1200, true], ["Wall_End_N", 600, 1200, true], ["Wall_Cor_W", 600, 1200, true], ["Wall_2F_W", 400, 1200, true], ["Wall_2F_S", 400, 1200, true], ["Wall_2F_E", 400, 1200, true], ["Wall_2F_N_B", 400, 1200, true], ["Wall_Cor_E", 600, 1200, true], ["Wall_2F_N_Lintel", 1000, 1200, true], ["Wall_End_W", 600, 1200, true], ["Wall_End_E", 600, 1200, true], ["Wall_End_S_A", 600, 1200, true], ["SkyAtmosphere", 992, 1248, true], ["Ceiling_Lobby", 1200, 1250, true], ["DirectionalLight", 536.1516360373016, 1320.2016616671815, true], ["SM_SkySphere", -1638400, 1638400, true]], "errors": [], "elapsed_sec": 52.66}
```

---

## 2 · Item 1 — every StaticMeshActor whose label contains "Wall"

Detail for the whole Wall/Floor/Ceiling/Ramp/Stair/Step/Rail set came from one script:

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: for every actor whose lowercased label contains wall/floor/ceiling/ramp/stair/step/rail ->
        get_class, get_actor_transform, get_actor_bounds, and StaticMesh from its StaticMeshComponent
```

It returned `{"matched": 58, ... "errors": [], "elapsed_sec": 57.34}`. **58 actors matched, all of
class `/Script/Engine.StaticMeshActor`, all with a static mesh resolved — no error, no null.**
42 of the 58 are Walls; the other 16 are in section 3.

Every mesh in this table is `/Game/LevelPrototyping/Meshes/SM_Cube.SM_Cube`. Every rotation is
pitch 0 / yaw 0 / roll 0. In this level `SM_Cube`'s pivot is at its minimum corner, so
`bounds.min` equals the actor location in all three axes — visible in the raw response and worth
knowing when reading the numbers.

| Label | Location (x, y, z) | Scale (x, y, z) | Bottom Z | **Top Z** | Mesh |
| --- | --- | --- | --- | --- | --- |
| Wall_2F_E | -1300, 1400, 400 | 26, 2, 8 | 400 | **1200** | SM_Cube |
| Wall_2F_N_A | 1100, -1400, 400 | 2, 13, 8 | 400 | **1200** | SM_Cube |
| Wall_2F_N_B | 1100, 100, 400 | 2, 13, 8 | 400 | **1200** | SM_Cube |
| Wall_2F_N_Lintel | 1100, -100, 1000 | 2, 2, 2 | 1000 | **1200** | SM_Cube |
| Wall_2F_N_Sill | 1100, -100, 400 | 2, 2, 2 | 400 | **600** | SM_Cube |
| Wall_2F_S | -1300, -1400, 400 | 2, 28, 8 | 400 | **1200** | SM_Cube |
| Wall_2F_W | -1300, -1600, 400 | 26, 2, 8 | 400 | **1200** | SM_Cube |
| Wall_Cor_E | 1300, 100, 600 | 4, 2, 6 | 600 | **1200** | SM_Cube |
| Wall_Cor_W | 1300, -300, 600 | 4, 2, 6 | 600 | **1200** | SM_Cube |
| Wall_E_Lower | -1300, 3600, 0 | 20, 2, 2 | 0 | **200** | SM_Cube |
| Wall_E_Upper | -1300, 3600, 200 | 20, 2, 2 | 200 | **400** | SM_Cube |
| Wall_End_E | 1900, 600, 600 | 8, 2, 6 | 600 | **1200** | SM_Cube |
| Wall_End_N | 2700, -800, 600 | 2, 16, 6 | 600 | **1200** | SM_Cube |
| Wall_End_S_A | 1700, -800, 600 | 2, 7, 6 | 600 | **1200** | SM_Cube |
| Wall_End_S_B | 1700, 100, 600 | 2, 7, 6 | 600 | **1200** | SM_Cube |
| Wall_End_W | 1900, -800, 600 | 8, 2, 6 | 600 | **1200** | SM_Cube |
| Wall_Lobby_E_LowerA | -1300, 1400, 0 | 9, 2, 2 | 0 | **200** | SM_Cube |
| Wall_Lobby_E_LowerB | -200, 1400, 0 | 15, 2, 2 | 0 | **200** | SM_Cube |
| Wall_Lobby_E_UpperA | -1300, 1400, 200 | 9, 2, 2 | 200 | **400** | SM_Cube |
| Wall_Lobby_E_UpperB | -200, 1400, 200 | 15, 2, 2 | 200 | **400** | SM_Cube |
| Wall_Lobby_N_LowerA | 1100, -1600, 0 | 2, 15, 2 | 0 | **200** | SM_Cube |
| Wall_Lobby_N_LowerB | 1100, 100, 0 | 2, 15, 2 | 0 | **200** | SM_Cube |
| Wall_Lobby_N_UpperA | 1100, -1600, 200 | 2, 15, 2 | 200 | **400** | SM_Cube |
| Wall_Lobby_N_UpperB | 1100, 100, 200 | 2, 15, 2 | 200 | **400** | SM_Cube |
| Wall_Lobby_W_LowerA | -1300, -1600, 0 | 9, 2, 2 | 0 | **200** | SM_Cube |
| Wall_Lobby_W_LowerB | -200, -1600, 0 | 15, 2, 2 | 0 | **200** | SM_Cube |
| Wall_Lobby_W_UpperA | -1300, -1600, 200 | 9, 2, 2 | 200 | **400** | SM_Cube |
| Wall_Lobby_W_UpperB | -200, -1600, 200 | 15, 2, 2 | 200 | **400** | SM_Cube |
| Wall_R1_N_Lower | 500, -3600, 0 | 2, 22, 2 | 0 | **200** | SM_Cube |
| Wall_R1_N_Upper | 500, -3600, 200 | 2, 22, 2 | 200 | **400** | SM_Cube |
| Wall_R2_E_Lower | 1300, 1000, 0 | 18, 2, 2 | 0 | **200** | SM_Cube |
| Wall_R2_E_Upper | 1300, 1000, 200 | 18, 2, 2 | 200 | **400** | SM_Cube |
| Wall_R2_N_Lower | 2900, -1200, 0 | 2, 24, 2 | 0 | **200** | SM_Cube |
| Wall_R2_N_Upper | 2900, -1200, 200 | 2, 24, 2 | 200 | **400** | SM_Cube |
| Wall_R2_W_Lower | 1300, -1200, 0 | 18, 2, 2 | 0 | **200** | SM_Cube |
| Wall_R2_W_Upper | 1300, -1200, 200 | 18, 2, 2 | 200 | **400** | SM_Cube |
| Wall_R3_N_Lower | 500, 1400, 0 | 2, 24, 2 | 0 | **200** | SM_Cube |
| Wall_R3_N_Upper | 500, 1400, 200 | 2, 24, 2 | 200 | **400** | SM_Cube |
| Wall_S_Lower | -1300, -3600, 0 | 2, 74, 2 | 0 | **200** | SM_Cube |
| Wall_S_Upper | -1300, -3600, 200 | 2, 74, 2 | 200 | **400** | SM_Cube |
| Wall_W_Lower | -1300, -3600, 0 | 20, 2, 2 | 0 | **200** | SM_Cube |
| Wall_W_Upper | -1300, -3600, 200 | 20, 2, 2 | 200 | **400** | SM_Cube |

### Wall top-Z summary

- **Count:** 42 wall actors, all StaticMeshActor, all SM_Cube.
- **Minimum top Z: 200**
- **Maximum top Z: 1200**
- **Distinct top-Z values: {200, 400, 600, 1200}** — exactly four.

| Top Z | How many | Which |
| --- | --- | --- |
| 200 | 14 | every `*_Lower*` wall |
| 400 | 14 | every `*_Upper*` wall |
| 600 | 1 | Wall_2F_N_Sill |
| 1200 | 13 | Wall_2F_E/W/S, Wall_2F_N_A/B, Wall_2F_N_Lintel, Wall_Cor_E/W, Wall_End_E/N/S_A/S_B/W |

Bottom Z across the walls: minimum 0, maximum 1000 (Wall_2F_N_Lintel), distinct set
{0, 200, 400, 600, 1000}.

---

## 3 · Item 2 — Floor / Ceiling / Ramp / Stair / Step / Rail

From the same script response. No actor label in this level contains "Stair" or "Step" — those two
keywords matched nothing, which is a result, not a gap.

| Label | Location (x, y, z) | Scale (x, y, z) | Bottom Z | **Top Z** | Mesh |
| --- | --- | --- | --- | --- | --- |
| Ceiling_Lobby | -1300, -1600, 1200 | 26, 32, 0.5 | 1200 | **1250** | SM_Cube |
| Floor_2F_East | -1100, 1000, 550 | 18, 4, 0.5 | 550 | **600** | SM_Cube |
| Floor_2F_North | 700, -1400, 550 | 4, 28, 0.5 | 550 | **600** | SM_Cube |
| Floor_2F_West | -1100, -1400, 550 | 18, 4, 0.5 | 550 | **600** | SM_Cube |
| Floor_End_A | 1300, -300, 550 | 4, 6, 0.5 | 550 | **600** | SM_Cube |
| Floor_End_B | 1700, -800, 550 | 12, 16, 0.5 | 550 | **600** | SM_Cube |
| Floor_LobbyNorth | 500, -1600, -50 | 8, 32, 0.5 | -50 | **0** | SM_Cube |
| Floor_Main | -1300, -3600, -50 | 20, 74, 0.5 | -50 | **0** | SM_Cube |
| Floor_Room2 | 1100, -1200, -50 | 20, 24, 0.5 | -50 | **0** | SM_Cube |
| Rail_2F_E | -1100, 1000, 600 | 18, 1, 1 | 600 | **700** | SM_Cube |
| Rail_2F_N_A | 700, -1000, 600 | 1, 1, 1 | 600 | **700** | SM_Cube |
| Rail_2F_N_B | 700, -300, 600 | 1, 6, 1 | 600 | **700** | SM_Cube |
| Rail_2F_N_C | 700, 900, 600 | 1, 1, 1 | 600 | **700** | SM_Cube |
| Rail_2F_W | -1100, -1100, 600 | 18, 1, 1 | 600 | **700** | SM_Cube |
| Ramp_E | 700, 300, 0 | 6, 10, 6 | 0 | **600** | SM_Ramp |
| Ramp_W | 700, -900, 0 | 6, 10, 6 | 0 | **600** | SM_Ramp |

Two of these differ from the rest and matter for the decision:

- **Ramp_E and Ramp_W** are the only actors here using
  `/Game/LevelPrototyping/Meshes/SM_Ramp.SM_Ramp`, and the only ones with a non-zero rotation
  (`yaw 89.99999999999999`). Their bounds run **from Z 0 to Z 600** — a single actor spanning the
  whole climb from ground floor to second floor. Their X bounds show the rotation:
  `Ramp_E` min x `-300.0000000000002`, max x `700.0000000000001`.
- **The 2F floors top at exactly 600**, the same number as the current NavMesh bounds ceiling.

---

## 4 · Item 3 — PlayerStart

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: find_actors("PlayerStart" | "NavBounds" | "RecastNavMesh") -> get_class, get_actor_transform, get_actor_bounds
```

```
{"PlayerStart": [{"ref": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.PlayerStart_UAID_F4A475FF15A3736A02_1961960731", "class": "/Script/Engine.PlayerStart", "transform": {"location": {"x": 0, "y": 0, "z": 192.01264300000003}, "rotation": {"pitch": 0, "yaw": 0, "roll": 0}, "scale": {"x": 1, "y": 1, "z": 1}}, "bounds": {"min": {"x": -128, "y": -128, "z": 64.01264300000003}, "max": {"x": 240, "y": 128, "z": 320.012643}, "isValid": true}}], "NavBounds": [{"ref": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.NavMeshBoundsVolume_UAID_9C6B005AF86909FD02_1188892250", "class": "/Script/NavigationSystem.NavMeshBoundsVolume", "transform": {"location": {"x": 900, "y": 100, "z": 200}, "rotation": {"pitch": 0, "yaw": 0, "roll": 0}, "scale": {"x": 23, "y": 38, "z": 4}}, "bounds": {"min": {"x": -1400, "y": -3700, "z": -200}, "max": {"x": 3200, "y": 3900, "z": 600}, "isValid": true}}], "RecastNavMesh": [{"ref": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default", "class": "/Script/NavigationSystem.RecastNavMesh", "transform": {"location": {"x": 0, "y": 0, "z": 0}, "rotation": {"pitch": 0, "yaw": 0, "roll": 0}, "scale": {"x": 1, "y": 1, "z": 1}}, "bounds": {"min": {"x": -1976, "y": -3952, "z": 10}, "max": {"x": 3952, "y": 3952, "z": 570}, "isValid": true}}]}
```

**PlayerStart location: (0, 0, 192.01264300000003).** Its capsule bounds run Z 64.01264300000003
to 320.012643.

The walkable surface underneath it is `Floor_Main`, whose top is **Z 0** — PlayerStart sits 192
units above it, which is the usual PlayerStart float, not a raised platform. The floor the player
spawns on is at **Z 0**.

Two useful confirmations in the same response:

- **NavBounds_Main** world bounds are Z **-200 to 600**, matching the description in the task.
- **RecastNavMesh-Default** — the *generated* navmesh — has bounds Z **10 to 570**, not up to 600.

---

## 5 · Item 4 — everything whose top Z falls between 250 and 650

Filtered from the section 1 dataset. **50 actors of the 120 have a bounding-box top Z in
[250, 650].**

| Top Z | Count | Actors |
| --- | --- | --- |
| 320.012643 | 1 | PlayerStart |
| 378 | 12 | Torch_1F_N_1, Torch_1F_N_2, Torch_1F_N_3, Torch_1F_N_4, Torch_1F_S_1, Torch_1F_S_2, Torch_1F_S_3, Torch_1F_S_4, Torch_1F_E_1, Torch_1F_E_2, Torch_1F_W_1, Torch_1F_W_2 |
| 400 | 20 | Wall_S_Upper, Wall_E_Upper, Wall_W_Upper, Wall_R1_N_Upper, Wall_R2_E_Upper, Wall_R2_N_Upper, Wall_R2_W_Upper, Wall_R3_N_Upper, Wall_Lobby_E_UpperA, Wall_Lobby_E_UpperB, Wall_Lobby_N_UpperA, Wall_Lobby_N_UpperB, Wall_Lobby_W_UpperA, Wall_Lobby_W_UpperB, Room1, Room2, Room3, Door_R1, Door_R2, Door_R3 |
| 550 | 6 | Pillar_W1, Pillar_W2, Pillar_W3, Pillar_E1, Pillar_E2, Pillar_E3 |
| 570 | 1 | RecastNavMesh-Default (the navmesh actor itself) |
| 600 | 10 | Floor_2F_East, Floor_2F_West, Floor_2F_North, Floor_End_A, Floor_End_B, Ramp_E, Ramp_W, Wall_2F_N_Sill, NavBounds_Main, PostProcessVolume |

Just outside the band, and relevant because they are the nearest things above it:

- **Rail_2F_E, Rail_2F_W, Rail_2F_N_A, Rail_2F_N_B, Rail_2F_N_C — top Z 700**, bottom 600. The
  2F railings sit entirely above 650.
- Below the band: every `*_Lower*` wall tops at 200, the six enemies at 180.

---

## 6 · What the numbers say about where to cut

The task frames this as "walkable navmesh on top of the room walls, so lower the ceiling". The
numbers do not support a clean version of that move, and this is the part worth reading before
picking a value.

**The wall tops that can collect navmesh are at Z 200 (14 walls) and Z 400 (14 walls).** The
13 walls topping at 1200 are already far above the current 600 ceiling and cannot be the source.

**The 2F floor tops at Z 550–600** (Floor_2F_East/West/North, Floor_End_A/B), and both ramps run
0 → 600 to reach it.

So the two things sit in this order: wall tops at 200 and 400, then the 2F walkable floor at 600,
**above** them. Any ceiling low enough to exclude the 400 wall tops also excludes the entire second
floor and both ramps. There is no Z value that keeps the 2F floor and drops the wall tops — a
single axis-aligned ceiling cannot separate them, because the unwanted surfaces are *below* the
wanted one.

Two further observations from the data, both of which change what the fix should probably be:

**a. The 2F floor may already have no navmesh.** The generated `RecastNavMesh-Default` bounds top
out at **Z 570**, while the 2F floor top is **600** and the NavBounds ceiling is also **600**.
Recast needs clear voxel space above a surface for the agent to stand — `AgentHeight` is 144
(section 7) — and there are only 0 units between the floor top and the bounds ceiling. That is
consistent with the second floor being unreachable by the navmesh right now, and with 570 being
the highest thing that did generate (the pillar tops at 550, plus cell height). **This is
inference from the bounds numbers, not a measurement of the navmesh polys** — I did not query the
navmesh tile data, and there is no MCP tool here that exposes it.

**b. If anything, the ceiling is too low, not too high.** To cover the 2F floor at 600 the volume
would need to reach roughly 600 + 144 (AgentHeight) = ~744 or above, which also swallows the rails
at 700.

If the goal is specifically to stop navmesh appearing on the 200/400 wall tops, the levers the
data points at are not the Z ceiling: the wall tops are 200 units wide (scale 2 on the thin axis)
against an `AgentRadius` of 35, so they are wide enough to hold a walkable strip. Marking the wall
actors as not affecting navigation, or giving them a NavArea of Null, cuts them without touching
the volume. Choosing between those is a design decision and is outside a read-only survey — no
change was made.

---

## 7 · Item 5 — RecastNavMesh settings

First attempt asked for the property names the task used, and **three of them do not exist on this
class in UE 5.8**:

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default"}, "properties": ["AgentRadius", "AgentHeight", "AgentMaxStepHeight", "AgentMaxSlope", "CellSize", "CellHeight", "RuntimeGeneration"]}
```

```
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default' (RecastNavMesh): the following properties could not be read: AgentMaxStepHeight, CellSize, CellHeight
```

Listing the class's properties confirms they are absent rather than misspelled:

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: list_properties on RecastNavMesh, filtered to names containing agent/cell/runtime/step/slope/tile/height/radius
```

```
{"total_properties": 146, "candidates": ["bDrawTileBounds", "bDrawTileResolutions", "bDrawTileLabels", "bDrawTileBuildTimes", "bDrawTileBuildTimesHeatMap", "tileGenerationDebug", "bFixedTilePoolSize", "tilePoolSize", "tileSizeUU", "averageLayersPerTile", "agentRadius", "agentHeight", "agentMaxSlope", "maxSimultaneousTileGenerationJobsCount", "tileNumberHardLimit", "expectedMaxLayersPerTile", "polyRefTileBits", "ledgeSlopeFilterMode", "bMarkLowHeightAreas", "bUseExtraTopCellWhenMarkingAreas", "bFilterLowSpanFromTileCache", "invokerTilePriorityBumpDistanceThresholdInTileUnits", "invokerTilePriorityBumpIncrease", "runtimeGeneration", "runtimeGrid"]}
```

`agentRadius`, `agentHeight`, `agentMaxSlope`, `runtimeGeneration` are there; no `cellSize`,
`cellHeight` or `agentMaxStepHeight`. The engine source says why — checked rather than guessed, in
`Engine/Source/Runtime/NavigationSystem/Public/NavMesh/RecastNavMesh.h`:

```
$ grep -n "AgentMaxStepHeight\|float CellSize\|float CellHeight\|GetCellSize\|GetCellHeight" ".../NavMesh/RecastNavMesh.h"
555:	bool IsValid() const { return CellSize > 0.f && CellHeight > 0.f && AgentMaxStepHeight > 0.f; }
559:	float CellSize = 25.f;
563:	float CellHeight = 10.f;
567:	float AgentMaxStepHeight = 35.f;
712:	float CellSize;
716:	float CellHeight;
718:	UE_DEPRECATED(all, "Use NavMeshResolutionParams to set AgentMaxStepHeight for the different resolutions instead")
719:	UPROPERTY(config, meta = (DeprecatedProperty, DeprecationMessage = "Use NavMeshResolutionParams to set AgentMaxStepHeight for the different resolutions instead"))
720:	float AgentMaxStepHeight;
1107:	float GetCellSize(const ENavigationDataResolution Resolution) const { return NavMeshResolutionParams[(uint8)Resolution].CellSize; }
1113:	float GetCellHeight(const ENavigationDataResolution Resolution) const { return NavMeshResolutionParams[(uint8)Resolution].CellHeight; }
1118:	/** Get the AgentMaxStepHeight for the given resolution. */
1119:	float GetAgentMaxStepHeight(const ENavigationDataResolution Resolution) const { return NavMeshResolutionParams[(uint8)Resolution].AgentMaxStepHeight; }
```

In UE 5.8 those three moved into the per-resolution `NavMeshResolutionParams` array, and the
top-level copies are deprecated and no longer reflected. Reading them there:

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default"}, "properties": ["AgentRadius", "AgentHeight", "AgentMaxSlope", "RuntimeGeneration", "NavMeshResolutionParams", "TileSizeUU", "TilePoolSize"]}
```

```
{"returnValue":"{\"AgentRadius\":35,\"AgentHeight\":144,\"AgentMaxSlope\":44,\"RuntimeGeneration\":\"Dynamic\",\"NavMeshResolutionParams\":[{\"cellSize\":38,\"cellHeight\":10,\"agentMaxStepHeight\":35},{\"cellSize\":19,\"cellHeight\":10,\"agentMaxStepHeight\":35},{\"cellSize\":19,\"cellHeight\":10,\"agentMaxStepHeight\":35}],\"TileSizeUU\":1000,\"TilePoolSize\":1024}"}
```

| Setting | Value |
| --- | --- |
| AgentRadius | 35 |
| AgentHeight | 144 |
| AgentMaxSlope | 44 |
| RuntimeGeneration | **Dynamic** |
| AgentMaxStepHeight | 35 — per resolution: Low 35, Default 35, High 35 |
| CellSize | per resolution: Low 38, Default 19, High 19 |
| CellHeight | per resolution: Low 10, Default 10, High 10 |
| TileSizeUU | 1000 |
| TilePoolSize | 1024 |

The three array entries are the Low / Default / High navmesh resolutions in that declaration
order; the tool returns the array without labelling which is which, so that mapping comes from the
engine header, not from the response.

`RuntimeGeneration: Dynamic` means the navmesh rebuilds at runtime, so a bounds change takes
effect without a manual rebuild — but it also means the setting is not just an editor-time
convenience.

---

## 8 · What was not done

No writes. No `set_properties`, no `save_assets`, no bounds change, no rebuild. The only
non-`unreal-mcp` command was one `grep` against the read-only engine headers under
`C:\Program Files\Epic Games\UE_5.8\`.

Not measured: the actual navmesh polygons. Section 6a argues from the `RecastNavMesh-Default`
actor bounds (Z 10–570) that the second floor is probably not covered, but no tool available here
reads navmesh tile or poly data, so that remains inference. Confirming it would mean looking at
the navmesh debug draw in the viewport — a human-eyes check, or a viewport capture.

Also not surveyed: whether any of the 42 wall actors already carry a `bCanEverAffectNavigation`
override or a custom NavArea. That was not asked for and was not read.
