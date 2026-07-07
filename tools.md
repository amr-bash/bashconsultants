---
title: The BASH toolkit
sub-title: Deep-dive guides and training for small businesses and the consultants who serve them
description: The BASH toolkit — DIY guides for small businesses and advanced technical training for IT consultants, across cloud, ERP, data, finance, AI, and security
excerpt: A two-track library — plain-English DIY guides for small businesses, and deep technical training for the consultants who build these systems.
layout: default
preview: /assets/images/previews/from-prompts-to-pipelines-agentic-ai-in-vs-code.png
sidebar:
  nav: toolkit
keywords:
  - small business IT guides
  - DIY IT for small business
  - IT consultant training
  - cloud ERP data security tutorials
  - AI adoption for small business
  - BASH consultant partner program
categories:
  - tools
  - ai
tags:
  - toolkit
  - training
  - ai
draft: false
date: 2026-07-06T12:00:00.000Z
lastmod: 2026-07-07T12:00:00.000Z
permalink: /tools/
slug: tools
---

## What the toolkit is

The BASH toolkit is our open library of how-to knowledge — the same material we use to guide clients and to train the consultants who deliver the work. It comes in two tracks, because two very different readers need it.

- **[For your business](/tools/business/)** — plain-English, do-it-yourself guides for owners, operators, and in-house generalists at small and medium businesses. No jargon, no sales pitch. Whether you run a law office, a construction firm, a clinic, a distributor, a retailer, or a nonprofit, the underlying technology needs are more alike than you'd think, and these guides meet you where you are.
- **[For BASH partners](/tools/partners/)** — deep technical training for the consultants who build these systems. Wide and deep on the architectures, frameworks, and trade-offs behind every capability we offer. Written for senior practitioners who are expected to be among the most advanced IT professionals in the room.

Everything here is free to read. The business track helps you decide what to do and how much you can do yourself; the partner track is the reference we hold our own delivery standard to.

## For your business

DIY guides and foundations, applicable across every kind of small business. Start with the foundations, then go deep on whatever is slowing you down.

<div class="row row-cols-1 row-cols-md-2 g-4 my-3">
{% assign business_docs = site.toolkit | where_exp: "d", "d.categories contains 'business'" | where_exp: "d", "d.topic" | sort: "order" %}
{% for doc in business_docs %}
  <div class="col">
    <div class="card h-100 shadow-sm">
      <div class="card-body d-flex flex-column">
        <div class="mb-2">
          <span class="badge text-bg-primary">{{ doc.topic_label }}</span>
          {% if doc.level %}<span class="badge text-bg-secondary text-capitalize">{{ doc.level }}</span>{% endif %}
        </div>
        <h3 class="fs-5 fw-bold card-title">
          <a href="{{ doc.url | relative_url }}" class="stretched-link text-decoration-none text-body-emphasis">{{ doc.title }}</a>
        </h3>
        <p class="card-text small">{{ doc.description }}</p>
      </div>
    </div>
  </div>
{% endfor %}
</div>

<a href="/tools/business/" class="btn btn-outline-primary">Browse the business track</a>

## For BASH partners

Advanced technical training on the technologies and frameworks behind every service we offer. If you are a consultant partnering with BASH, this is the depth we expect you to work at.

<div class="row row-cols-1 row-cols-md-2 g-4 my-3">
{% assign partner_docs = site.toolkit | where_exp: "d", "d.categories contains 'partners'" | where_exp: "d", "d.topic" | sort: "order" %}
{% for doc in partner_docs %}
  <div class="col">
    <div class="card h-100 shadow-sm border-primary-subtle">
      <div class="card-body d-flex flex-column">
        <div class="mb-2">
          <span class="badge text-bg-dark">{{ doc.topic_label }}</span>
          {% if doc.level %}<span class="badge text-bg-secondary text-capitalize">{{ doc.level }}</span>{% endif %}
        </div>
        <h3 class="fs-5 fw-bold card-title">
          <a href="{{ doc.url | relative_url }}" class="stretched-link text-decoration-none text-body-emphasis">{{ doc.title }}</a>
        </h3>
        <p class="card-text small">{{ doc.description }}</p>
      </div>
    </div>
  </div>
{% endfor %}
</div>

<a href="/tools/partners/" class="btn btn-outline-primary">Browse the partner track</a>

## How we practice what we teach

We don't just publish this material — we run our own operation on it. This site is written, reviewed, illustrated, validated, and shipped through a governed AI pipeline, and the partner track documents that pipeline in full. See [[Running an AI-native consulting practice]] for the tools, prompts, and guardrails behind it, and [how an AI-augmented practice runs](/ai-operations/) for the operating model in plain terms.

## Where to start

- Not sure what your business needs? Begin with [[The small-business IT foundation]].
- Weighing a specific move — cloud, ERP, AI, better reporting? Jump straight to the matching guide in the [business track](/tools/business/).
- A consultant looking to partner or level up? Start with [[The BASH engagement method]], then go deep on your specialty.

Have a question a guide doesn't answer? [Book a free consultation](/contact/) and we'll point you to the right starting place.
