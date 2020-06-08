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

def regroup(path, seq, name_of_regroup):
	pdf_reader = PdfFileReader(path)
	pdf_writer = PdfFileWriter()

	for page in seq:
		pdf_writer.addPage(pdf_reader.getPage(page - 1))

	output = name_of_regroup + '.pdf'
	with open(output, 'wb') as output_pdf:
		pdf_writer.write(output_pdf)

# 這是用來建立頁數範圍用的函式
# 比如說，如果你指定create_list(2, 10)
# 那就會產生一個[2, 3, 4, 5, 6, 7, 8, 9, 10]的結果
def create_list(s_idx, e_idx):
	res_list = []
	if (s_idx == e_idx):
		res_list.append(s_idx)
	elif (s_idx < e_idx):
		while (s_idx < e_idx + 1):
			res_list.append(s_idx)
			s_idx = s_idx + 1
	else:
		while (s_idx > e_idx - 1):
			res_list.append(s_idx)
			s_idx = s_idx - 1

	return res_list

if __name__ == '__main__':
	if len(sys.argv) < 2:
                # <split unit>
		print('python pdf_tool.py merge')
		print('python pdf_tool.py split <split unit>')
		print('python pdf_tool.py regroup')
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
	elif sys.argv[1] == 'regroup':
        # path是指定要作處理的檔案
		path = u'HD_Disposal_Guidelines.pdf'

        # sequence是用來指定處理過的檔案，頁面要用什麼樣的順序呈現，以下都以HD_Disposal_Guidelines.pdf作例子，這個pdf檔有6頁內容
        # 所以說，它本來的頁面順序是[1, 2, 3, 4, 5, 6]
		# 範例一： sequence = [2, 4, 6, 1, 2, 3]，處理後的pdf還是有6頁，只是順序變了
        # 範例二： sequence = [1, 3, 5]，處理好的pdf只剩下三頁
		# 範例三： sequence = [1, 2, 3]
		#       sequence.extend(create_list(1, 6))
        #  這個例子比較複雜，處理好的pdf會有9頁，前三頁是page 1, page 2, page 3，然後是1, 2, 3, 4, 5, 6

        # 下面的HD_regroup是預設處理完的檔案名字，可以改成想要的名字
		regroup(path, sequence, u'HD_regroup')
	else:
		print('python pdf_tool.py [merge/split]')

	sys.exit(0)



