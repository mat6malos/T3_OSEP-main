class OptimizarFinal:
    
    def __init__(self, P, S, Cs, a , b , c):
        self.P          = P
        self.S          = S
        self.Cs         = Cs
        self.a          = a
        self.b          = b
        self.c          = c
        self.FO         = self.GFO()
        
    def GFO(self):
        # Realizar la multiplicación fila por fila
        Cs_S = []
        for i in range(len(self.Cs)):
            # Multiplicar cada fila por el valor correspondiente del vector fila
            nueva_fila = [self.Cs[i] * self.S[i][t] for t in range(len(self.S[0]))]
            Cs_S.append(nueva_fila)
        P_b  = []
        for i in range(len(self.P)):
            # Multiplicar cada fila por el valor correspondiente del vector fila
            nueva_fila = [self.b[i] * self.P[i][t] for t in range(len(self.P[0]))]
            P_b.append(nueva_fila)
        P2 = [[var * var for var in fila] for fila in self.P]
        P2_c = []
        for i in range(len(self.P)):
            # Multiplicar cada fila por el valor correspondiente del vector fila
            nueva_fila = [self.c[i] * P2[i][t] for t in range(len(P2[0]))]
            P2_c.append(nueva_fila)
        Fc = [[P_b[i][j] + P2_c[i][j] for j in range(len(P_b[0]))] for i in range(len(P_b))]
        Fcf = [[Fc[i][j] + self.a[i] for j in range(len(Fc[0]))] for i in range(len(Fc))]
        MFO = [[Fcf[i][j] + Cs_S[i][j] for j in range(len(Fcf[0]))] for i in range(len(Fcf))]
        FO = sum(sum(fila) for fila in MFO)
        return FO