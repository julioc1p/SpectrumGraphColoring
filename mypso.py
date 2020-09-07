import random
import numpy as np 


class MyPSO():

    def __init__(self, n_particles, dim, bounds):
        self.n_particles = n_particles
        self.dim = dim
        self.min = bounds[0]
        self.max = bounds[1]
        self.init_particles()
   
    def init_particles(self, fun=None, *args, **kargs):
        self.particles = np.random.uniform(self.min, self.max, (self.n_particles, self.dim))
        self.gbest_value = float('inf')
        self.gbest_position = np.array([random.random()*self.dim, random.random()*self.dim])
        self.velocities = np.zeros((self.n_particles, self.dim))
        pbest_value = [0]*self.n_particles
        pbest_position = [0]*self.n_particles
        for i in range(self.n_particles):
            particle = self.particles[i]
            pbest_position[i] = particle
            if fun is not None:
                pbest_value[i] = fun(particle, *args, **kargs)
            else:
                self.pbest_value = float('inf')
        self.pbest_value = np.array(pbest_value)
        self.pbest_position = np.array(pbest_position)

    def minimize(self, fun, n_iters, w, c1, c2, *args, **kargs):
        self.init_particles(fun, *args, **kargs)
        iters = 0
        while iters < n_iters:
            # pbest loop
            for i in range(self.n_particles):
                particle = self.particles[i]
                fitness_cadidate = fun(particle, *args, **kargs)
                if fitness_cadidate < self.pbest_value[i] :
                    self.pbest_value[i] = fitness_cadidate
                    self.pbest_position[i] = particle
            # gbest loop
            for i in range(self.n_particles):
                particle = self.particles[i]
                best_fitness_cadidate = self.pbest_value[i]
                if best_fitness_cadidate < self.gbest_value:
                    self.gbest_value = best_fitness_cadidate
                    self.gbest_position = particle
            # move loop
            for i in range(self.n_particles):
                particle = self.particles[i]
                new_velocity = (w*self.velocities[i]) + (c1*random.random()) * (self.pbest_position[i] - particle) + \
                            (c2*random.random()) * (self.gbest_position - particle)
                new_particle = particle + new_velocity
                self.try_move(particle, new_particle)
                self.particles[i] = new_particle
                self.velocities[i] = new_velocity
            iters+=1
        return self.gbest_value, self.gbest_position

    def try_move(self, particle, new_particle):
        for i in range(self.dim):
            if new_particle[i] >= self.max or new_particle[i] < self.min:
                new_particle[i] = particle[i]
            

# search_space = Space(1, target_error, n_particles)
# particles_vector = [Particle() for _ in range(search_space.n_particles)]
# search_space.particles = particles_vector
# search_space.print_particles()

# iteration = 0
# while(iteration < n_iterations):
#     search_space.set_pbest()    
#     search_space.set_gbest()

#     if(abs(search_space.gbest_value - search_space.target) <= search_space.target_error):
#         break

#     search_space.move_particles()
#     iteration += 1
    
# print("The best solution is: ", search_space.gbest_position, " in n_iterations: ", iteration)