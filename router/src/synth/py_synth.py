import os

# Set filepaths
synth_script = "./synth.tcl"
rtr_path     = ".."
clib_path    = "../clib"

# Filter for Verilog files only
rtr_list  = [f for f in os.listdir(rtr_path)  if ".v" in f]
clib_list = [f for f in os.listdir(clib_path) if ".v" in f]

def main():
    global clib_list
    global rtr_list

    synthesize("c", clib_list)
    synthesize("r", rtr_list)
    return


def synthesize(prefix, src_list):
    global synth_script

    # Iterating over c_lib files first
    count = 0
    while len(src_list) > 0 and count < 3:
        
        error_list = []
        out_name = "out_" + prefix + "_" + str(count)
        if os.path.isfile(out_name):
            cmd = "rm -rf " + out_name
            os.system(cmd)
        
        # Synthesize design
        with open(synth_script, "r+") as sp_file:
            # Read text
            text = sp_file.read()
            lines = text.split('\n')
            for i in range(len(lines)):

                # Skipping irrelevant lines
                if "set src_list" not in lines[i]:
                    continue

                lines[i] = "set src_list [list " + " ".join(src_list) + "]"
            
            sp_file.close()

        with open(synth_script, "w") as sp_file:
            # Replace new text
            text = '\n'.join(lines)
            sp_file.write(text)
            sp_file.close()

            # Running dc_shell-t
            cmd = "dc_shell-t -f " + synth_script + " > " + out_name
            os.system(cmd)

        # If output has error, add to error_list
        with open(out_name, "r") as out_file:
            inst = ""
            # Read each line
            for line in out_file.readlines():
                # Grab instance name
                if "Current design is \'" in line:
                    inst = line.split("\'")[1] + ".v"
                
                # If instance has error, add to list
                if "Warning: " in line and "unresolved references" in line:
                    if inst not in error_list:
                        error_list.append(inst)
                elif "Error: " in line and "unitless" not in line:
                   if inst not in error_list:
                        error_list.append(inst)

            out_file.close()
        
        src_list = error_list
        count = count + 1
    return

if __name__ == "__main__":
    main()
