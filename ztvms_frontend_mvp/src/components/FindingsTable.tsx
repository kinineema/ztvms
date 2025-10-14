import React from "react";
import { Paper, Table, TableHead, TableRow, TableCell, TableBody, Chip, Link } from "@mui/material";

type Finding = {
  tool?: string;
  name?: string;
  risk?: string;
  url?: string;
  param?: string | null;
  evidence?: string | null;
};

function riskColor(risk?: string) {
  switch ((risk || "").toLowerCase()) {
    case "high": return "error";
    case "medium": return "warning";
    case "low": return "info";
    default: return "default";
  }
}

export default function FindingsTable({ findings }: { findings: Finding[] }) {
  if (!findings || findings.length === 0) return null;

  return (
    <Paper sx={{ mt: 2, overflow: "auto" }}>
      <Table size="small">
        <TableHead>
          <TableRow>
            <TableCell>Tool</TableCell>
            <TableCell>Name</TableCell>
            <TableCell>Risk</TableCell>
            <TableCell>URL</TableCell>
            <TableCell>Param</TableCell>
            <TableCell>Evidence</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {findings.map((f, i) => (
            <TableRow key={i}>
              <TableCell>{f.tool || "-"}</TableCell>
              <TableCell>{f.name || "-"}</TableCell>
              <TableCell>
                <Chip label={f.risk || "-"} color={riskColor(f.risk) as any} size="small" />
              </TableCell>
              <TableCell>
                {f.url ? (
                  <Link
                    href={f.url.startsWith("http") ? f.url : `https://${f.url}`}
                    target="_blank"
                    rel="noopener noreferrer"
                    underline="always"
                    onClick={(e) => e.stopPropagation()}
                    sx={{ wordBreak: "break-all", cursor: "pointer" }}
                  >
                    {f.url}
                  </Link>
                ) : (
                  "-"
                )}
              </TableCell>
              <TableCell>{f.param || "-"}</TableCell>
              <TableCell
                sx={{ maxWidth: 320, whiteSpace: "nowrap", overflow: "hidden", textOverflow: "ellipsis" }}
              >
                {f.evidence || "-"}
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Paper>
  );
}
