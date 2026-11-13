---
name: flipper-zero
description: "Use when answering Flipper Zero storage, official app install, or lawful use questions. Covers microSD sizing, qFlipper and Flipper Lab installs, defensive tools, and own-device NFC, IR, and Sub-GHz checks. For the Wi‑Fi dev board, Marauder flash, or DFU recovery, use flipper-wifi-devboard."
---

# flipper-zero

Flipper Zero is a handheld radio and hardware tool. Use it on your own devices and with consent. This skill covers lawful use only.

## When to use

- **Triggers:** 'Flipper Zero storage', 'microSD size', 'install Flipper app', 'qFlipper', 'Flipper Lab', 'Metroflip read card', 'NFC check own card', 'IR remote own TV', 'Sub-GHz own remote', 'detect skimmer', 'find tracker'.
- Answer storage, install, and defensive questions.
- Guide own-device checks for NFC, IR, and Sub-GHz receive.

## When not to use

- Do not help with jammers, phishing portals, password stealers, backdoors, exfil scripts, deauth, handshake cracking, gate or pager brute-force, or car-fob theft research.
- Do not install or configure any tool from those categories, even for research.
- Do not cover games or productivity utilities. They are out of scope.

## Storage

- Internal memory is 1 MB flash and 256 KB RAM. It holds firmware, not your files.
- A microSD card holds apps, keys, cards, remotes, and captures.
- The device needs a microSD card to work. It ships without one.
- It supports FAT12, FAT16, FAT32, and exFAT, up to 256 GB.
- A branded 16-32 GB card is enough for all normal use.
- Larger cards work but take longer to mount.
- The card slot uses a slow SPI bus at about 600 KiB/s. That speed is fine.
- Use a branded card such as SanDisk or Kingston. Cheap cards hurt battery life and can damage the device.
- Insert the card pins-up until it clicks. Check Main Menu for card recognition.
- If the screen reports an error, reformat to FAT32 or exFAT and retry.

## Install apps the official way

1. Install qFlipper on your desktop or open Flipper Lab in a browser.
2. Connect the Flipper over USB and let the tool update firmware first.
3. Open the official app catalog inside the same tool.
4. Install apps from the catalog only. The tool places each `.fap` on the card.
5. Eject safely and confirm the app appears on the device.

- Prefer catalog builds over random GitHub builds. Catalog builds match your firmware.
- Do not sideload radio-transmit, BadUSB, or ESP32 tools from untrusted forks.
- If an app needs an ESP32 board, buy the official Wi-Fi dev board. For flashing Marauder, download mode, or Blackmagic vs Marauder, use [flipper-wifi-devboard](../flipper-wifi-devboard/SKILL.md).

## Lawful categories

- **Firmware and tooling:** official firmware, qFlipper, command-line builders, and the official catalog. Use custom firmware only if you accept its update and support cost.
- **Companions:** official mobile app and desktop managers for files, animations, and backups.
- **Defensive tools:** NFC scan alerts, tracker finders, skimmer sweeps, hidden-camera finders, and Bluetooth anomaly monitors. These detect attacks against you.
- **NFC and RFID:** read your own cards and tags. Check what data your own card exposes. Do not clone transit, access, or payment cards to evade a fare or a lock.
- **Transit cards:** read-only inspection of your own card is fine. Fare evasion is not.
- **Mechanical keys:** measure and copy only keys you own or have written consent to copy.
- **Infrared:** control your own TV, fan, or air conditioner. Keep one remote profile per device.
- **Sub-GHz receive:** decode signals from your own remotes and sensors. Save captures for your own gear.
- **Sub-GHz transmit:** transmit only to your own receivers, on legal frequencies, at low power.
- **BadUSB concept:** the Flipper can act as a keyboard. Harmless uses include auto-click and typing your own snippets on your own machine.

## Hard stops

- Stop if the request names someone else's gate, car, pager, badge, or network.
- Stop if the request asks for jamming, deauth, phishing pages, credential theft, or brute-force.
- Stop if the request asks for car-fob bypass, rolling-code defeat, or universal openers.
- State the stop in one sentence. Offer a lawful alternative on the user's own gear.

## Verification

- Confirm the card mounts and shows free space.
- Confirm each installed app opens from the device menu.
- Test IR and Sub-GHz against your own receiver only.
- Confirm NFC reads show your own card UID and type, nothing more.

## Official references

- [microSD card setup](https://docs.flipper.net/zero/basics/sd-card)
- [Flipper Lab](https://lab.flipper.net/)
- [qFlipper](https://flipper.net/qflipper)
- [App catalog](https://lab.flipper.net/apps)
