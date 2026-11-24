# PLATEAU GitHub Use Cases — i-UR ADE (`uro:`) Attribute Usage Analysis

**Prepared:** 2026-11-24  
**Scope:** Six Project PLATEAU repositories listed below. For each repository, this report identifies which i-UR ADE attributes (CityGML attributes with the `uro:` prefix) are read, how they are used, how often they are referenced, and how critical they are to the use case.  
**Method:** shallow clone → static search for `uro:`, `BuildingDetailAttribute`, `RiverFloodingRiskAttribute`, `i-UR`/`iur`, canonical ADE field names, and code/config/visualization references → trace each hit to a read/join/write/symbol usage site → classify criticality.

## Repositories and analysed snapshots

| # | Repository | Use case (as stated in README) | Commit analysed |
|---|---|---|---|
| 1 | [Urban-structure-analysis](https://github.com/Project-PLATEAU/Urban-structure-analysis) | 都市構造評価ツール / urban structure evaluation (UC25-09) | `cb4435b` |
| 2 | [Fire-Spread-Simulator](https://github.com/Project-PLATEAU/Fire-Spread-Simulator) | 火災延焼シミュレーション / city fire spread simulation (UC25-08) | `ca2e7b6` |
| 3 | [PLATEAU-VIEW-5.0](https://github.com/Project-PLATEAU/PLATEAU-VIEW-5.0) | PLATEAU data platform: viewer, converter/flow engine, QC, API | `c3fe100` |
| 4 | [landscape-design-tool](https://github.com/Project-PLATEAU/landscape-design-tool) | 景観まちづくりDX / landscape and outdoor-advertising support (UC25-12) | `0111b2c` |
| 5 | [Fluid-dynamics-simulator](https://github.com/Project-PLATEAU/Fluid-dynamics-simulator) | 熱流体シミュレーション / heat-fluid simulation (UC25-03) | `b6586b9` |
| 6 | [Earthquake-simulation-tools](https://github.com/Project-PLATEAU/Earthquake-simulation-tools) | 建物振動シミュレーション / building vibration simulation | `91a11aa` |

---

## 0. How to read this report

### 0.1 What counts as a “`uro:` attribute”

Only attributes defined in the i-UR ADE namespace (`uro:`) are counted as `uro:` attributes. Standard CityGML attributes remain in the `bldg:`, `tran:`, `urf:`, `luse:` namespaces and are **not** i-UR ADE attributes, even when they carry similar information. This distinction matters in practice:

- `bldg:usage`, `bldg:yearOfConstruction`, `bldg:storeysAboveGround`, `bldg:storeysBelowGround`, `bldg:measuredHeight` are **standard** `bldg` attributes.
- `uro:totalFloorArea`, `uro:buildingFootprintArea`, `uro:buildingStructureType`, `uro:fireproofStructureType`, `uro:districtsAndZonesType`, `uro:surveyYear`, `uro:majorUsage`, `uro:detailedUsage`, risk-attribute fields (`uro:rank`, `uro:depth`, `uro:scale`, …) are **i-UR ADE** attributes.

Several repositories access attributes after conversion to GeoPackage/MVT, where the `uro:` prefix is stripped (e.g. `uro:totalFloorArea` → `total_floor_area`). Attribution in this report was cross-checked against the i-UR schema embedded in `PLATEAU-VIEW-5.0` (`server/citygml/schema_defs.json`), not inferred from field names alone.

### 0.2 Criticality legend

| Label | Meaning |
|---|---|
| **Analytical-critical** | Directly drives a computed result; removing it materially changes or breaks the output. |
| **Input-critical / Required** | The pipeline aborts, or the layer/attribute is structurally required for the use case to run. |
| **Fallback / Moderate** | Used when a primary attribute is absent/unknown, or refines accuracy but has a safe default. |
| **Visualization-only** | Used only for symbology, styling, labelling, or UI display. |
| **Joined-but-unused / Dead** | Loaded, joined, or exposed but never consumed by a calculation or visualization. |
| **Structural** | Join key or table-presence requirement; carries no semantic value itself. |

### 0.3 Frequency convention

“Frequency” is the number of **static references** in the repository (code, config, templates), not runtime frequency. A single consumed attribute can have few references but high criticality; a coloring rule can have hundreds of references but low criticality.

---

## 1. Cross-repository summary

| Repository | `uro:` classes actually used | Distinct `uro:` attributes consumed | Most important attributes | Overall verdict |
|---|---|---|---|---|
| **Urban-structure-analysis** | `BuildingDetailAttribute` (required layer), `RiverFloodingRiskAttribute` (optional) | **1 consumed** (`uro:totalFloorArea`) + 2 flood fields joined but unused | `uro:totalFloorArea` | Light ADE use. Most building logic relies on standard `bldg:` attributes. Flood-risk table is dead data. |
| **Fire-Spread-Simulator** | `BuildingDetailAttribute` | **5** | `uro:fireproofStructureType`, `uro:buildingStructureType` | Tight, core ADE dependency with explicit fallback chains. |
| **PLATEAU-VIEW-5.0** | 11 ADE attribute classes | **190 distinct flattened specs** + schema-wide coverage | `BuildingDetailAttribute`, `BuildingIDAttribute`, `DataQualityAttribute`, five risk-attribute classes | Platform/infrastructure, not a single use case. Broad, schema-complete support. |
| **landscape-design-tool** | — | **0** | — | Geometry/visualization only; one standard `bldg:measuredHeight` read. |
| **Fluid-dynamics-simulator** | — | **0** | — | Geometry (OBJ/STL) only; no CityGML/ADE parsing in repo. |
| **Earthquake-simulation-tools** | — | **0 directly** | — | Consumes preprocessed MVT properties (`bui_floor`, `_NAME*`); no i-UR parsing in repo. |

**Headline:** only 3 of 6 repositories use i-UR ADE attributes. Adoption is concentrated in building detail (`totalFloorArea`, structure/fireproof type, footprint, zoning) and — only in PLATEAU-VIEW — in data-quality and disaster-risk attributes. Three repositories are geometry-only or consume preprocessed derivatives.

---

## 2. Per-repository analysis

### 2.1 Urban-structure-analysis (都市構造評価ツール)

**Purpose.** A QGIS plugin that ingests PLATEAU building models and open data, computes urban-structure indicators (population, residential induction, public transport, urban function, disaster prevention, land use, fiscal/financial), visualizes them, and exports CSV.

**`uro:` input path.** `algorithms/utils/data_loader.py` loads a GeoPackage produced by the PLATEAU GIS Converter and touches exactly two ADE tables:

1. `uro:BuildingDetailAttribute` — **mandatory**; the load aborts if the layer is absent (`data_loader.py:76-86`). It is left-joined to `bldg:Building` on `detail.parentId = building.id` (`data_loader.py:181-198`). All detail fields are copied onto the building layer and snake-cased.
2. `uro:RiverFloodingRiskAttribute` — **optional**; if absent, the plugin logs a warning and continues (`data_loader.py:101-123`). It is joined on `risk.parentId = building.id`; `scale` splits L1/L2, then the maximum `depth` per building becomes `flood_depth_l1` / `flood_depth_l2` (`data_loader.py:215-323`).

#### `uro:` attributes: usage, frequency, criticality

| i-UR table | Attribute | How it is used | Evidence | Frequency | Criticality |
|---|---|---|---|---|---|
| `uro:BuildingDetailAttribute` | `uro:totalFloorArea` → `total_floor_area` | Living-area weighting for distributing mesh population to individual buildings; buildings below 10 m² are skipped; unknown/`-9999` triggers equal-split fallback | `data_loader.py:76-86, 181-198`; `building_data_assigner.py:156-174, 519-540` | 6 code references | **Analytical-critical** |
| `uro:BuildingDetailAttribute` | All other detail fields (e.g. `uro:buildingStructureType`, `uro:fireproofStructureType`, `uro:districtsAndZonesType`, `uro:buildingHeight`, `uro:surveyYear`, `uro:vacancy`, …) | Joined wholesale onto the building layer and exposed in the output GeoPackage, but **no metric or symbology reads them** | `data_loader.py:181-198`; no downstream reads found | 0 consumers | **Joined-but-unused** (exposed) |
| `uro:RiverFloodingRiskAttribute` | `uro:depth` | Maximum depth per building is written to `flood_depth_l1` / `flood_depth_l2` | `data_loader.py:228-274` | join/write only | **Joined-but-unused / Dead** |
| `uro:RiverFloodingRiskAttribute` | `uro:scale` | Classifies `L1`/`計画規模` vs `L2`/`想定最大規模` during the join | `data_loader.py:279-298` | 2 references | **Joined-but-unused / Dead** |
| (structural) | `parentId` (and building `id`) | Join keys between ADE tables and `bldg:Building` | `data_loader.py:181-198, 228-262` | — | **Structural / Required** |

**Key finding (correction to a naive grep).** The fields that drive this tool’s population logic are mostly **standard `bldg` attributes**, not `uro:` attributes:

| Standard attribute | Use | Evidence | Criticality |
|---|---|---|---|
| `bldg:usage` | Residential building classification (`住宅`, `共同住宅`, `店舗等併用住宅`, …); `不明` fallback; **480** map-coloring rule references | `building_data_assigner.py:143-152`; `config/LayersColoringConfig.xml` | Analytical-critical (+ Visualization-only) |
| `bldg:storeysAboveGround` | Living-area ratio; `9999` → 1 | `building_data_assigner.py:522-538` | Moderate |
| `bldg:storeysBelowGround` | Living-area ratio; `9999` → 0 | `building_data_assigner.py:527-538` | Moderate |
| `bldg:yearOfConstruction` | Age-based map coloring only (pre/post-2015 rules); no metric reads it | `config/LayersColoringConfig.xml` (183 references) | Visualization-only |

These names (`usage`, `storeys_*`, `year_of_construction`) share the field vocabulary of the shapefile import template (`algorithms/utils/dir_maker.py:109-113`), which is why a search for “usage” can wrongly suggest `uro:` usage. Cross-checking against the i-UR schema shows `uro:usage` exists only for `uro:ConstructionInstallation` / `uro:OtherConstruction` / port facilities, `uro:storeysAboveGround`/`BelowGround` do not exist, and `uro:yearOfConstruction` exists only under `uro:IfcPsetBuildingCommon` — none of which this plugin reads.

**Disaster-prevention nuance.** The “flood-risk high-area population share” metrics do **not** use `uro:RiverFloodingRiskAttribute`. They use external hazard-area Shapefiles (`A31b_101`) converted by `area_data_generator.py:2018+` and consumed by `disaster_prevention_metric_calculator.py:42-55, 320-400`. The ADE flood table is therefore loaded and exposed but analytically dead.

---

### 2.2 Fire-Spread-Simulator (火災延焼シミュレーション)

**Purpose.** A Windows GUI tool that converts PLATEAU CityGML into simulation input files for the NILIM/BRII city fire-spread engine, and provides a condition-setting support tool. Buildings are simulated one by one under wind and ignition conditions.

**`uro:` input path.** The mapping is **configuration-driven** in `Src/SimulationSourceFileCreator/Resources/ElementAddSetting.xml`. The C# code reads each configured XPath and applies a fallback/補完 (completion) chain in `IntermediateCsvFileCreator.cs`. The production code does not hard-code `uro:` field names; it reads the XML paths.

#### `uro:` attributes: usage, frequency, criticality

| i-UR table | Attribute | How it is used | Evidence | Frequency | Criticality |
|---|---|---|---|---|---|
| `uro:BuildingDetailAttribute` | `uro:fireproofStructureType` | **Primary** fireproof classification: `1001` → type 1, `1002` → type 2; other/unknown values fall through to building structure, then floor area | `ElementAddSetting.xml:10`; `IntermediateCsvFileCreator.cs:124-171` | 1 config path + primary branch | **Analytical-critical** |
| `uro:BuildingDetailAttribute` | `uro:buildingStructureType` | (a) **secondary** fireproof classification when fireproof type is unknown (`601` wood, `602-606`, `610`); (b) **primary** structure classification for MOKU (`601` → 1, `602-610` → 2) | `ElementAddSetting.xml:11,17`; `IntermediateCsvFileCreator.cs:174-190, 242-285` | 2 config paths + two branches | **Analytical-critical** |
| `uro:BuildingDetailAttribute` | `uro:totalFloorArea` | Threshold test in the fireproof fallback: > 3000 m² → type 1; ≤ 3000 m² → selected default | `ElementAddSetting.xml:13`; `IntermediateCsvFileCreator.cs:133-208` | 1 config path + fallback branches | **Fallback / Moderate** |
| `uro:BuildingDetailAttribute` | `uro:buildingFootprintArea` | Final fallback when total floor area is unknown: `footprint × storeys > 3000 m²` → type 1 | `ElementAddSetting.xml:14`; `IntermediateCsvFileCreator.cs:137-224` | 1 config path + final fallback | **Fallback / Moderate** |
| `uro:BuildingDetailAttribute` | `uro:districtsAndZonesType` | Extracted as `ZONE` and written to `sim:districtsAndZonesCityFireSimulationType` (default `0` if absent) | `ElementAddSetting.xml:26,45`; `IntermediateCsvFileCreator.cs:91-95`; `ElementAddCityGmlFileCreator.cs:135-159` | 1 config path | **Analytical (secondary input)** |

**Non-`uro:` context (important for this repo).**

| Standard attribute | Use | Evidence |
|---|---|---|
| `bldg:storeysAboveGround` | Third-level fireproof fallback (≥ 4 storeys → type 1) | `ElementAddSetting.xml:12`; `IntermediateCsvFileCreator.cs:129-209` |
| `bldg:usage` | YOTO mapping to simulation usage code (`401`→1 … default `22`) | `ElementAddSetting.xml:20`; `IntermediateCsvFileCreator.cs:296-320` |
| `bldg:Building gml:id` | Building ID | `ElementAddSetting.xml:5` |
| `bldg:measuredHeight` | Removal of implausible storey data for LOD2 | `ElementAddCityGmlFileCreator.cs:175-205` |

**Notes.**
- `uro:buildingIDAttribute` / `uro:BuildingIDAttribute` appears only in unit-test fixtures (`Src/UnitTest/...`), not in production logic; production uses `bldg:Building gml:id` for the building ID.
- The `uro:` namespace declaration in the generated output is `https://www.geospatial.jp/iur/uro/3.2` (`ElementAddCityGmlFileCreator.cs:311-312`).
- Criticality is high because the fireproof/structure classification determines the fire-spread behaviour class of every building; the fallback chain exists precisely to cope with missing `uro:` values.

---

### 2.3 PLATEAU-VIEW-5.0 (PLATEAU data platform)

**Purpose.** A large platform rather than a single analytical use case. It includes a web viewer/CMS, a data-conversion “flow” engine (CityGML → 3D Tiles/MVT), data-quality-check processors, a Go citygml API, and a feature-inspector extension.

**Where `uro:` attributes are used.**

| Subsystem | Role of `uro:` attributes | Evidence |
|---|---|---|
| **Attribute flattener (Plateau 4)** | Defines which attributes are flattened into tiles. `flatten_attributes.json` contains **190 distinct `uro:` attribute specs** across **11 attribute classes** for 148 feature types. | `flow/engine/runtime/action-plateau-processor/src/plateau4/attribute_flattener/flatten_attributes.json`; `constants.rs` |
| **Attribute flattener (Plateau 3)** | Older hard-coded mapping of ~38 building-related `uro:` attribute pairs plus disaster-risk extraction. | `.../plateau3/attribute_flattener.rs:30-81, 109-241` |
| **Building usage QC** | Validates the i-UR building-usage hierarchy and city codes. | `.../plateau4/building_usage_attribute_validator.rs:20-30, 150-270`; Plateau 3 equivalent at `.../plateau3/building_usage_attribute_validator.rs:26-31` |
| **Missing-attribute detector** | Detects missing LOD geometry-source and public-survey quality attributes. | `.../plateau4/missing_attribute_detector.rs:846-867, 1009-1052` |
| **CityGML API (Go)** | Schema-driven extraction of any attribute defined in `schema_defs.json` (**4,874 `uro:` references**), so the API is schema-complete. | `server/citygml/attributes.go`, `schema_defs.json`, `attributes_test.go` |
| **Feature inspector (TypeScript)** | Display-label map for the inspector: **85 `uro:` label entries** covering building, risk, indoor/IFC, construction, port, etc. | `extension/src/shared/plateau/featureInspector/parseAttributes.ts` |

#### `uro:` attribute classes and representative fields

| i-UR class | Representative attributes | How used | Frequency | Criticality |
|---|---|---|---|---|
| `uro:BuildingDetailAttribute` | `totalFloorArea`, `buildingFootprintArea`, `buildingStructureType`, `fireproofStructureType`, `districtsAndZonesType`, `buildingHeight`, `eaveHeight`, `surveyYear`, `majorUsage`, `majorUsage2`, `detailedUsage`, `detailedUsage2`, `detailedUsage3`, `groundFloorUsage`, `secondFloorUsage`, `thirdFloorUsage`, `basementFirstUsage`, `basementSecondUsage`, `vacancy`, coverage/floor-area rates | Flattened into tiles (20 fields) and validated for usage hierarchy; `surveyYear` is required for usage QC | 20 flatten specs; ~11 usage-QC attributes | **Analytical / infrastructure-critical** |
| `uro:BuildingIDAttribute` | `buildingID`, `branchID`, `partID`, `prefecture`, `city` (+ `_code` variants) | Flattened; required by usage QC; city-code validation against a local-authority code list | 5 flatten specs + QC | **Structural / Required for QC** |
| `uro:DataQualityAttribute` / `uro:PublicSurveyDataQualityAttribute` | `geometrySrcDescLodN`, `thematicSrcDesc`, `srcScaleLodN`, `publicSurveySrcDescLodN` (+ codes) | Missing-attribute and LOD quality checks | ~6+ checks | **QC-critical** |
| Risk attributes: `RiverFlooding`, `Tsunami`, `HighTide`, `InlandFlooding`, `ReservoirFlooding` | `description`, `rank`, `rankOrg`, `scale`, `adminType`, `depth`, `duration` (+ codes) | Flattened to tiles; inspector labels (“浸水ランク”, “規模”, etc.) | 5 classes, 27 specs | **Display / analysis-critical** |
| `LandUseDetailAttribute` | `areaInHa`, `areaInSquareMeter`, `orgLandUse`, `ownerType`, `districtsAndZonesType`, rates, `surveyYear` | Flattened | 25 specs | Feature-critical |
| `LargeCustomerFacilityAttribute` | `class`, `name`, `capacity`, `totalFloorArea`, `inauguralDate`, `yearOpened`, `yearClosed`, `districtsAndZonesType`, … | Flattened | 12 specs | Feature-critical |
| `RealEstateIDAttribute` | `realEstateIDOfBuilding`, `matchingScore` | Flattened | 2 specs | Feature-specific |
| `RoadStructureAttribute`, `SquareUrbanPlanAttribute`, `StationSquareAttribute`, `TerminalAttribute`, `TrafficVolumeAttribute` | width/lane/section, project dates/areas, station/terminal attributes, traffic volumes | Flattened | ~90 specs | Feature-specific |
| (standard, not `uro:`) | `bldg:usage`, `bldg:yearOfConstruction`, `bldg:measuredHeight`, `bldg:storeysAboveGround`, `bldg:storeysBelowGround` | Also flattened, but these are standard `bldg` attributes | 5 specs | — |

**Criticality for PLATEAU-VIEW.** Because this repository is infrastructure, the “criticality” is platform-level: the flattener/QC/API must handle these attributes for the downstream viewer and quality checks to function. It is not a single analytical model whose result depends on one attribute. The most consequential building-level fields are the BuildingDetail, BuildingID, DataQuality, and risk-attribute sets.

---

### 2.4 landscape-design-tool (景観まちづくりDX v3.0)

**Purpose.** A Unity/PLATEAU SDK tool for landscape simulation, outdoor-advertising wall-area ratio calculation, regulation-range display, distance measurement, BIM import, and landscape-plan area editing.

**`uro:` usage: none.**

| Search | Result |
|---|---|
| `uro:` / `BuildingDetailAttribute` / `RiverFloodingRiskAttribute` in C#/JSON/Markdown | 0 relevant hits |
| ADE access | None. The only building attribute read is `bldg:measuredHeight` (`Runtime/VisualizeHeight/VisualizeHeight.cs:81`), used for height visualization. |
| Apparent false positives | The single `usage` hit is a code comment in `Plugins/TriangleNet/.../NewLocation.cs`; the `ADE` hits are hexadecimal colour strings. |

**Assessment.** The use case consumes PLATEAU geometry and standard building height only. No i-UR ADE attribute is used. It would not be affected by missing `uro:` tables.

---

### 2.5 Fluid-dynamics-simulator (熱流体シミュレーション)

**Purpose.** A Laravel web application for large-scale heat/fluid simulation over 3D city models, using OpenFOAM, with vegetation models and Cesium/Leaflet visualization.

**`uro:` usage: none.**

| Search | Result |
|---|---|
| `uro:` / `buildingStructureType` / `fireproof` / `yearOfConstruction` / `storeysAboveGround` / `totalFloorArea` / `districtsAndZones` | 0 hits |
| CityGML handling | CityGML upload has been removed (`src/srcWeb/app/Http/Controllers/CityModelController.php:125-126`: “CityGmlファイルアップロード機能がなくなった…”). Models are converted externally (FME) to OBJ/STL and uploaded as geometry. |
| Attribute use | Only simulation-model metadata (`SimulationModelService.php`, `CityModelService.php`), not CityGML/ADE attributes. |

**Assessment.** No i-UR ADE attribute is used. The simulation is geometry-driven (OBJ/STL), so the use case does not depend on `uro:` data.

---

### 2.6 Earthquake-simulation-tools (建物振動シミュレーション)

**Purpose.** A SvelteKit/AWS web application for building-vibration simulation: job reservation, result download, dashboard visualization (damage, road blockage, temporary housing), and map display.

**`uro:` usage: none directly.**

| Search | Result |
|---|---|
| `uro:` / `CityGML` / `buildingStructureType` / `fireproof` / `yearOfConstruction` / `storeysAboveGround` / `totalFloorArea` / `districtsAndZones` | 0 hits (lock-file hits are package-name false positives) |
| Attribute use | Consumes **preprocessed MVT/GeoJSON properties**: `bui_floor` (storeys), `_NAME00000/_NAME00001/_NAME00002/_NAME00009` (structure names), `max_drift`, etc. See `apps/viewer/src/lib/utils/DeckLayerFactory.ts:86-91, 203-217` and `packages/shared/src/constants/buildingDamageThresholds.ts:150-190`. |
| Provenance | The conversion from CityGML/i-UR to `bui_*`/`_NAME*` MVT properties is **outside this repository**; the repo contains no `uro:` parser. |

**Assessment.** No i-UR ADE attribute is read by this repository. `bui_floor` and `_NAME*` may be derived from PLATEAU attributes upstream, but that mapping is not present here, so no `uro:` attribute can be attributed to this use case from the code alone.

---

## 3. Cross-repository attribute matrix

Legend: **●** consumed analytically / in pipeline · **◐** joined or exposed but not consumed · **○** fallback or secondary use · **▽** visualization-only · **·** not present.

| i-UR attribute | Urban-structure | Fire-Spread | PLATEAU-VIEW | Landscape | Fluid | Earthquake |
|---|:---:|:---:|:---:|:---:|:---:|:---:|
| `uro:totalFloorArea` | ● | ○ | ● | · | · | · |
| `uro:buildingFootprintArea` | ◐ | ○ | ● | · | · | · |
| `uro:buildingStructureType` | ◐ | ● | ● | · | · | · |
| `uro:fireproofStructureType` | ◐ | ● | ● | · | · | · |
| `uro:districtsAndZonesType` | ◐ | ● | ● | · | · | · |
| `uro:buildingHeight`, `uro:eaveHeight` | ◐ | · | ● | · | · | · |
| `uro:surveyYear` | ◐ | · | ● | · | · | · |
| `uro:majorUsage*`, `uro:detailedUsage*`, floor usages | · | · | ● | · | · | · |
| `uro:BuildingIDAttribute` fields (`buildingID`, `branchID`, `partID`, `prefecture`, `city`) | · | · | ● | · | · | · |
| `uro:DataQualityAttribute` / `PublicSurveyDataQualityAttribute` fields | · | · | ● | · | · | · |
| Risk attributes: `rank`, `rankOrg`, `scale`, `depth`, `description`, `adminType`, `duration` | ◐ (depth/scale, dead) | · | ● | · | · | · |
| `uro:LandUseDetailAttribute` fields | · | · | ● | · | · | · |
| `uro:LargeCustomerFacilityAttribute` fields | · | · | ● | · | · | · |
| `uro:RealEstateIDAttribute` fields | · | · | ● | · | · | · |
| `uro:RoadStructureAttribute` / `TrafficVolumeAttribute` fields | · | · | ● | · | · | · |
| `uro:SquareUrbanPlanAttribute` / `StationSquareAttribute` / `TerminalAttribute` fields | · | · | ● | · | · | · |
| *(non-`uro:`) `bldg:usage` | ● | ● | ● | · | · | · |
| *(non-`uro:`) `bldg:storeysAboveGround/BelowGround` | ● | ● | ● | · | · | · |
| *(non-`uro:`) `bldg:yearOfConstruction` | ▽ | · | ● | · | · | · |
| *(non-`uro:`) `bldg:measuredHeight` | · | ● | ● | ● | · | · |

---

## 4. Observations and patterns

1. **ADE adoption is selective, not universal.** Three of six repositories use no i-UR ADE attribute at all. Two are geometry-driven simulations (Fluid-dynamics: OBJ/STL; Earthquake: preprocessed MVT), and one is a geometry/visualization tool (landscape-design: Unity + `bldg:measuredHeight`).

2. **`uro:totalFloorArea` is the most cross-cutting ADE attribute.** It is the only `uro:` attribute analytically consumed by Urban-structure, a fallback input in Fire-Spread, and a flattened/feature attribute in PLATEAU-VIEW. Building structure/fireproof/footprint/zoning follow, used by two repos each.

3. **A naive `uro`/`usage` search over-attributes standard `bldg` data.** Urban-structure’s population logic leans heavily on `bldg:usage`, `bldg:storeysAboveGround/BelowGround`, and `bldg:yearOfConstruction`, none of which are `uro:` attributes. Reports that count these as i-UR ADE would substantially overstate ADE dependence.

4. **Urban-structure contains the largest volume of loaded-but-unused ADE data.** The entire `uro:RiverFloodingRiskAttribute` table (depth/scale → `flood_depth_l1/l2`) is joined onto buildings but never consumed by any metric or symbology; most `uro:BuildingDetailAttribute` fields are likewise only exposed in the output GeoPackage. The actual analytical ADE surface is one field (`totalFloorArea`).

5. **Fire-Spread-Simulator has the most tightly coupled ADE dependency.** Five `BuildingDetailAttribute` fields drive a four-level fireproof/structure fallback chain that determines each building’s fire-spread class. Missing values degrade to standard `bldg` data and geometric defaults, but the ADE fields are the preferred authoritative inputs.

6. **PLATEAU-VIEW-5.0 is infrastructure, not a use case.** Its 190 flattened `uro:` attribute specs, 4,874 schema references, 85 inspector labels, and dedicated QC validators make it schema-complete. Its criticality is platform-level; it supports many downstream use cases rather than computing one indicator.

7. **Risk attributes diverge by generation.** Urban-structure’s flood path uses `uro:depth`/`uro:scale` from `uro:RiverFloodingRiskAttribute`; Fire-Spread uses no risk attributes; PLATEAU-VIEW supports five separate risk classes (`RiverFlooding`, `Tsunami`, `HighTide`, `InlandFlooding`, `ReservoirFlooding`) with `rank`/`rankOrg`/`scale`/`depth`/`duration` and both Plateau 3 and Plateau 4 attribute naming (`uro:buildingDisasterRiskAttribute` vs `uro:BuildingRiverFloodingRiskAttribute`, etc.).

8. **Schema cross-checking is essential.** Because GeoPackage/MVT conversion strips the `uro:` prefix, field names alone are ambiguous. Cross-checking against `server/citygml/schema_defs.json` prevented misattributing `usage`, `storeys`, and `yearOfConstruction` to i-UR ADE.

---

## 5. Reproducibility appendix

### 5.1 Snapshots

| Repository | Commit |
|---|---|
| Urban-structure-analysis | `cb4435b` |
| Fire-Spread-Simulator | `ca2e7b6` |
| PLATEAU-VIEW-5.0 | `c3fe100` |
| landscape-design-tool | `0111b2c` |
| Fluid-dynamics-simulator | `b6586b9` |
| Earthquake-simulation-tools | `91a11aa` |

### 5.2 Representative search commands

```bash
# Any i-UR / ADE reference in the repository
grep -rIn --exclude-dir=.git --exclude-dir=node_modules \
  -E "uro:|BuildingDetailAttribute|RiverFloodingRiskAttribute|i-UR|iur" <repo>

# Canonical building ADE attributes
grep -rIoh -E "uro:(totalFloorArea|buildingFootprintArea|buildingStructureType|fireproofStructureType|districtsAndZonesType|buildingHeight|surveyYear|majorUsage|detailedUsage|rank|depth|scale)" <repo>

# Distinguish standard bldg attributes from ADE
grep -rIn -E "bldg:(usage|yearOfConstruction|storeysAboveGround|storeysBelowGround|measuredHeight)" <repo>
```

### 5.3 Key files by repository

| Repository | Primary evidence files |
|---|---|
| Urban-structure-analysis | `algorithms/utils/data_loader.py`; `algorithms/utils/building_data_assigner.py`; `config/LayersColoringConfig.xml`; `algorithms/utils/dir_maker.py` |
| Fire-Spread-Simulator | `Src/SimulationSourceFileCreator/Resources/ElementAddSetting.xml`; `Src/SimulationSourceFileCreator/Controller/IntermediateCsvFileCreator.cs`; `.../ElementAddCityGmlFileCreator.cs` |
| PLATEAU-VIEW-5.0 | `flow/engine/runtime/action-plateau-processor/src/plateau4/attribute_flattener/flatten_attributes.json`; `.../plateau4/building_usage_attribute_validator.rs`; `.../plateau4/missing_attribute_detector.rs`; `.../plateau3/attribute_flattener.rs`; `server/citygml/attributes.go`; `server/citygml/schema_defs.json`; `extension/src/shared/plateau/featureInspector/parseAttributes.ts` |
| landscape-design-tool | `Runtime/VisualizeHeight/VisualizeHeight.cs`; no `uro:` code |
| Fluid-dynamics-simulator | `src/srcWeb/app/Http/Controllers/CityModelController.php`; README (FME conversion); no `uro:` code |
| Earthquake-simulation-tools | `apps/viewer/src/lib/utils/DeckLayerFactory.ts`; `packages/shared/src/constants/buildingDamageThresholds.ts`; no `uro:` code |

### 5.4 Caveats

- Static analysis only; runtime behaviour for edge cases (null geometry, malformed CityGML, alternate i-UR versions) was not executed.
- “Frequency” counts are static reference counts and are sensitive to templates, tests, generated/bundled files, and duplicate configurations; they are indicative, not precise runtime metrics.
- PLATEAU-VIEW-5.0 is a monorepo with generated bundles and large schema/test fixtures; fixture GML/XSD files were excluded from the counts.
- Repository default branches and commit contents are as of the dates shown above.
