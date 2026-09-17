---
name: fluxterprise-human
description: "Human and accessibility skill for fluxterprise. Contrast, keyboard, focus, and states for real people. Includes the contrast checker."
allowed-tools: Bash(python *) Bash(python3 *) Read Write Edit Glob Grep
---

> Created by **Candra Prasetya**
# fluxterprise-human

> Fluxterprise: Rules for AI Coding Agents. Human skill

> Part of the fluxterprise system. Read together with `fluxterprise/SKILL.md` (the core). This skill deep-dives the human concern: the UI must stay usable by people with different eyes, hands, and setups. Contrast, keyboard, focus, states, and the mobile details that exclude people.

## How to use this skill

- Load together with `fluxterprise/SKILL.md` whenever the task builds or edits UI. The core holds the mechanism (the purpose test, the three tiers, the Delivery Gate); this skill holds the human-side depth: the parts of a UI that exclude people with different eyes, hands, and setups.
- Every entry has the same shape: **Tell** (the pattern), **Why** (who it excludes, and why it reads as unfinished), **Fix** (what to do instead), with the governing core rule cited as FG-XX.
- Accessibility is not a checklist of extras bolted on at the end. It is part of the core promise that "the UI holds up" (C-4). The Delivery Gate in the core remains the gate; the "Human Skill Checklist" at the end of this file is the supplement to run alongside it.
- The contrast checker (formula + reference table + script) lives in this skill. Use it for every color pairing you cannot verify by eye.
- This skill keeps only the mobile details that exclude people: zooming, and the on-screen keyboard.

## Color & Contrast

### Low-Contrast Text

- **Tell:** light grey text on a white or near-white background, thin body text, muted labels chosen because they look "elegant" but are hard to read.
- **Why:** it excludes low-vision users and everyone in bright light. It is a visual choice made without checking the standard, which is exactly the kind of default the filter exists to catch.
- **Fix:** meet WCAG AA minimums (FG-25): 4.5:1 for normal text, 3:1 for large text (18px+). Compute the ratio; do not eyeball it.

### Text Over a Photo or Gradient

- **Tell:** white text placed directly over an image or gradient that is light in some areas, checked at one bright spot only.
- **Why:** contrast is local. Where the image is light, the text drops below 4.5:1 even if the hero still "looks" fine. FG-25 requires testing the whole area the text passes over, not a single point.
- **Fix:** add a scrim or a solid color block behind the text, then verify the worst spot, not the best. If any part of the text area fails, the treatment fails.

### The Grey-on-Grey Hallucination

- **Tell:** "dark grey on black" or "light grey on white" claimed to pass AA without a computation.
- **Why:** this is the most common accessibility hallucination. The eye overestimates contrast on grey pairs, and agents repeat the claim because it sounds plausible. #555555 on black is 2.8:1. It fails.
- **Fix:** never assert a pairing passes. Run the contrast checker (below) or apply the formula. When neither is possible, use the reference table.

### Non-Text Contrast

- **Tell:** interactive components (buttons, icons, input borders, focus indicators, chart segments) distinguished from their background by less than 3:1.
- **Why:** non-text UI carries information by shape and edge. When the edge is a hair of tint, low-vision users cannot find the control. The same bar applies to states like hover and selected.
- **Fix:** give every component boundary and every status indicator a 3:1 ratio against adjacent colors (WCAG 1.4.11). Pair icons with a text label that meets 4.5:1.

### The Contrast Checker

The home of the contrast checker. Three layers, from most to least convenient:

**The script.** When a script runtime is available and the file is present, run it instead of computing by hand. The script ships in this skill's folder (`contrast-check.py`, next to this `SKILL.md`). Run it with `python3` on macOS and Linux, `python` on Windows:

```bash
python3 "${CLAUDE_SKILL_DIR}/contrast-check.py" "#FFFFFF" "#777777"
# normal text: FAIL (4.48 < 4.5)
# large text:  PASS (4.48 >= 3.0)
```

If the `${CLAUDE_SKILL_DIR}` variable is not available in this agent, point the script path at this skill's folder directly. The script exists so agents stop hallucinating AA. It takes two hex colors and prints the ratio and the verdict for both text sizes. If the file is missing, the formula and table below are complete on their own. Never block on the script.

**The formula (WCAG 2.x).**

1. Contrast ratio = (L1 + 0.05) / (L2 + 0.05), where L1 is the lighter relative luminance and L2 the darker.
2. Relative luminance L of one color: convert each channel to 0-1 (`c = hex / 255`), then linearize: if `c <= 0.03928`, `c_lin = c / 12.92`; otherwise `c_lin = ((c + 0.055) / 1.055)^2.4`.
3. `L = 0.2126*R + 0.7152*G + 0.0722*B`.
4. Round the ratio to two decimals and compare: 4.5:1 for normal text, 3:1 for large text (18px+, per FG-25). The maximum ratio is 21.0 (black on white).

**The reference table** (common pairings, computed with the formula):

| Pairing (text on background) | Ratio | Normal text (4.5) | Large text (3.0) |
|------------------------------|-------|-------------------|------------------|
| Black on white | 21.00 | Pass | Pass |
| White on black | 21.00 | Pass | Pass |
| White on #333333 | 12.63 | Pass | Pass |
| White on #666666 | 5.74 | Pass | Pass |
| #777777 on white | 4.48 | Fail | Pass |
| White on #888888 | 3.54 | Fail | Pass |
| White on #999999 | 2.85 | Fail | Fail |
| #555555 on black | 2.82 | Fail | Fail |

Read the table as a sanity check, not as a substitute. Any pairing not listed, or anything near a threshold, goes through the formula or the script.

## Keyboard

### Removed Focus Outline

- **Tell:** `outline: none` or `outline: 0` with no replacement focus style.
- **Why:** keyboard users cannot see where they are. It is the fastest way to make a UI unusable without a mouse, and FG-32 forbids it outright.
- **Fix:** keep or replace the outline with a visible `:focus-visible` style that meets the same contrast bar (3:1 against its neighbors). Never set `outline: none` without a replacement.

### Mouse-Only Patterns

- **Tell:** menus that open on hover only, dropdowns that click-open but do not keyboard-open, drag-and-drop with no keyboard fallback.
- **Why:** each one excludes keyboard and assistive-technology users (FG-32). If a control cannot be reached and operated by Tab, Enter, or Space, it does not exist for a whole group of people.
- **Fix:** every interactive element is reachable and operable by keyboard (FG-32): logical tab order following visual order, activation with Enter or Space, and dialogs closable with Escape (FG-26).

### Broken Tab Order

- **Tell:** focus jumps around the page, skips content, or lands on hidden elements because the DOM order does not match the visual order.
- **Why:** tab order that reads the code order instead of the visual order makes navigation unpredictable (FG-32). Users lose their place and the page feels broken.
- **Fix:** keep the source order matching the visual order, add skip links for long pages, and never give real content `tabindex="-1"` unless it is part of a controlled focus trap such as a dialog.

## Focus & States

### Weak or Invisible Focus Indicator

- **Tell:** a focus ring the same color as the background, a ring that only appears on hover, or an indicator thinner than a 1px border.
- **Why:** the focus indicator is how keyboard users know where they are. If it fails the contrast bar or only shows on hover, keyboard-only use breaks (FG-32, FG-34).
- **Fix:** a visible focus indicator on every interactive element, 3:1 against adjacent colors, in every theme you ship. Check it in dark and light mode.

### Color-Only Feedback

- **Tell:** success, error, and status communicated only by color: red error text, green success border, a tinted chip, with no icon, label, or text.
- **Why:** it excludes color-blind and low-vision users, and it disappears entirely in forced-colors mode. A status that depends on seeing hue is not a status (C-4).
- **Fix:** pair every color signal with text, an icon, or a pattern. Error states are text first: "Password must be at least 8 characters", not just a red border.

### Missing UI States

- **Tell:** a data view with no empty, loading, or error state, or states that exist but are invisible: a spinner with no text, an empty screen with no explanation.
- **Why:** FG-27 requires the three states; the accessibility angle is that each must be perceivable and informative, not decorative. A loading spinner with no context reads as a frozen page to screen-reader users.
- **Fix:** every data view has all three states (FG-27), each announced or visible: an explicit empty message, a loading state with text, and an error state that says what happened and how to proceed.

## Zoom & Mobile Use

The layout mechanics behind mobile (breakpoints, scale, grids, overflow, tap targets) are the concern of `fluxterprise-layoutmobile`. This section keeps only the mobile details that exclude people: zooming, and the on-screen keyboard.

### Text That Cannot Zoom

- **Tell:** fixed pixel font sizes, or containers with `overflow: hidden` that clip text at 200% zoom.
- **Why:** users must be able to resize text (WCAG 1.4.4). If zooming to 200% clips the content or forces horizontal scroll, the text is not resizable in practice.
- **Fix:** fluid type that reflows with zoom, no clipping containers on text, and verify the layout holds at 200% zoom on a narrow viewport (FG-35).

### Mobile Keyboard Covers the Form

- **Tell:** inputs at the bottom of the viewport hidden behind the on-screen keyboard, with no scroll-into-view and no room for the input.
- **Why:** a form the user cannot see or reach is a form they cannot complete. It is a mobile-only exclusion (FG-03).
- **Fix:** when an input is focused, it scrolls into view above the keyboard, with enough bottom padding that the focused field is never covered. Test with a real device or an emulated keyboard.

## ARIA & Semantics

### No Semantic Markup

- **Tell:** `<div>` and `<span>` for everything: buttons, headings, lists, navigation, dialogs. No `<main>`, `<nav>`, `<header>`, `<footer>`, `<aside>`, `<article>`, `<section>`.
- **Why:** screen readers use semantic elements to build a page map. Without them, the entire page is one undifferentiated block. Keyboard users cannot skip to main content. Landmark navigation breaks entirely.
- **Fix:** use semantic HTML elements for their intended purpose. Every page needs at least `<main>` for primary content. Navigation uses `<nav>`. Interactive controls use `<button>` or `<a>`, never `<div onclick>`.
- **Rule:** FG-32 (keyboard accessibility), C-4 (resilience).

### Missing ARIA Labels

- **Tell:** icon-only buttons with no `aria-label`, images with no `alt` or empty `alt=""` on images that carry meaning, custom widgets (tabs, accordions, toggles) with no ARIA roles.
- **Why:** screen readers announce "button" with no context, or skip images entirely. A user relying on a screen reader cannot tell what a star icon button does.
- **Fix:** every icon-only control gets `aria-label` describing its action ("Star this post", not "Star"). Every meaningful image gets descriptive `alt` text. Decorative images get `alt=""` or `role="presentation"`. Custom widgets get appropriate ARIA roles (`role="tablist"`, `role="tab"`, `aria-selected`).
- **Rule:** FG-32.

### Missing Live Regions

- **Tell:** dynamic content updates (toast notifications, chat messages, form validation errors, loading states) that are not announced to screen readers.
- **Why:** the visual user sees a toast appear; the screen reader user hears nothing. A form validation error appears on screen but the screen reader user has no idea why the submit failed.
- **Fix:** use `aria-live="polite"` for non-urgent updates (toast, status messages). Use `aria-live="assertive"` for urgent updates (error messages, connection lost). Use `role="alert"` for immediate announcements. In Flutter, use `SemanticsService.announce()`.
- **Rule:** FG-32, FG-27 (UI states).

### Missing Landmark Navigation

- **Tell:** no skip-to-content link, no `<main>` landmark, no `<nav>` landmark, content not navigable by landmark.
- **Why:** keyboard and screen reader users must tab through every element to reach main content. On a page with 50 nav items, that is 50 tabs before the content starts.
- **Fix:** add a skip-to-content link as the first focusable element: `<a href="#main" class="skip-link">Skip to content</a>`. Wrap primary content in `<main id="main">`. Wrap navigation in `<nav>`.
- **Rule:** FG-32.

### Flutter: Semantics Widget

- **Tell:** `Icon(Icons.star)` with no `Semantics`, `GestureDetector` with no `Semantics`, `CustomPaint` with no `Semantics`.
- **Why:** Flutter's Semantics widget is the equivalent of ARIA. Without it, screen readers (VoiceOver, TalkBack) announce "button" or "image" with no context.
- **Fix:** wrap meaningful icons in `Semantics(label: 'Star this post')`. Give every custom-painted element a semantic label. Use `SemanticsService.announce()` for dynamic content updates.
- **Rule:** FG-32, FR-15 (Flutter accessibility).

## Motion Sensitivity

### No Reduced Motion Support

- **Tell:** parallax effects, auto-playing carousels, fade-in animations, scroll-triggered animations that play regardless of user preference.
- **Why:** vestibular disorders affect ~35% of adults over 40. Motion can cause nausea, dizziness, and disorientation. WCAG 2.3.3 requires animation from interactions to be disableable.
- **Fix:** respect `prefers-reduced-motion: reduce` (web) or `MediaQuery.disableAnimations` (Flutter). When detected:
  - Disable parallax effects
  - Replace slide/fade transitions with instant state changes
  - Stop auto-playing carousels
  - Remove scroll-triggered animations
  - Keep only essential motion (focus indicators, state changes)
- **Rule:** FG-32 (keyboard accessibility), C-4 (resilience).

### Implementation

**Web:**
```css
@media (prefers-reduced-motion: reduce) {
  *, *::before, *::after {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

**Flutter:**
```dart
// Check before animating
final disableAnimations = MediaQuery.disableAnimations(context);

// Use in animation decisions
Widget build(BuildContext context) {
  if (MediaQuery.disableAnimations(context)) {
    return PostTile(post: post); // no animation
  }
  return FadeTransition(
    opacity: _animation,
    child: PostTile(post: post),
  );
}
```

- Always test with reduced motion enabled. The UI must remain fully functional without animation.

## Human Skill Checklist

Run these alongside the core Delivery Gate when the task involves UI. All answers must be **yes**:

- [ ] Is every text and background pairing verified against the contrast checker (formula, table, or script), including text over images and gradients? (FG-25)
- [ ] Does every interactive component boundary and status indicator meet 3:1 against its background? (non-text contrast)
- [ ] Is the focus indicator visible, high-contrast, and present on every interactive element in every theme? (FG-32, FG-34)
- [ ] Is every interactive element reachable and operable by keyboard, with dialogs closable via Escape and no `outline: none` without a replacement? (FG-32, FG-26)
- [ ] Are the empty, loading, and error states of every data view present and perceivable, not color-only? (FG-27, C-4)
- [ ] Can text be resized to 200% without being clipped, and does the mobile keyboard never cover a focused input? (FG-35)
