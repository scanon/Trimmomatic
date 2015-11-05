import unittest
from os import chdir
from Trimmomatic.TrimmomaticImpl import Trimmomatic

class TrimmoaticTest(unittest.TestCase):
    def setUp(self):
        chdir('work/')	
        config={'workspace-url':'https://ci.kbase.us/services/ws'}
        with open('./token') as tf:
           token=tf.read().rstrip()
        self.token=token
        self.cc = Trimmomatic(config)

    def tearDown(self):
        return

    def test_trimmomatic(self):
        print "run trim"
        ctx={'token':self.token}
        input_params={}
        input_params['input_ws']='psdehal:1446073144048'
        input_params['input_paired_end_library']='rhodo.art.q20.int.PE.reads'
	result=self.cc.runTrimmomatic(ctx, input_params)
        print result
        assert result[0].find('Completed successfully')>=0
        input_params['input_paired_end_library']='rhodo.art.jgi.reads'
	result=self.cc.runTrimmomatic(ctx, input_params)
        print result
        assert result[0].find('Completed successfully')>=0
        input_params['input_paired_end_library']='gw460_reads'
	result=self.cc.runTrimmomatic(ctx, input_params)
        print result
        assert result[0].find('Completed successfully')>=0
