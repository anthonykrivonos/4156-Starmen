import React from 'react'
import ReactDOM from 'react-dom'
import App from './pages/App'
import reportWebVitals from './reportWebVitals'
import './index.module.sass'

ReactDOM.render(
	<React.StrictMode>
		<App />
	</React.StrictMode>,
	document.getElementById('root')
)

reportWebVitals(console.log)
