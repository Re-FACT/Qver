#####################################################################
# Force the bitstream to specific ports
# - Parse bitstream file
# - Adapt paths for each configuration bit
# - Force signal to the design under test (DUT)
#####################################################################

from cocotb.handle import Force, Release, Deposit
import xml.etree.ElementTree as ET
import re
import cocotb

def parse_base_xml(base_file):
    """
    Parse the base XML file containing mapping from bit IDs to signal paths.
    Returns a dictionary: {bit_id: signal_path}.
    """
    id_to_path = {}
    tree = ET.parse(base_file)
    root = tree.getroot()

    for region in root.findall("region"):
        for bit in region.findall("bit"):
            bit_id = int(bit.attrib["id"])
            path = bit.attrib["path"]
            id_to_path[bit_id] = path

    return id_to_path


def parse_bit_xml(bit_file):
    """
    Parse the bit XML file containing mapping from bit IDs to bit values.
    Returns a dictionary: {bit_id: bit_value}.
    """
    bit_values = {}
    tree = ET.parse(bit_file)
    root = tree.getroot()

    for region in root.findall("region"):
        for bit in region.findall("bit"):
            bit_id = int(bit.attrib["id"])
            value = int(bit.attrib["value"])
            bit_values[bit_id] = value

    return bit_values


def cocotb_force_bitstream_to_dut_from_xml(
    dut,
    bitfile,
    pathfile,
    netlist_type,
    fpga_top_module="fpga_top",
    dut_path="dut.U0_formal_verification",
):
    """
    Force configuration bits from XML bitstream files to the DUT.

    Args:
        dut: cocotb DUT handle
        bitfile: XML file containing bit values
        pathfile: XML file containing signal paths
        netlist_type: Type of netlist ('rtl', 'gl', 'pl')
        fpga_top_module: Top module name in the bitstream
        dut_path: Corresponding path in the DUT
    """
    # Parse XML files
    id_to_path = parse_base_xml(pathfile)
    bit_values = parse_bit_xml(bitfile)

    # Build a mapping from path -> value
    path_value_map = {}
    for bit_id, path in id_to_path.items():
        value = bit_values.get(bit_id, 0)
        path_value_map[path] = value

    # Group bits by bus (e.g., signal[0], signal[1], etc.)
    bus_dict = {}
    pattern = re.compile(r"(.*)\[(\d+)\]$")

    for path, value in path_value_map.items():
        m = pattern.match(path)
        if not m:
            continue
        base_path, index = m.group(1), int(m.group(2))
        if base_path not in bus_dict:
            bus_dict[base_path] = {}
        bus_dict[base_path][index] = value

    # Construct full bus data values
    for base_path, bits in bus_dict.items():
        max_idx = max(bits.keys())
        # Concatenate bits
        data_bits = "".join(str(bits.get(i, 0)) for i in range(max_idx + 1))
        data_int = int(data_bits, 2)

        # Adjust hierarchical path for the testbench instance
        if netlist_type == "rtl":
            config_bit_fpath = str(base_path).replace(fpga_top_module, dut_path)
        elif netlist_type == "gl":
            config_bit_fpath = str(base_path).replace(fpga_top_module, dut_path)
        elif netlist_type == "pl":
            config_bit_fpath = str(base_path).replace(fpga_top_module, dut_path)

        # Apply force based on netlist type
        if netlist_type in ["rtl", "gl"]:
            obj = dut
            for name in config_bit_fpath.split(".")[1:]:  # Skip initial 'dut'
                obj = getattr(obj, name)
            # icarus verilog requires a different way to force signal
            # In case the SIM_NAME for icarus change. Use print(f"Sim: {cocotb.SIM_NAME}") to double check
            if cocotb.SIM_NAME == "Icarus Verilog":
                obj.value = data_int
            else: # The follow works on commercial simulators: vcs, modelsim, xceilum etc.
                obj.value = Force(data_int)

        elif netlist_type == "pl":
            dut._log.error("Post-layout netlist is not supported yet! Exiting...")

        else:
            raise Exception(f"Invalid netlist type '{netlist_type}'. Expected one of [rtl|gl|pl]!")
