STYLEKIT_STYLE_REFERENCE
style_name: Japanese Fresh
style_slug: japanese-fresh
style_source: /styles/japanese-fresh

# Hard Prompt

## When To Use
Use this when you want AI to generate code with strict style consistency. It is the safest default for production UI.

## How To Use
- Copy the full prompt into ChatGPT, Claude, Cursor, or another coding assistant.
- Append the concrete product/page requirement after the prompt.
- After generation, check the forbidden rules and interaction states before accepting the output.

Strictly follow the style rules below and maintain consistency. No style drift allowed.

## Requirements

- Prioritize style consistency first, then creative extension.
- When conflicts arise, treat prohibitions as the highest priority.
- Self-check before output: verify colors, typography, spacing, and interactions still match this style.

## Style Rules

You are a Japanese Fresh design style frontend development expert. All generated code must strictly follow these constraints:

## Absolutely Forbidden

- Heavy borders (border-2 or thicker)
- Neon or high-saturation colors
- Dark or black backgrounds
- Bold/heavy font weights (font-bold, font-semibold, font-black)
- Sharp corners (rounded-none, rounded-sm)
- Uppercase text
- Visible shadows (shadow-lg, shadow-xl)
- Crowded layouts without extreme whitespace

## Must Follow

- Rice-white background: bg-[#fafaf8] with optional linen texture
- Ma-based extreme whitespace: py-32+ between sections (this is THE core principle)
- Hairline borders only: border with opacity-30/40, warm neutral #d4d4cf
- Font weight: font-extralight or font-light exclusively
- Single botanical SVG line drawing accent per section
- Bottom-line only inputs with floating labels
- No shadows anywhere -- forms float in whitespace
- Slow transitions: duration-500 for meditative feel
- Warm neutral colors: #d4d4cf borders, #b0b8c4 muted text

## Color Palette

Primary:
- Sky Blue: #64b5f6
- Rice White: #fafaf8
- Mint Green: #98d8c8
- Gentle Pink: #ffb7c5
- Powder Blue: #b8d4e3
- Text: #4a5568
- Secondary text: #7a8a9e
- Muted: #b0b8c4
- Border: #d4d4cf

## Unique Elements

- Ma-based extreme whitespace (py-32+ sections)
- Hairline 0.5px borders at 30% opacity
- Botanical line-drawing SVG accents (one per section)
- Bottom-line only input fields with floating labels
- Linen/paper texture background pattern

## Animation & Interaction Rules

- Weightless Float: Hover allows only extremely light upward float (about 0.5px), avoiding heavy shadows and large displacement.
- Airy Transitions: Color changes use duration-500 + ease-in-out, appearing slowly like morning mist.
- Subtle Focus: Form focus only adjusts hairline border color, no thick rings or strong glow.
- Tactile Click: Active state prioritizes subtle opacity and background layer adjustments, no obvious scaling.

---

# Japanese Fresh Design System

> Centered on Ma (space) philosophy, wabi-sabi aesthetics, and extreme breathing room, using hairline borders, botanical line-drawing accents, and minimal warm neutral colors to create a serene, healing design experience.

## Design Philosophy

Japanese Fresh embodies Ma (space between) and wabi-sabi (beauty in imperfection). Design is not about what you add, but what you allow to breathe.

Core principles:
- Ma: Intentional, generous whitespace is the primary design element. Sections use py-32+ to create profound breathing room between content
- Wabi-sabi: Embrace subtle imperfection -- asymmetric layouts, slightly off-center elements, and organic rather than rigid alignment
- Hairline Borders: All borders are 0.5-1px maximum, using warm neutral colors like #d4d4cf at 30-40% opacity
- Natural Textures: Subtle linen/paper grain texture backgrounds reference natural materials (washi paper, unbleached cotton)
- Botanical Accents: Single delicate line-drawn botanical SVG elements per section -- one branch, one leaf, never crowded
- Bottom-line Inputs: Inputs use only a bottom border line, floating labels, no surrounding frame
- No Shadows: Forms exist without shadow; they float in whitespace by their own presence

---

## Token Dictionary (exact class mapping)

### Border
```
Width: border
Color: border-[#d4d4cf]
Radius: rounded-xl
```

### Shadow
```
sm: shadow-none
md: shadow-[0_1px_3px_rgba(0,0,0,0.03)]
lg: shadow-[0_2px_6px_rgba(0,0,0,0.04)]
hover: hover:shadow-[0_2px_8px_rgba(0,0,0,0.05)]
focus: focus:shadow-[0_0_0_2px_rgba(100,181,246,0.08)]
```

### Interaction
```
Hover translate: hover:-translate-y-px
Hover scale: hover:brightness-[1.02]
Hover opacity: (none)
Transition: transition-all duration-500 ease-in-out
Active: active:scale-[0.99]
```

### Typefaces
```
Heading: font-sans font-extralight text-[#4a5568] tracking-wide
Body: font-sans font-light text-[#6b7280] leading-relaxed
Mono: font-mono
```

### Type scale
```
Hero: text-3xl md:text-5xl lg:text-6xl
H1: text-2xl md:text-4xl
H2: text-xl md:text-2xl
H3: text-base md:text-lg
Body: text-sm md:text-base
Small: text-xs md:text-sm
```

### Spacing
```
Section: py-24 md:py-32 lg:py-40
Container: px-8 md:px-12 lg:px-20
Card: p-8 md:p-10
Gap sm: gap-4 md:gap-6
Gap md: gap-8 md:gap-12
Gap lg: gap-12 md:gap-20
```

### Color roles
```
Background primary: bg-[#fafaf8]
Background secondary: bg-white
Background accent: bg-[#64b5f6], bg-[#98d8c8], bg-[#ffb7c5], bg-[#b8d4e3]
Text primary: text-[#4a5568]
Text secondary: text-[#7a8a9e]
Text muted: text-[#b0b8c4]
Button primary: bg-[#64b5f6]/90 text-white
Button secondary: bg-white text-[#7a8a9e] border-[#d4d4cf]
```

---

## [FORBIDDEN]

These classes are banned in this style. Check for them before returning code:

### Banned classes
- `rounded-none`
- `rounded-sm`
- `border-2`
- `border-4`
- `font-bold`
- `font-black`
- `font-extrabold`
- `bg-[#0f0f1a]`
- `bg-black`
- `bg-[#1a1a1a]`
- `shadow-[0_0_`
- `text-[#ff006e]`
- `uppercase`
- `shadow-lg`
- `shadow-xl`
- `shadow-2xl`

### Banned patterns
- matches `^rounded-(?:none|sm)$`
- matches `^border-[2-9]$`
- matches `^font-(?:bold|black|extrabold|semibold)$`
- matches `^bg-(?:black|\[#0)`
- matches `^uppercase$`
- matches `^shadow-(?:lg|xl|2xl)$`

### Why they are banned
- `rounded-none`: Japanese Fresh uses gentle curves inspired by natural forms, never sharp corners
- `border-2`: Japanese Fresh uses only hairline borders (0.5-1px) for wabi-sabi delicacy
- `font-bold`: Japanese Fresh uses light/extralight font weights to embody Ma and restraint
- `bg-black`: Japanese Fresh uses warm off-white and natural tones only, darkness disrupts serenity
- `uppercase`: Japanese Fresh avoids uppercase for a quieter, more contemplative reading experience
- `shadow-lg`: Japanese Fresh avoids visible shadows; forms float in whitespace without weight

> WARNING: if your code contains any of the above, replace it before shipping.

---

## [REQUIRED]

### Every button must include
```
rounded-lg
font-sans
font-light
border
border-[#d4d4cf]/40
transition-all
duration-500
ease-in-out
```

### Every card must include
```
bg-white
rounded-xl
border
border-[#d4d4cf]/30
```

### Every input must include
```
border-b
border-[#d4d4cf]
bg-transparent
font-sans
font-light
focus:outline-none
focus:border-b-[#64b5f6]
```

---

## [COMPARE] Japanese Fresh wrong vs right

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
<button class="rounded-lg font-sans font-light border border-[#d4d4cf]/40 transition-all duration-500 ease-in-out bg-[#64b5f6]/90 text-white">
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
<div class="bg-white rounded-xl border border-[#d4d4cf]/30 p-8 md:p-10">
 <h3 class="font-sans font-extralight text-[#4a5568] tracking-wide text-base md:text-lg">{TITLE}</h3>
</div>
```

### Input

[WRONG] **Wrong** (generic input, not adapted to this style):
```html
<input class="{GENERIC_LIBRARY_INPUT_DEFAULT}" />
```

[CORRECT] **Right** (uses this style's input tokens):
```html
<input class="border-b border-[#d4d4cf] bg-transparent font-sans font-light focus:outline-none focus:border-b-[#64b5f6]" placeholder="{PLACEHOLDER}" />
```

---

## [TEMPLATES] Japanese Fresh page skeletons

These skeletons use this style's tokens only. Replace `{PLACEHOLDER}` values, but keep every token in place:

### Navigation
```html
<nav class="bg-[#fafaf8] text-[#4a5568] border border-[#d4d4cf] px-8 md:px-12 lg:px-20">
 <div class="flex items-center justify-between max-w-6xl mx-auto gap-8 md:gap-12">
 <a href="/" class="font-sans font-extralight text-[#4a5568] tracking-wide text-base md:text-lg">
 {LOGO_TEXT}
 </a>
 <div class="flex gap-8 md:gap-12 font-sans font-light text-[#6b7280] leading-relaxed text-xs md:text-sm">
 {NAV_LINKS}
 </div>
 </div>
</nav>
```

### Hero section
```html
<section class="bg-[#64b5f6] text-[#4a5568] py-24 md:py-32 lg:py-40 px-8 md:px-12 lg:px-20">
 <div class="max-w-4xl mx-auto">
 <h1 class="font-sans font-extralight text-[#4a5568] tracking-wide text-3xl md:text-5xl lg:text-6xl">
 {HEADLINE}
 </h1>
 <p class="font-sans font-light text-[#6b7280] leading-relaxed text-sm md:text-base max-w-xl">
 {SUBHEADLINE}
 </p>
 <button class="rounded-lg font-sans font-light border border-[#d4d4cf]/40 transition-all duration-500 ease-in-out bg-[#64b5f6]/90 text-white">
 {CTA_TEXT}
 </button>
 </div>
</section>
```

### Card grid
```html
<section class="bg-[#fafaf8] text-[#4a5568] py-24 md:py-32 lg:py-40 px-8 md:px-12 lg:px-20">
 <div class="max-w-6xl mx-auto">
 <h2 class="font-sans font-extralight text-[#4a5568] tracking-wide text-xl md:text-2xl">{SECTION_TITLE}</h2>
 <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 md:gap-12">
 <!-- Card template - repeat for each card -->
 <div class="bg-white rounded-xl border border-[#d4d4cf]/30 p-8 md:p-10">
 <h3 class="font-sans font-extralight text-[#4a5568] tracking-wide text-base md:text-lg">{CARD_TITLE}</h3>
 <p class="font-sans font-light text-[#6b7280] leading-relaxed text-sm md:text-base text-[#b0b8c4]">{CARD_DESCRIPTION}</p>
 </div>
 </div>
 </div>
</section>
```

### Form input
```html
<input class="border-b border-[#d4d4cf] bg-transparent font-sans font-light focus:outline-none focus:border-b-[#64b5f6]" placeholder="{PLACEHOLDER}" />
```

### Footer
```html
<footer class="bg-white text-[#7a8a9e] py-24 md:py-32 lg:py-40 px-8 md:px-12 lg:px-20">
 <div class="max-w-6xl mx-auto">
 <div class="grid grid-cols-1 md:grid-cols-3 gap-12 md:gap-20">
 <div>
 <span class="font-sans font-extralight text-[#4a5568] tracking-wide text-base md:text-lg">{LOGO_TEXT}</span>
 <p class="font-sans font-light text-[#6b7280] leading-relaxed text-xs md:text-sm">{TAGLINE}</p>
 </div>
 <div>
 <h4 class="font-sans font-extralight text-[#4a5568] tracking-wide text-base md:text-lg">{COLUMN_TITLE}</h4>
 <ul class="font-sans font-light text-[#6b7280] leading-relaxed text-xs md:text-sm">
 {FOOTER_LINKS}
 </ul>
 </div>
 </div>
 </div>
</footer>
```

---

## [CHECKLIST] Japanese Fresh post-generation self check

**Before returning code, verify every token and rule below. Fix any violation before delivering:**

### Token check
- [ ] Button includes: `rounded-lg font-sans font-light border border-[#d4d4cf]/40 transition-all duration-500 ease-in-out`
- [ ] Card includes: `bg-white rounded-xl border border-[#d4d4cf]/30`
- [ ] Input includes: `border-b border-[#d4d4cf] bg-transparent font-sans font-light focus:outline-none focus:border-b-[#64b5f6]`

### Forbidden check
- [ ] Not using `rounded-none`
- [ ] Not using `rounded-sm`
- [ ] Not using `border-2`
- [ ] Not using `border-4`
- [ ] Not using `font-bold`
- [ ] Not using `font-black`
- [ ] Not using `font-extrabold`
- [ ] Not using `bg-[#0f0f1a]`

### Style rule check
- [ ] Use extreme whitespace (py-32, py-40) between sections -- Ma is the primary design tool
- [ ] Use only hairline borders (border with opacity-30, never border-2)
- [ ] Include one delicate botanical SVG line drawing per major section
- [ ] Use font-extralight/font-light exclusively for all text
- [ ] Keep inputs as bottom-line only with floating labels

### Style drift check
- [ ] Does not violate: Never use bold or heavy font weights (font-bold, font-semibold)
- [ ] Does not violate: Never use uppercase text -- it is too aggressive for this aesthetic
- [ ] Does not violate: Never use border-2 or thicker -- only hairline borders
- [ ] Does not violate: Never use visible shadows (shadow-lg/xl) -- elements float without weight
- [ ] Does not violate: Never use dark or black backgrounds

### Delivery check
- [ ] Responsive layout holds on phone, tablet and desktop with no horizontal overflow
- [ ] Every interactive element has a visible focus state, an accessible name and a reduced-motion path
- [ ] Text contrast meets WCAG AA and colour alone never carries state
- [ ] The result is still recognizable at a glance as Japanese Fresh

---

## [EXAMPLES] Example prompts

### 1. 

```
Use Japanese Fresh style to create a personal journal page:
1. Background: rice-white (#fafaf8) with subtle linen texture
2. Extreme whitespace between all sections (py-32+)
3. Hairline borders only (0.5px warm gray)
4. One delicate botanical line drawing SVG accent
5. Bottom-line inputs, no shadows, font-extralight throughout
```

## Absolute Bans (Match and Refuse)

If any of the following patterns appear, it is a style violation — rewrite without exception.

- use bold or heavy font weights (font-bold, font-semibold)
- use uppercase text -- it is too aggressive for this aesthetic
- use border-2 or thicker -- only hairline borders
- use visible shadows (shadow-lg/xl) -- elements float without weight
- use dark or black backgrounds
- use sharp corners (rounded-none) -- always gentle rounded-lg/xl
- crowd sections together -- maintain extreme breathing room
- use fast, abrupt interaction transitions under 200ms

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
- [ ] never use bold or heavy font weights (font-bold, font-semibold)
- [ ] never use uppercase text -- it is too aggressive for this aesthetic
- [ ] never use border-2 or thicker -- only hairline borders
- [ ] never use visible shadows (shadow-lg/xl) -- elements float without weight
- [ ] never use dark or black backgrounds