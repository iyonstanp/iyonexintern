from content_helpers import section_head, tile, grid, process_step, process, cta_band, hero_3d

PAGES_AMR = []

body = f"""
  <section class="hero" style="padding-bottom:0;">
    <div class="aurora"></div>
    <div class="blueprint-bg"></div>
    <div class="wrap hero-inner" style="position:relative;z-index:1;">
      <div>
        <div class="hero-tag reveal"><span class="dot"></span>AMR PLATFORM · IN DEVELOPMENT</div>
        <h1 class="h1 grad-text reveal" style="font-size:clamp(2.2rem,4.4vw,3.6rem);">Move materials. Not people.</h1>
        <h2 style="color:var(--text-dim);font-weight:600;font-size:1.1rem;margin-bottom:20px;" class="reveal">Iyonex Autonomous Material Movement Platform</h2>
        <p class="hero-sub reveal">We are developing an easy-to-use AMR platform for repetitive material transport in small and medium factories. The goal: straightforward mapping, destination selection and operator controls, without a specialist supervising every task.</p>
        <div class="btn-row reveal">
          <a href="contact.html" class="btn btn-primary">Talk to Iyonex <span class="arrow" aria-hidden="true">&rarr;</span></a>
          <a href="technology.html" class="btn btn-ghost">See the Technology</a>
        </div>
      </div>
      <div class="hero-3d reveal">{hero_3d("SENSORS: ONLINE", "FLEET: COORDINATED")}</div>
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      {section_head("DEVELOPMENT ROADMAP", "A practical roadmap for factory movement.",
                     "The features below describe our development direction. Availability and validation status must be confirmed for each pilot; they are not a claim of deployed functionality.")}
      {grid(3, [
        tile("", "Autonomous Navigation", "Robots plan and follow routes across the facility without fixed rails or wires."),
        tile("", "Obstacle Detection", "Sensors continuously scan the environment to identify people, equipment and obstructions."),
        tile("", "Dynamic Path Planning", "Routes are recalculated on the fly as the floor layout or traffic changes."),
        tile("", "Point-to-Point Transportation", "Materials move directly between defined pickup and drop-off locations."),
        tile("", "Material Handling", "Interfaces designed around how materials are actually loaded and unloaded on your floor."),
        tile("", "Multi-Robot Coordination", "Multiple units share the floor and coordinate to avoid conflicts and bottlenecks."),
        tile("", "Real-Time Monitoring", "Operators can see robot status, location and task progress as it happens."),
        tile("", "Factory Workflow Integration", "The platform is designed to connect with existing production and logistics workflows."),
        tile("", "Scalable Deployment", "Start with a single unit or route, and expand coverage as requirements grow."),
      ])}
      <p class="placeholder-note reveal" style="margin-top:24px;">Payload, dimensions, runtime, navigation accuracy and safety validation are not yet published. Discuss the current prototype and pilot fit with our team before making a procurement decision.</p>
    </div>
  </section>

  <section class="section section--tight" style="background:var(--bg-raised);border-top:1px solid var(--line-soft);border-bottom:1px solid var(--line-soft);">
    <div class="wrap">
      {section_head("HOW IT OPERATES", "Perception, planning and action, in a continuous loop.",
                     "An illustrative operating model for the platform under development.")}
      {process([
        process_step("01", "Sense", "Onboard sensors build a live picture of the surrounding floor, racks and moving obstacles."),
        process_step("02", "Localize", "The robot determines exactly where it is on the facility map in real time."),
        process_step("03", "Plan", "A path to the next pickup or drop-off point is calculated, accounting for traffic and obstacles."),
        process_step("04", "Act", "The robot moves, adjusting speed and route continuously as conditions change."),
        process_step("05", "Report", "Task status and location are reported back to the fleet monitoring layer."),
      ])}
    </div>
  </section>

  <section class="section">
    <div class="wrap">
      {section_head("WHERE IT FITS", "Built for repetitive, high-friction material flows.", "")}
      {grid(4, [
        tile("", "Automotive", "Line-side component delivery and intra-factory logistics."),
        tile("", "Manufacturing", "Raw material, WIP and finished-goods transportation."),
        tile("", "Electronics", "Controlled movement between sensitive process stages."),
        tile("", "Warehousing", "Repetitive transportation across storage and dispatch zones."),
      ])}
    </div>
  </section>

  {cta_band("Explore the AMR platform for your factory.",
            "Share your material movement challenge and we&rsquo;ll help you evaluate where autonomous transportation fits.",
            "Discuss a Pilot", "contact.html", "Explore All Solutions", "solutions.html")}
"""

PAGES_AMR.append(("amr.html", {
    "title": "Autonomous Mobile Robots (AMR) | Iyonex Automation",
    "desc": "Iyonex is developing an easy-to-use AMR platform for material movement in small and medium factories. Explore the concept and discuss pilot requirements.",
    "active": "solutions",
}, body))

