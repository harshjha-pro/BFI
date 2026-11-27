# signup edge function

Creates a customer account that is confirmed at once (no email needed), saves the name and optional mobile number, and limits sign-ups to 5 per hour per connection (hashed IP, `signup_rate_check`).

Allowed browser origins: https://bfiluxe.com, https://www.bfiluxe.com (plus the old Vercel address and http://localhost:8765 for testing). The deployed source (version 4) is in `index.ts` next to this file.
