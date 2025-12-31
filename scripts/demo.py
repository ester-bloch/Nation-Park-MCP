#!/usr/bin/env python3
"""Minimal MCP stdio client demo.

This script is intentionally dependency-free: it speaks MCP over stdio using
the common JSON-RPC framing (Content-Length headers), similar to LSP.

It is designed as a *demo fallback* when Claude Desktop is unavailable.

Usage:
  python scripts/demo.py

Environment:
  NPS_API_KEY (optional) - if missing, API-backed tools will return a
  structured error response, which is still useful for demoing the protocol.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
import time
from dataclasses import dataclass
from typing import Any, Dict, Optional, Tuple


@dataclass
class MCPProcess:
    proc: subprocess.Popen

    def close(self) -> None:
        try:
            if self.proc.poll() is None:
                self.proc.terminate()
                self.proc.wait(timeout=5)
        except Exception:
            try:
                self.proc.kill()
            except Exception:
                pass


def _encode_message(payload: Dict[str, Any]) -> bytes:
    body = json.dumps(payload, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    header = f"Content-Length: {len(body)}\r\n\r\n".encode("ascii")
    return header + body


def _read_exact(stream, n: int) -> bytes:
    buf = b""
    while len(buf) < n:
        chunk = stream.read(n - len(buf))
        if not chunk:
            raise EOFError("MCP server closed the stream")
        buf += chunk
    return buf


def _read_message(stream, timeout_s: float = 10.0) -> Dict[str, Any]:
    """Read one MCP JSON-RPC message framed with Content-Length headers."""
    start = time.time()
    # Read headers line-by-line until an empty line.
    headers: Dict[str, str] = {}
    line = b""
    while True:
        if time.time() - start > timeout_s:
            raise TimeoutError("Timed out waiting for MCP response headers")
        line = stream.readline()
        if not line:
            raise EOFError("MCP server closed the stream")
        line_str = line.decode("ascii", errors="replace").strip()
        if not line_str:
            break
        if ":" in line_str:
            k, v = line_str.split(":", 1)
            headers[k.strip().lower()] = v.strip()

    if "content-length" not in headers:
        raise ValueError(f"Missing Content-Length header. Headers: {headers}")

    length = int(headers["content-length"])
    body = _read_exact(stream, length)
    return json.loads(body.decode("utf-8"))


def _send(proc: subprocess.Popen, payload: Dict[str, Any]) -> None:
    assert proc.stdin is not None
    proc.stdin.write(_encode_message(payload))
    proc.stdin.flush()


def _request(
    proc: subprocess.Popen,
    *,
    req_id: int,
    method: str,
    params: Optional[Dict[str, Any]] = None,
    timeout_s: float = 10.0,
) -> Dict[str, Any]:
    _send(
        proc,
        {
            "jsonrpc": "2.0",
            "id": req_id,
            "method": method,
            "params": params or {},
        },
    )
    assert proc.stdout is not None
    return _read_message(proc.stdout, timeout_s=timeout_s)


def _notify(proc: subprocess.Popen, *, method: str, params: Optional[Dict[str, Any]] = None) -> None:
    _send(
        proc,
        {
            "jsonrpc": "2.0",
            "method": method,
            "params": params or {},
        },
    )


def _spawn_server() -> MCPProcess:
    """Spawn the MCP server as a subprocess."""
    env = os.environ.copy()
    # Ensure unbuffered I/O for reliable stdio framing.
    env.setdefault("PYTHONUNBUFFERED", "1")

    cmd = [sys.executable, "-m", "src.main"]
    proc = subprocess.Popen(
        cmd,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=sys.stderr,  # keep server logs visible during demo
        env=env,
        cwd=os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
        bufsize=0,
    )
    return MCPProcess(proc=proc)


def _pretty(obj: Any) -> str:
    return json.dumps(obj, indent=2, ensure_ascii=False, sort_keys=True)


def main() -> int:
    mcp = _spawn_server()
    try:
        proc = mcp.proc

        # 1) Initialize
        init = _request(
            proc,
            req_id=1,
            method="initialize",
            params={
                "protocolVersion": "2024-11-05",
                "clientInfo": {"name": "demo-client", "version": "0.1.0"},
                "capabilities": {},
            },
            timeout_s=15.0,
        )
        print("\n=== initialize ===")
        print(_pretty(init))

        # 2) Initialized notification (some servers expect it)
        _notify(proc, method="notifications/initialized")

        # 3) List tools
        tools = _request(proc, req_id=2, method="tools/list", params={}, timeout_s=15.0)
        print("\n=== tools/list ===")
        print(_pretty(tools))

        # 4) Call a representative tool
        # Prefer findParks if present, otherwise call the first tool.
        tool_name = "findParks"
        tool_list = tools.get("result", {}).get("tools", []) if isinstance(tools, dict) else []
        if tool_list and all(t.get("name") != tool_name for t in tool_list if isinstance(t, dict)):
            first = tool_list[0]
            if isinstance(first, dict) and "name" in first:
                tool_name = str(first["name"])

        call_params = {
            "name": tool_name,
            "arguments": {"stateCode": "CA", "limit": 1},
        }
        call = _request(proc, req_id=3, method="tools/call", params=call_params, timeout_s=30.0)
        print("\n=== tools/call ===")
        print(f"Tool: {tool_name}")
        print(_pretty(call))

        return 0
    except Exception as e:
        print(f"\nDemo failed: {e}", file=sys.stderr)
        return 1
    finally:
        mcp.close()


if __name__ == "__main__":
    raise SystemExit(main())
