import sys
import os
import subprocess
import shlex
import time

def print_dimensions(args):
    val = ''
    for num in args:
        val = val + 'by' + str(num)
    return val[2:]

def get_dimension_override(dimension, args):
    val = []
    count = 0
    for num in args:
        val.append(('network.'+dimension + '[{0}]=uint={1} ').format(count, num))
        count = count + 1
    return val

def get_weight_override(num):
    val = []
    count = 0
    for i in range(0, num):
        val.append(('network.dimension_weights[{0}]=uint=1 ').format(count))
        count = count + 1
    return val

def join_underscores(*args):
    val = ''
    for string in args:
        val = val + '_{0}'.format(string)
    return val[1:]

if __name__ == '__main__':
    os.chdir('/home/rprabala/ee382c_project/ee382c_final_project')
    model_folder = os.path.join('Synfull', 'models')
    # cycle_sweep = [20000, 50000] #, 2000000, 5000000]
    cycle_sweep = [2000000, 500000]
    json_file = os.path.join('./supersim_env', 'supersim', 'json', 'synfull_blank.json')
    # network = 'hyperx'
    num_vcs = [4, 8]
    dimensions = [ [2,16], [4,8], [1,32], [2,2,8], [2,4,4], [2,2,2,2,2]]
    # dimensions = [[4,8], [2,2,2,2,2]]
    num_dimensions = [2, 2, 2, 3, 3, 5]
    # num_dimensions = [2, 5]
    # networks = ['torus', 'hyperx']
    networks = ['hyperx', 'torus']
    # dim_names = ['dimensions', 'dimension_widths']
    dim_names = ['dimension_widths', 'dimensions']
    routing = ['dimension_order']
    end_steady_state = 1

    print get_dimension_override('dimensions', dimensions[0])

    for n in range(0,len(networks)):
        network = networks[n]
        dim_name = dim_names[n]
        for f in os.listdir(model_folder):
            for x in range(0,len(dimensions)):
                if network == 'hyperx' and x == 2:
                    continue

                for vc in num_vcs:
                    for route in routing:
                        supersim_cmd = './supersim_env/supersim/bin/supersim ' + json_file + ' '
                        overrides = get_dimension_override(dim_name, dimensions[x])
                        weights = get_weight_override(num_dimensions[x])
                        for y in range(0, num_dimensions[x]):
                            supersim_cmd = supersim_cmd + overrides[y]
                        for z in range(0, num_dimensions[x]):
                            supersim_cmd = supersim_cmd + weights[z]

                        supersim_cmd = supersim_cmd + ' network.num_vcs=uint=' + str(vc) + ' network.routing.algorithm=string='+route
                        supersim_cmd = supersim_cmd + ' network.topology=string=' + network
                        # print supersim_cmd
                        for c in cycle_sweep:
                            output_file = 'output/'+join_underscores(network, route, vc, f, c, print_dimensions(dimensions[x]))
                            rate_file = 'output/rates/'+join_underscores(network, route, vc, f, c, print_dimensions(dimensions[x]))
                            if os.path.exists(output_file):
                                print(output_file, ' exists, skipping')
                                continue
                            tgen_cmd = ('./Synfull/src/tgen ./' + model_folder + '/{0} {1} {2} ').format(f, c, end_steady_state)
                            tgen_cmd = tgen_cmd + 'output/'+join_underscores(network, route, vc, f, c, print_dimensions(dimensions[x]))
                            supersim_cmd = supersim_cmd + ' application.rate_log.file=string='+rate_file
                            subprocess.Popen(shlex.split(supersim_cmd))
                            time.sleep(2)
                            subprocess.check_call(shlex.split(tgen_cmd))

