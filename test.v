// Single-Port Block RAM No-Change Mode
// File: rams_sp_nc.v
//module rams_sp_nc (clk, we, en, addr, di, dout);
//    input clk;
//    input we;
//    input en;
//    input [9:0] addr;
//    input [15:0] di;
//    output [15:0] dout;
//    reg [15:0] RAM [1023:0];
//    reg [15:0] dout;
//    .memcompose begin
//    	clock = clk
//    .memcompose end
//    always @(posedge clk) begin
//        if (en) begin
//            if (we)
//		        RAM[addr] <= di;
//		    else
//		        dout <= RAM[addr];
//		end
//    end
//endmodule

// ****** OPENRAM LINKING ********
//module rams_sp_nc (clk, we, en, addr, di, dout);
//    input clk;
//    input we;
//    input en;
//    input [9:0] addr;
//    input [15:0] di;
//    * slight modification here. All outputs should be defined as reg
//    output [15:0] dout;
//    reg [15:0] dout;
//    * will need to add a wire here using the output name
//    * this action will be repeated for each output of the memory
//    wire [15:0] dout_wire;
//
//    * will need to generate this instantiation 
//    sram_8_512_scn4m_subm mem0 (
//    	.clk0(clk),
//    	.csb0(~en),
//    	.web0(~we),
//    	.addr0(addr),
//    	.din0(di),
//    	.dout0(dout_wire)
//    	);
//
//    	* will need to generate one always block here
//    	always @(posedge clk) begin
//    		// this action will be repeated for each output of the memory
//    		dout <= dout_wire;
//    	end
//endmodule



// Simple Dual-Port Block RAM with One Clock
// File: simple_dual_one_clock.v
//
// dest_mem_pointers = [addra]
// source_mem_pointers = [addrb]
//
//module simple_dual_one_clock (
//    input clk,
//	input ena,
//	input enb,
//	input wea,
//    input [9:0] addra,
//    input [9:0] addrb,
//    input [15:0] dia,
//    output [15:0] dob
//	);
//
//    reg [15:0] ram [1023:0];
//    reg [15:0] dob;
//
//	// .memcompose begin
//	// chip_select = ena , enb
//	// write_en = wea 
//	// addr = addra, addrb
//	// clock = clk
//	// 
//	// .memcompose end
//    always @(posedge clk) begin
//        if (ena) begin
//            if (wea)
//                ram[addra] <= dia;
//        end
//    end
//    always @(posedge clk) begin
//        if (enb)
//            dob <= ram[addrb];
//        end
//endmodule

// dest_mem_pointers = [addra, addrb]
// source_mem_pointers = [addra]
//module v_rams_16_1rw_1w (clka,clkb,ena,enb,wea,web,addra,addrb,dia,dib,doa);
//    input  clka,clkb,ena,enb,wea,web;
//    input  [5:0]  addra,addrb;
//    input  [15:0] dia,dib;
//    output [15:0] doa;
//    reg    [15:0] ram [63:0];
//    reg    [15:0] doa;
//    always @(posedge clka) begin
//        if (ena)
//        begin
//            if (wea)
//                ram[addra] <= dia;
//            doa <= ram[addra];
//		end 
//    end
//    always @(posedge clkb) begin
//        if (enb)
//        begin
//            if (web)
//                ram[addrb] <= dib;
//end end
//endmodule

// dest_mem_pointers = [addra]
// source_mem_pointers = [addra, addrb]
module v_rams_16_1rw_1r (
    input  clka,
	input clkb,
	input ena,
	input enb,
	input wea,
    input  [5:0]  addra,
    input [5:0] addrb,
    input  [15:0] dia,
    output [15:0] doa,
	output [15:0] dob
	);
    reg    [15:0] ram [63:0];
    reg    [15:0] doa,dob;


//	wire out_wire;
//	hello mymodule (
//			.in(clka),
//			.out(out_wire)
//	);

    always @(posedge clka) begin
        if (ena)
        begin
            if (wea)
                ram[addra] <= dia;
            doa <= ram[addra];
		end 
    end
    always @(posedge clkb) begin
        if (enb) begin
            dob <= ram[addrb];
		end 
    end
endmodule

module hello (
		input in,
		output out
);
assign out = in;
endmodule
//
// Dual-Port Block RAM with Two Write Ports
//
// Download: http://www.xilinx.com/txpatches/pub/documentation/misc/xstug_examples.zip
// File: HDL_Coding_Techniques/rams/rams_16.v
//
//module v_rams_16 (clka,clkb,ena,enb,wea,web,addra,addrb,dia,dib,doa,dob);
//    input  clka,clkb,ena,enb,wea,web;
//    input  [5:0]  addra,addrb;
//    input  [15:0] dia,dib;
//    output [15:0] doa,dob;
//    reg    [15:0] ram [63:0];
//    reg    [15:0] doa,dob;
//    always @(posedge clka) begin
//        if (ena)
//        begin
//            if (wea)
//                ram[addra] <= dia;
//            doa <= ram[addra];
//		end 
//    end
//    always @(posedge clkb) begin
//        if (enb)
//        begin
//            if (web)
//                ram[addrb] <= dib;
//            dob <= ram[addrb];
//end end
//endmodule
