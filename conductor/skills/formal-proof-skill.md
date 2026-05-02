# Skill: formal-proof-skill

## Overview
This skill governs the 'Formal/Logic' agent stream. It enforces rigorous SVA implementation and mathematical deadlock-free proofs for elastic pipelines.

## SOPs
1. **SVA First:** No RTL logic can be implemented without corresponding SVA properties defined in `.sv` files.
2. **Formal Liveness:** Every state-machine transition MUST be formally proven to be deadlock-free using a bounded model check (min depth: 20).
3. **Artifact Logging:** Upon completion of a proof, generate a report with the formal tool output and append it to `docs/SWARM_REPORT_CARD.md` with a SHA-256 hash of the SVA proof file.
4. **Failure Protocol:** If any proof fails, halt and generate a 'Deadlock/Safety Bug' ticket.
