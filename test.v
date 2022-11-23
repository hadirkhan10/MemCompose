module TOP (
  input CLK,
  input RST_X,

  input [7:0] ADDR,
  input WE,
  input [7:0] D,
  output [7:0] Q);

  reg [7:0] mem [0:511];
  reg [7:0] d_ADDR; 
  wire a;
  wire b;
  
  always @(posedge CLK) begin
    if(WE) mem[ADDR] <= D;
    d_ADDR <= ADDR;
  end
  assign Q = mem[d_ADDR];
  
endmodule

//module AnotherTop(
//		input clk,
//		input rst,
//		output flag);
//
//		assign flag = 1;
//endmodule
