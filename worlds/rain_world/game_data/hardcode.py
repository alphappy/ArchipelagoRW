def apply_hardcoded_exceptions(data: dict):
    for gameversion, gameversion_data in data.items():
        for dlcstate, dlcstate_data in gameversion_data.items():
            for region, region_data in dlcstate_data.items():
                for room, room_data in region_data.items():
                    for objtype, obj_data in room_data.get("objects", {}).items():

                        # Karma flowers do not spawn for hunter.
                        if objtype == "KarmaFlower":
                            obj_data.setdefault("filter", {"Red"}).update({"Red"})

                # `room_to_region` needs all the `OFFSCREEN`s to be different
                if offscreen_data := region_data.get("OFFSCREEN", {}):
                    region_data[f"{region}_OFFSCREEN"] = offscreen_data
                    del region_data["OFFSCREEN"]

            if "MSC" in dlcstate:
                # This token is not reasonably accessible for Artificer or at all for Sofanthiel.
                dlcstate_data["GW"]["GW_C09"]["shinies"]["BrotherLongLegs"]["filter"].update({"Artificer", "Inv"})
                dlcstate_data["GW"]["GW_C09"]["shinies"]["BrotherLongLegs"]["whitelist"].difference_update({"Artificer", "Inv"})

                dlcstate_data["GW"]["GW_A14"]["shinies"]["RedLizard"]["filter"].update({"Inv"})
                dlcstate_data["GW"]["GW_A14"]["shinies"]["RedLizard"]["whitelist"].difference_update({"Inv"})

                # These require a jetfish jump or similar (and in the LM version they're entirely behind a wall).
                del dlcstate_data["LM"]["LM_E02"]["objects"]["Hazer"]
                del dlcstate_data["SL"]["SL_E02"]["objects"]["Hazer"]

                # This token is ridiculous to get as Spearmaster.
                dlcstate_data["LM"]["LM_LEGENTRANCE"]["shinies"]["LM"]["filter"].update({"Spear"})
