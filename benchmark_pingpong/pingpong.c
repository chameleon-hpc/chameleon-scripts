#include <mpi.h>
#include <stdio.h>
#include <math.h>
#include <stdlib.h>
#include <omp.h>

#ifndef NUM_ITERATIONS
#define NUM_ITERATIONS 100
#endif

#ifndef MAX_MSG_SIZE_EXPONENT
#define MAX_MSG_SIZE_EXPONENT 28
#endif

#ifndef BENCHMARK_TYPE
#define BENCHMARK_TYPE 0 // regular ping pong benchmark using cached, contiguous data
// #define BENCHMARK_TYPE 1 // ping pong that always uses a different chunk of data (also contiguous but might not be cached)
// #define BENCHMARK_TYPE 2 // using custom MPI data types like done in Chameleon (strided data access but with cached data)
#endif

int main(int argc, char *argv[]) {
    int iMyRank, iNumProcs;
	MPI_Init(&argc, &argv);
	MPI_Comm_size(MPI_COMM_WORLD, &iNumProcs);
	MPI_Comm_rank(MPI_COMM_WORLD, &iMyRank);

    int msg_size_start  = 2;
    int msg_size_end    = MAX_MSG_SIZE_EXPONENT;
    int msg_size;
    int iter;
    int b;

    if(iNumProcs != 2) {
        fprintf(stderr, "Wrong number of processes. Has to be 2.\n");
        return 1;
    }

    #if BENCHMARK_TYPE == 1
    void **tmp_buffers_send = malloc(sizeof(void*)*NUM_ITERATIONS);
    void **tmp_buffers_recv = malloc(sizeof(void*)*NUM_ITERATIONS);
    #elif BENCHMARK_TYPE == 2
    void **tmp_buffers_send = (void **) malloc(sizeof(void*)*4);
    void **tmp_buffers_recv = (void **) malloc(sizeof(void*)*4);
    #endif

    for(msg_size = msg_size_start; msg_size <= msg_size_end; msg_size++) {
        int cur_size_bytes = pow(2.0, msg_size);

        #if BENCHMARK_TYPE == 0
        int *tmp_buffer_send = (int*) malloc(cur_size_bytes);
        int *tmp_buffer_recv = (int*) malloc(cur_size_bytes);
        for(b = 0; b < cur_size_bytes/sizeof(int); b++) {
            tmp_buffer_send[b] = 1;
            tmp_buffer_send[b] = 0;
        }
        #elif BENCHMARK_TYPE == 1
        for(iter = 0; iter < NUM_ITERATIONS; iter++) {
            tmp_buffers_send[iter] = malloc(cur_size_bytes);
            tmp_buffers_recv[iter] = malloc(cur_size_bytes);
            int *cur_send = (int*) tmp_buffers_send[iter];
            int *cur_recv = (int*) tmp_buffers_recv[iter];
            for(b = 0; b < cur_size_bytes/sizeof(int); b++) {
                cur_send[b] = 1;
                cur_recv[b] = 0;
            }
        }
        #elif BENCHMARK_TYPE == 2
        for(iter = 0; iter < 4; iter++) {
            tmp_buffers_send[iter] = malloc(cur_size_bytes);
            tmp_buffers_recv[iter] = malloc(cur_size_bytes);
            int *cur_send = (int*) tmp_buffers_send[iter];
            int *cur_recv = (int*) tmp_buffers_recv[iter];
            for(b = 0; b < cur_size_bytes/sizeof(int); b++) {
                cur_send[b] = 1;
                cur_recv[b] = 0;
            }
        }
        #endif

        #if BENCHMARK_TYPE == 2
        MPI_Datatype    cur_type_send;
        MPI_Datatype    dt_send[4];
        int             blocklen_send[4];
        MPI_Aint        disp_send[4];

        MPI_Datatype    cur_type_recv;
        MPI_Datatype    dt_recv[4];
        int             blocklen_recv[4];
        MPI_Aint        disp_recv[4];

        int chunk, ierr;
        for(chunk = 0; chunk < 4; chunk++) {
            dt_send[chunk]          = MPI_BYTE;
            blocklen_send[chunk]    = cur_size_bytes/4;
            MPI_Get_address(tmp_buffers_send[chunk], &(disp_send[chunk]));

            dt_recv[chunk]          = MPI_BYTE;
            blocklen_recv[chunk]    = cur_size_bytes/4;
            MPI_Get_address(tmp_buffers_recv[chunk], &(disp_recv[chunk]));
        }

        ierr = MPI_Type_create_struct(4, blocklen_send, disp_send, dt_send, &cur_type_send);
        ierr = MPI_Type_commit(&cur_type_send);
        ierr = MPI_Type_create_struct(4, blocklen_recv, disp_recv, dt_recv, &cur_type_recv);
        ierr = MPI_Type_commit(&cur_type_recv);
        #endif
        
        double time = 0.;
        if(iMyRank == 0) {
            MPI_Barrier(MPI_COMM_WORLD);
            MPI_Barrier(MPI_COMM_WORLD);
            MPI_Barrier(MPI_COMM_WORLD);

            time -= omp_get_wtime();
            for(iter = 0; iter < NUM_ITERATIONS; iter++) {
                #if BENCHMARK_TYPE == 0
                MPI_Send(tmp_buffer_send, cur_size_bytes, MPI_BYTE, 1, 0, MPI_COMM_WORLD);
                MPI_Recv(tmp_buffer_recv, cur_size_bytes, MPI_BYTE, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                #elif BENCHMARK_TYPE == 1
                MPI_Send(tmp_buffers_send[iter], cur_size_bytes, MPI_BYTE, 1, 0, MPI_COMM_WORLD);
                MPI_Recv(tmp_buffers_recv[iter], cur_size_bytes, MPI_BYTE, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                #elif BENCHMARK_TYPE == 2
                MPI_Send(MPI_BOTTOM, 1, cur_type_send, 1, 0, MPI_COMM_WORLD);
                MPI_Recv(MPI_BOTTOM, 1, cur_type_recv, 1, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                #endif
            }
            time += omp_get_wtime();
            time /= NUM_ITERATIONS;
        } else {
            MPI_Barrier(MPI_COMM_WORLD);
            MPI_Barrier(MPI_COMM_WORLD);
            MPI_Barrier(MPI_COMM_WORLD);

            time -= omp_get_wtime();
            for(iter = 0; iter < NUM_ITERATIONS; iter++) {                
                #if BENCHMARK_TYPE == 0
                MPI_Recv(tmp_buffer_recv, cur_size_bytes, MPI_BYTE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                MPI_Send(tmp_buffer_send, cur_size_bytes, MPI_BYTE, 0, 0, MPI_COMM_WORLD);
                #elif BENCHMARK_TYPE == 1
                MPI_Recv(tmp_buffers_recv[iter], cur_size_bytes, MPI_BYTE, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                MPI_Send(tmp_buffers_send[iter], cur_size_bytes, MPI_BYTE, 0, 0, MPI_COMM_WORLD);
                #elif BENCHMARK_TYPE == 2
                MPI_Recv(MPI_BOTTOM, 1, cur_type_recv, 0, 0, MPI_COMM_WORLD, MPI_STATUS_IGNORE);
                MPI_Send(MPI_BOTTOM, 1, cur_type_send, 0, 0, MPI_COMM_WORLD);
                #endif
            }
            time += omp_get_wtime();
            time /= NUM_ITERATIONS;
        }

        if(iMyRank == 0) {
            fprintf(stderr, "PingPong with msg_size: %*d (%*.3f KB) took %*.3f us with a throughput of %*.3f MB/s\n", 13, cur_size_bytes, 13, cur_size_bytes/1000.0 , 10, time*1e06, 10, ((double)cur_size_bytes*2.0/(1e06*time)));
        }

        #if BENCHMARK_TYPE == 0
        free(tmp_buffer_send);
        free(tmp_buffer_recv);
        #elif BENCHMARK_TYPE == 1
        for(iter = 0; iter < NUM_ITERATIONS; iter++) {
            free(tmp_buffers_send[iter]);
            free(tmp_buffers_recv[iter]);
        }
        #elif BENCHMARK_TYPE == 2
        for(iter = 0; iter < 4; iter++) {
            free(tmp_buffers_send[iter]);
            free(tmp_buffers_recv[iter]);
        }
        MPI_Type_free(&cur_type_send);
        MPI_Type_free(&cur_type_recv);
        #endif
    }
    
    #if BENCHMARK_TYPE == 1 || BENCHMARK_TYPE == 2
    free(tmp_buffers_send);
    free(tmp_buffers_recv);
    #endif
    
    MPI_Finalize();
    return 0;
}