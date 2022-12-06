// Dual-Port Block RAM with Two Write Ports
//
// Download: http://www.xilinx.com/txpatches/pub/documentation/misc/xstug_examples.zip
// File: HDL_Coding_Techniques/rams/rams_16.v
//
module dualport_2rw (
    input  clka,
	input clkb,
	input ena,
	input enb,
	input wea,
	input web,
    input  [5:0]  addra,addrb,
    input  [15:0] dia,dib,
    output [15:0] doa,dob);
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
