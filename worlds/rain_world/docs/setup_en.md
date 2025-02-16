# Rain World Setup Guide

## 0. Add the Rain World APWorld

The APWorld for Rain World is self-contained in `worlds/rain_world`.
You can either clone this fork or copy `worlds/rain_world`
to an existing Archipelago source.

## 1. Create a YAML settings file
### What is a YAML and why do I need one?
You can see the [basic multiworld setup guide](/tutorial/Archipelago/setup/en) here on the Archipelago website to learn 
about why Archipelago uses YAML files and what they're for.

### Where do I get a YAML?
You can use the [game options page](/games/Risk%20of%20Rain%202/player-options) here on the Archipelago 
website to generate a YAML using a graphical interface.
You can also edit this file directly if you understand the format.

## 2. Enable the Randomizer mod

Install the Archipelago build of the Randomizer mod from GitHub:
https://github.com/SaltiestSyrup/RWRandomizer/releases/tag/v1.1.0-ap_alpha

Once enabled, the Randomizer mod should have a Remix menu interface with an `Archipelago` tab
where a connection to an Archipelago room may be established.
If this Remix menu interface appears, the mod is loaded correctly.

## 3. Set Remix and mod settings

The `Passage progress without Survivor` setting in the YAML
must match the setting you use in the Rain World Remix options in-game.
For all other Rain World Remix settings, the choice is yours.

If you select a More Slugcats (MSC) gamestate in your YAML, MSC must also be enabled in-game.

## 4. Join an Archipelago room

When the Archipelago room is open, the Randomizer mod Remix menu interface 
may be used to connect to a room.
The name entered here must exactly match the name specified in the YAML.

A message should be returned indicating a successful connection.
At that point, you can start a Story campaign to begin.

The client will remain connected if you go back out to the main menu or any other menu.
It may not remain connected if you close or hot-reload the game (e.g., via Rain Reloader),
or if the host address or port number changes.

For details on everything that gets randomized,
see the [game description page](en_Rain%20World.md).