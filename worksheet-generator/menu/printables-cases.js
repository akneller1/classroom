/* Printable Generators: the Whodunnit cases. Each case has 6 suspects, 6 places and 6 methods.
   The generator picks the culprit, the place and the method for each printout, so the same case can be
   used again with a different answer. Clue text is filled in from these pieces:
   - an alibi clears one suspect AND one place: "<suspect> was <act> <place phrase> the whole time. <proof>"
   - a method clue clears one method: one of the method's `clear` sentences.
   Place `acts` read naturally after "was" and before the place, e.g. "was fixing a machine in" + "Pinball Alley". */
(function (G) {
  'use strict';
  var PR = G.MKMENU.printables = G.MKMENU.printables || {};
  PR.PROOFS = ['The security camera shows it.', 'Three people saw it.', 'A photo with a time stamp proves it.', 'Everyone there agrees.',
    'A sign-in sheet backs it up.', 'Two teachers confirmed it.', 'It is all on video.', 'The receipt has the time on it.'];
  PR.CASES = {
    museum: {
      name: 'The Missing Moonstone', item: 'the Moonstone', where: 'the Hall of Wonders Museum',
      intro: 'It was Family Night at <b>the Hall of Wonders Museum</b>. At 8:00 the lights flickered, and when they came back on, <b>the Moonstone</b>, a glowing blue gem the size of an egg, was gone from its glass case!',
      suspects: [{ n: 'Dr. Ada Finch', r: 'Head Curator' }, { n: 'Marco Bell', r: 'Night Guard' }, { n: 'Rosa Kim', r: 'Tour Guide' }, { n: 'Mr. Pike', r: 'Gift Shop Owner' }, { n: 'Nina Ford', r: 'Visiting Scientist' }, { n: 'Leo Grant', r: 'Lighting Tech' }],
      places: [{ n: 'Dinosaur Hall', a: 'giving a tour in' }, { n: 'Gift Shop', a: 'ringing up sales in the' }, { n: 'Planetarium', a: 'running the star show in the' }, { n: 'Mummy Room', a: 'cleaning the cases in the' }, { n: 'Café', a: 'serving hot cocoa in the' }, { n: 'Map Room', a: 'sorting old maps in the' }],
      methods: [{ n: 'Hidden in a hollow book', clear: ['Every book in the museum was checked. None of them were hollow.', 'The only hollow book was locked in the office, and it was empty.'] },
        { n: 'Dropped in a backpack', clear: ['Every backpack was searched at the exit. Only snacks and maps.', 'Backpacks were left at the coat check all night.'] },
        { n: 'Swapped with a fake', clear: ['The gem was NOT swapped: the case was empty, not holding a fake.', 'No fake gem was found anywhere in the museum.'] },
        { n: 'Lowered from a skylight', clear: ['The skylights were bolted shut and covered in dust.', 'A rope on the skylight would have set off the roof alarm. It stayed silent.'] },
        { n: 'Tucked in a coat pocket', clear: ['Coats were zipped in plastic bags at the coat check all night.', 'Every coat was checked twice. The pockets were empty.'] },
        { n: 'Rolled away in a mop bucket', clear: ['The mop buckets were locked in a closet all night.', 'The only mop bucket was full of water and nothing else.'] }]
    },
    bakesale: {
      name: 'The Great Cupcake Caper', item: 'the Golden Whisk trophy', where: 'Maple Middle School’s bake-off',
      intro: 'The annual <b>bake-off</b> at Maple Middle School was almost over. The judges turned around to taste the last pie, and <b>the Golden Whisk trophy</b> vanished from the prize table!',
      suspects: [{ n: 'Chef Rossi', r: 'Head Judge' }, { n: 'Mia Lopez', r: 'Student Baker' }, { n: 'Mr. Dunn', r: 'Custodian' }, { n: 'Kayla Brooks', r: 'Last Year’s Winner' }, { n: 'Coach Reed', r: 'Gym Teacher' }, { n: 'Omar Haddad', r: 'Student Reporter' }],
      places: [{ n: 'Kitchen', a: 'washing pans in the' }, { n: 'Gym', a: 'setting up tables in the' }, { n: 'Library', a: 'writing a story in the' }, { n: 'Hallway', a: 'hanging posters in the' }, { n: 'Cafeteria', a: 'slicing pies in the' }, { n: 'Front Office', a: 'counting raffle tickets in the' }],
      methods: [{ n: 'Hidden in a cake box', clear: ['Every cake box was opened by the judges. Only cake inside.', 'The cake boxes were too small to hold the trophy.'] },
        { n: 'Wrapped in an apron', clear: ['All the aprons were hanging on hooks the whole time.', 'The aprons were collected and washed before the theft.'] },
        { n: 'Slipped into a lunch bag', clear: ['Lunch bags were locked in the lockers all afternoon.', 'Every lunch bag was searched. No trophy.'] },
        { n: 'Carried on a cooling rack', clear: ['The cooling racks never left the kitchen counter.', 'Every cooling rack was covered in cookies, not trophies.'] },
        { n: 'Dropped in the recycling bin', clear: ['The recycling bins were emptied and checked. Only cans.', 'The recycling bins were outside, locked behind a gate.'] },
        { n: 'Pushed out on a cart', clear: ['The only cart had a flat tire and never moved.', 'The carts were chained together by the door.'] }]
    },
    sciencefair: {
      name: 'The Science Fair Sabotage', item: 'the blue-ribbon robot', where: 'the county science fair',
      intro: 'Judging day at <b>the county science fair</b>! Minutes before the awards, the crowd gasped: <b>the blue-ribbon robot</b>, built by the eighth grade, had rolled away from its table, and it was nowhere to be found!',
      suspects: [{ n: 'Dr. Patel', r: 'Lead Judge' }, { n: 'Sam Rivers', r: 'Rival Inventor' }, { n: 'Ms. Ortiz', r: 'Science Teacher' }, { n: 'Jake Moon', r: 'Volunteer' }, { n: 'Lily Chen', r: 'Robot Club President' }, { n: 'Mr. Gray', r: 'Building Manager' }],
      places: [{ n: 'Chemistry Lab', a: 'mixing solutions in the' }, { n: 'Auditorium', a: 'testing the microphones in the' }, { n: 'Greenhouse', a: 'watering plants in the' }, { n: 'Computer Lab', a: 'printing award certificates in the' }, { n: 'Loading Dock', a: 'unloading boxes at the' }, { n: 'Snack Table', a: 'handing out water at the' }],
      methods: [{ n: 'Hidden under a lab coat', clear: ['Every lab coat was hanging on its hook all day.', 'The lab coats were far too thin to hide a robot.'] },
        { n: 'Packed in a poster tube', clear: ['The robot was much too wide to fit in a poster tube.', 'Every poster tube held only rolled-up posters.'] },
        { n: 'Driven by remote control', clear: ['The robot’s remote was locked in the judges’ box the whole time.', 'The robot’s battery was dead. It could not drive anywhere.'] },
        { n: 'Stacked in a box of cables', clear: ['The cable boxes were taped shut all day.', 'Every cable box was checked. Only wires inside.'] },
        { n: 'Wheeled out in a trash can', clear: ['The trash cans were emptied at noon, before the theft.', 'The trash cans were bolted to the floor.'] },
        { n: 'Covered with a tablecloth', clear: ['All the tablecloths were on the tables when the robot went missing.', 'The tablecloths were too short to hide a robot.'] }]
    },
    zoo: {
      name: 'The Zoo Parade Puzzle', item: 'the parade crown', where: 'Sunnyside Zoo',
      intro: 'The Spring Parade at <b>Sunnyside Zoo</b> was about to start. The zookeeper opened the treasure chest for the parade crown, but <b>the parade crown</b> was gone, and the band was already marching!',
      suspects: [{ n: 'Keeper Lou', r: 'Elephant Keeper' }, { n: 'Dr. Sato', r: 'Zoo Vet' }, { n: 'Tina Marsh', r: 'Parade Leader' }, { n: 'Ben Ruiz', r: 'Ice Cream Seller' }, { n: 'Grace Hall', r: 'Bird Trainer' }, { n: 'Mr. Webb', r: 'Gate Keeper' }],
      places: [{ n: 'Penguin Pool', a: 'feeding fish to the birds at the' }, { n: 'Reptile House', a: 'checking the lights in the' }, { n: 'Petting Barn', a: 'brushing goats in the' }, { n: 'Gift Stand', a: 'selling stuffed animals at the' }, { n: 'Monkey Island', a: 'counting monkeys at' }, { n: 'Main Gate', a: 'taking tickets at the' }],
      methods: [{ n: 'Hidden in a hay bale', clear: ['The hay bales were delivered after the crown went missing.', 'Every hay bale was pulled apart. Only hay.'] },
        { n: 'Stuffed in a balloon bag', clear: ['The balloon bags were all handed out to kids before noon.', 'The balloon bags were see-through. No crown inside.'] },
        { n: 'Dropped in a feed bucket', clear: ['The feed buckets were full of fish all morning.', 'Every feed bucket was checked by the vet.'] },
        { n: 'Carried in a stroller', clear: ['No strollers were allowed past the parade gate.', 'Every stroller was searched. Only sleepy babies.'] },
        { n: 'Tied to a kite', clear: ['There was no wind at all: no kites flew.', 'The only kite was stuck in a tree all day.'] },
        { n: 'Packed in a cooler', clear: ['The coolers were full of ice cream bars, not crowns.', 'The coolers were locked in the ice cream truck.'] }]
    },
    theater: {
      name: 'The Opening Night Mystery', item: 'the lead actor’s golden mask', where: 'the Spotlight Theater',
      intro: 'It was opening night at <b>the Spotlight Theater</b>. Five minutes before the curtain went up, the stage manager screamed: <b>the golden mask</b> for the lead role was missing from the prop table!',
      suspects: [{ n: 'Ms. Lane', r: 'Director' }, { n: 'Theo Park', r: 'Lead Actor' }, { n: 'Ruby Shaw', r: 'Understudy' }, { n: 'Mr. Vance', r: 'Set Builder' }, { n: 'Ivy Cole', r: 'Costume Designer' }, { n: 'Dev Shah', r: 'Sound Tech' }],
      places: [{ n: 'Dressing Room', a: 'doing makeup in the' }, { n: 'Sound Booth', a: 'testing the speakers in the' }, { n: 'Lobby', a: 'greeting guests in the' }, { n: 'Costume Shop', a: 'sewing buttons in the' }, { n: 'Stage', a: 'sweeping the' }, { n: 'Basement', a: 'painting scenery in the' }],
      methods: [{ n: 'Hidden in a hat box', clear: ['The hat boxes were open on a shelf. Only hats.', 'Every hat box was checked by the director.'] },
        { n: 'Slipped into a costume', clear: ['The costumes were zipped in bags all night.', 'Every costume was shaken out. No mask.'] },
        { n: 'Dropped through a trapdoor', clear: ['The trapdoor was nailed shut for repairs.', 'The trapdoor squeaks loudly, and nobody heard it.'] },
        { n: 'Carried in a flower bouquet', clear: ['The flowers were delivered after the mask went missing.', 'The bouquets were wrapped in clear plastic.'] },
        { n: 'Hidden in a prop chest', clear: ['The prop chest was locked, and the key was in the safe.', 'The prop chest was searched first. Empty.'] },
        { n: 'Rolled in a curtain', clear: ['The curtains never came down all night.', 'The spare curtain was folded flat in a closet.'] }]
    },
    spacecamp: {
      name: 'The Space Camp Snatch', item: 'the meteorite', where: 'Starlight Space Camp',
      intro: 'On the last night of <b>Starlight Space Camp</b>, the campers came back from stargazing to find the display case empty. <b>The meteorite</b>, a real rock from space, was gone!',
      suspects: [{ n: 'Commander Ray', r: 'Camp Director' }, { n: 'Ella Stone', r: 'Camp Counselor' }, { n: 'Dr. Huang', r: 'Astronomer' }, { n: 'Pete Lyle', r: 'Camp Cook' }, { n: 'Ana Silva', r: 'Rocket Club Leader' }, { n: 'Max Young', r: 'Camper' }],
      places: [{ n: 'Launch Pad', a: 'setting up rockets at the' }, { n: 'Mess Hall', a: 'cooking dinner in the' }, { n: 'Observatory', a: 'aiming the telescope in the' }, { n: 'Cabins', a: 'checking beds in the' }, { n: 'Training Room', a: 'running the spin chair in the' }, { n: 'Campfire', a: 'telling stories at the' }],
      methods: [{ n: 'Hidden in a space helmet', clear: ['The space helmets were hanging on hooks, and every one was empty.', 'The helmets were locked in a cage all night.'] },
        { n: 'Packed in a sleeping bag', clear: ['The sleeping bags were rolled tight and tied. No meteorite.', 'Every sleeping bag was shaken out.'] },
        { n: 'Launched in a rocket', clear: ['The model rockets were too small to carry a rock.', 'No rockets were launched that night.'] },
        { n: 'Buried in the sandbox', clear: ['The sandbox was raked smooth. Nothing was buried.', 'The sandbox was covered with a tarp all night.'] },
        { n: 'Dropped in a soup pot', clear: ['The soup pots were full of chili all night.', 'Every soup pot was washed and empty.'] },
        { n: 'Tucked in a backpack', clear: ['All backpacks were on the bus during stargazing.', 'Every backpack was searched. Only flashlights.'] }]
    }
  };
})(typeof window !== 'undefined' ? window : globalThis);
