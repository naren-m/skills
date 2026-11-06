---
name: create-goal
description: Use when the user invokes /create-goal or asks to turn a vague implementation idea into a concrete design, plan, and Codex goal for later implementation.
---

# Create Goal

Turn a vague implementation idea into an explicit Codex goal that can be resumed and executed.

## Workflow

1. Treat `/create-goal <idea>` as an explicit user request to create a goal.
2. Use the `design` skill first and follow its brainstorming flow:
   - Explore the current project context before proposing changes.
   - Ask one clarifying question at a time only when the missing answer materially changes the design.
   - Present 2-3 implementation approaches with tradeoffs.
   - Draft the design artifact in the required design shape.
   - Get user approval before planning or implementation.
3. After the design is approved, use the `plan` skill to convert the design into implementation tasks.
4. Create a Codex goal with `create_goal` only after design approval and planning. The objective must include:
   - The approved design artifact path or summary.
   - The implementation plan path or task identifiers.
   - Acceptance criteria and required verification commands.
   - Any explicit non-goals or constraints from the design.
5. Do not implement during `/create-goal` unless the user explicitly asks to continue into implementation after the goal is created.

## Goal Objective Template

```text
Implement the approved design for <topic>.

Design: <path or concise summary>
Plan: <path or task IDs>
Acceptance criteria:
- <criterion>
- <criterion>
Verification:
- <command>
- <command>
Constraints:
- <constraint or non-goal>
```

## Completion

End by reporting the created goal objective and the next command or workflow the user can invoke to implement it.
