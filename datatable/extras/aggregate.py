    #!/usr/bin/env python3
# © H2O.ai 2018; -*- encoding: utf-8 -*-
#   This Source Code Form is subject to the terms of the Mozilla Public
#   License, v. 2.0. If a copy of the MPL was not distributed with this
#   file, You can obtain one at http://mozilla.org/MPL/2.0/.
#-------------------------------------------------------------------------------
from datatable import Frame
    
#@typed(n_bins=int,nx_bins=int,ny_bins=int)
def aggregate(self, epsilon=1.0e-15, n_bins=500, nx_bins=50, ny_bins=50, max_dimensions=50, seed=0):
    dt_agg = self._dt.aggregate(epsilon, n_bins, nx_bins, ny_bins, max_dimensions, seed)
    return Frame(dt_agg)

Frame.aggregate = aggregate