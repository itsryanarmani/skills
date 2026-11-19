---
name: flipper-wifi-devboard
description: "Flipper Zero official Wi‑Fi dev board (ESP32‑S2): Blackmagic vs Marauder, safe Marauder flash from a computer (download mode BOOT/RESET), qFlipper DFU recovery on the main unit, daily use with the companion app, and what not to flash. Lawful lab Wi‑Fi only. Use for Wi‑Fi dev board, Marauder flash, ESP Flasher, Blackmagic, or stuck DFU after radio recovery."
---

# flipper-wifi-devboard

The Wi‑Fi Developer Board is an **ESP32‑S2 add‑on**. It is **not** built‑in Flipper Wi‑Fi.
Flash **only the board** for Marauder; never push Marauder through qFlipper **radio /
core2radio / recovery** on the Flipper itself — that targets the Bluetooth coprocessor and
can leave the Flipper in **DFU** (blank screen).

Automation helper: [pooriaarab/scripts `flash-marauder.sh`](https://github.com/pooriaarab/scripts/tree/main/scripts/flipper-wifi-devboard).

## When to use

- Wi‑Fi dev board, Marauder, ESP32 Marauder app, ESP Flasher, Blackmagic firmware.
- Flipper works but board shows **Blackmagic ESP32** on USB and Marauder app won’t connect.
- **DFU in FS Mode** on the Flipper after a failed wireless stack update.

## Hard stops

- No deauth, jamming, evil portal, or credential capture on networks the user does not own
  or lacks permission to test.
- No qFlipper `core2radio`, `marauder_flipper.bin`, or wireless recovery images on the
  **Flipper** — board flash only.
- No `wipe` / `erase` on Flipper internal memory unless the owner explicitly requests it.

## Blackmagic vs Marauder (same chip, one firmware at a time)

| Firmware | USB name (typical) | Use |
|----------|-------------------|-----|
| **Blackmagic** (stock) | Blackmagic ESP32 | PC Wi‑Fi debugging; not the Marauder Flipper app |
| **Marauder** | After flash, normal app use on Flipper | Flipper companion app + Wi‑Fi toolkit on the board |

Switch by **reflashing the board** only. Flipper SD data stays.

## Flash Marauder — computer only, Flipper aside

1. **USB from dev board → computer** (not stacked on Flipper).
2. **Download mode** (pick one):
   - **A:** Hold **BOOT** → tap **RESET** → keep holding BOOT **~10s** → release.
   - **B:** Unplug USB → hold **BOOT** → plug USB while holding → hold **5–10s** → release.
3. **macOS USB hint:** Blackmagic → **`ESP32-S2`** and serial port often renames (e.g.
   `cu.usbmodem01`). Flash **immediately**; the window is short.
4. Run `scripts/flipper-wifi-devboard/flash-marauder.sh` from
   [pooriaarab/scripts](https://github.com/pooriaarab/scripts) (**omit `--port`** so it
   re-scans, unless you know the post‑download port).
5. **RESET** on board → unplug USB → stack on Flipper → **Apps → GPIO → ESP32 Marauder**
   (install from catalog if missing).

**Option B — no laptop esptool:** Put four `.bin` files on SD under `apps_data/esp_flasher/`,
board download mode, **Apps → GPIO → ESP Flasher → Manual Flash**.

Official asset: Marauder release file ending in **`_flipper.bin`**.

## Flipper stuck in DFU (main unit, not the board)

Symptom: blank screen, USB **DFU in FS Mode** / `PID_df11`.

1. Remove Wi‑Fi board from Flipper.
2. qFlipper **Firmware Update / Repair** (CLI with no args or app) — **not** wipe/erase.
3. Confirm device returns as normal Flipper USB, not DFU.

Preserve SD card; optional `qFlipper-cli backup` for internal storage if available.

## Daily use (after Marauder)

1. Stack board on Flipper GPIO; **no USB** for normal use.
2. Wake Flipper → Marauder companion app → wait for connect (can take 10–30s).
3. Sub‑GHz / NFC / IR on the Flipper work as before; only ESP32 apps use the board.

## Verification

- After board flash: companion app connects after reseat or reboot.
- After Flipper repair: boots with screen; qFlipper shows normal firmware, not DFU.
- Offensive Wi‑Fi actions only described for **owned lab** networks.

## References

- [Flipper wiki — Marauder guide](https://flipper.wiki/tutorials/Marauder_guide/guide/)
- [ESP32Marauder releases `_flipper.bin`](https://github.com/justcallmekoko/ESP32Marauder/releases)
- [pooriaarab/scripts flipper-wifi-devboard README](https://github.com/pooriaarab/scripts/blob/main/scripts/flipper-wifi-devboard/README.md)
