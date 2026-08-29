# Remove the pickup debug print and turn off line trace debug drawing - BP_ThirdPersonCharacter

Date: 2026-08-29
Blueprint: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter`
Graph: `BP_ThirdPersonCharacter:EventGraph`

All facts below were read back with
`editor_toolset.toolsets.blueprint.BlueprintTools.get_node_infos`, `.list_variables` and
`.list_graphs`. The "before" state was read back BEFORE anything was changed; everything else
was read back AFTER the compile and save. None of them come from the return value of a write
call.

---

## 1. Shape found before changing anything

Read back with `get_node_infos` as the first action of this command, before any write:

```
NODE K2Node_CallArrayFunction_3 [Utilities|Array|SetArrayElem] pos=320,220
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_2.out0'] | val=
  IN  1 TargetArray (Array of Names) <- ['K2Node_VariableGet_6.out0'] | val=
  IN  2 Index (Integer) <- ['K2Node_VariableGet_9.out0'] | val=0
  IN  3 Item (Name (by ref)) <- ['K2Node_BreakStruct_1.out1'] | val=
  IN  4 bSizeToFit (Boolean) <- <none> | val=false
  OUT 0 then (Exec) -> ['K2Node_CallFunction_18.in0']
NODE K2Node_CallFunction_18 [|RefreshHeldItem] pos=600,220
  IN  0 execute (Exec) <- ['K2Node_CallArrayFunction_3.out0'] | val=
  IN  1 self (Self Object Reference) <- <none> | val=
  OUT 0 then (Exec) -> ['K2Node_CallFunction_34.in0']
NODE K2Node_CallFunction_34 [Development|PrintString] pos=860,220
  IN  0 execute (Exec) <- ['K2Node_CallFunction_18.out0'] | val=
  IN  1 InString (String) <- ['K2Node_CallFunction_33.out0'] | val=Hello
  IN  2 bPrintToScreen (Boolean) <- <none> | val=true
  IN  3 bPrintToLog (Boolean) <- <none> | val=true
  IN  4 TextColor (Linear Color Structure) <- <none> | val=(R=0.000000,G=0.660000,B=1.000000,A=1.000000)
  IN  5 Duration (Float (single-precision)) <- <none> | val=3.0
  IN  6 Key (Name) <- <none> | val=None
  OUT 0 then (Exec) -> ['K2Node_CallFunction_35.in0']
NODE K2Node_CallFunction_35 [Actor|DestroyActor] pos=1140,220
  IN  0 execute (Exec) <- ['K2Node_CallFunction_34.out0'] | val=
  IN  1 self (Actor Object Reference) <- ['K2Node_DynamicCast_1.out2'] | val=
  OUT 0 then (Exec) -> <none>
NODE K2Node_CallFunction_32 [Utilities|String|BuildString(Name)] pos=320,640
  IN  0 AppendTo (String) <- <none> | val=
  IN  1 Prefix (String) <- <none> | val=PICKED 
  IN  2 InName (Name) <- ['K2Node_BreakStruct_1.out1'] | val=None
  IN  3 Suffix (String) <- <none> | val= -> slot 
  OUT 0 ReturnValue (String) -> ['K2Node_CallFunction_33.in0']
NODE K2Node_CallFunction_33 [Utilities|String|BuildString(Integer)] pos=600,640
  IN  0 AppendTo (String) <- ['K2Node_CallFunction_32.out0'] | val=
  IN  1 Prefix (String) <- <none> | val=
  IN  2 InInt (Integer) <- ['K2Node_VariableGet_10.out0'] | val=0
  IN  3 Suffix (String) <- <none> | val=
  OUT 0 ReturnValue (String) -> ['K2Node_CallFunction_34.in1']
NODE K2Node_BreakStruct_1 [Utilities|Struct|BreakDataTableRowHandle] pos=-620,520
  IN  0 DataTableRowHandle (Data Table Row Handle Structure (by ref)) <- ['K2Node_VariableGet_3.out0'] | val=
  OUT 0 DataTable (Data Table Object Reference) -> <none>
  OUT 1 RowName (Name) -> ['K2Node_CallArrayFunction_3.in3', 'K2Node_CallFunction_32.in2']
NODE K2Node_VariableGet_10 [|GetFoundSlotIndex] pos=360,800
  OUT 0 FoundSlotIndex (Integer) -> ['K2Node_CallFunction_33.in2']
NODE K2Node_CallFunction_25 [Collision|LineTraceByChannel] pos=-1560,220
  IN  0 execute (Exec) <- ['K2Node_EnhancedInputAction_3.out1'] | val=
  IN  1 Start (Vector) <- ['K2Node_CallFunction_20.out0'] | val=0, 0, 0
  IN  2 End (Vector) <- ['K2Node_PromotableOperator_3.out0'] | val=0, 0, 0
  IN  3 TraceChannel (ETraceTypeQuery Enum) <- <none> | val=TraceTypeQuery1
  IN  4 bTraceComplex (Boolean) <- <none> | val=false
  IN  5 ActorsToIgnore (Array of Actor Object References) <- <none> | val=
  IN  6 DrawDebugType (EDrawDebugTrace Enum) <- <none> | val=ForDuration
  IN  7 bIgnoreSelf (Boolean) <- <none> | val=true
  IN  8 TraceColor (Linear Color Structure) <- <none> | val=(R=1.000000,G=0.000000,B=0.000000,A=1.000000)
  IN  9 TraceHitColor (Linear Color Structure) <- <none> | val=(R=0.000000,G=1.000000,B=0.000000,A=1.000000)
  IN  10 DrawTime (Float (single-precision)) <- <none> | val=5.000000
  OUT 0 then (Exec) -> ['K2Node_IfThenElse_1.in0']
  OUT 1 OutHit (Hit Result Structure) -> ['K2Node_CallFunction_26.in0']
  OUT 2 ReturnValue (Boolean) -> ['K2Node_IfThenElse_1.in1']
NODE K2Node_CallFunction_36 [Development|PrintString] pos=320,980
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_2.out1'] | val=
  IN  1 InString (String) <- <none> | val=INVENTORY FULL
  IN  2 bPrintToScreen (Boolean) <- <none> | val=true
  IN  3 bPrintToLog (Boolean) <- <none> | val=true
  IN  4 TextColor (Linear Color Structure) <- <none> | val=(R=0.000000,G=0.660000,B=1.000000,A=1.000000)
  IN  5 Duration (Float (single-precision)) <- <none> | val=3.0
  IN  6 Key (Name) <- <none> | val=None
  OUT 0 then (Exec) -> <none>
NODE K2Node_IfThenElse_2 [Utilities|FlowControl|Branch] pos=-170,220
  IN  0 execute (Exec) <- ['K2Node_VariableSet_1.out0'] | val=
  IN  1 Condition (Boolean) <- ['K2Node_PromotableOperator_5.out0'] | val=true
  OUT 0 then (Exec) -> ['K2Node_CallArrayFunction_3.in0']
  OUT 1 else (Exec) -> ['K2Node_CallFunction_36.in0']
```

Checked point by point against the shape the command described:

| described | found | match |
|---|---|---|
| `SetArrayElem -> K2Node_CallFunction_18 (RefreshHeldItem)` | `K2Node_CallArrayFunction_3.out0 -> ['K2Node_CallFunction_18.in0']` | yes |
| `RefreshHeldItem -> K2Node_CallFunction_34 (Print String)` | `K2Node_CallFunction_18.out0 -> ['K2Node_CallFunction_34.in0']` | yes |
| `Print String -> K2Node_CallFunction_35 (Destroy Actor)` | `K2Node_CallFunction_34.out0 -> ['K2Node_CallFunction_35.in0']` | yes |
| `K2Node_CallFunction_32 BuildString(Name)` Prefix `"PICKED "` | `IN 1 Prefix = PICKED ` | yes |
| `K2Node_CallFunction_32` Suffix `" -> slot "` | `IN 3 Suffix =  -> slot ` | yes |
| `K2Node_CallFunction_32.InName <- K2Node_BreakStruct_1.out1` | `IN 2 InName <- ['K2Node_BreakStruct_1.out1']` | yes |
| `K2Node_CallFunction_32 -> K2Node_CallFunction_33 BuildString(Integer)` | `OUT 0 -> ['K2Node_CallFunction_33.in0']` | yes |
| `K2Node_CallFunction_33.InInt <- K2Node_VariableGet_10` | `IN 2 InInt <- ['K2Node_VariableGet_10.out0']` | yes |
| `K2Node_CallFunction_33 -> K2Node_CallFunction_34.InString` | `OUT 0 -> ['K2Node_CallFunction_34.in1']` | yes |
| `K2Node_CallFunction_25 DrawDebugType = ForDuration` | `IN 6 DrawDebugType (EDrawDebugTrace Enum) = ForDuration` | yes |

Also noted before changing anything, because both matter to the instructions:

- `K2Node_BreakStruct_1.out1 (RowName)` had **two** consumers:
  `K2Node_CallArrayFunction_3.in3` (the Item pin that must survive) and
  `K2Node_CallFunction_32.in2` (the one that goes away with the deleted node).
- `K2Node_CallFunction_36` ("INVENTORY FULL") sits on `K2Node_IfThenElse_2.out1 (else)`,
  entirely off the success path being edited.

**No difference found. Proceeded with the changes.**

---

## 2. What was done

Verbatim log from the batch script:

```
OK  delete_node K2Node_CallFunction_34 -> null
OK  delete_node K2Node_CallFunction_33 -> null
OK  delete_node K2Node_CallFunction_32 -> null
OK  connect CallFunction_18.then -> CallFunction_35.execute -> null
OK  delete_node K2Node_VariableGet_10 (0 consumers) -> null
OK  set CallFunction_25.in6 DrawDebugType = None -> null
```

### Step 3 - what happened to K2Node_VariableGet_10 and why

`K2Node_VariableGet_10` is a **Get of the variable `FoundSlotIndex`** - its `type_id` reads
back as `|GetFoundSlotIndex` and its output pin is named `FoundSlotIndex`, type `Integer`.

After step 1 deleted the three string/print nodes, `K2Node_VariableGet_10` was re-read with
`get_node_infos` before deciding. Result:

```
{"pin": "FoundSlotIndex", "type": "Integer", "targets": []}
remaining consumers: 0
```

Its only consumer before this command was `K2Node_CallFunction_33.in2` (the deleted
BuildString(Integer)'s InInt pin). With that node gone it had zero outgoing connections, so
per the command's instruction - "if its output has NO remaining outgoing connections, delete
it too" - **I deleted it**.

Note that this did **not** orphan the `FoundSlotIndex` variable itself. A different Get of
the same variable, `K2Node_VariableGet_9` at pos 60,430, survives and still feeds
`K2Node_CallArrayFunction_3.in2` (the Set Array Elem Index pin), and `K2Node_VariableSet_1`
still writes it. Only the second, now-unused getter node was removed. The variable is still
in the variable list, unchanged.

---

## 3. Every node remaining in the IA_Interact chain after the change

Read back verbatim from `get_node_infos` after compile and save:

```
NODE K2Node_EnhancedInputAction_3 [Input|EnhancedActionEvents|EnhancedInputActionIA_Interact] pos=-2800,200
  OUT 0 Triggered (Exec) -> <none>
  OUT 1 Started (Exec) -> ['K2Node_CallFunction_25.in0']
  OUT 2 Ongoing (Exec) -> <none>
  OUT 3 Canceled (Exec) -> <none>
  OUT 4 Completed (Exec) -> <none>
  OUT 5 ActionValue (Boolean) -> <none>
  OUT 6 ElapsedSeconds (Float (double-precision)) -> <none>
  OUT 7 TriggeredSeconds (Float (double-precision)) -> <none>
  OUT 8 InputAction (Input Action Object Reference) -> <none>
NODE K2Node_CallFunction_25 [Collision|LineTraceByChannel] pos=-1560,220
  IN  0 execute (Exec) <- ['K2Node_EnhancedInputAction_3.out1'] | val=
  IN  1 Start (Vector) <- ['K2Node_CallFunction_20.out0'] | val=0, 0, 0
  IN  2 End (Vector) <- ['K2Node_PromotableOperator_3.out0'] | val=0, 0, 0
  IN  3 TraceChannel (ETraceTypeQuery Enum) <- <none> | val=TraceTypeQuery1
  IN  4 bTraceComplex (Boolean) <- <none> | val=false
  IN  5 ActorsToIgnore (Array of Actor Object References) <- <none> | val=
  IN  6 DrawDebugType (EDrawDebugTrace Enum) <- <none> | val=None
  IN  7 bIgnoreSelf (Boolean) <- <none> | val=true
  IN  8 TraceColor (Linear Color Structure) <- <none> | val=(R=1.000000,G=0.000000,B=0.000000,A=1.000000)
  IN  9 TraceHitColor (Linear Color Structure) <- <none> | val=(R=0.000000,G=1.000000,B=0.000000,A=1.000000)
  IN  10 DrawTime (Float (single-precision)) <- <none> | val=5.000000
  OUT 0 then (Exec) -> ['K2Node_IfThenElse_1.in0']
  OUT 1 OutHit (Hit Result Structure) -> ['K2Node_CallFunction_26.in0']
  OUT 2 ReturnValue (Boolean) -> ['K2Node_IfThenElse_1.in1']
NODE K2Node_IfThenElse_1 [Utilities|FlowControl|Branch] pos=-1150,220
  IN  0 execute (Exec) <- ['K2Node_CallFunction_25.out0'] | val=
  IN  1 Condition (Boolean) <- ['K2Node_CallFunction_25.out2'] | val=true
  OUT 0 then (Exec) -> ['K2Node_DynamicCast_1.in0']
  OUT 1 else (Exec) -> <none>
NODE K2Node_CallFunction_26 [Collision|BreakHitResult] pos=-1150,430
  IN  0 Hit (Hit Result Structure (by ref)) <- ['K2Node_CallFunction_25.out1'] | val=
  OUT 0 bBlockingHit (Boolean) -> <none>
  OUT 1 bInitialOverlap (Boolean) -> <none>
  OUT 2 Time (Float (single-precision)) -> <none>
  OUT 3 Distance (Float (single-precision)) -> <none>
  OUT 4 Location (Vector) -> <none>
  OUT 5 ImpactPoint (Vector) -> <none>
  OUT 6 Normal (Vector) -> <none>
  OUT 7 ImpactNormal (Vector) -> <none>
  OUT 8 PhysMat (Physical Material Object Reference) -> <none>
  OUT 9 HitActor (Actor Object Reference) -> ['K2Node_DynamicCast_1.in1']
  OUT 10 HitComponent (Primitive Component Object Reference) -> <none>
  OUT 11 HitBoneName (Name) -> <none>
  OUT 12 BoneName (Name) -> <none>
  OUT 13 HitItem (Integer) -> <none>
  OUT 14 ElementIndex (Integer) -> <none>
  OUT 15 FaceIndex (Integer) -> <none>
  OUT 16 TraceStart (Vector) -> <none>
  OUT 17 TraceEnd (Vector) -> <none>
NODE K2Node_DynamicCast_1 [Utilities|Casting|CastToBP_ItemPickup] pos=-860,220
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_1.out0'] | val=
  IN  1 Object (Object Reference) <- ['K2Node_CallFunction_26.out9'] | val=
  OUT 0 then (Exec) -> ['K2Node_VariableSet_1.in0']
  OUT 1 CastFailed (Exec) -> <none>
  OUT 2 AsBP Item Pickup (BP Item Pickup Object Reference) -> ['K2Node_VariableGet_3.in0', 'K2Node_CallFunction_35.in1']
NODE K2Node_VariableGet_3 [|GetItemRow] pos=-860,520
  IN  0 self (BP Item Pickup Object Reference) <- ['K2Node_DynamicCast_1.out2'] | val=
  OUT 0 ItemRow (Data Table Row Handle Structure) -> ['K2Node_BreakStruct_1.in0']
NODE K2Node_BreakStruct_1 [Utilities|Struct|BreakDataTableRowHandle] pos=-620,520
  IN  0 DataTableRowHandle (Data Table Row Handle Structure (by ref)) <- ['K2Node_VariableGet_3.out0'] | val=
  OUT 0 DataTable (Data Table Object Reference) -> <none>
  OUT 1 RowName (Name) -> ['K2Node_CallArrayFunction_3.in3']
NODE K2Node_VariableGet_5 [|GetInventorySlots] pos=-900,720
  OUT 0 InventorySlots (Array of Names) -> ['K2Node_CallArrayFunction_2.in0']
NODE K2Node_CallArrayFunction_2 [Utilities|Array|FindItem] pos=-640,720
  IN  0 TargetArray (Array of Names) <- ['K2Node_VariableGet_5.out0'] | val=
  IN  1 ItemToFind (Name (by ref)) <- <none> | val=
  OUT 0 ReturnValue (Integer) -> ['K2Node_VariableSet_1.in1']
NODE K2Node_PromotableOperator_5 [Math|Integer|integer>=integer] pos=-400,780
  IN  0 A (Integer) <- ['K2Node_VariableGet_8.out0'] | val=
  IN  1 B (Integer) <- <none> | val=
  OUT 0 ReturnValue (Boolean) -> ['K2Node_IfThenElse_2.in1']
NODE K2Node_VariableSet_1 [|SetFoundSlotIndex] pos=-450,220
  IN  0 execute (Exec) <- ['K2Node_DynamicCast_1.out0'] | val=
  IN  1 FoundSlotIndex (Integer) <- ['K2Node_CallArrayFunction_2.out0'] | val=0
  OUT 0 then (Exec) -> ['K2Node_IfThenElse_2.in0']
  OUT 1 Output_Get (Integer) -> <none>
NODE K2Node_IfThenElse_2 [Utilities|FlowControl|Branch] pos=-170,220
  IN  0 execute (Exec) <- ['K2Node_VariableSet_1.out0'] | val=
  IN  1 Condition (Boolean) <- ['K2Node_PromotableOperator_5.out0'] | val=true
  OUT 0 then (Exec) -> ['K2Node_CallArrayFunction_3.in0']
  OUT 1 else (Exec) -> ['K2Node_CallFunction_36.in0']
NODE K2Node_VariableGet_6 [|GetInventorySlots] pos=60,600
  OUT 0 InventorySlots (Array of Names) -> ['K2Node_CallArrayFunction_3.in1']
NODE K2Node_VariableGet_9 [|GetFoundSlotIndex] pos=60,430
  OUT 0 FoundSlotIndex (Integer) -> ['K2Node_CallArrayFunction_3.in2']
NODE K2Node_CallArrayFunction_3 [Utilities|Array|SetArrayElem] pos=320,220
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_2.out0'] | val=
  IN  1 TargetArray (Array of Names) <- ['K2Node_VariableGet_6.out0'] | val=
  IN  2 Index (Integer) <- ['K2Node_VariableGet_9.out0'] | val=0
  IN  3 Item (Name (by ref)) <- ['K2Node_BreakStruct_1.out1'] | val=
  IN  4 bSizeToFit (Boolean) <- <none> | val=false
  OUT 0 then (Exec) -> ['K2Node_CallFunction_18.in0']
NODE K2Node_CallFunction_18 [|RefreshHeldItem] pos=600,220
  IN  0 execute (Exec) <- ['K2Node_CallArrayFunction_3.out0'] | val=
  IN  1 self (Self Object Reference) <- <none> | val=
  OUT 0 then (Exec) -> ['K2Node_CallFunction_35.in0']
NODE K2Node_CallFunction_35 [Actor|DestroyActor] pos=1140,220
  IN  0 execute (Exec) <- ['K2Node_CallFunction_18.out0'] | val=
  IN  1 self (Actor Object Reference) <- ['K2Node_DynamicCast_1.out2'] | val=
  OUT 0 then (Exec) -> <none>
NODE K2Node_CallFunction_36 [Development|PrintString] pos=320,980
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_2.out1'] | val=
  IN  1 InString (String) <- <none> | val=INVENTORY FULL
  IN  2 bPrintToScreen (Boolean) <- <none> | val=true
  IN  3 bPrintToLog (Boolean) <- <none> | val=true
  IN  4 TextColor (Linear Color Structure) <- <none> | val=(R=0.000000,G=0.660000,B=1.000000,A=1.000000)
  IN  5 Duration (Float (single-precision)) <- <none> | val=3.0
  IN  6 Key (Name) <- <none> | val=None
  OUT 0 then (Exec) -> <none>
```

### Step 2 verification - the success path is now three nodes

`K2Node_CallArrayFunction_3.out0 (then)` reads `-> ['K2Node_CallFunction_18.in0']`,
`K2Node_CallFunction_18.out0 (then)` reads `-> ['K2Node_CallFunction_35.in0']`, and
`K2Node_CallFunction_35.in0 (execute)` reads `<- ['K2Node_CallFunction_18.out0']`. Confirmed
from both ends:

```
Set Array Elem -> RefreshHeldItem -> Destroy Actor
```

`K2Node_CallFunction_35`'s `self` pin is still fed by `K2Node_DynamicCast_1.out2`, unchanged.

---

## 4. Full pin list of K2Node_CallFunction_25 after the change

```
NODE K2Node_CallFunction_25 [Collision|LineTraceByChannel] pos=-1560,220
  IN  0 execute (Exec) <- ['K2Node_EnhancedInputAction_3.out1'] | val=
  IN  1 Start (Vector) <- ['K2Node_CallFunction_20.out0'] | val=0, 0, 0
  IN  2 End (Vector) <- ['K2Node_PromotableOperator_3.out0'] | val=0, 0, 0
  IN  3 TraceChannel (ETraceTypeQuery Enum) <- <none> | val=TraceTypeQuery1
  IN  4 bTraceComplex (Boolean) <- <none> | val=false
  IN  5 ActorsToIgnore (Array of Actor Object References) <- <none> | val=
  IN  6 DrawDebugType (EDrawDebugTrace Enum) <- <none> | val=None
  IN  7 bIgnoreSelf (Boolean) <- <none> | val=true
  IN  8 TraceColor (Linear Color Structure) <- <none> | val=(R=1.000000,G=0.000000,B=0.000000,A=1.000000)
  IN  9 TraceHitColor (Linear Color Structure) <- <none> | val=(R=0.000000,G=1.000000,B=0.000000,A=1.000000)
  IN  10 DrawTime (Float (single-precision)) <- <none> | val=5.000000
  OUT 0 then (Exec) -> ['K2Node_IfThenElse_1.in0']
  OUT 1 OutHit (Hit Result Structure) -> ['K2Node_CallFunction_26.in0']
  OUT 2 ReturnValue (Boolean) -> ['K2Node_IfThenElse_1.in1']
```

Pin by pin against before:

| pin | before | after | changed |
|---|---|---|---|
| 0 execute | `K2Node_EnhancedInputAction_3.out1` | same | no |
| 1 Start | `K2Node_CallFunction_20.out0` | same | no |
| 2 End | `K2Node_PromotableOperator_3.out0` | same | no |
| 3 TraceChannel | `TraceTypeQuery1` | `TraceTypeQuery1` | no |
| 4 bTraceComplex | `false` | `false` | no |
| 5 ActorsToIgnore | empty | empty | no |
| **6 DrawDebugType** | **`ForDuration`** | **`None`** | **yes - the only change** |
| 7 bIgnoreSelf | `true` | `true` | no |
| 8 TraceColor | `(R=1.000000,G=0.000000,B=0.000000,A=1.000000)` | same | no |
| 9 TraceHitColor | `(R=0.000000,G=1.000000,B=0.000000,A=1.000000)` | same | no |
| 10 DrawTime | `5.000000` | `5.000000` | no |
| OUT 0 then | `K2Node_IfThenElse_1.in0` | same | no |
| OUT 1 OutHit | `K2Node_CallFunction_26.in0` | same | no |
| OUT 2 ReturnValue | `K2Node_IfThenElse_1.in1` | same | no |

Exactly one pin changed. `DrawTime` was deliberately left at 5.000000 as instructed - it is
inert while DrawDebugType is None.

---

## 5. K2Node_BreakStruct_1 and K2Node_CallFunction_36

### K2Node_BreakStruct_1 - survived, one consumer removed as required

Before:

```
NODE K2Node_BreakStruct_1 [Utilities|Struct|BreakDataTableRowHandle] pos=-620,520
  IN  0 DataTableRowHandle (Data Table Row Handle Structure (by ref)) <- ['K2Node_VariableGet_3.out0'] | val=
  OUT 0 DataTable (Data Table Object Reference) -> <none>
  OUT 1 RowName (Name) -> ['K2Node_CallArrayFunction_3.in3', 'K2Node_CallFunction_32.in2']
```

After:

```
NODE K2Node_BreakStruct_1 [Utilities|Struct|BreakDataTableRowHandle] pos=-620,520
  IN  0 DataTableRowHandle (Data Table Row Handle Structure (by ref)) <- ['K2Node_VariableGet_3.out0'] | val=
  OUT 0 DataTable (Data Table Object Reference) -> <none>
  OUT 1 RowName (Name) -> ['K2Node_CallArrayFunction_3.in3']
```

The node was **not** deleted. Its type, position and input are identical. `OUT 0 DataTable`
is still unconnected. `OUT 1 RowName` lost exactly one target - `K2Node_CallFunction_32.in2`,
which went away with the deleted BuildString(Name) node - and **retains
`K2Node_CallArrayFunction_3.in3`**, the Set Array Elem `Item` pin that the command said must
survive. That is the only difference, and it is the unavoidable consequence of deleting one
of its two consumers.

### K2Node_CallFunction_36 - completely untouched

Before and after are byte-identical:

```
NODE K2Node_CallFunction_36 [Development|PrintString] pos=320,980
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_2.out1'] | val=
  IN  1 InString (String) <- <none> | val=INVENTORY FULL
  IN  2 bPrintToScreen (Boolean) <- <none> | val=true
  IN  3 bPrintToLog (Boolean) <- <none> | val=true
  IN  4 TextColor (Linear Color Structure) <- <none> | val=(R=0.000000,G=0.660000,B=1.000000,A=1.000000)
  IN  5 Duration (Float (single-precision)) <- <none> | val=3.0
  IN  6 Key (Name) <- <none> | val=None
  OUT 0 then (Exec) -> <none>
```

Independently confirmed by the set difference in section 7: not one line naming
`K2Node_CallFunction_36` appears in the removed set. `K2Node_IfThenElse_2.out1 (else)` still
drives it.

---

## 6. Node counts

Per graph, before:

```
{"UserConstructionScript": 1, "Move": 11, "Aim": 5, "ToggleCameraView": 34, "RefreshHeldItem": 19, "EventGraph": 74}
```

Per graph, after:

```
{"UserConstructionScript": 1, "Move": 11, "Aim": 5, "ToggleCameraView": 34, "RefreshHeldItem": 19, "EventGraph": 70}
```

EventGraph: **74 -> 70**, four nodes removed, none added. The four are
`K2Node_CallFunction_34`, `K2Node_CallFunction_33`, `K2Node_CallFunction_32` and
`K2Node_VariableGet_10`.

Every other graph is unchanged in node count: `Move`, `Aim`, `ToggleCameraView`,
`RefreshHeldItem` and `UserConstructionScript` were not touched, and the graph list itself is
unchanged:

```
before: ["UserConstructionScript", "Move", "Aim", "ToggleCameraView", "RefreshHeldItem", "EventGraph"]
after:  ["UserConstructionScript", "Move", "Aim", "ToggleCameraView", "RefreshHeldItem", "EventGraph"]
```

---

## 7. Whole-graph before/after set difference

Every graph in the Blueprint was dumped node by node - every node, every edge including
explicit `-> <none>`, every input pin value, each line prefixed with its graph name - and the
two dumps compared as line sets.

Lines present BEFORE but missing AFTER - i.e. every removal or alteration anywhere in the
Blueprint:

```
[EventGraph]   EDGE K2Node_BreakStruct_1.out1(RowName) -> K2Node_CallFunction_32.in2
[EventGraph]   EDGE K2Node_CallFunction_18.out0(then) -> K2Node_CallFunction_34.in0
[EventGraph]   EDGE K2Node_CallFunction_32.out0(ReturnValue) -> K2Node_CallFunction_33.in0
[EventGraph]   EDGE K2Node_CallFunction_33.out0(ReturnValue) -> K2Node_CallFunction_34.in1
[EventGraph]   EDGE K2Node_CallFunction_34.out0(then) -> K2Node_CallFunction_35.in0
[EventGraph]   EDGE K2Node_VariableGet_10.out0(FoundSlotIndex) -> K2Node_CallFunction_33.in2
[EventGraph]   VAL K2Node_CallFunction_25.in6(DrawDebugType) = ForDuration
[EventGraph]   VAL K2Node_CallFunction_32.in0(AppendTo) = 
[EventGraph]   VAL K2Node_CallFunction_32.in1(Prefix) = PICKED 
[EventGraph]   VAL K2Node_CallFunction_32.in2(InName) = None
[EventGraph]   VAL K2Node_CallFunction_32.in3(Suffix) =  -> slot 
[EventGraph]   VAL K2Node_CallFunction_33.in0(AppendTo) = 
[EventGraph]   VAL K2Node_CallFunction_33.in1(Prefix) = 
[EventGraph]   VAL K2Node_CallFunction_33.in2(InInt) = 0
[EventGraph]   VAL K2Node_CallFunction_33.in3(Suffix) = 
[EventGraph]   VAL K2Node_CallFunction_34.in0(execute) = 
[EventGraph]   VAL K2Node_CallFunction_34.in1(InString) = Hello
[EventGraph]   VAL K2Node_CallFunction_34.in2(bPrintToScreen) = true
[EventGraph]   VAL K2Node_CallFunction_34.in3(bPrintToLog) = true
[EventGraph]   VAL K2Node_CallFunction_34.in4(TextColor) = (R=0.000000,G=0.660000,B=1.000000,A=1.000000)
[EventGraph]   VAL K2Node_CallFunction_34.in5(Duration) = 3.0
[EventGraph]   VAL K2Node_CallFunction_34.in6(Key) = None
[EventGraph] NODE K2Node_CallFunction_32 type=Utilities|String|BuildString(Name) pos=320,640
[EventGraph] NODE K2Node_CallFunction_33 type=Utilities|String|BuildString(Integer) pos=600,640
[EventGraph] NODE K2Node_CallFunction_34 type=Development|PrintString pos=860,220
[EventGraph] NODE K2Node_VariableGet_10 type=|GetFoundSlotIndex pos=360,800
```

Lines present AFTER but not BEFORE - i.e. every addition:

```
[EventGraph]   EDGE K2Node_CallFunction_18.out0(then) -> K2Node_CallFunction_35.in0
[EventGraph]   VAL K2Node_CallFunction_25.in6(DrawDebugType) = None
```

Reading that list:

- Four `NODE` lines removed - exactly the three the command named plus `K2Node_VariableGet_10`,
  which step 3 authorised conditionally and whose condition was met.
- Every removed `VAL` line belongs to one of those four deleted nodes, with a single
  exception: `K2Node_CallFunction_25.in6(DrawDebugType) = ForDuration`, which is step 4's
  change and reappears on the added side as `= None`.
- Every removed `EDGE` line either belongs to a deleted node or is one of the two edges that
  had to break: `K2Node_BreakStruct_1.out1 -> K2Node_CallFunction_32.in2` (the deleted
  consumer) and `K2Node_CallFunction_18.out0 -> K2Node_CallFunction_34.in0` (replaced by the
  added direct edge to `K2Node_CallFunction_35.in0`).
- Two additions only: the re-route and the DrawDebugType value.
- No line belonging to the IA_UseItem chain, the BeginPlay attach chain, `RefreshHeldItem`,
  `Move`, `Aim`, `ToggleCameraView`, `UserConstructionScript`, `K2Node_BreakStruct_1` as a
  node, or `K2Node_CallFunction_36` appears in either set.

---

## 8. Variable list

Before (12), from `list_variables`:

```
["bIsFirstPerson", "FirstPersonPitchMin", "FirstPersonPitchMax", "ThirdPersonPitchMin", "ThirdPersonPitchMax", "InventorySlots", "SelectedSlot", "HeldItemSlot", "CurrentHP", "MaxHP", "InteractDistance", "FoundSlotIndex"]
```

After (12), from `list_variables`:

```
["bIsFirstPerson", "FirstPersonPitchMin", "FirstPersonPitchMax", "ThirdPersonPitchMin", "ThirdPersonPitchMax", "InventorySlots", "SelectedSlot", "HeldItemSlot", "CurrentHP", "MaxHP", "InteractDistance", "FoundSlotIndex"]
```

Identical. Nothing added, renamed or removed. In particular `FoundSlotIndex` is still
present - only one of its two getter nodes was deleted, not the variable. No variable default
was touched; this command issued no `set_properties` call at all.

---

## 9. Compile result

One compile was run in this command, with `warnings_as_errors: true`, and it did not raise.

Verbatim log line for this command's compile:

```
[2026.08.29-04.53.01:232][555]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
```

A regex sweep of the output log across 04.52 - 04.59 for `Warning|Error`, which covers the
deletions, the reconnection, the pin change, the compile and the save, returned an empty
list:

```
{"returnValue":[]}
```

No errors. No warnings. `save_assets` returned `true` and `is_dirty` afterwards returned
`false`.

### Warning and error lines seen, verbatim

No warning or error was produced by this command's Blueprint work. A wider sweep of the log
(04.40 - 04.59) did surface one unrelated warning family, recorded here verbatim because the
instruction asks for any warning line seen:

```
[2026.08.29-04.43.39:165][102]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c7a0, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.29-04.43.39:165][102]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+ae50, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.29-04.43.39:165][102]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+b300, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.29-04.43.39:165][102]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+ae30, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
```

Those are the editor terminal font lacking Hangul glyphs while rendering text in the Terminal
panel. They are a display-font condition of this environment, at 04.43, ten minutes before
this command's compile, and have nothing to do with the Blueprint. Truncated here to four
representative lines out of eight identical-shaped lines differing only in codepoint.

A separate historical family exists further back in the log, at 02.02.52, of the form
`LogBlueprint: Warning: No then pin found on node ...:EventGraph.K2Node_CallFunction_32` and
similar for `K2Node_CallFunction_33`, `K2Node_VariableGet_10`, `K2Node_VariableGet_9` and
others. Those are from a read-only graph traversal in an earlier session command - pure nodes
genuinely have no `then` pin - not from any compile, and not from this command. They are
noted because three of the nodes they name were deleted here.

---

## 10. On-disk file size

| | bytes | mtime |
|---|---|---|
| before | 482210 | Aug 29 12:01 |
| after  | 469014 | Aug 29 13:53 |

Delta: **-13196 bytes**. The file shrank, which is consistent with a deletion command.

Raw `ls -la` before:

```
-rw-r--r-- 1 a0108 197609 482210 Aug 29 12:01 /d/20260827/MCP1/Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

Raw `ls -la` after:

```
-rw-r--r-- 1 a0108 197609 469014 Aug 29 13:53 Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

`git status` after the save:

```
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonHUD.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonPlayerController.uasset
?? Docs/Terminal-Log/
```

The HUD and player controller entries are from earlier commands in this session and were not
touched here.

---

## 11. Places where a tool's response disagreed with the read-back

1. **Write calls return `null` on success, not `true`.**
   All four `delete_node` calls, the `connect_pins` call, the `set_pin_value` call and
   `compile_blueprint` all returned `null`. Read-back confirmed the four nodes are gone, the
   new edge exists, `DrawDebugType` reads `None`, and the Blueprint compiled. `null` here
   means success and the return value carries no information either way. By contrast
   `AssetTools.save_assets` returned `true`. None of these return values were used as
   evidence anywhere in this report.

2. **No other disagreement.** Every claim in this report was checked against a read-back
   after the compile and save, and each read-back matched what the write calls implied. In
   particular the enum literal written as the string `None` to `DrawDebugType` reads back as
   the string `None`, unchanged.

---

## 12. Not verified

No PIE run was performed. The following are unconfirmed at runtime:

- that picking an item up still works end to end - Set Array Elem, then RefreshHeldItem, then
  the pickup actor being destroyed - now that the print between the last two is gone
- that no red debug line is drawn on an interact trace any more
- that the "INVENTORY FULL" message still appears when the inventory is full

Only graph structure, the pin values on `K2Node_CallFunction_25`, and a clean compile are
established.
