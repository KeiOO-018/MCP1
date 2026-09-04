# 2026-09-04-56 · BP_Torch CastShadow off (Backplate / Bracket / Cup)

Executed live through `unreal-mcp` (`http://127.0.0.1:8000/mcp`) from inside the UE Terminal
session. Every block below is the raw tool response, copied verbatim, in the order the calls
were made. Nothing has been reformatted or summarised.

Editor state at the time of the calls: `get_current_level` returned
`/Game/ThirdPerson/Lvl_Stage`, and no returned `refPath` carried a `UEDPIE_0_` prefix, so these
reads and writes hit the editor world, not a PIE world.

---

## 0 · Resolving the Blueprint's component templates

`editor_toolset.toolsets.actor.ActorTools.get_components` refuses the generated class directly:

```
call: editor_toolset.toolsets.actor.ActorTools.get_components
args: {"actor": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C"}}
```

```
Parameter error: /Game/Interaction/BP_Torch.BP_Torch_C is not valid Actor for property 'actor'.
```

An earlier attempt with the fully qualified tool name also failed, which is worth noting for
future sessions — `call_tool` wants the bare tool name plus a separate `toolset_name`:

```
call: editor_toolset.toolsets.actor.ActorTools.get_components (as tool_name)
```

```
Unknown tool editor_toolset.toolsets.actor.ActorTools.get_components
```

So the CDO was fetched first:

```
call: editor_toolset.toolsets.blueprint.BlueprintTools.get_default_object
args: {"blueprint": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch"}}
```

```
{"returnValue":{"refPath":"/Game/Interaction/BP_Torch.Default__BP_Torch_C"}}
```

```
call: editor_toolset.toolsets.actor.ActorTools.get_components
args: {"actor": {"refPath": "/Game/Interaction/BP_Torch.Default__BP_Torch_C"}}
```

```
{"returnValue":[{"refPath":"/Game/Interaction/BP_Torch.BP_Torch_C:Backplate_GEN_VARIABLE"},{"refPath":"/Game/Interaction/BP_Torch.BP_Torch_C:Bracket_GEN_VARIABLE"},{"refPath":"/Game/Interaction/BP_Torch.BP_Torch_C:Cup_GEN_VARIABLE"},{"refPath":"/Game/Interaction/BP_Torch.BP_Torch_C:Flame_GEN_VARIABLE"},{"refPath":"/Game/Interaction/BP_Torch.BP_Torch_C:Light_GEN_VARIABLE"},{"refPath":"/Game/Interaction/BP_Torch.BP_Torch_C:DefaultSceneRoot_GEN_VARIABLE"}]}
```

---

## 1 · CastShadow before the write (Blueprint component templates)

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Backplate_GEN_VARIABLE"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":true}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Bracket_GEN_VARIABLE"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":true}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Cup_GEN_VARIABLE"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":true}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Flame_GEN_VARIABLE"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

Flame was already `false` before this session touched anything. It was not written to.

---

## 2 · The write

```
call: editor_toolset.toolsets.object.ObjectTools.set_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Backplate_GEN_VARIABLE"}, "values": "{\"CastShadow\": false}"}
```

```
{"returnValue":true}
```

```
call: editor_toolset.toolsets.object.ObjectTools.set_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Bracket_GEN_VARIABLE"}, "values": "{\"CastShadow\": false}"}
```

```
{"returnValue":true}
```

```
call: editor_toolset.toolsets.object.ObjectTools.set_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Cup_GEN_VARIABLE"}, "values": "{\"CastShadow\": false}"}
```

```
{"returnValue":true}
```

`Flame_GEN_VARIABLE` and `Light_GEN_VARIABLE` received no `set_properties` call.

---

## 3 · Compile and save

```
call: editor_toolset.toolsets.blueprint.BlueprintTools.compile_blueprint
args: {"blueprint": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch"}}
```

```
{"returnValue":null}
```

`null`, not `true`. Per the standing note in this project, an `unreal-mcp` return value is not
evidence — `null` here is the tool's normal "no return value" for a void call, not a failure
signal, and it was checked against disk rather than believed.

```
call: editor_toolset.toolsets.asset.AssetTools.save_assets
args: {"asset_paths": ["/Game/Interaction/BP_Torch"]}
```

```
{"returnValue":true}
```

```
call: editor_toolset.toolsets.asset.AssetTools.is_dirty
args: {"asset_path": "/Game/Interaction/BP_Torch"}
```

```
{"returnValue":false}
```

Disk check (shell, outside MCP):

```
$ ls -l --time-style=full-iso "D:/20260827/MCP1/Content/Interaction/BP_Torch.uasset"; date
-rw-r--r-- 1 a0108 197609 35755 2026-09-04 10:19:53.426632100 +0900 D:/20260827/MCP1/Content/Interaction/BP_Torch.uasset
Fri Sep  4 10:19:59     2026
```

The `.uasset` mtime is six seconds before the `date` call, so the save genuinely reached disk.

---

## 4 · Read-back 1 — CastShadow on the Blueprint's component templates

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Backplate_GEN_VARIABLE"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Bracket_GEN_VARIABLE"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Cup_GEN_VARIABLE"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Flame_GEN_VARIABLE"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

| Blueprint component template | CastShadow |
| --- | --- |
| Backplate | false (changed by this session) |
| Bracket | false (changed by this session) |
| Cup | false (changed by this session) |
| Flame | false (already false; not written) |

The write landed on the class.

---

## 5 · How many BP_Torch actors exist in Lvl_Stage

```
call: editor_toolset.toolsets.scene.SceneTools.get_current_level
args: {}
```

```
{"returnValue":"/Game/ThirdPerson/Lvl_Stage"}
```

```
call: editor_toolset.toolsets.scene.SceneTools.find_actors
args: {"name": "", "tag": "", "collision_channels": [], "actor_type": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C"}}
```

```
{"returnValue":[{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1632447418"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1631447417"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1629798415"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1635118422"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1641174430"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1633477420"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1638841426"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1640173428"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1637113424"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1640188429"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1638113425"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1630779416"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1634114421"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1641842431"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1632782419"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1628783414"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1639178427"}]}
```

**18** BP_Torch actors, all in `PersistentLevel` of `/Game/ThirdPerson/Lvl_Stage`. None of the
paths carries a `UEDPIE_0_` prefix, so this is the editor world.

---

## 6 · Read-back 2 — CastShadow on ONE placed actor

Actor chosen: `BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423` (first entry returned by
`find_actors`).

```
call: editor_toolset.toolsets.actor.ActorTools.get_components
args: {"actor": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423"}}
```

```
{"returnValue":[{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.DefaultSceneRoot"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.BillboardComponent_0"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Backplate"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Bracket"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Cup"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Flame"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Light"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.BillboardComponent_1"}]}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Backplate"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":true}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Bracket"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":true}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Cup"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":true}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Flame"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

A second actor was sampled to check whether the first one was an outlier:

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1628783414.Backplate"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":true}"}
```

| Component on placed actor `..._1636115423` | Blueprint template | Placed instance |
| --- | --- | --- |
| Backplate | false | **true** |
| Bracket | false | **true** |
| Cup | false | **true** |
| Flame | false | false |

### This is the disagreement worth recording

The class default now says `false` and the placed actor still says `true`. The three components
were read **after** `compile_blueprint` and **after** the save that the disk mtime confirms, so
this is not a stale read of a pre-compile state.

The reading that fits: the placed instances carry a **per-instance override** of `CastShadow`,
serialised into the level actor when the torches were placed on 2026-09-03 while the class value
was still `true`. An overridden property on an instance does not follow a later change to the
class default — the same trap already recorded for this project as "BP variable default instance
trap". A second actor was checked and reads `true` as well, so this is not one stray instance;
the 18 placed torches most likely all hold the override.

**What was NOT confirmed:** only 2 of the 18 actors were read for Backplate, and only 1 of the 18
for Bracket / Cup / Flame. The remaining 16 are assumed, not verified. Nothing was done to clear
the overrides — `reset_properties` was not called on any actor, because this task asked for the
class change and a read-back, not for an instance fix.

---

## 7 · Read-back 3 — Light component on that same placed actor

The first attempt asked for both `CastShadows` and `CastShadow`, and the tool **errored out
entirely** rather than returning the properties it could read:

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Light"}, "properties": ["Intensity", "IntensityUnits", "AttenuationRadius", "LightColor", "CastShadows", "CastShadow", "SourceRadius", "Mobility"]}
```

```
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Light' (PointLightComponent): the following properties could not be read: CastShadow
```

A `PointLightComponent` has `CastShadows` (a `ULightComponentBase` property) and no `CastShadow`
— `CastShadow` is the `UPrimitiveComponent` property that the three static meshes use. One
unreadable name fails the whole call; the request had to be re-sent without it.

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Light"}, "properties": ["Intensity", "IntensityUnits", "AttenuationRadius", "LightColor", "CastShadows", "SourceRadius", "Mobility"]}
```

```
{"returnValue":"{\"Intensity\":5000,\"IntensityUnits\":\"Unitless\",\"AttenuationRadius\":1200,\"LightColor\":{\"r\":1,\"g\":0.66666668653488159,\"b\":0.35294118523597717,\"a\":1},\"CastShadows\":true,\"SourceRadius\":10,\"Mobility\":\"Movable\"}"}
```

| Light property (placed actor `..._1636115423`) | Value |
| --- | --- |
| Intensity | 5000 |
| IntensityUnits | Unitless |
| AttenuationRadius | 1200 |
| LightColor | r 1, g 0.66666668653488159, b 0.35294118523597717, a 1 |
| CastShadows | **true** |
| CastShadow | property does not exist on PointLightComponent (see error above) |
| SourceRadius | 10 |
| Mobility | Movable |

The same properties read off the Blueprint's Light template, to show the light was not touched:

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Light_GEN_VARIABLE"}, "properties": ["Intensity", "IntensityUnits", "AttenuationRadius", "LightColor", "CastShadows", "SourceRadius", "Mobility"]}
```

```
{"returnValue":"{\"Intensity\":5000,\"IntensityUnits\":\"Unitless\",\"AttenuationRadius\":1200,\"LightColor\":{\"r\":1,\"g\":0.66666668653488159,\"b\":0.35294118523597717,\"a\":1},\"CastShadows\":true,\"SourceRadius\":10,\"Mobility\":\"Movable\"}"}
```

Class and instance agree on every light value, and `CastShadows` is still `true`. The point light
keeps casting shadows, as required.

---

## 8 · What changed on disk

```
$ git status --short
 M Content/Interaction/BP_Torch.uasset
?? "Docs/Spec/2026-09-04-<Korean filename, shown as octal escapes by git>.md"
```

`Content/Interaction/BP_Torch.uasset` is the only asset this session modified. The untracked
`Docs/Spec/` file was already present before these calls and was not created here. No level
package and no `__ExternalActors__` file was written, which is consistent with nothing having
been changed on the placed actors.

---

## 9 · Open item

Turning off `CastShadow` on the class does **not**, on its own, stop the 18 placed torches from
casting mesh shadows, because each placed instance appears to hold its own `CastShadow = true`.
Clearing that would mean calling `ObjectTools.reset_properties` with `["CastShadow"]` on
Backplate / Bracket / Cup for each of the 18 actors, then saving the level. That was not done —
it is an 18-actor write to the level and was outside what this task asked for.
