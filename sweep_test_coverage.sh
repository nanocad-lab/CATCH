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
INPUT_NETLIST_FILE="chiplet_16_50_netlist.xml"
INPUT_IO_FILE="io_definitions.xml"
INPUT_LAYER_FILE="layer_definitions.xml"
INPUT_WAFER_FILE="wafer_process_definitions.xml"
INPUT_ASSEMBLY_FILE="assembly_process_definitions.xml"
INPUT_TEST_FILE="test_definitions.xml"

SWEEP="0.84 0.92 0.96 0.98 0.99"
#SWEEP="0.5 0.9 0.95 1.0"

# echo "Creating a temporary file temp_${INPUT_FILE}"
echo "x-axis label: Fault Coverage"
echo "y-axis label: Cost ($)"
echo "Sweep Test Coverage For: ${SWEEP}"
echo "stack: non-scrap scrap"
for coverage in $SWEEP
#organic_25_simultaneous_bonding organic_55_simultaneous_bonding organic_simultaneous_bonding silicon_individual_bonding silicon_45_individual_bonding
do
    # echo "Replacing ${ap} in ${INPUT_FILE}"
    # python search_and_replace.py ${INPUT_FILE} organic_simultaneous_bonding silicon_individual_bonding temp_${INPUT_FILE}
    # python search_and_replace.py temp_${INPUT_FILE} combined_interposer_organic combined_interposer_silicon temp_${INPUT_FILE}
    python search_and_replace.py ${INPUT_FILE} combined_5nm combined_3nm_0.005 temp_${INPUT_FILE}
    python search_and_replace.py temp_${INPUT_FILE} KGD_free_test free_test_${coverage} temp_${INPUT_FILE}

    python load_and_test_design_test_breakdown.py ${INPUT_IO_FILE} ${INPUT_LAYER_FILE} ${INPUT_WAFER_FILE} ${INPUT_ASSEMBLY_FILE} ${INPUT_TEST_FILE} ${INPUT_NETLIST_FILE} temp_${INPUT_FILE}
    # Note that it is possible to replace multiple lines by running search and replace on the output file instead of regenerating from scratch.
    # python search_and_replace.py temp_${INPUT_FILE} <something> <something_else> temp_${INPUT_FILE}
done
rm temp_${INPUT_FILE}
# echo "Temp file removed."
