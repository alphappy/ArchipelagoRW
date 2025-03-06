def apply_hardcoded_exceptions(data: dict):
    for dlcstate, dlcstate_data in data.items():
        for region, region_data in dlcstate_data.items():
            for room, room_data in region_data.items():
                for objtype, obj_data in room_data.get("objects", {}).items():

                    # Karma flowers do not spawn for hunter.
                    if objtype == "KarmaFlower":
                        obj_data.setdefault("filter", {"Red"}).update({"Red"})

    # This token is not reasonably accessible for Artificer or at all for Sofanthiel.
    data["MSC"]["GW"]["GW_C09"]["shinies"]["BrotherLongLegs"]["filter"].update({"Artificer", "Inv"})
    data["MSC"]["GW"]["GW_C09"]["shinies"]["BrotherLongLegs"]["whitelist"].difference_update({"Artificer", "Inv"})

    data["MSC"]["GW"]["GW_A14"]["shinies"]["RedLizard"]["filter"].update({"Inv"})
    data["MSC"]["GW"]["GW_A14"]["shinies"]["RedLizard"]["whitelist"].difference_update({"Inv"})

    # These require a jetfish jump or similar (and in the LM version they're entirely behind a wall).
    del data["MSC"]["LM"]["LM_E02"]["objects"]["Hazer"]
    del data["MSC"]["SL"]["SL_E02"]["objects"]["Hazer"]
