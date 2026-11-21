# IYONEX Automation website

Static website for robotics, an AMR platform under development, embedded engineering, internships and institution workshops.

## Build
Run `python build.py` after editing the shared generator or content modules. Deploy the project root to the existing static host. Run `python -m http.server 8080` for local preview. CSS and JavaScript are checked in; no npm build is required.

Shared business details are in content_business.py, styles in css/style.css and navigation/email draft handling in js/main.js.

## Enquiries
Contact, internship and workshop forms prepare a draft addressed to ceo@iyonex.com. Visitors review it, open their email app or copy the text, and send it themselves. The page never reports successful delivery. No submissions or resumes are stored in localStorage or a website database. Applicants attach their PDF resume in their email app.

Automatic delivery and a shared inbox dashboard are not configured. Provision a server-side form service or endpoint, configure credentials outside the public repository, add abuse controls and server-side validation, and verify delivery before changing the UI to say submitted. Update the privacy notice accordingly.

The former client-side staff login and local-only dashboard are retired. Legacy admin URLs show a noindex information page with no login credentials. robots.txt is a crawl directive, not access control.

## Content
- AMR features are development goals, not validated commercial specifications. The SVG hero is illustrative, not live telemetry.
- Confirm learning dates, eligibility, duration, prices, fees/stipends and certificates before booking.
- Unsplash images are illustrative. Add consented real prototype and workshop photographs when available.
- Google Fonts and Unsplash receive external requests; system fonts are the fallback.
- The generator outputs unique canonical URLs and a complete public sitemap.
- A GitHub commit does not prove www.iyonex.com has deployed. Check the existing hosting deployment before announcing it live.


## Razorpay checkout (test mode setup)

A dedicated `payment.html` page is backed by two Vercel Python Functions:
- `POST /api/create-order` validates the supplied INR amount and reference, then creates a Razorpay order using server-side environment variables.
- `POST /api/verify-payment` validates the HMAC-SHA256 signature, checks that the payment belongs to the supplied order, and confirms the amount/currency and captured status with Razorpay.

Set these variables in Vercel Project Settings → Environment Variables (never commit a `.env` file):
- `RAZORPAY_KEY_ID`
- `RAZORPAY_KEY_SECRET` (sensitive)

The browser receives only the Key ID. Rotate any key secret that has been pasted into a chat, ticket, source file or other shared location. Use Razorpay test credentials for the first deployment. Run a live payment only after validating all test cases, configuring live credentials, and confirming the invoice / fee process.

The payment page is an invoice-reference checkout, not an invoice database. The payer enters the exact amount and reference from an IYONEX-issued invoice or written fee confirmation. The backend does not currently compare that reference to an internal billing ledger, because this site has no payment database. Reconcile captured payments against the issued invoice before marking an invoice settled.

Local preview of the static website: `python -m http.server 8080`. The `/api` routes require the Vercel Functions runtime; test them with `vercel dev` after installing the Vercel CLI and configuring local environment variables.
