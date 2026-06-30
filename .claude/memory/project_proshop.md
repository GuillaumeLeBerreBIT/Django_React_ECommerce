---
name: Project — ProShop Course Log
description: Django+React e-commerce Udemy course tracking, learning log maintained in NOTES.md
type: project
---

User is following this Udemy course: https://www.udemy.com/course/django-with-react-an-ecommerce-website/

A `NOTES.md` file exists at the project root:
`/Users/guillaumeleberre/GuillaumesLab/WebDevelopment/Django_W_React_ECommerice_Udemy/NOTES.md`

**Why:** User wants a personal reference doc that explains the project end-to-end — concepts, decisions, code structure — built up section by section as the course progresses.

**How to apply:** After each course section, when the user asks for a summary:
1. Read all recently changed/added files
2. Summarize what was built, why, and key concepts learned
3. Append a new section to `NOTES.md` following the existing format (section heading, files created, code snippets with explanations, key concepts)

**Current progress (as of 2026-06-30): COURSE COMPLETE — all 12 sections watched.**
- Sections 1–12 all documented in NOTES.md (scaffold → frontend → Django/DRF backend → Redux → cart → JWT auth → checkout → orders → admin CRUD → search/pagination → top-rated carousel).
- NOTES.md ends with a "Course Wrap-Up — End-to-End Architecture Recap" tying every slice/endpoint/component together.
- Last feature added: Top-Rated Products Carousel (backend `TopProduct` view at `top/`, `productTopRated` Redux slice, `ProductCarousel.jsx`). Changes were uncommitted at time of writing.
- Flagged two harmless code issues to the user in NOTES.md: `reqeust` typo in `TopProduct.get`, and dead `className="carousel.caption"` in ProductCarousel.jsx.

**Next time:** the section-by-section log is finished. Future asks are likely refactors, bug fixes, deployment, or revisiting concepts — not new course sections.
