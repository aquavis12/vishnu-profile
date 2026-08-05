# Deploying /my-cfp — Design-Matched Version

This matches vishnurachapudi.com's exact CSS system (same fonts, color tokens,
panel styling, terminal component) and sits behind full Cognito auth with
required TOTP MFA — nothing renders, not even the CFP list, until you sign in.

## What's different from the plain static version

- **Login gate**: full-page terminal-styled card matching your site's aesthetic,
  not a generic form
- **Submission board**: mirrors your certification board — a grid of cells that
  light up, azure for proven talks, gold for proposed ones, animated on load
- **CFP list**: styled like your `.talk-row` deployment-log rows, same hover
  accent bar, same monospace metadata line
- **Nav**: links back to your homepage's `#about`, `#certifications`, `#talks`,
  `#blog` anchors, plus a "cfp" link marked current on this page
- All 56 CFPs from our thread are embedded directly in the page (the `CFPS`
  array) — no separate data file to manage

## 1. Deploy the backend

Same CloudFormation as before — one file, provisions Cognito (TOTP required,
no self-signup), DynamoDB, Lambda, API Gateway:

```bash
aws cloudformation deploy \
  --template-file cfp-backend.yaml \
  --stack-name my-cfp-backend \
  --parameter-overrides SiteDomain=vishnurachapudi.com CognitoDomainPrefix=vishnu-mycfp-auth \
  --capabilities CAPABILITY_IAM

aws cloudformation describe-stacks --stack-name my-cfp-backend --query "Stacks[0].Outputs"
```

## 2. Fill in config

Near the top of the `<script>` block in `my-cfp/index.html`:

```js
const CONFIG = {
  userPoolClientId: '...',
  hostedUiDomain: '...',
  redirectUri: window.location.origin + window.location.pathname,
  apiEndpoint: '...',
};
```

## 3. Create your one admin user

```bash
aws cognito-idp admin-create-user \
  --user-pool-id <UserPoolId> \
  --username you@yourdomain.com \
  --user-attributes Name=email,Value=you@yourdomain.com Name=email_verified,Value=true \
  --temporary-password "TempPass123!" \
  --message-action SUPPRESS
```

## 4. Upload

Put `my-cfp/index.html` at that exact path in whatever hosts
vishnurachapudi.com — so it's reachable at `vishnurachapudi.com/my-cfp/`.

## 5. First login

Visit the page — you'll see the terminal-styled login card, not the CFP
content. Click Sign In, go through Cognito's Hosted UI, set your permanent
password, scan the TOTP QR code. Every subsequent login requires that code.

## Adding CFPs later

Two ways:
- **Permanent additions**: edit the `CFPS` array directly in `index.html`
  (search for `const CFPS = [`), matching the existing object shape
- **Quick additions via the UI**: click "+ Add CFP" once logged in — these
  save to DynamoDB and appear under "My Submissions" with a delete button;
  the embedded ones don't have delete since they're not in the database

## Note on the submission board

The board counts and animates every CFP currently loaded — proven ones show
a ✓ in azure, proposed ones show empty gold cells. This updates live as you
add/delete through the form.
