from tkinter import *
import networkx as nx
import matplotlib.pyplot as plt
import DiGraph
from tkinter.filedialog import askopenfilename
import tkinter.messagebox as msg


class Interface(Frame):
    def __init__(self,master):
        Frame.__init__(self)
        self.Digraph = DiGraph.DiGraph()
        self.g = nx.DiGraph()
        self.master = master
        self.caixa = IntVar()
        self.aplicativo = []
        self.box_menu_0()
        self.box_select_1()
        self.box_scrolled_2()
        self.box_image_3()

    def add_Edge(self, c=1, pessoa=None, amigo=None, afinidade=None):
        try:
         if c == 1:
            self.Digraph.addEdge(self.box_pessoa.get(), self.box_amigo.get(), int(self.box_afinidade.get()))
            self.g.add_edge(self.box_pessoa.get(), self.box_amigo.get())
            self.loadGraph()
            self.box_pessoa.delete(0,END)
            self.box_amigo.delete(0,END)
            self.box_afinidade.delete(0,END)
         else:
            self.Digraph.addEdge(pessoa, amigo, int(afinidade))
            self.g.add_edge(pessoa, amigo)
        except:
            msg.showinfo("Erro","Algo digitado errado!")


    def remove(self):
        try:
         self.Digraph.removeVertex(self.nome_dell.get())
         self.g.remove_node(self.nome_dell.get())
         self.loadGraph()
        except:
            msg.showinfo("Erro404!","Nome não encontrado!")

    def shortespath(self):
        try:
         self.Digraph.incomingEdges(self.box_pessoa.get())
         self.Digraph.incomingEdges(self.box_destino.get())
         vet = self.Digraph.Dijkstra2(self.box_origem.get(),self.box_destino.get())
         texto = " O menor caminho de " + self.box_origem.get() + " até " + self.box_destino.get() +":"
         self.add_list(texto)
         for i in range(len(vet)):
            if i != len(vet)-1:
                texto = " (" + str(vet[i].getVertex()) + ": d= " + str(vet[i].getCost()) +") --->"
            else:
                texto = " (" + str(vet[i].getVertex()) + ": d= " + str(vet[i].getCost()) + ")"
            self.add_list(texto)
        except:
            msg.showinfo("Erro","Por favor preencher corretamente!")

    def recommendfriend(self):
        try:
         print(self.caixa.get())
         if self.caixa.get() == 1:
            topK = int(self.variable.get())
            itens=topK
            dist = self.Digraph.Dijkstra(self.box_pessoa_recomend.get())
            dist.pop(self.box_pessoa_recomend.get()) #Remove a personOfInterest do dicionário
            friends = self.Digraph.adjacentTo(self.box_pessoa_recomend.get())
            order1 = dict()
            order2 = dict()


            for item in friends:
                dist.pop(item.getVertex())

            aux = sorted(dist, key=dist.get)[0]

            for key in sorted(dist, key = dist.get):
                order1[key] = dist[key]
                itens -= 1
                if (dist[aux] == dist[key]) and (itens > 0):
                    topK += 1
                aux = key

            for i in order1:
                if (topK > 0) and (dist[i] != float("inf")):
                    order2[i] = order1[i]
                    topK -= 1

            self.add_list( "Amigos recomendados(Normal):" )

            for i in order2:
                self.lista.insert(END, str(i) + " " + str(order2[i]))

         elif self.caixa.get() == 0:
            topK = int(self.variable.get())
            itens = topK
            dist = self.Digraph.Dijkstra(self.box_pessoa_recomend.get())
            dist.pop(self.box_pessoa_recomend.get())  # Remove a personOfInterest do dicionário
            friends = self.Digraph.adjacentTo(self.box_pessoa_recomend.get())
            order1 = dict()
            order2 = dict()

            for item in friends:
                dist.pop(item.getVertex())

            for key in dist:
                dist[key] = dist[key]*(self.Digraph.numEdges()-len(self.Digraph.incomingEdges(key)))

            aux = sorted(dist, key=dist.get)[0]
            for key in sorted(dist, key = dist.get):
                order1[key] = dist[key]
                itens -= 1
                if (dist[aux] == dist[key]) and (itens > 0):
                    topK += 1
                aux = key

            for i in order1:
                if (topK > 0) and (dist[i] != float("inf")):
                    order2[i] = order1[i]
                    topK -= 1

            self.lista.insert(END, "Amigos recomendados(Ponderado):")

            for i in order2:
                self.lista.insert(END, str(i) + " " + str(order2[i]))
        except:
            msg.showinfo("Erro","Nome não encontrado!")

    def interpret(self, c):
        for i in range(len(c)):
            if c[i][0] == "add":
                self.add_Edge(0, c[i][1], c[i][2], c[i][3])
            elif c[i][0] == "showFriends":
                pass
            elif c[i][0] == "recommendFriends" and c[i][2] == "dist":
                pass
            elif c[i][0] == "recommendFriends" and c[i][2] == "weightedDist":
                pass
            elif c[i][0] == "shortestPath":
                pass
            elif c[i][0] == "remove":
                pass
            else:
                print(c[i])
                print("Comando inválido")
        self.loadGraph()
        self.lista.insert(END, "              Arquivo de texto ")
        self.lista.insert(END, "      adicionado com sucesso!")

    def add_list(self, text):
        self.lista.insert(END, " ")
        self.lista.insert(END,text)

    def load_archive(self):
        try:
         if self.Entry_name_arch.get() == "":
            filename =  askopenfilename(filetypes=(("text files", "*.txt"), ("all files", "*.*")))
            self.Entry_name_arch.insert(INSERT,filename)
            self.interpret(self.read_open(filename))
         else:
            self.interpret(self.read_open(self.Entry_name_arch.get()))
        except:
            msg.showinfo("Erro","Aquivo não encontrado!")

    def read_open(self,nome):
        comandos = []
        with open(nome, "r") as arq:
            for i in arq:
                comandos.append(i.split())
        return comandos


    def loadGraph(self):
        nx.draw_shell(self.g, with_labels=True)
        plt.savefig("grafo.png")
        plt.clf()
        img = PhotoImage(file="grafo.png", )
        self.aplicativo[3].config(image=img)
        self.aplicativo[3].image=img


    def delete(self):
        self.aplicativo[1].destroy()
        self.aplicativo[1] = Frame()

        Label_dell = Label(self.aplicativo[1], bg="white")
        Label_dell.pack()

        separador = Label(Label_dell, text="")
        self.nome_dell = Entry(Label_dell)
        button_dell = Button(Label_dell,text="Deletar", command=self.remove)

        self.nome_dell.pack(side="left")
        separador.pack(side="left")
        button_dell.pack(side="left")

        self.aplicativo[1].grid(row=0, column=1)


    def add(self):
        self.aplicativo[1].destroy()
        self.aplicativo[1] = Frame()
        Label_friends = Label(self.aplicativo[1], bg="white")
        Label_friends.pack()

        Label_pessoa = Label(Label_friends, bg="white")
        Label_amigo = Label(Label_friends, bg="white")
        Label_afinidade = Label(Label_friends, bg="white")

        texto_pessoa = Label(Label_pessoa,text="Pessoa:")
        texto_amigo = Label(Label_amigo,text="Amigo:")
        texto_afinidade = Label(Label_afinidade,text="Afinidade:")

        self.box_pessoa = Entry(Label_pessoa,width=20)
        self.box_amigo = Entry(Label_amigo,width=20)
        self.box_afinidade = Entry(Label_afinidade,width=10)

        box_send = Button(Label_friends,text="Enviar!",command=self.add_Edge)

        texto_pessoa.pack(side="left")
        self.box_pessoa.pack(side="left")
        Label_pessoa.pack(side="left")

        separador = Label(Label_friends, bg="White", text="")
        separador.pack(side="left")

        texto_amigo.pack(side="left")
        self.box_amigo.pack(side="left")
        Label_amigo.pack(side="left")

        separador = Label(Label_friends, bg="White", text="")
        separador.pack(side="left")

        texto_afinidade.pack(side="left")
        self.box_afinidade.pack(side="left")
        Label_afinidade.pack(side="left")
        separador.pack(side="left")

        separador = Label(Label_friends, bg="White", text="")
        separador.pack(side="left")

        box_send.pack(side="left")

        self.aplicativo[1].grid(row=0, column=1)


    def Recomend(self):
        self.aplicativo[1].destroy()
        self.aplicativo[1] = Frame()
        Label_shorter = Label(self.aplicativo[1])
        Label_recomend = Label(self.aplicativo[1])
        Label_shorter.pack(side=TOP)
        Label_recomend.pack(side=BOTTOM)

        #menor caminho

        Titulo = Label(Label_shorter, text="Menor Caminho                                                                                                                              ", bg="white")
        Titulo.pack(side=TOP)

        self.box_origem = Entry(Label_shorter, width=20)
        self.box_destino = Entry(Label_shorter,width=20)

        text_origem = Label(Label_shorter,text="Origem:")
        test_destino = Label(Label_shorter,text="Destino:")

        Button_caminho = Button(Label_shorter,text= "Ok",width=10,command=self.shortespath)

        text_origem.pack(side=LEFT)
        self.box_origem.pack(side=LEFT)

        separador = Label(Label_shorter, text=" ")
        separador.pack(side=LEFT)

        test_destino.pack(side=LEFT)
        self.box_destino.pack(side=LEFT)

        separador = Label(Label_shorter, text=" ")
        separador.pack(side=LEFT)

        Button_caminho.pack(side=LEFT)


        #recomendações

        Titulo = Label(Label_recomend,text="Amigos recomendados                                                                                                                  ",bg="white")
        Titulo.pack(side=TOP)
        quadro2 = Label(Label_recomend)
        Label_origem = Label(quadro2)

        quadro = Label(Label_recomend)
        Label_ponderada = Label(quadro)
        Label_normal = Label(quadro)

        texto_pessoa = Label(Label_origem,text="Pessoa:",height=3)
        texto_ponderada = Label(Label_ponderada,text="Ponderada:")
        texto_normal = Label(Label_normal, text="Normal:")

        self.box_pessoa_recomend = Entry(Label_origem,width=20)

        ponderada = Radiobutton(Label_ponderada, variable = self.caixa, value = 0)
        normal = Radiobutton(Label_normal, variable = self.caixa, value = 1)

        texto_ponderada.pack(side=LEFT)
        ponderada.pack(side=RIGHT)
        Label_ponderada.pack(side=TOP)

        texto_normal.pack(side=LEFT)
        normal.pack(side=RIGHT)
        Label_normal.pack(side=BOTTOM)
        quadro.pack(side=LEFT)

        texto_pessoa.pack(side=LEFT)
        self.box_pessoa_recomend.pack(side=RIGHT)
        Label_origem.pack()

        quadro2.pack(side=LEFT)

        quadro3 = Label(Label_recomend)
        texto_select= Label(quadro3, text="Distância:",height=3)
        self.variable = StringVar(quadro3)
        self.variable.set("None")
        w = OptionMenu(quadro3,self.variable,1,2,3,4,5 )
        texto_select.pack(side=LEFT)
        w.pack(side=LEFT)

        quadro3.pack(side=LEFT)

        Buscar = Button(quadro3,text="Buscar", height=3, width=10, command= self.recommendfriend)
        Buscar.pack(side=RIGHT)


        self.aplicativo[1].grid(row=0, column=1)


    def box_menu_0(self):
        branco = "white" #cor das layers

        self.aplicativo.append(Frame())
        self.aplicativo[0].grid(row=0, column=0)

        Label_menu = Label(self.aplicativo[0],bg=branco,borderwidth=10)
        Label_menu.pack(side="top")
        nome = Label(Label_menu,text="Entre com o nome do arquivo:",bg=branco,justify="left")
        nome.pack(side="top")

        Label_abrir = Label(Label_menu)
        Label_abrir.pack(side="top")

        self.Entry_name_arch = Entry(Label_abrir,width=20, bg="white")
        self.Entry_name_arch.pack(side="left")
        separador = Label(Label_abrir, text="",bg=branco)
        separador.pack(side="left")
        Button_name = Button(Label_abrir, width = 5,text="Abrir", command=self.load_archive)
        Button_name.pack(side="left")

        Label_modo = Label(Label_menu)
        Label_modo.pack(side="bottom")

        separador = Label(Label_modo,text="")

        Recomendado = Button(Label_modo,text="Recomendados", command=self.Recomend)

        Recomendado.pack(side="left")
        separador.pack(side="left")

        Label_modo2 = Label(Label_menu)
        Label_modo2.pack(side="bottom")

        separador = Label(Label_modo2,text="")

        Adicionar = Button(Label_modo2,text="Adicionar",command=self.add)
        Remover = Button(Label_modo2,text="Remover",command=self.delete)

        Adicionar.pack(side="left")
        separador.pack(side="left")
        Remover.pack(side="left")

        Modo_texto = Label(Label_menu,text="Selecione o modo:", bg=branco)
        Modo_texto.pack(side="bottom")

    def box_select_1(self):
        self.aplicativo.append(Label(width=90, text="Toda função selecionada será exibida aqui!"))
        self.aplicativo[1].grid(row=0, column=1)


    def box_scrolled_2(self):
        self.aplicativo.append(Frame())
        scrollbar = Scrollbar(self.aplicativo[2])
        self.lista = Listbox(self.aplicativo[2],bg="white", height=30,width=30,yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.lista.yview)
        self.lista.pack(side="left")
        scrollbar.pack(side=RIGHT,fill=Y)
        self.aplicativo[2].grid(row=1, column=0)

    def box_image_3(self):

        img = PhotoImage(file="grafo-none.png")
        self.aplicativo.append(Label(image=img))
        self.aplicativo[3].image=img
        self.aplicativo[3].grid(row=1,column=1,ipady=1)

if __name__ == '__main__':
    window = Tk()
    window.resizable(0,0)
    app = Interface(window)
    window.mainloop()


