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
//    always @(posedge clk) begin
//        if (en) begin
//            if (we)
//		        RAM[addr] <= di;
//		    else
//		        dout <= RAM[addr];
//		end
//    end
//endmodule

// Simple Dual-Port Block RAM with One Clock
// File: simple_dual_one_clock.v
//
// dest_mem_pointers = [addra]
// source_mem_pointers = [addrb]
//
//module simple_dual_one_clock (clk,ena,enb,wea,addra,addrb,dia,dob);
//    input clk,ena,enb,wea;
//    input [9:0] addra,addrb;
//    input [15:0] dia;
//    output [15:0] dob;
//    reg [15:0] ram [1023:0];
//    reg [15:0] doa,dob;
//
//	// .memcompose begin
//	// chip_select = ena , enb
//	// write_en = wea 
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
//module v_rams_16_1rw_1r (clka,clkb,ena,enb,wea,addra,addrb,dia,doa,dob);
//    input  clka,clkb,ena,enb,wea;
//    input  [5:0]  addra,addrb;
//    input  [15:0] dia;
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
//        if (enb) begin
//            dob <= ram[addrb];
//		end 
//    end
//endmodule
//
// Dual-Port Block RAM with Two Write Ports
//
// Download: http://www.xilinx.com/txpatches/pub/documentation/misc/xstug_examples.zip
// File: HDL_Coding_Techniques/rams/rams_16.v
//
module v_rams_16 (clka,clkb,ena,enb,wea,web,addra,addrb,dia,dib,doa,dob);
    input  clka,clkb,ena,enb,wea,web;
    input  [5:0]  addra,addrb;
    input  [15:0] dia,dib;
    output [15:0] doa,dob;
    reg    [15:0] ram [63:0];
    reg    [15:0] doa,dob;
    always @(posedge clka) begin
        if (ena)
        begin
            if (wea)
                ram[addra] <= dia;
            doa <= ram[addra];
		end 
    end
    always @(posedge clkb) begin
        if (enb)
        begin
            if (web)
                ram[addrb] <= dib;
            dob <= ram[addrb];
end end
endmodule
