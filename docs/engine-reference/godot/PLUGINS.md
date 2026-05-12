# Godot 4.6 — Add-ons, Modules & Optional Systems

**Last verified:** 2026-02-12
**Pinned engine version:** Godot 4.6 (see `VERSION.md`)

This document indexes optional add-ons and modules commonly paired with Godot.
Unlike Unity/Unreal, Godot's ecosystem leans on community add-ons distributed via
the Asset Library rather than a first-party package manager.

> **Knowledge gap warning:** the LLM training cutoff is May 2025 (~Godot 4.3).
> Versions 4.4, 4.5, and 4.6 introduced significant changes to physics,
> accessibility, and the rendering pipeline. Verify any non-obvious API call
> against the official docs at https://docs.godotengine.org/en/stable/ before
> committing to it. Sections marked `[VERIFY — Godot 4.6]` need direct
> documentation cross-check.

---

## How to Use This Guide

- ✅ **First-party (in-engine):** ships with Godot, no install needed.
- 🟡 **First-party module (compile flag):** needs a custom engine build.
- 📦 **Asset Library add-on:** install through Editor → AssetLib tab.
- ⚠️ **Experimental:** API may change before stabilization.

---

## First-Party Subsystems Worth Knowing

### ✅ Jolt Physics (default in 4.6)

- **Purpose:** High-performance 3D physics engine, replaces GodotPhysics3D as the
  default in Godot 4.6.
- **When to use:** Any 3D physics work. GodotPhysics3D remains available for
  projects that need its exact behavior.
- **Knowledge gap:** Jolt was an *optional* third-party module in 4.4, became the
  default in 4.6. Anything the LLM learned about Godot 3D physics is now stale.
- **Status:** Production-ready, default.
- **Detailed docs:** [modules/physics.md](modules/physics.md)
- **Official:** https://docs.godotengine.org/en/stable/tutorials/physics/index.html

### ✅ AccessKit Accessibility (4.5+)

- **Purpose:** Screen reader and accessibility integration via the AccessKit
  cross-platform library.
- **When to use:** Any game shipping on platforms that require accessibility
  compliance (consoles, EU launches under GAAD/EAA, government contracts).
- **Knowledge gap:** Added in Godot 4.5 — the LLM training data has no
  information about Godot accessibility APIs. `[VERIFY — Godot 4.6]`
- **Status:** Production-ready in 4.6.
- **Official:** https://docs.godotengine.org/en/stable/tutorials/ui/accessibility.html

### ✅ Shader Baker (4.5+)

- **Purpose:** Precompile shaders at build time to eliminate first-frame shader
  stutter at runtime.
- **When to use:** Any project that ships on platforms where shader compile
  stutter is visible (PC, console).
- **Knowledge gap:** Workflow and recommended usage patterns added in 4.5.
  `[VERIFY — Godot 4.6]`
- **Status:** Production-ready.

### ✅ D3D12 Renderer (default on Windows in 4.6)

- **Purpose:** Direct3D 12 backend, now the default rendering backend on Windows
  in Godot 4.6 (replaced Vulkan as the Windows default).
- **When to use:** Default — no opt-in required on Windows.
- **Knowledge gap:** Major change in 4.6. Vulkan still available as an opt-in.
  `[VERIFY — Godot 4.6]`
- **Detailed docs:** [modules/rendering.md](modules/rendering.md)

### ✅ Variadic Function Arguments (4.5+)

- **Purpose:** GDScript and shader language now support variadic arguments.
- **When to use:** Cleaner public APIs that previously required arrays.
- **Knowledge gap:** Not in training data. `[VERIFY — Godot 4.6]`

### ✅ `@abstract` Class Modifier (4.5+)

- **Purpose:** Mark a class as abstract to prevent instantiation, enforce
  subclassing.
- **When to use:** Base classes that should never be instantiated directly.
- **Knowledge gap:** New language feature in 4.5.

### ✅ Inverse Kinematics (restored in 4.6)

- **Purpose:** IK solver for skeletons.
- **Knowledge gap:** IK was removed in early 4.x and restored in 4.6 with a
  redesigned API. Whatever the LLM remembers about Skeleton IK from 3.x or
  early 4.x is wrong. `[VERIFY — Godot 4.6]`

---

## Common Asset Library Add-ons

The Asset Library is the official add-on distribution channel
(`https://godotengine.org/asset-library/`). Add-ons that the LLM may have
opinions about — check current version compatibility before recommending:

### 📦 Dialogic — narrative/dialogue system

- **Purpose:** Visual editor for branching dialogue, character profiles, theming.
- **When to use:** Story-driven games, RPGs, visual novels.
- **Compatibility:** Verify the Dialogic version supports Godot 4.6. Major
  rewrites historically broke between minor Godot versions.

### 📦 Phantom Camera — virtual camera system

- **Purpose:** Cinemachine-style virtual camera workflow for Godot.
- **When to use:** 3D games needing complex camera behavior (third-person,
  cutscenes, follow cameras).
- **Compatibility:** Active project; verify the 4.6 branch.

### 📦 Beehave — behavior trees

- **Purpose:** Visual behavior tree authoring for AI.
- **When to use:** Enemy AI, NPC behavior, anything more complex than a state
  machine.

### 📦 GodotSteam — Steam integration

- **Purpose:** Wraps the Steamworks SDK for achievements, leaderboards,
  workshop, networking.
- **When to use:** Steam-bound releases.

### 📦 Input Helper / Input Remapping

- **Purpose:** Common patterns for runtime input remapping and gamepad
  detection.
- **Compatibility:** Some add-ons in this space pre-date the InputEvent
  improvements in 4.5+; prefer add-ons updated for 4.6.

---

## What's NOT Listed Here

- Engine modules requiring custom builds (`modules/` source compilation) — out
  of scope for most indie teams. See
  https://docs.godotengine.org/en/stable/contributing/development/compiling/
- GDExtension native add-ons (`.gdextension`) — covered conceptually in
  `modules/rendering.md` and the `godot-gdextension-specialist` agent.
- Asset Library entries that have not been updated for Godot 4.x — they will
  not load.

---

## Verification Checklist Before Recommending a Plugin

1. Open the Asset Library entry and confirm "Compatible with Godot 4.6" in the
   support matrix.
2. Read the plugin's README for known breaking changes since the version the
   LLM training data covered.
3. For first-party features marked `[VERIFY — Godot 4.6]` above, open the
   matching page in https://docs.godotengine.org/en/stable/ and confirm the
   API signature.
4. If recommending in production code, link directly to the doc URL in the ADR
   or design doc — do not rely on agent memory of the API.
