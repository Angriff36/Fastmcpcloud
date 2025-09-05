# AuthKit 🤝 FastMCP

> Secure your FastMCP server with AuthKit by WorkOS

export const VersionBadge = ({version}) => {
  return <code className="version-badge-container">
            <p className="version-badge">
                <span className="version-badge-label">New in version:</span> 
                <code className="version-badge-version">{version}</code>
            </p>
        </code>;
};

<VersionBadge version="2.11.0" />

This guide shows you how to secure your FastMCP server using WorkOS's **AuthKit**, a complete authentication and user management solution. This integration uses the [**Remote OAuth**](/servers/auth/remote-oauth) pattern, where AuthKit handles user login and your FastMCP server validates the tokens.

## Configuration

### Prerequisites

Before you begin, you will need:

1. A **[WorkOS Account](https://workos.com/)** and a new **Project**.
2. An **[AuthKit](https://www.authkit.com/)** instance configured within your WorkOS project.
3. Your FastMCP server's URL (can be localhost for development, e.g., `http://localhost:8000`).

### Step 1: AuthKit Configuration

In your WorkOS Dashboard, enable AuthKit and configure the following settings:

<Steps>
  <Step title="Enable Dynamic Client Registration">
    Go to **Applications → Configuration** and enable **Dynamic Client Registration**. This allows MCP clients register with your application automatically.

        <img src="https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/integrations/images/authkit/enable_dcr.png?fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=5849352618ef89da08cf452c5dcf38a8" alt="Enable Dynamic Client Registration" width="2644" height="1588" data-path="integrations/images/authkit/enable_dcr.png" srcset="https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/integrations/images/authkit/enable_dcr.png?w=280&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=afe3af1599ffac48411edaa7eb8ee35e 280w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/integrations/images/authkit/enable_dcr.png?w=560&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=fa6e286fd2e98a984dbed9dd30375e07 560w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/integrations/images/authkit/enable_dcr.png?w=840&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=26ba396eef845948a2bbe7405716a419 840w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/integrations/images/authkit/enable_dcr.png?w=1100&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=5270b0b09891741087494f2819be6f19 1100w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/integrations/images/authkit/enable_dcr.png?w=1650&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=604955d22d5556d3464f5b4919664c41 1650w, https://mintcdn.com/fastmcp/hUosZw7ujHZFemrG/integrations/images/authkit/enable_dcr.png?w=2500&fit=max&auto=format&n=hUosZw7ujHZFemrG&q=85&s=a4e1627dd14ee7c1c2ad6b6628dc8520 2500w" data-optimize="true" data-opv="2" />
  </Step>

  <Step title="Note Your AuthKit Domain">
    Find your **AuthKit Domain** on the configuration page. It will look like `https://your-project-12345.authkit.app`. You'll need this for your FastMCP server configuration.
  </Step>
</Steps>

### Step 2: FastMCP Configuration

Create your FastMCP server file and use the `AuthKitProvider` to handle all the OAuth integration automatically:

```python server.py
from fastmcp import FastMCP
from fastmcp.server.auth.providers.workos import AuthKitProvider

# The AuthKitProvider automatically discovers WorkOS endpoints
# and configures JWT token validation
auth_provider = AuthKitProvider(
    authkit_domain="https://your-project-12345.authkit.app",
    base_url="http://localhost:8000"  # Use your actual server URL
)

mcp = FastMCP(name="AuthKit Secured App", auth=auth_provider)
```

## Testing

To test your server, you can use the `fastmcp` CLI to run it locally. Assuming you've saved the above code to `server.py` (after replacing the `authkit_domain` and `base_url` with your actual values!), you can run the following command:

```bash
fastmcp run server.py --transport http --port 8000
```

Now, you can use a FastMCP client to test that you can reach your server after authenticating:

```python
from fastmcp import Client
import asyncio

async def main():
    async with Client("http://localhost:8000/mcp/", auth="oauth") as client:
        assert await client.ping()

if __name__ == "__main__":
    asyncio.run(main())
```

## Environment Variables

<VersionBadge version="2.12.1" />

For production deployments, use environment variables instead of hardcoding credentials.

### Provider Selection

Setting this environment variable allows the AuthKit provider to be used automatically without explicitly instantiating it in code.

<Card>
  <ParamField path="FASTMCP_SERVER_AUTH" default="Not set">
    Set to `fastmcp.server.auth.providers.workos.AuthKitProvider` to use AuthKit authentication.
  </ParamField>
</Card>

### AuthKit-Specific Configuration

These environment variables provide default values for the AuthKit provider, whether it's instantiated manually or configured via `FASTMCP_SERVER_AUTH`.

<Card>
  <ParamField path="FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN" required>
    Your AuthKit domain (e.g., `https://your-project-12345.authkit.app`)
  </ParamField>

  <ParamField path="FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_BASE_URL" required>
    Public URL of your FastMCP server (e.g., `https://your-server.com` or `http://localhost:8000` for development)
  </ParamField>

  <ParamField path="FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_REQUIRED_SCOPES" default="[]">
    Comma-, space-, or JSON-separated list of required OAuth scopes (e.g., `openid profile email` or `["openid", "profile", "email"]`)
  </ParamField>
</Card>

Example `.env` file:

```bash
# Use the AuthKit provider
FASTMCP_SERVER_AUTH=fastmcp.server.auth.providers.workos.AuthKitProvider

# AuthKit configuration
FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_AUTHKIT_DOMAIN=https://your-project-12345.authkit.app
FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_BASE_URL=https://your-server.com
FASTMCP_SERVER_AUTH_AUTHKITPROVIDER_REQUIRED_SCOPES=openid,profile,email
```

With environment variables set, your server code simplifies to:

```python server.py
from fastmcp import FastMCP

# Authentication is automatically configured from environment
mcp = FastMCP(name="AuthKit Secured App")
```
