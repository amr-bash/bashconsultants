---
title: The BASH toolkit
description: The working tools behind BASH Consulting — a governed prompt playbook, a VS Code orchestrator, and AI pipelines we use in client work
excerpt: The tools that run this practice every day — a prompt playbook, an editorial governance stack, a VS Code extension, and automated build gates.
layout: default
preview: /assets/images/previews/from-prompts-to-pipelines-agentic-ai-in-vs-code.png
sidebar:
  nav: dynamic
keywords:
  - AI consulting tools Denver
  - governed AI prompts
  - prompt library for business
  - VS Code prompt orchestrator
  - AI content governance
  - small business AI adoption
  - AI workflow automation
categories:
  - tools
  - ai
tags:
  - tools
  - ai
draft: false
date: 2026-07-06T12:00:00.000Z
lastmod: 2026-07-06T12:00:00.000Z
permalink: /tools/
slug: tools
---

## Why we publish our toolkit

Before you pay anyone to bring artificial intelligence (AI) into your business, ask them to show you how they run it in their own. This page is our answer. Everything below is a working part of this practice — written down, version-controlled, and visible in [this site's public GitHub repository](https://github.com/bamr87/bashconsultants). We sell what we use: every tool here runs this practice daily, and the same patterns transfer to a law office's engagement letters, a distributor's order confirmations, or a clinic's patient communications.

The point isn't the specific software. It's the operating discipline: recurring AI work runs from written, reviewed playbooks — not from whatever someone happened to type into a chat window that morning. For the full story of how these pieces fit together day to day, see [how an AI-augmented practice runs](/ai-operations/).

## Prompt Orchestrator: a VS Code extension

Prompt Orchestrator is a small Visual Studio Code (VS Code) extension we built to run our playbook without leaving the editor. Today it does four things:

- Discovers prompt templates automatically from the repository's `.github/prompts/` directory.
- Shows them in a sidebar view in the VS Code Explorer, so anyone on a project sees the same task list.
- Runs a chosen prompt against a chosen file from the Command Palette or the file's right-click menu, packaging the file's content as context.
- Hands the assembled prompt to GitHub Copilot Chat, executes it directly through the VS Code Language Model API, or copies it to the clipboard for use anywhere else.

It's an internal tool, MIT-licensed and early-stage — we run it from source rather than the extension marketplace — and the full TypeScript source is public in the [extension folder of this repository](https://github.com/bamr87/bashconsultants/tree/main/extension). If your team runs repeatable AI tasks — drafting, reviewing, summarizing — this is the shape we'd recommend: templates in one governed place, executed the same way by everyone.

## The prompt playbook

Each recurring task in this practice has a written prompt with a defined role, inputs, and quality criteria. Prompts are versioned like code and reviewed like code. The table below isn't hand-maintained — a script ([`scripts/generate_playbook_data.py`](https://github.com/bamr87/bashconsultants/blob/main/scripts/generate_playbook_data.py)) reads the actual prompt files and regenerates it, so this page can't quietly drift from what we really run.

{:table .table .table-striped}
Prompt | What it does
---------|----------
{% for prompt in site.data.playbook.prompts -%}
{{ prompt.name }} | {{ prompt.description }}
{% endfor %}

## The governance stack

Prompts say what to do; instruction files say what "good" means. These are scoped rule files that load automatically whenever an AI agent (or a person) works on matching files — editorial voice and banned phrases for customer-facing pages, frontmatter schemas for posts, coding conventions for the extension. They're the same mechanism VS Code documents for [customizing Copilot with instruction files](https://code.visualstudio.com/docs/copilot/copilot-customization), applied as the editorial authority for this whole site. This table is generated from the same script:

{:table .table .table-striped}
Rule set | What it governs
---------|----------
{% for instruction in site.data.playbook.instructions -%}
{{ instruction.name }} | {{ instruction.description }}
{% endfor %}

## The preview-image pipeline

Every article banner on this site is generated, not stock. A Bash script scans posts for missing preview images, builds an image prompt from the post's own title and description, calls OpenAI's gpt-image-2 model, saves the result, and updates the post's metadata — typically about $0.15–0.20 per image at current API rates ([OpenAI API pricing](https://platform.openai.com/docs/pricing), as of July 2026). That's the honest economics of this kind of automation: a task that once meant an hour of stock-photo hunting per article now costs cents and minutes, with a human glancing at the output before it ships.

## Build gates and scheduled runs

None of the above publishes anything on its own. Every push and pull request to this site triggers a full build in continuous integration (CI) before deployment — if the build breaks, nothing ships. Recurring upkeep (article reviews, refactoring, test generation, documentation) runs through the same playbook prompts on a routine cadence, and a person reads every change before it merges. Agents draft; humans approve. That's the rule here, and it's the rule we set up for clients.

## Put the same discipline to work

If you want AI in your business with this kind of structure behind it — governed prompts, written rules, and human sign-off — that's exactly what we build for clients.

<a href="/services/ai/" class="btn btn-primary btn-lg px-4">Explore our AI services</a>
