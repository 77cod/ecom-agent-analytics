
import '@ant-design/v5-patch-for-react-19'
import 'normalize.css'
import { createRoot } from 'react-dom/client'
import './antd.scss'
import App from './App.tsx'
import './index.css'

// 注册 ECharts 中文语言包
import('echarts/i18n/langZH').then(({ default: zh }) => {
  import('echarts').then((echarts) => {
    echarts.registerLocale('ZH', zh)
  })
}).catch(() => {
  // 低版本兼容，静默忽略
})

createRoot(document.getElementById('root')!).render(<App />)
