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

INPUT_FILE="chiplet_nre_study_def.xml"
INPUT_NETLIST="chiplet_nre_study_netlist.xml"

QUANTITIES="10000 100000 1000000 10000000"

echo "x-axis label: New Die Quantity"
echo "y-axis label: Cost ($)"
echo "Sweep: $QUANTITIES"
for q in $QUANTITIES
do
    python search_and_replace.py ${INPUT_FILE} INSERTSWEEPQUANTITY $q temp_${INPUT_FILE}
    python load_and_test_design.py io_definitions.xml layer_definitions.xml wafer_process_definitions.xml assembly_process_definitions.xml test_definitions.xml ${INPUT_NETLIST} temp_${INPUT_FILE}
    rm temp_${INPUT_FILE}
done
