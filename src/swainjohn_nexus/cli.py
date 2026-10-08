import argparse
import json

from swainjohn_nexus.socket_server import run_server_once


def main() -> int:
    parser = argparse.ArgumentParser(description="SWAINJOHN Nexus runtime")
    parser.add_argument("--host", default="0.0.0.0")
    parser.add_argument("--port", type=int, default=8443)
    parser.add_argument("--timeout", type=float, default=2.0)
    args = parser.parse_args()

    result = run_server_once(host=args.host, port=args.port, timeout=args.timeout)
    print(json.dumps(result, indent=2, sort_keys=True))

    if result.get("status") == "ok":
        return 0
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
