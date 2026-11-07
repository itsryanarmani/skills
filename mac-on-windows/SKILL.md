---
name: mac-on-windows
description: "Make a Windows host feel like macOS for someone whose muscle memory is Mac — Cmd-based shortcuts, emacs text navigation, Spotlight, Quick Look, Mission Control and Spaces, screenshots. Starts by detecting the input topology, because whether Command arrives as Win or as Alt decides the entire keymap and is the one thing that cannot be guessed. Carries the ceilings honestly: Win+L is uninterceptable without a policy change, AutoHotkey's AltTab action accepts exactly one L/R-qualified modifier, and a Magic Trackpad behind a KVM forwards no multi-touch at all — gestures need the trackpad paired directly to Windows, or a BetterTouchTool gesture-to-keystroke relay."
---

# Mac on Windows

Use when someone works primarily on a Mac and wants a Windows machine to stop
fighting their muscle memory — usually a second desktop, a work-issued PC, or a
box driven over a software KVM.

## Triggers

- "make Windows behave like a Mac", "Mac keyboard shortcuts on Windows"
- "Cmd+C doesn't work", "I keep hitting the wrong key"
- "Magic Trackpad gestures on Windows", "three-finger swipe"
- "Spotlight on Windows", "Quick Look on Windows"

---

## Phase 0 — Detect the input topology first

Everything downstream depends on **which physical key the Mac's Command lands
on**, and that cannot be guessed. Three topologies produce three different
answers:

| Topology | Command arrives as | Notes |
|---|---|---|
| Apple keyboard paired directly to Windows, no Boot Camp drivers | **Win** | Option lands on Alt |
| Apple keyboard with Boot Camp / Magicoft drivers | often **Alt** | drivers swap Cmd/Option to match PC layout |
| Mac drives Windows over Deskflow / Synergy / Barrier | **Win** | KVM maps Cmd → super → `VK_LWIN` |

Detect it rather than assuming:

```powershell
# Is a KVM client running here?
Get-CimInstance Win32_Process -Filter "Name like 'deskflow%' or Name like 'synergy%'" |
    Select-Object Name, CommandLine
# 'client' in the command line means the keyboard is on the OTHER machine.

# What input hardware is actually attached?
Get-PnpDevice -PresentOnly |
    Where-Object { $_.Class -in 'Keyboard','Mouse','HIDClass' -and $_.FriendlyName -match 'Apple|Magic' }
```

If no Apple hardware is present locally but a KVM client is running, the Mac is
upstream and **Command arrives as Win**.

Confirm before writing a keymap. A one-line AutoHotkey probe settles it:

```ahk
#Requires AutoHotkey v2.0
~*LWin::ToolTip "Win"
~*LAlt::ToolTip "Alt"
```

## Phase 1 — The keymap

Map Command from **Win**, and leave **Ctrl and Alt untouched**. This is the
choice that makes everything else fall into place:

- a locally attached PC keyboard keeps behaving like normal Windows
- Ctrl becomes genuinely free, so it can carry macOS's system-wide emacs text
  navigation (`Ctrl+A/E/B/F/N/P/D/H/K`) — which is exactly how a Mac splits the
  two modifiers

A working, commented implementation lives at
[`itsryanarmani/scripts/scripts/mac-keys-windows`](https://github.com/itsryanarmani/scripts/tree/main/scripts/mac-keys-windows).
Prefer it over PowerToys Keyboard Manager, which is not context-aware and will
happily break Alt+Tab and terminal keys with a blanket swap.

Generate the bulk of the bindings rather than hand-writing 40 hotkeys:

```ahk
Pass(keys) => Send("{Blind}{LWin up}{RWin up}" keys)   ; drop Win, keep Shift
CmdOf(t)   => (*) => Pass("^" t)
for key in StrSplit("abdefgijklnoprstuwxyz1234567890,./;=-")
    try Hotkey("*#" key, CmdOf(key))
```

`{Blind}` is what makes one hotkey per key sufficient: it preserves a
physically-held Shift, so `Cmd+Shift+Z` arrives as `Ctrl+Shift+Z` for free.

**Exclude terminals from the Ctrl bindings.** Check the active process against a
list and bail out — `Ctrl+C` must stay an interrupt, `Ctrl+A` is the tmux
prefix. Inside terminals map `Cmd+C`/`Cmd+V` to `Ctrl+Shift+C`/`Ctrl+Shift+V`,
which is the same trick Terminal.app plays.

## Phase 2 — The rest of the desktop

| macOS | Windows |
|---|---|
| Spotlight | PowerToys Run — read its hotkey from `%LOCALAPPDATA%\Microsoft\PowerToys\PowerToys Run\settings.json` (`open_powerlauncher`) and relay Cmd+Space to it, rather than editing PowerToys config |
| Quick Look | QuickLook (`winget install QL-Win.QuickLook`) — spacebar preview, no configuration needed |
| Mission Control | `Win+Tab`, bound to `Ctrl+Up` |
| Spaces | `Win+Ctrl+←/→`, bound to `Ctrl+←/→` |
| Screenshots | `Win+PrintScreen`, `Win+Shift+S`, `Win+Alt+R` |
| Finder | the Files app, or Explorer with QuickLook |

Skip macOS *theming*. The credible options are paid (Stardock Curtains) or deep
shell hooks (MyDockFinder), and UxTheme patchers break on Windows updates. Say
so rather than installing one unasked.

## Phase 3 — Trackpad gestures, and their real ceiling

This is where expectations need managing early. **A software KVM forwards mouse
motion, buttons, scroll and clipboard — not multi-touch.** Deskflow, Synergy and
Barrier all interpret gestures on the machine the trackpad is attached to. A
three-finger swipe on a Mac-attached Magic Trackpad triggers Mission Control *on
the Mac* and nothing crosses the wire.

There are exactly two ways forward, and they are mutually exclusive:

**A. Pair the Magic Trackpad directly to Windows.** Install
[mac-precision-touchpad](https://github.com/imbushuo/mac-precision-touchpad),
which exposes a Magic Trackpad 2 as a Windows Precision Touchpad. Real
multi-touch: two-finger scroll, pinch zoom, three-finger swipe for Task View and
app switching, four-finger for Spaces, all configurable under
Settings → Bluetooth & devices → Touchpad. This is the only path to something
close to full parity. Costs: the trackpad now drives Windows only, Bluetooth
pairs to one host at a time, and the driver is community-signed so installation
needs an explicit trust prompt.

**B. Keep the trackpad on the Mac and relay gestures as keystrokes.** Use
BetterTouchTool on the Mac to bind each gesture to a keyboard shortcut, which
the KVM forwards like any other key, and map that shortcut on the Windows side.
Discrete gestures only — three-finger swipes work, continuous ones (pinch zoom,
smooth swipe tracking) do not, because there is no gesture stream to interpolate.

Do not promise parity through a KVM. Establish which of A or B the user wants
before building anything, because they imply different hardware setups.

## Gotchas

- **`Win+L` cannot be hooked.** Windows reserves it below any keyboard hook, so
  `Cmd+L` locks the screen instead of focusing the address bar. The only fix is
  `DisableLockWorkstation=1` under
  `HKCU\Software\Microsoft\Windows\CurrentVersion\Policies\System`. Offer it as
  an opt-in and move locking to `Cmd+Ctrl+Q`, the real macOS shortcut.
- **AutoHotkey's `AltTab` action takes exactly one L/R-qualified modifier.**
  `#Tab::AltTab` fails with *"must specify which key (L or R)"*;
  `<#<+Tab::ShiftAltTab` fails with *"must have exactly one modifier/prefix"*.
  Spell out `<#Tab` and `>#Tab`, and drive the reverse direction by hand:

  ```ahk
  *#+Tab:: {
      if GetKeyState("Alt")                        ; switcher already open
          Send "{Blind}{LWin up}{RWin up}{Tab}"    ; Shift held -> backwards
      else
          Send "{LWin up}{RWin up}{Shift up}!+{Tab}"
  }
  ```

- **A backtick hotkey needs a scan code.** Backtick is AutoHotkey's escape
  character, so `Cmd+\`` must be written `#SC029`.
- **`/validate` is not a v2.0 switch.** Passing it runs the script instead of
  checking it. To verify a load, launch it, wait, and look for a `#32770`
  dialog owned by the AutoHotkey process; `PrintWindow` captures the message
  even when the dialog is behind another window.
- **Scroll direction through a KVM is already inverted.** macOS applies natural
  scrolling before the KVM forwards the delta, so Windows usually receives the
  right direction. The `FlipFlopWheel` registry trick will not help either way —
  it acts on HID drivers, and KVM input is injected. Provide a runtime toggle.
- **Ship a panic switch.** A global keymap that misfires is unusable and
  un-fixable by keyboard. Bind suspend to a combination that survives the remap
  (`Ctrl+Alt+F12`) and expose it in the tray menu.

## What is genuinely unavailable

The global menu bar, and app-level `Cmd+Q` quit semantics — Windows closes
windows, it has no concept of a running app with no windows. Say this up front
instead of approximating it badly.
