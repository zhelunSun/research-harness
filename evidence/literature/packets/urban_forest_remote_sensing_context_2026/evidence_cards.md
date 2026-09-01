# Evidence cards: urban-forest remote-sensing context

> Packet: `urban-forest-remote-sensing-context-2026`
>
> Full-text state: four peer-reviewed PDFs inspected
>
> Zotero state: absent by exact title and DOI; import not authorized
>
> Writing state: provisional keys; no contract merge

## Evidence-grade convention

- `G1-R`: peer-reviewed formal review; the claim is limited to the review's included literature and stated synthesis.
- `G1-P`: peer-reviewed primary study; the claim is limited to the reported study design, place, data, and interpretation.

## S-UFR-001: Remote Sensing in Urban Forestry

### Located fact

- Intake key: `li_remote-sensing-urban-forestry_2019`; evidence grade: `G1-R`.
- The review classifies 63 empirical studies by multi-source, multi-temporal, and multi-scale inputs. Optical imagery and LiDAR can contribute complementary spectral and structural information, while multi-source use adds fusion, co-registration, cost, resolution, and acquisition-interval constraints.
- The reviewed relationship between urban forests and ecosystem services varies with spatial scale; the authors caution against ignoring scale effects when informing land-use policy or estimating services.

### Boundary

- This is a review of urban-forestry remote sensing, not a validated universal processing chain. Its tables show task-specific strengths and limitations rather than one best sensor or scale.
- Official source: https://doi.org/10.3390/rs11101144

## S-UFR-002: Urban-vegetation ecosystem-service methods

### Located fact

- Intake key: `garcia-pardo_remote-sensing-assessment_2022`; evidence grade: `G1-R`.
- The review identifies three method-selection factors: intended approach, geographical scale, and available image resolution. It lists analysis/collection, atmospheric-radiometric-topographic-geometric correction, shadow or urban-contamination removal, orthorectification/georeferencing, QA/QC, and result cross-checking as recurring processes.
- Remote sensing alone does not exhaust ecosystem-service assessment; the authors call for ground monitoring and a transdisciplinary framework involving planning, vegetation, and other relevant specialists.

### Boundary

- The paper synthesizes heterogeneous studies rather than prescribing a single method. Its decision guidance is conditional on site, available data, ecosystem-service target, and urban context.
- Official source: https://doi.org/10.1016/j.ufug.2022.127636

## S-UFR-003: Object-based urban tree-species classification

### Located fact

- Intake key: `zhang_object-based-tree-species_2016`; evidence grade: `G1-P`.
- The primary workflow uses LiDAR crown delineation, hyperspectral value extraction and dimensionality reduction, supervised classification, and accuracy assessment. It therefore demonstrates a multi-stage dependency rather than a single image-to-label operation.
- Results depend on spatial resolution, registration, overlapping crowns, sample count, data dimensionality, classifiers, study sites, and the seven selected species.

### Boundary

- The reported accuracy is not a cross-city benchmark. The authors explicitly caution against direct comparison with studies using different sites, species, sensor densities, or sample sizes and call for further testing on other urban stands.
- Official source: https://doi.org/10.3390/f7060122

## S-UFR-004: Urban-forest ecosystem-service indicator framework

### Located fact

- Intake key: `dobbs_framework_2011`; evidence grade: `G1-P`.
- The Gainesville study combines field tree and soil measurements, a functional model, remote-sensing-accessible structure, and literature to build ecosystem-service, goods, and disservice indicators. Land use and time since urbanization affected several indicators.
- The interpretation of service and disservice depends on human preferences plus socio-political and biophysical context. The authors require site-specific species, climate, and social parameters and local rescaling for application elsewhere.

### Boundary

- Selected indicators depend on available data and do not represent the full set of urban-forest services. A canopy or structure map cannot, by itself, determine social value, disservice priority, or policy relevance.
- Official source: https://doi.org/10.1016/j.landurbplan.2010.11.004

## Decision synthesis

| Dependency or boundary | Direct source | What must remain conditional |
| --- | --- | --- |
| multi-source, multi-temporal, multi-scale inputs | Li et al. 2019 | sensor complementarity, fusion, cost, alignment, temporal quality, scale effects |
| purpose-scale-resolution method choice and processing obligations | García-Pardo et al. 2022 | correction, contamination, registration, QA/QC, ground and disciplinary interpretation |
| staged multi-sensor classification workflow | Zhang et al. 2016 | site, species, sample, spatial resolution, crown overlap, classifier validity |
| ecological-service and governance interpretation | Dobbs et al. 2011 | local species/climate, data availability, user preferences, social and policy context |

The four-source stop condition is met. `UFR-C5` remains `needs_review`: the packet supports a bounded description of domain complexity, but does not establish a universal workflow or any performance gain from an Agent, knowledge representation, or automated planning mechanism.
