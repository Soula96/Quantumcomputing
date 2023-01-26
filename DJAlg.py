# -*- coding: utf-8 -*-
"""
Created on Sat Nov 26 10:59:04 2022

@author: MaxPr
"""
import numpy as np
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, transpile, assemble
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram


#Problem von Deutsch: Anzahl der Eingabebits=1 
# im Deutsch-Josza Algorithmus

def BlackBox(case, n):
    BlackBoxCircuit = QuantumCircuit(n+1)
    if (case == 'balanced'):
        """
        creates a rand int between 1 - 2**n -1
        format b as string, lead with 0s; format with the length of n
        use binary representation
        """
        b = np.random.randint(1, 2**n)  
        b_str = format(b, '0'+str(n)+'b') 
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                BlackBoxCircuit.x(qubit)
        for qubit in range(n):
            BlackBoxCircuit.cx(qubit, n)
        for qubit in range(len(b_str)):
            if b_str[qubit] == '1':
                BlackBoxCircuit.x(qubit)
    if (case == 'constant'):
        b = np.random.randint(2)
        if b == 1:
            BlackBoxCircuit.x(n)
    BlackBoxGate = BlackBoxCircuit.to_gate()
    BlackBoxGate.name = "Black Box"
    BlackBoxCircuit.draw(output='mpl')
    return BlackBoxGate

def DJAlg(BlackBox, n):
    DJCircuit = QuantumCircuit(n+1, n)
    DJCircuit.x(n)
    for qubit in range(n+1):
        DJCircuit.h(qubit)
    DJCircuit.append(BlackBox, range(n+1))
    for qubit in range(n):
        DJCircuit.h(qubit)
    for i in range(n):
        DJCircuit.measure(i, i)
    return DJCircuit

n = 4
BBGate = BlackBox('constant', n)
DJ = DJAlg(BBGate, n)
DJ.draw(output='mpl')

simulator = QasmSimulator()
CompiledCircuit = transpile(DJ, simulator)
job = simulator.run(CompiledCircuit, shots=1000)
result = job.result()
counts = result.get_counts(CompiledCircuit)
plot_histogram(counts)



        
  