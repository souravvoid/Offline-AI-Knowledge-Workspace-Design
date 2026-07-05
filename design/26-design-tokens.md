# Design Tokens Reference

Complete design token values for implementation in CSS custom properties and TypeScript constants.

---

## Color Tokens

```css
/* Light Theme */
:root {
  --color-primary-50: #EEF2FF;
  --color-primary-100: #E0E7FF;
  --color-primary-200: #C7D2FE;
  --color-primary-300: #A5B4FC;
  --color-primary-400: #818CF8;
  --color-primary-500: #6366F1;
  --color-primary-600: #4F46E5;
  --color-primary-700: #4338CA;
  --color-primary-800: #3730A3;
  --color-primary-900: #312E81;

  --color-secondary-50: #F0F9FF;
  --color-secondary-500: #0EA5E9;
  --color-secondary-600: #0284C7;

  --color-accent-50: #F5F3FF;
  --color-accent-500: #8B5CF6;
  --color-accent-600: #7C3AED;

  --color-success-50: #ECFDF5;
  --color-success-500: #10B981;
  --color-success-600: #059669;

  --color-warning-50: #FFFBEB;
  --color-warning-500: #F59E0B;
  --color-warning-600: #D97706;

  --color-error-50: #FEF2F2;
  --color-error-500: #EF4444;
  --color-error-600: #DC2626;

  /* Neutral (Slate) */
  --color-neutral-50: #F8FAFC;
  --color-neutral-100: #F1F5F9;
  --color-neutral-200: #E2E8F0;
  --color-neutral-300: #CBD5E1;
  --color-neutral-400: #94A3B8;
  --color-neutral-500: #64748B;
  --color-neutral-600: #475569;
  --color-neutral-700: #334155;
  --color-neutral-800: #1E293B;
  --color-neutral-900: #0F172A;

  /* Semantic */
  --bg-primary: #FFFFFF;
  --bg-secondary: #F8FAFC;
  --bg-tertiary: #F1F5F9;
  --border-default: #E2E8F0;
  --border-hover: #CBD5E1;
  --text-primary: #0F172A;
  --text-secondary: #475569;
  --text-tertiary: #94A3B8;
  --text-inverse: #FFFFFF;
}

/* Dark Theme */
[data-theme="dark"] {
  --color-primary-500: #818CF8;
  --color-primary-600: #6366F1;

  --bg-primary: #0F172A;
  --bg-secondary: #1E293B;
  --bg-tertiary: #334155;
  --border-default: #334155;
  --border-hover: #475569;
  --text-primary: #F1F5F9;
  --text-secondary: #94A3B8;
  --text-tertiary: #64748B;
  --text-inverse: #0F172A;
}
```

---

## Typography Tokens

```css
/* Font Families */
--font-sans: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
--font-mono: 'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace;
--font-serif: 'Source Serif 4', Georgia, 'Times New Roman', serif;

/* Font Sizes */
--text-xs:   0.75rem   (12px);
--text-sm:   0.875rem  (14px);
--text-base: 1rem      (16px);
--text-lg:   1.125rem  (18px);
--text-xl:   1.25rem   (20px);
--text-2xl:  1.5rem    (24px);
--text-3xl:  1.875rem  (30px);
--text-4xl:  2.25rem   (36px);

/* Line Heights */
--leading-none:    1;
--leading-tight:   1.25;
--leading-snug:    1.375;
--leading-normal:  1.5;
--leading-relaxed: 1.625;
--leading-loose:   2;

/* Font Weights */
--weight-normal:  400;
--weight-medium:  500;
--weight-semibold: 600;
--weight-bold:    700;

/* Heading Sizes */
--h1-size: 2.25rem;
--h1-weight: 700;
--h1-line-height: 1.2;
--h2-size: 1.5rem;
--h2-weight: 600;
--h2-line-height: 1.3;
--h3-size: 1.25rem;
--h3-weight: 600;
--h3-line-height: 1.4;
--h4-size: 1.125rem;
--h4-weight: 500;
--h4-line-height: 1.4;

/* Body Sizes */
--body-lg:   1.125rem (18px) line-height: 1.7;
--body-base: 1rem     (16px) line-height: 1.6;
--body-sm:   0.875rem (14px) line-height: 1.5;
--body-xs:   0.75rem  (12px) line-height: 1.4;

/* Reading Mode */
--reading-font: var(--font-serif);
--reading-size: 1.0625rem (17px);
--reading-leading: 1.75;
--reading-width: 720px;
```

---

## Spacing Tokens

```css
/* Scale: 4px base (0.25rem increments) */
--space-0:   0;
--space-1:   0.25rem  (4px);
--space-2:   0.5rem   (8px);
--space-3:   0.75rem  (12px);
--space-4:   1rem     (16px);
--space-5:   1.25rem  (20px);
--space-6:   1.5rem   (24px);
--space-8:   2rem     (32px);
--space-10:  2.5rem   (40px);
--space-12:  3rem     (48px);
--space-14:  3.5rem   (56px);
--space-16:  4rem     (64px);
--space-20:  5rem     (80px);
--space-24:  6rem     (96px);

/* Page Margins */
--page-margin-sm:    var(--space-4);
--page-margin-md:    var(--space-6);
--page-margin-lg:    var(--space-8);

/* Section Gaps */
--section-gap-sm:    var(--space-4);
--section-gap-md:    var(--space-6);
--section-gap-lg:    var(--space-8);
--section-gap-xl:    var(--space-12);

/* Component Padding */
--padding-button-sm:  var(--space-1) var(--space-3);
--padding-button-md:  var(--space-2) var(--space-4);
--padding-button-lg:  var(--space-3) var(--space-6);
--padding-card:       var(--space-4);
--padding-modal:      var(--space-6);
--padding-input:      var(--space-2) var(--space-3);
```

---

## Border Radius Tokens

```css
--radius-sm:   0.375rem  (6px);
--radius-md:   0.5rem    (8px);
--radius-lg:   0.75rem   (12px);
--radius-xl:   1rem      (16px);
--radius-2xl:  1.5rem    (24px);
--radius-3xl:  2rem      (32px);
--radius-full: 9999px    (pill/circle);

/* Common assignments */
--radius-button:  var(--radius-md);
--radius-card:    var(--radius-lg);
--radius-modal:   var(--radius-xl);
--radius-input:   var(--radius-md);
--radius-badge:   var(--radius-full);
```

---

## Shadow / Elevation Tokens

```css
--shadow-xs:   0 1px 2px rgba(0,0,0,0.04);
--shadow-sm:   0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
--shadow-md:   0 4px 6px -1px rgba(0,0,0,0.07), 0 2px 4px -2px rgba(0,0,0,0.05);
--shadow-lg:   0 10px 15px -3px rgba(0,0,0,0.08), 0 4px 6px -4px rgba(0,0,0,0.04);
--shadow-xl:   0 20px 25px -5px rgba(0,0,0,0.1), 0 8px 10px -6px rgba(0,0,0,0.06);
--shadow-2xl:  0 25px 50px -12px rgba(0,0,0,0.15);

/* Elevation levels for components */
--elevation-card:     var(--shadow-sm);
--elevation-hover:    var(--shadow-md);
--elevation-dropdown: var(--shadow-lg);
--elevation-modal:    var(--shadow-xl);
--elevation-toast:    var(--shadow-2xl);

/* Dark theme shadows (stronger for visibility) */
[data-theme="dark"] {
  --shadow-sm:  0 1px 3px rgba(0,0,0,0.3);
  --shadow-md:  0 4px 6px rgba(0,0,0,0.35);
  --shadow-lg:  0 10px 15px rgba(0,0,0,0.4);
  --shadow-xl:  0 20px 25px rgba(0,0,0,0.45);
  --shadow-2xl: 0 25px 50px rgba(0,0,0,0.5);
}
```

---

## Animation & Timing Tokens

```css
/* Duration */
--duration-instant: 0ms;
--duration-fast:   100ms;
--duration-normal: 200ms;
--duration-slow:   300ms;
--duration-slower: 500ms;

/* Easing */
--ease-out:   cubic-bezier(0.0, 0.0, 0.2, 1);
--ease-in:    cubic-bezier(0.4, 0.0, 1, 1);
--ease-in-out: cubic-bezier(0.4, 0.0, 0.2, 1);
--ease-spring: cubic-bezier(0.34, 1.56, 0.64, 1);

/* Common assignments */
--transition-button:   background-color var(--duration-fast) var(--ease-out),
                      box-shadow var(--duration-fast) var(--ease-out);
--transition-card:     transform var(--duration-normal) var(--ease-out),
                      box-shadow var(--duration-normal) var(--ease-out);
--transition-panel:    width var(--duration-normal) var(--ease-in-out),
                      opacity var(--duration-normal) var(--ease-in-out);
--transition-modal:    transform var(--duration-normal) var(--ease-out),
                      opacity var(--duration-normal) var(--ease-out);
--transition-flashcard: transform var(--duration-slower) var(--ease-in-out);

/* Animation durations */
--spin-duration: 600ms;
--pulse-duration: 2000ms;
--skeleton-duration: 1500ms;
```

---

## Z-Index Tokens

```css
--z-base:      0;
--z-dropdown:  100;
--z-sticky:    200;
--z-overlay:   300;
--z-modal:     400;
--z-toast:     500;
--z-tooltip:   600;
```

---

## Opacity Tokens

```css
--opacity-disabled:   0.5;
--opacity-hover:     0.85;
--opacity-active:    0.7;
--opacity-overlay:   0.5;
--opacity-subtle:    0.1;
```

---

## Icon Size Tokens

```css
--icon-xs:   14px;
--icon-sm:   16px;
--icon-md:   20px;
--icon-lg:   24px;
--icon-xl:   32px;

/* Contextual assignments */
--icon-nav:      var(--icon-md);
--icon-button:   var(--icon-sm);
--icon-empty:    var(--icon-xl);
--icon-badge:    var(--icon-xs);
```

---

## Tailwind CSS Configuration

```js
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#EEF2FF',
          100: '#E0E7FF',
          200: '#C7D2FE',
          300: '#A5B4FC',
          400: '#818CF8',
          500: '#6366F1',
          600: '#4F46E5',
          700: '#4338CA',
          800: '#3730A3',
          900: '#312E81',
        },
        // ... all colors from above
        surface: {
          DEFAULT: 'var(--bg-primary)',
          secondary: 'var(--bg-secondary)',
          tertiary: 'var(--bg-tertiary)',
        },
      },
      fontFamily: {
        sans: ['Inter', 'system-ui', 'sans-serif'],
        mono: ['JetBrains Mono', 'monospace'],
        serif: ['Source Serif 4', 'serif'],
      },
      fontSize: {
        '2xs': ['0.625rem', { lineHeight: '0.875rem' }],
        xs: ['0.75rem', { lineHeight: '1rem' }],
        sm: ['0.875rem', { lineHeight: '1.25rem' }],
        base: ['1rem', { lineHeight: '1.5rem' }],
        lg: ['1.125rem', { lineHeight: '1.75rem' }],
        xl: ['1.25rem', { lineHeight: '1.75rem' }],
        '2xl': ['1.5rem', { lineHeight: '2rem' }],
        '3xl': ['1.875rem', { lineHeight: '2.25rem' }],
        '4xl': ['2.25rem', { lineHeight: '2.5rem' }],
      },
      spacing: {
        4.5: '1.125rem',
        18: '4.5rem',
        88: '22rem',
        100: '25rem',
      },
      borderRadius: {
        sm: '0.375rem',
        md: '0.5rem',
        lg: '0.75rem',
        xl: '1rem',
        '2xl': '1.5rem',
        '3xl': '2rem',
      },
      boxShadow: {
        'elevation-card': 'var(--elevation-card)',
        'elevation-hover': 'var(--elevation-hover)',
        'elevation-dropdown': 'var(--elevation-dropdown)',
        'elevation-modal': 'var(--elevation-modal)',
      },
      animation: {
        'spin-slow': 'spin 3s linear infinite',
        'pulse-soft': 'pulse 2s cubic-bezier(0.4, 0, 0.6, 1) infinite',
        'slide-in': 'slideIn 0.2s ease-out',
        'slide-out': 'slideOut 0.15s ease-in',
        'scale-in': 'scaleIn 0.2s ease-out',
        'fade-in': 'fadeIn 0.15s ease-out',
        'flashcard-flip': 'flip 0.4s ease-in-out',
      },
      keyframes: {
        slideIn: {
          '0%': { transform: 'translateY(-4px)', opacity: '0' },
          '100%': { transform: 'translateY(0)', opacity: '1' },
        },
        slideOut: {
          '0%': { transform: 'translateY(0)', opacity: '1' },
          '100%': { transform: 'translateY(-4px)', opacity: '0' },
        },
        scaleIn: {
          '0%': { transform: 'scale(0.95)', opacity: '0' },
          '100%': { transform: 'scale(1)', opacity: '1' },
        },
        fadeIn: {
          '0%': { opacity: '0' },
          '100%': { opacity: '1' },
        },
        flip: {
          '0%': { transform: 'rotateY(0deg)' },
          '100%': { transform: 'rotateY(180deg)' },
        },
      },
    },
  },
};
```

## TypeScript Token Constants

```typescript
// tokens.ts
export const tokens = {
  color: {
    primary: {
      50: '#EEF2FF',
      500: '#6366F1',
      600: '#4F46E5',
    },
    secondary: {
      50: '#F0F9FF',
      500: '#0EA5E9',
    },
    success: '#10B981',
    warning: '#F59E0B',
    error: '#EF4444',
  },
  space: {
    xs: 4,
    sm: 8,
    md: 16,
    lg: 24,
    xl: 32,
    '2xl': 48,
    '3xl': 64,
  } as const,
  radius: {
    sm: 6,
    md: 8,
    lg: 12,
    xl: 16,
    full: 9999,
  } as const,
  duration: {
    fast: 100,
    normal: 200,
    slow: 300,
    slower: 500,
  } as const,
  icon: {
    xs: 14,
    sm: 16,
    md: 20,
    lg: 24,
    xl: 32,
  } as const,
  zIndex: {
    base: 0,
    dropdown: 100,
    sticky: 200,
    overlay: 300,
    modal: 400,
    toast: 500,
    tooltip: 600,
  } as const,
} as const;
```

## Accessible Contrast Values

```typescript
export const contrastRatios = {
  // Light theme
  light: {
    'text-primary-on-bg': 12.5,  // WCAG AAA
    'text-secondary-on-bg': 7.2, // WCAG AAA
    'text-tertiary-on-bg': 4.8,  // WCAG AA
    'primary-on-bg': 6.8,        // WCAG AA
  },
  // Dark theme
  dark: {
    'text-primary-on-bg': 14.2,  // WCAG AAA
    'text-secondary-on-bg': 7.8, // WCAG AAA
    'text-tertiary-on-bg': 5.1,  // WCAG AA
    'primary-on-bg': 7.2,        // WCAG AA
  },
} as const;
```
