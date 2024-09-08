class Comp1:
    def compT(self, J):
        return 2 / (J*(J-2))

    def compD(self, J):
        return 1.5 / (J*(J - 3))

    def compH(self, J):
        return 1.33333333333 / (J*(J - 4))

class Comp2:
    def compT(self, J):
        return (1/(J-2) - 1/J)

    def compD(self, J):
        return (1/(J-3) - 1/J)/2

    def compH(self, J):
        return (1/(J-4) - 1/J)/3

    def showJStats(self, J):
        T=self.compT(J)
        D=self.compD(J)
        H=self.compH(J)
        sum = T+D+H
        diff = sum - 1/J
        print(J, end='')
        if True:
            print(f' {1/(2*T + D + H):.4f}', end='')
            print(f' {1/(T + 3*D + H):.4f}', end='')
            print(f' {1/(T + D + 4*H):.4f}', end='')
        print()


comper = Comp2()
# J=7.838149
prevJ = 0
place = 1
while place >= 0.00000000000000001:
    for n in range(0,10):
        J = prevJ + n*place
        if J<=4:
            continue
        T=comper.compT(J)
        D=comper.compD(J)
        H=comper.compH(J)
        sum = T+D+H
        diff = sum - 1/J
        if False:
            print(J, diff, end='')
            print()
        if diff >= 0:
            bestJ = J
        else:
            break
    print(f'place={place}')
    comper.showJStats(bestJ)
    place = place / 10
    prevJ = bestJ

    
