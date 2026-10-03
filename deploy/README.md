# One-Sheet Zine Kit site

Public zine-making tool at https://zine.imurph.com, served by Nginx behind
Traefik and the Cloudflare proxy. No sign-in is needed. The source page is `zine-kit.html` in the
project root.

The commands below use `$VPS_HOST` for your SSH host. Set it first, for
example `export VPS_HOST=my-vps` (an alias from `~/.ssh/config`).

## Deployment

- Remote directory: `/docker/zine`
- Image: `nginx:1.28.3-alpine`
- Container port: 80; no host port is published
- Network: external `app-net`
- Files: read-only bind mount from `/docker/zine/site`: `index.html`, and the
  how-to video and its poster image in `media/`
- No database, application secrets, or Docker data volumes. Each visitor's
  zine is saved in their own browser (`localStorage`), not on the server.
- Health: `/healthz` (inside the container)
- Hostname: `zine.imurph.com`. The DNS record must stay Cloudflare-proxied
  (orange cloud), because the VPS firewall accepts web traffic only from
  Cloudflare.
- Headers: `noindex` asks search engines not to list the site, and
  `no-store` stops caching of the page so updates show up right away. Files in
  `/media/` are cacheable (1 day in browsers, 7 days at Cloudflare), so the
  video does not download from the VPS on every view.

To make the site private again, add a Cloudflare Access application for the
hostname. For defense in depth, you can also add this line to the `location /`
and `location /media/` blocks in `default.conf`. It returns 403 to requests that did not come through
Access:

```nginx
if ($http_cf_access_jwt_assertion = "") { return 403; }
```

## Update

From the project root, copy the page and upload it:

```sh
cp zine-kit.html deploy/site/index.html
scp deploy/site/index.html "$VPS_HOST":/docker/zine/site/index.html
```

If you change the video or its poster, copy and upload `media/` too:

```sh
cp media/how-to-make-a-zine.mp4 media/how-to-make-a-zine.jpg deploy/site/media/
scp deploy/site/media/* "$VPS_HOST":/docker/zine/site/media/
```

Media files are cached for up to 7 days at Cloudflare. To replace the video
right away, give it a new file name and update the `<source>` path in
`zine-kit.html`, or purge the URL in the Cloudflare dashboard.

No restart is needed for page-only changes. For configuration changes:

```sh
ssh "$VPS_HOST" 'cp -a /docker/zine /docker/zine.backup-$(date +%Y%m%d-%H%M%S)'
scp deploy/docker-compose.yml deploy/default.conf "$VPS_HOST":/docker/zine/
ssh "$VPS_HOST" 'cd /docker/zine && docker compose config --quiet && docker compose run --rm --no-deps zine nginx -t && docker compose up -d'
```

## Verify and roll back

Check `docker compose ps` (should show `healthy`). Then open
https://zine.imurph.com in a private browser window. The page should load
with no sign-in, and printing should show one landscape sheet.

To roll back a configuration change, copy the files back from the dated
backup folder and run `docker compose up -d`. To take the site offline, run
`docker compose stop` in `/docker/zine` and keep the files.
