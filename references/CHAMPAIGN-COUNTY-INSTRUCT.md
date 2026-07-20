# Champaign County, Ohio — LLM Instruct & Reference Brain

**Project:** Fake Burg Telegram (`fakeburgtelegram.com`)  
**Purpose:** Single source for Onion-style satirical local news that feels like Champaign County, Ohio.  
**Sources merged:** Grok Heavy research (`fakeburg/context.txt`, all revisions) + prior local bible (businesses, streets, policy).  
**Last assembled:** July 2026  

**Hard rules**
1. Use this file for place names, roads, mascots, surnames, landmarks, and businesses. **Do not invent** new towns, highways, high-school mascots, or surnames outside these lists.
2. **Invent characters** freely. Use real geography as *setting* (where someone parks, drives, shops, argues).
3. **Do not** invent crimes, bigotry, health-code scandals, or illegal acts attributed to **real living private people** or real businesses. Real businesses = passive scenery only (line at Crabill’s, parking by the Gloria). No fake quotes from real owners.
4. There is a **Mechanicsburg, PA** and a **Lewisburg, OH (Preble Co.)**. We mean **Mechanicsburg, Champaign Co.** and **North Lewisburg, Champaign Co.**
5. Businesses open/close — re-check if a special section depends on a specific shop still existing.

---

## System / instruct prompt (copy for the model)

You write fake local news articles in the exact style of **The Onion**: formal, deadpan newspaper voice; escalating absurdity from a kernel of real small-town Midwest reality. Every piece should feel clipped from the **Urbana Daily Citizen** or township trustee minutes.

**Ground every article with 3–6 authentic details** sampled from this file (especially roads, obscure places, mascots, surnames, businesses used as scenery). Prefer hyper-specific combos, e.g. “a farmer on Lonesome Road near Davey Woods” or “Crybaby Bridge on the edge of Cable.”

### Tone
- Treat high-school sports, **Graham wrestling**, FFA, 4-H, the county fair, church potlucks, and township trustee meetings with the **gravitas of national politics**.
- Exaggerate earnest rural Ohio; comedy comes from straight-faced presentation of the absurd — not mean-spirited mockery of real private people.
- Rivalries (Urbana Hillclimbers vs. Graham Falcons; village vs. “the city”; farm township vs. farm township) are always high-stakes.
- Weather, grain prices, deer, grain elevators, and historical markers are constant conversational fixtures.
- Occasional historical asides (Simon Kenton, Underground Railroad, B-17 at Grimes Field) are encouraged for texture.

### Article formula (Fake Burg Telegram house style)
1. YAML frontmatter: `title`, `slug`, `date`, `category`, `author`, `excerpt`; optional `image`, `featured`, `top_story`, `publish_date`, `draft`.
2. Dateline: `URBANA —` / `MECHANICSBURG —` / `ST. PARIS —` / `NORTH LEWISBURG —` / `CHAMPAIGN COUNTY —` etc.
3. One absurd premise + 3–6 real local anchors + short grafs + deadpan quotes from invented locals.
4. Author default: `Staff report` unless a column needs a fictional byline.

### Variety (do not over-index)
| Overused (throttle hard) | Prefer for fresh batches |
|--------------------------|---------------------------|
| **US-36** / “out on 36” as the default road | **US-68**, **SR-29, 54, 55, 161, 235, 245, 559, 560**, named county roads |
| Parking / mowing / leaf blower / GPS / corn height only | Business scenery, wrestling, aviation, caverns/bog, ghost-lore, FFA/fair, orbit towns |
| Simple Coffee + Frosty’s every other piece | Underused shops (Carmazzi’s, Mayflowers, Ruthie’s, Whitman’s, Scioto Inn, etc.) |
| Only Mechanicsburg / Urbana | Woodstock, Christiansburg, Mutual, Cable, Rosewood, Mingo, Westville, hamlets |

**Soft cap:** at most **~1 in 6** new stories should lead with US-36. Rotate town primary and road primary every piece.

### Seed examples (voice check)
- “St. Paris Man Claims Falcon Spirit Animal Instructed Him to Run for Township Trustee”
- “Urbana Hillclimbers Refuse to Practice Until Man on the Monument Faces a More Motivational Direction”
- “Cable Man Claims Crybaby Bridge Baby Instructed Him to Challenge Pence for Adams Township Trustee”
- “Lonesome Road Residents Near Davey Woods Demand ‘Little Smokies’ Status Officially Recognized by State”
- “Local on Millerstown Road Reports Concord Mills Ghost Mills Still Grinding Corn at Midnight”
- “Graham Wrestling Room Declared Off-Limits to Anyone Who Still Calls a Single a ‘Win’”

---

## County snapshot

| Item | Notes |
|------|--------|
| County | Champaign County, west-central Ohio |
| Population | ~38,800–39,000 |
| Land / farms | Heavily agricultural (~72% cultivated; ~873 farms, avg ~218 acres) |
| Name origin | French for “open level country” / plain |
| Formed | March 1, 1805 (18th Ohio county) from parts of Greene and Franklin |
| County seat / only city | **Urbana** (~11,200) |
| Stats areas | Urbana Micropolitan; Dayton–Springfield–Sidney Combined |
| Phone | Mostly **937** |
| Newspaper of record (real) | **Urbana Daily Citizen** (tone model; we are a satirical sibling brand) |
| Fair | **Champaign County Fair**, fairgrounds **384 Park Ave, Urbana** |
| Region vibe | Farmland, small villages, high-school sports as civic religion; Dayton/Springfield orbit |
| Interstates | **None through the county** (I-70 south in Clark Co.; I-75 west) |

---

## Geography & communities

### City
- **Urbana** — county seat; Monument Square; “the city” relative to villages

### Villages
St. Paris · Mechanicsburg · North Lewisburg · Christiansburg · Woodstock · Mutual

### CDP
- **Rosewood**

### Unincorporated / hamlets (sample freely)
Cable · Carysville · Kingscreek · Millerstown · Mingo · Springhills · Terre Haute · Thackery · Westville · Eris · Kennard · Fountain Park · others

### Townships (exactly 12)
Adams · Concord · Goshen · Harrison · Jackson · Johnson · Mad River · Rush · Salem · Union · Urbana · Wayne

### Nearby places locals constantly reference (not Champaign, but fine as orbit)
Indian Lake (Logan Co.) · West Liberty–Salem · Springfield · Bellefontaine · Marysville · Clark County line south of Christiansburg

### Place cheat-sheet

| Place | Use for |
|-------|---------|
| **Urbana** | Square traffic, “city” airs, fair week, Hillclimbers, aviation museum |
| **Mechanicsburg (“The Burg”)** | Main + Sandusky corner culture; Indians; coffee wars |
| **St. Paris** | Springfield St shops; Graham Falcons; west-county energy |
| **North Lewisburg** | Triad Cardinals; Brush Lake Rd; tiny-village density |
| **Woodstock** | Extreme smallness; one-intersection politics; don’t invent a mall |
| **Christiansburg** | South county; “almost Clark County” |
| **Mutual** | Tiny village; SR-161 begins here at SR-29 |
| **Cable / Rosewood / Mingo / Westville** | Rural pride, township roads, farm edges |
| **Kingscreek / Salem Twp** | West Liberty-Salem Tigers orbit |

---

## Roads & infrastructure

### U.S. highways
| Route | How locals use it |
|-------|-------------------|
| **US 68** | Main **north–south** artery; becomes **Main Street** in Urbana; passes **Grimes Field** / Champaign Aviation Museum; Freshwater Farms north |
| **US 36** | Main **east–west** artery; St. Paris ↔ Urbana ↔ Mechanicsburg corridor; Graham campuses west of St. Paris |

### State routes (key)
| Route | Notes |
|-------|--------|
| **SR 161** | Begins in **Mutual** at **SR 29**; runs east through Champaign Co. (intersects **SR 559** and **SR 4**) into Union Co. toward Columbus suburbs |
| **SR 559** | N–S; starts downtown **Mechanicsburg** at signalized junction of **SR 29 / SR 4**; eastern Champaign (crosses **US 36** near **Woodstock**, serves **North Lewisburg** area); continues into Logan Co. |
| **SR 29** | Urbana / west-ish corridor; meets other routes at Monument Square |
| **SR 54** | Toward **Oak Dale Cemetery** (among other uses) |
| **SR 4** | County network; Mechanicsburg junction with 29 / 559 |
| **SR 55**, **SR 56**, **SR 296**, **SR 560** | Sample for variety |
| **SR 235** | **Kiser Lake** |
| **SR 245** | **Ohio Caverns** (near West Liberty / Salem Twp) |

### Named local / county / township roads (prime satire fuel)
Brush Lake Road · Millerstown Road · River Road · **Woodburn Road** (Cedar Bog) · Neal Road · **Lonesome Road** (Davey Woods) · Pence Road · Zimmerman Road · Heck Road / Heck Hill Road · East Kanagy Road · Game Farm Road · Church Road · Stevenson Road · Upper Valley Pike · Lippincott Road · St. Paris–New Carlisle Road · Troy–Urbana Road · Urbana–Woodstock Pike · Cowpath Road · Dunn Burton Road · Brigner Road · Jackson Hill Road · Stone Quarry Road · numbered **township roads (TR)**

County maintains ~**242 miles** of county roads and assists with ~**340 miles** of township roads.

### Downtown Urbana geometry
Prominent **roundabout** at **Monument Square**: **US 36 / US 68 / SR 29 / SR 54**.

### Village street spines (pair with town name)
| Town | Streets / civic |
|------|------------------|
| Urbana | Main, Miami, Scioto, Church, Market, Washington Ave; Scioto Street Historic District |
| Mechanicsburg | Main, Sandusky, High Street; village offices **18 N Main St**, 43044; schools **60 High Street** |
| St. Paris | S Springfield St, W/E Main; village offices **135 W Main St**, 43072 |
| North Lewisburg | Maple St, East St; village offices **60 East Maple St**, 43060; Triad campus **Brush Lake Rd** |

---

## Weird / absurd / obscure places (sample freely)

### Ghost towns & vanished places
Baker (Jackson Twp, along St. Paris–New Carlisle Rd / Blacksnake Creek) · Brush Lake (Rush Twp) · Concord Mills (mills on Mad River at Millerstown Rd & River Rd; Kenton Memorial Cemetery nearby) · Gourdville · Hagenbaugh / Long (Salem Twp) · Jennings Park (near airport on US 68) · Proctor

### Local lore / “haunted” spots
| Spot | Lore |
|------|------|
| **Crybaby Bridge** (near Cable) | Car stalls at midnight; baby cry + train whistle + woman scream |
| **Evergreen Cemetery** (St. Paris) | Glowing McMorran family tombstone |
| **Lincoln’s funeral train** (Urbana tracks, April lore) | Apparition; clocks stop; skeleton crew |
| **Cedar Bog access road** | Fence legends (Bigfoot / “creature” stories — or just deer) |

### Natural & unique sites
| Site | Notes |
|------|--------|
| **Ohio Caverns** | Ohio’s largest / “most beautiful” cave; Crystal King stalactite; **SR 245** near West Liberty |
| **Cedar Bog Nature Preserve** | Actually a **fen**; rare orchids; National Natural Landmark; **Woodburn Road** south of Urbana |
| **Davey Woods State Nature Preserve** | “Little Smokies of Champaign County”; **Lonesome Road**; mature tulip trees |
| **Siegenthaler-Kaestner Esker State Nature Preserve** | Glacial landform |
| **Kiser Lake State Park** | **SR 235** |
| **Freshwater Farms of Ohio** | **US 68 N** — largest indoor trout hatchery in the state; trout feeding; sturgeon petting zoo lore |
| **Mad River** and valley | Settlement / mill history texture |

### Museums, culture, parks
- **Champaign Aviation Museum / Grimes Field** — B-17 “**Champaign Lady**” under restoration; B-25; Grimes Flying Lab  
- **Pony Wagon Town Historical Museum** (St. Paris; old Pennsylvania Railroad freight depot)  
- **Johnny Appleseed Museum** (former Urbana University campus association)  
- **Gloria Theatre** (216 S Main St, Urbana)  
- **Oak Dale Cemetery** (Simon Kenton grave + life-size statue; historic monuments)  
- **Kenton Memorial Cemetery** · **Honey Creek Cemetery** (Christiansburg)  
- **Champaign County Historical Museum**  
- **Melvin Miller Park**, Gwynne Street Park, Barbara Howell Park  
- **Scioto Inn** · **Simon Kenton Trail** (multi-use path)  
- **Johnson Maple Syrup & Log Cabin** (Stevenson Rd, Cable)  
- Fairgrounds **384 Park Avenue**

---

## Education, mascots & sports

| District / school | Town / area | Mascot | Colors | Notes |
|-------------------|-------------|--------|--------|-------|
| **Urbana High School** | Urbana | **Hillclimbers** (Sparky often) | Maroon & white | Rivalry with Graham; stadium area **Washington Ave** |
| **Graham High School** (Graham Local) | St. Paris / US 36 campuses | **Falcons** | Black & white | **Wrestling = perennial statewide powerhouse** |
| **Mechanicsburg High School** (EVSD) | Mechanicsburg | **Indians** | Purple & gold | High St campus; bowling titles lore OK |
| **Triad High School** | North Lewisburg | **Cardinals** | Red & white | **7920 Brush Lake Rd** complex |
| **West Liberty-Salem** | Salem Twp / Kingscreek / northern orbit | **Tigers** | Black & orange | Serves parts of northern county |

### Graham wrestling (treat as civic religion)
- Perennial **OHSAA team state championship** machine (locals cite **25+ consecutive** team titles / **26+** overall in recent tallies — use as lore, not a spreadsheet argument).  
- Scoring records, multiple individual state champions year after year.  
- Deep program roots with the **Jordan** family; produced Olympic gold medalist **David Taylor**.  
- Any reference should carry the same reverence locals give it — the county’s most consistent claim to athletic fame.

### Conferences / rivalry texture
Central Buckeye Conference (CBC) · Ohio Heritage Conference lore OK · Friday night lights as major civic events · Mechanicsburg Indians ≠ Falcons ≠ Cardinals ≠ Hillclimbers (never mix mascots).

### Elementary / campus notes (optional texture)
- Mechanicsburg: **Dohron Wilson Elementary**; district on High Street  
- Graham: HS **7800 W US Hwy 36**; Middle **9644**; Elementary **9464**; district ~**9915 W US Hwy 36**  

---

## Surnames (characters, officials, farmers, coaches)

**Common:** Smith, Miller, Johnson, Brown, Wilson, Williams, Jones, Davis, Moore, Taylor, Anderson, Baker, Clark, Adams, Thompson, Martin, White, Hall, Lewis, Young  

**Distinctively local / cemetery & record flavor:** Pence, Bodey, Evilsizor / Evilsizer, Ferryman, Neer, Zerkle / Zeigler, Ropp, Huffman, Ward, Grove, Hedges, Kizer, Fraley  

Mix one common + one local-flavor name per cast when possible.

---

## Famous / historical names & accomplishments

Use for texture, asides, school pride, “as every local child is taught…” — **not** as invented scandal protagonists.

| Name | Why it matters here |
|------|---------------------|
| **Simon Kenton** | Frontiersman; associate of Boone; buried **Oak Dale Cemetery**, Urbana, with life-size statue |
| **Col. William Ward** | Founder of Urbana |
| **Joseph Vance** | Ohio Governor 1836–1838; lived in Urbana |
| **Udney Hyde** | Underground Railroad conductor, **Mechanicsburg**; helped hundreds of freedom seekers |
| **Warren G. Grimes** | “Father of the Aircraft Lighting Industry”; **Grimes Field** named for him |
| **Clancy Brown** | Actor (Mr. Krabs, Shawshank, etc.); born Urbana 1959 |
| **Matt Rife** | Comedian; born Urbana |
| **Pete Dye** | Golf-course architect; grew up in Urbana |
| **Robert L. Eichelberger** | WWII general; born Urbana |
| **John Quincy Adams Ward** | Sculptor; strong Urbana connections |
| **Jim Jordan** | U.S. Representative, Ohio’s 4th District (living public figure — use carefully; no invented criminality) |
| **David Taylor** | Olympic wrestling gold; Graham program lore |

**Living public figures policy:** OK as ambient civic context. Do **not** invent crimes, affairs, or medical claims about them.

---

## History & cultural truths

- Agriculture dominates: corn, soybeans, livestock; elevators; county fair; FFA; 4-H.  
- Strong **Underground Railroad** history, especially **Mechanicsburg**.  
- Early 19th-century settlement along the **Mad River**; frontiersman culture still celebrated.  
- Republican-leaning rural politics; **township trustees** (three-member boards) hold surprising local power.  
- Conversational constants: high-school sports, church life, weather.  
- Mild rivalry between “city” Urbana and villages / farm townships.  
- Aviation pride (Grimes / Champaign Lady), cave/fen tourism, historical markers everywhere.  
- Classic Midwest fabric: diners, elevators, Friday-night lights, potlucks, mild suspicion of Columbus traffic.

---

## Businesses by town (scenery only)

### Urbana
| Business | Notes |
|----------|--------|
| **Carmazzi’s** | Historic candy / general-store energy; downtown Main (1890s lore) |
| **TeaBaggers** | Café / coffee / wine — **127 N Main St** |
| **Mumford’s Potato Chips and Deli** | Local institution since 1930s in various spots |
| **Crabill’s Hamburger Shoppe** | Since **1927**; cash-only / drive-thru lore |
| **Mayflowers Chinese Restaurant** | Longtime downtown staple |
| **Guild Galleries** | Interiors & gifts |
| **Mike Major** studio presence | Fine art / sculpture downtown |
| **Gloria Theatre** | Movies + live; “we went to the Gloria” |
| **Scioto Inn** | Boutique hotel downtown |
| **Monument Square District** | Second Saturday / downtown brand events |

### Mechanicsburg
| Business | Notes |
|----------|--------|
| **Simple Coffee Co.** | Main & Sandusky corner; **1 S Main** territory |
| **Hemisphere Coffee Roasters** | **275 E Sandusky St** |
| **Frosty’s Pizza** | **11 N Main St** |
| **The Mercantile** | **13 E Main** — artisan / vintage |
| **Mixin’s N Fixin’s** | Local list fixture (verify if featuring heavily) |

### St. Paris
| Business | Notes |
|----------|--------|
| **Thrifty Falcon** | **119 S Springfield St** |
| **Ruthie’s Farmhouse Boutique** | **121 S Springfield St** |
| **The Local Pair Market** | **127 S Springfield St** |
| **Luna Belle’s Sweet Shoppe** | **144 S Springfield St** |
| **Whitman’s Bike Shop** | **134 S Springfield St** |
| **Wag n Tails Grooming Salon** | **142 S Springfield St** |
| **Wooten Automotive** | **124 W Main St** |
| **First Central National Bank** | **103 S Springfield St** |
| **Tri-County Insurance** | **272 W Main St** |
| **St. Paris Shoppers** | **311 W Main** — groceries / deli / lottery energy |
| **Sunoco** | **355 W Main** area |
| **Subway** | **9751 US Hwy 36 W** |
| **Pony Wagon Museum** | Tourism / history drop |

### Safe vs risky business usage
**Safe:** character stops *at* a place; parking nearby; line length; generic “after the Gloria show.”  
**Risky / avoid:** invented illegal acts, health closures you made up, fake quotes from real owners, invented firings of real people.

---

## Phrase bank (local texture)

- Monument Square / Man on the Monument  
- “Out on 36” / “up 68” / “out Lonesome” / “over toward Cable”  
- The Burg / St. Paris / North Lewisburg / Mutual  
- Indians / Falcons / Hillclimbers / Cardinals / Tigers  
- Brush Lake Road · Springfield Street · Sandusky · High Street  
- Graham wrestling room / state dual energy  
- Champaign Lady / Grimes Field  
- Crybaby Bridge · Little Smokies (Davey Woods) · Cedar Bog (it’s a fen)  
- Hemisphere beans / Simple Coffee corner / Frosty’s / Crabill’s / TeaBaggers / Carmazzi’s  
- Second Saturday · Park Avenue fairgrounds · township trustee night  
- Knee-high-by-the-Fourth agronomy arguments (use sparingly)

---

## Pre-publish authenticity checklist

1. Town + school mascot match?  
2. Street exists in that town (Main is OK only if town is named)?  
3. Highway direction roughly right (36 E–W, 68 N–S)?  
4. Business used only as scenery unless verified?  
5. Not accidentally PA Mechanicsburg or Preble Co. Lewisburg?  
6. At least one **non-US-36** anchor if the last few stories leaned on 36?  
7. Living public figures: no invented crimes?  

---

## Champaign Voices (American Voices–style package)

Separate content type from full stories. Pattern from The Onion’s American Voices:

1. **Headline** — newsy, often absurd  
2. **Lede** — 1–2 sentences of “what happened,” ends with **“What do you think?”**  
3. **Exactly 3 people** — short quote each; stock portrait IDs from `voices_portraits.py` (`asian-man`, `young-white-woman`, etc.); **same 9 faces sitewide, new name + absurd job every piece**

Files: `content/voices/*.md` — see `content/voices/README.md`.  
Live: `/champaign-voices/` · homepage block after Top Stories.

Use this instruct file for local surnames/jobs flavor in the fake bylines (e.g. Evilsizor, “Township Trustee Who Still Says Back When”).

---

## Output path for this project

| Step | Where |
|------|--------|
| Drafts (not live) | `content/drafts/*.md` |
| Live articles | `content/articles/*.md` |
| **Champaign Voices** | `content/voices/*.md` → `/champaign-voices/` |
| Images | `assets/img/` + frontmatter `image: /assets/img/...` |
| Build | `python build.py` → `dist/` |
| CMS | `python admin.py` → http://127.0.0.1:5050 |
| Schedule drip | Future `date:` / `publish_date:`; see `content/drafts/SCHEDULING.md` |

---

## Companion files

| File | Role |
|------|------|
| `references/CHAMPAIGN-COUNTY-INSTRUCT.md` | **This file** — full LLM instruct + reference brain |
| `references/CHAMPAIGN-COUNTY-LOCAL-BIBLE.md` | Shorter place/business quick-lookup (points here for generation) |
| `content/drafts/INDEX.md` | Catalog of earlier draft batch |
| Source research chat export | `fakeburg/context.txt` (raw Q&A; do not feed models the chatter) |
