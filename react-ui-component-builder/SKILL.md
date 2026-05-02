---
name: react-ui-component-builder
description: Build high-performance React UI components using Framer Motion for animations, Tailwind CSS for styling, glassmorphism card design, and inclusive hover/focus states. Use when creating or refactoring modern web interfaces.
---

# React UI Component Builder

This skill provides a standardized workflow and set of patterns for building premium, animated React components with a "Hardware/Deep-Tech" aesthetic.

## Design System Specifications

### 1. Glassmorphism Layering
Always use layered transparency to create depth.
- **Base**: `bg-silicon-black/60` or `bg-white/5`
- **Blur**: `backdrop-blur-xl` or `backdrop-blur-2xl`
- **Border**: `border border-white/10` (use `hover:border-white/20` for interaction)
- **Shadow**: `shadow-[0_20px_50px_rgba(0,0,0,0.5)]`

### 2. Framer Motion Patterns
Prioritize lightweight, performant animations.
- **Entrance**: 
  - `initial={{ opacity: 0, y: 10 }}`
  - `animate={{ opacity: 1, y: 0 }}`
  - `transition={{ duration: 0.5, ease: "easeOut" }}`
- **Micro-interactions**:
  - `whileHover={{ scale: 1.01, y: -2 }}`
  - `whileTap={{ scale: 0.98 }}`
- **Viewport Triggers**:
  - `whileInView={{ opacity: 1 }}`
  - `viewport={{ once: true, margin: "-50px" }}`

### 3. Typography & Metallic Effects
- **Metallic Shine**: Use the `.text-shiny-metallic` class for headlines.
- **Monospace Accents**: Use `font-mono` for technical data or labels.
- **Interactive Links**: Always add a `motion.span` underline transition on hover.

### 4. Accessibility (Focus States)
Never ignore focus states. Every interactive element must be keyboard-accessible.
- **Classes**: `focus:outline-none focus:ring-2 focus:ring-neon-cyan/50 focus:ring-offset-2 focus:ring-offset-silicon-black`

## Implementation Workflow

1.  **Define Props**: Use TypeScript interfaces for component props.
2.  **Structure JSX**: Use semantic HTML and Tailwind utility classes.
3.  **Add Motion**: Wrap the outermost element in `motion.div` (or appropriate tag).
4.  **Style Interactions**: Add `hover:` and `focus:` variants.
5.  **Test Responsiveness**: Ensure grid/flex layouts work on all screen sizes.

## Component Templates

### Glass Container
```tsx
import { motion } from 'framer-motion';

export const GlassContainer = ({ children, className = "" }) => (
  <motion.div
    initial={{ opacity: 0, scale: 0.98 }}
    animate={{ opacity: 1, scale: 1 }}
    whileHover={{ borderColor: 'rgba(255, 255, 255, 0.2)' }}
    className={`bg-white/5 backdrop-blur-xl border border-white/10 rounded-3xl p-8 shadow-2xl transition-colors ${className}`}
  >
    {children}
  </motion.div>
);
```

### Metallic Button
```tsx
export const MetallicButton = ({ label, onClick }) => (
  <motion.button
    whileHover={{ scale: 1.05, boxShadow: "0 0 20px rgba(0, 245, 255, 0.4)" }}
    whileTap={{ scale: 0.95 }}
    onClick={onClick}
    className="px-8 py-3 bg-white text-silicon-black font-bold rounded-full hover:bg-oxide-green transition-colors focus:ring-2 focus:ring-neon-cyan focus:ring-offset-2"
  >
    {label}
  </motion.button>
);
```
