# SWAINJOHN MCP Server Skeleton

This document describes the initial MCP-compatible server layer for SWAINJOHN.

## Purpose

The goal is to provide a minimal registry-style skeleton that exposes a small set of operational tools without claiming production-grade MCP readiness. This is intentionally a prototype layer built on top of the existing SWAINJOHN runtime logic.

## Current status

This repository is not yet a full registry-ready MCP server. It is a foundation for that work.

Current capabilities in the skeleton:
- parse and validate SOGGY-011 packet headers
- assess spatial drift compliance
- expose a small tool surface suitable for future MCP client wiring

## Package entrypoint

The skeleton is available from:
- `src/swainjohn_nexus/mcp_server.py`

You can run it with:

```bash
python -m swainjohn_nexus.mcp_server --transport stdio
```

## Install

```bash
pip install -e .
```

If MCP support is enabled through the `mcp` package, the server can be exposed via the standard client-facing runtime. If the dependency is not installed yet, the server exits with an installation hint rather than pretending to be fully operational.

## Why this matters

This server skeleton helps demonstrate how the existing SWAINJOHN logic can be surfaced in a machine-readable, tool-oriented interface for evaluation, automation, and eventual interoperability with AI agents.

## Future tasks for registry readiness

- formal tool schema definitions
- proper package metadata and versioning
- client-validation against an MCP runtime
- security and trust boundaries review
- packaging cleanup for public registry use
