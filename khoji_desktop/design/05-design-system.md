# Phase 5-6: Design System & Color Palette

## Product Name: Khoji Design System
## Version: 1.0
## Codename: "Seeker"

---

## 1. Design Tokens

### 1.1 Color Palette

#### Light Theme

```
Primary:          #6366F1 (Indigo 500)
Primary Hover:    #4F46E5 (Indigo 600)
Primary Light:    #EEF2FF (Indigo 50)
Primary Dark:     #4338CA (Indigo 700)

Secondary:        #0EA5E9 (Sky 500)
Secondary Hover:  #0284C7 (Sky 600)
Secondary Light:  #F0F9FF (Sky 50)

Accent:           #8B5CF6 (Violet 500)
Accent Hover:     #7C3AED (Violet 600)
Accent Light:     #F5F3FF (Violet 50)

Success:          #10B981 (Emerald 500)
Success Light:    #ECFDF5 (Emerald 50)

Warning:          #F59E0B (Amber 500)
Warning Light:    #FFFBEB (Amber 50)

Error:            #EF4444 (Red 500)
Error Light:      #FEF2F2 (Red 50)

Neutral:
  --bg-primary:    #FFFFFF
  --bg-secondary:  #F8FAFC
  --bg-tertiary:   #F1F5F9
  --border:        #E2E8F0
  --border-hover:  #CBD5E1
  --text-primary:  #0F172A
  --text-secondary:#475569
  --text-tertiary: #94A3B8
  --text-inverse:  #FFFFFF

Surface:
  --surface-card:  #FFFFFF
  --surface-modal: #FFFFFF
  --surface-tooltip:#0F172A
  --surface-hover: #F8FAFC
  --surface-active:#EEF2FF

Shadow:
  --shadow-sm:   0 1px 2px rgba(0,0,0,0.05)
  --shadow-md:   0 4px 6px -1px rgba(0,0,0,0.07)
  --shadow-lg:   0 10px 15px -3px rgba(0,0,0,0.08)
  --shadow-xl:   0 20px 25px -5px rgba(0,0,0,0.1)

Glassmorphism (Light):
  background: rgba(255, 255, 255, 0.7)
  backdrop-filter: blur(12px)
  border: 1px solid rgba(255, 255, 255, 0.3)
```

#### Dark Theme

```
Primary:          #818CF8 (Indigo 400)
Primary Hover:    #6366F1 (Indigo 500)
Primary Light:    rgba(99, 102, 241, 0.15)
Primary Dark:     #A5B4FC (Indigo 300)

Secondary:        #38BDF8 (Sky 400)
Secondary Hover:  #0EA5E9 (Sky 500)

Accent:           #A78BFA (Violet 400)
Accent Hover:     #8B5CF6 (Violet 500)

Success:          #34D399 (Emerald 400)
Warning:          #FBBF24 (Amber 400)
Error:            #F87171 (Red 400)

Neutral:
  --bg-primary:    #0F172A
  --bg-secondary:  #1E293B
  --bg-tertiary:   #334155
  --border:        #334155
  --border-hover:  #475569
  --text-primary:  #F1F5F9
  --text-secondary:#94A3B8
  --text-tertiary: #64748B
  --text-inverse:  #0F172A

Surface:
  --surface-card:  #1E293B
  --surface-modal: #1E293B
  --surface-tooltip:#F1F5F9
  --surface-hover: #334155
  --surface-active:rgba(99, 102, 241, 0.15)

Shadow:
  --shadow-sm:   0 1px 2px rgba(0,0,0,0.2)
  --shadow-md:   0 4px 6px -1px rgba(0,0,0,0.3)
  --shadow-lg:   0 10px 15px -3px rgba(0,0,0,0.3)
  --shadow-xl:   0 20px 25px -5px rgba(0,0,0,0.4)

Glassmorphism (Dark):
  background: rgba(30, 41, 59, 0.7)
  backdrop-filter: blur(12px)
  border: 1px solid rgba(51, 65, 85, 0.5)
```

### 1.2 Typography

```
Font Family:
  --font-sans:    'Inter', -apple-system, BlinkMacSystemFont, sans-serif
  --font-mono:    'JetBrains Mono', 'Fira Code', monospace
  --font-serif:   'Source Serif 4', Georgia, serif (for reading mode)

Headings:
  --h1-size:      2.25rem  (36px)  line-height: 1.2  font-weight: 700
  --h2-size:      1.5rem   (24px)  line-height: 1.3  font-weight: 600
  --h3-size:      1.25rem  (20px)  line-height: 1.4  font-weight: 600
  --h4-size:      1.125rem (18px)  line-height: 1.4  font-weight: 500

Body:
  --body-lg:      1.125rem (18px)  line-height: 1.7
  --body-base:    1rem     (16px)  line-height: 1.6
  --body-sm:      0.875rem (14px)  line-height: 1.5
  --body-xs:      0.75rem  (12px)  line-height: 1.4

Markdown Content:
  --reading-width: 720px
  --reading-font: 'Source Serif 4', serif (toggleable)
  --reading-size:  1.0625rem (17px)
  --reading-leading: 1.75
```

### 1.3 Spacing

```
Scale (4px base):
  --space-1:  0.25rem  (4px)
  --space-2:  0.5rem   (8px)
  --space-3:  0.75rem  (12px)
  --space-4:  1rem     (16px)
  --space-5:  1.25rem  (20px)
  --space-6:  1.5rem   (24px)
  --space-8:  2rem     (32px)
  --space-10: 2.5rem   (40px)
  --space-12: 3rem     (48px)
  --space-16: 4rem     (64px)
  --space-20: 5rem     (80px)
```

### 1.4 Border Radius

```
  --radius-sm:   0.375rem (6px)
  --radius-md:   0.5rem   (8px)
  --radius-lg:   0.75rem  (12px)
  --radius-xl:   1rem     (16px)
  --radius-2xl:  1.5rem   (24px)
  --radius-full: 9999px   (pill)
```

---

## 2. Component Specifications

### 2.1 Buttons

```
Primary Button:
  padding:      0.5rem 1rem (8px 16px)
  font-size:    0.875rem
  font-weight:  500
  border-radius:0.5rem
  background:   var(--primary)
  color:        white
  hover:        var(--primary-hover)
  active:       var(--primary-dark)
  transition:   150ms ease
  icon + text gap: 0.5rem

Secondary Button:
  background:   transparent
  border:       1px solid var(--border)
  color:        var(--text-primary)
  hover:        var(--surface-hover)

Ghost Button:
  background:   transparent
  color:        var(--text-secondary)
  hover:        var(--surface-hover)

Icon Button:
  width:        2.25rem (36px)
  height:       2.25rem
  padding:      0.5rem
  border-radius:0.5rem

Button Sizes:
  sm:   0.375rem 0.75rem, font 0.75rem
  md:   0.5rem 1rem, font 0.875rem (default)
  lg:   0.625rem 1.25rem, font 1rem
  xl:   0.75rem 1.5rem, font 1.125rem
```

### 2.2 Cards

```
Document Card:
  width:        280px (in grid)
  padding:      1rem
  border-radius:0.75rem
  background:   var(--surface-card)
  border:       1px solid var(--border)
  shadow:       var(--shadow-sm)
  hover:        shadow-md, border-color var(--border-hover)
  transition:   200ms ease

Content Card:
  padding:      1.5rem
  border-radius:0.75rem
  background:   var(--surface-card)
  border:       1px solid var(--border)
```

### 2.3 Inputs

```
Text Input:
  padding:      0.5rem 0.75rem
  border-radius:0.5rem
  border:       1px solid var(--border)
  background:   var(--bg-primary)
  color:        var(--text-primary)
  focus:        ring-2 ring-primary/20, border-primary
  placeholder:  var(--text-tertiary)
  font-size:    0.875rem

Search Input:
  Same as text input but with
  icon prefix (search)
  clear button suffix
  Cmd+K badge
```

### 2.4 Sidebar

```
Sidebar (Desktop):
  width:        260px (collapsed: 56px)
  bg:           var(--bg-secondary)
  border-right: 1px solid var(--border)
  transition:   200ms ease

Nav Item:
  padding:      0.5rem 0.75rem
  border-radius:0.5rem
  margin:       0.125rem 0.5rem
  color:        var(--text-secondary)
  hover:        bg var(--surface-hover), color var(--text-primary)
  active:       bg var(--surface-active), color var(--primary)
  icon:         20px
  gap:          0.75rem
```

### 2.5 Modals & Dialogs

```
Modal:
  bg:           var(--surface-modal)
  border-radius:var(--radius-xl)
  shadow:       var(--shadow-xl)
  padding:      1.5rem
  max-width:    32rem
  animation:    scale-in 200ms ease

Dialog Backdrop:
  background:   rgba(0, 0, 0, 0.5)
  backdrop-filter: blur(4px)
```

### 2.6 Tabs

```
Tab Bar:
  display:      flex
  gap:          0
  border-bottom: 1px solid var(--border)

Tab Item:
  padding:      0.625rem 1rem
  font-size:    0.875rem
  font-weight:  500
  color:        var(--text-tertiary)
  border-bottom: 2px solid transparent
  hover:        color var(--text-secondary)
  active:       color var(--primary), border-color var(--primary)
```

### 2.7 Badges

```
Badge:
  padding:      0.125rem 0.5rem
  font-size:    0.75rem
  font-weight:  500
  border-radius:9999px
  variants:     primary, secondary, success, warning, error, neutral
```

### 2.8 Progress Indicators

```
Progress Bar:
  height:       0.375rem
  border-radius:9999px
  background:   var(--bg-tertiary)
  fill:         var(--primary)
  transition:   width 300ms ease

Spinner:
  width:        1.25rem
  height:       1.25rem
  border:       2px solid var(--border)
  border-top-color: var(--primary)
  animation:    spin 600ms linear infinite

Pipeline Step Indicator:
  Horizontal step bar
  Each step: icon + label
  Completed: green check
  Current: pulsing primary
  Pending: gray
  Error: red exclamation
```

---

## 3. Keyboard Shortcuts

```
Global:
  Cmd+K        Quick search
  Cmd+,        Settings
  Cmd+N        New note
  Cmd+Shift+U  Upload document

Document Workspace:
  Cmd+Enter    Ask AI chat
  Cmd+P        Toggle preview/edit
  Cmd+E        Export
  Cmd+F        Find in document
  Cmd+D        Toggle dark mode

Navigation:
  Cmd+1        Library
  Cmd+2        Notes
  Cmd+3        Flashcards
  Cmd+4        Quiz
  Cmd+5        Mind Maps
  Cmd+6        Chat history
  Cmd+B        Toggle sidebar
  Cmd+Shift+L  Toggle right panel (chat)

Flashcard Review:
  Space        Show answer
  1            Again
  2            Hard
  3            Good
  4            Easy
  →            Next card
  R            Restart queue

Quiz:
  A/B/C/D      Select option
  Enter        Confirm answer
  →            Next question
  ←            Previous question
```

---

## 4. Responsive Breakpoints

```
Mobile:        0 - 640px
Tablet:        641px - 1024px
Desktop:       1025px - 1440px
Wide:          1441px+

Layout Adjustments:
  Mobile:     Single column, bottom tab bar, slide-over panels
  Tablet:     Two column, collapsible sidebar, side-by-side tabs
  Desktop:    Three column (sidebar + content + chat)
  Wide:       Same as desktop, wider content area
```

---

## 5. Accessibility (WCAG 2.1 AA)

```
Target:       AA minimum, AAA where possible

Contrast:
  Text:          4.5:1 minimum
  Large text:    3:1 minimum
  UI components: 3:1 minimum

Focus:
  Visible focus ring: 2px solid var(--primary)
  Outline offset: 2px
  Never remove outline without replacement

Keyboard:
  All actions via keyboard
  Logical tab order
  Skip to content link
  No keyboard traps

Screen Reader:
  ARIA labels on all interactive elements
  Live regions for dynamic content
  Status announcements for long operations
  Semantic HTML structure

Motion:
  Respect prefers-reduced-motion
  No flashing animations (>3Hz)
  Animations optional and non-essential

Reading:
  Font size adjustable (100% - 200%)
  Line spacing adjustable
  Reading mode (serif font, wider text)
  High contrast mode
```

---

## 6. Icons

```
Icon Set:     Lucide Icons (open source, consistent)
Icon Size:    16px (default UI), 20px (nav), 24px (empty states)
Icon Weight:  Regular (2px stroke)
Icon Color:   Current color (inherits from text/button)

Core Icons:
  Upload:    upload, file-up, file-plus
  Document:  file-text, file-image, file-type
  Notes:     file-edit, sticky-note
  Flashcard: layers, shuffle
  Quiz:      help-circle, clipboard-list
  Mind Map:  git-branch, network
  Chat:      message-square, bot
  Search:    search
  Settings:  settings, cog
  Library:   books, library
  Collection:folder, folder-open
  Export:    download, file-down
  Delete:    trash-2
  Edit:      pencil, pen
  Share:     share-2
  Star:      star
  Time:      clock, history
  User:      user, user-circle
  Chevron:   chevron-down, chevron-right, chevron-left
  Close:     x
  Menu:      menu
  Minimize:  minimize-2
  Maximize:  maximize-2
  AI:        sparkles, brain, cpu
  Offline:   wifi-off
  Error:     alert-circle, alert-triangle
  Success:   check-circle-2
  Warning:   alert-triangle
```
