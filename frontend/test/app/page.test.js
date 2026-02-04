import { render, screen } from '@testing-library/react'
import Home from '@/app/page'

describe('Home Page', () => {
  test('should render page title', () => {
    render(<Home />)

    const heading = screen.getByRole('heading', { name: /Firewall Log Monitor/i })
    expect(heading).toBeInTheDocument()
  })

  test('should render subtitle', () => {
    render(<Home />)

    const subtitle = screen.getByText(/방화벽 로그 모니터링 웹 어드민/i)
    expect(subtitle).toBeInTheDocument()
  })

  test('should render Backend API section', () => {
    render(<Home />)

    const backendHeading = screen.getByRole('heading', { name: /Backend API/i })
    expect(backendHeading).toBeInTheDocument()

    const apiLink = screen.getByRole('link', { name: /http:\/\/localhost:8000\/docs/i })
    expect(apiLink).toBeInTheDocument()
    expect(apiLink).toHaveAttribute('href', 'http://localhost:8000/docs')
    expect(apiLink).toHaveAttribute('target', '_blank')
    expect(apiLink).toHaveAttribute('rel', 'noopener noreferrer')
  })

  test('should render Frontend section', () => {
    render(<Home />)

    const frontendHeading = screen.getByRole('heading', { name: /Frontend/i })
    expect(frontendHeading).toBeInTheDocument()

    const frontendUrl = screen.getByText(/http:\/\/localhost:3000/i)
    expect(frontendUrl).toBeInTheDocument()
  })

  test('should render feature completion status', () => {
    render(<Home />)

    const featureStatus1 = screen.getByText(/Feature 1.1 & 1.2 구현 완료/i)
    expect(featureStatus1).toBeInTheDocument()

    const featureStatus2 = screen.getByText(/프로젝트 환경 설정 및 데이터베이스 스키마 설계/i)
    expect(featureStatus2).toBeInTheDocument()
  })

  test('should have proper styling classes', () => {
    const { container } = render(<Home />)

    const main = container.querySelector('main')
    expect(main).toHaveClass('flex', 'min-h-screen', 'flex-col', 'items-center', 'justify-center', 'p-24')
  })

  test('should render two information cards', () => {
    render(<Home />)

    const backendCard = screen.getByRole('heading', { name: /Backend API/i }).closest('div')
    const frontendCard = screen.getByRole('heading', { name: /Frontend/i }).closest('div')

    expect(backendCard).toBeInTheDocument()
    expect(frontendCard).toBeInTheDocument()
  })
})
