from content_helpers import section_head, tile, grid, cta_band
from content_images import IMG_TEAM_ENGINEERING, IMG_ROBOT_ARM_BLUE
from content_business import (
    COMPANY_NAME, COMPANY_EMAIL, COMPANY_PHONE, COMPANY_PHONE_TEL,
    COMPANY_ADDRESS_FULL, COMPANY_LINKEDIN,
)

PAGES_AC = []

# ------------------------------------------------------------------ ABOUT
about_body = f"""
  <section class="hero" style="padding-bottom:20px;">
    <div class="aurora"></div>
    <div class="blueprint-bg"></div>
    <div class="wrap" style="position:relative;z-index:1;max-width:780px;">
      <div class="eyebrow reveal">ABOUT</div>
      <h1 class="h1 grad-text reveal" style="font-size:clamp(2.2rem,4.4vw,3.4rem);">Engineering the future of industrial automation.</h1>
      <p class="hero-sub reveal">Iyonex Automation is a robotics and industrial automation company focused on developing intelligent solutions for modern manufacturing and industrial environments.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid-2" style="align-items:center;">
      <div class="reveal">
        <p class="body-copy" style="margin-bottom:22px;max-width:none;">Our work spans Autonomous Mobile Robots, robotics, embedded systems, industrial automation and intelligent material movement.</p>
        <p class="body-copy" style="max-width:none;">We focus on solving practical industrial problems through engineering-driven innovation.</p>
      </div>
      <div class="reveal" style="border:1px solid var(--line);overflow:hidden;box-shadow:0 24px 60px -24px rgba(46,60,90,0.18);aspect-ratio:4/3;">
        <img src="{IMG_TEAM_ENGINEERING}" alt="Engineers reviewing technical work together" style="width:100%;height:100%;object-fit:cover;display:block;">
      </div>
    </div>
  </section>

  <section class="section section--tight" style="background:var(--bg-raised);border-top:1px solid var(--line-soft);border-bottom:1px solid var(--line-soft);">
    <div class="wrap grid-2" style="align-items:center;">
      <div class="reveal" style="border:1px solid var(--line);overflow:hidden;box-shadow:0 24px 60px -24px rgba(46,60,90,0.18);aspect-ratio:4/3;order:2;">
        <img src="{IMG_ROBOT_ARM_BLUE}" alt="Industrial robot arm operating on a factory floor" style="width:100%;height:100%;object-fit:cover;display:block;">
      </div>
      <div class="reveal" style="order:1;">
        <div class="eyebrow">HOW WE BUILD</div>
        <h2 class="h2" style="font-size:clamp(1.6rem,2.6vw,2.1rem);margin-bottom:18px;">One engineering ecosystem, not a patchwork of vendors.</h2>
        <p class="body-copy" style="max-width:none;">Hardware, embedded systems, robotics, automation and software are developed together, so a solution that works on a bench is designed from day one to keep working on a factory floor.</p>
      </div>
    </div>
  </section>

  <section class="section">
    <div class="wrap" style="max-width:780px;">
      <p class="h2 reveal" style="font-size:clamp(1.5rem,2.6vw,2rem);line-height:1.35;margin-bottom:40px;">Build technology that works beyond the laboratory and creates measurable value in the real world.</p>
      <div class="note-box reveal">
        <h3>Iyonstan P · Founder</h3><p>Iyonstan brings practical experience in robotics, embedded systems, IoT prototyping and student technical training. His work includes mobile robot development, microcontroller systems and hands-on engineering workshops.</p><p>IYONEX is building toward accessible automation for small factories, combining product development with practical technical learning.</p><a class="tile-link" href="{COMPANY_LINKEDIN}" target="_blank" rel="noopener">Meet the founder on LinkedIn &rarr;</a>
      </div>
    </div>
  </section>

  {cta_band("Want to know more about our engineering approach?",
            "We&rsquo;re happy to walk through how we&rsquo;d approach your specific automation challenge.",
            "Talk to Iyonex", "contact.html", "Explore Solutions", "solutions.html")}
"""

PAGES_AC.append(("about.html", {
    "title": "About | Iyonex Automation",
    "desc": "Iyonex Automation is a robotics and industrial automation company engineering intelligent solutions for modern manufacturing.",
    "active": "about",
}, about_body))

# --------------------------------------------------------------- CONTACT
contact_body = f"""
  <section class="hero" style="padding-bottom:20px;">
    <div class="aurora"></div>
    <div class="blueprint-bg"></div>
    <div class="wrap" style="position:relative;z-index:1;max-width:760px;">
      <div class="eyebrow reveal">CONTACT</div>
      <h1 class="h1 grad-text reveal" style="font-size:clamp(2.2rem,4.4vw,3.4rem);">Let&rsquo;s build the future of automation.</h1>
      <p class="hero-sub reveal">Have an automation challenge? Tell us about your process, factory or robotics requirement.</p>
    </div>
  </section>

  <section class="section">
    <div class="wrap grid-2">
      <form class="reveal" action="mailto:ceo@iyonex.com" method="post" enctype="text/plain" data-email-form data-enquiry="contact">
        <div class="form-grid">
          <div class="field"><label for="c-name">Name</label><input id="c-name" name="name" type="text" required></div>
          <div class="field"><label for="c-company">Company</label><input id="c-company" name="company" type="text"></div>
          <div class="field"><label for="c-email">Work Email</label><input id="c-email" name="email" type="email" required></div>
          <div class="field"><label for="c-phone">Phone</label><input id="c-phone" name="phone" type="tel"></div>
          <div class="field full"><label for="c-industry">Industry</label><input id="c-industry" name="industry" type="text"></div>
          <div class="field full">
            <label for="c-requirement">Requirement</label>
            <select id="c-requirement" name="requirement">
              <option>Autonomous Mobile Robots</option>
              <option>Industrial Automation</option>
              <option>Factory Integration</option>
              <option>Robotics Software</option>
              <option>Workshop / Internship</option>
              <option>Other</option>
            </select>
          </div>
          <div class="field full"><label for="c-message">Message</label><textarea id="c-message" name="message"></textarea></div>
        </div>
        <button type="submit" class="btn btn-primary" style="margin-top:26px;">Prepare Enquiry Email</button>
        <p class="form-status" style="display:none;margin-top:16px;color:var(--text-dim);font-size:0.9rem;"></p>
      </form>

      <div class="reveal">
        <div class="tile tile--glass" style="margin-bottom:24px;">
          <h3 style="margin-bottom:20px;">{COMPANY_NAME}</h3>
          <p style="margin-bottom:14px;color:var(--text-dim);display:flex;gap:10px;"><span style="color:var(--blue);">&#9679;</span> {COMPANY_ADDRESS_FULL}</p>
          <p style="margin-bottom:14px;color:var(--text-dim);display:flex;gap:10px;"><span style="color:var(--blue);">&#9679;</span> <a href="mailto:{COMPANY_EMAIL}" style="color:var(--text-dim);">{COMPANY_EMAIL}</a></p>
          <p style="margin-bottom:14px;color:var(--text-dim);display:flex;gap:10px;"><span style="color:var(--blue);">&#9679;</span> <a href="tel:{COMPANY_PHONE_TEL}" style="color:var(--text-dim);">{COMPANY_PHONE}</a></p>
          <p style="color:var(--text-dim);display:flex;gap:10px;"><span style="color:var(--blue);">&#9679;</span> <a href="{COMPANY_LINKEDIN}" target="_blank" rel="noopener" style="color:var(--text-dim);">Founder on LinkedIn</a></p>
        </div>
        <div class="note-box">
          This form prepares an email draft addressed to ceo@iyonex.com. Send it from your email app to contact us. No enquiry is submitted automatically. You can also call directly. <a href="privacy.html">Privacy notice</a>.
        </div>
      </div>
    </div>
  </section>
"""

PAGES_AC.append(("contact.html", {
    "title": "Contact | Iyonex Automation",
    "desc": "Get in touch with Iyonex Automation about robotics, industrial automation, workshops or internship opportunities.",
    "active": "contact",
}, contact_body))

# ------------------------------------------------------------------- 404
notfound_body = """
  <section class="notfound">
    <div class="blueprint-bg"></div>
    <div style="position:relative;z-index:1;">
      <div class="notfound-code reveal">404</div>
      <h1 class="h2 reveal" style="margin-bottom:14px;">This route isn&rsquo;t mapped.</h1>
      <p class="lede reveal" style="margin:0 auto 30px;">The page you&rsquo;re looking for doesn&rsquo;t exist, or may have moved.</p>
      <div class="btn-row reveal" style="justify-content:center;">
        <a href="index.html" class="btn btn-primary">Back to Home</a>
        <a href="contact.html" class="btn btn-ghost">Talk to Iyonex</a>
      </div>
    </div>
  </section>
"""

PAGES_AC.append(("404.html", {
    "title": "Page Not Found | Iyonex Automation",
    "desc": "This page could not be found.",
    "active": "",
}, notfound_body))


privacy_body = """
<section class="hero"><div class="wrap"><div class="eyebrow">PRIVACY</div><h1 class="h1">Your enquiry, handled clearly.</h1><p class="lede">Last updated: 18 October 2026</p></div></section>
<section class="section"><div class="wrap" style="max-width:780px;">
<h2 class="h2">Enquiry information</h2><p class="body-copy">Our enquiry forms prepare an email draft on your device. The website does not save form entries or resumes in a database or browser storage. Information reaches Iyonex only when you send the email yourself. You may contact us directly instead of using a form.</p>
<h3>How we use information you send</h3><p class="body-copy">We use your name, contact details, requirements and any resume you choose to send to respond to your enquiry, discuss a project or review your interest in a learning program. Please do not include passwords, identity documents or other information unrelated to your enquiry.</p>
<h3>Third-party services</h3><p class="body-copy">Your email provider handles the email draft and delivery under its own policies. Fonts load from Google Fonts, and some illustrative images load from Unsplash; those requests disclose connection information to that provider. Hosting providers may keep operational access logs. External social links have their own privacy practices.</p>
<h3>Questions or deletion requests</h3><p class="body-copy">Email <a href="mailto:ceo@iyonex.com">ceo@iyonex.com</a> to ask about information you have sent, request a correction or request deletion. We retain correspondence as needed to handle the enquiry and any resulting business relationship.</p>
</div></section>
"""
PAGES_AC.append(("privacy.html", {"title":"Privacy | Iyonex Automation", "desc":"How Iyonex Automation handles enquiry information and email-based internship and workshop requests.", "active":""}, privacy_body))
