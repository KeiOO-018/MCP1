# Selected item name and "[E] Use" prompt above the inventory bar - BP_ThirdPersonHUD

Date: 2026-08-29
Blueprint: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD`
Graph: `BP_ThirdPersonHUD:EventGraph` (Event Receive Draw HUD)

All node/pin facts below were read back with
`editor_toolset.toolsets.blueprint.BlueprintTools.get_node_infos` AFTER the compile and save.
None of them come from the return value of a write call.

---

## 1. On-disk file size

| | bytes | mtime |
|---|---|---|
| before | 239649 | Aug 29 12:27 |
| after  | 297982 | Aug 29 12:41 |

Delta: +58333 bytes.

Raw `ls -la` before:

```
-rw-r--r-- 1 a0108 197609 239649 Aug 29 12:27 Content/ThirdPerson/Blueprints/BP_ThirdPersonHUD.uasset
```

Raw `ls -la` after:

```
-rw-r--r-- 1 a0108 197609 297982 Aug 29 12:41 Content/ThirdPerson/Blueprints/BP_ThirdPersonHUD.uasset
```

---

## 2. Variable list

Before (12), from `list_variables`:

```
["SelectedSlot", "SlotCount", "SlotSize", "SlotGap", "BottomMargin", "BorderThickness", "ColorIdle", "ColorSelected", "CachedCharacter", "HPBarHeight", "ColorHPBack", "ColorHPFill"]
```

After (13), from `list_variables`:

```
["SelectedSlot", "SlotCount", "SlotSize", "SlotGap", "BottomMargin", "BorderThickness", "ColorIdle", "ColorSelected", "CachedCharacter", "HPBarHeight", "ColorHPBack", "ColorHPFill", "TextLineHeight"]
```

One variable added (`TextLineHeight`), none renamed, none removed. The twelve pre-existing
names are unchanged and in their original order.

### Variable creation calls (verbatim log from the batch script)

```
OK  add_variable TextLineHeight float -> null
OK  instance_editable TextLineHeight = True -> null
OK  compile after add_variable -> null
OK  set TextLineHeight = 24 -> true
```

---

## 3. TextLineHeight default read back from the class default object

Instance: `/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.Default__BP_ThirdPersonHUD_C`

Raw return of `ObjectTools.get_properties` after the compile and save:

```
{"TextLineHeight":24}
```

Requested 24, read back 24. Match.

`TextLineHeight` was created with `type_name: "float"`. In UE5 the Blueprint "float" type is
double-precision; the read-back Get node (`K2Node_VariableGet_46`) reports its output pin as
`Float (double-precision)`, which is the expected result, not a deviation.

### Instance Editable - could NOT be read back

`set_variable_instance_editable(..., instance_editable: True)` was called and returned
without error. There is no corresponding getter in this toolset: `BlueprintTools` exposes
`get_variable_category` and `get_variable_replication` but no
`get_variable_instance_editable`. **The Instance Editable flag therefore rests on the write
call succeeding and was not independently verified by a read-back.** This is the only
unverified claim in this report.

---

## 4. Reused existing nodes

Each was confirmed by its pin connections, read back before use.

### BAR_X

refPath:

```
/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD:EventGraph.K2Node_PromotableOperator_5
```

Type `Math|Float|float-float` at pos 4480,0.

How confirmed: its `in0 (A)` comes from `K2Node_PromotableOperator_3`
(`Math|Float|float/float`, = SizeX / 2) and its `in1 (B)` comes from
`K2Node_PromotableOperator_4` (`Math|Float|float/float`, = BAR_W / 2), i.e. it computes
`SizeX/2 - BAR_W/2`. Before this command its output already fed
`K2Node_PromotableOperator_12.in0`, `K2Node_CallFunction_19.in3` and
`K2Node_CallFunction_20.in3` - the ScreenX of the slot row and of both HP bar rects.

### SLOT_TOP

refPath:

```
/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD:EventGraph.K2Node_PromotableOperator_7
```

Type `Math|Float|float-float` at pos 5040,0.

How confirmed: its output feeds `K2Node_CallFunction_6.in4`, which is the ScreenY of the
first slot DrawRect, i.e. the top edge of the slot row.

### CHARACTER

refPath:

```
/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD:EventGraph.K2Node_VariableGet_17
```

Type `|GetCachedCharacter` at pos 7560,420.

How confirmed: there are exactly two Gets of CachedCharacter in the graph.
`K2Node_VariableGet_16` (pos 200,-700) feeds `K2Node_MacroInstance_2.in1`, the IsValid gate.
`K2Node_VariableGet_17` is the one in the drawing region; before this command its output fed
`K2Node_VariableGet_18.in0` (GetSelectedSlot), `K2Node_VariableGet_28.in0`
(GetInventorySlots), `K2Node_VariableGet_39.in0` (GetMaxHP) and `K2Node_VariableGet_40.in0`
(GetCurrentHP).

### COLOR_IDLE

refPath:

```
/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD:EventGraph.K2Node_VariableGet_6
```

Type `|GetColorIdle` at pos 1960,0.

How confirmed: read back before use as

```
NODE K2Node_VariableGet_6 [|GetColorIdle] pos=1960,0
  OUT 0 ColorIdle (Linear Color Structure) -> ['K2Node_Select_0.in0']
```

i.e. it is the Get of ColorIdle feeding the Select node, on `Option 0`. It is the only Get of
ColorIdle in the graph.

### COLOR_SELECTED

refPath:

```
/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD:EventGraph.K2Node_VariableGet_7
```

Type `|GetColorSelected` at pos 2240,0.

How confirmed: read back before use as

```
NODE K2Node_VariableGet_7 [|GetColorSelected] pos=2240,0
  OUT 0 ColorSelected (Linear Color Structure) -> ['K2Node_Select_0.in1']
```

i.e. it is the Get of ColorSelected feeding the Select node, on `Option 1`. It is the only
Get of ColorSelected in the graph.

### Append point

`K2Node_CallFunction_20` (`HUD|DrawRect`, the HP fill rect at pos 8520,1700) had
`OUT 0 then (Exec) -> <none>` before this command. That is the pin the new chain was
appended to.

---

## 5. Every new node with its pin connections

Read back verbatim from `get_node_infos` after compile and save:

```
NODE K2Node_VariableGet_44 [|GetSelectedSlot] pos=7000,3200
  IN  0 self (BP Third Person Character Object Reference) <- ['K2Node_VariableGet_17.out0'] | val=
  OUT 0 SelectedSlot (Integer) -> ['K2Node_PromotableOperator_29.in0']
NODE K2Node_PromotableOperator_29 [Math|Integer|int-int] pos=7300,3200
  IN  0 A (Integer) <- ['K2Node_VariableGet_44.out0'] | val=
  IN  1 B (Integer) <- <none> | val=1
  OUT 0 ReturnValue (Integer) -> ['K2Node_GetArrayItem_2.in1', 'K2Node_PromotableOperator_30.in0', 'K2Node_PromotableOperator_31.in0']
NODE K2Node_VariableGet_45 [|GetInventorySlots] pos=7000,3360
  IN  0 self (BP Third Person Character Object Reference) <- ['K2Node_VariableGet_17.out0'] | val=
  OUT 0 InventorySlots (Array of Names) -> ['K2Node_CallArrayFunction_2.in0', 'K2Node_GetArrayItem_2.in0']
NODE K2Node_CallArrayFunction_2 [Utilities|Array|Length] pos=7300,3360
  IN  0 TargetArray (Array of Names) <- ['K2Node_VariableGet_45.out0'] | val=
  OUT 0 ReturnValue (Integer) -> ['K2Node_PromotableOperator_31.in1']
NODE K2Node_PromotableOperator_30 [Math|Integer|integer>=integer] pos=7600,3120
  IN  0 A (Integer) <- ['K2Node_PromotableOperator_29.out0'] | val=
  IN  1 B (Integer) <- <none> | val=0
  OUT 0 ReturnValue (Boolean) -> ['K2Node_CommutativeAssociativeBinaryOperator_0.in0']
NODE K2Node_PromotableOperator_31 [Math|Integer|integer<integer] pos=7600,3280
  IN  0 A (Integer) <- ['K2Node_PromotableOperator_29.out0'] | val=
  IN  1 B (Integer) <- ['K2Node_CallArrayFunction_2.out0'] | val=
  OUT 0 ReturnValue (Boolean) -> ['K2Node_CommutativeAssociativeBinaryOperator_0.in1']
NODE K2Node_CommutativeAssociativeBinaryOperator_0 [Math|Boolean|ANDBoolean] pos=7900,3200
  IN  0 A (Boolean) <- ['K2Node_PromotableOperator_30.out0'] | val=false
  IN  1 B (Boolean) <- ['K2Node_PromotableOperator_31.out0'] | val=false
  OUT 0 ReturnValue (Boolean) -> ['K2Node_IfThenElse_4.in1']
NODE K2Node_IfThenElse_4 [Utilities|FlowControl|Branch] pos=8200,2900
  IN  0 execute (Exec) <- ['K2Node_CallFunction_20.out0'] | val=
  IN  1 Condition (Boolean) <- ['K2Node_CommutativeAssociativeBinaryOperator_0.out0'] | val=true
  OUT 0 then (Exec) -> ['K2Node_IfThenElse_5.in0']
  OUT 1 else (Exec) -> <none>
NODE K2Node_GetArrayItem_2 [Utilities|Array|Get(acopy)] pos=7600,3460
  IN  0 Array (Array of Names) <- ['K2Node_VariableGet_45.out0'] | val=
  IN  1 Dimension 1 (Integer) <- ['K2Node_PromotableOperator_29.out0'] | val=0
  OUT 0 Output (Name) -> ['K2Node_PromotableOperator_32.in0', 'K2Node_GetDataTableRow_1.in2']
NODE K2Node_PromotableOperator_32 [Utilities|Name|NotEqual(Name)] pos=7900,3460
  IN  0 A (Name) <- ['K2Node_GetArrayItem_2.out0'] | val=
  IN  1 B (Name) <- <none> | val=None
  OUT 0 ReturnValue (Boolean) -> ['K2Node_IfThenElse_5.in1']
NODE K2Node_IfThenElse_5 [Utilities|FlowControl|Branch] pos=8500,2900
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_4.out0'] | val=
  IN  1 Condition (Boolean) <- ['K2Node_PromotableOperator_32.out0'] | val=true
  OUT 0 then (Exec) -> ['K2Node_GetDataTableRow_1.in0']
  OUT 1 else (Exec) -> <none>
NODE K2Node_GetDataTableRow_1 [Utilities|GetDataTableRowDT_Items] pos=8800,2900
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_5.out0'] | val=
  IN  1 DataTable (Data Table Object Reference) <- <none> | val=/Game/Inventory/DT_Items.DT_Items
  IN  2 RowName (Name) <- ['K2Node_GetArrayItem_2.out0'] | val=
  OUT 0 then (Exec) -> ['K2Node_CallFunction_23.in0']
  OUT 1 RowNotFound (Exec) -> <none>
  OUT 2 ReturnValue (S Item Def Structure) -> ['K2Node_BreakStruct_2.in0']
NODE K2Node_BreakStruct_2 [Utilities|Struct|BreakSItemDef] pos=9150,3100
  IN  0 S_ItemDef (S Item Def Structure (by ref)) <- ['K2Node_GetDataTableRow_1.out2'] | val=
  OUT 0 DisplayName_6_316658864C6896A7946669A06167DB4B (Text) -> ['K2Node_CallFunction_22.in0']
  OUT 1 IconColor_8_811E92F4435525896A5C83A65306CDB7 (Linear Color Structure) -> <none>
  OUT 2 Mesh_10_B54826BF409F07BBD3D6519BBEC71038 (Static Mesh Object Reference) -> <none>
  OUT 3 Nature_14_9CD81B334FEC2B43BD0CA9A8F85A6615 (E_ItemNature Enum) -> ['K2Node_EnumEquality_0.in0']
  OUT 4 HealAmount_13_1283CF0D45B72F35CA15BEAD35901B99 (Float (double-precision)) -> <none>
NODE K2Node_CallFunction_22 [Utilities|String|ToString(Text)] pos=9450,3220
  IN  0 InText (Text (by ref)) <- ['K2Node_BreakStruct_2.out0'] | val=
  OUT 0 ReturnValue (String) -> ['K2Node_CallFunction_23.in2']
NODE K2Node_VariableGet_46 [|GetTextLineHeight] pos=7000,3620
  OUT 0 TextLineHeight (Float (double-precision)) -> ['K2Node_PromotableOperator_33.in0', 'K2Node_PromotableOperator_35.in1']
NODE K2Node_PromotableOperator_33 [Math|Float|float*float] pos=7300,3620
  IN  0 A (Float (double-precision)) <- ['K2Node_VariableGet_46.out0'] | val=
  IN  1 B (Float (double-precision)) <- <none> | val=2
  OUT 0 ReturnValue (Float (double-precision)) -> ['K2Node_PromotableOperator_34.in1']
NODE K2Node_PromotableOperator_34 [Math|Float|float-float] pos=7600,3620
  IN  0 A (Float (double-precision)) <- ['K2Node_PromotableOperator_7.out0'] | val=
  IN  1 B (Float (double-precision)) <- ['K2Node_PromotableOperator_33.out0'] | val=
  OUT 0 ReturnValue (Float (double-precision)) -> ['K2Node_CallFunction_23.in5']
NODE K2Node_PromotableOperator_35 [Math|Float|float-float] pos=7600,3780
  IN  0 A (Float (double-precision)) <- ['K2Node_PromotableOperator_7.out0'] | val=
  IN  1 B (Float (double-precision)) <- ['K2Node_VariableGet_46.out0'] | val=
  OUT 0 ReturnValue (Float (double-precision)) -> ['K2Node_CallFunction_24.in5']
NODE K2Node_CallFunction_23 [HUD|DrawText] pos=9800,2900
  IN  0 execute (Exec) <- ['K2Node_GetDataTableRow_1.out0'] | val=
  IN  1 self (HUD Object Reference) <- <none> | val=
  IN  2 Text (String) <- ['K2Node_CallFunction_22.out0'] | val=
  IN  3 TextColor (Linear Color Structure) <- ['K2Node_VariableGet_6.out0'] | val=(R=0,G=0,B=0,A=1)
  IN  4 ScreenX (Float (single-precision)) <- ['K2Node_PromotableOperator_5.out0'] | val=0.0
  IN  5 ScreenY (Float (single-precision)) <- ['K2Node_PromotableOperator_34.out0'] | val=0.0
  IN  6 Font (Font Object Reference) <- <none> | val=
  IN  7 Scale (Float (single-precision)) <- <none> | val=1.000000
  IN  8 bScalePosition (Boolean) <- <none> | val=false
  OUT 0 then (Exec) -> ['K2Node_IfThenElse_6.in0']
NODE K2Node_EnumEquality_0 [Utilities|Enum|Equal(Enum)] pos=9450,3420
  IN  0 A (E_ItemNature Enum) <- ['K2Node_BreakStruct_2.out3'] | val=
  IN  1 B (E_ItemNature Enum) <- <none> | val=NewEnumerator1
  OUT 0 ReturnValue (Boolean) -> ['K2Node_IfThenElse_6.in1']
NODE K2Node_IfThenElse_6 [Utilities|FlowControl|Branch] pos=10200,2900
  IN  0 execute (Exec) <- ['K2Node_CallFunction_23.out0'] | val=
  IN  1 Condition (Boolean) <- ['K2Node_EnumEquality_0.out0'] | val=true
  OUT 0 then (Exec) -> ['K2Node_CallFunction_24.in0']
  OUT 1 else (Exec) -> <none>
NODE K2Node_CallFunction_24 [HUD|DrawText] pos=10550,2900
  IN  0 execute (Exec) <- ['K2Node_IfThenElse_6.out0'] | val=
  IN  1 self (HUD Object Reference) <- <none> | val=
  IN  2 Text (String) <- <none> | val=[E] Use
  IN  3 TextColor (Linear Color Structure) <- ['K2Node_VariableGet_7.out0'] | val=(R=0,G=0,B=0,A=1)
  IN  4 ScreenX (Float (single-precision)) <- ['K2Node_PromotableOperator_5.out0'] | val=0.0
  IN  5 ScreenY (Float (single-precision)) <- ['K2Node_PromotableOperator_35.out0'] | val=0.0
  IN  6 Font (Font Object Reference) <- <none> | val=
  IN  7 Scale (Float (single-precision)) <- <none> | val=1.000000
  IN  8 bScalePosition (Boolean) <- <none> | val=false
  OUT 0 then (Exec) -> <none>
```

22 new nodes. Node count in the graph went 76 -> 98.

Notes on shape, checked against the spec:

- Exec chain: `K2Node_CallFunction_20.then` -> Branch A (`K2Node_IfThenElse_4`) -> Branch B
  (`K2Node_IfThenElse_5`) -> Get Data Table Row (`K2Node_GetDataTableRow_1`) -> DrawText
  name (`K2Node_CallFunction_23`) -> Branch C (`K2Node_IfThenElse_6`) -> DrawText prompt
  (`K2Node_CallFunction_24`). It runs once per frame after the slot loop and the HP bar, not
  inside the loop.
- Branch A uses the AND node (`K2Node_CommutativeAssociativeBinaryOperator_0`); neither of
  its inputs reads the array. Branch B is nested inside Branch A's `then`, not ANDed with it,
  so the array is only read after the range check has passed.
- A single Subtract (`K2Node_PromotableOperator_29`, SEL) feeds all three consumers:
  `K2Node_GetArrayItem_2.in1`, `K2Node_PromotableOperator_30.in0`,
  `K2Node_PromotableOperator_31.in0`.
- A single Array Get (`K2Node_GetArrayItem_2`) feeds both Branch B's NotEqual
  (`K2Node_PromotableOperator_32.in0`) and the Get Data Table Row RowName pin
  (`K2Node_GetDataTableRow_1.in2`).
- Every "leave unconnected" pin is unconnected: `K2Node_IfThenElse_4.out1 (else)`,
  `K2Node_IfThenElse_5.out1 (else)`, `K2Node_GetDataTableRow_1.out1 (RowNotFound)`,
  `K2Node_IfThenElse_6.out1 (else)`.
- Arithmetic nodes created: exactly four, as specified - SEL
  (`K2Node_PromotableOperator_29`, `Math|Integer|int-int`, B = 1), TextLineHeight * 2
  (`K2Node_PromotableOperator_33`, `Math|Float|float*float`, B = 2), NAME_Y
  (`K2Node_PromotableOperator_34` = SLOT_TOP - (TextLineHeight * 2)), and USE_Y
  (`K2Node_PromotableOperator_35` = SLOT_TOP - TextLineHeight). The comparison nodes
  (`K2Node_PromotableOperator_30` >=, `K2Node_PromotableOperator_31` <,
  `K2Node_PromotableOperator_32` NotEqual(Name), `K2Node_EnumEquality_0` Equal(Enum)) are
  Branch conditions, not arithmetic.
- NAME_Y feeds only `K2Node_CallFunction_23.in5` (the name line). USE_Y feeds only
  `K2Node_CallFunction_24.in5` (the prompt line). The prompt therefore sits one
  TextLineHeight below the name, and the name two below SLOT_TOP.
- Both DrawText nodes take ScreenX from BAR_X (`K2Node_PromotableOperator_5`).
- `Font`, `Scale` and `bScalePosition` on both DrawText nodes were left at their node
  defaults, which already read back as Font unconnected/empty (None),
  `Scale = 1.000000`, `bScalePosition = false` - exactly the values the spec asked for. No
  write was issued to those three pins on either node.
- The `TextColor` pins on both new DrawText nodes show `val=(R=0,G=0,B=0,A=1)`. That is the
  inert literal default underneath a connected pin; the connection from
  `K2Node_VariableGet_6` / `K2Node_VariableGet_7` is what supplies the value.

### Where the ToString conversion sits

`K2Node_CallFunction_22` (`Utilities|String|ToString(Text)`) at pos 9450,3220 sits **between
the Break and the first DrawText**, on the data path only:

```
K2Node_BreakStruct_2.out0 (DisplayName_6_..., Text)
    -> K2Node_CallFunction_22.in0 (InText, Text (by ref))
K2Node_CallFunction_22.out0 (ReturnValue, String)
    -> K2Node_CallFunction_23.in2 (Text, String)
```

It is a pure node with no exec pins, so it does not sit in the execution chain; the exec
path runs `K2Node_GetDataTableRow_1.then -> K2Node_CallFunction_23`. The conversion is
needed because the Break's displayName output is a `Text` pin while `AHUD::DrawText` takes an
`FString`.

### The literal string stored in the Equal (Enum) pin

Read back from `K2Node_EnumEquality_0`:

```
NODE K2Node_EnumEquality_0 [Utilities|Enum|Equal(Enum)] pos=9450,3420
  IN  0 A (E_ItemNature Enum) <- ['K2Node_BreakStruct_2.out3'] | val=
  IN  1 B (E_ItemNature Enum) <- <none> | val=NewEnumerator1
  OUT 0 ReturnValue (Boolean) -> ['K2Node_IfThenElse_6.in1']
```

**The exact string stored in the literal pin `B` is `NewEnumerator1`.**

The index used is **1**. Reasons:

- E_ItemNature's declaration order is Key, Consumable, Holdable, so Consumable is index 1.
- E_ItemNature is a Blueprint UserDefinedEnum. Its *internal* entry names are
  `NewEnumerator0`, `NewEnumerator1`, `NewEnumerator2`, assigned in declaration order; the
  names shown in the editor (Key / Consumable / Holdable) are the separate display names
  held in DisplayNameMap. Enum literal pins store the internal name, so index 1 is written
  and read back as the string `NewEnumerator1`, not as `Consumable`.
- This matches the mapping established in the previous session command, where three
  independent checks agreed: (a) `Engine/Source/Editor/BlueprintGraph/Private/K2Node_SwitchEnum.cpp`
  lines 61-69 and 187-189 show pin names come from `Enum->GetNameStringByIndex(EnumIndex)`
  (internal name) and pins are created in declaration index order, while the editor label
  comes separately from `GetDisplayNameTextByIndex`; (b) the byte offsets of the strings
  inside `Content/Inventory/E_ItemNature.uasset` are `NewEnumerator0` @ 595,
  `NewEnumerator1` @ 632, `NewEnumerator2` @ 669 and `Key` @ 1050, `Consumable` @ 1215,
  `Holdable` @ 1387 - the same relative order in both blocks; (c) the stated declaration
  order.

The value was written as the string `NewEnumerator1` and read back unchanged as
`NewEnumerator1`.

---

## 6. Whole-graph before/after set difference

The full graph (every node, every edge including explicit `-> <none>`, every input pin value)
was dumped before and after and compared as line sets.

Lines present BEFORE but missing AFTER - i.e. every removal or alteration in the entire graph:

```
  EDGE K2Node_CallFunction_20.out0(then) -> <none>
```

That is the complete list: one line, and it is the intended change - the append point.
119 lines were added. Nothing else in the graph was removed or altered.

The reused nodes gained additional outgoing links (fan-out), which is additive and appears
only on the added side. Read back after compile and save:

```
NODE K2Node_CallFunction_20 [HUD|DrawRect] pos=8520,1700
  IN  0 execute (Exec) <- ['K2Node_CallFunction_19.out0'] | val=
  IN  1 self (HUD Object Reference) <- <none> | val=
  IN  2 RectColor (Linear Color Structure) <- ['K2Node_VariableGet_43.out0'] | val=(R=0,G=0,B=0,A=1)
  IN  3 ScreenX (Float (single-precision)) <- ['K2Node_PromotableOperator_5.out0'] | val=0.0
  IN  4 ScreenY (Float (single-precision)) <- ['K2Node_PromotableOperator_28.out0'] | val=0.0
  IN  5 ScreenW (Float (single-precision)) <- ['K2Node_PromotableOperator_26.out0'] | val=0.0
  IN  6 ScreenH (Float (single-precision)) <- ['K2Node_VariableGet_41.out0'] | val=0.0
  OUT 0 then (Exec) -> ['K2Node_IfThenElse_4.in0']
NODE K2Node_PromotableOperator_5 [Math|Float|float-float] pos=4480,0
  IN  0 A (Float (double-precision)) <- ['K2Node_PromotableOperator_3.out0'] | val=
  IN  1 B (Float (double-precision)) <- ['K2Node_PromotableOperator_4.out0'] | val=
  OUT 0 ReturnValue (Float (double-precision)) -> ['K2Node_PromotableOperator_12.in0', 'K2Node_CallFunction_19.in3', 'K2Node_CallFunction_20.in3', 'K2Node_CallFunction_23.in4', 'K2Node_CallFunction_24.in4']
NODE K2Node_PromotableOperator_7 [Math|Float|float-float] pos=5040,0
  IN  0 A (Float (double-precision)) <- ['K2Node_PromotableOperator_6.out0'] | val=
  IN  1 B (Float (double-precision)) <- ['K2Node_VariableGet_0.out0'] | val=
  OUT 0 ReturnValue (Float (double-precision)) -> ['K2Node_CallFunction_6.in4', 'K2Node_PromotableOperator_15.in0', 'K2Node_PromotableOperator_17.in0', 'K2Node_PromotableOperator_20.in0', 'K2Node_PromotableOperator_27.in0', 'K2Node_PromotableOperator_34.in0', 'K2Node_PromotableOperator_35.in0']
NODE K2Node_VariableGet_17 [|GetCachedCharacter] pos=7560,420
  OUT 0 CachedCharacter (BP Third Person Character Object Reference) -> ['K2Node_VariableGet_18.in0', 'K2Node_VariableGet_28.in0', 'K2Node_VariableGet_39.in0', 'K2Node_VariableGet_40.in0', 'K2Node_VariableGet_44.in0', 'K2Node_VariableGet_45.in0']
NODE K2Node_VariableGet_6 [|GetColorIdle] pos=1960,0
  OUT 0 ColorIdle (Linear Color Structure) -> ['K2Node_Select_0.in0', 'K2Node_CallFunction_23.in3']
NODE K2Node_VariableGet_7 [|GetColorSelected] pos=2240,0
  OUT 0 ColorSelected (Linear Color Structure) -> ['K2Node_Select_0.in1', 'K2Node_CallFunction_24.in3']
```

In each case every pre-existing target is still present and in its original order; only new
targets were appended. `K2Node_CallFunction_20`'s seven input pins and their values are
identical to before; only its `then` output changed, which is the append point.

`K2Node_Select_0.in0` and `.in1` still receive ColorIdle and ColorSelected respectively, so
the slot border color logic is untouched.

---

## 7. Compile result

Two compiles were run in this command, both with `warnings_as_errors: true`, and neither
raised:

1. after adding `TextLineHeight`
2. after wiring the graph

Verbatim log lines for this command's compiles:

```
[2026.08.29-03.40.22:153][711]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD'
[2026.08.29-03.41.35:979][932]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD.BP_ThirdPersonHUD'
```

A regex sweep of the output log across 03.35 - 03.59 for `Warning|Error`, which covers both
compiles and the save, returned an empty list:

```
{"returnValue":[]}
```

No errors. No warnings from the compile. `save_assets` returned `true` and `is_dirty`
afterwards returned `false`.

### Warning and error lines seen, verbatim

No warning or error was produced by this command's Blueprint work. A wider sweep of the log
(03.00 - 03.59) did surface two unrelated warning families, recorded here verbatim because
the instruction asks for any warning line seen:

```
[2026.08.29-03.00.10:250][294]LogScript: Warning: GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: DisplayNameMap
[2026.08.29-03.00.10:584][295]LogScript: Warning: GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: Names
[2026.08.29-03.00.10:919][296]LogScript: Warning: GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: NamesAndValues
[2026.08.29-03.00.11:251][297]LogScript: Warning: GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: EnumDisplayNameFn
[2026.08.29-03.00.11:252][297]LogScript: Warning: GetObjectProperties on '/Game/Inventory/E_ItemNature.E_ItemNature' (UserDefinedEnum): the following properties could not be read: CppForm
```

Those five are from the PREVIOUS command (03.00), where the enum asset's properties were
probed read-only to establish the enumerator mapping. They confirm that
`ObjectTools.get_properties` cannot read any property on a `UserDefinedEnum`, which is why
this command relied on the already-established mapping rather than re-probing.

```
[2026.08.29-03.32.24:958][396]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+b85c, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.29-03.32.24:959][396]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+bc14, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.29-03.32.24:959][396]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+d655, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.29-03.32.24:959][396]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c778, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
```

Those are the editor terminal font lacking Hangul glyphs while rendering text in the
Terminal panel. They are a display-font condition of this environment, at 03.32, before this
command's compiles, and have nothing to do with the Blueprint. Truncated here to four
representative lines out of roughly thirty identical-shaped lines differing only in
codepoint.

---

## 8. Places where a tool's response disagreed with the read-back

1. **Write calls return `null` on success, not `true`.**
   `add_variable`, `set_variable_instance_editable` and `compile_blueprint` all returned
   `null`. Read-back confirmed the variable exists with the requested type and that the
   Blueprint compiled. So `null` here means success and the return value carries no
   information either way. By contrast `ObjectTools.set_properties` and
   `AssetTools.save_assets` both returned `true`. None of these return values were used as
   evidence anywhere in this report.

2. **Instance Editable cannot be read back.**
   There is no `get_variable_instance_editable` in `BlueprintTools`. The flag was set by a
   write call that returned `null` (see item 1), so its state is asserted, not verified.
   This is the only unverified claim in this report.

3. **`find_node_types` filter "E_ItemNature" does not surface the enum comparison node.**
   Filtering on `E_ItemNature` returned only `BytetoEnum`, `Literalenum`, `ForEach`,
   `Getnumberofentriesin` and `Switchon` variants. The node actually needed is registered
   under the generic id `Utilities|Enum|Equal(Enum)` and was only found by filtering on
   `Equal`. Not a wrong answer from the tool, but the obvious filter does not find it.

4. **`Utilities|Enum|Equal(Enum)` is created with Wildcard pins.**
   Immediately after `create_node` the node read back as
   `IN 0:A:Wildcard= | 1:B:Wildcard=`. Both pins resolved to `E_ItemNature Enum` only after
   `A` was connected to the Break's Nature output. The literal on `B` was therefore set
   after that connection, and read back correctly as `NewEnumerator1`.

5. **`type_name: "float"` produces a double-precision pin.**
   `TextLineHeight` was requested as `float`; the created Get node reports
   `Float (double-precision)`. This is UE5's normal Blueprint float, not a mismatch.

6. **Not a tool disagreement, recorded as an environment note:**
   The Bash working directory persisted from a previous command into `Docs/Terminal-Log`,
   which made a relative `ls Content/...` fail once with
   `ls: cannot access 'Content/ThirdPerson/Blueprints/BP_ThirdPersonHUD.uasset': No such file or directory`
   and made `git status` print paths as `../../Content/...`. This was a shell-state issue on
   my side, corrected by using absolute paths; it did not affect any Blueprint operation or
   any figure in this report. The before-size figure of 239649 bytes is the after-size
   recorded in the previous command's report for the same file and mtime.

---

## 9. Not verified

No PIE run was performed. The following are unconfirmed at runtime:

- that the item name and the "[E] Use" prompt actually appear above the inventory bar
- that NAME_Y and USE_Y place the two lines where intended on screen, and that they do not
  overlap the slot row or run off the top of the viewport
- that the name text renders correctly through the Text -> String conversion
- that the prompt appears only for Consumable items and not for Key or Holdable - this is
  the check that would directly confirm the `NewEnumerator1` mapping in the running game
- that nothing is drawn when the selected slot is empty, out of range, or when the row is
  missing from DT_Items

Only graph topology, the variable default on the CDO, and a clean compile are established.
