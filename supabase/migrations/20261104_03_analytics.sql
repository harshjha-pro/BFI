-- First-party, cookie-free usage events. Visitors can only insert; only the studio (dashboard) can read.
create table public.analytics_events (
  id bigint generated always as identity primary key,
  name text not null check (name ~ '^[a-z_]{2,40}$'),
  page text check (char_length(page) <= 120),
  meta jsonb not null default '{}'::jsonb check (pg_column_size(meta) < 1000),
  sid text check (char_length(sid) <= 20),
  created_at timestamptz not null default now()
);
alter table public.analytics_events enable row level security;
create policy "analytics: anyone can record" on public.analytics_events for insert to anon, authenticated with check (true);
create index analytics_events_name_time_idx on public.analytics_events(name, created_at desc);

create view public.analytics_funnel_daily with (security_invoker = true) as
select date_trunc('day', created_at)::date as day, name, count(*) as events, count(distinct sid) as sessions
from public.analytics_events group by 1, 2;
revoke all on public.analytics_funnel_daily from anon, authenticated;
