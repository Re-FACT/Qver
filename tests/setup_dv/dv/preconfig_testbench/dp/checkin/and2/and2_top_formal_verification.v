//-------------------------------------------
//	FPGA Synthesizable Verilog Netlist
//	Description: Verilog netlist for pre-configured FPGA fabric by design: and2
//	Author: Xifan TANG
//	Organization: University of Utah
//	Date: Tue Sep 29 09:50:44 2026
//-------------------------------------------
//----- Default net type -----
`default_nettype none

module and2_top_formal_verification (
input [0:0] a,
input [0:0] b,
output [0:0] c);

// ----- Local wires for FPGA fabric -----
wire [0:63] gfpga_pad_GPIO_PAD_fm;
wire [0:0] ccff_head_fm;
wire [0:0] ccff_tail_fm;
wire [0:0] prog_clk_fm;
wire [0:0] set_fm;
wire [0:0] reset_fm;
wire [0:0] clk_fm;

// ----- FPGA top-level module to be capsulated -----
	fpga_top U0_formal_verification (
		.prog_clk(prog_clk_fm[0]),
		.set(set_fm[0]),
		.reset(reset_fm[0]),
		.clk(clk_fm[0]),
		.gfpga_pad_GPIO_PAD(gfpga_pad_GPIO_PAD_fm[0:63]),
		.ccff_head(ccff_head_fm[0]),
		.ccff_tail(ccff_tail_fm[0]));

// ----- Begin Connect Global ports of FPGA top module -----
	assign set_fm[0] = 1'b0;
	assign reset_fm[0] = 1'b0;
	assign clk_fm[0] = 1'b0;
	assign prog_clk_fm[0] = 1'b0;
// ----- End Connect Global ports of FPGA top module -----

// ----- Link BLIF Benchmark I/Os to FPGA I/Os -----
// ----- Blif Benchmark input a is mapped to FPGA IOPAD gfpga_pad_GPIO_PAD_fm[1] -----
	assign gfpga_pad_GPIO_PAD_fm[1] = a[0];

// ----- Blif Benchmark input b is mapped to FPGA IOPAD gfpga_pad_GPIO_PAD_fm[2] -----
	assign gfpga_pad_GPIO_PAD_fm[2] = b[0];

// ----- Blif Benchmark output c is mapped to FPGA IOPAD gfpga_pad_GPIO_PAD_fm[0] -----
	assign c[0] = gfpga_pad_GPIO_PAD_fm[0];

// ----- Wire unused FPGA I/Os to constants -----
	assign gfpga_pad_GPIO_PAD_fm[3] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[4] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[5] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[6] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[7] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[8] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[9] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[10] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[11] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[12] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[13] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[14] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[15] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[16] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[17] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[18] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[19] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[20] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[21] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[22] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[23] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[24] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[25] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[26] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[27] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[28] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[29] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[30] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[31] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[32] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[33] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[34] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[35] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[36] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[37] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[38] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[39] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[40] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[41] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[42] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[43] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[44] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[45] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[46] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[47] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[48] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[49] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[50] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[51] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[52] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[53] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[54] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[55] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[56] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[57] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[58] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[59] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[60] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[61] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[62] = 1'b0;
	assign gfpga_pad_GPIO_PAD_fm[63] = 1'b0;
endmodule
// ----- END Verilog module for and2_top_formal_verification -----

//----- Default net type -----
`default_nettype wire

