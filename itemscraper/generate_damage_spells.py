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
from typing import Any, Dict, Iterable, List, Mapping, MutableMapping, Optional, Sequence, Set, Tuple

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

STAT_BUFF_CHARACTERISTICS = {
    10: "buff_str",
    11: "buff_vit",
    13: "buff_cha",
    14: "buff_agi",
    15: "buff_int",
    25: "buff_pow",
}

BUFF_SORT_ORDER = {
    "buff_str": 0,
    "buff_int": 1,
    "buff_cha": 2,
    "buff_agi": 3,
    "buff_vit": 4,
    "buff_pow": 5,
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
GLYPH_EFFECT_IDS = {401, 402, 1091, 1165}


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
    stacks: Optional[int] = None
    heals: Optional[List[bool]] = None
    aggregates: Optional[List[Tuple[str, List[int]]]] = None


def _parse_damage_literal(literal: str) -> tuple[int, int]:
    parts = literal.split("-", 1)
    try:
        if len(parts) == 1:
            value = int(parts[0])
            return value, value
        return int(parts[0]), int(parts[1])
    except ValueError:
        return 0, 0


def _format_damage_literal(min_val: int, max_val: int) -> str:
    if min_val == max_val:
        return str(min_val)
    return f"{min_val}-{max_val}"


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
    elements=["'buff_pow_weapon'"],
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


def _build_spell_lookup(all_spells: Sequence[Mapping[str, Any]]) -> Dict[int, Mapping[str, Any]]:
    lookup: Dict[int, Mapping[str, Any]] = {}
    for spell in all_spells:
        try:
            ankama_id = int(spell.get("ankama_id"))
        except (TypeError, ValueError):
            continue
        if ankama_id <= 0:
            continue
        lookup[ankama_id] = spell
    return lookup


def _apply_stackable_damage(
    damage_template: Optional[Mapping[str, Any]],
    level_requirements: Sequence[int],
    non_crit: List[List[str]],
    crit: Optional[List[List[str]]],
    elements: List[str],
    steals: Optional[List[bool]],
    heals: Optional[List[bool]],
) -> Optional[List[Tuple[str, List[int]]]]:
    if not damage_template:
        return None
    stack_info = damage_template.get("stackable_damage")
    if not stack_info or len(non_crit) != 1 or not elements:
        return None
    per_stack = stack_info.get("per_stack") or []
    if len(per_stack) != len(level_requirements):
        return None
    caps = stack_info.get("max_stacks") or []
    if len(caps) < len(level_requirements):
        caps = caps + [None] * (len(level_requirements) - len(caps))
    stack_cap = 0
    for cap in caps:
        if cap and cap > stack_cap:
            stack_cap = cap
    if stack_cap <= 0:
        return None
    base_non_crit = non_crit[0]
    base_crit = crit[0] if crit else None
    default_element = elements[0]
    default_steal = steals[0] if steals else False
    default_heal = heals[0] if heals else False
    aggregates: List[Tuple[str, List[int]]] = [("Stack 0", [0])]
    for stack_count in range(1, stack_cap + 1):
        new_non: List[str] = []
        for level_idx, base_literal in enumerate(base_non_crit):
            delta_single = per_stack[level_idx] or 0
            if delta_single == 0:
                new_non.append(base_literal)
                continue
            cap = caps[level_idx] if level_idx < len(caps) else None
            effective_stack = min(stack_count, cap) if cap else stack_count
            min_val, max_val = _parse_damage_literal(base_literal)
            delta_total = delta_single * effective_stack
            new_non.append(_format_damage_literal(min_val + delta_total, max_val + delta_total))
        non_crit.append(new_non)
        if base_crit is not None and crit is not None:
            new_crit: List[str] = []
            for level_idx, base_literal in enumerate(base_crit):
                delta_single = per_stack[level_idx] or 0
                if delta_single == 0:
                    new_crit.append(base_literal)
                    continue
                cap = caps[level_idx] if level_idx < len(caps) else None
                effective_stack = min(stack_count, cap) if cap else stack_count
                min_val, max_val = _parse_damage_literal(base_literal)
                delta_total = delta_single * effective_stack
                new_crit.append(_format_damage_literal(min_val + delta_total, max_val + delta_total))
            crit.append(new_crit)
        elements.append(default_element)
        if steals is not None:
            steals.append(default_steal)
        if heals is not None:
            heals.append(default_heal)
        aggregates.append((f"Stack {stack_count}", [len(non_crit) - 1]))
    return aggregates

def build_spell_map(class_data: Mapping[str, Any], all_spells: Sequence[Mapping[str, Any]]) -> Dict[str, List[SpellEntry]]:
    breed_lookup = _build_breed_lookup(class_data)
    spell_lookup = _build_spell_lookup(all_spells)
    spells_by_class: Dict[str, List[SpellEntry]] = {cls: [] for cls in CHARACTER_CLASSES}

    for spell in sorted(all_spells, key=_sort_key):
        converted = convert_spell(spell, spell_lookup=spell_lookup)
        if not converted:
            continue
        matched_classes = _classes_for_spell(spell, breed_lookup)
        if matched_classes:
            for class_name in matched_classes:
                spells_by_class[class_name].append(replace(converted))

    for class_name in spells_by_class:
        spells_by_class[class_name].sort(key=lambda entry: (entry.order, entry.ankama_id))

    default_entries = _select_named_defaults(all_spells, spell_lookup)
    extras = _extract_default_entries(class_data, spell_lookup)
    if extras:
        default_entries = _merge_spell_lists(default_entries, extras)
    if not default_entries:
        default_entries = extras
    spells_by_class = {"default": default_entries, **spells_by_class}
    _prune_missing_links(spells_by_class)
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


def _extract_default_entries(class_data: Mapping[str, Any], spell_lookup: Mapping[int, Mapping[str, Any]]) -> List[SpellEntry]:
    payload = class_data.get("default")
    if not payload:
        return []
    entries: List[SpellEntry] = []
    for spell in sorted(payload.get("spells", []), key=_sort_key):
        converted = convert_spell(spell, spell_lookup=spell_lookup)
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


def _prune_missing_links(spells_by_class: Mapping[str, List[SpellEntry]]) -> None:
    for entries in spells_by_class.values():
        names = {entry.name for entry in entries}
        for entry in entries:
            if entry.is_linked and entry.is_linked[1] not in names:
                entry.is_linked = None


def _select_named_defaults(
    all_spells: Sequence[Mapping[str, Any]],
    spell_lookup: Mapping[int, Mapping[str, Any]],
) -> List[SpellEntry]:
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
            converted = convert_spell(spell, spell_lookup=spell_lookup)
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


def _extract_stat_buff_rows(spell: Mapping[str, Any], level_count: int) -> List[Dict[str, Any]]:
    levels = spell.get("levels") or []
    if not levels or level_count <= 0:
        return []
    rows: Dict[str, Dict[str, Any]] = {}

    def _ensure_row(token: str, order: int) -> Dict[str, Any]:
        row = rows.get(token)
        if row is None:
            row = {
                "token": token,
                "normal": [None] * level_count,
                "critical": None,
                "order": order,
            }
            rows[token] = row
        return row

    for level_idx, level in enumerate(levels):
        for effect in level.get("effects", []):
            token = _stat_buff_token(effect)
            if not token:
                continue
            value = _format_buff_value(effect.get("dice"))
            if not value:
                continue
            row = _ensure_row(token, effect.get("order") or 0)
            row["normal"][level_idx] = value

    for level_idx, level in enumerate(levels):
        for effect in level.get("critical_effects", []):
            token = _stat_buff_token(effect)
            if not token:
                continue
            value = _format_buff_value(effect.get("dice"))
            if not value:
                continue
            row = _ensure_row(token, effect.get("order") or 0)
            if row["critical"] is None:
                row["critical"] = [None] * level_count
            row["critical"][level_idx] = value

    supplemental: List[Dict[str, Any]] = []
    for token, row in rows.items():
        filled_normal = _fill_missing_row(row["normal"])
        filled_crit = _fill_missing_row(row["critical"]) if row["critical"] else None
        supplemental.append(
            {
                "token": token,
                "element": repr(token),
                "normal": filled_normal,
                "critical": filled_crit,
                "order": row["order"],
            }
        )

    supplemental.sort(key=lambda item: (BUFF_SORT_ORDER.get(item["token"], 1000), item["order"], item["element"]))
    return supplemental


def _stat_buff_token(effect: Mapping[str, Any]) -> Optional[str]:
    metadata = effect.get("effect_metadata") or {}
    characteristic = metadata.get("characteristic")
    token = STAT_BUFF_CHARACTERISTICS.get(characteristic)
    if not token:
        return None

    description = (metadata.get("description") or {}).get("en", "").lower()
    if "steals" in description:
        return token

    bonus_type = metadata.get("bonus_type")
    try:
        bonus_value = int(bonus_type)
    except (TypeError, ValueError):
        bonus_value = None
    if bonus_value and bonus_value > 0:
        return token
    return None


def _format_buff_value(dice: Optional[Mapping[str, Any]]) -> Optional[str]:
    if not dice:
        return None
    min_val = dice.get("min")
    max_val = dice.get("max")
    if min_val is None:
        return None
    if max_val in (None, 0, min_val):
        return str(min_val)
    return f"{min_val}-{max_val}"


def _fill_missing_row(values: Optional[Sequence[Optional[str]]]) -> List[str]:
    if not values:
        return []
    filled: List[str] = []
    last_value: Optional[str] = None
    for value in values:
        if value is None:
            filled.append(last_value or "0")
        else:
            filled.append(value)
            last_value = value
    return filled


def _extract_stack_limit(spell: Mapping[str, Any]) -> Optional[int]:
    levels = spell.get("levels") or []
    stack_values: List[int] = []
    for level in levels:
        try:
            stack = int(level.get("max_stack"))
        except (TypeError, ValueError):
            continue
        if stack <= 1:
            continue
        stack_values.append(stack)
    if not stack_values:
        return None
    return max(stack_values)


def _derive_glyph_damage(
    spell: Mapping[str, Any],
    spell_lookup: Mapping[int, Mapping[str, Any]],
    level_count: int,
) -> Optional[Dict[str, List[Dict[str, Any]]]]:
    if level_count <= 0:
        return None
    sources = _glyph_damage_sources(spell, spell_lookup)
    if not sources:
        return None

    normal_rows: List[Dict[str, Any]] = []
    critical_rows: List[Dict[str, Any]] = []
    for _, linked_spell in sources:
        damage = linked_spell.get("damage_templates") or {}
        normal_rows.extend(_copy_damage_rows(damage.get("normal"), level_count))
        critical_rows.extend(_copy_damage_rows(damage.get("critical"), level_count))

    if not normal_rows:
        return None
    return {"normal": normal_rows, "critical": critical_rows}


def _glyph_damage_sources(
    spell: Mapping[str, Any],
    spell_lookup: Mapping[int, Mapping[str, Any]],
) -> List[tuple]:
    candidates: List[tuple] = []
    for level in spell.get("levels") or []:
        for effect_block in (level.get("effects") or []), (level.get("critical_effects") or []):
            for effect in effect_block or []:
                if effect.get("effect_id") not in GLYPH_EFFECT_IDS:
                    continue
                dice = effect.get("dice") or {}
                for key in ("min", "max"):
                    linked_id = dice.get(key)
                    if not isinstance(linked_id, int):
                        continue
                    if linked_id not in spell_lookup:
                        continue
                    candidates.append((effect.get("order") or 0, linked_id))

    ordered: List[tuple] = []
    seen: Set[int] = set()
    for order, spell_id in sorted(candidates):
        if spell_id in seen:
            continue
        seen.add(spell_id)
        linked_spell = spell_lookup.get(spell_id)
        if not linked_spell:
            continue
        damage = linked_spell.get("damage_templates") or {}
        if not (damage.get("normal") or damage.get("critical")):
            continue
        ordered.append((order, linked_spell))
    return ordered


def _copy_damage_rows(rows: Optional[Sequence[Mapping[str, Any]]], level_count: int) -> List[Dict[str, Any]]:
    if not rows or level_count <= 0:
        return []
    copied: List[Dict[str, Any]] = []
    for row in rows:
        copied.append(
            {
                "element": row.get("element"),
                "steals": row.get("steals"),
                "ranges": _fit_ranges(list(row.get("ranges", [])), level_count),
            }
        )
    return copied


def _fit_ranges(source: List[Optional[str]], target_len: int) -> List[str]:
    if target_len <= 0:
        return []
    result: List[str] = []
    last_value: Optional[str] = None
    for idx in range(target_len):
        value = source[idx] if idx < len(source) else None
        if value:
            last_value = value
            result.append(value)
        else:
            result.append(last_value or "0-0")
    return result


def convert_spell(
    spell: Mapping[str, Any],
    *,
    spell_lookup: Optional[Mapping[int, Mapping[str, Any]]] = None,
) -> Optional[SpellEntry]:
    damage = spell.get("damage_templates") or {}
    level_requirements = spell.get("level_requirements") or damage.get("levels")
    if not level_requirements:
        return None
    level_count = len(level_requirements)

    normal_rows = damage.get("normal") or []
    crit_rows = damage.get("critical") or []
    if not normal_rows and spell_lookup:
        glyph_damage = _derive_glyph_damage(spell, spell_lookup, level_count)
        if glyph_damage:
            normal_rows = glyph_damage["normal"]
            crit_rows = glyph_damage["critical"]

    non_crit: List[List[str]] = [
        [str(value) for value in row.get("ranges", [])]
        for row in normal_rows
    ]
    crit: Optional[List[List[str]]] = (
        [[str(value) for value in row.get("ranges", [])] for row in crit_rows]
        if crit_rows
        else None
    )
    elements: List[str] = [
        ELEMENT_LITERAL.get(row.get("element"), repr(row.get("element")))
        for row in normal_rows
    ]
    steals_raw = [bool(row.get("steals")) for row in normal_rows]
    steals = steals_raw if any(steals_raw) else None
    heals_raw = [bool(row.get("heals")) for row in normal_rows]
    heals = heals_raw if any(heals_raw) else None

    buff_rows = _extract_stat_buff_rows(spell, len(level_requirements))
    if buff_rows:
        for row in buff_rows:
            non_crit.append(row["normal"])
            if row["critical"] is not None and len(row["critical"]) == len(level_requirements):
                if crit is None:
                    crit = []
                crit.append(row["critical"])
            elif crit is not None:
                crit.append(list(row["normal"]))
            elements.append(row["element"])
        if steals is not None:
            steals.extend([False] * len(buff_rows))
        if heals is not None:
            heals.extend([False] * len(buff_rows))
    stack_aggregates = _apply_stackable_damage(
        damage,
        level_requirements,
        non_crit,
        crit,
        elements,
        steals,
        heals,
    )
    if not non_crit:
        return None
    stacks = _extract_stack_limit(spell)
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
        heals=heals,
        is_linked=is_linked,
        stacks=stacks,
        aggregates=stack_aggregates,
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
    if entry.heals is not None:
        heals_literal = "[" + ", ".join("True" if val else "False" for val in entry.heals) + "]"
        lines.append(f"{indent}    heals={heals_literal},")
    closing = f"{indent})"
    extra_args: List[str] = []
    if entry.aggregates:
        aggregates_literal = pprint.pformat(entry.aggregates)
        extra_args.append(f"aggregates={aggregates_literal}")
    if entry.stacks not in (None, 1):
        extra_args.append(f"stacks={entry.stacks}")
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
