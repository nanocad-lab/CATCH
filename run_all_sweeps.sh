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
# Filename: run_all_sweeps.sh
# Author: Alexander Graening
# Affiliation: University of California, Los Angeles
# Email: agraening@ucla.edu
# ====================================================================================


# Sweep script for CATCH: a Cost Analysis Tool for Co-optimization of chiplet-based Heterogeneous systems"
# Simply run with sh run_all_sweeps.sh to generate all plots in the paper.

# For sweeps, use python search_and_replace.py <input_file> <string_to_replace> <replacement_string> <output_file>
# Also, clean up temp files to avoid workspace bloat.

echo
echo "Running all sweeps"

echo
python generate_grid_test_files.py 2 UCIe_advanced True False 32 100 0.0
python generate_grid_test_files.py 4 UCIe_advanced True False 32 100 0.0
python generate_grid_test_files.py 9 UCIe_advanced True False 32 100 0.0
python generate_grid_test_files.py 16 UCIe_advanced True False 32 100 0.0
python generate_grid_test_files.py 25 UCIe_advanced True False 32 100 0.0
python generate_grid_test_files.py 36 UCIe_advanced True False 32 100 0.0
python generate_grid_test_files.py 49 UCIe_advanced True False 32 100 0.0
python generate_grid_test_files.py 64 UCIe_advanced True False 32 100 0.0

echo
echo "Sweeping size"
sh sweep_chiplet_size.sh > sweep_chiplet_size_results.txt
cat sweep_chiplet_size_results.txt
python generate_plot.py sweep_chiplet_size_results.txt 0 center line sweep_chiplet_size_results.png
rm sweep_chiplet_size_results.txt

echo
echo "Sweeping defect density"
sh sweep_defect_density.sh > sweep_defect_density_results.txt
cat sweep_defect_density_results.txt
python generate_plot.py sweep_defect_density_results.txt 0 center line sweep_defect_density_results.png
rm sweep_defect_density_results.txt

echo
echo "Sweeping assembly process"
sh sweep_assembly_process.sh > sweep_assembly_process_results.txt
cat sweep_assembly_process_results.txt
python generate_plot.py sweep_assembly_process_results.txt 0 center line sweep_assembly_process_results.png
rm sweep_assembly_process_results.txt

echo
echo "Sweeping NRE"
sh sweep_nre.sh > sweep_nre_results.txt
cat sweep_nre_results.txt
python generate_plot.py sweep_nre_results.txt 0 center line sweep_nre_results.png
rm sweep_nre_results.txt

echo "Cleaning up"
rm chiplet_2_400_def.xml
rm chiplet_2_400_netlist.xml
rm chiplet_4_200_def.xml
rm chiplet_4_200_netlist.xml
rm chiplet_9_88_def.xml
rm chiplet_9_88_netlist.xml
rm chiplet_16_50_def.xml
rm chiplet_16_50_netlist.xml
rm chiplet_25_32_def.xml
rm chiplet_25_32_netlist.xml
rm chiplet_36_22_def.xml
rm chiplet_36_22_netlist.xml
rm chiplet_49_16_def.xml
rm chiplet_49_16_netlist.xml
rm chiplet_64_12_def.xml
rm chiplet_64_12_netlist.xml

# To see the impact of sweeping design quantity to see the impact on NRE for
# a case where a single design unit is repeated homogeneously across the design
# we adjust the design costs as below.
#
# Note that the design cost here increases for smaller dies to account for the
# increasing quantities since different dies are not marked as the same.
# Instead, quantities are inflated.
echo
python generate_grid_test_files.py 2 UCIe_advanced True False 32 100 0.02
python generate_grid_test_files.py 4 UCIe_advanced True False 32 100 0.04
python generate_grid_test_files.py 9 UCIe_advanced True False 32 100 0.09
python generate_grid_test_files.py 16 UCIe_advanced True False 32 100 0.16
python generate_grid_test_files.py 25 UCIe_advanced True False 32 100 0.25
python generate_grid_test_files.py 36 UCIe_advanced True False 32 100 0.36
python generate_grid_test_files.py 49 UCIe_advanced True False 32 100 0.49
python generate_grid_test_files.py 64 UCIe_advanced True False 32 100 0.64

echo
echo "Sweeping NRE"
sh sweep_nre.sh > sweep_nre_design_results.txt
cat sweep_nre_design_results.txt
python generate_plot.py sweep_nre_design_results.txt 0 center line sweep_nre_design_results.png
rm sweep_nre_design_results.txt

echo "Cleaning up"
rm chiplet_2_400_def.xml
rm chiplet_2_400_netlist.xml
rm chiplet_4_200_def.xml
rm chiplet_4_200_netlist.xml
rm chiplet_9_88_def.xml
rm chiplet_9_88_netlist.xml
rm chiplet_16_50_def.xml
rm chiplet_16_50_netlist.xml
rm chiplet_25_32_def.xml
rm chiplet_25_32_netlist.xml
rm chiplet_36_22_def.xml
rm chiplet_36_22_netlist.xml
rm chiplet_49_16_def.xml
rm chiplet_49_16_netlist.xml
rm chiplet_64_12_def.xml
rm chiplet_64_12_netlist.xml

# NRE_1_custom uses a custom test case

echo
echo "Sweeping NRE with a single custom die in a group of 4"
sh sweep_nre_1_custom.sh > sweep_nre_1_custom_results.txt
cat sweep_nre_1_custom_results.txt
python generate_plot.py sweep_nre_1_custom_results.txt 0 center bar sweep_nre_1_custom_results.png
rm sweep_nre_1_custom_results.txt

echo
python generate_grid_test_files.py 16 UCIe_standard True True 10000 100 0.0

echo
echo "Sweep IO reach"
sh sweep_reach.sh > sweep_reach_results.txt
cat sweep_reach_results.txt
python generate_plot.py sweep_reach_results.txt 0 center bar sweep_reach_results.png
rm sweep_reach_results.txt

echo "Cleaning up"
rm chiplet_16_50_def.xml
rm chiplet_16_50_netlist.xml

echo
python generate_grid_test_files.py 16 UCIe_standard True True 32 100 0.0

echo
echo "Sweeping different substrates"
sh sweep_substrates.sh > sweep_substrates_results.txt
cat sweep_substrates_results.txt
python generate_plot.py sweep_substrates_results.txt 0 center bar sweep_substrates_results.png
rm sweep_substrates_results.txt

echo
echo "Sweep test coverage"
sh sweep_test_coverage.sh > sweep_test_coverage_results.txt
cat sweep_test_coverage_results.txt
python generate_plot.py sweep_test_coverage_results.txt 0 center bar sweep_test_coverage_results.png
rm sweep_test_coverage_results.txt

echo
echo "Sweep test coverage immature process"
sh sweep_test_coverage_immature.sh > sweep_test_coverage_immature_results.txt
cat sweep_test_coverage_immature_results.txt
python generate_plot.py sweep_test_coverage_immature_results.txt 0 center bar sweep_test_coverage_immature_results.png
rm sweep_test_coverage_immature_results.txt

echo "Cleaning up"
rm chiplet_16_50_def.xml
rm chiplet_16_50_netlist.xml

# The following sweeps use the same basic testcase.
echo
python generate_grid_test_files_3d.py 16 UCIe_advanced True False 32 100 0.0

echo
echo "Sweep test coverage 3D"
sh sweep_test_coverage.sh > sweep_test_coverage_results.txt
cat sweep_test_coverage_results.txt
python generate_plot.py sweep_test_coverage_results.txt 0 center bar sweep_test_coverage_3d_results.png
rm sweep_test_coverage_results.txt

echo
echo "Sweep test coverage 3D immature process"
sh sweep_test_coverage_immature.sh > sweep_test_coverage_immature_results.txt
cat sweep_test_coverage_immature_results.txt
python generate_plot.py sweep_test_coverage_immature_results.txt 0 center bar sweep_test_coverage_immature_3d_results.png
rm sweep_test_coverage_immature_results.txt

echo "Cleaning up"
rm chiplet_16_50_def.xml
rm chiplet_16_50_netlist.xml
