from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser

import pyverilog
import pyverilog.utils.util as util
from pyverilog.vparser.parser import parse
from pyverilog.dataflow.dataflow_analyzer import VerilogDataflowAnalyzer
from pyverilog.dataflow.optimizer import VerilogDataflowOptimizer
from pyverilog.dataflow.walker import VerilogDataflowWalker
from collections import defaultdict
import json



def parse_verilog(filelist, preprocess_include, preprocess_define):
    ast, directives = parse(filelist,
                            preprocess_include=preprocess_include,
                            preprocess_define=preprocess_define)

    return ast

    #mem_data = {}

    #for child in ast.children():
    #    # child.definitions gives us all the modules defined in the file
    #    for module in child.definitions:
    #        module_name = module.name
    #        print(type(module.portlist))
    #        for ports in module.portlist.ports:
    #            #ports_data[ports.first.name] = (por
    #            print(f"port type {ports.first}")
    #            print(f"port name {ports.first.name}")
    #            print(f"port width {ports.first.width}")
    #        # module.items give us the delcarations, always and assign statements
    #        for items in module.items:
    #            # filtering out just the declarations
    #            if str(type(items)) == "<class 'pyverilog.vparser.ast.Decl'>":
    #                # items.list for the declarations give us the either Reg or wires that are delcared
    #                for decl in items.list:
    #                    # looking for just register definitions
    #                    if str(type(decl)) == "<class 'pyverilog.vparser.ast.Reg'>":
    #                        # filtering just the multidimensional register declarations (considered as memories)
    #                        if (decl.dimensions != None):
    #                            memory_name = decl.name
    #                            mem_width = (int(decl.width.msb.value) - int(decl.width.lsb.value)) + 1
    #                            for dimensions in decl.dimensions.lengths:
    #                                mem_depth = (int(dimensions.msb.value) - int(dimensions.lsb.value)) + 1
    #                                mem_data[module_name + '.' + memory_name] = (mem_depth, mem_width)




    #ast.show()
    #return mem_data

def parse_json(jsonFile):
    acceptable_port_types = ["clock", "chip_select", "write_en", "address", "data_in", "data_out"]
    acceptable_polarity_types = ["active low", "active high"]
    module_port_list = defaultdict(list)
    module_port_polarity = {}

    with open(jsonFile, 'r') as f:
        contents = json.loads(f.read())

    for port in contents["ports"]:
        if port["type"] not in acceptable_port_types:
            raise Exception(f'invalid port type: {port["type"]}')
        else:
            if port["type"] == "chip_select" or port["type"] == "write_en":
                if port["polarity"] not in acceptable_polarity_types:
                    raise Exception(f'invalid polarity type: {port["polarity"]}')
                else:
                    module_port_polarity[port["type"]] = port["polarity"]
            module_port_list[port["type"]].append(port["name"])

    return module_port_list, module_port_polarity


def get_mem_data(ast):
    mem_data = {}

    for child in ast.children():
        # child.definitions gives us all the modules defined in the file
        for module in child.definitions:
            module_name = module.name
            # module.items give us the delcarations, always and assign statements
            for items in module.items:
                # filtering out just the declarations
                if str(type(items)) == "<class 'pyverilog.vparser.ast.InstanceList'>":
                    for instance in items.instances:
                        print(instance.parameterlist)
                        print(instance.module)
                        print(type(instance.module))
                        print(instance.name)
                        print(type(instance.name))
                        print(type(instance.portlist))
                        for port in instance.portlist:
                            print(type(port))
                            print("port name", port.portname)
                            print(type(port.portname))
                            print("argname", port.argname)
                            print(type(port.argname))
                if str(type(items)) == "<class 'pyverilog.vparser.ast.Decl'>":
                    # items.list for the declarations give us the either Reg or wires that are delcared
                    for decl in items.list:
                        # looking for just register definitions
                        if str(type(decl)) == "<class 'pyverilog.vparser.ast.Reg'>":
                            # filtering just the multidimensional register declarations (considered as memories)
                            if (decl.dimensions != None):
                                memory_name = decl.name
                                mem_width = (int(decl.width.msb.value) - int(decl.width.lsb.value)) + 1
                                for dimensions in decl.dimensions.lengths:
                                    mem_depth = (int(dimensions.msb.value) - int(dimensions.lsb.value)) + 1
                                    mem_data[module_name + '.' + memory_name] = (mem_depth, mem_width)

    return mem_data


def get_ports(ast):
    for child in ast.children():
        # child.definitions gives us all the modules defined in the file
        for module in child.definitions:
            return module.portlist


if __name__ == '__main__':
    parse_verilog()
