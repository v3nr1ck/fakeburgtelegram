#!/usr/bin/env python3
"""Append 100 Champaign Voices for the next 100 days (does not wipe existing)."""

from __future__ import annotations

import re
from datetime import date, timedelta
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "content" / "voices"

PORTRAITS = [
    "asian-man",
    "asian-woman",
    "black-man",
    "hispanic-man",
    "hispanic-woman",
    "old-white-man",
    "old-white-woman",
    "young-white-man",
    "young-white-woman",
]

# 100 more: broader current-events texture; small-town voices, not local news
PACKAGES: list[tuple[str, str, list[tuple[str, str, str]]]] = [
    (
        "Congress Votes to Investigate the Investigation of the Investigation",
        "Lawmakers authorized another probe into prior probes, ensuring full employment for lawyers and partial employment for truth. What do you think?",
        [
            ("Harlan Zerkle", "C-SPAN Accidental Historian", "If they investigate any harder, they'll find my unpaid parking ticket from 1998."),
            ("Denise Bodey", "Subcommittee Snack Coordinator", "We need results. Also we need fewer subcommittees."),
            ("Mitch Grove", "Talk Radio Volume Knob", "Investigation is free content. Solutions cost money."),
        ],
    ),
    (
        "AI Writes a Constitution for a Country That Doesn't Exist Yet",
        "A research lab published a model-authored constitution for a hypothetical state, complete with rights, duties, and a suspiciously clean comments section. What do you think?",
        [
            ("Carol Evilsizor", "League of Women Voters Binder Keeper", "If a robot writes the constitution, who do we recall?"),
            ("Troy Pence", "Township Charter Skeptic", "Mine came with coffee stains. That's legitimacy."),
            ("April Ferryman", "School Government Advisor", "At least it probably spelled ' bicameral' right."),
        ],
    ),
    (
        "Major Studio Reboots a Reboot of a Remake Nobody Requested",
        "Hollywood greenlit another layer of nostalgia, promising a fresh take that looks expensive and feels like homework. What do you think?",
        [
            ("Buddy Neer", "VHS Box Set Archivist", "Leave the dead franchises alone."),
            ("Linda Ropp", "Opening Weekend Realist", "I'll watch if the popcorn is free. It's not."),
            ("Greg Huffman", "Man Who Liked the Original Wrongly", "My childhood is not a quarterly earnings call."),
        ],
    ),
    (
        "Federal Agency Issues 400-Page Guidance on How to Read Guidance",
        "A new manual explains how to interpret last year's manuals, a recursive triumph of bureaucracy over daylight. What do you think?",
        [
            ("Earl Fraley", "Form-Filling Endurance Athlete", "I need a summary of the summary."),
            ("Sharon Hedges", "PDF Zoom Specialist", "If it needs guidance, it failed kindergarten."),
            ("Nadine Kizer", "Office Supply Prophet", "Print less. Fear more."),
        ],
    ),
    (
        "Billionaires Race to Buy Glaciers 'For Conservation and Also Bragging'",
        "Ultra-wealthy buyers are acquiring polar and alpine assets framed as climate stewardship that also photographs well on yachts. What do you think?",
        [
            ("Dale Evilsizor", "Ice Tray Traditionalist", "You can't own winter. You can only rent it from God."),
            ("Karen Pence", "Thrift Store Conservationist", "Donate coats. Don't buy a glacier."),
            ("Ron Bodey", "Man Suspicious of Philanthropy Press Releases", "If it's charity, why is there a logo?"),
        ],
    ),
    (
        "Smart Toilets Promise Health Data; America Declines That Level of Friendship",
        "Connected bathroom fixtures that analyze biometrics hit the market, a product category that assumes you want your plumbing to gossip. What do you think?",
        [
            ("Irene Neer", "Privacy Absolutist of the Powder Room", "My toilet does not need Wi-Fi. Full stop."),
            ("Walt Huffman", "Man Who Still Fears Bidets", "If it beeps, I'm moving to the woods."),
            ("Tina Grove", "Gadget Drawer Warden", "Health is good. Surveillance on the throne is a line."),
        ],
    ),
    (
        "National Spelling of 'Canceled' vs 'Cancelled' Reopens Civil Cold War",
        "Style guides and social feeds reignited the one-L versus two-L fight, proving America can divide over anything with vowels. What do you think?",
        [
            ("Harlan Zerkle", "Dictionary That Lives in the Truck", "Spell it how you want. Just pay your taxes."),
            ("Denise Bodey", "Church Bulletin Copy Editor", "Two L's look fancier. One L is faster. Both are tired."),
            ("Mitch Grove", "Autocorrect Hostage", "My phone already decided. I live under occupation."),
        ],
    ),
    (
        "Scientists Teach Rats to Drive Tiny Cars for Science and Content",
        "Researchers reported rodents navigating miniature vehicles, a study equal parts neuroscience and something you forward to your group chat. What do you think?",
        [
            ("Carol Evilsizor", "Science Fair Mom", "If rats can drive, why can't my nephew parallel park?"),
            ("Troy Pence", "DMV Line Theologian", "Issue them licenses. Collect the fees."),
            ("April Ferryman", "Pet Insurance Skeptic", "Don't give them keys. That's how empires fall."),
        ],
    ),
    (
        "Streaming Service Adds 'Skip Intro' to Real Life via AR Glasses Prototype",
        "A tech demo suggested wearable software that could skip small talk, ads, and possibly your uncle's stories, raising ethical questions and hope. What do you think?",
        [
            ("Buddy Neer", "Small Talk Professional", "If you skip my hello, we're fighting."),
            ("Linda Ropp", "Church Greeting Time Escape Artist", "Ship it yesterday."),
            ("Greg Huffman", "Man Who Explains Movies During Movies", "I need the opposite feature: force people to listen."),
        ],
    ),
    (
        "World Bank Warns of Debt Spiral; Households Say Join the Club",
        "Economists flagged rising sovereign debt risks as families nodded along from under their own interest rates. What do you think?",
        [
            ("Earl Fraley", "Minimum Payment Philosopher", "The world has a credit card. We've been there."),
            ("Sharon Hedges", "Envelope Budget Revivalist", "Stop spending. Also keep my programs. Nuance."),
            ("Nadine Kizer", "Grocery Calculator in Her Head", "Wake me when eggs apologize."),
        ],
    ),
    (
        "Celebrity Pastor NFT Baptism Declared Theologically Complicated",
        "A high-profile ministry experimented with digital collectibles tied to spiritual branding, uniting atheists and deacons in shared confusion. What do you think?",
        [
            ("Dale Evilsizor", "Pew Endurance Athlete", "Baptism needs water, not Wi-Fi."),
            ("Karen Pence", "Hymnal Page Turner", "If Jesus needed blockchain, He'd have mentioned it."),
            ("Ron Bodey", "Fellowship Hall Coffee Guard", "Pass the plate. Skip the tokens."),
        ],
    ),
    (
        "Airlines Sell 'Quiet Cabin' Tier That Still Includes Crying Infants and Destiny",
        "Carriers unveiled premium quiet zones with rules that cannot overrule physics, biology, or middle-seat politics. What do you think?",
        [
            ("Irene Neer", "Neck Pillow Constitutionalist", "Quiet is a myth sold by people with better seats."),
            ("Walt Huffman", "Man Who Claps When the Plane Lands", "I paid for noise-canceling headphones. That's my tier."),
            ("Tina Grove", "Armrest Treaty Negotiator", "Sell me legroom. Stop selling vibes."),
        ],
    ),
    (
        "Lab Claims Room-Temperature Superconductor Again; Physics Teachers Sigh Collectively",
        "Another superconductor announcement lit up social media before replication attempts poured cold water, a cycle as reliable as gravity. What do you think?",
        [
            ("Harlan Zerkle", "High School Science Room Fossil", "Wake me when the magnets levitate my truck payment."),
            ("Denise Bodey", "Science Channel Narrator Voice", "Breakthrough means 'press release' until proven."),
            ("Mitch Grove", "Man Who Believes in Magnets Selectively", "If it works, cool. If not, still cool-looking."),
        ],
    ),
    (
        "Cities Mandate Composting; Fruit Flies Form Local Government",
        "New organic-waste rules expanded municipal composting as households learned the politics of banana peels. What do you think?",
        [
            ("Carol Evilsizor", "Countertop Compost Diplomat", "I support the Earth. I do not support the smell."),
            ("Troy Pence", "Trash Day Traditionalist", "One can was enough drama."),
            ("April Ferryman", "Garden Club Realist", "Fine. But give me a bin that raccoons respect."),
        ],
    ),
    (
        "National Park Lottery for Entry Makes Nature Feel Like Concert Tickets",
        "Popular parks expanded lottery systems for access, turning sunrise hikes into something you refresh a browser for. What do you think?",
        [
            ("Buddy Neer", "Scenic Overlook Photographer of Strangers' Heads", "Wilderness should not need StubHub energy."),
            ("Linda Ropp", "Cooler Packing General", "I'll take the ugly park that still lets me in."),
            ("Greg Huffman", "Man Who Parks Creatively", "If I need luck to see a tree, society failed."),
        ],
    ),
    (
        "Phone OS Update Moves Every Button; Marriages Tested Nationwide",
        "A major software release redesigned interfaces overnight, creating a brief era of adults who could not place a call without children present. What do you think?",
        [
            ("Earl Fraley", "Settings Menu Labyrinth Survivor", "If it ain't broke, update it until it is."),
            ("Sharon Hedges", "Screenshot Instructional Designer for Parents", "I run a free tech support nonprofit called Family."),
            ("Nadine Kizer", "Woman Who Taped the Old Icons in Her Mind", "Put the button back or face the consequences."),
        ],
    ),
    (
        "Global Olive Oil Shortage Threatens Salad Diplomacy",
        "Crop failures and demand spikes pushed olive oil prices up, forcing kitchens to confront whether dinner needs Mediterranean authenticity. What do you think?",
        [
            ("Dale Evilsizor", "Butter Absolutist", "I never trusted oil that sounds fancy."),
            ("Karen Pence", "Church Potluck Dressing Authority", "Ranch will fill the void. It always does."),
            ("Ron Bodey", "Man Who Fries in Whatever Is Cheap", "Shortage is just a sale on lard nostalgia."),
        ],
    ),
    (
        "AI Judge Bot Settles Parking Ticket; Appeals Court Files Existential Motion",
        "A pilot program let software adjudicate minor citations, saving time and creating new grounds for 'the robot hates my car' appeals. What do you think?",
        [
            ("Irene Neer", "Meter Feeding Olympian", "If the robot is fair, fine. If it's wrong, I want a face to glare at."),
            ("Walt Huffman", "Parking Lot Philosopher", "My truck has rights. Sort of."),
            ("Tina Grove", "City Hall Line Veteran", "Faster injustice is still injustice. Also faster is nice."),
        ],
    ),
    (
        "Fashion Declares Cargo Pants Back; Pockets Celebrate Quietly",
        "Runways re-embraced cargo pants, validating people who never stopped dressing like they might need a multitool at dinner. What do you think?",
        [
            ("Harlan Zerkle", "Pocket Constitutionalist", "I never left. The fashion people did."),
            ("Denise Bodey", "Purse Minimalist", "Pockets are gender justice. Fight me."),
            ("Mitch Grove", "Jeans With Fake Pockets Victim", "If it can't hold my phone, it's a costume."),
        ],
    ),
    (
        "Satellite Megaconstellations Light Up Night Sky; Stargazers File Emotional Damages",
        "Astronomers warned that expanding satellite fleets are streaking night-sky images, a tradeoff between rural broadband and cosmic romance. What do you think?",
        [
            ("Carol Evilsizor", "Front Porch Astronomer", "I wanted stars. I got a slide show of capitalism."),
            ("Troy Pence", "Man Who Just Got Decent Internet", "Sorry, cosmos. I needed weather radar."),
            ("April Ferryman", "Telescope Birthday Gift Receiver", "Can we dim the future a little?"),
        ],
    ),
    (
        "Congress Debates TikTok Ban While Live-Tweeting the Hearing",
        "Lawmakers grilled tech executives about a foreign-owned app using the same attention economy they claim to fear. What do you think?",
        [
            ("Buddy Neer", "Man Who Calls All Apps Facebook", "Ban it. Keep the grandkid videos somehow."),
            ("Linda Ropp", "Silent Scroll Observer", "They'll ban the fun and keep the ads."),
            ("Greg Huffman", "National Security Lawn Chair", "If China wants my chili recipe, they can ask."),
        ],
    ),
    (
        "Hospitals Report Record ER Boarding; Waiting Rooms Achieve Sentience",
        "Overcrowding left patients in hallways for hours as staff juggled capacity, a crisis that makes 'take a number' feel optimistic. What do you think?",
        [
            ("Earl Fraley", "Magazine From 2019 Reader", "I brought snacks like it's a siege."),
            ("Sharon Hedges", "Nurse Appreciation Casserole Deliverer", "Pay nurses. Build beds. Skip the slogans."),
            ("Nadine Kizer", "Clipboard Form Calligrapher", "If I'm vertical, they call it fine. I'm not fine."),
        ],
    ),
    (
        "Electric Vehicle Charging Etiquette Wars Break Out in Parking Lots",
        "As chargers spread, so did conflicts over ICEing spots, charge-hogging, and whether a 12-minute top-up justifies a strongly worded note. What do you think?",
        [
            ("Dale Evilsizor", "Gas Pump Nostalgist", "At least gas doesn't require a support group."),
            ("Karen Pence", "Note-Under-Wiper Author", "Move your fully charged ego."),
            ("Ron Bodey", "Adapter Cable Hoarder", "I brought three cords. I am the infrastructure."),
        ],
    ),
    (
        "Study Says Loneliness Epidemic Continues; Group Chats Offer Quantity Not Quality",
        "Public health voices framed social isolation as a major risk while digital connection multiplied without fixing the ache. What do you think?",
        [
            ("Irene Neer", "Porch Wave Enforcement Officer", "Wave at people. It's free medicine."),
            ("Walt Huffman", "Coffee Shop Regular Without AirPods", "Sit with someone. Suffer in person."),
            ("Tina Grove", "Family Reunion RSVP Manager", "We are lonely together on purpose. Fixable."),
        ],
    ),
    (
        "Major Bank Adds 'Financial Wellness' Tips While Charging Overdraft Poetry",
        "A consumer bank launched wellness content about budgeting that arrived in the same app that fee'd users for existing. What do you think?",
        [
            ("Harlan Zerkle", "Mattress Bank Traditionalist", "Don't advise me while you pick my pocket."),
            ("Denise Bodey", "Spreadsheet Anxiety Hobbyist", "Wellness is not a push notification."),
            ("Mitch Grove", "Man Who Rounds Up for 'Charity'", "I'll take fewer tips and fewer fees."),
        ],
    ),
    (
        "Antarctica Sees Record Heat Day; Penguins Decline Interview Requests",
        "Climate monitors reported extreme Antarctic temperatures relative to norms, a data point that should scare more people than it entertains. What do you think?",
        [
            ("Carol Evilsizor", "Thermostat War Veteran", "If the ice is sweating, listen."),
            ("Troy Pence", "Man Who Calls Climate 'Weather With Homework'", "It's far away until it isn't."),
            ("April Ferryman", "Science Teacher Who Deserves a Raise", "This is the homework. Do it."),
        ],
    ),
    (
        "Gaming Company Patents Feeling of FOMO; Lawyers High-Five",
        "A studio filed intellectual property claims around engagement mechanics critics call addictive by design. What do you think?",
        [
            ("Buddy Neer", "Intergenerational Controller Passer", "You can't patent anxiety. You can only monetize it."),
            ("Linda Ropp", "Parent of a Battle Pass", "If it dings, it's a slot machine."),
            ("Greg Huffman", "Man Who Unplugs for Lent Sometimes", "Patent denied by God."),
        ],
    ),
    (
        "Universities Deploy Drone Campuses for Remote Labs; Tuition Unchanged",
        "Schools piloted remote lab experiences via robots and cameras while the bill remained stubbornly physical. What do you think?",
        [
            ("Earl Fraley", "Student Loan Statement Avoider", "If I'm paying full price, I want full gravity."),
            ("Sharon Hedges", "Lab Goggles Nostalgia", "Science needs smells. Drones don't smell."),
            ("Nadine Kizer", "Scholarship Essay Trauma Survivor", "Cut costs or cut the speech about innovation."),
        ],
    ),
    (
        "Meat Recall Expands; Grill Season Enters Trust Issues Arc",
        "A multistate recall hit popular protein brands, turning cookouts into label-reading seminars. What do you think?",
        [
            ("Dale Evilsizor", "Charcoal Loyalty Program", "I cook it hotter. That's my food safety."),
            ("Karen Pence", "Sell-By Date Mystic", "When in doubt, throw it out. When broke, pray."),
            ("Ron Bodey", "Smoker Temperature Whisperer", "Recall my weekend. Rude."),
        ],
    ),
    (
        "Supreme Court Shadows Docket Grows; Public Still Thinks They Wear Wigs",
        "The Court's emergency orders continued shaping policy between full opinions as civics knowledge remained optional in comment sections. What do you think?",
        [
            ("Irene Neer", "Constitution Pocket Copy Owner", "Just explain it in English after."),
            ("Walt Huffman", "Man Who Confuses Courts on Purpose", "Nine people in robes run more than my HOA. Concerning."),
            ("Tina Grove", "School House Rock Karaoke Lead", "We need more cartoons and fewer takes."),
        ],
    ),
    (
        "Startup Sells Air as a Subscription for 'Optimized Breathing Spaces'",
        "A wellness company marketed premium purified air memberships for homes and offices, a product for people who forgot windows open. What do you think?",
        [
            ("Harlan Zerkle", "Screen Door Philosopher", "Air is free. Stop it."),
            ("Denise Bodey", "Candle Scent Maximalist", "I'll open a window before I pay for oxygen cosplay."),
            ("Mitch Grove", "Furnace Filter Replacement Procrastinator", "Subscription breathing is late-stage nonsense."),
        ],
    ),
    (
        "National Weather Service Upgrades Alarms; Phones Become Tornado Sirens With Ads",
        "More aggressive mobile alerts rolled out for extreme weather, saving lives and interrupting dinners with equal efficiency. What do you think?",
        [
            ("Carol Evilsizor", "Basement Battery Organizer", "Alert me. Then stop selling me boots in the same minute."),
            ("Troy Pence", "Scanner App Addict", "I want sirens, not sponsorships."),
            ("April Ferryman", "Family Group Chat Disaster Admin", "Forward the alert. Skip the theories."),
        ],
    ),
    (
        "Olympics Allow More Professionalism; Amateur Spirit Files for Unemployment",
        "Rule changes continued blurring amateur and pro lines as the Games embraced the reality that excellence is expensive. What do you think?",
        [
            ("Buddy Neer", "Couch Flag Waver", "Pay athletes. Sell fewer commemorative coins."),
            ("Linda Ropp", "Opening Ceremony Costume Critic", "I watch for sequins and national drama."),
            ("Greg Huffman", "Man Who Calls Everything a Distraction", "Bread and circuses, but with vaults."),
        ],
    ),
    (
        "ChatGPT-Style Tools Start Passing Medical Exams; Bedside Manner Still Human-Only",
        "Language models scored well on benchmark tests while clinicians noted that empathy is not a multiple-choice section. What do you think?",
        [
            ("Earl Fraley", "Waiting Room Philosopher", "The robot can study. I want a person who flinches with me."),
            ("Sharon Hedges", "Second Opinion Collector", "Use AI for paperwork. Not for the scary parts."),
            ("Nadine Kizer", "Nurse Appreciation Society", "Help nurses first. Then brag about models."),
        ],
    ),
    (
        "Cities Try Daytime Curfews for Scooters; Scooters Do Not Read Signs",
        "Municipal rules targeted shared e-scooters after sidewalk chaos, a policy clash between convenience and ankles. What do you think?",
        [
            ("Dale Evilsizor", "Sidewalk Territorial Governor", "If it has wheels and no license, walk it."),
            ("Karen Pence", "Ankle Integrity Advocate", "Ban the silent ones that appear behind you like ghosts."),
            ("Ron Bodey", "Man Who Almost Bought One", "Fun until you meet a curb with opinions."),
        ],
    ),
    (
        "Film Industry Says Theatrical Is Back; Couches Remain Unconvinced",
        "Studios touted box office rebounds while living rooms continued offering cheaper snacks and pause buttons. What do you think?",
        [
            ("Irene Neer", "Matinee Discount Hunter", "I'll go out if the popcorn isn't a car payment."),
            ("Walt Huffman", "Remote Control Monarch", "My couch doesn't shush me."),
            ("Tina Grove", "Spoiler Avoidance Monk", "Theaters are for events. Tuesday nights are for blankets."),
        ],
    ),
    (
        "Gene Therapy Price Tags Hit Millions; Insurers Practice Looking Away",
        "Breakthrough treatments with life-changing potential arrived with invoices that look like national budgets. What do you think?",
        [
            ("Harlan Zerkle", "Deductible Shock Absorber", "Cure me in installments I can understand."),
            ("Denise Bodey", "GoFundMe Fatigue Patient", "Healthcare shouldn't be a bake sale."),
            ("Mitch Grove", "Man Who Reads Explanation of Benefits Like Horror", "If it works, society should act like it matters."),
        ],
    ),
    (
        "Retailers Put Security Cases on Everything Including Socks",
        "Theft-prevention packaging expanded across aisles, turning simple shopping into a scavenger hunt for an employee with keys. What do you think?",
        [
            ("Carol Evilsizor", "Customer Service Bell Tapper", "I just want toothpaste without a hostage negotiation."),
            ("Troy Pence", "Man Who Leaves the Cart", "If socks are locked up, the culture failed."),
            ("April Ferryman", "Self-Checkout Moral Crisis", "Trust is dead. Long live the plastic case."),
        ],
    ),
    (
        "Mars Time Zones Proposed for Future Colonies; Earth Meetings Get Worse",
        "Engineers discussed clocks for multi-planet operations as remote work already made scheduling a war crime. What do you think?",
        [
            ("Buddy Neer", "Calendar Invite Victim", "We can't schedule three people on Earth. Sit down, Mars."),
            ("Linda Ropp", "Church Potluck Timing Authority", "Pick a time. Bring a dish. Leave space alone."),
            ("Greg Huffman", "Man Late to Everything On Purpose", "New zones just mean new excuses."),
        ],
    ),
    (
        "National Archives Release More UFO Files; Aliens Still on Read",
        "Declassified documents fueled another cycle of sightings, black bars, and confidence without evidence. What do you think?",
        [
            ("Earl Fraley", "Night Sky Smoker of One Cigar a Year", "If they're here, they hate our weather too."),
            ("Sharon Hedges", "Conspiracy Diet Moderator", "I want disclosure and also better cable."),
            ("Nadine Kizer", "Skeptic With a Porch Light", "Show me a ship or let me sleep."),
        ],
    ),
    (
        "Fast Fashion Shipments Face New Fees; Closets Breathe a Little",
        "Policy shifts and shipping costs hit ultra-cheap apparel hauls, a minor speed bump for impulse polyester. What do you think?",
        [
            ("Dale Evilsizor", "Flannel Economist", "Buy fewer shirts that survive one wash."),
            ("Karen Pence", "Thrift Store Sniper", "Secondhand is the original fast fashion killer."),
            ("Ron Bodey", "Man With Five Identical Work Shirts", "I don't need trends. I need pockets."),
        ],
    ),
    (
        "AI Voice Actors Unionize Before They Technically Exist",
        "Performers and unions pushed contracts covering synthetic voice clones as studios tested cheaper audio pipelines. What do you think?",
        [
            ("Irene Neer", "Church Choir Alto With Standards", "If it sounds like a person, pay a person."),
            ("Walt Huffman", "Radio Booth Nostalgist", "My voice is not freeware."),
            ("Tina Grove", "Audiobook Insomniac", "I can tell when the soul is missing."),
        ],
    ),
    (
        "State Bans Lab-Grown Meat; Grill Culture Declares Victory Lap",
        "A statehouse moved to restrict cultivated meat sales, framing tradition as policy while startups called it fear with a gavel. What do you think?",
        [
            ("Harlan Zerkle", "Beef Loyalty Program", "Cows built this country. Sort of."),
            ("Denise Bodey", "Grocery Budget Realist", "If it's safe and cheaper, stop panicking."),
            ("Mitch Grove", "Sauce Diplomacy Expert", "I'll taste it before I vote on it."),
        ],
    ),
    (
        "Social Platform Tests Chronological Feed Again Like It Invented Time",
        "An app reintroduced chronological sorting as a premium-feeling feature that used to be called 'how things work.' What do you think?",
        [
            ("Carol Evilsizor", "Timeline Hostage", "Put it back and leave it. No toggle games."),
            ("Troy Pence", "Man Who Misses When Posts Had Dates That Made Sense", "Algorithm who? Just show me the lies in order."),
            ("April Ferryman", "Muted Relatives Curator", "Chronological still includes uncle theories. Progress."),
        ],
    ),
    (
        "Global Chipmakers Build Factories Everywhere; Local Housing Feels It First",
        "Semiconductor investment booms reshaped towns with jobs, traffic, and rents that moved faster than wages. What do you think?",
        [
            ("Buddy Neer", "Factory Town Memory Keeper", "Jobs yes. Displacement no. Both can be true."),
            ("Linda Ropp", "Rent Receipt Historian", "Bring industry if you bring apartments."),
            ("Greg Huffman", "Commute Time Theologian", "My drive is now a part-time job."),
        ],
    ),
    (
        "Doctors Warn About Ultra-Marathon Culture; Humans Keep Signing Up Anyway",
        "Medical voices cautioned about extreme endurance trends as registrants treated 100 miles like a personality. What do you think?",
        [
            ("Earl Fraley", "Porch Sitting Olympian", "My knees filed a dissenting opinion."),
            ("Sharon Hedges", "5K Once in 2014 Finisher", "Walk the dog. Leave the ER beds free."),
            ("Nadine Kizer", "Compression Sock Diplomat", "If it requires a GoFundMe for toenails, rethink it."),
        ],
    ),
    (
        "Government Tries Digital Dollar Pilot; Cash Loyalists Buy More Safes",
        "A limited CBDC-style pilot drew predictable panic and curiosity about programmable money. What do you think?",
        [
            ("Dale Evilsizor", "Cash-Only Diner Regular", "Paper money doesn't need an update."),
            ("Karen Pence", "Venmo Boundary Setter", "I'll try it when my aunt can too."),
            ("Ron Bodey", "Gold Coin Gift Shop Browser", "If they can turn it off, it's not mine."),
        ],
    ),
    (
        "Hollywood Strike Echoes Fade; AI Background Extras Quietly Multiply",
        "After labor fights cooled, synthetic crowd tools kept spreading through production pipelines with less press and more pixels. What do you think?",
        [
            ("Irene Neer", "Movie Theater Butter Budgeter", "Pay the humans in the blur too."),
            ("Walt Huffman", "Man Who Watches Credits", "If nobody is real, why is popcorn real-priced?"),
            ("Tina Grove", "SAG-Curious Aunt", "Unions exist for this exact nonsense."),
        ],
    ),
    (
        "National Debt Interest Exceeds Popular Programs; Math Becomes a Campaign Issue Briefly",
        "Budget hawks highlighted interest costs overtaking familiar line items before attention returned to vibes. What do you think?",
        [
            ("Harlan Zerkle", "Household Interest Rate Trauma Patient", "Compound interest is a horror genre."),
            ("Denise Bodey", "Coupon Stacking Grandmaster", "Stop charging the future for today's speeches."),
            ("Mitch Grove", "Man Who Understands Debt Until the Graph Appears", "Show me the graph with groceries on it."),
        ],
    ),
    (
        "Smartwatches Detect More Diseases; Users Detect More Anxiety",
        "Wearables expanded health alerts that save lives and also ruin brunch with vibration-based dread. What do you think?",
        [
            ("Carol Evilsizor", "Step Count Theologian", "If my watch panics, I panic. Then I eat toast."),
            ("Troy Pence", "Man Who Won't Wear a Ring That Spies", "My pulse is not content."),
            ("April Ferryman", "Doctor Google in Recovery", "Alert me for real emergencies only."),
        ],
    ),
    (
        "Countries Form AI Safety Pact With Verbs Stronger Than Enforcement",
        "A multinational statement promised responsible AI development using language optimized for applause not audits. What do you think?",
        [
            ("Buddy Neer", "Committee Minutes Translator", "Pacts without teeth are group chats."),
            ("Linda Ropp", "Science Fair Ribbon Presenter", "Write rules a 10-year-old can check."),
            ("Greg Huffman", "Man Who Wants Simple Bans", "Don't build the Skynet. Meeting adjourned."),
        ],
    ),
    (
        "Grocery Stores Test AI Carts That Follow You; Dignity Files a Complaint",
        "Autonomous shopping carts piloted in select markets, promising convenience and delivering a robot that knows you buy the same sad cereal. What do you think?",
        [
            ("Earl Fraley", "Cart Wheel Fighter", "I can push my own judgment."),
            ("Sharon Hedges", "List on the Back of an Envelope", "If it follows me, it better not chirp."),
            ("Nadine Kizer", "Self-Checkout Moral Crisis", "One more robot between me and milk."),
        ],
    ),
    (
        "Space Hotel Concept Art Drops; Earth Hotels Still Can't Get the Ice Machine Right",
        "Tourism companies shared glossy plans for orbital lodging while terrestrial hospitality continued basic struggles. What do you think?",
        [
            ("Dale Evilsizor", "Ice Machine Kicker", "Fix Earth ice first."),
            ("Karen Pence", "Loyalty Points Mystic", "I'll stay somewhere with gravity and coffee."),
            ("Ron Bodey", "Man Who Hates Recycled Air", "Space hotel is a fancy tin can."),
        ],
    ),
    (
        "Public Schools Debate Phone Pouches; Students Debate Human Rights",
        "Districts expanded locked-away phone policies during class as teens framed it as tyranny and teachers framed it as Tuesday. What do you think?",
        [
            ("Irene Neer", "Teacher's Lounge Diplomat", "Pouch the phones. Save the lesson."),
            ("Walt Huffman", "Man Who Survived Boredom", "We had notes on paper. We lived."),
            ("Tina Grove", "Parent of a Notification Center", "Take the phone. Leave me a way to reach the office."),
        ],
    ),
    (
        "Insurance Drops Coverage in Risk Zones; Maps Become Destiny",
        "Carriers withdrew from high-risk regions citing climate losses, leaving homeowners to navigate residual markets and rage. What do you think?",
        [
            ("Harlan Zerkle", "Roof Estimate Collector", "They take premiums in the sun and leave in the storm."),
            ("Denise Bodey", "Claims Call Hold Music Critic", "Coverage should mean something on bad days."),
            ("Mitch Grove", "Man Who Reads the Fine Print Too Late", "The map shouldn't erase the neighborhood."),
        ],
    ),
    (
        "Influencer Nation Sells Water With a Backstory; Tap Water Feels Insecure",
        "Bottled water brands leaned into origin myths and aesthetics while municipal water stayed cheaper and less photogenic. What do you think?",
        [
            ("Carol Evilsizor", "Tap Water Loyalist", "My sink doesn't need a lore document."),
            ("Troy Pence", "Hydration Bro Skeptic", "If it needs a podcast, it's not water."),
            ("April Ferryman", "Reusable Bottle That Tastes Like Plastic", "Marketing is dry. Drink the tap."),
        ],
    ),
    (
        "Robotaxis Expand Service Area; Steering Wheel Collectors Form Clubs",
        "Autonomous ride-hail grew into new cities amid crashes, hype, and the slow death of small talk with drivers. What do you think?",
        [
            ("Buddy Neer", "Cab Driver Philosopher Fan", "I miss complaining to a person about traffic."),
            ("Linda Ropp", "Back Seat Prayer Whisperer", "If there's no driver, who do I thank for arriving alive?"),
            ("Greg Huffman", "Man Who Distrusts Cars That Think", "I'll drive myself into the sunset, thanks."),
        ],
    ),
    (
        "National Park Bans Drones Over Nesting Areas; Content Creators Grieve Publicly",
        "Wildlife protections limited aerial filming as creators argued about art, access, and bird boundaries. What do you think?",
        [
            ("Earl Fraley", "Binocular Traditionalist", "Let the birds parent without a soundtrack."),
            ("Sharon Hedges", "Trail Etiquette Lecturer", "Your content is not more important than a nest."),
            ("Nadine Kizer", "Phone Video of a Deer Archivist", "Zoom with your feet. Quietly."),
        ],
    ),
    (
        "Economy Adds Jobs People Don't Want at Wages People Can't Use",
        "Headlines celebrated employment numbers while workers described openings that ignore rent, childcare, and dignity. What do you think?",
        [
            ("Dale Evilsizor", "Help Wanted Sign Anthropologist", "A job isn't a favor if it can't pay the light bill."),
            ("Karen Pence", "Two-Income Household CFO", "Count jobs that count."),
            ("Ron Bodey", "Man Who Worked Since 16", "Work hard. Also get paid like it's the current century."),
        ],
    ),
    (
        "Scientists Map Human Brain Connections; Comment Section Remains Unmapped",
        "A major connectomics milestone advanced understanding of neural wiring as online discourse stayed proudly unexamined. What do you think?",
        [
            ("Irene Neer", "Crossword Puzzle Neuroscientist", "Map my brain after you map why I open the fridge twice."),
            ("Walt Huffman", "Man Who Thinks Feelings Are Optional", "Interesting. Still not going to therapy."),
            ("Tina Grove", "Podcast Half-Listener", "We're complicated. Act accordingly."),
        ],
    ),
    (
        "Sports League Adds More International Games; Jet Lag Becomes a Stat",
        "Leagues chased global audiences with overseas matchups that test bodies, TV times, and loyalty at 8 a.m. local. What do you think?",
        [
            ("Harlan Zerkle", "Bar Stool Statistician", "I'll watch at any hour if wings are involved."),
            ("Denise Bodey", "Youth Sports Scheduler", "Players need sleep. Owners need money. Guess who wins."),
            ("Mitch Grove", "Man Who Records Everything", "Spoilers are the real rival now."),
        ],
    ),
    (
        "Browser Vendors Kill Third-Party Cookies; Ad Trackers Learn New Shapes",
        "Privacy changes forced advertisers to adapt tracking methods that users experience as slightly different creepy. What do you think?",
        [
            ("Carol Evilsizor", "Reject All Button Speedrunner", "I reject all and still see boots."),
            ("Troy Pence", "Incognito Mode False Security", "If it's free, invent a new way to sell me."),
            ("April Ferryman", "Woman Who Reads One Line of the Popup", "Just show the article."),
        ],
    ),
    (
        "Lab-Grown Coffee Experiments Proceed; Morning People Remain Hostage",
        "Biotech firms pursued coffee without traditional farming constraints while caffeine dependency stayed fully natural. What do you think?",
        [
            ("Buddy Neer", "Drip Coffee Fundamentalist", "If it wakes me up, stop explaining the lab."),
            ("Linda Ropp", "Church Coffee Urn Technician", "I'll try it after the regular pot runs out."),
            ("Greg Huffman", "Gas Station Coffee Connoisseur", "Taste is politics. Caffeine is law."),
        ],
    ),
    (
        "Countries Debate Gene Editing in Embryos; Ethics Boards Stock Up on Coffee",
        "Scientific advances reopened fierce arguments about heritable human editing, hope for disease, and slippery slopes with real cliffs. What do you think?",
        [
            ("Earl Fraley", "Church Basement Ethics Seminar", "Cure suffering. Don't design fashion babies."),
            ("Sharon Hedges", "Parent of a Kid With a Hard Diagnosis", "If it saves lives, don't sneer from a safe body."),
            ("Nadine Kizer", "Science Fair Judge", "Slow is okay when the stakes are people."),
        ],
    ),
    (
        "Airline Miles Devalue Overnight; Loyalty Becomes a Situationship",
        "Program changes quietly made free flights less free as frequent flyers refreshed apps in stages of grief. What do you think?",
        [
            ("Dale Evilsizor", "Points Spreadsheet Monk", "I earned those miles in middle seats. Honor them."),
            ("Karen Pence", "Upgrade Whisperer", "Loyalty without rewards is just branding."),
            ("Ron Bodey", "Man Who Pays Cash Like a Peasant Proudly", "I never trusted pretend money."),
        ],
    ),
    (
        "Smart Fridge Orders Groceries Autonomously; Bank Account Files Restraining Order",
        "Connected appliances with auto-replenish features created surprise orders and a new genre of marital debate. What do you think?",
        [
            ("Irene Neer", "List on the Fridge Traditionalist", "My fridge does not get a credit card."),
            ("Walt Huffman", "Man Who Eats Leftovers as a Personality", "If it orders kale again, unplug it."),
            ("Tina Grove", "Coupon Binder Archivist", "Autonomy is fine until it buys premium cheese."),
        ],
    ),
    (
        "UN Votes on Plastic Treaty Language for the 19th Time",
        "Negotiators refined adjectives around binding limits as oceans continued collecting evidence. What do you think?",
        [
            ("Harlan Zerkle", "Reusable Bag Lost-and-Found", "Binding or bust. Stop the catered stalling."),
            ("Denise Bodey", "Blue Bin Optimist in Crisis", "I've washed trash for years. Your move, nations."),
            ("Mitch Grove", "Man Who Still Uses Butter Containers", "Less speech. More less plastic."),
        ],
    ),
    (
        "Teen Sleep Study Blames Phones; Teens Blame Sunrise",
        "Researchers linked late-night scrolling to sleep loss as adolescents proposed later school starts and darker curtains. What do you think?",
        [
            ("Carol Evilsizor", "School Start Time Lobby of One", "Start school later. The sun can wait."),
            ("Troy Pence", "Man Who Wakes at 5 for No Reason", "Phones bad. Discipline good. Nuance unavailable."),
            ("April Ferryman", "Charger Cable Confiscator", "Dock the phone outside the bedroom. Revolutionary."),
        ],
    ),
    (
        "Major Publisher Uses AI to 'Assist' Novels; Readers Demand a Human to Blame",
        "A house admitted AI-assisted drafting on select titles, sparking refund requests and philosophical fights about authorship. What do you think?",
        [
            ("Buddy Neer", "Library Late-Fee Survivor", "If a robot wrote it, put the robot on the book tour."),
            ("Linda Ropp", "Book Club Snack Captain", "I want a person to argue with about the ending."),
            ("Greg Huffman", "Man Who Still Buys Paperbacks", "Ink should have a pulse."),
        ],
    ),
    (
        "National Guard Deployments Dominate Headlines; Local Bake Sales Continue Anyway",
        "High-profile domestic deployments filled cable news as everyday community life proceeded with casseroles and quieter fears. What do you think?",
        [
            ("Earl Fraley", "VFW Coffee Pot Guardian", "Take it seriously. Also check on your neighbors."),
            ("Sharon Hedges", "Prayer Chain Network Admin", "I can pray and still want answers."),
            ("Nadine Kizer", "Woman Who Mutes Cable for Sanity", "Noise isn't the same as understanding."),
        ],
    ),
    (
        "Fitness App Sells AI Trainer That Shames You With Better Grammar",
        "Workout software added generative coaching that critiques form and life choices in polished sentences. What do you think?",
        [
            ("Dale Evilsizor", "Gym Membership Ghost", "I don't need eloquence. I need knees."),
            ("Karen Pence", "Walking as Exercise Purist", "My dog already coaches me. He's cheaper."),
            ("Ron Bodey", "Pushup Form Philosopher", "If it beeps at me, I quit."),
        ],
    ),
    (
        "Trade Negotiators Argue Over Chips, Cars, and Whose Farmers Are More Sacred",
        "International talks bundled semiconductors and agriculture into one tense package only lobbyists could love. What do you think?",
        [
            ("Irene Neer", "Farmers Market Loyalty Program", "Don't trade away the people who grow dinner."),
            ("Walt Huffman", "Factory Shift Memory", "Chips and corn can both matter. Act like adults."),
            ("Tina Grove", "Price Tag Photographer for Group Chat", "If my cart goes up, the treaty failed."),
        ],
    ),
    (
        "Browser History Subpoena Fights Reignite; Everyone Suddenly Cares About Privacy",
        "Legal battles over access to personal browsing data made privacy popular again for one news cycle. What do you think?",
        [
            ("Harlan Zerkle", "Incognito Mode Theologian", "My searches are between me and regret."),
            ("Denise Bodey", "Password Sticky-Note Curator", "Privacy until it's inconvenient, then hypocrisy."),
            ("Mitch Grove", "Man Who Googles Symptoms at 2 a.m.", "That history is medical and embarrassing. Hands off."),
        ],
    ),
    (
        "Cities Install 'Smart' Streetlights That Dim and Also Occasionally Spy Debates",
        "Adaptive lighting promised energy savings while camera-adjacent features revived surveillance arguments on neighborhood apps. What do you think?",
        [
            ("Carol Evilsizor", "Porch Light Traditionalist", "Light the street. Don't audition me."),
            ("Troy Pence", "Man Who Waves at Every Camera", "If it prevents crime without a lecture, okay."),
            ("April Ferryman", "Night Walker With a Dog", "Safety yes. Creepy firmware no."),
        ],
    ),
    (
        "Streaming Wars Force Yet Another Password Reshuffle Across Households",
        "Account crackdowns continued as families reconfigured who lives in whose 'household' for legal fiction purposes. What do you think?",
        [
            ("Buddy Neer", "Password Patriarch", "My household is a state of mind."),
            ("Linda Ropp", "Cousin in Another Zip Code", "I'll visit monthly for login communion."),
            ("Greg Huffman", "Pirate Bay Moral Crisis Patient", "They trained us to share. Shocked Pikachu."),
        ],
    ),
    (
        "Lab Reports Microplastics in Testicles; Public Runs Out of Punchlines",
        "A study detecting microplastics in reproductive tissue briefly united comedy and dread before fading under newer horrors. What do you think?",
        [
            ("Earl Fraley", "Man Who Suddenly Supports Glass", "Stop putting the ocean in my body."),
            ("Sharon Hedges", "Plastic Container Archaeologist", "I've been microwaving regret for years."),
            ("Nadine Kizer", "Reusable Everything Exhausted Person", "Policy. Not vibes. Policy."),
        ],
    ),
    (
        "Candidates Campaign in Video Games; NPC Voters Remain Skeptical",
        "Political outreach moved into gaming platforms to chase young voters with avatars and awkward emotes. What do you think?",
        [
            ("Dale Evilsizor", "Controller Dual-Wield Grandpa", "If you can't pronounce the game, don't campaign in it."),
            ("Karen Pence", "Parent Who Pays the V-Bucks", "Talk policy, not skins."),
            ("Ron Bodey", "Man Who Thinks Games Rot Brains Selectively", "Vote in real life. The pixels can wait."),
        ],
    ),
    (
        "Electric Grid Adds Batteries the Size of Warehouses; HOAs Add Complaints",
        "Utility-scale storage projects broke ground amid local fights over viewsheds, safety, and the aesthetics of progress. What do you think?",
        [
            ("Irene Neer", "Not In My Backyard With Nuance", "Power me without turning the horizon into a box farm if possible."),
            ("Walt Huffman", "Generator Bragging Rights", "Batteries beat blackouts. Build them smart."),
            ("Tina Grove", "Meeting Comment Timer", "Bring snacks to the hearing. Stay until the end."),
        ],
    ),
    (
        "Fashion Houses Sell $500 'Work Boot' Unfit for Work",
        "Designer boots mimicked jobsite footwear at luxury prices that would not survive a single muddy driveway. What do you think?",
        [
            ("Harlan Zerkle", "Actual Work Boot Owner", "If they can't take salt and oil, they're costumes."),
            ("Denise Bodey", "Clearance Rack Olympian", "My boots cost less and have stories."),
            ("Mitch Grove", "Mudroom Philosopher", "Function first. Influencer second."),
        ],
    ),
    (
        "AI Transcription Errors Enter Court Records; Typos Become Precedent Adjacent",
        "Automated transcripts introduced inventively wrong words into legal processes, creating a new genre of 'the computer heard wrong' motions. What do you think?",
        [
            ("Carol Evilsizor", "Court Stenographer Respect Society", "Pay humans who hear nuance."),
            ("Troy Pence", "Man Who Mishears on Purpose", "If the record lies, justice stumbles."),
            ("April Ferryman", "Spellcheck Hostage", "Read it twice before you swear on it."),
        ],
    ),
    (
        "Global Fertility Tech Market Booms; Babies Remain Expensive Hobby",
        "Investment poured into fertility startups as families faced costs that make 'just have kids' advice sound like satire. What do you think?",
        [
            ("Buddy Neer", "Grandparent Babysitting With Opinions", "Help people afford kids or stop the lectures."),
            ("Linda Ropp", "Daycare Waitlist Veteran", "It's not a mystery. It's math."),
            ("Greg Huffman", "Man Who Thinks Everyone Should Figure It Out", "We figured it out. The numbers said no."),
        ],
    ),
    (
        "Museums Use AI to Restore Damaged Art; Purists Demand Original Cracks",
        "Restoration tools filled gaps in historic works, delighting some visitors and enraging authenticity hawks. What do you think?",
        [
            ("Earl Fraley", "Antique Mall Moral Philosopher", "Fix it enough to see it. Don't plastic-surgery the past."),
            ("Sharon Hedges", "Gift Shop Magnet Collector", "I like pretty. Sue me."),
            ("Nadine Kizer", "Art History Elective Survivor", "Label what the robot did. Honesty is the frame."),
        ],
    ),
    (
        "National Beef Over Seed Oils Continues; Cast Iron Influencers Ascendant",
        "Nutrition culture wars elevated seed oils into villains as home cooks rediscovered lard with missionary zeal. What do you think?",
        [
            ("Dale Evilsizor", "Crisco Historian", "Everything is bad until it isn't. Fry the fish."),
            ("Karen Pence", "Butter Absolutist", "Butter is a personality and a cooking medium."),
            ("Ron Bodey", "Grill As Primary Identity", "Smoke solves discourse."),
        ],
    ),
    (
        "Tech CEOs Promise Water-Positive Data Centers Next to Droughts",
        "Companies pledged water stewardship for AI infrastructure in dry regions, a sentence that requires diagrams and trust. What do you think?",
        [
            ("Irene Neer", "Rain Barrel Idealist", "Don't put a thirsty computer in a thirsty place without receipts."),
            ("Walt Huffman", "Well Water Bragging Rights", "Water is not a branding exercise."),
            ("Tina Grove", "Lawn Peer Pressure Victim", "My grass can suffer. Towns shouldn't."),
        ],
    ),
    (
        "Pop Star's AI Clone Tour Proposed; Fans Split Into Philosophical Factions",
        "A promoter floated concerts featuring a digital likeness, forcing debates about art, consent, and ticket prices for ghosts. What do you think?",
        [
            ("Harlan Zerkle", "Classic Rock Radio Hostage", "If the singer isn't sweating, I'm not paying."),
            ("Denise Bodey", "Concert Earplug Mother", "Holograms don't hug the crowd."),
            ("Mitch Grove", "Merch Table Economist", "I'll watch a screen at home for free."),
        ],
    ),
    (
        "States Compete to Host Chip Plants With Tax Breaks Visible From Space",
        "Incentive packages for semiconductor fabs grew so large locals asked who exactly was winning. What do you think?",
        [
            ("Carol Evilsizor", "School Levy Campaign Scar Veteran", "Jobs yes. Blank checks no."),
            ("Troy Pence", "Property Tax Philosopher", "If corporations get breaks, so do people with roofs."),
            ("April Ferryman", "Chamber of Commerce Side-Eye", "Bring industry that stays when the subsidies end."),
        ],
    ),
    (
        "Deepfake Local Mayor Goes Viral; Actual Mayor Forced to Smile Harder",
        "A synthetic video of a municipal leader saying outrageous things spread faster than denials, a preview of every election forever. What do you think?",
        [
            ("Buddy Neer", "Forwarded Email Historian", "If it's shocking, verify before you ruin Thanksgiving."),
            ("Linda Ropp", "City Council Meeting Insomniac", "Our real meetings are boring. That's how you know they're real."),
            ("Greg Huffman", "Family Code Word Advocate", "Call the real number. Ignore the fake face."),
        ],
    ),
    (
        "Coffee Chains Test Dynamic Pricing by Time of Day; Morning Hostages Outraged",
        "Menu prices that flex with rush hour landed poorly among people who require caffeine before ethics. What do you think?",
        [
            ("Earl Fraley", "Drip Coffee Fundamentalist", "The price of waking up should not surge."),
            ("Sharon Hedges", "Reward App Prisoner", "I'll make it at home and sulk."),
            ("Nadine Kizer", "Line Philosopher", "Charge me the same for the same cup. Radical."),
        ],
    ),
    (
        "Wildlife Corridors Funded to Help Animals Cross Highways; Drivers Asked to Notice",
        "Infrastructure bills included crossings for wildlife as crash stats and ecology finally shared a spreadsheet. What do you think?",
        [
            ("Dale Evilsizor", "Deer Brake Specialist", "Build the bridges. My bumper is tired."),
            ("Karen Pence", "Nature Documentary Narrator Impersonator", "Animals had the land first. Rude of us."),
            ("Ron Bodey", "Man Who Waves at Cows", "I'll slow down. That's free policy."),
        ],
    ),
    (
        "Personal Robots Demo Household Chores; Laundry Still Wins",
        "Home robot demos folded towels imperfectly while costing more than a year of laundry service. What do you think?",
        [
            ("Irene Neer", "Laundry Night Scheduler", "If it sorts socks, marry it."),
            ("Walt Huffman", "Dishwasher Loading Constitutionalist", "Robots can't load a dishwasher right. Humans barely can."),
            ("Tina Grove", "Chore Chart Authoritarian", "Buy me time, not a gadget that needs its own Wi-Fi password."),
        ],
    ),
    (
        "Major App Outage Proves We Cannot Remember Phone Numbers Anymore",
        "A multi-hour messenger blackout left people stranded in the pre-2010 skill gap of actually contacting each other. What do you think?",
        [
            ("Harlan Zerkle", "Phone Tree Traditionalist", "Write numbers on paper like a civilization."),
            ("Denise Bodey", "Emergency Contact Laminator", "I knew this day would come. I laminated."),
            ("Mitch Grove", "Man Who Memorizes Nothing On Purpose", "My brain outsourced itself. Rude awakening."),
        ],
    ),
    (
        "Scientists Revive Woolly Mammoth Discourse for Funding Season",
        "De-extinction headlines returned with charismatic megafauna energy and fine print about ecosystems. What do you think?",
        [
            ("Carol Evilsizor", "Zoo Gift Shop Realist", "We can't handle geese. Sit down, mammoth."),
            ("Troy Pence", "Jurassic Park Quote Machine", "Life finds a way. Also lawsuits."),
            ("April Ferryman", "4-H Livestock Alumni", "Fix living species before cosplay fossils."),
        ],
    ),
    (
        "Board Games Outsell Hype Consoles for One Glorious Statistical Blip",
        "A retail report showed tabletop sales strength as families rediscovered arguing face to face about rules. What do you think?",
        [
            ("Buddy Neer", "Monopoly Relationship Stress Test Admin", "Dice heal what screens break. Sometimes."),
            ("Linda Ropp", "Game Night Snack Captain", "Cards on the table. Phones in a basket."),
            ("Greg Huffman", "Man Who House-Rules Everything", "My rules are house law. Appeal denied."),
        ],
    ),
    (
        "Cyberattack Hits Hospital Systems; Paper Charts Become Heroic Technology",
        "Ransomware disrupted care networks, forcing staff back to handwritten workarounds and reminding everyone that health is infrastructure. What do you think?",
        [
            ("Earl Fraley", "Clipboard Form Calligrapher", "Paper doesn't need a patch Tuesday."),
            ("Sharon Hedges", "Nurse Appreciation Society", "Fund IT like lives depend on it. They do."),
            ("Nadine Kizer", "Patient Portal Password Reset Victim", "I miss when charts couldn't be held hostage."),
        ],
    ),
    (
        "Luxury Brands Sell 'Quiet Luxury' Loudly",
        "Marketing campaigns insisted on subtle wealth signals using the least subtle ad buys available. What do you think?",
        [
            ("Dale Evilsizor", "Clearance Rack Olympian", "Quiet luxury is just beige with a story."),
            ("Karen Pence", "Hand-Me-Down Economist", "My quiet luxury is paid-off boots."),
            ("Ron Bodey", "Logo Hat Traditionalist", "If it's quiet, why are you yelling?"),
        ],
    ),
    (
        "Federal Student Loan Policy Changes Again; Spreadsheets Cry Out",
        "Borrowers faced another round of rule shifts and portal glitches, a saga longer than most degrees. What do you think?",
        [
            ("Irene Neer", "Parent Cosigner PTSD", "Pick a policy and stick to it for one fiscal year."),
            ("Walt Huffman", "Man Who Paid Cash for Trade School Proudly", "College math should not require a lawyer."),
            ("Tina Grove", "Income-Driven Repayment Translator", "If I need a webinar to pay a bill, the bill is broken."),
        ],
    ),
    (
        "Drone Delivery Completes First Suburban Pizza Drop Without Trauma",
        "A pilot delivered food by air successfully, a milestone that thrills logistics nerds and terrifies people under flight paths. What do you think?",
        [
            ("Harlan Zerkle", "Porch Pirate Theorist", "If a drone brings pizza, raccoons unionize."),
            ("Denise Bodey", "Tip Screen Guilt Target", "Do I tip the robot or the sky?"),
            ("Mitch Grove", "Backyard Privacy Advocate", "Keep your flying boxes out of my barbecue photos."),
        ],
    ),
    (
        "National Mood Ring Economy: Consumer Confidence Surveys Everyone Ignores Until Headlines",
        "Confidence indexes wiggled again as analysts treated feelings like leading indicators and households treated analysts like weather. What do you think?",
        [
            ("Carol Evilsizor", "Cart Total Anthropologist", "My confidence is the receipt."),
            ("Troy Pence", "Gas Price Mood Ring", "If diesel is up, I am down. Science."),
            ("April Ferryman", "Woman Who Buys Store Brand Without Shame", "Surveys don't stock my pantry."),
        ],
    ),
    (
        "AI Customer Avatars Attend Parent-Teacher Conferences as a Bit That Went Too Far",
        "A viral experiment used synthetic parents in school meetings, a joke that made educators file real complaints. What do you think?",
        [
            ("Buddy Neer", "Booster Club Button Maker", "Show up. In meatspace."),
            ("Linda Ropp", "Bake Sale Logistics General", "If you can deepfake a conference, you can find a sitter."),
            ("Greg Huffman", "Report Card Refrigerator Curator", "Kids notice who cares. Robots don't count."),
        ],
    ),
    (
        "Ocean Cleanup Tech Captures Plastic and Also Unwanted Metaphors",
        "Engineering projects pulled trash from waterways with partial success and full press kits. What do you think?",
        [
            ("Earl Fraley", "River Bank Walker", "Clean it up. Then stop putting it in."),
            ("Sharon Hedges", "Reusable Bottle Evangelist", "Tech is a mop. Policy is turning off the faucet."),
            ("Nadine Kizer", "School Earth Day Coordinator", "Show kids the trash mountain. Motivation."),
        ],
    ),
    (
        "Politicians Promise to Fix Housing With Bills Named Like Action Movies",
        "Legislative packages with aggressive titles met the slow reality of zoning, labor, and materials. What do you think?",
        [
            ("Dale Evilsizor", "Paid-Off Mortgage Smugness Society", "Build more houses. Skip the trailer music."),
            ("Karen Pence", "First-Time Buyer Grief Counselor", "Starter homes shouldn't require a movie title."),
            ("Ron Bodey", "Zoning Meeting Endurance Athlete", "Show up to the hearing if you want change."),
        ],
    ),
    (
        "Night Sky Satellite Count Hits New High; Wish Upon a Star Becomes Wish Upon a Server",
        "Orbital traffic statistics climbed as romantics adjusted their metaphors. What do you think?",
        [
            ("Irene Neer", "Front Porch Astronomer", "I wished on a star and it pinged a data center."),
            ("Walt Huffman", "Man Who Just Got Rural Internet", "Sorry, sky. I needed the school Zoom."),
            ("Tina Grove", "Telescope Birthday Gift Receiver", "Dim the future a little. Please."),
        ],
    ),
    (
        "Health Insurers Promote 'Wellness Apps' While Denying Gym Claims",
        "Carriers pushed digital wellness while reimbursement for basic preventive care stayed a maze. What do you think?",
        [
            ("Harlan Zerkle", "Explanation of Benefits Horror Reader", "Don't send me an app. Send me coverage."),
            ("Denise Bodey", "Deductible Countdown Clock", "Wellness is great after you approve the MRI."),
            ("Mitch Grove", "Man Who Walks for Free", "My wellness plan is sidewalks."),
        ],
    ),
    (
        "Global Summit on Inequality Held at Extremely Equal Five-Star Hotel",
        "Leaders discussed fairness between sessions catered with precision that mocked the agenda. What do you think?",
        [
            ("Carol Evilsizor", "Potluck Equality Theorist", "Talk poverty after you bus your own plates."),
            ("Troy Pence", "Factory Shift Memory", "Speeches don't pay rent."),
            ("April Ferryman", "Food Bank Volunteer", "Invite the people you're talking about next time."),
        ],
    ),
    (
        "Smart TVs Add More Ads to Homes People Already Paid For",
        "Manufacturers expanded ad tiers on living room screens, converting ownership into a soft subscription. What do you think?",
        [
            ("Buddy Neer", "Remote Control Monarch", "I bought the TV. Stop renting my eyeballs."),
            ("Linda Ropp", "Cord Cutter With Regrets", "We left cable for this?"),
            ("Greg Huffman", "Antenna Romantic", "Rabbit ears didn't buffer ads over paid hardware."),
        ],
    ),
    (
        "Scientists Say Ultra-Processed Sleep Advice Is Also a Problem",
        "A wave of sleep optimization content was itself linked to anxiety that ruins sleep, a perfect modern loop. What do you think?",
        [
            ("Earl Fraley", "Nap Defender Without Tenure", "Turn off the podcast. Close eyes. Advanced mode."),
            ("Sharon Hedges", "Blue Light Scold", "I dim screens. I do not need a sleep industrial complex."),
            ("Nadine Kizer", "Woman Who Counts Sheep Ironically", "Stop optimizing. Start resting."),
        ],
    ),
    (
        "Border Towns Ask for Policy Clarity; Cable Offers Volume Instead",
        "Communities requested practical resources while national media supplied graphics and certainty. What do you think?",
        [
            ("Dale Evilsizor", "Talk Radio Volume Knob", "Less slogan. More logistics."),
            ("Karen Pence", "Church Mission Trip Packer", "Complicated problems need chairs and budgets."),
            ("Ron Bodey", "Man Who Gets News From Previews", "If the graphic is red, I'm mad on schedule."),
        ],
    ),
    (
        "AI Music Labels Sign Synthetic Artists; Human Opening Acts Notice",
        "Industry deals with fully synthetic acts expanded as living musicians asked about split sheets and souls. What do you think?",
        [
            ("Irene Neer", "Church Choir Alto", "If it didn't suffer, it's not country."),
            ("Walt Huffman", "Classic Rock Hostage", "I can't tell anymore and that scares me."),
            ("Tina Grove", "Karaoke Scorekeeper", "Pay humans. Robots don't need gas money."),
        ],
    ),
    (
        "National Park Wi-Fi Proposal Divided Into Ethical Subcommittees",
        "A plan to expand connectivity in parks split outdoor culture into purists and people who want maps that work. What do you think?",
        [
            ("Harlan Zerkle", "Trail Mix Rationing Officer", "Get lost a little. It's free therapy."),
            ("Denise Bodey", "Emergency Contact Laminator", "One bar for safety. Zero bars for vibes."),
            ("Mitch Grove", "Man Who Posts Sunsets Immediately", "If I can't upload, did I even hike?"),
        ],
    ),
    (
        "Court Rules on Platform Liability in Way Only Lawyers Enjoy",
        "A dense decision on online speech and responsibility produced victory claims from everyone and clarity for no one. What do you think?",
        [
            ("Carol Evilsizor", "Group Chat Moderator of Chaos", "I just want fewer scams and more block buttons."),
            ("Troy Pence", "Forwarded Meme Historian", "If it's illegal offline, don't launder it online."),
            ("April Ferryman", "First Amendment Yard Sign Collector", "Speech is sacred. Harassment is not a hobby."),
        ],
    ),
    (
        "Robot Vacuum Union Joke Goes Too Far as Support Forums Demand Rights",
        "A viral gag about appliance labor conditions became an earnest argument about planned obsolescence. What do you think?",
        [
            ("Buddy Neer", "Roomba Hostage Negotiator", "Mine gets stuck on the same cord. Solidarity."),
            ("Linda Ropp", "Dust Bunny Diplomat", "Build things that last. Radical labor policy."),
            ("Greg Huffman", "Man Who Still Owns a Broom", "My broom has never needed a firmware update."),
        ],
    ),
    (
        "World Series of Birdwatching Goes Viral; Patience Briefly Trendy",
        "A competitive birding event captured mainstream attention, celebrating quiet skills in a loud century. What do you think?",
        [
            ("Earl Fraley", "Binocular Traditionalist", "Finally a sport that rewards shutting up."),
            ("Sharon Hedges", "Feeder Refill Technician", "My backyard is the minor leagues."),
            ("Nadine Kizer", "Phone Video of a Cardinal Archivist", "Look up. It's free content."),
        ],
    ),
    (
        "Medicare Navigation AI Launches; Seniors Request Grandchildren Anyway",
        "A digital assistant for benefits questions debuted to mixed reviews from people who prefer a human on speakerphone. What do you think?",
        [
            ("Dale Evilsizor", "Hold Music Lyricist", "Press 0 until a person answers."),
            ("Karen Pence", "Pill Organizer Logistics", "AI can help after it learns my pharmacy hours."),
            ("Ron Bodey", "Man Who Writes Questions on Paper First", "I'll try the bot. Then I'll call my niece."),
        ],
    ),
    (
        "Celebrity Divorce Settlement Includes Shared Custody of Brand Deals",
        "Entertainment coverage focused on who keeps which sponsorships, a window into romance as LLC. What do you think?",
        [
            ("Irene Neer", "Checkout Line Magazine Scholar", "Love is temporary. Endorsements are forever."),
            ("Walt Huffman", "Man Who Married Before Influencers", "We split a couch. Simpler times."),
            ("Tina Grove", "Wedding Industrial Complex Escapee", "Prenups for product placements. Peak now."),
        ],
    ),
    (
        "Global Shipping Adopts 'Slow Steaming' Again; Patience Becomes a Tariff",
        "Carriers slowed ships to save fuel and costs, extending delivery windows into philosophical territory. What do you think?",
        [
            ("Harlan Zerkle", "Amazon Package Porch Sentry", "Just tell me the real day. Stop flirting."),
            ("Denise Bodey", "Christmas-in-July Panic Buyer", "This is why I keep spare toasters."),
            ("Mitch Grove", "Local Store Suddenly Looking Wise", "Buy local when the boat is late."),
        ],
    ),
    (
        "Education Dept. Issues AI Syllabus Guidance; Teachers Request Time Travel",
        "Schools received frameworks for AI classroom use that assume spare hours nobody has. What do you think?",
        [
            ("Carol Evilsizor", "Teacher's Lounge Diplomat", "Guidance without prep time is decoration."),
            ("Troy Pence", "Book Report Survivor", "Kids need to think. Tools second."),
            ("April Ferryman", "Parent Who Proofreads at Midnight", "If the robot writes it, my kid still faces the teacher."),
        ],
    ),
    (
        "National Mood Improves Slightly on Cheap Wings Specials Alone",
        "Consumer sentiment ticked up in regions where restaurants discounted appetizers, a reminder that joy has a price point. What do you think?",
        [
            ("Buddy Neer", "Bar Stool Economist", "Wings down, hope up. That's the index I trust."),
            ("Linda Ropp", "Coupon Stacking Grandmaster", "Happiness is a sale that includes ranch."),
            ("Greg Huffman", "Man Who Shares Appetizers Grudgingly", "My confidence is half-price nachos."),
        ],
    ),
    (
        "Final Boarding Call for Common Sense Delayed Again Due to Weather and Vibes",
        "A metaphorical audit of public life found common sense still stuck on the tarmac waiting for a gate that may not exist. What do you think?",
        [
            ("Earl Fraley", "Gate Agent Stare Specialist", "We'll board when we board. Bring snacks."),
            ("Sharon Hedges", "Woman Who Packs a Neck Pillow Just in Case", "Hope is a carry-on. Don't check it."),
            ("Nadine Kizer", "Township Meeting Endurance Athlete", "Show up. Speak plain. Pass the cookies."),
        ],
    ),
]


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-")[:80] or "voices"


def wrap(text: str, width: int = 88) -> list[str]:
    words = text.split()
    rows: list[str] = []
    cur: list[str] = []
    n = 0
    for w in words:
        add = len(w) + (1 if cur else 0)
        if n + add > width and cur:
            rows.append(" ".join(cur))
            cur = [w]
            n = len(w)
        else:
            cur.append(w)
            n += add
    if cur:
        rows.append(" ".join(cur))
    return rows or [text]


def main() -> None:
    # ASCII-safe punctuation; keep first 100 if more drafts exist in PACKAGES
    packages = []
    for title, lede, people in PACKAGES:
        title = title.replace("\u2019", "'").replace("\u2018", "'")
        lede = lede.replace("\u2019", "'").replace("\u2018", "'")
        pe = [(n, j.replace("\u2019", "'"), q.replace("\u2019", "'")) for n, j, q in people]
        packages.append((title, lede, pe))
    packages = packages[:100]

    if len(packages) != 100:
        raise SystemExit(f"Expected 100 packages, got {len(packages)}")

    start = date(2026, 7, 21)
    OUT.mkdir(parents=True, exist_ok=True)

    written = 0
    for i, (title, lede, people) in enumerate(packages):
        d = start + timedelta(days=i)
        slug = slugify(title)
        ports = [
            PORTRAITS[i % len(PORTRAITS)],
            PORTRAITS[(i + 3) % len(PORTRAITS)],
            PORTRAITS[(i + 6) % len(PORTRAITS)],
        ]
        seen: set[str] = set()
        for j, pid in enumerate(ports):
            if pid in seen:
                for alt in PORTRAITS:
                    if alt not in seen:
                        ports[j] = alt
                        break
            seen.add(ports[j])

        path = OUT / f"{d.isoformat()}-{slug}.md"
        if path.exists():
            raise SystemExit(f"Refusing to overwrite existing file: {path.name}")

        lines = [
            "---",
            f'title: "{title.replace(chr(34), chr(39))}"',
            f"slug: {slug}",
            f"date: {d.isoformat()}",
            f"publish_date: {d.isoformat()}",
            "lede: >",
        ]
        for chunk in wrap(lede):
            lines.append(f"  {chunk}")
        lines.append("people:")
        for j, (name, job, quote) in enumerate(people):
            lines.append(f"  - portrait: {ports[j]}")
            lines.append(f'    name: "{name}"')
            lines.append(f'    title: "{job.replace(chr(34), chr(39))}"')
            lines.append(f'    quote: "{quote.replace(chr(34), chr(39))}"')
        lines.append("---")
        lines.append("")
        path.write_text("\n".join(lines), encoding="utf-8")
        written += 1

    end = start + timedelta(days=99)
    print(f"Wrote {written} Champaign Voices (append-only)")
    print(f"Date range: {start.isoformat()} → {end.isoformat()}")
    total = len([p for p in OUT.glob("2026-*.md")])
    print(f"Total voice files now: {total}")


if __name__ == "__main__":
    main()
