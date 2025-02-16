# Rain World

## Where is the options page?

The [player options page for this game](../player-options) contains all the options you need to configure and export a
config file.

## What is the win condition?

The default goal is ascension.
Logically, this requires raising max karma to 10 and gain access to Subterranean.
The win condition is met upon entering the Void Sea itself.
If More Slugcats Expansion is enabled,
the option for alternate victory conditions is available for most Slugcats.

## What does randomization do to Rain World?

### Karma and Echoes
Initial max karma is 1 by default, regardless of Slugcat.
Raising max karma requires finding karma cap increases in the item pool rather than meeting echoes.
Meeting echoes still requires a certain karma level depending on current max
and is not possible with less than 5 karma -
except for Artificer and Saint, who can see echoes by being at max karma with karma reinforcement.
There are at least 8 karma cap increases
(one increase is worth 2 as max karma jumps from 5 to 7),
though more may be added through the settings.

### Gates
Karma gates, in addition to requiring karma, require a key unique to each gate
which is added to the item pool.
Currently collected keys are displayed on the pause screen in-game.

### Passages
Completing a passage is a check.
Passage tokens are added to the item pool, rather than being awarded by completing passages.

### The Mark of Communication
The Mark of Communication is added to the item pool.
Five Pebbles does not automatically give the Mark to Monk, Survivor, Gourmand, or Artificer,
and Looks to the Moon does not automatically give Spearmaster the Mark.
Hunter and Rivulet do not start with the Mark.
The Mark is still required to make progress on The Scholar,
and certain alternate victory conditions require the Mark.

### Neuron Glow
Neuron glow is added to the item pool.
Eating a neuron fly may or may not grant the glow.

### Story flags
Story flags are added to the item pool:
- Hunter does not start with the green neuron.
- Artificer does not start with the citizen ID drone.
- The rarefaction cell is not found in the heart of The Rot.
- Spearmaster does not receive their pearl by meeting Five Pebbles.
- Spearmaster's pearl does not get rewritten by meeting Looks to the Moon with the pearl.

## Is the Archipelago mod compatible with other mods or DLC?

- **More Slugcats Expansion** (Downpour): 
Tokens, regions, and passages added are fully supported.
**Make sure you set the DLC setting correctly in your YAML!**

- **Room Randomizer**: Partially compatible.
As long as Room Randomizer is set to ensure that all gates are accessible,
the game should remain logically completable.

- **Enemy Randomizer**: Conditionally compatibile.
Certain checks, such as _The Dragon Slayer_ and the food quest,
assume that certain creatures will appear in certain regions.
Disabling these checks entirely is reccomended if using Enemy Randomizer.

- **Expedition** (Downpour): Unsupported.
Archipelago mode is not designed to work with Expedition mode.
Just having Expedition enabled is fine, though.

## What checks (locations) are added to the pool?

Randomization adds the following checks to the pool:
- **Unlock tokens** (the small holograms on stalks which normally unlock things for Arena or Story):
Touching an unlock token is a check.
While randomized, these tokens are collectable
even if you've already collected them on the current save file.
The unlock tokens introduced by MSC are also supported.

- **Colored pearls**:
Bringing a colored pearl to a shelter for the first time is a check.
Though the Mark of Communication is required for the pearls to make progress towards The Scholar,
it is not necessary for the checks.

- **Echoes**:
Each Echo is its own check.
Whether an echo appears still depends on karma and possibly on karma reinforcement.
You do not need the Mark of Communication to check an Echo.

- **Passages**:
Completing a Passage is a check.
Note that which Passages are logically possible depends on
whether you enabled `Passage progress without Survivor` in the YAML.
_The Wanderer_ additionally awards a check for each pip (each region hibernated in).

- **Food quest**:
If enabled, every point toward the food quest is a check.
The food quest can be made to appear even if not playing Gourmand's campaign.
Food quest points that cannot be earned by the selected Slugcat are never logically required
(e.g., Survivor will never need to earn the Yellow Lizard food quest pip).
Food quest checks require MSC to be enabled.

See [the checks subpage](/tutorial/Rain%20World/checks/en) for more details.

## What items are added to the pool?

### Unique
Randomization adds the following _unique items_ to the pool,
meaning that these items will not necessarily appear in their normal locations.
For instance, echoes do not necessarily increase karma,
and completing a passage does not necessarily award a token.
- Karma cap increase (at least 8)
- "Keys" for each region (except the starting region)
- Passage tokens
- The Mark of Communication
- The neuron glow
- (MSC) Artificer's citizen ID drone

### Filler
Randomization adds the following _filler items_ to the pool:
- Several vanilla weapons
(rocks, spears, explosive spears, grenades, flashbangs, sporepuffs, and cherrybombs)
- Several vanilla foods
(blue fruit, bubble fruit, eggbug eggs, jellyfish, mushrooms, slime mold)
- Several MSC weapons, if enabled (electric spears, lilypucks, singularity bombs)
- Several MSC foods, if enabled (firebug eggs, glow weed, gooieducks)

### Traps
Randomization adds the following _trap items_ to the pool.
Although they are "traps," many of them can be exploited for personal gain (or are neutral).
The only thing that all traps have in common is that they affect the game world instantly.
- **Stun**: Slugcat is briefly stunned.
- **Creature**: a dangerous creature spawns in an adjacent room.
This may be a Red Lizard, Red Centipede, Spitter Spider, any type of Vulture, or an Elite Scavenger.
The creature is immediately aware of Slugcat's position.
- **Timer**: the current cycle timer is shortened.
- (UNIMPLEMENTED) **Rain**: rain starts and quickly becomes deadly to anything directly exposed.
The rain ends after some time.
- (UNIMPLEMENTED) **Gravity**: Slugcat's personal gravity is reduced, possibly to zero.
Their gravity returns to normal after some time.
- **Zoomies**: Slugcat and/or creatures around them suddenly start moving much faster.
The effect wears off after entering a pipe.
- (UNIMPLEMENTED) **Fog**: a thick fog obscures view.  The fog wears off after some time.
- (UNIMPLEMENTED) **Darkness**: the world is suddenly enveloped in darkness like that of the Shaded Citadel.
The light returns after some time.
- (UNIMPLEMENTED) **Blizzard**: a severe blizzard suddenly starts.
Exposed creatures may be pushed around by the wind and suffer hypothermia.
The blizzard ends after a long time.
- (UNIMPLEMENTED) **Warp**: Slugcat is suddenly warped to another room in the current region.
- (UNIMPLEMENTED) **Kill squad**: a Scavenger kill squad is sent after Slugcat.
- (UNIMPLEMENTED) **Alarm**: every creature in the region is made aware of Slugcat's position.

