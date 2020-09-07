import matplotlib.pyplot as plt

# def plot_k4():
#     x = [6, 7, 8, 30, 35, 40, 54, 63, 72]
#     bound = [6.7, 7.3, 7.8, 22.5, 25.8, 28.6, 33.1, 37.6, 43.3]
#     random = [6.4, 7.5, 8.7, 21.6, 25.5, 28.6, 32.8, 38.3, 43.7]
#     pso = [4.7, 5.8, 6.9, 18.4, 22.1, 24.6, 28.7, 33.5, 38.1] 
#     dsatur = [3.7, 4.7, 5.7, 17.6, 21.3, 23.5, 28.7, 33.5, 38.0]
#     plt.plot(x, bound, '-hk', mfc='none', label='Cota')
#     plt.plot(x, random, '-^r', label='Aleatorio')
#     plt.plot(x, pso, '-xg', label='PSO')
#     plt.plot(x, dsatur, '-ob', label='DSATUR')
#     plt.ylabel('$T_{4}(G, W)$')
#     plt.xlabel('np')
#     plt.legend(loc='upper left')
#     plt.show()

# def plot_k6():
#     x = [6, 7, 8, 30, 35, 40, 54, 63, 72]
#     bound = [5.2, 5.6, 6.5, 17.5, 19.2, 22.3, 25.3, 29.3, 34.1]
#     random = [5.4, 5.9, 7.1, 17.3, 19.7, 22.5, 26.0, 30.3, 34.3]
#     pso = [3.6, 4.2, 5.2, 13.8, 16.2, 18.5, 21.5, 25.2, 28.8]
#     dsatur = [2.2, 2.7, 3.5, 12.4, 14.5, 16.8, 21.4, 25.0, 28.5]
#     plt.plot(x, bound, '-hk', mfc='none', label='Cota')
#     plt.plot(x, random, '-^r', label='Aleatorio')
#     plt.plot(x, pso, '-xg', label='PSO')
#     plt.plot(x, dsatur, '-ob', label='DSATUR')
#     plt.ylabel('$T_{6}(G, W)$')
#     plt.xlabel('np')
#     plt.legend(loc='upper left')
#     plt.show()

# def plot_k11():
#     x = [6, 7, 8, 30, 35, 40, 54, 63, 72]
#     bound = [3.2, 3.7, 4.0, 10.4, 12.2, 13.3, 15.4, 17.8, 20.8]
#     random = [3.9, 4.5, 4.9, 11.4, 13.3, 15.0, 17.1, 19.7, 22.5]
#     pso = [2.1, 2.6, 3.1, 8.7, 10.4, 11.7, 13.3, 15.7, 17.9]
#     dsatur = [0.8, 1.0, 1.2, 6.7, 8.3, 9.3, 12.8, 15.2, 17.3]
#     plt.plot(x, bound, '-hk', mfc='none', label='Cota')
#     plt.plot(x, random, '-^r', label='Aleatorio')
#     plt.plot(x, pso, '-xg', label='PSO')
#     plt.plot(x, dsatur, '-ob', label='DSATUR')
#     plt.ylabel('$T_{11}(G, W)$')
#     plt.xlabel('np')
#     plt.legend(loc='upper left')
#     plt.show()

# def plot_time():
#     x = [6, 7, 8, 30, 35, 40, 54, 63, 72]
#     k4 = [1000*3.7/4.5, 1000*4.6/5.9, 1000*5.4/7.5, 1000*7.8/7.3, 1000*10.2/9.7, 1000*12.8/12.5, 1000*11.8/10.4, 1000*15.7/14.1, 1000*20.1/18.0]
#     k6 = [1000*3.8/4.7, 1000*4.5/6.2, 1000*5.5/8.0, 1000*7.9/8.1, 1000*10.2/11.1, 1000*12.7/14.1, 1000*11.9/12.2, 1000*15.9/16.5, 1000*20.0/21.3]
#     k11 = [1000*3.8/5.4, 1000*4.6/7.1, 1000*5.6/9.1, 1000*8.0/10.8, 1000*10.4/14.5, 1000*13.2/18.7, 1000*12.1/16.4, 1000*16.4/22.4, 1000*20.7/29.0]
#     plt.plot(x, k4, '-h', mfc='none', label='k = 4')
#     plt.plot(x, k6, '-x', label='k = 6')
#     plt.plot(x, k11, '-o', label='k = 11')
#     plt.ylabel('$t_{PSO}/t_{TSC-DSATUR}$')
#     plt.xlabel('np')
#     plt.legend(loc='upper rigth')
#     plt.show()

def plot_times_k4():
    x = [6, 8, 10, 30, 40, 50, 54, 72, 90]
    bound = [3.2, 3.7, 4.0, 10.4, 12.2, 13.3, 15.4, 17.8, 20.8]
    dsatur = [5, 11, 11, 7, 13, 19, 14, 23, 30]
    bfs = [1, 3, 3, 4, 7, 11, 9, 14, 19]
    dbfs = [3, 7, 8, 6, 11, 16, 11, 19, 25]
    vm = [5, 11, 12, 7, 14, 21, 13, 23, 31]
    swo = [47, 106, 116, 126, 232, 342, 276, 470, 632] 
    # plt.plot(x, bound, '-hk', mfc='none', label='Cota')
    plt.plot(x, dsatur, '-ob', label='DSATUR')
    plt.plot(x, bfs, '-hk', label='BFS')
    plt.plot(x, dbfs, '-^r', label='Deg-BFS')
    plt.plot(x, vm, '-xg', label='VM')
    plt.plot(x, swo, '-xg', label='SWO')
    # plt.plot(x, dsatur, '-ob', label='DSATUR')
    # plt.plot(x, dsatur, '-ob', label='DSATUR')
    plt.ylabel('$T_{11}(G, W)$')
    plt.xlabel('np')
    plt.legend(loc='upper left')
    plt.show()

def plot_k4():
    x = [6, 8, 10, 30, 40, 50, 54, 72, 90]
    # bound = [3.2, 3.7, 4.0, 10.4, 12.2, 13.3, 15.4, 17.8, 20.8]
    dsatur = [4.0, 5.1, 6.4, 16.7, 22.2, 28.1, 28.2, 37.5, 46.8]
    bfs = [4.4, 5.6, 7.0, 17.0, 22.9, 28.8, 28.0, 37.5, 46.7]
    dbfs = [4.0, 5.1, 6.3, 16.6, 22.1, 27.9, 28.2, 37.5, 46.8]
    vm = [4.1, 5.2, 6.4, 16.5, 21.8, 28.0, 28.0, 37.3, 46.7]
    swo = [3.7, 4.7, 5.9, 15.8, 21.4, 26.9, 27.9, 37.2, 46.6] 
    # plt.plot(x, bound, '-hk', mfc='none', label='Cota')
    plt.plot(x, dsatur, '-ob', label='DSATUR')
    plt.plot(x, bfs, '-hk', label='BFS')
    plt.plot(x, dbfs, '-^r', label='Deg-BFS')
    plt.plot(x, vm, '-2g', label='VM')
    plt.plot(x, swo, '-xy', label='SWO')
    # plt.plot(x, dsatur, '-ob', label='DSATUR')
    # plt.plot(x, dsatur, '-ob', label='DSATUR')
    plt.ylabel('$T_{11}(G, W)$')
    plt.xlabel('np')
    plt.legend(loc='upper left')
    plt.show()

if __name__ == "__main__":
    

    # plot para k=4
    # plot_k4_()

    # plot para k=6
    # plot_k6_()
    
    # plot para k=11
    # plot_k11()

    plot_k4()