#!/usr/bin/env python3
"""Build an SRT from selected/translated Scribe dialogue segment IDs."""

import argparse
import json
import re
from pathlib import Path


WEAK_ENDS = {
    "a", "as", "com", "da", "das", "de", "do", "dos", "e", "em", "na",
    "nas", "no", "nos", "o", "os", "ou", "para", "por", "que", "se",
    "sem", "um", "uma",
}
SHORT_FILLER = re.compile(
    r"^(?:mm(?:-hmm)?|m+|uh+|um+|yeah|yep|right|okay|ok|wow|oh|ah|huh|"
    r"you know|I mean|there it is|that's right)[.!? …-]*$",
    re.IGNORECASE,
)


def stamp(value):
    millis = max(0, round(value * 1000))
    hours, millis = divmod(millis, 3_600_000)
    minutes, millis = divmod(millis, 60_000)
    seconds, millis = divmod(millis, 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d},{millis:03d}"


def normalize(text):
    return re.sub(r"\s+", " ", text.replace("\n", " ")).strip()


def wrap(text, width=42):
    text = normalize(text)
    if len(text) <= width:
        return text
    candidates = []
    for index, char in enumerate(text):
        if char != " ":
            continue
        top = text[:index].strip()
        bottom = text[index + 1 :].strip()
        if len(top) > width or len(bottom) > width:
            continue
        weak = top.split()[-1].lower().strip(",.;:!?") in WEAK_ENDS
        top_too_heavy = max(0, len(top) - len(bottom) - 10)
        score = weak * 80 + top_too_heavy * 4 + abs(len(top) - len(bottom))
        candidates.append((score, top, bottom))
    if not candidates:
        return text
    _, top, bottom = min(candidates)
    return f"{top}\n{bottom}"


def load_selection(path):
    value = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(value, dict) and "choices" in value:
        value = json.loads(value["choices"][0]["message"]["content"])
    if isinstance(value, dict):
        value = value.get("cues", value.get("translations", []))
    return value


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("segments")
    parser.add_argument("selection")
    parser.add_argument("output")
    parser.add_argument("--selection-extra", action="append", default=[])
    parser.add_argument("--edits", action="append", default=[])
    parser.add_argument("--audit-json")
    parser.add_argument("--drop-short-fillers", action="store_true")
    parser.add_argument("--merge-gap", type=float, default=0.32)
    args = parser.parse_args()

    segments = json.loads(Path(args.segments).read_text(encoding="utf-8"))
    by_id = {item["id"]: item for item in segments}
    # Keep the optional end_id emitted by the dialogue reviewer. Scribe often
    # splits one spoken sentence into several fragments; using the first ID for
    # the cue start and the last ID for its end prevents a subtitle from
    # appearing only after the sentence has already begun.
    selection_items = load_selection(args.selection)
    for selection_path in args.selection_extra:
        selection_items.extend(load_selection(selection_path))
    selection = {
        item["id"]: {
            "text": item["text"],
            "end_id": item.get("end_id", item["id"]),
        }
        for item in selection_items
    }
    edits = {
        "drop": [], "replace": {}, "add": {}, "end": {}, "end_id": {},
        "final_replace": {},
    }
    for edit_path in args.edits:
        edit_value = json.loads(Path(edit_path).read_text(encoding="utf-8"))
        if isinstance(edit_value, dict) and "choices" in edit_value:
            edit_value = json.loads(edit_value["choices"][0]["message"]["content"])
        if "replacements" in edit_value:
            edit_value = {
                "final_replace": {
                    str(item["id"]): item["text"]
                    for item in edit_value["replacements"]
                }
            }
        for key, value in edit_value.items():
            if key in edits and isinstance(edits[key], dict) and isinstance(value, dict):
                edits[key].update(value)
            else:
                edits[key] = value
    for cue_id in edits["drop"]:
        selection.pop(int(cue_id), None)
    for cue_id, text in edits["replace"].items():
        if int(cue_id) in selection:
            selection[int(cue_id)]["text"] = text
    for cue_id, text in edits["add"].items():
        selection[int(cue_id)] = {"text": text, "end_id": int(cue_id)}
    for cue_id, end_id in edits["end_id"].items():
        if int(cue_id) in selection:
            selection[int(cue_id)]["end_id"] = int(end_id)

    items = []
    covered_until_id = 0
    for cue_id in sorted(selection):
        # A reviewed grouped cue may already cover a fragment that also exists
        # as a standalone draft cue. Keep the grouped cue and discard the
        # duplicate so their time ranges cannot overlap.
        if cue_id <= covered_until_id:
            continue
        source = by_id[cue_id]
        end_id = int(selection[cue_id].get("end_id", cue_id))
        if end_id not in by_id or end_id < cue_id:
            raise ValueError(f"Invalid end_id {end_id} for cue {cue_id}")
        end_source = by_id[end_id]
        if (
            args.drop_short_fillers
            and end_id == cue_id
            and source["end"] - source["start"] < 1.2
            and SHORT_FILLER.match(source["text"].strip())
        ):
            covered_until_id = end_id
            continue
        covered_until_id = end_id
        items.append({
            "ids": list(range(cue_id, end_id + 1)),
            "start": source["start"],
            "end": min(
                float(edits["end"].get(str(cue_id), end_source["end"])),
                source["start"] + 7.28,
            ),
            "speaker": source["speaker"],
            "text": normalize(selection[cue_id]["text"]),
        })

    merged = []
    for item in items:
        if merged:
            previous = merged[-1]
            combined = f'{previous["text"]} {item["text"]}'
            if (
                previous["speaker"] == item["speaker"]
                and item["start"] - previous["end"] <= args.merge_gap
                and len(combined) <= 78
                and item["end"] - previous["start"] <= 7.5
            ):
                previous["ids"].extend(item["ids"])
                previous["end"] = item["end"]
                previous["text"] = combined
                continue
        merged.append(item)

    for item in merged:
        replacement = edits["final_replace"].get(str(item["ids"][0]))
        if replacement is not None:
            item["text"] = normalize(replacement)

    timed = []
    for index, item in enumerate(merged):
        next_start = merged[index + 1]["start"] if index + 1 < len(merged) else None
        # Aim slightly below the hard 17 CPS ceiling to avoid millisecond
        # rounding making an otherwise valid cue fail validation.
        readable_duration = len(item["text"]) / 16.5
        proposed = max(item["end"] + 0.22, item["start"] + readable_duration)
        proposed = min(proposed, item["start"] + 7.5)
        if next_start is not None:
            proposed = min(proposed, next_start - 0.08)
        item["end"] = proposed
        # When two speakers genuinely overlap, a standalone cue can have no
        # usable display window. Drop only these sub-frame items instead of
        # shifting their start earlier or overlapping the next speaker.
        if item["end"] - item["start"] >= 0.12:
            timed.append(item)
    merged = timed

    blocks = []
    for number, item in enumerate(merged, 1):
        blocks.append(
            f'{number}\n{stamp(item["start"])} --> {stamp(item["end"])}\n{wrap(item["text"])}'
        )
    Path(args.output).write_text("\n\n".join(blocks) + "\n", encoding="utf-8")
    if args.audit_json:
        audit = []
        for number, item in enumerate(merged, 1):
            duration = item["end"] - item["start"]
            audit.append({
                "cue": number,
                "id": item["ids"][0],
                "ids": item["ids"],
                "start": item["start"],
                "end": item["end"],
                "duration": round(duration, 3),
                "max_chars": max(1, int(duration * 16.5)),
                "text": item["text"],
                "source": " ".join(by_id[value]["text"] for value in item["ids"]),
            })
        Path(args.audit_json).write_text(
            json.dumps(audit, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )


if __name__ == "__main__":
    main()
