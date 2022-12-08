import pyverilog.vparser.ast as vast
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator
import sram_compiler

def create_config(mem_data, num_r_ports, num_w_ports, num_rw_ports):
    for key, value in mem_data.items():
        num_words = value[0]
        word_size = value[1]
        tech_name = 'scn4m_subm'
        name = key.split(".")[0]
        with open(f"{name}.py", "w") as file:
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

        print("Done creating OpenRAM configuration file for memory:", key, "of depth:", num_words, "and width:", word_size)
        return f"sram_{word_size}_{num_words}_{tech_name}"

def verilog_writer(
        topmodule, portlist, instance_name, num_r_ports,
        num_w_ports, num_rw_ports, openram_ports,
        module_port_list, module_port_polarity):
    items = []
    assignments = []
    ports_list = portlist
    for port in ports_list.ports:
        if str(type(port.first)) == "<class 'pyverilog.vparser.ast.Output'>":
            dout = vast.Reg(str(port.first.name), width=port.first.width)
            dout_wire = vast.Wire(str(port.first.name+"_wire"), width=port.first.width)
            items.append(dout)
            items.append(dout_wire)
            assign_dout = vast.NonblockingSubstitution(
                vast.Lvalue(vast.Identifier(str(port.first.name))),
                vast.Rvalue(vast.Identifier(str(port.first.name+"_wire"))))
            assignments.append(assign_dout)


    openram_port_polarity = sram_compiler.get_openram_port_polarity()

    def get_port_polarity(module_port_pol, openram_port_pol):
        if module_port_pol == "active low" and openram_port_pol == "active low":
            return ""
        elif module_port_pol == "active low" and openram_port_pol == "active high":
            return "~"
        elif module_port_pol == "active high" and openram_port_pol == "active low":
            return "~"
        elif module_port_pol == "active high " and openram_port_pol == "active high":
            return ""


    # right now just storing the read value to dout reg based on the
    # first clock provided by the user in case of dual port sram
    clock = module_port_list["clock"][0]

    sens = vast.Sens(vast.Identifier(clock), type='posedge')
    senslist = vast.SensList([sens])

    statement = vast.Block(assignments)

    always = vast.Always(senslist, statement)

    instance_port_list = []

    for key, ports in openram_ports.items():
        if num_rw_ports == 2:
            port_type = key
            if port_type == "chip_select" or port_type == "write_en":
                sign = get_port_polarity(module_port_polarity[port_type], openram_port_polarity[port_type])

                argname0 = sign + module_port_list[port_type][0]
                argname1 = sign + module_port_list[port_type][1]
                port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                instance_port_list.append(port0)
                instance_port_list.append(port1)
            else:
                if port_type == "data_out":
                    argname0 = module_port_list[port_type][0]+"_wire"
                    argname1 = module_port_list[port_type][1]+"_wire"
                    port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                    port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                    instance_port_list.append(port0)
                    instance_port_list.append(port1)
                else:
                    port0_name = ports[0]
                    port1_name = ports[1]
                    argname0 = module_port_list[port_type][0]
                    argname1 = module_port_list[port_type][1]
                    port0 = vast.PortArg(portname=port0_name, argname=vast.Identifier(name=argname0))
                    port1 = vast.PortArg(portname=port1_name, argname=vast.Identifier(name=argname1))
                    instance_port_list.append(port0)
                    instance_port_list.append(port1)
        elif num_rw_ports == 1:
            if num_r_ports == 1:
                # 1rw1r configuration
                port_type = key
                if port_type == "data_in" or port_type == "write_en":
                    # checking for the polarity on write_en
                    if port_type == "write_en":
                        sign = get_port_polarity(module_port_polarity[port_type], openram_port_polarity[port_type])
                        argname0 = sign + module_port_list[port_type][0]
                        port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                        instance_port_list.append(port0)
                    else:
                        argname0 = module_port_list[port_type][0]
                        port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                        instance_port_list.append(port0)
                else:
                    if port_type == "data_out":
                        argname0 = module_port_list[port_type][0]+"_wire"
                        argname1 = module_port_list[port_type][1]+"_wire"
                        port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                        port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                        instance_port_list.append(port0)
                        instance_port_list.append(port1)
                    else:
                        if port_type == "chip_select":
                            sign = get_port_polarity(module_port_polarity[port_type], openram_port_polarity[port_type])

                            argname0 = sign + module_port_list[port_type][0]
                            argname1 = sign + module_port_list[port_type][1]
                            port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                            port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                            instance_port_list.append(port0)
                            instance_port_list.append(port1)
                        else:
                            argname0 = module_port_list[port_type][0]
                            argname1 = module_port_list[port_type][1]
                            port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                            port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                            instance_port_list.append(port0)
                            instance_port_list.append(port1)
            elif num_w_ports == 1:
                # 1rw1w configuration
                port_type = key
                if port_type == "data_out":
                    argname0 = module_port_list[port_type][0]+"_wire"
                    port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                    instance_port_list.append(port0)
                elif port_type == "write_en":
                    sign = get_port_polarity(module_port_polarity[port_type], openram_port_polarity[port_type])
                    argname0 = sign + module_port_list[port_type][0]
                    port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                    instance_port_list.append(port0)
                else:
                    if port_type == "chip_select":
                        sign = get_port_polarity(module_port_polarity[port_type], openram_port_polarity[port_type])

                        argname0 = sign + module_port_list[port_type][0]
                        argname1 = sign + module_port_list[port_type][1]
                        port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                        port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                        instance_port_list.append(port0)
                        instance_port_list.append(port1)
                    else:
                        argname0 = module_port_list[port_type][0]
                        argname1 = module_port_list[port_type][1]
                        port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                        port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                        instance_port_list.append(port0)
                        instance_port_list.append(port1)
            else:
                # 1rw configuration
                port_type = key
                if port_type == "data_out":
                    argname0 = module_port_list[port_type][0]+"_wire"
                    port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                    instance_port_list.append(port0)
                elif port_type == "chip_select" or port_type == "write_en":
                    sign = get_port_polarity(module_port_polarity[port_type], openram_port_polarity[port_type])
                    argname0 = sign + module_port_list[port_type][0]
                    port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                    instance_port_list.append(port0)
                else:
                    argname0 = module_port_list[port_type][0]
                    port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                    instance_port_list.append(port0)
        else:
            if num_r_ports == 1 and num_w_ports == 1:
                # 1r1w configuration
                port_type = key
                if port_type == "data_in" or port_type == "data_out":
                    if port_type == "data_out":
                        argname0 = module_port_list[port_type][0]+"_wire"
                        port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                        instance_port_list.append(port0)
                    else:
                        argname0 = module_port_list[port_type][0]
                        port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                        instance_port_list.append(port0)
                elif port_type == "write_en":
                    pass
                elif port_type == "chip_select":
                    sign = get_port_polarity(module_port_polarity[port_type], openram_port_polarity[port_type])

                    argname0 = sign + module_port_list[port_type][0]
                    argname1 = sign + module_port_list[port_type][1]
                    port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                    port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                    instance_port_list.append(port0)
                    instance_port_list.append(port1)
                else:
                    argname0 = module_port_list[port_type][0]
                    argname1 = module_port_list[port_type][1]
                    port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                    port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                    instance_port_list.append(port0)
                    instance_port_list.append(port1)

    instance = vast.Instance(
            module=instance_name, name="sram",
            portlist=instance_port_list,
            parameterlist=None)

    instance_list = [instance]
    instances = vast.InstanceList(instance_name, (), instance_list)
    items.append(always)
    items.append(instances)
    ast = vast.ModuleDef(topmodule, None, ports_list, items)
    codegen = ASTCodeGenerator()
    rslt = codegen.visit(ast)

    with open(topmodule+"_generated.v", 'w') as f:
        print(rslt, file=f)
    print("Done writing verilog file:", topmodule+"_generated.v")
