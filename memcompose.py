from __future__ import absolute_import
from __future__ import print_function
import sys
import os
from optparse import OptionParser
import pyverilog
import parser
import sram_compiler
import dataflow
import backend

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
    optparser.add_option("-j", "--json", dest="jsonFile",
                         default=None, help="json file for port declaration")
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

    if not os.path.exists(options.jsonFile):
        raise IOError("file not found: " + options.jsonFile)

    ast = parser.parse_verilog(filelist,
                            preprocess_include=options.include,
                            preprocess_define=options.define)

    mem_data = parser.get_mem_data(ast)

    ports = parser.get_ports(ast)

    num_r_ports, num_w_ports, num_rw_ports = dataflow.dataflow_analysis(
                                                filelist,
                                                options.topmodule,
                                                mem_data, options.noreorder,
                                                options.nobind,
                                                options.include,
                                                options.define)

    instance_name = backend.create_config(mem_data, num_r_ports, num_w_ports, num_rw_ports)

    openram_ports = sram_compiler.create_openram_style_ports(
                            num_r_ports,
                            num_w_ports,
                            num_rw_ports)

    module_port_list, module_port_polarity = parser.parse_json(options.jsonFile)

    backend.verilog_writer(
            options.topmodule, ports, instance_name,
            num_r_ports, num_w_ports,
            num_rw_ports, openram_ports,
            module_port_list, module_port_polarity)


if __name__ == "__main__":
    main()

