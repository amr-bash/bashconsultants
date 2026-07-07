---
title: "The BASH toolkit for your business"
sub-title: Plain-English, do-it-yourself IT guides for small and medium businesses
description: Do-it-yourself IT guides for small and medium businesses — cloud, ERP, finance automation, data, AI, and security explained in plain English
excerpt: DIY guides that help a small-business owner or in-house generalist understand, plan, and do more of their own IT — no jargon, no sales pitch.
layout: default
sidebar:
  nav: toolkit
keywords:
  - DIY IT for small business
  - small business technology guide
  - cloud migration small business
  - QuickBooks to ERP guide
  - small business security checklist
  - AI for small business
categories:
  - business
tags:
  - toolkit
  - small-business
landing: true
lastmod: 2026-07-07T12:00:00.000Z
permalink: /tools/business/
---

These guides are written for the person who runs the business, not an IT department. The examples span a law office, a construction firm, a dental clinic, a distributor, a multi-location retailer, and a nonprofit — because the underlying technology needs are remarkably similar once you look past the industry. Each guide tells you what the capability is, whether you can do it yourself, where the real risk is, and when it's worth bringing in help.

New here? Start with [[The small-business IT foundation]], then follow whichever thread is slowing you down.

{% assign topic_order = "foundations,ai,cloud,erp,fintech,data,dev,strategy,security" | split: "," %}
{% assign track_docs = site.toolkit | where_exp: "d", "d.categories contains 'business'" | where_exp: "d", "d.topic" %}
{% for topic in topic_order %}
{% assign in_topic = track_docs | where: "topic", topic | sort: "order" %}
{% if in_topic.size > 0 %}
## {{ in_topic[0].topic_label }}

{% for doc in in_topic %}
- **[{{ doc.title }}]({{ doc.url | relative_url }})**{% if doc.level %} <span class="badge text-bg-secondary text-capitalize">{{ doc.level }}</span>{% endif %} — {{ doc.description }}
{% endfor %}
{% endif %}
{% endfor %}

## Want a hand?

These guides are meant to make you self-sufficient. When a project is bigger than a weekend — a real migration, an audit deadline, a system that has to keep running while you change it — that's when a conversation helps. [Tell us what's slowing you down](/contact/) and we'll point you to the right guide or the right next step.
