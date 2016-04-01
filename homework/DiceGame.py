# -*-coding:utf-8-*-
import random

import math


class Dice:
    def __init__(self, count):
        self.count = count
        self.dices = []
        for i in range(count):
            point = random.randint(1, 6)
            self.dices.append(point)

    def waveDice(self):
        sum = 0
        for dice in self.dices:
            sum += dice
        return sum

    def s_or_b(self):
        mid_point = (3*self.count + math.ceil(float((self.count-1))/2))
        print mid_point
        sum = self.waveDice()
        if sum > mid_point:
            return True
        else:
            return False


class Player:
    def __init__(self):
        self.score = 100
        self.nums = []
        self.bets = []

    def addNum(self, num):
        self.nums.append(num)

    def addBet(self, bet):
        self.bets.append(bet)
        self.score -= bet


class Game:
    def __init__(self):
        self.GameOver = False

    def startGame(self, dice, player):
        n = int(raw_input(u'你要下几注?'))
        for i in range(n):
            self.getNum(dice, player)
            self.getBet(player)
        self.getScore(dice, player)

    def getNum(self, dice, player):
        while 1:
            try:
                inputs = int(raw_input(u'请选择押大小(输入1)或者押数字(输入2):'))
                if inputs == 1:
                    while 1:
                        sb = raw_input(u'请输入+ 代表大,- 代表小:')
                        if sb == '+' or sb == '-':
                            player.addNum(sb)
                            break
                elif inputs == 2:
                    while 1:
                        inputs = raw_input(u'请输入数字3-18:')
                        try:
                            num = int(inputs)
                            if (num >= dice.count) and (num <= 6*dice.count):
                                print u'你押的是数字:' + str(num)
                                player.addNum(num)
                                # print player.nums
                                break
                        except:
                            pass
                else:
                    continue
                break
            except:
                pass

    def getBet(self, player):
        while 1:
            inputs = raw_input(u'押多少积分?')
            try:
                bet = int(inputs)
                if (bet > 0) and (bet <= player.score):
                    player.addBet(bet)
                    print u'剩余积分:'+str(player.score)
                    break
                else:
                    if bet > player.score:
                        print u'你的积分不足!'
                    else:
                        print u'输入有误!'
            except:
                print u'请输入数字!'
                # print player.bets
                # print player.score

    def getScore(self, dice, player):
        result = dice.waveDice()
        big = dice.s_or_b()
        nums = player.nums
        bets = player.bets
        for i in range(len(nums)):
            # print i
            if nums[i] == result:
                print '获得*10'
                player.score += bets[i] * 10
            if ((not big) and nums[i] == '-') or (big and nums[i] == '+'):
                print '获得*2'
                player.score += bets[i] * 2

count = 3
game = Game()
dice = Dice(count)
player = Player()
game.startGame(dice, player)
print player.score
