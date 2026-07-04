import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { SSEClientTransport } from '@modelcontextprotocol/sdk/client/sse.js';

async function main() {
  console.log('Conectando ao MCP Server via SSE...');
  const transport = new SSEClientTransport(new URL('http://localhost:3000/mcp/sse'));
  
  const client = new Client(
    { name: 'test-client', version: '1.0.0' },
    { capabilities: {} }
  );
  
  await client.connect(transport);
  console.log('✅ Conectado com sucesso!');

  console.log('\n--- Solicitando lista de ferramentas ---');
  const response = await client.listTools();
  console.log(`Recebidas ${response.tools.length} ferramentas:\n`);
  
  for (const tool of response.tools) {
    console.log(`- ${tool.name}: ${tool.description.substring(0, 80)}...`);
  }

  console.log('\n--- Chamando ferramenta "create_post_draft" ---');
  const result = await client.callTool({
    name: 'create_post_draft',
    arguments: {
      template_id: 'artigo',
      fields: {
        category: 'DIREITO & TECNOLOGIA',
        title: 'O Futuro da Inteligência Artificial no Sistema Judiciário',
        meta: 'Publicado em 04/07/2026 · 10 min de leitura',
        tags: '#LegalTech #IA #InovaçãoJurídica',
        cta: 'Ler artigo completo →'
      },
      photo_url: 'http://localhost:3000/assets/lex/conectado.png'
    }
  });
  
  console.log('Resultado:');
  const jsonResult = JSON.parse(result.content[0].text);
  console.log(JSON.stringify(jsonResult, null, 2));

  console.log('\n✅ Design Gerado! Para ver a arte no Editor Pro, acesse:');
  console.log(jsonResult.editorUrl);

  console.log('\nFechando conexão...');
  process.exit(0);
}

main().catch(err => {
  console.error('ERRO:', err);
  process.exit(1);
});
