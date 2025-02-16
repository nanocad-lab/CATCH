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

INPUT_FILE_PRE="chiplet_"
INPUT_FILE_POST="_def.xml"
INPUT_NETLIST_PRE="chiplet_"
INPUT_NETLIST_POST="_netlist.xml"

SWEEP="2_400 4_200 9_88 16_50 25_32 36_22 49_16 64_12"

QUANTITIES="10000 100000 1000000 10000000"


echo "x-axis label: Count_Size(mm2)"
echo "y-axis label: Cost ($)"
echo "Sweep: ${SWEEP}"
for q in $QUANTITIES
do
    echo "series: ${q}"

    for size in $SWEEP 
    do
        INPUT_FILE="${INPUT_FILE_PRE}${size}${INPUT_FILE_POST}"
        INPUT_NETLIST="${INPUT_NETLIST_PRE}${size}${INPUT_NETLIST_POST}"
        python search_and_replace.py ${INPUT_FILE} 10000000 $q temp_${INPUT_FILE}
        # Extract the part of size before a '_' and set it to a variable
        NUM_CHIPS=$(echo $size | cut -d'_' -f1)
        # Multiply NUM_CHIPS by 10000000 and set it to a variable
        QUANTITY_TO_REPLACE=$(($NUM_CHIPS * 10000000))
        NEW_QUANTITY=$(($NUM_CHIPS * $q))
        python search_and_replace.py temp_${INPUT_FILE} $QUANTITY_TO_REPLACE $NEW_QUANTITY temp_${INPUT_FILE}
        python load_and_test_design.py io_definitions.xml layer_definitions.xml wafer_process_definitions.xml assembly_process_definitions.xml test_definitions.xml ${INPUT_NETLIST} temp_${INPUT_FILE}
        rm temp_${INPUT_FILE}
    done
done
