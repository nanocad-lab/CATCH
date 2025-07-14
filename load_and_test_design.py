# =======================================================================
# Copyright 2025 UCLA NanoCAD Laboratory
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#     http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# =======================================================================

# ====================================================================================
# Filename: load_and_test_design.py
# Author: Alexander Graening
# Affiliation: University of California, Los Angeles
# Email: agraening@ucla.edu
#
# Description: This is the main file used to launch loading a single design and viewing cost.
# ====================================================================================

import design as d
import readDesignFromFile as readDesign
import sys
import time


# Main function
def main():
    # Get start time
    start_time = time.time()
    # Read the file names as command line arguments.
    if len(sys.argv) != 8:
        print("Usage: python load_and_test_design.py <io_file> <layer_file> <wafer_process_file> <assembly_process_file> <test_file> <netlist_file> <chip_file>")
        return 1

    # Read the File Names as Command Line Arguments
    io_file = sys.argv[1]
    layer_file = sys.argv[2]
    wafer_process_file = sys.argv[3]
    assembly_process_file = sys.argv[4]
    test_file = sys.argv[5]
    netlist_file = sys.argv[6]
    chip_file = sys.argv[7]

    # Read the Design Library Files
    io_list = readDesign.io_definition_list_from_file(io_file)
    layer_list = readDesign.layer_definition_list_from_file(layer_file)
    wafer_process_list = readDesign.wafer_process_definition_list_from_file(wafer_process_file)
    assembly_process_list = readDesign.assembly_process_definition_list_from_file(assembly_process_file)
    test_process_list = readDesign.test_process_definition_list_from_file(test_file)

    # Read the Design Netlist File
    adjacency_matrix, utilization, names = readDesign.global_adjacency_matrix_from_file(netlist_file,io_list)

    # Read the System Definition
    sip = d.Chip(filename = chip_file, etree = None, parent_chip = None, wafer_process_list = wafer_process_list, assembly_process_list = assembly_process_list, test_process_list = test_process_list, layers = layer_list, ios = io_list, adjacency_matrix_definitions = adjacency_matrix, average_bandwidth_utilization=utilization, block_names = names, static = False)

    # Print the Design Description
    #sip.print_description()

    #print("Cost of design = " + str(sip.get_cost()))
    print(sip.compute_total_cost())

#    for chip in sip.get_chips():
#        print(chip.name + " " + str(chip.get_cost()))

    end_time = time.time()

    #print("Total time: " + str(end_time - start_time) + " seconds")

    return 0


# Setup auto-run of main function.
if __name__ == "__main__":
    main()
