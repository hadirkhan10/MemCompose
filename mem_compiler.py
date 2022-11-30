
def create_config(mem_data, num_r_ports, num_w_ports, num_rw_ports):
    for key, value in mem_data.items():
        num_words = value[0]
        word_size = value[1]
        tech_name = 'scn4m_subm'
        print("Creating memory:", key, "of depth:", num_words, "and width:", word_size)
        with open(f"{key}.py", "w") as file:
            file.write(f"# this file is created by MemCompose - Muhammad Hadir Khan\n"
                       f"# data word size \n"
                       f"word_size = {word_size}\n"
                       f"# num of words \n"
                       f"num_words = {num_words}\n"
                       f"num_rw_ports = {num_rw_ports}\n"
                       f"num_w_ports = {num_w_ports}\n"
                       f"num_r_ports = {num_r_ports}\n"
                       f"# Technology to use in $OPENRAM_TECH \n"
                       f"tech_name = '{tech_name}' \n"
                       f"nominal_corner_only = True \n"
                       f"output_path = 'temp' \n"
                       f"output_name = 'sram_{word_size}_{num_words}_{tech_name}'"
                       )

        return f"sram_{word_size}_{num_words}_{tech_name}"


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
            openram_ports["data_out"] = (data_out+"0")
            openram_ports["write_en"] = ()

    return openram_ports

