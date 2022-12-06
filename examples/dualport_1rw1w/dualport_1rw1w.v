// dest_mem_pointers = [addra, addrb]
// source_mem_pointers = [addra]

module dualport_1rw1w (
    input  clka,
	input clkb,
	input ena,
	input enb,
	input wea,
    input  [5:0]  addra,addrb,
    input  [15:0] dia,dib,
    output [15:0] doa);

    reg    [15:0] ram [63:0];
    reg    [15:0] doa;
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
		    ram[addrb] <= dib;
end end
endmodule
