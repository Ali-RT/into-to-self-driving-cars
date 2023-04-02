#include "headers/initialize_beliefs.h"

using namespace std;

// OPTIMIZATION: pass large variables by reference
vector< vector <float> > initialize_beliefs(int &height, int &width) {

	// OPTIMIZATION: Which of these variables are necessary?
	// OPTIMIZATION: Reserve space in memory for vectors
  	vector< vector <float> > newGrid;

	float total, prob_per_cell;
	
 
  	prob_per_cell = 1.0 / ( (float) height * width) ;
	vector<float> newRow(width, prob_per_cell);
  	// OPTIMIZATION: Is there a way to get the same results 	// without nested for loops?
	for (unsigned int i=0; i<height; i++) {
		newGrid.push_back(newRow);
	}
	return newGrid;
}