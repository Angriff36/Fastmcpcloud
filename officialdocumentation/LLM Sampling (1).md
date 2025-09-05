---
title: "LLM Sampling"
source: "https://gofastmcp.com/clients/sampling"
author:
  - "[[FastMCP]]"
published:
created: 2025-09-04
description: "Handle server-initiated LLM sampling requests."
tags:
  - "clippings"
---
`` New in version: `2.0.0` `` MCP servers can request LLM completions from clients. The client handles these requests through a sampling handler callback.

## Sampling Handler

Provide a `sampling_handler` function when creating the client:

```
from fastmcp import Client

from fastmcp.client.sampling import (

    SamplingMessage,

    SamplingParams,

    RequestContext,

)

async def sampling_handler(

    messages: list[SamplingMessage],

    params: SamplingParams,

    context: RequestContext

) -> str:

    # Your LLM integration logic here

    # Extract text from messages and generate a response

    return "Generated response based on the messages"

client = Client(

    "my_mcp_server.py",

    sampling_handler=sampling_handler,

)
```

### Handler Parameters

The sampling handler receives three parameters:

## Sampling Handler ParametersSamplingMessage

Sampling Message Object

Showattributesrole

Literal\["user", "assistant"\]

The role of the message.content

TextContent | ImageContent | AudioContent

The content of the message.TextContent is most common, and has a `.text` attribute.SamplingParams

Sampling Parameters Object

Showattributesmessages

list\[SamplingMessage\]

The messages to sample frommodelPreferences

ModelPreferences | None

The server’s preferences for which model to select. The client MAY ignore these preferences.

Showattributeshints

list\[ModelHint\] | None

The hints to use for model selection.costPriority

float | None

The cost priority for model selection.speedPriority

float | None

The speed priority for model selection.intelligencePriority

float | None

The intelligence priority for model selection.systemPrompt

str | None

An optional system prompt the server wants to use for sampling.includeContext

IncludeContext | None

A request to include context from one or more MCP servers (including the caller), to be attached to the prompt.temperature

float | None

The sampling temperature.maxTokens

int

The maximum number of tokens to sample.stopSequences

list\[str\] | None

The stop sequences to use for sampling.

Optional metadata to pass through to the LLM provider.RequestContext

Request Context Object

Showattributesrequest\_id

RequestId

Unique identifier for the MCP request

## Basic Example

```
from fastmcp import Client

from fastmcp.client.sampling import SamplingMessage, SamplingParams, RequestContext

async def basic_sampling_handler(

    messages: list[SamplingMessage],

    params: SamplingParams,

    context: RequestContext

) -> str:

    # Extract message content

    conversation = []

    for message in messages:

        content = message.content.text if hasattr(message.content, 'text') else str(message.content)

        conversation.append(f"{message.role}: {content}")

    # Use the system prompt if provided

    system_prompt = params.systemPrompt or "You are a helpful assistant."

    # Here you would integrate with your preferred LLM service

    # This is just a placeholder response

    return f"Response based on conversation: {' | '.join(conversation)}"

client = Client(

    "my_mcp_server.py",

    sampling_handler=basic_sampling_handler

)
```

## Sampling fallback

Client support for sampling is optional, if the client does not support sampling, the server will report an error indicating that the client does not support sampling.A `sampling_handler` can also be provided to the FastMCP server, which will be used to handle sampling requests if the client does not support sampling. This sampling handler bypasses the client and sends sampling requests directly to the LLM provider.Sampling handlers can be implemented using any LLM provider but a sample implementation for OpenAI is provided as a Contrib module. Sampling lacks the full capabilities of typical LLM completions. For this reason, the OpenAI sampling handler, pointed at a third-party provider’s OpenAI-compatible API, is often sufficient to implement a sampling handler.

```
import asyncio

import os

from mcp.types import ContentBlock

from openai import OpenAI

from fastmcp import FastMCP

from fastmcp.experimental.sampling.handlers.openai import OpenAISamplingHandler

from fastmcp.server.context import Context

async def async_main():

    server = FastMCP(

        name="OpenAI Sampling Fallback Example",

        sampling_handler=OpenAISamplingHandler(

            default_model="gpt-4o-mini",

            client=OpenAI(

                api_key=os.getenv("API_KEY"),

                base_url=os.getenv("BASE_URL"),

            ),

        ),

    )

    @server.tool

    async def test_sample_fallback(ctx: Context) -> ContentBlock:

        return await ctx.sample(

            messages=["hello world!"],

        )

    await server.run_http_async()

if __name__ == "__main__":

    asyncio.run(async_main())
```