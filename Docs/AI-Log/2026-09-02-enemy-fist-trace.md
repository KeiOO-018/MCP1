# 2026-09-02

## 작업물

적의 주먹이 지나간 궤적으로 타격을 판정하는 것 — 플레이어의 칼 판정을 적에게 옮겼다. 그리고 플레이어 시작 체력 100, 미사용 변수 둘 삭제, 디버그 표시 전면 제거.

**소요 시간**: 증거가 남은 범위로 `AM_Enemy_Attack.uasset` 저장(로컬 `13:14:10`)부터 마지막 PIE 종료(UE 로그 `05:15:13` UTC = 로컬 `14:15`)까지 약 **1시간 1분**. 그 앞의 조사·심문·사양 구간은 파일도 로그도 안 남겨서 **실제 벽시계 시간은 이보다 길다.** 세션 시작 시각을 기록하지 않아 정확한 값을 모른다. UE 로그 타임스탬프가 UTC이고 파일 mtime이 로컬(KST)이라 둘을 섞어 읽을 때 9시간 차이를 보정해야 했다.

## 명령

### 한글

```
작업준비
```
```
적 공격에 같은 궤적 판정 붙이기 
플레이어 CurrentHP 기본값100으로 
디버그 표시 제거 
K2Node_Self_1(BP_Enemy)을 ApplyDamage 근처로 옮길 것인가 이거는 정리개념인가?
미사용 변수 AttackRange·AttackTraceRadius를 지울 것인가 안쓰는건 지워
칼 회전 45도 절충안을 볼 것인가 — 이대로하자
```
```
1. a
2. a
3. a
4. 이미지 첨부 이름은 EnemyAttackHit 로 
5. b
6. a
```
```
결과 확인
```
```
결과확인
```
```
했어
```
```
아화면잠시만
```
```
이거바바
```
```
결과 확인
```
```
결과 확인
```
```
결과 확인해봐
```
```
터미널 로그
```
```
a 로하자
```
```
저장은 다됬는데 all saved 떠있어
```
```
결과 확인
```
```
확인
```
```
결과 확인
```
```
결과확인
```
```
PIE 결과 이상없음
```
```
기록하고 정리하자 다음작업을 위한 준비도 하고
```

### English — MCP에 실제로 보낸 명령

**이 세션에서도 영어 명령은 내가 MCP로 보낸 것이 아니다.** 전부 **사용자가 UE Terminal에 붙여넣도록 만들어 건넨 원문**이다. 내가 직접 부른 MCP는 전부 읽기 호출이었다 — `list_toolsets`, `describe_toolset`, `list_graphs`, `read_graph_dsl`, `find_nodes`, `get_node_infos`, `get_connected_subgraph`, `list_variables`, `get_variable_category`, `get_variable_replication`, `get_default_object`, `get_properties`, `get_rows`, `get_socket_names`, `get_pin_value`, `find_actors`, `GetLogEntries`. 아래는 Terminal에 건넨 영어 원문 그대로다.

명령 3은 영어 명령이 없다. MCP가 몽타주 노티파이를 읽지도 쓰지도 못해서 몽타주 에디터 수작업이었다.

**명령 1 — `BP_Enemy` 변수 넷**

```
In the Blueprint /Game/Enemy/BP_Enemy, add four new variables:

1. Name "bIsSwinging", type Boolean, default value false, NOT instance editable.
2. Name "PrevFistCenter", type Vector, default value (0, 0, 0), NOT instance editable.
3. Name "HitActorsThisSwing", type Actor object reference, as an ARRAY, NOT instance editable.
4. Name "FistRadius", type Float, default value 15.0, instance editable.

Put all four in the "Default" category, the same category the existing AttackRange
variable uses. Leave all four Not Replicated.

Do not touch any existing variable. In particular do not touch AttackRange,
AttackDamage, AttackCooldown or ThinkInterval. Do not change any existing node.

Then compile the Blueprint, list all variables on it, and report each of the four new
variables with its type, whether it is an array, its default value, and whether it is
instance editable.
```

**명령 2 — 배치 인스턴스의 `FistRadius` 고치기**

```
In the currently loaded level, there is one placed BP_Enemy actor at this path:
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879

That actor instance has FistRadius overridden to 0, while the class default is 15.
Set FistRadius to 15.0 on that actor instance, then save the actor.

Do not change any other property on that actor. Do not change the class defaults.

Then read FistRadius back from that actor instance and report its value.
```

**명령 4 — `Think` 재배선 + 타격 창 여닫기**

```
Work in the EventGraph of /Game/Enemy/BP_Enemy.

PART A - remove the old always-hit path.

1. Delete exactly one node: the PlayAnimMontage node (K2Node_CallFunction_47).

2. Do NOT delete the ApplyDamage node (K2Node_CallFunction_49). Instead disconnect it
   from the Think chain, leaving it in place unconnected - it gets reused later:
     - break its exec output "then" -> the Delay node (K2Node_CallFunction_50)
     - break its "DamagedActor" input <- the PlayerRef getter (K2Node_VariableGet_30)
   Leave its BaseDamage, EventInstigator and DamageCauser inputs connected exactly as
   they are.

3. Do NOT delete the PlayerRef getter (K2Node_VariableGet_30). Five other nodes still
   read from it.

4. Do NOT delete or change: the "ATTACK" PrintString (K2Node_CallFunction_44), the
   StopMovement node (K2Node_CallFunction_46), the AttackMontage getter
   (K2Node_VariableGet_37), the Delay node (K2Node_CallFunction_50), the AttackCooldown
   getter (K2Node_VariableGet_39), or the Think call (K2Node_CallFunction_51).

PART B - restore the loop with a Sequence, so the attack cadence stays exactly as it is
now (AttackCooldown measured from when the montage starts).

5. Create a Sequence node with two output pins.
     exec in = the "then" output of StopMovement (K2Node_CallFunction_46)

6. Create a "Play Montage" node (the async one with OnCompleted / OnBlendOut /
   OnInterrupted / OnNotifyBegin / OnNotifyEnd output pins - NOT PlayAnimMontage).
   Wire it:
     exec in                    = the Sequence's "Then 0" pin
     In Skeletal Mesh Component = the Mesh component of this Character
     Montage to Play            = the EXISTING AttackMontage getter (K2Node_VariableGet_37)
     Play Rate                  = 1.0
     Starting Position          = 0.0
     Starting Section           = None

7. Connect the Sequence's "Then 1" pin to the exec input of the EXISTING Delay node
   (K2Node_CallFunction_50). Its Duration is already wired to the AttackCooldown getter
   and its "then" already runs into the Think call - leave both alone.

PART C - open the hit window. From Play Montage's OnNotifyBegin pin, run this chain:
  1. A new Name Equal node comparing OnNotifyBegin's NotifyName output to the literal
     Name "EnemyAttackHit"
  2. That into a new Branch's condition
  3. Branch True -> Set bIsSwinging = true
  4. -> an array Clear node on HitActorsThisSwing
  5. -> Set PrevFistCenter to the result of a GetSocketLocation call on the Mesh
     component with In Socket Name = "HandGrip_R"

PART D - close the hit window. Add ONE Set bIsSwinging = false node and drive it from
three places:
  1. Play Montage's OnNotifyEnd -> a new Name Equal node comparing that pin's NotifyName
     output to the literal Name "EnemyAttackHit" -> a new Branch -> True pin
     -> the Set bIsSwinging = false node
  2. Play Montage's OnBlendOut    -> the same Set bIsSwinging = false node
  3. Play Montage's OnInterrupted -> the same Set bIsSwinging = false node

Do not touch the CHASE, RETURN, IDLE_HOME, IDLE_WAIT or NO_PLAYER branches. Do not touch
Event BeginPlay or Event AnyDamage. Do not change any variable's default value.

Then compile the Blueprint and report: any compile errors or warnings, the full exec
chain from the Branch K2Node_IfThenElse_1 True pin onward, and every node connected to
the new Play Montage node.
```

**명령 5 — `Event Tick` 궤적 스윕**

```
Work in the EventGraph of /Game/Enemy/BP_Enemy.
Add a new Event Tick node and build this chain. Reuse the existing nodes named below
instead of creating new ones.

1. Event Tick -> a new Branch, condition = a bIsSwinging variable getter.

2. From that Branch's True pin, call MultiSphereTraceForObjects
   (the MULTI version, for objects - not the single version, not the channel version,
    and not the box or capsule version). Wire its inputs:
     Start          = a PrevFistCenter variable getter
     End            = a GetSocketLocation call on the Mesh component
                      with In Socket Name = "HandGrip_R"
     Radius         = a FistRadius variable getter
     Object Types   = a new Make Array node holding one element, ObjectTypeQuery3
     Trace Complex  = false
     Actors to Ignore = leave empty
     Ignore Self    = true
     Draw Debug Type = ForDuration
     Draw Time      = 0.5

3. From MultiSphereTraceForObjects' exec output, run a ForEachLoop over its
   Out Hits array output.

4. Inside the loop body:
   a. Feed the loop's Array Element (a Hit Result) into the Hit input of a new
      BreakHitResult node.
   b. Add an "Array Contains Item" node: array = a HitActorsThisSwing getter,
      item = that BreakHitResult's Hit Actor output.
   c. Feed Contains into a NOT Boolean node, and that into a new Branch's condition.
   d. Loop body exec -> that new Branch.
   e. Branch True -> an "Array Add" node (array = HitActorsThisSwing, item = the same
      Hit Actor output)
      -> a new PrintString node whose InString comes from a new Append node built as
         "EnemyHit: " + GetDisplayName(that same Hit Actor). Leave PrintToScreen and
         PrintToLog at their defaults and leave Duration at its default.
      -> then into the exec input of the EXISTING ApplyDamage node
         (K2Node_CallFunction_49), which is currently sitting disconnected.
   f. Connect that same Hit Actor output to the ApplyDamage node's DamagedActor input.
      Do NOT touch its BaseDamage, EventInstigator or DamageCauser inputs - they are
      already connected correctly.

5. From the ForEachLoop's Completed pin, Set PrevFistCenter to a GetSocketLocation call
   on the Mesh component with In Socket Name = "HandGrip_R" (a second GetSocketLocation
   call is fine).

Do not touch the Think event, Event BeginPlay or Event AnyDamage. Do not change any
variable's default value.

Then compile the Blueprint and report: any compile errors or warnings, the full node
list connected to the new Event Tick node, and whether the Blueprint's class defaults
have Actor Tick "Start with Tick Enabled" checked.
```

**명령 6 — 플레이어 시작 체력 100 + 임시 HP 로그**

```
Work in the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.

PART A - change one default value.

1. Set the default value of the variable "CurrentHP" to 100.0 on the class defaults.
   It is currently 75. Do not change MaxHP, AttackDamage, RespawnDelay, or any other
   variable's default.

PART B - add one TEMPORARY debug PrintString inside Event AnyDamage.

2. There are two "Set CurrentHP" nodes in the EventGraph. Work ONLY on
   K2Node_VariableSet_0, the one at position (1200, 4700) whose exec input comes from
   the Branch K2Node_IfThenElse_2 and whose "then" runs into the Branch
   K2Node_IfThenElse_8. That is the one inside Event AnyDamage.
   Do NOT touch K2Node_VariableSet_2 at (200, 2200) - that is the healing path.

3. Insert a new PrintString between K2Node_VariableSet_0 and K2Node_IfThenElse_8, so
   the exec order becomes:
     Set CurrentHP (K2Node_VariableSet_0) -> new PrintString -> Branch (K2Node_IfThenElse_8)

4. Wire that PrintString's InString from a new Append node built as
   "PlayerHP: " + ToString(Float) of the Output_Get pin on K2Node_VariableSet_0
   (that is the Set node's own value output pin, which is currently unconnected).
   Leave PrintToScreen and PrintToLog at their defaults and leave Duration at its
   default.

Do not change anything else in the graph. Do not touch Event Tick, the
MultiBoxTraceForObjects node, or the Play Montage chain.

Then compile the Blueprint and report: any compile errors or warnings, the current
default value of CurrentHP on the class defaults, and the full exec chain of
Event AnyDamage from the event node onward.
```

**명령 7 — 플레이어 미사용 변수 둘 삭제**

```
In the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, delete two
variables that no node reads any more:

1. "AttackRange"        (Float, currently 200)
2. "AttackTraceRadius"  (Float, currently 40)

Delete ONLY those two. Do NOT touch AttackDamage, AttackMontage, BladeHalfLength,
BladeRadius, CurrentHP, MaxHP or any other variable.

Note that a DIFFERENT Blueprint, /Game/Enemy/BP_Enemy, also has a variable named
AttackRange and that one IS still in use - do not open or modify that Blueprint.

Then compile the Blueprint and report: any compile errors or warnings, and the full
list of variables remaining on BP_ThirdPersonCharacter.
```

**명령 8 — 디버그 표시 제거**

```
PART 1 - work in the EventGraph of /Game/Enemy/BP_Enemy.

Delete these ten PrintString nodes and reconnect the exec chains around them:

  K2Node_CallFunction_41   key "2_dist"     - then reconnect MacroInstance_27 pin 0
                                              ("Is Valid") straight to K2Node_CallFunction_176
  K2Node_CallFunction_43   key "3_home"     - part of the same chain
  K2Node_CallFunction_176  key "4_angle"    - after all three above are gone, connect
                                              MacroInstance_27 pin 0 -> K2Node_IfThenElse_0
  K2Node_CallFunction_44   "ATTACK"         - reconnect K2Node_IfThenElse_1 True pin
                                              -> K2Node_CallFunction_46 (StopMovement)
  K2Node_CallFunction_52   "CHASE"          - reconnect K2Node_IfThenElse_1 False pin
                                              -> K2Node_CallFunction_54
  K2Node_CallFunction_57   "RETURN"         - reconnect K2Node_IfThenElse_2 True pin
                                              -> K2Node_CallFunction_20
  K2Node_CallFunction_63   "IDLE_HOME"      - reconnect K2Node_IfThenElse_3 True pin
                                              -> K2Node_CallFunction_65
  K2Node_CallFunction_69   "IDLE_WAIT"      - reconnect K2Node_IfThenElse_3 False pin
                                              -> K2Node_CallFunction_71
  K2Node_CallFunction_74   "NO_PLAYER"      - reconnect MacroInstance_27 pin 1
                                              ("Is Not Valid") -> K2Node_VariableSet_9
  K2Node_CallFunction_98   "EnemyHit: "     - reconnect K2Node_CallArrayFunction_3
                                              (the Array Add) -> K2Node_CallFunction_49
                                              (ApplyDamage)

Also delete the pure nodes that only fed those, and nothing else:
  K2Node_CallFunction_40, K2Node_CallFunction_42, K2Node_CallFunction_175
      (the three ToString(Float) nodes feeding 2_dist / 3_home / 4_angle)
  K2Node_CommutativeAssociativeBinaryOperator_4
      (the Append feeding "EnemyHit: ") and the GetDisplayName node feeding it

DO NOT DELETE K2Node_CallFunction_2 - that is the "EnemyHP: " PrintString and it stays,
along with its Append node K2Node_CommutativeAssociativeBinaryOperator_0 and the
ToString(Float) feeding that. Leave Event AnyDamage untouched.

Then set the DrawDebugType input on K2Node_CallFunction_94
(MultiSphereTraceForObjects, in Event Tick) from ForDuration to None.

PART 2 - work in the EventGraph of /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.

Delete these two PrintString nodes and reconnect around them:

  K2Node_CallFunction_86   "Hit: "       - reconnect K2Node_CallArrayFunction_7
                                           (the Array Add) -> K2Node_CallFunction_61
                                           (ApplyDamage)
  K2Node_CallFunction_87   "PlayerHP: "  - reconnect K2Node_VariableSet_0
                                           (Set CurrentHP) -> K2Node_IfThenElse_8

Also delete the pure nodes that only fed those:
  K2Node_CommutativeAssociativeBinaryOperator_3 (the Append feeding "Hit: ")
      and the GetDisplayName node feeding it
  K2Node_CommutativeAssociativeBinaryOperator_5 (the Append feeding "PlayerHP: ")
      and K2Node_CallFunction_88 (the ToString(Float) feeding that)

Then set the DrawDebugType input on K2Node_CallFunction_31
(MultiBoxTraceForObjects, in Event Tick) from ForDuration to None.

Do NOT touch the ShowHUDMessage function graph - the PrintString in there is a feature,
not debug output. Do not change any variable default. Do not touch the Play Montage
chains in either Blueprint.

Then compile BOTH Blueprints and report: any compile errors or warnings, the full list
of PrintString nodes remaining in each EventGraph, and the DrawDebugType value on both
trace nodes.
```

**옮기며 넣은 해석**

- 한글의 **"적 공격에 같은 궤적 판정 붙이기"**를 나는 **"플레이어의 칼 판정 구조를 그대로 적의 주먹에 옮긴다"**로 읽었다. 심문에서 판정 모양(구체 vs 상자), 기준점(소켓 vs 본), 루프 재개 방식 세 가지를 갈라 물어서 확정했다.
- 한글의 **"칼 회전 45도 절충안을 볼 것인가 — 이대로하자"**를 나는 **"지금 값을 유지한다"**로 읽었다. "이대로 하자"가 "45도로 하자"일 수도 있어서 명시적으로 해석을 밝히고 진행했고, 반대 지적이 없었다.
- **`FistRadius 15.0`** — 한글 지시에 없는 숫자다. 주먹+손목 굵기를 반지름 15cm로 잡았고 **근거는 감이다.** 인스턴스 편집으로 열어뒀다.
- **노티파이 구간을 프레임 9~16으로 잡은 것** — 내가 정했다. 플레이어는 9~14인데, 사용자가 첨부한 몽타주 화면의 프레임 16(0.56초)에서 팔이 아직 뻗어 있어서 뒤쪽을 넓혔다. 근거는 그 화면 한 장뿐이다.
- **`Sequence`로 `Think` 루프를 가른 것** — 사용자가 말한 적 없다. `Play Montage`에 즉시 실행 핀이 없다고 내가 (틀리게) 판단해서 넣은 구조다. 결과적으로 공격 주기는 보존됐다.
- **`"EnemyHit: "` / `"PlayerHP: "` `PrintString`** — 사용자가 말한 적 없다. 합격 기준을 로그로 확인할 수단이 없어서 임시 검증용으로 내가 넣었고, 명령 8에서 뺐다.
- **`DrawDebugType`을 지우지 않고 `None`으로 바꾼 것** — 사용자는 "디버그 표시 제거"만 말했다. 노드를 지우면 판정 자체가 사라지므로 값만 바꾼 것은 내 판단이다.
- **`ObjectTypes`를 `Pawn` 하나로 둔 것** — 심문 6번에서 사용자가 (a)로 골랐다. 적이 다른 적을 때릴 수 있는 상태를 받아들인 것이다.

## Terminal 결과

### 원문 — English

**UE Terminal 자체의 출력은 이 세션에서 딱 한 번 들어왔다.** 명령 5 실행 로그다. 나머지는 사용자가 붙여넣지 않았고, 나는 매번 MCP 읽기 호출과 UE 출력 로그로 실제 상태를 다시 확인했다.

**UE Terminal 출력 — 명령 5 실행분. 사용자가 붙여넣은 전문**

```
Called unreal-mcp 3 times

Creating the nodes.

  Called unreal-mcp 5 times

Correct node — has OutHits array and ObjectTypes. Creating the rest.

  Called unreal-mcp 16 times

Now the Completed-branch nodes for step 5.

  Called unreal-mcp 4 times
```

**MCP 실패 응답 — 전문**

```
Parameter error: /Game/ThirdPerson/Blueprints/BP_Enemy.BP_Enemy is not valid Blueprint for property 'blueprint'.
```

```
GetObjectProperties on '/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Enemy_Attack.AM_Enemy_Attack' (AnimMontage): the following properties could not be read: Notifies, AnimNotifyTracks
```

```
Function "get_properties", input param "properties" is required by the function input schema Json, but is missing from the incoming function input params Json.
Function schema Json -
{"type":"object","properties":{"instance":{"type":"object","title":"/Script/CoreUObject.Object","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]},"properties":{"type":"array","items":{"type":"string"}}},"required":["instance","properties"]}
Function input params Json -
{"instance":{"refPath":"/Game/Enemy/BP_Enemy.Default__BP_Enemy_C"},"property_names":["SightRange","AttackRange","AttackDamage","AttackCooldown","ThinkInterval","AttackMontage","SightHalfAngle","MaxHP","CurrentHP","ReturnDelay","ReturnSightRange","HomeArriveRadius"]}
```

```
Function "get_socket_names", input param "mesh" is required by the function input schema Json, but is missing from the incoming function input params Json.
Function schema Json -
{"type":"object","properties":{"mesh":{"type":"object","title":"/Script/Engine.SkeletalMesh","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]}},"required":["mesh"]}
Function input params Json -
{"skeletal_mesh":{"refPath":"/Game/Characters/Mannequins/Meshes/SKM_Manny_Simple.SKM_Manny_Simple"}}
```

```
Function "get_pin_value", input param "pin" is required by the function input schema Json, but is missing from the incoming function input params Json.
Function schema Json -
{"type":"object","properties":{"pin":{"title":"PinID","type":"object","properties":{"direction":{"type":"string","title":"EEdGraphPinDirection","enum":["EGPD_Input","EGPD_Output"]},"index_id":{"type":"integer"},"node":{"type":"object","title":"/Script/Engine.EdGraphNode","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]}},"required":["direction","index_id","node"]}},"required":["pin"]}
Function input params Json -
{"node":{"refPath":"/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_CallFunction_31"},"pin_name":"DrawDebugType"}
```

```
Error: result (111,791 characters across 1 line) exceeds maximum allowed tokens.
```

```
Error: Unknown tool run_script
```

**인스턴스 함정을 잡은 MCP 응답 두 개 — 같은 프로퍼티를 CDO와 배치 인스턴스에서 각각 읽은 것**

```
{"bIsSwinging":false,"PrevFistCenter":{"x":0,"y":0,"z":0},"HitActorsThisSwing":[],"FistRadius":15,"AttackRange":150,"AttackDamage":10,"AttackCooldown":1.5,"ThinkInterval":0.29999999999999999}
```

```
{"bIsSwinging":false,"PrevFistCenter":{"x":0,"y":0,"z":0},"HitActorsThisSwing":[],"FistRadius":0,"AttackRange":150,"AttackDamage":10,"AttackCooldown":1.5}
```

**UE 출력 로그 — 첫 궤적 판정 PIE. 여덟 번의 공격 전부**

```
[2026.09.02-04.40.51:920][486]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.40.53:426][592]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.09.02-04.40.53:733][614]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.40.54:055][637]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHit: BP_ThirdPersonCharacter0
[2026.09.02-04.40.55:244][720]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_WAIT
[2026.09.02-04.40.56:780][830]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.09.02-04.40.57:089][852]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.40.57:494][881]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHit: BP_ThirdPersonCharacter0
[2026.09.02-04.40.58:605][959]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.09.02-04.40.59:839][ 47]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.41.01:342][153]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_WAIT
[2026.09.02-04.41.01:958][197]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.09.02-04.41.02:266][219]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.41.02:701][250]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHit: BP_ThirdPersonCharacter0
[2026.09.02-04.41.03:774][324]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.09.02-04.41.07:754][607]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.41.09:263][713]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_WAIT
[2026.09.02-04.41.09:569][735]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.09.02-04.41.09:878][757]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 66.0
[2026.09.02-04.41.09:878][757]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.41.10:294][790]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHit: BP_ThirdPersonCharacter0
[2026.09.02-04.41.11:383][869]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_WAIT
[2026.09.02-04.41.13:856][ 45]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.09.02-04.41.14:165][ 67]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.41.14:308][ 77]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 32.0
[2026.09.02-04.41.14:598][ 97]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHit: BP_ThirdPersonCharacter0
[2026.09.02-04.41.15:667][172]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_WAIT
```

**UE 출력 로그 — 합격 기준 1을 확정한 PIE. 다섯 번의 공격 전부**

```
[2026.09.02-04.52.07:925][716]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.52.08:361][746]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHit: BP_ThirdPersonCharacter0
[2026.09.02-04.52.08:361][746]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 90.0
[2026.09.02-04.52.09:431][819]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.52.11:249][944]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.52.11:679][974]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHit: BP_ThirdPersonCharacter0
[2026.09.02-04.52.11:680][974]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 80.0
[2026.09.02-04.52.13:698][114]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.52.14:099][142]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHit: BP_ThirdPersonCharacter0
[2026.09.02-04.52.14:099][142]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 70.0
[2026.09.02-04.52.15:815][260]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.09.02-04.52.16:211][288]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHit: BP_ThirdPersonCharacter0
[2026.09.02-04.52.16:212][288]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 60.0
```

**UE 출력 로그 — 디버그 제거 후 PIE 두 번. `LogBlueprintUserMessages`에 남은 전부**

```
[2026.09.02-05.14.03:111][958]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 66.0
[2026.09.02-05.14.05:189][136]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 32.0
[2026.09.02-05.14.08:155][390]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 0.0
[2026.09.02-05.15.04:973][504]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 66.0
[2026.09.02-05.15.11:021][988]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 32.0
[2026.09.02-05.15.13:300][176]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 0.0
```

### 요약 — 한글

**애셋 단위로 바뀐 것 넷**

- `Content/Enemy/BP_Enemy.uasset` — 변수 넷 추가, `Think`의 `ATTACK` 갈래 재배선, `Event Tick` 신설, `PrintString` 열 개 삭제
- `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset` — `CurrentHP` 기본값 `75 → 100`, 변수 둘 삭제, `PrintString` 둘 삭제, `DrawDebugType` `ForDuration → None`
- `Content/Characters/Mannequins/Anims/Unarmed/Attack/AM_Enemy_Attack.uasset` — `Montage Notify Window` `EnemyAttackHit` 하나 추가 (프레임 9~16)
- `Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/0/KM/MV2KKKYMIZ9A43Y7GVWSU9.uasset` — 배치된 `BP_Enemy` 인스턴스의 `FistRadius` `0 → 15`

**변수 단위**

- `BP_Enemy`에 추가 — `bIsSwinging`(Boolean, `false`), `PrevFistCenter`(Vector, `(0,0,0)`), `HitActorsThisSwing`(Actor 배열, 빈 배열), `FistRadius`(Float, `15`, 인스턴스 편집). 전부 `Default` 카테고리, `Not Replicated`
- `BP_ThirdPersonCharacter`에서 삭제 — `AttackRange`(`200`), `AttackTraceRadius`(`40`)
- `BP_ThirdPersonCharacter`에서 값 변경 — `CurrentHP` `75 → 100`
- 안 건드린 튜닝 값 — `BP_Enemy`의 `AttackRange 150`, `AttackDamage 10`, `AttackCooldown 1.5`, `ThinkInterval 0.3`, `SightRange 1200`, `SightHalfAngle 60`, `MaxHP 100` / `BP_ThirdPersonCharacter`의 `AttackDamage 34`, `MaxHP 100`, `RespawnDelay 2`, `BladeHalfLength 25`, `BladeRadius 3` / `DT_Items`의 `Knife` 행 전체

**노드 단위 — `BP_Enemy`에서 지운 것**

`K2Node_CallFunction_47`(`PlayAnimMontage`), `K2Node_CallFunction_41`(`2_dist`), `K2Node_CallFunction_43`(`3_home`), `K2Node_CallFunction_176`(`4_angle`), `K2Node_CallFunction_44`(`ATTACK`), `K2Node_CallFunction_52`(`CHASE`), `K2Node_CallFunction_57`(`RETURN`), `K2Node_CallFunction_63`(`IDLE_HOME`), `K2Node_CallFunction_69`(`IDLE_WAIT`), `K2Node_CallFunction_74`(`NO_PLAYER`), `K2Node_CallFunction_98`(`EnemyHit:`), `ToString(Float)` 셋(`40`·`42`·`175`), `Append` 하나(`CommutativeAssociativeBinaryOperator_4`)와 그 `GetDisplayName`

**노드 단위 — `BP_Enemy`에서 만든 것**

`K2Node_PlayMontage_0`, `K2Node_ExecutionSequence_0`, `K2Node_CallFunction_94`(`MultiSphereTraceForObjects`), `K2Node_MakeArray_0`, `K2Node_PromotableOperator_11`·`12`(`Name Equal`), `K2Node_IfThenElse_5`·`6`·`7`, `K2Node_VariableSet_15`(`Set bIsSwinging false`), `K2Node_CallArrayFunction_3`(`Array Add`), `K2Node_MacroInstance_2`(`ForEachLoop`), `K2Node_CallFunction_96`(`BreakHitResult`), `GetSocketLocation` 셋, `Event Tick`

**노드 단위 — 지우지 않고 재사용한 것**

`K2Node_CallFunction_49`(`ApplyDamage`) — `DamagedActor`만 `PlayerRef` → `HitActor`로 바꿨다. `BaseDamage ← AttackDamage`, `EventInstigator ← GetController`, `DamageCauser ← K2Node_Self_1` 셋은 손대지 않았다. `K2Node_VariableGet_37`(`AttackMontage` 게터)은 `PlayAnimMontage`에서 `Play Montage`로 옮겨 물렸다.

**노드 단위 — `BP_ThirdPersonCharacter`에서 지운 것**

`K2Node_CallFunction_86`(`Hit:`), `K2Node_CallFunction_87`(`PlayerHP:`), `Append` 둘(`CommutativeAssociativeBinaryOperator_3`·`5`), `K2Node_CallFunction_88`(`ToString(Float)`), `GetDisplayName` 하나

## 분석

### 무엇을 만들었나

**변수 (`BP_Enemy`, 넷)**

- `bIsSwinging` — Boolean, `false`. 타격 창이 열려 있는지. `Event Tick`의 유일한 게이트
- `PrevFistCenter` — Vector, `(0,0,0)`. 직전 프레임의 주먹 월드 위치
- `HitActorsThisSwing` — Actor 배열, 빈 배열. 이번 스윙에서 이미 때린 액터
- `FistRadius` — Float, `15.0`, 인스턴스 편집. 주먹+손목 굵기를 감으로 잡은 값

넷 다 `Default` 카테고리, `Not Replicated`. 싱글이므로 리플리케이션은 건드리지 않았다.

**애니메이션 (`AM_Enemy_Attack`)**

- 슬롯 `DefaultSlot`(전신), 세그먼트 `MM_Attack_01` 하나, 길이 1초, 블렌드 인/아웃 각 0.25초 `HermiteCubic`. 원래 구성이고 안 건드렸다
- 노티파이 트랙 `1`번 줄이 비어 있었다. `Montage Notify Window` `EnemyAttackHit`을 **새로** 찍었다
- 구간은 `Timing` 마커 기준 **프레임 9 → 16**. 실측 창 길이는 로그 기준 `ATTACK`에서 `EnemyHit`까지 `0.322` ~ `0.435`초

**`Think`의 `ATTACK` 갈래 (`EventGraph`)**

바뀌기 전:

```
Branch(거리 ≤ AttackRange 150) True
  → PrintString "ATTACK" → StopMovement → PlayAnimMontage(AttackMontage)
  → ApplyDamage(PlayerRef, AttackDamage 10, GetController, self)
  → Delay(AttackCooldown 1.5) → Think
```

바뀐 뒤:

```
Branch(거리 ≤ AttackRange 150) True
  → StopMovement → Sequence
       Then 0 → Play Montage(Mesh, AttackMontage, PlayRate 1.0,
                             StartingPosition 0.0, StartingSection None,
                             bShouldStopAllMontages true)
       Then 1 → Delay(AttackCooldown 1.5) → Think
```

**타격 창 (`EventGraph`)**

- 열기 — `Play Montage.OnNotifyBegin` → `Name Equal(NotifyName, "EnemyAttackHit")` → `Branch` True → `Set bIsSwinging(true)` → `Clear(HitActorsThisSwing)` → `Set PrevFistCenter ← Mesh.GetSocketLocation("HandGrip_R")`
- 닫기 — `Set bIsSwinging(false)` 하나에 입력 셋. `OnNotifyEnd` + 이름 검사 `Branch`, `OnBlendOut`, `OnInterrupted`

**궤적 판정 (`Event Tick`, `BP_Enemy`)**

- `Branch(bIsSwinging)` — 거짓이면 여기서 끝
- `MultiSphereTraceForObjects` — `Start = PrevFistCenter`, `End = Mesh.GetSocketLocation("HandGrip_R")`, `Radius = FistRadius 15`, `ObjectTypes = [ObjectTypeQuery3]`, `bTraceComplex = false`, `ActorsToIgnore` 비었음, `bIgnoreSelf = true`, `DrawDebugType = None`(작업 중엔 `ForDuration`), `DrawTime = 0.5`, `TraceColor` 빨강, `TraceHitColor` 초록
- `ForEachLoop(OutHits)` → `BreakHitResult` → `Contains(HitActorsThisSwing, HitActor)` → `NOT` → `Branch` True → `Array Add` → `ApplyDamage(HitActor, AttackDamage 10, GetController, self)`
- `Completed` → `Set PrevFistCenter ← Mesh.GetSocketLocation("HandGrip_R")`

**플레이어 (`BP_ThirdPersonCharacter`)**

- `CurrentHP` 기본값 `75 → 100`. `BeginPlay`에 `CurrentHP = MaxHP` 초기화는 **안 넣었다** — 요청 범위 밖
- `AttackRange`(`200`)·`AttackTraceRadius`(`40`) 변수 삭제. 참조하는 노드가 그래프 열 개 전부에서 0개인 것을 확인하고 지웠다
- `Hit:` `PrintString` + `Append` + `GetDisplayName` 삭제. `Array Add → ApplyDamage` 직결
- `MultiBoxTraceForObjects`의 `DrawDebugType` `ForDuration → None`
- `ShowHUDMessage` 함수 그래프의 `PrintString`(`K2Node_CallFunction_6`)은 **남겼다.** 기능이다

**임시로 넣었다 뺀 것**

- `BP_Enemy`의 `"EnemyHit: " + GetDisplayName(HitActor)` `PrintString`
- `BP_ThirdPersonCharacter`의 `"PlayerHP: " + ToString(Float)` `PrintString`. `Set CurrentHP`의 `Output_Get` 핀에서 값을 받았다

### 기술적으로 맞게 짚은 부분

**애셋 경로를 디스크에서 먼저 찾은 것.**
`list_graphs`가 `/Game/ThirdPerson/Blueprints/BP_Enemy.BP_Enemy`를 거부했을 때, MCP 버그로 넘기지 않고 `find Content -iname "BP_*.uasset"`으로 실제 위치를 찾았다. `BP_Enemy`는 `/Game/Enemy/`에 있었다. **지난 기록에 "MCP가 블루프린트 애셋 경로를 거부하는 새 형태"로 적혀 있던 것이 실은 내가 경로를 틀린 것이었다.** 올바른 경로로는 `list_graphs`·`read_graph_dsl`·`list_variables`가 전부 된다.

**`bShouldStopAllMontages`와 콜백 발화 규칙을 소스에서 확인한 것.**
`UPlayMontageCallbackProxy::OnMontageBlendingOut`은 `bInterrupted`면 `OnInterrupted`를 쏘고 플래그를 세우며, 아니면 `OnBlendOut`을 쏜다. `OnMontageEnded`는 `!bInterrupted`면 `OnCompleted`를, 플래그가 안 섰으면 `OnInterrupted`를 쏜다 (`PlayMontageCallbackProxy.cpp:104-127`). 즉 **정상 재생이면 `OnBlendOut`과 `OnCompleted`가 둘 다 뜨고, 중단이면 `OnInterrupted`만 한 번 뜬다.** `Think` 루프를 `OnBlendOut`으로 재개했으면 중단 시 루프가 멈추고, `OnCompleted`+`OnBlendOut` 둘 다 물렸으면 루프가 두 배로 돈다. 이걸 명령을 쓰기 전에 확인해서 그 함정을 안 밟았다.

**`AnimInstance` 델리게이트 우회로를 소스로 배제한 것.**
`BeginPlay`에서 `OnPlayMontageNotifyBegin`/`End`에 바인딩하면 `Think`를 아예 안 건드려도 됐다. 그런데 그 둘에는 `UPROPERTY(BlueprintAssignable)`이 없다 (`AnimInstance.h:1818-1823`). **`Play Montage` 노드가 유일한 경로**라는 것을 확인하고 나서 `Think` 재배선으로 갔다. 확인 안 했으면 있지도 않은 노드를 찾으라는 명령을 냈을 것이다.

**구체 트레이스를 고른 것.**
`SphereTraceMultiForObjects`에는 회전 인자가 없다 (`KismetSystemLibrary.h:1444`). 칼은 긴 막대라 방향이 있어서 상자가 필요했지만, **주먹은 방향이 없다.** 구체로 가면서 `MakeVector`와 `GetWorldRotation` 두 노드가 안 생겼다. 지난 세션에 "캡슐에 회전이 있을 것"으로 잘못 적었던 것을 반복하지 않으려고 이번엔 명령을 쓰기 전에 시그니처를 읽었다.

**튜닝 값이 안 바뀌는 구조를 고른 것.**
`Sequence`의 `Then 1`로 `Delay(AttackCooldown)`을 태워서 **몽타주 시작 시점 기준 1.5초**를 유지했다. `OnCompleted`로 재개했으면 몽타주 1초가 앞에 붙어 실질 2.5초가 됐다. 로그에서 여덟 번 전부 `1.502` ~ `1.516`초로 나왔다 — **손으로 맞춘 값을 안 건드린다는 규칙이 측정으로 지켜졌다.**

**`ApplyDamage`를 지우지 않고 옮긴 것.**
`EventInstigator ← GetController`, `DamageCauser ← self` 배선이 이미 맞게 물려 있었다. 새로 만들었으면 그 둘을 다시 이어야 했고, `self` 참조 노드도 새로 만들어야 했다. 명령 4에서 "지울 것"과 "끊되 남길 것"을 나눠 적은 덕에 명령 5에서 연결 두 개로 끝났다.

**배치 인스턴스를 되읽은 것.**
명령 1에서 `FistRadius`를 "default value 15.0"으로 만들라고 명시했고 CDO는 `15`로 나왔다. 그런데 **배치 인스턴스는 `0`이었다.** CDO만 봤으면 반지름 0으로 훑는 것을 PIE에서야 알았을 것이고, "맞아도 데미지가 안 들어간다"는 증상에서 원인까지 한참 걸렸을 것이다.

**디버그 제거를 맨 마지막으로 미룬 것.**
`ATTACK` 표시와 초록 구체가 없으면 새 판정이 되는지 볼 수단이 없다. 사용자가 디버그 제거를 다른 항목과 같이 지시했지만 **순서는 내가 정해서 맨 뒤로 보냈다.** 결과적으로 합격 기준 넷 중 셋을 그 표시들로 확인했다.

**임시 로그를 넣기 전에 "무엇을 못 보고 있는가"를 먼저 말한 것.**
합격 기준 1은 "플레이어 HP가 정확히 10 준다"인데, `EnemyHit:`만으로는 `ApplyDamage`가 불렸다는 것까지밖에 모른다. 그 간극을 "절반만 확인됐다"로 보고하고 임시 `PrintString`을 제안했다. 넣고 나서 `100 → 90 → 80 → 70 → 60`이 나왔다.

**같은 이름의 변수를 명령문에서 명시적으로 갈라놓은 것.**
`AttackRange`가 `BP_ThirdPersonCharacter`(`200`, 미사용)와 `BP_Enemy`(`150`, 사용 중) 양쪽에 있었다. 명령 7에 "a DIFFERENT Blueprint ... also has a variable named AttackRange and that one IS still in use - do not open or modify that Blueprint"를 넣었다. 확인 결과 `BP_Enemy`의 변수 21개가 그대로였다.

### 확인한 것 / 확인 못 한 것

**확인한 것**

- **`BP_Enemy` 변수 넷** — CDO에서 되읽어 `{"bIsSwinging":false,"PrevFistCenter":{"x":0,"y":0,"z":0},"HitActorsThisSwing":[],"FistRadius":15}`. 카테고리 `Default`, `HitActorsThisSwing`의 리플리케이션 `None`
- **배치 인스턴스의 `FistRadius`** — 처음 `0`이었던 것을 명령 2로 `15`로 고치고 되읽어 확인
- **`AM_Enemy_Attack`의 노티파이** — 사용자 화면. `Notifies` 트랙 `1`번 줄에 구간 막대 **하나뿐**, 이름 `EnemyAttackHit`, `Timing` 마커가 프레임 9와 16
- **`Play Montage` 배선 전부** — `get_node_infos`로 입력 일곱과 출력 여섯의 연결을 하나씩 확인. `OnBlendOut`과 `OnInterrupted`가 같은 `Set bIsSwinging(false)`에 물린 것까지
- **`Sequence` 배선** — `execute ← StopMovement`, `then_0 → Play Montage`, `then_1 → 기존 Delay`
- **`MultiSphereTraceForObjects` 입력 전부** — `Start`/`End`/`Radius`/`ObjectTypes`/`bTraceComplex`/`ActorsToIgnore`/`bIgnoreSelf`/`DrawDebugType`/`DrawTime` 각각 어느 노드에서 오는지
- **`ApplyDamage` 재사용** — 노드 ID가 `K2Node_CallFunction_49`로 같고, `DamagedActor`만 `BreakHitResult`의 `HitActor`로 바뀌었고, 나머지 셋은 그대로
- **`PlayerRef` 게터가 안 지워진 것** — 연결이 6개에서 5개로 줄었을 뿐
- **합격 기준 1** — `PlayerHP: 90.0 → 80.0 → 70.0 → 60.0`. 네 번 전부 정확히 10. `EnemyHit`과 같은 프레임 번호에 찍혔다
- **합격 기준 3** — 공격 열세 번 전부 `EnemyHit:`이 0줄 또는 1줄. 두 줄 난 적 없음
- **합격 기준 4** — `ATTACK`에서 다음 상태 표시까지 여덟 번 전부 `1.502` ~ `1.516`초
- **디버그 제거 후 로그** — PIE 두 번에 `LogBlueprintUserMessages`가 `EnemyHP:` 여섯 줄뿐. 상태 표시 여섯·수치 표시 셋·`EnemyHit:`·`PlayerHP:`·`Hit:` 전부 사라짐
- **디버그 제거 후에도 칼 판정이 산다는 것** — `EnemyHP: 100 → 66 → 32 → 0`이 두 번. 34씩 세 번
- **`Think`의 여섯 갈래가 안 끊긴 것** — `read_graph_dsl`로 `ATTACK`/`CHASE`/`RETURN`/`IDLE_HOME`/`IDLE_WAIT`/`NO_PLAYER` 각각의 이동 호출과 `Delay → Think` 재귀를 확인
- **`ShowHUDMessage`의 `PrintString`이 남은 것** — `find_nodes`로 `K2Node_CallFunction_6` 존재 확인
- **`BP_ThirdPersonCharacter` 변수 19개** — `AttackRange`·`AttackTraceRadius` 없음, `BP_Enemy`의 변수 21개는 그대로
- **`DT_Items`의 `Knife` 행** — 에디터 값이 커밋된 값과 같음. `Translation (0,0,25)`, `Rotation` 단위값, `Scale3D (0.04,0.04,0.5)`. **지난 기록의 "저장됐는지 모른다" 항목이 여기서 닫혔다**

**확인 못 한 것**

- **합격 기준 2 (비켜서면 안 맞음)** — 통제된 시험이 아니다. 공격 열세 번 중 네 번이 `EnemyHit` 없이 지나갔지만, **거리와 각도를 정해놓고 "이 위치에서는 안 맞는다"를 확인한 것이 아니다.** 사용자가 자유롭게 움직이는 중에 나온 정황이다
- **컴파일 경고 원문** — 명령마다 "compile and report any errors or warnings"를 요구했지만 터미널 출력이 한 번만 들어왔고 그 안에도 컴파일 보고가 없다. 컴파일이 통과했다는 것은 PIE가 새 동작으로 돌았다는 데서 간접적으로만 안다
- **인스턴스 편집 플래그** — MCP가 변수의 edit 지정자를 못 읽는다. `FistRadius`가 실제로 인스턴스 편집인지, 나머지 셋이 아닌지 확인 못 했다
- **노티파이가 정확히 `Montage Notify Window` 클래스인지** — MCP가 `Notifies`를 못 읽는다. 화면에서 구간 막대라는 것과 `OnNotifyEnd`가 실제로 떠서 창이 닫혔다는 동작 근거뿐이다
- **`bIsSwinging`·`PrevFistCenter`·`HitActorsThisSwing` 셋의 인스턴스 함정 여부** — 기본값이 전부 0/빈 값이라 배치 인스턴스가 굳혔는지 아닌지 **구분이 안 된다.** 값이 같아서 문제가 안 될 뿐이다
- **적의 `RETURN`/`IDLE_HOME` 복귀와 플레이어 사망·리스폰** — 디버그 제거 후 확인 항목으로 요청했지만 그 경로의 표시를 지워서 프로그램적 증거가 없다. **사용자가 화면에서 "이상없음"으로 본 것이 유일한 근거다**
- **적이 둘 이상일 때** — `MultiSphereTrace`라 여럿이 잡히도록 만들었지만 적이 하나뿐이라 시험 못 했다
- **`Event Tick`의 한 프레임 지연** — 플레이어 쪽과 같은 구조적 가능성이 적에게도 있다. 측정 안 했다
- **`BP_ThirdPersonCharacter.uasset`이 세션 시작 때 이미 dirty였던 이유** — 오늘 플레이어 BP를 건드리기 전부터 저장 대상에 들어 있었다. CDO 값은 안 바뀐 것을 확인했지만 **왜 dirty였는지는 모른다**

### 남는 리스크

- **~~`Sequence`가 불필요하다~~ — 같은 세션에서 제거했다.** `Play Montage` 노드에는 `then` 핀이 index 0으로 실제로 있는데, 내가 헤더의 `BlueprintAssignable` 목록만 보고 "즉시 실행 핀이 없다"고 단정해서 넣었던 구조다. `StopMovement → Play Montage`, `Play Montage.then → Delay → Think`로 바꿨다. **제거 후 공격 주기를 측정하지 않았다** — `ATTACK` 표시를 이미 지운 뒤라 로그로 잴 수 없었고, 사용자가 PIE 화면에서 "괜찮은 것 같다"고 본 것이 유일한 근거다
- **배치 인스턴스의 `FistRadius` 덮어쓰기 상태를 프로그램적으로 확인할 수단이 없다.** 기록 작성 후 `ObjectTools.reset_properties`를 걸었지만 `__ExternalActors__` 파일이 안 바뀌었고, Details 패널에는 되돌리기 화살표가 **없었다**(사용자 화면). 화살표가 없는 것은 "덮어쓰기가 없다"와 "덮어쓰기 값이 CDO와 같아서 안 뜬다" 양쪽에 다 맞아서 **구분이 안 된다.** UE가 어느 쪽으로 동작하는지 확인하지 않았다. 값이 `15`로 맞으므로 실용적 문제는 없고, **나중에 CDO의 `FistRadius`를 바꿀 때 인스턴스를 되읽으면 그 자리에서 드러난다**
- **`FistRadius 15`에 근거가 없다.** 주먹 굵기를 감으로 잡았다. 너무 크면 스치기만 해도 맞고, 너무 작으면 정타도 빠진다. 인스턴스 편집으로 열려 있어서 PIE에서 맞출 수는 있다
- **적이 다른 적을 때린다.** `ObjectTypes`가 `Pawn`뿐이고 `bIgnoreSelf`는 자기만 막는다. 지금 적이 하나뿐이라 안 드러난다. 심문 6번에서 사용자가 (a)로 고른 결과다
- **벽을 무시한다.** 플레이어 쪽과 같은 이유다. 주먹 사거리 15cm라 실사용에서 잘 안 나겠지만 원리상 뚫린다
- **`Event Tick`이 `BP_Enemy`에도 생겼다.** 창이 닫혀 있으면 `Branch` 하나지만, 이 블루프린트에 Tick 경로가 생긴 것 자체가 새 사실이다. 이제 플레이어와 적 양쪽에 Tick이 있다
- **적의 상태를 볼 수단이 사라졌다.** `1_state` 표시 여섯과 거리·각도 표시 셋을 전부 지웠다. 다음에 적 AI가 이상하게 굴면 **그 표시들을 다시 심는 것부터** 시작해야 한다. 지운 노드 ID와 재연결 지점은 이 기록의 명령 8에 남아 있다
- **`ReturnStepDistance`가 미사용이다.** `BP_Enemy`의 변수인데 그래프 어디에서도 안 읽힌다. 오늘 범위 밖이라 안 건드렸다
- **`MM_Attack_01`은 주먹 모션이다.** 적에게는 이게 맞다 — 적은 맨손이다. 플레이어 쪽에서만 어긋난 채로 남아 있다
- **몽타주 노티파이는 여전히 화면으로만 안다.** MCP가 `Notifies`를 못 읽는다. 이번엔 사용자가 화면을 보내줘서 하나뿐인 것을 확인했지만, 프로그램적 수단은 지난 세션에 쓴 "창 열림 로그를 임시로 심는 것"이 유일하다
- **`AM_Player_Attack`과 `AM_Enemy_Attack`의 노티파이 구간이 다르다.** 같은 `MM_Attack_01`인데 플레이어는 9~14, 적은 9~16이다. 내가 화면 한 장을 보고 뒤를 넓힌 결과이고, 통일할 이유가 생기면 어느 쪽이 맞는지 다시 봐야 한다

### 총평

요청은 여섯이었고 여섯 다 처리했다. 넷은 만들었고, 하나(`K2Node_Self_1` 이동)는 안 했고, 하나(칼 회전 45도)는 안 보기로 했다.

**핵심 작업인 적 궤적 판정은 합격 기준 넷 중 셋을 로그로 확인했다.** 기준 2만 정황이다 — 이건 지난 세션 플레이어 쪽과 정확히 같은 상태이고, 두 세션 연속으로 같은 항목이 미확인으로 남았다.

이 작업의 실질적 난이도는 세 군데였다.

첫째는 **명령을 쓰기 전에 엔진 소스를 읽은 것**이다. 지난 세션에 "캡슐에 회전 인자가 있을 것"으로 적었다가 명령 하나를 버렸다. 이번엔 `Play Montage`의 콜백 발화 규칙, `AnimInstance` 델리게이트의 `BlueprintAssignable` 여부, 구체 트레이스의 시그니처 셋을 사양 단계에서 읽었다. 그 결과 **루프가 두 번 도는 함정과 없는 노드를 찾으라는 명령 둘을 미리 피했다.** 다만 같은 소스를 읽고도 `Play Montage`의 `then` 핀은 놓쳤다 — `UPROPERTY` 목록만 보고 K2Node가 만드는 핀 전체를 확인하지 않았다.

둘째는 **인스턴스 함정이다.** 메모리에 이미 적혀 있는 함정인데, 명령문에 "default value 15.0"을 명시했음에도 배치 인스턴스가 `0`을 굳혔다. **명령을 어떻게 쓰든 막을 수 없다는 뜻이다.** 유일한 방어는 만든 뒤에 CDO와 인스턴스를 따로 되읽는 것이고, 이번에 그걸 해서 PIE 전에 잡았다. 나머지 세 변수는 기본값이 0/빈 값이라 함정에 걸렸는지조차 알 수 없다는 것도 이 과정에서 드러났다.

셋째는 **검증 수단을 스스로 없애는 작업의 순서**다. 디버그 제거는 사용자가 다른 다섯 항목과 나란히 지시했지만, 먼저 하면 새로 만든 것을 볼 눈이 없어진다. 순서를 맨 뒤로 미루고, 그 전에 임시 `PrintString` 둘을 넣어 합격 기준 1을 확정하고, 마지막에 그 둘까지 같이 지웠다. **지우는 명령에 "무엇을 남길지"를 노드 ID로 못박아 적은 것**이 `EnemyHP:`와 `ShowHUDMessage`를 살렸다.

부수적으로 **지난 기록의 관찰 하나가 틀렸다는 것**을 알았다. "MCP가 블루프린트 애셋 경로를 거부한다"는 항목은 내가 `BP_Enemy`의 경로를 `/Game/ThirdPerson/Blueprints/`로 잘못 알고 있었던 것이다. 실제 위치는 `/Game/Enemy/`다. 이걸 안 잡았으면 이번에도 우회로를 찾느라 시간을 썼을 것이고, 기록은 틀린 채로 한 번 더 굳었을 것이다. **기록이 틀릴 수 있다는 것, 그리고 디스크에서 직접 확인하는 것이 그걸 깨는 방법이라는 것**이 이 세션에서 가장 값이 컸다.

## AI의 제안

> **(a) 구체** — `MultiSphereTraceForObjects`, 반지름 **15cm**(내가 정한 값). 회전 인자가 필요 없어서 `GetSocketRotation`·`MakeVector` 노드가 안 생긴다. 주먹은 방향성이 없으니 모양이 실물에 맞다

얻는 것 — 노드 둘이 줄고, 판정 모양이 주먹이라는 실물과 맞는다. 잃는 것 — 플레이어의 상자 판정과 구조가 달라져서 "같은 판정"이라고 말할 때 한 줄 설명이 더 필요하다.

> **(a) `Sequence` 노드로 가른다** — `Then 0` → `Play Montage`, `Then 1` → `Delay(AttackCooldown)` → `Think`. **현재 공격 주기가 정확히 보존된다** (몽타주 시작 시점 기준 1.5초)

얻는 것 — 손으로 맞춘 `AttackCooldown 1.5`가 그대로 지켜진다. 실측 `1.502` ~ `1.516`초. 잃는 것 — 나중에 밝혀졌듯 `Play Montage`에 `then` 핀이 있어서 이 노드는 없어도 됐다. 불필요한 노드 하나.

> **순서는 제가 정합니다** — 디버그 제거는 **맨 마지막**에 합니다. 적 궤적 판정이 되는지 확인하려면 `"ATTACK"` 표시와 `MultiBoxTrace`의 빨간 상자가 필요합니다

얻는 것 — 합격 기준 넷 중 셋을 그 표시들로 확인할 수 있었다. 잃는 것 — 없다. 사용자 요청 여섯 개의 순서를 내가 바꾼 것이지만 항목을 뺀 것은 아니다.

> **플레이어 `EventAnyDamage`에 `"PlayerHP: " + CurrentHP` `PrintString`을 넣을까요?** 합격 기준 1("플레이어 HP가 정확히 10 줄어든다")을 확인할 유일한 수단입니다

얻는 것 — `100 → 90 → 80 → 70 → 60`이 로그에 남아 기준 1이 "절반 확인"에서 "확인"으로 바뀌었다. 잃는 것 — 임시 노드 셋을 넣었다 빼는 왕복 한 번.

> **`BP_Enemy`에 `ReturnStepDistance`라는 변수가 있는데 그래프 어디에서도 안 읽힙니다. 오늘 범위 밖이라 안 건드립니다**

얻는 것 — 요청 범위를 넘지 않으면서 다음에 처리할 것을 남겼다. 잃는 것 — 미사용 변수가 하나 더 남아 있다.

> **`Content/Enemy/BP_Enemy.uasset`이 아직 없습니다.** 변수 넷과 그래프 변경 전부가 에디터 메모리에만 있습니다. 지금 에디터가 죽으면 다 날아갑니다

얻는 것 — `git status`와 파일 mtime으로 "저장됐는가"를 세 번 확인했고, 마지막 한 번은 명령 7·8이 디스크에 없다는 것을 잡아냈다. 잃는 것 — 없다.

## 다음으로 넘김

**바로 이어서 할 것**

- 없음. 기록 작성 후 정리 작업 넷(`Sequence` 제거, `ApplyDamage` 클러스터 이동, `ReturnStepDistance` 삭제, 인스턴스 `FistRadius` 리셋)을 같은 세션에서 이어서 했다. 그 결과는 아래에 반영했다

**결정 필요**

- **`FistRadius 15`가 적당한가.** 근거 없이 정한 값이다. 실제로 쳐보면서 맞출 것인지, 지금 값으로 둘 것인지
- **플레이어 `BeginPlay`에 `CurrentHP = MaxHP` 초기화를 넣을 것인가.** 적에는 있고 플레이어에는 없다. 지금은 변수 기본값 `100`이 곧 시작 체력이라 동작에 문제는 없다
- **`AM_Player_Attack`의 노티파이 구간을 9~16으로 맞출 것인가.** 지금 플레이어 9~14, 적 9~16으로 다르다. 같은 `MM_Attack_01`인데 값이 갈려 있다
- **적 상태 표시를 다시 심을 것인가.** 지웠으므로 적 AI가 이상하게 굴면 볼 수단이 없다. 다시 심는 명령은 이 기록의 명령 8을 뒤집으면 된다

**확인 필요**

- **합격 기준 2의 통제된 시험.** 거리와 각도를 정해놓고 빗나가는 것을 확인. **플레이어 쪽도 적 쪽도 두 세션 연속 미확인이다**
- **적의 `RETURN`/`IDLE_HOME` 복귀와 플레이어 사망·리스폰.** 디버그 제거 후 사용자 화면으로만 "이상없음"을 봤다. 로그 증거가 없다
- **적이 둘 이상일 때 한 스윙으로 둘 다 맞는지.** 플레이어 쪽과 같은 미확인 항목이다
- **`bIsSwinging`·`PrevFistCenter`·`HitActorsThisSwing`의 배치 인스턴스 값.** 기본값이 0/빈 값이라 인스턴스가 굳혔는지 구분이 안 된다. 나중에 기본값을 바꿀 일이 생기면 이게 문제가 된다
- **`BP_ThirdPersonCharacter.uasset`이 세션 시작 때 이미 dirty였던 이유.** CDO 값은 안 바뀐 것을 확인했지만 원인은 모른다
- **컴파일 경고 원문.** 여덟 개 명령 전부 "compile and report any errors or warnings"를 요구했는데 한 번도 받지 못했다. **UE Terminal이 그 보고를 어디에 뱉는지 자체를 모른다**
- **MCP 인자 이름이 스키마와 다른 사례 셋.** `get_properties`는 `property_names`가 아니라 `properties`, `get_socket_names`는 `skeletal_mesh`가 아니라 `mesh`, `get_pin_value`는 `node`+`pin_name`이 아니라 `pin` 객체 하나. 셋 다 실패 응답에 전체 스키마가 딸려 와서 고칠 수 있었다
- **`get_connected_subgraph`가 큰 그래프에서 못 쓴다.** `BP_Enemy`의 `K2Node_IfThenElse_5`에 걸었더니 `111,791 characters`가 돌아와서 잘렸다. `read_graph_dsl`이 같은 정보를 훨씬 작게 준다
- **MCP가 못 읽는 프로퍼티 목록.** `Notifies`, `AnimNotifyTracks`, `BranchingPointMarkers`, `BranchingPointStateNotifyIndices`, `ActiveStateBranchingPoints`, `CompositeSections`, `AttachSocketName`, `attachParent`, `CollisionEnabled`, `NewVariables`, `ActorLabel`. 이번에 `AM_Enemy_Attack`에서 앞의 둘이 또 실패했다
- **`_C_0`이 아닌 플레이어 인스턴스.** 예전 로그에 `BP_ThirdPersonCharacter_C_7`이 있었다. 오늘 로그에도 `_C_0`만 찍혔다. 다만 `EnemyHit:`이 가리킨 액터 이름은 `BP_ThirdPersonCharacter0`(언더스코어 없음)이었다 — `GetDisplayName`과 로그 접두어가 서로 다른 이름을 쓴다
- **`2026-09-01-enemy-hp-death.md`의 `확인 필요` 목록.** `arrange_nodes`, `read_graph_dsl` 절단, `EditorPerProjectUserSettings.ini` 저장 실패, `CaptureViewport`가 에디터 월드를 그리는 것 등이 그 파일에 그대로 있다. **이번 세션에 `read_graph_dsl`은 `BP_Enemy`·`BP_ThirdPersonCharacter` 양쪽에서 잘리지 않고 전문이 나왔다**

**접어둔 것**

- **Mixamo 등 외부 베기 애니메이션.** 프로젝트에 IK Rig도 IK Retargeter도 없고 MCP 툴셋에도 리타깃 도구가 없다. 한 세션짜리 수작업이다
- **`MM_Attack_02` / `MM_Attack_03` / `MM_ChargedAttack`.** 사용자가 열어보고 "셋 다 칼이랑 관련없음"으로 확인했다. 칼에 쓸 수 없다는 것만 안다
- **진짜 칼 메시 구하기.** 구하면 `BladeHalfLength`와 중심 오프셋을 손잡이 위로 옮겨 "칼날만" 판정이 된다
- **`Knife`와 `Key_Stage1`이 같은 `Cube` 메시라 색이 같은 것.** 머티리얼로 가를 수 있다
- **`heldTransform`의 회전·오프셋이 짝이라는 사실을 `DT_Items` 어디에도 안 적어뒀다.** 주석 칸이 없다
- **적 공격 이펙트·사운드.** 판정만 만들었다
- **맞은 액터가 플레이어인지 검사하는 분기.** 두 번째 적이 실제로 생겼을 때 단다
