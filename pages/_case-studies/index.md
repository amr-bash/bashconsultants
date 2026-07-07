---
title: "Case studies"
description: Anonymized snapshots of real ERP, finance system, and data projects from the founder's enterprise career and independent practice
permalink: /case-studies/
author: Amr Abdel-Motaleb
lastmod: 2026-07-06T12:00:00.000Z
keywords:
  - IT consulting case studies
  - ERP implementation examples
  - QuickBooks to ERP migration
  - financial consolidation project
  - Denver IT consultant
  - data warehouse case study
draft: false
---

These are engagement snapshots — categories of real work drawn from the founder's enterprise career and independent consulting practice. Each one describes a project the way it actually went: the situation, the work, and what changed.

A few ground rules on how we present them:

- **Anonymized.** No client names. Where a company is described ("a multi-entity manufacturer"), that is the category of business, not a pseudonym you're meant to decode.
- **No invented numbers.** Where we cite a figure, it comes from the underlying work record; otherwise we use ranges or plain qualitative outcomes.
- **Verifiable background.** The employers, roles, and systems behind these projects are listed on the [[Amr Abdel-Motaleb]].

Most of this work was done for manufacturers and distributors, because that's where the founder's enterprise career happened. The same patterns — outgrown accounting systems, disconnected data, manual re-keying — show up in construction firms, clinics, professional services, and nonprofits, and the write-ups point out where they carry over.

## Engagement snapshots

{% assign entries = site['case-studies'] | sort: "title" %}
{% for cs in entries %}{% if cs.url == page.url %}{% continue %}{% endif %}
### [{{ cs.title }}]({{ cs.url }})

**Industry:** {{ cs.industry | capitalize }}

{{ cs.description }}.

**Outcome:** {{ cs.outcome }}
{% endfor %}

## Sound familiar

If one of these situations reads like your Monday morning, the fastest way to find out whether it applies to your business is a short conversation — no pitch deck, no obligation. [Contact us](/contact/) and describe what's breaking.
