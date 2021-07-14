#include "ap_int.h"
#define INPUT_ROW 200
#define HIDDEN_ROW 90
#define OUTPUT_ROW 9

void mlp(int input[INPUT_ROW][1], int result[OUTPUT_ROW][1]) {
#pragma HLS INTERFACE ap_ctrl_none port=return
#pragma HLS INTERFACE s_axilite port=input
#pragma HLS INTERFACE s_axilite port=result

int weightsHidden[HIDDEN_ROW][INPUT_ROW] = {{80,15,96,50,39,72,92,15,87,50,44,75,86,27,20,4,40,68,16,41},
											{25,94,39,42,3,22,62,3,49,89,94,42,89,52,75,14,24,22,13,50},
											{71,35,60,25,85,53,65,0,24,42,51,0,9,34,30,44,54,60,32,56},
											{56,51,88,70,60,70,13,82,8,90,33,69,76,67,96,33,80,46,23,40},
											{85,80,71,85,50,27,15,33,77,77,72,6,26,32,14,66,91,41,32,47},
											{82,74,93,14,4,72,52,17,17,53,61,75,8,66,43,17,78,75,40,41},
											{77,74,80,69,85,41,70,74,28,73,76,17,71,43,38,50,68,54,90,40},	
											{66,11,39,4,17,27,13,29,25,27,63,69,84,96,5,46,8,15,63,1},
											{88,81,0,87,94,64,51,7,71,48,76,17,75,68,40,91,96,60,69,77},
											{6,89,94,6,95,90,19,8,68,51,72,9,19,38,41,21,12,68,94,86},	
											{22,24,89,56,31,83,53,48,50,29,3,67,6,1,71,58,14,30,83,6},	
											{32,27,65,16,21,5,70,33,33,87,49,16,55,17,49,72,88,69,65,75},
											{46,41,74,28,30,95,58,0,82,76,37,54,47,89,32,87,0,80,75,9},
											{41,91,55,66,49,1,95,67,96,37,15,26,78,34,31,62,7,53,3,88},
											{26,92,13,52,18,39,68,28,78,67,31,40,39,5,93,84,60,24,90,23},
											{79,28,41,57,32,55,78,95,28,40,18,23,8,53,49,94,93,19,64,79}};

int weightsOut[OUTPUT_ROW][HIDDEN_ROW] = {{82,24,95,72,80,25,40,38,67,89,21,27,0,89,25,10},
										  {67,79,17,79,29,46,58,60,61,81,54,47,50,31,87,75},	
										  {86,5,0,66,1,56,91,83,80,27,63,55,27,54,18,30},	
										  {84,80,33,28,42,33,71,43,5,73,43,45,62,57,69,44},	
										  {3,2,21,91,50,3,25,19,82,0,35,35,56,34,35,30},	
										  {40,1,72,14,58,60,88,73,21,59,9,40,12,81,75,61},
										  {88,0,28,3,77,52,57,88,69,58,89,62,14,31,5,81},	
										  {17,23,94,71,32,74,20,26,37,14,91,88,12,54,40,26},	
										  {32,66,54,67,96,73,2,73,28,19,64,59,34,9,68,94}};

int hidden[HIDDEN_ROW][1] = {0};

int biasHidden[HIDDEN_ROW] = {26, 6, 14, 98, 12, 39, 53, 29, 18, 0, 19, 19, 35, 93, 36, 60};
int biasOut[OUTPUT_ROW] = {19, 47, 64, 15, 69, 21, 23, 11, 9};

	//Hidden layer
	for(int i = 0; i < HIDDEN_ROW; i++) {
		#pragma HLS pipeline
	    // Iterate over the columns of the B matrix
	    for(int j = 0; j < 1; j++) {
	    	// Do the inner product of a row of A and col of B
	    	hidden[i][j] = 0;
	    	for(int k = 0; k < INPUT_ROW; k++) {
	    		hidden[i][j] += weightsHidden[i][k] * input[k][j];
	    	}
	    }
	}

	//Bias, ReLU
	for(int i = 0; i < HIDDEN_ROW; i++) {
		#pragma HLS pipeline
		for(int j = 0; j < 1; j++) {
			hidden[i][j] /= 256;
			hidden[i][j] += biasHidden[i];
			if (hidden[i][j] < 0) {
				hidden[i][j] = 0;
			}
		}
	}

	//Output layer
	for(int i = 0; i < OUTPUT_ROW; i++) {
		#pragma HLS pipeline
	    // Iterate over the columns of the B matrix
	    for(int j = 0; j < 1; j++) {
	    	// Do the inner product of a row of A and col of B
	    	result[i][j] = 0;
	    	for(int k = 0; k < HIDDEN_ROW; k++) {
	    		result[i][j] += weightsOut[i][k] * hidden[k][j];
	    	}
	    }
	}

	//Bias, ReLU
	for(int i = 0; i < OUTPUT_ROW; i++) {
		#pragma HLS pipeline
		for(int j = 0; j < 1; j++) {
			result[i][j] /= 256;
			result[i][j] += biasOut;
			if (result[i][j] < 0) {
				result[i][j] = 0;
			}
		}
	}

}
