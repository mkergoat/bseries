# bseries

1. [Short desciption](#short-description)
1. [Use](#use)
1. [Example](#example)
1. [Further use](#further-use)

## Short description
This code plots the open-water properties of Wageningen B-Series from data available in Bernitsas , *KT, KQ and efficiency curves for the Wageningen B-series propellers*  Departement of Naval Architecture and Marine Engineering, University of Michigan 1981

## Use
The code can be launched via a command prompt, typing python bseries.py.
You will have to provide pitch ratio (P/D) maximum and minimum and then the values of P/D will be computed using a step of 0.1, number of blades (Z) and expanded area ratio (EAR = Ae/A0) for the calculations to be performed.

Please note that the following restrictions apply: 2 <= Z <= 7, 0.30 <= Ae/A0 <= 1.05, 0.50 <= P/D <= 1.40.

The Reynolds number should also be provided to the code. A correction is then applied to the results (that have been obtained at a precise Reynolds number) so that they take into account the flow regime. 

## Example

In this part we will try to reproduce a figure from the reference cited above : the B4-40 (Z = 4, Ae/A0 = 0.40) for pitch ratios ranging from 0.5 to 1.4.

#TBD

## Further use
This code is used in a code that provides the autopropulsion point, given ship resistance. See (insert ref)
