---
title: "One reporting layer over every general ledger"
description: How a general ledger data warehouse and dashboards gave a manufacturer one governed reporting layer across multiple ERP systems
industry: manufacturing
services: [data]
outcome: Leadership pulled financial results from dashboards backed by one governed dataset instead of waiting on manually assembled spreadsheet packs.
author: Amr Abdel-Motaleb
lastmod: 2026-07-06T12:00:00.000Z
keywords:
  - general ledger data warehouse
  - financial reporting dashboards
  - Power BI financial reporting
  - ERP data integration
  - business intelligence consultant
  - data governance finance
draft: false
---

## The situation

A manufacturer running several Enterprise Resource Planning (ERP) systems had a reporting problem disguised as a staffing problem. Every management reporting cycle, analysts pulled general ledger (GL) extracts from each system, cleaned them in spreadsheets, reconciled the versions that didn't agree, and assembled a pack — by which point the questions had changed. Leaders didn't distrust the numbers exactly; they distrusted how long the numbers took and how much handling happened along the way.

## What we did

At a multi-billion-dollar manufacturer, the founder provided the technical design for a global GL data mart — the data storage structures, data mining, and data cleansing that pull ledger detail from multiple ERP systems into one governed model — and built companion marts for accounts receivable and revenue recognition reporting. On top of that layer, he developed dashboards and advanced data models covering more than $4 billion in activity across multiple ERP instances. The sequence:

- **Define the common model.** One structure for accounts, entities, periods, and currencies that every source ERP maps into — the financial-systems equivalent of agreeing on units before you measure.
- **Automate the extracts.** Scheduled pipelines replace analysts pulling files, so the data arrives the same way every time and discrepancies surface as data issues to fix, not mysteries to reconcile.
- **Build reporting people actually use.** Business Intelligence (BI) dashboards designed around the questions leadership asks — results by entity, trend against plan, drill-down to the ledger detail — using tools like [Microsoft Power BI](https://learn.microsoft.com/en-us/power-bi/).

## How it played out

Reporting shifted from assembly work to analysis. The same governed dataset fed corporate reporting, management dashboards, and ad hoc questions, so different audiences stopped getting subtly different numbers. And because the pipelines were documented and automated, the reporting didn't degrade when any one analyst changed jobs.

## What it means for a business like yours

Scale down the ERP count and this is most SMBs: a Denver accounting firm with practice management in one system and books in another, or a multi-location retailer reconciling point-of-sale against QuickBooks. The fix is the same shape — one agreed data model, automated feeds, and a reporting layer your team can run — typically built in weeks-to-months at small-business scale, not the year-long programs enterprises endure.

## Next step

Our [[Data and BI]] work starts with the question your reports can't currently answer — bring one and we'll show you what the pipeline to answer it looks like.
