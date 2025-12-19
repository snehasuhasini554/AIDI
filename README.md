# AIDI Companion

AIDI is your sticky blue koala productivity buddy: Pomodoro, motivational AI chat, achievements, mood boosters, skins, and more.

## Screenshots

<div align="center">
  <img src="screenshots/01_idle_state.png" alt="AIDI companion showing idle state with blue koala character and 25:00 Pomodoro timer" width="200"/>
  <img src="screenshots/02_timer_running.png" alt="AIDI showing active Pomodoro timer countdown at 24:35 in Focus Mode" width="200"/>
  <img src="screenshots/03_break_mode.png" alt="AIDI in Break Mode with timer at 04:52 and achievement star badge" width="200"/>
</div>

<div align="center">
  <img src="screenshots/04_with_achievement.png" alt="AIDI with fire achievement badge after completing multiple Pomodoro sessions" width="200"/>
  <img src="screenshots/05_paused_state.png" alt="AIDI in paused state showing timer at 15:42 with paused status label" width="200"/>
</div>

*AIDI companion states: idle → focus mode → break → achievements → paused*

For more details about each screenshot, see the [screenshots](screenshots/) directory.

## Features

- Floating koala with Pomodoro timer
- Distraction/Afk detection, achievements, and stats
- Gen-Z assistant chat (offline: Ollama / cloud: HuggingFace)
- Custom mood boosters, affirmations, music suggestions
- Koala character skin selector
- System tray, keyboard shortcuts, accessibility
- Installable package (pip install .), one-click launch

## Installation

```bash
pip install .
aidi-companion
```

## Customization

- Add PNG/GIF koala images to `aidi/skins/`
- Add affirmations/music in "Mood Booster Settings"

## License

MIT (see LICENSE)