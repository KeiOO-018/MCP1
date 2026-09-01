# 2026-09-01

## 작업물

적에게 HP·피격·사망을 만들고, 칸막이 세 조각의 이름을 실제 배치에 맞게 고쳤다.

**소요 시간**: 약 1시간 45분 (22:19 ~ 00:04)

## 명령

### 한글

```
잔업먼저하고 하자
```

칸막이 이름에 대한 답 (AskUserQuestion):

```
칸막이 이름을 고칠까요?  → L / R / Top으로 고침 (권장)
```

```
결과 확인
```

적 HP·피격·사망 심문에 대한 답 넷 (AskUserQuestion, 전부 권장안):

```
적 체력과 플레이어 공격 데미지를 얼마로 할까요?  → 적 100 / 데미지 34 — 3대 (권장)
적이 죽으면 어떻게 할까요?                      → 그 자리에서 사라짐 (권장)
적이 맞았을 때 반응을 넣을까요?                  → PrintString만 (권장)
죽은 적을 리스폰시킬까요?                        → 안 함 (권장)
```

```
그대로하자
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
그 내가 잘못본게 아니라면 한대맞고 죽은거같은데 이거 확인좀
```

```
PIE멈춤
```

```
결과 확인
```

```
PIE 켜져있는데 저거 결과 바바
```

```
1. 복귀도 잘되는데 2 할까 어떤데
```

```
고치고하자
```

```
결과 확인
```

```
공격 애니메이션 나옴
```

### English — MCP에 실제로 보낸 명령

**명령 1 — 칸막이 이름 바로잡기**

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, correct two
actor labels. The three divider pieces were labelled Divider_L / Divider_M /
Divider_R on the assumption they sit side by side. They do not: two are the
jambs either side of the doorway, and the third is the header spanning above
it. This is a label change only.

Measured extents (Cube is 100 units, location is the min corner):
  Divider_L   X 1800..2000   Y -2000..-100   Z   0..200   (jamb, -Y side)
  Divider_M   X 1800..2000   Y   100..2000   Z   0..200   (jamb, +Y side)
  Divider_R   X 1900..2000   Y -2000..2000   Z 200..400   (header, spans all Y)

Renames, in this order:
  "Divider_R"  ->  "Divider_Top"
  "Divider_M"  ->  "Divider_R"
  "Divider_L"  ->  unchanged, do not touch

The order matters: the current "Divider_R" must vacate the name BEFORE
"Divider_M" takes it, or two actors will briefly share the label.

CAUTION: find_actors matches labels by substring, so "Divider_R" also matches
nothing else right now but "Divider" matches all three. Resolve each actor by
its object path, not by a fresh substring search, once you have read them in
STEP 0. The object paths are:
  Divider_L  ...StaticMeshActor_UAID_F4A475FF15A3736A02_1961959730
  Divider_M  ...StaticMeshActor_UAID_9C6B005AF86930FD02_1392108111
  Divider_R  ...StaticMeshActor_UAID_F4A475FF15A3736A02_1961956726

Do NOT rename any other actor.
Do NOT change any transform - no location, rotation or scale on any actor.
Do NOT touch any Blueprint or DataTable.

STEP 0. Find all actors whose label contains "Divider" and report, for each,
  its object path, its exact label, and its world location, rotation and
  scale. Confirm there are exactly three and that they match the paths above.
  If not, STOP.
STEP 1. Rename the two labels in the order given.
STEP 2. Re-read all three by object path and report their exact labels and
  their world location, rotation and scale.
STEP 3. Save the level.

REPORT:
 R1. the STEP 0 listing, verbatim
 R2. each rename performed, one line each
 R3. the STEP 2 re-read - confirm the three labels are now
     Divider_L, Divider_R, Divider_Top
 R4. confirm all three transforms are IDENTICAL to the STEP 0 reading,
     value by value
 R5. confirm nothing is still labelled "Divider_M"
 R6. the save result
```

**명령 2 — 적의 HP 변수와 초기화**

```
In /Game/Enemy/BP_Enemy, make two changes and nothing else.

CHANGE 1 - add two variables.
  a) A float member variable named MaxHP, default value 100.0, instance-editable
     (the eye icon ON, so it can be tuned on the placed instance). This matches
     how SightRange, AttackDamage and ReturnDelay are already set up.
  b) A float member variable named CurrentHP, default value 0.0, NOT
     instance-editable (eye icon OFF). This is runtime state, so it follows
     PlayerRef / LastSeenTime / HomeLocation / HomeRotation, which all have the
     eye icon off. It is filled in at BeginPlay by CHANGE 2 - do NOT give it a
     default of 100.
Add no other variable. Do NOT rename or remove any existing variable.

CHANGE 2 - insert one assignment into the existing Event BeginPlay chain.
Today that chain is exactly six nodes, left to right:
  K2Node_Event_0        Event BeginPlay          at (0, 3554)
  K2Node_VariableSet_10 Set PlayerRef            at (560, 3554)
  K2Node_VariableSet_11 Set HomeLocation         at (1120, 3554)
  K2Node_VariableSet_12 Set HomeRotation         at (1680, 3554)
  K2Node_VariableSet_13 Set LastSeenTime         at (2240, 3554)
  K2Node_CallFunction_82 Think (custom event call) at (2520, 3554)

Insert "Set CurrentHP = MaxHP" BETWEEN K2Node_VariableSet_13 and
K2Node_CallFunction_82. It must come BEFORE the Think call, not after: Think
is the entry of a Delay-driven loop, so anything wired after it does not run
when expected.

Target chain:
  Event BeginPlay
    -> Set PlayerRef
    -> Set HomeLocation
    -> Set HomeRotation
    -> Set LastSeenTime
    -> Set CurrentHP  (value = Get MaxHP)
    -> Think

Node placement, so nothing overlaps:
  new Set CurrentHP node   at (2520, 3554)
  new Get MaxHP getter     at (2440, 3700)
  move K2Node_CallFunction_82 (Think) to (2900, 3554)
Moving that one Think node is the only node move allowed in this command.

Do NOT touch the Think custom event's own body.
Do NOT touch the ATTACK, CHASE, RETURN, IDLE_HOME, IDLE_WAIT or NO_PLAYER
branches.
Do NOT add or remove any PrintString.
Do NOT reconnect or delete K2Node_Self_1 or its single link to
K2Node_CallFunction_49 (ApplyDamage . DamageCauser).
Do NOT change any existing default value: ThinkInterval 0.3, ReturnDelay 7,
HomeArriveRadius 100, ReturnStepDistance 300, ReturnSightRange 300,
SightRange 1200, SightHalfAngle 60, AttackRange 150, AttackDamage 10,
AttackCooldown 1.5 all stay as they are.
Do NOT touch BP_ThirdPersonCharacter, DT_Items, the level, or any animation
asset.

STEP 0. Report the current variable list and the current BeginPlay chain.
STEP 1. Add the two variables.
STEP 2. Compile, so the new variables exist on the generated class.
STEP 3. Set the defaults: MaxHP 100.0, CurrentHP 0.0. Read them back and
  report the values you actually read, not the values you wrote.
STEP 4. Build the Set CurrentHP / Get MaxHP nodes and rewire as specified.
STEP 5. Compile again.

REPORT:
 R1. the STEP 0 reading
 R2. the variable list after, and the default values read back in STEP 3
 R3. every node created, every connection made or broken, and the Think move
 R4. the BeginPlay chain read back node by node with get_node_infos
 R5. confirm Think is still the LAST node in the chain
 R6. whether MaxHP shows the instance-editable eye icon as ON, and CurrentHP
     as OFF, in the My Blueprint panel
 R7. the EventGraph node count before and after
 R8. any compile warning or error, quoted verbatim
```

**이 명령이 버그를 만들었다.** `STEP 2`에서 컴파일하는 순간 레벨 인스턴스가 그때의 기본값 `MaxHP 0`을 자기 값으로 굳혔고, `STEP 3`에서 CDO를 `100`으로 올려도 인스턴스는 따라오지 않았다. `R2`가 CDO만 되읽게 되어 있어서 그 자리에서 안 잡혔다. 명령 4가 그 뒷수습이다.

**명령 3 — 적 피격·사망 + 플레이어 데미지**

```
Make changes in TWO Blueprints. Do the enemy first, compile it, then the player.

=====================================================================
PART A - /Game/Enemy/BP_Enemy : add an Event AnyDamage chain.
=====================================================================

The graph currently occupies x 0..10920, y 300..3700. Build this new chain in
the empty area starting at (0, 4100) so it overlaps nothing.

Target shape:
  Event AnyDamage (Damage, DamageType, InstigatedBy, DamageCauser)
    -> Set CurrentHP = Clamp(CurrentHP - Damage, 0.0, MaxHP)
    -> PrintString( "EnemyHP: " + ToString(CurrentHP) )
    -> Branch (Condition = CurrentHP <= 0.0)
         True  -> DestroyActor
         False -> nothing connected

Details that matter:
  - Feed the Append and the Branch from the Set CurrentHP node's own output
    value pin, not from a fresh Get CurrentHP node. That guarantees they read
    the value just written.
  - The PrintString gets bPrintToScreen true, bPrintToLog true, Key = None
    (no key - each hit must appear as its own line, not overwrite in place).
  - DestroyActor targets self: leave its self pin EMPTY. An unconnected self
    pin compiles to self (KismetCompiler.cpp:2185). Do NOT create a Self node.
  - Do NOT add any "is dead" flag or new variable. Destroying the actor
    cancels the pending Delay in the Think loop, which is what stops it.

Do NOT touch Event BeginPlay, the Think custom event, or the ATTACK / CHASE /
RETURN / IDLE_HOME / IDLE_WAIT / NO_PLAYER branches.
Do NOT touch K2Node_Self_1 or its single link to K2Node_CallFunction_49
(ApplyDamage . DamageCauser).
Do NOT change any default value.
Compile BP_Enemy and save it.

=====================================================================
PART B - /Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter
=====================================================================

B1 - add one variable.
  A float member variable named AttackDamage, default value 34.0,
  instance-editable (eye icon ON). Add no other variable.
  Compile so it exists on the generated class, then set the default to 34.0
  and read it back.

B2 - extend the existing attack hit chain. Today it ends like this:
    K2Node_CallFunction_83  SphereTraceForObjects   at (950, 6300)
      OutHit -> K2Node_CallFunction_84  BreakHitResult  at (1400, 6600)
                  HitActor -> K2Node_CallFunction_85 GetDisplayName (1750,6700)
      then/ReturnValue -> K2Node_IfThenElse_12  Branch  at (1400, 6300)
        then -> K2Node_CallFunction_86  PrintString  at (2300, 6300)
    K2Node_CallFunction_86's "then" pin is not connected to anything.

  Append ApplyDamage AFTER the existing PrintString. Keep the PrintString and
  everything feeding it exactly as it is - it is the current debug readout.

  New nodes:
    ApplyDamage        at (2750, 6300)
    Get AttackDamage   at (2500, 6500)
    GetController      at (2500, 6650)   - leave its self pin EMPTY
    Self               at (2500, 6800)

  Wiring:
    K2Node_CallFunction_86 . then          -> ApplyDamage . execute
    K2Node_CallFunction_84 . HitActor      -> ApplyDamage . DamagedActor
       (reuse the EXISTING HitActor pin - it already feeds GetDisplayName.
        Do not create a second BreakHitResult.)
    Get AttackDamage                       -> ApplyDamage . BaseDamage
    GetController                          -> ApplyDamage . EventInstigator
    Self                                   -> ApplyDamage . DamageCauser

Do NOT touch ShowHUDMessage, RefreshHeldItem, TryAddItem, TryConsumeSelected,
ToggleCameraView, Move, Aim or CanJumpInternal.
Do NOT touch the Event AnyDamage chain that already exists on the player.
Do NOT touch K2Node_Self_0 at (-620, -220) - create a new local Self node
instead, so no wire crosses the graph.
Do NOT change any existing default value: MaxHP 100, RespawnDelay 2,
AttackRange 200, AttackTraceRadius 40, InteractDistance, the pitch limits.
Do NOT change CurrentHP's default of 75 - it looks wrong but it is out of
scope for this command.
Compile BP_ThirdPersonCharacter and save it.

=====================================================================
REPORT
=====================================================================
 R1. BP_Enemy: the new AnyDamage chain read back node by node with
     get_node_infos, including which pin feeds the Append and the Branch
 R2. BP_Enemy: confirm the DestroyActor self pin is EMPTY
 R3. BP_Enemy: EventGraph node count before and after
 R4. BP_Enemy: confirm Event BeginPlay still ends with the Think call and that
     Set CurrentHP is still between Set LastSeenTime and Think
 R5. BP_ThirdPersonCharacter: the variable list, and AttackDamage's default
     read back
 R6. BP_ThirdPersonCharacter: the attack chain from SphereTraceForObjects to
     ApplyDamage read back node by node, with every ApplyDamage input pin and
     what feeds it
 R7. BP_ThirdPersonCharacter: confirm PrintString K2Node_CallFunction_86 still
     exists and still receives the same InString it did before
 R8. both compile results with any warning text verbatim
 R9. both save results
```

**명령 4 — 인스턴스의 덮어쓴 `MaxHP` 지우기**

```
In the currently loaded level /Game/ThirdPerson/Lvl_ThirdPerson, fix one
per-instance property override on the placed enemy.

The actor is labelled "Enemy_Test", object name
  BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879

It currently holds MaxHP = 0 as a per-instance override, while the Blueprint
class default is MaxHP = 100. The instance captured 0 at the moment the
variable was created, before the class default was raised to 100, and a class
default does not propagate to an instance that already holds its own value.

Do NOT write 100 onto the instance. RESET the override instead, using
ObjectTools.reset_properties, so the instance inherits the class default and
will keep following it if the class default changes again later.

Reset exactly one property on that actor: MaxHP.

Do NOT reset or change CurrentHP - it is runtime state, filled at BeginPlay.
Do NOT reset AttackMontage - the instance override there is deliberate and is
the ONLY thing making the enemy play its attack animation, because the class
default for AttackMontage is None.
Do NOT reset AttackDamage, AttackCooldown, SightRange, SightHalfAngle,
ReturnDelay, ReturnSightRange, ReturnStepDistance, HomeArriveRadius or
ThinkInterval - they already match the class default and must stay untouched.
Do NOT change any transform.
Do NOT touch any Blueprint graph, any variable definition, or any other actor.

STEP 0. Read and report, side by side:
   - the class defaults on /Game/Enemy/BP_Enemy for MaxHP, CurrentHP,
     AttackDamage, AttackCooldown, SightRange, SightHalfAngle, ReturnDelay,
     AttackMontage
   - the same properties on the Enemy_Test instance
STEP 1. Reset MaxHP on the instance.
STEP 2. Read the same property set back on the instance and report it.
STEP 3. Save the level.

REPORT:
 R1. the STEP 0 side-by-side reading, verbatim
 R2. the reset call and what it returned
 R3. the STEP 2 reading - confirm the instance now reads MaxHP 100
 R4. confirm the instance still reads AttackMontage = AM_Enemy_Attack.
     If this came back None, say so loudly - the reset hit the wrong property
 R5. confirm AttackDamage 10, AttackCooldown 1.5, SightRange 1200,
     SightHalfAngle 60, ReturnDelay 7 are all unchanged on the instance
 R6. the save result, including any "Failed to save 'Enemy_Test'" warning
     quoted verbatim - that warning appeared once already at 14:28:40
```

**명령 5 — `AttackMontage`를 클래스 기본값으로 올리기**

```
In /Game/Enemy/BP_Enemy, move the attack montage from a per-instance override
up to the class default, then drop the now-redundant override.

Today:
  class default (CDO)   AttackMontage = None
  Enemy_Test instance   AttackMontage = /Game/Characters/Mannequins/Anims/
                                        Unarmed/Attack/AM_Enemy_Attack.AM_Enemy_Attack

The instance override is the ONLY reason the enemy plays its attack animation.
Any second enemy placed or spawned from this Blueprint would get None.

Behaviour must not change. At every step of this command the Enemy_Test
instance must still resolve to AM_Enemy_Attack - first from its own override,
then, after STEP 3, inherited from the class default.

STEP 0. Read and report both:
   - AttackMontage on the class default /Game/Enemy/BP_Enemy
   - AttackMontage on the placed actor labelled "Enemy_Test",
     object name BP_Enemy_C_UAID_9C6B005AF8693AFD02_1187327879

STEP 1. Set the CLASS DEFAULT AttackMontage to
     /Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Enemy_Attack.AM_Enemy_Attack
   Do this on the Blueprint's default object, not on the instance.

STEP 2. Read BOTH the class default and the instance back and report them.
   The instance must still read AM_Enemy_Attack at this point - it still has
   its own override. If the instance reads None here, STOP and report.

STEP 3. Reset the AttackMontage override on the Enemy_Test instance with
   ObjectTools.reset_properties, so the instance inherits the class default
   instead of carrying its own copy.
   Reset exactly one property: AttackMontage.

STEP 4. Read BOTH back again and report them. Both must read AM_Enemy_Attack.
   If the instance reads None after the reset, STOP and report loudly - that
   would mean STEP 1 did not stick.

Do NOT touch MaxHP, CurrentHP, AttackDamage, AttackCooldown, AttackRange,
SightRange, SightHalfAngle, ThinkInterval, ReturnDelay, ReturnSightRange,
ReturnStepDistance or HomeArriveRadius on either the class or the instance.
The instance was just reset to inherit MaxHP 100 - do not disturb that.
Do NOT touch any Blueprint graph or node.
Do NOT touch any other actor or any transform.
Do NOT touch BP_ThirdPersonCharacter or DT_Items.

STEP 5. Compile and save BP_Enemy, and save the level.

REPORT:
 R1. the STEP 0 reading of both
 R2. the STEP 2 reading of both
 R3. the reset call and what it returned
 R4. the STEP 4 reading of both - state plainly whether the instance still
     resolves to AM_Enemy_Attack
 R5. confirm MaxHP still reads 100 on BOTH class and instance
 R6. the compile result and both save results, with any
     "Failed to save 'Enemy_Test'" warning quoted verbatim
```

**옮기며 AI가 해석을 넣은 곳 여섯.**

1. **`Divider_Top`이라는 이름과 리네임 순서** (명령 1). 사용자는 선택지에서 "L / R / Top으로 고침"을 골랐지만, 어느 조각이 Top인지와 두 번의 리네임 순서는 AI가 정했다. `L`/`R`의 기준도 "+X 방향으로 걸어 들어가는 사람"으로 AI가 정했다.
2. **`CurrentHP`의 기본값 `0`** (명령 2). 사양에 적었지만 사용자가 말한 값은 아니다. `100`으로 두면 `BeginPlay`의 대입이 있으나 마나가 된다.
3. **`Think`를 `(2900, 3554)`로 옮긴 것과 새 노드 좌표 전부** (명령 2, 3).
4. **`PrintString`을 지우지 않고 뒤에 `ApplyDamage`를 붙인 것** (명령 3). 이월 메모는 "`PrintString`을 `ApplyDamage`로 올려야"라고 적혀 있었으나, 디버그를 남기기로 한 결정에 맞춰 교체가 아니라 추가로 했다.
5. **적 `PrintString`의 `Key`를 `None`으로 둔 것** (명령 3). 적의 다른 프린트는 `1_state`·`2_dist` 같은 키가 있어 제자리에서 덮어쓴다. 피격은 사건이라 매번 새 줄로 남아야 타격 수를 셀 수 있다.
6. **명령 5의 STEP 3에서 인스턴스 덮어쓰기를 지운 것.** 사용자는 "고치고하자"라고만 했다. 클래스 기본값만 올려도 동작은 같지만 같은 값이 두 군데 남아, 나중에 클래스를 바꿔도 이 인스턴스가 안 따라오는 상태가 유지된다.

**AI가 직접 MCP로 한 조사 호출.** 쓰기는 전부 사용자의 Terminal로 넘겼다.

```
editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script   (다수)
editor_toolset.toolsets.blueprint.BlueprintTools.find_nodes / get_node_infos / list_variables
editor_toolset.toolsets.object.ObjectTools.get_properties / get_class
editor_toolset.toolsets.scene.SceneTools.find_actors
editor_toolset.toolsets.actor.ActorTools.get_actor_transform
editor_toolset.toolsets.data_table.DataTableTools.get_rows
EditorToolset.EditorAppToolset.IsPIERunning
EditorToolset.LogsToolset.GetLogEntries
```

## Terminal 결과

### 원문 — English

**칸막이 세 조각의 실제 좌표 — 이름을 틀리게 붙인 근거가 된 읽기**

```
Divider_L   loc (1800, -2000,   0)   scale (2, 19, 2)
Divider_M   loc (1800,   100,   0)   scale (2, 19, 2)
Divider_R   loc (1900, -2000, 200)   scale (1, 40, 2)
```

**적의 클래스 기본값과 레벨 인스턴스가 어긋나 있던 것 — 한 대에 죽은 원인**

```
CDO_enemy: {"MaxHP":100,"CurrentHP":0,"AttackDamage":10,"AttackMontage":"None"}
instance : {"MaxHP":0,"CurrentHP":0,"AttackDamage":10,"AttackCooldown":1.5,
            "SightRange":1200,"SightHalfAngle":60,"ReturnDelay":7,
            "AttackMontage":{"refPath":"/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Enemy_Attack.AM_Enemy_Attack"}}
```

**한 대에 죽은 PIE 로그 — 같은 프레임에 타격 하나, HP 하나**

```
14.36.03:996 f525 Hit: Enemy_Test
14.36.03:997 f525 EnemyHP: 0.0
```

그 직후로 상태 프린트가 한 줄도 안 나왔다.

```
14.36.03:176 CHASE
14.36.03:493 CHASE
14.36.03:801 CHASE
14.36.03:997 EnemyHP: 0.0
```

**`Enemy_Test` 저장 실패 — 전문**

```
[2026.09.01-14.28.40:509][769]LogScript: Warning: Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/0/KM/MV2KKKYMIZ9A43Y7GVWSU9
[2026.09.01-14.28.40:509][769]LogScript: Warning: Failed to save 'Enemy_Test'.
```

**PIE 중 `find_actors`가 빈 결과를 준 것**

```
{"CDO": "{\"MaxHP\":100,\"CurrentHP\":0,\"AttackDamage\":10}", "instance": []}
```

같은 순간의 PIE 상태.

```
{"returnValue":true}
```

**`LogJson` 경고 — AI의 `get_properties` 호출이 부른 것, 10줄 중 4줄 발췌**

```
[2026.09.01-14.15.30:679][471]LogJson: Warning: Property "OnActorBeginOverlap" type FActorBeginOverlapSignature unhandled during Json schema generation.
[2026.09.01-14.15.30:679][471]LogJson: Warning: Property "OnTakeRadialDamage" type FTakeRadialDamageSignature unhandled during Json schema generation.
[2026.09.01-14.15.30:679][471]LogJson: Warning: Property "OnTakePointDamage" type FTakePointDamageSignature unhandled during Json schema generation.
[2026.09.01-14.15.30:679][471]LogJson: Warning: Property "OnTakeAnyDamage" type FTakeAnyDamageSignature unhandled during Json schema generation.
```

**`LogCrowdFollowing` — PIE 종료 무렵 또 나옴**

```
[2026.09.01-14.23.11:512][324]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
```

**컴파일 — 이번 세션의 다섯 번 전부 진단 없음**

```
[2026.09.01-14.13.15:340][ 45]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.01-14.13.15:429][ 45]LogUObjectHash: Compacting FUObjectHashTables data took   1.56ms
[2026.09.01-14.14.44:007][331]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.01-14.14.44:087][331]LogUObjectHash: Compacting FUObjectHashTables data took   1.95ms
[2026.09.01-14.27.49:230][533]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
[2026.09.01-14.29.30:170][918]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.09.01-14.30.39:063][229]LogBlueprint: Compiling Blueprint '/Game/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.BP_ThirdPersonCharacter'
[2026.09.01-14.58.52:127][572]LogBlueprint: Compiling Blueprint '/Game/Enemy/BP_Enemy.BP_Enemy'
```

**고친 뒤의 PIE — 세 대에 죽는 것**

```
14.48.47:287 f955 Hit: Enemy_Test
14.48.47:287 f955 EnemyHP: 66.0
14.48.50:001 f176 Hit: Enemy_Test
14.48.50:001 f176 EnemyHP: 32.0
14.48.52:794 f402 Hit: Enemy_Test
14.48.52:794 f402 EnemyHP: 0.0
```

같은 판의 상태 전이. 마지막 줄 뒤로 아무것도 안 찍혔고, 그때 PIE는 계속 켜져 있었다.

```
14.48.36:976 IDLE_HOME
14.48.46:000 CHASE
14.48.47:549 ATTACK
14.48.49:058 IDLE_WAIT
14.48.49:674 CHASE
14.48.49:979 ATTACK
14.48.51:486 CHASE
14.48.52:715 ATTACK
```

**두 대만 맞고 살아서 복귀한 판**

```
14.51.42:497 IDLE_HOME
14.51.51:326 CHASE
14.51.52:869 Hit: Enemy_Test
14.51.52:869 EnemyHP: 66.0
14.51.52:887 ATTACK
14.51.54:393 IDLE_WAIT
14.51.55:619 CHASE
14.51.57:443 ATTACK
14.51.58:947 CHASE
14.51.59:520 Hit: Enemy_Test
14.51.59:520 EnemyHP: 32.0
14.51.59:553 ATTACK
14.52.01:058 CHASE
14.52.02:900 IDLE_WAIT
14.52.09:679 RETURN
14.52.14:296 IDLE_HOME
```

**명령 5 이후의 클래스/인스턴스 일치**

```
class_default: {"AttackMontage":{"refPath":"/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Enemy_Attack.AM_Enemy_Attack"},"MaxHP":100,"CurrentHP":0,"AttackDamage":10,"AttackCooldown":1.5,"AttackRange":150,"SightRange":1200,"SightHalfAngle":60,"ThinkInterval":0.29999999999999999,"ReturnDelay":7,"ReturnSightRange":300,"ReturnStepDistance":300,"HomeArriveRadius":100}
instance     : {"AttackMontage":{"refPath":"/Game/Characters/Mannequins/Anims/Unarmed/Attack/AM_Enemy_Attack.AM_Enemy_Attack"},"MaxHP":100,"CurrentHP":0,"AttackDamage":10,"AttackCooldown":1.5,"AttackRange":150,"SightRange":1200,"SightHalfAngle":60,"ThinkInterval":0.29999999999999999,"ReturnDelay":7,"ReturnSightRange":300,"ReturnStepDistance":300,"HomeArriveRadius":100}
```

**애셋 클래스 조회 — 사망·피격 애니메이션이 몽타주가 아니라는 것**

```
{"MM_Death_Front_01": "/Script/Engine.AnimSequence",
 "MM_HitReact_Front_Lgt_01": "/Script/Engine.AnimSequence",
 "AM_Enemy_Attack": "/Script/Engine.AnimMontage",
 "AM_Player_Attack": "/Script/Engine.AnimMontage"}
```

### 요약 — 한글

- 레벨 액터 라벨 둘이 바뀌었다. `Divider_R` → `Divider_Top`, `Divider_M` → `Divider_R`. `Divider_L`은 무변경. 세 액터의 트랜스폼은 리네임 전 읽어둔 값과 하나까지 같다
- `BP_Enemy`에 `MaxHP`(Float, 100) · `CurrentHP`(Float, 0) 두 변수가 생겼다. 변수 15개 → 17개
- `BP_Enemy`의 `EventBeginPlay` 체인에 `Set CurrentHP = Get MaxHP`가 `Set LastSeenTime`과 `Think` 사이에 끼워졌다. `Think`는 `(2520, 3554)` → `(2900, 3554)`로 이동
- `BP_Enemy`에 `Event AnyDamage` 체인이 생겼다. `Clamp(CurrentHP - Damage, 0, MaxHP)` → `PrintString("EnemyHP: " + …)` → `Branch(CurrentHP <= 0)` → `DestroyActor`. 노드 12개. `EventGraph` 100 → 112
- `BP_ThirdPersonCharacter`에 `AttackDamage`(Float, 34)가 생겼다. 변수 15개 → 16개
- `BP_ThirdPersonCharacter`의 공격 체인에서 `PrintString`(`K2Node_CallFunction_86`) 뒤에 `ApplyDamage`(`K2Node_CallFunction_61`)가 붙었다. `DamagedActor`는 기존 `BreakHitResult`(`K2Node_CallFunction_84`)의 `HitActor` 핀 재사용, `BaseDamage`는 `GetAttackDamage`, `EventInstigator`는 `GetController`(self 핀 빔), `DamageCauser`는 새 로컬 `Self` 노드(`K2Node_Self_1`, `(2500, 6800)`). `EventGraph` 143 → 147
- `Enemy_Test` 인스턴스의 `MaxHP` 덮어쓰기가 지워져 클래스 기본값 100을 상속한다
- `BP_Enemy`의 클래스 기본값 `AttackMontage`가 `None` → `AM_Enemy_Attack`이 되고, `Enemy_Test`의 같은 덮어쓰기가 지워졌다. 읽은 13개 프로퍼티가 클래스와 인스턴스에서 전부 같다
- `git status` 기준 바뀐 파일 다섯 — `Content/Enemy/BP_Enemy.uasset`, `Content/ThirdPerson/Blueprints/BP_ThirdPersonCharacter.uasset`, `Content/__ExternalActors__/ThirdPerson/Lvl_ThirdPerson/` 아래 `.uasset` 셋 (`0/KM` = `Enemy_Test`, `6/8I`·`D/5R` = 칸막이 둘)

## 분석

### 무엇을 만들었나

**레벨 — 라벨 둘**

| 오브젝트 | 이전 라벨 | 새 라벨 | 실제 범위 |
|---|---|---|---|
| `..._1961959730` | `Divider_L` | `Divider_L` (무변경) | X 1800..2000, Y -2000..-100, Z 0..200 |
| `..._1392108111` | `Divider_M` | **`Divider_R`** | X 1800..2000, Y 100..2000, Z 0..200 |
| `..._1961956726` | `Divider_R` | **`Divider_Top`** | X 1900..2000, Y -2000..2000, Z 200..400 |

문간은 `X 1800..2000, Y -100..100, Z 0..200`, 폭 200.

**`BP_Enemy` — 변수 둘**

| 변수 | 타입 | 기본값 | 인스턴스 편집 |
|---|---|---|---|
| `MaxHP` | Float | 100.0 | 켬 |
| `CurrentHP` | Float | 0.0 | 끔 |

**`BP_Enemy` — `EventBeginPlay` 체인 (변경 후)**

```
K2Node_Event_0         Event BeginPlay      (0, 3554)
K2Node_VariableSet_10  Set PlayerRef        (560, 3554)
K2Node_VariableSet_11  Set HomeLocation     (1120, 3554)
K2Node_VariableSet_12  Set HomeRotation     (1680, 3554)
K2Node_VariableSet_13  Set LastSeenTime     (2240, 3554)
K2Node_VariableSet_0   Set CurrentHP        (2520, 3554)   신규
   └ K2Node_VariableGet_0  Get MaxHP        (2440, 3700)   신규
K2Node_CallFunction_82 Think                (2900, 3554)   이동
```

**`BP_Enemy` — `Event AnyDamage` 체인 (신규, 노드 12개)**

```
K2Node_Event_1                       Event AnyDamage        (0, 4100)
K2Node_VariableGet_1                 Get CurrentHP          (350, 4420)
K2Node_PromotableOperator_6          float-float            (620, 4360)
    A <- Get CurrentHP,  B <- Event.Damage
K2Node_VariableGet_2                 Get MaxHP              (620, 4600)
K2Node_CallFunction_0                Clamp(Float)           (880, 4360)
    Value <- 뺄셈,  Min 0.0,  Max <- Get MaxHP
K2Node_VariableSet_1                 Set CurrentHP          (1150, 4100)
K2Node_CallFunction_1                ToString(Float)        (1450, 4420)
    InDouble <- Set CurrentHP 의 Output_Get
K2Node_CommutativeAssociativeBinaryOperator_0  Append       (1700, 4320)
    A "EnemyHP: ",  B <- ToString
K2Node_CallFunction_2                PrintString            (2020, 4100)
    Screen true, Log true, Duration 2.0, Key None
K2Node_PromotableOperator_7          float<=float           (2020, 4560)
    A <- Set CurrentHP 의 Output_Get,  B 0.0
K2Node_IfThenElse_4                  Branch                 (2400, 4100)
K2Node_CallFunction_3                DestroyActor           (2700, 4100)
    self 핀 빔
```

**`BP_ThirdPersonCharacter` — 변수 하나**

| 변수 | 타입 | 기본값 | 인스턴스 편집 |
|---|---|---|---|
| `AttackDamage` | Float | 34.0 | 켬 |

**`BP_ThirdPersonCharacter` — 공격 체인 꼬리 (신규 노드 4개)**

```
K2Node_CallFunction_86  PrintString    (2300, 6300)   기존, 그대로
  then -> K2Node_CallFunction_61  ApplyDamage        (2750, 6300)   신규
      DamagedActor    <- K2Node_CallFunction_84 . HitActor   기존 핀 재사용
      BaseDamage      <- K2Node_VariableGet_26  Get AttackDamage  (2500, 6500)  신규
      EventInstigator <- K2Node_CallFunction_62  GetController     (2500, 6650)  신규, self 빔
      DamageCauser    <- K2Node_Self_1                            (2500, 6800)  신규
      DamageTypeClass 비어 있음
```

**클래스 기본값 정리**

| | 이전 | 이후 |
|---|---|---|
| `BP_Enemy` CDO `AttackMontage` | `None` | `AM_Enemy_Attack` |
| `Enemy_Test` `AttackMontage` | 덮어쓰기 있음 | 상속 |
| `Enemy_Test` `MaxHP` | 덮어쓰기 `0` | 상속 (`100`) |

### 기술적으로 맞게 짚은 부분

**죽음을 상태가 아니라 액터의 소멸로 본 것.** `isDead` 불리언을 만들고 `Think`의 모든 분기 앞에 검사를 넣는 방식이 흔한 답이지만, 이 사양에서는 필요가 없었다. `DestroyActor`가 액터를 지우면 대기 중인 `Delay`의 래턴트 액션이 액터와 함께 취소되어 `Think` 루프가 저절로 끊긴다. 결정 사다리 1번("안 만들어도 되는가")에서 멈춘 항목이고, PIE 로그가 이를 증명했다 — `EnemyHP: 0.0` 이후 PIE가 켜져 있는 채로 상태 프린트가 한 줄도 안 나왔다. 변수 하나와 분기 다섯 개를 안 만들었다.

**뺄셈은 새 게터에서, 출력은 `Set` 노드에서 읽게 나눈 것.** `Clamp(CurrentHP - Damage, ...)`의 `CurrentHP`는 **쓰기 전** 값이어야 하고, `PrintString`과 `Branch`의 `CurrentHP`는 **쓴 뒤** 값이어야 한다. 둘 다 `Get CurrentHP` 노드로 읽으면 블루프린트의 실행 순서에 따라 어느 쪽이 나올지 보장되지 않는다. `Set` 노드의 `Output_Get` 핀은 방금 쓴 값을 돌려주므로 이 구분이 명시적으로 표현된다.

**끊기 전에 목적지 핀의 이름을 확인하게 한 것 — 이번에도 값을 했다.** 명령 5에서 `AttackMontage`를 클래스로 올릴 때 순서를 "클래스 먼저 채우고 → 확인하고 → 그 다음에 인스턴스 덮어쓰기 삭제"로 못박았다. 반대로 했으면 인스턴스가 잠시 `None`을 상속하는 구간이 생기고, 그 사이에 `set_properties`가 실패하면 적이 공격 애니메이션을 잃은 채로 남는다.

**인스턴스에 `100`을 쓰지 않고 덮어쓰기를 리셋한 것.** `MaxHP`를 인스턴스에 직접 써넣었으면 지금 동작은 같지만 덮어쓰기가 그대로 남아, 다음에 클래스 기본값을 바꿀 때 또 안 따라온다. `reset_properties`로 지우니 `git status`에서 그 액터 파일이 목록에서 사라졌다 — 파일 내용이 원래 커밋된 상태로 돌아갔다는 뜻이고, 덮어쓰기가 정말 없어졌다는 증거다.

**로그의 프린트 순서로 원인을 좁힌 것.** "한 대에 죽었다"는 관찰에서 `MaxHP` 인스턴스 값이 0이라는 결론까지, PIE 로그만으로 갔다. 사슬은 이렇다 — `CHASE`가 찍혔다 → `Think`가 돌았다 → `Think`는 `BeginPlay` 체인에서 `Set CurrentHP` 바로 뒤다 → `Set CurrentHP`는 확실히 실행됐다 → 따라서 피격 직전 `CurrentHP == MaxHP` → 34 데미지에 결과가 0이면 `MaxHP ≤ 34` → CDO는 100이니 인스턴스가 다르다. 노드를 하나도 안 고치고 원인이 나왔다.

**`Hit:`과 `EnemyHP:`가 같은 프레임(f525)에 하나씩만 찍힌 것을 확인한 것.** "한 대에 죽었다"의 다른 가설은 "한 번 휘두를 때 여러 번 맞는다"였다. 프레임 번호까지 보고 각각 한 줄인 것을 확인해서 그 갈래를 잘랐다. 이걸 안 봤으면 트레이스나 노티파이 쪽을 헛되이 팠을 것이다.

**손대지 않은 것이 옳았던 것 둘.** 플레이어의 `CurrentHP 75`를 이번 명령에서 명시적으로 금지했다 — 고쳐야 할 값으로 보이지만 이번 사양의 범위가 아니고, 같은 커밋에 섞으면 무엇이 무엇을 고쳤는지 흐려진다. `ReturnStepDistance`도 여전히 안 지웠다.

### 확인한 것 / 확인 못 한 것

**확인한 것**

- **라벨 셋이 `Divider_L` / `Divider_R` / `Divider_Top`.** 각 이름으로 `find_actors`를 돌려 정확히 하나씩 잡혔고, `Divider_M`과 `SM_Cube17`은 0개다
- **세 액터의 트랜스폼이 리네임 전과 값 하나까지 같다.** 이번에는 리네임 **전에** 좌표를 읽어뒀기 때문에 값 대 값 대조가 됐다
- **외부 액터 파일이 정확히 둘만 바뀌었다.** 리네임한 액터 수와 일치한다
- **`MaxHP` 100, `CurrentHP` 0으로 되읽힘.** MCP로 다시 읽었다
- **`Get MaxHP` 게터가 진짜 `MaxHP`를 읽는다.** `K2Node_VariableGet_0`의 `type_id`가 `|GetMaxHP`이고 출력이 `Set CurrentHP`로 간다
- **`Think`가 여전히 `BeginPlay` 체인의 마지막.** 체인을 노드별로 다시 읽었다
- **`BeginPlay`를 건드려도 `Think` 루프가 안 깨졌다.** PIE에서 `IDLE_HOME → CHASE → IDLE_WAIT → RETURN → IDLE_HOME`이 그대로 났고 대기 6.778초였다
- **`Event AnyDamage` 체인이 사양대로다.** 12개 노드를 전부 다시 읽었고, 뺄셈이 `Get CurrentHP`에서, `Append`와 `Branch`가 `Set` 노드의 `Output_Get`에서 오는 것을 확인했다
- **`DestroyActor`의 `self` 핀이 비어 있다**
- **`ApplyDamage`의 네 입력 핀이 전부 의도한 소스에서 온다.** `K2Node_VariableGet_26`이 `|GetAttackDamage`, `K2Node_CallFunction_62`가 `Pawn|GetController`(self 빔), `K2Node_Self_1`이 `(2500, 6800)`의 새 노드임을 각각 확인했다
- **`K2Node_Self_0`(-620, -220)이 안 건드려졌다.** 여전히 `K2Node_Message_1`만 먹인다
- **`PrintString`(`K2Node_CallFunction_86`)이 살아 있고 `InString`도 그대로다**
- **노드 수가 예측대로 늘었다.** `BP_Enemy` 98 → 100 → 112, `BP_ThirdPersonCharacter` 143 → 147
- **컴파일 다섯 번 전부 진단 없음.** 컴파일 줄과 그 다음 줄 사이에 아무것도 안 찍혔다
- **인스턴스 `MaxHP`가 0이었다.** 가설을 세운 뒤 실제로 읽어서 확정했다
- **리셋 후 인스턴스 `MaxHP` 100, `AttackMontage`는 `AM_Enemy_Attack` 유지**
- **합격 기준 1 — 한 대에 `EnemyHP: 66.0`.** `100 - 34`. 이것이 `BeginPlay` 초기화도 같이 증명한다
- **합격 기준 2 — 세 대에 사라짐.** `66.0 → 32.0 → 0.0`
- **합격 기준 3 — 죽은 뒤 상태 프린트가 멈춤.** PIE가 켜져 있는 채로 마지막 블루프린트 메시지가 `EnemyHP: 0.0`이었다
- **합격 기준 4 — 두 대만 맞고 살아서 복귀.** HP 32로 `IDLE_WAIT` 6.779초 뒤 `RETURN`, 4.617초 뒤 `IDLE_HOME`
- **명령 5 이후 클래스와 인스턴스의 13개 프로퍼티가 전부 같다**
- **적의 공격 애니메이션이 명령 5 이후에도 나온다.** 사용자가 PIE에서 눈으로 확인했다
- **`MM_Death_*`와 `MM_HitReact_*`는 `AnimSequence`, `AM_*`만 `AnimMontage`다.** `get_class`로 읽었다
- **에디터 월드에 배치된 `BP_ThirdPersonCharacter` 인스턴스가 없다.** `PlayerStart`에서 스폰되므로 인스턴스 값 굳는 함정에 안 걸린다

**확인 못 한 것**

- **`MaxHP`·`CurrentHP`·`AttackDamage`의 인스턴스 편집 아이콘.** MCP에 읽는 수단이 없다. 화면으로 봐야 한다
- **`Divider_L` / `R` / `Top`이 사람이 보기에도 맞는 방향인지.** `L`/`R`은 "+X 방향으로 걸어 들어가는 사람" 기준으로 AI가 정한 것이고, 실제로 플레이어가 그 방향으로 들어가는지는 안 봤다
- **`AttackDamage`가 정확히 34로 전달되는지.** `EnemyHP: 66.0`이 `100 - 34`와 맞지만, `100 - 34`를 만드는 다른 조합을 배제한 것은 아니다. 다만 `66 → 32`도 34 차이라 사실상 확인된 것에 가깝다
- **`Enemy_Test` 저장이 14:28:40에 왜 실패했는지.** `Asset does not exist`라는데 파일은 디스크에 있다. 그 뒤로는 안 났다
- **그 실패로 무엇을 잃었는지.** 인스턴스에 새로 덮어쓴 값이 없어서 실무상 잃은 게 없어 보이지만, "없다"고 단언할 근거는 없다
- **`0/KM/MV2KKKYMIZ9A43Y7GVWSU9`가 `Enemy_Test`라는 것은 로그의 실패 메시지로 알았다.** 정상 경로로 GUID와 액터를 대응시키는 방법은 모른다

### 남는 리스크

- **플레이어 `CurrentHP`의 기본값이 75다.** PIE를 시작하면 체력이 75에서 시작한다. 이번 명령에서 명시적으로 안 건드렸다
- **사망·피격 연출이 없다.** 적은 그 자리에서 사라진다. `MM_Death_*`가 `AnimSequence`라 몽타주로 감싸는 손 작업이 필요하다
- **적이 하나뿐이다.** `SphereTraceForObjects`가 `Multi` 버전이 아니라 한 번에 하나만 때린다
- **적 공격은 여전히 무조건 맞는다.** `PlayAnimMontage → ApplyDamage → Delay`다. 플레이어만 트레이스로 판정한다 — 양쪽이 비대칭이다
- **디버그 프린트가 늘었다.** `BP_Enemy`의 `PrintString`이 9 → 10, `ToString(Float)`가 3 → 4. `BP_ThirdPersonCharacter`는 그대로
- **`ApplyDamage`의 `DamageTypeClass`가 비어 있다.** 지금은 데미지 종류를 안 가르지만, 나중에 종류별 처리가 필요해지면 여기부터 봐야 한다
- **`ReturnStepDistance 300`이 여전히 읽히지 않는 값으로 남아 있다**
- **`EditorPerProjectUserSettings.ini` 저장 실패가 여전하다**

### 총평

요청은 접어둔 목록의 본체인 적 HP·피격·사망을 만드는 것이었고, 사양의 합격 기준 넷이 전부 PIE 로그로 증명됐다. 새 애셋 없이, 새 상태 없이, 새 플래그 없이 끝났다.

**실질적 난이도는 노드를 만드는 데 있지 않았다.** `Event AnyDamage` 체인은 플레이어 쪽에 이미 있던 것의 거울상이고, 만드는 데 명령 한 번이면 됐다. 어려웠던 것은 **"한 대에 죽는다"의 원인을 찾는 일**이었고, 그 원인은 AI가 명령을 쓴 방식이 만든 것이었다.

명령 2를 "변수 추가 → 컴파일 → 기본값 설정" 순서로 짰다. 컴파일하는 순간 레벨에 배치된 인스턴스가 그때의 기본값 `0`을 자기 값으로 굳혔고, 그 다음에 CDO를 `100`으로 올려도 인스턴스는 따라오지 않았다. CLAUDE.md가 "부모 BP 기본값을 바꿨다면 이미 덮어쓴 자식·레벨 인스턴스는 따라오지 않는다"고 경고하는 바로 그 경우인데, **경고를 읽고도 명령을 그 함정에 정확히 맞춰 썼다.**

더 나쁜 것은 검증이었다. 명령 2의 `R2`가 CDO만 되읽게 되어 있었다. 인스턴스를 같이 읽는 한 줄만 있었으면 그 자리에서 잡혔고, 사용자가 "한대맞고 죽은거같은데"를 알아채기 전에 끝났을 것이다. **되읽기를 요구한 것은 맞았고, 무엇을 되읽을지 좁게 잡은 것이 틀렸다.**

건진 것도 있다. 원인 추적이 로그만으로 끝났다는 점이다. 노드를 고쳐보고 돌려보는 반복 없이, 프린트 순서와 프레임 번호만으로 "인스턴스의 `MaxHP`가 0"까지 좁혔고 그 다음에 딱 한 번 읽어서 확정했다. 그리고 그 사고 덕에 `AttackMontage`의 같은 함정을 **터지기 전에** 찾아 고쳤다 — `MaxHP`로 한 번 데지 않았으면 그건 적을 둘로 늘리는 날까지 안 보였을 것이다.

## AI의 제안

1)
```
Rename all three divider pieces to match what they actually are, not
Divider_L / M / R:
  "Divider_R"  ->  "Divider_Top"   (the header above the doorway)
  "Divider_M"  ->  "Divider_R"     (the +Y jamb)
  "Divider_L"  ->  unchanged       (the -Y jamb)
```
얻는 것 — 이름이 배치를 맞게 말한다. 잃는 것 — 같은 액터의 라벨이 하루에 두 번 바뀌었다. 과거 기록의 `SM_Cube2` / `SM_Cube17` / `Divider_M`을 지금 라벨과 대조하려면 두 단계를 거쳐야 한다.

2)
```
Do NOT add any "is dead" flag or new variable. Destroying the actor
cancels the pending Delay in the Think loop, which is what stops it.
```
얻는 것 — 변수 하나와 `Think`의 모든 분기 앞 검사를 안 만든다. 잃는 것 — "왜 루프가 멈추는가"가 그래프에 안 보인다. `DestroyActor`가 래턴트 액션을 취소한다는 엔진 동작을 알아야 읽힌다.

3)
```
Feed the Append and the Branch from the Set CurrentHP node's own output
value pin, not from a fresh Get CurrentHP node. That guarantees they read
the value just written.
```
얻는 것 — "쓰기 전 값"과 "쓴 뒤 값"의 구분이 그래프에 명시된다. 잃는 것 — `Set` 노드에서 선이 셋 나가서 그 부분이 조금 빽빽해진다.

4)
```
Do NOT write 100 onto the instance. RESET the override instead, using
ObjectTools.reset_properties, so the instance inherits the class default and
will keep following it if the class default changes again later.
```
얻는 것 — 튜닝 값의 주인이 한 군데가 된다. 인스턴스 파일이 커밋된 상태로 돌아가 diff도 깨끗해진다. 잃는 것 — 그 인스턴스만 다른 값을 주고 싶어지면 다시 덮어써야 한다.

5)
```
Set the CLASS DEFAULT AttackMontage to AM_Enemy_Attack, then reset the
per-instance override. Do the class first and verify, so the instance never
resolves to None at any point.
```
얻는 것 — 적을 하나 더 놓거나 스폰해도 공격 애니메이션이 나온다. 잃는 것 — 없다. 이 제안은 사용자가 요청한 범위 밖이었고 AI가 먼저 꺼냈다.

## 다음으로 넘김

**바로 이어서 할 것**

없음.

**결정 필요**

- **다음 사양이 무엇인가.** 접어둔 목록에서 가까운 후보는 (1) 적 공격에도 히트 판정 붙이기 — 지금 적만 무조건 맞히므로 양쪽이 비대칭이다, (2) 적 리스폰, (3) 사망 연출
- **플레이어 `CurrentHP`의 기본값 75를 100으로 고칠 것인가.** PIE 시작 체력이 75다. 고칠 때 **배치된 인스턴스가 없으므로** 인스턴스 함정은 안 걸린다
- **디버그 표시 제거 시점.** 이번에 늘었다. 실제 개수는 `BP_Enemy`의 `PrintString` 10개 + `ToString(Float)` 4개, `BP_ThirdPersonCharacter`의 `PrintString` 1개 + `SphereTraceForObjects`의 `DrawDebugType ForDuration` 하나. **`ShowHUDMessage` 안의 `PrintString`은 기능이므로 지우면 안 된다**
- **칼의 회전.** `heldTransform.Rotation`이 단위값이라 막대가 수평으로 몸 앞을 향한다. 값은 PIE에서 봐야 안다
- **`K2Node_Self_1`(`BP_Enemy`)을 `ApplyDamage` 근처로 옮길 것인가.** 남은 장거리 선 하나가 사라진다

**확인 필요**

- **`MaxHP`·`CurrentHP`(`BP_Enemy`)와 `AttackDamage`(플레이어)의 인스턴스 편집 아이콘.** 화면으로 봐야 한다
- **`Enemy_Test` 저장이 14:28:40에 왜 실패했는지, 그리고 그때 무엇을 잃었는지**
- **`__ExternalActors__`의 GUID 파일명과 액터를 대응시키는 정상적인 방법**
- **`AttackDamage` 34가 정확히 34로 전달되는지.** `100 → 66 → 32`가 두 번 다 34 차이라 사실상 확인됐지만 직접 찍어본 것은 아니다
- **`Divider_L` / `R`이 플레이어가 실제로 들어가는 방향 기준으로도 맞는지**
- **PIE 중에는 `find_actors`가 PIE 월드를 본다.** 이번에 죽은 적을 찾다가 빈 배열을 받아서 알았다. 에디터 월드를 읽어야 할 때는 PIE를 먼저 멈춰야 한다
- **`CaptureEditorImage`가 PIE 중에도 되는지.** 되면 "PIE 화면을 못 본다"는 제약이 사라진다
- **`arrange_nodes`가 실제로 어떤 배치를 내는지**
- **`ProgrammaticToolset`으로 코멘트 노드를 만들 수 있는지**
- **`BP_Enemy`의 `PrintString`이 8에서 9로 언제 늘었는지** (이번 작업 전 기준)
- **`BP_ThirdPersonCharacter`의 `PrintString`이 왜 10으로 기록됐었는지.** 실제는 2였다
- **`BP_Enemy`가 왜 `BP_ThirdPersonCharacter` 컴파일에 딸려 dirty가 되는지**
- **`read_graph_dsl`이 그래프를 통째로 안 뱉는다.** `find_nodes`가 143개를 반환하는 그래프에서 DSL은 본문 몇 줄에서 끊겼다
- **MCP가 못 읽는 프로퍼티 목록.** `AttachSocketName`, `attachParent`, `CollisionEnabled`, `Notifies`, `bEnableRootMotionTranslation`, `bEnableRootMotionRotation`, `bRootMotionSettingsCopiedFromMontage`, `SlotGroups`, `SlotToGroupNameMap`, `NewVariables`, `ActorLabel`
- **MCP는 블루프린트 애셋 경로를 항상 CDO로 리다이렉트한다**
- **`ProgrammaticToolset`의 dict가 `_StrictDict`다.** `.get(key, default)`가 막혀 있다
- **`DataTableTools.set_rows`는 `Translation` / `Rotation`(`W` 포함) / `Scale3D`를 받는다.** 쓰기 경로가 `LogCSVImportFactory`를 탄다
- **`LogJson: Warning: Property "..." unhandled during Json schema generation`.** `get_properties`를 Character에 부를 때마다 델리게이트 프로퍼티 열 줄이 찍힌다
- **`LogCrowdFollowing: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance`.** 이번에도 PIE 종료 무렵 났다
- **`LogModelContextProtocol: Error: Call to unknown method "server/discover"`**
- **`EditorPerProjectUserSettings.ini` 저장 실패 (`Error Code 183`)**
- **`read_graph_dsl`과 `write_graph_dsl`의 id 체계가 다른 이유**
- **`find_node_types`와 `get_node_type_pins`의 type_id 표기가 다른 이유**
- **`CaptureViewport`가 PIE 화면이 아니라 에디터 월드를 렌더하는 것**
- **MCP로는 만들 수 없는 노드 목록.** `K2Node_CallParentFunction`, 순수 `IsValid`, `Use Cached Pose`
- **`UpperBody` 슬롯이 원래 있었는지 이번에 추가됐는지**
- **`Use cached pose 'BodyBase'`가 왜 `find_node_types`에 안 떴는지**
- **적이 제자리에서 공격할 때 다리가 멈추는 것이 티가 나는지**
- **`SaveCachedPose 'BodyBase'`의 `NOTE` 배지가 사라졌는지**
- **`ABP_Unarmed`의 `Is Falling` → `NOT` → `ShouldDoIKTrace` 배선이 무엇을 하는지**
- **`MM_ChargedAttack`이 어떤 동작인지**
- **막대의 긴 축 `Y`는 어느 방향인지**
- **재직렬화된 `.uasset`들의 내용이 실제로 안 바뀌었는지**
- **`Knife`의 `displayName` NSLOCTEXT 네임스페이스가 기존 행과 다른 이유**
- **`DisableInput`이 Enhanced Input 매핑까지 막는지**
- **HUD의 `CachedCharacter` 재획득이 실제로 일어나는지**
- **2번 방의 조명**
- **`bCanEverTick`이 명령 56 직후 `false`로 읽혔던 이유**
- **`trace_world`가 방향에 따라 같은 솔리드를 놓치는 이유**
- **`show navigation`이 PIE에서 안 먹는 이유**
- **`__ExternalObjects__` 파일의 정체.** `__ExternalActors__`는 액터 하나가 `.uasset` 하나다
- **`Lvl_ArenaShooter`의 WorldSettings가 `BP_ShooterGameMode`를 가리키는지**

**접어둔 것**

- **적 공격에도 히트 판정 붙이기.** 지금은 `PlayAnimMontage → ApplyDamage → Delay`로 무조건 맞는다. 플레이어는 트레이스로 판정하므로 양쪽이 비대칭이다. 필요한 것 셋 — (1) `PlayAnimMontage`를 `Play Montage`로 교체, (2) `AM_Enemy_Attack`에 `Montage Notify` 찍기(수작업), (3) `ApplyDamage`를 노티파이 분기 뒤 트레이스 성공 쪽으로 옮기기
- **적 리스폰.** `AttackMontage`의 클래스 기본값을 이번에 채웠으므로 스폰된 적도 공격 애니메이션이 나온다
- **적 사망·피격 연출.** `MM_Death_*` 6개와 `MM_HitReact_*` 8개가 있지만 전부 `AnimSequence`다. 몽타주로 감싸는 에디터 손 작업이 필요하고 MCP로는 안 된다
- **적 체력바 위젯 / 순찰 / EQS / 여러 적의 회피 / 적 종류별 DataTable**
- **소리 감지 · 여러 적의 정보 공유 · "뭔가 봤다" 중간 경계 상태**
- **여러 적을 한 번에 때리기.** `SphereTraceForObjects`의 `Multi` 버전으로 노드 하나 교체
- **칼 메시 구하기.** 리타깃 비용이 애셋 고르는 기준에 들어가야 한다. 루트 모션이 켜져 있는지도 봐야 한다
- **칼 궤적 트레이스.** 밑동·칼끝 소켓 사이를 매 프레임 훑는 방식. `Play Montage`의 `OnNotifyEnd` 핀이 비어 있어 `Montage Notify Window`로 바꾸면 그대로 올라간다
- **카메라 작업.** 셋으로 갈렸다
  - **A — 원본 ICI 구조(`캡슐 → Camera → SkeletalMesh`)로 교체.** 팔만 있는 스켈레탈 메시가 프로젝트에 없어 지금 그대로는 못 한다
  - **B — 지금 구조를 두고 팔을 시야로 올린다.** `Variant_Shooter/Anims/ABP_FP_Weapon` + `Ctrl_HandAdjusment`
  - **C — 전환 스냅 완화만.** 요 보간 또는 `SetViewTargetWithBlend`. 2026-08-27부터 이월
- **1인칭으로 죽으면 3인칭으로 부활하는 것.** 사용자가 `내비두자`로 정했다
- **30초 갇힘 사망**
- **사망 시 아이템 드롭**
- **게임오버 화면 · 사망 카운트 · 체크포인트**
- **`BP_ShooterNPC` · `ST_Shooter` · EQS 3개 · StateTree 태스크 6개.** 안 쓰기로 했지만 지우지 않는다
- **`--append-system-prompt`가 저장소에 없다.** `Editor Preferences → General → Terminal → Startup Commands`의 사용자 설정이다. 원문은 `Docs/AI-Log/2026-08-28-inventory-item-data.md`의 `명령` 칸에 있다
- **`BP_Door.uasset`의 재직렬화.** 참조하는 블루프린트를 컴파일하면 딸려 dirty가 된다
- **문간 위 `X 1800..1900, Z 200..400`의 열린 홈.** 이번에 원인이 나왔다 — `Divider_Top`이 X를 `1900..2000`만 덮는데 양옆 벽은 `1800..2000`이다
- **열린 문짝 20cm가 문간 위로 삐져나온다.** 문짝 220, 문간 200
- **`ForLoop.FirstIndex`가 빈 값인 이유.** 동작에 지장이 없다
- **`SP` 스태미나.** 원본에 있고 MCP1에 없다. `06-플레이어-UI.md:54` 참조
- **슬롯 2칸 vs 3칸.** 원본은 2칸, MCP1은 3칸이다
- **미사용 애셋 정리.** 2026-08-30에 **남기기로** 정했다
- **`MoveComponentTo`의 `Stop`·`Return` 핀.** 연타로는 문제가 안 났다
- **칼 픽업이 바닥에 파묻히는 것.** 기존 픽업 6개도 같다
- **`Knife`와 `Key_Stage1`이 같은 메시라 색이 같은 것.** 머티리얼로 가를 수 있다
