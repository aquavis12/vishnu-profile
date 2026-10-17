# Visitor Counter — Backend

Serverless visitor counter for the site: **API Gateway (HTTP API) → Lambda → DynamoDB**.
Everything here fits comfortably inside the AWS free tier for a personal site.

## What gets created

| Resource | Purpose |
|----------|---------|
| DynamoDB table `visitor-counter` | Stores one item (`id = site`) with a `visits` number, incremented atomically |
| Lambda `CounterFunction` (Python 3.12) | Increments the counter and returns `{"count": N}` as JSON with CORS |
| HTTP API `GET /count` | Public endpoint the website calls on page load |

## Prerequisites

- An AWS account and the [AWS CLI](https://docs.aws.amazon.com/cli/latest/userguide/getting-started-install.html) configured (`aws configure`)
- The [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html)

## Deploy

From this `backend/` folder:

```bash
sam build
sam deploy --guided
```

During `--guided` you'll be asked for:
- **Stack name**: e.g. `visitor-counter`
- **AWS Region**: e.g. `us-east-1` (N. Virginia) — match the region in `index.html`
- **AllowOrigin**: keep the default `https://www.vishnurachapudi.com`
  (for local testing you can temporarily use `*`)

When it finishes, copy the **`CounterApiUrl`** output. It looks like:

```
https://abc123xyz.execute-api.us-east-1.amazonaws.com/count
```

## Wire up the front-end

In `index.html`, find the visitor-counter block and replace the placeholder:

```js
var COUNTER_API = 'https://REPLACE_WITH_YOUR_API_ID.execute-api.us-east-1.amazonaws.com/count';
```

with the `CounterApiUrl` value from the deploy output. The counter stays hidden
(shows `—`) until a real URL is set, so nothing breaks before deployment.

> **Deployed:** stack `visitor-counter` in `us-east-1`. Live endpoint:
> `https://on6g4fpu1d.execute-api.us-east-1.amazonaws.com/count`

## Test the endpoint

```bash
curl https://<your-api-id>.execute-api.<region>.amazonaws.com/count
# {"count": 1}   (increments by 1 each call)
```

## Notes & hardening

- **One count per page load.** Each GET increments by 1. If you want "unique-ish"
  counting, gate the fetch behind `sessionStorage` on the client, or add a
  `/count` (read-only) vs `/hit` (increment) split in the Lambda.
- **Cost.** PAY_PER_REQUEST DynamoDB + a tiny Lambda + HTTP API = effectively free
  at personal-site traffic; well within the always-free Lambda tier.
- **CORS.** Locked to your domain via `AllowOrigin`. Update the parameter and
  redeploy if your domain changes.
- **Region.** Keep the Lambda region and the URL region in `index.html` the same.

## Tear down

```bash
sam delete
```
