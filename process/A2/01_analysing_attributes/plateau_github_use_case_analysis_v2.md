# PLATEAU GitHub Use Cases — i-UR ADE (`uro:`) Attribute Usage Analysis (v2)

**Prepared:** 2026-11-24  
**Scope:** Thirteen Project PLATEAU repositories. For each repository this report identifies which i-UR ADE attributes (CityGML attributes in the `uro:` namespace, i.e. the i-UR **Urban Object Module**) are read, written, or consumed, how they are used, how often they are referenced, and how critical they are to the use case.  
**Method:** shallow clone → exhaustive static search for `uro:`, `uro_`, `BuildingDetailAttribute`, `RiverFloodingRiskAttribute`, `i-UR`/`iur`, canonical ADE field names, XPath/JSON keys, schema/XSD definitions, and prefix-stripped/preprocessed column names → trace each hit to a read/join/write/validation/flatten/display site → cross-check against the i-UR schema → classify criticality.

## Repositories and analysed snapshots

| # | Repository | Use case (as stated in README) | Commit analysed |
|---|---|---|---|
| 1 | [Urban-structure-analysis](https://github.com/Project-PLATEAU/Urban-structure-analysis) | 都市構造評価ツール / urban structure evaluation (UC25-09) | `cb4435b` |
| 2 | [Fire-Spread-Simulator](https://github.com/Project-PLATEAU/Fire-Spread-Simulator) | 火災延焼シミュレーション / city fire spread simulation (UC25-08) | `ca2e7b6` |
| 3 | [PLATEAU-VIEW-5.0](https://github.com/Project-PLATEAU/PLATEAU-VIEW-5.0) | PLATEAU data platform: viewer, converter/flow engine, QC, API | `c3fe100` |
| 4 | [landscape-design-tool](https://github.com/Project-PLATEAU/landscape-design-tool) | 景観まちづくりDX / landscape and outdoor-advertising support (UC25-12) | `0111b2c` |
| 5 | [Fluid-dynamics-simulator](https://github.com/Project-PLATEAU/Fluid-dynamics-simulator) | 熱流体シミュレーション / heat-fluid simulation (UC25-03) | `b6586b9` |
| 6 | [Earthquake-simulation-tools](https://github.com/Project-PLATEAU/Earthquake-simulation-tools) | 建物振動シミュレーション / building vibration simulation | `91a11aa` |
| 7 | [snow-removal-prioritization-system](https://github.com/Project-PLATEAU/snow-removal-prioritization-system) | 除雪優先度算出システム / snow-removal prioritisation (UC25-01) | `b0a0208` |
| 8 | [SAR-Hazard-Estimator](https://github.com/Project-PLATEAU/SAR-Hazard-Estimator) | SAR衛星を用いた建物被害判定 / SAR-based building damage estimation | `6e87f64` |
| 9 | [SolarPotential](https://github.com/Project-PLATEAU/SolarPotential) | 太陽光発電ポテンシャル推計 / solar potential and suitability | `a175dd3` |
| 10 | [Disaster-Prevention-Planner](https://github.com/Project-PLATEAU/Disaster-Prevention-Planner) | 地区防災計画作成支援 / district disaster-prevention planning | `a514568` |
| 11 | [Building-collapse-detector](https://github.com/Project-PLATEAU/Building-collapse-detector) | 家屋倒壊判定 / building collapse detection for debris flow | `9fc799b` |
| 12 | [RealEstateID-matching-system](https://github.com/Project-PLATEAU/RealEstateID-matching-system) | 不動産ID付与 / real-estate ID matching | `ae08e47` |
| 13 | [Disaster-damage-simulator](https://github.com/Project-PLATEAU/Disaster-damage-simulator) | 水害・土砂災害の家屋被害額予測 / disaster damage valuation | `2f712fd` |

---

## 0. How to read this report

### 0.1 What counts as a “`uro:` attribute”

Only attributes defined in the i-UR ADE namespace (`uro:`) are counted as i-UR ADE attributes. Standard CityGML attributes remain in the `bldg:`, `tran:`, `urf:`, `luse:` namespaces and are **not** i-UR ADE attributes, even when they carry similar information.

- `bldg:usage`, `bldg:yearOfConstruction`, `bldg:storeysAboveGround`, `bldg:storeysBelowGround`, `bldg:measuredHeight` are **standard `bldg` attributes**.
- `uro:totalFloorArea`, `uro:buildingFootprintArea`, `uro:buildingStructureType`, `uro:fireproofStructureType`, `uro:districtsAndZonesType`, `uro:surveyYear`, `uro:majorUsage`, `uro:detailedUsage`, risk-attribute fields (`uro:rank`, `uro:depth`, `uro:scale`, …) are **i-UR ADE attributes**.

Several repositories access attributes after conversion to GeoPackage/MVT/ArcGIS, where the `uro:` prefix is stripped or transformed (`uro:totalFloorArea` → `total_floor_area`, `uro_BuildingDetailAttribute_buildingStructureType`, etc.). Attribution was cross-checked against the i-UR schema embedded in `PLATEAU-VIEW-5.0` (`server/citygml/schema_defs.json`, 156 `uro` types, 1,654 `uro`-prefixed properties), not inferred from field names alone.

### 0.2 Criticality legend

| Label | Meaning |
|---|---|
| **Analytical-critical** | Directly drives a computed result or output; removing it materially changes or breaks the output. |
| **Input-critical / Required** | The pipeline aborts, or the layer/attribute is structurally required for the use case to run. |
| **Fallback / Moderate** | Used when a primary attribute is absent/unknown, or refines accuracy but has a safe default. |
| **Visualization-only** | Used only for symbology, styling, labelling, or UI display. |
| **Joined-but-unused / Dead** | Loaded, joined, parsed, or exposed but never consumed by a calculation or visualization (includes defined-but-never-called parser functions). |
| **Indirect / Preprocessed** | Consumed from a flattened/preprocessed derivative (GeoPackage/MVT/ArcGIS) rather than parsed directly from CityGML in the repository. |
| **Structural** | Join key or table-presence requirement; carries no semantic value itself. |

### 0.3 Frequency convention

“Frequency” is the number of **static references** in the repository (code, config, templates), not runtime frequency. A single consumed attribute can have few references but high criticality; a coloring rule can have hundreds of references but low criticality. Test fixtures, generated bundles, and embedded schema files are excluded from usage counts unless explicitly noted.

### 0.4 What is new in v2

- Seven additional repositories (snow-removal, SAR, SolarPotential, Disaster-Prevention-Planner, Building-collapse-detector, RealEstateID, Disaster-damage-simulator).
- The **full i-UR Urban Object Module catalog** (`uro` feature types, complex types, and properties) is included as Appendix A, and every repository was checked against it.
- Indirect/preprocessed `uro` usage is now counted and explicitly flagged.
- The six v1 repositories were re-scanned with the same exhaustive method; this added findings that v1 missed (notably the bundled `plateaupy` parser in Fire-Spread-Simulator).

---

## 1. Cross-repository summary

| Repository | `uro:` classes actually used | Distinct `uro:` attributes consumed | Most important attributes | Overall verdict |
|---|---|---|---|---|
| **Urban-structure-analysis** | `BuildingDetailAttribute` (required layer), `RiverFloodingRiskAttribute` (optional) | **1 consumed** (`uro:totalFloorArea`) + 2 flood fields joined but unused | `uro:totalFloorArea` | Light ADE use. Population logic relies mostly on standard `bldg:` attributes. Flood-risk table is dead data. |
| **Fire-Spread-Simulator** | `BuildingDetailAttribute`; generic `BuildingDetails` / `KeyValuePair` in bundled `plateaupy` | **5** (plus generic containers) | `uro:fireproofStructureType`, `uro:buildingStructureType` | Tight, core ADE dependency with explicit fallback chains. |
| **PLATEAU-VIEW-5.0** | 11 ADE attribute classes | **190 distinct flattened specs** + schema-wide coverage | `BuildingDetailAttribute`, `BuildingIDAttribute`, `DataQualityAttribute`, five flood/tsunami risk classes (+ landslide in Plateau 3) | Platform/infrastructure, not a single use case. Broad, schema-complete support. |
| **landscape-design-tool** | — | **0** | — | Geometry/visualization only; one standard `bldg:measuredHeight` read. |
| **Fluid-dynamics-simulator** | — | **0** | — | Geometry (OBJ/STL) only; no CityGML/ADE parsing in repo. |
| **Earthquake-simulation-tools** | — | **0 directly** | — | Consumes preprocessed MVT properties (`bui_floor`, `_NAME*`); no i-UR parsing in repo. |
| **snow-removal-prioritization-system** | — | **0** | — | Front-end only; PLATEAU data preparation lives in a companion repository. |
| **SAR-Hazard-Estimator** | — | **0** | — | Integrates SAR-derived CSV results; no CityGML/ADE parsing. |
| **SolarPotential** | `BuildingDetailAttribute`, `BuildingIDAttribute`, `KeyValuePair`; risk attributes are dead | **3 active** + 4 dead | `uro:buildingStructureType`, `uro:buildingID`, `uro:extendedAttribute/KeyValuePair` | Structure and ID are core; disaster-risk parsers are defined but never called. |
| **Disaster-Prevention-Planner** | — | **0** | — | Web planning app; building data referenced by ID only. |
| **Building-collapse-detector** | — | **0 directly** | — | Consumes preprocessed building structure/year/storeys via CSV/Shapefile; i-UR provenance outside repo. |
| **RealEstateID-matching-system** | `BuildingDetailAttribute` (input), `RealEstateIDAttribute` (output) | **2 read + 6 written** | `uro:buildingStructureType`, `uro:buildingFootprintArea`, `uro:RealEstateIDAttribute/*` | The only repository that writes i-UR ADE output. |
| **Disaster-damage-simulator** | `BuildingDetailAttribute`, `BuildingIDAttribute` (indirect) | **2 consumed** + 1 exposed | `uro:buildingStructureType`, `uro:totalFloorArea` | Indirect but analytically important for damage valuation. |

**Headline:** 6 of 13 repositories use `uro` ADE attributes (Urban-structure, Fire-Spread, PLATEAU-VIEW, SolarPotential, RealEstateID, Disaster-damage). Seven are geometry-only, consume preprocessed derivatives without explicit ADE provenance, or are front-end/planning tools. Adoption is concentrated in building detail (`totalFloorArea`, structure/fireproof type, footprint, zoning) and, in PLATEAU-VIEW, in data-quality and disaster-risk attributes.

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

**`uro:` input path.** The main mapping is **configuration-driven** in `Src/SimulationSourceFileCreator/Resources/ElementAddSetting.xml`. The C# code reads each configured XPath and applies a fallback/補完 (completion) chain in `IntermediateCsvFileCreator.cs`. A bundled external Python tool (`Src/ExternalTools/Src_GeneFile/plateaupy/plbldg.py`) additionally parses generic ADE blocks.

#### `uro:` attributes: usage, frequency, criticality

| i-UR table | Attribute | How it is used | Evidence | Frequency | Criticality |
|---|---|---|---|---|---|
| `uro:BuildingDetailAttribute` | `uro:fireproofStructureType` | **Primary** fireproof classification: `1001` → type 1, `1002` → type 2; other/unknown values fall through to building structure, then floor area | `ElementAddSetting.xml:10`; `IntermediateCsvFileCreator.cs:124-171` | 1 config path + primary branch | **Analytical-critical** |
| `uro:BuildingDetailAttribute` | `uro:buildingStructureType` | (a) **secondary** fireproof classification when fireproof type is unknown (`601` wood, `602-606`, `610`); (b) **primary** structure classification for MOKU (`601` → 1, `602-610` → 2) | `ElementAddSetting.xml:11,17`; `IntermediateCsvFileCreator.cs:174-190, 242-285` | 2 config paths + two branches | **Analytical-critical** |
| `uro:BuildingDetailAttribute` | `uro:totalFloorArea` | Threshold test in the fireproof fallback: > 3000 m² → type 1; ≤ 3000 m² → selected default | `ElementAddSetting.xml:13`; `IntermediateCsvFileCreator.cs:133-208` | 1 config path + fallback branches | **Fallback / Moderate** |
| `uro:BuildingDetailAttribute` | `uro:buildingFootprintArea` | Final fallback when total floor area is unknown: `footprint × storeys > 3000 m²` → type 1 | `ElementAddSetting.xml:14`; `IntermediateCsvFileCreator.cs:137-224` | 1 config path + final fallback | **Fallback / Moderate** |
| `uro:BuildingDetailAttribute` | `uro:districtsAndZonesType` | Extracted as `ZONE` and written to `sim:districtsAndZonesCityFireSimulationType` (default `0` if absent) | `ElementAddSetting.xml:26,45`; `IntermediateCsvFileCreator.cs:91-95`; `ElementAddCityGmlFileCreator.cs:135-159` | 1 config path | **Analytical (secondary input)** |
| `uro:BuildingDetails` (generic container) | child elements of `uro:buildingDetails/uro:BuildingDetails` | Parsed generically into `b.buildingDetails[tag]` by the bundled `plateaupy` library; the fire-simulation conversion does **not** consume this dictionary | `Src/ExternalTools/Src_GeneFile/plateaupy/plbldg.py:174-179`; no downstream use in `plateau_conv.py` | 1 parser | **Joined-but-unused / Exposed** |
| `uro:KeyValuePair` (generic extension) | `uro:key`, `uro:codeValue` within `uro:extendedAttribute` | Parsed generically into `b.extendedAttribute`; not consumed by the fire-simulation conversion | `Src/ExternalTools/Src_GeneFile/plateaupy/plbldg.py:180-183`; no downstream use | 1 parser | **Joined-but-unused / Exposed** |

**Non-`uro:` context (important for this repo).**

| Standard attribute | Use | Evidence |
|---|---|---|
| `bldg:storeysAboveGround` | Third-level fireproof fallback (≥ 4 storeys → type 1); also used by `plateaupy` for floor height | `ElementAddSetting.xml:12`; `IntermediateCsvFileCreator.cs:129-209`; `plbldg.py:158-163` |
| `bldg:usage` | YOTO mapping to simulation usage code (`401`→1 … default `22`) | `ElementAddSetting.xml:20`; `IntermediateCsvFileCreator.cs:296-320` |
| `bldg:yearOfConstruction` | Consumed by the bundled `plateaupy` conversion (`smfrbld.cnstrct_yr`) | `plbldg.py:194-195`; `plateau_conv.py:732` |
| `bldg:measuredHeight` | Height used by the conversion; removal of implausible storey data for LOD2 | `ElementAddSetting.xml`; `ElementAddCityGmlFileCreator.cs:175-205`; `plateau_conv.py:626-659` |
| `bldg:Building gml:id` | Building ID | `ElementAddSetting.xml:5` |

**Notes.**
- `uro:buildingIDAttribute` / `uro:BuildingIDAttribute` appears only in unit-test fixtures (`Src/UnitTest/...`), not in production logic; production uses `bldg:Building gml:id` for the building ID.
- The `uro:` namespace declaration in the generated output is `https://www.geospatial.jp/iur/uro/3.2` (`ElementAddCityGmlFileCreator.cs:311-312`).
- Criticality is high because the fireproof/structure classification determines the fire-spread behaviour class of every building; the fallback chain exists precisely to cope with missing `uro:` values.

---

### 2.3 PLATEAU-VIEW-5.0 (PLATEAU data platform)

**Purpose.** A large platform rather than a single analytical use case. It includes a web viewer/CMS, a data-conversion “flow” engine (CityGML → 3D Tiles/MVT), data-quality-check processors, a Go CityGML API, and a feature-inspector extension.

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
| Risk attributes: `RiverFlooding`, `Tsunami`, `HighTide`, `InlandFlooding`, `ReservoirFlooding` (plus `LandSlideRiskAttribute` in the Plateau 3 flattener) | `description`, `rank`, `rankOrg`, `scale`, `adminType`, `depth`, `duration` (+ codes); landslide uses `areaType`, `description` | Flattened to tiles; inspector labels (“浸水ランク”, “規模”, etc.) | 5 classes / 27 specs (+ landslide in Plateau 3) | **Display / analysis-critical** |
| `uro:LandUseDetailAttribute` | `areaInHa`, `areaInSquareMeter`, `orgLandUse`, `ownerType`, `districtsAndZonesType`, rates, `surveyYear` | Flattened | 25 specs | Feature-critical |
| `uro:LargeCustomerFacilityAttribute` | `class`, `name`, `capacity`, `totalFloorArea`, `inauguralDate`, `yearOpened`, `yearClosed`, `districtsAndZonesType`, … | Flattened | 12 specs | Feature-critical |
| `uro:RealEstateIDAttribute` | `realEstateIDOfBuilding`, `matchingScore` | Flattened | 2 specs | Feature-specific |
| `uro:RoadStructureAttribute`, `uro:SquareUrbanPlanAttribute`, `uro:StationSquareAttribute`, `uro:TerminalAttribute`, `uro:TrafficVolumeAttribute` | width/lane/section, project dates/areas, station/terminal attributes, traffic volumes | Flattened | ~90 specs | Feature-specific |
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

**Assessment.** No i-UR ADE attribute is read by this repository. `bui_floor` and `_NAME*` may be derived from PLATEAU attributes upstream, but that mapping is not present here, so no `uro:` attribute can be attributed to this use case from the code alone. Flagged as **indirect / external provenance**, not counted.

---

### 2.7 snow-removal-prioritization-system (除雪優先度算出システム)

**Purpose.** The front-end (PHP/JavaScript/OpenLayers) of a system that estimates per-building snow load and snow-removal priority from weather data and PLATEAU building shape/construction year.

**`uro:` usage: none.**

| Search | Result |
|---|---|
| `uro:` / `CityGML` / `bldg:` / `BuildingDetail` / `yearOfConstruction` / `storeys` | 0 relevant hits in this repository |
| Architecture | The README states the system is split into three repositories: this front-end, `snow-removal-prioritization-system-data` (data collection/calculation/creation), and `snow-removal-prioritization-system-api`. PLATEAU ingestion is in the **data** repository, not here. |
| Building data | The front-end consumes precomputed snow-load/priority records and building geometry; it references building IDs and display attributes but not `uro:` fields. |

**Assessment.** No i-UR ADE attribute is used in this repository. Any ADE dependence lives in the companion data repository, which is outside the analysed set.

---

### 2.8 SAR-Hazard-Estimator (SAR衛星を用いた建物被害判定)

**Purpose.** Integrates large-SAR and small-SAR building-damage CSV results into a single building-level damage estimate.

**`uro:` usage: none.**

| Search | Result |
|---|---|
| `uro:` / `CityGML` / `PLATEAU` attribute access | 0 hits |
| Input/output | Only `large_sat_analysis_result.csv`, `small_sat_analysis_results.csv`, and `integrated_damage_polygons.csv`; the join key is a building `fid`. |
| Code | `src/integrate_sar_analysis.py` uses pandas; no CityGML/ADE parser. |

**Assessment.** No i-UR ADE attribute is used. The PLATEAU link is via building identifiers inherited from upstream SAR products, not via `uro:` attributes in this repository.

---

### 2.9 SolarPotential (太陽光発電ポテンシャル推計)

**Purpose.** Estimates solar-radiation potential and reflects suitability for photovoltaic deployment, using PLATEAU building geometry and attributes, and performs suitability judgments (including disaster-risk exclusions).

**`uro:` input path.** C++/C#/MFC application. XPath macros in `SRC/DLL/AggregateData/AggregateData.h` and `SRC/DLL/AnalyzeData/AnalyzeData.h` define the ADE paths; the parsers are in `AggregateData.cpp` / `AnalyzeData.cpp`.

#### `uro:` attributes: usage, frequency, criticality

| i-UR table | Attribute | How it is used | Evidence | Frequency | Criticality |
|---|---|---|---|---|---|
| `uro:BuildingDetailAttribute` (also legacy `uro:BuildingDetails`) | `uro:buildingStructureType` | Reads the 3-digit structure code and maps it to wood / reinforced-concrete / steel / light-gauge steel / masonry / non-wood for suitability judgments | `AggregateData.h:86-89`; `AggregateData.cpp:694-760, 899-903`; `JudgeSuitablePlaceMng.cpp:247-253`; `ExtendedAttributeIniFile.h:117-149` | 2 XPath variants + parser + judgment | **Analytical-critical** |
| `uro:BuildingIDAttribute` | `uro:buildingID` | Building identifier used to key results; extracted from `uro:buildingIDAttribute/uro:BuildingIDAttribute/uro:buildingID` | `AggregateData.h:105-106`; `AggregateData.cpp:2505`; `AnalyzeData.h:85-86`; `AnalyzeData.cpp:3383` | 2 XPath pairs + 2 direct paths | **Structural** |
| `uro:KeyValuePair` (via `uro:extendedAttribute`) | `uro:key`, `uro:codeValue` | Local-government extended attributes; keys `10` and `100` map to a custom structure type and floor-type code used in suitability judgments | `AggregateData.h:90-92`; `AggregateData.cpp:907-1000`; `JudgeSuitablePlaceMng.cpp:251-311` | 3 XPaths + parser + judgment | **Analytical (secondary)** |
| `uro:BuildingRiverFloodingRiskAttribute` | `uro:depth` | XPath and parser `getRiverFloodingRisk` extract maximum flood depth; **no call site found in the repository** | `AggregateData.h:79-80`; `AggregateData.cpp:369-522` | 1 parser, 0 calls | **Joined-but-unused / Dead** |
| `uro:BuildingTsunamiRiskAttribute` | `uro:depth` | XPath and parser `getTsunamiRisk` extract tsunami height; **no call site found** | `AggregateData.h:81-82`; `AggregateData.cpp:524-655` | 1 parser, 0 calls | **Joined-but-unused / Dead** |
| `uro:BuildingLandSlideRiskAttribute` | (presence / `uro:description`) | XPath and parser `getLandSlideRisk` check landslide-area presence; `uro:description` XPath is defined but unused; **no call site found** | `AggregateData.h:82-83`; `AggregateData.cpp:657-692` | 1 parser, 0 calls | **Joined-but-unused / Dead** |

**Important nuance.** The disaster-risk *fields* used in the final suitability judgments (`dFloodDepth`, `dTsunamiHeight`, `bLandslideArea`) are populated from **hazard-area LOD polygons** (`hazardRiskData`), not from the `uro:` risk attributes (`AggregateData.cpp:2320-2441, 3335-3417`; `JudgeSuitablePlaceMng.cpp:327-351, 638-662`). The `uro:` risk parsers are defined but never invoked, so the ADE risk attributes are effectively dead code in this repository. `uro:buildingStructureType`, `uro:buildingID`, and the extended key/value attributes are the active ADE inputs.

**Non-`uro:` context.** `bldg:measuredHeight` is read for building height (`AggregateData.cpp:860-890`); hazard polygons come from external LOD hazard data.

---

### 2.10 Disaster-Prevention-Planner (地区防災計画作成支援)

**Purpose.** A Laravel web application supporting the creation and management of district disaster-prevention plans (shelters, emergency supplies, stockpiles, organisations, residents, reports).

**`uro:` usage: none.**

| Search | Result |
|---|---|
| `uro:` | Only false positives: “Curotec” in the default Laravel README, and `nunomaduro/*` package names in `composer.lock`. |
| `CityGML` / `BuildingDetailAttribute` | 0 hits |
| `bldg` | Only web-form field names such as `bldgId`, `bldgLat`, `bldgLng`, and database columns `bldg_id`, `latitude`, `longitude` — not CityGML attributes. |
| PLATEAU references | Footer text (“PLATEAU by MLIT”) and embedded Re:Earth viewer URLs (`system/config/reearth.php`). |

**Assessment.** No i-UR ADE attribute is used. The application links to PLATEAU/Re:Earth visualizations and stores building IDs/coordinates, but does not read `uro:` attributes.

---

### 2.11 Building-collapse-detector (家屋倒壊判定モジュール)

**Purpose.** A Fortran subroutine integrated into the iRIC Morpho2DH debris-flow solver to judge whether individual buildings collapse under debris-flow forces, varying the collapse threshold by building attributes.

**`uro:` usage: none directly.**

| Search | Result |
|---|---|
| `uro:` / `CityGML` | 0 hits |
| Attribute input | The solver receives building attributes from an iRIC/CSV/Shapefile input prepared externally. `func_cforce.f90` uses building year (`IByearA`), building height (`BHeightA`), and a storey code (`IBStoryA`, values 501–521), plus a structure-dependent base threshold (`BCritA`). |
| Evidence | `morpho2DHSolver/src/func_cforce.f90:1-80`; README states that 3D city model attributes (shape, placement, structure type) are used; 3D models are converted to CSV/Shapefile before use. |
| i-UR provenance | The mapping from `uro:`/`bldg:` fields to `IByearA`, `IBStoryA`, and `BCritA` is **outside this repository**. |

**Assessment.** No direct i-UR ADE parsing. The use case is attribute-dependent in principle (structure, year, storeys) but consumes preprocessed values whose i-UR provenance is not in the repository. Flagged as **indirect / external provenance**, not counted.

---

### 2.12 RealEstateID-matching-system (不動産ID付与)

**Purpose.** Matches PLATEAU building CityGML to real-estate registry data and writes real-estate IDs (不動産ID) back into the CityGML as i-UR ADE attributes.

**`uro:` input path.** The batch pipeline (`matching/batch/src/main.py`) imports CityGML into PostGIS with `ogr2ogr` and a GFS template (`src/lod0RoofEdge.gfs`, `src/lod0FootPrint.gfs`). The GFS maps building attributes to columns including `buildingStructureType_uro` and `buildingFootprintArea_uro` (`lod0RoofEdge.gfs:40-41, 55-56`). The matching SQL compares these with registry-derived structure/floor-space values (`main.py:459-467, 631, 866`).

**`uro:` output path.** `append_new_elements` creates `uro:bldgRealEstateIDAttribute` containing `uro:RealEstateIDAttribute`, with child elements written in this order (`main.py:997-1017, 1099-1161`):
`uro:realEstateIDOfBuilding`, `uro:numberOfBuildingUnitOwnership`, `uro:realEstateIDOfBuildingUnitOwnership` (repeated), `uro:numberOfRealEstateIDOfLand`, `uro:realEstateIDOfLand` (repeated), `uro:matchingScore`.

#### `uro:` attributes: usage, frequency, criticality

| i-UR table | Attribute | How it is used | Evidence | Frequency | Criticality |
|---|---|---|---|---|---|
| `uro:BuildingDetailAttribute` | `uro:buildingStructureType` | Read into `buildingStructureType_uro`; matched against registry structure code as part of the match score | `main.py:95-96, 142-143, 159-160, 459-467, 866`; `lod0RoofEdge.gfs:40-41` | 1 column + matching SQL | **Analytical-critical** |
| `uro:BuildingDetailAttribute` | `uro:buildingFootprintArea` | Read into `buildingFootprintArea_uro`; compared with registry floor space (`citygml_floor_space`) | `main.py:95-96, 142-143, 159-160, 459-467, 631`; `lod0RoofEdge.gfs:55-56` | 1 column + matching SQL | **Analytical-critical** |
| `uro:bldgRealEstateIDAttribute` / `uro:RealEstateIDAttribute` | `realEstateIDOfBuilding` | **Written** as the building real-estate ID | `main.py:1000-1001, 1099-1108` | output | **Analytical-critical (output)** |
| `uro:RealEstateIDAttribute` | `numberOfBuildingUnitOwnership`, `realEstateIDOfBuildingUnitOwnership` | **Written** for condominium-unit ownership IDs | `main.py:1112-1132` | output | **Analytical-critical (output)** |
| `uro:RealEstateIDAttribute` | `numberOfRealEstateIDOfLand`, `realEstateIDOfLand` | **Written** for linked land real-estate IDs | `main.py:1133-1158` | output | **Analytical-critical (output)** |
| `uro:RealEstateIDAttribute` | `matchingScore` | **Written** as the match confidence score | `main.py:1159-1165` | output | **Analytical (output metadata)** |

**Caveat.** The GFS `ElementPath` values are flat names (`buildingStructureType_uro`, `buildingFootprintArea_uro`), not explicit nested ADE XPaths. The pipeline is clearly *designed* to ingest `uro:BuildingDetailAttribute/buildingStructureType` and `uro:buildingFootprintArea`, but the exact ADE path binding depends on how the GML driver names the nested elements. The output side, in contrast, is explicit and unambiguous: it writes the i-UR `RealEstateIDAttribute` structure with the `uro:` namespace URI taken from the input file (`main.py:1077-1081`).

**Non-`uro:` context.** The pipeline also reads `bldg:usage`, `bldg:storeysAboveGround`, `bldg:storeysBelowGround`, `bldg:yearOfConstruction`, `bldg:measuredHeight`, and building geometry (`bldg:lod0RoofEdge` / `bldg:lod0FootPrint`), plus `gml:id` and a `gen:stringAttribute` building ID.

---

### 2.13 Disaster-damage-simulator (水害・土砂災害の家屋被害額予測)

**Purpose.** An ArcGIS Pro toolkit that simulates flood/sediment disasters and estimates per-building damage costs, using PLATEAU-derived building attributes.

**`uro:` input path (indirect).** Attribute tables are preprocessed/exported with fully qualified ADE column names. The Python scripts read these columns from an ArcGIS feature class.

#### `uro:` attributes: usage, frequency, criticality

| i-UR table | Attribute | How it is used | Evidence | Frequency | Criticality |
|---|---|---|---|---|---|
| `uro:BuildingDetailAttribute` | `uro:buildingStructureType` → `uro_BuildingDetailAttribute_buildingStructureType` | Looked up with building usage to select a building unit price and a damage-rate pattern (e.g. `評価額_建物単価.csv`, `損傷率_建物.csv`) | `plateau/tools/python/cal_value_all.py:34, 80`; `cal_value_damage.py:132, 149` | 2 scripts + 2 lookups | **Analytical-critical (indirect)** |
| `uro:BuildingDetailAttribute` | `uro:totalFloorArea` → `totalFloorArea` / `uro_BuildingDetailAttribute_totalFloorArea` | Multiplied by unit price to compute building value (`value_building`) | `plateau/tools/python/cal_value_all.py:81, 111`; `plateau/symbol/plateau_3d.lyrx`, `plateau_symbol.lyrx` | 1 calculation + symbology | **Analytical-critical (indirect)** |
| `uro:BuildingIDAttribute` | `uro:prefecture` → `uro_buildingIDAttribute_prefecture` | Included in the attribute export and layer symbology; not used in the damage-value calculation itself | `cal_value_all.py:80`; `plateau/symbol/plateau_3d.lyrx`, `plateau_symbol.lyrx` | 1 export + symbology | **Joined-but-unused / Context** |

**Non-`uro:` context.** `bldg:usage` (`bldg_usage1`), `bldg:measuredHeight`/height, `bldg:storeysAboveGround`/`BelowGround`, and a derived `buildingType` drive the calculations.

**Caveat.** The Python code reads the unprefixed `totalFloorArea` column, while the ArcGIS layer files reference the fully qualified `uro_BuildingDetailAttribute_totalFloorArea`. This is consistent with an ArcGIS flattening/renaming step; both refer to the same i-UR `uro:totalFloorArea` field.

---

## 3. Cross-repository attribute matrix

Legend: **●** consumed analytically / in pipeline · **◐** joined, parsed, or exposed but not consumed · **○** fallback or secondary use · **▽** visualization-only · **✎** written as output · **·** not present.

| i-UR attribute | USA | Fire | VIEW | Solar | REID | DDS | Land | Fluid | EQ | Snow | SAR | DPP | BCD |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `uro:totalFloorArea` | ● | ○ | ● | · | · | ● | · | · | · | · | · | · | · |
| `uro:buildingFootprintArea` | ◐ | ○ | ● | · | ● | · | · | · | · | · | · | · | · |
| `uro:buildingStructureType` | ◐ | ● | ● | ● | ● | ● | · | · | · | · | · | · | · |
| `uro:fireproofStructureType` | ◐ | ● | ● | · | · | · | · | · | · | · | · | · | · |
| `uro:districtsAndZonesType` | ◐ | ● | ● | · | · | · | · | · | · | · | · | · | · |
| `uro:buildingHeight` / `uro:eaveHeight` | ◐ | · | ● | · | · | · | · | · | · | · | · | · | · |
| `uro:surveyYear` | ◐ | · | ● | · | · | · | · | · | · | · | · | · | · |
| `uro:majorUsage*` / `uro:detailedUsage*` / floor usages | · | · | ● | · | · | · | · | · | · | · | · | · | · |
| `uro:BuildingIDAttribute` (`buildingID`, `branchID`, `partID`, `prefecture`, `city`) | · | · | ● | ● | · | ◐ | · | · | · | · | · | · | · |
| `uro:DataQualityAttribute` / `PublicSurveyDataQualityAttribute` | · | · | ● | · | · | · | · | · | · | · | · | · | · |
| Risk: `rank`, `rankOrg`, `scale`, `depth`, `description`, `adminType`, `duration` | ◐ (dead) | · | ● | ◐ (dead) | · | · | · | · | · | · | · | · | · |
| `uro:LandUseDetailAttribute` | · | · | ● | · | · | · | · | · | · | · | · | · | · |
| `uro:LargeCustomerFacilityAttribute` | · | · | ● | · | · | · | · | · | · | · | · | · | · |
| `uro:RealEstateIDAttribute` | · | · | ● | · | ✎ | · | · | · | · | · | · | · | · |
| `uro:RoadStructureAttribute` / `TrafficVolumeAttribute` | · | · | ● | · | · | · | · | · | · | · | · | · | · |
| `uro:SquareUrbanPlanAttribute` / `StationSquareAttribute` / `TerminalAttribute` | · | · | ● | · | · | · | · | · | · | · | · | · | · |
| `uro:KeyValuePair` (extended attributes) | · | ◐ | · | ● | · | · | · | · | · | · | · | · | · |
| `uro:BuildingDetails` (generic container) | · | ◐ | · | · | · | · | · | · | · | · | · | · | · |
| *(non-`uro:`) `bldg:usage` | ● | ● | ● | · | ● | ● | · | · | · | · | · | · | · |
| *(non-`uro:`) `bldg:storeysAboveGround/BelowGround` | ● | ● | ● | · | ● | ● | · | · | · | · | · | · | ◐ |
| *(non-`uro:`) `bldg:yearOfConstruction` | ▽ | ● | ● | · | ● | · | · | · | · | · | · | · | ◐ |
| *(non-`uro:`) `bldg:measuredHeight` | · | ● | ● | ● | ● | ● | ● | · | · | · | · | · | ● |

Column keys: **USA** Urban-structure-analysis; **Fire** Fire-Spread-Simulator; **VIEW** PLATEAU-VIEW-5.0; **Solar** SolarPotential; **REID** RealEstateID-matching-system; **DDS** Disaster-damage-simulator; **Land** landscape-design-tool; **Fluid** Fluid-dynamics-simulator; **EQ** Earthquake-simulation-tools; **Snow** snow-removal-prioritization-system; **SAR** SAR-Hazard-Estimator; **DPP** Disaster-Prevention-Planner; **BCD** Building-collapse-detector.

---

## 4. Observations and patterns

1. **ADE adoption remains selective: 6 of 13 repositories use `uro:` attributes.** The other seven are geometry-only, consume preprocessed derivatives without in-repo ADE provenance, or are front-end/planning tools.

2. **`uro:buildingStructureType` is the most widely consumed ADE attribute** (Fire-Spread, PLATEAU-VIEW, SolarPotential, RealEstateID, Disaster-damage) — five repositories. `uro:totalFloorArea` follows (Urban-structure, Fire-Spread as fallback, PLATEAU-VIEW, Disaster-damage). `uro:buildingFootprintArea`, `uro:fireproofStructureType`, and `uro:districtsAndZonesType` are used by two to three repositories each.

3. **A naive `uro`/`usage` search over-attributes standard `bldg` data.** Urban-structure’s population logic leans heavily on `bldg:usage`, `bldg:storeysAboveGround/BelowGround`, and `bldg:yearOfConstruction`, none of which are `uro:` attributes. Reports that count these as i-UR ADE would substantially overstate ADE dependence. The same applies to Fire-Spread (`bldg:usage`, `bldg:storeysAboveGround`) and RealEstateID (`bldg:usage`, `bldg:storeys*`, `bldg:yearOfConstruction`).

4. **Two important ADE inputs are dead code.** Urban-structure joins the entire `uro:RiverFloodingRiskAttribute` table (`depth`, `scale` → `flood_depth_l1/l2`) but never consumes it. SolarPotential defines XPaths and parsers for `RiverFlooding`/`Tsunami`/`LandSlide` risk attributes but never calls them; its actual risk judgement uses external hazard polygons. In both cases, a search for `uro:` alone would overstate analytical dependence.

5. **Fire-Spread-Simulator has the most tightly coupled ADE dependency.** Five `BuildingDetailAttribute` fields drive a four-level fireproof/structure fallback chain that determines each building’s fire-spread class. The bundled `plateaupy` parser also reads generic `uro:BuildingDetails` and `uro:KeyValuePair` blocks, but the fire-simulation conversion does not consume them.

6. **RealEstateID-matching-system is the only repository that writes i-UR ADE output.** It writes `uro:bldgRealEstateIDAttribute/uro:RealEstateIDAttribute` with building, unit-ownership, land, and match-score children. Its input side reads `uro:buildingStructureType` and `uro:buildingFootprintArea` for matching, although the GFS mapping uses flat column names.

7. **PLATEAU-VIEW-5.0 is infrastructure, not a use case.** Its 190 flattened `uro:` attribute specs, 4,874 schema references, 85 inspector labels, and dedicated QC validators make it schema-complete. Its criticality is platform-level; it supports many downstream use cases rather than computing one indicator. It is also the only repository that actively consumes the disaster-risk attribute family (`rank`, `rankOrg`, `scale`, `depth`, `description`, `adminType`, `duration`).

8. **Disaster-damage-simulator is the clearest indirect ADE consumer.** It reads `uro_BuildingDetailAttribute_buildingStructureType` and `totalFloorArea` from a preprocessed ArcGIS feature class to compute building values and damage rates. `uro_buildingIDAttribute_prefecture` is exported and used in symbology but not in the calculation.

9. **Risk-attribute naming diverges by i-UR generation.** Urban-structure uses `uro:depth`/`uro:scale` from `uro:RiverFloodingRiskAttribute`; Fire-Spread uses no risk attributes; SolarPotential targets `uro:buildingDisasterRiskAttribute/uro:BuildingRiverFloodingRiskAttribute` (dead); PLATEAU-VIEW supports five flood/tsunami risk classes (`RiverFlooding`, `Tsunami`, `HighTide`, `InlandFlooding`, `ReservoirFlooding`) plus `LandSlideRiskAttribute` in the Plateau 3 flattener, with both Plateau 3 and Plateau 4 naming (`uro:buildingDisasterRiskAttribute` vs `uro:BuildingRiverFloodingRiskAttribute`, etc.).

10. **Schema cross-checking is essential.** Because GeoPackage/MVT/ArcGIS conversion strips or transforms the `uro:` prefix, field names alone are ambiguous. Cross-checking against `server/citygml/schema_defs.json` prevented misattributing `usage`, `storeys`, and `yearOfConstruction` to i-UR ADE, and confirmed that `uro:usage` is not a `BuildingDetailAttribute` property.

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
| snow-removal-prioritization-system | `b0a0208` |
| SAR-Hazard-Estimator | `6e87f64` |
| SolarPotential | `a175dd3` |
| Disaster-Prevention-Planner | `a514568` |
| Building-collapse-detector | `9fc799b` |
| RealEstateID-matching-system | `ae08e47` |
| Disaster-damage-simulator | `2f712fd` |

### 5.2 Representative search commands

```bash
# Any i-UR / ADE reference in the repository
grep -rIn --exclude-dir=.git --exclude-dir=node_modules \
  -E "uro:|uro_[A-Za-z]|BuildingDetailAttribute|RiverFloodingRiskAttribute|i-UR|iur" <repo>

# Canonical building ADE attributes (active and dead)
grep -rIoh -E "uro:(totalFloorArea|buildingFootprintArea|buildingStructureType|fireproofStructureType|districtsAndZonesType|buildingHeight|surveyYear|majorUsage|detailedUsage|groundFloorUsage|rank|rankOrg|depth|scale|description|adminType|duration|buildingID|prefecture)" <repo>

# Prefix-stripped/preprocessed ADE columns
grep -rIn -E "uro_[A-Za-z]+Attribute_|buildingStructureType_uro|buildingFootprintArea_uro|_uro\b" <repo>

# Distinguish standard bldg attributes from ADE
grep -rIn -E "bldg:(usage|yearOfConstruction|storeysAboveGround|storeysBelowGround|measuredHeight)" <repo>
```

### 5.3 Key files by repository

| Repository | Primary evidence files |
|---|---|
| Urban-structure-analysis | `algorithms/utils/data_loader.py`; `algorithms/utils/building_data_assigner.py`; `config/LayersColoringConfig.xml`; `algorithms/utils/dir_maker.py` |
| Fire-Spread-Simulator | `Src/SimulationSourceFileCreator/Resources/ElementAddSetting.xml`; `.../Controller/IntermediateCsvFileCreator.cs`; `.../ElementAddCityGmlFileCreator.cs`; `Src/ExternalTools/Src_GeneFile/plateaupy/plbldg.py` |
| PLATEAU-VIEW-5.0 | `flow/engine/runtime/action-plateau-processor/src/plateau4/attribute_flattener/flatten_attributes.json`; `.../plateau4/building_usage_attribute_validator.rs`; `.../plateau4/missing_attribute_detector.rs`; `.../plateau3/attribute_flattener.rs`; `server/citygml/attributes.go`; `server/citygml/schema_defs.json`; `extension/src/shared/plateau/featureInspector/parseAttributes.ts` |
| landscape-design-tool | `Runtime/VisualizeHeight/VisualizeHeight.cs`; no `uro:` code |
| Fluid-dynamics-simulator | `src/srcWeb/app/Http/Controllers/CityModelController.php`; README (FME conversion); no `uro:` code |
| Earthquake-simulation-tools | `apps/viewer/src/lib/utils/DeckLayerFactory.ts`; `packages/shared/src/constants/buildingDamageThresholds.ts`; no `uro:` code |
| snow-removal-prioritization-system | `README.md` (three-repository split); no `uro:` code |
| SAR-Hazard-Estimator | `src/integrate_sar_analysis.py`; CSV inputs; no `uro:` code |
| SolarPotential | `SRC/DLL/AggregateData/AggregateData.h` and `.cpp`; `SRC/DLL/AnalyzeData/AnalyzeData.h` and `.cpp`; `SRC/DLL/JudgeSuitablePlace/*`; `SampleData/1_R6CityGML/54363371_bldg_6697.gml` |
| Disaster-Prevention-Planner | `system/` Laravel app; no `uro:` code |
| Building-collapse-detector | `morpho2DHSolver/src/func_cforce.f90`; `func_fbuilding.f90`; README; no `uro:` code |
| RealEstateID-matching-system | `matching/batch/src/main.py`; `matching/batch/src/lod0RoofEdge.gfs`; `matching/batch/src/lod0FootPrint.gfs` |
| Disaster-damage-simulator | `plateau/tools/python/cal_value_all.py`; `plateau/tools/python/cal_value_damage.py`; `plateau/symbol/plateau_3d.lyrx`; `plateau_symbol.lyrx` |

### 5.4 Coverage verification

- The canonical catalog in Appendix A was built from `PLATEAU-VIEW-5.0/server/citygml/schema_defs.json`: **156 `uro` feature/complex types** and **1,654 `uro:`-prefixed properties**.
- All 13 repositories were searched for every `uro` type/property name, for `uro:` XPath/JSON keys, and for prefix-stripped/preprocessed variants (`uro_...`).
- Seven repositories produced zero `uro` matches: landscape-design, Fluid-dynamics, Earthquake-simulation, snow-removal, SAR-Hazard-Estimator, Disaster-Prevention-Planner, and Building-collapse-detector. For the last two and Earthquake, the use case is attribute-dependent in principle, but the i-UR provenance is external and is flagged as indirect, not counted.
- Test fixtures, generated bundles, embedded schemas, and lock files were excluded from usage counts; they are not evidence of runtime use.

### 5.5 Caveats

- Static analysis only; runtime behaviour for edge cases (malformed CityGML, alternate i-UR versions, missing attributes) was not executed.
- “Frequency” counts are static reference counts and are sensitive to templates, tests, generated/bundled files, and duplicate configurations; they are indicative, not precise runtime metrics.
- PLATEAU-VIEW-5.0 is a monorepo with generated bundles and large schema/test fixtures; fixture GML/XSD files were excluded from the counts.
- Dead-code findings (Urban-structure flood join, SolarPotential risk parsers) are based on the absence of call sites in the repository; they could be invoked by an external host/exported symbol not present in the snapshot.
- The RealEstateID GFS mapping uses flat column names; the exact nested ADE XPath binding is implicit.
- Repository default branches and commit contents are as of the dates shown above.

---

## Appendix A — Full i-UR Urban Object Module (`uro`) catalog

The table below lists every `uro` feature type and complex type found in the i-UR schema used by PLATEAU-VIEW-5.0, with all `uro:`-prefixed properties. It is the checklist against which the 13 repositories were searched. “Kind” distinguishes concrete feature types from reusable complex types; many complex types are used as the value of an attribute property (e.g. `uro:BuildingDetailAttribute` inside `uro:buildingDetailAttribute`).

| `uro` type | Kind | # props | Properties (all `uro:`-prefixed) |
|---|---|---:|---|
| `uro:AbstractConstruction` | feature | 22 | `uro:boundedBy`, `uro:conditionOfConstruction`, `uro:consBaseAttribute`, `uro:consDataQualityAttribute`, `uro:consDisasterRiskAttribute`, `uro:consDmAttribute`, `uro:consFacilityAttribute`, `uro:consFacilityIdAttribute`, `uro:consFacilityTypeAttribute`, `uro:consStructureAttribute`, `uro:constructionEvent`, `uro:constructionInstallation`, `uro:dateOfConstruction`, `uro:dateOfDemolition`, `uro:elevation`, `uro:height`, `uro:lod0Geometry`, `uro:lod1Geometry`, `uro:lod2Geometry`, `uro:lod3Geometry`, `uro:lod4Geometry`, `uro:occupancy` |
| `uro:Appurtenance` | feature | 17 | `uro:administrator`, `uro:appurtenanceType`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:nextLink`, `uro:occupierName`, `uro:occupierType`, `uro:offsetDepth`, `uro:previousLink`, `uro:rotationAngle`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:BridgeFunctionalAttribute` | complexType | 2 | `uro:directionType`, `uro:userType` |
| `uro:BridgeStructureAttribute` | complexType | 11 | `uro:area`, `uro:bridgeType`, `uro:escalator`, `uro:heightRestriction`, `uro:length`, `uro:material`, `uro:slopeType`, `uro:underGirderHeight`, `uro:weightRestriction`, `uro:width`, `uro:widthRestriction` |
| `uro:BuildingDataQualityAttribute` | complexType | 6 | `uro:appearanceSrcDesc`, `uro:geometrySrcDesc`, `uro:lod1HeightType`, `uro:lodType`, `uro:srcScale`, `uro:thematicSrcDesc` |
| `uro:BuildingDetailAttribute` | complexType | 38 | `uro:areaClassificationType`, `uro:basementFirstUsage`, `uro:basementSecondUsage`, `uro:basementUsage`, `uro:buildingCoverageRate`, `uro:buildingFootprintArea`, `uro:buildingHeight`, `uro:buildingRoofEdgeArea`, `uro:buildingStructureOrgType`, `uro:buildingStructureType`, `uro:detailedUsage`, `uro:detailedUsage2`, `uro:detailedUsage3`, `uro:developmentArea`, `uro:districtsAndZonesType`, `uro:eaveHeight`, `uro:fireproofStructureType`, `uro:floorAreaRate`, `uro:groundFloorUsage`, `uro:implementingBody`, `uro:landUseType`, `uro:majorUsage`, `uro:majorUsage2`, `uro:note`, `uro:orgUsage`, `uro:orgUsage2`, `uro:reference`, `uro:secondFloorUsage`, `uro:serialNumberOfBuildingCertification`, `uro:siteArea`, `uro:specifiedBuildingCoverageRate`, `uro:specifiedFloorAreaRate`, `uro:standardFloorAreaRate`, `uro:surveyYear`, `uro:thirdFloorUsage`, `uro:totalFloorArea`, `uro:urbanPlanType`, `uro:vacancy` |
| `uro:BuildingHighTideRiskAttribute` | complexType | 4 | `uro:depth`, `uro:description`, `uro:rank`, `uro:rankOrg` |
| `uro:BuildingIDAttribute` | complexType | 5 | `uro:branchID`, `uro:buildingID`, `uro:city`, `uro:partID`, `uro:prefecture` |
| `uro:BuildingInlandFloodingRiskAttribute` | complexType | 4 | `uro:depth`, `uro:description`, `uro:rank`, `uro:rankOrg` |
| `uro:BuildingLandSlideRiskAttribute` | complexType | 2 | `uro:areaType`, `uro:description` |
| `uro:BuildingRiverFloodingRiskAttribute` | complexType | 7 | `uro:adminType`, `uro:depth`, `uro:description`, `uro:duration`, `uro:rank`, `uro:rankOrg`, `uro:scale` |
| `uro:BuildingTsunamiRiskAttribute` | complexType | 4 | `uro:depth`, `uro:description`, `uro:rank`, `uro:rankOrg` |
| `uro:Cable` | feature | 27 | `uro:administrator`, `uro:cables`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:columns`, `uro:depth`, `uro:endNode`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:lengthAttribute`, `uro:material`, `uro:maxDepth`, `uro:maxWidth`, `uro:minDepth`, `uro:occupierName`, `uro:occupierType`, `uro:offset`, `uro:offsetDepth`, `uro:routeEndNode`, `uro:routeStartNode`, `uro:rows`, `uro:startNode`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:CargoHandlingFacility` | complexType | 21 | `uro:ability`, `uro:acquisitionYear`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:innerOfSiteArea`, `uro:innerTotalFloorArea`, `uro:isDesignated`, `uro:liftableLoad`, `uro:mainCargo`, `uro:mainMaterial`, `uro:mooringFacility`, `uro:note`, `uro:outerOfTotalFloorArea`, `uro:outerSiteArea`, `uro:packingName`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:totalCost` |
| `uro:CircularCurveType` | complexType | 4 | `uro:curveLength`, `uro:cutLength`, `uro:intersection`, `uro:radius` |
| `uro:CityFurnitureDataQualityAttribute` | complexType | 5 | `uro:appearanceSrcDesc`, `uro:geometrySrcDesc`, `uro:lodType`, `uro:srcScale`, `uro:thematicSrcDesc` |
| `uro:CityFurnitureDetailAttribute` | complexType | 2 | `uro:description`, `uro:facilityType` |
| `uro:ClosureSurface` | feature | 2 | `uro:lod2MultiSurface`, `uro:lod3MultiSurface` |
| `uro:ConstructionBaseAttribute` | complexType | 14 | `uro:adminOffice`, `uro:adminType`, `uro:administorator`, `uro:completionYear`, `uro:constructionStartYear`, `uro:facilityAge`, `uro:installer`, `uro:installerType`, `uro:kana`, `uro:operatorType`, `uro:purpose`, `uro:specification`, `uro:structureOrdinance`, `uro:update` |
| `uro:ConstructionDataQualityAttribute` | complexType | 8 | `uro:appearanceSrcDesc`, `uro:dataAcquisition`, `uro:geometrySrcDesc`, `uro:lod1HeightType`, `uro:lodType`, `uro:photoScale`, `uro:srcScale`, `uro:thematicSrcDesc` |
| `uro:ConstructionEvent` | complexType | 3 | `uro:dateOfEvent`, `uro:description`, `uro:event` |
| `uro:ConstructionInstallation` | feature | 5 | `uro:class`, `uro:function`, `uro:lod2Geometry`, `uro:lod3Geometry`, `uro:usage` |
| `uro:ConstructionRiskAssessmentAttribute` | complexType | 4 | `uro:referenceDate`, `uro:riskType`, `uro:status`, `uro:surveyYear` |
| `uro:ConstructionStructureAttribute` | complexType | 5 | `uro:depth`, `uro:length`, `uro:structureType`, `uro:volume`, `uro:width` |
| `uro:ControlPoint` | complexType | 6 | `uro:endPoint`, `uro:endPost`, `uro:function`, `uro:parameter`, `uro:startPoint`, `uro:startPost` |
| `uro:ControlPointType` | complexType | 4 | `uro:circularCurve`, `uro:slopeType`, `uro:transitionCurve`, `uro:verticalCurve` |
| `uro:CountermeasuresCost` | complexType | 2 | `uro:cost`, `uro:costUnit` |
| `uro:CyberportMarinaAndPBS` | complexType | 48 | `uro:apronWidth`, `uro:areaType`, `uro:bumper`, `uro:ceilingHeight`, `uro:currentDepth`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:facilityWidth`, `uro:form`, `uro:geologicalType`, `uro:grantType`, `uro:gravityResistant`, `uro:innerOfSiteArea`, `uro:innerTotalFloorArea`, `uro:isDesignated`, `uro:isDredged`, `uro:lifesaving`, `uro:lifesavingNumber`, `uro:lighting`, `uro:mainCargo`, `uro:mainMaterial`, `uro:mainPartLength`, `uro:mainVessels`, `uro:mooringPostWeight`, `uro:note`, `uro:numberOfMooringPosts`, `uro:numberOfSeats`, `uro:numberOfVehicleBoardings`, `uro:obstructingStructures`, `uro:outerOfTotalFloorArea`, `uro:outerSiteArea`, `uro:plannedDepth`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:resistantMaterial`, `uro:restrictionStructure`, `uro:shipType`, `uro:stairs`, `uro:storageCapacity`, `uro:storageCapacityUnit`, `uro:structureType`, `uro:subsidy`, `uro:totalCost`, `uro:totalLength`, `uro:vehicleBoardingWidth`, `uro:waveDissipatorLength` |
| `uro:DamAttribute` | complexType | 7 | `uro:damCode`, `uro:depth`, `uro:length`, `uro:structureType`, `uro:totalWaterStorage`, `uro:volume`, `uro:width` |
| `uro:DmAnnotation` | complexType | 12 | `uro:dmCode`, `uro:dmElement`, `uro:geometryType`, `uro:isVertical`, `uro:label`, `uro:linewidth`, `uro:lod0anchorPoint`, `uro:meshCode`, `uro:orientation`, `uro:shapeType`, `uro:size`, `uro:spacing` |
| `uro:DmElement` | complexType | 16 | `uro:annotationType`, `uro:attributeType`, `uro:attributeValue`, `uro:attributeValueType`, `uro:breakType`, `uro:creationDate`, `uro:dataType`, `uro:dislocationType`, `uro:elementKey`, `uro:freeSpace`, `uro:hierarchyLevel`, `uro:infoType`, `uro:locationType`, `uro:precisionType`, `uro:terminationDate`, `uro:updateDate` |
| `uro:DmGeometricAttribute` | complexType | 14 | `uro:angle`, `uro:dmCode`, `uro:dmElement`, `uro:elevation`, `uro:geometryType`, `uro:is3d`, `uro:isEdited`, `uro:isInstallation`, `uro:isSupplementarySymbol`, `uro:lod0Geometry`, `uro:mapLevel`, `uro:meshCode`, `uro:shapeType`, `uro:visibility` |
| `uro:Duct` | feature | 25 | `uro:administrator`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:depth`, `uro:endNode`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:lengthAttribute`, `uro:material`, `uro:maxDepth`, `uro:maxWidth`, `uro:minDepth`, `uro:occupierName`, `uro:occupierType`, `uro:offset`, `uro:offsetDepth`, `uro:routeEndNode`, `uro:routeStartNode`, `uro:startNode`, `uro:thematicShape`, `uro:width`, `uro:year`, `uro:yearType` |
| `uro:ElectricityCable` | feature | 27 | `uro:administrator`, `uro:cables`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:columns`, `uro:depth`, `uro:endNode`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:lengthAttribute`, `uro:material`, `uro:maxDepth`, `uro:maxWidth`, `uro:minDepth`, `uro:occupierName`, `uro:occupierType`, `uro:offset`, `uro:offsetDepth`, `uro:routeEndNode`, `uro:routeStartNode`, `uro:rows`, `uro:startNode`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:Elevation` | complexType | 2 | `uro:elevationReference`, `uro:elevationValue` |
| `uro:EmbankmentAttribute` | complexType | 8 | `uro:ceilingHeight`, `uro:depth`, `uro:length`, `uro:mainPartLength`, `uro:structureType`, `uro:volume`, `uro:waveDissipatorLength`, `uro:width` |
| `uro:FacilityIdAttribute` | complexType | 11 | `uro:alternativeName`, `uro:branchId`, `uro:city`, `uro:endPost`, `uro:id`, `uro:partId`, `uro:prefecture`, `uro:route`, `uro:startLat`, `uro:startLong`, `uro:startPost` |
| `uro:FacilityTypeAttribute` | complexType | 2 | `uro:class`, `uro:function` |
| `uro:FishingPortCapacity` | complexType | 22 | `uro:candlePower`, `uro:capacity`, `uro:facilityId`, `uro:handleablePower`, `uro:heightAboveAWL`, `uro:heightOnFoundations`, `uro:hullForm`, `uro:lightType`, `uro:luminousColor`, `uro:luminousRange`, `uro:maximumGroundingWeight`, `uro:maximumRefueling`, `uro:maximumWaterSupply`, `uro:other`, `uro:people`, `uro:period`, `uro:shipNumber`, `uro:waterDepth-2m`, `uro:waterDepth2-3m`, `uro:waterDepth3-6m`, `uro:waterDepth6-m`, `uro:weightCapacity` |
| `uro:FishingPortFacility` | complexType | 24 | `uro:address`, `uro:administrator`, `uro:area`, `uro:ceilingHeight`, `uro:cost`, `uro:dateOfConstructionOrAcquisition`, `uro:depth`, `uro:designatedAdministrator`, `uro:designatedArea`, `uro:designation`, `uro:facilityDetailsType`, `uro:facilityId`, `uro:facilityManager`, `uro:grantType`, `uro:length`, `uro:mainMaterial`, `uro:note`, `uro:otherSizeDescription`, `uro:otherStructure`, `uro:portName`, `uro:portType`, `uro:referenceNumber`, `uro:structureType`, `uro:width` |
| `uro:GroundSurface` | feature | 2 | `uro:lod2MultiSurface`, `uro:lod3MultiSurface` |
| `uro:Handhole` | feature | 21 | `uro:administrator`, `uro:appurtenance`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:containerType`, `uro:depth`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:innerDiamiterLong`, `uro:innerDiamiterShort`, `uro:occupierName`, `uro:occupierType`, `uro:offsetDepth`, `uro:outerDiamiterLong`, `uro:outerDiamiterShort`, `uro:rotationAngle`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:HarborFacility` | complexType | 23 | `uro:areaType`, `uro:currentDepth`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:geologicalType`, `uro:grantType`, `uro:innerArea`, `uro:isDesignated`, `uro:isDredged`, `uro:length`, `uro:maximumWidth`, `uro:minimumWidth`, `uro:note`, `uro:obstructingStructures`, `uro:outerArea`, `uro:plannedDepth`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:structuralLimitations`, `uro:subsidy`, `uro:totalCost` |
| `uro:Height` | complexType | 4 | `uro:highReference`, `uro:lowReference`, `uro:status`, `uro:value` |
| `uro:HighTideRiskAttribute` | complexType | 4 | `uro:depth`, `uro:description`, `uro:rank`, `uro:rankOrg` |
| `uro:IfcAxis2Placement3D` | complexType | 3 | `uro:axis`, `uro:location`, `uro:refDirection` |
| `uro:IfcBuilding` | complexType | 9 | `uro:buildingAddress`, `uro:compositionType`, `uro:description`, `uro:elevationOfRefHeight`, `uro:elevationOfTerrain`, `uro:globalId`, `uro:longName`, `uro:name`, `uro:objectType` |
| `uro:IfcBuildingElement` | complexType | 15 | `uro:capacityByNumber`, `uro:capacityByWeight`, `uro:description`, `uro:elementType`, `uro:globalId`, `uro:name`, `uro:numberOfRiser`, `uro:numberOfTreads`, `uro:objectType`, `uro:operationType`, `uro:predefinedType`, `uro:riserHeight`, `uro:shapeType`, `uro:tag`, `uro:treadLength` |
| `uro:IfcBuildingStorey` | complexType | 7 | `uro:compositionType`, `uro:description`, `uro:elevation`, `uro:globalId`, `uro:longName`, `uro:name`, `uro:objectType` |
| `uro:IfcClassification` | complexType | 4 | `uro:edition`, `uro:editionDate`, `uro:name`, `uro:source` |
| `uro:IfcClassificationReference` | complexType | 4 | `uro:itemReference`, `uro:location`, `uro:name`, `uro:referenceSource` |
| `uro:IfcCoordinateReferenceSystem` | complexType | 4 | `uro:description`, `uro:geodeticDatum`, `uro:name`, `uro:verticalDatum` |
| `uro:IfcCurtainWall` | complexType | 15 | `uro:capacityByNumber`, `uro:capacityByWeight`, `uro:description`, `uro:elementType`, `uro:globalId`, `uro:name`, `uro:numberOfRiser`, `uro:numberOfTreads`, `uro:objectType`, `uro:operationType`, `uro:predefinedType`, `uro:riserHeight`, `uro:shapeType`, `uro:tag`, `uro:treadLength` |
| `uro:IfcDoor` | complexType | 17 | `uro:capacityByNumber`, `uro:capacityByWeight`, `uro:description`, `uro:elementType`, `uro:globalId`, `uro:name`, `uro:numberOfRiser`, `uro:numberOfTreads`, `uro:objectType`, `uro:operationType`, `uro:overallHeight`, `uro:overallWidth`, `uro:predefinedType`, `uro:riserHeight`, `uro:shapeType`, `uro:tag`, `uro:treadLength` |
| `uro:IfcFurnishingElement` | complexType | 5 | `uro:description`, `uro:globalId`, `uro:name`, `uro:objectType`, `uro:tag` |
| `uro:IfcGeometricRepresentationContext` | complexType | 6 | `uro:contextIdentifier`, `uro:contextType`, `uro:coordinateSpaceDimension`, `uro:precision`, `uro:trueNorth`, `uro:worldCoordinateSystem` |
| `uro:IfcGroup` | complexType | 4 | `uro:description`, `uro:globalId`, `uro:name`, `uro:objectType` |
| `uro:IfcMapConversion` | complexType | 8 | `uro:eastings`, `uro:northings`, `uro:orthogonalHeight`, `uro:scale`, `uro:sourceCRS`, `uro:targetCRS`, `uro:xAxisAbscissa`, `uro:xAxisOrdinate` |
| `uro:IfcOpeningElement` | complexType | 7 | `uro:description`, `uro:globalId`, `uro:name`, `uro:nominalArea`, `uro:nominalVolume`, `uro:objectType`, `uro:tag` |
| `uro:IfcProject` | complexType | 8 | `uro:description`, `uro:globalId`, `uro:longName`, `uro:name`, `uro:objectType`, `uro:phase`, `uro:representationContexts`, `uro:unitsInContext` |
| `uro:IfcProjectedCRS` | complexType | 7 | `uro:description`, `uro:geodeticDatum`, `uro:mapProjection`, `uro:mapUnit`, `uro:mapZone`, `uro:name`, `uro:verticalDatum` |
| `uro:IfcPsetBuildingCommon` | complexType | 11 | `uro:ancillaryFireUse`, `uro:buildingId`, `uro:grossPlannedArea`, `uro:isLandmarked`, `uro:isPermanentId`, `uro:mainFireUse`, `uro:numberOfStoreys`, `uro:occupancyType`, `uro:sprinklerProtection`, `uro:sprinklerProtectionAutomatic`, `uro:yearOfConstruction` |
| `uro:IfcPsetDoorCommon` | complexType | 12 | `uro:acousticRating`, `uro:fireExit`, `uro:firerating`, `uro:glazingAreaFraction`, `uro:handicapAccessible`, `uro:infiltration`, `uro:isExternal`, `uro:reference`, `uro:securityRating`, `uro:selfClosing`, `uro:smokeStop`, `uro:thermalTransmittance` |
| `uro:IfcPsetOpeningElementCommon` | complexType | 5 | `uro:fireExit`, `uro:parallelJambs`, `uro:protectedOpening`, `uro:purpose`, `uro:reference` |
| `uro:IfcPsetSiteCommon` | complexType | 3 | `uro:buildableArea`, `uro:buildingHeightLimit`, `uro:totalArea` |
| `uro:IfcPsetSpaceCommon` | complexType | 12 | `uro:category`, `uro:ceilingCovering`, `uro:concealedCeiling`, `uro:concealedFlooring`, `uro:floorCovering`, `uro:grossPlannedArea`, `uro:handicapAccessible`, `uro:netPlannedArea`, `uro:publiclyAccessible`, `uro:reference`, `uro:skirtingBoard`, `uro:wallCovering` |
| `uro:IfcPsetWindowCommon` | complexType | 9 | `uro:acousticRating`, `uro:fireRating`, `uro:glazingAreaFraction`, `uro:infiltration`, `uro:isExternal`, `uro:reference`, `uro:securityRating`, `uro:smokeStop`, `uro:thermalTransmittance` |
| `uro:IfcRoof` | complexType | 15 | `uro:capacityByNumber`, `uro:capacityByWeight`, `uro:description`, `uro:elementType`, `uro:globalId`, `uro:name`, `uro:numberOfRiser`, `uro:numberOfTreads`, `uro:objectType`, `uro:operationType`, `uro:predefinedType`, `uro:riserHeight`, `uro:shapeType`, `uro:tag`, `uro:treadLength` |
| `uro:IfcSite` | complexType | 11 | `uro:compositionType`, `uro:description`, `uro:globalId`, `uro:landTitleNumber`, `uro:longName`, `uro:name`, `uro:objectType`, `uro:refElevation`, `uro:refLatitude`, `uro:refLongitude`, `uro:siteAddress` |
| `uro:IfcSpace` | complexType | 8 | `uro:compositionType`, `uro:description`, `uro:elevationWithFlooring`, `uro:globalId`, `uro:interiorOrExteriorSpace`, `uro:longName`, `uro:name`, `uro:objectType` |
| `uro:IfcSpaceBaseQuantity` | complexType | 13 | `uro:clearHeight`, `uro:finishCeilingHeight`, `uro:grossCeilingArea`, `uro:grossFloorArea`, `uro:grossPerimeter`, `uro:grossVolume`, `uro:grossWallArea`, `uro:netCeilingArea`, `uro:netFloorArea`, `uro:netPerimeter`, `uro:netVolume`, `uro:netWallArea`, `uro:nominalHeight` |
| `uro:IfcUnit` | complexType | 4 | `uro:dimensions`, `uro:name`, `uro:perfix`, `uro:unitType` |
| `uro:IfcWall` | complexType | 28 | `uro:capacityByNumber`, `uro:capacityByWeight`, `uro:description`, `uro:elementType`, `uro:globalId`, `uro:grossFootPrintArea`, `uro:grossSideArea`, `uro:grossSideAreaLeft`, `uro:grossSideAreaRight`, `uro:grossVolume`, `uro:name`, `uro:netFootPrintArea`, `uro:netSideArea`, `uro:netSideAreaLeft`, `uro:netSideAreaRight`, `uro:netVolume`, `uro:nominalHeight`, `uro:nominalLength`, `uro:nominalWidth`, `uro:numberOfRiser`, `uro:numberOfTreads`, `uro:objectType`, `uro:operationType`, `uro:predefinedType`, `uro:riserHeight`, `uro:shapeType`, `uro:tag`, `uro:treadLength` |
| `uro:IfcWallStandardCase` | complexType | 28 | `uro:capacityByNumber`, `uro:capacityByWeight`, `uro:description`, `uro:elementType`, `uro:globalId`, `uro:grossFootPrintArea`, `uro:grossSideArea`, `uro:grossSideAreaLeft`, `uro:grossSideAreaRight`, `uro:grossVolume`, `uro:name`, `uro:netFootPrintArea`, `uro:netSideArea`, `uro:netSideAreaLeft`, `uro:netSideAreaRight`, `uro:netVolume`, `uro:nominalHeight`, `uro:nominalLength`, `uro:nominalWidth`, `uro:numberOfRiser`, `uro:numberOfTreads`, `uro:objectType`, `uro:operationType`, `uro:predefinedType`, `uro:riserHeight`, `uro:shapeType`, `uro:tag`, `uro:treadLength` |
| `uro:IfcWindow` | complexType | 17 | `uro:capacityByNumber`, `uro:capacityByWeight`, `uro:description`, `uro:elementType`, `uro:globalId`, `uro:name`, `uro:numberOfRiser`, `uro:numberOfTreads`, `uro:objectType`, `uro:operationType`, `uro:overallHeight`, `uro:overallWidth`, `uro:predefinedType`, `uro:riserHeight`, `uro:shapeType`, `uro:tag`, `uro:treadLength` |
| `uro:IfcZone` | complexType | 4 | `uro:description`, `uro:globalId`, `uro:name`, `uro:objectType` |
| `uro:IndoorFacilityAttribute` | complexType | 5 | `uro:phone`, `uro:source`, `uro:website`, `uro:weekdayHours`, `uro:weekendHours` |
| `uro:IndoorFurnishingAttribute` | complexType | 2 | `uro:floorId`, `uro:source` |
| `uro:IndoorPublicTagAttribute` | complexType | 2 | `uro:source`, `uro:ucode` |
| `uro:IndoorSpaceAttribute` | complexType | 6 | `uro:floorId`, `uro:isPublic`, `uro:isRestricted`, `uro:source`, `uro:suite`, `uro:tollType` |
| `uro:IndoorStoreyAttribute` | complexType | 3 | `uro:category`, `uro:ordinal`, `uro:source` |
| `uro:IndoorTacatileTileAttribute` | complexType | 6 | `uro:category`, `uro:endNode`, `uro:floorId`, `uro:roof`, `uro:source`, `uro:startNode` |
| `uro:IndoorUserDefinedAttribute` | complexType | 5 | `uro:description`, `uro:name`, `uro:nominalValue`, `uro:source`, `uro:unit` |
| `uro:IndoorZoneAttribute` | complexType | 2 | `uro:floorId`, `uro:source` |
| `uro:InlandFloodingRiskAttribute` | complexType | 4 | `uro:depth`, `uro:description`, `uro:rank`, `uro:rankOrg` |
| `uro:KeyValuePairAttribute` | complexType | 8 | `uro:codeValue`, `uro:dateValue`, `uro:doubleValue`, `uro:intValue`, `uro:key`, `uro:measuredValue`, `uro:stringValue`, `uro:uriValue` |
| `uro:LandSlideRiskAttribute` | complexType | 2 | `uro:areaType`, `uro:description` |
| `uro:LandUseDataQualityAttribute` | complexType | 3 | `uro:geometrySrcDesc`, `uro:srcScale`, `uro:thematicSrcDesc` |
| `uro:LandUseDetailAttribute` | complexType | 20 | `uro:areaClassificationType`, `uro:areaInHa`, `uro:areaInSquareMeter`, `uro:buildingCoverageRate`, `uro:city`, `uro:districtsAndZonesType`, `uro:floorAreaRate`, `uro:id`, `uro:nominalArea`, `uro:note`, `uro:orgLandUse`, `uro:owner`, `uro:ownerType`, `uro:prefecture`, `uro:reference`, `uro:specifiedBuildingCoverageRate`, `uro:specifiedFloorAreaRate`, `uro:standardFloorAreaRate`, `uro:surveyYear`, `uro:urbanPlanType` |
| `uro:LargeCustomerFacilityAttribute` | complexType | 18 | `uro:areaClassificationType`, `uro:availability`, `uro:capacity`, `uro:class`, `uro:districtsAndZonesType`, `uro:inauguralDate`, `uro:keyTenants`, `uro:landUseType`, `uro:name`, `uro:note`, `uro:owner`, `uro:reference`, `uro:surveyYear`, `uro:totalFloorArea`, `uro:totalStoreFloorArea`, `uro:urbanPlanType`, `uro:yearClosed`, `uro:yearOpened` |
| `uro:LengthAttribute` | complexType | 3 | `uro:length`, `uro:mesureType`, `uro:phaseType` |
| `uro:LongevityMeasures` | complexType | 3 | `uro:countermeasuresCost`, `uro:description`, `uro:fiscalYearForCountermeasures` |
| `uro:MaintenanceHistoryAttribute` | complexType | 7 | `uro:description`, `uro:facilityId`, `uro:maintenanceDate`, `uro:maintenanceFiscalYear`, `uro:maintenanceType`, `uro:maintenanceYear`, `uro:status` |
| `uro:Manhole` | feature | 22 | `uro:administrator`, `uro:appurtenance`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:containerType`, `uro:depth`, `uro:elevation`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:innerDiamiterLong`, `uro:innerDiamiterShort`, `uro:occupierName`, `uro:occupierType`, `uro:offsetDepth`, `uro:outerDiamiterLong`, `uro:outerDiamiterShort`, `uro:rotationAngle`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:MooringFacility` | complexType | 37 | `uro:apronWidth`, `uro:area`, `uro:bumper`, `uro:ceilingHeight`, `uro:currentDepth`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:facilityWidth`, `uro:form`, `uro:grantType`, `uro:gravityResistant`, `uro:isDesignated`, `uro:lifesavingAppliances`, `uro:lighting`, `uro:mainCargo`, `uro:mainMaterial`, `uro:mainPartLength`, `uro:mainVessels`, `uro:mooringPostWeight`, `uro:note`, `uro:numberOfLifesavingAppliances`, `uro:numberOfMooringPosts`, `uro:numberOfSeats`, `uro:numberOfVehicleBoardings`, `uro:plannedDepth`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:resistantMaterial`, `uro:shipType`, `uro:stairs`, `uro:structureType`, `uro:subsidy`, `uro:totalCost`, `uro:totalLength`, `uro:vehicleBoardingWidth` |
| `uro:NavigationAssistanceFacility` | complexType | 11 | `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:isDesignated`, `uro:note`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:subsidy`, `uro:totalCost` |
| `uro:NumberOfFacilities` | complexType | 2 | `uro:quantity`, `uro:quantityUnit` |
| `uro:Occupancy` | complexType | 3 | `uro:interval`, `uro:numberofOccupants`, `uro:occupantType` |
| `uro:OffsetDepth` | complexType | 5 | `uro:depth`, `uro:maxDepth`, `uro:minDepth`, `uro:offset`, `uro:pos` |
| `uro:OilGasChemicalsPipe` | feature | 27 | `uro:administrator`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:depth`, `uro:endNode`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:innerDiamiter`, `uro:lengthAttribute`, `uro:material`, `uro:maxDepth`, `uro:maxWidth`, `uro:minDepth`, `uro:occupierName`, `uro:occupierType`, `uro:offset`, `uro:offsetDepth`, `uro:outerDiamiter`, `uro:routeEndNode`, `uro:routeStartNode`, `uro:sleeveType`, `uro:startNode`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:OtherConstruction` | feature | 25 | `uro:boundedBy`, `uro:class`, `uro:conditionOfConstruction`, `uro:consBaseAttribute`, `uro:consDataQualityAttribute`, `uro:consDisasterRiskAttribute`, `uro:consDmAttribute`, `uro:consFacilityAttribute`, `uro:consFacilityIdAttribute`, `uro:consFacilityTypeAttribute`, `uro:consStructureAttribute`, `uro:constructionEvent`, `uro:constructionInstallation`, `uro:dateOfConstruction`, `uro:dateOfDemolition`, `uro:elevation`, `uro:function`, `uro:height`, `uro:lod0Geometry`, `uro:lod1Geometry`, `uro:lod2Geometry`, `uro:lod3Geometry`, `uro:lod4Geometry`, `uro:occupancy`, `uro:usage` |
| `uro:OuterCeilingSurface` | feature | 2 | `uro:lod2MultiSurface`, `uro:lod3MultiSurface` |
| `uro:OuterFloorSurface` | feature | 2 | `uro:lod2MultiSurface`, `uro:lod3MultiSurface` |
| `uro:ParkFacilityLongevityPlanAttribute` | complexType | 20 | `uro:disposalLimitPeriod`, `uro:expectedRenewalYearWithMeasures`, `uro:expectedUsagePeriod`, `uro:facilityId`, `uro:facilityName`, `uro:facilityNameOptional`, `uro:installationYear`, `uro:longevityMeasures`, `uro:mainMaterial`, `uro:mainMaterialOptional`, `uro:managementType`, `uro:noteForLongevity`, `uro:numberOfFacilities`, `uro:parkCode`, `uro:parkHealthAssessment`, `uro:parkName`, `uro:parkType`, `uro:repairsBeforeParkHealthAssessment`, `uro:size`, `uro:specificFacilityName` |
| `uro:ParkHealthAssessment` | complexType | 4 | `uro:assessmentFiscalYear`, `uro:condition`, `uro:deteriorationStatus`, `uro:urgency` |
| `uro:Pipe` | feature | 27 | `uro:administrator`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:depth`, `uro:endNode`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:innerDiamiter`, `uro:lengthAttribute`, `uro:material`, `uro:maxDepth`, `uro:maxWidth`, `uro:minDepth`, `uro:occupierName`, `uro:occupierType`, `uro:offset`, `uro:offsetDepth`, `uro:outerDiamiter`, `uro:routeEndNode`, `uro:routeStartNode`, `uro:sleeveType`, `uro:startNode`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:PortEnvironmentalImprovementFacility` | complexType | 15 | `uro:area`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:isDesignated`, `uro:length`, `uro:note`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:subsidy`, `uro:totalCost`, `uro:totalFoorArea`, `uro:usage` |
| `uro:PortManagementFacility` | complexType | 17 | `uro:acquisitionYear`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:isDesignated`, `uro:loadingCapacity`, `uro:note`, `uro:numberOfShipTypes`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:subsidy`, `uro:totalCost`, `uro:totalFloorArea`, `uro:unitOfShipType`, `uro:usage` |
| `uro:PortPassengerFacility` | complexType | 15 | `uro:acquisitionYear`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:isDesignated`, `uro:length`, `uro:mainMaterial`, `uro:note`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:totalCost`, `uro:totalFloorArea`, `uro:width` |
| `uro:PortPollutionControlFacility` | complexType | 17 | `uro:area`, `uro:crossSectionalArea`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:height`, `uro:isDesignated`, `uro:length`, `uro:mainMaterial`, `uro:note`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:subsidy`, `uro:totalCost`, `uro:width` |
| `uro:PortProtectiveFacility` | complexType | 13 | `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:isDesignated`, `uro:mainMaterial`, `uro:note`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:structureType`, `uro:subsidy`, `uro:totalCost` |
| `uro:PortStorageFacility` | complexType | 18 | `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:innerOfSiteArea`, `uro:innerTotalFloorArea`, `uro:isDesignated`, `uro:mainCargo`, `uro:mainMaterial`, `uro:note`, `uro:outerOfTotalFloorArea`, `uro:outerSiteArea`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:storageCapacity`, `uro:storageCapacityUnit`, `uro:totalCost` |
| `uro:PortTransportationFacility` | complexType | 27 | `uro:area`, `uro:beddingWidth`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:heightLimit`, `uro:heightToDigit`, `uro:isDesignated`, `uro:length`, `uro:mainCargo`, `uro:minimumDepth`, `uro:minimumWidth`, `uro:note`, `uro:numberOfAircraftParkingSpaces`, `uro:numberOfLanes`, `uro:parkingLotCapacityOfBus`, `uro:parkingLotCapacityOfCars`, `uro:pavementType`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:routeType`, `uro:startingPoint`, `uro:structureType`, `uro:subsidy`, `uro:totalCost` |
| `uro:PortWasteTreatmentFacility` | complexType | 25 | `uro:acquisitionYear`, `uro:ceilingHeight`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:innerShoreLength`, `uro:isDesignated`, `uro:mainMaterial`, `uro:mainPartLength`, `uro:note`, `uro:perimeter`, `uro:plannedDisposalAmount`, `uro:plannedDisposalArea`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:receivingCapacity`, `uro:shipType`, `uro:structureType`, `uro:subsidy`, `uro:totalCost`, `uro:unitOfReceivingCapacity`, `uro:wasteType`, `uro:waveDissipatorLength` |
| `uro:PortWelfareFacility` | complexType | 11 | `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:isDesignated`, `uro:note`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:totalCost`, `uro:totalFloorArea` |
| `uro:PublicLand` | feature | 14 | `uro:area`, `uro:id`, `uro:ifcLandUseAttribute`, `uro:landCategory`, `uro:landUseDetailAttribute`, `uro:luseDataQualityAttribute`, `uro:luseDmAttribute`, `uro:luseFacilityAttribute`, `uro:luseFacilityIdAttribute`, `uro:luseFacilityTypeAttribute`, `uro:note`, `uro:ownerName`, `uro:ownerType`, `uro:status` |
| `uro:RailwayRouteAttribute` | complexType | 6 | `uro:alternativeName`, `uro:endStation`, `uro:operator`, `uro:operatorType`, `uro:railwayType`, `uro:startStation` |
| `uro:RailwayTrackAttribute` | complexType | 9 | `uro:alignmentType`, `uro:controlPoint`, `uro:directionType`, `uro:endPost`, `uro:lod2Network`, `uro:lod3Network`, `uro:routeName`, `uro:startPost`, `uro:trackType` |
| `uro:RealEstateIDAttribute` | complexType | 6 | `uro:matchingScore`, `uro:numberOfBuildingUnitOwnership`, `uro:numberOfRealEstateIDOfLand`, `uro:realEstateIDOfBuilding`, `uro:realEstateIDOfBuildingUnitOwnership`, `uro:realEstateIDOfLand` |
| `uro:RepairsBeforeParkHealthAssessment` | complexType | 2 | `uro:repair`, `uro:repairFiscalYear` |
| `uro:RiverFacilityIdAttribute` | complexType | 26 | `uro:alternativeName`, `uro:branchId`, `uro:city`, `uro:endPost`, `uro:id`, `uro:lefEndDistance`, `uro:leftDistance`, `uro:leftEndPost`, `uro:leftPost`, `uro:leftStartDistance`, `uro:leftStartPost`, `uro:partId`, `uro:prefecture`, `uro:rightDistance`, `uro:rightEndDistance`, `uro:rightEndPost`, `uro:rightPost`, `uro:rightStartDistance`, `uro:rightStartPost`, `uro:riverCode`, `uro:riverName`, `uro:route`, `uro:sideType`, `uro:startLat`, `uro:startLong`, `uro:startPost` |
| `uro:RiverFloodingRiskAttribute` | complexType | 7 | `uro:adminType`, `uro:depth`, `uro:description`, `uro:duration`, `uro:rank`, `uro:rankOrg`, `uro:scale` |
| `uro:RoadStructureAttribute` | complexType | 4 | `uro:numberOfLanes`, `uro:sectionType`, `uro:width`, `uro:widthType` |
| `uro:RoadType` | complexType | 8 | `uro:creationDate`, `uro:id`, `uro:isHighWay`, `uro:isTemporary`, `uro:isTollRoad`, `uro:roadType`, `uro:separator`, `uro:widthType` |
| `uro:RoofSurface` | feature | 2 | `uro:lod2MultiSurface`, `uro:lod3MultiSurface` |
| `uro:RoomDataQualityAttribute` | complexType | 5 | `uro:appearanceSrcDesc`, `uro:geometrySrcDesc`, `uro:lodType`, `uro:srcScale`, `uro:thematicSrcDesc` |
| `uro:SewerPipe` | feature | 28 | `uro:administrator`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:depth`, `uro:endNode`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:innerDiamiter`, `uro:lengthAttribute`, `uro:material`, `uro:maxDepth`, `uro:maxWidth`, `uro:minDepth`, `uro:occupierName`, `uro:occupierType`, `uro:offset`, `uro:offsetDepth`, `uro:outerDiamiter`, `uro:routeEndNode`, `uro:routeStartNode`, `uro:sleeveType`, `uro:slope`, `uro:startNode`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:ShipServiceFacility` | complexType | 18 | `uro:acquisitionYear`, `uro:area`, `uro:degradationLevel`, `uro:district`, `uro:facilityId`, `uro:grantType`, `uro:isDesignated`, `uro:length`, `uro:mooringPlace`, `uro:note`, `uro:portFacilityDetailsType`, `uro:portName`, `uro:portStatus`, `uro:shipType`, `uro:supplyAbility`, `uro:supplyAbilityUnit`, `uro:totalCost`, `uro:width` |
| `uro:SlopeType` | complexType | 2 | `uro:angle`, `uro:elevation` |
| `uro:SquareUrbanPlanAttribute` | complexType | 18 | `uro:areaCompleted`, `uro:areaImproved`, `uro:areaInService`, `uro:areaPlanned`, `uro:city`, `uro:dateOfDecision`, `uro:dateOfRevision`, `uro:enforcer`, `uro:isAuthorized`, `uro:isCompleted`, `uro:note`, `uro:prefecture`, `uro:projectEndDate`, `uro:projectStartDate`, `uro:purpose`, `uro:remarks`, `uro:status`, `uro:urbanPlanningAreaName` |
| `uro:StationSquareAttribute` | complexType | 21 | `uro:areaCompleted`, `uro:areaImproved`, `uro:areaInService`, `uro:areaPlanned`, `uro:city`, `uro:dateOfDecision`, `uro:dateOfRevision`, `uro:enforcer`, `uro:isAuthorized`, `uro:isCompleted`, `uro:note`, `uro:prefecture`, `uro:projectEndDate`, `uro:projectStartDate`, `uro:purpose`, `uro:railwayType`, `uro:remarks`, `uro:route`, `uro:station`, `uro:status`, `uro:urbanPlanningAreaName` |
| `uro:TelecommunicationsCable` | feature | 27 | `uro:administrator`, `uro:cables`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:columns`, `uro:depth`, `uro:endNode`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:lengthAttribute`, `uro:material`, `uro:maxDepth`, `uro:maxWidth`, `uro:minDepth`, `uro:occupierName`, `uro:occupierType`, `uro:offset`, `uro:offsetDepth`, `uro:routeEndNode`, `uro:routeStartNode`, `uro:rows`, `uro:startNode`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:TerminalAttribute` | complexType | 23 | `uro:areaCompleted`, `uro:areaImproved`, `uro:areaInService`, `uro:areaPlanned`, `uro:city`, `uro:dateOfDecision`, `uro:dateOfRevision`, `uro:enforcer`, `uro:isAuthorized`, `uro:isCompleted`, `uro:note`, `uro:numberOfBerthsInService`, `uro:numberOfBerthsPlanned`, `uro:prefecture`, `uro:projectEndDate`, `uro:projectStartDate`, `uro:purpose`, `uro:remarks`, `uro:status`, `uro:structure`, `uro:terminalType`, `uro:urbanPlanningAreaName`, `uro:userType` |
| `uro:ThematicShape` | complexType | 3 | `uro:heightType`, `uro:horizontalType`, `uro:shape` |
| `uro:ThermalPipe` | feature | 27 | `uro:administrator`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:depth`, `uro:endNode`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:innerDiamiter`, `uro:lengthAttribute`, `uro:material`, `uro:maxDepth`, `uro:maxWidth`, `uro:minDepth`, `uro:occupierName`, `uro:occupierType`, `uro:offset`, `uro:offsetDepth`, `uro:outerDiamiter`, `uro:routeEndNode`, `uro:routeStartNode`, `uro:sleeveType`, `uro:startNode`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:TrackAttribute` | complexType | 7 | `uro:adminType`, `uro:alternativeName`, `uro:isTollRoad`, `uro:relativeLevel`, `uro:separator`, `uro:structureType`, `uro:widthType` |
| `uro:TrafficAreaStructureAttribute` | complexType | 1 | `uro:numberOfLanes` |
| `uro:TrafficVolumeAttribute` | complexType | 14 | `uro:averageInboundTravelSpeedInCongestion`, `uro:averageInboundTravelSpeedNotCongestion`, `uro:averageOutboundTravelSpeedInCongestion`, `uro:averageOutboundTravelSpeedNotCongestion`, `uro:averageTravelSpeedInCongestion`, `uro:congestionRate`, `uro:largeVehicleRate`, `uro:observationPointName`, `uro:reference`, `uro:routeName`, `uro:sectionID`, `uro:surveyYear`, `uro:weekday12hourTrafficVolume`, `uro:weekday24hourTrafficVolume` |
| `uro:TransitionCurveType` | complexType | 3 | `uro:curveLength`, `uro:distance`, `uro:intersection` |
| `uro:TransportationDataQualityAttribute` | complexType | 5 | `uro:appearanceSrcDesc`, `uro:geometrySrcDesc`, `uro:lodType`, `uro:srcScale`, `uro:thematicSrcDesc` |
| `uro:TsunamiRiskAttribute` | complexType | 4 | `uro:depth`, `uro:description`, `uro:rank`, `uro:rankOrg` |
| `uro:TunnelFunctionalAttribute` | complexType | 2 | `uro:directionType`, `uro:userType` |
| `uro:TunnelStructureAttribute` | complexType | 9 | `uro:area`, `uro:effectiveHeight`, `uro:innerHeight`, `uro:length`, `uro:mouthType`, `uro:slopeType`, `uro:tunnelSubtype`, `uro:tunnelType`, `uro:width` |
| `uro:UndergroundBuilding` | feature | 13 | `uro:bldgDmAttribute`, `uro:bldgFacilityAttribute`, `uro:bldgFacilityIdAttribute`, `uro:bldgFacilityTypeAttribute`, `uro:bldgRealEstateIDAttribute`, `uro:buildingDataQualityAttribute`, `uro:buildingDetailAttribute`, `uro:buildingDisasterRiskAttribute`, `uro:buildingIDAttribute`, `uro:ifcBuildingAttribute`, `uro:indoorBuildingAttribute`, `uro:keyValuePairAttribute`, `uro:largeCustomerFacilityAttribute` |
| `uro:UserDefinedValue` | complexType | 7 | `uro:codeValue`, `uro:dateValue`, `uro:doubleValue`, `uro:intValue`, `uro:measuredValue`, `uro:stringValue`, `uro:uriValue` |
| `uro:VegetationDataQualityAttribute` | complexType | 4 | `uro:appearanceSrcDesc`, `uro:geometrySrcDesc`, `uro:srcScale`, `uro:thematicSrcDesc` |
| `uro:VerticalCurveType` | complexType | 2 | `uro:length`, `uro:verticalDistance` |
| `uro:WallSurface` | feature | 2 | `uro:lod2MultiSurface`, `uro:lod3MultiSurface` |
| `uro:WaterBodyDetailAttribute` | complexType | 11 | `uro:adminType`, `uro:area`, `uro:city`, `uro:flowDirection`, `uro:kana`, `uro:maximumDepth`, `uro:measurementYearMonth`, `uro:prefecture`, `uro:riverCode`, `uro:waterSurfaceElevation`, `uro:waterSystemCode` |
| `uro:WaterBodyHighTideRiskAttribute` | complexType | 4 | `uro:depth`, `uro:description`, `uro:rank`, `uro:rankOrg` |
| `uro:WaterBodyInlandFloodingRiskAttribute` | complexType | 4 | `uro:depth`, `uro:description`, `uro:rank`, `uro:rankOrg` |
| `uro:WaterBodyRiverFloodingRiskAttribute` | complexType | 7 | `uro:adminType`, `uro:depth`, `uro:description`, `uro:duration`, `uro:rank`, `uro:rankOrg`, `uro:scale` |
| `uro:WaterBodyTsunamiRiskAttribute` | complexType | 4 | `uro:depth`, `uro:description`, `uro:rank`, `uro:rankOrg` |
| `uro:WaterPipe` | feature | 27 | `uro:administrator`, `uro:cityFurnitureDataQualityAttribute`, `uro:cityFurnitureDetailAttribute`, `uro:depth`, `uro:endNode`, `uro:frnDmAttribute`, `uro:frnFacilityAttribute`, `uro:frnFacilityIdAttribute`, `uro:frnFacilityTypeAttribute`, `uro:innerDiamiter`, `uro:lengthAttribute`, `uro:material`, `uro:maxDepth`, `uro:maxWidth`, `uro:minDepth`, `uro:occupierName`, `uro:occupierType`, `uro:offset`, `uro:offsetDepth`, `uro:outerDiamiter`, `uro:routeEndNode`, `uro:routeStartNode`, `uro:sleeveType`, `uro:startNode`, `uro:thematicShape`, `uro:year`, `uro:yearType` |
| `uro:Waterway` | feature | 6 | `uro:tranDataQualityAttribute`, `uro:tranDmAttribute`, `uro:tranFacilityAttribute`, `uro:tranFacilityIdAttribute`, `uro:tranFacilityTypeAttribute`, `uro:waterwayDetailAttribute` |
| `uro:WaterwayDetailAttribute` | complexType | 9 | `uro:length`, `uro:maximumWidth`, `uro:minimumWidth`, `uro:navigation`, `uro:plannedDepth`, `uro:routeDirection`, `uro:routeId`, `uro:speedLimit`, `uro:targetShipType` |

---

## Appendix B — Attributes actively used in the analysed repositories

The following compact index complements the matrix in Section 3. It lists the `uro:` attributes for which an active consumer, fallback, parser, or writer was found. Attributes present only as schema/label coverage (PLATEAU-VIEW) or as dead code are marked accordingly in Sections 2 and 3.

| Attribute | Type context | Repositories |
|---|---|---|
| `uro:totalFloorArea` | `BuildingDetailAttribute` | Urban-structure (●), Fire-Spread (○), PLATEAU-VIEW (●), Disaster-damage (●) |
| `uro:buildingFootprintArea` | `BuildingDetailAttribute` | Fire-Spread (○), PLATEAU-VIEW (●), RealEstateID (● input) |
| `uro:buildingStructureType` | `BuildingDetailAttribute` | Fire-Spread (●), PLATEAU-VIEW (●), SolarPotential (●), RealEstateID (● input), Disaster-damage (●) |
| `uro:fireproofStructureType` | `BuildingDetailAttribute` | Fire-Spread (●), PLATEAU-VIEW (●) |
| `uro:districtsAndZonesType` | `BuildingDetailAttribute` | Fire-Spread (●), PLATEAU-VIEW (●) |
| `uro:buildingHeight`, `uro:eaveHeight` | `BuildingDetailAttribute` | PLATEAU-VIEW (●) |
| `uro:surveyYear` | `BuildingDetailAttribute` | PLATEAU-VIEW (● QC) |
| `uro:majorUsage*`, `uro:detailedUsage*`, `uro:groundFloorUsage`, `uro:secondFloorUsage`, `uro:thirdFloorUsage`, `uro:basement*Usage` | `BuildingDetailAttribute` | PLATEAU-VIEW (● QC) |
| `uro:buildingID`, `uro:branchID`, `uro:partID`, `uro:prefecture`, `uro:city` | `BuildingIDAttribute` | PLATEAU-VIEW (●), SolarPotential (● buildingID) |
| `uro:prefecture` | `BuildingIDAttribute` | Disaster-damage (◐ exported/symbology) |
| `uro:geometrySrcDescLodN`, `uro:thematicSrcDesc`, `uro:srcScaleLodN`, `uro:publicSurveySrcDescLodN` | `DataQualityAttribute` / `PublicSurveyDataQualityAttribute` | PLATEAU-VIEW (● QC) |
| `uro:rank`, `uro:rankOrg`, `uro:scale`, `uro:depth`, `uro:description`, `uro:adminType`, `uro:duration`, `uro:areaType` | Risk attributes (`RiverFlooding`, `Tsunami`, `HighTide`, `InlandFlooding`, `ReservoirFlooding`, `LandSlide`) | PLATEAU-VIEW (●); Urban-structure (◐ dead depth/scale); SolarPotential (◐ dead depth/description) |
| `uro:realEstateIDOfBuilding`, `uro:realEstateIDOfLand`, `uro:realEstateIDOfBuildingUnitOwnership`, `uro:numberOfRealEstateIDOfLand`, `uro:numberOfBuildingUnitOwnership`, `uro:matchingScore` | `RealEstateIDAttribute` | RealEstateID (✎ output); PLATEAU-VIEW (● flatten of two fields) |
| `uro:key`, `uro:codeValue` | `KeyValuePair` (extended attributes) | SolarPotential (● custom structure/floor type); Fire-Spread (◐ parsed, unused) |
| `uro:LandUseDetailAttribute` fields | `LandUseDetailAttribute` | PLATEAU-VIEW (●) |
| `uro:LargeCustomerFacilityAttribute` fields | `LargeCustomerFacilityAttribute` | PLATEAU-VIEW (●) |
| `uro:RoadStructureAttribute`, `uro:TrafficVolumeAttribute` fields | transport attributes | PLATEAU-VIEW (●) |
| `uro:SquareUrbanPlanAttribute`, `uro:StationSquareAttribute`, `uro:TerminalAttribute` fields | urban-plan attributes | PLATEAU-VIEW (●) |

*Symbols: ● active consumer/pipeline; ○ fallback/secondary; ◐ parsed/joined/exposed but unused or context; ✎ written output.*
