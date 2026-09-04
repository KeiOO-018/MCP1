# 2026-09-04-58 · Lvl_Stage reloaded, torch CastShadow read back

**Result: the reload succeeded with no prompt and no dialog, and all twelve values now read
`false`. The placed torches do pick up the Blueprint class default once constructed fresh from
disk.**

Read-back only. No actor was written, the level was not saved, and `git status` at the end
confirms nothing under `Content/` changed. All tool responses below are verbatim, in call order,
including the warnings the reload produced.

---

## 0 · Log baseline before the reload

Taken so that any new map-load line afterwards could be attributed to this task:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "LoadMap|Bringing World|Editor autosave|Saving Package|World Composition", "maxEntries": 8}
```

```
{"returnValue":["[2026.09.04-01.12.39:421][714]LogWorld: Bringing World /Game/ThirdPerson/UEDPIE_0_Lvl_Stage.Lvl_Stage up for play (max tick rate 0) at 2026.09.04-10.12.39","[2026.09.04-01.19.53:404][463]LogFileHelpers: Saving Package: /Game/Interaction/BP_Torch","[2026.09.04-01.22.20:803][ 63]LogFileHelpers: Editor autosave (incl. external actors) for '/Game/ThirdPerson/Lvl_Stage' took 0.225","[2026.09.04-01.22.20:803][ 63]LogFileHelpers: Editor autosave (incl. sublevels & external actors) for all levels took 0.225"]}
```

The only map-load-ish line in the session so far was a PIE world bring-up at 01:12:39. No editor
map load had happened yet.

---

## STEP 1 · Reload

```
call: editor_toolset.toolsets.scene.SceneTools.load_level
args: {"level_path": "/Game/ThirdPerson/Lvl_Stage"}
```

```
{"returnValue":null}
```

`null` again — the tool declares no return value, so the response proves nothing on its own. The
first check for evidence looked in the wrong minute of the log and came back empty, which briefly
suggested the call had done nothing:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "(?i)loadmap|bringing world|took .* seconds to|discard|prompt|dialog", "maxEntries": 25}
```

That returned only startup-era `LogSlate` / `LogModuleManager` lines and the 01:12:39 PIE line —
nothing new. The reason was a misread clock, not a failed reload: the call actually landed at
**01:44:45**, and UE does not log the phrase "LoadMap" for an editor `MAP LOAD`. Confirming the
dispatch time first:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "LogModelContextProtocol", "pattern": "", "maxEntries": 14}
```

```
[2026.09.04-01.44.45:333][264]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.scene.SceneTools.load_level'
```

Then reading that window across all categories:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "01\\.4[4-9]\\.", "maxEntries": 60}
```

```
{"returnValue":["[2026.09.04-01.44.40:371][177]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-01.44.40:371][177]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.LogsToolset.GetLogEntries'","[2026.09.04-01.44.45:333][264]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-01.44.45:333][264]LogModelContextProtocol: Dispatching toolset tool: 'editor_toolset.toolsets.scene.SceneTools.load_level'","[2026.09.04-01.44.45:335][264]Cmd: MAP LOAD FILE=\"D:/20260827/MCP1/Content/ThirdPerson/Lvl_Stage.umap\" TEMPLATE=0 SHOWPROGRESS=1 FEATURELEVEL=4","[2026.09.04-01.44.45:410][264]LogWorld: UWorld::CleanupWorld for Lvl_Stage, bSessionEnded=true, bCleanupResources=true","[2026.09.04-01.44.45:411][264]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance","[2026.09.04-01.44.45:411][264]LogSlate: InvalidateAllWidgets triggered.  All widgets were invalidated","[2026.09.04-01.44.45:411][264]LogWorldPartition: UWorldPartition::Uninitialize : World = /Game/ThirdPerson/Lvl_Stage.Lvl_Stage","[2026.09.04-01.44.45:506][264]LogAudio: Display: Audio Device unregistered from world 'Lvl_Stage'.","[2026.09.04-01.44.45:513][264]LogUObjectHash: Compacting FUObjectHashTables data took   0.65ms","[2026.09.04-01.44.45:516][264]LogStreaming: Display: FlushAsyncLoading(482): 1 QueuedPackages, 0 AsyncPackages","[2026.09.04-01.44.45:530][264]LogAudio: Display: Audio Device (ID: 1) registered with world 'Lvl_Stage'.","[2026.09.04-01.44.45:530][264]LogChaosDD: Creating Chaos Debug Draw Scene for world Lvl_Stage","[2026.09.04-01.44.45:536][264]LogWorldPartition: ULevel::OnLevelLoaded(Lvl_Stage)(bIsOwningWorldGameWorld=0, bIsOwningWorldPartitioned=1, InitializeForMainWorld=1, InitializeForEditor=1, InitializeForGame=0)","[2026.09.04-01.44.45:537][264]LogWorldPartition: Display: WorldPartition initialize started...","[2026.09.04-01.44.45:537][264]LogWorldPartition: UWorldPartition::Initialize : World = /Game/ThirdPerson/Lvl_Stage.Lvl_Stage, World Type = Editor, IsMainWorldPartition = 1, Location = V(0), Rotation = R(0), IsEditor = 1, IsGame = 0, IsPIEWorldTravel = 0, IsCooking = 0","[2026.09.04-01.44.45:563][264]LogWorldPartition: Display: WorldPartition initialize took 26.556 ms (total: 2.62 sec)","[2026.09.04-01.44.45:615][264]LogEditorServer: Finished looking for orphan Actors (0.000 secs)","[2026.09.04-01.44.45:615][264]LogNavigation: Warning: Recreating dtNavMesh instance (RecastNavMesh_UAID_9C6B005AF86909FD02-Default) due mismatch in number of bytes required to store serialized maxTiles (serialized: 135, 8 bits) vs calculated required (120, 7 bits)","[2026.09.04-01.44.45:642][264]LogUObjectHash: Compacting FUObjectHashTables data took   0.46ms","[2026.09.04-01.44.45:715][264]Cmd: MAP CHECKDEP NOCLEARLOG","[2026.09.04-01.44.45:717][264]MapCheck: Map check complete: 0 Error(s), 0 Warning(s), took 0.81ms to complete.","[2026.09.04-01.44.49:723][277]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-01.44.49:723][277]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.LogsToolset.GetLogEntries'","[2026.09.04-01.44.57:056][299]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-01.44.49:723][277]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.LogsToolset.GetLogEntries'","[2026.09.04-01.45.08:389][333]LogModelContextProtocol: Running tool: 'call_tool'","[2026.09.04-01.45.08:389][333]LogModelContextProtocol: Dispatching toolset tool: 'EditorToolset.LogsToolset.GetLogEntries'"]}
```

The reload is unambiguous in that block:

| Line | What it shows |
| --- | --- |
| `Cmd: MAP LOAD FILE="D:/20260827/MCP1/Content/ThirdPerson/Lvl_Stage.umap"` | the map was loaded from the `.umap` on disk |
| `UWorld::CleanupWorld for Lvl_Stage, bSessionEnded=true, bCleanupResources=true` | the old world was torn down |
| `UWorldPartition::Uninitialize` then `UWorldPartition::Initialize` | World Partition cycled |
| `ULevel::OnLevelLoaded(Lvl_Stage)` | the level came back up |
| `MapCheck: Map check complete: 0 Error(s), 0 Warning(s)` | clean load |

**No save prompt, no modal dialog, no error.** There is no
`LogFileHelpers: InternalPromptForCheckoutAndSave` line in the reload window — the last one in
the whole session is still the 01:19:53 one from the BP_Torch save two tasks ago. The 18 dirty
`__ExternalActors__` packages were discarded silently, as intended.

**Two warnings the reload did produce**, recorded rather than dropped:

```
[2026.09.04-01.44.45:411][264]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
[2026.09.04-01.44.45:615][264]LogNavigation: Warning: Recreating dtNavMesh instance (RecastNavMesh_UAID_9C6B005AF86909FD02-Default) due mismatch in number of bytes required to store serialized maxTiles (serialized: 135, 8 bits) vs calculated required (120, 7 bits)
```

Both are navmesh warnings, unrelated to torches or shadows. The navmesh one says the serialized
tile count in the level does not match what the current settings compute, so the editor rebuilt
the dtNavMesh in memory. Noting it because it is the kind of thing that dirties a package on its
own; see STEP 4.

---

## STEP 2 · BP_Torch actors after the reload

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
{"returnValue":[{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1632447418"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1631447417"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1629798415"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1635118422"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1641174430"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1633477420"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1638841426"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1640173428"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1637113424"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1640188429"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1638113425"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1630779416"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1634114421"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1641842431"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1632782419"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1628783414"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1639178427"},{"refPath":"/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423"}]}
```

**18 BP_Torch actors** — the same count as before the reload, and the same 18 UAIDs. The list
order changed (`..._1636115423` was first before the reload and is last now), which is expected
when the level is rebuilt from disk.

---

## STEP 3 · CastShadow on three different torch actors

Actors chosen: `..._1636115423` and `..._1628783414` (the two read before the reload, so the
before/after comparison is on the same objects) and `..._1632447418` (a third, not read before).

### Actor `..._1636115423`

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Backplate"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Bracket"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Cup"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Flame"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

### Actor `..._1628783414`

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1628783414.Backplate"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1628783414.Bracket"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1628783414.Cup"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1628783414.Flame"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

### Actor `..._1632447418`

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1632447418.Backplate"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1632447418.Bracket"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1632447418.Cup"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1632447418.Flame"}, "properties": ["CastShadow"]}
```

```
{"returnValue":"{\"CastShadow\":false}"}
```

### All twelve values

| Actor | Backplate | Bracket | Cup | Flame |
| --- | --- | --- | --- | --- |
| `..._1636115423` | false | false | false | false |
| `..._1628783414` | false | false | false | false |
| `..._1632447418` | false | false | false | false |

**Twelve of twelve `false`.** Nothing read `true`. Backplate, Bracket and Cup now match the
Blueprint class default, and Flame is unchanged at `false` as it always was.

### What this corrects from the previous log

Log 2026-09-04-56 recorded these components reading `true` on the placed actors after the compile
and save, and read that as a per-instance override serialised into the level. **That reading was
wrong.** There was no override in the actor packages — the values on disk were already deferring
to the class default, and a fresh load proves it. What the earlier reads saw was the in-memory
state of actors that the reinstancer had rebuilt but had not repopulated with the new class
default, which is exactly the state that also left those 18 packages dirty. The dirty flags and
the stale `true` values were two symptoms of one thing, not two separate problems.

Concretely: `compile_blueprint` through MCP changes the class, but the already-instanced editor
actors are not reliably brought up to date by it. A level reload is what makes them agree.

---

## STEP 4 · Is anything dirty after the reload

Three separate checks, and one of them is weaker than it looks.

**a. Enumerate and test every addressable `/Game` asset.** Same method as the previous task
(`AssetTools.is_dirty` is still the only dirty query `unreal-mcp` exposes, one path at a time):

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: for a in find_assets("/Game", "") if "__External" not in a: is_dirty(a)
```

```
{"total_found": 207, "skipped_external": 10, "scanned": 197, "dirty": [], "elapsed_sec": 18.74}
```

197 of 197 not dirty. The 10 `__ExternalObjects__` paths are skipped because `is_dirty` errors on
them (`Asset does not exist`), unchanged from last task.

**b. The level package on its own.**

```
call: editor_toolset.toolsets.asset.AssetTools.is_dirty
args: {"asset_path": "/Game/ThirdPerson/Lvl_Stage"}
```

```
{"returnValue":false}
```

**c. The autosave witness — and why it does not count yet.** Last task the 18 dirty external
actor packages were found only because autosave had fired and named them in the log, since
`is_dirty` cannot address `__ExternalActors__` paths at all. Checking for a new autosave:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "LogFileHelpers", "pattern": "", "maxEntries": 20}
```

```
{"returnValue":["[2026.09.04-01.19.53:350][463]LogFileHelpers: InternalPromptForCheckoutAndSave started...","[2026.09.04-01.19.53:404][463]LogFileHelpers: Saving Package: /Game/Interaction/BP_Torch","[2026.09.04-01.22.20:803][ 63]LogFileHelpers: Editor autosave (incl. external actors) for '/Game/ThirdPerson/Lvl_Stage' took 0.225","[2026.09.04-01.22.20:803][ 63]LogFileHelpers: Editor autosave (incl. sublevels & external actors) for all levels took 0.225"]}
```

No new autosave. **But the reload was at 01:44:45 and the last MCP call in this task was at about
01:47, so barely two minutes have passed — autosave has not had the chance to fire.** Its silence
is not yet evidence of anything. This is the honest limit of the check: the 113
`__ExternalActors__` packages of this level remain unqueryable by any tool available here, and the
one indirect witness has not reported in yet.

**d. Disk.** Nothing was written:

```
$ git status --short
 M Content/Interaction/BP_Torch.uasset
?? "Docs/Spec/2026-09-04-<Korean filename, shown as octal escapes by git>.md"
?? Docs/Terminal-Log/2026-09-04-56-torch-cast-shadow-off.md
?? Docs/Terminal-Log/2026-09-04-57-torch-shadow-after-reload.md

$ git status --short -- Content/__ExternalActors__
(no output)
```

The only modified asset is still `BP_Torch.uasset` from task 56. The two untracked files are the
previous logs. Nothing under `Content/__ExternalActors__` changed, which is what a read-only task
should look like.

### Answer

By everything that can be measured: **no package is dirty after the reload.** 197 `/Game` assets
clean, level package clean, disk untouched. The unmeasured part is the level's 113
`__ExternalActors__` packages, and the navmesh warning in section STEP 1 is a reason not to
assume too hard — `Recreating dtNavMesh instance` is the kind of load-time fixup that can mark a
package dirty. If a `LogFileHelpers: Editor autosave (incl. external actors)` line appears later
in this editor session without anyone having edited the level, that is what it will mean.

---

## What was not done

No `set_properties`, no `reset_properties`, no `save_assets`, no `save_actor`. Every call in this
task other than `load_level` is a read, and `load_level` wrote nothing to disk.

Fifteen of the eighteen torch actors were not read; three were, as asked. The class-default fix
is confirmed on those three and is expected to hold for the rest, but that is not verified here.
