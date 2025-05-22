# Watcher-specific notes

Any documentation details that are specific to The Watcher are detailed here.

## This necessarily contains major spoilers!

## Everything here is preliminary and subject to change!

## General
### Terminology
A few pieces of terminology are used in this documentation for brevity:
* **BWP region**:  A bad warp pool region - one of Corrupted Factories, Crumbling Fringes, Decaying Tunnels, or Infested Wastes.
* **Permarotted region**: Any BWP region, plus Unfortunate Evolution and Outer Rim.
* **Unrottable region**: Any of Shattered Terrace, Ancient Urban, or Daemon.
* **Normal region**: Any region that isn't permarotted or unrottable.

### Start in Watcherspace
A Watcher world always starts in Watcherspace (that is, not on the Five Pebbles facility grounds).
Max Ripple starts at 1, as if all three of the first Spinning Tops have already been encountered,
which means the ability to camouflage is already unlocked.
(UNIMPLEMENTED) 
By default, the starting region is one of the three original starting regions -
Coral Caves, Sunlit Port, or Torrential Railways -
but this can be changed by the `random_starting_region` player YAML setting.
Any Five Pebbles facility grounds regions are invalid values for this setting.

## Items
### Keys
As with karma gates, most warp points have a key which is required to use it.
There are several exceptions which do not require keys:
* All dynamic warp points, including the semi-permanent ones created in The Throne.
* All warps leaving a rotted Five Pebbles facility grounds region.
* The warp from Daemon to Shattered Terrace.

Spinning Top warps also have keys (except for the encounter in the rotted regions).
Spinning Top does not appear if the key is not collected.

### Ripple
Twelve progressive Ripple items are placed in the pool rather than being awarded by visiting Spinning Top.
Initially, Ripple is restricted to 1 (as with Karma for unmodded Artificer).
The first four Ripple items increase the maximum Ripple by one stage;
after all four are collected, current Ripple may lie between 1 and 5.
The next four Ripple items increase both the minimum and maximum by one stage;
after eight total are collected, current Ripple may lie between 5 and 9.
At this point, it is possible to enter ripplespace.
The final four Ripple items increase the minimum by one stage,
after which current Ripple is fixed at 9.

Effects which are tied to current Ripple, such as the behavior of the camouflage ability
and the creation of Ripple spawn, are still tied to current Ripple.

## Checks

Most of Watcher's checks fall into one of a few categories.
See [the naming subpage](/tutorial/Rain%20World/naming/en) for naming of checks not unique to Watcher.

| Check type         | Count | Naming                                                                                                                          |
|--------------------|------:|---------------------------------------------------------------------------------------------------------------------------------|
| Fixed warp point   |    78 | `REGION - Warp Point - ROOM_NAME`                                                                                               |
| Fixed Karma Flower |    76 | `REGION - Karma Flower - ROOM_NAME`                                                                                             |
| Throne warp point  |     4 | (UNIMPLEMENTED) `Outer Rim - Throne Warp - LOC` where `LOC` is either `upper west`, `lower west`, `upper east`, or `lower east` |
| Spinning Top       |    14 | `REGION - Spinning Top`                                                                                                         |
| Spread the Rot     |    18 | `REGION - Spread the Rot`                                                                                                       |
| The Prince         |    6? | (UNIMPLEMENTED) `Outer Rim - The Prince - NTH encounter` where `NTH` is `first`, `second`, etc.                                 |

### Fixed warp points
Visting a warp point, which puts it on the map, is a check.
A pair of two-way warp points is two separate checks.
The check is earned even if the warp is not currently usable
(e.g., cannot enter ripplespace or don't have the key).

### Fixed Karma Flowers
If `checks_karma_flowers` is enabled, each fixed Karma Flower spawn is a check.
The check is earned by grabbing the Karma Flower.

### Throne warp points
(UNIMPLEMENTED) 
Creating a semipermanent warp point in The Throne is a check.

### Spinning Top
Visiting Spinning Top in a _normal_ region is a check.
By default, Spinning Top does not appear if the key corresponding to the warp point is not collected
(but this behavior may be changed with the `spinning_top_keys` player YAML setting).
In that case, the check cannot be earned without the key.

All Spinning Top checks are immediately released when the `WAUA_BATH` Spinning Top is visited,
even if `which_victory_condition` is `ascension`,
since Spinning Top no longer appears after they ascend.

### Spread the Rot
Spreading the Rot to a new region is a check.
The check is earned upon hibernation if the region is sufficiently infected.
By default (see `checks_spread_rot`), these checks are only generated for the `alternate` victory condition.

### The Prince
(UNIMPLEMENTED) 
Each unique encounter with The Prince is a check.
These checks are awarded upon visiting the top-left-most screen where The Prince is (or will be).

### Other
* (UNIMPLEMENTED) Watcher can earn some passages.
Watcher cannot earn The Pilgrim, The Nomad, The Scholar, The Wanderer, or The Mother.
* (UNIMPLEMENTED) If `sheltersanity` is enabled, every shelter is a check when visited.
* (UNIMPLEMENTED) If `checks_food_quest` is enabled, Watcher can earn certain food quest checks.

## Settings

### Karma Flower checks
`checks_karma_flowers` controls whether fixed Karma Flowers are checks.
Enabling this is strongly reccomended as otherwise Watcher has relatively few checks.

### Rot spread checks
`checks_spread_rot` controls whether spreading the Rot to a new region is a check.
Its default setting, `alternate_only`, only generates the checks if `which_victory_condition` is `alternate`.

### Victory condition
The `ascension` victory condition is the Toys/Driedel/Spinning Top ending.
Logically, this just requires access to Ancient Urban.
This in turn requires access to Shattered Terrace (possibly, but not necessarily, through Daemon)
and the ability to shift into ripplespace,
which in turn requires at least 8 Ripple items (but see `logic_ripplespace_min_req` below).

The `alternate` victory condition is the Sentient Rot ending.
This requires awakening The Prince, which in turn requires 8 Ripple items
and several visits to Outer Rim, creating all four Throne warps in the process,
and spreading sentient rot to all 18 infectable regions (but see `rotted_region_target` below).

With the `alternate` victory condition enabled, meeting Spinning Top in Ancient Urban
will release all progressive Spinning Top checks immediately.

### Ripplespace minimum Ripple requirement
`logic_ripplespace_min_req` controls the number of Ripple items required for Ripplespace to be logically accessible.
The true access requirement for Ripplespace is having a *maximum* Ripple of 9.
This requires 8 Ripple items, which would raise *minimum* Ripple to 5.
This is the logical behavior if `logic_ripplespace_min_req` is set to `5` (its default).
Setting it to anything higher ensures that more Ripple items are logically required to enter Ripplespace,
reducing difficulty in maintaining the Ripple necessary to enter Ripplespace.
If set to `9`, 12 Ripple items must be in logic so that minimum Ripple may be raised to 9
before entering Ripplespace is required.

This setting may affect logic even if `which_victory_condition` is `alternate`,
since reaching the Spinning Top in Ancient Urban still releases all other Spinning Top checks.

### Rotted region target
`rotted_region_target` controls the number of regions that must be rotted to trigger the Sentient Rot ending.
The default, unaltered behavior is all 18 infectable regions.
This has no effect if `which_victory_condition` is `ascension`.

### Spinning Top keys
`spinning_top_keys` controls whether each Spinning Top location requires a key as most warp points do.
If enabled and the key has not been collected, Spinning Top will not appear and the warp will not be usable.
If disabled, Spinning Top always appears and the associated warp does not require a key.

### Rotted generation
`logic_rotted_generation` controls the generation and connectivity of BWP regions.
It only affects logic and the check pool.

| Value            | BWP regions have checks? | BWP connections might be part of logic? |
|------------------|--------------------------|-----------------------------------------|
| `none` (default) | No                       | No                                      |
| `passthrough`    | No                       | Yes                                     |
| `full`           | Yes                      | Yes                                     |

If set to `none`, the only way to logically access Outer Rim is through Unfortunate Evolution.
If set to `passthrough` or `full`, logic may draw the victory path through a BWP region,
though this requires the Outer Rim to Daemon warp key.

### Dynamic warp behavior
There are two settings which affect the behavior of normal dynamic warps (`normal_dynamic_warp_behavior`)
and of the semipermanent dynamic warps created in The Throne (`throne_dynamic_warp_behavior`).
Both settings have similar possible values and similar effects.
Their defaults are `visited` and `predetermined`, respectively.

Some values for the `normal_dynamic_warp_behavior` setting
can be further adjusted customized by adjusting `dynamic_warp_pool_size`.
This defaults to 18 (all normal regions).
It has no effect on Throne dynamic warps.

| Setting                                       | Effect                                                                                                                                                                                                                                                                                                                                                                                                |
|-----------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| `ignored` <sup>o</sup>                        | Targetting behavior is unaltered.  Logic assumes dynamic warps are impossible, but this means they can easily take the player out of logic.                                                                                                                                                                                                                                                           |
| `visited` <sup>o</sup>                        | Dynamic warps can only target already-visited regions and are thus logically irrelevant.                                                                                                                                                                                                                                                                                                              |
| `predetermined`                               | For normal warps, each region is tied to a predetermined target in another region.  For Throne warps, each of the four warp rooms is tied to a predetermined target, and the Ripple requirement depends only on which Throne warp it is rather than the Ripple requirement of the target.                                                                                                             |
| `predetermined_unlockable_source` <sup>n/sup> | Like `predetermined`, but each region additionally needs an item to unlock the ability to dynamic warp _from_ it.                                                                                                                                                                                                                                                                                     |
| `static_target_pool` <sup>n</sup>             | A static pool<sup>p</sup> of possible normal warp targets is decided by the randomizer.  Regions not in this pool can never be the target of a dynamic warp.  Targets still have Ripple requirements that must be met to be eligible.  If the pool size is set to 18 - all normal regions - this most closely reflects the actual game logic, but requires dealing with the randomness of targetting. |
| `unlockable_target_pool` <sup>n</sup>         | A static pool<sup>p</sup> of possible normal warp targets is decided by the randomizer.  Each region requires collecting an item to unlock it as an eligible warp target.  With none of these items collected, dynamic warps are not possible.                                                                                                                                                        |

- <sup>n</sup> This value is only valid for `normal_dynamic_warp_behavior`.
- <sup>o</sup> This value takes dynamic warps out of logic,
so they will never be required to reach the victory condition.
- <sup>p</sup> The number of regions in this pool is controlled by `dynamic_warp_pool_size`.

### Dynamic warp ripple requirement
(UNIMPLEMENTED) 
`dynamic_warp_ripple_requirement` dictates how the Ripple requirements for dynamic warp targets are handled.
This only affects normal dynamic warps.

| Value       | Effect                                                                |
|-------------|-----------------------------------------------------------------------|
| `unaltered` | Unaltered.  Each target has some Ripple requirement that must be met. |
| `none`      | Each target has no Ripple requirement.                                |