# Section evidence

This file records the sample behind the typical ranges and the method-paper patterns in
[section-contracts.md](section-contracts.md). It describes what published papers do. It does not show
that a pattern causes acceptance, and it is not a format specification: formats come from the
journal's current guide.

## Sample

- **Source and date:** Europe PMC, searched on 2026-10-09.
- **Frame:** open-access research papers with full text, published 2022 to 2025 in Nature Methods,
  Nature Biotechnology or Nature Communications, with "single-cell", "single cell", "spatial
  transcriptomics", "spatially" or "perturbation" in the title; sorted by citation count.
- **Inclusion:** per journal, the first ten papers that introduce a named computational method.
  Biology atlases, wet-laboratory methods and benchmarks were skipped.
- **Excluded after inclusion:** CytoTRACE 2 and CytoSPACE, which are Brief Communications without
  Results or Discussion headings. That leaves 28 Articles.
- **Accepted manuscripts:** alevin-fry, Milo, CARD, Scissor and DestVI were available only as
  accepted manuscripts. They count towards structure but not towards abstract length or figure
  counts.

| Journal | Articles |
|---|---|
| Nature Methods | SCENIC+, CellRank, COMMOT, CellRank 2, CellOT, scPoli, alevin-fry, Nicheformer, SATURN |
| Nature Biotechnology | Milo, scArches, CARD, GLUE, Scissor, DestVI, SEACells, Higashi, MaxFuse |
| Nature Communications | ScType, STAGATE, GraphST, ALRA, SpatialPCA, STdeconvolve, dsb, SpaTalk, scDEAL, nnSVG |

PMCIDs for both samples and the counting code are in the repository at `scripts/section_corpus.py`, which is not
part of the installed skill. Run it with `--xml-dir <cache>` to fetch the same papers and recompute
every count in the next section.

## Counted by script

| Measure | Result |
|---|---|
| Abstract length, typeset Nature Methods (n = 8) | 148–156 words |
| Abstract length, typeset Nature Biotechnology (n = 5) | 140–170 words |
| Abstract length, typeset Nature Communications (n = 10) | 75–201 words |
| Abstract sentences, typeset (n = 23) | median 6, interquartile range 5–7, range 3–8 |
| Position of the sentence introducing the study | 2nd in 11, 3rd in 14, 4th in 2, 6th in 1 (an accepted manuscript) |
| Abstracts with a performance number | 2 by pattern; 3 on reading ("four orders of magnitude fewer parameters") |
| Introduction paragraphs | median 4, range 3–7; 3–5 in 22 of 28 |
| Results subsections | median 6, range 5–13; 5–8 in 26 of 28 |
| Paragraphs per Results subsection (n = 180) | median 4, interquartile range 3–6 |
| Opening sentence of subsections after the first (n = 152) | question, context or claim 83; sequence ("Next", "We next") 30; action ("We ...") 21; purpose ("To ...") 18 |
| Numbers per Results paragraph (n = 827) | median 2; none in 248; five or more in 252 |
| Subsections whose last sentence states an interpretation | 81 of 180 (takeaway marker or interpretive verb) |
| Discussion paragraphs (n = 27; ALRA combines Results and Discussion) | median 5, interquartile range 5–7, range 2–11; 3–5 in 13; 4–8 in 22 |
| Discussions comparing the method with other methods | 20 of 27 |
| Main figures, typeset (n = 23) | median 5, range 3–7 |
| Title or abstract uses "novel" / "powerful" | 0 / 0 of 28 |
| First Results heading "Overview of X" or "Method overview" | 11 of 28 |
| Typeset abstracts with a semicolon | 3 of 23 |
| Results and Discussion paragraphs without a semicolon (n = 982) | 749 (one in 133, two or more in 100) |

## Coded by reading

One reader coded these from the paragraph openings, headings and captions. Treat the counts as
approximate.

- **Final Introduction paragraph:** previews findings application by application in 14 of 28,
  in one or two sentences in 9, and not at all in 5.
- **First Results subsection presents the method:** 23 of 28. CARD, ScType, ALRA, STdeconvolve
  and dsb open with a result.
- **Results order:** the comparison with baselines is the second subsection in about 15 of 28; the
  last subsection is a biological application or discovery in about 20 of 28.
- **Results headings:** about two thirds state a finding rather than name a topic or dataset.
- **Fig. 1:** presents the method in 25 of the 27 papers with a captioned Fig. 1; dsb and nnSVG
  open with a result.
- **Title:** 16 of 28 omit the method name and describe the task and the key idea; 4 of 28 are claim
  sentences.
- **Discussion:** the first paragraph restates the contribution in about 22 of 27; genuine
  limitations are followed by a separate outlook paragraph in about 15 and share the final
  paragraph with the outlook in about 6; the last sentence is a field-level outlook in about 18 and a
  software availability statement in 4.

## Reader: method Articles compared with `Nature`

The broad register in the contracts' Readers section was checked against a second sample, selected
on 2026-10-10 from Europe PMC: open-access `Nature` papers from 2020 to 2025 with method-like title
terms, sorted by citations, keeping the first twelve that introduce a computational method for
biology or medicine (AlphaFold, AlphaFold 3, ModelAngelo, RETFound, Prov-GigaPath, AF-Cluster, a
breast cancer response predictor, Chroma, luciferase design, NYUTron, Swarm Learning and EVEscape).
SCimilarity and GET, the only single-cell or transcription methods among the 80 candidates, are a
supplement and are not counted. Only abstracts were read. One reader coded them.

| Abstract feature | 28 method Articles | 12 `Nature` papers |
|---|---|---|
| First sentence states a biological or biomedical stake | 3 (CellOT, Nicheformer, DestVI; SATURN in part) | 6 |
| First sentence states a specific problem, limit or need | 8 | 5 |
| A specific problem stated by the end of the second sentence | 18 | 8 |
| Two opening sentences without a specific problem | 10 (5 go straight to "Here we present") | 4 |
| Method introduced by what it does before how it works | 14 | 9 |
| Success measured against experiment, expert work or known biology | 1 or 2 | about 6 |
| Main finding framed as a capability or biological insight first | about 8 | 7 (3 more mix it with a benchmark) |
| Last sentence states a field-level implication | most; 8 end on software availability | 11 |
| Model-internal terms per abstract (script) | median 1, none in 9 | median 1, none in 4 |
| Any number a reader can use (typeset abstracts only) | 7 of 23 | 8 of 12 |
| Scale of the data or validation (cells, images, patients, proteins tested, tasks) | 4 | 6 |
| Size of a gain or a result, with its comparison or units | 3 | 5 |
| Abstracts with a semicolon (script) | 3 of 23 | 1 of 12 |

The model-internal terms row is the decisive one. Breadth does not come from using fewer technical
terms: both samples name model families at the same rate. It comes from framing: how soon the
reader meets the problem, what success is measured against, and in whose terms the finding is
stated.

What separates strong openings from weak ones is not biology against technology. Strong openings
state a limit the reader meets in their own work, often in technical words ("Many spatially resolved
transcriptomic technologies do not have single-cell resolution" in CARD, and "Interpreting electron
cryo-microscopy (cryo-EM) maps with atomic models requires high levels of expertise and
labour-intensive manual intervention" in ModelAngelo). Weak openings are truisms that could open any
paper in the field, biological ("Tissue makeup depends on the local cellular microenvironment",
Nicheformer) as often as technical ("Recent advances in spatially resolved transcriptomics have
enabled ...", STAGATE). A general first sentence is the majority in both samples (20 of 28 and 7 of
12). It works when the second sentence states the problem, as in AlphaFold ("... but this represents
a small fraction of the billions of known protein sequences"). The opening rows were coded by one
reader from the first two sentences of each abstract.

Broad framing does not mean fewer numbers. The `Nature` abstracts carry more of them than the method
Articles: the scale of the evidence ("1.6 million unlabelled retinal images", "more than 16,400 blood
transcriptomes derived from 127 clinical studies", "experimental characterization of 310 proteins")
and the size of the result in units a field reader can judge ("an area under the curve of 0.87",
"an improvement of 5.36-14.7% in the AUC compared with traditional models", "25 out of 26 tasks", "a
backbone root-mean-square deviation of around 1.0 Å"). One abstract carries about ten numbers. Seven
state their main result in words only, and four of these compare it with experiment or human
experts ("accuracy competitive with experimental structures", "of similar quality to those generated
by human experts", "as accurate as high-throughput experimental scans"). The number rows were coded
by one reader from the abstracts. Numbers in citations, names and background dates were not counted,
and one `Nature` abstract counts only for a number giving the scale of the problem ("around 100,000
unique proteins" against "billions of known protein sequences").

## House choices that depart from the sample

- **Reader:** checks 2 to 4 of the contracts' Readers section are house choices. Most method
  Articles in the first sample measure success only against other algorithms and state findings as
  benchmark gains. The `Nature` sample shows the register those checks ask for. Check 1, that the
  reader meets the problem by the second sentence, follows the majority of both samples.
- **Discussion length:** the contracts set 3–5 paragraphs; 13 of 27 papers fall in that range and
  the median is 5. The narrower range keeps the three moves compact.
- **Final Introduction paragraph:** the contracts ask for an enlarged version of the Abstract's
  findings, not an application-by-application preview, which is the most common form in the
  sample (14 of 28). This avoids repeating the Results in advance.
- **Results openers:** the contracts treat procedural openers as acceptable occasionally but not as
  the default. The sample's majority (83 of 152) already opens with the question or context, but
  69 of 152 use a procedural opener, so this is a preference rather than a norm.
- **Explicit interpretation at the end of a subsection:** required only when the inference is not
  obvious from the observation; 81 of 180 subsections in the sample end this way.

## Limits

The sample ranks by citation count, so 2022 papers are over-represented and recent ones are scarce.
It includes only open-access papers in three journals, and only computational methods for
single-cell and spatial data; CellOT is the only perturbation-response paper. The `Nature` sample
is small, spans protein structure and clinical prediction rather than single-cell biology, and was
read only at the level of the abstract. Five papers are
accepted manuscripts rather than typeset versions. The coded counts rest on one reader. A pattern
that most published papers share may still be one that editors tolerate rather than reward.
