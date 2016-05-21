# Setting target libraries / paths
set clib_path ../clib/
set rtr_path  ../
set search_path [concat $search_path $clib_path $rtr_path]
set target_library class.db
set link_library   class.db

# Grabbing clib source files
set src_list [list rtr_top.v vcr_top.v whr_top.v]
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

  if {[string match *top* $design_name]} {
    puts "=================================================="
    puts [concat "TOP MODULE REPORTS: " $design_name]
    puts "=================================================="
    report_timing
    report_area
    report_power
  }

  if {[string match *wrap* $design_name]} {
    puts "=================================================="
    puts [concat "WRAPPER MODULE REPORTS: " $design_name]
    puts "=================================================="
    report_timing
    report_area
    report_power
  }
}

exit
