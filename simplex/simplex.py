'''
algoritimo do simplex revisado para a disciplina de programação linear


ainda falta alguns ajustes pra fazer mas ja esta funcional 

'''

import numpy as np
import copy

class Simplex:
  def __init__(self, cr, cb, R, B, b):
    self.cr = cr
    self.cb = cb
    self.R = R
    self.B = B
    self.b = b
    self.fo = 0
    self.index = []

  def verificar_solucao(self):
    menorCoeficiente = min(self.cr)    
    if menorCoeficiente >= 0: 
      return None
    else:        
      self.index.append(self.cr.index(menorCoeficiente))
      return self.cr.index(menorCoeficiente)

  def pivotamento(self):
    cr = np.array(self.cr)
    cb = np.array(self.cb)
    B = np.array(self.B)
    R = np.array(self.R)
    invB = np.linalg.inv(B)
    resultmult = np.dot(invB, R)
    resultmult2 = np.dot(cb, resultmult)
    newcr = np.subtract(cr, resultmult2)   
    for i in range(len(self.cr)):
      self.cr[i] = newcr[i] 
    b = np.array(self.b)
    newb = np.dot(invB, b)
    for i in range(len(self.b)):
      self.b[i] = newb[i]
    newR = np.dot(invB, R)
    for i in range(len(self.R)):
      for j in range(len(self.R[i])):
        self.R[i][j] = newR[i][j]


  def organizar_tableu(self):
    index = self.verificar_solucao()
    if index == None:
      return
    p = 99999999
    sai = None
    for i in range(len(self.R)):
      if p > self.b[i]/self.R[i][index]:
        p = self.b[i]/self.R[i][index]
        sai = i
    for i in range(len(self.R)):
      aux = self.R[i][index]
      self.R[i][index] = self.B[i][sai]
      self.B[i][sai] = aux
    aux2 = self.cr[index]
    self.cr[index] = self.cb[sai]
    self.cb[sai] = aux2
    self.pivotamento()
    self.organizar_tableu()

  def tablou_final(self, index):    
    p = 99999999
    for i in range(len(self.R)):
      if p > self.b[i]/self.R[i][index]:
        p = self.b[i]/self.R[i][index]
    for i in range(len(self.R)):
      aux = self.R[i][index]
      self.R[i][index] = self.B[i][index]
      self.B[i][index] = aux
    aux2 = self.cr[index]
    self.cr[index] = self.cb[index]
    self.cb[index] = aux2

  def calcular_fo(self):
    B = np.array(self.B)
    Binv = np.linalg.inv(B)
    cb = np.array(self.cb)
    b = np.array(self.b)
    mult1 = np.dot(cb, Binv)
    newfo = np.dot(mult1, b)
    self.fo =  newfo
    
  def run(self):
    aux = copy.deepcopy(self)
    aux.organizar_tableu()
    self.index = aux.index

    self.index.sort()
    for i in self.index:
      self.tablou_final(i)
 
    self.calcular_fo()
    self.pivotamento()
    for i in range(len(self.cr)):
      self.cr[i] = 0

'''
exemplo

fo = Max 20x1 + 24x2

3x1 + 6x2 ≤ 60
4x1 + 2x2 ≤ 32
x1, x2 ≥ 0

forma padrão

Min - 20x1- 24x2 - 0x3  0x4
3x1 + 6x2 + 1x3 + 0x4 = 60
4x1 + 2x2 + 0x3 + 1x4 = 32
x1, x2, x3, x4 ≥ 0

'''
'''         informar função objetivo, lista com os valores de fora da base e outra com os valores de dentro     informar restrições           '''
sim = Simplex([-20, -24], [0, 0],                                                                              [[3, 6],[4, 2]], [[1,0],[0,1]], [60, 32])
sim.run()
print(f'solução:  {sim.b}{sim.cr}')
print(f'\nresultado da fo:  {sim.fo}')
