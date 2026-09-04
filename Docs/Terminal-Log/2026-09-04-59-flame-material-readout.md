# 2026-09-04-59 · M_Flame readout — why the flame renders white

Read-only investigation. Nothing was written: no `set_properties`, no `connect_*`, no
`disconnect_*`, no `recompile`, no `save_assets`. Every call below is a read.

**Headline: the material graph is wired correctly and the material is assigned correctly. The
white is not a broken connection. `FlameBrightness` defaults to 30, so the emissive value the
material outputs is `(30, 13.5, 3.6)` — far past the point where the tonemapper desaturates it to
white.** Full evidence below; the reasoning is in section 6.

---

## 0 · PIE state

```
call: EditorToolset.EditorAppToolset.IsPIERunning
args: {}
```

```
{"returnValue":false}
```

**No PIE session is running.** Every actor read below therefore hit the editor world. No
`refPath` in this log carries a `UEDPIE_0_` prefix, which is the second confirmation.

---

## 1 · The M_Flame node graph

```
call: editor_toolset.toolsets.asset.AssetTools.exists
args: {"path": "/Game/LevelPrototyping/Materials/M_Flame"}
```

```
{"returnValue":true}
```

### Every node

```
call: editor_toolset.toolsets.material.MaterialTools.get_expressions
args: {"material_or_function": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame"}}
```

```
{"returnValue":[{"refPath":"/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionVectorParameter_0"},{"refPath":"/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionScalarParameter_0"},{"refPath":"/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionMultiply_0"}]}
```

Three nodes. That is the entire graph.

### Every node's type, pins, and input wiring

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: get_class / get_expression_input_names / get_expression_output_names / get_expression_inputs for each of the three nodes
```

```
{"MaterialExpressionVectorParameter_0": {"class": {"refPath": "/Script/Engine.MaterialExpressionVectorParameter"}, "input_pins": [], "output_pins": ["RGB", "R", "G", "B", "A", "RGBA"], "input_wiring": []}, "MaterialExpressionScalarParameter_0": {"class": {"refPath": "/Script/Engine.MaterialExpressionScalarParameter"}, "input_pins": [], "output_pins": [""], "input_wiring": []}, "MaterialExpressionMultiply_0": {"class": {"refPath": "/Script/Engine.MaterialExpressionMultiply"}, "input_pins": ["A", "B"], "output_pins": [""], "input_wiring": [{"output_name": "RGB", "expression": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionVectorParameter_0"}, "input_name": "A"}, {"output_name": "", "expression": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionScalarParameter_0"}, "input_name": "B"}]}}
```

The Multiply node's wiring read on its own, so it is not buried inside a script result:

```
call: editor_toolset.toolsets.material.MaterialTools.get_expression_inputs
args: {"material_or_function": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame"}, "expression": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionMultiply_0"}}
```

```
{"returnValue":[{"output_name":"RGB","expression":{"refPath":"/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionVectorParameter_0"},"input_name":"A"},{"output_name":"","expression":{"refPath":"/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionScalarParameter_0"},"input_name":"B"}]}
```

### What is plugged into Emissive Color

```
call: editor_toolset.toolsets.material.MaterialTools.get_property_input
args: {"material": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame"}, "material_property": "MP_EmissiveColor"}
```

```
{"returnValue":{"output_name":"","expression":{"refPath":"/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionMultiply_0"},"input_name":""}}
```

**Emissive Color is driven by `MaterialExpressionMultiply_0`.** It is connected, not empty.

### Every other material output property

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: get_property_input for each of 13 material properties
```

```
{"MP_EmissiveColor": {"output_name": "", "expression": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionMultiply_0"}, "input_name": ""}, "MP_BaseColor": {"output_name": "", "expression": "None", "input_name": ""}, "MP_Metallic": {"output_name": "", "expression": "None", "input_name": ""}, "MP_Specular": {"output_name": "", "expression": "None", "input_name": ""}, "MP_Roughness": {"output_name": "", "expression": "None", "input_name": ""}, "MP_Normal": {"output_name": "", "expression": "None", "input_name": ""}, "MP_Opacity": {"output_name": "", "expression": "None", "input_name": ""}, "MP_OpacityMask": {"output_name": "", "expression": "None", "input_name": ""}, "MP_AmbientOcclusion": {"output_name": "", "expression": "None", "input_name": ""}, "MP_WorldPositionOffset": {"output_name": "", "expression": "None", "input_name": ""}, "MP_Refraction": {"output_name": "", "expression": "None", "input_name": ""}, "MP_ShadingModel": {"ERROR": "ToolsetRegistry: TypeError: function: Failed to convert argument at pos '2' when calling function 'get_property_input' on 'MaterialTools'\n  TypeError: PythonizeProperty: Cannot pythonize 'material_property' (ByteProperty)\n    TypeError: PythonizeEnumEntry: Cannot pythonize '29' (int64) as 'MaterialProperty'"}, "MP_MaterialAttributes": {"output_name": "", "expression": "None", "input_name": ""}}
```

`MP_ShadingModel` **could not be read** — the enum value 29 fails to convert on the way into the
tool. That one property is unknown; every other output is disconnected. (The material's
`ShadingModel` field itself is readable and is reported in section 3.)

### The graph, written out

```
  VectorParameter "FlameColor"          ScalarParameter "FlameBrightness"
  (-500, 0)                             (-500, 220)
  out pins: RGB R G B A RGBA            out pin: (unnamed)
        |                                     |
        | RGB                                 | (unnamed)
        v                                     v
       [A]                                   [B]
        \                                    /
         \                                  /
          Multiply  (MaterialExpressionMultiply_0, at -200, 60)
          ConstA=0  ConstB=1  (both unused: A and B are both wired)
                    |
                    | (unnamed output)
                    v
          M_Flame  ->  Emissive Color   (MP_EmissiveColor)

  Base Color, Metallic, Specular, Roughness, Normal, Opacity, Opacity Mask,
  Ambient Occlusion, World Position Offset, Refraction, Material Attributes:
  all disconnected.  Shading Model input: could not be read (see error above).
```

**FlameColor and FlameBrightness both reach Emissive Color.** There is no missing connection.

---

## 2 · Parameter defaults and types

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionVectorParameter_0"}, "properties": ["ParameterName", "DefaultValue", "Group", "SortPriority", "MaterialExpressionEditorX", "MaterialExpressionEditorY", "Desc"]}
```

```
{"returnValue":"{\"ParameterName\":\"FlameColor\",\"DefaultValue\":{\"r\":1,\"g\":0.44999998807907104,\"b\":0.11999999731779099,\"a\":1},\"Group\":\"None\",\"SortPriority\":32,\"MaterialExpressionEditorX\":-500,\"MaterialExpressionEditorY\":0,\"Desc\":\"\"}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionScalarParameter_0"}, "properties": ["ParameterName", "DefaultValue", "Group", "SortPriority", "SliderMin", "SliderMax", "MaterialExpressionEditorX", "MaterialExpressionEditorY", "Desc"]}
```

```
{"returnValue":"{\"ParameterName\":\"FlameBrightness\",\"DefaultValue\":30,\"Group\":\"None\",\"SortPriority\":32,\"SliderMin\":0,\"SliderMax\":0,\"MaterialExpressionEditorX\":-500,\"MaterialExpressionEditorY\":220,\"Desc\":\"\"}"}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionMultiply_0"}, "properties": ["ConstA", "ConstB", "MaterialExpressionEditorX", "MaterialExpressionEditorY", "Desc"]}
```

```
{"returnValue":"{\"ConstA\":0,\"ConstB\":1,\"MaterialExpressionEditorX\":-200,\"MaterialExpressionEditorY\":60,\"Desc\":\"\"}"}
```

| Parameter | Type (UClass) | Default | Group |
| --- | --- | --- | --- |
| `FlameColor` | `MaterialExpressionVectorParameter` (Vector / LinearColor) | r 1, g 0.44999998807907104, b 0.11999999731779099, a 1 | `None` |
| `FlameBrightness` | `MaterialExpressionScalarParameter` (Scalar / float) | 30 | `None` |

`SliderMin` and `SliderMax` on FlameBrightness are both 0, meaning no slider range was set.
The Multiply node's `ConstA` / `ConstB` are 0 and 1 but both pins are wired, so neither constant
is used.

---

## 3 · M_Flame material settings

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame"}, "properties": ["ShadingModel", "BlendMode", "TwoSided", "bUsedWithStaticLighting", "bUsedWithSkeletalMesh", "bUsedWithParticleSprites", "bUsedWithInstancedStaticMeshes", "bCastDynamicShadowAsMasked", "OpacityMaskClipValue", "bUseEmissiveForDynamicAreaLighting", "MaterialDomain", "bTangentSpaceNormal", "bFullyRough", "bUsedAsSpecialEngineMaterial"]}
```

```
GetObjectProperties on '/Game/LevelPrototyping/Materials/M_Flame.M_Flame' (Material): the following properties could not be read: bUsedAsSpecialEngineMaterial
```

One bad name aborts the whole call — the same behaviour recorded in log 2026-09-04-56 for
`CastShadow` on a PointLightComponent. Re-sent without it:

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame"}, "properties": ["ShadingModel", "BlendMode", "TwoSided", "bUsedWithStaticLighting", "bUsedWithSkeletalMesh", "bUsedWithParticleSprites", "bUsedWithInstancedStaticMeshes", "bCastDynamicShadowAsMasked", "OpacityMaskClipValue", "bUseEmissiveForDynamicAreaLighting", "MaterialDomain", "bTangentSpaceNormal", "bFullyRough"]}
```

```
{"returnValue":"{\"ShadingModel\":\"MSM_Unlit\",\"BlendMode\":\"BLEND_Opaque\",\"TwoSided\":false,\"bUsedWithStaticLighting\":false,\"bUsedWithSkeletalMesh\":false,\"bUsedWithParticleSprites\":false,\"bUsedWithInstancedStaticMeshes\":false,\"bCastDynamicShadowAsMasked\":false,\"OpacityMaskClipValue\":0.33329999446868896,\"bUseEmissiveForDynamicAreaLighting\":false,\"MaterialDomain\":\"MD_Surface\",\"bTangentSpaceNormal\":true,\"bFullyRough\":false}"}
```

There is a `bUsedWithStaticMesh` flag on Material in UE 5.8. Found by listing the property names
rather than assuming:

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: list_properties on M_Flame, filtered to names containing "UsedWith" or "usage"
```

```
{"total_properties": 128, "used_with_properties": ["bUsedWithSkeletalMesh", "bUsedWithMeshDeformer", "bUsedWithEditorCompositing", "bUsedWithParticleSprites", "bUsedWithBeamTrails", "bUsedWithMeshParticles", "bUsedWithNiagaraSprites", "bUsedWithNiagaraRibbons", "bUsedWithNiagaraMeshParticles", "bUsedWithGeometryCache", "bUsedWithStaticLighting", "bUsedWithMorphTargets", "bUsedWithSplineMeshes", "bUsedWithInstancedStaticMeshes", "bUsedWithGeometryCollections", "bUsedWithClothing", "bUsedWithWater", "bUsedWithHairStrands", "bUsedWithLidarPointCloud", "bUsedWithVirtualHeightfieldMesh", "bUsedWithNanite", "bUsedWithVoxels", "bUsedWithCurves", "bUsedWithVolumetricCloud", "bUsedWithHeterogeneousVolumes", "bUsedWithInstancedSkinnedMesh", "bUsedWithStaticMesh", "bAutomaticallySetUsageInEditor", "bUsedWithNeuralNetworks"]}
```

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame"}, "properties": ["bUsedWithStaticMesh", "bAutomaticallySetUsageInEditor", "bUsedWithNanite", "bUsedWithSplineMeshes"]}
```

```
{"returnValue":"{\"bUsedWithStaticMesh\":true,\"bAutomaticallySetUsageInEditor\":true,\"bUsedWithNanite\":false,\"bUsedWithSplineMeshes\":false}"}
```

| Setting | Value |
| --- | --- |
| Shading Model | `MSM_Unlit` |
| Blend Mode | `BLEND_Opaque` |
| Two Sided | `false` |
| Used with Static Meshes (`bUsedWithStaticMesh`) | **`true`** |
| Material Domain | `MD_Surface` |
| Automatically Set Usage In Editor | `true` |

Unlit is the right shading model for a self-lit flame, and with Unlit the only channel that
renders is Emissive Color — which is the one channel that is connected. Nothing here is wrong.

---

## 4 · Material actually assigned to the Flame component

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Flame_GEN_VARIABLE"}, "properties": ["StaticMesh", "OverrideMaterials", "RelativeScale3D", "RelativeLocation", "RelativeRotation", "CastShadow", "Mobility", "bVisible"]}
```

```
{"returnValue":"{\"StaticMesh\":{\"refPath\":\"/Engine/BasicShapes/Cone.Cone\"},\"OverrideMaterials\":[{\"refPath\":\"/Game/LevelPrototyping/Materials/M_Flame.M_Flame\"}],\"RelativeScale3D\":{\"x\":0.17999999999999999,\"y\":0.17999999999999999,\"z\":0.30000004577637418},\"RelativeLocation\":{\"x\":0,\"y\":0,\"z\":-14},\"RelativeRotation\":{\"pitch\":0,\"yaw\":0,\"roll\":0},\"CastShadow\":false,\"Mobility\":\"Movable\",\"bVisible\":true}"}
```

**`OverrideMaterials[0]` is `/Game/LevelPrototyping/Materials/M_Flame.M_Flame`.** It *is*
M_Flame — the assignment is correct, not some leftover default material.

Supplementary read, not asked for but cheap and relevant: the same component on a placed actor,
to rule out a per-instance material override:

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Flame"}, "properties": ["StaticMesh", "OverrideMaterials", "RelativeScale3D", "RelativeLocation"]}
```

```
{"returnValue":"{\"StaticMesh\":{\"refPath\":\"/Engine/BasicShapes/Cone.Cone\"},\"OverrideMaterials\":[{\"refPath\":\"/Game/LevelPrototyping/Materials/M_Flame.M_Flame\"}],\"RelativeScale3D\":{\"x\":0.17999999999999999,\"y\":0.17999999999999999,\"z\":0.30000004577637418},\"RelativeLocation\":{\"x\":0,\"y\":0,\"z\":-14}}"}
```

Identical to the class template. No per-instance override.

### Does any material instance of M_Flame exist in /Game?

```
call: editor_toolset.toolsets.asset.AssetTools.get_referencers
args: {"asset_path": "/Game/LevelPrototyping/Materials/M_Flame"}
```

```
{"returnValue":["/Game/Interaction/BP_Torch"]}
```

```
call: editor_toolset.toolsets.asset.AssetTools.find_assets
args: {"folder_path": "/Game", "name": "", "recursive": true, "asset_type": {"refPath": "/Script/Engine.MaterialInstanceConstant"}}
```

```
{"returnValue":["/Game/LevelPrototyping/Materials/MI_Castle_Wood","/Game/Characters/Mannequins/Materials/Quinn/MI_Quinn_01","/Game/Characters/Mannequins/Materials/Quinn/MI_Quinn_02","/Game/Characters/Mannequins/Materials/Manny/MI_Manny_01_New","/Game/Characters/Mannequins/Materials/Manny/MI_Manny_02_New","/Game/LevelPrototyping/Materials/MI_Castle_Stone","/Game/ThirdPerson/MI_ThirdPersonColWay","/Game/LevelPrototyping/Materials/MI_PrototypeGrid_TopDark","/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_Round","/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray_02","/Game/LevelPrototyping/Materials/MI_PrototypeGrid_Gray","/Game/LevelPrototyping/Materials/MI_DefaultColorway","/Game/LevelPrototyping/Interactable/JumpPad/Assets/Materials/MI_GlowNT"]}
```

**No material instance of M_Flame exists anywhere in /Game.** There are 13 MaterialInstanceConstant
assets in the project and none of them is parented to M_Flame — `get_referencers` on M_Flame
returns exactly one referencer, `/Game/Interaction/BP_Torch`, and a child material instance would
have to appear in that list.

---

## 5 · Flame component mesh and transform on the BP_Torch class template

From the same `get_properties` response quoted in section 4:

| Property | Value |
| --- | --- |
| StaticMesh | `/Engine/BasicShapes/Cone.Cone` |
| RelativeScale3D | x 0.17999999999999999, y 0.17999999999999999, z 0.30000004577637418 |
| RelativeLocation | x 0, y 0, z -14 |
| RelativeRotation | pitch 0, yaw 0, roll 0 |
| CastShadow | false |
| Mobility | Movable |
| bVisible | true |

The flame is an engine Cone scaled to 18% × 18% × 30%, sitting 14 units *below* the component's
parent origin.

---

## 6 · Reading of the evidence

Everything the question suspected turns out to be fine:

- Emissive Color **is** connected.
- FlameColor and FlameBrightness **both** reach it, through the Multiply.
- The assigned material **is** M_Flame, on both the class template and a placed actor.
- Shading model Unlit is correct for this, and Unlit renders only Emissive.
- No stray material instance is shadowing anything.

What is left is the arithmetic. The material outputs

```
Emissive = FlameColor.RGB * FlameBrightness
         = (1, 0.45, 0.12) * 30
         = (30, 13.5, 3.6)
```

All three channels are far above 1.0, and the ratio between them survives the multiply — the
colour is still orange in linear space. But the scene tonemapper maps that range toward the top of
the display curve, where the channels converge, and bloom spreads the brightest pixels outward.
An emissive of 30 on a small object is the standard recipe for a white core with a coloured
fringe. The perceived hue at these values comes from the *shape* of the falloff, not from the
parameter.

That is a reading of the numbers, **not something verified on screen.** Nothing in this task
rendered or measured a pixel. Confirming it would mean lowering FlameBrightness — 2 to 5 is the
usual range where an unlit emissive keeps its hue — and looking at the result, or capturing the
viewport. Both are writes or renders, and this task was read-only.

One loose end: `MP_ShadingModel`'s input could not be read at all (the enum conversion error in
section 1). The material's `ShadingModel` field says `MSM_Unlit`, but whether something is wired
into the Shading Model *input pin* is unknown. With only three nodes in the graph and both
parameters accounted for, there is nothing left that could be driving it, so this is very likely
nothing — but it was not verified and is recorded as unverified.

---

## What was not done

No write of any kind. `git status` was not disturbed by this task; the only calls were
`exists`, `get_expressions`, `get_property_input`, `get_expression_inputs`,
`get_expression_input_names`, `get_expression_output_names`, `get_class`, `list_properties`,
`get_properties`, `get_referencers`, `find_assets`, and `IsPIERunning`.
