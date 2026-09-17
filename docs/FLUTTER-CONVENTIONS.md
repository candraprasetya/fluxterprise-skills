# Flutter Enterprise Conventions

Detailed reference for the `fluxterprise-flutter` skill. This document describes the architecture, patterns, and conventions used in the [Flutter Enterprise Starter Kit](https://github.com/nicolinx/flutter_enterprise_starter_kit).

## Why Clean Architecture

Each feature is split into `data` / `domain` / `presentation`, and dependencies only point inward: `presentation` depends on `domain`, `data` implements `domain`'s interfaces, and `domain` depends on nothing external (no Flutter, no Firebase, no Dio). This is what makes the codebase testable and lets a data source change (REST to GraphQL, Firestore to Supabase) without touching domain or UI code.

## Why Cubit, not full Bloc

Only use `flutter_bloc`'s `Cubit`, not the event-based `Bloc` API. Every feature is a direct action-to-state transition; `Bloc`'s event stream adds ceremony (event classes, `on<Event>` mapping) without buying anything until you need real event transformation (debounce/throttle/concurrency policies). Built on the same package, so the underlying mental model, unidirectional state with `BlocBuilder`/`BlocListener`, is identical.

## Why `get_it` with manual registration, no `injectable`

DI is registered explicitly in `lib/core/di/injection.dart`. A few more lines per dependency, no code generation step, and arguably easier to read than generated `injection.config.dart` output.

## Why `Either<Failure, T>` (fpdart) instead of exceptions

Repositories never throw across the domain boundary. Data sources throw typed exceptions (`ServerException`, `CacheException`, `NetworkException`); repositories catch those and return `Either<Failure, T>`, so every use case's success/failure path is explicit in its return type instead of hidden in a try/catch the caller has to remember to write.

## Why Freezed for `Failure`

`Failure` is a sealed class with one variant per failure kind (`ServerFailure`, `NetworkFailure`, `CacheFailure`, `UnexpectedFailure`), each carrying a message. Exhaustive `switch`/`map` on `Failure` means the analyzer catches a missing case at compile time instead of a silent fallthrough at runtime.

---

## Architecture: Feature-First Clean Architecture

Every feature lives under `lib/features/<feature_name>/` with strict layer separation:

```
lib/
  core/           # DI, networking, error handling, theming, routing; shared by every feature
  features/
    auth/         # Firebase email/password auth, the fullest example, read this one first
    home/         # Post-login landing page
    posts/        # REST CRUD via Dio, real Freezed+json_serializable model, Hive cache
  app.dart, bootstrap.dart, main_development.dart, main_production.dart
```

### Feature Structure

```
feature/
  data/
    datasources/   # Talks to the actual SDK/API. Throws typed exceptions, never returns Either.
    models/        # Maps the raw SDK/API shape to domain entities (JSON model, or a mapper)
    repositories/  # Implements the domain repository interface. Exceptions -> Either<Failure, T>.
  domain/
    entities/      # Plain value objects. No Flutter, no Firebase, no JSON.
    repositories/  # Abstract interfaces, the contract data/ implements.
    usecases/      # One class per business action. The only thing presentation/ is allowed to call.
  presentation/
    cubit/         # UI state for this feature.
    pages/         # Screens.
    widgets/       # Feature-local widgets.
```

### Dependency Direction

```
presentation  →  domain  ←  data
```

- `presentation` depends on `domain` (use cases, entities)
- `data` depends on `domain` (implements repository interfaces)
- `domain` depends on **nothing** external (no Flutter, no Firebase, no Dio)
- `domain` may only use `fpdart` and `freezed`

### Import Rules

```dart
// CORRECT: absolute package import
import 'package:flutter_enterprise_starter_kit/features/posts/domain/entities/post.dart';

// WRONG: relative import
import '../../domain/entities/post.dart';
```

---

## Where Business Logic Lives vs. UI

Business logic is not "wherever it fits" — it has a specific home per concern:

- **Business logic = use cases** (`domain/usecases/`), one class per action. A use case's `call()` just forwards to the repository interface; the actual logic (branch on connectivity, cache-then-return, map exceptions to failures) lives one layer down, in the **repository implementation** (`data/repositories/*_impl.dart`), not in the use case and not in the cubit.
- **Orchestration/UI state = cubits** (`presentation/cubit/`). A cubit calls one or more use cases and translates the `Either<Failure, T>` result into UI state; it holds no business rules of its own beyond "what should the screen show right now."
- **UI = pages/widgets** (`presentation/pages/`, `presentation/widgets/`). Zero business logic. A page's `build()` only lays out widgets and reads/reacts to cubit state; it never calls a repository, use case, or data source directly, and never contains a conditional business rule.
- **Data shaping = models** (`data/models/`). JSON parsing or SDK-object-to-entity mapping lives here, never inline in a repository.

---

## State Management: Cubit-Only

### State Definition (Freezed Sealed Class)

```dart
@freezed
sealed class PostsState with _$PostsState {
  const factory PostsState.initial() = PostsInitial;
  const factory PostsState.loading() = PostsLoading;
  const factory PostsState.loaded(List<Post> posts) = PostsLoaded;
  const factory PostsState.error(String message) = PostsError;
}
```

### Cubit Implementation

```dart
class PostsCubit extends Cubit<PostsState> {
  PostsCubit(this._getPosts) : super(const PostsState.initial());
  final GetPosts _getPosts;

  Future<void> load() async {
    emit(const PostsState.loading());
    final result = await _getPosts(const NoParams());
    result.match(
      (failure) => emit(PostsState.error(_messageFor(failure))),
      (posts) => emit(PostsState.loaded(posts)),
    );
  }

  String _messageFor(Failure failure) => failure.map(
    server: (e) => e.message,
    network: (_) => 'No internet connection',
  );
}
```

### State Reading in Widgets

```dart
// Exhaustive switch (PREFERRED)
return switch (state) {
  PostsInitial() || PostsLoading() => const CircularProgressIndicator(),
  PostsError(:final message) => Center(child: Text(message)),
  PostsLoaded(:final posts) => _PostList(posts),
};

// WRONG: type check
if (state is PostsLoaded) { ... }
```

---

## Dependency Injection: GetIt

### Registration Conventions

| Type | Registration | Reason |
|------|-------------|--------|
| Data sources | `registerLazySingleton` | One instance, lazily created |
| Repositories | `registerLazySingleton` | One instance, lazily created |
| Use cases | `registerLazySingleton` | One instance, lazily created |
| Screen-scoped Cubits | `registerFactory` | New instance per navigation |
| App-wide Cubits | `registerLazySingleton` | Shared across the app |

### Per-Feature Injection

```dart
// features/posts/posts_injection.dart
void configurePostsDependencies() {
  getIt
    ..registerLazySingleton<PostRemoteDataSource>(
      () => PostRemoteDataSourceImpl(getIt<Dio>()),
    )
    ..registerLazySingleton<PostLocalDataSource>(
      () => PostLocalDataSourceImpl(),
    )
    ..registerLazySingleton<PostRepository>(
      () => PostRepositoryImpl(
        remoteDataSource: getIt<PostRemoteDataSource>(),
        localDataSource: getIt<PostLocalDataSource>(),
        networkInfo: getIt<NetworkInfo>(),
      ),
    )
    ..registerLazySingleton<GetPosts>(
      () => GetPosts(getIt<PostRepository>()),
    )
    ..registerFactory<PostsCubit>(
      () => PostsCubit(getIt<GetPosts>()),
    );
}
```

Called from `core/di/injection.dart`:

```dart
Future<void> configureDependencies() async {
  // Core registrations...
  configureAuthDependencies();
  await configurePostsDependencies();
}
```

---

## Page Construction: Two-Widget Pattern

```dart
// PUBLIC: wires DI + BlocProvider
class PostsListPage extends StatelessWidget {
  const PostsListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) {
        final cubit = getIt<PostsCubit>();
        unawaited(cubit.load());  // Trigger loading here
        return cubit;
      },
      child: const _PostsListView(),
    );
  }
}

// PRIVATE: builds the actual UI
class _PostsListView extends StatelessWidget {
  const _PostsListView();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Posts')),
      body: BlocBuilder<PostsCubit, PostsState>(
        builder: (context, state) {
          return switch (state) {
            PostsInitial() || PostsLoading() => const Center(
              child: CircularProgressIndicator(),
            ),
            PostsError(:final message) => Center(
              child: Text(message),
            ),
            PostsLoaded(:final posts) => RefreshIndicator(
              onRefresh: () async => context.read<PostsCubit>().load(),
              child: ListView.builder(
                itemCount: posts.length,
                itemBuilder: (context, index) => PostTile(post: posts[index]),
              ),
            ),
          };
        },
      ),
    );
  }
}
```

---

## Error Handling: fpdart Either

```dart
// Use case returns Either
class GetPosts extends UseCase<List<Post>, NoParams> {
  GetPosts(this._repository);
  final PostRepository _repository;

  @override
  Future<Either<Failure, List<Post>>> call(NoParams params) async {
    return _repository.getPosts();
  }
}

// Repository catches and returns Either
class PostRepositoryImpl implements PostRepository {
  @override
  Future<Either<Failure, List<Post>>> getPosts() async {
    try {
      final models = await _remoteDataSource.getPosts();
      await _localDataSource.cachePosts(models);
      return Right(models.map((m) => m.toEntity()).toList());
    } on ServerException catch (e) {
      return Left(Failure.server(e.message));
    } on NetworkException {
      return const Left(Failure.network('No internet connection'));
    }
  }
}

// Cubit pattern-matches the Either
result.match(
  (failure) => emit(PostsState.error(_messageFor(failure))),
  (posts) => emit(PostsState.loaded(posts)),
);
```

---

## Auth Request Walkthrough

Tapping "Sign in" on `LoginPage`:

1. `LoginCubit.submit()` emits `LoginState.submitting()`, then calls the `SignInWithEmailAndPassword` use case.
2. The use case forwards to `AuthRepository.signInWithEmailAndPassword()`. It only knows the abstract interface, not that `AuthRepositoryImpl` (Firebase-backed) is behind it.
3. `AuthRepositoryImpl` calls `AuthRemoteDataSource`, which calls `FirebaseAuth` directly. Any `FirebaseAuthException` is caught there and rethrown as a typed `ServerException`.
4. Back in `AuthRepositoryImpl`, that exception becomes `Left(Failure.server(message))`; success becomes `Right(user.toDomain())`.
5. `LoginCubit` pattern-matches the `Either` and emits `LoginState.failure(...)` or `LoginState.success()`.

Note what's not in this list: navigation. `LoginCubit` never calls `Navigator`/`GoRouter` directly. Instead, `AuthRepositoryImpl.authStateChanges` wraps Firebase's own `authStateChanges()` stream, `AuthCubit` (a single long-lived instance provided at the app root) subscribes to it for the app's whole lifetime, and `go_router`'s `redirect` re-evaluates automatically whenever `AuthCubit` emits.

---

## Posts Feature: Cache-Aside Reads, Remote-Only Writes

`PostRepositoryImpl.getPosts()` branches on `NetworkInfo.isConnected`:
- **Online**: fetches from `PostRemoteDataSource` (Dio against JSONPlaceholder), writes the result into `PostLocalDataSource` (a Hive box), then returns it.
- **Offline**: skips the network entirely and reads whatever was last cached, returning `Left(Failure.cache(...))` only if nothing has been cached yet.
- `createPost`/`updatePost`/`deletePost` are remote-only, there's no offline write queue.

---

## Navigation: GoRouter

```dart
// Route paths as constants
abstract class RoutePaths {
  static const root = '/';
  static const login = '/login';
  static const posts = '/posts';
  static String postDetailPath(int id) => '/posts/$id';
}

// Navigation calls
context.push(RoutePaths.postDetailPath(post.id));
context.go(RoutePaths.posts);
```

---

## Theme: Material 3

```dart
// app_colors.dart - Centralized tokens
abstract class AppColors {
  static const seed = Color(0xFF3D5AFE);
  static const success = Color(0xFF2E7D32);
  static const warning = Color(0xFFF9A825);
  static const error = Color(0xFFC62828);
}

// app_theme.dart - Material 3 with ColorScheme.fromSeed
abstract class AppTheme {
  static ThemeData get light => _themeFrom(Brightness.light);
  static ThemeData get dark => _themeFrom(Brightness.dark);
}

// app_text_styles.dart - Named text styles
abstract class AppTextStyles {
  static TextStyle title(BuildContext context) =>
      Theme.of(context).textTheme.headlineSmall!.copyWith(fontWeight: FontWeight.bold);
  static TextStyle body(BuildContext context) =>
      Theme.of(context).textTheme.bodyMedium!;
  static TextStyle caption(BuildContext context) =>
      Theme.of(context).textTheme.bodySmall!.copyWith(
        color: Theme.of(context).hintColor,
      );
}
```

---

## Testing Convention

Tests mirror `lib/`'s structure 1:1 under `test/`, e.g.
`lib/features/posts/presentation/cubit/posts_cubit.dart` ->
`test/features/posts/presentation/cubit/posts_cubit_test.dart`.

### Cubit Tests (mock use case, one layer down)

```dart
class _MockGetPosts extends Mock implements GetPosts {}

blocTest<PostsCubit, PostsState>(
  'emits [loading, loaded] when getPosts succeeds',
  build: () => PostsCubit(mockGetPosts),
  setUp: () {
    when(() => mockGetPosts(any())).thenAnswer(
      (_) async => const Right([post]),
    );
  },
  act: (cubit) => cubit.load(),
  expect: () => const [
    PostsState.loading(),
    PostsState.loaded([post]),
  ],
);
```

### Repository Tests (mock datasource, one layer down)

```dart
class _MockRemoteDataSource extends Mock implements PostRemoteDataSource {}
class _MockLocalDataSource extends Mock implements PostLocalDataSource {}
class _MockNetworkInfo extends Mock implements NetworkInfo {}

test('online: fetches remote, caches, returns domain posts', () async {
  when(() => networkInfo.isConnected).thenAnswer((_) async => true);
  when(() => remoteDataSource.getPosts()).thenAnswer((_) async => [postModel]);
  when(() => localDataSource.cachePosts(any())).thenAnswer((_) async {});

  final result = await repository.getPosts();

  result.match(
    (failure) => fail('expected Right, got Left($failure)'),
    (posts) => expect(posts, equals(const [post])),
  );
  verify(() => localDataSource.cachePosts([postModel])).called(1);
});
```

---

## Coding Rules

### Language & Type Safety

- **Never use `var` or `dynamic`.** Declare an explicit type, or let strong inference apply to a `final` with an unambiguous right-hand side.
- **Always prefer `final` over mutable locals.** Only use a non-final local when the variable is genuinely reassigned.
- **Null safety is not optional.** Model absence with `?` and handle it explicitly. Never use the `!` bang operator to silence the analyzer.
- Use `const` constructors for every value object (`Failure`, `User`, `NoParams`, exceptions).

### Naming Conventions

| Type | Convention | Example |
|------|-----------|---------|
| Classes/types | `UpperCamelCase` | `PostsCubit`, `LoginState` |
| Cubits | `<Feature>Cubit` | `PostsCubit`, `LoginCubit` |
| States | `<Feature>State` (sealed) | `PostsState.initial()`, `PostsState.loaded()` |
| Use cases | Verb phrase | `GetPosts`, `SignInWithEmailAndPassword` |
| Params | `<UseCase>Params` | `CreatePostParams`, `SignInWithEmailAndPasswordParams` |
| Files | `snake_case.dart` | `posts_cubit.dart` → `PostsCubit` |
| Private widgets | `_` prefix | `_PostsListView`, `_demoUserId` |
| Booleans | Predicate | `isConnected`, `isAuthenticated` |
| Interfaces | Plain name | `AuthRepository`, `NetworkInfo` |
| Implementations | Name + `Impl` | `AuthRepositoryImpl`, `NetworkInfoImpl` |

### Const Correctness

- Every widget, literal, or constructor call that can be `const`, must be `const`.
- Every `StatelessWidget` must have a `const` constructor.
- When a widget has no parameters beyond `key`, its call site should use `const` explicitly.

### Imports & Structure

- Always use full `package:flutter_enterprise_starter_kit/...` imports for cross-directory project code (not relative `../../` imports).
- One public class per file, file named after it in `snake_case`.
- `part`/`part of` only for generated Freezed/`json_serializable` output. Never hand-edit a generated file.

### Formatting

- Format with `dart format` defaults.
- Cascades (`..registerLazySingleton(...)`) over repeated `getIt.register...` statements.
- No `print()` anywhere in `lib/`. Use a proper logging interceptor/service.

---

## Commands

```bash
flutter pub get
dart run build_runner build --delete-conflicting-outputs   # Regenerate after @freezed/@JsonSerializable changes
flutter run -t lib/main_development.dart                   # Run dev flavor
flutter test                                                # Run all tests
flutter test test/path/to/some_test.dart                    # Run single test
flutter analyze                                              # Lint
dart format .                                               # Format
```
