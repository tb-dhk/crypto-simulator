import os
import time
import json
import subprocess 
import random

with open('resource/gpu.json', 'r') as file:
    gpu_list = json.load(file)

crypto = 0
gpu = {
    "name": gpu_list[0]['name'],
    "quality": 1
}

name = ""

def gum_table(ls, headers, index=0, print_index=1):
    option = subprocess.check_output(
        [
            "gum", "table", 
            "--height=" + str(len(ls) + 1), 
            "--widths=4," + ",".join([str(max(len(str(o[c])) for o in [headers] + ls)) for c in range(len(ls[0]))]),
            "--columns=" + ",".join(["#"] + headers)
        ], 
        input="\n".join(f"{i}," + ",".join(str(o) for o in opt) for i, opt in enumerate(ls)),
        text=True
    ).strip().split(",")
    print(">", option[print_index])
    return option[index]

def gum_confirm(s):
    try:
        subprocess.check_output([
            "gum", "confirm", s,
            "--affirmative=yes", "--negative=no"
        ])
    except:
        return False
    else:
        return True

def new_game(save_name):
    global crypto
    global gpu
    crypto = 0
    gpu["name"] = "grandpa's video card"
    gpu["quality"] = 1
    save_game(save_name)
    Game(save_name)

def load_save(save_name):
    global crypto
    global gpu
    with open(f"saves/{save_name}.json", "r") as save:
        data = json.load(save)
        crypto = data['crypto']
        gpu["name"] = data["gpu"]["name"]
        gpu["quality"] = data["gpu"]["quality"]
    Game(save_name)

def save_game(save_name):
    global crypto
    global gpu
    with open(f"saves/{save_name}.json", "w") as save:
        data = {
            'crypto': crypto,
            'gpu': gpu 
        }
        save.write(json.dumps(data,indent=4))

def mine():
    global crypto
    global gpu
    save_game(name)
    start = crypto
    print("mining... (press Ctrl+C to exit)")
    while True:
        try:
            crypto += gpu["quality"] ** 2 * 4 * random.random()
            crypto = round(crypto, 2)
            print(f"> you have {crypto} crypto. (+{round(crypto-start, 2)})", end="     \r")
            save_game(name)
            time.sleep(1)
        except KeyboardInterrupt:
            print(f"\ryou have mined {crypto-start} crypto! you now have {crypto} crypto.")
            break

def buy_gpu(choice):
    global crypto, gpu
    for g in gpu_list:
        if g["name"] == choice:
            name = g["name"]
            quality = g["quality"]
            price = g["price"]
            break
   
    if crypto < price:
        print(f"sorry, you don't have enough crypto. you need {price} ({price - crypto} more).")
        return

    sure = gum_confirm("are you sure?") 

    if sure:
        crypto = round(crypto - price, 2)
        gpu["name"] = name
        gpu["quality"] = quality
    else:
        return

def gpu_store():
    while 1:
        print("welcome to the gpu store!")
        print(f"current gpu: {gpu["name"]} (quality {gpu["quality"]})")
        choice = gum_table([[g["name"], g["price"], g["quality"]] for g in gpu_list if g["quality"] > gpu["quality"]], ["name", "price", "quality"], index=1)
        if choice == 0:
            break
        buy_gpu(choice)
        break

def profile():
    global crypto, gpu
    print(f"you have {crypto} crypto, and gpu {gpu["name"]} (quality {gpu["quality"]}).")
    return

def Game(name):
    if __name__ != "__main__":
        return
    options = [
        ["buy gpu"],
        ["start mining"],
        ["return to menu"],
    ]
    while 1:
        print()
        profile()
        save_game(name)

        choice = gum_table(options, ["option"])
        match int(choice):
            case 0:
                gpu_store()
            case 1:
                mine()
            case 2:
                Menu()
            case _:
                print("invalid input. try again.")

def Menu():
    global name

    while True:
        print("welcome!")
        options = [
            ["load game"],
            ["new game"],
            ["exit"],
        ]
        choice = gum_table(options, ["option"])
        match int(choice):
            case 0:
                name = gum_table([[s.split(".")[0]] for s in os.listdir("saves")], ["option"], index=1)
                load_save(name)
            case 1:
                name = input("enter new save name: ")
                with open(f"saves/{name}.json", "w") as f:
                    f.write("{}")
                new_game(name)
            case 2:
                exit()
        print()

if __name__ == "__main__":
    Menu()
