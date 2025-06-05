import { StrictMode } from 'react'
import { createRoot } from 'react-dom/client'
import { BrowserRouter, Routes, Route } from 'react-router'
import './index.css'
import Index from '@/components/Index.tsx'
import LangInput from './components/LangInput'
import DBInput from './components/DBInput'
import CloudInput from './components/CloudInput'
import WebInput from './components/WebInput'
import EmbeddedInput from './components/EmbeddedInput'
import DevopsInput from './components/DevopsInput'
import MiscInput from './components/MiscInput'
import ProfTech from './components/ProfTech'

createRoot(document.getElementById('root')!).render(
  <StrictMode>
    <BrowserRouter>
      <Routes>
        <Route path ="/" element ={<Index />} />
        <Route path ="/lang" element = {<LangInput />} />
        <Route path ="/db-skills" element = {<DBInput />} />
        <Route path ="/cloud-skills" element = {<CloudInput />} />
        <Route path ="/web-skills" element = {<WebInput />} />
        <Route path ="/embedded-skills" element = {<EmbeddedInput />} />
        <Route path ="/devops-skills" element = {<DevopsInput />} />
        <Route path ="/misc-skills" element = {<MiscInput />} />
        <Route path ="/prof" element = {<ProfTech />} />
      </Routes>
    </BrowserRouter>
  </StrictMode>,
)
