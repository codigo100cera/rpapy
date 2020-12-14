*** Settings ***
Documentation    Documentacao das Keywords da Suite de Tasks
Library     rpapy.core.activities


*** Variables ***
${VAR}=         variables
${LIMPAR}=      {HOME}{DEL 20}
${BALDE}=       btn_balde



*** Keywords ***
Primeira Keyword
    [Arguments]         ${arg}
    Log To Console      Hello ${arg}!


Abrir Mspaint
    Open Executable     mspaint.exe     Sem Título - Paint      work_dir=C:/Windows/System32/


Editar Cor RGB
    [Arguments]     ${r}    ${g}    ${b}    ${matiz}=0   ${sat}=0    ${lum}=

    Click Vision    btn_editar_cores    backend=uia

    Wait Element Vision    titulo_editar_cores

    Write Text Vision    campo_red    backend=uia
    ...    text=${LIMPAR}${r}      move_x=30

    Write Text Vision    campo_green    backend=uia
    ...    text=${LIMPAR}${g}      move_x=30

    Write Text Vision    campo_blue    backend=uia
    ...    text=${LIMPAR}${b}      move_x=30

    Write Text Vision    campo_matiz      backend=uia
    ...    text=${LIMPAR}${matiz}    move_x=30

    Write Text Vision    campo_sat      backend=uia
    ...    text=${LIMPAR}${sat}    move_x=30

    Write Text Vision    campo_lum    backend=uia
    ...    text=${LIMPAR}${lum}    move_x=30

    Click Vision    btn_ok_cor_definida    backend=uia


Reduzir zoom
    Wait Element Vision    icone_paint
    Click Vision    btn_reduzir_zoom    backend=uia     after=0.5


Aumentar zoom
    Wait Element Vision    icone_paint
    Click Vision    btn_aumentar_zoom    backend=uia     after=0.5


Definir tamanho da imagem
    [Arguments]    ${largura}    ${altura}

    Wait Element Vision    icone_paint    

    Click Vision    btn_menu_arquivo    backend=uia
    
    Click Vision    btn_item_menu_propriedades    backend=uia

    Write Text Vision    campo_largura_imagem    backend=uia
    ...    text=${LIMPAR}${largura}    move_x=40
    
    Write Text Vision    campo_altura_imagem    backend=uia
    ...    text=${LIMPAR}${altura}    move_x=40
    
    Click Vision    btn_ok_propriedades_imagem    backend=uia    after=0.5


Selecionar ferramenta "${nome_ferramenta}"

    Wait Element Vision    icone_paint

    Click Vision    ${nome_ferramenta}    backend=uia


Pintar desenho
    [Arguments]     ${dados_imagem}

    Selecionar ferramenta "${BALDE}"

    FOR     ${key}     ${value}   IN      &{dados_imagem}
        
        ${cor}      Set Variable      ${value}[param_cor]
        Editar Cor RGB  @{cor}

        Pintar area     ${value}[coordenadas]
   
    END


Pintar area
    [Arguments]     ${coordenadas}
    
    FOR    ${coord}   IN    @{coordenadas}
        Click Coord     ${coord}[0]     ${coord}[1]
    END
