-- Partner enquiries
alter table public.enquiries drop constraint if exists enquiries_source_check;
alter table public.enquiries add constraint enquiries_source_check check (source in ('contact','details','customize','partner'));

-- Sign-up rate limiting (used by the signup edge function; no public access)
create table public.signup_attempts (
  id bigint generated always as identity primary key,
  ip_hash text not null check (char_length(ip_hash) <= 64),
  created_at timestamptz not null default now()
);
alter table public.signup_attempts enable row level security;
create index signup_attempts_ip_time_idx on public.signup_attempts(ip_hash, created_at desc);

create or replace function public.signup_rate_check(p_hash text, p_limit int)
returns boolean language plpgsql security definer set search_path = '' as $$
declare n int;
begin
  perform pg_advisory_xact_lock(hashtext(p_hash));
  select count(*) into n from public.signup_attempts where ip_hash = p_hash and created_at > now() - interval '1 hour';
  if n >= p_limit then return false; end if;
  insert into public.signup_attempts (ip_hash) values (p_hash);
  return true;
end $$;
revoke execute on function public.signup_rate_check(text, int) from public, anon, authenticated;
grant execute on function public.signup_rate_check(text, int) to service_role;
