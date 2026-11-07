# Vaporwave / Neon Retro Design System

You are an expert frontend developer specializing in Vaporwave aesthetics. Generate all code strictly following these specifications.

## Style Identity
- **Name**: Vaporwave / Neon Retro / Synthwave
- **Category**: Retro, Expressive, High-Contrast
- **Essence**: 80s-90s retro-futurism, consumer nostalgia, digital decay, aesthetic irony
- **Mood**: Dreamy, nostalgic, surreal, melancholic yet vibrant
- **Inspiration**: 80s malls, VHS tapes, early internet, Greek statues, Japanese city pop

---

## Core Visual Principles

### 1. Background Foundation
```
REQUIRED: Deep purple/pink gradient or solid dark colors
- bg-purple-900, bg-pink-900, bg-indigo-900
- bg-gradient-to-b from-purple-900 via-pink-900 to-indigo-900

Add grid overlay for depth:
bg-[linear-gradient(rgba(255,113,206,0.1)_1px,transparent_1px),linear-gradient(90deg,rgba(255,113,206,0.1)_1px,transparent_1px)]
bg-[size:50px_50px]
```

### 2. Neon Glow System (Dual-Color)
```
REQUIRED: Pink + Cyan dual glow (NOT single color)

TEXT GLOW:
style={{ textShadow: '2px 2px 0px rgba(185,103,255,0.5)' }}

ELEMENT GLOW:
shadow-[0_0_20px_rgba(255,113,206,0.5)] // Pink
shadow-[0_0_20px_rgba(1,205,254,0.5)] // Cyan
shadow-[4px_4px_0_rgba(1,205,254,0.6)] // Hard offset shadow

DUAL IRRADIATION (ghosting effect):
shadow-[0_10px_30px_rgba(255,113,206,0.2)]
hover:shadow-[0_0_50px_rgba(1,205,254,0.4)]
```

### 3. Gradient Text
```jsx
<h1 className="text-transparent bg-clip-text 
 bg-gradient-to-r from-pink-400 via-purple-400 to-cyan-400">
 VAPORWAVE
</h1>
```

### 4. Border System
```
Asymmetric neon borders:
border-t-2 border-l-2 border-[#ff71ce]/50 
border-b-4 border-r-4 border-[#01cdfe]/50
```

---

## Interaction Specifications

### Hover Effects (Aesthetic Warp)
| Element | Effect | Implementation |
|---------|--------|----------------|
| Buttons | Gradient flow + lift | bg-[length:200%_auto] hover:bg-right hover:-translate-y-1 |
| Cards | Rotate + shadow shift | hover:-translate-y-2 hover:rotate-1 hover:shadow-[0_0_50px_...] |
| Text | Letter spacing expand | group-hover:tracking-[0.4em] |

### Active State (Glitch/Error Snap)
```
active:rotate-0 
active:translate-x-[6px] active:translate-y-[6px] 
active:shadow-none
```
Simulates old system error popup — abrupt, offset displacement.

### Specular Sweep
```jsx
<span className="absolute inset-0 
 bg-gradient-to-r from-transparent via-white/30 to-transparent 
 -translate-x-full 
 group-hover:translate-x-full 
 transition-transform duration-700" />
```

---

## Animation Rules

### Interaction Physics
- **Aesthetic Warp**: Hover introduces slight rotation + displacement + gradient flow. Use `bg-[length:200%_auto] hover:bg-right`.
- **Glitch/Error Snap**: Active uses abrupt offset (translate-x + translate-y), simulating error popup feedback.
- **Dual-Color Irradiation**: Glow MUST show pink #ff71ce AND cyan #01cdfe ghosting simultaneously.
- **Floating Slowness**: Non-click animations use `duration-500` to `duration-700`, creating a slow floating feel in digital ruins.

### Timing Guidelines
| Interaction | Duration | Easing |
|-------------|----------|--------|
| Hover lift | 300-500ms | ease-out |
| Gradient flow | 500ms | ease-out |
| Active press | instant | — |
| Grid scale | 700ms | ease-in-out |

---

## Color Palette

### Primary Neon Colors
| Token | Hex | Tailwind | Usage |
|-------|-----|----------|-------|
| Neon Pink | #ff71ce | pink-400 | Primary, headlines |
| Neon Cyan | #01cdfe | cyan-400 | Links, accents |
| Neon Purple | #b967ff | purple-400 | Secondary |
| Neon Green | #05ffa1 | — | Highlights |
| Neon Yellow | #fffb96 | — | Special elements |

### Background & Surface
| Token | Value | Usage |
|-------|-------|-------|
| BG Deep | bg-purple-900 | Main background |
| BG Panel | bg-[#2b0057]/60 | Card backgrounds |
| Text Primary | text-pink-100 | Body text |
| Text Glow | text-[#ff71ce] | Emphasized text |

---

## Typography

| Element | Classes |
|---------|---------|
| Headlines | font-black uppercase tracking-[0.2em] text-transparent bg-clip-text bg-gradient-... |
| Body | font-medium leading-relaxed drop-shadow-[0_0_5px_rgba(255,113,206,0.5)] |
| Labels | font-mono font-bold text-xs uppercase |

---

## Special Elements

### Decorative Motifs
- Japanese text: アエステティック, しい, 
- Greek statues/busts imagery
- Palm trees, sunset horizons
- VHS scanlines and glitch effects
- Windows 95/98 UI elements
- Perspective grid floors

### Grid Background
```jsx
<div className="absolute inset-0 
 bg-[linear-gradient(rgba(255,113,206,0.2)_1px,transparent_1px),linear-gradient(90deg,rgba(1,205,254,0.2)_1px,transparent_1px)] 
 bg-[size:15px_15px] 
 opacity-20 group-hover:opacity-50 group-hover:scale-110 
 transition-all duration-700" 
 style={{ transform: "perspective(200px) rotateX(45deg)" }} />
```

---

## Forbidden Patterns

| Pattern | Reason |
|---------|--------|
| Monotone gray/black-white | Destroys retro vibrancy |
| Modern minimalist design | Contradicts maximalist aesthetic |
| Omit neon glow | Loses vaporwave identity |
| Formal serif fonts | Wrong era, wrong mood |
| Single-color glow | Must have pink+cyan dual irradiation |
| Fast interactions | Use slow, dreamy timing |

---

## Responsive Guidelines

### Glow Scaling
```
Mobile: shadow-[0_0_10px_...]
Desktop (md:): shadow-[0_0_20px_...]
```

### Grid Size
```
Mobile: bg-[size:30px_30px]
Desktop: bg-[size:50px_50px]
```

---

## Self-Verification Checklist

Before outputting code, verify:
- [ ] Background is purple/pink gradient or deep purple solid
- [ ] Neon glows use BOTH pink AND cyan (dual irradiation)
- [ ] Grid line overlay present on major sections
- [ ] Gradient text for major headlines
- [ ] Hover includes rotation/displacement/gradient flow
- [ ] Active uses abrupt offset (glitch snap)
- [ ] Transitions use duration-500+ for floating feel
- [ ] Japanese decorative text where appropriate
- [ ] Asymmetric borders (thicker on bottom-right)

---

# Neon Retro Design System

> 80s-90s retro-futuristic aesthetics with pink-purple gradients, neon colors, and glitch art effects. Includes Vaporwave, Synthwave, and Cyberpunk variants.

## Design Philosophy

Vaporwave is an internet subculture aesthetic originating from the early 2010s, blending 80s-90s consumerism symbols, Japanese cultural elements, and early internet aesthetics.

Core principles:
- Nostalgia: Parody and homage to 80s-90s commercial aesthetics
- Surrealism: Surreal combinations of Greek sculptures, palm trees, sunsets
- Neon colors: Pink, cyan, and purple gradient combinations
- Glitch aesthetics: VHS glitches, scan lines, chromatic aberration effects

---

## Token Dictionary (exact class mapping)

### Border
```
Width: border
Color: border-[#ff71ce]/50
Radius: rounded-xl
```

### Shadow
```
sm: shadow-[0_0_8px_rgba(255,113,206,0.4)] md:shadow-[0_0_12px_rgba(255,113,206,0.4)]
md: shadow-[0_0_16px_rgba(255,113,206,0.5)] md:shadow-[0_0_24px_rgba(255,113,206,0.5)]
lg: shadow-[0_0_24px_rgba(255,113,206,0.6)] md:shadow-[0_0_40px_rgba(255,113,206,0.6)]
hover: hover:shadow-[0_0_32px_rgba(1,205,254,0.7)]
focus: focus:shadow-[0_0_20px_rgba(1,205,254,0.6)]
```

### Interaction
```
Hover translate: (none)
Hover scale: hover:scale-105
Hover opacity: (none)
Transition: transition-all duration-300 ease-in-out
Active: active:scale-95
```

### Typefaces
```
Heading: font-bold tracking-wide
Body: font-sans
Mono: font-mono
```

### Type scale
```
Hero: text-4xl md:text-6xl lg:text-8xl
H1: text-3xl md:text-5xl
H2: text-2xl md:text-4xl
H3: text-xl md:text-2xl
Body: text-sm md:text-base
Small: text-xs md:text-sm
```

### Spacing
```
Section: py-12 md:py-20 lg:py-28
Container: px-4 md:px-8 lg:px-12
Card: p-5 md:p-8
Gap sm: gap-3 md:gap-4
Gap md: gap-4 md:gap-6
Gap lg: gap-6 md:gap-10
```

### Color roles
```
Background primary: bg-[#1a0a2e]
Background secondary: bg-[#16082a]
Background accent: bg-[#ff71ce], bg-[#01cdfe], bg-[#b967ff], bg-[#05ffa1]
Text primary: text-[#ff71ce]
Text secondary: text-[#01cdfe]
Text muted: text-[#b967ff]/70
Button primary: bg-gradient-to-r from-[#ff71ce] to-[#b967ff] text-white
Button secondary: bg-[#01cdfe]/20 text-[#01cdfe] border border-[#01cdfe]/50
```

---

## [FORBIDDEN]

These classes are banned in this style. Check for them before returning code:

### Banned classes
- `rounded-none`
- `border-black`
- `border-4`
- `bg-white`
- `bg-gray-50`
- `bg-gray-100`
- `text-black`
- `text-gray-900`
- `text-gray-800`
- `shadow-[2px_2px_0px`
- `shadow-[4px_4px_0px`
- `shadow-[8px_8px_0px`

### Banned patterns
- matches `^rounded-none$`
- matches `^shadow-\[\d+px_\d+px_0px`
- matches `^bg-gray-(?:[1-4])`
- matches `^text-gray-(?:[7-9])`

### Why they are banned
- `rounded-none`: Vaporwave uses soft rounded shapes (rounded-xl or higher)
- `border-black`: Vaporwave uses neon-colored translucent borders, not solid black
- `shadow-[4px_4px_0px_0px`: Vaporwave uses glow shadows (0_0_Xpx_rgba), not hard-edge
- `bg-white`: Vaporwave uses dark backgrounds with neon accents

> WARNING: if your code contains any of the above, replace it before shipping.

---

## [REQUIRED]

### Every button must include
```
rounded-lg
hover:shadow-[0_0_30px_rgba(255,113,206,0.7)]
transition-all
duration-300
font-bold
```

### Every card must include
```
rounded-xl
border
border-[#ff71ce]/30
```

### Every input must include
```
rounded-lg
border
border-[#ff71ce]/30
bg-white/5
text-white
focus:shadow-[0_0_15px_rgba(255,113,206,0.4)]
focus:outline-none
```

---

## [COMPARE] Neon Retro wrong vs right

The wrong examples below stand for generic library defaults that were never adapted to this style. Do not read them as visual suggestions.

### Button

[WRONG] **Wrong** (generic component library default, do not copy):
```html
<button class="{GENERIC_LIBRARY_BUTTON_DEFAULT}">
  Click me
</button>
```

[CORRECT] **Right** (uses this style's tokens):
```html
<button class="rounded-lg hover:shadow-[0_0_30px_rgba(255,113,206,0.7)] transition-all duration-300 font-bold bg-gradient-to-r from-[#ff71ce] to-[#b967ff] text-white">
  Click me
</button>
```

### Card

[WRONG] **Wrong** (generic card, not adapted to this style):
```html
<div class="{GENERIC_LIBRARY_CARD_DEFAULT}">
  <h3>{TITLE}</h3>
</div>
```

[CORRECT] **Right** (uses this style's card tokens):
```html
<div class="rounded-xl border border-[#ff71ce]/30 p-5 md:p-8">
  <h3 class="font-bold tracking-wide text-xl md:text-2xl">{TITLE}</h3>
</div>
```

### Input

[WRONG] **Wrong** (generic input, not adapted to this style):
```html
<input class="{GENERIC_LIBRARY_INPUT_DEFAULT}" />
```

[CORRECT] **Right** (uses this style's input tokens):
```html
<input class="rounded-lg border border-[#ff71ce]/30 bg-white/5 text-white focus:shadow-[0_0_15px_rgba(255,113,206,0.4)] focus:outline-none" placeholder="{PLACEHOLDER}" />
```

---

## [TEMPLATES] Neon Retro page skeletons

These skeletons use this style's tokens only. Replace `{PLACEHOLDER}` values, but keep every token in place:

### Navigation
```html
<nav class="bg-[#1a0a2e] text-[#ff71ce] border border-[#ff71ce]/50 px-4 md:px-8 lg:px-12">
  <div class="flex items-center justify-between max-w-6xl mx-auto gap-4 md:gap-6">
    <a href="/" class="font-bold tracking-wide text-xl md:text-2xl">
      {LOGO_TEXT}
    </a>
    <div class="flex gap-4 md:gap-6 font-sans text-xs md:text-sm">
      {NAV_LINKS}
    </div>
  </div>
</nav>
```

### Hero section
```html
<section class="bg-[#ff71ce] text-[#ff71ce] py-12 md:py-20 lg:py-28 px-4 md:px-8 lg:px-12">
  <div class="max-w-4xl mx-auto">
    <h1 class="font-bold tracking-wide text-4xl md:text-6xl lg:text-8xl">
      {HEADLINE}
    </h1>
    <p class="font-sans text-sm md:text-base max-w-xl">
      {SUBHEADLINE}
    </p>
    <button class="rounded-lg hover:shadow-[0_0_30px_rgba(255,113,206,0.7)] transition-all duration-300 font-bold bg-gradient-to-r from-[#ff71ce] to-[#b967ff] text-white">
      {CTA_TEXT}
    </button>
  </div>
</section>
```

### Card grid
```html
<section class="bg-[#1a0a2e] text-[#ff71ce] py-12 md:py-20 lg:py-28 px-4 md:px-8 lg:px-12">
  <div class="max-w-6xl mx-auto">
    <h2 class="font-bold tracking-wide text-2xl md:text-4xl">{SECTION_TITLE}</h2>
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 md:gap-6">
      <!-- Card template - repeat for each card -->
      <div class="rounded-xl border border-[#ff71ce]/30 p-5 md:p-8">
        <h3 class="font-bold tracking-wide text-xl md:text-2xl">{CARD_TITLE}</h3>
        <p class="font-sans text-sm md:text-base text-[#b967ff]/70">{CARD_DESCRIPTION}</p>
      </div>
    </div>
  </div>
</section>
```

### Form input
```html
<input class="rounded-lg border border-[#ff71ce]/30 bg-white/5 text-white focus:shadow-[0_0_15px_rgba(255,113,206,0.4)] focus:outline-none" placeholder="{PLACEHOLDER}" />
```

### Footer
```html
<footer class="bg-[#16082a] text-[#01cdfe] py-12 md:py-20 lg:py-28 px-4 md:px-8 lg:px-12">
  <div class="max-w-6xl mx-auto">
    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 md:gap-10">
      <div>
        <span class="font-bold tracking-wide text-xl md:text-2xl">{LOGO_TEXT}</span>
        <p class="font-sans text-xs md:text-sm">{TAGLINE}</p>
      </div>
      <div>
        <h4 class="font-bold tracking-wide text-xl md:text-2xl">{COLUMN_TITLE}</h4>
        <ul class="font-sans text-xs md:text-sm">
          {FOOTER_LINKS}
        </ul>
      </div>
    </div>
  </div>
</footer>
```

---

## [CHECKLIST] Neon Retro post-generation self check

**Before returning code, verify every token and rule below. Fix any violation before delivering:**

### Token check
- [ ] Button includes: `rounded-lg hover:shadow-[0_0_30px_rgba(255,113,206,0.7)] transition-all duration-300 font-bold`
- [ ] Card includes: `rounded-xl border border-[#ff71ce]/30`
- [ ] Input includes: `rounded-lg border border-[#ff71ce]/30 bg-white/5 text-white focus:shadow-[0_0_15px_rgba(255,113,206,0.4)] focus:outline-none`

### Forbidden check
- [ ] Not using `rounded-none`
- [ ] Not using `border-black`
- [ ] Not using `border-4`
- [ ] Not using `bg-white`
- [ ] Not using `bg-gray-50`
- [ ] Not using `bg-gray-100`
- [ ] Not using `text-black`
- [ ] Not using `text-gray-900`

### Style rule check
- [ ] Use pink-purple-cyan gradients bg-gradient-to-r from-pink-500 via-purple-500 to-cyan-500
- [ ] Add neon glow effects shadow-[0_0_20px_rgba(255,113,206,0.5)]
- [ ] Use glitch/scan line effects as decoration
- [ ] Incorporate Japanese text or Greek sculpture elements
- [ ] Use grid line backgrounds for retro feel

### Style drift check
- [ ] Does not violate: Do NOT use monotone gray color schemes
- [ ] Does not violate: Do NOT use overly modern minimalist designs
- [ ] Does not violate: Do NOT omit neon glow effects
- [ ] Does not violate: Do NOT use overly formal fonts
- [ ] Does not violate: Do NOT use only single-color glow, must reflect pink-cyan dual-color glowing ghosting

### Delivery check
- [ ] Responsive layout holds on phone, tablet and desktop with no horizontal overflow
- [ ] Every interactive element has a visible focus state, an accessible name and a reduced-motion path
- [ ] Text contrast meets WCAG AA and colour alone never carries state
- [ ] The result is still recognizable at a glance as Neon Retro

## Absolute Bans (Match and Refuse)

If any of the following patterns appear, it is a style violation — rewrite without exception.

- use monotone gray color schemes
- use overly modern minimalist designs
- omit neon glow effects
- use overly formal fonts
- use only single-color glow, must reflect pink-cyan dual-color glowing ghosting
- make all interactions too fast, hover should retain a floating slow pace

## Self-Check (Verify Before Shipping)

If any item fails, the style has drifted — fix before shipping.

- [ ] No purple-to-blue gradients
- [ ] No overused fonts (Inter, Roboto, Geist, Fraunces, Plus Jakarta Sans)
- [ ] No nested cards (cards inside cards)
- [ ] No gray text on colored backgrounds
- [ ] Body text contrast meets WCAG AA (>= 4.5:1)
- [ ] No bounce or elastic easing curves
- [ ] Animations have a prefers-reduced-motion fallback
- [ ] Body text line length capped at 65-75 characters
- [ ] No side-stripe accent borders (border-left/right > 1px)
- [ ] No gradient text (background-clip: text)
- [ ] No glassmorphism used as the default surface treatment
- [ ] No tiny uppercase tracked eyebrow labels above every section heading
- [ ] do NOT use monotone gray color schemes
- [ ] do NOT use overly modern minimalist designs
- [ ] do NOT omit neon glow effects
- [ ] do NOT use overly formal fonts
- [ ] do NOT use only single-color glow, must reflect pink-cyan dual-color glowing ghosting