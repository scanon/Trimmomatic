#BEGIN_HEADER
from biokbase.workspace.client import Workspace as workspaceService
import requests
import subprocess
import os
import sys
import re
#END_HEADER


class Trimmomatic:
    '''
    Module Name:
    Trimmomatic

    Module Description:
    A KBase module: Trimmomatic
This sample module contains one small method - count_contigs.
    '''

    ######## WARNING FOR GEVENT USERS #######
    # Since asynchronous IO can lead to methods - even the same method -
    # interrupting each other, you must be *very* careful when using global
    # state. A method could easily clobber the state set by another while
    # the latter method is running.
    #########################################
    #BEGIN_CLASS_HEADER
    workspaceURL = None
    #END_CLASS_HEADER

    # config contains contents of config file in a hash or None if it couldn't
    # be found
    def __init__(self, config):
        #BEGIN_CONSTRUCTOR
        self.workspaceURL = config['workspace-url']
        #END_CONSTRUCTOR
        pass

    def count_contigs(self, ctx, workspace_name, contigset_id):
        # ctx is the context object
        # return variables are: returnVal
        #BEGIN count_contigs
        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        contigSet = wsClient.get_objects([{'ref': workspace_name+'/'+contigset_id}])[0]['data']
        returnVal = {'contig_count': len(contigSet['contigs'])}
        #END count_contigs

        # At some point might do deeper type checking...
        if not isinstance(returnVal, dict):
            raise ValueError('Method count_contigs return value ' +
                             'returnVal is not type dict as required.')
        # return the results
        return [returnVal]

    def runTrimmomatic(self, ctx, input_params):
        # ctx is the context object
        # return variables are: report
        #BEGIN runTrimmomatic
        token = ctx['token']
        wsClient = workspaceService(self.workspaceURL, token=token)
        headers = {'Authorization': 'OAuth '+token}

        TrimmomaticCmd = 'java -jar /kb/module/Trimmomatic-0.33/trimmomatic-0.33.jar '
        TrimmomaticParams = ''

        report = ""    

        # set read type
        if 'read_type' in input_params:
            TrimmomaticCmd += input_params['read_type']
        else:
            print 'read type not defined'
            raise

        # set read quality encoding
        TrimmomaticCmd = TrimmomaticCmd + " -" + input_params['quality_encoding']

        # set adapter trimming
        if 'adapterFa' in input_params:
            ILLUMINACLIP = ("ILLUMINACLIP:/kb/module/Trimmomatic-0.33/adapters/" + 
                            ":".join( (input_params['adapterFa'],
                                       input_params['seed_mismatches'], 
                                       input_params['palindrome_clip_threshold'],
                                       input_params['simple_clip_threshold']) ) + 
                            " " +
                            TrimmomaticParams)
        else:
            ILLUMINACLIP = ""

        # set Crop
        if 'crop_length' in input_params:
            CROP = 'CROP:' + input_params['crop_length']
        else:
            CROP = ""

        # set Headcrop
        if 'head_crop_length' in input_params:
            HEADCROP = 'HEADCROP:' + input_params['head_crop_length']
        else:
            HEADCROP = ""

        # set Leading
        if 'leading_min_quality' in input_params:
            LEADING = 'LEADING:' + input_params['leading_min_quality']
        else:
            LEADING = ""

        # set Trailing
        if 'trailing_min_quality' in input_params:
            TRAILING = 'TRAILING:' + input_params['trailing_min_quality']
        else:
            TRAILING = ""

        # set sliding window
        if 'sliding_window_size' in input_params and 'sliding_window_min_quality' in input_params:
            SLIDINGWINDOW = 'SLIDINGWINDOW:' + input_params['sliding_window_size'] + ":" + input_params['sliding_window_min_quality']
        else:
            SLIDINGWINDOW = ""

        # set min length
        if 'min_length' in input_params:
            MINLEN = 'MINLEN:' + input_params['min_length']
        else:
            MINLEN = ""

        # set params
        TrimmomaticParams = " ".join( (ILLUMINACLIP, CROP, HEADCROP, LEADING, TRAILING, SLIDINGWINDOW, MINLEN) )


        try:
            readLibrary = wsClient.get_objects([{'name': input_params['input_read_library'], 
                                                            'workspace' : input_params['input_ws']}])[0]
        except:
            print "get objects failed"
            raise


        if input_params['read_type'] == 'PE':
            if 'lib1' in readLibrary['data']:
                forward_reads = readLibrary['data']['lib1']['file']
            elif 'handle_1' in readLibrary['data']:
                forward_reads = readLibrary['data']['handle_1']
            if 'lib2' in readLibrary['data']:
                reverse_reads = readLibrary['data']['lib2']['file']
            elif 'handle_2' in readLibrary['data']:
                reverse_reads = readLibrary['data']['handle_2']
            else:
                reverse_reads={}

            forward_reads_file = open(forward_reads['file_name'], 'w', 0)
            r = requests.get(forward_reads['url']+'/node/'+forward_reads['id']+'?download', stream=True, headers=headers)
            for chunk in r.iter_content(1024):
                forward_reads_file.write(chunk)

            if 'interleaved' in readLibrary['data'] and readLibrary['data']['interleaved']:
                if re.search('gz', forward_reads['file_name'], re.I):
                    bcmdstring = 'gunzip -c ' + forward_reads['file_name']
                else:    
                    bcmdstring = 'cat ' + forward_reads['file_name'] 

                
                cmdstring = bcmdstring + '| (paste - - - - - - - -  | tee >(cut -f 1-4 | tr "\t" "\n" > forward.fastq) | cut -f 5-8 | tr "\t" "\n" > reverse.fastq )'
                cmdProcess = subprocess.Popen(cmdstring, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True, executable='/bin/bash')
                stdout, stderr = cmdProcess.communicate()

                # Check return status
                report = "cmdstring: " + cmdstring + " stdout: " + stdout + " stderr: " + stderr
                
                forward_reads['file_name']='forward.fastq'
                reverse_reads['file_name']='reverse.fastq'
            else:
                reverse_reads_file = open(reverse_reads['file_name'], 'w', 0)
                r = requests.get(reverse_reads['url']+'/node/'+reverse_reads['id']+'?download', stream=True, headers=headers)
                for chunk in r.iter_content(1024):
                    reverse_reads_file.write(chunk)

            cmdstring = " ".join( (TrimmomaticCmd, 
                            forward_reads['file_name'], 
                            reverse_reads['file_name'],
                            'forward_paired_'   +forward_reads['file_name'],
                            'forward_unpaired_' +forward_reads['file_name'],
                            'reverse_paired_'   +reverse_reads['file_name'],
                            'reverse_unpaired_' +reverse_reads['file_name'],
                            TrimmomaticParams) )

            cmdProcess = subprocess.Popen(cmdstring, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

            stdout, stderr = cmdProcess.communicate()
            report += "cmdstring: " + cmdstring + " stdout: " + stdout + " stderr " + stderr
        else:
            if 'handle' in readLibrary['data']:
                reads_file = open(readLibrary['data']['handle']['file_name'], 'w', 0)
                r = requests.get(readLibrary['data']['handle']['url']+'/node/'+readLibrary['data']['handle']['id']+'download', stream=True, headers=headers)
                for chunk in r.iter_content(1024):
                    reads_file.write(chunk)

            cmdstring = " ".join( (TrimmomaticCmd,
                            readLibrary['data']['handle']['file_name'],
                            'trimmed_' + readLibrary['data']['handle']['file_name'],
                            TrimmomaticParams) )

            cmdProcess = subprocess.Popen(cmdstring, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
            stdout, stderr = cmdProcess.communicate()
            report = "cmdstring: " + cmdstring + " stdout: " + stdout + " stderr: " + stderr

        #print report

        #END runTrimmomatic

        # At some point might do deeper type checking...
        if not isinstance(report, basestring):
            raise ValueError('Method runTrimmomatic return value ' +
                             'report is not type basestring as required.')
        # return the results
        return [report]
