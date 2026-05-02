# Execution Plan: Gemma-3 Full SoC Integration

## Phase 1: Top-Level Architectural Refactor
- [ ] Task: RTL - Refactor `gpu_system_top_v2.v` to replace legacy compute stages with verified `rmsnorm_vp`, `rope_unit_v2`, and `gated_mlp_da`.
- [ ] Task: RTL - Update `command_processor.v` and `gpu_config_regs.v` to support new Gemma-3 opcodes.
- [ ] Task: Conductor - Phase-Gated Debate 'Phase 1: Top-Level Architectural Refactor'

## Phase 2: Elastic Pipeline Integration
- [ ] Task: RTL - Connect all new stages using the `skid_buffer.v` handshaking protocol for end-to-end elasticity.
- [ ] Task: RTL - Wire `mem_controller_mixed` to the new stage inputs to provide low-latency weight streaming.
- [ ] Task: Conductor - Phase-Gated Debate 'Phase 2: Elastic Pipeline Integration'

## Phase 3: Full-Stack Integration & Visualization
- [ ] Task: Frontend - Integrate Three.js meshes (`<RMSNormNode>`, `<RoPENode>`, `<GatedMLPNode>`) into `GemmaExecutionFlow`.
- [ ] Task: Frontend - Wire up runtime metrics from `useSimulatedMetrics` to these nodes for real-time visualization.
- [ ] Task: Conductor - Phase-Gated Debate 'Phase 3: Full-Stack Integration & Visualization'

## Phase 4: Final SoC Validation & Performance
- [ ] Task: Validation - Run the full 1000-cycle randomized full-system regression suite.
- [ ] Task: Performance - Final verify cycle-accuracy for the integrated pipeline.
- [ ] Task: Conductor - Final SOTA Alignment Debate & Strategy Update.
