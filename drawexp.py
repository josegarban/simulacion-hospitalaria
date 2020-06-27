import main, clean
import pprint

from scipy.stats import expon
import matplotlib.pyplot as plt
import numpy as np

def generationtest():

    fig, ax = plt.subplots(1, 1)

    mean, var, skew, kurt = expon.stats(moments='mvsk')

    # numpy.linspace: generate a linear space of numbers
    # matplotlib.expon.ppf: percent point function (inverse of cumulative distribution function — percentiles)
    x = np.linspace(expon.ppf(0.01), expon.ppf(0.99), 100) # start, stop, number of samples to generate
    # print(x)
    ax.plot(x, expon.pdf(x), 'r-', lw=5, alpha=0.9, label='expon pdf')

    # Freeze the distribution and display the frozen pdf:
    rv = expon()
    ax.plot(x, rv.pdf(x), 'k-', lw=2, label='frozen pdf')

    vals = expon.ppf([0.001, 0.5, 0.999])
    # print(vals)

    # Check accuracy of cdf and ppf:
    close = np.allclose([0.001, 0.5, 0.999], expon.cdf(vals))
    print(close)

    # Generate random numbers
    r = expon.rvs(size=1000)
    # print(r)
    ax.hist(r, density=True, histtype='stepfilled', alpha=0.2)
    ax.legend(loc='best', frameon=False)
    plt.show()


def main():
    generationtest()

if __name__ == '__main__':
    main()
