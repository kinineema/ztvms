import React from 'react'
import { AppBar, Toolbar, Typography, Container, Box, Button } from '@mui/material'
import { useAuth } from '../features/auth/AuthContext'

export default function AppShell({children}:{children: React.ReactNode}){
  const { user, logout } = useAuth()
  return (<>
    <AppBar position="static">
      <Toolbar sx={{ display: 'flex', gap: 2 }}>
        <Typography variant="h6" sx={{ flexGrow: 1 }}>SecScan MVP</Typography>
        {user && (
          <Box display="flex" alignItems="center" gap={2}>
            <Typography variant="body2">{user.email} — <strong>{user.role}</strong></Typography>
            <Button color="inherit" onClick={logout}>Logout</Button>
          </Box>
        )}
      </Toolbar>
    </AppBar>
    <Container sx={{mt:4, mb:6}}>{children}</Container>
  </>)
}
