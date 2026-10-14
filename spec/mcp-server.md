# MCP servers

**Status: binding, implemented in all three; §7 lists the commits.** The design decisions in §5 were
made by the owner on 2026-10-14, who then had all three apps implement it the same day. Adoption
was tracked as one AWB issue per app, all closed (§7).

## 1. What it covers

Each of MyCal, MyMail and MyNotes ships one more binary: a Model Context Protocol (MCP) server
that an MCP client starts as a subprocess and talks to over stdio. It exposes, as MCP resources and
tools, **exactly the bearer-protected API routes an API token can reach** in that app, and nothing
else. Routes every client can reach without credentials (API discovery, MyNotes' published notes)
are not part of that surface; §2.3 lists them.

| App     | Repo         | Binary        | Source       | Resource URI scheme |
|---------|--------------|---------------|--------------|---------------------|
| MyCal   | `../mycal`   | `mycal-mcp`   | `cmd/mcp/`   | `mycal:`            |
| MyMail  | `../mymail`  | `mymail-mcp`  | `cmd/mcp/`   | `mymail:`           |
| MyNotes | `../mynotes` | `mynotes-mcp` | `cmd/mcp/`   | `mynotes:`          |

Like `spec/device-login.md` and `spec/api-discovery.md`, this is an app integration protocol, not a
UI contract. Nothing in it is rendered, and `spec/measurement-protocol.md` does not apply. It
binds three apps; MyLinks and MyPass are out of scope (§6).

The MCP server is an HTTP **client** of the app's running server, in the same way as `*-cli`. It
holds no data and makes no authorization decision. Scoping, the snapshot reads and the write
barrier all stay in each server's bearer-token middleware, which is the only authorization
boundary (§5.1).

## 2. Mandated behaviour

### 2.1 Process, transport and configuration

- The only transport is **stdio**: newline-delimited JSON-RPC on stdin/stdout, as in the MCP
  specification. When the binary runs the transport, stdout carries protocol messages and nothing
  else, from the first byte. Diagnostics go to stderr. `-help` is the one exception: it prints
  usage to stdout and exits without starting the transport.
- The binary is **statically linked**: built with `CGO_ENABLED=0` and `-tags netgo`. This is
  held by the build command alone; §4 does not verify it (§5.9).
- It uses `github.com/modelcontextprotocol/go-sdk` **v1.8.0**.
- The MCP `serverInfo.name` is the binary name (`mycal-mcp`, …). `serverInfo.version` is local.
- Flags and environment, matching that app's `*-cli`:

  | Flag               | Default                                   | Meaning                           |
  |--------------------|-------------------------------------------|-----------------------------------|
  | `-url URL`         | `MYCAL_URL`, else `http://127.0.0.1:8080` | server base URL, may carry a path |
  | `-token-file PATH` | `MYCAL_TOKEN_FILE`                        | read the API token from a file    |
  | `-help`            |                                           | print usage to stdout, exit 0     |

  with `MYMAIL_` and `MYNOTES_` in the other two. There is **no `-token-stdin`**, because stdin
  is the protocol channel.
- **No token is not an error.** Without `-token-file` or the environment variable, the server
  runs unauthenticated and sends no `Authorization` header, as `*-cli` does. That works against a
  server with no Basic authentication configured; against one with it, every read fails with the
  401 message in §2.5.
- **The exposed surface does not depend on authentication.** An unauthenticated server would
  answer more routes than a token can reach; the MCP server still exposes only the token surface
  in §2.3, so the same binary offers the same resources and tools against every server.
- URL rules are `*-cli`'s, by reusing that app's `internal/clihttp`: plain HTTP only to a literal
  loopback address, HTTPS otherwise; redirects and environment HTTP proxies disabled.
- Startup fails, with a message on stderr and exit status 1, only on bad configuration: an
  unparseable or disallowed URL, or a token file that cannot be read or is empty. An unreachable
  server is **not** a startup failure; it is reported per request (§2.5).
- The token secret never appears on stdout, on stderr, or in any resource or tool result. That
  includes text the server or a proxy sends back. An error body echoing the `Authorization`
  header has the secret replaced in the error text taken from its `error` field, and an error
  body shown as it is (§2.5) is not shown at all if it contains the secret. A successful body
  containing it is **refused whole**, as an error, because §2.4 passes a body's bytes through
  unchanged or not at all. "Containing" covers a JSON string that decodes to it (`\u0072…`), not
  only its literal bytes, since the server's own decoding (MyMail's `/text`, completion) would
  otherwise hand the secret on, and it covers every string in the body, keys and repeated
  members included: a decoded map keeps only the last of a repeated key.

### 2.2 Resources first, tools only where a resource cannot work

- A read is an MCP **resource**. A fixed read is a static resource listed by `resources/list`. A
  read with parameters is a **resource template** (RFC 6570) listed by `resources/templates/list`.
- **Free-text search is a tool**, in all three apps. A search is a query the model formulates,
  not a document it addresses.
- **A write is a tool.** There is one: MyMail's `mark_message_read`.
- `resources/list` returns only the static resources in §2.3. It never enumerates notes, events
  or messages.
- Resources do not support subscription, and the server does not send `list_changed`.

### 2.3 The surface, per app

Query parameter names and values in a resource URI are **the API's own**, forwarded unchanged
except where noted. A list-valued parameter is repeated (`calendar_id=1&calendar_id=2`), which is
what RFC 6570's exploded `{?name*}` produces and what each API accepts. Tool argument names are
also the API's parameter names, with the API's types: a list-valued argument is a JSON array
(MyCal `calendar_id`: array of integers; MyNotes `tag`: array of strings), forwarded as the
repeated query parameter. Path variables are percent-decoded from the URI and
percent-encoded again into the HTTP path.

**MyCal**

| Resource or tool                                  | MIME type          | API request                   |
|---------------------------------------------------|--------------------|-------------------------------|
| `mycal://calendars` (static)                      | `application/json` | `GET /api/v1/calendars`       |
| `mycal://events{?from,to,calendar_id*,limit,offset}` | `application/json` | `GET /api/v1/events`       |
| `mycal://events/{id}`                             | `application/json` | `GET /api/v1/events/{id}`     |
| `mycal://events/{id}/ics`                         | `text/calendar`    | `GET /api/v1/events/{id}/ics` |
| `mycal://calendar.ics{?calendar_id*}`             | `text/calendar`    | `GET /api/v1/events.ics`      |
| tool `search_events(q, from?, to?, calendar_id?, limit?, offset?)` | `application/json` | `GET /api/v1/events?q=…` |

- `from` and `to` are required by `mycal://events`. Both there and in `search_events` they accept
  the forms `mycal-cli` accepts — RFC 3339, `YYYY-MM-DD`, `YYYY-MM-DD[T or space]HH:MM[:SS]` —
  and are converted to RFC 3339 exactly as `mycal-cli` converts them. This is the one exception
  to forwarding values unchanged, and §5.4 says why.
- `limit` (1–200) and `offset` page both. They were added to the API for this server, in MyCal
  `cb4d43d`; without `limit` the response is unbounded, as it was before, from `offset` on. A recurring event is
  expanded before paging in a listing; search pages the stored events, newest first.
- In `search_events`, `from` and `to` are given together or not at all, as in `mycal-cli`.
- **`search_events` returns no `structuredContent`.** The API answers with a JSON array, and
  go-sdk v1.8.0 appends a second, re-serialised text block to any structured output that is not
  an object (`mcp/server.go`, read 2026-10-14), which would break the one-text-block rule below.
  Its one text block is the server's bytes.
- `mycal://calendar.ics` with no query is also a static resource, the whole feed.
- Event IDs may be composite (`42_2026-03-09T09:00:00Z`) and are percent-encoded in the URI.
- `calendar_id` in `search_events` is an array of integers, forwarded as repeated `calendar_id`
  parameters.
- **MyCal scopes by filtering, not by refusing.** A token's calendar IDs are intersected with the
  ones requested, so an out-of-scope calendar yields a shorter or empty list, and an out-of-scope
  event is 404. The MCP server passes that through; it does not turn either into a scope error.

**MyMail**

| Resource or tool                                                                                         | MIME type                         | API request                                                                           |
|----------------------------------------------------------------------------------------------------------|-----------------------------------|---------------------------------------------------------------------------------------|
| `mymail://folders` (static)                                                                              | `application/json`                | `GET /api/v1/folders`, which the server filters to the token's folders                |
| `mymail://folders/{folder_id}/messages{?limit,offset,unread,flagged}`                                    | `application/json`                | `GET /api/v1/folders/{folder_id}/messages`                                            |
| `mymail://messages/{id}`                                                                                 | `application/json`                | `GET /api/v1/messages/{id}`                                                           |
| `mymail://messages/{id}/text`                                                                            | `text/plain`                      | `body_text` of `GET /api/v1/messages/{id}`, as `mymail-cli messages text` extracts it |
| `mymail://messages/{id}/headers`                                                                         | `text/plain`                      | `GET /api/v1/messages/{id}/headers`                                                   |
| `mymail://messages/{id}/body{?external}`                                                                 | `text/html`                       | `GET /api/v1/messages/{id}/body`                                                      |
| `mymail://messages/{id}/raw`                                                                             | `message/rfc822`, blob            | `GET /api/v1/messages/{id}/raw`                                                       |
| `mymail://attachments/{id}`                                                                              | the server's `Content-Type`, blob | `GET /api/v1/attachments/{id}`                                                        |
| tool `search_messages(folder_id, q, date_from?, date_to?, from_addr?, to_addr?, sort?, limit?, offset?)` | `application/json`                | `GET /api/v1/messages/search`                                                         |
| tool `mark_message_read(id)`                                                                             | none                              | `PUT /api/v1/messages/{id}/read`                                                      |

- **MyMail's bearer middleware answers a message outside the token's folders and a message that
  does not exist alike, with 403**, so the scope message says it may be either. Without a token
  against a server with no Basic authentication, a missing message is 404 and reads as not found.
- `search_messages` **requires `folder_id`**, in its input schema. That is the server's rule for
  bearer requests (exactly one `folder_id`), stated where a model reads it.
- `mark_message_read` is annotated `readOnlyHint: false`, `destructiveHint: false`,
  `idempotentHint: true`, `openWorldHint: false`. On 204 it returns a text result saying the
  message is marked read.

**MyNotes**

| Resource or tool                                            | MIME type                         | API request                                  |
|-------------------------------------------------------------|-----------------------------------|----------------------------------------------|
| `mynotes://tags` (static)                                   | `application/json`                | `GET /api/v1/tags`                           |
| `mynotes://notes{?tag*,sort,order,limit,offset}`            | `application/json`                | `GET /api/v1/notes`                          |
| `mynotes://notes/{slug}`                                    | `application/json`                | `GET /api/v1/notes/{slug}`                   |
| `mynotes://notes/{slug}/markdown`                           | `text/markdown`                   | `GET /api/v1/notes/{slug}/download-markdown` |
| `mynotes://artifacts/{sha256}`                              | the server's `Content-Type`, blob | `GET /api/v1/artifacts/{sha256}`             |
| tool `search_notes(q, titlePrefix?, tag?, limit?, offset?)` | `application/json`                | `GET /api/v1/notes?q=…`                      |

- `mynotes://notes` with no query is also a static resource, the first page of the browse list.
- `tag` in `search_notes` is an array of strings, forwarded as repeated `tag` parameters.
- `search_notes` has no `sort` or `order`: the API ignores both when `q` is set.

**Every search tool** is annotated `readOnlyHint: true`, `openWorldHint: false`. Its input schema
marks `q` required. It returns the server's JSON as one text block, the server's bytes, not a
re-serialisation, and, where that JSON is an object (MyMail, MyNotes), also as
`structuredContent`.

**Excluded, deliberately**, and the drift test (§4) lists exactly these. Routes reachable without
any credential, which a token can also reach:

- In all three: `GET /openapi.yaml` and `GET /.well-known/api-catalog` (`spec/api-discovery.md`).
- MyNotes: `GET /public/…` (published notes, their artifacts and stylesheet), which the bearer
  middleware hands to the full-access handler before looking at the token.

Bearer-protected routes:

- MyCal `GET /calendar.ics`: documented in MyCal's `openapi.yaml` as *"Same as
  `/api/v1/events.ics`"*, a convenience URL for calendar apps.
- MyCal's `calendar` query parameter (filter by calendar name), described there as *"backward
  compatible"*. `calendar_id` covers it.
- MyNotes `GET /api/v1/icons/…`: UI assets.
- `HEAD` on any route. It adds nothing a `GET` does not.

### 2.4 Resource contents

- The MIME type column in §2.3 is what the server is expected to send. **The response decides**:
  `mimeType` in the result is the response's `Content-Type`, without parameters.
- The resources marked **blob** in §2.3 (MyMail raw and attachments, MyNotes artifacts) are always
  returned as blobs, whatever their bytes. Every other resource is returned as **text** when the
  response's `Content-Type` is `text/*` or `application/json` and its body is valid UTF-8, and as a
  blob otherwise.
- **An empty body is an empty blob**, whatever the resource. go-sdk v1.8.0 drops an empty `text`
  field from the wire (`omitempty`) but keeps an empty, non-nil `blob` (`omitzero`, serialised as
  `""`), so empty text would arrive as contents that are neither. MyMail's
  `mymail://messages/{id}/text` for a message with no plain-text body is the case that will
  happen.
- **A draft has no raw form.** MyMail answers `/messages/{id}/raw` for a draft with 200,
  `application/json` and `{}` (its `openapi.yaml`). `mymail://messages/{id}/raw` turns that into a
  read error saying the message is a draft, not a two-byte blob.
- JSON is passed through as the server sent it. The MCP layer does not reshape it.
- **Every resource is capped at 1 MiB** (1,048,576 bytes) of response body, text and blob alike.
  The server reads at most one byte more than the cap; a body over it fails the read with an error
  naming the limit. It is never truncated. The same cap applies to the response a tool reads. A
  search pages, but MyCal's is unbounded whenever `limit` is omitted, so the cap
  is what bounds it.
- **Unknown query parameters are rejected** without an HTTP request. A resource URI reaches only
  the parameters in its template, so search cannot be reached through `mycal://events?q=…`. On a
  template that takes a query, the handler refuses an unknown or repeated parameter with JSON-RPC
  code **-32603** and a message saying what to do instead (§5.8). A query on a resource or template
  that takes none matches no template, so the SDK's dispatch refuses it as "Resource not found"
  (-32602 in go-sdk v1.8.0) before any handler runs.
- Query parameters may appear in any order and list parameters may repeat. **The handler parses
  the query itself** (§3), because the SDK's template library does neither.

### 2.5 Errors

| Condition                             | Resource read                                                                    | Tool call                   |
|---------------------------------------|----------------------------------------------------------------------------------|-----------------------------|
| 401, token configured                 | JSON-RPC error: token expired or revoked; run `mycal-token login`                | `isError` result, same text |
| 401, no token                         | JSON-RPC error: the server requires authentication; set `MYCAL_TOKEN_FILE`       | `isError` result, same text |
| 403                                   | JSON-RPC error: outside this token's scope (MyMail; MyCal filters instead, §2.3) | `isError` result, same text |
| 404                                   | the SDK's `ResourceNotFoundError`                                                | `isError` result            |
| other status                          | JSON-RPC error carrying the status and the server's error field (§2.5 below)     | `isError` result, same text |
| network failure                       | JSON-RPC error                                                                   | `isError` result            |
| response over the cap                  | JSON-RPC error naming the limit                                                  | `isError` result, same text |
| missing required or unknown parameter | -32603 with the reason, or the SDK's not-found (§2.4); without an HTTP request | `isError` result, without an HTTP request |

The binary and variable names in the messages are each app's own. No message echoes the token.

An error body is read under the same 1 MiB cap as any other. Its error field is carried whole or
not at all: a body over the cap gives the status alone. The field is `error` in the API's own
errors and **`error_message`** when ogen rejects a request before the handler runs (an
out-of-range or malformed query parameter); ogen v1.24.0 writes the latter in
`ogenerrors/handler.go`, and all three apps use ogen. A body that is not the API's error shape,
such as a proxy's page, is shown only when it is short (MyNotes: up to 1 KiB of UTF-8).

### 2.6 Completion

The server supports `completion/complete` for exactly these template arguments, whose values the
token can list cheaply: MyCal `calendar_id` (from `/api/v1/calendars`), MyMail `folder_id` (from
`/api/v1/folders`), MyNotes `tag` (from `/api/v1/tags`). Nothing else is completed. Note slugs,
event IDs and message IDs are unbounded collections.

## 3. Mechanisms: mandated and local

**Mandated:** the binary names, flags, environment variables, stdio, static linking, the SDK
version, the URI schemes and templates, which reads are resources and which are tools, tool names
and argument names, annotations, the text/blob rule, the resource cap, the error mapping and its
wording's content, completion's scope, and that the surface equals the token surface.

**Local:** the package layout under `cmd/mcp/`, how requests are built (reusing the app's
`internal/clihttp` is expected but the URL rules are what is mandated), `serverInfo.version`, the
exact error wording, and server `instructions` text if any.

**Why handlers parse URIs themselves.** go-sdk v1.8.0 dispatches a `resources/read` by matching the
URI against each template's regular expression from `github.com/yosida95/uritemplate/v3` v3.0.2.
Measured on 2026-10-14 against that version:

> `{?from,to,calendar_id*}` against `?to=b&from=a` matches, and `Match` returns no values.
> Against `?from=a&to=b&calendar_id=1&calendar_id=2` it matches, and `Match` returns
> `calendar_id` as empty. Against `?bogus=1` it matches.
> The query-value character class excludes an unencoded `:` and `+`.

So the template decides **which handler** runs, and the handler parses the URI with `net/url`.
That is a reading of one version of two libraries, not a property of MCP; re-run it before
relying on it after an upgrade.

## 4. Verification

Each app holds its own half, in its Go test suite, using go-sdk's in-memory transports against an
`httptest` server that runs **the app's real router behind its real bearer middleware and a real
token store**. Not a mock: the point is that authorization is the server's.

1. **The drift test.** Enumerate the static resources, templates and tools the MCP server offers.
   Every one maps to a route the bearer middleware permits. Every route the bearer middleware
   permits is covered, or is on the exclusion list in §2.3, which the test holds verbatim.
2. Each resource and tool returns what the API returns for the same request, with the MIME type
   and text/blob form in §2.4.
3. **Scope**, as each server enforces it. MyMail: a token scoped to folder A gets the 403 error
   for B through each resource template and `search_messages`; `mark_message_read` succeeds in
   scope, is idempotent, and gets 403 out of scope. MyCal: with a token scoped to calendar A,
   `mycal://calendars`, `mycal://events`, `mycal://calendar.ics` and `search_events` return
   nothing from B even when B is requested, and an event in B is not found.
4. **No token**: reads succeed against a server without Basic authentication and give the
   no-token 401 message against one with it.
5. A response body of exactly 1 MiB is returned, as a text resource, as a blob resource and
   through a search tool; one byte more is refused in all three.
6. Query parameters out of order and repeated are honoured; an unknown one is refused with -32603
   and its reason, without an HTTP request; MyCal `from=2026-10-01` is accepted.
7. Startup with a disallowed URL or an unreadable token file exits 1 and writes nothing to stdout.
8. `completion/complete` returns values for exactly the arguments in §2.6, from the server, and
   nothing for any other argument.
9. Every tool's annotations and input schema are as in §2.3: required arguments marked required,
    list arguments typed as arrays.
10. A configured token that the server rejects gives the token-configured 401 message.
11. With the server down, startup succeeds and each read and tool call reports the failure.
12. The token secret appears in no stdout, stderr, result or error, on any of the paths above,
    including a successful response and an error response that echo it, literally or JSON-escaped,
    and in a repeated JSON member.
13. The `initialize` result advertises no resource subscription and no `listChanged`.
14. A draft's raw resource gives the draft error, not a blob.
15. An empty body arrives as an empty blob, with the response's MIME type.
16. An out-of-range query parameter, rejected by ogen, gives the `error_message` text, not the raw
    body.

**Nothing checks the three against each other** (`AGENTS.md` §2.1). `tools/check-contract.py`
does not check this contract.

## 5. Decisions recorded

### 5.1 A stdio client, not an endpoint in the server

Ruled by the owner on 2026-10-14: stdio only, separate binaries. The alternative was a Streamable
HTTP endpoint at `/mcp` inside each server. A client keeps authorization where it already is and
adds no server attack surface. A remote endpoint would also have to answer the MCP authorization
specification (OAuth with RFC 9728 protected-resource metadata), which `spec/device-login.md` and
`spec/api-discovery.md` §6 put out of scope.

### 5.2 Unauthenticated runs are allowed

Ruled by the owner on 2026-10-14, matching `*-cli`. The surface stays the token surface (§2.1).

### 5.3 Resources wherever possible; search and writes are tools

Ruled by the owner on 2026-10-14, in two steps: resources wherever possible, then free-text search
as a tool in all three. **The cost, accepted:** resources are read when the client chooses to. An
MCP client that exposes only tools to its model will see little of these servers.

### 5.4 MyCal date forms

Not an owner ruling; recorded here so it can be overruled. A model writing a resource URI by hand
writes `from=2026-10-01T09:00:00Z`, whose unencoded `:` fails the SDK's template match (§3) with
"Resource not found", which reads as though the resource does not exist. Accepting `mycal-cli`'s
date-only form avoids the common case, and reuses a parser MyCal already ships.

**The remaining case stays as documented, by the owner's ruling on 2026-10-14**, after trying
MyCal from Claude Code, where `from=2026-10-01T00:00:00Z` gave *"Resource not found"*. The
alternative considered was an extra catch-all template using RFC 6570's reserved expansion
(`{+…}`), whose match permits `:`, so that such URIs reach the handler. It was not adopted: it
adds a confusing entry to every app's template list. MyCal's server instructions suggest a date
such as `2026-10-01`, and its user manual says to percent-encode the colons of a time.

### 5.5 `mark_message_read` is exposed

Ruled by the owner on 2026-10-14. It is the only write a token can make in any of the three apps.

### 5.6 The 1 MiB resource cap

Ruled by the owner on 2026-10-14, first for blobs and then, the same day, for text resources too,
closing what §8 had listed as a gap.

### 5.7 Tool argument errors are tool results

Measured while implementing MyNotes, on 2026-10-14: go-sdk v1.8.0 validates tool arguments against
the input schema and reports a failure as a tool result with `isError`, not as a JSON-RPC error.
The contract first said invalid params; it now follows the SDK, which also lets a model read the
message and retry. The inferred schema already refuses unknown properties
(`additionalProperties: false`). It types every Go slice as `["null", "array"]`, so an
implementation pins list arguments to `array` explicitly (§2.3).

### 5.8 A refusal is -32603, so its message survives the client

Ruled by the owner on 2026-10-14, after trying MyNotes from Claude Code. go-sdk v1.8.0 gives
"Resource not found" the invalid-params code, -32602, and Claude Code shows every -32602 from
`resources/read` as *"Resource not found … the URI is stale"*. A refusal sent as invalid params
therefore lost its message, including *"use the search_notes tool to search"*, which is what lets
a model recover. Sent as -32603, the message reaches the model, as an HTTP 400's did in the same
session. The cost, accepted: the code no longer says the request was malformed.

### 5.9 Static linking is required but not verified

Ruled by the owner on 2026-10-14: the check was dropped. MyNotes' first implementation had
`build.sh` assert `CGO_ENABLED=0` and `-tags=netgo` in `go version -m`, and the owner removed it.
The build flags in §2.1 stay mandated; nothing checks that a built binary carries them.

## 6. Out of scope

- An HTTP or SSE transport, and MCP authorization (§5.1).
- MyLinks and MyPass. MyLinks is bound by `api-discovery.md` but has no API tokens: its Go sources had no bearer handling on 2026-10-14.
- Anything a token cannot reach, even when the server is unauthenticated (§2.1).
- Prompts, sampling, elicitation, roots and logging capabilities.
- Resource subscriptions and change notifications.

## 7. Adoption

Each app's adoption also adds a reference to this contract in its own `AGENTS.md` files, beside
its references to `spec/device-login.md` and `spec/api-discovery.md` (`spec/README.md`, *Adding a
contract*).

| App     | AWB issue | Implementing commit |
|---------|-----------|---------------------|
| MyNotes | `mys-ld3qsf` | `5ab2327`, `7c80584` (refusing a body that contains the token), `a0aeefe` (checking every JSON string) |
| MyMail  | `mys-07x53a` | `ca9527f`, `4fd4a86` (checking every JSON string) |
| MyCal   | `mys-5rbsw8` | `5bf3c4e`; it needed paging for `GET /api/v1/events` first, `mys-dxqj7x`, MyCal `cb4d43d` |

All of these were on each repository's `origin/main` on 2026-10-14, read from the local
remote-tracking refs, not by querying the remotes. All four issues were closed the same day. Each app's first commit (`5ab2327`, `ca9527f`, `5bf3c4e`) adds its
`AGENTS.md` references.
`./build.sh` passed at every commit listed, on 2026-10-14, after a cross-harness review was folded
in.

The order changed from the plan: MyMail went second while MyCal waited for paging.

## 8. Known gaps

- **The drift test sees only documented routes.** All three implementations enumerate the
  operations a token may use from `openapi.yaml`, probed through the bearer middleware (MyNotes:
  its GET operations; MyMail and MyCal: every operation, with IDs the token can reach), so a
  bearer-reachable route missing from `openapi.yaml` is invisible to it. MyCal's test fixture also
  omits the public discovery routes, which `openapi.yaml` does not list.
- **Tried against one client besides the SDK's own: Claude Code, on 2026-10-14, by hand, with
  all three, against the owner's own servers and tokens.** MyNotes: static resources, a template
  read with query parameters, a note as JSON and Markdown, an artifact blob, `search_notes`, a
  not-found read and refusals; that trial produced §5.8 and the `error_message` rule in §2.5.
  MyMail: folders, a folder page, a message as JSON, text and headers, raw and attachment blobs,
  `search_messages`, `mark_message_read` on an already-read message, a scope error and a
  refusal. MyCal: calendars, events by date and by percent-encoded time with paging, an event as
  iCalendar, `search_events`, scope filtering and refusals; that trial produced the ruling in
  §5.4. Not every binary tried was the final commit in §7. Nothing automated runs against any
  client but the SDK's, and other clients present resource templates to their models
  differently.
- **Source set.** Written from the MCP planning discussion of 2026-10-14 with the owner's rulings
  in §5, and from, at the commits below: each app's bearer-token middleware (MyCal
  `internal/token/bearer.go`, MyMail `internal/token/token.go` `Bearer`, MyNotes
  `internal/token/bearer.go`), `openapi.yaml`, `cmd/cli/main.go` and `build.sh`; MyCal `64146bc`,
  MyMail `8dd04e5`, MyNotes `2388858`; for MyCal's paging, its `openapi.yaml` at `cb4d43d`. go-sdk
  v1.8.0's `mcp/resource.go` and `mcp/server.go`, and the template measurement in §3. Corrected
  since from each implementation and the cross-harness reviews of them, as §5 and §7 record.

## 9. Withdrawn rules

None yet.
