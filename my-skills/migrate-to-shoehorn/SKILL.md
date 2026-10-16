---
name: migrate-to-shoehorn
description: "把测试文件从 `as` 类型断言迁移到 @total-typescript/shoehorn。当用户提到 shoehorn、想替换测试中的 `as`，或需要部分测试数据时使用。"
---

# Migrate to Shoehorn

## Why shoehorn?

`shoehorn` lets you pass partial data in tests while keeping TypeScript happy. It replaces `as` assertions with type-safe alternatives.

**Test code only.** Never use shoehorn in production code.

Problems with `as` in tests:

- Trained not to use it
- Must manually specify target type
- Double-as (`as unknown as Type`) for intentionally wrong data

## Dependency and scope

Inspect the repository manifest, lockfile, existing test conventions, and working-tree diff first. Reuse the installed version when available. If the requested migration needs a new dependency, add it as a test-only dependency with the repository's package manager; do not install globally. Avoid running package lifecycle scripts unless the repository's normal install process requires them.

Example for npm: npm install --save-dev @total-typescript/shoehorn. Translate only after identifying the repository's package manager.

Do not replace every type assertion mechanically. Keep assertions that express a real contract, narrow a discriminated union, define a const literal, or belong to a type-level test. Change only test fixtures whose intent matches a Shoehorn helper below.

## Migration patterns

### Large objects with few needed properties

Before:

```ts
type Request = {
  body: { id: string };
  headers: Record<string, string>;
  cookies: Record<string, string>;
  // ...20 more properties
};

it("gets user by id", () => {
  // Only care about body.id but must fake entire Request
  getUser({
    body: { id: "123" },
    headers: {},
    cookies: {},
    // ...fake all 20 properties
  });
});
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

it("gets user by id", () => {
  getUser(
    fromPartial({
      body: { id: "123" },
    }),
  );
});
```

### `as Type` → `fromPartial()`

Before:

```ts
getUser({ body: { id: "123" } } as Request);
```

After:

```ts
import { fromPartial } from "@total-typescript/shoehorn";

getUser(fromPartial({ body: { id: "123" } }));
```

### `as unknown as Type` → `fromAny()`

Before:

```ts
getUser({ body: { id: 123 } } as unknown as Request); // wrong type on purpose
```

After:

```ts
import { fromAny } from "@total-typescript/shoehorn";

getUser(fromAny({ body: { id: 123 } }));
```

## When to use each

| Function        | Use case                                           |
| --------------- | -------------------------------------------------- |
| `fromPartial()` | Pass partial data that still type-checks           |
| `fromAny()`     | Pass intentionally wrong data (keeps autocomplete) |
| `fromExact()`   | Force full object (swap with fromPartial later)    |

## Workflow

1. Resolve the requested scope. Reuse file names, migration boundaries, and test intent already supplied by the user. Otherwise inspect the relevant test directories with the host's search tool, such as rg, for the project's test extensions (for example, *.test.ts, *.spec.ts, *.test.tsx, and *.spec.tsx). Ask only when the remaining ambiguity could change which tests or behavior are migrated.
2. Classify each candidate by intent. Read its surrounding test and target type. Use fromPartial() for a valid but incomplete fixture, fromAny() for deliberately invalid input whose runtime validation is under test, and fromExact() only when the fixture is intentionally complete. Leave unrelated casts unchanged and record why a matching cast stays.
3. Use the project's dependency path. If Shoehorn is absent and dependency changes are within the requested migration, add it as a test-only dependency using the detected package manager. If dependency changes are outside scope, complete the analysis and report the missing dependency without installing it.
4. Make the smallest edits. Add imports once per file, preserve assertions that are not fixture casts, and avoid production-code edits.
5. Verify the affected behavior. Run the narrow test or type-check command found in the repository's scripts and configuration. If no such command exists, use the available checks and report what remains unverified; do not claim a pass. Review the final diff and report migrated, retained, and unverified cases.

A text match is only a candidate. The migration is complete when every in-scope candidate has either been converted and checked or has a recorded reason to remain unchanged.
