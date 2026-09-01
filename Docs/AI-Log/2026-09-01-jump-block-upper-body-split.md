# 2026-09-01

## 작업물

`AttackHit` 노티파이를 타격 프레임으로 옮기고, 공격 중 양방향 점프 금지를 만들고, 플레이어만 상하체를 분리하고, 적 복귀를 비래턴트로 바꿨다.

**소요 시간**: 약 2시간 25분 (17:20 ~ 19:43)

## 명령

### 한글

```
작업 준비
```

```
순서대로하자
```

```
했어
```

```
했어
```

```
이거야?
```
(이미지 첨부 — `AM_Player_Attack` 몽타주 에디터, Notifies 트랙의 `AttackHit`이 눈금 1 근처)

```
이거바바
```
(이미지 첨부 — 스크러버가 `11* (0.40) (39.65%)`, 캐릭터가 팔을 뻗은 자세)

```
오른팔임
```

```
했어
```

```
했어 확인좀
```

```
1. 팔이 휘둘릴 때 나옴
2. 다리 정지 거슬림 
3. 앞으로 밀림

공격할 때 점프 못하게 해야할지도
```

(AskUserQuestion 4문항 답변)
```
공격 중 점프 금지 — 어디까지 막을까?     → 양방향으로 막기
공격 중 앞으로 밀리는 것은 어떻게 할까?   → 아직 모르겠다 — 분리 후에 보고 정한다
상체를 어느 본부터 가를까?                → spine_01 (허리부터)
이번 세션에서 어디까지 갈까?              → 점프 금지 먼저, 그 다음 상하체 분리
```

```
하자
```

```
결과 확인
```

(Terminal 에이전트 보고 원문 붙여넣기 — `IsValid` 순수 함수 생성 실패)

```
이거 맞아? CanJump는 있는데 CanJumpInternal 이거 다시 봐줘
```
(이미지 첨부 — `CanJump (const)` 그래프, Entry와 Return Node만 있고 `Return Value` 미연결)

```
이렇게?
```
(이미지 첨부 — `Parent: CanJump`가 붙고 컴파일 성공 메시지)

```
결과 확인
```

```
점프한 상태로 공격 되는건 아직 안한거지? 나머지 1에서 3까진 다 잘 됨
```

```
결과 확인
```

```
3번 이랑 너가 말해준거 이상없음
```

```
저장했으
```

```
하자
```

```
했어 확인좀
```

```
했어
```

```
했어 확인좀
```

```
결과 확인
```

(Terminal 에이전트 보고 원문 붙여넣기 — `Use Cached Pose` 생성 실패, 컴파일 요구)

```
일단 원본 보고있어봐
```

```
이거말하는거야?
```
(이미지 첨부 — AnimGraph 우클릭 메뉴에 `Use cached pose 'BodyBase'`)

```
이미지확인
```
(이미지 첨부 — AnimGraph 전체, `BodyBase` 노드에 `NOTE` 배지)

```
이렇게 두개놓고컴파일해?
```
(이미지 첨부 — `Use cached pose 'BodyBase'` 두 개가 놓임)

```
결과 확인
```

```
전부 이상없음 이거 하던거 다하고 나서 리턴할때 끊어서 가는거 그것만 고치고 마무리하는건어때
```

```
결과 확인
```

```
PIE 결과 이상 없음
```

```
이대로하자
```

```
결과 확인
```

```
1에서 4까지 문제없음
```

```
지금 작업은 다한건가그럼?
```

```
기록할 것이나 커밋 다하고 그럼 마무리할까 여기세션
```

### English — MCP에 실제로 보낸 명령

**이번 세션에 AI가 MCP로 직접 보낸 것은 전부 읽기다.** 쓰기는 아래 명령문을 사용자가 UE Terminal에 붙여 실행했고, 일부는 사용자가 에디터에서 손으로 했다. AI가 직접 부른 MCP 툴 — `list_toolsets` · `describe_toolset` · `GetLogEntries` · `get_properties` · `get_default_object` · `list_graphs` · `list_functions` · `list_variables` · `find_nodes` · `get_node_infos` · `read_graph_dsl`.

콘솔 명령 넷은 사용자가 UE의 `Enter Console Command` 칸에 넣었다.

```
GetAll AnimMontage Notifies Name=AM_Player_Attack
```
(같은 명령을 네 번 넣었다 — 노티파이 이동 전 확인, 이동 확인 실패 두 번, 이동 성공 확인, 슬롯 변경 후 확인)

```
GetAll Skeleton SlotToGroupNameMap Name=SK_Mannequin
```

```
GetAll Skeleton SlotGroups Name=SK_Mannequin
```

---

**명령 1 — `CanJumpInternal` 오버라이드 (실패)**

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, override the inherited
function CanJumpInternal (its Blueprint display name is "CanJump") and implement
it so the character cannot jump while any montage is playing.

Do NOT touch BP_ThirdPersonCharacter:EventGraph in this command.
Do NOT create any new Blueprint variable.
Do NOT modify any other asset. Do NOT touch ABP_Unarmed, AM_Player_Attack,
BP_Enemy, or SK_Mannequin.

PRE-FLIGHT. Report every result. Stop and report if any of these fails:
 P1. list_functions on BP_ThirdPersonCharacter must list CanJumpInternal with
     bIsImplemented = false. If it is already true, STOP - the override exists.
 P2. list_variables must return exactly these 15 names:
     bIsFirstPerson, FirstPersonPitchMin, FirstPersonPitchMax,
     ThirdPersonPitchMin, ThirdPersonPitchMax, InventorySlots, SelectedSlot,
     CurrentHP, MaxHP, InteractDistance, FoundSlotIndex, RespawnDelay,
     AttackMontage, AttackRange, AttackTraceRadius
 P3. Record the exact node count of BP_ThirdPersonCharacter:EventGraph.
     It must be unchanged at the end of this command.

IMPLEMENT. The override graph must contain exactly these six nodes:
 1. the function Entry node for CanJumpInternal
 2. a "Parent: CanJump" call-to-parent-function node
 3. GetCurrentMontage, target = self
 4. IsValid - the PURE function from KismetSystemLibrary that takes an Object
    and returns a Boolean. NOT the "Is Valid" macro with execution pins.
    Its Object input comes from the GetCurrentMontage return value.
 5. a Boolean NOT node fed by the IsValid result
 6. a Boolean AND node fed by the Parent: CanJump result and the NOT result
Wire the AND result into the function Return node's ReturnValue.
The Parent: CanJump call is REQUIRED - without it the engine's own ground check
and jump-count limit are gone.

Then compile BP_ThirdPersonCharacter.

REPORT, in this order:
 R1. the P1/P2/P3 results
 R2. every node you created, by node title and class
 R3. every pin connection you made, as "SourceNode.Pin -> TargetNode.Pin"
 R4. the compile result, including any warning text verbatim
 R5. the node count of BP_ThirdPersonCharacter:EventGraph after the change,
     and whether it matches P3
Do not claim success from a tool return value alone. Read the graph back with
find_nodes and get_node_infos and report what you actually read.
```

옮기며 AI가 정한 것 — `IsValid`를 순수 함수 버전으로 못박은 것(이벤트 그래프의 기존 공격 체인은 exec 핀이 있는 매크로를 쓴다), 노드를 정확히 여섯 개로 못박은 것(사양에 개수는 없었다).

---

**명령 2 — 로직 반전으로 재시도 (부분 성공, Stage 2에서 정지)**

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, build the
CanJumpInternal override again, this time WITHOUT any IsValid node.

Logic: ReturnValue = ( Parent: CanJump ) AND ( GetCurrentMontage == none )

Do NOT touch BP_ThirdPersonCharacter:EventGraph.
Do NOT create any new Blueprint variable.
Do NOT touch ABP_Unarmed, AM_Player_Attack, BP_Enemy, or SK_Mannequin.
Do NOT use any IsValid node, macro or function.

Work in the four STAGES below, in order. After each stage, read the graph
back with find_nodes / get_node_infos and report what you actually read.
If a stage fails, STOP at that stage and report - do NOT roll back, because
each stage is designed to leave jumping in a safe state.

STAGE 1. add_function_graph(blueprint, graph_name="CanJumpInternal").
  Use exactly the name CanJumpInternal, not the display name CanJump.
  Confirm the graph contains a FunctionEntry and a FunctionResult node.
  Report their node names.

STAGE 2. Create the call-to-parent node for CanJumpInternal and connect its
  Boolean output DIRECTLY to the FunctionResult ReturnValue pin.
  Search the override graph with find_node_types for the parent-call node type
  and report every candidate type_id you get back BEFORE creating anything.
  If no parent-call node type can be created, STOP and report - do not
  substitute a hand-built equivalent of the engine's ground check.
  After this stage the override returns exactly what the engine would, so it
  is safe to stop here.

STAGE 3. Create GetCurrentMontage (target = self) and an "Equal (Object)"
  pure node from KismetMathLibrary (DisplayName "Equal (Object)",
  CompactNodeTitle "==", Category "Utilities", declared at
  Engine/Source/Runtime/Engine/Classes/Kismet/KismetMathLibrary.h:3884).
  Before creating it, run find_node_types and report how many candidates
  match. If more than one candidate is indistinguishable by type_id - the
  same failure mode as IsValid in the previous command - STOP and report.
  Wire GetCurrentMontage's return value into pin A of Equal (Object).
  Leave pin B empty so it compares against none.
  Do not connect this to anything else yet.

STAGE 4. Create a Boolean AND node. Feed it the Parent: CanJump output and
  the Equal (Object) output. Break the direct Parent -> ReturnValue link from
  stage 2 and connect the AND result to ReturnValue instead.
  Then compile BP_ThirdPersonCharacter.

REPORT:
 R1. per stage: nodes created (title + class) and every connection made,
     as "SourceNode.Pin -> TargetNode.Pin"
 R2. the find_node_types candidate lists from stages 2 and 3, verbatim
 R3. the final graph read back node by node with get_node_infos
 R4. the compile result, with any warning text verbatim
 R5. the EventGraph node count - it must still be 140
```

옮기며 AI가 정한 것 — `Not Equal (Object)`가 아니라 `Equal (Object)`를 쓰는 쪽. `!=`를 쓰면 결과를 다시 뒤집어야 해서 `NOT`이 되살아난다.

**이 명령문의 "각 단계가 멈춰도 안전하다"는 전제가 틀렸다.** Stage 2가 실패하면 배선 없는 `Return`이 `false`를 돌려주므로 점프가 통째로 막힌다. 롤백 금지 지시도 그 틀린 전제 위에 있었다.

---

**명령 3 — 손으로 만든 `Parent: CanJump` 위에 나머지 배선**

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, finish the
CanJumpInternal override.

Current state, already verified - do NOT rebuild these:
  K2Node_FunctionEntry_0        (type |CanJump)
  K2Node_CallParentFunction_0   (type Character|Parent:CanJump)
  K2Node_FunctionResult_0       (type |ReturnNode)
  Entry.then -> Parent.execute
  Parent.then -> Result.execute
  Parent.ReturnValue -> Result.ReturnValue

Target logic: ReturnValue = ( Parent: CanJump ) AND ( GetCurrentMontage == none )

Do NOT touch BP_ThirdPersonCharacter:EventGraph. It must stay at 140 nodes.
Do NOT create any new Blueprint variable.
Do NOT delete or recreate the three nodes listed above.
Do NOT use any IsValid node, macro or function.
Do NOT compile until STEP 4.

STEP 1. Create these three nodes. Before creating each one, run find_node_types
  on the CanJumpInternal graph and report every candidate type_id verbatim.
  If two or more candidates are indistinguishable by type_id, STOP and report -
  that is the same failure that blocked IsValid last time.
  a) GetCurrentMontage, target = self. Note it is BlueprintCallable and NOT
     BlueprintPure (Character.h:897), so it HAS exec pins.
  b) Equal (Object) - the pure node from KismetMathLibrary, DisplayName
     "Equal (Object)", CompactNodeTitle "==", Category "Utilities"
     (KismetMathLibrary.h:3884).
  c) a Boolean AND node.

STEP 2. Data wiring only. Make exactly these connections:
  GetCurrentMontage.ReturnValue -> Equal(Object).A
  Parent.ReturnValue            -> AND input 0
  Equal(Object).ReturnValue     -> AND input 1
  Leave Equal(Object) pin B empty so it compares against none.
  Do not touch any exec pin in this step.

STEP 3. Rewiring. Do these three in this exact order:
  1) Parent.then           -> GetCurrentMontage.execute
  2) GetCurrentMontage.then -> Result.execute
  3) AND.ReturnValue        -> Result.ReturnValue
  After this step Result.ReturnValue must be fed by AND, not by Parent.

STEP 4. Compile BP_ThirdPersonCharacter.

REPORT:
 R1. the find_node_types candidate lists from STEP 1, verbatim
 R2. every node created (title + class) and every connection made
 R3. the whole CanJumpInternal graph read back with get_node_infos, node by
     node, including which pin feeds Result.ReturnValue
 R4. the compile result with any warning text verbatim
 R5. the EventGraph node count
```

옮기며 AI가 정한 것 — `GetCurrentMontage`를 `Entry` 뒤가 아니라 `Parent`와 `Result` 사이에 끼운 것. 기존 링크 중 끊기는 것이 하나뿐이라 재배선이 가장 적다. **이 명령문의 "`GetCurrentMontage`는 exec 핀이 있다"는 서술은 틀렸다.** 실제로는 순수 노드로 생성됐고 STEP 3의 exec 재배선 두 개는 일어나지 않았다.

---

**명령 4 — 공중에서 공격 금지**

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter:EventGraph, block the
attack while the character is in the air.

Do NOT touch the CanJumpInternal graph - it is finished and verified.
Do NOT create any new Blueprint variable.
Do NOT touch ABP_Unarmed, AM_Player_Attack, BP_Enemy, or SK_Mannequin.
Do NOT change AttackRange, AttackTraceRadius, AttackMontage or any other
tuning value.
Do NOT compile until STEP 4.

STEP 0. Identify the existing IA_Attack chain and report the exact node
  refPaths you find, before changing anything. Based on a prior read the chain
  is believed to be:
     K2Node_EnhancedInputAction_8  = IA_Attack
     K2Node_CallFunction_60        = GetCurrentMontage
     K2Node_MacroInstance_2        = the IsValid macro
     K2Node_IfThenElse_9           = first Branch (inventory index range)
     K2Node_IfThenElse_10          = second Branch (name == "Knife")
     K2Node_PlayMontage_0          = Play Montage
  VERIFY this by reading pins, do not trust the list. If the real chain differs,
  STOP and report what it actually is.
  Also confirm which exec pin currently feeds K2Node_IfThenElse_9.execute -
  it is expected to be the IsValid macro's "Is Not Valid" output.

STEP 1. Create three nodes. Before each, run find_node_types and report every
  candidate type_id verbatim. If two candidates are indistinguishable, STOP.
  a) a getter for the CharacterMovement component of self
  b) IsFalling, target = that CharacterMovement component
  c) a Branch node

STEP 2. Data wiring only:
  CharacterMovement -> IsFalling target/self pin
  IsFalling.ReturnValue -> Branch.Condition
  Touch no exec pin in this step.

STEP 3. Exec rewiring, in this exact order:
  1) Branch.False -> K2Node_IfThenElse_9.execute
  2) the IsValid macro's "Is Not Valid" output -> Branch.execute
  Leave Branch.True unconnected - falling means no attack.
  After this the chain must read:
     IA_Attack -> GetCurrentMontage -> IsValid
       Is Not Valid -> Branch(IsFalling)
         False -> IfThenElse_9 -> IfThenElse_10 -> Play Montage
         True  -> nothing

STEP 4. Compile BP_ThirdPersonCharacter.

REPORT:
 R1. the STEP 0 verification - the real chain, node by node
 R2. the find_node_types candidate lists, verbatim
 R3. every node created and every connection made
 R4. the compile result with any warning text verbatim
 R5. the EventGraph node count - it was 140, it must now be 143
```

옮기며 AI가 정한 것 둘 — `Branch`의 `True`를 비우고 `False`로 진행하게 한 것(`NOT` 노드 하나를 아낀다), 분기를 `IsValid` 바로 뒤·인벤토리 검사 앞에 넣은 것(공중이면 인벤토리를 볼 이유가 없다).

---

**명령 5 — `ABP_Unarmed` 노드 5개 (STEP 1b에서 정지)**

```
In /Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed, add upper-body
layering to the AnimGraph.

CRITICAL: this AnimGraph is SHARED with BP_Enemy. The enemy must come out
looking exactly as it does now.

Current AnimGraph, already verified by reading pins:
  AnimGraphNode_StateMachine_0 "Locomotion"  -> AnimGraphNode_SaveCachedPose_0 'Locomotion'
  AnimGraphNode_StateMachine_1 "Main States" -> AnimGraphNode_Slot_0 (slot 'DefaultSlot')
  AnimGraphNode_Slot_0 -> AnimGraphNode_ControlRig_0.Source
  AnimGraphNode_ControlRig_0 -> AnimGraphNode_Root_0.Result

Do NOT touch AnimGraphNode_StateMachine_0, AnimGraphNode_SaveCachedPose_0,
or anything inside either state machine.
Do NOT touch ABP_Unarmed:EventGraph.
Do NOT touch AM_Player_Attack, AM_Enemy_Attack, BP_Enemy, SK_Mannequin,
or BP_ThirdPersonCharacter.
Do NOT change AnimGraphNode_ControlRig_0's Alpha or ShouldDoIKTrace.
Do NOT compile until STEP 4.

STEP 1. Create five nodes, unconnected. Before each, run find_node_types and
  report every candidate type_id verbatim. If candidates are indistinguishable,
  STOP and report.
  a) Save Cached Pose, cache name  BodyBase
  b) Use Cached Pose  referencing  BodyBase          (call this USE_A)
  c) Use Cached Pose  referencing  BodyBase          (call this USE_B)
  d) Slot node with slotName  UpperBody
     UpperBody is already registered in SK_Mannequin's DefaultGroup - do NOT
     add or modify any slot on the skeleton.
  e) Layered blend per bone (FAnimNode_LayeredBoneBlend)

STEP 2. Configure the blend node. Report the exact property paths you write to.
  LayerSetup[0].BranchFilters[0].BoneName    = spine_01
  LayerSetup[0].BranchFilters[0].BlendDepth  = 1
  BlendWeights[0]                            = 1.0
  Leave bBlendRootMotionBasedOnRootBone at its default of true.
  Leave bMeshSpaceRotationBlend and bMeshSpaceScaleBlend at their defaults.
  If these cannot be written through the available tools, STOP and report -
  do NOT substitute different settings.

STEP 3. Wiring. Do it in exactly this order. Steps 3a-3c leave the existing
  chain untouched and working; only 3d switches it over.
  3a. USE_A            -> LayeredBoneBlend.BasePose
  3b. USE_B            -> Slot'UpperBody'.Source
  3c. Slot'UpperBody'  -> LayeredBoneBlend.BlendPoses[0]
      If BlendPoses has no index 0 pin, add one, and report that you did.
  3d. these two, back to back:
        AnimGraphNode_Slot_0 -> SaveCachedPose'BodyBase'.Pose
        LayeredBoneBlend     -> AnimGraphNode_ControlRig_0.Source
      The first of these breaks Slot_0 -> ControlRig_0. That is intended.

  Final shape must be:
    StateMachine_1 -> Slot'DefaultSlot' -> SaveCachedPose'BodyBase'
    USE_A -> LayeredBoneBlend.BasePose
    USE_B -> Slot'UpperBody' -> LayeredBoneBlend.BlendPoses[0]
    LayeredBoneBlend -> ControlRig -> Output Pose

STEP 4. Compile ABP_Unarmed.

REPORT:
 R1. the find_node_types candidate lists, verbatim
 R2. every node created with its type_id, and every connection made
 R3. the blend node's LayerSetup and BlendWeights read back after writing
 R4. the whole AnimGraph read back with get_node_infos, node by node
 R5. the compile result with any warning text verbatim
```

옮기며 AI가 정한 것 둘 — 캐시 이름을 `BodyBase`로 한 것(사양에 쓴 `FullBody`가 이미 `SK_Mannequin`의 슬롯 이름으로 존재한다), `bBlendRootMotionBasedOnRootBone`을 기본값 `true`로 두라고 명시한 것(루트 모션 결론이 이 값에 걸려 있다).

**이 명령문의 "STEP 4까지 컴파일 금지"가 STEP 1b를 막았다.**

---

**명령 6 — 중간 컴파일 허용 후 재개 (STEP 0에서 정지)**

```
Resume the ABP_Unarmed work. The previous command's restrictions still apply
EXCEPT the compile ban, which was my error and is lifted.

CRITICAL: this AnimGraph is SHARED with BP_Enemy.

Already done, do NOT redo:
  AnimGraphNode_SaveCachedPose_1, cacheName = BodyBase, Pose input unconnected

Do NOT touch AnimGraphNode_StateMachine_0/_1, AnimGraphNode_SaveCachedPose_0,
or anything inside either state machine.
Do NOT touch ABP_Unarmed:EventGraph.
Do NOT touch AM_Player_Attack, AM_Enemy_Attack, BP_Enemy, SK_Mannequin,
or BP_ThirdPersonCharacter.
Do NOT change AnimGraphNode_ControlRig_0's Alpha or ShouldDoIKTrace.

STEP 0. Compile ABP_Unarmed now, so Usecachedpose'BodyBase' enters the node
  registry. Report the compile result verbatim, including any warning about
  the unused cached pose - such a warning is expected and is not a failure.
  Then run find_node_types with filter "cachedpose" and report the list.
  If Usecachedpose'BodyBase' still does not appear, STOP and report.

STEP 1. Create four nodes, unconnected:
  b) Use Cached Pose referencing BodyBase   (USE_A)
  c) Use Cached Pose referencing BodyBase   (USE_B)
  d) Slot node with slotName UpperBody
     UpperBody is already registered in SK_Mannequin's DefaultGroup.
     Do NOT add or modify any slot on the skeleton.
  e) Layered blend per bone (FAnimNode_LayeredBoneBlend)
  Before each, run find_node_types and report every candidate verbatim.

STEP 2. Configure the blend node. Report the exact property paths you write to
  and read them back afterwards.
  LayerSetup[0].BranchFilters[0].BoneName   = spine_01
  LayerSetup[0].BranchFilters[0].BlendDepth = 1
  BlendWeights[0]                           = 1.0
  Leave bBlendRootMotionBasedOnRootBone at its default of true.
  If any of these cannot be written, STOP and report exactly which one and what
  the tool said. Do NOT substitute different settings, and do NOT proceed to
  STEP 3 with a half-configured blend node.

STEP 3. Wiring, in this exact order:
  3a. USE_A           -> LayeredBoneBlend.BasePose
  3b. USE_B           -> Slot'UpperBody'.Source
  3c. Slot'UpperBody' -> LayeredBoneBlend.BlendPoses[0]
      If BlendPoses has no index 0 pin, add one and report that you did.
  3d. these two, back to back:
        AnimGraphNode_Slot_0 -> SaveCachedPose'BodyBase'.Pose
        LayeredBoneBlend     -> AnimGraphNode_ControlRig_0.Source
      The first breaks Slot_0 -> ControlRig_0. That is intended.

  Final shape:
    StateMachine_1 -> Slot'DefaultSlot' -> SaveCachedPose'BodyBase'
    USE_A -> LayeredBoneBlend.BasePose
    USE_B -> Slot'UpperBody' -> LayeredBoneBlend.BlendPoses[0]
    LayeredBoneBlend -> ControlRig -> Output Pose

STEP 4. Compile ABP_Unarmed again.

REPORT:
 R1. STEP 0's compile result and the cachedpose candidate list, verbatim
 R2. every node created with its type_id, and every connection made
 R3. LayerSetup and BlendWeights read back after writing
 R4. the whole AnimGraph read back with get_node_infos, node by node
 R5. the final compile result with any warning text verbatim
```

---

**명령 7 — 손으로 놓은 `Use Cached Pose` 위에 나머지**

```
Finish the upper-body layering in
/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed:AnimGraph.

CRITICAL: this AnimGraph is SHARED with BP_Enemy.

Already present, created by hand - do NOT recreate or delete these:
  AnimGraphNode_SaveCachedPose_1   cacheName = BodyBase, Pose unconnected
  AnimGraphNode_UseCachedPose_1    referencing BodyBase, unconnected  (USE_A)
  AnimGraphNode_UseCachedPose_2    referencing BodyBase, unconnected  (USE_B)
The blue NOTE badge on SaveCachedPose_1 is "Pose  was visible but ignored",
an informational Note from AnimBlueprintExtension_Base.cpp:288, not an error.
It clears once its Pose input is fed in STEP 3d.

Do NOT touch AnimGraphNode_StateMachine_0/_1, AnimGraphNode_SaveCachedPose_0,
K2Node_VariableGet_0, K2Node_CallFunction_0, or anything inside either state
machine.
Do NOT touch ABP_Unarmed:EventGraph.
Do NOT touch AM_Player_Attack, AM_Enemy_Attack, BP_Enemy, SK_Mannequin,
or BP_ThirdPersonCharacter.
Do NOT change AnimGraphNode_ControlRig_0's Alpha or ShouldDoIKTrace.

STEP 1. Create two nodes, unconnected. Before each, run find_node_types and
  report every candidate type_id verbatim.
  d) Slot node with slotName UpperBody
     UpperBody is already registered in SK_Mannequin's DefaultGroup.
     Do NOT add or modify any slot on the skeleton.
  e) Layered blend per bone (FAnimNode_LayeredBoneBlend)

STEP 2. Configure the blend node. Report the exact property paths you write to,
  then READ THEM BACK and report what came back.
  LayerSetup[0].BranchFilters[0].BoneName   = spine_01
  LayerSetup[0].BranchFilters[0].BlendDepth = 1
  BlendWeights[0]                           = 1.0
  Leave bBlendRootMotionBasedOnRootBone at its default of true.
  If a write silently no-ops - the read-back does not show what you wrote -
  treat that as failure. STOP and report which path failed and what the tool
  returned. Do NOT substitute different settings and do NOT continue to STEP 3.
  Nothing is rewired until STEP 3, so stopping here leaves the enemy untouched.

STEP 3. Wiring, in this exact order:
  3a. AnimGraphNode_UseCachedPose_1 -> LayeredBoneBlend.BasePose
  3b. AnimGraphNode_UseCachedPose_2 -> Slot'UpperBody'.Source
  3c. Slot'UpperBody'               -> LayeredBoneBlend.BlendPoses[0]
      If BlendPoses has no index 0 pin, add one and report that you did.
  3d. these two, back to back, nothing in between:
        AnimGraphNode_Slot_0 -> AnimGraphNode_SaveCachedPose_1.Pose
        LayeredBoneBlend     -> AnimGraphNode_ControlRig_0.Source
      The first breaks Slot_0 -> ControlRig_0. That is intended and is the only
      moment the evaluated chain is incomplete.

  Final shape:
    StateMachine_1 -> Slot'DefaultSlot' -> SaveCachedPose'BodyBase'
    UseCachedPose_1 -> LayeredBoneBlend.BasePose
    UseCachedPose_2 -> Slot'UpperBody' -> LayeredBoneBlend.BlendPoses[0]
    LayeredBoneBlend -> ControlRig -> Output Pose

STEP 4. Compile ABP_Unarmed.

REPORT:
 R1. the find_node_types candidate lists, verbatim
 R2. every node created with its type_id, and every connection made
 R3. LayerSetup and BlendWeights READ BACK after writing, verbatim
 R4. the whole AnimGraph read back with get_node_infos, node by node
 R5. the compile result with any warning text verbatim
```

---

**명령 8 — 몽타주 슬롯 변경**

```
In /Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack, change
the montage's slot from DefaultSlot to UpperBody.

Do NOT touch AM_Enemy_Attack. It must stay on DefaultSlot.
Do NOT touch ABP_Unarmed, SK_Mannequin, BP_Enemy, or BP_ThirdPersonCharacter.
Do NOT change SequenceLength, BlendIn, BlendOut, or anything under Notifies.
Do NOT change the animation segment - it must stay MM_Attack_01, 0.0 to 1.0,
playRate 1.

PRE-FLIGHT. Report the result. Stop if it differs:
 P1. read AM_Player_Attack's SlotAnimTracks and report it verbatim.
     It is expected to be exactly:
     [{"slotName":"DefaultSlot","animTrack":{"animSegments":[{
       "cachedPlayLength":1,
       "animReference":{"refPath":"/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01.MM_Attack_01"},
       "startPos":0,"animStartTime":0,"animEndTime":1,
       "animPlayRate":1,"loopingCount":1}]}}]
 P2. read the montage's Notifies via any means available and record what you
     see. If Notifies cannot be read - it is a bare UPROPERTY and this session
     has already established that - say so and continue.

WRITE. Set SlotAnimTracks so that the ONLY difference from P1 is:
     slotName: "DefaultSlot"  ->  "UpperBody"
Every other field must be written back byte-identical to what P1 returned.
UpperBody is already registered in SK_Mannequin's DefaultGroup - do NOT add or
modify any slot on the skeleton.

VERIFY. Read SlotAnimTracks back and report it verbatim. If anything other
than slotName changed, say so explicitly.

REPORT:
 R1. P1 and P2 results, verbatim
 R2. the exact write call you made
 R3. the read-back after writing, verbatim
 R4. whether the montage asset is now dirty
```

옮기며 AI가 정한 것 — 노티파이를 P2에서 미리 찍어두라고 한 것. `animReference`를 바꿨을 때 노티파이의 `LinkedSequence`가 옛 값에 남은 전례가 있어 비교 대상이 필요했다.

---

**명령 9 — 적 복귀 비래턴트**

```
In /Game/Enemy/BP_Enemy:EventGraph, make the RETURN branch non-latent so the
enemy re-evaluates every ThinkInterval while walking home.

The RETURN branch currently reads:
  PrintString "RETURN"
  K2Node_AIMoveTo_2( self,
      GetActorLocation + Normalize(HomeLocation - GetActorLocation)
                       * Min(ReturnStepDistance, distToHome),
      AcceptanceRadius 0.0 )
    OnSuccess -> Delay(ThinkInterval) -> Think
    OnFail    -> Delay(ThinkInterval) -> Think

Target shape, identical in form to the CHASE branch:
  PrintString "RETURN"
  SimpleMoveToLocation( GetController(self), GetHomeLocation )
  Delay(ThinkInterval)
  Think

Do NOT touch the ATTACK, CHASE, IDLE_HOME, IDLE_WAIT or NO_PLAYER branches.
Do NOT touch EventBeginPlay.
Do NOT delete or rename ANY Blueprint variable, including ReturnStepDistance -
it becomes unread but the variable itself stays.
Do NOT change any default value: ThinkInterval 0.3, ReturnDelay 7,
HomeArriveRadius 100, ReturnStepDistance 300, ReturnSightRange 300,
SightRange 1200, SightHalfAngle 60, AttackRange 150 all stay as they are.
Do NOT remove any PrintString.
Do NOT touch BP_ThirdPersonCharacter, ABP_Unarmed, or any animation asset.
Do NOT compile until STEP 4.

STEP 0. Report the RETURN branch as it stands: every node refPath in it, and
  which Delay/Think pair hangs off OnSuccess and which off OnFail.

STEP 1. Create two nodes. Before each, run find_node_types and report every
  candidate type_id verbatim. If candidates are indistinguishable, STOP.
  a) SimpleMoveToLocation - AIBlueprintHelperLibrary, Category "AI|Navigation"
     (AIBlueprintHelperLibrary.h:94-95). NOT SimpleMoveToActor.
  b) GetController with target self, to feed its Controller pin

STEP 2. Data wiring only:
  GetController(self)             -> SimpleMoveToLocation.Controller
  the EXISTING GetHomeLocation getter's output -> SimpleMoveToLocation.Goal
  Reuse the GetHomeLocation node already in the graph; do not create a second
  one. Touch no exec pin in this step.

STEP 3. Exec rewiring:
  3a. PrintString "RETURN".then -> SimpleMoveToLocation.execute
      This breaks PrintString -> K2Node_AIMoveTo_2.
  3b. SimpleMoveToLocation.then -> the Delay that currently hangs off
      K2Node_AIMoveTo_2's OnSuccess pin. Keep that Delay and its Think.
  3c. Delete these nodes, and report each deletion:
        K2Node_AIMoveTo_2
        the Normalize node feeding its destination
        the Min(Float) node feeding its destination
        the vector*vector node feeding its destination
        the vector+vector node feeding its destination
        the GetReturnStepDistance getter feeding the Min node
        the now-orphaned Delay and Think that hung off OnFail
      Before deleting each of the five math nodes and the getter, VERIFY it has
      no other consumer anywhere in the graph. If any of them is also read by
      another branch, do NOT delete it - leave it and report that.

STEP 4. Compile BP_Enemy.

REPORT:
 R1. the STEP 0 reading of the branch
 R2. the find_node_types candidate lists, verbatim
 R3. every node created, every connection made, every node deleted
 R4. the RETURN branch read back with get_node_infos, node by node
 R5. the compile result with any warning text verbatim
 R6. confirm ReturnStepDistance still exists as a variable
```

옮기며 AI가 정한 것 — `OnSuccess` 쪽 `Delay`/`Think` 쌍을 살리고 `OnFail` 쪽을 지우게 한 것. 지정하지 않으면 둘 다 지우고 새로 만들 수 있고, 그러면 `ThinkInterval` 게터 배선이 새로 생기면서 틀릴 여지가 는다.

---

**손으로 한 작업 넷** — 도구로 안 되어 사용자가 에디터에서 직접 했다.

1. `AM_Player_Attack` 몽타주 에디터에서 `AttackHit` 노티파이를 프레임 1에서 0.3965초로 드래그
2. `CanJumpInternal` 그래프에서 Entry 노드를 선택하고 우클릭 → `Add Call to Parent Function`, 나온 `Parent: CanJump`의 Boolean 출력을 `Return Node`의 `Return Value`에 연결
3. `AM_Player_Attack`의 `DefaultGroup.DefaultSlot` 행 드롭다운 → `Slot Manager...` → `Add Slot` → 이름 `UpperBody` → `Save`
4. `ABP_Unarmed`의 AnimGraph에서 우클릭 → `Use cached pose 'BodyBase'`를 두 개 배치

## Terminal 결과

### 원문 — English

**노티파이 이동 전 — 콘솔 `GetAll` 출력**

```
[2026.09.01-08.11.47:375][ 66]Cmd: GetAll AnimMontage Notifies Name=AM_Player_Attack
[2026.09.01-08.11.47:388][ 66]0) AnimMontage /Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack.Notifies =
[2026.09.01-08.11.47:388][ 66]	0: (TriggerWeightThreshold=0.000010,NotifyName="PlayMontageNotify",Notify="/Script/AnimGraphRuntime.AnimNotify_PlayMontageNotify'/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack:AnimNotify_PlayMontageNotify_1'",EndLink=(SegmentIndex=-1,LinkValue=0.027284),NotifyTriggerChance=1.000000,bCanBeFilteredViaRequest=True,bTriggerOnDedicatedServer=True,NotifyColor=(B=0,G=0,R=0,A=255),Guid=049237AA4E28B24CAED25D8AD788725C,LinkedMontage="/Script/Engine.AnimMontage'/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack'",SegmentLength=1.000000,LinkValue=0.027284,LinkedSequence="/Script/Engine.AnimSequence'/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_02.MM_Attack_02'")
```

**두 번째 실행 — 값이 안 바뀌었다**

```
[2026.09.01-08.16.07:099][ 77]Cmd: GetAll AnimMontage Notifies Name=AM_Player_Attack
[2026.09.01-08.16.07:107][ 77]	0: (... SegmentLength=1.000000,LinkValue=0.027284,LinkedSequence="...MM_Attack_02.MM_Attack_02")
```
(발췌 — 첫 출력과 소수점 여섯 자리까지 동일해서 달라진 필드만 남겼다)

**노티파이 이동 후**

```
[2026.09.01-08.23.48:967][325]	0: (TriggerWeightThreshold=0.000010,NotifyName="PlayMontageNotify",Notify="/Script/AnimGraphRuntime.AnimNotify_PlayMontageNotify'/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack:AnimNotify_PlayMontageNotify_1'",EndLink=(SegmentIndex=-1,LinkValue=0.027284),NotifyTriggerChance=1.000000,bCanBeFilteredViaRequest=True,bTriggerOnDedicatedServer=True,NotifyColor=(B=0,G=0,R=0,A=255),Guid=049237AA4E28B24CAED25D8AD788725C,LinkedMontage="/Script/Engine.AnimMontage'/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack'",SegmentLength=1.000000,LinkValue=0.397855,LinkedSequence="/Script/Engine.AnimSequence'/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01.MM_Attack_01'")
```

**슬롯 변경 후 — 노티파이가 그대로인지 확인**

```
[2026.09.01-10.25.57:221][544]	0: (... SegmentLength=1.000000,LinkValue=0.397855,LinkedSequence="/Script/Engine.AnimSequence'/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01.MM_Attack_01'")
```
(발췌 — 앞 출력과 같은지만 보면 되어 뒷부분만 남겼다)

**Notify 오브젝트의 `NotifyName` — MCP `get_properties`**

```
{"NotifyName":"AttackHit"}
```

**`SlotToGroupNameMap` 조회 실패 — 프로퍼티를 못 찾았다**

```
[2026.09.01-09.44.50:500][598]Cmd: GetAll Skeleton SlotToGroupNameMap Name=SK_Mannequin
[2026.09.01-09.44.50:505][598]0) Skeleton /Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin
```

**`SlotGroups` 조회 성공**

```
[2026.09.01-09.46.06:332][129]Cmd: GetAll Skeleton SlotGroups Name=SK_Mannequin
[2026.09.01-09.46.06:336][129]0) Skeleton /Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin.SlotGroups =
[2026.09.01-09.46.06:336][129]	0: (GroupName="DefaultGroup",SlotNames=("FullBody","DefaultSlot","UpperBody","FullBodyAdditivePreAim","UpperBodyAdditive","UpperBodyDynAdditiveBase","UpperBodyDynAdditive","Arms"))
[2026.09.01-09.46.06:336][129]	1: (GroupName="AdditiveGroup",SlotNames=("AdditiveHitReact"))
```

**MCP가 거부한 프로퍼티**

```
[2026.09.01-08.29.49:078][144]LogScript: Warning: GetObjectProperties on '/Game/Characters/Mannequins/Meshes/SK_Mannequin.SK_Mannequin' (Skeleton): the following properties could not be read: SlotGroups, SlotToGroupNameMap
```

**명령 1의 실패 — Terminal 에이전트 보고 전문**

```
P1 and P2 pass. Counting P3: 140 nodes in EventGraph.

Now checking how to create the override graph:

Override graph created with Entry + Result. Now the critical node - the pure IsValid:

declaring_class ignored again. Running one diagnostic to confirm the parameter is inert rather than mis-specified:

Confirmed inert - a deliberately wrong declaring_class produced an identical macro. create_node cannot select the pure function.

Stopping here per the spec. Removing my partial[ly im]plemented CanJumpInternal override returns the Result node's default false - that would silently disable jumping entirely:

Stopped. Node 4 cannot be created with these t[ools as im]plemented, and I rolled back what I had started.

R1 - Pre-flight

P1 - PASS. list_functions returned 9 entries; the last is:
{"name":"CanJumpInternal",
 "description":"Customizable event to check if[ the character can jump in th]e current state.\nDefault implementation returns true if the character is on the ground and not crouching,\nhas a valid CharacterMovementComponent and CanEverJump() returns true. ...",
 "bIsImplemented":false}
bIsImplemented = false -> no existing override, proceed.

P2 - PASS. list_variables returned exactly 15 names, in your order, no extras:
bIsFirstPerson, FirstPersonPitchMin, FirstPersonPitchMax, ThirdPersonPitchMin, ThirdPersonPitchMax, InventorySlots, SelectedSlot, CurrentHP, MaxHP, InteractDistance, FoundSlotIndex, RespawnDelay, AttackMontage, AttackRange, AttackTraceRadius

P3 - EventGraph node count: 140. (Counted from the find_nodes list, first entry K2Node_CallFunction_23, last
K2Node_MakeArray_0.) Correcting myself: at the[ end of the last session ]I said the count went "121 -> 135". The true[ ]post-state was 140 - I under-counted then. 140 is the figure this command is measured against, and it was read fresh, not carried over.

R2 - Nodes created

Only two, both discarded. Neither is the node[ that was needed.]

| Node | [type_id] | Fate |
| CanJumpInternal.K2Node_MacroInstance_0 | Uti[lities|IsValid - the macro] | deleted with the graph |
| CanJumpInternal.K2Node_MacroInstance_1 | Utilities|IsValid - the macro (diagnostic) | deleted with the graph |

add_function_graph(graph_name="CanJumpInternal") did work - it returned ...BP_ThirdPersonCharacter:CanJumpInternal and
find_nodes on it showed the override was corre[ctly formed with K2Node_Funct]ionEntry_0 and K2Node_FunctionResult_0. So[ ]requirement 1 and the Return node were achievable. I never reached nodes 2, 3, 5, 6.

R3 - Pin connections

None. I made no connect_pins call in this command.

Why it stopped

Requirement 4 is the pure IsValid from KismetSystemLibrary, explicitly not the macro. In the engine source it is declared:
// Return true if the object is usable : non-null and not pending kill
UFUNCTION(BlueprintPure, Category = "Utilities")
static bool IsValid(const UObject* Object);
C:\Program Files\Epic Games\UE_5.8\Engine\Source\Runtime\Engine\Classes\Kismet\KismetSystemLibrary.h:127-128

Category Utilities + name IsValid -> type_id Utilities|IsValid - the same string the macro uses. find_node_types on the override graph returns it three times, indistinguishably:
["Utilities|IsValidSoftObjectReference","Utili[ties|IsValidSoftClassReferenc]e",
 "Utilities|IsValidInterface","Utilities|IsValidClass",
 "Utilities|IsValid","Utilities|IsValid","Utilities|IsValid"]

create_node's only disambiguator is declaring_class. I tested it twice:

- type_id="Utilities|IsValid", declaring_class="/Script/Engine.KismetSystemLibrary" -> K2Node_MacroInstance_0. Pin read-back: outputs Is Valid / Is Not Valid (both Exec), inputs exec (Exec) + InputObject. The macro. No Boolean output.
- Same call with a deliberately wrong declaring_class="/Script/Engine.KismetMathLibrary" -> K2Node_MacroInstance_1,
byte-identical result.

The wrong class producing the identical node proves declaring_class is inert for this resolution path - it isn't that I passed the wrong value. There is no index para[meter, and retarget_node_class only ]swaps a node's class reference, not its[ ]function, so it can't convert one to the other. I found no other route.

Rollback, and why

A CanJumpInternal override whose Return node is unwired returns the Result node's default - false. Leaving a half-built override in place would have made the character unable to jump at all, a silent gameplay regression worse than not doing the task. So I called remove_function_graph(graph_name="CanJumpInternal") and recompiled.

Verified after rollback:
- list_functions -> CanJumpInternal back to bIsImplemented: false, all 8 real functions intact.
- list_graphs -> 9 graphs, no CanJumpInternal entry, matching the pre-command set.

R4 - Compile result

The only compile I ran was after the rollback.[ It succeeded, log line quoted in f]ull. LogBlueprint gained no new line beyond the[ ]Compiling Blueprint entry; no warning or error text was emitted, so there is nothing to quote verbatim. As established earlier in this session, the Compiler Results panel's verdict is not retrievable through these tools.

R5 - EventGraph node count after

140 - matches P3. Re-read with find_nodes, sam[e first entry (K2Node_CallFun]ction_23) and same last entry(K2Node_MakeArray_0). I also re-read the graph DSL: all 15 event chains render identically to before, including the IA_Attack chain. EventGraph was never opened for writing in this command.

No other asset was touched. ABP_Unarmed, AM_Player_Attack, BP_Enemy and SK_Mannequin were not read or written. No variable was created.

To actually get this done

The override graph itself builds fine - the blocker is one node. Options:

1. You place the IsValid node by hand. I can create the graph plus nodes 1, 2, 3, 5, 6 and all wiring except the IsValid, leaving its two connections for you to make in the editor. Small manual step, no tool limitation hit.
2. Use Not Equal (Object) against an empty object reference instead of IsValid - creatable via
   Utilities|Operators|NotEqual(!=), gives a re[al Boolean, and a null montag]e pointer behaves the same. That drops the[ literal ]IsValid node but keeps the six-node shape and the pure-function requirement.
3. Invert the logic to remove the NOT: Parent: CanJump AND (GetCurrentMontage == none). Same node count, no IsValid at all.

Tell me which and I'll build it.
```
(대괄호 부분은 사용자가 붙여넣은 원문에서 터미널 폭 때문에 잘려 있던 자리다. 잘린 글자를 문맥으로 메운 것이며, 원문에는 그 자리가 비어 있었다.)

**명령 2의 정지 — `Parent: CanJump` 노드를 만들 수 없다 (발췌)**

```
STOPPED AT STAGE 2. No parent-call node type exists in the creatable set.

Your instruction said not to roll back "because each stage is designed to leave jumping in a safe state." That premise does not hold for a Stage 2 failure. The CanJumpInternal override now exists with ReturnValue unconnected at its default:

{"value":"false", "connected_pins":[], "name":"ReturnValue", "type_id":"Boolean"}

An override returning constant false means the character can never jump - the engine no longer reaches its own implementation. Stage 2 was what would have made it safe, and Stage 2 is exactly what failed.

R2 - find_node_types candidate lists, verbatim

Stage 2, filter "Parent" - 126 candidates, none a parent-function call. Not one contains CanJump.

Stage 2, filter "CanJump":
["Character|CanJump"]

Stage 2, filter "Super":
[]

Stage 2, filter "CallParent":
[]

Stage 2, filter "CanJumpInternal":
[]

Why Character|CanJump is not a substitute - it would recurse

bool ACharacter::CanJump() const
{
      return CanJumpInternal();
}
Engine/Source/Runtime/Engine/Private/Character.cpp:308-311

UFUNCTION(BlueprintNativeEvent, Category=Character, meta=(DisplayName="CanJump"))
ENGINE_API bool CanJumpInternal() const;
Engine/Source/Runtime/Engine/Classes/GameFramework/Character.h:871-872

CanJump() calls CanJumpInternal(), which is the function being overridden. Calling Character|CanJump from inside the override would call the override again - unbounded recursion, stack overflow on the first jump input.
```
(발췌 — R1·R3·R4·R5는 "만든 것 없음 / 연결 없음 / 컴파일 안 함 / 140 유지"였다)

**명령 5의 정지 — `Use Cached Pose`를 만들 수 없다 (발췌)**

```
STOPPED at STEP 1b. "Use Cached Pose referencing BodyBase" cannot be created without a compile, and you forbade compiling before STEP 4.

1a, filter "CachedPoses":
["Animation|CachedPoses|Usecachedpose'Locomoti[on'","Animation|CachedPoses|N]ewSavecachedpose..."]

1b, filter "Usecachedpose":
["Animation|CachedPoses|Usecachedpose'Locomotion'"]

Use-Cached-Pose node types are generated per c[ache. The regis]try offers Usecachedpose'Locomotion' because[ ]that cache exists in the compiled class. There is no generic "Use Cached Pose" type to create and then point at a cache.

list_properties on the[ newly ]created node returns only showPinForProperties, initialUpdateFunction, becomeRelevantFunction, updateFunction, binding, tag, errorMsg - no cache reference of any kind. The engine header explains why:

UPROPERTY()
mutable TWeakObjectPtr<UAnimGraphNode_SaveCach[edPose> SaveCachedPoseNode;]
...
private:
      UPROPERTY()
      mutable FString NameOfCache;
Engine/Source/Editor/AnimGraph/Public/AnimGraphNode_UseCachedPose.h:24-25, 47-49

Both are bare UPROPERTY() with no EditAnywhere/BlueprintReadWrite, and NameOfCache is private. set_properties cannot address either. retarget_node_class swaps a class reference, not a cache name, so it does not apply.
```

**명령 6의 정지 — 컴파일해도 안 나타난다 (발췌)**

```
STOPPED at STEP 0's stop condition. Usecachedpose'BodyBase' still does not appear after the compile.

Compile:
[2026.09.01-09.54.07:626][204]LogBlueprint: Compiling Blueprint '/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed'
compile_blueprint returned null. No warning about the unused cached pose reached the log.

Candidate list, filter "cachedpose":
["Animation|CachedPoses|Usecachedpose'Locomotion'","Animation|CachedPoses|NewSavecachedpose..."]

Second query, filter "BodyBase":
["Utilities|Casting|CastToRigidBodyBase","Utilities|Casting|CastToRigidBodyBaseClass"]

No Usecachedpose'BodyBase' in either.

The cache name did persist. Reading the node b[ack:]
- cacheName = "BodyBase"
- the node's own type_id has updated to Anima[tion|CachedPoses|Savecachedpos]e'BodyBase'
- but errorMsg = "Pose  was visible but ignored" (verbatim, including the double space)

And its Pose input pin reads connected_pins: [].
```

**명령 7 이후 — 블렌드 노드 설정 읽기 (MCP `get_properties`)**

```json
{"Node":{"basePose":{"linkId":-1,"sourceLinkId":-1},"blendPoses":[{"linkId":-1,"sourceLinkId":-1}],"blendMode":"BranchFilter","blendMasks":[],"layerSetup":[{"branchFilters":[{"boneName":"spine_01","blendDepth":1}]}],"blendWeights":[1],"perBoneBlendWeights":[],"skeletonGuid":"00000000-0000-0000-0000-000000000000","virtualBoneGuid":"00000000-0000-0000-0000-000000000000","lODThreshold":-1,"bMeshSpaceRotationBlend":false,"bRootSpaceRotationBlend":false,"bMeshSpaceScaleBlend":false,"curveBlendOption":"Override","bBlendRootMotionBasedOnRootBone":true,"bUpdateBasePoseFirst":false,"initialUpdateFunction":{"className":"None","functionName":"None"},"becomeRelevantFunction":{"className":"None","functionName":"None"},"updateFunction":{"className":"None","functionName":"None"}}}
```

**명령 8 이후 — 몽타주 슬롯 읽기 (MCP `get_properties`)**

```json
{"SlotAnimTracks":[{"slotName":"UpperBody","animTrack":{"animSegments":[{"cachedPlayLength":1,"animReference":{"refPath":"/Game/Characters/Mannequins/Anims/Unarmed/Attack/MM_Attack_01.MM_Attack_01"},"startPos":0,"animStartTime":0,"animEndTime":1,"animPlayRate":1,"loopingCount":1}]}}],"SequenceLength":1,"BlendIn":{"customCurve":"None","blendTime":0.25,"blendOption":"HermiteCubic"},"BlendOut":{"customCurve":"None","blendTime":0.25,"blendOption":"HermiteCubic"}}
```

**명령 9 이후 — `BP_Enemy` `RETURN` 분기 (MCP `read_graph_dsl` 발췌)**

```
        (elif (and (>= (- _returnvalue_2 (Variables|Default|GetLastSeenTime)) (Variables|Default|GetReturnDelay)) (> _returnvalue_5 _homearriveradius))
          (Development|PrintString "RETURN" true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 1.0 "1_state")
          (AI|Navigation|SimpleMoveToLocation (Pawn|GetController) _homelocation)
          (Utilities|FlowControl|Delay (Variables|Default|GetThinkInterval))
          (CallFunction|Think)
```

**`BP_Enemy` 기본값 (MCP `get_properties`)**

```json
{"ThinkInterval":0.29999999999999999,"ReturnDelay":7,"ReturnStepDistance":300,"HomeArriveRadius":100,"ReturnSightRange":300,"SightRange":1200,"SightHalfAngle":60,"AttackRange":150}
```

**컴파일 로그 — 이번 세션 전부. 경고·에러 줄은 하나도 없다**

```
[2026.09.01-08.39.51:330][366]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.09.01-08.58.57:107][508]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.09.01-09.05.25:642][785]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.09.01-09.21.04:610][436]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.09.01-09.54.07:626][204]LogBlueprint: Compiling Blueprint '/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed'
[2026.09.01-10.04.21:526][547]LogBlueprint: Compiling Blueprint '/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed'
[2026.09.01-10.08.09:019][178]LogBlueprint: Compiling Blueprint '/Game/Characters/Mannequins/Anims/Unarmed/ABP_Unarmed.ABP_Unarmed'
[2026.09.01-10.37.50:226][392]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
```

**에디터 화면에 뜬 컴파일 결과** (`Parent: CanJump` 연결 직후, 스크린샷에서 옮김)

```
[1578.73] Compile of BP_ThirdPersonCharacter successful! [in 191 ms] (/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPerso...
```

**세션 중 계속 나온 무관한 경고**

```
[2026.09.01-08.26.26:707][ 62]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
[2026.09.01-07.58.55:323][332]LogModelContextProtocol: Error: Call to unknown method "server/discover"
```

**AI가 MCP 툴 이름을 잘못 불러 실패한 것**

```
Missing required parameter: tool_name
Tool 'EditorToolset.LogsToolset.GetLogEntries' not found
Tool 'GetLogEntries' not found
Function "get_properties", input param "instance" is required by the function input schema Json, but is missing from the incoming function input params Json.
Function "find_nodes", input param "title" is required by the function input schema Json, but is missing from the incoming function input params Json.
Parameter error: /Game/Characters/Mannequins/Animations/ABP_Unarmed.ABP_Unarmed is not valid Blueprint for property 'blueprint'.
```

### 요약 — 한글

**애셋 다섯 개가 바뀌었다.**

`AM_Player_Attack` — `AttackHit` 노티파이의 `LinkValue`가 `0.027284`에서 `0.397855`로 옮겨졌다. 30 fps 기준 프레임 11.94다. 같이 `LinkedSequence`가 `MM_Attack_02`에서 `MM_Attack_01`로 고쳐졌다 — 손대지 않았는데 노티파이를 끄는 과정에서 링크가 재계산됐다. `SlotAnimTracks[0].slotName`이 `DefaultSlot`에서 `UpperBody`로 바뀌었고, 그 안의 `animSegments`·`SequenceLength`·`BlendIn`·`BlendOut`은 전부 그대로다.

`SK_Mannequin` — `SlotGroups`의 `DefaultGroup`에 `UpperBody` 슬롯 이름이 있다. **다만 이번에 추가된 것인지 원래 있던 것인지 구분하지 못했다** — 아래 「확인 못 한 것」 참조.

`BP_ThirdPersonCharacter` — `CanJumpInternal` 오버라이드 함수 그래프가 새로 생겼다. 노드 여섯 개다.

| 노드 | type_id |
| --- | --- |
| `K2Node_FunctionEntry_0` | `\|CanJump` |
| `K2Node_CallParentFunction_0` | `Character\|Parent:CanJump` |
| `K2Node_CallFunction_1` | `Animation\|GetCurrentMontage` |
| `K2Node_PromotableOperator_0` | `Utilities\|Equal(Object)` |
| `K2Node_CommutativeAssociativeBinaryOperator_0` | `Math\|Boolean\|ANDBoolean` |
| `K2Node_FunctionResult_0` | `\|ReturnNode` |

배선은 `Entry.then → Parent.execute`, `Parent.then → Result.execute`, `GetCurrentMontage.ReturnValue → Equal.A`(`Equal.B`는 비움), `Parent.ReturnValue → AND.A`, `Equal.ReturnValue → AND.B`, `AND.ReturnValue → Result.ReturnValue`다.

같은 블루프린트의 `EventGraph`에 노드 셋이 늘었다 — `K2Node_VariableGet_44`(`|GetCharacterMovement`), `K2Node_CallFunction_106`(`Movement|IsFalling`), `K2Node_IfThenElse_13`(`Utilities|FlowControl|Branch`). `IA_Attack` 체인의 `IsValid` 매크로 `Is Not Valid` 출력이 이 `Branch`로 가고, `Branch.else`가 기존 인벤토리 인덱스 검사(`K2Node_IfThenElse_9`)로 간다. `Branch.then`은 비어 있다.

`ABP_Unarmed` — AnimGraph에 노드 다섯이 늘어 8개에서 13개가 됐다. `AnimGraphNode_SaveCachedPose_1`(캐시 이름 `BodyBase`), `AnimGraphNode_UseCachedPose_1`·`_2`, `AnimGraphNode_Slot_1`(`Slot'UpperBody'`), `AnimGraphNode_LayeredBoneBlend_0`이다. 포즈 흐름이 `StateMachine_1 → Slot'DefaultSlot' → SaveCachedPose'BodyBase'` / `UseCachedPose_1 → LayeredBoneBlend.BasePose` / `UseCachedPose_2 → Slot'UpperBody' → LayeredBoneBlend.BlendPoses_0` / `LayeredBoneBlend → ControlRig → Output Pose`가 됐다. 블렌드 노드 설정은 `layerSetup[0].branchFilters[0] = { boneName: spine_01, blendDepth: 1 }`, `blendWeights[0] = 1`, `bBlendRootMotionBasedOnRootBone = true`(기본값 유지)다.

`BP_Enemy` — `EventGraph`의 `RETURN` 분기에서 `K2Node_AIMoveTo_2`와 홉 수식 노드들(`Normalize`, `Min(Float)`, `vector*vector`, `vector+vector`), `GetReturnStepDistance` 게터, `OnFail` 쪽의 `Delay`+`Think`가 지워졌다. 대신 `K2Node_CallFunction_20`(`AI|Navigation|SimpleMoveToLocation`)과 `K2Node_CallFunction_21`(`Pawn|GetController`)이 들어갔다. `Goal` 핀은 그래프에 이미 있던 `K2Node_VariableGet_29`(`GetHomeLocation`)를 재사용했다 — 그 노드의 출력이 이제 `vector-vector`와 `SimpleMoveToLocation.Goal` 두 곳으로 나간다. `ReturnStepDistance` 변수 자체는 남아 있고 `list_variables`가 15개를 그대로 돌려준다.

**도구가 못 한 일이 넷 있었다.** `create_node`가 순수 `IsValid` 함수를 못 만들었고, `K2Node_CallParentFunction`은 `find_node_types`에 아예 없었고, `Use Cached Pose`는 컴파일 뒤에도 목록에 안 떴고, `SK_Mannequin`의 슬롯 등록은 `RegisterSlotNode`가 `UFUNCTION`이 아니라 손댈 수 없었다. 넷 다 사용자가 에디터에서 직접 처리했다.

**중간에 점프가 완전히 막힌 구간이 있었다.** 명령 2가 Stage 2에서 멈추면서 `CanJumpInternal` 오버라이드가 `ReturnValue` 미연결(`false`) 상태로 남았다. 명령문에 "롤백하지 마라"고 적어둔 탓에 에이전트가 그대로 두었고, 사용자가 손으로 `Parent: CanJump`를 연결하고 나서야 풀렸다.

## 분석

### 무엇을 만들었나

**노티파이**

- `AM_Player_Attack`의 `AttackHit` — `LinkValue 0.397855`. 몽타주 길이 1.0초, 30 fps, 프레임 11.94. 사용자가 스크러버로 오른팔이 가장 뻗은 자세를 찾아 그 위치(`0.3965`)로 끌었다
- `EndLink.LinkValue`는 `0.027284`로 남아 있다. 구간형 노티파이(`AnimNotifyState`)에서만 쓰는 끝점 필드라 단발 `Montage Notify`인 지금은 참조되지 않는다
- `FAnimNotifyEvent.NotifyName`은 여전히 `"PlayMontageNotify"`다. 이건 에디터 표시용 캐시고, 블루프린트 분기에 쓰이는 이름은 Notify 오브젝트 안의 별도 `NotifyName` 프로퍼티(`"AttackHit"`)다

**점프 금지 — 함수 그래프**

- `CanJumpInternal` 오버라이드. `ReturnValue = Parent: CanJump AND (GetCurrentMontage == none)`
- 새 변수 없음. 판정 근거는 엔진이 이미 들고 있는 `ACharacter::GetCurrentMontage()` 하나

**점프 금지 — 이벤트 그래프**

- `IA_Attack` 체인에 `Branch(IsFalling)` 하나. `False`로 진행하고 `True`는 비운다
- `GetCharacterMovement → IsFalling → Branch.Condition`
- 위치는 `IsValid` 바로 뒤, 인벤토리 인덱스 검사 앞

**상하체 분리 — 스켈레톤**

- `SK_Mannequin`의 `DefaultGroup`에 `UpperBody` 슬롯. `AdditiveGroup`은 안 건드렸다

**상하체 분리 — AnimGraph**

- `SaveCachedPose 'BodyBase'` / `UseCachedPose` 둘 / `Slot 'UpperBody'` / `LayeredBoneBlend`
- `LayerSetup[0].BranchFilters[0]` = `{ BoneName: spine_01, BlendDepth: 1 }`
- `BlendWeights[0] = 1.0`, `BlendMode = BranchFilter`
- `bBlendRootMotionBasedOnRootBone = true`, `bMeshSpaceRotationBlend = false`, `bMeshSpaceScaleBlend = false` — 전부 생성자 기본값 그대로

**상하체 분리 — 몽타주**

- `AM_Player_Attack.SlotAnimTracks[0].slotName = UpperBody`
- `AM_Enemy_Attack`은 `DefaultSlot` 그대로

**적 복귀**

- `RETURN` 분기가 `PrintString "RETURN"` → `SimpleMoveToLocation(GetController, HomeLocation)` → `Delay(ThinkInterval)` → `Think`
- 튜닝 값은 하나도 안 바뀌었다. `ThinkInterval 0.3` / `ReturnDelay 7` / `ReturnStepDistance 300` / `HomeArriveRadius 100` / `ReturnSightRange 300` / `SightRange 1200` / `SightHalfAngle 60` / `AttackRange 150`

### 기술적으로 맞게 짚은 부분

**`GetCurrentMontage`로 공격 중을 판정하고 새 불리언을 안 만든 것.**
`Character.h:897`이 `UFUNCTION(BlueprintCallable, Category=Animation) UAnimMontage* GetCurrentMontage() const`을 준다. 지난 세션에 연타 방지로 이미 쓰던 것을 점프 금지에도 그대로 썼다. `bIsAttacking` 같은 상태를 따로 들면 그것을 켜고 끄는 자리가 늘고, 몽타주가 중단됐을 때 끄는 걸 잊으면 **영원히 점프 못 하는 버그**가 된다. 엔진이 이미 들고 있는 상태를 읽으면 그 부류가 통째로 사라진다.

**`Parent: CanJump`를 반드시 물리게 한 것.**
`Character.h:871`의 `CanJumpInternal`은 `BlueprintNativeEvent`다. 블루프린트에서 오버라이드하면 **부모 구현이 자동으로 안 불린다.** 기본 구현은 `Character.cpp:313`의 `!IsCrouched() && JumpIsAllowedInternal()`이고, 그 안에 지면 판정과 `JumpMaxCount` 검사가 들어 있다. 부모 호출을 빠뜨리면 공중 무한 점프가 된다. 합격 기준 4("칼을 안 든 상태로 `Space`를 누르면 평소처럼 점프된다")를 이걸 잡으려고 넣었고, 실제로 통과했다.

**에이전트가 `Character|CanJump`를 대체품으로 안 쓴 것.**
`find_node_types`에서 유일하게 걸린 후보가 `Character|CanJump`였고 핀 모양이 정확히 맞았다. 그런데 `Character.cpp:308-310`의 `ACharacter::CanJump()`는 `CanJumpInternal()`을 부른다 — 지금 오버라이드하고 있는 바로 그 함수다. 물렸으면 첫 점프 입력에서 무한 재귀였다. `CanJumpInternal`에 `meta=(DisplayName="CanJump")`가 붙어 있어 **부모 호출과 재귀 호출이 같은 이름으로 보인다.** 소스를 읽고 멈춘 판단이 옳았다.

**미완성 오버라이드를 롤백한 판단(명령 1).**
배선 없는 `Return`은 `false`를 돌려준다. 반쯤 만든 오버라이드는 "아무것도 안 한 것"보다 나쁘다 — 점프가 통째로 죽는데 컴파일은 성공한다. 명령 1에서 에이전트가 스스로 되돌린 것은 정확했다. **반대로 명령 2에서 내가 "롤백하지 마라"고 못박은 것이 틀렸다.**

**`Branch.True`를 비우고 `False`로 진행하게 한 것.**
`NOT` 노드 하나를 아낀다. 결과는 같고, 공중일 때 아무 데도 안 가는 것이 "공격이 안 나간다"를 그대로 표현한다.

**`Equal (Object)`로 뒤집은 것.**
`IsValid` 순수 함수를 못 만드는 벽에 부딪혔을 때 에이전트가 낸 세 안 중 이것을 골랐다. `Not Equal (Object)`를 쓰면 결과를 다시 뒤집어야 해서 `NOT`이 되살아난다. `==`로 비교하면 "몽타주가 없다 = 점프 가능"이 그대로 `AND`에 들어간다. 노드가 원래 계획보다 하나 줄었다.

**캐시 포즈를 쓴 것.**
같은 포즈를 `LayeredBoneBlend`의 베이스와 상체 슬롯 양쪽에 먹여야 한다. 포즈 출력을 두 갈래로 나누면 평가가 중복된다. `ABP_Unarmed`에는 이미 `SaveCachedPose 'Locomotion'`이 있어 패턴도 같다.

**`bBlendRootMotionBasedOnRootBone`을 건드리지 말라고 명시한 것.**
`AnimNode_LayeredBoneBlend.h:126`의 생성자 기본값이 `true`다. 이 값이 `true`면 `.cpp:155`에서 `RootMotionClearWeight = 0`이 되고, `spine_01`부터 블렌드할 때 루트 본의 블렌드 가중치가 0이라 `.cpp:181-192`에서 `RootMotionWeight = 0`·`RootMotionBlendPose = -1`로 떨어진다. 결과가 둘로 갈린다 — 블렌드 포즈(상체 슬롯의 몽타주)는 루트 모션이 제거되고, 베이스 포즈는 `.cpp:205-213`의 `BasePose.Update(Context)`로 그대로 받는다. **플레이어만 안 밀리고 적은 밀리는 것이 이 한 값에 걸려 있다.** 에이전트가 임의로 껐으면 결론이 뒤집혔을 것이다.

**공유 애셋 변경 직전에 "아무것도 안 바뀌어야 하는 상태"에서 PIE를 한 번 돌린 것.**
`ABP_Unarmed`에 `LayeredBoneBlend`를 끼웠지만 `AM_Player_Attack`은 아직 `DefaultSlot`이던 시점이다. 상체 슬롯이 비어 있어 블렌드 결과가 베이스와 같아야 하는 구간이라, **블렌드 노드를 끼운 것 자체가 무해한지**를 슬롯 변경과 분리해서 확인할 수 있었다. 여기서 이상이 났으면 원인이 둘 중 어느 쪽인지 갈리지 않았을 것이다.

**`SimpleMoveToLocation`으로 바꾸면서 `GetHomeLocation` 게터를 재사용하게 한 것.**
그래프에 이미 있던 노드의 출력을 나눠 쓴다. 데이터 핀은 다중 연결이 되므로 두 번째 게터를 만들 이유가 없다.

**`ReturnStepDistance` 변수를 안 지운 것.**
읽는 곳이 없어졌지만 변수는 남겼다. 블루프린트 변수를 지우면 그것을 참조하던 다른 곳이 **컴파일 에러 없이 조용히 끊긴다.** 남기는 비용은 목록에 이름 하나고, 확인하는 비용보다 싸다.

**`RETURN`을 `CHASE`와 같은 모양으로 맞춘 것.**
`CHASE`는 이미 `SimpleMoveToActor` + `Delay(ThinkInterval)` + `Think`였다. `RETURN`만 래턴트 `AIMoveTo`로 남아 있었다. 두 분기가 같은 골격을 쓰면 나중에 한쪽을 고칠 때 다른 쪽을 잊는 일이 준다.

### 확인한 것 / 확인 못 한 것

**확인한 것 — PIE에서 실제로 본 것**

- 팔이 휘둘릴 때 타격 판정이 나온다. `AttackHit` 이동이 실제로 먹었다
- 서서 `LMB`를 누른 직후 `Space`를 누르면 점프가 안 된다
- 공격 몽타주가 끝난 뒤 `Space`를 누르면 점프가 된다
- 칼을 안 든 상태로 `Space`를 누르면 평소처럼 점프된다 — `Parent: CanJump`가 물려 지면 판정이 살아 있다
- 공중에 있는 동안 `LMB`를 누르면 공격이 나가지 않는다
- 공중에서 `LMB`를 누른 뒤 착지하면 다시 `LMB`가 정상으로 먹는다
- `LayeredBoneBlend`를 끼우고 슬롯은 아직 안 바꾼 중간 상태에서, 플레이어와 적 둘 다 이전과 똑같았다
- 달리면서 `LMB`를 누르면 다리가 달리는 동작을 유지한다
- 달리면서 `LMB`를 눌러도 앞으로 밀리지 않는다
- 적은 전신으로 공격하고 앞으로 밀린다 — 상하체 분리 전과 같다
- 서서 `LMB`를 누르면 `Hit:` 출력이 그대로 나온다
- 적을 유인했다가 시야에서 벗어나면 집으로 멈칫거리지 않고 이어서 이동한다
- 복귀 중 적 앞에 나타나면 곧바로 `CHASE`로 바뀐다
- 적이 집에 도착하면 `IDLE_HOME`이 뜨고 원래 방향으로 돌아본다
- `RETURN` 줄 간격이 짧아졌다

**확인한 것 — MCP로 실제 상태를 다시 읽은 것**

- `AttackHit`의 `LinkValue`가 `0.397855`, `LinkedSequence`가 `MM_Attack_01`
- Notify 오브젝트의 `NotifyName`이 `"AttackHit"`
- `SK_Mannequin`의 `SlotGroups`에 `UpperBody`가 있다
- `CanJumpInternal` 그래프의 노드 여섯과 배선 전부
- `EventGraph`의 공중 차단 노드 셋과 배선
- `LayeredBoneBlend`의 `layerSetup`·`blendWeights`·`bBlendRootMotionBasedOnRootBone` — **써놓고 다시 읽어서 대조했다**
- AnimGraph 최종 포즈 흐름
- `AM_Player_Attack.SlotAnimTracks[0].slotName = UpperBody`이고 나머지 필드가 그대로인 것
- `BP_Enemy`의 `RETURN` 분기 최종 형태, `AIMoveTo`·`Normalize`·`GetReturnStepDistance` 게터가 사라진 것, `ReturnStepDistance` 변수가 남아 있는 것
- 컴파일 8회 전부 `LogBlueprint`에 경고·에러 없음
- 다섯 애셋 모두 디스크에 저장된 것 (파일 시각과 크기 변화로)

**확인 못 한 것**

- **`UpperBody` 슬롯이 이번에 추가된 것인지 원래 있던 것인지.** `SlotGroups`를 읽는 방법을 슬롯 등록을 끝낸 **뒤에야** 찾았다. 목록에 `FullBodyAdditivePreAim`·`UpperBodyDynAdditiveBase` 같은 Epic 템플릿 슬롯이 함께 있어서, `UpperBody`도 원래 있었을 가능성이 남는다. 결정 사다리 2번("이 프로젝트에 이미 있는가")을 먼저 밟았어야 하는데 순서가 뒤집혔다
- **`SK_Mannequin.uasset`이 왜 수정으로 잡혔는지.** 슬롯이 추가돼서인지, `Save`가 재직렬화만 한 것인지 구분 못 한다. 바이너리라 못 읽는다
- **`Use cached pose 'BodyBase'`가 왜 `find_node_types`에 안 떴는지.** `AnimGraphNode_UseCachedPose.cpp:128-142`의 `GetMenuActions`는 `FBlueprintEditorUtils::GetAllNodesOfClass`로 그래프를 직접 훑으므로 컴파일과 무관하다. 그런데 컴파일 뒤에도 안 떴고, 같은 순간 에디터 우클릭 메뉴에는 떴다. 액션 데이터베이스 갱신 문제로 보이지만 **확인하지 않았다**
- **`EventGraph` 노드 수가 정말 143인지.** 새 노드 셋을 개별로 확인했으니 140 + 3이 맞지만, 목록을 세어 대조하지는 않았다
- **복귀 속도가 실제로 빨라졌는지.** 물었으나 답을 못 받았다. 기록에 "복귀가 초당 45로 느려진 원인은 `AcceptanceRadius 0`" 가설이 미확인으로 남아 있는데, 이번 변경이 그 가설을 검증할 자리였다
- **`AttackMontage`·`AttackRange`·`AttackTraceRadius`와 `BP_Enemy`의 여섯 변수, 합쳐서 아홉 개의 인스턴스 편집 표시.** `set_variable_instance_editable`은 있는데 get이 없어 AI가 읽을 수단이 없다. 지난 세션에서 이월된 그대로다
- **`ControlRig` 아래의 `NOT`과 `Is Falling` 노드가 무엇을 하는지.** `Is Falling` 변수 → `NOT` → `ShouldDoIKTrace` 배선인 것은 읽었지만, `ABP_Unarmed`에 왜 그런 IK 게이트가 있는지는 안 봤다
- **`SaveCachedPose 'BodyBase'`의 `NOTE` 배지가 실제로 사라졌는지.** `Pose` 입력이 연결됐으니 사라져야 하는데 화면을 다시 안 봤다
- **`skeletonGuid`가 `00000000-...`인 것.** 블렌드 노드를 읽었을 때 전부 0이었다. 컴파일 때 채워지는 값으로 보이나 확인 안 했다

### 남는 리스크

**공유 애셋 둘을 건드렸다.** `ABP_Unarmed`와 `SK_Mannequin`은 `BP_Enemy`가 함께 쓴다. 합격 기준 3으로 적이 그대로인 것을 확인했지만, 앞으로 적 쪽에서 이상한 것이 나오면 여기부터 의심할 자리다. 특히 `LayeredBoneBlend`는 적의 포즈도 반드시 통과한다.

**적은 공격 중 여전히 앞으로 밀리고 다리도 멈춘다.** 의도한 것이 아니라 "플레이어만 분리한다"는 결정에 딸려온 것이다. 적이 달려들며 치는 모양이라 문제로 보이지 않지만, 적이 제자리에서 칠 때 다리가 멈추는 것은 **확인 안 했다.**

**`GetCurrentMontage`는 어떤 몽타주든 유효를 돌려준다.** 지금 플레이어가 재생하는 몽타주가 `AM_Player_Attack` 하나뿐이라 구분이 필요 없었다. 피격 반응 같은 몽타주가 생기면 **그 몽타주 재생 중에도 점프가 막힌다.** 그때는 몽타주를 지정해 비교해야 한다.

**`Equal (Object)`의 B 핀이 비어 있는 것에 의존한다.** 누군가 그 핀에 무언가를 꽂으면 조건이 조용히 바뀐다. 눈으로는 "빈 핀"이라 의도가 안 보인다.

**`GetController`의 `self` 핀이 비어 있다.** `KismetCompiler.cpp:2185`가 self 호환성을 검증하고 통과시키므로 정상이지만, `BP_Enemy`의 다른 분기는 전부 `self`를 명시하고 있어 **이 한 곳만 모양이 다르다.** 나중에 읽는 사람이 실수로 본다.

**디버그 표시가 그대로 쌓여 있다.** `BP_Enemy`의 `PrintString` 여덟 개와 `ToString(Float)` 셋, `BP_ThirdPersonCharacter`의 `PrintString` 열 개와 `DrawDebugType ForDuration` 하나. 지난 세션부터 이월된 항목이고 이번에도 안 건드렸다.

**`ReturnStepDistance 300`이 읽히지 않는 값으로 남았다.** 나중에 이 값을 바꾸고 "왜 안 변하지" 하는 일이 생길 수 있다.

**`EndLink.LinkValue`가 `0.027284`로 남아 있다.** 지금은 참조되지 않지만 노티파이를 구간형(`Montage Notify Window`)으로 바꾸면 그 값이 살아난다. 칼 궤적 트레이스를 만들 때가 그때다.

**`FAnimNotifyEvent.NotifyName` 표시 캐시가 `"PlayMontageNotify"`로 어긋나 있다.** 동작에는 영향이 없지만 콘솔로 노티파이를 읽는 사람이 이름을 보고 헷갈린다.

**노드 여섯 개를 지웠다.** `RETURN` 분기의 `AIMoveTo`와 홉 수식들이다. 되돌리려면 다시 만들어야 한다. 삭제 전에 다른 소비자가 없는지 확인하게 했지만, 그 확인 결과의 원문은 못 받았다.

### 총평

요청은 넷이었고 넷 다 만들었다. 합격 기준도 전부 PIE에서 통과했다.

**실질적 난이도는 만드는 것이 아니라 도구가 못 하는 일을 알아내는 데 있었다.** 여섯 번의 명령 중 셋이 도구 한계로 중간에 멈췄고, 그때마다 원인을 엔진 소스에서 확인한 뒤에야 다음 수가 나왔다. `create_node`의 `declaring_class`가 무기력하다는 것, `K2Node_CallParentFunction`이 노드 스포너가 아니라는 것, `Use Cached Pose`가 액션 목록에 안 뜬다는 것 — 셋 다 시도하기 전에는 알 수 없었고, 알고 나니 우회로가 명확했다.

**가장 비쌌던 실수는 내 명령문에 있었다.** "각 단계가 멈춰도 안전하다"는 전제를 검증 없이 쓰고 그 위에 "롤백하지 마라"를 얹었다. Stage 2가 실패하면서 점프가 통째로 막힌 채 남았고, 사용자가 손으로 `Parent: CanJump`를 연결할 때까지 풀리지 않았다. 에이전트는 그 자리에서 전제가 틀렸다고 짚었는데, 내 지시가 그것을 막았다.

**두 번째 실수는 진단을 남의 말로 받은 것이다.** "캐시가 컴파일돼야 `Use Cached Pose`가 생긴다"는 에이전트의 진단을 받아들여 중간 컴파일을 허용하는 명령을 냈고, 그것도 실패했다. 그 뒤에 소스를 읽으니 `GetMenuActions`는 컴파일 결과를 아예 안 본다. 적을 T-포즈로 만드는 "깨진 창" 경로까지 검토했는데, 사용자가 우클릭 한 번 하니 메뉴에 그냥 있었다. **먼저 화면을 보게 했으면 왕복 두 번이 없었다.**

반대로 잘 된 것은 **공유 애셋을 건드리기 직전에 "아무것도 안 바뀌어야 하는 상태"를 만들어 PIE를 한 번 돌린 것**이다. `LayeredBoneBlend`를 끼운 것과 슬롯을 바꾼 것을 분리해서 확인할 수 있었고, 만약 이상이 났다면 원인이 어느 쪽인지 바로 갈렸다.

그리고 **루트 모션 결론을 소스에서 먼저 읽은 것**이 사양을 단단하게 만들었다. `bBlendRootMotionBasedOnRootBone`이 기본 `true`라는 사실 하나로 "플레이어만 안 밀리고 적은 밀린다"가 예측됐고, PIE에서 그대로 나왔다. 사용자가 "분리 후에 보고 정한다"고 미뤄둔 항목이 별도 작업 없이 닫혔다.

## AI의 제안

1. **`Equal (Object)`로 로직을 뒤집자 (에이전트의 3안 채택)**
   > Invert the logic to remove the NOT: Parent: CanJump AND (GetCurrentMontage == none). Same node count, no IsValid at all.

   얻는 것 — 만들 수 없는 노드를 피하면서 노드가 오히려 하나 준다. 잃는 것 — 없다. `Equal (Object)`의 B 핀이 비어 있는 것에 의존하게 되지만, 그건 표준적인 null 비교 방식이다.

2. **공유 애셋 변경 직전에 "아무것도 안 바뀌어야 하는 상태"에서 PIE를 돌리자**
   > 지금은 `AM_Player_Attack`이 아직 `DefaultSlot`이라 화면에서 아무것도 달라지지 않아야 하는 상태다. 즉 `LayeredBoneBlend`를 끼운 것 자체가 무해한지를 지금 딱 한 번 공짜로 확인할 수 있다.

   얻는 것 — 블렌드 노드 삽입과 슬롯 변경을 분리해서 검증한다. 이상이 나면 원인이 어느 쪽인지 바로 갈린다. 잃는 것 — PIE 한 번의 시간뿐이다.

3. **`AttackHit` 노티파이를 옮길 프레임은 사용자가 고르자**
   > 목표 프레임은 스크러빙해서 직접 고르는 것이 맞다 — 내가 숫자를 정하면 그건 사용자가 말한 값이 아니라 내가 지어낸 값이 된다.

   얻는 것 — 튜닝 값의 주인이 사용자로 남는다. 잃는 것 — 왕복 한 번. 다만 "어느 손으로 치는가"를 확인 안 하고 골랐다가 왕복 두 번을 쓴 지난 세션의 전례가 있어서, 이번에는 손 확인까지 물었다.

4. **`ReturnStepDistance` 변수는 지우지 말자**
   > 읽는 곳이 없어지지만 변수를 지우면 다른 데서 참조할 때 컴파일 에러 없이 조용히 끊긴다. 남기는 비용이 확인하는 비용보다 싸다.

   얻는 것 — 조용히 끊기는 부류의 사고를 통째로 피한다. 잃는 것 — 읽히지 않는 값이 목록에 남아, 나중에 이 값을 바꾸고 "왜 안 변하지" 할 여지가 생긴다.

5. **먼저 에디터에서 우클릭해보자**
   > `ABP_Unarmed`의 AnimGraph를 열고 빈 곳에 우클릭한 뒤 검색창에 `BodyBase`를 쳐달라. 화면만 보면 되는 일이라 30초면 갈린다.

   얻는 것 — 적을 T-포즈로 만드는 깨진 창 경로를 안 밟아도 됐다. 잃는 것 — 없다. **다만 이 제안을 두 턴 늦게 꺼냈다.** 에이전트의 진단을 먼저 받아들여 중간 컴파일 명령을 낸 왕복이 그 사이에 있었다.

## 다음으로 넘김

**바로 이어서 할 것**

- **인스턴스 편집 표시 확인 아홉 개.** `AttackMontage`·`AttackRange`·`AttackTraceRadius` + `BP_Enemy`의 앞선 넷 + `RespawnDelay` + `SightHalfAngle`. My Blueprint 패널의 눈 아이콘. **`set_variable_instance_editable`은 있는데 get이 없어 AI가 읽을 수단이 없음이 확정됐다.** 지난 세션부터 그대로 이월된 유일한 항목이다
- **복귀 속도가 빨라졌는지 확인.** 이번 변경이 "복귀가 초당 45로 느려진 원인은 `AcceptanceRadius 0`" 가설을 검증하는 자리였는데 답을 못 받았다. 빨라졌으면 가설이 맞은 것이고, 그대로면 원인이 다른 데 있다

**결정 필요**

- **디버그 표시 제거 시점.** `BP_Enemy`의 `PrintString` 8개 + `ToString(Float)` 3개, `BP_ThirdPersonCharacter`의 `PrintString` 10개 + `ToString(Float)` 3개 + `DrawDebugType ForDuration` 하나. 합격 기준을 이걸로 읽고 있어서 지금 지우면 검증 수단이 없어진다
- **`GetController`의 빈 `self` 핀을 명시로 바꿀 것인가.** 동작은 정상이지만 `BP_Enemy`의 다른 분기와 모양이 다르다
- **칼 손잡이 오프셋.** `heldTransform.location`에 `(0, 0, 25)` 또는 `(0, 0, -25)`. 부호는 PIE에서 봐야 안다
- **칸막이 `SM_Cube2`를 `Divider_L`로 리네임할 것인가.** 짝이 `SM_Cube2` / `Divider_R`로 어긋나 있다

**확인 필요**

- **`UpperBody` 슬롯이 원래 있었는지 이번에 추가됐는지.** 다음에 `SK_Mannequin`을 건드릴 일이 있으면 그 전에 `GetAll Skeleton SlotGroups Name=SK_Mannequin`을 먼저 찍어두면 같은 혼동이 안 생긴다
- **`Use cached pose 'BodyBase'`가 왜 `find_node_types`에 안 떴는지.** 에디터 메뉴에는 같은 순간에 떴다. 액션 데이터베이스 갱신 문제로 보이나 확인 안 함
- **적이 제자리에서 공격할 때 다리가 멈추는 것이 티가 나는지.** 적은 전신 몽타주를 그대로 쓴다
- **`SaveCachedPose 'BodyBase'`의 `NOTE` 배지가 사라졌는지**
- **`ABP_Unarmed`의 `Is Falling` → `NOT` → `ShouldDoIKTrace` 배선이 무엇을 하는지**
- **`MM_ChargedAttack`이 어떤 동작인지.** 유일하게 안 열어본 공격 시퀀스다
- **막대의 긴 축 `Y`는 어느 방향인지.** `Z`·`X`는 봤고 둘 다 팔 방향이 아니었다
- **`BP_Enemy`가 왜 `BP_ThirdPersonCharacter` 컴파일에 딸려 dirty가 되는지.** 참조 사슬이 안 보인다
- **재직렬화된 `.uasset`들의 내용이 실제로 안 바뀌었는지.** 바이너리라 못 읽는다
- **`LogCrowdFollowing: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance`.** PIE 종료 무렵마다 나온다
- **`LogModelContextProtocol: Error: Call to unknown method "server/discover"`.** 세션 시작 무렵 한 번 찍힌다
- **`EditorPerProjectUserSettings.ini` 저장 실패 (`Error Code 183`).** 열 번 재시도 후 최종 실패했다
- **`read_graph_dsl`과 `write_graph_dsl`의 id 체계가 다른 이유.** 누적 세 종류
- **`find_node_types`와 `get_node_type_pins`의 type_id 표기가 다른 이유.** `SimpleMovetoActor` / `SimpleMoveToActor`
- **MCP 읽기/쓰기 모양 비대칭.** `heldTransform`은 쓸 때 `location/rotation/scale`, 읽을 때 `Translation/Rotation(쿼터니언)/Scale3D`
- **`CaptureViewport`가 PIE 화면이 아니라 에디터 월드를 렌더하는 것**
- **MCP가 못 읽는 프로퍼티 목록.** `AttachSocketName`, `attachParent`, `CollisionEnabled`, `Notifies`, `bEnableRootMotionTranslation`, `bEnableRootMotionRotation`, `bRootMotionSettingsCopiedFromMontage`, `SlotGroups`, `SlotToGroupNameMap`. **이번에 갈래가 둘로 나뉘는 것이 확인됐다** — `Notifies`·`SlotGroups`는 `UPROPERTY`이긴 하나 edit 지정자가 없어 MCP만 거부하고 콘솔 `GETALL`로는 읽힌다. `SlotToGroupNameMap`은 `UPROPERTY`가 아예 없어(`Skeleton.h:548-549`, 런타임 전용) 어느 쪽으로도 못 읽는다
- **MCP로는 만들 수 없는 노드 목록.** `K2Node_CallParentFunction`(노드 스포너가 아니라 에디터 컨텍스트 액션 `FBlueprintEditor::OnAddParentNode`), 순수 `IsValid`(`type_id`가 매크로와 같고 `declaring_class`가 무기력), `Use Cached Pose`(에디터에는 뜨는데 `find_node_types`에는 안 뜸)
- **`Knife`의 `displayName` NSLOCTEXT 네임스페이스가 기존 행과 다른 이유**
- **`DisableInput`이 Enhanced Input 매핑까지 막는지**
- **HUD의 `CachedCharacter` 재획득이 실제로 일어나는지**
- **2번 방의 조명.** `DirectionalLight`·`SkyLight` 외에 아무것도 없다
- **`bCanEverTick`이 명령 56 직후 `false`로 읽혔던 이유**
- **`trace_world`가 방향에 따라 같은 솔리드를 놓치는 이유**
- **`show navigation`이 PIE에서 안 먹는 이유.** 에디터 뷰포트의 `P`로 우회했다
- **외부 액터 패키지와 `__ExternalObjects__` 파일의 정체**
- **`Lvl_ArenaShooter`의 WorldSettings가 `BP_ShooterGameMode`를 가리키는지**

**접어둔 것**

- **적 HP·피격·사망.** 다음 사양의 본체다. 만들 때 **플레이어의 `PrintString`을 `ApplyDamage`로 올려야 적과 짝이 맞는다**
- **적 공격에도 히트 판정 붙이기.** 지금은 `PlayAnimMontage → ApplyDamage → Delay`로 무조건 맞는다. 바꾸는 데 필요한 것 셋 — (1) `PlayAnimMontage`를 `Play Montage`로 교체, (2) `AM_Enemy_Attack`에 `Montage Notify` 찍기(수작업), (3) `ApplyDamage`를 노티파이 분기 뒤 트레이스 성공 쪽으로 옮기기
- **칼 메시 구하기.** 리타깃 비용이 애셋 고르는 기준에 들어가야 한다. 루트 모션이 켜져 있는지도 봐야 한다
- **칼 궤적 트레이스.** 밑동·칼끝 소켓 사이를 매 프레임 훑는 방식. `Play Montage`의 `OnNotifyEnd` 핀이 비어 있어 `Montage Notify Window`로 바꾸면 그대로 올라간다. **바꾸면 `EndLink.LinkValue`가 살아나므로 그 값도 같이 봐야 한다**
- **카메라 작업.** 셋으로 갈렸다
  - **A — 원본 ICI 구조(`캡슐 → Camera → SkeletalMesh`)로 교체.** 팔만 있는 스켈레탈 메시가 프로젝트에 없어 지금 그대로는 못 한다
  - **B — 지금 구조를 두고 팔을 시야로 올린다.** `Variant_Shooter/Anims/ABP_FP_Weapon` + `Ctrl_HandAdjusment`
  - **C — 전환 스냅 완화만.** 요 보간 또는 `SetViewTargetWithBlend`. 2026-08-27부터 이월
- **1인칭으로 죽으면 3인칭으로 부활하는 것.** 사용자가 `내비두자`로 정했다
- **30초 갇힘 사망**
- **사망 시 아이템 드롭**
- **게임오버 화면 · 사망 카운트 · 체크포인트**
- **적 체력바 위젯 / 순찰 / EQS / 여러 적의 회피 / 적 종류별 DataTable**
- **소리 감지 · 여러 적의 정보 공유 · "뭔가 봤다" 중간 경계 상태**
- **여러 적을 한 번에 때리기.** `SphereTraceForObjects`의 `Multi` 버전으로 노드 하나 교체
- **`BP_ShooterNPC` · `ST_Shooter` · EQS 3개 · StateTree 태스크 6개.** 안 쓰기로 했지만 지우지 않는다
- **`--append-system-prompt`가 저장소에 없다.** `Editor Preferences → General → Terminal → Startup Commands`의 사용자 설정이다. 원문은 `Docs/AI-Log/2026-08-28-inventory-item-data.md`의 `명령` 칸에 있다
- **`BP_Door.uasset`의 재직렬화.** 참조하는 블루프린트를 컴파일하면 딸려 dirty가 된다
- **문간 위 `X 1800..1900, Z 200..400`의 열린 홈.** 관통은 아니다
- **열린 문짝 20cm가 문간 위로 삐져나온다.** 문짝 220, 문간 200
- **`ForLoop.FirstIndex`가 빈 값인 이유.** 동작에 지장이 없다
- **`SP` 스태미나.** 원본에 있고 MCP1에 없다. `06-플레이어-UI.md:54` 참조
- **슬롯 2칸 vs 3칸.** 원본은 2칸, MCP1은 3칸이다
- **미사용 애셋 정리.** 2026-08-30에 **남기기로** 정했다
- **`MoveComponentTo`의 `Stop`·`Return` 핀.** 연타로는 문제가 안 났다
- **칼 픽업이 바닥에 파묻히는 것.** 기존 픽업 6개도 같다
- **`Knife`와 `Key_Stage1`이 같은 메시라 색이 같은 것.** 머티리얼로 가를 수 있다
