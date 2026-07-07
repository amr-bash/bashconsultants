---
title: "Backups and recovery that actually work"
sub-title: "Why 'we have backups' is usually a false comfort, and how to fix it before you need it"
description: A plain-English guide to small business backups and recovery — the 3-2-1 rule, immutable copies, RTO and RPO, and the restore test that proves it works
excerpt: The difference between having backups and being able to recover — the 3-2-1 rule, offline copies, RTO and RPO, and a quarterly restore test in plain English.
author: "Amr Abdel-Motaleb"
layout: default
categories: [business]
topic: security
topic_label: "Security & managed IT"
level: foundational
order: 95
permalink: /tools/business/backup-and-recovery/
tags: [security, backup, disaster-recovery, ransomware, business-continuity, small-business]
keywords:
  - small business backup strategy
  - 3-2-1 backup rule
  - immutable backup ransomware
  - recovery time objective RTO
  - recovery point objective RPO
  - test your backups restore
  - disaster recovery for small business
  - offline backup ransomware protection
lastmod: 2026-07-07T12:00:00.000Z
mermaid: false
sidebar:
  nav: toolkit
---

Ask almost any small business owner whether they have backups and the answer is yes. Ask whether they have ever restored from one and watched it work, and the room goes quiet. That gap is where disasters live. "We have backups" is a statement about the past. "We can recover by Thursday" is about the future, and it is the only one that matters when a drive fails, an employee deletes the wrong folder, or ransomware encrypts every file you can reach.

This guide closes that gap. It explains the 3-2-1 rule in plain English, why one copy has to be untouchable, what to actually back up (hint: it is not just files), how to decide how much downtime and data loss you can live with, and the single test that turns a hopeful backup into a proven one. None of this requires an IT department, and most of it you can verify yourself this week.

## Why "we have backups" is usually false comfort

Three quiet assumptions turn a backup into a liability, and each one has taken down businesses that thought they were covered.

- **Sync is not backup.** Cloud file tools such as OneDrive, Google Drive, and Dropbox faithfully copy your latest state everywhere — including your mistakes. Delete a folder and the deletion syncs. Get hit by ransomware and the encrypted files sync over the good ones. Sync keeps your files current; it does not keep an older, safe version you can roll back to.
- **The backup is reachable, so ransomware can reach it too.** Modern ransomware specifically hunts for backups. If your backup drive is plugged into the same computer, or your backup account uses the same login as everything else, the attacker encrypts it along with the originals. A backup the malware can touch is not a backup.
- **Nobody has ever restored from it.** Backups fail silently. The job reports success for months while quietly skipping the database, saving corrupt files, or missing the one folder that matters — and you discover this at the worst possible moment. An untested backup is a rumor, not a safety net.

The fix for all three is a deliberate design, not a bigger hard drive. That design has a name.

## The 3-2-1 rule in plain English

The 3-2-1 rule is the accepted baseline for backups, and the United States Cybersecurity and Infrastructure Security Agency (CISA) recommends it directly for small businesses. It is three numbers:

- **3 copies** of anything important — the working copy you use every day, plus two backups.
- **2 different types of storage** — for example, one backup on a local device and one in the cloud. Two copies on the same failing drive is really one copy.
- **1 copy kept off-site and offline** — somewhere physically separate and disconnected from your network, so a fire, a theft, or ransomware cannot take the original and the backup in one stroke.

A worked example for a fifteen-person design firm: live project files sit on Google Workspace (copy 1). A backup service writes a nightly copy to a local network-attached storage (NAS) device or external drive in the office (copy 2, a genuinely different storage type). Weekly, an automated job writes an encrypted copy to storage the firm cannot delete for 30 days (copy 3, off-site and effectively offline). Lose any one and the other two still bring the business back.

## The copy ransomware cannot reach

The most important word in that third copy is *immutable* — once written, the backup cannot be changed or deleted for a set period, even by an administrator, even by malware holding the admin password. CISA's guidance is explicit that backup data should be encrypted and immutable, with at least one copy offline. This is the single feature that separates businesses that pay a ransom from businesses that shrug and restore.

You have two practical ways to get an untouchable copy:

- **Immutable cloud storage.** Many backup services and cloud providers offer a "write once, cannot delete for N days" setting, sometimes called object lock or immutable storage. Turn it on and set the retention window to longer than it would realistically take you to notice an attack — 30 days is a sensible floor.
- **Offline media rotation.** For smaller setups, an external drive that you back up to and then physically unplug and store off-site does the same job. Malware cannot encrypt a drive that is sitting in a drawer at your accountant's office.

The watch-out: immutable storage is unforgiving by design. Misconfigure the retention or lock the wrong data and you can run up storage costs or lock yourself out. Start with your most critical data, set a reasonable window, and confirm the setting behaves as expected before you rely on it.

## What to actually back up

Most people back up documents and stop. But a business does not run on documents alone — it runs on its systems of record, the authoritative places your real data lives. If you only back up files, a server failure can still erase the thing you cannot rebuild from memory.

Walk through this list and confirm each item has a backup, not just an assumption:

| What to back up | Examples | The risk if you skip it |
|---|---|---|
| Files and documents | Contracts, drawings, spreadsheets, shared drives | Lost work, version chaos |
| Systems of record | Accounting data, customer relationship management (CRM), practice-management or point-of-sale databases | The unrebuildable core of the business |
| Email and calendars | Microsoft 365 or Google Workspace mailboxes | Providers do not retain deleted mail forever |
| Configuration and access | List of accounts, admin logins, vendor contacts, how to log in | Data survives but nobody can get to it |

That last row surprises people. Cloud providers such as Microsoft and Google keep the service running, but backing up your *data* inside those services is your responsibility, not theirs — deleted email and files age out of their recovery windows. Treat email and line-of-business databases as first-class backup targets, not afterthoughts.

## Deciding how fast, and how recent: RTO and RPO

Two simple questions size your entire backup plan. The acronyms are worth naming because every vendor uses them.

- **Recovery time objective (RTO): how long can you be down?** If your systems vanished this morning, how many hours until being offline causes real damage — missed payroll, patients you cannot check in, orders you cannot ship? A dental clinic might tolerate two hours; a distributor mid-shipment, one. That tells you how fast recovery has to be.
- **Recovery point objective (RPO): how much data can you afford to lose?** Restore from last night's backup and you lose everything entered today. Is a day of lost data an annoyance or a catastrophe? A business taking hundreds of orders a day may need hourly backups; a consultancy updating a few files a day is fine with nightly.

Write down an honest RTO and RPO for each critical system. They drive the design: a one-hour RPO means backing up hourly, not nightly; a two-hour RTO means you cannot rely on a restore that takes a day to download. Most small businesses land somewhere reasonable — nightly backups, same-day recovery — but the point is to choose the number on purpose instead of discovering it during a crisis.

## The test that proves it works

Here is the rule that changes everything: **a backup you have not restored from is not a backup — it is a hope.** The only proof is to recover something and watch it open. This is the step almost everyone skips, and it is the step that separates real safety from paper safety. CISA's small-business guidance stresses testing your ability to restore data both fully and partially, precisely because untested backups fail when you need them.

Run this restore test, and put it on the calendar to repeat every quarter.

**The quarterly restore test**

1. **Pick a real target.** Choose an actual file and, at least once a year, an entire system of record — your accounting data or a key database, not just a spreadsheet.
2. **Restore to a safe place.** Recover it somewhere that will not overwrite the live version, so a failed test cannot cause the damage it is meant to prevent.
3. **Open it and verify.** Confirm the file opens, the data is current to your RPO, and nothing is corrupt or missing.
4. **Time it.** Note how long the whole recovery took and compare it to your RTO. If restoring took a full day and your RTO is two hours, you have a plan that looks fine on paper and fails in reality.
5. **Write down what broke.** Every test surfaces something — a missing folder, an expired login, a step nobody documented. Fix it now, while it is cheap.

Do this four times a year and "I think we have backups" becomes "I restored our books last month; it took 40 minutes."

## Your backup and recovery checklist

Work through these in order. Most can be done or verified this week without outside help.

- **Confirm 3-2-1.** Three copies, two storage types, one off-site and offline. If any number is short, that is your first fix.
- **Add one immutable or offline copy.** Turn on object lock or immutable retention, or start rotating an external drive off-site. Set retention to at least 30 days.
- **Back up your systems of record and email**, not just files. Explicitly include your accounting, CRM, and Microsoft 365 or Google Workspace data.
- **Write down an RTO and RPO** for each critical system. Let those numbers set your backup frequency and recovery method.
- **Separate the backup login** from your everyday accounts, with its own strong password and multi-factor authentication, so an attacker who gets into your email cannot also wipe your backups.
- **Run the restore test** above, then schedule it quarterly with an owner's name attached.
- **Document the recovery steps** — where backups live, who has access, and the exact steps to restore — and store that document somewhere the disaster cannot also destroy.

## The watch-outs that bite people

- **Trusting sync as backup.** The most common and most expensive mistake. If your only "backup" is a cloud sync folder, a deletion or ransomware event propagates to every copy. You need versioned backups that the problem cannot reach.
- **A backup on the same network as the threat.** A backup drive left plugged in, or a backup account sharing your everyday login, gets encrypted right along with the originals. Isolate at least one copy.
- **Never testing.** A backup that has quietly failed for six months looks identical to a working one until the day you need it. The quarterly restore test is not optional busywork; it is the only thing that tells the difference.

Backups are one pillar of a broader defense. They work best alongside the preventive controls in [[The security baseline every small business needs]] — multi-factor authentication, patching, and email filtering that stop many incidents before you ever need to recover.

## When to get help, and the next step

You can set up and verify most of this yourself. Bring in help when you have servers or databases that need application-aware backups, strict recovery targets (an RTO measured in minutes), compliance rules about where data is stored, or simply want someone to own the quarterly test so it actually happens. That reliable-recovery discipline — automated backups, immutable copies, and a proven restore process — is exactly what [[Managed IT services]] is built to provide.

For the authoritative baseline, CISA's [Back Up Business Data guidance for small and medium businesses](https://www.cisa.gov/audiences/small-and-medium-businesses/secure-your-business/back-up-business-data) is worth ten minutes of your time and costs nothing.

If you would rather know your recovery works before you need it, [tell us what would hurt most to lose](/contact/) and we will help you build backups that actually bring the business back.
