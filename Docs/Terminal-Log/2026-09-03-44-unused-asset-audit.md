# 2026-09-03 · Command 44 — Unused asset audit (DRY RUN, nothing deleted)

**Dry run only. Nothing was deleted, moved, renamed or saved. PIE was not run.**
No write tool of any kind was called against the project — the only calls were
`find_assets`, `exists`, `get_referencers`, `get_dependencies` and
`get_asset_class`, all read-only.

Current level throughout: `/Game/ThirdPerson/Lvl_Stage`.

**Headline: the delete set is 83 assets. It has ZERO referencers from outside
itself. Verified twice, from both directions. The two KEEP LIST assets are
correctly excluded — and one of them, `ABP_FP_Copy`, is genuinely load-bearing:
it is referenced by `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`,
which is not in the delete set.**

**Also: the premise in step 5 was wrong. `/Game/Weapons/Rifle/SM_Rifle` does not
exist and never did. The asset is at `/Game/Weapons/Rifle/Meshes/SM_Rifle` —
the path in the question was missing the `Meshes/` segment. `get_referencers`
was correct to reject it. See section 5.**

---

## 1. Delete set enumeration

`AssetTools.find_assets`, empty `name`, `recursive: true` for the three folder
paths. The two single-asset paths were confirmed with `AssetTools.exists`.

| Path | Count |
|---|---|
| `/Game/Variant_Shooter/` | **50** |
| `/Game/Weapons/` | **27** |
| `/Game/FirstPerson/Blueprints/` | **4** |
| `/Game/FirstPerson/Lvl_FirstPerson` | **1** (`exists` → `true`) |
| `/Game/FirstPerson/MI_FirstPersonColorway` | **1** (`exists` → `true`) |
| **Total delete set** | **83** |

The script computed `delete_set_size: 83` and `delete_set_unique: 83` — no path
appears twice, so the three folders do not overlap.

### `/Game/Variant_Shooter/` — 50 assets

```
/Game/Variant_Shooter/Input/Actions/IA_Shoot
/Game/Variant_Shooter/Input/Actions/IA_SwapWeapon
/Game/Variant_Shooter/Lvl_ArenaShooter
/Game/Variant_Shooter/Anims/ABP_FP_Pistol
/Game/Variant_Shooter/Anims/ABP_FP_Weapon
/Game/Variant_Shooter/Anims/ABP_TP_Pistol
/Game/Variant_Shooter/Anims/ABP_TP_Rifle
/Game/Variant_Shooter/Anims/Ctrl_HandAdjusment
/Game/Variant_Shooter/Anims/Ctrl_HandAdjusment_Pistol
/Game/Variant_Shooter/Anims/FP_Rifle_Shoot_Montage
/Game/Variant_Shooter/Blueprints/BPI_Shooter
/Game/Variant_Shooter/Blueprints/BPI_Teammate
/Game/Variant_Shooter/Blueprints/BP_ShooterCharacter
/Game/Variant_Shooter/Blueprints/BP_ShooterGameMode
/Game/Variant_Shooter/Blueprints/BP_ShooterPlayerController
/Game/Variant_Shooter/Blueprints/AI/BP_ShooterAIController
/Game/Variant_Shooter/Blueprints/AI/BP_ShooterNPC
/Game/Variant_Shooter/Blueprints/AI/BP_ShooterNPCSpawner
/Game/Variant_Shooter/Blueprints/AI/ST_Shooter
/Game/Variant_Shooter/Blueprints/AI/ST_Shooter_ShootAtTarget
/Game/Variant_Shooter/Blueprints/AI/EQS/EnvQueryContext_Target
/Game/Variant_Shooter/Blueprints/AI/EQS/EQS_FindRoamLocation
/Game/Variant_Shooter/Blueprints/AI/EQS/EQS_FindSnipingLocation
/Game/Variant_Shooter/Blueprints/AI/StateTree/StateTreeCondition_HasLineOfSightToTarget
/Game/Variant_Shooter/Blueprints/AI/StateTree/StateTreeTask_FaceActor
/Game/Variant_Shooter/Blueprints/AI/StateTree/StateTreeTask_FaceLocation
/Game/Variant_Shooter/Blueprints/AI/StateTree/StateTreeTask_SenseEnemies
/Game/Variant_Shooter/Blueprints/AI/StateTree/StateTreeTask_SetRandomFloat
/Game/Variant_Shooter/Blueprints/AI/StateTree/StateTreeTask_ShootAtTarget
/Game/Variant_Shooter/Blueprints/Pickups/DT_WeaponList
/Game/Variant_Shooter/Blueprints/Pickups/ST_WeaponTableRow
/Game/Variant_Shooter/Blueprints/Pickups/BPI_Pickups
/Game/Variant_Shooter/Blueprints/Pickups/BPI_WeaponHolder
/Game/Variant_Shooter/Blueprints/Pickups/BP_ShooterPickup
/Game/Variant_Shooter/Blueprints/Pickups/BP_ShooterWeaponBase
/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectileBase
/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Bullet
/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_ShooterProjectile_Grenade
/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/BP_Shooter_GrenadeExplosion
/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/Materials/M_Explosion
/Game/Variant_Shooter/Blueprints/Pickups/Projectiles/Meshes/SM_FoamBullet
/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_GrenadeLauncher
/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Pistol
/Game/Variant_Shooter/Blueprints/Pickups/Weapons/BP_ShooterWeapon_Rifle
/Game/Variant_Shooter/Input/BPI_Touch_Shooter
/Game/Variant_Shooter/Input/IMC_Weapons
/Game/Variant_Shooter/Input/UI_TouchInterface_Shooter
/Game/Variant_Shooter/UI/M_BulletCounter
/Game/Variant_Shooter/UI/UI_Shooter
/Game/Variant_Shooter/UI/UI_ShooterBulletCounter
```

### `/Game/Weapons/` — 27 assets

```
/Game/Weapons/GrenadeLauncher/Audio/FirstPersonTemplateWeaponFire02
/Game/Weapons/GrenadeLauncher/Materials/M_GrenadeLauncher
/Game/Weapons/GrenadeLauncher/Materials/M_ProjectileBullet
/Game/Weapons/GrenadeLauncher/Meshes/SK_GrenadeLauncher
/Game/Weapons/GrenadeLauncher/Meshes/FirstPersonProjectileMesh
/Game/Weapons/GrenadeLauncher/Meshes/PA_GrenadeLauncher
/Game/Weapons/GrenadeLauncher/Meshes/SKM_GrenadeLauncher
/Game/Weapons/GrenadeLauncher/Meshes/SM_GrenadeLauncher
/Game/Weapons/GrenadeLauncher/Textures/T_FPGun_M
/Game/Weapons/GrenadeLauncher/Textures/T_FPGun_N
/Game/Weapons/Pistol/Materials/MI_Weapon_Pistol
/Game/Weapons/Pistol/Meshes/SK_Pistol
/Game/Weapons/Pistol/Meshes/PA_Pistol
/Game/Weapons/Pistol/Meshes/SKM_Pistol
/Game/Weapons/Pistol/Meshes/SM_Pistol
/Game/Weapons/Pistol/Textures/T_Pistol_AORM
/Game/Weapons/Pistol/Textures/T_Pistol_D
/Game/Weapons/Pistol/Textures/T_Pistol_Masks
/Game/Weapons/Pistol/Textures/T_Pistol_N
/Game/Weapons/Rifle/Materials/M_Rifle
/Game/Weapons/Rifle/Materials/M_Weapon
/Game/Weapons/Rifle/Meshes/SK_Rifle
/Game/Weapons/Rifle/Meshes/PA_Rifle
/Game/Weapons/Rifle/Meshes/SKM_Rifle
/Game/Weapons/Rifle/Meshes/SM_Rifle
/Game/Weapons/Rifle/Textures/T_Rifle_BC
/Game/Weapons/Rifle/Textures/T_Rifle_N
```

### `/Game/FirstPerson/Blueprints/` — 4 assets

```
/Game/FirstPerson/Blueprints/BP_FirstPersonCameraManager
/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter
/Game/FirstPerson/Blueprints/BP_FirstPersonGameMode
/Game/FirstPerson/Blueprints/BP_FirstPersonPlayerController
```

### The two single assets

```
/Game/FirstPerson/Lvl_FirstPerson              exists -> true
/Game/FirstPerson/MI_FirstPersonColorway       exists -> true
```

### Cross-check on `/Game/FirstPerson/`

`find_assets("/Game/FirstPerson", "", recursive=false)` returns exactly the two
single assets above:

```json
["/Game/FirstPerson/Lvl_FirstPerson", "/Game/FirstPerson/MI_FirstPersonColorway"]
```

`find_assets("/Game/FirstPerson", "", recursive=true)` returns **8** assets =
2 (root) + 4 (Blueprints) + 2 (Anims). The 2 under `Anims` are exactly the KEEP
LIST, and they are **not** in the delete set, because the delete set names
`/Game/FirstPerson/Blueprints/` and the two root files individually, never
`/Game/FirstPerson/` as a whole. **The keep list is honoured by construction,
not merely by exception.**

```json
"firstperson_anims": ["/Game/FirstPerson/Anims/CtrlRig_FPWarp",
                      "/Game/FirstPerson/Anims/ABP_FP_Copy"]
```

---

## 2. Referencer classification

`AssetTools.get_referencers` was called on **all 83** delete-set assets.

A referencer counts as INSIDE if it is itself in the delete set, or if it starts
with one of:

```
/Game/__ExternalActors__/Variant_Shooter/
/Game/__ExternalActors__/FirstPerson/
/Game/__ExternalObjects__/Variant_Shooter/
/Game/__ExternalObjects__/FirstPerson/
```

Anything else is OUTSIDE.

Raw result:

```json
{"delete_set_size": 83,
 "delete_set_unique": 83,
 "total_referencer_edges": 435,
 "external_prefix_referencer_edges": 293,
 "outside_count": 0,
 "outside_pairs": [],
 "assets_with_zero_referencers":
   ["/Game/Weapons/GrenadeLauncher/Audio/FirstPersonTemplateWeaponFire02"],
 "zero_ref_count": 1}
```

- 435 referencer edges in total across the 83 assets.
- 293 of those come from the four `__ExternalActors__` / `__ExternalObjects__`
  prefixes — per-actor external files belonging to `Lvl_ArenaShooter` and
  `Lvl_FirstPerson`, which are themselves in the delete set.
- The remaining 142 edges are delete-set assets referencing each other.
- Exactly one asset has no referencer at all:
  `/Game/Weapons/GrenadeLauncher/Audio/FirstPersonTemplateWeaponFire02`.

---

## 3. Outside referencers

**There are none.** `outside_count` is `0` and `outside_pairs` is `[]`.

Not a single asset in the delete set is referenced by anything outside the
delete set and outside the four listed external-file prefixes. Stated in the
requested pair form: the list of

```
<asset in delete set>  <-  <outside referencer>
```

pairs is **empty**.

### Independent verification from the opposite direction

`get_referencers` has already been shown to be unreliable on at least one path
in this project (section 5), so the conclusion was re-derived using
`get_dependencies`, which walks the graph the other way.

Every asset under `/Game/` that is **not** in the delete set and **not** under
any `__External*` path was enumerated — 193 assets — and `get_dependencies` was
called on each, checking whether any dependency lands in the delete set.

```json
{"outsiders": 193,
 "resolvable_scanned": 193,
 "unresolvable": [],
 "offender_count": 0,
 "offenders": []}
```

**Zero offenders.** All 193 resolved and were scanned; none depends on anything
in the delete set. The two directions agree.

Asset census for context:

| Bucket | Count |
|---|---|
| Total assets under `/Game/` | 296 |
| Delete set | 83 |
| Outsiders, excluding all `__External*` | 193 |
| Outsiders under `__External*` (all `ThirdPerson`) | 10 |
| | 83 + 193 + 10 = **286** |

The 10-asset gap from 296 is the `__External*` entries under the four
delete-set-adjacent prefixes, which classify as INSIDE.

**Caveat, stated plainly:** the 10 `__ExternalObjects__` entries under
`/Game/__ExternalObjects__/ThirdPerson/` could **not** be scanned. All 10 return
`false` from `exists` and raise `Asset does not exist` from
`get_dependencies` — they are registry entries for in-memory, never-saved
external objects belonging to `Lvl_Stage` and `Lvl_ThirdPerson`. Five belong to
`Lvl_Stage`, which is the level with 98 unsaved in-memory actors from this
session, so their being unwritten is expected. They are the one hole in the
otherwise complete reverse scan. Sample:

```
/Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/D/MP/1OU6UE00HRZKI42ATRN5WP
/Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/C/VN/7O6FXTR28IQ92JNY14ENUW
/Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/6/3J/M1ISS10UBLM1HT5YP1D74G
/Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/5/2N/FCVKIYP6OKL5TD4S33JRIO
/Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/1/2C/2CHLD5GCB4WLP4X15FK46A
/Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/0/TQ/1UP2MCOIYXC0GTW985R4K0
/Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/4/N4/1UVYQEVSONIYWETDLYKSAD
/Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/5/TX/O6OLZU4WSCI3YRJS922SWL
/Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/9/CJ/HU1I8LGRRCYOV9I0SJEY8V
/Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/E/2R/I7YTTKZX32ZUPSIFKIB1NS
```

The forward scan in section 2 does cover this hole from the other side: if any
of these referenced a delete-set asset, that asset's `get_referencers` would
have listed it as an OUTSIDE referencer, and none did.

---

## 4. KEEP LIST referencers, verbatim

### `/Game/FirstPerson/Anims/ABP_FP_Copy`

Class: `ABP_FP_Copy_C`

```json
["/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter",
 "/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter"]
```

**This is the reason the keep list exists.** Two referencers:

- `/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter` — **in the delete set.**
  Deleting it removes this referencer, which is fine.
- `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter` — **NOT in the delete
  set, and the live player character this whole session has been editing.**
  Deleting `ABP_FP_Copy` would break it.

### `/Game/FirstPerson/Anims/CtrlRig_FPWarp`

Class: `CtrlRig_FPWarp_C`

```json
["/Game/FirstPerson/Anims/ABP_FP_Copy"]
```

One referencer, the other keep-list asset. So the keep list is internally
closed: `BP_ThirdPersonCharacter` → `ABP_FP_Copy` → `CtrlRig_FPWarp`. Keeping
both is necessary and sufficient for that chain; keeping only `ABP_FP_Copy`
would break it.

---

## 5. `/Game/Weapons/Rifle/SM_Rifle` — the premise was wrong

The question states the disk has `Content/Weapons/Rifle/SM_Rifle.uasset` and
asks why `get_referencers` returned "Asset does not exist" for it.

**It returned that because the asset genuinely is not at that path.**

Reproduction of the reported error, verbatim:

```
AssetTools.get_referencers  asset_path = /Game/Weapons/Rifle/SM_Rifle
-> Asset does not exist: /Game/Weapons/Rifle/SM_Rifle
```

What `find_assets` actually returns under `/Game/Weapons/Rifle`, recursive:

```json
["/Game/Weapons/Rifle/Materials/M_Rifle",
 "/Game/Weapons/Rifle/Materials/M_Weapon",
 "/Game/Weapons/Rifle/Meshes/SK_Rifle",
 "/Game/Weapons/Rifle/Meshes/PA_Rifle",
 "/Game/Weapons/Rifle/Meshes/SKM_Rifle",
 "/Game/Weapons/Rifle/Meshes/SM_Rifle",
 "/Game/Weapons/Rifle/Textures/T_Rifle_BC",
 "/Game/Weapons/Rifle/Textures/T_Rifle_N"]
```

Non-recursive on the same folder returns `[]` — every asset sits in a
subfolder, none at the `Rifle/` root.

The listed path is `/Game/Weapons/Rifle/**Meshes**/SM_Rifle`. The path in the
question is missing the `Meshes/` segment.

Confirmed on disk with `find`:

```
./Rifle/Materials/M_Rifle.uasset
./Rifle/Meshes/PA_Rifle.uasset
./Rifle/Meshes/SKM_Rifle.uasset
./Rifle/Meshes/SK_Rifle.uasset
./Rifle/Meshes/SM_Rifle.uasset
./Rifle/Textures/T_Rifle_BC.uasset
./Rifle/Textures/T_Rifle_N.uasset
```

There is **no** `Content/Weapons/Rifle/SM_Rifle.uasset`. The only `SM_Rifle` on
disk is `Content/Weapons/Rifle/Meshes/SM_Rifle.uasset`.

The correct path resolves cleanly:

```json
{"path": "/Game/Weapons/Rifle/Meshes/SM_Rifle",
 "class": "StaticMesh",
 "referencers": ["/Game/Variant_Shooter/Blueprints/Pickups/DT_WeaponList"]}
```

One referencer, `DT_WeaponList`, which is itself in the delete set — so
`SM_Rifle` is INSIDE, consistent with section 3.

**This is not an MCP bug.** `find_assets`, `get_referencers`, `exists` and the
filesystem all agree with each other. The earlier "Asset does not exist" was a
correct answer to a wrong question. Recording this because the project's log
convention is to capture divergences — and the useful lesson here is the
inverse of the usual one: the tool was right and the remembered path was wrong,
so the path should be checked on disk before the tool is blamed.

### A real divergence, found while verifying the above

Separately and genuinely: `find_assets("/Game", recursive=true)` lists 10
`__ExternalObjects__` paths under `/Game/__ExternalObjects__/ThirdPerson/` that
`exists` reports as `false` and `get_dependencies` rejects with `Asset does not
exist`. The asset registry lists entries that have no file behind them. Details
and the full list are in section 3.

Operational note: that error is **not catchable** from inside an
`execute_tool_script` Python `try/except` — it aborts the whole script. Two
scripts in this command died that way before the loops were rewritten to
pre-filter with `exists`. Same behaviour was seen earlier in the session with
`create_node` on a non-existent type id.

---

## Verdict

The delete set of 83 assets can be deleted without breaking any asset outside
it, on the evidence gathered here — forward scan (`get_referencers` on all 83)
and reverse scan (`get_dependencies` on all 193 outsiders) both return zero
cross-boundary references.

Two qualifications on that verdict:

1. The 10 unresolvable `__ExternalObjects__` entries under `ThirdPerson/` could
   not be scanned in the reverse direction. The forward scan covers them.
2. `/Game/FirstPerson/Anims/` must be preserved. The delete set as specified
   already excludes it, but anyone widening the paths to `/Game/FirstPerson/`
   wholesale would take `ABP_FP_Copy` with it and break
   `BP_ThirdPersonCharacter`.

**Nothing was deleted. This was a dry run.**
