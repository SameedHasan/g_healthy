import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import './index.css'
import App from './App.jsx'
import { FrappeProvider } from 'frappe-react-sdk'

createRoot(document.getElementById('root')).render(
  <FrappeProvider swrConfig={{
    revalidateOnFocus: false,
    shouldRetryOnError: false,
    suspense: false,
  }}
  siteName={"ghealthy"}
  enableSocket={true}
  socketPort={9003}>
      <App />
  </FrappeProvider>,
)
