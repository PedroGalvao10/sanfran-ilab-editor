import { exec } from 'child_process';

const server = exec('node api/server.js', { env: { ...process.env, PORT: 3006 } });
server.stdout.on('data', data => console.log(`[API]: ${data}`));
server.stderr.on('data', data => console.error(`[API ERRO]: ${data}`));

setTimeout(async () => {
  try {
    const res = await fetch('http://127.0.0.1:3006/brand/assets');
    const json = await res.json();
    console.log('✅ Catálogo de Assets recuperado!');
    console.log(`- Encontrados ${Object.keys(json).length} categorias.`);
    console.log('- Exemplo de categorias:', Object.keys(json).slice(0, 5).join(', '));
    if (json.foxes) {
      console.log('- Exemplo de Asset em "foxes":', json.foxes[0]);
    }
  } catch (err) {
    console.error('❌ Erro no teste:', err.message);
  } finally {
    server.kill();
    process.exit(0);
  }
}, 2000);
