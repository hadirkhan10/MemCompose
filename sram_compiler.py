def create_openram_style_ports(num_r_ports, num_w_ports, num_rw_ports):
    openram_ports = {}
    clock = "clk"
    chip_select = "csb"
    address = "addr"
    data_in = "din"
    data_out = "dout"
    write_en = "web"
    # valid port numberings can be:
    # num_rw_ports = 2
    # num_rw_ports = 1
    # num_r_ports = 1, num_w_ports = 1
    # num_r_ports = 1, num_rw_ports = 1
    # num_w_ports = 1, num_rw_ports = 1
    if num_rw_ports == 2:
        # its a dual port 2rw configuration
        openram_ports["clock"] = (clock+"0", clock+"1")
        openram_ports["chip_select"] = (chip_select+"0", chip_select+"1")
        openram_ports["address"] = (address+"0", address+"1")
        openram_ports["data_in"] = (data_in+"0", data_in+"1")
        openram_ports["data_out"] = (data_out+"0", data_out+"1")
        openram_ports["write_en"] = (write_en+"0", write_en+"1")
    elif num_rw_ports == 1:
        if num_r_ports == 1:
            # its a dual port 1rw1r configuration
            openram_ports["clock"] = (clock+"0", clock+"1")
            openram_ports["chip_select"] = (chip_select+"0", chip_select+"1")
            openram_ports["address"] = (address+"0", address+"1")
            openram_ports["data_in"] = (data_in+"0")
            openram_ports["data_out"] = (data_out+"0", data_out+"1")
            openram_ports["write_en"] = (write_en+"0")
        elif num_w_ports == 1:
            # its a dual port 1rw1w configuration
            openram_ports["clock"] = (clock+"0", clock+"1")
            openram_ports["chip_select"] = (chip_select+"0", chip_select+"1")
            openram_ports["address"] = (address+"0", address+"1")
            openram_ports["data_in"] = (data_in+"0", data_in+"1")
            openram_ports["data_out"] = (data_out+"0")
            openram_ports["write_en"] = (write_en+"0")
        else:
            # its a single port 1rw configuration
            openram_ports["clock"] = (clock+"0")
            openram_ports["chip_select"] = (chip_select+"0")
            openram_ports["address"] = (address+"0")
            openram_ports["data_in"] = (data_in+"0")
            openram_ports["data_out"] = (data_out+"0")
            openram_ports["write_en"] = (write_en+"0")
    else:
        if num_r_ports == 1 and num_w_ports == 1:
            # its a dual port 1r1w configuration
            openram_ports["clock"] = (clock+"0", clock+"1")
            openram_ports["chip_select"] = (chip_select+"0", chip_select+"1")
            openram_ports["address"] = (address+"0", address+"1")
            openram_ports["data_in"] = (data_in+"0")
            openram_ports["data_out"] = (data_out+"1")
            openram_ports["write_en"] = ()

    return openram_ports


def get_openram_port_polarity():
    openram_port_polarity = {
            "chip_select": "active low",
            "write_en": "active low"
            }
    return openram_port_polarity
