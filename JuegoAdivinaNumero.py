#-*- coding: 'utf-8' -*-
from __future__ import unicode_literals

from telegram import Update
from random import randint as fn_escoger_numero
from telegram.ext import (

    CommandHandler
    ,MessageHandler
    ,filters
    ,ContextTypes
    ,ConversationHandler

)

##############  Etapas del juego y variables  #####################
ADIVINAR = 'Etapa de adivinación' #Etapa única de esta converzación.

async def fn_adivnar_empiezo(

    update: Update
    ,context: ContextTypes.DEFAULT_TYPE

):
    """
    Función inicial que recibe e instruye al usuario sobre las reglas y capacidades del juego.
    """
    s_firstName = update.effective_user.first_name #Nombre del que empieza el juego.
    i_numero_desconocido = fn_escoger_numero(1, 10000)
    print(f'\nEl número selecionado es -> {i_numero_desconocido}\n')# Línea de depuración y prueba. Luego se puede borrar
    context.chat_data['unknown_number'] = i_numero_desconocido
    context.chat_data['try_counter'] = 12
    b_es_grupo = update.message.chat.type != 'private'
    s_cadena_variante = 'Tendrás intentos ilimitados para' if b_es_grupo else 'Tendrás doce intentos para'
    await update.message.reply_text(

        f'Bueno señoras y señores! {s_firstName} acaba de pedirme que inicie un juego de adivinanza. Te nos unes?\n\n'
        '\t\t\tReglas:\n\nJusto ahora se ha escogido un número que está entre el 1 y el 10,000. '+s_cadena_variante
        +' adivinar el número.\nLas entradas deben ser números sólamente. Nada de texto. Si logras adivinar el número, se '\
        +'acabó!! Ganastes y fin del juego. Si se te pasan o no son suficientes las oportunidades, lo mismo pasa sólo que '\
        +'pierdes. Se entiende? Excelente para ser un humando! Entonces que empiece el juego.'
            
    )# Fin del método reply_text
    return ADIVINAR 

# Fin de la función fn_adivnar_empiezo
async def fn_recibir_intento(

    update: Update
    ,context: ContextTypes.DEFAULT_TYPE

):
    """
    Función que realiza la lógica principal del juego. Condiciona si avanza al estado final 
    o vuelve a ejecutar esta función en un intento más por adivinar el número elegido al azar.
    """
    ############## Sección de variables ##################
    s_firstName = update.effective_user.first_name #Nombre del que empieza el juego.
    i_numero_desconocido = context.chat_data['unknown_number'] 
    i_try = int(update.message.text)
    b_endGame = False # Valor bandera que valida si el juego acaba o se sigue intentando
    i_contador_intentos = context.chat_data['try_counter'] 
    b_es_grupo = update.message.chat.type != 'private'
    ######### Sección de lógica del programa #############
    if i_try < i_numero_desconocido:
        await update.message.reply_text(

             f'Buen intento, {s_firstName}!!! Nada mal para ser un humano promedio!!! Lo malo es que te faltó para acertar. '
             f'Pero tranquilo!! Aún te quedan {i_contador_intentos - 1} intentos para que lo inevitable pase...'

         )# Fin del método fn_responder
    # Fin del if que ejecuta en caso de que el número ingresado sea mayor que el que se espera adivinar.
    elif i_try > i_numero_desconocido:
        await update.message.reply_text(

             f'Buen intento, {s_firstName}!!! El intento que acabas de gastar solamente peca de ser demasiado grande.'
             f' Algo así como equivocarse en una dirección por un factor de tres estados. Trata de no cagarla de nuevo en los {i_contador_intentos - 1} intentos '
             'que te quedan!'

         )# Fin del método fn_responder
    # Fin del elif que ejecuta en el caso de que el intento sea mayor que el número a adivinar
    else:
        await update.message.reply_text(

            f'Excelente trabajo, humano!! Feliciten todos a {s_firstName} por acertar el número elegido al principio del juego. De los diez intentos iniciales '
            f'{s_firstName} acertó y aún le quedaban {i_contador_intentos - 1} intentos. Mejor suerte para la próxima vez a los demás que participaron.'
            '\n\n\n\t\t\tGAME OVER'

        )# Fin del método fn_responder
        b_endGame = True# Se termina porque se adivinó el número.

    # Fin del else que ejecuta en el caso de que el jugador acierte.
    print(f'Este es el valor de chat.type -> {update.message.chat.type}')#Línea de prueba. Puede ser borrada.
    if update.message.chat.type != 'group':
     i_contador_intentos -= 1 # Se quita un intento del contador.
    context.chat_data['try_counter'] = i_contador_intentos# Se guarda el contador en la variable de contexto.
    if i_contador_intentos == 0 and not b_endGame:# Se finish!
        await update.message.reply_text(

            f'Bueno chic(@)s!! El sr(a) {s_firstName} acaba de cagarla y quemó el último intento que quedaba.'
            f' El número que estaban tratando de adivinar era el -> {i_numero_desconocido}.\n\n\t\t\tGAME OVER\n'

        )#Fin del método reply_text
        b_endGame = True# Se termina porque se agotaron los intentos

    #Fin del if que ejecuta cuando agotas el número de intentos para acertar el número elegido.
    return ConversationHandler.END if b_endGame else ADIVINAR 

# Fin de la función fn_recibir_intento
async def fn_abortar_juego(


    update: Update
    ,context: ContextTypes.DEFAULT_TYPE

):
    s_firstName = update.effective_user.first_name #Nombre del que empieza el juego.
    await update.message.reply_text(

        f'El o la usuario(a) {s_firstName} ha decidido que no quiere continuar con el juego.\n\nEntiendo que mis juegos han sido demasiado para ti, pobre mortal!'
        ' Después de todo, tu tiempo es limitado. De todas formas, acá estaré como siempre si quieres volver a jugar.\n\n\n\t\t\tGAME OVER.'

    )#Fin del método reply text
    return ConversationHandler.END

#Fin de la función fn_abortar_juego
############### Configuración del handler ######################
game = ConversationHandler(

    entry_points = [
        CommandHandler(

            'AdivinaNumero'
            ,fn_adivnar_empiezo

        )
    ]# /AdivinaNumero para empezar el juego.
    ,states = {
        ADIVINAR: [
            MessageHandler(

                filters.Regex(r'^[0-9]+$')
                ,fn_recibir_intento

            )#Fin de la inicialización del objeto Messagehandler
            ,MessageHandler(

                filters.TEXT & filters.Regex(r'^[0-9]+$')
                ,fn_recibir_intento

            )#Fin de la inicialización del objeto Messagehandler
        ]# Fin del arreglo asociado al estado Adivinar
    }#Fin del diccionario states
    ,fallbacks = [
        CommandHandler(

            'abortar' 
            ,fn_abortar_juego

        )#Fin de la inicialización del CommandHandler
    ]# /abortar para terminar de manera prematura el juego.
    ,per_user=False #Permite converzaciones compartidas

)#Fin de la inicialización del objeto handler Game
