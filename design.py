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
import copy


# =========================================
# Custom Exceptions
# =========================================
class DesignError(Exception):
    """Base class for exceptions in this module."""
    pass

class ConfigurationError(DesignError):
    """Exception raised for errors in the input configuration or object setup."""
    pass

class CalculationError(DesignError):
    """Exception raised for errors during calculation, such as physical impossibilities."""
    pass


# =========================================
# Wafer Process Class
# =========================================
# The class has the following attributes:
#   name: The name of the wafer process.
#   wafer_diameter: The diameter of the wafer in mm.
#   edge_exclusion: The edge exclusion of the wafer in mm.
#   wafer_process_yield: The yield of the wafer process. Value should be between 0 and 1.
#   dicing_distance: Width of scribe line in mm.
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
# The class has the following methods:
#   __init__(...): Initializes the WaferProcess object.
#   __str__(): Returns a string representation of the object.
#   wafer_fully_defined(): Checks if all attributes are defined.
#   set_static(): Sets the 'static' flag to True to prevent further modifications.
# =========================================

class WaferProcess:
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) != str:
                raise ConfigurationError("Wafer process name must be a string.")
            else:
                self.__name = value    
                return 0
        
    @property
    def wafer_diameter(self):
        return self.__wafer_diameter
    @wafer_diameter.setter
    def wafer_diameter(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Wafer diameter must be a number.")
            elif value < 0:
                raise ConfigurationError("Wafer diameter must be nonnegative.")
            else:
                self.__wafer_diameter = value
                return 0

    @property
    def edge_exclusion(self):
        return self.__edge_exclusion
    @edge_exclusion.setter
    def edge_exclusion(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Edge exclusion must be a number.")
            elif value < 0:
                raise ConfigurationError("Edge exclusion must be nonnegative.")
            elif value > self.wafer_diameter/2:
                raise ConfigurationError("Edge exclusion must be less than half the wafer diameter.")
            else:
                self.__edge_exclusion = value
                return 0
        
    @property
    def wafer_process_yield(self):
        return self.__wafer_process_yield
    @wafer_process_yield.setter
    def wafer_process_yield(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Wafer process yield must be a number.")
            elif value < 0.0 or value > 1.0:
                raise ConfigurationError("Wafer process yield must be between 0 and 1.")
            else:
                self.__wafer_process_yield = value
                return 0

    @property
    def dicing_distance(self):
        return self.__dicing_distance
    @dicing_distance.setter
    def dicing_distance(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Dicing distance must be a number.")
            elif value < 0:
                raise ConfigurationError("Dicing distance must be nonnegative.")
            elif value > self.wafer_diameter/2:
                raise ConfigurationError("Dicing distance must be less than half the wafer diameter.")
            else:
                self.__dicing_distance = value
                return 0
        
    @property
    def reticle_x(self):
        return self.__reticle_x
    @reticle_x.setter
    def reticle_x(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Reticle x dimension must be a number.")
            elif value < 0:
                raise ConfigurationError("Reticle x dimension must be nonnegative.")
            elif value > self.wafer_diameter/2:
                raise ConfigurationError("Reticle x dimension must be less than half the wafer diameter.")
            else:
                self.__reticle_x = value
                return 0

    @property
    def reticle_y(self):
        return self.__reticle_y
    @reticle_y.setter
    def reticle_y(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Reticle y dimension must be a number.")
            elif value < 0:
                raise ConfigurationError("Reticle y dimension must be nonnegative.")
            elif value > self.wafer_diameter/2:
                raise ConfigurationError("Reticle y dimension must be less than half the wafer diameter.")
            else:
                self.__reticle_y = value
                return 0
        
    @property
    def wafer_fill_grid(self):
        return self.__wafer_fill_grid
    @wafer_fill_grid.setter
    def wafer_fill_grid(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) != str:
                raise ConfigurationError("Wafer fill grid must be a string. (True or False)")
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
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("NRE front end cost per mm^2 memory must be a number.")
            elif value < 0:
                raise ConfigurationError("NRE front end cost per mm^2 memory must be nonnegative.")
            else:
                self.__nre_front_end_cost_per_mm2_memory = value
                return 0

    @property
    def nre_back_end_cost_per_mm2_memory(self):
        return self.__nre_back_end_cost_per_mm2_memory
    @nre_back_end_cost_per_mm2_memory.setter
    def nre_back_end_cost_per_mm2_memory(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("NRE back end cost per mm^2 memory must be a number.")
            elif value < 0:
                raise ConfigurationError("NRE back end cost per mm^2 memory must be nonnegative.")
            else:
                self.__nre_back_end_cost_per_mm2_memory = value
                return 0
        
    @property
    def nre_front_end_cost_per_mm2_logic(self):
        return self.__nre_front_end_cost_per_mm2_logic
    @nre_front_end_cost_per_mm2_logic.setter
    def nre_front_end_cost_per_mm2_logic(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("NRE front end cost per mm^2 logic must be a number.")
            elif value < 0:
                raise ConfigurationError("NRE front end cost per mm^2 logic must be nonnegative.")
            else:
                self.__nre_front_end_cost_per_mm2_logic = value
                return 0
        
    @property
    def nre_back_end_cost_per_mm2_logic(self):
        return self.__nre_back_end_cost_per_mm2_logic
    @nre_back_end_cost_per_mm2_logic.setter
    def nre_back_end_cost_per_mm2_logic(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("NRE back end cost per mm^2 logic must be a number.")
            elif value < 0:
                raise ConfigurationError("NRE back end cost per mm^2 logic must be nonnegative.")
            else:
                self.__nre_back_end_cost_per_mm2_logic = value
                return 0
        
    @property
    def nre_front_end_cost_per_mm2_analog(self):
        return self.__nre_front_end_cost_per_mm2_analog
    @nre_front_end_cost_per_mm2_analog.setter
    def nre_front_end_cost_per_mm2_analog(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("NRE front end cost per mm^2 analog must be a number.")
            elif value < 0:
                raise ConfigurationError("NRE front end cost per mm^2 analog must be nonnegative.")
            else:
                self.__nre_front_end_cost_per_mm2_analog = value
                return 0
        
    @property
    def nre_back_end_cost_per_mm2_analog(self):
        return self.__nre_back_end_cost_per_mm2_analog
    @nre_back_end_cost_per_mm2_analog.setter
    def nre_back_end_cost_per_mm2_analog(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static wafer process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("NRE back end cost per mm^2 analog must be a number.")
            elif value < 0:
                raise ConfigurationError("NRE back end cost per mm^2 analog must be nonnegative.")
            else:
                self.__nre_back_end_cost_per_mm2_analog = value
                return 0
        
    @property
    def static(self):
        return self.__static
    @static.setter
    def static(self, value):
        self.__static = value

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

    def __str__(self) -> str:
        return_str = "Wafer Process Name: " + self.name
        return_str += "\n\r\tWafer Diameter: " + str(self.wafer_diameter)
        return_str += "\n\r\tEdge Exclusion: " + str(self.edge_exclusion)
        return_str += "\n\r\tWafer Process Yield: " + str(self.wafer_process_yield) 
        return_str += "\n\r\tDicing Distance: " + str(self.dicing_distance)
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
                self.wafer_process_yield is None or self.dicing_distance is None or self.reticle_x is None or self.reticle_y is None or 
                self.wafer_fill_grid is None or self.nre_front_end_cost_per_mm2_memory is None or 
                self.nre_back_end_cost_per_mm2_memory is None or self.nre_front_end_cost_per_mm2_logic is None or 
                self.nre_back_end_cost_per_mm2_logic is None or self.nre_front_end_cost_per_mm2_analog is None or 
                self.nre_back_end_cost_per_mm2_analog is None):
            return False
        else:
            return True

    def set_static(self) -> int:
        if not self.wafer_fully_defined():
            raise ConfigurationError(f"Attempt to set wafer process '{self.name}' static without defining all parameters.\n{self}")
        self.static = True
        return 0


# =========================================
# IO Class
# =========================================
# The class has the following attributes:
#   type: The type of IO for this adjacency matrix. (Select from list of IO definitions.)
#   rx_area: The area of RX IOs in mm^2.
#   tx_area: The area of TX IOs in mm^2.
#   shoreline: The shoreline of the IO in mm.
#   bandwidth: The bandwidth of the IO in Gbps.
#   wire_count: The number of wires in the IO.
#   bidirectional: Whether the IO is bidirectional or not.
#   energy_per_bit: The energy per bit of the IO in pJ/bit.
#   reach: The reach of the IO in mm.
#   static: A boolean set true when the IO is defined to prevent further changes.
# =========================================
# The class has the following methods:
#   __init__(...): Initializes the IO object.
#   __str__(): Returns a string representation of the object.
#   io_fully_defined(): Checks if all attributes are defined.
#   set_static(): Sets the 'static' flag to True to prevent further modifications.
# =========================================

class IO:
    @property
    def type(self):
        return self.__type
    @type.setter
    def type(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static IO.")
        else:
            if type(value) != str:
                raise ConfigurationError("IO type must be a string.")
            else:
                self.__type = value
                return 0

    @property
    def rx_area(self):
        return self.__rx_area
    @rx_area.setter
    def rx_area(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static IO.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("RX area must be a number.")
            elif value < 0:
                raise ConfigurationError("RX area must be nonnegative.")
            else:
                self.__rx_area = value
                return 0

    @property
    def tx_area(self):
        return self.__tx_area
    @tx_area.setter
    def tx_area(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static IO.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("TX area must be a number.")
            elif value < 0:
                raise ConfigurationError("TX area must be nonnegative.")
            else:
                self.__tx_area = value
                return 0

    @property
    def shoreline(self):
        return self.__shoreline
    @shoreline.setter
    def shoreline(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static IO.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Shoreline must be a number.")
            elif value < 0:
                raise ConfigurationError("Shoreline must be nonnegative.")
            else:
                self.__shoreline = value
                return 0

    @property
    def bandwidth(self):
        return self.__bandwidth
    @bandwidth.setter
    def bandwidth(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static IO.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Bandwidth must be a number.")
            elif value < 0:
                raise ConfigurationError("Bandwidth must be nonnegative.")
            else:
                self.__bandwidth = value
                return 0

    @property
    def wire_count(self):
        return self.__wire_count
    @wire_count.setter
    def wire_count(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static IO.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Wire count must be a number.")
            elif value < 0:
                raise ConfigurationError("Wire count must be nonnegative.")
            else:
                self.__wire_count = value
                return 0

    @property
    def bidirectional(self):
        return self.__bidirectional
    @bidirectional.setter
    def bidirectional(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static IO.")
        else:
            if type(value) != str:
                raise ConfigurationError("Bidirectional must be a string. (True or False)")
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
            raise ConfigurationError("Cannot change static IO.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Energy per bit must be a number.")
            elif value < 0:
                raise ConfigurationError("Energy per bit must be nonnegative.")
            else:
                self.__energy_per_bit = value
                return 0

    @property
    def reach(self):
        return self.__reach
    @reach.setter
    def reach(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static IO.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Reach must be a number.")
            elif value < 0:
                raise ConfigurationError("Reach must be nonnegative.")
            else:
                self.__reach = value
                return 0

    @property
    def static(self):
        return self.__static
    @static.setter
    def static(self, value):
        self.__static = value

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
        self.energy_per_bit = energy_per_bit
        self.reach = reach
        self.static = static
        if not self.io_fully_defined():
            print("Warning: IO not fully defined, setting to non-static.")
            self.static = False
            print(self)
        return

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
            raise ConfigurationError(f"Attempt to set IO '{self.type}' static without defining all parameters.\n{self}")
        self.static = True
        return 0


# =========================================
# Layer Class
# =========================================
# The class consists of the following attributes:
#   name: The name of the layer.
#   active: Whether the layer is active or not.
#   routing_layer_count: The number of routing layers in the layer.
#                       A value of 0 will not allow any horizontal routing of signals through the layer.
#   routing_layer_pitch: The pitch of the routing layers in the layer.
#                       A value of 0 will allow for infinite wires in a single routing layer.
#   cost_per_mm2: The cost per mm^2 of the layer.
#   defect_density: The defect density of the layer.
#   critical_area_ratio: The critical area ratio of the layer.
#   clustering_factor: The clustering factor of the layer.
#   transistor_density: The transistor density of the layer in millions per mm^2.
#   litho_percent: The litho percent of the layer.
#   mask_cost: The mask cost of the layer.
#   stitching_yield: The stitching yield of the layer.
#   static: A boolean set true when the layer is defined to prevent further changes.
# =========================================
# The class has the following methods:
#   __init__(...): Initializes the Layer object.
#   __str__(): Returns a string representation of the object.
#   get_gates_per_mm2(): Calculates and returns the number of logic gates per mm^2.
#   layer_fully_defined(): Checks if all attributes are defined.
#   set_static(): Sets the 'static' flag to True to prevent further modifications.
# == Computation ==
#   compute_number_reticles(area, wp): Computes the number of reticles and stitches required for a given area.
#   layer_yield(area): Computes the yield of the layer given the area of the layer.
#   reticle_utilization(area, reticle_x, reticle_y): Computes the reticle utilization.
#   layer_cost(area, aspect_ratio, wafer_process): Computes the manufacturing cost of the layer.
#   compute_grid_dies_per_wafer(...): Calculates the number of dies that fit on a wafer with a grid alignment.
#   compute_nogrid_dies_per_wafer(...): Calculates the number of dies that fit on a wafer without a grid alignment.
#   compute_dies_per_wafer(...): Determines the number of dies per wafer based on the fill strategy.
#   compute_cost_per_mm2(area, aspect_ratio, wafer_process): Computes the effective cost per mm^2 considering wafer fit.
# =========================================

class Layer:
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) != str:
                raise ConfigurationError("Layer name must be a string.")
            else:
                self.__name = value
                return 0

    @property
    def active(self):
        return self.__active
    @active.setter
    def active(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) != str:
                raise ConfigurationError("Active must be a string. (True or False)")
            else:
                if value.lower() == "true":
                    self.__active = True
                else:
                    self.__active = False
                return 0

    @property
    def routing_layer_count(self):
        return self.__routing_layer_count
    @routing_layer_count.setter
    def routing_layer_count(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) not in [int]:
                raise ConfigurationError("Routing layer count must be an int.")
            elif value < 0:
                raise ConfigurationError("Routing layer count must be nonnegative.")
            else:
                self.__routing_layer_count = value
                return 0
    
    @property
    def routing_layer_pitch(self):
        return self.__routing_layer_pitch
    @routing_layer_pitch.setter
    def routing_layer_pitch(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Routing layer pitch must be a number.")
            elif value < 0:
                raise ConfigurationError("Routing layer pitch must be nonnegative.")
            else:
                self.__routing_layer_pitch = value
                return 0

    @property
    def cost_per_mm2(self):
        return self.__cost_per_mm2
    @cost_per_mm2.setter
    def cost_per_mm2(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Cost per mm^2 must be a number.")
            elif value < 0:
                raise ConfigurationError("Cost per mm^2 must be nonnegative.")
            else:
                self.__cost_per_mm2 = value
                return 0

    @property
    def transistor_density(self):
        return self.__transistor_density
    @transistor_density.setter
    def transistor_density(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Transistor density must be a number.")
            elif value < 0:
                raise ConfigurationError("Transistor density must be nonnegative.")
            else:
                self.__transistor_density = value
                return 0

    @property
    def defect_density(self):
        return self.__defect_density
    @defect_density.setter
    def defect_density(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Defect density must be a number.")
            elif value < 0:
                raise ConfigurationError("Defect density must be nonnegative.")
            else:
                self.__defect_density = value
                return 0

    @property
    def critical_area_ratio(self):
        return self.__critical_area_ratio
    @critical_area_ratio.setter
    def critical_area_ratio(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Critical area ratio must be a number.")
            elif value < 0:
                raise ConfigurationError("Critical area ratio must be nonnegative.")
            else:
                self.__critical_area_ratio = value
                return 0

    @property
    def clustering_factor(self):
        return self.__clustering_factor
    @clustering_factor.setter
    def clustering_factor(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Clustering factor must be a number.")
            elif value < 0:
                raise ConfigurationError("Clustering factor must be nonnegative.")
            else:
                self.__clustering_factor = value
                return 0

    @property
    def litho_percent(self):
        return self.__litho_percent
    @litho_percent.setter
    def litho_percent(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Litho percent must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Litho percent must be between 0 and 1.")
            else:
                self.__litho_percent = value
                return 0

    @property
    def mask_cost(self):
        return self.__mask_cost
    @mask_cost.setter
    def mask_cost(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Mask cost must be a number.")
            elif value < 0:
                raise ConfigurationError("Mask cost must be nonnegative.")
            else:
                self.__mask_cost = value
                return 0

    @property
    def stitching_yield(self):
        return self.__stitching_yield
    @stitching_yield.setter
    def stitching_yield(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static layer.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Stitching yield must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Stitching yield must be between 0 and 1.")
            else:
                self.__stitching_yield = value
                return 0

    @property
    def static(self):
        return self.__static
    @static.setter
    def static(self, value):
        self.__static = value

    def __init__(self, name = None, active = None, cost_per_mm2 = None, transistor_density = None, defect_density = None,
                 critical_area_ratio = None, clustering_factor = None, litho_percent = None, mask_cost = None,
                 stitching_yield = None, routing_layer_count = None, routing_layer_pitch = None, static = True) -> None:
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
        self.routing_layer_count = routing_layer_count
        self.routing_layer_pitch = routing_layer_pitch
        self.static = static
        if not self.layer_fully_defined():
            print("Warning: Layer not fully defined. Setting non-static.")
            self.static = False
            print(self)
        return

    def get_gates_per_mm2(self) -> float:
        # Transistor density is in million transistors per mm^2. 
        # An assumption of 4 transistors per standard logic gate (e.g., NAND) is used.
        return self.transistor_density * 1e6 / 4

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
            raise ConfigurationError(f"Attempt to set layer '{self.name}' static without defining all parameters.\n{self}")
        self.static = True
        return 0

    # ========== Computation Functions =========

    def compute_number_of_routing_tracks(self, area, aspect_ratio) -> int:
        # This function will compute the number of wires that can escape the bottom of a die.
        # Calculate the width and height of the area based on the aspect ratio.
        width = math.sqrt(area * aspect_ratio)
        height = area / width
        
        routing_tracks = self.routing_layer_count * ( 2 * (width + height)) / self.routing_layer_pitch

        return routing_tracks

    def compute_number_reticles(self, area, wp) -> int:
        # TODO: Ground this by actually packing rectangles to calculate a more accurate number of reticles.
        reticle_area = wp.reticle_x*wp.reticle_y
        num_reticles = math.ceil(area/reticle_area)
        # This calculation approximates the number of stitch lines required for a multi-reticle design.
        largest_square_side = math.floor(math.sqrt(num_reticles))
        largest_square_num_reticles = largest_square_side**2
        num_stitches = largest_square_side*(largest_square_side-1)*2+2*(num_reticles-largest_square_num_reticles)-math.ceil((num_reticles-largest_square_num_reticles)/largest_square_side)
        return num_reticles, num_stitches

    def layer_yield(self,area) -> float:
        # This function calculates the layer yield based on defect density and stitching yield.
        # Currently, num_stitches is 0, meaning stitching yield is not factored in here. This should be revisited for reticle-stitching designs.
        num_stitches = 0
        # The defect yield is modeled using the negative binomial distribution.
        defect_yield = (1+(self.defect_density*area*self.critical_area_ratio)/self.clustering_factor)**(-1*self.clustering_factor)
        stitching_yield = self.stitching_yield**num_stitches
        final_layer_yield = stitching_yield*defect_yield
        return final_layer_yield

    def reticle_utilization(self,area,reticle_x,reticle_y) -> float:
        reticle_area = reticle_x*reticle_y
        # If the chip area is larger than the reticle area, this requires stitching.
        # The model assumes multiple reticles are used, effectively increasing the "total" reticle area.
        while reticle_area < area:
            reticle_area += reticle_x*reticle_y
        # Calculate how many full chips can be patterned within one reticle exposure area.
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
            # First, compute the cost of the layer before considering the scaling of lithography costs with reticle fit.
            layer_cost = area*self.compute_cost_per_mm2(area,aspect_ratio,wafer_process)

            # Get utilization based on reticle fit.
            # Edge case to avoid division by zero.
            if (self.litho_percent == 0.0):
                reticle_utilization = 1.0
            elif (self.litho_percent > 0.0):
                reticle_utilization = self.reticle_utilization(area,wafer_process.reticle_x,wafer_process.reticle_y)
            # A negative percent does not make sense and should crash the program.
            else:
                raise CalculationError("Negative litho percent in Layer.layer_cost().")

            # Scale the lithography component of the manufacturing cost by the reticle utilization.
            # Poor utilization increases the effective cost of the lithography steps.
            layer_cost = layer_cost*(1-self.litho_percent) + (layer_cost*self.litho_percent)/reticle_utilization

        # Negative area does not make sense and should crash the program.
        else:
            raise CalculationError("Negative area in Layer.layer_cost().")

        return layer_cost

    def compute_grid_dies_per_wafer(self, x_dim, y_dim, usable_wafer_diameter, dicing_distance):
        # This is a full calculator for die placement on a wafer assuming a grid layout.
        # It iterates through possible starting orientations to maximize the number of dies.
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
                chord_length = math.sqrt(r**2 - row_chord_height**2)*2
    
                # Compute how many squares over from the first square it is possible to fit another square on top.
                location_of_first_fit_candidate = (usable_wafer_diameter - chord_length)/2
                starting_location = math.ceil((location_of_first_fit_candidate - starting_distance_from_left)/x_dim_eff)*x_dim_eff + starting_distance_from_left
                effective_cord_length = chord_length - (starting_location - location_of_first_fit_candidate)
                dies_per_wafer += 2*math.floor(effective_cord_length/x_dim_eff)
                for j in range(math.floor(effective_cord_length/x_dim_eff)):
                    x = starting_location + j*x_dim_eff - usable_wafer_diameter/2
                    y = row_chord_height - y_dim_eff
                    die_locations.append((x, y))
                    die_locations.append((x, -1*y-y_dim_eff))
                row_chord_height += y_dim_eff
    
            if dies_per_wafer > best_dies_per_wafer:
                best_dies_per_wafer = dies_per_wafer
                best_die_locations = die_locations
            left_column_height = left_column_height + 1
    
        return best_dies_per_wafer
    
    def compute_nogrid_dies_per_wafer(self, x_dim, y_dim, usable_wafer_diameter, dicing_distance):
        # This function calculates the number of dies that can be placed on a wafer when
        # vertical alignment (grid) is not required. It considers two primary packing cases.
        x_dim_eff = x_dim + dicing_distance
        y_dim_eff = y_dim + dicing_distance
        
        # Case 1: The first row of dies is centered on the wafer's horizontal diameter.
        num_squares_case_1 = 0
        die_locations_1 = []
        row_chord_height = y_dim_eff/2
        chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height - dicing_distance/2)**2)*2 + dicing_distance
        num_squares_case_1 += math.floor(chord_length/x_dim_eff)
        for j in range(math.floor(chord_length/x_dim_eff)):
            x = j*x_dim_eff - chord_length/2
            y = -1*y_dim_eff/2
            die_locations_1.append((x, y))
        row_chord_height += y_dim_eff
        # Iterate through subsequent rows above and below the center.
        while row_chord_height < usable_wafer_diameter/2:
            chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height - dicing_distance/2)**2)*2 + dicing_distance
            num_squares_case_1 += 2*math.floor(chord_length/x_dim_eff)
            for j in range(math.floor(chord_length/x_dim_eff)):
                x = j*x_dim_eff - chord_length/2
                y = row_chord_height - y_dim_eff
                die_locations_1.append((x, y))
                die_locations_1.append((x, -1*y-y_dim_eff))
            row_chord_height += y_dim_eff

        # Case 2: The first two rows of dies are placed just above and below the diameter.
        num_squares_case_2 = 0
        die_locations_2 = []
        row_chord_height = y_dim_eff
        chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height - dicing_distance/2)**2)*2 + dicing_distance
        num_squares_case_2 += 2*math.floor(chord_length/x_dim_eff)
        row_chord_height += y_dim_eff
        while row_chord_height < usable_wafer_diameter/2:
            chord_length = math.sqrt((usable_wafer_diameter/2)**2 - (row_chord_height - dicing_distance/2)**2)*2 + dicing_distance
            num_squares_case_2 += 2*math.floor(chord_length/x_dim_eff)
            row_chord_height += y_dim_eff

        # Return the maximum number of dies from the two cases considered.
        if num_squares_case_2 > num_squares_case_1:
            num_squares = num_squares_case_2
        else:
            num_squares = num_squares_case_1
        
        return num_squares

    def compute_dies_per_wafer(self, x_dim, y_dim, usable_wafer_diameter, dicing_distance, grid_fill):
        # This function computes the number of dies that can fit on a wafer.
        # It can use a simple approximation or a more detailed calculation based on the grid_fill flag.
        simple_equation_flag = False

        if simple_equation_flag:
            # A simplified analytical equation for estimating dies per wafer.
            num_squares = usable_wafer_diameter*math.pi*((usable_wafer_diameter/(4*(y_dim+dicing_distance)*(x_dim+dicing_distance)))-(1/math.sqrt(2*(y_dim+dicing_distance)*(x_dim+dicing_distance))))
        else:
            # Use more detailed geometric calculations based on the fill strategy.
            if grid_fill:
                num_squares = self.compute_grid_dies_per_wafer(x_dim, y_dim, usable_wafer_diameter, dicing_distance)
            else:
                num_squares = self.compute_nogrid_dies_per_wafer(x_dim, y_dim, usable_wafer_diameter, dicing_distance)

        return num_squares

    def compute_cost_per_mm2(self, area, aspect_ratio, wafer_process) -> float:
        # Access parameters that will be used multiple times.
        wafer_diameter = wafer_process.wafer_diameter
        grid_fill = wafer_process.wafer_fill_grid

        # Calculate die dimensions from area and aspect ratio.
        x_dim = math.sqrt(area*aspect_ratio)
        y_dim = math.sqrt(area/aspect_ratio)

        # Find effective wafer diameter that is valid for placing dies.
        usable_wafer_diameter = wafer_diameter - 2*wafer_process.edge_exclusion

        # Check if the die is too large to fit on the wafer.
        if (math.sqrt(x_dim**2 + y_dim**2) > usable_wafer_diameter/2):
            raise CalculationError("Die size is too large for accurate calculation of fit for wafer.")

        # Check for zero-sized die dimensions.
        if (x_dim == 0 or y_dim == 0):
            raise CalculationError("Die size is zero.")

        # Calculate the number of dies that can be fabricated on a single wafer.
        dies_per_wafer = self.compute_dies_per_wafer(x_dim, y_dim, usable_wafer_diameter, wafer_process.dicing_distance, grid_fill)

        if (dies_per_wafer == 0):
            raise CalculationError("Dies per wafer is zero.")

        # Compute the effective cost per mm^2 by distributing the total wafer cost over the area of the good dies.
        used_area = dies_per_wafer*area
        circle_area = math.pi*(wafer_diameter/2)**2
        cost_per_mm2 = self.cost_per_mm2*circle_area/used_area
        return cost_per_mm2

# =========================================
# Assembly Definition Class
# =========================================
# The class has attributes:
#   name: The name of the assembly process.
#   materials_cost_per_mm2: The cost of the materials per mm^2 of the assembly.
#   bb_cost_per_second: A black-box cost per second for the entire assembly process.
#   picknplace_machine_cost: The cost of the pick-and-place machine.
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
#   edge_exclusion: The distance from the edge of the substrate/interposer to the first die in mm.
#   max_pad_current_density: The maximum current density of the pads in mA/mm^2.
#   bonding_pitch: The pitch of the bonding pads in mm.
#   alignment_yield: The yield of the alignment process.
#   bonding_yield: The yield of the bonding process.
#   dielectric_bond_defect_density: The defect density of the dielectric bond.
#   static: A boolean set true when the assembly process is defined to prevent further changes.
# =========================================
# The class has the following methods:
#   __init__(...): Initializes the Assembly object.
#   __str__(): Returns a string representation of the object.
#   assembly_fully_defined(): Checks if all attributes are defined.
#   set_static(): Sets the 'static' flag to True to prevent further modifications.
#   get_power_per_pad(core_voltage): Computes the power per pad given the core voltage.
#   compute_picknplace_time(n_chips): Computes the time it takes to pick and place a given number of dies.
#   compute_bonding_time(n_chips): Computes the time it takes to bond a given number of dies.
#   assembly_time(n_chips): Computes the total assembly time.
#   compute_picknplace_cost_per_second(): Computes the cost per second of the pick-and-place process.
#   compute_bonding_cost_per_second(): Computes the cost per second of the bonding process.
#   assembly_cost(n_chips, area): Computes the cost of the assembly process.
#   assembly_yield(n_chips, n_bonds, n_tsvs, area): Computes the yield of the assembly process.
# =========================================

class Assembly:
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) != str:
                raise ConfigurationError("Assembly process name must be a string.")
            else:
                self.__name = value
                return 0

    @property
    def materials_cost_per_mm2(self):
        return self.__materials_cost_per_mm2
    @materials_cost_per_mm2.setter
    def materials_cost_per_mm2(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Materials cost per mm^2 must be a number.")
            elif value < 0:
                raise ConfigurationError("Materials cost per mm^2 must be nonnegative.")
            else:
                self.__materials_cost_per_mm2 = value
                return 0
    
    @property
    def bb_cost_per_second(self):
        return self.__bb_cost_per_second
    @bb_cost_per_second.setter
    def bb_cost_per_second(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if value == None:
                self.__bb_cost_per_second = value
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Black-box cost per second must be a number.")
            elif value < 0:
                raise ConfigurationError("Black-box cost per second must be nonnegative.")
            else:
                self.__bb_cost_per_second = value
                return 0

    @property
    def picknplace_machine_cost(self):
        return self.__picknplace_machine_cost
    @picknplace_machine_cost.setter
    def picknplace_machine_cost(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Pick and place machine cost must be a number.")
            elif value < 0:
                raise ConfigurationError("Pick and place machine cost must be nonnegative.")
            else:
                self.__picknplace_machine_cost = value
                return 0
        
    @property
    def picknplace_machine_lifetime(self):
        return self.__picknplace_machine_lifetime
    @picknplace_machine_lifetime.setter
    def picknplace_machine_lifetime(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Pick and place machine lifetime must be a number.")
            elif value < 0:
                raise ConfigurationError("Pick and place machine lifetime must be nonnegative.")
            else:
                self.__picknplace_machine_lifetime = value
                return 0
        
    @property
    def picknplace_machine_uptime(self):
        return self.__picknplace_machine_uptime
    @picknplace_machine_uptime.setter
    def picknplace_machine_uptime(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Pick and place machine uptime must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Pick and place machine uptime must be between 0 and 1.")
            else:
                self.__picknplace_machine_uptime = value
                return 0
        
    @property
    def picknplace_technician_yearly_cost(self):
        return self.__picknplace_technician_yearly_cost
    @picknplace_technician_yearly_cost.setter
    def picknplace_technician_yearly_cost(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Pick and place technician yearly cost must be a number.")
            elif value < 0:
                raise ConfigurationError("Pick and place technician yearly cost must be nonnegative.")
            else:
                self.__picknplace_technician_yearly_cost = value
                return 0
        
    @property
    def picknplace_time(self):
        return self.__picknplace_time
    @picknplace_time.setter
    def picknplace_time(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Pick and place time must be a number.")
            elif value < 0:
                raise ConfigurationError("Pick and place time must be nonnegative.")
            else:
                self.__picknplace_time = value
                return 0
        
    @property
    def picknplace_group(self):
        return self.__picknplace_group
    @picknplace_group.setter
    def picknplace_group(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) != int:
                raise ConfigurationError("Pick and place group must be an integer.")
            elif value <= 0:
                print(value)
                raise ConfigurationError("Pick and place group must be positive.")
            else:
                self.__picknplace_group = value
                return 0
        
    @property
    def bonding_machine_cost(self):
        return self.__bonding_machine_cost
    @bonding_machine_cost.setter
    def bonding_machine_cost(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Bonding machine cost must be a number.")
            elif value < 0:
                raise ConfigurationError("Bonding machine cost must be nonnegative.")
            else:
                self.__bonding_machine_cost = value
                return 0
        
    @property
    def bonding_machine_lifetime(self):
        return self.__bonding_machine_lifetime
    @bonding_machine_lifetime.setter
    def bonding_machine_lifetime(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Bonding machine lifetime must be a number.")
            elif value < 0:
                raise ConfigurationError("Bonding machine lifetime must be nonnegative.")
            else:
                self.__bonding_machine_lifetime = value
                return 0
        
    @property
    def bonding_machine_uptime(self):
        return self.__bonding_machine_uptime
    @bonding_machine_uptime.setter
    def bonding_machine_uptime(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Bonding machine uptime must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Bonding machine uptime must be between 0 and 1.")
            else:
                self.__bonding_machine_uptime = value
                return 0

    @property
    def bonding_technician_yearly_cost(self):
        return self.__bonding_technician_yearly_cost
    @bonding_technician_yearly_cost.setter
    def bonding_technician_yearly_cost(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Bonding technician yearly cost must be a number.")
            elif value < 0:
                raise ConfigurationError("Bonding technician yearly cost must be nonnegative.")
            else:
                self.__bonding_technician_yearly_cost = value
                return 0

    @property
    def bonding_time(self):
        return self.__bonding_time
    @bonding_time.setter
    def bonding_time(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Bonding time must be a number.")
            elif value < 0:
                raise ConfigurationError("Bonding time must be nonnegative.")
            else:
                self.__bonding_time = value
                return 0

    @property
    def bonding_group(self):
        return self.__bonding_group
    @bonding_group.setter
    def bonding_group(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) != int:
                raise ConfigurationError("Bonding group must be an integer.")
            elif value <= 0:
                raise ConfigurationError("Bonding group must be positive.")
            else:
                self.__bonding_group = value
                return 0

    @property
    def die_separation(self):
        return self.__die_separation
    @die_separation.setter
    def die_separation(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Die separation must be a number.")
            elif value < 0:
                raise ConfigurationError("Die separation must be nonnegative.")
            else:
                self.__die_separation = value
                return 0

    @property
    def edge_exclusion(self):
        return self.__edge_exclusion
    @edge_exclusion.setter
    def edge_exclusion(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Edge exclusion must be a number.")
            elif value < 0:
                raise ConfigurationError("Edge exclusion must be nonnegative.")
            else:
                self.__edge_exclusion = value
                return 0

    @property
    def max_pad_current_density(self):
        return self.__max_pad_current_density
    @max_pad_current_density.setter
    def max_pad_current_density(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Max pad current density must be a number.")
            elif value < 0:
                raise ConfigurationError("Max pad current density must be nonnegative.")
            else:
                self.__max_pad_current_density = value
                return 0

    @property
    def bonding_pitch(self):
        return self.__bonding_pitch
    @bonding_pitch.setter
    def bonding_pitch(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Bonding pitch must be a number.")
            elif value < 0:
                raise ConfigurationError("Bonding pitch must be nonnegative.")
            else:
                self.__bonding_pitch = value
                return 0

    @property
    def alignment_yield(self):
        return self.__alignment_yield
    @alignment_yield.setter
    def alignment_yield(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Alignment yield must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Alignment yield must be between 0 and 1.")
            else:
                self.__alignment_yield = value
                return 0

    @property
    def bonding_yield(self):
        return self.__bonding_yield
    @bonding_yield.setter
    def bonding_yield(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Bonding yield must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Bonding yield must be between 0 and 1.")
            else:
                self.__bonding_yield = value
                return 0

    @property
    def dielectric_bond_defect_density(self):
        return self.__dielectric_bond_defect_density
    @dielectric_bond_defect_density.setter
    def dielectric_bond_defect_density(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Dielectric bond defect density must be a number.")
            elif value < 0:
                raise ConfigurationError("Dielectric bond defect density must be nonnegative.")
            else:
                self.__dielectric_bond_defect_density = value
                return 0

    @property
    def static(self):
        return self.__static
    @static.setter
    def static(self, value):
        self.__static = value

    @property
    def picknplace_cost_per_second(self):
        return self.__picknplace_cost_per_second
    @picknplace_cost_per_second.setter
    def picknplace_cost_per_second(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if value is None:
                self.__picknplace_cost_per_second = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Pick and place cost per second must be a number.")
            elif value < 0:
                raise ConfigurationError("Pick and place cost per second must be nonnegative.")
            else:
                self.__picknplace_cost_per_second = value
                return 0
            
    @property
    def bonding_cost_per_second(self):
        return self.__bonding_cost_per_second
    @bonding_cost_per_second.setter
    def bonding_cost_per_second(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if value is None:
                self.__bonding_cost_per_second = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Bonding cost per second must be a number.")
            elif value < 0:
                raise ConfigurationError("Bonding cost per second must be nonnegative.")
            else:
                self.__bonding_cost_per_second = value
                return 0

    @property
    def tsv_area(self):
        return self.__tsv_area

    @tsv_area.setter
    def tsv_area(self, value):
        if self.static:
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if value is not None and type(value) not in [int, float]:
                raise ConfigurationError("TSV area must be a number or None.")
            elif value is not None and value < 0:
                raise ConfigurationError("TSV area must be nonnegative.")
            else:
                self.__tsv_area = value
                return 0

    @property
    def tsv_yield(self):
        return self.__tsv_yield

    @tsv_yield.setter
    def tsv_yield(self, value):
        if self.static:
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if value is not None and type(value) not in [int, float]:
                raise ConfigurationError("TSV yield must be a number or None.")
            elif value is not None and (value < 0 or value > 1):
                raise ConfigurationError("TSV yield must be between 0 and 1.")
            else:
                self.__tsv_yield = value
                return 0

    @property
    def tsv_pitch(self):
        return self.__tsv_pitch

    @tsv_pitch.setter
    def tsv_pitch(self, value):
        if self.static:
            raise ConfigurationError("Cannot change static assembly process.")
        else:
            if value is not None and type(value) not in [int, float]:
                raise ConfigurationError("TSV pitch must be a number or None.")
            elif value is not None and value < 0:
                raise ConfigurationError("TSV pitch must be nonnegative.")
            else:
                self.__tsv_pitch = value
                return 0
    
    def __init__(self, name = "", materials_cost_per_mm2 = None, bb_cost_per_second = None, picknplace_machine_cost = None,
                 picknplace_machine_lifetime = None, picknplace_machine_uptime = None, picknplace_technician_yearly_cost = None,
                 picknplace_time = None, picknplace_group = None, bonding_machine_cost = None, bonding_machine_lifetime = None,
                 bonding_machine_uptime = None, bonding_technician_yearly_cost = None, bonding_time = None,
                 bonding_group = None, die_separation = None, edge_exclusion = None, max_pad_current_density = None,
                 bonding_pitch = None, alignment_yield = None, bonding_yield = None, dielectric_bond_defect_density = None,
                 tsv_area = None, tsv_yield = None, tsv_pitch = None, static = True) -> None:
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
        self.die_separation = die_separation
        self.edge_exclusion = edge_exclusion
        self.max_pad_current_density = max_pad_current_density
        self.bonding_pitch = bonding_pitch
        self.tsv_area = tsv_area
        self.tsv_yield = tsv_yield
        self.tsv_pitch = tsv_pitch
        self.picknplace_cost_per_second = None
        self.bonding_cost_per_second = None
        self.bonding_yield = bonding_yield
        self.alignment_yield = alignment_yield
        self.dielectric_bond_defect_density = dielectric_bond_defect_density

        if not self.assembly_fully_defined():
            print("Warning: Assembly not fully defined. Setting non-static.")
            print(self)
            self.static = False
        else:
            # Pre-calculate costs per second upon initialization if possible.
            self.compute_picknplace_cost_per_second()
            self.compute_bonding_cost_per_second()

        self.static = static
        
        return

    def __str__(self) -> str:
        return_str = "Assembly Process Name: " + self.name
        return_str += "\n\r\tMaterials Cost Per mm^2: " + str(self.materials_cost_per_mm2)
        return_str += "\n\r\tBlack-Box Cost Per Second: " + str(self.bb_cost_per_second)
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
        return_str += "\n\r\tStatic: " + str(self.static)
        return return_str

    def assembly_fully_defined(self) -> bool:
        # This check needs to account for the possibility of a black-box cost per second, which makes other cost parameters optional.
        cost_params_defined = (self.bb_cost_per_second is not None) or \
                              (self.picknplace_machine_cost is not None and
                               self.picknplace_machine_lifetime is not None and
                               self.picknplace_machine_uptime is not None and
                               self.picknplace_technician_yearly_cost is not None and
                               self.bonding_machine_cost is not None and
                               self.bonding_machine_lifetime is not None and
                               self.bonding_machine_uptime is not None and
                               self.bonding_technician_yearly_cost is not None)

        other_params_defined = (self.name is not None and self.materials_cost_per_mm2 is not None and
                                self.picknplace_time is not None and self.picknplace_group is not None and
                                self.bonding_time is not None and self.bonding_group is not None and
                                self.die_separation is not None and self.edge_exclusion is not None and
                                self.max_pad_current_density is not None and self.bonding_pitch is not None and
                                self.alignment_yield is not None and self.bonding_yield is not None and
                                self.dielectric_bond_defect_density is not None)

        return cost_params_defined and other_params_defined

    def set_static(self) -> int:
        if not self.assembly_fully_defined():
            raise ConfigurationError(f"Attempt to set assembly '{self.name}' static without defining all parameters.\n{self}")
        self.static = True
        return 0

    def get_power_per_pad(self,core_voltage) -> float:
        # Calculate the area of a circular pad
        pad_area = math.pi*(self.bonding_pitch/4)**2
        # Calculate the maximum current per pad based on current density
        current_per_pad = self.max_pad_current_density*pad_area
        # Calculate the power per pad
        power_per_pad = current_per_pad*core_voltage
        return power_per_pad

    def compute_picknplace_time(self, n_chips):
        # Calculate the number of pick-and-place cycles needed
        picknplace_steps = math.ceil(n_chips/self.picknplace_group)
        # Calculate total time
        time = self.picknplace_time*picknplace_steps
        return time
    
    def compute_bonding_time(self, n_chips):
        # Calculate the number of bonding cycles needed
        bonding_steps = math.ceil(n_chips/self.bonding_group)
        # Calculate total time
        time = self.bonding_time*bonding_steps
        return time
    
    def assembly_time(self, n_chips):
        # Total assembly time is the sum of pick-and-place and bonding times
        time = self.compute_picknplace_time(n_chips) + self.compute_bonding_time(n_chips)
        return time

    def compute_picknplace_cost_per_second(self):
        # If a black-box cost is provided, use it directly.
        if self.bb_cost_per_second is not None:
            self.picknplace_cost_per_second = self.bb_cost_per_second
            return self.bb_cost_per_second
        # Otherwise, calculate it from machine and labor costs.
        machine_cost_per_year = self.picknplace_machine_cost/self.picknplace_machine_lifetime
        technician_cost_per_year = self.picknplace_technician_yearly_cost
        picknplace_cost_per_year = machine_cost_per_year + technician_cost_per_year
        # Convert yearly cost to cost per second, accounting for machine uptime.
        picknplace_cost_per_second = picknplace_cost_per_year/(365*24*60*60)*self.picknplace_machine_uptime
        self.picknplace_cost_per_second = picknplace_cost_per_second
        return picknplace_cost_per_second
    
    def compute_bonding_cost_per_second(self):
        # If a black-box cost is provided, use it directly.
        if self.bb_cost_per_second is not None:
            self.bonding_cost_per_second = self.bb_cost_per_second
            return self.bb_cost_per_second
        # Otherwise, calculate it from machine and labor costs.
        machine_cost_per_year = self.bonding_machine_cost/self.bonding_machine_lifetime
        technician_cost_per_year = self.bonding_technician_yearly_cost
        bonding_cost_per_year = machine_cost_per_year + technician_cost_per_year
        # Convert yearly cost to cost per second, accounting for machine uptime.
        bonding_cost_per_second = bonding_cost_per_year/(365*24*60*60)*self.bonding_machine_uptime
        self.bonding_cost_per_second = bonding_cost_per_second
        return bonding_cost_per_second

    # Assembly cost includes cost of machine time and materials cost.
    def assembly_cost(self, n_chips, area):
        # Time-based costs for pick-and-place and bonding
        assembly_cost = (self.picknplace_cost_per_second*self.compute_picknplace_time(n_chips) 
                        + self.bonding_cost_per_second*self.compute_bonding_time(n_chips))
        # Area-based materials cost
        assembly_cost += self.materials_cost_per_mm2*area
        return assembly_cost

    def assembly_yield(self, n_chips, n_bonds, n_tsvs, area):
        # Start with a perfect yield of 1.0
        assem_yield = 1.0
        # Factor in the alignment yield for each chip placed
        assem_yield *= self.alignment_yield**n_chips
        # Factor in the yield for each individual bond
        assem_yield *= self.bonding_yield**n_bonds
        # Factor in the yield for each TSV
        assem_yield *= self.tsv_yield**n_tsvs

        # For processes like hybrid bonding, there is a yield impact from the dielectric bond.
        # This is modeled using a simple defect density model.
        dielectric_bond_area = area
        dielectric_bond_yield = 1/(1 + self.dielectric_bond_defect_density*dielectric_bond_area)
        assem_yield *= dielectric_bond_yield
        
        return assem_yield

# =========================================
# Test Definition Class
# =========================================
# The class has attributes:
#   name: The name of the test process.
#   time_per_test_cycle: The time for a single test cycle in seconds.
#   cost_per_second: The cost of running the test equipment per second.
#   samples_per_input: The number of samples to take per input vector.
#   test_self: Boolean indicating if individual die (self) testing is performed.
#   bb_self_pattern_count: Black-box value for the number of test patterns for self-test.
#   bb_self_scan_chain_length: Black-box value for the scan chain length for self-test.
#   self_defect_coverage: The defect coverage of the self-test process (0 to 1).
#   self_test_reuse: The reuse factor for self-test patterns.
#   self_num_scan_chains: The number of scan chains for self-test.
#   self_num_io_per_scan_chain: The number of I/O pins per scan chain for self-test.
#   self_num_test_io_offset: An offset for the number of test I/O pins for self-test.
#   self_test_failure_dist: The statistical distribution of test failures for self-test.
#   test_assembly: Boolean indicating if assembled package testing is performed.
#   bb_assembly_pattern_count: Black-box value for the number of test patterns for assembly-test.
#   bb_assembly_scan_chain_length: Black-box value for the scan chain length for assembly-test.
#   assembly_defect_coverage: The defect coverage of the assembly-test process (0 to 1).
#   assembly_test_reuse: The reuse factor for assembly-test patterns.
#   assembly_num_scan_chains: The number of scan chains for assembly-test.
#   assembly_num_io_per_scan_chain: The number of I/O pins per scan chain for assembly-test.
#   assembly_num_test_io_offset: An offset for the number of test I/O pins for assembly-test.
#   assembly_test_failure_dist: The statistical distribution of test failures for assembly-test.
#   static: A boolean set true when the test process is defined to prevent further changes.
# =========================================
# The class has the following methods:
#   __init__(...): Initializes the Test object.
#   __str__(): Returns a string representation of the object.
#   test_fully_defined(): Checks if all required attributes are defined.
#   set_static(): Sets the 'static' flag to True to prevent further modifications.
#   compute_self_test_yield(chip): Calculates the yield of the self-test process.
#   compute_self_quality(chip): Calculates the quality (true positives / all positives) of the self-test.
#   compute_assembly_test_yield(chip): Calculates the yield of the assembly-test process.
#   compute_assembly_quality(chip): Calculates the quality of the assembly-test.
#   compute_self_pattern_count(chip): Computes the number of patterns for self-test.
#   compute_self_scan_chain_length_per_mm2(chip): Computes the scan chain length for self-test.
#   compute_self_test_cost(chip): Computes the cost of the self-test.
#   assembly_gate_flop_ratio(chip): Calculates the gate-to-flop ratio for the entire assembly.
#   compute_assembly_pattern_count(chip): Computes the number of patterns for assembly-test.
#   compute_assembly_scan_chain_length_per_mm2(chip): Computes the scan chain length for assembly-test.
#   compute_assembly_test_cost(chip): Computes the cost of the assembly-test.
#   num_test_ios(): Calculates the total number of test I/O pins required.
#   get_atpg_cost(chip): Calculates the Automatic Test Pattern Generation (ATPG) cost.
# =========================================
class Test:
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != str:
                raise ConfigurationError("Test name must be a string.")
            else:
                self.__name = value
                return 0

    @property
    def time_per_test_cycle(self):
        return self.__time_per_test_cycle
    @time_per_test_cycle.setter
    def time_per_test_cycle(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Time per test cycle must be a number.")
            elif value < 0:
                raise ConfigurationError("Time per test cycle must be nonnegative.")
            else:
                self.__time_per_test_cycle = value
                return 0

    @property
    def cost_per_second(self):
        return self.__cost_per_second
    @cost_per_second.setter
    def cost_per_second(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Cost per second must be a number.")
            elif value < 0:
                raise ConfigurationError("Cost per second must be nonnegative.")
            else:
                self.__cost_per_second = value
                return 0

    @property
    def samples_per_input(self):
        return self.__samples_per_input
    @samples_per_input.setter
    def samples_per_input(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != int:
                raise ConfigurationError("Samples per input must be an integer.")
            elif value < 0:
                raise ConfigurationError("Samples per input must be nonnegative.")
            else:
                self.__samples_per_input = value
                return 0

    @property
    def test_self(self):
        return self.__test_self
    @test_self.setter
    def test_self(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != str:
                raise ConfigurationError("Test self must be a string either \"True\" or \"true\".")
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
            raise ConfigurationError("Cannot change static testing.")
        else:
            if value is None or value == "":
                self.__bb_self_pattern_count = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("BB self pattern count must be a number.")
            elif value < 0:
                raise ConfigurationError("BB self pattern count must be nonnegative.")
            else:
                self.__bb_self_pattern_count = value
                return 0
        
    @property
    def bb_self_scan_chain_length(self):
        return self.__bb_self_scan_chain_length
    @bb_self_scan_chain_length.setter
    def bb_self_scan_chain_length(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if value is None or value == "":
                self.__bb_self_scan_chain_length = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("BB self scan chain length must be a number.")
            elif value < 0:
                raise ConfigurationError("BB self scan chain length must be nonnegative.")
            else:
                self.__bb_self_scan_chain_length = value
                return 0
        
    @property
    def self_defect_coverage(self):
        return self.__self_defect_coverage
    @self_defect_coverage.setter
    def self_defect_coverage(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Self defect coverage must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Self defect coverage must be between 0 and 1.")
            else:
                self.__self_defect_coverage = value
                return 0

    @property
    def self_test_reuse(self):
        return self.__self_test_reuse
    @self_test_reuse.setter
    def self_test_reuse(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Self test reuse must be a number.")
            elif value < 0:
                raise ConfigurationError("Self test reuse must be nonnegative.")
            else:
                self.__self_test_reuse = value
                return 0

    @property
    def self_num_scan_chains(self):
        return self.__self_num_scan_chains
    @self_num_scan_chains.setter
    def self_num_scan_chains(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != int:
                raise ConfigurationError("Self num scan chains must be an integer.")
            elif value < 0:
                raise ConfigurationError("Self num scan chains must be nonnegative.")
            else:
                self.__self_num_scan_chains = value
                return 0

    @property
    def self_num_io_per_scan_chain(self):
        return self.__self_num_io_per_scan_chain
    @self_num_io_per_scan_chain.setter
    def self_num_io_per_scan_chain(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != int:
                raise ConfigurationError("Self num IO per scan chain must be an integer.")
            elif value < 0:
                raise ConfigurationError("Self num IO per scan chain must be nonnegative.")
            else:
                self.__self_num_io_per_scan_chain = value
                return 0

    @property
    def self_num_test_io_offset(self):
        return self.__self_num_test_io_offset
    @self_num_test_io_offset.setter
    def self_num_test_io_offset(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != int:
                raise ConfigurationError("Self num test IO offset must be an integer.")
            elif value < 0:
                raise ConfigurationError("Self num test IO offset must be nonnegative.")
            else:
                self.__self_num_test_io_offset = value
                return 0

    @property
    def self_test_failure_dist(self):
        return self.__self_test_failure_dist
    @self_test_failure_dist.setter
    def self_test_failure_dist(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != str:
                raise ConfigurationError("Self test failure dist must be a string.")
            else:
                self.__self_test_failure_dist = value
                return 0
        
    @property
    def test_assembly(self):
        return self.__test_assembly
    @test_assembly.setter
    def test_assembly(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != str:
                raise ConfigurationError("Test assembly must be a string either \"True\" or \"true\".")
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
            raise ConfigurationError("Cannot change static testing.")
        else:
            if value is None or value == "":
                self.__bb_assembly_pattern_count = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("BB assembly pattern count must be a number.")
            elif value < 0:
                raise ConfigurationError("BB assembly pattern count must be nonnegative.")
            else:
                self.__bb_assembly_pattern_count = value
                return 0
        
    @property
    def bb_assembly_scan_chain_length(self):
        return self.__bb_assembly_scan_chain_length
    @bb_assembly_scan_chain_length.setter
    def bb_assembly_scan_chain_length(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if value is None or value == "":
                self.__bb_assembly_scan_chain_length = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("BB assembly scan chain length must be a number.")
            elif value < 0:
                raise ConfigurationError("BB assembly scan chain length must be nonnegative.")
            else:
                self.__bb_assembly_scan_chain_length = value
                return 0
        
    @property
    def assembly_defect_coverage(self):
        return self.__assembly_defect_coverage
    @assembly_defect_coverage.setter
    def assembly_defect_coverage(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Assembly defect coverage must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Assembly defect coverage must be between 0 and 1.")
            else:
                self.__assembly_defect_coverage = value
                return 0
        
    @property
    def assembly_test_reuse(self):
        return self.__assembly_test_reuse
    @assembly_test_reuse.setter
    def assembly_test_reuse(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Assembly test reuse must be a number.")
            elif value < 0:
                raise ConfigurationError("Assembly test reuse must be nonnegative.")
            else:
                self.__assembly_test_reuse = value
                return 0
        
    @property
    def assembly_num_scan_chains(self):
        return self.__assembly_num_scan_chains
    @assembly_num_scan_chains.setter
    def assembly_num_scan_chains(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != int:
                raise ConfigurationError("Assembly num scan chains must be an integer.")
            elif value < 0:
                raise ConfigurationError("Assembly num scan chains must be nonnegative.")
            else:
                self.__assembly_num_scan_chains = value
                return 0
        
    @property
    def assembly_num_io_per_scan_chain(self):
        return self.__assembly_num_io_per_scan_chain
    @assembly_num_io_per_scan_chain.setter
    def assembly_num_io_per_scan_chain(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != int:
                raise ConfigurationError("Assembly num IO per scan chain must be an integer.")
            elif value < 0:
                raise ConfigurationError("Assembly num IO per scan chain must be nonnegative.")
            else:
                self.__assembly_num_io_per_scan_chain = value
                return 0
        
    @property
    def assembly_num_test_io_offset(self):
        return self.__assembly_num_test_io_offset
    @assembly_num_test_io_offset.setter
    def assembly_num_test_io_offset(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != int:
                raise ConfigurationError("Assembly num test IO offset must be an integer.")
            elif value < 0:
                raise ConfigurationError("Assembly num test IO offset must be nonnegative.")
            else:
                self.__assembly_num_test_io_offset = value
                return 0

    @property
    def assembly_test_failure_dist(self):
        return self.__assembly_test_failure_dist
    @assembly_test_failure_dist.setter
    def assembly_test_failure_dist(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static testing.")
        else:
            if type(value) != str:
                raise ConfigurationError("Assembly test failure dist must be a string.")
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
        self.cost_per_second = cost_per_second
        self.samples_per_input = samples_per_input

        # Self-test related parameters
        self.test_self = test_self
        self.bb_self_pattern_count = bb_self_pattern_count
        self.bb_self_scan_chain_length = bb_self_scan_chain_length
        self.self_defect_coverage = self_defect_coverage
        self.self_test_reuse = self_test_reuse
        self.self_num_scan_chains = self_num_scan_chains
        self.self_num_io_per_scan_chain = self_num_io_per_scan_chain
        self.self_num_test_io_offset = self_num_test_io_offset
        self.self_test_failure_dist = self_test_failure_dist

        # Assembly-test related parameters
        self.test_assembly = test_assembly
        self.bb_assembly_pattern_count = bb_assembly_pattern_count
        self.bb_assembly_scan_chain_length = bb_assembly_scan_chain_length
        self.assembly_defect_coverage = assembly_defect_coverage     
        self.assembly_test_reuse = assembly_test_reuse
        self.assembly_num_scan_chains = assembly_num_scan_chains
        self.assembly_num_io_per_scan_chain = assembly_num_io_per_scan_chain
        self.assembly_num_test_io_offset = assembly_num_test_io_offset
        self.assembly_test_failure_dist = assembly_test_failure_dist
        
        self.static = static
        if not self.test_fully_defined():
            print(f"Warning: Test '{self.name}' not fully defined. Setting non-static.")
            self.static = False
        return
        
    def set_static(self) -> int:
        if not self.test_fully_defined():
            raise ConfigurationError(f"Attempt to set test '{self.name}' static without defining all parameters.\n{self}")
        else:
            self.static = True
            return 0

    def test_fully_defined(self) -> bool:
        # A test is fully defined if its core parameters and the parameters for any active test stages (self or assembly) are defined.
        core_defined = (self.name is not None and self.time_per_test_cycle is not None and
                        self.cost_per_second is not None and self.samples_per_input is not None)
        
        self_test_defined = (not self.test_self) or \
                            (self.self_defect_coverage is not None and
                             self.self_test_reuse is not None and
                             self.self_num_scan_chains is not None and
                             self.self_num_io_per_scan_chain is not None and
                             self.self_num_test_io_offset is not None and
                             self.self_test_failure_dist is not None)

        assembly_test_defined = (not self.test_assembly) or \
                                (self.assembly_defect_coverage is not None and
                                 self.assembly_test_reuse is not None and
                                 self.assembly_num_scan_chains is not None and
                                 self.assembly_num_io_per_scan_chain is not None and
                                 self.assembly_num_test_io_offset is not None and
                                 self.assembly_test_failure_dist is not None)
        
        return core_defined and self_test_defined and assembly_test_defined

    def __str__(self) -> str:
        return_str = f"Test: {self.name}\n"
        return_str += f"\tTime per Test Cycle: {self.time_per_test_cycle}\n"
        return_str += f"\tCost per Second: {self.cost_per_second}\n"
        return_str += f"\tSamples per Input: {self.samples_per_input}\n"
        return_str += f"\t--- Self Test ---\n"
        return_str += f"\tTest Self: {self.test_self}\n"
        if self.test_self:
            return_str += f"\t\tBB Self Pattern Count: {self.bb_self_pattern_count}\n"
            return_str += f"\t\tBB Self Scan Chain Length: {self.bb_self_scan_chain_length}\n"
            return_str += f"\t\tSelf Defect Coverage: {self.self_defect_coverage}\n"
            return_str += f"\t\tSelf Test Reuse: {self.self_test_reuse}\n"
            return_str += f"\t\tSelf Num Scan Chains: {self.self_num_scan_chains}\n"
            return_str += f"\t\tSelf Num IO per Scan Chain: {self.self_num_io_per_scan_chain}\n"
            return_str += f"\t\tSelf Num Test IO Offset: {self.self_num_test_io_offset}\n"
            return_str += f"\t\tSelf Test Failure Dist: {self.self_test_failure_dist}\n"
        return_str += f"\t--- Assembly Test ---\n"
        return_str += f"\tTest Assembly: {self.test_assembly}\n"
        if self.test_assembly:
            return_str += f"\t\tBB Assembly Pattern Count: {self.bb_assembly_pattern_count}\n"
            return_str += f"\t\tBB Assembly Scan Chain Length: {self.bb_assembly_scan_chain_length}\n"
            return_str += f"\t\tAssembly Defect Coverage: {self.assembly_defect_coverage}\n"
            return_str += f"\t\tAssembly Test Reuse: {self.assembly_test_reuse}\n"
            return_str += f"\t\tAssembly Num Scan Chains: {self.assembly_num_scan_chains}\n"
            return_str += f"\t\tAssembly Num IO per Scan Chain: {self.assembly_num_io_per_scan_chain}\n"
            return_str += f"\t\tAssembly Num Test IO Offset: {self.assembly_num_test_io_offset}\n"
            return_str += f"\t\tAssembly Test Failure Dist: {self.assembly_test_failure_dist}\n"
        return_str += f"\tStatic: {self.static}\n"
        return return_str

    # This is the yield based on number of chips that pass test.
    def compute_self_test_yield(self, chip) -> float:
        if self.test_self == True:
            true_yield = chip.self_true_yield
            # Test yield is the probability that a chip passes the test.
            # It's 1 minus the probability that a truly bad chip fails the test (which is covered by defect coverage).
            test_yield = 1-(1-true_yield)*self.self_defect_coverage
        else:
            # If no self-test is performed, the test yield is effectively 100% (no chips are screened out).
            test_yield = 1.0
        return test_yield

    def compute_self_quality(self, chip) -> float:
        test_yield = chip.self_test_yield
        true_yield = chip.self_true_yield
        # Quality is the ratio of truly good chips to chips that passed the test.
        quality = true_yield/test_yield
        if quality > 1.0: # Account for rounding errors
            quality = 1.0
        return quality

    def compute_assembly_test_yield(self, chip) -> float:
        if self.test_assembly == True:
            assembly_true_yield = chip.chip_true_yield
            assembly_test_yield = 1.0-(1.0-assembly_true_yield)*self.assembly_defect_coverage
        else:
            # If no assembly test, no parts are screened out at this stage.
            assembly_test_yield = 1.0
        return assembly_test_yield

    def compute_assembly_quality(self, chip) -> float:
        assembly_true_yield = chip.chip_true_yield
        assembly_test_yield = chip.chip_test_yield
        # Quality is the ratio of truly good assemblies to assemblies that passed the test.
        assembly_quality = assembly_true_yield/assembly_test_yield
        return assembly_quality

    def compute_self_pattern_count(self, chip) -> float:
        # Use black-box value if provided.
        if self.bb_self_pattern_count is not None and self.bb_self_pattern_count != "":
            return self.bb_self_pattern_count
        else:
            # Otherwise, estimate based on logic depth, which is approximated from the gate-to-flop ratio.
            # TODO: Evaluate this model and determine accuracy. This is a heuristic.
            wires_per_flop = 3*chip.gate_flop_ratio/2
            self_pattern_count = 2**wires_per_flop
            return self_pattern_count

    def compute_self_scan_chain_length_per_mm2(self, chip) -> float:
        # Use black-box value if provided.
        if self.bb_self_scan_chain_length is not None and self.bb_self_scan_chain_length != "":
            return self.bb_self_scan_chain_length
        else:
            # Otherwise, estimate scan chain length as the number of flops, normalized by area and number of chains.
            flops_per_mm2 = chip.get_self_gates_per_mm2()/chip.gate_flop_ratio
            self_scan_chain_length = flops_per_mm2/self.self_num_scan_chains
            return self_scan_chain_length

    def compute_self_test_cost(self, chip) -> float:
        if (self.test_self == False):
            return 0.0
        else:
            # Test cost is a function of test time (driven by patterns and scan length) and the cost of the tester.
            test_cost = chip.core_area * self.time_per_test_cycle * self.cost_per_second * \
                        (self.compute_self_pattern_count(chip)+self.samples_per_input) * \
                        self.compute_self_scan_chain_length_per_mm2(chip)
            
            # The derating factor based on failure distribution is currently ignored.
            # This could be used to model scenarios where test time varies.
            derating_factor = 1.0
            test_cost = derating_factor*test_cost
        return test_cost

    def assembly_gate_flop_ratio(self, chip) -> float:
        # Calculate a weighted average of the gate-to-flop ratio across the entire assembly.
        gate_flop_area_product = chip.gate_flop_ratio*chip.core_area
        total_area = chip.core_area
        for c in chip.face_chips:
            total_area += c.core_area
            gate_flop_area_product += c.gate_flop_ratio*c.core_area
        for c in chip.back_chips:
            total_area += c.core_area
            gate_flop_area_product += c.gate_flop_ratio*c.core_area
        # for c in chip.chips:
        #     total_area += c.core_area
        #     gate_flop_area_product += c.gate_flop_ratio*c.core_area
        
        if total_area == 0:
            return 0
        
        avg_gate_flop_ratio = gate_flop_area_product/total_area
        return avg_gate_flop_ratio

    def compute_assembly_pattern_count(self,chip) -> float:
        # Use black-box value if provided.
        if self.bb_assembly_pattern_count is not None and self.bb_assembly_pattern_count != "":
            return self.bb_assembly_pattern_count
        else:
            # Estimate based on the average gate-to-flop ratio of the entire assembly.
            # TODO: Evaluate this model and determine accuracy. This is a heuristic.
            gate_flop_ratio = self.assembly_gate_flop_ratio(chip)
            wires_per_flop = 3*gate_flop_ratio/2
            assembly_pattern_count = 2**wires_per_flop
            return assembly_pattern_count

    def compute_assembly_scan_chain_length_per_mm2(self, chip) -> float:
        # Use black-box value if provided.
        if self.bb_assembly_scan_chain_length is not None and self.bb_assembly_scan_chain_length != "":
            return self.bb_assembly_scan_chain_length
        else:
            # Estimate based on the flops in the entire assembly.
            assembly_scan_chain_length = chip.get_assembly_gates_per_mm2()/self.assembly_gate_flop_ratio(chip)
            assembly_scan_chain_length = assembly_scan_chain_length/self.assembly_num_scan_chains
            return assembly_scan_chain_length

    def compute_assembly_test_cost(self, chip) -> float:
        if (self.test_assembly == False):
            return 0.0
        else:
            # Calculate the total area of the assembly.
            area = chip.core_area
            for c in chip.face_chips:
                area += c.core_area
            for c in chip.back_chips:
                area += c.core_area
            # chips = chip.chips
            # for c in chips:
            #     area += c.core_area

            # Calculate the cost of the assembly test.
            test_cost = area * self.time_per_test_cycle * self.cost_per_second * \
                        self.compute_assembly_pattern_count(chip) * \
                        self.compute_assembly_scan_chain_length_per_mm2(chip)

            # Derating factor is currently ignored.
            derating_factor = 1.0
            test_cost = derating_factor*test_cost*self.samples_per_input 
        return test_cost

    def num_test_ios(self) -> float:
        # Calculate the total number of I/O pins required for testing.
        num_ios = 0
        if self.test_self == True:
            num_ios = self.self_num_io_per_scan_chain*self.self_num_scan_chains + self.self_num_test_io_offset
        if self.test_assembly == True:
            num_ios += self.assembly_num_io_per_scan_chain*self.assembly_num_scan_chains + self.assembly_num_test_io_offset
        return num_ios

    def get_atpg_cost(self, chip) -> float:
        # Constant for cost of ATPG effort.
        K = 1.0 # This is a placeholder constant.
        # ATPG cost is modeled as proportional to the number of gates and inversely proportional to the reuse factor.
        atpg_effort = 0.0
        if self.test_self == True:
            atpg_effort = chip.gate_flop_ratio*chip.core_area*chip.get_self_gates_per_mm2()/self.self_test_reuse
        if self.test_assembly == True:
            area = chip.core_area
            for c in chip.face_chips:
                area += c.core_area
            for c in chip.back_chips:
                area += c.core_area
            atpg_effort += chip.gate_flop_ratio*area*chip.get_assembly_gates_per_mm2()/self.assembly_test_reuse
        atpg_cost = atpg_effort*K
        # NOTE: ATPG cost calculation is currently disabled by returning 0.0.
        return 0.0

# =========================================
# Chip Class
# =========================================
# The class has attributes:
#   name: The name of the chip.
#   core_area: The area of the core in mm^2.
#   aspect_ratio: The aspect ratio (x/y) of the chip.
#   x_location, y_location: The coordinates of the chip in a larger assembly.
#   orientation: Orientation has two valid values: "face-up" and "face-down".
#                These are relative orientations to the parent Chip.
#                "face-down" means the Chip has the metal layer side facing the parent Chip.
#                "face-up" means the Chip has the silicon side facing the parent Chip.
#                orientation of the root Chip will determine the orientation of the entire assembly for display purposes.
#   stack_side: Stack side has two valid values: "face" and "back".
#                This indicates which side of the parent Chip the Chip is stacked on.
#   bb_area, bb_cost, bb_quality, bb_power: Black-box override values.
#   fraction_memory, fraction_logic, fraction_analog: The proportions of different circuit types.
#   gate_flop_ratio: The ratio of logic gates to flip-flops.
#   reticle_share: The fraction of the reticle cost this chip is responsible for.
#   buried: Boolean indicating if the chip is buried (e.g., a bridge die).
#   chips: A list of Chip objects that are stacked on this chip.
#   assembly_process: The Assembly object used to assemble this chip.
#   test_process: The Test object used for testing.
#   stackup: A list of Layer objects defining the chip's vertical structure.
#   wafer_process: The WaferProcess object for this chip's fabrication.
#   core_voltage: The operating voltage of the chip core.
#   power: The intrinsic power consumption of the chip core in Watts.
#   quantity: The number of chips to be produced.
#   static: A boolean to lock the object from further changes.
#   parent_chip: A reference to the parent Chip object in a hierarchy.
#   (and many more calculated attributes like cost, yield, quality, etc.)
# =========================================
# The class has the following methods:
#   __init__(...): Initializes the Chip object from file or etree, recursively building sub-chips.
#   (Numerous @property and @setter methods for all attributes)
#   set_static(): Locks the chip object.
#   compute_stack_power(): Calculates the power consumed by all chips stacked on this one.
#   find_process(...), find_wafer_process(...), etc.: Helper methods to find definition objects.
#   build_stackup(...): Constructs the layer stackup from a string definition.
#   print_description(): Dumps values of all parameters for inspection.
#   (and many more get/set/compute methods for area, cost, yield, power, etc.)
# =========================================
class Chip:
    @property
    def name(self):
        return self.__name
    @name.setter
    def name(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) != str:
                raise ConfigurationError("Chip name must be a string.")
            else:
                self.__name = value
                return 0
        
    @property
    def core_area(self):
        return self.__core_area
    @core_area.setter
    def core_area(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Core area must be a number.")
            elif value < 0:
                raise ConfigurationError("Core area must be nonnegative.")
            else:
                self.__core_area = value
                return 0

    @property
    def aspect_ratio(self):
        return self.__aspect_ratio
    @aspect_ratio.setter
    def aspect_ratio(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Aspect ratio must be a number.")
            elif value < 0:
                raise ConfigurationError("Aspect ratio must be nonnegative.")
            else:
                self.__aspect_ratio = value
                return 0

    @property
    def x_location(self):
        return self.__x_location
    @x_location.setter
    def x_location(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if value is None or value == "":
                self.__x_location = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("X location must be a number.")
            else:
                self.__x_location = value
                return 0
        
    @property
    def y_location(self):
        return self.__y_location
    @y_location.setter
    def y_location(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if value is None or value == "":
                self.__y_location = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Y location must be a number.")
            else:
                self.__y_location = value
                return 0
    
    @property
    def orientation(self):
        return self.__orientation
    @orientation.setter
    def orientation(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) != str:
                raise ConfigurationError("Orientation must be a string.")
            value_lower = value.lower()
            if value_lower not in ["face-up", "face-down"]:
                raise ConfigurationError("Orientation must be either 'face-up' or 'face-down'.")
            else:
                self.__orientation = value_lower
                return 0

    @property
    def stack_side(self):
        return self.__stack_side
    @stack_side.setter
    def stack_side(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) != str:
                raise ConfigurationError("Stack side must be a string.")
            value_lower = value.lower()
            if value_lower not in ["face", "back"]:
                raise ConfigurationError("Stack side must be either 'face' or 'back'.")
            else:
                self.__stack_side = value_lower
                return 0

    @property
    def bb_area(self):
        return self.__bb_area
    @bb_area.setter
    def bb_area(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if value is None or value == "":
                self.__bb_area = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("BB area must be a number.")
            elif value < 0:
                raise ConfigurationError("BB area must be nonnegative.")
            else:
                self.__bb_area = value
                return 0

    @property
    def bb_cost(self):
        return self.__bb_cost
    @bb_cost.setter
    def bb_cost(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if value is None or value == "":
                self.__bb_cost = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("BB cost must be a number.")
            elif value < 0:
                raise ConfigurationError("BB cost must be nonnegative.")
            else:
                self.__bb_cost = value
                return 0

    @property
    def bb_quality(self):
        return self.__bb_quality
    @bb_quality.setter
    def bb_quality(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if value is None or value == "":
                self.__bb_quality = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("BB quality must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("BB quality must be between 0 and 1.")
            else:
                self.__bb_quality = value
                return 0
        
    @property
    def bb_power(self):
        return self.__bb_power
    @bb_power.setter
    def bb_power(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if value is None or value == "":
                self.__bb_power = None
                return 0
            elif type(value) not in [int, float, np.float64]:
                raise ConfigurationError("BB power must be a number.")
            elif value < 0:
                raise ConfigurationError("BB power must be nonnegative.")
            else:
                self.__bb_power = value
                return 0
        
    @property
    def fraction_memory(self):
        return self.__fraction_memory
    @fraction_memory.setter
    def fraction_memory(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Fraction memory must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Fraction memory must be between 0 and 1.")
            else:
                self.__fraction_memory = value
                return 0
        
    @property
    def fraction_logic(self):
        return self.__fraction_logic
    @fraction_logic.setter
    def fraction_logic(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Fraction logic must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Fraction logic must be between 0 and 1.")
            else:
                self.__fraction_logic = value
                return 0
        
    @property
    def fraction_analog(self):
        return self.__fraction_analog
    @fraction_analog.setter
    def fraction_analog(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Fraction analog must be a number.")
            elif value < 0 or value > 1:
                raise ConfigurationError("Fraction analog must be between 0 and 1.")
            else:
                self.__fraction_analog = value
                return 0
        
    @property
    def gate_flop_ratio(self):
        return self.__gate_flop_ratio
    @gate_flop_ratio.setter
    def gate_flop_ratio(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Gate flop ratio must be a number.")
            elif value < 0:
                raise ConfigurationError("Gate flop ratio must be nonnegative.")
            else:
                self.__gate_flop_ratio = value
                return 0
        
    @property
    def reticle_share(self):
        return self.__reticle_share
    @reticle_share.setter
    def reticle_share(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Reticle share must be a number.")
            elif value < 0:
                raise ConfigurationError("Reticle share must be nonnegative.")
            else:
                self.__reticle_share = value
                return 0
        
    @property
    def buried(self):
        return self.__buried
    @buried.setter
    def buried(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) != str:
                raise ConfigurationError("Buried must be a string with value \"True\" or \"true\".")
            elif value.lower() == "true":
                self.__buried = True
                return 0
            else:
                self.__buried = False
                return 0

    @property
    def face_chips(self):
        return self.__face_chips
    @face_chips.setter
    def face_chips(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if not isinstance(value, list):
                raise ConfigurationError("Face chips must be a list of Chip objects.")
            for c in value:
                if not isinstance(c, Chip):
                    raise ConfigurationError("All face chips must be Chip objects.")
            self.__face_chips = value
            return 0
    
    @property
    def back_chips(self):
        return self.__back_chips
    @back_chips.setter
    def back_chips(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if not isinstance(value, list):
                raise ConfigurationError("Back chips must be a list of Chip objects.")
            for c in value:
                if not isinstance(c, Chip):
                    raise ConfigurationError("All back chips must be Chip objects.")
            self.__back_chips = value
            return 0
        
    # @property
    # def chips(self):
    #     return self.__chips
    # @chips.setter
    # def chips(self, value):
    #     if (self.static):
    #         raise ConfigurationError("Cannot change static chip.")
    #     else:
    #         self.__chips = value
    #         return 0
        
    @property
    def assembly_process(self):
        return self.__assembly_process
    @assembly_process.setter
    def assembly_process(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            self.__assembly_process = value
            return 0
        
    @property
    def test_process(self):
        return self.__test_process
    @test_process.setter
    def test_process(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            self.__test_process = value
            return 0

    @property
    def stackup(self):
        return self.__stackup
    @stackup.setter
    def stackup(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            self.__stackup = value
            return 0
        
    @property
    def wafer_process(self):
        return self.__wafer_process
    @wafer_process.setter
    def wafer_process(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            self.__wafer_process = value
            return 0

    @property
    def core_voltage(self):
        return self.__core_voltage
    @core_voltage.setter
    def core_voltage(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Core voltage must be a number.")
            elif value < 0:
                raise ConfigurationError("Core voltage must be nonnegative.")
            else:
                self.__core_voltage = value
                return 0
        
    @property
    def power(self):
        return self.__power
    @power.setter
    def power(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) not in [int, float, np.float64]:
                raise ConfigurationError("Power must be a number.")
            elif value < 0:
                raise ConfigurationError("Power must be nonnegative.")
            else:
                self.__power = value
                return 0
        
    @property
    def quantity(self):
        return self.__quantity
    @quantity.setter
    def quantity(self, value):
        if (self.static):
            raise ConfigurationError("Cannot change static chip.")
        else:
            if type(value) != int:
                raise ConfigurationError("Quantity must be an integer.")
            elif value < 0:
                raise ConfigurationError("Quantity must be nonnegative.")
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
    
    @property
    def parent_chip(self): return self.__parent_chip
    @parent_chip.setter
    def parent_chip(self, value):
        if not isinstance(value, Chip) and value is not None:
            raise ConfigurationError("parent_chip must be a Chip object or None.")
        self.__parent_chip = value
    
    @property
    def self_cost(self): return self.__self_cost
    @self_cost.setter
    def self_cost(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Self cost must be a number.")
        if value < 0:
            raise ConfigurationError("Self cost must be non-negative.")
        self.__self_cost = value

    @property
    def cost(self): return self.__cost
    @cost.setter
    def cost(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Cost must be a number.")
        if value < 0:
            raise ConfigurationError("Cost must be non-negative.")
        self.__cost = value

    @property
    def self_true_yield(self): return self.__self_true_yield
    @self_true_yield.setter
    def self_true_yield(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Yield must be a number.")
        if not (0.0 <= value <= 1.0):
            raise ConfigurationError("Yield must be between 0.0 and 1.0.")
        self.__self_true_yield = value

    @property
    def chip_true_yield(self): return self.__chip_true_yield
    @chip_true_yield.setter
    def chip_true_yield(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Yield must be a number.")
        if not (0.0 <= value <= 1.0):
            raise ConfigurationError("Yield must be between 0.0 and 1.0.")
        self.__chip_true_yield = value

    @property
    def self_test_yield(self): return self.__self_test_yield
    @self_test_yield.setter
    def self_test_yield(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Yield must be a number.")
        if not (0.0 <= value <= 1.0):
            raise ConfigurationError("Yield must be between 0.0 and 1.0.")
        self.__self_test_yield = value

    @property
    def chip_test_yield(self): return self.__chip_test_yield
    @chip_test_yield.setter
    def chip_test_yield(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Yield must be a number.")
        if not (0.0 <= value <= 1.0):
            raise ConfigurationError("Yield must be between 0.0 and 1.0.")
        self.__chip_test_yield = value

    @property
    def self_quality(self): return self.__self_quality
    @self_quality.setter
    def self_quality(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Quality must be a number.")
        if value < 0:
            raise ConfigurationError("Quality must be non-negative.")
        self.__self_quality = value

    @property
    def quality(self): return self.__quality
    @quality.setter
    def quality(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Quality must be a number.")
        if value < 0:
            raise ConfigurationError("Quality must be non-negative.")
        self.__quality = value
    
    @property
    def stack_power(self): return self.__stack_power
    @stack_power.setter
    def stack_power(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Power must be a number.")
        if value < 0:
            raise ConfigurationError("Power must be non-negative.")
        self.__stack_power = value
        
    @property
    def io_power(self): return self.__io_power
    @io_power.setter
    def io_power(self, value):
        if type(value) not in [int, float, np.float64]:
            print(type(value))
            raise ConfigurationError("Power must be a number.")
        if value < 0:
            raise ConfigurationError("Power must be non-negative.")
        self.__io_power = value

    @property
    def total_power(self): return self.__total_power
    @total_power.setter
    def total_power(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Power must be a number.")
        if value < 0:
            raise ConfigurationError("Power must be non-negative.")
        self.__total_power = value

    @property
    def area(self): return self.__area
    @area.setter
    def area(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("Area must be a number.")
        if value < 0:
            raise ConfigurationError("Area must be non-negative.")
        self.__area = value
        
    @property
    def nre_design_cost(self): return self.__nre_design_cost
    @nre_design_cost.setter
    def nre_design_cost(self, value):
        if type(value) not in [int, float, np.float64]:
            raise ConfigurationError("NRE cost must be a number.")
        if value < 0:
            raise ConfigurationError("NRE cost must be non-negative.")
        self.__nre_design_cost = value

    # ===== Initialization Functions =====
    # "etree" is an element tree built from the system definition xml file.
    def __init__(self, filename = None, etree = None, parent_chip = None, wafer_process_list = None, assembly_process_list = None, test_process_list = None, layers = None, ios = None, adjacency_matrix_definitions = None, average_bandwidth_utilization = None, block_names = None, static = False) -> None:
        self.static = False
        # If the critical definition lists are not provided, throw an error and exit.
        if wafer_process_list is None:
            raise ConfigurationError("wafer_process_list is None.")
        if assembly_process_list is None:
            raise ConfigurationError("assembly_process_list is None.")
        if test_process_list is None:
            raise ConfigurationError("test_process_list is None.")
        if layers is None:
            raise ConfigurationError("layers is None.")
        if ios is None:
            raise ConfigurationError("ios is None.")
        if adjacency_matrix_definitions is None:
            raise ConfigurationError("adjacency_matrix_definitions is None.")
        if average_bandwidth_utilization is None:
            raise ConfigurationError("average_bandwidth_utilization is None.")
        if block_names is None:
            raise ConfigurationError("block_names is None.")

        root = {}
        # If the filename is given and the etree is not, read the file and build the etree.
        if filename is not None and filename != "" and etree is None:
            tree = ET.parse(filename)
            root = tree.getroot()
        # If the etree is given, use it.
        elif etree is not None:
            root = etree
        else:
            raise ConfigurationError("Invalid chip definition. A filename or etree must be provided.")

        self.parent_chip = parent_chip
        attributes = root.attrib

        # The copy_from feature is not fully implemented and should be used with caution.
        copy_from = attributes.get("copy_from")
        if copy_from is not None:
            print("Warning: The 'copy_from' feature is experimental.")
            # Need to search the Chip list using the parent_chip pointer.
            if parent_chip:
                for chip_object in parent_chip.face_chips:
                    if chip_object.name == copy_from:
                        # Deep copy the found chip and re-assign self. This is tricky in Python.
                        # A better implementation might be a factory function.
                        self = copy.deepcopy(chip_object)
                        break
                for chip_object in parent_chip.back_chips:
                    if chip_object.name == copy_from:
                        # Deep copy the found chip and re-assign self. This is tricky in Python.
                        # A better implementation might be a factory function.
                        self = copy.deepcopy(chip_object)
                        break
                # for chip_object in parent_chip.chips:
                #     if chip_object.name == copy_from:
                #         # Deep copy the found chip and re-assign self. This is tricky in Python.
                #         # A better implementation might be a factory function.
                #         self = copy.deepcopy(chip_object)
                #         break
        else:
            # The following are the class parameter objects. The find_* functions match the correct object with the name given in the chip definition.
            self.wafer_process = self.find_wafer_process(attributes["wafer_process"], wafer_process_list)
            self.assembly_process = self.find_assembly_process(attributes["assembly_process"], assembly_process_list)
            self.test_process = self.find_test_process(attributes["test_process"], test_process_list)
            self.stackup = self.build_stackup(attributes["stackup"], layers)

            # Recursively handle the chips that are stacked on this chip.
            # self.chips = []
            self.face_chips = []
            self.back_chips = []
            for chip_def in root:
                if "chip" in chip_def.tag:
                    if chip_def.attrib.get("stack_side") == "face":
                        self.face_chips.append(Chip(filename=None, etree=chip_def, parent_chip=self, wafer_process_list=wafer_process_list, assembly_process_list=assembly_process_list, test_process_list=test_process_list, layers=layers, ios=ios, adjacency_matrix_definitions=adjacency_matrix_definitions, average_bandwidth_utilization=average_bandwidth_utilization, block_names=block_names, static=static))
                    elif chip_def.attrib.get("stack_side") == "back":
                        self.back_chips.append(Chip(filename=None, etree=chip_def, parent_chip=self, wafer_process_list=wafer_process_list, assembly_process_list=assembly_process_list, test_process_list=test_process_list, layers=layers, ios=ios, adjacency_matrix_definitions=adjacency_matrix_definitions, average_bandwidth_utilization=average_bandwidth_utilization, block_names=block_names, static=static))
                    # self.chips.append(Chip(filename=None, etree=chip_def, parent_chip=self, wafer_process_list=wafer_process_list, assembly_process_list=assembly_process_list, test_process_list=test_process_list, layers=layers, ios=ios, adjacency_matrix_definitions=adjacency_matrix_definitions, average_bandwidth_utilization=average_bandwidth_utilization, block_names=block_names, static=static))

            # Set Black-Box Parameters
            self.bb_area = float(attributes["bb_area"]) if attributes.get("bb_area") else None
            self.bb_cost = float(attributes["bb_cost"]) if attributes.get("bb_cost") else None
            self.bb_quality = float(attributes["bb_quality"]) if attributes.get("bb_quality") else None
            self.bb_power = float(attributes["bb_power"]) if attributes.get("bb_power") else None
            self.aspect_ratio = float(attributes.get("aspect_ratio", 1.0)) if attributes.get("aspect_ratio", 1.0) else 1.0
            self.x_location = float(attributes["x_location"]) if attributes.get("x_location") else None
            self.y_location = float(attributes["y_location"]) if attributes.get("y_location") else None
            self.orientation = attributes["orientation"] if attributes.get("orientation") else "face-up"
            self.stack_side = attributes["stack_side"] if attributes.get("stack_side") else "face"

            # Chip name should match the name in the netlist file.
            self.name = attributes["name"]
            self.core_area = float(attributes["core_area"])
            self.fraction_memory = float(attributes["fraction_memory"])
            self.fraction_logic = float(attributes["fraction_logic"])
            self.fraction_analog = float(attributes["fraction_analog"])
            self.gate_flop_ratio = float(attributes["gate_flop_ratio"])
            self.reticle_share = float(attributes.get("reticle_share", 1.0))
            self.quantity = int(attributes["quantity"])
            self.buried = attributes["buried"] if attributes.get("buried") else False
            self.power = float(attributes["power"])
            self.core_voltage = float(attributes["core_voltage"])
            
            # Store references to global definition lists
            self.global_adjacency_matrix = adjacency_matrix_definitions
            self.average_bandwidth_utilization = average_bandwidth_utilization
            self.block_names = block_names
            self.io_list = ios

            # Perform all calculations after initial parameters are set
            self.__perform_calculations()

            # Check routing congestion below the chip by checking the routing tracks available on the parent chip.
            if self.parent_chip is not None:
                num_tracks = 0
                for layer in self.parent_chip.stackup:
                    num_tracks += layer.compute_number_of_routing_tracks(self.area, self.aspect_ratio)

                signal_pads, signal_with_reach_count = self.get_signal_count(self.get_chip_list())
                escape_wires = signal_pads + self.test_process.num_test_ios()
                if num_tracks < escape_wires:
                    print("Warning: The number of excape routing tracks available on the parent chip is less than the number of routing tracks required by " + str(self.name) + ".")
                # else:
                #     print("Passed routing congestion check for " + str(self.name) + ".")
            
            # If the chip is defined as static, it should not be changed.
            if static:
                self.set_static()

        return

    def set_static(self):
        self.__static = True
        return 0    

    def __perform_calculations(self):
        """Helper function to run all cost, yield, power, and area calculations."""
        # This function centralizes the calculation calls that happen after initialization.
        #self.set_stack_power(self.compute_stack_power())
        self.stack_power = self.compute_stack_power()
        self.io_power = self.get_signal_power(self.get_chip_list())

        if self.bb_power is None:
            self.total_power = self.power + self.io_power + self.stack_power
        else:
            self.total_power = self.bb_power + self.stack_power

        self.nre_design_cost = self.compute_nre_design_cost()
        self.area = self.compute_area()
        self.self_true_yield = self.compute_layer_aware_yield()
        self.self_test_yield = self.test_process.compute_self_test_yield(self)
        
        if self.bb_quality is None:
            self.self_quality = self.test_process.compute_self_quality(self)
        else:
            self.self_quality = self.bb_quality

        self.chip_true_yield = self.compute_chip_yield()
        self.chip_test_yield = self.test_process.compute_assembly_test_yield(self)
        self.quality = self.test_process.compute_assembly_quality(self)
        self.self_cost = self.compute_self_cost()
        self.cost = self.compute_cost()
    
    def face_stack_power(self) -> float:
        """Calculates the power consumed by all chips stacked on the face of this chip."""
        face_stack_power = 0.0
        for chip in self.face_chips:
            face_stack_power += chip.total_power
        return face_stack_power

    def back_stack_power(self) -> float:
        """Calculates the power consumed by all chips stacked on the back of this chip."""
        back_stack_power = 0.0
        for chip in self.back_chips:
            back_stack_power += chip.total_power
        return back_stack_power

    def compute_stack_power(self) -> float:
        stack_power = self.face_stack_power() + self.back_stack_power()
        # stack_power = 0.0
        # for chip in self.face_chips:
            # stack_power += chip.total_power
        return stack_power

    def find_process(self, process_name, process_list):
        # Generic helper to find a process object in a list by its name.
        for p in process_list:
            if p.name == process_name:
                return p
        print(f"Error: Process '{process_name}' not found in the provided list.")
        return None

    def find_io_type(self, io_type, io_list):
        # Function to find IO type since IO does not have a name field.
        # In the future, this should probably be standardized to include a name field.
        for p in io_list:
            if p.type == io_type:
                return p
        print(f"Error: Process '{io_type}' not found in the provided list.")
        return None

    def find_wafer_process(self, wafer_process_name, wafer_process_list):
        wafer_process = self.find_process(wafer_process_name, wafer_process_list)
        if wafer_process is None:
            raise ConfigurationError(f"Wafer Process '{wafer_process_name}' not found.")
        return wafer_process

    def find_assembly_process(self, assembly_process_name, assembly_process_list):
        assembly_process = self.find_process(assembly_process_name, assembly_process_list)
        if assembly_process is None:
            raise ConfigurationError(f"Assembly Process '{assembly_process_name}' not found.")
        return assembly_process

    def find_test_process(self, test_process_name, test_process_list):
        test_process = self.find_process(test_process_name, test_process_list)
        if test_process is None:
            raise ConfigurationError(f"Test Process '{test_process_name}' not found.")
        return test_process

    def build_stackup(self, stackup_string, layers):
        stackup = []
        # The stackup string is a comma-separated list, e.g., "4:M1,2:M2"
        stackup_parts = stackup_string.split(",")
        for part in stackup_parts:
            try:
                count_str, layer_name = part.split(":")
                count = int(count_str)
                if count >= 0:
                    layer_obj = self.find_process(layer_name.strip(), layers)
                    if layer_obj:
                        stackup.extend([layer_obj] * count)
                    else:
                        raise ConfigurationError(f"Layer '{layer_name}' not found in layer definitions.")
                else:
                    raise ConfigurationError(f"Invalid layer count '{count}' for layer '{layer_name}'.")
            except ValueError:
                raise ConfigurationError(f"Invalid stackup format for part '{part}'. Expected 'count:name'.")
        return stackup

    # ===== Other Getters (Directly computed or from sub-objects) =====

    def get_assembly_core_area(self) -> float:
        assembly_core_area = self.core_area
        for chip in self.face_chips:
            assembly_core_area += chip.get_assembly_core_area()
        for chip in self.back_chips:
            assembly_core_area += chip.get_assembly_core_area()
        # for chip in self.chips:
            # assembly_core_area += chip.get_assembly_core_area()
        return assembly_core_area

    def get_self_gates_per_mm2(self) -> float:
        self_gates_per_mm2 = 0.0
        for layer in self.stackup:
            if layer.active:
                self_gates_per_mm2 += layer.get_gates_per_mm2()
        return self_gates_per_mm2

    def get_assembly_gates_per_mm2(self) -> float:
        total_core_area = self.get_assembly_core_area()
        if total_core_area == 0:
            return 0.0
        
        weighted_gates_sum = self.get_self_gates_per_mm2() * self.core_area
        for chip in self.face_chips:
            weighted_gates_sum += chip.get_assembly_gates_per_mm2() * chip.get_assembly_core_area()
        for chip in self.back_chips:
            weighted_gates_sum += chip.get_assembly_gates_per_mm2() * chip.get_assembly_core_area()
        # for chip in self.chips:
            # weighted_gates_sum += chip.get_assembly_gates_per_mm2() * chip.get_assembly_core_area()

        return weighted_gates_sum / total_core_area
    
    def get_chips_len(self) -> int:
        # return len(self.chips)
        return len(self.face_chips) + len(self.back_chips)

    def get_stacked_die_area(self) -> float:
        # Calculates the area required by the stack of chips on this interposer/chip,
        # including separation and edge exclusion.
        face_area = 0.0
        for chip in self.face_chips:
            if not chip.buried:
                # Expand each child chip's area by the die separation distance.
                temp_area = self.expandedArea(chip.area, self.assembly_process.die_separation/2, chip.aspect_ratio)
                face_area += temp_area
        back_area = 0.0
        for chip in self.back_chips:
            if not chip.buried:
                # Expand each child chip's area by the die separation distance.
                temp_area = self.expandedArea(chip.area, self.assembly_process.die_separation/2, chip.aspect_ratio)
                back_area += temp_area
        stacked_die_area = max(face_area, back_area)
        # for chip in self.chips:
        #     if not chip.buried:
        #         # Expand each child chip's area by the die separation distance.
        #         temp_area = self.expandedArea(chip.area, self.assembly_process.die_separation/2, chip.aspect_ratio)
        #         stacked_die_area += temp_area
        
        # Expand the total stacked area by the edge exclusion.
        # Note: Assumes a square packing for this calculation, which is an approximation.
        if stacked_die_area > 0:
            stacked_die_area = self.expandedArea(stacked_die_area, self.assembly_process.edge_exclusion)

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

    def __str__(self):
        """String representation of the chip with detailed description."""
        lines = []
        lines.append(f"--- Chip Description: {self.name} ---")
        lines.append(f"  Wafer Process: {self.wafer_process.name}, Assembly: {self.assembly_process.name}, Test: {self.test_process.name}")
        if self.bb_area or self.bb_cost or self.bb_quality or self.bb_power:
            lines.append(f"  Black-Box Overrides: Area={self.bb_area}, Cost={self.bb_cost}, Quality={self.bb_quality}, Power={self.bb_power}")
        lines.append(f"  Core Area: {self.core_area:.2f} mm^2, Aspect Ratio: {self.aspect_ratio:.2f}")
        lines.append(f"  Pad Area: {self.get_pad_area():.2f} mm^2")
        lines.append(f"  IO Area: {self.get_io_area():.2f} mm^2, TSV Area: {self.get_tsv_area():.2f} mm^2")
        lines.append(f"  Fractions: {self.fraction_memory*100}% Mem, {self.fraction_logic*100}% Logic, {self.fraction_analog*100}% Analog")
        lines.append(f"  Calculated Total Area: {self.area:.2f} mm^2")
        lines.append(f"  Calculated Power: {self.power:.2f}W (Core), {self.io_power:.2f}W (IO), {self.stack_power:.2f}W (Stack) -> Total: {self.total_power:.2f}W")
        lines.append(f"  --- Yield & Quality ---")
        lines.append(f"  Self True/Test Yield: {self.self_true_yield:.4f} / {self.self_test_yield:.4f}")
        lines.append(f"  Self Quality: {self.self_quality:.4f}")
        lines.append(f"  Assembly True/Test Yield: {self.chip_true_yield:.4f} / {self.chip_test_yield:.4f}")
        lines.append(f"  Final Quality: {self.quality:.4f}")
        lines.append(f"  --- Cost (per unit for quantity={self.quantity}) ---")
        lines.append(f"  Self Cost (yielded): ${self.self_cost:,.2f}")
        lines.append(f"  NRE Cost (design, mask, ATPG): ${self.compute_nre_cost():,.2f}")
        lines.append(f"  Total Final Cost (including stack, assembly, test): ${self.cost:,.2f}")
        lines.append(f"  Total Cost with NRE: ${self.compute_total_cost():,.2f}")
        
        if self.face_chips:
            lines.append(f"  --- Stacked Chips on Face ({len(self.face_chips)}) ---")
            for chip in self.face_chips:
                lines.append(str(chip))
            lines.append(f"  --- End Stack for {self.name} (Face) ---")
        if self.back_chips:
            lines.append(f"  --- Stacked Chips on Back ({len(self.back_chips)}) ---")
            for chip in self.back_chips:
                lines.append(str(chip))
            lines.append(f"  --- End Stack for {self.name} (Back) ---")
        # if self.chips:
        #     lines.append(f"  --- Stacked Chips ({len(self.chips)}) ---")
        #     for chip in self.chips:
        #         lines.append(str(chip))
        #     lines.append(f"  --- End Stack for {self.name} ---")
        lines.append(f"--- End Description: {self.name} ---\n")
        
        return "\n".join(lines)

    def print_description(self):
        """Print chip description. Kept for backward compatibility."""
        print(self)

    def expandedArea(self,area,border,aspect_ratio=1.0):
        # Calculates the new area after adding a border around an existing area.
        if area <= 0.0:
            return 0.0
        x = math.sqrt(area*aspect_ratio)
        y = math.sqrt(area/aspect_ratio)
        new_area = (x+2*border)*(y+2*border)
        return new_area

    def get_io_area(self):
        # Calculates the total area required by the I/O cells based on the netlist.
        io_area = 0.0
        try:
            block_index = self.block_names.index(self.name)
        except ValueError:
            # This chip is not in the netlist, so it has no direct IOs.
            return 0.0
            
        for io_type in self.global_adjacency_matrix:
            io = self.find_io_type(io_type, self.io_list)
            if io:
                # Sum connections from this chip to others (TX) and from others to this chip (RX).
                tx_connections = np.sum(self.global_adjacency_matrix[io_type][block_index, :])
                rx_connections = np.sum(self.global_adjacency_matrix[io_type][:, block_index])
                io_area += tx_connections * io.tx_area + rx_connections * io.rx_area
        return io_area

    def get_power_pads(self):
        # Calculates the number of pads required for power and ground.
        if self.core_voltage == 0: return 0
        power_per_pad = self.assembly_process.get_power_per_pad(self.core_voltage)
        if power_per_pad == 0: return float('inf') # Avoid division by zero
        # One pad for power, one for ground.
        num_power_delivery_pads = math.ceil(self.total_power / power_per_pad) * 2
        return num_power_delivery_pads

    def get_pad_count(self):
        """
        Returns the total number of pads required for this chip (power pads + test pads + signal pads).
        """
        num_power_pads = self.get_power_pads()
        num_test_pads = self.test_process.num_test_ios()
        signal_pads, _ = self.get_signal_count(self.get_chip_list())
        num_pads = signal_pads + num_power_pads + num_test_pads
        if self.orientation == "face-up":
            for chip in self.back_chips:
                num_pads += chip.get_pad_count()
        else:
            for chip in self.face_chips:
                num_pads += chip.get_pad_count()
        return num_pads

    def get_face_pad_count(self):
        face_pad_count = 0
        if self.orientation == "face-up":
            # Count the pads facing away from the parent chip.
            face_pad_count = 0
            for chip in self.face_chips:
                face_pad_count += chip.get_pad_count()
        else:
            # Count the pads facing towards the parent chip.
            face_pad_count = self.get_pad_count()
        return face_pad_count

    def get_back_pad_count(self):
        back_pad_count = 0
        if self.orientation == "face-up":
            # Count the pads facing towards the parent chip.
            back_pad_count = self.get_pad_count()
        else:
            # Count the pads facing away from the parent chip.
            back_pad_count = 0
            for chip in self.back_chips:
                back_pad_count += chip.get_pad_count()
        return back_pad_count

    def get_tsv_count(self):
        # This is just an alias for get_back_pad_count
        return self.get_back_pad_count()

    def get_tsv_area(self):
        tsv_count = self.get_tsv_count()
        if tsv_count == 0:
            return 0.0
        # Each TSV will have a fixed area based on the tsv process.
        tsv_area = self.assembly_process.tsv_area * tsv_count
        return tsv_area

    def get_pad_area(self):
        num_power_pads = self.get_power_pads()
        num_test_pads = self.test_process.num_test_ios()
        signal_pads, signal_with_reach_count = self.get_signal_count(self.get_chip_list())
        num_pads = signal_pads + num_power_pads + num_test_pads
        # print("num pads = " + str(num_pads))

        parent_chip = self.parent_chip
        if parent_chip is not None:
            bonding_pitch = max(parent_chip.assembly_process.bonding_pitch, self.assembly_process.bonding_pitch)
            if self.stack_side == "back":
                bonding_pitch = max(bonding_pitch, parent_chip.assembly_process.tsv_pitch)
                if self.orientation == "face-up":
                    bonding_pitch = max(bonding_pitch, self.assembly_process.tsv_pitch)
            else:
                if self.orientation == "face-up":
                    bonding_pitch = max(bonding_pitch, self.assembly_process.tsv_pitch)
        else:
            bonding_pitch = self.assembly_process.bonding_pitch
        area_per_pad = bonding_pitch**2

        under_stacked_chip_area = 0.0
        if self.orientation == "face-up":
            for chip in self.back_chips:
                under_stacked_chip_area += chip.area
        else:
            for chip in self.face_chips:
                under_stacked_chip_area += chip.area

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
                raise CalculationError("Reach is smaller than chip separation.")
            current_count += signal_with_reach_count[str(reach)]
            # Find the minimum boundary that would contain all the pads with the current reach.
            required_area = current_count*area_per_pad + under_stacked_chip_area
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

    def compute_area(self):
        # The final area of the chip is the maximum of three factors:
        # 1. The core logic/memory area plus its own I/O cells.
        # 2. The area required to place all the dies stacked on top of it.
        # 3. The area required for all the physical bonding pads on its surface.
        if self.bb_area is not None:
            return self.bb_area

        chip_io_area = self.core_area + self.get_io_area() + self.get_tsv_area()
        pad_required_area = self.get_pad_area()
        stacked_die_bound_area = self.get_stacked_die_area()
        
        chip_area = max(stacked_die_bound_area, pad_required_area, chip_io_area)
        return chip_area
        
    def compute_layer_aware_yield(self) -> float:
        # The intrinsic yield of the chip itself, based on its layer stackup.
        layer_yield = 1.0
        # Total area susceptible to defects is the core area plus the I/O cell area.
        defect_area = self.core_area + self.get_io_area()
        for layer in self.stackup:
            layer_yield *= layer.layer_yield(defect_area)
        return layer_yield

    def quality_yield(self) -> float:
        # The probability that all component chips received for assembly are actually good,
        # given that they passed their own tests.
        quality_yield = 1.0
        for chip in self.face_chips:
            quality_yield *= chip.self_quality
        for chip in self.back_chips:
            quality_yield *= chip.self_quality
        # for chip in self.chips:
        #     quality_yield *= chip.quality
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

    # def get_signal_count(self, internal_block_list):
    #     # Counts the number of signal wires connecting this chip to external blocks.
    #     signal_count = 0
    #     signal_with_reach_count = {} # This is not currently used but could be for more detailed analysis.

    #     try:
    #         block_index = self.block_names.index(self.name)
    #     except ValueError:
    #         return 0, {}

    #     # Vectorized approach to find external block indices
    #     num_blocks = len(self.block_names)
    #     is_internal = np.zeros(num_blocks, dtype=bool)
    #     internal_indices = [self.block_names.index(name) for name in internal_block_list if name in self.block_names]
    #     is_internal[internal_indices] = True
    #     is_external = ~is_internal

    #     for io_type in self.global_adjacency_matrix:
    #         io = self.find_io_type(io_type, self.io_list)
    #         if io:
    #             bidirectional_factor = 0.5 if io.bidirectional else 1.0
    #             adj_matrix = self.global_adjacency_matrix[io_type]
                
    #             # Sum connections to (TX) and from (RX) all external blocks
    #             tx_connections = np.sum(adj_matrix[block_index, is_external])
    #             rx_connections = np.sum(adj_matrix[is_external, block_index])
                
    #             connections = tx_connections + rx_connections
    #             signal_count += connections * io.wire_count * bidirectional_factor
                
    #     return signal_count, signal_with_reach_count

    def get_signal_power(self,internal_block_list) -> float:
        # Calculates the power consumed by signal I/O.
        signal_power = 0.0
        try:
            block_index = self.block_names.index(self.name)
        except ValueError:
            return 0.0

        for io_type in self.global_adjacency_matrix:
            io = self.find_io_type(io_type, self.io_list)
            if io:
                bidirectional_factor = 0.5 if io.bidirectional else 1.0
                # Sum the bandwidth of all connections, element-wise weighted by utilization.
                tx_bw = np.sum(self.global_adjacency_matrix[io_type][block_index,:] * self.average_bandwidth_utilization[io_type][block_index,:])
                rx_bw = np.sum(self.global_adjacency_matrix[io_type][:,block_index] * self.average_bandwidth_utilization[io_type][:,block_index])
                total_utilized_bw = (tx_bw + rx_bw) * bidirectional_factor
                # Power = (Total Gbps) * (pJ/bit) = (Total bits/s * 1e-9) * (Joules/bit * 1e-12) -> needs conversion
                # Power (W) = (Gbps * 1e9) * (pJ/bit * 1e-12)
                signal_power += total_utilized_bw * io.bandwidth * io.energy_per_bit * 1e-3
        return signal_power

    def get_chip_list(self):
        # Recursively build a flat list of all chip names in the current assembly stack.
        chip_list = [self.name]
        for chip in self.face_chips:
            chip_list.extend(chip.get_chip_list())
        for chip in self.back_chips:
            chip_list.extend(chip.get_chip_list())
        # for chip in self.chips:
        #     chip_list.extend(chip.get_chip_list())
        return chip_list

    def get_chips_signal_count(self) -> int:
        # Counts the total number of signals for all chips in the stack.
        signal_count = 0
        internal_chip_list = self.get_chip_list()
        for chip in self.face_chips:
            signal_count += chip.get_signal_count(internal_chip_list)[0]
        for chip in self.back_chips:
            signal_count += chip.get_signal_count(internal_chip_list)[0]
        # for chip in self.chips:
        #     signal_count += chip.get_signal_count(internal_chip_list)[0]
        return signal_count

    def compute_chip_yield(self) -> float:
        # Computes the true yield of a fully assembled chip.
        # It's a product of this chip's own quality, the quality of its components, the assembly process yield, and the base wafer yield.
        # This chip's quality after its own test
        chip_yield = self.self_quality
        # Probability that all sub-components are good
        chip_yield *= self.quality_yield()
        # Yield of the physical assembly process
        chip_yield *= self.assembly_process.assembly_yield(len(self.face_chips) + len(self.back_chips), self.get_chips_signal_count(), self.get_tsv_count(), self.get_stacked_die_area())
        # Base yield of the wafer process
        chip_yield *= self.wafer_process.wafer_process_yield
        return chip_yield

    def get_layer_aware_cost(self):
        # Calculates the manufacturing cost of the chip's layers.
        cost = 0
        for layer in self.stackup:
            cost += layer.layer_cost(self.area, self.aspect_ratio, self.wafer_process)
        return cost

    def get_mask_cost(self):
        # Calculates the NRE cost of the mask set for this chip.
        cost = 0
        for layer in self.stackup:
            cost += layer.mask_cost
        # Account for sharing the mask set with other designs.
        cost *= self.reticle_share
        return cost

    def compute_nre_cost(self) -> float:
        # Computes the total Non-Recurring Engineering (NRE) cost per chip.
        # This includes design, mask, and test pattern generation costs, amortized over the production quantity.
        nre_cost = (self.nre_design_cost + self.get_mask_cost() + self.test_process.get_atpg_cost(self))/self.quantity
        # Recursively add the NRE costs from sub-chips.
        for chip in self.face_chips:
            nre_cost += chip.compute_nre_cost()
        for chip in self.back_chips:
            nre_cost += chip.compute_nre_cost()
        # for chip in self.chips:
        #     nre_cost += chip.compute_nre_cost()
        return nre_cost

    def compute_self_cost(self) -> float:
        # The cost of a single, standalone chip, including manufacturing and self-test, adjusted for yield losses at this stage.
        if self.bb_cost is not None:
            return self.bb_cost
        
        # Start with the raw manufacturing cost of the layers.
        cost = self.get_layer_aware_cost()
        # Add the cost of testing this individual chip.
        cost += self.test_process.compute_self_test_cost(self)
        # Adjust for yield: the cost of good chips must cover the cost of bad ones discarded during self-test.
        if self.self_test_yield > 0:
            cost /= self.self_test_yield
        else:
            return float('inf') # If yield is zero, cost is infinite.
            
        return cost

    def compute_cost(self) -> float:
        # The final cost of the fully assembled product.
        # Start with the cost of the base chip itself.
        cost = self.self_cost
        
        # Add the cost of all the stacked chips.
        for chip in self.face_chips:
            cost += chip.cost
        for chip in self.back_chips:
            cost += chip.cost
        # for chip in self.chips:
        #     cost += chip.cost
        
        # Add the cost of the physical assembly process.
        cost += self.assembly_process.assembly_cost(len(self.face_chips) + len(self.back_chips), self.get_stacked_die_area())

        # Add the cost of testing the final assembly.
        cost += self.test_process.compute_assembly_test_cost(self)
        
        # Adjust for yield of the final assembly and test process.
        if self.chip_test_yield > 0:
            cost /= self.chip_test_yield
        else:
            return float('inf')
            
        return cost
    
    def compute_self_perfect_yield_cost(self) -> float:
        # Calculates the cost assuming 100% yield at the self-test stage.
        if self.bb_cost is not None:
            return self.bb_cost
        
        cost = self.get_layer_aware_cost()
        cost += self.test_process.compute_self_test_cost(self)
        return cost

    def compute_perfect_yield_cost(self) -> float:
        # Calculates the final cost assuming 100% yield at all stages.
        cost = self.compute_self_perfect_yield_cost()
        for chip in self.face_chips:
            cost += chip.compute_perfect_yield_cost()
        for chip in self.back_chips:
            cost += chip.compute_perfect_yield_cost()
        # for chip in self.chips:
        #     cost += chip.compute_perfect_yield_cost()
        cost += self.assembly_process.assembly_cost(len(self.face_chips) + len(self.back_chips), self.get_stacked_die_area())
        cost += self.test_process.compute_assembly_test_cost(self)
        return cost
    
    def compute_scrap_cost(self) -> float:
        # The scrap cost is the difference between the actual cost (with yield losses) and the ideal cost (with perfect yield).
        return self.cost - self.compute_perfect_yield_cost()

    def compute_total_non_scrap_cost(self) -> float:
        # The total cost of a good part, including ideal manufacturing and NRE.
        return self.compute_perfect_yield_cost() + self.compute_nre_cost()

    def compute_total_cost(self) -> float:
        # The final, all-inclusive cost per unit.
        total_cost = self.cost + self.compute_nre_cost()
        return total_cost
