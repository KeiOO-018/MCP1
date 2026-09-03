# 2026-09-03

## 작업물

로비를 중세 성 내부로 만드는 1차 작업 — 문간 높이 `200`→`400`, 로비 천장, 실내 조명 `18`개, 석재·목재 재질, 횃불 액터 `BP_Torch`.

**소요 시간**: 약 `3`시간 `40`분. 근거는 파일 mtime이다 — 직전 세션 기록이 `18:00`, 이 세션의 첫 터미널 보고(`45`)가 `18:46`, 마지막 보고(`55`)가 `21:37`이다. 사양 작성과 심문이 그 앞에 있었다.

## 명령

### 한글

> 작업 준비 하고 나서 중세풍 디자인을 어떻게 구현할 것인가에 대해 고민해보는 시간을 가져보자 저게 컨셉이 중세 성 인데 지금 보면 계단도 대충만들고 벽도 대충 바닥도 대충 문도 폴리없이 대충 했잔아 등등 내부 꾸미는 요소들도 확인해야하고 게임 소개 파일에 있는데 이것에 대해 고민해보기

(이어서 AI가 `AskUserQuestion`으로 물은 넷에 답한 것)

> 목표 수준 = 실루엣까지 만든다
> 경로 = A. 재질 + 조명 마감, B. 프리미티브 조립 키트, C. OBJ를 직접 써서 임포트
> 범위 = 로비 먼저
> 작업 주체 = 전부 Terminal 명령문으로

> 키워보자 그리고 견적 제보자

> 저건 저것들 할때 할까 저 미결들이 큰 영향을 줌?

> 일단 그냥 진행하자

> 결과 확인

> 커밋하자 PIE에서 저 3가지 다 이상없다

> 1. 1층 왼쪽 오른쪽 방에 각각 입구 문 양 옆에 1층 북쪽 방 문 양 옆 과 같은 조명 배치 하기
> 2. 2층 중앙 문 조명도 1층과 같이 문 양 옆에 조명 배치하기

> 세번째 사진에 보면 문 중앙에도 밝잔아 저기에도 조명 하나 있던데 2층 중앙문에 저거 의도인지 확인

> 스폰지점에서 바로 천장보기 확인

> 일단 명령 수행중임 기둘

> 결과 봐바ㅗ

> 커밋하자

> 일단 문짝목재랑 횃불 먼저 만들어볼까 횃불은 메시야 이펙트로해?

> 후자로 하자그럼

> 두번째사진이 로비 남쪽인데 이렇게보임

> 석재만하자일단

> 결과 확인과 오늘의 작업 정리 및 기록과 다음 세션을 위한 준비

**옮기며 넣은 해석이 셋 있다.**

첫째, `"키워보자"`에는 **얼마나 키울지가 없다.** 내가 `400`으로 정했다. 근거는 1층 벽 전체 높이가 `400`이라 새 인방을 안 만들어도 위층 벽이 인방이 된다는 것이고, 타일 `200`의 정확히 `2`칸이라는 것이다. `600` 같은 다른 값이었으면 2층 바닥 슬래브(`Z 550`)를 뚫어야 해서 비용이 완전히 달라진다.

둘째, `"1층 북쪽 방 문 양 옆 과 같은 조명 배치"`에서 **"같은"이 무엇을 가리키는지**를 내가 정했다. 기존 `Torch_1F_N_2`(`1050, -400`)와 `_N_3`(`1050, 400`)이 방2 문간(`Y -100..100`) 중심에서 `±400`씩 떨어져 있는 것을 보고, **그 `±400`이라는 간격**을 나머지 문 셋에 옮겼다. 사용자가 `±400`이라고 말한 적은 없다.

셋째, `"석재만하자일단"`이 **범위를 로비로 유지하라는 뜻인지 아닌지**가 모호했다. 나는 로비만 자르는 것이 기술적으로 불가능하다고 판단하고(아래 `무엇을 만들었나` 참조) 레벨 전체에 적용했다. 그 판단을 명령을 내기 전에 사용자에게 밝히고 진행했다.

### English — MCP에 실제로 보낸 명령

명령 `45`~`55` 열한 개다. 각 명령의 전문은 해당 `Docs/Terminal-Log/` 파일 첫머리에도 그대로 인용돼 있다.

**명령 45 — 문간 상단 벽 분할**

```
In the currently open level /Game/ThirdPerson/Lvl_Stage, raise the three ground-floor
doorways and the second-floor final doorway from 200 units tall to 400 units tall.

All actors below use SM_Cube (/Game/LevelPrototyping/Meshes/SM_Cube), whose pivot is at
its MINIMUM corner and whose unscaled size is 100 x 100 x 100. Therefore actor location
is the minimum corner of the resulting box, and actor scale is size divided by 100.
Every actor listed here currently has rotation (0,0,0). Keep rotation at (0,0,0)
everywhere. Do not add or change any material.

STEP 1 - Split the three continuous upper walls (Z 200..400) so that the doorway gaps
in the lower walls below them continue up to Z 400.

  1a) Rename the existing actor "Wall_Lobby_W_Upper" to "Wall_Lobby_W_UpperA".
      Keep its location at (-1300, -1600, 200). Set its scale to (9, 2, 2).
      Expected world bounds: X -1300..-400, Y -1600..-1400, Z 200..400.

  1b) Create a new StaticMeshActor using SM_Cube, labeled "Wall_Lobby_W_UpperB",
      at location (-200, -1600, 200), rotation (0, 0, 0), scale (15, 2, 2).
      Expected world bounds: X -200..1300, Y -1600..-1400, Z 200..400.

  1c) Rename the existing actor "Wall_Lobby_E_Upper" to "Wall_Lobby_E_UpperA".
      Keep its location at (-1300, 1400, 200). Set its scale to (9, 2, 2).
      Expected world bounds: X -1300..-400, Y 1400..1600, Z 200..400.

  1d) Create a new StaticMeshActor using SM_Cube, labeled "Wall_Lobby_E_UpperB",
      at location (-200, 1400, 200), rotation (0, 0, 0), scale (15, 2, 2).
      Expected world bounds: X -200..1300, Y 1400..1600, Z 200..400.

  1e) Rename the existing actor "Wall_Lobby_N_Upper" to "Wall_Lobby_N_UpperA".
      Keep its location at (1100, -1600, 200). Set its scale to (2, 15, 2).
      Expected world bounds: X 1100..1300, Y -1600..-100, Z 200..400.

  1f) Create a new StaticMeshActor using SM_Cube, labeled "Wall_Lobby_N_UpperB",
      at location (1100, 100, 200), rotation (0, 0, 0), scale (2, 15, 2).
      Expected world bounds: X 1100..1300, Y 100..1600, Z 200..400.

STEP 2 - Shrink the second-floor lintel so the final doorway becomes Z 600..1000.

  2a) On the existing actor "Wall_2F_N_Lintel", set location to (1100, -100, 1000)
      and scale to (2, 2, 2). Keep rotation (0, 0, 0).
      Expected world bounds: X 1100..1300, Y -100..100, Z 1000..1200.

DO NOT touch any other actor. In particular do not move, resize, rename or delete
Wall_Lobby_W_LowerA, Wall_Lobby_W_LowerB, Wall_Lobby_E_LowerA, Wall_Lobby_E_LowerB,
Wall_Lobby_N_LowerA, Wall_Lobby_N_LowerB, Wall_2F_W, Wall_2F_E, Wall_2F_N_A,
Wall_2F_N_B, Wall_2F_N_Sill, Door_R1, Door_R2, Door_R3 or Door_Final.

VERIFY AND REPORT. After the edits, read back and report the actual world bounding box
of each of these 11 actors, and say for each whether it matches the expected bounds
above: Wall_Lobby_W_UpperA, Wall_Lobby_W_UpperB, Wall_Lobby_E_UpperA,
Wall_Lobby_E_UpperB, Wall_Lobby_N_UpperA, Wall_Lobby_N_UpperB, Wall_2F_N_Lintel,
Wall_2F_W, Wall_2F_E, Wall_2F_N_Sill, Wall_2F_N_Lintel.
Also report the total actor count in the level before and after.
Report any warning or error text verbatim in English; do not summarize or translate it.

Write the report to Docs/Terminal-Log/2026-09-03-45-doorway-height-400.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

**명령 46 — 문짝 높이 (실패)**

```
In the currently open level /Game/ThirdPerson/Lvl_Stage, make the door leaves match the
doorways that were just raised to 400 units tall.

Background you need for the numbers: BP_Door's DoorMesh component uses the static mesh
SM_Door (/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door). SM_Door is a
200 x 200 x 200 box whose pivot is at its CENTER, not at a corner. The leaf is centered
on the door actor's origin, so doubling the mesh's Z scale and raising the actor by 100
turns a leaf that spans Z 0..200 into one that spans Z 0..400.

STEP 1 - Edit the Blueprint class default.

  1a) Open the Blueprint /Game/Interaction/BP_Door. On its DoorMesh component, change
      RelativeScale3D from (0.05, 0.5, 1.0) to (0.05, 0.5, 2.0).
      Do NOT change RelativeLocation, which must stay (0, 50, 0).
      Do NOT change the StaticMesh, the Hinge component, any variable, or any graph.
  1b) Compile the Blueprint. Report the compile result verbatim.
  1c) Save the Blueprint asset to disk, and confirm it was written.

STEP 2 - Raise the four door actors in the level by 100 units. Change ONLY the Z of the
location. Keep X, Y, rotation and scale exactly as they are.

  2a) Door_R1     from (-400, -1500, 100) to (-400, -1500, 200). Rotation yaw -90, scale (1, 2, 1).
  2b) Door_R2     from (1200,  -100, 100) to (1200,  -100, 200). Rotation yaw   0, scale (1, 2, 1).
  2c) Door_R3     from (-400,  1500, 100) to (-400,  1500, 200). Rotation yaw -90, scale (1, 2, 1).
  2d) Door_Final  from (1200,  -100, 700) to (1200,  -100, 800). Rotation yaw   0, scale (1, 2, 1).

STEP 3 - Confirm the class default actually reached every instance. On EACH of the four
door actors, read back the DoorMesh component's RelativeScale3D. If any of them still
reads (0.05, 0.5, 1.0), that instance had an override, so set (0.05, 0.5, 2.0) directly
on that instance and say in the report which instances needed it.

DO NOT touch any wall, floor, ramp, railing, pillar, enemy, item pickup, BP_StageRoom,
BP_EndTrigger or the GameMode.

VERIFY AND REPORT.

  A) For each of the four door actors report: world location, rotation, actor scale, and
     the DoorMesh component's RelativeLocation and RelativeScale3D.

  B) Run these line traces with SceneTools.trace_world and report the returned distance
     for every one of them. A number near 195 means the leaf is blocking. A null means
     there is still a hole.

     Room 1 doorway,  for z = 30, 150, 250, 350, 390:
       start (-300, -1300, z)  end (-300, -1700, z)
     Room 3 doorway,  for z = 30, 150, 250, 350, 390:
       start (-300,  1300, z)  end (-300,  1700, z)
     Room 2 doorway,  for z = 30, 150, 250, 350, 390:
       start (1000,     0, z)  end (1400,     0, z)
     Final doorway,   for z = 630, 750, 850, 950, 990:
       start (1000,     0, z)  end (1400,     0, z)

     All 20 traces are expected to return a distance near 195, and none of them is
     expected to return null.

  C) Report the total actor count in the level.

  D) Report any warning or error text verbatim in English. Do not summarize or translate.

Write the report to Docs/Terminal-Log/2026-09-03-46-door-leaf-height-400.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

**명령 47 — 문짝 높이, 액터 스케일 우회**

```
In the currently open level /Game/ThirdPerson/Lvl_Stage, finish raising the door leaves.
Command 46 could not do it through the component; this command does it through the
actor scale instead.

Why: the leaf size is SM_Door (200 x 200 x 200, pivot centered) multiplied by the
DoorMesh component scale (0.05, 0.5, 1.0) and then by the door actor's scale (1, 2, 1).
Command 46 proved that ObjectTools.set_properties silently refuses to write
RelativeScale3D on these component instances, but ActorTools.set_actor_transform does
work on the actors. Setting the actor Z scale from 1 to 2 produces the same 400-tall
leaf without touching any component.

STEP 1 - Undo the class default change made by command 46, so it cannot take effect
later if the per-instance overrides are ever cleared.

  1a) Open /Game/Interaction/BP_Door. On its DoorMesh component, set RelativeScale3D
      back to (0.05, 0.5, 1.0).
  1b) Compile the Blueprint and report the result verbatim.
  1c) Save the Blueprint asset and confirm it was written to disk.
  1d) Read back the class default and confirm it now reads (0.05, 0.5, 1.0).

STEP 2 - Set the actor scale on the four doors. Use ActorTools.set_actor_transform.
Change ONLY the Z component of the scale, from 1 to 2. Keep location and rotation
exactly as they are.

  2a) Door_R1     location (-400, -1500, 200), rotation yaw -90, scale (1, 2, 1) -> (1, 2, 2)
  2b) Door_R2     location (1200,  -100, 200), rotation yaw   0, scale (1, 2, 1) -> (1, 2, 2)
  2c) Door_R3     location (-400,  1500, 200), rotation yaw -90, scale (1, 2, 1) -> (1, 2, 2)
  2d) Door_Final  location (1200,  -100, 800), rotation yaw   0, scale (1, 2, 1) -> (1, 2, 2)

DO NOT change any component property on any door. DO NOT delete or re-create any door
actor - each one carries per-instance Blueprint state (bLocked, RequiredKey, tags) and
three BP_StageRoom actors hold references to them. DO NOT reload the level: the wall
changes from command 45 are still unsaved in memory.

STEP 3 - Save. After the verification below passes, save the level so command 45's wall
edits and this command's door edits both reach disk. Report which packages were written.

VERIFY AND REPORT.

  A) For each of the four doors report world location, rotation, actor scale, and the
     DoorMesh component's RelativeLocation and RelativeScale3D. The component values are
     expected to be UNCHANGED at RelativeLocation (0, 50, 0) and RelativeScale3D
     (0.05, 0.5, 1.0) - this command deliberately does not touch them.

  B) Run these line traces with SceneTools.trace_world and report the distance for each.
     A number near 195 means the leaf is blocking. A null means a hole is still there.

     Room 1 doorway, for z = 30, 150, 250, 350, 390:
       start (-300, -1300, z)  end (-300, -1700, z)
     Room 3 doorway, for z = 30, 150, 250, 350, 390:
       start (-300,  1300, z)  end (-300,  1700, z)
     Room 2 doorway, for z = 30, 150, 250, 350, 390:
       start (1000,     0, z)  end (1400,     0, z)
     Final doorway,  for z = 630, 750, 850, 950, 990:
       start (1000,     0, z)  end (1400,     0, z)

     All 20 are expected to return a distance near 195. None is expected to return null.

  C) Report the actor bounding box of each of the four doors.

  D) Report the total actor count in the level, and confirm no actor was created or
     deleted by this command.

  E) Report any warning or error text verbatim in English. Do not summarize or translate.

Write the report to Docs/Terminal-Log/2026-09-03-47-door-leaf-via-actor-scale.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

**명령 48 — 로비 천장**

```
In the currently open level /Game/ThirdPerson/Lvl_Stage, add a ceiling slab over the
lobby. This is one new actor and nothing else.

Purpose: this level has no ceiling anywhere, so the lobby is lit by the outdoor sky.
Capping the lobby cuts that sky light for the lobby ONLY, which is what makes it
possible to relight the lobby with torches without darkening rooms 1, 2 and 3.

The slab covers the whole lobby footprint including the walls, so there is no seam at
the wall faces and the wall tops are capped. The lobby's second-floor walls all end at
Z 1200, so the slab sits directly on top of them.

  Create a new StaticMeshActor using SM_Cube
  (/Game/LevelPrototyping/Meshes/SM_Cube), labeled "Ceiling_Lobby",
  at location (-1300, -1600, 1200), rotation (0, 0, 0), scale (26, 32, 0.5).

  SM_Cube's pivot is at its minimum corner and its unscaled size is 100 x 100 x 100,
  so this gives world bounds X -1300..1300, Y -1600..1600, Z 1200..1250.

  Do not set a material. It must inherit SM_Cube's own material, the same way every
  wall in this level does.

DO NOT touch any other actor. DO NOT edit any Blueprint. DO NOT change any light,
the SkyLight, the SkyAtmosphere, the DirectionalLight, the ExponentialHeightFog or the
PostProcessVolume - this command only adds geometry.

STEP 2 - Save, using AssetTools.save_assets with an empty list. Report which packages
were written, verified on disk and not from the return value.

VERIFY AND REPORT.

  A) Report Ceiling_Lobby's location, rotation, scale, world bounding box, static mesh
     and OverrideMaterials, and say whether the bounds match X -1300..1300,
     Y -1600..1600, Z 1200..1250.

  B) Confirm the slab actually seals. Run these downward line traces with
     SceneTools.trace_world and report the distance for each. Each starts at Z 2000 and
     ends at Z 0 at the same X and Y. A distance of 750 means it hit the top of the slab
     at Z 1250. A larger number or a null means there is a hole.

       ( 0,     0)   ( 700,     0)   (-1000,     0)
       (-1000, -1300) ( 1000, -1300) (-1000,  1300) ( 1000,  1300)
       ( 1200,     0) (-1200,     0) ( 0,    -1500) ( 0,     1500)

  C) Report the total actor count before and after. Exactly one actor is expected to be
     added.

  D) Report any warning or error text verbatim in English. Do not summarize or translate.

Write the report to Docs/Terminal-Log/2026-09-03-48-lobby-ceiling.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

**명령 49 — 조명 13개**

```
In the currently open level /Game/ThirdPerson/Lvl_Stage, add point lights to the lobby.
It is completely dark since command 48 capped it, so nothing can be judged until there
is light in it.

Create 13 PointLight actors. Put every one of them in the outliner folder "Lighting",
which already exists in this level.

Settings shared by ALL 13 lights:
  Mobility        = Movable
  LightColor      = R 255, G 170, B 90   (warm torch colour)
  IntensityUnits  = Unitless
  SourceRadius    = 10
  CastShadows     = true
  Rotation        = (0, 0, 0)

GROUP 1 - ground floor wall torches. Z 250, 50 units off the wall face.
Intensity 5000, AttenuationRadius 1200 for all eight.

  Torch_1F_S_1   (-1050, -1200, 250)
  Torch_1F_S_2   (-1050,  -400, 250)
  Torch_1F_S_3   (-1050,   400, 250)
  Torch_1F_S_4   (-1050,  1200, 250)
  Torch_1F_N_1   ( 1050, -1200, 250)
  Torch_1F_N_2   ( 1050,  -400, 250)
  Torch_1F_N_3   ( 1050,   400, 250)
  Torch_1F_N_4   ( 1050,  1200, 250)

GROUP 2 - second floor gallery torches. Z 850, which is 250 above the 2F walking
surface at Z 600. Intensity 5000, AttenuationRadius 1200 for all four.

  Torch_2F_W_1   (-700, -1350, 850)
  Torch_2F_W_2   ( 300, -1350, 850)
  Torch_2F_E_1   (-700,  1350, 850)
  Torch_2F_E_2   ( 300,  1350, 850)

GROUP 3 - the key light, in front of the final door on the second floor. This is the
one dominant warm light the room reads from.

  KeyLight_FinalDoor   (1000, 0, 900)
  Intensity 20000, AttenuationRadius 2500

DO NOT change the existing DirectionalLight, SkyLight, SkyAtmosphere, VolumetricCloud,
ExponentialHeightFog or PostProcessVolume. Rooms 1, 2 and 3 still have no ceiling and
are lit by those; touching them would darken the rooms too. DO NOT edit any Blueprint,
move any wall, floor, door, ramp, railing or pillar, and do not add any mesh.

STEP 2 - Save with AssetTools.save_assets and an empty list. Report which packages were
written, verified on disk and not from the return value.

VERIFY AND REPORT.

  A) For all 13 lights report the actual world location, Mobility, Intensity,
     IntensityUnits, AttenuationRadius, LightColor and CastShadows, read back after
     creation. Say for each whether it matches what was asked. If any property could not
     be set, say so plainly and give the error verbatim rather than reporting success.

  B) Report the outliner folder each light ended up in.

  C) Report the total actor count before and after. Exactly 13 are expected to be added.

  D) Confirm by reading them back that the DirectionalLight, SkyLight and
     PostProcessVolume are unchanged, and report their Intensity values.

  E) Report any warning or error text verbatim in English. Do not summarize or translate.

Write the report to Docs/Terminal-Log/2026-09-03-49-lobby-lights.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

**명령 50 — 문 양옆 조명 6개**

```
In the currently open level /Game/ThirdPerson/Lvl_Stage, add 6 more PointLight actors so
that all four doorways have a torch on each side, matching the pair that already flanks
the Room 2 doorway (Torch_1F_N_2 and Torch_1F_N_3, which sit 400 units to either side of
that doorway's centre line).

Every one of the 6 uses EXACTLY the same settings as the 12 existing torches:
  Mobility        = Movable
  Intensity       = 5000
  IntensityUnits  = Unitless
  AttenuationRadius = 1200
  LightColor      = R 255, G 170, B 90
  SourceRadius    = 10
  CastShadows     = true
  Rotation        = (0, 0, 0)
  Outliner folder = "Lighting"

GROUP 1 - ground floor, Room 1 doorway (the left / west one). That doorway is the gap
X -400..-200 in the wall at Y -1600..-1400, so its centre is X -300 and the wall's inner
face is Y -1400. Lights go 50 units off that face at Y -1350, and 400 units to either
side of X -300.

  Torch_1F_W_1   (-700, -1350, 250)
  Torch_1F_W_2   ( 100, -1350, 250)

GROUP 2 - ground floor, Room 3 doorway (the right / east one). Same doorway shape,
mirrored to the wall at Y 1400..1600.

  Torch_1F_E_1   (-700, 1350, 250)
  Torch_1F_E_2   ( 100, 1350, 250)

GROUP 3 - second floor, the final door in the middle of the north wall. That doorway is
the gap Y -100..100 in the wall at X 1100..1300, at Z 600..1000. Its centre is Y 0 and
the wall's inner face is X 1100. Lights go 50 units off that face at X 1050, 400 units
to either side of Y 0, at Z 850 - which is 250 above the second floor walking surface at
Z 600, the same height above the floor as the ground floor torches.

  Torch_2F_N_1   (1050, -400, 850)
  Torch_2F_N_2   (1050,  400, 850)

DO NOT move, delete or change any of the 13 lights that already exist, including
KeyLight_FinalDoor. DO NOT change the DirectionalLight, SkyLight, SkyAtmosphere,
VolumetricCloud, ExponentialHeightFog or PostProcessVolume. DO NOT edit any Blueprint or
touch any mesh, wall, floor, door, ramp, railing or pillar.

STEP 2 - Save with AssetTools.save_assets and an empty list. Do not use save_actor - it
fails on external actor packages that have not been written yet. Verify on disk that 6
new packages appeared under Content/__ExternalActors__/ThirdPerson/Lvl_Stage/, and do
not report success from the return value alone.

VERIFY AND REPORT.

  A) For each of the 6 new lights report the world location, Mobility, Intensity,
     IntensityUnits, AttenuationRadius, LightColor, SourceRadius, CastShadows and
     outliner folder, read back after creation.

  B) Read back all 12 pre-existing torches and KeyLight_FinalDoor and confirm none of
     them changed. Report their Intensity and location.

  C) Report the total actor count before and after. Exactly 6 are expected to be added.

  D) Report which packages were written to disk.

  E) Report any warning or error text verbatim in English. Do not summarize or translate.

Write the report to Docs/Terminal-Log/2026-09-03-50-doorway-flanking-torches.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

**명령 51 — 키 라이트 삭제**

```
In the currently open level /Game/ThirdPerson/Lvl_Stage, delete the PointLight actor
labeled "KeyLight_FinalDoor". It sits at (1000, 0, 900) with Intensity 20000 and
AttenuationRadius 2500, and it is the only light in the level that does not use the
shared torch settings.

Reason: command 50 added Torch_2F_N_1 and Torch_2F_N_2 flanking that same doorway, so
the area is now lit three times over and is blown out. Removing this one leaves all four
doorways with the same treatment - exactly two flanking torches - and leaves every light
in the level at Intensity 5000 / AttenuationRadius 1200.

Delete ONLY that actor. Do not touch the 18 torches, the DirectionalLight, the SkyLight,
the SkyAtmosphere, the VolumetricCloud, the ExponentialHeightFog or the
PostProcessVolume. Do not edit any Blueprint, mesh, wall, floor, door, ramp, railing or
pillar.

STEP 2 - Save with AssetTools.save_assets and an empty list. Verify on disk that the
actor's external package was removed, and do not report success from the return value
alone.

VERIFY AND REPORT.

  A) Confirm no actor labeled "KeyLight_FinalDoor" remains in the level.
  B) List all remaining PointLight actors with their label, world location, Intensity and
     AttenuationRadius. Exactly 18 are expected, all at Intensity 5000 and
     AttenuationRadius 1200.
  C) Report the total actor count before and after. Exactly one actor should be removed.
  D) Report which packages were written or deleted on disk.
  E) Report any warning or error text verbatim in English. Do not summarize or translate.

Write the report to Docs/Terminal-Log/2026-09-03-51-remove-final-door-key-light.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

이 명령은 **PIE가 켜져 있어서 터미널이 실행을 거부했다.** 사용자가 PIE를 끈 뒤 다음 한 줄을 덧붙여 다시 보냈다.

```
PIE is stopped now. IsPIERunning returns false, the actor count is back to 121, and no
refPath contains UEDPIE. Go ahead with the deletion of KeyLight_FinalDoor as originally
instructed, re-checking IsPIERunning yourself first.
```

**명령 52 — 석재 재질**

```
In the currently open project, create a stone MaterialInstance and put it on the three
prototype meshes the level is built from.

Do NOT author a new Material from scratch. /Game/LevelPrototyping/Materials/
M_PrototypeGrid already exposes every parameter needed, including separate colours for
upward-facing surfaces, so a MaterialInstance of it is enough.

STEP 1 - Create a MaterialInstanceConstant.

  Folder  /Game/LevelPrototyping/Materials
  Name    MI_Castle_Stone
  Parent  /Game/LevelPrototyping/Materials/M_PrototypeGrid

STEP 2 - Set these parameters on it. Every one is an override on the instance.

  Scalar parameters
    Grid Size   200        (was 100 on MI_PrototypeGrid_Gray; 200 makes one block equal
                            one 2 m floor tile, the module this level is built on)
    Roughness   1.0

  Vector parameters - side faces, i.e. walls
    SurfaceColor          R 0.135  G 0.125  B 0.112
    GridColor             R 0.045  G 0.042  B 0.038
    SubGridColor          R 0.090  G 0.085  B 0.078

  Vector parameters - upward faces, i.e. floors and the ceiling underside
    TopSurfaceColor       R 0.115  G 0.110  B 0.102
    TopGridColor          R 0.040  G 0.038  B 0.035
    TopSubGridGridColor   R 0.080  G 0.076  B 0.070

  If any of these parameter names does not exist on M_PrototypeGrid, do NOT guess a
  different name. Report the exact list of parameter names the material actually exposes
  and stop.

STEP 3 - Assign it to the material slot of the three meshes the level geometry uses.
All three currently point at MI_PrototypeGrid_Gray on a slot named "lambert1".

  /Game/LevelPrototyping/Meshes/SM_Cube        slot lambert1
  /Game/LevelPrototyping/Meshes/SM_Cylinder    slot lambert1
  /Game/LevelPrototyping/Meshes/SM_Ramp        slot lambert1

DO NOT touch SM_Door, M_FlatCol, MI_DefaultColorway, or any of the existing
MI_PrototypeGrid_* instances - leave all of them exactly as they are. DO NOT set a
material override on any actor. DO NOT edit any Blueprint, move any actor, or change any
light.

STEP 4 - Save with AssetTools.save_assets and an empty list. Report which packages were
written, verified on disk and not from the return value.

VERIFY AND REPORT.

  A) Read back MI_Castle_Stone and report its Parent plus every scalar and vector
     parameter override it now carries, with values. Say for each whether it matches
     what was asked.

  B) Read back the material assigned to slot lambert1 on SM_Cube, SM_Cylinder and
     SM_Ramp and confirm all three are MI_Castle_Stone.

  C) Read back SM_Door's slot Material_0 and confirm it is still M_FlatCol, and read
     back MI_PrototypeGrid_Gray's parameters and confirm they are unchanged.

  D) Report EditorToolset.EditorAppToolset.IsPIERunning. If it returns true, stop before
     making any change and say so - with PIE running the tools resolve against the
     UEDPIE_0_ copy of the world, not the editor world.

  E) Report which packages were written to disk.

  F) Report any warning or error text verbatim in English. Do not summarize or translate.

Write the report to Docs/Terminal-Log/2026-09-03-52-castle-stone-material.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

**명령 53 — 목재 재질**

```
In the currently open project, give the door leaves a wood material.

SM_Door (/Game/LevelPrototyping/Interactable/Door/Meshes/SM_Door) currently points its
only slot, "Material_0", directly at the material /Game/LevelPrototyping/Materials/
M_FlatCol with no instance in between, so all four doors render as a flat grey slab. In
the now-dark lobby that reads as a hole rather than a door.

STEP 1 - Create a MaterialInstanceConstant.

  Folder  /Game/LevelPrototyping/Materials
  Name    MI_Castle_Wood
  Parent  /Game/LevelPrototyping/Materials/M_FlatCol

STEP 2 - Set these parameters on it.

  Vector parameter
    Base Color   R 0.055  G 0.032  B 0.018

  Scalar parameter
    Roughness    0.75

  The parameter is named "Base Color" with a space - that is the name
  MI_DefaultColorway uses on this same parent. If either name does not exist, do NOT
  guess a different one: report the exact list of parameters M_FlatCol exposes and stop.

STEP 3 - Assign MI_Castle_Wood to SM_Door, slot "Material_0".

DO NOT modify M_FlatCol itself, MI_DefaultColorway, MI_Castle_Stone,
MI_PrototypeGrid_Gray or any other existing material. DO NOT touch SM_Cube, SM_Cylinder
or SM_Ramp. DO NOT edit any Blueprint, move any actor, or change any light.

STEP 4 - Save with AssetTools.save_assets and an empty list. Report which packages were
written, verified on disk and not from the return value.

VERIFY AND REPORT.

  A) Report EditorToolset.EditorAppToolset.IsPIERunning first. If it returns true, make
     no change and stop - with PIE running the tools resolve against the UEDPIE_0_ copy
     of the world rather than the editor world.

  B) Read back MI_Castle_Wood and report its Parent and every parameter override with
     values, saying whether each matches what was asked.

  C) Read back SM_Door slot Material_0 and confirm it is MI_Castle_Wood.

  D) Read back M_FlatCol and MI_DefaultColorway and confirm neither changed. Report
     MI_DefaultColorway's Base Color and Roughness.

  E) Report which packages were written to disk.

  F) Report any warning or error text verbatim in English. Do not summarize or translate.

Write the report to Docs/Terminal-Log/2026-09-03-53-door-wood-material.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

**명령 54 — `M_Flame`과 `BP_Torch`**

```
In the currently open project, create a torch. This command creates assets ONLY - it
must not add, move or delete any actor in the level, and must not touch the 18 existing
PointLight actors. Replacing them comes in a separate command.

Background for the geometry: the torch will be placed against a wall, at the exact
positions the 18 existing PointLight actors occupy. Those sit 50 units out from the wall
face. So build the torch in local space with the wall behind it at local X = -50, and
the torch pointing along local +X into the room. Each placement will then just need a
yaw to face the right wall.

STEP 1 - Create an emissive flame material.

  Folder  /Game/LevelPrototyping/Materials
  Name    M_Flame
  Shading model unlit if the material supports it, otherwise leave the default.

  Graph: a constant colour of R 1.0, G 0.45, B 0.12 multiplied by a scalar of 30,
  connected to Emissive Color. Expose the colour as a vector parameter named
  "FlameColor" and the scalar as a scalar parameter named "FlameBrightness" so both can
  be tuned from an instance later. Compile it and report the compile result verbatim.

STEP 2 - Create an Actor Blueprint.

  Folder  /Game/Interaction
  Name    BP_Torch
  Parent class  Actor

  Set bCanEverTick to false.
  Add NO variables and NO event graph logic. This actor is geometry and a light, nothing
  more.

STEP 3 - Add five components to BP_Torch. All local transforms are relative to the
actor origin. The actor origin is where the light goes, so that placing BP_Torch at an
existing PointLight's coordinates reproduces that light exactly.

  1. "Backplate"  cube,     dimensions X 12, Y 16, Z 34,  local location (-46, 0, -24)
  2. "Bracket"    cylinder, radius 5,  height 55,          local location (-24, 0, -22),
                                                           local rotation pitch 55
  3. "Cup"        cone,     radius 13, height 20,          local location (0, 0, -24)
  4. "Flame"      cone,     radius 9,  height 30,          local location (0, 0, -14)
  5. "Light"      PointLight component,                    local location (0, 0, 0)

  Cup must open upward like a bowl. If the cone primitive is created with its apex up
  and its base down, rotate Cup by 180 degrees so the apex points down. Flame keeps the
  default orientation, apex up.

  Assign M_Flame to the Flame component only. Backplate, Bracket and Cup take
  /Game/LevelPrototyping/Materials/MI_Castle_Stone.

  Set the Light component to exactly the values the 18 existing PointLight actors use:
    Mobility          Movable
    Intensity         5000
    IntensityUnits    Unitless
    AttenuationRadius 1200
    SourceRadius      10
    CastShadows       true
    LightColor        R 255, G 170, B 90

  Give the Flame component CastShadow false and collision disabled, so the flame mesh
  does not block its own light.

STEP 4 - Compile and save BP_Torch and M_Flame. Save with AssetTools.save_assets and an
empty list. Report which packages were written, verified on disk.

DO NOT create, move or delete any actor in the level. DO NOT touch the 18 PointLight
actors, any wall, floor, door, ramp, railing or pillar. DO NOT modify MI_Castle_Stone,
MI_Castle_Wood, M_FlatCol, M_PrototypeGrid or any MI_PrototypeGrid_* instance.

VERIFY AND REPORT.

  A) Report EditorToolset.EditorAppToolset.IsPIERunning first. If true, stop and say so.

  B) List every component on BP_Torch with its name, type, local location, local
     rotation, local scale, assigned material, and - for the mesh components - the
     LOCAL-SPACE bounding box the component actually occupies. I need the real bounds
     because I do not know this toolset's pivot and axis convention for cube, cylinder
     and cone primitives, and the numbers above were written assuming Z-up shapes.
     Report what they really are rather than what was asked for.

  C) Report the combined local bounding box of the whole actor, so I can tell how far
     the torch sticks out from the wall and how tall it is.

  D) Report every property of the Light component, and say whether each matches the
     values listed in STEP 3.

  E) Confirm the level was not modified: report the total actor count and confirm it is
     120, the same as before this command.

  F) Report which packages were written to disk.

  G) Report any warning or error text verbatim in English. Do not summarize or translate.

Write the report to Docs/Terminal-Log/2026-09-03-54-torch-blueprint.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

**명령 55 — 횃불 18개 배치와 조명 18개 삭제**

```
In the currently open level /Game/ThirdPerson/Lvl_Stage, replace the 18 bare PointLight
actors with 18 BP_Torch actors, so each torch is one actor carrying both its mesh and
its light.

Order matters: create all 18 first, verify them, and only then delete the 18 PointLight
actors. Do not delete anything before the 18 new actors are confirmed present. The 18
labels are reused, so during the middle of this command two actors will briefly share
each label - that is expected and harmless, because the delete step targets actors whose
class is PointLight, never BP_Torch.

BP_Torch is built pointing along its local +X with the wall behind it at local X = -50,
and its origin is where the light sits. So each actor goes at the exact coordinates the
PointLight it replaces occupies, and only the yaw differs, chosen so local +X points
into the room.

STEP 1 - Create 18 actors from /Game/Interaction/BP_Torch. Rotation is (pitch 0, yaw as
listed, roll 0) and scale (1, 1, 1) for every one. Put all 18 in the outliner folder
"Lighting".

  Label            Location              Yaw    Wall it hangs on
  Torch_1F_S_1     (-1050, -1200, 250)     0    south, X -1100
  Torch_1F_S_2     (-1050,  -400, 250)     0    south
  Torch_1F_S_3     (-1050,   400, 250)     0    south
  Torch_1F_S_4     (-1050,  1200, 250)     0    south
  Torch_1F_N_1     ( 1050, -1200, 250)   180    north, X 1100
  Torch_1F_N_2     ( 1050,  -400, 250)   180    north
  Torch_1F_N_3     ( 1050,   400, 250)   180    north
  Torch_1F_N_4     ( 1050,  1200, 250)   180    north
  Torch_1F_W_1     ( -700, -1350, 250)    90    west,  Y -1400
  Torch_1F_W_2     (  100, -1350, 250)    90    west
  Torch_1F_E_1     ( -700,  1350, 250)   -90    east,  Y 1400
  Torch_1F_E_2     (  100,  1350, 250)   -90    east
  Torch_2F_W_1     ( -700, -1350, 850)    90    west
  Torch_2F_W_2     (  300, -1350, 850)    90    west
  Torch_2F_E_1     ( -700,  1350, 850)   -90    east
  Torch_2F_E_2     (  300,  1350, 850)   -90    east
  Torch_2F_N_1     ( 1050,  -400, 850)   180    north
  Torch_2F_N_2     ( 1050,   400, 850)   180    north

STEP 2 - Verify all 18 BP_Torch actors exist at the right transforms. If any is missing
or wrong, STOP HERE, delete nothing, and report what happened.

STEP 3 - Only after STEP 2 passes, delete the 18 actors whose class is PointLight. There
are exactly 18 of them and they carry the same 18 labels. Delete ONLY actors of class
PointLight. Do NOT delete the DirectionalLight, the SkyLight, or anything else.

STEP 4 - Save with AssetTools.save_assets and an empty list. Verify on disk which
packages were written and which were removed.

DO NOT touch the DirectionalLight, SkyLight, SkyAtmosphere, VolumetricCloud,
ExponentialHeightFog or PostProcessVolume. DO NOT edit any Blueprint, material or mesh
asset. DO NOT move any wall, floor, door, ramp, railing, pillar or the ceiling.

VERIFY AND REPORT.

  A) Report EditorToolset.EditorAppToolset.IsPIERunning first. If true, stop before
     making any change and say so.

  B) For each of the 18 BP_Torch actors report label, world location, rotation, scale,
     outliner folder, and the actor's world bounding box.

  C) Confirm zero actors of class PointLight remain in the level.

  D) Report the total actor count before and after. It should start at 120, rise to 138,
     and end at 120.

  E) Report which packages were written and which were removed on disk.

  F) Report any warning or error text verbatim in English. Do not summarize or translate.

Write the report to Docs/Terminal-Log/2026-09-03-55-place-torches.md
(a repo path - do NOT write under Saved/, it is gitignored).
```

## Terminal 결과

### 원문 — English

**이 세션은 명령 열한 개 전부에서 터미널 보고를 파일로 받았다.** 원문은 `Docs/Terminal-Log/2026-09-03-45..55`에 있고 합계 `240`KB가 넘는다. 아래는 발췌다 — **다만 실패·경고·어긋난 응답은 발췌하지 않고 전문을 붙였다.**

성공한 명령의 요약 줄만 먼저 옮긴다.

```
Command 45 — Headline: all 7 edits applied and read back clean. All the requested actors
have world bounds that match the expected bounds exactly, with no float residue —
every component is an exact integer. Actor count 98 before, 101 after (+3, the
three new B walls). No warning or error was emitted during the edit window. The
level is dirty in memory and was NOT saved.

Command 47 — All three steps succeeded. All 20 verification traces return a distance
near 195 and none returns null — the result command 46 could not reach. The four door
leaves now span the full 400-tall doorway. No component property was touched. No
actor was created, deleted or re-created. Everything is on disk: 12 packages written
in total.

Command 48 — One actor created. Nothing else touched. No Blueprint edited, no light or
atmosphere actor touched, no material set. Saved to disk.

Command 49 — 13 PointLight actors created, all 13 configured, all 13 in the "Lighting"
folder, all 13 saved to disk. No existing actor was modified — proven by the save
writing 13 new packages and zero modified ones.

Command 50 — 6 PointLight actors created, all 6 configured identically to the existing 12
torches, all 6 in the "Lighting" folder, all 6 saved to disk. All 13 pre-existing
lights verified byte-identical to a baseline captured before any write.

Command 51 — One actor deleted. Nothing else touched. Saved to disk, verified by a
before/after diff of the external actor package list: exactly one package
removed, zero added, zero modified.

Command 53 — One MaterialInstanceConstant created with both requested parameter overrides,
assigned to SM_Door's only slot, saved to disk. 2 packages written: 1 new, 1
modified. Nothing else changed. No warning or error was emitted by this command.

Command 54 — Two assets created: `M_Flame` (unlit emissive material, 2 exposed parameters)
and `BP_Torch` (Actor Blueprint, 5 components + DefaultSceneRoot, no variables, no
graph logic). Both compiled clean and saved. 2 packages written, both new.

Command 55 — 18 BP_Torch actors created and verified, then the 18 PointLight actors
deleted. Actor count 120 → 138 → 120. Zero PointLight-class actors remain. 18 packages
written and 18 removed on disk, a clean one-for-one swap.
```

**명령 46 — `STEP 3` 실패. 전문.**

```
STEP 1 succeeded and is on disk. STEP 2 succeeded. STEP 3 FAILED — the class
default did not reach a single instance, and it cannot be forced with what this
server exposes. The remedy STEP 3 prescribes was attempted on all four doors and
did not take. As a result 12 of the 20 verification traces return null.

### The read-back that triggered STEP 3

"Door_R1"    RelativeScale3D {"x":0.050000000000000003,"y":0.5,"z":1}
"Door_R2"    RelativeScale3D {"x":0.050000000000000003,"y":0.5,"z":1}
"Door_R3"    RelativeScale3D {"x":0.050000000000000003,"y":0.5,"z":1}
"Door_Final" RelativeScale3D {"x":0.050000000000000003,"y":0.5,"z":1}

All four instances needed the STEP 3 remedy. Not one of them picked up the
class default, even though the Blueprint had already been compiled and saved, and
even though STEP 2 had since written each actor's transform (which normally
reruns construction scripts).

### The remedy was attempted on all four and did not take

ObjectTools.set_properties on each instance's DoorMesh, values
{"RelativeScale3D":{"x":0.05,"y":0.5,"z":2.0}}:

"Door_R1":    {"set_returned": true, "after": "...\"RelativeScale3D\":{\"x\":0.050000000000000003,\"y\":0.5,\"z\":1}..."}
"Door_R2":    {"set_returned": true, "after": "...\"RelativeScale3D\":{\"x\":0.050000000000000003,\"y\":0.5,\"z\":1}..."}
"Door_R3":    {"set_returned": true, "after": "...\"RelativeScale3D\":{\"x\":0.050000000000000003,\"y\":0.5,\"z\":1}..."}
"Door_Final": {"set_returned": true, "after": "...\"RelativeScale3D\":{\"x\":0.050000000000000003,\"y\":0.5,\"z\":1}..."}

set_properties returned true four times and changed nothing. This is the
exact failure mode CLAUDE.md warns about: the MCP return value is not evidence.

### What else was tried, in order, and what each returned

1. ObjectTools.reset_properties (the documented tool for "removing any
per-instance overrides"), on Door_R2's DoorMesh, properties: ["RelativeScale3D"]:

{"returnValue":true}

Read-back:

{"RelativeScale3D":{"x":1,"y":0.5,"z":1},"RelativeLocation":{"x":0,"y":50,"z":0}}

This did write, but incoherently: X went 0.05 → 1, while Y stayed 0.5 and Z
stayed 1. It reset toward the native SceneComponent default of (1,1,1), not
toward the Blueprint archetype (0.05, 0.5, 2), and it only moved one component
of the vector.

2. set_properties again on Door_R2 with (0.05, 0.5, 2.0):
{"returnValue":true}
Read-back: {"RelativeScale3D":{"x":0.050000000000000003,"y":0.5,"z":1},...}

3. camelCase key. {"relativeScale3D":{"x":0.05,"y":0.5,"z":2.0}}:
{"returnValue":true}
Read-back: still {"x":0.050000000000000003,"y":0.5,"z":1}. Key casing is not
the cause.

4. The decisive controlled probe. Two writes on the same Door_R2 DoorMesh
component, each read back and each restored:

| bVisible baseline            | {"bVisible":true}
| set bVisible false           | true
| bVisible after               | {"bVisible":false}   ← the write landed
| restore bVisible true        | true
| bVisible restored            | {"bVisible":true}    ← restored
| RelativeScale3D baseline     | {"x":0.050000000000000003,"y":0.5,"z":1}
| set (0.05, 0.9, 1.0) Y probe | true
| RelativeScale3D after        | {"x":0.050000000000000003,"y":0.5,"z":1}  ← unchanged
| restore (0.05, 0.5, 1.0)     | true
| RelativeScale3D restored     | {"x":0.050000000000000003,"y":0.5,"z":1}

Conclusion, stated as a finding rather than a theory: on a Blueprint
component instance in this level, ObjectTools.set_properties writes ordinary
properties but silently refuses RelativeScale3D, returning true either way.
ObjectTools.reset_properties writes a partial, wrong value. No log line is
emitted for any of these.

### Every tool that exists for this, and why none of them can do it

ActorTools was enumerated in full. It has set_actor_transform, which takes an
Actor, not a SceneComponent, and there is no set_component_transform
anywhere in the toolset. PrimitiveTools only adds new primitive components.
SceneTools has no component-transform entry point. ObjectTools.set_properties
is the only write path to a component property that this server exposes, and it
is the one demonstrated above not to work for this property.
```

**명령 47 — 저장 경로 두 개가 실패한 전문.**

```
### Second attempt — SceneTools.save_actor, which failed on all 11

Called on each of the 11 actors changed by commands 45–47. All 11 failed, with
this text verbatim:

Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/3/NT/AE23ABHD86QNB96RH83E51
Failed to save 'Wall_Lobby_W_UpperA'.

save_actor resolves the actor's external package path and then refuses because
that package is not in the asset registry. It cannot save an actor whose
external package has not been written yet, which is exactly the case that needs
saving.

### Third attempt — save_assets with an empty list, which worked

AssetTools.save_assets with [] ("Pass an empty list to save all dirty assets"):
{"returnValue":true}
This one really wrote. Verified on disk, not from the return value.
```

명령 `47`의 첫 시도에 대한 설명도 전문으로 옮긴다.

```
Why: this is a World Partition level. Lvl_Stage.umap is only 12,824
bytes and there are 134 actor packages under
Content/__ExternalActors__/ThirdPerson/Lvl_Stage/. The actors are not stored in
the .umap at all — each lives in its own package. The level package genuinely
was not dirty, so is_dirty: false was truthful about the level package and
completely uninformative about the actors.
```

**명령 51 — PIE 때문에 실행을 거부한 전문.**

```
Stopping — Play-In-Editor is running. The refPath came back as /Game/ThirdPerson/
UEDPIE_0_Lvl_Stage..., and the actor count is 138 rather than the 121 this level has.
The tools are resolving against the PIE world, not the editor world.

Confirmed — IsPIERunning returns true. This blocks the task, and I've made no changes.

Why it blocks: with PIE running, every scene tool resolves against the PIE world, not
the editor world. The KeyLight_FinalDoor I found lives at /Game/ThirdPerson/
UEDPIE_0_Lvl_Stage... — a temporary copy. Deleting it would vanish when you stop PIE,
the real editor actor would survive untouched, and I'd have reported a success that
isn't real. The actor count confirms it: 138 in the PIE world versus the level's actual
121. There is no world-selection parameter on find_actors, so I cannot reach the editor
world while PIE is up.

I can stop PIE and proceed, but that ends your play session — and you may be in it right
now judging the very lighting this command is about.
```

**명령 52 — 정적 스위치 문제. 전문.**

```
One thing needs your attention before this looks right: the TopSurfaceColor
static switch is false on the new instance, so the three "upward faces"
colours are stored but will not render.

### Static switches — inherited, and one of them matters

| Switch | Value |
| TopSurfaceColor | false |
| ObjectAligned   | false |
| Grid            | true  |

## The problem: the "upward faces" colours will not render

The instruction's stated reason for using this parent was that it exposes
"separate colours for upward-facing surfaces". It does — but that feature is
gated behind a static switch that is currently off on the new instance.

M_PrototypeGrid exposes TopSurfaceColor twice: once as a Vector (the
colour) and once as a StaticSwitch (the on/off for the whole top-surface
branch). The three Top* colours were written correctly, but the switch reads
false, inherited from the parent material's default.

Evidence that the switch is what gates the feature — a read-only comparison
across every MI_PrototypeGrid_* instance in the project:

| Instance                  | TopSurfaceColor switch | Vector TopSurfaceColor | Vector SurfaceColor |
| MI_PrototypeGrid_Gray     | false | 0.048, 0.048, 0.048 | 0.18, 0.18, 0.18 |
| MI_PrototypeGrid_Gray_02  | false | 0.048, 0.048, 0.048 | 0.18, 0.18, 0.18 |
| MI_PrototypeGrid_TopDark  | true  | 0.06, 0.06, 0.06    | 0.18, 0.18, 0.18 |
| MI_Castle_Stone (new)     | false | 0.115, 0.11, 0.102  | 0.135, 0.125, 0.112 |

MI_PrototypeGrid_TopDark — the one stock instance whose name says it has a
dark top — is the only one with that switch enabled, and it is otherwise
identical to Gray apart from the top colour. That is as direct a demonstration as
the project offers: the switch turns the top-colour branch on.

Consequence: as saved, floors, stair treads and the lobby ceiling underside
will render with the side-face colours (SurfaceColor 0.135/0.125/0.112 and
its grid colours), not the slightly darker top set. The material will still look
like stone and the Grid Size 200 change still applies everywhere — but the
floor/wall distinction the instruction was after is not there.

I did not fix this. Two reasons: the instruction listed exactly 8 parameters
and said every one is an override on the instance, and changing a static switch is
a different kind of edit that triggers a shader recompile — the toolset
documentation says so explicitly. Flipping it was not authorised.

The fix, if you want it, is one call:
MaterialInstanceTools.set_static_switch_parameter on MI_Castle_Stone, name
TopSurfaceColor, value true.
```

**명령 55 — 렌더러 경고. 전문.**

```
The engine emitted a new rendering warning during this command — a virtual
shadow map light overflow. It is the first of its kind in the session and it is a
direct consequence of 18 shadow-casting torches.

### The one that matters — virtual shadow map light overflow

[2026.09.03-12.33.48:332][286]LogRenderer: Warning: [VSM] One Pass Projection max lights overflow. If you see shadow artifacts, decrease the amount of local lights per pixel, or increase r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel.

This is the first LogRenderer warning of any kind in the entire session. The
full LogRenderer history is otherwise nine benign Display lines about ray
tracing PSOs and SBT recreation, dating back to editor startup. Nothing like this
appeared during commands 49, 50 or 51, when the same 18 lights existed as bare
PointLights.

It fired at 12:33:48, four seconds after the delete step was dispatched at
12:33:44 — i.e. on the first viewport redraw after the swap completed.

What it means: too many shadow-casting local lights overlap on some pixels for
the virtual shadow map's one-pass projection path to handle. Each torch now
contributes both a shadow-casting point light and three shadow-casting meshes
(Backplate, Bracket, Cup — only Flame has castShadow false), where before there
was a light and nothing else. That is the shadow cost flagged as unverified at the
end of commands 50 and 54, now confirmed by the engine itself rather than by
speculation.

The warning is conditional — "If you see shadow artifacts" — so it is not proof
of a visible defect. But it is a genuine signal that the lighting setup is at or
past a renderer limit, and it appeared only once, so it has not been characterised
under camera movement.

The two remedies the engine names are raising
r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel or reducing overlapping
local lights. Neither was applied — no console variable was changed and no
light was altered, because neither was part of this instruction.
```

**명령 48·54의 `LogScript` 경고 (반복되는 무해한 패턴).**

```
[2026.09.03-10.06.39:457][703]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Door.BP_Door_C:DefaultSceneRoot_GEN_VARIABLE' (SceneComponent): the following properties could not be read: StaticMesh
[2026.09.03-10.06.39:795][704]LogScript: Warning: GetObjectProperties on '/Game/Interaction/BP_Door.BP_Door_C:Hinge_GEN_VARIABLE' (SceneComponent): the following properties could not be read: StaticMesh
[2026.09.03-10.31.28:203][324]LogCrowdFollowing: Warning: Unable to find RecastNavMesh instance while trying to create UCrowdManager instance
[2026.09.03-10.22.28:496][ 10]LogSlate: Warning: Could not find Glyph Index 0 with codepoint U+d130, getting last resort font data C:\WINDOWS/Fonts/CascadiaMono.ttf
```

### 요약 — 한글

식별자는 영어 그대로 둔다.

**레벨 지오메트리** — `Wall_Lobby_W_Upper` · `Wall_Lobby_E_Upper` · `Wall_Lobby_N_Upper` 셋이 `_UpperA`로 이름이 바뀌고 스케일이 줄었으며, `_UpperB` 셋이 새로 생겼다. `Wall_2F_N_Lintel`이 `Z 800..1200`에서 `1000..1200`으로 줄었다. `Ceiling_Lobby`가 새로 생겼다. 액터 `98` → `101` → `102`.

**문** — `Door_R1` · `Door_R2` · `Door_R3`가 `Z 100` → `200`, `Door_Final`이 `Z 700` → `800`. 넷 다 액터 스케일이 `(1, 2, 1)` → `(1, 2, 2)`. `BP_Door`의 `DoorMesh.RelativeScale3D`는 `(0.05, 0.5, 1.0)` → `(0.05, 0.5, 2.0)` → `(0.05, 0.5, 1.0)`으로 왕복해 **원래 값으로 돌아왔다.**

**조명** — `PointLight` 액터 `13`개 생성(`Torch_1F_S_1..4` · `Torch_1F_N_1..4` · `Torch_2F_W_1..2` · `Torch_2F_E_1..2` · `KeyLight_FinalDoor`), 이어서 `6`개 추가(`Torch_1F_W_1..2` · `Torch_1F_E_1..2` · `Torch_2F_N_1..2`), 이어서 `KeyLight_FinalDoor` 삭제. `18`개가 남았고 값이 한 종류였다. 마지막에 `18`개 전부 삭제되고 `BP_Torch` 인스턴스 `18`개로 대체됐다.

**재질** — `MI_Castle_Stone`(부모 `M_PrototypeGrid`) 신규, 파라미터 여덟 개. `MI_Castle_Wood`(부모 `M_FlatCol`) 신규, 파라미터 둘. `M_Flame` 신규, `FlameColor`·`FlameBrightness` 노출. `SM_Cube` · `SM_Cylinder` · `SM_Ramp`의 `lambert1` 슬롯이 `MI_PrototypeGrid_Gray` → `MI_Castle_Stone`. `SM_Door`의 `Material_0` 슬롯이 `M_FlatCol` → `MI_Castle_Wood`.

**블루프린트** — `BP_Torch` 신규. 컴포넌트 다섯(`Backplate` · `Bracket` · `Cup` · `Flame` · `Light`) + `DefaultSceneRoot`. 변수 `0`개, 그래프 로직 없음, `bCanEverTick` `false`.

**어긋난 것** — `ObjectTools.set_properties`가 `RelativeScale3D`에 `true`를 반환하고 안 썼다. `ObjectTools.reset_properties`가 `x`만 바꿨다. `SceneTools.save_actor`가 `Asset does not exist`로 `11`개 전부 실패했다. PIE가 켜져 있을 때 도구가 `UEDPIE_0_` 사본을 잡았다. `MI_Castle_Stone`의 `TopSurfaceColor` 정적 스위치가 `false`라 윗면 색이 안 나온다. `LogRenderer`가 VSM 광원 오버플로 경고를 처음 뱉었다.

## 분석

### 무엇을 만들었나

**문간 넷 (`400`으로 확대)**

기존 문간은 폭 `200` · 높이 `200`이고 상단 벽(`Z 200..400`)이 인방을 겸했다. 그 상단 벽이 벽 하나로 끊기지 않고 지나가고 있어서, 하단 벽의 틈만 `200` 높이로 뚫려 있었다.

| 원본 액터 | 이전 | 이후 (A) | 새로 만든 것 (B) |
|---|---|---|---|
| `Wall_Lobby_W_Upper` | `(-1300, -1600, 200)` 스케일 `(26, 2, 2)` | `Wall_Lobby_W_UpperA` 스케일 `(9, 2, 2)` → `X -1300..-400` | `Wall_Lobby_W_UpperB` `(-200, -1600, 200)` `(15, 2, 2)` → `X -200..1300` |
| `Wall_Lobby_E_Upper` | `(-1300, 1400, 200)` `(26, 2, 2)` | `Wall_Lobby_E_UpperA` `(9, 2, 2)` | `Wall_Lobby_E_UpperB` `(-200, 1400, 200)` `(15, 2, 2)` |
| `Wall_Lobby_N_Upper` | `(1100, -1600, 200)` `(2, 32, 2)` | `Wall_Lobby_N_UpperA` `(2, 15, 2)` → `Y -1600..-100` | `Wall_Lobby_N_UpperB` `(1100, 100, 200)` `(2, 15, 2)` → `Y 100..1600` |
| `Wall_2F_N_Lintel` | `(1100, -100, 800)` `(2, 2, 4)` → `Z 800..1200` | `(1100, -100, 1000)` `(2, 2, 2)` → `Z 1000..1200` | — |

**새 인방을 하나도 안 만들었다.** 세 문간 위에 이미 벽이 있었다 — `Wall_2F_W`(`Z 400..1200`) · `Wall_2F_E`(`Z 400..1200`) · `Wall_2F_N_Sill`(`Z 400..600`). 상단 벽을 끊자 그 밑면(`Z 400`)이 그대로 인방이 됐다.

끊는 좌표는 하단 벽의 기존 경계값을 그대로 썼다 — 서·동은 `X -400..-200`, 북은 `Y -100..100`. **새로 만든 숫자가 하나도 없다.**

**문짝 넷**

| 액터 | 위치 | 회전 | 액터 스케일 |
|---|---|---|---|
| `Door_R1` | `(-400, -1500, 200)` | yaw `-90` | `(1, 2, 2)` |
| `Door_R2` | `(1200, -100, 200)` | yaw `0` | `(1, 2, 2)` |
| `Door_R3` | `(-400, 1500, 200)` | yaw `-90` | `(1, 2, 2)` |
| `Door_Final` | `(1200, -100, 800)` | yaw `0` | `(1, 2, 2)` |

`DoorMesh` 컴포넌트는 넷 다 `RelativeLocation (0, 50, 0)` · `RelativeScale3D (0.05, 0.5, 1.0)`으로 **안 건드려졌다.**

문짝 크기 계산: `SM_Door`가 `200³`에 피벗 중앙이므로 `200 × 0.05 × 1 = 10`(두께) × `200 × 0.5 × 2 = 200`(폭) × `200 × 1 × 2 = 400`(높이). 광원이 아니라 액터 스케일의 `z`가 높이를 두 배로 만들었다.

**`Ceiling_Lobby`** — `SM_Cube`, `(-1300, -1600, 1200)` 스케일 `(26, 32, 0.5)`. 월드 `X -1300..1300` / `Y -1600..1600` / `Z 1200..1250`. 재질 오버라이드 없음.

사양 초안은 실내만(`X -1100..1100` / `Y -1400..1400`) 덮으려 했는데 **벽까지 덮도록 넓혔다.** 실내만 덮으면 벽 안쪽 면과 만나는 자리에 이음매가 생기고 벽 꼭대기가 안 덮인다. 최종 문 복도(`Wall_Cor_W/E`, `X 1300`부터)와 정확히 맞닿고 겹치지 않는다.

**조명 `18`개 → `BP_Torch` `18`개**

| 라벨 | 위치 | yaw | 붙은 벽 |
|---|---|---|---|
| `Torch_1F_S_1..4` | `(-1050, -1200 / -400 / 400 / 1200, 250)` | `0` | 남쪽 `X -1100` |
| `Torch_1F_N_1..4` | `(1050, -1200 / -400 / 400 / 1200, 250)` | `180` | 북쪽 `X 1100` |
| `Torch_1F_W_1..2` | `(-700 / 100, -1350, 250)` | `90` | 서쪽 `Y -1400` |
| `Torch_1F_E_1..2` | `(-700 / 100, 1350, 250)` | `-90` | 동쪽 `Y 1400` |
| `Torch_2F_W_1..2` | `(-700 / 300, -1350, 850)` | `90` | 서쪽 |
| `Torch_2F_E_1..2` | `(-700 / 300, 1350, 850)` | `-90` | 동쪽 |
| `Torch_2F_N_1..2` | `(1050, -400 / 400, 850)` | `180` | 북쪽 |

`Light` 컴포넌트 값 — `Movable` · `Intensity 5000` · `Unitless` · `AttenuationRadius 1200` · `SourceRadius 10` · `CastShadows true` · `LightColor (1, 0.6667, 0.3529)`.

`Intensity 5000`은 **엔진 기본값 그대로**다. `Engine/Source/Runtime/Engine/Private/Components/LocalLightComponent.cpp:13-16`에서 `Intensity = 5000` · `IntensityUnits = Unitless` · `AttenuationRadius = 1000`을 확인했다. 반경만 `1000` → `1200`으로 키웠다 — 벽 사이가 `2200`이라 양쪽에서 `1200`씩이면 가운데가 덮인다.

`(255, 170, 90)`은 원본 로비 스크린샷의 따뜻한 키 라이트를 보고 내가 고른 값이다.

**`BP_Torch` 컴포넌트**

| 이름 | 메시 | 상대 위치 | 상대 회전 | 상대 스케일 | 재질 |
|---|---|---|---|---|---|
| `Backplate` | `/Engine/BasicShapes/Cube` | `(-46, 0, -24)` | `0` | `(0.12, 0.16, 0.34)` | `MI_Castle_Stone` |
| `Bracket` | `/Engine/BasicShapes/Cylinder` | `(-24, 0, -22)` | pitch `55` | `(0.1, 0.1, 0.55)` | `MI_Castle_Stone` |
| `Cup` | `/Engine/BasicShapes/Cone` | `(0, 0, -24)` | roll `180` | `(0.26, 0.26, 0.2)` | `MI_Castle_Stone` |
| `Flame` | `/Engine/BasicShapes/Cone` | `(0, 0, -14)` | `0` | `(0.18, 0.18, 0.3)` | `M_Flame`, `CastShadow false` |
| `Light` | — | `(0, 0, 0)` | `0` | `1` | — |

**프리미티브 셋 다 `100³` 중심 피벗**(`-50..50`)이다. `SM_Cube`(`0..100`, 최소 모서리)와 규약이 다르다.

계산한 로컬 범위 — `Backplate` `X -52..-40` · `Z -41..-7`, `Cup` `X -13..13` · `Z -34..-14`, `Flame` `Z -29..+1`, 전체 `X -52..+13` · `Y -8..8` · `Z -41..+1`. 벽면이 로컬 `X -50`이므로 `Backplate`가 벽에 `2` 박힌다.

**재질 셋**

| 애셋 | 부모 | 파라미터 |
|---|---|---|
| `MI_Castle_Stone` | `M_PrototypeGrid` | `Grid Size 200` · `Roughness 1.0` · `SurfaceColor (0.135, 0.125, 0.112)` · `GridColor (0.045, 0.042, 0.038)` · `SubGridColor (0.090, 0.085, 0.078)` · `TopSurfaceColor (0.115, 0.110, 0.102)` · `TopGridColor (0.040, 0.038, 0.035)` · `TopSubGridGridColor (0.080, 0.076, 0.070)` |
| `MI_Castle_Wood` | `M_FlatCol` | `Base Color (0.055, 0.032, 0.018)` · `Roughness 0.75` |
| `M_Flame` | — (신규 머티리얼) | `FlameColor (1.0, 0.45, 0.12)` · `FlameBrightness 30` → Emissive |

**재질 범위가 로비를 벗어난 이유.** 액터별 오버라이드로 로비만 자르려 했는데 **로비와 방이 액터를 공유한다.** `Floor_Main` 하나가 `X -1300..700` / `Y -3600..3800`으로 방1 + 로비 + 방3의 바닥을 전부 맡고, `Wall_S_Lower`/`_Upper` 하나가 `Y -3600..3800`으로 남쪽 벽 전체를 맡는다. 액터를 쪼개지 않는 한 로비만 다른 재질을 줄 수 없어서 메시 애셋의 슬롯을 바꿨다.

### 기술적으로 맞게 짚은 부분

**문간 높이로 `400`을 고른 것.** 임의의 값이 아니라 **기존 지오메트리가 공짜로 만들어주는 유일한 값**이다. 1층 벽 전체가 `Z 0..400`이고 그 위에 2층 벽이 `Z 400`부터 얹혀 있으므로, 상단 벽만 끊으면 2층 벽 밑면이 인방이 된다. `600`이었으면 2층 바닥 슬래브(`Z 550..600`)를 뚫어야 하고, `300`이었으면 상단 벽을 세로로 쪼개야 해서 벽 액터가 두 배로 늘었을 것이다. **비용이 `0`인 값이 하나뿐이었고 그게 `400`이었다.**

**액터 스케일로 문짝 높이를 우회한 것.** 컴포넌트 스케일 쓰기가 막혔을 때 흔한 대응은 인스턴스를 지웠다 다시 만들거나 레벨을 리로드하는 것인데, 둘 다 손실이 있다 — 문 넷은 `bLocked` · `RequiredKey` · 태그 같은 인스턴스 상태를 들고 있고 `BP_StageRoom` 셋이 `MyDoor`로 참조한다. **최종 크기가 `메시 × 컴포넌트 스케일 × 액터 스케일`이라는 사실을 이용하면 막힌 항을 건드리지 않고 같은 곱을 만들 수 있다.** 회전축이 `Z`라 `z` 스케일이 여닫이 궤적을 안 건드리고, `DoorMesh`의 상대 위치 `(0, 50, 0)`은 `z` 성분이 `0`이라 안 움직인다.

**CDO를 되돌린 것.** 명령 `47`이 `BP_Door` CDO를 `(0.05, 0.5, 1.0)`으로 되돌렸다. 안 되돌리면 인스턴스 override가 나중에 어떤 이유로든 풀렸을 때 `2 × 2 = 4`배가 된다. **되돌려두면 override가 풀리든 말든 결과가 `400`으로 같다.** 값이 두 곳에서 곱해질 수 있을 때는 한쪽을 중립으로 만들어두는 것이 정석이다.

**천장으로 조명 범위를 자른 것.** 레벨의 조명 액터가 전부 전역이라 `DirectionalLight`를 내리면 방 셋이 같이 죽는다. **빛을 줄이는 대신 빛이 들어오는 구멍을 막는 것**이 범위를 공간으로 자르는 방법이었고, 액터 하나로 끝났다. 사양이 "로비만"으로 자른 이유가 조명이었는데, 그 제약을 조명 설정이 아니라 지오메트리로 만족시켰다.

**만들고 나서 지운 순서.** 명령 `55`가 `BP_Torch` `18`개를 먼저 만들고 검증한 뒤에 `PointLight` `18`개를 지웠다. 반대로 했으면 중간에 멈췄을 때 로비가 캄캄한 채로 남는다. **중간 상태가 "두 배로 밝음"이면 회복이 필요 없고, "완전 어둠"이면 회복이 필요하다.** 라벨이 잠시 겹치는 것은 삭제 대상을 클래스(`PointLight`)로 지정해 해결했다.

**빛을 `BP_Torch` 안에 넣은 것.** 메시만 겹쳐 놓는 안보다 액터가 `18`개 적고, 무엇보다 **밝기 조정이 액터 `18`개가 아니라 BP 기본값 한 곳**이 된다. 조명 세기는 이 작업에서 확실히 더 만질 값이라 지금 정당화된다 — 가상의 미래를 위한 구조가 아니다.

**새 머티리얼을 안 짠 것.** `M_PrototypeGrid`가 이미 `Grid Size` · `Roughness` · `SurfaceColor` · `GridColor` · `SubGridColor`에 더해 윗면 전용 세 개까지 열고 있었다. 사다리 2단(이 프로젝트에 이미 있는가)에서 멈춰 `MaterialInstance` 하나로 끝냈다. **노드를 하나도 안 짜고 벽·바닥·기둥·천장·계단이 전부 바뀌었다.**

**`Grid Size`를 `200`으로 한 것.** 임의의 값이 아니라 **이 레벨의 모듈 치수**다. 원본 도면의 바닥 타일이 `2m`이고 지금 레벨의 모든 치수가 `200`의 배수다. 블록 하나가 타일 하나와 같아진다.

**손대지 않은 것이 옳았던 것 둘.** 첫째, 터미널이 `MI_Castle_Stone`의 `TopSurfaceColor` 정적 스위치를 **안 켰다.** 명령이 파라미터 여덟 개를 열거하며 "every one is an override"라고 했고, 정적 스위치는 셰이더 재컴파일을 부르는 다른 종류의 편집이다. 시키지 않은 것을 하는 대신 보고했다. 둘째, 명령 `51`에서 PIE가 켜져 있자 **아무것도 안 하고 멈췄다.** 그대로 지웠으면 `UEDPIE_0_` 사본만 지워지고 PIE를 끄는 순간 원본이 돌아오는데 보고서에는 "삭제 성공"이 남았을 것이다.

### 확인한 것 / 확인 못 한 것

**확인한 것** — 전부 에디터에서 MCP로 직접 읽은 것이다. MCP 응답이 아니라 되읽은 값이다.

- **문간 넷이 실제로 뚫렸다.** 명령 `45` 뒤 트레이스로 확인했다. 방1·방2·방3 문간에서 `Z 250`·`Z 350`이 `null`(관통), `Z 450`이 `100`(인방에서 막힘). 벽 한복판 대조군은 `Z 350`에서 `100`으로 막혀서, `null`이 "트레이스가 안 돈 것"이 아니라 진짜 구멍임이 갈렸다. 최종 문간도 `Z 900`·`Z 950`이 `null`, `Z 1050`이 `100`
- **문짝 넷이 문간을 빈틈없이 채운다.** 명령 `47` 뒤 트레이스 `20`개가 전부 `195`에서 막히고 `null`이 `0`개다. 추가로 쏜 `Z 10`(문 바닥)도 `195`에서 막혀 아래 구멍이 닫혔다
- **벽 액터 `16`개의 월드 바운드가 목표값과 일치**하고 회전이 전부 `(0,0,0)`이며 옛 라벨 셋이 사라졌다
- **천장이 실제로 막는다.** 아래로 쏜 트레이스 `13`개가 전부 `750`(= `Z 1250`)에서 막힌다. 정확한 네 모서리(`±1290`, `±1590`) 포함. 로비 밖 대조군 둘은 안 막힌다
- **천장이 화면에 보인다.** 사용자가 스폰에서 위를 본 스크린샷으로 확인했다. 구멍이나 이음매가 없는 한 면이다
- **조명 `18`개의 위치·설정이 전부 일치**하고, 설정이 **두 종류로만** 갈렸다(토치 `18`개 동일 + 키 라이트 하나). 키 라이트를 지운 뒤에는 한 종류가 됐다
- **`BP_Torch` 인스턴스 `18`개의 위치·yaw·스케일·아웃라이너 폴더가 전부 일치**하고 `PointLight` 클래스 액터가 `0`개 남았다
- **`MI_Castle_Stone`의 파라미터 여덟 개와 `MI_Castle_Wood`의 둘이 지정값과 정확히 일치**하고, `MI_PrototypeGrid_Gray`(되돌릴 때 쓸 원본)와 `MI_DefaultColorway`가 안 건드려졌다
- **`BP_Torch`의 `Light` 컴포넌트 값이 지운 `PointLight` `18`개와 완전히 같다**
- **`DirectionalLight`(`Intensity 3`)와 `SkyLight`(`Intensity 1`)가 안 건드려졌다.** 방 셋이 계속 이 둘로 밝다
- **디스크 저장이 실제로 됐다.** `git status`의 `__ExternalActors__` 경로로 매번 확인했다. 명령 `55`는 `18` 삭제 / `18` 추가로 정확히 맞물렸다
- **`PIE`가 꺼져 있는 상태에서 읽었다.** 명령 `51` 이후 모든 검증 스크립트에 `IsPIERunning`과 `refPath`의 `UEDPIE` 포함 여부를 같이 찍었다
- **사용자가 PIE에서 확인한 것 셋** — 문이 열릴 때 문짝이 이상하지 않다, 닫힌 문이 막는다, 문간이 시원해 보인다

**확인 못 한 것**

- **횃불 `18`개를 화면에서 본 적이 없다.** 명령 `55`가 세션 마지막이었고 그 뒤 스크린샷을 못 받았다. 팔(`Bracket`) 방향이 어떻게 보이는지, 불꽃(`FlameBrightness 30`)이 적당한지, 벽에 박히는 정도가 맞는지 전부 미확인이다. **이 세션에서 만든 것 중 유일하게 눈으로 검증이 안 된 산출물이다**
- **`M_Flame`의 그래프를 안 읽었다.** 터미널이 "unlit emissive material, 2 exposed parameters"라고 보고했고 컴파일이 통과했다는 것만 안다. 노드 구성과 `FlameColor`·`FlameBrightness`가 실제로 Emissive에 연결됐는지 되읽지 않았다
- **`MI_Castle_Stone`의 윗면 색이 안 나온다.** `TopSurfaceColor` 정적 스위치가 `false`다. 바닥·계단 디딤면·천장 밑면이 옆면 색(`SurfaceColor`)으로 렌더된다. **터미널이 보고했고 내가 아직 안 고쳤다**
- **VSM 광원 오버플로 경고가 실제 아티팩트를 만드는지 안 봤다.** 경고 문구 자체가 조건부("If you see shadow artifacts")이고 한 번만 떴다. 카메라를 움직이며 확인한 적이 없다
- **`Bracket`의 `pitch 55`가 화면에서 어떻게 보이는지.** 계산으로는 벽 위쪽에서 그릇 쪽으로 내려오는 팔이 된다. 명령문에는 "up-out"이라고 썼는데 실제는 반대다
- **`Flame` 컴포넌트의 collision 비활성화 여부.** 명령에 넣었지만 되읽지 않았다. `CastShadow false`만 확인했다
- **NavMesh를 안 구웠다.** 문간이 `400`이 되고 천장이 생겼는데 `Build Paths`를 안 돌렸다. 문간이 커진 것은 통행에 유리하기만 하므로 급하지 않지만, 확인은 안 됐다
- **방 셋이 얼마나 어두워졌는지.** 알베도를 `0.18` → `0.135`로 내렸고 방은 하늘빛으로만 밝다. 사용자에게 방 안 스크린샷을 부탁했지만 못 받았다
- **문짝이 목재로 바뀐 뒤의 화면.** `MI_Castle_Wood` 적용 뒤 스크린샷이 없다
- **아이템 픽업이 재질 변경의 영향을 안 받는다는 것은 확인했다.** `/Engine/BasicShapes/Cube`와 `Cylinder`를 쓴다. 다만 **어두운 로비에서 안 보이는 것은 그대로다**

### 남는 리스크

- **`MI_Castle_Stone`의 윗면 색이 죽어 있다.** `TopSurfaceColor` 정적 스위치가 `false`. 바닥과 벽의 색 구분이 없다. 고치는 것은 호출 하나(`set_static_switch_parameter`)지만 **셰이더 재컴파일이 걸린다**
- **VSM 광원 오버플로.** 그림자 던지는 로컬 광원이 픽셀당 한계를 넘었다. 횃불 하나가 광원 하나 + 그림자 던지는 메시 셋(`Backplate` · `Bracket` · `Cup`)을 들고 있다. 대책 둘 — `r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel`을 올리거나, 겹치는 광원을 줄이거나, 메시의 `CastShadow`를 끄거나. **아무것도 안 했다**
- **줄눈이 일직선으로 통한다.** `M_PrototypeGrid`는 격자라 벽돌이 엇갈려 쌓이지 않는다. **지금 남은 유일한 "프로토타입" 신호다.** 고치려면 새 머티리얼을 직접 짜야 한다
- **문짝이 단색이다.** `M_FlatCol`은 단색 머티리얼이라 널결·패널·철띠를 못 그린다. 문짝 메시를 새로 만들 때(사양 `13`번, 경로 C) 들어간다
- **액터 스케일이 비균일하다.** 문 넷이 `(1, 2, 2)`다. 힌지가 `Z`축으로 도는데 부모 스케일의 `X`와 `Y`가 달라서, **문이 열릴 때 문짝 폭이 변한다.** `(1, 2, 1)`이던 때부터 있던 문제이고 이번에 악화되지 않았다. 사용자가 PIE에서 "이상 없다"고 확인했지만 원인 자체는 남아 있다
- **`Bracket`이 아래로 기운다.** 명령문의 의도("up-out")와 반대다. 반대로 돌리면 팔 끝이 그릇 위로 솟아 더 어색해서 그대로 뒀다. 화면을 못 봤다
- **재질이 레벨 전체에 걸렸다.** "로비 먼저"라는 사양 범위를 벗어났다. 액터를 공유해서 어쩔 수 없었지만, **방 셋이 어두워지는 부작용이 확인되지 않았다**
- **아이템이 어두운 로비에서 안 보인다.** `/Engine/BasicShapes/`의 기본 재질을 쓴다. 이미 `접어둔 것`에 있던 항목인데 조명이 어두워지면서 심해졌다
- **`M_Flame`의 그래프를 안 읽었다.** 컴파일 통과와 파라미터 둘 노출만 보고받았다. 실제 연결을 확인 안 했다
- **`BP_Torch`가 `UserConstructionScript`와 `EventGraph`를 갖고 있다.** 둘 다 비어 있지만 존재한다. Actor BP의 기본이라 만든 게 아니다
- **남쪽 벽이 `2800`짜리 민 벽이다.** 토치 넷이 웅덩이만 찍고 사이가 어둡다. 조명 문제가 아니라 채울 물건이 없는 문제다. 도면의 남쪽 장식 아치가 그 자리를 메우는 물건이다

### 총평

**요청은 다 했다.** 문간 확대, 견적, 천장, 조명, 문 양옆 배치, 키 라이트 정리, 석재, 목재, 횃불 — 열한 개 명령이 전부 목표 상태에 도달했고 그중 아홉 개는 한 번에 됐다.

**실질적 난이도는 지오메트리가 아니라 도구였다.** 좌표와 치수는 기존 벽의 경계값에서 거의 다 나왔다 — 문간 `400`은 벽 높이가 정해줬고, 조명 간격 `±400`은 기존 쌍이 정해줬고, `Grid Size 200`은 타일 모듈이 정해줬다. **내가 지어낸 숫자는 재질 색과 횃불 치수뿐이다.**

어려웠던 것은 **플러그인이 조용히 거짓말하는 자리를 찾는 것**이었다. 이 세션에서 그런 자리를 다섯 개 잡았다 — `set_properties`의 `RelativeScale3D` 무시, `reset_properties`의 부분 쓰기, `save_actor`의 저장 불가, PIE 중 `UEDPIE_0_` 세계, 정적 스위치에 가려진 파라미터. **다섯 개 중 셋을 터미널이 잡았고 둘을 내가 잡았다.** 전부 `true`나 성공 응답을 받은 뒤에 되읽어서 드러난 것이다.

견적은 `1`~`3`번을 명령 `3`개로 봤는데 실제로 `7`개를 썼다. 초과분 넷의 출처가 각각 다르다 — CDO 실패(`+1`, 견적에 위험도 `중간`으로 적어둔 자리에서 나왔다), 사용자 요청으로 조명 재배치(`+1`), 내 판단 착오로 키 라이트 제거(`+1`), PIE 차단으로 같은 명령을 두 번(`+0`, 명령은 하나로 셌다).

**가장 크게 바뀐 것은 재질이었다.** 명령 하나, 새 애셋 하나, 노드 `0`개로 벽·바닥·기둥·천장·계단이 전부 바뀌었다. 세션 초반에 "대충의 원인 넷 중 폴리곤 문제는 하나뿐"이라고 진단한 것이 그대로 맞았다.

**미검증이 하나 남았다.** 횃불 `18`개가 화면에 어떻게 보이는지 모른다. 지오메트리와 값은 다 맞는데 형태를 눈으로 본 적이 없고, 그 위에 VSM 경고까지 얹혀 있다. **이 세션의 마지막 산출물이 검증이 가장 얕다.**

## AI의 제안

> `문간 높이를 400으로 한다. 1층 벽 전체 높이가 400이라 새 인방을 만들 필요 없이 위층 벽이 그대로 인방이 된다.`

사용자는 "키워보자"만 말했고 숫자는 AI가 정했다. 얻는 것은 명령 `2`개 · 액터 `+3`개로 끝나는 것이다. 잃는 것은 `400`이 원본의 `360` 근처와 정확히 같지는 않다는 것 — 다만 타일 모듈의 배수라는 이점이 더 크다고 봤다.

> `천장 슬래브를 로비 실내가 아니라 벽까지 덮는다. X -1300..1300 / Y -1600..1600 / Z 1200..1250.`

사양 초안은 실내만 덮으려 했다. 얻는 것은 벽 안쪽 면과의 이음매가 없어지고 벽 꼭대기가 덮이는 것이다. 잃는 것은 밖에서 보면 로비만 뚜껑이 덮인 모양이 되는 것인데, 밖에서 볼 일이 지금 없다.

> `전역 조명은 그대로 두고, 로비에만 천장을 덮어 하늘빛을 차단한다.`

범위를 "로비만"으로 잘라도 조명은 안 잘린다는 것을 발견한 뒤 낸 제안이다. 얻는 것이 셋 — 방 셋이 안 어두워지고, 로비 천장이 어두워져 원본과 같은 그림이 되고, 넘어온 미결 하나(최종 구역이 방2 위에 떠 보이는 것)가 같이 가려진다. 잃는 것은 로비가 완전히 캄캄해져서 조명을 놓기 전까지 아무것도 판단할 수 없다는 것이고, 실제로 그렇게 됐다.

> `Intensity 5000은 엔진 기본값 그대로다. 내가 지어낸 밝기가 아니다.`

값을 고를 때 엔진 소스(`LocalLightComponent.cpp:13-16`)를 먼저 읽고 그 기본값을 출발점으로 삼았다. 얻는 것은 "왜 이 숫자냐"에 답이 있는 것이다. 잃는 것은 그 값이 이 공간에 맞다는 보장이 없다는 것 — 실제로 사진에서 웅덩이가 좁게 찍혔다.

> `KeyLight_FinalDoor를 지운다. 명령 50이 같은 문에 토치 둘을 붙이면서 조명이 셋 겹쳐 날아갔다.`

사용자가 스크린샷에서 "저기 조명 하나 있던데 의도인지"를 물어서 답하다 낸 제안이다. 얻는 것은 문 넷이 전부 "양옆 토치 둘"이라는 하나의 규칙이 되고 조명 값이 한 종류가 되는 것이다. 잃는 것은 원본이 가졌던 "화면을 지배하는 키 라이트 하나"가 없어지는 것이다. 그건 문 조명이 아니라 홀 전체를 잡는 조명이어야 한다고 봤다.

> `새 머티리얼을 안 짜고 M_PrototypeGrid의 MaterialInstance로 간다. 사다리 2단에서 멈춘다.`

얻는 것은 노드를 하나도 안 짜고 레벨 전체가 바뀌는 것이다. 잃는 것은 줄눈이 엇갈리지 않는 것이고, 그게 지금 남은 유일한 프로토타입 신호다.

> `재질은 로비만 자를 수 없다. Floor_Main 하나가 방1+로비+방3의 바닥이고 Wall_S_Lower/Upper 하나가 남쪽 벽 전체다.`

사양 범위를 벗어나는 판단이라 명령을 내기 전에 밝혔다. 얻는 것은 방 셋도 같은 성으로 보이는 것. 잃는 것은 방 셋이 어두워지는 것이고 아직 확인 안 됐다.

> `횃불은 메시로 간다. MCP에 Niagara 툴셋이 없고, 가져다 쓸 불 애셋도 없다.`

사용자가 "메시야 이펙트로해?"라고 물어서 답한 것이다. 얻는 것은 명령문으로 만들 수 있다는 것이다. 잃는 것은 불꽃이 안 움직인다는 것이고, 나중에 발광 머티리얼에 노이즈를 흘려 올릴 길은 열려 있다.

> `빛을 BP_Torch 안에 넣고 18개를 교체한다. 밝기 조정이 액터 18개가 아니라 BP 기본값 한 곳이 된다.`

메시만 겹쳐 놓는 안과 둘 중에 고르라고 제시했고 사용자가 후자를 골랐다. 얻는 것은 조정 지점이 하나가 되는 것. 잃는 것은 검증 끝난 액터 `18`개를 지운다는 것이고, 값이 커밋과 `Terminal-Log`에 남아 있어 회복 가능하다고 봤다.

> `만들고 나서 지운다. 반대로 하면 중간에 멈췄을 때 조명이 사라진 채로 남는다.`

얻는 것은 중간 상태가 "두 배로 밝음"이 되어 회복이 필요 없다는 것. 잃는 것은 라벨이 잠시 겹치는 것이고, 삭제 대상을 클래스로 지정해 해결했다.

> `검증 스크립트마다 IsPIERunning과 refPath의 UEDPIE 포함 여부를 같이 찍는다.`

터미널이 명령 `51`에서 PIE를 잡은 뒤, 내 검증에도 같은 위험이 있다는 것을 인정하며 낸 것이다. 얻는 것은 거의 공짜로 조용한 오류 하나를 막는 것. 잃는 것은 없다.

## 다음으로 넘김

**바로 이어서 할 것**

- **횃불 `18`개를 PIE에서 볼 것.** 이 세션의 마지막 산출물이고 **유일하게 눈으로 검증이 안 됐다.** 볼 것 넷 — `Bracket`이 아래로 기운 게 어떻게 보이는지, `FlameBrightness 30`이 적당한지, 벽에 박히는 정도(`Backplate`가 `2` 박힌다)가 맞는지, 그림자 아티팩트가 실제로 보이는지
- **`MI_Castle_Stone`의 `TopSurfaceColor` 정적 스위치를 켤 것인가.** 지금 `false`라 바닥·계단 디딤면·천장 밑면이 옆면 색으로 렌더된다. `MaterialInstanceTools.set_static_switch_parameter`, 이름 `TopSurfaceColor`, 값 `true` 한 번이면 되지만 **셰이더 재컴파일이 걸린다**
- **다음 Terminal-Log 번호는 `56`이다.** `45`~`55`가 이 세션 것이다

**결정 필요**

- **VSM 광원 오버플로를 어떻게 할 것인가.** 대책 셋 — `r.Shadow.Virtual.OnePassProjection.MaxLightsPerPixel`을 올리거나, `Backplate`·`Bracket`·`Cup`의 `CastShadow`를 끄거나, 토치 수를 줄이거나. **셋째 것이 가장 싸 보인다** — 작은 소품이 그림자를 던질 이유가 별로 없다
- **줄눈을 엇갈리게 할 것인가.** 지금 남은 유일한 "프로토타입" 신호다. `M_PrototypeGrid`를 안 건드리고 새 머티리얼을 짜야 한다 — 월드 좌표에서 켜를 계산해 홀수 켜를 반 칸 밀고 줄눈을 그린다. 노드 `15`개 안팎이고 **경로 C 성격이라 재작업 `1`회를 봐야 한다**
- **방 셋이 얼마나 어두워졌는지 보고 대응할 것인가.** 알베도를 `0.18` → `0.135`로 내렸고 방은 하늘빛으로만 밝다
- **남쪽 벽을 무엇으로 채울 것인가.** `2800`짜리 민 벽이라 토치 사이가 어둡다. 도면의 남쪽 장식 아치가 그 자리다. **이건 조명이 아니라 물건 문제다**
- **문짝 액터 스케일의 비균일을 정리할 것인가.** 문 넷이 `(1, 2, 2)`라 열릴 때 폭이 변한다. 문짝 메시를 새로 만들 때 스케일을 `1`로 정리하는 것이 근본 해결이다
- **아이템을 어떻게 보이게 할 것인가.** `/Engine/BasicShapes/` 기본 재질이라 어두운 로비에서 안 보인다. 발광 재질을 주거나 `iconColor`를 실제로 쓰거나
- **`Content/FirstPerson/`을 어떻게 할 것인가.** 앞 세션에서 넘어온 항목. 안에 `Anims/` 둘만 남았고 그 둘이 `BP_ThirdPersonCharacter`의 살아 있는 의존이다
- **`Docs/Spec`의 `09-01` 이후 끊긴 구간을 소급 회수할 것인가.** 앞 세션에서 넘어온 항목
- **`Content/` 재배치.** 앞 세션에서 "게임이 한 번 완성된 뒤"로 미룬 항목. `BP_ThirdPersonGameMode.NotifyRoomCleared`가 `"/Game/Interaction/BP_Door.BP_Door_C"`를 문자열로 들고 있어 옮기면 조용히 끊긴다
- **램프(계단) 옆면 난간 · 난간 높이 `100` · `Wall_2F_S`의 방1·방3 구간 · 로비 남쪽 장식 문.** 넷 다 사양의 미결이고 앞 세션에서도 넘어온 항목이다
- **계단 폭 `600` 유지 여부와 난간 높이.** 둘 다 **OBJ를 쓰기 전에** 정해야 한다. 경로 C는 값이 메시에 굳는다
- **중복 열쇠 회수 · `Ball_Test` 행 · `FoundSlotIndex` 삭제 · `AM_Player_Attack` 창 시작.** 앞 세션에서 넘어온 항목들

**확인 필요**

- **`M_Flame`의 그래프.** 컴파일 통과와 파라미터 둘 노출만 보고받았고 `FlameColor`·`FlameBrightness`가 실제로 Emissive에 연결됐는지 안 읽었다
- **`Flame` 컴포넌트의 collision.** 명령에 비활성화를 넣었지만 되읽지 않았다. `CastShadow false`만 확인했다
- **`Build` → `Build Paths`로 NavMesh를 굽고 저장.** 사흘째 넘어온 항목이다. 문간이 `400`이 되고 천장이 생겼다. 문간 확대는 통행에 유리하기만 하지만 확인은 안 됐다. `NavBounds_Main`(`Z -200..600`)의 위쪽 경계가 2층 바닥(`Z 600`)에 걸쳐 있어 2층에 NavMesh가 깔리는지도 그때 드러난다
- **`BP_Torch`의 빈 `UserConstructionScript`·`EventGraph`.** Actor BP의 기본인지, 아니면 터미널이 만든 것인지 안 갈렸다
- **회수한 여덟 파일의 본문.** `Docs/Terminal-Log/recovered/`에 있고 앞 세션에서 넘어온 항목이다. **아무도 안 읽었다**
- **`BP_Door`의 `Event Interact` 마지막 `else` 가지.** `read_graph_dsl`이 `_`로만 찍는다. 앞 세션에서 넘어온 항목
- **`read_graph_dsl` 또는 `get_properties`가 패키지를 dirty로 만드는지.** 앞 세션에서 넘어온 항목
- **터미널이 시키지 않은 액터를 만드는 경로.** 앞 세션에서 넘어온 항목이고 이번 세션에는 관찰되지 않았다
- **`2026-09-01-enemy-hp-death.md`의 `확인 필요` 목록.** `arrange_nodes`, `EditorPerProjectUserSettings.ini` 저장 실패, `CaptureViewport`가 에디터 월드를 그리는 것이 그 파일에 그대로 있다

**접어둔 것**

- 앞 세션의 `접어둔 것` 열두 항목이 그대로 유효하다 — 적 사망 연출 분리, 적 상태 표시 다시 심기, `HitActorsThisSwing` 리네임, 플레이어 `BeginPlay` HP 초기화, Mixamo 외부 베기 애니메이션, 진짜 칼 메시, `heldTransform` 회전·오프셋 기록, 적 공격 이펙트·사운드, `MM_Attack_02/03`·`MM_ChargedAttack`, `TriggerBox` + 레벨 블루프린트로 클리어 트리거 만들기
- **기성 애셋(Fab 무료 중세 팩) 도입.** 심문에서 사용자가 경로 `D`를 안 골랐다. 원본 프로젝트가 간 길이지만 이 프로젝트 성격과 어긋난다고 봤다
- **횃불을 Niagara 이펙트로 만들기.** MCP에 Niagara 툴셋이 없고 가져다 쓸 불 애셋도 없다. 발광 머티리얼에 노이즈를 흘려 움직이게 하는 길은 열려 있다
