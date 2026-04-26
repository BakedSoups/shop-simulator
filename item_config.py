from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ItemDefinition:
    key: str
    display_name: str
    asset_name: str
    category: str


ITEMS: dict[str, ItemDefinition] = {
    "seed": ItemDefinition(
        key="seed",
        display_name="Seeds",
        asset_name="items/seed.png",
        category="farm",
    ),
    "crop_raw": ItemDefinition(
        key="crop_raw",
        display_name="Produce",
        asset_name="items/crop_raw.png",
        category="produce",
    ),
    "fertilizer": ItemDefinition(
        key="fertilizer",
        display_name="Fertilizer",
        asset_name="items/fertilizer.png",
        category="farm",
    ),
    "crop_washed": ItemDefinition(
        key="crop_washed",
        display_name="Washed Crop",
        asset_name="items/crop_washed.png",
        category="produce",
    ),
    "juice_cup": ItemDefinition(
        key="juice_cup",
        display_name="Juice Cup",
        asset_name="items/juice_cup.png",
        category="product",
    ),
    "juice_lidded": ItemDefinition(
        key="juice_lidded",
        display_name="Lidded Juice",
        asset_name="items/juice_lidded.png",
        category="product",
    ),
    "juice_packaged": ItemDefinition(
        key="juice_packaged",
        display_name="Juice",
        asset_name="items/juice_packaged.png",
        category="product",
    ),
}


def item_def(item_key: str) -> ItemDefinition:
    return ITEMS[item_key]
