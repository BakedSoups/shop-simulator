from __future__ import annotations

import json
import os
import sys
from dataclasses import dataclass
from pathlib import Path

os.environ.setdefault("PYGAME_HIDE_SUPPORT_PROMPT", "1")

import pygame

try:
    import tkinter as tk
    from tkinter import filedialog
except Exception:  # pragma: no cover
    tk = None
    filedialog = None


WINDOW_W = 1380
WINDOW_H = 900
LEFT_W = 860
BG = (24, 27, 34)
PANEL = (34, 39, 48)
CARD = (48, 55, 67)
TEXT = (236, 239, 243)
MUTED = (155, 163, 174)
ACCENT = (255, 196, 87)
GRID = (80, 87, 98)
HIGHLIGHT = (120, 210, 255)


@dataclass
class Clip:
    name: str
    frames: list[int]
    fps: int = 8
    loop: bool = True


class AnimationEditor:
    def __init__(self, image_path: str | None = None):
        pygame.init()
        pygame.font.init()
        self.screen = pygame.display.set_mode((WINDOW_W, WINDOW_H), pygame.RESIZABLE)
        pygame.display.set_caption("Sprite Animation Editor")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("arial", 16)
        self.font_small = pygame.font.SysFont("arial", 13)
        self.font_big = pygame.font.SysFont("arial", 18, bold=True)
        self.running = True
        self.image_path: Path | None = None
        self.sheet: pygame.Surface | None = None
        self.grid_cols = 4
        self.grid_rows = 1
        self.frame_w = 16
        self.frame_h = 16
        self.margin_x = 0
        self.margin_y = 0
        self.spacing_x = 0
        self.spacing_y = 0
        self.scale = 3
        self.scroll_y = 0
        self.selected_frame = 0
        self.selected_frames: list[int] = []
        self.preview_time = 0.0
        self.active_field = "grid_cols"
        self.clip_name = "idle_right"
        self.clip_fps = 8
        self.clip_loop = True
        self.clips: list[Clip] = []
        self.status = "O: open image  Enter: add animation from selected tiles"
        if image_path:
            self.load_image(Path(image_path))

    def load_image(self, path: Path):
        self.sheet = pygame.image.load(path).convert_alpha()
        self.image_path = path
        self.selected_frame = 0
        self.selected_frames = []
        self.preview_time = 0.0
        self.grid_cols = max(1, self.sheet.get_width() // self.frame_w)
        self.grid_rows = max(1, self.sheet.get_height() // self.frame_h)
        self.status = f"Loaded {path.name}"

    def sync_frame_size_from_grid(self):
        if self.sheet is None:
            return
        usable_w = self.sheet.get_width() - self.margin_x * 2 - self.spacing_x * (self.grid_cols - 1)
        usable_h = self.sheet.get_height() - self.margin_y * 2 - self.spacing_y * (self.grid_rows - 1)
        self.frame_w = max(1, usable_w // max(1, self.grid_cols))
        self.frame_h = max(1, usable_h // max(1, self.grid_rows))

    def open_dialog(self):
        if tk is None or filedialog is None:
            self.status = "File dialog unavailable; pass image path on CLI."
            return
        root = tk.Tk()
        root.withdraw()
        filename = filedialog.askopenfilename(
            title="Choose sprite sheet",
            filetypes=[("Images", "*.png;*.jpg;*.jpeg;*.webp"), ("All files", "*.*")],
        )
        root.destroy()
        if filename:
            self.load_image(Path(filename))

    def frame_rects(self) -> list[pygame.Rect]:
        if self.sheet is None:
            return []
        rects: list[pygame.Rect] = []
        for row in range(self.grid_rows):
            y = self.margin_y + row * (self.frame_h + self.spacing_y)
            for col in range(self.grid_cols):
                x = self.margin_x + col * (self.frame_w + self.spacing_x)
                if x + self.frame_w <= self.sheet.get_width() and y + self.frame_h <= self.sheet.get_height():
                    rects.append(pygame.Rect(x, y, self.frame_w, self.frame_h))
        return rects

    def current_preview_frame(self) -> int:
        if self.clips:
            clip = self.clips[-1]
            if not clip.frames:
                return self.selected_frame
            frame_count = len(clip.frames)
            idx = int(self.preview_time * clip.fps)
            if clip.loop:
                idx %= frame_count
            else:
                idx = min(frame_count - 1, idx)
            return clip.frames[idx]
        if not self.selected_frames:
            return self.selected_frame
        idx = int(self.preview_time * max(1, self.clip_fps)) % len(self.selected_frames)
        return self.selected_frames[idx]

    def draw_text(self, text: str, x: int, y: int, color=TEXT, small=False, big=False):
        font = self.font_big if big else self.font_small if small else self.font
        self.screen.blit(font.render(text, True, color), (x, y))

    def draw_sheet(self):
        view = pygame.Rect(0, 0, LEFT_W, WINDOW_H)
        pygame.draw.rect(self.screen, PANEL, view)
        if self.sheet is None:
            self.draw_text("Open a sprite sheet with O", 24, 24, big=True)
            return
        scaled = pygame.transform.scale(
            self.sheet,
            (self.sheet.get_width() * self.scale, self.sheet.get_height() * self.scale),
        )
        self.screen.blit(scaled, (16, 16 - self.scroll_y))
        for idx, rect in enumerate(self.frame_rects()):
            draw = pygame.Rect(
                16 + rect.x * self.scale,
                16 + rect.y * self.scale - self.scroll_y,
                rect.width * self.scale,
                rect.height * self.scale,
            )
            if draw.bottom < 0 or draw.top > WINDOW_H:
                continue
            color = HIGHLIGHT if idx == self.selected_frame else GRID
            pygame.draw.rect(self.screen, color, draw, 2)
            if idx == self.selected_frame:
                self.draw_text(f"{idx}", draw.x + 2, draw.y + 2, small=True)

    def draw_preview(self):
        panel = pygame.Rect(LEFT_W + 10, 10, WINDOW_W - LEFT_W - 20, WINDOW_H - 20)
        pygame.draw.rect(self.screen, PANEL, panel, border_radius=8)
        self.draw_text("Animation Editor", panel.x + 16, panel.y + 14, big=True)
        self.draw_text(self.image_path.name if self.image_path else "No image loaded", panel.x + 16, panel.y + 44, MUTED)
        fields = [
            f"grid_cols: {self.grid_cols}",
            f"grid_rows: {self.grid_rows}",
            f"frame_w: {self.frame_w}",
            f"frame_h: {self.frame_h}",
            f"margin_x: {self.margin_x}",
            f"margin_y: {self.margin_y}",
            f"spacing_x: {self.spacing_x}",
            f"spacing_y: {self.spacing_y}",
            f"scale: {self.scale}",
        ]
        self.draw_text("Slice Settings", panel.x + 16, panel.y + 80, big=True)
        for i, field in enumerate(fields):
            color = ACCENT if field.startswith(self.active_field) else TEXT
            self.draw_text(field, panel.x + 20, panel.y + 112 + i * 22, color)
        self.draw_text("Tab: cycle field  Arrows: edit", panel.x + 20, panel.y + 302, MUTED, small=True)
        self.draw_text("Animation", panel.x + 16, panel.y + 330, big=True)
        self.draw_text(f"name: {self.clip_name}", panel.x + 20, panel.y + 352)
        self.draw_text(f"selected frames: {self.selected_frames or [self.selected_frame]}", panel.x + 20, panel.y + 374)
        self.draw_text(f"fps: {self.clip_fps}", panel.x + 20, panel.y + 418)
        self.draw_text(f"loop: {self.clip_loop}", panel.x + 20, panel.y + 440)
        self.draw_text("N: rename  Enter: add  C: clear  ; ': fps  L: loop", panel.x + 20, panel.y + 468, MUTED, small=True)
        preview_box = pygame.Rect(panel.x + 210, panel.y + 100, 230, 230)
        pygame.draw.rect(self.screen, CARD, preview_box, border_radius=8)
        rects = self.frame_rects()
        if self.sheet is not None and rects:
            idx = min(self.current_preview_frame(), len(rects) - 1)
            frame = pygame.Surface(rects[idx].size, pygame.SRCALPHA)
            frame.blit(self.sheet, (0, 0), rects[idx])
            bounds = frame.get_bounding_rect()
            if bounds.width > 0 and bounds.height > 0:
                trimmed = pygame.Surface(bounds.size, pygame.SRCALPHA)
                trimmed.blit(frame, (-bounds.x, -bounds.y))
                scale = min(180 / max(1, trimmed.get_width()), 180 / max(1, trimmed.get_height()))
                scaled = pygame.transform.scale(trimmed, (max(1, int(trimmed.get_width() * scale)), max(1, int(trimmed.get_height() * scale))))
                self.screen.blit(scaled, scaled.get_rect(center=preview_box.center))
        self.draw_text("Animations", panel.x + 16, panel.y + 520, big=True)
        for i, clip in enumerate(self.clips[-10:]):
            self.draw_text(f"{clip.name}: {clip.frames} @ {clip.fps}fps", panel.x + 20, panel.y + 552 + i * 20, small=True)
        self.draw_text(self.status, panel.x + 16, panel.bottom - 28, MUTED, small=True)

    def save_config(self):
        if self.image_path is None:
            self.status = "No image loaded."
            return
        out = {
            "image": str(self.image_path),
            "frame": {
                "grid_cols": self.grid_cols,
                "grid_rows": self.grid_rows,
                "width": self.frame_w,
                "height": self.frame_h,
                "margin_x": self.margin_x,
                "margin_y": self.margin_y,
                "spacing_x": self.spacing_x,
                "spacing_y": self.spacing_y,
            },
            "animations": [
                {
                    "name": clip.name,
                    "frames": clip.frames,
                    "fps": clip.fps,
                    "loop": clip.loop,
                    "tiles": [{"col": frame % self.grid_cols, "row": frame // self.grid_cols} for frame in clip.frames],
                }
                for clip in self.clips
            ],
        }
        out_path = self.image_path.with_suffix(".anim.json")
        out_path.write_text(json.dumps(out, indent=2))
        self.status = f"Saved {out_path.name}"

    def add_clip(self):
        frames = list(self.selected_frames) if self.selected_frames else [self.selected_frame]
        self.clips.append(Clip(self.clip_name, frames, self.clip_fps, self.clip_loop))
        self.preview_time = 0.0
        self.status = f"Added animation {self.clip_name}"

    def rename_clip(self):
        print("\nEnter clip name:", end=" ", flush=True)
        name = sys.stdin.readline().strip()
        if name:
            self.clip_name = name
            self.status = f"Clip name set to {name}"

    def adjust_field(self, delta: int):
        fields = {
            "grid_cols": "grid_cols",
            "grid_rows": "grid_rows",
            "frame_w": "frame_w",
            "frame_h": "frame_h",
            "margin_x": "margin_x",
            "margin_y": "margin_y",
            "spacing_x": "spacing_x",
            "spacing_y": "spacing_y",
            "scale": "scale",
        }
        attr = fields[self.active_field]
        value = max(0 if attr != "scale" else 1, getattr(self, attr) + delta)
        setattr(self, attr, value)
        if attr in {"grid_cols", "grid_rows"}:
            self.sync_frame_size_from_grid()

    def cycle_field(self):
        order = ["grid_cols", "grid_rows", "frame_w", "frame_h", "margin_x", "margin_y", "spacing_x", "spacing_y", "scale"]
        idx = (order.index(self.active_field) + 1) % len(order)
        self.active_field = order[idx]

    def handle_mouse(self, event: pygame.event.Event):
        if event.button == 1 and self.sheet is not None:
            rects = self.frame_rects()
            mx, my = event.pos
            for idx, rect in enumerate(rects):
                draw = pygame.Rect(
                    16 + rect.x * self.scale,
                    16 + rect.y * self.scale - self.scroll_y,
                    rect.width * self.scale,
                    rect.height * self.scale,
                )
                if draw.collidepoint(mx, my):
                    self.selected_frame = idx
                    if idx in self.selected_frames:
                        self.selected_frames.remove(idx)
                        self.status = f"Removed frame {idx} from selection"
                    else:
                        self.selected_frames.append(idx)
                        self.status = f"Selected frame {idx}"
                    break
        elif event.button == 4:
            self.scroll_y = max(0, self.scroll_y - 48)
        elif event.button == 5:
            self.scroll_y += 48

    def handle_key(self, event: pygame.event.Event):
        if event.key == pygame.K_o:
            self.open_dialog()
        elif event.key == pygame.K_s:
            self.save_config()
        elif event.key == pygame.K_a:
            self.add_clip()
        elif event.key == pygame.K_RETURN:
            self.add_clip()
        elif event.key == pygame.K_n:
            self.rename_clip()
        elif event.key == pygame.K_c:
            self.selected_frames.clear()
            self.status = "Cleared frame selection"
        elif event.key == pygame.K_TAB:
            self.cycle_field()
        elif event.key == pygame.K_LEFT:
            self.adjust_field(-1)
        elif event.key == pygame.K_RIGHT:
            self.adjust_field(1)
        elif event.key == pygame.K_UP:
            self.adjust_field(1)
        elif event.key == pygame.K_DOWN:
            self.adjust_field(-1)
        elif event.key == pygame.K_SEMICOLON:
            self.clip_fps = max(1, self.clip_fps - 1)
        elif event.key == pygame.K_QUOTE:
            self.clip_fps += 1
        elif event.key == pygame.K_l:
            self.clip_loop = not self.clip_loop

    def run(self):
        while self.running:
            dt = self.clock.tick(60) / 1000.0
            self.preview_time += dt
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_key(event)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.handle_mouse(event)
            self.screen.fill(BG)
            self.draw_sheet()
            self.draw_preview()
            pygame.display.flip()
        pygame.quit()


if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else None
    AnimationEditor(path).run()
