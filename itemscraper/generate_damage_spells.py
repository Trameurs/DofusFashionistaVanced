#!/usr/bin/env python3
from __future__ import annotations

import argparse
from copy import deepcopy
import json
import pprint
import sys
import textwrap
from dataclasses import dataclass, replace
from pathlib import Path
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set

from default_damage_spells import DefaultSpellSpec, DEFAULT_DAMAGE_SPELL_SPECS

AUTO_START = "# AUTO-GENERATED DAMAGE_SPELLS START"
AUTO_END = "# AUTO-GENERATED DAMAGE_SPELLS END"
AUTO_COMMENT = (
    "# The block below is overwritten by itemscraper/generate_damage_spells.py.\n"
    "# Do not edit it manually."
)

ELEMENT_LITERAL = {
    "NEUTRAL": "NEUTRAL",
    "EARTH": "EARTH",
    "FIRE": "FIRE",
    "WATER": "WATER",
    "AIR": "AIR",
}

BASE_CLASSES = [
    "Eniripsa",
    "Iop",
    "Xelor",
    "Osamodas",
    "Feca",
    "Sacrier",
    "Ecaflip",
    "Enutrof",
    "Sram",
    "Sadida",
    "Cra",
    "Pandawa",
    "Rogue",
    "Masqueraider",
    "Foggernaut",
    "Eliotrope",
    "Huppermage",
    "Ouginak",
    "Forgelance",
]
CHARACTER_CLASSES = sorted(BASE_CLASSES)


@dataclass
class SpellEntry:
    name: str
    level_requirements: List[int]
    non_crit_ranges: List[List[str]]
    crit_ranges: Optional[List[List[str]]]
    elements: List[str]
    steals: Optional[List[bool]]
    is_linked: Optional[Sequence[Any]]
    order: int
    ankama_id: int


LEGACY_DEFAULT_SPELLS: Dict[str, SpellEntry] = {
    "Burnt Pie": SpellEntry(
        name="Burnt Pie",
        level_requirements=[30, 97, 164],
        non_crit_ranges=[["5-7", "6-8", "8-10"] for _ in range(4)],
        crit_ranges=[["6-8", "8-10", "10-12"] for _ in range(4)],
        elements=["EARTH", "FIRE", "WATER", "AIR"],
        steals=None,
        is_linked=(1, "Leek Pie"),
        order=0,
        ankama_id=0,
    ),
    "Ebony Dofus": SpellEntry(
        name="Ebony Dofus",
        level_requirements=[180],
        non_crit_ranges=[["14-16"], ["14-16"], ["14-16"], ["14-16"]],
        crit_ranges=None,
        elements=["EARTH", "FIRE", "WATER", "AIR"],
        steals=None,
        is_linked=None,
        order=0,
        ankama_id=0,
    ),
    "Leek Pie": SpellEntry(
        name="Leek Pie",
        level_requirements=[97, 164],
        non_crit_ranges=[["6-8", "8-10"] for _ in range(4)],
        crit_ranges=[["8-10", "10-12"] for _ in range(4)],
        elements=["EARTH", "FIRE", "WATER", "AIR"],
        steals=None,
        is_linked=(2, "Burnt Pie"),
        order=0,
        ankama_id=0,
    ),
    "Weapon Skill": SpellEntry(
        name="Weapon Skill",
        level_requirements=[1],
        non_crit_ranges=[["300"]],
        crit_ranges=[["350"]],
        elements=["buff_pow_weapon"],
        steals=None,
        is_linked=None,
        order=0,
        ankama_id=0,
    ),
    "Pestilential Fog": SpellEntry(
        name="Pestilential Fog",
        level_requirements=[200],
        non_crit_ranges=[["16-18"], ["16-18"], ["16-18"], ["16-18"], ["16-18"]],
        crit_ranges=None,
        elements=["NEUTRAL", "EARTH", "FIRE", "WATER", "AIR"],
        steals=None,
        is_linked=None,
        order=0,
        ankama_id=0,
    ),
    "Scurvion Toxicity": SpellEntry(
        name="Scurvion Toxicity",
        level_requirements=[200],
        non_crit_ranges=[["6-8"], ["6-8"], ["6-8"], ["6-8"], ["6-8"]],
        crit_ranges=None,
        elements=["NEUTRAL", "EARTH", "FIRE", "WATER", "AIR"],
        steals=None,
        is_linked=None,
        order=0,
        ankama_id=0,
    ),
}


def parse_args(argv: Optional[Sequence[str]] = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--class-json",
        type=Path,
        default=Path("itemscraper/transformed_class_spells.json"),
        help="Path to transformed_class_spells.json",
    )
    parser.add_argument(
        "--spells-json",
        type=Path,
        default=Path("itemscraper/transformed_spells.json"),
        help="Path to transformed_spells.json",
    )
    parser.add_argument(
        "--constants",
        type=Path,
        default=Path("fashionistapulp/fashionistapulp/dofus_constants.py"),
        help="Path to dofus_constants.py",
    )
    return parser.parse_args(argv)


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def build_spell_map(class_data: Mapping[str, Any], all_spells: Sequence[Mapping[str, Any]]) -> Dict[str, List[SpellEntry]]:
    breed_lookup = _build_breed_lookup(class_data)
    spells_by_class: Dict[str, List[SpellEntry]] = {cls: [] for cls in CHARACTER_CLASSES}

    for spell in sorted(all_spells, key=_sort_key):
        converted = convert_spell(spell)
        if not converted:
            continue
        matched_classes = _classes_for_spell(spell, breed_lookup)
        if matched_classes:
            for class_name in matched_classes:
                spells_by_class[class_name].append(replace(converted))

    for class_name in spells_by_class:
        spells_by_class[class_name].sort(key=lambda entry: (entry.order, entry.ankama_id))

    default_entries = _select_named_defaults(all_spells)
    extras = _extract_default_entries(class_data)
    if extras:
        default_entries = _merge_spell_lists(default_entries, extras)
    if not default_entries:
        default_entries = extras
    spells_by_class = {"default": default_entries, **spells_by_class}
    return spells_by_class


def _sort_key(spell: Mapping[str, Any]) -> tuple:
    return (spell.get("order") or 0, spell.get("ankama_id") or 0)


def _build_breed_lookup(class_data: Mapping[str, Any]) -> Dict[int, str]:
    lookup: Dict[int, str] = {}
    for class_name, payload in class_data.items():
        if class_name == "default" or not isinstance(payload, Mapping):
            continue
        breed_id = payload.get("breed_id")
        if breed_id is None:
            continue
        try:
            lookup[int(breed_id)] = class_name
        except (TypeError, ValueError):
            continue
    return lookup


def _classes_for_spell(spell: Mapping[str, Any], breed_lookup: Mapping[int, str]) -> Set[str]:
    classes: Set[str] = set()
    variant = spell.get("variant_group")
    if isinstance(variant, Mapping):
        breed_id = variant.get("breed_id")
        try:
            breed_key = int(breed_id)
        except (TypeError, ValueError):
            breed_key = None
        if breed_key is not None:
            class_name = breed_lookup.get(breed_key)
            if class_name:
                classes.add(class_name)

    breed_ids = spell.get("breed_ids") or []
    for breed_id in breed_ids:
        try:
            breed_key = int(breed_id)
        except (TypeError, ValueError):
            continue
        class_name = breed_lookup.get(breed_key)
        if class_name:
            classes.add(class_name)
    return classes


def _extract_default_entries(class_data: Mapping[str, Any]) -> List[SpellEntry]:
    payload = class_data.get("default")
    if not payload:
        return []
    entries: List[SpellEntry] = []
    for spell in sorted(payload.get("spells", []), key=_sort_key):
        converted = convert_spell(spell)
        if converted:
            entries.append(converted)
    return entries


def _merge_spell_lists(
    primary: Optional[Sequence[SpellEntry]],
    extras: Sequence[SpellEntry],
) -> List[SpellEntry]:
    merged: List[SpellEntry] = list(primary or [])
    seen = {entry.name for entry in merged}
    for entry in extras:
        if entry.name in seen:
            continue
        merged.append(entry)
        seen.add(entry.name)
    return merged


def _select_named_defaults(all_spells: Sequence[Mapping[str, Any]]) -> List[SpellEntry]:
    lookup: Dict[str, List[Mapping[str, Any]]] = {}
    for spell in all_spells:
        name = (spell.get("name_en") or "").strip().lower()
        if not name:
            continue
        lookup.setdefault(name, []).append(spell)

    entries: List[SpellEntry] = []
    missing: List[str] = []
    for spec in DEFAULT_DAMAGE_SPELL_SPECS:
        spell = _choose_default_candidate(lookup.get(spec.name.lower(), []), spec)
        if spell:
            converted = convert_spell(spell)
            if converted:
                entries.append(converted)
                continue
        legacy = LEGACY_DEFAULT_SPELLS.get(spec.name)
        if legacy:
            entries.append(deepcopy(legacy))
            continue
        missing.append(spec.name)
    if missing:
        print(
            "Warning: the following default spells were not found in transformed_spells.json: "
            + ", ".join(missing),
            file=sys.stderr,
        )
    return entries


def _choose_default_candidate(
    candidates: Optional[Sequence[Mapping[str, Any]]], spec
) -> Optional[Mapping[str, Any]]:
    if not candidates:
        return None

    def score(spell: Mapping[str, Any]) -> tuple:
        variant_group = spell.get("variant_group")
        has_variant = bool(variant_group)
        variant_penalty = 0
        if spec.prefer_variant and not has_variant:
            variant_penalty = 1
        elif not spec.prefer_variant and has_variant:
            variant_penalty = 0
        breed_ids = spell.get("breed_ids") or []
        breed_penalty = 0
        if breed_ids:
            if not all(_is_player_breed(bid) for bid in breed_ids):
                breed_penalty = 1
        damage_penalty = 0 if spell.get("damage_templates") else 1
        return (variant_penalty, breed_penalty, damage_penalty, spell.get("ankama_id") or 0)

    return min(candidates, key=score)


def _is_player_breed(breed_id: Any) -> bool:
    try:
        value = int(breed_id)
    except (TypeError, ValueError):
        return False
    return 1 <= value <= 19


def convert_spell(spell: Mapping[str, Any]) -> Optional[SpellEntry]:
    damage = spell.get("damage_templates")
    if not damage:
        return None
    normal_rows = damage.get("normal") or []
    if not normal_rows:
        return None
    crit_rows = damage.get("critical") or []
    non_crit = [[str(value) for value in row.get("ranges", [])] for row in normal_rows]
    crit = [[str(value) for value in row.get("ranges", [])] for row in crit_rows] if crit_rows else None
    elements = [
        ELEMENT_LITERAL.get(row.get("element"), repr(row.get("element")))
        for row in normal_rows
    ]
    steals_raw = [bool(row.get("steals")) for row in normal_rows]
    steals = steals_raw if any(steals_raw) else None
    level_requirements = spell.get("level_requirements") or damage.get("levels")
    if not level_requirements:
        return None
    variant_link = spell.get("variant_link")
    is_linked = _convert_variant_link(variant_link)

    name = pick_name(spell)
    order = spell.get("order") or 0
    ankama_id = spell.get("ankama_id") or 0
    return SpellEntry(
        name=name,
        level_requirements=[int(level) for level in level_requirements],
        non_crit_ranges=non_crit,
        crit_ranges=crit,
        elements=elements,
        steals=steals,
        is_linked=is_linked,
        order=order,
        ankama_id=ankama_id,
    )


def _convert_variant_link(variant_link: Optional[Mapping[str, Any]]) -> Optional[Sequence[Any]]:
    if not variant_link:
        return None
    linked = variant_link.get("linked_spells") or []
    if not linked:
        return None
    linked_name = pick_name(linked[0].get("names", {}))
    if not linked_name:
        return None
    position = variant_link.get("position", 1)
    return (position, linked_name)


def pick_name(source: Mapping[str, Any]) -> str:
    for key in ("name_en", "name_fr", "name_es", "name_pt", "name_de", "en", "fr", "es", "pt", "de", "name"):
        value = source.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return ""


def render_block(spells_by_class: Mapping[str, List[SpellEntry]]) -> str:
    ordered_keys = ["default"] + [cls for cls in CHARACTER_CLASSES if cls in spells_by_class]
    lines: List[str] = [AUTO_START, AUTO_COMMENT, "DAMAGE_SPELLS = {"]
    for idx, key in enumerate(ordered_keys):
        entries = spells_by_class.get(key, [])
        trailing = "," if idx < len(ordered_keys) - 1 else ""
        lines.append(f"    {key!r}: [")
        for entry in entries:
            lines.extend(render_spell(entry))
        lines.append(f"    ]{trailing}")
    lines.append("}")
    lines.append(AUTO_END)
    lines.append("")
    return "\n".join(lines)


def render_spell(entry: SpellEntry) -> List[str]:
    indent = " " * 8
    literal_levels = pprint.pformat(entry.level_requirements)
    lines: List[str] = [f"{indent}Spell({entry.name!r}, {literal_levels}, Effects("]
    lines.append(_format_literal(entry.non_crit_ranges, indent + "    ") + ",")
    if entry.crit_ranges is None:
        lines.append(f"{indent}    None,")
    else:
        lines.append(_format_literal(entry.crit_ranges, indent + "    ") + ",")
    elements_literal = "[" + ", ".join(entry.elements) + "]"
    lines.append(f"{indent}    {elements_literal},")
    if entry.steals is not None:
        steals_literal = "[" + ", ".join("True" if val else "False" for val in entry.steals) + "]"
        lines.append(f"{indent}    steals={steals_literal},")
    closing = f"{indent})"
    extra_args: List[str] = []
    if entry.is_linked:
        extra_args.append(f"is_linked=({entry.is_linked[0]}, {entry.is_linked[1]!r})")
    if extra_args:
        closing += ", " + ", ".join(extra_args)
    closing += ")"
    closing += ","
    lines.append(closing)
    return lines


def _format_literal(value: Any, indent: str) -> str:
    text = pprint.pformat(value, width=80, compact=False)
    return textwrap.indent(text, indent)


def update_constants_file(path: Path, block: str) -> None:
    text = path.read_text(encoding="utf-8")
    start = text.find(AUTO_START)
    end_marker_index = text.find(AUTO_END)
    if start == -1 or end_marker_index == -1:
        raise RuntimeError("Auto-generated markers not found in dofus_constants.py")
    end = end_marker_index + len(AUTO_END)
    # consume trailing newline(s)
    while end < len(text) and text[end] in "\r\n":
        end += 1
    existing_block = text[start:end]
    if existing_block == block:
        print("DAMAGE_SPELLS already up to date")
        return
    new_text = text[:start] + block + text[end:]
    path.write_text(new_text, encoding="utf-8")
    print(f"Updated DAMAGE_SPELLS in {path}")


def main(argv: Optional[Sequence[str]] = None) -> int:
    args = parse_args(argv)
    class_data = load_json(args.class_json)
    all_spells = load_json(args.spells_json)
    spells_by_class = build_spell_map(class_data, all_spells)
    block = render_block(spells_by_class)
    update_constants_file(args.constants, block)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
