# Description

This is a hack to get bHaptics working with OpenMW v0.48 with a Python wrapper.

1. Run OpenMW and capture the prints
    - OpenMW is running a new Lua script to print certain events, such as the player taking damage, that will be captured in the Python wrapper
2. Setup connection to the bHaptics local server using a WebSocket protocol
    - Tested using bHaptics v1.8.2.2
3. Register of all of the pre-defined .tact files
    - .tact files sourced, without modification, from Shizof's work (https://www.nexusmods.com/skyrimspecialedition/mods/24486)
4. Parse the print statements generated by the Lua script running in OpenMW to know what events are occurring
5. Send a JSON-like payload to the bHaptics server defining the type of haptic feedback and modifications to intensity and duration if needed

# Installation
1. Install OpenMW v0.48+ (any version w/ Lua scripting support should work), but you'll probably want the VR version (https://gitlab.com/madsbuvi/openmw)
2. Install bHaptics (https://www.bhaptics.com/support/downloads), **which unforunately is Windows only for desktop computer users**
3. Sync your bHaptics device(s) with the bHaptics app. I only have the vest, so I can't test the other devices.
4. Place this repo somewhere, for example `C:\Users\<USERNAME>\Documents\openMW_bhaptics`
5. Add the following lines to `openmw.cfg`, likely the one in `C:\Users\<USERNAME>\Documents\My Games\OpenMW`

    `data="C:\Users\<USERNAME>\Documents\openMW_bhaptics\lua"` <- Match the path to where you placed this repo (step 4)
  
    `content=bHaptics.omwscripts`

# Usage

1. Open up `config.json` in your favorite text editor
    - Point `openMW_exe_path` to the full filepath of the OpenMW executable binary (VR or otherwise)
    - Change `bHaptics_URI` if you have a non-standard URI for the bHaptics server
    - Change `intensity` and `duration` under `health` and `magicka` to taste, 1.0 is the default
    - Set `dynamic_scaling` under `health` and `magicka` to `true` to enable haptic feedback intensity to be adjusted dependent on how much health you lost or magicka used for a spell (percentage of base values)
    - Change `tact_directory` to point to the directory where you have the .tact files if you are not using the default directory
    - Change `tact_files` under `health` and `magicka` if you've got a different set of .tact files you want to use
2. Run the Python Wrapper instead of `openmw.exe`. You can still use the launcher to change settings; just don't actually launch it from there. **It needs to be in the same directory as `config.json`.**
    - Use the provided Windows 64-bit binary executable file or
      - https://github.com/SiftingSands/openMW_bhaptics/releases/tag/v0.2 -> download `wrapper.exe`
    - Run this in your own Python environment or
      - Install https://websockets.readthedocs.io/en/stable/index.html (aka `pip install websocket-client`)
    - Build your own binary executable file
      - I used `python -m PyInstaller wrapper.py --onefile`

# Limitations

1. Haptic feedback for damage to the player and spell casting is randomly picked out from a series of patterns. I don't know how to get more relevant details from OpenMW, such as what type of spell cast or type of weapon used to damage the player. I think projectile collision with the player is possible? Just let your brain resolve the disparity.
2. With `dynamic_scaling` turned on. Set your health to a very high level and get attacked by a swarm of enemies doing low amounts of damage. Try to cast a big spell, and the haptic feedback of the spell is dampened by all of the send request to the bHaptics server from the low damage attacks.
3. Heartbeat on low health not implemented (yet?)
4. No haptic feedback on player weapon attacks (melee nor ranged), blocks, swimming, teleporting, weather, or opening containers
5. I can't seem to detect health and magicka fortification in OpenMW's Lua scripting, so `dynamic_scaling` always works off the base values. `dynamic_scaling` also only affects intensity and not duration of haptics.
6. No MCM to customize settings, because I would have to read those into the Python wrapper. Definitely doable, just not ideal because there would be two places to configure settings.
7. I don't notice any latency between the haptic feedback and the event that triggered it with this Python wrapper. Your results may vary on less powerful hardware (but PC VR typically means you've got some beefy hardware).
8. I had never written a single line of Lua or even looked at OpenMW's codebase 48 hours ago, so expect bugs.

# License

All files except for Shizof's .tact files are under the MIT license

# Acknowledgements

- The OpenMW team and Mads (https://gitlab.com/madsbuvi) for the VR implementation
  - Getting off the boat at Seyda Neen in VR was a tidal wave of nostalgia
- Shizof for the .tact files and existence proof of bHaptics on Skyrim VR
- GitHub Copilot for being my intelligent auto-complete on the boilerplate
