-- Bfiluxe admin: roles, editable prices/settings, lead tracking, audit log.
-- Admin access needs BOTH: the user is listed in private.admins AND the session
-- passed two-factor authentication (JWT aal = 'aal2').

create schema if not exists private;
revoke all on schema private from public, anon;
grant usage on schema private to authenticated;

create table if not exists private.admins (
  user_id uuid primary key references auth.users(id) on delete cascade,
  created_at timestamptz not null default now()
);
revoke all on private.admins from public, anon, authenticated;

create or replace function private.is_admin() returns boolean
language sql stable security definer set search_path = '' as $$
  select exists (select 1 from private.admins a where a.user_id = (select auth.uid()))
     and coalesce((select auth.jwt()) ->> 'aal', '') = 'aal2';
$$;
revoke all on function private.is_admin() from public, anon;
grant execute on function private.is_admin() to authenticated;

-- Tells the admin page whether this account is an admin (before 2FA too), nothing else.
create or replace function public.admin_whoami() returns json
language sql stable security definer set search_path = '' as $$
  select json_build_object(
    'listed', exists (select 1 from private.admins a where a.user_id = (select auth.uid())),
    'aal', coalesce((select auth.jwt()) ->> 'aal', ''));
$$;
revoke all on function public.admin_whoami() from public, anon;
grant execute on function public.admin_whoami() to authenticated;

-- ---------- Site settings (prices, offer bar) ----------
create table if not exists public.site_settings (
  key text primary key check (key ~ '^[a-z_]{2,40}$'),
  value jsonb not null check (pg_column_size(value) < 8000),
  updated_at timestamptz not null default now(),
  updated_by uuid default auth.uid()
);
alter table public.site_settings enable row level security;
drop policy if exists "settings: public read" on public.site_settings;
create policy "settings: public read" on public.site_settings for select to anon, authenticated using (true);
drop policy if exists "settings: admin write" on public.site_settings;
create policy "settings: admin write" on public.site_settings for all to authenticated
  using ((select private.is_admin())) with check ((select private.is_admin()));
revoke all on public.site_settings from anon;
grant select on public.site_settings to anon;
grant select, insert, update, delete on public.site_settings to authenticated;

insert into public.site_settings (key, value) values
 ('packages', '{"Basic":{"price":3999,"mrp":5999,"days":"3–5 working days"},"Premium":{"price":8999,"mrp":14999,"days":"7–14 working days"},"Luxury":{"price":24999,"mrp":35999,"days":"15–21 working days"}}'),
 ('video_packages', '{"Basic":{"price":1499,"mrp":2499,"days":"2–3 working days"},"Premium":{"price":2499,"mrp":3999,"days":"2–3 working days"},"Luxury":{"price":3999,"mrp":5999,"days":"2–3 working days"}}'),
 ('announcement', '{"on":false,"text":"","link":""}')
on conflict (key) do nothing;

-- ---------- Lead and order tracking ----------
alter table public.enquiries add column if not exists admin_note text check (char_length(admin_note) <= 2000);
alter table public.enquiries add column if not exists deal_value integer check (deal_value between 0 and 10000000);
alter table public.enquiries add column if not exists advance_paid integer check (advance_paid between 0 and 10000000);
alter table public.enquiries add column if not exists updated_at timestamptz;
alter table public.customizations add column if not exists admin_note text check (char_length(admin_note) <= 2000);

alter table public.customizations drop constraint if exists customizations_status_check;
alter table public.customizations add constraint customizations_status_check
  check (status in ('draft','submitted','in_progress','preview_sent','approved','delivered','cancelled'));

-- Visitors may only create NEW enquiries (no setting status, notes or money).
drop policy if exists "enquiries: anyone can create" on public.enquiries;
create policy "enquiries: anyone can create" on public.enquiries for insert to anon, authenticated
  with check (((user_id is null) or (user_id = (select auth.uid())))
              and status = 'new' and admin_note is null and deal_value is null and advance_paid is null);

-- Customers may only move their own order between draft and submitted.
drop policy if exists "customizations: create own" on public.customizations;
create policy "customizations: create own" on public.customizations for insert to authenticated
  with check (user_id = (select auth.uid()) and status in ('draft','submitted') and admin_note is null);
drop policy if exists "customizations: update own" on public.customizations;
create policy "customizations: update own" on public.customizations for update to authenticated
  using (user_id = (select auth.uid()) and status in ('draft','submitted'))
  with check (user_id = (select auth.uid()) and status in ('draft','submitted') and admin_note is null);

-- ---------- Admin access to every table ----------
do $$
declare t text;
begin
  foreach t in array array['enquiries','customizations','reviews','profiles','favorites','invitations'] loop
    execute format('drop policy if exists "admin: read all" on public.%I', t);
    execute format('create policy "admin: read all" on public.%I for select to authenticated using ((select private.is_admin()))', t);
  end loop;
end $$;

drop policy if exists "admin: update" on public.enquiries;
create policy "admin: update" on public.enquiries for update to authenticated using ((select private.is_admin())) with check ((select private.is_admin()));
drop policy if exists "admin: delete" on public.enquiries;
create policy "admin: delete" on public.enquiries for delete to authenticated using ((select private.is_admin()));
drop policy if exists "admin: update" on public.customizations;
create policy "admin: update" on public.customizations for update to authenticated using ((select private.is_admin())) with check ((select private.is_admin()));
drop policy if exists "admin: update" on public.reviews;
create policy "admin: update" on public.reviews for update to authenticated using ((select private.is_admin())) with check ((select private.is_admin()));
drop policy if exists "admin: delete" on public.reviews;
create policy "admin: delete" on public.reviews for delete to authenticated using ((select private.is_admin()));
drop policy if exists "admin: update" on public.invitations;
create policy "admin: update" on public.invitations for update to authenticated using ((select private.is_admin())) with check ((select private.is_admin()));
grant update, delete on public.enquiries to authenticated;
grant update on public.customizations, public.reviews, public.invitations to authenticated;
grant delete on public.reviews to authenticated;

-- ---------- Audit log: every admin change is recorded ----------
create table if not exists private.audit_log (
  id bigint generated always as identity primary key,
  at timestamptz not null default now(),
  user_id uuid default auth.uid(),
  tbl text not null,
  action text not null,
  row_key text,
  old_row jsonb,
  new_row jsonb
);
revoke all on private.audit_log from public, anon, authenticated;

create or replace function private.audit() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  if (select private.is_admin()) then
    insert into private.audit_log (tbl, action, row_key, old_row, new_row)
    values (tg_table_name, tg_op,
            coalesce(to_jsonb(new) ->> 'id', to_jsonb(new) ->> 'slug', to_jsonb(new) ->> 'key', to_jsonb(old) ->> 'id', to_jsonb(old) ->> 'slug', to_jsonb(old) ->> 'key'),
            case when tg_op <> 'INSERT' then to_jsonb(old) end,
            case when tg_op <> 'DELETE' then to_jsonb(new) end);
  end if;
  return coalesce(new, old);
end $$;
revoke all on function private.audit() from public, anon, authenticated;

do $$
declare t text;
begin
  foreach t in array array['site_settings','enquiries','customizations','reviews','invitations'] loop
    execute format('drop trigger if exists audit_admin on public.%I', t);
    execute format('create trigger audit_admin after insert or update or delete on public.%I for each row execute function private.audit()', t);
  end loop;
end $$;

create or replace function public.admin_audit(p_limit integer default 50) returns setof json
language plpgsql stable security definer set search_path = '' as $$
begin
  if not (select private.is_admin()) then raise exception 'not allowed' using errcode = '42501'; end if;
  return query select json_build_object('at', a.at, 'tbl', a.tbl, 'action', a.action, 'row_key', a.row_key,
                                        'who', u.email, 'old', a.old_row, 'new', a.new_row)
    from private.audit_log a left join auth.users u on u.id = a.user_id
    order by a.at desc limit least(greatest(p_limit, 1), 200);
end $$;
revoke all on function public.admin_audit(integer) from public, anon;
grant execute on function public.admin_audit(integer) to authenticated;

-- ---------- Admin reads: customers and analytics ----------
create or replace function public.admin_customers() returns setof json
language plpgsql stable security definer set search_path = '' as $$
begin
  if not (select private.is_admin()) then raise exception 'not allowed' using errcode = '42501'; end if;
  return query select json_build_object('id', u.id, 'email', u.email, 'created_at', u.created_at, 'last_sign_in_at', u.last_sign_in_at,
      'provider', u.raw_app_meta_data ->> 'provider', 'name', p.full_name, 'phone', p.phone,
      'orders', (select count(*) from public.customizations c where c.user_id = u.id),
      'favorites', (select count(*) from public.favorites f where f.user_id = u.id))
    from auth.users u left join public.profiles p on p.id = u.id order by u.created_at desc limit 1000;
end $$;
revoke all on function public.admin_customers() from public, anon;
grant execute on function public.admin_customers() to authenticated;

create or replace function public.admin_stats(p_days integer default 30) returns json
language plpgsql stable security definer set search_path = '' as $$
declare d integer := least(greatest(p_days, 1), 365); since timestamptz := now() - make_interval(days => d); r json;
begin
  if not (select private.is_admin()) then raise exception 'not allowed' using errcode = '42501'; end if;
  select json_build_object(
    'days', d,
    'views', (select count(*) from public.analytics_events where name = 'page_view' and created_at >= since),
    'visitors', (select count(distinct sid) from public.analytics_events where created_at >= since),
    'views_prev', (select count(*) from public.analytics_events where name = 'page_view' and created_at >= since - make_interval(days => d) and created_at < since),
    'enquiries', (select count(*) from public.enquiries where created_at >= since),
    'enquiries_new', (select count(*) from public.enquiries where status = 'new'),
    'won', (select count(*) from public.enquiries where status = 'won'),
    'revenue', (select coalesce(sum(deal_value), 0) from public.enquiries where status = 'won'),
    'advance', (select coalesce(sum(advance_paid), 0) from public.enquiries),
    'orders', (select count(*) from public.customizations where status <> 'draft'),
    'drafts', (select count(*) from public.customizations where status = 'draft'),
    'users', (select count(*) from auth.users),
    'users_new', (select count(*) from auth.users where created_at >= since),
    'reviews_pending', (select count(*) from public.reviews where not approved),
    'daily', (select coalesce(json_agg(x order by x.day), '[]') from (
        select (created_at at time zone 'Asia/Kolkata')::date as day, count(*) filter (where name = 'page_view') as views, count(distinct sid) as visitors
        from public.analytics_events where created_at >= since group by 1) x),
    'pages', (select coalesce(json_agg(x), '[]') from (
        select case when page in ('/', '/index.html', '/index') then '/' else page end as page, count(*) as views from public.analytics_events where name = 'page_view' and created_at >= since
        group by 1 order by 2 desc limit 12) x),
    'events', (select coalesce(json_agg(x), '[]') from (
        select name, count(*) as n from public.analytics_events where name <> 'page_view' and created_at >= since
        group by name order by 2 desc limit 15) x),
    'referrers', (select coalesce(json_agg(x), '[]') from (
        select coalesce(nullif(meta ->> 'ref', ''), 'Direct / WhatsApp') as ref, count(*) as n from public.analytics_events
        where name = 'page_view' and created_at >= since
          and coalesce(meta ->> 'ref', '') not in ('bfiluxe.com', 'www.bfiluxe.com', 'admin.bfiluxe.com', 'bfi-royal-heritage.vercel.app')
          and coalesce(meta ->> 'ref', '') not like 'bfi-royal-heritage-%.vercel.app'
        group by 1 order by 2 desc limit 8) x),
    'designs', (select coalesce(json_agg(x), '[]') from (
        select i.slug, i.name, i.tier, i.price_from, i.image,
               (select count(*) from public.analytics_events e where e.name = 'page_view' and e.page like '%design-' || i.slug || '%' and e.created_at >= since) as views,
               (select count(*) from public.enquiries q where q.design_slug = i.slug) as enquiries,
               (select count(*) from public.favorites f where f.slug = i.slug) as favorites
        from public.invitations i order by 6 desc, i.sort) x)
  ) into r;
  return r;
end $$;
revoke all on function public.admin_stats(integer) from public, anon;
grant execute on function public.admin_stats(integer) to authenticated;
