# figure out if the memory is a single port or dual port
# if single port:
#   one sensitivity list
# else:
#   two sensitivity list

import pyverilog.vparser.ast as vast
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator


def verilog_writer(portlist, instance_name, num_r_ports, num_w_ports, num_rw_ports, openram_ports):
    items = []
    assignments = []
    ports_list = portlist
    for port in ports_list.ports:
        if str(type(port.first)) == "<class 'pyverilog.vparser.ast.Output'>":
            print(f"output name: {port.first.name}")
            print(f"output width: {port.first.width}")
            dout = vast.Reg(str(port.first.name), width=port.first.width)
            dout_wire = vast.Wire(str(port.first.name+"_wire"), width=port.first.width)
            items.append(dout)
            items.append(dout_wire)
            assign_dout = vast.NonblockingSubstitution(
                vast.Lvalue(vast.Identifier(str(port.first.name))),
                vast.Rvalue(vast.Identifier(str(port.first.name+"_wire"))))
            assignments.append(assign_dout)

    # 2RW
    # module_port_list = {

    #        "clock": ("clka", "clkb"),
    #        "chip_select": ("ena", "enb"),
    #        "write_en": ("wea", "web"),
    #        "address": ("addra", "addrb"),
    #        "data_in": ("dina", "dinb"),
    #        "data_out": ("douta", "doutb")
    #        }

    # 1rw1r
    # module_port_list = {
    #        "clock": ("clka", "clkb"),
    #        "chip_select": ("ena", "enb"),
    #        "write_en": ("wea"),
    #        "address": ("addra", "addrb"),
    #        "data_in": ("dina"),
    #        "data_out": ("doa", "dob")
    #        }

    # 1rw1w
    # module_port_list = {
    #        "clock": ("clka", "clkb"),
    #        "chip_select": ("ena", "enb"),
    #        "write_en": ("wea"),
    #        "address": ("addra", "addrb"),
    #        "data_in": ("dina", "dinb"),
    #        "data_out": ("doa")
    #        }

    # 1rw
    # module_port_list = {
    #        "clock": ("clk"),
    #        "chip_select": ("en"),
    #        "write_en": ("we"),
    #        "address": ("addr"),
    #        "data_in": ("di"),
    #        "data_out": ("dout")
    #        }

    # 1r1w
    module_port_list = {
            "clock": ("clka", "clkb"),
            "chip_select": ("ena", "enb"),
            "write_en": (),
            "address": ("addra", "addrb"),
            "data_in": ("dia"),
            "data_out": ("dob")
            }

    # TODO: right now just storing the read value to dout reg based on the
    # first clock provided by the user in case of dual port sram
    if len(module_port_list["clock"]) > 1:
        clock = module_port_list["clock"][0]
    else:
        clock = module_port_list["clock"]

    sens = vast.Sens(vast.Identifier(clock), type='posedge')
    senslist = vast.SensList([sens])

    statement = vast.Block(assignments)

    always = vast.Always(senslist, statement)

    instance_port_list = []

    for key, ports in openram_ports.items():
        if num_rw_ports == 2:
            port_type = key
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
                port_type = key
                if port_type == "data_in" or port_type == "write_en":
                    argname0 = module_port_list[port_type]
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
                        argname0 = module_port_list[port_type][0]
                        argname1 = module_port_list[port_type][1]
                        port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                        port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                        instance_port_list.append(port0)
                        instance_port_list.append(port1)
            elif num_w_ports == 1:
                port_type = key
                if port_type == "data_out" or port_type == "write_en":
                    if port_type == "data_out":
                        argname0 = module_port_list[port_type]+"_wire"
                        port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                        instance_port_list.append(port0)
                    else:
                        argname0 = module_port_list[port_type]
                        port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                        instance_port_list.append(port0)
                else:
                    argname0 = module_port_list[port_type][0]
                    argname1 = module_port_list[port_type][1]
                    port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                    port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                    instance_port_list.append(port0)
                    instance_port_list.append(port1)
            else:
                port_type = key
                if port_type == "data_out":
                    argname0 = module_port_list[port_type]+"_wire"
                    port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                    instance_port_list.append(port0)
                else:
                    argname0 = module_port_list[port_type]
                    port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                    instance_port_list.append(port0)
        else:
            if num_r_ports == 1 and num_w_ports == 1:
                port_type = key
                if port_type == "data_in" or port_type == "data_out":
                    if port_type == "data_out":
                        argname0 = module_port_list[port_type]+"_wire"
                        port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                        instance_port_list.append(port0)
                    else:
                        argname0 = module_port_list[port_type]
                        port0 = vast.PortArg(portname=ports, argname=vast.Identifier(name=argname0))
                        instance_port_list.append(port0)
                elif port_type == "write_en":
                    pass
                else:
                    argname0 = module_port_list[port_type][0]
                    argname1 = module_port_list[port_type][1]
                    port0 = vast.PortArg(portname=ports[0], argname=vast.Identifier(name=argname0))
                    port1 = vast.PortArg(portname=ports[1], argname=vast.Identifier(name=argname1))
                    instance_port_list.append(port0)
                    instance_port_list.append(port1)





    #instance_port_list = [vast.PortArg(portname="in", argname=vast.Identifier(name="clk"))]

    instance = vast.Instance(
            module=instance_name, name="sram",
            portlist=instance_port_list,
            parameterlist=None)

    instance_list = [instance]
    instances = vast.InstanceList(instance_name, (), instance_list)
    items.append(always)
    items.append(instances)
    ast = vast.ModuleDef("top", None, ports_list, items)
    codegen = ASTCodeGenerator()
    rslt = codegen.visit(ast)
    print(rslt)
