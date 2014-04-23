#!/usr/bin/python3.3
# coding=utf-8
"""
Module for PSO clustering.
"""
__author__ = 'Hossein Noroozpour Thany Abady'
import numpy
from random import random as rand
import sys


class PSO():
    """
    Class for PSO.
    """
    def __init__(self, n_clusters=100, n_particles=100, n_iterations=100, w=0.6, wg=1.6, wp=0.6):
        self.n_particles = n_particles
        self.n_iterations = n_iterations
        self.n_clusters = n_clusters
        self.w = w
        self.wg = wg
        self.wp = wp

    def fit(self, x):
        """
        :param x:
        """
        class Particle():
            """
            Particle in PSO.
            """
            def __init__(self, attributes_minimums, attributes_limits, n_clusters, number_attributes, w, wp, wg):
                init_clusters = []
                init_velocity = []
                for j in range(n_clusters):
                    init_clusters.append([rand() * attributes_limits[k] + attributes_minimums[k]
                                          for k in range(number_attributes)])
                    init_velocity.append([(rand() - 0.5) * 2 * attributes_limits[k] + attributes_minimums[k]
                                          for k in range(number_attributes)])
                self.current_position = numpy.array(init_clusters)
                self.velocity = numpy.array(init_velocity)
                self.local_best_known_position = numpy.array(init_clusters)
                self.last_fitness = sys.float_info.max
                self.w = w
                self.wp = wp
                self.wg = wg

            def fitness(self, data):
                """
                :param data:
                :return:
                """
                fitness = 0.0
                for d in data:
                    vectors = self.current_position - d
                    distances = numpy.array([numpy.linalg.norm(v) for v in vectors])
                    fitness += distances.min()
                if self.last_fitness > fitness:
                    self.local_best_known_position = numpy.array(self.current_position)
                    self.last_fitness = fitness
                return fitness

            def update(self, global_best_known_position):
                # update velocity ######################################################################################
                """
                :param global_best_known_position:
                """
                self.velocity = self.velocity * self.w + self.local_best_known_position * self.wp + \
                    global_best_known_position * self.wg
                self.current_position += self.velocity

        n_attributes = len(x[0])
        train = numpy.array(x, copy=False)
        # creating clusters ############################################################################################
        minimums = [train[:, i].min() for i in range(n_attributes)]
        maximums = [train[:, i].max() for i in range(n_attributes)]
        limits = [maximums[i] - minimums[i] for i in range(n_attributes)]
        particles = []
        for i in range(self.n_particles):
            particles.append(Particle(minimums, limits, self.n_clusters, n_attributes))
        best_fitness = sys.float_info.max
        best_global_position = None
        for i in range(self.n_iterations):
            # best global position #####################################################################################
            for p in particles:
                particle_fitness = p.fitness(train)
                if best_fitness > particle_fitness:
                    best_fitness = particle_fitness
                    best_global_position = p.local_best_known_position
            # update velocity and move #################################################################################
