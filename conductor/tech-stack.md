# Technology Stack: BitbyBit Tri-Fold Prototype

## Hardware / Core Engine (Backend)
- **Hardware Description Language (HDL):** Verilog-2005 (`.v` files)
- **Simulation & Verification:** Icarus Verilog (`iverilog`), GTKWave (for `.vcd` viewing)
- **Data & Precision:** Q8.8 Fixed-Point, Ternary/1.58-bit, 2:4 Structured Sparsity

## Scripting & Inference (Middleware)
- **Language:** Python 3.10+
- **Libraries:** NumPy (for golden models and weights generation)
- **Models Targeted:** NanoGPT, OPT-125M, Gemma-3 270M (Planned)

## Web Dashboard (Frontend)
- **Project Name:** bitbybit
- **Framework:** Next.js 14 (App Router)
- **Language:** TypeScript
- **Styling:** Tailwind CSS, `shadcn/ui`
- **Visualization:** Three.js (`@react-three/fiber`, `@react-three/drei`)
- **Testing:** Playwright, Vitest