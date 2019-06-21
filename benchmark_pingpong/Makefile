ADDITIONAL_COMPILE_FLAGS ?=

compile:
	I_MPI_CC=icc mpiicc -O3 ${ADDITIONAL_COMPILE_FLAGS} -o pingpong.exe pingpong.c -lm

run-sm:
	I_MPI_DEBUG=5 I_MPI_FABRICS="shm:tmi" I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec.hydra -np 2 pingpong.exe

run-3m:
	I_MPI_DEBUG=5 I_MPI_FABRICS="shm:tmi" I_MPI_PIN=1 I_MPI_PIN_DOMAIN=auto mpiexec -np 2 pingpong.exe