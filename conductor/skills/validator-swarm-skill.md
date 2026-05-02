# Skill: validator-swarm-skill

## Overview
This skill governs the 'Independent Validator' stream. It is the ultimate gatekeeper, enforcing "Perfect Validation" and auditing the work of Streams A and B.

## SOPs
1. **Perfect Validation:** All modules MUST achieve 100% parity with Python golden hex files. Any mismatch is a FAIL.
2. **Stress-Load Check:** Run randomized regression with backpressure (asserting `ready` randomly) for at least 5000 cycles.
3. **Cross-Stream Audit:** Verify that all SHA-256 hashes reported by Streams A and B match the actual files on disk. 
4. **Final Gatekeeping:** If ANY artifact hash mismatch or validation error is detected, issue an immediate "System Halt" and flag the responsible agent by Stream ID.
