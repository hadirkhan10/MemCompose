// dest_mem_pointers = [addra]
// source_mem_pointers = [addra, addrb]

module dualport_1rw1r (
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
