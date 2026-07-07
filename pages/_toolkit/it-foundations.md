---
title: "The small-business IT foundation"
sub-title: "The eight IT basics every small business needs, and how they fit together"
description: A plain-English guide to small business IT foundations — accounts, devices, network, files, backup, and security explained without the jargon
excerpt: The baseline IT capabilities every small business needs, framed as a maturity ladder with a one-page self-assessment you can run this week.
author: "Amr Abdel-Motaleb"
layout: default
categories: [business]
topic: foundations
topic_label: "Foundations"
level: foundational
order: 10
tags: [foundations, small-business, it-basics, checklist, security]
keywords:
  - small business IT foundation
  - IT basics for small business
  - IT setup checklist small business
  - single sign-on for small business
  - small business backup and security
  - system of record small business
  - IT maturity model small business
lastmod: 2026-07-07T12:00:00.000Z
mermaid: false
sidebar:
  nav: toolkit
---

Most small businesses never sit down and design their technology. It accumulates. Someone signs up for an email service, then a file-sharing tool, then an accounting app, then a customer list in a spreadsheet, and five years later nobody can say exactly what you own, who has access, or what happens if the laptop with the payroll file on it gets stolen. This guide is the map you never drew. It lays out the eight capabilities every business needs regardless of industry, shows how they connect, and gives you a one-page checklist to see where you stand.

You do not need all of this to be sophisticated. A three-person law office and a forty-person distributor need the same eight things — just at different sizes. The goal here is not to make you an IT department. It is to make you the informed owner who knows what questions to ask and which problems are urgent.

## The eight capabilities every business needs

Think of these as the load-bearing walls. Skip one and the building still stands, until the day it does not.

**1. Identity and accounts.** This is the single most important and most neglected item. Every person who works for you needs a company account — usually a work email address — that you control. Not a personal Gmail. When you use a proper business account system such as [Microsoft 365](https://learn.microsoft.com/en-us/microsoft-365/admin/setup/setup) or [Google Workspace](https://support.google.com/a/answer/6365252), one login can unlock every other tool through single sign-on (SSO), and one action can shut that person out of everything the day they leave. Offboarding a departing employee should take five minutes, not five days of hunting for forgotten logins.

**2. Devices and endpoints.** The laptops, desktops, phones, and tablets your team works on. You want to know how many there are, who has which one, whether they auto-update, and whether they encrypt their storage. A lost encrypted laptop is an inconvenience. A lost unencrypted one can be a reportable data breach.

**3. Network and internet resilience.** Your internet connection is now a utility as critical as electricity. If a dental clinic loses connectivity, it cannot check patients in or run cards. The fix is rarely expensive: a business-grade router and a cellular backup that fails over automatically when the main line drops.

**4. File storage and sharing.** One place where documents live, with permissions that match reality. The failure mode here is files scattered across desktops, personal drives, and email attachments, where the current version of anything is a guess.

**5. Systems of record.** For each core function, there should be one authoritative place the data lives — the system of record. Accounting in your books, customers in a customer relationship management (CRM) tool, operations in whatever runs your actual work. When the same customer exists in three places with three phone numbers, you have three systems of record and no truth.

**6. Backup.** A copy of everything important that survives when the original does not — ransomware, a deleted folder, a failed drive, a mistaken sync. Cloud tools are not backups; they faithfully replicate your mistakes. See [[Backups and recovery that actually work]] for how to do this properly.

**7. Security basics.** Multi-factor authentication (MFA) on every account, a password manager, current software, and enough email filtering to catch the obvious scams. This is not paranoia; it is a smoke detector. See [[The security baseline every small business needs]].

**8. Documentation.** A single shared document that records what you have, who the administrators are, which vendors you pay, and how to recover from the obvious disasters. When the person who "just knows how it all works" is on vacation, this is what saves you.

Here is how they stack. Identity sits at the bottom because everything else authenticates against it. Systems of record sit at the top because they are what the business actually runs on.

| Capability | What it answers | Common failure |
|---|---|---|
| Identity and accounts | Who are you, and what can you reach | Personal accounts you cannot control |
| Devices and endpoints | What are you working on | Unencrypted, un-updated laptops |
| Network resilience | Can you get online | No backup connection |
| File storage and sharing | Where do documents live | Scattered, version-confused files |
| Systems of record | Where does the truth live | Same data in three tools |
| Backup | Can you recover | "The cloud is our backup" |
| Security basics | Are you locked | No MFA, shared passwords |
| Documentation | Does anyone know how this works | It all lives in one person's head |

## The maturity ladder: surviving, stable, scaling

Not every business needs the same rung. Match your ambition to your reality.

**Surviving.** You have accounts, devices work, and files are mostly findable. But logins are shared, there is no real backup, MFA is off, and offboarding means changing one password and hoping. Most businesses under ten people live here without realizing how exposed they are. The move up is cheap and mostly about turning on features you already pay for.

**Stable.** Every person has their own controlled account with MFA. Devices are encrypted and updating. Backups run automatically and you have actually restored a test file to prove they work. There is one system of record per function. A departing employee is fully offboarded in minutes. This is the target for almost every small and medium business, and it is achievable in a few focused weeks.

**Scaling.** You are adding people or locations and the manual approach strains. Now you want centralized device management, single sign-on across all your tools, integrations so systems share data automatically, and a written [[Building a 12-month IT roadmap]]. This is where an outside hand usually pays for itself, because the cost of doing it wrong multiplies with headcount.

The honest number: moving a typical five-to-fifty-person business from surviving to stable is usually a matter of days of work spread over four to eight weeks, not a large capital project. Most of the cost is attention, not money.

## What you can do yourself this week

You can genuinely do most of the "surviving to stable" work without help. Here is a concrete order of operations.

- **Inventory in one hour.** Open a spreadsheet. List every tool you pay for, who administers it, what it costs, and who has access. This single document is the start of your documentation capability and it will surprise you.
- **Turn on MFA everywhere.** Start with email, banking, and accounting. Most tools have it built in and off by default. This one step blocks the large majority of account-takeover attacks.
- **Adopt a password manager.** Pick one, get the team on it, and stop reusing passwords. It takes an afternoon and removes a whole category of risk.
- **Fix offboarding.** Write down the exact steps to fully remove a departing person. If you cannot, that is a sign your accounts are not truly centralized yet.
- **Verify one backup restore.** Do not trust that backups work. Restore a single file and confirm it opens. An untested backup is a rumor.
- **Name your systems of record.** For accounting, customers, and operations, write down the one place each lives. If a function has two, plan to consolidate.

## The watch-outs that bite people

Three mistakes cause most of the real pain.

- **Personal accounts you do not own.** When the business email or the QuickBooks file is tied to an employee's personal account and that person leaves on bad terms, you can be locked out of your own operation. Everything critical must live under an account the business controls. If you are wrestling with an accounting system you have outgrown, [[Outgrowing QuickBooks: is it time for ERP?]] covers the next step.
- **Confusing sync with backup.** Cloud file sync copies your latest state everywhere, including your mistakes. Delete a folder or get hit by ransomware and the deletion syncs too. You need a separate backup that keeps older versions and cannot be overwritten by the problem it is protecting against.
- **The one person who knows everything.** If a single employee or a single outside contractor is the only one who understands your setup, you have a hidden single point of failure. Documentation is the cheap insurance against the day they are unreachable.

## Where this leads

This foundation is the entry point. Once the basics are stable, the other guides in this toolkit build on top of it: moving workloads to the cloud in [[Moving to the cloud: a small-business playbook]], turning your data into decisions in [[From spreadsheets to dashboards]], connecting your tools in [[Making your software talk to each other]], and adopting AI without losing control in [[Adopting AI in your business without losing control]]. Each assumes you have the walls in this guide standing first.

If you would rather not draw the map alone, our [[IT strategy]] work exists to do exactly this — take stock of what you have, find the gaps that matter, and sequence the fixes so the important ones happen first. [Tell us where you are on the ladder](/contact/) and we will point you to the right next step.
