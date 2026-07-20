#!/usr/bin/env python3
"""Generate 100 Champaign Voices packages: small-town minds on big national/world news."""

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

# (headline, lede, [(name, job, quote), x3])
# Topics: broader current-events style (roughly last ~6 months of political/tech/culture news texture)
# Voices: Champaign County surnames + absurd small-town jobs; opinions, not local news items.
PACKAGES: list[tuple[str, str, list[tuple[str, str, str]]]] = [
    (
        "Congress Debates Whether AI Can Serve as a Committee Witness",
        "Lawmakers are weighing a proposal that would allow artificial intelligence systems to deliver sworn testimony before congressional committees, a move supporters call efficiency and critics call a cry for help. What do you think?",
        [
            ("Harlan Zerkle", "Township Trustee Who Still Faxes", "If the robot can sit through a three-hour budget hearing without sighing, hire it."),
            ("Denise Bodey", "Church Potluck Spreadsheet Custodian", "My cousin's chatbot already lies about when it did the dishes. I don't need it under oath."),
            ("Mitch Grove", "High School Parking Lot Philosopher", "Finally, something in Washington that doesn't need a lunch break."),
        ],
    ),
    (
        "Scientists Announce First Lab-Grown Blood Available in Hospitals",
        "Researchers say synthetic blood could ease shortages nationwide after successful early clinical use, though patients still prefer the kind that comes with a story about a high school football injury. What do you think?",
        [
            ("Carol Evilsizor", "Blood Drive Cookie Arranger", "As long as it doesn't come from a lab that also makes the weird yogurt."),
            ("Troy Pence", "Volunteer Fire Department Historian", "I donated for years. Are you telling me I could've kept it?"),
            ("April Ferryman", "Urgent Care Waiting Room Expert", "If it's red and it works, stop explaining it to me."),
        ],
    ),
    (
        "Major Social Network Tests 'Pay to Be Seen by Your Own Friends' Feature",
        "A leading social platform is piloting fees that prioritize posts to friends and family, effectively charging users for the attention they used to get for free by being annoying. What do you think?",
        [
            ("Buddy Neer", "Facebook Birthday Reminder Professional", "I already pay with my dignity. Now they want a card?"),
            ("Linda Ropp", "Group Chat Lurker Emeritus", "Good. Maybe my nephew will finally shut up about his protein powder."),
            ("Greg Huffman", "Self-Appointed Fact Checker", "I'll pay if the algorithm promises not to show me my ex's boat."),
        ],
    ),
    (
        "Federal Reserve Holds Rates Steady, Markets React by Doing Nothing Helpful",
        "The Federal Reserve left interest rates unchanged, prompting analysts to issue 14 different explanations and homeowners to stare at their mortgages like they might blink first. What do you think?",
        [
            ("Earl Fraley", "Grain Elevator Mood Reader", "They held steady. My truck payment did not get the memo."),
            ("Sharon Hedges", "Refinance-Tab Browser Hoarder", "I don't understand rates, but I know when I'm being personally disrespected."),
            ("Nadine Kizer", "Coupon Binder Archivist", "Just tell me if eggs are going to keep acting like jewelry."),
        ],
    ),
    (
        "NASA Confirms Humans Will Return to the Moon 'Sometime Before Everyone Involved Retires'",
        "Space agency officials updated lunar timelines again, assuring the public that boots will touch the Moon in a window wide enough to include several presidential administrations and at least one new phone charger standard. What do you think?",
        [
            ("Dale Evilsizor", "Night-Sky Explainer at Family Reunions", "We already went. Check the VHS."),
            ("Karen Pence", "Elementary Science Fair Judge", "If they need volunteers who can pack a cooler, I'm free."),
            ("Ron Bodey", "Tractor GPS Distruster", "They can't keep the Wi-Fi up on Main Street but they're going to the Moon?"),
        ],
    ),
    (
        "Supreme Court Agrees to Hear Case About Whether Phones Count as 'Being Present'",
        "Justices will consider a dispute over digital presence and legal obligations, a question that already ruins every dinner table in America without needing a ruling. What do you think?",
        [
            ("Irene Neer", "Family Dinner Phone Basket Enforcer", "If the phone is at the table, the person is not. I've been saying this for years."),
            ("Walt Huffman", "Church Usher Who Sees Everything", "If you're on your phone, you're absent. Also if you're thinking about lunch."),
            ("Tina Grove", "Group Project Survivor", "Being present used to mean bringing snacks. Lower the bar carefully."),
        ],
    ),
    (
        "Automakers Race to Add AI Dashboards That Argue Back About Your Driving",
        "New vehicle software will critique acceleration, following distance, and 'vibes,' turning every commute into a performance review you cannot transfer to another department. What do you think?",
        [
            ("Harlan Zerkle", "Pickup Tailgate Philosopher", "My truck already judges me. I don't need it with a voice."),
            ("Denise Bodey", "Parallel Parking Avoidance Specialist", "If it nags like my mother, I'm walking."),
            ("Mitch Grove", "Left-Lane Moral Authority", "Finally something that will tell the guy in front of me to pick a speed."),
        ],
    ),
    (
        "World Health Officials Urge Calm After New Virus Variant With a Confusing Name",
        "Health agencies say a newly tracked variant is worth watching but not panicking over, advice the public will ignore in opposite directions simultaneously. What do you think?",
        [
            ("Carol Evilsizor", "Hand Sanitizer Hoarder in Recovery", "Name it something pronounceable or I refuse to fear it correctly."),
            ("Troy Pence", "Hardware Store Epidemiologist", "I already bought the wrong masks last time. I'm sitting this one out."),
            ("April Ferryman", "Church Greeting-Time Dodger", "If it spreads by small talk, cancel the coffee hour."),
        ],
    ),
    (
        "Congress Proposes TikTok Ban Except for Everyone Who Already Has It",
        "Legislators advanced another round of restrictions on foreign-owned social apps while carefully protecting the exact behavior they claim to fear. What do you think?",
        [
            ("Buddy Neer", "Man Who Still Calls It 'The Tik Tak'", "Ban it. Unless my granddaughter needs it for school spirit."),
            ("Linda Ropp", "Silent Observer of Dance Trends", "I don't have the app and somehow I still know too much."),
            ("Greg Huffman", "National Security Lawn Chair Expert", "If China wants my recipe for chili, they can just ask like a normal spy."),
        ],
    ),
    (
        "Major Bank Outage Leaves Millions Unable to Venmo Their Share of the Appetizer",
        "A widespread banking app failure disrupted digital payments for hours, forcing Americans to confront the ancient ritual of actually owing each other cash. What do you think?",
        [
            ("Earl Fraley", "Cash-Only Diner Regular", "I told you plastic money was a personality disorder."),
            ("Sharon Hedges", "Split-the-Check Diplomat", "I watched three grown men try to remember how checks work."),
            ("Nadine Kizer", "Envelope Budget Romantic", "My system never crashed because it never left the kitchen drawer."),
        ],
    ),
    (
        "Researchers Say Microplastics Found in Clouds, Human Brains, and Probably Your Favorite Mug",
        "New studies detected microplastics in yet more places once considered pure, prompting experts to recommend fewer plastic bags and more existential dread. What do you think?",
        [
            ("Dale Evilsizor", "Reusable Bag Lost-and-Found Manager", "So the clouds are trash now. That tracks."),
            ("Karen Pence", "Tupperware Archaeologist", "I've been eating off plastic lids since 1987. Explain my success."),
            ("Ron Bodey", "Outdoor Grill Plastic-Avoider", "If it's in my brain, that explains the passwords."),
        ],
    ),
    (
        "United Nations Hosts Climate Summit Where Leaders Arrive in Very Large Planes",
        "World leaders gathered to discuss emissions reductions after traveling by methods that make the average pickup truck look like a bicycle with manners. What do you think?",
        [
            ("Irene Neer", "Thermostat War Veteran", "They can save the planet after they learn to carpool."),
            ("Walt Huffman", "Man Who Idles for 'Warm-Up Reasons'", "I recycle. That should cover their jet."),
            ("Tina Grove", "Garden Hose Philosopher", "I'm not taking shorter showers so a motorcade can feel moisturized."),
        ],
    ),
    (
        "Streaming Wars Force Fans to Subscribe to Four Services to Watch One Show",
        "Entertainment conglomerates reshuffled licensing deals again, ensuring that finishing a series now requires a budget meeting and a password shared against corporate policy. What do you think?",
        [
            ("Harlan Zerkle", "Remote Control Monarch", "I already pay for cable to not watch it. This is advanced."),
            ("Denise Bodey", "Password-Sharing Risk Officer", "We used to steal HBO with foil. Progress is a scam."),
            ("Mitch Grove", "Spoiler Avoidance Monk", "Just tell me who died in a text like a civilized society."),
        ],
    ),
    (
        "Tech Giants Promise 'Safe AI' While Racing to Make It Louder and Faster",
        "Companies unveiled safety frameworks on the same day they launched models that can write lawsuits, love letters, and your kid's book report with equal confidence. What do you think?",
        [
            ("Carol Evilsizor", "Library Late-Fee Survivor", "Safe AI is like diet soda. Still not water."),
            ("Troy Pence", "Man Who Asks Siri for Directions He Ignores", "If it can't find the fairgrounds, it shouldn't run the world."),
            ("April Ferryman", "Homework Integrity Skeptic", "My nephew's essay cited a book that doesn't exist. Leadership material."),
        ],
    ),
    (
        "FDA Reviews Weight-Loss Drugs Americans Are Already Obtaining Creatively",
        "Regulators are examining popular weight-loss medications amid soaring demand, shortages, and a thriving informal economy of people who 'know a guy.' What do you think?",
        [
            ("Buddy Neer", "Church Basement Diet Historian", "We had cabbage soup. It was worse and somehow more honest."),
            ("Linda Ropp", "Scale That Lives in the Bathroom Closet", "If it works, my jeans will forgive the ethics."),
            ("Greg Huffman", "Gym Membership Ghost", "I'll wait until it's in the free sample aisle."),
        ],
    ),
    (
        "Europe Considers Digital ID Wallets; Americans Immediately Form Conspiracy Clubs",
        "Several European governments advanced digital identity plans intended to simplify services, a concept U.S. comment sections received as the end of freedom and also slightly convenient. What do you think?",
        [
            ("Earl Fraley", "Laminated Library Card Loyalist", "My identity is a flannel and a wave. Keep your wallet."),
            ("Sharon Hedges", "Password Sticky-Note Curator", "If it remembers my login, I might sell a little freedom."),
            ("Nadine Kizer", "DMV Line Theologian", "I've waited four hours for a sticker. Digitize me."),
        ],
    ),
    (
        "Pro Sports Leagues Expand Playoffs Until Regular Season Becomes a Suggestion",
        "Commissioners defended longer postseasons as good for fans and revenue, while purists noted that eventually everyone with a jersey will make the dance. What do you think?",
        [
            ("Dale Evilsizor", "Fantasy League Commissioner for Life", "More games means more excuses for pizza."),
            ("Karen Pence", "Friday Night Lights Absolutist", "If everyone makes playoffs, call it what it is: content."),
            ("Ron Bodey", "Bar Stool Statistician", "I don't care who wins as long as it ruins someone's weekend."),
        ],
    ),
    (
        "Major Airline Apologizes After App Sells Seats That Don't Exist",
        "A carrier issued refunds and vouchers after software glitches sold imaginary seats, proving once again that the real product was always your patience. What do you think?",
        [
            ("Irene Neer", "Carry-On Tetris Champion", "I believed the seat was real because the charge was real."),
            ("Walt Huffman", "Man Who Packs a Neck Pillow 'Just in Case'", "Vouchers are monopoly money with worse customer service."),
            ("Tina Grove", "Airport Charging-Port Homesteader", "Next time sell me a gate that exists."),
        ],
    ),
    (
        "Study Finds Remote Work Makes Employees Happier and Managers More Suspicious",
        "New workplace research shows productivity holds while trust evaporates, as bosses invent new ways to confirm you are not folding laundry on company time. What do you think?",
        [
            ("Harlan Zerkle", "Shop Foreman Who Trusts Nobody", "If I can't see you working, you're fishing. That's science."),
            ("Denise Bodey", "Kitchen-Table Office Manager", "I get more done in sweatpants. That's also science."),
            ("Mitch Grove", "Zoom Background Barn Owner", "Camera on is the new time clock. Camera off is a lifestyle."),
        ],
    ),
    (
        "Cryptocurrency Bounces Again; Local Guy Mentions He 'Almost Bought'",
        "Digital asset prices surged on optimism and vibes, reviving every conversation in which someone claims they nearly became rich through bravery they did not have. What do you think?",
        [
            ("Carol Evilsizor", "Envelope Savings Traditionalist", "If I can't put it in a cookie jar, it's not money."),
            ("Troy Pence", "Gas Station Lottery Analyst", "I almost bought. That's my retirement plan: almost."),
            ("April Ferryman", "Spreadsheet Anxiety Hobbyist", "Wake me when it pays for a water heater."),
        ],
    ),
    (
        "White House Rolls Out New Messaging App Nobody Asked Their Intern to Install",
        "Officials promoted a secure communications platform for government business, guaranteeing it will be screenshotted within 20 minutes of launch. What do you think?",
        [
            ("Buddy Neer", "Man Who Still Uses Voicemail as a Weapon", "Secure until someone takes a picture of the screen with another phone."),
            ("Linda Ropp", "Prayer Chain Network Admin", "We already have a group text. It's chaotic and effective."),
            ("Greg Huffman", "Conspiracy Whiteboard Enthusiast", "If it's free, you're the product. If it's government, you're the homework."),
        ],
    ),
    (
        "Scientists Revive Dire Wolf Talk After Gene-Editing Breakthrough Headlines",
        "A wave of coverage about ancient DNA and gene editing has the public debating whether extinct animals should return and who would be responsible for the poop. What do you think?",
        [
            ("Earl Fraley", "Dog Park Diplomat", "We can't handle golden doodles. Sit down."),
            ("Sharon Hedges", "Nature Channel Narrator Impersonator", "Bring them back only if they pay property tax."),
            ("Nadine Kizer", "Yard-Chicken Survivalist", "I don't need a dire wolf near my compost."),
        ],
    ),
    (
        "College Athletes Cash In on Name Deals While Tuition Still Feels Like a Mortage",
        "NIL money continues reshaping campus sports as boosters write checks and English majors write term papers about inequality they can see from the student section. What do you think?",
        [
            ("Dale Evilsizor", "Booster Club Button Maker", "Pay the kids. Then explain why parking still costs eighteen dollars."),
            ("Karen Pence", "Scholarship Application Trauma Survivor", "I got a free T-shirt in 1998 and thought that was wealth."),
            ("Ron Bodey", "Tailgate Grill Ownership Society", "If he can dunk, he can have a car dealership."),
        ],
    ),
    (
        "Electric Grid Operators Warn Summer Demand Could Outpace 'Hopes and Prayers'",
        "Utilities cautioned that heat waves and data centers are stressing power systems, politely asking Americans to consider not running every appliance at 5 p.m. What do you think?",
        [
            ("Irene Neer", "Ceiling Fan Maximum Setting Loyalist", "I'll unplug the toaster when the server farms unplug first."),
            ("Walt Huffman", "Generator Bragging Rights Holder", "My plan is diesel and denial."),
            ("Tina Grove", "Laundry Night Scheduler", "We already do laundry at 9 p.m. like criminals."),
        ],
    ),
    (
        "Global Chip Shortage Eases, Immediately Replaced by Different Chip Shortage",
        "Manufacturers celebrated improved semiconductor supply just as a new bottleneck emerged, continuing the tradition of progress that feels like rearranging the same problem. What do you think?",
        [
            ("Harlan Zerkle", "Man Waiting on a Tractor Part Since Easter", "Shortages are just 'not yet' with a press release."),
            ("Denise Bodey", "Smartphone Upgrade Resister", "My phone is fine. It's the world that's broken."),
            ("Mitch Grove", "Gaming PC Dreamer on a Budget", "I don't need chips. I need peace."),
        ],
    ),
    (
        "Celebrity Couple Breaks Up; Economy Remains Weirdly Unaffected",
        "A high-profile separation dominated entertainment coverage for a full news cycle, during which actual economic indicators refused to participate in the drama. What do you think?",
        [
            ("Carol Evilsizor", "Checkout Line Magazine Scholar", "I needed this. The other news is too heavy for a Tuesday."),
            ("Troy Pence", "Sports Radio Caller Archetype", "Breakups are free content. Wars cost money."),
            ("April Ferryman", "Wedding Industrial Complex Skeptic", "If love can't survive a press tour, what chance do the rest of us have?"),
        ],
    ),
    (
        "Cities Test Robot Delivery Sidewalks; Dogs Immediately Form a Union",
        "Autonomous delivery bots are expanding into more neighborhoods, delighting tech firms and enraging anyone who has ever walked a dog past a wheeled cooler with opinions. What do you think?",
        [
            ("Buddy Neer", "Sidewalk Territorial Governor", "If it doesn't wave back, I don't trust it."),
            ("Linda Ropp", "Porch Pirate Theorist", "A robot bringing me toothpaste is the softest dystopia."),
            ("Greg Huffman", "Dog That Barks at Wheelie Bins, Owner Of", "My dog already works security. Don't automate him."),
        ],
    ),
    (
        "IRS Teases Direct File Tool Expansion; Accountants Quietly Recalculate Their Worth",
        "Tax officials promoted wider access to free filing software, a convenience that still requires you to understand what a 'dependent' is at 11 p.m. on April 14. What do you think?",
        [
            ("Earl Fraley", "Shoebox Receipt Preservationist", "Free filing is great until the form asks a riddle."),
            ("Sharon Hedges", "Extension-Filing Olympian", "I don't fear taxes. I fear the PDF."),
            ("Nadine Kizer", "H&R Block Emotional Support Client", "If it's free, why do I still feel fined?"),
        ],
    ),
    (
        "Ocean Heat Records Broken Again, Fish Decline to Comment",
        "Scientists reported another stretch of record ocean temperatures, linking them to climate trends while seafood restaurants quietly reprint menus with fewer options. What do you think?",
        [
            ("Dale Evilsizor", "Lake Weather App Obsessive", "The ocean is large. It should know better."),
            ("Karen Pence", "Fish Fry Friday Historian", "If cod gets fancy, I'm switching to hot dogs."),
            ("Ron Bodey", "Man Who Calls Climate 'The Weather'", "It's been hot before. Also cold. I'm busy."),
        ],
    ),
    (
        "AI Music Charts Climb as Human Songwriters Demand to Be Paid Like Robots Eventually Will",
        "Streaming charts filled with AI-assisted tracks have sparked fights over credit, royalties, and whether a chorus written by a model counts as country if it mentions a truck. What do you think?",
        [
            ("Irene Neer", "Church Choir Alto With Standards", "If it didn't suffer, it's not a ballad."),
            ("Walt Huffman", "Classic Rock Radio Hostage", "I can't tell anymore and that scares me more than the robots."),
            ("Tina Grove", "Karaoke Night Scorekeeper", "Pay the humans. The robots don't need gas money."),
        ],
    ),
    (
        "Border Policy Fight Intensifies; Cable News Invents New Graphic",
        "Washington resumed a familiar immigration standoff with fresh rhetoric and the same unresolved logistics, while networks debuted maps in more aggressive fonts. What do you think?",
        [
            ("Harlan Zerkle", "Talk Radio Volume Knob Specialist", "Everyone's yelling. Nobody's hiring a translator for reality."),
            ("Denise Bodey", "Church Mission Trip Packer", "Complicated problems deserve fewer slogans and more folding chairs."),
            ("Mitch Grove", "Man Who Gets News From Previews", "If the graphic is red, I'm supposed to be mad. Got it."),
        ],
    ),
    (
        "Major Retailer Rolls Out AI Return Policy That Argues With You",
        "A national chain deployed automated tools to process returns, resulting in customers debating a chatbot about a shirt that 'technically left the house.' What do you think?",
        [
            ("Carol Evilsizor", "Gift Receipt Archivist", "I don't negotiate with kiosks."),
            ("Troy Pence", "Customer Service Call-Hold Composer", "Put a person on the line or keep the shirt."),
            ("April Ferryman", "Online Order Regret Specialist", "The robot said no. I said watch me drive there."),
        ],
    ),
    (
        "Space Company Loses Rocket, Calls It a 'Learning Experience' Valued at Billions",
        "A high-profile launch failure destroyed hardware and cargo, which executives framed as valuable data while insurance adjusters framed it as a very expensive firework. What do you think?",
        [
            ("Buddy Neer", "Amateur Pyrotechnics Admirer", "If my truck exploded, I couldn't call it R&D."),
            ("Linda Ropp", "Science Fair Participation Award Presenter", "Learning is good. Maybe learn closer to the ground."),
            ("Greg Huffman", "Man Who Fixes Things With Duct Tape First", "Billions for a boom. I fix fences for free."),
        ],
    ),
    (
        "Health Agencies Warn of Measles Outbreaks Linked to 'I Thought We Fixed This' Energy",
        "Officials reported rising measles cases in multiple regions, a development that has doctors exhausted and grandparents confused about which decade this is. What do you think?",
        [
            ("Earl Fraley", "School Nurse Nostalgia Patient", "We had shots. Then we had opinions. Now we have spots."),
            ("Sharon Hedges", "PTA Snack Coordinator", "I'm not anti-science. I'm anti-group-chat science."),
            ("Nadine Kizer", "Waiting Room Magazine Reader", "Bring back the diseases we already beat? Bold strategy."),
        ],
    ),
    (
        "Gaming Company Sells Skins That Cost More Than Actual Jackets",
        "A popular game's cosmetic marketplace hit new highs as teens spent real money on digital coats that cannot keep anyone warm at the bus stop. What do you think?",
        [
            ("Dale Evilsizor", "Hand-Me-Down Coat Economist", "I bought a real jacket in 1994. Still works. Still ugly."),
            ("Karen Pence", "Allowance Negotiator", "If it's not physical, it better not be $70."),
            ("Ron Bodey", "Man Who Doesn't Understand Fortnite", "At least baseball cards were something you could lose under the seat."),
        ],
    ),
    (
        "Central Banks Explore Digital Currencies; People Immediately Hide Cash in Freezers",
        "Policymakers discussed central bank digital currencies as a modern payment rail, while a significant portion of the public heard 'they're coming for the twenties under the mattress.' What do you think?",
        [
            ("Irene Neer", "Emergency Envelope Under the Sink", "My money is cold and offline. As God intended."),
            ("Walt Huffman", "Gold Coin Gift Shop Browser", "Digital dollars sound like gift cards for the whole country."),
            ("Tina Grove", "Venmo Boundary Setter", "I'll use it when my aunt figures out the app."),
        ],
    ),
    (
        "Hollywood Writers and Studios Clash Again Over AI Script Helpers",
        "Labor talks reignited around how much artificial intelligence can touch a screenplay before someone has to admit the robot wrote the quippy sidekick. What do you think?",
        [
            ("Harlan Zerkle", "Movie Theater Butter Budgeter", "If the robot writes it, can it also sit through the credits?"),
            ("Denise Bodey", "Rom-Com Continuity Expert", "I can already tell when a joke was written by a committee of ghosts."),
            ("Mitch Grove", "Spoiler-Free Trailer Watcher", "Pay writers. Robots don't need craft services."),
        ],
    ),
    (
        "National Parks See Record Crowds Seeking 'Peace' in 40-Minute Parking Lines",
        "Visitation surged as travelers chased nature, only to discover nature now requires a timed entry pass and a personality that can tolerate RVs. What do you think?",
        [
            ("Carol Evilsizor", "Scenic Overlook Photographer of Other People's Heads", "I went for quiet and found a food truck."),
            ("Troy Pence", "Campground Generator Diplomat", "Wilderness should not have Wi-Fi. Or maybe just a little."),
            ("April Ferryman", "Trail Mix Rationing Officer", "If I wanted a crowd, I'd go to a funeral potluck."),
        ],
    ),
    (
        "Phone Makers Remove Charger Again, Call It Environmentalism",
        "Manufacturers defended shipping phones without charging bricks as an eco-friendly choice that also happens to sell a lot of separate charging bricks. What do you think?",
        [
            ("Buddy Neer", "Drawer Full of Mystery Cables", "I have 40 cords and none of them fit the new one."),
            ("Linda Ropp", "Thrift Store Electronics Skeptic", "Save the planet by charging me extra. Cute."),
            ("Greg Huffman", "USB Archaeology Specialist", "I miss when plugs made sense and hurt your hand honestly."),
        ],
    ),
    (
        "Global Shipping Prices Spike After Red Sea Chaos Ruins Delivery Estimates",
        "Attacks and detours along major shipping lanes pushed freight costs up, meaning your cart's 'arrives Thursday' promise is now more of a spiritual goal. What do you think?",
        [
            ("Earl Fraley", "Amazon Package Porch Sentry", "Just tell me when it's actually here. Stop flirting."),
            ("Sharon Hedges", "Christmas Shopping in July Panic Buyer", "This is why I still keep a spare toaster."),
            ("Nadine Kizer", "Local Store Suddenly Looking Wise", "Maybe we should buy some things from people we can yell at in person."),
        ],
    ),
    (
        "Scientists Grow Meat in a Lab; Grillmasters File Emotional Damages",
        "Lab-grown meat moved closer to wider sale, sparking debates about ethics, taste, and whether a burger without a farm can still justify a man standing outside in smoke for four hours. What do you think?",
        [
            ("Dale Evilsizor", "Charcoal Loyalty Program Member", "If it didn't moo or cluck, it's a science project."),
            ("Karen Pence", "Casserole Traditionalist", "I'll try it if it goes on sale next to the real guilt."),
            ("Ron Bodey", "Smoker Temperature Whisperer", "You can grow it. I'm still putting sauce on it."),
        ],
    ),
    (
        "Big Tech Testifies About Child Safety While Ads Target Kids With Precision",
        "Executives faced questions on youth mental health and platform design, a hearing that produced strong statements and weak follow-through, as is tradition. What do you think?",
        [
            ("Irene Neer", "Parental Control Password Hidden in Plain Sight", "They can protect kids right after they stop selling them snacks via algorithm."),
            ("Walt Huffman", "Man Who Thinks Facebook Is Still the Internet", "I don't understand the app and somehow I'm still worried."),
            ("Tina Grove", "Screen-Time Bargain Mediator", "If Congress had a bedtime, maybe the apps would too."),
        ],
    ),
    (
        "Olympics Prep Spending Defended as 'Investment in National Pride and Temporary Traffic Cones'",
        "Host cities and sponsors touted long-term benefits of Olympic infrastructure while residents mostly experienced construction and the promise of a stadium nobody asked to maintain. What do you think?",
        [
            ("Harlan Zerkle", "Traffic Cone Anthropologist", "Pride is fine. I need a lane."),
            ("Denise Bodey", "Opening Ceremony Costume Critic", "I'll watch for the outfits. Not the bond payments."),
            ("Mitch Grove", "Couch Flag Waver", "If we win medals, it was worth it. If we don't, it was always corrupt."),
        ],
    ),
    (
        "Insurance Companies Blame Climate for Rate Hikes; Customers Blame Insurance Companies",
        "Insurers pointed to extreme weather losses as they raised premiums, a conversation that ends with everyone agreeing only that the bill is higher. What do you think?",
        [
            ("Carol Evilsizor", "Deductible Shock Absorber", "I'm not a hurricane and somehow I'm paying like one."),
            ("Troy Pence", "Roof Estimate Collector", "They cover everything except the thing that happens."),
            ("April Ferryman", "Claims Call Hold Music Critic", "Raise rates quieter next time."),
        ],
    ),
    (
        "Startup Promises Brain Implants for 'Focus'; Offices Immediately Want Mandates",
        "A neurotech firm hyped implants that could boost concentration, prompting managers everywhere to wonder if productivity can be installed like printer software. What do you think?",
        [
            ("Buddy Neer", "Coffee as Primary Operating System", "My focus implant is the third cup."),
            ("Linda Ropp", "Open Office Noise Martyr", "Install quiet first."),
            ("Greg Huffman", "Man Who Unplugs the Smart Speaker", "Nothing goes in my head that I didn't put there with a fork."),
        ],
    ),
    (
        "Election Officials Beg Public to Ignore AI Deepfakes, Public Forwards Them Anyway",
        "Officials warned that synthetic audio and video could muddy campaigns this year, a threat that thrives because outrage is more shareable than verification. What do you think?",
        [
            ("Earl Fraley", "Forwarded Email Historian", "If it's shocking, I send it. That's how family works."),
            ("Sharon Hedges", "Fact-Check Tab Opener (Sometimes)", "I almost fell for one. Then I noticed the ears were wrong."),
            ("Nadine Kizer", "Local Facebook Group Moderator of Chaos", "We need a rule: no videos of politicians saying things they wish they said."),
        ],
    ),
    (
        "Water Wars Heat Up as West Negotiates River Cuts and Lawns Panic",
        "States and cities intensified talks over river allocations amid drought pressure, leaving suburban sprinkler systems feeling politically exposed. What do you think?",
        [
            ("Dale Evilsizor", "Green Grass Peer Pressure Victim", "My lawn is a lifestyle. Don't make it a scandal."),
            ("Karen Pence", "Rain Barrel Idealist", "We should share water like we share casseroles: unevenly but with judgment."),
            ("Ron Bodey", "Well Water Bragging Rights", "I don't trust rivers that need meetings."),
        ],
    ),
    (
        "Military Drone Budget Soars as Someone Still Has to Iron the Dress Uniforms",
        "Defense spending debates highlighted advanced unmanned systems while older, human logistics problems remained unsolved and unglamorous. What do you think?",
        [
            ("Irene Neer", "Care Package Shipper", "Buy the drones. Also buy socks for people."),
            ("Walt Huffman", "VFW Coffee Pot Guardian", "Wars get fancier. Grief doesn't."),
            ("Tina Grove", "Recruiting Poster Realist", "If a robot can fight, can it also do the paperwork?"),
        ],
    ),
    (
        "Fast Food Chains Test Dynamic Pricing That Changes While You're in Line",
        "Restaurants experimented with prices that adjust by time and demand, ensuring your burger costs more because you had the audacity to be hungry at noon. What do you think?",
        [
            ("Harlan Zerkle", "Value Menu Archaeologist", "The dollar menu died and this is the funeral."),
            ("Denise Bodey", "Drive-Thru Diplomat", "If the price moves, I'm reversing."),
            ("Mitch Grove", "Fries-as-a-Side Constitutional Scholar", "Just write the number in stone like a normal country."),
        ],
    ),
    (
        "Scientists Say Sleep Deprivation Is Killing Us; Economy Says Start at 7 a.m.",
        "Health research linked chronic sleep loss to major disease risks as workplaces continued to treat exhaustion like a personality trait worth promoting. What do you think?",
        [
            ("Carol Evilsizor", "Early Bird Weaponizer", "I wake up at 5. That doesn't mean I'm right. It means I'm loud."),
            ("Troy Pence", "Nap Defender Without Tenure", "If sleep is medicine, why is the alarm legal?"),
            ("April Ferryman", "Night Shift Survivor", "I don't need a study. I need curtains."),
        ],
    ),
    (
        "Museum Returns Artifact After Decades; Comment Section Starts New War",
        "A major museum agreed to repatriate a cultural object, reopening debates about history, ownership, and whether everything in a glass case was acquired politely. What do you think?",
        [
            ("Buddy Neer", "Antique Mall Moral Philosopher", "If you stole it, give it back. If your great-grandpa stole it, still give it back."),
            ("Linda Ropp", "Gift Shop Magnet Collector", "Can I keep the postcard?"),
            ("Greg Huffman", "History Channel Documentarian of His Own Opinions", "Next they'll want the arrowheads from my uncle's coffee can."),
        ],
    ),
    (
        "Self-Driving Truck Pilot Expands; Human Drivers Demand to Keep Steering Wheels as Emotional Support Objects",
        "Freight companies touted autonomous trucking progress while drivers and unions asked who gets sued when the robot parks creatively. What do you think?",
        [
            ("Earl Fraley", "CB Radio Nostalgia Patient", "A truck without a driver is just a missile with turn signals."),
            ("Sharon Hedges", "Highway Merger Anxiety Patient", "If it can merge better than Dave from accounting, fine."),
            ("Nadine Kizer", "Rest Stop Coffee Connoisseur", "Robots don't tip. That's my issue."),
        ],
    ),
    (
        "Billionaire Launches Private City Concept; Locals Already Hate the Logo",
        "A tech mogul floated plans for a privately governed city optimized for innovation, housing, and rules written by people who have never attended a zoning meeting. What do you think?",
        [
            ("Dale Evilsizor", "Township Meeting Endurance Athlete", "You want a city? Bring snacks and sit through public comment."),
            ("Karen Pence", "HOA Horror Storyteller", "Private rules are just HOAs with better fonts."),
            ("Ron Bodey", "Man Suspicious of Utopias", "If it's perfect, there's a fine."),
        ],
    ),
    (
        "Antibiotic Resistance Warning Escalates; People Still Demand Antibiotics for the Vibes",
        "Doctors reiterated that antibiotics don't treat viruses as resistant infections climb, a message that loses to the ancient human need to leave with a prescription. What do you think?",
        [
            ("Irene Neer", "Urgent Care Gift Shop Customer", "I want a pill so I can feel proactive."),
            ("Walt Huffman", "Chicken Soup Traditionalist", "My grandmother cured everything with broth and threats."),
            ("Tina Grove", "Symptom Googler in Recovery", "If WebMD says rare flesh disease, I still want amoxicillin."),
        ],
    ),
    (
        "Satellite Internet Blankets Rural Areas; Family Zoom Calls Become Unavoidable",
        "Expanded satellite broadband reached more remote homes, closing the digital divide and opening a new era of relatives who can finally see your kitchen mess in HD. What do you think?",
        [
            ("Harlan Zerkle", "Dial-Up Trauma Survivor", "I wanted weather radar, not my cousin's face at breakfast."),
            ("Denise Bodey", "Wi-Fi Password Landlord", "Faster internet means faster arguments."),
            ("Mitch Grove", "Man Who Waves at the Install Van", "If it works during a storm, I'll believe in the future."),
        ],
    ),
    (
        "Fashion Brand Sells $400 'Work Shirt' That Looks Like a Work Shirt",
        "A luxury label released a premium basic indistinguishable from hardware-store cotton, except for the price and the way it makes you angry in a boutique. What do you think?",
        [
            ("Carol Evilsizor", "Clearance Rack Olympian", "I can get that look with bleach and denial."),
            ("Troy Pence", "Flannel Economist", "If it doesn't have a pocket for a pencil, it's cosplay."),
            ("April Ferryman", "Thrifting Sniper", "Four hundred dollars should include the guy who invents the shirt."),
        ],
    ),
    (
        "Nuclear Power Gets Rebranded as Clean; Old Protest Signs Confused",
        "Policymakers and tech firms revived nuclear energy as a climate solution, forcing a cultural rewrite for people who learned to fear it from movies and the news in 1986. What do you think?",
        [
            ("Buddy Neer", "Glow-in-the-Dark Joke Specialist", "If it keeps the lights on without roasting the planet, stop whispering."),
            ("Linda Ropp", "Three Mile Island Documentary Watcher", "I'll allow it if the waste doesn't live next to the fairgrounds."),
            ("Greg Huffman", "Man Who Distrusts Anything Rebranded", "First it was dangerous. Now it's trendy. Pick a lane."),
        ],
    ),
    (
        "Dating Apps Add AI Wingmen That Message for You; Romance Declines to Participate",
        "Apps are testing automated openers and conversation helpers, optimizing love the way spam optimized hope. What do you think?",
        [
            ("Earl Fraley", "Married Before Apps Existed and Smug About It", "If a robot writes your hello, who's getting married?"),
            ("Sharon Hedges", "Left-Swipe Cardio Athlete", "I want fewer messages, not better lies."),
            ("Nadine Kizer", "Church Mixer Traditionalist", "Meet people near the coffee. Suffer normally."),
        ],
    ),
    (
        "Global Birth Rates Fall; Economists Panic About Who Will Pay for Everything Later",
        "Demographers reported declining fertility in many countries, sparking debates about childcare costs, culture, and whether anyone can afford a second bedroom. What do you think?",
        [
            ("Dale Evilsizor", "Grandparent Who Offers Free Babysitting With Opinions", "People would have kids if houses didn't cost like castles."),
            ("Karen Pence", "Daycare Waitlist Veteran", "It's not a mystery. It's a budget."),
            ("Ron Bodey", "Man Who Thinks Everyone Should Just 'Figure It Out'", "We figured it out. The numbers said no."),
        ],
    ),
    (
        "Food Delivery Fees Exceed Cost of the Food; Customers Pay Anyway",
        "Platform fees and tips stacked high enough to make a burrito a luxury good, yet orders continued because cooking would require standing up. What do you think?",
        [
            ("Irene Neer", "Crockpot Evangelist", "I could make this for $4 and emotional stability."),
            ("Walt Huffman", "Tip Screen Guilt Target", "I tipped 25% on fees. I need a priest."),
            ("Tina Grove", "Lazy Tuesday Dinner Negotiator", "Yes it's dumb. Bring the fries."),
        ],
    ),
    (
        "Congress Passes Something Bipartisan by Accident, Immediately Starts Fighting About Credit",
        "A rare cross-party bill advanced before lawmakers remembered they prefer narrative conflict to outcomes, and the press conference became a second battlefield. What do you think?",
        [
            ("Harlan Zerkle", "C-SPAN Accidental Viewer", "They did a good thing and ruined it with a speech."),
            ("Denise Bodey", "Local League of Women Voters Pamphlet Keeper", "Pass the law. Skip the parade."),
            ("Mitch Grove", "Man Who Votes and Then Goes Fishing", "If both sides claim it, it might actually help somebody."),
        ],
    ),
    (
        "Virtual Reality Offices Promise Collaboration; Deliver Motion Sickness",
        "Companies demoed VR workplaces meant to replace video calls, a solution in search of a problem that can also make you nauseous before lunch. What do you think?",
        [
            ("Carol Evilsizor", "Headset Hair Concern Committee", "I won't put a computer on my face for a meeting about toner."),
            ("Troy Pence", "Mute Button Artist", "Zoom is bad. This is Zoom in a fishbowl."),
            ("April Ferryman", "Office Plant Waterer", "If I wanted to feel unreal, I'd read my performance review."),
        ],
    ),
    (
        "Major Storm Season Forecast Looks Aggressive; Plywood Demand Philosophically Rises",
        "Meteorologists warned of an active season ahead, prompting coastal prep and inland people to act like wind is a personal vendetta. What do you think?",
        [
            ("Buddy Neer", "Basement Battery Organizer", "I don't fear storms. I fear the group chat during storms."),
            ("Linda Ropp", "Flashlight That Works Sometimes", "Every year we act surprised. Weather is not a plot twist."),
            ("Greg Huffman", "Generator Neighbor Envy", "My plan is to become friends with whoever bought diesel early."),
        ],
    ),
    (
        "Universities Crack Down on AI Homework; Students Crack Down on Trying",
        "Schools expanded detection tools and honor codes as generative AI made essays optional in spirit if not in policy. What do you think?",
        [
            ("Earl Fraley", "Book Report Survivor of the 1970s", "We copied the encyclopedia. At least the encyclopedia was heavy."),
            ("Sharon Hedges", "Parent Who Proofreads at Midnight", "If the robot writes it, my kid still has to read the email from the teacher."),
            ("Nadine Kizer", "Library Quiet Zone Enforcer", "Learn something or don't. But don't make the robot your personality."),
        ],
    ),
    (
        "Oil Prices Swing on Headlines Alone; Gas Station Signs Have Panic Attacks",
        "Crude markets jerked on geopolitical rumors and inventory reports, and pump prices followed with the emotional stability of a soap opera. What do you think?",
        [
            ("Dale Evilsizor", "Half-Tank Anxiety Patient", "I fill up at $0.03 cheaper like I won something."),
            ("Karen Pence", "Carpool Guilt Administrator", "Just tell me the number before I leave the house."),
            ("Ron Bodey", "Diesel Truck Identity Holder", "The sign changes faster than my opinions."),
        ],
    ),
    (
        "Celebrity Memoir Admits to Flaws Everyone Already Googled",
        "A star released a confessional book covering addictions, feuds, and growth, timed perfectly for a press tour and a discount bin by February. What do you think?",
        [
            ("Irene Neer", "Beach Read Realist", "I'll read it if the font is large and the tea is hot."),
            ("Walt Huffman", "Biography Section Browser Who Buys Nothing", "Confessing for profit is the national sport."),
            ("Tina Grove", "Book Club Snack Captain", "As long as there's a chapter about therapy and a chapter about a dog."),
        ],
    ),
    (
        "Cities Ban Gas Leaf Blowers; Suburbs Enter Quiet Crisis",
        "Local ordinances targeting gas blowers spread as noise and emissions concerns won, leaving lawns temporarily peaceful and certain men spiritually unmoored. What do you think?",
        [
            ("Harlan Zerkle", "Leaf Blower Conductor", "If I can't make noise, how will the neighborhood know I care?"),
            ("Denise Bodey", "Rake Traditionalist", "Use a rake. Build character. Ruin Saturdays honestly."),
            ("Mitch Grove", "HOA Complaint Draftsman", "Quiet is nice until the leaves win."),
        ],
    ),
    (
        "Pharmaceutical Ad Lists Side Effects Longer Than the Disease",
        "A new prime-time drug commercial spent most of its runtime warning about risks, including some that sounded worse than the condition being treated. What do you think?",
        [
            ("Carol Evilsizor", "Commercial Volume Spike Victim", "If the side effect is death, maybe whisper."),
            ("Troy Pence", "Man Who Asks His Doctor About the Ad", "I don't have that disease and now I'm scared I will."),
            ("April Ferryman", "Remote Mute Reflex Athlete", "Cure me quieter."),
        ],
    ),
    (
        "International Court Issues Warrant; Cable Panels Issue Hot Takes",
        "A high-profile international legal action dominated foreign-policy coverage as pundits confidently explained jurisdictions they learned about that morning. What do you think?",
        [
            ("Buddy Neer", "World Map on the Wall That Still Says USSR", "I don't know the court, but I know yelling."),
            ("Linda Ropp", "Sunday Morning Show Accidental Viewer", "If it's far away, we still argue like it's the school board."),
            ("Greg Huffman", "Sovereignty Speechwriter for His Truck", "Nobody tells us what to do except the HOA and God."),
        ],
    ),
    (
        "Smart Homes Keep Locking Owners Out; Owners Keep Calling It Progress",
        "Connected locks and apps failed in widely shared incidents, stranding people outside houses they technically still owned in the offline sense. What do you think?",
        [
            ("Earl Fraley", "Spare Key Under Fake Rock Traditionalist", "My key doesn't need an update."),
            ("Sharon Hedges", "Password Reset Therapist", "I was locked out of my own life by a 404 error."),
            ("Nadine Kizer", "Neighbor With a Ladder", "Smart is fine. Dumb backup is required."),
        ],
    ),
    (
        "Fashion Trend Revives Tiny Sunglasses That Make Everyone Look Like a Bug",
        "Runways and influencers pushed microscopic frames back into style, a look that protects neither eyes nor dignity. What do you think?",
        [
            ("Dale Evilsizor", "Wraparound Sunglasses Forever Man", "If they don't cover my eyes, they're jewelry."),
            ("Karen Pence", "Drugstore Aisle Fashionista", "I look dumb enough without help."),
            ("Ron Bodey", "Ball Cap Constitutionalist", "My face is not a trend."),
        ],
    ),
    (
        "Lab Leak Theories and Wet Market Theories Keep Trading Places in the Discourse",
        "Scientific and political arguments over pandemic origins continued without a clean ending, ensuring the only lasting product is distrust. What do you think?",
        [
            ("Irene Neer", "Conspiracy Diet Moderator", "I just wash my hands and distrust everyone equally."),
            ("Walt Huffman", "Man Who Wants a Simple Villain", "If nobody admits anything, everybody's guilty of something."),
            ("Tina Grove", "Public Health Flyer Keeper", "Tell me how to not get sick. Save the thriller plot for later."),
        ],
    ),
    (
        "Streaming Service Cracks Down on Password Sharing; Families Invent New Lies",
        "A major platform intensified household verification, turning living rooms into interrogation rooms about who counts as 'family.' What do you think?",
        [
            ("Harlan Zerkle", "Password Patriarch", "My household is whoever I say it is."),
            ("Denise Bodey", "Cousin in Another Zip Code", "I will drive over once a month if that's what love costs."),
            ("Mitch Grove", "Pirate Bay Moral Crisis Patient", "They trained us to share. Now they're shocked."),
        ],
    ),
    (
        "Mars Sample Return Mission Delayed; Earth Samples Remain Abundant and Disappointing",
        "Space agencies postponed complex Mars sample logistics again, a reminder that even rocks have better travel agents than some airlines. What do you think?",
        [
            ("Carol Evilsizor", "Science Documentary Pause-Button User", "Bring the rocks. Or don't. I have gravel."),
            ("Troy Pence", "Man Who Thought We'd Have Jetpacks by Now", "We can't return rocks but we can deliver tacos. Priorities."),
            ("April Ferryman", "Elementary Space Week Volunteer", "Tell the kids it's delayed, not canceled. Hope is curriculum."),
        ],
    ),
    (
        "National Debt Hits New Milestone Nobody Can Visualize",
        "The debt clock rolled over another symbolic threshold as economists argued about sustainability and voters argued about which party did it on purpose. What do you think?",
        [
            ("Buddy Neer", "Household Budget Sticky Note Accountant", "If my credit card looked like that, I'd hide the mail."),
            ("Linda Ropp", "Coupon Stacking Grandmaster", "Trillions aren't real until they show up as eggs."),
            ("Greg Huffman", "Man Who Solves Debt by Not Looking", "Stop spending. Also keep my programs. I'm consistent."),
        ],
    ),
    (
        "Gene-Edited Crops Expand; Farmers Ask Who Owns the Seeds This Time",
        "New gene-edited plant varieties advanced toward market as rural communities weighed yield promises against corporate control and familiar skepticism. What do you think?",
        [
            ("Earl Fraley", "Seed Catalog Romantic", "If I can't replant it, I'm renting my dinner."),
            ("Sharon Hedges", "Farmers Market Loyalty Program", "Edit the bugs first."),
            ("Nadine Kizer", "Canning Jar Futurist", "I'll eat it. I'm not naming my corn after a patent."),
        ],
    ),
    (
        "AI Judges Suggested for Minor Disputes; Lawyers Laugh Until They Check Billing Hours",
        "A pilot concept for algorithmic rulings on small claims sparked jokes and dread about justice that runs on uptime and training data. What do you think?",
        [
            ("Dale Evilsizor", "Small Claims Court Spectator Sport Fan", "A robot can't understand neighbor fence energy."),
            ("Karen Pence", "Mediation Cookie Bringer", "If it settles faster, fine. If it's wrong, we still have casseroles."),
            ("Ron Bodey", "Man Who Settles Arguments by Volume", "Justice needs a face so I know who to glare at."),
        ],
    ),
    (
        "Plastic Recycling Rates Exposed as Mostly a Feel-Good Sorting Hobby",
        "Reporting and audits again suggested much of household recycling never becomes new products, crushing the spiritual high of rinsing yogurt cups. What do you think?",
        [
            ("Irene Neer", "Blue Bin Optimist in Crisis", "I've been washing trash for years like a chump."),
            ("Walt Huffman", "Man Who Throws It All in One Can Honestly", "I was right for the wrong reasons."),
            ("Tina Grove", "Elementary Earth Day Coordinator", "Tell the kids the truth gently. Then invent a better system."),
        ],
    ),
    (
        "Bosses Demand Return to Office Citing Culture; Employees Cite Parking",
        "Corporate RTO campaigns emphasized collaboration and mentorship while staff emphasized commutes, childcare, and the sacred right to eat lunch in sweatpants. What do you think?",
        [
            ("Harlan Zerkle", "Time Clock Romantic", "Show up. Suffer together. That's culture."),
            ("Denise Bodey", "Hybrid Schedule Puzzle Solver", "Culture doesn't need my car payment."),
            ("Mitch Grove", "Hot Desk Refugee", "I'll come in if you guarantee a chair that isn't haunted."),
        ],
    ),
    (
        "Influencer Nation Elects Unofficial Leaders With Better Lighting Than Congress",
        "Creators with massive followings increasingly shape politics and products, a power structure based on engagement rather than legislation or shame. What do you think?",
        [
            ("Carol Evilsizor", "Cable News Hostage", "At least senators have to wear real pants sometimes."),
            ("Troy Pence", "Man Who Distrusts Anyone With Ring Lights", "If your job is filming yourself, sit down."),
            ("April Ferryman", "Teen Trend Translator for Parents", "My kid listens to a 22-year-old about banking. We're lost."),
        ],
    ),
    (
        "Vaccine Calendar Adds Shots; Public Adds Opinions",
        "Updated immunization schedules for various age groups rolled out with the usual mix of clinical guidance and social media fan fiction. What do you think?",
        [
            ("Buddy Neer", "Pharmacy Waiting Chair Historian", "I'll take the shot if the pharmacist doesn't upsell me gum."),
            ("Linda Ropp", "Symptom Tracker Spreadsheet Owner", "Science moves. Facebook stays dramatic."),
            ("Greg Huffman", "Man Who Needs a Brochure and a Nap", "Just put the schedule on one page. My brain is full."),
        ],
    ),
    (
        "Luxury Bunkers Sell Out as Rich Prepare for End Times in Style",
        "Demand for high-end underground shelters rose among the wealthy, complete with gyms, wine cellars, and the quiet admission that the future might be rude. What do you think?",
        [
            ("Earl Fraley", "Basement Canned Goods Minimalist", "My bunker is a pantry and a bad attitude."),
            ("Sharon Hedges", "Apocalypse Book Club Member", "If the world ends, I don't want to survive with those people."),
            ("Nadine Kizer", "Neighborly Tool Lender", "Community is the bunker. Also a generator."),
        ],
    ),
    (
        "Chatbots Begin Offering Therapy Vibes; Actual Therapists Request Boundaries",
        "AI companions marketed emotional support as clinicians warned about dependency, privacy, and the difference between comfort and care. What do you think?",
        [
            ("Dale Evilsizor", "Man Who Talks to His Dog Instead", "My dog keeps secrets better than a server."),
            ("Karen Pence", "Waiting List for a Human Therapist", "If the bot helps at 2 a.m., okay. If it bills my data, no."),
            ("Ron Bodey", "Feelings Avoidance Professional", "I don't want therapy from a toaster."),
        ],
    ),
    (
        "Global Plastic Treaty Talks Stall on Word 'Binding'",
        "International negotiators struggled to agree on enforceable plastics limits, proving diplomacy can recycle the same sentence for weeks. What do you think?",
        [
            ("Irene Neer", "Grocery Bag Decision Fatigue Patient", "Binding is the whole point. Otherwise it's a suggestion with flags."),
            ("Walt Huffman", "Man Who Reuses Butter Containers", "I already did my part. Your move, continents."),
            ("Tina Grove", "School Recycling Poster Artist", "Write a rule or stop the conference catering."),
        ],
    ),
    (
        "Sports Betting Ads Invade Every Broadcast Including Apparently Funerals Next",
        "Legalized betting partnerships flooded media with prop bets and apps, normalizing gambling the way commercials normalized pharmaceuticals. What do you think?",
        [
            ("Harlan Zerkle", "Church League Bowling Shark", "Betting on everything is how you make fun boring and expensive."),
            ("Denise Bodey", "Parent of a Teen With Notifications", "If it dings like candy, it's a problem."),
            ("Mitch Grove", "Casual Degenerate with a Budget Spreadsheet", "I'll bet on kickoffs but not on my dignity."),
        ],
    ),
    (
        "Hospitals Deploy AI Triage Tools; Waiting Rooms Remain Waiting Rooms",
        "Health systems piloted algorithms to prioritize care while patients continued to experience the ancient technology of fluorescent lighting and old magazines. What do you think?",
        [
            ("Carol Evilsizor", "Clipboard Form Calligrapher", "The AI can triage me after it finds me a chair."),
            ("Troy Pence", "ER Snack Machine Victim", "If it shortens the wait, bless it. If it misreads my pain, sue it."),
            ("April Ferryman", "Nurse Appreciation Casserole Deliverer", "Help the nurses first. Then help the robots."),
        ],
    ),
    (
        "Trade War Tariffs Return Like a Sequel Nobody Scripted Well",
        "New tariff threats and counters rolled through markets and factory towns, reviving arguments about jobs, prices, and who exactly pays at checkout. What do you think?",
        [
            ("Buddy Neer", "Made in USA Label Inspector", "Tariffs sound tough until the cart total bites."),
            ("Linda Ropp", "Price Tag Photographer for Group Chat", "I'll support workers. Also I need cheap towels."),
            ("Greg Huffman", "Factory Town Memory Keeper", "Jobs are real. Speeches are decorations."),
        ],
    ),
    (
        "Personal Carbon Scores Floated by Consultants; Public Floats Middle Finger",
        "Think tanks and startups discussed individual carbon tracking as a climate tool, a proposal received about as warmly as a surprise audit. What do you think?",
        [
            ("Earl Fraley", "Truck as Personality Extension", "Score my carbon and I'll score your nerve."),
            ("Sharon Hedges", "LED Bulb Early Adopter", "I'll change bulbs. I won't wear a guilt Fitbit."),
            ("Nadine Kizer", "Bus Rider Without a Press Release", "Tax the yachts before you lecture my casserole."),
        ],
    ),
    (
        "Quantum Computing Breakthrough Claimed; Passwords Still 'password123' for Most Users",
        "Labs touted progress toward quantum machines that could shatter encryption, while everyday security remained one reused password away from disaster. What do you think?",
        [
            ("Dale Evilsizor", "Sticky Note Password Museum Curator", "Quantum can wait. My login is on the monitor."),
            ("Karen Pence", "Two-Factor Authentication Hostage", "Text me a code forever. I don't care. Just don't lock me out."),
            ("Ron Bodey", "Man Who Thinks Incognito Mode Is a Disguise", "If hackers want my email, they'll be bored."),
        ],
    ),
    (
        "Celebrity Space Tourists Return With Profound Clichés About Earth",
        "Paying passengers completed suborbital trips and described the planet as fragile and beautiful, insights available free from any airplane window seat. What do you think?",
        [
            ("Irene Neer", "Window Seat Democrat", "I learned that for the price of pretzels."),
            ("Walt Huffman", "Grounded Patriot", "Earth is fine. People are the problem."),
            ("Tina Grove", "Science Teacher Who Deserves the Seat", "Send a kid next time, not a brand deal."),
        ],
    ),
    (
        "States Sue Social Platforms Over Youth Features Platforms Invented On Purpose",
        "Attorneys general advanced cases arguing that addictive design harms minors, while companies replied with the sacred rights of engagement metrics. What do you think?",
        [
            ("Harlan Zerkle", "Flip Phone Romantic", "If it dings every three seconds, it's not a tool, it's a slot machine."),
            ("Denise Bodey", "Parent of Three Notification Centers", "Sue them. Also help me set the controls without a degree."),
            ("Mitch Grove", "Former Teen Who Survived Boredom", "We had malls. It was worse and better."),
        ],
    ),
    (
        "Coffee Prices Spike on Crop Trouble; Americans Negotiate With Their Addiction",
        "Supply shocks pushed coffee higher, forcing households to confront whether the morning ritual is nonnegotiable or merely a hostage situation. What do you think?",
        [
            ("Carol Evilsizor", "Drip Coffee Fundamentalist", "I'll pay. Don't test me."),
            ("Troy Pence", "Gas Station Coffee Connoisseur", "There's always a hotter, worse cup nearby."),
            ("April Ferryman", "Oat Milk Diplomat", "If coffee goes luxury, society ends at 8 a.m."),
        ],
    ),
    (
        "Military Advises Public to Prepare 72-Hour Kits; Public Prepares Jokes",
        "Emergency agencies refreshed guidance on household preparedness for disasters, a sensible checklist that Americans turned into memes within minutes. What do you think?",
        [
            ("Buddy Neer", "Flashlight Battery Tester", "I have water, batteries, and denial for 72 hours."),
            ("Linda Ropp", "First Aid Kit Expired Bandage Curator", "Prepare? I can barely prepare dinner."),
            ("Greg Huffman", "Man Who Thinks His Truck Is a Plan", "My kit is a full tank and a bad map."),
        ],
    ),
    (
        "AI Customer Service Finally Passes Turing Test for Being Unhelpful",
        "Companies celebrated smarter support bots that can now fail to solve problems with near-human confidence and vocabulary. What do you think?",
        [
            ("Earl Fraley", "Zero Option Phone Menu Explorer", "I want a person who can say sorry like they mean the warranty."),
            ("Sharon Hedges", "Chat Bubble Rage Quilter", "It understood my words and ignored my needs."),
            ("Nadine Kizer", "Hold Music Lyricist", "Press 0 until God answers."),
        ],
    ),
    (
        "World Cup Host Planning Chaos Reminds Everyone Sports Are Logistics With Jerseys",
        "Organizers faced heat over venues, travel, and timelines for the global tournament, revealing that the beautiful game depends on ugly spreadsheets. What do you think?",
        [
            ("Dale Evilsizor", "Parking Lot Tailgate General", "I don't need perfection. I need a bathroom line under an hour."),
            ("Karen Pence", "Flag Face Paint Artist", "We'll watch anyway. Suffering is fandom."),
            ("Ron Bodey", "Man Who Calls Every Tournament a Distraction", "Bread and circuses, but with vuvuzelas."),
        ],
    ),
    (
        "Scientists Warn Ultraprocessed Food Is Bad; Ultraprocessed Food Remains Delicious",
        "Nutrition studies linked heavily processed diets to health risks as grocery aisles continued to look like a candy-colored engineering exhibit. What do you think?",
        [
            ("Irene Neer", "Casserole From a Can Artist", "If it has a shelf life longer than my dog, maybe rethink it."),
            ("Walt Huffman", "Chips as a Food Group Defender", "Everything kills you. At least this crunch is honest."),
            ("Tina Grove", "Meal Prep Sunday Dropout", "I'll cook more when time becomes free."),
        ],
    ),
    (
        "Privacy Law Forces Cookie Popups So Aggressive They Become a Personality Trait",
        "New compliance rules multiplied consent banners until simply reading news required accepting or rejecting a small novel. What do you think?",
        [
            ("Harlan Zerkle", "Reject All Button Speedrunner", "I reject all and still get ads for boots."),
            ("Denise Bodey", "Woman Who Reads the First Line Only", "Just give me the article. Stop negotiating."),
            ("Mitch Grove", "Incognito Mode False Sense of Security", "Cookies used to be food. Simpler times."),
        ],
    ),
    (
        "Autonomous Weapons Debated at UN While Video Games Normalized Them Years Ago",
        "Diplomats argued limits on lethal autonomous systems as younger generations noted they have been virtually deploying them since middle school. What do you think?",
        [
            ("Carol Evilsizor", "Mom Who Doesn't Understand Respawn", "Robots that kill should require more meetings than robots that vacuum."),
            ("Troy Pence", "Call of Duty Historian", "We've been training for this on couches."),
            ("April Ferryman", "Peace Is a Casserole Believer", "If it can shoot without a person, don't build it. Full stop."),
        ],
    ),
    (
        "Housing Prices Stay Absurd; Grown Adults Invent New Definitions of 'Starter Home'",
        "Markets continued to price first-time buyers out as listings for modest houses read like luxury ads and 'starter' began to mean 'maybe in a decade.' What do you think?",
        [
            ("Buddy Neer", "Paid-Off Mortgage Smugness Society", "We bought when houses cost a truck. Sorry not sorry."),
            ("Linda Ropp", "Interest Rate Doom Scroller", "A starter home shouldn't require a trust fund."),
            ("Greg Huffman", "Basement Apartment Philosopher", "I'll move out when math starts making sense."),
        ],
    ),
    (
        "Deepfake Porn Laws Advance as Technology Outruns Shame",
        "Legislatures moved to criminalize nonconsensual synthetic intimate images, a rare tech policy area with bipartisan disgust if not always bipartisan competence. What do you think?",
        [
            ("Earl Fraley", "Man Who Still Thinks the Internet Is Optional", "If it's fake and filthy and nonconsensual, lock somebody up."),
            ("Sharon Hedges", "Parent of a Daughter With a Phone", "Write the law in plain English and enforce it yesterday."),
            ("Nadine Kizer", "Group Chat Decency Moderator", "Tech did this. Tech can help undo it. Also laws."),
        ],
    ),
    (
        "Airline Seat Sizes Shrink Again in Defiance of Human Hips",
        "Carriers adjusted cabin layouts for density while passengers continued to be shaped like people, not revenue models. What do you think?",
        [
            ("Dale Evilsizor", "Middle Seat Martyr", "My knees have rights."),
            ("Karen Pence", "Armrest Treaty Negotiator", "Charge me for legroom or stop pretending this is travel."),
            ("Ron Bodey", "Man Who Drives 12 Hours Instead", "I'll take the truck. The truck respects me."),
        ],
    ),
    (
        "National Archives Digitize History; Commenters Immediately Request Cover-Ups",
        "A major digitization push made more records searchable online, which delighted historians and terrified anyone who has ever written a dumb memo. What do you think?",
        [
            ("Irene Neer", "Scrapbook Preservationist", "Put it online. Truth can handle bandwidth."),
            ("Walt Huffman", "Man Who Burns Old Letters 'For Privacy'", "Some things should stay in boxes."),
            ("Tina Grove", "Genealogy Website Addict", "I want the records and also I fear the records."),
        ],
    ),
    (
        "Energy Drink Market Targets Kids With Cartoons and 300mg of Bad Decisions",
        "Regulators and parents clashed with beverage marketers over youth-focused caffeine products that turn Tuesday into a medical event. What do you think?",
        [
            ("Harlan Zerkle", "Coffee Before It Was Extreme", "Kids need water and consequences, not wings."),
            ("Denise Bodey", "Youth Sports Snack Table Manager", "If it glows, it doesn't go in a lunchbox."),
            ("Mitch Grove", "Convenience Store Philosopher", "I drank one and saw God. God told me to nap."),
        ],
    ),
    (
        "Global Summit on AI Safety Produces Communiqué Strong Enough to Frame",
        "World leaders issued a joint statement on artificial intelligence risks that used many verbs and few enforceable nouns. What do you think?",
        [
            ("Carol Evilsizor", "Committee Minutes Translator", "A communiqué is a group project where nobody does the homework."),
            ("Troy Pence", "Man Who Wants Simple Rules", "Don't build the Skynet. Meeting adjourned."),
            ("April Ferryman", "Science Fair Ribbon Presenter", "If they can't explain it to a 10-year-old, they can't govern it."),
        ],
    ),
    (
        "Telehealth Flexibilities Extended; People Keep Showing Doctors Their Throats Over Wi-Fi",
        "Regulators kept pandemic-era virtual care options alive as patients perfected the art of aiming a phone camera at a rash with confidence. What do you think?",
        [
            ("Buddy Neer", "Hold the Phone Higher Patient", "I miss when the doctor could smell I was sick."),
            ("Linda Ropp", "Rural Drive-Time Calculator", "If it saves me 90 minutes, pixelate my tonsils."),
            ("Greg Huffman", "Man Who Distrusts Webcams", "Fine for refills. Not for anything that can kill me stylishly."),
        ],
    ),
    (
        "Stock Market Hits Record on Hopes Alone; Retirement Accounts Feel Emotions",
        "Indexes climbed on soft-landing optimism and AI enthusiasm, which is great news unless you sold everything in March out of principle. What do you think?",
        [
            ("Earl Fraley", "401(k) Statement Avoider", "If I don't open the email, it can't hurt me."),
            ("Sharon Hedges", "Index Fund Church Member", "Records are nice. Grocery prices are the sermon."),
            ("Nadine Kizer", "Woman Who Invests in Casseroles", "Wake me when the market pays for brakes."),
        ],
    ),
    (
        "Politicians Discover Video Games Are Real, Immediately Mispronounce Them",
        "A hearing on gaming, money, and youth featured elected officials naming titles with the confidence of someone reading a foreign menu. What do you think?",
        [
            ("Dale Evilsizor", "Controller Dual-Wield Grandpa", "They regulate what they can't pronounce. Classic."),
            ("Karen Pence", "Parent Who Pays the V-Bucks", "Focus on the money sink, not the elf swords."),
            ("Ron Bodey", "Man Who Thinks Games Rot Brains Selectively", "My brain rotted on free TV. Cheaper."),
        ],
    ),
    (
        "Lab-Grown Diamonds Crash Wedding Budgets and Also Certain Uncles' Opinions",
        "Cheaper lab diamonds gained share as jewelers and traditionalists fought over meaning, rarity, and whether love requires a hole in the ground. What do you think?",
        [
            ("Irene Neer", "Wedding Industrial Complex Escapee", "If it sparkles and nobody bled for a cartel, I'm good."),
            ("Walt Huffman", "Man Who Bought a Ring in 1989", "I paid real money for real pressure. Kids these days get science."),
            ("Tina Grove", "Etsy Ring Browser", "Spend on the honeymoon. Rocks are rocks."),
        ],
    ),
    (
        "Cities Experiment With Congestion Pricing; Suburbs Treat It Like a Personal Attack",
        "Urban toll schemes aimed at traffic and pollution expanded, and drivers everywhere declared it the end of freedom to sit in traffic for free. What do you think?",
        [
            ("Harlan Zerkle", "Bypass Route Folklorist", "Charge me to sit still? At least buy me coffee."),
            ("Denise Bodey", "Carpool Lane Moralist", "If it funds trains that work, fine. If it's just a fee, no."),
            ("Mitch Grove", "Man Who Leaves Two Hours Early Out of Spite", "I'll wake up earlier than your policy."),
        ],
    ),
    (
        "Bee Populations Still Struggling; Almond Milk Feels Awkward",
        "Ecologists reported continued pressure on pollinators essential to food systems, a crisis that makes breakfast choices suddenly ethical. What do you think?",
        [
            ("Carol Evilsizor", "Garden Club Pollinator Committee", "Plant flowers. Stop mowing everything into a golf course."),
            ("Troy Pence", "Man Who Swats First", "I support bees in theory. In my soda, less so."),
            ("April Ferryman", "Honey in Tea Traditionalist", "If the bees go, cereal gets weird. Pay attention."),
        ],
    ),
    (
        "Government Tries Once-A-Year Tax Reform Conversation; Lobbyists Bring Snacks",
        "Annual attempts to simplify the tax code produced hearings, white papers, and no simplification, as complex rules protect complex interests. What do you think?",
        [
            ("Buddy Neer", "Standard Deduction Absolutist", "If I need software, the code failed."),
            ("Linda Ropp", "Charitable Donation Envelope Counter", "Make it fair and boring. Boring is good governance."),
            ("Greg Huffman", "Man Who Thinks Loopholes Are for Other People", "Close theirs. Keep mine. I'm nuanced."),
        ],
    ),
    (
        "AI Voice Clones Scam Grandparents; Grandparents Stay One Step Too Trusting",
        "Fraud rings using cloned voices of relatives surged, exploiting love and caller ID in equal measure. What do you think?",
        [
            ("Earl Fraley", "Grandparent Scam Interceptor", "We need a family code word. Mine is 'casserole.'"),
            ("Sharon Hedges", "Woman Who Calls Back on a Known Number", "If it's urgent, hang up and dial real."),
            ("Nadine Kizer", "Church Elder Tech Class Teacher", "I'll teach them. Bring cookies and patience."),
        ],
    ),
    (
        "National Spelling Bee Includes Words Nobody Should Be Forced to Pronounce",
        "The bee reached rounds with vocabulary that felt designed by a sadistic dictionary, delighting language nerds and terrifying parents. What do you think?",
        [
            ("Dale Evilsizor", "Autocorrect Dependent", "If spellcheck fails, the word shouldn't exist."),
            ("Karen Pence", "Pronouncer Sympathy Society", "These kids are tougher than Congress."),
            ("Ron Bodey", "Man Who Spells How He Speaks", "I respect it. I will not attempt it."),
        ],
    ),
    (
        "Meatless Burgers Quietly Retreat From Menus as Hype Cycle Completes",
        "Several chains reduced plant-based options after demand cooled, a market correction that vegans saw coming and marketers called a learning moment. What do you think?",
        [
            ("Irene Neer", "Black Bean Burger Diplomat", "I liked them. I also like not being lectured by a commercial."),
            ("Walt Huffman", "Beef Loyalty Program", "The cow always wins in this county."),
            ("Tina Grove", "Flexitarian Without a Label", "Put both on the menu and stop the culture war."),
        ],
    ),
    (
        "Scientists Confirm Universe Expansion Is Accelerating; Local Concerns Remain Parking-Related",
        "Astrophysicists reaffirmed that the universe's expansion is speeding up for reasons still debated, a finding that changes nothing about the school board agenda. What do you think?",
        [
            ("Harlan Zerkle", "Night Sky Smoker of One Cigar a Year", "Space is big and getting ruder. Noted."),
            ("Denise Bodey", "Existential Dread Compartmentalizer", "If the universe is accelerating, why is my package not?"),
            ("Mitch Grove", "Man Who Needs Problems He Can Hit With a Hammer", "Cool. Wake me when it affects corn."),
        ],
    ),
]


def slugify(s: str) -> str:
    s = s.lower().strip()
    s = re.sub(r"[^a-z0-9\s-]", "", s)
    s = re.sub(r"[\s_]+", "-", s)
    return re.sub(r"-+", "-", s).strip("-") or "voices"


def main() -> None:
    # Prefer the stronger openers as the most recent (homepage) pieces
    packages = list(reversed(PACKAGES[:100]))
    if len(packages) != 100:
        raise SystemExit(f"Expected 100 packages, got {len(packages)}")

    OUT.mkdir(parents=True, exist_ok=True)
    # Wipe prior generated stories only (not README)
    for p in OUT.glob("*.md"):
        if p.name.upper() in ("README.MD", "INDEX.MD", "SCHEDULING.MD"):
            continue
        p.unlink()

    # Spread dates: end on 2026-07-20, one per day backward so latest is most recent big-news energy
    end = date(2026, 7, 20)
    start = end - timedelta(days=len(packages) - 1)

    for i, (title, lede, people) in enumerate(packages):
        d = start + timedelta(days=i)
        slug = slugify(title)[:80]
        # rotate distinct portraits for the trio
        p0 = PORTRAITS[i % len(PORTRAITS)]
        p1 = PORTRAITS[(i + 3) % len(PORTRAITS)]
        p2 = PORTRAITS[(i + 6) % len(PORTRAITS)]
        ports = [p0, p1, p2]
        # ensure unique within piece
        seen = set()
        for j, pid in enumerate(ports):
            if pid in seen:
                for alt in PORTRAITS:
                    if alt not in seen:
                        ports[j] = alt
                        break
            seen.add(ports[j])

        lines = [
            "---",
            f'title: "{title.replace(chr(34), chr(39))}"',
            f"slug: {slug}",
            f"date: {d.isoformat()}",
            f"publish_date: {d.isoformat()}",
            "lede: >",
        ]
        # fold lede
        for chunk in _wrap(lede, 88):
            lines.append(f"  {chunk}")
        lines.append("people:")
        for j, (name, job, quote) in enumerate(people):
            lines.append(f"  - portrait: {ports[j]}")
            lines.append(f'    name: "{name}"')
            lines.append(f'    title: "{job.replace(chr(34), chr(39))}"')
            lines.append(f'    quote: "{quote.replace(chr(34), chr(39))}"')
        lines.append("---")
        lines.append("")

        path = OUT / f"{d.isoformat()}-{slug}.md"
        path.write_text("\n".join(lines), encoding="utf-8")

    print(f"Wrote {len(packages)} Champaign Voices → {OUT}")
    print(f"Date range: {start.isoformat()} → {end.isoformat()}")


def _wrap(text: str, width: int) -> list[str]:
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


if __name__ == "__main__":
    main()
