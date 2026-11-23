# PLATEAU Building ADE (`uro`) Attribute Descriptions

**Source:** [3D都市モデル標準製品仕様書 — 4.2.3.2 bldg:Buildingの拡張属性](https://www.mlit.go.jp/plateaudocument/toc4/toc4_02/toc4_02_03/toc4_02_03_02/)

This document lists the `uro` attributes defined for `bldg:Building` and translates the Japanese `定義` (definition) column into English. Attribute names, codelist filenames, units, and technical identifiers are retained as in the source. Translations are working translations; consult the Japanese specification for authoritative wording.

Prompt: 
> Could you translate a bigger part of the documentation for me? Specifically section "4.2.3.2 bldg:Buildingの拡張属性" on https://www.mlit.go.jp/plateaudocument/toc4/toc4_02/toc4_02_03/toc4_02_03_02/? I mostly want the tables for each subsection with attribute names and then a translated description (what is in the columns with name "定義"). And can you write it to a markdown file in the same folder as before with filename "PLATEAU_attribute_descriptions.md"? It should contain all attributes in the tables from: BuildingIDAttribute, BuildingDetailAttribute, LargeCustomerFacilityAttribute, RiverFloodingRiskAttribute, LandSlideRiskAttribute, KeyValuePairAttribute, DataQualityAttribute, PublicSurveyDataQualityAttribute, and RealEstateIDAttribute. So just the firt columns ("属性名") and the translated last columns ("定義").

---

## 4.2.3.2.1 `uro:BuildingIDAttribute`

**Type definition:** Information for identifying a building.

| Attribute | Definition (English translation) |
|---|---|
| `uro:buildingID` | Number for identifying the principal building. Mandatory. Format: `[municipality code]-[prefix]-[object serial number]`. The municipality code is the code of the municipality in which the feature is located. Do not omit leading zeros; write as 5 digits. The prefix is a 3- or 4-digit code indicating the feature type; for buildings, use `bldg`. The object serial number is a sequence of half-width digits. |
| `uro:branchID` | Number for identifying a building attached to the principal building. |
| `uro:partID` | Number for identifying a building part when the principal building is described as multiple `bldg:BuildingPart`s. Mandatory for `bldg:BuildingPart`. |
| `uro:prefecture` | Prefecture code of the prefecture in which the building is located. Two-digit half-width number defined in JIS X0401. Select from the codelist (`Common_localPublicAuthorities.xml`). |
| `uro:city` | Municipality code of the municipality in which the building is located. Five-digit half-width number combining the 2-digit number defined in JIS X0401 and the 3-digit number defined in JIS X0402. For designated cities, use the ward's municipality code. Select from the codelist (`Common_localPublicAuthorities.xml`). Although i-UR defines the multiplicity as [0..1], it is mandatory in the Standard Product Specification because it is used to determine the building's location. |

---

## 4.2.3.2.2 `uro:BuildingDetailAttribute`

**Type definition:** Basic information about buildings collected in the Urban Planning Basic Survey conducted under the City Planning Act.

| Attribute | Definition (English translation) |
|---|---|
| `uro:serialNumberOfBuildingCertification` | Building confirmation application number. |
| `uro:siteArea` | Area of the site on which the building is located. Unit: m2 (uom="m2"). |
| `uro:totalFloorArea` | Total floor area of each floor of the building. Unit: m2 (uom="m2"). |
| `uro:buildingFootprintArea` | Horizontal projected area of the part enclosed by the center lines of the building's walls and columns. Unit: m2 (uom="m2"). |
| `uro:buildingRoofEdgeArea` | Horizontal projected area of the building including the roof. Unit: m2 (uom="m2"). |
| `uro:developmentArea` | Developed area. Unit: m2 (uom="m2"). |
| `uro:buildingStructureType` | Structural type. Select from the codelist (`BuildingDetailAttribute_buildingStructureType.xml`). |
| `uro:buildingStructureOrgType` | Building structural type based on a municipality-specific classification. Select from the codelist (`BuildingDetailAttribute_buildingStructureOrgType.xml`). Create a codelist if this attribute is used. |
| `uro:fireproofStructureType` | Fireproof structure classification. Select from the codelist (`BuildingDetailAttribute_fireproofStructureType.xml`). |
| `uro:implementingBody` | Name of the entity that implemented the building construction. |
| `uro:urbanPlanType` | Classification of the urban planning area to which the land on which the building is located belongs. Select from the codelist (`Common_urbanPlanType.xml`). |
| `uro:areaClassificationType` | Area classification of the land on which the building is located. Select from the codelist (`Common_areaClassificationType.xml`). |
| `uro:districtsAndZonesType` | District/zone classification of the land on which the building is located. Select from the codelist (`Common_districtsAndZonesType.xml`). If the building is included in multiple districts/zones, list multiple values. |
| `uro:landUseType` | Land use classification of the land on which the building is located. Select from the codelist (`Common_landUseType.xml`). |
| `uro:reference` | Number on the drawing indicating the building's position. |
| `uro:majorUsage` | Municipality-specific classification using a coarser category than `urf:orgUsage`. Select from the codelist (`BuildingDetailAttribute_majorUsage.xml`). Create a codelist if this attribute is used. |
| `uro:majorUsage2` | Municipality-specific classification that is coarser than `uro:orgUsage` and finer than `uro:majorUsage`. Select from the codelist (`BuildingDetailAttribute_majorUsage2.xml`). Create a codelist if this attribute is used. |
| `uro:orgUsage` | Municipality-specific classification corresponding to the "use classification" of buildings shown in the Urban Planning Basic Survey Implementation Guidelines (Ministry of Land, Infrastructure, Transport and Tourism, Urban Bureau). Select from the codelist (`BuildingDetailAttribute_orgUsage.xml`). Create a codelist if this attribute is used. |
| `uro:orgUsage2` | Municipality-specific classification corresponding to the detailed categories for commercial facilities, educational/cultural/health facilities, transportation/warehouse facilities, and factories within the "use classification" shown in the Urban Planning Basic Survey Implementation Guidelines. Select from the codelist (`BuildingDetailAttribute_orgUsage2.xml`). Create a codelist if this attribute is used. |
| `uro:detailedUsage` | Municipality-specific classification using a finer category than `uro:orgUsage2`. Select from the codelist (`BuildingDetailAttribute_detailedUsage.xml`). If this attribute is used, modify the codelist shown in this product specification as necessary. |
| `uro:detailedUsage2` | Municipality-specific classification using a finer category than `uro:detailedUsage`. Select from the codelist (`BuildingDetailAttribute_detailedUsage2.xml`). Create a codelist if this attribute is used. |
| `uro:detailedUsage3` | Municipality-specific classification using a finer category than `uro:detailedUsage2`. Select from the codelist (`BuildingDetailAttribute_detailedUsage3.xml`). Create a codelist if this attribute is used. |
| `uro:groundFloorUsage` | Use of the building's first floor based on a municipality-specific classification. Select from the codelist (`BuildingDetailAttribute_groundFloorUsage.xml`). Create a codelist if this attribute is used. |
| `uro:secondFloorUsage` | Use of the building's second floor or higher based on a municipality-specific classification. Select from the codelist (`BuildingDetailAttribute_secondFloorUsage.xml`). Create a codelist if this attribute is used. |
| `uro:thirdFloorUsage` | Use of the building's third floor or higher based on a municipality-specific classification. Select from the codelist (`BuildingDetailAttribute_thirdFloorUsage.xml`). Create a codelist if this attribute is used. |
| `uro:basementUsage` | Use of the building's basement based on a municipality-specific classification. Select from the codelist (`BuildingDetailAttribute_basementFloorUsage.xml`). Create a codelist if this attribute is used. |
| `uro:basementFirstUsage` | Use of the building's first basement floor based on a municipality-specific classification. Select from the codelist (`BuildingDetailAttribute_basementFirstUsage.xml`). Create a codelist if this attribute is used. |
| `uro:basementSecondUsage` | Use of the building's second basement floor based on a municipality-specific classification. Select from the codelist (`BuildingDetailAttribute_basementSecondUsage.xml`). Create a codelist if this attribute is used. |
| `uro:vacancy` | Whether the building is vacant. Select from the codelist (`BuildingDetailAttribute_vacancy.xml`). |
| `uro:buildingCoverageRate` | Building coverage ratio (ratio of building area to site area). Write as a percentage where the whole is 100. Unit: %. |
| `uro:floorAreaRate` | Floor area ratio (ratio of total floor area to site area). Write as a percentage where the whole is 100. Unit: %. |
| `uro:specifiedBuildingCoverageRate` | Designated building coverage ratio (building coverage ratio specified for each use district). Write as a percentage where the whole is 100. Unit: %. |
| `uro:specifiedFloorAreaRate` | Designated floor area ratio (maximum floor area ratio specified in urban planning). Write as a percentage where the whole is 100. Unit: %. |
| `uro:standardFloorAreaRate` | Standard floor area ratio (floor area ratio calculated based on the limit imposed by the width of the front road when the front road width is less than 12 m). Write as a percentage where the whole is 100. Unit: %. |
| `uro:buildingHeight` | Height of the building from the ground surface as defined in Article 2 of the Enforcement Order of the Building Standards Act. Unit: m (uom="m"). |
| `uro:eaveHeight` | Height from the ground surface to the eaves beam of the building as defined in Article 2 of the Enforcement Order of the Building Standards Act. Unit: m (uom="m"). |
| `uro:note` | Other matters worthy of special mention regarding the building. |
| `uro:surveyYear` | Year (in the Western calendar) in which the building use survey was conducted. |

---

## 4.2.3.2.3 `uro:LargeCustomerFacilityAttribute`

**Type definition:** Basic information about large retail stores and large customer-attraction facilities collected in the Urban Planning Basic Survey conducted under the City Planning Act.

| Attribute | Definition (English translation) |
|---|---|
| `uro:class` | Type of customer-attraction facility. Select from the codelist (`LargeCustomerFacilityAttribute_class.xml`). |
| `uro:name` | Name of the customer-attraction facility. |
| `uro:capacity` | Capacity of the customer-attraction facility (for hospitals, the number of beds; for universities, etc., the number of students). |
| `uro:owner` | Name of the facility owner. |
| `uro:totalFloorArea` | Total floor area of all floors of the customer-attraction facility. Unit: m2 (uom="m2"). |
| `uro:totalStoreFloorArea` | Total store floor area of all floors of the customer-attraction facility. Unit: m2 (uom="m2"). |
| `uro:inauguralDate` | Date on which the customer-attraction facility began operation. |
| `uro:yearOpened` | Year of opening. |
| `uro:yearClosed` | Year of closure. |
| `uro:keyTenants` | Names of the main tenants when the customer-attraction facility is a commercial facility. |
| `uro:availability` | Whether the customer-attraction facility has the scale of a tertiary medical service area, when the facility is a medical facility. |
| `uro:urbanPlanType` | Classification of the urban planning area to which the land on which the customer-attraction facility is located belongs. Select from the codelist (`Common_urbanPlanType.xml`). |
| `uro:areaClassificationType` | Area classification of the land on which the customer-attraction facility is located. Select from the codelist (`Common_areaClassificationType.xml`). |
| `uro:districtsAndZonesType` | District/zone classification of the land on which the customer-attraction facility is located. Select from the codelist (`Common_districtsAndZonesType.xml`). If the land is included in multiple districts/zones, list multiple values. |
| `uro:landUseType` | Land use classification of the land on which the customer-attraction facility is located. Select from the codelist (`Common_landUseType.xml`). |
| `uro:reference` | Drawing reference number. Number on the drawing indicating the location of the customer-attraction facility. |
| `uro:note` | Other matters worthy of special mention regarding the customer-attraction facility. |
| `uro:surveyYear` | Year (in the Western calendar) in which the customer-attraction facility location survey was conducted. |

---

## 4.2.3.2.4 `uro:RiverFloodingRiskAttribute`

**Type definition:** An attribute type for assigning the attributes of a flood inundation assumption zone to a building located within that zone. If a building straddles multiple zones in the same flood inundation assumption zone map, meshes with the same inundation rank are treated as one zone, and the inundation rank value of the zone with the largest overlapping area with the building is used (if the areas are equal, the zone with the more dangerous inundation rank is used). For the inundation depth, adopt the inundation depth of the mesh with the largest overlapping area with the building among the meshes having the adopted inundation rank (meshes with the same inundation depth are summed when calculating the area). For the inundation duration, adopt the inundation duration of the inundation duration mesh overlapping the adopted inundation depth mesh; if multiple inundation duration meshes overlap, adopt the largest inundation duration value. The number of significant digits for inundation depth follows the "Guideline for Digitization of Flood Inundation Assumption Zone Data (4th Edition)"; up to 3 decimal places may be registered, but 2 decimal places are also acceptable. The number of significant digits for area shall be 2 decimal places (rounded at the 3rd decimal place).

| Attribute | Definition (English translation) |
|---|---|
| `uro:description` | For flood inundation assumption zones: name of the designated river. Select from the codelist (`RiverFloodingRiskAttribute_description.xml`). Create a codelist for each municipality. The designated river name should basically use the "water system name" and "designated river name" indicated as a flood forecast river or water-level notification river subject to the flood inundation assumption zone map designated under the Flood Prevention Act. If a single inundation assumption zone map includes multiple flood forecast rivers or water-level notification rivers, list the "designated river names". When listing designated river names, use "・" (full-width middle dot) as the separator. For inundation area maps independently prepared by prefectures, use a name indicating the target area from the name of the relevant inundation assumption zone. |
| `uro:rank` | Classification according to inundation depth (for tsunami inundation assumptions, "water level"). Either `uro:rank` or `uro:rankOrg` is provided. For flood inundation assumption zones, select from the codelist (`RiverFloodingRiskAttribute_rank.xml`). For tsunami inundation assumptions, the water level uses the "tsunami reference water level" if available; otherwise, the water level related to the depth specified in the tsunami inundation assumption. |
| `uro:rankOrg` | Classification according to inundation depth (for tsunami inundation assumptions, "water level") independently set by municipalities, etc. Either `uro:rank` or `uro:rankOrg` is provided. For flood inundation assumption zones, select from the codelist (`RiverFloodingRiskAttribute_rankOrg.xml`). |
| `uro:depth` | Inundation depth. For tsunami inundation assumptions, storm surge inundation assumption zones, inland flooding assumption zones, and reservoir hazard maps, the height from the ground to the water surface when the water surface reaches the highest position at each point on land. Unit: m (uom="m"). |
| `uro:adminType` | Type of organization that designated the flood forecast river or water-level notification river. Select from the codelist (`RiverFloodingRiskAttribute_adminType.xml`). |
| `uro:scale` | Classification of whether the data was created based on maximum expected rainfall or planned-scale rainfall. Select from the codelist (`RiverFloodingRiskAttribute_scale.xml`). |
| `uro:duration` | Duration for which inundation continues. Unit: hour (uom="hour"). |

---

## 4.2.3.2.9 `uro:LandSlideRiskAttribute`

**Type definition:** Assigns as an attribute which zone a structure located in a landslide hazard area or landslide special hazard area is included in. If multiple "zone classifications" overlap for one urban object, assign only the zone classification with the highest priority based on the following priority order (highest first): landslide special hazard area (designated), landslide hazard area (designated), landslide special hazard area (pre-designation), landslide hazard area (pre-designation). If multiple "phenomenon classifications" overlap for one building, describe each as a landslide risk attribute.

| Attribute | Definition (English translation) |
|---|---|
| `uro:description` | For landslide hazard areas: the type of disaster expected to occur. Select from the codelist (`LandSlideRiskAttribute_description.xml`). |
| `uro:areaType` | Zone classification of the landslide hazard area. Select from the codelist (`LandSlideRiskAttribute_areaType.xml`). |

---

## 4.2.3.2.10 `uro:KeyValuePairAttribute`

**Type definition:** Additional information assigned to an urban object. Used when adding code-type attributes other than those inherited by or defined for the urban object. Consists of pairs of attribute names and attribute values. To add attributes other than code values, use `gen:_GenericAttribute`.

| Attribute | Definition (English translation) |
|---|---|
| `uro:key` | Name of the attribute to be extended. Create and select from a codelist (`KeyValuePairAttribute_key.xml`). |
| `uro:codeValue` | Value of the extended attribute. Create and select from a codelist (`KeyValuePairAttribute_key[key].xml`). `[key]` matches the value of the attribute `uro:key`. |

---

## 4.2.3.2.11 `uro:DataQualityAttribute`

**Type definition:** Data type for describing the quality of an urban object.

| Attribute | Definition (English translation) |
|---|---|
| `uro:geometrySrcDescLod0` | Type of source material used to create the LOD0 geometric object. Select from the codelist (`DataQualityAttribute_geometrySrcDesc.xml`). Mandatory when LOD0 geometric objects are within the scope of the extended product specification. In this case, even if the specific urban object does not contain an LOD0 geometric object, select code "999" indicating "not created" (for example, even if LOD0 geometric objects are created only for part of the area in a building model and the target urban object contains only LOD1 geometric objects, the value of this attribute for that urban object is "999"). |
| `uro:geometrySrcDescLod1` | Type of source material used to create the LOD1 geometric object. Select from the codelist (`DataQualityAttribute_geometrySrcDesc.xml`). Even if the specific urban object does not contain an LOD1 geometric object, select code "999" indicating "not created". |
| `uro:geometrySrcDescLod2` | Type of source material used to create the LOD2 geometric object. Select from the codelist (`DataQualityAttribute_geometrySrcDesc.xml`). Mandatory when LOD2 geometric objects are within the scope of the extended product specification. In this case, even if the specific urban object does not contain an LOD2 geometric object, select code "999" indicating "not created". |
| `uro:geometrySrcDescLod3` | Type of source material used to create the LOD3 geometric object. Select from the codelist (`DataQualityAttribute_geometrySrcDesc.xml`). Mandatory when LOD3 geometric objects are within the scope of the extended product specification. In this case, even if the specific urban object does not contain an LOD3 geometric object, select code "999" indicating "not created". |
| `uro:geometrySrcDescLod4` | Type of source material used to create the LOD4 geometric object. Select from the codelist (`DataQualityAttribute_geometrySrcDesc.xml`). Mandatory when LOD4 geometric objects are within the scope of the extended product specification. In this case, even if the specific urban object does not contain an LOD4 geometric object, select code "999" indicating "not created". |
| `uro:thematicSrcDesc` | Type of source material used to create the thematic attributes. Select from the codelist (`DataQualityAttribute_thematicSrcDesc.xml`). Mandatory when thematic attributes are within the scope. |
| `uro:appearanceSrcDescLod0` | Type of source material used for the appearance of the LOD0 geometric object. Select from the codelist (`DataQualityAttribute_appearanceSrcDesc.xml`). Mandatory when the appearance of LOD0 geometric objects is within the scope of the extended product specification. In this case, even if the specific urban object does not contain an appearance for an LOD0 geometric object, select code "99" indicating "not created". |
| `uro:appearanceSrcDescLod1` | Type of source material used for the appearance of the LOD1 geometric object. Select from the codelist (`DataQualityAttribute_appearanceSrcDesc.xml`). Mandatory when the appearance of LOD1 geometric objects is within the scope of the extended product specification. In this case, even if the specific urban object does not contain an appearance for an LOD1 geometric object, select code "99" indicating "not created". |
| `uro:appearanceSrcDescLod2` | Type of source material used for the appearance of the LOD2 geometric object. Select from the codelist (`DataQualityAttribute_appearanceSrcDesc.xml`). Mandatory when the appearance of LOD2 geometric objects is within the scope of the extended product specification. In this case, even if the specific urban object does not contain an appearance for an LOD2 geometric object, select code "99" indicating "not created". |
| `uro:appearanceSrcDescLod3` | Type of source material used for the appearance of the LOD3 geometric object. Select from the codelist (`DataQualityAttribute_appearanceSrcDesc.xml`). Mandatory when the appearance of LOD3 geometric objects is within the scope of the extended product specification. In this case, even if the specific urban object does not contain an appearance for an LOD3 geometric object, select code "99" indicating "not created". |
| `uro:appearanceSrcDescLod4` | Type of source material used for the appearance of the LOD4 geometric object. Select from the codelist (`DataQualityAttribute_appearanceSrcDesc.xml`). Mandatory when the appearance of LOD4 geometric objects is within the scope of the extended product specification. In this case, even if the specific urban object does not contain an appearance for an LOD4 geometric object, select code "99" indicating "not created". |
| `uro:lodType` | Detailed classification of the LOD applied to the geometric object. For buildings: select from the codelist (`Building_lodType.xml`); mandatory when creating LOD2 or higher geometric objects. For roads, pedestrian paths, or plazas: select from `Road_lodType.xml`; mandatory when creating LOD3 geometric objects. For railways: select from `Railway_lodType.xml`; mandatory when creating LOD3 geometric objects. For feature types for which LOD subdivisions are not defined: do not use this attribute. |
| `uro:lod1HeightType` | Height calculation method used when creating the LOD1 solid geometry. Select from the codelist (`DataQualityAttribute_lod1HeightType.xml`). |
| `uro:tranDataAcquisition` | Attribute for describing the "acquisition level" defined in the "Road Base Map Information (Development Promotion Edition) Product Specification (Draft) (May 2015)". Used only for roads. |
| `uro:publicSurveyDataQualityAttribute` *(related role)* | Map information level and type of the public survey results or basic survey results used. Mandatory when the code value of the attribute concerning the type of source material used to create the geometric object of each LOD (`uro:geometrySrcDescLod0`, etc.) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is public survey results or basic survey results (code "000"). |

---

## 4.2.3.2.12 `uro:PublicSurveyDataQualityAttribute`

**Type definition:** Data type for describing data creation information of an urban object.

| Attribute | Definition (English translation) |
|---|---|
| `uro:srcScaleLod0` | Map information level of the source material used to create the LOD0 geometric object. Select from the codelist (`PublicSurveyDataQualityAttribute_srcScale.xml`). Mandatory when the code value of the attribute concerning the type of source material used to create the LOD0 geometric object (`uro:geometrySrcDescLod0`) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is only public survey results or basic survey results (code "000"). |
| `uro:srcScaleLod1` | Map information level of the source material used to create the LOD1 geometric object. Select from the codelist (`PublicSurveyDataQualityAttribute_srcScale.xml`). Mandatory when the code value of the attribute concerning the type of source material used to create the LOD1 geometric object (`uro:geometrySrcDescLod1`) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is only public survey results or basic survey results (code "000"). |
| `uro:srcScaleLod2` | Map information level of the source material used to create the LOD2 geometric object. Select from the codelist (`PublicSurveyDataQualityAttribute_srcScale.xml`). Mandatory when the code value of the attribute concerning the type of source material used to create the LOD2 geometric object (`uro:geometrySrcDescLod2`) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is only public survey results or basic survey results (code "000"). If multiple map information levels are mixed, record the lowest map information level. For example, if walls are at map information level 1000 and roof surfaces at 2500, use 2500. |
| `uro:srcScaleLod3` | Map information level of the source material used to create the LOD3 geometric object. Select from the codelist (`PublicSurveyDataQualityAttribute_srcScale.xml`). Mandatory when the code value of the attribute concerning the type of source material used to create the LOD3 geometric object (`uro:geometrySrcDescLod3`) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is only public survey results or basic survey results (code "000"). If multiple map information levels are mixed, record the lowest map information level. For example, if walls are at map information level 1000 and roof surfaces at 2500, use 2500. |
| `uro:srcScaleLod4` | Map information level of the source material used to create the LOD4 geometric object. Select from the codelist (`PublicSurveyDataQualityAttribute_srcScale.xml`). Mandatory when the code value of the attribute concerning the type of source material used to create the LOD4 geometric object (`uro:geometrySrcDescLod4`) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is only public survey results or basic survey results (code "000"). If multiple map information levels are mixed, record the lowest map information level. For example, if the outer shape is at map information level 1000 and the indoor shape at 500, use 1000. |
| `uro:publicSurveySrcDescLod0` | Type of source material used to create the LOD0 geometric object. Select from the codelist (`PublicSurveyDataQualityAttribute_geometrySrcDesc.xml`). Mandatory when the code value of the attribute concerning the type of source material used to create the LOD0 geometric object (`uro:geometrySrcDescLod0`) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is only public survey results or basic survey results (code "000"). If multiple types of source material are used, describe each. |
| `uro:publicSurveySrcDescLod1` | Type of source material used to create the LOD1 geometric object. Select from the codelist (`PublicSurveyDataQualityAttribute_geometrySrcDesc.xml`). Mandatory when the code value of the attribute concerning the type of source material used to create the LOD1 geometric object (`uro:geometrySrcDescLod1`) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is only public survey results or basic survey results (code "000"). If multiple types of source material are used, describe each. |
| `uro:publicSurveySrcDescLod2` | Type of source material used to create the LOD2 geometric object. Select from the codelist (`PublicSurveyDataQualityAttribute_geometrySrcDesc.xml`). Mandatory when the code value of the attribute concerning the type of source material used to create the LOD2 geometric object (`uro:geometrySrcDescLod2`) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is only public survey results or basic survey results (code "000"). If multiple types of source material are used, describe each. |
| `uro:publicSurveySrcDescLod3` | Type of source material used to create the LOD3 geometric object. Select from the codelist (`PublicSurveyDataQualityAttribute_geometrySrcDesc.xml`). Mandatory when the code value of the attribute concerning the type of source material used to create the LOD3 geometric object (`uro:geometrySrcDescLod3`) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is only public survey results or basic survey results (code "000"). If multiple types of source material are used, describe each. |
| `uro:publicSurveySrcDescLod4` | Type of source material used to create the LOD4 geometric object. Select from the codelist (`PublicSurveyDataQualityAttribute_geometrySrcDesc.xml`). Mandatory when the code value of the attribute concerning the type of source material used to create the LOD4 geometric object (`uro:geometrySrcDescLod4`) (selected from `DataQualityAttribute_geometrySrcDesc.xml`) is only public survey results or basic survey results (code "000"). If multiple types of source material are used, describe each. |

---

## 4.2.3.2.13 `uro:RealEstateIDAttribute`

**Type definition:** Data type for assigning, as building attributes, the real estate IDs linked to the land on which the building exists and to the building. A real estate ID is a "common code for each real estate that can uniquely identify the real estate" (Real Estate ID Rule Guidelines).

| Attribute | Definition (English translation) |
|---|---|
| `uro:realEstateIDOfBuilding` | Real estate ID assigned to the "entire building" of the building. Recorded as "13-digit real estate number + '-' (hyphen) + 4 digits" based on the Real Estate ID Rule Guidelines (Ministry of Land, Infrastructure, Transport and Tourism). |
| `uro:numberOfBuildingUnitOwnership` | Number of unit ownerships of the building when the building is a condominium (divided ownership). |
| `uro:realEstateIDOfBuildingUnitOwnership` | List of real estate IDs of each exclusive part of the building when the building is a condominium. Recorded as "13-digit real estate number + '-' (hyphen) + 4 digits" based on the Real Estate ID Rule Guidelines (MLIT). |
| `uro:numberOfRealEstateIDOfLand` | Number of parcels of land (lots) on which the building is located. |
| `uro:realEstateIDOfLand` | Real estate ID of the land on which the building is located. Recorded as "13-digit real estate number + '-' (hyphen) + 4 digits" based on the Real Estate ID Rule Guidelines (MLIT). If the building spans multiple parcels, follow the order of the lot numbers listed in the "location" column of the registry linked to the building. |
| `uro:matchingScore` | When using the "dt23-03 3D City Model / Real Estate ID Matching System" developed by Project PLATEAU in FY2023 to assign real estate IDs to buildings, because a probabilistic matching method is used, the degree of agreement between the spatial and thematic attributes of the building and the parcel to which the registry data is assigned is scored. `uro:matchingScore` represents that value. Mandatory when using the "dt23-03 3D City Model / Real Estate ID Matching System". The score is calculated by converting the larger of the total scores (out of 300) of the three items "①, ② and ④" or "①, ③ and ④" among the four items ① to ④ below into a score out of 100. ① Overlap score: the overlap ratio (%) of the two-dimensional spatial attributes of the land listed in the "location" column of the registry linked to the building and the building projected onto the land. ② Floor-count score: when the building holds its above-ground floor count in the `bldg:storeysBelowGround` attribute, the degree of agreement between the above-ground floor count calculated from the "floor area" column of the registry linked to the building and the building's above-ground floor count; 100 points if they match, 0 points if they do not. ③ Building height score: the degree of agreement between the height converted from the above-ground floor count calculated from the "floor area" column of the registry linked to the building and the measured height of the building (`bldg:measuredHeight`). ④ Floor area score: the degree of agreement between the maximum floor area among the floor areas of each floor calculated from the "floor area" column of the registry linked to the building and the building's graphic area; if the building has the `uro:buildingFootprintArea` attribute, compare with the area calculated from the registry and give 100 points if they match in m2, otherwise calculate according to the formula in the source. See the source page for the detailed scoring formulas and diagrams. |
