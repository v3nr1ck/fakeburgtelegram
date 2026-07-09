# GoDaddy DNS for fakeburgtelegram.com → GitHub Pages

Repo: https://github.com/v3nr1ck/fakeburgtelegram  
GitHub Pages username host: **v3nr1ck.github.io**

Do this **after** GitHub Pages is enabled (see checklist at the bottom).

---

## Part A — GitHub first (5 minutes)

1. Open https://github.com/v3nr1ck/fakeburgtelegram  
2. **Settings** → **Pages** (left sidebar)  
3. **Build and deployment → Source**: choose **GitHub Actions**  
4. Open the **Actions** tab → open the latest **Deploy to GitHub Pages** run → wait until it is green  
5. Back on **Settings → Pages**, under **Custom domain**, type:

   ```
   fakeburgtelegram.com
   ```

6. Click **Save**  
7. Leave **Enforce HTTPS** unchecked until DNS works; turn it **on** after the check passes (can take a few minutes to hours)

GitHub will show DNS instructions. Use the GoDaddy steps below.

Temporary site (until domain works):  
https://v3nr1ck.github.io/fakeburgtelegram/

---

## Part B — GoDaddy DNS (exact records)

1. Log in at [godaddy.com](https://www.godaddy.com)  
2. **My Products** → find **fakeburgtelegram.com** → **DNS** (or **Manage DNS**)  
3. You will edit **records** for the domain

### Delete or stop using these if present

Remove or replace anything that fights GitHub:

| Type | Name | Why remove |
|------|------|------------|
| A | `@` | Old parking / website builder IPs |
| CNAME | `@` | Apex should be A records, not CNAME (on GoDaddy) |
| Forwarding | domain forward to somewhere else | Breaks Pages |
| “GoDaddy Website” / Website Builder link | connected site | Disconnect if DNS is locked to their product |

If GoDaddy shows **Domain Forwarding**, turn it **Off**.

If there is a **Parked** page, that’s fine once A records point at GitHub.

### Add these 4 A records (root domain)

Click **Add** for each (Type **A**, Name **`@`** or blank, TTL 1 hour or default):

| Type | Name | Value | TTL |
|------|------|--------|-----|
| A | `@` | `185.199.108.153` | 1 Hour |
| A | `@` | `185.199.109.153` | 1 Hour |
| A | `@` | `185.199.110.153` | 1 Hour |
| A | `@` | `185.199.111.153` | 1 Hour |

You should end up with **four** A records for `@`, all GitHub IPs above. No other A records for `@`.

### Add www

| Type | Name | Value | TTL |
|------|------|--------|-----|
| CNAME | `www` | `v3nr1ck.github.io` | 1 Hour |

**Important:** Value is `v3nr1ck.github.io` — **not** `v3nr1ck.github.io/fakeburgtelegram` and **not** your domain name.

If a CNAME for `www` already exists (e.g. to GoDaddy parking), **edit** it to `v3nr1ck.github.io`.

### Optional: do not add

- No need for a CNAME named `fakeburgtelegram.com`  
- No need for GoDaddy “Website” A records once GitHub is set  

### Screenshot checklist (what the DNS table should look like)

```
Type   Name   Data
A      @      185.199.108.153
A      @      185.199.109.153
A      @      185.199.110.153
A      @      185.199.111.153
CNAME  www    v3nr1ck.github.io.
```

(Other records like MX for email can stay if you use email on this domain.)

---

## Part C — After DNS is saved

1. Wait **15 minutes to a few hours** (sometimes up to 24–48h, usually faster)  
2. GitHub **Settings → Pages** → custom domain should show a green check for DNS  
3. Enable **Enforce HTTPS**  
4. Test:

   - http://fakeburgtelegram.com  
   - https://fakeburgtelegram.com  
   - https://www.fakeburgtelegram.com  

5. If `www` doesn’t redirect cleanly, in GitHub custom domain you can use `www.fakeburgtelegram.com` as primary and redirect apex, or keep apex as primary (both usually work with the records above).

---

## Common GoDaddy gotchas

| Problem | Fix |
|---------|-----|
| Site still shows GoDaddy “parked” / coming soon | Old A records still there — delete non-GitHub A records for `@` |
| “This site can’t be reached” | Wait for DNS; check A records with https://dnschecker.org |
| GitHub says domain not verified | Fix A/CNAME values; wait; click Save again on Pages custom domain |
| HTTPS error | Wait for certificate after DNS is correct, then Enforce HTTPS |
| Repo site works on github.io but domain 404s | Pages source must be **GitHub Actions**, deploy must be green |
| Wrong CNAME target | Must be `v3nr1ck.github.io` only |

### Quick DNS check (PowerShell)

```powershell
nslookup fakeburgtelegram.com
nslookup www.fakeburgtelegram.com
```

You want the A answers to be the `185.199.x.x` GitHub addresses, and `www` to point at `v3nr1ck.github.io`.

---

## Full order of operations

1. ✅ Code pushed to `v3nr1ck/fakeburgtelegram`  
2. ⬜ GitHub → Settings → Pages → **GitHub Actions**  
3. ⬜ Actions tab → green deploy  
4. ⬜ Pages → Custom domain `fakeburgtelegram.com` → Save  
5. ⬜ GoDaddy DNS: 4× A + www CNAME (this file)  
6. ⬜ Wait → green DNS check → Enforce HTTPS  
7. ⬜ Open https://fakeburgtelegram.com  

---

## Later: adding articles (after live)

```powershell
cd C:\Users\comfy\Pictures\projects\fakeburg-telegram
# add content/articles/....md and optional assets/img/...
git add content assets
git commit -m "Add article: headline"
git push
```

Actions redeploys automatically.
