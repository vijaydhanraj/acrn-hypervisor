# Copyright (C) 2019 Intel Corporation. All rights reserved.
#
# SPDX-License-Identifier: BSD-3-Clause
#

import parser_lib

RDT_TYPE = {
        "L2":4,
        "L3":2
    }


def dump_cpuid_reg(cmd, reg):
    """execute the cmd of cpuid, and return the register value by reg
    :param cmd: command what can be executed in shell
    :param reg: register name
    """
    res = parser_lib.cmd_execute(cmd)
    if reg == "ebx":
        idx = 3

    if reg == "edx":
        idx = 5

    while True:
        line = parser_lib.decode_stdout(res)

        if not line:
            break

        if len(line.split()) <= 2:
            continue

        reg_value = line.split()[idx].split('=')[1]

        if reg == "ebx":
            cache_t = []
            if int(reg_value, 16) & RDT_TYPE['L2'] != 0:
                cache_t.append("L2")
                break

            if int(reg_value, 16) & RDT_TYPE['L3'] != 0:
                cache_t.append("L3")

                break
        elif reg == "edx":
            cache_t = int(reg_value, 16) + 1
            break

    return cache_t


def get_clos_info():
    """Get clos max and clos cache type"""
    rdt_clos_max = []
    rdt_res = []
    cmd = "cpuid -r -l 0x10"
    rdt_res = dump_cpuid_reg(cmd, "ebx")

    if len(rdt_res) == 0:
        parser_lib.print_yel("Resource Allocation is not supported!")
    else:
        for i in range(len(rdt_res)):
            if rdt_res[i] == "L2":
                cmd = "cpuid -r -l 0x10 --subleaf 2"
                rdt_clos_max.append(dump_cpuid_reg(cmd, "edx"))

            if rdt_res[i] == "L3":
                cmd = "cpuid -r -l 0x10 --subleaf 1"
                rdt_clos_max.append(dump_cpuid_reg(cmd, "edx"))

    return (rdt_res, rdt_clos_max)


def generate_info(board_info):
    """Generate clos information
    :param board_info: this is the file which stores the hardware board information
    """
    (rdt_res, rdt_res_clos_max) = get_clos_info()

    with open(board_info, 'a+') as config:
        print("\t<CLOS_INFO>", file=config)
        print("\trdt resources supported:", ', '.join(rdt_res), file=config)
        print("\trdt resource clos max:",str(rdt_res_clos_max).strip('[]'), file=config)
        print("\t</CLOS_INFO>\n", file=config)
