# Tradução PT-BR | Ghost of a Tale - Instalador Automático

-----

## 📥 Guia de Download

Escolha a plataforma de sua preferência para baixar:

### Opção 1: Nexus Mods (Recomendado)

A maneira mais comum para jogadores de PC.

1.  Acesse a página do mod no Nexus: **[Link para o seu Mod no Nexus]**.
2.  Vá até a aba **Files**.
3.  Clique em **Manual Download** no arquivo "Tradução PT-BR - Instalador".
4.  Execute o arquivo baixado.

### Opção 2: GitHub Releases

Download direto do repositório.

1.  Vá até a aba **[link suspeito removido]** aqui ao lado.
2.  Baixe o arquivo **`Instalador_GhostOfATale_PTBR.exe`**.

-----

### 🔎 Opção 3: Para Desenvolvedores (Código Fonte)

Se você tem receio de executáveis ou quer ver como a mágica acontece:

1.  Clone este repositório.
2.  Certifique-se de ter Python instalado.
3.  Instale o Tkinter (`pip install tk` - geralmente já vem com o Python).
4.  Execute o script `instalador.py` (o arquivo `patch_traducao.json` deve estar na mesma pasta).

-----

### 📋 Como Instalar

1. Execute o arquivo **Instalador.exe** (ou o nome que você deu ao executável).
2. O Windows pode pedir permissão de Administrador. Clique em **Sim** (necessário para modificar a pasta do jogo).
3. No instalador, clique no botão **"Procurar..."**.
4. Navegue até a pasta onde o jogo está instalado.
   * *Geralmente: `Steam\steamapps\common\Ghost of a Tale\Ghost of a Tale_Data`*
5. Selecione o arquivo **`resources.assets`** e clique em Abrir.
6. Clique no botão roxo **"INSTALAR TRADUÇÃO"**.
7. Aguarde a barra de progresso chegar a 100% e a mensagem de Sucesso.

Pronto! O jogo está traduzido.

### ⚠️ Importante: Alerta de Antivírus / SmartScreen

Como este é um software criado por fã e não possui uma "Assinatura Digital" (que é paga e cara), o Windows ou seu navegador podem bloquear o download acusando ser suspeito. **Isso é um falso positivo.**

  * **No Windows (Tela Azul "O Windows protegeu o computador"):** Clique em **"Mais informações"** e depois no botão **"Executar assim mesmo"**.
  * **No Navegador:** Se bloquear, escolha a opção "Manter arquivo" ou "Permitir".

Todo o código fonte está disponível neste repositório para quem quiser auditar a segurança da ferramenta.


## 🛠️ Bastidores e Detalhes Técnicos

### 📅 A História

Este projeto nasceu de uma necessidade pessoal. Ao decidir jogar *Ghost of a Tale*, percebi que não havia suporte oficial para Português e nenhuma tradução da comunidade disponível.
Decidi aceitar o desafio e realizei este projeto em um único **fim de semana**. O objetivo era tornar o jogo acessível para mim e, consequentemente, para outros jogadores brasileiros.

### 💻 Como foi feito (A Engenharia)

Sou **programador**, não tradutor. Por isso, abordei a tradução como um problema de engenharia de software:

1.  **Análise:** Inicialmente utilizei o **UABEA** (Unity Asset Bundle Extractor Avalon) para entender a estrutura dos arquivos `.assets` do jogo.
2.  **Ferramenta Própria:** Para agilizar o processo, desenvolvi uma **ferramenta em Python do zero**. Este software foi capaz de interpretar os arquivos binários da Unity, permitindo:
      * Exportar todos os textos do jogo para arquivos JSON estruturados.
      * Reimportar os textos traduzidos para dentro do arquivo binário original.
3.  **O Patch:** O instalador que você baixou **não contém nenhum arquivo original do jogo**. Ele carrega apenas um "Patch" (um arquivo JSON com as diferenças binárias). Isso garante que não haja distribuição ilegal de propriedade intelectual. O instalador aplica essas diferenças matematicamente sobre o seu arquivo original.

### 🤖 Sobre a Tradução (Disclaimer)

Como mencionado, minha especialidade é código. Para o texto, utilizei um fluxo de tradução assistida por Inteligência Artificial:

  * **Ferramentas:** ChatGPT, Gemini e Google Tradutor.
  * **Revisão:** A revisão foi feita dentro do tempo limitado do fim de semana.
  * **Expectativa:** Você pode encontrar inconsistências de contexto ou termos literais. O foco foi a compreensão geral da história e das mecânicas.

*Aproveite o jogo\!*

-----

### 🛡️ Segurança e Backup

Não se preocupe em perder os arquivos originais.
O instalador cria **automaticamente** um backup antes de fazer qualquer alteração.

* Uma pasta chamada `backup resources` será criada dentro da pasta de dados do jogo.
* O arquivo original (`resources.assets`) intacto estará lá dentro.

### ↩️ Como Desinstalar (Restaurar Original)

Se quiser remover a tradução e voltar para o inglês:

1. Vá até a pasta do jogo (`Ghost of a Tale_Data`).
2. Abra a pasta `backup resources`.
3. Copie o arquivo `resources.assets` que está lá dentro.
4. Volte uma pasta e cole, substituindo o arquivo modificado.

---

### ⚠️ Notas Importantes

* Este patch foi feito para a versão PC (Steam/GOG).
* Se o jogo atualizar, a tradução pode parar de funcionar. Basta usar a opção de "Verificar integridade dos arquivos" na Steam e reinstalar a tradução se houver uma versão compatível.

**Créditos:**
* Tradução e Ferramenta por: Matheus Araújo