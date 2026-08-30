# 2026-08-30 — Q (drop item) spawn: BLOCKED, nothing built

**No nodes were created. The EventGraph is byte-for-byte as the previous command left it.**

Nodes 24 (`BeginDeferredActorSpawnFromClass`) and 27 (`FinishSpawningActor`) cannot be created
through this MCP server. They are marked `BlueprintInternalUseOnly = "true"` in the engine
source, which removes them from the node palette that `create_node` resolves against. Without
those two, nodes 26 and 28/29 must not be built either — see section 4 for why building the
buildable remainder would have been worse than building nothing.

---

## 1. Dirty check before any work

`AssetTools.is_dirty` on `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`, called before
anything else in this command:

```
{"returnValue":false}
```

**Not dirty.** Same as the previous command. The pre-existing-unsaved-change problem from
command 24 has not recurred.

Re-checked at the end of this command, after the six failed create attempts:

```
{"returnValue":false}
```

Still clean. The failures did not dirty the asset, so there was nothing to save and
`save_assets` was not called.

---

## 2. Nodes created

**None.** There is no table to fill in here.

The six `create_node` calls that were attempted all failed; their exact error text is in
section 6. No node was created by any of them, verified by node count in section 5.

---

## 3. Input pins of nodes 21–29

**Not applicable — no node 21–29 exists.**

---

## 4. Why the whole chain was stopped, not just nodes 24 and 27

### 4.1 What the registry does and does not have

`find_node_types` was run for every node on the list. Results:

| # | requested | found in registry | verdict |
|---|---|---|---|
| 21 | Break Hit Result | `Collision\|BreakHitResult` | creatable |
| 22 | `Math\|Vector\|vector+vector` | `Utilities\|Operators\|Add` (promotable) | creatable |
| 23 | Make Transform | `Math\|Transform\|MakeTransform` | creatable |
| 24 | `BeginDeferredActorSpawnFromClass` | **nothing** | **BLOCKED** |
| 25 | Make DataTableRowHandle | `Utilities\|Struct\|MakeDataTableRowHandle` | creatable |
| 26 | Set ItemRow on another object | `Class\|BPItemPickup\|SetItemRow` | creatable |
| 27 | `FinishSpawningActor` | **nothing** | **BLOCKED** |
| 28 | `Utilities\|Array\|SetArrayElem` | `Utilities\|Array\|SetArrayElem` | creatable |
| 29 | `\|RefreshHeldItem` | `CallFunction\|RefreshHeldItem` | creatable |

Worth noting for whoever picks this up: **node 26 exists and is exactly what was asked for.**
`Class|BPItemPickup|SetItemRow` is a set-node for another object's variable, with its own
target pin — no workaround needed. It is only unusable here because nothing can produce the
deferred actor to feed its target.

Searches for `Deferred`, `FinishSpawning`, `Finish` and `Spawn` turned up no deferred-spawn
node of any kind. The only actor-spawn node in the palette is `Game|SpawnActorfromClass` — the
plain, non-deferred one.

### 4.2 Why they are missing — engine source

From `C:\Program Files\Epic Games\UE_5.8\Engine\Source\Runtime\Engine\Classes\Kismet\GameplayStatics.h`,
lines 65–71:

```cpp
	/** Spawns an instance of an actor class, but does not automatically run its construction script.  */
	UFUNCTION(BlueprintCallable, Category = "Spawning", meta = (WorldContext = "WorldContextObject", UnsafeDuringActorConstruction = "true", BlueprintInternalUseOnly = "true"))
	static ENGINE_API class AActor* BeginDeferredActorSpawnFromClass(const UObject* WorldContextObject, TSubclassOf<AActor> ActorClass, const FTransform& SpawnTransform, ESpawnActorCollisionHandlingMethod CollisionHandlingOverride = ESpawnActorCollisionHandlingMethod::Undefined, AActor* Owner = nullptr, ESpawnActorScaleMethod TransformScaleMethod = ESpawnActorScaleMethod::MultiplyWithRoot);

	/** 'Finish' spawning an actor.  This will run the construction script. */
	UFUNCTION(BlueprintCallable, Category="Spawning", meta=(UnsafeDuringActorConstruction = "true", BlueprintInternalUseOnly = "true"))
	static ENGINE_API class AActor* FinishSpawningActor(class AActor* Actor, const FTransform& SpawnTransform, ESpawnActorScaleMethod TransformScaleMethod = ESpawnActorScaleMethod::MultiplyWithRoot);
```

Both carry `BlueprintInternalUseOnly = "true"`. That flag keeps a function out of the Blueprint
action palette. These two are not meant to be placed by hand at all — in stock UE the
`K2Node_SpawnActorFromClass` node *expands into* this pair at compile time, setting the
exposed-on-spawn pins in between. There is no user-facing "SpawnActorDeferred" node in
Blueprint; the deferred sequence is the compiler's internal expansion of the ordinary
SpawnActor node.

So the absence is by engine design, not an `unreal-mcp` gap. `find_node_types` is reporting
the palette correctly.

### 4.3 Confirmed by direct create attempts

Six `create_node` calls were made anyway, on the chance that `create_node` resolves against a
wider set than `find_node_types` reports. All six failed. Exact text in section 6.

### 4.4 Why nodes 21, 22, 23, 25, 28, 29 were not built either

They are creatable, and the instinct is to build what can be built. That would have been the
wrong call here:

- **28 and 29 are destructive without the spawn.** `SetArrayElem` writes an empty Name into
  `InventorySlots[SelectedSlot - 1]`, and `RefreshHeldItem` then redraws. Wired to
  `K2Node_IfThenElse_6 . then` without a spawn in front of them, pressing Q on a valid slot
  over valid ground would **delete the held item and drop nothing.** The command's own stated
  ordering rule — "the actor is spawned and finished BEFORE the slot is cleared, so a failed
  spawn cannot empty the slot" — is exactly the guarantee that partial build would break, and
  it would break it in the compiled, saved, playable Blueprint.
- **21, 22, 23, 25 alone deliver nothing.** They are pure nodes. Built and left unconnected to
  any exec chain they would compute nothing, change no behaviour, and just leave six orphans
  in the graph for the next session to puzzle over or clean up.

Leaving the graph untouched keeps `K2Node_IfThenElse_6 . then` open as a clean attachment
point and keeps the Q chain in its current honest state: it traces, it draws the debug line,
and it prints CANNOT DROP HERE on a miss. On a hit it currently does nothing, which is
incomplete but not wrong.

### 4.5 Routes that were checked and do not work

- **Plain `Game|SpawnActorfromClass` + `Class|BPItemPickup|SetItemRow` afterwards.** This is
  the obvious fallback and it defeats the purpose. `BP_ItemPickup`'s ConstructionScript builds
  the mesh from `ItemRow`, and it runs *during* SpawnActor — before the Set could execute. The
  dropped item would spawn with whatever mesh an empty row produces. This is precisely the
  failure the command's deferred approach was written to avoid, so it was not substituted in
  silently.
- **Spawn plain, set ItemRow, then re-run the construction script.** `RerunConstructionScripts`
  is not in the palette either; a search for `ConstructionScript` returned only three unrelated
  Spline entries (`Spline|SetOverrideConstructionScript`,
  `Class|SplineComponent|GetInputSplinePointstoConstructionScript`,
  `Class|SplineComponent|SetInputSplinePointstoConstructionScript`).
- **Exposing `ItemRow` on spawn so a plain SpawnActor gets the pin.** Still blocked from
  command 23: this server has no tool that can read or write a Blueprint variable's
  Expose on Spawn or Instance Editable. See `2026-08-30-23-drop-item-prep.md` section 3.

---

## 5. EventGraph node count

From the length of a `find_nodes` result (graph = EventGraph, `title` = `""`):

- **Before:** 91
- **After the six failed create attempts:** 91
- **After (end of command):** 91

Unchanged. The failed calls left no partial nodes behind — this mattered to check, because in
command 24 a script that failed midway had already created the nodes before the failing one.

### The three reuse nodes gained no consumers

They were read before the work and again at the end. Nothing was connected to them, so nothing
changed:

| node | consumers (unchanged) |
|---|---|
| `K2Node_GetArrayItem_1` out 0 | `K2Node_PromotableOperator_11[in 0]` — 1 consumer |
| `K2Node_VariableGet_1` out 0 | `K2Node_CallArrayFunction_4[in 0]`, `K2Node_GetArrayItem_1[in 0]` — 2 consumers |
| `K2Node_PromotableOperator_8` out 0 | `K2Node_PromotableOperator_9[in 0]`, `K2Node_PromotableOperator_10[in 0]`, `K2Node_GetArrayItem_1[in 1]` — 3 consumers |

The command asked for read-back confirmation that each gained exactly one new consumer. **They
gained none**, because nothing was built to consume them.

### The attach points are still open

Read back at the end of the command:

```
K2Node_IfThenElse_6: [{"n": "then", "to": []}, {"n": "else", "to": ["K2Node_CallFunction_8"]}]
K2Node_CallFunction_7: [{"n": "then", "to": ["K2Node_IfThenElse_6"]}, {"n": "OutHit", "to": []}, {"n": "ReturnValue", "to": ["K2Node_IfThenElse_6"]}]
```

`K2Node_IfThenElse_6 . then` is still unconnected, and `K2Node_CallFunction_7 . OutHit` — which
node 21 was to break — is still unconnected. Both remain available.

---

## 6. Errors and warnings — exact English text

All six `create_node` attempts for the two blocked nodes, verbatim:

```
The node could not be created / Spawning|BeginDeferredActorSpawnFromClass does not exist
The node could not be created / CallFunction|BeginDeferredActorSpawnFromClass does not exist
The node could not be created / BeginDeferredActorSpawnFromClass does not exist
The node could not be created / Spawning|FinishSpawningActor does not exist
The node could not be created / CallFunction|FinishSpawningActor does not exist
The node could not be created / FinishSpawningActor does not exist
```

No other tool call in this command produced an error or a warning. No new `LogBlueprint` entries
were generated, because no Blueprint modification and no compile took place.

---

## 7. Compile result

**Not compiled.** Nothing in the Blueprint was changed, so `compile_blueprint` was deliberately
not called — compiling and saving an unmodified Blueprint would dirty
`Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset` in git for no change, exactly
as was avoided in command 23 for BP_ItemPickup.

`AssetTools.is_dirty` reads `false` at the end of the command. `save_assets` was not called.

---

## 8. Nodes created that were not on the list

**None.** Nothing was created at all.

For contrast, the previous command did add one node beyond its list — the `MakeLiteralFloat`
feeding node 15's `B` pin — and that is documented in
`2026-08-30-25-drop-item-trace.md` section 4. Nothing comparable happened here.

---

## 9. git status

```
 M Content/Input/IMC_Inventory.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
?? Content/Input/Actions/IA_DropItem.uasset
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/2/9H/
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/2/LI/
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/8/WQ/
?? "Docs/2026-08-29-중간점검.md"
?? Docs/Terminal-Log/2026-08-30-23-drop-item-prep.md
?? Docs/Terminal-Log/2026-08-30-24-drop-item-gate.md
?? Docs/Terminal-Log/2026-08-30-25-drop-item-trace.md
```

`BP_ThirdPersonCharacter.uasset` shows modified from the **previous** command's saved work, not
from this one. This command wrote nothing to disk except this report.

---

## 10. What this needs next — a decision, not another command

The deferred-spawn approach cannot be built through `unreal-mcp`. Three ways forward; the
choice is the user's:

1. **Do the spawn by hand in the editor.** Open BP_ThirdPersonCharacter, drag from
   `K2Node_IfThenElse_6 . then`, and build the SpawnActor chain in the graph editor. The
   editor's own SpawnActor node handles the deferred expansion internally, which is the
   supported way to do this. Everything else on the list — 21, 22, 23, 25, 28, 29 — could then
   still be built by MCP around it, or by hand at the same time.

2. **Turn on Expose on Spawn for `ItemRow` by hand, then use plain SpawnActor via MCP.** Open
   BP_ItemPickup, tick Instance Editable and Expose on Spawn on `ItemRow`, compile, save. Then
   `Game|SpawnActorfromClass` gains an `ItemRow` pin and the whole rest of the chain is
   buildable by MCP with no deferred nodes at all — nodes 24, 26 and 27 collapse into one
   SpawnActor node. This is the smallest hand-edit that unblocks full automation, and it is
   the same flag command 23 already flagged as unreachable.

3. **Accept the mesh being built from an empty row.** Plain SpawnActor, then
   `Class|BPItemPickup|SetItemRow` after. Fully buildable by MCP right now, but the dropped
   item's ConstructionScript runs before `ItemRow` is set, so the mesh will be wrong unless
   BP_ItemPickup rebuilds it somewhere outside the ConstructionScript. That was not checked.

Option 2 looks like the best trade — one checkbox by hand, everything else automatable — but it
depends on whether `ItemRow` is currently Instance Editable, which still cannot be read.

**Not verified:** whether BP_ItemPickup rebuilds its mesh anywhere other than the
ConstructionScript. If it does, option 3 becomes viable. Its graphs were not read in this
command.
