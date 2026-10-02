# Figure production and checks

Figures are the one layer with executable audits, so it is worth spelling out:

```
figure-planner          one claim per figure, panel roles, main vs supplement,
   │                    legend and Results aligned. Draws nothing.
   ▼
nature-figure           routing protocol
   ├ step 1  read the manifest plus the always-loaded contract.md / stance.md
   ├ step 2  backend gate (blocking): Python or R, remembered
   ├ step 3  load only the selected backend's fragment
   ├ step 4  build: five-point contract -> stance -> backend fragment
   ├ step 5  open any of the 17 references on demand
   └ step 6  run the audits before delivery
   ▼
figure-style            correctness checklist plus the kernel.py helpers
   ▼
audit scripts           before rendering  validate_figure.py my_figure.py
(skills/figure/         after export      audit_pdf_text.py panel_a.pdf --min-pt 5   <- per panel
 nature-figure/         after assembly    audit_figure_collisions.py fig02.pdf       <- the composite
 scripts/)              multi-panel       audit_panel_alignment.py fig02.layout.json
                        data side         figure_source_data.py -> <figure>.qa.json
                        numerics          figure_safety.py
   ▼
qa-contract.md          pre-submission checklist
```

**One exit-code contract**, shared by the four audit tools. `validate_figure.py` only ever returns 0/1/2, because a static source check always runs and can always answer; the other three also use 3 and 4:

| Code | Meaning | A pass? |
|---|---|---|
| 0 | PASS, the check ran and the figure is acceptable | yes |
| 1 | FAIL, the check ran and found a blocking problem | no |
| 2 | ERROR, usage or I/O problem; nothing was audited | no |
| 3 | NOT RUN, a required dependency is absent | no |
| 4 | NOT AUDITABLE, the input cannot answer this question | no |

Codes 2, 3, and 4 mean the figure is **unchecked**, not clean. A wrapper that branches on `returncode != 1` ships an unaudited figure, and an audit that cannot say "I could not check this" is more dangerous than no audit at all.
