"""
Directly run NarutoScript with a specified config file, bypassing the GUI.

Usage:
    python run_config.py <config_name>    e.g. python run_config.py 1-RiZhouHuo
    python run_config.py <index>          e.g. python run_config.py 1
    python run_config.py                  List available configs and choose

Config files are expected at ./config/<config_name>.json
"""

import glob
import os
import signal
import sys


def list_configs():
    """List all available config files in the config/ directory."""
    config_files = glob.glob("config/*.json")
    configs = []
    for f in config_files:
        name = os.path.splitext(os.path.basename(f))[0]
        # Skip template configs (they are templates, not runnable configs)
        if name.startswith("template"):
            continue
        configs.append(name)
    return sorted(configs)


def resolve_config_name(arg: str) -> str:
    """
    Resolve the config name from user input, which can be:
    - A full config name (e.g. "1-日周活")
    - A numeric index into the sorted config list (1-based)
    """
    configs = list_configs()

    if not configs:
        print("[NarutoScript] ERROR: No config files found in config/ directory")
        sys.exit(1)

    # Try numeric index first
    try:
        index = int(arg) - 1  # Convert to 0-based
        if 0 <= index < len(configs):
            return configs[index]
        else:
            print(f"[NarutoScript] ERROR: Config index {arg} is out of range (1-{len(configs)})")
            print()
            print("Available configs:")
            for i, c in enumerate(configs, 1):
                print(f"  [{i}] {c}")
            sys.exit(1)
    except ValueError:
        pass

    # Try exact match
    config_path = f"config/{arg}.json"
    if os.path.exists(config_path):
        return arg

    # Not found - show available configs
    print(f"[NarutoScript] ERROR: Config file not found: config/{arg}.json")
    print()
    print("Available configs:")
    for i, c in enumerate(configs, 1):
        print(f"  [{i}] {c}")
    sys.exit(1)


def show_and_choose():
    """Show available configs and let the user choose interactively."""
    configs = list_configs()
    if not configs:
        print("[NarutoScript] ERROR: No config files found in config/ directory")
        sys.exit(1)

    print("Available configs:")
    for i, c in enumerate(configs, 1):
        print(f"  [{i}] {c}")

    print()
    try:
        choice = input("Enter config number (or name): ").strip()
    except (EOFError, KeyboardInterrupt):
        print("\n[NarutoScript] Cancelled")
        sys.exit(0)

    if not choice:
        print("[NarutoScript] Cancelled")
        sys.exit(0)

    return resolve_config_name(choice)


def launch_gui(arg=1):
    """
    Resolve config by index/name and launch the web GUI with auto-run.
    Called from start.bat with a numeric index (no Chinese in batch).

    Usage:
        python -c "from run_config import launch_gui; launch_gui(1)"
    """
    config_name = resolve_config_name(str(arg))
    print(f"[NarutoScript] Launching GUI with config: {config_name}")
    import subprocess
    subprocess.run([sys.executable, "gui.py", "--run", config_name])


def main():
    if len(sys.argv) < 2:
        config_name = show_and_choose()
    else:
        config_name = resolve_config_name(sys.argv[1])

    config_path = f"config/{config_name}.json"

    print(f"[NarutoScript] Starting with config: {config_name}")
    print(f"[NarutoScript] Config file: {config_path}")
    print("[NarutoScript] Press Ctrl+C to stop")
    print()

    from src import StarRailCopilot

    src = StarRailCopilot(config_name=config_name)

    # Handle Ctrl+C gracefully
    def signal_handler(sig, frame):
        print("\n[NarutoScript] Interrupted by user, exiting...")
        sys.exit(0)

    signal.signal(signal.SIGINT, signal_handler)

    try:
        src.loop()
    except KeyboardInterrupt:
        print("[NarutoScript] Stopped by user")
    except SystemExit:
        pass


if __name__ == "__main__":
    main()
