<div align="center">

<img src="https://img.shields.io/badge/🎋_hatsune_miku_approved-%2339C5BB?style=for-the-badge&logoColor=white" alt="Miku Approved"/>
<img src="https://img.shields.io/badge/初音ミク-loves_this_repo-%2386CECB?style=for-the-badge&logoColor=white" alt="Miku loves this repo"/>

# 💍 commit-to-forever

### A full-stack, production-grade wedding management platform built with Flask, Firebase, and Stripe.

> *「愛は、コードで書けない。でも、デプロイはできる。」*
> *"Love cannot be written in code. But it can be deployed."*
> — 初音ミク, probably

<br/>

![Python](https://img.shields.io/badge/Python_3.12-3776AB?style=flat-square&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask_3.0-000000?style=flat-square&logo=flask&logoColor=white)
![Firebase](https://img.shields.io/badge/Firebase_Firestore-FFCA28?style=flat-square&logo=firebase&logoColor=black)
![Stripe](https://img.shields.io/badge/Stripe_Checkout-635BFF?style=flat-square&logo=stripe&logoColor=white)
![Vercel](https://img.shields.io/badge/Vercel-000000?style=flat-square&logo=vercel&logoColor=white)
![Cloudinary](https://img.shields.io/badge/Cloudinary-3448C5?style=flat-square&logo=cloudinary&logoColor=white)
![Miku](https://img.shields.io/badge/Powered_by-Leek-%2339C5BB?style=flat-square)

</div>

---

## Overview

**commit-to-forever** is a bespoke, invitation-only wedding website designed to handle every guest-facing concern of a modern wedding — from RSVP management and personalised gift funding, to a live message wall and real-time countdown. All configuration — venues, names, dates, dress code, transport, photos — lives entirely in **Firebase Firestore**, enabling the couple to update any detail in production without a single redeploy.

Payments are handled end-to-end through **Stripe Checkout** in MXN, with support for full gift purchases and partial crowd-funded contributions, anonymous or attributed.

---

## Feature Highlights

| Feature | Description |
|---|---|
| **Invitation-gated access** | Guests log in via a unique invite code — no passwords, no accounts |
| **RSVP management** | Attendance confirmation with dietary notes, stored in Firestore |
| **Gift registry** | Full and partial (crowd-funded) gift contributions via Stripe Checkout |
| **Anonymity toggle** | Guests choose whether their name appears on a funded gift |
| **Live message wall** | Guests leave messages for the couple, displayed in real time |
| **Countdown timer** | Live JavaScript countdown to the wedding date |
| **Parallax photo band** | Full-width cinematic photo strip between sections |
| **Fully configurable from DB** | Every text, photo, colour swatch, and venue detail is editable from Firestore |
| **Zero-downtime photo updates** | Photo URLs (via Cloudinary) are read from Firestore — swapping a photo is instant |

---

## Architecture

```
                        🎋 ／人◕ ‿‿ ◕人＼ 🎋
        Miku has blessed this infrastructure with her twin tails

┌─────────────────────────────────────────────────────────┐
│                        Vercel                           │
│  Flask app (serverless Python)                          │
│  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌────────┐  │
│  │  /main   │  │  /auth   │  │  /gifts  │  │ /rsvp  │  │
│  └────┬─────┘  └────┬─────┘  └────┬─────┘  └───┬────┘  │
└───────┼─────────────┼─────────────┼─────────────┼───────┘
        │             │             │             │
        ▼             ▼             ▼             ▼
┌───────────────┐            ┌───────────────────────────┐
│   Firebase    │            │         Stripe            │
│   Firestore   │            │  Checkout Sessions        │
│               │            │  Webhooks → Firestore     │
│  config/      │            └───────────────────────────┘
│   wedding     │
│  gifts/       │            ┌───────────────────────────┐
│  guests/      │            │        Cloudinary         │
│  rsvp/        │            │  Photo CDN (free tier)    │
│  messages/    │            │  URLs stored in Firestore │
└───────────────┘            └───────────────────────────┘
```

**Blueprints:** `main` · `auth` · `gifts` · `rsvp` · `messages`  
**Services:** `WeddingService` · `GiftService` · `AuthService` · `GuestService` · `RSVPService` · `MessagesService`  
**Config source of truth:** `config/wedding` document in Firestore — injected into every template via a Flask context processor.

---

## Local Development

### Prerequisites

- Python 3.12+
- A Firebase project with Firestore enabled (Spark plan — free)
- A Stripe account (test mode keys)
- A Cloudinary account (free tier)
- [Stripe CLI](https://stripe.com/docs/stripe-cli) for local webhook forwarding
- 一本のネギ (one leek, for good luck) 🌿

### Setup

```bash
# 1. Clone and create a virtual environment
git clone https://github.com/JuK-VT/commit-to-forever.git
cd commit-to-forever
python -m venv .venv
.venv\Scripts\activate        # Windows
# source .venv/bin/activate   # macOS / Linux

# 2. Install dependencies
pip install -r requirements.txt

# 3. Configure environment
cp .env.example .env
# Edit .env with your keys (see Environment Variables below)

# 4. Seed Firestore with placeholder wedding config
python dev/seed_wedding_once.py

# 5. Add missing photo fields (if upgrading an existing seed)
python dev/add_photo_fields.py

# 6. Start the Stripe CLI webhook forwarder (separate terminal)
stripe listen --forward-to localhost:5000/gifts/webhook

# 7. Run the app  🎵 *Miku starts playing in the background* 🎵
flask run
```

---

## Environment Variables

| Variable | Description |
|---|---|
| `FLASK_SECRET_KEY` | Flask session secret — generate with `python -c "import secrets; print(secrets.token_hex(32))"` |
| `FLASK_DEBUG` | Set to `true` for local development |
| `FIREBASE_CREDENTIALS` | Path to service account JSON (local) **or** the full JSON string (production) |
| `STRIPE_SECRET_KEY` | Stripe secret key (`sk_test_...` or `sk_live_...`) |
| `STRIPE_PUBLISHABLE_KEY` | Stripe publishable key (`pk_test_...` or `pk_live_...`) |
| `STRIPE_WEBHOOK_SECRET` | Webhook signing secret (`whsec_...`) — from Stripe CLI locally, from Stripe Dashboard in production |

> **Never commit `.env`.** It is gitignored. Store production secrets in Vercel's Environment Variables dashboard.

---

## Firestore Data Model

```
config/
  wedding             ← All site configuration (names, venues, dates, photos, dress code…)

gifts/
  {gift_id}           ← title, description, price, amount_funded, contributors[], is_funded, order

guests/
  {guest_id}          ← name, invite_code (hashed), is_attending

rsvp/
  {rsvp_id}           ← guest_name, attending, dietary, message, submitted_at

messages/
  {message_id}        ← guest_name, message, created_at
```

---

## Photo Management

Photos are hosted on **Cloudinary** (free tier — 25 GB storage / 25 GB bandwidth per month) and referenced by URL in the `config/wedding` Firestore document. Updating a photo requires no redeploy:

1. Upload the new image to your Cloudinary Media Library
2. Copy the direct image URL
3. Paste it into the corresponding field in the Firebase Console under `config → wedding`

| Firestore field | Location on site |
|---|---|
| `cover_photo` | Full-width parallax band |
| `hero_photo_left` | Hero section — left portrait |
| `hero_photo_right` | Hero section — right portrait |
| `story_photo_main` | "Nuestra historia" — large photo |
| `story_photo_accent` | "Nuestra historia" — accent photo |

---

## Stripe Payments

Gifts support two contribution modes:

- **Full purchase** — guest pays the exact listed price; gift is marked as fully funded
- **Partial contribution** — guest chooses any amount ≥ $50 MXN; multiple guests can co-fund a gift

All payments go through **Stripe Checkout** (hosted). The webhook at `/gifts/webhook` listens for `checkout.session.completed` events and updates Firestore atomically using `Increment` and `ArrayUnion`.

In production, register the webhook at `https://your-domain.vercel.app/gifts/webhook` in the [Stripe Dashboard](https://dashboard.stripe.com/webhooks) and listen for the `checkout.session.completed` event.

---

## Deployment (Vercel)

```bash
npm i -g vercel
vercel --prod
```

Set all environment variables listed above in the Vercel Dashboard under **Settings → Environment Variables**. The `vercel.json` at the repo root configures the serverless Python runtime automatically.

---

## Security Notes

- All guest routes require an active session (`session['guest_name']`)
- Invite codes are stored **hashed** with bcrypt — plaintext codes never persist
- Stripe webhook signatures are verified via `stripe.Webhook.construct_event` before any Firestore write
- No personal data lives in the repository — all configuration is in Firestore, all secrets in environment variables
- Firebase service account credentials are gitignored (`*serviceAccount*.json`)

---

<div align="center">

```
／人◕ ‿‿ ◕人＼  ミクミク に してあげる♪
```

*Built with Flask, Firebase, Stripe, and an unreasonable amount of care.*

*This repository is protected by Hatsune Miku. Unauthorised forks will be serenaded.*

<sub>初音ミク is watching over this repo 🎋 — BPM: 39C5BB</sub>

</div>
