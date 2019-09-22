/*
 * Copyright (C) 2019 Intel Corporation. All rights reserved.
 *
 * SPDX-License-Identifier: BSD-3-Clause
 */

#ifndef RDT_H
#define RDT_H

enum {
	RDT_RESOURCE_L3,
	RDT_RESOURCE_L2,

	/* Must be the last */
	RDT_NUM_RESOURCES,
};

/* The intel Resource Director Tech(RDT) based Allocation Tech support */
struct rdt_hw_info {
	bool supported;		/* If L2/L3 CAT supported */
	uint32_t bitmask;	/* Used by other entities */
	uint16_t cbm_len;	/* Length of Cache mask in bits */
	uint16_t clos_max;	/* Maximum CLOS supported, the number of cache masks */

	uint32_t res_id;
};

extern struct rdt_hw_info res_cap_info[];
extern const uint16_t hv_clos;
bool setup_clos(uint16_t pcpu_id);

#define RESID_L3    1U
#define RESID_L2    2U

int32_t init_rdt_cap_info(void);
bool platform_rdt_support(void);
uint64_t clos2pqr_msr(uint16_t clos);

#endif	/* RDT_H */
