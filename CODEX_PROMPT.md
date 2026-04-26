# Farm Store Simulator — Codex Build Prompt

## Project Overview

Build a top-down 2D farm-to-store simulator in **pure Python using Pygame**. The visual style is Factorio-inspired: clean top-down view, tile-based grid, colored rectangles and circles representing all entities. No image assets yet — everything is drawn with Pygame primitives (rectangles, circles, lines, text). All art will be swapped for real pixel art sprites later, so the code must use a centralized asset/color config that makes swapping easy.

The game has two connected zones on one map:
- **Farm zone** (left ~60% of map): grow crops, harvest, process
- **Store zone** (right ~40% of map): serve customers, run registers, collect cash

The core fantasy: **start by doing everything manually, then automate it all with belts and grabber arms until the farm-to-counter pipeline runs itself.**

---

## Technical Stack

- Python 3.10+
- Pygame 2.x (main game loop, rendering, input)
- No other dependencies
- Target resolution: 1280x800, resizable window
- 60fps cap, fixed timestep update loop
- All game code in one `main.py` to start, with clear class separation
- Folder structure:
  ```
  farm_store_sim/
  ├── main.py
  ├── assets/
  │   ├── tiles/         # placeholder color PNGs (generated at startup)
  │   ├── entities/      # placeholder color PNGs
  │   ├── items/         # placeholder color PNGs
  │   ├── machines/      # placeholder color PNGs
  │   └── ui/            # placeholder color PNGs
  └── CODEX_PROMPT.md
  ```

---

## Asset System (Critical — Read First)

At startup, the game programmatically generates placeholder PNG images for every asset using Pygame and saves them into the `assets/` subfolders. This means:
- The game runs immediately with no missing asset errors
- Every asset has a unique color and label drawn on it
- Real pixel art can be swapped in later by replacing the PNG files
- The asset loader always loads from file — never draws primitives directly in game logic

### Asset Manifest — generate all of these at startup:

**tiles/** (40x40px each)
| filename | color (RGB) | label |
|---|---|---|
| floor_farm.png | (139, 195, 74) | - |
| floor_store.png | (240, 230, 210) | - |
| soil_dry.png | (139, 115, 85) | - |
| soil_wet.png | (101, 80, 55) | - |
| soil_planted.png | (101, 80, 55) + green dot | - |
| soil_ready.png | (101, 80, 55) + bright dot | - |
| wall.png | (60, 60, 70) | - |
| path.png | (180, 160, 130) | - |
| water_source.png | (64, 164, 223) | H2O |
| greenhouse.png | (180, 230, 180) | GH |

**tiles/furniture/**
| filename | color (RGB) | label |
|---|---|---|
| shelf.png | (160, 110, 60) | SHELF |
| register.png | (60, 180, 100) | REG |
| storage_crate.png | (70, 130, 200) | CRATE |
| counter.png | (200, 180, 150) | CNTR |
| entrance.png | (255, 220, 50) | ENTER |

**machines/** (40x40px each)
| filename | color (RGB) | label |
|---|---|---|
| washer.png | (100, 180, 220) | WASH |
| juicer.png | (220, 150, 50) | JUICE |
| capper.png | (180, 100, 180) | CAP |
| packager.png | (100, 200, 150) | PACK |
| belt_h.png | (80, 80, 90) | → |
| belt_v.png | (80, 80, 90) | ↓ |
| belt_tl.png | (80, 80, 90) | ↙ |
| belt_tr.png | (80, 80, 90) | ↘ |
| grabber.png | (220, 80, 80) | ARM |
| sprinkler.png | (100, 200, 240) | SPRNK |
| harvester.png | (240, 180, 50) | HARVST |

**entities/** (32x32px each)
| filename | color (RGB) | label |
|---|---|---|
| worker_farmer.png | (255, 160, 50) | circle |
| worker_stocker.png | (255, 100, 100) | circle |
| worker_cashier.png | (100, 220, 180) | circle |
| worker_engineer.png | (180, 100, 220) | circle |
| customer.png | (220, 220, 220) | circle |

**items/** (24x24px each)
| filename | color (RGB) | label |
|---|---|---|
| crop_raw.png | (100, 200, 80) | RAW |
| crop_washed.png | (140, 220, 100) | WSHED |
| juice_cup.png | (255, 200, 50) | CUP |
| juice_lidded.png | (255, 220, 100) | JUICE |
| juice_packaged.png | (200, 240, 160) | PKG |
| seed.png | (180, 140, 80) | SEED |

---

## Tile & Grid System

- Tile size: 40x40 pixels
- Map size: 60 wide x 24 tall tiles (2400x960 logical pixels)
- Camera pans with WASD or middle-mouse drag, zoom with scroll wheel (0.5x to 2x)
- Each tile has:
  - `type`: floor, soil, wall, path, water, machine, furniture
  - `asset`: filename string to load sprite from
  - `walkable`: bool
  - `entity`: reference to machine/furniture placed on it (or None)
  - `item`: item sitting on this tile (or None) — used for belt transport
- Grid stored as a 2D array of Tile objects
- Separate layers: ground layer, object layer, item layer, entity layer
- Collision uses object layer for pathfinding

### Starting Map Layout (hardcoded default)

```
Columns 0-35: Farm zone
  - Rows 1-3: Top wall border
  - Rows 4-20: Farm floor tiles
  - Rows 4-6, cols 2-10: 3x9 soil patch (default)
  - Row 22, col 5: Water source tile
  - Col 34-35: Transition path between zones (yellow-tinted floor)

Columns 36-59: Store zone
  - Rows 4-20: Store floor tiles
  - Row 4, cols 37-55: Back wall with shelves placed every 3 tiles
  - Rows 17-18, cols 40-55: Counter row (customer-facing)
  - Col 38, rows 8-16: Storage crates (3 of them)
  - Row 20, col 48: Entrance tile (where customers spawn)
  - Rows 8-16, col 55: 3 register tiles
```

---

## The Product Chain (Single Item: Fresh Juice)

This is the ONLY sellable product. The full chain:

```
[Soil] → grow fruit crop (15s) 
  → [Harvest] manually pick or harvester arm 
  → [Storage Crate] holds raw crops 
  → [Wash Station] 3s per crop → washed crop 
  → [Juicer] 4s per crop → fills cup 
  → [Capper Station] 2s → lidded cup 
  → [Packager] 2s → packaged juice 
  → [Counter/Shelf] → customer picks up → [Register] → sale!
```

Each processing station:
- Has an `input_item` type it accepts
- Has an `output_item` type it produces
- Has a `process_time` in seconds
- Has a `progress` float (0.0 to 1.0) shown as a progress bar on the tile
- Can hold 1 item being processed + 1 item queued as input + 1 item ready as output
- Draws progress bar as a colored rectangle below the machine tile

Items on belts:
- Represented as small colored rectangles sliding across belt tiles
- Move at 1 tile per 2 seconds along belt direction
- At a grabber tile, the grabber arm picks up item and places it on the target tile
- Grabber has configurable input direction and output direction (set by player)

---

## Farming System

### Soil Tiles
- Player clicks soil tile to till it (changes visual)
- Click tilled soil with seed selected → plants seed
- Soil needs water: either player uses watering can (click water source to fill, click soil to water) or sprinkler covers 3x3 radius automatically
- Growth stages: dry → planted → growing (halfway) → ready (flashing)
- Growth time: 15 seconds base, 10s in greenhouse, 8s with sprinkler
- When ready: player clicks to harvest (adds raw crop to inventory) OR harvester arm picks it up automatically

### Player Inventory
- Player carries up to 6 item slots shown in bottom bar
- Click a tile to interact (harvest, water, deposit to machine, pick up from machine)
- Items can be manually carried from machine to machine
- This is the "manual play" mode — chaotic and fun

### Automation Unlocks (placed from build menu)
| Automation | Cost | Effect |
|---|---|---|
| Sprinkler | $50 | Waters 3x3 soil area every 10s |
| Harvester Arm | $120 | Picks ripe crops, drops to adjacent belt or crate |
| Belt (per tile) | $10 | Moves items in one direction |
| Grabber Arm | $80 | Transfers items between two adjacent tiles |
| Auto-Washer | $150 | Wash station runs without worker |
| Auto-Juicer | $200 | Juicer runs without worker |
| Smart Router | $250 | Belt that splits items between two outputs |
| Buffer Crate | $60 | Holds up to 8 items, auto-feeds to adjacent machine |

---

## Worker System

### Worker Types
| Type | Color | Role |
|---|---|---|
| Farmer | Orange circle | Tills, plants, waters, harvests |
| Stocker | Red circle | Moves items from crates to machines or shelves |
| Cashier | Cyan circle | Stands at register, serves customers |
| Engineer | Purple circle | Places belts and grabbers (auto-build mode) |

### State Machine (all workers share this base)
```
IDLE → find_task() → WALKING(path) → ARRIVE → WORKING(timer) → DONE → IDLE
```

Worker-specific tasks:
- **Farmer**: CheckSoil → WaterIfDry → HarvestIfReady → PlantIfEmpty → Idle
- **Stocker**: CheckCrates → PickUp → WalkToMachine → Deposit → Return
- **Cashier**: WalkToRegister → WaitForCustomer → ServeCustomer(2s) → CollectCash → WaitForCustomer
- **Engineer**: assigned tasks queue from player clicking belt/grabber placement

### Pathfinding
- A* on the tile grid
- Heuristic: Manhattan distance
- Impassable: wall tiles, machine tiles (except destination), other worker tiles
- Path cached, recalculated only when grid changes or new target assigned
- Workers move at 80px/second (2 tiles/second)
- Draw path as small dots in debug mode (toggle with F1)

### Hiring
- Costs $80 per worker
- Workers spawn at entrance tile
- Max 8 workers total
- Workers shown in right panel with name, type, current state, and task

---

## Customer System

### Spawning
- Customers spawn at entrance tile every 10-20 seconds (random, scales with day progression)
- Each customer is a white circle with a small order bubble above their head
- Order bubble shows item icon (juice cup) and quantity (1-3)

### Customer States
```
ENTER → WALK_TO_PRODUCT_AREA → WAIT_FOR_STOCK → WALK_TO_REGISTER → WAIT_IN_LINE → BEING_SERVED → EXIT_HAPPY
                                      ↓ (patience runs out)
                                  EXIT_ANGRY
```

### Patience
- Each customer has 40 seconds of patience shown as a shrinking colored bar above them
- Bar is green → yellow → red as patience depletes
- If patience hits 0: customer leaves, -10 score, log message
- Successful sale: +$8 to $20 depending on order size, +10 score per item

### Queue System
- Register tiles have a queue list
- Customers join the shortest queue
- Cashier serves front of queue, 2.5 seconds per customer
- If no cashier assigned to a register, customers wait indefinitely (increasing frustration)

---

## Automation Logic (Belts & Grabbers)

### Belt Tiles
- Directional: N, S, E, W (set when placed)
- Items placed on a belt slide to the next tile in that direction every 2 seconds
- If next tile is blocked (machine processing, full buffer), item waits
- Belt draws an arrow showing direction
- Belt animation: moving stripes in the belt direction (drawn with lines)

### Grabber Arms
- Placed on a tile, configured with: input_direction, output_direction
- Every 1.5 seconds: check input tile for item → pick up → place on output tile
- Draws as a small arm line from center pointing toward input, with a claw icon
- Cannot grab from machines that are mid-process
- Can grab from: belt tiles, buffer crates, machine output slots

### Build Mode
- Press B to toggle build mode
- Side panel shows all placeable tiles and machines
- Click to select tool, click grid to place
- Right-click to remove
- Cannot place on occupied tiles
- Shows ghost preview of placement under cursor
- ESC to cancel placement

---

## UI Layout

```
┌─────────────────────────────────────┬──────────────────┐
│                                     │  RIGHT PANEL      │
│         GAME VIEWPORT               │  (220px wide)     │
│         (scrollable map)            │                   │
│                                     │  [Cash / Score]   │
│                                     │  [Day / Time]     │
│                                     │  [Speed: 1x 2x 4x]│
│                                     │  [Orders list]    │
│                                     │  [Workers list]   │
│                                     │  [Event log]      │
├─────────────────────────────────────┴──────────────────┤
│  BOTTOM BAR (60px tall)                                  │
│  [Player inventory: 6 slots] [Build mode toggle] [Menu] │
└──────────────────────────────────────────────────────────┘
```

### Right Panel Details
- **Stats card**: Cash ($), Score, Day, Customers served
- **Speed buttons**: 1x / 2x / 4x — scales all timers and movement
- **Orders**: scrollable list, each showing quantity + patience bar
- **Workers**: each worker shown as colored dot + name + state + task
- **Event log**: last 8 events, newest on top, fade out after 10s
- **Build panel** (shown when B pressed): grid of all buildable items with cost

### Bottom Bar
- 6 inventory slots (40x40px each), selected slot highlighted
- Currently held item shown with count
- Seed selector: click to cycle seed type (only 1 seed type for now: fruit)
- Hotkeys: 1-6 for inventory slots

---

## Day/Night Cycle

- Each in-game day = 3 minutes real time (at 1x speed)
- Visual: sky color at top of screen shifts from light blue (day) to dark blue/orange (dusk) to dark (night)
- At night: no new customers spawn, workers return to a rest tile near entrance
- End of day: modal popup showing:
  - Juice sold: N units
  - Revenue: $X
  - Expenses: worker wages ($5 per worker per day)
  - Net profit: $X
  - Score: +points
  - "Next Day" button to continue
- Day counter increments, customer spawn rate increases slightly each day

---

## Progression & Economy

### Starting State
- $500 cash
- 1 Farmer worker (free)
- 9 soil tiles tilled
- 10 seeds in storage
- No automation — everything done manually

### Economy
- Juice sells for $12 per unit at register
- Seeds cost $2 each (bought from a "shop" button in UI)
- Workers cost $80 to hire, $5/day wage
- Automation items cost as listed above
- Goal: hit $5000 total to "win" day 30 challenge

### Upgrade Shop (UI button)
Simple modal with a list:
- Buy seeds (10x for $20)
- Hire worker (select type, $80)
- Buy automation item (select from list, place on map after purchase)
- Upgrade machine speed (Washer Mk2: processes in 1.5s instead of 3s, costs $200)

---

## Multiplayer Architecture (Design For It, Don't Implement Yet)

Structure the code so that the player character is abstracted as a `PlayerController` class. All player actions go through methods like `player.interact(tile)`, `player.move(dx, dy)`, `player.pickup()`, `player.drop()`. This makes it straightforward to add a second local player (WASD vs arrow keys) or network player later. Add a comment in the code: `# MULTIPLAYER: add second PlayerController here with arrow key bindings`

---

## Code Architecture

```python
# main.py structure

class AssetManager:
    # generates placeholder PNGs at startup
    # loads all assets into a dict keyed by filename
    # get(name) returns surface, falls back to colored rect if missing

class Config:
    # all constants: tile size, colors, speeds, costs, timings
    # change ASSET_MODE = 'placeholder' | 'sprites' to switch art

class Tile:
    # type, asset_name, walkable, entity, item, position

class Grid:
    # 2D array of Tiles
    # place_entity(), remove_entity(), get_neighbors(), is_walkable()
    # pathfind(start, end) → list of (x,y) waypoints using A*

class Item:
    # item_type, asset_name, quantity
    # types: RAW_CROP, WASHED_CROP, JUICE_CUP, JUICE_LIDDED, JUICE_PACKAGED, SEED

class Machine:
    # base class for all processing stations
    # input_type, output_type, process_time, progress, state
    # update(dt), draw(surface, camera)
    # subclasses: WashStation, Juicer, Capper, Packager

class Belt(Machine):
    # direction, move items along belt path

class GrabberArm(Machine):
    # input_dir, output_dir, grab_timer

class Sprinkler(Machine):
    # radius, water_timer, waters nearby soil

class HarvesterArm(Machine):
    # checks adjacent tiles for ripe soil, harvests, drops to belt

class Agent:
    # base class for workers and customers
    # position (float x,y), speed, path, state, asset_name
    # update(dt), draw(surface, camera)
    # move_along_path(dt), find_path(target)

class Worker(Agent):
    # type (FARMER/STOCKER/CASHIER/ENGINEER)
    # task_queue, current_task, inventory (1 item slot)
    # think() called each frame when IDLE — assigns self next task

class Customer(Agent):
    # order (list of items), patience, state
    # assigned_register

class Player(Agent):
    # inventory (6 slots), selected_slot
    # handle_input(events), interact(grid)

class Order:
    # items_needed, patience, reward, customer reference

class TaskQueue:
    # global list of pending tasks
    # add_task(task), get_best_task_for(worker)
    # task types: WATER_SOIL, HARVEST, PLANT, MOVE_ITEM, RESTOCK, SERVE_CUSTOMER

class Camera:
    # offset_x, offset_y, zoom
    # world_to_screen(x,y), screen_to_world(x,y)
    # pan(dx,dy), zoom_in/out

class UI:
    # draw_right_panel(), draw_bottom_bar(), draw_build_menu()
    # draw_order_list(), draw_worker_list(), draw_event_log()
    # draw_end_of_day_modal()
    # handle_click(pos) → returns action

class EventLog:
    # messages list with timestamps
    # add(message, color), draw(surface), prune old messages

class Game:
    # owns grid, workers, customers, player, camera, ui, task_queue
    # update(dt), draw(), handle_events()
    # spawn_customer(), end_of_day(), new_day()

# Entry point
if __name__ == '__main__':
    pygame.init()
    game = Game()
    game.run()
```

---

## Controls

| Key/Action | Effect |
|---|---|
| WASD | Pan camera |
| Scroll wheel | Zoom in/out |
| Middle mouse drag | Pan camera |
| Left click | Interact with tile / place building |
| Right click | Remove building / cancel |
| B | Toggle build mode |
| F1 | Toggle debug mode (show paths, tile coords, states) |
| 1-6 | Select inventory slot |
| ESC | Deselect tool / close modal |
| Space | Pause/unpause |

---

## Debug Mode (F1)

When enabled, draw on top of everything:
- Each tile's grid coordinate (tiny text)
- Each worker's current state and target tile (text above head)
- Each worker's A* path (series of small dots)
- Each machine's input/output item types and progress value
- FPS counter top-left
- Mouse tile coordinate top-right

---

## Implementation Notes for Codex

1. Generate all placeholder assets FIRST in `AssetManager.__init__()` before any game objects are created
2. Use `pygame.time.Clock` for delta time, cap at 60fps
3. Apply `game_speed` multiplier to ALL `dt` values passed to `update(dt)` calls
4. A* implementation: use a min-heap (`heapq`), Manhattan distance heuristic, cache results in a dict keyed by `(start, end)`, invalidate cache on grid change
5. Keep rendering and logic completely separate — `update()` never calls drawing functions
6. All money values are floats, displayed as `f"${value:.2f}"`
7. Every class should have a `__repr__` for easy debugging
8. Use `pygame.sprite.Group` for customers and workers for efficient collision/draw
9. Belt item movement: store items as `(item, progress_0_to_1)` tuples on each belt tile, advance progress each frame
10. Grabber arm animation: draw a line from tile center toward input_dir, length proportional to grab progress

---

## Deliverable Checklist

The finished code should demonstrate all of the following working:
- [ ] Map renders with farm and store zones clearly visible
- [ ] Camera pans and zooms smoothly
- [ ] Player can walk around, pick up items, deposit to machines
- [ ] Soil can be tilled, planted, watered, grown, harvested manually
- [ ] Full juice production chain works manually (player carries items between machines)
- [ ] Workers pathfind and do their jobs autonomously
- [ ] Customers spawn, order, wait, get served, leave happy or angry
- [ ] Belts move items between tiles
- [ ] Grabber arms transfer items between belt/machine tiles
- [ ] Sprinkler waters soil automatically
- [ ] Harvester arm picks ripe crops and drops to belt
- [ ] Build mode lets player place/remove all tile types
- [ ] UI shows all stats, orders, workers, log
- [ ] Day/night cycle with end-of-day summary
- [ ] Speed multiplier works correctly (2x and 4x modes)
- [ ] All placeholder assets generated and loaded from files
- [ ] Debug mode shows pathfinding and state info
