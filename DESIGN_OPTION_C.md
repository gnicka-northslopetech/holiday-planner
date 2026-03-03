# Option C: The Action Plan Flow

## Complete UX Design Document for TripForge Web App

**Author:** Senior Product Designer (ex-Booking.com, 5 years on Trip Planner & Group Booking)
**Date:** February 2026
**Status:** Implementation-ready specification

---

## Table of Contents

1. [Design Philosophy](#1-design-philosophy)
2. [Design System](#2-design-system)
3. [Screen 1: Landing / Entry](#3-screen-1-landing--entry)
4. [Screen 2: Input (The Brief)](#4-screen-2-input-the-brief)
5. [Screen 3: Confirmation (Review & Edit)](#5-screen-3-confirmation-review--edit)
6. [Screen 4: Research / Loading](#6-screen-4-research--loading)
7. [Screen 5: Results / Itinerary](#7-screen-5-results--itinerary)
8. [Screen 6: Sharing](#8-screen-6-sharing)
9. [Screen 7: Post-Share (Recipient View)](#9-screen-7-post-share-recipient-view)
10. [State Management & Transitions](#10-state-management--transitions)
11. [Implementation Notes](#11-implementation-notes)

---

## 1. Design Philosophy

### The Core Insight

The Group Organiser is doing unpaid labor. They have 14 browser tabs open. They are copy-pasting flight times into a Notes app. They are doing currency conversions on their phone. They dread the WhatsApp thread where someone says "can we look at Mykonos instead?"

TripForge exists to compress 6 hours of research into 60 seconds of waiting, and to give the organiser a single shareable artifact that says: "Here is the plan. Here is what it costs you. Here is what to book first."

### Design Principles

1. **One question at a time.** Never show a form with 12 fields. The chat-style input lets the user dump their brain, then we confirm.
2. **Progress is visible.** The user always knows where they are and what happens next. Borrowed from Booking's 3-step checkout progress bar.
3. **Urgency without anxiety.** We use scarcity signals (ferry routes, small island accommodation) that are *actually true* -- not manufactured. This is Greece in August. The scarcity is real.
4. **The output is the product.** The itinerary page is not a "result" -- it is the thing the organiser shares. It must be beautiful on mobile, it must preview well in WhatsApp, and it must make the organiser look competent.
5. **Mobile-first, WhatsApp-native.** 80%+ of recipients will open the shared link on their phone. The organiser might start on desktop but will share from mobile.

### Key Behavioral Insight from Booking.com

At Booking, we learned that the *moment of highest engagement* is not the search -- it is the moment the user gets results and sees prices. They are most likely to share, screenshot, or forward at that exact moment. TripForge must capture this moment and channel it directly into the WhatsApp share action.

---

## 2. Design System

### Color Palette

```
Primary:         #003580  (Booking dark blue -- trust, authority)
Primary Light:   #00487a  (hover states, secondary surfaces)
Accent/CTA:      #febb02  (Booking yellow -- action, urgency)
Accent Hover:    #e5a800  (darkened yellow for hover)
Success:         #008009  (Booking green -- confirmations, savings)
Urgency:         #c00     (red -- book now, selling fast)
Urgency Soft:    #b93d00  (orange-red -- moderate urgency)

Background:      #f5f5f5  (page background)
Surface:         #ffffff  (cards)
Surface Raised:  #ffffff  (cards with shadow)
Border:          #e6e6e6  (card borders, dividers)
Border Light:    #f0f0f0  (subtle dividers)

Text Primary:    #1a1a1a  (headings, important text)
Text Secondary:  #474747  (body text)
Text Tertiary:   #6b6b6b  (labels, captions)
Text Inverted:   #ffffff  (text on dark/primary backgrounds)
Text Link:       #006ce4  (Booking link blue)

Rating:          #febb02  (star/score color, same as CTA)
Badge BG:        #f0f6ff  (light blue badge background)
Badge Text:      #003580  (badge text)
```

### Typography

```
Font Stack:      'Avenir Next', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif
                 (Booking uses their custom BlinkMacSystem, we use Avenir Next for similar warmth)

Fallback Web:    'Inter', -apple-system, sans-serif
                 (Google Font fallback if Avenir not available)

Heading 1:       32px / 38px, weight 700, color #1a1a1a, letter-spacing -0.5px
Heading 2:       24px / 30px, weight 700, color #1a1a1a, letter-spacing -0.3px
Heading 3:       18px / 24px, weight 600, color #1a1a1a
Body:            14px / 22px, weight 400, color #474747
Body Small:      13px / 20px, weight 400, color #6b6b6b
Caption:         12px / 16px, weight 400, color #6b6b6b
Label:           12px / 16px, weight 600, text-transform uppercase, letter-spacing 0.5px, color #6b6b6b
Price Large:     28px / 32px, weight 700, color #1a1a1a
Price Medium:    20px / 24px, weight 700, color #1a1a1a
Badge:           12px / 16px, weight 600
```

### Spacing Scale

```
4px, 8px, 12px, 16px, 20px, 24px, 32px, 40px, 48px, 64px
```

### Border Radius

```
Small:    4px   (badges, tags)
Medium:   8px   (cards, inputs)
Large:    12px  (modals, large cards)
Full:     9999px (pills, buttons)
```

### Shadows

```
Card:       0 1px 4px rgba(0,0,0,0.08), 0 0 0 1px rgba(0,0,0,0.04)
Card Hover: 0 2px 8px rgba(0,0,0,0.12), 0 0 0 1px rgba(0,0,0,0.06)
Elevated:   0 4px 16px rgba(0,0,0,0.12)
Sticky:     0 -2px 8px rgba(0,0,0,0.08)
```

### Components

#### Primary Button (CTA)
```css
.btn-primary {
  background: #febb02;
  color: #1a1a1a;
  font-size: 16px;
  font-weight: 600;
  padding: 14px 32px;
  border-radius: 9999px;
  border: none;
  cursor: pointer;
  transition: background 0.15s ease;
  font-family: inherit;
  line-height: 1;
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 8px;
  min-height: 48px;
}
.btn-primary:hover { background: #e5a800; }
.btn-primary:active { transform: scale(0.98); }
```

#### Secondary Button
```css
.btn-secondary {
  background: transparent;
  color: #006ce4;
  font-size: 14px;
  font-weight: 600;
  padding: 10px 24px;
  border-radius: 9999px;
  border: 1px solid #006ce4;
  cursor: pointer;
  transition: background 0.15s ease;
  font-family: inherit;
}
.btn-secondary:hover { background: #f0f6ff; }
```

#### Card
```css
.card {
  background: #ffffff;
  border-radius: 8px;
  border: 1px solid #e6e6e6;
  padding: 20px;
  transition: box-shadow 0.15s ease;
}
.card:hover {
  box-shadow: 0 2px 8px rgba(0,0,0,0.12);
}
```

#### Badge
```css
.badge {
  display: inline-flex;
  align-items: center;
  gap: 4px;
  padding: 4px 8px;
  border-radius: 4px;
  font-size: 12px;
  font-weight: 600;
  line-height: 1;
}
.badge-flight { background: #f0f6ff; color: #003580; }
.badge-ferry  { background: #e8f5e9; color: #1b5e20; }
.badge-urgency { background: #ffeee8; color: #c00; }
.badge-info   { background: #f0f6ff; color: #006ce4; }
```

#### Progress Bar (top of page, always visible during flow)
```css
.progress-bar {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: #e6e6e6;
  z-index: 1000;
}
.progress-bar__fill {
  height: 100%;
  background: #003580;
  transition: width 0.4s ease;
}
```

---

## 3. Screen 1: Landing / Entry

### URL: `tripforge.app/`

### Emotional State: Curious, slightly overwhelmed, looking for a shortcut

The organiser has just been voluntold in a WhatsApp group that they are "the planner." They Google "greek island trip planner" or get a link from a friend. They arrive here.

### Layout

```
[Full-screen single view, no scroll needed on desktop]

HEADER BAR (height: 56px, white, subtle bottom border)
  Left:   TripForge logo (icon + wordmark, #003580)
  Right:  [empty -- no nav, no hamburger, no distractions]

HERO SECTION (centered, max-width 640px, padding-top 80px)
  [Illustration: minimal line art of Greek islands,
   or a single high-quality photo of Cycladic white+blue
   with subtle gradient overlay. Keep it fast -- use CSS
   gradient fallback if image hasn't loaded.]

  H1: "Plan your Greek Islands trip in 60 seconds"

  Subhead (Body, color #474747):
  "Tell us where you're going, who's coming, and when.
   We'll research flights, ferries, and places to stay --
   and build a plan you can share with your group."

  [PRIMARY INPUT AREA -- see next section for detail]

  SOCIAL PROOF BAR (below input, 16px margin-top):
  "1,247 trips planned this month"
  (small dot separator)
  "Milos, Santorini, Naxos, Paros, and 11 more islands"

TRUST STRIP (fixed bottom, padding 16px, border-top)
  Row of small gray logos:
  "Data from" Skyscanner  Ferryhopper  Booking.com  Airbnb
  (logos at 50% opacity, 20px height)
```

### The Input Widget

This is the single most important component on the page. Borrowing from Booking's search bar -- it looks simple but is enormously powerful. However, instead of separate fields for destination/dates/guests, we use a single free-text input that *looks* like a chat message.

```
[White card, border-radius 12px, shadow: Elevated, padding: 24px]

  PLACEHOLDER TEXT (inside a textarea, not an input):
  "e.g. 3 couples from London and Athens, going to
   Milos and Koufonisia, August 14-21, mid-range budget"

  [Textarea: 3 rows visible, auto-expand up to 6 rows]
  [Font: 16px (prevents iOS zoom), color: #1a1a1a]
  [Border: 2px solid #e6e6e6, focus: 2px solid #003580]
  [Border-radius: 8px, padding: 16px]

  [Below textarea, right-aligned:]
  [PRIMARY BUTTON] "Build my trip plan"
  [Below button, centered, Caption style:]
  "Takes about 60 seconds. Free, no signup required."
```

### Quick-Start Chips (below the card, 12px gap)

For users who want even less friction. Tapping a chip fills the textarea.

```
Popular trips:

[chip] "London to Santorini + Milos, 7 nights, couple"
[chip] "4 friends, Mykonos + Paros + Naxos, 10 days"
[chip] "Family of 4, Crete + Santorini, last week of August"
```

Chip styling:
```css
.quick-chip {
  display: inline-block;
  padding: 8px 16px;
  border-radius: 9999px;
  border: 1px solid #e6e6e6;
  font-size: 13px;
  color: #474747;
  background: #fff;
  cursor: pointer;
  transition: border-color 0.15s, background 0.15s;
}
.quick-chip:hover {
  border-color: #003580;
  background: #f0f6ff;
  color: #003580;
}
```

### Mobile Adaptation (< 600px)

- Hero padding-top reduces to 40px
- H1 drops to 24px
- Textarea fills full width
- Quick-start chips stack vertically
- Trust strip logos wrap to 2 lines

### Interactions

1. User types (or taps a chip) in the textarea
2. As they type, the "Build my trip plan" button pulses subtly with a glow animation on first render (attention-grab), then settles
3. Button is disabled (gray) until textarea has > 20 characters
4. On button click: textarea content is sent to the extraction endpoint
5. Transition: card gently shrinks up, a spinner appears inline inside the button ("Understanding your trip..."), then the page transitions to Screen 3

### What NOT to do here

- No signup wall. No email capture. The output page is the email capture (they will come back).
- No multi-step wizard for the first interaction. Get them to results as fast as possible.
- No feature tour. No "how it works" carousel. The subhead says everything.

---

## 4. Screen 2: Input (The Brief)

### This is NOT a separate screen

The input lives on Screen 1. However, there is an important *micro-interaction* that deserves its own section: the AI extraction step.

### What Happens After They Click "Build my trip plan"

The button text changes to "Understanding your trip..." with a small spinner. The textarea becomes read-only (slight opacity reduction to 0.7). This takes 2-5 seconds (Claude Haiku extraction).

If extraction fails or is ambiguous, we show inline clarification questions below the textarea:

```
[Yellow-tinted card, border-left: 3px solid #febb02]

"Just checking a couple of things:"

[Question 1] "How many nights on each island?"
  [Inline mini-inputs: "Milos" [__5__] nights  "Koufonisia" [__2__] nights]

[Question 2] "Flying from where?"
  [Chips: "London (Heathrow/Gatwick)" "London (Stansted)" "Other: ____"]

[BUTTON] "That's right, continue"
```

This pattern only appears when the AI cannot confidently extract all required fields. In the happy path (user provides complete info like the example placeholder), we skip straight to Screen 3.

### Extraction → Confirmation Transition Animation

1. Textarea card slides up slightly
2. A "receipt" card slides in from below (the Confirmation screen)
3. Total transition: 300ms, ease-out

---

## 5. Screen 3: Confirmation (Review & Edit)

### URL: `tripforge.app/#confirm` (same page, hash-routed)

### Emotional State: "Did it understand me correctly?" -- mild anxiety, want to verify before waiting

This is directly inspired by Booking's "Review your booking details" page that appears before payment. The user needs to see their trip details structured back to them and confirm before we spend 30-60 seconds researching.

### Layout

```
PROGRESS BAR: [====25%==========                    ]
              "Step 1 of 3: Confirm your trip"

HEADER BAR (same as before)

MAIN CONTENT (max-width: 600px, centered, padding: 24px)

  H2: "Here's what we understood"
  Body: "Check these details before we research prices."

  [TRIP SUMMARY CARD -- white, border-radius 12px, shadow]

    TRIP TITLE (editable inline):
    "Greece 2026"  [edit icon, pencil, 16px, #6b6b6b]

    SECTION: "Your Group"
    --------------------------------
    [icon: people]  3 couples (6 travelers)
    [icon: plane]   London crew (4 people) -- flying from London
    [icon: pin]     Athens crew (2 people) -- already in Greece

    [link: "Edit group details"]  (expands inline editor)

    SECTION: "Your Route"
    --------------------------------
    [Visual route pills, same style as existing template but light-mode:]

    [London] --> [Athens] --> [Milos] --> [Koufonisia] --> [Athens] --> [London]
     fly          fly/ferry    5 nights     2 nights       ferry        fly

    SECTION: "Dates"
    --------------------------------
    [icon: calendar]  Fri 14 Aug -- Fri 21 Aug 2026 (7 nights)

    [Date picker trigger -- opens native date picker on mobile,
     flatpickr on desktop. Inline, not modal.]

    SECTION: "Islands"
    --------------------------------
    [For each island, a sub-card:]

    [Island Card: Milos]
      5 nights | Needs a car rental
      "Sarakiniko, Kleftiko boat tour, Plaka sunset"
      [edit] [remove]

    [Island Card: Koufonisia]
      2 nights | Walk everywhere
      "Tiny island, Pori beach"
      [edit] [remove]

    [+ Add another island]  (opens island picker -- searchable list)

    SECTION: "Preferences"
    --------------------------------
    [Tags:] Beach-focused | Good food | Mix of activity and relaxation
    [+ Add preference]

    SECTION: "Budget"
    --------------------------------
    "Mid-range, not backpacker but not luxury"
    [Toggle pills:] [Budget] [Mid-range (selected)] [Comfort] [Luxury]

  [END CARD]

  [URGENCY NUDGE -- subtle, below the card:]
  [icon: fire, orange]  "August is peak season for Greek islands.
                          Koufonisia has only ~20 places to stay
                          on the entire island."
  [Caption:] "The sooner you have a plan, the sooner you can book."

  [PRIMARY BUTTON, full-width on mobile:]
  "Research flights, ferries & stays"

  [Caption below button:]
  "This takes about 60 seconds. We'll search Skyscanner,
   Ferryhopper, Booking.com, and more."
```

### Edit Interactions

Each section has an [edit] trigger (pencil icon or "Edit" text link). Clicking it:
- Expands that section inline with form fields
- The rest of the card dims slightly (opacity 0.5)
- A "Save" button appears inline
- The section collapses back on Save

This avoids modals entirely. Everything happens in-flow.

### Island Picker (for "Add another island")

```
[Expanding section, slides down]

  [Search input:] "Search islands..."

  [Grid of island cards, 2 columns:]
  Each card shows:
    Island name
    One-line description
    "Needs car" or "Walkable" tag
    "Has airport" tag (if applicable)

  Popular first: Santorini, Mykonos, Naxos, Paros, Milos, Ios, Sifnos...

  On select: card highlights with blue border,
  "How many nights?" input appears, then "Add to route" button
```

### Island Card Detail (edit mode)

```
[Expanded card]
  Island: Milos
  Nights: [- 5 +]  (stepper input)
  Needs car: [toggle switch, on]
  Notes: [textarea, optional] "Sarakiniko, Kleftiko..."
  [Save] [Remove from trip]
```

### Mobile Adaptation

- Full-width cards, no horizontal padding beyond 16px
- Route pills scroll horizontally if > 4 stops
- Edit sections push content down (no overlays)
- CTA button is sticky at bottom when scrolled past it

### The Confirm Button Behavior

On tap:
1. Button text changes to "Searching..." with spinner
2. Page scrolls to top
3. Smooth transition to Screen 4 (loading)
4. Button becomes part of the loading UI (it was the last thing they touched, so the loading feels like a continuation)

---

## 6. Screen 4: Research / Loading

### URL: `tripforge.app/#researching` (same page, hash-routed)

### Emotional State: Waiting -- this is where you either lose them or build anticipation. 30-60 seconds is an eternity. Booking.com uses this time brilliantly.

### The Golden Rule of Loading States

Booking taught me: if the user is watching a spinner, you have already failed. The loading screen must be *more interesting than opening a new tab*. Every second of dead time is a second they might tab away to Google Flights.

### Layout

```
PROGRESS BAR: [==========50%===========             ]
              "Step 2 of 3: Researching your trip"

HEADER BAR

MAIN CONTENT (max-width: 600px, centered)

  [TRIP SUMMARY STRIP -- compact, sticky below header]
  "Greece 2026 | 3 couples | Aug 14-21 | Milos + Koufonisia"
  (One line, 13px, #6b6b6b, acts as context reminder)

  [ANIMATED RESEARCH FEED -- the core of this screen]

  This is a vertical feed of cards that appear one by one,
  each representing a research step completing. Cards animate
  in with a slide-up + fade (200ms each, staggered).

  Each card has:
  - Left icon (contextual: plane, ferry, bed)
  - Research step description
  - Status: spinner (in progress) or green check (done)
  - When done: a teaser of what was found

  CARD SEQUENCE (appears over 30-60 seconds):

  [1] [plane icon] [green check]
      "Searching London to Athens flights..."
      "Found 12 options from 5 airlines -- cheapest GBP85"
      [2 seconds after appearing, check replaces spinner]

  [2] [plane icon] [green check]
      "Searching Athens to Milos flights..."
      "Found 4 options -- Olympic Air & Sky Express from EUR45"

  [3] [ferry icon] [green check]
      "Checking Piraeus to Milos ferries..."
      "SeaJets high-speed 2h 35m from EUR63"

  [4] [bed icon] [spinner...]
      "Searching Milos accommodation (5 nights)..."
      [When done:] "Found 5 options -- EUR118-321/night"

  [5] [ferry icon] [green check]
      "Checking Milos to Koufonisia ferries..."
      "SeaJets ~4h, limited schedule -- check sailing days"

  [6] [bed icon] [spinner...]
      "Searching Koufonisia accommodation (2 nights)..."
      [When done:] "Found 6 options -- USD85-194/night"
      [URGENCY INLINE:]
        [red dot] "Only ~20 properties on this island"

  [7] [ferry icon] [green check]
      "Checking Koufonisia to Piraeus return ferries..."

  [8] [plane icon] [green check]
      "Searching Athens to London return flights..."
      "Found 8 options from EUR79"

  [9] [calculator icon] [green check]
      "Calculating costs per person..."

  [10] [sparkle icon] [green check]
       "Building your itinerary..."

  [END STATE -- all cards have green checks]
```

### Urgency / Social Proof Interstitials

Between research cards (not every time -- 2-3 of these total), inject contextual nuggets:

```
[Interstitial 1 -- appears after accommodation search starts]
[Yellow-left-border card, no icon]
  "Peak season alert"
  "August 14-21 includes the Assumption of Mary (Aug 15),
   one of Greece's biggest holidays. Popular islands book
   out months in advance."

[Interstitial 2 -- appears after Koufonisia accommodation]
[Red-left-border card]
  "Koufonisia is a tiny island"
  "There are roughly 20 places to stay on the entire island.
   In August, they often sell out by March."

[Interstitial 3 -- appears near the end]
[Blue-left-border card]
  "This route is a great choice"
  "Milos + Koufonisia gives you volcanic landscapes, secluded
   beaches, and one of the most authentic Small Cyclades islands."
```

These are NOT pop-ups. They are inline cards in the feed, styled slightly differently from research cards. They build anticipation and context.

### The "Almost Done" Moment

When 8/10 steps are complete:

```
[The progress bar accelerates]
[Below the feed:]

  "Your trip plan is almost ready..."
  [Subtle pulsing dot animation]
```

When all 10 steps complete:

```
[Progress bar hits 100%]
[All cards get green checks]
[1-second pause -- let the completion register]

[Then: the entire feed fades out (300ms)]
[Screen 5 fades in from below]
```

### What If They Tab Away?

If `document.hidden` becomes true during research:
- When they return, snap to current state (no replaying animations)
- If research is done, show a brief "Welcome back! Your plan is ready." with a button

### What If Research Takes > 60 Seconds?

After 45 seconds, show:
```
"This is taking a bit longer than usual.
 Complex routes with multiple islands need extra research time."
[Still show the feed with remaining spinners]
```

After 90 seconds:
```
"Almost there -- just finalizing a few details."
```

This is honest, not manipulative. Multi-source research genuinely varies.

### Card Styling

```css
.research-card {
  background: #fff;
  border: 1px solid #e6e6e6;
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 12px;
  display: flex;
  align-items: flex-start;
  gap: 12px;
  animation: slideUp 0.3s ease-out;
}

.research-card__icon {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.research-card__icon--flight { background: #f0f6ff; color: #003580; }
.research-card__icon--ferry  { background: #e8f5e9; color: #1b5e20; }
.research-card__icon--stay   { background: #fff3e0; color: #e65100; }
.research-card__icon--calc   { background: #f3e5f5; color: #6a1b9a; }

.research-card__title {
  font-size: 14px;
  font-weight: 500;
  color: #1a1a1a;
  margin-bottom: 2px;
}

.research-card__result {
  font-size: 13px;
  color: #6b6b6b;
}

.research-card__result strong {
  color: #1a1a1a;
}

.research-card__status {
  margin-left: auto;
  flex-shrink: 0;
}

.research-card__check {
  width: 20px;
  height: 20px;
  border-radius: 50%;
  background: #008009;
  color: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
}

@keyframes slideUp {
  from { opacity: 0; transform: translateY(16px); }
  to   { opacity: 1; transform: translateY(0); }
}

.urgency-interstitial {
  background: #fff;
  border-radius: 8px;
  padding: 16px 20px;
  margin-bottom: 12px;
  border-left: 3px solid #febb02;
  animation: slideUp 0.3s ease-out;
}

.urgency-interstitial--red {
  border-left-color: #c00;
}

.urgency-interstitial--blue {
  border-left-color: #003580;
}
```

---

## 7. Screen 5: Results / Itinerary

### URL: `tripforge.app/trip/abc123` (unique, shareable URL)

### Emotional State: The payoff. "Holy shit, this is exactly what I needed." The organiser sees their entire trip laid out, priced, and actionable. This is the moment they share.

### Critical Design Decision: Light Mode

The current template uses a dark theme (#0a0a0a background). For the web app, we switch to Booking-style light mode. Reasons:
1. WhatsApp preview cards render better with light OG images
2. Light mode is more "trustworthy" for pricing information (Booking, Google Flights, Skyscanner all use light mode)
3. Readability of price comparisons and tables is superior
4. Screenshots shared in WhatsApp groups look cleaner

The dark theme is beautiful and can remain as an option or for a "premium" feel, but the default shareable output must be light.

### Layout

```
PROGRESS BAR: [=============================100%]
              "Your trip plan is ready"
              (fades out after 3 seconds)

[OG META TAGS -- critical for WhatsApp preview:]
og:title       = "Greece 2026 -- Milos & Koufonisia"
og:description = "3 couples | Aug 14-21 | Est. EUR700-1,500pp | Built with TripForge"
og:image       = [dynamically generated card image, 1200x630px]
                 (shows route: London > Athens > Milos > Koufonisia)
                 (shows price range)
                 (shows date range)
                 (Cycladic blue gradient background)

===============================================

HERO SECTION
  Background: linear-gradient(135deg, #003580 0%, #006ce4 100%)
  Padding: 40px 24px 32px
  Text color: white

  [Logo: TripForge, small, top-left, white]

  H1: "Greece 2026"

  Subtitle: "Milos & Koufonisia"
  (18px, weight 300, rgba(255,255,255,0.85))

  [Pill badge, inline:]
  "Fri 14 Aug -- Fri 21 Aug 2026  |  3 couples  |  6 travelers"
  (background: rgba(255,255,255,0.15), border-radius: 9999px,
   padding: 8px 20px, font-size: 14px)

  [Route visualization:]
  [London] --plane--> [Athens] --plane/ferry--> [Milos] --ferry--> [Koufonisia] --ferry--> [Athens] --plane--> [London]

  (Same pill style as current template but white-on-blue instead of white-on-dark.
   Transport mode icons between pills instead of plain arrows.)

STICKY ACTION BAR (appears on scroll, fixed bottom)
  Height: 64px
  Background: white
  Border-top: 1px solid #e6e6e6
  Shadow: Sticky

  Left:  "Est. per person"
         "EUR700 -- 1,500" (Price Medium, #003580)
  Right: [PRIMARY BUTTON] "Share with group"
         (opens share sheet, see Screen 6)

===============================================

MAIN CONTENT
  max-width: 680px, centered
  padding: 0 20px
  background: #f5f5f5

-----------------------------------------------
SECTION: "Your Itinerary"
  Section title styling:
    font-size: 12px, weight 600, uppercase,
    letter-spacing 1.5px, color #6b6b6b,
    margin-bottom 16px, padding-bottom 8px,
    border-bottom: 1px solid #e6e6e6

  [DAY CARDS -- one per day/block]

  [Day Card: Travel Day]
    Background: white
    Border-radius: 8px
    Border: 1px solid #e6e6e6
    Padding: 20px
    Margin-bottom: 12px
    Border-left: 4px solid #003580

    Header row:
      Left:  "Thu Aug 14" (12px, weight 600, #6b6b6b)
      Right: (nothing)

    H3: "Travel Day" (18px, weight 600, #1a1a1a)
    Subtitle: "London > Athens > Milos" (14px, #006ce4)

    [Transport legs, each as a sub-row:]

    [FLIGHT badge] London to Athens -- 3h 30m direct
      BA from GBP130 | Aegean GBP145 | easyJet GBP95 | Ryanair GBP89
      (each airline is a small clickable pill that opens booking URL)

    [FLIGHT badge] Athens to Milos -- 40 min
      Olympic Air from EUR55 | Sky Express from EUR45

    [FERRY badge] Piraeus to Milos -- SeaJets 2h 35m -- EUR76
      "Ferry alternative to flying"

    [INFO NOTE, yellow-left-border:]
    "Athens crew: Same options -- fly from ATH or take the ferry
     from Piraeus. Coordinate arrival times in the group chat."

  [Day Card: Milos -- HIGHLIGHT]
    Border-left: 4px solid #febb02  (amber for highlight days)

    Header row:
      Left:  "Aug 14-19" (12px, weight 600, #6b6b6b)
      Right: [badge] "5 nights" | [badge] "Needs car"

    H3: "Milos" (18px, weight 600, #1a1a1a)

    [Activity list with custom bullet (small filled circle, #003580):]
    - Sarakiniko (lunar landscape beach)
    - Tsigrado & Firiplaka (south coast gems)
    - Kleftiko boat tour from Adamas (~EUR60-120pp)
    - Plaka village for sunset
    - Paleochori (hot sand beach with tavernas)

    [WARNING NOTE, red-left-border:]
    "Aug 15 is Assumption of Mary -- big Greek holiday.
     Expect crowds and some businesses closed."

  [Day Card: Island Hop]
    Border-left: 4px solid #003580

    "Wed Aug 19"
    H3: "Island Hop"
    Subtitle: "Milos > Koufonisia"

    [FERRY badge] SeaJets -- ~4h -- EUR105 per person

    [WARNING NOTE:]
    "This route may only run on certain days.
     Check the sailing schedule for August 19."

  [Day Card: Koufonisia -- HIGHLIGHT]
    (same pattern as Milos card)

  [Day Card: Return]
    (same pattern as Travel Day card)

-----------------------------------------------
SECTION: "Where to Stay"

  [Sub-section: Milos Accommodation]
    Section subtitle:
    "Milos | Aug 14-19 (5 nights) | 2 guests"
    (14px, weight 500, #474747)

    [Accommodation cards -- Booking.com list-item style:]

    Each card:
    +-----------------------------------------------+
    |  [Property name]              [Rating badge]   |
    |  [Location + features]        [8.7/10]         |
    |  [Source badge: Holidu]       "Very Good"       |
    |                                                 |
    |                    EUR118/night | ~EUR590 total  |
    |                    [View on Holidu -->]          |
    +-----------------------------------------------+

    Card CSS:
    ```
    Background: white
    Border: 1px solid #e6e6e6
    Border-radius: 8px
    Padding: 16px 20px
    Margin-bottom: 8px
    Display: flex
    Justify-content: space-between
    Align-items: center
    ```

    Rating badge (Booking style):
    ```
    Background: #003580
    Color: white
    Border-radius: 4px 4px 4px 0
    Padding: 4px 8px
    Font-size: 14px
    Font-weight: 700
    ```

    Rating label:
    ```
    Font-size: 12px
    Color: #474747
    ```

    10.0 = "Exceptional"
    9.0+ = "Wonderful"
    8.0+ = "Very Good"
    7.0+ = "Good"

    Price:
    ```
    Font-size: 20px
    Font-weight: 700
    Color: #1a1a1a
    ```

    "per night" and total:
    ```
    Font-size: 12px
    Color: #6b6b6b
    ```

    View link:
    ```
    Color: #006ce4
    Font-size: 13px
    Font-weight: 600
    ```

    Show first 3, then:
    [Expandable: "Show 2 more options"]
    (uses <details><summary> for zero-JS)

  [Sub-section: Koufonisia Accommodation]
    (same pattern)

    [URGENCY BANNER at top of this sub-section:]
    Background: #ffeee8
    Border-radius: 8px
    Padding: 12px 16px

    [flame icon] "Only ~20 properties on this island.
                   August availability disappears fast."
    Font-size: 13px, color: #c00, weight: 500

-----------------------------------------------
SECTION: "Estimated Costs Per Person"

  [Tab bar for multi-origin groups:]
  [London group (active)]  [Athens couple]

  Tab styling:
  ```css
  .cost-tab {
    padding: 8px 20px;
    border-radius: 9999px;
    font-size: 13px;
    font-weight: 600;
    cursor: pointer;
    border: none;
    background: #f0f0f0;
    color: #6b6b6b;
  }
  .cost-tab--active {
    background: #003580;
    color: #fff;
  }
  ```

  [Cost table -- clean, Booking-style:]
  ```
  Flights London <-> Athens (return)        GBP85 -- 145
  Flight Athens -> Milos (one way)          EUR45 -- 55
  Ferry Milos -> Koufonisia                 EUR105
  Ferry Koufonisia -> Piraeus               EUR38 -- 64
  Taxi Piraeus -> Airport                   EUR20 (shared)
  Milos accommodation (5 nights, per person) $295 -- $802
  Koufonisia accommodation (2 nights, pp)    $85 -- $194
  Car rental Milos (5 days, shared)          EUR75 -- 125
  ─────────────────────────────────────────────────────
  TOTAL PER PERSON (APPROX)                 EUR700 -- 1,500
  ```

  Table styling:
  ```css
  .cost-table { width: 100%; border-collapse: collapse; }
  .cost-table td {
    padding: 12px 0;
    font-size: 14px;
    border-bottom: 1px solid #f0f0f0;
  }
  .cost-table td:first-child { color: #474747; }
  .cost-table td:last-child {
    text-align: right;
    color: #1a1a1a;
    font-weight: 600;
  }
  .cost-table tr.total td {
    border-top: 2px solid #003580;
    border-bottom: none;
    padding-top: 16px;
    font-size: 16px;
    font-weight: 700;
    color: #003580;
  }
  ```

  [Below table:]
  Caption: "Prices are estimates based on current availability.
            Check booking links for live prices."

-----------------------------------------------
SECTION: "What to Book First"

  This is the highest-value section of the page. It tells the
  organiser exactly what to do, in order, with direct links.

  [Numbered action cards:]

  [1] [URGENT badge: red]
      "Koufonisia accommodation"
      "Only ~20 places on the entire island. August sells out completely."
      [Button: "Search Airbnb"] [Button: "Search Booking.com"]

  [2] [URGENT badge: orange]
      "Athens -> Milos flight"
      "Tiny 70-seat turboprops. Sells out months ahead."
      [Button: "Olympic Air"] [Button: "Sky Express"]

  [3] "Milos accommodation"
      "Peak August -- book early for best selection."
      [Button: "Search Holidu"] [Button: "Search Airbnb"]

  ...and so on.

  Card styling:
  ```css
  .action-card {
    background: #fff;
    border: 1px solid #e6e6e6;
    border-radius: 8px;
    padding: 20px;
    margin-bottom: 12px;
    position: relative;
    padding-left: 56px;
  }
  .action-card__number {
    position: absolute;
    left: 20px;
    top: 20px;
    width: 24px;
    height: 24px;
    border-radius: 50%;
    background: #003580;
    color: #fff;
    font-size: 12px;
    font-weight: 700;
    display: flex;
    align-items: center;
    justify-content: center;
  }
  .action-card__title {
    font-size: 15px;
    font-weight: 600;
    color: #1a1a1a;
    margin-bottom: 4px;
  }
  .action-card__reason {
    font-size: 13px;
    color: #6b6b6b;
    margin-bottom: 12px;
  }
  .action-card__links {
    display: flex;
    gap: 8px;
    flex-wrap: wrap;
  }
  .action-link {
    display: inline-flex;
    align-items: center;
    gap: 4px;
    padding: 8px 16px;
    border-radius: 9999px;
    border: 1px solid #006ce4;
    color: #006ce4;
    font-size: 13px;
    font-weight: 600;
    text-decoration: none;
    transition: background 0.15s;
  }
  .action-link:hover {
    background: #f0f6ff;
  }
  ```

-----------------------------------------------
SECTION: "Booking Checklist"

  [Interactive checklist with localStorage persistence]
  Same pattern as current template but light-themed:

  Each item:
  ```
  [ ] Koufonisia accommodation
  [ ] Athens -> Milos flight
  [ ] Milos accommodation
  [ ] London <-> Athens flights
  [ ] Ferries
  [ ] Car rental (Milos)
  ```

  Checkbox styling:
  ```css
  .checklist-item {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 14px 16px;
    background: #fff;
    border: 1px solid #e6e6e6;
    border-radius: 8px;
    margin-bottom: 6px;
    cursor: pointer;
    transition: opacity 0.2s;
  }
  .checklist-item--done {
    opacity: 0.5;
    text-decoration: line-through;
  }
  .checklist-item input[type="checkbox"] {
    width: 20px;
    height: 20px;
    accent-color: #003580;
  }
  ```

-----------------------------------------------
SECTION: "Useful Links"

  [2-column grid of link cards, same as current template but light-mode]

-----------------------------------------------

FOOTER
  "Built with TripForge | Prices are estimates | Feb 2026"
  Font-size: 12px, color: #6b6b6b, text-align: center
  Padding: 32px 20px 100px (100px for sticky bar clearance)
```

### Mobile Adaptation (< 600px)

- Hero: H1 at 24px, route pills scroll horizontally
- Day cards: full bleed (no side margin, only top/bottom gap)
- Accommodation cards: stack price below info (flex-direction: column)
- Cost table: smaller font (13px), abbreviate labels
- Action cards: buttons stack vertically
- Sticky bar: price on top line, button on second line (full width)

---

## 8. Screen 6: Sharing

### Emotional State: Pride. The organiser has built something comprehensive and wants to drop it in the WhatsApp group with authority.

### The Share Trigger

The "Share with group" button in the sticky bar triggers a native share sheet on mobile (via `navigator.share()`) or a custom share modal on desktop.

### Mobile (navigator.share available)

```javascript
navigator.share({
  title: "Greece 2026 -- Milos & Koufonisia",
  text: "Here's our trip plan! Flights, ferries, accommodation all researched. Check what we need to book first.",
  url: "https://tripforge.app/trip/abc123"
});
```

This opens the native iOS/Android share sheet. WhatsApp, iMessage, Telegram, etc. all appear. The user chooses WhatsApp, picks their group, and sends.

### Desktop (no navigator.share)

A custom modal appears:

```
[Modal, centered, max-width 440px]
[Background overlay: rgba(0,0,0,0.4)]
[Modal background: white, border-radius: 12px, padding: 32px]

  H3: "Share your trip plan"

  [WhatsApp share button -- full width, green:]
  Background: #25D366
  Color: white
  Text: "Send on WhatsApp"
  Icon: WhatsApp logo (left)

  (Opens: https://wa.me/?text=...)

  The prefilled WhatsApp message:
  "Greece 2026 -- Milos & Koufonisia
   3 couples | Aug 14-21 | ~EUR700-1,500pp

   I've researched flights, ferries, and places to stay.
   Have a look and tell me what you think:
   https://tripforge.app/trip/abc123"

  [Separator: "or"]

  [Copy link button -- secondary style:]
  "Copy link"
  (On click: copies URL, button text changes to
   "Copied!" with a green check for 2 seconds)

  [Email button -- secondary style:]
  "Send by email"
  (Opens mailto: with subject and body prefilled)

  [Close: X button, top-right corner]
```

### WhatsApp Preview Card

When the link is pasted in WhatsApp, the og:meta tags generate this preview:

```
+------------------------------------------+
|  Greece 2026 -- Milos & Koufonisia       |
|  3 couples | Aug 14-21 | EUR700-1,500pp  |
|  Built with TripForge                    |
|  [gradient image: route visualization]    |
+------------------------------------------+
```

The og:image is critical. It should be a 1200x630px image with:
- Blue gradient background (#003580 to #006ce4)
- White text: trip title, subtitle, date range
- Route pills: London > Athens > Milos > Koufonisia
- Price range in large text
- TripForge logo, small, bottom-right

This image can be generated server-side (e.g., Satori/Vercel OG, or a simple SVG-to-PNG).

### Pre-Share Nudge

Before the share sheet opens, show a brief toast at the bottom:

```
"Tip: Ask everyone to check the 'What to Book First' section.
 The sooner Koufonisia accommodation is sorted, the better."
```

Toast styling:
```css
.share-tip {
  position: fixed;
  bottom: 80px;
  left: 20px;
  right: 20px;
  max-width: 440px;
  margin: 0 auto;
  background: #1a1a1a;
  color: #fff;
  padding: 16px 20px;
  border-radius: 8px;
  font-size: 13px;
  animation: fadeUp 0.3s ease-out;
  z-index: 200;
}
```

---

## 9. Screen 7: Post-Share (Recipient View)

### URL: Same as Screen 5: `tripforge.app/trip/abc123`

### Emotional State: Curiosity mixed with relief. "Finally, someone figured out the logistics." The recipient wants to know: What does this cost me? What do I need to do?

### What the Recipient Sees

The same itinerary page as the organiser, but with two key differences:

### Difference 1: Top Banner for Recipients

When someone opens the link and has not been to TripForge before (no localStorage flag), show a contextual banner:

```
[Full-width banner, background: #f0f6ff, padding: 16px 20px]
[Dismissable: X button top-right]

  "[Name, if available from WhatsApp -- otherwise 'Someone']
   shared this trip plan with you."

  "Scroll down to 'What to Book First' to see what needs
   booking urgently."

  [BUTTON, small, secondary:] "Jump to costs"
  (Smooth-scrolls to cost section)
```

### Difference 2: Reaction / Feedback Strip

Below the hero, above the itinerary:

```
[Card, white, centered text]
  "What do you think?"

  [Emoji reaction buttons, large, spaced:]
  [thumbs up] [fire] [thinking face] [eyes] [x mark]

  (Tapping stores reaction in backend, shows:
   "Sarah reacted [fire], Alex reacted [thumbs up]"
   visible to all viewers of this trip URL)
```

This is lightweight group coordination. Not a full collaboration tool -- just enough for the organiser to gauge sentiment before booking.

### Difference 3: Individual Cost Calculator

Below the cost section, add:

```
[Card, white, border: 1px solid #febb02]

  H3: "What will this cost YOU?"

  "Where are you flying from?"
  [Chip selector:] [London (selected)] [Athens] [Other]

  "Sharing accommodation with:"
  [Chip selector:] [A partner] [Solo room] [Sharing with group]

  [CALCULATED RESULT:]
  "Your estimated cost: EUR850 -- 1,200"

  (Dynamically adjusts based on selections:
   London adds flights, Athens doesn't.
   Solo room doubles accommodation.
   Group sharing divides by group size.)
```

### Interactions Available to Recipients

1. **Browse full itinerary** -- read-only, same as organiser sees
2. **React** with emoji -- stored server-side, visible to all
3. **Use personal cost calculator** -- dynamic, client-side only
4. **Tick checklist items** -- synced via localStorage (per-device)
5. **Click booking links** -- opens external sites directly
6. **Share further** -- via the sticky bar button (now says "Share plan")

### What Recipients CANNOT Do

- Edit the itinerary (no confusion about "whose version is right")
- Change dates, islands, or group composition
- Create a competing plan from this page

If a recipient wants to modify the plan, the page footer says:
```
"Want to explore different islands or dates?
 Build your own plan at tripforge.app"
```

---

## 10. State Management & Transitions

### URL Routing (Hash-based, single page)

```
tripforge.app/              -> Landing (Screen 1)
tripforge.app/#confirm      -> Confirmation (Screen 3)
tripforge.app/#researching  -> Loading (Screen 4)
tripforge.app/trip/{id}     -> Results (Screen 5/7)
```

### Client-Side State

Minimal JS state, stored in a single object:

```javascript
const state = {
  phase: 'landing',       // landing | confirming | researching | ready
  brief: '',              // raw text input
  spec: null,             // TripSpecification (from extraction)
  researchSteps: [],      // array of { id, label, status, result }
  itinerary: null,        // final Itinerary object
  tripId: null,           // server-assigned ID for sharing
};
```

### Transitions

```
landing --> confirming
  Trigger: "Build my trip plan" button
  Action:  POST /api/extract with brief text
  Duration: 2-5 seconds
  Animation: Button spinner, then card transition

confirming --> researching
  Trigger: "Research flights, ferries & stays" button
  Action:  POST /api/research with confirmed spec
  Duration: 30-60 seconds
  Animation: Progress bar fills, research feed appears

researching --> ready
  Trigger: All research steps complete
  Action:  GET /api/trip/{id} for final itinerary
  Duration: 1-3 seconds (synthesis)
  Animation: Feed fades out, itinerary fades in

ready --> sharing
  Trigger: "Share with group" button
  Action:  Client-side share sheet
  Duration: Instant
  Animation: Modal or native share sheet
```

### Server Communication

The research phase uses Server-Sent Events (SSE) rather than polling:

```
POST /api/research
  Body: { spec: TripSpecification }
  Response: SSE stream

  event: step
  data: {"id": "flights_lon_ath", "status": "searching", "label": "London to Athens flights"}

  event: step
  data: {"id": "flights_lon_ath", "status": "done", "label": "London to Athens flights", "summary": "12 options, cheapest GBP85"}

  event: step
  data: {"id": "flights_ath_mlo", "status": "searching", ...}

  ...

  event: complete
  data: {"trip_id": "abc123", "itinerary_url": "/trip/abc123"}
```

This gives us real-time updates for the research feed without WebSockets.

### Progressive Enhancement

The entire flow works without JavaScript for the final itinerary page:
- The `/trip/{id}` URL serves complete server-rendered HTML
- Checklist uses `<details>` and `<summary>` for expand/collapse
- Cost tabs use anchor links as fallback
- Share button falls back to "Copy this URL" text

JavaScript enhances:
- Chat-style input and extraction
- Animated loading feed
- Smooth transitions between screens
- localStorage for checklist state
- `navigator.share()` for mobile sharing

---

## 11. Implementation Notes

### What to Build First (MVP)

The screens have clear priority ordering:

**Phase 1: Shareable Itinerary (Screen 5)**
- Port the existing dark Jinja2 template to light Booking-style
- Add og:meta tags for WhatsApp preview
- Deploy to a public URL with unique trip IDs
- Add WhatsApp share button with prefilled message
- This alone makes the current CLI tool 10x more useful

**Phase 2: Loading Experience (Screen 4)**
- Add SSE endpoint for research progress
- Build the animated research feed
- Add urgency interstitials (these are static content, cheap to build)

**Phase 3: Input + Confirmation (Screens 1, 2, 3)**
- Build the landing page with free-text input
- Wire up Claude extraction to /api/extract
- Build the confirmation/edit screen
- This completes the end-to-end web flow

**Phase 4: Recipient Features (Screen 7)**
- Emoji reactions (requires server-side storage)
- Personal cost calculator (client-side only)
- Recipient banner

### File Changes Required

The existing codebase needs these modifications:

1. **`/Users/gerinicka-new/holiday-planner/templates/itinerary.html.j2`** -- Rewrite for light theme, Booking-style design system, og:meta tags, share functionality

2. **`/Users/gerinicka-new/holiday-planner/output/share.py`** -- Add real URL generation (not file://), WhatsApp message builder, og:image generation

3. **New: `templates/app.html`** -- Single-page app shell (landing + confirm + loading + results)

4. **New: `web/app.py`** -- FastAPI/Starlette web server with routes:
   - `GET /` -- serves landing page
   - `POST /api/extract` -- free-text to TripSpecification
   - `POST /api/research` -- SSE stream of research progress
   - `GET /trip/{id}` -- serves rendered itinerary
   - `GET /api/og-image/{id}` -- generates og:image

5. **`/Users/gerinicka-new/holiday-planner/agents/orchestrator.py`** -- Add progress callback support for SSE streaming of research steps

6. **`/Users/gerinicka-new/holiday-planner/models/trip.py`** -- Add `trip_id` field to Itinerary, add reaction model

### OG Image Generation

For WhatsApp previews, generate a 1200x630 image server-side:

```python
# Using Pillow or satori-like approach
def generate_og_image(itinerary: Itinerary) -> bytes:
    """Generate a 1200x630 OG image for WhatsApp preview."""
    # Blue gradient background
    # White text: title, subtitle
    # Route pills in a row
    # Price range, large
    # TripForge watermark
    pass
```

Alternatively, use an HTML-to-image service or pre-render with Playwright.

### Performance Budget

- Landing page: < 50KB HTML + CSS (no external JS frameworks)
- Itinerary page: < 100KB HTML + CSS (all inline, single file)
- Time to first paint: < 1 second
- Time to interactive: < 2 seconds
- No framework. Vanilla JS. The CSS is already more powerful than most frameworks for this layout.

### Analytics Events to Track

```
page_view:landing
input_started           (user begins typing)
input_chip_used         (user tapped a quick-start chip)
extraction_started
extraction_complete
extraction_clarification_needed
confirmation_edit       (user edited a field)
confirmation_island_added
confirmation_island_removed
research_started
research_tab_away       (user left during research)
research_tab_return
research_complete
itinerary_viewed
itinerary_scroll_depth  (25%, 50%, 75%, 100%)
share_button_clicked
share_completed         (confirmed share via navigator.share)
share_link_copied
share_whatsapp          (detected WhatsApp as share target)
recipient_page_view     (no localStorage flag = new visitor)
recipient_reaction
recipient_cost_calculator_used
booking_link_clicked    (with destination: airbnb/booking/skyscanner/etc)
checklist_item_toggled
```

---

## Appendix: Key Copy Decisions

### Tone of Voice

TripForge speaks like a well-traveled friend who happens to be organized. Not a travel agent. Not a chatbot. Not a brand with a personality deck.

Good: "Only ~20 places to stay on the entire island."
Bad:  "This destination has limited accommodation options!"

Good: "Tiny 70-seat turboprops. Sells out months ahead."
Bad:  "Book early to avoid disappointment!"

Good: "August 15 is Assumption of Mary -- big Greek holiday."
Bad:  "Please note that Greek national holidays may affect availability."

### Microcopy Inventory

| Location | Copy |
|----------|------|
| Landing H1 | "Plan your Greek Islands trip in 60 seconds" |
| Landing subhead | "Tell us where you're going, who's coming, and when. We'll research flights, ferries, and places to stay -- and build a plan you can share with your group." |
| Input placeholder | "e.g. 3 couples from London and Athens, going to Milos and Koufonisia, August 14-21, mid-range budget" |
| CTA button | "Build my trip plan" |
| Below CTA | "Takes about 60 seconds. Free, no signup required." |
| Extraction loading | "Understanding your trip..." |
| Confirm H2 | "Here's what we understood" |
| Confirm subhead | "Check these details before we research prices." |
| Confirm CTA | "Research flights, ferries & stays" |
| Below confirm CTA | "This takes about 60 seconds. We'll search Skyscanner, Ferryhopper, Booking.com, and more." |
| Research complete | "Your trip plan is ready" |
| Share button | "Share with group" |
| Share modal H3 | "Share your trip plan" |
| WhatsApp prefill | "[Title]\n[Group] | [Dates] | ~[Cost]pp\n\nI've researched flights, ferries, and places to stay. Have a look and tell me what you think:\n[URL]" |
| Recipient banner | "[Someone] shared this trip plan with you." |
| Recipient CTA | "Jump to costs" |
| Footer | "Prices are estimates based on current availability. Check booking links for live prices." |
| Empty state (research slow) | "This is taking a bit longer than usual. Complex routes need extra research time." |

---

*End of design document. This specification should be sufficient to implement the complete TripForge web experience without additional design input. Build Phase 1 first -- the shareable itinerary page is the atomic unit of value.*
