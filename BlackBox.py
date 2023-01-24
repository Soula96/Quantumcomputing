# -*- coding: utf-8 -*-
"""
Created on Wed Nov 23 17:43:22 2022

@author: MaxPr
"""
import numpy as np
from qiskit import QuantumCircuit, transpile
from qiskit.providers.aer import QasmSimulator
from qiskit.visualization import plot_histogram

def DJBlackBox(case, n):
    BlackBoxCircuit = QuantumCircuit(n+1)
    if(case == 'balanced'):
        b = np.random.randint(1, 2**n)
        """
        Formatiere b als binären String mit Nullen aufgefüllt
        """
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
        output = np.random.randint(2)
        if output == 1:
            BlackBoxCircuit.x(n)
    BlackBoxGate = BlackBoxCircuit.to_gate()
    BlackBoxGate.name = "Black Box"
    BlackBoxCircuit.draw(output='mpl')
    return BlackBoxGate
def DJAlgorithm(BlackBox, n):
    DJCircuit = QuantumCircuit(n+1, n)
    DJCircuit.x(n)
    for qubit in range(n+1):
        DJCircuit.h(qubit)
    DJCircuit.append(BlackBox, range(n+1))
    for qubit in range(n):
        DJCircuit.h(qubit)
    for i in range(n):
        DJCircuit.measure(i,i)
    return DJCircuit

n = 3
BBGate = DJBlackBox('balanced', n)
DJCircuit = DJAlgorithm(BBGate, n)
DJCircuit.draw(output='mpl')
    
        