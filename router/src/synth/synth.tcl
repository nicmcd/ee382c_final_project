
set search_path [concat $search_path .. ../clib]
set target_library class.db
set link_library   class.db

set name rtr_top
set wild *
# set c_files   [glob -path ../clib/ $wild$name$wild]
set rtr_files   [glob -path ../ $wild$name$wild]

# set c_files   [glob -path ../clib/ *]
set c_files   []
# set rtr_files [glob -path ../ rtr*]
# set rtr_files []
set all_files [concat $c_files $rtr_files]

foreach path $all_files {
  set file_name [lindex [split $path /] end]
  set design_name [lindex [split $file_name .] 0]

  if {[string match $design_name "c_functions"  ]} { continue }
  if {[string match $design_name "c_constants"  ]} { continue }
  if {[string match $design_name "rtr_constants"]} { continue }

  puts $file_name
  read_file -f verilog $file_name
  analyze   -f verilog $file_name
  elaborate $design_name
  compile_ultra

  if {[string match $design_name "rtr_top"]} {
    report_timing
    report_area
    report_power
  }
}

exit
