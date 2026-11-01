#!/usr/bin/env python3
"""Generate an image through the local CLIProxyAPI OpenAI-compatible endpoint.

Usage: gen.py OUT.png "prompt" [--size WxH] [--transparent] [--ref ref1.png ...] [--model M]
"""
import argparse, base64, json, os, sys, time, urllib.request, uuid

KEY = os.environ.get("IMAGE_API_KEY", "")
BASE = os.environ.get("IMAGE_API_BASE", "http://127.0.0.1:8317/v1").rstrip("/")


def post_json(url, payload):
    req = urllib.request.Request(url, data=json.dumps(payload).encode(),
                                 headers={"Authorization": f"Bearer {KEY}", "Content-Type": "application/json"})
    return json.load(urllib.request.urlopen(req, timeout=600))


def post_multipart(url, fields, files):
    boundary = uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, path in files:
        data = open(path, "rb").read()
        body += (f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{os.path.basename(path)}\"\r\n"
                 f"Content-Type: image/png\r\n\r\n").encode() + data + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(url, data=body, headers={"Authorization": f"Bearer {KEY}",
                                                          "Content-Type": f"multipart/form-data; boundary={boundary}"})
    return json.load(urllib.request.urlopen(req, timeout=600))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("prompt")
    ap.add_argument("--size", default="1536x1024")
    ap.add_argument("--transparent", action="store_true")
    ap.add_argument("--ref", nargs="*", default=[])
    ap.add_argument("--model", default="gpt-image-2.5")
    ap.add_argument("--tries", type=int, default=3)
    a = ap.parse_args()
    if not KEY:
        ap.error("Set IMAGE_API_KEY for your image service.")
    fields = {"model": a.model, "prompt": a.prompt, "size": a.size, "n": 1, "quality": "high"}
    if a.transparent:
        fields["background"] = "transparent"
        fields["output_format"] = "png"
    last = None
    for attempt in range(a.tries):
        try:
            if a.ref:
                d = post_multipart(BASE + "/images/edits", {k: str(v) for k, v in fields.items()},
                                   [("image[]", r) for r in a.ref])
            else:
                d = post_json(BASE + "/images/generations", fields)
            b = d["data"][0]["b64_json"]
            os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
            open(a.out, "wb").write(base64.b64decode(b))
            print("OK", a.out)
            return
        except urllib.error.HTTPError as e:
            last = f"HTTP {e.code}: {e.read()[:500]!r}"
        except Exception as e:  # noqa
            last = repr(e)
        print("retry", attempt, last, file=sys.stderr)
        time.sleep(3)
    print("FAIL", a.out, last)
    sys.exit(1)


if __name__ == "__main__":
    main()
