import { createTheme } from "@mui/material/styles";
import { grey, indigo, cyan, red, amber, lightGreen } from "@mui/material/colors";

export const theme = createTheme({
  palette: {
    mode: "dark",
    primary: { main: indigo[400] },
    secondary: { main: cyan[400] },
    background: {
      default: "#0B0F1A",   // page bg
      paper:   "#111827",   // card/table bg
    },
    text: {
      primary:  "#E5E7EB",
      secondary:"#9CA3AF",
    },
    error:   { main: red[400] },
    warning: { main: amber[400] },
    info:    { main: cyan[300] },
    success: { main: lightGreen[400] },
    divider: "rgba(255,255,255,0.08)",
  },
  shape: { borderRadius: 12 },
  typography: {
    fontFamily: `'Inter', system-ui, -apple-system, Segoe UI, Roboto, Arial, sans-serif`,
    h5: { fontWeight: 600 },
    button: { textTransform: "none", fontWeight: 600 },
    body2: { color: "#A3A7B0" },
  },
  components: {
    MuiCssBaseline: {
      styleOverrides: {
        "html, body, #root": { height: "100%" },
        body: {
          backgroundColor: "#0B0F1A",
          backgroundImage: "none",
        },
        "*::-webkit-scrollbar": { height: 10, width: 10 },
        "*::-webkit-scrollbar-thumb": {
          backgroundColor: "rgba(255,255,255,0.15)", borderRadius: 8,
        },
      },
    },
    MuiPaper: {
      defaultProps: { elevation: 0 },
      styleOverrides: {
        root: {
          backgroundImage: "none",
          border: "1px solid rgba(255,255,255,0.08)",
        },
      },
    },
    MuiAppBar: {
      styleOverrides: {
        root: {
          background: "rgba(17,24,39,0.7)",
          backdropFilter: "saturate(120%) blur(6px)",
          borderBottom: "1px solid rgba(255,255,255,0.08)",
        },
      },
    },
    MuiButton: {
      styleOverrides: {
        root: { borderRadius: 10, paddingInline: 14 },
      },
    },
    MuiTableCell: {
      styleOverrides: {
        root: { borderColor: "rgba(255,255,255,0.06)" },
        head: { color: "#CBD5E1", fontWeight: 600 },
      },
    },
    MuiChip: {
      styleOverrides: {
        root: { fontWeight: 600 },
      },
    },
    MuiLink: {
      styleOverrides: {
        root: { color: cyan[300] },
      },
    },
    MuiTextField: {
      styleOverrides: {
        root: { backgroundColor: "rgba(255,255,255,0.03)", borderRadius: 10 },
      },
    },
    MuiCard: {
      styleOverrides: {
        root: {
          backgroundImage: "none",
          border: "1px solid rgba(255,255,255,0.08)",
        },
      },
    },
  },
});
