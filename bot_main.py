#-*- coding: 'utf-8' -*-
from __future__ import unicode_literals
import os
import Listado_de_opciones as Opciones
from random import randint as fn_escoger_numero
from JuegoAdivinaNumero import game

from telegram import (

    Update
    ,InlineKeyboardButton
    ,InlineKeyboardMarkup

)# Fin del import en masa del paquete telegram
from telegram.ext import(

    ApplicationBuilder
    ,CommandHandler
    ,MessageHandler
    ,filters
    ,ContextTypes
    ,CallbackQueryHandler

)# Fin del import en masa del paquete telegram ext

i_dania_id = int(os.environ['DaniaID'])# El ID de Dania para que se use en diferentes partes del código.
i_sukume_id = int(os.environ['SukumeID'])
i_arthur_id = int(os.environ['ArthurID'])
i_melissa_id = int(os.environ['MelissaID']) 
i_creador_id = int(os.environ['CreadorID'])

async def fn_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Has despertado a una Diosa, humano. Qué quieres ahora?")

def fn_selec_string(ar_arreglo) -> str:
    """
    Función utilitaria que selecciona al azar un string de un arreglo y lo devuelve.
    Parámetro único. Arreglo de strings del cuál se espera escoger uno al azar.
    """
    i_indice = fn_escoger_numero(

        0 #Toma en cuenta el elemento inicial
        ,len(ar_arreglo) - 1 # y el elemento final del arreglo

    )# Fin de la función fn_escoger_numero que selecciona al azar un número entero que será el elemento a devolver.
    return ar_arreglo[i_indice]

# Fin de la función fn_selec_string
# Cuando alguien entra
async def fn_bienvenida(update: Update, context: ContextTypes.DEFAULT_TYPE):
    for user in update.message.new_chat_members:

        nombre = user.first_name
        #i_indice = fn_escoger_numero(0, len(Opciones.Ar_MensajesBienvenida) - 1)# Escoje un índice al azar basado en un número.
        #s_cadena_aleatoria = Opciones.Ar_MensajesBienvenida[i_indice] # Extrae el mensaje seleccionado del arreglo de bienvenida 
        s_cadena_aleatoria = fn_selec_string(Opciones.Ar_MensajesBienvenida)
        await update.message.reply_text(f"{nombre}, " + s_cadena_aleatoria )

# Fin de la función fn_bienvenida
# Cuando alguien se va
async def fn_despedida(update: Update, context: ContextTypes.DEFAULT_TYPE):

    user = update.message.left_chat_member
    nombre = user.first_name
    await update.message.reply_text(f"Adios, {nombre}!! Siempre te recordaremos como el tipo que se fue justo en este momento.")

# Fin de la función fn_despedida
def fn_elegir_saludo(obj_contexto) -> str:

    int_user_id = obj_contexto.id #Parámetro obligatorio.
    s_firstName = obj_contexto.first_name #Parámetro obligatorio.
    s_lastName = obj_contexto.last_name
    s_userName = obj_contexto.username
    print(

            f"El ID es lo siguiente -> {int_user_id}\n"
            f"El first name es el siguiente -> {s_firstName}\n"
            f"El last name es el siguiente -> {s_lastName}\n"
            f"El user name es el siguiente -> {s_userName}\n"

    )# fin del bloque print
    if s_firstName == 'CodeGen' or s_userName == 'DarkFireLight':
     respuesta = fn_selec_string(Opciones.ar_saludoCreador)
    elif int_user_id == i_melissa_id:
     respuesta = fn_selec_string(Opciones.ar_saludosMelissa)
    elif int_user_id == i_dania_id:
     respuesta = fn_selec_string(Opciones.ar_saludoDania)
    elif int_user_id == i_sukume_id:
     respuesta = fn_selec_string(Opciones.ar_saludoSokete)
    elif int_user_id == i_arthur_id:
     respuesta = fn_selec_string(Opciones.ar_saludosArthur)
    else:
     respuesta = f"Buen intento, {s_firstName}. Pero una Diosa como yo no es fácil de conquistar con un solo \"hola\". Sin embargo, debo de "\
     + "coincidir contigo en que si buscas una waifu, el paso inicial siempre será un \"hola\""
    return respuesta

# Fin de la función fn_elegir_saludo
async def fn_hola(update: Update, context: ContextTypes.DEFAULT_TYPE):

    """
    Función que devuelve un saludo personalizado dependiendo de la persona que ejecuta
    el comando.
    """
    b_es_boton = False
    try:
     dir(update.message.reply_text)
    except AttributeError:
     b_es_boton = True
    if b_es_boton:

        answer=fn_elegir_saludo(update.callback_query.from_user)
        await update.callback_query.message.reply_text(answer)

    # Fin del if que ejecuta cuando el usuario pulsa botón
    else:

        answer=fn_elegir_saludo(update.effective_user)
        await update.message.reply_text(answer)

    # Fin del else que ejecuta cuando el usuario utiliza un comando
# Fin de la función fn_hola
async def fn_holo(update: Update, context: ContextTypes.DEFAULT_TYPE):

    s_firstName = update.effective_user.first_name #Parámetro obligatorio.
    s_mensaje = " ".join(context.args)
    try:
        with open("HoloSeñal.jpg", "rb") as img:
            await context.bot.send_photo(

                chat_id = i_dania_id 
                ,photo = img
                ,caption = f"El usuario {s_firstName} te manda a decir lo siguiente '{s_mensaje}'"

            )# Fin del paréntesis de send_photo
        # Fin del bloque with
        await update.message.reply_text(f'Dania Sama ha sido invocada según su mandato, oh gran {s_firstName}')

    # Fin del bloque try
    except Exception as e:
     await update.message.reply_text(f'Algo salió mal! El detalle del error es el siguiente ->\n-{e}')

## Fin de la función holo

async def fn_echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(update.message.text)

async def fn_gata(update: Update, context: ContextTypes.DEFAULT_TYPE):

    s_userName = update.effective_user.username
    if s_userName == "amte30":
     respuesta = 'Pero mi señora!! Sé que soy una Diosa pero esto es demasiado... Qué dirá mi creador si se diera cuenta!!'\
     ' No tenía idea que tuvieras esos gustos!! 😉'
    else:
     respuesta = "Alto gata!!! Mi creador ya tiene su dueña y señora. No le coquetés!"
    await update.message.reply_text(respuesta)

#Fin de la función fn_gata
async def fn_notificar_miembros(

    update: Update
    ,context: ContextTypes.DEFAULT_TYPE

):# Fin de la lista de parámetros de la función fn_notificar_miembros
    """
    Función que se activa para notificar a todos los miembros del grupo que alguien ha iniciado un directo.
    """
    ar_miembros = [

        i_creador_id
        ,i_dania_id #ID de Dania
        ,i_melissa_id 
        ,i_sukume_id
        ,i_arthur_id

    ]# Fin del arreglo ar_miembros
    b_hay_Error = False
    for i_ID in ar_miembros:
        try:
            await context.bot.send_message(

                i_ID 
                ,"Oye humano(a)! Siéntete feliz ya que mi creador me ha mandado a avisarte de lo siguiente..."

            )# fin de la función send_Message
            with open('InvitaciónDirectoFinal_001.mp4', 'rb') as video:
                await context.bot.send_video(

                    i_ID 
                    ,video

                )# Fin de la función send_video
            # Fin del bloque with
        # Fin del bloque Try
        except Exception as e:
            await context.bot.send_message(

                i_creador_id#ID del admin o del creador que activó la función
                ,f"Este es el detalle del error, mi gran creador: \n\n{e}\n\nY ocurrió con la ID: {i_ID}"

            )# Fin del método send message
            b_hay_Error = True #Establece la bandera que indica que hubo algún error para notificar en el chat general

        #Fin del bloque except
    # Fin del bloque for
    if b_hay_Error :
     await update.message.reply_text('Algo salió mal!')

#Fin de la función fn_notificar_miembros
async def fn_mostrar_menu(

    update: Update
    ,context: ContextTypes.DEFAULT_TYPE

):
    ar_menu =[

       [InlineKeyboardButton('Hola', callback_data='Saludar')]
       ,[InlineKeyboardButton('Invocar a Dania', callback_data='Dania')]

    ]# Fin del arreglo menú con los botones para mostrar en el menú
    await update.message.reply_text(

        'Este es el exhuberante menú de opciones que te ofrece tu deidad favorita. Elige la que te guste más, humano!'
        ,reply_markup=InlineKeyboardMarkup(ar_menu)

    )# Fin del reply text
# Fin de la función fn_mostrar_menu
async def fn_manejador_botones_menu(

    update: Update
    ,context: ContextTypes.DEFAULT_TYPE

):
    query = update.callback_query
    await query.answer()
    if query.data == 'Saludar':
     await fn_hola(update, context)
    else:
     await fn_holo(query, context)

# Fin de la función fn_manejador_botones_menu para manejo de los botones del menú

# Token sagrado para que Telegram reconozca que esta ejecución es legítima.
TOKEN = os.environ['BotToken']

if __name__ == '__main__':
    
    app = ApplicationBuilder().token(TOKEN).build()
    ################ Sección de handlers del bot ############################
    app.add_handler(CommandHandler("start", fn_start))
    app.add_handler(CommandHandler("Hola", fn_hola))
    app.add_handler(CommandHandler("Holo", fn_holo))
    app.add_handler(MessageHandler(filters.TEXT & filters.Regex(r'(?i)^oye!*$'), fn_gata))
    #app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, fn_echo))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, fn_despedida))
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, fn_bienvenida))
    app.add_handler(MessageHandler(filters.StatusUpdate.VIDEO_CHAT_STARTED, fn_notificar_miembros))
    app.add_handler(game)
    app.add_handler(CommandHandler("Menu", fn_mostrar_menu))
    app.add_handler(CallbackQueryHandler(fn_manejador_botones_menu))

    print("Bot en funcionamiento... Presiona CNTL + C para terminar")
    app.run_polling()

# Fin del if que ejecuta el bloque de código principal del bot
