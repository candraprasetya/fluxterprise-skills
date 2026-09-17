---

name: fluxterprise-flutter-motion
description: "Flutter 60fps smooth animations, micro-interactions, cross-platform consistency. Load with the core and flutter skills."
allowed-tools: Read Write Edit Glob Grep
---

> Created by **Candra Prasetya**

# fluxterprise-flutter-motion

> Flutter 60fps & Micro-Animation Quality Gate

> Part of the fluxterprise system. Read together with `fluxterprise/SKILL.md` (the core) and `fluxterprise-flutter/SKILL.md`. This skill enforces smooth 60fps animations, intentional micro-interactions, and cross-platform motion consistency. Load it when the task involves animation, transitions, gestures, or motion design in Flutter.

## How to use this skill

- Load together with `fluxterprise/SKILL.md` and `fluxterprise-flutter/SKILL.md`. The core holds the gate mechanism; the Flutter skill holds architecture and code quality; this skill holds motion-specific depth.
- Every entry has the same shape: **Tell** (the pattern), **Why** (why it breaks 60fps or feels wrong), **Fix** (what to do instead), with the governing core rule cited as FG-XX or FR-XX.
- The Quality Gate in the core remains the gate. The "Motion Skill Checklist" at the end of this file is the motion-specific supplement to run alongside it.
- Cross-platform: these rules apply to Android, iOS, macOS, and Windows. All motion must be smooth on all targets.

---


## Part 1: 60fps Rules

Every animation must hit 60fps (or 120fps on ProMotion/high-refresh displays). A frame drop is a defect.

### The 16ms Budget

- 60fps = 16.67ms per frame. The build + layout + paint pipeline must complete within that budget.
- A `const` widget costs 0ms to build. A non-const widget that hasn't changed still costs layout+paint time.
- The goal: **minimum work per frame**. Only rebuild what changed, only animate what moves.

### Do Not Animate These Properties

| Property | Why | Alternative |
|----------|-----|-------------|
| `width` / `height` | Triggers layout on every frame | Use `Transform.scale` or `AnimatedSize` |
| `padding` / `margin` | Triggers layout on every frame | Use `Transform.translate` |
| `TextAlign` | Triggers text layout | Animate opacity or transform instead |
| `BoxConstraints` | Triggers layout | Use `Transform` |
| `Opacity` (value 0) | Still paints the widget, just invisible | Use `Visibility` or `Offstage` |
| `Positioned` in `Stack` | Triggers layout | Use `Transform` with `Positioned` static |

### Transform Over Layout

```dart
// WRONG: layout on every frame (expensive)
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  width: _expanded ? 200 : 100,   // layout every frame
  height: _expanded ? 200 : 100,  // layout every frame
)

// CORRECT: transform only (cheap, GPU-composited)
Transform.scale(
  scale: _expanded ? 1.0 : 0.5,
  child: Container(width: 200, height: 200),
)
```

### Opacity vs Visibility

```dart
// WRONG: paints the widget even when invisible
AnimatedOpacity(
  opacity: _visible ? 1.0 : 0.0,
  child: HeavyWidget(),
)

// CORRECT: don't paint at all when hidden
Visibility(
  visible: _visible,
  maintainState: false,
  maintainAnimation: false,
  maintainSize: false,
  maintainSemantics: false,
  maintainInteractivity: false,
  child: HeavyWidget(),
)

// OR: for animated transitions, use FadeTransition + Conditional rendering
if (_visible) FadeTransition(
  opacity: _animation,
  child: HeavyWidget(),
)
```

### Implicit Animations (use first)

Use `AnimatedContainer`, `AnimatedPositioned`, `AnimatedOpacity`, `AnimatedSwitcher` for simple state changes. They handle the animation loop internally and are optimized.

```dart
// CORRECT: implicit animation
AnimatedContainer(
  duration: const Duration(milliseconds: 200),
  curve: Curves.easeOut,
  color: _isSelected ? Colors.blue : Colors.grey,
  child: child,
)
```

### When to Use AnimationController

Use `AnimationController` only when:
- You need **coordinated** multi-step choreography
- The animation is **driven by gestures** (drag, fling)
- The animation needs to be **seekable** (scrubbed by scroll position)
- You need **repeating** or **circular** animations

```dart
// CORRECT: AnimationController for gesture-driven animation
class _DraggableCardState extends State<DraggableCard>
    with SingleTickerProviderStateMixin {
  late final _controller = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 300),
  );

  @override
  void dispose() {
    _controller.dispose(); // ALWAYS dispose
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onHorizontalDragUpdate: (details) {
        _controller.value += details.delta.dx / 200;
      },
      onHorizontalDragEnd: (details) {
        _controller.animateTo(
          0.0,
          duration: const Duration(milliseconds: 300),
          curve: Curves.easeOut,
        );
      },
      child: AnimatedBuilder(
        animation: _controller,
        builder: (context, child) {
          return Transform.translate(
            offset: Offset(_controller.value * 100, 0),
            child: child,
          );
        },
        child: Card(child: widget.content),
      ),
    );
  }
}
```

---


## Part 2: Micro-Interactions

Micro-animations are small, purposeful motions that provide feedback. They should be:

- **Fast**: 100-300ms max
- **Subtle**: don't steal attention
- **Meaningful**: every one communicates a state change

### Button Feedback

```dart
// WRONG: no feedback
ElevatedButton(
  onPressed: _submit,
  child: Text('Submit'),
)

// CORRECT: tap feedback with scale + haptic
ElevatedButton(
  onPressed: _submit,
  child: GestureDetector(
    onTapDown: (_) => _controller.forward(),
    onTapUp: (_) => _controller.reverse(),
    child: ScaleTransition(
      scale: Tween(begin: 1.0, end: 0.95).animate(
        CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
      ),
      child: Text('Submit'),
    ),
  ),
)
```

### Toggle State

```dart
// WRONG: instant switch
Switch(
  value: _enabled,
  onChanged: (v) => setState(() => _enabled = v),
)

// CORRECT: animated toggle with color transition
AnimatedContainer(
  duration: const Duration(milliseconds: 200),
  decoration: BoxDecoration(
    color: _enabled ? Colors.green : Colors.grey,
    borderRadius: BorderRadius.circular(16),
  ),
  child: Switch(
    value: _enabled,
    onChanged: (v) {
      HapticFeedback.lightImpact();
      setState(() => _enabled = v);
    },
  ),
)
```

### List Item Entrance

```dart
// WRONG: everything appears at once
ListView.builder(
  itemCount: posts.length,
  itemBuilder: (_, i) => PostTile(post: posts[i]),
)

// CORRECT: staggered entrance animation
class _PostListState extends State<_PostList>
    with SingleTickerProviderStateMixin {
  late final _controller = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 600),
  );

  @override
  void initState() {
    super.initState();
    _controller.forward();
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: widget.posts.length,
      itemBuilder: (_, i) {
        final delay = (i * 0.05).clamp(0.0, 0.5);
        final animation = CurvedAnimation(
          parent: _controller,
          curve: Interval(delay, (delay + 0.5).clamp(0.0, 1.0), curve: Curves.easeOut),
        );
        return FadeTransition(
          opacity: animation,
          child: SlideTransition(
            position: Tween(begin: const Offset(0, 0.1), end: Offset.zero).animate(animation),
            child: PostTile(post: widget.posts[i]),
          ),
        );
      },
    );
  }
}
```

### Pull-to-Refresh

```dart
// WRONG: basic spinner
RefreshIndicator(
  onRefresh: _loadData,
  child: ListView(...),
)

// CORRECT: custom refresh indicator with animation
RefreshIndicator(
  onRefresh: _loadData,
  strokeWidth: 2.5,
  displacement: 40,
  child: ListView(...),
)
// The RefreshIndicator already animates. Don't add extra animations on top.
```

### Page Transitions

```dart
// WRONG: default slide (boring)
Navigator.of(context).push(MaterialPageRoute(
  builder: (_) => DetailPage(post: post),
));

// CORRECT: platform-appropriate transition
// Android: shared element or fade-through
// iOS: slide from right
// Desktop: fade or scale
GoRouter.of(context).push(
  '/posts/${post.id}',
  extra: post,
);

// Configure in GoRouter:
GoRoute(
  path: '/posts/:id',
  pageBuilder: (context, state) {
    final post = state.extra as Post;
    return CustomTransitionPage(
      child: PostDetailPage(post: post),
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return switch (Theme.of(context).platform) {
          TargetPlatform.iOS => SlideTransition(
            position: Tween(begin: const Offset(1.0, 0.0), end: Offset.zero)
                .animate(CurvedAnimation(parent: animation, curve: Curves.easeOutCubic)),
            child: child,
          ),
          _ => FadeTransition(
            opacity: CurvedAnimation(parent: animation, curve: Curves.easeOut),
            child: child,
          ),
        };
      },
    );
  },
)
```

### Loading Skeleton

```dart
// WRONG: spinner
Center(child: CircularProgressIndicator())

// CORRECT: shimmer loading skeleton
class _SkeletonLoader extends StatefulWidget {
  @override
  State<_SkeletonLoader> createState() => _SkeletonLoaderState();
}

class _SkeletonLoaderState extends State<_SkeletonLoader>
    with SingleTickerProviderStateMixin {
  late final _controller = AnimationController(
    vsync: this,
    duration: const Duration(milliseconds: 1500),
  )..repeat();

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _controller,
      builder: (context, _) {
        return Container(
          decoration: BoxDecoration(
            gradient: LinearGradient(
              begin: Alignment(-1.0 + 2.0 * _controller.value, 0),
              end: Alignment(-0.5 + 2.0 * _controller.value, 0),
              colors: [
                Colors.grey.shade300,
                Colors.grey.shade100,
                Colors.grey.shade300,
              ],
            ),
          ),
        );
      },
    );
  }
}
```

---


## Part 3: Cross-Platform Motion Consistency

### Platform Motion Language

Each platform has its own motion language. Respect it:

| Platform | Transition | Duration | Curve |
|----------|-----------|----------|-------|
| **Android** | Fade through (Material 3) | 300ms | `Curves.easeInOut` |
| **iOS** | Slide from right | 350ms | `Curves.easeOutCubic` |
| **macOS** | Fade + scale | 250ms | `Curves.easeOut` |
| **Windows** | Slide from bottom | 200ms | `Curves.easeOut` |

### Platform-Adaptive Curves

```dart
// WRONG: one curve for all platforms
animation.drive(CurveTween(curve: Curves.easeInOut));

// CORRECT: platform-specific curves
Curve curveFor(BuildContext context) => switch (Theme.of(context).platform) {
  TargetPlatform.iOS => Curves.easeOutCubic,
  TargetPlatform.android => Curves.easeInOut,
  TargetPlatform.macOS => Curves.easeOut,
  TargetPlatform.windows => Curves.easeOut,
  _ => Curves.easeInOut,
};
```

### Platform-Adaptive Durations

```dart
// CORRECT: platform-specific durations
Duration durationFor(BuildContext context) => switch (Theme.of(context).platform) {
  TargetPlatform.iOS => const Duration(milliseconds: 350),
  TargetPlatform.android => const Duration(milliseconds: 300),
  TargetPlatform.macOS => const Duration(milliseconds: 250),
  TargetPlatform.windows => const Duration(milliseconds: 200),
  _ => const Duration(milliseconds: 300),
};
```

### Consistent Haptic Feedback

```dart
// Use haptic feedback consistently across platforms
void hapticLight() => HapticFeedback.lightImpact();   // iOS only, no-op on Android
void hapticMedium() => HapticFeedback.mediumImpact(); // iOS only
void hapticHeavy() => HapticFeedback.heavyImpact();   // iOS only

// For Android: use Vibration.vibrate() if you need actual vibration
// For macOS/Windows: no haptic available, skip silently
```

### Hero Transitions

```dart
// CORRECT: Hero with platform-aware transition
Hero(
  tag: 'post-${post.id}',
  child: PostTile(post: post),
)

// In the destination:
Hero(
  tag: 'post-${post.id}',
  child: PostDetailHeader(post: post),
)
// Flutter handles the platform-appropriate transition automatically.
```

---


## Part 3b: Animation Accessibility

### Respect Reduced Motion

Every animation must respect the user's motion preference. In Flutter, check `MediaQuery.disableAnimations(context)`.

```dart
// WRONG: always animate
AnimatedContainer(
  duration: Duration(milliseconds: 300),
  color: _selected ? Colors.blue : Colors.grey,
)

// CORRECT: respect motion preference
Widget build(BuildContext context) {
  if (MediaQuery.disableAnimations(context)) {
    return Container(color: _selected ? Colors.blue : Colors.grey);
  }
  return AnimatedContainer(
    duration: Duration(milliseconds: 300),
    color: _selected ? Colors.blue : Colors.grey,
  );
}
```

### Reduced Motion Alternatives

| Animation | Full Motion | Reduced Motion |
|-----------|------------|----------------|
| Page transition | Slide from right | Instant (no transition) |
| List entrance | Staggered fade+slide | Instant (all visible) |
| Toggle | Animated color/scale | Instant color/scale change |
| Skeleton shimmer | Gradient sweep | Static grey placeholder |
| Parallax scroll | Offset transform | No transform |
| Hero | Shared element fly | Crossfade (no movement) |

### Animation Accessibility Checklist

- [ ] Does every animation check `MediaQuery.disableAnimations(context)` before playing?
- [ ] Is there a reduced-motion alternative for every animation?
- [ ] Does the UI remain fully functional without animation?
- [ ] Are auto-playing animations (carousel, skeleton) stopped in reduced motion mode?
- [ ] Are essential state changes (focus, error, success) still visible without animation?

---


## Part 4: Animation Patterns

### Staggered List Animation

```dart
class StaggeredListItem extends StatelessWidget {
  const StaggeredListItem({required this.child, required this.index});
  final Widget child;
  final int index;

  @override
  Widget build(BuildContext context) {
    return TweenAnimationBuilder<double>(
      tween: Tween(begin: 0.0, end: 1.0),
      duration: Duration(milliseconds: 400 + (index * 100).clamp(0, 400)),
      curve: Curves.easeOutCubic,
      builder: (context, value, _) {
        return Opacity(
          opacity: value,
          child: Transform.translate(
            offset: Offset(0, 20 * (1 - value)),
            child: child,
          ),
        );
      },
    );
  }
}
```

### Shared Element Transition

```dart
// Hero-based shared element
Hero(
  tag: 'avatar-${user.id}',
  child: CircleAvatar(
    backgroundImage: NetworkImage(user.avatarUrl),
    radius: 24,
  ),
)
```

### Animated List

```dart
// CORRECT: AnimatedList for insert/remove
class _AnimatedPostList extends StatefulWidget {
  @override
  State<_AnimatedPostList> createState() => _AnimatedPostListState();
}

class _AnimatedPostListState extends State<_AnimatedPostList> {
  final _listKey = GlobalKey<AnimatedListState>();
  final _posts = <Post>[];

  void _addPost(Post post) {
    _posts.insert(0, post);
    _listKey.currentState?.insertItem(0, duration: const Duration(milliseconds: 300));
  }

  void _removePost(int index) {
    final removed = _posts.removeAt(index);
    _listKey.currentState?.removeItem(
      index,
      (_, animation) => SizeTransition(
        sizeFactor: animation,
        child: PostTile(post: removed),
      ),
      duration: const Duration(milliseconds: 300),
    );
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedList(
      key: _listKey,
      initialItemCount: _posts.length,
      itemBuilder: (_, i, animation) => FadeTransition(
        opacity: animation,
        child: PostTile(post: _posts[i]),
      ),
    );
  }
}
```

### Scroll-Driven Animation

```dart
class ParallaxHeader extends StatefulWidget {
  const ParallaxHeader({required this.child});
  final Widget child;

  @override
  State<ParallaxHeader> createState() => _ParallaxHeaderState();
}

class _ParallaxHeaderState extends State<ParallaxHeader> {
  final _scrollController = ScrollController();

  @override
  void dispose() {
    _scrollController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return NotificationListener<ScrollNotification>(
      onNotification: (notification) {
        setState(() {});
        return false;
      },
      child: CustomScrollView(
        controller: _scrollController,
        slivers: [
          SliverToBoxAdapter(
            child: AnimatedBuilder(
              listener: (_) {},
              child: widget.child,
              builder: (context, child) {
                final offset = _scrollController.hasClients
                    ? _scrollController.offset
                    : 0.0;
                return Transform.translate(
                  offset: Offset(0, offset * 0.3),
                  child: Opacity(
                    opacity: (1 - offset / 300).clamp(0.0, 1.0),
                    child: child,
                  ),
                );
              },
            ),
          ),
          // ... rest of list
        ],
      ),
    );
  }
}
```

---


## Part 6: External Animation Tools

### When to Use Rive / Lottie

| Tool | Best For | Performance | File Size |
|------|----------|-------------|-----------|
| **Rive** | Interactive animations (buttons, toggles, loaders), state machine animations | Excellent (native runtime, GPU-composited) | Smallest (binary format) |
| **Lottie** | Brand animations (logo reveals, splash), complex vector animations | Good (JSON-based, some overhead) | Medium (JSON can be large) |
| **CustomPainter** | Data visualizations, custom charts, particle effects | Best (direct canvas, zero abstraction) | Zero (code only) |

### Rive Integration

```dart
// pubspec.yaml
dependencies:
  rive: ^0.13.0

// Usage
class RiveLoader extends StatelessWidget {
  const RiveLoader({super.key});

  @override
  Widget build(BuildContext context) {
    return RiveAnimation.asset(
      'assets/animations/loader.riv',
      stateMachines: ['State Machine 1'],
      onInit: (artboard) {
        final controller = StateMachineController.fromArtboard(
          artboard, 'State Machine 1',
        );
        if (controller != null) {
          artboard.addController(controller);
        }
      },
    );
  }
}
```

### Lottie Integration

```dart
// pubspec.yaml
dependencies:
  lottie: ^3.0.0

// Usage
class LottieSuccess extends StatelessWidget {
  const LottieSuccess({super.key});

  @override
  Widget build(BuildContext context) {
    return Lottie.asset(
      'assets/animations/success.json',
      width: 120,
      height: 120,
      repeat: false,
      onLoaded: (composition) {
        // Animation duration: composition.duration
      },
    );
  }
}
```

### Lottie Performance Rules

| Rule | Why |
|------|-----|
| Pre-cache animations with `Lottie.asset()` during splash | Avoids first-play jank |
| Use `repeat: false` for one-shot animations | Saves CPU when idle |
| Keep JSON files under 100KB | Large JSON causes frame drops on decode |
| Avoid gradient fills in Lottie | Expensive to render per-frame |
| Use `Lottie.network()` with caching | Avoids re-download |

### Rive vs Lottie Decision

- **Use Rive** when: animation is interactive (responds to touch/state), needs state machines, needs smallest file size
- **Use Lottie** when: animation is a pre-made brand asset (from After Effects), needs designer collaboration, is a simple playback
- **Use CustomPainter** when: animation is data-driven (charts, particles), needs per-frame logic, needs pixel-level control

---


## Part 7: CustomPainter Performance

Custom painting is the most performant way to draw complex visuals, but it's also the easiest way to create jank if done wrong.

### Path Caching

```dart
// WRONG: recreate Path every frame
@override
void paint(Canvas canvas, Size size) {
  final path = Path()
    ..moveTo(0, 0)
    ..lineTo(size.width, size.height)
    ..close();
  canvas.drawPath(path, paint);
}

// CORRECT: cache Path, only recreate when size changes
Path? _cachedPath;
Size? _cachedSize;

@override
void paint(Canvas canvas, Size size) {
  if (_cachedSize != size) {
    _cachedPath = Path()
      ..moveTo(0, 0)
      ..lineTo(size.width, size.height)
      ..close();
    _cachedSize = size;
  }
  canvas.drawPath(_cachedPath!, paint);
}
```

### Paint Object Reuse

```dart
// WRONG: create Paint every frame
@override
void paint(Canvas canvas, Size size) {
  final paint = Paint()
    ..color = Colors.blue
    ..strokeWidth = 2
    ..style = PaintingStyle.stroke;
  canvas.drawRect(rect, paint);
}

// CORRECT: reuse Paint object
final _paint = Paint()
  ..color = Colors.blue
  ..strokeWidth = 2
  ..style = PaintingStyle.stroke;

@override
void paint(Canvas canvas, Size size) {
  canvas.drawRect(rect, _paint);
}
```

### shouldRepaint

```dart
// WRONG: always repaint
@override
bool shouldRepaint(covariant CustomPainter oldDelegate) => true;

// CORRECT: only repaint when data changes
@override
bool shouldRepaint(covariant _MyPainter oldDelegate) =>
    oldDelegate.data != data;
```

### CustomPainter Performance Rules

| Rule | Why |
|------|-----|
| Cache `Path` objects, recreate only on size change | Path creation is expensive |
| Reuse `Paint` objects, configure once | Paint allocation per frame is wasteful |
| Implement `shouldRepaint` correctly | `true` forces repaint every frame |
| Avoid `canvas.saveLayer()` | Forces offscreen buffer, doubles paint cost |
| Use `RepaintBoundary` around the CustomPaint | Isolates repaint to that subtree |
| Avoid `Path.combine()` in paint | Creates new Path every call, very expensive |

### When to Use CustomPainter vs. Widgets

| Scenario | Use CustomPainter? | Why |
|----------|-------------------|-----|
| Bar chart with 100 bars | **Yes** | One draw call vs 100 widget rebuilds |
| Simple line divider | No | `Divider` widget is simpler |
| Animated particle system | **Yes** | Per-frame logic needs canvas control |
| Gradient background | No | `Container` with `BoxDecoration` is sufficient |
| Custom progress indicator | Depends | Use `CustomPainter` for complex shapes, `AnimatedContainer` for simple ones |

---


## Part 5: Performance Checklist

### Animation Performance Rules

| Rule | Why |
|------|-----|
| Use `Transform` over `Container` sizing | Transform is GPU-composited, no layout recalc |
| Use `Opacity` only for fade-in/out | 0-opacity still paints; use `Visibility` for hide |
| Prefer implicit animations | They skip the animation loop overhead |
| Use `RepaintBoundary` for complex widgets | Isolates repaint to that subtree |
| Avoid `saveLayer` (unnecessary `Opacity` widgets) | Forces offscreen buffer |
| Use `const` widgets | Zero rebuild cost |
| Scope `BlocBuilder` tightly | Don't rebuild the whole screen for a badge update |

### Measuring Performance

```dart
// Use Flutter DevTools or debug paint
MaterialApp(
  showPerformanceOverlay: kDebugMode, // shows frame time graph
)

// Or wrap widgets with RepaintBoundary to isolate
RepaintBoundary(
  child: AnimatedWidget(),
)
```

### Jank Detection

```dart
// Monitor frame timing
import 'dart:developer';

void _onFrameTimings(FrameTiming timings) {
  final buildDuration = timings.buildDuration.inMicroseconds;
  final rasterDuration = timings.rasterDuration.inMicroseconds;
  if (buildDuration > 16000 || rasterDuration > 16000) {
    log('JANK: build=${buildDuration}us raster=${rasterDuration}us');
  }
}

// In main.dart:
WidgetsBinding.instance.addTimingsCallback(_onFrameTimings);
```

---


## Motion Skill Checklist

Run these alongside the core Quality Gate when the task involves animation or motion. All answers must be **yes**:

### 60fps (must pass)

- [ ] Do all animations use `Transform` over layout properties (width, height, padding)?
- [ ] Is `Opacity(0)` replaced with `Visibility` or conditional rendering?
- [ ] Are all `AnimationController`s, `ScrollController`s, and `StreamSubscription`s disposed?
- [ ] Are `BlocBuilder`s scoped to only the widgets that need them?
- [ ] Is `const` used on all immutable widgets?
- [ ] Are `RepaintBoundary` used on complex animated subtrees?

### Micro-Interactions (must pass)

- [ ] Does every interactive element have tap/press feedback (scale, haptic, or color)?
- [ ] Are list items staggered on entrance (not all appearing at once)?
- [ ] Are page transitions platform-appropriate (slide on iOS, fade on Android)?
- [ ] Are loading states skeletons/shimmer (not bare spinners)?
- [ ] Are toggle states animated (not instant switch)?

### Cross-Platform (must pass)

- [ ] Are curves and durations platform-specific?
- [ ] Are haptic calls wrapped to no-op on unsupported platforms?
- [ ] Are Hero transitions used for shared elements across pages?
- [ ] Is the layout adaptive (mobile/tablet/desktop)?
- [ ] Do animations feel native on each target platform?

### Memory (must pass)

- [ ] Is every controller disposed in `dispose()`?
- [ ] Are repeating animations cancelled when the widget is removed?
- [ ] Are scroll controllers disposed when the list is removed?
- [ ] Are stream subscriptions cancelled on dispose?
- [ ] Is pagination used for long lists (not loading everything at once)?


Relative paths in this skill (e.g., scripts/, reference/) are relative to this base directory.
