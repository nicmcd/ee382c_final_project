import os
import sys

# Set filepaths
place_script = "./place.tcl"
synth_path     = "."

def main():
    src_list = []
    if len(sys.argv) > 1:
        src_list = sys.argv[1:]
    else:
        src_list  = [f for f in os.listdir(synth_path) if (".v" in f) and (("top" in f) or ("wrap" in f))]

    place_route(src_list)

    return

def place_route(src_list):
    global place_script
    place_list = []

    for src in src_list:
        name = "".join((src.split(".")[0], ".out.place.v"))
        # If top-level module, then synthesize
        if ("top" in name) or ("wrap" in name):
            place_list.append(name)
        # If not already synthesized, then synthesize
        elif name not in os.listdir(synth_path):
            place_list.append(name)

    out_name = "out" + "_place"
    if os.path.isfile(out_name):
        cmd = "rm -rf " + out_name
        os.system(cmd)
    
    # Place and Route design
    with open(place_script, "r+") as pr_file:
    # Read text
        text = pr_file.read()
        lines = text.split('\n')
        for i in range(len(lines)):

            # Skipping irrelevant lines
            if "set src_list" not in lines[i]:
                continue

            lines[i] = "set src_list [list " + " ".join(place_list) + "]"
        
        pr_file.close()

    with open(place_script, "w") as pr_file:
        # Replace new text
        text = '\n'.join(lines)
        pr_file.write(text)
        pr_file.close()

    # Running icc_shell
    cmd = "icc_shell -64bit -f " + place_script + " > " + out_name
    os.system(cmd)

    # # If output has error, add to error_list
    # with open(out_name, "r") as out_file:
    # inst = ""
    # # Read each line
    # for line in out_file.readlines():
    #     # Grab instance name
    #     if "Current design is \'" in line:
    #         inst = line.split("\'")[1] + ".v"
    #     
    #     # If instance has error, add to list
    #     if "Warning: " in line and "unresolved references" in line:
    #         if inst not in error_list:
    #             error_list.append(inst)
    #     elif "Error: " in line and "unitless" not in line:
    #        if inst not in error_list:
    #             error_list.append(inst)

    # out_file.close()
    
    return

if __name__ == "__main__":
    main()
