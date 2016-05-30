import os
import sys

# Set filepaths
param_file   = "../parameters.v"
sweep_var = {}
# sweep_var["num_nodes"] = [32]
sweep_var["num_dimensions"] = [3]

def main():
  global sweep_var
  global param_file
  
  src_list = []
  if len(sys.argv) > 1:
      src_list = sys.argv[1:]

  # Sweep through each value
  for (parameter, values) in sweep_var.iteritems():
    for value in values:

        # Set parameter to sweep value
        set_param(param_file, parameter, value)

        print "==================================="
        print "Parameter: " + parameter
        print "Value: " + str(value)
        print "==================================="

        # Set output log suffix
        log_suffix = ""
        if type(value) is str:
            log_suffix = parameter + "_" + value[1:]
        elif type(value) is int:
            log_suffix = parameter + "_" + str(value)

        # Run synthesis
        synth_cmd = "python py_synth.py " + " ".join(src_list)
        os.system(synth_cmd)

        # Combining synthesis reports
        synth_log = "out_synth_" + log_suffix
        synth_out_list = [f for f in os.listdir("./") if ".rpt.synth" in f]
        with open("./" + synth_log, "w") as log:
            for synth_out in synth_out_list:
                with open(synth_out) as out_file:
                    for line in out_file:
                        log.write(line)
        
        os.system("rm -rf *rpt.synth*")
        
        # Run place/route
        place_cmd = "python py_place.py " + " ".join(src_list)
        os.system(place_cmd)

        # Combining place/route reports
        place_log = "out_place_" + log_suffix
        place_out_list = [f for f in os.listdir("./") if ".rpt.place" in f]
        with open("./" + place_log, "w") as log:
            for place_out in place_out_list:
                with open(place_out) as out_file:
                    for line in out_file:
                        log.write(line)

        os.system("rm -rf *rpt.place*")
        
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
