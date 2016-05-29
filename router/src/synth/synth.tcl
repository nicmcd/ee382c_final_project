# Setting target libraries / paths
set lib_path  ../../lib/front_end/timing_power_noise/ECSM/
# set lib_path ../../lib/synopsys/lib/ami05/
set clib_path ../clib/
set rtr_path  ../
set search_path [concat $search_path $clib_path $rtr_path $lib_path]

# set target_library osu05_stdcells.db
# set link_library osu05_stdcells.db
set target_library NanGate_15nm_OCL_typical_conditional_ecsm.db
set link_library   NanGate_15nm_OCL_typical_conditional_ecsm.db

# Grabbing clib source files
set src_list [list c_align.v]

# Iterating over each file
foreach path $src_list {
  set file_name [lindex [split $path /] end]
  set design_name [lindex [split $file_name .] 0]

  # Removing unsynthesizeable functions
  if {[string match *function*   $design_name]} { continue }
  if {[string match *constant*   $design_name]} { continue }
  if {[string match *parameters* $design_name]} { continue }

  read_file -f verilog $file_name
  analyze   -f verilog $file_name
  elaborate $design_name
  compile_ultra

  change_names -rules verilog
  write -f verilog -hierarchy -output [join [list $design_name ".out.synth.v"] ""]
  write_sdc -nosplit [join [list $design_name ".out.synth.sdc"] ""]

  if {[string match *top* $design_name]} {
    puts "=================================================="
    puts [concat "TOP MODULE REPORTS: " $design_name]
    puts "=================================================="
    report_timing -nosplit
    report_area   -nosplit
    report_power  -nosplit
  }

  if {[string match *wrap* $design_name]} {
    puts "=================================================="
    puts [concat "WRAPPER MODULE REPORTS: " $design_name]
    puts "=================================================="
    report_timing -nosplit
    report_area   -nosplit
    report_power  -nosplit
  }
}

exit
