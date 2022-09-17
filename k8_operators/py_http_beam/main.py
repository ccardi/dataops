import argparse
import logging
import requests

import apache_beam as beam
from apache_beam.io import WriteToText
from apache_beam.io.textio import ReadFromText
from apache_beam.options.pipeline_options import PipelineOptions
from apache_beam.options.pipeline_options import SetupOptions

#API Call Function
class getId(beam.DoFn):
	def process(self, element, url):
		URL=url
		r = requests.get(URL)
		yield r.status_code, r.json, element, url

#Filters
def is_200(element):
  return element[0] == 200

def is_not200(element):
  return element[0] != 200

def run(argv=None):
  parser = argparse.ArgumentParser()
  parser.add_argument('--input',
                      required=True,
                      help='Input file to process.')
  parser.add_argument('--url',
                      required=True,
                      help='url to call')
  parser.add_argument('--output',
                      required=False,
                      help='Output file to write results to.')
  known_args, pipeline_args = parser.parse_known_args(argv)
  # We use the save_main_session option because one or more DoFn's in this
  # workflow rely on global context (e.g., a module imported at module level).
  pipeline_options = PipelineOptions(pipeline_args)
  pipeline_options.view_as(SetupOptions).save_main_session = True
  
  with beam.Pipeline(options=pipeline_options) as p:
  	reads =	(
		  p 
		  | "Read ids" >> ReadFromText(file_pattern=known_args.input) 
		  | "API Call" >> beam.ParDo(getId(), known_args.url)
	)
  	writeOK = (
		  reads 
		  | 'Filter 200' >> beam.Filter(is_200)
		  | "writeToFile200" >> WriteToText(known_args.output,file_name_suffix='status200')
	)
  	writeKO = (
		  reads
		  | 'Filter not 200' >> beam.Filter(is_not200)
		  | "writeToFileNot200" >> WriteToText(known_args.output,file_name_suffix='statusNot200')
	)

if __name__ == '__main__':
  logging.getLogger().setLevel(logging.INFO)
  run()