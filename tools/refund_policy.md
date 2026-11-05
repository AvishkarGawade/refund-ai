# Refund.AI Platform Refund & Reversal Policy (v1.0)

## Core Eligibility Rules
To qualify for a manual refund reversal, an incoming request must satisfy all three criteria:

1. **Transaction Status (`STATUS_CHECK`)**:
   - The original transaction must have a status of `captured`.
   - `failed`, `pending`, or `authorized` transactions are not eligible. (Failed debits auto-reverse via standard banking clearing cycles within 24–48 hours).

2. **Time Window (`TIME_WINDOW_CHECK`)**:
   - The refund request must be initiated within **30 calendar days** of the transaction creation timestamp (`created_at`).
   - Any transaction exceeding 30 days is strictly ineligible.

3. **Duplicate Prevention (`DUPLICATE_CHECK`)**:
   - The transaction must not have an existing refund record.
   - `refund_status` must be `null` or unassigned.
   - If `refund_status` is `pending` or `processed`, reject immediately to avoid duplicate payouts.

## Operational Standards
- **Turnaround Time (TAT)**: 5–7 business days back to the original payment source.
- **Action on Approval**: Automatically trigger the gateway reversal tool and generate a reference `rfnd_` ID.