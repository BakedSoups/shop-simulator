from __future__ import annotations

import math
import os
import random
from collections import deque
from dataclasses import dataclass, field
from pathlib import Path
from typing import ClassVar

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame

from item_config import ITEMS, item_def


class Config:
    SCREEN_WIDTH = 1280
    SCREEN_HEIGHT = 800
    RIGHT_PANEL_WIDTH = 220
    BOTTOM_BAR_HEIGHT = 60
    VIEWPORT_WIDTH = SCREEN_WIDTH - RIGHT_PANEL_WIDTH
    VIEWPORT_HEIGHT = SCREEN_HEIGHT - BOTTOM_BAR_HEIGHT
    FPS = 60
    FIXED_DT = 1.0 / 60.0
    TILE_SIZE = 40
    MAP_WIDTH = 32
    MAP_HEIGHT = 18
    CAMERA_ZOOM_MIN = 0.25
    CAMERA_ZOOM_MAX = 2.0
    CAMERA_PAN_SPEED = 650
    PLAYER_SPEED = 160
    WORKER_SPEED = 80
    CUSTOMER_SPEED = 70
    DAY_LENGTH = 180.0
    SOIL_GROWTH_TIME = 15.0
    SPRINKLER_GROWTH_TIME = 8.0
    GREENHOUSE_GROWTH_TIME = 10.0
    CUSTOMER_PATIENCE = 40.0
    MACHINE_TIMES = {
        "washer": 3.0,
        "juicer": 4.0,
        "capper": 2.0,
        "packager": 2.0,
    }
    COSTS = {
        "sprinkler": 50.0,
        "harvester": 120.0,
        "belt": 10.0,
        "grabber": 80.0,
        "buffer_crate": 60.0,
        "worker": 80.0,
        "seed_bundle": 20.0,
    }
    PRODUCT_PRICE = 12.0
    UI_BG = (29, 34, 40)
    UI_PANEL = (40, 47, 56)
    UI_CARD = (55, 64, 75)
    UI_TEXT = (230, 234, 238)
    UI_MUTED = (145, 154, 163)
    UI_ACCENT = (255, 193, 87)
    SOIL_STATES = ("dry", "wet", "planted", "ready")
    FARM_TILES = [(3, 5), (5, 5), (3, 7), (5, 7)]
    FARM_STARTER_STATES = {
        (3, 5): ("ready", SOIL_GROWTH_TIME),
        (5, 5): ("planted", SOIL_GROWTH_TIME * 0.45),
        (3, 7): ("wet", 0.0),
        (5, 7): ("planted", SOIL_GROWTH_TIME * 0.15),
    }
    ASSET_ROOT = Path(__file__).resolve().parent / "assets"


ASSET_MANIFEST = {
    "tiles/floor_farm.png": ((40, 40), (139, 195, 74), "", (255, 255, 255), "rect", (110, 160, 55)),
    "tiles/floor_store.png": ((40, 40), (240, 230, 210), "", (200, 180, 150), "rect", (200, 185, 165)),
    "tiles/soil_dry.png": ((40, 40), (139, 115, 85), "", (255, 255, 255), "rect", (100, 80, 55)),
    "tiles/soil_wet.png": ((40, 40), (101, 80, 55), "", (255, 255, 255), "rect", (70, 50, 30)),
    "tiles/soil_planted.png": ((40, 40), (101, 80, 55), "o", (100, 220, 80), "rect", (70, 50, 30)),
    "tiles/soil_ready.png": ((40, 40), (101, 80, 55), "*", (100, 255, 80), "rect", (70, 50, 30)),
    "tiles/wall.png": ((40, 40), (60, 60, 70), "", (255, 255, 255), "rect", (40, 40, 50)),
    "tiles/path.png": ((40, 40), (180, 160, 130), "", (255, 255, 255), "rect", (150, 130, 100)),
    "tiles/road.png": ((40, 40), (74, 78, 86), "", (255, 255, 255), "rect", (58, 62, 70)),
    "tiles/water_source.png": ((40, 40), (64, 164, 223), "", (255, 255, 255), "rect", (40, 130, 190)),
    "tiles/greenhouse.png": ((40, 40), (180, 230, 180), "GH", (80, 150, 80), "rect", (140, 200, 140)),
    "tiles/furniture/shelf.png": ((40, 40), (160, 110, 60), "SHELF", (255, 240, 200), "rect", (120, 80, 30)),
    "tiles/furniture/register.png": ((40, 40), (60, 180, 100), "REG", (255, 255, 255), "rect", (30, 140, 70)),
    "tiles/furniture/storage_crate.png": ((40, 40), (70, 130, 200), "CRATE", (255, 255, 255), "rect", (40, 90, 160)),
    "tiles/furniture/counter.png": ((40, 40), (200, 180, 150), "CNTR", (120, 100, 70), "rect", (160, 140, 110)),
    "tiles/furniture/entrance.png": ((40, 40), (255, 220, 50), "ENTER", (120, 80, 0), "rect", (200, 160, 0)),
    "tiles/furniture/door.png": ((40, 40), (120, 80, 40), "DOOR", (255, 240, 200), "rect", (85, 55, 25)),
    "machines/washer.png": ((40, 40), (100, 180, 220), "WASH", (255, 255, 255), "rect", (60, 140, 190)),
    "machines/juicer.png": ((40, 40), (220, 150, 50), "JUICE", (255, 255, 255), "rect", (180, 110, 20)),
    "machines/capper.png": ((40, 40), (180, 100, 180), "CAP", (255, 255, 255), "rect", (140, 60, 140)),
    "machines/packager.png": ((40, 40), (100, 200, 150), "PACK", (255, 255, 255), "rect", (60, 160, 110)),
    "machines/belt_h.png": ((40, 40), (80, 80, 90), "E", (200, 200, 220), "rect", (50, 50, 60)),
    "machines/belt_v.png": ((40, 40), (80, 80, 90), "S", (200, 200, 220), "rect", (50, 50, 60)),
    "machines/belt_tl.png": ((40, 40), (80, 80, 90), "W", (200, 200, 220), "rect", (50, 50, 60)),
    "machines/belt_tr.png": ((40, 40), (80, 80, 90), "N", (200, 200, 220), "rect", (50, 50, 60)),
    "machines/grabber.png": ((40, 40), (220, 80, 80), "ARM", (255, 255, 255), "rect", (180, 40, 40)),
    "machines/sprinkler.png": ((40, 40), (100, 200, 240), "SPRNK", (255, 255, 255), "rect", (60, 160, 210)),
    "machines/harvester.png": ((40, 40), (240, 180, 50), "HARV", (255, 255, 255), "rect", (200, 140, 20)),
    "entities/worker_farmer.png": ((32, 32), (255, 160, 50), "F", (255, 255, 255), "circle", (200, 110, 0)),
    "entities/worker_stocker.png": ((32, 32), (255, 100, 100), "S", (255, 255, 255), "circle", (200, 40, 40)),
    "entities/worker_cashier.png": ((32, 32), (100, 220, 180), "C", (255, 255, 255), "circle", (40, 170, 130)),
    "entities/worker_engineer.png": ((32, 32), (180, 100, 220), "E", (255, 255, 255), "circle", (130, 40, 180)),
    "entities/customer.png": ((32, 32), (220, 220, 220), "?", (100, 100, 100), "circle", (160, 160, 160)),
    "entities/car_red.png": ((40, 40), (200, 70, 70), "CAR", (255, 255, 255), "rect", (140, 35, 35)),
    "entities/car_blue.png": ((40, 40), (70, 120, 210), "CAR", (255, 255, 255), "rect", (40, 80, 160)),
    "entities/car_green.png": ((40, 40), (80, 170, 110), "CAR", (255, 255, 255), "rect", (40, 120, 70)),
    "items/crop_raw.png": ((24, 24), (100, 200, 80), "RAW", (255, 255, 255), "diamond", None),
    "items/crop_washed.png": ((24, 24), (140, 220, 100), "WSH", (255, 255, 255), "diamond", None),
    "items/juice_cup.png": ((24, 24), (255, 200, 50), "CUP", (180, 100, 0), "rect", (200, 150, 0)),
    "items/juice_lidded.png": ((24, 24), (255, 220, 100), "JCE", (180, 100, 0), "rect", (200, 160, 20)),
    "items/juice_packaged.png": ((24, 24), (200, 240, 160), "PKG", (80, 140, 40), "rect", (140, 200, 100)),
    "items/fertilizer.png": ((24, 24), (110, 90, 70), "FERT", (255, 255, 255), "rect", (80, 60, 40)),
    "items/seed.png": ((24, 24), (180, 140, 80), "SEED", (255, 255, 255), "diamond", None),
}

DIRS = {"N": (0, -1), "S": (0, 1), "E": (1, 0), "W": (-1, 0)}
WORKER_ASSETS = {
    "farmer": "entities/worker_farmer.png",
    "stocker": "entities/worker_stocker.png",
    "cashier": "entities/worker_cashier.png",
    "engineer": "entities/worker_engineer.png",
}
class AssetManager:
    def __init__(self):
        self.assets: dict[str, pygame.Surface] = {}
        self.font_cache: dict[tuple[str, int, bool], pygame.font.Font] = {}
        self.custom_carrot_stage_names: list[str] = []
        self.custom_full_carrot_name: str | None = None
        self.custom_player_name: str | None = None
        self.generate_placeholder_assets()
        self.load_assets()
        self.load_optional_custom_assets()

    def __repr__(self):
        return f"AssetManager({len(self.assets)} assets)"

    def font(self, size: int, bold: bool = False) -> pygame.font.Font:
        key = ("arial", size, bold)
        if key not in self.font_cache:
            self.font_cache[key] = pygame.font.SysFont(key[0], size, bold=bold)
        return self.font_cache[key]

    def draw_label(self, surface: pygame.Surface, label: str, color: tuple[int, int, int]):
        if not label:
            return
        size = max(10, min(16, surface.get_width() // max(1, len(label)) + 5))
        text = self.font(size, bold=True).render(label, True, color)
        surface.blit(text, text.get_rect(center=surface.get_rect().center))

    def generate_placeholder_assets(self):
        for rel_path, (size, bg, label, label_color, shape, border) in ASSET_MANIFEST.items():
            path = Config.ASSET_ROOT / rel_path
            if path.exists():
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            surface = pygame.Surface(size, pygame.SRCALPHA)
            rect = surface.get_rect()
            if shape == "circle":
                pygame.draw.ellipse(surface, bg, rect.inflate(-4, -4))
                if border:
                    pygame.draw.ellipse(surface, border, rect.inflate(-4, -4), 2)
            elif shape == "diamond":
                points = [(rect.centerx, 2), (rect.right - 2, rect.centery), (rect.centerx, rect.bottom - 2), (2, rect.centery)]
                pygame.draw.polygon(surface, bg, points)
                if border:
                    pygame.draw.polygon(surface, border, points, 2)
            else:
                surface.fill(bg)
                if border:
                    pygame.draw.rect(surface, border, rect, 2)
            self.draw_label(surface, label, label_color)
            pygame.image.save(surface, path)

    def load_assets(self):
        for rel_path in ASSET_MANIFEST:
            self.assets[rel_path] = pygame.image.load(Config.ASSET_ROOT / rel_path).convert_alpha()

    def load_optional_custom_assets(self):
        search_roots = [Path(__file__).resolve().parent, Config.ASSET_ROOT]
        carrot_stage_files: list[Path] = []
        full_carrot_files: list[Path] = []
        player_files: list[Path] = []
        for root in search_roots:
            carrot_stage_files.extend(sorted(root.glob("**/spr_carrot_stage*.png")))
            carrot_stage_files.extend(sorted(root.glob("**/spr_carrot_*.png")))
            full_carrot_files.extend(sorted(root.glob("**/*full_carrot*.png")))
            player_files.extend(sorted(root.glob("**/spr_bumpkin_*.png")))
        seen: set[Path] = set()
        for path in carrot_stage_files:
            if path in seen:
                continue
            seen.add(path)
            key = f"custom/{path.stem}"
            self.assets[key] = pygame.image.load(path).convert_alpha()
            self.custom_carrot_stage_names.append(key)
        if full_carrot_files:
            path = full_carrot_files[0]
            key = f"custom/{path.stem}"
            self.assets[key] = pygame.image.load(path).convert_alpha()
            self.custom_full_carrot_name = key
        if player_files:
            path = player_files[0]
            key = f"custom/{path.stem}"
            self.assets[key] = pygame.image.load(path).convert_alpha()
            self.custom_player_name = key

    def get(self, name: str) -> pygame.Surface:
        return self.assets[name]

    def has(self, name: str) -> bool:
        return name in self.assets


@dataclass
class Item:
    item_type: str
    quantity: int = 1

    def __repr__(self):
        return f"Item({self.item_type}, qty={self.quantity})"

    @property
    def asset_name(self) -> str:
        return item_def(self.item_type).asset_name

    @property
    def display_name(self) -> str:
        return item_def(self.item_type).display_name


@dataclass
class InventorySlot:
    item_type: str | None = None
    quantity: int = 0

    def __repr__(self):
        return f"Slot({self.item_type}, {self.quantity})"

    def can_stack(self, item_type: str) -> bool:
        return self.item_type in (None, item_type)

    def add(self, item_type: str, quantity: int = 1) -> bool:
        if not self.can_stack(item_type):
            return False
        self.item_type = item_type
        self.quantity += quantity
        return True

    def remove(self, quantity: int = 1) -> bool:
        if self.quantity < quantity:
            return False
        self.quantity -= quantity
        if self.quantity == 0:
            self.item_type = None
        return True


@dataclass
class Tile:
    x: int
    y: int
    type: str
    asset_name: str
    walkable: bool = True
    entity: object | None = None
    item: Item | None = None
    belt_progress: float = 0.0
    soil_state: str | None = None
    growth_timer: float = 0.0
    watered: bool = False

    def __repr__(self):
        return f"Tile({self.x}, {self.y}, {self.type}, walkable={self.walkable})"

    def is_soil(self) -> bool:
        return self.type == "soil"

    def reset_soil_visual(self):
        if self.soil_state == "dry":
            self.asset_name = "tiles/soil_dry.png"
        elif self.soil_state == "wet":
            self.asset_name = "tiles/soil_wet.png"
        elif self.soil_state == "planted":
            self.asset_name = "tiles/soil_planted.png"
        elif self.soil_state == "ready":
            self.asset_name = "tiles/soil_ready.png"


class Grid:
    def __init__(self):
        self.tiles = [
            [Tile(x, y, "grass", "tiles/floor_farm.png", True) for y in range(Config.MAP_HEIGHT)]
            for x in range(Config.MAP_WIDTH)
        ]
        self.path_cache: dict[tuple[tuple[int, int], tuple[int, int]], list[tuple[int, int]]] = {}
        self.entrance_tile = (26, 8)
        self.street_exit_tile = (31, 8)
        self.rest_tile = (22, 8)
        self.register_positions: list[tuple[int, int]] = []
        self.counter_positions: list[tuple[int, int]] = []
        self.shelf_positions: list[tuple[int, int]] = []
        self.storage_positions: list[tuple[int, int]] = []
        self.machine_positions: list[tuple[int, int]] = []
        self.build_map()

    def __repr__(self):
        return f"Grid({Config.MAP_WIDTH}x{Config.MAP_HEIGHT})"

    def invalidate_path_cache(self):
        self.path_cache.clear()

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < Config.MAP_WIDTH and 0 <= y < Config.MAP_HEIGHT

    def get(self, x: int, y: int) -> Tile | None:
        if self.in_bounds(x, y):
            return self.tiles[x][y]
        return None

    def neighbors(self, x: int, y: int):
        for dx, dy in DIRS.values():
            nx, ny = x + dx, y + dy
            if self.in_bounds(nx, ny):
                yield nx, ny

    def is_walkable(self, x: int, y: int, goal: tuple[int, int] | None = None) -> bool:
        tile = self.get(x, y)
        if tile is None:
            return False
        if goal == (x, y):
            return True
        if tile.entity and not getattr(tile.entity, "walkable_through", False):
            return False
        return tile.walkable

    def find_path(self, start: tuple[int, int], goal: tuple[int, int]) -> list[tuple[int, int]]:
        if start == goal:
            return []
        cache_key = (start, goal)
        if cache_key in self.path_cache:
            return list(self.path_cache[cache_key])
        frontier: list[tuple[int, tuple[int, int]]] = [(0, start)]
        came_from = {start: None}
        cost_so_far = {start: 0}
        while frontier:
            frontier.sort(key=lambda item: item[0])
            _, current = frontier.pop(0)
            if current == goal:
                break
            for next_pos in self.neighbors(*current):
                if not self.is_walkable(*next_pos, goal=goal):
                    continue
                new_cost = cost_so_far[current] + 1
                if next_pos not in cost_so_far or new_cost < cost_so_far[next_pos]:
                    cost_so_far[next_pos] = new_cost
                    priority = new_cost + abs(goal[0] - next_pos[0]) + abs(goal[1] - next_pos[1])
                    frontier.append((priority, next_pos))
                    came_from[next_pos] = current
        if goal not in came_from:
            return []
        path = []
        current = goal
        while current != start:
            path.append(current)
            current = came_from[current]
        path.reverse()
        self.path_cache[cache_key] = path
        return list(path)

    def set_tile(self, x: int, y: int, type_name: str, asset_name: str, walkable: bool = True):
        tile = self.get(x, y)
        if tile:
            tile.type = type_name
            tile.asset_name = asset_name
            tile.walkable = walkable

    def build_map(self):
        for x in range(Config.MAP_WIDTH):
            for y in range(Config.MAP_HEIGHT):
                if x >= 20:
                    self.set_tile(x, y, "floor", "tiles/floor_store.png")
                else:
                    self.set_tile(x, y, "floor", "tiles/floor_farm.png")
        for x in range(Config.MAP_WIDTH):
            for y in range(0, 3):
                self.set_tile(x, y, "wall", "tiles/wall.png", walkable=False)
        for x, y in Config.FARM_TILES:
            tile = self.get(x, y)
            tile.type = "soil"
            tile.walkable = True
            tile.soil_state = "dry"
            tile.reset_soil_visual()
        for x in range(18, 20):
            for y in range(4, 14):
                self.set_tile(x, y, "path", "tiles/path.png")
        for y in range(4, 13):
            self.set_tile(25, y, "wall", "tiles/wall.png", walkable=False)
        self.set_tile(25, 8, "door", "tiles/furniture/door.png", walkable=True)
        self.set_tile(26, 8, "entrance", "tiles/furniture/entrance.png")
        self.storage_positions.append((8, 8))
        self.shelf_positions.append((22, 6))
        self.machine_positions.append((10, 6))
        for x in range(26, 32):
            for y in range(6, 11):
                self.set_tile(x, y, "road", "tiles/road.png")
        for x in range(24, 26):
            for y in range(6, 11):
                self.set_tile(x, y, "path", "tiles/path.png")


class Machine:
    walkable_through: ClassVar[bool] = False

    def __init__(self, game: "Game", pos: tuple[int, int], asset_name: str, name: str, input_type: str | None, output_type: str | None, process_time: float):
        self.game = game
        self.pos = pos
        self.asset_name = asset_name
        self.name = name
        self.input_type = input_type
        self.output_type = output_type
        self.process_time = process_time
        self.progress = 0.0
        self.input_queue: deque[Item] = deque()
        self.processing_item: Item | None = None
        self.output_item: Item | None = None
        self.walkable_through = False

    def __repr__(self):
        return f"{self.name}@{self.pos}"

    def accepts(self, item: Item) -> bool:
        return self.input_type == item.item_type and len(self.input_queue) < 1 and self.processing_item is None

    def can_receive_output(self) -> bool:
        return self.output_item is None

    def enqueue(self, item: Item) -> bool:
        if self.input_type != item.item_type or len(self.input_queue) >= 1:
            return False
        self.input_queue.append(item)
        return True

    def take_output(self) -> Item | None:
        item = self.output_item
        self.output_item = None
        return item

    def update(self, dt: float):
        if self.processing_item is None and self.input_queue:
            self.processing_item = self.input_queue.popleft()
            self.progress = 0.0
        if self.processing_item is None:
            return
        self.progress += dt / self.process_time
        if self.progress >= 1.0:
            self.output_item = Item(self.output_type)
            self.processing_item = None
            self.progress = 0.0

    def draw_overlay(self, surface: pygame.Surface, camera: "Camera"):
        if self.processing_item:
            x, y = camera.world_to_screen(*self.pos)
            bar = pygame.Rect(x, y + int(Config.TILE_SIZE * camera.zoom) + 2, int(Config.TILE_SIZE * camera.zoom), 6)
            pygame.draw.rect(surface, (20, 20, 20), bar)
            fill = bar.copy()
            fill.width = int(fill.width * self.progress)
            pygame.draw.rect(surface, (91, 217, 124), fill)


class StorageCrate(Machine):
    walkable_through = False

    def __init__(self, game: "Game", pos: tuple[int, int], capacity: int = 8):
        super().__init__(game, pos, "tiles/furniture/storage_crate.png", "crate", None, None, 0.0)
        self.capacity = capacity
        self.items: list[Item] = []

    def enqueue(self, item: Item) -> bool:
        if len(self.items) >= self.capacity:
            return False
        self.items.append(item)
        return True

    def take_matching(self, item_type: str) -> Item | None:
        for index, item in enumerate(self.items):
            if item.item_type == item_type:
                return self.items.pop(index)
        return None

    def count(self, item_type: str) -> int:
        return sum(1 for item in self.items if item.item_type == item_type)

    def update(self, dt: float):
        return


class Shelf(Machine):
    walkable_through = False

    def __init__(self, game: "Game", pos: tuple[int, int]):
        super().__init__(game, pos, "tiles/furniture/shelf.png", "shelf", None, None, 0.0)
        self.stock: list[Item] = []

    def enqueue(self, item: Item) -> bool:
        if item.item_type != "juice_packaged" or len(self.stock) >= 5:
            return False
        self.stock.append(item)
        return True

    def take_one(self) -> Item | None:
        return self.stock.pop(0) if self.stock else None

    def update(self, dt: float):
        return


class Register(Machine):
    walkable_through = False

    def __init__(self, game: "Game", pos: tuple[int, int]):
        super().__init__(game, pos, "tiles/furniture/register.png", "register", None, None, 0.0)
        self.queue: list[Customer] = []

    def update(self, dt: float):
        return


class Belt(Machine):
    def __init__(self, game: "Game", pos: tuple[int, int], direction: str):
        asset = {
            "E": "machines/belt_h.png",
            "W": "machines/belt_tl.png",
            "S": "machines/belt_v.png",
            "N": "machines/belt_tr.png",
        }[direction]
        super().__init__(game, pos, asset, "belt", None, None, 0.0)
        self.direction = direction
        self.walkable_through = True

    def update(self, dt: float):
        tile = self.game.grid.get(*self.pos)
        if not tile or not tile.item:
            tile.belt_progress = 0.0
            return
        tile.belt_progress += dt / 2.0
        if tile.belt_progress < 1.0:
            return
        next_pos = add_pos(self.pos, DIRS[self.direction])
        next_tile = self.game.grid.get(*next_pos)
        if not next_tile:
            tile.belt_progress = 1.0
            return
        if self.game.try_place_item_on_tile(next_tile, tile.item):
            tile.item = None
            tile.belt_progress = 0.0
        else:
            tile.belt_progress = 1.0


class Sprinkler(Machine):
    def __init__(self, game: "Game", pos: tuple[int, int]):
        super().__init__(game, pos, "machines/sprinkler.png", "sprinkler", None, None, 0.0)
        self.timer = 0.0
        self.radius = 1
        self.walkable_through = False

    def update(self, dt: float):
        self.timer += dt
        if self.timer < 2.0:
            return
        self.timer = 0.0
        for x in range(self.pos[0] - self.radius, self.pos[0] + self.radius + 1):
            for y in range(self.pos[1] - self.radius, self.pos[1] + self.radius + 1):
                tile = self.game.grid.get(x, y)
                if tile and tile.is_soil():
                    tile.watered = True
                    if tile.soil_state == "dry":
                        tile.soil_state = "wet"
                        tile.reset_soil_visual()


class GrabberArm(Machine):
    def __init__(self, game: "Game", pos: tuple[int, int], input_dir: str = "W", output_dir: str = "E"):
        super().__init__(game, pos, "machines/grabber.png", "grabber", None, None, 0.0)
        self.input_dir = input_dir
        self.output_dir = output_dir
        self.timer = 0.0
        self.animation = 0.0

    def update(self, dt: float):
        self.timer += dt
        self.animation = min(1.0, self.timer / 1.5)
        if self.timer < 1.5:
            return
        self.timer = 0.0
        source_tile = self.game.grid.get(*add_pos(self.pos, DIRS[self.input_dir]))
        target_tile = self.game.grid.get(*add_pos(self.pos, DIRS[self.output_dir]))
        if not source_tile or not target_tile:
            return
        item = self.game.extract_item_from_tile(source_tile)
        if item and not self.game.try_place_item_on_tile(target_tile, item):
            self.game.try_place_item_on_tile(source_tile, item)

    def draw_overlay(self, surface: pygame.Surface, camera: "Camera"):
        x, y = camera.world_to_screen(*self.pos)
        center = (x + int(Config.TILE_SIZE * camera.zoom / 2), y + int(Config.TILE_SIZE * camera.zoom / 2))
        dx, dy = DIRS[self.input_dir]
        end = (center[0] + int(dx * 12 * camera.zoom * self.animation), center[1] + int(dy * 12 * camera.zoom * self.animation))
        pygame.draw.line(surface, (255, 245, 245), center, end, 3)


class HarvesterArm(Machine):
    def __init__(self, game: "Game", pos: tuple[int, int]):
        super().__init__(game, pos, "machines/harvester.png", "harvester", None, None, 0.0)
        self.timer = 0.0

    def update(self, dt: float):
        self.timer += dt
        if self.timer < 2.0:
            return
        self.timer = 0.0
        for nx, ny in self.game.grid.neighbors(*self.pos):
            tile = self.game.grid.get(nx, ny)
            if tile and tile.is_soil() and tile.soil_state == "ready":
                if self.game.try_drop_adjacent_item(self.pos, Item("crop_raw")):
                    tile.soil_state = "dry"
                    tile.growth_timer = 0.0
                    tile.watered = False
                    tile.reset_soil_visual()
                    self.game.log.add("Harvester picked ripe crop.", (240, 200, 100))
                    return


class Processor(Machine):
    pass


class Decoration(Machine):
    def __init__(self, game: "Game", pos: tuple[int, int], asset_name: str, name: str = "decoration", walkable: bool = False):
        super().__init__(game, pos, asset_name, name, None, None, 0.0)
        self.walkable_through = walkable

    def update(self, dt: float):
        return


@dataclass
class EventLogEntry:
    message: str
    color: tuple[int, int, int]
    age: float = 0.0


class EventLog:
    def __init__(self):
        self.messages: deque[EventLogEntry] = deque(maxlen=8)

    def __repr__(self):
        return f"EventLog({len(self.messages)})"

    def add(self, message: str, color: tuple[int, int, int] = Config.UI_TEXT):
        self.messages.appendleft(EventLogEntry(message, color))

    def update(self, dt: float):
        for entry in self.messages:
            entry.age += dt


class Camera:
    def __init__(self):
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.zoom = 1.0
        self.screen_origin_x = 0
        self.screen_origin_y = 0

    def __repr__(self):
        return f"Camera(offset=({self.offset_x:.1f},{self.offset_y:.1f}), zoom={self.zoom:.2f})"

    def world_to_screen(self, tx: int | float, ty: int | float) -> tuple[int, int]:
        x = int(self.screen_origin_x + (tx * Config.TILE_SIZE - self.offset_x) * self.zoom)
        y = int(self.screen_origin_y + (ty * Config.TILE_SIZE - self.offset_y) * self.zoom)
        return x, y

    def screen_to_world(self, sx: int, sy: int) -> tuple[int, int]:
        world_x = ((sx - self.screen_origin_x) / self.zoom + self.offset_x) / Config.TILE_SIZE
        world_y = ((sy - self.screen_origin_y) / self.zoom + self.offset_y) / Config.TILE_SIZE
        return int(world_x), int(world_y)

    def fit_world(self, view_width: int, view_height: int):
        world_width = Config.MAP_WIDTH * Config.TILE_SIZE
        world_height = Config.MAP_HEIGHT * Config.TILE_SIZE
        self.zoom = min(view_width / world_width, view_height / world_height)
        self.offset_x = 0.0
        self.offset_y = 0.0
        self.screen_origin_x = int((view_width - world_width * self.zoom) / 2)
        self.screen_origin_y = int((view_height - world_height * self.zoom) / 2)

    def pan(self, dx: float, dy: float):
        self.offset_x = max(0.0, min(self.offset_x + dx, Config.MAP_WIDTH * Config.TILE_SIZE - Config.VIEWPORT_WIDTH / self.zoom))
        self.offset_y = max(0.0, min(self.offset_y + dy, Config.MAP_HEIGHT * Config.TILE_SIZE - Config.VIEWPORT_HEIGHT / self.zoom))

    def apply_zoom(self, amount: float, focus: tuple[int, int]):
        before = self.screen_to_world(*focus)
        self.zoom = max(Config.CAMERA_ZOOM_MIN, min(Config.CAMERA_ZOOM_MAX, self.zoom + amount))
        after = self.screen_to_world(*focus)
        self.pan((before[0] - after[0]) * Config.TILE_SIZE, (before[1] - after[1]) * Config.TILE_SIZE)


class Agent:
    def __init__(self, game: "Game", tile_pos: tuple[int, int], speed: float, asset_name: str, name: str):
        self.game = game
        self.x = tile_pos[0] * Config.TILE_SIZE + Config.TILE_SIZE / 2
        self.y = tile_pos[1] * Config.TILE_SIZE + Config.TILE_SIZE / 2
        self.speed = speed
        self.asset_name = asset_name
        self.name = name
        self.state = "IDLE"
        self.path: list[tuple[int, int]] = []
        self.target_tile: tuple[int, int] | None = None

    def __repr__(self):
        return f"{self.name}({self.state})"

    @property
    def tile_pos(self) -> tuple[int, int]:
        return int(self.x // Config.TILE_SIZE), int(self.y // Config.TILE_SIZE)

    def set_path_to(self, tile_pos: tuple[int, int]):
        self.target_tile = tile_pos
        self.path = self.game.grid.find_path(self.tile_pos, tile_pos)

    def move_along_path(self, dt: float):
        if not self.path:
            return
        next_tile = self.path[0]
        target_x = next_tile[0] * Config.TILE_SIZE + Config.TILE_SIZE / 2
        target_y = next_tile[1] * Config.TILE_SIZE + Config.TILE_SIZE / 2
        dx = target_x - self.x
        dy = target_y - self.y
        dist = math.hypot(dx, dy)
        if dist < 1:
            self.x, self.y = target_x, target_y
            self.path.pop(0)
            return
        step = min(dist, self.speed * dt)
        self.x += dx / dist * step
        self.y += dy / dist * step

    def draw(self, surface: pygame.Surface, camera: Camera, assets: AssetManager):
        sprite = assets.get(self.asset_name)
        x = int((self.x - sprite.get_width() / 2 - camera.offset_x) * camera.zoom)
        y = int((self.y - sprite.get_height() / 2 - camera.offset_y) * camera.zoom)
        if camera.zoom != 1.0:
            sprite = pygame.transform.smoothscale(sprite, (max(1, int(sprite.get_width() * camera.zoom)), max(1, int(sprite.get_height() * camera.zoom))))
        surface.blit(sprite, (x, y))


class Worker(Agent):
    def __init__(self, game: "Game", tile_pos: tuple[int, int], worker_type: str, name: str):
        super().__init__(game, tile_pos, Config.WORKER_SPEED, WORKER_ASSETS[worker_type], name)
        self.worker_type = worker_type
        self.current_task: str = "Idle"
        self.work_timer = 0.0
        self.inventory: Item | None = None
        self.assigned_register: Register | None = None

    def update(self, dt: float):
        if self.state == "WALKING":
            self.move_along_path(dt)
            if not self.path and self.target_tile == self.tile_pos:
                self.state = "WORKING"
                self.work_timer = 0.0
        elif self.state == "WORKING":
            self.work_timer += dt
            self.perform_task(dt)
        else:
            self.think()

    def think(self):
        if self.worker_type == "farmer":
            self.find_farmer_task()
        elif self.worker_type == "stocker":
            self.find_stocker_task()
        elif self.worker_type == "cashier":
            self.find_cashier_task()
        else:
            self.current_task = "Idle"

    def assign_walk(self, target: tuple[int, int], task: str):
        self.current_task = task
        self.state = "WALKING"
        self.set_path_to(target)

    def find_farmer_task(self):
        for tile in self.game.soil_tiles():
            if tile.soil_state == "ready":
                self.assign_walk((tile.x, tile.y), "Harvest")
                return
        for tile in self.game.soil_tiles():
            if tile.soil_state == "dry":
                self.assign_walk((tile.x, tile.y), "Water")
                return
        for tile in self.game.soil_tiles():
            if tile.soil_state == "wet" and self.game.seed_count() > 0:
                self.assign_walk((tile.x, tile.y), "Plant")
                return
        self.current_task = "Idle"

    def find_stocker_task(self):
        if self.inventory is None:
            for machine in self.game.processing_chain:
                source = self.game.find_supply_for_machine(machine)
                if source:
                    self.assign_walk(source.pos, f"Pickup {machine.name}")
                    self.target_machine = machine
                    return
            for shelf in self.game.shelves:
                if len(shelf.stock) < 5:
                    producer = self.game.packager
                    if producer.output_item:
                        self.assign_walk(producer.pos, "Pickup packaged juice")
                        self.target_machine = shelf
                        return
        else:
            target = self.game.find_drop_target_for_item(self.inventory)
            if target:
                self.assign_walk(target.pos, f"Deliver {self.inventory.item_type}")
                self.target_machine = target
                return
        self.current_task = "Idle"

    def find_cashier_task(self):
        if self.assigned_register is None:
            for register, worker in self.game.register_staff.items():
                if worker is self:
                    self.assigned_register = register
                    break
        if self.assigned_register is None:
            register = min(self.game.registers, key=lambda reg: len(reg.queue))
            self.game.register_staff[register] = self
            self.assigned_register = register
        if self.tile_pos != self.assigned_register.pos:
            self.assign_walk(self.assigned_register.pos, "Reach register")
        else:
            self.current_task = "Serve"
            self.state = "WORKING"

    def perform_task(self, dt: float):
        tile = self.game.grid.get(*self.tile_pos)
        if self.worker_type == "farmer":
            if self.current_task == "Water" and tile and tile.soil_state == "dry":
                tile.soil_state = "wet"
                tile.watered = True
                tile.reset_soil_visual()
                self.finish_task("Farmer watered soil.")
            elif self.current_task == "Plant" and tile and tile.soil_state == "wet" and self.game.consume_seed():
                tile.soil_state = "planted"
                tile.growth_timer = 0.0
                tile.reset_soil_visual()
                self.finish_task("Farmer planted seed.")
            elif self.current_task == "Harvest" and tile and tile.soil_state == "ready":
                if self.game.deposit_raw_crop():
                    tile.soil_state = "dry"
                    tile.watered = False
                    tile.growth_timer = 0.0
                    tile.reset_soil_visual()
                    self.finish_task("Farmer harvested crop.")
            else:
                self.state = "IDLE"
        elif self.worker_type == "stocker":
            if self.inventory is None:
                self.inventory = self.game.pick_item_for_stocker(self.tile_pos, getattr(self, "target_machine", None))
                self.finish_task("Stocker picked item.", keep_idle=False)
            else:
                target = getattr(self, "target_machine", None)
                if target and self.game.drop_item_to_machine(target, self.inventory):
                    self.inventory = None
                    self.finish_task("Stocker delivered item.", keep_idle=False)
                else:
                    self.state = "IDLE"
        elif self.worker_type == "cashier":
            register = self.assigned_register
            if register and register.queue:
                customer = register.queue[0]
                if customer.state == "WAIT_IN_LINE":
                    customer.serve_progress += dt / 2.5
                    if customer.serve_progress >= 1.0:
                        register.queue.pop(0)
                        customer.finish_purchase()
            else:
                self.current_task = "Waiting"

    def finish_task(self, message: str, keep_idle: bool = True):
        self.game.log.add(message)
        self.work_timer = 0.0
        self.state = "IDLE" if keep_idle else "IDLE"


class Customer(Agent):
    def __init__(self, game: "Game", tile_pos: tuple[int, int], quantity: int):
        super().__init__(game, tile_pos, Config.CUSTOMER_SPEED, "entities/customer.png", f"Customer{len(game.customers)+1}")
        self.quantity = quantity
        self.patience = Config.CUSTOMER_PATIENCE
        self.register: Register | None = None
        self.serve_progress = 0.0
        self.state = "ENTER"
        self.target_shelf: Shelf | None = None
        self.queue_tile: tuple[int, int] | None = None

    def update(self, dt: float):
        self.patience -= dt
        if self.patience <= 0 and self.state not in {"EXIT", "DONE"}:
            if self.register and self in self.register.queue:
                self.register.queue.remove(self)
            self.state = "EXIT"
            self.set_path_to(self.game.grid.street_exit_tile)
            self.game.log.add("Customer left angry.", (255, 120, 120))
            self.game.score = max(0, self.game.score - 10)
        if self.state in {"WALK_TO_PRODUCT", "WAIT_FOR_STOCK"}:
            desired_tile = self.game.get_shelf_queue_tile(self)
            if desired_tile and desired_tile != self.queue_tile:
                self.queue_tile = desired_tile
                if self.state == "WALK_TO_PRODUCT":
                    self.set_path_to(desired_tile)
        if self.state in {"ENTER", "WALK_TO_PRODUCT", "WALK_TO_REGISTER", "EXIT"}:
            self.move_along_path(dt)
            if not self.path:
                self.advance_state()
        elif self.state == "WAIT_FOR_STOCK":
            if self.target_shelf and self.game.is_front_customer(self) and len(self.target_shelf.stock) >= self.quantity:
                for _ in range(self.quantity):
                    self.target_shelf.take_one()
                self.finish_purchase()
        elif self.state == "WAIT_IN_LINE":
            return
        elif self.state == "DONE":
            self.move_along_path(dt)

    def advance_state(self):
        if self.state == "ENTER":
            self.target_shelf = self.game.shelves[0]
            self.state = "WALK_TO_PRODUCT"
            self.queue_tile = self.game.get_shelf_queue_tile(self)
            self.set_path_to(self.queue_tile or self.target_shelf.pos)
        elif self.state == "WALK_TO_PRODUCT":
            self.state = "WAIT_FOR_STOCK"
        elif self.state in {"EXIT", "DONE"} and self.tile_pos == self.game.grid.street_exit_tile:
            self.game.remove_customer(self)

    def finish_purchase(self):
        revenue = self.quantity * Config.PRODUCT_PRICE
        self.game.cash += revenue
        self.game.log_sale(revenue, self.quantity)
        self.game.score += 10 * self.quantity
        self.game.customers_served += 1
        self.game.log.add(f"Sold {self.quantity} juice for ${revenue:.2f}.", (120, 240, 150))
        self.state = "DONE"
        self.set_path_to(self.game.grid.street_exit_tile)

    @property
    def order_text(self) -> str:
        return f"{self.quantity}x Juice"


class PlayerController:
    # MULTIPLAYER: add second PlayerController here with arrow key bindings
    def __init__(self, game: "Game"):
        self.game = game
        self.held_item: Item | None = None
        self.watering_can_full = False
        start = (8, 8)
        self.x = start[0] * Config.TILE_SIZE + Config.TILE_SIZE / 2
        self.y = start[1] * Config.TILE_SIZE + Config.TILE_SIZE / 2
        self.speed = Config.PLAYER_SPEED
        self.asset_name = game.assets.custom_player_name or "entities/worker_farmer.png"
        self.path: list[tuple[int, int]] = []
        self.pending_interaction: Tile | None = None
        self.state = "IDLE"
        self.last_grid_tile = start
        self.focus_offset = (1, 0)

    def __repr__(self):
        held = self.held_item.item_type if self.held_item else None
        return f"PlayerController(held={held}, watering={self.watering_can_full})"

    @property
    def tile_pos(self) -> tuple[int, int]:
        return int(self.x // Config.TILE_SIZE), int(self.y // Config.TILE_SIZE)

    def refresh_focus_from_grid_step(self):
        current_tile = self.tile_pos
        if current_tile != self.last_grid_tile:
            dx = current_tile[0] - self.last_grid_tile[0]
            dy = current_tile[1] - self.last_grid_tile[1]
            if abs(dx) >= abs(dy) and dx != 0:
                self.focus_offset = (1, 0) if dx > 0 else (-1, 0)
            elif dy != 0:
                self.focus_offset = (0, 1) if dy > 0 else (0, -1)
            self.last_grid_tile = current_tile

    def draw(self, surface: pygame.Surface, camera: Camera, assets: AssetManager):
        sprite = assets.get(self.asset_name)
        x = int((self.x - sprite.get_width() / 2 - camera.offset_x) * camera.zoom)
        y = int((self.y - sprite.get_height() / 2 - camera.offset_y) * camera.zoom)
        if camera.zoom != 1.0:
            sprite = pygame.transform.smoothscale(
                sprite,
                (max(1, int(sprite.get_width() * camera.zoom)), max(1, int(sprite.get_height() * camera.zoom))),
            )
        surface.blit(sprite, (x, y))
        if self.held_item:
            held_sprite_name = self.held_item.asset_name
            if self.held_item.item_type == "crop_raw" and assets.custom_full_carrot_name:
                held_sprite_name = assets.custom_full_carrot_name
            held_sprite = assets.get(held_sprite_name)
            if self.held_item.item_type == "crop_raw":
                held_sprite = pygame.transform.rotate(held_sprite, -35)
            target_h = max(14, int(sprite.get_height() * 0.9))
            target_w = max(12, int(held_sprite.get_width() * (target_h / max(1, held_sprite.get_height()))))
            held_sprite = pygame.transform.smoothscale(held_sprite, (target_w, target_h))
            rect = held_sprite.get_rect(
                center=(
                    x + sprite.get_width() // 2,
                    y - max(10, int(16 * camera.zoom)),
                )
            )
            surface.blit(held_sprite, rect)

    def update(self, dt: float):
        if self.path:
            next_tile = self.path[0]
            target_x = next_tile[0] * Config.TILE_SIZE + Config.TILE_SIZE / 2
            target_y = next_tile[1] * Config.TILE_SIZE + Config.TILE_SIZE / 2
            dx = target_x - self.x
            dy = target_y - self.y
            dist = math.hypot(dx, dy)
            if dist < 1:
                self.x, self.y = target_x, target_y
                self.path.pop(0)
            else:
                step = min(dist, self.speed * dt)
                self.x += dx / dist * step
                self.y += dy / dist * step
                self.refresh_focus_from_grid_step()
            self.state = "WALKING"
            return
        if self.pending_interaction:
            tile = self.pending_interaction
            self.pending_interaction = None
            self.state = "INTERACT"
            self.interact(tile)
        else:
            self.state = "IDLE"

    def manual_move(self, dx: float, dy: float, dt: float):
        if self.path:
            return
        if dx == 0 and dy == 0:
            return
        length = math.hypot(dx, dy)
        dx /= length
        dy /= length
        next_x = self.x + dx * self.speed * dt
        next_y = self.y + dy * self.speed * dt
        target_tile = self.game.grid.get(int(next_x // Config.TILE_SIZE), int(next_y // Config.TILE_SIZE))
        if target_tile and self.game.grid.is_walkable(target_tile.x, target_tile.y):
            self.x = next_x
            self.y = next_y
            self.refresh_focus_from_grid_step()
            self.state = "WALKING"

    def command_move_to(self, tile: Tile):
        target = self.game.get_interaction_tile(tile)
        if target is None:
            self.game.log.add("No path to that spot.", (255, 160, 120))
            return
        self.pending_interaction = None
        self.path = self.game.grid.find_path(self.tile_pos, target)
        if not self.path and self.tile_pos != target:
            self.game.log.add("No path to that spot.", (255, 160, 120))
    
    def try_hold(self, item_type: str) -> bool:
        if self.held_item is not None:
            return False
        self.held_item = Item(item_type)
        return True

    def clear_hand(self):
        self.held_item = None

    def interact(self, tile: Tile):
        if tile.type == "water":
            self.watering_can_full = True
            self.game.log.add("Watering can refilled.", (110, 200, 255))
            return
        if tile.is_soil():
            if tile.soil_state == "dry" and self.watering_can_full:
                tile.soil_state = "wet"
                tile.watered = True
                tile.reset_soil_visual()
                self.watering_can_full = False
                self.game.log.add("Watered soil.")
                return
            if tile.soil_state == "wet" and self.game.consume_seed():
                tile.soil_state = "planted"
                tile.growth_timer = 0.0
                tile.reset_soil_visual()
                self.game.log.add("Planted a seed.")
                return
            if tile.soil_state == "ready":
                if self.try_hold("crop_raw"):
                    tile.soil_state = "dry"
                    tile.watered = False
                    tile.growth_timer = 0.0
                    tile.reset_soil_visual()
                    self.game.log.add("Picked grapes.")
                else:
                    self.game.log.add("Your hand is full.", (255, 180, 120))
                return
        if tile.entity:
            self.game.interact_with_entity(tile.entity)


class UI:
    def __init__(self, game: "Game"):
        self.game = game

    def __repr__(self):
        return "UI()"

    def build_panel_rect(self) -> pygame.Rect:
        return pygame.Rect(20, 20, 250, 180)

    def build_option_rects(self) -> list[tuple[str, pygame.Rect]]:
        rects: list[tuple[str, pygame.Rect]] = []
        panel = self.build_panel_rect()
        for index, (key, _cost) in enumerate(self.game.build_catalog):
            rects.append((key, pygame.Rect(panel.x + 10, panel.y + 36 + index * 24, panel.width - 20, 20)))
        return rects

    def draw_panel(self, surface: pygame.Surface, rect: pygame.Rect, title: str):
        pygame.draw.rect(surface, Config.UI_PANEL, rect, border_radius=8)
        title_text = self.game.assets.font(16, bold=True).render(title, True, Config.UI_TEXT)
        surface.blit(title_text, (rect.x + 10, rect.y + 8))

    def draw(self, surface: pygame.Surface):
        panel = pygame.Rect(Config.VIEWPORT_WIDTH, 0, Config.RIGHT_PANEL_WIDTH, Config.SCREEN_HEIGHT)
        pygame.draw.rect(surface, Config.UI_BG, panel)
        self.draw_stats(surface)
        self.draw_orders(surface)
        self.draw_workers(surface)
        self.draw_log(surface)
        self.draw_bottom_bar(surface)
        if self.game.build_mode:
            self.draw_build_panel(surface)
        if self.game.day_paused:
            self.draw_day_modal(surface)

    def draw_stats(self, surface: pygame.Surface):
        rect = pygame.Rect(Config.VIEWPORT_WIDTH + 10, 10, Config.RIGHT_PANEL_WIDTH - 20, 110)
        self.draw_panel(surface, rect, "Stats")
        lines = [
            f"Cash: ${self.game.cash:.2f}",
            f"Score: {self.game.score}",
            f"Day: {self.game.day}",
            f"Served: {self.game.customers_served}",
            f"Speed: {self.game.game_speed}x",
        ]
        for index, line in enumerate(lines):
            text = self.game.assets.font(15).render(line, True, Config.UI_TEXT)
            surface.blit(text, (rect.x + 12, rect.y + 32 + index * 16))

    def draw_orders(self, surface: pygame.Surface):
        rect = pygame.Rect(Config.VIEWPORT_WIDTH + 10, 130, Config.RIGHT_PANEL_WIDTH - 20, 150)
        self.draw_panel(surface, rect, "Orders")
        for index, customer in enumerate(self.game.customers[:5]):
            y = rect.y + 32 + index * 26
            label = self.game.assets.font(13, bold=True).render(f"{customer.name}", True, Config.UI_TEXT)
            surface.blit(label, (rect.x + 12, y))
            order = self.game.assets.font(12).render(customer.order_text, True, Config.UI_MUTED)
            surface.blit(order, (rect.x + 12, y + 12))
            bar = pygame.Rect(rect.x + 110, y + 8, 80, 10)
            ratio = max(0.0, customer.patience / Config.CUSTOMER_PATIENCE)
            color = (100, 220, 120) if ratio > 0.6 else (240, 210, 70) if ratio > 0.3 else (240, 90, 90)
            pygame.draw.rect(surface, (24, 24, 24), bar)
            fill = bar.copy()
            fill.width = int(bar.width * ratio)
            pygame.draw.rect(surface, color, fill)

    def draw_workers(self, surface: pygame.Surface):
        rect = pygame.Rect(Config.VIEWPORT_WIDTH + 10, 290, Config.RIGHT_PANEL_WIDTH - 20, 170)
        self.draw_panel(surface, rect, "Workers")
        for index, worker in enumerate(self.game.workers[:6]):
            y = rect.y + 32 + index * 24
            pygame.draw.circle(surface, asset_color_for_worker(worker.worker_type), (rect.x + 18, y + 8), 7)
            text = self.game.assets.font(13).render(f"{worker.name}: {worker.current_task}", True, Config.UI_TEXT)
            surface.blit(text, (rect.x + 32, y))

    def draw_log(self, surface: pygame.Surface):
        rect = pygame.Rect(Config.VIEWPORT_WIDTH + 10, 470, Config.RIGHT_PANEL_WIDTH - 20, 190)
        self.draw_panel(surface, rect, "Event Log")
        for index, entry in enumerate(self.game.log.messages):
            text = self.game.assets.font(12).render(entry.message[:28], True, entry.color)
            surface.blit(text, (rect.x + 12, rect.y + 32 + index * 18))

    def draw_bottom_bar(self, surface: pygame.Surface):
        rect = pygame.Rect(0, Config.VIEWPORT_HEIGHT, Config.VIEWPORT_WIDTH, Config.BOTTOM_BAR_HEIGHT)
        pygame.draw.rect(surface, Config.UI_BG, rect)
        hand_rect = pygame.Rect(12, rect.y + 10, 40, 40)
        pygame.draw.rect(surface, Config.UI_CARD, hand_rect, border_radius=4)
        pygame.draw.rect(surface, Config.UI_ACCENT, hand_rect, 2, border_radius=4)
        if self.game.player.held_item:
            icon = self.game.assets.get(self.game.player.held_item.asset_name)
            surface.blit(icon, icon.get_rect(center=hand_rect.center))
        label = self.game.assets.font(14, bold=True).render("Hand", True, Config.UI_TEXT)
        surface.blit(label, (60, rect.y + 10))
        held_name = self.game.player.held_item.item_type if self.game.player.held_item else "empty"
        held_text = self.game.assets.font(14).render(held_name.replace("_", " "), True, Config.UI_TEXT)
        surface.blit(held_text, (60, rect.y + 30))
        seeds = self.game.assets.font(14).render(f"Seeds: {self.game.seed_count()}", True, Config.UI_TEXT)
        surface.blit(seeds, (220, rect.y + 22))
        text = self.game.assets.font(14).render("WASD move  K interact  B build  F1 debug", True, Config.UI_TEXT)
        surface.blit(text, (360, rect.y + 22))

    def draw_build_panel(self, surface: pygame.Surface):
        rect = self.build_panel_rect()
        pygame.draw.rect(surface, (12, 16, 24), rect, border_radius=8)
        title = self.game.assets.font(16, bold=True).render("Build Mode", True, Config.UI_TEXT)
        surface.blit(title, (rect.x + 12, rect.y + 12))
        for index, (key, cost) in enumerate(self.game.build_catalog):
            option_rect = pygame.Rect(rect.x + 10, rect.y + 36 + index * 24, rect.width - 20, 20)
            if key == self.game.selected_build:
                pygame.draw.rect(surface, Config.UI_ACCENT, option_rect, border_radius=4)
                text_color = (20, 20, 20)
            else:
                pygame.draw.rect(surface, (32, 40, 52), option_rect, border_radius=4)
                text_color = Config.UI_TEXT
            label = self.game.assets.font(14).render(f"{index+1}. {key} ${cost}", True, Config.UI_TEXT)
            label = self.game.assets.font(14).render(f"{index+1}. {key} ${cost}", True, text_color)
            surface.blit(label, (option_rect.x + 8, option_rect.y + 2))
        hint = self.game.assets.font(12).render("Click item, then click map tile", True, Config.UI_MUTED)
        surface.blit(hint, (rect.x + 12, rect.bottom - 18))

    def draw_day_modal(self, surface: pygame.Surface):
        rect = pygame.Rect(320, 180, 420, 220)
        pygame.draw.rect(surface, (18, 22, 30), rect, border_radius=10)
        pygame.draw.rect(surface, Config.UI_ACCENT, rect, 2, border_radius=10)
        lines = [
            f"Day {self.game.day} complete",
            f"Juice sold: {self.game.day_sales}",
            f"Revenue: ${self.game.day_revenue:.2f}",
            f"Expenses: ${self.game.day_expenses:.2f}",
            f"Net: ${self.game.day_revenue - self.game.day_expenses:.2f}",
            "Press Enter for next day",
        ]
        for index, line in enumerate(lines):
            text = self.game.assets.font(18 if index == 0 else 16, bold=index == 0).render(line, True, Config.UI_TEXT)
            surface.blit(text, (rect.x + 24, rect.y + 28 + index * 28))


class Game:
    def __init__(self):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((Config.SCREEN_WIDTH, Config.SCREEN_HEIGHT), pygame.RESIZABLE)
        pygame.display.set_caption("Farm Store Simulator Prototype")
        self.clock = pygame.time.Clock()
        self.assets = AssetManager()
        self.grid = Grid()
        self.camera = Camera()
        self.camera.fit_world(Config.VIEWPORT_WIDTH, Config.VIEWPORT_HEIGHT)
        self.log = EventLog()
        self.ui = UI(self)
        self.running = True
        self.paused = False
        self.day_paused = False
        self.game_speed = 1
        self.debug = False
        self.build_mode = False
        self.selected_build: str | None = None
        self.build_catalog = [
            ("sprinkler", 50),
            ("belt", 10),
            ("grabber", 80),
            ("harvester", 120),
            ("buffer_crate", 60),
        ]
        self.dragging = False
        self.cash = 500.0
        self.score = 0
        self.day = 1
        self.day_timer = 0.0
        self.day_sales = 0
        self.day_revenue = 0.0
        self.day_expenses = 0.0
        self.customers_served = 0
        self.customer_spawn_timer = 0.0
        self.next_customer_spawn = random.uniform(10.0, 20.0)
        self.player = PlayerController(self)
        self.global_seed_stock = 0
        self.workers: list[Worker] = []
        self.customers: list[Customer] = []
        self.register_staff: dict[Register, Worker | None] = {}
        self.machines: dict[tuple[int, int], Machine] = {}
        self.processing_chain: list[Machine] = []
        self.registers: list[Register] = []
        self.shelves: list[Shelf] = []
        self.crates: list[StorageCrate] = []
        self.create_world_entities()
        self.log.add("Prototype loaded. Plant, process, and sell juice.")

    def __repr__(self):
        return f"Game(day={self.day}, cash={self.cash:.2f})"

    def create_world_entities(self):
        for pos in self.grid.shelf_positions:
            shelf = Shelf(self, pos)
            self.place_machine(shelf)
            self.shelves.append(shelf)
        for pos in self.grid.storage_positions:
            crate = StorageCrate(self, pos)
            if pos == self.grid.storage_positions[0]:
                for _ in range(10):
                    crate.items.append(Item("seed"))
            self.place_machine(crate)
            self.crates.append(crate)
        processor_specs = [
            ("juicer", "machines/juicer.png", "crop_raw", "juice_packaged"),
        ]
        for pos, (name, asset, input_type, output_type) in zip(self.grid.machine_positions, processor_specs):
            machine = Processor(self, pos, asset, name, input_type, output_type, Config.MACHINE_TIMES[name])
            self.place_machine(machine)
            self.processing_chain.append(machine)
        self.juicer = self.processing_chain[0]
        self.setup_street_scene()
        self.setup_example_farm()

    def setup_example_farm(self):
        for x, y in Config.FARM_TILES:
            tile = self.grid.get(x, y)
            if tile:
                tile.soil_state = "dry"
                tile.growth_timer = 0.0
                tile.watered = False
                tile.reset_soil_visual()
        for (x, y), (state, timer) in Config.FARM_STARTER_STATES.items():
            tile = self.grid.get(x, y)
            if not tile or not tile.is_soil():
                continue
            tile.soil_state = state
            tile.growth_timer = timer
            tile.watered = state in {"wet", "planted", "ready"}
            tile.reset_soil_visual()

        starter_machines: list[Machine] = [Sprinkler(self, (4, 6))]
        for machine in starter_machines:
            if self.grid.get(*machine.pos).entity is None:
                self.place_machine(machine)
        if self.shelves:
            self.shelves[0].stock.extend([Item("juice_packaged")])
        self.global_seed_stock = 6

    def setup_street_scene(self):
        parked_cars = [
            ((27, 7), "entities/car_red.png"),
            ((29, 7), "entities/car_blue.png"),
            ((30, 9), "entities/car_green.png"),
        ]
        for pos, asset_name in parked_cars:
            tile = self.grid.get(*pos)
            if tile and tile.entity is None:
                self.place_machine(Decoration(self, pos, asset_name, "car"))

    def place_machine(self, machine: Machine):
        self.machines[machine.pos] = machine
        tile = self.grid.get(*machine.pos)
        tile.entity = machine
        tile.walkable = machine.walkable_through
        self.grid.invalidate_path_cache()

    def remove_customer(self, customer: Customer):
        if customer in self.customers:
            self.customers.remove(customer)

    def log_sale(self, revenue: float, quantity: int):
        self.day_sales += quantity
        self.day_revenue += revenue

    def soil_tiles(self):
        for column in self.grid.tiles:
            for tile in column:
                if tile.is_soil():
                    yield tile

    def seed_count(self) -> int:
        return self.global_seed_stock

    def shelf_line_customers(self) -> list[Customer]:
        return [
            customer
            for customer in self.customers
            if customer.state in {"ENTER", "WALK_TO_PRODUCT", "WAIT_FOR_STOCK"}
        ]

    def get_shelf_queue_tile(self, customer: Customer) -> tuple[int, int] | None:
        if not self.shelves:
            return None
        shelf = self.shelves[0]
        line_tiles = [
            (shelf.pos[0] - 1, shelf.pos[1]),
            (shelf.pos[0] - 2, shelf.pos[1]),
            (shelf.pos[0] - 2, shelf.pos[1] + 1),
            (shelf.pos[0] - 3, shelf.pos[1] + 1),
        ]
        line = self.shelf_line_customers()
        try:
            index = line.index(customer)
        except ValueError:
            index = 0
        return line_tiles[min(index, len(line_tiles) - 1)]

    def is_front_customer(self, customer: Customer) -> bool:
        line = self.shelf_line_customers()
        return bool(line) and line[0] is customer

    def consume_seed(self) -> bool:
        if self.global_seed_stock > 0:
            self.global_seed_stock -= 1
            return True
        for crate in self.crates:
            seed = crate.take_matching("seed")
            if seed:
                return True
        return False

    def deposit_raw_crop(self, player_manual: bool = False) -> bool:
        if player_manual:
            return self.player.try_hold("crop_raw")
        for crate in self.crates:
            if crate.enqueue(Item("crop_raw")):
                return True
        return False

    def interact_with_entity(self, entity: Machine):
        if isinstance(entity, Processor):
            if entity.output_item and self.player.try_hold(entity.output_item.item_type):
                entity.output_item = None
                self.log.add("Picked up juice.")
                return
            if self.player.held_item and entity.enqueue(Item(self.player.held_item.item_type)):
                self.player.clear_hand()
                self.log.add(f"Loaded grapes into {entity.name}.")
            elif self.player.held_item:
                self.log.add("That does not go in the juicer.", (255, 180, 120))
        elif isinstance(entity, Shelf):
            if self.player.held_item and self.player.held_item.item_type == "juice_packaged" and entity.enqueue(Item(self.player.held_item.item_type)):
                self.player.clear_hand()
                self.log.add("Placed juice on shelf.")
            elif self.player.held_item:
                self.log.add("Only finished juice goes on the shelf.", (255, 180, 120))
        elif isinstance(entity, StorageCrate):
            if self.player.held_item and entity.enqueue(Item(self.player.held_item.item_type)):
                stored = self.player.held_item.item_type
                self.player.clear_hand()
                self.log.add(f"Stored {stored}.")
                return
            if entity.items:
                item = entity.items.pop(0)
                if self.player.try_hold(item.item_type):
                    self.log.add(f"Took {item.item_type} from crate.")
                else:
                    entity.items.insert(0, item)

    def extract_item_from_tile(self, tile: Tile) -> Item | None:
        if tile.item:
            item = tile.item
            tile.item = None
            tile.belt_progress = 0.0
            return item
        if isinstance(tile.entity, Processor) and tile.entity.output_item:
            return tile.entity.take_output()
        if isinstance(tile.entity, StorageCrate) and tile.entity.items:
            return tile.entity.items.pop(0)
        if isinstance(tile.entity, Shelf) and tile.entity.stock:
            return tile.entity.take_one()
        return None

    def try_place_item_on_tile(self, tile: Tile, item: Item) -> bool:
        if tile.item is None and tile.entity is None:
            tile.item = item
            return True
        entity = tile.entity
        if isinstance(entity, Processor):
            return entity.enqueue(item)
        if isinstance(entity, StorageCrate):
            return entity.enqueue(item)
        if isinstance(entity, Shelf):
            return entity.enqueue(item)
        return False

    def get_interaction_tile(self, tile: Tile) -> tuple[int, int] | None:
        if self.grid.is_walkable(tile.x, tile.y):
            return (tile.x, tile.y)
        options = []
        for nx, ny in self.grid.neighbors(tile.x, tile.y):
            if self.grid.is_walkable(nx, ny):
                options.append((abs(nx - self.player.tile_pos[0]) + abs(ny - self.player.tile_pos[1]), (nx, ny)))
        if not options:
            return None
        options.sort(key=lambda item: item[0])
        return options[0][1]

    def find_nearest_interactable_tile(self) -> Tile | None:
        px, py = self.player.tile_pos
        candidates: list[tuple[int, int, Tile]] = []
        for dx in range(-1, 2):
            for dy in range(-1, 2):
                tile = self.grid.get(px + dx, py + dy)
                if tile is None:
                    continue
                if tile.is_soil() and tile.soil_state in {"ready", "wet"}:
                    candidates.append((abs(dx) + abs(dy), 0, tile))
                elif tile.entity and (
                    isinstance(tile.entity, Processor)
                    or isinstance(tile.entity, Shelf)
                    or isinstance(tile.entity, StorageCrate)
                ):
                    candidates.append((abs(dx) + abs(dy), 1, tile))
        if not candidates:
            return None
        candidates.sort(key=lambda entry: (entry[0], entry[1]))
        return candidates[0][2]

    def player_focus_tile(self) -> Tile | None:
        px, py = self.player.tile_pos
        fx, fy = self.player.focus_offset
        return self.grid.get(px + fx, py + fy)

    def try_drop_adjacent_item(self, pos: tuple[int, int], item: Item) -> bool:
        for nx, ny in self.grid.neighbors(*pos):
            tile = self.grid.get(nx, ny)
            if tile and self.try_place_item_on_tile(tile, item):
                return True
        return False

    def find_supply_for_machine(self, machine: Machine) -> Machine | None:
        if machine.input_type == "crop_raw":
            return next((crate for crate in self.crates if crate.count("crop_raw") > 0), None)
        if machine.input_type == "crop_washed" and self.washer.output_item:
            return self.washer
        if machine.input_type == "juice_cup" and self.juicer.output_item:
            return self.juicer
        if machine.input_type == "juice_lidded" and self.capper.output_item:
            return self.capper
        return None

    def find_drop_target_for_item(self, item: Item) -> Machine | None:
        if item.item_type == "crop_raw":
            return self.washer if self.washer.accepts(item) else None
        if item.item_type == "crop_washed":
            return self.juicer if self.juicer.accepts(item) else None
        if item.item_type == "juice_cup":
            return self.capper if self.capper.accepts(item) else None
        if item.item_type == "juice_lidded":
            return self.packager if self.packager.accepts(item) else None
        if item.item_type == "juice_packaged":
            return next((shelf for shelf in self.shelves if len(shelf.stock) < 5), None)
        return None

    def pick_item_for_stocker(self, pos: tuple[int, int], target_machine: Machine | None) -> Item | None:
        tile = self.grid.get(*pos)
        if not tile or not tile.entity:
            return None
        entity = tile.entity
        if isinstance(entity, StorageCrate):
            needed = target_machine.input_type if isinstance(target_machine, Processor) else "crop_raw"
            return entity.take_matching(needed)
        if isinstance(entity, Processor):
            return entity.take_output()
        return None

    def drop_item_to_machine(self, machine: Machine, item: Item) -> bool:
        return self.try_place_item_on_tile(self.grid.get(*machine.pos), item)

    def update_soil(self, dt: float):
        for tile in self.soil_tiles():
            if tile.soil_state == "planted":
                if not tile.watered:
                    continue
                growth_time = Config.SOIL_GROWTH_TIME
                for machine in self.machines.values():
                    if isinstance(machine, Sprinkler) and abs(machine.pos[0] - tile.x) <= 1 and abs(machine.pos[1] - tile.y) <= 1:
                        growth_time = Config.SPRINKLER_GROWTH_TIME
                        break
                tile.growth_timer += dt
                if tile.growth_timer >= growth_time:
                    tile.soil_state = "ready"
                    tile.reset_soil_visual()

    def update_day_cycle(self, dt: float):
        self.day_timer += dt
        if self.day_timer >= Config.DAY_LENGTH:
            self.day_paused = True
            self.day_expenses = len(self.workers) * 5.0
            self.cash -= self.day_expenses

    def spawn_customer(self):
        quantity = random.randint(1, 3)
        customer = Customer(self, self.grid.entrance_tile, quantity)
        self.customers.append(customer)
        customer.set_path_to(self.grid.entrance_tile)
        self.log.add(f"Customer wants {quantity} juice.")

    def update_customers(self, dt: float):
        if not self.day_paused:
            self.customer_spawn_timer += dt
            if self.customer_spawn_timer >= self.next_customer_spawn:
                self.customer_spawn_timer = 0.0
                self.next_customer_spawn = max(6.0, random.uniform(10.0, 20.0) - self.day * 0.25)
                self.spawn_customer()
        for customer in list(self.customers):
            customer.update(dt)

    def update(self, dt: float):
        if self.paused or self.day_paused:
            return
        scaled_dt = dt * self.game_speed
        self.log.update(scaled_dt)
        self.player.update(scaled_dt)
        self.update_soil(scaled_dt)
        self.update_day_cycle(scaled_dt)
        self.update_customers(scaled_dt)
        for machine in self.machines.values():
            machine.update(scaled_dt)
        for worker in self.workers:
            worker.update(scaled_dt)

    def draw_world(self, surface: pygame.Surface):
        surface.fill((76, 108, 139))
        world = pygame.Surface((Config.VIEWPORT_WIDTH, Config.VIEWPORT_HEIGHT))
        world.fill((114, 171, 212))
        for x in range(Config.MAP_WIDTH):
            for y in range(Config.MAP_HEIGHT):
                tile = self.grid.get(x, y)
                sprite = self.assets.get(tile.asset_name)
                sx, sy = self.camera.world_to_screen(x, y)
                if sx > Config.VIEWPORT_WIDTH or sy > Config.VIEWPORT_HEIGHT or sx < -Config.TILE_SIZE * self.camera.zoom or sy < -Config.TILE_SIZE * self.camera.zoom:
                    continue
                if self.camera.zoom != 1.0:
                    sprite = pygame.transform.smoothscale(sprite, (int(Config.TILE_SIZE * self.camera.zoom), int(Config.TILE_SIZE * self.camera.zoom)))
                world.blit(sprite, (sx, sy))
                self.draw_soil_crop_overlay(world, tile, sx, sy)
                if tile.entity:
                    entity_sprite = self.assets.get(tile.entity.asset_name)
                    if self.camera.zoom != 1.0:
                        entity_sprite = pygame.transform.smoothscale(
                            entity_sprite,
                            (int(Config.TILE_SIZE * self.camera.zoom), int(Config.TILE_SIZE * self.camera.zoom)),
                        )
                    world.blit(entity_sprite, (sx, sy))
                if tile.item:
                    item_sprite = self.assets.get(tile.item.asset_name)
                    if self.camera.zoom != 1.0:
                        size = max(1, int(item_sprite.get_width() * self.camera.zoom))
                        item_sprite = pygame.transform.smoothscale(item_sprite, (size, size))
                    offset = (0, 0)
                    if isinstance(tile.entity, Belt):
                        dx, dy = DIRS[tile.entity.direction]
                        offset = (int(dx * 10 * tile.belt_progress * self.camera.zoom), int(dy * 10 * tile.belt_progress * self.camera.zoom))
                    rect = item_sprite.get_rect(center=(sx + int(Config.TILE_SIZE * self.camera.zoom / 2) + offset[0], sy + int(Config.TILE_SIZE * self.camera.zoom / 2) + offset[1]))
                    world.blit(item_sprite, rect)
        for machine in self.machines.values():
            machine.draw_overlay(world, self.camera)
            if isinstance(machine, Shelf):
                self.draw_shelf_overlay(world, machine)
        for customer in self.customers:
            customer.draw(world, self.camera, self.assets)
            self.draw_customer_overlay(world, customer)
        self.draw_player_focus_tile(world)
        self.player.draw(world, self.camera, self.assets)
        for worker in self.workers:
            worker.draw(world, self.camera, self.assets)
            if self.debug:
                self.draw_agent_debug(world, worker)
        if self.debug:
            self.draw_debug(world)
        surface.blit(world, (0, 0))

    def draw_customer_overlay(self, surface: pygame.Surface, customer: Customer):
        tx, ty = customer.tile_pos
        sx, sy = self.camera.world_to_screen(tx, ty)
        name = self.assets.font(10, bold=True).render(customer.name, True, (255, 255, 255))
        surface.blit(name, (sx - 2, sy - 44))
        bubble = pygame.Rect(sx, sy - 20, 52, 14)
        pygame.draw.rect(surface, (245, 245, 245), bubble, border_radius=7)
        text = self.assets.font(10, bold=True).render(customer.order_text, True, (20, 20, 20))
        surface.blit(text, (bubble.x + 4, bubble.y + 2))
        bar = pygame.Rect(sx, sy - 30, 52, 6)
        pygame.draw.rect(surface, (40, 40, 40), bar)
        fill = bar.copy()
        ratio = max(0.0, customer.patience / Config.CUSTOMER_PATIENCE)
        fill.width = int(bar.width * ratio)
        color = (100, 220, 120) if ratio > 0.6 else (240, 210, 70) if ratio > 0.3 else (240, 90, 90)
        pygame.draw.rect(surface, color, fill)

    def draw_player_focus_tile(self, surface: pygame.Surface):
        tile = self.player_focus_tile()
        if tile is None:
            return
        sx, sy = self.camera.world_to_screen(tile.x, tile.y)
        size = int(Config.TILE_SIZE * self.camera.zoom)
        rect = pygame.Rect(sx, sy, size, size)
        pygame.draw.rect(surface, (255, 237, 140), rect, max(2, int(2 * self.camera.zoom)))

    def draw_soil_crop_overlay(self, surface: pygame.Surface, tile: Tile, sx: int, sy: int):
        if not self.assets.custom_carrot_stage_names or not tile.is_soil():
            return
        stage_name: str | None = None
        if tile.soil_state == "ready":
            stage_name = self.assets.custom_carrot_stage_names[-1]
        elif tile.soil_state == "planted":
            if len(self.assets.custom_carrot_stage_names) == 1:
                stage_name = self.assets.custom_carrot_stage_names[0]
            else:
                growth_ratio = max(0.0, min(0.999, tile.growth_timer / Config.SOIL_GROWTH_TIME))
                index = min(len(self.assets.custom_carrot_stage_names) - 1, int(growth_ratio * len(self.assets.custom_carrot_stage_names)))
                stage_name = self.assets.custom_carrot_stage_names[index]
        elif tile.soil_state == "wet" and self.assets.custom_carrot_stage_names:
            stage_name = self.assets.custom_carrot_stage_names[0]
        if stage_name is None:
            return
        sprite = self.assets.get(stage_name)
        if self.camera.zoom != 1.0:
            sprite = pygame.transform.smoothscale(
                sprite,
                (int(Config.TILE_SIZE * self.camera.zoom), int(Config.TILE_SIZE * self.camera.zoom)),
            )
        surface.blit(sprite, (sx, sy))

    def draw_shelf_overlay(self, surface: pygame.Surface, shelf: Shelf):
        if not shelf.stock:
            return
        sx, sy = self.camera.world_to_screen(*shelf.pos)
        count = min(3, len(shelf.stock))
        for index in range(count):
            sprite = self.assets.get(shelf.stock[index].asset_name)
            size = max(1, int(sprite.get_width() * self.camera.zoom))
            if self.camera.zoom != 1.0:
                sprite = pygame.transform.smoothscale(sprite, (size, size))
            rect = sprite.get_rect(center=(sx + int((12 + index * 10) * self.camera.zoom), sy - int(6 * self.camera.zoom)))
            surface.blit(sprite, rect)

    def draw_agent_debug(self, surface: pygame.Surface, agent: Agent):
        text = self.assets.font(12).render(agent.state, True, (255, 255, 255))
        tx, ty = self.camera.world_to_screen(*agent.tile_pos)
        surface.blit(text, (tx, ty - 14))
        for point in agent.path:
            px, py = self.camera.world_to_screen(*point)
            pygame.draw.circle(surface, (255, 220, 90), (px + 8, py + 8), 3)

    def draw_debug(self, surface: pygame.Surface):
        mouse = pygame.mouse.get_pos()
        if mouse[0] < Config.VIEWPORT_WIDTH and mouse[1] < Config.VIEWPORT_HEIGHT:
            tile = self.camera.screen_to_world(*mouse)
            label = self.assets.font(14).render(f"{tile}", True, (255, 255, 255))
            surface.blit(label, (Config.VIEWPORT_WIDTH - 80, 10))
        fps = self.assets.font(14).render(f"FPS {self.clock.get_fps():.0f}", True, (255, 255, 255))
        surface.blit(fps, (10, 10))
        for x in range(Config.MAP_WIDTH):
            for y in range(Config.MAP_HEIGHT):
                sx, sy = self.camera.world_to_screen(x, y)
                if 0 <= sx < Config.VIEWPORT_WIDTH and 0 <= sy < Config.VIEWPORT_HEIGHT:
                    label = self.assets.font(10).render(f"{x},{y}", True, (0, 0, 0))
                    surface.blit(label, (sx + 2, sy + 2))

    def draw(self):
        self.draw_world(self.screen)
        self.ui.draw(self.screen)
        pygame.display.flip()

    def next_day(self):
        self.day += 1
        self.day_timer = 0.0
        self.day_sales = 0
        self.day_revenue = 0.0
        self.day_expenses = 0.0
        self.day_paused = False
        self.log.add(f"Day {self.day} started.", (255, 210, 110))

    def handle_build_hotkey(self, key: int):
        mapping = {
            pygame.K_1: self.build_catalog[0][0],
            pygame.K_2: self.build_catalog[1][0],
            pygame.K_3: self.build_catalog[2][0],
            pygame.K_4: self.build_catalog[3][0],
            pygame.K_5: self.build_catalog[4][0],
        }
        if key in mapping:
            self.selected_build = mapping[key]
            self.log.add(f"Selected {self.selected_build}.", (180, 220, 255))

    def attempt_build(self, tile: Tile):
        if not self.selected_build:
            self.log.add("Select a build item first.", (255, 180, 120))
            return
        if tile.entity:
            self.log.add("That tile is occupied.", (255, 180, 120))
            return
        if tile.type == "water":
            self.log.add("Cannot build on water.", (255, 180, 120))
            return
        if tile.is_soil() and self.selected_build not in {"sprinkler", "harvester"}:
            self.log.add("Only sprinklers and harvesters can go on soil.", (255, 180, 120))
            return
        cost = Config.COSTS.get(self.selected_build or "", 0.0)
        if self.cash < cost:
            self.log.add("Not enough cash.", (255, 100, 100))
            return
        machine: Machine | None = None
        if self.selected_build == "sprinkler":
            machine = Sprinkler(self, (tile.x, tile.y))
        elif self.selected_build == "belt":
            machine = Belt(self, (tile.x, tile.y), "E")
        elif self.selected_build == "grabber":
            machine = GrabberArm(self, (tile.x, tile.y))
        elif self.selected_build == "harvester":
            machine = HarvesterArm(self, (tile.x, tile.y))
        elif self.selected_build == "buffer_crate":
            machine = StorageCrate(self, (tile.x, tile.y))
            self.crates.append(machine)
        if machine:
            self.cash -= cost
            self.place_machine(machine)
            self.log.add(f"Placed {self.selected_build}.", (120, 220, 255))
        else:
            self.log.add("That build item is not implemented yet.", (255, 180, 120))

    def select_build_from_click(self, pos: tuple[int, int]) -> bool:
        if not self.build_mode:
            return False
        for build_key, rect in self.ui.build_option_rects():
            if rect.collidepoint(pos):
                self.selected_build = build_key
                self.log.add(f"Selected {build_key}.", (180, 220, 255))
                return True
        return False

    def handle_mouse(self, event: pygame.event.Event):
        if event.button == 2:
            self.dragging = True
        elif event.button == 1:
            if self.select_build_from_click(event.pos):
                return
            if event.pos[1] >= Config.VIEWPORT_HEIGHT or event.pos[0] >= Config.VIEWPORT_WIDTH:
                return
            tile_pos = self.camera.screen_to_world(*event.pos)
            tile = self.grid.get(*tile_pos)
            if not tile:
                return
            if self.build_mode and self.selected_build:
                self.attempt_build(tile)
            else:
                self.player.command_move_to(tile)
        elif event.button == 3:
            self.selected_build = None
            self.build_mode = False
        elif event.button == 4:
            self.camera.apply_zoom(0.1, event.pos)
        elif event.button == 5:
            self.camera.apply_zoom(-0.1, event.pos)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.handle_mouse(event)
            elif event.type == pygame.MOUSEBUTTONUP and event.button == 2:
                self.dragging = False
            elif event.type == pygame.MOUSEMOTION and self.dragging:
                self.camera.pan(-event.rel[0] / self.camera.zoom, -event.rel[1] / self.camera.zoom)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.selected_build = None
                    self.build_mode = False
                elif event.key == pygame.K_b:
                    self.build_mode = not self.build_mode
                    if self.build_mode and self.selected_build is None:
                        self.selected_build = self.build_catalog[0][0]
                    self.log.add(
                        f"Build mode {'on' if self.build_mode else 'off'}"
                        + (f": {self.selected_build}" if self.build_mode and self.selected_build else "."),
                        (180, 220, 255),
                    )
                elif event.key == pygame.K_F1:
                    self.debug = not self.debug
                elif event.key == pygame.K_k:
                    tile = self.find_nearest_interactable_tile()
                    if tile:
                        self.player.interact(tile)
                    else:
                        self.log.add("Nothing nearby to use.", (255, 180, 120))
                elif event.key == pygame.K_SPACE:
                    self.paused = not self.paused
                elif event.key in (pygame.K_1, pygame.K_2, pygame.K_3, pygame.K_4, pygame.K_5, pygame.K_6):
                    if self.build_mode:
                        self.handle_build_hotkey(event.key)
                elif event.key == pygame.K_RETURN and self.day_paused:
                    self.next_day()
                elif event.key == pygame.K_MINUS:
                    self.game_speed = max(1, self.game_speed // 2)
                elif event.key == pygame.K_EQUALS:
                    self.game_speed = min(4, self.game_speed * 2)
        keys = pygame.key.get_pressed()
        move_x = 0.0
        move_y = 0.0
        if keys[pygame.K_a]:
            move_x -= 1.0
        if keys[pygame.K_d]:
            move_x += 1.0
        if keys[pygame.K_w]:
            move_y -= 1.0
        if keys[pygame.K_s]:
            move_y += 1.0
        self.player.manual_move(move_x, move_y, Config.FIXED_DT)

    def run(self):
        accumulator = 0.0
        while self.running:
            frame_dt = min(0.25, self.clock.tick(Config.FPS) / 1000.0)
            accumulator += frame_dt
            self.handle_events()
            while accumulator >= Config.FIXED_DT:
                self.update(Config.FIXED_DT)
                accumulator -= Config.FIXED_DT
            self.draw()
        pygame.quit()


def add_pos(a: tuple[int, int], b: tuple[int, int]) -> tuple[int, int]:
    return a[0] + b[0], a[1] + b[1]


def asset_color_for_worker(worker_type: str) -> tuple[int, int, int]:
    return {
        "farmer": (255, 160, 50),
        "stocker": (255, 100, 100),
        "cashier": (100, 220, 180),
        "engineer": (180, 100, 220),
    }[worker_type]


if __name__ == "__main__":
    Game().run()
