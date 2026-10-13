# Device login for read-only API tokens

MyMail, MyCal and MyNotes share RFC 8628 protocol code from
`go-server-common/devicegrant`. MyMail/MyCal have resource-scoped access; MyNotes
has unscoped read-only access to its whole API.

- `mymail-token login -name NAME [-lifetime N[s|m|h|d]] [-folders ID[,ID…]] [-out FILE]`
  and `mycal-token login -name NAME [-lifetime N[s|m|h|d]] [-calendars ID[,ID…]] [-out FILE]`
  and `mynotes-token login -name NAME [-lifetime N[s|m|h|d]] [-out FILE]`
  read no credentials. Explicit credential options are rejected; the user environment
  default is ignored. Requested lifetime defaults to 30 days. In MyMail/MyCal,
  requested resources are optional suggestions, never an authorization decision. Malformed or
  nonexistent requested resources fail login with invalid_scope before a code
  is issued.
- The CLI prints an approval URL and a short `XXXX-XXXX` user code to stderr.
  The link opens a separate `device-approval.html` page showing only the approval
  flow. A complete URL fills in the code and loads the request without approving
  it. Once loaded, the dedicated page shows the request without a redundant
  code-entry form or Review request button. Manual entry remains available when
  no request is loaded, after a failed decision, and in Settings → API Tokens. Code entry is case-
  and hyphen-insensitive.
- Settings → API Tokens is a separate tab in all three apps. It lists existing
  tokens with expiry and, in MyMail/MyCal, their resource scope, supports confirmed revocation,
  and allows manual device-code approval. Direct token creation uses the CLI.
  Review request is disabled while the code is empty or whitespace.
- Before approving, the user sees the code, CLI identity, requested token name,
  requested access (folders/calendars in MyMail/MyCal; the whole API in MyNotes),
  lifetime, request age, and socket IP/User-Agent.
  The UI reminds them to approve only a login they started and compare its code.
  Requested scope and lifetime are pre-filled. The user can adjust them, must
  grant at least one resource in MyMail/MyCal, and chooses a positive lifetime up to ten years,
  then explicitly Approve or Deny. A decision cannot be changed or repeated.
  The dedicated page attempts to close after either successful decision. If the
  browser blocks closing, it shows completion and tells the user to close the tab.
- The grant expires after ten minutes. The CLI waits five seconds between polls
  and increases that wait by five seconds after `slow_down`. Network timeouts
  and dropped connections (EOF, truncated responses, resets) as well as transient
  server failures back off; cancellation and expiry stop the flow.
- Approval records consent. The next eligible poll creates an ordinary read-only,
  hash-stored API token and consumes the grant in one transaction. Its secret is
  returned once; transient mint failures can be retried. If that response is lost
  after minting, the CLI cannot recover the secret; it advises checking the token
  list and revoking unused tokens before starting again. In MyMail/MyCal, a
  removed approved resource invalidates the grant with invalid_grant, even if its ID is reused. Denial creates no token.
  Live requests are capped at ten globally and three per socket IP.
- On success, only the token goes to stdout (or a newly created 0600 file with
  `-out`); the revocation slug goes to stderr. Files are never overwritten.
  Existing `create` and `revoke` credential flows continue to work unchanged.
- Both unauthenticated CLI POST routes retain Host, CSRF and body-size checks.
  All four OAuth operations refuse bearer credentials. Approval requires full
  access (Basic authentication when configured) and normal CSRF protection.
  Demo mode does not offer API tokens or device approval.

MyNotes accepts only client ID `mynotes-token` and empty requested/granted scope.
Empty scope means whole-API read-only access (notes/search, tags, artifacts, icons,
Markdown downloads), with GET and corresponding HEAD support. Nonempty scopes
are rejected, and there is no resource picker or resource-selection CLI flag.
The consent page explicitly describes that whole-API access. MyNotes uses
shared v1.14.0 with `AllowEmptyScope: true`; its scope validator still rejects
nonempty scopes on approval and exchange. All device protocol handlers are shared.

The device grant changes token issuance only. Existing scope restrictions,
listing, revocation and token expiry remain the app's own token-store behavior.
Refresh tokens, discovery metadata and dynamic client registration are out of scope.

Verification lives in each app's `device_login_test.go`, `device_page_test.go`
(CSP importmap and deployment URL checks), token CLI tests, and
`e2e/tests/device-approval.spec.ts`, plus the shared package's protocol/client
unit tests. These checks run against local code; they do not establish which
library version has been published or which app commit has been deployed.
