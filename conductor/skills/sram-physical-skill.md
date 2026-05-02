# Skill: sram-physical-skill

## Overview
This skill governs the 'SRAM/Physical' agent stream. It enforces thermal-aware floorplanning, area-efficient RTL, and structural tiling.

## SOPs
1. **16x8 Tiling Rule:** All SRAM implementations must adhere to the 160KB-per-bank tiling structure established in Phase 1.
2. **Thermal-Awareness:** Interleave memory banks in a checkerboard pattern. No two high-activity banks can be placed in adjacent tiles.
3. **Elastic Boundary:** Every compute block boundary MUST utilize a `skid_buffer` (`ready/valid`) to ensure the design remains pipelined and area-efficient.
4. **Artifact Logging:** Append the generated RTL and synthesis reports to `docs/SWARM_REPORT_CARD.md` with SHA-256 hashes for all synthesized `.v` files.
