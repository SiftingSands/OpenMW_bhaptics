from subprocess import Popen, PIPE, STDOUT
from pathlib import Path
import re
import json
import random
import asyncio
import websockets

def register_tact(key:str, tact_filepath:str):
    tact_data = json.load(open(tact_filepath))
    # reshape the tact data to match the websocket payload
    payload = {
        "Register": [
            {
            "Key": key,
            "Project": {
                "Tracks": tact_data["project"]["tracks"],
                "Layout": tact_data["project"]["layout"]
            }
        }
        ]
    }
    return json.dumps(payload)

def submit_payload(key:str, scale_option:dict):
    # rotation is currently out of scope
    rotation_option = {"offsetAngleX": 0, "offsetY": 0}
    payload = {
        "Submit": [
            {
                "Type": "key",
                "Key": key,
                "Parameters": {
                    "altKey": "alt",
                    "rotationOption": rotation_option,
                    "scaleOption": scale_option
                }
            }
        ]
    }
    return json.dumps(payload)

async def main(config, process):
    URI = config['bHaptics_URI']
    async with websockets.connect(URI, compression=None) as websocket:
        # first register all of the tact files
        tact_folder = Path(config['tact_directory'])
        health_tact_files = config['health']['tact_files']
        for health_tact_file in health_tact_files:
            fullpath = tact_folder.joinpath(health_tact_file)
            await websocket.send(register_tact(health_tact_file, fullpath))

        magicka_tact_files = config['magicka']['tact_files']
        for magicka_tact_file in magicka_tact_files:
            fullpath = tact_folder.joinpath(magicka_tact_file)
            await websocket.send(register_tact(magicka_tact_file, fullpath))

        # these tact files don't have other options
        # TODO : add duration and intensity options to these tact files
        await websocket.send(register_tact("UnequipCuirass_1", tact_folder.joinpath("UnequipCuirass_1.tact")))
        await websocket.send(register_tact("UnequipGauntlets_1", tact_folder.joinpath("UnequipGauntlets_1.tact")))
        await websocket.send(register_tact("UnequipHelmet_1", tact_folder.joinpath("UnequipHelmet_1.tact")))
        await websocket.send(register_tact("UnequipClothing_1", tact_folder.joinpath("UnequipClothing_1.tact")))
        await websocket.send(register_tact("UnholsterArrowLeftShoulder_1", tact_folder.joinpath("UnholsterArrowLeftShoulder_1.tact")))

        await websocket.send(register_tact("EquipCuirass_1", tact_folder.joinpath("EquipCuirass_1.tact")))
        await websocket.send(register_tact("EquipGauntlets_1", tact_folder.joinpath("EquipGauntlets_1.tact")))
        await websocket.send(register_tact("EquipHelmet_1", tact_folder.joinpath("EquipHelmet_1.tact")))
        await websocket.send(register_tact("EquipClothing_1", tact_folder.joinpath("EquipClothing_1.tact")))

        await websocket.send(register_tact("ConsumableDrink_1", tact_folder.joinpath("ConsumableDrink_1.tact")))
        await websocket.send(register_tact("ConsumableFood_1", tact_folder.joinpath("ConsumableFood_1.tact")))

        await websocket.send(register_tact("FallEffect_1", tact_folder.joinpath("FallEffect_1.tact")))

        debug = config['debug']
        while True:
            output = process.stdout.readline()
            if debug:
                print(output)
            if process.poll() is not None:
                if config['debug']:
                    print('Game quit')
                await asyncio.sleep(0)
                break
            elif output:
                # Begin the disgusting amount of if/elif statements
                # to check for the different types of events
                # damage to or spell cast by the player
                if 'bHap health' in output:
                    if config['health']['dynamic_scaling']:
                        # remove substring before the word bHap
                        # should be a value from 0 and 1
                        output = re.sub(r"^.+?(?=bHap)", "", output)
                        health_decrease = float(re.findall("\d+\.\d+", output)[0])
                    else:
                        health_decrease = 1.0
                    if debug:
                        print(f'I got hit for {health_decrease} of my life!')
                    health_tact_file = random.choice(health_tact_files)
                    await websocket.send(submit_payload(health_tact_file,
                        scale_option={"intensity": health_decrease * config['health']['intensity'],
                                      "duration": config['health']['duration']}))
                    # TODO : check for sustained low health to trigger a heartbeat response
                elif 'bHap magicka' in output:
                    if config['magicka']['dynamic_scaling']:
                        output = re.sub(r"^.+?(?=bHap)", "", output)
                        magicka_decrease = float(re.findall("\d+\.\d+", output)[0])
                    else:
                        magicka_decrease = 1.0
                    if debug:
                        print(f'I cast magic missle! {magicka_decrease} used!')
                    magicka_tact_file = random.choice(magicka_tact_files)
                    await websocket.send(submit_payload(magicka_tact_file,
                        scale_option={"intensity": magicka_decrease * config['magicka']['intensity'],
                                      "duration": config['magicka']['duration']}))
                # unequip
                elif 'bHap helmet unequipped' in output:
                    if debug:
                        print('Helmet unequipped!')
                    await websocket.send(submit_payload("UnequipHelmet_1",
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                elif 'bHap cuirass unequipped' in output:
                    if debug:
                        print('Cuirass unequipped!')
                    await websocket.send(submit_payload("UnequipCuirass_1",
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                elif 'bhap shirt unequipped' in output:
                    if debug:
                        print('Shirt unequipped!')
                    await websocket.send(submit_payload("UnequipClothing_1",
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                elif 'bHap robe unequipped' in output:
                    if debug:
                        print('Robe unequipped!')
                    await websocket.send(submit_payload("UnequipClothing_1", 
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                # ideally have a separate tact file for each gauntlet
                elif 'bHap left gauntlet unequipped' in output:
                    if debug:
                        print('Gauntlet unequipped!')
                    await websocket.send(submit_payload("UnequipGauntlets_1", 
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                elif 'bHap right gauntlet unequipped' in output:
                    if debug:
                        print('Gauntlet unequipped!')
                    await websocket.send(submit_payload("UnequipGauntlets_1", 
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))

                # equip
                elif 'bHap helmet equipped' in output:
                    if debug:
                        print('Helmet equipped!')
                    await websocket.send(submit_payload("EquipHelmet_1", 
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                elif 'bHap cuirass equipped' in output:
                    if debug:
                        print('Cuirass equipped!')
                    await websocket.send(submit_payload("EquipCuirass_1", 
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                elif 'bhap shirt equipped' in output:
                    if debug:
                        print('Shirt equipped!')
                    await websocket.send(submit_payload("EquipClothing_1", 
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                elif 'bHap robe equipped' in output:
                    if debug:
                        print('Robe equipped!')
                    await websocket.send(submit_payload("EquipClothing_1", 
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                # ideally have a separate tact file for each gauntlet
                elif 'bHap left gauntlet equipped' in output:
                    if debug:
                        print('Gauntlet equipped!')
                    await websocket.send(submit_payload("EquipGauntlets_1", 
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                elif 'bHap right gauntlet equipped' in output:
                    if debug:
                        print('Gauntlet equipped!')
                    await websocket.send(submit_payload("EquipGauntlets_1", 
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))

                # consumables
                elif 'bHap potion consumed' in output:
                    if debug:
                        print('Potion consumed!')
                    await websocket.send(submit_payload("ConsumableDrink_1", 
                        scale_option={"intensity": 0.75,
                                    "duration": 1.0}))
                elif 'bHap ingredient consumed' in output:
                    if debug:
                        print('Ingredient consumed!')
                    await websocket.send(submit_payload("ConsumableFood_1", 
                        scale_option={"intensity": 0.75,
                                    "duration": 1.0}))
                # assume we're right handed?
                elif 'bHap ammo' in output:
                    if debug:
                        print('Ammo equip/unequip')
                    await websocket.send(submit_payload("UnholsterArrowRightShoulder_1", 
                        scale_option={"intensity": 1.0,
                                    "duration": 1.0}))
                elif 'bHap player landed' in output:
                    if debug:
                        print('Player landed')
                    # big falls will be amplified by the haptics from health loss
                    # so keep the intensity and duration small
                    await websocket.send(submit_payload("FallEffect_1",
                        scale_option={"intensity": 0.5,
                                    "duration": 0.5})) 
                else:
                    continue
                await asyncio.sleep(0)

def create_session(config, process):
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main(config, process))
    except websockets.exceptions.ConnectionClosedError:
        if config['debug']:
            print("Connection closed")

if __name__ == '__main__':
    # read the config file
    config_filepath = Path('./config.json')
    config = json.load(open(config_filepath))

    # start openMW
    process = Popen(config['openMW_exe_path'], stdin=PIPE, stdout=PIPE, 
        universal_newlines = True)

    create_session(config, process)
    # Reconnect if game is still running
    while True:
        if process.poll() is None:
            if config['debug']:
                print('Reconnecting to bHaptics player')
            create_session(config, process)
        else:
            break