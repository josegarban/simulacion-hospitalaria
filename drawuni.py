import main, clean
import pprint

from scipy.stats import uniform
import matplotlib.pyplot as plt
import numpy as np

def generationtest():

    fig, ax = plt.subplots(1, 1)

    mean, var, skew, kurt = uniform.stats(moments='mvsk')
    print(mean, var, skew, kurt)

    # numpy.linspace: generate a linear space of numbers
    # matplotlib.uniform.ppf: percent point function (inverse of cumulative distribution function — percentiles)
    x = np.linspace(uniform.ppf(0.01), uniform.ppf(0.99), 100)
    ax.plot(x, uniform.pdf(x), 'r-', lw=5, alpha=0.6, label='uniform pdf')

    rv = uniform()
    ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

    vals = uniform.ppf([0.001, 0.5, 0.999])
    test = np.allclose([0.001, 0.5, 0.999], uniform.cdf(vals))
    print(test)

    r = uniform.rvs(size=1000)

    ax.hist(r, density=True, histtype='stepfilled', alpha=0.2)
    ax.legend(loc='best', frameon=False)
    plt.show()


def main():
    generationtest()

if __name__ == '__main__':
    main()
