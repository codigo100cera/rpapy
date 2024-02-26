*** Settings ***
Documentation    Documentação da Suite de Tasks Robot Framework

Library     ../resources/custom_keywords.py
Resource    ../resources/keywords.robot

Suite Setup     Toast Process Start Notifier
  
*** Variables ***
${VAR}=             Everybody
${LAPIS}=           btn_lapis
${NOME_IMAGEM}      robotframework


*** Tasks ***
Tarefa principal
    Keyword principal


*** Keywords ***
Keyword principal
    Primeira Keyword        ${VAR}
    Abrir Mspaint
    Reduzir zoom
    Definir tamanho da imagem    2700   1100
    Selecionar ferramenta "${LAPIS}"
    Desenhar            ${NOME_IMAGEM}
    ${DADOS_CORES}      Get Dados Cores     ${NOME_IMAGEM}
    Pintar desenho      ${DADOS_CORES}