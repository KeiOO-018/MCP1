# 2026-08-28

## 작업물

UE 5.8 엔진 설치본에서 `Variant_Shooter` 공유 콘텐츠 팩을 파일 복사로 프로젝트에 반입했다. 새 프로젝트 생성도 Migrate도 쓰지 않았다.

**소요 시간**: 약 50분 (세션 시작 ~ 반입 커밋 `6225dd9` 13:32:40). 세션 시작 시각이 따로 기록돼 있지 않아 첫 MCP 호출 무렵으로 잡은 값이다.

## 명령

### 한글

> 작업하기 전 준비

> 1번하자

이 지점에서 선택지 세 개를 제시하고 답을 받았다. 타이핑이 아니라 선택이라 원문이 없으므로 고른 항목을 적는다.

- 최종 목표: `무기 한 자루까지`
- 반입 범위: `팩 전체 (권장)`
- 이번 범위: `반입까지만`

> 진행하자

> Output log 열어둬 달라는게 켰는데 그럼 뭐해이제?

> 첫번째는 바닥에 총모양 아이콘 보여? 저 아이콘이 아이템이거든 아이템을 먹으면 총이 들어지는데 그 받침대야
> 두번째는 탄창표시는 왼쪽아래에 보면 UI그림으로 노란색캡슐여러개가 있고 비어있는것도 있잔아 그게 총알이야 쏠때마다 줄어드는걸 표현한

> 이상없음

> 1번으로

### English — MCP에 실제로 보낸 명령

**없다.** 이 작업에서 사용자가 UE Terminal에 붙여 넣은 영어 명령은 하나도 없다. 반입은 파일 복사로 했고, 검증은 내가 `unreal-mcp`의 조회 도구를 직접 호출해서 했다. 자연어 명령이 아니라 도구 호출이므로 여기 적을 원문이 없다.

파일 복사에 쓴 셸 명령은 아래와 같다. 영어 명령은 아니지만 이 작업의 실제 실행 내용이므로 남긴다.

```
cp -r "$SRC/Content/." "$DST/Variant_Shooter/"
cp -r "$SRC/__ExternalActors__/Lvl_ArenaShooter" "$DST/__ExternalActors__/Variant_Shooter/"
cp -r "$SRC/__ExternalObjects__/Lvl_ArenaShooter" "$DST/__ExternalObjects__/Variant_Shooter/"
```

`$SRC`는 `C:\Program Files\Epic Games\UE_5.8\Templates\TemplateResources\Standard\Variant_Shooter`, `$DST`는 `d:/20260827/MCP1/Content`다.

**옮기며 들어간 해석** — 한글 지시에 없던 것을 내가 정한 것들이다.

- 반입 방법을 파일 복사로 정한 것. 사용자는 "1번하자"로 항목만 골랐고 방법은 말하지 않았다. Migrate 경로는 이미 프로젝트에 있는 애셋 19개와 충돌 처리를 해야 해서 더 비싸다고 판단했다.
- 목적지 배치. `Content/Variant_Shooter/`, `Content/__ExternalActors__/Variant_Shooter/`, `Content/__ExternalObjects__/Variant_Shooter/`. 다만 이건 내가 발명한 게 아니라 팩의 `FeaturePack/manifest.json`이 `DestinationFilesFolder: "Variant_Shooter"`로 지정한 값을 따른 것이다.
- `.ini` 파일도 함께 복사한 것. `Lvl_ArenaShooter.ini`는 애셋이 아니지만, 지난 세션에 들어온 `Content/FirstPerson/Lvl_FirstPerson.ini`가 프로젝트에 있는 것을 확인하고 같게 맞췄다.
- 합격 기준 1의 뒷부분 "손이 화면 중앙에 보인다". 사용자는 이런 말을 한 적이 없다. 지난 세션 기록의 기대를 내가 그대로 기준으로 옮겼고, 그게 틀린 기준이었다.

## Terminal 결과

### 원문 — English

이 작업에는 Terminal 에이전트가 없었다. 아래는 내가 `unreal-mcp`를 직접 호출해 받은 응답과 셸 출력이다. 성공 보고는 판단 근거가 된 줄만 발췌했고, 실패·경고·어긋난 응답은 전문을 붙였다.

`describe_toolset`이 알려준 툴 이름을 `call_tool`에 그대로 넣었을 때. 전문.

> Unknown tool EditorToolset.LogsToolset.GetLogEntries

접두사를 뗀 `GetLogEntries`로는 통했다. **지난 세션 기록에 원인 미상으로 남아 있던 `Unknown tool editor_toolset.toolsets.asset.AssetTools.find_assets`와 같은 원인이다.**

`IMC_Default`의 매핑을 읽으려 했을 때. 전문.

> {"Mappings":[]}

빈 배열이라 처음에는 어긋남으로 판단했으나 **그 판단이 틀렸다.** UE 5.8에서 이 필드는 deprecated다. 엔진 소스 `Engine/Plugins/EnhancedInput/Source/EnhancedInput/Public/InputMappingContext.h`:

> UE_DEPRECATED(5.7, "Use the DefaultKeyMappings struct instead.")
> UPROPERTY(config, BlueprintReadOnly, Category = "Mappings", meta = (DeprecatedProperty="Note", DeprecationMessage = "Use the DefaultKeyMappings struct instead."))
> TArray<FEnhancedActionKeyMapping> Mappings;

`DefaultKeyMappings`로 읽으니 매핑 13개가 전부 나왔다.

`Add Feature or Content Pack` UI에 이 팩이 안 뜨는 이유. 엔진 소스 `Engine/Source/Editor/AddContentDialog/Private/ViewModels/AddContentWidgetViewModel.cpp:130-133`. 발췌.

> // List of categories we don't want to see
> TArray<EContentSourceCategory> FilteredCategories;
> FilteredCategories.Add(EContentSourceCategory::SharedPack);
> FilteredCategories.Add(EContentSourceCategory::Unknown);

팩의 `manifest.json`이 `"Category": "SharedPack"`이므로 목록에서 걸러진다.

바이트 단위 대조 결과. 발췌.

> Content: identical
> ExternalActors: identical
> ExternalObjects: identical

`ABP_FP_Weapon`의 의존성. 발췌.

> /Game/Characters/Mannequins/Meshes/SK_Mannequin
> /Game/FirstPerson/Blueprints/BP_FirstPersonCharacter
> /Game/Variant_Shooter/Anims/Ctrl_HandAdjusment
> /Game/Variant_Shooter/Blueprints/BP_ShooterCharacter

`BP_ShooterCharacter`의 부모 클래스. 전문.

> {"returnValue":{"refPath":"/Game/FirstPerson/Blueprints/BP_FirstPersonCharacter.BP_FirstPersonCharacter_C"}}

PIE 로그. 발췌.

> LogLoad: Game class is 'BP_ThirdPersonGameMode_C'

`Variant_Shooter` 문자열로 로그를 검색한 결과. 전문.

> {"returnValue":[]}

### 요약 — 한글

엔진 설치본의 `Variant_Shooter` 폴더 세 개를 프로젝트로 복사했다.

| 대상 | 변화 |
|---|---|
| `Content/Variant_Shooter/` | 신규 51파일 — 애셋 50개 + `Lvl_ArenaShooter.ini` |
| `Content/__ExternalActors__/Variant_Shooter/Lvl_ArenaShooter/` | 신규 132파일 |
| `Content/__ExternalObjects__/Variant_Shooter/Lvl_ArenaShooter/` | 신규 9파일 |
| 애셋 총계 | 339 → 530 (+191) |
| 덮어쓴 기존 애셋 | **0개** |

`diff -r`로 세 폴더 모두 엔진 원본과 바이트 단위 동일함을 확인했다.

커밋 1개: `6225dd9`.

## 분석

### 무엇을 만들었나

**반입한 애셋 — `/Game/Variant_Shooter/` 50개**

- `Anims/` 7개 — `ABP_FP_Weapon`, `ABP_FP_Pistol`, `ABP_TP_Pistol`, `ABP_TP_Rifle`, `Ctrl_HandAdjusment`, `Ctrl_HandAdjusment_Pistol`, `FP_Rifle_Shoot_Montage`
- `Blueprints/` 21개 — `BP_ShooterCharacter`, `BP_ShooterGameMode`, `BP_ShooterPlayerController`, 인터페이스 `BPI_Shooter`·`BPI_Teammate`, AI 9개(`BP_ShooterNPC`, `BP_ShooterAIController`, StateTree 태스크 6개, EQS 3개), 픽업·무기·발사체 8개
- `Input/` 5개 — `IA_Shoot`, `IA_SwapWeapon`, `IMC_Weapons`, `BPI_Touch_Shooter`, `UI_TouchInterface_Shooter`
- `UI/` 3개 — `UI_Shooter`, `UI_ShooterBulletCounter`, `M_BulletCounter`
- `Lvl_ArenaShooter.umap` + `.ini`, 외부 액터 132개 / 외부 오브젝트 9개

**아무것도 연결하지 않았다.** `BP_ThirdPersonCharacter`, `IMC_Default`, `Lvl_ThirdPerson` 전부 그대로다. 반입된 입력 액션 `IA_Shoot`·`IA_SwapWeapon`과 `IMC_Weapons`도 어디에도 등록되지 않았다.

**외부 참조 20개 중 19개가 이미 프로젝트에 있었다.** `Characters/Mannequins/`의 애님과 메시, `FirstPerson/`의 BP 두 개와 머티리얼 인스턴스, `Input/Touch/`의 인터페이스와 위젯, `LevelPrototyping/`의 메시 두 개, `Weapons/`의 스켈레탈 메시 네 개. 나머지 하나 `/Game/Variants/Shooter/Blueprints/Pickups/Pistol/Mesh/SK_Pistol`은 `SM_FoamBullet.uasset` 안의 구 경로 잔재이고 **Epic 원본에도 대상이 없다.**

### 기술적으로 맞게 짚은 부분

**지난 기록의 전제를 검증하고 뒤집은 것.** 넘김 항목에는 "빈 ArenaShooter 프로젝트를 만들어 Migrate하는 경로가 유력하나 확인 안 했다"고 적혀 있었다. 실제로 엔진 설치본을 뒤져보니 `Templates/TemplateResources/Standard/Variant_Shooter/`에 팩이 **이미 풀린 채로** 있었다. 새 프로젝트를 만들 이유가 없었다. **적혀 있는 계획을 그대로 실행하지 않고 먼저 확인한 것이 프로젝트 생성 한 번을 통째로 아꼈다.**

**UI에 안 뜨는 이유를 엔진 소스로 확정한 것.** 지난 세션에 사용자가 `Add Feature or Content Pack` 메뉴에서 팩을 못 찾은 일이 있었고, 그때는 원인을 못 짚었다. 이번에는 `AddContentDialog` 모듈을 읽어 `SharedPack` 카테고리가 목록 생성 시점에 명시적으로 필터링된다는 것을 확인했다. **"메뉴에 없더라"가 아니라 "코드가 거른다"까지 간 것이 다음에 같은 함정에 빠지지 않게 한다.**

**덮어쓰기 예상을 파일 단위로 미리 확정한 것.** 복사 대상이 전부 `Variant_Shooter/` 하위이고 프로젝트에 그 경로가 셋 다 없다는 것을 먼저 확인했다. 그래서 "덮어쓴 애셋 0개"를 추측이 아니라 사실로 말할 수 있었다.

**`.uasset`을 `grep -a`로 읽어 참조를 뽑은 것.** 애셋을 열지 않고도 팩이 프로젝트 밖으로 무엇을 참조하는지 전수 조사할 수 있었다. 읽기 전용이고 대상이 엔진 설치본이라 프로젝트 애셋을 위협하지 않는다. `.uasset`을 텍스트로 편집하지 않는다는 규칙의 의도를 벗어나지 않으면서 필요한 정보를 얻었다.

**손이 안 보이는 것이 우리 결함이 아님을 상속 관계로 증명한 것.** `BP_ShooterCharacter`의 부모가 `BP_FirstPersonCharacter_C`라는 사실 하나로, Epic의 아레나 슈터도 카메라가 `head` 본에 붙는다는 것이 확정됐다. 우리 포팅을 의심하며 실험할 필요가 없었다.

### 확인한 것 / 확인 못 한 것

**확인한 것** — 파일 51 + 132 + 9개가 엔진 원본과 바이트 단위 동일하다(`diff -r`). 애셋 50개 전부 Asset Registry에 인식된다(`find_assets`가 정확히 50개 반환). 로그에 `Variant_Shooter` 문자열이 한 줄도 없다 — 로드 실패·미해결 참조 에러 0. `ABP_FP_Weapon`을 로드했고 의존성에 `Ctrl_HandAdjusment`가 실제로 들어 있다. `BP_ShooterCharacter`도 로드 성공. PIE에서 `Lvl_ArenaShooter`를 플레이해 무기 장착·조준·발사가 되는 것을 사용자가 화면으로 확인했다. `Lvl_ThirdPerson`에서 V 토글·이동·점프에 회귀가 없는 것도 사용자가 확인했다.

**확인 못 한 것** — `ABP_FP_Weapon`의 컴파일 상태 플래그를 직접 읽지 않았다. `compile_blueprint`를 부르면 애셋을 dirty로 만들 수 있어 호출하지 않았고, 로드가 되고 에러가 안 찍혔다는 정황만 있다. 팩 애셋 50개 중 **실제로 로드해본 것은 2개뿐**이다. `Lvl_ArenaShooter` 플레이가 상당수를 간접적으로 돌렸지만 전수는 아니다. `SM_FoamBullet` 안의 깨진 참조가 런타임에 무해한지는 수류탄 발사기를 쏴봐야 아는데 안 해봤다. `Lvl_ArenaShooter`가 실제로 어떤 GameMode를 쓰는지도 확인하지 않았다 — 이 레벨에서 인벤토리 HUD가 안 보일 것이라고 예상만 적었다.

### 남는 리스크

- **손이 안 보이는 것은 이 구성의 정상 결과다.** Epic 원본도 같다. `Variant_Shooter`를 다 가져와도 "손이 보이는 1인칭"은 되지 않는다. 총이 보였던 것은 총열이 길어서다.
- **칼로 무기를 바꾸면 위 문제가 막다른 길이 된다.** 칼은 총열 길이가 없으므로 손이 안 보이면 칼도 안 보인다. 카메라를 `head`에서 떼거나 팔을 올리는 작업이 선행돼야 한다.
- **미사용 애셋이 크게 늘었다.** 실제로 쓸 것은 `ABP_FP_Weapon`과 `Ctrl_HandAdjusment` 정도이고, AI 9개·픽업 8개·UI 3개·아레나 레벨과 외부 액터 141개는 참조 구현으로만 남는다. 지난 세션의 `Content/Weapons/` 27개와 합치면 미사용이 상당하다.
- **`SM_FoamBullet`의 깨진 참조가 그대로 들어왔다.** Epic 원본의 결함이고 우리가 만든 게 아니지만, 나중에 참조 검사를 돌리면 잡힌다.
- **`Lvl_ArenaShooter`에서 우리 `BP_ThirdPersonGameMode`가 안 쓰인다.** 그 레벨은 자체 GameMode를 쓸 가능성이 높다. 확인하지 않았다.

### 총평

요청은 "`Variant_Shooter` 확보 경로 결정"이었고, 결과적으로 **경로 결정뿐 아니라 반입까지 끝났다.** 지난 기록이 유력하다고 적어둔 경로(새 프로젝트 → Migrate)가 불필요했기 때문에 예상보다 훨씬 싸게 끝났다.

이 작업의 실질적 난이도는 복사가 아니라 **적혀 있는 계획을 의심하는 데 있었다.** 넘김 항목을 그대로 실행했다면 빈 ArenaShooter 프로젝트를 만들고 Migrate 대화상자에서 충돌 19개를 처리했을 것이다. 엔진 설치본을 먼저 뒤진 것이 그 전부를 없앴다.

반대로 **합격 기준을 잘못 세운 것은 명확한 실패다.** "손이 화면 중앙에 보인다"를 기준 1에 넣었는데, 그건 사용자가 말한 적 없고 지난 기록의 기대를 내가 옮긴 것이다. 그 결과 Epic 원본이 정상 동작하는데도 "부분 불통"으로 판정하는 이상한 상황이 됐다. **기준은 사용자의 요구에서 나와야지 이전 기록의 기대에서 나오면 안 된다.**

## AI의 제안

없음.

## 다음으로 넘김

없음. 이 세션의 미결 항목은 같은 날 후속 작업 기록인 2026-08-28-inventory-hud.md의 `다음으로 넘김`에 모았다.
