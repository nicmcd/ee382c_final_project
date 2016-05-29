# Setting target libraries / paths
set lib_path ../../lib/synopsys/lib/ami05/
set clib_path ../clib/
set rtr_path  ../
set search_path [concat $search_path $clib_path $rtr_path $lib_path]

set target_library osu05_stdcells.db
set link_library   osu05_stdcells.db

# Grabbing clib source files
set src_list [list parameters.v router_wrap.v rtr_alloc_mac.v rtr_channel_input.v rtr_channel_output.v rtr_constants.v rtr_crossbar_mac.v rtr_fc_state.v rtr_flags_mux.v rtr_flit_buffer.v rtr_flit_type_check.v rtr_flow_ctrl_input.v rtr_flow_ctrl_output.v rtr_ip_ctrl_mac.v rtr_next_hop_addr.v rtr_op_ctrl_mac.v rtr_route_filter.v rtr_routing_logic.v rtr_top.v vcr_alloc_mac.v vcr_constants.v vcr_ip_ctrl_mac.v vcr_ivc_ctrl.v vcr_op_ctrl_mac.v vcr_ovc_ctrl.v vcr_sw_alloc_sep_if.v vcr_sw_alloc_sep_of.v vcr_sw_alloc_wf.v vcr_top.v vcr_vc_alloc_sep_if.v vcr_vc_alloc_sep_of.v vcr_vc_alloc_wf.v whr_alloc_mac.v whr_constants.v whr_ip_ctrl_mac.v whr_op_ctrl_mac.v whr_top.v parameters.v_bak]

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
    report_timing -nosplit > [join [list $design_name ".rpt.synth.timing"] ""]
    report_area   -nosplit > [join [list $design_name ".rpt.synth.area"] ""]
    report_power  -nosplit > [join [list $design_name ".rpt.synth.power"] ""]
  }

  if {[string match *wrap* $design_name]} {
    report_timing -nosplit > [join [list $design_name ".rpt.synth.timing"] ""]
    report_area   -nosplit > [join [list $design_name ".rpt.synth.area"] ""]
    report_power  -nosplit > [join [list $design_name ".rpt.synth.power"] ""]
  }
}

exit
