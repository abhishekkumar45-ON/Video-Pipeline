# MANIFEST | heat-on-the-isobaric-leg | fps 30 | narration offset 5.000s
# script: masterclass/t1_script.md | audio: t1_narration.wav (Kokoro af_bella, PENDING) | alignment: PENDING (forced-alignment of final take)
# NOTE: frame numbers below are PROVISIONAL, computed at 145 wpm from the script. The renderer is a
#       manim-voiceover scene (scenes/t1.py -> Scene_t1): each beat's animations are auto-synced to the
#       spoken audio, which satisfies Law 2 (seen when spoken) at sentence granularity. Re-derive exact
#       frame anchors against the aligned final take before any frame-locked delivery.

PERSISTENT STATE OBJECTS
  AGENDA      : born SCENE 003 (decode); entries C1 "adiabatic relation", C2 "isobaric heat"; each
                resolves on its RETURN cue; dies entering SCENE 010 (compression).
  CANVAS      : the V-versus-T cycle + equation stack (slots T_X, T_Y, Q). Born SCENE 001. Parks on
                each WALL, restores from snapshot on each RETURN. Never redrawn.
  EQ_STACK    : lives lower-left of canvas; lines accumulate (adiabatic link, T_Y doubling, heat line).
  BLOCK_SPACE : opens on WALL, collapses on RETURN; carries one guard card back each time.

[SCENE 001 | seg 2 question-card | in 00:05.00 f150 | out 00:20.00 f600]
state_in: [sting handoff background]
elements:
  - id: qcard        enter f150  anchor "JEE"            motion: assemble per guideline
  - id: meta         enter f156  anchor "twenty"         motion: settle (year/paper/marks)
  - id: cycle_VT     enter f168  anchor "cycle"          motion: draw W,X,Y skeleton on V-vs-T
  - id: vol_labels   enter f300  anchor "sixty"          motion: 64,125,250 highlight as read
  - id: anchor_1J    enter f470  anchor "one joule"      motion: nRT_W = 1 J settles
  - id: find_line    enter f560  anchor "heat"           motion: "heat on X->Y" glows on the leg
state_out: [qcard live, cycle_VT live, anchor_1J live]

[SCENE 002 | seg 3 attempt-pause | in 00:20.00 f600 | out 00:25.00 f750]
elements:
  - id: countdown    enter on cue final word "first" +0ms   duration 150f exactly
constraints: no other motion; no captions; question fully visible

[SCENE 003 | seg 4 decode + agenda | in 00:25.00 f750 | out 00:51.00 f1530]
state_in: [cycle_VT live]
elements:
  - id: given_block  enter f762  anchor "given"          motion: 3 volumes + energy anchor list in
  - id: find_block   enter f900  anchor "need"           motion: X->Y leg glows as target
  - id: agenda_C1    enter f980  anchor "adiabatic"      motion: agenda entry 1 enters
  - id: agenda_C2    enter f1000 anchor "isobaric"       motion: agenda entry 2 enters
  - id: promise      enter f1470 anchor "three"          motion: "solution = 3 lines" tag pins
state_out: [agenda live (C1,C2 pending), canvas live]

[SCENE 004 | seg 5 STEP 1 | in 00:51.00 f1530 | out 01:05.00 f1950]
elements:
  - id: slot_TX      enter f1560 anchor "temperatures"   motion: empty T_X, T_Y slots appear in EQ_STACK
  - id: back_arrow   enter f1740 anchor "adiabatic"      motion: arrow points along W->X leg
state_out: [canvas live, slots empty]

[SCENE 005 | seg 5 WALL 1 -> BLOCK C1 | in 01:05.00 f1950 | out 03:05.00 f5550]
state_in: [canvas live: cycle_VT, slots]
actions:
  - park:   canvas -> parked slot, snapshot S1 saved      anchor "stops us"
  - open:   block_space_C1                                 anchor "adiabatic process"
  - agenda: highlight C1                                   anchor "current"
elements:
  - id: c1_cyl       enter f2010 anchor "trades no heat"  motion: insulated cylinder; compress=heat, expand=cool
  - id: c1_res1      enter f2460 anchor "constant"        motion: card "T V^(gamma-1) = const"
  - id: c1_res2      enter f2620 anchor "atoms"           motion: card Cv=3/2R, Cp=5/2R, gamma=5/3, g-1=2/3
  - id: c1_trap      enter f3040 anchor "reflex"          motion: tempting "T V = const" writes...
  - id: c1_break     enter f3260 anchor "break"           motion: ...cross strikes it (exponent 1 wrong)
  - id: c1_guard     enter f3420 anchor "guard"           motion: guard card "use exponent 2/3" boxes
  - id: c1_jee       enter f4520 anchor "clean powers"    motion: 64^(2/3)=16, 125^(2/3)=25 flash integer
actions_end:
  - collapse: block_space_C1                               anchor "Back"
  - restore:  canvas from snapshot S1                      anchor "Back"
  - agenda:   resolve C1                                   anchor "Back"
  - carryback: c1_guard -> canvas margin
sync_note: RETURN cue at ~f5490; blocked STEP 2 must resolve by ~f6150 (within two-sentence window)

[SCENE 006 | seg 5 STEP 2 (resolves via C1) | in 03:05.00 f5550 | out 03:27.00 f6210]
elements:
  - id: eq_adia      enter f5580 anchor "equal at both"   motion: T_W*64^(2/3)=T_X*125^(2/3) writes
  - id: eq_nums      enter f5760 anchor "sixteen"         motion: 16*T_W = 25*T_X, numbers drop from guard
  - id: fill_TX      enter f6060 anchor "sixteen twenty"  motion: slot_TX fills = (16/25) T_W
  - id: hl_XY        enter f6150 anchor "highlights"      motion: X->Y leg highlights as next target
state_out: [canvas live, T_X filled, T_Y empty]

[SCENE 007 | seg 5 WALL 2 -> BLOCK C2 | in 03:27.00 f6210 | out 05:27.00 f9810]
state_in: [canvas live: T_X filled]
actions:
  - park:   canvas -> parked slot, snapshot S2 saved      anchor "stops us again"
  - open:   block_space_C2                                 anchor "isobaric process"
  - agenda: highlight C2                                   anchor "current"
elements:
  - id: c2_cyl       enter f6270 anchor "held fixed"      motion: free-piston cylinder under constant weight
  - id: c2_lockstep  enter f6420 anchor "together"        motion: V bar and T bar rise in lockstep
  - id: c2_split     enter f6540 anchor "two jobs"        motion: heat arrow splits -> internal energy + work
  - id: c2_res1      enter f6900 anchor "constant pressure" motion: card "Q = n Cp dT", Cp=5/2R
  - id: c2_res2      enter f7080 anchor "doubling"        motion: card "V doubles => T doubles"; fill T_Y=2T_X
  - id: c2_trap      enter f7500 anchor "reaches for"     motion: tempting Cv=3/2R writes...
  - id: c2_break     enter f7700 anchor "breaks"          motion: ...cross; missing R work-term added -> Cp
  - id: c2_guard     enter f7880 anchor "guard"           motion: guard card "constant pressure takes Cp"
  - id: c2_jee       enter f8760 anchor "plain sight"     motion: anchor nRT_W=1J glows, thread to heat expr
actions_end:
  - collapse: block_space_C2                               anchor "Back"
  - restore:  canvas from snapshot S2                      anchor "Back"
  - agenda:   resolve C2                                   anchor "Back"
  - carryback: c2_guard -> canvas margin
sync_note: RETURN cue at ~f9750; STEP 3 resolves to the boxed answer within two sentences

[SCENE 008 | seg 5 STEP 3 (resolves via C2) + PAYOFF | in 05:27.00 f9810 | out 05:53.00 f10590]
elements:
  - id: fill_TY      enter f9840 anchor "twice"           motion: T_Y = 2 T_X confirmed
  - id: eq_heat      enter f9960 anchor "heat is"         motion: Q = (5/2) nR * (16/25) T_W assembles
  - id: bundle_1J    enter f10200 anchor "one joule"      motion: nR*T_W group lights, collapses to 1
  - id: answer_box   enter f10380 anchor "one point six" motion: (beat) 1.6 J boxes as the answer
constraints: payoff motion (answer boxing) lands inside the (beat); no competing motion
state_out: [answer boxed on canvas; both guard cards in margin]

[SCENE 009 | seg 6 variant sweep | in 05:53.00 f10590 | out 06:17.00 f11310]
elements:
  - id: var_1  enter f10620 anchor "W to X"     motion: card, heat=0 (adiabatic leg)
  - id: var_2  enter f10770 anchor "work"       motion: card, ask work not heat
  - id: var_3  enter f10920 anchor "diatomic"   motion: card, Cp -> 7/2 R
  - id: var_4  enter f11070 anchor "whole cycle" motion: card, net cycle heat
state_out: [4 variant cards live]

[SCENE 010 | seg 7 exam craft | in 06:17.00 f11310 | out 06:37.00 f11910]
actions:
  - agenda: DIE (tracker retires before compression)
elements:
  - id: replay   enter f11340 anchor "thirty second"  motion: fast skim of the 3 canvas lines
  - id: pow_flash enter f11460 anchor "cubes"          motion: 16 and 25 pulse
  - id: frac_flash enter f11760 anchor "sixteen twenty" motion: final fraction pulses
state_out: [craft strip live]

[SCENE 011 | seg 8 compression | in 06:37.00 f11910 | out 06:55.00 f12450]
state_in: [clear stage]
elements:
  - id: sum_concepts enter f11940 anchor "two ideas"   motion: C1,C2 named
  - id: sum_method   enter f12060 anchor "Temperature at X" motion: 3 method lines assemble
  - id: sum_guards   enter f12330 anchor "guards"       motion: 2 guard rules pin
constraints: frame must read standalone with audio muted
state_out: [compression card live]

[SCENE 012 | seg 9 outro bridge | in 06:55.00 f12450 | out 07:20.00 f13200]
elements:
  - id: outro     enter on bridge first word "Two"    motion: outro asset (cached, out of scope)
  - id: sibling   enter f12480 anchor "screen now"     motion: sibling question thumbnail slides in
runtime_check: total ~07:20, inside 3:00 to 8:00. captions: question-card first word (f150) through outro line last word.
