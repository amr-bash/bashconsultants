---
title: "The BASH toolkit for partners"
sub-title: Advanced technical training for the consultants who build these systems
description: Advanced technical training for IT consultants — production AI, cloud landing zones, ERP and data architecture, and security frameworks
excerpt: Deep, wide technical reference for senior practitioners — the architectures, frameworks, and trade-offs behind every capability BASH delivers.
layout: default
sidebar:
  nav: toolkit
keywords:
  - IT consultant technical training
  - production AI architecture
  - cloud landing zone reference
  - ERP implementation architecture
  - modern data stack
  - security architecture SMB
categories:
  - partners
tags:
  - toolkit
  - partners
  - advanced
landing: true
lastmod: 2026-07-07T12:00:00.000Z
permalink: /tools/partners/
---

The partner track is the reference we hold our own delivery to. It assumes you are a senior practitioner — you can read an architecture diagram, reason about failure modes, and weigh a trade-off without a vendor telling you the answer. The through-line across every guide is the BASH doctrine: **deterministic, auditable foundations first; AI as an overlay, never as the load-bearing wall.** If a step can be a script, it's a script; the model is spent where judgment is genuinely needed.

Start with [[The BASH engagement method]] for how we run the work, and [[The deterministic-first doctrine]] for why we build the way we do. Then go deep on your specialty.

{% assign topic_order = "practice,ai,cloud,erp,fintech,data,dev,strategy,security" | split: "," %}
{% assign track_docs = site.toolkit | where_exp: "d", "d.categories contains 'partners'" | where_exp: "d", "d.topic" %}
{% for topic in topic_order %}
{% assign in_topic = track_docs | where: "topic", topic | sort: "order" %}
{% if in_topic.size > 0 %}
## {{ in_topic[0].topic_label }}

{% for doc in in_topic %}
- **[{{ doc.title }}]({{ doc.url | relative_url }})**{% if doc.level %} <span class="badge text-bg-secondary text-capitalize">{{ doc.level }}</span>{% endif %} — {{ doc.description }}
{% endfor %}
{% endif %}
{% endfor %}

## Partnering with BASH

BASH consultants are expected to be among the most advanced IT professionals in the room, and to teach as well as they build. If you work at this level and want to deliver enterprise-grade systems to the small and medium businesses that rarely get access to them, [start a conversation](/contact/).
