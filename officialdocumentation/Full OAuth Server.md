---
title: "Full OAuth Server"
source: "https://gofastmcp.com/servers/auth/full-oauth-server"
author:
  - "[[Authorization Flow]]"
  - "[[​]]"
published:
created: 2025-09-04
description: "Build a self-contained authentication system where your FastMCP server manages users, issues tokens, and validates them."
tags:
  - "clippings"
---
`` New in version: `2.11.0` ``

**This is an extremely advanced pattern that most users should avoid.** Building a secure OAuth 2.1 server requires deep expertise in authentication protocols, cryptography, and security best practices. The complexity extends far beyond initial implementation to include ongoing security monitoring, threat response, and compliance maintenance.**Use [Remote OAuth](https://gofastmcp.com/servers/auth/remote-oauth) instead** unless you have compelling requirements that external identity providers cannot meet, such as air-gapped environments or specialized compliance needs.

The Full OAuth Server pattern exists to support the MCP protocol specification’s requirements. Your FastMCP server becomes both an Authorization Server and Resource Server, handling the complete authentication lifecycle from user login to token validation.This documentation exists for completeness - the vast majority of applications should use external identity providers instead.

## OAuthProvider

FastMCP provides the `OAuthProvider` abstract class that implements the OAuth 2.1 specification. To use this pattern, you must subclass `OAuthProvider` and implement all required abstract methods.

`OAuthProvider` handles OAuth endpoints, protocol flows, and security requirements, but delegates all storage, user management, and business logic to your implementation of the abstract methods.

## Required Implementation

You must implement these abstract methods to create a functioning OAuth server:

### Client Management

## Client Management Methodsget\_client

async method

Retrieve client information by ID from your database.

ShowParametersclient\_id

str

Client identifier to look up

ShowReturnsOAuthClientInformationFull | None

return type

Client information object or `None` if client not found

### Authorization Flow

## Authorization Flow Methods

authorize

async method

Handle authorization request and return redirect URL. Must implement user authentication and consent collection.

ShowParametersclient

OAuthClientInformationFull

OAuth client making the authorization requestparams

AuthorizationParams

Authorization request parameters from the client

ShowReturnsstr

return type

Redirect URL to send the client to

load\_authorization\_code

async method

Load authorization code from storage by code string. Return `None` if code is invalid or expired.

ShowParametersclient

OAuthClientInformationFull

OAuth client attempting to use the authorization code

authorization\_code

str

Authorization code string to look up

ShowReturns

AuthorizationCode | None

return type

Authorization code object or `None` if not found

### Token Management

## Token Management Methods

exchange\_authorization\_code

async method

Exchange authorization code for access and refresh tokens. Must validate code and create new tokens.

ShowParametersclient

OAuthClientInformationFull

OAuth client exchanging the authorization code

authorization\_code

AuthorizationCode

Valid authorization code object to exchange

ShowReturnsOAuthToken

return type

New OAuth token containing access and refresh tokensload\_refresh\_token

async method

Load refresh token from storage by token string. Return `None` if token is invalid or expired.

ShowParametersclient

OAuthClientInformationFull

OAuth client attempting to use the refresh tokenrefresh\_token

str

Refresh token string to look up

ShowReturnsRefreshToken | None

return type

Refresh token object or `None` if not foundexchange\_refresh\_token

async method

Exchange refresh token for new access/refresh token pair. Must validate scopes and token.

ShowParametersclient

OAuthClientInformationFull

OAuth client using the refresh tokenrefresh\_token

RefreshToken

Valid refresh token object to exchangescopes

list\[str\]

Requested scopes for the new access token

ShowReturnsOAuthToken

return type

New OAuth token with updated access and refresh tokensload\_access\_token

async method

Load an access token by its token string.

ShowParameterstoken

str

The access token to verify

ShowReturnsAccessToken | None

return type

The access token object, or `None` if the token is invalidrevoke\_token

async method

Revoke access or refresh token, marking it as invalid in storage.

ShowParameterstoken

AccessToken | RefreshToken

Token object to revoke and mark invalid

ShowReturnsNone

return type

No return valueverify\_token

async method

Verify bearer token for incoming requests. Return `AccessToken` if valid, `None` if invalid.

ShowParameterstoken

str

Bearer token string from incoming request

ShowReturnsAccessToken | None

return type

Access token object if valid, `None` if invalid or expired

Each method must handle storage, validation, security, and error cases according to the OAuth 2.1 specification. The implementation complexity is substantial and requires expertise in OAuth security considerations.

**Security Notice:** OAuth server implementation involves numerous security considerations including PKCE, state parameters, redirect URI validation, token binding, replay attack prevention, and secure storage requirements. Mistakes can lead to serious security vulnerabilities.