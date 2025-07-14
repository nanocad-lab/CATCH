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

import math
import sys
import os
# Generate a system definition .xml file.


# As input, take the number of chiplets, IO type, a bidirectional flag, external bandwidth, and the total power as inputs.
if len(sys.argv) != 8:
    print("ERROR: Incorrect Number of Input Arguments\nUsage: python generate_test_files_3d.py <number_of_chiplets> <interchiplet_IO_type> <bidirectional_flag> <organic_flag> <external_bandwidth> <total_power> <logic_fraction>\nExiting...")
    sys.exit(1)


number_of_chiplets = int(sys.argv[1])
interchiplet_IO_type = sys.argv[2]
bidirectional = sys.argv[3]
organic_flag_str = sys.argv[4]
total_ext_bandwidth = float(sys.argv[5])
total_power = float(sys.argv[6])
logic_fraction = float(sys.argv[7])

total_chiplet_area = 800

area_of_chiplets = total_chiplet_area / number_of_chiplets
power_per_chiplet = total_power / number_of_chiplets

identifier = "chiplet_" + str(number_of_chiplets) + "_" + str(math.floor(area_of_chiplets))

test_process = "KGD_free_test"
interposer_test_process = "KGD_interposer_free_test"
wafer_process = "process_1"
# wafer_diameter = "300"
# edge_exclusion = "3"
# wafer_process_yield = " 0.94"
# reticle_x = "26"
# reticle_y = "33"

# externalInputs = "0"
# externalOutputs = "0"

system_quantity = "10000000"
quantity=str(int(system_quantity) * number_of_chiplets)

if bidirectional == "True":
    bidirectional_flag = True
elif bidirectional == "False":
    bidirectional_flag = False
else:
    print("ERROR: Invalid bidirectional flag\nExiting...")
    sys.exit(1)

if organic_flag_str == "True" or organic_flag_str == "true":
    organic_flag = True
elif organic_flag_str == "False" or organic_flag_str == "false":
    organic_flag = False
else:
    organic_flag = False

if organic_flag:
    assembly_process = "organic_simultaneous_bonding"
    interposer_stackup = "1:combined_interposer_organic"
else:
    assembly_process = "silicon_individual_bonding"
    interposer_stackup = "1:combined_interposer_silicon"

chip_stackup = "1:combined_5nm"

# Generate def xml file
def_file = open(identifier + "_def" + ".xml", "w")

def_file.write("<chip name=\"interposer\"\n")
def_file.write("\tbb_area=\"\"\n")
def_file.write("\tbb_cost=\"\"\n")
def_file.write("\tbb_quality=\"\"\n")
def_file.write("\tbb_power=\"\"\n")
def_file.write("\taspect_ratio=\"\"\n")
def_file.write("\tx_location=\"\"\n")
def_file.write("\ty_location=\"\"\n")
def_file.write("\torientation=\"face-up\"\n")
def_file.write("\tstack_side=\"face\"\n")
def_file.write("\tcore_area=\"0.0\"\n")
def_file.write("\tfraction_memory=\"0.0\"\n")
def_file.write("\tfraction_logic=\"0.0\"\n")
def_file.write("\tfraction_analog=\"1.0\"\n")
def_file.write("\tgate_flop_ratio=\"1.0\"\n")
def_file.write("\treticle_share=\"1.0\"\n")
def_file.write("\tburied=\"False\"\n")
def_file.write("\tassembly_process=\"" + assembly_process + "\"\n")
def_file.write("\ttest_process=\"" + interposer_test_process + "\"\n")
def_file.write("\tstackup=\"" + interposer_stackup + "\"\n")
def_file.write("\twafer_process=\"" + wafer_process + "\"\n")
def_file.write("\tpower=\"0.0\"\n")
def_file.write("\tquantity=\"" + system_quantity + "\"\n")
def_file.write("\tcore_voltage=\"1.0\">\n")

for i in range(number_of_chiplets):
    def_file.write("\t<chip name=\"chiplet_" + str(i) + "\"\n")
    def_file.write("\t\tbb_area=\"\"\n")
    def_file.write("\t\tbb_cost=\"\"\n")
    def_file.write("\t\tbb_quality=\"\"\n")
    def_file.write("\t\tbb_power=\"\"\n")
    def_file.write("\t\taspect_ratio=\"\"\n")
    def_file.write("\t\tx_location=\"\"\n")
    def_file.write("\t\ty_location=\"\"\n")
    def_file.write("\t\torientation=\"face-down\"\n")
    if i == 0:
        def_file.write("\t\tstack_side=\"face\"\n")
    else:
        def_file.write("\t\tstack_side=\"back\"\n")
    def_file.write("\t\tcore_area=\"" + str(area_of_chiplets) + "\"\n")
    def_file.write("\t\tfraction_memory=\"0.0\"\n")
    def_file.write("\t\tfraction_logic=\"" + str(logic_fraction) + "\"\n")
    def_file.write("\t\tfraction_analog=\"0.0\"\n")
    def_file.write("\t\tgate_flop_ratio=\"1.0\"\n")
    def_file.write("\t\treticle_share=\"1.0\"\n")
    def_file.write("\t\tburied=\"False\"\n")
    def_file.write("\t\tassembly_process=\"" + assembly_process + "\"\n")
    def_file.write("\t\ttest_process=\"" + test_process + "\"\n")
    def_file.write("\t\tstackup=\"" + chip_stackup + "\"\n")
    def_file.write("\t\twafer_process=\"" + wafer_process + "\"\n")
    def_file.write("\t\tpower=\"" + str(power_per_chiplet) + "\"\n")
    def_file.write("\t\tquantity=\"" + quantity + "\"\n")
    def_file.write("\t\tcore_voltage=\"1.0\">\n")

for i in range(number_of_chiplets):
    def_file.write("\t</chip>\n")

def_file.write("</chip>\n")
def_file.close()

# Generate netlist xml file
# Open netlist file
netlist_file = open(identifier + "_netlist" + ".xml", "w")
netlist_file.write("<netlist>\n")

edge_bandwidth = total_ext_bandwidth / (math.sqrt(number_of_chiplets) * 4)

for i in range(number_of_chiplets):
    if i == 0 or i == number_of_chiplets - 1 or i == math.sqrt(number_of_chiplets) - 1 or i == number_of_chiplets - math.sqrt(number_of_chiplets):
        # corner
        external_bandwidth = edge_bandwidth * 2
    elif i % math.sqrt(number_of_chiplets) == 0 or i % math.sqrt(number_of_chiplets) == math.sqrt(number_of_chiplets) - 1:
        # edge
        external_bandwidth = edge_bandwidth
    netlist_file.write("\t<net type=\"" + interchiplet_IO_type + "\"\n")
    netlist_file.write("\t\tblock0=\"chiplet_" + str(i) + "\"\n")
    netlist_file.write("\t\tblock1=\"external\"\n")
    netlist_file.write("\t\tbb_count=\"\"\n")
    netlist_file.write("\t\taverage_bandwidth_utilization=\"0.5\"\n")
    netlist_file.write("\t\tbandwidth=\"" + str(external_bandwidth) + "\">\n")
    netlist_file.write("\t</net>\n")
    # Now the other direction
    netlist_file.write("\t<net type=\"" + interchiplet_IO_type +  "\"\n")
    netlist_file.write("\t\tblock0=\"external\"\n")
    netlist_file.write("\t\tblock1=\"chiplet_" + str(i) + "\"\n")
    netlist_file.write("\t\tbb_count=\"\"\n")
    netlist_file.write("\t\taverage_bandwidth_utilization=\"0.5\"\n")
    netlist_file.write("\t\tbandwidth=\"" + str(external_bandwidth) + "\">\n")
    netlist_file.write("\t</net>\n")

# Now define internal connections assuming a grid of squares with the same edge bandwidth between each adjacent chiplets.
for i in range(number_of_chiplets):
    if i % math.sqrt(number_of_chiplets) != math.sqrt(number_of_chiplets) - 1: # Connect to chiplet on the right
        netlist_file.write("\t<net type=\"" + interchiplet_IO_type + "\"\n")
        netlist_file.write("\t\tblock0=\"chiplet_" + str(i) + "\"\n")
        netlist_file.write("\t\tblock1=\"chiplet_" + str(i + 1) + "\"\n")
        netlist_file.write("\t\tbb_count=\"\"\n")
        netlist_file.write("\t\taverage_bandwidth_utilization=\"0.5\"\n")
        netlist_file.write("\t\tbandwidth=\"" + str(edge_bandwidth) + "\">\n")
        netlist_file.write("\t</net>\n")
    if bidirectional_flag != True:
        if i % math.sqrt(number_of_chiplets) != 0: # Connect to chiplet on the left
            netlist_file.write("\t<net type=\"" + interchiplet_IO_type + "\"\n")
            netlist_file.write("\t\tblock0=\"chiplet_" + str(i) + "\"\n")
            netlist_file.write("\t\tblock1=\"chiplet_" + str(i - 1) + "\"\n")
            netlist_file.write("\t\tbb_count=\"\"\n")
            netlist_file.write("\t\taverage_bandwidth_utilization=\"0.5\"\n")
            netlist_file.write("\t\tbandwidth=\"" + str(edge_bandwidth) + "\">\n")
            netlist_file.write("\t</net>\n")
    if i >= math.sqrt(number_of_chiplets): # Connect to chiplet above
        netlist_file.write("\t<net type=\"" + interchiplet_IO_type + "\"\n")
        netlist_file.write("\t\tblock0=\"chiplet_" + str(i) + "\"\n")
        netlist_file.write("\t\tblock1=\"chiplet_" + str(int(i - math.sqrt(number_of_chiplets))) + "\"\n")
        netlist_file.write("\t\tbb_count=\"\"\n")
        netlist_file.write("\t\taverage_bandwidth_utilization=\"0.5\"\n")
        netlist_file.write("\t\tbandwidth=\"" + str(edge_bandwidth) + "\">\n")
        netlist_file.write("\t</net>\n")
    if bidirectional_flag != True:   
        if i < number_of_chiplets - math.sqrt(number_of_chiplets): # Connect to chiplet below
            netlist_file.write("\t<net type=\"" + interchiplet_IO_type + "\"\n")
            netlist_file.write("\t\tblock0=\"chiplet_" + str(i) + "\"\n")
            netlist_file.write("\t\tblock1=\"chiplet_" + str(int(i + math.sqrt(number_of_chiplets))) + "\"\n")
            netlist_file.write("\t\tbb_count=\"\"\n")
            netlist_file.write("\t\taverage_bandwidth_utilization=\"0.5\"\n")
            netlist_file.write("\t\tbandwidth=\"" + str(edge_bandwidth) + "\">\n")
            netlist_file.write("\t</net>\n")


netlist_file.write("</netlist>\n")
netlist_file.close()
print("Generated " + identifier + "_def.xml and " + identifier + "_netlist.xml")
