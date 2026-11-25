# PLATEAU Attribute Descriptions — Additions

This file supplements `PLATEAU_attribute_descriptions.md` with practical explanations for three areas that the translated attribute list alone does not make obvious:

1. `uro:KeyValuePairAttribute` — how dataset-defined code attributes work.
2. `uro:DataQualityAttribute` and `uro:PublicSurveyDataQualityAttribute` — mandatory status, meaning, and why high LODs often look “unknown”.
3. `uro:BuildingIDAttribute` field `uro:branchID` — what it represents and why it is absent from the analysed data.

## Part 1 — `uro:KeyValuePairAttribute` in practice

### Short answer

`uro:KeyValuePairAttribute` is a generic, dataset-defined extension mechanism for adding an extra **code-type** attribute to a building without changing the CityGML/i-UR schema. It consists of a key code (`uro:key`) and a value code (`uro:codeValue`), each resolved through a codelist. It is not a free-form key/value store; for non-code values (strings, integers, dates, measures, free text), use `gen:_GenericAttribute` instead.

### What it is for / why it exists

- i-UR/PLATEAU defines a core set of building attributes, but municipalities and data publishers often need to carry additional coded attributes (for example building structure, fire-prevention district, height district, change flags).
- Rather than modifying the schema, the standard provides a generic role: `uro:bldgKeyValuePairAttribute` on `bldg:Building`, containing zero or more `uro:KeyValuePairAttribute` elements.
- Each pair is “key = which extended attribute” and “codeValue = which coded option for that attribute”.
- Both fields are `gml:CodeType` and must have `codeSpace` URIs pointing to codelists. The key codelist is `KeyValuePairAttribute_key.xml`; the value codelist is selected by the key (for example key `100` maps to `KeyValuePairAttribute_key100.xml`).
- The human-readable meaning of a key lives in the codelist as `gml:description`, not in the GML itself.

### The two fields

| Field | Type | Multiplicity | Meaning | Codelist |
|---|---|---|---|---|
| `uro:key` | `gml:CodeType` | `[1..1]` | Identifies which extended attribute is being encoded | `KeyValuePairAttribute_key.xml`; `gml:description` gives the human-readable name |
| `uro:codeValue` | `gml:CodeType` | `[1..1]` | The coded value for that key | `KeyValuePairAttribute_key<key>.xml` (spec form: `KeyValuePairAttribute_key[key].xml`) |

- The building role is `uro:bldgKeyValuePairAttribute` with multiplicity `[0..*]` on `bldg:Building`.
- Multiple pairs may appear; one pair carries one value. Repeating the same key is technically possible but ambiguous unless the codelist allows multi-valued codes.

### How it is applied, step by step

1. Read `uro:key` and resolve it through `KeyValuePairAttribute_key.xml` to learn what the attribute is.
2. Use the key value to build the value-codelist filename: `KeyValuePairAttribute_key100.xml` for key `100`.
3. Resolve `uro:codeValue` through that codelist to get the meaning.
4. Keep the `codeSpace` URIs relative to the GML file, as in the Hachioji data, so the codelist files stay tied to the dataset.
5. Do not invent meanings from the integer alone; the same numeric code can mean different things under different keys.

### Concrete example — Hachioji 2025

Source: `13201_hachioji_2025_op/udx/bldg/53393139_bldg_6697_op.gml` and `13201_hachioji_2025_op/codelists/`.

Key codelist `KeyValuePairAttribute_key.xml`:

| Key | Japanese description | English gloss |
|---|---|---|
| `100` | 建物構造コード | Building structure code |
| `101` | 延べ面積換算コード | Total floor area conversion code |
| `102` | 変化フラグ | Change flag |
| `105` | 高度地区 | Height district |
| `106` | 防火及び準防火地域 | Fire prevention / quasi-fire prevention district |

Value codelist `KeyValuePairAttribute_key100.xml`:

| `codeValue` | Japanese | English |
|---|---|---|
| `11` | 耐火構造 | Fireproof structure |
| `12` | 準防火造 | Semi-fireproof structure |
| `21` | 防火造 | Fire-resistant structure |
| `22` | 木造 | Wooden structure |
| `0` | 調査時不明 | Unknown at survey time |
| `99` | 不明 | Unknown |

XML example — key `100` with value `99` means “building structure code = unknown”:

```xml
<uro:bldgKeyValuePairAttribute>
  <uro:KeyValuePairAttribute>
    <uro:key codeSpace="../../codelists/KeyValuePairAttribute_key.xml">100</uro:key>
    <uro:codeValue codeSpace="../../codelists/KeyValuePairAttribute_key100.xml">99</uro:codeValue>
  </uro:KeyValuePairAttribute>
</uro:bldgKeyValuePairAttribute>
```

XML example — key `106` with value `20` means “fire/quasi-fire prevention district = quasi-fire prevention district”:

```xml
<uro:bldgKeyValuePairAttribute>
  <uro:KeyValuePairAttribute>
    <uro:key codeSpace="../../codelists/KeyValuePairAttribute_key.xml">106</uro:key>
    <uro:codeValue codeSpace="../../codelists/KeyValuePairAttribute_key106.xml">20</uro:codeValue>
  </uro:KeyValuePairAttribute>
</uro:bldgKeyValuePairAttribute>
```

### Important interpretation rules

- `codeValue=99` under key `100` is a meaningful code (“unknown”), not an encoding error or a missing value.
- The meaning is dataset-specific because the codelists are published by the data provider. The same key number in another dataset must be checked against that dataset’s codelists.
- `uro:KeyValuePairAttribute` carries **codes only**. Free text and numeric quantities belong in `gen:_GenericAttribute` (for example `gen:stringAttribute`, `gen:integerAttribute`, `gen:measureAttribute`).
- Do not replace the standard `uro:BuildingDetailAttribute` fields with key/value pairs; use key/value only for attributes not defined in the standard schema.

### Older PLATEAU / i-UR encoding note

Older PLATEAU data uses different element names for the same idea:

| Older element | Newer element |
|---|---|
| `uro:extendedAttribute` | `uro:bldgKeyValuePairAttribute` |
| `uro:KeyValuePair` | `uro:KeyValuePairAttribute` |
| `extendedAttribute_key.xml` | `KeyValuePairAttribute_key.xml` |

When comparing datasets across PLATEAU versions, check both spellings.

### When to use it vs. other mechanisms

- Use `uro:BuildingDetailAttribute` / `uro:LargeCustomerFacilityAttribute` for attributes the standard already defines (usage, building structure, floors, survey year, etc.).
- Use `uro:KeyValuePairAttribute` only for **additional coded** attributes defined by the dataset/codelist.
- Use `gen:_GenericAttribute` for non-coded additions (free text, numbers, dates, measurements).
- Use `uro:BuildingIDAttribute` fields for identifier semantics, not key/value pairs.

## Part 2 — `uro:DataQualityAttribute` and `uro:PublicSurveyDataQualityAttribute`

### Short answer

`uro:bldgDataQualityAttribute` is mandatory in principle on every `bldg:Building` (or on its `bldg:BuildingPart`s), and its sub-attributes are conditionally mandatory depending on which LODs and source types are in scope. They are genuinely useful in real-world applications for provenance, fitness-for-use, QA, integration, and official/legal traceability. The high “unknown” counts at high LODs are mostly `999`/`99` = “not created”, not missing metadata. When a LOD actually exists, the quality attributes are populated and informative. So the high-LOD unknowns are largely a structural consequence of LOD coverage, not a reason to discard the attributes.

### 1. Mandatory status

- `uro:bldgDataQualityAttribute` is a role on `bldg:_AbstractBuilding` with multiplicity `[0..1]`.
- The product specification says it is **mandatory in principle** (原則必須):
  - If a `bldg:Building` has no `bldg:BuildingPart`, the quality attribute must be on the Building.
  - If the Building is composed of BuildingParts, the quality attribute may be placed on the BuildingParts instead; in that case the Building itself may omit it.
- The XML Schema (`urbanObject.xsd`) is more permissive: most quality sub-elements have `minOccurs="0"`; only `geometrySrcDescLod1` has `minOccurs="1"`. Mandatory rules are product-spec conformance, not schema enforcement.

Conditional mandatory table:

| Sub-attribute | Multiplicity | Mandatory condition | “Not created” value |
|---|---|---|---|
| `geometrySrcDescLod0` | `[0..*]` | LOD0 in scope | `999` |
| `geometrySrcDescLod1` | `[1..*]` | Always (buildings have LOD1) | `999` |
| `geometrySrcDescLod2` | `[0..*]` | LOD2 in scope | `999` |
| `geometrySrcDescLod3` | `[0..*]` | LOD3 in scope | `999` |
| `geometrySrcDescLod4` | `[0..*]` | LOD4 in scope | `999` |
| `thematicSrcDesc` | `[0..*]` | Thematic attributes in scope | — |
| `appearanceSrcDescLod0` | `[0..*]` | LOD0 appearance in scope | `99` |
| `appearanceSrcDescLod1` | `[0..*]` | LOD1 appearance in scope | `99` |
| `appearanceSrcDescLod2` | `[0..*]` | LOD2 appearance in scope | `99` |
| `appearanceSrcDescLod3` | `[0..*]` | LOD3 appearance in scope | `99` |
| `appearanceSrcDescLod4` | `[0..*]` | LOD4 appearance in scope | `99` |
| `lodType` | `[0..*]` | Mandatory for buildings with LOD2+; for roads/railways at LOD3 | — |
| `lod1HeightType` | `[0..1]` | Optional, but important for interpreting height | — |
| `tranDataAcquisition` | `[0..*]` | Road features only | — |

`uro:publicSurveyDataQualityAttribute` is a nested role with multiplicity `[0..1]`:

- It becomes conditionally mandatory when `geometrySrcDescLodN` is only `000` (public/basic survey geometry).
- In that case `srcScaleLodN` and `publicSurveySrcDescLodN` are mandatory.
- XSD alone marks it optional; the conditional rule comes from the product specification.

### 2. What they record

`uro:DataQualityAttribute` records:

- Geometry source per LOD (`geometrySrcDescLod0`–`4`): where the geometry came from (public survey map, BIM/CAD, estimation, other GIS, not created, etc.).
- Thematic source (`thematicSrcDesc`): source of the semantic attributes.
- Appearance source per LOD (`appearanceSrcDescLod0`–`4`): image, scan, other, or not created.
- LOD type (`lodType`): how faithfully the geometry represents the building (for example `2.2`, `3.3`, `4.2`).
- LOD1 height derivation (`lod1HeightType`): point-cloud statistic, aerial photo, building confirmation documents, uniform fallback, etc.
- For roads only: `tranDataAcquisition`.

`uro:PublicSurveyDataQualityAttribute` records:

- `srcScaleLodN`: source map scale for each LOD (for example `1` = 1:500, `2` = 1:1000, `3` = 1:2500, `9` = undefined).
- `publicSurveySrcDescLodN`: which public/basic survey data was used for each LOD.

Together they document provenance, not just presence/absence of geometry.

### 3. Why higher LODs show more “unknown” values

- The analysis used the regex `^-?9+$` to count “unknown”; this conflates several different codes.
- `geometrySrcDesc`: `999` = geometry not created; `901` = estimation; `500` = BIM/CAD; `400` = other GIS; `000` = public/basic survey. Thus `999` is a meaningful “LOD not created”, not a data-quality failure.
- `appearanceSrcDesc`: `99` = appearance not created; `1`–`5` = actual source types.
- `srcScale`: `9` = undefined; `0`–`3` = actual scales.
- `9999` is a sentinel value; `0` and `8` in `lod1HeightType` are uniform-height fallbacks.
- In the analysed Takeshiba data:
  - `geometrySrcDescLod0` / `Lod1` and `thematicSrcDesc`: 0% unknown; 100% populated.
  - `geometrySrcDescLod3`: about 98.5% unknown; `Lod4`: about 100% unknown.
  - `appearanceSrcDescLod3`: about 99.2% unknown; `Lod4`: about 100% unknown.
  - `lodType`: about 87.2% coverage.
  - `publicSurveySrcDescLod2` / `srcScaleLod2`: about 86.3% coverage.
- The pattern is expected: LOD0/LOD1 and thematic data are always in scope, while LOD3/LOD4 geometry and appearance are often not created for many buildings. When those LODs do exist, the quality fields are filled meaningfully.
- Concrete counter-example from `53393680_bldg_6697_223342_op.gml`, building `bldg_4ab21821-b73b-4ef2-95b4-de2859999fc7`:
  - `geometrySrcDescLod3 = 000,400`, `geometrySrcDescLod4 = 500`
  - `appearanceSrcDescLod3 = 5`, `appearanceSrcDescLod4 = 1`
  - `lodType = 2.2,3.3,4.2`
  - `lod1HeightType = 2`
  - `thematicSrcDesc = 201,000,023,400`
  - `publicSurveySrcDescLod0/1 = 003,023`, `srcScaleLod0/1 = 1`
- High-LOD “unknown” counts are therefore mostly a structural consequence of LOD coverage, not a reason to discard the data-quality attributes.

## Part 3 — `uro:branchID`

### Short answer

`uro:branchID` is optional (`[0..1]`, `xs:integer`). It is not one of the mandatory `BuildingIDAttribute` fields — only `uro:buildingID` and `uro:city` are mandatory. It represents a branch number for an ancillary/attached building (for example a warehouse, shed, garbage collection point, or assembly hall) that is treated as part of the same principal building and therefore shares the same `uro:buildingID`. It was almost certainly absent in the analysed data because most PLATEAU datasets model each building as a separate `bldg:Building` with its own unique `buildingID`; they do not use the “one main building + ancillary buildings sharing the same ID” pattern. In the Hachioji and Takeshiba samples, `uro:branchID`, `uro:partID`, `bldg:BuildingPart`, and the generic attribute `枝番` are all absent.

### What `branchID` represents

- The XSD defines `uro:branchID` as `xs:integer` with `minOccurs="0"` and `maxOccurs="1"` on the `BuildingIDAttribute` type.
- The concept from the PLATEAU work procedure (C.3.2.5) is:
  - **Principal building**: the main building that has a `buildingID`.
  - **Ancillary building**: a smaller building attached to or associated with the principal building (warehouse, shed, garbage collection point, assembly hall, etc.).
  - If an ancillary building is treated as part of the same building, it can share the principal building’s `uro:buildingID` and be distinguished by a branch number.
- The i-UR 4.0 draft gives the English definition: “Branch ID for Warehouses and sheds associated with the main building”.
- The work procedure says that when multiple buildings are given the same building ID, a branch number can be assigned if it is necessary to distinguish the main building from ancillary buildings. It also notes that ancillary buildings should mainly have spatial attributes, and that supplemental information can be put in `uro:note`.
- In older PLATEAU materials the same idea appears as a generic attribute named `枝番` (branch number), which is not part of the standard `uro` schema.

### Mandatory status

- XSD multiplicity for `BuildingIDAttribute`:

| Field | Type | Multiplicity | Mandatory? |
|---|---|---|---|
| `uro:buildingID` | `xs:integer` | `[1..1]` | Yes |
| `uro:city` | `xs:string` | `[1..1]` | Yes |
| `uro:prefecture` | `xs:string` | `[0..1]` | No |
| `uro:branchID` | `xs:integer` | `[0..1]` | No |
| `uro:partID` | `xs:integer` | `[0..1]` on `bldg:Building`; mandatory on `bldg:BuildingPart` | Conditional |

- The standard work procedure C.3.2.5 lists five attributes for `uro:BuildingIDAttribute`, but says only `buildingID` and `city` are mandatory.
- `branchID` is conditional/practical: use it only when several buildings deliberately share the same `buildingID`. Otherwise each building gets its own unique `buildingID` and `branchID` is omitted.
- The work procedure wording is permissive (“can distinguish”), not a hard requirement.

### Why it was never present in the analysed data

- `branchID` is optional and only meaningful under a specific modelling choice: one principal `buildingID` shared by ancillary buildings.
- Most PLATEAU CityGML datasets follow the simpler pattern: one `bldg:Building` per physical building, each with a unique `uro:buildingID`. In that pattern there is no need for `branchID`.
- If a building is divided into parts (different roof shape, number of storeys, or use), the standard mechanism is `bldg:BuildingPart` with `uro:partID`, not `branchID`. The analysed samples had no `bldg:BuildingPart` either.
- Some municipalities may encode an ancillary-building branch number as a generic attribute `枝番` instead of `uro:branchID`; the analysed samples had no `枝番` either.
- The 2020 PLATEAU attribute publication list shows `枝番` (branch number) in only 14 of 56 cities, while `建物ID` (building ID) appears in all 57 listed cities. So even when the concept is used, it is not standardised across all datasets.
- Concrete sample counts:
  - Hachioji `53393139_bldg_6697_op.gml`: `branchID = 0`, `partID = 0`, `bldg:BuildingPart = 0`, `枝番 = 0`.
  - Takeshiba `53393680_bldg_6697_223342_op.gml`: `branchID = 0`, `partID = 0`, `bldg:BuildingPart = 0`, `枝番 = 0`.

### What to do if branch numbers are needed

- **Option A — share the main `buildingID` and add a branch number**: keep `uro:buildingID` the same for the principal and ancillary buildings; add `uro:branchID` (or a documented generic `枝番`) to distinguish them. Record the convention in metadata/notes.
- **Option B — give every building its own `buildingID`**: treat each physical building as a separate `bldg:Building` with a unique `buildingID`; do not use `branchID`. This is the most common PLATEAU pattern and avoids ambiguity.
- **Option C — true parts of one building**: if the “pieces” are parts of the same building rather than separate ancillary buildings, model them as `bldg:BuildingPart` and use `uro:partID`.
- In all cases, keep the modelling choice consistent within a dataset and document it, because `branchID` alone does not explain what kind of ancillary building is present; use `uro:note` or `uro:usage` for that.

## Sources

- PLATEAU `bldg:Building` extended attributes index: https://www.mlit.go.jp/plateaudocument/toc4/toc4_02/toc4_02_03/toc4_02_03_02/
- `uro:BuildingIDAttribute`: https://www.mlit.go.jp/plateaudocument/toc4/toc4_02/toc4_02_03/toc4_02_03_02/_0c2d6556-52fb-73df-f30d-1179d54b9f41
- `uro:KeyValuePairAttribute`: https://www.mlit.go.jp/plateaudocument/toc4/toc4_02/toc4_02_03/toc4_02_03_02/_0c7cf3d3-0fef-be4b-502e-0c3f22c70d59
- `uro:DataQualityAttribute`: https://www.mlit.go.jp/plateaudocument/toc4/toc4_02/toc4_02_03/toc4_02_03_02/_66dcc9d1-cf9a-9b1f-5f7d-f4d4e0991cc6
- `uro:PublicSurveyDataQualityAttribute`: https://www.mlit.go.jp/plateaudocument/toc4/toc4_02/toc4_02_03/toc4_02_03_02/_9cc36889-505e-0dec-59d1-3937fdaff377
- `bldg:Building` role/multiplicity table: https://www.mlit.go.jp/plateaudocument/toc4/toc4_02/toc4_02_03/toc4_02_03_01/_2866d73e-c0ea-8c02-25a8-9d2fc438a297
- PLATEAU Standard Product Specification PDF: https://www.mlit.go.jp/plateau/file/libraries/doc/plateau_doc_0001_ver04.pdf
- i-UR 4.0 draft dictionary: https://www.geospatial.jp/iur/shiyouan4_0.pdf
- 2020 PLATEAU attribute publication list: https://gic-plateau.s3.ap-northeast-1.amazonaws.com/2020/attributedata.pdf
- i-UR 3.2 codelist base URL: https://www.geospatial.jp/iur/codelists/3.2/
- Local Hachioji sample: `/home/kellyrsch/mscthesis/bldg/53393139_bldg_6697_op.gml`
- Local Hachioji codelists: `/home/kellyrsch/mscthesis/bldg/codelists/`
- Local Takeshiba sample: `/home/kellyrsch/mscthesis/53393680_bldg_6697_223342_op.gml`
- Local XSD: `/home/kellyrsch/mscthesis/bldg/schemas/iur/uro/3.2/urbanObject.xsd`
- Local analysis reports: `/home/kellyrsch/mscthesis/hachioji_bldg_ade_attribute_analysis_v3.md` and `/home/kellyrsch/mscthesis/takeshiba_bldg_ade_attribute_analysis_v3.md`
