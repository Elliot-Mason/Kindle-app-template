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

## Testing in Kindle Simulator

To preview this app inside the [Kindle-simulator](https://github.com/Elliot-Mason/Kindle-simulator) with simulated E-Ink Pearl ghosting and 212 PPI scaling:

```bash
python /path/to/Kindle-simulator/server.py --app .
```

---

## Project Structure

```
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
