# 2026-09-02

## 작업물

만들어놓고 시험 못 한 두 경로를 적 둘로 검증하고, 그 과정에서 드러난 적끼리 때리는 문제를 막은 것. 그리고 미뤄둔 정리 넷 — 불필요한 `Sequence` 제거, `ApplyDamage` 클러스터 이동, 미사용 변수 삭제, 배치 인스턴스 덮어쓰기 리셋 시도.

**소요 시간**: 앞선 기록(`2026-09-02-enemy-fist-trace.md`)을 커밋한 뒤부터 이 기록을 쓰기까지. 커밋 `b55df0b`가 로컬 `14:2x`, 마지막 커밋 `0f7850d`가 로컬 `17:07`. 약 **2시간 45분**. 그 안에 에디터 재시작 한 번이 들어 있다. 정확한 세션 경계는 커밋 시각으로만 잡았고, 중간에 대화만 오간 구간은 로그도 파일도 안 남긴다.

## 명령

### 한글

```
가벼운것들만 다하고 다음으로 넘어가자
```
```
이대로하자
```
```
결과확인
```
```
결과확인
```
```
공격주기 괜찬은거같에 PIE 했는데 딱히 문제될 건 안보이거든? 일단 PIE까지 다했어
```
```
저장했으
```
```
a로 하자
```
```
이거바바
```
```
다음꺼하자
```
```
a로 하자 커밋하고 이거 비켜서면 걍 주먹 경로에 없어서 안맞는거 아님?
```
```
에디터 껏다킴 잠만
```
```
켰어
```
```
결과 확인
```
```
결과확인
```
```
결과 확인좀
```
```
a
로그에 PlayerHP도 추가할까그럼?
```
```
결과 확인
```
```
결과 확인
```
```
PIE 결과 이상 없어보임
```
```
커밋하고 레벨에 남기자 적두마리로
```
```
결과 확인
```
```
저장했는데 봐봐
```
```
했어
```
```
새로 쓰자그럼
```

### English — MCP에 실제로 보낸 명령

**이번에도 영어 명령은 내가 MCP로 보낸 것이 아니다.** 전부 **사용자가 UE Terminal에 붙여넣도록 만들어 건넨 원문**이다. 내가 직접 부른 MCP는 전부 읽기 호출이었다 — `list_graphs`, `read_graph_dsl`, `find_nodes`, `get_node_infos`, `list_variables`, `get_properties`, `get_pin_value`, `get_label`, `get_current_level`, `get_actors_in_folder`, `find_actors`, `get_socket_transform`, `describe_toolset`, `GetLogEntries`. 아래는 Terminal에 건넨 영어 원문 그대로다.

**명령 9 — `BP_Enemy` 노드 위치 정리 + 미사용 변수 삭제**

```
Work in /Game/Enemy/BP_Enemy.

PART 1 - move four nodes only. Change POSITIONS ONLY. Do not add, delete, connect or
disconnect anything. These four currently sit in the old Think row at y=700 even though
ApplyDamage now runs from the Event Tick chain at y=2450:

  K2Node_CallFunction_49   (ApplyDamage)          from (10080, 700) to (11100, 2450)
  K2Node_VariableGet_38    (AttackDamage getter)  from ( 9520, 700) to (10800, 2700)
  K2Node_CallFunction_48   (GetController)        from ( 9800, 700) to (10800, 2820)
  K2Node_Self_1            (Self reference)       from (    0, 420) to (10800, 2940)

Do not move any other node. In particular do not move K2Node_CallArrayFunction_3
(the Array Add at (10620, 2450)) or K2Node_CallFunction_94 (the trace node).

PART 2 - delete one unused variable.

  Delete the variable "ReturnStepDistance" (Float, currently 300) from this Blueprint.
  No node reads it - searching both the EventGraph and the UserConstructionScript for
  "Return" returns no getter or setter for it.

  Delete ONLY that one. Do NOT touch ReturnDelay or ReturnSightRange - both are still
  in use by the Think event.

Then compile the Blueprint and report: any compile errors or warnings, the positions of
the four moved nodes, and the full list of variables remaining on BP_Enemy.
```

**명령 10 — `Sequence` 제거**

```
Work in the EventGraph of /Game/Enemy/BP_Enemy.

Remove the Sequence node, which turned out to be unnecessary. The Play Montage node
has a plain "then" exec output pin (index 0) that fires immediately, so the Sequence
adds nothing.

Current wiring:
  K2Node_CallFunction_46      (StopMovement)
    -> K2Node_ExecutionSequence_0 (Sequence)
         Then 0 -> K2Node_PlayMontage_0  (Play Montage)
         Then 1 -> K2Node_CallFunction_50 (Delay)

Target wiring:
  K2Node_CallFunction_46      (StopMovement)
    -> K2Node_PlayMontage_0   (Play Montage)
         then (the plain exec output, index 0, currently unconnected)
           -> K2Node_CallFunction_50 (Delay)

Steps:
1. Delete K2Node_ExecutionSequence_0.
2. Connect StopMovement's "then" output to Play Montage's exec input.
3. Connect Play Montage's plain "then" output pin - the first exec output, NOT
   OnCompleted, NOT OnBlendOut, NOT OnInterrupted, NOT OnNotifyBegin, NOT OnNotifyEnd -
   to the exec input of the existing Delay node K2Node_CallFunction_50.

Do not touch anything else on the Play Montage node. Its OnNotifyBegin / OnNotifyEnd /
OnBlendOut / OnInterrupted chains, its Mesh and AttackMontage inputs, and the Delay's
Duration <- AttackCooldown wiring and its "then" -> Think call all stay exactly as they
are.

Then compile the Blueprint and report: any compile errors or warnings, and every node
connected to K2Node_PlayMontage_0 with the pin name each connection uses.
```

**명령 11 — 배치 인스턴스 `FistRadius` 덮어쓰기 지우기**

```
In the currently loaded level, there is one placed BP_Enemy actor at this path:
/Game/ThirdPerson/Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879

That actor has a per-instance override on FistRadius. It was written to 15 earlier,
which happens to match the class default, but the override itself is still there - so
if the class default ever changes, this instance will not follow.

Use ObjectTools.reset_properties on that actor with properties = ["FistRadius"] to
remove the per-instance override so it inherits from the class default instead.
Do NOT use set_properties - writing the value back is what created this situation.

Do not reset or change any other property on that actor. Do not touch the class
defaults.

Then save the actor, read FistRadius back from that actor instance, and report its
value.
```

**명령 12 — 디버그 도형 임시 복구**

```
Two trace nodes currently have DrawDebugType set to None. Set both back to ForDuration
temporarily. Change ONLY the DrawDebugType pin on each - do not touch any other pin,
node, or variable.

1. In the EventGraph of /Game/Enemy/BP_Enemy:
     node K2Node_CallFunction_94 (MultiSphereTraceForObjects, inside Event Tick)
     set its DrawDebugType input pin from None to ForDuration
     leave DrawTime at 0.5

2. In the EventGraph of /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter:
     node K2Node_CallFunction_31 (MultiBoxTraceForObjects, inside Event Tick)
     set its DrawDebugType input pin from None to ForDuration
     leave DrawTime at 0.5

Do not restore any PrintString node. Do not change any variable default.

Then compile both Blueprints and report the DrawDebugType and DrawTime values on both
nodes.
```

**명령 13 — 적 하나 추가 배치**

```
Place one more BP_Enemy in the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson.

Use SceneTools.add_to_scene_from_asset with:
  asset_path = /Game/Enemy/BP_Enemy
  name       = Enemy_Test2
  xform      = location (4000, 150, 90), rotation pitch 0 yaw 180 roll 0, scale (1,1,1)
  parent     = not set
  snap_to_ground = false

For reference, the existing enemy Enemy_Test sits at location (4000, 0, 90) with
yaw 180, so this puts the new one 150cm to its side facing the same way.

Then put Enemy_Test2 in the same outliner folder as Enemy_Test.

Do not move, modify or delete Enemy_Test. Do not change the BP_Enemy class defaults.

Then save the new actor and report:
  - the new actor's full path and its world location and rotation
  - the values of FistRadius, AttackRange, AttackDamage, AttackCooldown and MaxHP
    read back FROM THE NEW ACTOR INSTANCE (not from the class defaults)
```

**명령 14 — 적이 적을 때리지 않게**

```
Work in the EventGraph of /Game/Enemy/BP_Enemy, inside the Event Tick chain.

Right now every Pawn the fist sweep touches takes damage, including other BP_Enemy
actors. Restrict the damage to the player only.

Current wiring inside the ForEachLoop body:
  K2Node_IfThenElse_8       (the Branch on NOT Contains)
    True -> K2Node_CallArrayFunction_3   (Array Add into HitActorsThisSwing)
            -> K2Node_CallFunction_49    (ApplyDamage)

Target wiring:
  K2Node_IfThenElse_8
    True -> K2Node_CallArrayFunction_3   (Array Add - unchanged)
            -> NEW Branch
                 True -> K2Node_CallFunction_49  (ApplyDamage)
                 False -> nothing

Steps:
1. Break the exec connection from K2Node_CallArrayFunction_3 to K2Node_CallFunction_49.
2. Create an object equality node (Equal, object reference) and wire its two inputs:
     A = the Hit Actor output of K2Node_CallFunction_96 (the BreakHitResult node,
         output pin index 9) - the SAME pin that already feeds Array Add and
         ApplyDamage's DamagedActor
     B = the EXISTING PlayerRef getter K2Node_VariableGet_30
3. Create a new Branch. Its Condition = that equality node's output.
4. Wire K2Node_CallArrayFunction_3's "then" -> the new Branch's exec input.
5. Wire the new Branch's True pin -> K2Node_CallFunction_49's exec input.
   Leave the new Branch's False pin unconnected.

Do not change ApplyDamage's DamagedActor, BaseDamage, EventInstigator or DamageCauser
inputs. Do not touch the trace node, the ForEachLoop, the Contains/NOT chain, or the
Completed -> Set PrevFistCenter wiring. Do not delete K2Node_VariableGet_30 - five
other nodes read from it.

Then compile the Blueprint and report: any compile errors or warnings, and the full
exec chain inside the ForEachLoop body from K2Node_IfThenElse_8 onward.
```

**명령 15 — 플레이어 HP 로그 (영구)**

```
Work in the Blueprint /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.

Add a PrintString inside Event AnyDamage that reports the player's HP after damage,
mirroring the "EnemyHP: " PrintString that BP_Enemy already has. This one is permanent,
not a temporary debug node.

1. There are two "Set CurrentHP" nodes in the EventGraph. Work ONLY on
   K2Node_VariableSet_0, the one at position (1200, 4700) whose exec input comes from
   the Branch K2Node_IfThenElse_2 and whose "then" currently runs into the Branch
   K2Node_IfThenElse_8. That is the one inside Event AnyDamage.
   Do NOT touch the other Set CurrentHP at (200, 2200) - that is the healing path.

2. Insert a new PrintString between K2Node_VariableSet_0 and K2Node_IfThenElse_8, so
   the exec order becomes:
     Set CurrentHP (K2Node_VariableSet_0) -> new PrintString -> Branch (K2Node_IfThenElse_8)

3. Wire that PrintString's InString from a new Append node built as
   "PlayerHP: " + ToString(Float) of the Output_Get pin on K2Node_VariableSet_0
   (the Set node's own value output pin, currently unconnected).

4. Leave PrintToScreen, PrintToLog, TextColor, Duration and Key at their defaults.

Do not change anything else. Do not touch Event Tick, the MultiBoxTraceForObjects node,
or the Play Montage chain. Do not change any variable default.

Then compile the Blueprint and report: any compile errors or warnings, and the full
exec chain of Event AnyDamage from the event node onward.
```

**명령 16 — 디버그 도형 다시 끄기**

```
Two trace nodes are temporarily set to ForDuration for testing. Set both back to None.
Change ONLY the DrawDebugType pin on each - do not touch any other pin, node, or
variable.

1. In the EventGraph of /Game/Enemy/BP_Enemy:
     node K2Node_CallFunction_94 (MultiSphereTraceForObjects, inside Event Tick)
     set its DrawDebugType input pin from ForDuration to None

2. In the EventGraph of /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter:
     node K2Node_CallFunction_31 (MultiBoxTraceForObjects, inside Event Tick)
     set its DrawDebugType input pin from ForDuration to None

Leave DrawTime at 0.5 on both.

Do NOT remove any PrintString. The "EnemyHP: " node in BP_Enemy (K2Node_CallFunction_2)
and the "PlayerHP: " node in BP_ThirdPersonCharacter (K2Node_CallFunction_34) both stay -
they are permanent, not debug.

Do not touch the new Branch K2Node_IfThenElse_9 or the Equal(Object) node
K2Node_PromotableOperator_13 in BP_Enemy - those are the enemy-friendly-fire guard.

Then compile both Blueprints and report the DrawDebugType value on both nodes.
```

**옮기며 넣은 해석**

- 한글의 **"가벼운것들만 다하고"**를 나는 **"재검증이 필요 없거나 되읽기 한 번으로 끝나는 것"**으로 읽고 넷을 골랐다. `Sequence` 제거는 PIE가 필요해서 "중간"으로 분류했는데 사용자가 "이대로하자"로 포함시켰다.
- **`ApplyDamage`와 입력 셋까지 같이 옮긴 것** — 사용자가 넘긴 항목은 `K2Node_Self_1` 하나였다. 실제로 보니 `ApplyDamage` 자체가 `Event Tick` 체인에서 1750 떨어져 있어서 넷을 묶어 옮기는 것으로 넓혔고, **명령을 내기 전에 넓혔다는 사실을 밝히고 좁게 갈 선택지를 같이 제시했다.**
- **좌표 넷** — 한글 지시에 없는 숫자다. `Array Add`가 `(10620, 2450)`인 것을 기준으로 내가 정했다.
- **`(4000, 150, 90)`** — 새 적의 위치. 내가 정했다. `Enemy_Test` 옆 1.5m이고, 벽에 박히면 화면에서 바로 보인다는 전제로 골랐다.
- **적끼리 방지 `Branch`를 `Array Add` 다음에 넣은 것** — 사용자는 "막는다"만 골랐다. 앞이냐 뒤냐는 내가 정했고, **다른 적도 `HitActorsThisSwing`에 들어간다**는 부작용이 있다.
- **`PlayerHP:`를 임시가 아니라 영구로 넣은 것** — 사용자가 "추가할까?"라고 물었고 내가 영구를 권했다. 앞선 기록에서 임시로 넣었다 뺀 것을 되살린 것이다.
- **시험 2(관용 폭)를 합격 기준에서 뺀 것** — 사용자가 "비켜서면 걍 주먹 경로에 없어서 안맞는거 아님?"이라고 지적했고, 나는 그 지적이 맞다고 판단해 통과/실패 시험을 측정으로 바꿨다. 결과적으로 측정도 못 했다.

## Terminal 결과

### 원문 — English

**UE Terminal 자체의 출력은 이번 묶음에서 한 번도 들어오지 않았다.** 사용자가 붙여넣지 않았고, 나는 매번 MCP 읽기 호출과 UE 출력 로그로 실제 상태를 다시 확인했다. 아래는 **내가 받은 MCP 응답 원문**과 **UE 출력 로그 원문**이다.

**MCP 실패 응답 — 전문**

```
Unknown tool get_transform
```

```
Function "get_pin_value", input param "pin" is required by the function input schema Json, but is missing from the incoming function input params Json.
Function schema Json -
{"type":"object","properties":{"pin":{"title":"PinID","type":"object","properties":{"direction":{"type":"string","title":"EEdGraphPinDirection","enum":["EGPD_Input","EGPD_Output"]},"index_id":{"type":"integer"},"node":{"type":"object","title":"/Script/Engine.EdGraphNode","description":"Represents a reference to a UObject or UClass.","properties":{"refPath":{"type":"string","description":"The reference stored as a soft path string."}},"required":["refPath"]}},"required":["direction","index_id","node"]}},"required":["pin"]}
Function input params Json -
{"node":{"refPath":"/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter:EventGraph.K2Node_CallFunction_31"},"pin_name":"DrawDebugType"}
```

**MCP 연결이 끊겼다 붙은 흔적 — 에디터 재시작 직후 시스템 알림 전문**

```
The following MCP servers are still connecting — their tools (typically named mcp__<server>__*) are not yet available but will appear shortly:
unreal-mcp
```

**UE 출력 로그 — 적 둘 첫 PIE. `LogBlueprintUserMessages` 전부**

```
[2026.09.02-07.15.53:166][671]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143] EnemyHP: 66.0
[2026.09.02-07.15.53:178][672]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 66.0
[2026.09.02-07.15.53:639][706]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 56.0
[2026.09.02-07.15.57:465][ 50]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 22.0
[2026.09.02-07.16.02:302][419]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 0.0
[2026.09.02-07.16.04:774][664]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143] EnemyHP: 32.0
[2026.09.02-07.16.06:734][864]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143] EnemyHP: 0.0
```

**UE 출력 로그 — 적끼리 방지 후 PIE. `LogBlueprintUserMessages` 전부**

```
[2026.09.02-07.45.27:834][172]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 66.0
[2026.09.02-07.45.28:182][199]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 90.0
[2026.09.02-07.45.30:976][421]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143] EnemyHP: 66.0
[2026.09.02-07.45.33:592][652]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 32.0
[2026.09.02-07.45.39:358][101]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143] EnemyHP: 32.0
[2026.09.02-07.45.39:478][110]LogBlueprintUserMessages: [BP_ThirdPersonCharacter_C_0] PlayerHP: 80.0
[2026.09.02-07.45.46:111][638]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] EnemyHP: 0.0
[2026.09.02-07.45.47:973][789]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143] EnemyHP: 0.0
```

**저장이 안 된 것을 잡은 근거 — `git status`와 파일 mtime을 나란히 읽은 것. 세 번 찍었다**

```
Wed Sep  2 17:02:31     2026
 M Content/Enemy/BP_Enemy.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/A/IN/
---mtimes---
-rw-r--r-- 1 a0108 197609 396162 16:23:42 Content/Enemy/BP_Enemy.uasset
-rw-r--r-- 1 a0108 197609 834233 16:47:26 Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

```
Wed Sep  2 17:04:22     2026
 M Content/Enemy/BP_Enemy.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/A/IN/
---mtimes---
-rw-r--r-- 1 a0108 197609 396162 16:23:42 Content/Enemy/BP_Enemy.uasset
-rw-r--r-- 1 a0108 197609 834233 16:47:26 Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

```
Wed Sep  2 17:07:25     2026
 M Content/Enemy/BP_Enemy.uasset
 M Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
?? Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/A/IN/
---mtimes---
-rw-r--r-- 1 a0108 197609 395090 17:06:54 Content/Enemy/BP_Enemy.uasset
-rw-r--r-- 1 a0108 197609 834166 17:07:09 Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset
```

**정리 커밋 직후의 파일 크기 대조 — 노드 삭제가 실제로 반영됐는지 본 것**

```
Content/Enemy/BP_Enemy.uasset                                            HEAD=393241  NOW=389330
```

**새 적 인스턴스를 인스턴스에서 되읽은 응답**

```
{"FistRadius":15,"AttackRange":150,"AttackDamage":10,"AttackCooldown":1.5,"MaxHP":100,"SightRange":1200,"SightHalfAngle":60,"ThinkInterval":0.29999999999999999,"AttackMontage":{"refPath":"/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Enemy_Attack.AM_Enemy_Attack"},"bIsSwinging":false}
```

### 요약 — 한글

**애셋 단위로 바뀐 것 셋**

- `Content/Enemy/BP_Enemy.uasset` — `Sequence` 삭제, `ApplyDamage` 클러스터 넷 이동, `ReturnStepDistance` 삭제, 적끼리 방지 `Branch` + `Equal(Object)` 추가, `DrawDebugType` 왕복
- `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset` — `"PlayerHP: "` `PrintString` + `Append` + `ToString(Float)` 추가(영구), `DrawDebugType` 왕복
- `Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/A/IN/5FI6JSM02A316FCLSZ10WA.uasset` — 새 액터 `Enemy_Test2` (신규 파일)

**변수 단위**

- `BP_Enemy`에서 삭제 — `ReturnStepDistance`(Float, `300`). 변수 21개 → **20개**
- `BP_ThirdPersonCharacter` 변수 19개 그대로
- 튜닝 값 하나도 안 건드렸다 — `AttackRange 150`, `AttackDamage 10`, `AttackCooldown 1.5`, `ThinkInterval 0.3`, `FistRadius 15`, `MaxHP 100`, 플레이어 `AttackDamage 34`, `CurrentHP 100`

**노드 단위 — `BP_Enemy`에서 지운 것**

`K2Node_ExecutionSequence_0`(`Sequence`)

**노드 단위 — `BP_Enemy`에서 만든 것**

`K2Node_IfThenElse_9`(적끼리 방지 `Branch`), `K2Node_PromotableOperator_13`(`Equal(Object)`)

**노드 단위 — `BP_Enemy`에서 옮긴 것 (위치만, 배선 무변화)**

- `K2Node_CallFunction_49`(`ApplyDamage`) `(10080, 700)` → `(11100, 2450)`
- `K2Node_VariableGet_38`(`AttackDamage` 게터) `(9520, 700)` → `(10800, 2700)`
- `K2Node_CallFunction_48`(`GetController`) `(9800, 700)` → `(10800, 2820)`
- `K2Node_Self_1` `(0, 420)` → `(10800, 2940)`

**노드 단위 — `BP_ThirdPersonCharacter`에서 만든 것**

`K2Node_CallFunction_34`(`PrintString`), `K2Node_CommutativeAssociativeBinaryOperator_3`(`Append`, `A = "PlayerHP: "`), `K2Node_CallFunction_14`(`ToString(Float)`)

**배선 단위 — 적끼리 방지 전후**

```
전: K2Node_IfThenElse_8 True -> K2Node_CallArrayFunction_3 -> K2Node_CallFunction_49
후: K2Node_IfThenElse_8 True -> K2Node_CallArrayFunction_3 -> K2Node_IfThenElse_9
                                                               True  -> K2Node_CallFunction_49
                                                               False -> (비었음)
    K2Node_IfThenElse_9.Condition <- K2Node_PromotableOperator_13
      A <- K2Node_CallFunction_96 (BreakHitResult) 의 Hit Actor, 출력 index 9
      B <- K2Node_VariableGet_30 (PlayerRef 게터)
```

**배선 단위 — `Sequence` 제거 전후**

```
전: K2Node_CallFunction_46 -> K2Node_ExecutionSequence_0
                                Then 0 -> K2Node_PlayMontage_0
                                Then 1 -> K2Node_CallFunction_50 (Delay)
후: K2Node_CallFunction_46 -> K2Node_PlayMontage_0
                                then (출력 index 0) -> K2Node_CallFunction_50 (Delay)
```

**레벨 단위**

- `Enemy_Test2` 추가 — `BP_Enemy_C_UAID_9C6B005AF869E6FD02_1187686143`, 위치 `(4000, 150, 90)`, 회전 yaw `180`, 스케일 `(1,1,1)`
- 기존 `Enemy_Test`는 `(4000, 0, 90)` yaw `180`. 안 건드렸다

## 분석

### 무엇을 만들었나

**적끼리 방지 (`BP_Enemy`, `Event Tick`의 `ForEachLoop` 안)**

- `Array Add` 다음, `ApplyDamage` 앞에 `Branch` 하나
- 조건은 `Equal(Object)` — `BreakHitResult`의 `Hit Actor`(출력 index 9)와 `PlayerRef` 게터를 비교
- `False` 핀은 비워뒀다. 플레이어가 아니면 아무것도 안 한다
- **다른 적도 `HitActorsThisSwing`에는 들어간다.** 검사를 `Array Add` 뒤에 뒀기 때문이다

**플레이어 HP 로그 (`BP_ThirdPersonCharacter`, `Event AnyDamage`)**

- `Set CurrentHP`(`K2Node_VariableSet_0`) → `PrintString` → `Branch`(`K2Node_IfThenElse_8`)
- `InString = Append("PlayerHP: ", ToString(Float)(Set CurrentHP의 Output_Get))`
- `TextColor` 파랑 `(0, 0.66, 1)`, `Duration 2.0`, `Key None`. 적의 `EnemyHP:`와 같은 계열
- **회복 경로(`K2Node_VariableSet_2`, `(200, 2200)`)는 안 건드렸다**

**레벨 (`Lvl_ThirdPerson`)**

- `Enemy_Test2` 하나 추가. `(4000, 150, 90)`, yaw `180`
- 인스턴스에서 되읽은 값이 CDO와 전부 일치 — `FistRadius 15`, `AttackRange 150`, `AttackDamage 10`, `AttackCooldown 1.5`, `MaxHP 100`, `SightRange 1200`, `SightHalfAngle 60`, `ThinkInterval 0.3`, `AttackMontage = AM_Enemy_Attack`, `bIsSwinging false`

**정리 넷**

- `Sequence` 삭제 — `Play Montage`의 `then`(출력 index 0)이 즉시 실행 핀이라 불필요했다
- `ApplyDamage` 클러스터 넷을 옛 `Think` 줄(`y=700`)에서 `Event Tick` 줄(`y=2450`~`2940`)로 이동
- `ReturnStepDistance`(`300`) 삭제 — 그래프 둘 다에서 참조 0개
- 배치 인스턴스 `FistRadius`에 `reset_properties` 시도

**임시로 켰다 끈 것**

- `BP_Enemy` `K2Node_CallFunction_94`와 `BP_ThirdPersonCharacter` `K2Node_CallFunction_31`의 `DrawDebugType`을 `None → ForDuration → None`. `DrawTime`은 `0.5` 그대로

### 기술적으로 맞게 짚은 부분

**사용자의 반박을 받아들여 시험 자체를 바꾼 것.**
합격 기준 2("비켜서면 안 맞는다")에 대해 사용자가 "걍 주먹 경로에 없어서 안맞는거 아님?"이라고 물었다. **맞는 지적이다.** 구현이 "이전 주먹 위치 → 현재 위치를 반지름 15로 훑는다"이므로 경로 밖이면 안 맞는 것이 구현의 정의다. 그 시험은 "구현이 구현대로 동작한다"만 확인한다. 그래서 통과/실패 시험을 **관용 폭 측정**으로 바꿨다 — 플레이어 캡슐 반지름 `35` + `FistRadius 15` = **주먹 중심선에서 `50cm`**가 예상 경계다. 사양 단계에서 그 문장을 그대로 통과시킨 것이 안일했고, 사용자가 그걸 잡았다.

**노드를 옮기라는 요청을 받고 실제 좌표를 먼저 읽은 것.**
넘김 항목은 "`K2Node_Self_1`을 `ApplyDamage` 근처로"였다. 읽어보니 `ApplyDamage` 자체가 `(10080, 700)`이고 그 exec 이웃인 `Array Add`는 `(10620, 2450)`이었다 — **`ApplyDamage`가 이미 자기 체인에서 1750 떨어져 있었다.** `Self_1`만 옮겼으면 넷이 통째로 엉뚱한 자리에 남는다. 범위를 넓히면서 **넓힌다는 사실과 좁게 갈 선택지를 명령 전에 밝혔다.**

**적끼리 방지 검사를 `Array Add` 뒤에 둔 것.**
앞에 두면 다른 적이 `HitActorsThisSwing`에 안 들어가서 창이 열린 12프레임 내내 매 프레임 다시 `Contains` → `NOT` → `Equal` 을 돈다. 뒤에 두면 한 번 걸러진 뒤 그 스윙 동안 `Contains`에서 바로 빠진다. **변수 이름과 의미가 약간 어긋나는 대가로 반복 연산을 없앴고, 그 트레이드오프를 명령에 적어뒀다.**

**`Get Player Character`를 새로 부르지 않고 `PlayerRef` 게터를 재사용한 것.**
`PlayerRef`는 `BeginPlay`에서 세팅되고 `NO_PLAYER` 갈래에서 재획득된다. `Event Tick` 안에서 `Get Player Character`를 부르면 프로젝트 규칙(Tick에서 조회 금지)에 정면으로 걸린다. 게터는 이미 다섯 노드가 읽고 있어서 노드가 늘지도 않았다.

**타입 걱정을 명령에 적어두고 틀린 것.**
`Hit Actor`는 `Actor`, `PlayerRef`는 `Character`라 비교가 될지 확인하지 못해 "안 되면 말씀해달라"고 적었다. 실제로는 `Equal(Object)`가 두 입력을 `Object Reference`로 승격시켜 문제없이 붙었다. **확인 안 한 것을 확인 안 했다고 적은 것이 맞았고, 결과는 기우였다.**

**`EnemyHP:` 하나로 적 둘 시험을 설계한 것.**
`Hit:` `PrintString`을 다시 심을 뻔했는데, `EnemyHP:`가 이미 남아 있고 로그에 **액터 인스턴스 이름이 붙는다는 것**을 떠올렸다. 서로 다른 두 액터 ID로 `EnemyHP: 66.0`이 나오면 그게 곧 증거다. **그래프를 한 번도 안 건드리고 시험 하나를 설계했다.**

**감소량으로 가해자를 특정한 것.**
`66 → 56`은 감소량이 정확히 `10`이고, 칼은 `34`다. `10`은 적의 `AttackDamage`다. `bIgnoreSelf`가 자기 자신만 막으므로 **`Enemy_Test2`가 `Enemy_Test`를 때린 것**으로 특정됐다. 화면을 안 보고 로그 한 줄에서 나온 결론이다.

**저장 여부를 mtime으로 검증한 것.**
사용자가 "저장했어"라고 두 번 말했고 두 번 다 mtime이 안 바뀌어 있었다. `git status`만 봤으면 ` M`이 떠 있으니 "저장됐구나"로 넘어갔을 것이다 — **그 ` M`은 그 전 저장의 흔적이었다.** 현재 시각과 mtime을 나란히 찍는 습관이 이걸 잡았다.

**커밋 전에 디버그를 되돌린 것.**
사용자가 "커밋하고"라고 했을 때 `DrawDebugType`이 `ForDuration`이었다. 그대로 커밋하면 앞선 세션에서 명시적으로 정한 "디버그 표시 제거"와 어긋난 상태가 이력에 박힌다. **한 줄로 이유를 대고 되돌린 뒤 커밋했다.**

### 확인한 것 / 확인 못 한 것

**확인한 것**

- **`Sequence` 제거** — `Sequence` 검색 결과 0개. `Play Montage`의 `execute ← StopMovement`, `then`(index 0) `→ Delay`. 나머지 출력 다섯 핀의 연결이 그대로인 것도 하나씩
- **노드 넷 이동** — `get_node_infos`로 네 좌표가 지정한 값과 일치. `ApplyDamage`의 입력 다섯이 전부 같은 노드에서 오는 것도 확인
- **`ReturnStepDistance` 삭제** — 변수 21개 → 20개. `ReturnDelay`·`ReturnSightRange`는 남아 있음
- **적끼리 방지 배선** — `K2Node_IfThenElse_9`의 `execute ← Array Add`, `Condition ← Equal(Object)`, `then → ApplyDamage`, `else` 비었음. `Equal(Object)`의 `A ← BreakHitResult`의 index 9, `B ← PlayerRef` 게터
- **`PlayerHP:` 배선** — `Set CurrentHP → PrintString → Branch`. `InString ← Append("PlayerHP: ", ToString(Float))`. `EventGraph`의 `PrintString`이 이것 하나뿐
- **`Enemy_Test2` 배치** — 위치·회전이 지정한 대로. **인스턴스에서 되읽은 값 아홉 개가 CDO와 전부 일치.** 인스턴스 함정 안 걸림
- **한 스윙에 적 둘 다 맞는다** — 두 액터가 각각 `100 → 66`, 34씩. 12ms 간격
- **적끼리 안 때린다** — 방지 후 PIE에서 `EnemyHP` 감소량이 전부 `34` 또는 클램프된 `32`. **`10`짜리가 하나도 없다**
- **적이 플레이어는 여전히 때린다** — `PlayerHP: 100 → 90 → 80`, 10씩
- **`DrawDebugType`이 양쪽 다 `None`으로 돌아온 것** — `get_pin_value`로 각각
- **저장이 안 됐던 것과 결국 된 것** — mtime `16:23:42`/`16:47:26`이 두 번 그대로였고, Compile 후 저장하니 `17:06:54`/`17:07:09`으로 갱신됐다. 크기도 `396162 → 395090`, `834233 → 834166`으로 줄었다
- **최종 `git status` 비었음** — 커밋 `0f7850d` 이후

**확인 못 한 것**

- **`MultiTrace`가 한 프레임에 `OutHits`를 둘 반환하는 경로.** 적 둘을 한 스윙에 때렸지만 프레임 번호가 `671`과 `672`로 **연속 두 프레임**이었다. 한 `Tick`의 `ForEachLoop`가 히트 둘을 처리한 적은 이번에도 없다. 게임플레이 요구는 충족되지만 그 코드 경로는 여전히 미검증이다
- **적끼리 방지가 "걸러진" 것인지 "안 닿은" 것인지.** `10`짜리 감소가 없다는 것은 **없음의 증거**다. 적들의 주먹이 실제로 서로 닿았는데 `Branch`가 막은 것인지, 애초에 안 닿은 것인지 구분할 수단이 없다
- **관용 폭.** 20초 동안 적 둘이 붙었는데 플레이어가 두 번 맞았다. **`ATTACK` 표시를 지운 상태라 몇 번 공격했는지(분모)를 셀 수 없어** 비율을 못 낸다. 사용자가 화면에서 초록/빨간 구체 경계를 봤는지도 답을 못 받았다
- **`Sequence` 제거 후 공격 주기가 여전히 1.5초인지.** `ATTACK` 표시가 없어 로그로 못 쟀다. 사용자가 PIE 화면에서 "괜찮은 것 같다"고 본 것이 유일한 근거다
- **배치 인스턴스 `FistRadius`의 덮어쓰기 유무.** `reset_properties` 후 `__ExternalActors__` 파일이 안 바뀌었고, Details 패널에 되돌리기 화살표도 없었다. **화살표 없음은 "덮어쓰기가 없다"와 "덮어쓰기 값이 CDO와 같아서 안 뜬다" 양쪽에 다 맞는다.** UE가 어느 쪽으로 동작하는지 확인하지 않았다
- **컴파일 경고 원문.** 명령 여덟 개 전부 "compile and report any errors or warnings"를 요구했는데 이번 묶음에서는 터미널 출력이 **한 번도** 안 들어왔다
- **`BP_Door`·`BP_ThirdPersonHUD`·`BP_ThirdPersonPlayerController`가 앞선 커밋에서 왜 dirty였는지.** 이번 묶음에서는 안 나타났다

### 남는 리스크

- **MCP로 핀 값을 바꾸면 패키지가 dirty로 안 잡히는 것으로 보인다.** `Save All`을 두 번 눌러도 mtime이 안 바뀌었고, 블루프린트를 열어 **Compile을 누른 뒤** 저장해야 디스크에 갔다. **"저장했다"는 말과 실제 저장이 어긋나는 경로이고, 이번에 실제로 두 번 어긋났다.** 원인은 추정이고 확인한 것은 mtime뿐이다
- **`reset_properties`도 같은 모양이다.** 값이 바뀌었다는 표시는 없고 파일도 안 바뀌었다. 이 툴이 실제로 뭘 했는지 모른다
- **다른 적이 `HitActorsThisSwing`에 들어간다.** 변수 이름은 "이번 스윙에 때린 액터"인데 실제로는 "이번 스윙에 훑힌 액터"다. 다음에 이 배열을 다른 용도로 쓰면 어긋난다
- **적끼리 방지가 `PlayerRef`에 의존한다.** `PlayerRef`가 `None`이면 아무도 안 맞는다. `Think`의 `NO_PLAYER` 갈래가 재획득하지만, 그 사이 스윙은 무해하게 지나간다. 안전한 실패 방향이긴 하다
- **적이 둘이 되면서 서로 밀친다.** `CHASE`에서 둘 다 `SimpleMoveToActor`로 플레이어에게 붙으면 캡슐끼리 밀린다. 이번 PIE에서 문제는 안 났지만 관찰은 안 했다
- **레벨에 적이 둘로 고정됐다.** 사용자가 남기기로 정했다. 앞으로 모든 PIE가 적 둘 기준이 된다
- **`Event Tick`이 이제 적 둘에서 돈다.** 창이 닫혀 있으면 `Branch` 하나지만 인스턴스 수만큼 는다
- **`PlayerHP:`가 영구 노드가 됐다.** 릴리스를 생각하면 지워야 하는데, 이 프로젝트는 연습장이라 지금은 이득이 크다
- **`FistRadius 15`는 여전히 근거 없는 값이다.** 관용 폭을 못 재서 이번에도 확정 못 했다
- **`AM_Player_Attack`(9~14)과 `AM_Enemy_Attack`(9~16)의 노티파이 구간이 다르다.** 같은 `MM_Attack_01`인데 갈려 있다

### 총평

두 묶음이었고 둘 다 됐다. 정리 넷은 전부 반영됐고, 검증 둘 중 하나(적 둘 동시 타격)는 통과, 다른 하나(관용 폭)는 **재지 못했다.**

가장 값이 컸던 것은 **사용자가 합격 기준을 반박한 것**이다. "비켜서면 걍 주먹 경로에 없어서 안맞는거 아님?" — 이 한 문장이 두 세션 동안 "미확인"으로 끌고 온 항목이 애초에 확인할 값이 없는 항목이었다는 것을 드러냈다. 내가 사양에 쓴 문장이고, 두 번의 검증에서 "정황만 있다"고 성실하게 보고했지만, **그 문장 자체가 정보를 못 내는 형태라는 것은 못 봤다.** 형식(`PIE에서 ___하면 ___가 된다`)을 지켰다고 내용이 좋은 것은 아니다.

두 번째는 **적을 하나 더 놓자마자 첫 PIE에서 버그가 나온 것**이다. "적이 다른 적을 때릴 수 있다"는 심문 6번에서 사용자가 (a)를 고르며 받아들인 리스크였고, 나는 앞선 기록의 `남는 리스크`에 적어두고 "두 번째가 실제로 생겼을 때 뽑는다"로 넘겼다. **두 번째가 생기자 20초 만에 나왔다.** 미리 만들지 않은 판단은 맞았고, 리스크로 적어둔 판단도 맞았다.

세 번째는 **저장이다.** 이 세션에서 "저장했다"는 말이 실제 저장과 어긋난 것이 두 번이다. `git status`의 ` M`은 **지금 저장됐다는 뜻이 아니라 마지막 저장이 커밋과 다르다는 뜻**이고, 그 둘을 구분하려면 mtime을 봐야 한다. 그리고 이 프로젝트에서는 **MCP로 그래프를 고친 뒤 Compile을 눌러야 저장이 걸린다.** 이건 다음 세션이 반드시 알아야 하는 절차다.

부수적으로 **인스턴스 함정의 조건이 좁혀졌다.** `Enemy_Test2`는 변수를 만든 뒤에 배치해서 CDO 값을 그대로 받았다. 함정은 "변수 생성 시점에 이미 배치돼 있던 액터"에만 걸린다.

## AI의 제안

> **`Hit:` `PrintString`을 복구할 필요가 없습니다** — `EnemyHP:` 표시가 아직 살아 있고, 로그에 액터 인스턴스 이름이 붙습니다. 적 둘을 한 스윙에 때리면 같은 프레임에 **서로 다른 두 액터 ID로 `EnemyHP: 66.0`이 두 줄** 나옵니다

얻는 것 — 그래프를 안 건드리고 시험을 설계했다. 넣었다 빼는 왕복 두 번이 사라졌다. 잃는 것 — 판정 기준을 "같은 프레임 두 줄"로 잡았는데 실제로는 연속 두 프레임이 나와서, 통과인지 아닌지를 다시 해석해야 했다.

> **`PlayerHP`는 영구로 넣는 것을 권합니다.** 임시로 넣었다 뺀 게 이번 세션에만 한 번이고, 방금 또 없어서 못 봤습니다. **두 번 빼먹었으면 그건 임시가 아닙니다**

얻는 것 — 전투를 건드릴 때마다 같은 노드를 다시 심는 왕복이 사라진다. 적/플레이어 로그가 대칭이 된다. 잃는 것 — 릴리스 때 지워야 할 노드가 하나 는다.

> **`DrawDebugType`을 먼저 되돌리고 커밋하겠습니다** — 지금 커밋하면 아까 "디버그 표시 제거"로 정한 것과 어긋난 상태가 들어갑니다

얻는 것 — 이력에 남는 상태가 결정과 일치한다. 잃는 것 — 커밋이 명령 하나만큼 늦어진다.

> **각 블루프린트를 열고 Compile 버튼을 누른 다음 `Ctrl+S`.** 컴파일하면 dirty로 잡힙니다

얻는 것 — 두 번 실패한 저장이 됐다. mtime과 파일 크기 양쪽에서 확인됐다. 잃는 것 — 사용자가 손으로 두 번 더 눌러야 한다.

> **시험 C(관용 폭)는 접겠습니다.** 제대로 재려면 `ATTACK` 표시를 다시 심어야 해서 지금 할 일이 아닙니다. `FistRadius`를 실제로 튜닝할 때 같이 하는 게 낫습니다

얻는 것 — 반쪽짜리 측정을 "쟀다"고 기록하지 않는다. 잃는 것 — 세 세션 연속 미확인으로 남는다.

## 다음으로 넘김

**바로 이어서 할 것**

- 없음. `git status` 비었고 커밋 `0f7850d`까지 반영됐다

**결정 필요**

- **`FistRadius 15`가 적당한가.** 근거 없이 정한 값이고 세 세션째 그대로다. 관용 폭(플레이어 캡슐 반지름 `35` + `FistRadius`)이 지금 `50cm`다. 튜닝하려면 `ATTACK` 표시를 임시로 심어 분모를 세야 한다
- **`AM_Player_Attack`의 노티파이 구간을 9~16으로 맞출 것인가.** 지금 플레이어 9~14, 적 9~16. 같은 `MM_Attack_01`이다
- **적 상태 표시(`ATTACK`/`CHASE`/`RETURN`/`IDLE_HOME`/`IDLE_WAIT`/`NO_PLAYER`)를 다시 심을 것인가.** 관용 폭 측정과 공격 주기 측정 양쪽이 이걸 필요로 한다. 다시 심는 명령은 `2026-09-02-enemy-fist-trace.md`의 명령 8을 뒤집으면 된다
- **`HitActorsThisSwing`의 이름을 실제 의미에 맞출 것인가.** 지금 "훑힌 액터"인데 이름은 "때린 액터"다. **BP 변수 이름을 바꾸면 참조하던 다른 BP가 조용히 끊길 수 있다**
- **플레이어 `BeginPlay`에 `CurrentHP = MaxHP` 초기화를 넣을 것인가.** 적에는 있고 플레이어에는 없다. 지금은 기본값 `100`이 곧 시작 체력이라 동작에 문제는 없다

**확인 필요**

- **MCP로 그래프를 고친 뒤에는 Compile을 눌러야 저장이 걸린다.** 이번에 두 번 어긋났다. **`Save All`만으로는 안 된다.** 원인은 확인 못 했고 mtime 관측뿐이다
- **저장 여부는 `git status`가 아니라 파일 mtime으로 본다.** ` M`은 "마지막 저장이 커밋과 다르다"는 뜻이지 "방금 저장됐다"가 아니다
- **`MultiTrace`가 한 프레임에 히트 둘을 반환하는 경로.** 두 번 시도해 두 번 다 연속 프레임이었다. 억지로 만들려면 적 둘을 캡슐이 맞닿게(중심 간 `70cm`) 고정해야 한다
- **적끼리 방지가 실제로 막은 것인지.** 없음의 증거뿐이다. 확정하려면 방지 `Branch`의 `False` 핀에 임시 `PrintString`을 물리면 된다 — **한 줄이면 되고 이게 가장 싼 방법이다**
- **`Sequence` 제거 후 공격 주기.** 화면 인상만 있다
- **배치 인스턴스 `FistRadius`의 덮어쓰기 유무.** CDO를 다른 값으로 바꾸고 컴파일한 뒤 인스턴스를 읽으면 갈린다. **실제로 `FistRadius`를 튜닝할 때 자연히 드러난다**
- **컴파일 경고 원문을 UE Terminal이 어디에 뱉는지.** 여덟 번 요구해서 한 번도 못 받았다
- **적 둘이 서로 밀치는 동작.** 이번 PIE에서 문제는 안 났지만 관찰하지 않았다
- **`2026-09-01-enemy-hp-death.md`의 `확인 필요` 목록.** `arrange_nodes`, `EditorPerProjectUserSettings.ini` 저장 실패, `CaptureViewport`가 에디터 월드를 그리는 것 등이 그 파일에 그대로 있다

**접어둔 것**

- **Mixamo 등 외부 베기 애니메이션.** IK Rig도 IK Retargeter도 없고 MCP 툴셋에 리타깃 도구가 없다. 한 세션짜리 수작업
- **진짜 칼 메시 구하기.** 구하면 `BladeHalfLength`와 중심 오프셋을 손잡이 위로 옮겨 "칼날만" 판정이 된다
- **`Knife`와 `Key_Stage1`이 같은 `Cube` 메시라 색이 같은 것.** 머티리얼로 가를 수 있다
- **`heldTransform`의 회전·오프셋이 짝이라는 사실을 `DT_Items` 어디에도 안 적어뒀다.** 주석 칸이 없다
- **적 공격 이펙트·사운드.** 판정만 있다
- **`MM_Attack_02` / `MM_Attack_03` / `MM_ChargedAttack`.** 사용자가 "셋 다 칼이랑 관련없음"으로 확인했다
