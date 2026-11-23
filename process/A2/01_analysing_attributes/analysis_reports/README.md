# ADE attribute analysis

## Using the Python script

Use the python script `plateau_ade_analysis{_v*}.py` in a Linux terminal with one of the following commands: 

```
python3 plateau_ade_analysis.py file   /path/to/xxx.gml
python3 plateau_ade_analysis.py folder /path/to/folder
```

Optional flags: `--output PATH`, `--unknown-pattern REGEX` (default `^-?9+$`). Reports are written next to the input by default and also printed to stdout.

## Definitions of variables 
A definition of the different variables in the analysis reports:

| Name | File/Folder | Definition |
|---|---|---|
| `bldgFileCount` | Folder | how many building CityGML files are in the folder |
| `totalBldgCountFolder` | Folder | total amount of buildings in the folder |
| `totalAttrCountFolder` | Folder | total amount of unique attributes that are present in the files in the folder |
| `attrName` | File and Folder | the i-UR ADE attributes that are in the file/folder (with prefix ‘uro’) |
| `attrCount` | File and Folder | how many times in total the attribute is present in the file/folder |
| `bldgWithAttrCount` | File and Folder | how many of the buildings have this attribute (does not count duplicates, so if a building has several instances of the same attribute) |
| `bldgWithAttrCount_pct` | Folder | percentage of bldgWithAttrCount compared with the amount of buildings in a folder |
| `attrUnkwnCount` | File and Folder | how many times is the value of this attribute unknown (indicated with values of 99, 999, -9999 etc.) |
| `attrUnkwnCount_pct` | Folder | percentage of attrUnkwnCount compared to the amount of attributes of this type |
| `attrEmptyCount` | File and Folder | how many times is this attribute present but without a value |
| `attrEmptyCount_pct` | Folder | percentage of attrEmptyCount compared to the amount of attributes of this type |
| `attrNullCount` | File and Folder | how many times is this attribute present but with a null value (independent of letter capatilasation |
| `attrNullCount_pct` | Folder | percentage of attrNullCount compared to the amount of attributes of this type |

Some variables are only present when the script is run on a folder, which results in an extra summary table containing the complete set of variables. This is indicated in the second column. 

## Script versions

- `plateau_ade_analysis_v3.py` - added distinction between attributes with the same `attrName` but different parent group (e.g. `uro:surveyYear` which can be part of `uro:BuildingDetailAttribute` or `uro:LargeCustomerFacilityAttribute`), and added check for null values
- `plateau_ade_analysis_v2.py` - added folder specific variables and folder summary table
- `plateau_ade_analysis.py` - basic script
