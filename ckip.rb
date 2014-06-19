require 'ckip_client'
text = File.open('testfile.txt').read
puts CKIP.segment( text )