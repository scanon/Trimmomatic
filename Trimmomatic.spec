/*
A KBase module: Trimmomatic
This sample module contains one small method - count_contigs.
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
};