# 2026-09-04-57 · Dirty-package check before reloading Lvl_Stage — STOPPED AT STEP 1

**Result: STEP 1 tripped the stop condition. The level was NOT reloaded. Steps 2, 3 and 4 were
not performed.**

18 packages other than the level itself hold unsaved changes: the 18 `__ExternalActors__`
packages of `/Game/ThirdPerson/Lvl_Stage`, one per placed BP_Torch actor. They were dirtied by
the `compile_blueprint` call in the previous task (log 2026-09-04-56) and nothing has saved them
since. Reloading the level would have discarded them.

All raw tool responses below are verbatim, in call order, including the errors.

---

## 0 · There is no "list dirty packages" tool

Checked every toolset returned by `list_toolsets` (18 of them). The only dirty-state query
`unreal-mcp` exposes is:

```
editor_toolset.toolsets.asset.AssetTools.is_dirty
  inputSchema: {"asset_path": {"type": "string"}}
  "Checks whether an asset has unsaved changes."
```

One asset path at a time. There is no tool that returns the engine's own dirty-package list
(`UEditorLoadingAndSavingUtils::GetDirtyContentPackages` / `GetDirtyMapPackages` are not
surfaced), and there is no console-exec tool to reach one. So "list every dirty package" had to
be done by enumerating assets and calling `is_dirty` on each. The limits of that approach are
stated in section 3 and they turned out to matter.

Editor state first — a reload during PIE would be a different operation entirely:

```
call: EditorToolset.EditorAppToolset.IsPIERunning
args: {}
```

```
{"returnValue":false}
```

Also worth recording for future sessions: `call_tool` rejects the fully qualified name in
`tool_name`; the toolset prefix belongs in `toolset_name`.

```
call: EditorToolset.EditorAppToolset.IsPIERunning (passed as tool_name)
```

```
Tool 'EditorToolset.EditorAppToolset.IsPIERunning' not found
```

---

## 1 · Enumerating /Game and testing every asset

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: find_assets("", "") grouped by content root
```

```
{"roots": {"Game": 207, "Niagara": 1157, "Water": 247, "HairStrands": 100, "ACLPlugin": 2, "ControlRig": 72, "AudioWidgets": 75, "Paper2D": 17, "PCG": 311, "SpeedTreeImporter": 12, "MeshModelingToolsetExp": 55, "Landmass": 531, "MediaPlate": 14, "Fab": 75, "MeshModelingToolset": 1, "DeformerGraph": 30, "ChaosVD": 8, "Dataflow": 7, "ChaosNiagara": 6, "GeometryCollectionPlugin": 8, "NNEDenoiser": 24, "MetaHumanSDK": 3, "GeometryScripting": 1, "ResonanceAudio": 3, "AnimationSharing": 4, "MediaCompositing": 2, "ConcertSyncClient": 19, "BaseMaterial": 146, "Bridge": 95, "Mutable": 1, "UVEditor": 20, "Metasound": 2, "Takes": 4, "AnimatorKit": 35, "ControlRigModules": 116, "ControlRigSpline": 1, "GameplayCameras": 3, "DatasmithContent": 137, "GLTFExporter": 29, "InterchangeAssets": 226, "Interchange": 17, "InterchangeAxfAssets": 39}}
```

3862 assets total, 207 of them under `/Game`. `get_plugin_content_paths(include_engine=False)`
returned `[]`, so every non-`/Game` root above is engine plugin content.

The first scan of `/Game` **failed outright**. `find_assets` returns `__ExternalObjects__`
entries, but `is_dirty` refuses them, and the raised errors killed the whole script rather than
being caught by the `try/except` inside it:

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: for a in find_assets("/Game", ""): if is_dirty(a): dirty.append(a)
```

```
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

The asset registry lists these paths; `is_dirty` says they do not exist. Those two statements
disagree, and the disagreement is recorded here rather than smoothed over. Re-run with the
`__External` paths skipped:

```
call: editor_toolset.toolsets.programmatic.ProgrammaticToolset.execute_tool_script
script: same, skipping any path containing "__External"
```

```
{"total_found": 207, "skipped_external": 10, "external_sample": ["/Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/1/2C/2CHLD5GCB4WLP4X15FK46A", "/Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/5/2N/FCVKIYP6OKL5TD4S33JRIO", "/Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/6/3J/M1ISS10UBLM1HT5YP1D74G", "/Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/C/VN/7O6FXTR28IQ92JNY14ENUW", "/Game/__ExternalObjects__/ThirdPerson/Lvl_Stage/D/MP/1OU6UE00HRZKI42ATRN5WP", "/Game/__ExternalObjects__/ThirdPerson/Lvl_ThirdPerson/0/TQ/1UP2MCOIYXC0GTW985R4K0"], "scanned": 197, "dirty": [], "elapsed_sec": 17.98}
```

**197 of 197 addressable `/Game` assets: not dirty. The `dirty` list is empty.**

The two that matter individually, called on their own so the responses are unambiguous:

```
call: editor_toolset.toolsets.asset.AssetTools.is_dirty
args: {"asset_path": "/Game/ThirdPerson/Lvl_Stage"}
```

```
{"returnValue":false}
```

```
call: editor_toolset.toolsets.asset.AssetTools.is_dirty
args: {"asset_path": "/Game/Interaction/BP_Torch"}
```

```
{"returnValue":false}
```

Note that the level package itself is **not** dirty. Whatever is dirty, it is not the level.

---

## 2 · What `is_dirty` cannot see

`find_assets("/Game", "")` returns `__ExternalObjects__` paths but **no `__ExternalActors__`
paths at all**. On disk there are 113 of them for this level:

```
$ find Content/__ExternalActors__/ThirdPerson/Lvl_Stage -name '*.uasset' | wc -l
113
```

Asking `is_dirty` about one directly, using a path built from the disk layout:

```
call: editor_toolset.toolsets.asset.AssetTools.is_dirty
args: {"asset_path": "/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/0/3M/P6JIGHZ879GWQXGT391UUE"}
```

```
Asset does not exist: /Game/__ExternalActors__/ThirdPerson/Lvl_Stage/0/3M/P6JIGHZ879GWQXGT391UUE
```

So the enumeration in section 1 is blind to exactly the packages that hold this level's actors.
Its empty `dirty` list is not evidence that nothing is dirty. It had to be checked another way.

---

## 3 · The output log says 18 packages are dirty

The editor's own autosave is the witness. Autosave writes only packages that are dirty, and it
writes them to `Saved/Autosaves/` — it does **not** clear the dirty flag or touch `Content/`.

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "LogFileHelpers", "pattern": "", "maxEntries": 60}
```

```
{"returnValue":["[2026.09.04-01.19.53:350][463]LogFileHelpers: InternalPromptForCheckoutAndSave started...","[2026.09.04-01.19.53:404][463]LogFileHelpers: Saving Package: /Game/Interaction/BP_Torch","[2026.09.04-01.19.53:464][463]LogFileHelpers: InternalPromptForCheckoutAndSave took 115.253 ms","[2026.09.04-01.22.20:803][ 63]LogFileHelpers: Editor autosave (incl. external actors) for '/Game/ThirdPerson/Lvl_Stage' took 0.225","[2026.09.04-01.22.20:803][ 63]LogFileHelpers: Editor autosave (incl. sublevels & external actors) for all levels took 0.225"]}
```

The packages that autosave wrote:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "LogSavePackage", "pattern": "Moving output files for package", "maxEntries": 0}
```

```
{"returnValue":["[2026.09.04-01.19.53:426][463]LogSavePackage: Moving output files for package: /Game/Interaction/BP_Torch","[2026.09.04-01.22.20:621][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/D/KC/GT8X6H5TBDS1HXMGH1IMLU_Auto1","[2026.09.04-01.22.20:653][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/E/X0/TJILOUY6XF4UI6CNQAAIVM_Auto1","[2026.09.04-01.22.20:675][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/0/3M/P6JIGHZ879GWQXGT391UUE_Auto1","[2026.09.04-01.22.20:692][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/4/3X/2GXVP3ZH3K0QJUXBX0Z91M_Auto1","[2026.09.04-01.22.20:700][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/4/Q1/60U60G6J3GO4J6R3VQJWKU_Auto1","[2026.09.04-01.22.20:709][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/5/JW/CM2PD8NYBNR2ZTBDGX6FU8_Auto1","[2026.09.04-01.22.20:716][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/7/57/UU7NDMHA9OJ8L9W8D5AZYL_Auto1","[2026.09.04-01.22.20:721][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/7/G9/9KYQPMJ1USTU6JIQGBGHSL_Auto1","[2026.09.04-01.22.20:729][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/7/ZY/DK86JMBJG7GY1J09QO20TN_Auto1","[2026.09.04-01.22.20:734][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/8/MX/8W0U3QCKVHMJVYRFF53VVM_Auto1","[2026.09.04-01.22.20:740][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/8/YJ/PUBCXX0PV3IM7O2RMMDMRQ_Auto1","[2026.09.04-01.22.20:747][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/KW/AM1SBVWN51GLKRVO179A4L_Auto1","[2026.09.04-01.22.20:754][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/NG/W5B9FPBDBAFOWFY5W0EG1D_Auto1","[2026.09.04-01.22.20:759][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/NG/XDT24DOHOISKSPTK5Y44BC_Auto1","[2026.09.04-01.22.20:765][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/C/1Q/HMKIOS8ZGDUT8UQQLZNY89_Auto1","[2026.09.04-01.22.20:774][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/C/DU/ZF7WMSHK1V7T3MF3SOO52C_Auto1","[2026.09.04-01.22.20:781][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/C/VT/5G811NTTYAZ5DJH52GD3XM_Auto1","[2026.09.04-01.22.20:801][ 63]LogSavePackage: Moving output files for package: /Temp/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/E/TK/8818ACEC7Z8SCS0SAVQLAZ_Auto1"]}
```

**Exactly 18 external actor packages of Lvl_Stage.** The level's own package is not among them.

### The dirty list

| # | Package |
| --- | --- |
| 1 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/D/KC/GT8X6H5TBDS1HXMGH1IMLU` |
| 2 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/E/X0/TJILOUY6XF4UI6CNQAAIVM` |
| 3 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/0/3M/P6JIGHZ879GWQXGT391UUE` |
| 4 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/4/3X/2GXVP3ZH3K0QJUXBX0Z91M` |
| 5 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/4/Q1/60U60G6J3GO4J6R3VQJWKU` |
| 6 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/5/JW/CM2PD8NYBNR2ZTBDGX6FU8` |
| 7 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/7/57/UU7NDMHA9OJ8L9W8D5AZYL` |
| 8 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/7/G9/9KYQPMJ1USTU6JIQGBGHSL` |
| 9 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/7/ZY/DK86JMBJG7GY1J09QO20TN` |
| 10 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/8/MX/8W0U3QCKVHMJVYRFF53VVM` |
| 11 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/8/YJ/PUBCXX0PV3IM7O2RMMDMRQ` |
| 12 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/KW/AM1SBVWN51GLKRVO179A4L` |
| 13 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/NG/W5B9FPBDBAFOWFY5W0EG1D` |
| 14 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/B/NG/XDT24DOHOISKSPTK5Y44BC` |
| 15 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/C/1Q/HMKIOS8ZGDUT8UQQLZNY89` |
| 16 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/C/DU/ZF7WMSHK1V7T3MF3SOO52C` |
| 17 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/C/VT/5G811NTTYAZ5DJH52GD3XM` |
| 18 | `/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/E/TK/8818ACEC7Z8SCS0SAVQLAZ` |

All 18 correspond to packages that already exist in `Content/`, so these are edits to existing
actors, not newly created ones:

```
$ for p in <the 18 paths>; do [ -f "$p.uasset" ] && echo EXISTS || echo "MISSING $p"; done | sort | uniq -c
     18 EXISTS
```

And none of them is modified on disk, so the in-memory changes have never been written to
`Content/`:

```
$ git status --short -- Content/__ExternalActors__
(no output)
```

---

## 4 · Why they are dirty

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "(?i)reinstanc|recompil|compiled|BP_Torch", "maxEntries": 30}
```

The relevant lines from that response:

```
[2026.09.04-01.19.00:113][172]LogScript: Warning: /Game/Interaction/BP_Torch.BP_Torch_C is not valid Actor for property 'actor'
[2026.09.04-01.19.46:115][310]LogBlueprint: Compiling Blueprint '/Game/Interaction/BP_Torch.BP_Torch'
[2026.09.04-01.19.53:404][463]LogFileHelpers: Saving Package: /Game/Interaction/BP_Torch
[2026.09.04-01.19.53:426][463]LogSavePackage: Moving 'D:/20260827/MCP1/Saved/BP_Torch69224EF94698E892A36A4B95B4535521.tmp' to 'D:/20260827/MCP1/Content/Interaction/BP_Torch.uasset'
[2026.09.04-01.19.53:497][464]AssetCheck: /Game/Interaction/BP_Torch Validating asset
[2026.09.04-01.21.04:243][727]LogScript: Warning: GetObjectProperties on '/Game/ThirdPerson/Lvl_Stage.Lvl_Stage:PersistentLevel.BP_Torch_C_UAID_9C6B005AF86948FE02_1636115423.Light' (PointLightComponent): the following properties could not be read: CastShadow
```

And everything the editor did between the compile and the autosave:

```
call: EditorToolset.LogsToolset.GetLogEntries
args: {"category": "", "pattern": "01\\.19\\.|01\\.20\\.|01\\.21\\.", "maxEntries": 40}
```

That response is all `LogModelContextProtocol: Dispatching toolset tool:` lines for
`is_dirty`, `get_properties`, `get_current_level`, `find_actors`, `get_components` — reads only —
plus the `LogScript` warning above and some `LogEOSSDK` chatter. No writes.

Timeline, in UTC as the log stamps it (KST is +9):

| Time | Event |
| --- | --- |
| 01:19:46 | `Compiling Blueprint '/Game/Interaction/BP_Torch.BP_Torch'` |
| 01:19:53 | `BP_Torch.uasset` saved to `Content/` |
| 01:19:56 – 01:21:16 | read-only MCP calls only |
| 01:22:20 | autosave writes 18 Lvl_Stage external actor packages |

Compiling the Blueprint reinstanced the 18 placed BP_Torch actors, and reinstancing marked each
actor's own package dirty. Nothing has saved those packages since — there is no
`LogFileHelpers: Saving Package` line for any of them, and `git status` shows `Content/` clean —
so they are still dirty now.

**How firm is that:** the 18 entries in the dirty list are read directly from the log, verbatim.
That they are *still* dirty is inference, not a direct read: `is_dirty` cannot address these
packages at all (section 2), so there is no tool call that can confirm it. The inference rests on
autosave never clearing the dirty flag, and on the absence of any save of these packages
afterwards. It is not a measurement.

---

## 5 · What was not checked

- **3655 engine plugin content assets** across the 41 non-`/Game` roots listed in section 1.
  At the observed rate of ~91 ms per `is_dirty` call that is roughly 5.5 minutes of editor time,
  and CLAUDE.md forbids running long operations without asking first. None of them is a project
  asset and nothing this session touched could have dirtied them, but they were **not** verified.
- **The 10 `/Game/__ExternalObjects__` packages** — `is_dirty` errors on every one of them.
- **The other 95 `__ExternalActors__` packages** of Lvl_Stage (113 on disk, 18 accounted for
  above). They are unreachable by `is_dirty` and they did not appear in the autosave, which is
  reason to think they are clean but is not the same as having checked them.

---

## 6 · Steps 2, 3 and 4: not performed

`SceneTools.load_level("/Game/ThirdPerson/Lvl_Stage")` was **not** called. The instruction was to
stop if any package other than the level itself is dirty, and 18 are. Reloading the level
discards the in-memory state of its actor packages, so it would have thrown away the 18 dirtied
torch actors without a further decision.

Nothing in the editor was changed by this task. Every call above is a read.

---

## 7 · What this means for the question behind the reload

The reload was meant to test whether the 18 placed torches pick up the new class default
`CastShadow = false` once constructed fresh from disk. The dirty flags say something about that
before the test is even run: the compile *did* reach the 18 actors — it reinstanced them and
dirtied their packages — and yet immediately afterwards they still read `CastShadow = true`
(log 2026-09-04-56, section 6). An actor that was reconstructed and still reports the old value is
carrying a per-instance override, which is what a reload would confirm rather than fix.

Two ways forward, both needing a decision:

1. **Discard and reload.** Accept losing the 18 dirty packages (they are unmodified on disk and
   committed in git, so "losing" them means returning to the committed state) and reload to run
   the test as written.
2. **Clear the overrides instead.** `ObjectTools.reset_properties` with `["CastShadow"]` on
   Backplate / Bracket / Cup for each of the 18 actors, then save the level. This changes the
   level rather than testing it, and it is an 18-actor write.

Autosave copies of the 18 packages are sitting in `Saved/Autosaves/Game/__ExternalActors__/ThirdPerson/Lvl_Stage/`
if their current in-memory state ever needs recovering.
