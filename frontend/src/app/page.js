export default function Home() {
  return (
    <main className="flex min-h-screen flex-col items-center justify-center p-24">
      <div className="z-10 max-w-5xl w-full items-center justify-center font-mono text-sm">
        <div className="text-center">
          <h1 className="text-6xl font-bold mb-4 bg-gradient-to-r from-blue-600 to-purple-600 bg-clip-text text-transparent">
            Firewall Log Monitor
          </h1>
          <p className="text-xl text-gray-600 dark:text-gray-300 mb-8">
            방화벽 로그 모니터링 웹 어드민
          </p>
          <div className="flex gap-4 justify-center">
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
              <h2 className="text-2xl font-semibold mb-2">Backend API</h2>
              <p className="text-gray-600 dark:text-gray-400">
                <a
                  href="http://localhost:8000/docs"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="text-blue-500 hover:underline"
                >
                  http://localhost:8000/docs
                </a>
              </p>
            </div>
            <div className="p-6 bg-white dark:bg-gray-800 rounded-lg shadow-lg">
              <h2 className="text-2xl font-semibold mb-2">Frontend</h2>
              <p className="text-gray-600 dark:text-gray-400">
                <span className="text-blue-500">http://localhost:3000</span>
              </p>
            </div>
          </div>
          <div className="mt-8 text-sm text-gray-500 dark:text-gray-400">
            <p>Feature 1.1 & 1.2 구현 완료</p>
            <p>프로젝트 환경 설정 및 데이터베이스 스키마 설계</p>
          </div>
        </div>
      </div>
    </main>
  )
}
