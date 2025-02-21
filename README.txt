=======================================================================
Copyright 2025 UCLA NanoCAD Laboratory

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
=======================================================================
Author: Alexander Graening (agraening@ucla.edu)

====================================
README for Chiplet Cost Model
====================================

General Usage:
python load_and_test_design.py io_definitions.xml layer_definitions.xml wafer_process_definitions.xml assembly_process_definitions.xml test_definitions.xml netlist.xml sip.xml

The above command will run the cost calculation on the demo configuration file sip.xml and demo netlist file netlist.xml

To generate the plots in the paper "CATCH: a Cost Analysis Tool for Co-optimization of chiplet-based Heterogeneous systems" you can launch the script run_all_sweeps.sh
    sh run_all_sweeps.sh

Requirements:
Currently, I am running this using:
    Python 3.10.6
    Numpy 1.25.0
    xml.etree.ElementTree 1.3.0
    matplotlib 3.10.0 (for plotting sweeps)


====================================
Included Files:
====================================

design.py
    Contains class definitions for the chip class that is core to the model along with class definitions for layers, IOs, testing processes, wafer processes, and assembly methods.

generate_grid_test_files.py
    This is used to generate the netlist and system definition files for the 800mm^2 testcase. The chiplets are placed next to each other on an interposer.

generate_grid_test_files_3D.py
    This is used to generate the netlist and system definition files for the 800mm^2 testcase. The chiplets are stacked on top of each other in a single stack.

load_and_test_design.py
    This is used to pass file names as an argument and build the system. This also prints out the computed system information.

load_and_test_design_test_breakdown.py
    This is a variation of the above file to split the cost into scrap cost and non-scrap cost for plotting.

readDesignFromFile.py
    Functions for reading xml files into the dictionary format and processing into the class structure are included here.

search_and_replace.py
    This simply takes an input file and replaces one string with another. This is used to modify the configuration files to run sweeps.

sip.xml
    Demo system definition file

netlist.xml
    Demo netlist file

io_definitions.xml
    IO definitions file

layer_definitions.xml
    Layer definition file. This contains both "combined" layers that model a full stackup and individual layers such as metal and active layers to build a full stackup based on number of required metal layers.

test_definitions.xml
    Test process definition file. This contains the constants necessary to compute testing cost and to compute a testing method aware yield.

wafer_process_definitions.xml
    This contains the constants that are generally shared about parameters such as reticle size and wafer processing yield.

assembly_process_definitions.xml
    This contains definitions of constants necessary for computing the assembly cost and yield impact.

chiplet_nre_study_def.xml and chiplet_nre_study_netlist.xml
    Configuration files for study with a single low volume chip in a design with 3 high volume chips.

run_all_sweeps.sh
    Runs all sweep scripts.

sweep_assembly_process.sh
    Runs sweep on the assembly process across different 800mm2 homogeneous graph processor test cases.

sweep_chiplet_size.sh
    Runs sweep of different 800mm2 homogeneous graph processor test cases for different process technology nodes.

sweep_defect_density.sh
    Runs sweep defect density across different 800mm2 homogeneous graph processor test cases.

sweep_nre.sh
    Runs sweep of different quantities across different 800mm2 homogeneous graph processor test cases without.

sweep_nre_1_custom.sh
    Runs a sweep of quantity for a design with a single low-volume die and 3 high volume dies.

sweep_reach.sh
    Runs a sweep of reach across a testcase.

sweep_substrates.sh
    Compares organic, silicon, and glass for one example.

sweep_test_coverage.sh
    Sweeps test coverage at the "typical" defect density used for the paper.

sweep_test_coverage_immature.sh
    Sweeps test coverage at an elevated defect density.


====================================
General Summary
====================================

The general organization of the code:
 - Class definitions and model functions are included in design.py
 - Functions for reading the design are included in readDesignFromFile.py
 - load_and_test_design.py is a wrapper that makes this easier to use to test a single design.
 - Example sweeps are included in distinct .sh scripts and can all be run by launching run_all_sweeps.sh

Modify or create new .xml files to evaluate new systems and processes. To add new considerations, edit the corresponding class in design.py.
