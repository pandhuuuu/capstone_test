---
name: Disaster Command Center
colors:
  surface: '#f7f9fb'
  surface-dim: '#d8dadc'
  surface-bright: '#f7f9fb'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f2f4f6'
  surface-container: '#eceef0'
  surface-container-high: '#e6e8ea'
  surface-container-highest: '#e0e3e5'
  on-surface: '#191c1e'
  on-surface-variant: '#44474c'
  inverse-surface: '#2d3133'
  inverse-on-surface: '#eff1f3'
  outline: '#75777d'
  outline-variant: '#c5c6cd'
  surface-tint: '#525f75'
  primary: '#000000'
  on-primary: '#ffffff'
  primary-container: '#0e1c2f'
  on-primary-container: '#77849c'
  inverse-primary: '#bac7e1'
  secondary: '#a73a00'
  on-secondary: '#ffffff'
  secondary-container: '#fd651e'
  on-secondary-container: '#571a00'
  tertiary: '#000000'
  on-tertiary: '#ffffff'
  tertiary-container: '#111c2d'
  on-tertiary-container: '#79849a'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#d6e3fe'
  primary-fixed-dim: '#bac7e1'
  on-primary-fixed: '#0e1c2f'
  on-primary-fixed-variant: '#3a475c'
  secondary-fixed: '#ffdbce'
  secondary-fixed-dim: '#ffb599'
  on-secondary-fixed: '#370e00'
  on-secondary-fixed-variant: '#7f2b00'
  tertiary-fixed: '#d8e3fb'
  tertiary-fixed-dim: '#bcc7de'
  on-tertiary-fixed: '#111c2d'
  on-tertiary-fixed-variant: '#3c475a'
  background: '#f7f9fb'
  on-background: '#191c1e'
  surface-variant: '#e0e3e5'
typography:
  headline-xl:
    fontFamily: Space Grotesk
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-xl-mobile:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '700'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-lg:
    fontFamily: Space Grotesk
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
    letterSpacing: -0.01em
  headline-md:
    fontFamily: Space Grotesk
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  headline-sm:
    fontFamily: Space Grotesk
    fontSize: 16px
    fontWeight: '600'
    lineHeight: 24px
  body-lg:
    fontFamily: IBM Plex Sans
    fontSize: 15px
    fontWeight: '400'
    lineHeight: 22px
  body-md:
    fontFamily: IBM Plex Sans
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  body-sm:
    fontFamily: IBM Plex Sans
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-code:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  label-status:
    fontFamily: JetBrains Mono
    fontSize: 11px
    fontWeight: '600'
    lineHeight: 14px
    letterSpacing: 0.05em
  label-timestamp:
    fontFamily: JetBrains Mono
    fontSize: 10px
    fontWeight: '500'
    lineHeight: 12px
    letterSpacing: 0.04em
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  gutter: 0.75rem
  gutter-desktop: 1rem
  margin: 1rem
  margin-desktop: 1.5rem
  space-xs: 0.25rem
  space-sm: 0.375rem
  space-md: 0.75rem
  space-lg: 1rem
  space-xl: 1.5rem
---

## Brand & Style

This design system is engineered specifically for mission-critical, 24/7 disaster management command operations. The interface must communicate unwavering authority, operational clarity, and high situational awareness under extreme cognitive load.

The design movement combines **Tactical Modernism** with **High-Density Utilitarianism**:
- Zero decorative ornamentation; every pixel directly conveys status, geospatial intelligence, or triage telemetry.
- High visual structure driven by tabular layouts, clear bounding containers, and explicit status hierarchy.
- The interface evokes vigilance, military-grade discipline, and emergency response readiness, allowing operators to transition from scanning regional maps to dispatching logistics within seconds.

## Colors

The palette establishes an immediate operational hierarchy, contrasting institutional slate authority against life-critical alerts.

### Roles & Semantic Assignment
- **Primary Navy Slate (`#0B192C`)**: Anchor tone for the command header, persistent side navigation rails, critical modal backdrops, and active high-level metrics.
- **Rescue Orange (`#EA580C`)**: Reserved exclusively for BNPB primary action triggers, alert notifications, priority triage markers, and system warning states.
- **Surface Canvas (`#F8FAFC`)**: Light grey canvas baseline to minimize ocular strain during multi-hour operational shifts.
- **Card Surface (`#FFFFFF`)**: Pure white containers for data cards, incident summaries, and GIS side panels.
- **Border Structural (`#E2E8F0`)**: Crisp, 1px structural framing separating data points without visual noise.

### Status Indicators
- **Verified / Operational (`#10B981`)**: Emerald green for confirmed disasters, deployed units, and green-channel reports.
- **Pending / In Review (`#F59E0B`)**: Amber for incoming unverified community reports, weather watches, and pending logistics approvals.
- **Hoax / Critical Red (`#EF4444`)**: Crimson red for verified hoaxes, critical flash flood warnings, or severe infrastructure collapses.

## Typography

Typography enforces high legibility and information density. 

- **Space Grotesk** powers headers and key command metrics, providing an authoritative, structured, and modern technical profile.
- **IBM Plex Sans** delivers neutral, crisp readability across multi-column data sheets, event descriptions, and incident triage feeds.
- **JetBrains Mono** anchors operational precision: timestamps (UTC/WIB), coordinate grids, casualty counts, status pills, and radio callsigns. All numerals are tabular to maintain vertical alignment in tables.

## Layout & Spacing

The command interface implements a **high-density fluid dashboard layout** structured around strict screen efficiency:

- **Grid Architecture**: 12-column layout on desktop with persistent operational side panels and a central dynamic viewport (e.g., interactive GIS maps, data tables).
- **Responsive Handling**:
  - **Desktop (1440px+)**: Multi-pane command view (sidebar, telemetry overview, main workspace, tactical feed) displaying maximum data points above the fold.
  - **Tablet (768px - 1439px)**: Collapsible sidebar into an icon-only strip; secondary telemetry transforms into horizontally swipeable cards or drawers.
  - **Mobile (< 768px)**: Single-column priority view with bottom-anchored emergency actions and tabbed switching between Map, Incident Feed, and Metrics.
- **Spacing Principle**: Dense vertical pacing (`space-sm` and `space-md` predominate) to minimize scrolling during live incident triage while preserving 1px structural dividing lines.

## Elevation & Depth

To maximize clarity under brightly lit command centers or multi-monitor setups, elevation relies on **structural borders and tonal differentiation** rather than soft ambient shadows.

- **Level 0 (Canvas)**: Background tone (`#F8FAFC`).
- **Level 1 (Card Panels)**: Pure white (`#FFFFFF`) framed with a 1px solid border (`#E2E8F0`). Flat surface, 0px blur.
- **Level 2 (Hover / Active Cards)**: Subtle elevation via a tight edge shadow (`0 2px 4px rgba(11, 25, 44, 0.06)`), combined with a border transition to `#CBD5E1`.
- **Level 3 (Command Overlays / Modals / Floating Map Controls)**: Bounded by 1px solid border (`#94A3B8`) with a high-definition structural shadow (`0 8px 16px -2px rgba(11, 25, 44, 0.12), 0 2px 4px -1px rgba(11, 25, 44, 0.08)`).
- **Header Layer**: Deep Slate `#0B192C` with a bottom border `#1E293B` to anchor the top command perimeter.

## Shapes

The design uses **Soft (0.25rem / 4px)** geometry across interactive surfaces and container boundaries to project tactical precision:

- **Cards & Data Panels**: 4px radius (`rounded-sm`).
- **Input Fields & Buttons**: 4px radius (`rounded-sm`).
- **Status Pills & Chips**: 2px to 4px slight rounding, avoiding organic pill shapes to maintain the mechanical, instrument-like aesthetic.
- **Modal Containers**: 6px radius max (`rounded-md`).

## Components

### Buttons
- **Primary Operational Button**: Background `#EA580C`, text `#FFFFFF`, font `Space Grotesk` 600, 4px border radius. Hover state `#C2410C`. Compact height (36px).
- **Secondary Command Button**: Deep Slate `#0B192C` with text `#FFFFFF` for administrative confirmations.
- **Tertiary / Utility Button**: Transparent background, 1px solid `#E2E8F0` border, text `#0B192C`. Hover fills with `#F1F5F9`.

### Status Badges & Pills
- Monospaced typography (`JetBrains Mono`, 11px uppercase).
- **Verified**: Background `#ECFDF5`, text `#065F46`, 1px border `#A7F3D0`, with a solid 6px `#10B981` leading pulse dot.
- **Pending**: Background `#FFFBEB`, text `#92400E`, 1px border `#FDE68A`, with a solid 6px `#F59E0B` leading dot.
- **Hoax / False Report**: Background `#FEF2F2`, text `#991B1B`, 1px border `#FECACA`, strikethrough or cross mark indicator.

### Data Tables & Incident Feeds
- Zebra striping is omitted in favor of fine 1px border separations (`#E2E8F0`).
- Compact row height (36px–40px) to maximize visible records.
- Numerical values, coordinates, and military time stamps rendered strictly in `JetBrains Mono`.

### Form Inputs & Filters
- Clean white inputs with 1px border (`#CBD5E1`), 4px border-radius, font `IBM Plex Sans` 13px. Focus state triggers a 1px border highlight in `#EA580C` with zero glow radius.

### Emergency Alert Broadcast Banner
- Full-width pinned container with bold contrast: Deep Navy Slate `#0B192C` body, an aggressive left accent bar in BNPB Orange (`#EA580C`, 4px width), and real-time live tickers.