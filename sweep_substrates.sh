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
# Author: Alexander Graening
# Affiliation: University of California, Los Angeles
# Email: agraening@ucla.edu
# ====================================================================================

INPUT_FILE="chiplet_16_50_def.xml"
INPUT_NETLIST="chiplet_16_50_netlist.xml"

SWEEP="organic silicon glass"
# SWEEP="organic_simultaneous_bonding silicon_individual_bonding"

# echo "Creating a temporary file temp_${INPUT_FILE}"
echo "x-axis label: Substrate"
echo "y-axis label: Cost ($)"
echo "Sweep: ${SWEEP}"
for ap in $SWEEP 
#organic_25_simultaneous_bonding organic_55_simultaneous_bonding organic_simultaneous_bonding silicon_individual_bonding silicon_45_individual_bonding
do
    # echo "Replacing ${ap} in ${INPUT_FILE}"
    if echo "$ap" | grep -q "organic"; then
        # echo "Replacing silicon_individual_bonding with organic_simultaneous_bonding"
        python search_and_replace.py ${INPUT_FILE} silicon_individual_bonding organic_simultaneous_bonding temp_${INPUT_FILE}
        cp ${INPUT_NETLIST} temp_${INPUT_NETLIST}
    elif echo "$ap" | grep -q "silicon"; then
        # echo "Replacing silicon_individual_bonding with silicon_individual_bonding"
        python search_and_replace.py ${INPUT_FILE} silicon_individual_bonding silicon_individual_bonding temp_${INPUT_FILE}
        python search_and_replace.py temp_${INPUT_NETLIST} UCIe_standard UCIe_advanced temp_${INPUT_NETLIST}
    elif echo "$ap" | grep -q "glass"; then
        # echo "Replacing silicon_individual_bonding with silicon_individual_bonding"
        python search_and_replace.py ${INPUT_FILE} silicon_individual_bonding glass_individual_bonding temp_${INPUT_FILE}
        python search_and_replace.py temp_${INPUT_NETLIST} UCIe_standard UCIe_advanced temp_${INPUT_NETLIST}
    else
        echo "Error: ap does not contain silicon, organic, or glass"
        cp ${INPUT_NETLIST} temp_${INPUT_NETLIST}
    fi

    # echo "$ap"
    # If ap includes the word "silicon", then also replace "combined_interposer_silicon" with "combined_interposer_silicon"
    if echo "$ap" | grep -q "silicon"; then
        # echo "Replacing combined_interposer_silicon with combined_interposer_silicon"
        python search_and_replace.py temp_${INPUT_FILE} combined_interposer_silicon combined_interposer_silicon temp_${INPUT_FILE}
        python search_and_replace.py ${INPUT_NETLIST} UCIe_standard UCIe_advanced temp_${INPUT_NETLIST}
    elif echo "$ap" | grep -q "organic"; then
        # echo "Replacing combined_interposer_silicon with combined_interposer_organic"
        python search_and_replace.py temp_${INPUT_FILE} combined_interposer_silicon combined_interposer_organic temp_${INPUT_FILE} 
        cp ${INPUT_NETLIST} temp_${INPUT_NETLIST}
    elif echo "$ap" | grep -q "glass"; then
        # echo "Replacing combined_interposer_silicon with combined_interposer_organic"
        python search_and_replace.py temp_${INPUT_FILE} combined_interposer_silicon combined_interposer_glass temp_${INPUT_FILE} 
        python search_and_replace.py ${INPUT_NETLIST} UCIe_standard UCIe_advanced temp_${INPUT_NETLIST}
    else
        echo "Error: ap does not contain silicon, organic, or glass"
        cp ${INPUT_NETLIST} temp_${INPUT_NETLIST}
    fi

    python load_and_test_design.py io_definitions.xml layer_definitions.xml wafer_process_definitions.xml assembly_process_definitions.xml test_definitions.xml temp_${INPUT_NETLIST} temp_${INPUT_FILE}
    # Note that it is possible to replace multiple lines by running search and replace on the output file instead of regenerating from scratch.
    # python search_and_replace.py temp_${INPUT_FILE} <something> <something_else> temp_${INPUT_FILE}
done
rm temp_${INPUT_FILE}
rm temp_${INPUT_NETLIST}
# echo "Temp file removed."
