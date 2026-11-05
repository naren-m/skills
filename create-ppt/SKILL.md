---
name: create-ppt
description: Use when the user says create-ppt or asks to turn supplied material into a consistent executive PowerPoint deck.
---

# Create PPT

Use the visual defaults below instead of asking the user to choose a theme. Brainstorm the content, audience, and message.

## Workflow

Complete these stages in order. At each approval gate, stop and wait for the user.

1. **Brainstorm the deck.** Use superpowers:brainstorming before creating an artifact. Confirm the audience, purpose, message, evidence, and slide flow. Present a recommended direction.
2. **Create the Markdown storyboard.** Write a `.md` file that mirrors the proposed deck. For every slide, include its title, main message, on-slide content, intended visual or diagram, and evidence source. Show the file to the user and wait for approval.
3. **Create the HTML slideshow.** Build one self-contained HTML file from the approved storyboard. Match the approved content, order, theme, and diagrams. Open or render it for review and wait for approval.
4. **Create the PowerPoint.** After approval of the HTML slideshow, use presentations:Presentations for PPTX authoring, rendering, and validation. Preserve the approved content and visual system.

## Output contract

- Use the supplied material as the factual source. Verify linked evidence when practical and do not invent results.
- Write for an executive audience in direct, regular language. Remove troubleshooting history, implementation chatter, corporate filler, and AI terminology unless it is part of an official name.
- Use the shortest narrative that fits. An executive decision usually covers the problem, solution, evidence, outcome, next step, and decision. Combine these into three slides when readable.
- A status deck covers the objective, result, evidence, risks, and next actions. A technical deck covers context, architecture or process, and operational impact.
- Do not add a separate cover unless requested.
- If a pull request or other proof link is supplied, include an accurate screenshot or an editable evidence excerpt. Clearly label a recreated excerpt.

## Visual defaults

- Use a 16:9 canvas and Arial.
- Follow a supplied template or brand. Otherwise use the same warm off-white background `#F7F5F0` on every slide.
- Use navy `#102A43` for titles and decision bars, teal `#0B7A75` for the central solution, blue `#2F6B9A` for flows, green `#287A4D` for verified outcomes, red `#C93C37` for risks, and amber `#C06A15` for access or ownership.
- Keep layouts flat, spacious, and readable. Reuse the same title position, section label, page number, margins, and footer style across the deck.

## Diagrams

When relationships, ownership, data flow, or process steps matter, create one editable block diagram with native PowerPoint objects. Name the actual components and show their real direction of use. Keep supporting dependencies outside the main flow. Skip the diagram when it does not improve understanding.

## Completion

Render and inspect every PowerPoint slide, fix clipping or overlap, run presentation validation, and deliver the approved Markdown storyboard, HTML slideshow, and final PPTX from the workspace output directory.
