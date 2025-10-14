// src/api/scans.ts
import api from "./client";

export type StartResp = { scan_id: string; status: "queued"|"running"|"done"|"failed" };
export type StatusResp = { scan_id: string; status: "queued"|"running"|"done"|"failed" };

export async function startScan(target_url: string){
  const r = await api.post<StartResp>("/scans", { target_url });
  return r.data;
}

export async function getScanStatus(scanId: string){
  const r = await api.get<StatusResp>(`/scans/${scanId}/status`);
  return r.data;
}

export async function getScanReport(scanId: string){
  const r = await api.get(`/scans/${scanId}/report`);
  return r.data;
}
