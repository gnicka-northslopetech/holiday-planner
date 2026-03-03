# Option A: The Wanderlust Flow

## Complete UX Design Document for TripForge

**Author:** Product Design
**Date:** February 2026
**Status:** Ready for implementation
**Target platform:** Mobile-first responsive web app (single page, minimal JS)

---

## Table of Contents

1. [Design Philosophy & Foundations](#1-design-philosophy--foundations)
2. [Design System](#2-design-system)
3. [Screen 1: Landing / Entry](#3-screen-1-landing--entry)
4. [Screen 2: The Brief (Input)](#4-screen-2-the-brief-input)
5. [Screen 3: Confirmation / Edit](#5-screen-3-confirmation--edit)
6. [Screen 4: Research / Loading](#6-screen-4-research--loading)
7. [Screen 5: The Itinerary (Results)](#7-screen-5-the-itinerary-results)
8. [Screen 6: Share Flow](#8-screen-6-share-flow)
9. [Screen 7: Recipient / Post-Share View](#9-screen-7-recipient--post-share-view)
10. [Interaction Map & State Transitions](#10-interaction-map--state-transitions)
11. [Implementation Notes](#11-implementation-notes)

---

## 1. Design Philosophy & Foundations

### The Core Insight

The Group Organiser is doing unpaid labour. They spend 8-15 hours across browser tabs, Google Docs, WhatsApp threads, and spreadsheets. They do this because they care. They do this because nobody else will. And when they finally share the plan, the response is "looks good!" in 3 seconds.

TripForge should make the organiser feel competent, not overwhelmed. It should make their output look professional enough that the group responds with "holy shit, this is amazing." The organiser's reward is recognition. We are building a tool that manufactures that recognition.

### Design Principles

1. **Warmth over efficiency.** This is a holiday, not a boarding pass. Every screen should feel like opening a travel magazine, not filing a form.
2. **Progressive disclosure.** Show only what matters at each step. The organiser already knows what they want -- we need to prove we understood them, then get out of the way.
3. **Photography-driven trust.** Real images of Greek islands create instant emotional buy-in. They say "we know these places" without a single word.
4. **Shareable by default.** The output is the product. If it does not look stunning on a phone screen in WhatsApp, nothing else matters.
5. **Respect the organiser's knowledge.** They have already researched. Do not quiz them. Let them tell us in their own words, then show them we got it.

### Emotional Arc

```
Landing:     Anticipation  →  "This understands trips like mine"
Input:       Confidence     →  "I can just say what I want"
Confirm:     Control        →  "It got it right, and I can fix what it didn't"
Loading:     Excitement     →  "It's actually doing the research for me"
Results:     Pride          →  "This looks incredible. I made this."
Share:       Recognition    →  "Everyone is going to love this"
Post-share:  Trust          →  "This is real, I can actually book from this"
```

---

## 2. Design System

### Color Palette

The current implementation uses a dark theme with cyan accents (#00b4d8). This is fine for a dev prototype but reads as "dashboard" not "holiday." We shift to a warm, light-dominant palette inspired by the Aegean.

```css
:root {
  /* ── Primary palette ── */
  --white:           #FFFFFF;
  --sand:            #FAF7F2;        /* Page background — warm off-white */
  --sand-dark:       #F0EBE3;        /* Card hover, subtle borders */
  --stone:           #E8E2D9;        /* Dividers, rules */

  /* ── Text ── */
  --ink:             #1A1A1A;        /* Primary text */
  --ink-secondary:   #6B6560;        /* Secondary/meta text */
  --ink-tertiary:    #A39E97;        /* Placeholder, disabled */

  /* ── Accent: Aegean ── */
  --aegean:          #1E6B8A;        /* Primary action color — deep teal-blue */
  --aegean-light:    #E8F4F8;        /* Badge background, selected states */
  --aegean-hover:    #175A75;        /* Button hover */

  /* ── Accent: Sunset ── */
  --sunset:          #E07A4F;        /* Highlight accent — terracotta orange */
  --sunset-light:    #FFF0E8;        /* Highlight badge backgrounds */
  --sunset-hover:    #C96A42;

  /* ── Accent: Sea ── */
  --sea:             #2D9B83;        /* Success, confirmations — Mediterranean green */
  --sea-light:       #E6F7F3;

  /* ── Transport badges ── */
  --badge-flight-bg: #E8F4F8;
  --badge-flight-fg: #1E6B8A;
  --badge-ferry-bg:  #E6F7F3;
  --badge-ferry-fg:  #1B7A62;
  --badge-taxi-bg:   #FFF6E8;
  --badge-taxi-fg:   #9A7320;

  /* ── Shadows ── */
  --shadow-sm:       0 1px 3px rgba(0,0,0,0.06);
  --shadow-md:       0 4px 12px rgba(0,0,0,0.08);
  --shadow-lg:       0 8px 30px rgba(0,0,0,0.12);

  /* ── Radii ── */
  --radius-sm:       8px;
  --radius-md:       12px;
  --radius-lg:       16px;
  --radius-xl:       24px;
  --radius-full:     9999px;
}
```

### Typography

Replace Inter with a serif/sans-serif pairing that signals editorial quality.

```css
@import url('https://fonts.googleapis.com/css2?family=DM+Serif+Display&family=Inter:wght@300;400;500;600&display=swap');

:root {
  --font-display:    'DM Serif Display', Georgia, serif;
  --font-body:       'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

/* Type scale */
.type-hero {
  font-family: var(--font-display);
  font-size: 2.5rem;       /* 40px */
  line-height: 1.15;
  letter-spacing: -0.5px;
  color: var(--ink);
}

.type-h1 {
  font-family: var(--font-display);
  font-size: 1.75rem;      /* 28px */
  line-height: 1.25;
  color: var(--ink);
}

.type-h2 {
  font-family: var(--font-body);
  font-size: 1.125rem;     /* 18px */
  font-weight: 600;
  line-height: 1.35;
  color: var(--ink);
}

.type-h3 {
  font-family: var(--font-body);
  font-size: 0.9375rem;    /* 15px */
  font-weight: 600;
  line-height: 1.4;
  color: var(--ink);
}

.type-body {
  font-family: var(--font-body);
  font-size: 0.9375rem;    /* 15px */
  font-weight: 400;
  line-height: 1.6;
  color: var(--ink);
}

.type-small {
  font-family: var(--font-body);
  font-size: 0.8125rem;    /* 13px */
  font-weight: 400;
  line-height: 1.5;
  color: var(--ink-secondary);
}

.type-caption {
  font-family: var(--font-body);
  font-size: 0.6875rem;    /* 11px */
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: var(--ink-tertiary);
}
```

### Spacing Scale

```css
/* 4px base unit */
--space-1:  4px;
--space-2:  8px;
--space-3:  12px;
--space-4:  16px;
--space-5:  20px;
--space-6:  24px;
--space-8:  32px;
--space-10: 40px;
--space-12: 48px;
--space-16: 64px;
--space-20: 80px;
```

### Layout

```css
.page-container {
  max-width: 680px;
  margin: 0 auto;
  padding: 0 20px;
}

/* Mobile: 20px side padding
   Tablet+: centered 680px max-width column */
```

### Component Patterns

**Primary Button**
```css
.btn-primary {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  padding: 14px 28px;
  background: var(--ink);
  color: var(--white);
  border: none;
  border-radius: var(--radius-full);
  font-family: var(--font-body);
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease, transform 0.1s ease;
}
.btn-primary:hover { background: #333; }
.btn-primary:active { transform: scale(0.98); }
```

**Secondary Button**
```css
.btn-secondary {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--white);
  color: var(--ink);
  border: 1.5px solid var(--stone);
  border-radius: var(--radius-full);
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: border-color 0.15s ease, background 0.15s ease;
}
.btn-secondary:hover {
  border-color: var(--ink-secondary);
  background: var(--sand);
}
```

**Card**
```css
.card {
  background: var(--white);
  border-radius: var(--radius-md);
  padding: 20px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--stone);
  transition: box-shadow 0.2s ease;
}
.card:hover { box-shadow: var(--shadow-md); }
```

**Badge**
```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 3px 10px;
  border-radius: var(--radius-sm);
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
}
.badge-flight { background: var(--badge-flight-bg); color: var(--badge-flight-fg); }
.badge-ferry  { background: var(--badge-ferry-bg);  color: var(--badge-ferry-fg); }
.badge-taxi   { background: var(--badge-taxi-bg);   color: var(--badge-taxi-fg); }
```

---

## 3. Screen 1: Landing / Entry

### URL: `tripforge.app/`

### Emotional Target: Anticipation + "This is for someone exactly like me"

### Layout

The landing page is a single-scroll page, hero-heavy, designed to get the user to the input screen in under 10 seconds. No signup. No accounts. No friction.

```
┌────────────────────────────────────────────┐
│                                            │
│  [Full-bleed hero image: aerial shot of    │
│   Greek island coastline, turquoise water, │
│   white village visible. Soft warm filter] │
│                                            │
│         TripForge                           │
│                                            │
│   Your Greek island trip,                  │
│   planned in 60 seconds.                   │
│                                            │
│   Tell us about your trip in plain          │
│   English. We'll find the flights,         │
│   ferries, and places to stay — and        │
│   build a page you can share with          │
│   your group.                              │
│                                            │
│       [ Start planning  ->  ]              │
│                                            │
│   No account needed. Free while in beta.   │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  HOW IT WORKS                              │
│                                            │
│  ① Describe your trip                      │
│     "4 of us from London, Milos +          │
│      Koufonisia, mid-August, 7 nights"     │
│                                            │
│  ② We do the research                      │
│     Flights, ferries, accommodation,       │
│     costs — all assembled in 60 seconds    │
│                                            │
│  ③ Share one beautiful page                │
│     Drop it in your group chat. Everyone   │
│     sees the plan, the prices, the links   │
│     to book.                               │
│                                            │
├────────────────────────────────────────────┤
│                                            │
│  [Example itinerary screenshot/preview     │
│   — a tasteful mockup showing the output   │
│   card for a Milos trip, slightly tilted,  │
│   with a phone frame around it. Below:]    │
│                                            │
│  "Made for the person who does all the     │
│   research so everyone else doesn't        │
│   have to."                                │
│                                            │
│       [ Start planning  ->  ]              │
│                                            │
├────────────────────────────────────────────┤
│  TripForge · Prices are estimates ·        │
│  Not a booking platform                    │
└────────────────────────────────────────────┘
```

### Specific CSS for the Hero

```css
.landing-hero {
  position: relative;
  min-height: 85vh;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 24px;
  overflow: hidden;
}

.landing-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/images/hero-milos-aerial.jpg') center/cover no-repeat;
  filter: brightness(0.55) saturate(1.1);
  z-index: 0;
}

.landing-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(26, 26, 26, 0.2) 0%,
    rgba(26, 26, 26, 0.5) 60%,
    rgba(26, 26, 26, 0.8) 100%
  );
  z-index: 1;
}

.landing-hero > * {
  position: relative;
  z-index: 2;
}

.landing-logo {
  font-family: var(--font-body);
  font-size: 0.8125rem;
  font-weight: 600;
  letter-spacing: 3px;
  text-transform: uppercase;
  color: rgba(255, 255, 255, 0.7);
  margin-bottom: 24px;
}

.landing-headline {
  font-family: var(--font-display);
  font-size: clamp(2rem, 5vw, 3.25rem);
  line-height: 1.1;
  color: #FFFFFF;
  max-width: 480px;
  margin-bottom: 16px;
}

.landing-subhead {
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 400;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.8);
  max-width: 400px;
  margin-bottom: 32px;
}

.landing-cta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 16px 32px;
  background: var(--white);
  color: var(--ink);
  border: none;
  border-radius: var(--radius-full);
  font-family: var(--font-body);
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: transform 0.15s ease, box-shadow 0.15s ease;
  box-shadow: 0 4px 20px rgba(0,0,0,0.2);
}

.landing-cta:hover {
  transform: translateY(-1px);
  box-shadow: 0 6px 24px rgba(0,0,0,0.25);
}

.landing-cta svg {
  width: 18px;
  height: 18px;
  transition: transform 0.15s ease;
}

.landing-cta:hover svg {
  transform: translateX(3px);
}

.landing-fine-print {
  font-size: 0.75rem;
  color: rgba(255, 255, 255, 0.5);
  margin-top: 16px;
}
```

### Microcopy

- **Logo text:** `TRIPFORGE`
- **Headline:** `Your Greek island trip, planned in 60 seconds.`
- **Subhead:** `Tell us about your trip in plain English. We'll find the flights, ferries, and places to stay -- and build a page you can share with your group.`
- **CTA:** `Start planning` + right arrow icon
- **Fine print:** `No account needed. Free while in beta.`

### How It Works Section

```css
.how-it-works {
  background: var(--sand);
  padding: 64px 24px;
}

.how-it-works-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 40px;
  max-width: 480px;
  margin: 0 auto;
}

.how-step {
  display: flex;
  gap: 20px;
  align-items: flex-start;
}

.how-step-number {
  flex-shrink: 0;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: var(--aegean);
  color: white;
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 600;
  display: flex;
  align-items: center;
  justify-content: center;
}

.how-step-title {
  font-family: var(--font-body);
  font-weight: 600;
  font-size: 1rem;
  color: var(--ink);
  margin-bottom: 4px;
}

.how-step-body {
  font-size: 0.9375rem;
  color: var(--ink-secondary);
  line-height: 1.5;
}
```

### Interactions

- Clicking "Start planning" smooth-scrolls to the Brief input on the same page (or navigates to `/new` if we want a separate URL)
- The hero image uses `loading="eager"` and is optimized as a 1200px WebP at ~60KB
- Page loads in under 1.5 seconds on 3G -- critical because the organiser may be on mobile in a cafe

---

## 4. Screen 2: The Brief (Input)

### URL: `tripforge.app/new` (or same page, scrolled)

### Emotional Target: Confidence + "I can just talk naturally"

### The Core Decision: Chat vs. Form

A form says "fill in our fields." A text area says "tell us in your words." The organiser has already done the thinking. They know "4 of us from London, Milos + Koufonisia, mid-August, 7 nights." Forcing that into dropdowns is insulting to their research.

We use a **single large textarea** styled to feel like writing a message, with an example prompt for guidance.

### Layout

```
┌────────────────────────────────────────────┐
│                                            │
│  <- Back                    TRIPFORGE      │
│                                            │
│  Tell us about your trip                   │
│                                            │
│  Write it however you like — the way       │
│  you'd describe it to a friend.            │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │                                      │  │
│  │  e.g. "3 couples. 4 of us are       │  │
│  │  flying from London, 2 already in   │  │
│  │  Athens. We want to do Milos (5     │  │
│  │  nights) then Koufonisia (2 nights) │  │
│  │  around mid-August 2026. Mid-range  │  │
│  │  budget. Beach-focused, good food,  │  │
│  │  mix of activity and relaxation."   │  │
│  │                                      │  │
│  │                                      │  │
│  │                                      │  │
│  │                                      │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  HELPFUL TO INCLUDE                        │
│                                            │
│  · How many people and where from          │
│  · Which islands you want                  │
│  · Dates (even rough like "mid-August")    │
│  · How many nights per island              │
│  · Vibe / budget / preferences             │
│                                            │
│           [ Build my trip  ->  ]           │
│                                            │
│  Examples:                                 │
│  "London to Santorini + Milos, 5 people,  │
│   Sep 10-18, apartments with a pool"       │
│                                            │
│  "Couple from Berlin, island hopping       │
│   Paros → Naxos → Koufonisia, late July,  │
│   10 days, mid-budget"                     │
│                                            │
└────────────────────────────────────────────┘
```

### Specific CSS

```css
.brief-screen {
  background: var(--white);
  min-height: 100vh;
  padding: 0 0 120px;
}

.brief-header {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 16px 20px;
  border-bottom: 1px solid var(--stone);
}

.brief-back {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--ink-secondary);
  text-decoration: none;
  border: none;
  background: none;
  cursor: pointer;
}

.brief-content {
  max-width: 560px;
  margin: 0 auto;
  padding: 40px 20px;
}

.brief-title {
  font-family: var(--font-display);
  font-size: 1.75rem;
  color: var(--ink);
  margin-bottom: 8px;
}

.brief-subtitle {
  font-size: 0.9375rem;
  color: var(--ink-secondary);
  margin-bottom: 32px;
  line-height: 1.5;
}

.brief-textarea {
  width: 100%;
  min-height: 200px;
  padding: 20px;
  border: 1.5px solid var(--stone);
  border-radius: var(--radius-md);
  font-family: var(--font-body);
  font-size: 1rem;
  line-height: 1.6;
  color: var(--ink);
  background: var(--white);
  resize: vertical;
  transition: border-color 0.2s ease, box-shadow 0.2s ease;
}

.brief-textarea:focus {
  outline: none;
  border-color: var(--aegean);
  box-shadow: 0 0 0 3px var(--aegean-light);
}

.brief-textarea::placeholder {
  color: var(--ink-tertiary);
  font-style: italic;
}

.brief-hints {
  margin-top: 24px;
  padding: 0;
}

.brief-hints-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: var(--ink-tertiary);
  margin-bottom: 12px;
}

.brief-hints ul {
  list-style: none;
  padding: 0;
  margin: 0;
}

.brief-hints li {
  font-size: 0.875rem;
  color: var(--ink-secondary);
  padding: 4px 0;
  padding-left: 16px;
  position: relative;
}

.brief-hints li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 11px;
  width: 5px;
  height: 5px;
  border-radius: 50%;
  background: var(--stone);
}

.brief-submit-area {
  margin-top: 32px;
  text-align: center;
}

.brief-examples {
  margin-top: 40px;
  padding-top: 32px;
  border-top: 1px solid var(--stone);
}

.brief-examples-label {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1px;
  color: var(--ink-tertiary);
  margin-bottom: 12px;
}

.brief-example {
  padding: 12px 16px;
  background: var(--sand);
  border-radius: var(--radius-sm);
  font-size: 0.875rem;
  color: var(--ink-secondary);
  line-height: 1.5;
  margin-bottom: 8px;
  cursor: pointer;
  border: 1px solid transparent;
  transition: border-color 0.15s ease;
}

.brief-example:hover {
  border-color: var(--aegean);
}
```

### Interactions

1. **Placeholder text** fills the textarea with the example brief in italic gray. As soon as the user starts typing, it disappears.
2. **Example briefs** below the textarea are clickable -- tapping one fills the textarea with that text (makes it easy to try the product without thinking).
3. **"Build my trip"** button is disabled (grayed out, `opacity: 0.4`) until the textarea has at least 30 characters.
4. **Character counter** appears subtly at bottom-right of textarea once the user starts typing: `142 characters` in `var(--ink-tertiary)`. No maximum, but we want to signal that more detail is fine.
5. **On submit**, the button changes to a loading state: text becomes "Understanding your trip..." with a subtle pulse animation, then the page transitions to Screen 3.

### Microcopy

- **Title:** `Tell us about your trip`
- **Subtitle:** `Write it however you like -- the way you'd describe it to a friend.`
- **Placeholder:** `e.g. "3 couples. 4 of us are flying from London, 2 already in Athens. We want to do Milos (5 nights) then Koufonisia (2 nights) around mid-August 2026. Mid-range budget. Beach-focused, good food, mix of activity and relaxation."`
- **Hints label:** `HELPFUL TO INCLUDE`
- **Hints:**
  - `How many people and where they're flying from`
  - `Which islands (and in what order, if you have a preference)`
  - `Dates or at least time of year`
  - `How many nights per island`
  - `Budget range, vibe, any preferences`
- **Submit button:** `Build my trip` + right arrow SVG
- **Examples label:** `EXAMPLES YOU CAN TRY`

### What Happens Under the Hood

When the user clicks "Build my trip," we POST their text to the backend which calls `extract_trip_spec()` using Claude Haiku. This typically returns in 1-3 seconds. During this time, we show the button's loading state. Once the TripSpecification is returned, we transition to Screen 3.

---

## 5. Screen 3: Confirmation / Edit

### URL: `tripforge.app/new?step=confirm` (or same page, animated transition)

### Emotional Target: Control + "It understood me, and I can fine-tune anything"

### The Core Design Idea

We take the AI-extracted TripSpecification and present it as a **visual itinerary preview** -- not a form, not a JSON dump, not a table. The user sees their trip laid out as a visual route with editable cards. This is the "did we get it right?" moment.

This screen must accomplish two things:
1. Make the user feel seen ("yes, that's exactly what I described")
2. Give them confidence that corrections are easy ("oh, I can just tap to change the dates")

### Layout

```
┌────────────────────────────────────────────┐
│  <- Edit brief              TRIPFORGE      │
│                                            │
│  Here's what we understood                 │
│  Check the details, then we'll find        │
│  flights, ferries, and places to stay.     │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  TITLE                               │  │
│  │  Greece 2026                    [edit]│  │
│  ├──────────────────────────────────────┤  │
│  │  TRAVELERS                           │  │
│  │  6 people · 3 couples                │  │
│  │                                      │  │
│  │  London crew (4)         ✈ LON       │  │
│  │  Athens crew (2)         ✈ ATH       │  │
│  │                                [edit]│  │
│  ├──────────────────────────────────────┤  │
│  │  DATES                               │  │
│  │  Aug 14 – 21, 2026                   │  │
│  │  7 nights                       [edit]│  │
│  ├──────────────────────────────────────┤  │
│  │  ROUTE                               │  │
│  │                                      │  │
│  │  London ─── ✈ ───> Athens            │  │
│  │       │                              │  │
│  │       └──── ✈/⛴ ──> Milos           │  │
│  │                       5 nights       │  │
│  │                       🚗 rent a car  │  │
│  │                       │              │  │
│  │                       └── ⛴ ──>     │  │
│  │                        Koufonisia    │  │
│  │                        2 nights      │  │
│  │                        🚶 walkable   │  │
│  │                       │              │  │
│  │                       └── ⛴ ──>     │  │
│  │                        Athens        │  │
│  │       └──── ✈ ────> London           │  │
│  │                                [edit]│  │
│  ├──────────────────────────────────────┤  │
│  │  PREFERENCES                         │  │
│  │  Beach-focused · Good food ·         │  │
│  │  Mix of activity and relaxation      │  │
│  │  Mid-range budget               [edit]│  │
│  └──────────────────────────────────────┘  │
│                                            │
│       [ Looks good — find options -> ]     │
│                                            │
│  or  [go back and edit the brief]          │
│                                            │
└────────────────────────────────────────────┘
```

### CSS for Confirmation Cards

```css
.confirm-screen {
  background: var(--sand);
  min-height: 100vh;
  padding-bottom: 120px;
}

.confirm-content {
  max-width: 560px;
  margin: 0 auto;
  padding: 40px 20px;
}

.confirm-title {
  font-family: var(--font-display);
  font-size: 1.75rem;
  color: var(--ink);
  margin-bottom: 8px;
}

.confirm-subtitle {
  font-size: 0.9375rem;
  color: var(--ink-secondary);
  line-height: 1.5;
  margin-bottom: 32px;
}

.confirm-card {
  background: var(--white);
  border-radius: var(--radius-lg);
  overflow: hidden;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--stone);
}

.confirm-section {
  padding: 20px 24px;
  border-bottom: 1px solid var(--stone);
  position: relative;
}

.confirm-section:last-child {
  border-bottom: none;
}

.confirm-section-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.2px;
  color: var(--ink-tertiary);
  margin-bottom: 8px;
}

.confirm-section-value {
  font-size: 1rem;
  font-weight: 500;
  color: var(--ink);
  line-height: 1.5;
}

.confirm-section-detail {
  font-size: 0.875rem;
  color: var(--ink-secondary);
  margin-top: 4px;
}

.confirm-edit-btn {
  position: absolute;
  top: 16px;
  right: 16px;
  padding: 6px 12px;
  border-radius: var(--radius-full);
  border: 1px solid var(--stone);
  background: var(--white);
  font-size: 0.75rem;
  font-weight: 500;
  color: var(--ink-secondary);
  cursor: pointer;
  transition: border-color 0.15s ease, color 0.15s ease;
}

.confirm-edit-btn:hover {
  border-color: var(--aegean);
  color: var(--aegean);
}

/* Route visualization */
.confirm-route {
  padding: 4px 0;
}

.route-leg {
  display: flex;
  align-items: flex-start;
  gap: 16px;
  padding: 8px 0;
}

.route-line {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 24px;
  flex-shrink: 0;
}

.route-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--aegean);
  flex-shrink: 0;
}

.route-dot.island {
  width: 14px;
  height: 14px;
  background: var(--sunset);
}

.route-connector {
  width: 2px;
  height: 32px;
  background: var(--stone);
}

.route-connector.dashed {
  background: repeating-linear-gradient(
    to bottom,
    var(--stone) 0px,
    var(--stone) 4px,
    transparent 4px,
    transparent 8px
  );
}

.route-leg-info {
  flex: 1;
  padding-top: 0;
}

.route-place-name {
  font-weight: 600;
  font-size: 0.9375rem;
  color: var(--ink);
}

.route-place-meta {
  font-size: 0.8125rem;
  color: var(--ink-secondary);
  margin-top: 2px;
}

.route-transport-label {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  color: var(--ink-tertiary);
  margin-top: 4px;
}
```

### Edit Interaction Pattern

When the user taps an "edit" button on any section, it opens inline:

**For Title:** The text becomes an inline input field, with the current value pre-filled. Auto-focus. Press Enter or tap outside to confirm.

**For Travelers:** A compact inline editor appears:

```
┌──────────────────────────────────────┐
│  TRAVELERS                           │
│                                      │
│  Group 1:                            │
│  City [London     ]  People [4]      │
│  Label [London crew]                 │
│                                      │
│  Group 2:                            │
│  City [Athens     ]  People [2]      │
│  Label [Athens crew]                 │
│                                      │
│  + Add another origin                │
│                                      │
│  Description: [3 couples]            │
│                                      │
│              [Save]   [Cancel]       │
└──────────────────────────────────────┘
```

**For Dates:** A date range picker appears (simple HTML date inputs for MVP). Start date and end date.

**For Route:** Each island becomes editable with nights count. User can reorder islands (drag or up/down arrows on mobile) or add/remove stops.

**For Preferences:** Tags become editable. User can delete tags (x button) or add new ones by typing.

All edits are instant and local -- no server round-trip needed. The user is editing the TripSpecification object in JS memory.

### Microcopy

- **Title:** `Here's what we understood`
- **Subtitle:** `Check the details, then we'll find flights, ferries, and places to stay.`
- **CTA:** `Looks good -- find options` + right arrow
- **Secondary action:** `Go back and edit the brief` (link-styled, not a button)
- **Edit button labels:** `Edit` (just the word, clean)
- **Section labels:** `TITLE`, `TRAVELERS`, `DATES`, `ROUTE`, `PREFERENCES`
- **Route details:** `5 nights` / `rent a car` / `walkable` / `no car needed`
- **Validation error (if any field is bad):** `We need at least one island to plan a trip.` (warm, not angry)

---

## 6. Screen 4: Research / Loading

### URL: `tripforge.app/plan/{id}?loading=1`

### Emotional Target: Excitement + "It's actually doing the work"

### The Core Design Idea

This is a 30-60 second wait. In most apps, this kills conversion. We turn it into the most delightful moment in the flow.

Instead of a spinner, we show a **live progress sequence** that tells the user what is happening, paired with a beautiful full-screen island image. The user watches their trip being assembled in real-time. Each research step is announced, creating a sense of "it's working, it's working."

### Layout

```
┌────────────────────────────────────────────┐
│                                            │
│  [Full-bleed background: soft-focus image  │
│   of Milos/first island, warm sunset       │
│   tones. 60% opacity overlay]              │
│                                            │
│                                            │
│         ·  ·  ·  ·  ·                     │
│     (5 dots, filling in as steps complete) │
│                                            │
│     Planning your trip to                  │
│     Milos & Koufonisia                     │
│                                            │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │                                      │  │
│  │  ✓  Checking London → Athens flights │  │
│  │  ✓  Checking Athens → Milos flights  │  │
│  │  ◎  Searching Milos ferries...       │  │
│  │  ○  Searching accommodation          │  │
│  │  ○  Building your itinerary          │  │
│  │                                      │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  While you wait:                           │
│  Milos is a volcanic island with 70+       │
│  beaches. Don't miss Sarakiniko — it       │
│  looks like the moon landed in the         │
│  Aegean.                                   │
│                                            │
└────────────────────────────────────────────┘
```

### CSS

```css
.loading-screen {
  position: fixed;
  inset: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  text-align: center;
  padding: 40px 24px;
  z-index: 200;
}

.loading-bg {
  position: absolute;
  inset: 0;
  background: url('/images/island-loading.jpg') center/cover no-repeat;
  filter: brightness(0.35) saturate(0.9);
  z-index: 0;
}

.loading-screen > * {
  position: relative;
  z-index: 1;
}

/* Progress dots */
.loading-dots {
  display: flex;
  gap: 8px;
  margin-bottom: 32px;
}

.loading-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.25);
  transition: background 0.5s ease, transform 0.3s ease;
}

.loading-dot.active {
  background: var(--white);
  transform: scale(1.25);
}

.loading-dot.complete {
  background: var(--sea);
}

.loading-headline {
  font-family: var(--font-body);
  font-size: 0.875rem;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.6);
  margin-bottom: 8px;
}

.loading-destination {
  font-family: var(--font-display);
  font-size: 1.75rem;
  color: var(--white);
  margin-bottom: 40px;
}

/* Step list */
.loading-steps {
  background: rgba(0, 0, 0, 0.4);
  backdrop-filter: blur(20px);
  -webkit-backdrop-filter: blur(20px);
  border-radius: var(--radius-md);
  padding: 24px 28px;
  max-width: 380px;
  width: 100%;
  text-align: left;
}

.loading-step {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 8px 0;
  font-size: 0.875rem;
  color: rgba(255, 255, 255, 0.4);
  transition: color 0.3s ease;
}

.loading-step.active {
  color: rgba(255, 255, 255, 0.9);
}

.loading-step.complete {
  color: rgba(255, 255, 255, 0.6);
}

.loading-step-icon {
  width: 20px;
  height: 20px;
  flex-shrink: 0;
  display: flex;
  align-items: center;
  justify-content: center;
}

/* Checkmark for complete steps */
.loading-step.complete .loading-step-icon::after {
  content: '';
  width: 8px;
  height: 14px;
  border: 2px solid var(--sea);
  border-top: none;
  border-left: none;
  transform: rotate(45deg) translateY(-2px);
}

/* Pulsing dot for active step */
.loading-step.active .loading-step-icon::after {
  content: '';
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: var(--white);
  animation: pulse 1.5s ease-in-out infinite;
}

/* Empty circle for pending steps */
.loading-step.pending .loading-step-icon::after {
  content: '';
  width: 10px;
  height: 10px;
  border-radius: 50%;
  border: 1.5px solid rgba(255, 255, 255, 0.25);
}

@keyframes pulse {
  0%, 100% { opacity: 1; transform: scale(1); }
  50% { opacity: 0.5; transform: scale(0.8); }
}

/* Fun fact / while you wait */
.loading-fact {
  max-width: 340px;
  margin-top: 40px;
  font-size: 0.8125rem;
  line-height: 1.6;
  color: rgba(255, 255, 255, 0.5);
}

.loading-fact strong {
  color: rgba(255, 255, 255, 0.7);
}
```

### Progress Steps (mapped to actual research pipeline)

The steps shown correlate to the actual `run_parallel_research` tasks. We group them into 5 user-facing steps:

| Step | Label | Maps to backend |
|------|-------|-----------------|
| 1 | `Checking flights to Athens` | `flights_{origin}_to_Athens` for each origin |
| 2 | `Checking flights to {first_island}` | `flights_Athens_to_{island}` + `ferries_hub_to_{island}` |
| 3 | `Searching island ferries` | Inter-island ferries + return ferries |
| 4 | `Finding places to stay` | All accommodation searches |
| 5 | `Building your itinerary` | `_synthesize_itinerary` or `_build_itinerary` |

Steps 1-4 can run in parallel, so they may complete out of order. Each step transitions from `pending` to `active` to `complete` as the corresponding API calls resolve.

### Island Fun Facts (rotating)

While waiting, show one fact about the islands in the trip, rotating every 8 seconds with a fade transition:

For Milos:
- `Milos is a volcanic island with 70+ beaches. Don't miss Sarakiniko -- it looks like the moon landed in the Aegean.`
- `The Venus de Milo was found on Milos in 1820 by a farmer. It's now in the Louvre. The locals want it back.`
- `Kleftiko is a sea cave complex you can only reach by boat. Book the tour from Adamas port.`

For Koufonisia:
- `Koufonisia has about 400 permanent residents and roughly 20 places to stay. If you haven't booked yet, now is the time.`
- `Pori beach on Koufonisia has sand so fine it squeaks when you walk on it. No loungers, no umbrellas, no buildings.`

### Transition to Results

When the itinerary is built, the loading screen does the following 1.5-second animation:
1. All 5 dots turn green (0.3s)
2. Steps list fades out (0.3s)
3. A checkmark appears with the text "Your trip is ready" (0.5s)
4. The screen fades up to reveal the itinerary page beneath (0.4s)

---

## 7. Screen 5: The Itinerary (Results)

### URL: `tripforge.app/plan/{id}`

### Emotional Target: Pride + "I made this, and it looks professional"

This is the money screen. This is what gets shared. This is the organiser's resume of caring. It must look stunning.

### Major Changes from Current Template

The existing `itinerary.html.j2` is a dark-mode developer aesthetic. We shift to the warm light palette from our design system, add photography, and restructure for scannability.

### Layout (section by section)

#### A. Hero / Header

```
┌────────────────────────────────────────────┐
│                                            │
│  [Background image: aerial view of first   │
│   island. Warm tones. Image fills top      │
│   300px with gradient overlay fading       │
│   to sand/white at the bottom]             │
│                                            │
│        Greece 2026                         │
│        Milos & Koufonisia                  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  Aug 14 – 21, 2026 · 3 couples      │  │
│  └──────────────────────────────────────┘  │
│                                            │
│   London → Athens → Milos → Koufonisia     │
│            → Athens → London               │
│                                            │
│                                            │
│  ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ ─ │
│  background fades to sand here             │
└────────────────────────────────────────────┘
```

```css
.itin-hero {
  position: relative;
  padding: 80px 24px 48px;
  text-align: center;
  overflow: hidden;
  min-height: 340px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: flex-end;
}

.itin-hero::before {
  content: '';
  position: absolute;
  inset: 0;
  background: url('/images/hero-milos.jpg') center/cover no-repeat;
  filter: saturate(1.1);
  z-index: 0;
}

.itin-hero::after {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(
    180deg,
    rgba(250, 247, 242, 0) 0%,
    rgba(250, 247, 242, 0.3) 40%,
    rgba(250, 247, 242, 0.85) 70%,
    rgba(250, 247, 242, 1) 100%
  );
  z-index: 1;
}

.itin-hero > * {
  position: relative;
  z-index: 2;
}

.itin-hero-title {
  font-family: var(--font-display);
  font-size: clamp(2rem, 5vw, 2.75rem);
  color: var(--ink);
  margin-bottom: 4px;
}

.itin-hero-subtitle {
  font-family: var(--font-display);
  font-size: 1.25rem;
  color: var(--ink-secondary);
  margin-bottom: 16px;
}

.itin-hero-meta {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 8px 20px;
  background: var(--white);
  border-radius: var(--radius-full);
  font-size: 0.875rem;
  font-weight: 500;
  color: var(--ink-secondary);
  box-shadow: var(--shadow-sm);
}

.itin-route-pills {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0;
  margin-top: 20px;
  flex-wrap: wrap;
  padding: 0 16px;
}

.itin-route-stop {
  font-size: 0.8125rem;
  font-weight: 600;
  color: var(--ink);
  background: var(--white);
  padding: 5px 12px;
  border-radius: var(--radius-full);
  white-space: nowrap;
  box-shadow: var(--shadow-sm);
}

.itin-route-stop.island {
  background: var(--sunset-light);
  color: var(--sunset);
}

.itin-route-arrow {
  color: var(--ink-tertiary);
  font-size: 0.75rem;
  padding: 0 6px;
}
```

#### B. Itinerary Day Cards

Each day gets a card. Island-stay days get a warm highlight treatment. Travel days are more utilitarian.

```css
.itin-container {
  max-width: 680px;
  margin: 0 auto;
  padding: 0 20px 120px;
  background: var(--sand);
}

.itin-section {
  margin: 40px 0;
}

.itin-section-label {
  font-size: 0.6875rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 1.5px;
  color: var(--ink-tertiary);
  margin-bottom: 16px;
  padding-left: 4px;
}

.itin-day-card {
  background: var(--white);
  border-radius: var(--radius-md);
  padding: 24px;
  margin-bottom: 12px;
  box-shadow: var(--shadow-sm);
  border: 1px solid var(--stone);
  border-left: 4px solid var(--aegean);
}

.itin-day-card.highlight {
  border-left-color: var(--sunset);
  background: linear-gradient(135deg, var(--white) 0%, var(--sunset-light) 100%);
}

.itin-day-date {
  font-size: 0.75rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--ink-tertiary);
  margin-bottom: 4px;
}

.itin-day-title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  color: var(--ink);
  margin-bottom: 4px;
}

.itin-day-subtitle {
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--aegean);
  margin-bottom: 16px;
}

.itin-day-card.highlight .itin-day-subtitle {
  color: var(--sunset);
}

/* Transport legs inside day cards */
.itin-transport {
  display: flex;
  align-items: flex-start;
  gap: 12px;
  padding: 10px 0;
  border-bottom: 1px solid var(--stone);
}

.itin-transport:last-of-type {
  border-bottom: none;
}

.itin-transport-badge {
  flex-shrink: 0;
  margin-top: 2px;
}

.itin-transport-info {
  flex: 1;
}

.itin-transport-route {
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--ink);
}

.itin-transport-detail {
  font-size: 0.8125rem;
  color: var(--ink-secondary);
  margin-top: 2px;
}

.itin-transport-price {
  font-size: 0.875rem;
  font-weight: 600;
  color: var(--ink);
  flex-shrink: 0;
  text-align: right;
}

/* Highlights list (activities) */
.itin-highlights {
  list-style: none;
  padding: 0;
  margin: 12px 0 0;
}

.itin-highlights li {
  padding: 5px 0 5px 20px;
  position: relative;
  font-size: 0.875rem;
  color: var(--ink-secondary);
  line-height: 1.5;
}

.itin-highlights li::before {
  content: '';
  position: absolute;
  left: 0;
  top: 12px;
  width: 6px;
  height: 6px;
  border-radius: 50%;
  background: var(--sunset);
}

/* Warning/note callout */
.itin-note {
  display: flex;
  gap: 10px;
  align-items: flex-start;
  background: var(--sunset-light);
  border-radius: var(--radius-sm);
  padding: 12px 16px;
  margin-top: 12px;
  font-size: 0.8125rem;
  color: var(--ink-secondary);
  line-height: 1.5;
}

.itin-note-icon {
  flex-shrink: 0;
  width: 18px;
  height: 18px;
  color: var(--sunset);
  margin-top: 1px;
}

.itin-note strong {
  color: var(--ink);
}
```

#### C. Accommodation Sections

Each island gets its own accommodation section. Cards show more visual information and are clearly tappable for booking.

```css
.itin-accommodation-card {
  display: flex;
  gap: 16px;
  align-items: center;
  padding: 16px;
  background: var(--white);
  border: 1px solid var(--stone);
  border-radius: var(--radius-md);
  margin-bottom: 8px;
  text-decoration: none;
  color: inherit;
  transition: box-shadow 0.2s ease, border-color 0.2s ease;
  cursor: pointer;
}

.itin-accommodation-card:hover {
  box-shadow: var(--shadow-md);
  border-color: var(--aegean);
}

.itin-acc-info {
  flex: 1;
  min-width: 0;
}

.itin-acc-name {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 2px;
}

.itin-acc-location {
  font-size: 0.8125rem;
  color: var(--ink-secondary);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.itin-acc-rating {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  font-size: 0.75rem;
  font-weight: 600;
  color: var(--sunset);
  margin-top: 4px;
}

.itin-acc-price {
  flex-shrink: 0;
  text-align: right;
}

.itin-acc-price-amount {
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--ink);
}

.itin-acc-price-meta {
  font-size: 0.6875rem;
  color: var(--ink-tertiary);
  margin-top: 2px;
}

.itin-acc-source {
  display: inline-block;
  font-size: 0.625rem;
  font-weight: 600;
  text-transform: uppercase;
  letter-spacing: 0.5px;
  color: var(--aegean);
  background: var(--aegean-light);
  padding: 2px 6px;
  border-radius: 4px;
  margin-top: 4px;
}

/* "View more options" toggle */
.itin-acc-more {
  text-align: center;
  padding: 12px;
}

.itin-acc-more-btn {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 0.8125rem;
  font-weight: 500;
  color: var(--aegean);
  background: none;
  border: none;
  cursor: pointer;
  padding: 8px 16px;
  border-radius: var(--radius-full);
  transition: background 0.15s ease;
}

.itin-acc-more-btn:hover {
  background: var(--aegean-light);
}
```

#### D. Cost Breakdown

A clean, scannable table. The multi-origin tabs remain but are restyled.

```css
.itin-cost-tabs {
  display: flex;
  gap: 6px;
  margin-bottom: 20px;
}

.itin-cost-tab {
  padding: 8px 18px;
  border-radius: var(--radius-full);
  font-size: 0.8125rem;
  font-weight: 500;
  cursor: pointer;
  background: transparent;
  color: var(--ink-secondary);
  border: 1.5px solid var(--stone);
  transition: all 0.15s ease;
}

.itin-cost-tab.active {
  background: var(--ink);
  color: var(--white);
  border-color: var(--ink);
}

.itin-cost-table {
  width: 100%;
  border-collapse: collapse;
}

.itin-cost-table tr {
  border-bottom: 1px solid var(--stone);
}

.itin-cost-table td {
  padding: 12px 0;
  font-size: 0.875rem;
  vertical-align: top;
}

.itin-cost-table td:first-child {
  color: var(--ink-secondary);
  padding-right: 16px;
}

.itin-cost-table td:last-child {
  text-align: right;
  font-weight: 600;
  color: var(--ink);
  white-space: nowrap;
}

.itin-cost-table tr.total {
  border-bottom: none;
}

.itin-cost-table tr.total td {
  padding-top: 16px;
  font-size: 1rem;
  font-weight: 700;
  color: var(--aegean);
  border-top: 2px solid var(--aegean);
}
```

#### E. Booking Actions (urgency-ordered)

```css
.itin-action {
  display: flex;
  gap: 16px;
  align-items: flex-start;
  padding: 16px 20px;
  background: var(--white);
  border: 1px solid var(--stone);
  border-radius: var(--radius-md);
  margin-bottom: 8px;
}

.itin-action-number {
  flex-shrink: 0;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: var(--aegean);
  color: var(--white);
  font-size: 0.75rem;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
}

.itin-action-content {
  flex: 1;
}

.itin-action-title {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--ink);
  margin-bottom: 2px;
}

.itin-action-reason {
  font-size: 0.8125rem;
  color: var(--ink-secondary);
  line-height: 1.4;
  margin-bottom: 8px;
}

.itin-action-links {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.itin-action-link {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 5px 12px;
  border-radius: var(--radius-full);
  background: var(--aegean-light);
  color: var(--aegean);
  font-size: 0.75rem;
  font-weight: 600;
  text-decoration: none;
  transition: background 0.15s ease;
}

.itin-action-link:hover {
  background: #D0E8F0;
}
```

#### F. Booking Checklist

The checklist stays -- it is a great interactive feature. Restyle it for the warm palette.

```css
.itin-checklist {
  list-style: none;
  padding: 0;
  margin: 0;
}

.itin-checklist li {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 14px 16px;
  background: var(--white);
  border: 1px solid var(--stone);
  border-radius: var(--radius-sm);
  margin-bottom: 6px;
  font-size: 0.875rem;
  color: var(--ink);
  transition: opacity 0.2s ease;
}

.itin-checklist li.checked {
  opacity: 0.45;
}

.itin-checklist li.checked span {
  text-decoration: line-through;
}

.itin-checklist input[type="checkbox"] {
  width: 18px;
  height: 18px;
  accent-color: var(--sea);
  flex-shrink: 0;
  cursor: pointer;
}
```

#### G. Sticky Bottom Bar

The bottom bar is the most important interactive element. It contains the per-person cost summary and the share button. The share button is the primary CTA for this entire page.

```css
.itin-sticky-bar {
  position: fixed;
  bottom: 0;
  left: 0;
  right: 0;
  background: var(--white);
  border-top: 1px solid var(--stone);
  padding: 12px 20px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  z-index: 100;
  box-shadow: 0 -2px 10px rgba(0,0,0,0.06);
}

.itin-sticky-cost {
  font-size: 0.8125rem;
  color: var(--ink-secondary);
  line-height: 1.3;
}

.itin-sticky-cost strong {
  display: block;
  font-size: 1.125rem;
  font-weight: 700;
  color: var(--ink);
}

.itin-share-btn {
  display: inline-flex;
  align-items: center;
  gap: 8px;
  padding: 12px 24px;
  background: var(--ink);
  color: var(--white);
  border: none;
  border-radius: var(--radius-full);
  font-family: var(--font-body);
  font-size: 0.9375rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.15s ease, transform 0.1s ease;
}

.itin-share-btn:hover {
  background: #333;
}

.itin-share-btn:active {
  transform: scale(0.97);
}

/* WhatsApp green variant for the share button on mobile */
@media (max-width: 600px) {
  .itin-share-btn {
    background: #25D366;
    color: var(--white);
  }
  .itin-share-btn:hover {
    background: #1DA851;
  }
}
```

### Mobile-specific (this is a WhatsApp-shared link -- 90%+ traffic will be mobile)

```css
@media (max-width: 600px) {
  .itin-hero {
    min-height: 280px;
    padding: 60px 16px 32px;
  }

  .itin-hero-title {
    font-size: 1.75rem;
  }

  .itin-container {
    padding: 0 16px 100px;
  }

  .itin-day-card {
    padding: 20px 16px;
  }

  .itin-accommodation-card {
    flex-direction: column;
    align-items: flex-start;
  }

  .itin-acc-price {
    text-align: left;
    margin-top: 8px;
    display: flex;
    align-items: baseline;
    gap: 8px;
  }

  .itin-acc-price-meta {
    margin-top: 0;
  }

  .itin-route-stop {
    font-size: 0.75rem;
    padding: 4px 8px;
  }
}
```

---

## 8. Screen 6: Share Flow

### Triggered by: Tapping "Share Plan" in the sticky bottom bar

### Emotional Target: Recognition anticipation + "my group is going to love this"

### The Share Sheet

Instead of relying on the browser's native `navigator.share()` (inconsistent across devices), we show a custom share sheet with targeted options.

```
┌────────────────────────────────────────────┐
│                                            │
│  Share your trip plan                      │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  📱 Share to WhatsApp               │  │
│  │  Opens WhatsApp with a link and      │  │
│  │  preview message                     │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  📋 Copy link                       │  │
│  │  For any app or email               │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  ┌──────────────────────────────────────┐  │
│  │  📤 Share via...                    │  │
│  │  Open system share sheet            │  │
│  └──────────────────────────────────────┘  │
│                                            │
│  [Cancel]                                  │
│                                            │
└────────────────────────────────────────────┘
```

### CSS for Share Sheet

```css
.share-overlay {
  position: fixed;
  inset: 0;
  background: rgba(26, 26, 26, 0.4);
  z-index: 300;
  display: flex;
  align-items: flex-end;
  justify-content: center;
  animation: fadeIn 0.2s ease;
}

@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}

.share-sheet {
  background: var(--white);
  border-radius: var(--radius-lg) var(--radius-lg) 0 0;
  padding: 28px 24px 40px;
  width: 100%;
  max-width: 500px;
  animation: slideUp 0.25s ease;
}

@keyframes slideUp {
  from { transform: translateY(100%); }
  to { transform: translateY(0); }
}

.share-sheet-title {
  font-family: var(--font-display);
  font-size: 1.25rem;
  color: var(--ink);
  margin-bottom: 20px;
  text-align: center;
}

.share-option {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 16px;
  border-radius: var(--radius-md);
  border: 1px solid var(--stone);
  margin-bottom: 8px;
  cursor: pointer;
  background: var(--white);
  transition: background 0.15s ease, border-color 0.15s ease;
  text-decoration: none;
  color: inherit;
  width: 100%;
  text-align: left;
  font-family: var(--font-body);
}

.share-option:hover {
  background: var(--sand);
  border-color: var(--ink-secondary);
}

.share-option-whatsapp {
  border-color: #25D366;
}

.share-option-whatsapp:hover {
  background: #E8F8EE;
}

.share-option-icon {
  width: 40px;
  height: 40px;
  border-radius: var(--radius-sm);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.share-option-icon.whatsapp {
  background: #25D366;
  color: white;
}

.share-option-icon.copy {
  background: var(--sand);
  color: var(--ink-secondary);
}

.share-option-icon.system {
  background: var(--aegean-light);
  color: var(--aegean);
}

.share-option-text {
  flex: 1;
}

.share-option-label {
  font-size: 0.9375rem;
  font-weight: 600;
  color: var(--ink);
}

.share-option-desc {
  font-size: 0.8125rem;
  color: var(--ink-secondary);
  margin-top: 1px;
}

.share-cancel {
  display: block;
  width: 100%;
  padding: 14px;
  border: none;
  background: none;
  font-family: var(--font-body);
  font-size: 0.9375rem;
  font-weight: 500;
  color: var(--ink-secondary);
  cursor: pointer;
  text-align: center;
  margin-top: 8px;
  border-radius: var(--radius-md);
}

.share-cancel:hover {
  background: var(--sand);
}
```

### WhatsApp Share Details

When the user taps "Share to WhatsApp," we generate a WhatsApp deep link:

```
https://wa.me/?text=Greece%202026%20%E2%80%93%20Milos%20%26%20Koufonisia%0A%0AAug%2014%E2%80%9321%20%C2%B7%203%20couples%20%C2%B7%20~%E2%82%AC700%E2%80%931%2C500pp%0A%0AI%20put%20together%20the%20full%20plan%20%E2%80%93%20flights%2C%20ferries%2C%20places%20to%20stay%2C%20costs.%20Have%20a%20look%3A%0A%0Ahttps%3A%2F%2Ftripforge.app%2Fplan%2Fabc123
```

Which decodes to:

```
Greece 2026 -- Milos & Koufonisia

Aug 14-21 · 3 couples · ~EUR700-1,500pp

I put together the full plan -- flights, ferries, places to stay, costs. Have a look:

https://tripforge.app/plan/abc123
```

This message is pre-composed for the organiser. They can edit it before sending. It contains:
1. The trip name (so the recipient immediately knows what this is)
2. Key facts (dates, group, ballpark cost)
3. A summary that positions the organiser as the hero ("I put together the full plan")
4. The link

### Copy Link Behavior

On tap, the link is copied to clipboard and the button text changes:

```
📋 Copy link              →    ✓ Link copied!
For any app or email            (resets after 2 seconds)
```

### OG Meta Tags (for WhatsApp preview)

When the link is shared in WhatsApp, it should show a rich preview. This requires proper OG tags on the itinerary page:

```html
<meta property="og:title" content="Greece 2026 -- Milos & Koufonisia">
<meta property="og:description" content="Aug 14-21, 2026 · 3 couples · Flights, ferries, accommodation & costs · ~EUR700-1,500 per person">
<meta property="og:image" content="https://tripforge.app/og/plan/abc123.png">
<meta property="og:image:width" content="1200">
<meta property="og:image:height" content="630">
<meta property="og:url" content="https://tripforge.app/plan/abc123">
<meta property="og:type" content="website">
```

The OG image should be a dynamically generated image (using something like Satori/Vercel OG or a simple canvas render on the server) that shows:
- The trip title in the serif font
- The island names
- The dates
- A stylized route map
- The TripForge logo
- All on a warm background with a subtle map illustration

This image is critical. When the organiser drops the link in WhatsApp, the preview image IS the first impression for every recipient. It must look beautiful.

---

## 9. Screen 7: Recipient / Post-Share View

### URL: Same as Screen 5 -- `tripforge.app/plan/{id}`

### Emotional Target: Trust + "This is legit, I can actually use this"

The recipient (a friend in the group chat) sees the exact same itinerary page as the organiser. There is no login gate, no "sign up to view," no degraded experience. The full plan is accessible to anyone with the link.

### Differences from Organiser View

The recipient's experience has subtle differences:

1. **No editing capability.** The "Edit" buttons from Screen 3 are not present. This is a read-only view.

2. **Attribution banner** at the top, below the hero:

```
┌────────────────────────────────────────────┐
│  Planned by Sarah · powered by TripForge   │
│  Prices are estimates. Tap links to check  │
│  live availability and book.               │
└────────────────────────────────────────────┘
```

```css
.itin-attribution {
  text-align: center;
  padding: 16px 20px;
  background: var(--white);
  border-bottom: 1px solid var(--stone);
  font-size: 0.8125rem;
  color: var(--ink-secondary);
  line-height: 1.5;
}

.itin-attribution strong {
  color: var(--ink);
}
```

3. **The sticky bar changes.** Instead of "Share Plan," the CTA becomes "Plan your own trip":

```css
.itin-sticky-bar-recipient .itin-share-btn {
  background: var(--aegean);
}
```

- Left side: Still shows per-person cost estimate
- Right side: Button says `Plan your own trip` (links back to `tripforge.app/`)

4. **Booking checklist** still works with localStorage, so each recipient can independently track what they have booked. This is powerful -- each person in the group can check off their own bookings.

5. **"I'm in" reaction** (optional, future feature). A floating button at the bottom: "I'm in! (4 of 6 confirmed)". Each person can tap it, and the organiser sees who has confirmed. This is aspirational but deeply satisfying for the organiser. For MVP, skip this -- it requires user identity.

### Mobile-First Emphasis

Since 90%+ of recipients will open this in WhatsApp's in-app browser or their phone's default browser, the itinerary page must be tested extensively on:
- iOS Safari (via WhatsApp link)
- Android Chrome (via WhatsApp link)
- Samsung Internet

Key mobile behaviors:
- All phone numbers and addresses should be tappable (tel: links, Google Maps links)
- Booking links should open in the system browser, not WhatsApp's in-app browser (use `target="_blank"`)
- The sticky bar must not conflict with iOS safe area / home indicator
- Scroll performance must be smooth (no janky scroll handlers)

```css
/* iOS safe area support */
.itin-sticky-bar {
  padding-bottom: calc(12px + env(safe-area-inset-bottom, 0px));
}

/* Ensure the page content doesn't get hidden behind sticky bar */
.itin-container {
  padding-bottom: calc(100px + env(safe-area-inset-bottom, 0px));
}
```

---

## 10. Interaction Map & State Transitions

### Full Flow Diagram

```
   [Landing Page]
        |
        | Click "Start planning"
        v
   [Brief Input]
        |
        | Click "Build my trip"
        | (POST brief text to /api/extract)
        | Loading state: "Understanding your trip..."
        | Duration: 1-3 seconds
        v
   [Confirmation]
        |
        |--- Edit any section (inline editing)
        |    └── Updates TripSpecification in JS state
        |
        |--- "Go back and edit the brief"
        |    └── Returns to Brief Input with text preserved
        |
        | Click "Looks good -- find options"
        | (POST TripSpecification to /api/plan)
        v
   [Loading Screen]
        |
        | Research pipeline runs (30-60 seconds)
        | SSE or polling for step progress
        | 5 steps: flights, island flights, ferries, accommodation, synthesis
        v
   [Itinerary Page]
        |
        |--- Scroll, read, check boxes (localStorage)
        |--- Click accommodation links (opens booking sites)
        |--- Click booking action links
        |
        | Click "Share Plan" (sticky bar)
        v
   [Share Sheet]
        |
        |--- "WhatsApp" → opens wa.me deep link
        |--- "Copy link" → clipboard
        |--- "Share via..." → navigator.share()
        |--- "Cancel" → closes sheet
        |
        v
   [Recipient opens link]
        |
        v
   [Itinerary Page (recipient view)]
        |
        |--- Same page, read-only
        |--- Checklist works per-device
        |--- "Plan your own trip" CTA → Landing Page
```

### State Management

For the single-page flow (Landing through Itinerary), state can be managed with simple JavaScript:

```javascript
const state = {
  step: 'landing',      // landing | brief | confirm | loading | itinerary
  briefText: '',         // raw user input
  tripSpec: null,        // TripSpecification (from extraction)
  itinerary: null,       // Itinerary (from research pipeline)
  loadingStep: 0,        // 0-4, which research step is active
  planId: null,          // server-generated plan ID for shareable URL
};
```

Transitions between steps use CSS class swaps for animation:

```css
.step {
  opacity: 0;
  transform: translateY(20px);
  transition: opacity 0.3s ease, transform 0.3s ease;
  pointer-events: none;
  position: absolute;
}

.step.active {
  opacity: 1;
  transform: translateY(0);
  pointer-events: auto;
  position: relative;
}
```

---

## 11. Implementation Notes

### Mapping to Existing Codebase

The existing codebase (`/Users/gerinicka-new/holiday-planner/`) has the following components that map directly to this design:

| Design Screen | Existing Backend | Needs |
|---|---|---|
| Brief Input | `extract_trip_spec()` in `agents/orchestrator.py` | Web endpoint wrapping the CLI function |
| Confirmation | `TripSpecification` in `models/trip.py` | JSON serialization to/from frontend |
| Loading | `run_orchestrator()` in `agents/orchestrator.py` | SSE endpoint for progress events |
| Itinerary | `Itinerary` model + `itinerary.html.j2` template | Restyle template with new design system |
| Share | `get_whatsapp_share_url()` in `output/share.py` | Hosting on a public URL (Cloudflare R2, Vercel, etc.) |

### What Needs to Change in the Template

The existing Jinja2 template (`/Users/gerinicka-new/holiday-planner/templates/itinerary.html.j2`) needs a complete visual overhaul but the structural HTML is close. The key changes:

1. **Replace the color scheme** -- swap all `#0a0a0a` / `#111` / `#00b4d8` dark-theme values with the warm palette from Section 2.
2. **Add the serif font** for headlines (`DM Serif Display`).
3. **Rework the hero** to use a background image with gradient overlay instead of the solid gradient.
4. **Add the attribution banner** for recipient views (controlled by a template variable `is_owner`).
5. **Restyle all cards** from dark cards to white cards with subtle shadows.
6. **Replace the share button** in the sticky bar with the share sheet trigger.
7. **Add OG image meta tag** for WhatsApp preview.

### Required New Endpoints

```
POST /api/extract     — Takes { brief: string }, returns TripSpecification JSON
POST /api/plan        — Takes TripSpecification JSON, returns plan_id, starts research
GET  /api/plan/{id}/status — SSE stream of research progress events
GET  /plan/{id}       — Renders the itinerary page (the shareable URL)
GET  /og/plan/{id}.png — Dynamically generated OG image for WhatsApp preview
```

### Minimal JS Budget

The entire flow uses minimal JavaScript:

1. **Brief submission** -- form POST with fetch(), button loading state
2. **Confirmation editing** -- inline field editing with DOM manipulation
3. **Loading progress** -- EventSource (SSE) listener updating step states
4. **Cost tabs** -- same tab switching as current implementation
5. **Checklist** -- same localStorage pattern as current implementation
6. **Share sheet** -- show/hide a DOM element, clipboard API, WhatsApp deep link

Total JS estimate: under 200 lines, no framework needed. Vanilla JS with progressive enhancement.

### Image Strategy

The design relies on island photography. For MVP:

1. **Hero images** -- Use 5-6 curated, royalty-free aerial photos of popular Cycladic islands. Serve as WebP at 1200px wide, ~60KB each. Map island names to images in a simple lookup.
2. **Loading background** -- One soft-focus island image, served at 800px wide.
3. **OG image** -- Server-rendered using a Canvas or SVG-to-PNG approach. Shows trip details as styled text on a warm background.

No user-uploaded images. No Google Maps embeds. No external image dependencies that could break.

### Performance Targets

- **Landing page:** First Contentful Paint under 1.5s on 3G
- **Brief to Confirmation:** Under 3 seconds (API call)
- **Loading to Itinerary:** 30-60 seconds (show progress), perceived as fast because of the step-by-step reveal
- **Itinerary page load (shared link):** Under 2 seconds on 3G (it is a single self-contained HTML page)
- **Total page weight:** Under 150KB (HTML + CSS + JS + one hero image)

### Accessibility Fundamentals

- All interactive elements have focus styles (`:focus-visible` with `outline: 2px solid var(--aegean); outline-offset: 2px;`)
- Color contrast meets WCAG AA: `--ink` (#1A1A1A) on `--sand` (#FAF7F2) = 14.7:1 ratio
- Form inputs have associated labels
- The loading screen uses `aria-live="polite"` for step announcements
- Share sheet has `role="dialog"` and traps focus

---

## Appendix: Key Microcopy Reference

### Landing Page
- Logo: `TRIPFORGE`
- Headline: `Your Greek island trip, planned in 60 seconds.`
- Subhead: `Tell us about your trip in plain English. We'll find the flights, ferries, and places to stay -- and build a page you can share with your group.`
- CTA: `Start planning`
- Fine print: `No account needed. Free while in beta.`
- How-it-works step 1: `Describe your trip` / `Just write what you want, the way you'd tell a friend. "4 of us from London, Milos + Koufonisia, mid-August, 7 nights."`
- How-it-works step 2: `We do the research` / `We search flights, ferries, and accommodation across multiple sites. Real prices, real availability.`
- How-it-works step 3: `Share one beautiful page` / `Drop it in your group chat. Everyone sees the full plan -- the itinerary, the options, the prices, and where to book.`
- Social proof line: `Made for the person who does all the research so everyone else doesn't have to.`

### Brief Input
- Title: `Tell us about your trip`
- Subtitle: `Write it however you like -- the way you'd describe it to a friend.`
- Placeholder: (the full example brief)
- Hints header: `HELPFUL TO INCLUDE`
- Submit: `Build my trip`
- Submit loading state: `Understanding your trip...`

### Confirmation
- Title: `Here's what we understood`
- Subtitle: `Check the details, then we'll find flights, ferries, and places to stay.`
- CTA: `Looks good -- find options`
- Back link: `Go back and edit the brief`
- Edit button: `Edit`
- Empty state (if extraction failed): `We couldn't quite parse that. Could you try describing your trip again with a few more details?`

### Loading Screen
- Pre-title: `Planning your trip to`
- Title: `{island names}` (e.g., `Milos & Koufonisia`)
- Step labels: `Checking flights to Athens` / `Finding routes to Milos` / `Searching island ferries` / `Finding places to stay` / `Building your itinerary`
- Completion: `Your trip is ready`
- Fun fact prefix: `While you wait:`

### Itinerary Page
- Attribution (recipient): `Planned by {name} · powered by TripForge`
- Disclaimer: `Prices are estimates from {month} {year}. Tap any link to check live availability and book.`
- Section headers: `ITINERARY` / `MILOS ACCOMMODATION` / `ESTIMATED COSTS PER PERSON` / `WHAT TO BOOK FIRST` / `BOOKING CHECKLIST` / `USEFUL LINKS`
- Footer: `Built with TripForge · Prices are estimates, check links for live availability`

### Share Sheet
- Title: `Share your trip plan`
- WhatsApp option: `Share to WhatsApp` / `Opens WhatsApp with a preview message`
- Copy option: `Copy link` / `For any app or email`
- Copy success: `Link copied!`
- System share: `Share via...` / `Open system share sheet`
- Cancel: `Cancel`

### WhatsApp Pre-composed Message
```
{title} -- {islands}

{date range} · {group description} · ~{cost range}pp

I put together the full plan -- flights, ferries, places to stay, costs. Have a look:

{url}
```

---

*End of design document. This flow covers the complete user journey from first visit through group sharing. Every screen has been specified with layout, styling, interaction patterns, emotional intent, and implementation-ready CSS. The design prioritizes the organiser's emotional reward -- the moment their friends open the link and say "this is amazing."*
