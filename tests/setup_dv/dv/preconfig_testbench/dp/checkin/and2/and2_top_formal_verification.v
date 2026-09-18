//-------------------------------------------
//	FPGA Synthesizable Verilog Netlist
//	Description: Verilog netlist for pre-configured FPGA fabric by design: and2
//	Author: Xifan TANG
//	Organization: University of Utah
//	Date: Wed Sep 30 09:18:18 2026
//-------------------------------------------
//----- Default net type -----
`default_nettype none

module and2_top_formal_verification (
input [0:0] a,
input [0:0] b,
output [0:0] c);

// ----- Local wires for FPGA fabric -----
wire [0:17] gfpga_pad_EMBEDDED_IO_SOC_IN_fm;
wire [0:17] gfpga_pad_EMBEDDED_IO_SOC_OUT_fm;
wire [0:17] gfpga_pad_EMBEDDED_IO_SOC_DIR_fm;
wire [0:0] ccff_head_fm;
wire [0:0] ccff_tail_fm;
wire [0:0] prog_clk_fm;
wire [0:0] Test_en_fm;
wire [0:0] reset_fm;
wire [0:0] set_fm;
wire [0:0] clk_fm;

// ----- FPGA top-level module to be capsulated -----
	fpga_top U0_formal_verification (
		.prog_clk(prog_clk_fm[0]),
		.Test_en(Test_en_fm[0]),
		.reset(reset_fm[0]),
		.set(set_fm[0]),
		.clk(clk_fm[0]),
		.gfpga_pad_EMBEDDED_IO_SOC_IN(gfpga_pad_EMBEDDED_IO_SOC_IN_fm[0:17]),
		.gfpga_pad_EMBEDDED_IO_SOC_OUT(gfpga_pad_EMBEDDED_IO_SOC_OUT_fm[0:17]),
		.gfpga_pad_EMBEDDED_IO_SOC_DIR(gfpga_pad_EMBEDDED_IO_SOC_DIR_fm[0:17]),
		.ccff_head(ccff_head_fm[0]),
		.ccff_tail(ccff_tail_fm[0]));

// ----- Begin Connect Global ports of FPGA top module -----
	assign Test_en_fm[0] = 1'b0;
	assign reset_fm[0] = 1'b0;
	assign set_fm[0] = 1'b0;
	assign clk_fm[0] = 1'b0;
	assign prog_clk_fm[0] = 1'b0;
// ----- End Connect Global ports of FPGA top module -----

// ----- Link BLIF Benchmark I/Os to FPGA I/Os -----
// ----- Blif Benchmark input a is mapped to FPGA IOPAD gfpga_pad_EMBEDDED_IO_SOC_IN_fm[16] -----
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[16] = a[0];

// ----- Blif Benchmark input b is mapped to FPGA IOPAD gfpga_pad_EMBEDDED_IO_SOC_IN_fm[17] -----
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[17] = b[0];

// ----- Blif Benchmark output c is mapped to FPGA IOPAD gfpga_pad_EMBEDDED_IO_SOC_OUT_fm[0] -----
	assign c[0] = gfpga_pad_EMBEDDED_IO_SOC_OUT_fm[0];

// ----- Wire unused FPGA I/Os to constants -----
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[0] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[1] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[2] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[3] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[4] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[5] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[6] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[7] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[8] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[9] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[10] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[11] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[12] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[13] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[14] = 1'b0;
	assign gfpga_pad_EMBEDDED_IO_SOC_IN_fm[15] = 1'b0;

endmodule
// ----- END Verilog module for and2_top_formal_verification -----

//----- Default net type -----
`default_nettype wire

