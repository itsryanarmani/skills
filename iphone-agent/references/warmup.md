# Warmup recipes

Social media account warmup via the ESP32 iPhone agent. Uses the scripts in
[`itsryanarmani/scripts`](https://github.com/itsryanarmani/scripts).

Every session is **different** — random action order, varied scroll distances,
human-like pauses, tap jitter. No two runs are identical.

## Platforms available

| App | Script | Coords (Social folder pg 1) |
|-----|--------|------|
| Instagram | `warmup-instagram` | (0.74, 0.36) |
| TikTok | `warmup-tiktok` | (0.50, 0.48) |
| X | `warmup-x` | (0.50, 0.59) |
| LinkedIn | `warmup-linkedin` | (0.27, 0.48) |
| YouTube | `warmup-youtube` (via Safari) | Safari dock (0.62, 0.93) |

## Basic warmup

```bash
# One round of each
warmup-instagram --rounds 1
warmup-tiktok --rounds 2
warmup-x --rounds 3
warmup-linkedin --rounds 2
warmup-youtube --rounds 1
```

## Fast mode

```bash
# Run all platforms fast (minimal pauses)
warmup --auto --rounds 2
```

## Duration mode

```bash
# Let it run in the background for 10 minutes
warmup-tiktok --duration 10m &
```

## Before each round

1. The phone must be unlocked and on the Home Screen.
2. The ESP32 must be on and serving on port 8890.
3. Coordinate jitter ensures taps are never exact.

## Gates

No account creation or post publishing yet. These scripts:
- Scroll feeds ✓
- Like posts ✓
- Leave comments ✓
- Read/send DMs ✓
- Follow accounts ✓
- Watch stories/shorts ✓
- Search topics ✓

These still need frame-by-frame pixel mapping:
- Publish posts (needs media picker)
- Create content
- Account signup/sign-in