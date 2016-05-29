import os

# Set filepaths
synth_script = "./synth.tcl"
param_file   = "../parameters.v"
sweep_var = {
  "topology"  : ["`TOPOLOGY_MESH", "`TOPOLOGY_TORUS"],
  "num_nodes" : [64, 81, 100]
}

# Deleting previous log file
def delete_log():
  cmd = "rm -rf *.out_sweep"
  os.system(cmd)
  return

# Set synthesis target to router_wrap.v
def set_synth(synth_script):
  with open(synth_script, "r+") as sp_file:
    # Read text
    text = sp_file.read()
    lines = text.split('\n')
    for i in range(len(lines)):

      # Skipping irrelevant lines
      if "set src_list" not in lines[i]:
        continue

      lines[i] = "set src_list [list router_wrap.v]"
    
    sp_file.close()

  with open(synth_script, "w") as sp_file:
    # Replace new text
    text = '\n'.join(lines)
    sp_file.write(text)
    sp_file.close()
  
  return

# Set parameter to sweep value
def set_param(param_file, parameter, value):
  with open(param_file, "r+") as p_file:
    # Read text
    text = p_file.read()
    lines = text.split('\n')
    for i in range(len(lines)):

      # Skipping irrelevant lines
      if (parameter + " = ") not in lines[i]:
        continue
      
      lines[i] = "parameter " + parameter + " = " + str(value) + ";"
    
    p_file.close()

  with open(param_file, "w") as p_file:
    # Replace new text
    text = '\n'.join(lines)
    p_file.write(text)
    p_file.close()

  return

def main():
  global synth_script
  global sweep_var
  global param_file
  
  # Delete previous log file
  delete_log()
  
  # Set synthesis target to router_wrap.v
  set_synth(synth_script)
  
  # Sweep through each value
  for (parameter, values) in sweep_var.iteritems():
    for value in values:

        # Set parameter to sweep value
        set_param(param_file, parameter, value)
        
        # Run dc_shell-t
        cmd = "dc_shell-t -f " + synth_script + " > "
        if type(value) is int:
            cmd = cmd + parameter + "_" + str(value) + ".out_sweep"
        elif parameter == "topology":
            cmd = cmd + parameter + "_" + value[1:] +  ".out_sweep"
        os.system(cmd)

  return

if __name__ == "__main__":
  main()
