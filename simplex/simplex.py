import numpy as np

class Simplex:
  def __init__(self, cr, cb, R, B, b):
    self.cr = cr
    self.cb = cb
    self.R = R
    self.B = B
    self.b = b
    self.fo = 0

  def verificar_solucao(self):
    menorCoeficiente = min(self.cr)
    
    if menorCoeficiente >= 0: 
      return None
    else:        
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

  def calcular_fo(self):
    B = np.array(self.B)
    Binv = np.linalg.inv(B)
    cb = np.array(self.cb)
    b = np.array(self.b)
    mult1 = np.dot(cb, Binv)
    newfo = np.dot(mult1, b)
    self.fo =  newfo
    
  def run(self):
    self.organizar_tableu()
    self.calcular_fo()


sim = Simplex([-20, -24], [0, 0], [[3, 6],[4, 2]], [[1,0],[0,1]], [60, 32])
sim.run()
print(sim.cr)
print('')
print(sim.b)
print(sim.R)
print('')
print(sim.fo)