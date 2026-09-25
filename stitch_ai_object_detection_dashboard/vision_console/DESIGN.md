---
name: Vision Console
colors:
  surface: '#0f131d'
  surface-dim: '#0f131d'
  surface-bright: '#353944'
  surface-container-lowest: '#0a0e18'
  surface-container-low: '#171b26'
  surface-container: '#1c1f2a'
  surface-container-high: '#262a35'
  surface-container-highest: '#313540'
  on-surface: '#dfe2f1'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#dfe2f1'
  inverse-on-surface: '#2c303b'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#4cd7f6'
  on-secondary: '#003640'
  secondary-container: '#03b5d3'
  on-secondary-container: '#00424e'
  tertiary: '#4edea3'
  on-tertiary: '#003824'
  tertiary-container: '#00a572'
  on-tertiary-container: '#00311f'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#acedff'
  secondary-fixed-dim: '#4cd7f6'
  on-secondary-fixed: '#001f26'
  on-secondary-fixed-variant: '#004e5c'
  tertiary-fixed: '#6ffbbe'
  tertiary-fixed-dim: '#4edea3'
  on-tertiary-fixed: '#002113'
  on-tertiary-fixed-variant: '#005236'
  background: '#0f131d'
  on-background: '#dfe2f1'
  surface-variant: '#313540'
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: 44px
    letterSpacing: -0.025em
  headline-xl-mobile:
    fontFamily: Inter
    fontSize: 28px
    fontWeight: '700'
    lineHeight: 36px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
  label-md:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.01em
  label-sm:
    fontFamily: Inter
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.05em
  code-md:
    fontFamily: JetBrains Mono
    fontSize: 13px
    fontWeight: '500'
    lineHeight: 18px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '500'
    lineHeight: 16px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1rem
  gutter-desktop: 1.5rem
  margin: 1rem
  margin-desktop: 2rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2rem
---

## Brand & Style

This design system establishes an ultra-precise, mission-critical interface architecture designed for real-time computer vision orchestration, model telemetry, and visual spatial computing. Engineered for machine learning researchers, autonomous systems engineers, and video pipeline operators, it replaces visual noise with structural clarity, hyper-legible telemetry, and deterministic UI feedback.

### Visual Style
- **Technical Console Minimalism:** Clean dark surfaces, fine structural grids, and razor-sharp data hierarchy ensure zero distraction when auditing dense detection matrices.
- **Micro-Luminescent Accents:** High-potency electric blue (`#3B82F6`) and cybernetic status emitters punctuate an obsidian-slate substrate, directing attention strictly to inference states, detection thresholds, and bounding anomalies.
- **Glass & Slate Architecture:** Translucent overlays with 1px precision borders reinforce visual depth without obscuring high-resolution camera feeds and bounding overlays.

## Colors

The palette is engineered around an ultra-deep dark mode substrate optimized for sustained spatial scanning, dynamic canvas contrast, and zero eye fatigue.

### Palette Architecture
- **Primary (`#3B82F6`):** Electric Cobalt. Used for active bounding focus, primary controls, primary stepper milestones, and focused interactive states.
- **Secondary (`#06B6D4`):** Cyber Cyan. Represents real-time data streaming, active camera feed streams, and inference pipeline processing indicators.
- **Tertiary (`#10B981`):** Precision Emerald. Designates passed quality thresholds, verified model readiness, high-confidence bounding tags (>90%), and nominal cluster health.
- **Warning (`#F59E0B`):** Amber. Applied to model latency spikes, low-confidence scores (<50%), edge-drift alerts, and non-blocking sensor warnings.
- **Danger (`#EF4444`):** Crimson. Reserved for critical inference pipeline drops, hardware dropouts, dropped frame bursts, and visual classification violations.

### Neutral Layering Hierarchy
- **Canvas Base (`#0B0F19`):** Deep navy obsidian canvas grounding the entire console viewport.
- **Surface Elevation 1 (`#111827`):** Primary card modules, comparison sidebars, and control panels.
- **Surface Elevation 2 (`#1E293B`):** Interactive inputs, nested inspect panels, telemetry chips, and elevated modals.
- **Structural Borders (`#334155` at 60% opacity):** Hairline 1px borders delineating viewport partitions.
- **Text Layers:** `#F8FAFC` (Primary Data/Headlines), `#94A3B8` (Secondary Technical Labels), `#64748B` (Muted Metadata and Axis Units).

## Typography

Typography prioritizes rapid visual parsing under mission-critical conditions. 

- **Display & Headings:** `Inter` in medium, semibold, and bold weights with tight letter-tracking (`-0.015em` to `-0.025em`) produces structured, industrial titles.
- **Telemetry & Numerical Data:** Monospaced numerals (`JetBrains Mono` or tabular figures with `font-feature-settings: "tnum"`) are mandatory across confidence scores, GPU temperatures, spatial coordinates `[x1, y1, x2, y2]`, and latency readouts to prevent horizontal jitter during live telemetry ticks.
- **Labels & Micro-indicators:** `label-sm` utilizes uppercase transformations with `0.05em` tracking for technical status badges and bounding class classifications.

## Layout & Spacing

The layout is built around a fluid, density-optimized 12-column analytical grid capable of collapsing and resizing to preserve viewport visibility for live video feeds and split comparison windows.

### Layout Mechanics
- **Grid Structure:** 12-column responsive fluid grid with 1rem gutters on mobile/tablet, expanding to 1.5rem gutters on desktop (1440px+). Canvas margins transition from 1rem on handheld views to 2rem on high-density operation consoles.
- **Responsive Adaptations:**
  - **Desktop (1280px+):** Tri-pane layout featuring an expandable left pipeline rail (3 cols), central dual-canvas spatial workspace (6 cols), and right-hand telemetry/bounding inspector (3 cols).
  - **Tablet (768px - 1279px):** Bi-pane layout. Central inspection canvas spans full width; telemetry and pipeline controls collapse into tabbed side-drawers or persistent bottom sheets.
  - **Mobile (<768px):** Stacked single-column hierarchy. Telemetry converts to a horizontal scrolling metric bar pinned beneath the detection preview canvas.

## Elevation & Depth

Visual hierarchy uses tonal surface layering coupled with subtle boundary luminance rather than diffuse dropshadows, ensuring camera imagery remains the focal point.

### Surface Hierarchy
- **Level 0 (Base Canvas):** `#0B0F19` flat background.
- **Level 1 (Panel Tier):** `#111827` with 80% opacity, `backdrop-filter: blur(12px)`, and a crisp perimeter outline: `1px solid rgba(51, 65, 85, 0.45)`.
- **Level 2 (Active/Floating Inspector):** `#1E293B` with `backdrop-filter: blur(16px)` and `1px solid rgba(59, 130, 246, 0.3)`.
- **Level 3 (Modal Dialogs & Floating Overlays):** `#0F172A` elevated with a 24px ambient blur: `box-shadow: 0 20px 40px -15px rgba(0, 0, 0, 0.7), 0 0 0 1px rgba(51, 65, 85, 0.6)`.

### Optical Highlights & Emitters
Interactive bounding boxes and verified status indicators feature a targeted inner glow or drop highlight using `0 0 12px rgba(59, 130, 246, 0.35)` or `0 0 10px rgba(16, 185, 129, 0.3)`.

## Shapes

The design system employs **Level 2 Roundedness**, balancing functional discipline with ergonomic UI surfaces.

- **Base Radius (`rounded-md`, 0.5rem):** Applied to buttons, numeric badges, input frames, and coordinate chip tags.
- **Container Radius (`rounded-lg`, 1rem):** Applied to telemetry panels, pipeline step cards, image inspection wrappers, and detection modals.
- **Enclosure Radius (`rounded-xl`, 1.5rem):** Reserved for primary outer canvas viewports, multi-stream view clusters, and parent console shells.
- **Pill Form Factor (`rounded-full`):** Strictly reserved for dynamic pipeline status chips, live model status toggles, and confidence score badges.

## Components

### Buttons
- **Primary:** Solid `#3B82F6` background, `#F8FAFC` label, crisp 0.5rem radius. Hover state: `#2563EB` with `box-shadow: 0 0 16px rgba(59, 130, 246, 0.4)`. Active: `#1D4ED8`.
- **Secondary / Ghost:** `rgba(30, 41, 59, 0.6)` background, `1px solid rgba(51, 65, 85, 0.8)`, text `#94A3B8`. Hover: border `#64748B`, text `#F8FAFC`.
- **Destructive:** `rgba(239, 68, 68, 0.1)` with `1px solid rgba(239, 68, 68, 0.3)`, text `#EF4444`. Hover: `rgba(239, 68, 68, 0.2)`.

### Status Pills & Confidence Badges
- Pill-shaped badge (`rounded-full`, 4px vertical / 10px horizontal padding).
- Format: `inline-flex items-center gap-2`.
- Includes a 6px pulsating dot indicator.
  - **Online/Optimal:** `bg-emerald-500/10 text-emerald-400 border border-emerald-500/20`.
  - **Inference Streaming:** `bg-cyan-500/10 text-cyan-400 border border-cyan-500/20`.
  - **Degraded/Confidence Alert:** `bg-amber-500/10 text-amber-400 border border-amber-500/20`.

### Interactive Stepper Pipeline
- A 4-stage pipeline rail: `[1. Upload] -> [2. Quality Check] -> [3. Object Detection] -> [4. Complete]`.
- Connected via a 2px horizontal rule (`bg-slate-800` when incomplete, `bg-blue-500` with glow when complete).
- Step Nodes: 32px rounded-full containers displaying step index or checkmark icons. Active stage features a radiant perimeter pulse: `ring-4 ring-blue-500/20 border-blue-500 text-blue-400`.

### Side-by-Side Comparison Canvas
- Dual-viewport structure separated by an interactive 2px scrub divider (`bg-blue-500/50` with centered circular drag handle).
- Left: Raw input feed with resolution watermarks.
- Right: Inference output with drawn SVG bounding boxes.
- Bounding box styling: 1.5px solid borders keyed to class color (e.g., `#3B82F6` for pedestrians, `#06B6D4` for vehicles) with an anchored top-left micro-chip displaying `[Class Name | 98.4%]`.

### Inputs & Confidence Sliders
- **Text/Numeric Inputs:** `#111827` background, 1px border `#334155`, text `#F8FAFC`, placeholder `#64748B`. Focus: `border-blue-500 ring-1 ring-blue-500`.
- **Threshold Sliders:** 4px rail (`bg-slate-800`), filled interval (`bg-blue-500`), circular 16px thumb (`bg-white` with `shadow-md shadow-blue-500/50`).

### Technical Inference Metrics Card
- Enclosed panel (`#111827/80`, 1px border `#334155/60`, rounded-lg, 1rem padding).
- Header with model tag (`YOLOv8x`, `Faster R-CNN`) using `label-sm` monospaced chip.
- 2x2 or 4x1 metric grid displaying: Latency (`42ms`), FPS (`24.1`), Device (`NVIDIA RTX 4090`), Precision (`FP16`). Values set in bold `JetBrains Mono` at 18px.