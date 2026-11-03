-- Customer reviews: written by signed-in customers, shown publicly only after the studio approves them.
create table public.reviews (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade default auth.uid(),
  name text not null check (char_length(name) between 1 and 80),
  city text check (char_length(city) <= 60),
  design_slug text references public.invitations(slug) on delete set null,
  rating smallint not null check (rating between 1 and 5),
  body text not null check (char_length(body) between 10 and 800),
  approved boolean not null default false,
  created_at timestamptz not null default now()
);
alter table public.reviews enable row level security;
create policy "reviews: public read approved" on public.reviews for select to anon, authenticated using (approved);
create policy "reviews: read own" on public.reviews for select to authenticated using (user_id = (select auth.uid()));
create policy "reviews: write own, unapproved" on public.reviews for insert to authenticated
  with check (user_id = (select auth.uid()) and approved = false);
create index reviews_user_idx on public.reviews(user_id);
create index reviews_design_idx on public.reviews(design_slug);
create index reviews_approved_idx on public.reviews(approved, created_at desc);
