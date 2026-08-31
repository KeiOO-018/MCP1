# 2026-08-31

## 작업물

**적 AI가 추격 중에는 아무것도 재평가하지 못하던 것과, 복귀해도 집에 도착 판정이 안 나던 것 두 개를 고치고, 복귀 사양의 합격 기준 다섯과 새로 세운 기준 넷을 전부 PIE로 통과시켰다** — 명령 68·70, 커밋 없음(정리 시점에 한 번).

**소요 시간**: 약 1시간 40분. 근거는 UE 로그와 파일시스템 시각이다. 에디터는 `[12.59.55]LogEOSSDK`의 `Time: 1683.177246`(에디터 기동 후 경과 초)로 역산해 `12:31:52` UTC에 떴고, 첫 PIE의 첫 `IDLE_HOME`이 `12:41:58` UTC, 마지막 PIE가 `14:00:55` UTC, 기록 착수가 `23:13:20` KST다. **UE 로그는 UTC이고 파일시스템·git은 KST(+9)다** — 이번 세션에서도 다시 확인됐다. `LogFileHelpers: Saving Package: /Game/Enemy/BP_Enemy`가 로그에서 `13.52.31`인데 그때 저장된 `BP_Enemy.uasset`의 mtime이 `22:52:31`로 정확히 9시간 차다. 그래서 실제 구간은 `21:35 ~ 23:13 KST`.

**Terminal 명령은 둘뿐이다**(68·70). 나머지 시간은 전부 조사와 PIE 검증에 썼다. 이 세션은 만든 것보다 **읽어서 알아낸 것**이 많다.

## 명령

### 한글

```
작업 준비
```

```
68 고고
```

```
PIE 결과 이상 없음
```

```
이거 나를 계속 쫒아와 문 사이로 다시 닫고 있지 않으면 계속 쫒아오고 문을 닫고 나면 제대로 되돌아가는걸 확인해 이거 확인좀
```

```
고친다
```

```
결과 확인
```

```
PIE 결과 이상 없음 4번까지했어
```

```
했는데 아 이게 리턴하면 리턴한 방향에서 다시 문쪽 안바라보는거 같은데 이거 확인하는거임?
```

```
안바라봄 내가 눈으로 봤으 그거 로그확인해바
```

```
결과 확인
```

```
지금 봐봐 리턴 상태인데 IDLE_HOME 이 내눈엔 안보였는데 확인해바
```

```
아 아니다 이거 시간 지나면 되네
```

```
이게 내가 리턴상태인데 도착지점 즈음에 좀더 기다렸다가 홈으로 바뀌는데
```

```
그대로두자
```

```
지금 그럼 다음 작업하기 전에 지금까지했던 것들 정리할까
```

이 밖에 선택지 질문 둘에 답했다. 첫 질문 묶음의 답은 `거리만 유지 — 문은 물리적 장벽뿐 (권장)` / `그 자리에 즉시 선다 (권장)`, 정리 시점의 답은 `남긴 채 정리한다 (권장)` / `AI-Log 새 기록, 사양 파일 갱신, 이전 기록의 인계 정리, 커밋`이다.

### English — MCP에 실제로 보낸 명령

**이번 세션에 AI가 MCP로 직접 보낸 쓰기 명령은 하나도 없다.** 쓰기는 전부 아래 영어 명령문을 사용자가 UE Terminal에 붙여서 실행했다. AI가 MCP를 직접 부른 것은 전부 읽기다 — `list_toolsets` · `describe_toolset` · `read_graph_dsl` · `find_nodes` · `find_node_types` · `get_node_type_pins` · `list_graphs` · `get_default_object` · `get_properties` · `get_actor_transform` · `find_actors` · `get_current_level` · `IsPIERunning` · `GetLogEntries`.

**명령 68**

```
In /Game/Enemy/BP_Enemy, edit the EventGraph's Custom Event "Think".
Make exactly two changes and nothing else.

CHANGE 1 - the CHASE branch.
Right now the CHASE branch is:
  PrintString "CHASE"
    -> AI MoveTo (self, Goal Actor = PlayerRef, Acceptance Radius = AttackRange - 20.0)
         OnSuccess -> Delay(ThinkInterval) -> Think
         OnFail    -> Delay(ThinkInterval) -> Think
The latent AI MoveTo holds its execution pin for the whole pursuit, so Think never runs
again while the enemy is chasing. Replace it with a non-latent move:
  PrintString "CHASE"
    -> SimpleMoveToActor   (type_id "AI|Navigation|SimpleMoveToActor")
         Controller = GetController(self)
         Goal       = PlayerRef
    -> Delay (Duration = ThinkInterval)
    -> Think
Delete the AI MoveTo node, delete the second duplicate Delay + Think pair (the two
former OnSuccess / OnFail chains collapse into one), and delete the
"AttackRange - 20.0" subtract node if nothing else uses it. Keep the GetAttackRange
getter - the ATTACK test still uses it.

CHANGE 2 - stop the pawn on the three branches that issue no move.
SimpleMoveToActor is not latent and sets goal actor observation, so the pawn keeps
walking and repathing toward the player until something stops it. Insert a StopMovement
node (type_id "AI|Navigation|StopMovement", self = GetController(self)) as the first
node after the PrintString of each of these three branches:
  - ATTACK    - between PrintString "ATTACK" and PlayAnimMontage
  - IDLE_WAIT - between PrintString "IDLE_WAIT" and its Delay
  - IDLE_HOME - between PrintString "IDLE_HOME" and SetActorRotation
Do NOT add StopMovement to the RETURN branch; it issues its own AI MoveTo.
Do NOT add StopMovement to the NO_PLAYER branch.

Change nothing else. Do not touch any variable, any default value, any PrintString,
the RETURN branch's hop math, or the EventBeginPlay event.

Then compile BP_Enemy and save it. Then report:
  - the node count before and after
  - the complete DSL of the Think event after the change
  - whether write_graph_dsl created any empty event stub
  - any compile warning or error, quoted verbatim
```

**명령 70**

```
In /Game/Enemy/BP_Enemy, edit the EventGraph's Custom Event "Think".
Make exactly one change and nothing else.

In the RETURN branch there is an AI MoveTo node whose Acceptance Radius pin is wired to
the HomeArriveRadius variable getter. Break that wire and set the Acceptance Radius pin
to the literal value 0.0 instead.

Reason, for your reference only - do not change anything else based on it: AI MoveTo's
internal reach test is AcceptanceRadius + GoalRadius + AgentRadius * 1.1. With
AcceptanceRadius = HomeArriveRadius = 100 and the pawn's CapsuleRadius = 35, AI MoveTo
declares arrival at 138.5 uu from home and returns success without moving, while the
Blueprint's own test (homeDist <= HomeArriveRadius, i.e. 100) still says "not home".
The enemy gets stuck in that 100..138.5 band and loops RETURN forever. Passing 0.0 makes
AI MoveTo stop at 38.5 uu, safely inside the Blueprint's 100.

Keep the HomeArriveRadius getter - it is still used by the two comparison nodes
("homeDist > HomeArriveRadius" and "homeDist <= HomeArriveRadius"). Only the AI MoveTo
Acceptance Radius pin changes.

Do not touch the CHASE branch, the SimpleMoveToActor node, any StopMovement node, any
variable, any default value, any PrintString, or EventBeginPlay.

Then compile BP_Enemy and save it. Then report:
  - the node count before and after
  - the complete DSL of the Think event after the change
  - any compile warning or error, quoted verbatim
```

**명령 69와 71은 Terminal 명령이 아니다.** 둘 다 한글로 낸 PIE 플레이 절차다 — 사용자가 키보드로 직접 조작해야 하는 검증이라 영어로 옮길 대상이 없었다. 명령 69는 새 기준 넷을 보는 절차, 명령 71은 복귀 사양 기준 4를 보는 절차다.

**옮기며 넣은 해석** — 한글 지시에 없던 것을 영어 명령에 넣은 것이 넷 있다.

- **`AI MoveTo` → `SimpleMoveToActor` 교체.** 사용자는 `고친다`라고만 했다. 무엇으로 고칠지는 AI가 정했다. 짧은 홉 방식(`RETURN`이 쓰는 것)은 홉 목표점이 칸막이 벽 안에 떨어질 수 있어 기각했다
- **`StopMovement`를 세 분기에만.** `ATTACK` · `IDLE_WAIT` · `IDLE_HOME`. `NO_PLAYER`를 뺀 것도 AI 판단이다 — 플레이어 사망이 아직 구현돼 있지 않아 `PlayerRef`가 무효가 될 경로가 없다
- **`AcceptanceRadius = 0.0`.** 61.5 미만이면 무엇이든 되는데 0이 여유가 가장 크고, 엔진이 `-1`만 "기본값 사용" 신호로 쓰므로 0은 진짜 0으로 쓰인다
- **명령 69·71의 거리 숫자.** `2_dist 500~900을 유지하며 따라간다`, `3_home이 1500 아래로 내려가면 멈춘다`, `X 2500보다 −X 쪽` 등은 사양에 없다. 기준을 한 판으로 묶으려고 AI가 계산해 낸 경로다

## Terminal 결과

### 원문 — English

**먼저 밝힌다 — UE Terminal이 화면에 뱉은 출력은 이 기록에 없다.** 사용자가 명령을 붙여 실행한 뒤 `결과 확인`이라고만 했고, AI는 Terminal 창을 볼 수단이 없다. 아래는 전부 **AI가 MCP로 직접 읽은 것**이다: `EditorToolset.LogsToolset.GetLogEntries`로 읽은 UE 출력 로그와, `read_graph_dsl` · `get_properties` · `get_actor_transform`으로 읽은 실제 에디터 상태. **명령 68·70이 요구한 "node count before and after"와 "empty event stub 여부"는 사용자가 옮겨 오지 않아 확보하지 못했다.**

**명령 68 이후의 `Think` 그래프 전문** — `read_graph_dsl`로 읽었다.

```
(event Custom|Think
  (bind _returnvalue (Utilities|Time|GetGameTimeInSeconds))
  (bind _self self)
  (bind _returnvalue_1 (Transformation|GetActorLocation _self))
  (bind _homelocation (Variables|Default|GetHomeLocation))
  (bind _returnvalue_2 (Math|Vector|vector-vector _homelocation _returnvalue_1))
  (bind _returnvalue_3 (Math|Vector|VectorLength _returnvalue_2))
  (bind _playerref (Variables|Default|GetPlayerRef))
  (bind _returnvalue_4 (Transformation|GetDistanceTo _self _playerref))
  (bind _homearriveradius (Variables|Default|GetHomeArriveRadius))
  (bind _returnvalue_5 (> _returnvalue_3 _homearriveradius))
  (bind _returndelay (Variables|Default|GetReturnDelay))
  (bind _lastseentime (Variables|Default|GetLastSeenTime))
  (bind _returnvalue_6 (- _returnvalue _lastseentime))
  (bind _returnvalue_7 (>= _returnvalue_6 _returndelay))
  (bind _returnvalue_8 (and _returnvalue_7 _returnvalue_5))
  (Utilities|IsValid _playerref
    (:"Is Valid"
      (Development|PrintString (Utilities|String|ToString(Float) _returnvalue_4) true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 1.0 "2_dist")
      (Development|PrintString (Utilities|String|ToString(Float) _returnvalue_3) true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 1.0 "3_home")
      (if (<= _returnvalue_4 (select _returnvalue_8 (Variables|Default|GetReturnSightRange) (Variables|Default|GetSightRange)))
        (Variables|Default|SetLastSeenTime _returnvalue)
        (if (<= _returnvalue_4 (Variables|Default|GetAttackRange))
          (Development|PrintString "ATTACK" true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 1.0 "1_state")
          (AI|Navigation|StopMovement (Pawn|GetController _self))
          (Animation|PlayAnimMontage _self (Variables|Default|GetAttackMontage))
          (Game|Damage|ApplyDamage _playerref (Variables|Default|GetAttackDamage) (Pawn|GetController _self) _self)
          (Utilities|FlowControl|Delay (Variables|Default|GetAttackCooldown))
          (CallFunction|Think)
          (else
            (Development|PrintString "CHASE" true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 1.0 "1_state")
            (AI|Navigation|SimpleMoveToActor (Pawn|GetController _self) _playerref)
            (Utilities|FlowControl|Delay (Variables|Default|GetThinkInterval))
            (CallFunction|Think)))
        (elif _returnvalue_8
          (Development|PrintString "RETURN" true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 1.0 "1_state")
          (AI|AIMoveTo _self (Math|Vector|vector+vector _returnvalue_1 (Math|Vector|vector*vector (Math|Vector|Normalize _returnvalue_2) (Math|Float|Min(Float) (Variables|Default|GetReturnStepDistance) _returnvalue_3))) 0 _homearriveradius
            (:OnSuccess
              (Utilities|FlowControl|Delay (Variables|Default|GetThinkInterval))
              (CallFunction|Think))
            (:OnFail
              (Utilities|FlowControl|Delay (Variables|Default|GetThinkInterval))
              (CallFunction|Think)))
          (elif (<= _returnvalue_3 _homearriveradius)
            (Development|PrintString "IDLE_HOME" true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 1.0 "1_state")
            (AI|Navigation|StopMovement (Pawn|GetController _self))
            (Transformation|SetActorRotation _self (Variables|Default|GetHomeRotation))
            (Utilities|FlowControl|Delay (Variables|Default|GetThinkInterval))
            (CallFunction|Think)
            (else
              (Development|PrintString "IDLE_WAIT" true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 1.0 "1_state")
              (AI|Navigation|StopMovement (Pawn|GetController _self))
              (Utilities|FlowControl|Delay (Variables|Default|GetThinkInterval))
              (CallFunction|Think))))))
    (:"Is Not Valid"
      (Development|PrintString "NO_PLAYER" true true "(R=0.000000,G=0.660000,B=1.000000,A=1.000000)" 1.0 "1_state")
      (Variables|Default|SetPlayerRef (Game|GetPlayerCharacter 0))
      (Utilities|FlowControl|Delay (Variables|Default|GetThinkInterval))
      (CallFunction|Think))))

(event EventBeginPlay
  (bind _self self)
  (Variables|Default|SetPlayerRef (Game|GetPlayerCharacter 0))
  (Variables|Default|SetHomeLocation (Transformation|GetActorLocation _self))
  (Variables|Default|SetHomeRotation (Transformation|GetActorRotation _self))
  (Variables|Default|SetLastSeenTime (Utilities|Time|GetGameTimeInSeconds))
  (CallFunction|Think))
```

**명령 70 이후 바뀐 단 한 줄.** `RETURN` 분기의 `AIMoveTo` 네 번째 인자가 `_homearriveradius`에서 `0.0`이 됐다.

```
          (AI|AIMoveTo _self (Math|Vector|vector+vector _returnvalue_1 (Math|Vector|vector*vector (Math|Vector|Normalize _returnvalue_2) (Math|Float|Min(Float) (Variables|Default|GetReturnStepDistance) _returnvalue_3))) 0 0.0
```

**명령 68 도중에 나온 실패 원문.** `13.20.30`의 쓰기 시도가 이것으로 실패했고, `13.21.23`에 컴파일이 성공한 것으로 보아 사용자가 우회해서 통과시켰다. 어떻게 우회했는지는 Terminal 출력을 못 봐서 **모른다.**

```
[2026.08.31-13.20.30:468][757]LogScript: Warning: AssertionError: The node could not be created / Math|Vector|vector-vector does not exist
```

```
[2026.08.31-13.23.18:986][212]LogScript: Warning: Log category 'LogBlueprintCompile' not found.
```

```
[2026.08.31-13.24.33:322][435]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c624, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.31-13.24.33:335][435]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+c624, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.31-13.24.33:335][435]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+d6c4, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
[2026.08.31-13.24.33:335][435]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+d6c4, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
```

**PIE 종료 무렵마다 나온 것.** 이번 변경과 무관해 보이지만 원인은 안 봤다.

```
[2026.08.31-13.40.48:791][207]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
[2026.08.31-13.45.59:892][916]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
```

**컴파일과 저장.** 에러 없음.

```
[2026.08.31-13.21.23:243][882]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.08.31-13.23.06:654][175]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.08.31-13.23.38:367][270]LogFileHelpers: Saving Package: /Game/Enemy/BP_Enemy
[2026.08.31-13.23.38:367][270]Cmd: OBJ SAVEPACKAGE PACKAGE="/Game/Enemy/BP_Enemy" FILE="D:/20260827/MCP1/Content/Enemy/BP_Enemy.uasset" SILENT=true
[2026.08.31-13.52.14:786][556]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.08.31-13.52.31:478][588]LogFileHelpers: Saving Package: /Game/Enemy/BP_Enemy
```

**첫 PIE(12:41:58~12:43:08). 명령 68 이전.** 추격이 `Think`를 막는다는 첫 증거다. 상태 줄만 발췌했다.

```
[2026.08.31-12.42.08:718][855]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1142.742065
[2026.08.31-12.42.08:718][855]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.25
[2026.08.31-12.42.08:719][855]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.08.31-12.42.16:412][544]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
...
[2026.08.31-12.42.25:712][362]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 707.738220
[2026.08.31-12.42.25:712][362]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 342.976125
[2026.08.31-12.42.25:712][362]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-12.42.26:747][457]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 291.667236
[2026.08.31-12.42.26:748][457]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 140.738501
[2026.08.31-12.42.26:748][457]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.08.31-12.42.59:735][391]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
```

`12.42.26:748`의 `CHASE`와 `12.42.59:735`의 `RETURN` 사이에 **33초 동안 로그가 한 줄도 없다.** 그동안 `Think`가 0회 돌았다.

**두 번째 PIE(12:48:27~12:48:38). 명령 68 이전.** `CHASE`로 끝나고 아무 줄도 안 나온다.

```
[2026.08.31-12.48.38:202][266]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1233.661377
[2026.08.31-12.48.38:202][266]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.25
[2026.08.31-12.48.38:202][266]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
[2026.08.31-12.48.38:510][293]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1050.273560
[2026.08.31-12.48.38:510][293]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 0.25
[2026.08.31-12.48.38:510][293]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
```

**세 번째 PIE(13:39:46~13:40:48). 명령 68 이후.** `IDLE_WAIT`이 이 프로젝트에서 처음 로그에 나왔다. 상태 줄만 발췌했다.

```
[2026.08.31-13.39.58:791][566]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.08.31-13.39.59:097][595]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.08.31-13.39.59:399][624]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.08.31-13.40.11:574][844]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.08.31-13.40.11:884][874]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_WAIT
[2026.08.31-13.40.18:618][541]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-13.40.29:622][614]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.08.31-13.40.29:922][637]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_WAIT
[2026.08.31-13.40.36:621][287]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
```

같은 PIE에서 적이 처음으로 집에 도착했다. 거리 값을 붙인 전문이다.

```
[2026.08.31-13.40.36:621][287]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 2335.921875
[2026.08.31-13.40.36:621][287]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 900.375886
[2026.08.31-13.40.36:621][287]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-13.40.37:647][377]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1922.611572
[2026.08.31-13.40.37:647][377]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 698.938074
[2026.08.31-13.40.37:647][377]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-13.40.38:668][455]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 2029.534912
[2026.08.31-13.40.38:668][455]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 497.944740
[2026.08.31-13.40.38:668][455]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-13.40.39:690][533]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1830.894653
[2026.08.31-13.40.39:690][533]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 297.619219
[2026.08.31-13.40.39:690][533]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-13.40.40:555][598]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1461.396729
[2026.08.31-13.40.40:555][598]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 147.809892
[2026.08.31-13.40.40:555][598]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-13.40.41:072][636]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1201.135986
[2026.08.31-13.40.41:072][636]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 98.540625
[2026.08.31-13.40.41:072][636]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
[2026.08.31-13.40.41:385][659]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1149.159180
[2026.08.31-13.40.41:385][659]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 98.540625
[2026.08.31-13.40.41:385][659]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] CHASE
[2026.08.31-13.40.41:694][682]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1202.687500
[2026.08.31-13.40.41:694][682]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 170.797825
[2026.08.31-13.40.41:694][682]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_WAIT
```

**네 번째 PIE(13:45). 명령 70 이전.** 이번 세션에서 가장 중요한 원문이다. `3_home`이 `106.648573`에 소수점까지 얼어붙은 채 `RETURN`이 0.30초 간격으로 무한 반복된다.

```
[2026.08.31-13.45.55:927][536]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1420.466309
[2026.08.31-13.45.55:927][536]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 106.648573
[2026.08.31-13.45.55:927][536]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-13.45.56:230][565]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1587.083740
[2026.08.31-13.45.56:230][565]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 106.648573
[2026.08.31-13.45.56:230][565]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-13.45.57:159][652]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 2065.952148
[2026.08.31-13.45.57:159][652]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 106.648573
[2026.08.31-13.45.57:159][652]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-13.45.58:987][830]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 2033.159180
[2026.08.31-13.45.58:987][830]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 106.648573
[2026.08.31-13.45.58:987][830]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-13.45.59:599][890]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 2033.159180
[2026.08.31-13.45.59:599][890]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 106.648573
[2026.08.31-13.45.59:599][890]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
```

**다섯 번째 PIE(14:00). 명령 70 이후.** 홉마다 `3_home`이 정확히 300씩 줄고, 홉 하나에 6.4초가 걸린다.

```
[2026.08.31-14.00.20:308][479]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1480.022705
[2026.08.31-14.00.20:308][479]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 951.805449
[2026.08.31-14.00.20:308][479]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-14.00.26:669][105]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 1164.120483
[2026.08.31-14.00.26:669][105]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 651.805610
[2026.08.31-14.00.26:669][105]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-14.00.33:403][489]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 2459.172852
[2026.08.31-14.00.33:403][489]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 351.805646
[2026.08.31-14.00.33:403][489]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] RETURN
[2026.08.31-14.00.41:070][512]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 2755.863770
[2026.08.31-14.00.41:070][512]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] 51.806236
[2026.08.31-14.00.41:070][512]LogBlueprintUserMessages: [BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879] IDLE_HOME
```

**PIE 중에 읽은 `Enemy_Test`의 실제 트랜스폼.** `get_actor_transform`으로 `UEDPIE_0_` 월드의 액터를 직접 읽었다. 합격 기준 4의 유일한 증거다.

```
{"location":{"x":3948.2209728821163,"y":-1.6600871237589327,"z":92.150001049041748},
 "rotation":{"pitch":0,"yaw":180,"roll":-0},
 "scale":{"x":1,"y":1,"z":1}}
```

```
{"HomeRotation":{"pitch":0,"yaw":180,"roll":-0},
 "HomeLocation":{"x":4000,"y":0,"z":92.400001525878906},
 "LastSeenTime":42.837184399366379}
```

```
{"MaxWalkSpeed":300,"Velocity":{"x":0,"y":0,"z":0},"MaxAcceleration":2048,
 "BrakingDecelerationWalking":2048,"bOrientRotationToMovement":true,
 "RotationRate":{"pitch":0,"yaw":500,"roll":0},"bUseRVOAvoidance":false}
```

**세션 시작 시 읽은 `Enemy_Test`의 변수.** 명령 66에서 걷어낸 `0` 오버라이드가 그대로 걷힌 채 있음을 확인했다.

```
{"ReturnDelay":7,"ReturnSightRange":300,"ReturnStepDistance":300,"HomeArriveRadius":100,
 "SightRange":1200,"ThinkInterval":0.29999999999999999,"AttackRange":150,
 "AttackCooldown":1.5,"AttackDamage":10}
```

```
{"CapsuleRadius":35,"CapsuleHalfHeight":90}
```

**엔진 소스 원문.** 명령 70의 근거다.

```cpp
// Engine/Source/Runtime/AIModule/Private/Navigation/PathFollowingComponent.cpp:1328
const FVector::FReal UseRadius = RadiusThreshold + GoalRadius + (AgentRadius * AgentRadiusMultiplier);
```

```cpp
// PathFollowingComponent.cpp:136
	MinAgentRadiusPct = 1.1f;
// PathFollowingComponent.cpp:159
	bReachTestIncludesAgentRadius = true;
// PathFollowingComponent.cpp:125
const float UPathFollowingComponent::DefaultAcceptanceRadius = -1.f;
```

```cpp
// Engine/Source/Runtime/AIModule/Private/AISystem.cpp:28
	bFinishMoveOnGoalOverlap = true;
// Engine/Source/Runtime/AIModule/Private/Tasks/AITask_MoveTo.cpp:21
	MoveRequest.SetReachTestIncludesAgentRadius(GET_AI_CONFIG_VAR(bFinishMoveOnGoalOverlap));
```

명령 68의 근거가 된 소스다.

```cpp
// Engine/Source/Runtime/AIModule/Classes/Blueprint/AIBlueprintHelperLibrary.h:92
	UFUNCTION(BlueprintCallable, Category = "AI|Navigation")
	static AIMODULE_API void SimpleMoveToActor(AController* Controller, const AActor* Goal);
```

```cpp
// Engine/Source/Runtime/AIModule/Private/Blueprint/AIBlueprintHelperLibrary.cpp:493
	const bool bAlreadyAtGoal = PFollowComp->HasReached(*Goal, EPathFollowingReachMode::OverlapAgentAndGoal);

	// script source, keep only one move request at time
	if (PFollowComp->GetStatus() != EPathFollowingStatus::Idle)
	{
		PFollowComp->AbortMove(*NavSys, FPathFollowingResultFlags::ForcedScript | FPathFollowingResultFlags::NewRequest
			, FAIRequestID::AnyRequest, bAlreadyAtGoal ? EPathFollowingVelocityMode::Reset : EPathFollowingVelocityMode::Keep);
	}
	...
			if (Result.IsSuccessful())
			{
				Result.Path->SetGoalActorObservation(*Goal, 100.0f);
				PFollowComp->RequestMove(FAIMoveRequest(Goal), Result.Path);
			}
```

```cpp
// Engine/Source/Runtime/Engine/Classes/GameFramework/Controller.h:353
	/** Aborts the move the controller is currently performing */
	UFUNCTION(BlueprintCallable, Category="AI|Navigation")
	ENGINE_API virtual void StopMovement();
```

`bOrientRotationToMovement`가 `SetActorRotation`과 안 싸우는 근거다.

```cpp
// Engine/Source/Runtime/Engine/Private/Components/CharacterMovementComponent.cpp:6606
FRotator UCharacterMovementComponent::ComputeOrientToMovementRotation(const FRotator& CurrentRotation, float DeltaTime, FRotator& DeltaRotation) const
{
	if (Acceleration.SizeSquared() < UE_KINDA_SMALL_NUMBER)
	{
		// AI path following request can orient us in that direction (it's effectively an acceleration)
		if (bHasRequestedVelocity && RequestedVelocity.SizeSquared() > UE_KINDA_SMALL_NUMBER)
		{
			return RequestedVelocity.GetSafeNormal().Rotation();
		}

		// Don't change rotation if there is no acceleration.
		return CurrentRotation;
	}

	// Rotate toward direction of acceleration.
	return Acceleration.GetSafeNormal().Rotation();
}
```

**MCP 툴 사이의 표기 어긋남.** 같은 노드인데 툴마다 다르게 부른다.

```
find_node_types      → "AI|Navigation|SimpleMovetoActor"   (소문자 t)
get_node_type_pins   → "AI|Navigation|SimpleMoveToActor"   (대문자 T)
```

### 요약 — 한글

**`BP_Enemy`의 `Think` 이벤트 그래프만 고쳤다. 애셋은 `Content/Enemy/BP_Enemy.uasset` 하나뿐이다.**

**명령 68 — `CHASE` 분기 교체와 `StopMovement` 셋**

- `CHASE` 분기의 래턴트 `AI|AIMoveTo`(목표 = `PlayerRef`, 수용 반경 = `AttackRange - 20.0`) 노드를 삭제하고 비래턴트 `AI|Navigation|SimpleMoveToActor`(`Controller` = `Pawn|GetController(self)`, `Goal` = `PlayerRef`)로 바꿨다
- `OnSuccess` / `OnFail` 두 갈래가 하나로 합쳐지면서 중복이던 `Delay` + `Think` 쌍 하나가 사라졌다
- `AttackRange - 20.0` 감산 노드가 사라졌다. `GetAttackRange` 게터는 `ATTACK` 판정이 계속 써서 남았다
- `AI|Navigation|StopMovement`(`self` = `Pawn|GetController(self)`) 세 개를 `ATTACK` · `IDLE_HOME` · `IDLE_WAIT` 분기의 `PrintString` 바로 뒤에 넣었다. `RETURN`과 `NO_PLAYER`에는 안 넣었다
- 노드 수는 `find_nodes`로 세어 **94**다. 변경 전 수는 확보 못 했다

**명령 70 — `AcceptanceRadius` 핀 하나**

- `RETURN` 분기 `AI|AIMoveTo`의 `AcceptanceRadius` 핀에 걸려 있던 `GetHomeArriveRadius` 게터 선을 끊고 리터럴 `0.0`을 넣었다
- 노드는 안 늘고 안 줄었다. `GetHomeArriveRadius` 게터는 비교 노드 둘(`homeDist > HomeArriveRadius`, `homeDist <= HomeArriveRadius`)이 계속 쓴다

**안 바꾼 것** — 변수 일곱(`ReturnDelay` · `ReturnSightRange` · `ReturnStepDistance` · `HomeArriveRadius` · `HomeLocation` · `HomeRotation` · `LastSeenTime`)과 옛 변수 전부, 모든 기본값, `RETURN` 분기의 홉 수식(`Normalize` · `Min(Float)` · `vector+vector` · `vector*vector`), 디버그 `PrintString` 8개와 `ToString(Float)` 2개, `EventBeginPlay`, 레벨 인스턴스 `Enemy_Test`.

**변수를 하나도 안 건드렸으므로** 명령 66 때처럼 인스턴스가 클래스 기본값을 안 따라오는 문제는 이번엔 없다.

## 분석

### 무엇을 만들었나

**애셋은 하나다.** `Content/Enemy/BP_Enemy.uasset`. 새 블루프린트도 새 컴포넌트도 새 변수도 없다.

**그래프 변경 — `Think` 이벤트, 노드 94개**

`CHASE` 분기가 이렇게 됐다.

```
PrintString "CHASE"  (Key "1_state")
  → SimpleMoveToActor (Controller = GetController(self), Goal = PlayerRef)
  → Delay (ThinkInterval = 0.3)
  → Think
```

`ATTACK` 분기.

```
PrintString "ATTACK"
  → StopMovement (GetController(self))          ← 신규
  → PlayAnimMontage (AttackMontage)
  → ApplyDamage (PlayerRef, AttackDamage = 10, GetController(self), self)
  → Delay (AttackCooldown = 1.5)
  → Think
```

`IDLE_HOME` 분기.

```
PrintString "IDLE_HOME"
  → StopMovement (GetController(self))          ← 신규
  → SetActorRotation (self, HomeRotation)
  → Delay (ThinkInterval = 0.3)
  → Think
```

`IDLE_WAIT` 분기.

```
PrintString "IDLE_WAIT"
  → StopMovement (GetController(self))          ← 신규
  → Delay (ThinkInterval = 0.3)
  → Think
```

`RETURN` 분기 — 홉 수식은 그대로, 수용 반경만 바뀌었다.

```
PrintString "RETURN"
  → AIMoveTo (self,
              Destination = ActorLocation + Normalize(HomeLocation - ActorLocation)
                            * Min(ReturnStepDistance = 300, homeDist),
              Target Actor = null,
              Acceptance Radius = 0.0)          ← HomeArriveRadius 였다
      OnSuccess → Delay(0.3) → Think
      OnFail    → Delay(0.3) → Think
```

`NO_PLAYER` 분기와 `EventBeginPlay`는 손대지 않았다.

**튜닝 값은 하나도 안 바뀌었다.** 세션 시작 때 읽은 값이 끝까지 그대로다 — `ReturnDelay 7` · `ReturnSightRange 300` · `ReturnStepDistance 300` · `HomeArriveRadius 100` · `SightRange 1200` · `ThinkInterval 0.3` · `AttackRange 150` · `AttackCooldown 1.5` · `AttackDamage 10`. 무브먼트도 그대로다 — `MaxWalkSpeed 300` · `MaxAcceleration 2048` · `BrakingDecelerationWalking 2048` · `bOrientRotationToMovement true` · `RotationRate yaw 500` · `bUseRVOAvoidance false`. 캡슐은 `CapsuleRadius 35` · `CapsuleHalfHeight 90`.

**레벨 배치는 안 건드렸다.** `Enemy_Test`는 `(4000, 0, 90)` yaw 180 그대로다. `HomeLocation`이 `(4000, 0, 92.4)`로 읽히는 것은 `BeginPlay`가 캡슐 중심의 실제 위치를 굳혔기 때문이고, 배치 Z 90과 다른 것은 지면 스냅 때문이다.

### 기술적으로 맞게 짚은 부분

**짧은 홉을 `CHASE`에 안 쓴 것.** 이게 이번 세션에서 가장 중요한 "안 한 판단"이다. `RETURN`이 이미 짧은 홉으로 매 홉 재평가를 하고 있었으니 `CHASE`에도 같은 패턴을 쓰는 것이 자연스러워 보였다. 안 썼다. 이유는 이 레벨의 구조다 — 두 방이 문간 하나로만 이어져 있어서, 플레이어가 1번 방에 있고 적이 2번 방에 있으면 **직선 방향의 홉 목표점이 칸막이 벽 안에 떨어진다.** `RETURN`이 안 걸렸던 것은 집이 항상 열린 바닥 위이고 직선 경로가 방 안에 머물기 때문이지, 홉 방식이 안전해서가 아니다. 같은 패턴을 다른 맥락에 옮기면 깨진다는 것을 옮기기 전에 봤다.

**`SimpleMoveToActor`를 고른 것.** 결정 사다리 3번 — 엔진이 이미 준다. 구현을 읽고 세 가지를 확인한 뒤에 골랐다. 첫째, `UFUNCTION(BlueprintCallable)`이고 래턴트가 아니라 실행 핀을 안 문다. 둘째, `FindPathSync`로 제대로 경로를 찾으므로 문간을 돌아간다 — 홉 방식이 못 하는 것이다. 셋째, `SetGoalActorObservation(*Goal, 100.0f)`로 플레이어가 100 이상 움직이면 알아서 재경로한다. 그리고 재호출 시 `AbortMove`를 `EPathFollowingVelocityMode::Keep`으로 하므로 **0.3초마다 다시 불러도 속도가 안 끊긴다.** 이 마지막 것을 안 읽었으면 0.3초마다 멈칫거릴 것을 걱정해 다른 설계로 갔을 것이다.

**`StopMovement`가 캐스트를 안 요구하는 것을 확인한 것.** `AAIController`에 있을 것으로 짐작하면 `Cast To AIController`가 한 개 필요해지고, 그러면 0.3초마다 도는 `Think`에 Cast가 들어간다. 소스를 보니 `AController`에 `BlueprintCallable`로 있었다. 그래프에 이미 있던 `Pawn|GetController`를 그대로 쓰면 됐다. **짐작으로 갔으면 필요 없는 노드를 하나 더 만들었을 것이다.**

**`NO_PLAYER` 분기에 `StopMovement`를 안 넣은 것.** 넣으면 대칭이 예뻐진다. 안 넣었다. `PlayerRef`가 무효가 되는 경로는 플레이어 사망뿐인데 사망이 아직 구현돼 있지 않다. **지금 없는 상황을 위해 노드를 만들지 않는다** — 결정 사다리 1번.

**`HomeArriveRadius`를 안 건드리고 `AcceptanceRadius`를 건드린 것.** 사각지대를 없애는 방법은 둘이었다. 블루프린트 판정을 느슨하게(`HomeArriveRadius` 100 → 150) 하거나, 무버의 정지 반경을 좁게(`AcceptanceRadius` 100 → 0) 하거나. 앞엣것은 **손으로 맞춘 튜닝 값을 바꾸는 것**이고 "이 안이면 집에 도착"이라는 의미까지 넓어진다. 뒤엣것은 구현 세부다. 뒤를 골랐다.

**`0`이 안전한 값인지 확인한 것.** `DefaultAcceptanceRadius = -1.f`라는 것을 소스에서 보고 넣었다. `0`이 "기본값 사용" 신호였다면 조용히 다른 값이 들어갔을 것이고, 그러면 왜 안 되는지 알아내는 데 또 한 판이 걸렸을 것이다.

**`bOrientRotationToMovement`와 `SetActorRotation`이 안 싸운다는 것을 소스로 미리 확인한 것.** 복귀 사양이 이것을 `남는 위험` 1번으로 적어뒀다. `ComputeOrientToMovementRotation`이 가속도가 0이면 `CurrentRotation`을 그대로 돌려준다는 것을 읽고, 위험이 사양이 적은 것보다 낮다고 먼저 말했다. **결과적으로 맞았다** — 기준 4가 실패한 진짜 이유는 회전 싸움이 아니라 애초에 `IDLE_HOME`에 못 들어간 것이었다. 사양이 지목한 용의자가 아니었다.

**로그로 진단한 것.** 두 버그 다 정적 분석으로는 안 잡혔을 것이다. 그래프는 두 번 다 "맞게" 보였다. `CHASE` 뒤의 33초 공백과, `3_home`이 `106.648573`에 소수점까지 얼어붙은 것 — 둘 다 **숫자가 안 변한다는 사실 자체가 증거**였다. 디버그 `PrintString`을 `bPrintToLog true`로 넣어둔 것(명령 67)이 여기서 값을 했다.

**사용자의 관찰을 뒤집지 않은 것.** `PIE 결과 이상 없음`이라는 보고를 받고도 로그를 읽었고, 아홉 중 여덟이 아니라 셋만 통과했다는 것을 그때 찾았다. 반대로 `안바라봄 내가 눈으로 봤으`라고 했을 때는 로그가 그것을 그대로 뒷받침했다.

### 확인한 것 / 확인 못 한 것

**확인한 것**

- **`Think` 그래프의 최종 상태.** `read_graph_dsl`로 명령 68 뒤와 명령 70 뒤 두 번 읽었다. MCP의 "됐다"는 응답이 아니라 그래프 전문을 대조했다
- **`K2Node_AIMoveTo`가 하나만 남았다.** `find_nodes`로 전체 94개를 나열해 확인했다. 남은 하나는 `RETURN` 분기의 것이다. `CHASE`의 래턴트 노드가 실제로 제거됐다는 직접 증거다
- **컴파일 에러·경고 없음.** `13.21.23` · `13.23.06` · `13.52.14` 세 번 컴파일됐고 `LogBlueprint`에 에러가 없다
- **디스크에 실제로 썼다.** `13.23.38`과 `13.52.31`의 `Saving Package` 로그, 그리고 `BP_Enemy.uasset`의 mtime `22:52:31`
- **`git status`가 `M Content/Enemy/BP_Enemy.uasset` 하나뿐이다.** 다른 것을 안 건드렸다는 증거다
- **명령 68의 새 합격 기준 1** — 문을 연 채 도망쳤는데 복귀했다. `13.40.11:574 CHASE` → `13.40.18:618 RETURN`으로 **7.044초**, `13.40.29:622 CHASE` → `13.40.36:621 RETURN`으로 **6.999초**. 두 번 독립적으로 나왔다
- **명령 68의 새 합격 기준 2** — 추격 중 `CHASE`가 0.30초 간격으로 계속 찍힌다. 최대 공백 0.31초. 명령 68 이전의 33초 공백이 사라졌다
- **`IDLE_WAIT`이 로그에 처음 나왔다.** 이 프로젝트에서 한 번도 안 나왔던 상태다. `Think`가 추격 중에도 돈다는 직접 증거다
- **복귀 사양 합격 기준 1** — 위와 같다
- **복귀 사양 합격 기준 2** — 복귀 중 `2_dist` `291.667236`과 `283.514038`에서 `CHASE`로 전환. `ReturnSightRange 300` 바로 아래다. 두 번 나왔다
- **복귀 사양 합격 기준 3** — 플레이어가 1461~2335 거리에서 따라오는 동안 적이 무시하고 집까지 갔다. `3_home` 900.375886 → 98.540625
- **복귀 사양 합격 기준 4** — PIE 중에 `UEDPIE_0_` 월드의 액터를 `get_actor_transform`으로 직접 읽었다. `rotation yaw 180`, `HomeRotation`의 yaw 180과 일치. 위치 `(3948.221, -1.660, 92.150)`, 집에서 51.8
- **복귀 사양 합격 기준 5** — 복귀해서 집에 선 적(`3_home 98.540625`)이 `2_dist 1149.159180`으로 `SightRange 1200` 안에 들어오자 `CHASE`. **스폰 직후가 아니라 진짜 복귀 후 상태다**
- **`Enemy_Test` 인스턴스의 값이 정상이다.** 세션 시작 때 아홉 개를 읽어 클래스 기본값과 같음을 확인했다. 명령 66에서 걷어낸 `0` 오버라이드가 다시 안 생겼다
- **UE 로그가 UTC이고 파일시스템이 KST(+9)라는 것.** `Saving Package`의 `13.52.31`과 mtime `22:52:31`이 정확히 9시간 차다

**확인 못 한 것**

- **명령 68의 새 합격 기준 3(`ATTACK` 때 제자리에 서서 때린다).** 로그에는 `ATTACK` `13.40.27:205` → `CHASE` `13.40.28:706`으로 `AttackCooldown 1.5`와 맞는 간격만 남는다. **밀고 지나갔는지는 화면에서만 보이고, 사용자의 육안 보고가 유일한 근거다**
- **명령 68의 새 합격 기준 4(범위 밖으로 나가면 즉시 선다).** `CHASE` → `IDLE_WAIT` 전이가 0.31초 만에 일어난 것은 로그에 있지만, **실제로 멈춰 서는 것은 로그에 안 남는다.** 사용자의 육안 보고가 근거다
- **Terminal이 화면에 뱉은 출력 전부.** 사용자가 옮겨 오지 않았고 AI는 Terminal 창을 볼 수단이 없다. 명령 68·70이 요구한 변경 전 노드 수와 `write_graph_dsl`의 빈 이벤트 스텁 생성 여부를 **확보하지 못했다**
- **`13.20.30`의 실패를 사용자가 어떻게 우회했는지.** `Math|Vector|vector-vector does not exist` 뒤 53초 만에 컴파일이 성공했는데 그 사이에 무엇을 했는지 모른다
- **복귀가 4배 느려진 원인.** 관찰은 확실하다 — 명령 70 이전에는 초당 180(900.4 → 98.5를 4.451초), 이후에는 초당 45(951.8 → 51.8을 약 20초). `MaxWalkSpeed`는 PIE에서 읽어도 300이다. **`AcceptanceRadius 0`이 목표점에 정확히 닿기를 요구해 미세 조정에 시간을 쓴다**는 가설을 세웠지만 증명하지 못했다. 우회로만 확인했다 — `3_home`이 홉마다 정확히 300씩 줄었으므로 경로 우회는 아니다
- **`LogCrowdFollowing: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance`의 원인.** PIE 종료 무렵마다 나온다. 이번 변경과 무관해 보이지만 안 봤다
- **`find_node_types`와 `get_node_type_pins`가 같은 노드를 다르게 부르는 이유.** 어느 쪽이 `write_graph_dsl`이 받는 표기인지도 확정 못 했다 — 대문자 `T`로 보냈고 통과했다는 것만 안다
- **`read_graph_dsl`이 뱉은 `Math|Vector|vector-vector`를 `write_graph_dsl`이 거부하는 이유.** 읽기와 쓰기가 같은 id 체계를 안 쓴다는 사실만 확보했다

### 남는 리스크

- **복귀 속도가 초당 45다.** 명령 70 이전의 4분의 1이다. 사용자가 `그대로두자`로 정했다. 고치려면 `AcceptanceRadius`에 0 대신 중간값(예: 30 — 최악의 경우 도달 반경 `30 + 35 × 1.1 = 68.5`로 `HomeArriveRadius 100` 안)을 넣고 PIE로 재봐야 한다. **경험적인 값이라 계산으로는 못 정한다**
- **문을 닫아도 1200 안이면 안 돌아간다.** 감지가 순수 거리라 벽을 통과해서 본다. 명령 68 이전에는 문을 닫으면 `AIMoveTo`가 경로 실패로 끝나 복귀가 일어났는데, 이제 `Think`가 계속 돌면서 벽 너머 플레이어를 계속 본다. **사용자가 `거리만 유지 — 문은 물리적 장벽뿐`을 골랐다.** 시야각·라인 오브 사이트가 생기면 해결된다
- **`HomeArriveRadius 100`이 한 `Think` 틱과 거의 같다.** 속도 300에 `ThinkInterval 0.3`이면 한 틱이 최대 90이다. `13.40.41:385`의 `CHASE` 한 틱에 적이 72를 움직여 `3_home`이 98.5 → 170.8이 됐고, 집을 벗어나 다시 7초를 기다렸다. 집 근처에서 상태가 튄다. **튜닝 값이라 안 건드렸다**
- **`SimpleMoveToActor`가 0.3초마다 `FindPathSync`를 동기로 부른다.** 적 하나면 무시할 수준이다. **적이 여럿이 되면 다시 봐야 한다**
- **`SimpleMoveToActor`에는 수용 반경이 없다.** 예전 `AIMoveTo`는 `AttackRange - 20 = 130`에서 멈췄다. 이제 `ATTACK` 분기의 `StopMovement`가 멈추는데 `Think`가 0.3초 간격이라 최대 90을 더 파고들 수 있다. 캡슐 충돌이 막을 것으로 보지만 **육안 확인 외에 근거가 없다**
- **`RETURN` 분기만 아직 래턴트다.** `AIMoveTo`가 홉 하나를 무는 동안 `Think`가 안 돈다. 지금은 홉이 6.4초라 **복귀 중 감지 주기가 6.4초**다. 명령 70 이전에는 1.03초였다. 복귀 사양 합격 기준 2가 이미 통과했으므로 사양 위반은 아니지만, 실질 감지 주기가 여섯 배 나빠졌다
- **`NO_PLAYER` 분기에 `StopMovement`가 없다.** 플레이어 사망이 생기면 `PlayerRef`가 무효가 되고, 그때 적이 계속 걸어갈 수 있다. **적 HP·사망을 만들 때 같이 봐야 한다**
- **디버그 `PrintString` 8개와 `ToString(Float)` 2개가 그래프에 남아 있다.** 사양은 합격 기준이 통과하면 지우라고 적어뒀고 아홉 다 통과했다. **사용자가 `남긴 채 정리한다`를 골랐다** — 적 HP·피격·사망을 만들 때 다시 쓸 것이기 때문이다

### 총평

**요청은 다 채웠다.** 사용자가 처음 요청한 것은 `68 고고` — 이미 구현된 복귀 기능을 PIE로 검증하는 것이었다. 검증하다 두 개의 버그가 나왔고 둘 다 고쳐서 아홉 기준을 전부 통과시켰다.

**이 작업의 실질적 난이도는 만드는 데 있지 않았다.** Terminal 명령은 둘뿐이고, 하나는 노드 넷을 바꾸는 것이고 다른 하나는 핀 하나에 숫자를 넣는 것이다. 어려웠던 것은 **무엇을 고쳐야 하는지 알아내는 것**이었다.

두 버그 다 그래프를 아무리 봐도 안 보인다. 첫째는 `AI MoveTo`가 래턴트라는 것 — 노드 하나가 실행 핀을 물고 있으면 그 뒤의 모든 판정이 정지한다는 사실이 그래프의 모양에는 안 나타난다. 둘째는 `AcceptanceRadius`가 그대로 쓰이지 않고 에이전트 반지름이 더해진다는 것 — 이건 엔진 소스를 읽기 전에는 알 방법이 없다. **둘 다 "블루프린트가 시킨 것"과 "엔진이 실제로 하는 것" 사이의 틈이었다.**

찾아낸 수단도 같았다. `PrintString`의 숫자가 **안 변한다**는 것. 33초의 공백과 `106.648573`이라는 고정값. 어느 쪽도 에러가 아니고 경고도 없다. 로그를 안 읽었으면 "가끔 이상하네"로 남았을 것이다.

**사용자의 육안 관찰이 두 번 결정적이었다.** `문을 닫고 나면 제대로 되돌아가는걸`은 첫 버그의 증상을 정확히 지목한 것이고, `리턴하면 리턴한 방향에서 다시 문쪽 안바라보는거 같은데`는 둘째 버그의 입구였다. 로그는 그 관찰이 어디서 오는지 설명했을 뿐이다. **어느 쪽도 AI가 먼저 못 봤다.**

반대로 `PIE 결과 이상 없음`이라는 보고를 그대로 받았으면 아홉 중 셋만 통과한 상태로 넘어갔을 것이다. 눈과 로그가 서로를 보정했다.

## AI의 제안

> **짧은 홉은 기각한다.** `RETURN`이 쓰는 홉 패턴을 `CHASE`에 그대로 쓰면 **홉 목표점이 칸막이 벽 안에 떨어진다.** (…) **대신 `Simple Move To Actor`가 있다.** 엔진이 이미 준다 — 결정 사다리 3번.

사용자는 `고친다`라고만 했고 방법은 AI가 정했다. 얻는 것은 문간을 제대로 돌아가는 경로 탐색과 0.3초마다의 재평가, 잃는 것은 `RETURN`과 `CHASE`가 서로 다른 이동 방식을 쓰게 되는 비대칭이다.

> **`StopMovement`도 캐스트 없이 된다.** `AController`에 `BlueprintCallable`로 있다 — 이미 그래프에 있는 `GetController`를 그대로 쓴다.

AI가 먼저 소스를 확인하고 꺼낸 것이다. 얻는 것은 0.3초마다 도는 `Think`에 `Cast To AIController`가 안 들어가는 것, 잃는 것은 없다.

> **`NO_PLAYER`를 뺀 이유** — `PlayerRef`가 무효가 되는 경우는 플레이어 사망뿐인데 **아직 사망이 구현돼 있지 않다.** 지금 없는 상황을 위해 노드를 넣지 않는다.

사양에는 "세 분기"만 적혀 있었고 네 번째를 넣을지는 AI가 정했다. 얻는 것은 노드 하나를 안 만드는 것, 잃는 것은 플레이어 사망을 만들 때 이 분기를 다시 봐야 한다는 것이다.

> **기준 4의 위험이 사양이 적은 것보다 낮다.** (…) 엔진 소스를 확인했다 — `ComputeOrientToMovementRotation`은 가속도가 0이면 `CurrentRotation`을 그대로 돌려준다. **멈춰 있으면 안 싸운다.**

사용자가 묻지 않았는데 AI가 먼저 사양의 `남는 위험` 1번을 재평가한 것이다. 얻는 것은 엉뚱한 용의자를 쫓지 않은 것, 잃는 것은 없다.

> **`HomeArriveRadius 100`이 아슬아슬하다.** 속도 300에 `ThinkInterval 0.3`이면 **한 틱이 최대 90**이다. `HomeArriveRadius`가 100이니 **틱 하나가 도착 반경과 거의 같다.** (…) 손으로 맞춘 값이라 안 건드린다.

사용자가 묻지 않았다. 얻는 것은 집 근처에서 상태가 튀는 이유를 알아둔 것, 잃는 것은 없다 — 값을 안 바꿨다.

> **중간값을 넣어본다** — `AcceptanceRadius`를 `0` 대신 **30**으로. 도달 반경이 최악의 경우에도 `30 + 35×1.1 = 68.5`로 `HomeArriveRadius 100`보다 작아 기준 4는 유지된다.

복귀가 4배 느려진 것을 AI가 먼저 발견하고 꺼낸 것이다. 얻는 것은 복귀 속도 회복 가능성, 잃는 것은 PIE를 한 판 더 돌려야 하고 값이 경험적이라 한 번에 맞는다는 보장이 없다는 것. **사용자가 `그대로두자`로 정했다.**

## 다음으로 넘김

**이 칸은 더 이상 최신이 아니다. 현재 인계는 [2026-09-01-player-death-and-enemy-fov.md](2026-09-01-player-death-and-enemy-fov.md)의 `다음으로 넘김`이다.**
아래에서 처리된 항목은 지웠다 — `시야각을 언제 넣을 것인가`(넣었다),
`적의 HP·피격·사망`의 선행 조사(플레이어 공격 수단이 없어 못 한다는 것이 밝혀졌고
플레이어 사망·리스폰을 먼저 만들었다). 나머지는 새 기록으로 옮겼다.

**바로 이어서 할 것**

- 없음. 새 기록으로 넘어갔다

**결정 필요**

- 없음. 새 기록으로 넘어갔다
- **`RETURN` 분기도 비래턴트로 바꿀 것인가.** 지금 복귀 중 감지 주기가 6.4초다. 명령 70 이전에는 1.03초였다. `SimpleMoveToLocation`으로 바꾸면 0.3초가 되지만, 짧은 홉 구조의 존재 이유가 없어지고 이미 통과한 복귀 사양 합격 기준 2의 동작이 바뀐다
- **칸막이 `SM_Cube2`를 `Divider_L`로 리네임할 것인가.** 짝이 `SM_Cube2` / `Divider_R`로 어긋나 있다
- **`BP_Door.uasset`의 재직렬화를 어떻게 다룰 것인가.** 누적 세 번이다

**확인 필요**

- **복귀가 4배 느려진 진짜 원인.** `AcceptanceRadius 0`이 목표점 정확 도달을 요구한다는 가설만 있다. 경로 우회가 아니라는 것만 배제했다
- **`BP_Enemy`의 새 변수 넷이 인스턴스 편집으로 표시됐는지.** `ReturnDelay` · `ReturnSightRange` · `ReturnStepDistance` · `HomeArriveRadius`. 지난 세션부터 이월된 항목이다. **AI가 읽을 수단이 없다** — `set_variable_instance_editable`은 있는데 그것을 되읽는 툴이 없고, `get_properties`로 값이 읽히는 것은 증거가 안 된다(플래그와 무관하게 읽힌다). My Blueprint 패널에서 눈 아이콘을 봐야 한다. 명령 53의 여섯 개는 사용자가 확인해줬고 이 넷은 아직 안 물어봤다
- **`LogCrowdFollowing: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance`.** PIE 종료 무렵마다 나온다
- **`find_node_types`와 `get_node_type_pins`의 type_id 표기가 다른 이유.** `SimpleMovetoActor` / `SimpleMoveToActor`
- **`read_graph_dsl`이 뱉는 `Math|Vector|vector-vector`를 `write_graph_dsl`이 거부하는 이유.** 읽기와 쓰기의 id 체계가 다르다
- **`13.20.30` 실패를 사용자가 어떻게 우회했는지.** Terminal 출력을 못 봤다
- **2번 방의 조명.** `DirectionalLight`·`SkyLight` 외에 아무것도 없다
- **`Save All`이 왜 `BP_Enemy`를 안 썼는지.** 지난 세션 항목이다. 이번엔 안 나왔다
- **`write_graph_dsl`이 빈 이벤트 스텁을 만드는 조건.** 이번 세션에는 확인할 수단이 없었다 — Terminal 출력을 못 봤다
- **`bCanEverTick`이 명령 56 직후 `false`로 읽혔던 이유.** 지난 세션 항목이다
- **`trace_world`가 방향에 따라 같은 솔리드를 놓치는 이유.** 원인 미상
- **`show navigation`이 PIE에서 안 먹는 이유.** 에디터 뷰포트의 `P`로 우회했다
- **두 신규 외부 액터 패키지의 정체와 `__ExternalObjects__` 파일의 정체**
- **`Lvl_ArenaShooter`의 WorldSettings가 `BP_ShooterGameMode`를 가리키는지.** `.umap`이 바이너리라 못 읽었다
- **`HandGrip_R` 소켓의 위치·각도.** 방향이 있는 메시(칼)가 오면 드러난다

**접어둔 것**

- **카메라 작업.** 셋으로 갈렸다
  - **A — 원본 ICI 구조(`캡슐 → Camera → SkeletalMesh`)로 교체.** 팔만 있는 스켈레탈 메시가 프로젝트에 없어 지금 그대로는 못 한다
  - **B — 지금 구조를 두고 팔을 시야로 올린다.** `Variant_Shooter/Anims/ABP_FP_Weapon` + `Ctrl_HandAdjusment`. 무기용이라 맨손·칼에 맞는지는 열어봐야 안다
  - **C — 전환 스냅 완화만.** 요 보간 또는 `SetViewTargetWithBlend`. 2026-08-27부터 이월. 작다
  - **칼 직전에 B로 가는 것을 권했고 사용자가 적 AI를 먼저 하기로 정했다**
- **플레이어 사망과 리스폰.** 지금은 `CurrentHP`가 0이 되어도 아무 일도 안 일어난다. 진행 구조 단계
- **적 체력바 위젯 / 순찰 / EQS / 여러 적의 회피 / 적 종류별 DataTable.** 사양의 `접어둔 것` 참조
- **AnimNotify로 타격 창 열기.** 무기가 생길 때. 지금은 데미지가 애니메이션의 타격 순간보다 먼저 들어간다
- **`BP_ShooterNPC` · `ST_Shooter` · EQS 3개 · StateTree 태스크 6개.** 안 쓰기로 했지만 지우지 않는다
- **`--append-system-prompt`가 저장소에 없다.** `Editor Preferences → General → Terminal → Startup Commands`의 사용자 설정이라 다른 환경에서는 다시 넣어야 한다. 원문은 `Docs/AI-Log/2026-08-28-inventory-item-data.md`의 `명령` 칸에 있다
- **문간 위 `X 1800..1900, Z 200..400`의 열린 홈.** 1번 방 쪽에서 보면 문 위가 우묵하다. 관통은 아니다
- **열린 문짝 20cm가 문간 위로 삐져나온다.** 문짝 220, 문간 200
- **`ForLoop.FirstIndex`가 빈 값인 이유.** 동작에 지장이 없다
- **`SP` 스태미나.** 원본에 있고 MCP1에 없다. `06-플레이어-UI.md:54` 참조
- **슬롯 2칸 vs 3칸.** 원본은 2칸, MCP1은 3칸이다. 의도한 차이인지 안 정했다
- **미사용 애셋 정리.** 2026-08-30에 **남기기로** 정했다. 지우지 않는다
- **`MoveComponentTo`의 `Stop`·`Return` 핀.** 연타로는 문제가 안 났다
