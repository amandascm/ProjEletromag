import numpy as np
import math
from mpl_toolkits import mplot3d
import matplotlib.pyplot as plt
from matplotlib import cm

class Placa:
    def __init__(self, L = 0.1, N = 20, Vo = 1):
        # Parametros
        self.L = L # em metros
        self.N = N # numero natural par
        self.Vo = Vo # potencial em V

        # Matriz de tensao (um valor para cada centro de elemento quadrado, que são 3(N**2)/4 elementos)
        self.matTensao = np.ones(shape=((3*(N**2)//4),1)) * Vo

        # Coordenadas dos centros de cada quadrado obtido com discretizacao
        self.xCoords = []
        self.yCoords = []

        # Define a matriz de impedancia e as coordenadas dos centros de cada elemento de area
        self.discretCalcMatImped()

        # Define a matriz de amplitudes A
        self.calcAmp()
        self.zCoords = list(self.A.reshape((self.A.shape[0])))

    def plotDistCarga(self):
        # set up a figure twice as wide as it is tall
        fig = plt.figure(figsize=plt.figaspect(0.25))
        plt.title(f"Dist. superficial de carga aproximada com N = {self.N}, Vo = {self.Vo}V e L = {self.L}m")
        #===============
        #  First subplot (surface)
        ax = fig.add_subplot(1, 2, 1, projection='3d')
        surf = ax.plot_trisurf(self.xCoords, self.yCoords, self.zCoords, cmap=cm.jet, linewidth=0.1)
        fig.colorbar(surf, shrink=0.5, aspect=5)
        #===============
        # Second subplot (points)
        ax = fig.add_subplot(1, 2, 2, projection='3d')
        ax.scatter(self.xCoords,self.yCoords,self.zCoords, c="red")
        plt.show()
        fig.savefig(f"../imgs/distCarga/grafN{self.N}")

    def getCargaTotal(self):
        return np.sum(self.A * (self.L/self.N)**2)

    def calcAmp(self):
        matImpedInv = np.linalg.inv(self.matImped) # inversa da matriz de impedancia
        self.A = np.dot(matImpedInv, self.matTensao) # amplitudes   

    def discretCalcMatImped(self):
        N = self.N
        delta = self.L/N
        epsilon = 8.85*1e-12

        # a matriz de impedancia estabelece uma relacao de cada quadradinho com todos os outros, por isso tem dimensao 3(N**2)/4 x 3(N**2)/4
        matImped = np.ones(shape=((3*(N**2)//4),(3*(N**2)//4)))
        for m in range(matImped.shape[0]):
            if (m > (N*(N/2))):
                p = m%(N/2) + 1
                q = (N/2) + (m - (N*(N/2)))//(N/2) + 1
            else:
                p = m%N + 1
                q = m//N + 1

            xp = p * delta - delta/2
            yq = q * delta - delta/2

            self.xCoords += [xp]
            self.yCoords += [yq]

            for n in range(matImped.shape[1]):
                if (n > (N*(N/2))):
                    xiindex = n%(N/2) + 1
                    yjindex = (N/2) + (n - (N*(N/2)))//(N/2) + 1
                else:
                    xiindex = n%N + 1
                    yjindex = n//N + 1

                xi = xiindex * delta - delta/2
                yj = yjindex * delta - delta/2

                if m != n:
                    distPQtoIJ = math.sqrt((xp - xi)**2 + (yq - yj)**2)
                    matImped[m][n] = (1/(4 * math.pi * epsilon)) * ((delta**2)/distPQtoIJ)
                else:
                    matImped[m][n] = (delta/(math.pi * epsilon)) * np.log(1 + math.sqrt(2))
        self.matImped = matImped