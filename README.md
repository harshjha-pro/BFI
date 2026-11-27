# Bfiluxe website

This branch (`main`) is the live website for **https://bfiluxe.com**. Every file here is served exactly as it is.

- **Hosting:** Hostinger (Git deployment from this branch into `public_html`).
- **Server settings:** `.htaccess` (https and bare-domain redirect, 404 page, cache and security headers).
- **Source:** the page builder, docs, brand files and art live on the `source` branch. Pages are rebuilt there with `python3 tools/build_website.py`, then the `site/` folder is copied here.
- **Admin:** the `admin/` folder is the private admin studio. It's served at `https://admin.bfiluxe.com` (a Hostinger subdomain pointing at `public_html/admin`) and also works at `https://bfiluxe.com/admin/`. All protection is in the database: an admin account plus two-step sign-in.
