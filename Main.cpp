﻿// Simple wrapper for Sven Forstmann's mesh simplification tool
//
// Loads a OBJ format mesh, decimates mesh, saves decimated mesh as OBJ format
// http://voxels.blogspot.com/2014/05/quadric-mesh-simplification-with-source.html
// https://github.com/sp4cerat/Fast-Quadric-Mesh-Simplification
//To compile for Linux/OSX (GCC/LLVM)
//  g++ Main.cpp -O3 -o simplify
//To compile for Windows (Visual Studio)
// vcvarsall amd64
// cl /EHsc Main.cpp /osimplify
//To execute
//  ./simplify wall.obj out.obj 0.04
//
// Pascal Version by Chris Roden:
// https://github.com/neurolabusc/Fast-Quadric-Mesh-Simplification-Pascal-
//

#include "Simplify.h"
#include <stdio.h>
#include <time.h>  // clock_t, clock, CLOCKS_PER_SEC

void showHelp(const char * argv[]) {
    const char *cstr = (argv[0]);
    printf("Usage: %s <input> <output> <ratio> <agressiveness)\n", cstr);
    printf(" Input: name of existing OBJ format mesh\n");
    printf(" Output: name for decimated OBJ format mesh\n");
    printf(" Ratio: (default = 0.5) for example 0.2 will decimate 80%% of triangles\n");
    printf(" Agressiveness: (default = 7.0) faster or better decimation\n");
    printf("Examples :\n");
#if defined(_WIN64) || defined(_WIN32)
    printf("  %s c:\\dir\\in.obj c:\\dir\\out.obj 0.2\n", cstr);
    printf("  %s C:\\Users\\liuchuang.NUCTECH\\Desktop\\in.obj C:\\Users\\liuchuang.NUCTECH\\Desktop\\out.obj 0.2\n", cstr);

#else
    printf("  %s ~/dir/in.obj ~/dir/out.obj 0.2\n", cstr);
#endif
} //showHelp()

//int main(int argc, const char * argv[]) {
//    printf("Mesh Simplification (C)2014 by Sven Forstmann in 2014, MIT License (%zu-bit)\n", sizeof(size_t)*8);
//    if (argc < 3) {
//        showHelp(argv);
//        return EXIT_SUCCESS;
//    }
//	Simplify::load_obj(argv[1]);
//	if ((Simplify::triangles.size() < 3) || (Simplify::vertices.size() < 3))
//		return EXIT_FAILURE;
//	int target_count =  Simplify::triangles.size() >> 1;
//    if (argc > 3) {
//    	float reduceFraction = atof(argv[3]);
//    	if (reduceFraction > 1.0) reduceFraction = 1.0; //lossless only
//    	if (reduceFraction <= 0.0) {
//    		printf("Ratio must be BETWEEN zero and one.\n");
//    		return EXIT_FAILURE;
//    	}
//    	target_count = round((float)Simplify::triangles.size() * atof(argv[3]));
//    }
//    if (target_count < 4) {
//		printf("Object will not survive such extreme decimation\n");
//    	return EXIT_FAILURE;
//    }
//    double agressiveness = 7.0;
//    if (argc > 4) {
//    	agressiveness = atof(argv[4]);
//    }
//	clock_t start = clock();
//	printf("Input: %zu vertices, %zu triangles (target %d)\n", Simplify::vertices.size(), Simplify::triangles.size(), target_count);
//	int startSize = Simplify::triangles.size();
//	Simplify::simplify_mesh(target_count, agressiveness, true);
//	//Simplify::simplify_mesh_lossless( false);
//	if ( Simplify::triangles.size() >= startSize) {
//		printf("Unable to reduce mesh.\n");
//    	return EXIT_FAILURE;
//	}
//	Simplify::write_obj(argv[2]);
//	printf("Output: %zu vertices, %zu triangles (%f reduction; %.4f sec)\n",Simplify::vertices.size(), Simplify::triangles.size()
//		, (float)Simplify::triangles.size()/ (float) startSize  , ((float)(clock()-start))/CLOCKS_PER_SEC );
//	return EXIT_SUCCESS;
//}

using namespace IO;
int main() {
	// Input and output file paths
	std::string input_file = "D:/ProgramCode/Fast-Quadric-Mesh-Simplification/src.cmd/x64/Release/input.stl";
	std::string output_file = 
	convert_stl_to_obj(input_file);

	// Define simplification parameters
	int target_percentages[] = { 50, 51, 52, 53, 54, 55, 56, 57, 58, 59,
							  60, 61, 62, 63, 64, 65, 66, 67, 68, 69,
							  70, 71, 72, 73, 74, 75, 76, 77, 78, 79,
							  80, 81, 82, 83, 84, 85, 86, 87, 88, 89,
							  90, 91};

	double aggressiveness = 7.0;

	// Load the mesh
	Simplify::load_obj(output_file.c_str());

	// Perform simplification for different target percentages
	for (int percentage : target_percentages) {
		int target_count = Simplify::triangles.size() * (1.0 - (percentage * 1.0f / 100));

		// Perform simplification
		Simplify::simplify_mesh(target_count, aggressiveness, true);

		// Write the simplified mesh to file
		std::string output_filename = std::to_string((percentage)) + "%.obj";
		Simplify::write_obj(output_filename.c_str());
	
		// Reset the mesh for next iteration
		Simplify::vertices.clear();
		Simplify::triangles.clear();

		// Reload the original mesh
		Simplify::load_obj(output_file.c_str());
	}

	return 0;
}