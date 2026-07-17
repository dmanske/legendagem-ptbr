# Configuração de IA e ElevenLabs

## IA

Uma IA ativa é necessária para revisar a transcrição, traduzir o sentido da música e aplicar as regras editoriais. No Codex, a autenticação da IA é administrada pelo próprio produto; não é necessário colocar uma chave de IA dentro desta skill.

Em uma automação independente, use um provedor compatível com Chat Completions e configure `AI_BASE_URL`, `AI_API_KEY` e `AI_MODEL` fora do Git. Essas variáveis são reservadas para a automação que consumir a skill; os scripts deste repositório não enviam tradução diretamente a um provedor.

## ElevenLabs

Crie uma chave da ElevenLabs com permissão Speech to Text. A skill usa o modelo `scribe_v2` e solicita timestamps por palavra.

### macOS ou Linux — sessão atual

```bash
export ELEVENLABS_API_KEY="sua-chave"
```

### Windows PowerShell — sessão atual

```powershell
$env:ELEVENLABS_API_KEY = "sua-chave"
```

Para armazenamento permanente, prefira o cofre de credenciais do sistema ou o gerenciador seguro usado pela sua automação. Variáveis persistentes em arquivos de perfil ficam armazenadas como texto e exigem cuidado.

## Testar sem revelar a chave

```bash
python3 skill/tradutor-de-clipes/scripts/doctor.py
```

O diagnóstico informa apenas se a variável existe. Ele nunca imprime o valor.

## Segurança

- Nunca coloque chaves em `.env.example`.
- Nunca faça commit de `.env`.
- Nunca cole chaves em conversas, issues ou capturas de tela.
- Revogue imediatamente uma chave exposta.
- Restrinja a chave ElevenLabs ao recurso Speech to Text quando possível.
