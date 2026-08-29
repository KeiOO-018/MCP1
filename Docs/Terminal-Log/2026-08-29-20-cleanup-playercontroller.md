# Remove the dead HUD branch and collapse the Sequence - BP_ThirdPersonPlayerController

Date: 2026-08-29
Blueprint: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController`
Graph: `BP_ThirdPersonPlayerController:EventGraph`

All node/pin facts below were read back with
`editor_toolset.toolsets.blueprint.BlueprintTools.get_node_infos`. The "before" shape was
read back BEFORE anything was deleted; everything else was read back AFTER the compile and
save. None of them come from the return value of a write call.

---

## 1. Shape found before deleting anything

Read back with `get_node_infos` as the first action of this command, before any write:

```
NODE K2Node_EnhancedInputAction_0 [Input|EnhancedActionEvents|EnhancedInputActionIA_SelectSlot] pos=-704,500
  OUT 0 Triggered (Exec) -> ['K2Node_ExecutionSequence_0.in0']
  OUT 1 Started (Exec) -> <none>
  OUT 2 Ongoing (Exec) -> <none>
  OUT 3 Canceled (Exec) -> <none>
  OUT 4 Completed (Exec) -> <none>
  OUT 5 ActionValue (Float (double-precision)) -> ['K2Node_CallFunction_47.in0']
  OUT 6 ElapsedSeconds (Float (double-precision)) -> <none>
  OUT 7 TriggeredSeconds (Float (double-precision)) -> <none>
  OUT 8 InputAction (Input Action Object Reference) -> <none>
NODE K2Node_ExecutionSequence_0 [Utilities|FlowControl|Sequence] pos=-540,500
  IN  0 execute (Exec) <- ['K2Node_EnhancedInputAction_0.out0'] | val=
  OUT 0 then_0 (Exec) -> ['K2Node_DynamicCast_2.in0']
  OUT 1 then_1 (Exec) -> ['K2Node_DynamicCast_0.in0']
NODE K2Node_CallFunction_46 [HUD|GetHUD] pos=-704,648
  IN  0 self (Player Controller Object Reference) <- <none> | val=
  OUT 0 ReturnValue (HUD Object Reference) -> ['K2Node_DynamicCast_2.in1']
NODE K2Node_DynamicCast_2 [Utilities|Casting|CastToBP_ThirdPersonHUD] pos=-354,574
  IN  0 execute (Exec) <- ['K2Node_ExecutionSequence_0.out0'] | val=
  IN  1 Object (Object Reference) <- ['K2Node_CallFunction_46.out0'] | val=
  OUT 0 then (Exec) -> ['K2Node_CallFunction_48.in0']
  OUT 1 CastFailed (Exec) -> <none>
  OUT 2 AsBP Third Person HUD (BP Third Person HUD Object Reference) -> ['K2Node_CallFunction_48.in1']
NODE K2Node_CallFunction_48 [|SetSlot] pos=-4,648
  IN  0 execute (Exec) <- ['K2Node_DynamicCast_2.out0'] | val=
  IN  1 self (BP Third Person HUD Object Reference) <- ['K2Node_DynamicCast_2.out2'] | val=
  IN  2 NewSlot (Integer) <- ['K2Node_CallFunction_47.out0'] | val=0
  OUT 0 then (Exec) -> <none>
NODE K2Node_CallFunction_47 [Math|Float|Truncate] pos=-354,722
  IN  0 A (Float (double-precision)) <- ['K2Node_EnhancedInputAction_0.out5'] | val=0.0
  OUT 0 ReturnValue (Integer) -> ['K2Node_CallFunction_48.in2', 'K2Node_VariableSet_0.in1']
NODE K2Node_CallFunction_10 [Pawn|GetControlledPawn] pos=-704,980
  IN  0 self (Controller Object Reference) <- <none> | val=
  OUT 0 ReturnValue (Pawn Object Reference) -> ['K2Node_DynamicCast_0.in1']
NODE K2Node_DynamicCast_0 [Utilities|Casting|CastToBP_ThirdPersonCharacter] pos=-354,900
  IN  0 execute (Exec) <- ['K2Node_ExecutionSequence_0.out1'] | val=
  IN  1 Object (Object Reference) <- ['K2Node_CallFunction_10.out0'] | val=
  OUT 0 then (Exec) -> ['K2Node_VariableSet_0.in0']
  OUT 1 CastFailed (Exec) -> <none>
  OUT 2 AsBP Third Person Character (BP Third Person Character Object Reference) -> ['K2Node_VariableSet_0.in2', 'K2Node_CallFunction_11.in1']
NODE K2Node_VariableSet_0 [|SetSelectedSlot] pos=-4,900
  IN  0 execute (Exec) <- ['K2Node_DynamicCast_0.out0'] | val=
  IN  1 SelectedSlot (Integer) <- ['K2Node_CallFunction_47.out0'] | val=0
  IN  2 self (BP Third Person Character Object Reference) <- ['K2Node_DynamicCast_0.out2'] | val=
  OUT 0 then (Exec) -> ['K2Node_CallFunction_11.in0']
  OUT 1 Output_Get (Integer) -> <none>
NODE K2Node_CallFunction_11 [|RefreshHeldItem] pos=300,900
  IN  0 execute (Exec) <- ['K2Node_VariableSet_0.out0'] | val=
  IN  1 self (BP Third Person Character Object Reference) <- ['K2Node_DynamicCast_0.out2'] | val=
  OUT 0 then (Exec) -> <none>
```

Checked point by point against the shape the command described:

| described | found | match |
|---|---|---|
| `IA_SelectSlot.Triggered -> K2Node_ExecutionSequence_0` | `OUT 0 Triggered -> ['K2Node_ExecutionSequence_0.in0']` | yes |
| `Sequence.then_0 -> K2Node_DynamicCast_2` | `OUT 0 then_0 -> ['K2Node_DynamicCast_2.in0']` | yes |
| `DynamicCast_2.Object <- K2Node_CallFunction_46 (Get HUD)` | `IN 1 Object <- ['K2Node_CallFunction_46.out0']` | yes |
| `DynamicCast_2.then -> K2Node_CallFunction_48 (SetSlot)` | `OUT 0 then -> ['K2Node_CallFunction_48.in0']` | yes |
| `DynamicCast_2.AsBP... -> K2Node_CallFunction_48.self` | `OUT 2 AsBP Third Person HUD -> ['K2Node_CallFunction_48.in1']` | yes |
| `Sequence.then_1 -> K2Node_DynamicCast_0` | `OUT 1 then_1 -> ['K2Node_DynamicCast_0.in0']` | yes |
| `DynamicCast_0.Object <- K2Node_CallFunction_10 (Get Controlled Pawn)` | `IN 1 Object <- ['K2Node_CallFunction_10.out0']` | yes |
| `DynamicCast_0.then -> K2Node_VariableSet_0` | `OUT 0 then -> ['K2Node_VariableSet_0.in0']` | yes |
| `K2Node_VariableSet_0 -> K2Node_CallFunction_11 (RefreshHeldItem)` | `OUT 0 then -> ['K2Node_CallFunction_11.in0']` | yes |
| `K2Node_CallFunction_47 (Truncate) takes ActionValue` | `IN 0 A <- ['K2Node_EnhancedInputAction_0.out5']` | yes |
| Truncate feeds BOTH SetSlot.NewSlot AND SetSelectedSlot | `OUT 0 -> ['K2Node_CallFunction_48.in2', 'K2Node_VariableSet_0.in1']` | yes |

**No difference found. Proceeded with the deletion.**

---

## 2. Node count

| | count |
|---|---|
| before | 26 |
| after  | 22 |

Four nodes removed, none added. Full node name list before:

```
["K2Node_CallFunction_10", "K2Node_CallFunction_11", "K2Node_CallFunction_18", "K2Node_CallFunction_19", "K2Node_CallFunction_20", "K2Node_CallFunction_21", "K2Node_CallFunction_22", "K2Node_CallFunction_23", "K2Node_CallFunction_24", "K2Node_CallFunction_46", "K2Node_CallFunction_47", "K2Node_CallFunction_48", "K2Node_CreateWidget_3", "K2Node_DynamicCast_0", "K2Node_DynamicCast_2", "K2Node_EnhancedInputAction_0", "K2Node_Event_0", "K2Node_ExecutionSequence_0", "K2Node_GetSubsystem_6", "K2Node_GetSubsystem_7", "K2Node_GetSubsystem_8", "K2Node_IfThenElse_4", "K2Node_IfThenElse_5", "K2Node_Self_2", "K2Node_VariableGet_3", "K2Node_VariableSet_0"]
```

Full node name list after:

```
["K2Node_CallFunction_10", "K2Node_CallFunction_11", "K2Node_CallFunction_18", "K2Node_CallFunction_19", "K2Node_CallFunction_20", "K2Node_CallFunction_21", "K2Node_CallFunction_22", "K2Node_CallFunction_23", "K2Node_CallFunction_24", "K2Node_CallFunction_47", "K2Node_CreateWidget_3", "K2Node_DynamicCast_0", "K2Node_EnhancedInputAction_0", "K2Node_Event_0", "K2Node_GetSubsystem_6", "K2Node_GetSubsystem_7", "K2Node_GetSubsystem_8", "K2Node_IfThenElse_4", "K2Node_IfThenElse_5", "K2Node_Self_2", "K2Node_VariableGet_3", "K2Node_VariableSet_0"]
```

The set difference of those two lists is exactly the four nodes the command named:
`K2Node_CallFunction_48`, `K2Node_DynamicCast_2`, `K2Node_CallFunction_46`,
`K2Node_ExecutionSequence_0`. `K2Node_CallFunction_47` (Truncate) is still present, as
required.

### Deletion calls (verbatim log from the batch script)

```
OK  delete_node K2Node_CallFunction_48 -> null
OK  delete_node K2Node_DynamicCast_2 -> null
OK  delete_node K2Node_CallFunction_46 -> null
OK  delete_node K2Node_ExecutionSequence_0 -> null
OK  connect EnhancedInputAction_0.Triggered -> DynamicCast_0.execute -> null
```

---

## 3. Every node remaining in the IA_SelectSlot chain after the change

Read back verbatim from `get_node_infos` after compile and save:

```
NODE K2Node_EnhancedInputAction_0 [Input|EnhancedActionEvents|EnhancedInputActionIA_SelectSlot] pos=-704,500
  OUT 0 Triggered (Exec) -> ['K2Node_DynamicCast_0.in0']
  OUT 1 Started (Exec) -> <none>
  OUT 2 Ongoing (Exec) -> <none>
  OUT 3 Canceled (Exec) -> <none>
  OUT 4 Completed (Exec) -> <none>
  OUT 5 ActionValue (Float (double-precision)) -> ['K2Node_CallFunction_47.in0']
  OUT 6 ElapsedSeconds (Float (double-precision)) -> <none>
  OUT 7 TriggeredSeconds (Float (double-precision)) -> <none>
  OUT 8 InputAction (Input Action Object Reference) -> <none>
NODE K2Node_CallFunction_47 [Math|Float|Truncate] pos=-354,722
  IN  0 A (Float (double-precision)) <- ['K2Node_EnhancedInputAction_0.out5'] | val=0.0
  OUT 0 ReturnValue (Integer) -> ['K2Node_VariableSet_0.in1']
NODE K2Node_CallFunction_10 [Pawn|GetControlledPawn] pos=-704,980
  IN  0 self (Controller Object Reference) <- <none> | val=
  OUT 0 ReturnValue (Pawn Object Reference) -> ['K2Node_DynamicCast_0.in1']
NODE K2Node_DynamicCast_0 [Utilities|Casting|CastToBP_ThirdPersonCharacter] pos=-354,900
  IN  0 execute (Exec) <- ['K2Node_EnhancedInputAction_0.out0'] | val=
  IN  1 Object (Object Reference) <- ['K2Node_CallFunction_10.out0'] | val=
  OUT 0 then (Exec) -> ['K2Node_VariableSet_0.in0']
  OUT 1 CastFailed (Exec) -> <none>
  OUT 2 AsBP Third Person Character (BP Third Person Character Object Reference) -> ['K2Node_VariableSet_0.in2', 'K2Node_CallFunction_11.in1']
NODE K2Node_VariableSet_0 [|SetSelectedSlot] pos=-4,900
  IN  0 execute (Exec) <- ['K2Node_DynamicCast_0.out0'] | val=
  IN  1 SelectedSlot (Integer) <- ['K2Node_CallFunction_47.out0'] | val=0
  IN  2 self (BP Third Person Character Object Reference) <- ['K2Node_DynamicCast_0.out2'] | val=
  OUT 0 then (Exec) -> ['K2Node_CallFunction_11.in0']
  OUT 1 Output_Get (Integer) -> <none>
NODE K2Node_CallFunction_11 [|RefreshHeldItem] pos=300,900
  IN  0 execute (Exec) <- ['K2Node_VariableSet_0.out0'] | val=
  IN  1 self (BP Third Person Character Object Reference) <- ['K2Node_DynamicCast_0.out2'] | val=
  OUT 0 then (Exec) -> <none>
```

The chain is now:

```
K2Node_EnhancedInputAction_0 (IA_SelectSlot) . Triggered
  -> K2Node_DynamicCast_0 (Cast To BP_ThirdPersonCharacter)
       Object   <- K2Node_CallFunction_10 (Get Controlled Pawn)
       CastFailed -> <none>
       then     -> K2Node_VariableSet_0 (SET SelectedSlot)
                     SelectedSlot <- K2Node_CallFunction_47 (Truncate)
                     self         <- K2Node_DynamicCast_0.AsBP Third Person Character
                -> K2Node_CallFunction_11 (RefreshHeldItem)
                     self         <- K2Node_DynamicCast_0.AsBP Third Person Character
                     then -> <none>
```

### Step 2 verification - Triggered now drives the cast directly

`K2Node_EnhancedInputAction_0.out0 (Triggered)` reads
`-> ['K2Node_DynamicCast_0.in0']`, and `K2Node_DynamicCast_0.in0 (execute)` reads
`<- ['K2Node_EnhancedInputAction_0.out0']`. Confirmed from both ends. The Sequence is gone
and the one surviving consumer is driven directly.

### Step 3 verification - Truncate survived with exactly one outgoing connection

```
NODE K2Node_CallFunction_47 [Math|Float|Truncate] pos=-354,722
  IN  0 A (Float (double-precision)) <- ['K2Node_EnhancedInputAction_0.out5'] | val=0.0
  OUT 0 ReturnValue (Integer) -> ['K2Node_VariableSet_0.in1']
```

- The node still exists (it appears in the after node list).
- `OUT 0 ReturnValue` has **exactly one** outgoing connection, `K2Node_VariableSet_0.in1`.
  Before the deletion it had two; the `K2Node_CallFunction_48.in2` target went away with the
  SetSlot node.
- `IN 0 A` is still fed by `K2Node_EnhancedInputAction_0.out5`, which is the event's
  `ActionValue` pin (confirmed by the event node's own read-back, where `OUT 5 ActionValue`
  reads `-> ['K2Node_CallFunction_47.in0']`).

Both conditions the command asked me to confirm hold.

---

## 4. Whole-graph before/after set difference

The full graph (every node, every edge including explicit `-> <none>`, every input pin value)
was dumped before and after and compared as line sets.

Lines present BEFORE but missing AFTER - i.e. every removal or alteration in the entire graph:

```
  EDGE K2Node_CallFunction_46.out0(ReturnValue) -> K2Node_DynamicCast_2.in1
  EDGE K2Node_CallFunction_47.out0(ReturnValue) -> K2Node_CallFunction_48.in2
  EDGE K2Node_CallFunction_48.out0(then) -> <none>
  EDGE K2Node_DynamicCast_2.out0(then) -> K2Node_CallFunction_48.in0
  EDGE K2Node_DynamicCast_2.out1(CastFailed) -> <none>
  EDGE K2Node_DynamicCast_2.out2(AsBP Third Person HUD) -> K2Node_CallFunction_48.in1
  EDGE K2Node_EnhancedInputAction_0.out0(Triggered) -> K2Node_ExecutionSequence_0.in0
  EDGE K2Node_ExecutionSequence_0.out0(then_0) -> K2Node_DynamicCast_2.in0
  EDGE K2Node_ExecutionSequence_0.out1(then_1) -> K2Node_DynamicCast_0.in0
  VAL K2Node_CallFunction_46.in0(self) = 
  VAL K2Node_CallFunction_48.in0(execute) = 
  VAL K2Node_CallFunction_48.in1(self) = 
  VAL K2Node_CallFunction_48.in2(NewSlot) = 0
  VAL K2Node_DynamicCast_2.in0(execute) = 
  VAL K2Node_DynamicCast_2.in1(Object) = 
  VAL K2Node_ExecutionSequence_0.in0(execute) = 
NODE K2Node_CallFunction_46 type=HUD|GetHUD pos=-704,648
NODE K2Node_CallFunction_48 type=|SetSlot pos=-4,648
NODE K2Node_DynamicCast_2 type=Utilities|Casting|CastToBP_ThirdPersonHUD pos=-354,574
NODE K2Node_ExecutionSequence_0 type=Utilities|FlowControl|Sequence pos=-540,500
```

Lines present AFTER but not BEFORE - i.e. every addition:

```
  EDGE K2Node_EnhancedInputAction_0.out0(Triggered) -> K2Node_DynamicCast_0.in0
```

Reading that list:

- The four `NODE` lines are the four nodes the command named for deletion, and nothing else.
- Every removed `EDGE` and `VAL` line belongs to one of those four nodes, with two
  exceptions, both of which are the intended consequence of the deletion:
  - `K2Node_CallFunction_47.out0 -> K2Node_CallFunction_48.in2` - the Truncate's second
    consumer, which went away with SetSlot. The Truncate node itself survives with its other
    connection intact.
  - `K2Node_EnhancedInputAction_0.out0 (Triggered) -> K2Node_ExecutionSequence_0.in0` -
    replaced by the single added line, the direct connection to `K2Node_DynamicCast_0.in0`.
- `K2Node_ExecutionSequence_0.out1 (then_1) -> K2Node_DynamicCast_0.in0` was removed with the
  Sequence; `K2Node_DynamicCast_0.in0` is now driven by the event instead. `K2Node_DynamicCast_0`
  itself was not deleted and none of its other pins changed.
- Exactly one line was added, and it is the step 2 reconnection.

No line belonging to the BeginPlay chain, the three AddMappingContext calls, the touch
controls branch, `K2Node_CallFunction_10`, `K2Node_DynamicCast_0`, `K2Node_VariableSet_0` or
`K2Node_CallFunction_11` appears in the removed set.

---

## 5. BeginPlay chain untouched

Read back verbatim after compile and save:

```
NODE K2Node_Event_0 [AddEvent|EventBeginPlay] pos=-704,-352
  OUT 0 OutputDelegate (Delegate) -> <none>
  OUT 1 then (Exec) -> ['K2Node_CallFunction_18.in0']
NODE K2Node_CallFunction_18 [Utilities|FlowControl|DelayUntilNextTick] pos=-424,-352
  IN  0 execute (Exec) <- ['K2Node_Event_0.out1'] | val=
  OUT 0 then (Exec) -> ['K2Node_IfThenElse_4.in0']
NODE K2Node_CallFunction_19 [Pawn|IsLocalPlayerController] pos=-144,-352
  IN  0 self (Controller Object Reference) <- <none> | val=
  OUT 0 ReturnValue (Boolean) -> ['K2Node_IfThenElse_4.in1']
NODE K2Node_CallFunction_20 [Input|AddMappingContext] pos=696,-352
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_4.out0'] | val=
  IN  1 self (Enhanced Input Subsystem Interface Interface) <- ['K2Node_GetSubsystem_6.out0'] | val=
  IN  2 MappingContext (Input Mapping Context Object Reference) <- <none> | val=/Game/Input/IMC_Default.IMC_Default
  IN  3 Priority (Integer) <- <none> | val=0
  IN  4 Options (Modify Context Options Structure (by ref)) <- <none> | val=(bIgnoreAllPressedKeysUntilRelease=True,bForceImmediately=False,bNotifyUserSettings=False)
  OUT 0 then (Exec) -> ['K2Node_CallFunction_21.in0']
NODE K2Node_CallFunction_21 [Input|AddMappingContext] pos=1256,-352
  IN  0 execute (Exec) <- ['K2Node_CallFunction_20.out0'] | val=
  IN  1 self (Enhanced Input Subsystem Interface Interface) <- ['K2Node_GetSubsystem_7.out0'] | val=
  IN  2 MappingContext (Input Mapping Context Object Reference) <- <none> | val=/Game/Input/IMC_Inventory.IMC_Inventory
  IN  3 Priority (Integer) <- <none> | val=0
  IN  4 Options (Modify Context Options Structure (by ref)) <- <none> | val=(bIgnoreAllPressedKeysUntilRelease=True,bForceImmediately=False,bNotifyUserSettings=False)
  OUT 0 then (Exec) -> ['K2Node_IfThenElse_5.in0']
NODE K2Node_CallFunction_22 [Default|ShouldUseTouchControls] pos=1536,-352
  OUT 0 Use Mobile Controls (Boolean) -> ['K2Node_IfThenElse_5.in1']
NODE K2Node_CallFunction_23 [UserInterface|Viewport|AddToPlayerScreen] pos=2656,-352
  IN  0 execute (Exec) <- ['K2Node_CreateWidget_3.out0'] | val=
  IN  1 self (User Widget Object Reference) <- ['K2Node_CreateWidget_3.out1'] | val=
  IN  2 ZOrder (Integer) <- <none> | val=0
  OUT 0 then (Exec) -> <none>
  OUT 1 ReturnValue (Boolean) -> <none>
NODE K2Node_CallFunction_24 [Input|AddMappingContext] pos=2376,-152
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_5.out1'] | val=
  IN  1 self (Enhanced Input Subsystem Interface Interface) <- ['K2Node_GetSubsystem_8.out0'] | val=
  IN  2 MappingContext (Input Mapping Context Object Reference) <- <none> | val=/Game/Input/IMC_MouseLook.IMC_MouseLook
  IN  3 Priority (Integer) <- <none> | val=0
  IN  4 Options (Modify Context Options Structure (by ref)) <- <none> | val=(bIgnoreAllPressedKeysUntilRelease=True,bForceImmediately=False,bNotifyUserSettings=False)
  OUT 0 then (Exec) -> <none>
NODE K2Node_IfThenElse_4 [Utilities|FlowControl|Branch] pos=136,-352
  IN  0 execute (Exec) <- ['K2Node_CallFunction_18.out0'] | val=
  IN  1 Condition (Boolean) <- ['K2Node_CallFunction_19.out0'] | val=true
  OUT 0 then (Exec) -> ['K2Node_CallFunction_20.in0']
  OUT 1 else (Exec) -> <none>
NODE K2Node_IfThenElse_5 [Utilities|FlowControl|Branch] pos=1816,-352
  IN  0 execute (Exec) <- ['K2Node_CallFunction_21.out0'] | val=
  IN  1 Condition (Boolean) <- ['K2Node_CallFunction_22.out0'] | val=true
  OUT 0 then (Exec) -> ['K2Node_CreateWidget_3.in0']
  OUT 1 else (Exec) -> ['K2Node_CallFunction_24.in0']
NODE K2Node_CreateWidget_3 [UserInterface|CreateWidget] pos=2376,-352
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_5.out0'] | val=
  IN  1 Class (User Widget Class Reference) <- ['K2Node_VariableGet_3.out0'] | val=
  IN  2 OwningPlayer (Player Controller Object Reference) <- ['K2Node_Self_2.out0'] | val=
  OUT 0 then (Exec) -> ['K2Node_CallFunction_23.in0']
  OUT 1 ReturnValue (User Widget Object Reference) -> ['K2Node_CallFunction_23.in1']
NODE K2Node_GetSubsystem_6 [LocalPlayerSubsystems|GetEnhancedInputLocalPlayerSubsystem] pos=416,-352
  OUT 0 ReturnValue (Enhanced Input Local Player Subsystem Object Reference) -> ['K2Node_CallFunction_20.in1']
NODE K2Node_GetSubsystem_7 [LocalPlayerSubsystems|GetEnhancedInputLocalPlayerSubsystem] pos=976,-352
  OUT 0 ReturnValue (Enhanced Input Local Player Subsystem Object Reference) -> ['K2Node_CallFunction_21.in1']
NODE K2Node_GetSubsystem_8 [LocalPlayerSubsystems|GetEnhancedInputLocalPlayerSubsystem] pos=2096,-152
  OUT 0 ReturnValue (Enhanced Input Local Player Subsystem Object Reference) -> ['K2Node_CallFunction_24.in1']
NODE K2Node_Self_2 [Variables|Self-Reference] pos=-704,-432
  OUT 0 self (Self Object Reference) -> ['K2Node_CreateWidget_3.in2']
NODE K2Node_VariableGet_3 [|GetTouchControlsWidgetClass] pos=2096,-352
  OUT 0 Touch Controls Widget Class (User Widget Class Reference) -> ['K2Node_CreateWidget_3.in1']
```

All sixteen BeginPlay-side nodes are present with identical types, positions, connections and
pin values. Independently confirmed by the set difference in section 4: not one line naming
any of these nodes appears in the removed set. Specifically intact:

- `BeginPlay -> DelayUntilNextTick -> Branch(IsLocalPlayerController)`
- the three `AddMappingContext` calls with their contexts unchanged - `IMC_Default`
  (`K2Node_CallFunction_20`), `IMC_Inventory` (`K2Node_CallFunction_21`), `IMC_MouseLook`
  (`K2Node_CallFunction_24`) - each still Priority 0 with the same Options struct
- the touch controls branch `K2Node_IfThenElse_5` with `then -> CreateWidget -> AddToPlayerScreen`
  and `else -> AddMappingContext(IMC_MouseLook)`

---

## 6. Variable list

Before (2), from `list_variables`:

```
["Touch Controls Widget Class", "Force Touch Controls"]
```

After (2), from `list_variables`:

```
["Touch Controls Widget Class", "Force Touch Controls"]
```

Identical. Nothing added, renamed or removed. The graph list is also unchanged:

```
before: ["UserConstructionScript", "Should Use Touch Controls", "EventGraph"]
after:  ["UserConstructionScript", "Should Use Touch Controls", "EventGraph"]
```

Nothing was deleted or modified in `BP_ThirdPersonHUD` in this command. Its `SelectedSlot`
variable and `SetSlot` function are still present there; `SetSlot` now simply has no callers,
which is the intended state until a later step removes it.

---

## 7. On-disk file size

| | bytes | mtime |
|---|---|---|
| before | 116970 | Aug 29 11:14 |
| after  | 107507 | Aug 29 13:32 |

Delta: **-9463 bytes**. The file shrank, which is consistent with a deletion command.

Raw `ls -la` before:

```
-rw-r--r-- 1 a0108 197609 116970 Aug 29 11:14 Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset
```

Raw `ls -la` after:

```
-rw-r--r-- 1 a0108 197609 107507 Aug 29 13:32 Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset
```

`git status` after the save:

```
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonHUD.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset
?? Docs/Terminal-Log/
```

The HUD entry is from earlier commands in this session and was not touched here.

---

## 8. Compile result

One compile was run in this command, with `warnings_as_errors: true`, and it did not raise.

Verbatim log line for this command's compile:

```
[2026.08.29-04.32.05:158][311]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.BP_ThirdPersonPlayerController'
```

A regex sweep of the output log across 04.30 - 04.39 for `Warning|Error`, which covers the
compile and the save, returned an empty list:

```
{"returnValue":[]}
```

No errors. No warnings. `save_assets` returned `true` and `is_dirty` afterwards returned
`false`.

### Warning and error lines seen, verbatim

**None.** Zero warning or error lines were produced at any point in this command - during the
read-back, the four deletions, the reconnection, the compile, or the save. The sweep above is
the evidence.

Worth noting explicitly because it was a plausible failure mode: deleting
`K2Node_CallFunction_48` removed the only caller of `BP_ThirdPersonHUD`'s `SetSlot` function,
and the compile produced no warning about the now-uncalled function. That is expected - an
uncalled Blueprint function is not a compile diagnostic - but it means the compiler will not
flag `SetSlot` as dead when it is removed in a later step.

---

## 9. Places where a tool's response disagreed with the read-back

1. **Write calls return `null` on success, not `true`.**
   All four `delete_node` calls and the `connect_pins` call returned `null`, as did
   `compile_blueprint`. Read-back confirmed the four nodes are gone, the new connection
   exists, and the Blueprint compiled. `null` here means success and the return value carries
   no information either way. By contrast `AssetTools.save_assets` returned `true`. None of
   these return values were used as evidence anywhere in this report.

2. **No other disagreement.** Every claim in this report was checked against a read-back
   after the compile and save, and each read-back matched what the write calls implied. There
   was nothing in this command that a tool reported one way and the graph showed another.

---

## 10. Not verified

No PIE run was performed. The following are unconfirmed at runtime:

- that pressing 1/2/3 still sets `SelectedSlot` on the pawn and refreshes the held item
- that the HUD still displays the correct selected slot now that the player controller no
  longer pushes it - the HUD reads `SelectedSlot` from the cached pawn instead, wired in an
  earlier command, and this command relies on that path already working
- that removing the Sequence introduced no ordering change that matters. With one consumer
  left there is no ordering to preserve, but this is reasoned, not observed.

Only graph topology and a clean compile are established.
