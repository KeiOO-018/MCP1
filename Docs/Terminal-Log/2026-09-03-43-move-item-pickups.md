# 2026-09-03 · Command 43 — Move BP_ItemPickup and BP_ItemPickup2

Level change only, in `/Game/ThirdPerson/Lvl_Stage`. Two existing actors moved.
**No Blueprint was edited. No actor was created or deleted. Nothing was saved.**

Instruction, verbatim from the user:

> Move two existing actors. Match their editor labels exactly.
> Change only the location. Do not change rotation or scale.
> Do not use snap_to_ground.
>
>     label "BP_ItemPickup"    from (170, -430, 20)   to (-600, -430, 20)
>     label "BP_ItemPickup2"   from (-160, -440, 20)  to (-900, -440, 20)
>
> Be careful: "BP_ItemPickup" is a prefix of "BP_ItemPickup2".
> Match the whole label, not a prefix.

**Headline: both actors moved to the exact target locations. Rotation and scale
verified byte-identical to their previous values. The prefix hazard was handled
by exact dictionary lookup, and both labels resolved to exactly one actor each.
Actor count unchanged at 98.**

---

## Pre-flight

### P1 — `SceneTools.get_current_level`

```json
{"returnValue":"/Game/ThirdPerson/Lvl_Stage"}
```

**PASS.** The level guard is also built into both scripts: each aborts with
`{"aborted": "wrong level"}` if `get_current_level` is not
`/Game/ThirdPerson/Lvl_Stage`. It never fired.

### P2 — Identify the actors, and prove the prefix hazard was handled

`SceneTools.find_actors` with empty `name`, empty `tag`, empty
`collision_channels` — 98 actors. `ActorTools.get_label` on each, results
collected into a `label -> [actors]` dictionary. Matching is an **exact
dictionary key lookup** (`by_label.get("BP_ItemPickup")`), never a substring or
`startswith` test.

Every actor whose label contains "pickup", with class and transform:

```json
[
 {"label": "Knife_Pickup",
  "internal": "BP_ItemPickup_C_UAID_9C6B005AF86987FD02_2109068423",
  "class": "/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C",
  "xform": {"location": {"x": 300, "y": 0, "z": 20},
            "rotation": {"pitch": 0, "yaw": 0, "roll": 0},
            "scale": {"x": 1, "y": 1, "z": 1}}},
 {"label": "BP_ItemPickup2",
  "internal": "BP_ItemPickup_C_UAID_9C6B005AF86927FE02_1885181622",
  "class": "/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C",
  "xform": {"location": {"x": -160, "y": -440, "z": 20},
            "rotation": {"pitch": 0, "yaw": 0, "roll": 0},
            "scale": {"x": 1, "y": 1, "z": 1}}},
 {"label": "BP_ItemPickup",
  "internal": "BP_ItemPickup_C_UAID_9C6B005AF86927FE02_1872193621",
  "class": "/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C",
  "xform": {"location": {"x": 170, "y": -430, "z": 20},
            "rotation": {"pitch": 0, "yaw": 0, "roll": 0},
            "scale": {"x": 1, "y": 1, "z": 1}}}
]
```

Exact-match counts:

```json
{"exact_match_count__BP_ItemPickup": 1,
 "exact_match_count__BP_ItemPickup2": 1}
```

**PASS**, on four separate grounds:

1. Each label resolved to **exactly one** actor. If either had resolved to zero
   or more than one, the script would have added it to `skipped` and made no
   write. `skipped` came back empty.
2. The two actors have **different internal names** — `..._1872193621` and
   `..._1885181622` — so they are genuinely distinct objects, not one actor
   reached twice.
3. Both starting transforms matched the "from" values the user supplied
   exactly: `(170, -430, 20)` and `(-160, -440, 20)`. This independently
   confirms the right pair was grabbed.
4. A **third** actor of the same Blueprint class exists in the level —
   `Knife_Pickup` at `(300, 0, 20)`. A prefix or substring match on
   "BP_ItemPickup" would not have caught it (its label does not start with that
   string), but it is recorded here because it is the same class and would be a
   plausible mis-grab under a class-based rather than label-based search. It was
   not touched.

---

## The write

`ActorTools.set_actor_transform`, `worldspace: true`, once per actor.

**How rotation and scale were preserved.** The `ToolsetTransform` schema
documents unset fields as "don't change" when modifying an existing object, but
that behaviour was not relied on. For each actor the current transform was read
with `get_actor_transform` first, and the **exact returned rotation and scale
objects were sent back** alongside the new location. "Unchanged" is therefore
verified by comparison, not assumed from omission:

```python
old = get_xform(a)
xform = {"location": {"x": loc[0], "y": loc[1], "z": loc[2]},
         "rotation": old["rotation"],
         "scale":    old["scale"]}
set_xform(a, xform)
```

`snap_to_ground` does not exist on `set_actor_transform` — it is an
`add_to_scene_from_asset` parameter only — so there was nothing to disable. No
actor was added this command.

Both calls returned:

```json
{"returnValue": true}
```

---

## Verification

Raw return value of the whole script:

```json
{"count_before": 98, "count_after": 98, "modified": 2, "skipped": [],
 "all_loc_ok": true, "all_rot_unchanged": true, "all_scale_unchanged": true,
 "rows": [
  {"label": "BP_ItemPickup",
   "internal": "BP_ItemPickup_C_UAID_9C6B005AF86927FE02_1872193621",
   "class": "/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C",
   "set_returned": true,
   "old_xform": {"location": {"x": 170, "y": -430, "z": 20},
                 "rotation": {"pitch": 0, "yaw": 0, "roll": 0},
                 "scale": {"x": 1, "y": 1, "z": 1}},
   "new_xform": {"location": {"x": -600, "y": -430, "z": 20},
                 "rotation": {"pitch": 0, "yaw": 0, "roll": 0},
                 "scale": {"x": 1, "y": 1, "z": 1}},
   "bounds": {"min": {"x": -650, "y": -480, "z": -30},
              "max": {"x": -550, "y": -380, "z": 70}, "isValid": true},
   "loc_ok": true, "rot_unchanged": true, "scale_unchanged": true},
  {"label": "BP_ItemPickup2",
   "internal": "BP_ItemPickup_C_UAID_9C6B005AF86927FE02_1885181622",
   "class": "/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C",
   "set_returned": true,
   "old_xform": {"location": {"x": -160, "y": -440, "z": 20},
                 "rotation": {"pitch": 0, "yaw": 0, "roll": 0},
                 "scale": {"x": 1, "y": 1, "z": 1}},
   "new_xform": {"location": {"x": -900, "y": -440, "z": 20},
                 "rotation": {"pitch": 0, "yaw": 0, "roll": 0},
                 "scale": {"x": 1, "y": 1, "z": 1}},
   "bounds": {"min": {"x": -950, "y": -490, "z": -30},
              "max": {"x": -850, "y": -390, "z": 70}, "isValid": true},
   "loc_ok": true, "rot_unchanged": true, "scale_unchanged": true}
 ]}
```

### V1 — BP_ItemPickup

| Field | Value |
|---|---|
| Editor label | `BP_ItemPickup` |
| Internal name | `BP_ItemPickup_C_UAID_9C6B005AF86927FE02_1872193621` |
| Class | `/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C` |
| Location | `(-600, -430, 20)` |
| Rotation | `(0, 0, 0)` |
| Scale | `(1, 1, 1)` |
| Bounds min | `(-650, -480, -30)` |
| Bounds max | `(-550, -380, 70)` |
| Previous location | `(170, -430, 20)` |

**PASS.** Location exact — all three components integer-equal to the target, no
float residue. Rotation and scale compare equal to the pre-write values. Moved
770 units in −X; Y and Z unchanged, matching the instruction, which only altered
X for this actor.

### V2 — BP_ItemPickup2

| Field | Value |
|---|---|
| Editor label | `BP_ItemPickup2` |
| Internal name | `BP_ItemPickup_C_UAID_9C6B005AF86927FE02_1885181622` |
| Class | `/Game/Inventory/BP_ItemPickup.BP_ItemPickup_C` |
| Location | `(-900, -440, 20)` |
| Rotation | `(0, 0, 0)` |
| Scale | `(1, 1, 1)` |
| Bounds min | `(-950, -490, -30)` |
| Bounds max | `(-850, -390, 70)` |
| Previous location | `(-160, -440, 20)` |

**PASS.** Location exact. Rotation and scale compare equal to the pre-write
values. Moved 740 units in −X; Y and Z unchanged.

### V3 — Nothing else changed

`count_before` 98, `count_after` 98. No actor created, none deleted. `skipped`
empty, `modified` 2 — the script wrote to exactly two actors and no others. The
aggregate flags `all_loc_ok`, `all_rot_unchanged` and `all_scale_unchanged` are
all `true`.

Bounds sanity: each actor's bounding box is a 100 x 100 x 100 box centred on its
location, consistent with the unchanged scale of `(1, 1, 1)`. The box extends 50
below the actor origin (Z −30 for an origin at Z 20), which matches the other
`BP_ItemPickup` instances observed earlier in the session.

---

## Not saved

`AssetTools.save_assets` was **not** called. The level is dirty in memory only.

`Lvl_Stage.umap` on disk is still the original 50-actor duplicate made at the
start of the session. The level currently holds **98 actors in memory**, all of
which — including these two moves — are lost if the editor closes without
saving. This is by instruction ("Do not save"), not an oversight.

PIE was not run.

---

## Why this report is a file

The user's next message came back as a **truncated fragment of the previous
report**, cut off mid-sentence at "A third". That is precisely the failure mode
CLAUDE.md describes: screen output is clipped at terminal width and the clipped
fragment then masquerades as the original. This report is written to a repo path
so the full text survives.
