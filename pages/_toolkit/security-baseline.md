---
title: "The security baseline every small business needs"
sub-title: "The six controls that stop most attacks — and satisfy your cyber-insurance form"
description: The six security controls every small business needs first, in priority order, plus a 30-minute self-audit and how they map to cyber insurance
excerpt: The six security controls to put in place first — MFA, EDR, patching, least privilege, phishing awareness, and tested backups — with a 30-minute self-audit.
author: "Amr Abdel-Motaleb"
layout: default
categories: [business]
topic: security
topic_label: "Security & managed IT"
level: foundational
order: 90
tags: [security, mfa, cyber-insurance, edr, small-business]
keywords:
  - small business security checklist
  - multi-factor authentication for business
  - cyber insurance requirements small business
  - endpoint detection and response vs antivirus
  - phishing prevention small business
  - least privilege access
  - CISA Cyber Essentials
lastmod: 2026-07-07T12:00:00.000Z
mermaid: false
sidebar:
  nav: toolkit
---

Most small businesses do not get breached because an attacker did something clever. They get breached because a password was reused, a laptop had no protection, or a piece of software went eighteen months without an update. The controls that stop the common attacks are the same ones your cyber-insurance carrier now asks about on the application. Do them and you get two things at once: real protection and a lower premium — or, in some cases, the ability to get covered at all.

This guide walks through the six controls in the order you should tackle them, explains each in plain terms, tells you what you can do yourself versus when to call for help, and ties each to the question you will see on an insurance form. At the end there is a 30-minute self-audit you can run this week.

The federal government maintains a free, plain-language starting point for this: the [CISA Cyber Essentials guide](https://www.cisa.gov/resources-tools/resources/cyber-essentials) from the Cybersecurity and Infrastructure Security Agency. It is aimed at small-business and local-government leaders, and it lines up closely with everything below.

## Start here: the six controls in priority order

Do them in this order. Each is worth more than the one below it, and the top three cover the attacks that actually happen.

1. **Multi-factor authentication (MFA) everywhere**
2. **Endpoint detection and response (EDR)** on every computer
3. **Patching** — keep software and operating systems current
4. **Least-privilege accounts and fast offboarding**
5. **Phishing awareness** for every employee
6. **Tested backups** you have actually restored from

### 1. Turn on multi-factor authentication everywhere

Multi-factor authentication (MFA) means logging in takes more than a password — usually a code from an app on your phone or a tap to approve. It is the single most effective control on this list because it defeats the most common attack: someone gets or guesses a password and tries to log in as your employee.

What "everywhere" means: email first, then anything that touches money (banking, payroll, your accounting or Enterprise Resource Planning system), then remote-access tools, then everything else. Email is first because whoever controls the email inbox can reset the password on almost everything else.

- **Do it yourself:** Microsoft 365 and Google Workspace both let an administrator require MFA for all users from the admin console. Turn on the built-in "security defaults" or an equivalent conditional-access policy. Use an authenticator app, not text-message codes, where you can — text messages can be intercepted.
- **Get help when:** you have on-premises systems, a virtual private network (VPN), or line-of-business software that does not support modern MFA. Retrofitting those safely is where a [[Managed IT services]] engagement earns its keep.

**On the insurance form:** carriers now ask whether MFA is enforced on email, remote access, and privileged (administrator) accounts. Answering "no" can void a claim even if you have coverage. This is usually a hard requirement, not a discount.

### 2. Replace antivirus with endpoint detection and response

Traditional antivirus works from a list of known bad files. Endpoint detection and response (EDR) watches for bad *behavior* — a program suddenly encrypting hundreds of files, a login from an odd location, a script reaching out to an unknown server — and can isolate the machine automatically. Ransomware routinely slips past signature-based antivirus, which is why "do you have EDR?" has replaced "do you have antivirus?" on insurance applications.

- **Do it yourself:** small teams can buy per-seat EDR from vendors like Microsoft Defender for Business (included in some Microsoft 365 plans), CrowdStrike, or SentinelOne. Deployment on a handful of laptops is a weekend project.
- **Get help when:** you have more than roughly 15–20 endpoints, or you want someone watching the alerts. EDR that no one monitors is a smoke detector no one is home to hear. A managed provider running it as a monitored service — sometimes sold as managed detection and response (MDR) — is the honest answer for most businesses.

**On the insurance form:** expect "Do you deploy EDR/MDR across all endpoints and servers?" The word *all* matters — one unprotected server is the one that gets hit.

### 3. Keep everything patched

A patch is a fix the vendor releases for a security flaw. Attackers read the same release notes you do and start hunting for machines that have not applied the fix, often within days. Patching is unglamorous and it is one of the highest-value things you can do.

- **Do it yourself:** turn on automatic updates for Windows, macOS, and web browsers. In Microsoft 365 or Google Workspace, set update policies from the admin console. Make a short list of every other piece of software you run — the accounting package, the design suite, the plugin on your website — and note how each one updates.
- **Get help when:** you run servers, specialized industry software, or anything you are afraid to update because it might break. That fear is legitimate; the answer is a tested patching process, not skipping patches.

**On the insurance form:** carriers ask how quickly you apply critical patches. A common expectation is critical patches within 14 days (some ask for shorter). Have an honest answer.

### 4. Give people the least access they need — and remove it fast

Least privilege means each account can reach only what that person's job requires. The bookkeeper does not need administrator rights on every computer; the summer intern does not need access to payroll. When accounts have more access than the job needs, one compromised login becomes a company-wide problem.

The other half is offboarding. When someone leaves, their access should be gone the same day — email, shared drives, the accounting system, any remote-access tool, and building or door-code systems if those are tied in.

- **Do it yourself:** keep a simple list of who has access to what. Give day-to-day work a standard (non-administrator) account and use a separate administrator account only when needed. Write a one-page offboarding checklist and run it every time someone departs.
- **Get help when:** access has sprawled across a dozen systems and no one is sure who can see what. Untangling that is common early work in a [[Managed IT services]] relationship.

**On the insurance form:** questions cover whether administrator access is limited and separated from daily accounts, and whether you have a documented offboarding process.

### 5. Make phishing awareness a habit, not a memo

Phishing is a fake email or message designed to get someone to click a link, enter a password, or approve a payment. It is how most breaches start, and no software fully stops it — because it targets people, not machines.

- **Do it yourself:** run a short training session and repeat it. Teach two habits above all: verify any request to change bank details or send money using a phone number you already have (never one from the email itself), and treat urgency as a red flag — "do this now or else" is the oldest trick there is. Give people a simple, no-blame way to report a suspicious message.
- **Get help when:** you want ongoing simulated-phishing tests and tracking. Several vendors automate this cheaply; a managed provider can run it for you.

**On the insurance form:** carriers ask whether you conduct security-awareness training and whether you have controls against fraudulent wire and invoice requests (often called business email compromise).

### 6. Back up your data — and prove you can restore it

Backups are your last line of defense. When ransomware hits or a server dies, a good backup is the difference between a bad afternoon and a closed business. But a backup you have never restored from is a hope, not a plan — a crisis is the wrong time to learn it was corrupt.

This guide keeps backups short because they deserve their own: see [[Backups and recovery that actually work]] for how to set up the 3-2-1 approach, protect backups from ransomware, and run a real restore test.

**On the insurance form:** carriers ask whether backups exist, whether at least one copy is offline or immutable (so ransomware cannot reach it), and whether you test restores. "Yes, and we tested it last quarter" is the answer that pays claims.

## How the controls map to your cyber-insurance application

Insurance underwriting has become the de facto security checklist for small businesses — which is useful, because it tells you exactly what the market considers non-negotiable.

| Control | Typical application question | Usually required or a discount? |
|---|---|---|
| MFA | Enforced on email, remote access, and admin accounts? | Required — often a coverage gate |
| EDR / MDR | Deployed on all endpoints and servers? | Required or heavily weighted |
| Patching | Critical patches applied within a set window? | Required, with a stated timeframe |
| Least privilege | Admin access limited; offboarding documented? | Discount / risk factor |
| Phishing awareness | Regular training; wire-fraud controls? | Discount / risk factor |
| Tested backups | Offline or immutable copy; restores tested? | Required for ransomware coverage |

Two practical notes. First, answer these questions truthfully — a claim can be denied if the application overstated your controls. Second, if you cannot yet answer "yes" to the required rows, that gap is your project plan for the next 90 days.

## Your 30-minute self-audit

Set a timer. You will not fix everything in half an hour, but you will know exactly where you stand and what to do first.

- **Minutes 0–8 — MFA.** Log into your email admin console (Microsoft 365 or Google Workspace). Is MFA required for every user, including you and any other administrators? Note anyone without it.
- **Minutes 8–14 — Endpoints.** Walk to (or list) every company computer. Does each have EDR or, at minimum, active protection that someone is watching? Count the ones that do not.
- **Minutes 14–19 — Patching.** Pick three machines at random. Are operating-system and browser updates set to automatic and actually current? Check the "last updated" date.
- **Minutes 19–24 — Access.** Pull up your list of users. Does anyone have administrator or financial access they no longer need? Is there anyone still active who has left the company?
- **Minutes 24–28 — Backups.** When did someone last successfully *restore* a file from backup — not just confirm the backup ran? If the answer is "never" or "I'm not sure," flag it.
- **Minutes 28–30 — Write it down.** List every "no" you found. That list, in the priority order above, is your plan.

## The watch-outs that bite people

- **Partial MFA is a false sense of security.** MFA on your main email but not on the finance system, the VPN, or a second admin account leaves the door most attackers use standing open. Coverage has to be complete to count.
- **Nobody is watching the alerts.** EDR that fires an alert into an unmonitored inbox stops nothing. Decide who reads the alerts and how fast they respond before you rely on the tool.
- **Untested backups fail exactly when you need them.** Corrupt files, an incomplete scope, or a backup the ransomware also encrypted are all common. The only proof is a restore you have actually performed — which is why [[Backups and recovery that actually work]] treats testing as the whole point.

## Your next step

If your self-audit turned up a short list of "no" answers you can fix yourself this week, fix them — that is what this guide is for. If it turned up gaps that involve servers, monitored detection, or systems you are afraid to touch, that is where outside help pays for itself. Our [[Managed IT services]] work starts from precisely this baseline: get the six controls in place, keep them running, and make sure your insurance application tells the truth. [Tell us where your baseline stands](/contact/) and we will help you close the gaps that matter first.
