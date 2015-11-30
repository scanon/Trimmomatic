/*
A KBase module: Trimmomatic
This module wraps the Trimmomatic tool
http://www.usadellab.org/cms/index.php?page=trimmomatic
*/

module Trimmomatic {
	/*
	A string representing a ContigSet id.
	*/
	typedef string contigset_id;
	
	/*
	A string representing a workspace name.
	*/
	typedef string workspace_name;
	
	typedef structure {
	    int contig_count;
	} CountContigsResults;
	
	/*
	Count contigs in a ContigSet
	contigset_id - the ContigSet to count.
	*/
	funcdef count_contigs(workspace_name,contigset_id) returns (CountContigsResults) authentication required;



	/* using KBaseFile.PairedEndLibrary */

	typedef structure {
		workspace_name input_ws;
		workspace_name output_ws;
		string read_type;
		string input_read_library;
		string adapterFa;
		int seed_mismatches;
		int palindrom_clip_threshold;
		int simple_clip_threshold;
		string quality_encoding;
		int slinding_window_size;
		int sliding_window_min_quality;
		int leading_min_quality;
		int trailing_min_quality;
		int crop_length;
		int head_crop_length;
		int min_length;
		string output_read_library;
	} TrimmomaticInput;

	funcdef runTrimmomatic(TrimmomaticInput input_params) 
		returns (string report) 
		authentication required;

};