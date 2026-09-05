# 2026-09-04

## 작업물

지난 세션이 만들어놓고 눈으로 못 본 횃불 18개를 PIE 스크린샷으로 처음 검증하고, 거기서 나온 세 가지(토치 자기 그림자 · 불꽃 클리핑 · 윗면 색)를 고친 뒤 NavMesh를 사흘 만에 다시 구웠다.

**소요 시간**: 약 2시간 30분. `Docs/Terminal-Log/2026-09-04-56`의 mtime이 `10:24:03`, 마지막 NavMesh 패키지 저장이 `12:24:49`다. 세션 시작 시각은 어디에도 안 남아서 파일 mtime에서 역산한 값이고, 준비 단계는 그 앞에 더 있었다.

## 명령

### 한글

사용자가 입력한 원문을 보낸 순서대로 전부 옮긴다.

```
작업 준비
```

```
이것들봐봐
```
(PIE 스크린샷 2장 첨부)

```
그럼 지금 할 작업 목록 정리하고 하자
```

```
하자
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
이거봐바
```
(PIE 스크린샷 1장 첨부)

```
결과 확인
```

```
이거봐봐
```
(PIE 스크린샷 1장 첨부)

```
결과 확인
```

```
이거봐봐
```
(PIE 스크린샷 2장 첨부)

```
어거봐봐
```
(Base Color 뷰모드 스크린샷 2장 첨부)

```
결과 확인
```

```
이거봐봐
```
(Base Color 1장 + Lit PIE 1장 첨부)

```
봐봐
```
(NavMesh 시각화 스크린샷 4장 첨부)

```
결과 확인
```

```
이거 잘못하고 한번 더 보냈는데 이거어케해
```

```
맨마지막꺼 그래서 그냥 넘어갈까
```

```
이상없음 두 가지 다 잘됨
```

```
근데 적이 로비에 나오면 안되는데 그래서 스테이지 진입 시에 문을 어차피 닫잔아 이거 해야됨?
```

```
이상없음
```

```
기록하고 커밋하고 정리하자
```

선택지로 답한 것 셋도 사용자의 지시다.

- `FlameBrightness`를 얼마로 내릴까 → **`5 (추천)`**
- `TopSurfaceColor` 벡터를 어떻게 할까 → **`0.18로 밝히기 (추천)`**
- 벽 윗면(Z 400)의 NavMesh를 어떻게 할까 → **`천장을 350으로 내린다 (추천)`**

### English — MCP에 실제로 보낸 명령

사용자는 한글로 지시했고, UE Terminal에 넣을 영어 명령은 전부 AI가 옮겨 썼다. 아래가 그 원문 그대로다. 아홉 개이고 번호는 `Docs/Terminal-Log/`의 번호와 같다.

**명령 56 — `BP_Torch`의 `CastShadow` 끄기**

```
In the Unreal project, open the Blueprint /Game/Interaction/BP_Torch and turn OFF shadow casting for three of its static mesh component templates: Backplate, Bracket, and Cup. Set CastShadow to false on each of those three. Do NOT touch the Flame component and do NOT touch the Light (PointLightComponent) component - the point light must keep casting shadows so the torch still lights the room with shadows from walls and props.

Then compile the Blueprint and save it.

After saving, read back and report:
1. The CastShadow value of Backplate, Bracket, Cup, and Flame on the Blueprint's component templates, to confirm the write landed.
2. The CastShadow value of those same four components on ONE placed BP_Torch actor in the currently loaded level Lvl_Stage, so we can tell whether the 18 placed instances inherit the new class default or whether any of them has a per-instance override that ignores it.
3. The full property values of the Light component on that same placed actor: Intensity, IntensityUnits, AttenuationRadius, LightColor, CastShadows/CastShadow, SourceRadius, and Mobility.
4. How many BP_Torch actors exist in Lvl_Stage.

Report the raw tool responses verbatim, including any that returned an error, a warning, or a value that disagrees with what was requested. Do not clean up or summarize the raw output.

Write the report to Docs/Terminal-Log/2026-09-04-56-torch-cast-shadow-off.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

옮기며 넣은 해석: 한글 목록에는 "`Backplate`·`Bracket`·`Cup`"만 있었는데 영어 명령에는 **`Flame`과 `Light`를 건드리지 말라는 금지를 명시적으로 추가**했다. "토치 그림자 끄기"를 광원까지로 읽을 여지를 막은 것이다. 되읽기 4항목도 사용자 지시에 없고, 특히 2번(배치 인스턴스 되읽기)은 CLAUDE.md의 "MCP 응답을 성공 근거로 삼지 않는다"에서 나왔다. 3번(`Light` 값 읽기)은 이번 작업에 필요해서가 아니라 나중에 로비 밝기를 판단할 기준값이 없어서 넣었다.

**명령 57 — 리로드 전 dirty 확인**

```
In the Unreal project, do this in order and stop at the first step that fails.

STEP 1 - Before reloading anything, list every package that is currently dirty (unsaved) in the editor. Report the full list verbatim. If ANY package other than the level itself is dirty, STOP HERE, report the list, and do not reload - I will decide what to do.

STEP 2 - If nothing unexpected is dirty, reload the level /Game/ThirdPerson/Lvl_Stage so its actors are constructed fresh from disk.

STEP 3 - After the reload, find all BP_Torch actors in the level and read CastShadow on the Backplate, Bracket, Cup and Flame components of THREE different torch actors (not just one). Report all twelve values.

I expect Backplate, Bracket and Cup to now read false, matching the Blueprint class default that was changed and saved earlier today. If any of them still reads true after a fresh load, say so plainly - that result is more interesting than the expected one and must not be smoothed over.

STEP 4 - Also report whether reloading the level left any package dirty.

Report the raw tool responses verbatim, including any error or warning, and do not clean up or summarize the raw output.

Write the report to Docs/Terminal-Log/2026-09-04-57-torch-shadow-after-reload.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

옮기며 넣은 해석: 액터 **셋**을 읽으라는 것과, STEP 1의 **정지 조건**은 사용자 지시에 없다. 레벨 리로드가 저장 안 한 변경을 버리므로 안전장치로 넣었다.

**명령 58 — 리로드하고 되읽기**

```
In the Unreal project, do this in order.

CONTEXT - the 18 dirty __ExternalActors__ packages found in the previous task are safe to discard. I verified on disk that Content/__ExternalActors__ is byte-identical to the last git commit, so those packages hold no work of ours; they were dirtied only by the reinstancing that ran when BP_Torch was compiled. Discarding them returns the actors to their committed state, which is what we want.

STEP 1 - Reload the level /Game/ThirdPerson/Lvl_Stage so its actors are constructed fresh from disk, discarding the in-memory state of the 18 external actor packages. If the editor raises a save prompt, a modal dialog, or any error instead of reloading, report exactly what happened and stop.

STEP 2 - After the reload, find all BP_Torch actors in the level. Report how many there are.

STEP 3 - Read CastShadow on the Backplate, Bracket, Cup and Flame components of THREE different torch actors. Report all twelve values.

I expect Backplate, Bracket and Cup to now read false, matching the Blueprint class default. If any of them still reads true after a fresh load, say so plainly and do not smooth it over - that result would mean the old value is stored somewhere other than the actor's own package, and finding where would matter more than the fix.

STEP 4 - Report whether the reload left any package dirty, and how you determined that.

Do NOT write to any actor. Do NOT save the level. This task is a read-back only.

Report the raw tool responses verbatim, including any error or warning, and do not clean up or summarize the raw output.

Write the report to Docs/Terminal-Log/2026-09-04-58-torch-shadow-reload-readback.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

옮기며 넣은 해석: `CONTEXT` 문단으로 **앞 명령의 정지 조건을 AI가 직접 해제**했다. 근거는 `git diff HEAD -- Content/__ExternalActors__`가 비어 있다는 것이고, 사용자 판단이 아니라 AI 판단이다.

**명령 59 — `M_Flame` 읽기**

```
In the Unreal project, do NOT change anything. This is a read-only investigation.

First report whether a PIE session is currently running, since that changes which world the actor reads hit.

I need to understand why the torch flame renders as a featureless white blob instead of showing its FlameColor. Read and report all of the following.

1. The material asset /Game/LevelPrototyping/Materials/M_Flame - read its full node graph: every node, every node's type, and every connection between them. I specifically need to see what is actually plugged into the Emissive Color input of the material output node, and how the FlameColor and FlameBrightness parameters reach it (or whether they reach it at all).

2. The default values of the FlameColor and FlameBrightness parameters on M_Flame, and their parameter types.

3. M_Flame's material settings: Shading Model, Blend Mode, Two Sided, and whether it is set to be used with static meshes.

4. Which material is actually assigned to the Flame static mesh component on the BP_Torch class template - report the full asset path. If it is not M_Flame, say so. Also report whether any material instance of M_Flame exists anywhere in /Game.

5. The Flame component's static mesh asset path and its RelativeScale3D and RelativeLocation on the BP_Torch class template.

Report the raw tool responses verbatim, including any error or warning, and do not clean up or summarize the raw output. If a tool cannot read a material graph, say which tool you tried and what it returned rather than guessing at the graph's contents.

Write the report to Docs/Terminal-Log/2026-09-04-59-flame-material-readout.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

옮기며 넣은 해석: 4번과 5번은 한글 의도("불꽃이 왜 흰가")에 없다. `M_Flame`이 멀쩡한데 메시가 그 재질을 안 쓰고 있을 가능성과, 메시 스케일이 원뿔 실루엣의 원인일 가능성을 같이 잘라내려고 AI가 넣었다.

**명령 60 — `FlameBrightness` `30` → `5`**

```
In the Unreal project, change ONE value and verify it.

Set the DefaultValue of the ScalarParameter named FlameBrightness in the material /Game/LevelPrototyping/Materials/M_Flame from 30 to 5. Do not touch FlameColor, do not touch the Multiply node, do not touch any material setting, and do not create a material instance.

Then recompile the material and save it. The parameter lives on the material itself, not on an instance, so the shader has to be rebuilt for the change to reach the screen - report how long that took and whether any shader compile errors or warnings appeared in the log.

After saving, read back and report:
1. The DefaultValue of the FlameBrightness ScalarParameter, to confirm the write landed.
2. The DefaultValue of the FlameColor VectorParameter, to confirm it was not disturbed. It should still be r 1, g 0.44999998807907104, b 0.11999999731779099, a 1.
3. Whether MP_EmissiveColor is still driven by MaterialExpressionMultiply_0, to confirm the graph was not rewired.
4. Whether /Game/LevelPrototyping/Materials/M_Flame is still dirty after the save, and the mtime of Content/LevelPrototyping/Materials/M_Flame.uasset from the shell, compared against the current time, so we know the save actually reached disk rather than only clearing a flag.
5. The output of `git status --short` at the end.

Report the raw tool responses verbatim, including any error or warning, and do not clean up or summarize the raw output.

Write the report to Docs/Terminal-Log/2026-09-04-60-flame-brightness-30-to-5.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

옮기며 넣은 해석: 4번의 mtime 대조는 사용자 지시에 없다. 메모리의 "저장은 Compile 뒤에 걸린다"에서 나왔다. 그리고 이 명령에 쓴 **"셰이더를 다시 빌드해야 한다"는 전제가 틀렸다** — 아래 결과 참조.

**명령 61 — `TopSurfaceColor` 정적 스위치 켜기**

```
In the Unreal project, change ONE static switch and verify it.

Set the static switch parameter named TopSurfaceColor on the material instance /Game/LevelPrototyping/Materials/MI_Castle_Stone to true. Do not change any other parameter on that material instance - no scalar, no vector, no texture, no other static switch. Do not touch its parent material.

A static switch is baked into the shader, unlike a scalar parameter, so this one really does force a shader rebuild. Report how long the rebuild took, how many shaders were compiled, and every shader compile error or warning that appeared in the log - quote them verbatim, do not summarize them.

Then save the material instance.

After saving, read back and report:
1. The value of the TopSurfaceColor static switch, to confirm the write landed.
2. A full list of every other static switch parameter on MI_Castle_Stone with its value, and a full list of every scalar and vector parameter override on it with its value, so we can see nothing else moved.
3. Whether /Game/LevelPrototyping/Materials/MI_Castle_Stone is still dirty after the save, and the mtime of Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset from the shell compared against the current time.
4. The output of `git status --short` at the end.

Also report whether a PIE session is running.

Report the raw tool responses verbatim, including any error or warning, and do not clean up or summarize the raw output.

Write the report to Docs/Terminal-Log/2026-09-04-61-castle-stone-top-surface-color.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

옮기며 넣은 해석: 2번의 "다른 파라미터 전부 나열"은 AI가 넣었다. 지난 세션이 손으로 맞춘 석재 값이 이 MI에 들어 있는데 기준선이 없었다. 그리고 여기서도 **"정적 스위치는 진짜로 셰이더를 다시 빌드한다"는 전제가 화면에서 확인되지 않았다.**

**명령 62 — `TopSurfaceColor` 벡터 밝히기**

```
In the Unreal project, change ONE vector parameter and verify it.

On the material instance /Game/LevelPrototyping/Materials/MI_Castle_Stone, set the VECTOR parameter named TopSurfaceColor to r 0.18, g 0.172174, b 0.159652, a 1.0.

CAUTION - MI_Castle_Stone has TWO parameters named TopSurfaceColor: one Vector and one StaticSwitch. They are different parameters that share a name. You must write the VECTOR one. Do NOT touch the StaticSwitch of the same name, which is currently true and must stay true.

Change nothing else. Do not touch TopGridColor, TopSubGridGridColor, SurfaceColor, GridColor, SubGridColor, Line Dimensions, any scalar, any other static switch, or the parent material M_PrototypeGrid.

Then save the material instance.

After saving, read back and report:
1. The effective value of the TopSurfaceColor VECTOR parameter, to confirm the write landed.
2. The value of the TopSurfaceColor STATIC SWITCH, which must still be true.
3. The effective values of all three static switches, all four scalars, and all seven vectors on MI_Castle_Stone, so we can see nothing else moved. For comparison, here is what they were before this change:
   static switches: TopSurfaceColor true, ObjectAligned false, Grid true
   scalars: Roughness 1, Grid Size 200, Sub Grid Number 5, CircleSize 100
   vectors: SurfaceColor (0.135, 0.125, 0.112, 1), TopGridColor (0.04, 0.038, 0.035, 1), GridColor (0.045, 0.042, 0.038, 1), TopSurfaceColor (0.115, 0.11, 0.102, 1), TopSubGridGridColor (0.08, 0.076, 0.07, 1), SubGridColor (0.09, 0.085, 0.078, 1), Line Dimensions (0.021838, 0.001347, 0.5, 0)
   TopSurfaceColor is the only one that should differ.
4. Whether MI_Castle_Stone is still dirty after the save, and the mtime of Content/LevelPrototyping/Materials/MI_Castle_Stone.uasset from the shell compared against the current time.
5. The output of `git status --short` at the end.

Also report whether a PIE session is running.

Report the raw tool responses verbatim, including any error or warning, and do not clean up or summarize the raw output.

Write the report to Docs/Terminal-Log/2026-09-04-62-top-surface-color-brighten.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

옮기며 넣은 해석: 사용자는 숫자 하나(`0.18`)를 골랐지만 이건 RGB 벡터다. AI가 **기존 색조 비율 `1 : 0.9565 : 0.8870`을 유지**하고 밝기만 올려 `(0.18, 0.172174, 0.159652)`로 정했다. 세 채널을 다 `0.18`로 하면 무채색이 되기 때문이다. `TopGridColor`·`TopSubGridGridColor`(윗면 줄눈)를 안 건드린 것도 AI 판단이다.

**명령 63 — NavMesh 경계 결정용 지형 조사**

```
In the Unreal project, do NOT change anything. This is a read-only survey to decide where to cut the NavMesh bounds.

The level /Game/ThirdPerson/Lvl_Stage has a single NavMeshBoundsVolume at location (900, 100, 200) with scale (23, 38, 4), which with the default 100-unit half-extent box gives a Z range of -200 to 600. Building paths put walkable navmesh on top of the room walls, which is outside the playable space. I need the numbers to choose a new top for that Z range.

Survey the level and report:

1. Every StaticMeshActor in the level whose label contains "Wall". For each one report its label, its world location, its scale, its static mesh asset path, and - most importantly - the world-space Z of the TOP of its bounding box and the Z of the BOTTOM. Compute the top and bottom from the actor's actual world bounds, not from my arithmetic. Then give me the minimum, maximum, and the distinct set of top-Z values across all of them.

2. The same for every actor whose label contains "Floor", "Ceiling", "Ramp", "Stair", "Step", or "Rail". Label, location, scale, bounding box top Z and bottom Z.

3. The world-space Z of the walkable surface the player spawns on - report the PlayerStart actor's location.

4. Every actor in the level whose bounding box top Z is between 250 and 650, listed with its label and top Z. This is the band I am considering cutting through, and I need to know what else lives in it before choosing a number.

5. The RecastNavMesh actor's settings: AgentRadius, AgentHeight, AgentMaxStepHeight, AgentMaxSlope, CellSize, CellHeight, and its RuntimeGeneration mode.

Use the programmatic toolset to enumerate rather than making one call per actor, but report the raw responses, and if a script fails part way say so rather than filling the gap.

Report the raw tool responses verbatim, including any error or warning, and do not clean up or summarize the raw output. Also report whether a PIE session is running.

Write the report to Docs/Terminal-Log/2026-09-04-63-navmesh-bounds-survey.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

옮기며 넣은 해석: 4번의 `250 ~ 650` 구간은 AI가 잡았다. 벽 윗면은 자르고 1층 바닥은 남기려면 그 사이여야 하는데, 그 구간에 다른 것이 살고 있으면 숫자가 달라지기 때문이다.

**명령 64 — `NavBounds_Main` 천장 내리기**

```
In the Unreal project, change ONE actor's transform and verify the navmesh that results.

The actor NavMeshBoundsVolume named NavBounds_Main in /Game/ThirdPerson/Lvl_Stage currently has location (900, 100, 200) and scale (23, 38, 4), giving world bounds Z -200 to 600.

Change it to location (900, 100, 75) and scale (23, 38, 2.75). Leave X and Y of both location and scale exactly as they are - only the Z of the location and the Z of the scale change. Do not rotate it. Do not touch any other actor.

The intended result is world bounds Z -200 to 350, so that the wall tops at Z 400 fall outside the volume and stop generating walkable navmesh, while the ground floor at Z 0 stays well inside.

After the change:

1. Read back NavBounds_Main's transform AND its world-space bounds via get_actor_bounds. The bounds must read Z min -200, Z max 350, and X and Y must be unchanged from X -1400..3200, Y -3700..3900. If X or Y moved, say so - that would mean the scale write did something I did not intend.

2. RuntimeGeneration on the navmesh is Dynamic, so the navmesh should rebuild by itself. Report whether it did: quote any LogNavigation or LogNavigationDataBuild lines that appear after the transform change, verbatim. If nothing rebuilt, say so rather than assuming.

3. Read the RecastNavMesh-Default actor's world bounds via get_actor_bounds. Before this change they were Z 10 to 570. Report the new values. I expect the Z max to drop below 400.

4. Save the level. This is a World Partition level, so the moved actor lives in its own __ExternalActors__ package - make sure the save actually covers it, and report which packages were written by quoting the LogSavePackage lines.

5. Report `git status --short`, and confirm from it that an __ExternalActors__ package was modified. If nothing under Content/__ExternalActors__ changed, the save did not reach the actor and you should say so plainly.

Also report whether a PIE session is running before you start.

Report the raw tool responses verbatim, including any error or warning, and do not clean up or summarize the raw output.

Write the report to Docs/Terminal-Log/2026-09-04-64-navbounds-lower-ceiling.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

옮기며 넣은 해석: `350`은 AI가 제시하고 사용자가 고른 값이다. 벽 윗면 `400`에서 `50` 아래다. 1번의 X·Y 되읽기 요구는 AI가 넣었다 — 스케일을 건드리면 X·Y가 같이 흔들릴 수 있고, 줄어들면 조용히 레벨 일부에 NavMesh가 사라지기 때문이다. 그리고 이 명령의 **"`RuntimeGeneration`이 `Dynamic`이니 NavMesh가 저절로 다시 만들어질 것"이라는 전제도 틀렸다.**

MCP를 AI가 직접 부른 것도 있다. 읽기만 했고, 목록은 `IsPIERunning`, `list_toolsets`, `describe_toolset`, `ObjectTools.list_properties`, `ObjectTools.get_properties`, `SceneTools.find_actors`, `ActorTools.get_components`, `ActorTools.get_actor_transform`, `ActorTools.get_actor_bounds`다.

## Terminal 결과

### 원문 — English

터미널 보고서 아홉 개는 각각 `Docs/Terminal-Log/2026-09-04-56` ~ `64`에 전문이 있다. 아래는 **판단 근거가 된 줄만 발췌**한 것이고, 발췌했다는 사실을 밝힌다. 다만 **실패·경고·어긋난 응답은 발췌하지 않고 전문**으로 붙인다.

**클래스 기본값은 바뀌었는데 배치 인스턴스는 안 바뀐 것 (명령 56)**

```
call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C:Backplate_GEN_VARIABLE"}, "properties": ["CastShadow"]}
{"returnValue":"{\"CastShadow\":false}"}

call: editor_toolset.toolsets.object.ObjectTools.get_properties
args: {"instance": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Backplate"}, "properties": ["CastShadow"]}
{"returnValue":"{\"CastShadow\":true}"}
```

**어긋난 응답 · 전문 — `get_components`가 생성 클래스를 거부**

```
call: editor_toolset.toolsets.actor.ActorTools.get_components
args: {"actor": {"refPath": "/Game/Interaction/BP_Torch.BP_Torch_C"}}

Parameter error: /Game/Interaction/BP_Torch.BP_Torch_C is not valid Actor for property 'actor'.
```

**어긋난 응답 · 전문 — `call_tool`이 완전한 이름을 거부**

```
call: editor_toolset.toolsets.actor.ActorTools.get_components (as tool_name)

Unknown tool editor_toolset.toolsets.actor.ActorTools.get_components
```

```
call: EditorToolset.EditorAppToolset.IsPIERunning (passed as tool_name)

Tool 'EditorToolset.EditorAppToolset.IsPIERunning' not found
```

**어긋난 응답 · 전문 — 이름 하나가 못 읽히면 호출 전체가 실패한다 (세 번 관찰)**

```
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Light' (PointLightComponent): the following properties could not be read: CastShadow
```

```
GetObjectProperties on '/Game/LevelPrototyping/Materials/M_Flame.M_Flame' (Material): the following properties could not be read: bUsedAsSpecialEngineMaterial
```

```
GetObjectProperties on '/Game/LevelPrototyping/Materials/MI_Castle_Stone.MI_Castle_Stone' (MaterialInstanceConstant): the following properties could not be read: StaticParameters, StaticParametersRuntime
```

```
GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.RecastNavMesh_UAID_9C6B005AF86909FD02-Default' (RecastNavMesh): the following properties could not be read: AgentMaxStepHeight, CellSize, CellHeight
```

**어긋난 응답 · 전문 — 애셋 레지스트리와 `is_dirty`가 서로 다른 말을 한다**

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: for a in find_assets("/Game", ""): if is_dirty(a): dirty.append(a)

Asset does not exist: /Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/1/2C/2CHLD5GCB4WLP4X15FK46A
Asset does not exist: /Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/5/2N/FCVKIYP6OKL5TD4S33JRIO
Asset does not exist: /Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/6/3J/M1ISS10UBLM1HT5YP1D74G
Asset does not exist: /Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/C/VN/7O6FXTR28IQ92JNY14ENUW
Asset does not exist: /Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/D/MP/1OU6UE00HRZKI42ATRN5WP
Asset does not exist: /Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/0/TQ/1UP2MCOIYXC0GTW985R4K0
Asset does not exist: /Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/4/N4/1UVYQEVSONIYWETDLYKSAD
Asset does not exist: /Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/5/TX/O6OLZU4WSCI3YRJS922SWL
Asset does not exist: /Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/9/CJ/HU1I8LGRRCYOV9I0SJEY8V
Asset does not exist: /Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/E/2R/I7YTTKZX32ZUPSIFKIB1NS
```

```
call: editor_toolset.toolsets.asset.AssetTools.is_dirty
args: {"asset_path": "/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/0/3M/P6JIGHZ879GWQXGT391UUE"}

Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/0/3M/P6JIGHZ879GWQXGT391UUE
```

```
call: editor_toolset.toolsets.scene.SceneTools.save_actor
args: {"actor": {"refPath": "/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.NavMeshBoundsVolume_UAID_9C6B005AF86909FD02_1188892250"}}

Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/1/5U/P7ECEQCYRKZWH9L3ZRDTWI
Failed to save 'NavBounds_Main'.
```

**어긋난 응답 · 전문 — 열거형 값이 파이썬으로 못 넘어간다**

```
"MP_ShadingModel": {"ERROR": "ToolsetRegistry: TypeError: function: Failed to convert argument at pos '2' when calling function 'get_property_input' on 'MaterialTools'\n  TypeError: PythonizeProperty: Cannot pythonize 'material_property' (ByteProperty)\n    TypeError: PythonizeEnumEntry: Cannot pythonize '29' (int64) as 'MaterialProperty'"}
```

**리로드 (명령 58) — 발췌**

```
[2026.09.04-01.44.45:335][264]Cmd: MAP LOAD FILE="D:/20260827/MCP1/Content/ThirdPerson/Lvl_Stage.umap" TEMPLATE=0 SHOWPROGRESS=1 FEATURELEVEL=4
[2026.09.04-01.44.45:410][264]LogWorld: UWorld::CleanupWorld for Lvl_Stage, bSessionEnded=true, bCleanupResources=true
[2026.09.04-01.44.45:717][264]MapCheck: Map check complete: 0 Error(s), 0 Warning(s), took 0.81ms to complete.
```

**경고 · 전문 — 리로드가 뱉은 것 둘**

```
[2026.09.04-01.44.45:411][264]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
[2026.09.04-01.44.45:615][264]LogNavigation: Warning: Recreating dtNavMesh instance (RecastNavMesh_UAID_9C6B005AF86909FD02-Default) due mismatch in number of bytes required to store serialized maxTiles (serialized: 135, 8 bits) vs calculated required (120, 7 bits)
```

**리로드 뒤 되읽기 (명령 58) — 발췌, 12개 중 3개**

```
{"returnValue":"{\"CastShadow\":false}"}
{"returnValue":"{\"CastShadow\":false}"}
{"returnValue":"{\"CastShadow\":false}"}
```

**`M_Flame` 그래프 (명령 59) — 발췌**

```
call: editor_toolset.toolsets.material.MaterialTools.get_property_input
args: {"material": {"refPath": "/Game/LevelPrototyping/Materials/M_Flame.M_Flame"}, "material_property": "MP_EmissiveColor"}
{"returnValue":{"output_name":"","expression":{"refPath":"/Game/LevelPrototyping/Materials/M_Flame.M_Flame:MaterialExpressionMultiply_0"},"input_name":""}}

{"returnValue":"{\"ParameterName\":\"FlameColor\",\"DefaultValue\":{\"r\":1,\"g\":0.44999998807907104,\"b\":0.11999999731779099,\"a\":1},...}"}
{"returnValue":"{\"ParameterName\":\"FlameBrightness\",\"DefaultValue\":30,...}"}

{"returnValue":"{\"ShadingModel\":\"MSM_Unlit\",\"BlendMode\":\"BLEND_Opaque\",\"TwoSided\":false,...}"}
{"returnValue":"{\"StaticMesh\":{\"refPath\":\"/Engine/BasicShapes/Cone.Cone\"},\"OverrideMaterials\":[{\"refPath\":\"/Game/LevelPrototyping/Materials/M_Flame.M_Flame\"}],\"RelativeScale3D\":{\"x\":0.17999999999999999,\"y\":0.17999999999999999,\"z\":0.30000004577637418},\"RelativeLocation\":{\"x\":0,\"y\":0,\"z\":-14},\"RelativeRotation\":{\"pitch\":0,\"yaw\":0,\"roll\":0},\"CastShadow\":false,\"Mobility\":\"Movable\",\"bVisible\":true}"}
```

**같은 이름의 파라미터 둘 (명령 61) — 발췌**

```
call: editor_toolset.toolsets.material_instance.MaterialInstanceTools.list_parameters
{"returnValue":[{"type":"Scalar","name":"Roughness"},{"type":"Scalar","name":"Grid Size"},{"type":"Scalar","name":"Sub Grid Number"},{"type":"Scalar","name":"CircleSize"},{"type":"Vector","name":"SurfaceColor"},{"type":"Vector","name":"TopGridColor"},{"type":"Vector","name":"GridColor"},{"type":"Vector","name":"TopSurfaceColor"},{"type":"Vector","name":"TopSubGridGridColor"},{"type":"Vector","name":"SubGridColor"},{"type":"Vector","name":"Line Dimensions"},{"type":"StaticSwitch","name":"TopSurfaceColor"},{"type":"StaticSwitch","name":"ObjectAligned"},{"type":"StaticSwitch","name":"Grid"}]}
```

**NavMesh 경계와 재빌드 (명령 64) — 발췌**

```
call: editor_toolset.toolsets.actor.ActorTools.get_actor_bounds  (NavBounds_Main, after)
{"returnValue":{"min":{"x":-1400,"y":-3700,"z":-200},"max":{"x":3200,"y":3900,"z":350},"isValid":true}}

call: editor_toolset.toolsets.actor.ActorTools.get_actor_bounds  (RecastNavMesh-Default, after)
{"returnValue":{"min":{"x":-1976,"y":-3952,"z":10},"max":{"x":3952,"y":3952,"z":570},"isValid":true}}

[2026.09.04-03.10.06:306][320]LogSavePackage: Moving output files for package: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/1/5U/P7ECEQCYRKZWH9L3ZRDTWI
```

**엔진 소스로 확인한 것 — 발췌**

```
LevelEditor/Private/ViewportToolbar/LevelEditorSubmenus.cpp:1103:  LOCTEXT("VisualizeBufferViewModeDisplayName", "Buffer Visualization"),
Config/BaseEngine.ini:3141:BaseColor=(Material="/Engine/BufferVisualization/BaseColor.BaseColor", Name=LOCTEXT("BaseColorMat", "Base Color"), EnableOnMobile=true)
LevelEditor/Private/LevelEditorActions.cpp:4434:  UI_COMMAND( BuildPathsOnly, "Build Paths", "Only builds paths (all levels.)", EUserInterfaceActionType::Button, FInputChord() );
NavigationSystem/Public/NavigationSystem.h:1300:  static NAVIGATIONSYSTEM_API bool bNavigationAutoUpdateEnabled;
NavMesh/RecastNavMesh.h:719:  UPROPERTY(config, meta = (DeprecatedProperty, DeprecationMessage = "Use NavMeshResolutionParams to set AgentMaxStepHeight for the different resolutions instead"))
```

### 요약 — 한글

바뀐 것은 애셋 여섯 개다.

- **`BP_Torch`** — 컴포넌트 템플릿 `Backplate`·`Bracket`·`Cup`의 `CastShadow`가 `true` → `false`. `Flame`은 원래 `false`였고 안 건드렸다. `Light`(`PointLightComponent`)의 `CastShadows`는 `true` 그대로다
- **`M_Flame`** — `MaterialExpressionScalarParameter_0`(`FlameBrightness`)의 `DefaultValue`가 `30` → `5`. `MaterialExpressionVectorParameter_0`(`FlameColor`)와 `MaterialExpressionMultiply_0`, `MP_EmissiveColor` 연결은 그대로
- **`MI_Castle_Stone`** — `StaticSwitch` `TopSurfaceColor`가 `false` → `true`. `Vector` `TopSurfaceColor`가 `(0.115, 0.11, 0.102, 1)` → `(0.18, 0.172174, 0.159652, 1)`. 나머지 파라미터 12개는 값도 `expressionGUId`도 그대로
- **`NavBounds_Main`** — `location` `(900, 100, 200)` → `(900, 100, 75)`, `scale` `(23, 38, 4)` → `(23, 38, 2.75)`. 월드 경계가 `Z -200..600` → `Z -200..350`. X·Y는 `-1400..3200`, `-3700..3900`으로 불변
- **`RecastNavMesh-Default` 패키지** — 사용자가 `Build Paths`를 두 번 돌리고 `Ctrl+S` 했다. `33054` → `72208`바이트, mtime `12:24:49`
- **`M_PrototypeGrid`** — **AI가 안 건드린 것이다.** 명령 61·62에서 명시적으로 금지했고 두 보고서의 `LogSavePackage`에도 없다. `11:48:34`에 저장됐는데 그건 사용자가 첫 `Build Paths` 뒤 `Ctrl+S`를 누른 시각이다

레벨은 한 번 다시 열었다(`SceneTools.load_level`). 컴파일이 dirty로 만든 `__ExternalActors__` 패키지 18개를 버리기 위한 것이고, 버리기 전에 `git diff HEAD -- Content/__ExternalActors__`가 비어 있는 것을 확인했다.

## 분석

### 무엇을 만들었나

**사양** — `Docs/Spec/2026-09-04-토치-그림자와-불꽃.md`. 범위 · 상태(하나뿐) · 권한(싱글) · 수명(레벨 배치) · 튜닝 값의 주인, 그리고 합격 기준 넷. `Docs/Spec/`이 `09-01` 이후 끊겼다가 `09-03`에 되살아난 뒤 두 번째 파일이다.

**`BP_Torch` 컴포넌트 셋** — `Backplate` · `Bracket` · `Cup`의 `CastShadow`가 `false`. `Flame`(`/Engine/BasicShapes/Cone`, 스케일 `(0.18, 0.18, 0.30)`, 위치 `(0, 0, -14)`)과 `Light`(`Intensity 5000`, `IntensityUnits Unitless`, `AttenuationRadius 1200`, `LightColor (1, 0.6667, 0.3529, 1)`, `SourceRadius 10`, `Mobility Movable`, `CastShadows true`)는 안 건드렸다.

**`M_Flame` 파라미터 하나** — `FlameBrightness` `30` → `5`. 그래프는 노드 셋뿐이다: `VectorParameter FlameColor (1, 0.45, 0.12, 1)`의 `RGB`가 `Multiply.A`로, `ScalarParameter FlameBrightness`가 `Multiply.B`로, `Multiply`의 출력이 `MP_EmissiveColor`로. `ShadingModel MSM_Unlit`, `BlendMode BLEND_Opaque`, `TwoSided false`, `bUsedWithStaticMesh true`. 머티리얼 인스턴스는 없고 `get_referencers`가 `/Game/Interaction/BP_Torch` 하나만 돌려준다.

**`MI_Castle_Stone` 파라미터 둘** — `StaticSwitch TopSurfaceColor` `false` → `true`, `Vector TopSurfaceColor` `(0.115, 0.11, 0.102, 1)` → `(0.18, 0.172174, 0.159652, 1)`. 부모는 `M_PrototypeGrid`. 이 MI는 `SM_Cube`의 머티리얼 슬롯 `lambert1`에 직접 물려 있고, 바닥 액터들은 `OverrideMaterials`가 비어 있어서 메시 슬롯 값을 그대로 쓴다.

**`NavBounds_Main`** — `location.z` `200` → `75`, `scale.z` `4` → `2.75`. 월드 경계 `Z -200..350`.

**터미널 보고서 아홉** — `Docs/Terminal-Log/2026-09-04-56` ~ `64`. `08-31`부터 `09-03`까지 다섯 세션 동안 사라졌던 방식이 `09-03`에 되살아난 뒤 이번이 두 번째다.

### 기술적으로 맞게 짚은 부분

**`CastShadow`는 끄고 `CastShadows`는 살린 것.** `UPrimitiveComponent::CastShadow`는 그 메시가 **그림자를 던지는가**이고, `ULightComponentBase::CastShadows`는 그 광원이 **그림자를 만드는가**다. 이름이 한 글자 차이라 뭉뚱그리기 쉬운데, 소품 셋만 끄고 광원을 살렸기 때문에 벽·기둥·플레이어 그림자가 그대로 남았다. 스크린샷에서 플레이어 그림자가 바닥에 있는 것이 그 증거다. 광원까지 껐으면 방 전체가 평평해졌을 것이다.

**오버라이드인지 메모리 잔재인지를 디스크에서 가른 것.** 클래스 기본값이 `false`인데 배치 인스턴스가 `true`로 읽혔을 때, 터미널 보고서는 "인스턴스 오버라이드"로 진단하고 `reset_properties`를 18개 액터에 부르자고 제안했다. 그 대신 `Content/__ExternalActors__`의 해당 패키지 18개를 바이너리로 `CastShadow` 문자열 검색했다 — **18개 중 0개.** 그리고 같은 grep이 다른 액터 패키지 2개에서는 걸리는 것까지 확인해서 **grep 자체가 유효하다는 것**을 먼저 세웠다. 오버라이드된 프로퍼티는 패키지 이름 테이블에 문자열로 남으므로, 안 걸리면 디스크에 없다는 뜻이다. 리로드 한 번으로 12개 값이 전부 `false`가 되면서 이 판단이 맞았다.

**`reset_properties`를 18개 액터에 안 부른 것.** 손대지 않은 게 정답인 경우다. 불렀다면 레벨 액터 18개를 쓰고 저장해서 `git`에 18개 파일이 올라갔을 것이고, 그러고도 근본 원인(재인스턴싱이 새 클래스 기본값을 안 내려보내는 것)은 안 드러났을 것이다.

**보고서의 `bCanEverAffectNavigation` 제안을 거부한 것.** 명령 63의 보고서가 "벽 액터를 navigation에 영향 없게 표시하면 벽 위 타일이 사라진다"고 제안했는데, 그 플래그는 **벽을 장애물에서 빼는 것**이다. 그대로 했으면 적이 벽을 통과하는 경로가 생겼을 것이다. 그림자 문제와 형태가 비슷해 보이지만 반대 방향이다.

**벽이 정확히 겹쳐 쌓인 것을 좌표로 확인해 보고서의 결론을 뒤집은 것.** 명령 63의 보고서는 "벽 윗면이 `200`과 `400`에 있고 2F 바닥이 `600`이라 하나의 천장으로 못 가른다"고 결론지었다. 그런데 표를 보면 `Wall_S_Lower (-1300, -3600, 0) scale (2, 74, 2)`와 `Wall_S_Upper (-1300, -3600, 200) scale (2, 74, 2)`처럼 **14쌍 전부 X·Y·스케일이 일치**한다. `200`짜리 윗면은 위 벽에 덮여 있어서 NavMesh가 생길 수 없다. 노출된 윗면은 `400` 하나뿐이고, 그래서 `350`이라는 답이 나온다.

**조명을 빼고 알베도만 본 것.** 기준 3을 `Lit`으로 판정하려 했을 때 바닥이 벽보다 어두워 보였지만 **빛 각도 차이와 구분이 안 됐다.** `Buffer Visualization` → `Base Color`로 바꾸면 조명이 빠져서 알베도만 남는다. 첫 판정에서 "세 면이 같은 회색"이 나왔고, 값을 계산해 보니 sRGB `103` vs `95` — `8/255` 차이라 안 보이는 게 정상이었다. 값을 올린 뒤 다시 같은 모드로 봐서 갈렸다. **모드를 안 바꿨으면 "스위치가 안 먹는다"고 잘못 결론 냈을 것이다.**

**메뉴 경로를 기억이 아니라 엔진 소스로 확인한 것.** `Buffer Visualization`(`LevelEditorSubmenus.cpp:1103`), `Base Color`(`BaseEngine.ini:3141`), `Build Paths`(`LevelEditorActions.cpp:4434`) 셋 다 코드 블록에 넣기 전에 grep했다. 메모리에 "UE UI 경로는 검증하고 쓴다"가 있는 이유다.

**색조 비율을 유지한 것.** 사용자가 고른 것은 `0.18`이라는 숫자 하나였는데 대상은 RGB 벡터다. 세 채널을 다 `0.18`로 하면 무채색이 되어 따뜻한 석재 색이 사라진다. 기존 비율 `1 : 0.9565 : 0.8870`을 유지해서 `(0.18, 0.172174, 0.159652)`로 옮겼고, 되읽은 값이 비율까지 그대로였다.

**사용자가 합격 기준의 오류를 잡은 것.** 이건 AI가 아니라 사용자가 짚었다. `PIE에서 적이 문간을 지나 플레이어를 쫓아온다`는 기준은 `BP_StageRoom`의 `RoomBounds` 오버랩이 **방에 들어가는 순간 문을 닫고 봉인**하기 때문에 게임에서 일어나지 않는 상황이었다. 사양을 쓸 때 `Docs/AI-Log/2026-09-03-t-shape-level-stage-rules.md`의 명령 21을 안 읽고 "NavMesh가 이어졌는가"를 문간으로 확인하려 한 것이 원인이다. **사양의 게이트가 게임 규칙과 어긋나 있었고, 그걸 AI가 아니라 사람이 잡았다.**

### 확인한 것 / 확인 못 한 것

**확인한 것** — 전부 에디터·PIE 화면에서 눈으로 본 것이다.

- 합격 기준 1 통과. 토치 아래 벽의 부채꼴 검은 그림자가 사라졌다. PIE 스크린샷
- 같은 스크린샷에서 플레이어 그림자와 기둥 그림자가 남아 있다 — `Light`의 `CastShadows`가 살아 있다
- 받침(`Bracket`) 모양이 "꺾인 배관"처럼 보이던 것이 **형태 문제가 아니라 자기 그림자 때문**이었다. 그림자를 끄니 받침으로 읽힌다
- 합격 기준 2 조건부 통과. 불꽃에 주황이 돌아왔다. 다만 심지는 여전히 희다
- 벽에 깔리는 빛이 안 어두워졌다 — 발광 메시가 조명에 기여하고 있던 게 아니다
- 합격 기준 3 부분 통과. `Base Color` 모드에서 바닥이 벽보다 밝은 회색으로 갈렸다
- 리로드 뒤 배치 토치 3개 × 4개 컴포넌트 = 12개 값이 전부 `false`
- NavMesh를 다시 구운 뒤 **벽 윗면의 초록 테두리가 사라졌고 1층 바닥은 그대로 덮여 있다.** 사용자가 `P` 키 시각화로 확인
- 문간을 NavMesh가 통과한다. 사용자 스크린샷
- 합격 기준 4(고쳐 쓴 것) 통과. 방 안에서 적이 플레이어에게 달려온다. 사용자가 PIE에서 확인
- `NavBounds_Main` 경계 `Z -200..350`, X·Y 불변. AI가 MCP로 되읽음
- `M_Flame.uasset`·`MI_Castle_Stone.uasset`·`NavBounds_Main` 패키지의 mtime이 `LogSavePackage` 줄과 밀리초까지 일치 — 저장이 디스크에 갔다
- `RecastNavMesh` 패키지가 `12:24:49`에 저장됐다. 두 번째 `Build Paths` 뒤다

**확인 못 한 것** — 왜 못 했는지까지.

- **`M_PrototypeGrid.uasset`이 왜 바뀌었는지.** `11:48:34`에 저장됐고 그건 사용자의 `Ctrl+S` 시각이다. 정적 스위치 변경으로 부모가 dirty가 됐다는 추정이지만, **그 시각에 무엇이 dirty였는지는 이제 못 읽는다.** `is_dirty`는 현재 상태만 준다
- **VSM 광원 오버플로 경고가 실제로 있었는지.** 지난 세션 기록의 항목인데, 이번에 그 경고 원문을 한 번도 못 봤다. 터미널에 찍게 하지 않았다
- **`Flame` 컴포넌트의 collision.** 지난 세션에서 넘어온 항목이고 이번에도 안 읽었다. `CastShadow false`만 봤다
- **`MP_ShadingModel` 입력 핀에 무엇이 물려 있는지.** 열거형 값 `29`가 파이썬으로 변환이 안 돼서 호출 자체가 실패한다. 노드가 셋뿐이라 아마 아무것도 안 물려 있겠지만 **읽지 못했다**
- **셰이더가 실제로 컴파일됐는지.** 명령 60·61 둘 다 `LogShaderCompilers` 줄이 0개다. 스칼라는 유니폼이라 그렇다 치고, **정적 스위치는 셰이더 순열을 바꾸는데도 컴파일 로그가 없다.** 보고서는 DDC 히트로 설명하지만 그건 추론이고, 확인하려면 DDC를 지워야 해서 안 했다
- **에디터 자동 NavMesh 재빌드가 왜 안 걸리는지.** `bNavigationAutoUpdateEnabled`가 `UPROPERTY`가 아닌 static 멤버라 `ObjectTools`로 못 읽는다. 콘솔 변수 검색에도 없다. `Build` 메뉴를 눈으로 봐야 갈린다
- **2층에 NavMesh가 없다는 것.** `RecastNavMesh` 경계 `Z 10..570` < 2F 바닥 `600`으로 추론했다. 이제 천장을 `350`으로 내렸으니 확실히 없지만, **바꾸기 전 상태를 직접 본 적은 없다**
- **레벨의 `__ExternalActors__` 113개가 정말 깨끗한지.** `is_dirty`가 이 경로를 아예 못 읽는다. autosave가 아무것도 안 쓴 것으로 간접 확인했을 뿐이다
- **`/Game` 밖 3655개 엔진 플러그인 애셋의 dirty 여부.** `is_dirty` 한 번에 `91ms`라 `5.5`분이 걸린다. CLAUDE.md가 오래 걸리는 작업을 임의로 돌리지 말라고 해서 안 했다
- **`Docs/ProjectICI5.8/`의 전제가 틀렸다.** `09-구현-대조.md`가 원본 GameMode를 *"`Stage 1/2/3 Spawn` 함수 3벌"* 식으로 비판하는데, `Docs/ICI/포토폴리오_Project ICI .pdf` 첫 장의 *"제출자가 직접 만들고 구성한 부분만"* 선언으로 **그 GameMode/GameState가 사용자 본인 구현임이 확인됐다.** 그 문서들은 지금 남의 프로젝트를 분석한 것처럼 쓰여 있다. **지난 기록을 소급 수정하지 않는 것이 이 프로젝트 규칙이라 고칠지 자체가 결정이다**
- **회수한 여덟 파일의 본문.** `Docs/Terminal-Log/recovered/`에 있고 세 세션째 아무도 안 읽었다

### 남는 리스크

**컵 밑면이 새까만 원반으로 보인다.** 아래에서 올려다본 스크린샷에서 드러났다. 광원이 컵 바로 위(불꽃 자리)에 있어서 컵 밑면에 빛이 하나도 안 닿는다. 그림자와 무관하고 `CastShadow`를 꺼도 안 없어진다. 2층이 생겨서 토치를 위아래로 볼 일이 생긴 것이 이걸 드러냈다.

**불꽃 원뿔의 실루엣이 또렷해졌다.** 밝기를 내린 대가다. 흰 덩어리일 때는 형태가 안 보였는데 색이 돌아오면서 직선 모서리와 평평한 밑면이 드러난다. `/Engine/BasicShapes/Cone`을 스케일만 줄여 쓰고 있어서 값으로는 못 고친다.

**불꽃 심지가 여전히 희다.** `(5, 2.25, 0.6)`이라 R·G가 `1`을 넘는다. 더 내리면 원뿔 실루엣이 더 또렷해진다. 색과 형태가 맞바꿈 관계다.

**천장 밑면이 벽과 같은 색이다.** `TopSurfaceColor`는 위를 향한 면에 걸리는데 천장의 보이는 쪽은 아래를 향한 면이다. 이 스위치로는 원리상 못 닿는다. **사양의 합격 기준 3을 "바닥과 천장 밑면"으로 묶어 쓴 것이 애초에 틀렸다.**

**2층 · 램프 · 최종 구역의 NavMesh가 완전히 사라졌다.** `Z 550~600`이라 새 천장 `350` 밖이다. `F = a`(적은 2층에 안 온다)와 같은 방향이지만, **클리어 직후 문이 자동으로 열린 뒤**와 **죽고 부활해 문이 열쇠 없이 열린 뒤**에 적이 어떻게 행동하는지는 아무도 안 봤다. 되돌리려면 볼륨을 다시 올려야 한다.

**MCP `compile_blueprint`가 배치 액터를 갱신하지 않는다.** 클래스 템플릿은 바뀌는데 이미 인스턴스화된 에디터 액터는 옛 값을 들고 있고, 동시에 그 액터들의 패키지가 dirty가 된다. 레벨을 다시 열어야 맞춰진다. **이번에 이걸 "인스턴스 오버라이드"로 오진할 뻔했다.** 메모리에 `mcp-compile-does-not-refresh-placed-actors`로 남겼다.

**`ObjectTools.get_properties`는 이름 하나가 못 읽히면 호출 전체를 실패시킨다.** 이번 세션에 네 번 걸렸다(`CastShadow` on `PointLightComponent`, `bUsedAsSpecialEngineMaterial`, `StaticParameters`, `AgentMaxStepHeight`/`CellSize`/`CellHeight`). 읽을 수 있는 것까지 같이 날아간다.

**`__ExternalActors__` 경로를 여러 도구가 못 읽는다.** `is_dirty`도 `save_actor`도 `Asset does not exist`를 준다. 애셋 레지스트리는 `__ExternalObjects__`를 목록에 넣는데 `is_dirty`는 존재하지 않는다고 한다. **레벨 액터의 dirty 상태를 직접 물어볼 방법이 없다** — autosave 로그로 간접 추론하는 수밖에 없다.

**터미널 보고서가 그럴듯하게 틀린 결론을 낸다.** 이번에 세 번 나왔다 — 인스턴스 오버라이드 오진, "하나의 Z로 못 가른다"는 잘못된 결론, 색조 비율이 덜 따뜻해졌다는 잘못된 서술. 셋 다 **원문 데이터는 정확한데 그 위에 얹은 해석이 틀린 것**이라, 원문을 다시 읽어야만 잡힌다.

**`M_PrototypeGrid`가 설명 없이 변경된 상태로 커밋에 들어간다.** 이건 엔진 템플릿 머티리얼이고 레벨 전체가 쓴다.

### 총평

요청은 충족했다. 목록 1~4를 다 했고 합격 기준 넷 중 둘은 통과, 둘은 조건부·부분 통과로 **무엇이 통과 못 했는지까지 문장으로 남겼다.**

**이번 세션의 실질적 난이도는 블루프린트도 머티리얼도 아니라, 자기 확신에 찬 보고서를 의심하는 데 있었다.** 터미널이 돌려준 원문은 매번 정확했다. 틀린 것은 그 위에 얹은 해석이었고, 세 번 다 원문 숫자를 다시 읽어서 뒤집었다. 특히 "인스턴스 오버라이드"는 그대로 믿었으면 액터 18개를 쓰는 헛수고를 했을 것이고, "하나의 Z로 못 가른다"를 믿었으면 벽 위 NavMesh를 그냥 두거나 벽을 장애물에서 빼는 위험한 길로 갔을 것이다.

**AI가 낸 명령의 전제도 세 번 틀렸다.** "스칼라 파라미터를 바꾸면 셰이더를 다시 빌드해야 한다"(아니다, 유니폼이다), "정적 스위치는 진짜로 셰이더를 다시 빌드한다"(로그에 컴파일이 0줄이다), "`RuntimeGeneration`이 `Dynamic`이니 NavMesh가 저절로 재생성된다"(에디터에서는 안 걸린다). 셋 다 명령문에 단정문으로 써 보냈고, 셋 다 터미널이 "그런 일은 없었다"고 돌려줬다. **명령에 "왜 그런지"를 설명으로 넣는 습관이 검증 없는 단정을 흘려보내는 통로가 됐다.**

가장 값진 순간은 사용자가 **"근데 적이 로비에 나오면 안되는데"**라고 물은 자리다. 합격 기준 하나가 게임이 일부러 막아둔 상황을 검사하고 있었고, 그건 사양을 쓸 때 기존 규칙을 안 읽어서 생긴 것이다. AI가 만든 게이트가 게임과 어긋나 있었는데 사람이 잡았다.

## AI의 제안

> **"기록에 적힌 'VSM 대책 셋' 중 `CastShadow` 끄기가 이제 성능 문제가 아니라 보이는 문제의 해결책이 됐다."**

지난 세션이 성능 대책 후보로 적어둔 것을 스크린샷을 보고 시각 문제의 해법으로 다시 읽은 것. 얻는 것은 명령 하나로 두 문제를 같이 줄이는 것이고, 잃는 것은 소품이 그림자를 안 던져서 생기는 미세한 입체감이다.

> **"Then compile the Blueprint and save it. ... The CastShadow value of those same four components on ONE placed BP_Torch actor in the currently loaded level Lvl_Stage, so we can tell whether the 18 placed instances inherit the new class default or whether any of them has a per-instance override that ignores it."**

사용자가 요구하지 않은 되읽기를 명령에 넣은 것. 얻는 것은 이 세션에서 가장 큰 발견(컴파일이 배치 액터를 갱신 안 함)이고, 잃는 것은 명령이 길어지고 터미널 왕복이 늘어나는 것이다.

> **"`Content/__ExternalActors__`에서 해당 액터 패키지를 바이너리로 grep한다. 오버라이드된 프로퍼티는 이름 테이블에 문자열로 남으므로, 속성 이름이 안 걸리면 디스크에는 오버라이드가 없다는 뜻이다."**

MCP가 답을 못 주는 자리에서 디스크를 직접 본 것. 얻는 것은 오진을 뒤집는 결정적 증거이고, 잃는 것은 `.uasset`을 바이너리로 읽는다는 점에서 애셋 취급 규칙의 경계에 서는 것이다(읽기만 했다).

> **"뷰포트 왼쪽 위 `Lit` 드롭다운에서 `Buffer Visualization` → `Base Color`로 바꾸면 알베도만 그려지므로 윗면·옆면 색차가 조명과 섞이지 않는다."**

`Lit`으로는 판정이 안 되는 것을 보고 낸 것. 얻는 것은 조명 변수를 제거한 깨끗한 판정이고, 잃는 것은 사용자가 뷰포트 모드를 바꿨다 되돌려야 하는 수고다.

> **"보고서가 제안한 대안 하나는 쓰면 안 된다. '벽 액터를 navigation에 영향 없게 표시'는 벽 위 타일을 없애는 게 아니라 벽이 장애물이 아니게 만든다. 적이 벽을 통과하는 경로가 생긴다."**

터미널 보고서의 제안을 명시적으로 거부한 것. 얻는 것은 적 AI가 벽을 뚫는 사고를 막는 것이고, 잃는 것은 없다.

> **"기준을 바꾸는 게 맞다. 새 기준 — `PIE에서 방에 들어가 적의 시야에 잡히면, 적이 방 안에서 플레이어에게 달려온다.`"**

사용자의 봉인 지적을 받아 합격 기준을 다시 쓴 것. 얻는 것은 실제로 쓰이는 경로로 NavMesh를 검증하는 것이고, 잃는 것은 사양의 게이트를 작업 도중에 바꾼다는 점이다 — 그래서 원래 문장과 왜 틀렸는지를 사양 파일에 같이 남겼다.

## 다음으로 넘김

**바로 이어서 할 것**

- **다음 Terminal-Log 번호는 `65`다.** `56`~`64`가 이 세션 것이다. **`09-04` 오후 세션은 MCP를 한 번도 안 써서 번호가 안 늘었다**
- **커밋 안 된 것 넷.** `Docs/2026-09-04-프로젝트-총정리.md`(469줄) · `Docs/ICI/`(2025년 원본 PDF 3) · `Docs/Image/`(PIE 스크린샷 11) · `Portfolio/`(지원용, 13쪽 PDF 포함). 전부 `??` 상태다. **커밋할지 자체가 결정 사항이다** — 특히 `Portfolio/`는 게임 애셋이 아니라 지원 자료다
- **컵 밑면이 새까만 원반으로 보이는 것.** 이번 세션에 새로 드러났고 화면에서 가장 눈에 띈다. 안 셋 — 광원을 컵 아래로 조금 내리거나, 컵을 양면으로 만들거나, 밑면이 안 보이도록 토치 높이를 올리거나. **첫째가 가장 싸 보인다**

**결정 필요**

- **불꽃 원뿔을 어떻게 할 것인가.** `/Engine/BasicShapes/Cone`을 그냥 쓰고 있어서 값으로는 못 고친다. 발광 머티리얼에 노이즈를 흘리거나 메시를 바꾸는 길
- **천장 밑면을 무엇으로 다르게 만들 것인가.** `TopSurfaceColor`로는 원리상 못 닿는다. 천장 액터에만 다른 MI를 물리는 것이 가장 단순하다
- **2층 · 램프 · 최종 구역에 NavMesh를 되돌릴 것인가.** 지금 완전히 없다. 클리어 후와 부활 후에 적이 어떻게 행동하는지 보고 정한다
- **`M_PrototypeGrid`의 변경을 어떻게 할 것인가.** 왜 바뀌었는지 모른 채로 커밋에 들어간다. 되돌릴 수도, 그대로 둘 수도 있다
- **VSM 광원 오버플로.** `CastShadow` 셋을 끈 것으로 완화됐을 수 있지만 경고 원문을 한 번도 못 봤다. 남은 대책은 토치 수를 줄이는 것과 `r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel`을 올리는 것
- **줄눈을 엇갈리게 할 것인가.** 지금 남은 유일한 "프로토타입" 신호다. `M_PrototypeGrid`를 안 건드리고 새 머티리얼을 짜야 한다
- **방 셋에 천장이 없어 문 너머로 하늘이 보인다.** `09-04` 오후 스크린샷으로 확인됐다 — 어두워진 게 아니라 `DirectionalLight`/`SkyLight`가 그대로 들어와 **로비(횃불 주황)와 톤이 정반대다.** 큐브 셋으로 덮으면 되지만 **덮는 순간 캄캄해져서 방마다 횃불 6~8개가 같이 필요하다.** 로비가 `2200 × 2800`에 18개였다
- **로비 중앙이 어둡다.** 가설 셋 — 자동 노출이 어두운 쪽으로 수렴 / `AttenuationRadius 1200`이 로비 `2200 × 2800`에 부족 / 램프에 직접 닿는 광원이 없음. **판별은 공짜다** — 뷰포트를 `Unlit`으로 바꿔 램프 형태가 보이면 조명 문제, 안 보이면 재질 문제다
- **`DOOR IS LOCKED`가 시안색이라 따뜻한 톤과 부딪친다.** `ColorMessage` 값 하나. 임시 디버그 표시처럼 읽힌다
- **로비 남쪽 벽을 무엇으로 채울 것인가.** `2800`짜리 민 벽이라 토치 사이가 어둡다. 조명이 아니라 물건 문제다
- **문짝 액터 스케일의 비균일을 정리할 것인가.** 문 넷이 `(1, 2, 2)`라 열릴 때 폭이 변한다
- **아이템을 어떻게 보이게 할 것인가.** `/Engine/BasicShapes/` 기본 재질이라 어두운 로비에서 안 보인다. **2층에서 내려다보면 포션 둘이 보인다는 것은 `09-04`에 확인됐다** — 바닥 높이 시점이 문제다
- **`GAME CLEAR`를 한 번만 띄울 것인가.** 지금은 막다른 방에 들어갈 때마다 뜬다
- **봉인 닫기 속도를 여는 속도와 가를 것인가.** 지금 `SwingSpeed = 1`이라 여닫기 둘 다 `1.00`초다
- **`Content/FirstPerson/`을 어떻게 할 것인가.** 안에 `Anims/` 둘만 남았고 그 둘이 `BP_ThirdPersonCharacter`의 살아 있는 의존이다
- **`Content/` 재배치.** `BP_ThirdPersonGameMode.NotifyRoomCleared`가 `"/Game/Interaction/BP_Door.BP_Door_C"`를 문자열로 들고 있어 옮기면 조용히 끊긴다
- **`Docs/Spec`의 `09-01` 이후 끊긴 구간을 소급 회수할 것인가**
- **램프 옆면 난간 · 난간 높이 `100` · `Wall_2F_S`의 방1·방3 구간 · 로비 남쪽 장식 문.** 넷 다 사양의 미결이고 여러 세션째 넘어온 항목이다
- **중복 열쇠 회수 · `Ball_Test` 행 · `FoundSlotIndex` 삭제 · `AM_Player_Attack` 창 시작.** 앞 세션들에서 넘어온 항목들

**확인 필요**

- **에디터 자동 NavMesh 재빌드가 왜 안 걸리는지.** `Build` 메뉴에서 `Auto Update Navigation`이 꺼져 있는지 눈으로 보면 된다. `bNavigationAutoUpdateEnabled`는 `UPROPERTY`가 아니라 MCP로 못 읽는다
- **정적 스위치를 바꿔도 셰이더 컴파일 로그가 0줄인 것.** DDC 히트라는 설명은 추론이다
- **`M_PrototypeGrid`가 왜 저장됐는지**
- **VSM 광원 오버플로 경고의 원문**
- **`Flame` 컴포넌트의 collision.** 두 세션째 넘어온 항목이다
- **`BP_Torch`의 빈 `UserConstructionScript`·`EventGraph`.** Actor BP의 기본인지 터미널이 만든 것인지 안 갈렸다
- **`MP_ShadingModel` 입력 핀.** 열거형 변환 오류로 못 읽는다
- **`Docs/ProjectICI5.8/`의 전제가 틀렸다.** `09-구현-대조.md`가 원본 GameMode를 *"`Stage 1/2/3 Spawn` 함수 3벌"* 식으로 비판하는데, `Docs/ICI/포토폴리오_Project ICI .pdf` 첫 장의 *"제출자가 직접 만들고 구성한 부분만"* 선언으로 **그 GameMode/GameState가 사용자 본인 구현임이 확인됐다.** 그 문서들은 지금 남의 프로젝트를 분석한 것처럼 쓰여 있다. **지난 기록을 소급 수정하지 않는 것이 이 프로젝트 규칙이라 고칠지 자체가 결정이다**
- **회수한 여덟 파일의 본문.** `Docs/Terminal-Log/recovered/`에 있고 **세 세션째 아무도 안 읽었다**
- **`BP_Door`의 `Event Interact` 마지막 `else` 가지.** `read_graph_dsl`이 `_`로만 찍는다
- **문틀에 서 있을 때 문이 닫히면 끼이는지**
- **클리어한 뒤 · 부활한 뒤 적이 열린 문으로 로비까지 나오는지.** 이제 2층 NavMesh가 없어서 램프는 못 타지만 문은 그대로다
- **적 여섯이 서로 밀치는지**
- **`iconColor`의 구리색.** 은색(`Silver Key`, `0.75/0.78/0.8`)은 `09-04`에 화면으로 확인됐다. **구리색(`Key_Stage3`)은 아직 못 봤고 은색과 구분되는지도 모른다**
- **`M_Flame.FlameBrightness`를 `30 → 5`로 낮춘 것이 과했는지.** `09-04` 스크린샷에서 불꽃이 거의 안 보인다. 횃불인데 불이 안 보이면 광원의 출처가 화면에서 사라진다
- **`ClearedRooms`의 실제 값**
- **터미널이 시키지 않은 액터를 만드는 경로.** 이번 세션에는 관찰되지 않았다
- **`2026-09-01-enemy-hp-death.md`의 `확인 필요` 목록.** `arrange_nodes`, `EditorPerProjectUserSettings.ini` 저장 실패, `CaptureViewport`가 에디터 월드를 그리는 것이 그 파일에 그대로 있다

**접어둔 것**

- **`Bracket` 모양 고치기.** 이번에 해소됐다 — "꺾인 배관"처럼 보이던 것은 형태가 아니라 자기 그림자 때문이었다
- 앞 세션의 접어둔 항목이 그대로 유효하다 — 적 사망 연출 분리, 적 상태 표시 다시 심기, `HitActorsThisSwing` 리네임, 플레이어 `BeginPlay` HP 초기화, Mixamo 외부 베기 애니메이션, 진짜 칼 메시, `heldTransform` 회전·오프셋 기록, 적 공격 이펙트·사운드, `MM_Attack_02/03`·`MM_ChargedAttack`, `TriggerBox` + 레벨 블루프린트로 클리어 트리거 만들기
- **기성 애셋(Fab 무료 중세 팩) 도입.** 원본 프로젝트가 간 길이지만 이 프로젝트 성격과 어긋난다고 봤다
- **횃불을 Niagara 이펙트로 만들기.** MCP에 Niagara 툴셋이 없다
