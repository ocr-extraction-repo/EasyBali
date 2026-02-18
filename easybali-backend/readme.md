# EasyBali Backend

## Configure Staging Xendit Test Account

This setup is fully internal and does not require client involvement.

### 1. Set staging environment variables

Configure these in your staging backend service (Render/VPS):

- `APP_ENV=staging`
- `XENDIT_SECRET_KEY=<your Xendit test secret key>`
- `XENDIT_WEBHOOK_CALLBACK_TOKEN=<your Xendit callback verification token>`
- `XENDIT_WEBHOOK_PATH=/webhook/xendit`
- `XENDIT_ENABLE_DISBURSEMENT=false`
- `BASE_URL=<your staging backend public URL>`

Notes:
- Keep `XENDIT_ENABLE_DISBURSEMENT=false` in staging to prevent payout/disbursement calls.
- Use Xendit test mode credentials only (`xnd_development_...`).

### 2. Configure Xendit test webhook

In Xendit dashboard (test mode):

- Callback URL: `<BASE_URL>/webhook/xendit`
- Callback token: same value as `XENDIT_WEBHOOK_CALLBACK_TOKEN`

The backend also supports legacy webhook path `/webhook/xendit-payment` for backward compatibility.

### 3. Verify behavior

1. Create a test booking that generates an invoice.
2. Complete payment using Xendit test flow.
3. Confirm webhook marks payment as completed.
4. Confirm database shows disbursement skipped in staging (`payment.disbursements.skipped=true`).

### 4. Production safety checklist

Before production payout automation:

- Set `APP_ENV=production`
- Use production `XENDIT_SECRET_KEY`
- Set production callback token
- Set `XENDIT_ENABLE_DISBURSEMENT=true` only when ready
