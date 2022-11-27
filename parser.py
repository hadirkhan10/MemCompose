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


def parse_verilog(filelist, preprocess_include, preprocess_define):
    ast, directives = parse(filelist,
                            preprocess_include=preprocess_include,
                            preprocess_define=preprocess_define)




    mem_data = {}
    for child in ast.children():
        # child.definitions gives us all the modules defined in the file
        for module in child.definitions:
            # module.items give us the param list, port list, delcarations, always and assign statements
            module_name = module.name
            for items in module.items:
                # filtering out just the declarations
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




    #ast.show()
    return mem_data


if __name__ == '__main__':
    parse_verilog()
