import os
import sys
import copy
import xml.etree.ElementTree as ET
import subprocess
import tempfile
import shutil

# Files to analyze
SIP_FILE = "sip.xml"
NETLIST_FILE = "netlist.xml"
IO_FILE = "io_definitions.xml"
LAYER_FILE = "layer_definitions.xml"
WAFER_FILE = "wafer_process_definitions.xml"
ASSEMBLY_FILE = "assembly_process_definitions.xml"
TEST_FILE = "test_definitions.xml"
LOAD_SCRIPT = "load_and_test_design.py"


PERCENT_CHANGE = 0.01  # 1% perturbation

# Parameter bounds based on design.py setters and domain knowledge
PARAM_BOUNDS = {
    # Chip/Stack parameters
    "fraction_memory": (0.0, 1.0),
    "fraction_logic": (0.0, 1.0),
    "fraction_analog": (0.0, 1.0),
    "reticle_share": (0.0, 1.0),
    "core_area": (0.0, None),  # >= 0
    "power": (0.0, None),      # >= 0
    "quantity": (0.0, None),   # >= 0
    "aspect_ratio": (0.0, None), # >= 0
    "gate_flop_ratio": (0.0, None), # >= 0
    "core_voltage": (0.0, None), # >= 0
    # IO parameters
    "tx_area": (0.0, None),
    "rx_area": (0.0, None),
    "shoreline": (0.0, None),
    "bandwidth": (0.0, None),
    "wire_count": (0.0, None),
    "energy_per_bit": (0.0, None),
    "reach": (0.0, None),
    # Layer parameters
    "cost_per_mm2": (0.0, None),
    "defect_density": (0.0, None),
    "critical_area_ratio": (0.0, 1.0),
    "clustering_factor": (0.0, None),
    "transistor_density": (0.0, None),
    "litho_percent": (0.0, 1.0),
    "nre_mask_cost": (0.0, None),
    "stitching_yield": (0.0, 1.0),
    # Wafer process parameters
    "wafer_diameter": (0.0, None),
    "edge_exclusion": (0.0, None),
    "wafer_process_yield": (0.0, 1.0),
    "dicing_distance": (0.0, None),
    "reticle_x": (0.0, None),
    "reticle_y": (0.0, None),
    "wafer_fill_grid": (0.0, 1.0),  # Boolean, but treat as [0,1]
    "nre_front_end_cost_per_mm2_memory": (0.0, None),
    "nre_back_end_cost_per_mm2_memory": (0.0, None),
    "nre_front_end_cost_per_mm2_logic": (0.0, None),
    "nre_back_end_cost_per_mm2_logic": (0.0, None),
    "nre_front_end_cost_per_mm2_analog": (0.0, None),
    "nre_back_end_cost_per_mm2_analog": (0.0, None),
    # Assembly process parameters
    "materials_cost_per_mm2": (0.0, None),
    "picknplace_machine_cost": (0.0, None),
    "picknplace_machine_lifetime": (0.0, None),
    "picknplace_machine_uptime": (0.0, 1.0),
    "picknplace_technician_yearly_cost": (0.0, None),
    "picknplace_time": (0.0, None),
    "picknplace_group": (1.0, None),
    "bonding_machine_cost": (0.0, None),
    "bonding_machine_lifetime": (0.0, None),
    "bonding_machine_uptime": (0.0, 1.0),
    "bonding_technician_yearly_cost": (0.0, None),
    "bonding_time": (0.0, None),
    "bonding_group": (1.0, None),
    "die_separation": (0.0, None),
    "edge_exclusion": (0.0, None),
    "max_pad_current_density": (0.0, None),
    "bonding_pitch": (0.0, None),
    "alignment_yield": (0.0, 1.0),
    "bonding_yield": (0.0, 1.0),
    "dielectric_bond_defect_density": (0.0, None),
    # Test process parameters
    "time_per_test_cycle": (0.0, None),
    "samples_per_input": (1.0, None),
    "cost_per_second": (0.0, None),
    "self_defect_coverage": (0.0, 1.0),
    "self_test_reuse": (1.0, None),
    "self_num_scan_chains": (0.0, None),
    "self_num_io_per_scan_chain": (1.0, None),
    "self_num_test_io_offset": (0.0, None),
    "assembly_defect_coverage": (0.0, 1.0),
    "assembly_test_reuse": (1.0, None),
    "assembly_num_scan_chains": (0.0, None),
    "assembly_num_io_per_scan_chain": (1.0, None),
    "assembly_num_test_io_offset": (0.0, None),
    # Netlist parameters
    "bb_count": (0.0, None),
    "average_bandwidth_utilization": (0.0, 1.0),
}

PARAM_INTEGER = {
    # Parameters that must be integers (from XML and design.py conventions)
    # These are not to be perturbed as floats
    "wire_count": True,  # IO
    "picknplace_group": True,  # assembly
    "bonding_group": True,  # assembly
    "samples_per_input": True,  # test
    "self_num_scan_chains": True,  # test
    "self_num_io_per_scan_chain": True,  # test
    "self_num_test_io_offset": True,  # test
    "assembly_num_scan_chains": True,  # test
    "assembly_num_io_per_scan_chain": True,  # test
    "assembly_num_test_io_offset": True,  # test
    "wiring_layer_count": True,  # layer
    "bb_count": True,  # netlist
    "bb_assembly_pattern_count": True,  # netlist
    "bb_assembly_scan_chain_length": True,  # netlist
    "quantity": True,  # chip
    "routing_layer_count": True,  # layer    
}

def is_integer_param(param):
    return PARAM_INTEGER.get(param, False)

def is_in_bounds(param, value):
    """Check if value is within bounds for param."""
    bounds = PARAM_BOUNDS.get(param)
    if bounds is None:
        return True
    low, high = bounds
    if low is not None and value < low:
        return False
    if high is not None and value > high:
        return False
    return True

def get_total_cost(args):
    """Run load_and_test_design.py and return the total cost as a float."""
    result = subprocess.run(
        [sys.executable, LOAD_SCRIPT] + args,
        capture_output=True, text=True
    )
    for line in result.stdout.splitlines():
        try:
            return float(line.strip().replace(",", ""))
        except ValueError:
            continue
    raise RuntimeError("Could not parse cost from output:\n" + result.stdout)

def find_referenced_names(sip_tree):
    """Return sets of referenced process/layer/io names from sip.xml."""
    referenced = {
        "assembly": set(),
        "test": set(),
        "wafer": set(),
        "layer": set(),
        "chip": set(),
    }
    root = sip_tree.getroot()
    recurse_chip_tree(root, referenced)
    return referenced

def recurse_chip_tree(chip_elem, referenced):
    referenced["chip"].add(chip_elem.attrib.get("name", ""))
    if "assembly_process" in chip_elem.attrib:
        referenced["assembly"].add(chip_elem.attrib["assembly_process"])
    if "test_process" in chip_elem.attrib:
        referenced["test"].add(chip_elem.attrib["test_process"])
    if "wafer_process" in chip_elem.attrib:
        referenced["wafer"].add(chip_elem.attrib["wafer_process"])
    if "stackup" in chip_elem.attrib:
        for layer in chip_elem.attrib["stackup"].split(","):
            if ":" in layer:
                _, lname = layer.split(":", 1)
                referenced["layer"].add(lname.strip())
    for child in chip_elem.findall("chip"):
        recurse_chip_tree(child, referenced)

def get_numeric_params(elem, path_prefix):
    """Yield (param_path, value, attrib_key, path_to_elem) for numeric attributes."""
    return _get_numeric_params_recurse(elem, path_prefix, [])

def _get_numeric_params_recurse(e, prefix, path):
    # Always add the current element to the path if it has a name attribute
    # This ensures the path uniquely identifies the element for perturbation
    new_path = path
    name = e.attrib.get("name")
    if name is not None:
        new_path = path + [(e.tag, name)]
    else:
        new_path = path
    for k, v in e.attrib.items():
        if v == "":
            continue  # Skip parameters with empty string values
        try:
            val = float(v)
            yield (f"{prefix}/{k}", val, k, new_path)
        except Exception:
            continue
    for child in e.findall("chip"):
        yield from _get_numeric_params_recurse(child, prefix, new_path)

def perturb_and_run(
    file_path, path, attrib_key, orig_val, percent, args, param_path
):
    """Perturb a parameter, write temp file, run, and restore."""
    with tempfile.NamedTemporaryFile("w", delete=False, suffix=".xml") as tf:
        temp_path = tf.name
    tree = ET.parse(file_path)
    root = tree.getroot()
    # If path is empty, the target is the root element
    if not path:
        target_elem = root
    else:
        target_elem = find_elem_by_path(root, path)
    if target_elem is None:
        raise RuntimeError(f"Element not found for {param_path}")
    param_name = attrib_key
    # Check if parameter is integer-valued
    if is_integer_param(param_name):
        # Try increasing first
        new_val_up = int(orig_val * (1 + percent))
        if new_val_up != orig_val and is_in_bounds(param_name, new_val_up):
            print(f"Truncating perturbed value for integer parameter {param_path}: {orig_val} -> {new_val_up}")
            target_elem.attrib[attrib_key] = str(new_val_up)
            tree.write(temp_path)
            new_args = [temp_path if os.path.basename(a) == os.path.basename(file_path) else a for a in args]
            cost = get_total_cost(new_args)
            os.remove(temp_path)
            return cost, 'increase', new_val_up
        # If increasing is out of bounds or no change, try decreasing
        new_val_down = int(orig_val * (1 - percent))
        if new_val_down != orig_val and is_in_bounds(param_name, new_val_down):
            print(f"Truncating perturbed value for integer parameter {param_path}: {orig_val} -> {new_val_down}")
            target_elem.attrib[attrib_key] = str(new_val_down)
            tree.write(temp_path)
            new_args = [temp_path if os.path.basename(a) == os.path.basename(file_path) else a for a in args]
            cost = get_total_cost(new_args)
            os.remove(temp_path)
            return cost, 'decrease', new_val_down
        # Both directions out of bounds or no change
        print(f"Error: Both increase ({new_val_up}) and decrease ({new_val_down}) out of bounds or no integer change for {param_path}")
        os.remove(temp_path)
        return None, 'error', None
    # Try increasing first (float)
    new_val_up = orig_val * (1 + percent)
    if is_in_bounds(param_name, new_val_up):
        target_elem.attrib[attrib_key] = str(new_val_up)
        tree.write(temp_path)
        new_args = [temp_path if os.path.basename(a) == os.path.basename(file_path) else a for a in args]
        cost = get_total_cost(new_args)
        os.remove(temp_path)
        return cost, 'increase', new_val_up
    # If increasing is out of bounds, try decreasing
    new_val_down = orig_val * (1 - percent)
    if is_in_bounds(param_name, new_val_down):
        target_elem.attrib[attrib_key] = str(new_val_down)
        tree.write(temp_path)
        new_args = [temp_path if os.path.basename(a) == os.path.basename(file_path) else a for a in args]
        cost = get_total_cost(new_args)
        os.remove(temp_path)
        return cost, 'decrease', new_val_down
    # Both directions out of bounds
    print(f"Error: Both increase ({new_val_up}) and decrease ({new_val_down}) out of bounds for {param_path}")
    os.remove(temp_path)
    return None, 'error', None

def find_elem_by_path(root, path):
    # If path is empty, return the root element
    if not path:
        return root
    
    # Make a copy of the path to avoid modifying the original
    path_copy = list(path)
    
    # Check if the root element matches the first item in the path
    if len(path_copy) > 0:
        first_tag, first_name = path_copy[0]
        if root.tag == first_tag and root.attrib.get("name") == first_name:
            # Remove the first path element since it matches the root
            path_copy.pop(0)
    
    # Start with the root element
    elem = root
    
    # Traverse the tree based on the path
    for tag, name in path_copy:
        # print(f"Searching for tag '{tag}' with name '{name}' in element '{elem.tag}'")
        found = False
        for child in elem:
            # print(f"Checking child element: {child.tag} with name {child.attrib.get('name')}")
            if child.tag == tag and child.attrib.get("name") == name:
                # print(f"Found matching element: {child.tag} with name {child.attrib.get('name')}")
                elem = child
                found = True
                break
            else:
                temp_elem = find_elem_by_path(child, path_copy)
                if temp_elem is not None:
                    elem = temp_elem
                    found = True
                    break
        if not found:
            # print(f"\tElement not found for tag '{tag}' with name '{name}' in element '{elem.tag}'")
            return None
    
    return elem

def analyze_file(file_path, tag, name_key, referenced_names, prefix, args, base_cost, results):
    tree = ET.parse(file_path)
    for elem in tree.getroot():
        if elem.tag != tag:
            continue
        name = elem.attrib.get(name_key, "")
        if name not in referenced_names:
            continue
        for param_path, orig_val, attrib_key, path in get_numeric_params(elem, f"{prefix}:{name}"):
            try:
                msg_buffer = []
                # Patch: capture stdout for messages from perturb_and_run
                import io
                import contextlib
                buf = io.StringIO()
                with contextlib.redirect_stdout(buf):
                    perturbed_cost, direction, new_val = perturb_and_run(
                        file_path, path, attrib_key, orig_val, PERCENT_CHANGE, args, param_path
                    )
                msg = buf.getvalue()
                if msg:
                    msg_buffer.append(msg.strip())
                if direction == 'integer':
                    results.append({
                        "param": param_path,
                        "base_value": orig_val,
                        "sensitivity": None,
                        "direction": 'integer',
                        "message": f"Parameter is integer-valued and not perturbed",
                        "extra_msgs": msg_buffer
                    })
                    continue
                if direction == 'error':
                    results.append({
                        "param": param_path,
                        "base_value": orig_val,
                        "sensitivity": None,
                        "direction": 'error',
                        "message": f"Both increase and decrease out of bounds",
                        "extra_msgs": msg_buffer
                    })
                    continue
                if perturbed_cost is None:
                    continue
                rel_sens = (perturbed_cost - base_cost) / (base_cost * PERCENT_CHANGE)
                if direction == 'decrease':
                    rel_sens *= -1
                results.append({
                    "param": param_path,
                    "base_value": orig_val,
                    "sensitivity": rel_sens,
                    "direction": direction,
                    "perturbed_value": new_val,
                    "extra_msgs": msg_buffer
                })
            except Exception as e:
                results.append({
                    "param": param_path,
                    "base_value": orig_val,
                    "sensitivity": None,
                    "direction": 'error',
                    "message": f"Exception: {e}",
                    "extra_msgs": []
                })

def analyze_chips(elem, prefix, args, base_cost, results):
    name = elem.attrib.get("name", "")
    for param_path, orig_val, attrib_key, path in get_numeric_params(elem, f"{prefix}:{name}"):
        try:
            msg_buffer = []
            import io
            import contextlib
            buf = io.StringIO()
            with contextlib.redirect_stdout(buf):
                perturbed_cost, direction, new_val = perturb_and_run(
                    SIP_FILE, path, attrib_key, orig_val, PERCENT_CHANGE, args, param_path
                )
            msg = buf.getvalue()
            if msg:
                msg_buffer.append(msg.strip())
            if direction == 'integer':
                results.append({
                    "param": param_path,
                    "base_value": orig_val,
                    "sensitivity": None,
                    "direction": 'integer',
                    "message": f"Parameter is integer-valued and not perturbed",
                    "extra_msgs": msg_buffer
                })
                continue
            if direction == 'error':
                results.append({
                    "param": param_path,
                    "base_value": orig_val,
                    "sensitivity": None,
                    "direction": 'error',
                    "message": f"Both increase and decrease out of bounds",
                    "extra_msgs": msg_buffer
                })
                continue
            if perturbed_cost is None:
                continue
            rel_sens = (perturbed_cost - base_cost) / (base_cost * PERCENT_CHANGE)
            if direction == 'decrease':
                rel_sens *= -1
            results.append({
                "param": param_path,
                "base_value": orig_val,
                "sensitivity": rel_sens,
                "direction": direction,
                "perturbed_value": new_val,
                "extra_msgs": msg_buffer
            })
        except Exception as e:
            results.append({
                "param": param_path,
                "base_value": orig_val,
                "sensitivity": None,
                "direction": 'error',
                "message": f"Exception: {e}",
                "extra_msgs": []
            })
    for child in elem.findall("chip"):
        analyze_chips(child, prefix, args, base_cost, results)

def analyze_io_file(io_file, referenced_io_types, args, base_cost, results):
    tree = ET.parse(io_file)
    for elem in tree.getroot():
        if elem.tag != "io":
            continue
        name = elem.attrib.get("type", "")
        if name not in referenced_io_types:
            continue
        for param_path, orig_val, attrib_key, path in get_numeric_params(elem, f"io:{name}"):
            try:
                msg_buffer = []
                import io as _io
                import contextlib as _contextlib
                buf = _io.StringIO()
                with _contextlib.redirect_stdout(buf):
                    perturbed_cost, direction, new_val = perturb_and_run(
                        io_file, path, attrib_key, orig_val, PERCENT_CHANGE, args, param_path
                    )
                msg = buf.getvalue()
                if msg:
                    msg_buffer.append(msg.strip())
                if direction == 'integer':
                    results.append({
                        "param": param_path,
                        "base_value": orig_val,
                        "sensitivity": None,
                        "direction": 'integer',
                        "message": f"Parameter is integer-valued and not perturbed",
                        "extra_msgs": msg_buffer
                    })
                    continue
                if direction == 'error':
                    results.append({
                        "param": param_path,
                        "base_value": orig_val,
                        "sensitivity": None,
                        "direction": 'error',
                        "message": f"Both increase and decrease out of bounds",
                        "extra_msgs": msg_buffer
                    })
                    continue
                if perturbed_cost is None:
                    continue
                rel_sens = (perturbed_cost - base_cost) / (base_cost * PERCENT_CHANGE)
                if direction == 'decrease':
                    rel_sens *= -1
                results.append({
                    "param": param_path,
                    "base_value": orig_val,
                    "sensitivity": rel_sens,
                    "direction": direction,
                    "perturbed_value": new_val,
                    "extra_msgs": msg_buffer
                })
            except Exception as e:
                results.append({
                    "param": param_path,
                    "base_value": orig_val,
                    "sensitivity": None,
                    "direction": 'error',
                    "message": f"Exception: {e}",
                    "extra_msgs": []
                })

def sort_key(r):
    s = r.get("sensitivity")
    return (-(abs(s) if s is not None else -1), r.get("param"))

def main():

    # Parse command line arguments for XML input files
    if len(sys.argv) != 8:
        print("Usage: python sensitivity_analysis.py <io_file> <layer_file> <wafer_process_file> <assembly_process_file> <test_file> <netlist_file> <chip_file>")
        sys.exit(1)

    io_file = sys.argv[1]
    layer_file = sys.argv[2]
    wafer_file = sys.argv[3]
    assembly_file = sys.argv[4]
    test_file = sys.argv[5]
    netlist_file = sys.argv[6]
    sip_file = sys.argv[7]

    # Parse sip.xml and find referenced processes/layers/etc.
    sip_tree = ET.parse(sip_file)
    referenced = find_referenced_names(sip_tree)

    # Get base cost
    args = [io_file, layer_file, wafer_file, assembly_file, test_file, netlist_file, sip_file]
    base_cost = get_total_cost(args)

    results = []

    # Update global file constants for use in perturb_and_run
    global SIP_FILE, IO_FILE, LAYER_FILE, WAFER_FILE, ASSEMBLY_FILE, TEST_FILE, NETLIST_FILE
    SIP_FILE = sip_file
    IO_FILE = io_file
    LAYER_FILE = layer_file
    WAFER_FILE = wafer_file
    ASSEMBLY_FILE = assembly_file
    TEST_FILE = test_file
    NETLIST_FILE = netlist_file

    analyze_chips(sip_tree.getroot(), "chip", args, base_cost, results)

    # Analyze referenced processes/layers
    analyze_file(assembly_file, "assembly", "name", referenced["assembly"], "assembly", args, base_cost, results)
    analyze_file(wafer_file, "wafer_process", "name", referenced["wafer"], "wafer_process", args, base_cost, results)
    analyze_file(test_file, "test_process", "name", referenced["test"], "test_process", args, base_cost, results)
    analyze_file(layer_file, "layer", "name", referenced["layer"], "layer", args, base_cost, results)

    # --- Analyze IO definitions for only IO types referenced in netlist.xml ---
    # 1. Parse netlist.xml to get set of referenced IO types
    netlist_tree = ET.parse(netlist_file)
    netlist_root = netlist_tree.getroot()
    referenced_io_types = set()
    for net in netlist_root.findall("net"):
        io_type = net.attrib.get("type")
        if io_type:
            referenced_io_types.add(io_type)

    # 2. Analyze only those IOs in io_definitions.xml
    analyze_io_file(io_file, referenced_io_types, args, base_cost, results)

    # Output results
    print("\n=== Sensitivity Analysis Results ===")
    # Separate successful and error results
    successful = [r for r in results if r.get("direction") not in ('error',)]
    errors = [r for r in results if r.get("direction") == 'error']
    # Sort all successful results (including integer) by descending |sensitivity|, with None last
    successful_sorted = sorted(successful, key=sort_key)
    # Print successful results
    for r in successful_sorted:
        for msg in r.get("extra_msgs", []):
            if msg:
                print(msg)
        if r.get("direction") == 'integer':
            print(f"{r['param']}: base={r['base_value']}, NOTE: {r['message']}")
        elif r.get("sensitivity") is not None:
            print(f"{r['param']} ({r['direction']}): base={r['base_value']}, perturbed={r['perturbed_value']}, sensitivity={r['sensitivity']:.4f}")
    # Print errors at the end
    if errors:
        print("\n--- Parameters with Errors ---")
        for r in errors:
            for msg in r.get("extra_msgs", []):
                if msg:
                    print(msg)
            print(f"{r['param']}: base={r['base_value']}, ERROR: {r['message']}")

if __name__ == "__main__":
    main()