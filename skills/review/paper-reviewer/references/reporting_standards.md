# Scientific Reporting Standards and Guidelines

This catalogs major reporting standards across disciplines. As the referee, verify that authors followed
the appropriate guideline for their study type. Answering a compliance comment, use it to find the
specific item at issue, because an item-level answer closes the point and a general claim of compliance
does not.

`scientific-writing` owns which guideline to follow while drafting. This file is the referee-side and
reply-side view: which guideline a referee will check against, and what a reply must show to close the
ask.

## Contents

- [Nature Portfolio requirements](#nature-portfolio-requirements)
- Clinical trials and medical research: CONSORT, STROBE, PRISMA, SPIRIT, CARE
- Animal research: ARRIVE
- Genomics and molecular biology: MIAME, MINSEQE, MIGS/MIMS
- Structural biology: PDB deposition
- Proteomics and mass spectrometry: MIAPE
- Neuroscience: COBIDAS
- Flow cytometry: MIFlowCyt
- Ecology and environmental science: MIAPPE
- Chemistry and chemical biology: MIRIBEL
- Quality assessment and bias: CAMARADES, SYRCLE
- [General principles across guidelines](#general-principles-across-guidelines)
- [Answering a guideline comment](#answering-a-guideline-comment)

## Nature Portfolio requirements

These apply across the portfolio and are the ones most likely to appear in a real referee report or an
editorial requirement, yet they sit outside the discipline catalogue below.

**Reporting Summary.** Authors of research articles in the life sciences, behavioural and social
sciences, and ecology, evolution and environmental sciences must complete a reporting summary covering
elements of experimental and analytical design that are frequently poorly reported. It is available to
editors and reviewers during assessment and is published with all accepted manuscripts. In the physical
sciences it applies to solar cells and to claims of lasing.

**Editorial Policy Checklist.** Also visible to reviewers during assessment. A referee may raise a point
that comes from the checklist rather than from the manuscript text.

**Code availability.** A `Code availability` statement is required as a separate section after the data
availability statement and before the references. Nature journals peer-review custom code, mathematical
algorithms, and software when they are central to the manuscript, and some titles expose a separate
code-assessment section in the referee form.

**Data availability.** See `data-availability` for drafting and auditing the statement itself.

Reference: Nature Portfolio, Reporting standards and availability of data, materials, code and
protocols, https://www.nature.com/nature-portfolio/editorial-policies/reporting-standards

## Clinical Trials and Medical Research

### CONSORT (Consolidated Standards of Reporting Trials)
**Purpose:** Randomized controlled trials (RCTs)
**Key Requirements:**
- Trial design, participants, and interventions clearly described
- Primary and secondary outcomes specified
- Sample size calculation and statistical methods
- Participant flow through trial (enrollment, allocation, follow-up, analysis)
- Baseline characteristics of participants
- Numbers analyzed in each group
- Outcomes and estimation with confidence intervals
- Adverse events
- Trial registration number and protocol access

**Reference:** http://www.consort-statement.org/

### STROBE (Strengthening the Reporting of Observational Studies in Epidemiology)
**Purpose:** Observational studies (cohort, case-control, cross-sectional)
**Key Requirements:**
- Study design clearly stated
- Setting, eligibility criteria, and participant sources
- Variables clearly defined
- Data sources and measurement methods
- Bias assessment
- Sample size justification
- Statistical methods including handling of missing data
- Participant flow and characteristics
- Main results with confidence intervals
- Limitations discussed

**Reference:** https://www.strobe-statement.org/

### PRISMA (Preferred Reporting Items for Systematic Reviews and Meta-Analyses)
**Purpose:** Systematic reviews and meta-analyses
**Key Requirements:**
- Protocol registration
- Systematic search strategy across multiple databases
- Inclusion/exclusion criteria
- Study selection process
- Data extraction methods
- Quality assessment of included studies
- Statistical methods for meta-analysis
- Assessment of publication bias
- Heterogeneity assessment
- PRISMA flow diagram showing study selection
- Summary of findings tables

**Reference:** http://www.prisma-statement.org/

### SPIRIT (Standard Protocol Items: Recommendations for Interventional Trials)
**Purpose:** Clinical trial protocols
**Key Requirements:**
- Administrative information (title, registration, funding)
- Introduction (rationale, objectives)
- Methods (design, participants, interventions, outcomes, sample size)
- Ethics and dissemination
- Trial schedule and assessments

**Reference:** https://www.spirit-statement.org/

### CARE (CAse REport guidelines)
**Purpose:** Case reports
**Key Requirements:**
- Patient information and demographics
- Clinical findings
- Timeline of events
- Diagnostic assessment
- Therapeutic interventions
- Follow-up and outcomes
- Patient perspective
- Informed consent

**Reference:** https://www.care-statement.org/

## Animal Research

### ARRIVE (Animal Research: Reporting of In Vivo Experiments)
**Purpose:** Studies involving animal research
**Key Requirements:**
- Title indicates study involves animals
- Abstract provides accurate summary
- Background and objectives clearly stated
- Ethical statement and approval
- Housing and husbandry details
- Animal details (species, strain, sex, age, weight)
- Experimental procedures in detail
- Experimental animals (number, allocation, welfare assessment)
- Statistical methods appropriate
- Exclusion criteria stated
- Sample size determination
- Randomization and blinding described
- Outcome measures defined
- Adverse events reported

**Reference:** https://arriveguidelines.org/

## Genomics and Molecular Biology

### MIAME (Minimum Information About a Microarray Experiment)
**Purpose:** Microarray experiments
**Key Requirements:**
- Experimental design clearly described
- Array design information
- Samples (origin, preparation, labeling)
- Hybridization procedures and parameters
- Image acquisition and quantification
- Normalization and data transformation
- Raw and processed data availability
- Database accession numbers

**Reference:** http://fged.org/projects/miame/

### MINSEQE (Minimum Information about a high-throughput Nucleotide Sequencing Experiment)
**Purpose:** High-throughput sequencing (RNA-seq, ChIP-seq, etc.)
**Key Requirements:**
- Experimental design and biological context
- Sample information (source, preparation, QC)
- Library preparation (protocol, adapters, size selection)
- Sequencing platform and parameters
- Data processing pipeline (alignment, quantification, normalization)
- Quality control metrics
- Raw data deposition (SRA, GEO, ENA)
- Processed data and analysis code availability

### MIGS/MIMS (Minimum Information about a Genome/Metagenome Sequence)
**Purpose:** Genome and metagenome sequencing
**Key Requirements:**
- Sample origin and environmental context
- Sequencing methods and coverage
- Assembly methods and quality metrics
- Annotation approach
- Quality control and contamination screening
- Data deposition in INSDC databases

**Reference:** https://gensc.org/

## Structural Biology

### PDB (Protein Data Bank) Deposition Requirements
**Purpose:** Macromolecular structure determination
**Key Requirements:**
- Atomic coordinates deposited
- Structure factors for X-ray structures
- Restraints and experimental data for NMR
- EM maps and metadata for cryo-EM
- Model quality validation metrics
- Experimental conditions (crystallization, sample preparation)
- Data collection parameters
- Refinement statistics

**Reference:** https://www.wwpdb.org/

## Proteomics and Mass Spectrometry

### MIAPE (Minimum Information About a Proteomics Experiment)
**Purpose:** Proteomics experiments
**Key Requirements:**
- Sample processing and fractionation
- Separation methods (2D gel, LC)
- Mass spectrometry parameters (instrument, acquisition)
- Database search and validation parameters
- Peptide and protein identification criteria
- Quantification methods
- Statistical analysis
- Data deposition (PRIDE, PeptideAtlas)

**Reference:** http://www.psidev.info/

## Neuroscience

### COBIDAS (Committee on Best Practices in Data Analysis and Sharing)
**Purpose:** MRI and fMRI studies
**Key Requirements:**
- Scanner and sequence parameters
- Preprocessing pipeline details
- Software versions and parameters
- Statistical analysis approach
- Multiple comparison correction
- ROI definitions
- Data sharing (raw data, analysis scripts)

**Reference:** https://www.humanbrainmapping.org/cobidas

## Flow Cytometry

### MIFlowCyt (Minimum Information about a Flow Cytometry Experiment)
**Purpose:** Flow cytometry experiments
**Key Requirements:**
- Experimental overview and purpose
- Sample characteristics and preparation
- Instrument information and settings
- Reagents (antibodies, fluorophores, concentrations)
- Compensation and controls
- Gating strategy
- Data analysis approach
- Data availability

**Reference:** http://flowcyt.org/

## Ecology and Environmental Science

### MIAPPE (Minimum Information About a Plant Phenotyping Experiment)
**Purpose:** Plant phenotyping studies
**Key Requirements:**
- Investigation and study metadata
- Biological material information
- Environmental parameters
- Experimental design and factors
- Phenotypic measurements and methods
- Data file descriptions

**Reference:** https://www.miappe.org/

## Chemistry and Chemical Biology

### MIRIBEL (Minimum Information Reporting in Bio-Nano Experimental Literature)
**Purpose:** Nanomaterial characterization
**Key Requirements:**
- Nanomaterial composition and structure
- Size, shape, and morphology characterization
- Surface chemistry and functionalization
- Purity and stability
- Experimental conditions
- Characterization methods

## Quality Assessment and Bias

### CAMARADES (Collaborative Approach to Meta-Analysis and Review of Animal Data from Experimental Studies)
**Purpose:** Quality assessment for animal studies in systematic reviews
**Key Items:**
- Publication in peer-reviewed journal
- Statement of temperature control
- Randomization to treatment
- Blinded assessment of outcome
- Avoidance of anesthetic with marked intrinsic properties
- Use of appropriate animal model
- Sample size calculation
- Compliance with regulatory requirements
- Statement of conflict of interest
- Study pre-registration

### SYRCLE's Risk of Bias Tool
**Purpose:** Assessing risk of bias in animal intervention studies
**Domains:**
- Selection bias (sequence generation, baseline characteristics, allocation concealment)
- Performance bias (random housing, blinding of personnel)
- Detection bias (random outcome assessment, blinding of assessors)
- Attrition bias (incomplete outcome data)
- Reporting bias (selective outcome reporting)
- Other sources of bias

## General Principles Across Guidelines

### Common Requirements
1. **Transparency:** All methods, materials, and analyses fully described
2. **Reproducibility:** Sufficient detail for independent replication
3. **Data Availability:** Raw data and analysis code shared or deposited
4. **Registration:** Studies pre-registered where applicable
5. **Ethics:** Appropriate approvals and consent documented
6. **Conflicts of Interest:** Disclosed for all authors
7. **Statistical Rigor:** Methods appropriate and fully described
8. **Completeness:** All outcomes reported, including negative results

### Red Flags for Non-Compliance
- Methods section lacks critical details
- No mention of following reporting guidelines
- Data availability statement missing or vague
- No database accession numbers for omics data
- No trial registration for clinical studies
- Sample size not justified
- Statistical methods inadequately described
- Missing flow diagrams (CONSORT, PRISMA)
- Selective reporting of outcomes

## How to Use This Reference

When reviewing a manuscript:
1. Identify the study type and discipline
2. Find the relevant reporting guideline(s)
3. Check if authors mention following the guideline
4. Verify that key requirements are addressed
5. Note any missing elements in your review
6. Suggest the appropriate guideline if not mentioned

Many journals require authors to complete reporting checklists at submission. Reviewers should verify compliance even if a checklist was submitted.

## Answering a guideline comment

A completed checklist is not an answer to `item 11b is missing`. Run the same six steps backwards:

1. Name the guideline the referee named, in their words, even if you would have cited a different one.
2. Find the specific item behind the comment. Referees usually describe the item rather than number it,
   so translate their description into the item and cite the number.
3. Say where that item now appears: manuscript section and page, Reporting Summary field, or
   supplementary note. An item-level location closes the point; `we followed CONSORT` does not.
4. If the item genuinely does not apply, say why in one sentence, and say what you reported instead.
5. If the study does not fit the guideline the referee cited, name the guideline it does fit and why, in
   one sentence, without lecturing.
6. If the ask reaches the Reporting Summary or the Editorial Policy Checklist, remember the referee can
   already see both. Point at the field rather than describing what you put in it.
