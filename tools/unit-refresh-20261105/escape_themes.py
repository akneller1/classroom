# Escape Room themes: one per course unit. Fields:
# title, room (singular noun for each room), introEmoji, endEmoji, intro, word (5-letter final password),
# cipher (sentence, capitals and spaces only), clue (word inside the cipher), ask, outro, scene emojis (4), bg, floor
T = {}
def t(key, title, room, ie, ee, intro, word, cipher, clue, ask, outro, scene, bg, floor):
    T[key] = dict(title=title, room=room, introEmoji=ie, endEmoji=ee, intro=intro, word=word, cipher=cipher, clue=clue, ask=ask, outro=outro, scene=scene, bg=bg, floor=floor)

# ---------------- Grade 6
t("math6/ratios-rates-percent-proportions", "Smoothie Shop Shutdown", "station", "🥤", "🍓🏆",
  "The blender jammed and the Smoothie Shop locked down with your class inside! Every station opens with a ratio, rate, or percent code. Crack all five before the shop alarm sounds in <b>10 minutes</b>.",
  "MANGO", "THE SPARE KEY IS IN THE FREEZER", "FREEZER", "Where is the spare key?",
  "The register beeps MANGO and the doors slide open. Free smoothies for the whole team!", ["🍓", "🍌", "🥭", "🧊"], "#2b1638", "#5a2d4f")
t("math6/fractions-decimals-operations", "The Pizza Parlor Puzzle", "kitchen", "🍕", "🍕🏆",
  "The pizza oven timer locked every door in Pepe's Pizza Parlor. Each kitchen opens only when you slice the fraction and decimal problems correctly. You have <b>10 minutes</b> before the oven overheats.",
  "CRUST", "THE OVEN CODE IS UNDER THE BASIL", "BASIL", "Where is the oven code?",
  "The keypad flashes CRUST and the oven cools. Pepe hands out slices to the whole crew.", ["🍕", "🧀", "🍅", "🌿"], "#3a1a12", "#6b3420")
t("math6/rational-numbers", "Below Zero: The Ice Cave", "cavern", "🧊", "❄️🏆",
  "Your field trip took a wrong turn into an ice cave where every temperature is below zero. Each cavern gate needs a number-line code. Find the way out in <b>10 minutes</b> before the tunnel freezes shut.",
  "FROST", "THE EXIT MAP IS INSIDE THE IGLOO", "IGLOO", "Where is the exit map?",
  "The ice wall cracks open after you enter FROST. Sunlight and warm cocoa wait outside.", ["🧊", "🐧", "❄️", "🔦"], "#0c2440", "#1d4a6e")
t("math6/expressions-equations", "The Secret Recipe Lab", "lab", "🧪", "🧁🏆",
  "Professor Pinch locked her cupcake lab and hid the secret recipe behind five expression locks. Simplify, evaluate and solve to open each lab before the batter sets in <b>10 minutes</b>.",
  "WHISK", "THE RECIPE CARD IS BEHIND THE MIXER", "MIXER", "Where is the recipe card?",
  "WHISK! The vault pops open and the secret recipe is yours. Cupcakes for everyone.", ["🧁", "🥣", "🧪", "🍫"], "#2a1a35", "#4b2f5c")
t("math6/inequalities", "Roller Coaster Height Check", "ride", "🎢", "🎡🏆",
  "The theme park's ride computers crashed and every gate now asks an inequality question. Prove you know who can ride and who must wait, and reach the exit in <b>10 minutes</b>.",
  "TRACK", "THE RIDE KEY IS IN THE TICKET BOOTH", "BOOTH", "Where is the ride key?",
  "TRACK lights up on the control panel and the coasters roll again. Front-row seats for your team!", ["🎢", "🎟️", "🍿", "🎈"], "#1f1640", "#3b2a70")
t("math6/geometry", "Treehouse Builders", "deck", "🌳", "🏡🏆",
  "The treehouse ladder pulled itself up and left your team stranded on the deck! Measure areas, nets and volumes to unlock each deck and climb down in <b>10 minutes</b>.",
  "PLANK", "THE ROPE LADDER IS NEAR THE ACORN", "ACORN", "Where is the rope ladder?",
  "PLANK opens the trap door and the ladder drops down. Best treehouse builders in town!", ["🌳", "🪵", "🔨", "🐿️"], "#13301c", "#2e5a2f")
t("math6/data-displays", "Weather Station Blackout", "tower", "🌦️", "📡🏆",
  "A storm knocked out the weather station and every tower is locked. Read dot plots, histograms and box plots to restore each tower before the next storm arrives in <b>10 minutes</b>.",
  "STORM", "THE BACKUP POWER IS BY THE RAIN GAUGE", "GAUGE", "Where is the backup power?",
  "STORM! The radar spins back on and the forecast is saved.", ["🌦️", "📡", "🌡️", "🌬️"], "#10213a", "#25415f")

# ---------------- Grade 7
t("prealgebra7/algebraic-expressions-integers", "Submarine Depth Dive", "deck", "🚢", "🌊🏆",
  "Your research submarine is sinking deeper with every wrong move. Each hatch needs an integer or expression code. Surface safely in <b>10 minutes</b>.",
  "SONAR", "THE HATCH WHEEL IS NEAR THE PERISCOPE", "PERISCOPE", "Where is the hatch wheel?",
  "SONAR pings back and the submarine rises to the surface. Mission accomplished, crew!", ["🐠", "⚓", "🔦", "🐙"], "#06243a", "#0e3c5a")
t("prealgebra7/one-step-equations-inequalities", "The Locked Library", "aisle", "📚", "📖🏆",
  "The library's book-return robot locked every aisle after closing. Each aisle opens with a one-step equation or inequality. Escape before the night guard's rounds in <b>10 minutes</b>.",
  "SHELF", "THE MASTER KEY IS UNDER THE ATLAS", "ATLAS", "Where is the master key?",
  "SHELF unlocks the front doors. The robot even stamps your library cards on the way out.", ["📚", "📖", "🤖", "🕯️"], "#2b1d14", "#4d3624")
t("prealgebra7/decimals-equations", "Market Day Mix-Up", "stall", "🛒", "🧺🏆",
  "The farmers market vault holds today's earnings, and the coin counter scrambled every lock. Round, estimate and solve decimal equations to open each stall in <b>10 minutes</b>.",
  "PEACH", "THE CASH BOX IS UNDER THE PUMPKINS", "PUMPKINS", "Where is the cash box?",
  "PEACH opens the vault and every stall gets paid on time.", ["🍎", "🥕", "🧺", "💵"], "#2d2412", "#544122")
t("prealgebra7/factors-fractions-exponents", "Castle Code Breakers", "tower", "🏰", "👑🏆",
  "The castle drawbridge rose with your team inside! Each tower door is guarded by factors, primes, fractions and exponents. Lower the bridge in <b>10 minutes</b>.",
  "CROWN", "THE DRAWBRIDGE CRANK IS IN THE ARMORY", "ARMORY", "Where is the drawbridge crank?",
  "CROWN! The drawbridge thunders down and the royal court cheers.", ["🏰", "🛡️", "🗡️", "🕯️"], "#24182e", "#4a3756")
t("prealgebra7/operations-fractions", "Bakery Measurement Mayhem", "oven", "🥐", "🥖🏆",
  "Every oven in the Bread Box Bakery locked while the dough was still rising. Add, subtract, multiply and divide fractions to rescue each oven in <b>10 minutes</b>.",
  "DOUGH", "THE OVEN KEY IS BEHIND THE FLOUR SACKS", "FLOUR", "Where is the oven key?",
  "DOUGH opens the last oven just in time. The bakery smells amazing.", ["🥐", "🥖", "🧈", "🥧"], "#33200f", "#5d3a1c")
t("prealgebra7/ratios-proportions-percentages", "Sneaker Sale Stampede", "aisle", "👟", "🛍️🏆",
  "The mall's Mega Sneaker Sale locked down at closing. Every aisle wants a ratio, proportion or percent answer. Check out before the lights go off in <b>10 minutes</b>.",
  "LACES", "THE STOCKROOM KEY IS IN THE SHOEBOX", "SHOEBOX", "Where is the stockroom key?",
  "LACES works and the doors open. You leave with the best deals in the mall.", ["👟", "🏷️", "🛍️", "💳"], "#1d1d36", "#37375f")
t("prealgebra7/solving-equations-inequalities", "Volcano Island Rescue", "camp", "🌋", "🚁🏆",
  "The volcano is rumbling and the rescue helicopter only lands when every camp is cleared. Solve multi-step equations and inequalities to reach the helipad in <b>10 minutes</b>.",
  "MAGMA", "THE FLARE GUN IS BESIDE THE CANOE", "CANOE", "Where is the flare gun?",
  "MAGMA opens the helipad gate. The helicopter lifts off as the volcano smokes below.", ["🌋", "🌴", "🔥", "🦜"], "#3a1208", "#5c2410")
t("prealgebra7/linear-functions-graphing", "Ski Slope Speedway", "chairlift", "⛷️", "🏔️🏆",
  "A whiteout stopped every chairlift on Mount Gradient. Read slopes, tables and graphs to restart each chairlift and get down the mountain in <b>10 minutes</b>.",
  "SLOPE", "THE LIFT CONTROLS ARE IN THE WARMING HUT", "HUT", "Where are the lift controls?",
  "SLOPE restarts the lifts and the team glides back to the lodge.", ["⛷️", "🏔️", "🎿", "☕"], "#13253f", "#e9eef7")
t("prealgebra7/spatial-thinking", "Origami Escape", "folding room", "📄", "🦢🏆",
  "A paper artist folded your team into her studio! Each room is a puzzle of nets, cross sections and views. Unfold your way out in <b>10 minutes</b>.",
  "CRANE", "THE EXIT FOLD IS UNDER THE LANTERN", "LANTERN", "Where is the exit fold?",
  "CRANE! A giant paper crane flaps open the studio door.", ["📄", "✂️", "🏮", "🦢"], "#2a2a33", "#4a4a5c")
t("prealgebra7/area-volume", "Aquarium After Hours", "tank", "🐠", "🐋🏆",
  "The aquarium's doors locked while you were watching the sharks. Each tank room opens with an area or volume code. Find the exit in <b>10 minutes</b> before feeding time.",
  "CORAL", "THE EXIT PASS IS BY THE STINGRAYS", "STINGRAYS", "Where is the exit pass?",
  "CORAL unlocks the lobby and a dolphin splashes goodbye.", ["🐠", "🦈", "🐢", "🪸"], "#062a3a", "#0f4a5e")
t("prealgebra7/right-triangles-algebra", "Pirate Ship Rigging", "deck", "🏴‍☠️", "⚓🏆",
  "Captain Hypotenuse locked your crew below deck. Every hatch opens with a right-triangle or square-root code. Escape before the ship sails in <b>10 minutes</b>.",
  "MASTS", "THE CAPTAINS KEY IS IN THE CROWS NEST", "NEST", "Where is the captain's key?",
  "MASTS opens the hatch and your crew takes the helm.", ["🏴‍☠️", "⚓", "🗺️", "🦜"], "#1b1a2e", "#4a3424")
t("prealgebra7/data-analysis-probability", "Game Show Showdown", "booth", "🎰", "🎉🏆",
  "The game show set locked between rounds! Every booth asks a statistics or probability question. Win your way off the stage in <b>10 minutes</b>.",
  "PRIZE", "THE BACKSTAGE PASS IS UNDER THE SPINNER", "SPINNER", "Where is the backstage pass?",
  "PRIZE lights up in neon and the audience goes wild. You win!", ["🎰", "🎲", "🎤", "🎁"], "#2c1035", "#52205f")
t("prealgebra7/nonlinear-functions-polynomials", "Rocket Garden Greenhouse", "greenhouse", "🌱", "🌻🏆",
  "Strange plants in the greenhouse grow faster than any straight line! Each greenhouse door needs a nonlinear function or polynomial code. Get out in <b>10 minutes</b> before the vines close in.",
  "BLOOM", "THE GATE KEY IS UNDER THE SUNFLOWER", "SUNFLOWER", "Where is the gate key?",
  "BLOOM opens the gate and the vines politely step aside.", ["🌱", "🌻", "🪴", "🐝"], "#12301a", "#2d5a2a")

# ---------------- Grade 8
t("prealgebra/real-numbers-exponents", "Star Cruiser Countdown", "module", "🛰️", "🌠🏆",
  "Your star cruiser's computer locked every module before launch. Square roots, exponents and scientific notation unlock each one. Launch in <b>10 minutes</b>.",
  "NOVAS", "THE LAUNCH KEY IS INSIDE THE SATELLITE", "SATELLITE", "Where is the launch key?",
  "NOVAS starts the engines and the cruiser blasts into orbit.", ["🛰️", "🌌", "🔭", "🪐"], "#090b22", "#1c1f45")
t("prealgebra/equations-expressions", "Detective Agency Lockdown", "office", "🕵️", "🔍🏆",
  "The detective agency's security system locked every office during your interview. Solve equations to crack each office and leave in <b>10 minutes</b>.",
  "CLUES", "THE CASE FILE IS IN THE COAT RACK", "RACK", "Where is the case file?",
  "CLUES opens the front door. Welcome to the agency, junior detectives.", ["🕵️", "🔍", "📁", "🧥"], "#1d1a17", "#3a332b")
t("prealgebra/linear-functional-relationships", "Bullet Train Breakdown", "car", "🚄", "🚉🏆",
  "The bullet train stopped between stations and every car door locked. Read rates of change and functions to restart the train in <b>10 minutes</b>.",
  "RAILS", "THE CONDUCTOR KEY IS IN THE DINING CAR", "DINING", "Where is the conductor key?",
  "RAILS restarts the engine and the train pulls into the station right on time.", ["🚄", "🎫", "🧳", "🍱"], "#16202e", "#30435a")
t("prealgebra/systems-linear-equations", "Twin Tunnel Mine", "tunnel", "⛏️", "💎🏆",
  "Two mine tunnels cross deep underground, and the elevator only opens where the paths meet. Solve systems to unlock each tunnel in <b>10 minutes</b>.",
  "DRILL", "THE ELEVATOR LEVER IS BY THE MINECART", "MINECART", "Where is the elevator lever?",
  "DRILL works! The elevator rumbles up into daylight.", ["⛏️", "💎", "🪨", "🔦"], "#1e1612", "#3d2c20")
t("prealgebra/patterns-bivariate-data", "Science Fair Fiasco", "booth", "🔬", "🥇🏆",
  "The science fair judges locked every booth until someone reads the scatter plots correctly. Find trends and lines of fit to open each booth in <b>10 minutes</b>.",
  "TREND", "THE BLUE RIBBON IS UNDER THE MICROSCOPE", "MICROSCOPE", "Where is the blue ribbon?",
  "TREND wins the grand prize and the gym doors open.", ["🔬", "🧫", "📊", "🎗️"], "#14243a", "#2c4566")
t("prealgebra/congruence-similarity", "Hall of Mirrors Carnival", "mirror hall", "🪞", "🎪🏆",
  "The carnival's Hall of Mirrors shuffled itself and locked every hall. Translations, rotations, reflections and dilations unlock each one. Escape in <b>10 minutes</b>.",
  "PRISM", "THE EXIT IS BEHIND THE CRACKED MIRROR", "CRACKED", "Where is the exit?",
  "PRISM sends light through the last mirror and the exit appears.", ["🪞", "🎪", "🎠", "✨"], "#22123a", "#43266a")
t("prealgebra/geometry-applications", "Lost Temple Expedition", "chamber", "🗿", "🏺🏆",
  "Your expedition team triggered a trap in the Lost Temple! Each chamber opens with an angle, Pythagorean or volume code. Escape in <b>10 minutes</b> before the sand fills the room.",
  "IDOLS", "THE SECRET DOOR IS BEHIND THE STATUE", "STATUE", "Where is the secret door?",
  "IDOLS slides the stone aside and sunlight floods in. Expedition complete!", ["🗿", "🏺", "🐍", "🕯️"], "#2a2110", "#4f3e1c")

# ---------------- Algebra 1 (reusing the original one-off rooms where they were unique)
t("algebra/foundations-algebra", "Night Shift at the Clock Tower", "floor", "🕰️", "🔔🏆",
  "The clock tower's gears jammed at midnight and locked your class inside. Each floor opens with an order-of-operations or real-number code. Reach the bell in <b>10 minutes</b>.",
  "CHIME", "THE TOWER KEY IS BEHIND THE PENDULUM", "PENDULUM", "Where is the tower key?",
  "CHIME rings out across town and the tower door swings open.", ["🕰️", "⚙️", "🔔", "🦉"], "#1c1a2c", "#3a3550")
t("algebra/expressions-equations", "The Great Rigged Bake-Off", "kitchen", "🍰", "🎂🏆",
  "Someone rigged the Great Bake-Off and locked the kitchens! Solve the equations to unlock each kitchen and win the bake-off in <b>10 minutes</b>.",
  "LEMON", "THE RECIPE IS IN THE PANTRY", "PANTRY", "Where is the recipe?",
  "LEMON wins the bake-off and the judges unlock the tent.", ["🍰", "🥚", "🍋", "🧁"], "#32172a", "#5a2d48")
t("algebra/inequalities", "Code Red: Station Nimbus", "module", "🚨", "🛸🏆",
  "Space Station Nimbus is losing air, and every module door asks an inequality question. Reach the escape pods in <b>10 minutes</b>.",
  "HATCH", "ESCAPE PODS ARE ON DECK NINE", "NINE", "Which deck has the escape pods?",
  "HATCH opens the escape pod and you drift safely home.", ["🛰️", "🚨", "👩‍🚀", "🛸"], "#0b0f24", "#20284a")
t("algebra/relations-functions", "Escape the Function Factory", "assembly line", "🏭", "⚙️🏆",
  "The Function Factory's machines locked down mid-shift. Every assembly line needs a domain, range or function code. Escape in <b>10 minutes</b>.",
  "GEARS", "THE NEXT KEY IS HIDDEN IN THE BOILER", "BOILER", "Where is the next key?",
  "GEARS turns the last machine off and the factory doors roll up.", ["🏭", "⚙️", "🔧", "📦"], "#1f1f24", "#3d3d46")
t("algebra/linear-equations-slope", "Avalanche Patrol: Race to the Lodge", "checkpoint", "🏂", "🏔️🏆",
  "An avalanche cut off the ski patrol route. Each checkpoint radio needs a slope or linear-equation code. Reach the lodge in <b>10 minutes</b>.",
  "LODGE", "THE RADIO CODE IS SNOWPLOW", "SNOWPLOW", "What is the radio code?",
  "LODGE clears the final gate and the whole patrol reaches safety.", ["🏂", "❄️", "📻", "🚩"], "#122640", "#e8eef6")
t("algebra/systems-of-equations", "Locked In: After Hours at the Art Gallery", "gallery", "🖼️", "🎨🏆",
  "The art gallery's alarm locked every room after closing. Solve each system of equations to open the galleries in <b>10 minutes</b>.",
  "MOUSE", "THE SAFE WORD IS TULIP", "TULIP", "What is the safe word?",
  "MOUSE opens the last gallery. The guard is impressed by your detective work.", ["🖼️", "🎨", "🗿", "🐭"], "#22162a", "#43304f")
t("algebra/exponents-exponential-functions", "Escape the Rocket Lab", "bay", "🚀", "🪐🏆",
  "The rocket lab sealed every launch bay for a test countdown. Exponent rules and scientific notation unlock each bay. Escape in <b>10 minutes</b>.",
  "ORBIT", "THE NEXT KEY IS IN THE AIRLOCK", "AIRLOCK", "Where is the next key?",
  "ORBIT clears the countdown and the blast doors slide open.", ["🚀", "🧑‍🚀", "🛠️", "🔥"], "#0d1028", "#252a52")
t("algebra/exponential-functions", "Dr. Petri's Growth Lab", "lab", "🦠", "🧬🏆",
  "Dr. Petri's bacteria are doubling and the lab is in lockdown. Each lab opens with an exponential growth or decay code. Stop the outbreak in <b>10 minutes</b>.",
  "PETRI", "THE SERUM IS BLUE", "BLUE", "What color is the serum?",
  "PETRI unlocks the cure and the outbreak is contained.", ["🦠", "🧫", "🧪", "🥼"], "#102a24", "#22483e")
t("algebra/polynomials-factoring", "Escape the Toy Workshop", "workbench", "🧸", "🎁🏆",
  "The toy workshop's wind-up robots locked every workbench. Add, subtract and multiply polynomials to open each one in <b>10 minutes</b>.",
  "BLOCK", "THE NEXT KEY IS INSIDE THE DRUM", "DRUM", "Where is the next key?",
  "BLOCK stacks into place and the workshop door opens.", ["🧸", "🥁", "🪀", "🎁"], "#2c1a14", "#523428")
t("algebra/factoring-zero-product", "The Wizard's Spell Library", "spell room", "🧙", "✨🏆",
  "The wizard's library sealed itself with factoring spells. Factor and use the zero product property to break each spell in <b>10 minutes</b>.",
  "MAGIC", "THE MAGIC WORD IS GLOW", "GLOW", "What is the magic word?",
  "MAGIC breaks the final seal and the library doors fly open.", ["🧙", "📜", "🔮", "🕯️"], "#1d1436", "#3a2a63")
t("algebra/quadratics", "Thunder Bolt: Launch Gone Wrong", "ride", "⚡", "🎢🏆",
  "The Thunder Bolt launch coaster froze mid-track. Each ride panel needs a quadratic code. Restart the ride in <b>10 minutes</b>.",
  "BRAKE", "THE PASSWORD IS BOLTS", "BOLTS", "What is the password?",
  "BRAKE releases and the coaster rolls safely back to the station.", ["⚡", "🎢", "🔩", "🎟️"], "#1a1430", "#352b5c")
t("algebra/statistics-data-modeling", "Escape the Stats Lab", "lab", "📊", "📈🏆",
  "The stats lab's scoreboard glitched and locked everyone in. Each lab opens with a data or regression code. Escape in <b>10 minutes</b>.",
  "GRAPH", "THE NEXT KEY IS UNDER THE SCOREBOARD", "SCOREBOARD", "Where is the next key?",
  "GRAPH lights up the scoreboard and the doors unlock.", ["📊", "📈", "🧮", "🏀"], "#13213a", "#2b4568")

# ---------------- Geometry
t("geometry/foundations-geometry", "Temple of Logic: Jungle Escape", "shrine", "🛕", "🦜🏆",
  "The jungle temple's stone doors close on anyone who reasons badly. Points, lines, planes and logic unlock each shrine. Escape in <b>10 minutes</b>.",
  "LOGIC", "SAY THE WORD PARROT", "PARROT", "What word must you say?",
  "LOGIC opens the last shrine and the jungle path appears.", ["🛕", "🦜", "🌿", "🐒"], "#132a17", "#2b4a26")
t("geometry/angles-parallel-lines", "Crossing Tracks: Rail Yard Escape", "switch tower", "🚂", "🚦🏆",
  "Trains are crossing on parallel tracks and the switch towers are locked. Use angle relationships to set each switch in <b>10 minutes</b>.",
  "TRAIN", "PULL THE LEVER", "LEVER", "What should you pull?",
  "TRAIN rolls through safely and the rail yard gates open.", ["🚂", "🚦", "🛤️", "🔧"], "#1d1d22", "#3a3a40")
t("geometry/triangle-congruence", "Lockdown at the Robot Factory", "assembly bay", "🤖", "🦾🏆",
  "The robot factory's twin robots must be built exactly alike, and the bays won't open until you prove it. Prove triangles congruent to escape in <b>10 minutes</b>.",
  "ROBOT", "THE PASSWORD IS SPROCKET", "SPROCKET", "What is the password?",
  "ROBOT powers down the line and the factory gates open.", ["🤖", "🔩", "⚙️", "🦾"], "#1a2230", "#36465c")
t("geometry/triangle-relationships", "Starlight Observatory: Locked Under the Stars", "dome", "🔭", "🌌🏆",
  "The observatory dome locked during a meteor shower. Midsegments, bisectors and triangle inequalities unlock each dome in <b>10 minutes</b>.",
  "LUNAR", "THE STAR MAP IS HIDDEN IN THE TOWER", "TOWER", "Where is the star map?",
  "LUNAR rotates the dome open just in time to see the meteors.", ["🔭", "🌙", "⭐", "🛰️"], "#080b1f", "#1b1f40")
t("geometry/similarity", "The Shrink-Ray Workshop", "workshop", "🔬", "📏🏆",
  "An inventor's shrink ray scaled the workshop doors to the wrong size. Use similarity and scale factors to fix each workshop in <b>10 minutes</b>.",
  "MODEL", "THE PASSWORD IS ENLARGE", "ENLARGE", "What is the password?",
  "MODEL restores every door to full size and you walk right out.", ["🔬", "📏", "🧲", "🪛"], "#221d2e", "#403856")
t("geometry/right-triangles-trigonometry", "Rotor Rescue: Summit Mission", "ridge", "🚁", "⛰️🏆",
  "A hiker is stranded on the summit and the rescue helicopter needs exact angles and distances. Use the Pythagorean theorem and trig ratios to complete each leg in <b>10 minutes</b>.",
  "RIDGE", "THE PASSWORD IS BEACON", "BEACON", "What is the password?",
  "RIDGE guides the helicopter in and the hiker is safe.", ["🚁", "⛰️", "🧗", "🔦"], "#16233a", "#3a4a5e")
t("geometry/quadrilaterals-polygons", "Lockdown at the Tile Factory", "kiln", "🧱", "🔷🏆",
  "The tile factory's kilns sealed themselves mid-batch. Polygon angle sums and quadrilateral properties unlock each kiln in <b>10 minutes</b>.",
  "TILES", "THE TILE KEY IS UNDER THE TABLE", "TABLE", "Where is the tile key?",
  "TILES opens the last kiln and the factory floor clears.", ["🧱", "🔷", "🔶", "🧰"], "#2a1b14", "#4c3326")
t("geometry/transformations", "Glitch World: Trapped in the Game", "level", "🎮", "👾🏆",
  "A video game glitch pulled your team inside! Each level opens only with the right translation, reflection, rotation or dilation. Beat the game in <b>10 minutes</b>.",
  "PIXEL", "THE CODE IS WARPZONE", "WARPZONE", "What is the code?",
  "PIXEL completes the final level and you pop back into the classroom.", ["🎮", "👾", "🕹️", "⭐"], "#120d2a", "#2c2156")
t("geometry/circles", "Carnival After Dark: Locked In the Midway", "booth", "🎡", "🎠🏆",
  "The carnival's Ferris wheel stopped and every midway booth locked. Arcs, chords, tangents and circle equations unlock each booth in <b>10 minutes</b>.",
  "CLOWN", "THE TOP PRIZE IS A TEDDY", "TEDDY", "What is the top prize?",
  "CLOWN honks the horn and the midway gates swing open.", ["🎡", "🤡", "🎯", "🍭"], "#2a1030", "#4f2058")
t("geometry/area-surface-area-volume", "The Pharaoh's Pyramid: Sealed Inside", "tomb", "🔺", "🏺🏆",
  "The pyramid's stone doors slammed shut! Area, surface area and volume codes unlock each tomb. Escape in <b>10 minutes</b> before the torches burn out.",
  "MUMMY", "THE PASSWORD IS ANUBIS", "ANUBIS", "What is the password?",
  "MUMMY slides the final stone and desert sunlight pours in.", ["🔺", "🏺", "🐫", "🔥"], "#2b2110", "#55421f")

# ---------------- Algebra 2
t("algebra2/functions-transformations", "Mirror Maze Mayhem", "mirror room", "🪞", "🎭🏆",
  "The funhouse mirror maze shifts, stretches and flips every reflection. Each room opens with the right function transformation. Escape in <b>10 minutes</b>.",
  "GLASS", "THE PASSCODE IS FUNHOUSE", "FUNHOUSE", "What is the passcode?",
  "GLASS shatters the last illusion and the exit appears.", ["🪞", "🎭", "🎪", "🌀"], "#1f1236", "#3d2566")
t("algebra2/linear-functions-systems", "Blizzard at Summit Lodge", "cabin", "🏔️", "🫎🏆",
  "A blizzard snowed in the Summit Lodge and every cabin door froze. Linear functions and systems unlock each cabin in <b>10 minutes</b>.",
  "MOOSE", "THE LODGE CODE IS SNOWDRIFT", "SNOWDRIFT", "What is the lodge code?",
  "MOOSE thaws the final lock and the snowcat arrives to take you home.", ["🏔️", "🫎", "🔥", "☕"], "#14243a", "#e6edf5")
t("algebra2/quadratic-functions-complex-numbers", "Lockdown at Fountain Park", "fountain", "⛲", "🦦🏆",
  "Every fountain in the park shoots a perfect parabola, and the gates won't open until you understand them. Quadratics and complex numbers unlock each fountain in <b>10 minutes</b>.",
  "OTTER", "THE GATE CODE IS WATERLILY", "WATERLILY", "What is the gate code?",
  "OTTER opens the park gates and the fountains dance.", ["⛲", "🦦", "🌸", "🦆"], "#0f2a2e", "#22504f")
t("algebra2/polynomial-functions", "Roller Coaster Design Studio", "design bay", "🎢", "🏗️🏆",
  "The coaster designers locked their studio until every track curve is checked. End behavior, zeros and factors unlock each design bay in <b>10 minutes</b>.",
  "LOOPS", "THE BLUEPRINT IS UNDER THE DRAFTING LAMP", "LAMP", "Where is the blueprint?",
  "LOOPS approves the design and the studio doors open.", ["🎢", "📐", "🏗️", "💡"], "#1a1d33", "#363c63")
t("algebra2/radicals-rational-exponents", "The Crystal Cavern", "grotto", "💎", "🔮🏆",
  "Glowing crystals sealed the cavern grottos. Radicals and rational exponents unlock each grotto. Climb out in <b>10 minutes</b>.",
  "QUART", "THE ROPE IS BEHIND THE STALAGMITE", "STALAGMITE", "Where is the rope?",
  "QUART lights the crystals and a passage opens to the surface.", ["💎", "🔮", "🦇", "🔦"], "#151030", "#2e2559")
t("algebra2/exponential-logarithmic-functions", "Pressure Drop: Escape the Deep", "hatch", "🐋", "⚓🏆",
  "The deep-sea research base is losing pressure. Exponential and logarithmic codes unlock each hatch. Surface in <b>10 minutes</b>.",
  "WHALE", "THE PASSCODE IS ANCHOR", "ANCHOR", "What is the passcode?",
  "WHALE seals the last hatch and the base rises safely.", ["🐋", "🐙", "🫧", "⚓"], "#041d33", "#0b3653")
t("algebra2/rational-functions", "Air Traffic Control Tower", "radar room", "✈️", "🛬🏆",
  "Air traffic control lost power and planes are circling. Asymptotes, holes and rational equations unlock each radar room in <b>10 minutes</b>.",
  "RADAR", "THE BACKUP SWITCH IS BY THE WINDSOCK", "WINDSOCK", "Where is the backup switch?",
  "RADAR comes back online and every plane lands safely.", ["✈️", "🛬", "📡", "🎧"], "#121c30", "#2c3a55")
t("algebra2/sequences-series", "The Domino Mansion", "hall", "🁢", "🏰🏆",
  "Every hallway in the Domino Mansion is a chain reaction. Arithmetic and geometric sequences and series unlock each hall in <b>10 minutes</b>.",
  "CHAIN", "THE GRAND KEY IS ON THE STAIRCASE", "STAIRCASE", "Where is the grand key?",
  "CHAIN topples the final domino and the mansion doors open.", ["🁢", "🕯️", "🪜", "🗝️"], "#22191a", "#43302f")
t("algebra2/conic-sections", "Orbit Control Center", "console", "🪐", "☄️🏆",
  "Satellites are drifting off their elliptical paths. Circles, parabolas, ellipses and hyperbolas unlock each console in <b>10 minutes</b>.",
  "HALOS", "THE OVERRIDE IS NEXT TO THE TELESCOPE", "TELESCOPE", "Where is the override?",
  "HALOS locks every satellite back in orbit.", ["🪐", "🛰️", "☄️", "🔭"], "#070a1e", "#191d3d")
t("algebra2/trigonometric-functions", "Lighthouse on Wave Rock", "landing", "🗼", "🌊🏆",
  "The lighthouse beam has stopped turning and ships are heading for the rocks. Radians, the unit circle and sinusoids unlock each landing in <b>10 minutes</b>.",
  "WAVES", "THE LAMP KEY IS IN THE FOGHORN", "FOGHORN", "Where is the lamp key?",
  "WAVES restarts the beam and the ships turn safely away.", ["🗼", "🌊", "⛵", "🐚"], "#0b1c30", "#173452")
t("algebra2/probability-statistics", "Treasure Island: The Lucky Map", "cove", "🏝️", "💰🏆",
  "The pirate's treasure map only reveals the next cove to sailors who know their odds. Probability and statistics unlock each cove in <b>10 minutes</b>.",
  "CHEST", "X MARKS THE SPOT UNDER THE PALM", "PALM", "What tree marks the spot?",
  "CHEST springs open and gold coins spill onto the sand.", ["🏝️", "🗺️", "💰", "🦀"], "#0e2a33", "#d9c08a")

# ---------------- Precalculus
t("precalculus/equations-inequalities", "Supply Drop Logistics", "hangar", "📦", "🚚🏆",
  "A relief mission is stuck at the airfield until the cargo plan is optimized. Equations, inequalities and linear programming unlock each hangar in <b>10 minutes</b>.",
  "CARGO", "THE FLIGHT PLAN IS IN THE CONTROL TOWER", "CONTROL", "Where is the flight plan?",
  "CARGO loads perfectly and the relief plane takes off.", ["📦", "✈️", "🚚", "📋"], "#1c2230", "#3a4558")
t("precalculus/functions", "The Function Observatory", "wing", "🔭", "🌠🏆",
  "The observatory's wings lock whenever a function is misread. Composition, inverses, logs and asymptotes unlock each wing in <b>10 minutes</b>.",
  "OPTIC", "THE STAR CHART IS UNDER THE SEXTANT", "SEXTANT", "Where is the star chart?",
  "OPTIC opens the final wing and the night sky glows.", ["🔭", "🌠", "🧭", "📜"], "#0a0d26", "#1e2350")
t("precalculus/conics", "Whispering Gallery Heist", "vault", "🏛️", "💍🏆",
  "In the Whispering Gallery, a whisper at one focus is heard at the other. Circles, parabolas, ellipses and hyperbolas unlock each vault in <b>10 minutes</b>.",
  "FOCUS", "THE JEWEL CASE IS BEHIND THE ARCH", "ARCH", "Where is the jewel case?",
  "FOCUS unlocks the last vault and the jewel is returned to the museum.", ["🏛️", "💍", "🔦", "🗝️"], "#1f1a26", "#3d344c")
t("precalculus/trigonometric-functions", "Ferris Wheel Engineers", "gondola", "🎡", "🎆🏆",
  "The giant Ferris wheel stopped with riders at the top. Radians, exact values and sinusoids unlock each gondola in <b>10 minutes</b>.",
  "SPOKE", "THE RESTART BUTTON IS IN THE HUB", "HUB", "Where is the restart button?",
  "SPOKE restarts the wheel and fireworks light up the sky.", ["🎡", "🎆", "🎟️", "🍿"], "#160f2c", "#30215a")
t("precalculus/general-triangle-trigonometry", "Surveyors of the Canyon", "outpost", "🏜️", "🧭🏆",
  "A canyon survey team is cut off by a flash flood. Law of Sines, Law of Cosines and triangle area unlock each outpost in <b>10 minutes</b>.",
  "MESAS", "THE RADIO IS BEHIND THE CACTUS", "CACTUS", "Where is the radio?",
  "MESAS confirms the route and the rescue truck finds you.", ["🏜️", "🌵", "🧭", "📐"], "#3a2210", "#64401f")
t("precalculus/matrices", "Matrix Mainframe Shutdown", "server room", "🖥️", "💾🏆",
  "The mainframe locked every server room with matrix encryption. Matrix operations, determinants and inverses unlock each room in <b>10 minutes</b>.",
  "GRIDS", "THE ADMIN PASSWORD IS FIREWALL", "FIREWALL", "What is the admin password?",
  "GRIDS decrypts the mainframe and the system reboots.", ["🖥️", "💾", "🔌", "🧮"], "#0b1f16", "#16402c")
t("precalculus/vectors", "Sailing Regatta Rescue", "buoy", "⛵", "🏁🏆",
  "Wind and current pushed the regatta off course. Vectors, complex numbers and polar coordinates guide you past each buoy in <b>10 minutes</b>.",
  "SAILS", "THE TOW ROPE IS ON THE LIGHTHOUSE DOCK", "DOCK", "Where is the tow rope?",
  "SAILS catches the wind and your team crosses the finish line.", ["⛵", "🌬️", "🧭", "🏁"], "#0a2238", "#17405f")
t("precalculus/probability", "Casino Royale Science Night", "table", "🃏", "🎲🏆",
  "Science Night turned the gym into a probability casino, and the tables locked! Counting, binomial and normal probabilities unlock each table in <b>10 minutes</b>.",
  "DICEY", "THE CHIP RACK IS UNDER THE ROULETTE WHEEL", "ROULETTE", "Where is the chip rack?",
  "DICEY wins the last game and the gym doors swing open.", ["🃏", "🎲", "🪙", "🎯"], "#0f2a1a", "#1d4a2e")

# ---------------- Calculus
t("calculus/precalculus-review", "Base Camp Systems Check", "tent", "🏕️", "🥾🏆",
  "Before the big climb, base camp runs a systems check. Factoring, exponentials, logs and the unit circle unlock each tent in <b>10 minutes</b>.",
  "TRAIL", "THE TRAIL MAP IS UNDER THE LANTERN POST", "POST", "Where is the trail map?",
  "TRAIL clears the checklist and the expedition begins.", ["🏕️", "🥾", "🔥", "🗺️"], "#13261a", "#2d4b30")
t("calculus/limits-continuity", "The Infinite Hallway", "corridor", "♾️", "🚪🏆",
  "This hallway gets closer and closer to the exit but never quite arrives. Limits and continuity unlock each corridor in <b>10 minutes</b>.",
  "LIMIT", "THE TRUE EXIT IS BEHIND THE GRANDFATHER CLOCK", "GRANDFATHER", "Where is the true exit?",
  "LIMIT reaches the door at last and the hallway ends.", ["♾️", "🚪", "🕰️", "🕯️"], "#191726", "#353148")
t("calculus/derivatives", "Speed Trap Highway Patrol", "checkpoint", "🚓", "🏎️🏆",
  "The radar gun broke and every highway checkpoint is closed. Instantaneous rates, derivative rules and tangent lines unlock each checkpoint in <b>10 minutes</b>.",
  "RATES", "THE RADAR GUN IS IN THE GLOVE BOX", "GLOVE", "Where is the radar gun?",
  "RATES clears the last checkpoint and traffic flows again.", ["🚓", "🏎️", "🚦", "📡"], "#16161f", "#30303e")
t("calculus/applications-derivatives", "Rocket Launch Optimization", "launch bay", "🚀", "🌕🏆",
  "Mission control locked the launch bays until every trajectory is optimized. Related rates, extrema and motion unlock each bay in <b>10 minutes</b>.",
  "PEAKS", "THE FUEL VALVE IS BESIDE THE GANTRY", "GANTRY", "Where is the fuel valve?",
  "PEAKS sets the perfect trajectory and the rocket heads for the moon.", ["🚀", "🌕", "🛰️", "⛽"], "#090c22", "#1d2148")
t("calculus/antiderivatives-definite-integrals", "Reservoir Floodgate Control", "floodgate", "🌧️", "💧🏆",
  "Heavy rain is filling the reservoir. Riemann sums, antiderivatives and integral properties unlock each floodgate in <b>10 minutes</b>.",
  "AREAS", "THE GATE WHEEL IS NEAR THE SPILLWAY", "SPILLWAY", "Where is the gate wheel?",
  "AREAS balances the water and the town stays dry.", ["🌧️", "💧", "🌉", "🦆"], "#0c2033", "#1c3e58")
t("calculus/fundamental-theorem-calculus", "The Clockmaker's Workshop", "workbench", "⏱️", "🕰️🏆",
  "The clockmaker connected every gear to every other gear. The Fundamental Theorem and accumulation functions unlock each workbench in <b>10 minutes</b>.",
  "TICKS", "THE WINDING KEY IS IN THE CUCKOO CLOCK", "CUCKOO", "Where is the winding key?",
  "TICKS sets every clock right and the workshop door chimes open.", ["⏱️", "🕰️", "⚙️", "🔑"], "#231b12", "#463624")
t("calculus/applications-integrals", "Wind Farm Power Grid", "turbine", "🌬️", "⚡🏆",
  "The wind farm's grid shut down after a storm. Net change, area and volume unlock each turbine in <b>10 minutes</b>.",
  "POWER", "THE RESET SWITCH IS BY THE SUBSTATION", "SUBSTATION", "Where is the reset switch?",
  "POWER flows again and the town lights come back on.", ["🌬️", "⚡", "🔋", "🏭"], "#102231", "#21445a")
t("calculus/differential-equations", "Wildlife Population Reserve", "habitat", "🦌", "🌲🏆",
  "The reserve's population models crashed and every habitat gate locked. Slope fields, Euler's method and separable equations unlock each habitat in <b>10 minutes</b>.",
  "HERDS", "THE RANGER KEY IS AT THE WATERING HOLE", "WATERING", "Where is the ranger key?",
  "HERDS balances the model and the reserve gates open.", ["🦌", "🌲", "🐺", "🦉"], "#122a18", "#2a4a2c")
t("calculus/ap-review", "AP Exam Escape Marathon", "exam room", "📝", "🎓🏆",
  "The night before the AP exam, the review center locked its doors. Limits, derivatives, integrals and justifications unlock each exam room in <b>10 minutes</b>.",
  "GRADS", "THE ANSWER SHEET IS UNDER THE STOPWATCH", "STOPWATCH", "Where is the answer sheet?",
  "GRADS! You conquered the review and walk out ready for exam day.", ["📝", "🎓", "⏱️", "✏️"], "#1a1d2e", "#353a55")
