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
# Filename: design.py
# Author: Alexander Graening
# Affiliation: University of California, Los Angeles
# Email: agraening@ucla.edu
#
# Description: This file contains the class definitions and functions for the cost model.
#              Note that changing the definition of a class also requires modifications in 
#              readDesignFromFile.py and the associated .xml file(s). More substantial
#              changes may also require modifications to load_and_test_design.py.
# ====================================================================================

import numpy as np
import math
import sys
import random
import xml.etree.ElementTree as ET


# =========================================
# Wafer Process Class
# =========================================
# The class has the following attributes:
#   name: The name of the wafer process.
#   wafer_diameter: The diameter of the wafer in mm.
#   edge_exclusion: The edge exclusion of the wafer in mm.
#   wafer_process_yield: The yield of the wafer process. Value should be between 0 and 1.
#   reticle_x: Reticle dimension in the x dimension in mm.
#   reticle_y: Reticle dimension in the y dimension in mm.
#   wafer_fill_grid: Whether the wafer is filled in a grid pattern or in a line pattern
#       that ignores vertical alignment in dicing.
#   nre_front_end_cost_per_mm2_memory: The NRE design cost per mm^2 of the front end of
#       the wafer process for memory. (Front end refers to higher level design steps.)
#   nre_back_end_cost_per_mm2_memory: The NRE design cost per mm^2 of the back end of
#       the wafer process for memory. (Back end refers to lower level design steps.)
#   nre_front_end_cost_per_mm2_logic: The NRE design cost per mm^2 of the front end of
#       the wafer process for logic. (Front end refers to higher level design steps.)
#   nre_back_end_cost_per_mm2_logic: The NRE design cost per mm^2 of the back end of
#       the wafer process for logic. (Back end refers to lower level design steps.)
#   nre_front_end_cost_per_mm2_analog: The NRE design cost per mm^2 of the front end of
#       the wafer process for analog. (Front end refers to higher level design steps.)
#   nre_back_end_cost_per_mm2_analog: The NRE design cost per mm^2 of the back end of
#       the wafer process for analog. (Back end refers to lower level design steps.)
#   static: A boolean set true when the process is defined to prevent further changes.
# =========================================
# The class has the following methods.
#   set_static()
#   an initialization function, get/set parameter functions, and cast to string of the object to print a description.
# =========================================

class WaferProcess:
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) != str:
                print("Error: Wafer process name must be a string.")
                return 1
            else:
                self.__name = value    
                return 0
        
    @property
    def wafer_diameter(self):
        return self.__wafer_diameter
    
    @wafer_diameter.setter
    def wafer_diameter(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Wafer diameter must be a number.")
                return 1
            elif value < 0:
                print("Error: Wafer diameter must be nonnegative.")
                return 1
            else:
                self.__wafer_diameter = value
                return 0

    @property
    def edge_exclusion(self):
        return self.__edge_exclusion
    
    @edge_exclusion.setter
    def edge_exclusion(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Edge exclusion must be a number.")
                return 1
            elif value < 0:
                print("Error: Edge exclusion must be nonnegative.")
                return 1
            elif value > self.wafer_diameter/2:
                print("Error: Edge exclusion must be less than half the wafer diameter.")
                return 1
            else:
                self.__edge_exclusion = value
                return 0
        
    @property
    def wafer_process_yield(self):
        return self.__wafer_process_yield
    
    @wafer_process_yield.setter
    def wafer_process_yield(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Wafer process yield must be a number.")
                return 1
            elif value < 0.0 or value > 1.0:
                print("Error: Wafer process yield must be between 0 and 1.")
                return 1
            else:
                self.__wafer_process_yield = value
                return 0

    @property
    def dicing_distance(self):
        return self.__dicing_distance
    
    @dicing_distance.setter
    def dicing_distance(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Dicing distance must be a number.")
                return 1
            elif value < 0:
                print("Error: Dicing distance must be nonnegative.")
                return 1
            elif value > self.wafer_diameter/2:
                print("Error: Dicing distance must be less than half the wafer diameter.")
                return 1
            else:
                self.__dicing_distance = value
                return 0
        
    @property
    def reticle_x(self):
        return self.__reticle_x
    
    @reticle_x.setter
    def reticle_x(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Reticle x dimension must be a number.")
                return 1
            elif value < 0:
                print("Error: Reticle x dimension must be nonnegative.")
                return 1
            elif value > self.wafer_diameter/2:
                print("Error: Reticle x dimension must be less than half the wafer diameter.")
                return 1
            else:
                self.__reticle_x = value
                return 0

    @property
    def reticle_y(self):
        return self.__reticle_y
    
    @reticle_y.setter
    def reticle_y(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Reticle y dimension must be a number.")
                return 1
            elif value < 0:
                print("Error: Reticle y dimension must be nonnegative.")
                return 1
            elif value > self.wafer_diameter/2:
                print("Error: Reticle y dimension must be less than half the wafer diameter.")
                return 1
            else:
                self.__reticle_y = value
                return 0
        
    @property
    def wafer_fill_grid(self):
        return self.__wafer_fill_grid
    
    @wafer_fill_grid.setter
    def wafer_fill_grid(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) != str:
                print("Error: Wafer fill grid must be a string. (True or False)")
            if value.lower() == "true":
                self.__wafer_fill_grid = True
            else:
                self.__wafer_fill_grid = False
            return 0
        
    @property
    def nre_front_end_cost_per_mm2_memory(self):
        return self.__nre_front_end_cost_per_mm2_memory
    
    @nre_front_end_cost_per_mm2_memory.setter
    def nre_front_end_cost_per_mm2_memory(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: NRE front end cost per mm^2 memory must be a number.")
                return 1
            elif value < 0:
                print("Error: NRE front end cost per mm^2 memory must be nonnegative.")
                return 1
            else:
                self.__nre_front_end_cost_per_mm2_memory = value
                return 0

    @property
    def nre_back_end_cost_per_mm2_memory(self):
        return self.__nre_back_end_cost_per_mm2_memory
    
    @nre_back_end_cost_per_mm2_memory.setter
    def nre_back_end_cost_per_mm2_memory(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: NRE back end cost per mm^2 memory must be a number.")
                return 1
            elif value < 0:
                print("Error: NRE back end cost per mm^2 memory must be nonnegative.")
                return 1
            else:
                self.__nre_back_end_cost_per_mm2_memory = value
                return 0
        
    @property
    def nre_front_end_cost_per_mm2_logic(self):
        return self.__nre_front_end_cost_per_mm2_logic
    
    @nre_front_end_cost_per_mm2_logic.setter
    def nre_front_end_cost_per_mm2_logic(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: NRE front end cost per mm^2 logic must be a number.")
                return 1
            elif value < 0:
                print("Error: NRE front end cost per mm^2 logic must be nonnegative.")
                return 1
            else:
                self.__nre_front_end_cost_per_mm2_logic = value
                return 0
        
    @property
    def nre_back_end_cost_per_mm2_logic(self):
        return self.__nre_back_end_cost_per_mm2_logic
    
    @nre_back_end_cost_per_mm2_logic.setter
    def nre_back_end_cost_per_mm2_logic(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: NRE back end cost per mm^2 logic must be a number.")
                return 1
            elif value < 0:
                print("Error: NRE back end cost per mm^2 logic must be nonnegative.")
                return 1
            else:
                self.__nre_back_end_cost_per_mm2_logic = value
                return 0
        
    @property
    def nre_front_end_cost_per_mm2_analog(self):
        return self.__nre_front_end_cost_per_mm2_analog
    
    @nre_front_end_cost_per_mm2_analog.setter
    def nre_front_end_cost_per_mm2_analog(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: NRE front end cost per mm^2 analog must be a number.")
                return 1
            elif value < 0:
                print("Error: NRE front end cost per mm^2 analog must be nonnegative.")
                return 1
            else:
                self.__nre_front_end_cost_per_mm2_analog = value
                return 0
        
    @property
    def nre_back_end_cost_per_mm2_analog(self):
        return self.__nre_back_end_cost_per_mm2_analog
    
    @nre_back_end_cost_per_mm2_analog.setter
    def nre_back_end_cost_per_mm2_analog(self, value):
        if (self.static):
            print("Error: Cannot change static wafer process.")
            return 1
        else:
            if type(value) == str:
                print("Error: NRE back end cost per mm^2 analog must be a number.")
                return 1
            elif value < 0:
                print("Error: NRE back end cost per mm^2 analog must be nonnegative.")
                return 1
            else:
                self.__nre_back_end_cost_per_mm2_analog = value
                return 0
        
    @property
    def static(self):
        return self.__static
    
    @static.setter
    def static(self, value):
        self.__static = value

    def __str__(self) -> str:
        return_str = "Wafer Process Name: " + self.name
        return_str += "\n\r\tWafer Diameter: " + str(self.wafer_diameter)
        return_str += "\n\r\tEdge Exclusion: " + str(self.edge_exclusion)
        return_str += "\n\r\tWafer Process Yield: " + str(self.wafer_process_yield) 
        return_str += "\n\r\tReticle X: " + str(self.reticle_x)
        return_str += "\n\r\tReticle Y: " + str(self.reticle_y)
        return_str += "\n\r\tWafer Fill Grid: " + str(self.wafer_fill_grid)
        return_str += "\n\r\tNRE Front End Cost Per mm^2 Memory: " + str(self.nre_front_end_cost_per_mm2_memory)
        return_str += "\n\r\tNRE Back End Cost Per mm^2 Memory: " + str(self.nre_back_end_cost_per_mm2_memory)
        return_str += "\n\r\tNRE Front End Cost Per mm^2 Logic: " + str(self.nre_front_end_cost_per_mm2_logic)
        return_str += "\n\r\tNRE Back End Cost Per mm^2 Logic: " + str(self.nre_back_end_cost_per_mm2_logic)
        return_str += "\n\r\tNRE Front End Cost Per mm^2 Analog: " + str(self.nre_front_end_cost_per_mm2_analog)
        return_str += "\n\r\tNRE Back End Cost Per mm^2 Analog: " + str(self.nre_back_end_cost_per_mm2_analog)
        return_str += "\n\r\tStatic: " + str(self.static)
        return return_str

    def wafer_fully_defined(self) -> bool:
        if (self.name is None or self.wafer_diameter is None or self.edge_exclusion is None or 
                self.wafer_process_yield is None or self.reticle_x is None or self.reticle_y is None or 
                self.wafer_fill_grid is None or self.nre_front_end_cost_per_mm2_memory is None or 
                self.nre_back_end_cost_per_mm2_memory is None or self.nre_front_end_cost_per_mm2_logic is None or 
                self.nre_back_end_cost_per_mm2_logic is None or self.nre_front_end_cost_per_mm2_analog is None or 
                self.nre_back_end_cost_per_mm2_analog is None):
            return False
        else:
            return True

    def set_static(self) -> int:
        if not self.wafer_fully_defined():
            print("Error: Attempt to set wafer process static without defining all parameters. Exiting...")
            print(self)
            sys.exit(1)
        self.static = True
        return 0

    def __init__(self, name = None, wafer_diameter = None, edge_exclusion = None, wafer_process_yield = None,
                 dicing_distance = None, reticle_x = None, reticle_y = None, wafer_fill_grid = None,
                 nre_front_end_cost_per_mm2_memory = None, nre_back_end_cost_per_mm2_memory = None,
                 nre_front_end_cost_per_mm2_logic = None, nre_back_end_cost_per_mm2_logic = None,
                 nre_front_end_cost_per_mm2_analog = None, nre_back_end_cost_per_mm2_analog = None, static = True) -> None:
        self.static = False
        self.name = name
        self.wafer_diameter = wafer_diameter
        self.edge_exclusion = edge_exclusion
        self.wafer_process_yield = wafer_process_yield
        self.dicing_distance = dicing_distance
        self.reticle_x = reticle_x
        self.reticle_y = reticle_y
        self.wafer_fill_grid = wafer_fill_grid
        self.nre_front_end_cost_per_mm2_memory = nre_front_end_cost_per_mm2_memory
        self.nre_back_end_cost_per_mm2_memory = nre_back_end_cost_per_mm2_memory
        self.nre_front_end_cost_per_mm2_logic = nre_front_end_cost_per_mm2_logic
        self.nre_back_end_cost_per_mm2_logic = nre_back_end_cost_per_mm2_logic
        self.nre_front_end_cost_per_mm2_analog = nre_front_end_cost_per_mm2_analog
        self.nre_back_end_cost_per_mm2_analog = nre_back_end_cost_per_mm2_analog
        self.static = static
        if not self.wafer_fully_defined():
            print("Warning: Wafer Process not fully defined, setting to non-static.")
            self.static = False
            print(self)
        return


# =========================================
# IO Class
# =========================================
# The class has the following attributes:
#   type: The type of IO for this adjacency matrix. (Select from list of IO definitions.)
#   rx_area: The area of RX IOs in mm^2.
#   tx_area: The area of TX IOs in mm^2
#   shoreline: The shoreline of the IO in mm.
#   bandwidth: The bandwidth of the IO in Gbps.
#   wire_count: The number of wires in the IO.
#   bidirectional: Whether the IO is bidirectional or not.
#   energy_per_bit: The energy per bit of the IO in pJ/bit.
#   reach: The reach of the IO in mm.
#   static: A boolean set true when the IO is defined to prevent further changes.
# =========================================
# The class has the following methods.
#   set_static()
#   an initialization function, get/set parameter functions, and cast to strin of the objectg to print a description.
# =========================================


class IO:
    @property
    def type(self):
        return self.__type

    @type.setter
    def type(self, value):
        if (self.static):
            print("Error: Cannot change static IO.")
            return 1
        else:
            if type(value) != str:
                print("Error: IO type must be a string.")
                return 1
            else:
                self.__type = value
                return 0

    @property
    def rx_area(self):
        return self.__rx_area

    @rx_area.setter
    def rx_area(self, value):
        if (self.static):
            print("Error: Cannot change static IO.")
            return 1
        else:
            if type(value) == str:
                print("Error: RX area must be a number.")
                return 1
            elif value < 0:
                print("Error: RX area must be nonnegative.")
                return 1
            else:
                self.__rx_area = value
                return 0

    @property
    def tx_area(self):
        return self.__tx_area

    @tx_area.setter
    def tx_area(self, value):
        if (self.static):
            print("Error: Cannot change static IO.")
            return 1
        else:
            if type(value) == str:
                print("Error: TX area must be a number.")
                return 1
            elif value < 0:
                print("Error: TX area must be nonnegative.")
                return 1
            else:
                self.__tx_area = value
                return 0

    @property
    def shoreline(self):
        return self.__shoreline

    @shoreline.setter
    def shoreline(self, value):
        if (self.static):
            print("Error: Cannot change static IO.")
            return 1
        else:
            if type(value) == str:
                print("Error: Shoreline must be a number.")
                return 1
            elif value < 0:
                print("Error: Shoreline must be nonnegative.")
                return 1
            else:
                self.__shoreline = value
                return 0

    @property
    def bandwidth(self):
        return self.__bandwidth

    @bandwidth.setter
    def bandwidth(self, value):
        if (self.static):
            print("Error: Cannot change static IO.")
            return 1
        else:
            if type(value) == str:
                print("Error: Bandwidth must be a number.")
                return 1
            elif value < 0:
                print("Error: Bandwidth must be nonnegative.")
                return 1
            else:
                self.__bandwidth = value
                return 0

    @property
    def wire_count(self):
        return self.__wire_count

    @wire_count.setter
    def wire_count(self, value):
        if (self.static):
            print("Error: Cannot change static IO.")
            return 1
        else:
            if type(value) == str:
                print("Error: Wire count must be a number.")
                return 1
            elif value < 0:
                print("Error: Wire count must be nonnegative.")
                return 1
            else:
                self.__wire_count = value
                return 0

    @property
    def bidirectional(self):
        return self.__bidirectional
    
    @bidirectional.setter
    def bidirectional(self, value):
        if (self.static):
            print("Error: Cannot change static IO.")
            return 1
        else:
            if type(value) != str:
                print("Error: Bidirectional must be a string. (True or False)")
                return 1
            else:
                if value.lower() == "true":
                    self.__bidirectional = True
                else:
                    self.__bidirectional = False
                return 0

    @property
    def energy_per_bit(self):
        return self.__energy_per_bit

    @energy_per_bit.setter
    def energy_per_bit(self, value):
        if (self.static):
            print("Error: Cannot change static IO.")
            return 1
        else:
            if type(value) == str:
                print("Error: Energy per bit must be a number.")
                return 1
            elif value < 0:
                print("Error: Energy per bit must be nonnegative.")
                return 1
            else:
                self.__energy_per_bit = value
                return 0

    @property
    def reach(self):
        return self.__reach

    @reach.setter
    def reach(self, value):
        if (self.static):
            print("Error: Cannot change static IO.")
            return 1
        else:
            if type(value) == str:
                print("Error: Reach must be a number.")
                return 1
            elif value < 0:
                print("Error: Reach must be nonnegative.")
                return 1
            else:
                self.__reach = value
                return 0

    @property
    def static(self):
        return self.__static

    @static.setter
    def static(self, value):
        self.__static = value

    def __str__(self) -> str:
        return_str = "IO Type: " + self.type
        return_str += "\n\r\tRX Area: " + str(self.rx_area)
        return_str += "\n\r\tTX Area: " + str(self.tx_area)
        return_str += "\n\r\tShoreline: " + str(self.shoreline)
        return_str += "\n\r\tBandwidth: " + str(self.bandwidth)
        return_str += "\n\r\tWire Count: " + str(self.wire_count)
        return_str += "\n\r\tBidirectional: " + str(self.bidirectional)
        return_str += "\n\r\tEnergy Per Bit: " + str(self.energy_per_bit)
        return_str += "\n\r\tReach: " + str(self.reach)
        return_str += "\n\r\tStatic: " + str(self.static)
        return return_str
    
    def io_fully_defined(self) -> bool:
        if (self.type is None or self.rx_area is None or self.tx_area is None or self.shoreline is None or 
                self.bandwidth is None or self.wire_count is None or self.bidirectional is None or 
                self.energy_per_bit is None or self.reach is None):
            return False
        else:
            return True

    def set_static(self) -> int:
        if not self.io_fully_defined():
            print("Error: Attempt to set IO static without defining all parameters. Exiting...")
            print(self)
            sys.exit(1)
        self.static = True
        return 0

    def __init__(self, type = None, rx_area = None, tx_area = None, shoreline = None, bandwidth = None,
                 wire_count = None, bidirectional = None, energy_per_bit = None, reach = None,
                 static = True) -> None:
        self.static = False
        self.type = type
        self.rx_area = rx_area
        self.tx_area = tx_area
        self.shoreline = shoreline
        self.bandwidth = bandwidth
        self.wire_count = wire_count
        self.bidirectional = bidirectional
        self.bidirectional = bidirectional
        self.energy_per_bit = energy_per_bit
        self.reach = reach
        self.static = static
        if not self.io_fully_defined():
            print("Warning: IO not fully defined, setting to non-static.")
            self.static = False
            print(self)
        return


# =========================================
# Layer Class
# =========================================
# The class consists of the following attributes:
#   name: The name of the layer.
#   active: Whether the layer is active or not.
#   cost_per_mm2: The cost per mm^2 of the layer.
#   defect_density: The defect density of the layer.
#   critical_area_ratio: The critical area ratio of the layer.
#   clustering_factor: The clustering factor of the layer.
#   transistor_density: The transistor density of the layer in millions per mm^2.
#   litho_percent: The litho percent of the layer.
#   nre_mask_cost: The mask cost of the layer.
#   stitching_yield: The stitching yield of the layer.
#   static: A boolean set true when the layer is defined to prevent further changes.
# =========================================
# The class has the following methods.
#   set_static()
#   initialization function, get/set parameter functions, and cast to string of the object to print a description.
# == Computation ==
#   layer_yield(float): Computes the yield of the layer given the area of the layer.
#   reticle_utilization(float,float,float): Computes the reticle utilization given the area of the layer,
#                                           the reticle x dimension, and the reticle y dimension.
#   layer_cost(float,float,float): Computes the cost of the layer given the area of the layer, the reticle x dimension,
#                                  and the reticle y dimension.
# =========================================

class Layer:
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if (self.static):
            print("Error: Cannot change static layer.")
            return 1
        else:
            if type(value) != str:
                print("Error: Layer name must be a string.")
                return 1
            else:
                self.__name = value
                return 0

    @property
    def active(self):
        return self.__active

    @active.setter
    def active(self, value):
        if (self.static):
            print("Error: Cannot change static layer.")
            return 1
        else:
            if type(value) != str:
                print("Error: Active must be a string. (True or False)")
                return 1
            else:
                if value.lower() == "true":
                    self.__active = True
                else:
                    self.__active = False
                return 0

    @property
    def cost_per_mm2(self):
        return self.__cost_per_mm2

    @cost_per_mm2.setter
    def cost_per_mm2(self, value):
        if (self.static):
            print("Error: Cannot change static layer.")
            return 1
        else:
            if type(value) == str:
                print("Error: Cost per mm^2 must be a number.")
                return 1
            elif value < 0:
                print("Error: Cost per mm^2 must be nonnegative.")
                return 1
            else:
                self.__cost_per_mm2 = value
                return 0

    @property
    def transistor_density(self):
        return self.__transistor_density

    @transistor_density.setter
    def transistor_density(self, value):
        if (self.static):
            print("Error: Cannot change static layer.")
            return 1
        else:
            if type(value) == str:
                print("Error: Transistor density must be a number.")
                return 1
            elif value < 0:
                print("Error: Transistor density must be nonnegative.")
                return 1
            else:
                self.__transistor_density = value
                return 0

    def get_gates_per_mm2(self) -> float:
        # Transistor density is in million transistors per mm^2. Divide by 4 (assuming 4-transistor NAND and NOR gates) to get gates per mm^2.
        return self.transistor_density*1e6/4

    @property
    def defect_density(self):
        return self.__defect_density

    @defect_density.setter
    def defect_density(self, value):
        if (self.static):
            print("Error: Cannot change static layer.")
            return 1
        else:
            if type(value) == str:
                print("Error: Defect density must be a number.")
                return 1
            elif value < 0:
                print("Error: Defect density must be nonnegative.")
                return 1
            else:
                self.__defect_density = value
                return 0

    @property
    def critical_area_ratio(self):
        return self.__critical_area_ratio

    @critical_area_ratio.setter
    def critical_area_ratio(self, value):
        if (self.static):
            print("Error: Cannot change static layer.")
            return 1
        else:
            if type(value) == str:
                print("Error: Critical area ratio must be a number.")
                return 1
            elif value < 0:
                print("Error: Critical area ratio must be nonnegative.")
                return 1
            else:
                self.__critical_area_ratio = value
                return 0

    @property
    def clustering_factor(self):
        return self.__clustering_factor

    @clustering_factor.setter
    def clustering_factor(self, value):
        if (self.static):
            print("Error: Cannot change static layer.")
            return 1
        else:
            if type(value) == str:
                print("Error: Clustering factor must be a number.")
                return 1
            elif value < 0:
                print("Error: Clustering factor must be nonnegative.")
                return 1
            else:
                self.__clustering_factor = value
                return 0

    @property
    def litho_percent(self):
        return self.__litho_percent

    @litho_percent.setter
    def litho_percent(self, value):
        if (self.static):
            print("Error: Cannot change static layer.")
            return 1
        else:
            if type(value) == str:
                print("Error: Litho percent must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Litho percent must be between 0 and 1.")
                return 1
            else:
                self.__litho_percent = value
                return 0

    @property
    def mask_cost(self):
        return self.__mask_cost

    @mask_cost.setter
    def mask_cost(self, value):
        if (self.static):
            print("Error: Cannot change static layer.")
            return 1
        else:
            if type(value) == str:
                print("Error: Mask cost must be a number.")
                return 1
            elif value < 0:
                print("Error: Mask cost must be nonnegative.")
                return 1
            else:
                self.__mask_cost = value
                return 0

    @property
    def stitching_yield(self):
        return self.__stitching_yield

    @stitching_yield.setter
    def stitching_yield(self, value):
        if (self.static):
            print("Error: Cannot change static layer.")
            return 1
        else:
            if type(value) == str:
                print("Error: Stitching yield must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Stitching yield must be between 0 and 1.")
                return 1
            else:
                self.__stitching_yield = value
                return 0

    @property
    def static(self):
        return self.__static

    @static.setter
    def static(self, value):
        self.__static = value

    def __str__(self) -> str:
        return_str = "Layer Name: " + self.name
        return_str += "\n\r\tActive: " + str(self.active)
        return_str += "\n\r\tCost Per mm^2: " + str(self.cost_per_mm2)
        return_str += "\n\r\tTransistor Density: " + str(self.transistor_density)
        return_str += "\n\r\tDefect Density: " + str(self.defect_density)
        return_str += "\n\r\tCritical Area Ratio: " + str(self.critical_area_ratio)
        return_str += "\n\r\tClustering Factor: " + str(self.clustering_factor)
        return_str += "\n\r\tLitho Percent: " + str(self.litho_percent)
        return_str += "\n\r\tMask Cost: " + str(self.mask_cost)
        return_str += "\n\r\tStitching Yield: " + str(self.stitching_yield)
        return_str += "\n\r\tStatic: " + str(self.static)
        return return_str

    def layer_fully_defined(self) -> bool:
        if (self.name is None or self.active is None or self.cost_per_mm2 is None or self.transistor_density is None or
                    self.defect_density is None or self.critical_area_ratio is None or self.clustering_factor is None or
                    self.litho_percent is None or self.mask_cost is None or self.stitching_yield is None):
            return False
        else:
            return True

    def set_static(self) -> int:
        if not self.layer_fully_defined():
            print("Error: Attempt to set layer static without defining all parameters. Exiting...")
            print(self)
            sys.exit(1)
        self.static = True
        return 0

    def __init__(self, name = None, active = None, cost_per_mm2 = None, transistor_density = None, defect_density = None,
                 critical_area_ratio = None, clustering_factor = None, litho_percent = None, mask_cost = None,
                 stitching_yield = None, static = True) -> None:
        self.static = False
        self.name = name
        self.active = active
        self.cost_per_mm2 = cost_per_mm2
        self.transistor_density = transistor_density
        self.defect_density = defect_density
        self.critical_area_ratio = critical_area_ratio
        self.clustering_factor = clustering_factor
        self.litho_percent = litho_percent
        self.mask_cost = mask_cost
        self.stitching_yield = stitching_yield
        self.static = static
        if not self.layer_fully_defined():
            print("Warning: Layer not fully defined. Setting non-static.")
            self.static = False
            print(self)
        return

    # ========== Computation Functions =========

    def layer_yield(self,area) -> float:
        num_stitches = 0
        defect_yield = (1+(self.defect_density*area*self.critical_area_ratio)/self.clustering_factor)**(-1*self.clustering_factor)
        stitching_yield = self.stitching_yield**num_stitches
        final_layer_yield = stitching_yield*defect_yield
        return final_layer_yield

    def reticle_utilization(self,area,reticle_x,reticle_y) -> float:
        reticle_area = reticle_x*reticle_y
        # If the area is larger than the reticle area, this requires stitching. To get the reticle utilization,
        #  increase the reticle area to the lowest multiple of the reticle area that will fit the stitched chip.
        while reticle_area < area:
            reticle_area += reticle_x*reticle_y
        number_chips_in_reticle = reticle_area//area
        unutilized_reticle = (reticle_area) - number_chips_in_reticle*area
        reticle_utilization = (reticle_area - unutilized_reticle)/(reticle_area)
        return reticle_utilization

    # Compute the cost of the layer given area and chip dimensions.
    def layer_cost(self,area,aspect_ratio,wafer_process) -> float:
        # If area is 0, the cost is 0.
        if area == 0:
            layer_cost = 0
            
        # For valid nonzero area, compute the cost.
        elif area > 0:
            # Compute the cost of the layer before considering scaling of lithography costs with reticle fit.
            layer_cost = area*self.compute_cost_per_mm2(area,aspect_ratio,wafer_process)

            # Get utilization based on reticle fit.
            # Edge case to avoid division by zero.
            if (self.litho_percent == 0.0):
                reticle_utilization = 1.0
            elif (self.litho_percent > 0.0):
                reticle_utilization = self.reticle_utilization(area,wafer_process.reticle_x,wafer_process.reticle_y)
            # A negative percent does not make sense and should crash the program.
            else:
                print("Error: Negative litho percent in Layer.layer_cost(). Exiting...")
                sys.exit(1)

            # Scale the lithography component of cost by the reticle utilization.
            layer_cost = layer_cost*(1-self.litho_percent) + (layer_cost*self.litho_percent)/reticle_utilization

        # Negative area does not make sense and should crash the program.
        else:
            print("Error: Negative area in Layer.layer_cost(). Exiting...")
            sys.exit(1)

        return layer_cost

    def compute_grid_dies_per_wafer(self, x_dim, y_dim, usable_wafer_diameter, dicing_distance):
        x_dim_eff = x_dim + dicing_distance
        y_dim_eff = y_dim + dicing_distance
        best_dies_per_wafer = 0
        best_die_locations = []
        left_column_height = 1
        first_row_height = y_dim_eff/2
        r = usable_wafer_diameter/2
        first_column_dist = r - math.sqrt(r**2 - (first_row_height)**2)
        crossover_column_height = math.sqrt(r**2 - (r-first_column_dist-x_dim_eff)**2)
        while left_column_height*y_dim_eff/2 < crossover_column_height:
            dies_per_wafer = 0
            die_locations = []
            # Get First Row or Block of Rows
    
            row_chord_height = (left_column_height*y_dim_eff/2) - dicing_distance/2
            chord_length = math.sqrt(r**2 - (row_chord_height)**2)*2
            num_dies_in_row = math.floor((chord_length+dicing_distance)/x_dim_eff)
            dies_per_wafer += num_dies_in_row*left_column_height    
            for j in range(num_dies_in_row):
                x = j*x_dim_eff - chord_length/2
                for i in range(left_column_height):
                    y = y_dim_eff*i - row_chord_height
                    # if x**2 + y**2 <= r**2:
                    die_locations.append((x, y))
            row_chord_height += y_dim_eff
    
            # Add correction for the far side of the wafer.
            end_of_rows = num_dies_in_row*x_dim_eff - chord_length/2
            for i in range(left_column_height):
                y = y_dim_eff*i - row_chord_height + y_dim_eff
                if (end_of_rows + x_dim_eff)**2 + y**2 <= r**2 and (end_of_rows + x_dim_eff)**2 + (y + y_dim_eff)**2 <= r**2:
                    dies_per_wafer += 1
                    die_locations.append((end_of_rows, y))
    
            starting_distance_from_left = (usable_wafer_diameter - chord_length)/2
            while row_chord_height < usable_wafer_diameter/2:
                #chord_length = math.sqrt(r**2 - row_chord_height**2)*2
                chord_length = math.sqrt(r**2 - row_chord_height**2)*2
    
                # Compute how many squares over from the first square it is possible to fit an other square on top.
                location_of_first_fit_candidate = (usable_wafer_diameter - chord_length)/2
                starting_location = math.ceil((location_of_first_fit_candidate - starting_distance_from_left)/x_dim_eff)*x_dim_eff + starting_distance_from_left
                # die_locations.append((starting_location-usable_wafer_diameter/2, row_chord_height-y_dim_eff))
                effective_cord_length = chord_length - (starting_location - location_of_first_fit_candidate)
                dies_per_wafer += 2*math.floor(effective_cord_length/x_dim_eff)
                for j in range(math.floor(effective_cord_length/x_dim_eff)):
                    x = starting_location + j*x_dim_eff - usable_wafer_diameter/2
                    y = row_chord_height - y_dim_eff
                    # if x**2 + y**2 <= r**2:
                    die_locations.append((x, y))
                    die_locations.append((x, -1*y-y_dim_eff))
                row_chord_height += y_dim_eff
    
            #print(dies_per_wafer)
            #plot_dies_on_wafer(die_locations, x_dim, y_dim, usable_wafer_diameter)
    
            if dies_per_wafer > best_dies_per_wafer:
                best_dies_per_wafer = dies_per_wafer
                best_die_locations = die_locations
            left_column_height = left_column_height + 1
    
        #print("Best Dies Per Wafer: ")
        #print(best_dies_per_wafer)
        #plot_dies_on_wafer(best_die_locations, x_dim, y_dim, usable_wafer_diameter)
    
        return best_dies_per_wafer
    
#    def compute_grid_dies_per_wafer(self, x_dim, y_dim, usable_wafer_diameter, dicing_distance):
#        x_dim_eff = x_dim + dicing_distance
#        y_dim_eff = y_dim + dicing_distance
#        best_dies_per_wafer = 0
#        left_column_height = 1
#        first_row_height = y_dim_eff/2
#        r = usable_wafer_diameter/2
#        first_column_dist = r - math.sqrt(r**2 - (first_row_height)**2)
#        crossover_column_height = math.sqrt(r**2 - (r-first_column_dist-x_dim_eff)**2)
#        while left_column_height*y_dim_eff/2 < crossover_column_height:
#            dies_per_wafer = 0
#            # Get First Row or Block of Rows
#
#            row_chord_height = left_column_height*y_dim_eff/2
#            chord_length = math.sqrt(r**2 - (row_chord_height - dicing_distance/2)**2)*2 + dicing_distance
#            dies_per_wafer += math.floor(chord_length/x_dim_eff)*left_column_height
#            row_chord_height += left_column_height
#
#            # Add correction for the far side of the wafer.
#            # TODO: Revisit and check results for this section of code.
#            counter = left_column_height - 2
#            extra_columns = 0
#            while counter > 0:
#                temp_chord_length = math.sqrt(r**2 - (counter*y_dim_eff/2)**2)*2
#                temp_dies_in_row = (math.floor(temp_chord_length/x_dim)-(math.floor(chord_length/x_dim))-extra_columns)*counter
#                dies_per_wafer += temp_dies_in_row
#                if temp_dies_in_row > 0:
#                    extra_columns += 1
#                counter -= 2
#
#            starting_distance_from_left = None
#            while row_chord_height < usable_wafer_diameter/2:
#                chord_length = math.sqrt(r**2 - (row_chord_height - dicing_distance/2)**2)*2 + dicing_distance
#
#                # For the Grid Fill case, the dies need to fit on top of the dies of the previous row.
#                if starting_distance_from_left is None:
#                    # TODO: Doublecheck the starting_distance_from_left and starting_location calculations.
#                    starting_distance_from_left = (usable_wafer_diameter - chord_length)/2
#                    dies_per_wafer += 2*math.floor(chord_length/x_dim_eff)
#                else:
#                    # Compute how many squares over from the first square it is possible to fit an other square on top.
#                    location_of_first_fit_candidate = (usable_wafer_diameter - chord_length)/2
#                    starting_location = math.ceil((location_of_first_fit_candidate - starting_distance_from_left)/x_dim_eff)*x_dim_eff + starting_distance_from_left
#                    effective_cord_length = chord_length - (starting_location - location_of_first_fit_candidate)
#                    dies_per_wafer += 2*math.floor(effective_cord_length/x_dim_eff)
#
#                row_chord_height += y_dim_eff
#                
#            if dies_per_wafer > best_dies_per_wafer:
#                best_dies_per_wafer = dies_per_wafer
#            left_column_height = left_column_height + 1
#
#        return best_dies_per_wafer

    def compute_nogrid_dies_per_wafer(self, x_dim, y_dim, usable_wafer_diameter, dicing_distance):
        # Case 1: Dies are centered on the diameter line of the circle.
        x_dim_eff = x_dim + dicing_distance
        y_dim_eff = y_dim + dicing_distance
        num_squares_case_1 = 0
        die_locations_1 = []
        # Compute the length of a chord that intersects the circle half the square's side length away from the center of the circle.
        row_chord_height = y_dim_eff/2
        chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height - dicing_distance/2)**2)*2 + dicing_distance
        # Compute the number of squares that fit along the chord length.
        num_squares_case_1 += math.floor(chord_length/x_dim_eff)
        for j in range(math.floor(chord_length/x_dim_eff)):
            x = j*x_dim_eff - chord_length/2
            y = -1*y_dim_eff/2
            # if x**2 + y**2 <= (usable_wafer_diameter/2)**2:
            die_locations_1.append((x, y))
        # Update the row chord height for the next row and start iterating.
        row_chord_height += y_dim_eff
        while row_chord_height < usable_wafer_diameter/2:
            # Compute the length of a chord that intersects the circle half the square's side length away from the center of the circle.
            chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height - dicing_distance/2)**2)*2 + dicing_distance
            # For the Line Fill case, compute the maximum number of squares that can fit along the chord length.
            num_squares_case_1 += 2*math.floor(chord_length/x_dim_eff)
            for j in range(math.floor(chord_length/x_dim_eff)):
                x = j*x_dim_eff - chord_length/2
                y = row_chord_height - y_dim_eff
                # if x**2 + y**2 <= (usable_wafer_diameter/2)**2:
                die_locations_1.append((x, y))
                die_locations_1.append((x, -1*y-y_dim_eff))
            row_chord_height += y_dim_eff

        # Case 2: Dies are above and below the diameter line of the circle.
        num_squares_case_2 = 0
        die_locations_2 = []
        # Compute the length of a chord that intersects the circle the square's side length away from the center of the circle.
        row_chord_height = y_dim_eff
        chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height - dicing_distance/2)**2)*2 + dicing_distance
        num_squares_case_2 += 2*math.floor(chord_length/x_dim_eff)

        row_chord_height += y_dim_eff
        while row_chord_height < usable_wafer_diameter/2:
            # Compute the length of a chord that intersects the circle half the square's side length away from the center of the circle.
            chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height - dicing_distance/2)**2)*2 + dicing_distance
            num_squares_case_2 += 2*math.floor(chord_length/x_dim_eff)
            row_chord_height += y_dim_eff

        # Find the maximum of the two cases.
        if num_squares_case_2 > num_squares_case_1:
            num_squares = num_squares_case_2
            die_locations = die_locations_2
        else:
            num_squares = num_squares_case_1
            die_locations = die_locations_1

        #print("Number of Squares: ")
        #print(num_squares)
        #print("Die Locations: ")
        #plot_dies_on_wafer(die_locations, x_dim, y_dim, usable_wafer_diameter)
        
        return num_squares

    #def plot_dies_on_wafer(die_positions, x_dim, y_dim, usable_wafer_diameter):
    #    print("In Plot Dies on Wafer")
    #    print("Create subplots")
    #    fig, ax = plt.subplots()
    #    print("Create wafer")
    #    wafer = plt.Circle((0, 0), usable_wafer_diameter / 2, color='lightgrey', fill=True)
    #    ax.add_artist(wafer)

    #    print("Plotting die positions")
    #    for (x, y) in die_positions:
    #        die = plt.Rectangle((x, y), x_dim, y_dim, edgecolor='blue', facecolor='none')
    #        ax.add_artist(die)

    #    print("Done Plotting")

    #    print("Plot settings")

    #    ax.set_xlim(1.1*(-1*usable_wafer_diameter / 2), 1.1*(usable_wafer_diameter / 2))
    #    ax.set_ylim(1.1*(-1*usable_wafer_diameter / 2), 1.1*(usable_wafer_diameter / 2))
    #    ax.set_aspect('equal', adjustable='box')

    #    plt.xlabel('X Position')
    #    plt.ylabel('Y Position')
    #    plt.title('Die Locations on Wafer')
    #    print("Showing plot")
    #    plt.show()
    #    print("Done Showing Plot")

    def compute_dies_per_wafer(self, x_dim, y_dim, usable_wafer_diameter, dicing_distance, grid_fill):
        # If grid_fill is True, we assume there will be some number of dies flush against the left of the wafer edge.
        #   We need to search through each of these possibilities until another die would fit to the left of this column.
        #   In this case, the 1-die flush case would cover it.
        #   Note that this is still an approximation. The actual number of dies may be slightly higher.
        # If grid_fill is False, we assume that dies are placed in a line along the diameter of the wafer or above and
        #   below the diameter line.

        simple_equation_flag = False

        if simple_equation_flag:
            num_squares = usable_wafer_diameter*math.pi*((usable_wafer_diameter/(4*(y_dim+dicing_distance)*(x_dim+dicing_distance)))-(1/math.sqrt(2*(y_dim+dicing_distance)*(x_dim+dicing_distance))))
        else:
            if grid_fill:
                num_squares = self.compute_grid_dies_per_wafer(x_dim, y_dim, usable_wafer_diameter, dicing_distance)
            else:
                num_squares = self.compute_nogrid_dies_per_wafer(x_dim, y_dim, usable_wafer_diameter, dicing_distance)

        ## Case 1: Dies are centered on the diameter line of the circle.
        #num_squares_case_1 = 0
        ## Compute the length of a chord that intersects the circle half the square's side length away from the center of the circle.
        #row_chord_height = y_dim/2
        #chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height)**2)*2
        ## Compute the number of squares that fit along the chord length.
        #num_squares_case_1 += math.floor(chord_length/x_dim)
        ## Update the row chord height for the next row and start iterating.
        #row_chord_height += y_dim
        #while row_chord_height < usable_wafer_diameter/2:
        #    # Compute the length of a chord that intersects the circle half the square's side length away from the center of the circle.
        #    chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height)**2)*2

        #    starting_distance_from_left = None

        #    if not grid_fill:
        #        # For the Line Fill case, compute the maximum number of squares that can fit along the chord length.
        #        num_squares_case_1 += 2*math.floor(chord_length/x_dim)
        #    else:
        #        # For the Grid Fill case, the dies need to fit on top of the dies of the previous row.
        #        if starting_distance_from_left is None:
        #            # TODO: Doublecheck the starting_distance_from_left and starting_location calculations.
        #            starting_distance_from_left = (usable_wafer_diameter - chord_length)/2
        #            num_squares_case_1 += 2*math.floor(chord_length/x_dim)
        #        else:
        #            # Compute how many squares over from the first square it is possible to fit an other square on top.
        #            location_of_first_fit_candidate = (usable_wafer_diameter - chord_length)/2
        #            starting_location = math.ceil((location_of_first_fit_candidate - starting_distance_from_left)/x_dim)*x_dim + starting_distance_from_left
        #            effective_cord_length = chord_length - (starting_location - location_of_first_fit_candidate)
        #            num_squares_case_1 += 2*math.floor(effective_cord_length/x_dim)
        #    
        #    row_chord_height += y_dim

        ## Case 2: Dies are above and below the diameter line of the circle.
        #num_squares_case_2 = 0
        ## Compute the length of a chord that intersects the circle the square's side length away from the center of the circle.
        #row_chord_height = y_dim
        #chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height)**2)*2
        #num_squares_case_2 += 2*math.floor(chord_length/x_dim)
        #row_chord_height += y_dim
        #if grid_fill:
        #    starting_distance_from_left = None
        #while row_chord_height < usable_wafer_diameter/2:
        #    # Compute the length of a chord that intersects the circle half the square's side length away from the center of the circle.
        #    chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height)**2)*2
        #    if not grid_fill:
        #        num_squares_case_2 += 2*math.floor(chord_length/x_dim)
        #    else:
        #        if starting_distance_from_left is None:
        #            starting_distance_from_left = (usable_wafer_diameter - chord_length)/2
        #            num_squares_case_2 += 2*math.floor(chord_length/x_dim)
        #        else:
        #            # Compute how many squares over from the first square it is possible to fit an other square on top.
        #            location_of_first_fit_candidate = (usable_wafer_diameter - chord_length)/2
        #            starting_location = math.ceil((location_of_first_fit_candidate - starting_distance_from_left)/x_dim)*x_dim + starting_distance_from_left
        #            effective_cord_length = chord_length - (starting_location - location_of_first_fit_candidate)
        #            num_squares_case_2 += 2*math.floor(effective_cord_length/x_dim)

        #    row_chord_height += y_dim
        
        ## Find the maximum of the two cases.
        #num_squares = max(num_squares_case_1, num_squares_case_2)

        return num_squares


    def compute_cost_per_mm2(self, area, aspect_ratio, wafer_process) -> float:
        # Access parameters that will be used multiple times.
        wafer_diameter = wafer_process.wafer_diameter
        grid_fill = wafer_process.wafer_fill_grid

        x_dim = math.sqrt(area*aspect_ratio) #+ wafer_process.dicing_distance
        y_dim = math.sqrt(area/aspect_ratio) #+ wafer_process.dicing_distance

        # Find effective wafer diameter that is valid for placing dies.
        usable_wafer_diameter = wafer_diameter - 2*wafer_process.edge_exclusion
        # Get the side length of the die assuming it is a square.
        #square_side = math.sqrt(square_area) + wafer_process.dicing_distance

        if (math.sqrt(x_dim**2 + y_dim**2) > usable_wafer_diameter/2):
            print("Error: Die size is too large for accurate calculation of fit for wafer. Exiting...")
            sys.exit(1)

        if (x_dim == 0 or y_dim == 0):
            print("Die size is zero. Exiting...")
            sys.exit(1)

        dies_per_wafer = self.compute_dies_per_wafer(x_dim, y_dim, usable_wafer_diameter, wafer_process.dicing_distance, grid_fill)

        if (dies_per_wafer == 0):
            print("Dies per wafer is zero. Exiting...")
            sys.exit(1)

        # Compute the cost per mm^2.
        used_area = dies_per_wafer*area
        circle_area = math.pi*(wafer_diameter/2)**2
        cost_per_mm2 = self.cost_per_mm2*circle_area/used_area
        return cost_per_mm2

#    def compute_cost_per_mm2(self, square_area, aspect_ratio, wafer_process) -> float:
#        # Access parameters that will be used multiple times.
#        wafer_diameter = wafer_process.wafer_diameter
#        grid_fill = wafer_process.wafer_fill_grid
#
#        x_dim = math.sqrt(square_area*aspect_ratio) + wafer_process.dicing_distance
#        y_dim = math.sqrt(square_area/aspect_ratio) + wafer_process.dicing_distance
#
#        # Find effective wafer diameter that is valid for placing dies.
#        usable_wafer_diameter = wafer_diameter - 2*wafer_process.edge_exclusion
#        # Get the side length of the die assuming it is a square.
#        #square_side = math.sqrt(square_area) + wafer_process.dicing_distance
#
#        if (math.sqrt(x_dim**2 + y_dim**2) > usable_wafer_diameter/2):
#            print("Error: Die size is too large for accurate calculation of fit for wafer. Exiting...")
#            sys.exit(1)
#
#        # Two different methods are supported for filling the wafer with dies:
#        #  1. Grid fill: The dies are placed in a grid pattern where both horizontal and vertical edges must line up.
#        #  2. Line fill: The dies are placed one row at a time without requiring vertical edges to line up.
#
#        # The number of dies that fit is estimated by taking the best of two cases:
#        #  1. The dies of the first placed row are centered on the diameter line of the circle.
#        #  2. The dies of the first placed rows are above and below the diameter line of the circle.
#
#        # TODO: Add aspect ratio support.
#
#        # Case 1: Dies are centered on the diameter line of the circle.
#        num_squares_case_1 = 0
#        # Compute the length of a chord that intersects the circle half the square's side length away from the center of the circle.
#        row_chord_height = y_dim/2
#        chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height)**2)*2
#        # Compute the number of squares that fit along the chord length.
#        num_squares_case_1 += math.floor(chord_length/x_dim)
#        # Update the row chord height for the next row and start iterating.
#        row_chord_height += y_dim
#        while row_chord_height < usable_wafer_diameter/2:
#            # Compute the length of a chord that intersects the circle half the square's side length away from the center of the circle.
#            chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height)**2)*2
#
#            starting_distance_from_left = None
#
#            if not grid_fill:
#                # For the Line Fill case, compute the maximum number of squares that can fit along the chord length.
#                num_squares_case_1 += 2*math.floor(chord_length/x_dim)
#            else:
#                # For the Grid Fill case, the dies need to fit on top of the dies of the previous row.
#                if starting_distance_from_left is None:
#                    # TODO: Doublecheck the starting_distance_from_left and starting_location calculations.
#                    starting_distance_from_left = (usable_wafer_diameter - chord_length)/2
#                    num_squares_case_1 += 2*math.floor(chord_length/x_dim)
#                else:
#                    # Compute how many squares over from the first square it is possible to fit an other square on top.
#                    location_of_first_fit_candidate = (usable_wafer_diameter - chord_length)/2
#                    starting_location = math.ceil((location_of_first_fit_candidate - starting_distance_from_left)/x_dim)*x_dim + starting_distance_from_left
#                    effective_cord_length = chord_length - (starting_location - location_of_first_fit_candidate)
#                    num_squares_case_1 += 2*math.floor(effective_cord_length/x_dim)
#            
#            row_chord_height += y_dim
#
#        # Case 2: Dies are above and below the diameter line of the circle.
#        num_squares_case_2 = 0
#        # Compute the length of a chord that intersects the circle the square's side length away from the center of the circle.
#        row_chord_height = y_dim
#        chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height)**2)*2
#        num_squares_case_2 += 2*math.floor(chord_length/x_dim)
#        row_chord_height += y_dim
#        if grid_fill:
#            starting_distance_from_left = None
#        while row_chord_height < usable_wafer_diameter/2:
#            # Compute the length of a chord that intersects the circle half the square's side length away from the center of the circle.
#            chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height)**2)*2
#            if not grid_fill:
#                num_squares_case_2 += 2*math.floor(chord_length/x_dim)
#            else:
#                if starting_distance_from_left is None:
#                    starting_distance_from_left = (usable_wafer_diameter - chord_length)/2
#                    num_squares_case_2 += 2*math.floor(chord_length/x_dim)
#                else:
#                    # Compute how many squares over from the first square it is possible to fit an other square on top.
#                    location_of_first_fit_candidate = (usable_wafer_diameter - chord_length)/2
#                    starting_location = math.ceil((location_of_first_fit_candidate - starting_distance_from_left)/x_dim)*x_dim + starting_distance_from_left
#                    effective_cord_length = chord_length - (starting_location - location_of_first_fit_candidate)
#                    num_squares_case_2 += 2*math.floor(effective_cord_length/x_dim)
#
#            row_chord_height += y_dim
#        
#        # Find the maximum of the two cases.
#        num_squares = max(num_squares_case_1, num_squares_case_2)
#
#        if (square_area == 0):
#            print("Square area is zero. Exiting...")
#            sys.exit(1)
#
#        if (num_squares == 0):
#            print("Number squares is zero. Exiting...")
#            sys.exit(1)
#
#        # Compute the cost per mm^2.
#        used_area = num_squares*square_area
#        circle_area = math.pi*(wafer_diameter/2)**2
#        cost_per_mm2 = self.cost_per_mm2*circle_area/used_area
#        return cost_per_mm2

    # ===== End of Computation Functions =======


# =========================================
# Assembly Definition Class
# =========================================
# The class has attributes:
#   name: The name of the assembly process.
#   materials_cost_per_mm2: The cost of the materials per mm^2 of the assembly.
#   picknplace_machine_cost: The cost of the machine.
#   picknplace_machine_lifetime: The lifetime of the machine in years.
#   picknplace_machine_uptime: The uptime of the machine as a fraction from 0 to 1.
#   picknplace_technician_yearly_cost: The cost of the technician for one year.
#   picknplace_time: The time it takes to pick and place a die in seconds.
#   picknplace_group: The number of dies that can be picked and placed at once.
#   bonding_machine_cost: The cost of the bonding machine.
#   bonding_machine_lifetime: The lifetime of the bonding machine in years.
#   bonding_machine_uptime: The uptime of the bonding machine as a fraction from 0 to 1.
#   bonding_technician_yearly_cost: The cost of the technician for one year.
#   bonding_time: The time it takes to bond a die in seconds.
#   bonding_group: The number of dies that can be bonded at once.
#   die_separation: The distance between the dies in mm.
#   edge_exclusion: The distance from the edge of the wafer to the first die in mm.
#   max_pad_current_density: The maximum current density of the pads in mA/mm^2.
#   bonding_pitch: The pitch of the bonding pads in mm.
#   alignment_yield: The yield of the alignment process.
#   bonding_yield: The yield of the bonding process.
#   dielectric_bond_defect_density: The defect density of the dielectric bond.
#   static: A boolean set true when the assembly process is defined to prevent further changes.
# =========================================
# The class has the following methods.
#   set_static()
#   get_power_per_pad(float): Computes the power per pad given the core voltage.
#   an initialization function, get/set parameter functions, and cast to strin of the objectg to print a description.
# == Other ==
#   compute_picknplace_time(int): Computes the time it takes to pick and place a given number of dies.
#   compute_bonding_time(int): Computes the time it takes to bond a given number of dies.
#   assembly_time(float): Computes the assembly time given the area of the die in mm^2.
#   compute_assembly_cost_per_second(): Computes the cost per second of the assembly process.
#   assembly_cost(float): Computes the cost of the assembly process given the area of the die in mm^2.
#   assembly_yield(float): Computes the yield of the assembly process given the area of the die in mm^2.
# =========================================

class Assembly:
    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) != str:
                print("Error: Assembly process name must be a string.")
                return 1
            else:
                self.__name = value
                return 0

    @property
    def materials_cost_per_mm2(self):
        return self.__materials_cost_per_mm2

    @materials_cost_per_mm2.setter
    def materials_cost_per_mm2(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Materials cost per mm^2 must be a number.")
                return 1
            elif value < 0:
                print("Error: Materials cost per mm^2 must be nonnegative.")
                return 1
            else:
                self.__materials_cost_per_mm2 = value
                return 0
    
    @property
    def bb_cost_per_second(self):
        return self.__bb_cost_per_second

    @bb_cost_per_second.setter
    def bb_cost_per_second(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if value == None:
                self.__bb_cost_per_second = value
                return 0
            elif type(value) == str:
                print("Error: Pick and place cost per second must be a number.")
                return 1
            elif value < 0:
                print("Error: Pick and place cost per second must be nonnegative.")
                return 1
            else:
                self.__bb_cost_per_second = value
                return 0

    @property
    def picknplace_machine_cost(self):
        return self.__picknplace_machine_cost

    @picknplace_machine_cost.setter
    def picknplace_machine_cost(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Pick and place machine cost must be a number.")
                return 1
            elif value < 0:
                print("Error: Pick and place machine cost must be nonnegative.")
                return 1
            else:
                self.__picknplace_machine_cost = value
                return 0
        
    @property
    def picknplace_machine_lifetime(self):
        return self.__picknplace_machine_lifetime
    
    @picknplace_machine_lifetime.setter
    def picknplace_machine_lifetime(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Pick and place machine lifetime must be a number.")
                return 1
            elif value < 0:
                print("Error: Pick and place machine lifetime must be nonnegative.")
                return 1
            else:
                self.__picknplace_machine_lifetime = value
                return 0
        
    @property
    def picknplace_machine_uptime(self):
        return self.__picknplace_machine_uptime
    
    @picknplace_machine_uptime.setter
    def picknplace_machine_uptime(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Pick and place machine uptime must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Pick and place machine uptime must be between 0 and 1.")
                return 1
            else:
                self.__picknplace_machine_uptime = value
                return 0
        
    @property
    def picknplace_technician_yearly_cost(self):
        return self.__picknplace_technician_yearly_cost
    
    @picknplace_technician_yearly_cost.setter
    def picknplace_technician_yearly_cost(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Pick and place technician yearly cost must be a number.")
                return 1
            elif value < 0:
                print("Error: Pick and place technician yearly cost must be nonnegative.")
                return 1
            else:
                self.__picknplace_technician_yearly_cost = value
                return 0
        
    @property
    def picknplace_time(self):
        return self.__picknplace_time
    
    @picknplace_time.setter
    def picknplace_time(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Pick and place time must be a number.")
                return 1
            elif value < 0:
                print("Error: Pick and place time must be nonnegative.")
                return 1
            else:
                self.__picknplace_time = value
                return 0
        
    @property
    def picknplace_group(self):
        return self.__picknplace_group
    
    @picknplace_group.setter
    def picknplace_group(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Pick and place group must be a number.")
                return 1
            elif value < 0:
                print("Error: Pick and place group must be nonnegative.")
                return 1
            else:
                self.__picknplace_group = value
                return 0
        
    @property
    def bonding_machine_cost(self):
        return self.__bonding_machine_cost
    
    @bonding_machine_cost.setter
    def bonding_machine_cost(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Bonding machine cost must be a number.")
                return 1
            elif value < 0:
                print("Error: Bonding machine cost must be nonnegative.")
                return 1
            else:
                self.__bonding_machine_cost = value
                return 0
        
    @property
    def bonding_machine_lifetime(self):
        return self.__bonding_machine_lifetime
    
    @bonding_machine_lifetime.setter
    def bonding_machine_lifetime(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Bonding machine lifetime must be a number.")
                return 1
            elif value < 0:
                print("Error: Bonding machine lifetime must be nonnegative.")
                return 1
            else:
                self.__bonding_machine_lifetime = value
                return 0
        
    @property
    def bonding_machine_uptime(self):
        return self.__bonding_machine_uptime
    
    @bonding_machine_uptime.setter
    def bonding_machine_uptime(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Bonding machine uptime must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Bonding machine uptime must be between 0 and 1.")
                return 1
            else:
                self.__bonding_machine_uptime = value
                return 0

    @property
    def bonding_technician_yearly_cost(self):
        return self.__bonding_technician_yearly_cost

    @bonding_technician_yearly_cost.setter
    def bonding_technician_yearly_cost(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Bonding technician yearly cost must be a number.")
                return 1
            elif value < 0:
                print("Error: Bonding technician yearly cost must be nonnegative.")
                return 1
            else:
                self.__bonding_technician_yearly_cost = value
                return 0

    @property
    def bonding_time(self):
        return self.__bonding_time

    @bonding_time.setter
    def bonding_time(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Bonding time must be a number.")
                return 1
            elif value < 0:
                print("Error: Bonding time must be nonnegative.")
                return 1
            else:
                self.__bonding_time = value
                return 0

    @property
    def bonding_group(self):
        return self.__bonding_group

    @bonding_group.setter
    def bonding_group(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Bonding group must be a number.")
                return 1
            elif value < 0:
                print("Error: Bonding group must be nonnegative.")
                return 1
            else:
                self.__bonding_group = value
                return 0

    @property
    def die_separation(self):
        return self.__die_separation

    @die_separation.setter
    def die_separation(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Die separation must be a number.")
                return 1
            elif value < 0:
                print("Error: Die separation must be nonnegative.")
                return 1
            else:
                self.__die_separation = value
                return 0

    @property
    def edge_exclusion(self):
        return self.__edge_exclusion

    @edge_exclusion.setter
    def edge_exclusion(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Edge exclusion must be a number.")
                return 1
            elif value < 0:
                print("Error: Edge exclusion must be nonnegative.")
                return 1
            else:
                self.__edge_exclusion = value
                return 0

    @property
    def max_pad_current_density(self):
        return self.__max_pad_current_density

    @max_pad_current_density.setter
    def max_pad_current_density(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Max pad current density must be a number.")
                return 1
            else:
                self.__max_pad_current_density = value
                return 0

    @property
    def bonding_pitch(self):
        return self.__bonding_pitch

    @bonding_pitch.setter
    def bonding_pitch(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Bonding pitch must be a number.")
                return 1
            elif value < 0:
                print("Error: Bonding pitch must be nonnegative.")
                return 1
            else:
                self.__bonding_pitch = value
                return 0

    @property
    def alignment_yield(self):
        return self.__alignment_yield

    @alignment_yield.setter
    def alignment_yield(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Alignment yield must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Alignment yield must be between 0 and 1.")
                return 1
            else:
                self.__alignment_yield = value
                return 0

    @property
    def bonding_yield(self):
        return self.__bonding_yield

    @bonding_yield.setter
    def bonding_yield(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Bonding yield must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Bonding yield must be between 0 and 1.")
                return 1
            else:
                self.__bonding_yield = value
                return 0

    @property
    def dielectric_bond_defect_density(self):
        return self.__dielectric_bond_defect_density

    @dielectric_bond_defect_density.setter
    def dielectric_bond_defect_density(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if type(value) == str:
                print("Error: Dielectric bond defect density must be a number.")
                return 1
            elif value < 0:
                print("Error: Dielectric bond defect density must be nonnegative.")
                return 1
            else:
                self.__dielectric_bond_defect_density = value
                return 0

    @property
    def static(self):
        return self.__static

    @static.setter
    def static(self, value):
        self.__static = value

    def set_static(self) -> int:
        if not self.assembly_fully_defined():
            print("Error: Attempt to set assembly static without defining all parameters. Exiting...")
            print(self)
            sys.exit(1)
        self.static = True
        return 0

    @property
    def picknplace_cost_per_second(self):
        return self.__picknplace_cost_per_second

    @picknplace_cost_per_second.setter
    def picknplace_cost_per_second(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if value is None:
                self.__picknplace_cost_per_second = None
                return 0
            elif type(value) == str:
                print("Error: Pick and place cost per second must be a number.")
                return 1
            elif value < 0:
                print("Error: Pick and place cost per second must be nonnegative.")
                return 1
            else:
                self.__picknplace_cost_per_second = value
                return 0
            
    @property
    def bonding_cost_per_second(self):
        return self.__bonding_cost_per_second
    
    @bonding_cost_per_second.setter
    def bonding_cost_per_second(self, value):
        if (self.static):
            print("Error: Cannot change static assembly process.")
            return 1
        else:
            if value is None:
                self.__bonding_cost_per_second = None
                return 0
            elif type(value) == str:
                print("Error: Bonding cost per second must be a number.")
                return 1
            elif value < 0:
                print("Error: Bonding cost per second must be nonnegative.")
                return 1
            else:
                self.__bonding_cost_per_second = value
                return 0
    
    def __str__(self) -> str:
        return_str = "Assembly Process Name: " + self.name
        return_str += "\n\r\tMaterials Cost Per mm^2: " + str(self.materials_cost_per_mm2)
        return_str += "\n\r\tPick and Place Machine Cost: " + str(self.picknplace_machine_cost)
        return_str += "\n\r\tPick and Place Machine Lifetime: " + str(self.picknplace_machine_lifetime)
        return_str += "\n\r\tPick and Place Machine Uptime: " + str(self.picknplace_machine_uptime)
        return_str += "\n\r\tPick and Place Technician Yearly Cost: " + str(self.picknplace_technician_yearly_cost)
        return_str += "\n\r\tPick and Place Time: " + str(self.picknplace_time)
        return_str += "\n\r\tPick and Place Group: " + str(self.picknplace_group)
        return_str += "\n\r\tBonding Machine Cost: " + str(self.bonding_machine_cost)
        return_str += "\n\r\tBonding Machine Lifetime: " + str(self.bonding_machine_lifetime)
        return_str += "\n\r\tBonding Machine Uptime: " + str(self.bonding_machine_uptime)
        return_str += "\n\r\tBonding Technician Yearly Cost: " + str(self.bonding_technician_yearly_cost)
        return_str += "\n\r\tBonding Time: " + str(self.bonding_time)
        return_str += "\n\r\tBonding Group: " + str(self.bonding_group)
        return_str += "\n\r\tDie Separation: " + str(self.die_separation)
        return_str += "\n\r\tEdge Exclusion: " + str(self.edge_exclusion)
        return_str += "\n\r\tMax Pad Current Density: " + str(self.max_pad_current_density)
        return_str += "\n\r\tBonding Pitch: " + str(self.bonding_pitch)
        return_str += "\n\r\tAlignment Yield: " + str(self.alignment_yield)
        return_str += "\n\r\tBonding Yield: " + str(self.bonding_yield)
        return_str += "\n\r\tDielectric Bond Defect Density: " + str(self.dielectric_bond_defect_density)
        return return_str

    def assembly_fully_defined(self) -> bool:
        if (self.name is None or self.materials_cost_per_mm2 is None or self.picknplace_machine_cost is None or
                self.picknplace_machine_lifetime is None or self.picknplace_machine_uptime is None or
                self.picknplace_technician_yearly_cost is None or self.picknplace_time is None or
                self.picknplace_group is None or self.bonding_machine_cost is None or self.bonding_machine_lifetime is None or
                self.bonding_machine_uptime is None or self.bonding_technician_yearly_cost is None or
                self.bonding_time is None or self.bonding_group is None or self.die_separation is None or
                self.edge_exclusion is None or self.max_pad_current_density is None or self.bonding_pitch is None or
                self.alignment_yield is None or self.bonding_yield is None or self.dielectric_bond_defect_density is None):
            return False
        else:
            return True

    def set_static(self) -> int:
        if not self.assembly_fully_defined():
            print("Error: Attempt to set assembly static without defining all parameters. Exiting...")
            print(self)
            sys.exit(1)
        self.static = True
        return 0

    def __init__(self, name = "", materials_cost_per_mm2 = None, bb_cost_per_second = None, picknplace_machine_cost = None,
                 picknplace_machine_lifetime = None, picknplace_machine_uptime = None, picknplace_technician_yearly_cost = None,
                 picknplace_time = None, picknplace_group = None, bonding_machine_cost = None, bonding_machine_lifetime = None,
                 bonding_machine_uptime = None, bonding_technician_yearly_cost = None, bonding_time = None,
                 bonding_group = None, die_separation = None, edge_exclusion = None, max_pad_current_density = None,
                 bonding_pitch = None, alignment_yield = None, bonding_yield = None, dielectric_bond_defect_density = None,
                 static = True) -> None:
        self.static = False
        self.name = name
        self.materials_cost_per_mm2 = materials_cost_per_mm2
        self.bb_cost_per_second = bb_cost_per_second
        self.picknplace_machine_cost = picknplace_machine_cost
        self.picknplace_machine_lifetime = picknplace_machine_lifetime
        self.picknplace_machine_uptime = picknplace_machine_uptime
        self.picknplace_technician_yearly_cost = picknplace_technician_yearly_cost
        self.picknplace_time = picknplace_time
        self.picknplace_group = picknplace_group
        self.bonding_machine_cost = bonding_machine_cost
        self.bonding_machine_lifetime = bonding_machine_lifetime
        self.bonding_machine_uptime = bonding_machine_uptime
        self.bonding_technician_yearly_cost = bonding_technician_yearly_cost
        self.bonding_time = bonding_time
        self.bonding_group = bonding_group
        self.die_separation = die_separation                # Given Parameter
        self.edge_exclusion = edge_exclusion                # Given Parameter
        self.max_pad_current_density = max_pad_current_density  # Given Parameter
        self.bonding_pitch = bonding_pitch
        self.picknplace_cost_per_second = None
        self.bonding_cost_per_second = None
        self.bonding_yield = bonding_yield
        self.alignment_yield = alignment_yield
        self.dielectric_bond_defect_density = dielectric_bond_defect_density
        self.static = static
        if not self.assembly_fully_defined():
            print("Warning: Assembly not fully defined. Setting non-static.")
            print(self)
            self.static = False
        else:
            self.compute_picknplace_cost_per_second()
            self.compute_bonding_cost_per_second()
        
        return

    # ====== Get/Set Functions ======

    def get_power_per_pad(self,core_voltage) -> float:
        pad_area = math.pi*(self.bonding_pitch/4)**2
        current_per_pad = self.max_pad_current_density*pad_area
        power_per_pad = current_per_pad*core_voltage
        return power_per_pad

    # ===== End of Get/Set Functions =====

    # ===== Other Functions =====

    def compute_picknplace_time(self, n_chips):
        picknplace_steps = math.ceil(n_chips/self.picknplace_group)
        time = self.picknplace_time*picknplace_steps
        return time
    
    def compute_bonding_time(self, n_chips):
        bonding_steps = math.ceil(n_chips/self.bonding_group)
        time = self.bonding_time*bonding_steps
        return time
    
    def assembly_time(self, n_chips):
        time = self.compute_picknplace_time(n_chips) + self.compute_bonding_time(n_chips)
        return time

    def compute_picknplace_cost_per_second(self):
        if self.bb_cost_per_second is not None:
            self.picknplace_cost_per_second = self.bb_cost_per_second
            return self.bb_cost_per_second
        machine_cost_per_year = self.picknplace_machine_cost/self.picknplace_machine_lifetime
        technician_cost_per_year = self.picknplace_technician_yearly_cost
        picknplace_cost_per_year = machine_cost_per_year + technician_cost_per_year
        picknplace_cost_per_second = picknplace_cost_per_year/(365*24*60*60)*self.picknplace_machine_uptime
        self.picknplace_cost_per_second = picknplace_cost_per_second
        return picknplace_cost_per_second
    
    def compute_bonding_cost_per_second(self):
        if self.bb_cost_per_second is not None:
            self.bonding_cost_per_second = self.bb_cost_per_second
            return self.bb_cost_per_second
        machine_cost_per_year = self.bonding_machine_cost/self.bonding_machine_lifetime
        technician_cost_per_year = self.bonding_technician_yearly_cost
        bonding_cost_per_year = machine_cost_per_year + technician_cost_per_year
        bonding_cost_per_second = bonding_cost_per_year/(365*24*60*60)*self.bonding_machine_uptime
        self.bonding_cost_per_second = bonding_cost_per_second
        return bonding_cost_per_second

    # Assembly cost includes cost of machine time and materials cost.
    def assembly_cost(self, n_chips, area):
        assembly_cost = (self.picknplace_cost_per_second*self.compute_picknplace_time(n_chips) 
                        + self.bonding_cost_per_second*self.compute_bonding_time(n_chips))
        assembly_cost += self.materials_cost_per_mm2*area
        return assembly_cost

    def assembly_yield(self, n_chips, n_bonds, area):
        assem_yield = 1.0
        assem_yield *= self.alignment_yield**n_chips
        assem_yield *= self.bonding_yield**n_bonds

        # If hybrid bonding, there is some yield impact of the dielectric bond.
        # This uses a defect density and area number which approximates the negative binomial yield model with no clustering.
        dielectric_bond_area = area
        dielectric_bond_yield = 1/(1 + self.dielectric_bond_defect_density*dielectric_bond_area)
        assem_yield *= dielectric_bond_yield

        return assem_yield

    # ===== End of Other Functions =====

# Test Definition Class
# The class has attributes:
#   name: string
#   time_per_test_cycle: float
#   samples_per_input: int
#   bb_cost_per_second: float
#   test_machine_cost: float
#   test_machine_lifetime: float
#   test_machine_uptime: float
#   test_technician_yearly_cost: float
#   test_self: bool
#   bb_self_pattern_count: int
#   bb_self_scan_chain_length: int
#   self_defect_coverage: float
#   self_test_reuse: float
#   self_num_scan_chains: int
#   self_num_io_per_scan_chain: int
#   self_num_test_io_offset: int
#   self_test_failure_dist: string
#   test_assembly: bool
#   bb_assembly_pattern_count: int
#   bb_assembly_scan_chain_length: int
#   assembly_defect_coverage: float
#   assembly_test_reuse: float
#   assembly_num_scan_chains: int
#   assembly_num_io_per_scan_chain: int
#   assembly_num_test_io_offset: int
#   assembly_test_failure_dist: string
#   static: boolean
# The class has methods:
#   set_static: sets static to True
#   cast to string, initialization function
class Test:
    # ===== Get/Set Functions =====

    @property
    def name(self):
        return self.__name

    @name.setter
    def name(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) != str:
                print("Error: Test name must be a string.")
                return 1
            else:
                self.__name = value
                return 0

    @property
    def time_per_test_cycle(self):
        return self.__time_per_test_cycle
    
    @time_per_test_cycle.setter
    def time_per_test_cycle(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Time per test cycle must be a number.")
                return 1
            elif value < 0:
                print("Error: Time per test cycle must be nonnegative.")
                return 1
            else:
                self.__time_per_test_cycle = value
                return 0

    @property
    def cost_per_second(self):
        return self.__cost_per_second
    
    @cost_per_second.setter
    def cost_per_second(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Cost per second must be a number.")
                return 1
            elif value < 0:
                print("Error: Cost per second must be nonnegative.")
                return 1
            else:
                self.__cost_per_second = value
                return 0

    @property
    def samples_per_input(self):
        return self.__samples_per_input
    
    @samples_per_input.setter
    def samples_per_input(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Samples per input must be a number.")
                return 1
            elif value < 0:
                print("Error: Samples per input must be nonnegative.")
                return 1
            else:
                self.__samples_per_input = value
                return 0

    @property
    def test_self(self):
        return self.__test_self

    @test_self.setter
    def test_self(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) != str:
                print("Error: Test self must be a string either \"True\" or \"true\".")
                return 1
            else:
                if value.lower() == "true":
                    self.__test_self = True
                else:
                    self.__test_self = False
                return 0
        
    @property
    def bb_self_pattern_count(self):
        return self.__bb_self_pattern_count
    
    @bb_self_pattern_count.setter
    def bb_self_pattern_count(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if value is None or value == "":
                self.__bb_self_pattern_count = None
                return 0
            elif type(value) == str:
                print("Error: BB self pattern count must be a number.")
                return 1
            elif value < 0:
                print("Error: BB self pattern count must be nonnegative.")
                return 1
            else:
                self.__bb_self_pattern_count = value
                return 0
        
    @property
    def bb_self_scan_chain_length(self):
        return self.__bb_self_scan_chain_length
    
    @bb_self_scan_chain_length.setter
    def bb_self_scan_chain_length(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if value is None or value == "":
                self.__bb_self_scan_chain_length = None
                return 0
            elif type(value) == str:
                print("Error: BB self scan chain length must be a number.")
                return 1
            elif value < 0:
                print("Error: BB self scan chain length must be nonnegative.")
                return 1
            else:
                self.__bb_self_scan_chain_length = value
                return 0
        
    @property
    def self_defect_coverage(self):
        return self.__self_defect_coverage
    
    @self_defect_coverage.setter
    def self_defect_coverage(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Self defect coverage must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Self defect coverage must be between 0 and 1.")
                return 1
            else:
                self.__self_defect_coverage = value
                return 0

    @property
    def self_test_reuse(self):
        return self.__self_test_reuse

    @self_test_reuse.setter
    def self_test_reuse(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Self test reuse must be a number.")
                return 1
            elif value < 0:
                print("Error: Self test reuse must be nonnegative.")
                return 1
            else:
                self.__self_test_reuse = value
                return 0

    @property
    def self_num_scan_chains(self):
        return self.__self_num_scan_chains

    @self_num_scan_chains.setter
    def self_num_scan_chains(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Self num scan chains must be a number.")
                return 1
            elif value < 0:
                print("Error: Self num scan chains must be nonnegative.")
                return 1
            else:
                self.__self_num_scan_chains = value
                return 0

    @property
    def self_num_io_per_scan_chain(self):
        return self.__self_num_io_per_scan_chain

    @self_num_io_per_scan_chain.setter
    def self_num_io_per_scan_chain(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Self num IO per scan chain must be a number.")
                return 1
            elif value < 0:
                print("Error: Self num IO per scan chain must be nonnegative.")
                return 1
            else:
                self.__self_num_io_per_scan_chain = value
                return 0

    @property
    def self_num_test_io_offset(self):
        return self.__self_num_test_io_offset

    @self_num_test_io_offset.setter
    def self_num_test_io_offset(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Self num test IO offset must be a number.")
                return 1
            elif value < 0:
                print("Error: Self num test IO offset must be nonnegative.")
                return 1
            else:
                self.__self_num_test_io_offset = value
                return 0

    @property
    def self_test_failure_dist(self):
        return self.__self_test_failure_dist

    @self_test_failure_dist.setter
    def self_test_failure_dist(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) != str:
                print("Error: Self test failure dist must be a string.")
                return 1
            else:
                self.__self_test_failure_dist = value
                return 0
        
    @property
    def test_assembly(self):
        return self.__test_assembly
    
    @test_assembly.setter
    def test_assembly(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) != str:
                print("Error: Test assembly must be a string either \"True\" or \"true\".")
                return 1
            else:
                if value.lower() == "true":
                    self.__test_assembly = True
                else:
                    self.__test_assembly = False
                return 0
        
    @property
    def bb_assembly_pattern_count(self):
        return self.__bb_assembly_pattern_count
    
    @bb_assembly_pattern_count.setter
    def bb_assembly_pattern_count(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if value is None or value == "":
                self.__bb_assembly_pattern_count = None
                return 0
            elif type(value) == str:
                print("Error: BB assembly pattern count must be a number.")
                return 1
            elif value < 0:
                print("Error: BB assembly pattern count must be nonnegative.")
                return 1
            else:
                self.__bb_assembly_pattern_count = value
                return 0
        
    @property
    def bb_assembly_scan_chain_length(self):
        return self.__bb_assembly_scan_chain_length
    
    @bb_assembly_scan_chain_length.setter
    def bb_assembly_scan_chain_length(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if value is None or value == "":
                self.__bb_assembly_scan_chain_length = None
                return 0
            elif type(value) == str:
                print("Error: BB assembly scan chain length must be a number.")
                return 1
            elif value < 0:
                print("Error: BB assembly scan chain length must be nonnegative.")
                return 1
            else:
                self.__bb_assembly_scan_chain_length = value
                return 0
        
    @property
    def assembly_defect_coverage(self):
        return self.__assembly_defect_coverage
    
    @assembly_defect_coverage.setter
    def assembly_defect_coverage(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Assembly defect coverage must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Assembly defect coverage must be between 0 and 1.")
                return 1
            else:
                self.__assembly_defect_coverage = value
                return 0
        
    @property
    def assembly_test_reuse(self):
        return self.__assembly_test_reuse
    
    @assembly_test_reuse.setter
    def assembly_test_reuse(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Assembly test reuse must be a number.")
                return 1
            elif value < 0:
                print("Error: Assembly test reuse must be nonnegative.")
                return 1
            else:
                self.__assembly_test_reuse = value
                return 0
        
    @property
    def assembly_gate_flop_ratio(self):
        return self.__assembly_gate_flop_ratio
    
    @assembly_gate_flop_ratio.setter
    def assembly_gate_flop_ratio(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Assembly gate flop ratio must be a number.")
                return 1
            elif value < 0:
                print("Error: Assembly gate flop ratio must be nonnegative.")
                return 1
            else:
                self.__assembly_gate_flop_ratio = value
                return 0
        
    @property
    def assembly_num_scan_chains(self):
        return self.__assembly_num_scan_chains
    
    @assembly_num_scan_chains.setter
    def assembly_num_scan_chains(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Assembly num scan chains must be a number.")
                return 1
            elif value < 0:
                print("Error: Assembly num scan chains must be nonnegative.")
                return 1
            else:
                self.__assembly_num_scan_chains = value
                return 0
        
    @property
    def assembly_num_io_per_scan_chain(self):
        return self.__assembly_num_io_per_scan_chain
    
    @assembly_num_io_per_scan_chain.setter
    def assembly_num_io_per_scan_chain(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Assembly num IO per scan chain must be a number.")
                return 1
            elif value < 0:
                print("Error: Assembly num IO per scan chain must be nonnegative.")
                return 1
            else:
                self.__assembly_num_io_per_scan_chain = value
                return 0
        
    @property
    def assembly_num_test_io_offset(self):
        return self.__assembly_num_test_io_offset
    
    @assembly_num_test_io_offset.setter
    def assembly_num_test_io_offset(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) == str:
                print("Error: Assembly num test IO offset must be a number.")
                return 1
            elif value < 0:
                print("Error: Assembly num test IO offset must be nonnegative.")
                return 1
            else:
                self.__assembly_num_test_io_offset = value
                return 0

    @property
    def assembly_test_failure_dist(self):
        return self.__assembly_test_failure_dist
    
    @assembly_test_failure_dist.setter
    def assembly_test_failure_dist(self, value):
        if (self.static):
            print("Error: Cannot change static testing.")
            return 1
        else:
            if type(value) != str:
                print("Error: Assembly test failure dist must be a string.")
                return 1
            else:
                self.__assembly_test_failure_dist = value
                return 0

    @property
    def static(self):
        return self.__static
    
    @static.setter
    def static(self, value):
        self.__static = value
        return 0
        
    def set_static(self) -> int:
        if not self.test_fully_defined():
            print("Error: Attempt to set test static without defining all parameters. Exiting...")
            print(self)
            sys.exit(1)
        else:
            self.static = True
            return 0

    def test_fully_defined(self) -> bool:
        if (self.name is None or self.time_per_test_cycle is None or self.cost_per_second is None or self.samples_per_input is None or
                self.test_self is None or self.self_defect_coverage is None or self.self_test_reuse is None or
                self.self_num_scan_chains is None or self.self_num_io_per_scan_chain is None or self.self_num_test_io_offset is None or
                self.self_test_failure_dist is None or self.test_assembly is None or self.assembly_defect_coverage is None or
                self.assembly_test_reuse is None or self.assembly_num_scan_chains is None or self.assembly_num_io_per_scan_chain is None or
                self.assembly_num_test_io_offset is None or self.assembly_test_failure_dist is None):
            return False
        else:
            return True

    #def compute_cost_per_second(self):
    #    seconds_in_one_year = 365*24*60*60 # Note this is approximate since it does not account for leap years.
    #    if self.bb_cost_per_second is None or self.bb_cost_per_second == "":
    #        if (self.test_machine_cost is None or self.test_machine_lifetime is None or
    #            self.test_machine_uptime is None or self.test_technician_yearly_cost is None or
    #            self.test_machine_lifetime == 0 or self.test_machine_uptime == 0):
    #            return 1 # Returning as a placeholder value that will make test extraordinarily expensive if not defined.
    #        cost_per_second = self.test_machine_cost/(self.test_machine_lifetime*seconds_in_one_year*self.test_machine_uptime)
    #        cost_per_second += self.test_technician_yearly_cost/seconds_in_one_year
    #    else:
    #        cost_per_second = self.bb_cost_per_second
    #    return cost_per_second

    # ===== End of Get/Set Functions =====

    # ===== Constructor =====
    def __init__(self, name = None,
                 time_per_test_cycle = None, cost_per_second = None, samples_per_input = None,
                 test_self = None, bb_self_pattern_count = None, bb_self_scan_chain_length = None,
                 self_defect_coverage = None, self_test_reuse = None,
                 self_num_scan_chains = None, self_num_io_per_scan_chain = None, self_num_test_io_offset = None,
                 self_test_failure_dist = None,
                 test_assembly = None, bb_assembly_pattern_count = None, bb_assembly_scan_chain_length = None,
                 assembly_defect_coverage = None, assembly_test_reuse = None,
                 assembly_num_scan_chains = None, assembly_num_io_per_scan_chain = None, assembly_num_test_io_offset = None,
                 assembly_test_failure_dist = None,
                 static = True) -> None:
        self.static = False
        self.name = name
        self.time_per_test_cycle = time_per_test_cycle
        self.samples_per_input = samples_per_input

        self.cost_per_second = cost_per_second

        self.static = static
        self.test_self = test_self
        self.bb_self_pattern_count = bb_self_pattern_count
        self.bb_self_scan_chain_length = bb_self_scan_chain_length
        self.self_defect_coverage = self_defect_coverage
        self.self_test_reuse = self_test_reuse
        self.self_num_scan_chains = self_num_scan_chains
        self.self_num_io_per_scan_chain = self_num_io_per_scan_chain
        self.self_num_test_io_offset = self_num_test_io_offset
        self.self_test_failure_dist = self_test_failure_dist

        self.test_assembly = test_assembly
        self.bb_assembly_pattern_count = bb_assembly_pattern_count
        self.bb_assembly_scan_chain_length = bb_assembly_scan_chain_length
        self.assembly_defect_coverage = assembly_defect_coverage     
        self.assembly_test_reuse = assembly_test_reuse
        self.assembly_num_scan_chains = assembly_num_scan_chains
        self.assembly_num_io_per_scan_chain = assembly_num_io_per_scan_chain
        self.assembly_num_test_io_offset = assembly_num_test_io_offset
        self.assembly_test_failure_dist = assembly_test_failure_dist
        if self.name is None:
            print("Warning: Test not fully defined. Setting non-static.")
            self.static = False
            print("Test has name " + self.name + ".")
        return

    # ====== End Constructor =====

    # ===== Print Functions =====

    def __str__(self) -> str:
        return_str = "Test: " + self.name + "\n"
        return_str += "Time_per_test_cycle: " + str(self.time_per_test_cycle) + "\n"
        return_str += "Cost_per_second: " + str(self.cost_per_second) + "\n"
        return_str += "Samples_per_input:" + str(self.samples_per_input) + "\n"
        return_str += "Test_self: " + str(self.test_self) + "\n"
        return_str += "bb_self_pattern_count: " + str(self.bb_self_pattern_count) + "\n"
        return_str += "bb_self_scan_chain_length: " + str(self.bb_self_scan_chain_length) + "\n"
        return_str += "Self_defect_coverage: " + str(self.self_defect_coverage) + "\n"
        return_str += "Self_test_reuse: " + str(self.self_test_reuse) + "\n"
        return_str += "Self_num_scan_chains: " + str(self.self_num_scan_chains) + "\n"
        return_str += "Self_num_io_per_scan_chain: " + str(self.self_num_io_per_scan_chain) + "\n"
        return_str += "Self_num_test_io_offset: " + str(self.self_num_test_io_offset) + "\n"
        return_str += "Self_test_failure_dist: " + self.self_test_failure_dist + "\n"
        return_str += "Test_assembly: " + str(self.test_assembly) + "\n"
        return_str += "bb_assembly_pattern_count: " + str(self.bb_assembly_pattern_count) + "\n"
        return_str += "bb_assembly_scan_chain_length: " + str(self.bb_assembly_scan_chain_length) + "\n"
        return_str += "Assembly_defect_coverage: " + str(self.assembly_defect_coverage) + "\n"
        return_str += "Assembly_test_reuse: " + str(self.assembly_test_reuse) + "\n"
        return_str += "Assembly_num_scan_chains: " + str(self.assembly_num_scan_chains) + "\n"
        return_str += "Assembly_num_io_per_scan_chain: " + str(self.assembly_num_io_per_scan_chain) + "\n"
        return_str += "Assembly_num_test_io_offset: " + str(self.assembly_num_test_io_offset) + "\n"
        return_str += "Assembly_test_failure_dist: " + self.assembly_test_failure_dist + "\n"
        return_str += "Static: " + str(self.static) + "\n"
        return return_str

    # ===== End of Print Functions =====

    # ===== Other Functions =====
    # This is the yield based on number of chips that pass test.
    def compute_self_test_yield(self, chip) -> float:
        if self.test_self == True:
            true_yield = chip.get_self_true_yield()
            test_yield = 1-(1-true_yield)*float(self.self_defect_coverage)
        else:
            test_yield = 1.0
        return test_yield

    def compute_self_quality(self, chip) -> float:
        test_yield = chip.get_self_test_yield()
        true_yield = chip.get_self_true_yield()

        quality = true_yield/test_yield

        return quality

    def compute_assembly_test_yield(self, chip) -> float:
        if self.test_assembly == True:
            assembly_true_yield = chip.get_chip_true_yield()
            assembly_test_yield = 1.0-(1.0-assembly_true_yield)*self.assembly_defect_coverage
        else:
            assembly_test_yield = 1.0

        return assembly_test_yield

    def compute_assembly_quality(self, chip) -> float:
        assembly_true_yield = chip.get_chip_true_yield()

        assembly_test_yield = chip.get_chip_test_yield()

        assembly_quality = assembly_true_yield/assembly_test_yield

        return assembly_quality

    def compute_self_pattern_count(self, chip) -> float:
        self_pattern_count = 0
        if self.bb_self_pattern_count != "" and self.bb_self_pattern_count is not None:
            self_pattern_count = self.bb_self_pattern_count
        else:
            # TODO: Evaluate this and determine accuracy
            # We assume there are 3 wires per logic gate.
            # We assume there are at least 2 logic gates per net.
            wires_per_flop = 3*chip.gate_flop_ratio/2
            # This approximates the logic depth.
            self_pattern_count = 2**wires_per_flop
        return self_pattern_count

    def compute_self_scan_chain_length_per_mm2(self, chip) -> float:
        self_scan_chain_length = 0
        if self.bb_self_scan_chain_length != "" and self.bb_self_scan_chain_length is not None:
            self_scan_chain_length = self.bb_self_scan_chain_length
        else:
            # Scan chain length is considered to be equal to the number of flops.
            # We want the number of flops per mm2
            # Since we have the number of gates per flop, we can multiply the number of gates per mm2 by 1/(gates per flop) to get scan chain length
            self_scan_chain_length = chip.get_self_gates_per_mm2()/chip.gate_flop_ratio
            self_scan_chain_length = self_scan_chain_length/self.self_num_scan_chains
        return self_scan_chain_length

    def compute_self_test_cost(self, chip) -> float:
        if (self.test_self == False):
            test_cost = 0.0
        else:
            test_cost = chip.core_area*self.time_per_test_cycle*self.cost_per_second*(self.compute_self_pattern_count(chip)+self.samples_per_input)*self.compute_self_scan_chain_length_per_mm2(chip) #Will need to add pattern count in test def.xml, and chain length parameters in sip.xml
            #if(self.self_test_failure_dist == "normal"): #Normal Distribution
            #    derating_factor = random.gauss(chip.get_chip_true_yield(),chip.get_chip_true_yield()*0.05)
            #elif(self.self_test_failure_dist == "uniform"): #Uniform Distribution
            #    derating_factor = abs((1-chip.get_chip_true_yield())/2 - chip.get_chip_true_yield()/2) #This means no deration
            #elif(self.self_test_failure_dist == "exponential"): #Exponential Distribution
            #    derating_factor = random.expovariate(1/chip.get_chip_true_yield())
            #elif(self.self_test_failure_dist == "lognormal"): #Lognormal Distribution
            #    derating_factor = random.lognormvariate(math.log(chip.get_chip_true_yield()),0.05)
            #else:
            #    print("Error: Invalid distribution type " + self.self_test_failure_dist + " for self test.")
            #    sys.exit(1)

            # Derating Factor Ignored for Now
            derating_factor = 1.0
            test_cost = derating_factor*test_cost #*self.samples_per_input
        return test_cost

    def assembly_gate_flop_ratio(self, chip) -> float:
        gate_flop_ratio = chip.gate_flop_ratio*chip.core_area
        total_area = chip.core_area
        for c in chip.get_chips():
            total_area += c.core_area
            gate_flop_ratio += c.gate_flop_ratio*c.core_area

        gate_flop_ratio = gate_flop_ratio/total_area

        return gate_flop_ratio

    def compute_assembly_pattern_count(self,chip) -> float:
        assembly_pattern_count = 0
        if self.bb_assembly_pattern_count != "" and self.bb_assembly_pattern_count is not None:
            assembly_pattern_count = self.bb_assembly_pattern_count
        else:
            # TODO: Evaluate this and determine accuracy
            # We assume there are 3 wires per logic gate.
            # We assume there are at least 2 logic gates per net.
            gate_flop_ratio = self.assembly_gate_flop_ratio(chip)

            wires_per_flop = 3*gate_flop_ratio/2
            # This approximates the logic depth.
            assembly_pattern_count = 2**wires_per_flop
        return assembly_pattern_count

    def compute_assembly_scan_chain_length_per_mm2(self, chip) -> float:
        assembly_scan_chain_length = 0
        if self.bb_assembly_scan_chain_length != "" and self.bb_assembly_scan_chain_length is not None:
            assembly_scan_chain_length = self.bb_assembly_scan_chain_length
        else:
            # Scan chain length is considered to be equal to the number of flops.
            # We want the number of flops per mm2
            # Since we have the number of gates per flop, we can multiply the number of gates per mm2 by 1/(gates per flop) to get scan chain length
            assembly_scan_chain_length = chip.get_assembly_gates_per_mm2()/self.assembly_gate_flop_ratio(chip)
            assembly_scan_chain_length = assembly_scan_chain_length/self.assembly_num_scan_chains
        return assembly_scan_chain_length

    def compute_assembly_test_cost(self, chip) -> float:
        if (self.test_assembly == False):
            test_cost = 0.0
        else:
            area = chip.core_area
            chips = chip.get_chips()
            for c in chips:
                area += c.core_area

            test_cost = area*self.time_per_test_cycle*self.cost_per_second*self.compute_assembly_pattern_count(chip)*self.compute_assembly_scan_chain_length_per_mm2(chip) #Will need to add pattern count in test def.xml, and chain length parameters in sip.xml
            #if(self.assembly_test_failure_dist == "normal"): #Normal Distribution
            #    derating_factor = random.gauss(chip.get_chip_true_yield(),chip.get_chip_true_yield()*0.05)
            #elif(self.assembly_test_failure_dist == "uniform"): #Uniform Distribution
            #    derating_factor = 1.0 #This means no deration
            #elif(self.assembly_test_failure_dist == "exponential"): #Exponential Distribution
            #    derating_factor = random.expovariate(1/chip.get_chip_true_yield())
            #elif(self.assembly_test_failure_dist == "lognormal"): #Lognormal Distribution
            #    derating_factor = random.lognormvariate(math.log(chip.get_chip_true_yield()),0.05)
            #else:
            #    print("Error: Invalid distribution type " + self.assembly_test_failure_dist + " for assembly test.")
            #    sys.exit(1)

            derating_factor = 1.0
            test_cost = derating_factor*test_cost*self.samples_per_input 
        return test_cost

    def num_test_ios(self) -> float:
        num_ios = 0
        if self.test_self == True:
            num_ios = self.self_num_io_per_scan_chain*self.self_num_scan_chains + self.self_num_test_io_offset
        if self.test_assembly == True:
            num_ios += self.assembly_num_io_per_scan_chain*self.assembly_num_scan_chains + self.assembly_num_test_io_offset
        return num_ios

    def get_atpg_cost(self, chip) -> float:
        # Constant for cost of ATPG effort.
        K = 1.0
        # Add atpg_cost calculation here.
        atpg_effort = 0.0
        if self.test_self == True:
            atpg_effort = chip.gate_flop_ratio*chip.core_area*chip.get_self_gates_per_mm2()/self.self_test_reuse
        if self.test_assembly == True:
            area = chip.core_area
            chips = chip.get_chips()
            for c in chips:
                area += c.core_area
            atpg_effort += chip.gate_flop_ratio*area*chip.get_assembly_gates_per_mm2()/self.assembly_test_reuse
        atpg_cost = atpg_effort*K
        return 0.0


    # ===== End of Other Functions =====

# =========================================
# Chip Class
# =========================================
# The class has attributes:
#   name: The name of the chip.
#   coreArea: The area of the core in mm^2.
#   cost: The cost of the chip in dollars.
#   chip_true_yield: The yield of the chip.
#   quality: The quality of the chip.
#   assembly_process: The assembly process used to assemble the chip.
#   stackup: The stackup of the chip.
#   chips: The list of chips that are stacked in this chip.
#   adjacencyMatrixList: The list of adjacency matrices for the chip.
#   power: The power of the chip in Watts.
#   static: A boolean set true when the chip is defined to prevent further changes.
# =========================================
# The class has the following methods.
# == Get/Set ==
#   get_name()
#   set_name(string)
#   get_core_area()
#   set_core_area(float)
#   get_cost()
#   set_cost(float)
#   get_chip_true_yield()
#   set_chip_true_yield(float)
#   get_quality()
#   set_quality(float)
#   get_assembly_process()
#   set_assembly_process(Assembly)
#   get_stackup()
#   set_stackup(list)
#   get_chips()
#   set_chips(list)
#   get_adjacencyMatrixList()
#   set_adjacencyMatrixList(list)
#   get_power()
#   set_power(float)
#   get_static()
#   set_static()
# == Print ==
#   print_description(): Dumps values of all the parameters for inspection.
# == Other ==
#   compute_area(): Computes the area of the chip in mm^2.
#   compute_cost(): Computes the cost of the chip in dollars.
#   compute_chip_yield(): Computes the yield of the chip.
# =========================================

class Chip:

    @property
    def name(self):
        return self.__name
    
    @name.setter
    def name(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if type(value) != str:
                print("Error: Chip name must be a string.")
                return 1
            else:
                self.__name = value
                return 0
        
    @property
    def core_area(self):
        return self.__core_area
    
    @core_area.setter
    def core_area(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if type(value) == str:
                print("Error: Core area must be a number.")
                return 1
            elif value < 0:
                print("Error: Core area must be nonnegative.")
                return 1
            else:
                self.__core_area = value
                return 0

    @property
    def aspect_ratio(self):
        return self.__aspect_ratio

    @aspect_ratio.setter
    def aspect_ratio(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if type(value) == str:
                print("Error: Aspect ratio must be a number.")
                return 1
            elif value < 0:
                print("Error: Aspect ratio must be nonnegative.")
                return 1
            else:
                self.__aspect_ratio = value
                return 0

    @property
    def x_location(self):
        return self.__x_location
    
    @x_location.setter
    def x_location(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if value is None or value == "":
                self.__x_location = None
                return 0
            elif type(value) == str:
                print("Error: X location must be a number.")
                return 1
            elif value < 0:
                print("Error: X location must be nonnegative.")
                return 1
            else:
                self.__x_location = value
                return 0
        
    @property
    def y_location(self):
        return self.__y_location
    
    @y_location.setter
    def y_location(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if value is None or value == "":
                self.__y_location = None
                return 0
            elif type(value) == str:
                print("Error: Y location must be a number.")
                return 1
            elif value < 0:
                print("Error: Y location must be nonnegative.")
                return 1
            else:
                self.__y_location = value
                return 0
        
    @property
    def bb_area(self):
        return self.__bb_area
    
    @bb_area.setter
    def bb_area(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if value is None or value == "":
                self.__bb_area = None
                return 0
            elif type(value) == str:
                print("Error: BB area must be a number.")
                return 1
            elif value < 0:
                print("Error: BB area must be nonnegative.")
                return 1
            else:
                self.__bb_area = value
                return 0
        
    @property
    def bb_cost(self):
        return self.__bb_cost
    
    @bb_cost.setter
    def bb_cost(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if value is None or value == "":
                self.__bb_cost = None
                return 0
            elif type(value) == str:
                print("Error: BB cost must be a number.")
                return 1
            elif value < 0:
                print("Error: BB cost must be nonnegative.")
                return 1
            else:
                self.__bb_cost = value
                return 0
        
    @property
    def bb_quality(self):
        return self.__bb_quality
    
    @bb_quality.setter
    def bb_quality(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if value is None or value == "":
                self.__bb_quality = None
                return 0
            elif type(value) == str:
                print("Error: BB quality must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: BB quality must be between 0 and 1.")
                return 1
            else:
                self.__bb_quality = value
                return 0
        
    @property
    def bb_power(self):
        return self.__bb_power
    
    @bb_power.setter
    def bb_power(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if value is None or value == "":
                self.__bb_power = None
                return 0
            elif type(value) == str:
                print("Error: BB power must be a number.")
                return 1
            elif value < 0:
                print("Error: BB power must be nonnegative.")
                return 1
            else:
                self.__bb_power = value
                return 0
        
    @property
    def fraction_memory(self):
        return self.__fraction_memory
    
    @fraction_memory.setter
    def fraction_memory(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if type(value) == str:
                print("Error: Fraction memory must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Fraction memory must be between 0 and 1.")
                return 1
            else:
                self.__fraction_memory = value
                return 0
        
    @property
    def fraction_logic(self):
        return self.__fraction_logic
    
    @fraction_logic.setter
    def fraction_logic(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if type(value) == str:
                print("Error: Fraction logic must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Fraction logic must be between 0 and 1.")
                return 1
            else:
                self.__fraction_logic = value
                return 0
        
    @property
    def fraction_analog(self):
        return self.__fraction_analog
    
    @fraction_analog.setter
    def fraction_analog(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if type(value) == str:
                print("Error: Fraction analog must be a number.")
                return 1
            elif value < 0 or value > 1:
                print("Error: Fraction analog must be between 0 and 1.")
                return 1
            else:
                self.__fraction_analog = value
                return 0
        
    @property
    def gate_flop_ratio(self):
        return self.__gate_flop_ratio
    
    @gate_flop_ratio.setter
    def gate_flop_ratio(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if type(value) == str:
                print("Error: Gate flop ratio must be a number.")
                return 1
            elif value < 0:
                print("Error: Gate flop ratio must be nonnegative.")
                return 1
            else:
                self.__gate_flop_ratio = value
                return 0
        
    @property
    def reticle_share(self):
        return self.__reticle_share
    
    @reticle_share.setter
    def reticle_share(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if type(value) == str:
                print("Error: Reticle share must be a number.")
                return 1
            elif value < 0:
                print("Error: Reticle share must be nonnegative.")
                return 1
            else:
                self.__reticle_share = value
                return 0
        
    @property
    def buried(self):
        return self.__buried
    
    @buried.setter
    def buried(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            if type(value) != str:
                print("Error: Buried must be a string with value \"True\" or \"true\".")
                return 1
            elif value.lower() == "true":
                self.__buried = True
                return 0
            else:
                self.__buried = False
                return 0
        
    @property
    def chips(self):
        return self.__chips
    
    @chips.setter
    def chips(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.__chips = value
            return 0
        
    @property
    def assembly_process(self):
        return self.__assembly_process
    
    @assembly_process.setter
    def assembly_process(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.__assembly_process = value
            return 0
        
    @property
    def test_process(self):
        return self.__test_process
    
    @test_process.setter
    def test_process(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.__test_process = value
            return 0

    @property
    def stackup(self):
        return self.__stackup
    
    @stackup.setter
    def stackup(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.__stackup = value
            return 0
        
    @property
    def wafer_process(self):
        return self.__wafer_process
    
    @wafer_process.setter
    def wafer_process(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.__wafer_process = value
            return 0

    @property
    def core_voltage(self):
        return self.__core_voltage
    
    @core_voltage.setter
    def core_voltage(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.__core_voltage = value
            return 0
        
    @property
    def power(self):
        return self.__power
    
    @power.setter
    def power(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.__power = value
            return 0
        
    @property
    def quantity(self):
        return self.__quantity
    
    @quantity.setter
    def quantity(self, value):
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.__quantity = value
            return 0
    
    @property
    def static(self):
        return self.__static
    
    @static.setter
    def static(self, value):
        self.__static = value
        return 0
    
    def set_static(self):
        self.__static = True
        return 0    

    # ===== Initialization Functions =====
    # "etree" is an element tree built from the system definition xml file. This can also be built without reading from the xml file and passed to the init function without defining the filename argument.
    def __init__(self, filename = None, etree = None, parent_chip = None, wafer_process_list = None, assembly_process_list = None, test_process_list = None, layers = None, ios = None, adjacency_matrix_definitions = None, average_bandwidth_utilization = None, block_names = None, static = False) -> None:
        self.static = False
        # If the critical parameters are not defined, throw an error and exit.
        if wafer_process_list is None:
            print("wafer_process_list is None")
            sys.exit(1)
        elif assembly_process_list is None:
            print("assembly_process_list is None")
            sys.exit(1)
        elif test_process_list is None:
            print("test_process_list is None")
            sys.exit(1)
        elif layers is None:
            print("layers is None")
            sys.exit(1)
        elif ios is None:
            print("ios is None")
            sys.exit(1)
        elif adjacency_matrix_definitions is None:
            print("adjacency_matrix_definitions is None")
            sys.exit(1)
        elif average_bandwidth_utilization is None:
            print("average_bandwidth_utilization is None")
            sys.exit(1)
        elif block_names is None:
            print("block_names is None")
            sys.exit(1)

        root = {}
        self.static = False
        # If the filename is given and the etree is not, read the file and build the etree.
        if filename is not None and filename != "" and etree is None:
            tree = ET.parse(filename)
            root = tree.getroot()
        # If the etree is given and the filename is not, use the etree.
        elif filename is None and etree is not None and etree != {}:
            root = etree
        elif (filename is None or filename == "") and (etree is None or etree == {}):
            print("Error: Invalid chip definition. The filename and etree are both None or empty. Exiting...")
            sys.exit(1) 
        # If neither is given, there is an error. If both are given, this is ambiguous, so it should also throw an error.
        else:
            print("Error: Invalid Chip definition. Filename and etree are both defined leading to possible ambiguity. Exiting...")
            sys.exit(1)

        self.parent_chip = parent_chip
        attributes = root.attrib

        # The following are the class parameter objects. The find_* functions match the correct object with the name given in the chip definition.
        self.wafer_process = self.find_wafer_process(attributes["wafer_process"], wafer_process_list)
        self.assembly_process = self.find_assembly_process(attributes["assembly_process"], assembly_process_list)
        self.test_process = self.find_test_process(attributes["test_process"], test_process_list)
        self.stackup = self.build_stackup(attributes["stackup"], layers)

        # Recursively handle the chips that are stacked on this chip.
        self.chips = []
        for chip_def in root:
            if "chip" in chip_def.tag:
                self.chips.append(Chip(filename = None, etree = chip_def, parent_chip = self, wafer_process_list = wafer_process_list, assembly_process_list = assembly_process_list, test_process_list = test_process_list, layers = layers, ios = ios, adjacency_matrix_definitions = adjacency_matrix_definitions, average_bandwidth_utilization = average_bandwidth_utilization, block_names = block_names, static = static))

        # Set Black-Box Parameters
        bb_area = attributes["bb_area"]
        if bb_area == "":
            self.bb_area = None
        else:
            self.bb_area = float(bb_area)
        bb_cost = attributes["bb_cost"]
        if bb_cost == "":
            self.bb_cost = None
        else:
            self.bb_cost = float(bb_cost)
        bb_quality = attributes["bb_quality"]
        if bb_quality == "":
            self.bb_quality = None
        else:
            self.bb_quality = float(bb_quality)
        bb_power = attributes["bb_power"]
        if bb_power == "":
            self.bb_power = None
        else:
            self.bb_power = float(bb_power)
        aspect_ratio = attributes["aspect_ratio"]
        if aspect_ratio == "":
            self.aspect_ratio = 1.0
        else:
            self.aspect_ratio = float(aspect_ratio)

        if attributes["x_location"] == "":
            self.x_location = None
        else:
            self.x_location = float(attributes["x_location"])

        if attributes["y_location"] == "":
            self.y_location = None
        else:
            self.y_location = float(attributes["y_location"])

        # Chip name should match the name in the netlist file.
        self.name = attributes["name"]

        # If core area is not given, this is an interposer and only has interconnect, so size is determined from the size of the stacked chiplets.
        # If core area is given, it is possible that the area will be determined by the size of the stacked chiplets or of the IO pads.
        self.core_area = float(attributes["core_area"])

        # NRE Design Cost Depends on the Type of Chip.
        # The following parameters allow defining a chip as a mix of memory, logic, and analog.
        self.fraction_memory = float(attributes["fraction_memory"])
        self.fraction_logic = float(attributes["fraction_logic"])
        self.fraction_analog = float(attributes["fraction_analog"])

        self.gate_flop_ratio = float(attributes["gate_flop_ratio"])

        # In the case of a shared reticle, NRE mask costs can be shared. This allows definition of the percentage of reticle costs which are incurred by this chip.
        self.reticle_share = float(attributes["reticle_share"])

        # All NRE costs scale with the quantity of chips produced.
        self.quantity = int(attributes["quantity"])

        # If a chip is defined as buried (such as a bridge die in EMIB), it is not counted in the total area of stacked chips.
        self.buried = attributes["buried"]

        # Store the adjacency matrix, bandwidth utilization, block names, and IO list.
        self.global_adjacency_matrix = adjacency_matrix_definitions
        self.average_bandwidth_utilization = average_bandwidth_utilization
        self.block_names = block_names
        self.io_list = ios

        # Power and Core Voltage are important for determining the number of power pads required.
        self.power = float(attributes["power"])
        self.core_voltage = float(attributes["core_voltage"])

        # If the chip is not fully defined, throw an error and exit.
        if self.name == "":
            print("Error: Chip name is \"\". Exiting...")
            sys.exit(1)
        elif self.wafer_process is None:
            print("wafer_process is None")
            sys.exit(1)
        elif self.assembly_process is None:
            print("assembly_process is None")
            sys.exit(1)
        elif self.test_process is None:
            print("test_process is None")
            sys.exit(1)
        elif self.stackup is None:
            print("stackup is None")
            sys.exit(1)

        # Compute power for all chips stacked on top of the current chip.
        self.set_stack_power(self.compute_stack_power())

        # Compute the io power for the chip.
        self.set_io_power(self.get_signal_power(self.get_chip_list()))

        # Compute the total power used for the chip.
        if self.bb_power is None:
            self.set_total_power(self.power + self.get_io_power() + self.get_stack_power())
        else:
            # bb_power overrides all power specific to the chip. So this is the io power and the self power, but stack power is part of other chip objects, so is still added.
            self.set_total_power(self.bb_power + self.get_stack_power())

        self.set_nre_design_cost()

        # print("Chip name is " + self.name + ".")
        self.set_area()

        self.set_self_true_yield(self.compute_layer_aware_yield())
        self.set_self_test_yield(self.test_process.compute_self_test_yield(self))
        if self.bb_quality is None:
            self.set_self_quality(self.test_process.compute_self_quality(self))
        else:
            self.set_self_quality(self.bb_quality)
        


        self.set_chip_true_yield(self.compute_chip_yield())
        self.set_chip_test_yield(self.test_process.compute_assembly_test_yield(self))
        self.set_quality(self.test_process.compute_assembly_quality(self))
        self.set_self_cost(self.compute_self_cost())
        self.set_cost(self.compute_cost())

#        self.set_chip_true_yield(self.compute_chip_yield())
#        self.set_quality(self.test_process.compute_assembly_quality(self))
#        self.set_chip_test_yield(self.test_process.compute_self_test_yield(self))
#        self.set_cost(self.compute_cost())

        # If the chip is defined as static, it should not be changed.
        self.static = static 

        return

    def compute_stack_power(self) -> float:
        stack_power = 0.0
        for chip in self.chips:
            stack_power += chip.get_total_power()
        return stack_power

#    def build_adjacency_matrices(self, adjacency_matrix_definitions, ios):
#        
#        # TODO: Implement a dynamic adjacency matrix that is oriented toward stacks rather than chiplets.
#                   The idea for this would be that instead of having chiplets connect with the adjacency matrix,
#                   the adjacency matrix would show the connection between stacks on the current chip.
#                   This would allow storage of the relevant parts of the adjacency matrix in the chip object
#                   instead of as a netlist object passed to every chip object in the assembly.
#
#        adjacencyMatrixList = {}
#        return adjacencyMatrixList

    # Find process function for use in searching through lists of processes.
    #       Note that there is a requirement that the processes support the
    #       get_name() function.
    def find_process(self, process_name, process_list):
        process = None
        for p in process_list:
            if p.name == process_name:
                process = p
                break
        if process is None:
            print("Error: Process not found.")
        return process

    def find_wafer_process(self, wafer_process_name, wafer_process_list):
        wafer_process = self.find_process(wafer_process_name, wafer_process_list)
        if wafer_process is None:
            print("Error: Wafer Process " + wafer_process_name + " not found.")
            print("Exiting")
            sys.exit(1)
        return wafer_process

    def find_assembly_process(self, assembly_process_name, assembly_process_list):
        assembly_process = self.find_process(assembly_process_name, assembly_process_list)
        if assembly_process is None:
            print("Error: Assembly Process " + assembly_process_name + " not found.")
            print("Exiting")
            sys.exit(1)
        return assembly_process

    def find_test_process(self, test_process_name, test_process_list):
        test_process = self.find_process(test_process_name, test_process_list)
        if test_process is None:
            print("Error: Test Process " + test_process_name + " not found.")
            print("Exiting")
            sys.exit(1)
        return test_process

    def build_stackup(self, stackup_string, layers):
        stackup = []
        # Split the stackup string at the commas.
        stackup_string = stackup_string.split(",")
        stackup_names = []
        for layer in stackup_string:
            layer_specification = layer.split(":")
            if int(layer_specification[0]) >= 0:
                for i in range(int(layer_specification[0])):
                    stackup_names.append(layer_specification[1])
            else:
                print("Error: Number of layers " + layer_specification[0] + " not valid for " + layer_specification[1] + ".")
                sys.exit(1)
        n_layers = len(stackup_names)
        for layer in stackup_names:
            l = self.find_process(layer, layers)
            if l is not None:
                stackup.append(l)
            else:
                print("Error: Layer " + layer + " not found.")
                print("Exiting")
                sys.exit(1)
        if len(stackup) != n_layers:
            print("Error: Stackup number of layers does not match definition, make sure all selected layers are included in the layer definition.")
            sys.exit(1)
        return stackup

    # ===== End of Initialization Functions =====

    # ===== Get/Set Functions =====

    def get_parent_chip(self):
        return self.parent_chip

    def get_assembly_core_area(self) -> float:
        assembly_core_area = self.core_area
        for chip in self.chips:
            assembly_core_area += chip.get_assembly_core_area()
        
        return assembly_core_area

    def get_self_cost(self) -> float:
        return self.self_cost
    
    def set_self_cost(self, value) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.self_cost = value
            return 0

    def get_cost(self) -> float:
        # If self.chips is not empty also print the costs of the chips.
        #if self.get_chips_len() > 0:
        #    for chip in self.chips:
        #        print("Child chip cost is " + str(chip.get_cost()))
        return self.cost
 
    def set_cost(self, value) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.cost = value
            return 0

    def get_self_true_yield(self) -> float:
        return self.self_true_yield
    
    def set_self_true_yield(self, value) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.self_true_yield = value
            return 0

    def get_chip_true_yield(self) -> float:
        return self.chip_true_yield

    def set_chip_true_yield(self, value) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.chip_true_yield = value
            return 0

    def get_self_test_yield(self) -> float:
        return self.self_test_yield
    
    def set_self_test_yield(self, value) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.self_test_yield = value
            return 0

    def get_chip_test_yield(self) -> float:
        return self.chip_test_yield

    def set_chip_test_yield(self, value) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.chip_test_yield = value
            return 0

    def get_self_gates_per_mm2(self) -> float:
        self_gates_per_mm2 = 0.0
        for layer in self.stackup:
            self_gates_per_mm2 += layer.get_gates_per_mm2()
        return self_gates_per_mm2

    def get_assembly_gates_per_mm2(self) -> float:
        total_core_area = self.get_assembly_core_area()
        assembly_gates_per_mm2 = self.get_self_gates_per_mm2()
        for chip in self.chips:
            total_core_area += chip.get_assembly_core_area()
            assembly_gates_per_mm2 += chip.get_assembly_gates_per_mm2()
        if total_core_area == 0:
            assembly_gates_per_mm2 = 0.0
        else:
            assembly_gates_per_mm2 = assembly_gates_per_mm2/total_core_area
        return assembly_gates_per_mm2
    
    def get_self_quality(self) -> float:
        return self.self_quality
    
    def set_self_quality(self, value) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.self_quality = value
            return 0

    def get_quality(self) -> float:
        return self.quality

    def set_quality(self, value) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.quality = value
            return 0
    
    def get_chips_len(self) -> int:
        return len(self.chips)

    def get_chips(self) -> list:
        return self.chips
    
    def set_chip_definitions(self,chip_definitions) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.chips = self.buildChips(chip_definitions)
            return 0
    
    def get_wafer_diameter(self) -> float:
        return self.wafer_process.wafer_diameter
    
    def get_edge_exclusion(self) -> float:
        return self.wafer_process.edge_exclusion
    
    def get_wafer_process_yield(self) -> float:
        return self.wafer_process.wafer_process_yield
    
    def get_reticle_x(self) -> float:
        return self.wafer_process.reticle_x
 
    def get_reticle_y(self) -> float:
        return self.wafer_process.reticle_y
     
    def get_stack_power(self) -> float:
        return self.stack_power
    
    def set_stack_power(self, value) -> int:
        self.stack_power = self.compute_stack_power()
        return 0

    def get_io_power(self) -> float:
        return self.io_power

    def set_io_power(self, value) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.io_power = value
            return 0

    def get_total_power(self) -> float:
        return self.total_power

    def set_total_power(self, value) -> int:
        if (self.static):
            print("Error: Cannot change static chip.")
            return 1
        else:
            self.total_power = value
            return 0

    def get_area(self) -> float:
        return self.area
    
    def set_area(self) -> int:
        self.area = self.compute_area()
        return 0

    # TODO: Add rectangle packing now that the aspect ratio is defined.
    def get_stacked_die_area(self) -> float:
        stacked_die_area = 0.0
        # print("\t\tStacked Die Area: " + str(stacked_die_area))
        for chip in self.chips:
            if not chip.buried:
                temp_area = self.expandedArea(chip.get_area(),self.assembly_process.die_separation/2,chip.aspect_ratio)
                stacked_die_area += temp_area
                # print("Expanded die area: " + str(temp_area))
        # print("Stacked die area after adding expanded dies: " + str(stacked_die_area))

        # print("\t\tStacked Die Area: " + str(stacked_die_area))
        # Note default aspect ratio is assumed here since this is not the final area for the chip object.
        stacked_die_area = self.expandedArea(stacked_die_area, self.assembly_process.edge_exclusion)
        # print("Final stacked die area: " + str(stacked_die_area))
        # print("\t\tStacked Die Area: " + str(stacked_die_area))
        return stacked_die_area

    def compute_nre_front_end_cost(self) -> float:
        front_end_cost = self.core_area*(self.wafer_process.nre_front_end_cost_per_mm2_memory*self.fraction_memory +
                                               self.wafer_process.nre_front_end_cost_per_mm2_logic*self.fraction_logic +
                                               self.wafer_process.nre_front_end_cost_per_mm2_analog*self.fraction_analog)
        return front_end_cost
    
    def compute_nre_back_end_cost(self) -> float:
        back_end_cost = self.core_area*(self.wafer_process.nre_back_end_cost_per_mm2_memory*self.fraction_memory +
                                              self.wafer_process.nre_back_end_cost_per_mm2_logic*self.fraction_logic +
                                              self.wafer_process.nre_back_end_cost_per_mm2_analog*self.fraction_analog)
        return back_end_cost

    def compute_nre_design_cost(self) -> float:
        nre_design_cost = self.compute_nre_front_end_cost() + self.compute_nre_back_end_cost()

        return nre_design_cost

    def get_nre_design_cost(self) -> float:
        return self.nre_design_cost

    def set_nre_design_cost(self) -> int:
        self.nre_design_cost = self.compute_nre_design_cost()
        return 0

    # ===== End of Get/Set Functions =====

    # ===== Print Functions =====

    def print_description(self):
        print("Chip Name: " + self.name)
        print()
        print("Black-Box Parameters: area = " + str(self.bb_area) + ", cost = " + str(self.bb_cost) + ", quality = " +
              str(self.bb_quality) + ", power = " + str(self.bb_power) +
              ". (If any of these parameters are not empty, the value will override the computed value.)")

        print()
        print("Chip Wafer Process: " + self.wafer_process.name)
        print("Chip Assembly Process: " + self.assembly_process.name)
        print("Chip Test Process: " + self.test_process.name)
        print("Chip Stackup: " + str([(l.name + ",") for l in self.stackup]))

        print()
        print("Chip Core Area: " + str(self.core_area))
        print("Chip Stacked Area: " + str(self.get_stacked_die_area()))
        print("Stacked Chips: " + str(self.chips))
        print("Chip IO Area: " + str(self.get_io_area()))
        print("Assembly Core Area: " + str(self.get_assembly_core_area()))
        print("Chip Buried: " + str(self.buried))
        print("Chip Core Voltage: " + str(self.core_voltage))

        print()
        print("Chip Area Breakdown: memory = " + str(self.fraction_memory) + ", logic = " + str(self.fraction_logic) +
              ", analog = " + str(self.fraction_analog) + ".")
        if self.reticle_share != 1.0:
            print("Chip takes up " + str(self.reticle_share*100) + " \% of a shared reticle")
        else:
            print("Reticle is not shared.")
        print("NRE Cost: " + str(self.compute_nre_cost()))
        print("Quantity: " + str(self.quantity))

        print()

        print("Chip Power: " + str(self.power))
        print("Stack Power: " + str(self.get_stack_power()))
        print("Total Power: " + str(self.get_total_power()))

        print()
        print("Number of Chip Power Pads: " + str(self.get_power_pads()))
        print("Number of Signal Pads: " + str(self.get_signal_count(self.get_chip_list())[0]))
        print("Total number of pads: " + str(self.get_power_pads() + self.get_signal_count(self.get_chip_list())[0]))
        
        print()
        print("Area of IO Cells: " + str(self.get_io_area()))
        print("Area required by pads: " + str(self.get_pad_area()))
        print("Chip Calculated Area: " + str(self.area))

        print()
        print("Chip Self True Yield: " + str(self.get_self_true_yield()))
        print("Chip Self Test Yield: " + str(self.get_self_test_yield()))
        print("Quality Yield: " + str(self.quality_yield()))
        print("Assembly Yield: " + str(self.assembly_process.assembly_yield(self.get_chips_len(),self.get_chips_signal_count(),self.get_stacked_die_area())))
        print("Chip Self Quality: " + str(self.get_self_quality()))
        print("Chip Self Cost: " + str(self.get_self_cost()))
        print("Chip NRE Total Cost: " + str(self.compute_nre_cost()))
        print("Chip True Yield: " + str(self.get_chip_true_yield()))
        print("Chip Tested Yield: " + str(self.get_chip_test_yield()))
        print("Chip Quality: " + str(self.get_quality()))
        print("Chip Cost: " + str(self.get_cost()))

        # print("Chip Cost: " + str(self.get_cost()))
        # print("Self Layer Cost: " + str(self.get_layer_aware_cost()))
        # print("Chip Cost Including Yield: " + str(self.get_cost()/self.get_chip_true_yield()))
        # print("Chip Quality: " + str(self.quality))
        # print("Chip Assembly Yield: " + str(self.assembly_process.assembly_yield(self.get_chips_len(),self.get_chips_signal_count(),self.get_stacked_die_area())))
        # print("Chip Assembly Process: " + self.assembly_process.name)
        # print("Chip Stackup: " + str([l.name for l in self.stackup]))
        # print("Chip Test Process: " + self.test_process.name)
        # print("Chip Wafer Diameter: " + str(self.get_wafer_diameter()) + "mm")
        # print("Reticle Dimensions: (" + str(self.get_reticle_x()) + "," + str(self.get_reticle_y()) + ")mm")
        # print("Chip Adjacency Matrix List: " + str(self.adjacencyMatrixList))
        # print("Chip List: " + str([c.name for c in self.chips]))
        #core_area_sum = 0.0
        #io_area_sum = 0.0
        #total_area = 0.0
        #for chip in self.chips:
        #    print("Cost = " + str(chip.get_cost()))
        #    print("Yield = " + str(chip.get_chip_true_yield()))
        for chip in self.chips:
           print(">>")
           chip.print_description()
        #   core_area_sum += chip.coreArea
        #   total_area += chip.area
        #   io_area_sum += chip.get_io_area()
        #   if chip.chips != []:
        #       for subchip in chip.chips:
        #            core_area_sum += subchip.coreArea
        #            total_area += subchip.area
        #            io_area_sum += chip.get_io_area()
           print("<<")
        #core_area_sum += self.core_area
        #io_area_sum += self.get_io_area()
        #total_area += self.area
        #print("core_area_sum = " + str(core_area_sum))
        #print("io_area_sum = " + str(io_area_sum))
        #print("total_area = " + str(total_area))
        return


    # ===== End of Print Functions =====

    # ===== Other Functions =====
 
    # Find the total area if a given area is assumed to be square and increased in size by a certain amount in every direction.
    def expandedArea(self,area,border,aspect_ratio=1.0):
        x = math.sqrt(area*aspect_ratio)
        y = math.sqrt(area/aspect_ratio)
        new_area = (x+2*border)*(y+2*border)
        return new_area

    # Get the area of the IOs on the chip.
    def get_io_area(self):
        # TODO: Ultimately, this needs to look at the adjacency matrices and count the number of connections. For now, filler.
        io_area = 0.0
        block_index = None
        for i in range(len(self.block_names)):
            if self.block_names[i] == self.name:
                block_index = i
                break
        if block_index is None:
            return 0
        for io_type in self.global_adjacency_matrix:
            # TODO: Fix this when the adjacency matrix is properly implemented.
            for io in self.io_list:
                if io.type == io_type:
                    break
            # Add all the entries in the row and column of the global adjacency matrix with the index correesponding to the name of the chip and weight with the wire_count of the IO type.
            io_area += sum(self.global_adjacency_matrix[io_type][block_index][:]) * io.tx_area + sum(self.global_adjacency_matrix[io_type][:][block_index]) * io.rx_area

        return io_area

    # Get number of Power Pads
    def get_power_pads(self):
        power = self.get_total_power()
        power_pads = math.ceil(power / self.assembly_process.get_power_per_pad(self.core_voltage))
        power_pads = power_pads*2 # Multiply by 2 for ground and power.
        return power_pads

    # Get the area taken up by the grid of pads on the bottom of the chip at the given pitch.
    def get_pad_area(self):
        num_power_pads = self.get_power_pads()
        num_test_pads = self.test_process.num_test_ios()
        signal_pads, signal_with_reach_count = self.get_signal_count(self.get_chip_list())
        num_pads = signal_pads + num_power_pads + num_test_pads
        # print("num pads = " + str(num_pads))

        parent_chip = self.get_parent_chip()
        if parent_chip is not None:
            bonding_pitch = parent_chip.assembly_process.bonding_pitch
        else:
            bonding_pitch = self.assembly_process.bonding_pitch
        area_per_pad = bonding_pitch**2

        # Create a list of reaches by taking the keys from the signal_with_reach_count dictionary and converting to floats.
        reaches = [float(key) for key in signal_with_reach_count.keys()]
        # Sort the reaches from smallest to largest.
        reaches.sort()
        #current_side = 0.0
        current_x = 0.0
        current_y = 0.0
        current_count = 0
        for reach in reaches:
            # Note that half of the reach with separation value is the valid placement band.
            if parent_chip is not None:
                reach_with_separation = reach - parent_chip.assembly_process.die_separation
            else:
                reach_with_separation = reach - self.assembly_process.die_separation
            if reach_with_separation < 0:
                print("Error: Reach is smaller than chip separation. Exiting...")
                sys.exit(1)
            current_count += signal_with_reach_count[str(reach)]
            # Find the minimum boundary that would contain all the pads with the current reach.
            required_area = current_count*area_per_pad
            if reach_with_separation < current_x and reach_with_separation < current_y: 
                #usable_area = 2*reach_with_separation*current_side - reach_with_separation**2
                # x*(reach_with_separation/2) is the placement band along a single edge.
                usable_area = reach_with_separation*(current_x+current_y) - reach_with_separation**2
            else:
                #usable_area = current_side**2
                usable_area = current_x*current_y
            if usable_area <= required_area:
                # Note that required_x and required_y are minimum. The real values are likely larger.
                required_x = math.sqrt(required_area*self.aspect_ratio)
                required_y = math.sqrt(required_area/self.aspect_ratio)
                if required_x > reach_with_separation and required_y > reach_with_separation:
                    # Work for computing the formulas below:
                    # required_area = 2*(new_req_x - (reach_with_separation/2)) * (reach_with_separation/2) + 2*(new_req_y - (reach_with_separation/2)) * (reach_with_separation/2)
                    # required_area = (2*new_req_x - reach_with_separation) * (reach_with_separation/2) + (2*new_req_y - reach_with_separation) * (reach_with_separation/2)
                    # required_area = (2*new_req_x + 2*new_req_y - 2*reach_with_separation) * (reach_with_separation/2)
                    # new_req_x = aspect_ratio*new_req_y
                    # 2*aspect_ratio*new_req_y + 2*new_req_y = (2*required_area/reach_with_separation) + 2*reach_with_separation
                    # new_req_y*(2*aspect_ratio + 2) = (2*required_area/reach_with_separation) + 2*reach_with_separation
                    # new_req_y = ((2*required_area/reach_with_separation) + 2*reach_with_separation)/(2*aspect_ratio + 2)
                    new_req_y = ((2*required_area/reach_with_separation) + 2*reach_with_separation)/(2*self.aspect_ratio + 2)
                    new_req_x = self.aspect_ratio*new_req_y
                else:
                    new_req_x = required_x
                    new_req_y = required_y
                # Round up to the nearest multiple of bonding pitch.
                new_req_x = math.ceil(new_req_x/bonding_pitch)*bonding_pitch
                new_req_y = math.ceil(new_req_y/bonding_pitch)*bonding_pitch
                if new_req_x > current_x:
                    current_x = new_req_x
                if new_req_y > current_y:
                    current_y = new_req_y

        # TODO: This is not strictly accurate. The aspect ratio requirement may break down when the chip becomes pad limited.
        #       Consider updating this if the connected placement tool does not account for pad area.
        required_area = area_per_pad * num_pads #current_x * current_y #current_side**2
        if required_area <= current_x*current_y:
            grid_x = math.ceil(current_x / bonding_pitch)
            grid_y = math.ceil(current_y / bonding_pitch)
        else:
            # Expand shorter side until sides are the same length, then expand both.
            if current_x < current_y:
                # Y is larger
                if current_y**2 <= required_area:
                    grid_y = math.ceil(current_y / bonding_pitch)
                    grid_x = math.ceil((required_area/current_y) / bonding_pitch)
                else:
                    required_side = math.sqrt(required_area)
                    grid_x = math.ceil(required_side / bonding_pitch)
                    grid_y = grid_x
            elif current_y < current_x:
                # X is larger
                if current_x**2 <= required_area:
                    grid_x = math.ceil(current_x / bonding_pitch)
                    grid_y = math.ceil((required_area/current_x) / bonding_pitch)
                else:
                    required_side = math.sqrt(required_area)
                    grid_x = math.ceil(required_side / bonding_pitch)
                    grid_y = grid_x
            else:
                # Both are the same size
                required_side = math.sqrt(required_area)
                grid_x = math.ceil(required_side / bonding_pitch)
                grid_y = grid_x

        pad_area = grid_x * grid_y * area_per_pad
        # print("Pad area is " + str(pad_area) + ".")

        return pad_area

    # Get the area of the interposer based on areas of the consituent chiplets.
    # Note that this is an approximation that assumes square chiplets that pack perfectly so it is an optimistic solution that actually gives a lower bound on area.
    # TODO: Implement proper packing and aspect ratio shaping so this is a legitimate solution instead of a strange L shaped interposer for example.
    def compute_area(self):
        if self.bb_area is not None:
            return self.bb_area

        # print("Computing area for chip " + self.name + "...")
        chip_io_area = self.core_area + self.get_io_area()
        #print("Chip io area: " + str(chip_io_area))

        pad_required_area = self.get_pad_area()
        #print("Pad required area: " + str(pad_required_area))

        stacked_die_bound_area = self.get_stacked_die_area()
        #print("Stacked die bound area: " + str(stacked_die_bound_area))
        #for chip in self.get_chips():
        #    chip_contribution = self.expandedArea(chip.core_area + chip.get_io_area(), self.assembly_process.die_separation/2)
        #    # print("\tAdding " + str(chip_contribution) + " from chip " + chip.name + " to stacked_die_bound_area.")
        #    stacked_die_bound_area += chip_contribution
        ## print("\tStacked die bound area is " + str(stacked_die_bound_area) + ".")

        # print("Selecting the maximum from (stacked_die_bound_area,pad_required_area,chip_io_area): " + str(stacked_die_bound_area) + ", " + str(pad_required_area) + ", and " + str(chip_io_area) + ".")
        # chip_area is the maximum value of the chip_io_area, stacked_die_bound_area, and pad_required_area.
        chip_area = max(stacked_die_bound_area, pad_required_area, chip_io_area)
        #print("Chip area: " + str(chip_area))

        return chip_area
 
    def compute_number_reticles(self, area) -> int:
        # TODO: Ground this by actually packing rectangles to calculate a more accurate number of reticles.
        reticle_area = self.get_reticle_x()*self.get_reticle_y()
        num_reticles = math.ceil(area/reticle_area)
        largest_square_side = math.floor(math.sqrt(num_reticles))
        largest_square_num_reticles = largest_square_side**2
        num_stitches = largest_square_side*(largest_square_side-1)*2+2*(num_reticles-largest_square_num_reticles)-math.ceil((num_reticles-largest_square_num_reticles)/largest_square_side)
        return num_reticles, num_stitches
        
    def compute_layer_aware_yield(self) -> float:
        layer_yield = 1.0
        for layer in self.stackup:
            layer_yield *= layer.layer_yield(self.core_area + self.get_io_area())

        return layer_yield

    # Get probability that all component tested chips are good.
    def quality_yield(self) -> float:
        quality_yield = 1.0
        for chip in self.chips:
            quality_yield *= chip.get_quality()
        return quality_yield

    def get_signal_count(self,internal_block_list):
        # print("Getting signal count")
        signal_count = 0
        # This is a dictionary where the key is the reach and the value is the number of signals with that reach.
        signal_with_reach_count = {}

        block_index = None
        internal_block_list_indices = []
        for i in range(len(self.block_names)):
            if self.block_names[i] == self.name:
                block_index = i
            if self.block_names[i] in internal_block_list:
                internal_block_list_indices.append(i)
        if block_index is None:
            #print("Warning: Chip " + self.name + " not found in block list netlist: " + str(self.block_names) + ". This can be ignored if the chip is a pass-through chip.")
            return 0, {}
        for io_type in self.global_adjacency_matrix:
            # TODO: Fix this when the adjacency matrix is properly implemented.
            for io in self.io_list:
                if io.type == io_type:
                    break
            if io.bidirectional:
                bidirectional_factor = 0.5
            else:
                bidirectional_factor = 1.0
            # Add all the entries in the row and column of the global adjacency matrix with the index correesponding to the name of the chip and weight with the wire_count of the IO type.
            for j in range(len(self.global_adjacency_matrix[io_type][block_index][:])):
                # print("Internal block list indices = " + str(internal_block_list_indices) + ".")
                # print("Adjacency matrix:" + str(self.global_adjacency_matrix[io_type][:][:]))
                if j not in internal_block_list_indices:
                    # print("Adding to signal count for " + self.block_names[j] + ".")
                    # print("io signal width = " + str(io.get_wire_count()) + ".")
                    # print("Signal count before = " + str(signal_count) + ".")
                    signal_count += (self.global_adjacency_matrix[io_type][block_index][j] + self.global_adjacency_matrix[io_type][j][block_index]) * io.wire_count * bidirectional_factor
                    # print("Signal count after = " + str(signal_count) + ".")
                    if str(io.reach) in signal_with_reach_count:
                        signal_with_reach_count[str(io.reach)] += (self.global_adjacency_matrix[io_type][block_index][j] + self.global_adjacency_matrix[io_type][j][block_index]) * io.wire_count * bidirectional_factor
                    else:
                        signal_with_reach_count[str(io.reach)] = (self.global_adjacency_matrix[io_type][block_index][j] + self.global_adjacency_matrix[io_type][j][block_index]) * io.wire_count * bidirectional_factor
            #signal_count += (sum(self.global_adjacency_matrix[io_type][block_index][:]) + sum(self.global_adjacency_matrix[io_type][:][block_index])) * io.wire_count
        
        # print("Signal count = " + str(signal_count) + ".")
        # print("Signal with reach count = " + str(signal_with_reach_count) + ".")

        # print()

        return signal_count, signal_with_reach_count

    def get_signal_power(self,internal_block_list) -> float:
        signal_power = 0.0
        block_index = None
        internal_block_list_indices = []
        for i in range(len(self.block_names)):
            if self.block_names[i] == self.name:
                block_index = i
            if self.block_names[i] in internal_block_list:
                internal_block_list_indices.append(i)
        # if block_index is None: #This is a chip with only pass-through connections such as an interposer.
            # return 0
        for io_type in self.global_adjacency_matrix:
            # TODO: Fix this when the local adjacency matrix is properly implemented.
            for io in self.io_list:
                if io.type == io_type:
                    break
            if io.bidirectional:
                bidirectional_factor = 0.5
            else:
                bidirectional_factor = 1.0
            link_weighted_sum = 0.0

            for index in internal_block_list_indices:
                # Sum of row and columns of the global adjacency matrix weighted element-wise by the average bandwidth utilization.
                value = (sum(self.global_adjacency_matrix[io_type][:][index]*self.average_bandwidth_utilization[io_type][:][index]) + sum(self.global_adjacency_matrix[io_type][index][:]*self.average_bandwidth_utilization[io_type][index][:]))
                link_weighted_sum += value
            signal_power += link_weighted_sum * io.bandwidth * io.energy_per_bit * bidirectional_factor
            #signal_power += link_weighted_sum * io.bandwidth * 1000000000 * io.energy_per_bit * bidirectional_factor

        return signal_power

    def get_chip_list(self):
        chip_list = []
        for chip in self.chips:
            chip_list.append(chip.get_chip_list())
        chip_list.append(self.name)
        return chip_list

    def get_chips_signal_count(self) -> int:
        signal_count = 0

        internal_chip_list = self.get_chip_list()

        for chip in self.chips:
            signal_count += chip.get_signal_count(internal_chip_list)[0]
        return signal_count

    # This computes the true yield of a chip assembly.
    def compute_chip_yield(self) -> float:
        # Account for the quality of the chip after self-test.
        chip_true_yield = self.get_self_quality()
        # Account for quality of component chiplets.
        quality_yield = self.quality_yield()
        # Account for assembly yield.
        assembly_yield = self.assembly_process.assembly_yield(self.get_chips_len(),self.get_chips_signal_count(),self.get_stacked_die_area())
        # Multiply the yields.
        chip_true_yield *= quality_yield*assembly_yield*self.get_wafer_process_yield()
        return chip_true_yield

    def wafer_area_eff(self) -> float:
        # TODO: Need to add a function or closed form solution to find the Gauss' circle problem for the number of chips that can fit on a wafer.
        usable_wafer_radius = (self.get_wafer_diameter()/2)-self.get_edge_exclusion()
        usable_wafer_area = math.pi*(usable_wafer_radius)**2
        return usable_wafer_area

    def get_layer_aware_cost(self):
        cost = 0
        for layer in self.stackup:
            cost += layer.layer_cost(self.get_area(), self.aspect_ratio, self.wafer_process)
        return cost

    def get_mask_cost(self):
        cost = 0
        for layer in self.stackup:
            cost += layer.mask_cost
        cost *= self.reticle_share
        return cost

    def compute_nre_cost(self) -> float:

        nre_cost = (self.get_nre_design_cost() + self.get_mask_cost() + self.test_process.get_atpg_cost(self))/self.quantity
        for i in range(len(self.chips)):
            nre_cost += self.chips[i].compute_nre_cost()

        return nre_cost

    def compute_self_cost(self) -> float:
        cost = 0.0

        # The bb_cost parameter will override the self cost computation.
        if self.bb_cost is not None:
            cost = self.bb_cost
        else:
            # Add cost of this chip
            self_layer_cost = self.get_layer_aware_cost()
            cost += self_layer_cost
            # NRE Cost
            # nre_cost = self.compute_nre_cost()
            
            # Add test cost
            self_test_cost = self.test_process.compute_self_test_cost(self)
            cost += self_test_cost

            cost = cost/self.get_self_test_yield()
            # cost += nre_cost

        return cost

    def compute_cost(self) -> float:
        cost = self.get_self_cost()
        #print()
        #print("Self cost = " + str(cost))

        stack_cost = 0.0
        # Add cost of stacked chips
        for i in range(len(self.chips)):
            stack_cost += self.chips[i].get_cost()
        #print("Stack cost = " + str(stack_cost))
        cost += stack_cost

        # Add assembly cost 
        assembly_cost = self.assembly_process.assembly_cost(self.get_chips_len(),self.get_stacked_die_area())
        #print("Assembly cost = " + str(assembly_cost))
        cost += assembly_cost

        # Add assembly test cost
        assembly_test_cost = self.test_process.compute_assembly_test_cost(self)
        #print("Assembly test cost = " + str(assembly_test_cost))
        cost += assembly_test_cost

        cost = cost/self.get_chip_test_yield()
        #print("Total Cost = " + str(cost))
        #print()

        return cost
    
    def compute_self_perfect_yield_cost(self) -> float:
        cost = 0.0

        # The bb_cost parameter will override the self cost computation.
        if self.bb_cost is not None:
            cost = self.bb_cost
        else:
            # Add cost of this chip
            self_layer_cost = self.get_layer_aware_cost()
            cost += self_layer_cost
            # NRE Cost
            # nre_cost = self.compute_nre_cost()
            
            # Add test cost
            self_test_cost = self.test_process.compute_self_test_cost(self)
            cost += self_test_cost

        return cost

    def compute_perfect_yield_cost(self) -> float:
        cost = self.compute_self_perfect_yield_cost()
        #print()
        #print("Self cost = " + str(cost))

        stack_cost = 0.0
        # Add cost of stacked chips
        for i in range(len(self.chips)):
            stack_cost += self.chips[i].compute_perfect_yield_cost()
        #print("Stack cost = " + str(stack_cost))
        cost += stack_cost

        # Add assembly cost 
        assembly_cost = self.assembly_process.assembly_cost(self.get_chips_len(),self.get_stacked_die_area())
        #print("Assembly cost = " + str(assembly_cost))
        cost += assembly_cost

        # Add assembly test cost
        assembly_test_cost = self.test_process.compute_assembly_test_cost(self)
        #print("Assembly test cost = " + str(assembly_test_cost))
        cost += assembly_test_cost

        return cost
    
    def compute_scrap_cost(self) -> float:
        return self.compute_cost() - self.compute_perfect_yield_cost()

    def compute_total_non_scrap_cost(self) -> float:
        return self.compute_perfect_yield_cost() + self.compute_nre_cost()

    def compute_total_cost(self) -> float:
        #print("compute_cost: " + str(self.compute_cost()))
        #print("compute_nre_cost: " + str(self.compute_nre_cost()))
        #print("==================================================")
        #self.print_description()
        #print("==================================================")
        total_cost = self.compute_cost() + self.compute_nre_cost()
        return total_cost

    # ===== End of Other Functions =====








# Interconnect Adjacency Matrix Class
# The class has the following attributes (These should be treated as private.):
#   type: The type of IO for this adjacency matrix. (Select from list of IO definitions.)
#   block_names: The names of the blocks in the adjacency matrix.
#   adjacency_matrix: The adjacency matrix itself.
#   static: A boolean value indicating whether the adjacency matrix is static or not. (This is meant to act like a latch.)
# The class has the following methods:
#   get_type(): Returns the type of the adjacency matrix.
#   set_type(): Sets the type of the adjacency matrix.
#   get_block_names_length(): Returns the length of the block names list.
#   get_block_names_entry(index): Returns the block name at the given index.
#   set_block_names_entry(index, value): Sets the block name at the given index to the given value.
#   get_block_names(): Returns the block names of the adjacency matrix.
#   set_block_names(): Sets the block names of the adjacency matrix.
#   get_adjacency_matrix_shape(): Returns the shape of the adjacency matrix.
#   get_adjacency_matrix_entry(row, column): Returns the entry at the given row and column.
#   set_adjacency_matrix_entry(row, column, value): Sets the entry at the given row and column to the given value.
#   get_adjacency_matrix(): Returns the adjacency matrix.
#   set_adjacency_matrix(): Sets the adjacency matrix.
#   get_static(): Returns the static value of the adjacency matrix.
#   set_static(): Sets the static value of the adjacency matrix.

#class InterconnectAdjacencyMatrix:
#    def __init__(self, type=None, IO_list=None, block_names=None, adjacency_matrix=[], static=False) -> None:
#        self.type = type
#        self.block_names = block_names
#        self.adjacency_matrix = adjacency_matrix
#        self.static = static
#        if self.type is None:
#            print("Error: Type not defined for Interconnect Adjacency Matrix. Exiting...")
#            sys.exit(1) 
#        # If the adjacency matrix is empty, exit.
#        if self.adjacency_matrix == []:
#            print("Error: Adjacency matrix not defined for Interconnect Adjacency Matrix. Exiting...")
#            sys.exit(1)
#        # If the adjacency matrix is not square, exit.
#        if len(self.adjacency_matrix) != len(self.adjacency_matrix[0]) or len(self.adjacency_matrix.shape) != 2:
#            print("Error: Adjacency matrix is not square. Exiting...")
#            sys.exit(1)
#        if self.block_names is None:
#            print("Warning: Block names not defined for Interconnect Adjacency Matrix. Generating default block names.")
#            block_names = []
#            for i in range(len(self.adjacency_matrix)):
#                block_names.append("Block " + str(i))
#        # If block_names is not the same length as the side of adjacency matrix exit.
#        if len(self.block_names) != len(self.adjacency_matrix):
#            print("Error: Block names is not the same length as the side of the adjacency matrix. Exiting...")
#            sys.exit(1)
#        if IO_list is None:
#            print("Error: IO list not defined for Interconnect Adjacency Matrix. Exiting...")
#            sys.exit(1)
#        self.IO = None
#        for IO in IO_list:
#            if IO.get_type() == type:
#                self.IO = IO
#                break
#        if self.IO is None:
#            print("Error: No IO of type " + type + " found.")
#            print("Exiting...")
#            sys.exit(1)
#        return
#
#    # ===== Get/Set Functions =====
#
#    def get_type(self) -> str:
#        return self.type
#
#    def get_block_names_len(self) -> int:
#        return len(self.block_names)
#
#    def get_block_names_entry(self, index) -> str:
#        return self.block_names[index]
#
#    def set_block_names_entry(self, index, value) -> int:
#        if (self.static):
#            print("Error: Cannot change static IO.")
#            return 1
#        else:
#            self.block_names[index] = value
#            return 0    
#
#    def get_block_names(self) -> list:
#        return self.block_names
#
#    def set_block_names(self, value) -> int:
#        if (self.static):
#            print("Error: Cannot change static IO.")
#            return 1
#        else:
#            self.block_names = value
#            return 0
#
#    def get_adjacency_matrix_shape(self) -> tuple:
#        return self.adjacency_matrix.shape
#
#    def get_adjacency_matrix_entry(self, TX, RX) -> int:
#        return self.adjacency_matrix[TX][RX]
#    
#    def set_adjacency_matrix_entry(self, TX, RX, value) -> int:
#        if (self.static):
#            print("Error: Cannot change static IO.")
#            return 1
#        else:
#            self.adjacency_matrix[TX][RX] = value
#            return 0
#
#    def get_adjacency_matrix(self) -> np.ndarray:
#        return self.adjacency_matrix
#
#    def set_adjacency_matrix(self, value) -> int:
#        if (self.static):
#            print("Error: Cannot change static IO.")
#            return 1
#        else:
#            self.adjacency_matrix = value
#            return 0
#
#    def get_static(self) -> bool:
#        return self.static
#    
#    def set_static(self) -> int:
#        self.static = True
#        return 0
#
#    # ===== End of Get/Set Functions =====
#
#    # ===== Print Functions =====
#
#    def print_description(self) -> None:
#        print("Type: " + self.type)
#        print("Static: " + str(self.static))
#
#        print("\t\t",end="")   
#        for i in range(len(self.block_names)):
#            print(self.block_names[i],end="\t")
#        print()
#        for i in range(len(self.block_names)):
#            print(self.block_names[i],end="\t")
#            for j in range(len(self.block_names)):
#                print(self.adjacency_matrix[i][j],end="\t")
#        return
#
#    # ===== End of Print Functions =====
#
#    # ===== Other Functions =====
#
#    def combine_blocks(self, block_1, block_2) -> int:
#        if (self.static):
#            print("Error: Cannot change static IO.")
#            return 1
#        else:
#            if block_1 == block_2:
#                print("Error: Cannot combine a block with itself.")
#                return 1
#            self.block_names[block_1] = self.block_names[block_1] + "," + self.block_names[block_2]
#            self.block_names.pop(block_2)
#            shape_am = self.adjacency_matrix.shape
#            for i in range(shape_am[0]):
#                if i != block_1 and i != block_2:
#                    self.adjacency_matrix[i][block_1] = self.adjacency_matrix[i][block_1] + self.adjacency_matrix[i][block_2]
#                    self.adjacency_matrix[i][block_2] = 0
#            for i in range(shape_am[1]):
#                if i != block_1 and i != block_2:
#                    self.adjacency_matrix[block_1][i] = self.adjacency_matrix[block_1][i] + self.adjacency_matrix[block_2][i]
#                    self.adjacency_matrix[block_2][i] = 0
#            self.adjacency_matrix = np.delete(self.adjacency_matrix, block_2, 0)
#            self.adjacency_matrix = np.delete(self.adjacency_matrix, block_2, 1)
#            return 0  
#
#    # ===== End of Other Functions =====
