import matplotlib.pyplot as plt

def plot_k4():
    x = [6, 7, 8, 30, 35, 40, 54, 63, 72]
    bound = [6.7, 7.3, 7.8, 22.5, 25.8, 28.6, 33.1, 37.6, 43.3]
    random = [6.4, 7.5, 8.7, 21.6, 25.5, 28.6, 32.8, 38.3, 43.7]
    pso = [4.7, 5.8, 6.9, 18.4, 22.1, 24.6, 28.7, 33.5, 38.1] 
    dsatur = [3.7, 4.7, 5.7, 17.6, 21.3, 23.5, 28.7, 33.5, 38.0]
    plt.plot(x, bound, '-hk', mfc='none', label='Cota')
    plt.plot(x, random, '-^r', label='Aleatorio')
    plt.plot(x, pso, '-xg', label='PSO')
    plt.plot(x, dsatur, '-ob', label='DSATUR')
    plt.ylabel('$T_{4}(G, W)$')
    plt.xlabel('np')
    plt.legend(loc='upper left')
    plt.show()

def plot_k6():
    x = [6, 7, 8, 30, 35, 40, 54, 63, 72]
    bound = [5.2, 5.6, 6.5, 17.5, 19.2, 22.3, 25.3, 29.3, 34.1]
    random = [5.4, 5.9, 7.1, 17.3, 19.7, 22.5, 26.0, 30.3, 34.3]
    pso = [3.6, 4.2, 5.2, 13.8, 16.2, 18.5, 21.5, 25.2, 28.8]
    dsatur = [2.2, 2.7, 3.5, 12.4, 14.5, 16.8, 21.4, 25.0, 28.5]
    plt.plot(x, bound, '-hk', mfc='none', label='Cota')
    plt.plot(x, random, '-^r', label='Aleatorio')
    plt.plot(x, pso, '-xg', label='PSO')
    plt.plot(x, dsatur, '-ob', label='DSATUR')
    plt.ylabel('$T_{6}(G, W)$')
    plt.xlabel('np')
    plt.legend(loc='upper left')
    plt.show()

def plot_k11():
    x = [6, 7, 8, 30, 35, 40, 54, 63, 72]
    bound = [3.2, 3.7, 4.0, 10.4, 12.2, 13.3, 15.4, 17.8, 20.8]
    random = [3.9, 4.5, 4.9, 11.4, 13.3, 15.0, 17.1, 19.7, 22.5]
    pso = [2.1, 2.6, 3.1, 8.7, 10.4, 11.7, 13.3, 15.7, 17.9]
    dsatur = [0.8, 1.0, 1.2, 6.7, 8.3, 9.3, 12.8, 15.2, 17.3]
    plt.plot(x, bound, '-hk', mfc='none', label='Cota')
    plt.plot(x, random, '-^r', label='Aleatorio')
    plt.plot(x, pso, '-xg', label='PSO')
    plt.plot(x, dsatur, '-ob', label='DSATUR')
    plt.ylabel('$T_{11}(G, W)$')
    plt.xlabel('np')
    plt.legend(loc='upper left')
    plt.show()

def plot_time():
    x = [6, 7, 8, 30, 35, 40, 54, 63, 72]
    k4 = [1000*3.7/4.5, 1000*4.6/5.9, 1000*5.4/7.5, 1000*7.8/7.3, 1000*10.2/9.7, 1000*12.8/12.5, 1000*11.8/10.4, 1000*15.7/14.1, 1000*20.1/18.0]
    k6 = [1000*3.8/4.7, 1000*4.5/6.2, 1000*5.5/8.0, 1000*7.9/8.1, 1000*10.2/11.1, 1000*12.7/14.1, 1000*11.9/12.2, 1000*15.9/16.5, 1000*20.0/21.3]
    k11 = [1000*3.8/5.4, 1000*4.6/7.1, 1000*5.6/9.1, 1000*8.0/10.8, 1000*10.4/14.5, 1000*13.2/18.7, 1000*12.1/16.4, 1000*16.4/22.4, 1000*20.7/29.0]
    plt.plot(x, k4, '-h', mfc='none', label='k = 4')
    plt.plot(x, k6, '-x', label='k = 6')
    plt.plot(x, k11, '-o', label='k = 11')
    plt.ylabel('$t_{PSO}/t_{TSC-DSATUR}$')
    plt.xlabel('np')
    plt.legend(loc='upper rigth')
    plt.show()

def plot_k4_():
    x = [6,  7, 8, 18, 21, 24, 30, 35, 40, 42, 49, 54, 56, 63, 72]
    dsatur = [4.2,  4.9, 5.5, 11.1, 12.8, 14.8, 17.7, 20.7, 23.3, 23.6, 27.4, 28.7, 31.5, 33.3, 38.0]
    mna = [3.9, 4.9, 5.5, 11.2, 12.7, 15.0, 17.6, 19.9, 22.8, 23.8, 27.5, 28.4, 31.2, 33.1, 37.9]
    swo_ss = [4.0,  4.4, 5.1, 10.3, 12.0, 14.5, 17.2, 19.6, 22.3, 22.4, 25.9,  27.6, 29.7, 32.3, 37.0]
    bfs = [4.1,  4.9, 5.6, 11.3, 12.7, 14.7, 17.6, 20.6, 23.4, 23.6, 27.3, 28.6, 31.5, 33.3, 38.0]
    plt.plot(x, bfs, '-^r', label='BFS-degree')
    plt.plot(x, mna, '-xg', label='Mezcla de no adyacentes')
    plt.plot(x, dsatur, '-ob', label='DSATUR')
    plt.plot(x, swo_ss, '-hk', label='SWO+BS')
    plt.ylabel('$T_{4}(G, W)$')
    plt.xlabel('np')
    plt.legend(loc='upper left')
    plt.show()

def plot_k6_():
    x = [6, 30, 54, 7, 35, 63, 8, 40, 72]
    mna = [3.9, 17.6, 28.4, 4.9, 19.9, 33.1, 5.5, 22.8, 37.9]
    dsatur = [2.3, 2.9, 3.3, 12.5, 14.8, 16.8, 21.2, 24.8, 28.4]
    plt.plot(x, vm, '-^r', label='Mezcla de Vertices')
    plt.plot(x, am, '-xg', label='Mezcla de no adyacentes')
    plt.plot(x, dsatur, '-ob', label='DSATUR')
    plt.ylabel('$T_{6}(G, W)$')
    plt.xlabel('np')
    plt.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    

    # plot para k=4
    plot_k4_()

    # plot para k=6
    # plot_k6_()
    
    # plot para k=11
    # plot_k11()

    # plot_time()