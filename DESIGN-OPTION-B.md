# Option B: The Deal Finder Flow

## Complete UX Design Document for TripForge Web App

**Author:** Product Design Lead (ex-Skyscanner, Multi-City & Everywhere)
**Date:** February 2026
**Status:** Ready for implementation

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Design System](#2-design-system)
3. [Screen 1: Landing / Entry](#3-screen-1-landing--entry)
4. [Screen 2: Trip Builder (Input)](#4-screen-2-trip-builder-input)
5. [Screen 3: Confirmation / Edit](#5-screen-3-confirmation--edit)
6. [Screen 4: Research / Loading](#6-screen-4-research--loading)
7. [Screen 5: Results / Itinerary](#7-screen-5-results--itinerary)
8. [Screen 6: Share Flow](#8-screen-6-share-flow)
9. [Screen 7: Recipient View](#9-screen-7-recipient-view)
10. [State Management & Transitions](#10-state-management--transitions)
11. [Implementation Architecture](#11-implementation-architecture)

---

## 1. Design Philosophy

### The Core Insight from Skyscanner

At Skyscanner, we learned that the multi-city builder fails when it asks the user to think like a database. "Select origin, select destination, select date" repeated N times is brutal for complex trips. The users who plan Greek island-hopping trips are not database operators -- they are *storytellers*. They say things like "We want to do Milos for a week then hop over to Koufonisia for a couple of nights."

The Deal Finder Flow works on a three-phase trust arc:

1. **"You understand me"** -- I describe my trip in natural language, you get it right
2. **"You did the work"** -- I can see you searched everywhere, compared everything
3. **"I can prove it to my group"** -- The shareable output makes me look like a genius organiser

### Design Principles

- **Utility over decoration.** Every pixel earns its space by reducing the organiser's anxiety.
- **Progressive disclosure.** Show the answer first. Let them drill in if they want.
- **Price confidence.** Never show a single price. Always show a range, a comparison, or a "we checked X sources" indicator.
- **Mobile-first, single-column.** The organiser is doing this on their phone at 11pm after the group chat blew up.
- **Zero accounts, zero friction.** No login. No signup. URL is the state.

### The Emotional Journey

```
Landing:        "Oh this is exactly what I need"        (Relief)
Input:          "That was easy, it understood me"        (Surprise)
Confirmation:   "Yes that's right, let me tweak one thing" (Control)
Loading:        "Wow it's checking everything"           (Anticipation)
Results:        "This is thorough, I trust these numbers" (Confidence)
Share:          "My group is going to love this"          (Pride)
Recipient:      "They really did their research"          (Trust)
```

---

## 2. Design System

### Typography

```css
/* Font stack -- Inter for UI, system fallback */
--font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;

/* Type scale (mobile-first, rem-based) */
--text-xs:    0.75rem;   /* 12px -- labels, badges */
--text-sm:    0.8125rem; /* 13px -- secondary text, captions */
--text-base:  0.9375rem; /* 15px -- body text */
--text-md:    1.0625rem; /* 17px -- card titles */
--text-lg:    1.25rem;   /* 20px -- section headers */
--text-xl:    1.5rem;    /* 24px -- page titles mobile */
--text-2xl:   2rem;      /* 32px -- hero titles mobile */
--text-3xl:   2.5rem;    /* 40px -- hero titles desktop */

/* Font weights */
--weight-light:    300;
--weight-regular:  400;
--weight-medium:   500;
--weight-semibold: 600;
--weight-bold:     700;

/* Line heights */
--leading-tight:  1.25;
--leading-normal: 1.5;
--leading-loose:  1.75;

/* Letter spacing */
--tracking-tight:  -0.025em;
--tracking-normal: 0;
--tracking-wide:   0.05em;
--tracking-caps:   0.1em;
```

### Colour Palette

The existing codebase uses a dark theme with cyan accents. We keep this -- it reads as "premium travel tool" rather than "another pastel SaaS landing page." But we need to expand the system for interactive states.

```css
:root {
  /* --- Backgrounds --- */
  --bg-base:       #0a0a0a;   /* Page background */
  --bg-surface:    #111111;   /* Cards, panels */
  --bg-surface-2:  #161616;   /* Nested surfaces, hover states */
  --bg-surface-3:  #1a1a1a;   /* Tertiary surface, dividers */
  --bg-overlay:    rgba(0, 0, 0, 0.6);  /* Modal backdrop */

  /* --- Text --- */
  --text-primary:    #e8e8e8;  /* Primary text */
  --text-secondary:  #a0a0a0;  /* Secondary / supporting */
  --text-tertiary:   #666666;  /* Disabled, muted */
  --text-inverse:    #0a0a0a;  /* Text on bright backgrounds */

  /* --- Brand / Accent --- */
  --accent-primary:   #00b4d8;  /* Primary CTA, links, active states */
  --accent-light:     #90e0ef;  /* Lighter accent for highlights */
  --accent-dark:      #0077b6;  /* Darker accent for gradients */
  --accent-subtle:    rgba(0, 180, 216, 0.1);  /* Accent tint for bg */

  /* --- Semantic --- */
  --color-success:    #34d399;  /* Confirmed, booked, good deal */
  --color-warning:    #f4a261;  /* Attention, urgency, amber highlight */
  --color-error:      #ef4444;  /* Error states */
  --color-info:       #60a5fa;  /* Informational */

  /* --- Transport mode badges (from existing codebase) --- */
  --badge-flight-bg:  #1a3a4a;
  --badge-flight-fg:  #90e0ef;
  --badge-ferry-bg:   #1a3a2a;
  --badge-ferry-fg:   #90efbf;
  --badge-taxi-bg:    #3a3a1a;
  --badge-taxi-fg:    #efe090;

  /* --- Price confidence --- */
  --price-great:      #34d399;  /* "Great price" */
  --price-good:       #00b4d8;  /* "Good price" */
  --price-fair:       #f4a261;  /* "Fair price" */
  --price-high:       #ef4444;  /* "Higher than usual" */

  /* --- Interactive states --- */
  --focus-ring:       rgba(0, 180, 216, 0.5);
  --hover-lift:       0 4px 12px rgba(0, 0, 0, 0.3);

  /* --- Gradients --- */
  --gradient-hero:    linear-gradient(135deg, #0077b6 0%, #00b4d8 50%, #90e0ef 100%);
  --gradient-cta:     linear-gradient(135deg, #00b4d8, #0077b6);
  --gradient-loading:  linear-gradient(90deg, #111 25%, #1a1a1a 50%, #111 75%);
}
```

### Spacing Scale

```css
:root {
  --space-1:   4px;
  --space-2:   8px;
  --space-3:   12px;
  --space-4:   16px;
  --space-5:   20px;
  --space-6:   24px;
  --space-8:   32px;
  --space-10:  40px;
  --space-12:  48px;
  --space-16:  64px;
}
```

### Border Radius

```css
:root {
  --radius-sm:   6px;
  --radius-md:   10px;
  --radius-lg:   14px;
  --radius-xl:   20px;
  --radius-full: 9999px;
}
```

### Shadows

```css
:root {
  --shadow-sm:  0 1px 2px rgba(0, 0, 0, 0.2);
  --shadow-md:  0 4px 12px rgba(0, 0, 0, 0.25);
  --shadow-lg:  0 8px 24px rgba(0, 0, 0, 0.3);
  --shadow-xl:  0 16px 48px rgba(0, 0, 0, 0.4);
}
```

### Component Primitives

```css
/* --- Pill button (primary CTA) --- */
.btn-primary {
  background: var(--accent-primary);
  color: var(--text-inverse);
  border: none;
  padding: 12px 28px;
  border-radius: var(--radius-full);
  font-family: var(--font-family);
  font-size: var(--text-base);
  font-weight: var(--weight-semibold);
  cursor: pointer;
  transition: background 0.15s ease, transform 0.1s ease;
  -webkit-tap-highlight-color: transparent;
}
.btn-primary:hover { background: #00c8f0; }
.btn-primary:active { transform: scale(0.97); }
.btn-primary:focus-visible { outline: 3px solid var(--focus-ring); outline-offset: 2px; }
.btn-primary:disabled {
  background: var(--bg-surface-3);
  color: var(--text-tertiary);
  cursor: not-allowed;
}

/* --- Ghost button --- */
.btn-ghost {
  background: transparent;
  color: var(--accent-primary);
  border: 1.5px solid var(--accent-primary);
  padding: 10px 24px;
  border-radius: var(--radius-full);
  font-family: var(--font-family);
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  cursor: pointer;
  transition: background 0.15s ease;
}
.btn-ghost:hover { background: var(--accent-subtle); }

/* --- Card --- */
.card {
  background: var(--bg-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  border: 1px solid transparent;
  transition: border-color 0.15s ease, box-shadow 0.15s ease;
}
.card:hover {
  border-color: var(--bg-surface-3);
  box-shadow: var(--shadow-sm);
}
.card--selected {
  border-color: var(--accent-primary);
  box-shadow: 0 0 0 1px var(--accent-primary);
}

/* --- Section label --- */
.section-label {
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-caps);
  color: var(--accent-primary);
  margin-bottom: var(--space-4);
  padding-bottom: var(--space-2);
  border-bottom: 1px solid var(--bg-surface-3);
}

/* --- Chip / Tag --- */
.chip {
  display: inline-flex;
  align-items: center;
  gap: var(--space-1);
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  background: var(--bg-surface-2);
  color: var(--text-secondary);
  white-space: nowrap;
}
.chip--accent {
  background: var(--accent-subtle);
  color: var(--accent-primary);
}
```

### Layout Container

```css
.container {
  max-width: 680px;   /* Narrower than 720px -- tighter reading column */
  margin: 0 auto;
  padding: 0 var(--space-5);
}

@media (min-width: 768px) {
  .container { padding: 0 var(--space-8); }
}
```

---

## 3. Screen 1: Landing / Entry

### User Emotional State
"I'm the group organiser. Everyone's asking me to figure out flights, ferries, accommodation. I've got 14 browser tabs open. I need help."

### URL
`tripforge.app` (root)

### Layout

The landing page is a single viewport with one job: get the user typing. No feature tours, no testimonials, no pricing. This is a tool, not a SaaS marketing site.

```
+--------------------------------------------------+
|                                                  |
|  [Logo: TripForge wordmark, top-left, small]     |
|                                                  |
|              (vertical center)                   |
|                                                  |
|     Plan your Greek Islands trip.                |
|     Flights. Ferries. Stays. One plan.           |
|                                                  |
|     +--------------------------------------+     |
|     | Tell us about your trip...           |     |
|     |                                      |     |
|     | [multi-line text input, 3 rows]      |     |
|     |                                      |     |
|     |                          [Build Plan]|     |
|     +--------------------------------------+     |
|                                                  |
|     Try: "3 couples, London and Athens to        |
|      Milos and Koufonisia, Aug 14-21"            |
|                                                  |
|     [Skyscanner] [Ferryhopper] [Booking.com]     |
|     "Searches 6+ sources for the best prices"    |
|                                                  |
+--------------------------------------------------+
```

### Detailed Specifications

**Background:** `--bg-base` (`#0a0a0a`) -- solid, no gradients on landing.

**Logo/Wordmark:**
- Position: top-left, `padding: 20px`
- Text: "TripForge" in Inter 600, `--text-base`, `--text-primary`
- No icon. Just text. The tool is the brand.

**Headline:**
```css
.landing-headline {
  font-size: var(--text-2xl);   /* 32px mobile */
  font-weight: var(--weight-bold);
  letter-spacing: var(--tracking-tight);
  color: var(--text-primary);
  line-height: var(--leading-tight);
  margin-bottom: var(--space-2);
}
@media (min-width: 768px) {
  .landing-headline { font-size: var(--text-3xl); } /* 40px desktop */
}
```
- Copy: **"Plan your Greek Islands trip."**

**Subheadline:**
```css
.landing-sub {
  font-size: var(--text-md);    /* 17px */
  font-weight: var(--weight-light);
  color: var(--text-secondary);
  margin-bottom: var(--space-8);
}
```
- Copy: **"Flights. Ferries. Stays. One plan."**

**Text Input Area:**
```css
.brief-input {
  width: 100%;
  min-height: 100px;
  max-height: 200px;
  background: var(--bg-surface);
  border: 1.5px solid var(--bg-surface-3);
  border-radius: var(--radius-lg);
  padding: var(--space-4) var(--space-5);
  padding-bottom: 56px;  /* Space for the button */
  font-family: var(--font-family);
  font-size: var(--text-base);
  font-weight: var(--weight-regular);
  color: var(--text-primary);
  line-height: var(--leading-normal);
  resize: none;
  outline: none;
  transition: border-color 0.15s ease;
}
.brief-input:focus {
  border-color: var(--accent-primary);
}
.brief-input::placeholder {
  color: var(--text-tertiary);
}
```
- Placeholder: **"Tell us about your trip..."**
- The input auto-grows as the user types (up to `max-height`).
- The "Build Plan" button sits inside the input container, bottom-right corner, absolutely positioned.

**Build Plan Button:**
```css
.build-btn {
  position: absolute;
  bottom: 12px;
  right: 12px;
  /* Uses .btn-primary styles */
  padding: 10px 24px;
  font-size: var(--text-sm);
}
```
- Disabled state until the user has typed at least 20 characters.
- Copy: **"Build Plan"** (not "Search" -- we're building something, not just searching).

**Example prompt (below input):**
```css
.example-prompt {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  margin-top: var(--space-3);
  cursor: pointer;
  transition: color 0.15s ease;
}
.example-prompt:hover { color: var(--text-secondary); }
.example-prompt strong {
  color: var(--text-secondary);
  font-weight: var(--weight-medium);
}
```
- Copy: **"Try:"** followed by a clickable example that fills the input.
- Example text: **"3 couples, London and Athens to Milos and Koufonisia, Aug 14-21"**
- On click: animate the text "typing" into the input field at 30ms/char. This is theatrical but effective -- it shows the user exactly what kind of input to give.

**Source logos (trust bar):**
```css
.trust-bar {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-5);
  margin-top: var(--space-10);
  opacity: 0.4;
}
.trust-bar img {
  height: 16px;
  filter: grayscale(1) brightness(2);
}
.trust-bar-label {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  text-align: center;
  margin-top: var(--space-2);
}
```
- Show greyed-out logos of: Skyscanner, Google Flights, Ferryhopper, SeaJets, Booking.com, Airbnb
- Below logos: **"Searches 6+ sources for the best prices"**
- This is the Skyscanner pattern: "searching 1000+ sites" but honest about scale.

### Interactions

1. **Type in the text area** -- The "Build Plan" button becomes active after 20+ characters.
2. **Click example text** -- Fills the input with the example, animating as if typed.
3. **Press Enter (with text)** -- Same as clicking "Build Plan."
4. **Click "Build Plan"** -- Transition to Screen 2 (Confirmation).

### Keyboard Behaviour

- `Cmd+Enter` / `Ctrl+Enter` submits (like Slack/Discord). Important because the input is multi-line so plain Enter creates a newline.
- Announce this with a subtle hint below the button: `Cmd+Enter to submit` in `--text-xs`, `--text-tertiary`.

---

## 4. Screen 2: Trip Builder (Input)

### Why This Screen Exists

At Skyscanner, the biggest conversion killer in multi-city was showing a wall of form fields up front. The Deal Finder Flow inverts this: the user describes their trip in plain text (Screen 1), the AI extracts structure, and Screen 2 shows that structure for confirmation. The user *reviews* rather than *builds*.

However -- and this is critical -- the AI extraction will sometimes be wrong. The user needs to be able to correct it without re-typing. This screen bridges "I said what I want" to "you understood me correctly."

### URL
`tripforge.app/plan?brief=...` (brief text in query param, URL-encoded)

### What Happens

When the user submits their brief, we call the `extract_trip_spec` endpoint. This uses Claude Haiku (fast, <2 seconds) to parse the free text into a `TripSpecification`. While we wait, we show a quick transition state.

### Transition Animation (1-3 seconds)

The text input shrinks and lifts to the top of the screen. Below it, a shimmer animation indicates processing. Copy appears letter by letter:

**"Understanding your trip..."**

```css
.extracting-state {
  text-align: center;
  padding: var(--space-12) 0;
}
.extracting-label {
  font-size: var(--text-md);
  font-weight: var(--weight-medium);
  color: var(--text-secondary);
}
/* Shimmer dots animation */
.extracting-dots::after {
  content: '';
  animation: dots 1.5s infinite;
}
@keyframes dots {
  0%   { content: ''; }
  25%  { content: '.'; }
  50%  { content: '..'; }
  75%  { content: '...'; }
}
```

This should be under 3 seconds. If it takes longer, show a progress message: **"Almost there -- parsing dates and routes..."**

### Confirmation Card Layout

Once extraction completes, the screen resolves into a structured confirmation card. This is the "did we get it right?" moment.

```
+--------------------------------------------------+
|  [< Back]                          TripForge     |
|                                                  |
|  Here's what we understood:                      |
|                                                  |
|  +----------------------------------------------+
|  |                                              |
|  |  GREECE 2026                                 |
|  |  Milos & Koufonisia                          |
|  |                                              |
|  |  [Aug 14] ---- 7 nights ---- [Aug 21]       |
|  |  Fri                                   Fri   |
|  |                                              |
|  |  ............................................|
|  |                                              |
|  |  WHO'S GOING                                 |
|  |                                              |
|  |  +------------------+ +------------------+   |
|  |  | London crew      | | Athens crew      |   |
|  |  | 4 travelers      | | 2 travelers      |   |
|  |  | LON              | | ATH              |   |
|  |  | [Edit]           | | [Edit]           |   |
|  |  +------------------+ +------------------+   |
|  |                                              |
|  |  ............................................|
|  |                                              |
|  |  THE ROUTE                                   |
|  |                                              |
|  |  London --> Athens --> Milos --> Koufonisia   |
|  |        fly        fly     ferry              |
|  |                                              |
|  |  +------- Milos --------+  +- Koufonisia -+  |
|  |  | 5 nights             |  | 2 nights     |  |
|  |  | Aug 14-19            |  | Aug 19-21    |  |
|  |  | Needs car rental     |  | Walk only    |  |
|  |  | [Edit]               |  | [Edit]       |  |
|  |  +----------------------+  +--------------+  |
|  |                                              |
|  |  ............................................|
|  |                                              |
|  |  PREFERENCES                                 |
|  |  [Beach-focused] [Good food] [Mid-range]     |
|  |                                              |
|  +----------------------------------------------+
|                                                  |
|  Anything wrong? Edit above or tell us:          |
|  +----------------------------------------------+
|  | "Actually, make Milos 4 nights..."    [Fix]  |
|  +----------------------------------------------+
|                                                  |
|              [  Find the Best Deals  ]           |
|                                                  |
+--------------------------------------------------+
```

### Detailed Specifications

**Page header:**
```css
.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-4) var(--space-5);
  position: sticky;
  top: 0;
  background: var(--bg-base);
  z-index: 50;
  border-bottom: 1px solid var(--bg-surface-3);
}
.back-btn {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  background: none;
  border: none;
  cursor: pointer;
  font-family: var(--font-family);
  padding: var(--space-2) var(--space-3);
}
```
- "< Back" returns to landing with the text still in the input.

**Introduction copy:**
```css
.confirm-intro {
  font-size: var(--text-lg);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
  margin: var(--space-6) 0 var(--space-5);
}
```
- Copy: **"Here's what we understood:"**

**Trip title (in card):**
```css
.trip-title-display {
  font-size: var(--text-xl);
  font-weight: var(--weight-bold);
  color: var(--text-primary);
  letter-spacing: var(--tracking-tight);
}
.trip-subtitle-display {
  font-size: var(--text-md);
  color: var(--text-secondary);
  font-weight: var(--weight-light);
}
```

**Date range display:**
A horizontal line with dates anchored at each end, total nights in the middle. This immediately communicates duration.

```css
.date-range-bar {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-4) 0;
  margin: var(--space-4) 0;
}
.date-endpoint {
  text-align: center;
}
.date-endpoint .day-name {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  text-transform: uppercase;
}
.date-endpoint .date-value {
  font-size: var(--text-md);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
}
.date-line {
  flex: 1;
  height: 2px;
  background: var(--bg-surface-3);
  position: relative;
}
.date-line .nights-badge {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  background: var(--bg-surface);
  padding: 2px 12px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--accent-primary);
  border: 1px solid var(--bg-surface-3);
}
```

**Origin group cards:**
```css
.origin-card {
  background: var(--bg-surface-2);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  flex: 1;
  min-width: 140px;
}
.origin-label {
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}
.origin-detail {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  line-height: var(--leading-loose);
}
.origin-edit {
  font-size: var(--text-xs);
  color: var(--accent-primary);
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  margin-top: var(--space-2);
  font-weight: var(--weight-medium);
}
```

**Route visualization:**
A horizontal chain of stops with transport mode labels between them.

```css
.route-chain {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: var(--space-1);
  padding: var(--space-4) 0;
}
.route-chain .stop-name {
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
  background: var(--bg-surface-2);
  padding: 4px 14px;
  border-radius: var(--radius-full);
}
.route-chain .transport-label {
  font-size: 0.6875rem; /* 11px */
  color: var(--text-tertiary);
  display: flex;
  align-items: center;
  gap: 4px;
}
.route-chain .transport-label .arrow {
  color: var(--text-tertiary);
}
```

**Island stop cards:**
```css
.stop-card {
  background: var(--bg-surface-2);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  border-left: 3px solid var(--color-warning); /* amber accent for destinations */
}
.stop-card .island-name {
  font-size: var(--text-md);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
}
.stop-card .stop-details {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  margin-top: var(--space-1);
  line-height: var(--leading-loose);
}
.stop-card .car-badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: var(--text-xs);
  color: var(--color-warning);
  margin-top: var(--space-2);
}
```

**Preference chips:**
```css
.pref-chips {
  display: flex;
  flex-wrap: wrap;
  gap: var(--space-2);
  margin-top: var(--space-3);
}
/* Uses .chip styles from design system */
```

**Correction input (below the card):**
This is a secondary text input for quick corrections. Instead of making every field editable (which would recreate a form), the user can type natural language corrections.

```css
.correction-area {
  margin-top: var(--space-5);
}
.correction-label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-2);
}
.correction-input {
  width: 100%;
  background: var(--bg-surface);
  border: 1.5px solid var(--bg-surface-3);
  border-radius: var(--radius-md);
  padding: var(--space-3) var(--space-4);
  padding-right: 64px; /* Space for Fix button */
  font-family: var(--font-family);
  font-size: var(--text-sm);
  color: var(--text-primary);
  outline: none;
  position: relative;
}
.correction-input:focus { border-color: var(--accent-primary); }
.correction-input::placeholder { color: var(--text-tertiary); }
```
- Placeholder examples (rotate every 4 seconds):
  - "Actually, make Milos 4 nights instead..."
  - "We're 2 couples, not 3..."
  - "Can we add Santorini for 2 nights?"
- The "Fix" button inside the input sends the correction to Claude Haiku, which returns an updated `TripSpecification`. The card re-renders with changed fields highlighted briefly in `--accent-primary`.

**Primary CTA:**
```css
.cta-container {
  text-align: center;
  padding: var(--space-8) 0 var(--space-16);
}
.find-deals-btn {
  /* Extends .btn-primary */
  padding: 14px 36px;
  font-size: var(--text-md);
  font-weight: var(--weight-bold);
  box-shadow: 0 0 20px rgba(0, 180, 216, 0.25);
}
```
- Copy: **"Find the Best Deals"** (not "Submit" or "Search" -- this is the promise).
- Below the button, in `--text-xs`, `--text-tertiary`: **"Takes about 30-60 seconds. We'll search flights, ferries, and accommodation."**

### Edit Interactions

Each "Edit" button on origin/stop cards opens a minimal inline edit mode:

```css
.inline-edit {
  background: var(--bg-surface-3);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  margin-top: var(--space-2);
}
.inline-edit input, .inline-edit select {
  background: var(--bg-base);
  border: 1px solid var(--bg-surface-3);
  border-radius: var(--radius-sm);
  padding: var(--space-2) var(--space-3);
  font-family: var(--font-family);
  font-size: var(--text-sm);
  color: var(--text-primary);
  width: 100%;
  margin-bottom: var(--space-2);
}
.inline-edit input:focus { border-color: var(--accent-primary); outline: none; }
.inline-edit-actions {
  display: flex;
  gap: var(--space-2);
  justify-content: flex-end;
}
```

For an origin card edit, the fields shown are:
- City name (text input)
- Number of travelers (number input, 1-10)
- Label (text input, optional)

For a stop card edit:
- Island name (text input with autocomplete from `island_info.json`)
- Number of nights (number input, 1-14)
- Car rental toggle (checkbox)

Save/Cancel buttons use `.btn-primary` (small) and `.btn-ghost` (small).

---

## 5. Screen 3: Confirmation / Edit

This is not a separate screen in the navigation sense. It IS Screen 2. The confirmation view and the edit capabilities live on the same screen. The confirmation card is always visible, always editable.

The critical design decision: **we do not have a separate "edit mode."** Every field is always potentially editable (via the Edit buttons or the correction input), but the default view is read-only and clean. This avoids the "am I in edit mode?" confusion.

### Transition to Research

When the user clicks "Find the Best Deals," the confirmation card collapses upward into a compact summary bar that sticks to the top, and the loading screen takes over the viewport below it.

```css
.trip-summary-bar {
  position: sticky;
  top: 0;
  z-index: 50;
  background: var(--bg-surface);
  border-bottom: 1px solid var(--bg-surface-3);
  padding: var(--space-3) var(--space-5);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.trip-summary-bar .trip-info {
  font-size: var(--text-sm);
  color: var(--text-primary);
  font-weight: var(--weight-medium);
}
.trip-summary-bar .trip-dates {
  font-size: var(--text-xs);
  color: var(--text-secondary);
}
.trip-summary-bar .edit-link {
  font-size: var(--text-xs);
  color: var(--accent-primary);
  cursor: pointer;
  border: none;
  background: none;
}
```

The summary bar shows: **"Greece 2026 -- Milos & Koufonisia -- Aug 14-21 -- 6 travelers"** with an "Edit" link that scrolls back up.

---

## 6. Screen 4: Research / Loading

### User Emotional State
"Is it actually doing anything? How long is this going to take? Am I going to have to start over?"

This is where most travel tools lose people. At Skyscanner, the "searching..." screen was the highest-bounce screen in the funnel. The fix was making the wait *feel* productive -- showing real progress, not a spinning circle.

### URL
Same URL as Screen 2, with a `#searching` hash. This means the back button returns to the confirmation card (important for "wait, I want to change something").

### Layout

```
+--------------------------------------------------+
|  Greece 2026 · Milos & Koufonisia · Aug 14-21    |
|                                         [Edit]   |
+--------------------------------------------------+
|                                                  |
|           Finding the best deals...              |
|                                                  |
|     +--------------------------------------+     |
|     |                                      |     |
|     |  London --> Athens                   |     |
|     |  [=====>            ] Checking       |     |
|     |  flights on 4 airlines               |     |
|     |                                      |     |
|     |  Athens --> Milos                     |     |
|     |  [===============>  ] Found 3        |     |
|     |  flights from EUR45                  |     |
|     |                                      |     |
|     |  Piraeus --> Milos ferry             |     |
|     |  [====================] Found!       |     |
|     |  SeaJets, 2h 35m, EUR76             |     |
|     |                                      |     |
|     |  Milos --> Koufonisia ferry          |     |
|     |  [===========>     ] Checking        |     |
|     |  schedules for Aug 19                |     |
|     |                                      |     |
|     |  Milos accommodation                |     |
|     |  [===============>  ] Found 5        |     |
|     |  places from $118/night              |     |
|     |                                      |     |
|     |  Koufonisia accommodation           |     |
|     |  [======>           ] Searching      |     |
|     |  (only ~20 places on this island)    |     |
|     |                                      |     |
|     |  Return ferries & flights           |     |
|     |  [===>              ] Queued         |     |
|     |                                      |     |
|     +--------------------------------------+     |
|                                                  |
|     Searched 3 of 8 segments                     |
|     [===========            ]                    |
|     Usually takes 30-45 seconds                  |
|                                                  |
+--------------------------------------------------+
```

### Detailed Specifications

**Page headline:**
```css
.loading-headline {
  font-size: var(--text-xl);
  font-weight: var(--weight-bold);
  color: var(--text-primary);
  text-align: center;
  margin: var(--space-8) 0 var(--space-6);
}
```
- Copy: **"Finding the best deals..."**

**Research progress card:**
```css
.research-card {
  background: var(--bg-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-5);
  margin-bottom: var(--space-6);
}

.research-item {
  padding: var(--space-3) 0;
  border-bottom: 1px solid var(--bg-surface-3);
}
.research-item:last-child { border-bottom: none; }

.research-item .label {
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--text-primary);
  margin-bottom: var(--space-1);
}

.research-item .progress-bar {
  height: 3px;
  background: var(--bg-surface-3);
  border-radius: 2px;
  overflow: hidden;
  margin-bottom: var(--space-1);
}
.research-item .progress-bar .fill {
  height: 100%;
  border-radius: 2px;
  transition: width 0.3s ease;
}

/* States */
.research-item.queued .fill { width: 0%; background: var(--text-tertiary); }
.research-item.searching .fill { background: var(--accent-primary); animation: pulse-bar 1.5s ease-in-out infinite; }
.research-item.found .fill { width: 100%; background: var(--color-success); }

@keyframes pulse-bar {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.6; }
}

.research-item .status {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}
.research-item.found .status {
  color: var(--color-success);
}
```

**Status text for each item has three states:**

1. **Queued:** "Queued" (grey text)
2. **Searching:** Dynamic status like "Checking flights on 4 airlines" or "Searching (only ~20 places on this island)" (accent color text)
3. **Found:** Shows result summary like "Found 3 flights from EUR45" or "SeaJets, 2h 35m, EUR76" (green text)

The Koufonisia accommodation item gets special copy: **"Searching (only ~20 places on this island)"** -- this builds urgency and demonstrates domain knowledge.

**Overall progress bar:**
```css
.overall-progress {
  text-align: center;
  margin-top: var(--space-5);
}
.overall-progress .label {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-2);
}
.overall-progress .bar {
  height: 4px;
  background: var(--bg-surface-3);
  border-radius: 2px;
  max-width: 300px;
  margin: 0 auto var(--space-2);
}
.overall-progress .bar .fill {
  height: 100%;
  background: var(--accent-primary);
  border-radius: 2px;
  transition: width 0.5s ease;
}
.overall-progress .time-est {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
}
```
- Copy: **"Searched 3 of 8 segments"** (updates in real time).
- Time estimate: **"Usually takes 30-45 seconds"** -- set honest expectations.

### Real-Time Updates via Server-Sent Events

The research pipeline runs these tasks (from `orchestrator.py`):
1. International flights (each origin to hub)
2. Hub to first island (flight + ferry)
3. Inter-island ferries
4. Return ferries/flights
5. Accommodation per island

Each task reports its status via SSE (Server-Sent Events), which is perfect for this: unidirectional, no WebSocket overhead, works with a simple Python backend.

```
event: research_progress
data: {"task": "flights_london_to_athens", "status": "searching", "detail": "Checking flights on 4 airlines"}

event: research_progress
data: {"task": "flights_london_to_athens", "status": "found", "detail": "Found 5 flights from GBP85", "preview": {"cheapest": 85, "currency": "GBP"}}

event: research_complete
data: {"redirect": "/plan/abc123"}
```

### Keeping the User Engaged

If the search takes more than 20 seconds, start revealing "early results" -- items that have already completed. For example, if flights are found but ferries are still searching:

A card slides in below the progress:
```css
.early-result {
  background: var(--bg-surface);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  margin-top: var(--space-4);
  border-left: 3px solid var(--color-success);
  animation: slideUp 0.3s ease;
}
@keyframes slideUp {
  from { opacity: 0; transform: translateY(12px); }
  to { opacity: 1; transform: translateY(0); }
}
.early-result .early-label {
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--color-success);
  text-transform: uppercase;
  letter-spacing: var(--tracking-wide);
  margin-bottom: var(--space-2);
}
```
- Label: **"EARLY RESULT"**
- Content: **"London to Athens flights from GBP85 (easyJet, Ryanair, BA, Aegean)"**
- This is the Skyscanner "results arriving" pattern -- it keeps the user from bouncing.

### Error Handling

If a specific research task fails (e.g., ferry API timeout), show it as a degraded state:

```css
.research-item.error .fill { width: 100%; background: var(--color-warning); }
.research-item.error .status { color: var(--color-warning); }
```
- Copy: **"Could not check live prices -- using cached data from 2 days ago"** or **"Schedules not yet published -- showing typical August routes"**
- The search continues. We never block on a single failure.

If ALL research fails, show:
```css
.error-state {
  text-align: center;
  padding: var(--space-12) 0;
}
.error-state .icon {
  font-size: 2rem;
  margin-bottom: var(--space-4);
}
.error-state .message {
  font-size: var(--text-md);
  color: var(--text-secondary);
  margin-bottom: var(--space-6);
}
```
- Copy: **"We hit a snag."** / **"Our sources are taking too long to respond. This usually resolves itself -- try again in a minute."**
- CTA: **"Try Again"** (re-runs research with same spec).

---

## 7. Screen 5: Results / Itinerary

### User Emotional State
"Show me the plan. How much is this going to cost? Is this a good deal? What do I need to book first?"

### URL
`tripforge.app/plan/abc123` (unique plan ID, shareable)

### Overview: The Information Architecture

The results page is the existing `itinerary.html.j2` output BUT redesigned as an interactive single-page app instead of a static document. The hierarchy:

1. **Hero** -- Trip name, dates, route visualization (keep existing design)
2. **Price Summary** -- NEW: big bold per-person cost with confidence indicator
3. **Itinerary Timeline** -- Day-by-day plan (enhanced from existing)
4. **Transport Comparison** -- NEW: side-by-side flight/ferry options with "best deal" badges
5. **Accommodation** -- Enhanced from existing, with sorting/filtering
6. **Cost Breakdown** -- Per-origin tabbed cost tables (keep existing)
7. **Booking Checklist** -- Urgency-ordered with progress tracking (enhanced from existing)
8. **Useful Links** -- Grid of search links (keep existing)

### 7.1 Hero Section

Keep the existing hero design from `itinerary.html.j2`. It is already well-designed. One addition:

```css
.hero .powered-by {
  font-size: var(--text-xs);
  color: rgba(255, 255, 255, 0.5);
  margin-top: var(--space-4);
}
```
- Copy: **"Built with TripForge -- prices checked Feb 26, 2026"**

### 7.2 Price Summary Card (NEW)

This is the most important new element. It appears immediately after the hero, before the itinerary. It answers the number one question: "How much?"

```
+--------------------------------------------------+
|  +----------------------------------------------+|
|  |  Estimated cost per person                   ||
|  |                                              ||
|  |    EUR 850 - 1,200                           ||
|  |    -----[===|=======]-----                   ||
|  |    GBP 720 - 1,020 for London crew           ||
|  |                                              ||
|  |  [Good deal for Aug]  Prices checked today   ||
|  +----------------------------------------------+|
+--------------------------------------------------+
```

```css
.price-summary {
  background: var(--bg-surface);
  border-radius: var(--radius-lg);
  padding: var(--space-6);
  margin: calc(-1 * var(--space-6)) var(--space-5) var(--space-6);
  /* Negative top margin to overlap hero slightly */
  position: relative;
  z-index: 10;
  box-shadow: var(--shadow-lg);
}

.price-summary .label {
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  text-transform: uppercase;
  letter-spacing: var(--tracking-caps);
  color: var(--text-secondary);
  margin-bottom: var(--space-3);
}

.price-summary .price-range {
  font-size: 1.75rem; /* 28px -- big and bold */
  font-weight: var(--weight-bold);
  color: var(--text-primary);
  letter-spacing: var(--tracking-tight);
  line-height: 1;
  margin-bottom: var(--space-2);
}

.price-summary .price-bar {
  height: 6px;
  background: var(--bg-surface-3);
  border-radius: 3px;
  position: relative;
  margin: var(--space-3) 0;
}
.price-summary .price-bar .range {
  position: absolute;
  height: 100%;
  border-radius: 3px;
  /* Position and width set dynamically */
}
.price-summary .price-bar .range.great { background: var(--price-great); }
.price-summary .price-bar .range.good { background: var(--price-good); }
.price-summary .price-bar .range.fair { background: var(--price-fair); }

.price-summary .alt-currency {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-bottom: var(--space-3);
}

.price-confidence {
  display: inline-flex;
  align-items: center;
  gap: var(--space-2);
  padding: 4px 12px;
  border-radius: var(--radius-full);
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
}
.price-confidence.good {
  background: rgba(0, 180, 216, 0.12);
  color: var(--accent-primary);
}
.price-confidence.great {
  background: rgba(52, 211, 153, 0.12);
  color: var(--color-success);
}

.price-checked {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  margin-left: var(--space-3);
}
```

**Price confidence indicator logic:**
- Compare per-person cost to typical range for this route/season (from cached historical data).
- Show one of: "Great deal for Aug" (green), "Good deal for Aug" (cyan), "Typical for Aug" (amber).
- This is directly borrowed from Skyscanner's price prediction feature.

### 7.3 Enhanced Itinerary Timeline

The existing day-card design is solid. Enhancements:

**Collapsible transport options:**

For each transport leg, show the cheapest option prominently, with a "See all N options" toggle.

```css
.transport-summary {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  padding: var(--space-3) 0;
}
.transport-summary .mode-badge {
  /* Existing badge styles */
}
.transport-summary .route {
  font-size: var(--text-sm);
  font-weight: var(--weight-medium);
  color: var(--text-primary);
}
.transport-summary .best-price {
  margin-left: auto;
  font-size: var(--text-sm);
  font-weight: var(--weight-bold);
  color: var(--color-success);
}
.transport-summary .option-count {
  font-size: var(--text-xs);
  color: var(--accent-primary);
  cursor: pointer;
  border: none;
  background: none;
  font-family: var(--font-family);
  padding: var(--space-1) 0;
}
```

**Expanded transport options (when toggled):**
```css
.transport-options {
  background: var(--bg-surface-2);
  border-radius: var(--radius-md);
  padding: var(--space-3);
  margin: var(--space-2) 0;
}
.transport-option-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: var(--space-2) var(--space-3);
  border-radius: var(--radius-sm);
  transition: background 0.1s ease;
}
.transport-option-row:hover { background: var(--bg-surface-3); }
.transport-option-row .airline {
  font-size: var(--text-sm);
  color: var(--text-primary);
  font-weight: var(--weight-medium);
}
.transport-option-row .time {
  font-size: var(--text-xs);
  color: var(--text-secondary);
}
.transport-option-row .price {
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
}
.transport-option-row .book-link {
  font-size: var(--text-xs);
  color: var(--accent-primary);
  text-decoration: none;
}
.transport-option-row.best .price {
  color: var(--color-success);
}
.transport-option-row.best::before {
  content: 'Best price';
  font-size: 0.625rem; /* 10px */
  font-weight: var(--weight-semibold);
  color: var(--color-success);
  background: rgba(52, 211, 153, 0.12);
  padding: 2px 6px;
  border-radius: var(--radius-full);
  margin-right: var(--space-2);
}
```

### 7.4 Accommodation Section

Keep the existing layout but add sorting controls and a "best value" badge.

**Sort/filter bar:**
```css
.acc-controls {
  display: flex;
  gap: var(--space-2);
  margin-bottom: var(--space-3);
  overflow-x: auto;
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
}
.acc-controls::-webkit-scrollbar { display: none; }

.sort-chip {
  /* Uses .chip styles */
  cursor: pointer;
  border: none;
  font-family: var(--font-family);
  transition: background 0.1s ease, color 0.1s ease;
}
.sort-chip.active {
  background: var(--accent-primary);
  color: var(--text-inverse);
}
```
- Sort options: **"Best value"** (default: rating/price ratio), **"Cheapest"**, **"Top rated"**, **"Closest to port"**

**"Best value" badge on top accommodation:**
```css
.best-value-badge {
  font-size: var(--text-xs);
  font-weight: var(--weight-semibold);
  color: var(--color-success);
  background: rgba(52, 211, 153, 0.1);
  padding: 2px 8px;
  border-radius: var(--radius-full);
  margin-left: var(--space-2);
}
```

### 7.5 Cost Breakdown

Keep the existing tabbed cost breakdown exactly as-is. It works well. One addition: add a "Split with group" toggle.

```css
.split-toggle {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  margin-bottom: var(--space-4);
  font-size: var(--text-sm);
  color: var(--text-secondary);
}
.split-toggle input[type="checkbox"] {
  accent-color: var(--accent-primary);
  width: 16px;
  height: 16px;
}
```
- Label: **"Show costs per couple (split between 2)"** -- toggling this divides accommodation costs by 2 and recalculates the total.

### 7.6 Booking Checklist

Enhanced version of the existing checklist with visual progress:

```css
.checklist-progress {
  display: flex;
  align-items: center;
  gap: var(--space-3);
  margin-bottom: var(--space-4);
  padding: var(--space-3) var(--space-4);
  background: var(--bg-surface);
  border-radius: var(--radius-md);
}
.checklist-progress .bar {
  flex: 1;
  height: 4px;
  background: var(--bg-surface-3);
  border-radius: 2px;
}
.checklist-progress .bar .fill {
  height: 100%;
  background: var(--color-success);
  border-radius: 2px;
  transition: width 0.3s ease;
}
.checklist-progress .label {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  white-space: nowrap;
}
```
- Label: **"2 of 7 booked"** (updates as items are checked).

### 7.7 Sticky Bottom Bar

Enhanced from existing:

```css
.sticky-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: rgba(10, 10, 10, 0.92);
  backdrop-filter: blur(16px);
  -webkit-backdrop-filter: blur(16px);
  border-top: 1px solid var(--bg-surface-3);
  padding: var(--space-3) var(--space-5);
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 100;
}

.sticky-bar .cost-summary {
  font-size: var(--text-xs);
  color: var(--text-secondary);
  line-height: 1.3;
}
.sticky-bar .cost-summary strong {
  display: block;
  font-size: var(--text-md);
  font-weight: var(--weight-bold);
  color: var(--accent-primary);
}

.sticky-bar .share-btn {
  display: flex;
  align-items: center;
  gap: var(--space-2);
  background: #25D366;  /* WhatsApp green */
  color: #fff;
  border: none;
  padding: 10px 20px;
  border-radius: var(--radius-full);
  font-size: var(--text-sm);
  font-weight: var(--weight-semibold);
  cursor: pointer;
  font-family: var(--font-family);
  transition: background 0.15s ease;
}
.sticky-bar .share-btn:hover { background: #20BD5C; }
```
- Share button is WhatsApp green, not cyan. This is intentional: the primary action at this point is sharing to the group. WhatsApp green is the most recognizable CTA color for the target user.
- Copy: **"Share to Group"** (not just "Share").
- The WhatsApp icon (inline SVG, 16x16) sits before the text.

---

## 8. Screen 6: Share Flow

### User Emotional State
"I want to send this to the group chat and look like I've got everything figured out."

### Share Button Behaviour

When the user taps "Share to Group," we use a two-step flow:

**Step 1: Share preview modal**

```
+--------------------------------------------------+
|                                                  |
|     (overlay dims the page)                      |
|                                                  |
|     +--------------------------------------+     |
|     |  Share your trip plan                |     |
|     |                                      |     |
|     |  +--------------------------------+  |     |
|     |  |  Greece 2026                   |  |     |
|     |  |  Milos & Koufonisia            |  |     |
|     |  |  Aug 14-21 · 3 couples         |  |     |
|     |  |  ~EUR850-1200 per person       |  |     |
|     |  |  tripforge.app/plan/abc123     |  |     |
|     |  +--------------------------------+  |     |
|     |                                      |     |
|     |  This is what they'll see in the     |     |
|     |  chat preview.                       |     |
|     |                                      |     |
|     |  [  Share on WhatsApp  ]             |     |
|     |                                      |     |
|     |  [Copy Link]  [Share...]             |     |
|     |                                      |     |
|     +--------------------------------------+     |
|                                                  |
+--------------------------------------------------+
```

```css
.share-modal {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: var(--bg-overlay);
  display: flex;
  align-items: flex-end;   /* Bottom sheet on mobile */
  justify-content: center;
  z-index: 200;
  padding: var(--space-5);
}

@media (min-width: 768px) {
  .share-modal { align-items: center; } /* Centered on desktop */
}

.share-modal .panel {
  background: var(--bg-surface);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  width: 100%;
  max-width: 420px;
  padding: var(--space-6);
  animation: slideUpSheet 0.25s ease;
}

@media (min-width: 768px) {
  .share-modal .panel {
    border-radius: var(--radius-lg);
  }
}

@keyframes slideUpSheet {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.share-modal .panel-title {
  font-size: var(--text-lg);
  font-weight: var(--weight-bold);
  color: var(--text-primary);
  margin-bottom: var(--space-5);
}

.share-preview {
  background: var(--bg-surface-2);
  border-radius: var(--radius-md);
  padding: var(--space-4);
  margin-bottom: var(--space-5);
  border: 1px solid var(--bg-surface-3);
}
.share-preview .preview-title {
  font-size: var(--text-md);
  font-weight: var(--weight-semibold);
  color: var(--text-primary);
}
.share-preview .preview-sub {
  font-size: var(--text-sm);
  color: var(--text-secondary);
  margin-top: var(--space-1);
}
.share-preview .preview-meta {
  font-size: var(--text-xs);
  color: var(--text-tertiary);
  margin-top: var(--space-1);
}
.share-preview .preview-url {
  font-size: var(--text-xs);
  color: var(--accent-primary);
  margin-top: var(--space-2);
  font-family: 'SF Mono', 'Fira Code', monospace;
}

.share-context {
  font-size: var(--text-sm);
  color: var(--text-tertiary);
  margin-bottom: var(--space-5);
}

.share-whatsapp {
  /* Full-width WhatsApp button */
  width: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: var(--space-2);
  background: #25D366;
  color: #fff;
  border: none;
  padding: 14px 24px;
  border-radius: var(--radius-md);
  font-size: var(--text-base);
  font-weight: var(--weight-semibold);
  cursor: pointer;
  font-family: var(--font-family);
  margin-bottom: var(--space-3);
}
.share-whatsapp:hover { background: #20BD5C; }

.share-secondary {
  display: flex;
  gap: var(--space-3);
  justify-content: center;
}
.share-secondary button {
  background: none;
  border: none;
  color: var(--text-secondary);
  font-size: var(--text-sm);
  cursor: pointer;
  padding: var(--space-2);
  font-family: var(--font-family);
}
.share-secondary button:hover { color: var(--accent-primary); }
```

**WhatsApp share link construction:**

The WhatsApp share URL sends a pre-composed message:

```
https://wa.me/?text=Greece%202026%20%F0%9F%87%AC%F0%9F%87%B7%0A%0AMilos%20%26%20Koufonisia%0AAug%2014-21%20%C2%B7%203%20couples%0A~%E2%82%AC850-1%2C200%20per%20person%0A%0AI%20put%20together%20the%20full%20plan%20with%20flights%2C%20ferries%2C%20accommodation%20%26%20costs%3A%0Ahttps%3A%2F%2Ftripforge.app%2Fplan%2Fabc123
```

Which decodes to:
```
Greece 2026

Milos & Koufonisia
Aug 14-21 · 3 couples
~EUR850-1,200 per person

I put together the full plan with flights, ferries, accommodation & costs:
https://tripforge.app/plan/abc123
```

Note: No emoji in the design doc text itself, but the WhatsApp message uses a Greek flag emoji as this is a messaging context where emoji is expected and functional (it makes the link preview more visually distinctive in a busy group chat).

**"Copy Link" behaviour:**
- Copies `https://tripforge.app/plan/abc123` to clipboard.
- Button text changes to "Copied!" for 2 seconds.
- Uses `navigator.clipboard.writeText()`.

**"Share..." behaviour:**
- Uses `navigator.share()` Web Share API (available on iOS Safari, Android Chrome).
- Shares title + URL. Falls back to "Copy Link" on unsupported browsers.

### OG Meta Tags for Link Previews

These are critical. When the link is pasted in WhatsApp, iMessage, or any other chat app, the preview card must look polished. The existing template has basic OG tags; we need to expand them:

```html
<meta property="og:title" content="Greece 2026 — Milos & Koufonisia">
<meta property="og:description" content="Aug 14-21 · 3 couples · ~EUR850-1,200pp · Flights, ferries, accommodation & costs all planned out">
<meta property="og:type" content="website">
<meta property="og:url" content="https://tripforge.app/plan/abc123">
<meta property="og:image" content="https://tripforge.app/plan/abc123/og-image.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
```

**OG image generation:** Server-side, generate a 1200x630px PNG with:
- Background: the hero gradient (`--gradient-hero`)
- White text: trip title, dates, route chain, estimated cost
- TripForge wordmark in bottom-right corner
- This can be generated with Pillow or a headless browser screenshot of a template

---

## 9. Screen 7: Recipient View

### User Emotional State
"Someone in my group sent a link. Let me see what the plan is."

### URL
Same URL: `tripforge.app/plan/abc123`

### What Recipients See

Recipients see the EXACT same page as the organiser. There is no reduced view, no "upgrade to see more" gate, no account wall. This is critical for the product to work:

- The plan must be self-contained and complete.
- The recipient must be able to check every price, click every booking link.
- The recipient must be able to use the checklist to track bookings.

### Differences from Organiser View

The only differences:

1. **No sticky bottom bar "Share to Group" button.** Instead, the sticky bar shows just the price summary and a "Start your own plan" link.

```css
.sticky-bar.recipient .share-btn {
  background: transparent;
  border: 1.5px solid var(--accent-primary);
  color: var(--accent-primary);
}
```
- Copy: **"Plan your own trip"** -- links to the landing page.

2. **A subtle banner at the very top:**
```css
.shared-banner {
  background: var(--accent-subtle);
  padding: var(--space-2) var(--space-5);
  text-align: center;
  font-size: var(--text-xs);
  color: var(--accent-primary);
}
```
- Copy: **"Trip plan shared by [Organiser Name]. Prices checked [date]."**
- If no organiser name is set: **"Trip plan created with TripForge. Prices checked [date]."**

3. **Checklist state is per-device (localStorage).** So each recipient can track their own bookings independently.

### Mobile Optimisation

The recipient view must be perfect on mobile. The person receiving this link is reading it in WhatsApp, which means they're tapping through on their phone's default browser. Key considerations:

- All content is single-column, max-width 680px.
- Touch targets are at least 44px tall.
- No horizontal scrolling anywhere.
- The `@media (max-width: 600px)` breakpoint from the existing template is correct; we keep all those overrides.
- `font-size: 16px` minimum on inputs (prevents iOS zoom-on-focus).

---

## 10. State Management & Transitions

### Application States

The app has 6 states, managed via URL:

```
STATE           URL                           DESCRIPTION
─────           ───                           ───────────
landing         /                             Text input, empty
extracting      /plan?brief=...               Brief submitted, AI parsing
confirming      /plan?brief=...#confirm       Spec extracted, user reviewing
researching     /plan?brief=...#searching     Research running, SSE updates
results         /plan/{id}                    Plan generated, viewing
error           /plan?brief=...#error         Research failed
```

### Transition Animations

All transitions use a consistent slide+fade:

```css
.screen-enter {
  animation: screenEnter 0.3s ease forwards;
}
@keyframes screenEnter {
  from { opacity: 0; transform: translateY(16px); }
  to { opacity: 1; transform: translateY(0); }
}

.screen-exit {
  animation: screenExit 0.2s ease forwards;
}
@keyframes screenExit {
  from { opacity: 1; transform: translateY(0); }
  to { opacity: 0; transform: translateY(-8px); }
}
```

### Data Flow

```
User types brief
       |
       v
POST /api/extract  (brief text)
       |
       v
Claude Haiku returns TripSpecification JSON
       |
       v
User reviews/edits on confirmation screen
       |
       v
POST /api/research  (TripSpecification JSON)
       |
       v
SSE stream: research_progress events
       |
       v
Final event: research_complete with plan ID
       |
       v
GET /plan/{id}  (server-rendered HTML)
```

### Persistence

- **Plans are stored server-side** with a unique ID (UUID or short hash like `abc123`). This means the URL is shareable immediately.
- **No user accounts.** The plan URL is the "account." Whoever has the URL can view it.
- **Checklist state is client-side** (localStorage). This is intentional: different group members track their own bookings.
- **Plans expire after 30 days** (or configurable). Show a banner if viewing an expired plan: "This plan was created over 30 days ago. Prices may have changed significantly."

---

## 11. Implementation Architecture

### What Needs to Change from Current Codebase

The current codebase (`/Users/gerinicka-new/holiday-planner`) is a CLI tool. To implement this UX:

**1. Add a web server layer.**

Use FastAPI (already in the Python ecosystem alongside Pydantic models):

```
New files:
  server.py              -- FastAPI app, routes, SSE endpoint
  templates/landing.html -- Landing page template
  templates/confirm.html -- Confirmation/edit template
  templates/loading.html -- Loading screen (mostly client-side JS)
  static/app.css         -- Design system CSS (extracted from this doc)
  static/app.js          -- Client-side interactions (~200 lines)
```

**2. Refactor the existing orchestrator for SSE.**

The `run_orchestrator()` in `agents/orchestrator.py` already runs research tasks in parallel via `run_parallel_research()`. Wrap this to yield progress events:

```python
async def run_orchestrator_streaming(spec: TripSpecification):
    """Yield SSE events as research progresses."""
    # ... yields {"task": "...", "status": "searching"} events
    # ... yields {"task": "...", "status": "found", "preview": {...}} events
    # ... yields {"status": "complete", "plan_id": "abc123"} at end
```

**3. Add plan storage.**

Simple SQLite (or even JSON files in an `output/plans/` directory keyed by plan ID). The plan ID maps to the rendered Itinerary JSON.

**4. Keep the existing template.**

`templates/itinerary.html.j2` becomes the results page. Add the new elements (price summary card, transport comparison, sort controls) without breaking the existing structure.

### API Endpoints

```
POST /api/extract
  Body: { "brief": "3 couples, London and Athens..." }
  Response: TripSpecification JSON

POST /api/extract/correct
  Body: { "spec": TripSpecification, "correction": "Make Milos 4 nights" }
  Response: Updated TripSpecification JSON

POST /api/research
  Body: TripSpecification JSON
  Response: SSE stream of progress events, final event has plan_id

GET /plan/{plan_id}
  Response: Rendered HTML page (the itinerary)

GET /plan/{plan_id}/og-image.png
  Response: Generated OG image for social sharing
```

### JS Budget

Target: under 300 lines of vanilla JS, no framework. The interactions are:
- Text input auto-grow
- Example prompt "typing" animation
- Inline edit toggles on confirmation screen
- Correction input submission
- SSE listener for research progress
- Accommodation sort controls
- Cost tab switching (existing)
- Checklist localStorage (existing)
- Share modal open/close
- Share/copy actions

No React. No Vue. No build step. This is a progressive enhancement layer on top of server-rendered HTML.

---

## Appendix A: Microcopy Reference

| Location | Copy | Notes |
|----------|------|-------|
| Landing headline | "Plan your Greek Islands trip." | Period, not exclamation. Calm confidence. |
| Landing subheadline | "Flights. Ferries. Stays. One plan." | Staccato rhythm. Lists what we do. |
| Landing example prefix | "Try:" | Lowercase "try", not "TRY" or "Example:" |
| Landing trust bar | "Searches 6+ sources for the best prices" | "6+" not exact number. "Best prices" not "lowest prices." |
| Input placeholder | "Tell us about your trip..." | Ellipsis invites continuation. |
| Build Plan button | "Build Plan" | Active verb. We're building, not just searching. |
| Extraction loading | "Understanding your trip..." | "Understanding" not "Processing." Human language. |
| Confirmation intro | "Here's what we understood:" | Colon invites them to check. "Understood" implies intelligence. |
| Correction prompt | "Anything wrong? Edit above or tell us:" | Two paths: edit directly or describe the fix. |
| Correction placeholder | "Actually, make Milos 4 nights instead..." | "Actually" is conversational. Rotate examples. |
| Primary CTA | "Find the Best Deals" | "Best Deals" is the promise. Capitalized for emphasis. |
| CTA subtext | "Takes about 30-60 seconds. We'll search flights, ferries, and accommodation." | Set expectations honestly. |
| Loading headline | "Finding the best deals..." | Matches the CTA copy. Continuity. |
| Loading progress | "Searched 3 of 8 segments" | Concrete progress, not vague "almost there." |
| Loading time est | "Usually takes 30-45 seconds" | "Usually" hedges honestly. |
| Koufonisia special | "Searching (only ~20 places on this island)" | Domain expertise. Builds trust and urgency. |
| Error state | "We hit a snag." / "Try again in a minute." | Casual, not apologetic. Practical suggestion. |
| Price confidence | "Good deal for Aug" | Month name, not "this time of year." Specific. |
| Sticky bar share | "Share to Group" | "to Group" not "with friends." The persona is an organiser. |
| Share modal title | "Share your trip plan" | "Your" -- they own it, they built it. |
| Share modal context | "This is what they'll see in the chat preview." | Manage expectations about the preview card. |
| WhatsApp button | "Share on WhatsApp" | Platform-specific, not generic "Share." |
| WhatsApp message last line | "I put together the full plan with flights, ferries, accommodation & costs:" | "I put together" -- gives the organiser credit. First person. |
| Recipient banner | "Trip plan shared by [Name]. Prices checked [date]." | Provenance and freshness. |
| Expired plan | "This plan was created over 30 days ago. Prices may have changed significantly." | Honest about staleness. |
| Footer | "Prices are estimates, check links for live availability" | Legal/trust. Already exists. Keep it. |

## Appendix B: Animation Timing Reference

| Animation | Duration | Easing | Trigger |
|-----------|----------|--------|---------|
| Button hover | 150ms | ease | :hover |
| Button press | 100ms | ease | :active |
| Screen transition in | 300ms | ease | State change |
| Screen transition out | 200ms | ease | State change |
| Share modal slide up | 250ms | ease | Share button tap |
| Progress bar fill | 300ms | ease | SSE update |
| Early result card | 300ms | ease | SSE found event |
| Example text typing | 30ms/char | linear | Click on example |
| Correction field highlight | 400ms | ease-out | Spec updated |
| Input border focus | 150ms | ease | :focus |
| Card hover lift | 150ms | ease | :hover |

## Appendix C: Responsive Breakpoints

```css
/* Mobile first. These are the only breakpoints needed. */

/* Small mobile (iPhone SE) */
@media (max-width: 374px) {
  .hero h1 { font-size: 1.75rem; }
  .price-summary .price-range { font-size: 1.5rem; }
  .sticky-bar { padding: var(--space-3) var(--space-4); }
}

/* Standard mobile (default) */
/* No media query -- this is the base */

/* Tablet / small desktop */
@media (min-width: 768px) {
  .container { max-width: 680px; padding: 0 var(--space-8); }
  .hero { padding: 72px 32px 56px; }
  .hero h1 { font-size: var(--text-3xl); }
  .share-modal { align-items: center; }
  .origin-cards { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-3); }
  .stop-cards { display: grid; grid-template-columns: 1fr 1fr; gap: var(--space-3); }
}

/* Desktop (rare for this product, but handle it) */
@media (min-width: 1024px) {
  .container { max-width: 720px; }
}
```

---

## Summary: What Makes This "Option B" Different

The Deal Finder Flow is built around three principles that differentiate it from a standard trip planning tool:

**1. Text-first input, form-second.**
The user describes their trip naturally. The AI does the structuring. The confirmation screen is a review step, not a data entry step. This inverts the typical travel booking form pattern and removes the biggest friction point.

**2. Visible research, not hidden loading.**
The loading screen shows every search being run, every result as it arrives. This is not a cosmetic choice -- it builds genuine confidence that we checked everywhere. The user sees "Checking flights on 4 airlines" and "Searching (only ~20 places on this island)" and knows this tool understands their trip.

**3. The output is the product.**
The shareable itinerary page is not a summary or a teaser. It is the complete, detailed, actionable plan with real booking links, real prices, and a real checklist. The organiser shares this one URL and their job is done. The group trusts it because it looks thorough, shows its sources, and lets each person verify independently.

This is the UX that the current CLI/YAML pipeline deserves. The data models (`TripSpecification`, `Itinerary`) are already correct. The research pipeline is already built. The HTML template is already 80% there. What is missing is the interaction layer that turns a developer tool into a product that earns the organiser's trust and makes them look good in the group chat.
