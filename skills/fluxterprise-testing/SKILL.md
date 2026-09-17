---
name: fluxterprise-testing
description: "Testing quality gate. Unit, integration, accessibility, and visual regression testing. Load with the core."
allowed-tools: Read Write Edit Glob Grep
---
# fluxterprise-testing

> Testing Quality Gate

> Created by **Candra Prasetya**

> Part of the fluxterprise system. Read together with `fluxterprise/SKILL.md` (the core). This skill enforces testing standards: unit tests, integration tests, accessibility testing, and visual regression. Load it when the task involves writing tests, setting up test infrastructure, or validating deliverables.

## How to use this skill

- Load together with `fluxterprise/SKILL.md` whenever the task touches testing. The core holds the gate mechanism; this skill holds testing-specific depth.
- Every entry has the same shape: **Tell** (the pattern), **Why** (why it falls below the gate), **Fix** (what to do instead).
- The Quality Gate in the core remains the gate. The "Testing Skill Checklist" at the end of this file is the testing-specific supplement to run alongside it.

---

## Part 1: Testing Philosophy

### Test the Behavior, Not the Implementation

- **Tell:** tests that assert on internal state (`expect(cubit.state, isA<Loaded>())`), test private methods, or verify exact widget tree structure.
- **Why:** implementation-coupled tests break on every refactor, even when behavior is unchanged. They test the "how" instead of the "what", so they give false failures and erode trust in the test suite.
- **Fix:** test observable behavior: what the user sees (widget output), what the API returns (use case output), what the UI does (navigation, state changes). Internal details are implementation, not behavior.
- **Rule:** C-1 (intentionality), C-4 (resilience).

### Test Pyramid

| Level | What It Tests | Speed | Cost | Count |
|-------|--------------|-------|------|-------|
| **Unit** | Pure logic, use cases, cubits | <1ms each | Low | Many (80%) |
| **Widget** | Widget rendering, interactions | 10-50ms each | Medium | Some (15%) |
| **Integration** | Full flows, multi-screen | 100ms-5s each | High | Few (5%) |

- **Tell:** all tests are integration tests, or all tests are unit tests.
- **Why:** all-integration is slow and brittle; all-unit misses integration bugs. The pyramid exists because each level catches different classes of defects at different costs.
- **Fix:** follow the pyramid: many fast unit tests, some widget tests, few integration tests. Unit tests catch logic bugs. Widget tests catch rendering bugs. Integration tests catch flow bugs.

---

## Part 2: Unit Testing Patterns

### Cubit Testing (Flutter)

```dart
// Mock the use case, one layer down
class _MockGetPosts extends Mock implements GetPosts {}

void main() {
  late _MockGetPosts mockGetPosts;
  late PostsCubit cubit;

  setUp(() {
    mockGetPosts = _MockGetPosts();
    cubit = PostsCubit(mockGetPosts);
  });

  tearDown(() => cubit.close());

  group('PostsCubit', () {
    blocTest<PostsCubit, PostsState>(
      'emits [loading, loaded] when getPosts succeeds',
      build: () => cubit,
      setUp: () {
        when(() => mockGetPosts(any()))
            .thenAnswer((_) async => const Right([post]));
      },
      act: (cubit) => cubit.load(),
      expect: () => const [
        PostsState.loading(),
        PostsState.loaded([post]),
      ],
    );

    blocTest<PostsCubit, PostsState>(
      'emits [loading, error] when getPosts fails',
      build: () => cubit,
      setUp: () {
        when(() => mockGetPosts(any()))
            .thenAnswer((_) async => const Left(Failure.server('timeout')));
      },
      act: (cubit) => cubit.load(),
      expect: () => const [
        PostsState.loading(),
        PostsState.error('timeout'),
      ],
    );
  });
}
```

### Use Case Testing

```dart
class _MockPostRepository extends Mock implements PostRepository {}

void main() {
  late _MockPostRepository mockRepository;
  late GetPosts useCase;

  setUp(() {
    mockRepository = _MockPostRepository();
    useCase = GetPosts(mockRepository);
  });

  test('returns posts from repository', () async {
    when(() => mockRepository.getPosts())
        .thenAnswer((_) async => const Right([post]));

    final result = await useCase(const NoParams());

    expect(result, const Right([post]));
    verify(() => mockRepository.getPosts()).called(1);
  });

  test('returns failure when repository fails', () async {
    when(() => mockRepository.getPosts())
        .thenAnswer((_) async => const Left(Failure.network('offline')));

    final result = await useCase(const NoParams());

    expect(result, const Left(Failure.network('offline')));
  });
}
```

### Repository Testing

```dart
class _MockRemoteDataSource extends Mock implements PostRemoteDataSource {}
class _MockLocalDataSource extends Mock implements PostLocalDataSource {}
class _MockNetworkInfo extends Mock implements NetworkInfo {}

void main() {
  late _MockRemoteDataSource remote;
  late _MockLocalDataSource local;
  late _MockNetworkInfo network;
  late PostRepositoryImpl repository;

  setUp(() {
    remote = _MockRemoteDataSource();
    local = _MockLocalDataSource();
    network = _MockNetworkInfo();
    repository = PostRepositoryImpl(
      remoteDataSource: remote,
      localDataSource: local,
      networkInfo: network,
    );
  });

  group('getPosts', () {
    test('online: fetches remote, caches, returns entity', () async {
      when(() => network.isConnected).thenAnswer((_) async => true);
      when(() => remote.getPosts()).thenAnswer((_) async => [postModel]);
      when(() => local.cachePosts(any())).thenAnswer((_) async {});

      final result = await repository.getPosts();

      result.match(
        (failure) => fail('expected Right, got Left($failure)'),
        (posts) => expect(posts, equals(const [post])),
      );
      verify(() => local.cachePosts([postModel])).called(1);
    });

    test('offline: returns cached data', () async {
      when(() => network.isConnected).thenAnswer((_) async => false);
      when(() => local.getCachedPosts()).thenAnswer((_) async => [postModel]);

      final result = await repository.getPosts();

      result.match(
        (failure) => fail('expected Right, got Left($failure)'),
        (posts) => expect(posts, equals(const [post])),
      );
      verifyNever(() => remote.getPosts());
    });
  });
}
```

---

## Part 3: Widget Testing

### Basic Widget Test

```dart
void main() {
  testWidgets('PostTile displays post title and body', (tester) async {
    await tester.pumpWidget(MaterialApp(
      home: PostTile(post: post),
    ));

    expect(find.text('Post Title'), findsOneWidget);
    expect(find.text('Post body text'), findsOneWidget);
  });

  testWidgets('PostTile calls onTap when tapped', (tester) async {
    var tapped = false;
    await tester.pumpWidget(MaterialApp(
      home: PostTile(post: post, onTap: () => tapped = true),
    ));

    await tester.tap(find.byType(PostTile));
    expect(tapped, true);
  });
}
```

### Widget Test with Cubit

```dart
void main() {
  testWidgets('PostsPage shows loading then loaded', (tester) async {
    final cubit = MockPostsCubit();
    when(() => cubit.state).thenReturn(const PostsState.loading());
    whenListen(cubit, Stream.fromIterable([
      const PostsState.loading(),
      const PostsState.loaded([post]),
    ]));

    await tester.pumpWidget(MaterialApp(
      home: BlocProvider<PostsCubit>.value(
        value: cubit,
        child: const PostsPage(),
      ),
    ));

    // Loading state
    expect(find.byType(CircularProgressIndicator), findsOneWidget);

    // Loaded state
    await tester.pump();
    expect(find.text('Post Title'), findsOneWidget);
  });
}
```

### Widget Test Checklist

- [ ] Does every widget have at least one test?
- [ ] Are interactions tested (tap, scroll, input)?
- [ ] Are all UI states tested (loading, error, empty, loaded)?
- [ ] Are edge cases tested (empty list, long text, no network)?

---

## Part 4: Accessibility Testing

### Automated Accessibility Testing

```dart
// Flutter: use flutter_test accessibility checks
testWidgets('PostTile meets accessibility standards', (tester) async {
  await tester.pumpWidget(MaterialApp(
    home: PostTile(post: post),
  ));

  // Check for semantics
  final semantics = tester.getSemantics(find.byType(PostTile));
  expect(semantics.label, isNotEmpty);

  // Check for tap target size
  final size = tester.getSize(find.byType(PostTile));
  expect(size.height, greaterThanOrEqualTo(44));
});

// Web: use axe-core in integration tests
// npm install --save-dev @axe-core/playwright
```

### Manual Accessibility Checklist

Run these alongside the automated tests:

- [ ] Can every screen be navigated by keyboard only?
- [ ] Does Tab order match visual order?
- [ ] Is every focusable element visually indicated?
- [ ] Can all dialogs be closed with Escape?
- [ ] Do all images have alt text (or alt="" for decorative)?
- [ ] Do all form fields have labels?
- [ ] Is text contrast at least 4.5:1 (normal) or 3:1 (large)?
- [ ] Does the UI work at 200% zoom?
- [ ] Is `prefers-reduced-motion` respected (web) or `MediaQuery.disableAnimations` (Flutter)?

---

## Part 5: Visual Regression Testing

### Screenshot Testing (Flutter)

```dart
// Use golden_toolkit or flutter_test golden tests
// pubspec.yaml: dev_dependencies: golden_toolkit: ^0.15.0

testGoldens('PostTile renders correctly', (tester) async {
  await tester.pumpWidgetBuilder(
    PostTile(post: post),
    wrapper: (child) => MaterialApp(home: child),
  );

  await screenMatchesGolden(tester, 'post_tile_default');
});

testGoldens('PostTile hover state', (tester) async {
  await tester.pumpWidgetBuilder(
    PostTile(post: post),
    wrapper: (child) => MaterialApp(home: child),
  );

  await tester.hover(find.byType(PostTile));
  await screenMatchesGolden(tester, 'post_tile_hover');
});
```

### Screenshot Testing (Web)

```javascript
// Playwright
const { test, expect } = require('@playwright/test');

test('homepage matches snapshot', async ({ page }) => {
  await page.goto('/');
  await expect(page).toHaveScreenshot('homepage.png', {
    maxDiffPixelRatio: 0.01,
  });
});
```

### Visual Regression Checklist

- [ ] Are critical screens covered by golden/screenshot tests?
- [ ] Are all theme variants (light/dark) covered?
- [ ] Are all breakpoints (mobile/tablet/desktop) covered?
- [ ] Is the max diff threshold set low enough to catch real regressions?

---

## Part 6: CI Integration

### Pre-Commit Checks

```bash
# .husky/pre-commit or similar
flutter analyze          # Lint
flutter test             # Unit + widget tests
dart format --set-exit-if-changed .  # Format check
```

### CI Pipeline Checks

```yaml
# GitHub Actions example
steps:
  - run: flutter analyze
  - run: flutter test --coverage
  - run: dart format --set-exit-if-changed .
  - run: dart run build_runner build --delete-conflicting-outputs
```

### Coverage Thresholds

| Metric | Minimum | Why |
|--------|---------|-----|
| Line coverage | 80% | Catches most regressions |
| Branch coverage | 70% | Ensures conditional paths tested |
| Critical path coverage | 100% | Auth, payment, data mutation |

---

## Testing Skill Checklist

Run these alongside the core Quality Gate. All answers must be **yes**:

### Unit Tests

- [ ] Does every cubit have tests for loading, success, and failure states?
- [ ] Does every use case have tests for success and failure?
- [ ] Does every repository have tests for online and offline behavior?
- [ ] Are mocks one layer down (use case mocks repository, cubit mocks use case)?
- [ ] Are mock classes private (`_MockXxx`) at the top of each test file?

### Widget Tests

- [ ] Does every page/screen have at least one widget test?
- [ ] Are all UI states tested (loading, error, empty, loaded)?
- [ ] Are interactions tested (tap, scroll, input)?
- [ ] Are edge cases tested (empty list, long text, no network)?

### Accessibility Tests

- [ ] Is keyboard navigation tested on every screen?
- [ ] Are tap target sizes verified (minimum 44x44 logical pixels)?
- [ ] Are text contrast ratios verified against the contrast checker?
- [ ] Is reduced motion behavior tested?

### Visual Regression

- [ ] Are critical screens covered by golden/screenshot tests?
- [ ] Are theme variants (light/dark) covered?
- [ ] Are breakpoints (mobile/tablet/desktop) covered?

### CI

- [ ] Does the CI pipeline run `flutter analyze` and `flutter test`?
- [ ] Is there a coverage threshold enforced?
- [ ] Are golden tests run in CI with platform-specific rendering?

---

## Quick Reference

| Concern | Tool | Command |
|---------|------|---------|
| **Unit tests** | `flutter test` | Runs all tests in `test/` |
| **Single test** | `flutter test test/path/to/test.dart` | Runs one file |
| **Coverage** | `flutter test --coverage` | Generates `lcov.info` |
| **Lint** | `flutter analyze` | Runs `analysis_options.yaml` |
| **Format** | `dart format .` | Formats all Dart files |
| **Build runner** | `dart run build_runner build --delete-conflicting-outputs` | Regenerate mocks/freezed |
| **Golden tests** | `flutter test --update-goldens` | Update golden files |
| **Web a11y** | `npx axe-cli http://localhost:3000` | Run axe-core audit |
