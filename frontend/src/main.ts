import './app.css'
import App from './App.svelte'
import Login from './Login.svelte'

// const app = new App({
//   target: document.getElementById('app')!,
// })

const login = new Login({
  target: document.getElementById('app')!,
})

export default login