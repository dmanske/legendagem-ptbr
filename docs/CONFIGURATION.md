# Configuração

## Agente de tradução

O Codex executa a tradução editorial usando o contexto completo da obra. Não é
necessário configurar outra chave de IA dentro desta skill.

## ElevenLabs Scribe v2

A transcrição principal usa o modelo `scribe_v2` com timestamps por palavra.
Crie uma chave com acesso a Speech to Text e mantenha-a fora do repositório.

### macOS com zsh

Para evitar que a chave fique no histórico do terminal:

```bash
read -s "ELEVENLABS_API_KEY?Cole a chave da ElevenLabs: "; echo
export ELEVENLABS_API_KEY
```

### Linux com bash

```bash
read -rsp "Cole a chave da ElevenLabs: " ELEVENLABS_API_KEY; echo
export ELEVENLABS_API_KEY
```

### Windows PowerShell

```powershell
$env:ELEVENLABS_API_KEY = Read-Host "Cole a chave da ElevenLabs"
```

Para armazenamento permanente, prefira o cofre de credenciais do sistema ou o
gerenciador seguro usado pelo seu ambiente. Arquivos de perfil armazenam o valor
como texto e exigem cuidado.

## Verificar sem revelar a chave

```bash
python3 ~/.codex/skills/legendagem-ptbr/scripts/doctor.py
```

O diagnóstico informa apenas `CONFIGURADA` ou `SEM CHAVE`.

## Falhas da ElevenLabs

A skill não deve trocar silenciosamente para outro transcritor. Se a credencial
estiver ausente, expirada ou sem permissão, ou se o serviço falhar, o agente deve
parar e informar o problema. O transcritor local incluído no pacote só deve ser
usado quando o usuário o escolher explicitamente.

## Segurança

- Nunca coloque credenciais em `.env.example`.
- Nunca faça commit de `.env`.
- Nunca cole a chave em conversas, issues ou capturas de tela.
- Revogue imediatamente qualquer chave exposta.
- Restrinja a chave ao recurso Speech to Text quando possível.
