module test_module(
    input clk,
    input rst,
    input data_in,
    output reg data_out
);

  always @(posedge clk or posedge rst) begin
    if (rst)
      data_out <= 1'b0;
    else
      data_out <= data_in;
  end

endmodule
