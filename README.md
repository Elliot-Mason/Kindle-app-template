# Kindle App Template

A clean, modular starter template for creating web applications optimized for the **Amazon Kindle Paperwhite (1st Gen, EY21, Firmware 5.6.1.1)** and compatible with [Kindle-simulator](https://github.com/Elliot-Mason/Kindle-simulator).

## Features
- **Strict ES5 Compatibility:** Works natively inside the Kindle Experimental Browser (no WebPack or Babel required).
- **High-Contrast E-Ink Typography:** Pre-styled 1-bit / grayscale layout with tactile touch-inverted buttons.
- **Kindle Hardware Header:** Built-in live clock, E-Ink ghosting flash refresh, and status indicator.
- **Simulator Compatible:** Plug-and-play with `Kindle-simulator` using `--app` or the `apps/` directory.

---

## Quick Start (Standalone Mode)

1. Copy the example configuration:
   ```bash
   cp config.example.json config.json
   ```
2. Start the local server:
   ```bash
   python server.py
   ```
3. Open on your PC at `http://localhost:5053/kindle` or point your Kindle's Experimental Browser to your computer's LAN IP displayed in the terminal:
   ```
   http://192.168.0.x:5053/kindle
   ```

---

## Running Natively on a Jailbroken Kindle (No PC Needed)

You can run this app template directly on your Kindle with **zero external PC or server running**:

### Prerequisites
1. **Jailbroken Kindle Paperwhite 1** (FW 5.6.1.1 or similar).
2. **KUAL** (Kindle Unified Application Launcher) installed.
3. **Python 3** installed on Kindle (install NiLuJe's `python3` package via MRPI or KUAL from the MobileRead forum).

### Installation Steps
1. Connect your Kindle to your computer via USB.
2. Copy this entire folder into the Kindle's `extensions` directory:
   ```
   [Kindle USB Root]
     └── extensions/
         └── my-app/               <-- Copy this repo here
             ├── config.xml
             ├── menu.json
             ├── bin/launcher.sh
             ├── server.py
             ├── kindle.html
             └── config.json       (copy from config.example.json)
   ```
3. Copy `config.example.json` to `config.json`.
4. Safely eject and unplug the USB cable.

### Launching on the Kindle
1. On your Kindle home screen, tap **KUAL**.
2. Select **Kindle App Template** &rarr; tap **Start (Standalone On-Device)**.
3. The launcher will automatically:
   - Prevent screensaver/sleep timeout (`preventScreenSaver = 1`).
   - Launch `python3 server.py` in the background on `127.0.0.1:5053`.
   - Open the Kindle Experimental Browser directly to `http://127.0.0.1:5053/kindle`.
4. Your application will now run completely standalone!

### Stopping the App
Open **KUAL** &rarr; **Kindle App Template** &rarr; **Stop App & Re-enable Sleep**.

---

## Testing in Kindle Simulator

To preview this app inside the [Kindle-simulator](https://github.com/Elliot-Mason/Kindle-simulator) with simulated E-Ink Pearl ghosting and 212 PPI scaling:

```bash
python /path/to/Kindle-simulator/server.py --app .
```

---

## Project Structure

```
Kindle-app-template/
├── config.xml             # KUAL extension manifest for jailbroken Kindle
├── menu.json              # KUAL on-device menu definition
├── bin/
│   └── launcher.sh        # On-device background daemon & browser launcher
├── kindle-app.json        # App manifest (id, name, icon, port)
├── server.py              # Lightweight Python backend (standard library only)
├── kindle.html            # E-Ink layout with ES5 touch controls
├── config.example.json    # Safe template configuration
└── config.json            # Local user settings (git-ignored)
```

## E-Ink Pearl Best Practices
- **Use pure black (`#000000`) and pure white (`#ffffff`):** High contrast maximizes readability on E-Ink Pearl screens without frontlight glare.
- **Touchable button size:** Minimum 48px height and bold 2.5px+ borders for responsive infrared touch registration.
- **JavaScript restrictions:** Kindle PW1 running FW 5.6.1.1 does not support ES6 (`const`, `let`, `=>`, or `async/await` in browser code). Use standard ES5 `var`, `function()`, and `XMLHttpRequest`.
