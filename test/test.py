# SPDX-FileCopyrightText: © 2024 Tiny Tapeout
# SPDX-License-Identifier: Apache-2.0

import cocotb
from cocotb.clock import Clock
from cocotb.triggers import ClockCycles
from cocotb.triggers import Timer
from cocotb.triggers import RisingEdge

@cocotb.test()
async def test_startup(dut):
    dut._log.info("Startup test with reset and internal enable")

    # Set the clock period to 200 ns (5 MHz)
    clock = Clock(dut.clk, 200, units="ns")
    cocotb.start_soon(clock.start())

    # Test
    dut._log.info("rst_n = 0, ui_in[0] = 0")
    dut.ena.value = 1
    dut.ui_in.value = 0
    dut.uio_in.value = 0
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 1)
    await Timer(2, units='ns')
    assert dut.uo_out[0].value == 0
    dut._log.info("uo_out[0] = 0")
    await ClockCycles(dut.clk, 10)
    dut.rst_n.value = 1
    dut._log.info("rst_n = 1, ui_in[0] = 0")
    await RisingEdge(dut.clk)
    await Timer(2, units='ns')
    assert dut.uo_out[0].value == 0
    dut._log.info("uo_out[0] = 0")
    await ClockCycles(dut.clk, 9)
    dut.ui_in[0].value = 1
    dut._log.info("rst_n = 1, ui_in[0] = 1")
    await RisingEdge(dut.clk)
    await Timer(2, units='ns')
    assert dut.uo_out[0].value == 1
    dut._log.info("uo_out[0] = 1")
    await RisingEdge(dut.clk)
    await Timer(2, units='ns')
    assert dut.uo_out[0].value == 0
    dut._log.info("uo_out[0] = 0")
    dut._log.info("Wait until 6 us")
    await ClockCycles(dut.clk, 8)
    dut._log.info("End of startup test")

@cocotb.test()
async def test_reset(dut):
    dut._log.info("Reset test")

    # Set the clock period to 200 ns (5 MHz)
    clock = Clock(dut.clk, 200, units="ns")
    cocotb.start_soon(clock.start())

    # Test
    dut._log.info("rst_n = 0, ui_in[0] = 1")
    dut.rst_n.value = 0
    await Timer(2, units='ns')
    assert dut.uo_out[0].value == 0
    dut._log.info("uo_out[0] = 0")
    assert dut.clk_factor.value == 1
    dut._log.info("clk_factor = 1")
    await RisingEdge(dut.clk)
    await Timer(2, units='ns')
    assert dut.uo_out[0].value == 0
    dut._log.info("uo_out[0] = 0")
    assert dut.clk_factor.value == 1
    dut._log.info("clk_factor = 1")
    await ClockCycles(dut.clk, 9)
    assert dut.uo_out[0].value == 0
    dut._log.info("uo_out[0] = 0")
    assert dut.clk_factor.value == 1
    dut._log.info("clk_factor = 1")
    dut.rst_n.value = 1
    dut._log.info("rst_n = 1, ui_in[0] = 1")
    await RisingEdge(dut.clk)
    await Timer(2, units='ns')
    assert dut.uo_out[0].value == 1
    dut._log.info("uo_out[0] = 1")
    assert dut.clk_factor.value == 1
    dut._log.info("clk_factor = 1")
    await RisingEdge(dut.clk)
    await Timer(2, units='ns')
    assert dut.uo_out[0].value == 0
    dut._log.info("uo_out[0] = 0")
    assert dut.clk_factor.value == 1
    dut._log.info("clk_factor = 1")
    dut._log.info("Wait until 10 us")
    await ClockCycles(dut.clk, 8)
    dut._log.info("End of reset test")

@cocotb.test()
async def test_internal_enable(dut):
    dut._log.info("Internal enable test")

    # Set the clock period to 200 ns (5 MHz)
    clock = Clock(dut.clk, 200, units="ns")
    cocotb.start_soon(clock.start())

    # Test
    dut._log.info("rst_n = 1, ui_in[0] = 0")
    dut.ui_in[0].value = 0
    await ClockCycles(dut.clk, 8)
    dut.ui_in[0].value = 1
    dut._log.info("rst_n = 1, ui_in[0] = 1")
    await RisingEdge(dut.clk)
    await Timer(2, units='ns')
    assert dut.uo_out[0].value == 1
    dut._log.info("uo_out[0] = 1")
    assert dut.clk_factor.value == 2
    dut._log.info("clk_factor = 2")
    dut._log.info("Wait until 13 us")
    await ClockCycles(dut.clk, 6)
    dut._log.info("Reset for 800 ns and wait 200 ns")
    dut.rst_n.value = 0
    await ClockCycles(dut.clk, 4)
    dut.rst_n.value = 1
    await RisingEdge(dut.clk)
    dut._log.info("End of internal enable test")

@cocotb.test()
async def test_period_count(dut):
    dut._log.info("Period count test")

    # Set the clock period to 200 ns (5 MHz)
    clock = Clock(dut.clk, 200, units="ns")
    cocotb.start_soon(clock.start())

    # Test
    await ClockCycles(dut.clk, 2)
    await Timer(2, units='ns')
    assert dut.clk_factor.value == 2
    dut._log.info("clk_factor = 2")
    await ClockCycles(dut.clk, 32)
    await Timer(2, units='ns')
    assert dut.clk_factor.value == 4
    dut._log.info("clk_factor = 4")
    await ClockCycles(dut.clk, 64)
    await Timer(2, units='ns')
    assert dut.clk_factor.value == 8
    dut._log.info("clk_factor = 8")
    await ClockCycles(dut.clk, 128)
    await Timer(2, units='ns')
    assert dut.clk_factor.value == 16
    dut._log.info("clk_factor = 16")
    dut._log.info("Wait until 200 us")
    await ClockCycles(dut.clk, 704)
    dut._log.info("End of period count test")