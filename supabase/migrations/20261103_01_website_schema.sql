-- BFI Royal Heritage website: schema, row-level security and catalogue seed.

-- Profiles (one per signed-in user)
create table public.profiles (
  id uuid primary key references auth.users(id) on delete cascade,
  full_name text check (char_length(full_name) <= 120),
  phone text check (char_length(phone) <= 20),
  created_at timestamptz not null default now()
);
alter table public.profiles enable row level security;
create policy "profiles: read own" on public.profiles for select to authenticated using ((select auth.uid()) = id);
create policy "profiles: update own" on public.profiles for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

create function public.handle_new_user() returns trigger
language plpgsql security definer set search_path = '' as $$
begin
  insert into public.profiles (id, full_name)
  values (new.id, coalesce(new.raw_user_meta_data->>'full_name', new.raw_user_meta_data->>'name'));
  return new;
end $$;
create trigger on_auth_user_created after insert on auth.users
  for each row execute function public.handle_new_user();
revoke execute on function public.handle_new_user() from public, anon, authenticated;

-- Invitation catalogue (public read)
create table public.invitations (
  slug text primary key,
  name text not null,
  collection text not null check (collection in ('royal','traditional','elegant','modern')),
  tier text not null check (tier in ('Basic','Premium','Luxury')),
  price_from integer not null,
  tagline text not null,
  description text not null,
  features text[] not null default '{}',
  image text not null,
  sort integer not null default 0,
  active boolean not null default true,
  created_at timestamptz not null default now()
);
alter table public.invitations enable row level security;
create policy "invitations: public read" on public.invitations for select to anon, authenticated using (active);

-- Enquiries (anyone can send; signed-in users see their own)
create table public.enquiries (
  id uuid primary key default gen_random_uuid(),
  user_id uuid references auth.users(id) on delete set null default auth.uid(),
  name text not null check (char_length(name) between 1 and 120),
  phone text check (char_length(phone) <= 20),
  email text check (char_length(email) <= 200),
  wedding_date date,
  city text check (char_length(city) <= 80),
  package text check (package in ('Basic','Premium','Luxury','Not sure')),
  design_slug text references public.invitations(slug) on delete set null,
  message text check (char_length(message) <= 2000),
  source text not null default 'contact' check (source in ('contact','details','customize')),
  status text not null default 'new' check (status in ('new','contacted','won','lost')),
  created_at timestamptz not null default now(),
  check (phone is not null or email is not null)
);
alter table public.enquiries enable row level security;
create policy "enquiries: anyone can create" on public.enquiries for insert to anon, authenticated
  with check (user_id is null or user_id = (select auth.uid()));
create policy "enquiries: read own" on public.enquiries for select to authenticated using (user_id = (select auth.uid()));
create index enquiries_user_idx on public.enquiries(user_id);
create index enquiries_design_idx on public.enquiries(design_slug);

-- Saved customisations (signed-in only)
create table public.customizations (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade default auth.uid(),
  design_slug text references public.invitations(slug) on delete set null,
  data jsonb not null default '{}'::jsonb check (pg_column_size(data) < 20000),
  status text not null default 'draft' check (status in ('draft','submitted')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
alter table public.customizations enable row level security;
create policy "customizations: read own" on public.customizations for select to authenticated using (user_id = (select auth.uid()));
create policy "customizations: create own" on public.customizations for insert to authenticated with check (user_id = (select auth.uid()));
create policy "customizations: update own" on public.customizations for update to authenticated using (user_id = (select auth.uid())) with check (user_id = (select auth.uid()));
create policy "customizations: delete own" on public.customizations for delete to authenticated using (user_id = (select auth.uid()));
create index customizations_user_idx on public.customizations(user_id);
create index customizations_design_idx on public.customizations(design_slug);

-- Favourites (heart button)
create table public.favorites (
  user_id uuid not null references auth.users(id) on delete cascade default auth.uid(),
  slug text not null references public.invitations(slug) on delete cascade,
  created_at timestamptz not null default now(),
  primary key (user_id, slug)
);
alter table public.favorites enable row level security;
create policy "favorites: read own" on public.favorites for select to authenticated using (user_id = (select auth.uid()));
create policy "favorites: add own" on public.favorites for insert to authenticated with check (user_id = (select auth.uid()));
create policy "favorites: remove own" on public.favorites for delete to authenticated using (user_id = (select auth.uid()));
create index favorites_slug_idx on public.favorites(slug);

-- Public image bucket for website artwork
insert into storage.buckets (id, name, public) values ('site','site', true) on conflict (id) do nothing;

-- Catalogue seed
insert into public.invitations (slug,name,collection,tier,price_from,tagline,description,features,image,sort) values
('rajwada-royale','Rajwada Royale','royal','Luxury',11999,'Golden palace and lanterns on deep maroon','A grand invitation inspired by Rajasthani palaces: hanging lanterns, a golden haveli and fine filigree for a traditional Marwari wedding.',array['Customizable names, dates and text','Music or shehnai audio','Shareable link and QR code','RSVP (optional)','Event pages with Google Maps'],'inv-rajwada-royale.jpg',1),
('gulmohar-classic','Gulmohar Classic','traditional','Premium',6999,'Roses and marigolds on ivory','A warm, festive border of roses and marigolds in Rajasthani folk style, loved by families who want a classic kankotri feel.',array['Customizable names, dates and text','Hindi, English or bilingual','Shareable link and QR code','RSVP (optional)'],'inv-gulmohar-classic.jpg',2),
('gulabi-bagh','Gulabi Bagh','elegant','Premium',6999,'Blush peonies and fine gold','Soft blush florals and delicate gold for a romantic, elegant celebration.',array['Customizable names, dates and text','Music option','Photo gallery','Shareable link and QR code','RSVP (optional)'],'inv-gulabi-bagh.jpg',3),
('mor-pankh','Mor Pankh','modern','Premium',7999,'Peacock on emerald green','A majestic peacock on emerald green: modern, bold and unmistakably Rajasthani.',array['Customizable names, dates and text','Music option','Countdown to the wedding','Shareable link and QR code','RSVP (optional)'],'inv-mor-pankh.jpg',4),
('neel-mahal','Neel Mahal','royal','Luxury',11999,'Moonlit palace on royal navy','A glowing palace under a crescent moon on royal navy, made for evening receptions and sangeet nights.',array['Customizable names, dates and text','Music or shehnai audio','Event pages with Google Maps','Shareable link and QR code','RSVP (optional)'],'inv-neel-mahal.jpg',5),
('gajraj-swagat','Gajraj Swagat','traditional','Basic',3999,'Royal elephants and marigold toran','Two royal elephants welcome your guests under a marigold toran: auspicious, joyful and simple to share.',array['Customizable names, dates and text','Hindi, English or bilingual','Shareable link and QR code'],'inv-gajraj-swagat.jpg',6),
('sheesh-mahal','Sheesh Mahal','royal','Luxury',14999,'Chandeliers and a golden haveli','Our grandest design: crystal chandeliers, a scalloped Mughal arch and a detailed golden haveli facade.',array['Customizable names, dates and text','Music or shehnai audio','Photo gallery','Event pages with Google Maps','RSVP with guest count','Shareable link and QR code'],'inv-sheesh-mahal.jpg',7),
('chhatri','Chhatri','elegant','Basic',3999,'A single gold chhatri, lots of calm','Minimal and refined: one gold-line chhatri pavilion and plenty of ivory space for your words.',array['Customizable names, dates and text','Hindi, English or bilingual','Shareable link and QR code'],'inv-chhatri.jpg',8);
