import { io } from "socket.io-client";

// extend window object
declare global {
  interface Window {
    site_name: string;
    socketio_port?: number;
  }
}

// Get socketio_port from window (set by Frappe at runtime) or use default
const getSocketioPort = () => window.socketio_port || 9000;

export function initSocket() {
  let host = window.location.hostname;
  let siteName = window.site_name || host;
  let port = window.location.port ? `:${getSocketioPort()}` : "";
  let protocol = port ? "http" : "https";
  let url = `${protocol}://${host}${port}/${siteName}`;

  const socket = io(url, {
    withCredentials: true,
    reconnectionAttempts: 5,
  });

  return socket;
}

export const socket = initSocket();
