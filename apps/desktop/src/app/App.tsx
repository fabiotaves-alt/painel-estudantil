import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { useState } from 'react'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      staleTime: 1000 * 60 * 5, // 5 minutos
      retry: 1,
      refetchOnWindowFocus: false,
    },
  },
})

export function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <a href="#main-content" className="skip-link">
        Pular para o conteúdo principal
      </a>
      <main id="main-content" tabIndex={-1}>
        <h1>Dashboard Acadêmico</h1>
        <p>Status do backend: <span data-testid="backend-status">Verificando...</span></p>
      </main>
    </QueryClientProvider>
  )
}
