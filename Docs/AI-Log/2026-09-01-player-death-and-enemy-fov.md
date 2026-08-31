# 2026-09-01

## 작업물

**플레이어 사망과 리스폰을 만들고, 적 AI에 시야각과 라인 오브 사이트를 붙여 벽 너머 감지를 닫았다** — 명령 72·75·77, 합격 기준 여덟 개를 전부 PIE 로그의 숫자로 통과시켰다.

**소요 시간**: 약 2시간 25분. 근거는 UE 로그와 파일시스템 시각이다. 앞 기록([2026-08-31-enemy-chase-return-fix.md](2026-08-31-enemy-chase-return-fix.md))의 정리가 끝난 `23:13 KST`부터, 마지막 PIE 판정이 `16:35:40 UTC`(= `01:35:40 KST`), 기록 착수가 `01:36 KST`다. **UE 로그는 UTC이고 파일시스템·git은 KST(+9)다** — 이번에도 확인됐다. `BP_Enemy` 저장이 로그에서 `15:58:24`인데 그때 쓰인 `.uasset`의 mtime이 `00:58:24`다. **날짜가 자정을 넘어간다** — 로그는 `2026.08.31`인데 파일시스템은 `2026-09-01`이다.

**두 덩어리로 나뉜다.** 앞쪽(72~74)은 플레이어 사망, 뒤쪽(75~78)은 적 시야각이다. **둘 다 인계 목록이 가리키던 `적의 HP·피격·사망`이 아니다** — 조사해보니 그건 플레이어 공격 수단이 없어 검증이 불가능했고, 순서를 바꿨다.

## 명령

### 한글

```
음 그대로 할까 고고
```

```
계속 작업할까 그럼
```

```
결과 확인
```

```
확인해봐
```

```
이거 리스폰하면 무조건 3인칭 그리고 죽은 시점에서 부활전까지 안움직여짐 그리고 슬롯도 전부 비어있는채로 부활함
```

```
물약 줍고 죽었을 때 다시 스폰되면 인벤토리 모두 비워져있었어 3인칭 부활은 내비두자
```

```
시야각이랑 라인오브사이트 저거 하고 커밋하고 정리할까
```

```
결과 확인
```

```
야 이거 감지 범위가 좀 줄어든거 같은데 확인좀
```

```
chase 가 한 100몇에서 뜨는거같은데? 확인좀
```

```
결과 확인
```

```
PIE 결과 이전 기준도 다 잘되는것같에 확인해바
```

```
저거 이상 없음 PIE로 순서대로 진행했을 때 문제 없음
```

이 밖에 선택지 질문 다섯 묶음에 답했다.

- 다음 작업 → `플레이어 사망·리스폰 (권장)`
- 리스폰 방식 → `RestartPlayer — 폰을 새로 스폰 (권장)` / 사망 연출 → `연출 없이 N초 뒤 리스폰 (권장)`
- 시야각 → `±60도 — 원뿔 120도 (권장)` / 작은 구형 → `항상 켜둔다 — 근접 전방위 (권장)` / LOS 범위 → `모든 감지에 (권장)`
- 복귀 중 원뿔 → `켜둔다 — 복귀 중에도 앞은 본다`

### English — MCP에 실제로 보낸 명령

**이번에도 AI가 MCP로 직접 보낸 쓰기 명령은 하나도 없다.** 쓰기는 전부 아래 영어 명령문을 사용자가 UE Terminal에 붙여서 실행했다. AI가 MCP를 직접 부른 것은 전부 읽기다.

**명령 72**

```
In /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter, make two changes and nothing else.

CHANGE 1 - add one variable.
Add a float member variable named RespawnDelay, default value 2.0, and make it
instance-editable (the eye icon on, so it can be tuned on the placed instance).
Add no other variable.

CHANGE 2 - extend the existing Event AnyDamage chain in the EventGraph.
Today that chain is exactly five nodes:
  Event AnyDamage -> Set CurrentHP = Clamp(CurrentHP - Damage, 0.0, MaxHP)
and the Set CurrentHP node's "then" execution pin is not connected to anything.

Rebuild it into this, keeping the existing Clamp / subtract / getter nodes:
  Event AnyDamage
    -> Branch  (Condition = CurrentHP > 0.0)
         False -> nothing
         True  -> Set CurrentHP = Clamp(CurrentHP - Damage, 0.0, MaxHP)   [the existing nodes]
                  -> Branch  (Condition = CurrentHP <= 0.0)
                       False -> nothing
                       True  -> DisableInput (target = self, PlayerController = GetPlayerController(0))
                                -> Delay (Duration = RespawnDelay)
                                -> DetachFromControllerPendingDestroy (target = self)
                                -> RestartPlayer (target = GetGameMode, NewPlayer = GetPlayerController(0))
                                -> DestroyActor (target = self)

The node order in the death branch is load-bearing - do not rearrange it:
  - DetachFromControllerPendingDestroy MUST run before RestartPlayer. Verified in
    Engine/Source/Runtime/Engine/Private/GameModeBase.cpp, AGameModeBase::RestartPlayerAtPlayerStart:
    if the controller still has a pawn it only copies that pawn's rotation and never
    spawns a new one.
  - Use GetPlayerController(0) from GameplayStatics for both the DisableInput and the
    RestartPlayer pins, NOT GetController(self). After the detach, GetController(self)
    returns null.
  - GetGameMode from GameplayStatics returns AGameModeBase*, and RestartPlayer is declared
    on AGameModeBase, so NO cast node is needed. Do not add one.
  - DestroyActor is last.

Change nothing else. Do not touch CurrentHP's default of 75, MaxHP's default of 100,
InventorySlots, SelectedSlot, InteractDistance, bIsFirstPerson, the HUD, BP_Enemy, or any
other graph in this Blueprint.

Then compile BP_ThirdPersonCharacter and save it. Then report:
  - the EventGraph node count before and after
  - the DSL of the Event AnyDamage chain after the change
  - whether RespawnDelay shows the instance-editable eye icon as ON in My Blueprint
  - any compile warning or error, quoted verbatim
```

**명령 75**

```
In /Game/Enemy/BP_Enemy, make two changes and nothing else.

CHANGE 1 - add one variable.
Add a float member variable named SightHalfAngle, default value 60.0, instance-editable
(eye icon on). This is the half-angle in DEGREES measured from the enemy's forward
vector, so 60.0 means a 120-degree cone. Add no other variable.

CHANGE 2 - replace the detection test in the Custom Event "Think".
Right now the detection test is this single condition:
    dist <= select(returning, GetReturnSightRange, GetSightRange)
where "dist" is the existing GetDistanceTo(self, PlayerRef) node and "returning" is the
existing AND of (now - LastSeenTime >= ReturnDelay) and (homeDist > HomeArriveRadius).

Replace that condition with:
    LineOfSightTo( GetController(self), PlayerRef )
    AND (
          dist <= GetReturnSightRange
          OR ( dist <= GetSightRange
               AND Acos(Degrees)( GetHorizontalDotProductTo(self, PlayerRef) ) <= GetSightHalfAngle )
        )

Node type_ids, all verified as pure (no exec pins):
  Controller|LineOfSightTo                   self:Controller, Other:Actor,
                                             ViewPoint = (0,0,0), bAlternateChecks = false
  Transformation|GetHorizontalDotProductTo   self:Actor, OtherActor:Actor
  Math|Trig|Acos(Degrees)                    A:double

Delete the Select node that picked between ReturnSightRange and SightRange - it now has
no consumer. Keep the GetReturnSightRange and GetSightRange getters; both are still used
above. Keep the "returning" AND node and its two comparisons untouched - the RETURN
branch still uses them.

CHANGE 2b - one more debug line, same style as the existing three.
Add a PrintString with Key "4_angle" printing ToString(Float) of the
Acos(Degrees)(GetHorizontalDotProductTo(...)) value, with bPrintToScreen true,
bPrintToLog true, the same color (R=0.0, G=0.66, B=1.0, A=1.0) and Duration 1.0.
Put it right after the existing "3_home" PrintString, before the detection Branch.

Change nothing else. Do not touch any existing default value (SightRange 1200,
ReturnSightRange 300, ReturnStepDistance 300, ReturnDelay 7, HomeArriveRadius 100,
ThinkInterval 0.3, AttackRange 150, AttackCooldown 1.5, AttackDamage 10), the CHASE
branch's SimpleMoveToActor, any StopMovement node, the RETURN branch's hop math, the
three existing PrintStrings, or EventBeginPlay.

Then compile BP_Enemy and save it. Then report:
  - the node count before and after
  - the complete DSL of the Think event after the change
  - whether SightHalfAngle shows the instance-editable eye icon as ON in My Blueprint
  - any compile warning or error, quoted verbatim
```

**명령 77**

```
In /Game/ThirdPerson/Lvl_ThirdPerson, find the actor labeled exactly "Enemy_Test"
(the BP_Enemy instance).

Its SightHalfAngle reads 0, but the class default on /Game/Enemy/BP_Enemy is 60.
The instance was placed in the level before that variable existed, so it carries a
stale per-instance override of 0. This makes the view-cone test "angle <= SightHalfAngle"
false for every angle, so the enemy only ever detects through the 300 uu proximity
sphere.

Reset that one property on the instance so the override is cleared and it inherits the
class default again - use ObjectTools.reset_properties on the actor with the property
list ["SightHalfAngle"]. Do not set it by hand to 60; clear the override.

Then save the level.

Then report, reading back FROM THE PLACED ACTOR Enemy_Test (not from the Blueprint class
default), all ten of these values so we can confirm nothing else drifted:
  SightHalfAngle, SightRange, ReturnSightRange, ReturnDelay, ReturnStepDistance,
  HomeArriveRadius, ThinkInterval, AttackRange, AttackCooldown, AttackDamage
and state whether reset_properties returned true.
```

**명령 73·74·76·78은 Terminal 명령이 아니다.** 넷 다 한글로 낸 PIE 플레이 절차다.

**옮기며 넣은 해석**

- **`RespawnDelay`라는 이름과 기본값 `2.0`.** 심문에서 "연출 없이 N초 뒤"라고만 물었고 2초는 AI가 제안했다
- **`DisableInput`을 넣는 것.** 사양의 심문에 없었다. 넣지 않으면 HP 0인 채로 2초 동안 뛰어다닐 수 있다
- **`Get Player Controller (0)`을 쓰는 것.** `GetController(self)`도 되지만 떼어낸 뒤 널이 되는 순서 함정을 아예 없애려고 골랐다
- **`SightHalfAngle`이라는 이름**과 **`4_angle` 디버그 줄을 추가하는 것.** 사양에 없다. 기준 1~3을 눈대중이 아니라 숫자로 판정하려고 넣었다
- **명령 76·78의 판정 기준값들** — `4_angle 60을 넘게 유지`, `2_dist 800쯤`, `문 뒤 500쯤`. 사양에 없고 AI가 계산해 낸 절차다

## Terminal 결과

### 원문 — English

**먼저 밝힌다 — UE Terminal이 화면에 뱉은 출력은 이 기록에 없다.** 사용자가 명령을 붙여 실행한 뒤 `결과 확인`이라고만 했고, AI는 Terminal 창을 볼 수단이 없다. 아래는 전부 **AI가 MCP로 직접 읽은 것**이다. **명령 72·75·77이 요구한 "node count before and after", "eye icon이 켜졌는지", "reset_properties가 true를 반환했는지"는 사용자가 옮겨 오지 않아 확보하지 못했다.**

**명령 72 이후 `Event AnyDamage` 사슬.** `get_connected_subgraph`로 노드와 핀 연결을 읽어 재구성했다.

```
Event AnyDamage (K2Node_Event_3)
  then -> IfThenElse_2 (Branch)      Condition <- Math|Float|float>float (GetCurrentHP, 0.0)
      else -> 연결 없음
      then -> VariableSet_0 (Set CurrentHP) <- Math|Float|Clamp(Float)
                                                 Value <- Math|Float|float-float (GetCurrentHP, Damage)
                                                 Min = 0.0
                                                 Max <- GetMaxHP
              then -> IfThenElse_8 (Branch)  Condition <- Math|Float|float<=float (GetCurrentHP, 0.0)
                  else -> 연결 없음
                  then -> CallFunction_45  Input|DisableInput
                                             self 미연결(= self)
                                             PlayerController <- CallFunction_46 Game|GetPlayerController (PlayerIndex 0)
                          then -> CallFunction_47  Utilities|FlowControl|Delay
                                                     Duration <- VariableGet_20 GetRespawnDelay
                                  then -> CallFunction_48  Pawn|DetachFromControllerPendingDestroy
                                                             self 미연결(= self)
                                          then -> CallFunction_49  Game|RestartPlayer
                                                                     self <- CallFunction_50 Game|GetGameMode
                                                                     NewPlayer <- CallFunction_51 Game|GetPlayerController (0)
                                                  then -> CallFunction_52  Actor|DestroyActor
                                                                             self 미연결(= self)
                                                          then -> 연결 없음
```

**명령 75 이후 `Think` 이벤트의 감지 조건.** `read_graph_dsl` 원문에서 발췌했다.

```
  (bind _playerref (Variables|Default|GetPlayerRef))
  (bind _self self)
  (bind _returnvalue (Transformation|GetHorizontalDotProductTo _self _playerref))
  (bind _returnvalue_1 (Math|Trig|Acos(Degrees) _returnvalue))
  ...
      (Development|PrintString (Utilities|String|ToString(Float) _returnvalue_1) true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 1.0 "4_angle")
      (if (and (Controller|LineOfSightTo (Pawn|GetController _self) _playerref) (or (<= _returnvalue_6 (Variables|Default|GetReturnSightRange)) (and (<= _returnvalue_6 (Variables|Default|GetSightRange)) (<= _returnvalue_1 (Variables|Default|GetSightHalfAngle)))))
```

`returning`은 `select`가 없어지면서 소비자가 하나로 줄어 인라인으로 렌더된다. 동작은 같다.

```
        (elif (and (>= (- _returnvalue_2 (Variables|Default|GetLastSeenTime)) (Variables|Default|GetReturnDelay)) (> _returnvalue_5 _homearriveradius))
```

**명령 72·75 이후의 클래스 기본값.**

```
BP_ThirdPersonCharacter:
{"RespawnDelay":2,"CurrentHP":75,"MaxHP":100,"InventorySlots":["None","None","None"],
 "SelectedSlot":1,"InteractDistance":800,"bIsFirstPerson":false}

BP_Enemy:
{"SightHalfAngle":60,"SightRange":1200,"ReturnSightRange":300,"ReturnStepDistance":300,
 "ReturnDelay":7,"HomeArriveRadius":100,"ThinkInterval":0.29999999999999999,
 "AttackRange":150,"AttackCooldown":1.5,"AttackDamage":10}
```

**명령 77 직전 — 배치된 `Enemy_Test`의 값. 이번 세션에서 가장 중요한 원문이다.**

```
{"SightHalfAngle":0,"SightRange":1200,"ReturnSightRange":300,"ReturnDelay":7,
 "ReturnStepDistance":300,"HomeArriveRadius":100,"ThinkInterval":0.29999999999999999,
 "AttackRange":150,"AttackCooldown":1.5,"AttackDamage":10}
```

**명령 77 직후 — 같은 액터.**

```
{"SightHalfAngle":60,"SightRange":1200,"ReturnSightRange":300,"ReturnDelay":7,
 "ReturnStepDistance":300,"HomeArriveRadius":100,"ThinkInterval":0.29999999999999999,
 "AttackRange":150,"AttackCooldown":1.5,"AttackDamage":10}
```

**플레이어 사망 PIE(15:10~15:11). `NO_PLAYER`가 이 프로젝트에서 처음 찍혔다.**

```
[2026.08.31-15.10.49:596][987]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.10.51:103][136]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.10.52:607][286]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.10.54:117][434]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.10.56:538][663]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.10.58:963][890]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.01:073][ 88]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.03:191][288]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.04:701][429]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.06:206][572]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] NO_PLAYER
[2026.08.31-15.11.19:574][847]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.21:380][ 19]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.23:494][220]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.25:298][395]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.27:106][575]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.28:610][726]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.30:116][876]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.31:617][ 24]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.33:429][199]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] ATTACK
[2026.08.31-15.11.34:933][343]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] NO_PLAYER
[2026.08.31-15.11.47:739][558]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
```

**PIE 중에 읽은 리스폰된 폰.** 액터 이름이 `_2`다 — 원본이 아니다.

```
/Game/ThirdPerson/UEDPIE_0_Lvl_ThirdPerson.Lvl_ThirdPerson:PersistentLevel.BP_ThirdPersonCharacter_C_2

{"CurrentHP":75,"MaxHP":100,"InventorySlots":["None","None","None"],"SelectedSlot":1,
 "RespawnDelay":2,"bIsFirstPerson":false}

{"location":{"x":158.90802277275625,"y":-719.67413418145838,"z":92.149996213039316},
 "rotation":{"pitch":0,"yaw":175.45001220703125,"roll":-0},"scale":{"x":1,"y":1,"z":1}}
```

**시야각 첫 PIE(16:13) — 실패한 판. `SightHalfAngle`이 0이라 원뿔이 안 열렸다.**

```
[2026.08.31-16.13.40:677][106]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 855.465698
[2026.08.31-16.13.40:677][106]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.250001
[2026.08.31-16.13.40:677][106]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1.526750
[2026.08.31-16.13.40:677][106]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
[2026.08.31-16.13.41:285][158]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 532.053955
[2026.08.31-16.13.41:285][158]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.250001
[2026.08.31-16.13.41:285][158]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1.546996
[2026.08.31-16.13.41:285][158]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
[2026.08.31-16.13.42:504][264]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 322.826294
[2026.08.31-16.13.42:504][264]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.250001
[2026.08.31-16.13.42:504][264]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1.432175
[2026.08.31-16.13.42:504][264]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
[2026.08.31-16.13.42:805][290]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 296.161774
[2026.08.31-16.13.42:805][290]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.250001
[2026.08.31-16.13.42:805][290]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1.405835
[2026.08.31-16.13.42:805][290]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
```

**시야각 마지막 PIE(16:26·16:35) — 합격 판정의 근거 전부.**

기준 1. `SightRange 1200` 바로 아래에서 전환된다.

```
[2026.08.31-16.26.22:311][372]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1383.392090
[2026.08.31-16.26.22:311][372]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.25
[2026.08.31-16.26.22:311][372]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.115350
[2026.08.31-16.26.22:311][372]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
[2026.08.31-16.26.22:618][398]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1199.352417
[2026.08.31-16.26.22:618][398]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.25
[2026.08.31-16.26.22:618][398]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.544286
[2026.08.31-16.26.22:618][398]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
```

기준 4. 정면 5.89도, 거리 847.6인데 안 보인다. 벽이다.

```
[2026.08.31-16.26.31:466][159]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 775.743225
[2026.08.31-16.26.31:466][159]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1534.540885
[2026.08.31-16.26.31:466][159]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 6.692576
[2026.08.31-16.26.31:466][159]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_WAIT
[2026.08.31-16.26.32:084][214]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 847.622498
[2026.08.31-16.26.32:084][214]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1534.540885
[2026.08.31-16.26.32:084][214]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 5.892155
[2026.08.31-16.26.32:084][214]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_WAIT
[2026.08.31-16.26.34:805][458]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 847.622498
[2026.08.31-16.26.34:805][458]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1534.540885
[2026.08.31-16.26.34:805][458]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 5.892155
[2026.08.31-16.26.34:805][458]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
```

기준 2. 각도 179도, 거리 716 → 359, 전부 `IDLE_HOME`. 열 표본 중 넷을 발췌했다.

```
[2026.08.31-16.35.37:126][583]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 716.047058
[2026.08.31-16.35.37:126][583]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.25
[2026.08.31-16.35.37:126][583]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 179.649455
[2026.08.31-16.35.37:126][583]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
[2026.08.31-16.35.38:377][655]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 551.517517
[2026.08.31-16.35.38:377][655]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.25
[2026.08.31-16.35.38:377][655]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 179.903087
[2026.08.31-16.35.38:377][655]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
[2026.08.31-16.35.39:627][727]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 375.960815
[2026.08.31-16.35.39:627][727]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.25
[2026.08.31-16.35.39:627][727]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 178.899793
[2026.08.31-16.35.39:627][727]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
```

기준 3. `ReturnSightRange 300`을 사이에 두고 갈린다.

```
[2026.08.31-16.35.40:252][763]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 329.787415
[2026.08.31-16.35.40:252][763]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.25
[2026.08.31-16.35.40:252][763]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 178.458073
[2026.08.31-16.35.40:252][763]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
[2026.08.31-16.35.40:565][781]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 281.863220
[2026.08.31-16.35.40:565][781]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.25
[2026.08.31-16.35.40:565][781]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 177.846322
[2026.08.31-16.35.40:565][781]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
```

**진단 중에 직접 잰 것.** `2_dist 2644` 시점의 두 액터 위치와 그 사이를 쏜 트레이스다.

```
적       {"location":{"x":3999.9999958206236,"y":4.8578302258572847e-07,"z":92.150000700630201},
          "rotation":{"pitch":0,"yaw":180,"roll":-0}}
플레이어  {"location":{"x":1423.6138839610494,"y":-596.90510656394417,"z":92.150000046629714},
          "rotation":{"pitch":0,"yaw":-124.32501220703124,"roll":0}}

trace_world (4000, 0, 156.15) → (1423.6, -596.9, 92.15)   =  2053.574951171875
```

거리 2644.6과 각도 13.04도를 손으로 계산했더니 `2_dist 2644.628662` · `4_angle 13.044317`과 일치했다. **디버그 출력이 맞다는 것을 이렇게 확인했다.**

**엔진 소스 원문.** 명령 72의 순서 근거다.

```cpp
// Engine/Source/Runtime/Engine/Private/GameModeBase.cpp
// AGameModeBase::RestartPlayerAtPlayerStart
	if (NewPlayer->GetPawn() != nullptr)
	{
		// If we have an existing pawn, just use it's rotation
		SpawnRotation = NewPlayer->GetPawn()->GetActorRotation();
	}
	else if (GetDefaultPawnClassForController(NewPlayer) != nullptr)
	{
		// Try to create a pawn to use of the default class for this player
		APawn* NewPawn = SpawnDefaultPawnFor(NewPlayer, StartSpot);
		if (IsValid(NewPawn))
		{
			NewPlayer->SetPawn(NewPawn);
		}
	}
```

```cpp
// Engine/Source/Runtime/Engine/Classes/GameFramework/GameModeBase.h:434
	UFUNCTION(BlueprintCallable, Category=Game)
	ENGINE_API virtual void RestartPlayer(AController* NewPlayer);

// Engine/Source/Runtime/Engine/Classes/GameFramework/Pawn.h:468
	UFUNCTION(BlueprintCallable, Category=Pawn, meta=(Keywords = "Delete"))
	ENGINE_API virtual void DetachFromControllerPendingDestroy();

// Engine/Source/Runtime/Engine/Classes/GameFramework/Actor.h:1435
	UFUNCTION(BlueprintCallable, Category="Input")
	ENGINE_API virtual void DisableInput(class APlayerController* PlayerController);

// Engine/Source/Runtime/Engine/Classes/Kismet/GameplayStatics.h:364
	UFUNCTION(BlueprintPure, Category="Game", meta=(WorldContext="WorldContextObject"))
	static ENGINE_API class AGameModeBase* GetGameMode(const UObject* WorldContextObject);
```

명령 75의 근거다.

```cpp
// Engine/Source/Runtime/Engine/Private/Actor.cpp
float AActor::GetHorizontalDotProductTo(const AActor* OtherActor) const
{
	if (OtherActor)
	{
		FVector Dir = GetActorForwardVector();
		FVector Offset = OtherActor->GetActorLocation() - GetActorLocation();
		Offset = Offset.GetSafeNormal2D();
		return FVector::DotProduct(Dir, Offset);
	}
	return -2.0;
}
```

```cpp
// Engine/Source/Runtime/Engine/Classes/GameFramework/Controller.h:177
	UFUNCTION(BlueprintCallable, Category=Controller)
	ENGINE_API virtual bool LineOfSightTo(const class AActor* Other, FVector ViewPoint = FVector(ForceInit), bool bAlternateChecks = false) const;
```

```cpp
// Engine/Source/Runtime/AIModule/Private/AIController.cpp
// AAIController::LineOfSightTo
	FVector TargetLocation = Other->GetTargetLocation(GetPawn());

	FCollisionQueryParams CollisionParams(SCENE_QUERY_STAT(LineOfSight), true, this->GetPawn());
	CollisionParams.AddIgnoredActor(Other);

	bool bHit = GetWorld()->LineTraceTestByChannel(ViewPoint, TargetLocation, ECC_Visibility, CollisionParams);
	if (!bHit)
	{
		return true;
	}
```

**MCP 어긋남 원문.** 이번 세션에 새로 잡은 것들이다.

```
[2026.08.31-14.57.18:909][ 62]LogScript: Warning: The node could not be created / |GetCurrentHP does not exist
[2026.08.31-15.01.53:744][107]LogScript: Warning: GetObjectProperties on '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.Default__BP_ThirdPersonCharacter_C' (BP_ThirdPersonCharacter_C): the following properties could not be read: NewVariables
[2026.08.31-14.44.22:065][583]LogScript: Warning: GetObjectProperties on '/Game/ThirdPerson/Blueprints/BP_ThirdPersonGameMode.Default__BP_ThirdPersonGameMode_C' (BP_ThirdPersonGameMode_C): the following properties could not be read: bDelayedStart
[2026.08.31-15.29.41:132][187]LogScript: Warning: The node could not be created / AI|Navigation|LineOfSightTo does not exist
[2026.08.31-15.29.41:132][187]LogScript: Warning: 'NoneType' object has no attribute 'get_node_title'
```

**`BP_ThirdPersonCharacter` 컴파일에 딸려 두 애셋이 재직렬화됐다.** 인계 목록에 `BP_Door.uasset의 재직렬화`로 세 세션째 올라와 있던 현상의 원문을 이번에 잡았다.

```
[2026.08.31-15.10.28:989][279]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.08.31-15.10.36:504][821]LogFileHelpers: Saving Package: /Game/ThirdPerson/Blueprints/BP_ThirdPersonHUD
[2026.08.31-15.10.36:538][821]LogFileHelpers: Saving Package: /Game/Enemy/BP_Enemy
```

**우리 작업과 무관한 것 둘.** PIE 종료 무렵의 것과 에디터 설정 파일 쓰기 충돌이다.

```
[2026.08.31-15.17.55:427][705]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
[2026.08.31-16.03.23:201][517]LogFileManager: Error: Error moving file 'D:/20260827/MCP1/Saved/EditorPerProjectUserSettingsB0697BB441F2D93F2AAEB99E71E2A0CA.tmp' to 'D:/20260827/MCP1/Saved/Config/WindowsEditor/EditorPerProjectUserSettings.ini'.
```

### 요약 — 한글

**애셋 셋이 바뀌었다.** `BP_ThirdPersonCharacter` · `BP_Enemy` · 그리고 재직렬화된 `BP_ThirdPersonHUD`.

**명령 72 — 플레이어 사망 사슬**

- `RespawnDelay` float `2.0` 신규. `BP_ThirdPersonCharacter`의 열두 번째 변수
- `Event AnyDamage` 앞에 `Branch (CurrentHP > 0)`을 넣어 죽은 뒤 데미지를 막았다
- `Set CurrentHP` 뒤에 `Branch (CurrentHP <= 0)`을 달고 그 `True`에
  `DisableInput` → `Delay(RespawnDelay)` → `DetachFromControllerPendingDestroy` →
  `RestartPlayer` → `DestroyActor`를 이었다
- `Set CurrentHP`의 비어 있던 `then` 핀이 처음으로 연결됐다

**명령 75 — 시야각과 LOS**

- `SightHalfAngle` float `60.0` 신규. `BP_Enemy`의 여덟 번째 변수
- 감지 조건에서 `select(returning, ReturnSightRange, SightRange)` 노드를 제거했다
- 조건이 `LineOfSightTo AND (dist <= 300 OR (dist <= 1200 AND angle <= 60))`이 됐다
- `Transformation|GetHorizontalDotProductTo` + `Math|Trig|Acos(Degrees)` + `Controller|LineOfSightTo` 셋 추가
- `4_angle` 디버그 줄 추가. `PrintString`이 9개에서 10개로

**명령 77 — 인스턴스 오버라이드 리셋**

- 배치된 `Enemy_Test`의 `SightHalfAngle`이 `0`이던 것을 `reset_properties`로 걷어냈다
- **`git status`에 외부 액터 파일이 안 나온다.** 델타가 사라져 커밋 시점과 바이트까지 같아졌다

**안 바꾼 것** — `CurrentHP 75` · `MaxHP 100` · `InventorySlots` · `SelectedSlot` · `InteractDistance 800` · `bIsFirstPerson`, `BP_Enemy`의 기존 값 아홉 전부, `CHASE`의 `SimpleMoveToActor`, `StopMovement` 셋, `RETURN`의 홉 수식과 `AcceptanceRadius 0.0`, `EventBeginPlay`, HUD 그래프.

## 분석

### 무엇을 만들었나

**`BP_ThirdPersonCharacter` — 변수 하나와 노드 사슬 하나**

```
RespawnDelay   float   2.0   인스턴스 편집(확인 못 함)
```

```
Event AnyDamage
  → Branch (CurrentHP > 0.0)
      False → 끝
      True  → Set CurrentHP = Clamp(CurrentHP − Damage, 0.0, MaxHP)     [기존]
              → Branch (CurrentHP <= 0.0)
                  False → 끝
                  True  → DisableInput (self, GetPlayerController(0))
                          → Delay (RespawnDelay = 2.0)
                          → DetachFromControllerPendingDestroy (self)
                          → RestartPlayer (GetGameMode, GetPlayerController(0))
                          → DestroyActor (self)
```

**`BP_Enemy` — 변수 하나와 조건식 교체**

```
SightHalfAngle   float   60.0   인스턴스 편집(확인 못 함).  정면 기준 반각(도)
```

```
seen = LineOfSightTo(GetController(self), PlayerRef)
       AND ( dist <= ReturnSightRange(300)
             OR ( dist <= SightRange(1200)
                  AND Acos(Degrees)(GetHorizontalDotProductTo(self, PlayerRef)) <= SightHalfAngle(60) ) )
```

디버그 표시가 넷이 됐다.

```
1_state   ATTACK / CHASE / RETURN / IDLE_HOME / IDLE_WAIT / NO_PLAYER
2_dist    플레이어까지 거리
3_home    집까지 거리
4_angle   플레이어가 정면에서 벗어난 각도(도)      ← 신규
```

**레벨 — `Enemy_Test`의 `SightHalfAngle` 오버라이드 제거.** 배치는 안 건드렸다.

**실효 감지 범위가 이렇게 바뀌었다.**

| 상황 | 전 | 후 |
|---|---|---|
| 정면 원뿔(±60°), 벽 없음 | 1200 | 1200 |
| 원뿔 밖 | 1200 | 300 |
| 벽 너머 | 1200 | 0 |

### 기술적으로 맞게 짚은 부분

**인계 목록을 그대로 따르지 않은 것.** 인계는 `적의 HP·피격·사망`을 가리키고 있었다. 조사해보니 `IA_Attack`이 없고 플레이어 변수 열하나에 공격 관련이 하나도 없다. **그걸 만들면 "PIE에서 적을 때리면 ___가 된다"를 쓸 수가 없다.** 합격 기준을 못 쓰는 작업은 시작하지 않는다는 것이 이 프로젝트의 규칙이라, 순서를 바꾸고 그 이유를 먼저 말했다. **인계 기록은 지도지 명령이 아니다.**

**플레이어 사망에서 만든 것이 거의 없다는 것을 먼저 확인한 것.** `CurrentHP`·`MaxHP`·`Event AnyDamage`·HUD의 HP 바·HUD의 재캐시 분기·적의 `NO_PLAYER` 분기가 전부 이미 있었다. 조사를 안 했으면 HP 바 위젯을 새로 만들거나 사망 상태 변수를 새로 팠을 것이다. **실제로 새로 만든 것은 변수 하나와 노드 여섯이다.**

**`bIsDead` 불리언을 안 만든 것.** 죽은 뒤 계속 들어오는 데미지가 `RestartPlayer`를 여러 번 예약하는 것을 막아야 했는데, 새 상태 변수 대신 **데미지 처리 자체를 `CurrentHP > 0`으로 가드**해서 `CurrentHP`가 상태 역할을 하게 했다. 로그를 보면 8대째에 죽고도 9대째가 들어오는데 아무 일도 안 일어난다. 결정 사다리 1번이 실제로 값을 냈다.

**`RestartPlayer`의 본문을 읽고 나서 명령을 쓴 것.** 짐작으로 `Delay → RestartPlayer`만 이었으면 **아무 일도 안 일어났을 것이다.** 컨트롤러가 폰을 들고 있으면 새 폰을 안 만든다는 것이 소스에만 있다. 그걸 읽었기에 `DetachFromControllerPendingDestroy`가 먼저라는 순서가 나왔고, 명령문에 그 근거를 파일·함수명까지 적어 보냈다.

**`GetController(self)` 대신 `GetPlayerController(0)`을 쓴 것.** 둘 다 되지만 앞엣것은 떼어낸 뒤 널이 되어 순서에 의존한다. **순서 의존을 하나 줄이는 쪽을 골랐다.**

**`GetHorizontalDotProductTo`를 찾은 것.** 시야각은 보통 `GetActorForwardVector` + 빼기 + `Normalize` + `Dot` 네 노드로 짠다. `find_node_types`로 훑다가 액터에 이미 있는 것을 찾았고, 구현을 읽어 **Z를 버린다는 것**까지 확인했다. 결정 사다리 5번 — 노드 하나로 됐다.

**`LineOfSightTo`를 직접 짜지 않은 것.** `LineTraceByChannel`로 짜면 시작점(눈높이)·채널·무시 액터·머리와 옆면 보정을 다 정해야 한다. `AAIController`가 그걸 이미 다 한다. 구현을 읽고 **눈높이·`ECC_Visibility`·자기와 대상 무시·머리와 옆 4점 재시도**를 확인한 뒤 골랐다. 결정 사다리 3번.

**`PawnSensing` / `AIPerception`을 안 쓴 것.** 컴포넌트와 이벤트 흐름을 새로 들이는 대신 조건식 세 줄로 끝냈다. 지금 요구가 그 이상을 정당화하지 않는다.

**로그로 진단한 것, 두 번.** 사용자가 `감지 범위가 좀 줄어든거 같은데`라고 짚었을 때 첫 응답은 **틀린 방향이었다** — 그때 플레이어가 벽 뒤에 있어서 "벽이 막는 게 정상"이라고 설명했다. 거리가 2644라 어차피 1200 밖이었다는 것을 놓쳤다. 사용자가 `chase 가 한 100몇에서 뜨는거같은데`로 다시 짚어준 뒤에야 전환 순간의 값을 뽑았고, `296.161774`가 `ReturnSightRange 300` 바로 아래라는 것에서 원뿔이 죽어 있다는 결론이 나왔다.

**가설을 세우고 틀렸을 때 무엇이 보일지를 먼저 말한 것.** `SightHalfAngle이 0일 것이다. 틀렸다면 60으로 읽힐 것이고 그러면 범인은 LineOfSightTo다`라고 적고 나서 읽었다. 0이었다.

**리셋을 손으로 60을 넣는 것보다 우선한 것.** 명령 66의 기록에 `인스턴스 값을 클래스 기본값과 같게 맞추자 오버라이드가 걷혔다`고 적혀 있었지만, `reset_properties`가 그 일을 하라고 있는 도구다. 결과로 `git status`에 외부 액터 파일이 아예 안 나왔다.

**디버그 줄을 하나 더 넣은 것.** `4_angle`이 없었으면 기준 1~3을 "정면인 것 같다"로 판정했을 것이다. 실제 판정은 `179.649455`, `0.544286` 같은 숫자로 했다.

### 확인한 것 / 확인 못 한 것

**확인한 것**

- **명령 72의 사슬 전체.** `get_connected_subgraph`로 노드와 핀 연결을 하나씩 읽었다. `DetachFromControllerPendingDestroy`(48)가 `RestartPlayer`(49) 앞이고, 양쪽 컨트롤러가 `GetPlayerController(0)`이고, `RestartPlayer`의 `self`가 `GetGameMode`에 **캐스트 없이** 물려 있고, `DestroyActor`가 맨 끝이며 두 `Branch`의 `else`가 비어 있다
- **명령 75의 조건식 전체.** `read_graph_dsl`로 읽었다. `select` 노드가 사라졌고 `4_angle`이 `3_home` 뒤에 들어갔다
- **`returning`이 인라인으로 바뀐 것이 표기 변화일 뿐이라는 것.** `select`가 소비자 하나를 잃어서 DSL 렌더링이 달라졌다. 식은 같다
- **두 블루프린트의 클래스 기본값 전부.** 새 값 둘(`RespawnDelay 2.0`, `SightHalfAngle 60.0`)과 안 건드린 값 전부
- **`Enemy_Test`의 `SightHalfAngle`이 리셋 전 `0`, 리셋 후 `60`.** 나머지 아홉은 양쪽 다 동일
- **컴파일 에러가 없다는 것.** `LogBlueprint: Compiling Blueprint` 다섯 번 모두
- **디스크에 실제로 썼다는 것.** `Saving Package` 로그와 `.uasset` mtime
- **플레이어 사망 기준 1.** 8대째 + `RespawnDelay 2.0`이 폰 파괴 창 안. 두 주기 다
- **플레이어 사망 기준 2.** 리스폰된 폰 `BP_ThirdPersonCharacter_C_2`에서 `CurrentHP 75` · `MaxHP 100` 실측
- **플레이어 사망 기준 4.** `NO_PLAYER` → `ATTACK`/`CHASE` 재획득 두 번
- **시야각 기준 1·2·3·4 전부.** 위 `Terminal 결과`의 숫자들
- **디버그 출력이 맞다는 것.** 두 액터 위치를 읽어 거리와 각도를 손으로 계산했더니 `2_dist`·`4_angle`과 소수점까지 일치했다
- **`git status`가 셋뿐이라는 것.** 외부 액터 파일은 안 나온다

**확인 못 한 것**

- **`RespawnDelay`와 `SightHalfAngle`의 인스턴스 편집 표시.** **AI가 읽을 수단이 없다.** `set_variable_instance_editable`은 있는데 되읽는 툴이 없고, `NewVariables`를 읽으려는 시도가 로그에 남아 있으며 실패했다. My Blueprint 패널의 눈 아이콘을 봐야 한다
- **Terminal이 화면에 뱉은 출력 전부.** 명령 72·75·77이 요구한 변경 전후 노드 수, 눈 아이콘 여부, `reset_properties`의 반환값을 **하나도 확보하지 못했다**
- **플레이어 사망 기준 3.** 사용자 육안이 유일한 근거다. 로그에 인벤토리가 안 남는다
- **1인칭으로 죽으면 3인칭으로 부활하는 것.** 사용자 육안. `bIsFirstPerson`이 클래스 기본값이라 그럴 것으로 보지만 소스로 확인하지는 않았다
- **`DisableInput`이 Enhanced Input 매핑까지 막는지.** PIE에서 안 움직이는 것만 봤다
- **HUD의 `CachedCharacter` 재획득이 실제로 일어났는지.** 그래프에 분기가 있는 것과 HP 바가 계속 그려지는 것만 봤다
- **`BP_ThirdPersonHUD`와 `BP_Enemy`의 재직렬화가 내용을 안 바꿨는지.** `.uasset`이 바이너리라 diff를 못 읽는다. `BP_ThirdPersonHUD`는 크기가 `355267 → 355267`로 같았다
- **`BP_Enemy`가 왜 `BP_ThirdPersonCharacter` 컴파일에 딸려 dirty가 됐는지.** `BP_ThirdPersonHUD`는 설명된다 — `CastToBP_ThirdPersonCharacter`를 하고 getter 넷을 부른다. `BP_Enemy`는 `PlayerRef`에 `GetPlayerCharacter(0)`을 캐스트 없이 넣으므로 타입이 `BP_ThirdPersonCharacter`가 아니다. **참조 사슬이 안 보인다**
- **`LogCrowdFollowing: Unable to find RecastNavMesh instance` 경고의 원인.** 지난 세션부터 이월
- **첫 진단에서 설명 못 했던 표본** `2_dist 906.889160` · `4_angle 11.115741` · `IDLE_WAIT`. 나중에 `SightHalfAngle 0`으로 설명됐다 — 원뿔이 죽어 있었고 906은 300 밖이다. **당시에는 두 액터 위치를 몰라 판단을 못 했다**

### 남는 리스크

- **`LineOfSightTo`가 `Think`마다 무조건 실행된다.** 블루프린트의 `AND`는 단락 평가를 안 한다. 호출당 최대 3회 트레이스, 초당 약 10회. 적 하나면 무시할 수준이다
- **`bIsFirstPerson`이 리스폰 때 초기화된다.** 1인칭으로 죽으면 3인칭으로 부활한다. **사용자가 `내비두자`로 정했다**
- **리스폰 지점에 적이 있을 수 있다.** 적이 1번 방까지 쫓아온 상태로 죽으면 `PlayerStart` 근처에서 바로 다시 맞는다
- **2초 동안 화면에 아무 표시가 없다.** 입력만 막힌 채 서 있는다
- **`RETURN` 분기가 아직 래턴트다.** 홉 하나(약 6.4초) 동안 `Think`가 멈춰서 그동안 시야각도 LOS도 판정되지 않는다. **시야각 기준 2를 처음 볼 때 이것 때문에 헛돌았다** — 뒤로 도는 구간이 통째로 홉 안에 들어가 "안 쫓아온 것"이 아니라 "아무 판정도 안 한 것"이었다. 적이 집에 선 상태에서 다시 재서 통과시켰다
- **`bOrientRotationToMovement`가 켜져 있어 한 번 들키면 시야각이 사실상 안 걸린다.** 추격 중 적의 정면이 늘 플레이어를 향한다. 의도한 동작이다
- **`GetHorizontalDotProductTo`가 높이차를 무시한다.** 지금 레벨이 평평해서 문제가 없다
- **`NO_PLAYER` 분기에 `StopMovement`가 없다.** 지금은 바로 재획득돼서 문제가 안 된다
- **디버그 표시가 넷으로 늘었다.** `PrintString` 10개 + `ToString(Float)` 3개
- **`BP_ThirdPersonCharacter`에 저장 안 된 컴파일이 남아 있다.** 세 번 짚었는데 mtime이 `00:01:37`에서 안 움직였다. 눈 아이콘을 켰다면 그 변경이 디스크에 없다
- **`BP_Enemy`에 변수를 추가할 때마다 `Enemy_Test`가 `0`을 물고 온다.** 두 번 연속 걸렸다

### 총평

**요청은 다 채웠다.** 합격 기준 여덟(사망 넷, 시야각 넷)을 전부 통과시켰고, 그중 여섯은 로그와 실측의 숫자로, 둘은 사용자 육안으로 닫았다.

**이번 세션의 실질적 난이도는 "무엇을 먼저 만들 것인가"와 "왜 안 되는가" 둘이었다.**

앞엣것은 인계 기록이 가리키는 곳과 실제로 만들 수 있는 것이 달랐던 문제다. `적의 HP·피격·사망`은 조건이 하나 안 갖춰져 있었고, 그걸 조사 없이 시작했으면 합격 기준을 못 쓰는 작업을 절반쯤 만들고 나서 알았을 것이다. **`Input/Actions/`를 한 번 훑는 것으로 갈렸다.**

뒤엣것은 같은 함정에 두 번째로 걸린 것이다. **명령 66이 이미 겪었고 사양에 적어뒀는데도 못 막았다.** 적어둔 규칙이 `적을 새로 배치할 때는 변수를 다 만든 뒤에 놓는다`였는데, **적은 이미 놓여 있으므로 그 규칙은 미래의 배치에만 적용된다.** 규칙이 실제 상황을 안 덮고 있었다. 이번에 `변수를 추가하는 명령에 리셋을 같이 넣는다`로 고쳐 적었다.

**틀린 진단을 한 번 했다.** 사용자가 감지 범위를 짚었을 때 벽을 원인으로 지목했는데, 그때 거리가 1200 밖이라 애초에 감지될 상황이 아니었다. 트레이스까지 쏴서 `2053.574951`이라는 숫자를 얻었지만 **맞는 측정으로 틀린 결론을 뒷받침한 것**이다. 사용자가 `chase 가 한 100몇에서 뜨는거같은데`라고 한 번 더 짚어주지 않았으면 그대로 넘어갔다.

**두 번 다 사용자의 관찰이 먼저였다.** `감지 범위가 좀 줄어든거 같은데`와 `리턴하면 리턴한 방향에서 다시 문쪽 안바라보는거 같은데`(앞 세션). 로그는 그 관찰이 어디서 오는지 설명했을 뿐이고, 어느 쪽도 AI가 먼저 못 봤다.

**엔진 소스가 두 번 결정적이었다.** `RestartPlayerAtPlayerStart`의 폰 분기와 `GetHorizontalDotProductTo`의 구현. 앞엣것은 안 읽었으면 동작 안 하는 사슬을 만들었을 것이고, 뒤엣것은 안 찾았으면 노드 넷을 손으로 짰을 것이다.

## AI의 제안

> **인계 기록은 `적의 HP·피격·사망`을 가리키고 있지만, 조사해보니 그건 플레이어 공격 수단이 없어 PIE로 검증할 수가 없다.**

사용자가 `계속 작업할까 그럼`이라고만 했고 무엇을 할지는 AI가 조사해서 갈랐다. 얻는 것은 합격 기준을 못 쓰는 작업을 시작하지 않는 것, 잃는 것은 인계 순서가 한 칸 밀리는 것이다.

> **`bIsDead` 불리언이 필요 없다.** 데미지 처리 자체를 `CurrentHP > 0`으로 가드한다. `CurrentHP`가 곧 상태다 — 결정 사다리 1번.

사용자가 상태 변수를 묻지 않았다. 얻는 것은 새 변수를 안 만드는 것과 사양의 무상태 규칙 유지, 잃는 것은 없다.

> **`DisableInput`을 넣는 것.** 넣지 않으면 HP 0인 채로 2초 동안 뛰어다닐 수 있다.

심문 항목에 없었다. 얻는 것은 죽은 뒤 조작이 막히는 것, 잃는 것은 노드 둘과 "연출 없이"라는 결정에 살짝 어긋나는 것이다. **결과적으로 PIE에서 동작이 확인됐다.**

> **짧은 홉은 기각한다. 대신 `Simple Move To Actor`가 있다.** (앞 세션의 판단을 이번에도 유지)

`CHASE`를 그대로 뒀다. 얻는 것은 이미 통과한 기준을 안 흔드는 것.

> **`Transformation|GetHorizontalDotProductTo`가 정확히 시야각 판정이다** — 결정 사다리 5번.

사용자는 `시야각이랑 라인오브사이트`라고만 했고 어떻게 잴지는 AI가 정했다. 얻는 것은 노드 넷 대신 둘, 잃는 것은 높이차를 무시한다는 것(지금 레벨에서는 무해).

> **`4_angle` 디버그 줄을 추가하는 것.**

사양에 없다. 얻는 것은 기준 1~3을 숫자로 판정할 수 있게 된 것, 잃는 것은 그래프에 비계가 셋 더 늘어난 것이다. **이것이 없었으면 `SightHalfAngle 0`을 못 찾았을 것이다.**

> **`SightHalfAngle`이 0일 것이다. 틀렸다면 60으로 읽힐 것이고 그러면 범인은 `LineOfSightTo`다.**

사용자가 `확인좀`이라고만 했다. 얻는 것은 한 번의 읽기로 원인이 갈린 것, 잃는 것은 없다.

> **`BP_Enemy`에 변수를 추가하는 명령에는 배치된 `Enemy_Test`의 그 변수를 `reset_properties`로 리셋하는 단계를 반드시 같이 넣는다.**

같은 함정에 두 번 걸린 뒤 AI가 규칙을 고쳐 적자고 꺼냈다. 얻는 것은 세 번째를 막는 것, 잃는 것은 명령이 한 단계 길어지는 것이다.

## 다음으로 넘김

**바로 이어서 할 것**

- **`Ctrl+Shift+S`(Save All).** `BP_ThirdPersonCharacter.uasset`의 mtime이 `00:01:37`에서 안 움직였는데 그 뒤 컴파일이 두 번 있었다. **눈 아이콘을 켰다면 그 변경이 디스크에 없다.** 세션 중 세 번 짚었고 아직 안 됐다
- **`RespawnDelay`와 `SightHalfAngle`의 인스턴스 편집 표시 확인.** My Blueprint 패널의 눈 아이콘. **AI가 읽을 수단이 없다.** `BP_Enemy`의 앞선 변수 넷도 같은 상태로 이월돼 있다 — 합쳐서 여섯 개다
- **플레이어 공격 수단.** 적 HP·피격·사망으로 가려면 이게 먼저다. `IA_Attack` 입력 액션과 매핑, 공격 몽타주(`MM_Attack_01`로 새로 만들어야 한다 — 지금은 애님 시퀀스뿐), 타격 판정. **맨손으로 갈지 칼을 먼저 넣을지를 정해야 한다.** 칼은 카메라 B안(팔을 시야로)과 엮여 있다

**결정 필요**

- **맨손 공격인가 칼인가.** 위 참조
- **`RETURN` 분기도 비래턴트로 바꿀 것인가.** 지금 복귀 중 감지 주기가 홉 하나(약 6.4초)다. `SimpleMoveToLocation`으로 바꾸면 0.3초가 되지만 짧은 홉 구조의 존재 이유가 없어지고 복귀 사양 기준 2·3의 동작이 바뀐다
- **복귀 속도를 되돌릴 것인가.** 초당 45다. `AcceptanceRadius`를 0 → 30으로 바꾸고 PIE로 재보는 것이 유일한 방법이다. **앞 세션에 `그대로두자`로 정했으므로 거슬릴 때만 다시 꺼낸다**
- **디버그 표시 제거 시점.** `PrintString` 10개 + `ToString(Float)` 3개, 노드 넷이 빠진다. 적 HP·피격·사망까지 끝난 뒤가 자연스럽다
- **칸막이 `SM_Cube2`를 `Divider_L`로 리네임할 것인가.** 짝이 `SM_Cube2` / `Divider_R`로 어긋나 있다

**확인 필요**

- **`BP_Enemy`가 왜 `BP_ThirdPersonCharacter` 컴파일에 딸려 dirty가 되는지.** `BP_ThirdPersonHUD`는 설명되는데 이건 참조 사슬이 안 보인다
- **재직렬화된 `.uasset` 둘의 내용이 실제로 안 바뀌었는지.** 바이너리라 못 읽는다
- **`LogCrowdFollowing: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance`.** PIE 종료 무렵마다 나온다
- **`read_graph_dsl`과 `write_graph_dsl`의 id 체계가 다른 이유.** 이번 세션에 `|GetCurrentHP does not exist`가 추가됐다. 누적 세 종류다
- **`find_node_types`와 `get_node_type_pins`의 type_id 표기가 다른 이유.** `SimpleMovetoActor` / `SimpleMoveToActor`
- **복귀가 초당 45로 느려진 진짜 원인.** `AcceptanceRadius 0`이 목표점 정확 도달을 요구한다는 가설만 있다
- **`DisableInput`이 Enhanced Input 매핑까지 막는지**
- **HUD의 `CachedCharacter` 재획득이 실제로 일어나는지**
- **2번 방의 조명.** `DirectionalLight`·`SkyLight` 외에 아무것도 없다
- **`bCanEverTick`이 명령 56 직후 `false`로 읽혔던 이유**
- **`trace_world`가 방향에 따라 같은 솔리드를 놓치는 이유**
- **`show navigation`이 PIE에서 안 먹는 이유.** 에디터 뷰포트의 `P`로 우회했다
- **두 신규 외부 액터 패키지의 정체와 `__ExternalObjects__` 파일의 정체**
- **`Lvl_ArenaShooter`의 WorldSettings가 `BP_ShooterGameMode`를 가리키는지.** `.umap`이 바이너리라 못 읽었다
- **`HandGrip_R` 소켓의 위치·각도.** 방향이 있는 메시(칼)가 오면 드러난다

**접어둔 것**

- **카메라 작업.** 셋으로 갈렸다
  - **A — 원본 ICI 구조(`캡슐 → Camera → SkeletalMesh`)로 교체.** 팔만 있는 스켈레탈 메시가 프로젝트에 없어 지금 그대로는 못 한다
  - **B — 지금 구조를 두고 팔을 시야로 올린다.** `Variant_Shooter/Anims/ABP_FP_Weapon` + `Ctrl_HandAdjusment`. 무기용이라 맨손·칼에 맞는지는 열어봐야 안다
  - **C — 전환 스냅 완화만.** 요 보간 또는 `SetViewTargetWithBlend`. 2026-08-27부터 이월
  - **칼 직전에 B로 가는 것을 권했고 사용자가 적 AI를 먼저 하기로 정했다**
- **1인칭으로 죽으면 3인칭으로 부활하는 것.** 사용자가 `내비두자`로 정했다. 고치려면 죽기 전 `bIsFirstPerson`을 PlayerController나 GameInstance에 넘겨야 하는데 지금 구조에 그 자리가 없다
- **30초 갇힘 사망.** 적 HP·피격·사망을 만들 때 같이 한다
- **사망 시 아이템 드롭.** `BP_ItemPickup`과 `IA_DropItem`이 있어 만들 수는 있다
- **게임오버 화면 · 사망 카운트 · 체크포인트**
- **적 체력바 위젯 / 순찰 / EQS / 여러 적의 회피 / 적 종류별 DataTable**
- **소리 감지 · 여러 적의 정보 공유 · "뭔가 봤다" 중간 경계 상태**
- **AnimNotify로 타격 창 열기.** 무기가 생길 때. 지금은 데미지가 애니메이션의 타격 순간보다 먼저 들어간다
- **`BP_ShooterNPC` · `ST_Shooter` · EQS 3개 · StateTree 태스크 6개.** 안 쓰기로 했지만 지우지 않는다
- **`--append-system-prompt`가 저장소에 없다.** `Editor Preferences → General → Terminal → Startup Commands`의 사용자 설정이라 다른 환경에서는 다시 넣어야 한다. 원문은 `Docs/AI-Log/2026-08-28-inventory-item-data.md`의 `명령` 칸에 있다
- **`BP_Door.uasset`의 재직렬화.** 이번에 원인의 절반이 잡혔다 — 참조하는 블루프린트를 컴파일하면 딸려 dirty가 된다
- **문간 위 `X 1800..1900, Z 200..400`의 열린 홈.** 관통은 아니다
- **열린 문짝 20cm가 문간 위로 삐져나온다.** 문짝 220, 문간 200
- **`ForLoop.FirstIndex`가 빈 값인 이유.** 동작에 지장이 없다
- **`SP` 스태미나.** 원본에 있고 MCP1에 없다. `06-플레이어-UI.md:54` 참조
- **슬롯 2칸 vs 3칸.** 원본은 2칸, MCP1은 3칸이다. 의도한 차이인지 안 정했다
- **미사용 애셋 정리.** 2026-08-30에 **남기기로** 정했다
- **`MoveComponentTo`의 `Stop`·`Return` 핀.** 연타로는 문제가 안 났다
