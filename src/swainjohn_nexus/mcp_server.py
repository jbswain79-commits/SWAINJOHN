import argparse
import json
from typing import Any

try:
    from mcp.server.fastmcp import FastMCP
except ImportError:  # pragma: no cover
    FastMCP = None

from swainjohn_nexus.core import generate_security_report, parse_soggy011_header


def _parse_hex_packet(packet_hex: str) -> dict[str, Any]:
    try:
        packet_bytes = bytes.fromhex(packet_hex)
    except ValueError:
        return {"status": "error", "reason": "invalid_hex"}

    parsed = parse_soggy011_header(packet_bytes)
    if parsed is False:
        return {"status": "rejected", "reason": "invalid_packet"}

    return {"status": "ok", "packet": parsed}


def build_mcp_server() -> Any:
    if FastMCP is None:
        raise RuntimeError(
            "The 'mcp' package is not installed. Install it with: pip install mcp"
        )

    server = FastMCP("swainjohn-nexus")

    @server.tool()
    def parse_packet_header(packet_hex: str) -> dict[str, Any]:
        """Validate and decode a SWAINJOHN SOGGY-011 packet from a hex string."""
        return _parse_hex_packet(packet_hex)

    @server.tool()
    def evaluate_spatial_drift(measured_area: float, baseline_area: float = 100.0) -> dict[str, Any]:
        """Return a local spatial-drift compliance report using the project baseline."""
        return generate_security_report(measured_area, baseline_area)

    @server.tool()
    def describe_project() -> dict[str, Any]:
        """Return a summary of the prototype project purpose and limits."""
        return {
            "name": "SWAINJOHN",
            "category": "experimental-government-tech-prototype",
            "focus": [
                "local data staging",
                "spatial schema design",
                "packet validation",
                "AI workflow evaluation",
            ],
            "status": "prototype",
            "scope": "illustrative-not-production",
        }

    return server


def main() -> int:
    parser = argparse.ArgumentParser(description="SWAINJOHN MCP server skeleton")
    parser.add_argument(
        "--transport",
        choices=["stdio", "streamable-http"],
        default="stdio",
        help="Transport for the MCP server",
    )
    parser.add_argument("--host", default="127.0.0.1", help="Host for HTTP transport")
    parser.add_argument("--port", type=int, default=8000, help="Port for HTTP transport")
    args = parser.parse_args()

    if FastMCP is None:
        print(
            json.dumps(
                {
                    "status": "not_ready",
                    "reason": "mcp package missing",
                    "install_hint": "pip install mcp",
                },
                indent=2,
                sort_keys=True,
            )
        )
        return 1

    server = build_mcp_server()

    if args.transport == "stdio":
        server.run(transport="stdio")
    else:
        server.run(transport="streamable-http", host=args.host, port=args.port)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
