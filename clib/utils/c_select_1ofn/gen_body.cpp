#include <iostream>
#include <cstdlib>

int main(int argc, char ** argv) {
  int min = (argc > 1) ? atoi(argv[1]) : 1;
  int max = (argc > 2) ? atoi(argv[2]) : std::max(min, 64);
  std::cout
    << "      // synopsys translate_off\n"
    << "      if(num_ports < " << min << ")\n"
    << "	begin\n"
    << "	   initial\n"
    << "	     begin\n"
    << "		$display({\"ERROR: Select-mux module %m needs at least " << min << " inputs.\"});\n"
    << "		$stop;\n"
    << "	     end\n"
    << "	end\n"
    << "      else if(num_ports > " << max << ")\n"
    << "	begin\n"
    << "	   initial\n"
    << "	     begin\n"
    << "		$display({\"ERROR: Select-mux module %m supports at most " << max << " inputs.\"});\n"
    << "		$stop;\n"
    << "	     end\n"
    << "	end\n"
    << "      // synopsys translate_on\n"
    << "      \n";
  for(int size = min; size <= max; ++size) {
    std::cout
      << "      ";
    if(size > min) {
      std::cout << "else ";
    }
    std::cout << "if(num_ports == " << size << ")\n"
      << "        always@(select, data_in)\n"
      << "          begin\n"
      << "             case(select)\n";
    for(int pos = 0; pos < size; ++pos) {
      std::cout
	<< "               " << size << "'b";
      for(int i = 0; i < pos; ++i) {
	std::cout << "0";
      }
      std::cout << "1";
      for(int i = pos + 1; i < size; ++i) {
	std::cout << "0";
      }
      std::cout
	<< ":\n"
	<< "                 data_out = data_in[" << pos << "*width:" << pos + 1 << "*width-1];\n";
    }
    std::cout
      << "               default:\n"
      << "                 data_out = {width{1'bx}};\n"
      << "             endcase\n"
      << "          end\n";
  }
}
