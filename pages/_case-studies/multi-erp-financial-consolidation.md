---
title: "Consolidated reporting across multiple ERP systems"
description: How a multi-entity manufacturer replaced spreadsheet consolidation with a governed platform producing one set of numbers across its ERPs
industry: manufacturing
services: [fintech, data]
outcome: Corporate accounting produced consolidated results from one governed platform instead of stitching together exports from each ERP.
author: Amr Abdel-Motaleb
lastmod: 2026-07-06T12:00:00.000Z
keywords:
  - financial consolidation software
  - OneStream implementation
  - Hyperion Financial Management
  - multi-entity reporting
  - chart of accounts harmonization
  - month-end close consolidation
draft: false
---

## The situation

A manufacturer operating multiple business units — acquired over time, each with its own Enterprise Resource Planning (ERP) system and its own chart of accounts — needed one set of consolidated financial statements. The monthly reality: each entity exported its trial balance, corporate accounting mapped everything in spreadsheets, intercompany eliminations were done by hand, and the consolidated numbers were finished days after anyone could act on them. Every acquisition made it worse.

## What we did

The founder has built this fix repeatedly across his enterprise career: on Oracle Hyperion Financial Management (HFM) at a global electronics manufacturer and an automotive manufacturer, and on OneStream at a multi-billion-dollar agriculture and infrastructure manufacturer, where he managed the financial systems team responsible for the platform. The work follows the same sequence regardless of tool:

- **Harmonize the chart of accounts.** Define corporate account structures, business rules, and data definitions that every entity maps into — the unglamorous step that determines whether the platform ever produces numbers people trust.
- **Design the consolidation model.** Entity hierarchies, currency translation, intercompany eliminations, and management-versus-legal reporting views, configured in the Enterprise Performance Management (EPM) platform.
- **Connect the ERPs.** Direct integrations from each ERP into the consolidation system, replacing the monthly export-and-paste routine.
- **Leave the team able to run it.** Documentation and training so the accounting team owns the close, not a consultant on retainer.

## How it played out

Consolidation moved from a spreadsheet exercise into a governed system with an audit trail — who mapped what, when eliminations posted, which version of the numbers is final. Close cycles shortened because mapping and eliminations ran in the platform rather than in whoever-has-the-spreadsheet's inbox. [Oracle's EPM documentation](https://docs.oracle.com/en/applications/enterprise-performance-management/) describes the product mechanics; the value is in the accounting design underneath.

## What it means for a business like yours

You don't need to be a global manufacturer to have this problem. A Denver professional services firm with three entities, or a multi-location retailer with a company per store, hits the same wall — just in smaller spreadsheets. The same discipline applies at SMB scale, often with lighter tools.

## Next step

If your consolidation lives in spreadsheets, our [[Finance tech]] work covers exactly this, sized to your entity count and budget.
