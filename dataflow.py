from pyverilog.dataflow.dataflow_analyzer import VerilogDataflowAnalyzer
from pyverilog.dataflow.optimizer import VerilogDataflowOptimizer
from pyverilog.dataflow.walker import VerilogDataflowWalker
from collections import defaultdict




def dataflow_analysis(file, topmodule, mem_data, noreorder, nobind, include, define):

    analyzer = VerilogDataflowAnalyzer(file, topmodule,
                                       noreorder=noreorder,
                                       nobind=nobind,
                                       preprocess_include=include,
                                       preprocess_define=define)

    analyzer.generate()
    terms = analyzer.getTerms()
    binddict = analyzer.getBinddict()

    walker = VerilogDataflowWalker(topmodule, terms, binddict, None, None, None)

    # single port - RW
    # ram: {
    #   pointer: addr,
    #   cond: en,
    #   en: {   truenode: {
    #               cond: we
    #               we: {   truenode: di,
    #                       falsenode: None
    #               }
    #           },
    #           falsenode: None
    #       }
    # },
    # dout: {
    #   cond: en,
    #   en: {   truenode: {
    #               cond: we
    #               we: {   truenode: None,
    #                       falsenode: (ram, addr)
    #                   }
    #           },
    #           falsenode: None
    #       }
    # }
    #       

    # dual port - 
    # ram: {
    #   pointer: addra,
    #   cond: ena,
    #   ena: {   truenode: {
    #               cond: wea
    #               wea: {   truenode: dia,
    #                       falsenode: None
    #               }
    #           },
    #           falsenode: None
    #       }
    # },
    # dout: {
    #   cond: enb,
    #   enb: {  truenode: (ram, addrb) 
    #           falsenode: None
    #       }
    # }
    #       

    # {
    #   chip_select: ena
    #   write_en: wea
    # }



    # single port configurations can be:
    #   1. 1rw

    # dual port configurations can be:
    #   1. 1r1w
    #   2. 1rw1r
    #   3. 1rw1w
    #   4. 2rw

    dest_mem_pointers = []
    source_mem_pointers = []
    num_rw_ports = 0
    num_w_ports = 0
    num_r_ports = 0


    def walkerForBranch(branch_node, dest):
        truenode, cond, falsenode = branch_node.children()
        if str(type(truenode)) == "<class 'pyverilog.dataflow.dataflow.DFBranch'>":
            walkerForBranch(truenode, dest)

        elif str(type(truenode)) == "<class 'pyverilog.dataflow.dataflow.DFTerminal'>":
            print(dest, "is written by",truenode.name)

        elif str(type(truenode)) == "<class 'pyverilog.dataflow.dataflow.DFPointer'>":
            # reading from a memory
            var, ptr = truenode.children()
            source_mem_pointers.append(str(ptr))
            print(f"{dest} is written by {var}[{ptr}]")


        if str(type(falsenode)) == "<class 'pyverilog.dataflow.dataflow.DFBranch'>":
            walkerForBranch(falsenode, dest)
        elif str(type(falsenode)) == "<class 'pyverilog.dataflow.dataflow.DFTerminal'>":
            print(dest, "is written by",falsenode.name)
        elif str(type(falsenode)) == "<class 'pyverilog.dataflow.dataflow.DFPointer'>":
            # reading from a memory
            var, ptr = falsenode.children()
            source_mem_pointers.append(str(ptr))
            print(f"{dest} is written by {var}[{ptr}]")


    for key, value in binddict.items():
        for v in value:
            print(v.tostr())

            if str(v.dest) in list(mem_data.keys()):
                mem_ptr = str(v.ptr)
                mem_name = str(v.dest)
                dest_mem_pointers.append(mem_ptr)
                print(v.ptr)


            tree = v.tree
            walked_tree = walker.walkTree(tree)
            if str(type(walked_tree)) == "<class 'pyverilog.dataflow.dataflow.DFBranch'>":
                walkerForBranch(walked_tree, v.dest)

    if dest_mem_pointers == source_mem_pointers:
        num_rw_ports = len(dest_mem_pointers)
        print(f"We have a {num_rw_ports}-RW configuration") 
    else:
        if len(dest_mem_pointers) > len(source_mem_pointers):
            # a scenario where config could be 1rw1w,
            # because of the extra dest_mem_pointer
            for val in dest_mem_pointers:
                if val in source_mem_pointers:
                    num_rw_ports = 1
                    num_w_ports = 1
        elif len(source_mem_pointers) > len(dest_mem_pointers):
            # a scenario where config could be 1rw1r,
            # because of the extra source_mem_pointer
            for val in source_mem_pointers:
                if val in dest_mem_pointers:
                    num_rw_ports = 1
                    num_r_ports = 1
        else:
            # a scenario where config could be 1r1w,
            num_r_ports = 1
            num_w_ports = 1

    print(f"Number of read-port: {num_r_ports}")
    print(f"Number of write-port: {num_w_ports}")
    print(f"Number of read-write-port: {num_rw_ports}")



