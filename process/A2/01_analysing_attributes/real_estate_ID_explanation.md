# Japan's Real Estate ID (不動産ID)

**What it is, why it was created, and where it stands**

| Item | Detail |
|---|---|
| Primary source | 国土交通省（MLIT）, *不動産IDルールガイドライン* (Real Estate ID Rule Guideline) |
| Published | 31 March 2022 (令和4年3月31日) |
| Publisher | MLIT, Real Estate and Construction Economy Bureau (不動産・建設経済局) |
| Source URL | <https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/content/001594268.pdf> |
| Document type | Administrative guideline, **not a law**; use is voluntary |
| Length | 18 pages |
| Status research cutoff | 24 November 2026 |

> **Note on the source.** The 2022 PDF is the original guideline. MLIT has since added a note to the current online version (October 2024) stating that the guideline's contents may change in light of problems found in the FY2023 demonstration projects. The 2022 text is therefore the authoritative statement of the *original* design, not necessarily the final design.

---

## 0. Quick answer

| Question | Short answer |
|---|---|
| **What is the Real Estate ID?** | A 17-character common code for uniquely identifying a piece of real estate: a **13-digit 不動産番号** (property register number) plus a **4-digit 特定コード** (specific code), normally written with a hyphen, e.g. `1234567890123-0203`. |
| **Why was it created?** | Japan had no widely shared property identifier. Addresses and parcel numbers have notation variations, and one address can contain several buildings, so public and private organisations could not quickly tell whether two records referred to the same property. Matching and linking data was slow and costly. |
| **Is it discontinued?** | **No.** It has not been cancelled. |
| **Is it already in use?** | **Not in general use.** It remains voluntary and pre-implementation. There have been prototypes and demonstration projects since FY2023. |
| **Is it still in development?** | **Yes.** As of late 2026 the numbering scheme itself is under review, and MLIT is preparing a trial in selected leading areas. |
| **Timeline** | Official target: **trial operation during FY2027** (April 2027–March 2028) in a few leading areas, then social implementation. Trade press in 2026 reports an aim of **full social implementation in the early 2030s**. Earlier expectations of rollout around 2025 have slipped. |
| **Will it never be used / is it unrealistic?** | It is **not unrealistic or abandoned**, but it is **behind schedule and not yet settled**. The 2022 17-digit register-based scheme may be modified or partly replaced. Its future depends on the 2026 review, budget, data coverage, legal mandate and operator model. |

---

## 1. What the Real Estate ID is

### 1.1 Definition

The guideline defines the Real Estate ID as:

> 「不動産を一意に特定することができる、各不動産の共通コード」
>
> "A common code for each piece of real estate that makes it possible to uniquely identify that real estate."

The ID is composed of:

```text
不動産ID (17 digits/characters)
= 不動産番号 (13 digits) + "-" + 特定コード (4 digits/characters)
```

Example from MLIT materials:

```text
0100123456789-0203
│             │
│             └── 特定コード: room 203 (0203)
└──────────────── 不動産番号: 13 digits
```

The ID is not a new number issued by a new government registry. It is assembled from an existing public number (the 不動産番号) plus a short additional code where necessary.

### 1.2 The 13-digit 不動産番号

The **不動産番号** is a number recorded in the title section (表題部) of the real estate register (不動産登記簿) under the Real Estate Registration Act and the Real Estate Registration Regulations.

Key properties:

- It is assigned **per parcel of land** (一筆の土地) or **per building** (一個の建物), and for a condominium building, **per exclusive-use unit** (一個の専有部分).
- It is normally printed in the **upper-right corner of a certificate of registered matters** (登記事項証明書).
- It is unique, stable, nationally widespread, and backed by authentic location information.
- It is already used in registration procedures; under the Real Estate Registration Order, citing it can allow certain location details to be omitted from an application.

The guideline treats the 不動産番号 as the "public and basic" foundation of the Real Estate ID because it satisfies the required properties: uniqueness, no ambiguity, nationwide coverage, uniform usability by businesses, and authenticity of linked location data.

### 1.3 The 4-digit 特定コード

The 不動産番号 identifies a parcel or a building (or a condominium unit), but it does **not** identify every unit that businesses actually transact.

The clearest example is an ordinary rental apartment building. It is usually a **non-condominium building** (非区分建物), so the whole building has **one** 不動産番号. The 13-digit number alone cannot distinguish room 101 from room 102.

The guideline therefore adds a **4-digit 特定コード** after the 不動産番号 when the 不動産番号 alone is insufficient. If no additional code is needed, the 特定コード is `0000`.

### 1.4 The ten basic rules

The guideline sets out ten rules by property type. The table below summarises them.

| No. | Property type | Unit to which the ID is attached | 13-digit part | 4-digit 特定コード | Example / note |
|---:|---|---|---|---|---|
| ① | Land (土地) | Per registered parcel (筆) | The parcel's 不動産番号 | `0000` | `1234567890123-0000` |
| ② | Detached house (建物・戸建て) | Whole building | The building's 不動産番号 | `0000` | `1234567890123-0000` |
| ③ | Non-condominium building, commercial use (非区分建物・商業用) | Per floor | The building's 不動産番号 | Floor code (2) + floor number (2) | 2nd floor above ground: `G002`; 1st basement: `B001` |
| ④ | Non-condominium building, residential use (非区分建物・居住用) | Per room | The building's 不動産番号 | Room number (4) | Room 203: `0203` |
| ⑤ | Whole non-condominium building (非区分建物全体) | Whole building | The building's 不動産番号 | `0000` | `1234567890123-0000` |
| ⑥ | Condominium, commercial, whole exclusive-use unit (区分所有建物・商業用・専有部分全体) | One exclusive-use unit | The unit's 不動産番号 | `0000` | `1234567890123-0000` |
| ⑦ | Condominium, commercial, part of an exclusive-use unit (区分所有建物・商業用・専有部分の一部) | Per floor within the unit | The unit's 不動産番号 | Floor code (2) + floor number (2) | Same floor-code rules as ③ |
| ⑧ | Condominium, residential, one room per unit (区分所有建物・居住用・専有部分＝1部屋) | One room / unit | The unit's 不動産番号 | `0000` | Typical subdivided-for-sale apartment |
| ⑨ | Condominium, residential, multiple rooms per unit (区分所有建物・居住用・専有部分＝複数部屋) | Per room | The unit's 不動産番号 | Room number (4) | E.g. landlord's home plus rental rooms in one registered unit |
| ⑩ | Whole condominium building (区分所有建物の建物全体) | Whole building | The **land** parcel's 不動産番号 | `000B` | Uses the land number, not a building number |

#### Floor code (for rules ③ and ⑦)

The 4-digit code is two digits of floor class plus two digits of floor number:

| Position | Meaning | Value |
|---|---|---|
| 1st character | Above ground or basement | `G` = above ground; `B` = basement |
| 2nd character | Ordinary floor or intermediate floor | `0` = ordinary; `M` = intermediate |
| 3rd–4th characters | Floor number, right-aligned | e.g. `02` for 2nd floor |

Examples:

- 2nd floor above ground: `G002`
- 1st basement: `B001`
- An intermediate above-ground floor: `GMxx`
- An intermediate basement floor: `BMxx`

Because the code identifies a **floor**, not an individual office or shop, all units on the same floor of a commercial non-condominium building receive the **same** Real Estate ID. The guideline explicitly accepts this.

#### Room number (for rules ④ and ⑨)

For residential non-condominium buildings such as rental apartments, the 4-digit code is the room number, padded to four digits where necessary (room 203 → `0203`).

Normalisation rules:

- Use only digits and Latin letters. Remove hiragana, katakana, kanji and other characters.
- Convert lowercase Latin letters to uppercase (e.g. `2a` → `2A`).
- Convert Roman numerals to Arabic numerals.
- Omit building numbers such as "A棟" or the "A" in "A1101", because registration and 不動産番号 are normally per building. In the example, `A1101` becomes `1101`.

### 1.5 Writing and formatting rules

The guideline requires a consistent textual representation so that databases can exchange the ID reliably:

- Use **half-width** characters: half-width digits and half-width uppercase Latin letters.
- The standard format is:

```text
不動産番号（13桁）-特定コード（4桁）
```

- Use a half-width hyphen `-` between the two parts.
- For database-design reasons, another delimiter (for example a half-width semicolon) may be used if that is more appropriate, but the default is the hyphen.
- The 13-digit part alone can also be used as a linking key. The hyphen exists to make the boundary between the 13-digit and 4-digit parts explicit.

### 1.6 What the Real Estate ID is **not**

This is important for avoiding common misunderstandings:

- **It is not a government-issued number from a new central database.** The guideline explicitly says the initiative is not intended for the national government to create a single database, issue IDs, collect real-estate information, and distribute it to actors.
- **It is not a mandatory legal identifier.** It is a guideline-based common code. At the time of writing there was no law requiring its use.
- **It is not the same as an address, parcel number (地番) or building number (家屋番号).** It is built on the 不動産番号 from the register.
- **It is not a complete national register of all buildings.** It only applies once a property has reached the title-registration stage (表題部登記). There is **no rule for unregistered properties**, including newly built but unregistered buildings.
- **It does not by itself make personal information public.** Linking an ID to internal data does not authorise disclosure of personal information or internal business information. What is shared is decided case by case by each actor.

### 1.7 Coverage gaps and edge cases in the 2022 design

The guideline itself identifies several limitations:

1. **Unregistered properties.** No ID rule exists before title-section registration. This includes newly built, unregistered buildings.
2. **Whole condominium building.** Because there is no building-wide 不動産番号 for a condominium, rule ⑩ uses the **land** parcel's number with code `000B`. Consequently:
   - if several condominium buildings stand on the same parcel, they can share the same whole-building ID;
   - if a building is demolished and rebuilt, the old and new buildings can share the same whole-building ID.
3. **Commercial floors.** Individual offices or shops on the same floor cannot be distinguished under rule ③; they share an ID.
4. **Mixed-use buildings.** Commercial vs residential is judged by the **building's overall use**, not by an individual room's use. If the building is genuinely mixed by floor (e.g. shops on floors 1–2, housing on floors 3–4), the relevant rules are applied floor by floor.
5. **Residential building used partly as offices.** A room in a residential building leased for non-residential purposes still follows the residential rules ④, ⑧ or ⑨.

### 1.8 Governance, privacy and permitted use

**Governance model.** The guideline does not create a central operator. Each public or private actor that holds real-estate-related information is expected to link the Real Estate ID to its own data, and then to link, accumulate and use that data through its own initiatives and negotiations with other actors. The role of the state is to define the rules and improve the enabling environment, not to run a single database.

**Privacy.** The ID alone does not identify a specific individual. However, if the holder of the ID (or the underlying 不動産番号) can easily cross-check it with other information and thereby identify a specific individual, the combined information can constitute "personal information" under Article 2(1) of the Act on the Protection of Personal Information (個人情報保護法). The guideline's position is:

- If use stays within existing practice under personal-information law, no special new measure is required.
- Beyond that, appropriate measures such as publishing the purpose of use or obtaining consent for third-party provision may be required.
- Anonymous processed information (匿名加工情報) and pseudonymised processed information (仮名加工情報) can be used under the statutory regimes, but anonymous processing requires removing linkage codes, including the Real Estate ID, without omission.

**Permitted use.** In principle, anyone, public or private, may use the ID freely. The guideline states that use for the following purposes is not acceptable:

- acts contrary to laws and regulations or public order and morals;
- use that unjustly harms a third party;
- use that undermines the credibility of the Real Estate ID system.

It recommends that organisations using the ID adopt internal rules to prevent such use.

---

## 2. Why the Real Estate ID was created

### 2.1 The problem

The guideline's diagnosis is straightforward:

> At present, in Japan's real-estate field, there is no number (ID) commonly used across a wide range of actors for either land or buildings. Because of variations in how addresses and parcel numbers are written, it is not immediately clear whether two records refer to the same property.

Consequences:

- When brokers, developers and others collect and match real-estate-related information held by many different actors, or when they try to provide accurate information to consumers, the work takes **time and effort**.
- This is a bottleneck for **linking, accumulating and using** real-estate-related information.
- The problem affects not only transaction data but also performance, management, infrastructure, maps, hazard maps and other area information.

The guideline's examples of the underlying problem include:

- different spellings or formats of the same address;
- mixing of addresses and parcel numbers;
- multiple buildings at the same address;
- addresses that are not unique identifiers.

### 2.2 The intended benefits

The guideline presents the ID as a **common code** that makes it possible to identify a property uniquely, including where addresses vary or where one address contains multiple buildings. Expected benefits include:

**For businesses and data management**

- Easier matching and linking of property records ("名寄せ") within a company or group.
- Easier linking of externally acquired data to an internal database by simply comparing IDs.
- Less manual work and lower cost in data collection and cleaning.

**For property portals and consumers**

- Better search functions.
- Batch display of duplicate listings.
- Timely removal of listings after a transaction is concluded.
- More accurate information provision to consumers.

**For the wider digital and physical environment**

- Linking real estate to spatial information.
- Use in life-infrastructure (electricity, gas, water, communications), town planning, logistics and other fields beyond real estate.
- Connection with the Digital Garden City Nation concept (デジタル田園都市国家構想), smart cities and digital twins.
- A foundational information layer for "real estate DX" and for the wider digital society.

The guideline also links the initiative to other policies: IT-based important-matters explanations in transactions, digitisation of administrative information, and the broader productivity and convenience agenda for the real-estate industry.

### 2.3 What the initiative was explicitly **not** meant to be

The guideline is careful to set expectations:

- It is **not** a national database project.
- It is **not** a scheme for the government to issue IDs centrally.
- It is **not** a scheme for the government to collect real-estate information and provide it to actors.
- It is **not** a mandate to disclose personal or internal information.
- It is **not** a substitute for decisions about what data each actor may share; those decisions remain with each actor and each use case.

The state's role is to provide the **rules** and to improve the environment, for example by making the 不動産番号 easier to confirm and by linking government and local-government data to the ID.

---

## 3. Status **in the 2022 document**

The 2022 document is a **rule guideline**, not a launch announcement. Its own status claims are modest:

- It defines the ID and explains the points to note when using it.
- It expects the ID to be used **voluntarily** by public and private actors.
- It expects benefits to emerge gradually as actors link IDs to their data and as linked data increases.
- It says MLIT will continue to work on:
  - making the 不動産番号 easier to confirm;
  - linking national and local-government data to the Real Estate ID;
  - improving the environment for use.

In other words, in March 2022 the project had **rules but no operational system**. The guideline was the starting point for voluntary adoption, not evidence that the system was already running.

---

## 4. Current status (as of 24 November 2026)

> This section goes beyond the 2022 PDF. It uses MLIT pages, official meeting minutes, a 2025 MIC/Japan Post progress deck, and 2026 trade-press reporting. Dates in parentheses are the source dates.

### 4.1 Timeline of the project after the guideline

| Date | Development |
|---|---|
| **31 Mar 2022** | MLIT publishes the *Real Estate ID Rule Guideline* (the source PDF). |
| **30 May 2023** | MLIT establishes the **Real Estate ID Public–Private Cooperation Council** (不動産ID官民連携協議会). By October 2023 it had around 250 members: industry bodies, private companies, local governments, academics and related ministries. |
| **FY2023** | MLIT builds a prototype **Real Estate ID confirmation system** (不動産ID確認システム), using registry data for 440 municipalities. 23 demonstration projects are conducted; 18 use the confirmation system. |
| **Jan–Feb 2024** | Social experiment with real-estate agents: agents obtain Real Estate IDs and enter them when registering properties on REINS. |
| **FY2024** | Problems with the registry-based approach become clear. MLIT shifts toward generating building IDs from **Japan Post address/delivery data**. In 19 test areas, about **90%** of data is confirmed to be covered. A trial at Akabane Post Office tests converting mailbox-level delivery data into building-level IDs. |
| **1 Jul 2025** | MIC/Japan Post progress report: the aim is to start **trial operation during FY2027**. Work continues on standardising data generation, expanding trials, and verifying use with local governments. |
| **29 May 2026** | MLIT launches the **Study Group on the Ideal Form of the Real Estate ID** (不動産IDのあり方に関する勉強会). |
| **1 Jul 2026** | Second study-group meeting. |
| **24 Aug 2026** | Third study-group meeting. Discussion includes whether issuance at the building-confirmation application stage should be legally mandatory, and whether the operator should be the state or a designated corporation. |
| **Autumn 2026** | The study group continues; a final compilation is expected around **December 2026**. |
| **FY2027 budget request** | MLIT requests **¥500 million** for "promotion of Real Estate ID development as the key to architectural and urban DX." If approved, a trial could begin **from April 2027** in areas such as central Tokyo, and system development would be outsourced. |
| **FY2027 (target)** | **Trial operation in selected leading areas** (一部先行整備地域における試験運用). |
| **After that** | Social implementation. Trade press in 2026 reports an aim of **full social implementation in the early 2030s**. |

### 4.2 What changed after 2022

The 2022 design was built on the **不動産番号** from the property register. That approach ran into practical problems:

- In the register, a building's "location" (所在) is recorded as the **land parcel number**, not as a residential address. This makes it hard to link a building ID to ordinary address-based data.
- Newly built but unregistered buildings have **no 不動産番号** and therefore no ID under the 2022 rules.
- Room-level and floor-level identification is incomplete or coarse in some property types.
- Coverage and data quality are uneven.

As a result, from FY2024 MLIT began investigating a different base: **Japan Post's address and delivery data**, combined with location information, to generate IDs at the **building level**. The 2025 MIC/Japan Post deck describes the aim as converting "per-mailbox" Japan Post data into "per-building" Real Estate ID data.

This is a significant shift. It does **not** mean the project was cancelled. It means the **numbering scheme and generation method are being redesigned** while the policy objective remains.

### 4.3 The 2026 review

In May 2026 MLIT established the **Study Group on the Ideal Form of the Real Estate ID**, with lawyer Kotaro Tamura (田村幸太郎) as chair. The group is reconsidering the ID's generation, management and use rules in parallel with system design for the FY2027 trial.

Themes reported from the meetings (these are **opinions and options**, not final decisions; the summary below also draws on secondary reporting of the meetings):

- **Start with a narrower scope.** Begin with buildings, where demand is clear and users are numerous; treat rooms and compartments as a future issue.
- **Building-level first.** There is no objection in principle to making buildings the basic unit of numbering.
- **Link with the Digital Agency's address base registry** (アドレス・ベース・レジストリ) and other base registries.
- **Use Japan Post delivery data** to improve coverage.
- **Legal mandate?** Whether to require issuance at the building-confirmation application stage is still under consideration.
- **Operator model?** Whether the state or a designated corporation should operate the system is still under consideration.

The study group is expected to compile its conclusions around December 2026, feeding into institutional design from FY2027 onward.

### 4.4 What is official and what is still uncertain

**Official / on MLIT's current page:**

- The government is working toward **trial operation in selected leading areas during FY2027**, and social implementation thereafter.
- It is currently studying the **generation method and system** for the ID.
- A study group is reconsidering the **generation, management and use rules**.

**Still uncertain as of 24 November 2026:**

- The final **numbering scheme** (whether the 2022 17-digit 不動産番号 + 特定コード design survives, is modified, or is replaced).
- Whether use or issuance will be **legally mandated** (for example at building-confirmation).
- The **operator**: government, designated corporation, or another model.
- The **final scope**: buildings only at first, with rooms/compartments later, or a broader scope from the start.
- The **budget**: the ¥500 million figure is a **request**, not an enacted budget.
- The **exact start date and areas** of the FY2027 trial.
- The **full-implementation date**: MLIT's page says "thereafter"; trade press reports "early 2030s"; an earlier 2023 roadmap envisaged fuller rollout from around 2028. The timeline has clearly slipped.

### 4.5 Bottom-line assessment

**Status category:** **In development / pilot preparation. Not discontinued. Not in general operation.**

A precise formulation for a thesis would be:

> The Real Estate ID is a voluntary, guideline-based common property identifier promoted by MLIT. It has not been enacted as a legal identifier and is not yet in general use. Since FY2023 it has been tested through a prototype confirmation system and demonstration projects. After problems with the original registry-number-based design, MLIT shifted toward building-level IDs generated from Japan Post address data and launched a review of the ID's ideal form in 2026. The official target is trial operation in selected leading areas during FY2027, with social implementation thereafter; trade press reports an aim of full implementation in the early 2030s. The 2022 17-digit design should therefore be treated as the original specification, not as the final operational specification.

**Is it unrealistic or likely never to be used?** No. It has consistent policy backing, a dedicated public–private council, budget requests, and an official trial target. But it is **not yet a done deal**. The main risks are:

- repeated redesign of the numbering scheme;
- weak incentives for voluntary adoption;
- incomplete data coverage, especially for unregistered buildings and room-level units;
- unresolved questions about legal mandate and operator;
- budget and political priority;
- competition or overlap with the Digital Agency's real-estate base registry work.

The realistic reading is: **likely to be piloted in some form in the late 2020s, but full nationwide use is a 2030s prospect and the final design may differ from the 2022 guideline.**

---

## 5. Implications for a thesis

If you are writing about the Real Estate ID, keep these distinctions explicit:

1. **Rule vs. system.** The 2022 guideline defines a rule. It does not prove that a system exists.
2. **Original design vs. current design.** The 17-digit 不動産番号 + 特定コード design is the 2022 design. Since FY2024 the generation method has been under review, and a 2026 study group is reconsidering the rules. Do not present the 2022 design as the final current specification without a caveat.
3. **Voluntary vs. mandatory.** As of late 2026 there is no law defining or mandating the Real Estate ID. Legal mandate is still being discussed.
4. **Trial vs. general use.** FY2027 is a trial in selected leading areas, not nationwide operation.
5. **"Not discontinued" vs. "on track."** Both are true in different senses: the project continues, but the timeline has slipped and the design is being revised.

A defensible summary sentence:

> Japan's Real Estate ID is a voluntary common property code whose original 2022 design combined the 13-digit property register number with a 4-digit specific code. It is still in the development and pilot stage; MLIT aims for trial operation in selected areas in FY2027, with full social implementation later, and the numbering scheme itself is under review as of 2026.

---

## 6. Glossary

| Japanese | English | Meaning |
|---|---|---|
| 不動産ID | Real Estate ID | The 17-character common code |
| 不動産番号 | Real estate number / property register number | 13-digit number recorded in the title section of the register |
| 特定コード | Specific code | 4-digit suffix used when the 不動産番号 alone is insufficient |
| 不動産登記簿 | Real estate register | Official register of land and buildings |
| 表題部 | Title section | Part of the register describing the property's physical details |
| 登記事項証明書 | Certificate of registered matters | Official certificate; the 不動産番号 is normally in the upper-right corner |
| 筆 | Parcel | A unit of land in the register |
| 区分所有建物 | Condominium / sectional ownership building | Building with separately owned exclusive-use units |
| 専有部分 | Exclusive-use unit | The privately owned part of a condominium |
| 非区分建物 | Non-condominium building | Building not divided into separately owned units |
| 地番 | Parcel number | Land identifier in the register |
| 家屋番号 | Building number | Building identifier in the register |
| 名寄せ | Name matching / record linkage | Matching records that refer to the same property or entity |
| 官民連携協議会 | Public–private cooperation council | MLIT's Real Estate ID promotion council |
| ベース・レジストリ | Base registry | Authoritative public reference data used across systems |

---

## 7. Sources

### Primary source

- MLIT, *不動産IDルールガイドライン*, 31 March 2022 (18 pages).  
  <https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/content/001594268.pdf>

### Official MLIT and government sources (post-2022 status)

- MLIT, 不動産市場整備：不動産ID (current portal page, accessed 24 Nov 2026).  
  <https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/tochi_fudousan_kensetsugyo_tk5_000001_00040.html>
- MLIT, current online version of the guideline with the October 2024 note that the contents may change.  
  <https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/content/001769626.pdf>
- MLIT, *不動産IDの2024年度の検討内容について* (25 June 2024).  
  <https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/content/001763035.pdf>
- MLIT, *第1回 不動産IDのあり方に関する勉強会 議事概要* (29 May 2026).  
  <https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/content/002008336.pdf>
- MLIT, *第3回 不動産IDのあり方に関する勉強会 議事概要* (24 Aug 2026).  
  <https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/content/002021100.pdf>
- MLIT, 不動産IDのあり方に関する勉強会 page (meeting list and materials).  
  <https://www.mlit.go.jp/tochi_fudousan_kensetsugyo/tochi_fudousan_kensetsugyo_tk5_000001_00040.html>
- Ministry of Internal Affairs and Communications / Japan Post, *不動産IDの進捗状況及び本年度の動き* (1 July 2025).  
  <https://www.soumu.go.jp/main_content/001017294.pdf>
- Cabinet Office, *国と地方のシステムWGご説明資料* (30 Oct 2023), including the 2023 roadmap and the public–private council membership.  
  <https://www5.cao.go.jp/keizai-shimon/kaigi/special/reform/wg6/20231030/pdf/shiryou2-2.pdf>
- MLIT, press release: *不動産の共通コードとしての「不動産ID」のルールを整備！* (31 March 2022).  
  <https://www.mlit.go.jp/report/press/tochi_fudousan_kensetsugyo05_hh_000001_00067.html>

### Trade press and secondary reporting (2026)

- Tokyu Livable / 日刊不動産経済通信, "国交省、来春にも「不動産ID」試験運用" (31 Aug 2026).  
  <https://www.livable.co.jp/shiritai/column/news/2026/083101.html>
- estie, "「不動産DXカンファレンス2026」開催レポート（前編）" (30 Sep 2026), reporting MLIT's statement that the originally envisioned method did not fit reality and stalled.  
  <https://www.estie.jp/blog/entry/2026/09/30/100000>
- 住宅新報, "「不動産ID」改めて検討 新勉強会で必要性など議論 国交省" (9 June 2026).  
  <https://www.jutaku-s.com/newsp/id/66905>
- ulsta, "不動産IDとは｜17桁のしくみ、不動産番号は何桁か、調べ方と使い道" (updated 7 Oct 2026), a secondary overview of the 2026 review.  
  <https://ulsta.jp/column/real-estate-id-system-2026/>

---

*Prepared 24 November 2026. The 2022 guideline is quoted and summarised from the Japanese original; the current-status section is based on the official and secondary sources listed above. Dates after the 2022 guideline are subject to confirmation against the latest MLIT materials, particularly the study group's final compilation expected around December 2026.*
