import os
import sys

# Set filepaths
param_file   = "../parameters.v"
sweep_var = {
  "topology"  : ["`TOPOLOGY_MESH", "`TOPOLOGY_TORUS"],
  "num_nodes" : [64, 81, 100]
}

def main():
  global sweep_var
  global param_file
  
  src_list = []
  if len(sys.argv) > 1:
      src_list = sys.argv[1:]

  # Delete previous log file
  cmd = "rm -rf *.out_sweep"
  os.system(cmd)
  
  # Sweep through each value
  for (parameter, values) in sweep_var.iteritems():
    for value in values:

        # Set parameter to sweep value
        set_param(param_file, parameter, value)
        
        # Set output log suffix
        log = ""
        if type(value) is str:
            log = parameter + "_" + value[1:]
        elif type(value) is int:
            log = parameter + "_" + str(value)

        # Run synthesis
        cmd = "python py_synth.py " + " ".join(src_list) + " > out_synth_" + log
        os.system(cmd)

        # Run place/route
        cmd = "python py_place.py " + " ".join(src_list) + " > out_place_" + log
        os.system(cmd)

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

if __name__ == "__main__":
  main()
