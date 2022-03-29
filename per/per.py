from itertools import *
import math

def func(x1, x2, x3, x4):
    x1 = True if x1 == 1 else False
    x2 = True if x2 == 1 else False
    x3 = True if x3 == 1 else False
    x4 = True if x4 == 1 else False
    f = (x1 or x2) and x3 or x4
    return f

def Tru_ta():
    print("x1 x2 x3 x4 f")
    for i in range(16):
        ib = bin(i)[2:].zfill(4)
        f = func(int(ib[0]), int(ib[1]), int(ib[2]), int(ib[3]))
        f = int(f)
        print("%1s" % (ib[0]),"%2s" % (ib[1]),"%2s" % (ib[2]),"%2s" % (ib[3]),"%2s" % (f))
    print()

class Perc():
    def __init__(self):
        self._n = 0.3
        self._w = [0.0, 0.0, 0.0, 0.0, 0.0]
       
    def tra_net(self, ib):
        net = self._w[0]
        for j in range(4):
            net += self._w[j + 1] * float(ib[j])
        if net >= 0:
            return 1
        else:
            return 0

    def log_net(self, ib):
        net = self._w[0]
        for j in range(4):
            net += self._w[j + 1] * float(ib[j])
        Fnet = 1/2*(math.tanh(net)+1)
        Dnet =  1-(1/(2*math.cos(net)*math.cos(net)))
        if Fnet >= 0.5:
            return 1, Dnet
        else:
            return 0, Dnet
    
    def Edu(self, activ):
        if activ == 'threshold':
            fuc_act = 0 
        elif activ == 'logic':
            fuc_act = 1 
        val = [] 
        Err = 1
        k = 0 
        print('k                   w                                    y                           Err')
        while Err != 0:
            if k > 50: 
                return False
            Err = 0
            print("%1s" % (str(k) + '  '), "%30s" % (str(self._w) + ' '), end='')
            for i in range(16):
                ib = bin(i)[2:].zfill(4)
                value = func(int(ib[0]), int(ib[1]), int(ib[2]), int(ib[3]))
                if fuc_act == 0:
                    y = self.tra_net(ib)
                    Dnet = 1
                else:
                    y, Dnet = self.log_net(ib)
                delta = int(value) - y
                val.append(y)
                if delta == 0:
                    continue
                else:
                    Err += 1
                    self._w[0] = self._w[0] + self._n * delta * Dnet
                    self._w[0] = round(self._w[0], 3)
                    for j in range(1, 5):
                        self._w[j] = self._w[j] + self._n * delta * float(ib[j - 1]) * Dnet
                        self._w[j] = round(self._w[j], 3)
            print("%50s" % (str(val) + ' '), "%1s" % (str(Err)))
            val = []
            k += 1

    def Min_edu(self, c, activ):
        if activ == 'threshold':
            fuc_act = 0
        elif activ == 'logic':
            fuc_act = 1
        self._w = [0.0, 0.0, 0.0, 0.0, 0.0]
        val = []
        k = 0
        Err = 1 
        ErSt = '  k                        w                              y           Err \n'
        while Err != 0:
            if k > 50:
                return False
            Err = 0
            ErSt += '{:>4}'.format(str(k) ) + '{:>41}'.format(str(self._w) )
            for i in c:
                ib = bin(i)[2:].zfill(4)
                value = func(int(ib[0]), int(ib[1]), int(ib[2]), int(ib[3]))
                if fuc_act == 0:
                    y = self.tra_net(ib)
                    Dnet = 1
                else:
                    y, Dnet = self.log_net(ib)
                delta = int(value) - y
                val.append(y)
                if delta == 0:
                    continue
                else:
                    Err += 1
                    self._w[0] = self._w[0] + self._n * delta * Dnet
                    self._w[0] = round(self._w[0], 3)
                    for j in range(1, 5):
                        self._w[j] = self._w[j] + self._n * delta * float(ib[j - 1]) * Dnet
                        self._w[j] = round(self._w[j], 3)
            ErSt += '{:>20}'.format(str(val) ) + '{:>7}'.format(str(Err) + '\n')
            val = []
            k += 1
        for i in range(16): # тестирование нейрона на всех возможных комбинациях входных значений
            ib = bin(i)[2:].zfill(4)
            value = func(int(ib[0]), int(ib[1]), int(ib[2]), int(ib[3]))
            if fuc_act == 0:
                y = self.tra_net(ib)
            else:
                y, Dnet = self.log_net(ib)
            if y == value:
                continue
            else:
                return False # нейрон не обучен
        print(ErSt)
        return True # нейрон обучен

    def min_s(self, activ):
        c = []
        vec = []
        jb = ''
        print('\n Min' + activ.upper())
        for i in range(16):
            vec.append(i)
        # перебор всех сочитаний без повторений для выявления минимальной комбинации векторов
        for i in range(3, 16):
            for j in combinations(vec, i):
                cor = self.Min_edu(j, activ)
                if cor == True:
                    jb = 'Min - '
                    for x in range(len(j)):
                        jb += str(bin(j[x])[2:].zfill(4)) + ', '
                    return jb[:-2]
        return 0

Tru_ta()
print(Perc().Edu('threshold'))
print(Perc().Edu('logic'))
print(Perc().min_s('threshold'))
print(Perc().min_s('logic'))
