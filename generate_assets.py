"""Standalone Pygame asset generator for the farm/store prototype."""

from pathlib import Path

import pygame


ROOT = Path(__file__).resolve().parent
ASSET_ROOT = ROOT / "assets"
TILE = (40, 40)
ENTITY = (32, 32)
ITEM = (24, 24)


def draw_label(surface, label, color):
    if not label:
        return
    font_size = max(10, min(16, surface.get_width() // max(1, len(label)) + 5))
    font = pygame.font.SysFont("arial", font_size, bold=True)
    text = font.render(label, True, color)
    rect = text.get_rect(center=surface.get_rect().center)
    surface.blit(text, rect)


def make_asset(path, size, bg_color, label="", label_color=(255, 255, 255), shape="rect", border_color=None):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    rect = surface.get_rect()
    if shape == "circle":
        pygame.draw.ellipse(surface, bg_color, rect.inflate(-4, -4))
        if border_color:
            pygame.draw.ellipse(surface, border_color, rect.inflate(-4, -4), 2)
    elif shape == "diamond":
        points = [(rect.centerx, 2), (rect.right - 2, rect.centery), (rect.centerx, rect.bottom - 2), (2, rect.centery)]
        pygame.draw.polygon(surface, bg_color, points)
        if border_color:
            pygame.draw.polygon(surface, border_color, points, 2)
    else:
        surface.fill(bg_color)
        if border_color:
            pygame.draw.rect(surface, border_color, rect, 2)
    draw_label(surface, label, label_color)
    path.parent.mkdir(parents=True, exist_ok=True)
    pygame.image.save(surface, path)
    print(f"created: {path.relative_to(ROOT)}")


def build_manifest():
    return [
        ("tiles/floor_farm.png", TILE, (139, 195, 74), "", (255, 255, 255), "rect", (110, 160, 55)),
        ("tiles/floor_store.png", TILE, (240, 230, 210), "", (200, 180, 150), "rect", (200, 185, 165)),
        ("tiles/soil_dry.png", TILE, (139, 115, 85), "", (255, 255, 255), "rect", (100, 80, 55)),
        ("tiles/soil_wet.png", TILE, (101, 80, 55), "", (255, 255, 255), "rect", (70, 50, 30)),
        ("tiles/soil_planted.png", TILE, (101, 80, 55), "o", (100, 220, 80), "rect", (70, 50, 30)),
        ("tiles/soil_ready.png", TILE, (101, 80, 55), "*", (100, 255, 80), "rect", (70, 50, 30)),
        ("tiles/wall.png", TILE, (60, 60, 70), "", (255, 255, 255), "rect", (40, 40, 50)),
        ("tiles/path.png", TILE, (180, 160, 130), "", (255, 255, 255), "rect", (150, 130, 100)),
        ("tiles/water_source.png", TILE, (64, 164, 223), "H2O", (255, 255, 255), "rect", (40, 130, 190)),
        ("tiles/greenhouse.png", TILE, (180, 230, 180), "GH", (80, 150, 80), "rect", (140, 200, 140)),
        ("tiles/furniture/shelf.png", TILE, (160, 110, 60), "SHELF", (255, 240, 200), "rect", (120, 80, 30)),
        ("tiles/furniture/register.png", TILE, (60, 180, 100), "REG", (255, 255, 255), "rect", (30, 140, 70)),
        ("tiles/furniture/storage_crate.png", TILE, (70, 130, 200), "CRATE", (255, 255, 255), "rect", (40, 90, 160)),
        ("tiles/furniture/counter.png", TILE, (200, 180, 150), "CNTR", (120, 100, 70), "rect", (160, 140, 110)),
        ("tiles/furniture/entrance.png", TILE, (255, 220, 50), "ENTER", (120, 80, 0), "rect", (200, 160, 0)),
        ("machines/washer.png", TILE, (100, 180, 220), "WASH", (255, 255, 255), "rect", (60, 140, 190)),
        ("machines/juicer.png", TILE, (220, 150, 50), "JUICE", (255, 255, 255), "rect", (180, 110, 20)),
        ("machines/capper.png", TILE, (180, 100, 180), "CAP", (255, 255, 255), "rect", (140, 60, 140)),
        ("machines/packager.png", TILE, (100, 200, 150), "PACK", (255, 255, 255), "rect", (60, 160, 110)),
        ("machines/belt_h.png", TILE, (80, 80, 90), "E", (200, 200, 220), "rect", (50, 50, 60)),
        ("machines/belt_v.png", TILE, (80, 80, 90), "S", (200, 200, 220), "rect", (50, 50, 60)),
        ("machines/belt_tl.png", TILE, (80, 80, 90), "W", (200, 200, 220), "rect", (50, 50, 60)),
        ("machines/belt_tr.png", TILE, (80, 80, 90), "N", (200, 200, 220), "rect", (50, 50, 60)),
        ("machines/grabber.png", TILE, (220, 80, 80), "ARM", (255, 255, 255), "rect", (180, 40, 40)),
        ("machines/sprinkler.png", TILE, (100, 200, 240), "SPRNK", (255, 255, 255), "rect", (60, 160, 210)),
        ("machines/harvester.png", TILE, (240, 180, 50), "HARV", (255, 255, 255), "rect", (200, 140, 20)),
        ("entities/worker_farmer.png", ENTITY, (255, 160, 50), "F", (255, 255, 255), "circle", (200, 110, 0)),
        ("entities/worker_stocker.png", ENTITY, (255, 100, 100), "S", (255, 255, 255), "circle", (200, 40, 40)),
        ("entities/worker_cashier.png", ENTITY, (100, 220, 180), "C", (255, 255, 255), "circle", (40, 170, 130)),
        ("entities/worker_engineer.png", ENTITY, (180, 100, 220), "E", (255, 255, 255), "circle", (130, 40, 180)),
        ("entities/customer.png", ENTITY, (220, 220, 220), "?", (100, 100, 100), "circle", (160, 160, 160)),
        ("items/crop_raw.png", ITEM, (100, 200, 80), "RAW", (255, 255, 255), "diamond", None),
        ("items/crop_washed.png", ITEM, (140, 220, 100), "WSH", (255, 255, 255), "diamond", None),
        ("items/juice_cup.png", ITEM, (255, 200, 50), "CUP", (180, 100, 0), "rect", (200, 150, 0)),
        ("items/juice_lidded.png", ITEM, (255, 220, 100), "JCE", (180, 100, 0), "rect", (200, 160, 20)),
        ("items/juice_packaged.png", ITEM, (200, 240, 160), "PKG", (80, 140, 40), "rect", (140, 200, 100)),
        ("items/seed.png", ITEM, (180, 140, 80), "SEED", (255, 255, 255), "diamond", None),
    ]


def main():
    pygame.init()
    pygame.font.init()
    for rel_path, size, bg, label, label_color, shape, border in build_manifest():
        make_asset(ASSET_ROOT / rel_path, size, bg, label, label_color, shape, border)
    pygame.quit()


if __name__ == "__main__":
    main()
