/*
 * Copyright (c) 2024 Jesus Minguillon
 * SPDX-License-Identifier: Apache-2.0
 */

module periodCount (
    input  wire         clk1,
    input  wire         clk2,
    input  wire         ena,
    input  wire         rst_n,
    output reg [4:0]    clk_factor
);

  parameter max_clk1_period_count = 8'd127;

  reg [6:0] clk1_period_count;
  
  always @(posedge clk1, negedge rst_n)
    begin
      if(!rst_n)
        begin
          clk1_period_count <= 1;
        end
      else if (ena)
        begin
          if (clk1_period_count < max_clk1_period_count)
            clk1_period_count <= clk1_period_count + 1;
          else
            clk1_period_count <= 1;
        end
    end

  always @(posedge clk2, negedge rst_n)
    begin
      if(!rst_n)
        begin
          clk_factor <= 1;
        end
      else if (ena)
        begin
          clk_factor <= clk1_period_count - 1;
          clk1_period_count <= 1;
        end
    end

endmodule