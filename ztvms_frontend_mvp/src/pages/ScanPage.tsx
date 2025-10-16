import React, { useState } from 'react'
import { Box, Button, Paper, TextField, Typography, CircularProgress, Alert } from '@mui/material'
import { startScan, getScanStatus, getScanReport } from '../api/scans'
import { useInterval } from '../hooks/useInterval'
import FindingsTable from "../components/FindingsTable";

const StatusChip: React.FC<{ status: string }> = ({ status }) => {
  const s = status?.toLowerCase();
  const styles: Record<string, React.CSSProperties> = {
    queued:  { background: '#e2e8f0', color: '#0f172a' },
    running: { background: '#fde68a', color: '#7c2d12' },
    done:    { background: '#bbf7d0', color: '#065f46' },
    failed:  { background: '#fecaca', color: '#7f1d1d' },
  };
  const label = s ? s[0].toUpperCase() + s.slice(1) : 'Queued';
  return (
    <span style={{ padding: '4px 10px', borderRadius: 999, fontWeight: 600, ...styles[s || 'queued'] }}>
      {label}
    </span>
  );
};

export default function ScanPage(){
  const [url, setUrl] = useState('')
  const [scanId, setScanId] = useState('')
  const [status, setStatus] = useState('')
  const [busy, setBusy] = useState(false)
  const [report, setReport] = useState<any | null>(null)
  const [error, setError] = useState<string | null>(null)

  const onStart = async () => {
    setError(null)
    setReport(null)
    if(!url) { setError('Please enter a target URL'); return }
    setBusy(true)
    try{
      const res = await startScan(url)
      setScanId(res.scan_id)
      setStatus(res.status)
    }catch(e:any){
      setError(e?.response?.data?.detail || 'Failed to start scan')
    }finally{
      setBusy(false)
    }
  }

  useInterval(()=>{
    if(!scanId) return
    if(status === 'queued' || status === 'running'){
      getScanStatus(scanId).then(r => setStatus(r.status)).catch(()=>{})
    }
  }, scanId ? 1000 : null)

  const onViewFindings = async () => {
    if(!scanId) return
    try{
      const r = await getScanReport(scanId)
      setReport(r)
    }catch(e:any){
      setError(e?.response?.data?.detail || 'Report not ready yet')
    }
  }

  return (
    <Paper sx={{p:3}}>
      <Typography variant="h6" gutterBottom>Start New Scan</Typography>
      <Box display="flex" gap={2} alignItems="center">
        <TextField label="Target URL" placeholder="https://example.com" fullWidth value={url} onChange={e=>setUrl(e.target.value)} />
        <Button variant="contained" onClick={onStart} disabled={busy}>
          {busy ? <CircularProgress size={22}/> : 'Start'}
        </Button>
      </Box>

      {error && <Box mt={2}><Alert severity="error">{error}</Alert></Box>}

      {scanId && (
        <Box mt={2}>
          <Typography><strong>Scan ID:</strong> {scanId}</Typography>
          <Typography>
  <strong>Status:</strong> <StatusChip status={status} />
</Typography>
          <Button sx={{mt:1}} variant="outlined" onClick={onViewFindings}>View Findings</Button>
        </Box>
      )}

      {report && (
  <Box mt={3}>
    <Typography variant="h6">Findings</Typography>
    <FindingsTable findings={Array.isArray(report.findings) ? report.findings : []} />
  </Box>
)}

    </Paper>
  )
}
