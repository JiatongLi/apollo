#!/usr/bin/env python3

###############################################################################
# Copyright 2017 The Apollo Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###############################################################################

import matplotlib.pyplot as plt
from matplotlib import cm as cmx
from matplotlib import colors as mcolors


class TrajSpeedSubplot:
    def __init__(self, ax):
        self.ax = ax
        self.speed_lines = []
        self.speed_lines_size = 30
        self.colors = []
        self.init_colors()
        # self.colors = ['b','r', 'y', 'k']
        for i in range(self.speed_lines_size):
            line, = ax.plot(
                [0], [0],
                c=self.colors[i % len(self.colors)],
                ls="-",
                marker='',
                lw=3,
                alpha=0.8)
            self.speed_lines.append(line)

        ax.set_xlabel("t (second)")
        # ax.set_xlim([-2, 10])
        ax.set_ylim([-1, 25])
        self.ax.autoscale_view()
        # self.ax.relim()
        ax.set_ylabel("speed (m/s)")
        ax.set_title("PLANNING SPEED")
        self.set_visible(False)

    def init_colors(self):
        self.colors = []
        values = list(range(self.speed_lines_size))
        jet = plt.get_cmap('brg')
        color_norm = mcolors.Normalize(vmin=0, vmax=values[-1])
        scalar_map = cmx.ScalarMappable(norm=color_norm, cmap=jet)
        for val in values:
            color_val = scalar_map.to_rgba(val)
            self.colors.append(color_val)

    def set_visible(self, visible):
        for line in self.speed_lines:
            line.set_visible(visible)

    def show(self, planning):
        planning.traj_data_lock.acquire()
        for i in range(len(planning.traj_speed_t_history)):
            if i >= self.speed_lines_size:
                print("WARNING: number of path lines is more than " \
                      + str(self.speed_lines_size))
                continue
            speed_line = self.speed_lines[self.speed_lines_size - i - 1]

            speed_line.set_xdata(planning.traj_speed_t_history[i])
            speed_line.set_ydata(planning.traj_speed_v_history[i])
            # speed_line.set_xdata([1,2,3,4])
            # speed_line.set_ydata([1,2,3,4])
            # speed_line.set_label(name[0:5])
            speed_line.set_visible(True)

        # self.ax.legend(loc="upper left", borderaxespad=0., ncol=5)
        # self.ax.axis('equal')
        planning.traj_data_lock.release()
        self.ax.autoscale_view()
        self.ax.relim()
