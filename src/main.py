import placa
import matplotlib.pyplot as plt

def Q2():
    print("----------Q2-----------")
    print("L = 0.1m\nN = 20\nVo = 1\n")
    p = placa.Placa()
    p.plotDistCarga()

def Q3():
    print("----------Q3-----------")
    listN = [10,30,50,70]
    for n in listN:
        print(f"------\nN = {n}")
        p = placa.Placa(N=n)
        p.plotDistCarga()

def Q4():
    print("----------Q4-----------")
    listQ = []
    listN = range(20,100,10)
    for n in listN:
        print(f"------\nN = {n}")
        p = placa.Placa(N=n)
        listQ += [p.getCargaTotal()]
    fig = plt.figure(1)
    plt.plot(listN, listQ, 'm')
    plt.xlabel('N')
    plt.ylabel('Carga total (C)')
    plt.title('Carga total aproximada obtida com diferentes valores de N')
    plt.show()
    fig.savefig(f"../imgs/carga/grafCarga")

def main():
    Q2()
    Q3()
    Q4()

if __name__ == "__main__":
    main()