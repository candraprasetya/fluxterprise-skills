# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- (planned) `fluxterprise-perf` — Dedicated performance skill
- (planned) `fluxterprise-designsystem` — Design system skill
- (planned) `fluxterprise-api` — API integration skill
- (planned) `fluxterprise-ci` — CI/CD integration skill

## [1.0.0] - 2026-09-18

### Added
- Core quality gate system (`fluxterprise`) with 38 rules (FG-01 to FG-38)
- Five-block Quality Gate: Hard Gate, Purpose Gate, Craftsmanship, Quality Locks, Performance
- Three dials system: ENERGY, RHYTHM, MOTION with web and Flutter anchors
- `fluxterprise-ui` — Visual & component patterns, design tokens, forms
- `fluxterprise-copywriting` — Copy patterns, microcopy, SEO, anti-AI-writing
- `fluxterprise-human` — Accessibility, ARIA, screen readers, motion sensitivity, contrast checker
- `fluxterprise-layoutmobile` — Mobile responsive layout patterns
- `fluxterprise-code` — Code comment hygiene
- `fluxterprise-flutter` — Dart shorthand, clean architecture, Material 3, i18n, reusable components
- `fluxterprise-flutter-motion` — 60fps animations, micro-interactions, Rive/Lottie, CustomPainter
- `fluxterprise-testing` — Unit, widget, integration, accessibility, visual regression testing
- Contrast checker script (`contrast-check.py`) with AA + AAA support, batch mode, JSON output
- Contrast checker MCP server (`contrast-mcp.py`)
- Install script (`scripts/install.sh`)
- SVG diagrams for documentation (quality-gate-flow, skill-map, before-after, three-dials, how-it-works)
- Comprehensive README with before/after examples, pros/cons, token usage estimates
- Flutter Enterprise Conventions reference (based on flutter_enterprise_starter_kit)
- Project Scaffold Protocol and Implementation Workflow enforcement
- Installation support for OpenCode, Claude Code, AGY Plugin, and manual setup

### Changed
- Rule prefix changed from `R-XX` to `FG-XX` (Fluxterprise Gate)
- Philosophy changed from "anti-slop" (destructive) to "Quality Gate" (constructive)
- All "Anti Slop" references replaced with "Fluxterprise"
- Flutter skills updated to match flutter_enterprise_starter_kit architecture
- Material 3 latest patterns added (Flutter 3.22+)
- i18n guidance added (gen_l10n, ARB files)

### Fixed
- R-XX to FG-XX aliasing across all sub-skills
- Local filesystem paths removed from distributable files
- Empty folder enforcement added to prevent incomplete implementations

## [0.1.0] - 2026-09-17

### Added
- Initial project structure
- Basic skill framework
- Core rules (originally named "antislop")

[Unreleased]: https://github.com/candraprasetya/fluxterprise-skills/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/candraprasetya/fluxterprise-skills/releases/tag/v1.0.0
[0.1.0]: https://github.com/candraprasetya/fluxterprise-skills/releases/tag/v0.1.0
