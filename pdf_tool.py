# coding=UTF-8

import sys
from PyPDF2 import PdfFileReader, PdfFileWriter

def merge_pdfs(paths, output):
	pdf_writer = PdfFileWriter()

	for path in paths:
		pdf_reader = PdfFileReader(path)
		for page in range(pdf_reader.getNumPages()):
			# Add each page to the writer object
			pdf_writer.addPage(pdf_reader.getPage(page))

	# Write out the merged PDF
	with open(output, 'wb') as out:
		pdf_writer.write(out)

def split(path, name_of_split, split_unit):
        out_count = 0
	pdf = PdfFileReader(path)
	try:
                if pdf.getNumPages() < split_unit:
                        raise

                for page in range(pdf.getNumPages() / split_unit):
                        pdf_writer = PdfFileWriter()
                        for unit in range(split_unit):
                                pdf_writer.addPage(pdf.getPage(page * split_unit + unit))

                        output = name_of_split + str(out_count) + '.pdf'
                        out_count = out_count + 1
                        with open(output, 'wb') as output_pdf:
        			pdf_writer.write(output_pdf)

        	if pdf.getNumPages() % split_unit:
                        rest = pdf.getNumPages() % split_unit
                        pdf_writer = PdfFileWriter()
                        for unit in range(rest, 0, -1):
                                pdf_writer.addPage(pdf.getPage(pdf.getNumPages() - unit))

                        output = name_of_split + str(out_count) + '.pdf'
                        with open(output, 'wb') as output_pdf:
                                pdf_writer.write(output_pdf)

        except:
                print('split_unit is too big')

if __name__ == '__main__':
	if len(sys.argv) < 2:
                # <split unit>
		print('python pdf_tool.py merge')
		print('python pdf_tool.py split <split unit>')
		sys.exit(0)

	if sys.argv[1] == 'merge':
		# paths裡面放的是要合併的檔案們，它只會按照放的檔案順序作合併
		paths = [u'HD_page4-1.pdf', u'HD_page4-2.pdf']
		merge_pdfs(paths, output='merged.pdf')
	elif sys.argv[1] == 'split':
                if len(sys.argv) != 3:
                        print('python pdf_tool.py split <split unit>')
                        sys.exit(0)

		# path是指定要切割的檔案
		path = u'1052_001.pdf'
		# 切割過的檔案，會一頁一頁的分別存放在HD_page_0.pdf, HD_page_1.pdf...
		# 可以改變下面的HD_page成想到的檔案名字
		split(path, u'HD_page', int(sys.argv[2]))
	else:
		print('python pdf_tool.py [merge/split]')

	sys.exit(0)
�JE