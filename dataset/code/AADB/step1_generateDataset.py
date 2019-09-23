#"HITId","HITTypeId","Title","Description","Keywords","Reward","CreationTime","MaxAssignments","RequesterAnnotation","AssignmentDurationInSeconds","AutoApprovalDelayInSeconds","Expiration","NumberOfSimilarHITs","LifetimeInSeconds","AssignmentId","WorkerId","AssignmentStatus","AcceptTime","SubmitTime","AutoApprovalTime","ApprovalTime","RejectionTime","RequesterFeedback","WorkTimeInSeconds","LifetimeApprovalRate","Last30DaysApprovalRate","Last7DaysApprovalRate","Input.image_url1","Input.image_url2","Input.image_url3","Input.image_url4","Input.image_url5","Input.image_url6","Input.image_url7","Input.image_url8","Input.image_url9","Input.image_url10","Answer.ColorHarmony1","Answer.ColorHarmony10","Answer.ColorHarmony2","Answer.ColorHarmony3","Answer.ColorHarmony4","Answer.ColorHarmony5","Answer.ColorHarmony6","Answer.ColorHarmony7","Answer.ColorHarmony8","Answer.ColorHarmony9","Answer.Content1","Answer.Content10","Answer.Content2","Answer.Content3","Answer.Content4","Answer.Content5","Answer.Content6","Answer.Content7","Answer.Content8","Answer.Content9","Answer.DoF1","Answer.DoF10","Answer.DoF2","Answer.DoF3","Answer.DoF4","Answer.DoF5","Answer.DoF6","Answer.DoF7","Answer.DoF8","Answer.DoF9","Answer.MotionBlur1","Answer.MotionBlur10","Answer.MotionBlur2","Answer.MotionBlur3","Answer.MotionBlur4","Answer.MotionBlur5","Answer.MotionBlur6","Answer.MotionBlur7","Answer.MotionBlur8","Answer.MotionBlur9","Answer.ObjectEmphasis1","Answer.ObjectEmphasis10","Answer.ObjectEmphasis2","Answer.ObjectEmphasis3","Answer.ObjectEmphasis4","Answer.ObjectEmphasis5","Answer.ObjectEmphasis6","Answer.ObjectEmphasis7","Answer.ObjectEmphasis8","Answer.ObjectEmphasis9","Answer.Repetition1","Answer.Repetition10","Answer.Repetition2","Answer.Repetition3","Answer.Repetition4","Answer.Repetition5","Answer.Repetition6","Answer.Repetition7","Answer.Repetition8","Answer.Repetition9","Answer.RuleOfThirds1","Answer.RuleOfThirds10","Answer.RuleOfThirds2","Answer.RuleOfThirds3","Answer.RuleOfThirds4","Answer.RuleOfThirds5","Answer.RuleOfThirds6","Answer.RuleOfThirds7","Answer.RuleOfThirds8","Answer.RuleOfThirds9","Answer.StrongColor1","Answer.StrongColor10","Answer.StrongColor2","Answer.StrongColor3","Answer.StrongColor4","Answer.StrongColor5","Answer.StrongColor6","Answer.StrongColor7","Answer.StrongColor8","Answer.StrongColor9","Answer.Symmetry1","Answer.Symmetry10","Answer.Symmetry2","Answer.Symmetry3","Answer.Symmetry4","Answer.Symmetry5","Answer.Symmetry6","Answer.Symmetry7","Answer.Symmetry8","Answer.Symmetry9","Answer.VisualBalance1","Answer.VisualBalance10","Answer.VisualBalance2","Answer.VisualBalance3","Answer.VisualBalance4","Answer.VisualBalance5","Answer.VisualBalance6","Answer.VisualBalance7","Answer.VisualBalance8","Answer.VisualBalance9","Answer.choiceLight1","Answer.choiceLight10","Answer.choiceLight2","Answer.choiceLight3","Answer.choiceLight4","Answer.choiceLight5","Answer.choiceLight6","Answer.choiceLight7","Answer.choiceLight8","Answer.choiceLight9","Answer.overallScore1","Answer.overallScore10","Answer.overallScore2","Answer.overallScore3","Answer.overallScore4","Answer.overallScore5","Answer.overallScore6","Answer.overallScore7","Answer.overallScore8","Answer.overallScore9","Approve","Reject"
import sys, string, math, time
import urllib
#import flickr
import os
import http.client
import requests
import os.path
import shutil
import numpy as np

###########################
score0imgFolder = r'./zeroScoreImages'
if os.path.isdir(score0imgFolder):
	shutil.rmtree(score0imgFolder)

os.mkdir( score0imgFolder )

###########################
# ten images per assignment
imgNum = 10

###########################
# refine the results
result_csv = './AllinAll.csv' # the result file
result_csvTMP = './result_csv.csv'
f = open(result_csv, 'r')
lines = f.readlines()
f.close()

ftmp = open(result_csvTMP, 'w')
for i in range(len(lines)):
	if i == 0:
		lineTMP = lines[i]
		#lineTMP = lineTMP.replace('"', '')
		lines[i] = lineTMP.strip()
		ftmp.write(lineTMP.strip()+'\n')
	else:
		lineTMP = lines[i]
		lineTMP = lineTMP.replace('rate the photo w.r.t its aesthetic, and select attributes to explain why this image is of high or low aesthetic', 'description')
		lineTMP = lineTMP.replace('photo aesthetic, attribute, tagging', 'keywords')
		lineTMP = lineTMP.replace('"', '')
		lineTMP = lineTMP.replace(',', '","')
		lineTMP = lineTMP.replace('""', '"n"')
		lineTMP = lineTMP.replace('Neutral', 'n')
		lineTMP = lineTMP.replace('Positive', '<font color="green">Pos</font>')
		lineTMP = lineTMP.replace('Negative', '<font color="red">Neg</font>')

		#lineTMP = lineTMP.replace('"', '')
		lines[i] = lineTMP.strip()
		ftmp.write(lineTMP.strip()+'\n')

ftmp.close()

# get all the titles
titleLine = lines[0]
titles = titleLine.split(',') #  as all keywords are separated by ',', changing 'description', 'keywords' and 'title' in the result file might be required!!!

count=0
for titleName in titles:
	titles[count] = titles[count].strip()
	count = count + 1
	#print count, titleName.strip()


####################################################################################################
########################## list all the individual images ##########################
####################################################################################################
print ('list all the individual images')
htmlFile = 'visualizeResultIndividualImage.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')

# check the file
count = 0
for lineIdx in lines[1:]:
	count = count + 1
	lines[count] = lines[count].strip()
	line = lines[count]
	line = line.split(',')
	f.write('<p>HITId: ' + line[titles.index('"HITId"')] + '</p>\n')
	f.write('<p>WorkerId: ' + line[titles.index('"WorkerId"')] + '</p>\n')
	#print count, titles.index('"WorkTimeInSeconds"'), line[titles.index('"WorkTimeInSeconds"')]
	f.write('<p>WorkTimeInSeconds: ' + line[titles.index('"WorkTimeInSeconds"')] + '</p>\n')
	f.write('<table border="1" style="width:100%">' + '\n')
	#
	# row -- header
	#
	f.write('<tr>\n')
	for i in range(imgNum):
		imgIdx = i+1
		imgUrl = line[titles.index('"Input.image_url' + str(imgIdx)+'"')]
		f.write('<th><a href="'+imgUrl.replace('"','')+'" target="_blank">img_' + str(imgIdx) + '</a></th>' + '\n')
	f.write('</tr>\n')
	#
	# row -- image
	#
	f.write('<tr>\n')
	for i in range(imgNum):
		imgIdx = i+1
		imgUrl = line[titles.index('"Input.image_url' + str(imgIdx)+'"')]
		f.write('<td><img  class="imagecontainer" src="'+imgUrl.replace('"','')+'" alt="img' + str(imgIdx) + '" height="100" width="150"></td>' + '\n')
	f.write('</tr>\n')
	#
	# overall score
	#
	f.write('<tr>\n')
	for i in range(imgNum):
		imgIdx = i+1
		overallScore = line[titles.index('"Answer.overallScore' + str(imgIdx)+'"')]
		f.write('<td><font size=4>score=' + overallScore.replace('"','') + '</font></td>' + '\n')
	f.write('</tr>\n')
	#
	# attributes
	#
	f.write('<tr>\n')
	for i in range(imgNum):
		imgIdx = i+1
		Content = line[titles.index('"Answer.Content' + str(imgIdx)+'"')]
		ObjectEmphasis = line[titles.index('"Answer.ObjectEmphasis' + str(imgIdx)+'"')]
		Light = line[titles.index('"Answer.choiceLight' + str(imgIdx)+'"')]
		ColorHarmony = line[titles.index('"Answer.ColorHarmony' + str(imgIdx)+'"')]
		StrongColor = line[titles.index('"Answer.StrongColor' + str(imgIdx)+'"')]
		DoF = line[titles.index('"Answer.DoF' + str(imgIdx)+'"')]
		MotionBlur = line[titles.index('"Answer.MotionBlur' + str(imgIdx)+'"')]
		RuleOfThirds = line[titles.index('"Answer.RuleOfThirds' + str(imgIdx)+'"')]
		Repetition = line[titles.index('"Answer.Repetition' + str(imgIdx)+'"')]
		Symmetry = line[titles.index('"Answer.Symmetry' + str(imgIdx)+'"')]
		VisualBalance = line[titles.index('"Answer.VisualBalance' + str(imgIdx)+'"')]
		f.write('<td>1. content: ' + Content.replace('"','') + '<br>' )
		f.write('2. ObjectEmpha: ' + ObjectEmphasis.replace('"','') + '<br>' )
		f.write('3. Light: ' + Light.replace('"','') + '<br>' )
		f.write('4. ColrHarmony: ' + ColorHarmony.replace('"','') + '<br>' )
		f.write('5. StrongColr: ' + StrongColor.replace('"','') + '<br>' )
		f.write('6. DoF: ' + DoF.replace('"','') + '<br>' )
		f.write('7. MotionBlur: ' + MotionBlur.replace('"','') + '<br>' )
		f.write('8. RuleOf3rds: ' + RuleOfThirds.replace('"','') + '<br>' )
		f.write('9. Repetition: ' + Repetition.replace('"','') + '<br>' )
		f.write('10. Symmetry: ' + Symmetry.replace('"','') + '<br>' )
		f.write('11. VisualBalan: ' + VisualBalance.replace('"','') + '<br>' )
		f.write('</td>\n')
	f.write('</tr>\n')
	f.write('</table>\n')
	f.write('<p>&nbsp;</p><p>&nbsp;</p>\n')

f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()





####################################################################################################
########################## multiple worker's summary ##########################
####################################################################################################
# get all images' ratings
print ('multiple worker`s summary')
workerNum = 5
imgDict = dict()
count = 0
for lineIdx in lines[1:]:
	count = count + 1
	lines[count] = lines[count].strip()
	line = lines[count]
	line = line.split(',')
	for i in range(imgNum):
		imgIdx = i+1
		Content = line[titles.index('"Answer.Content' + str(imgIdx)+'"')]
		ObjectEmphasis = line[titles.index('"Answer.ObjectEmphasis' + str(imgIdx)+'"')]
		Light = line[titles.index('"Answer.choiceLight' + str(imgIdx)+'"')]
		ColorHarmony = line[titles.index('"Answer.ColorHarmony' + str(imgIdx)+'"')]
		StrongColor = line[titles.index('"Answer.StrongColor' + str(imgIdx)+'"')]
		DoF = line[titles.index('"Answer.DoF' + str(imgIdx)+'"')]
		MotionBlur = line[titles.index('"Answer.MotionBlur' + str(imgIdx)+'"')]
		RuleOfThirds = line[titles.index('"Answer.RuleOfThirds' + str(imgIdx)+'"')]
		Repetition = line[titles.index('"Answer.Repetition' + str(imgIdx)+'"')]
		Symmetry = line[titles.index('"Answer.Symmetry' + str(imgIdx)+'"')]
		VisualBalance = line[titles.index('"Answer.VisualBalance' + str(imgIdx)+'"')]
		imgUrl = line[titles.index('"Input.image_url' + str(imgIdx)+'"')]
		WorkerId = line[titles.index('"WorkerId"')]
		overallScore = line[titles.index('"Answer.overallScore' + str(imgIdx)+'"')]
		structData=list()
		structData.append(imgUrl)
		structData.append(WorkerId)
		structData.append(Content)		#1
		structData.append(ObjectEmphasis)	#2
		structData.append(Light)		#3
		structData.append(ColorHarmony)		#4
		structData.append(StrongColor)		#5
		structData.append(DoF)			#6
		structData.append(MotionBlur)		#7
		structData.append(RuleOfThirds)		#8
		structData.append(Repetition)		#9
		structData.append(Symmetry)		#10
		structData.append(VisualBalance)	#11
		structData.append(overallScore)		#12
		if not (imgUrl in imgDict):
			imgDict[imgUrl] = list()
			imgDict[imgUrl].append(structData)
		else:
			imgDict[imgUrl].append(structData)



sortedImageURL = list()
sortedImageScore = list()
sortedImageStd = list()
sortedImageContent = list()
sortedImageObject = list()
sortedImageLight = list()
sortedImageColorHarmony = list()
sortedImageVividColor = list()
sortedImageDOF = list()
sortedImageMotionBlur = list()
sortedImageRuleOf3rds = list()
sortedImageRepetition = list()
sortedImageSymmetry = list()
sortedImageVisualBalance = list()
scoreSymbol=dict()
scoreSymbol['"n"']=0.0
scoreSymbol['"<font color="green">Pos</font>"']=1.0
scoreSymbol['"<font color="red">Neg</font>"']=-1.0
htmlFile = 'visualizeResultSummary.html'
count = 0
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
for key in imgDict.keys():
	count = count + 1
	f.write('<table border="1" style="width:100%">' + '\n')
	f.write('<col width="20%">')
	for i in range(workerNum):
		f.write('<col width="15%">')
	f.write('<col width="5%">')
	f.write('<tr>\n')
	f.write('<td rowspan="5"><a href="'+ key.replace('"','') +'" target="_blank"><img  class="imagecontainer" src="'+key.replace('"','')+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a></td>' + '\n')
	path,filename = os.path.split(key.replace('"',''))
	path,filename1 = os.path.split(path)
	path,filename2 = os.path.split(path)
	filename3 = filename2[0:filename2.find('.')]
	imgName = filename3+'_'+filename1+'_'+filename
	f.write('<td colspan="6">'+ str(count) + '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;' + key.replace('"','') + '<br>' + imgName)
	f.write('</td>\n')
	f.write('</tr>\n')
	f.write('<tr>\n')
	sortedImageURL.append(key.replace('"',''))
	for i in range(len(imgDict[key])):
		f.write('<td>')
		f.write('worker'+str(i+1))
		f.write('</td>\n')
	f.write('<td>Comment</td>')
	f.write('</tr>\n')

	f.write('<tr>\n')
	#f.write('<td></td>')
	for i in range(len(imgDict[key])):
		structData=imgDict[key][i]
		f.write('<td>workerID:<br>' + structData[1].replace('"','') )
	f.write('</tr>\n')


	f.write('<tr>\n')
	#f.write('<td></td>')
	scoreList = list()
	for i in range(len(imgDict[key])):
		structData=imgDict[key][i]
		scoreList.append(int(structData[13].replace('"','')))
		if structData[13].replace('"','') == '0':
			f.write('<td><strong><font color="red"> overall score=' + structData[13].replace('"','') + '</font></strong></td>\n')
		else:
			f.write('<td><strong>overall score=' + structData[13].replace('"','') + '</strong></td>\n')
	f.write('</tr>\n')
	scoreList = np.asarray(scoreList)
	aveScore = scoreList.mean()

	f.write('<tr>\n')
	valContent = 0.0
	valObject = 0.0
	valLight = 0.0
	valColorHarmony = 0.0
	valVividColor = 0.0
	valDOF = 0.0
	valMotionBlur = 0.0
	valRuleOf3rds = 0.0
	valRepetition = 0.0
	valSymmetry = 0.0
	valVisualBalance = 0.0
	for i in range(len(imgDict[key])):
		structData=imgDict[key][i]
		f.write('<td>1. content: ' + structData[2].replace('"','') + '<br>' )
		valContent = valContent + scoreSymbol[structData[2]]
		f.write('2. ObjectEmpha: ' + structData[3].replace('"','') + '<br>' )
		valObject = valObject + scoreSymbol[structData[3]]
		f.write('3. Light: ' + structData[4].replace('"','') + '<br>' )
		valLight = valLight +scoreSymbol[structData[4]]
		f.write('4. ColrHarmony: ' + structData[5].replace('"','') + '<br>' )
		valColorHarmony = valColorHarmony + scoreSymbol[structData[5]]
		f.write('5. StrongColr: ' + structData[6].replace('"','') + '<br>' )
		valVividColor = valVividColor + scoreSymbol[structData[6]]
		f.write('6. DoF: ' + structData[7].replace('"','') + '<br>' )
		valDOF = valDOF + scoreSymbol[structData[7]]
		f.write('7. MotionBlur: ' + structData[8].replace('"','') + '<br>' )
		valMotionBlur = valMotionBlur + scoreSymbol[structData[8]]
		f.write('8. RuleOf3rds: ' + structData[9].replace('"','') + '<br>' )
		valRuleOf3rds = valRuleOf3rds + scoreSymbol[structData[9]]
		f.write('9. Repetition: ' + structData[10].replace('"','') + '<br>' )
		valRepetition = valRepetition + scoreSymbol[structData[10]]
		f.write('10. Symmetry: ' + structData[11].replace('"','') + '<br>' )
		valSymmetry = valSymmetry + scoreSymbol[structData[11]]
		f.write('11. VisualBalan: ' + structData[12].replace('"','') + '<br>' )
		valVisualBalance = valVisualBalance + scoreSymbol[structData[12]]
		f.write('</td>\n')
	sortedImageContent.append(valContent*1.0/len(imgDict[key]))
	sortedImageObject.append(valObject*1.0/len(imgDict[key]))
	sortedImageLight.append(valLight*1.0/len(imgDict[key]))
	sortedImageColorHarmony.append(valColorHarmony*1.0/len(imgDict[key]))
	sortedImageVividColor.append(valVividColor*1.0/len(imgDict[key]))
	sortedImageDOF.append(valDOF*1.0/len(imgDict[key]))
	sortedImageMotionBlur.append(valMotionBlur*1.0/len(imgDict[key]))
	sortedImageRuleOf3rds.append(valRuleOf3rds*1.0/len(imgDict[key]))
	sortedImageRepetition.append(valRepetition*1.0/len(imgDict[key]))
	sortedImageSymmetry.append(valSymmetry*1.0/len(imgDict[key]))
	sortedImageVisualBalance.append(valVisualBalance*1.0/len(imgDict[key]))
	for i in range(workerNum-len(imgDict[key])):
		f.write('<td></td>')
	f.write('<td>')
	f.write('#workers='+ str(len(imgDict[key])) + '<br>')
	f.write('aveScore='+'%0.3f' %scoreList.mean() + '<br>')
	if scoreList.std() >= 1:
		f.write('<font color="red"><strong>stdScore='+'%0.3f' %scoreList.std() + '</strong></font><br>')
	else:
		f.write('stdScore='+'%0.3f' %scoreList.std() + '<br>')
	f.write('medianScore='+'%0.3f' %np.median(scoreList) + '<br>')
	f.write('highestScore=' + str(scoreList.max()) + '<br>')
	f.write('lowestScore=' + str(scoreList.min()) + '<br>')
	sortedImageScore.append(scoreList.mean())
	sortedImageStd.append(scoreList.std())
	imgDict[key].append(scoreList)
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	f.write('<p>1. content: ' + str(sortedImageContent[len(sortedImageContent)-1]) + '<br>' )
	f.write('2. ObjectEmpha: ' + str(sortedImageObject[len(sortedImageObject)-1]) + '<br>' )
	f.write('3. Light: ' + str(sortedImageLight[len(sortedImageLight)-1]) + '<br>' )
	f.write('4. ColrHarmony: ' + str(sortedImageColorHarmony[len(sortedImageColorHarmony)-1]) + '<br>' )
	f.write('5. StrongColr: ' + str(sortedImageVividColor[len(sortedImageVividColor)-1]) + '<br>' )
	f.write('6. DoF: ' + str(sortedImageDOF[len(sortedImageDOF)-1]) + '<br>' )
	f.write('7. MotionBlur: ' + str(sortedImageMotionBlur[len(sortedImageMotionBlur)-1]) + '<br>' )
	f.write('8. RuleOf3rds: ' + str(sortedImageRuleOf3rds[len(sortedImageRuleOf3rds)-1]) + '<br>' )
	f.write('9. Repetition: ' + str(sortedImageRepetition[len(sortedImageRepetition)-1]) + '<br>' )
	f.write('10. Symmetry: ' + str(sortedImageSymmetry[len(sortedImageSymmetry)-1]) + '<br>' )
	f.write('11. VisualBalan: ' + str(sortedImageVisualBalance[len(sortedImageVisualBalance)-1]) + '<br>' )
	f.write('</td>')
	f.write('</tr>\n')
	f.write('</table>\n')
	f.write('<p>&nbsp;</p><p>&nbsp;</p>\n')

f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()



##################################################
# sort images based on their average scores
##################################################
print ('sort images based on their average scores')
htmlFile = 'visualizeSortedImgAverageScore.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their overall score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
a = np.asarray(sortedImageScore)
a = np.argsort(a)
a = a[::-1]
gridNumPerRow=5
gridCount = 0
count = 0
for i in range(len(a)):
	count = count + 1
	gridCount = gridCount + 1
	imgIdx = a[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageScore[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	path,filename = os.path.split(imgURL)
	path,filename1 = os.path.split(path)
	path,filename2 = os.path.split(path)
	filename3 = filename2[0:filename2.find('.')]
	imgName = filename3+'_'+filename1+'_'+filename
	f.write('<td>'+imgURL+'<br>'+imgName+'<br>')
	f.write('<a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('<strong>aveScore=%.3f' %(aveScore) + '</strong><br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('<p><br>imageNO.'+str(count))
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()









##################################################
# sort images based on their calibrated average scores
##################################################
print ('sort images based on their calibrated average scores')
htmlFile = 'visualizeSortedImgCalibScore.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by the calibrated average score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
a = np.asarray(sortedImageScore)
a = np.argsort(a)
a = a[::-1]
gridNumPerRow=5
gridCount = 0
count = 0
for i in range(len(a)):
	count = count + 1
	gridCount = gridCount + 1
	imgIdx = a[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageScore[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	scoreList.sort()
	if scoreList.min()==0 and len(np.where(scoreList==0)[0]==1) and len(scoreList)>1:
		scoreList =  scoreList[1:]
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if minScore==0 and len(np.where(scoreList==0)[0]>1):
		gridCount = gridCount - 1
	else:
		if gridCount == 1:
			f.write('<tr>\n')
		path,filename = os.path.split(imgURL)
		path,filename1 = os.path.split(path)
		path,filename2 = os.path.split(path)
		filename3 = filename2[0:filename2.find('.')]
		imgName = filename3+'_'+filename1+'_'+filename
		f.write('<td>'+imgURL+'<br>'+imgName+'<br>')
		f.write('<a href="'+ imgURL +'" target="_blank"><img class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
		f.write('<p><br>imageNO.'+str(count))
		f.write('<p><p>#workers='+ str(len(scoreList)) + '<br>')
		f.write('<strong>CalibScore=%.3f' %(aveScore) + '</strong><br>')
		f.write('<strong>aveScore=%.3f' %(imgScore) + '</strong><br>')
		f.write('medianScore=' + str(medianScore) + '<br>')
		f.write('stdScore=%.3f' %(stdScore) + '<br>')
		f.write('maxScore=' + str(maxScore) + '<br>')
		f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')

		f.write('<p>1. content: ' + str(sortedImageContent[imgIdx]) + '<br>' )
		f.write('2. ObjectEmpha: ' + str(sortedImageObject[imgIdx]) + '<br>' )
		f.write('3. Light: ' + str(sortedImageLight[imgIdx]) + '<br>' )
		f.write('4. ColrHarmony: ' + str(sortedImageColorHarmony[imgIdx]) + '<br>' )
		f.write('5. StrongColr: ' + str(sortedImageVividColor[imgIdx]) + '<br>' )
		f.write('6. DoF: ' + str(sortedImageDOF[imgIdx]) + '<br>' )
		f.write('7. MotionBlur: ' + str(sortedImageMotionBlur[imgIdx]) + '<br>' )
		f.write('8. RuleOf3rds: ' + str(sortedImageRuleOf3rds[imgIdx]) + '<br>' )
		f.write('9. Repetition: ' + str(sortedImageRepetition[imgIdx]) + '<br>' )
		f.write('10. Symmetry: ' + str(sortedImageSymmetry[imgIdx]) + '<br>' )
		f.write('11. VisualBalan: ' + str(sortedImageVisualBalance[imgIdx]) + '<br>' )

		f.write('</td>')
		if gridCount == gridNumPerRow:
			f.write('</tr>\n')
			gridCount = 0

f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()







'''

##################################################
# sort images based on attributes
##################################################
print ('sort images based on attributes')
a = np.asarray(sortedImageScore)
a = np.argsort(a)
a = a[::-1]

contentList = np.asarray(sortedImageContent)
contentList = np.argsort(contentList)
contentList = contentList[::-1]

objectList = np.asarray(sortedImageObject)
objectList = np.argsort(objectList)
objectList = objectList[::-1]

lightList = np.asarray(sortedImageLight)
lightList = np.argsort(lightList)
lightList = lightList[::-1]

colorHarmonyList = np.asarray(sortedImageColorHarmony)
colorHarmonyList = np.argsort(colorHarmonyList)
colorHarmonyList = colorHarmonyList[::-1]

VividColorList = np.asarray(sortedImageVividColor)
VividColorList = np.argsort(VividColorList)
VividColorList = VividColorList[::-1]

DOFList = np.asarray(sortedImageDOF)
DOFList = np.argsort(DOFList)
DOFList = DOFList[::-1]

MotionBlurList = np.asarray(sortedImageMotionBlur)
MotionBlurList = np.argsort(MotionBlurList)
MotionBlurList = MotionBlurList[::-1]

RuleOf3rdsList = np.asarray(sortedImageRuleOf3rds)
RuleOf3rdsList = np.argsort(RuleOf3rdsList)
RuleOf3rdsList = RuleOf3rdsList[::-1]

RepetitionList = np.asarray(sortedImageRepetition)
RepetitionList = np.argsort(RepetitionList)
RepetitionList = RepetitionList[::-1]

SymmetryList = np.asarray(sortedImageSymmetry)
SymmetryList = np.argsort(SymmetryList)
SymmetryList = SymmetryList[::-1]

VisualBalanceList = np.asarray(sortedImageVisualBalance)
VisualBalanceList = np.argsort(VisualBalanceList)
VisualBalanceList = VisualBalanceList[::-1]




##################################################
##############   content  ##################
##################################################
print ('\tcontent')
htmlFile = 'visualizeSortedImgContent.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their overall score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(contentList)):
	gridCount = gridCount + 1
	imgIdx = contentList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageContent[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>content:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()





##################################################
##############   object  		##################
##################################################
print ('\tobject')
htmlFile = 'visualizeSortedImgObject.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their object emphasis score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(objectList)):
	gridCount = gridCount + 1
	imgIdx = objectList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageObject[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>ObjectEmphasis:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()





##################################################
##############   Light  ##################
##################################################
print ('\tLight')
htmlFile = 'visualizeSortedImgLight.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their lighting score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(contentList)):
	gridCount = gridCount + 1
	imgIdx = lightList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageLight[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>Light:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()





##################################################
##############   Color Harmony  ##################
##################################################
print ('\tColor Harmony')
htmlFile = 'visualizeSortedImgColorHarmony.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their color harmony score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(colorHarmonyList)):
	gridCount = gridCount + 1
	imgIdx = colorHarmonyList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageColorHarmony[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>ColorHarmony:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()





##################################################
##############   Vivid Color  ##################
##################################################
print ('\tvivid color')
htmlFile = 'visualizeSortedImgVividColor.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their vivid color score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(VividColorList)):
	gridCount = gridCount + 1
	imgIdx = VividColorList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageVividColor[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>VividColor:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()





##################################################
##############   DoF  ##################
##################################################
print ('\tDoF')
htmlFile = 'visualizeSortedImgDoF.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their DoF score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(DOFList)):
	gridCount = gridCount + 1
	imgIdx = DOFList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageDOF[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>DoF:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()






##################################################
##############   Motion Blur  ##################
##################################################
print ('\tMotion Blur')
htmlFile = 'visualizeSortedImgMotionBlur.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their motion blur score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(MotionBlurList)):
	gridCount = gridCount + 1
	imgIdx = MotionBlurList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageMotionBlur[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>MotionBlur:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()





##################################################
##############   Rule of Thirds  ##################
##################################################
print ('\tRule of Thirds')
htmlFile = 'visualizeSortedImgRuleOf3rds.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their Rule of Thirds score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(RuleOf3rdsList)):
	gridCount = gridCount + 1
	imgIdx = RuleOf3rdsList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageRuleOf3rds[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>RuleOf3rds:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()






##################################################
##############   Repetition  ##################
##################################################
print ('\tRepetition')
htmlFile = 'visualizeSortedImgRepetition.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their repetition score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(RepetitionList)):
	gridCount = gridCount + 1
	imgIdx = RepetitionList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageRepetition[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>Repetition:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()








##################################################
##############   Symmetry  ##################
##################################################
print ('\tSymmetry')
htmlFile = 'visualizeSortedImgSymmetry.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their symmetry score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(SymmetryList)):
	gridCount = gridCount + 1
	imgIdx = SymmetryList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageSymmetry[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>symmetry:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()






##################################################
##############   Balancing Elements  ##################
##################################################
print ('\tBalancing Elements')
htmlFile = 'visualizeSortedImgVisualBalance.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('list sorted images by their Balancing Elements score\n<br><p>&nbsp;</p>\n')
f.write('<table border="1" style="width:100%">' + '\n')
gridNumPerRow=5
gridCount = 0
for i in range(len(VisualBalanceList)):
	gridCount = gridCount + 1
	imgIdx = VisualBalanceList[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageVisualBalance[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	if gridCount == 1:
		f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img' + str(imgIdx) + '" height="300" width="450"></a><br> \n')
	f.write('<strong>VisualBalance:%.3f' %imgScore +'</strong><br>')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '<br><p>&nbsp;</p>')
	f.write('</td>')
	if gridCount == gridNumPerRow:
		f.write('</tr>\n')
		gridCount = 0
f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()










####################################################################################################
############## put them all in one page  ###########################################################
####################################################################################################
print ('put them all together')
htmlFile = 'visualizeSortedImgAttributes.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
f.write('<table border="1" style="width:100%">' + '\n')
for i in range(len(contentList)):
	imgIdx = a[i]
	imgURL = sortedImageURL[imgIdx]
	imgScore = sortedImageScore[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	#imgDict[key].append(scoreList.mean())
	#imgDict[key].append(np.median(scoreList))
	#imgDict[key].append(scoreList.std())
	#imgDict[key].append(scoreList.max())
	#imgDict[key].append(scoreList.min())
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]

	imgIdxContent = contentList[i]
	imgURLContent = sortedImageURL[imgIdxContent]
	contentVal = sortedImageContent[imgIdxContent]

	imgIdxObject = objectList[i]
	imgURLObject = sortedImageURL[imgIdxObject]
	objectVal = sortedImageObject[imgIdxObject]

	imgIdxLight = lightList[i]
	imgURLLight = sortedImageURL[imgIdxLight]
	lightVal = sortedImageLight[imgIdxLight]

	imgIdxColorHarmony = colorHarmonyList[i]
	imgURLColorHarmony = sortedImageURL[imgIdxColorHarmony]
	colorHarmonyVal = sortedImageColorHarmony[imgIdxColorHarmony]

	imgIdxVividColor = VividColorList[i]
	imgURLVividColor = sortedImageURL[imgIdxVividColor]
	vividColorVal = sortedImageVividColor[imgIdxVividColor]

	imgIdxDOF = DOFList[i]
	imgURLDOF = sortedImageURL[imgIdxDOF]
	DOFVal = sortedImageDOF[imgIdxDOF]

	imgIdxMotionBlur = MotionBlurList[i]
	imgURLMotionBlur = sortedImageURL[imgIdxMotionBlur]
	motionBlurVal = sortedImageMotionBlur[imgIdxMotionBlur]

	imgIdxRuleOf3rds = RuleOf3rdsList[i]
	imgURLRuleOf3rds = sortedImageURL[imgIdxRuleOf3rds]
	ruleOf3rdsVal = sortedImageRuleOf3rds[imgIdxRuleOf3rds]

	imgIdxRepetition = RepetitionList[i]
	imgURLRepetition = sortedImageURL[imgIdxRepetition]
	repetitionVal = sortedImageRepetition[imgIdxRepetition]

	imgIdxSymmetry = SymmetryList[i]
	imgURLSymmetry = sortedImageURL[imgIdxSymmetry]
	symmetryVal = sortedImageSymmetry[imgIdxSymmetry]

	imgIdxVisualBalance = VisualBalanceList[i]
	imgURLVisualBalance = sortedImageURL[imgIdxVisualBalance]
	visualBalanceVal = sortedImageVisualBalance[imgIdxVisualBalance]

	#imgScore = sortedImageScore[imgIdx]
	#aveScore = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	#medianScore = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	#stdScore = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	#maxScore = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	#minScore = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]

	f.write('<tr>\n')
	f.write('<td><p>&nbsp;</p><strong>aveScore: %.3f' %aveScore + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>Content: %.3f' %contentVal + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>Object: %.3f' %objectVal + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>Light: %.3f' %lightVal + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>ColorHarmony: %.3f' %colorHarmonyVal + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>VividColor: %.3f' %vividColorVal + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>DoF: %.3f' %DOFVal + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>MotionBlur: %.3f' %motionBlurVal + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>RuleOf3rds: %.3f' %ruleOf3rdsVal + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>Repetition: %.3f' %repetitionVal + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>Symmetry: %.3f' %symmetryVal + '</strong></td>\n')
	f.write('<td><p>&nbsp;</p><strong>VisualBalance: %.3f' %visualBalanceVal + '</strong></td>\n')
	f.write('</tr>\n')
	f.write('<tr>\n')
	f.write('<td>'+imgURL+'</td>\n')
	f.write('<td>'+imgURLContent+'</td>\n')
	f.write('<td>'+imgURLObject+'</td>\n')
	f.write('<td>'+imgURLLight+'</td>\n')
	f.write('<td>'+imgURLColorHarmony+'</td>\n')
	f.write('<td>'+imgURLVividColor+'</td>\n')
	f.write('<td>'+imgURLDOF+'</td>\n')
	f.write('<td>'+imgURLMotionBlur+'</td>\n')
	f.write('<td>'+imgURLRuleOf3rds+'</td>\n')
	f.write('<td>'+imgURLRepetition+'</td>\n')
	f.write('<td>'+imgURLSymmetry+'</td>\n')
	f.write('<td>'+imgURLVisualBalance+'</td>\n')
	f.write('</tr>\n')
	f.write('<tr>\n')
	f.write('<td><a href="'+ imgURL +'" target="_blank"><img  class="imagecontainer" src="'+imgURL+'" alt="img" height="200" width="300"></a><br>' + '\n')
	f.write('#workers='+ str(len(scoreList)) + '<br>')
	f.write('aveScore=%.3f' %(aveScore) + '<br>')
	f.write('medianScore=' + str(medianScore) + '<br>')
	f.write('stdScore=%.3f' %(stdScore) + '<br>')
	f.write('maxScore=' + str(maxScore) + '<br>')
	f.write('minScore=' + str(minScore) + '</td>')
	f.write('<td><a href="'+ imgURLContent +'" target="_blank"><img  class="imagecontainer" src="'+imgURLContent+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('<td><a href="'+ imgURLObject +'" target="_blank"><img  class="imagecontainer" src="'+imgURLObject+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('<td><a href="'+ imgURLLight +'" target="_blank"><img  class="imagecontainer" src="'+imgURLLight+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('<td><a href="'+ imgURLColorHarmony +'" target="_blank"><img  class="imagecontainer" src="'+imgURLColorHarmony+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('<td><a href="'+ imgURLVividColor +'" target="_blank"><img  class="imagecontainer" src="'+imgURLVividColor+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('<td><a href="'+ imgURLDOF +'" target="_blank"><img  class="imagecontainer" src="'+imgURLDOF+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('<td><a href="'+ imgURLMotionBlur +'" target="_blank"><img  class="imagecontainer" src="'+imgURLMotionBlur+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('<td><a href="'+ imgURLRuleOf3rds +'" target="_blank"><img  class="imagecontainer" src="'+imgURLRuleOf3rds+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('<td><a href="'+ imgURLRepetition +'" target="_blank"><img  class="imagecontainer" src="'+imgURLRepetition+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('<td><a href="'+ imgURLSymmetry +'" target="_blank"><img  class="imagecontainer" src="'+imgURLSymmetry+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('<td><a href="'+ imgURLVisualBalance +'" target="_blank"><img  class="imagecontainer" src="'+imgURLVisualBalance+'" alt="img" height="200" width="300"></a></td>' + '\n')
	f.write('</tr>\n')

f.write('</table>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()









##################################################
# check workers' performance
##################################################
print ('check workers` performance')
workerDict = dict()
count = 0
for lineIdx in lines[1:]:
	count = count + 1
	lines[count] = lines[count].strip()
	line = lines[count]
	line = line.split(',')
	workerID = line[titles.index('"WorkerId"')]
	if not workerDict.has_key(workerID):
		workerDict[workerID] = list()
	for i in range(imgNum):
		imgIdx = i+1
		overallScore = line[titles.index('"Answer.overallScore' + str(imgIdx)+'"')]
		WorkTimeInSeconds = line[titles.index('"WorkTimeInSeconds"')]
		imgUrl = line[titles.index('"Input.image_url' + str(imgIdx)+'"')]
		Content = line[titles.index('"Answer.Content' + str(imgIdx)+'"')]
		ObjectEmphasis = line[titles.index('"Answer.ObjectEmphasis' + str(imgIdx)+'"')]
		Light = line[titles.index('"Answer.choiceLight' + str(imgIdx)+'"')]
		ColorHarmony = line[titles.index('"Answer.ColorHarmony' + str(imgIdx)+'"')]
		StrongColor = line[titles.index('"Answer.StrongColor' + str(imgIdx)+'"')]
		DoF = line[titles.index('"Answer.DoF' + str(imgIdx)+'"')]
		MotionBlur = line[titles.index('"Answer.MotionBlur' + str(imgIdx)+'"')]
		RuleOfThirds = line[titles.index('"Answer.RuleOfThirds' + str(imgIdx)+'"')]
		Repetition = line[titles.index('"Answer.Repetition' + str(imgIdx)+'"')]
		Symmetry = line[titles.index('"Answer.Symmetry' + str(imgIdx)+'"')]
		VisualBalance = line[titles.index('"Answer.VisualBalance' + str(imgIdx)+'"')]
		structData = dict()
		structData['overallScore'] = overallScore
		structData['WorkTimeInSeconds'] = WorkTimeInSeconds
		structData['imgUrl'] = imgUrl
		structData['Content'] = Content
		structData['ObjectEmphasis'] = ObjectEmphasis
		structData['Light'] = Light
		structData['ColorHarmony'] = ColorHarmony
		structData['StrongColor'] = StrongColor
		structData['DoF'] = DoF
		structData['MotionBlur'] = MotionBlur
		structData['RuleOfThirds'] = RuleOfThirds
		structData['Repetition'] = Repetition
		structData['Symmetry'] = Symmetry
		structData['VisualBalance'] = VisualBalance
		structData['workerID'] = workerID
		workerDict[workerID].append(structData)


htmlFile = 'visualizeWokerPerformance.html'
f = open(htmlFile, 'w')
f.write('<!DOCTYPE html>\n<html>\n<body>\n')
count = 0
for workerKey in workerDict.keys():
	count = count + 1
	f.write('NO.'+str(count)+'&nbsp;&nbsp;&nbsp;')
	f.write('workerID: ' + workerKey + '<br>\n')
	f.write('number of images rated: ' + str(len(workerDict[workerKey])) + '<br>\n')
	f.write('<table border="1">' + '\n')
	f.write('<tr>\n')
	for i in range(len(workerDict[workerKey])):
		structData=workerDict[workerKey][i]
		f.write('<td>')
		f.write('image-'+str(i+1))
		f.write('</td>')
	f.write('</tr>\n')
	f.write('<tr>\n')
	for i in range(len(workerDict[workerKey])):
		structData=workerDict[workerKey][i]
		f.write('<td><a href="'+ structData['imgUrl'].replace('"','') +'" target="_blank"><img  class="imagecontainer" src="'+structData['imgUrl'].replace('"','')+'" alt="img' + str(imgIdx) + '" height="150" width="200"></a></td>\n')
	f.write('</tr>\n')
	for i in range(len(workerDict[workerKey])):
		structData=workerDict[workerKey][i]
		imgUrl=structData['imgUrl']
		scoreList = imgDict[imgUrl][len(imgDict[imgUrl])-1]
		aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
		medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
		stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
		maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
		minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
		f.write('<td>')
		f.write('#workers='+ str(len(scoreList)) + '<br>')
		f.write('aveScore=%.3f' %(aveScore) + '<br>')
		f.write('medianScore=' + str(medianScore) + '<br>')
		f.write('stdScore=%.3f' %(stdScore) + '<br>')
		f.write('maxScore=' + str(maxScore) + '<br>')
		f.write('minScore=' + str(minScore) + '<br>')
		f.write('</td>')
	f.write('</tr>\n')
	f.write('<tr>\n')
	for i in range(len(workerDict[workerKey])):
		structData=workerDict[workerKey][i]
		f.write('<td>')
		f.write('score:'+structData['overallScore'].replace('"',''))
		f.write('</td>')
	f.write('</tr>\n')
	for i in range(len(workerDict[workerKey])):
		structData=workerDict[workerKey][i]
		f.write('<td>')
		timeUsed = int(structData['WorkTimeInSeconds'].replace('"',''))/10.0
		if timeUsed < 15:
			f.write('<font color="red"><strong>time~%.3f'% (timeUsed) +'</strong></font>')
		else:
			f.write('time~%.3f'% (timeUsed) )
		f.write('</td>')
	f.write('</tr>\n')
	f.write('<tr>\n')
	for i in range(len(workerDict[workerKey])):
		structData=workerDict[workerKey][i]
		f.write('<td>1. content: ' + structData['Content'].replace('"','') + '<br>' )
		f.write('2. ObjectEmpha: ' + structData['ObjectEmphasis'].replace('"','') + '<br>' )
		f.write('3. Light: ' + structData['Light'].replace('"','') + '<br>' )
		f.write('4. ColrHarmony: ' + structData['ColorHarmony'].replace('"','') + '<br>' )
		f.write('5. StrongColr: ' + structData['StrongColor'].replace('"','') + '<br>' )
		f.write('6. DoF: ' + structData['DoF'].replace('"','') + '<br>' )
		f.write('7. MotionBlur: ' + structData['MotionBlur'].replace('"','') + '<br>' )
		f.write('8. RuleOf3rds: ' + structData['RuleOfThirds'].replace('"','') + '<br>' )
		f.write('9. Repetition: ' + structData['Repetition'].replace('"','') + '<br>' )
		f.write('10. Symmetry: ' + structData['Symmetry'].replace('"','') + '<br>' )
		f.write('11. VisualBalan: ' + structData['VisualBalance'].replace('"','') + '<br>' )
		f.write('</td>\n')
	f.write('</tr>\n')
	f.write('</table>\n')
	f.write('<p>&nbsp;</p><p>&nbsp;</p>\n')
f.write( '<style type="text/css">\n .imagecontainer {\ndisplay:block; \nfloat: left; \nposition: relative; \nheight:auto;\nheight:auto; \nmax-width: 300px;\nmax-height: 300px;\n}\n</style>')
f.write('</body>\n</html>\n')
f.close()





##################################################
################# check the file #################
##################################################
print ('check the file')
count = 1
for lineIdx in lines[1:]:
	lines[count] = lines[count].strip()
	line = lines[count]
	line = line.split(',')

	#print ('HITID'), line[0]
	#print line
	for i in range(imgNum):
		imgIdx = i+1
		#
		# get the index
		#
		timeUsed = line[titles.index('"WorkTimeInSeconds"')]
		imgUrl = line[titles.index('"Input.image_url' + str(imgIdx)+'"')]
		Content = line[titles.index('"Answer.Content' + str(imgIdx)+'"')]
		ObjectEmphasis = line[titles.index('"Answer.ObjectEmphasis' + str(imgIdx)+'"')]
		Light = line[titles.index('"Answer.choiceLight' + str(imgIdx)+'"')]
		ColorHarmony = line[titles.index('"Answer.ColorHarmony' + str(imgIdx)+'"')]
		StrongColor = line[titles.index('"Answer.StrongColor' + str(imgIdx)+'"')]
		DoF = line[titles.index('"Answer.DoF' + str(imgIdx)+'"')]
		MotionBlur = line[titles.index('"Answer.MotionBlur' + str(imgIdx)+'"')]
		RuleOfThirds = line[titles.index('"Answer.RuleOfThirds' + str(imgIdx)+'"')]
		Repetition = line[titles.index('"Answer.Repetition' + str(imgIdx)+'"')]
		Symmetry = line[titles.index('"Answer.Symmetry' + str(imgIdx)+'"')]
		VisualBalance = line[titles.index('"Answer.VisualBalance' + str(imgIdx)+'"')]
		overallScore = line[titles.index('"Answer.overallScore' + str(imgIdx)+'"')]
		#
		# get the corresponding image
		#
		a = imgUrl.find('.')
		farmTag = imgUrl[9:a]
		tmpURL = imgUrl[a+1:]
		tmpURL = tmpURL.split('/')
		folderTag = tmpURL[1]
		imgTag = tmpURL[2].replace('"','')
		#print imgTag.replace('"','')
		imgName = farmTag+'_'+folderTag+'_'+imgTag
		#print ('Input.image_url' + str(imgIdx), imgUrl, timeUsed, Content, ObjectEmphasis, Light, ColorHarmony, StrongColor, DoF, MotionBlur, RuleOfThirds, Repetition, Symmetry, VisualBalance, overallScore
		if not os.path.isfile(os.path.join('/home/skong/Desktop/datasets/AestheticAttribute/whole/', imgName.replace('"',''))):
			print 'No    ', imgName.replace('"','')
		#
		# check timeused for annotating
		#
		if timeUsed<='"100"':
			print imgName.replace('"',''), '\tattention the time used on annotation!', timeUsed

		if overallScore=='"0"':
			print imgName, '\toverallScore=0!'
			shutil.copy2('/home/skong/Desktop/datasets/AestheticAttribute/whole/'+imgName, os.path.join(score0imgFolder,imgName) )
	count = count + 1

'''




####################################################################################################
###########                        generate dataset                                #################
####################################################################################################
print ('generate dataset')

#datasetFolder = r'./datasetImages'
#if os.path.isdir(datasetFolder):
#	shutil.rmtree(datasetFolder)
#os.mkdir( datasetFolder )

datasetFolder = './datasetImages'
htmlFile = 'dataset.csv'
f = open(htmlFile, 'w')
f.write('NO,imgName,URL,meanScore,stdScore,medianScore,maxScore,minScore,#workers,Content,Object,Light,ColorHarmony,VividColor,DoF,MotionBlur,RuleOfThirds,Repetition,Symmetry,BalancingElements\n')
np.random.seed(23) # always generate the same pseudo random list for fair experiment
a = np.random.permutation(len(sortedImageScore))
count = 0
scoreListStatistics = list()
for i in range(len(a)):
	count = count + 1
	imgIdx = a[i]
	imgURL = sortedImageURL[imgIdx]
	path,filename = os.path.split(imgURL)
	path,filename1 = os.path.split(path)
	path,filename2 = os.path.split(path)
	filename3 = filename2[0:filename2.find('.')]
	imgName = filename3+'_'+filename1+'_'+filename
	imgScore = sortedImageScore[imgIdx]
	scoreList = imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	scoreList.sort()
	if scoreList.min()==0 and len(np.where(scoreList==0)[0]==1) and len(scoreList)>1:
		scoreList =  scoreList[1:]
	aveScore = scoreList.mean()#imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-5]
	scoreListStatistics.append(aveScore)
	medianScore = np.median(scoreList) # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-4]
	stdScore = scoreList.std() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-3]
	maxScore = scoreList.max() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-2]
	minScore = scoreList.min() # imgDict['"'+imgURL+'"'][len(imgDict['"'+imgURL+'"'])-1]
	f.write(str(count) + ',' + imgName + ',' + imgURL + ',%.3f'%aveScore + ',%.3f'%stdScore + ',%.3f'%medianScore +',%.3f'%maxScore + ',%.3f'%minScore +','+str(len(scoreList))+',%.3f'%sortedImageContent[imgIdx] + ',%.3f'%sortedImageObject[imgIdx] + ',%.3f'%sortedImageLight[imgIdx] + ',%.3f'%sortedImageColorHarmony[imgIdx] + ',%.3f'%sortedImageVividColor[imgIdx] + ',%.3f'%sortedImageDOF[imgIdx] + ',%.3f'%sortedImageMotionBlur[imgIdx] + ',%.3f'%sortedImageRuleOf3rds[imgIdx] + ',%.3f'%sortedImageRepetition[imgIdx] + ',%.3f'%sortedImageSymmetry[imgIdx]+ ',%.3f'%sortedImageVisualBalance[imgIdx]+'\n' )

	if not os.path.isfile('/home/skong/Desktop/datasets/AestheticAttribute/whole/'+imgName):
		print (imgName, imgURL)
	elif not os.path.isfile(os.path.join(datasetFolder,imgName)):
		shutil.copy2('/home/skong/Desktop/datasets/AestheticAttribute/whole/'+imgName, os.path.join(datasetFolder,imgName) )
	else:
		donothing = True
		#shutil.copy2('/home/skong/Desktop/datasets/AestheticAttribute/whole/'+imgName, os.path.join(datasetFolder,imgName) )

f.close()

scoreListStatistics = np.asarray(scoreListStatistics)
print ('average of all scores:', scoreListStatistics.mean())
print ('# of scores in [1,2):', len(np.where((scoreListStatistics>=1) & (scoreListStatistics<2))[0] ))
print ('# of scores in [2,3):', len(np.where((scoreListStatistics>=2) & (scoreListStatistics<3))[0] ))
print ('# of scores in [3,4):', len(np.where((scoreListStatistics>=3) & (scoreListStatistics<4))[0] ))
print ('# of scores in [4,5]:', len(np.where((scoreListStatistics>=4) & (scoreListStatistics<=5))[0] ))
