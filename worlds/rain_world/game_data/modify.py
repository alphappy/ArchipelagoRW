from dataclasses import dataclass
import re

MODIFY_FP = r'C:\Program Files (x86)\Steam\steamapps\common\Rain World\RainWorld_Data\StreamingAssets\mods\moreslugcats\modify\world\sb-rooms\sb_a09_settings.txt'
TARGET_FP = r'C:\Program Files (x86)\Steam\steamapps\common\Rain World\RainWorld_Data\StreamingAssets\world\sb-rooms\sb_a09_settings.txt'


@dataclass
class ReplaceOperation:
    find_kind: str
    find_text: str
    find_line: int
    find_line_number: int = -1
    replace_type: str = "REPLACE"
    replace_with: str = ""
    occurence: int = 0
    occurences_seen: int = 0


class Modification:
    def __init__(self, fp: str):
        self.source_fp: str = fp
        self.append_lines: list[str] = []
        self.insert_lines: dict[int, list[str]] = {}
        self.merge_lines: list[str] = []
        self.replacements: list[ReplaceOperation] = []

        self.collect()

    def collect(self):
        """See `ModManager.ModMerger.PendingApply.CollectModifications`."""
        find_text, find_kind = None, None
        i1, find_line, in_merge_block = -1, False, False
        input_lines = open(self.source_fp).readlines()

        for line in input_lines:
            line = line.strip()
            try:
                instruction, operand = line[1:].split("]", 1)
            except ValueError:
                # Line does not have `]`, making it invalid; this is part of the check on line 172.
                continue

            if in_merge_block:  # line 25
                if "[ENDMERGE]" in line:
                    in_merge_block = False
                self.merge_lines.append(line.replace("[ENDMERGE]", ""))

            elif line.startswith("[MERGE]"):  # line 39
                in_merge_block = True
                if len(s := line[7:].strip()) > 0:  # CRLF check?  line 46
                    self.merge_lines.append(s)

            elif line.startswith("[ADD]"):  # line 52
                self.append_lines.append(line[5:])  # CRLF check?  line 54

            elif line.startswith("[ADD_") and "]" in line:  # line 56
                try:
                    target_line, operand = line[5:].split("]")
                    target_line = int(target_line)
                    self.insert_lines.setdefault(target_line, []).append(operand)
                except ValueError:
                    pass

            elif instruction.startswith("FIND"):  # lines 68 - 121
                find_kind, find_text, i1 = instruction[4:].replace("LINE", "") or "NORMAL", operand, -1

            # elif line.startswith("[FIND]"):  # line 68
            #     find_substring, find_start, find_end, find_regex, i1, find_line = line[6:], None, None, None, -1, False
            #
            # elif line.startswith("[FINDLINE]"):  # line 77
            #     find_substring, find_start, find_end, find_regex, i1, find_line = line[10:], None, None, None, -1, True
            #
            # elif line.startswith("[FINDREGEX]"):  # line 86
            #     find_substring, find_start, find_end, find_regex, i1, find_line = None, None, None, line[11:], -1, False
            #
            # elif line.startswith("[FINDLINEREGEX]"):  # line 95
            #     find_substring, find_start, find_end, find_regex, i1, find_line = None, None, None, line[15:], -1, True
            #
            # elif line.startswith("[FINDLINESTART]"):  # line 104
            #     find_substring, find_start, find_end, find_regex, i1, find_line = None, line[15:], None, None, -1, True
            #
            # elif line.startswith("[FINDLINEEND]"):  # line 113
            #     find_substring, find_start, find_end, find_regex, i1, find_line = None, None, line[13:], None, -1, True

            elif line.startswith("[TARGETLINE]"):  # line 122
                try:
                    i1 = int(line[12:])
                    if i1 > 0:
                        find_kind, find_text = None, None
                    else:
                        i1 = -1
                except ValueError:
                    i1 = -1

            # line 144
            elif (instruction in ("REPLACE", "ADDBEFORE", "ADDAFTER")) and (find_text is not None or i1 > 0):
                self.replacements.append(ReplaceOperation(find_kind, find_text, find_line, i1, instruction, operand))

            else:  # line 170
                try:
                    iroot, itarget = instruction.split("_", 1)
                    itarget = int(itarget)
                except ValueError:
                    continue

                if (iroot not in ("REPLACE", "ADDBEFORE", "ADDAFTER")) or (find_text is None and i1 <= 0):
                    continue

                self.replacements.append(ReplaceOperation(find_kind, find_text, find_line, i1, iroot, operand, itarget))

    @staticmethod
    def apply_substring_replacement(source: str, find: str, replace: str, kind: str) -> str:
        match kind:
            case "REPLACE": return source.replace(find, replace)
            case "ADDBEFORE": return source.replace(find, replace + find)
            case "ADDAFTER": return source.replace(find, find + replace)
            case _: return source

    @staticmethod
    def apply_substring_regex_replacement(source: str, find: str, replace: str, kind: str) -> str:
        match kind:
            case "REPLACE": return re.sub(find, replace, source)
            case "ADDBEFORE": return re.sub(find, replace + "\\g<0>", source)
            case "ADDAFTER": return re.sub(find, "\\g<0>" + replace, source)
            case _: return source

    @staticmethod
    def apply_line_replacement(source: str, replace: str, kind: str) -> str:
        match kind:
            case "REPLACE": return replace
            case "ADDBEFORE": return replace + source
            case "ADDAFTER": return source + replace
            case _: return source

    def apply(self, target_fp: str) -> list[str]:
        """See `ModManager.ModMerger.PendingApply.ApplyModifications`."""
        target_lines = [line.strip() for line in open(target_fp).readlines()]  # line 20
        accumulated_lines: list[str] = []  # line 15

        for l, line in enumerate(target_lines):  # line 21.  `line` is `text` at line 27

            # lines 23-26
            if inserts := self.insert_lines.get(l, None):
                accumulated_lines += inserts

            # lines 28-31
            for rep in self.replacements:
                if rep.occurence == 0:

                    # lines 32-42
                    if rep.find_kind == "NORMAL":
                        if not rep.find_line:
                            line = self.apply_substring_replacement(
                                line, rep.find_text, rep.replace_with, rep.replace_type
                            )
                        elif rep.find_text in line:
                            line = self.apply_line_replacement(line, rep.replace_with, rep.replace_type)

                    # lines 43-53
                    elif rep.find_kind == "REGEX":
                        if not rep.find_line:
                            line = self.apply_substring_regex_replacement(
                                line, rep.find_text, rep.replace_with, rep.replace_type
                            )
                        elif re.search(rep.replace_with, line):
                            line = self.apply_line_replacement(line, rep.replace_with, rep.replace_type)

                    # lines 54-67
                    elif rep.find_kind == "START":
                        if line.startswith(rep.find_text):
                            line = self.apply_line_replacement(line, rep.replace_with, rep.replace_type)
                    elif rep.find_kind == "END":
                        if line.endswith(rep.find_text):
                            line = self.apply_line_replacement(line, rep.replace_with, rep.replace_type)

                    # lines 68-71
                    elif rep.find_line_number == l + 1:
                        line = self.apply_line_replacement(line, rep.replace_with, rep.replace_type)

                # line 73
                else:
                    if rep.occurences_seen < 0:
                        continue

                    # lines 79-99
                    if not rep.find_line:
                        matches: list[re.Match] | None = None
                        if rep.find_kind == "NORMAL":
                            matches = re.findall(f"\\b({rep.find_text})\\b", line)
                        elif rep.find_kind == "REGEX":
                            matches = re.findall(rep.find_text, line)
                        if matches is None:
                            continue
                        if rep.occurences_seen + len(matches) < rep.occurence:
                            rep.occurences_seen += len(matches)
                            continue
                        num = rep.occurence - rep.occurences_seen

                        # line 109-112
                        if num > len(matches):
                            continue

                        a = matches[num - 1].start()

                        # line 113-127
                        if rep.find_kind == "NORMAL":
                            if rep.replace_type == "REPLACE":
                                line = line[:a] + rep.replace_with + line[a + len(rep.find_text):]
                            if rep.replace_type == "ADDBEFORE":
                                line = line[:a] + rep.replace_with + rep.find_text + line[a + len(rep.find_text):]
                            if rep.replace_type == "ADDAFTER":
                                line = line[:a] + rep.find_text + rep.replace_with + line[a + len(rep.find_text):]

                        # line 128-143
                        elif rep.find_kind == "REGEX":
                            if rep.replace_type == "REPLACE":
                                line = line[:a] + re.sub(rep.find_text, rep.replace_with, line[a:], 1)
                            elif rep.replace_type == "ADDBEFORE":
                                line = line[:a] + re.sub(rep.find_text, rep.replace_with + matches[num - 1].group(0), line[a:], 1)
                            elif rep.replace_type == "ADDAFTER":
                                line = line[:a] + re.sub(rep.find_text, matches[num - 1].group(0) + rep.replace_with, line[a:], 1)

                        rep.occurences_seen = -1

                    # lines 146-157
                    elif rep.find_kind == "NORMAL":
                        if rep.find_text in line:
                            rep.occurences_seen += 1
                            if rep.occurences_seen >= rep.occurence:
                                line = self.apply_line_replacement(line, rep.replace_with, rep.replace_type)
                                rep.occurences_seen = -1

                    # lines 158-169
                    elif rep.find_kind == "REGEX":
                        if re.search(rep.find_text, line):
                            rep.occurences_seen += 1
                            if rep.occurences_seen >= rep.occurence:
                                line = self.apply_line_replacement(line, rep.replace_with, rep.replace_type)
                                rep.occurences_seen = -1

                    # lines 170-181
                    elif rep.find_kind == "START":
                        if line.startswith(rep.find_text):
                            rep.occurences_seen += 1
                            if rep.occurences_seen >= rep.occurence:
                                line = self.apply_line_replacement(line, rep.replace_with, rep.replace_type)
                                rep.occurences_seen = -1

                    # lines 182-190
                    elif rep.find_kind == "END":
                        if line.endswith(rep.find_text):
                            rep.occurences_seen += 1
                            if rep.occurences_seen >= rep.occurence:
                                line = self.apply_line_replacement(line, rep.replace_with, rep.replace_type)
                                rep.occurences_seen = -1

            # lines 193 - 196
            if line.strip() != "":
                accumulated_lines.append(line)

        # line 198
        accumulated_lines.extend(self.append_lines)

        return accumulated_lines

    def merge_room_settings(self):
        pass
