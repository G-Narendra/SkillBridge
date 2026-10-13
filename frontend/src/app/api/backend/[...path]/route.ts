import { NextRequest, NextResponse } from "next/server";

// Universal reverse proxy to backend FastAPI service.
// Eliminates browser CORS issues and connects directly to the production backend.
const OFFICIAL_RENDER_BACKEND = "https://skillbridge-backend-1pm3.onrender.com";

const getTargetBackend = () => {
  const envUrl = process.env.BACKEND_API_URL || process.env.NEXT_PUBLIC_API_URL;
  if (!envUrl || envUrl.includes("skillbridge-backend.onrender.com")) {
    return OFFICIAL_RENDER_BACKEND;
  }
  return envUrl.replace(/\/$/, "");
};

const TARGET_BACKEND = getTargetBackend();

async function proxyRequest(request: Request, { params }: { params: { path: string[] } }) {
  const rawPath = params.path ? params.path.join("/") : "";
  const cleanPath = rawPath.replace(/^api\/?/, "");
  const url = new URL(request.url);
  const targetUrl = cleanPath
    ? `${TARGET_BACKEND}/api/${cleanPath}${url.search}`
    : `${TARGET_BACKEND}/api/health${url.search}`;

  const forwardHeaders = new Headers();
  request.headers.forEach((value, key) => {
    // Avoid forwarding host and connection headers
    if (!["host", "connection", "transfer-encoding"].includes(key.toLowerCase())) {
      forwardHeaders.set(key, value);
    }
  });

  try {
    let body: any = null;
    if (request.method !== "GET" && request.method !== "HEAD") {
      body = await request.arrayBuffer();
    }

    const backendResponse = await fetch(targetUrl, {
      method: request.method,
      headers: forwardHeaders,
      body: body,
      cache: "no-store",
    });

    const responseHeaders = new Headers();
    backendResponse.headers.forEach((value, key) => {
      if (!["content-encoding", "transfer-encoding"].includes(key.toLowerCase())) {
        responseHeaders.set(key, value);
      }
    });

    responseHeaders.set("Access-Control-Allow-Origin", "*");
    responseHeaders.set("Access-Control-Allow-Methods", "GET, POST, PUT, DELETE, OPTIONS");
    responseHeaders.set("Access-Control-Allow-Headers", "*");

    const responseBody = await backendResponse.arrayBuffer();

    return new Response(responseBody, {
      status: backendResponse.status,
      statusText: backendResponse.statusText,
      headers: responseHeaders,
    });
  } catch (error: any) {
    return new Response(
      JSON.stringify({
        detail: `Proxy error reaching backend at ${targetUrl}: ${error.message || "Connection refused"}`
      }),
      {
        status: 502,
        headers: {
          "Content-Type": "application/json",
          "Access-Control-Allow-Origin": "*"
        }
      }
    );
  }
}

export const GET = proxyRequest;
export const POST = proxyRequest;
export const PUT = proxyRequest;
export const DELETE = proxyRequest;

export async function OPTIONS() {
  return new Response(null, {
    status: 204,
    headers: {
      "Access-Control-Allow-Origin": "*",
      "Access-Control-Allow-Methods": "GET, POST, PUT, DELETE, OPTIONS",
      "Access-Control-Allow-Headers": "*",
    },
  });
}
