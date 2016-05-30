# Setting target libraries / path
set v_path    ../../lib/synopsys/lib/ami05/osu05_stdcells
set db_path   ../../lib/synopsys/lib/ami05/
set lef_path  ../../lib/back_end/lef/
set tf_path   ../../lib/synopsys/flow/ami05/
set search_path [concat $search_path $db_path $lef_path $tf_path $v_path]

set target_library osu05_stdcells.db
set link_library   osu05_stdcells.db
# set target_library NanGate_15nm_OCL_typical_conditional_ecsm.db
# set link_library   NanGate_15nm_OCL_typical_conditional_ecsm.db

# Custom
set tf_name tech.tf
set tf_lib  $tf_path$tf_name

# Grabbing source files
set src_list [list router_wrap.out.place.v rtr_top.out.place.v vcr_top.out.place.v whr_top.out.place.v router_wrap.out.place.v]

create_mw_lib -technology $tf_lib -mw_reference_library {../../lib/synopsys/lib/ami05/osu05_stdcells} "router_lib"
open_mw_lib "router_lib"

# Iterating over each file
foreach path $src_list {
  set file_name [lindex [split $path /] end]
  set design_name [lindex [split $file_name .] 0]


  import_designs $file_name -format v -top $design_name -cell $design_name
  
  derive_pg_connection -create_nets
  
  create_floorplan \
    -control_type      "aspect_ratio" \
    -core_aspect_ratio "1"   \
    -core_utilization  "0.7" \
    -row_core_ratio    "1"

  create_fp_placement

  route_opt -effort low

  change_names -rule verilog -hierarchy
  write_verilog [join [list $design_name ".out.place.v"  ] ""] 
  write_sdc     [join [list $design_name ".out.place.sdc"] ""] 

  if {[string match *top* $design_name]} {
    report_timing -nosplit > [join [list $design_name ".rpt.place.timing"] ""]
    report_area   -nosplit > [join [list $design_name ".rpt.place.area"] ""]
    report_power  -nosplit > [join [list $design_name ".rpt.place.power"] ""]
  }

  if {[string match *wrap* $design_name]} {
    report_timing -nosplit > [join [list $design_name ".rpt.place.timing"] ""]
    report_area   -nosplit > [join [list $design_name ".rpt.place.area"] ""]
    report_power  -nosplit > [join [list $design_name ".rpt.place.power"] ""]
  }
}

exit
