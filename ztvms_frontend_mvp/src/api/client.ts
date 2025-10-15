import axios from "axios";

export const auth = { getToken: () => localStorage.getItem("token") || "" };

const api = axios.create({
  baseURL: "http://127.0.0.1:8000",   // FastAPI URL
  timeout: 20000,
});

api.interceptors.request.use((config) => {
  const t = auth.getToken();
  if (t) {
    config.headers = config.headers ?? {};
    config.headers.Authorization = `Bearer ${t}`;
  }
  return config;
});

export default api;