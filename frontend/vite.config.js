import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import { VitePWA } from 'vite-plugin-pwa';
export default defineConfig({plugins:[react(),VitePWA({registerType:'autoUpdate',manifest:{name:'Crawler Research Lab',short_name:'Crawler Lab',start_url:'/',display:'standalone',background_color:'#101827',theme_color:'#101827',icons:[{src:'/icon.svg',sizes:'any',type:'image/svg+xml',purpose:'any maskable'}]}})],server:{proxy:{'/api':'http://localhost:8000'}}});
