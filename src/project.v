/*
 * Copyright (c) 2024 Jesus Minguillon
 * SPDX-License-Identifier: Apache-2.0
 */

`default_nettype none

module tt_um_JesusMinguillon_freqSweep (
    input  wire [7:0] ui_in,    // Dedicated inputs
    output wire [7:0] uo_out,   // Dedicated outputs
    input  wire [7:0] uio_in,   // IOs: Input path
    output wire [7:0] uio_out,  // IOs: Output path
    output wire [7:0] uio_oe,   // IOs: Enable path (active high: 0=input, 1=output)
    input  wire       ena,      // Always 1 when the design is powered, so you can ignore it
    input  wire       clk,      // Clock
    input  wire       rst_n     // Reset_n - low to reset
);

  parameter max_periods = 4'd15;              // Number of periods before doubling clk_out period
  parameter max_clk_out_period_factor = 4'd8; // Maximum clk_out period factor. This factor is (period(clk_out)/period(clk))/2 

  reg clk_out;
  reg [3:0] clk_period_count;
  reg [3:0] clk_out_period_count;
  reg [3:0] clk_out_period_factor;

  always @(posedge clk, negedge rst_n)
    begin
      if(!rst_n)
        begin
          clk_out <= 0;
          clk_period_count <= 1;
        end
      else if (ui_in[0]) // ui_in[0] is used as internal enable
        begin
          if (clk_period_count < clk_out_period_factor)
            clk_period_count <= clk_period_count + 1;
          else
            begin
              clk_out <= ~clk_out;
              clk_period_count <= 1;
            end
        end
    end

  always @(posedge clk_out, negedge rst_n)
    begin
      if(!rst_n)
        begin
          clk_out_period_count <= 0;
          clk_out_period_factor <= 1;
        end
      else if (ui_in[0]) // ui_in[0] is used as internal enable
        begin
          if (clk_out_period_count < max_periods)
            clk_out_period_count <= clk_out_period_count + 1;
          else
            begin
              clk_out_period_count <= 1;
              if (clk_out_period_factor < max_clk_out_period_factor)
                clk_out_period_factor <= clk_out_period_factor << 1;
              else
                clk_out_period_factor <= 1;
            end
        end
    end

  // All output pins must be assigned. If not used, assign to 0.
  assign uo_out[0] = clk_out;
  assign uo_out[7:1] = 0; 
  assign uio_out = 0;
  assign uio_oe = 0;

  // List all unused inputs to prevent warnings
  wire _unused = &{ui_in[7:1], uio_in, ena, 1'b0};

endmodule
