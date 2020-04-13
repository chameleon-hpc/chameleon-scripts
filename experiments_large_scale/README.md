# Large-Scale Experiments - Power Consumption

The following experiments are conducted to measure the power consumption behavior for baseline and Chameleon versions with respect to the higher communication overhead.

## Robustness against hardware variation (imbalances caused by hardware)

* Experiment 1: MxM Example - Check for manufacturing variations
  * Equal load distribution (every ranks has to compute N MxM calculations)
  * Varying number of nodes / processes
  * Varying power cap from 105W (no powercap) to 60W (min recommended value)

* Experiment 2: MxM Example - Frequency Manipulation (constant)
  * Equal load distribution (every ranks has to compute N MxM calculations)
  * Varying number of nodes / processes
  * Varying number of slow nodes with constant frequency (from 1.2 GHz to 2.2 GHz)  up to 25% or 50% of total nodes or similar

* Experiment 3: MxM Example - Frequency Manipulation (round robin)
  * Equal load distribution (every ranks has to compute N MxM calculations)
  * Varying number of nodes / processes
  * Option1: Single slow node that is changing very 100 ms (from 1.2 GHz to 2.2 GHz)
  * Option2: Multiple slow nodes that are changing very 100 ms (from 1.2 GHz to 2.2 GHz)

## Robustness against software variation (imbalances caused by e.g. AMR or similar)

* Experiment 4: MxM Example - Unbalanced
  * Unequal load distribution (linear distribution from min to max according to number of nodes/processes involved)
  * Varying number of nodes / processes
  * No frequency manipulation or power cap

* Experiment 5: sam(oa)^2
  * Tohoku scenario
  * Tests in combination with and without CCP with a reasonable number of iterations
  * Varying number of nodes / processes 
  * 16 or 20 sections per thread

## Both

* Experiment 6: sam(oa)^2 + Power capping
  * Tohoku scenario
  * Tests in combination with and without CCP with a reasonable number of iterations
  * 16 or 20 sections per thread
  * Varying number of nodes / processes
  * Varying power cap from 105W (no powercap) to 60W (min recommended value)

## For all experiments:

* Run each experiment with and without Chameleon (each 5 times)
* Measure power consumption of complete rack (nodes + switches separately)
* Runs with less that 64 nodes: Idle nodes will be turned off completely to avoid corruption of power measurement due to idle power draw

## Open questions:

* Does it make sense to power cap just a few nodes? (I don't think so)
* What is an appropriate problem size for MxM example
  * I will figure it out (should be at least 20 seconds)
* Do we need to repeat frequency tests with sam(oa)^2
* Bo:
  * What is the min recommended value for Powercap?
  * Does it make sense to also set min freq?
  * Are the additional services deactivated on all nodes (likwid + telegraf)
  * Stability of the powermeter?
  * Need to test new python client with redirecting