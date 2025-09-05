---
title: "OAuth Proxy"
source: "https://gofastmcp.com/servers/auth/oauth-proxy"
author:
  - "[[Authorization Phase]]"
  - "[[​]]"
published:
created: 2025-09-04
description: "Bridge traditional OAuth providers to work seamlessly with MCP's authentication flow."
tags:
  - "clippings"
---
`` New in version: `2.12.0` `` OAuth Proxy enables FastMCP servers to authenticate with OAuth providers that **don’t support Dynamic Client Registration (DCR)**. This includes virtually all traditional OAuth providers: GitHub, Google, Azure, Discord, Facebook, and most enterprise identity systems. For providers that do support DCR (like WorkOS AuthKit), use [`RemoteAuthProvider`](https://gofastmcp.com/servers/auth/remote-oauth) instead.MCP clients expect to register automatically and obtain credentials on the fly, but traditional providers require manual app registration through their developer consoles. OAuth Proxy bridges this gap by presenting a DCR-compliant interface to MCP clients while using your pre-registered credentials with the upstream provider. When a client attempts to register, the proxy returns your fixed credentials. When a client initiates authorization, the proxy handles the complexity of callback forwarding—storing the client’s dynamic callback URL, using its own fixed callback with the provider, then forwarding back to the client after token exchange.This approach enables any MCP client (whether using random localhost ports or fixed URLs like Claude.ai) to authenticate with any traditional OAuth provider, all while maintaining full OAuth 2.1 and PKCE security.

## Implementation

### Provider Setup Requirements

Before using OAuth Proxy, you need to register your application with your OAuth provider:
1. **Register your application** in the provider’s developer console (GitHub Settings, Google Cloud Console, Azure Portal, etc.)
2. **Configure the redirect URI** as your FastMCP server URL plus your chosen callback path:
	- Default: `https://your-server.com/auth/callback`
	- Custom: `https://your-server.com/your/custom/path` (if you set `redirect_path`)
	- Development: `http://localhost:8000/auth/callback`
3. **Obtain your credentials**: Client ID and Client Secret
4. **Note the OAuth endpoints**: Authorization URL and Token URL (usually found in the provider’s OAuth documentation)

The redirect URI you configure with your provider must exactly match your FastMCP server’s URL plus the callback path. If you customize `redirect_path` in OAuth Proxy, update your provider’s redirect URI accordingly.

### Basic Setup

Here’s how to implement OAuth Proxy with any provider:

### Configuration Parameters

## OAuthProxy Parameterstoken\_verifier

TokenVerifier

required

A [`TokenVerifier`](https://gofastmcp.com/servers/auth/token-verification) instance to validate the provider’s tokensbase\_url

AnyHttpUrl | str

required

Public URL of your FastMCP server (e.g., `https://your-server.com`)redirect\_path

str

default:"/auth/callback"

Path for OAuth callbacks. Must match the redirect URI configured in your OAuth applicationupstream\_revocation\_endpoint

str | None

Optional URL of provider’s token revocation endpointissuer\_url

AnyHttpUrl | str | None

Issuer URL for OAuth metadata (defaults to base\_url)service\_documentation\_url

AnyHttpUrl | str | None

Optional URL to your service documentationforward\_pkce

bool

default:"True"

Whether to forward PKCE (Proof Key for Code Exchange) to the upstream OAuth provider. When enabled and the client uses PKCE, the proxy generates its own PKCE parameters to send upstream while separately validating the client’s PKCE. This ensures end-to-end PKCE security at both layers (client-to-proxy and proxy-to-upstream).
- `True` (default): Forward PKCE for providers that support it (Google, Azure, GitHub, etc.)
- `False`: Disable only if upstream provider doesn’t support PKCEallowed\_client\_redirect\_uris

list\[str\] | None

List of allowed redirect URI patterns for MCP clients. Patterns support wildcards (e.g., `"http://localhost:*"`, `"https://*.example.com/*"`).
- `None` (default): All redirect URIs allowed (for MCP/DCR compatibility)
- Empty list `[]`: No redirect URIs allowed
- Custom list: Only matching patterns allowed
These patterns apply to MCP client loopback redirects, NOT the upstream OAuth app redirect URI.valid\_scopes

list\[str\] | None

List of all possible valid scopes for the OAuth provider. These are advertised to clients through the `/.well-known` endpoints. Defaults to `required_scopes` from your TokenVerifier if not specified.

### Using Built-in Providers

FastMCP includes pre-configured providers for common services:

```
from fastmcp.server.auth.providers.github import GitHubProvider

auth = GitHubProvider(

    client_id="your-github-app-id",

    client_secret="your-github-app-secret",

    base_url="https://your-server.com"

)

mcp = FastMCP(name="My Server", auth=auth)
```

Available providers include `GitHubProvider`, `GoogleProvider`, and others. These handle token verification automatically.

### Scope Configuration

OAuth scopes are configured through your `TokenVerifier`. Set `required_scopes` to automatically request the permissions your application needs:

```
JWTVerifier(..., required_scopes = ["read:user", "write:data"])
```

Dynamic clients created by the proxy will automatically include these scopes in their authorization requests.

## How It Works

<svg aria-roledescription="sequence" role="graphics-document document" viewBox="-50 -10 985.5 1170" style="max-width: 985.5px;" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns="http://www.w3.org/2000/svg" width="100%" id="_r_2o_"><g><rect class="actor actor-bottom" ry="3" rx="3" name="Provider" height="65" width="150" stroke="#666" fill="#eaeaea" y="1084" x="735.5"></rect><text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="1116.5" x="810.5"><tspan dy="-8" x="810.5">OAuth Provider</tspan></text> <text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="1116.5" x="810.5"><tspan dy="8" x="810.5">(GitHub, etc.)</tspan></text></g> <g><rect class="actor actor-bottom" ry="3" rx="3" name="Proxy" height="65" width="187" stroke="#666" fill="#eaeaea" y="1084" x="351"></rect><text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="1116.5" x="444.5"><tspan dy="-8" x="444.5">FastMCP OAuth Proxy</tspan></text> <text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="1116.5" x="444.5"><tspan dy="8" x="444.5">(server:8000)</tspan></text></g> <g><rect class="actor actor-bottom" ry="3" rx="3" name="Client" height="65" width="163" stroke="#666" fill="#eaeaea" y="1084" x="0"></rect><text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="1116.5" x="81.5"><tspan dy="-8" x="81.5">MCP Client</tspan></text> <text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="1116.5" x="81.5"><tspan dy="8" x="81.5">(localhost:random)</tspan></text></g> <g><line name="Provider" stroke="#999" stroke-width="0.5px" class="actor-line 200" y2="1084" x2="810.5" y1="65" x1="810.5" id="actor14"></line><g id="root-14"><rect class="actor actor-top" ry="3" rx="3" name="Provider" height="65" width="150" stroke="#666" fill="#eaeaea" y="0" x="735.5"></rect><text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="32.5" x="810.5"><tspan dy="-8" x="810.5">OAuth Provider</tspan></text> <text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="32.5" x="810.5"><tspan dy="8" x="810.5">(GitHub, etc.)</tspan></text></g></g> <g><line name="Proxy" stroke="#999" stroke-width="0.5px" class="actor-line 200" y2="1084" x2="444.5" y1="65" x1="444.5" id="actor13"></line><g id="root-13"><rect class="actor actor-top" ry="3" rx="3" name="Proxy" height="65" width="187" stroke="#666" fill="#eaeaea" y="0" x="351"></rect><text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="32.5" x="444.5"><tspan dy="-8" x="444.5">FastMCP OAuth Proxy</tspan></text> <text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="32.5" x="444.5"><tspan dy="8" x="444.5">(server:8000)</tspan></text></g></g> <g><line name="Client" stroke="#999" stroke-width="0.5px" class="actor-line 200" y2="1084" x2="81.5" y1="65" x1="81.5" id="actor12"></line><g id="root-12"><rect class="actor actor-top" ry="3" rx="3" name="Client" height="65" width="163" stroke="#666" fill="#eaeaea" y="0" x="0"></rect><text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="32.5" x="81.5"><tspan dy="-8" x="81.5">MCP Client</tspan></text> <text style="text-anchor: middle; font-size: 16px; font-weight: 400; font-family: inherit;" class="actor actor-box" alignment-baseline="central" dominant-baseline="central" y="32.5" x="81.5"><tspan dy="8" x="81.5">(localhost:random)</tspan></text></g></g> <g></g><defs><symbol height="24" width="24" id="computer"><path d="M2 2v13h20v-13h-20zm18 11h-16v-9h16v9zm-10.228 6l.466-1h3.524l.467 1h-4.457zm14.228 3h-24l2-6h2.104l-1.33 4h18.45l-1.297-4h2.073l2 6zm-5-10h-14v-7h14v7z" transform="scale(.5)"></path></symbol></defs><defs><symbol clip-rule="evenodd" fill-rule="evenodd" id="database"><path d="M12.258.001l.256.004.255.005.253.008.251.01.249.012.247.015.246.016.242.019.241.02.239.023.236.024.233.027.231.028.229.031.225.032.223.034.22.036.217.038.214.04.211.041.208.043.205.045.201.046.198.048.194.05.191.051.187.053.183.054.18.056.175.057.172.059.168.06.163.061.16.063.155.064.15.066.074.033.073.033.071.034.07.034.069.035.068.035.067.035.066.035.064.036.064.036.062.036.06.036.06.037.058.037.058.037.055.038.055.038.053.038.052.038.051.039.05.039.048.039.047.039.045.04.044.04.043.04.041.04.04.041.039.041.037.041.036.041.034.041.033.042.032.042.03.042.029.042.027.042.026.043.024.043.023.043.021.043.02.043.018.044.017.043.015.044.013.044.012.044.011.045.009.044.007.045.006.045.004.045.002.045.001.045v17l-.001.045-.002.045-.004.045-.006.045-.007.045-.009.044-.011.045-.012.044-.013.044-.015.044-.017.043-.018.044-.02.043-.021.043-.023.043-.024.043-.026.043-.027.042-.029.042-.03.042-.032.042-.033.042-.034.041-.036.041-.037.041-.039.041-.04.041-.041.04-.043.04-.044.04-.045.04-.047.039-.048.039-.05.039-.051.039-.052.038-.053.038-.055.038-.055.038-.058.037-.058.037-.06.037-.06.036-.062.036-.064.036-.064.036-.066.035-.067.035-.068.035-.069.035-.07.034-.071.034-.073.033-.074.033-.15.066-.155.064-.16.063-.163.061-.168.06-.172.059-.175.057-.18.056-.183.054-.187.053-.191.051-.194.05-.198.048-.201.046-.205.045-.208.043-.211.041-.214.04-.217.038-.22.036-.223.034-.225.032-.229.031-.231.028-.233.027-.236.024-.239.023-.241.02-.242.019-.246.016-.247.015-.249.012-.251.01-.253.008-.255.005-.256.004-.258.001-.258-.001-.256-.004-.255-.005-.253-.008-.251-.01-.249-.012-.247-.015-.245-.016-.243-.019-.241-.02-.238-.023-.236-.024-.234-.027-.231-.028-.228-.031-.226-.032-.223-.034-.22-.036-.217-.038-.214-.04-.211-.041-.208-.043-.204-.045-.201-.046-.198-.048-.195-.05-.19-.051-.187-.053-.184-.054-.179-.056-.176-.057-.172-.059-.167-.06-.164-.061-.159-.063-.155-.064-.151-.066-.074-.033-.072-.033-.072-.034-.07-.034-.069-.035-.068-.035-.067-.035-.066-.035-.064-.036-.063-.036-.062-.036-.061-.036-.06-.037-.058-.037-.057-.037-.056-.038-.055-.038-.053-.038-.052-.038-.051-.039-.049-.039-.049-.039-.046-.039-.046-.04-.044-.04-.043-.04-.041-.04-.04-.041-.039-.041-.037-.041-.036-.041-.034-.041-.033-.042-.032-.042-.03-.042-.029-.042-.027-.042-.026-.043-.024-.043-.023-.043-.021-.043-.02-.043-.018-.044-.017-.043-.015-.044-.013-.044-.012-.044-.011-.045-.009-.044-.007-.045-.006-.045-.004-.045-.002-.045-.001-.045v-17l.001-.045.002-.045.004-.045.006-.045.007-.045.009-.044.011-.045.012-.044.013-.044.015-.044.017-.043.018-.044.02-.043.021-.043.023-.043.024-.043.026-.043.027-.042.029-.042.03-.042.032-.042.033-.042.034-.041.036-.041.037-.041.039-.041.04-.041.041-.04.043-.04.044-.04.046-.04.046-.039.049-.039.049-.039.051-.039.052-.038.053-.038.055-.038.056-.038.057-.037.058-.037.06-.037.061-.036.062-.036.063-.036.064-.036.066-.035.067-.035.068-.035.069-.035.07-.034.072-.034.072-.033.074-.033.151-.066.155-.064.159-.063.164-.061.167-.06.172-.059.176-.057.179-.056.184-.054.187-.053.19-.051.195-.05.198-.048.201-.046.204-.045.208-.043.211-.041.214-.04.217-.038.22-.036.223-.034.226-.032.228-.031.231-.028.234-.027.236-.024.238-.023.241-.02.243-.019.245-.016.247-.015.249-.012.251-.01.253-.008.255-.005.256-.004.258-.001.258.001zm-9.258 20.499v.01l.001.021.003.021.004.022.005.021.006.022.007.022.009.023.01.022.011.023.012.023.013.023.015.023.016.024.017.023.018.024.019.024.021.024.022.025.023.024.024.025.052.049.056.05.061.051.066.051.07.051.075.051.079.052.084.052.088.052.092.052.097.052.102.051.105.052.11.052.114.051.119.051.123.051.127.05.131.05.135.05.139.048.144.049.147.047.152.047.155.047.16.045.163.045.167.043.171.043.176.041.178.041.183.039.187.039.19.037.194.035.197.035.202.033.204.031.209.03.212.029.216.027.219.025.222.024.226.021.23.02.233.018.236.016.24.015.243.012.246.01.249.008.253.005.256.004.259.001.26-.001.257-.004.254-.005.25-.008.247-.011.244-.012.241-.014.237-.016.233-.018.231-.021.226-.021.224-.024.22-.026.216-.027.212-.028.21-.031.205-.031.202-.034.198-.034.194-.036.191-.037.187-.039.183-.04.179-.04.175-.042.172-.043.168-.044.163-.045.16-.046.155-.046.152-.047.148-.048.143-.049.139-.049.136-.05.131-.05.126-.05.123-.051.118-.052.114-.051.11-.052.106-.052.101-.052.096-.052.092-.052.088-.053.083-.051.079-.052.074-.052.07-.051.065-.051.06-.051.056-.05.051-.05.023-.024.023-.025.021-.024.02-.024.019-.024.018-.024.017-.024.015-.023.014-.024.013-.023.012-.023.01-.023.01-.022.008-.022.006-.022.006-.022.004-.022.004-.021.001-.021.001-.021v-4.127l-.077.055-.08.053-.083.054-.085.053-.087.052-.09.052-.093.051-.095.05-.097.05-.1.049-.102.049-.105.048-.106.047-.109.047-.111.046-.114.045-.115.045-.118.044-.12.043-.122.042-.124.042-.126.041-.128.04-.13.04-.132.038-.134.038-.135.037-.138.037-.139.035-.142.035-.143.034-.144.033-.147.032-.148.031-.15.03-.151.03-.153.029-.154.027-.156.027-.158.026-.159.025-.161.024-.162.023-.163.022-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.011-.178.01-.179.008-.179.008-.181.006-.182.005-.182.004-.184.003-.184.002h-.37l-.184-.002-.184-.003-.182-.004-.182-.005-.181-.006-.179-.008-.179-.008-.178-.01-.176-.011-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.022-.162-.023-.161-.024-.159-.025-.157-.026-.156-.027-.155-.027-.153-.029-.151-.03-.15-.03-.148-.031-.146-.032-.145-.033-.143-.034-.141-.035-.14-.035-.137-.037-.136-.037-.134-.038-.132-.038-.13-.04-.128-.04-.126-.041-.124-.042-.122-.042-.12-.044-.117-.043-.116-.045-.113-.045-.112-.046-.109-.047-.106-.047-.105-.048-.102-.049-.1-.049-.097-.05-.095-.05-.093-.052-.09-.051-.087-.052-.085-.053-.083-.054-.08-.054-.077-.054v4.127zm0-5.654v.011l.001.021.003.021.004.021.005.022.006.022.007.022.009.022.01.022.011.023.012.023.013.023.015.024.016.023.017.024.018.024.019.024.021.024.022.024.023.025.024.024.052.05.056.05.061.05.066.051.07.051.075.052.079.051.084.052.088.052.092.052.097.052.102.052.105.052.11.051.114.051.119.052.123.05.127.051.131.05.135.049.139.049.144.048.147.048.152.047.155.046.16.045.163.045.167.044.171.042.176.042.178.04.183.04.187.038.19.037.194.036.197.034.202.033.204.032.209.03.212.028.216.027.219.025.222.024.226.022.23.02.233.018.236.016.24.014.243.012.246.01.249.008.253.006.256.003.259.001.26-.001.257-.003.254-.006.25-.008.247-.01.244-.012.241-.015.237-.016.233-.018.231-.02.226-.022.224-.024.22-.025.216-.027.212-.029.21-.03.205-.032.202-.033.198-.035.194-.036.191-.037.187-.039.183-.039.179-.041.175-.042.172-.043.168-.044.163-.045.16-.045.155-.047.152-.047.148-.048.143-.048.139-.05.136-.049.131-.05.126-.051.123-.051.118-.051.114-.052.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.051.07-.052.065-.051.06-.05.056-.051.051-.049.023-.025.023-.024.021-.025.02-.024.019-.024.018-.024.017-.024.015-.023.014-.023.013-.024.012-.022.01-.023.01-.023.008-.022.006-.022.006-.022.004-.021.004-.022.001-.021.001-.021v-4.139l-.077.054-.08.054-.083.054-.085.052-.087.053-.09.051-.093.051-.095.051-.097.05-.1.049-.102.049-.105.048-.106.047-.109.047-.111.046-.114.045-.115.044-.118.044-.12.044-.122.042-.124.042-.126.041-.128.04-.13.039-.132.039-.134.038-.135.037-.138.036-.139.036-.142.035-.143.033-.144.033-.147.033-.148.031-.15.03-.151.03-.153.028-.154.028-.156.027-.158.026-.159.025-.161.024-.162.023-.163.022-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.011-.178.009-.179.009-.179.007-.181.007-.182.005-.182.004-.184.003-.184.002h-.37l-.184-.002-.184-.003-.182-.004-.182-.005-.181-.007-.179-.007-.179-.009-.178-.009-.176-.011-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.022-.162-.023-.161-.024-.159-.025-.157-.026-.156-.027-.155-.028-.153-.028-.151-.03-.15-.03-.148-.031-.146-.033-.145-.033-.143-.033-.141-.035-.14-.036-.137-.036-.136-.037-.134-.038-.132-.039-.13-.039-.128-.04-.126-.041-.124-.042-.122-.043-.12-.043-.117-.044-.116-.044-.113-.046-.112-.046-.109-.046-.106-.047-.105-.048-.102-.049-.1-.049-.097-.05-.095-.051-.093-.051-.09-.051-.087-.053-.085-.052-.083-.054-.08-.054-.077-.054v4.139zm0-5.666v.011l.001.02.003.022.004.021.005.022.006.021.007.022.009.023.01.022.011.023.012.023.013.023.015.023.016.024.017.024.018.023.019.024.021.025.022.024.023.024.024.025.052.05.056.05.061.05.066.051.07.051.075.052.079.051.084.052.088.052.092.052.097.052.102.052.105.051.11.052.114.051.119.051.123.051.127.05.131.05.135.05.139.049.144.048.147.048.152.047.155.046.16.045.163.045.167.043.171.043.176.042.178.04.183.04.187.038.19.037.194.036.197.034.202.033.204.032.209.03.212.028.216.027.219.025.222.024.226.021.23.02.233.018.236.017.24.014.243.012.246.01.249.008.253.006.256.003.259.001.26-.001.257-.003.254-.006.25-.008.247-.01.244-.013.241-.014.237-.016.233-.018.231-.02.226-.022.224-.024.22-.025.216-.027.212-.029.21-.03.205-.032.202-.033.198-.035.194-.036.191-.037.187-.039.183-.039.179-.041.175-.042.172-.043.168-.044.163-.045.16-.045.155-.047.152-.047.148-.048.143-.049.139-.049.136-.049.131-.051.126-.05.123-.051.118-.052.114-.051.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.052.07-.051.065-.051.06-.051.056-.05.051-.049.023-.025.023-.025.021-.024.02-.024.019-.024.018-.024.017-.024.015-.023.014-.024.013-.023.012-.023.01-.022.01-.023.008-.022.006-.022.006-.022.004-.022.004-.021.001-.021.001-.021v-4.153l-.077.054-.08.054-.083.053-.085.053-.087.053-.09.051-.093.051-.095.051-.097.05-.1.049-.102.048-.105.048-.106.048-.109.046-.111.046-.114.046-.115.044-.118.044-.12.043-.122.043-.124.042-.126.041-.128.04-.13.039-.132.039-.134.038-.135.037-.138.036-.139.036-.142.034-.143.034-.144.033-.147.032-.148.032-.15.03-.151.03-.153.028-.154.028-.156.027-.158.026-.159.024-.161.024-.162.023-.163.023-.165.021-.166.02-.167.019-.169.018-.169.017-.171.016-.173.015-.173.014-.175.013-.175.012-.177.01-.178.01-.179.009-.179.007-.181.006-.182.006-.182.004-.184.003-.184.001-.185.001-.185-.001-.184-.001-.184-.003-.182-.004-.182-.006-.181-.006-.179-.007-.179-.009-.178-.01-.176-.01-.176-.012-.175-.013-.173-.014-.172-.015-.171-.016-.17-.017-.169-.018-.167-.019-.166-.02-.165-.021-.163-.023-.162-.023-.161-.024-.159-.024-.157-.026-.156-.027-.155-.028-.153-.028-.151-.03-.15-.03-.148-.032-.146-.032-.145-.033-.143-.034-.141-.034-.14-.036-.137-.036-.136-.037-.134-.038-.132-.039-.13-.039-.128-.041-.126-.041-.124-.041-.122-.043-.12-.043-.117-.044-.116-.044-.113-.046-.112-.046-.109-.046-.106-.048-.105-.048-.102-.048-.1-.05-.097-.049-.095-.051-.093-.051-.09-.052-.087-.052-.085-.053-.083-.053-.08-.054-.077-.054v4.153zm8.74-8.179l-.257.004-.254.005-.25.008-.247.011-.244.012-.241.014-.237.016-.233.018-.231.021-.226.022-.224.023-.22.026-.216.027-.212.028-.21.031-.205.032-.202.033-.198.034-.194.036-.191.038-.187.038-.183.04-.179.041-.175.042-.172.043-.168.043-.163.045-.16.046-.155.046-.152.048-.148.048-.143.048-.139.049-.136.05-.131.05-.126.051-.123.051-.118.051-.114.052-.11.052-.106.052-.101.052-.096.052-.092.052-.088.052-.083.052-.079.052-.074.051-.07.052-.065.051-.06.05-.056.05-.051.05-.023.025-.023.024-.021.024-.02.025-.019.024-.018.024-.017.023-.015.024-.014.023-.013.023-.012.023-.01.023-.01.022-.008.022-.006.023-.006.021-.004.022-.004.021-.001.021-.001.021.001.021.001.021.004.021.004.022.006.021.006.023.008.022.01.022.01.023.012.023.013.023.014.023.015.024.017.023.018.024.019.024.02.025.021.024.023.024.023.025.051.05.056.05.06.05.065.051.07.052.074.051.079.052.083.052.088.052.092.052.096.052.101.052.106.052.11.052.114.052.118.051.123.051.126.051.131.05.136.05.139.049.143.048.148.048.152.048.155.046.16.046.163.045.168.043.172.043.175.042.179.041.183.04.187.038.191.038.194.036.198.034.202.033.205.032.21.031.212.028.216.027.22.026.224.023.226.022.231.021.233.018.237.016.241.014.244.012.247.011.25.008.254.005.257.004.26.001.26-.001.257-.004.254-.005.25-.008.247-.011.244-.012.241-.014.237-.016.233-.018.231-.021.226-.022.224-.023.22-.026.216-.027.212-.028.21-.031.205-.032.202-.033.198-.034.194-.036.191-.038.187-.038.183-.04.179-.041.175-.042.172-.043.168-.043.163-.045.16-.046.155-.046.152-.048.148-.048.143-.048.139-.049.136-.05.131-.05.126-.051.123-.051.118-.051.114-.052.11-.052.106-.052.101-.052.096-.052.092-.052.088-.052.083-.052.079-.052.074-.051.07-.052.065-.051.06-.05.056-.05.051-.05.023-.025.023-.024.021-.024.02-.025.019-.024.018-.024.017-.023.015-.024.014-.023.013-.023.012-.023.01-.023.01-.022.008-.022.006-.023.006-.021.004-.022.004-.021.001-.021.001-.021-.001-.021-.001-.021-.004-.021-.004-.022-.006-.021-.006-.023-.008-.022-.01-.022-.01-.023-.012-.023-.013-.023-.014-.023-.015-.024-.017-.023-.018-.024-.019-.024-.02-.025-.021-.024-.023-.024-.023-.025-.051-.05-.056-.05-.06-.05-.065-.051-.07-.052-.074-.051-.079-.052-.083-.052-.088-.052-.092-.052-.096-.052-.101-.052-.106-.052-.11-.052-.114-.052-.118-.051-.123-.051-.126-.051-.131-.05-.136-.05-.139-.049-.143-.048-.148-.048-.152-.048-.155-.046-.16-.046-.163-.045-.168-.043-.172-.043-.175-.042-.179-.041-.183-.04-.187-.038-.191-.038-.194-.036-.198-.034-.202-.033-.205-.032-.21-.031-.212-.028-.216-.027-.22-.026-.224-.023-.226-.022-.231-.021-.233-.018-.237-.016-.241-.014-.244-.012-.247-.011-.25-.008-.254-.005-.257-.004-.26-.001-.26.001z" transform="scale(.5)"></path></symbol></defs><defs><symbol height="24" width="24" id="clock"><path d="M12 2c5.514 0 10 4.486 10 10s-4.486 10-10 10-10-4.486-10-10 4.486-10 10-10zm0-2c-6.627 0-12 5.373-12 12s5.373 12 12 12 12-5.373 12-12-5.373-12-12-12zm5.848 12.459c.202.038.202.333.001.372-1.907.361-6.045 1.111-6.547 1.111-.719 0-1.301-.582-1.301-1.301 0-.512.77-5.447 1.125-7.445.034-.192.312-.181.343.014l.985 6.238 5.394 1.011z" transform="scale(.5)"></path></symbol></defs><defs><marker orient="auto-start-reverse" markerHeight="12" markerWidth="12" markerUnits="userSpaceOnUse" refY="5" refX="7.9" id="arrowhead"><path d="M -1 0 L 10 5 L 0 10 z"></path></marker></defs><defs><marker refY="4.5" refX="4" orient="auto" markerHeight="8" markerWidth="15" id="crosshead"><path style="stroke-dasharray: 0, 0;" d="M 1,2 L 6,7 M 6,2 L 1,7" stroke-width="1pt" stroke="#000000" fill="none"></path></marker></defs><defs><marker orient="auto" markerHeight="28" markerWidth="20" refY="7" refX="15.5" id="filled-head"><path d="M 18,7 L9,13 L14,7 L9,1 Z"></path></marker></defs><defs><marker orient="auto" markerHeight="40" markerWidth="60" refY="15" refX="15" id="sequencenumber"><circle r="6" cy="15" cx="15"></circle></marker></defs><g><rect class="note" height="40" width="413" stroke="#666" fill="#EDF2AE" y="75" x="56.5"></rect><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="noteText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="80" x="263"><tspan x="263">Dynamic Registration (Local)</tspan></text></g> <g><rect class="note" height="40" width="413" stroke="#666" fill="#EDF2AE" y="245" x="56.5"></rect><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="noteText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="250" x="263"><tspan x="263">Authorization with PKCE &amp; Callback Forwarding</tspan></text></g> <g><rect class="note" height="59" width="277" stroke="#666" fill="#EDF2AE" y="385" x="306"></rect><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="noteText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="390" x="445"><tspan x="445">Store transaction with client PKCE</tspan></text> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="noteText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="410" x="445"><tspan x="445">Generate proxy PKCE pair</tspan></text></g> <g><rect class="note" height="40" width="416" stroke="#666" fill="#EDF2AE" y="544" x="419.5"></rect><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="noteText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="549" x="628"><tspan x="628">Provider Callback</tspan></text></g> <g><rect class="note" height="40" width="413" stroke="#666" fill="#EDF2AE" y="784" x="56.5"></rect><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="noteText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="789" x="263"><tspan x="263">Client Callback Forwarding</tspan></text></g> <g><rect class="note" height="40" width="413" stroke="#666" fill="#EDF2AE" y="904" x="56.5"></rect><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="noteText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="909" x="263"><tspan x="263">Token Exchange</tspan></text></g> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="130" x="262">1. POST /register</text> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="150" x="262">redirect_uri: localhost:54321/callback</text> <line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="185" x2="440.5" y1="185" x1="82.5"></line><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="200" x="265">2. Returns fixed upstream credentials</text> <line style="stroke-dasharray: 3, 3; fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine1" y2="235" x2="85.5" y1="235" x1="443.5"></line><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="300" x="262">3. GET /authorize</text> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="320" x="262">redirect_uri=localhost:54321/callback</text> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="339" x="262">code_challenge=CLIENT_CHALLENGE</text> <line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="375" x2="440.5" y1="375" x1="82.5"></line><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="459" x="626">4. Redirect to provider</text> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="479" x="626">redirect_uri=server:8000/auth/callback</text> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="498" x="626">code_challenge=PROXY_CHALLENGE</text> <line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="534" x2="806.5" y1="534" x1="445.5"></line><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="599" x="629">5. GET /auth/callback</text> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="619" x="629">with authorization code</text> <line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="654" x2="448.5" y1="654" x1="809.5"></line><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="669" x="626">6. Exchange code for tokens</text> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="689" x="626">code_verifier=PROXY_VERIFIER</text> <line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="724" x2="806.5" y1="724" x1="445.5"></line><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="739" x="629">7. Access &amp; refresh tokens</text> <line style="stroke-dasharray: 3, 3; fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine1" y2="774" x2="448.5" y1="774" x1="809.5"></line><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="839" x="265">8. Redirect to localhost:54321/callback</text> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="859" x="265">with new authorization code</text> <line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="894" x2="85.5" y1="894" x1="443.5"></line><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="959" x="262">9. POST /token with code</text> <text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="979" x="262">code_verifier=CLIENT_VERIFIER</text> <line style="fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine0" y2="1014" x2="440.5" y1="1014" x1="82.5"></line><text style="font-family: inherit; font-size: 16px; font-weight: 400;" dy="1em" class="messageText" alignment-baseline="middle" dominant-baseline="middle" text-anchor="middle" y="1029" x="265">10. Returns stored provider tokens</text> <line style="stroke-dasharray: 3, 3; fill: none;" marker-end="url(#arrowhead)" stroke="none" stroke-width="2" class="messageLine1" y2="1064" x2="85.5" y1="1064" x1="443.5"></line></svg> The flow diagram above illustrates the complete OAuth Proxy pattern. Let’s understand each phase:

### Registration Phase

When an MCP client calls `/register` with its dynamic callback URL, the proxy responds with your pre-configured upstream credentials. The client stores these credentials believing it has registered a new app. Meanwhile, the proxy records the client’s callback URL for later use.

### Authorization Phase

The client initiates OAuth by redirecting to the proxy’s `/authorize` endpoint. The proxy:
1. Stores the client’s transaction with its PKCE challenge
2. Generates its own PKCE parameters for upstream security
3. Redirects to the upstream provider using the fixed callback URL
This dual-PKCE approach maintains end-to-end security at both the client-to-proxy and proxy-to-provider layers.

### Callback Phase

After user authorization, the provider redirects back to the proxy’s fixed callback URL. The proxy:
1. Exchanges the authorization code for tokens with the provider
2. Stores these tokens temporarily
3. Generates a new authorization code for the client
4. Redirects to the client’s original dynamic callback URL

### Token Exchange Phase

Finally, the client exchanges its authorization code with the proxy to receive the provider’s tokens. The proxy validates the client’s PKCE verifier before returning the stored tokens.This entire flow is transparent to the MCP client—it experiences a standard OAuth flow with dynamic registration, unaware that a proxy is managing the complexity behind the scenes.

### PKCE Forwarding

OAuth Proxy automatically handles PKCE (Proof Key for Code Exchange) when working with providers that support or require it. The proxy generates its own PKCE parameters to send upstream while separately validating the client’s PKCE, ensuring end-to-end security at both layers.This is enabled by default via the `forward_pkce` parameter and works seamlessly with providers like Google, Azure AD, and GitHub. Only disable it for legacy providers that don’t support PKCE:

```
# Disable PKCE forwarding only if upstream doesn't support it

auth = OAuthProxy(

    ...,

    forward_pkce=False  # Default is True

)
```

### Redirect URI Validation

While OAuth Proxy accepts all redirect URIs by default (for DCR compatibility), you can restrict which clients can connect by specifying allowed patterns:

```
# Allow only localhost clients (common for development)

auth = OAuthProxy(

    # ... other parameters ...

    allowed_client_redirect_uris=[

        "http://localhost:*",

        "http://127.0.0.1:*"

    ]

)

# Allow specific known clients

auth = OAuthProxy(

    # ... other parameters ...

    allowed_client_redirect_uris=[

        "http://localhost:*",

        "https://claude.ai/api/mcp/auth_callback",

        "https://*.mycompany.com/auth/*"  # Wildcard patterns supported

    ]

)
```

Check your server logs for “Client registered with redirect\_uri” messages to identify what URLs your clients use.

## Token Verification

OAuth Proxy requires a compatible `TokenVerifier` to validate tokens from your provider. Different providers use different token formats:
- **JWT tokens** (Google, Azure): Use `JWTVerifier` with the provider’s JWKS endpoint
- **Opaque tokens** (GitHub, Discord): Use provider-specific verifiers or implement custom validation
See the [Token Verification guide](https://gofastmcp.com/servers/auth/token-verification) for detailed setup instructions for your provider.

## Environment Configuration

`` New in version: `2.12.1` `` For production deployments, configure OAuth Proxy through environment variables instead of hardcoding credentials:

```
# Specify the provider implementation

export FASTMCP_SERVER_AUTH=fastmcp.server.auth.providers.github.GitHubProvider

# Provider-specific credentials

export FASTMCP_SERVER_AUTH_GITHUB_CLIENT_ID="Ov23li..."

export FASTMCP_SERVER_AUTH_GITHUB_CLIENT_SECRET="abc123..."

export FASTMCP_SERVER_AUTH_GITHUB_BASE_URL="https://your-production-server.com"
```

With environment configuration, your server code simplifies to:

```
from fastmcp import FastMCP

# Authentication automatically configured from environment

mcp = FastMCP(name="My Server")

@mcp.tool

def protected_tool(data: str) -> str:

    """This tool is now protected by OAuth."""

    return f"Processed: {data}"

if __name__ == "__main__":

    mcp.run(transport="http", port=8000)
```