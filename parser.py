from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser

import pyverilog
from pyverilog.vparser.parser import parse


def main():
    INFO = "Verilog code parser"
    VERSION = pyverilog.__version__
    USAGE = "Usage: python example_parser.py file ..."

    def showVersion():
        print(INFO)
        print(VERSION)
        print(USAGE)
        sys.exit()

    optparser = OptionParser()
    optparser.add_option("-v", "--version", action="store_true", dest="showversion",
                         default=False, help="Show the version")
    optparser.add_option("-I", "--include", dest="include", action="append",
                         default=[], help="Include path")
    optparser.add_option("-D", dest="define", action="append",
                         default=[], help="Macro Definition")
    (options, args) = optparser.parse_args()

    filelist = args
    if options.showversion:
        showVersion()

    for f in filelist:
        if not os.path.exists(f):
            raise IOError("file not found: " + f)

    if len(filelist) == 0:
        showVersion()

    ast, directives = parse(filelist,
                            preprocess_include=options.include,
                            preprocess_define=options.define)

    mem_data = {}
    for child in ast.children():
        # child.definitions gives us all the modules defined in the file
        for module in child.definitions:
            # module.items give us the param list, port list, delcarations, always and assign statements
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
                                    mem_depth = (int(dimensions.lsb.value) - int(dimensions.msb.value)) + 1
                                    mem_data[memory_name] = (mem_depth, mem_width)
    #print(ast.children()[0].children()[0].children())
    print(mem_data)
    ast.show()


if __name__ == '__main__':
    main()
