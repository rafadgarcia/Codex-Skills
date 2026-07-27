# Visual Intensity and Motion

Use this reference when deciding how much visual polish, animation, component complexity, or dependency weight a UI deserves. The goal is not to make every interface quieter. The goal is to make each interface feel intentional for its job.

## Core Rule

Do not add visual effects by default. Add a visual or motion treatment only when it improves at least one of:

- comprehension
- interaction feedback
- orientation between states
- hierarchy
- narrative
- perceived quality
- brand expression

If none apply, keep the solution simpler.

## Surface Types

### Landing Page

Prioritize interest, conversion, and brand memory.

Appropriate polish:

- stronger hero composition
- entry animation
- restrained stagger
- section transitions
- visual storytelling
- occasional parallax or scroll reveal
- one dominant visual idea

Avoid making every section use a different effect.

### Institutional Site

Prioritize trust, clarity, and navigation.

Appropriate polish:

- strong typography
- high-quality images
- subtle transitions
- quiet microinteractions
- refined spacing and hierarchy

The page should feel professional before it feels technically impressive.

### Dashboard

Prioritize scanning, density, speed, and repeated use.

Appropriate polish:

- clear data hierarchy
- stable layouts
- state feedback
- subtle transitions for filters, panels, and loading
- microinteractions on controls

Avoid decorative scroll animations, parallax, heavy glow, glassmorphism, and motion that delays reading.

### Admin Or Operational Tool

Prioritize task completion and predictability.

Appropriate polish:

- visible focus states
- compact controls
- stable tables and forms
- clear success/error/loading states
- short transitions for context changes

Avoid visual treatments that make routine actions slower or less legible.

### SaaS Product

Separate marketing from app surfaces.

- Marketing pages can use richer storytelling and visual identity.
- The logged-in product should favor clarity, performance, consistency, and predictable workflows.

Do not automatically apply the landing page's visual language to the dashboard.

### Portfolio Or Brand Experience

Accept more creative risk when the experience itself is part of the value.

Possible tools:

- expressive motion
- unusual layout
- Canvas
- WebGL
- 3D
- scroll-driven storytelling

Still preserve accessibility, navigation, performance, and content comprehension.

## Intensity Scale

Visual intensity does not measure interaction sophistication. A Level 0 or Level 1 interface may still contain highly refined interaction design, keyboard behavior, state management, transitions, and feedback.

### Level 0: Utility

Use for dense admin, ERP, internal tools, operational forms, and repeated workflows.

- no decorative animation
- compact hierarchy
- stable surfaces
- clear states

### Level 1: Discreet

Good default for most product UIs.

- hover/focus/active feedback
- short transitions
- loading and status feedback
- minor elevation or color changes

### Level 2: Refined

Good for SaaS marketing, product pages, institutional pages, and polished user-facing tools.

- controlled section reveals
- light stagger
- more expressive hero
- purposeful imagery
- one or two distinctive visual gestures

### Level 3: Expressive

Good for launches, campaigns, portfolios, and special product pages.

- visual storytelling
- parallax used sparingly
- coordinated motion
- stronger art direction
- expressive typography or media

### Level 4: Experimental

Use only when the experience is itself the product or brand statement.

- WebGL
- shaders
- 3D
- custom navigation
- highly interactive scenes

Never choose this level only to make the page look impressive.

## Existing Design Consistency

Before introducing a new visual pattern, inspect the surrounding product.

Prefer extending an established visual language over creating an isolated new one. Check existing:

- spacing
- typography
- radius
- shadows
- color usage
- component patterns
- motion patterns
- density

When modifying an existing interface, do not treat the task as permission to redesign unrelated areas. Improve the requested surface while preserving established product conventions unless the user explicitly asks for broader visual exploration.

## Implementation Ladder

Prefer the simplest layer that solves the problem well:

```text
semantic HTML
CSS or Tailwind
native browser APIs
existing project components
primitives or shadcn/ui
Motion for React
specialized visual components
Canvas, WebGL, or 3D
```

This is an approximate complexity ladder, not a ranking of quality.

## Motion Guidance

Use CSS for simple hover, focus, opacity, color, and transform changes.

Consider native APIs such as View Transitions or scroll-driven animations when they solve continuity without a heavy runtime. Treat newer APIs as progressive enhancement.

Use Motion for React when React animation needs coordination:

```tsx
import { motion } from "motion/react"
```

Good reasons to use Motion:

- coordinated entrance or exit animations
- staggered related elements
- conditional presence
- layout animations
- gestures
- scroll-driven sequences
- shared transition patterns

Avoid adding Motion when CSS handles the interaction cleanly.

## Motion Budget

Treat user attention as limited.

Prefer a small number of coordinated animated moments over many independent animations. When several animated elements are visible at once, establish a clear primary motion and reduce secondary motion.

## Animation Properties

Prefer:

- `opacity`
- `transform`
- `scale`
- `translate`
- `rotate`

Avoid frequent animation of properties that trigger layout or heavy repaint.

Default motion should be short, predictable, and non-intrusive. Longer animation is not automatically more premium.

## Scroll, Stagger, And Parallax

Use scroll animation when it reveals or explains content. Avoid hiding essential information behind JavaScript-only reveals.

Use stagger for related groups such as cards, logos, steps, or metrics. Keep delays short enough that the user does not wait on each item.

Use parallax mainly for heroes, campaign imagery, and storytelling. Avoid it in dashboards, tables, forms, and critical navigation.

Always respect:

```css
prefers-reduced-motion
```

Essential meaning cannot depend only on animation.

## Component Libraries

Use shadcn/ui or similar primitives when they improve accessibility, consistency, or implementation speed for complex controls such as dialogs, popovers, selects, tabs, command menus, forms, and sheets.

Do not use a complex component when semantic HTML and CSS are clearer.

Treat Aceternity UI, Magic UI, and similar visual registries as optional inspiration or specialized components. Use them only when:

- the effect serves a real product goal
- the style fits the project
- performance cost is acceptable
- maintenance cost is reasonable
- building it locally offers no clear advantage

## Avoid Generic AI-Looking UI

Do not automatically reach for:

- centered hero with gradient headline
- badge above every heading
- three identical feature cards
- dark purple glow background
- glassmorphism everywhere
- rounded cards nested inside rounded cards
- icons inside identical colored squares
- gradients on every title or button
- decorative grids, glows, noise, tilt, and animated borders all together

Pick a small number of visual moves and use them consistently. A premium page usually has rhythm: emphasis, calm, emphasis, calm.

Do not avoid common patterns merely to appear original. A familiar pattern is appropriate when it improves comprehension or usability.

Originality should come from composition, typography, content, imagery, interaction, and brand expression rather than forced novelty.

## Cards

Cards should communicate grouping, independence, interaction, or a distinct surface.

Avoid wrapping every section in a card. Avoid card-inside-card structures unless the nested surface is genuinely interactive or modal.

## Imagery

When strong photography, illustration, product screenshots, diagrams, or brand assets can carry the visual hierarchy, prefer them over adding decorative effects.

Do not substitute gradients, glows, or abstract backgrounds for meaningful visual content when better imagery is available.

## Typography, Spacing, And Identity

Build the visual base before adding effects:

- typography
- scale
- spacing
- grid
- contrast
- hierarchy
- composition
- imagery
- iconography
- proportion

Do not use motion to compensate for a weak layout.

## Dependencies

Before installing a visual or animation dependency, ask:

- Does the project already have a solution?
- Can CSS solve this?
- Is a native browser API enough?
- Can a small local component solve it?
- Will the dependency be reused?
- Does the benefit justify bundle, maintenance, risk, and lock-in?

Avoid artificial zero-dependency rules. A mature dependency can be better than custom code when it meaningfully reduces risk or maintenance.

## Decision Pattern

Before implementing a meaningful UI surface, decide internally:

- What is the page trying to do?
- Who uses it?
- Is it occasional or daily?
- Is the priority conversion, reading, operation, exploration, or branding?
- Which intensity level fits?
- Which motion, if any, has a function?
- Which existing project primitives should be reused?
- Which existing visual conventions should be preserved?
- Can performance stay healthy on ordinary mobile devices?

Do not turn this into a visible checklist for small tasks. Apply proportional judgment.

## Handling Excessive Visual Requests

When the user requests effects that may harm the product, preserve the intent while reducing the damage.

Example:

```text
Dashboard with parallax, glassmorphism, and scroll animations
```

Prefer:

- glass treatment only on a header or summary panel
- functional motion for filters and state changes
- no parallax over tables or forms
- clear contrast and dense information layout

Improve the user's creative direction instead of silently replacing it.

## Priority

This guidance is heuristic. Apply it together with:

- explicit user instructions
- product requirements
- project design system
- AGENTS.md
- framework constraints
- accessibility requirements
- performance requirements

When these conflict, follow the most specific valid constraint while preserving accessibility, functional correctness, and essential usability.

The best result should feel intentional, refined, fast, coherent, and appropriate to context.
