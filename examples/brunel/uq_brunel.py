import uncertainpy as un

from brunel_network_class import BrunelNetwork
from brunel_network_function import brunel_network

parameterlist = [["J_E", 4, None],
                 ["g", 4, None]]

parameters = un.Parameters(parameterlist)
parameters.setAllDistributions(un.Distribution(0.5).uniform)

# model = BrunelNetwork()
model = brunel_network

uncertainty = un.UncertaintyEstimation(model,
                                       parameters=parameters,
                                       features=None)

uncertainty.UQ(plot_condensed=False,
               plot_simulator_results=True)