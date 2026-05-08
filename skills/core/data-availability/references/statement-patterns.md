# Data Availability Statement Patterns

Use these patterns as starting points. Replace bracketed fields only with verified information.

## Public Repository, Single Dataset

```text
The [raw/processed/source] data supporting the findings of this study are available in [Repository] under accession [ACCESSION] / at [DOI or persistent URL].
```

## Public Repository, Multiple Datasets

```text
The datasets generated in this study are available as follows: [dataset family 1] in [Repository] under [DOI/accession]; [dataset family 2] in [Repository] under [DOI/accession]; and figure source data in [Repository/Supplementary Data file] under [identifier or file name].
```

## Data In Paper And Supplementary Files Only

Use only when the supporting dataset is genuinely small and fully represented in the article, source-data files, or supplementary files.

```text
All data supporting the findings of this study are included in the paper, its Supplementary Information, and Source Data files.
```

## Reused Public Data

```text
This study used publicly available [dataset name/type] from [Repository or source], available under [DOI/accession/stable URL]. We used [version/release/date accessed, if relevant].
```

## Mixed Generated And Reused Data

```text
Data generated in this study are available in [Repository] under [DOI/accession]. Public datasets reused in the analysis were obtained from [source 1, identifier/version] and [source 2, identifier/version]. Source data for [figures/tables] are provided in [location].
```

## Controlled-Access Human Or Sensitive Data

```text
The [data type] data supporting this study are not publicly available because [privacy, consent, legal, ethical or security reason]. Qualified researchers may request access from [data access committee/institutional office/repository procedure] at [contact or URL]. Access requires [ethics approval/data-use agreement/other conditions].
```

## Third-Party Or Licensed Data

```text
The [data type/name] data used in this study were obtained from [third-party provider] under licence and are not publicly redistributable by the authors. Requests for access should be directed to [provider/contact/URL].
```

## Request-Based Access With Justified Restriction

```text
The [data type] data are not publicly available because [specific reason]. Requests for access may be sent to [institutional group/contact route], and will be considered subject to [approval, agreement, or legal condition]. [Public metadata/aggregate data/source data] are available at [location].
```

## Anti-Patterns

Avoid these unless you can make them specific:

- `Data are available upon request.`
- `Data are available from the corresponding author on reasonable request.`
- `Data will be uploaded after acceptance.`
- `All data are in the manuscript.` when that is not literally true
- `Data are proprietary.` without naming the controller and access route
- `N/A.` without explanation
