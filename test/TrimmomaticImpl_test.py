import unittest
from os import chdir
from os import environ
from ConfigParser import ConfigParser
from Trimmomatic.TrimmomaticImpl import Trimmomatic

class TrimmoaticTest(unittest.TestCase):
    def setUp(self):
        #chdir('work/')	
        token = environ.get('KB_AUTH_TOKEN', None)
        config_file = environ.get('KB_DEPLOYMENT_CONFIG', None)
        config = {}
        config_p = ConfigParser()
        config_p.read(config_file)
        for nameval in config_p.items('Trimmomatic'):
            config[nameval[0]] = nameval[1]
        #wsURL = config['workspace-url']
        #wsClient = workspaceService(wsURL, token=token)

        self.token=token
        self.cc = Trimmomatic(config)

    def tearDown(self):
        return

    def test_trimmomatic(self):
        print "run trim"
        ctx={'token':self.token}
        input_params={}
        input_params['input_ws']='psdehal:1446073144048'
        input_params['input_read_library']='rhodo.art.q20.int.PE.reads'
        input_params['read_type']='PE'
        input_params['quality_encoding']='phred33'
        input_params['adapterFa']='TruSeq3-PE.fa'
        input_params['seed_mismatches']='2'
        input_params['palindrome_clip_threshold']='30'
        input_params['simple_clip_threshold']='10'
        input_params['crop_length']='200'
        input_params['head_crop_length']='1'
        input_params['leading_min_quality']='1'
        input_params['trailing_min_quality']='1'
        input_params['sliding_window_size']='4'
        input_params['sliding_window_min_quality']='15'
        input_params['min_length']='100'
	result=self.cc.runTrimmomatic(ctx, input_params)
        print result
        assert result[0].find('Completed successfully')>=0
        
        input_params['input_read_library']='rhodo.art.jgi.reads'
	result=self.cc.runTrimmomatic(ctx, input_params)
        print result
        assert result[0].find('Completed successfully')>=0
        input_params['input_read_library']='rhodo.art.q50.SE.reads'
        input_params['read_type']='SE'
        input_params['adapterFa']='TruSeq3-SE.fa'
	result=self.cc.runTrimmomatic(ctx, input_params)
        print result
        assert result[0].find('Completed successfully')>=0

    def test_params_trimmomatic(self):
        print "run trim parameter tests"
        ctx={'token':self.token}
        input_params={}
        input_params['input_ws']='psdehal:1446073144048'
        input_params['input_read_library']='rhodo.art.q20.int.PE.reads'
        input_params['read_type'] = None
        self.assertRaises(ValueError, lambda: self.cc.parse_trimmomatic_steps(input_params))
        input_params['read_type'] = 'XYZ'
        self.assertRaises(ValueError, lambda: self.cc.parse_trimmomatic_steps(input_params))
        input_params['read_type'] = 'PE'
        input_params['quality_encoding'] = None
        self.assertRaises(ValueError, lambda: self.cc.parse_trimmomatic_steps(input_params))
        input_params['quality_encoding'] = "XYZ"
        self.assertRaises(ValueError, lambda: self.cc.parse_trimmomatic_steps(input_params))
        input_params['quality_encoding'] = 'phred33'
        self.assertRaises(ValueError, lambda: self.cc.parse_trimmomatic_steps(input_params))
        input_params['crop_length'] = '1'
        input_params['adapterFa'] = None
        input_params['seed_mismatches']='2'
        self.assertRaises(ValueError, lambda: self.cc.parse_trimmomatic_steps(input_params))
        input_params['adapterFa']='TruSeq3-PE.fa'
        input_params['palindrome_clip_threshold']='30'
        input_params['simple_clip_threshold']='10'
        input_params['sliding_window_size']=None
        input_params['sliding_window_min_quality']='15'
        self.assertRaises(ValueError, lambda: self.cc.parse_trimmomatic_steps(input_params))
