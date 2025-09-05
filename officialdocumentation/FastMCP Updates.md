---
title: "FastMCP Updates"
source: "https://gofastmcp.com/updates"
author:
  - "[[FastMCP]]"
published:
created: 2025-09-04
description:
tags:
  - "clippings"
---
FastMCP 2.12

Releases

December 31, 2024FastMCP 2.11

Releases

December 13, 2024FastMCP 2.10

Releases

November 21, 2024FastMCP 2.9

Releases Blog Posts

June 23, 2025

[![_image?href=%2F_astro%2Fhero.BkVTdeBk](https://jlowin.dev/_image?href=%2F_astro%2Fhero.BkVTdeBk.jpg&w=1200&h=630&f=png)](https://www.jlowin.dev/blog/fastmcp-2-9-middleware)

## [FastMCP 2.9: MCP-Native Middleware](https://www.jlowin.dev/blog/fastmcp-2-9-middleware)

[

FastMCP 2.9 is a major release that, among other things, introduces two important features that push beyond the basic MCP protocol.🤝 *MCP Middleware* brings a flexible middleware system for intercepting and controlling server operations - think authentication, logging, rate limiting, and custom business logic without touching core protocol code.✨ *Server-side type conversion* for prompts solves a major developer pain point: while MCP requires string arguments, your functions can now work with native Python types like lists and dictionaries, with automatic conversion handling the complexity.These features transform FastMCP from a simple protocol implementation into a powerful framework for building sophisticated MCP applications. Combined with the new `File` utility for binary data and improvements to authentication and serialization, this release makes FastMCP significantly more flexible and developer-friendly while maintaining full protocol compliance.

](https://www.jlowin.dev/blog/fastmcp-2-9-middleware)FastMCP 2.8

Releases Blog Posts

June 11, 2025

[![_image?href=%2F_astro%2Fhero.su3kspkP](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.su3kspkP.png&w=1000&h=500&f=webp)](https://www.jlowin.dev/blog/fastmcp-2-8-tool-transformation)

## [FastMCP 2.8: Transform and Roll Out](https://www.jlowin.dev/blog/fastmcp-2-8-tool-transformation)[FastMCP 2.8 is here, and it’s all about taking control of your tools.This release is packed with new features for curating the perfect LLM experience:🛠️ Tool Transformation The headline feature lets you wrap any tool—from your own code, a third-party library, or an OpenAPI spec—to create an enhanced, LLM-friendly version. You can rename arguments, rewrite descriptions, and hide parameters without touching the original code.This feature was developed in close partnership with Bill Easton. As Bill brilliantly](https://www.jlowin.dev/blog/fastmcp-2-8-tool-transformation) [put it](https://www.linkedin.com/posts/williamseaston_huge-thanks-to-william-easton-for-providing-activity-7338011349525983232-Mw6T?utm_source=share&utm_medium=member_desktop&rcm=ACoAAAAd6d0B3uL9zpCsq9eYWKi3HIvb8eN_r_Q), “Tool transformation flips Prompt Engineering on its head: stop writing tool-friendly LLM prompts and start providing LLM-friendly tools.” 🏷️ Component Control Now that you’re transforming tools, you need a way to hide the old ones! In FastMCP 2.8 you can programmatically enable/disable any component, and for everyone who’s been asking what FastMCP’s tags are for—they finally have a purpose! You can now use tags to declaratively filter which components are exposed to your clients.🚀 Pragmatic by Default Lastly, to ensure maximum compatibility with the ecosystem, we’ve made the pragmatic decision to default all OpenAPI routes to Tools, making your entire API immediately accessible to any tool-using agent. When the industry catches up and supports resources, we’ll restore the old default — but no reason you should do extra work before OpenAI, Anthropic, or Google!FastMCP 2.7

Releases

June 6, 2025FastMCP 2.6

Releases Blog Posts

June 2, 2025

[![_image?href=%2F_astro%2Fhero.Bsu8afiw](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.Bsu8afiw.png&w=1000&h=500&f=webp)](https://www.jlowin.dev/blog/fastmcp-2-6)

## [FastMCP 2.6: Blast Auth](https://www.jlowin.dev/blog/fastmcp-2-6)

[

FastMCP 2.6 is here!This release introduces first-class authentication for MCP servers and clients, including pragmatic Bearer token support and seamless OAuth 2.1 integration. This release aligns with how major AI platforms are adopting MCP today, making it easier than ever to securely connect your tools to real-world AI models. Dive into the update and secure your stack with minimal friction.

](https://www.jlowin.dev/blog/fastmcp-2-6)Vibe-Testing

Blog Posts Tutorials

May 21, 2025

[![_image?href=%2F_astro%2Fhero.BUPy9I9c](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.BUPy9I9c.png&w=1000&h=500&f=webp)](https://www.jlowin.dev/blog/stop-vibe-testing-mcp-servers)

## [Stop Vibe-Testing Your MCP Server](https://www.jlowin.dev/blog/stop-vibe-testing-mcp-servers)

[

Your tests are bad and you should feel bad.Stop vibe-testing your MCP server through LLM guesswork. FastMCP 2.0 introduces in-memory testing for fast, deterministic, and fully Pythonic validation of your MCP logic—no network, no subprocesses, no vibes.

](https://www.jlowin.dev/blog/stop-vibe-testing-mcp-servers)10,000 Stars

Blog Posts

May 8, 2025

[![_image?href=%2F_astro%2Fhero.Cnvci9Q_](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.Cnvci9Q_.png&w=1000&h=500&f=webp)](https://www.jlowin.dev/blog/fastmcp-2-10k-stars)

## [Reflecting on FastMCP at 10k stars 🌟](https://www.jlowin.dev/blog/fastmcp-2-10k-stars)

[

In just six weeks since its relaunch, FastMCP has surpassed 10,000 GitHub stars—becoming the fastest-growing OSS project in our orbit. What started as a personal itch has become the backbone of Python-based MCP servers, powering a rapidly expanding ecosystem. While the protocol itself evolves, FastMCP continues to lead with clarity, developer experience, and opinionated tooling. Here’s to what’s next.

](https://www.jlowin.dev/blog/fastmcp-2-10k-stars)FastMCP 2.3

Blog Posts Releases

May 8, 2025

[![_image?href=%2F_astro%2Fhero.M_hv6gEB](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.M_hv6gEB.png&w=1000&h=500&f=webp)](https://www.jlowin.dev/blog/fastmcp-2-3-streamable-http)

## [Now Streaming: FastMCP 2.3](https://www.jlowin.dev/blog/fastmcp-2-3-streamable-http)

[

FastMCP 2.3 introduces full support for Streamable HTTP, a modern alternative to SSE that simplifies MCP deployments over the web. It’s efficient, reliable, and now the default HTTP transport. Just run your server with transport=“http” and connect clients via a standard URL—FastMCP handles the rest. No special setup required. This release makes deploying MCP servers easier and more portable than ever.

](https://www.jlowin.dev/blog/fastmcp-2-3-streamable-http)Proxy Servers

Blog Posts Tutorials

April 23, 2025

[![_image?href=%2F_astro%2Frobot-hero.DpmAqgui](https://www.jlowin.dev/_image?href=%2F_astro%2Frobot-hero.DpmAqgui.png&w=1000&h=500&f=webp)](https://www.jlowin.dev/blog/fastmcp-proxy)

## [MCP Proxy Servers with FastMCP 2.0](https://www.jlowin.dev/blog/fastmcp-proxy)

[

Even AI needs a good travel adapter 🔌 FastMCP now supports proxying arbitrary MCP servers, letting you run a local FastMCP instance that transparently forwards requests to any remote or third-party server—regardless of transport. This enables transport bridging (e.g., stdio ⇄ SSE), simplified client configuration, and powerful gateway patterns. Proxies are fully composable with other FastMCP servers, letting you mount or import them just like local servers. Use `FastMCP.from_client()` to wrap any backend in a clean, Pythonic proxy.

](https://www.jlowin.dev/blog/fastmcp-proxy)FastMCP 2.0

Releases Blog Posts

April 16, 2025

[![_image?href=%2F_astro%2Fhero.DpbmGNrr](https://www.jlowin.dev/_image?href=%2F_astro%2Fhero.DpbmGNrr.png&w=1000&h=500&f=webp)](https://www.jlowin.dev/blog/fastmcp-2)

## [Introducing FastMCP 2.0 🚀](https://www.jlowin.dev/blog/fastmcp-2)

[

This major release reimagines FastMCP as a full ecosystem platform, with powerful new features for composition, integration, and client interaction. You can now compose local and remote servers, proxy arbitrary MCP servers (with transport translation), and generate MCP servers from OpenAPI or FastAPI apps. A new client infrastructure supports advanced workflows like LLM sampling.FastMCP 2.0 builds on the success of v1 with a cleaner, more flexible foundation—try it out today!

](https://www.jlowin.dev/blog/fastmcp-2)Official SDK

Announcements

December 3, 2024## [FastMCP is joining the official MCP Python SDK!](https://bsky.app/profile/jlowin.dev/post/3lch4xk5cf22c)

[FastMCP 1.0 will become part of the official MCP Python SDK!](https://bsky.app/profile/jlowin.dev/post/3lch4xk5cf22c)FastMCP 1.0

Releases Blog Posts

December 1, 2024

[![_image?href=%2F_astro%2Ffastmcp.Bep7YlTw](https://www.jlowin.dev/_image?href=%2F_astro%2Ffastmcp.Bep7YlTw.png&w=1000&h=500&f=webp)](https://www.jlowin.dev/blog/introducing-fastmcp)

## [Introducing FastMCP 🚀](https://www.jlowin.dev/blog/introducing-fastmcp)

[

Because life’s too short for boilerplate.This is where it all started. FastMCP’s launch post introduced a clean, Pythonic way to build MCP servers without the protocol overhead. Just write functions; FastMCP handles the rest. What began as a weekend project quickly became the foundation of a growing ecosystem.

](https://www.jlowin.dev/blog/introducing-fastmcp)