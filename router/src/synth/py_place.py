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
        # Place/route router_wrap only!!
        src_list  = [f for f in os.listdir(synth_path) if (".out.synth.v" in f) and ("wrap" in f)]

    place_route(src_list)

    return

def place_route(src_list):
    global place_script
    place_list = []

    for src in src_list:
        name = "".join((src.split(".")[0], ".out.place.v"))
        # If top-level module, then place/route
        if ("wrap" in name):
            place_list.append(src)
        # If not already placed, then place/route
        elif name not in os.listdir(synth_path):
            place_list.append(src)

    print "INFO: Placing designs: " + " ".join(place_list)
    
    # Configuring log file (ROUTER WRAP ONLY!!)
    out_name = "router_wrap.rpt.place"
    if os.path.isfile(out_name):
        cmd = "rm -rf " + out_name
        os.system(cmd)
    
    # Inserting items to be placed
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

    return

if __name__ == "__main__":
    main()
