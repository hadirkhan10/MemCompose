from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser
import pyverilog
import parser
import mem_compiler
import dataflow

def main():
    INFO = "Verilog code parser"
    VERSION = pyverilog.__version__
    USAGE = "Usage: python memcompose.py file ..."

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
    optparser.add_option("-t", "--top", dest="topmodule",
                         default="TOP", help="Top module, Default=TOP")
    optparser.add_option("--nobind", action="store_true", dest="nobind",
                         default=False, help="No binding traversal, Default=False")
    optparser.add_option("--noreorder", action="store_true", dest="noreorder",
                         default=False, help="No reordering of binding dataflow, Default=False")
    (options, args) = optparser.parse_args()

    filelist = args
    if options.showversion:
        showVersion()

    for f in filelist:
        if not os.path.exists(f):
            raise IOError("file not found: " + f)

    if len(filelist) == 0:
        showVersion()

    mem_data = parser.parse_verilog(filelist,
                            preprocess_include=options.include,
                            preprocess_define=options.define)

    print(mem_data)

    mem_compiler.create_config(mem_data)

    dataflow.dataflow_analysis(filelist, options.topmodule, 
                               mem_data, options.noreorder, options.nobind, 
                               options.include, options.define)




if __name__ == "__main__":
    main()

