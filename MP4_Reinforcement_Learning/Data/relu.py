import numpy as np

Z = np.array([
[1.3565476213, 1.45771394424, 1.50109965789, 1.52996162149],
[1.46507229855, 0.154860821512, 0.815361956687, 1.04652279418],
[2.26219902, 1.79451057522, 2.93034410997, 1.3123696034],
[0.236827022288, 0.235670995932, 0.818587410666, -0.388271700598],
[0.817747243124, 0.497036862725, 1.68708708207, 0.79114179937],
[0.767800816841, -1.05707251906, 0.453867861946, -0.336912607238],
[0.229776388413, -1.06142232183, 0.233607024277, -1.48127943772],
[-0.600774727804, -0.868839796371, -0.870867878022, -0.762964836374],
[0.693232976094, 0.280523916818, 1.11132084879, -0.0493649852366],
[0.234454074768, -0.642654040537, -0.630474086786, -0.384635229845]])

A = np.array([
[1.3565476213, 1.45771394424, 1.50109965789, 1.52996162149],
[1.46507229855, 0.154860821512, 0.815361956687, 1.04652279418],
[2.26219902, 1.79451057522, 2.93034410997, 1.3123696034],
[0.236827022288, 0.235670995932, 0.818587410666, 0.0],
[0.817747243124, 0.497036862725, 1.68708708207, 0.79114179937],
[0.767800816841, 0.0, 0.453867861946, 0.0],
[0.229776388413, 0.0, 0.233607024277, 0.0],
[0.0, 0.0, 0.0, 0.0],
[0.693232976094, 0.280523916818, 1.11132084879, 0.0],
[0.234454074768, 0.0, 0.0, 0.0]])

dA = np.array([
[0.61463791745, 0.138201477229, -0.185633405548, -0.86166600909],
[0.394857546289, -0.0929146346439, 0.444111198941, 0.732764651857],
[0.951043010006, 0.711606684785, -0.97657183163, -0.280043871043],
[0.459981124848, -0.656740645477, 0.0420732124083, -0.891324023321],
[-0.600006950207, -0.962956411079, 0.587395406715, -0.552150623879],
[-0.309296638606, 0.856162586931, 0.408828803847, -0.936322140937],
[-0.670611687004, 0.242956803, 0.154457177208, -0.524214357251],
[0.86842799585, 0.227931911932, 0.0712656060499, 0.179819952709],
[0.460244059034, -0.376110009041, -0.203557875568, -0.58031250205],
[-0.627613988239, 0.888744779968, 0.479101590099, -0.0190823827649]])

dZ = np.array([
[0.61463791745, 0.138201477229, -0.185633405548, -0.86166600909],
[0.394857546289, -0.0929146346439, 0.444111198941, 0.732764651857],
[0.951043010006, 0.711606684785, -0.97657183163, -0.280043871043],
[0.459981124848, -0.656740645477, 0.0420732124083, -0.0],
[-0.600006950207, -0.962956411079, 0.587395406715, -0.552150623879],
[-0.309296638606, 0.0, 0.408828803847, -0.0],
[-0.670611687004, 0.0, 0.154457177208, -0.0],
[0.0, 0.0, 0.0, 0.0],
[0.460244059034, -0.376110009041, -0.203557875568, -0.0],
[-0.627613988239, 0.0, 0.0, -0.0]])