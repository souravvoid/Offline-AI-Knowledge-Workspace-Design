---
name: Khoji Technical Noir
colors:
  surface: '#121319'
  surface-dim: '#121319'
  surface-bright: '#383940'
  surface-container-lowest: '#0d0e14'
  surface-container-low: '#1a1b21'
  surface-container: '#1e1f26'
  surface-container-high: '#292a30'
  surface-container-highest: '#34343b'
  on-surface: '#e3e1ea'
  on-surface-variant: '#c6c5d5'
  inverse-surface: '#e3e1ea'
  inverse-on-surface: '#2f3037'
  outline: '#908f9e'
  outline-variant: '#454653'
  surface-tint: '#bdc2ff'
  primary: '#bdc2ff'
  on-primary: '#131e8c'
  primary-container: '#818cf8'
  on-primary-container: '#101b8a'
  inverse-primary: '#4953bc'
  secondary: '#bcc7df'
  on-secondary: '#263144'
  secondary-container: '#3c475b'
  on-secondary-container: '#aab5cd'
  tertiary: '#f7bd3e'
  on-tertiary: '#412d00'
  tertiary-container: '#c08d00'
  on-tertiary-container: '#3e2b00'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#e0e0ff'
  primary-fixed-dim: '#bdc2ff'
  on-primary-fixed: '#000767'
  on-primary-fixed-variant: '#2f3aa3'
  secondary-fixed: '#d7e3fc'
  secondary-fixed-dim: '#bcc7df'
  on-secondary-fixed: '#101c2e'
  on-secondary-fixed-variant: '#3c475b'
  tertiary-fixed: '#ffdea4'
  tertiary-fixed-dim: '#f7bd3e'
  on-tertiary-fixed: '#261900'
  on-tertiary-fixed-variant: '#5d4200'
  background: '#121319'
  on-background: '#e3e1ea'
  surface-variant: '#34343b'
  surface-glass: rgba(31, 31, 38, 0.8)
  syntax-keyword: '#bdc2ff'
  syntax-type: '#f7bd3e'
  syntax-string: '#aeb9d0'
  syntax-comment: '#454653'
  outline-muted: rgba(144, 143, 158, 0.1)
typography:
  headline-xl:
    fontFamily: Inter
    fontSize: 36px
    fontWeight: '700'
    lineHeight: '1.2'
  headline-lg:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: '1.3'
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.4'
  body-md:
    fontFamily: Source Serif 4
    fontSize: 16px
    fontWeight: '400'
    lineHeight: '1.6'
  label-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '500'
    lineHeight: '1.0'
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 14px
    fontWeight: '400'
    lineHeight: '1.5'
  code-xs:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: '1.0'
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: '1.3'
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  space-1: 4px
  space-2: 8px
  space-4: 16px
  space-6: 24px
  space-8: 32px
  space-12: 48px
  margin-page: 1.5rem
  gutter-grid: 1rem
---

## Brand & Style
The brand personality is **Technical, Precise, and Sophisticated**. It targets developers and data engineers who require a high-density information environment that feels both cutting-edge and reliable.

The design style is a hybrid of **Glassmorphism** and **Modern Corporate Noir**. It utilizes deep charcoal surfaces layered with translucent panels to create a sense of focused "night mode" productivity. Visual interest is generated through vibrant syntax highlighting and subtle glowing accents that mimic the aesthetic of high-end code editors and terminal environments. The emotional response should be one of "calm mastery" over complex data.

## Colors
The palette is centered on a deep **Neutral Black (#121319)** base to minimize eye strain. The **Primary Indigo (#818cf8)** acts as the functional lead, used for branding, active states, and primary actions. 

**Secondary Slate (#3e495d)** manages container levels, while **Tertiary Amber (#f7bd3e)** provides high-visibility warnings or data-type distinctions. The color system relies heavily on "Fidelity" variants, where subtle shifts in hex values differentiate between the background, low-containers, and high-containers to create a structured hierarchy without needing heavy lines.

## Typography
The system uses a sophisticated three-font approach:
- **Inter** (Headlines & Labels): Provides a clean, systematic feel for UI chrome and navigation.
- **Source Serif 4** (Body): Injected to give narrative content a high-quality, editorial feel, making long-form documentation easier to parse.
- **JetBrains Mono** (Technical): Reserved for data, code, and metadata, reinforcing the technical nature of the tool.

Large headlines should scale down by roughly 20% on mobile devices to maintain readability without excessive wrapping.

## Layout & Spacing
The layout follows a **Fluid Grid** model with a heavy emphasis on vertical rhythm. 
- **Mobile:** Single column with 16px lateral padding. 
- **Desktop:** 12-column grid with 24px gutters. 

Spacing is based on an 8px base unit. Navigation elements (App Bar and Bottom Nav) are fixed to the viewport to maintain context, while content areas use generous top/bottom padding (pt-20, pb-32) to ensure elements aren't obscured by the persistent UI bars.

## Elevation & Depth
Depth is communicated through **Glassmorphism** and **Tonal Layering**. 
- **Level 0 (Base):** Surface-dim (#121319).
- **Level 1 (Cards):** Surface-container with 1px `outline-muted` border.
- **Level 2 (Active Overlays):** Glass panels using `backdrop-filter: blur(12px)` and 80% opacity backgrounds.
- **Shadows:** Use large, soft shadows (`shadow-2xl`) for elevated containers to create a "floating" effect, often combined with a 10% opacity primary color glow positioned behind the card to simulate light emission.

## Shapes
A **Rounded** shape language is used to soften the technical density of the UI.
- Base components (Inputs, Chips): 0.5rem (rounded-lg).
- Main containers (Cards, Editor): 0.75rem to 1rem (rounded-xl).
- Interactive indicators/Badges: Full (rounded-full).
- Action items like navigation tabs use a 0.75rem radius to feel substantial and clickable.

## Components
- **Buttons:** Primary buttons use `bg-primary` with `on-primary` text. Secondary actions use `bg-secondary-container` with subtle borders. Hover states should include a slight brightness increase and transition duration of 200ms.
- **Chips/Tabs:** Inactive tabs are transparent with `on-surface-variant` text. Active tabs use `bg-secondary-container` with a subtle 20% opacity primary border to highlight focus.
- **Code Editor:** Must feature a distinct header with "traffic light" window controls (red/yellow/green at 40% opacity) and a dedicated line-number gutter.
- **Navigation Bars:** Glass panels with a bottom/top border of `outline-variant`. Icons should use the Material Symbols Outlined set, with active states filled.
- **Cards:** Border-heavy with `outline-variant/30` and a dark, non-transparent footer for metadata display.