# Meridian Crest Bank Operations Policy Manual

**FICTIONAL TRAINING MATERIAL — NOT A REAL BANK POLICY.** This synthetic manual exists only for the “Demo to Production: An Evals Lab for Enterprise AI” workshop. It is not legal, compliance, or operational guidance. Where this manual is silent, staff must pause and escalate to the responsible operations lead; they must not infer a policy.

## OPS-1.1 — Scope and operating principles

This manual covers routine deposit-account operations for Meridian Crest Bank (MCB). It applies to branch and centralized operations staff handling customer requests. It does not authorize a staff member to bypass identity checks, sanctions screening, system controls, or a required approval. The more restrictive control applies when a system alert and this manual appear to differ. Staff must record the policy section relied on in the case note and retain supporting records in the approved case system.

The terms “business day” and “business hours” refer to MCB processing calendars, not a branch schedule. A deadline stated in business days excludes weekends and bank holidays. “Customer” includes an individual or a legal entity unless a section says otherwise. “Written approval” means a dated approval in the case system from a person with the stated authority; a verbal assurance is not approval. Never promise a customer that a request will be completed before the relevant review is finished.

## OPS-2.1 — Domestic wire transfers

Domestic wires may be submitted by verified individual, small-business, and commercial customers. The standard daily outgoing limit is **$25,000 per individual**, **$75,000 per small-business relationship**, and **$250,000 per commercial relationship**. These are aggregate limits across all domestic outgoing wires in a calendar day, not per transaction. A joint individual account shares one $25,000 limit. Multiple accounts held under the same small-business or commercial relationship share that relationship’s limit.

An individual customer may request a one-time increase up to **$50,000** with approval from a branch manager and a successful callback to the telephone number already on file. No one-time increase is available for a joint individual account. Small-business increases up to **$150,000** require a branch manager and the Business Operations Manager. Commercial increases above $250,000 require written approval from the Treasury Operations Director before entry; there is no same-day verbal exception. Do not split a request into smaller wires to avoid a limit or approval.

For every domestic wire of **$10,000 or more**, staff must complete an outbound callback to a trusted number already recorded on the account, read back the beneficiary name and amount, and document the person reached, number, time, and result. A changed phone number supplied during the wire request is not trusted for that callback. If the customer cannot be reached, place the request in pending status; do not release it. Wires below $10,000 still require standard authentication and dual review when flagged by the transaction monitoring system.

Same-day domestic wire requests received by **3:00 p.m. Eastern Time** on a business day enter the same-day processing queue after all controls pass. Requests after 3:00 p.m. are processed the next business day. The cutoff is not a service guarantee: holds, missing information, screening, or system outages can delay a wire. Staff may not override a missed cutoff by changing the recorded receipt time.

## OPS-2.2 — International wires and screening

International wires require complete originator and beneficiary details, including legal name, physical address, receiving institution, destination country, and purpose. The standard daily limit is **$15,000 per individual**, **$50,000 per small-business relationship**, and **$150,000 per commercial relationship**. International wires count against their own limit and do not reduce the domestic limit. A request to a restricted or currently blocked destination must be stopped and referred to the Sanctions Review Desk; staff must not tell the customer that a screening alert is cleared until the desk records its decision.

Every international wire, regardless of amount, requires the trusted-number callback described in OPS-2.1 and independent second-person review. The international same-day submission cutoff is **1:00 p.m. Eastern Time** on a business day. A wire with an incomplete purpose statement or inconsistent beneficiary details remains pending. Staff may not use a domestic-wire approval to authorize an international transfer. A commercial customer’s higher domestic limit does not change its international limit.

## OPS-2.3 — Wire exceptions, returns, and corrections

If the beneficiary name, account identifier, or destination country changes after a wire is entered, stop processing and obtain fresh customer authorization plus a new review. A correction is not a clerical edit when it changes who receives the funds. A returned wire is credited only after the receiving institution’s return is confirmed and posted. Staff must not promise recovery of an irrevocable transfer. Suspected coercion, account takeover, or a request to send funds to an unrelated party must be referred to Fraud Operations before release, even when the request is within the applicable dollar limit.

The one-time individual increase in OPS-2.1 applies only to domestic wires. It does not raise the $15,000 international individual limit. Likewise, the commercial increase process in OPS-2.1 does not apply to international requests. These distinctions are deliberate; do not generalize an approval from one rail to another.

## OPS-3.1 — Customer identification and required records

Before opening an account or processing a material profile change, staff must verify the customer using approved identity procedures. For an individual, collect and retain the legal name, date of birth, residential address, and a government-issued photo identification number and expiration date. For a legal entity, collect the registered legal name, formation jurisdiction, business address, tax identifier, formation record, and identity details for each beneficial owner with **25% or more ownership**, plus one control person. If ownership cannot be established or documents conflict, do not proceed until reviewed by the CDD team.

Acceptable individual identity documents are a current passport, state driver license, or state identification card. An expired document is not sufficient by itself. A foreign passport may be used with a second approved proof of address. Acceptable address evidence includes a utility bill, government correspondence, or a signed lease dated within the prior **90 days**. A post office box alone is not a residential address. For entities, acceptable formation evidence includes a certificate of formation or equivalent government registry record. Staff must not keep unnecessary copies of sensitive identity records outside the approved system.

## OPS-3.2 — KYC/CDD refresh cadence

Customer due diligence records must be refreshed on a risk-based schedule: **low risk every 36 months**, **medium risk every 24 months**, and **high risk every 12 months**. The schedule is measured from the date of the last completed review. A review is complete only when required information is verified and the reviewer records the outcome; sending a request for documents does not reset the clock.

At refresh, confirm the customer’s legal name, address, occupation or business activity, expected account use, beneficial ownership where applicable, and contact details. Re-check identity documents if expired, changed, or inconsistent. Medium- and high-risk entities must reconfirm beneficial ownership and control persons at each refresh. Low-risk entity ownership may be reconfirmed using an authoritative registry if the registry record is current and no alert has appeared.

## OPS-3.3 — Enhanced review triggers

Refer a customer for enhanced due diligence (EDD) when there is a material change in ownership or control, a newly identified politically exposed person, unexplained high-value activity inconsistent with the stated purpose, repeated activity involving high-risk jurisdictions, credible adverse media related to financial crime, suspected identity manipulation, or a transaction-monitoring alert designated for EDD. A risk-tier change to high requires annual refresh under OPS-3.2. The CDD team may request source-of-funds documents, contracts, invoices, ownership charts, or updated identity evidence. Frontline staff must not tell the customer that an internal suspicious-activity review is underway.

An EDD referral is not itself a finding of wrongdoing and does not automatically close an account. Until the CDD team completes its review, staff may continue ordinary activity unless a separate fraud, sanctions, or legal hold applies. If required information is unavailable after **30 calendar days**, the CDD team decides whether to restrict services or recommend closure; branch staff must not make that decision alone.

## OPS-4.1 — Fraud holds

Place a temporary fraud hold when there is a credible indicator of unauthorized access or activity: a customer reports an account takeover, authentication factors appear compromised, a device or identity mismatch is supported by an alert, a check or deposit is suspected counterfeit, or a transaction pattern is materially inconsistent with the account and has an active Fraud Operations alert. A customer’s unfamiliarity with a transaction, without any supporting risk indicator, requires investigation but does not by itself justify a hold.

The initial hold may last no more than **5 business days**. Fraud Operations may extend it once, up to a total of **10 business days**, with a documented reason and notice to the customer unless notice is prohibited by law or an active investigation. A hold must be scoped to the funds or functions reasonably implicated; block the whole account only when Fraud Operations documents why a narrower restriction is insufficient. Staff must record the trigger, start time, affected funds or functions, reviewer, customer contact, and next review deadline.

Only a Fraud Operations Manager or the Fraud Operations Director may release a fraud hold. A branch manager may request release and supply evidence but cannot release it. Release promptly when the authorized reviewer documents that the risk is resolved or the hold period expires. If a legal order or sanctions restriction applies, follow that separate control and do not release under this section.

## OPS-4.2 — Hold reviews and customer contact

Fraud Operations reviews an active hold at least once every **2 business days** and records whether the scope remains necessary. When the customer provides evidence, attach it to the case and route it to the assigned reviewer within one business day. Do not disclose confidential monitoring logic. If the customer disputes a hold, log the dispute as a complaint under OPS-8.1 while the fraud review proceeds.

## OPS-5.1 — Fee reversals and overdraft refunds

An individual teller may approve a fee reversal or overdraft refund up to **$25 per customer per calendar month**, with a maximum of **two items per month**. A supervisor may approve up to **$100 per customer per calendar month**, including teller-authorized amounts. A branch manager may approve up to **$250 per customer per calendar month**, including any lower-level approvals. Amounts are cumulative across all accounts held by the customer and all fee or overdraft items. The approver must review the transaction, record the reason code, and tell the customer whether the credit is immediate or pending.

Requests above $250 per customer per calendar month, repeated requests suggesting a systemic issue, or requests involving suspected employee error must be referred to the Regional Operations Manager. No employee may divide a single requested refund across several transactions or months to avoid an approval threshold. A fee reversal is not an overdraft credit if it does not address an overdraft charge; select the accurate transaction type. An approved amount does not guarantee an immediate available balance if other restrictions apply.

## OPS-6.1 — Dormant accounts

An account becomes dormant after **24 consecutive months** with no customer-initiated financial transaction or authenticated customer contact. Interest postings, bank fees, automated statements, and bank-generated corrections do not count as customer activity. At **18 months** of inactivity, send a first notice to the last known mailing address and, where available, the secure message inbox. At **22 months**, send a second notice and attempt one documented phone contact using the number on file. Returned mail must be recorded and triggers an address verification request if the customer later contacts the bank.

Before classifying an account dormant, confirm no open fraud hold, legal restriction, deceased-customer case, or pending transaction changes the handling. Dormant status limits outbound transactions until identity is reverified; it does not itself close the account or forfeit the balance. Reactivate after successful identity verification and a customer-initiated instruction, with a case note documenting the date and control performed.

## OPS-6.2 — Unclaimed property and escheatment

For this training policy, funds in an account with no owner contact or qualifying customer activity for **5 years after dormancy** enter the escheatment review process, subject to the customer’s state of last known address and applicable law. At least **60 days before remittance**, send a final due-diligence notice to the last known address when required by the applicable jurisdiction. The Unclaimed Property Team validates the state, dormancy date, notice evidence, balance, and reporting format before remittance. Branch staff must not promise a precise return date or attempt to prevent escheatment by posting artificial activity. Once remitted, direct the owner to the relevant state unclaimed-property authority or the Unclaimed Property Team for recovery instructions.

## OPS-7.1 — Account closures

Verify the account owner’s identity and authority before accepting a closure request. For joint accounts, any owner may request closure unless the account agreement, restriction, or legal process requires all owners or another approval. For a business account, accept instructions only from an authorized signer or documented control person. Review pending deposits, outstanding checks, debit-card authorizations, liens, holds, and negative balances. Explain that a closure may be delayed while these items settle; do not backdate a closure.

Close an unrestricted account within **3 business days** after all pending items are resolved and the customer provides disbursement instructions. If the customer requests a cashier’s check, verify the payee and mailing or delivery instructions. If the balance is negative, route the case to Collections Operations; do not close by writing off the balance. A suspected fraud or legal restriction must be routed to the controlling team before closure. Record the request date, authorization, balance disposition, and final status.

## OPS-7.2 — Cash deposits and large-cash escalation

Count cash in the customer’s presence when practical, confirm the amount, and issue a receipt. Cash deposits of **$10,000 or more in one business day by or for the same person** must be referred to the Cash Compliance Desk before completion for required reporting and aggregation review. The threshold applies to related deposits that staff know or reasonably suspect are connected; do not treat separate deposits as unrelated merely because each is below $10,000. Never advise a customer to split a deposit to avoid reporting. A referral is not permission to disclose whether a report is filed.

If a deposit appears structured, involves a third party who cannot explain the relationship, or conflicts with the customer’s expected activity, preserve the transaction details and refer to the Cash Compliance Desk. Do not refuse a deposit solely because it meets the reporting threshold unless a separate restriction or the desk directs otherwise. Make a factual note without accusing the customer of wrongdoing.

## OPS-8.1 — Customer complaints

Log every expression of dissatisfaction about a product, service, employee interaction, fee, delay, or decision as a complaint, even if raised verbally and even if the issue is resolved during the same contact. Record the customer’s words where practical, date and channel, account reference, issue type, requested outcome, steps taken, and owner. Do not include unnecessary sensitive data in free-text notes. Send an acknowledgement within **2 business days** that includes the case reference and next update expectation.

Resolve routine complaints within **10 business days**. If more time is needed, send an update by day 10 and provide a revised target date no later than **30 calendar days** from receipt. A complaint involving suspected discrimination, financial harm above $1,000, an unresolved fraud hold, repeated service failure, or a threat of regulator or media contact must be escalated to the Customer Advocacy Manager within **1 business day**. Complaints alleging employee misconduct also go to the Conduct Review Desk. A frontline employee must not close a complaint solely because a customer stopped responding; make two contact attempts on separate business days and document them.

## OPS-8.2 — Escalation and records

Escalate policy ambiguity to the relevant functional owner: wire controls to Wire Operations, identity or refresh questions to CDD, fraud holds to Fraud Operations, cash reporting to the Cash Compliance Desk, dormant balances to the Unclaimed Property Team, and complaint handling to Customer Advocacy. An escalation should state the question, relevant facts, section consulted, deadline, and customer impact. Continue only actions that remain authorized while a response is pending. Store records in the approved case system under retention rules; do not use personal email, local notes, or unapproved messaging to transfer customer information.

## OPS-9.1 — Manual exclusions and unknown questions

This manual contains no policy on cryptocurrency, mortgages, loan rates, investment advice, employee or human-resources matters, or branch hours. It also does not establish tax advice, legal interpretation, or a rule for a situation not described here. For any uncovered subject, tell the requester that the manual does not cover it and suggest escalation to the appropriate qualified team or manager. Do not fill gaps using general knowledge, guesswork, another institution’s rules, or an invented section citation.

When uncertainty concerns a customer-specific decision, preserve the customer’s position, avoid making a commitment, and route the question to the responsible functional owner under OPS-8.2. The manual is fictional training material and must not be used to make a real financial decision.
