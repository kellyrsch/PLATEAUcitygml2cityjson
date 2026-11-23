# PLATEAU CityGML 2.0 → 3.0 comparison

Comparison of the two files in `C:\Users\Kelly\Documents\Geomatics\MSc_Thesis\A2_Midterm\misc_experiments\Existing PLATEAU CityGML3`
(WSL path: `/mnt/c/Users/Kelly/Documents/Geomatics/MSc_Thesis/A2_Midterm/misc_experiments/Existing PLATEAU CityGML3/`).

Prompt: 
> Hi, could you compare the two CityGML files in this folder: "C:\Users\Kelly\Documents\Geomatics\MSc_Thesis\A2_Midterm\misc_experiments\Existing PLATEAU CityGML3"? And could you write down exactly what changed between the two? I know it got upgraded from CityGML 2.0 to CityGML 3.0, but I want to know how things got mapped exactly and what the upgrade entails exactly. Could you write your findings to a markdown file in the same folder with filename "PLATEAU_CityGML23_comparison.md"?

[https://github.com/opengeospatial/CityGML3.0-GML-Encoding/tree/main/resources/examples/ADE-examples/Urban-Planning-ADE]

## 1. Scope and files

| | CityGML 2.0 file | CityGML 3.0 file |
|---|---|---|
| Filename | `53394517_bldg_6697_2_op_CityGML2.gml` | `53394517_bldg_6697_2_op_CityGML3.gml` |
| Size | 1,209,648 bytes | 1,236,041 bytes |
| Lines | 20,297 | 22,773 |
| Root | `core:CityModel` (core 2.0) | `core:CityModel` (core 3.0) |
| Buildings | 1 | 1 |
| Building ID | `BLD_77ca1a15-3b35-4386-8f86-152ed71c4c64` | identical |
| Building ID attribute (`建物ID`) | `13104-bldg-53` | identical |
| Envelope | `35.67463773337496 139.71176683323012 16.472` → `35.683632435821664 139.72503585352985 89.518`, EPSG:6697, 3D | identical |

Both files describe exactly the same single building and the same geometry (verified: all 785 `gml:posList` value strings are identical, all 1,951 `gml:id` values are identical, all 650 `xlink:href` values are identical). The upgrade is a **schema/encoding migration**, not a re-measurement or re-modelling of the object.

## 2. Summary of what changed

1. Every namespace URI was swapped to its 3.0 / GML 3.2 / xAL 3 equivalent, and a new `con` (construction) namespace was introduced.
2. LOD properties moved from the building namespace to the core namespace; the boundary-surface hierarchy moved from `bldg:*` to `con:*` and from `bldg:boundedBy` to `core:boundary`.
3. GML 3.1's `gml:CompositeSurface` became GML 3.2's `gml:Shell`.
4. The measured height was remodeled from a simple measure into a structured `con:Height` object.
5. Generic attributes were rewrapped (`core:genericAttribute` → `gen:StringAttribute` with a `gen:name` child instead of a `name` attribute).
6. PLATEAU's URO ADE attributes were moved into the mandatory CityGML 3 ADE container `bldg:adeOfAbstractBuilding/uro:BuildingProperties`, and the URO namespace URI changed from version 1.5 to 1.4 with a different authority.
7. The address moved from xAL 2 (`AddressDetails`/`CountryName`/`LocalityName`) to xAL 3 (`Address`/`NameElement`).
8. Appearance was restructured (`textureParameterization`/`TextureAssociation` wrappers, references moved from XML attributes to element text) and the duplicated texture-coordinate lists were collapsed (1298 → 649).
9. Child-element order inside `bldg:Building` changed.

## 3. Namespace and schema header mapping

| Prefix | CityGML 2.0 file | CityGML 3.0 file |
|---|---|---|
| `gml` | `http://www.opengis.net/gml` (GML 3.1.1) | `http://www.opengis.net/gml/3.2` |
| `core` | `http://www.opengis.net/citygml/2.0` | `http://www.opengis.net/citygml/3.0` |
| `bldg` | `http://www.opengis.net/citygml/building/2.0` | `http://www.opengis.net/citygml/building/3.0` |
| `gen` | `http://www.opengis.net/citygml/generics/2.0` | `http://www.opengis.net/citygml/generics/3.0` |
| `app` | `http://www.opengis.net/citygml/appearance/2.0` | `http://www.opengis.net/citygml/appearance/3.0` |
| `con` | *(absent)* | `http://www.opengis.net/citygml/construction/3.0` **(new)** |
| `uro` | `https://www.chisou.go.jp/tiiki/toshisaisei/itoshisaisei/iur/uro/1.5` | `http://www.kantei.go.jp/jp/singi/tiiki/toshisaisei/itoshisaisei/iur/uro/1.4` |
| `xAL` | `urn:oasis:names:tc:ciq:xsdschema:xAL:2.0` | `urn:oasis:names:tc:ciq:xal:3` |
| `xlink` | `http://www.w3.org/1999/xlink` | identical |
| `xsi` | `http://www.w3.org/2001/XMLSchema-instance` | identical |

`xsi:schemaLocation` also changed:

- **2.0:** remote PLATEAU `uro/1.5/urbanObject.xsd` plus `schemas.opengis.net` URLs for `building.xsd`, `generics.xsd`, `appearance.xsd`.
- **3.0:** local `./urbanObject_CityGML3.xsd` (URO 1.4), `../../../../standard/Schema/{building,generics,appearance}.xsd`, plus the GML 3.2.1 schema `http://schemas.opengis.net/gml/3.2.1/gml.xsd`.

## 4. Exact element-by-element mapping

### 4.1 Generic attributes (3 occurrences)

| CityGML 2.0 | CityGML 3.0 |
|---|---|
| `gen:stringAttribute name="建物ID"` → `gen:value` | `core:genericAttribute` → `gen:StringAttribute` → `gen:name` + `gen:value` |
| `gen:stringAttribute name="大字・町コード"` → `gen:value` | same pattern |
| `gen:stringAttribute name="13_区市町村コード_大字・町コード_町・丁目コード"` → `gen:value` | same pattern |

The `name` XML **attribute** became a `gen:name` **child element**; the strings and values (`13104-bldg-53`, `29`, `13104029000`) are unchanged.

### 4.2 Height

| CityGML 2.0 | CityGML 3.0 |
|---|---|
| `<bldg:measuredHeight uom="m">31.7</bldg:measuredHeight>` | `<con:height><con:Height><con:highReference>generalRoof</con:highReference><con:lowReference>lowestGroundPoint</con:lowReference><con:status>measured</con:status><con:value uom="urn:adv:uom:m">31.7</con:value></con:Height></con:height>` |

The numeric value is unchanged; the new structure adds explicit reference levels and a `measured` status. The UOM changed from the plain `m` to the URN form `urn:adv:uom:m`. In CityGML 3 height is inherited from the `Construction` module (`con:`), which `bldg:Building` now specializes.

### 4.3 LOD geometry and boundary surfaces

| CityGML 2.0 | CityGML 3.0 | Note |
|---|---|---|
| `bldg:lod0RoofEdge` | `core:lod0MultiSurface` | LOD0 property moved to `core:`; geometrically identical roof-edge `MultiSurface`. |
| `bldg:lod1Solid` | `core:lod1Solid` | Same Solid, 134 surface members, identical coordinates. |
| `bldg:lod2Solid` | `core:lod2Solid` | Same Solid, 650 surface members, identical coordinates. |
| `gml:CompositeSurface` (inside both Solids) | `gml:Shell` | GML 3.2 renamed/replaced the aggregate; same members. |
| `bldg:boundedBy` (650×) | `core:boundary` (650×) | Boundary property moved to `core:`. |
| `bldg:GroundSurface` | `con:GroundSurface` | Boundary surfaces moved to the construction module. |
| `bldg:RoofSurface` (279×) | `con:RoofSurface` (279×) | Identical IDs and geometry. |
| `bldg:WallSurface` (370×) | `con:WallSurface` (370×) | Identical IDs and geometry. |
| `bldg:lod2MultiSurface` (on each boundary surface) | `core:lod2MultiSurface` | LOD property moved to `core:`. |
| `gml:Polygon`, `gml:LinearRing`, `gml:MultiSurface`, `gml:exterior`, `gml:posList`, `gml:surfaceMember` | identical | All GML geometry payloads are unchanged as values. |

The 650 `gml:surfaceMember xlink:href="#poly_STAD0158_…"` references in `lod2Solid` point to the same polygons in both files. In 2.0 these are written with the `xlink:href` prefix; in 3.0 the same attribute is retained (the XML namespace is the same) but the containing aggregate is `gml:Shell`.

### 4.4 URO ADE attributes

| CityGML 2.0 | CityGML 3.0 |
|---|---|
| `uro:buildingDetails` directly under `bldg:Building` | `bldg:adeOfAbstractBuilding` → `uro:BuildingProperties` → `uro:buildingDetails` |
| `uro:extendedAttribute` directly under `bldg:Building` (3×) | inside the same `uro:BuildingProperties` container (3×) |

Contents are otherwise unchanged: `uro:BuildingDetails` still holds `buildingRoofEdgeArea uom="m2"` = `2513.85520`, `districtsAndZonesType` = `4`, `prefecture` = `13`, `city` = `13104`, `surveyYear` = `2016`; the three `uro:KeyValuePair`s still hold key/codeValue pairs `2/2`, `105/2`, `106/20`. The only textual differences are the `codeSpace` paths, shortened from `../../codelists/…` to `../codelists/…`, and the URO namespace URI/authority change (1.5 → 1.4). CityGML 3 requires ADE content to be carried in an explicit ADE container element, which is why the wrapper was added.

### 4.5 Address (xAL 2 → xAL 3)

**CityGML 2.0:**
```xml
<bldg:address>
  <core:Address>
    <core:xalAddress>
      <xAL:AddressDetails>
        <xAL:Country>
          <xAL:CountryName>日本</xAL:CountryName>
          <xAL:Locality>
            <xAL:LocalityName Type="Town">東京都新宿区霞ヶ丘町</xAL:LocalityName>
          </xAL:Locality>
        </xAL:Country>
      </xAL:AddressDetails>
    </core:xalAddress>
  </core:Address>
</bldg:address>
```

**CityGML 3.0:**
```xml
<bldg:address>
  <core:Address>
    <core:xalAddress>
      <xAL:Address>
        <xAL:Country>
          <xAL:NameElement>日本</xAL:NameElement>
        </xAL:Country>
        <xAL:Locality xAL:Type="Town">
          <xAL:NameElement xAL:NameType="Name">東京都新宿区霞ヶ丘町</xAL:NameElement>
        </xAL:Locality>
      </xAL:Address>
    </core:xalAddress>
  </core:Address>
</bldg:address>
```

Mapping: `AddressDetails` → `Address` (and `Country`/`Locality` become siblings directly under it); `CountryName`/`LocalityName` → generic `NameElement`; the unqualified `Type="Town"` attribute on `LocalityName` → namespaced `xAL:Type="Town"` on `Locality`, plus `xAL:NameType="Name"` on the locality's `NameElement`. Text values (`日本`, `東京都新宿区霞ヶ丘町`) are unchanged.

### 4.6 Appearance / textures

| CityGML 2.0 | CityGML 3.0 |
|---|---|
| `app:appearanceMember` on `core:CityModel` | `core:appearanceMember` |
| `app:surfaceDataMember` | `app:surfaceData` |
| `app:ParameterizedTexture` | identical |
| `app:imageURI` = `53394517_bldg_6697_appearance/stad0158.jpg`, `app:mimeType` = `image/jpg`, `app:theme` = `rgbTexture` | identical |
| `app:target uri="#poly_STAD0158_p1159_0"` (649×) | `app:target` element whose **text** is `#poly_STAD0158_p1159_0`, nested in `app:textureParameterization` → `app:TextureAssociation` (649×) |
| `app:TexCoordList` with two identical `app:textureCoordinates ring="#line_…"` children per target (1,298 total) | `app:TexCoordList` with one `app:textureCoordinates` child (649 total) plus a new sibling `app:ring` element holding `#line_…` |

Example:

**2.0:**
```xml
<app:target uri="#poly_STAD0158_p1159_0">
  <app:TexCoordList>
    <app:textureCoordinates ring="#line_STAD0158_p1159_0">0.433897 0.9716409 …</app:textureCoordinates>
    <app:textureCoordinates ring="#line_STAD0158_p1159_0">0.433897 0.9716409 …</app:textureCoordinates>
  </app:TexCoordList>
</app:target>
```

**3.0:**
```xml
<app:textureParameterization>
  <app:TextureAssociation>
    <app:target>#poly_STAD0158_p1159_0</app:target>
    <app:textureParameterization>
      <app:TexCoordList>
        <app:textureCoordinates>0.433897 0.9716409 …</app:textureCoordinates>
        <app:ring>#line_STAD0158_p1159_0</app:ring>
      </app:TexCoordList>
    </app:textureParameterization>
  </app:TextureAssociation>
</app:textureParameterization>
```

Note that the `uri`/`ring` **attributes** in 2.0 became element **text** in 3.0, and the duplicated texture-coordinate list per target was dropped. The 649 remaining coordinate strings are all exactly present (and unique) in the 2.0 file.

### 4.7 Child order inside `bldg:Building`

| CityGML 2.0 | CityGML 3.0 |
|---|---|
| 3 × `gen:stringAttribute`, `bldg:measuredHeight`, `bldg:lod0RoofEdge`, `bldg:lod1Solid`, `bldg:lod2Solid`, 650 × `bldg:boundedBy`, `bldg:address`, `uro:buildingDetails`, 3 × `uro:extendedAttribute` | 3 × `core:genericAttribute`, 650 × `core:boundary`, `core:lod0MultiSurface`, `core:lod1Solid`, `core:lod2Solid`, `con:height`, `bldg:address`, `bldg:adeOfAbstractBuilding` |

## 5. Data-preservation verification

| Measure | 2.0 file | 3.0 file | Result |
|---|---|---|---|
| `gml:posList` elements | 785 (785 unique) | 785 (785 unique) | 785/785 exact string matches |
| `gml:id` values | 1,951 unique | 1,951 unique | identical sets |
| - `Building` / `GroundSurface` / `RoofSurface` / `WallSurface` | 1 / 1 / 279 / 370 | 1 / 1 / 279 / 370 | identical |
| - `Polygon` / `LinearRing` | 650 / 650 | 650 / 650 | identical |
| `xlink:href` values in `lod2Solid` | 650 | 650 | identical sets |
| Textured polygons (`app:target`) | 649 | 649 | same 649 target IDs |
| `textureCoordinates` elements | 1,298 (649 unique, duplicated) | 649 (649 unique) | de-duplicated; no values lost |
| `imageURI` / `mimeType` / `theme` | 1 / 1 / 1 | 1 / 1 / 1 | identical |
| Generic attribute values | 3 | 3 | identical |
| URO ADE values | buildingDetails + 3 KeyValuePairs | same | identical |
| Address text | 日本 / 東京都新宿区霞ヶ丘町 | same | identical |
| Envelope coordinates | 6 values | 6 values | identical |

## 6. What the upgrade entails conceptually

- **GML 3.1 → 3.2**: namespace change and `CompositeSurface` → `Shell` for solid exteriors; `gml:Envelope`/`posList` usage stays compatible here.
- **CityGML 2 → 3 module reorganization**: theme classes that used to live in the building module (`lod0RoofEdge`, `lod2MultiSurface`, `boundedBy`) moved to the core module; boundary surface classes (`GroundSurface`, `RoofSurface`, `WallSurface`) moved to the new Construction module, which `bldg:Building` now derives from. That is why `con:height` and `con:*Surface` appear.
- **LOD representation**: LOD0/1/2 geometry is semantically the same, just renamed/renamespaced. `lod0RoofEdge` became the more neutral `lod0MultiSurface`.
- **Attributes and ADE**: CityGML 3 requires generic attributes in `core:genericAttribute` wrappers with typed `gen:*Attribute` children, and requires ADE content in explicit `adeOf*`/`*Properties` containers — hence the `uro:BuildingProperties` wrapper.
- **xAL 2 → 3**: address encoding uses generic `NameElement` with namespaced type attributes instead of dedicated `*Name` elements.
- **Appearance 2 → 3**: texture mapping is wrapped in `TextureAssociation`/`textureParameterization`, and references use element content rather than attributes.

## 7. Caveats / notable findings

- The `uro` namespace URI appears to go *backwards* in version number (1.5 → 1.4) while also changing host (`chisou.go.jp` → `kantei.go.jp`). This is how the two published PLATEAU distributions are encoded; it is not a typo introduced in this comparison.
- The CityGML 3 file removes the duplicated `textureCoordinates` entry that each 2.0 `TexCoordList` carried. No texture coordinate values are lost, but the raw element count drops from 1,298 to 649.
- `codeSpace` paths change from `../../codelists/…` to `../codelists/…`, consistent with the different relative locations of the XSD/codelist folders (`./urbanObject_CityGML3.xsd` vs the remote 2.0 schema URLs).
- Only geometry payloads, IDs and semantic values were compared here; XSD validation against the referenced schemas was not performed because those schema files are not present in the folder.
