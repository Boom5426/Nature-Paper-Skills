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

PMCIDs and the counting code are in the repository at `scripts/section_corpus.py`, which is not
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

## House choices that depart from the sample

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
single-cell and spatial data; CellOT is the only perturbation-response paper. Five papers are
accepted manuscripts rather than typeset versions. The coded counts rest on one reader. A pattern
that most published papers share may still be one that editors tolerate rather than reward.
