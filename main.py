﻿

from tkinter import *
from tkinter import ttk
import os
import sys
import subprocess
import re
import webbrowser
from tkinter import filedialog
#####################################################################


#funcion para buscar valor de capacitores comerciales
def buscar_cap():
    numero= codigo.get()
    #validamos que lo ingresado sea numeros
    digit=numero.isdigit()


    if  digit==False and re.match("^\d+?\.\d+?$",numero) is None:

        codigo.set('ERROR')

    else:
        cap_comercial=(0.5,1,1.2,1.5,1.8,2.2,2.7,3.3,3.9,4.7,5.6,6.8,8.2,10,12,15,18,22,27,33,39,47,56,68,82,100,120,150,180,220,270,330,390,470,560,680,820,1000,1200,1500,1800,2200,2700,3300,3900,4700,5600
        ,6800,8200,10000,12000,15000,18000,22000,27000,33000,39000,47000,56000,68000,82000,100000,120000,150000,180000,220000,330000,390000,470000,560000,680000,820000,1000000)
        #convertimos a una lista string
        numero= float(numero)
        disponible=numero in cap_comercial


        if disponible==True:
            #setiamos la entry
            cap_up.set('This value is')
            cap_down.set('Commercial')

        else:

            #numero mas cercano
            takeClosest= lambda num,collection:min(collection,key=lambda x:abs(num-x))
            Closest=takeClosest(numero,cap_comercial)
            print(Closest)

            Nexposicion=cap_comercial.index(Closest)


            if numero > Closest :
                cap_down.set(Closest)
                Nexposicion=Nexposicion+1
                Nexposicion=cap_comercial[Nexposicion]
                cap_up.set(Nexposicion)

            else:
                Nexposicion=Nexposicion-1
                Nexposicion=cap_comercial[Nexposicion]
                cap_down.set(Nexposicion)
                cap_up.set(Closest)




#def fun_sufijo(sufijo, capacitancia):
def fun_sufijo(*args):
    sufijo=args[0]
    capacitancia=args[1]
    # capcitancia por defecto en pf

    if sufijo == "nf":
        c=capacitancia/1000

    elif sufijo == "uf":
        c=capacitancia/1000000

    elif sufijo == "mf":
        c=capacitancia/1000000000

    elif sufijo == "f":
        c=capacitancia/1000000000000

    #else sufijo = "pf"
    else :
        c = capacitancia
        #retornar capacitancia y el sufijo que lo llame
    return c

#Funcion para calcular capacitores
def calculo_cap():

    #CALCULADO LOS VOLTIOS
    #creamos un diccionario
    dic_volt={'0G':'4VDC','0L':'5.5VDC','0J':'6.3VDC','1A':'10VDC','1C':'16VDC','1E':'25VDC','1H':'50VDC','1J':'63VDC','1K':'80VDC','2A':'100VDC','2Q':'110VDC','2B':'125VDC',
    '2C':'160VDC','2Z':'180VDC', '2D':'200VDC', '2P':'220VDC', '2E':'250VDC','2F':'315VDC','2V':'350VDC','2G':'400VDC','2W':'450VDC','2H':'500VDC','2J':'630VDC','3A':'1000VDC' }

    volts=vol_combo.get()
    #buscamos el codigo referente al voltaje en el diccionario y le asignamos el valor a volts
    volts=dic_volt.get(volts)
    #setiamos la entry de Voltaje
    volts_cap.set(volts)

    #CALCULANDO LA CAPACITANCIA
    pn=pn_combo.get() #primer numero
    sn=sn_combo.get() #segundo numero
    tn=cero_combo.get() #tercer numero

    if pn=='n'or sn=='n' or tn=='n':
        if pn=='n':
            valor = sn+tn #concatenamos caracteres
            ceros= '0'

        elif sn=='n':
            valor=pn+tn
            ceros='00'

        elif ceros=='n':
            valor=pn+sn
            ceros='000'

        capacitancia=float(valor+ceros)


    elif pn=='p' or sn=='p':


        if pn== 'p':
            sn=float(sn)
            valor=0.1*sn

        elif sn=='p':
            tn=float(tn)
            pn=float(pn)
            valor=pn+(tn/10)
        capacitancia=float(valor)


    else:
        valor= pn+sn
        valor=float(valor)

#    if ceros == 'None':
#        ceros=1
#    else:
        ceros=int(tn)
        #(1x10)^ceros
        ceros=10**ceros
        #multiplicamos el valor con el numero multiplicador
        capacitancia= valor*ceros

    #validamos el sufijo
    sufijo=combo.get()
    print(capacitancia)
    #llamamos a la funcion sufijo
    c=fun_sufijo(sufijo, capacitancia)
    capacitancia=c
    print(capacitancia)
    #por defecto el valor es en pf
    capacitancia= str(capacitancia) + sufijo
    #setiamos la entry capacitancia con el valor capacitancia
    valor_cap.set(capacitancia)



    #CALCULANDO TOLERANCIA

    #creamos un diccionario para la tolerancia
    dic_tole={'B':'0.10pf','C':'0.25pf','D':'0.5pf','E':'0.5%','F':'1%', 'G':'2%', 'H':'3%', 'J':'5%', 'K':'10%', 'M':'20%','N':'30%',
    'P':'+100%, -0%','Z':'+80%, -20%'}
    tolerancia=tole_combo.get()
    tolerancia=dic_tole.get(tolerancia)
    #setiamos la entry de Tolerancia
    tole_cap.set(tolerancia)


#   CALCULO DE CAPACITORES PARALELO

def cap_paralelo ():
    cap1=paralelo1.get()
    cap2=paralelo2.get()
    cap_result=cap1+cap2
    #setiamos la firts entry
    paralelo1.set(cap_result)
    paralelo2.set('  ')

def cap_serie ():
    cap1=serie1.get()
    cap2=serie2.get()
    cap_result=cap1*cap2/cap1+cap2
    #setiamos la firts entry
    serie1.set(cap_result)
    serie2.set('  ')

#Funciones para la pestaña resisitencia
def buscar_res():
    valor_res= code_res.get()
    #validamos que lo ingresado sea numeros
    digit=valor_res.isdigit()


    if  digit==False and re.match("^\d+?\.\d+?$",valor_res) is None:

        codigo.set('ERROR')

    else:
        res_comercial=(1,1.2,1.5,1.8,2.2,2.7,3.3,3.9,4.7,5.1,5.6,6.8,8.2,10,12,15,18,22,27,33,39,47,51,56,68,82,100,120,150,180,220,270,330,390,470,510,560,680,820,1000,1200,1500,1800,2200,2700,3300,3900,4700,
        5100,5600,6800,8200,10000,12000,15000,18000,22000,27000,33000,39000,47000,51000,56000,68000,82000,100000,120000,150000,180000,220000,330000,390000,470000,510000,560000,680000,820000,1000000)

        #convertimos a una lista string
        valor_res= float(valor_res)
        disponible=valor_res in res_comercial


        if disponible==True:
            #setiamos la entry
            res_up.set('This value is')
            res_down.set('Commercial')

        else:

            #numero mas cercano
            takeClosest= lambda num,collection:min(collection,key=lambda x:abs(num-x))
            Closest=takeClosest(valor_res,res_comercial)
            print(Closest)

            Nexposicion=res_comercial.index(Closest)


            if valor_res > Closest :
                res_down.set(Closest)
                Nexposicion=Nexposicion+1
                Nexposicion=res_comercial[Nexposicion]
                res_up.set(Nexposicion)

            else:
                Nexposicion=Nexposicion-1
                Nexposicion=res_comercial[Nexposicion]
                res_down.set(Nexposicion)
                res_up.set(Closest)




#Funcion calcular el codigo de colores
def calculo_color():
    #obtenmos el valor numerico
    valor_num=resistor_value.get()
    val1=valor_num[:1]
    val2=valor_num[1:2]
    val3=valor_num[2:]
    val4=valor_num[3:4]


    ceros=len(val3)
    #(1x10)^ceros
    ceros=str(10**int(ceros))
    # ceros=str(ceros)
    ceros=str(len(ceros[1:]))
    print(type(ceros))



    #Si es de 4 bandas
    # if len(valor_num)==4:
    #     ceros=int(val4)
    #     #(1x10)^ceros
    #     ceros=10**ceros



    # #buscamos los ceros
    # list_oh=[]
    # p_band=0
    # p_string=0 #posicion del cero en la cadena
    # for oh in valor_num:
    #     if oh=='0':
    #         p_string=p_string+1
    #         lista_ceros=list_oh.append(p_band)
    # #Posicion de la banda
    #     p_band=p_band+1
    # list_oh_1=[int(item) for item in list_oh]
    # print(len(list_oh))
    # print(list_oh)





    #creamos un diccionario
    #Esta vez buscamos el numero y el contenido es el color
    color_value={'1':'brown','2':'red','3':'orange','4':'yellow','5':'green','6':'blue','violet':'7','gray':'8','white':'9','black':'0'}

    tole_res={'N/A':'20%','Silver':'10%','Golden':'5%','Red':'2%','Brown':'1%','Green':'0.5%', 'Blue':'0.25%','Violet':'0.10%','Gray':'0.05%'}

    #diccionario para setiar el combobox tolerancia segun la banda seleccionada
    combo_tole_dic={'20%':'1','10%':'2','5%':'3','Red':'2%','Brown':'1%','Green':'0.5%', 'Blue':'0.25%','Violet':'0.10%','Gray':'0.05%'}


    banda1=color_value.get(val1)
    banda2=color_value.get(val2)
    banda3=color_value.get(ceros)
    #setiamos el color de la banda1
    label_ban1.configure(bg=banda1)
    label_ban2.configure(bg=banda2)
    label_ban3.configure(bg=banda3)
    # label_ban5.configure(bg=banda5)




#Funcion para calcular Resistores
def calculo_res():
    banda1=ban1_combo.get()
    banda2=ban2_combo.get()
    banda3=ban3_combo.get()
    banda4=ban4_combo.get()
    banda5=ban5_combo.get()


    #creamos un diccionario
    color_value={'brown':'1','red':'2','orange':'3','yellow':'4','green':'5','blue':'6','violet':'7','gray':'8','white':'9','black':'0'}

    tole_res={'N/A':'20%','Silver':'10%','Golden':'5%','Red':'2%','Brown':'1%','Green':'0.5%', 'Blue':'0.25%','Violet':'0.10%','Gray':'0.05%'}

    #diccionario para setiar el combobox tolerancia segun la banda seleccionada
    combo_tole_dic={'20%':'1','10%':'2','5%':'3','Red':'2%','Brown':'1%','Green':'0.5%', 'Blue':'0.25%','Violet':'0.10%','Gray':'0.05%'}


    if banda4 == 'none':
        print('entroo')
        label_ban4.configure(state='disable')
        ban4=' '
        ventana.update()

    if banda5== 'Golden':
        banda5= 'gold2'


    #setiamos el color de la banda1
    label_ban1.configure(bg=banda1)
    label_ban2.configure(bg=banda2)
    label_ban3.configure(bg=banda3)
    label_ban5.configure(bg=banda5)


    print('color')
    print(banda1)
    ban1=color_value.get(banda1)
    ban2=color_value.get(banda2)



    if banda4 == 'none':
        #banda3 multiplicador por ceros
        ban3=int(color_value.get(banda3))
        ban3=str(10**ban3)
        #asignamos solo los ceros
        ban3=ban3[1:]

    else:
        ban4=color_value.get(banda4)
        label_ban4.configure(bg=banda4)
        #banda 3 normal
        ban3=color_value.get(banda3)
        #banda4 multiplicador por ceros
        ban4=int(color_value.get(banda4))
        ban4=str(10**ban4)
        ban4=ban4[1:]


    valor_resis=ban1+ ban2 + ban3 + ban4 +'Ω'
    #setiamos la entry del valor de resisitencia
    resistor_value.set(valor_resis)

    #Setiamos la Tolerancia
    tolerancia=banda5
    print(tolerancia)
    #buscamos en el diccionario tole_res
    #tolerancia=tole_res.get(tolerancia)
    #tolera_combo.set(tolerancia)

#####################################################################
#Configuracion inicial
ventana =Tk()
ventana.title("GNU Pytronic")

#Organizando las pestañas
notebook=ttk.Notebook(ventana)
notebook.pack(fill='both',expand='yes')
pestana=ttk.Frame(notebook)
pestana0=ttk.Frame(notebook)
pestana1=ttk.Frame(notebook)
#pestana2=ttk.Frame(notebook)
pestana2=ttk.Frame(notebook)
notebook.add(pestana,text='Home')
notebook.add(pestana0,text='Capacitors')
notebook.add(pestana1,text='Resistors')
#notebook.add(pestana2,text='Inductors')
notebook.add(pestana2,text='About')


noteStyler = ttk.Style()
noteStyler.configure("TNotebook", background='gray', borderwidth=0)

COLOR_3 = 'black'
COLOR_4 = '#2E2E2E'
COLOR_5 = '#8A4B08'
COLOR_6 = '#DF7401'
noteStyler.configure("TNotebook.Tab", background="gray", foreground=COLOR_3, lightcolor=COLOR_6, borderwidth=2)

#Funcion para saber en que pesta#a esta el usuario
def personalData(event):
    if event.widget.index("current") == 0:
       pestanan= 0
       print("Home")
    elif event.widget.index("current") == 1:
       pestanan= 1
       print("Capacitor")
       #setiamos la label del dibujo del capacitor
       defaul_c=PhotoImage(file="Sources/ceramico.png")
       label_dib_cap.config(image=defaul_c)
       label_dib_cap.image =defaul_c
       grafic_tools = 1
    elif event.widget.index("current") == 2:
       pestanan= 2
       print("Resistors")
    else:
       pestanan= 3
       print("About")
    #else:
    #   print("Not One!")
       #ttk.Frame(pestana1,os.system ('python capacitores.py'))

    return

notebook.bind("<<NotebookTabChanged>>", personalData)



#////////////////////////////////////////////
#Selecion de imagen del capacitor en el listbox

def select_image_cap(event):
    #cambiador de imagenes IMAGEN DEL CAPACITOR, CERAMICO, Electrolitico...
    widget=event.widget
    selection=widget.curselection()

    #obtenemos en string el item seleccionado en el listbox
    piked= widget.get(selection[0])
    #usamos una lista
    lis_cap=['Ceramic', 'Polyester', 'Tamtalio', 'Electrolityc', 'Mica', 'Polypropilene']
    #buscamos en la lista el valor de piked y obtenemos la posicion
    p_lis_cap=lis_cap.index(piked)
    ruta_cap=(PhotoImage(file="Sources/ceramico.png"),PhotoImage(file="Sources/poliester.png"),PhotoImage(file="Sources/tamtalio.png"),PhotoImage(file="Sources/electrolitico.png"),PhotoImage(file="Sources/plastico.png"))
    #setiamos la label del dibujo del capacitor
    label_dib_cap.config(image=ruta_cap[p_lis_cap])
    label_dib_cap.image = ruta_cap[p_lis_cap]
    grafic_tools = 1 #activamos herramientas de graficacion



#//////////////////////////////////////////////









##############################################################################
#Pestaña About

Label(pestana2,text='GNU Pytronic, software Desarrollado por Ing.Ronal Forero').place(x=20,y=60)
Label(pestana2,text='Licencia GPL V3').place(x=20,y=80)



def callback(event):
    webbrowser.open_new(r"https://ronaldl337.wordpress.com/")


link = Label(pestana2, text="GNU Pyttonics Repository", fg="blue", cursor="hand2")
link.place(x=20,y=100)
link.bind("<Button-1>", callback)

##############################################################################
#Pestaña HOME

banner=PhotoImage(file="Sources/banner.png")
banner_home=Label(pestana,image=banner).place(x=0, y=20)


##############################################################################
#Pestaña Capacitores

#definimos variables
## variables de Capacitores
codigo =StringVar() #codigo del capacitor
valor_cap =StringVar() #valor real del capacitor
volts_cap= StringVar() # voltaje del capacitor
tole_cap= StringVar()
list_tipo_cap= StringVar() #obtener el valor seleccionado en tipo de capacitor
cap_up=StringVar()
cap_down=StringVar()
serie1=DoubleVar()
serie2=DoubleVar()
paralelo1=DoubleVar()
paralelo2=DoubleVar()

#variables de resistores
code_res =StringVar() #valor de la resistencia comercial
resistor_value= StringVar()
res_up=StringVar()
res_down=StringVar()
combo_tole=IntVar() #para setear el combobox de la tolerancia


#creamos demas objetos

#Entry
#Entry Capacitor
entry_codigo=Entry(pestana0,  width= 10, textvariable=codigo).place(x=114, y=225) #codigo del capacitor
entry_valor=Entry(pestana0,  width= 10, state='readonly', textvariable=valor_cap).place(x=10, y=160) #capacitancia
entry_volt=Entry(pestana0,  width= 10,state='readonly', textvariable=volts_cap).place(x=110, y=160) #voltaje
entry_tol=Entry(pestana0,  width= 10,state='readonly', textvariable=tole_cap).place(x=210, y=160) #tolerancia
entry_comerup=Entry(pestana0,  width= 10, state='readonly',textvariable=cap_up).place(x=330, y=210) #valor comercial disponible
entry_comerdown=Entry(pestana0,  width= 10, state='readonly',textvariable=cap_down).place(x=330, y=240) #valor comercial por debajo
entry_paralel1=Entry(pestana0,  width= 10,textvariable=paralelo1).place(x=10, y=330)
entry_paralel2=Entry(pestana0,  width= 10,textvariable=paralelo2).place(x=10, y=360)
entry_serie1=Entry(pestana0,  width= 10,textvariable=serie1).place(x=280, y=330)
entry_serie2=Entry(pestana0,  width= 10,textvariable=serie2).place(x=280, y=360)

#Entry Resistors
entry_codigo=Entry(pestana1,  width= 10, textvariable=code_res).place(x=114, y=255) #codigo del capacitor
Entry(pestana1,  width= 10, textvariable=resistor_value).place(x=295, y=64) #value code
Entry(pestana1,  width= 10).place(x=90, y=180) #value code SMD
Entry(pestana1,  width= 10, state='readonly',textvariable=res_up).place(x=330, y=240) #valor comercial disponible
Entry(pestana1,  width= 10, state='readonly',textvariable=res_down).place(x=330, y=270) #valor comercial por debajo
paralel1=Entry(pestana1,  width= 10).place(x=10, y=360)
paralel2=Entry(pestana1,  width= 10).place(x=10, y=390)
serie1=Entry(pestana1,  width= 10).place(x=280, y=360)
serie2=Entry(pestana1,  width= 10).place(x=280, y=390)
#entry_aproximar=Entry(ventana,  width= 8).place(x=10, y=400) #aproximar valor



#Botones
#Botones capacitores
Boton_calcular=Button(pestana0, text= "Calculate", command= calculo_cap).place(x=420, y=58)
Boton_buscar=Button(pestana0, text= "Search", command=buscar_cap).place(x=252, y=220)
Boton_graficar=Button(pestana0, text="Graficar").place(x=410, y=600)
Boton_guardar_data=Button(pestana0, text="Guardar DATA", state='disabled').place(x=10, y=570)
Boton_paralelo=Button(pestana0, text= "+", command=cap_paralelo).place(x=120, y=330)
Boton_serie=Button(pestana0, text= "+", command=cap_serie).place(x=390, y=330)

#Botones resistores
Button(pestana1, text= "Calculate", command= calculo_res).place(x=464, y=104) #Boton calcular
Button(pestana1, text= "Solve", command= calculo_color).place(x=464, y=60) #Boton solve value resistor
Button(pestana1, text= "Solve").place(x=200, y=176) #Boton solve value resistor SMD
Button(pestana1, text= "Search", command=buscar_res).place(x=240, y=250) #Boton buscar
Button(pestana1, text= "+", command=buscar_res).place(x=120, y=360) #Boton_paralelo
Button(pestana1, text= "+", command=buscar_res).place(x=390, y=360) #Boton serie


#Labels
#Labels Capacitores
label_cchino=Label(pestana0, text="Parallel Capacitors:").place(x=10, y=310)
label_cchino=Label(pestana0, text="Serial Capacitors:").place(x=280, y=310)
label_cchino=Label(pestana0, text="Comercial value:").place(x=10, y=225)
label_tc=Label(pestana0, text="Type of Capacitor:").place(x=10, y=44)
label_voltaje=Label(pestana0, text="Voltage").place(x=110, y=138)
label_tole=Label(pestana0, text="Tolerance").place(x=210, y=138)
label_ca=Label(pestana0, text="Capacitance").place(x=10, y=138)
label_code=Label(pestana0, text="Capacitor code:").place(x=140, y=44)
#label dibujo de capacitor
label_dib_cap=Label(pestana0)
label_dib_cap.place(x=450, y=110)


#Labels RESISTORES
ima_resistor=PhotoImage(file="Sources/resistencia.png")
banner_home=Label(pestana1,image=ima_resistor).place(x=84, y=40)

Label(pestana1, text="Parallel Resistors:").place(x=10, y=340)
Label(pestana1, text="Serial Resistors:").place(x=280, y=340)
label_cchino=Label(pestana1, text="Comercial value:").place(x=10, y=255)
label_tc=Label(pestana1, text="Color Code:").place(x=10, y=110)
Label(pestana1, text="Value:").place(x=250, y=64)
Label(pestana1, text="SMD Code:").place(x=10, y=180)
label_ban1=Label(pestana1,  height= 2)
label_ban1.place(x=110, y=50)
label_ban2=Label(pestana1,  height= 2)
label_ban2.place(x=130, y=50)
label_ban3=Label(pestana1,  height= 2)
label_ban3.place(x=150, y=50)
label_ban4=Label(pestana1,  height= 2)
label_ban4.place(x=170, y=50)
label_ban5=Label(pestana1, bg="gold2",  height= 2)
label_ban5.place(x=190, y=50)

#COMBOBOX

#   COMBOBOX PARA Capacitores

#combobox codigo de voltaje
vol_combo=ttk.Combobox(pestana0, width= 3, height=3)
vol_combo.place(x=140, y=64)
vol_combo['values']=('0G','0L','0J','1A','1C','1E','1H','1J','1K','2A','2Q','2B','2C','2Z', '2D', '2P', '2E','2F','2V','2G','2W','2H','2J','3A' )


pn_combo=ttk.Combobox(pestana0, width= 3,height=3)
pn_combo.place(x=200, y=64)
pn_combo['values']=('n','p','0','0.5','1','1.2','1.5','1.8','2','2.2','2.7','3','3.3','3.9','4','4.7','5','6','7','8','9')


sn_combo=ttk.Combobox(pestana0, width= 2,height=3)
sn_combo.place(x=245, y=64)
sn_combo['values']=('n','p','0','1','2','3','4','5','6','7','8','9')


cero_combo=ttk.Combobox(pestana0, width= 2,height=3)
cero_combo.place(x=282, y=64)
cero_combo['values']=('n','0','1','2','3','4','5','6','7','8','9')


#Combobox  TOLERANCIA
tole_combo=ttk.Combobox(pestana0, width= 2, height=3)
tole_combo.place(x=335, y=64)
tole_combo['values']=('B','C','D','E','F','G','H','J','K','M','N','P','Z')


#Combobox  convercion pf a uf...
combo=ttk.Combobox(pestana0, width= 2)
combo.place(x=380, y=64)
combo['values']=('f','mf','uf','pf','nf')
combo.current(2)

#Combobox  convercion pf a uf imput comercial...
in_combo=ttk.Combobox(pestana0, width= 2)
in_combo.place(x=209, y=225)
in_combo['values']=('f','mf','uf','pf','nf')
in_combo.current(3)

#Combobox  convercion pf a uf ouput comercial...
ou_combo=ttk.Combobox(pestana0, width= 2)
ou_combo.place(x=427, y=225)
ou_combo['values']=('f','mf','uf','pf','nf')
ou_combo.current(3)




#######COMBOBOX PARA RESISTORES
#BANDA 1
ban1_combo=ttk.Combobox(pestana1, width= 6, height=3)
ban1_combo.place(x=90, y=110)
ban1_combo['values']=('brown','red','orange','yellow','green', 'blue','violet','gray','white' )

#BANDA 2
ban2_combo=ttk.Combobox(pestana1, width= 6,height=3)
ban2_combo.place(x=160, y=110)
ban2_combo['values']=('brown','red','orange','yellow','green', 'blue','violet','gray','white','black' )

#BANDA 3
ban3_combo=ttk.Combobox(pestana1, width= 6,height=3)
ban3_combo.place(x=230, y=110)
ban3_combo['values']=('brown','red','orange','yellow','green', 'blue','violet','gray','white','black' )
#BANDA 4
ban4_combo=ttk.Combobox(pestana1, width= 6,height=3)
ban4_combo.place(x=300, y=110)
ban4_combo['values']=('none','brown','red','orange','yellow','green', 'blue','violet','gray','white','black' )
ban4_combo.current(0)

#BANDA 5
ban5_combo=ttk.Combobox(pestana1, width= 6, height=3)
ban5_combo.place(x=370, y=110)
ban5_combo['values']=('Silver','Golden','Red','Brown','Green', 'Blue','Violet','Gray' )
ban5_combo.current(1)

#TOLERANCIA
tolera_combo=ttk.Combobox(pestana1, width= 6, height=3)
tolera_combo.place(x=390, y=64)
tolera_combo['values']=('20%','10%','5%','1%','0.5%', '0.25%','0.10%','0.05%' )
tolera_combo.current(2)




#Listbox
list_tc=Listbox(pestana0,width= 14, height=2)
list_tc.insert(0,"Ceramic")
list_tc.insert(1,"Polyester")
list_tc.insert(2,"Tamtalio")
list_tc.insert(3,"Electrolityc")
list_tc.insert(4,"Mica")
list_tc.insert(4,"Polypropylene")
list_tc.place(x=10, y=62)
#barra de scroll para el listbox
scrollbar_list_tc= Scrollbar(pestana0, width= 12, orient="vertical")
scrollbar_list_tc.config(command=list_tc.yview)
scrollbar_list_tc.place(x=112, y=67)
list_tc.config(yscrollcommand=scrollbar_list_tc.set)
list_tc.select_set(0)
#list_tc.selectedindex = 0
list_tc.event_generate("<<ListboxSelect>>")
list_tc.bind('<<ListboxSelect>>',select_image_cap)

#########################################################################
ventana.geometry("600x450+0+0")
#icono del software
ventana.call('wm','iconphoto',ventana._w,PhotoImage(file='pytronics.png'))

#Tema tkinter para los objetos
s=ttk.Style()
s.theme_names()
#"""======== if you are under win 8.1 you must see ..
# ('winnative', 'clam', 'alt', 'default', 'classic', 'vista', 'xpnative') you can use for example 'clam' ===== """
s.theme_use('clam')
ventana.mainloop()
