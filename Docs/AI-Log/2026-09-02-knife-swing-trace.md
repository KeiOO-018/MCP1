# 2026-09-02

## 작업물

플레이어가 칼을 휘두르는 동안 칼날이 지나간 궤적으로 타격을 판정하는 것 — 타격 창이 열린 동안 매 프레임 이전 칼 위치에서 현재 칼 위치까지 칼 모양 상자를 훑고, 한 스윙에 같은 적은 한 번만 때린다. 그리고 칼의 회전값 확정.

**소요 시간**: UE 출력 로그 타임스탬프에 남은 범위로 `02:01:05` → `02:19:07`, 약 18분. 다만 그 앞의 조사·심문·사양·명령 작성 구간과, 뒤의 칼 회전 확인 PIE 세 번은 로그에 안 남아서 **실제 벽시계 시간은 이보다 길다.** 세션 시작 시각을 기록하지 않아 정확한 값을 모른다.

## 명령

### 한글

```
작업 준비
```
```
4 칼의 회전이랑 칼을 휘둘렀을 때 그 휘두르는 검귀라고 하나 그거대로 히트판정을 만들고싶은데 나중에칼날 부분이 직접 닿나 안닿나로 해서 데미지 계산하게 하고싶은데 이에 대해서 먼저 설계
```
```
1. C
2. a
3. a
4. a
5. a
6. a
7. 사진첨부
8. 이펙트가 필요한건아님, 플레이어의 공격방식이 완벽히 문제없이 만들어지면, 이를 적 AI 한테도 적용하는게 더 나은 방법인듯함, 구조체 칸은 내가 요청하면 추가해줌
```
```
가자 해보고 정안되면 바꾸지뭐
```
```
결과 확인
```
```
이게 고민인게 원본이 그냥 오른주먹 날리는 모션인데 여기에 칼넣으면 이상해지지 않을까 고민 애니메이션 칼 휘두루는걸 외부무료 사이트에서 구해야하나 Mixamo.com 같은곳에서
```
```
1. 셋다 칼이랑 관련없음
```
```
저거 위에 명령 2 수작업 했어 확인좀
```
```
이거임
```
```
결과 확인
```
```
결과 확인
```
```
결과 확인
```
```
그 두번째 공격인가 그거가 한번 때렸는데 드르륵맞은거같은데 다른건 다 잘 되거든? 그것들 확인좀
```
```
지금 결과바바
```
```
스윙 열번했어
```
```
했어 확인좀
```
```
결과 확인해봐
```
```
결과 확인
```
```
그리고 빨간 디버그 상자랑 막대랑 겹쳐서 보임
```
```
B
```
```
이거바바 왼쪽으로 돌려진거같은데 확인좀
```
```
이번엔 칼이 위를 보고있는데 팔에 박혀있어 이거 앞을 향하게 해야하나 이러면 처음 캐릭터 기본이 차렷자세비슷하니까
```
```
잘됬네
```
```
기록하자
```

### English — MCP에 실제로 보낸 명령

**이 세션에서 영어 명령은 내가 MCP로 보낸 것이 아니다.** 전부 **사용자가 UE Terminal에 붙여넣도록 만들어 건넨 원문**이다. 내가 직접 부른 MCP는 전부 읽기 호출이었다 — `list_toolsets`, `describe_toolset`, `find_nodes`, `get_node_infos`, `get_connected_subgraph`, `list_variables`, `get_variable_category`, `get_properties`, `get_default_object`, `get_rows`, `get_socket_names`, `get_socket_transform`, `get_socket_bone`, `GetLogEntries`. 아래는 Terminal에 건넨 영어 원문 그대로다.

명령 2는 영어 명령이 없다. MCP가 노티파이를 못 써서 몽타주 에디터 수작업이었다.

**명령 1 — 변수 다섯 개**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, add five new variables:

1. Name "bIsSwinging", type Boolean, default value false, not instance editable.
2. Name "PrevBladeCenter", type Vector, default value (0, 0, 0), not instance editable.
3. Name "HitActorsThisSwing", type Actor object reference, as an ARRAY, not instance editable.
4. Name "BladeHalfLength", type Float, default value 25.0, instance editable.
5. Name "BladeRadius", type Float, default value 3.0, instance editable.

Leave all five in the "Default" category, the same category the existing AttackRange
variable uses. Do not touch any existing variable. Do not change any existing node.

Then compile the Blueprint, list all variables on it, and report each of the five new
variables with its type, whether it is an array, its default value, and whether it is
instance editable.
```

**명령 3 — 기존 전방 구체 트레이스 제거 · 타격 창 여닫기**

```
Work in the EventGraph of /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.

PART A - delete the old forward sphere trace. Delete exactly these eight nodes:
  - the SphereTraceForObjects node                  (K2Node_CallFunction_83)
  - the Branch immediately after it                 (K2Node_IfThenElse_12)
  - the GetActorLocation node                       (K2Node_CallFunction_81)
  - the GetActorForwardVector node                  (K2Node_CallFunction_82)
  - the vector * vector node                        (K2Node_PromotableOperator_23)
  - the vector + vector node                        (K2Node_PromotableOperator_24)
  - the AttackRange variable getter                 (K2Node_VariableGet_34)
  - the AttackTraceRadius variable getter           (K2Node_VariableGet_35)

Do NOT delete these - they are reused in the next step, leave them in place even
though they end up unconnected:
  - the MakeArray node holding ObjectTypeQuery3     (K2Node_MakeArray_0)
  - the BreakHitResult node                         (K2Node_CallFunction_84)
  - the GetDisplayName node                         (K2Node_CallFunction_85)
  - the Append node                                 (K2Node_CommutativeAssociativeBinaryOperator_3)
  - the PrintString node                            (K2Node_CallFunction_86)
  - the ApplyDamage node                            (K2Node_CallFunction_61)
  - the GetController node                          (K2Node_CallFunction_62)
  - the Self reference node                         (K2Node_Self_1)
  - the AttackDamage variable getter                (K2Node_VariableGet_26)

Do not delete or change the Play Montage node, the Name Equal node comparing
NotifyName to "AttackHit", or the Branch it feeds (K2Node_IfThenElse_11).

PART B - open the hit window. From the True pin of that existing Branch
(K2Node_IfThenElse_11), run this exec chain in order:
  1. Set bIsSwinging = true
  2. Clear the HitActorsThisSwing array (the array Clear node)
  3. Set PrevBladeCenter to the result of HeldItemMesh -> GetWorldLocation
     (get the HeldItemMesh component reference, call GetWorldLocation on it,
      feed that into the PrevBladeCenter setter)

PART C - close the hit window. Add one Set bIsSwinging = false node, and drive it
from three places:
  1. Play Montage's OnNotifyEnd pin -> a new Name Equal node comparing that pin's
     NotifyName output to the literal Name "AttackHit" -> a new Branch -> True pin
     -> the Set bIsSwinging = false node
  2. Play Montage's OnInterrupted pin -> the same Set bIsSwinging = false node
  3. Play Montage's OnBlendOut pin    -> the same Set bIsSwinging = false node

Then compile the Blueprint and report: any compile errors or warnings, the full list
of nodes now connected to the Play Montage node, and the current value of
bIsSwinging on the class defaults.
```

**명령 4 — Tick 스윕 (캡슐 버전, 나중에 틀린 것으로 판명)**

```
Work in the EventGraph of /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.
Add a new Event Tick node and build this chain. Reuse the existing nodes named below
instead of creating new ones.

1. Event Tick -> Branch, condition = the bIsSwinging variable getter.

2. From that Branch's True pin, call CapsuleTraceMultiForObjects
   (the MULTI version, for objects - not the single version, not the channel version).
   Wire its inputs:
     Start        = the PrevBladeCenter variable getter
     End          = HeldItemMesh -> GetWorldLocation
     Radius       = the BladeRadius variable getter
     HalfHeight   = the BladeHalfLength variable getter
     Orientation  = HeldItemMesh -> GetWorldRotation
     ObjectTypes  = the EXISTING MakeArray node holding ObjectTypeQuery3 (K2Node_MakeArray_0)
     bIgnoreSelf  = true
     DrawDebugType = ForDuration
     DrawTime     = 0.5

3. From CapsuleTraceMultiForObjects' exec output, run a ForEachLoop over its
   OutHits array output.

4. Inside the loop body:
   a. Feed the loop's Array Element (a Hit Result) into the Hit input of the EXISTING
      BreakHitResult node (K2Node_CallFunction_84).
   b. Add an "Array Contains Item" node: array = the HitActorsThisSwing getter,
      item = that BreakHitResult's HitActor output.
   c. Feed Contains into a NOT Boolean node, and that into a new Branch's condition.
   d. Loop body exec -> that new Branch.
   e. Branch True -> "Array Add" node (array = HitActorsThisSwing, item = the same
      HitActor output) -> then into the exec input of the EXISTING PrintString node
      (K2Node_CallFunction_86), which already flows on into the existing ApplyDamage
      node (K2Node_CallFunction_61). Do not rewire PrintString's string input or
      ApplyDamage's inputs - they are already connected.

5. From the ForEachLoop's Completed pin, Set PrevBladeCenter to
   HeldItemMesh -> GetWorldLocation (a second GetWorldLocation call is fine).

Then compile the Blueprint and report: any compile errors or warnings, the full node
list connected to the new Event Tick node, and whether the Blueprint's class defaults
have Actor Tick "Start with Tick Enabled" checked.
```

**명령 5 — 박스 트레이스로 교체**

```
In the EventGraph of /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter,
replace the trace node with the box version, because the capsule version has no
orientation input.

1. Delete the CapsuleTraceMultiForObjects node (K2Node_CallFunction_14).

2. Create a BoxTraceMultiForObjects node (the MULTI version, for objects) and wire it:
     exec in      = the True pin of the Branch fed by Event Tick (K2Node_IfThenElse_15)
     Start        = the existing PrevBladeCenter getter          (K2Node_VariableGet_10)
     End          = the existing GetWorldLocation node           (K2Node_CallFunction_18)
     HalfSize     = a new Make Vector node wired as:
                      X = the existing BladeRadius getter        (K2Node_VariableGet_12)
                      Y = the same BladeRadius getter
                      Z = the existing BladeHalfLength getter    (K2Node_VariableGet_17)
     Orientation  = a new GetWorldRotation call on HeldItemMesh
                    (reuse the existing HeldItemMesh getter K2Node_VariableGet_11)
     ObjectTypes  = the existing MakeArray node                  (K2Node_MakeArray_0)
     bIgnoreSelf  = true
     DrawDebugType = ForDuration
     DrawTime     = 0.5

3. Wire its outputs back into the chain that is already there:
     exec out  -> the existing ForEachLoop node                  (K2Node_MacroInstance_25)
     OutHits   -> that ForEachLoop's Array input

Do not change anything else in that chain - the ForEachLoop body, the Contains/NOT/Branch,
the Array Add, PrintString, ApplyDamage and the Completed -> Set PrevBladeCenter wiring
are all already correct.

Then compile and report any errors or warnings, and list the input pins of the new
BoxTraceMultiForObjects node with their values or the node they are connected to.
```

**명령 6 — 임시 진단 로그 둘**

```
Work in the EventGraph of /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.
Add two temporary PrintString nodes for debugging.

1. On the hit-window OPEN path: insert a PrintString between the Branch that tests
   NotifyName == "AttackHit" off OnNotifyBegin (K2Node_IfThenElse_11) and the
   Set bIsSwinging = true node (K2Node_VariableSet_1). So the order becomes
   Branch True -> new PrintString -> Set bIsSwinging(true) -> Clear -> Set PrevBladeCenter.
   Its InString must be the literal text: WINDOW OPEN

2. On the hit-window CLOSE path: insert a PrintString directly after the
   Set bIsSwinging = false node (K2Node_VariableSet_4), on its "then" pin.
   Its InString must be the literal text: WINDOW CLOSE

For both nodes leave PrintToScreen and PrintToLog at their defaults (both true) and
leave Duration at its default. Do not change anything else.

Then compile and report the exec chain from OnNotifyBegin and from OnNotifyEnd.
```

**명령 7 — 임시 진단 로그 제거**

```
Work in the EventGraph of /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.
Remove the two temporary debug PrintString nodes added earlier:

1. Delete the PrintString whose InString is the literal text "WINDOW OPEN". It sits
   between the Branch that tests NotifyName == "AttackHit" off the Play Montage node's
   OnNotifyBegin pin and the Set bIsSwinging = true node. After deleting it, reconnect
   that Branch's True pin directly to the Set bIsSwinging = true node, so the chain is
   again Branch True -> Set bIsSwinging(true) -> Clear HitActorsThisSwing ->
   Set PrevBladeCenter.

2. Delete the PrintString whose InString is the literal text "WINDOW CLOSE". It hangs
   off the "then" pin of the Set bIsSwinging = false node and nothing follows it.

Do not delete the PrintString whose string comes from an Append node - that one is the
hit report and stays. Do not change anything else.

Then compile and report the exec chain from OnNotifyBegin and from OnNotifyEnd.
```

**명령 8 — 칼 회전 첫 후보값**

```
In the DataTable /Game/Inventory/DT_Items, set the heldTransform property on the
"Knife" row only:
  location = (25, 0, 0)
  rotation = pitch -90, yaw 0, roll 0
  scale    = (0.04, 0.04, 0.5)

Do not touch any other row, and do not touch any other property on the Knife row.
Then read the Knife row back and report its full contents.
```

**명령 9 — 칼 회전 둘째 후보값**

```
In the DataTable /Game/Inventory/DT_Items, set the heldTransform property on the
"Knife" row only:
  location = (0, -25, 0)
  rotation = pitch 0, yaw 0, roll 90
  scale    = (0.04, 0.04, 0.5)

Do not touch any other row, and do not touch any other property on the Knife row.
Then read the Knife row back and report its full contents.
```

**명령 10 — 원래 값으로 되돌리기**

```
In the DataTable /Game/Inventory/DT_Items, set the heldTransform property on the
"Knife" row only:
  location = (0, 0, 25)
  rotation = pitch 0, yaw 0, roll 0
  scale    = (0.04, 0.04, 0.5)

Do not touch any other row, and do not touch any other property on the Knife row.
Then read the Knife row back and report its full contents.
```

**옮기며 넣은 해석**

- 한글의 **"휘두르는 검귀"**를 나는 **"스윙의 궤적을 따라가는 히트 판정"**으로 읽었다. 시각 효과(트레일 VFX)가 아니라 판정으로 읽은 것이고, 심문 8번에서 사용자가 "이펙트가 필요한건아님"으로 확인해줬다.
- **`BladeHalfLength 25.0`** — 한글 지시에 없는 숫자다. `Knife`의 `Scale3D.Z 0.5` × 엔진 `Cube` 반높이 50에서 계산해 내가 정했다.
- **`BladeRadius 3.0`** — 한글 지시에 없는 숫자다. 실제 막대 반두께 2cm에 여유 1cm를 붙여 내가 정했다.
- **`DrawTime 0.5`** — 내가 정했다. 창이 열린 동안 매 프레임 그려지므로 기존 `2.0`을 쓰면 화면이 상자로 덮인다.
- **창을 `OnBlendOut`·`OnInterrupted`에서도 닫는 것** — 사용자가 말한 적 없다. 노티파이 스테이트가 몽타주 중단 시 `End`를 부르는지 확인 못 해서 안전판으로 내가 넣었다.
- **노티파이 이름을 `AttackHit`으로 유지** — 기존 그래프의 `Name Equal` 비교를 그대로 쓰려고 내가 정했다.
- **명령 8·9에서 `location`을 회전과 같이 바꾼 것** — 사용자는 회전만 말했다. 손잡이 오프셋이 칼날 방향을 따라가야 칼이 손에서 자라므로, 같이 돌린 것은 내 판단이다.

## Terminal 결과

### 원문 — English

**UE Terminal 자체의 출력은 이 기록에 없다.** 사용자가 명령 실행 후 터미널 출력을 붙여넣지 않았고, 나는 매번 MCP 읽기 호출과 UE 출력 로그로 실제 상태를 다시 확인하는 방식으로 검증했다. 그래서 아래는 **내가 받은 MCP 응답 원문**과 **UE 출력 로그 원문**이다.

**MCP 실패 응답 — 전문**

```
Function "get_rows", input param "data_table" is required by the function input schema Json, but is missing from the incoming function input params Json.
Function schema Json -
{"type":"object","properties":{"data_table":{"type":"object","title":"/Script/Engine.DataTable","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]},"row_names":{"type":"array","items":{"type":"string"}}},"required":["data_table","row_names"]}
Function input params Json -
{"data_table_path":"/Game/Inventory/DT_Items","row_names":["Knife"]}
```

```
GetObjectProperties on '/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack' (AnimMontage): the following properties could not be read: Notifies, AnimNotifyTracks
```

```
GetObjectProperties on '/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack' (AnimMontage): the following properties could not be read: BranchingPointStateNotifyIndices
```

```
GetObjectProperties on '/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.AM_Player_Attack' (AnimMontage): the following properties could not be read: BranchingPointMarkers, ActiveStateBranchingPoints, CompositeSections
```

```
Parameter error: /Game/ThirdPerson/Blueprints/BP_Enemy.BP_Enemy is not valid Object for property 'instance'.
```

```
Parameter error: /Game/ThirdPerson/Blueprints/BP_Enemy.BP_Enemy is not valid Blueprint for property 'blueprint'.
```

**UE 출력 로그 — 두 번째 창 문제를 잡은 근거. 스윙 열 번 중 앞 세 번만 발췌했다. 열 번 전부 같은 모양이었다.**

```
[2026.09.02-02.13.41:799][345]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.13.41:915][353]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.13.42:002][359]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.13.42:265][377]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.13.43:238][445]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.13.43:338][452]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.13.43:443][459]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.13.43:707][477]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.13.44:551][535]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.13.44:671][543]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.13.44:760][549]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.13.45:020][567]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
```

**같은 로그에 한 번 섞여 있던 세 번째 닫힘 — `OnBlendOut`이 따로 닫은 것**

```
[2026.09.02-02.13.49:479][875]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.13.49:729][892]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.13.49:984][909]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
```

**노티파이 하나를 지운 뒤 — 스윙 다섯 번 중 둘 발췌. 다섯 번 전부 여는 줄이 하나였다.**

```
[2026.09.02-02.17.06:084][745]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.17.06:292][759]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.17.06:531][775]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.17.07:413][835]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.17.07:635][850]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.17.07:889][867]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
```

**최종 검증 — 적을 실제로 때린 스윙 세 번. 전문이다.**

```
[2026.09.02-02.19.00:105][633]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.19.00:283][645]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] Hit: Enemy_Test
[2026.09.02-02.19.00:283][645]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 66.0
[2026.09.02-02.19.00:326][648]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.19.00:574][665]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.19.03:414][892]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.19.03:515][899]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] Hit: Enemy_Test
[2026.09.02-02.19.03:515][899]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 32.0
[2026.09.02-02.19.03:624][906]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.19.03:863][922]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.19.06:911][133]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW OPEN
[2026.09.02-02.19.07:029][141]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] Hit: Enemy_Test
[2026.09.02-02.19.07:029][141]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 0.0
[2026.09.02-02.19.07:119][147]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
[2026.09.02-02.19.07:371][164]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] WINDOW CLOSE
```

**문제를 처음 관측한 로그 — 임시 로그를 넣기 전, 한 스윙이 두 번 맞은 순간. 전문이다.**

```
[2026.09.02-02.01.05:392][661]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] Hit: Enemy_Test
[2026.09.02-02.01.05:392][661]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 66.0
[2026.09.02-02.01.15:692][412]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] Hit: Enemy_Test
[2026.09.02-02.01.15:692][412]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 32.0
[2026.09.02-02.01.15:738][415]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] Hit: Enemy_Test
[2026.09.02-02.01.15:738][415]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 0.0
```

**엔진 소스 — 캡슐과 박스의 차이를 확정한 근거. `KismetSystemLibrary.h`에서 두 줄만 발췌했다.**

```
1478:	static ENGINE_API bool BoxTraceMultiForObjects(const UObject* WorldContextObject, const FVector Start, const FVector End, const FVector HalfSize, const FRotator Orientation, const TArray<TEnumAsByte<EObjectTypeQuery> > & ObjectTypes, bool bTraceComplex, const TArray<AActor*>& ActorsToIgnore, EDrawDebugTrace::Type DrawDebugType, TArray<FHitResult>& OutHits, bool bIgnoreSelf, FLinearColor TraceColor = FLinearColor::Red, FLinearColor TraceHitColor = FLinearColor::Green, float DrawTime = 5.0f);
1512:	static ENGINE_API bool CapsuleTraceMultiForObjects(const UObject* WorldContextObject, const FVector Start, const FVector End, float Radius, float HalfHeight, const TArray<TEnumAsByte<EObjectTypeQuery> > & ObjectTypes, bool bTraceComplex, const TArray<AActor*>& ActorsToIgnore, EDrawDebugTrace::Type DrawDebugType, TArray<FHitResult>& OutHits, bool bIgnoreSelf, FLinearColor TraceColor = FLinearColor::Red, FLinearColor TraceHitColor = FLinearColor::Green, float DrawTime = 5.0f);
```

**엔진 소스 — 노티파이 윈도우가 `Begin`과 `End`를 모두 브로드캐스트한다는 근거. `AnimNotify_PlayMontageNotify.cpp` 발췌.**

```
void UAnimNotify_PlayMontageNotifyWindow::BranchingPointNotifyBegin(FBranchingPointNotifyPayload& BranchingPointPayload)
{
	Super::BranchingPointNotifyBegin(BranchingPointPayload);

	if (USkeletalMeshComponent* MeshComp = BranchingPointPayload.SkelMeshComponent)
	{
		if (UAnimInstance* AnimInstance = MeshComp->GetAnimInstance())
		{
			AnimInstance->OnPlayMontageNotifyBegin.Broadcast(NotifyName, BranchingPointPayload);
		}
	}
}


void UAnimNotify_PlayMontageNotifyWindow::BranchingPointNotifyEnd(FBranchingPointNotifyPayload& BranchingPointPayload)
{
	Super::BranchingPointNotifyEnd(BranchingPointPayload);

	if (USkeletalMeshComponent* MeshComp = BranchingPointPayload.SkelMeshComponent)
	{
		if (UAnimInstance* AnimInstance = MeshComp->GetAnimInstance())
		{
			AnimInstance->OnPlayMontageNotifyEnd.Broadcast(NotifyName, BranchingPointPayload);
		}
	}
}
```

**엔진 소스 — 노티파이 메뉴 문구의 근거. `SAnimNotifyPanel.cpp` 발췌.**

```
				Section.AddSubMenu(TEXT("AddNotify"),
					NSLOCTEXT("NewNotifySubMenu", "NewNotifySubMenuAddNotify", "Add Notify..."),
					NSLOCTEXT("NewNotifySubMenu", "NewNotifySubMenuAddNotifyToolTip", "Add AnimNotifyEvent"),
					FNewMenuDelegate::CreateRaw(SourceTrack.Get(), &SAnimNotifyTrack::FillNewNotifyMenu, false),
					false,
					FSlateIcon());

				Section.AddSubMenu(TEXT("AddNotifyState"),
					NSLOCTEXT("NewNotifySubMenu", "NewNotifySubMenuAddNotifyState", "Add Notify State..."),
					NSLOCTEXT("NewNotifySubMenu", "NewNotifySubMenuAddNotifyStateToolTip", "Add AnimNotifyState"),
					FNewMenuDelegate::CreateRaw(SourceTrack.Get(), &SAnimNotifyTrack::FillNewNotifyStateMenu, false),
					false,
					FSlateIcon());
```

**최종 상태 되읽기 — `DT_Items`의 `Knife` 행**

```
{"Knife": {"displayName": "NSLOCTEXT(\"DT_Items [31D95D90E0F90A083145F5565E5C1688]\", \"Knife_DisplayName\", \"Knife\")", "iconColor": {"R": 0.7, "G": 0.7, "B": 0.75, "A": 1}, "mesh": "/Script/Engine.StaticMesh'/Engine/BasicShapes/Cube.Cube'", "nature": "Holdable", "healAmount": 0, "heldTransform": {"Rotation": {"X": 0, "Y": 0, "Z": 0, "W": 1}, "Translation": {"X": 0, "Y": 0, "Z": 25}, "Scale3D": {"X": 0.04, "Y": 0.04, "Z": 0.5}}}}
```

**작업 후 `git status`**

```
 M Content/Characters/Mannequins/Anims/Unarmed/Attack/AM_Player_Attack.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

### 요약 — 한글

- `BP_ThirdPersonCharacter`에 변수 다섯 개가 생겼다 — `bIsSwinging`(Boolean, `false`), `PrevBladeCenter`(Vector, `0,0,0`), `HitActorsThisSwing`(Actor 배열, 빈 배열), `BladeHalfLength`(Float, `25`), `BladeRadius`(Float, `3`). 전부 `Default` 카테고리.
- `AM_Player_Attack`의 점 노티파이 `AttackHit`이 **노티파이 스테이트(`Montage Notify Window`)로 교체**됐다. 그런데 이때 **두 개가 찍혔고**, 나중에 하나를 지웠다. 최종 창 길이는 열림 → `OnNotifyEnd` 기준 약 0.21초.
- EventGraph에서 노드 여덟 개가 지워졌다 — `SphereTraceForObjects`, 그 뒤 `Branch`, `GetActorLocation`, `GetActorForwardVector`, `vector*vector`, `vector+vector`, `AttackRange` 게터, `AttackTraceRadius` 게터.
- 아홉 개는 남겨서 재사용했다 — `MakeArray`(`ObjectTypeQuery3`), `BreakHitResult`, `GetDisplayName`, `Append`, `PrintString`, `ApplyDamage`, `GetController`, `Self`, `AttackDamage` 게터.
- `OnNotifyBegin` → `Name Equal "AttackHit"` → `Branch` True → `Set bIsSwinging(true)` → `Clear(HitActorsThisSwing)` → `Set PrevBladeCenter ← HeldItemMesh.GetWorldLocation` 체인이 생겼다.
- `Set bIsSwinging(false)` 하나에 세 경로가 물렸다 — `OnNotifyEnd` + 이름 검사, `OnBlendOut`, `OnInterrupted`.
- `Event Tick`이 새로 생겼다. `Branch(bIsSwinging)` → `MultiBoxTraceForObjects` → `ForEachLoop(OutHits)` → `Contains` → `NOT` → `Branch` → `Array Add` → `PrintString` → `ApplyDamage`, 그리고 `Completed` → `Set PrevBladeCenter`.
- 트레이스는 처음 `MultiCapsuleTraceForObjects`로 만들었다가 **`Orientation` 핀이 없어서** `MultiBoxTraceForObjects`로 교체했다. `HalfSize`는 `MakeVector(BladeRadius, BladeRadius, BladeHalfLength)`, `Orientation`은 `HeldItemMesh.GetWorldRotation`.
- `DT_Items`의 `Knife` 행 `heldTransform`을 세 번 바꿨다 — `location (25,0,0)` / `pitch -90` → `location (0,-25,0)` / `roll 90` → **원래 값 `location (0,0,25)` / 회전 단위값으로 복귀.** 최종 상태는 작업 전과 같다.

## 분석

### 무엇을 만들었나

**변수 (`BP_ThirdPersonCharacter`, 다섯 개)**

- `bIsSwinging` — Boolean, 기본값 `false`. 타격 창이 열려 있는지. `Event Tick`의 유일한 게이트다
- `PrevBladeCenter` — Vector, 기본값 `(0,0,0)`. 직전 프레임의 칼 중심 월드 위치
- `HitActorsThisSwing` — Actor 배열, 기본값 빈 배열. 이번 스윙에서 이미 때린 액터
- `BladeHalfLength` — Float, `25.0`, 인스턴스 편집. 엔진 `Cube` 반높이 50 × `Scale3D.Z 0.5`
- `BladeRadius` — Float, `3.0`, 인스턴스 편집. 실제 막대 반두께 2cm + 여유 1cm

**애니메이션 (`AM_Player_Attack`)**

- 슬롯 `UpperBody`, 세그먼트 `MM_Attack_01` 하나, 길이 1초, 블렌드 인/아웃 각 0.25초 `HermiteCubic`. 이건 원래 있던 구성이고 안 건드렸다
- 노티파이 `AttackHit`이 점에서 **구간(`Montage Notify Window`)으로** 바뀌었다. 위치는 대략 프레임 9~14 (약 0.30초 → 0.47초), 눈금 픽셀을 눈대중한 값이다
- 실측 창 길이는 로그 기준 **약 0.21초** (열림 → 첫 닫힘 208~222ms)

**타격 창 (`EventGraph`)**

- 열기 — `Play Montage.OnNotifyBegin` → `Name Equal(NotifyName, "AttackHit")` → `Branch` True → `Set bIsSwinging(true)` → `Clear(HitActorsThisSwing)` → `Set PrevBladeCenter ← HeldItemMesh.GetWorldLocation`
- 닫기 — `Set bIsSwinging(false)` 하나에 세 입력. `OnNotifyEnd` + 이름 검사 `Branch`, `OnBlendOut`, `OnInterrupted`

**궤적 판정 (`Event Tick`)**

- `Branch(bIsSwinging)` — 거짓이면 여기서 끝
- `MultiBoxTraceForObjects` — `Start = PrevBladeCenter`, `End = HeldItemMesh.GetWorldLocation`, `HalfSize = MakeVector(BladeRadius, BladeRadius, BladeHalfLength)`, `Orientation = HeldItemMesh.GetWorldRotation`, `ObjectTypes = [ObjectTypeQuery3]`, `bTraceComplex = false`, `ActorsToIgnore` 비었음, `bIgnoreSelf = true`, `DrawDebugType = ForDuration`, `DrawTime = 0.5`, `TraceColor` 빨강, `TraceHitColor` 초록
- `ForEachLoop(OutHits)` → 루프 원소를 `BreakHitResult.Hit`로 → `Contains(HitActorsThisSwing, HitActor)` → `NOT` → `Branch` True → `Array Add` → `PrintString("Hit: " + GetDisplayName(HitActor))` → `ApplyDamage(DamagedActor = HitActor, BaseDamage = AttackDamage 34, EventInstigator = GetController, DamageCauser = self)`
- `Completed` → `Set PrevBladeCenter ← HeldItemMesh.GetWorldLocation` (두 번째 `GetWorldLocation` 호출)

**지운 것**

- 기존 전방 구체 트레이스 여덟 노드. 판정이 액터 정면 `AttackRange 200`cm, 반경 `AttackTraceRadius 40`cm 구체였다
- `AttackRange`·`AttackTraceRadius` **변수 자체는 남겼다.** 지금 아무 노드도 참조하지 않는다

**아이템 데이터 (`DT_Items`의 `Knife`)**

- 최종값은 작업 전과 같다 — `Translation (0, 0, 25)`, `Rotation` 단위값, `Scale3D (0.04, 0.04, 0.5)`
- 중간에 두 번 바꿨다가 되돌렸다. 파일 내용이 원래대로 돌아와서 `git status`에 안 뜬다

### 기술적으로 맞게 짚은 부분

**판정 기준을 소켓이 아니라 컴포넌트 트랜스폼으로 잡은 것.**
칼은 엔진 애셋 `/Engine/BasicShapes/Cube`다. 엔진 콘텐츠에 소켓을 박지 않으려면 칼날의 시작·끝을 다른 데서 얻어야 한다. `HeldItemMesh`의 월드 위치가 곧 큐브 중심(피벗이 정중앙)이고 월드 회전이 곧 칼날 방향이므로, 이 둘만으로 칼날 전체가 표현된다. **결과적으로 `heldTransform`의 회전을 바꿔도 판정이 자동으로 따라온다** — 회전 실험을 세 번 하는 동안 판정 배선을 한 번도 안 건드렸다.

**`Play Montage`의 `OnNotifyBegin`/`OnNotifyEnd`를 쓴 것.**
`UAnimNotify_PlayMontageNotifyWindow`는 `UAnimNotifyState`이고 `BranchingPointNotifyBegin`/`End`에서 각각 `AnimInstance->OnPlayMontageNotifyBegin`/`End`를 브로드캐스트한다(`AnimNotify_PlayMontageNotify.cpp`). 그래서 **`ABP_Unarmed`를 건드리지 않고** 캐릭터 블루프린트에서 창을 여닫을 수 있다. `ABP_Unarmed`는 `BP_Enemy`와 공유하는 애셋이라 이게 실질적인 이득이다.

**닫기를 세 군데에 물린 것.**
`OnNotifyEnd`만 믿으면 몽타주가 중간에 끊겼을 때 창이 열린 채 남고, `Event Tick`이 계속 트레이스를 돈다. `OnBlendOut`·`OnInterrupted`를 같이 물려서 그 경로를 막았다. 로그에서 실제로 `WINDOW CLOSE`가 스윙마다 두 줄(노티파이 끝 + 블렌드 아웃) 났고 한 번은 세 줄 났다 — **닫기가 중복 실행돼도 무해하다.** 같은 값을 다시 쓰는 것뿐이다.

**`Event Tick`의 게이트를 불리언 하나로 둔 것.**
프로젝트 규칙이 Tick을 기본으로 꺼두는 것인데, 여기서는 프레임 간 위치 차이가 필요해서 Tick이 불가피하다. 대신 창이 닫혀 있으면 `Branch` 하나에서 끝난다. `Get All Actors Of Class`나 `Cast`가 Tick에 들어가지 않았다.

**중복 제거를 스윙 단위로 둔 것.**
`Contains` → `NOT` → `Branch` → `Add`가 `PrintString`·`ApplyDamage` 앞에 있어서, 같은 프레임에 같은 액터의 컴포넌트 두 개가 잡혀도 한 번만 들어간다. 배열은 창이 **열릴 때** 비운다 — 닫힐 때 비우면 중단 경로에서 안 비워질 수 있다.

**기존 노드를 지우지 않고 재사용한 것.**
`MakeArray`의 `ObjectTypeQuery3`(Pawn)는 열거형 배열이라 다시 만들면 값을 새로 채워야 한다. `ApplyDamage`의 입력 넷도 이미 맞게 물려 있었다. 명령 3에서 "지울 것"과 "남길 것"을 따로 나열한 덕에 재배선이 명령 4에서 연결 두 개로 끝났다.

**버그를 가설 → 반증 조건 → 관측 순서로 잡은 것.**
"드르륵 맞았다"는 보고에 바로 고치지 않고 로그를 읽었다. 첫 가설(노티파이 두 개)을 세우면서 **"뒤 스윙들에서 반복되지 않으면 틀린 것"**이라는 반증 조건을 먼저 적었고, 실제로 세 스윙이 한 번씩만 맞아서 **그 자리에서 가설을 기각했다.** 그 다음 창 열림/닫힘 로그를 임시로 심어서 열 번 중 열 번 `WINDOW OPEN`이 두 줄인 것을 확인하고서야 원인을 확정했다. 결과적으로 첫 가설은 맞았지만, **맞았다는 근거가 처음엔 없었다.**

**틀린 값을 넣어보고 축을 알아낸 것.**
소켓의 로컬 축 방향은 확인할 수단이 없었다. `pitch -90`을 넣어 칼이 캐릭터 왼쪽을 향하는 것을 보고 "로컬 +Z = 앞, 로컬 +X = 왼쪽"을 확정했고, 남은 축이 위/아래라는 결론에서 `roll 90`을 계산해 한 번에 맞혔다. **추측을 코드 블록에 넣지 않고 실험으로 좁힌 것**이 맞는 순서였다.

**되돌린 것.**
칼끝을 위로 세우니 팔뚝에 박혔다. 오프셋으로 피할 수 있는 문제가 아니라 자세의 문제다 — 팔이 내려와 있으면 칼날이 지나갈 자리에 팔이 있다. 값을 더 만지지 않고 **명령 8 이전 값으로 정확히 복귀**시켰다. 새 숫자를 만들지 않았다.

### 확인한 것 / 확인 못 한 것

**확인한 것**

- **변수 다섯 개** — CDO에서 되읽어 `{"bIsSwinging":false,"PrevBladeCenter":{"x":0,"y":0,"z":0},"HitActorsThisSwing":[],"BladeHalfLength":25,"BladeRadius":3}`
- **지운 노드 여덟 개** — 그래프 전체 검색에서 `Trace`는 상호작용용 둘만, `Attack`은 `IA_Attack`·`AttackMontage` 게터·`AttackDamage` 게터 셋만 남았다
- **남긴 노드 아홉 개** — `get_node_infos`로 하나씩 존재와 연결을 확인
- **창 여닫기 배선** — `get_connected_subgraph`로 `Play Montage`에서 뻗은 실행 흐름 전부 확인. `OnBlendOut`·`OnInterrupted`가 같은 세터에 물린 것까지
- **박스 트레이스 입력 전부** — `Start`/`End`/`HalfSize`/`Orientation`/`ObjectTypes`/`bIgnoreSelf`/`DrawDebugType`/`DrawTime` 각각 어느 노드에서 오는지 확인. `MakeVector`의 X·Y가 같은 `BladeRadius` 게터에서 오는 것도 확인
- **캡슐 노드 제거** — `Capsule` 검색 결과 0개
- **임시 로그 제거** — `Print` 검색 결과가 히트 보고용 하나뿐
- **합격 기준 1** — PIE에서 칼이 닿으면 데미지가 들어간다. 히트당 정확히 34, `EnemyHP` `100 → 66 → 32 → 0`
- **합격 기준 4** — 한 스윙에 같은 적 한 번. 스윙 3/3에서 `Hit:` 한 줄씩
- **창이 스윙당 한 번만 열린다** — 노티파이 정리 후 스윙 8/8
- **디버그 상자가 칼 막대와 겹친다** — 사용자 화면. 칼날 축 가정(컴포넌트 로컬 +Z)이 맞다는 증거다
- **칼이 오른손에서 앞으로 뻗고 팔을 관통하지 않는다** — 사용자 화면
- **건드린 파일 둘뿐** — `AM_Player_Attack.uasset`, `BP_ThirdPersonCharacter.uasset`. 다른 BP가 딸려 dirty 되지 않았다

**확인 못 한 것**

- **합격 기준 2 (3m 밖에서 안 맞음)** — 거리를 통제한 시험을 안 했다. 사용자가 "다른 건 다 잘 된다"고 말한 것과, 빗나간 스윙들에 `Hit:`이 없다는 정황뿐이다
- **합격 기준 3 (등 뒤로는 안 맞음)** — 같은 이유
- **노티파이가 정확히 `Montage Notify Window` 클래스인지** — MCP가 `Notifies`를 못 읽는다. 화면에서 구간 막대라는 것과 `Notify Name` 칸이 있다는 것, 그리고 `OnNotifyEnd`가 실제로 떴다는 동작 근거뿐이다
- **노티파이 구간의 정확한 위치** — 스크린샷 픽셀 눈대중으로 프레임 9~14. 숫자를 읽은 게 아니다
- **인스턴스 편집 플래그** — MCP가 변수의 edit 지정자를 못 읽는다. `BladeHalfLength`·`BladeRadius`가 실제로 인스턴스 편집인지 확인 못 했다
- **컴파일 경고 원문** — 사용자가 터미널 출력을 붙여넣지 않았다. 컴파일이 통과했다는 것은 PIE가 새 동작으로 돌았다는 데서 간접적으로만 안다
- **`Event Tick`이 읽는 칼 위치가 그 프레임 포즈보다 한 프레임 늦는지** — 구조상 늦을 수 있다고 사양에 적었지만 실제로 늦는지 측정 안 했다
- **`DT_Items`가 저장됐는지** — 값이 원래대로 복귀해서 `git status`에 안 뜬다. 에디터에 저장 안 된 상태와 구분이 안 된다
- **적이 두 명 이상일 때의 동작** — `MultiBoxTrace`라 여럿이 잡히도록 만들었지만 적이 하나뿐이라 시험 못 했다

### 남는 리스크

- **미사용 변수 둘.** `AttackRange`(200)와 `AttackTraceRadius`(40)를 참조하는 노드가 하나도 없다. 지우지 않기로 한 이유는 되돌리기 어렵고 적 AI에 같은 구조를 옮길 때 쓸 수도 있어서다. 나중에 읽는 사람이 "이 값이 판정에 쓰인다"고 오해할 여지가 있다
- **디버그 표시가 남아 있다.** 박스 트레이스 `DrawDebugType = ForDuration`, `DrawTime 0.5`. 그리고 `Hit:` `PrintString` 하나
- **`Event Tick`이 켜졌다.** 창이 닫혀 있으면 `Branch` 하나지만, 이 블루프린트에 Tick 경로가 생긴 것 자체가 새 사실이다. 다음 사람이 Tick에 뭘 더 붙일 유혹이 생긴다
- **한 프레임 지연.** 스켈레탈 메시의 포즈 갱신이 캐릭터 Tick보다 뒤에 돌면 트레이스가 한 프레임 밀린다. 이전→현재를 잇는 스윕이라 궤적에 구멍은 안 생기고 전체가 밀릴 뿐이다. 티가 나면 Tick 그룹을 옮기는 선택지가 있다
- **벽을 무시한다.** `ObjectTypes`가 `Pawn`뿐이라 벽 너머 적도 맞는다. 칼 길이 50cm라 실사용에서 잘 안 나겠지만 원리상 뚫린다. 심문 6번에서 사용자가 (a)로 고른 결과다
- **칼날 구간이 곧 큐브 전체다.** 지금은 손잡이와 칼날의 구분이 없다. 진짜 칼 메시가 들어오면 `BladeHalfLength`와 중심 오프셋을 손잡이 위로 옮겨야 "칼날만"이 된다
- **`MM_Attack_01`은 주먹 모션이다.** 칼을 쥐면 찌르기로 읽히지만 베기는 아니다. 사용자가 이 상태를 받아들였다
- **노티파이가 둘이었던 사고가 다시 날 수 있다.** MCP가 노티파이를 못 읽으므로 **몽타주에 뭐가 몇 개 찍혔는지는 화면으로만 안다.** 오늘 쓴 방법(창 열림 로그)이 유일한 프로그램적 관측 수단이었다
- **`heldTransform`의 회전과 오프셋은 짝이다.** 하나만 바꾸면 칼이 허공에 뜬다. `DT_Items`에는 이 관계가 안 적혀 있다

### 총평

요청은 둘이었고 둘 다 됐다. 궤적 판정은 합격 기준 넷 중 둘(1·4)을 로그로 확인했고 둘(2·3)은 통제된 시험을 못 해 정황만 있다. 칼 회전은 세 후보를 실제로 넣어보고 원래 값이 맞다는 결론에 도달했다 — **되돌린 것이 결과물이다.**

이 작업의 실질적 난이도는 두 군데였다.

첫째는 **내 사양이 틀렸던 것**이다. "캡슐의 축이 곧 칼날"이라고 적었는데 `CapsuleTraceMultiForObjects`에는 회전 인자가 아예 없다. 사양 단계에서 엔진 소스를 확인했으면 안 났을 일이고, 확인 안 하고 "그럴 것"으로 적은 대가를 명령 하나로 치렀다. **다행히 검증에서 잡혔다** — 배선 확인 때 `Orientation` 핀이 목록에 없는 것이 바로 보였다. MCP 응답을 성공 근거로 안 삼는 습관이 여기서 값을 했다.

둘째는 **간헐적 버그의 원인 규명**이다. 한 번 관측된 이중 타격을 두고 세 스윙이 정상으로 나왔을 때, 그 자리에서 "이제 괜찮다"고 넘어갈 수 있었다. 실제로는 노티파이가 두 개였고 **적이 두 번째 창 순간에도 칼 범위에 있어야만** 증상이 나타나는 조건부 버그였다. 임시 로그 두 줄을 심어서 열 번 중 열 번 재현되는 구조적 사실로 바꾼 것이 이 세션에서 가장 값이 컸다.

부수적으로 **로그 프레임 번호가 1000에서 되감긴다**는 것을 알았다. 처음에 `661 → 412`를 "PIE 재시작"으로 읽고 세션 경계를 잘못 그었다가, HP가 100에서 시작하지 않는 모순 때문에 되짚어 잡았다. 이걸 안 잡았으면 "적 HP가 세션 간에 유지된다"는 존재하지 않는 버그를 쫓을 뻔했다.

## AI의 제안

> `CapsuleTraceMultiForObjects(... Start, End, float Radius, float HalfHeight, ObjectTypes, ...)` — **회전 인자가 없다** (`KismetSystemLibrary.h:1512`). 캡슐은 항상 월드 Z축으로 선다 / `BoxTraceMultiForObjects(... Start, End, FVector HalfSize, FRotator Orientation, ObjectTypes, ...)` — **`Orientation`이 있다** (`KismetSystemLibrary.h:1478`)

얻는 것 — 칼날이 실제 방향으로 서고, 큐브 칼이라 상자 모양이 실물과 정확히 일치한다. 잃는 것 — `MakeVector` 노드 하나가 는다.

> **`WINDOW OPEN`이 두 줄이면 A, 한 줄이면 B다.** 증거 없이 고치면 뭘 고쳤는지 모른다.

얻는 것 — 간헐적 증상을 열 번 중 열 번 재현되는 구조적 사실로 바꿔서, 고친 뒤 "정말 고쳐졌는지"를 같은 잣대로 확인할 수 있다. 잃는 것 — 임시 노드 두 개를 넣었다 빼는 왕복 두 번.

> **절충안이 하나 있다** — 앞으로 뻗되 45도 위로 든 모양. `rotation roll 45` · `location (0, -17.68, 17.68)`

얻는 것 — 팔에서 벗어나면서 칼끝이 서 있어 베기 동작과 덜 어긋난다. 잃는 것 — 45도면 팔뚝과 거의 나란해져 여전히 겹칠 수 있고, 확인 안 한 값이다.

> **`MM_Attack_01` 그대로 간다.** 오른손 스트레이트에 칼을 쥐면 "찌르기"로 읽힌다. Mixamo는 판정이 다 되고 나서 별도로 잡는다

얻는 것 — 애니메이션을 갈아도 판정 배선은 그대로라 검증이 재사용된다. 비용 0. 잃는 것 — 베기 모션이 아니어서 "검격 궤적"이라는 원래 그림과는 거리가 있다.

> **`AttackRange`·`AttackTraceRadius`는 변수만 남기고 쓰는 노드만 없앤다.** 지우면 되돌리기 어렵다. 적 AI에 같은 구조를 옮길 때 다시 쓸 수도 있다

얻는 것 — 참조가 조용히 끊길 위험이 없다. 잃는 것 — 아무도 안 쓰는 변수 둘이 남아 오해를 부른다.

## 다음으로 넘김

**바로 이어서 할 것**

- **`DT_Items` 저장 확인.** 값이 원래대로 복귀해 `git status`에 안 뜬다. 에디터에 저장 안 된 상태와 구분이 안 된다

**결정 필요**

- **적 공격에 같은 궤적 판정 붙이기.** 사용자가 "플레이어 쪽이 완벽해지면 적 AI에도 적용"으로 정한 다음 사양이다. 지금 적은 `PlayAnimMontage → ApplyDamage → Delay`로 무조건 맞힌다. 필요한 것 — (1) `PlayAnimMontage`를 `Play Montage`로 교체, (2) `AM_Enemy_Attack`에 `Montage Notify Window` 찍기(수작업), (3) 적에게도 `bIsSwinging`·`PrevBladeCenter`·`HitActorsThisSwing` 계열 변수와 Tick 스윕. **다만 적은 맨손이라 "칼날"에 해당하는 컴포넌트가 없다** — 손 소켓 기준으로 잡을지 먼저 정해야 한다
- **플레이어 `CurrentHP`의 기본값 75를 100으로 고칠 것인가.** PIE 시작 체력이 75다. 배치된 인스턴스가 없으므로 인스턴스 함정은 안 걸린다
- **디버그 표시 제거 시점.** 오늘 기준 실제 개수는 `BP_Enemy`의 `PrintString` 10개 + `ToString(Float)` 4개, `BP_ThirdPersonCharacter`의 `PrintString` 1개(`Hit:`) + `MultiBoxTraceForObjects`의 `DrawDebugType ForDuration` 하나. **`ShowHUDMessage` 안의 `PrintString`은 기능이므로 지우면 안 된다**
- **`K2Node_Self_1`(`BP_Enemy`)을 `ApplyDamage` 근처로 옮길 것인가.** 남은 장거리 선 하나가 사라진다
- **미사용 변수 `AttackRange`·`AttackTraceRadius`를 지울 것인가.** 오늘은 남겼다
- **칼 회전 45도 절충안을 볼 것인가.** 값은 계산해뒀다 — `roll 45` / `location (0, -17.68, 17.68)`

**확인 필요**

- **합격 기준 2·3의 통제된 시험.** 거리 3m, 등 뒤 각도를 정해놓고 스윙해서 `Hit:`이 안 나는 것을 로그로 확인
- **`Event Tick`의 한 프레임 지연이 실제로 있는지.** 있으면 Tick 그룹 이동을 검토
- **적이 둘 이상일 때 한 스윙으로 둘 다 맞는지.** `MultiBoxTrace`로 만들었지만 시험 못 했다
- **MCP가 못 읽는 프로퍼티 목록에 여섯이 추가됐다** — `Notifies`, `AnimNotifyTracks`, `BranchingPointMarkers`, `BranchingPointStateNotifyIndices`, `ActiveStateBranchingPoints`, `CompositeSections`. 기존 목록(`AttachSocketName`, `attachParent`, `CollisionEnabled`, `NewVariables`, `ActorLabel` 등)과 같은 부류로 보인다
- **MCP가 블루프린트 애셋 경로를 거부하는 새 형태.** `/Game/ThirdPerson/Blueprints/BP_Enemy.BP_Enemy`를 `ObjectTools.get_properties`와 `BlueprintTools.get_default_object` 양쪽에 줬더니 `is not valid Object for property 'instance'` / `is not valid Blueprint for property 'blueprint'`로 거부됐다. **레벨 액터 경로로는 읽혔다**
- **`_C_0`이 아닌 플레이어 인스턴스.** 예전 로그에 `BP_ThirdPersonCharacter_C_7`이 있었다. 오늘 로그에는 `_C_0`만 찍혔다
- **`2026-09-01-enemy-hp-death.md`의 `확인 필요` 목록은 이 기록으로 옮기지 않았다.** 오늘 건드리지 않은 항목이 대부분이라 그 파일에 그대로 있다. `arrange_nodes`, `read_graph_dsl` 절단, `EditorPerProjectUserSettings.ini` 저장 실패, `CaptureViewport`가 에디터 월드를 그리는 것 등이 거기 있다

**접어둔 것**

- **Mixamo 등 외부 베기 애니메이션.** 프로젝트에 IK Rig도 IK Retargeter도 없고(`Content` 전체에서 `IK_*`/`RTG_*`/`*Retarget*` 0개) MCP 툴셋에도 리타깃 도구가 없다. 본 이름 체계가 달라 IK Rig 둘 + Retargeter 하나를 손으로 만들어야 한다 — **한 세션짜리 일이고 전부 수작업이다**
- **`MM_Attack_02` / `MM_Attack_03` / `MM_ChargedAttack`.** 사용자가 열어보고 "셋 다 칼이랑 관련없음"으로 확인했다. 이제 이 셋이 어떤 동작인지는 확인 대상이 아니다 — **칼에 쓸 수 없다는 것만 안다**
- **진짜 칼 메시 구하기.** 구하면 `BladeHalfLength`와 중심 오프셋을 손잡이 위로 옮겨 "칼날만" 판정이 된다
- **여러 적을 한 번에 때리기.** 오늘 `MultiBoxTraceForObjects`로 이미 만들었다. 시험만 남았다
- **`Knife`와 `Key_Stage1`이 같은 `Cube` 메시라 색이 같은 것.** 머티리얼로 가를 수 있다
- **`heldTransform`의 회전·오프셋이 짝이라는 사실을 `DT_Items` 어디에도 안 적어뒀다.** 주석 칸이 없다
