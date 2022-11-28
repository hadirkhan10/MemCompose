# figure out if the memory is a single port or dual port
# if single port:
#   one sensitivity list
# else:
#   two sensitivity list

import pyverilog.vparser.ast as vast
from pyverilog.ast_code_generator.codegen import ASTCodeGenerator

def verilog_writer(portlist):
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

    # TODO: generalize the clk signal by parsing the verilog file and asking the user
    # what is the clock signal
    # the user can use format like
    # .memcompose begin
    #   clock = clk
    # .memcompose end
    sens = vast.Sens(vast.Identifier('clk'), type='posedge')
    senslist = vast.SensList([sens])


    statement = vast.Block(assignments)

    always = vast.Always(senslist, statement)

    instance_port_list = [vast.PortArg(portname="in", argname=vast.Identifier(name="clk"))]
    instance = vast.Instance(module="sram1", name="sram", portlist=instance_port_list, parameterlist=None)

    instance_list = [instance]
    instances = vast.InstanceList("sram1", (), instance_list)
    items.append(always)
    items.append(instances)
    ast = vast.ModuleDef("top", None, ports_list, items)
    codegen = ASTCodeGenerator()
    rslt = codegen.visit(ast)
    print(rslt)
