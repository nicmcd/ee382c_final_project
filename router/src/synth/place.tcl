# Setting target libraries / path
set v_path    ../../lib/synopsys/lib/ami05/osu05_stdcells
set db_path   ../../lib/synopsys/lib/ami05/
set lef_path  ../../lib/back_end/lef/
set tf_path   ../../lib/synopsys/flow/ami05/
set search_path [concat $search_path $db_path $lef_path $tf_path $v_path]

set target_library osu05_stdcells.db
set link_library   osu05_stdcells.db

# Custom
set tf_name tech.tf
set tf_lib  $tf_path$tf_name

# Grabbing source files
set src_list [list router_wrap.out.synth.v]

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

  route_zrt_global -effort minimum 
  route_zrt_track

  change_names -rule verilog -hierarchy
  write_verilog [join [list $design_name ".out.place.v"  ] ""] 
  write_sdc     [join [list $design_name ".out.place.sdc"] ""] 

  report_timing -nosplit
  report_area   -nosplit
  report_power  -nosplit
}

exit
