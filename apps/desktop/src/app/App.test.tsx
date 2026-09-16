import { describe, it, expect } from 'vitest'
import { render, screen } from '@testing-library/react'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { App } from './App'

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      retry: false,
    },
  },
})

function renderWithProviders(ui: React.ReactElement) {
  return render(
    <QueryClientProvider client={queryClient}>
      {ui}
    </QueryClientProvider>
  )
}

describe('App', () => {
  it('deve renderizar o título da aplicação', () => {
    renderWithProviders(<App />)
    expect(screen.getByRole('heading', { name: /dashboard acadêmico/i })).toBeInTheDocument()
  })

  it('deve exibir skip link para acessibilidade', () => {
    renderWithProviders(<App />)
    const skipLink = screen.getByText(/pular para o conteúdo principal/i)
    expect(skipLink).toHaveAttribute('href', '#main-content')
    expect(skipLink).toHaveClass('skip-link')
  })
})
