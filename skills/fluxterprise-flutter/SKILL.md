---

name: fluxterprise-flutter
description: "Flutter enterprise quality gate. Dart shorthand, architecture, code quality, reuse, memory. Load with the core."
allowed-tools: Read Write Edit Glob Grep
---

> Created by **Candra Prasetya**

# fluxterprise-flutter

> Flutter Enterprise Quality Gate

> Part of the fluxterprise system. Read together with `fluxterprise/SKILL.md` (the core). This skill enforces Flutter-specific craft: Dart shorthand, clean architecture, code consistency, reusable components, and minimal memory. Load it when the task builds or edits any Flutter screen, widget, cubit, or theme.

## How to use this skill

- Load together with `fluxterprise/SKILL.md` whenever the task touches Flutter code. The core holds the mechanism (the purpose test, the three tiers, the Quality Gate); this skill holds Flutter-specific depth.
- Every entry has the same shape: **Tell** (the pattern), **Why** (why it falls below the gate), **Fix** (what to do instead), with the governing core rule cited as FG-XX or FR-XX.
- This skill assumes the enterprise starter kit architecture: feature-first clean architecture, Cubit-only state management, GetIt DI, GoRouter navigation, freezed sealed states, fpdart Either for error handling.
- The Quality Gate in the core remains the gate. The "Flutter Skill Checklist" at the end of this file is the Flutter-specific supplement to run alongside it.

---


## Part 0: Project Scaffold Protocol (MUST follow for new projects)

When building a new Flutter project from scratch, follow this exact order. **Do NOT skip steps. Do NOT create empty folders.**

```
PHASE 1: PROJECT SETUP
  ├── 1. flutter create --org com.example --platforms android,ios,web,macos,windows,linux <app_name>
  ├── 2. Add dependencies to pubspec.yaml (flutter_bloc, get_it, go_router, fpdart, freezed, dio, hive_ce, etc.)
  ├── 3. Create analysis_options.yaml (very_good_analysis or custom strict rules)
  ├── 4. Run flutter pub get
  └── 5. Create lib/ structure (see below)

PHASE 2: CORE SETUP (lib/core/) — ALL files must have real code
  ├── 1. error/exceptions.dart        → ServerException, CacheException, NetworkException
  ├── 2. error/failures.dart          → @freezed sealed class Failure
  ├── 3. usecase/usecase.dart         → abstract class UseCase<Type, Params>
  ├── 4. network/network_info.dart    → abstract class NetworkInfo
  ├── 5. network/network_info_impl.dart → Wraps connectivity_plus
  ├── 6. network/dio_client.dart      → createDioClient() with interceptors
  ├── 7. di/injection.dart            → GetIt instance + configureDependencies()
  ├── 8. router/app_router.dart       → GoRouter configuration
  ├── 9. router/route_paths.dart      → Route path constants
  ├── 10. theme/app_colors.dart       → Centralized color tokens
  ├── 11. theme/app_text_styles.dart  → Named text styles
  ├── 12. theme/app_theme.dart        → Material 3 ThemeData
  └── 13. Run dart format .

PHASE 3: FIRST FEATURE (e.g., auth) — follow 5-step workflow below
  ├── Domain → Data → DI → Presentation → Wiring
  ├── Every file has real code, no placeholders
  └── Run flutter test to verify

PHASE 4: ADDITIONAL FEATURES — one at a time, all 5 steps each

PHASE 5: POLISH
  ├── 1. i18n setup (gen_l10n, ARB files)
  ├── 2. Reusable components (AppButton, AppTextField, etc.)
  ├── 3. Error/empty/loading states for every screen
  └── 4. Cross-platform testing
```

**ENFORCEMENT:**
- [ ] Every folder created MUST contain at least one file with real code
- [ ] No empty `__init.dart__` or placeholder files
- [ ] Domain layer MUST be complete before data layer starts
- [ ] Data layer MUST be complete before presentation layer starts
- [ ] Each feature MUST pass tests before moving to the next feature

---

## Part 1: Dart Shorthand & Modern Syntax

Use modern Dart 3+ syntax. Write less code that reads clearer.

### Record Types (not Map<String, dynamic>)

```dart
// WRONG
Map<String, dynamic> getUser() {
  return {'name': 'Andi', 'age': 25};
}

// CORRECT
(String name, int age) getUser() {
  return ('Andi', 25);
}
```

### Pattern Matching & Destructuring

```dart
// WRONG
if (state is Loaded) {
  final posts = state.posts;
  final count = state.count;
}

// CORRECT
if (state case Loaded(:final posts, :final count)) {
  // use posts, count
}
```

### Switch Expressions (not switch statements)

```dart
// WRONG
String getEmoji(String status) {
  switch (status) {
    case 'active':
      return '🟢';
    case 'inactive':
      return '🔴';
    default:
      return '⚪';
  }
}

// CORRECT
String getEmoji(String status) => switch (status) {
  'active' => '🟢',
  'inactive' => '🔴',
  _ => '⚪',
};
```

### MediaQuery Performance

```dart
// WRONG: triggers rebuild on ANY MediaQuery change (size, padding, orientation, etc.)
final width = MediaQuery.of(context).size.width;

// CORRECT: only rebuilds when size changes
final width = MediaQuery.sizeOf(context).size.width;

// CORRECT: only rebuilds when padding changes
final padding = MediaQuery.paddingOf(context);

// CORRECT: only rebuilds when orientation changes
final orientation = MediaQuery.orientationOf(context);
```

**Why this matters:** `MediaQuery.of(context)` creates a dependency on the entire `MediaQueryData` object. When the keyboard opens, when the device rotates, when the status bar changes — any of these trigger a rebuild of every widget that used `MediaQuery.of(context)`. The specific accessors (`sizeOf`, `paddingOf`, `orientationOf`) only trigger rebuilds when their specific value changes.

**Rule of thumb:** if you only need the width, use `MediaQuery.sizeOf(context).width`. Never use `MediaQuery.of(context)` unless you genuinely need multiple values.

### Enhanced Enums

```dart
// WRONG
class UserRole {
  static const int admin = 0;
  static const int editor = 1;
  static const int viewer = 2;
}

// CORRECT
enum UserRole {
  admin(label: 'Admin', color: Color(0xFFE53935)),
  editor(label: 'Editor', color: Color(0xFF1E88E5)),
  viewer(label: 'Viewer', color: Color(0xFF43A047));

  const UserRole({required this.label, required this.color});
  final String label;
  final Color color;
}
```

### Collection-if & Collection-for

```dart
// WRONG
final items = <Widget>[];
items.add(const SizedBox(height: 8));
if (showHeader) items.add(const Header());
for (final post in posts) items.add(PostTile(post: post));

// CORRECT
final items = [
  const SizedBox(height: 8),
  if (showHeader) const Header(),
  for (final post in posts) PostTile(post: post),
];
```

### Late & Late Final

```dart
// WRONG
class MyService {
  Database? _db;
  
  Database get db {
    _db ??= Database.open();
    return _db!;
  }
}

// CORRECT
class MyService {
  late final Database _db = Database.open();
}
```

### Null Safety Patterns

```dart
// WRONG
final name = user?.profile?.name ?? 'Unknown';

// CORRECT (when the fallback is a real default)
final name = switch (user?.profile?.name) {
  final n? => n,
  _ => 'Unknown',
};
```

### Sealed Classes (not type hierarchy)

```dart
// WRONG
abstract class Result {}
class Success extends Result { final dynamic data; Success(this.data); }
class Failure extends Result { final String message; Failure(this.message); }

// CORRECT
sealed class Result<T> {
  const Result();
}

class Success<T> extends Result<T> {
  final T data;
  const Success(this.data);
}

class Failure<T> extends Result<T> {
  final String message;
  const Failure(this.message);
}
```

### Extension Methods

```dart
// WRONG (scattered helper functions)
String formatDate(DateTime d) => '${d.day}/${d.month}/${d.year}';
bool get isAndroid => Platform.isAndroid;

// CORRECT
extension DateTimeX on DateTime {
  String get short => '$day/$month/$year';
  bool get isToday => DateUtils.isSameDay(this, DateTime.now());
}

extension PlatformX on BuildContext {
  bool get isMobile => MediaQuery.sizeOf(this).width < 600;
  bool get isTablet => MediaQuery.sizeOf(this).width >= 600 && MediaQuery.sizeOf(this).width < 1200;
  bool get isDesktop => MediaQuery.sizeOf(this).width >= 1200;
}
```

---


## Part 2: Architecture & Code Consistency

Based on the [Flutter Enterprise Starter Kit](https://github.com/nicolinx/flutter_enterprise_starter_kit).

### Why Clean Architecture

Each feature is split into `data` / `domain` / `presentation`, and dependencies only point inward: `presentation` depends on `domain`, `data` implements `domain`'s interfaces, and `domain` depends on nothing external (no Flutter, no Firebase, no Dio). This is what makes the codebase testable and lets a data source change (REST to GraphQL, Firestore to Supabase) without touching domain or UI code.

### CRITICAL: Implementation Workflow (MUST follow in order)

**NEVER skip steps. NEVER create empty folders. NEVER jump to UI before domain is complete.**

For EVERY new feature, follow this exact order:

```
Step 1: DOMAIN LAYER (no Flutter, no external packages except fpdart/freezed)
  ├── 1a. Create entities/     → Plain value objects with const constructors
  ├── 1b. Create repositories/ → Abstract interfaces only (no implementation)
  └── 1c. Create usecases/     → One class per business action, calls repository

Step 2: DATA LAYER (implements domain interfaces)
  ├── 2a. Create models/       → @freezed + @JsonSerializable DTOs, with toEntity()
  ├── 2b. Create datasources/  → Talks to API/SDK, throws typed exceptions
  └── 2c. Create repositories/ → Implements domain interfaces, catches exceptions → Either

Step 3: DI WIRING
  └── 3a. Create <feature>_injection.dart → Register all dependencies with GetIt

Step 4: PRESENTATION LAYER (depends on domain only)
  ├── 4a. Create cubit/        → Calls use cases, emits sealed states
  ├── 4b. Create pages/        → Two-widget pattern (Page + View)
  └── 4c. Create widgets/      → Feature-local, data-driven, no cubit reference

Step 5: CORE WIRING
  ├── 5a. Add routes to app_router.dart
  ├── 5b. Call configure<Feature>Dependencies() from injection.dart
  └── 5c. Run build_runner if any @freezed/@JsonSerializable changed
```

**ENFORCEMENT RULES:**

- [ ] **No empty folders.** If you create a directory, you MUST put at least one file in it. A folder with zero files is a FAIL.
- [ ] **Domain first, always.** Never write a cubit before the use case exists. Never write a use case before the repository interface exists.
- [ ] **One feature at a time.** Complete ALL 5 steps for one feature before starting the next.
- [ ] **No shortcuts.** Do not put business logic in cubits. Do not put API calls in widgets. Do not skip the use case layer.
- [ ] **Every file has real code.** No placeholder files, no `// TODO: implement later`, no empty classes.

### Feature-First Structure

Every feature lives under `lib/features/<feature_name>/` with strict layer separation:

```
lib/
  core/
    di/
      injection.dart            # DI configuration, called from all features
    error/
      exceptions.dart           # Typed exceptions (ServerException, CacheException, NetworkException)
      failures.dart             # Freezed sealed Failure class (ServerFailure, NetworkFailure, etc.)
    network/
      network_info.dart         # Abstract interface
      network_info_impl.dart    # Wraps connectivity_plus
      interceptors/
        error_interceptor.dart  # Normalizes DioException into typed exceptions
        logging_interceptor.dart
        retry_interceptor.dart  # Exponential backoff for transient failures
    feature_flags/
      feature_flag.dart         # Enum of known flags
      feature_flags.dart        # Abstract interface
      feature_flags_impl.dart   # Firebase Remote Config + Hive local override
    router/
      app_router.dart
      route_paths.dart
    theme/
      app_colors.dart
      app_text_styles.dart
      app_theme.dart
    usecase/
      usecase.dart              # abstract class UseCase<Type, Params>
  features/
    auth/
      auth_injection.dart
      data/
        datasources/
          auth_remote_data_source.dart    # Calls FirebaseAuth directly, throws typed exceptions
        models/
          user_mapper.dart                # Firebase User → domain User (extension, not Freezed)
        repositories/
          auth_repository_impl.dart       # Catches exceptions, returns Either<Failure, T>
      domain/
        entities/
          user.dart                       # Plain value object, no Flutter
        repositories/
          auth_repository.dart            # Abstract interface
        usecases/
          sign_in_with_email_and_password.dart
          sign_out.dart
      presentation/
        cubit/
          auth_cubit.dart                 # App-wide, subscribes to authStateChanges
          login_cubit.dart                # Screen-scoped, calls use cases
        pages/
          login_page.dart                 # Public: wires DI + BlocProvider
          login_view.dart                 # Private: builds UI
        widgets/
          auth_text_field.dart            # Feature-local, data-driven
    posts/
      posts_injection.dart
      data/
        datasources/
          post_remote_data_source.dart    # Dio, throws typed exceptions
          post_local_data_source.dart     # Hive, stores toJson() maps
        models/
          post_model.dart                 # @freezed + @JsonSerializable DTO
        repositories/
          post_repository_impl.dart       # Cache-aside reads, remote-only writes
      domain/
        entities/
          post.dart
        repositories/
          post_repository.dart
        usecases/
          get_posts.dart
          create_post.dart
      presentation/
        cubit/
          posts_cubit.dart
          post_form_cubit.dart
        pages/
          posts_list_page.dart
          post_form_page.dart
        widgets/
          post_tile.dart
    home/
      # Minimal placeholder, intentionally thin
  app.dart
  bootstrap.dart
  main_development.dart
  main_production.dart
```

### Dependency Direction (strict)

```
presentation  →  domain  ←  data
```

- `presentation` depends on `domain` only (use cases, entities)
- `data` depends on `domain` only (implements repository interfaces)
- `domain` depends on **nothing** external (no Flutter, no Firebase, no Dio)
- `domain` may only use `fpdart` and `freezed`

### Where Business Logic Lives

- **Business logic = use cases** (`domain/usecases/`), one class per action. A use case's `call()` just forwards to the repository interface; the actual logic (branch on connectivity, cache-then-return, map exceptions to failures) lives one layer down, in the **repository implementation** (`data/repositories/*_impl.dart`), not in the use case and not in the cubit.
- **Orchestration/UI state = cubits** (`presentation/cubit/`). A cubit calls one or more use cases and translates the `Either<Failure, T>` result into UI state; it holds no business rules of its own beyond "what should the screen show right now."
- **UI = pages/widgets** (`presentation/pages/`, `presentation/widgets/`). Zero business logic. A page's `build()` only lays out widgets and reads/reacts to cubit state; it never calls a repository, use case, or data source directly.
- **Data shaping = models** (`data/models/`). JSON parsing or SDK-object-to-entity mapping lives here, never inline in a repository.

### Error Handling: Data Sources Throw, Repositories Catch

```dart
// Data source: throws typed exceptions, never returns Either
class PostRemoteDataSourceImpl implements PostRemoteDataSource {
  @override
  Future<List<PostModel>> getPosts() async {
    try {
      final response = await _dio.get('/posts');
      return (response.data as List).map((j) => PostModel.fromJson(j)).toList();
    } on DioException catch (e) {
      throw ServerException(e.message ?? 'Server error');
    }
  }
}

// Repository: catches exceptions, returns Either<Failure, T>
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
    } on CacheException {
      return const Left(Failure.cache('No cached data'));
    }
  }
}

// Use case: never try/catch, just forwards to repository
class GetPosts extends UseCase<List<Post>, NoParams> {
  GetPosts(this._repository);
  final PostRepository _repository;

  @override
  Future<Either<Failure, List<Post>>> call(NoParams params) async {
    return _repository.getPosts();
  }
}

// Cubit: pattern-matches the Either, never try/catch
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

  String _messageFor(Failure failure) => switch (failure) {
    ServerFailure(:final message) => message,
    NetworkFailure() => 'No internet connection',
    CacheFailure() => 'Data is stale, showing last known',
  };
}
```

### Import Rules (strict)

```dart
// CORRECT: absolute package import
import 'package:flutter_enterprise_starter_kit/features/posts/domain/entities/post.dart';

// WRONG: relative import
import '../../domain/entities/post.dart';
```

### Naming Conventions (strict)

| Type | Convention | Example |
|------|-----------|---------|
| Feature folder | `snake_case` | `posts`, `user_profile` |
| Widget file | `snake_case` | `post_tile.dart`, `login_page.dart` |
| Cubit file | `snake_case` with `_cubit.dart` | `posts_cubit.dart` |
| State file | `snake_case` with `_state.dart` | `posts_state.dart` |
| Use case file | `snake_case` | `get_posts.dart`, `sign_in_with_email_and_password.dart` |
| Use case class | Verb phrase, `UpperCamelCase` | `GetPosts`, `SignInWithEmailAndPassword` |
| Params class | `<UseCase>Params` | `CreatePostParams` (lives in same file as use case) |
| Widget class | `PascalCase` | `PostTile`, `LoginPage` |
| Cubit class | `<Feature>Cubit` | `PostsCubit`, `LoginCubit` |
| State class | `<Feature>State` (sealed) | `PostsState.initial()`, `PostsState.loaded()` |
| Interface | Plain name | `AuthRepository`, `NetworkInfo` |
| Implementation | Name + `Impl` | `AuthRepositoryImpl`, `NetworkInfoImpl` |
| Private widgets | `_` prefix | `_PostsListView`, `_demoUserId` |
| Booleans | Predicate | `isConnected`, `isAuthenticated` |
| File naming | One public class per file | `post_tile.dart` contains `PostTile` |

### Coding Rules (strict)

- **Never use `var` or `dynamic`.** Declare an explicit type, or let strong inference apply to a `final` with an unambiguous right-hand side.
- **Always prefer `final` over mutable locals.** Only use a non-final local when the variable is genuinely reassigned.
- **Null safety is not optional.** Model absence with `?` and handle it explicitly. Never use the `!` bang operator.
- **Every widget, literal, or constructor call that can be `const`, must be `const`.** This includes `SizedBox`, `Icon`, `Text('literal')`, `EdgeInsets.all(...)`.
- **Every `StatelessWidget` must have a `const` constructor.**
- **No `print()` anywhere in `lib/`.** Use a proper logging interceptor/service.
- **Format with `dart format` defaults.** Trailing commas drive multi-line argument wrapping.
- **Cascades** (`..registerLazySingleton(...)`) over repeated `getIt.register...` statements.

### Two-Widget Page Pattern (every page)

Trigger side effects (`unawaited(cubit.load())`) inside `BlocProvider.create`, not in `initState`/`build`.

```dart
// PUBLIC: wires DI + BlocProvider. Zero business logic.
class PostsListPage extends StatelessWidget {
  const PostsListPage({super.key});

  @override
  Widget build(BuildContext context) {
    return BlocProvider(
      create: (_) {
        final cubit = getIt<PostsCubit>();
        unawaited(cubit.load());  // Trigger loading here, not in initState
        return cubit;
      },
      child: const _PostsListView(),
    );
  }
}

// PRIVATE: builds the actual UI. Reads state, never calls repositories.
class _PostsListView extends StatelessWidget {
  const _PostsListView();

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Posts')),
      body: BlocBuilder<PostsCubit, PostsState>(
        builder: (context, state) => switch (state) {
          PostsInitial() || PostsLoading() => const Center(
            child: CircularProgressIndicator(),
          ),
          PostsError(:final message) => Center(
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Text(message),
                const SizedBox(height: 16),
                FilledButton.tonal(
                  onPressed: () => context.read<PostsCubit>().load(),
                  child: const Text('Retry'),
                ),
              ],
            ),
          ),
          PostsLoaded(:final posts) => RefreshIndicator(
            onRefresh: () async => context.read<PostsCubit>().load(),
            child: ListView.builder(
              itemCount: posts.length,
              itemBuilder: (context, index) => PostTile(post: posts[index]),
            ),
          ),
        },
      ),
    );
  }
}
```

### Cubit Pattern (every cubit)

Cubit methods are named after the user action, not the mechanism (`submit`, `load`, `delete`). Always emit a "working" state before the async call, then pattern-match the `Either` result.

```dart
@freezed
sealed class PostsState with _$PostsState {
  const factory PostsState.initial() = PostsInitial;
  const factory PostsState.loading() = PostsLoading;
  const factory PostsState.loaded(List<Post> posts) = PostsLoaded;
  const factory PostsState.error(String message) = PostsError;
}

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

  String _messageFor(Failure failure) => switch (failure) {
    ServerFailure(:final message) => message,
    NetworkFailure() => 'No internet connection',
    CacheFailure() => 'Data is stale, showing last known',
  };
}
```

### Use Case Pattern (every use case)

A use case's `call()` just forwards to the repository interface. The actual logic lives in the repository implementation.

```dart
class GetPosts extends UseCase<List<Post>, NoParams> {
  GetPosts(this._repository);
  final PostRepository _repository;

  @override
  Future<Either<Failure, List<Post>>> call(NoParams params) async {
    return _repository.getPosts();
  }
}
```

### Repository Pattern (every repository)

Data sources throw typed exceptions. Repositories catch and return `Either<Failure, T>`.

```dart
// Abstract interface (domain layer)
abstract class PostRepository {
  Future<Either<Failure, List<Post>>> getPosts();
  Future<Either<Failure, Post>> createPost(CreatePostParams params);
}

// Implementation (data layer)
class PostRepositoryImpl implements PostRepository {
  PostRepositoryImpl({
    required PostRemoteDataSource remoteDataSource,
    required PostLocalDataSource localDataSource,
    required NetworkInfo networkInfo,
  })  : _remoteDataSource = remoteDataSource,
        _localDataSource = localDataSource,
        _networkInfo = networkInfo;

  final PostRemoteDataSource _remoteDataSource;
  final PostLocalDataSource _localDataSource;
  final NetworkInfo _networkInfo;

  @override
  Future<Either<Failure, List<Post>>> getPosts() async {
    if (await _networkInfo.isConnected) {
      try {
        final models = await _remoteDataSource.getPosts();
        await _localDataSource.cachePosts(models);
        return Right(models.map((m) => m.toEntity()).toList());
      } on ServerException catch (e) {
        return Left(Failure.server(e.message));
      }
    } else {
      try {
        final cached = await _localDataSource.getCachedPosts();
        return Right(cached.map((m) => m.toEntity()).toList());
      } on CacheException {
        return const Left(Failure.cache('No cached data'));
      }
    }
  }
}
```

### Injection Pattern (every feature)

Every feature exposes a `configure<Feature>Dependencies()` top-level function in a `<feature>_injection.dart` file at the feature root.

```dart
// features/posts/posts_injection.dart
void configurePostsDependencies() {
  getIt
    // Data sources (lazy singleton)
    ..registerLazySingleton<PostRemoteDataSource>(
      () => PostRemoteDataSourceImpl(getIt<Dio>()),
    )
    ..registerLazySingleton<PostLocalDataSource>(
      () => PostLocalDataSourceImpl(),
    )
    // Repository (lazy singleton)
    ..registerLazySingleton<PostRepository>(
      () => PostRepositoryImpl(
        remoteDataSource: getIt<PostRemoteDataSource>(),
        localDataSource: getIt<PostLocalDataSource>(),
        networkInfo: getIt<NetworkInfo>(),
      ),
    )
    // Use cases (lazy singleton)
    ..registerLazySingleton<GetPosts>(
      () => GetPosts(getIt<PostRepository>()),
    )
    // Cubits (factory = new instance per navigation)
    ..registerFactory<PostsCubit>(
      () => PostsCubit(getIt<GetPosts>()),
    );
}
```

Called from `core/di/injection.dart`:
```dart
Future<void> configureDependencies() async {
  // Core registrations (Dio, NetworkInfo, etc.)
  configureAuthDependencies();
  await configurePostsDependencies();
}
```

### Auth Request Walkthrough

Tapping "Sign in" on `LoginPage`:

1. `LoginCubit.submit()` emits `LoginState.submitting()`, then calls the `SignInWithEmailAndPassword` use case.
2. The use case forwards to `AuthRepository.signInWithEmailAndPassword()`. It only knows the abstract interface, not that `AuthRepositoryImpl` (Firebase-backed) is behind it.
3. `AuthRepositoryImpl` calls `AuthRemoteDataSource`, which calls `FirebaseAuth` directly. Any `FirebaseAuthException` is caught there and rethrown as a typed `ServerException`.
4. Back in `AuthRepositoryImpl`, that exception becomes `Left(Failure.server(message))`; success becomes `Right(user.toDomain())`.
5. `LoginCubit` pattern-matches the `Either` and emits `LoginState.failure(...)` or `LoginState.success()`.

Note: `LoginCubit` never calls `Navigator`/`GoRouter` directly. Instead, `AuthCubit` (app-wide) subscribes to `authStateChanges`, and `go_router`'s `redirect` re-evaluates automatically.

### Posts Feature: Cache-Aside Reads, Remote-Only Writes

`PostRepositoryImpl.getPosts()` branches on `NetworkInfo.isConnected`:
- **Online**: fetches from `PostRemoteDataSource` (Dio), writes into `PostLocalDataSource` (Hive), then returns.
- **Offline**: reads cached data, returns `Left(Failure.cache(...))` only if nothing cached.
- `createPost`/`updatePost`/`deletePost` are remote-only, no offline write queue.

---


## Part 3: Reusable Components

### Extract Rules

**Extract when:**
- Build method exceeds ~80 lines
- Visual pattern repeats 2+ times
- A sub-section is independently testable
- Same widget appears in 2+ screens

**Do NOT extract when:**
- It's a one-off decoration (`_BuildDivider`, `_BuildSpacer`)
- The widget has no meaningful name
- It would create more files than value

### Component Architecture

```dart
// GOOD: data-driven, no dependencies
class PostTile extends StatelessWidget {
  const PostTile({required this.post, this.onTap});
  final Post post;
  final VoidCallback? onTap;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(post.title),
      subtitle: Text(post.body),
      onTap: onTap,
    );
  }
}

// BAD: knows too much, hard to reuse
class _PostTile extends StatelessWidget {
  const _PostTile(this.post);
  final Post post;

  @override
  Widget build(BuildContext context) {
    return ListTile(
      title: Text(post.title),
      subtitle: Text(post.body),
      onTap: () => context.push('/posts/${post.id}'),
      leading: CircleAvatar(
        child: Text(post.title[0]),
      ),
      trailing: IconButton(
        icon: const Icon(Icons.delete),
        onPressed: () => context.read<PostsCubit>().delete(post.id),
      ),
    );
  }
}
```

### Stateful Widget Extraction

When a widget needs local state (toggle, scroll position, animation controller), extract it:

```dart
// WRONG: state inside build
class ProductCard extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () {
        // setState not available in StatelessWidget
      },
      child: ...
    );
  }
}

// CORRECT: extracted StatefulWidget
class ProductCard extends StatelessWidget {
  const ProductCard({required this.product});
  final Product product;

  @override
  Widget build(BuildContext context) {
    return _ProductCardView(product: product);
  }
}

class _ProductCardView extends StatefulWidget {
  const _ProductCardView({required this.product});
  final Product product;

  @override
  State<_ProductCardView> createState() => _ProductCardViewState();
}

class _ProductCardViewState extends State<_ProductCardView> {
  bool _isExpanded = false;

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: () => setState(() => _isExpanded = !_isExpanded),
      child: AnimatedSize(
        duration: const Duration(milliseconds: 200),
        child: widget.product.description,
      ),
    );
  }
}
```

---


## Part 4: Memory Optimization

### Avoid These Anti-Patterns

| Anti-Pattern | Problem | Fix |
|-------------|---------|-----|
| `setState` in `BlocBuilder` | Double rebuild: Bloc rebuilds + setState rebuilds | Move local state to a separate StatefulWidget |
| `ListView.builder` with `itemCount: list.length` when list grows | Rebuilds entire list on append | Use `ListView.separated` or `SliverList` with keys |
| `Image.network` without caching | Downloads same image repeatedly | Use `cached_network_image` or `ImageCache` |
| `Timer` without cancel | Leaks memory | Always cancel in `dispose()` |
| `StreamSubscription` without cancel | Leaks memory | Always cancel in `dispose()` |
| `ScrollController` without dispose | Leaks memory | Always call `dispose()` in `State.dispose()` |
| `AnimationController` without dispose | Leaks memory | Always call `dispose()` in `State.dispose()` |
| Building widgets in `initState` | Unnecessary rebuilds | Use `late` or build in `build()` |
| `const` missing on immutable widgets | Creates new instance every rebuild | Always add `const` constructors |

### Const Everywhere

```dart
// WRONG: new instance every rebuild
class _PostsListView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        SizedBox(height: 16),        // new SizedBox every rebuild
        Text('Posts'),                // new Text every rebuild
        Icon(Icons.list),            // new Icon every rebuild
      ],
    );
  }
}

// CORRECT: const avoids allocation
class _PostsListView extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return const Column(
      children: [
        SizedBox(height: 16),
        Text('Posts'),
        Icon(Icons.list),
      ],
    );
  }
}
```

### Keys for Lists

```dart
// WRONG: no key, Flutter rebuilds wrong items
ListView.builder(
  itemCount: posts.length,
  itemBuilder: (_, i) => PostTile(post: posts[i]),
)

// CORRECT: key helps Flutter track items
ListView.builder(
  itemCount: posts.length,
  itemBuilder: (_, i) => PostTile(key: ValueKey(posts[i].id), post: posts[i]),
)
```

### Dispose Pattern

```dart
class _MyScreenState extends State<MyScreen> with SingleTickerProviderStateMixin {
  late final AnimationController _controller;
  late final ScrollController _scrollController;
  StreamSubscription? _subscription;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(vsync: this, duration: const Duration(seconds: 1));
    _scrollController = ScrollController();
    _subscription = stream.listen((_) {});
  }

  @override
  void dispose() {
    _controller.dispose();
    _scrollController.dispose();
    _subscription?.cancel();
    super.dispose();
  }
}
```

### Prevent Unnecessary Rebuilds

```dart
// WRONG: BlocBuilder rebuilds entire screen
BlocBuilder<AuthCubit, AuthState>(
  builder: (context, state) {
    return Scaffold(
      body: Column(children: [
        Header(),           // rebuilds even if only auth changed
        const PostList(),   // rebuilds even though it's const
      ]),
    );
  },
)

// CORRECT: rebuild only what needs to rebuild
Scaffold(
  body: Column(children: [
    BlocBuilder<AuthCubit, AuthState>(
      builder: (context, state) => Header(user: state.user),
    ),
    const PostList(),
  ]),
)
```

### Lazy Loading & Pagination

```dart
// WRONG: load everything at once
class PostsCubit extends Cubit<PostsState> {
  Future<void> load() async {
    final all = await _repository.getAllPosts(); // loads 10K posts
    emit(PostsState.loaded(all));
  }
}

// CORRECT: paginated loading
class PostsCubit extends Cubit<PostsState> {
  int _page = 0;
  bool _hasMore = true;

  Future<void> loadMore() async {
    if (!_hasMore) return;
    final result = await _repository.getPosts(page: _page, limit: 20);
    result.match(
      (failure) => emit(PostsState.error(_messageFor(failure))),
      (posts) {
        _hasMore = posts.length == 20;
        _page++;
        emit(PostsState.loaded([...?state.data, ...posts]));
      },
    );
  }
}
```

---


## Part 5: Sliver Patterns

Slivers are the foundation of complex scroll layouts in Flutter. Use them when `ListView` or `GridView` alone cannot express the layout.

### When to Use Slivers

| Pattern | Use Slivers? | Why |
|---------|-------------|-----|
| Simple list of items | No | `ListView.builder` is simpler and sufficient |
| Grid of items | No | `GridView.builder` is sufficient |
| Collapsing app bar + list | **Yes** | `SliverAppBar` + `SliverList` |
| Mixed content (header + list + grid) | **Yes** | `SliverToBoxAdapter` + `SliverList` + `SliverGrid` |
| Sticky headers | **Yes** | `SliverPersistentHeader` with `pinned: true` |
| Animated list transitions | **Yes** | `SliverAnimatedOpacity` or `SliverAnimatedPaintExtent` |

### Collapsing App Bar

```dart
CustomScrollView(
  slivers: [
    SliverAppBar(
      expandedHeight: 200,
      floating: false,
      pinned: true,
      flexibleSpace: FlexibleSpaceBar(
        title: Text('Posts'),
        background: Image.network(coverUrl, fit: BoxFit.cover),
      ),
    ),
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => PostTile(post: posts[index]),
        childCount: posts.length,
      ),
    ),
  ],
)
```

### Mixed Content Layout

```dart
CustomScrollView(
  slivers: [
    // Header section
    SliverToBoxAdapter(child: Header()),
    // Grid of featured items
    SliverGrid(
      delegate: SliverChildBuilderDelegate(
        (context, index) => FeaturedCard(item: items[index]),
        childCount: items.length,
      ),
      gridDelegate: SliverGridDelegateWithFixedCrossAxisCount(
        crossAxisCount: 2,
        childAspectRatio: 1.5,
      ),
    ),
    // List of recent items
    SliverList(
      delegate: SliverChildBuilderDelegate(
        (context, index) => RecentTile(item: recent[index]),
        childCount: recent.length,
      ),
    ),
  ],
)
```

### Sticky Header

```dart
SliverPersistentHeader(
  pinned: true,
  delegate: _StickyHeaderDelegate(
    child: Container(
      color: Theme.of(context).colorScheme.surface,
      padding: EdgeInsets.all(16),
      child: Text('Section Title', style: Theme.of(context).textTheme.titleLarge),
    ),
    maxHeight: 56,
    minHeight: 56,
  ),
)
```

### Sliver Performance Rules

| Rule | Why |
|------|-----|
| Use `SliverChildBuilderDelegate` over `SliverChildListDelegate` | Builder creates items lazily; List creates all items at once |
| Prefer `SliverList` over `SliverToBoxAdapter` wrapping a `ListView` | Nested scrollables break scroll physics and accessibility |
| Use `const` on sliver children | Zero allocation cost for static content |
| Avoid `SliverToBoxAdapter` for long content | If the content is longer than one screen, it should be a sliver itself |

---


## Part 6: Cross-Platform Patterns

### Platform Detection

```dart
// WRONG: hardcoded platform checks
if (Platform.isAndroid) {
  // android specific
} else if (Platform.isIOS) {
  // ios specific
}

// CORRECT: abstraction via design system
abstract class PlatformStyles {
  static PlatformStyles of(BuildContext context) {
    final platform = Theme.of(context).platform;
    return switch (platform) {
      TargetPlatform.android || TargetPlatform.fuchsia => AndroidStyles(),
      TargetPlatform.iOS => IosStyles(),
      TargetPlatform.macOS || TargetPlatform.linux || TargetPlatform.windows => DesktopStyles(),
    };
  }
  
  double get navBarHeight;
  EdgeInsets get screenPadding;
  Widget buildBackButton(BuildContext context);
}
```

### Adaptive Layout

```dart
// WRONG: single layout
class DashboardPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: Column(children: [
        const Header(),
        const StatsRow(),
        const PostList(),
      ]),
    );
  }
}

// CORRECT: adaptive based on screen size
class DashboardPage extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: LayoutBuilder(
        builder: (context, constraints) {
          if (constraints.maxWidth >= 1200) {
            return const _DesktopLayout();
          } else if (constraints.maxWidth >= 600) {
            return const _TabletLayout();
          }
          return const _MobileLayout();
        },
      ),
    );
  }
}

class _MobileLayout extends StatelessWidget {
  const _MobileLayout();
  @override
  Widget build(BuildContext context) => const Column(children: [Header(), StatsRow(), PostList()]);
}

class _TabletLayout extends StatelessWidget {
  const _TabletLayout();
  @override
  Widget build(BuildContext context) => const Row(children: [Expanded(child: Sidebar()), Expanded(flex: 3, child: PostList())]);
}

class _DesktopLayout extends StatelessWidget {
  const _DesktopLayout();
  @override
  Widget build(BuildContext context) => const Row(children: [Sidebar(), Expanded(flex: 3, child: PostList()), InfoPanel()]);
}
```

### Platform-Specific Widgets

```dart
// WRONG: ignore platform conventions
context.push('/settings');

// CORRECT: use platform-native navigation when appropriate
abstract class NavigationService {
  void push(BuildContext context, String route);
  void pop(BuildContext context);
}

class MobileNavigation implements NavigationService {
  @override
  void push(BuildContext context, String route) => context.push(route);
  @override
  void pop(BuildContext context) => context.pop();
}

class DesktopNavigation implements NavigationService {
  @override
  void push(BuildContext context, String route) => context.go(route);
  @override
  void pop(BuildContext context) => context.go('/');
}
```

### Safe Area Handling

```dart
// WRONG: hardcode padding
Padding(padding: EdgeInsets.only(top: MediaQuery.of(context).padding.top))

// CORRECT: use SafeArea or consumeMediaQuery
SafeArea(child: content)

// Or for custom cases:
Padding(
  padding: EdgeInsets.only(
    top: MediaQuery.viewPaddingOf(context).top,
    bottom: MediaQuery.viewPaddingOf(context).bottom,
  ),
  child: content,
)
```

---


## Part 7: Reusable Component Library

Build reusable components FIRST, then compose screens from them. Every component is data-driven, i18n-ready, and Material 3 compliant.

### Component Rules

1. **Data in, widgets out.** Components receive data via constructor. Never access cubits, repositories, or services inside a reusable widget.
2. **i18n from the start.** All user-facing strings go through `context.l10n`. No hardcoded strings.
3. **Material 3 theming.** Use `Theme.of(context)` for colors, text styles, and shapes. Never hardcode.
4. **Const constructors.** Every immutable widget has `const` constructor.
5. **Semantic labels.** Every interactive element has `Semantics` or `labelText`.

### Core Reusable Components

#### AppButton (all button variants)

```dart
class AppButton extends StatelessWidget {
  const AppButton({
    required this.label,
    required this.onPressed,
    this.variant = AppButtonVariant.filled,
    this.icon,
    this.isLoading = false,
    super.key,
  });

  final String label;
  final VoidCallback? onPressed;
  final AppButtonVariant variant;
  final IconData? icon;
  final bool isLoading;

  @override
  Widget build(BuildContext context) {
    final child = isLoading
        ? const SizedBox(
            width: 20, height: 20,
            child: CircularProgressIndicator(strokeWidth: 2),
          )
        : Text(label);

    return switch (variant) {
      AppButtonVariant.filled => icon != null
          ? FilledButton.icon(onPressed: onPressed, icon: Icon(icon), label: child)
          : FilledButton(onPressed: onPressed, child: child),
      AppButtonVariant.tonal => icon != null
          ? FilledButton.tonalIcon(onPressed: onPressed, icon: Icon(icon), label: child)
          : FilledButton.tonal(onPressed: onPressed, child: child),
      AppButtonVariant.outlined => icon != null
          ? OutlinedButton.icon(onPressed: onPressed, icon: Icon(icon), label: child)
          : OutlinedButton(onPressed: onPressed, child: child),
      AppButtonVariant.text => icon != null
          ? TextButton.icon(onPressed: onPressed, icon: Icon(icon), label: child)
          : TextButton(onPressed: onPressed, child: child),
    };
  }
}

enum AppButtonVariant { filled, tonal, outlined, text }
```

#### AppTextField (all input variants)

```dart
class AppTextField extends StatelessWidget {
  const AppTextField({
    required this.label,
    this.hint,
    this.helperText,
    this.errorText,
    this.controller,
    this.onChanged,
    this.onSubmitted,
    this.keyboardType,
    this.textInputAction,
    this.obscureText = false,
    this.enabled = true,
    this.maxLines = 1,
    this.prefixIcon,
    this.suffixIcon,
    super.key,
  });

  final String label;
  final String? hint;
  final String? helperText;
  final String? errorText;
  final TextEditingController? controller;
  final ValueChanged<String>? onChanged;
  final ValueChanged<String>? onSubmitted;
  final TextInputType? keyboardType;
  final TextInputAction? textInputAction;
  final bool obscureText;
  final bool enabled;
  final int? maxLines;
  final Widget? prefixIcon;
  final Widget? suffixIcon;

  @override
  Widget build(BuildContext context) {
    return TextField(
      controller: controller,
      onChanged: onChanged,
      onSubmitted: onSubmitted,
      keyboardType: keyboardType,
      textInputAction: textInputAction,
      obscureText: obscureText,
      enabled: enabled,
      maxLines: maxLines,
      decoration: InputDecoration(
        labelText: label,
        hintText: hint,
        helperText: helperText,
        errorText: errorText,
        prefixIcon: prefixIcon,
        suffixIcon: suffixIcon,
      ),
    );
  }
}
```

#### AppCard (consistent card with Material 3)

```dart
class AppCard extends StatelessWidget {
  const AppCard({
    required this.child,
    this.onTap,
    this.padding,
    this.elevation,
    super.key,
  });

  final Widget child;
  final VoidCallback? onTap;
  final EdgeInsetsGeometry? padding;
  final double? elevation;

  @override
  Widget build(BuildContext context) {
    final card = Card(
      elevation: elevation ?? 0,
      clipBehavior: Clip.antiAlias,
      child: Padding(
        padding: padding ?? const EdgeInsets.all(16),
        child: child,
      ),
    );

    if (onTap != null) {
      return InkWell(onTap: onTap, child: card);
    }
    return card;
  }
}
```

#### AppEmptyState (reusable empty state)

```dart
class AppEmptyState extends StatelessWidget {
  const AppEmptyState({
    required this.title,
    required this.message,
    this.icon = Icons.inbox_outlined,
    this.actionLabel,
    this.onAction,
    super.key,
  });

  final String title;
  final String message;
  final IconData icon;
  final String? actionLabel;
  final VoidCallback? onAction;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(icon, size: 64, color: Theme.of(context).colorScheme.outline),
            const SizedBox(height: 16),
            Text(title, style: Theme.of(context).textTheme.titleMedium, textAlign: TextAlign.center),
            const SizedBox(height: 8),
            Text(message, style: Theme.of(context).textTheme.bodyMedium?.copyWith(
              color: Theme.of(context).colorScheme.onSurfaceVariant,
            ), textAlign: TextAlign.center),
            if (actionLabel != null && onAction != null) ...[
              const SizedBox(height: 24),
              FilledButton(onPressed: onAction, child: Text(actionLabel!)),
            ],
          ],
        ),
      ),
    );
  }
}
```

#### AppErrorView (reusable error state)

```dart
class AppErrorView extends StatelessWidget {
  const AppErrorView({
    required this.message,
    this.onRetry,
    super.key,
  });

  final String message;
  final VoidCallback? onRetry;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(Icons.error_outline, size: 64, color: Theme.of(context).colorScheme.error),
            const SizedBox(height: 16),
            Text(message, style: Theme.of(context).textTheme.bodyLarge, textAlign: TextAlign.center),
            if (onRetry != null) ...[
              const SizedBox(height: 24),
              FilledButton.tonalIcon(
                onPressed: onRetry,
                icon: const Icon(Icons.refresh),
                label: Text(context.l10n.retry), // i18n
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

#### AppLoadingView (reusable loading state)

```dart
class AppLoadingView extends StatelessWidget {
  const AppLoadingView({this.message, super.key});

  final String? message;

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const CircularProgressIndicator(),
          if (message != null) ...[
            const SizedBox(height: 16),
            Text(message!, style: Theme.of(context).textTheme.bodyMedium),
          ],
        ],
      ),
    );
  }
}
```

#### AppConfirmDialog (reusable confirmation)

```dart
class AppConfirmDialog extends StatelessWidget {
  const AppConfirmDialog({
    required this.title,
    required this.message,
    this.confirmLabel,
    this.cancelLabel,
    this.isDestructive = false,
    super.key,
  });

  final String title;
  final String message;
  final String? confirmLabel;
  final String? cancelLabel;
  final bool isDestructive;

  static Future<bool> show(
    BuildContext context, {
    required String title,
    required String message,
    String? confirmLabel,
    String? cancelLabel,
    bool isDestructive = false,
  }) async {
    final result = await showDialog<bool>(
      context: context,
      builder: (_) => AppConfirmDialog(
        title: title,
        message: message,
        confirmLabel: confirmLabel,
        cancelLabel: cancelLabel,
        isDestructive: isDestructive,
      ),
    );
    return result ?? false;
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Text(title),
      content: Text(message),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context, false),
          child: Text(cancelLabel ?? context.l10n.cancel),
        ),
        if (isDestructive)
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            style: FilledButton.styleFrom(
              backgroundColor: Theme.of(context).colorScheme.error,
            ),
            child: Text(confirmLabel ?? context.l10n.confirm),
          )
        else
          FilledButton(
            onPressed: () => Navigator.pop(context, true),
            child: Text(confirmLabel ?? context.l10n.confirm),
          ),
      ],
    );
  }
}
```

---

## Part 8: i18n (Internationalization)

Every user-facing string must go through i18n from day one. No hardcoded strings in widget code.

### Setup: gen_l10n (Recommended)

```yaml
# pubspec.yaml
flutter:
  generate: true  # enables gen_l10n

dependencies:
  flutter_localizations:
    sdk: flutter
  intl: any

# l10n.yaml (project root)
arb-dir: lib/l10n
template-arb-file: app_en.arb
output-localization-file: app_localizations.dart
output-class: AppLocalizations
```

### ARB Files

```json
// lib/l10n/app_en.arb
{
  "@@locale": "en",
  "appTitle": "My App",
  "@appTitle": { "description": "The title of the application" },
  "hello": "Hello, {name}",
  "@hello": {
    "description": "A greeting with the user's name",
    "placeholders": { "name": { "type": "String" } }
  },
  "postCount": "{count, plural, =0{No posts} =1{1 post} other{{count} posts}}",
  "@postCount": {
    "description": "Number of posts",
    "placeholders": { "count": { "type": "int" } }
  },
  "retry": "Try again",
  "cancel": "Cancel",
  "confirm": "Confirm",
  "delete": "Delete",
  "save": "Save",
  "loading": "Loading...",
  "error": "Something went wrong",
  "emptyTitle": "No data yet",
  "emptyMessage": "Add your first item to see it here"
}

// lib/l10n/app_id.arb
{
  "@@locale": "id",
  "appTitle": "Aplikasi Saya",
  "hello": "Halo, {name}",
  "postCount": "{count, plural, =0{Tidak ada postingan} =1{1 postingan} other{{count} postingan}}",
  "retry": "Coba lagi",
  "cancel": "Batal",
  "confirm": "Konfirmasi",
  "delete": "Hapus",
  "save": "Simpan",
  "loading": "Memuat...",
  "error": "Terjadi kesalahan",
  "emptyTitle": "Belum ada data",
  "emptyMessage": "Tambahkan item pertama Anda di sini"
}
```

### Usage in Widgets

```dart
// Access via context.l10n
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Text(context.l10n.hello('Andi'));  // "Hello, Andi"
  }
}

// Pluralization
Text(context.l10n.postCount(5))  // "5 posts"

// In MaterialLocalizations
MaterialLocalizations.of(context).cancelButtonLabel  // system-provided
```

### Date & Number Formatting

```dart
import 'package:intl/intl.dart';

// Date (locale-aware)
final date = DateFormat.yMMMd(context.locale.toString()).format(DateTime.now());
// "Sep 18, 2026" (en) / "18 Sep 2026" (id)

// Number (locale-aware)
final price = NumberFormat.currency(locale: context.locale.toString(), symbol: 'Rp').format(150000);
// "Rp150.000" (id) / "Rp150,000" (en)

// Relative time
final time = DateFormat.Hm(context.locale.toString()).format(DateTime.now());
// "14:30" (24h) / "2:30 PM" (12h)
```

### Text Expansion Handling

```dart
// WRONG: fixed width, German text overflows
SizedBox(width: 100, child: Text(context.l10n.save))

// CORRECT: flexible width
Flexible(child: Text(context.l10n.save))
// Or use FittedBox for buttons
FittedBox(fit: BoxFit.scaleDown, child: Text(context.l10n.save))
```

### i18n Checklist

- [ ] `gen_l10n` configured in `pubspec.yaml` + `l10n.yaml`
- [ ] At least `app_en.arb` exists with all user-facing strings
- [ ] All widgets use `context.l10n.xxx` instead of hardcoded strings
- [ ] Plurals use `{count, plural, ...}` syntax
- [ ] Dates use `DateFormat` with locale
- [ ] Numbers use `NumberFormat` with locale
- [ ] Text expansion handled (no fixed-width text containers)

---

## Part 9: Flutter 3.xx Material 3 Latest

Flutter 3.22+ defaults to Material 3. Use the latest APIs.

### Material 3 Setup

```dart
// app_theme.dart
MaterialApp(
  theme: ThemeData(
    useMaterial3: true,
    colorSchemeSeed: AppColors.seed,  // from your design tokens
    // brightness: Brightness.dark,  // for dark mode
  ),
)
```

### Material 3 Widget Migration

| Material 2 (deprecated) | Material 3 (use this) |
|------------------------|----------------------|
| `ElevatedButton` | `FilledButton` / `FilledButton.tonal` |
| `BottomNavigationBar` | `NavigationBar` |
| `AppBar` (default) | `AppBar` with `centerTitle: true` (iOS) or `false` (Android) |
| `Card` with `elevation` | `Card` with `elevation: 0` + `surfaceTintColor` |
| `TextField` (default) | `TextField` with `InputDecoration` (Material 3 styling auto) |
| `Dialog` | `AlertDialog` / `Dialog.fullscreen` |
| `TabBar` | `TabBar` with `TabBarTheme` (Material 3 auto) |
| `Switch` | `Switch` (Material 3 auto, thumb shape changed) |
| `Checkbox` | `Checkbox` (Material 3 auto, rounded shape) |
| `Radio` | `Radio` (Material 3 auto, filled circle) |
| `Slider` | `Slider` (Material 3 auto, pill thumb) |
| `CircularProgressIndicator` | `CircularProgressIndicator` (Material 3 auto, thicker) |
| `LinearProgressIndicator` | `LinearProgressIndicator` (Material 3 auto, rounded) |
| `Chip` | `Chip` / `FilterChip` / `InputChip` (Material 3 auto) |
| `Drawer` | `NavigationDrawer` (Material 3) |
| `SnackBar` | `SnackBar` (Material 3 auto, rounded) |
| `BottomSheet` | `BottomSheet` / `DraggableScrollableSheet` |
| `SearchDelegate` | `SearchAnchor` / `SearchBar` |

### ColorScheme.fromSeed

```dart
// WRONG: manual color scheme
colorScheme: ColorScheme.fromSwatch(primarySwatch: Colors.blue)

// CORRECT: seed-based Material 3
colorScheme: ColorScheme.fromSeed(seedColor: AppColors.seed)

// Dark mode
colorScheme: ColorScheme.fromSeed(
  seedColor: AppColors.seed,
  brightness: Brightness.dark,
)
```

### Material 3 Typography

```dart
// WRONG: manual text theme
textTheme: TextTheme(headlineLarge: TextStyle(fontSize: 32))

// CORRECT: use Material 3 text theme + override only what's needed
textTheme: GoogleFonts.interTextTheme(
  Theme.of(context).textTheme,
).copyWith(
  headlineLarge: GoogleFonts.inter(fontSize: 32, fontWeight: FontWeight.w700),
)
```

### Material 3 Shapes

```dart
// Use ShapeDecoration for Material 3 shapes
ShapeDecoration(
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(12),  // Material 3 default
  ),
  color: Theme.of(context).colorScheme.surfaceContainerHighest,
)

// Or use CardShapeTheme
CardTheme(
  shape: RoundedRectangleBorder(
    borderRadius: BorderRadius.circular(12),
  ),
  elevation: 0,
)
```

### NavigationBar (Material 3)

```dart
// WRONG: BottomNavigationBar (Material 2)
BottomNavigationBar(
  currentIndex: index,
  onTap: onTap,
  items: [
    BottomNavigationBarItem(icon: Icon(Icons.home), label: 'Home'),
    BottomNavigationBarItem(icon: Icon(Icons.search), label: 'Search'),
  ],
)

// CORRECT: NavigationBar (Material 3)
NavigationBar(
  selectedIndex: index,
  onDestinationSelected: onTap,
  destinations: [
    NavigationDestination(icon: Icon(Icons.home_outlined), label: context.l10n.home),
    NavigationDestination(icon: Icon(Icons.search_outlined), label: context.l10n.search),
  ],
)
```

### SearchAnchor (Material 3)

```dart
// WRONG: custom search implementation
TextField(onChanged: (q) => _search(q))

// CORRECT: SearchAnchor (Material 3)
SearchAnchor(
  builder: (context, controller) => SearchBar(
    controller: controller,
    onTap: () => controller.openView(),
    onChanged: (q) => controller.openView(),
    leading: Icon(Icons.search),
    hintText: context.l10n.search,
  ),
  suggestionsBuilder: (context, controller) async {
    final results = await _search(controller.text);
    return results.map((r) => ListTile(title: Text(r.title), onTap: () => controller.closeView(r.title)));
  },
)
```

---


## Quality Gate: Flutter Supplement

Run these alongside the core Quality Gate. All answers must be **no** (for "is there a problem?") or **yes** (for "does it meet the standard?").

### Hard Gate (Flutter)

- [ ] Are there any `Color(0xFF...)` values in widget code outside `AppColors`? *(FR-01)*
- [ ] Are there any inline `TextStyle(...)` repeated across widgets? *(FR-01)*
- [ ] Does any feature violate the feature-first architecture (wrong layer imports, domain importing Flutter)? *(FR-02)*
- [ ] Is any state management using `Bloc` with events instead of `Cubit`? *(FR-03)*
- [ ] Is any cubit registered with the wrong scope (screen-scoped as singleton)? *(FR-04)*
- [ ] Is any cubit using `try/catch` instead of `Either` pattern matching? *(FR-05)*
- [ ] Does any data-loading screen lack loading, error, or empty states? *(FR-06)*
- [ ] Are there any screens that only show the happy path? *(FR-06)*

### Purpose Gate (Flutter)

- [ ] Are there widgets extracted for every tiny helper, fragmenting the codebase? *(FR-07)*
- [ ] Are there arbitrary spacing values (17, 13, 7, 21) instead of consistent multiples? *(FR-08)*
- [ ] Is the layout broken at 375px width? *(FR-10)*

### Quality Locks (Flutter)

- [ ] Does every page use the two-widget pattern (public Page + private View)? *(FR-11)*
- [ ] Is navigation using `context.push`/`context.go` with `RoutePaths` constants? *(FR-12)*
- [ ] Were `@freezed`/`@JsonSerializable` classes regenerated after changes? *(FR-13)*
- [ ] Do cubit tests mock the use case (not the repository), and repository tests mock the datasource? *(FR-14)*
- [ ] Are all `Icon` widgets that convey meaning wrapped in `Semantics`? *(FR-15)*
- [ ] Do all `TextFormField` widgets have `labelText` or `Semantics`? *(FR-15)*
- [ ] Are all interactive elements at least 44x44 logical pixels? *(FR-15)*
- [ ] Does the visual treatment match the declared ENERGY/RHYTHM/MOTION dials? *(Part 3)*
- [ ] Does every widget decision have a one-line reason? *(core FG-31)*
- [ ] Is the overall design unique to this product, not a clone of another app? *(core FG-30)*

### Dart Shorthand (Flutter)

- [ ] Are records used instead of `Map<String, dynamic>` for structured data?
- [ ] Are switch expressions used instead of switch statements where possible?
- [ ] Are enhanced enums used instead of static const int?
- [ ] Are collection-if and collection-for used instead of manual list building?
- [ ] Are extension methods used for repeated platform/context checks?
- [ ] Are sealed classes used instead of abstract class hierarchies?
- [ ] Are `late final` used for lazy initialization instead of nullable + ?? pattern?

### Memory & Reuse (Flutter)

- [ ] Are all controllers, subscriptions, and streams disposed in `dispose()`?
- [ ] Are `const` constructors used on all immutable widgets?
- [ ] Are `ValueKey` or `ObjectKey` used on list items for efficient rebuilds?
- [ ] Are `BlocBuilder`/`BlocListener` scoped to only the widgets that need them?
- [ ] Is pagination or lazy loading used for large datasets?
- [ ] Are extracted widgets data-driven (receive data, not state managers)?
- [ ] Is the layout adaptive to screen size (mobile/tablet/desktop)?

### i18n (Flutter)

- [ ] Is `gen_l10n` or `slang` configured for all user-facing strings?
- [ ] Are there zero hardcoded strings in widget code?
- [ ] Are all strings accessed via `context.l10n.xxx` or `t.xxx`?
- [ ] Are pluralization rules handled correctly (`count` parameter)?
- [ ] Is the locale resolved from device settings, not hardcoded?
- [ ] Are date/number formats locale-aware (`DateFormat`, `NumberFormat`)?
- [ ] Does the UI handle text expansion (German ~30% longer than English)?

### Material 3 (Flutter)

- [ ] Is `useMaterial3: true` set in the theme?
- [ ] Are deprecated Material 2 widgets replaced with Material 3 equivalents?
- [ ] Is `ColorScheme.fromSeed` used for automatic Material 3 color generation?
- [ ] Are `FilledButton` / `OutlinedButton` / `TextButton` used instead of `ElevatedButton` where appropriate?
- [ ] Is `NavigationBar` used instead of `BottomNavigationBar`?
- [ ] Is `SearchBar` / `SearchAnchor` used instead of custom search implementations?

---


## Quick Reference: Enterprise Kit Conventions

| Concern | Convention |
|---------|-----------|
| **Architecture** | Feature-first clean architecture (`data/`, `domain/`, `presentation/`) |
| **State** | Cubit-only, freezed sealed states, exhaustive `switch` |
| **DI** | GetIt with manual registration, per-feature injection files |
| **Navigation** | GoRouter with centralized `RoutePaths` constants |
| **Theming** | Material 3 `ColorScheme.fromSeed`, `AppColors`, `AppTextStyles` |
| **Error Handling** | fpdart `Either<Failure, T>`, cubits call use cases |
| **Testing** | mocktail + bloc_test, mocks one layer down |
| **Code Gen** | `@freezed` + `@JsonSerializable`, `build_runner` |
| **Imports** | Absolute package paths (`package:flutter_enterprise_starter_kit/...`) |
| **Pages** | Two-widget pattern: public `Page` + private `View` |
| **Dart** | Records, switch expressions, enhanced enums, sealed classes, extension methods |
| **Memory** | const everywhere, dispose everything, keys on lists, scoped BlocBuilder |
| **Cross-Platform** | Adaptive layout, platform detection via Theme, SafeArea, responsive breakpoints |


Relative paths in this skill (e.g., scripts/, reference/) are relative to this base directory.
