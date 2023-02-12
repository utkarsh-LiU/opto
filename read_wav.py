import numpy as np

# function to read WAVECAR file
def read_wavecar(filename):
    with open(filename, 'rb') as f:
        # read record length
        rec_len = np.fromfile(f, dtype=np.int32, count=1)
        # read number of spin components
        num_spin = np.fromfile(f, dtype=np.int32, count=1)
        # read RTAG
        rtag = np.fromfile(f, dtype=np.int32, count=1)
        # read number of k-points
        num_kpts = np.fromfile(f, dtype=np.int32, count=1)
        # read number of bands
        num_bands = np.fromfile(f, dtype=np.int32, count=1)
        # read ENCUT
        encut = np.fromfile(f, dtype=np.float64, count=1)
        # read lattice vectors
        lat_vec_a = np.fromfile(f, dtype=np.float64, count=3)
        lat_vec_b = np.fromfile(f, dtype=np.float64, count=3)
        lat_vec_c = np.fromfile(f, dtype=np.float64, count=3)

        # calculate number of plane waves
        num_planewaves = rec_len[0] - (9 + 5 * num_spin[0])

        # read wavefunctions
        wavefunctions = np.empty((num_spin[0], num_kpts[0], num_bands[0], num_planewaves), dtype=np.complex128)
        for spin in range(num_spin[0]):
            for k in range(num_kpts[0]):
                # read k-vector
                k_vec = np.fromfile(f, dtype=np.float64, count=3)
                # read band energies and occupations
                band_energies = np.fromfile(f, dtype=np.float64, count=num_bands[0])
                band_occupations = np.fromfile(f, dtype=np.float64, count=num_bands[0])
                for n in range(num_bands[0]):
                    # read wavefunction coefficients
                    wavefunction = np.fromfile(f, dtype=np.complex128, count=num_planewaves)
                    wavefunctions[spin, k, n, :] = wavefunction
    return wavefunctions

# function to write wavefunctions to file
def write_wavefunctions(wavefunctions, filename_prefix):
    for spin in range(wavefunctions.shape[0]):
        for k in range(wavefunctions.shape[1]):
            for n in range(wavefunctions.shape[2]):
                filename = filename_prefix + '_spin' + str(spin) + '_k' + str(k) + '_n' + str(n) + '.txt'
                np.savetxt(filename, wavefunctions[spin, k, n, :], fmt='%.18e %.18e')

# main function
if __name__ == '__main__':
    filename = 'WAVECAR'
    wavefunctions = read_wavecar(filename)
    filename_prefix = 'wavefunctions.dat'
    write_wavefunctions(wavefunctions, filename_prefix)