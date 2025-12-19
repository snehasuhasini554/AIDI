# AIDI Demo Screenshots

This directory contains demo screenshots showcasing the AIDI Companion application features.

## Screenshots

### 1. Idle State (`01_idle_state.png`)
The default state of AIDI showing the blue koala companion with the Pomodoro timer set to 25:00 and control buttons (play, pause, reset).

### 2. Timer Running (`02_timer_running.png`)
AIDI in Focus Mode with the timer actively counting down (24:35). The "Focus Mode" status label is visible at the top.

### 3. Break Mode (`03_break_mode.png`)
AIDI during a break period with the timer showing remaining break time (04:52). Shows "Break!" status label and an achievement star (⭐) indicating a completed Pomodoro session.

### 4. With Achievement (`04_with_achievement.png`)
AIDI displaying an achievement badge (🔥) after completing multiple Pomodoro sessions. Timer is reset to 25:00.

### 5. Paused State (`05_paused_state.png`)
AIDI with a paused timer (15:42) showing the "Paused" status label.

## Features Demonstrated

- 🐨 Cute blue koala companion character
- ⏱️ Pomodoro timer (25-minute focus, 5-minute break)
- ▶️ Simple control buttons (Play, Pause, Reset)
- 📊 Status indicators (Focus Mode, Break, Paused)
- 🏆 Achievement badges for completed sessions
- 🎨 Clean, rounded UI with soft colors and shadows

## Regenerating Screenshots

To regenerate these screenshots, you'll need to create a script that:
1. Initializes a PyQt5 application with the AIDI window
2. Programmatically changes the UI state (timer values, status labels, achievement badges)
3. Uses `QWidget.grab()` to capture screenshots
4. Runs with `QT_QPA_PLATFORM=offscreen` for headless rendering

Example structure:
```python
QT_QPA_PLATFORM=offscreen python3 your_screenshot_script.py
```
