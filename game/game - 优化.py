from random import randint
import pickle
#coding=utf-8

print u'请输入你的名字：'
name = raw_input()
try:
	f = open('game.txt')
	scores = pickle.load(f)
	f.close()
	score = scores.get(name)
	if score == None:
		score = [0, 0, 0]
except:
	scores = {}
	score = [0, 0, 0]

game_times = int(score[0])
min_times = int(score[1])
total_times = int(score[2])


if game_times > 0:
	avg_times = float(total_times) / game_times
else:
	avg_times = 0

print u'%s，你已经玩了%d次，最少%d轮猜出答案，平均%.2f猜出答案' % (name, game_times, min_times, avg_times)

num = randint(1, 100)
times = 0
bingo = False
print u'猜下数，1-100之间！'
while bingo == False:
	try:
		answer = input()
		if answer<101 and answer>0:
			times += 1
			if answer < num:
				print 'too small!'
			if answer > num:
				print 'too big!'
			if answer == num:
				print 'Bingo!!'
				bingo = True
			print u'It\'s',times,'times！'
		else:
			print u'输入1-100之间的数：'
	except:
		print u'输入错误！请再次输入：'

if game_times == 0 or times < min_times:
	min_times = times
total_times += times
game_times += 1

scores[name] = [str(game_times), str(min_times), str(total_times)]
	
f = open('game.txt', 'w')
pickle.dump(scores, f)
f.close()