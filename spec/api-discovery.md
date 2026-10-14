# API discovery

**Status: binding, implemented in all four apps.** The implementing commits are listed in §7 and
were pushed to each repo's `origin/main` on 2026-10-14. That was confirmed from the local
remote-tracking refs, not by querying the remotes.

The owner accepted the contract for implementation on 2026-10-14. Until the first app
implemented it, it was a proposal, as `spec/README.md` requires.
Adoption is tracked as one AWB issue per app (§7). Once the contract is binding, an app still
adopting it is a claim with a deadline, not a standing exemption.

## 1. What it covers

How a client that knows only an app's origin finds that app's HTTP API and its machine-readable
description. It applies to **four** apps, which is one more than the UI contracts:

| App     | Repo         | API base path | OpenAPI document today                                              |
|---------|--------------|---------------|---------------------------------------------------------------------|
| MyCal   | `../mycal`   | `/api/v1/`    | `openapi.yaml`                                                      |
| MyMail  | `../mymail`  | `/api/v1/`    | `openapi.yaml`                                                      |
| MyNotes | `../mynotes` | `/api/v1/`    | `openapi.yaml`                                                      |
| MyLinks | `../mylinks` | `/`           | **none** when this contract was written; added by `mys-uqbie3` (§7) |

Like `spec/device-login.md`, this is an app integration protocol, not a UI contract. It mandates
HTTP behaviour; nothing in it is rendered, and `spec/measurement-protocol.md` does not apply.

Standards it uses: OpenAPI 3.0.3; RFC 9727 (`api-catalog`); RFC 9264 (Linkset); RFC 8631
(`service-desc`); RFC 8288 (`Link` header); RFC 8615 (`/.well-known/`); RFC 9512
(`application/yaml`).

## 2. Mandated behaviour

### 2.1 The OpenAPI document

- `GET /openapi.yaml` returns the app's OpenAPI document with status 200 and
  `Content-Type: application/yaml`. `HEAD` answers with the same headers and no body.
- The bytes served are **the file the server code is generated from**, embedded with
  `//go:embed`, unmodified. A document produced at runtime, or a second copy kept beside it, is
  not compliant, because the reason to serve it is that it cannot drift from the code.
- The document declares `openapi: 3.0.3` (§5.1).
- Its `servers[0].url` is a **relative** URL chosen so that, resolved against `/openapi.yaml`
  and joined with each path in `paths`, it gives the route the app actually serves. What is
  mandated is the resolved operation URL, not a particular server value, and the value differs
  per app. MyCal's `paths` already carry `/api/v1`, and it has one path, `/calendar.ics`, outside
  that prefix, so its server URL is `/`. MyMail's and MyNotes' paths do not carry the prefix, so
  theirs is `/api/v1`. An absolute `http://localhost:8080` is wrong for every client that
  discovers the document, because it names the developer's machine instead of the origin the
  client is talking to.

### 2.2 The API catalog

- `GET /.well-known/api-catalog` returns status 200 with
  `Content-Type: application/linkset+json; profile="https://www.rfc-editor.org/info/rfc9727"`
  and a Linkset of exactly one link context, the app's API:

  ```json
  {
    "linkset": [
      {
        "anchor": "/api/v1/",
        "service-desc": [
          { "href": "/openapi.yaml", "type": "application/yaml" }
        ]
      }
    ]
  }
  ```

  `anchor` is the API base path from §1, so MyLinks' is `/`. Further RFC 8631 relations
  (`service-doc`, `status`, `service-meta`) are **permitted but not mandated**. An app adding one
  is not divergence; an app adding one that points at nothing is a defect.
- `HEAD /.well-known/api-catalog` returns 200 with
  `Link: </.well-known/api-catalog>; rel="api-catalog"` (RFC 9727 §2 requires a `Link` header
  with the `api-catalog` relation on `HEAD`). `GET` may carry the same header.

### 2.3 The `Link` header on API responses

Every response under the API base path carries `Link: </openapi.yaml>; rel="service-desc"`,
whatever its status code, **except in demo mode** (§2.4). There the document returns 404, and a
link to it would advertise a resource that is not there. For MyLinks the API base is `/`, so this covers its HTML pages too.
That is harmless: the header is metadata, and a browser ignores it.

### 2.4 Access

- Both resources are served **without authentication**, including when HTTP Basic auth or API
  tokens are configured. A client needs them before it has credentials. They contain nothing
  that is not already public, since each repo is public and the document is a file in it.
- In **demo mode**, where an app's API answers as unavailable, both resources return 404. A
  catalog advertising an API that refuses every call is worse than none. MyCal, MyMail and
  MyNotes route `/api/v1/` to `demoAPIUnavailable` in demo mode. MyLinks has no server-side demo
  mode; its demo is a static bundle, which this contract does not cover.
- No CORS headers are mandated. Adding them is a separate decision, because it would need to be
  the same in all four apps.

## 3. Mechanisms: mandated and local

**Mandated:** the paths, status codes, media types, the `profile` parameter, the Linkset shape,
the `Link` header values, the no-authentication rule, and that the served document is the
embedded generator input. All of these are observable by a client.

**Local:** where the handler is registered, and how the embedded file reaches it. MyLinks'
`main` package is in `cmd/mylinks`, and `//go:embed` cannot reach a parent directory, so its
embed has to live in a package at or above `openapi.yaml`. The repo root already holds one such
file (`empty-efs.go`). Middleware versus per-handler is also local, as is whether `GET` also sends
the `api-catalog` `Link` header.

## 4. Verification

Each app holds its own half, in-process, in its Go test suite:

1. `GET /openapi.yaml` returns the on-disk `openapi.yaml` byte for byte, as `application/yaml`.
2. Its `servers[0].url` is relative, and for at least one operation, resolving it and joining
   the path gives a route the server answers. A test that only checks the URL is relative passes
   for MyCal with `/api/v1`, which resolves every operation to `/api/v1/api/v1/…`.
3. `GET /.well-known/api-catalog` parses as the Linkset in §2.2, with the media type and profile
   exactly as written.
4. `HEAD /.well-known/api-catalog` carries the `api-catalog` `Link` header.
5. A response under the API base, including an error response, carries the `service-desc` link.
6. Steps 1 and 3 succeed **with authentication configured and no credentials sent**.
7. In demo mode, both return 404, and API responses carry no `service-desc` link.

**Nothing checks the four against each other**, the same as every other contract here
(`AGENTS.md` §2.1). `tools/check-contract.py` does not check this contract.

## 5. Decisions recorded

### 5.1 OpenAPI 3.0.3, not 3.1

All four generate with ogen, pinned at **v1.24.0** by this contract. ogen's parser accepts
`openapi: 3.0`–`3.2`, but its JSON Schema model is still 3.0's. This was measured on 2026-10-14,
with ogen run against minimal 3.1 documents:

> v1.22.0: `type: [string, "null"]` fails, *"cannot unmarshal !!seq into string"*;
> numeric `exclusiveMinimum: 0` fails, *"cannot unmarshal !!int `0` into bool"*.
> v1.24.0: the type array generates; numeric `exclusiveMinimum` still fails, with the same error.

So declaring 3.1 would buy little, and it would mislead a reader into writing 3.1 schemas. Revisit
when ogen models 3.1 JSON Schema. **That is a reading of v1.24.0, not of the version you have**,
so re-run it before relying on it.

### 5.2 One fixed path at the origin root

`/openapi.yaml` is the same in all four, rather than `/api/v1/openapi.yaml` in three and something
else in MyLinks, whose API has no prefix. The catalog is what a client reads first, and it names
the path anyway. A single path makes the apps interchangeable for a human with `curl`.

### 5.3 Relative URIs in the Linkset, a deliberate deviation from a SHOULD

**Ruled by the owner on 2026-10-14: relative URIs are accepted.** RFC 9264 §4.2.2 and §4.2.3 (read
2026-10-14) say that `anchor` and `href` each *"MUST be a URI reference and SHOULD NOT be a relative
reference"*. RFC 9264 does not define how a relative reference in the JSON format resolves. This
contract relies on ordinary RFC 3986 resolution against the URL the catalog was retrieved from.

The alternative was absolute URIs. Those need the public origin, and while all four apps have a
`-public-url` flag, it is optional in all four (required only for wildcard binds or reverse
proxies). Without it, the only fallback is the client-controlled `Host` header. Absolute URIs built
from `-public-url` when it is set were considered and not adopted. Reopening that would change all
four apps.

## 6. Out of scope

- **OAuth discovery metadata** (RFC 8414 `/.well-known/oauth-authorization-server`, RFC 9728
  `/.well-known/oauth-protected-resource`). `spec/device-login.md` puts discovery metadata out of
  scope, and this contract does not reopen that.
- RFC 9457 problem details, hypermedia formats (HAL, JSON:API, Hydra), and Arazzo workflows.
- Deployment beneath a path prefix. `/.well-known/` lives at the origin root by definition (RFC
  8615), so an app served below `/mycal/` cannot satisfy §2.2 without help from the reverse proxy.
- MyPass. It was not part of the request this contract came from, and its API surface was not examined.

## 7. Adoption

| App     | AWB issue                                                | Implementing commit, on `origin/main` (2026-10-14) |
|---------|----------------------------------------------------------|----------------------------------------------------|
| MyLinks | `mys-uqbie3`: OpenAPI 3.0.3 document and ogen generation | `5e36342`                                          |
| MyLinks | `mys-m4zgzu`: discovery                                  | `e78a2db`                                          |
| MyCal   | `mys-jiijqf`                                             | `64146bc`                                          |
| MyMail  | `mys-k1xdht`                                             | `8dd04e5`                                          |
| MyNotes | `mys-o669cx`                                             | `2388858`                                          |

MyCal's, MyMail's and MyNotes' discovery commits also upgrade them from ogen v1.22.0 to v1.24.0.
MyLinks had no ogen before this work; its prerequisite `5e36342` introduces it at v1.24.0. Each app's agent reported a full build passing and a cross-harness review folded in. This
repository has not re-verified those reports. All five issues were closed by the owner on 2026-10-14.

## 8. Known gaps

- **Relative Linkset URIs have not been tested against a third-party RFC 9727 client.** The owner
  accepted relative URIs knowing this (§5.3). A client that stores the catalog without the URL it
  was retrieved from cannot resolve them.
- **Source set.** This contract was written from the API-discovery discussion on 2026-10-14 (the
  standards survey, the ogen measurement in §5.1, RFC 9727's text read the same day) and from
  each app's `openapi.yaml`, `go.mod`, `main.go` routing, and CI workflows at that date. MyLinks'
  routes were read from `cmd/mylinks/web/handlers.go`.

## 9. Withdrawn rules

None yet.
