---
name: Midnight Synapse
colors:
  surface: '#0e1321'
  surface-dim: '#0e1321'
  surface-bright: '#343948'
  surface-container-lowest: '#090e1c'
  surface-container-low: '#161b2a'
  surface-container: '#1a1f2e'
  surface-container-high: '#252a39'
  surface-container-highest: '#303444'
  on-surface: '#dee2f6'
  on-surface-variant: '#bcc9cd'
  inverse-surface: '#dee2f6'
  inverse-on-surface: '#2b303f'
  outline: '#869397'
  outline-variant: '#3d494c'
  surface-tint: '#4cd7f6'
  primary: '#4cd7f6'
  on-primary: '#003640'
  primary-container: '#06b6d4'
  on-primary-container: '#00424f'
  inverse-primary: '#00687a'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#c0c1ff'
  on-tertiary: '#1000a9'
  tertiary-container: '#9a9dff'
  on-tertiary-container: '#211cb4'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#acedff'
  primary-fixed-dim: '#4cd7f6'
  on-primary-fixed: '#001f26'
  on-primary-fixed-variant: '#004e5c'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#e1e0ff'
  tertiary-fixed-dim: '#c0c1ff'
  on-tertiary-fixed: '#07006c'
  on-tertiary-fixed-variant: '#2f2ebe'
  background: '#0e1321'
  on-background: '#dee2f6'
  surface-variant: '#303444'
typography:
  headline-xl:
    fontFamily: Outfit
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.03em
  headline-xl-mobile:
    fontFamily: Outfit
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Outfit
    fontSize: 36px
    fontWeight: '600'
    lineHeight: 44px
    letterSpacing: -0.025em
  headline-lg-mobile:
    fontFamily: Outfit
    fontSize: 26px
    fontWeight: '600'
    lineHeight: 34px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Outfit
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.015em
  headline-sm:
    fontFamily: Outfit
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
    letterSpacing: -0.01em
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 26px
    letterSpacing: -0.005em
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 22px
    letterSpacing: 0em
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 18px
    letterSpacing: 0.005em
  label-lg:
    fontFamily: Outfit
    fontSize: 14px
    fontWeight: '600'
    lineHeight: 20px
    letterSpacing: 0.02em
  label-md:
    fontFamily: Outfit
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.04em
  label-sm:
    fontFamily: Outfit
    fontSize: 10px
    fontWeight: '700'
    lineHeight: 14px
    letterSpacing: 0.08em
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  gutter: 1.5rem
  gutter-sm: 1rem
  margin: 2rem
  margin-sm: 1rem
  space-xs: 0.25rem
  space-sm: 0.5rem
  space-md: 1rem
  space-lg: 1.5rem
  space-xl: 2.5rem
---

## Brand & Style

This design system embodies an intelligent, executive-grade AI networking platform. The aesthetic pairs deep midnight space with radiant kinetic currents, positioning the interface as a high-velocity command center for professional relationship building. 

The design narrative merges **Refined Glassmorphism** with a **Cyber-Executive Minimalist** core:
- **Atmospheric Immersion:** Deep navy and midnight obsidian grounds provide endless depth, minimizing optical fatigue while making signal-bearing data pop.
- **Luminescent Telemetry:** Emerald, cyan, and electric violet gradients serve as indicators of AI synthesis, high-relevance match scoring, and live networking pipelines.
- **Glass Precision:** Translucent frosted panels (`backdrop-filter: blur(16px)`) with ultra-fine boundary strokes simulate precision-machined optical instruments.
- **Emotional Resonance:** High agency, frictionless intelligence, stealth luxury, and authoritative control.

## Colors

The palette leverages high-contrast luminescence over multi-tiered dark foundation slates:

- **Foundation Backgrounds:**
  - Base Void: `#0A0F1D` (Deep canvas root)
  - Surface Midnight: `#0F172A` (Elevated modules, navigation docks)
  - Surface Raised: `#1E293B` (Dropdown menus, flyout inspectors)

- **Accents & Gradients:**
  - **Primary (Cyan Beam - `#06B6D4`):** Real-time interaction triggers, active state signals, and focal navigation anchors.
  - **Secondary (Emerald Pulse - `#10B981`):** High match affinity scores, successful connection requests, and positive health metrics.
  - **Tertiary (Electric Indigo - `#6366F1`):** Autonomous AI background workflows, message synthesis engines, and insight highlights.
  - **Kinetic Gradient:** `linear-gradient(135deg, #10B981 0%, #06B6D4 50%, #6366F1 100%)` utilized exclusively for core AI actions, match strength rings, and high-impact hero metrics.

- **Text & Contrast System:**
  - Pure White (`#FFFFFF`): Primary headers, active states, key titles.
  - Slate High (`#E2E8F0`): Primary body text, readable metrics.
  - Slate Muted (`#94A3B8`): Meta captions, secondary attributes, timestamps.
  - Slate Ghost (`#475569`): Inactive iconography, placeholder fields.

## Typography

The typographic hierarchy couples **Outfit** for structural headings and labels with **Inter** for sustained legibility within content density:

- **Display & Headlines (Outfit):** Delivers geometric precision and crisp optical cuts. Used with tighter tracking (`-0.02em` to `-0.03em`) to yield a forward-leaning, technological presence.
- **Body & Data Reads (Inter):** Maximizes neutral readability across dense feeds, conversation logs, network summaries, and AI reasoning streams.
- **Labels, Badges, & Metrics (Outfit):** Set at medium-to-bold weights with expanded tracking for uppercase categories, micro-tags, and quantitative network telemetry.

## Layout & Spacing

The spatial grid is organized around an **8-point structural system** configured for multi-pane AI workstation dashboards:

- **Grid Architecture:** 12-column responsive fluid grid bounded at `1440px` maximum viewport width for ergonomic focus.
  - **Desktop (≥ 1280px):** 12 columns, `1.5rem` (`24px`) gutters, `2rem` (`32px`) margins. Sidebar docked at `280px` fixed, dynamic canvas center, persistent side-drawer inspector (`380px`).
  - **Tablet (768px - 1279px):** 8 columns, `1rem` (`16px`) gutters, `1.5rem` (`24px`) margins. Rail-collapsed navigation (`72px`), collapsible sliding inspectors.
  - **Mobile (< 768px):** 4 columns, `1rem` (`16px`) gutters, `1rem` (`16px`) canvas margin. Bottom-oriented thumb navigation bar, single-column stacked vertical cards.

- **Component Gap Rhythm:**
  - Micro relationships (icon-to-label, badge elements): `space-xs` (4px) to `space-sm` (8px).
  - Form items, inner-card metadata groups: `space-md` (16px).
  - Card block padding, section separation: `space-lg` (24px).
  - Major view modules, dashboard panel decoupling: `space-xl` (40px).

## Elevation & Depth

Depth is established through frosted refractive glass, boundary luminescence, and radial color diffusion rather than traditional drop shadows:

- **Level 0 (Canvas):** Pure base obsidian `#0A0F1D`.
- **Level 1 (Frosted Glass Cards):** Background `rgba(255, 255, 255, 0.03)`, backdrop filter `blur(16px)`, surrounded by a hairline boundary `1px solid rgba(255, 255, 255, 0.08)`.
- **Level 2 (Interactive Floating Modules / Hover States):** Background `rgba(255, 255, 255, 0.06)`, backdrop filter `blur(24px)`. Border brightens to `1px solid rgba(6, 182, 212, 0.35)`. Ambient underglow: `0 8px 32px -4px rgba(6, 182, 212, 0.12)`.
- **Level 3 (Modal Dialogs & Context Overlays):** Solidified glass `rgba(15, 23, 42, 0.85)`, backdrop filter `blur(32px)`, border `1px solid rgba(255, 255, 255, 0.15)`. Ambient multi-color drop shadow: `0 20px 48px -8px rgba(0, 0, 0, 0.7), 0 0 24px 0 rgba(99, 102, 241, 0.15)`.
- **Atmospheric Glows:** Passive soft radial gradients (`radial-gradient(circle at 50% 0%, rgba(6, 182, 212, 0.08), transparent 70%)`) anchored behind top-level cards and stats counters to provide visual breathing room.

## Shapes

A balanced `roundedness: 2` scale enforces a modern hardware feel, pairing structural cards with pill-shaped control elements:

- **Containers & Glass Panels:** Default radius `0.75rem` (`12px`) for nested inner elements, `1rem` (`16px`) for primary dashboard cards, and `1.5rem` (`24px`) for high-level viewport containers.
- **Interactive Controls:** All primary buttons, filter tags, search bars, and intelligence pill indicators utilize full pill bounds (`9999px`) to contrast against geometric card structures.
- **Micro-Indicators:** 2px circular status pings, 4px rounded indicators on progress steps.

## Components

### Buttons
- **Primary Kinetic Glow Button:**
  - Background: `linear-gradient(135deg, #10B981 0%, #06B6D4 50%, #6366F1 100%)`.
  - Content: Pure white `#FFFFFF`, `Outfit` font, SemiBold (600).
  - Shape: Pill radius (`9999px`), padding: `0.75rem 1.5rem`.
  - Shadow/Effect: `0 0 20px rgba(6, 182, 212, 0.35)`. On hover: `0 0 28px rgba(6, 182, 212, 0.55)`, scale `1.02`.
- **Secondary Ghost Glass Button:**
  - Background: `rgba(255, 255, 255, 0.04)`.
  - Border: `1px solid rgba(255, 255, 255, 0.1)`.
  - Color: `#E2E8F0`. Hover: `background: rgba(255, 255, 255, 0.08); border-color: rgba(255, 255, 255, 0.25)`.

### Badge Pills & Affinity Meters
- Match Affinity badges utilize pill enclosures (`padding: 0.25rem 0.75rem`).
- High-match (>90%): `background: rgba(16, 185, 129, 0.12)`, `border: 1px solid rgba(16, 185, 129, 0.3)`, text `#10B981`.
- AI Processing / Suggestion: `background: rgba(99, 102, 241, 0.12)`, `border: 1px solid rgba(99, 102, 241, 0.3)`, text `#818CF8`.

### Input Fields & Search Bars
- Background: `rgba(15, 23, 42, 0.6)`.
- Border: `1px solid rgba(255, 255, 255, 0.08)`.
- Radius: Pill (`9999px`) for global search; `0.75rem` (`12px`) for conversational and edit inputs.
- Active Focus: `border-color: #06B6D4`, ring shadow `0 0 0 3px rgba(6, 182, 212, 0.15)`.

### Cards & Network Dossiers
- Background: `rgba(255, 255, 255, 0.03)`, `backdrop-filter: blur(16px)`.
- Stroke: `1px solid rgba(255, 255, 255, 0.07)`.
- Radius: `1rem` (`16px`).
- Padding: `1.5rem` (`24px`).
- Hover Transition: Border shifts to `rgba(6, 182, 212, 0.4)` accompanied by a soft background ramp to `rgba(255, 255, 255, 0.05)`.

### Checkboxes & Switches
- **Checkboxes:** Base `18px x 18px` square with `4px` corner radius. Checked state fills with `#06B6D4`, white checkmark, and a subtle cyan illumination.
- **Switches:** Track is pill-shaped (`40px x 22px`) in `rgba(255, 255, 255, 0.1)`. Active track fills with `#10B981`. Knob is `#FFFFFF` with slight ambient shadow.

### AI Insight Cards (Specialized Component)
- Elevated card with an inset neon border highlight at the top edge (`2px` gradient stroke: `#10B981` to `#06B6D4`).
- Includes a miniature pulse indicator dot (`#10B981` with infinite soft beacon ping) indicating live autonomous parsing.