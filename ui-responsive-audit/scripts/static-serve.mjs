import { createReadStream, statSync } from "node:fs";
import { createServer } from "node:http";
import path from "node:path";

const root = path.resolve(process.env.ROOT || "out");
const rootWithSep = `${root}${path.sep}`;
const port = Number(process.env.PORT || 3100);

const types = {
  ".css": "text/css; charset=utf-8",
  ".html": "text/html; charset=utf-8",
  ".js": "text/javascript; charset=utf-8",
  ".json": "application/json; charset=utf-8",
  ".gif": "image/gif",
  ".jpeg": "image/jpeg",
  ".jpg": "image/jpeg",
  ".mp4": "video/mp4",
  ".png": "image/png",
  ".svg": "image/svg+xml",
  ".txt": "text/plain; charset=utf-8",
  ".webm": "video/webm",
  ".webp": "image/webp",
  ".woff": "font/woff",
  ".woff2": "font/woff2",
  ".xml": "application/xml; charset=utf-8",
  ".wasm": "application/wasm",
};

function isHiddenSegment(segment) {
  return segment.startsWith(".") && segment !== "." && segment !== "..";
}

function resolveRequest(urlPath) {
  let pathname = "/";
  try {
    pathname = decodeURIComponent((urlPath || "/").split("?")[0].split("#")[0]);
  } catch {
    return null;
  }

  if (pathname.includes("\0")) return null;

  const normalized = path.posix.normalize(pathname.replace(/\\/g, "/")).replace(/^\/+/, "");
  if (normalized.startsWith("..") || normalized.includes("/../") || normalized.includes("../")) return null;

  const segments = normalized ? normalized.split("/").filter(Boolean) : [];
  if (segments.some((segment) => isHiddenSegment(segment))) return null;

  const candidate = path.resolve(root, normalized);
  if (!candidate.startsWith(rootWithSep) && candidate !== root) return null;

  for (const file of [candidate, path.join(candidate, "index.html"), `${candidate}.html`]) {
    try {
      const stat = statSync(file);
      if (stat.isFile()) return file;
    } catch {}
  }

  return null;
}

createServer((request, response) => {
  const file = resolveRequest(request.url);
  if (!file) {
    response.writeHead(404, { "content-type": "text/plain; charset=utf-8" });
    response.end("Not found");
    return;
  }

  const extension = path.extname(file);
  response.writeHead(file.endsWith("404.html") ? 404 : 200, {
    "cache-control": "no-store",
    "content-type": types[extension] || "application/octet-stream",
  });
  const stream = createReadStream(file);
  stream.on("error", () => {
    if (!response.headersSent) {
      response.writeHead(500, { "content-type": "text/plain; charset=utf-8" });
    }
    response.end("Read error");
  });
  response.on("error", () => stream.destroy());
  response.on("close", () => stream.destroy());
  stream.pipe(response);
}).listen(port, () => {
  console.log(`Serving ${root} at http://localhost:${port}`);
});
