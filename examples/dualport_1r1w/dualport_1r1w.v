// dest_mem_pointers = [addra]
// source_mem_pointers = [addrb]

module dualport_1r1w (
    input clka,
    input clkb,
	input ena,
	input enb,
    input [9:0] addra,
    input [9:0] addrb,
    input [15:0] dia,
    output [15:0] dob
	);

    reg [15:0] ram [1023:0];
    reg [15:0] dob;

    always @(posedge clka) begin
        if (ena) begin
            ram[addra] <= dia;
        end
    end
    always @(posedge clkb) begin
        if (enb)
            dob <= ram[addrb];
        end
endmodule
